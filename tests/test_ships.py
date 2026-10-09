"""Package 36: other sail at far detail (spec M5 §25; the proposal's §5.2 and §6.1).

A vessel is a hull from one of the four ship files with a polar drawn once from the
file, a nation, a goal and a plan, moved at the roll-up's cadence by the same wind and
tide as the player; the level-of-detail switch with its promotion point; the lookout's
words as she nears (her rig, her colours or none, what she is), `the strangers`, `make
her out` and the chase; the captain's chart draws a sighting by bearing and estimate and
never her position; everything deterministic under the seed.
"""

from __future__ import annotations

import json
import math
from datetime import datetime

import pytest

from freesail import units
from freesail.api.queries import snapshot
from freesail.api.session import make_world
from freesail.core.world import Scenario
from freesail.ship.parts import SailState
from freesail.world import ships as S
from freesail.world.geo import Position, bearing_and_distance, destination, horizon_nm

FRIGATE = "data/ships/frigate-36.yaml"
SCHOONER = "data/ships/topsail-schooner.yaml"
CUTTER = "data/ships/cutter.yaml"
BRIG = "data/ships/brig.yaml"
OPEN_WATER = Position(49.60, -5.40)  # south-west of the Lizard, forty fathoms, no land in sight


def world_at(pos: Position = OPEN_WATER, ship: str = FRIGATE, heading: float = 180.0, **kw):
    sc = Scenario(
        start_time=datetime(1805, 6, 12, 10, 0),
        wind_from_deg=315.0,
        wind_speed_kn=14.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=heading,
        ship_speed_kn=0.0,
        position=pos.to_dict(),
        region="channel-west",
        **kw,
    )
    return make_world(7, ship, sc)


def events(world, kind: str):
    return [e for e in world.log if e.kind == kind]


def put(world, description: str, bearing_deg: float, miles: float, goal: str, **kw) -> S.Vessel:
    """A vessel of `description` put `miles` from the ship on `bearing_deg`, with a goal."""
    pos = destination(world.position, bearing_deg, miles * units.NAUTICAL_MILE)
    spec = {
        "description": description,
        "name": kw.pop("name", description.title()),
        "nation": kw.pop("nation", "britain"),
        "position": pos,
        "goal": goal,
        **kw,
    }
    world.vessels.serial += 1
    return world.vessels.add(S.vessel_from_spec(world, spec, world.vessels.serial))


# ---------------------------------------------------------------------------
# The polar drawn once from the file
# ---------------------------------------------------------------------------


def test_the_polar_is_drawn_from_the_file_and_agrees_with_the_measured_polars():
    """`polar_of` balances the sails model against the hull's resistance at each angle
    off the wind; its beam reaches in fifteen knots are within half a knot of the polars
    the truths measure by sailing (docs/dev/TuningNotes.md, "Where the four ships
    stand": the frigate 8.0, the schooner 7.9, the cutter 7.3, the brig 7.7), and the
    ships stand in the same order."""
    measured = {FRIGATE: 8.0, SCHOONER: 7.9, CUTTER: 7.3, BRIG: 7.7}
    for path, kn in measured.items():
        p = S.polar_of(path)
        assert abs(p.speed_kn(90.0, 15.0) - kn) <= 0.5, (path, p.speed_kn(90.0, 15.0))
        assert p.speed_kn(90.0, 8.0) < p.speed_kn(90.0, 15.0) < p.speed_kn(90.0, 25.0)
        assert p.speed_kn(20.0, 15.0) == 0.0  # nothing closer than the grid's first angle
    assert S.polar_of(CUTTER).speed_kn(90, 15) < S.polar_of(BRIG).speed_kn(90, 15)
    # the fore-and-aft rigs lie closer than the square ones (truths 2 and 74)
    assert S.polar_of(SCHOONER).closest_deg < S.polar_of(FRIGATE).closest_deg
    assert S.polar_of(CUTTER).closest_deg < S.polar_of(BRIG).closest_deg
    # drawn once and the same again
    S.polar_of.cache_clear()
    again = S.polar_of(FRIGATE)
    assert again.speeds_kn == S.polar_of(FRIGATE).speeds_kn


def test_the_descriptions_name_the_four_files_and_the_brigs_two_come_from_her_file():
    assert S.description_key("a merchant brig") == "merchant brig"
    assert S.description_key("brig-sloop") == "brig-sloop"
    assert S.description_key("a ship of the line") is None
    own = S.file_descriptions(BRIG)
    assert set(own) == {"brig-sloop", "merchant brig"}  # one file, two descriptions
    assert S.description("merchant brig")["what"] == own["merchant brig"]["what"]
    assert S.description("brig-sloop")["file"] == S.description("merchant brig")["file"] == BRIG
    assert S.description("frigate")["rig"] == "a ship"  # three masts, square-rigged, from the tops


# ---------------------------------------------------------------------------
# Goals and plans
# ---------------------------------------------------------------------------


def test_a_goal_makes_a_plan_and_a_goal_the_captain_does_not_know_is_refused_in_words():
    w = world_at()
    trade = put(w, "merchant brig", 90.0, 6.0, "trading Falmouth to the Lizard")
    assert trade.cycle and [leg[0] for leg in trade.plan] == ["to", "to"]
    assert trade.goal == "trading Falmouth to the Lizard"
    bound = put(w, "schooner", 180.0, 6.0, "bound from the Longships for the Eddystone")
    assert not bound.cycle and bound.plan[0][2] == "the Eddystone"
    patrol = put(w, "frigate", 270.0, 6.0, "patrolling off Ushant within 6 miles")
    assert patrol.cycle and len(patrol.plan) == 4
    for leg in patrol.plan:
        _, d = bearing_and_distance(Position(48.46, -5.095), leg[1])
        assert abs(d / units.NAUTICAL_MILE - 6.0) < 0.01
    home = put(w, "brig-sloop", 0.0, 6.0, "running home to Brest", nation="france")
    assert home.plan[0][0] == "home" and home.nation == "france"
    mail = put(w, "cutter", 45.0, 6.0, "carrying the mail to Plymouth")
    assert mail.plan[0][2] == "Plymouth"
    letter = put(w, "cutter", 135.0, 6.0, "carrying a letter to the ship", letter="A word.")
    assert [leg[0] for leg in letter.plan] == ["to_ship", "home"] and letter.letter is not None
    with pytest.raises(ValueError, match="no goal a captain at far detail knows"):
        put(w, "cutter", 0.0, 3.0, "hunting the coast")
    with pytest.raises(ValueError, match="knows no such place"):
        put(w, "cutter", 0.0, 3.0, "bound for Valparaiso")
    with pytest.raises(ValueError, match="no description"):
        put(w, "ship of the line", 0.0, 3.0, "bound for Brest")
    # two brigs of one file are not one brig: the sailing factor is drawn once each
    other = put(w, "merchant brig", 100.0, 7.0, "trading Falmouth to the Lizard")
    assert S.SAILING_FACTOR_MIN <= trade.sailing_factor <= 1.0
    assert trade.sailing_factor != other.sailing_factor


def test_she_moves_at_the_roll_ups_cadence_by_the_wind_and_the_tide_and_beats_when_she_must():
    """Truth 67's first half: a far-detail vessel moves once a game minute and no
    oftener, at her polar's speed for her course in the player's wind, the tide's stream
    added over the ground; a mark to windward is beaten for, close-hauled on the tack that
    points nearer, and the pace is no more than the polar gives."""
    w = world_at()
    v = put(w, "merchant brig", 180.0, 8.0, "bound for 49 00 N 5 00 W")  # a reach, SE
    p0 = v.position
    w.run(59)
    assert v.position == p0  # nothing between the minutes
    w.run(1)
    assert v.position != p0
    _, run_m = bearing_and_distance(p0, v.position)
    wind_from, wind_ms = v._wind_at(w)
    off = abs(units.rad_to_deg(units.wrap_pi(math.radians(v.heading_deg - wind_from))))
    polar_kn = v.polar.speed_kn(off, units.ms_to_knots(wind_ms)) * v.sailing_factor
    assert v.speed_kn == pytest.approx(polar_kn)
    # over the ground in a minute: her way and the stream's set (the tide of 34)
    east, north = w.tide.stream_at(v.position, w.clock.ship_time)
    stream_m = math.hypot(east, north) * 60.0
    assert abs(run_m - units.knots_to_ms(v.speed_kn) * 60.0) <= stream_m + 1.0
    assert v.sail_state == "under plain sail"
    # a mark dead to windward (NW): she beats, close-hauled on one tack, and holds it
    beat = put(w, "schooner", 90.0, 10.0, "bound for 50 00 N 6 00 W")
    w.run(600)
    wind_from, wind_ms = beat._wind_at(w)
    off = abs(units.rad_to_deg(units.wrap_pi(math.radians(beat.heading_deg - wind_from))))
    assert abs(off - beat.polar.beat_deg(units.ms_to_knots(wind_ms))) < 0.5 and beat.tack != 0.0
    assert beat.polar.beat_deg(15.0) >= beat.polar.closest_deg
    assert beat.speed_kn > 1.0


def test_the_level_of_detail_switch_promotes_within_two_miles_and_demotes_beyond_three():
    """Spec M5 §25: within `NEAR_DETAIL_NM` of the player a vessel is a near-detail
    object ticked every second, her head swinging at a rate; beyond `NEAR_DEMOTE_NM` she
    is far again. The crewed promotion is milestone 6's, and the switch says so."""
    assert "milestone 6" in (S.Vessel.promote.__doc__ or "")
    w = world_at()
    near = put(w, "cutter", 90.0, 1.5, "bound for 49 36 N 4 30 W")
    far = put(w, "cutter", 270.0, 5.0, "bound for 49 36 N 6 30 W")
    w.run(60)
    assert near.detail == "near" and far.detail == "far"
    p0 = near.position
    w.run(1)
    assert near.position != p0  # ticked by the second
    # her head swings at NEAR_TURN_DEG_S, not at once
    near.heading_deg = 0.0
    w.run(1)
    assert abs(units.wrap_pi(math.radians(near.heading_deg))) <= math.radians(
        S.NEAR_TURN_DEG_S + 1e-9
    )
    # demoted beyond three miles (she stands away eastward at her pace)
    for _ in range(90):
        w.run(60)
        if near.detail == "far":
            break
    _, d = bearing_and_distance(w.position, near.position)
    assert near.detail == "far" and d / units.NAUTICAL_MILE > S.NEAR_DEMOTE_NM


# ---------------------------------------------------------------------------
# The lookout: a sail, her rig, her colours, what she is; lost; the glass; the chase
# ---------------------------------------------------------------------------


def test_the_lookout_hails_a_sail_at_the_horizon_then_her_rig_her_colours_and_what_she_is():
    """Truth 67's second half: "Sail ho!" with a bearing first at the horizon distance
    her rig's height and the eye give, her rig only as she nears (within
    `RIG_MADE_OUT_NM`), her colours within `COLOURS_MADE_OUT_NM`, what she is within
    `MADE_OUT_NM`; each a routine line as it changes, the events for the book."""
    w = world_at()
    w.submit("let go the best bower")  # she rides where she is, so the brig's track passes her
    eye = w.lookout.height_of_eye_m if w.lookout.height_of_eye_m else 30.0
    horizon = horizon_nm(eye, S.rig_height_m(BRIG))
    # a merchant brig standing toward her from beyond the horizon, out of the north-east,
    # for a point a mile south of her
    past = destination(w.position, 180.0, 1.0 * units.NAUTICAL_MILE)
    goal = f"bound for {past.lat_deg:.4f} N {-past.lon_deg:.4f} W"
    v = put(w, "merchant brig", 45.0, horizon + 1.5, goal)
    seen = []
    for _ in range(600):
        w.run(60)
        sails = [e for e in events(w, "lookout.sighting") if e.data.get("seen_as") == "sail"]
        if sails and not seen:
            seen = sails
            _, d = bearing_and_distance(w.position, v.position)
            assert d / units.NAUTICAL_MILE <= horizon + 0.2
            assert (
                seen[0].text.startswith("Sail ho! A sail on the ") and "bearing N" in seen[0].text
            )
            assert seen[0].severity.value == "notable" and "distance_m" not in seen[0].data
        made = events(w, "lookout.made_out")
        if any(e.data["level"] >= 3 for e in made):
            break
    made = events(w, "lookout.made_out")
    levels = [e.data["level"] for e in made]
    assert levels == [1, 2, 3], [e.text for e in made]
    assert made[0].text.startswith("The sail ") and " is a brig, standing to the " in made[0].text
    assert "under plain sail" in made[0].text
    assert made[1].text.startswith("The brig ") and made[1].text.endswith(
        "shows British colours, the red ensign."
    )
    assert made[1].data["colours"] and made[1].data["nation"] == "britain"
    assert "is a merchant brig, deep laden" in made[2].text
    for e in made:
        assert e.severity.value == "routine" and "distance_m" not in e.data
    # the strangers: bearing, estimate and what has been made out; never her position
    st = w.readings["strangers"]
    assert st["in_sight"] and st["count"] == 1
    item = st["items"][0]
    assert {"bearing_deg", "estimate_m", "made_out", "words"} <= set(item)
    assert "lat_deg" not in item and "distance_m" not in item and item["made_out"] == 3
    assert item["words"].startswith("a merchant brig ")
    assert w.readings.words("strangers") == st["words"]


def test_a_stranger_under_no_colours_and_a_sail_lost():
    w = world_at()
    w.submit("let go the best bower")
    # a French brig-sloop out of the north, standing for a point a mile east of her
    past = destination(w.position, 90.0, 1.0 * units.NAUTICAL_MILE)
    goal = f"bound for {past.lat_deg:.4f} N {-past.lon_deg:.4f} W"
    v = put(w, "brig-sloop", 0.0, 3.5, goal, nation="france", colours="none")
    for _ in range(240):
        w.run(60)
        if any(e.data["level"] >= 2 for e in events(w, "lookout.made_out")):
            break
    colours = [e for e in events(w, "lookout.made_out") if e.data["level"] == 2]
    assert colours and colours[0].text.endswith("is a stranger, her colours not made out.")
    assert not colours[0].data["colours"] and colours[0].data["nation"] is None
    # she stands away south at her pace and is lost over the horizon
    v.plan = [("to", Position(47.0, -5.4), "away")]
    for _ in range(400):
        w.run(60)
        if events(w, "lookout.sail_lost"):
            break
    lost = events(w, "lookout.sail_lost")
    assert lost and lost[0].text.endswith(" is out of sight.") and lost[0].data["id"] == v.id
    assert not w.readings["strangers"]["in_sight"]


def test_make_her_out_sends_a_glass_aloft_and_give_chase_puts_the_helm_for_her_bearing():
    w = world_at()
    e = w.submit("make her out")
    assert e.kind == "order.rejected" and "No sail in sight to make out" in e.text
    e = w.submit("give chase")
    assert e.kind == "order.rejected" and "No sail in sight to chase" in e.text
    # a brig at five miles: the eye says a sail; the glass, half as far again, her rig
    put(w, "merchant brig", 90.0, 5.0, "bound for 49 36 N 4 00 W")
    w.run(60)
    assert w.readings["strangers"]["items"][0]["made_out"] == 0
    e = w.submit("make her out")
    assert e.kind == "lookout.made_out" and e.data["glass"] and e.data["level"] == 1
    assert e.text.startswith(
        "The glass aloft makes out the sail abeam to larboard: a brig, standing"
    )
    assert w.readings["strangers"]["items"][0]["made_out"] == 1
    # a sail beyond the glass's reach: nothing more, and the words say why
    far = put(w, "schooner", 270.0, 12.0, "bound for 49 36 N 7 00 W")
    w.run(60)
    e = w.submit("make out the schooner")
    assert e.kind == "order.rejected"  # not made out as a schooner yet: 'a sail'
    e = w.submit("make out the stranger")  # the nearest sail: the brig
    assert e.kind == "lookout.made_out" and e.data["id"] != far.id
    # the chase: the helm put for the brig's bearing, Luce 1884 p. 553
    e = w.submit("chase the brig")
    assert e.kind == "helm.set" and e.text.startswith("Gave chase to a brig")
    assert "bearing E" in e.text and abs(e.data["bearing_deg"] - 90.0) < 2.0
    assert abs(math.degrees(w.ship.dyn.target_heading) - e.data["bearing_deg"]) < 1.0
    # the events for the book
    e = w.submit('standing order "x": at a sail made out then give chase')
    assert e.kind == "standing.given"
    e = w.submit('standing order "y": at a stranger\'s colours made out then make her out')
    assert e.kind == "standing.given"
    e = w.submit('standing order "z": at a sail lost then heave the log')
    assert e.kind == "standing.given"


# ---------------------------------------------------------------------------
# The captain's chart: by account, never the truth
# ---------------------------------------------------------------------------


def test_the_chart_draws_a_sighting_by_bearing_and_estimate_and_the_snapshot_carries_no_position():
    """The proposal's §6.1: other ships "at the fidelity your lookouts can actually
    see". The snapshot's `strangers` are bearing, estimate and words; nothing in the
    snapshot gives a vessel's latitude or longitude, and the doubt grows with the
    estimate (the lookout's own error, 33b's rule, which `client/map.js` draws)."""
    w = world_at()
    v = put(w, "frigate", 60.0, 7.0, "patrolling off 49 40 N 5 10 W within 4 miles")
    w.run(120)
    snap = snapshot(w)
    st = snap["strangers"]
    assert st["count"] == 1
    item = st["items"][0]
    assert item["estimate_m"] and abs(item["bearing_deg"] - 60.0) < 3.0
    truth_bearing, truth_m = bearing_and_distance(w.position, v.position)
    assert abs(item["estimate_m"] / truth_m - 1.0) < 0.6  # an estimate, not the truth
    text = json.dumps(snap)
    for value in (v.position.lat_deg, v.position.lon_deg):
        for digits in (3, 4, 5):
            assert f"{value:.{digits}f}" not in text  # her truth is nowhere in the snapshot
    assert "position" not in json.dumps(st) and "lat_deg" not in json.dumps(st)
    # the drawing's rule is in the client
    js = open("client/map.js", encoding="utf-8").read()
    assert "drawStrangers" in js and "ESTIMATE_DOUBT = 0.15" in js


# ---------------------------------------------------------------------------
# Determinism and the save
# ---------------------------------------------------------------------------


def test_two_worlds_with_the_same_ships_give_one_digest_and_a_checkpoint_holds_them(tmp_path):
    from freesail.api.session import ship_factory
    from freesail.core import replay

    def voyage():
        w = world_at()
        put(w, "merchant brig", 45.0, 12.0, "bound for 49 30 N 5 40 W")
        put(w, "cutter", 200.0, 9.0, "patrolling off 49 30 N 5 30 W within 3 miles")
        w.submit("set plain sail")
        w.run(90 * 60)
        return w

    a, b = voyage(), voyage()
    assert a.log.digest() == b.log.digest()
    assert [v.to_dict() for v in a.vessels.vessels] == [v.to_dict() for v in b.vessels.vessels]
    assert "ships" in a.rng.stream_names() and "sail" in a.rng.stream_names()
    # a checkpoint holds the vessels whole and carries on to the same digest
    path = tmp_path / "ships.json"
    replay.save_to_file(a, path)
    loaded, how = replay.load(path, ship_factory)
    assert how == "checkpoint"
    assert [v.to_dict() for v in loaded.vessels.vessels] == [v.to_dict() for v in a.vessels.vessels]
    a.run(30 * 60)
    loaded.run(30 * 60)
    assert loaded.log.digest() == a.log.digest()


# ---------------------------------------------------------------------------
# A pilot's boat under oars (a port file's `pilot.vessel`; the lead, 2026-10-02)
# ---------------------------------------------------------------------------


def test_a_ports_pilot_vessel_comes_off_as_a_boat_seen_within_two_miles_pulling_at_four_knots(
    tmp_path,
):
    """35b's St Mary's and Roscoff declare what comes off under `pilot.vessel` (a gig,
    the town's boat): her masthead a few metres, so she is seen within `BOAT_SEEN_NM`
    and not at a cutter's horizon, her pace the boat's under oars, the lookout's words
    "pulling off from the land", and the boarding line naming her; Falmouth, Plymouth
    and Brest keep the cutter."""
    from freesail.world import ports as PT

    src = PT.port_files()["falmouth"]
    path = tmp_path / "falmouth.yaml"
    text = src.read_text(encoding="utf-8").replace(
        "  cutter: data/ships/cutter.yaml",
        "  cutter: data/ships/cutter.yaml\n"
        "  vessel: {kind: a gig, name: the Falmouth pilots' gig, under: oars and a lugsail}",
        1,
    )
    path.write_text(text, encoding="utf-8")
    # the frigate standing in for Falmouth from four miles south of the outer road
    w = world_at(Position(50.06, -5.03), heading=20.0)
    w.ports.ports["falmouth"] = PT.load_port(path, w.chart)
    assert w.ports.ports["falmouth"].pilot.craft == "gig"
    # package 37h: the pilot boards when he is taken at his hail
    w.submit('standing order "the pilot": at the pilot\'s hail then take the pilot')
    w.submit("set plain sail")
    for _ in range(150):
        w.run(60)
        if events(w, "port.pilot_aboard"):
            break
    gig = next(v for v in w.vessels.vessels if v.boat)
    assert gig.kind == "a gig" and gig.height_m == S.BOAT_MASTHEAD_M
    assert gig.pace_kn(0.0, 315.0, 14.0) == S.BOAT_PACE_KN
    sails = [e for e in events(w, "lookout.sighting") if e.data.get("seen_as") == "sail"]
    assert sails and sails[0].data["estimate_m"] <= S.BOAT_SEEN_NM * 1.4 * units.NAUTICAL_MILE
    assert "pulling off from the land" in " ".join(
        e.text for e in sails + events(w, "lookout.made_out")
    )
    hail = events(w, "port.pilot_hail")
    assert hail and hail[0].text.startswith("The gig hailed: a pilot for Falmouth")
    aboard = events(w, "port.pilot_aboard")
    assert aboard and "came aboard from the gig" in aboard[0].text
    # the three ports of 35 keep the cutter
    for pid in ("falmouth", "plymouth", "brest"):
        assert PT.load_port(PT.port_files()[pid], w.chart).pilot.craft == "cutter"


# ---------------------------------------------------------------------------
# A chase or a course across the wind: put about, worn or gybed for it (the fold-in of
# m5c-c; package 37m, the owner's ruling 3 of 2026-10-09)
# ---------------------------------------------------------------------------


def _under_way(heading_deg: float, ship: str = FRIGATE):
    """The ship under plain sail with way on, steady on `heading_deg` (the wind from
    315: 25 is close-hauled on the larboard tack), her yards and sheets trimmed."""
    w = world_at(heading=heading_deg, ship=ship)
    w.submit("set plain sail")
    w.submit(f"steer {heading_deg:.0f}")
    for i in range(1500):
        if i % 120 == 0:
            w.submit("trim sails")
        w.tick()
    assert float(w.ship.dyn.speed) > 1.0
    assert abs(units.wrap_pi(float(w.ship.dyn.heading) - math.radians(heading_deg))) < 0.2
    return w


def _until(w, kind: str, seconds: int = 1200):
    """Run until a line of `kind`; the line."""
    n0 = len(w.log)
    for _ in range(seconds):
        w.tick()
        found = [e for e in list(w.log)[n0:] if e.kind == kind]
        if found:
            return found[0]
    raise AssertionError(f"no {kind} in {seconds} s")


def _on(w, course_deg: float, within_deg: float = 6.0) -> bool:
    d = w.ship.dyn
    return abs(units.wrap_pi(float(d.heading) - math.radians(course_deg))) < math.radians(
        within_deg
    )


def test_a_chase_through_the_winds_wake_wears_her_and_does_not_leave_the_yards_braced():
    """The cruise's frigate at 07:30 on the 13th: the chase 175 degrees round, the shorter
    way by the stern, and a plain helm order turned her with the yards braced sharp up
    until every square sail was aback (the audit of m5c-c, C1 and C2). A course whose
    turn passes through the wind's wake is a wear, and she is worn for it; since package
    37m the wear ends on the chase's course, with no book to give it again."""
    w = _under_way(25.0)
    # a brig broad on her starboard quarter: the course for her lies by the stern
    put(w, "merchant brig", 150.0, 4.0, "bound for 48 00 N 5 00 W")
    w.run(60)
    e = w.submit("give chase")
    assert e.kind == "helm.set", e.text
    assert "lies across the wind from her head, by the stern; she is worn round for it" in e.text
    assert e.data["helm"]["verb"] == "wear ship", e.data
    course = e.data["course_deg"]
    wore = _until(w, "ship.wore")
    assert "for the course ordered" in wore.text, wore.text
    assert w.ship.dyn.helm_mode.value == "heading"
    assert abs(math.degrees(w.ship.dyn.target_heading) - course) < 1.0
    assert _on(w, course)
    # a course shaped the same way is worn for too
    w = _under_way(25.0)
    e = w.submit("shape a course for 48 30 N 5 30 W")
    assert "by the stern; she is worn round for it" in e.text, e.text
    assert e.data["judged"] == "wear"


def test_a_chase_through_the_winds_eye_puts_her_about_and_a_small_alteration_is_steered():
    w = _under_way(25.0)
    # a brig broad on the larboard quarter, across the eye the shorter way: put about,
    # having way enough to stay (package 37m; the fold-in wore her)
    put(w, "merchant brig", 240.0, 4.0, "bound for 48 00 N 5 00 W")
    w.run(60)
    e = w.submit("give chase")
    assert e.kind == "helm.set", e.text
    assert "lies across the wind's eye from her head; she is put about for it" in e.text
    assert e.data["helm"]["verb"] == "tack ship", e.data
    # a sail a point or two off the bow: the helm put for her bearing, nothing more
    w = _under_way(25.0)
    put(w, "merchant brig", 40.0, 4.0, "bound for 48 00 N 5 00 W")
    w.run(60)
    e = w.submit("give chase")
    assert e.kind == "helm.set" and "worn round" not in e.text, e.text
    assert e.data["helm"]["verb"] == "steer", e.data


@pytest.mark.parametrize("ship", [FRIGATE, SCHOONER])
def test_a_steer_across_the_winds_eye_puts_her_about_and_the_tack_ends_on_the_course(ship):
    """The owner's ruling 3: a plain `steer` through the wind tacks her as the ship and
    the course allow, the line saying so; the tack ends steering the course."""
    w = _under_way(25.0, ship)
    e = w.submit("steer 245")
    assert e.kind == "helm.order", e.text
    assert e.text.startswith("Helm ordered: steer WSW (245°); WSW (245°) lies across the ")
    assert "wind's eye from her head; she is put about for it. All hands about ship." in e.text
    assert e.data["judged"] == "tack" and e.data["helm"]["verb"] == "tack ship"
    tacked = _until(w, "ship.tacked")
    assert tacked.text.endswith("on the starboard tack, heading WSW (245°), the course ordered.")
    assert w.ship.dyn.helm_mode.value == "heading"
    assert w.ship.dyn.target_heading == pytest.approx(math.radians(245.0))
    assert not [x for x in w.log if x.kind == "ship.missed_stays"]


@pytest.mark.parametrize("ship", [FRIGATE, SCHOONER])
def test_a_steer_into_the_winds_eye_is_steered_as_given_and_the_line_warns(ship):
    """A course given directly into the wind's eye is steered, and she is taken aback:
    the line says so, notable, so that a captain may countermand (the owner's ruling)."""
    w = _under_way(25.0, ship)
    for said, course in (("steer NW", 315.0), ("steer NW by N", 326.25)):
        e = w.submit(said)
        assert e.kind == "helm.order", e.text
        assert "lies in the wind's eye from her head; she will be taken aback." in e.text, said
        assert e.severity.value == "notable" and e.data["judged"] == "aback"
        assert w.ship.dyn.target_heading == pytest.approx(math.radians(course))
    # two points from it is not the eye: on her own tack it is steered as given (pinched)
    e = w.submit("steer N")
    assert e.text == "Helm ordered: steer N (0°)." and "judged" not in e.data


@pytest.mark.parametrize("ship", [FRIGATE, SCHOONER])
def test_a_steer_too_near_the_wind_on_the_other_tack_puts_her_about_and_keeps_her_full(ship):
    w = _under_way(25.0, ship)
    e = w.submit("steer W by N")
    assert (
        "W by N (281°) lies too near the wind to be laid; she is put about and kept full and "
        "by on the starboard tack." in e.text
    ), e.text
    tacked = _until(w, "ship.tacked")
    assert tacked.text.endswith(", full and by."), tacked.text
    assert w.ship.dyn.helm_mode.value == "full_and_by"


def test_a_steer_through_the_wake_wears_a_ship_with_a_square_sail_set_and_else_gybes():
    w = _under_way(25.0)
    e = w.submit("steer SSW")
    assert "SSW (202°) lies across the wind from her head, by the stern; she is worn " in e.text
    assert e.data["judged"] == "wear"
    wore = _until(w, "ship.wore")
    assert wore.text == (
        "Wore ship; braced for the course ordered on the starboard tack, heading SSW (202°)."
    )
    assert _on(w, 202.5)
    # the topsail schooner with her fore topsail and topgallant set is worn as well, her
    # yards to be braced round (the lead's ruling on package 37m: gybed by the helm they
    # were still braced for the old tack and laid her aback)
    w = _under_way(25.0, SCHOONER)
    e = w.submit("steer SSW")
    given = e.tick
    assert "by the stern; she is worn round for it" in e.text, e.text
    wore = _until(w, "ship.wore")
    assert "for the course ordered" in wore.text, wore.text
    assert _on(w, 202.5)
    assert not [x for x in w.log if x.kind == "ship.aback" and x.tick >= given]
    # with no square sail set a fore-and-after gybes by the helm, her boom coming over
    w = _under_way(25.0, SCHOONER)
    for sail in w.ship.sails.values():
        if sail.cls == "square":
            sail.state = SailState.FURLED
    e = w.submit("steer SSW")
    assert e.text == (
        "Helm ordered: steer SSW (202°); SSW (202°) lies across the wind from her head, by "
        "the stern; she gybes for it by the helm."
    )
    assert e.data["judged"] == "gybe" and e.data["helm_mode"] == "heading"
    runner = w.ship.extra["evolutions"]
    assert not [i for i in runner.instances if i.evo.id in ("tack", "wear")]


def test_a_steer_across_the_eye_without_way_to_stay_wears_her():
    """Luce 1866, ch. XXIV, 'Wearing': worn "when ... the vessel has not sufficient
    headway for tacking"."""
    w = _under_way(25.0)
    d = w.ship.dyn
    d.u, d.v = units.knots_to_ms(1.5), 0.0
    d.speed = units.knots_to_ms(1.5)
    e = w.submit("steer 245")
    assert "lies across the wind's eye from her head; she has not way enough to stay, and is " in (
        e.text
    )
    assert e.data["judged"] == "wear", e.text


def test_from_a_reach_she_is_luffed_up_and_put_about_for_a_course_across_the_eye():
    w = _under_way(60.0)
    e = w.submit("steer 245")
    assert e.data["judged"] == "tack", e.text
    luff = _until(w, "helm.order")
    assert luff.text == "Luff up and brace up: she is brought by the wind to go about."
    tacked = _until(w, "ship.tacked", 1500)
    assert "WSW (245°)" in tacked.text and "the course ordered" in tacked.text


def test_a_course_given_while_she_is_going_about_is_steered_when_she_is_round():
    w = _under_way(25.0)
    w.submit("tack")
    w.run(30)
    e = w.submit("steer SW")
    assert e.text == (
        "Helm ordered: steer SW (225°); SW (225°): she is going about, and the course is "
        "given her as she comes round."
    )
    assert e.data["judged"] == "in_hand"
    # a point off, reckoned from her course, is left to the helm as it always was
    e = w.submit("bear away a point")
    assert "judged" not in e.data
    tacked = _until(w, "ship.tacked")
    assert "the course ordered" in tacked.text or "for the course ordered" in tacked.text


def test_a_steer_on_her_own_tack_and_a_drifting_ship_are_steered_as_given():
    w = _under_way(25.0)
    for said in ("steer NNE", "steer E", "come up a point", "bear away two points"):
        e = w.submit(said)
        assert e.kind == "helm.order" and "judged" not in e.data, (said, e.text)
    # no steerage way: steered as given, as it always was
    w = world_at(heading=25.0)
    e = w.submit("steer 245")
    assert e.text == "Helm ordered: steer WSW (245°)." and "judged" not in e.data
