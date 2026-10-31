"""Package 82, item 1 (the design's §3): the world with no ship of the player's.

A scenario with `ship: none` (or `director: observe`, which implies it) builds a World
whose own hull is the observer's, a hull of no ship kept as `hulls[PLAYER_ID]` with no
hull followed: the business and the other ships run under their captains, the drivers
open at the director's station, the ship's orders are refused in words and the readings
of a ship answer "no ship followed", the world orders stand, `follow "<ship>"` moves the
centre to her hull (woken under the cap as the followed hull), `follow nobody` gives the
view back and `look at <where>` moves it. Truths 7-320, 7-321 and 7-334 are in
tests/test_known_truths.py, calling here.
"""

from __future__ import annotations

import io
import json
from pathlib import Path

import pytest

from freesail.api import queries
from freesail.api.readings import NO_SHIP_FOLLOWED_WORDS
from freesail.api.session import ship_factory
from freesail.core import replay
from freesail.core.world import NO_SHIP_FOLLOWED
from freesail.world.scenarios import ScenarioError, begin, load_scenario, make_scenario_world

OBSERVED = "data/scenarios/the-channel-observed.yaml"


def observed_world():
    sf = load_scenario(OBSERVED)
    w = make_scenario_world(sf)
    begin(w, sf)
    return w, sf


def _run_until(w, cond, ticks: int, step: int = 60) -> bool:
    for _ in range(0, ticks, step):
        if cond():
            return True
        w.run(step)
    return cond()


def _write(tmp_path: Path, text: str) -> str:
    p = tmp_path / "observed.yaml"
    p.write_text(text, encoding="utf-8")
    return str(p)


HEAD = """name: A view
seed: 7
start: 1805-06-12T04:00
position: {lat_deg: 49.70, lon_deg: -5.20}
region: channel-west
"""


# ---------------------------------------------------------------------------
# the loader
# ---------------------------------------------------------------------------


def test_ship_none_and_director_observe_make_an_observed_scenario(tmp_path):
    sf = load_scenario(OBSERVED)
    assert sf.scenario.observed and sf.ship_file is None
    assert sf.scenario.director.get("observe") is True and sf.player_seat is None
    assert "No ship of the player's" in sf.lines()[1] and "look at" in sf.lines()[1]
    # `director: observe` alone implies `ship: none`
    sf2 = load_scenario(_write(tmp_path, HEAD + "director: observe\n"))
    assert sf2.scenario.observed and sf2.ship_file is None
    # the mapping form carries it too, beside the grant
    sf3 = load_scenario(_write(tmp_path, HEAD + "director: {observe: true, seats: 2}\n"))
    assert sf3.scenario.observed and sf3.scenario.director["seats"] == 2
    # a ship given on the command line is the player's, and nothing is observed
    w = make_scenario_world(sf, ship="data/ships/cutter.yaml")
    assert not w.observed and w.followed == "the ship" and not w.is_observer
    assert sf.scenario.observed  # the file's own scenario is left as read


@pytest.mark.parametrize(
    ("text", "words"),
    [
        (HEAD + "ship: anything\n", "'none'"),
        (HEAD + "ship: none\nintent: bound for Brest\n", "no standing orders, intent or first"),
        (HEAD + "ship: none\norders: [set plain sail]\n", "first orders"),
        (
            HEAD + "ship: none\nstanding_orders: [data/standing_orders/starter.orders]\n",
            "no standing orders",
        ),
        (HEAD + "ship: none\nstations: {officer: player}\n", "no officer's station"),
        (HEAD + "director: observe\nship: {file: data/ships/cutter.yaml}\n", "no ship of the"),
        (HEAD.split("position:")[0] + "ship: none\n", "needs a position"),
        (HEAD + "director: watch\n", "'observe'"),
    ],
)
def test_what_an_observed_scenario_cannot_carry_is_refused_in_words(tmp_path, text, words):
    with pytest.raises(ScenarioError, match=words):
        load_scenario(_write(tmp_path, text))


# ---------------------------------------------------------------------------
# the observer's hull
# ---------------------------------------------------------------------------


def test_the_observers_world_has_no_hull_followed_and_no_ship_on_the_sea():
    w, _ = observed_world()
    assert w.observed and w.is_observer and w.followed is None
    assert w.own is w.players and w.is_followed  # the shared tick runs for her
    assert w.followed_words == "no ship followed"
    assert w.followed_line.startswith("No ship followed: the observer's view at 49° 42' N")
    assert w.vessels.player_shadow(w) is None
    assert not any(v.name == "the ship" for v in w.vessels.vessels)
    assert "No ship followed: the observer's view at" in w.log.all()[0].text
    assert w.scenario.observed and "observed" in json.dumps(w.save()["scenario"])
    w.run(120)
    # the view does not drift with the tide's stream, and the lookout looks from a boat's
    # height of eye
    assert w.position.lat_deg == pytest.approx(49.70) and w.position.lon_deg == pytest.approx(-5.2)
    assert w.lookout.height_of_eye_m == 2.0
    assert "No ship followed" in w.summary_lines()[-1]


def test_the_observers_readings_answer_no_ship_followed_and_the_ships_orders_are_refused():
    w, _ = observed_world()
    w.run(60)
    r = w.readings
    assert r["speed"] is None and r["heading"] is None and r["sail"] is None
    assert r.words("speed") == NO_SHIP_FOLLOWED_WORDS == r.words("people")
    assert r["true_wind_speed"] > 0 and "knots" in r.words("true_wind_speed")
    assert r["in_sight"]["count"] > 0 and r["daylight"] == "day"
    assert r.as_dict()["speed"] is None and r.as_dict()["war"]
    e = w.submit("set plain sail")
    assert e.kind == "order.rejected" and NO_SHIP_FOLLOWED in e.text
    assert NO_SHIP_FOLLOWED in w.submit("where am i").text
    assert not w.journal  # nothing of the ship's was carried out
    # the world orders stand
    e = w.world_order("port falmouth: price of tin 300")
    assert e.data.get("result") != "refused"
    assert w.ports.ports["falmouth"].market.goods["tin"].price == 300.0
    e = w.world_order("aboard: a cask found stove")
    assert "No ship followed: name her ('aboard the Harpy: ...')" in e.text
    e = w.world_order("aboard the Harpy: a cask found stove")
    assert "aboard the Harpy: found aboard" in e.text
    e = w.world_order("captain: intent bound for Brest")
    assert "No ship followed: a captain order is the followed ship's" in e.text
    e = w.world_order('ship "the ship": crewed')
    assert "No ship of the player's: this world is observed" in e.text
    e = w.world_order('ship "Harpy": intent run home to Brest')
    assert e.data.get("result") != "refused"


def test_follow_moves_the_centre_and_the_cap_wakes_her_and_follow_nobody_gives_the_view_back():
    w, _ = observed_world()
    view = w.position
    with pytest.raises(ValueError, match="No ship of the player's"):
        w.follow("the ship")
    with pytest.raises(ValueError, match="No ship named"):
        w.follow("Nobody Known")
    e = w.follow("Medusa")
    assert e.kind == "driver.follow" and "Following the Medusa" in e.text
    hull = w.hulls["medusa"]
    assert w.followed == "medusa" and w.own is hull and not w.is_observer and w.is_followed
    assert w.position == hull.position != view and w.followed_line == "Following the Medusa."
    assert not hull.awake  # made in the far shape beyond the view's range
    assert _run_until(w, lambda: hull.awake, 240)  # the switch's minute wakes her, followed
    assert w.readings["speed"] is not None and w.readings.words("speed").endswith("knots")
    assert queries.snapshot(w)["ship"]["name"] == "Medusa" and "observer" not in queries.snapshot(w)
    e = w.submit("set the royals")  # an order to the followed hull is hers
    assert e.kind == "order.accepted" and any(x.text == "Order: set the royals." for x in hull.log)
    with pytest.raises(ValueError, match="while she is followed"):
        w.look_at("the Lizard")
    e = w.follow("nobody")
    assert e.kind == "driver.follow" and "Following no ship: the observer's view at" in e.text
    assert w.followed is None and w.own is w.players and w.is_observer
    assert w.position == view and w.readings["speed"] is None
    assert w.players.position == view  # the view stood where it was while she was followed


def test_look_at_moves_the_view_and_a_save_replays_with_the_view_and_the_followed_hull():
    w, _ = observed_world()
    e = w.look_at("the Lizard")
    assert e.kind == "driver.look_at" and "Looking at the Lizard (49° 58' N" in e.text
    assert w.position.lat_deg == pytest.approx(49.96, abs=0.01)
    w.run(60)
    e = w.look_at("49 50 N 5 30 W")
    assert "Looking at 49° 50' N, 5° 30' W" in e.text
    assert w.position.lat_deg == pytest.approx(49.8333, abs=1e-3)
    with pytest.raises(ValueError, match="No place named"):
        w.look_at("Atlantis")
    w.run(60)
    data = json.loads(json.dumps(w.save()))
    copy = replay.replay(data, ship_factory)
    assert copy.observed and copy.followed is None and copy.position == w.position
    assert copy.log.digest() == w.log.digest()
    # and mid-follow
    w.follow("Two Brothers")
    w.run(60)
    data = json.loads(json.dumps(w.save()))
    copy = replay.replay(data, ship_factory)
    assert copy.followed == "two-brothers" and copy.log.digest() == w.log.digest()
    assert copy.players.position == w.players.position


def test_a_world_with_a_ship_refuses_look_at_and_follow_nobody_as_before():
    from tests.test_director import world_at

    w = world_at(49.5, -5.5)
    assert not w.observed and not w.is_observer
    with pytest.raises(ValueError, match="The view is the ship's"):
        w.look_at("the Lizard")
    with pytest.raises(ValueError, match="No ship named"):
        w.follow("nobody")
    assert w.followed_line == f"Following the {w.ship.name}."
    assert w.readings.words("speed") != NO_SHIP_FOLLOWED_WORDS


# ---------------------------------------------------------------------------
# the drivers
# ---------------------------------------------------------------------------


def test_the_drivers_open_at_the_directors_station_and_the_console_reads_the_view():
    from freesail.agents.agent import DIRECTOR
    from freesail.agents.seat import seat_player
    from freesail.ui.console import Console, player_seat_for

    w, sf = observed_world()
    assert player_seat_for(w, None, sf) == "director"
    assert player_seat_for(w, "captain", sf) is None  # the captain's prompt is his own
    assert player_seat_for(w, "officer", sf) == "officer"
    seat = seat_player(w, player_seat_for(w, None, sf), door="console")
    assert seat.station.name == DIRECTOR and w.player_seat is seat
    out = io.StringIO()
    console = Console(w, out=out)

    def said(line: str) -> str:
        out.truncate(0)
        out.seek(0)
        console.handle_line(line)
        return out.getvalue()

    assert said("state").startswith("No ship followed: the observer's view at")
    assert NO_SHIP_FOLLOWED in said("set plain sail")
    truth = said("the truth")
    assert "no ship followed; at 49° 42' N" in truth and "from the view bearing" in truth
    assert "Following the Medusa." in said("follow Medusa")
    assert said("state").startswith("Following the Medusa.")
    assert "while she is followed" in said("look at the Lizard")
    assert "Following no ship" in said("follow nobody")
    assert "Looking at the Lizard" in said("look at the Lizard")
    assert "No place named" in said("look at Atlantis")


def test_the_browsers_snapshot_says_no_ship_followed_and_the_driver_follows_and_looks():
    pytest.importorskip("fastapi")
    from freesail.ui.server import Driver

    w, _ = observed_world()
    snap = queries.snapshot(w)
    assert snap["observer"] is True and snap["ship"]["name"] == "no ship followed"
    assert snap["ship"]["heading"] is None
    assert snap["reckoning"]["view"] and snap["reckoning"]["lat_deg"] == 49.7
    assert snap["reckoning"]["words"].startswith("the observer's view at")
    driver = Driver(w, compression=60.0)
    assert driver.state()["followed"] == {"id": None, "name": "no ship followed"}
    driver.follow("Medusa")
    assert driver.state()["followed"] == {"id": "medusa", "name": "Medusa"}
    assert "observer" not in driver.snapshot()
    with pytest.raises(ValueError):
        driver.look_at("the Lizard")
    driver.follow("nobody")
    driver.look_at("the Lizard")
    assert driver.snapshot()["observer"] is True
    assert driver.state()["followed"]["id"] is None


# ---------------------------------------------------------------------------
# the day (truth 7-320)
# ---------------------------------------------------------------------------


def a_day_observed(hours: float = 24.0, follow_at_hour: float = 20.0):
    """The Channel observed for a day at seed 7 with the business on and a director
    observing (a scripted one with nothing to say), the centre on the view and then on the
    Medusa from `follow_at_hour`; the world, its hull and the lines of the day."""
    from freesail.agents.fake import director_above_the_game
    from tests.test_director import seat_director

    w, _ = observed_world()
    seat_director(w, director_above_the_game([]), every=3600)
    before = len(w.vessels.vessels)
    w.run(int(follow_at_hour * 3600))
    assert w.is_observer and w.followed is None
    w.follow("Medusa")
    hull = w.hulls["medusa"]
    w.run(int((hours - follow_at_hour) * 3600))
    return w, hull, before


@pytest.mark.slow
def test_a_day_observed_runs_with_the_business_on_and_the_centre_where_the_observer_looks():
    w, hull, before = a_day_observed()
    assert w.followed == "medusa" and w.position == hull.position and hull.awake
    assert len(w.vessels.vessels) > before  # the business made ships through the day
    assert any(e.kind.startswith("lookout") or "Sail ho" in e.text for e in w.players.log)
    # the follow's line is written at the hull followed from then on (84's rule)
    assert any(e.kind == "driver.follow" for e in list(w.players.log) + list(hull.log))
    assert w.clock.tick == 24 * 3600
    # the Medusa kept her station through the day under her own captain
    from freesail.world.geo import Position, bearing_and_distance

    deadman = Position(50.22, -4.79)
    assert bearing_and_distance(deadman, hull.position)[1] / 1852.0 < 20.0
