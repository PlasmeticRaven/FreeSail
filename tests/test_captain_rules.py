"""The captain's rules of package 45, Part B (spec M6 §4; the owner's notes of gate m6a):
tack or wear by the ship's state (`put her about`, item 4), sail made again after the
gale whatever his state and a blown head sail replaced (item 5), the glass and the wind
over the hour as a trend that moves the gale lines (item 6), and the port's reach within
which she is in port and trades from the road (item 3)."""

from __future__ import annotations

from datetime import datetime

from freesail.api.session import make_world
from freesail.core.world import Scenario
from freesail.orders import navigation as N
from freesail.world import captains as C
from freesail.world.scenarios import begin, load_scenario, make_scenario_world

FRIGATE = "data/ships/frigate-36.yaml"
SCHOONER = "data/ships/topsail-schooner.yaml"
OPEN_SEA = {"lat_deg": 49.60, "lon_deg": -5.60}  # twenty miles south-west of the Lizard
OFF_THE_LIZARD_S = {"lat_deg": 49.935, "lon_deg": -5.205}  # a mile south of the point
FALMOUTH_OUTER = {"lat_deg": 50.133, "lon_deg": -5.035}
SE_OF_THE_ROAD = {"lat_deg": 50.115, "lon_deg": -5.000}  # a mile and a half from the outer road
S_OF_THE_ROAD = {"lat_deg": 50.088, "lon_deg": -5.035}  # two miles and three quarters south
GALE_TRIAL = "data/scenarios/trials/trial-station-gale.yaml"


def world_at(where, ship=FRIGATE, heading=200.0, speed=0.0, wind=225.0, wind_kn=12.0, **kw):
    sc = Scenario(
        start_time=datetime(1805, 6, 10, 10, 0),
        wind_from_deg=wind,
        wind_speed_kn=wind_kn,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=heading,
        ship_speed_kn=speed,
        position=where,
        chart="channel-west",
        **kw,
    )
    return make_world(7, ship, sc)


def by_the_wind(where=OPEN_SEA, **kw):
    """The frigate under plain sail, braced sharp up and kept full and by for a quarter
    of an hour: way enough on her to stay."""
    w = world_at(where, heading=150.0, speed=4.0, **kw)
    w.submit("set plain sail")
    w.run(300)
    w.submit("brace sharp up")
    w.submit("keep her full and by")
    w.run(900)
    return w


# -- tack or wear (item 4) ---------------------------------------------------------------


def test_put_her_about_tacks_with_whole_sail_in_a_moderate_wind_and_says_why():
    w = by_the_wind()
    assert N.put_about_choice(w.ship) == ("tack ship", "her sail is whole and the wind moderate")
    e = w.submit("put her about")
    assert e.kind == "order.accepted"
    w.run(1)
    note = [x for x in w.log if x.kind == "ship.put_about"]
    assert note and note[-1].text == "Put about: tacking, her sail is whole and the wind moderate."


def test_put_her_about_wears_with_no_head_sail_short_sail_a_gale_or_stays_missed_within_the_hour():
    # no head sail set
    w = by_the_wind()
    w.submit("take in the jib")
    w.submit("take in the fore topmast staysail")
    w.run(600)
    verb, why = N.put_about_choice(w.ship)
    assert verb == "wear ship" and why == "no head sail set"
    # the topsails close-reefed
    w = by_the_wind()
    w.submit("close-reef the topsails")
    w.run(1200)
    verb, why = N.put_about_choice(w.ship)
    assert verb == "wear ship" and why == "the topsails close-reefed"
    # the wind over the wearing line
    w = by_the_wind(wind_kn=36.0)
    verb, why = N.put_about_choice(w.ship)
    assert verb == "wear ship" and f"the wind {int(round(36.0))} knots" in why
    # stays missed within the hour, the sail whole and the wind moderate
    w = by_the_wind()
    w.ship.note("notable", "ship.missed_stays", "Missed stays; she fell off on the old tack.")
    w.run(1)
    verb, why = N.put_about_choice(w.ship)
    assert verb == "wear ship" and why == "she missed stays within the hour"
    w.run(N.MISSED_STAYS_WITHIN_S + 60)
    assert N.put_about_choice(w.ship)[0] == "tack ship"


def test_put_her_about_tacks_regardless_with_the_land_to_leeward_within_two_miles():
    # a mile south of the Lizard with the wind at south: the point under her lee
    w = by_the_wind(OFF_THE_LIZARD_S, wind=180.0, wind_kn=36.0)
    verb, why = N.put_about_choice(w.ship)
    assert verb == "tack ship"
    assert why.startswith("the land ")
    assert why.endswith("to leeward, where wearing would lose the ground")


# -- the glass and the wind over the hour (item 6) ----------------------------------------


def station_captain():
    sf = load_scenario(GALE_TRIAL)
    w = make_scenario_world(sf)
    begin(w, sf)
    w.run(360)
    cap = w.captain
    assert cap is not None and cap.state == "keeping station"
    # the trial's own first minutes forgotten: the glass falling fast and the wind at
    # twenty-seven knots are its weather, and these tests read their own
    cap._wind_log, cap.trend, cap._gale_over_since, cap._calm_since = [], "", None, None
    return w, cap


def test_the_trend_is_read_from_the_glass_and_the_winds_rise_or_fall_within_the_hour():
    _, cap = station_captain()
    p = C.Perception(tick=0, wind_kn=20.0)
    assert cap._read_trend(p) == ""
    assert cap._read_trend(C.Perception(tick=1800, wind_kn=27.0)) == "worsening"
    # the hour run out: the rise is measured from what is left of the log
    assert cap._read_trend(C.Perception(tick=5400, wind_kn=27.0)) == ""
    assert cap._read_trend(C.Perception(tick=5460, wind_kn=20.0)) == "mending"
    assert cap._read_trend(C.Perception(tick=5520, wind_kn=20.0, glass_tendency="rising")) == (
        "mending"
    )
    assert cap._read_trend(C.Perception(tick=5580, wind_kn=20.0, glass_falling_fast=True)) == (
        "worsening"
    )


def test_worsening_brings_the_gale_line_a_force_sooner_and_the_gale_over_line_waits_its_minutes():
    _, cap = station_captain()
    th = cap.doctrine.threshold
    gale, over = float(th("gale_kn")), float(th("gale_over_kn"))
    sooner, later = float(th("worsening_sooner_kn")), float(th("mending_sooner_kn"))
    minutes = float(th("gale_over_minutes"))
    assert (gale, over, sooner, later, minutes) == (40.0, 32.0, 6.0, 4.0, 10.0)
    # the glass steady: the gale at forty, not at thirty-five
    cap._read_trend(C.Perception(tick=0, wind_kn=35.0))
    assert not cap._stimulus("gale", C.Perception(tick=0, wind_kn=35.0))
    assert cap._stimulus("gale", C.Perception(tick=0, wind_kn=40.0))
    # the glass falling fast: the gale at thirty-four
    p = C.Perception(tick=60, wind_kn=35.0, glass_falling_fast=True)
    assert cap._read_trend(p) == "worsening"
    assert cap._stimulus("gale", p)
    # ... and the gale-over line held down with it (twenty-six), so that the band between
    # the two is not a gust's width: thirty knots is not the gale over while it falls
    p = C.Perception(tick=120, wind_kn=30.0, glass_falling_fast=True)
    cap._read_trend(p)
    assert cap._gale_over_since is None and not cap._stimulus("gale over", p)
    # the glass steady again at thirty: under the line, but not for ten minutes yet
    p = C.Perception(tick=180, wind_kn=30.0)
    cap._read_trend(p)
    assert cap._gale_over_since == 180 and not cap._stimulus("gale over", p)
    p = C.Perception(tick=180 + int(minutes * 60), wind_kn=30.0)
    cap._read_trend(p)
    assert cap._stimulus("gale over", p)
    # a gust over the line starts the minutes again
    cap._read_trend(C.Perception(tick=900, wind_kn=33.0))
    assert cap._gale_over_since is None
    # the glass rising: the line four knots sooner (thirty-six)
    p = C.Perception(tick=960, wind_kn=35.0, glass_tendency="rising")
    assert cap._read_trend(p) == "mending" and cap._gale_over_since == 960
    p = C.Perception(tick=960 + int(minutes * 60), wind_kn=35.0, glass_tendency="rising")
    cap._read_trend(p)
    assert cap._stimulus("gale over", p)


# -- sail after the gale, whatever his state (item 5) -------------------------------------


def test_after_the_gale_he_makes_sail_again_by_steps_whatever_his_state_and_bends_a_new_jib():
    """Package 45c, item 3 (package 45 made all sail at once, and the frigate under plain
    sail by the wind after the gale was aback by turns for an hour): the topsails when the
    wind has been under the shorten-sail line ten minutes; the topgallant masts, the reefs,
    a blown head sail bent anew and the jib when it has been under the sail-again line for
    the half hour; the courses last, plain sail, a quarter of an hour after the reefs are
    out."""
    _, cap = station_captain()
    given: list[tuple[str, str]] = []
    cap.give = lambda text, why="": given.append((text, why))  # type: ignore[method-assign]
    th = cap.doctrine.threshold
    again, minutes = float(th("sail_again_kn")), float(th("sail_again_minutes"))
    tops, courses = float(th("topsails_again_minutes")), float(th("courses_again_minutes"))
    assert (again, minutes, tops, courses) == (25.0, 30.0, 10.0, 15.0)
    # the gale met (over the shorten-sail line), the topsails handed, the jib blown out
    cap._read_trend(C.Perception(tick=0, wind_kn=38.0))
    cap._weather_work(C.Perception(tick=0, wind_kn=38.0, topsails_all_set=False), set())
    assert cap._business.get("gale_met") and given == []
    # under the shorten-sail line ten minutes: the topsails, as they stand reefed
    for tick in (60, 60 + int(tops * 60)):
        p = C.Perception(tick=tick, wind_kn=28.0, topsail_reefs=3, topsails_all_set=False)
        cap._weather_work(p, set())
    assert given == [("set the topsails", "the gale easing")]
    given.clear()
    # under twenty-five knots: the half hour not yet run
    blown = C.Perception(tick=1800, wind_kn=20.0, topsail_reefs=3, headsails_blown=["fore.jib"])
    cap._weather_work(blown, set())
    assert given == [] and cap._calm_since == 1800
    # the half hour run: the topgallant masts swayed up, the reefs out, a new jib bent and
    # set, in his state of keeping station (no hove-to book loaded); not the courses yet
    later = C.Perception(
        tick=1800 + int(minutes * 60), wind_kn=20.0, topsail_reefs=3, headsails_blown=["fore.jib"]
    )
    cap._weather_work(later, set())
    assert cap.state == "keeping station"
    assert [t for t, _ in given] == [
        "sway up the topgallant masts",
        "shake out the reefs in the topsails",
        "bend a new fore jib",
        "set the jib",
    ]
    assert {why for _, why in given} == {"the gale over", "blown out in the gale"}
    # the reefs not yet out a quarter of an hour on: the courses wait for them
    t2 = later.tick + int(courses * 60)
    cap._weather_work(C.Perception(tick=t2, wind_kn=20.0, topsail_reefs=1), set())
    assert len(given) == 4
    # the reefs out: plain sail, the courses last
    cap._weather_work(C.Perception(tick=t2 + 60, wind_kn=20.0, topsail_reefs=0), set())
    assert given[4:] == [("set plain sail", "the courses last, the gale over")]
    assert cap._business.get("made_sail_after") and not cap._business.get("gale_met")
    # not given twice
    cap._weather_work(C.Perception(tick=t2 + 120, wind_kn=20.0, topsail_reefs=0), set())
    assert len(given) == 5


def test_with_the_glass_rising_he_makes_sail_in_a_quarter_hour_and_shortens_sooner_when_it_falls():
    _, cap = station_captain()
    given: list[tuple[str, str]] = []
    cap.give = lambda text, why="": given.append((text, why))  # type: ignore[method-assign]
    cap._read_trend(C.Perception(tick=0, wind_kn=38.0))
    cap._weather_work(C.Perception(tick=0, wind_kn=38.0, topsail_reefs=3), set())
    p = C.Perception(tick=60, wind_kn=20.0, topsail_reefs=3, glass_tendency="rising")
    cap._read_trend(p)
    cap._weather_work(p, set())
    p = C.Perception(tick=60 + 15 * 60, wind_kn=20.0, topsail_reefs=3, glass_tendency="rising")
    cap._read_trend(p)
    cap._weather_work(p, set())
    assert [t for t, _ in given] == [
        "sway up the topgallant masts",
        "shake out the reefs in the topsails",
        "set the jib",
    ]
    assert all(why == "the gale over, the weather mending" for _, why in given)
    p = C.Perception(tick=60 + 30 * 60, wind_kn=20.0, topsail_reefs=0, glass_tendency="rising")
    cap._read_trend(p)
    cap._weather_work(p, set())
    assert given[-1] == ("set plain sail", "the courses last, the gale over")
    # the glass falling fast with the wind at twenty-five, plain sail set: the book's
    # shorten-sail line (thirty) comes a force sooner
    given.clear()
    p = C.Perception(tick=2000, wind_kn=25.0, topsail_reefs=0, glass_falling_fast=True)
    cap._read_trend(p)
    cap._weather_work(p, set())
    assert given == [("shorten sail", "the glass falling and the wind rising")]
    cap._weather_work(p, set())
    assert len(given) == 1


def test_after_the_gale_the_topgallant_masts_wait_for_sea_room():
    """Package 45c (the lee-shore trial, a first version: the topgallant masts held the
    offing's tack twenty minutes, she missed stays and took the ground): with the land
    under her lee within `lee_shore_nm` the masts wait, and go up when it is not."""
    _, cap = station_captain()
    given: list[tuple[str, str]] = []
    cap.give = lambda text, why="": given.append((text, why))  # type: ignore[method-assign]
    cap._weather_work(C.Perception(tick=0, wind_kn=38.0, topsail_reefs=3), set())
    for tick in (60, 60 + 30 * 60):
        cap._weather_work(
            C.Perception(tick=tick, wind_kn=20.0, topsail_reefs=3, lee_land_nm=4.0), set()
        )
    assert [t for t, _ in given] == ["shake out the reefs in the topsails", "set the jib"]
    cap._weather_work(
        C.Perception(tick=60 + 31 * 60, wind_kn=20.0, topsail_reefs=1, lee_land_nm=9.0), set()
    )
    assert given[-1] == ("sway up the topgallant masts", "the land no longer under her lee")


# -- in port within the port's reach (item 3) ---------------------------------------------


def anchored_at(where, **kw):
    w = world_at(where, ship=SCHOONER, heading=250.0, **kw)
    w.run(60)
    w.submit("let go the best bower")
    w.run(300)
    assert w.at_anchor
    return w


def test_in_port_is_within_the_ports_reach_and_the_boat_goes_ashore_from_the_road():
    w = anchored_at(FALMOUTH_OUTER)
    assert w.ports.ports["falmouth"].reach_nm == 2.0 and w.ports.in_port().id == "falmouth"
    # a mile and a half from the outer road: in port, and the boat goes for the prices
    w = anchored_at(SE_OF_THE_ROAD, cargo={"purse_pounds": 100.0})
    assert w.ports.in_port() is not None and w.ports.in_port().id == "falmouth"
    e = w.submit("send the boat ashore")
    assert e.kind == "order.accepted" and w.ports.boat.errand == "prices"
    # two miles and three quarters south of the road: at sea
    w = anchored_at(S_OF_THE_ROAD)
    assert w.ports.in_port() is None
    e = w.submit("send the boat ashore")
    assert e.kind == "order.rejected" and "not in port" in e.text
