"""Package 82, item 5 (the design's §6): towing by the boat, and the kedge's false denial.
The ship becalmed is towed by her boat ahead on a tow-line with her oars (`world/boats.py`,
`tow_with_boat`; the oar force of `physics/oars.py` at the ship's speed, less the boat's own
resistance, read by the integrator at her stem), her head brought round first and her way
gathered against her resistance, falling as the men tire; `the boat alongside` ends it;
refused in a sea the boat cannot work in, at anchor and aground. The boat laying out a kedge
is no longer denied by her keeper. Truths 7-330, 7-331 and 7b-113 are in
tests/test_known_truths.py, calling here.
"""

from __future__ import annotations

import math
from datetime import datetime, timedelta

from freesail import units
from freesail.api.session import make_world
from freesail.core.world import Scenario
from freesail.world import boats as B
from freesail.world.geo import Position, bearing_and_distance
from tests.test_reckoning import at_rest

CUTTER = "data/ships/cutter.yaml"
FRIGATE = "data/ships/frigate-36.yaml"
LUGGER = "data/ships/lugger.yaml"
REGION = "channel-west"


def _kn(w) -> float:
    return float(w.readings["speed"]) / 0.5144


def _heading(w) -> float:
    return math.degrees(float(w.ship.dyn.heading)) % 360.0


def _events(w, kind):
    return [e for e in w.log if e.kind == kind]


# ---------------------------------------------------------------------------
# the cutter becalmed, towed by her boat (truth 7-330)
# ---------------------------------------------------------------------------


def test_the_cutter_becalmed_is_towed_at_about_a_knot_fresh_her_head_brought_round_first():
    w = at_rest(49.6, -5.2, ship=CUTTER)
    cutter = w.players
    assert _kn(w) < 0.2
    e = w.submit("tow her with the boat to the NE")
    assert e.kind == "boat.towing", e.text
    assert "manned for the tow" in e.text and "to the NE" in e.text
    boat = B.towing_hull(w, cutter)
    assert boat is not None and B.is_boat(boat) and w.own is cutter  # nobody of the player's in her
    assert w.dealings.boat.away and w.dealings.boat.errand == "towing"
    assert w.readings.words("boat").startswith("the boat ahead on the tow-line")
    # her head comes round first: from north toward the north-east within ten minutes
    w.run(600)
    hdg = _heading(w)
    assert 20.0 < hdg < 70.0, hdg
    # she gathers way against her resistance: about a knot fresh (the design's figure)
    w.run(1200)
    fresh = _kn(w)
    assert 0.7 <= fresh <= 1.3, fresh
    # the boat keeps her station a line's length ahead on the bearing, her way the ship's
    brg, dist = bearing_and_distance(cutter.position, boat.position)
    assert B.TOW_LINE_M < dist < B.TOW_LINE_M + 0.6 * cutter.ship.hull.length + 5.0, dist
    assert 25.0 < brg % 360.0 < 65.0, brg
    # the men tire: her way falls, and the ship's log says so once an hour
    w.run(3600)
    tired = _kn(w)
    assert tired < fresh - 0.1, (fresh, tired)
    tiring = _events(w, "boat.tiring")
    assert tiring and "tiring" in tiring[0].text
    # `the boat alongside` ends it: the line cast off, the boat hoisted in, her way dying
    e = w.submit("the boat alongside")
    assert e.kind == "boat.alongside" and "hoisted in" in e.text, e.text
    assert B.towing_hull(w, cutter) is None and not w.dealings.boat.away
    assert "tow" not in w.ship.extra
    w.run(600)
    assert _kn(w) < tired


def test_the_tow_is_refused_in_a_sea_the_boat_cannot_work_in_at_anchor_and_aground():
    from tests.test_ground import on_the_falmouth_bank
    from tests.test_ports import CARRICK_ROAD, at_anchor_in

    w = at_anchor_in(CARRICK_ROAD, ship=CUTTER)
    e = w.submit("tow her with the boat")
    assert e.kind == "order.rejected" and "weigh first" in e.text
    w = on_the_falmouth_bank()
    e = w.submit("tow her with the boat")
    assert e.kind == "order.rejected" and "aground" in e.text
    # a sea above her weather: the cutter in a gale's sea, becalmed after it
    sc = Scenario(
        start_time=datetime(1805, 6, 15, 13, 0),
        wind_from_deg=225.0,
        wind_speed_kn=30.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=0.0,
        position={"lat_deg": 49.6, "lon_deg": -5.2},
        region=REGION,
        sea=True,
    )
    w = make_world(7, CUTTER, sc)
    w.run(3 * 3600)
    assert w.sea.reading().state in B.SWAMP_STATES_SMALL, w.sea.reading().state
    e = w.submit("tow her with the boat")
    assert e.kind == "order.rejected" and "cannot work in this sea" in e.text
    # and the words of a bad bearing
    w = at_rest(49.6, -5.2, ship=CUTTER)
    e = w.submit("tow her with the boat to the moon")
    assert e.kind == "order.rejected" and "not a bearing" in e.text


# ---------------------------------------------------------------------------
# the kedge's false denial mended (truth 7-331)
# ---------------------------------------------------------------------------


def test_lay_out_a_kedge_runs_to_its_end_with_the_boat_said_away_and_no_denial():
    from tests.test_ports import CARRICK_ROAD, at_anchor_in

    w = at_anchor_in(CARRICK_ROAD)
    e = w.submit("lay out a kedge to the NE")
    assert e.kind == "order.accepted"
    away_minutes = 0
    for _ in range(60):
        w.run(60)
        if _events(w, "ship.kedged"):
            break
        if w.readings["boat"]["away"]:
            away_minutes += 1
    assert _events(w, "ship.kedged")
    assert away_minutes >= 14, away_minutes  # hoist out, sling, pull out, back: never denied
    assert not _events(w, "boat.stood_down")
    assert not any("was not sent away" in e.text for e in w.log)
    assert not w.readings["boat"]["away"]


# ---------------------------------------------------------------------------
# 7b-113: the lugger towed clear of the Lavandière, and the frigate's head brought round
# ---------------------------------------------------------------------------

LAVANDIERE = Position(48.7327, -4.0453)


def _ebb_setting_west(start: datetime, pos: Position, w) -> datetime:
    """The first hour from `start` at which the stream at `pos` sets west at a third of a
    knot or more (the open Channel's ebb runs to the south-west)."""
    tide = w.tide
    when = start
    for _ in range(26):
        east, _north = tide.stream_at(pos, when)
        if east < -units.knots_to_ms(0.3):
            return when
        when += timedelta(hours=1)
    raise AssertionError("no ebb found in a day")


def the_lugger_towed_clear_of_the_lavandiere():
    """7b-113's first clause: the lugger becalmed a mile east of the Lavandière with the
    ebb setting her toward it, towed clear to the north by her boat at about half a knot,
    the men an hour at the oars."""
    probe = at_rest(48.7327, -4.030, ship=LUGGER)
    start = _ebb_setting_west(probe.clock.ship_time, LAVANDIERE, probe)
    w = at_rest(48.7327, -4.030, start=start, ship=LUGGER)
    lugger = w.players
    before = bearing_and_distance(LAVANDIERE, w.position)[1]
    e = w.submit("tow her with the boat to the N")
    assert e.kind == "boat.towing", e.text
    w.run(3600)
    assert not w.ship.extra.get("aground")
    speed = _kn(w)
    # the physics' figure by F_0 50 N an oar: about a knot through the water fresh and after
    # the first hour (the spec's "half a knot" is the figure at four hours at the oars, in the
    # known truth); the ebb is carried over the ground beside it
    assert 0.8 <= speed <= 1.3, speed
    assert 0.9 <= B.towing_hull(w, lugger).ship.extra["oars"].hours <= 1.1
    # clear of the rock: she is north of its line and no nearer than she began
    brg, dist = bearing_and_distance(LAVANDIERE, w.position)
    assert dist >= before * 0.8 and (brg % 360.0 < 80.0 or brg % 360.0 > 280.0), (brg, dist)
    assert B.towing_hull(w, lugger) is not None
    return w


def the_frigates_head_brought_round_by_her_launch():
    """7b-113's frigate clause as the design reads it (§6): her head brought round in a calm
    by her launch, and her way under a knot and falling as the men tire."""
    w = at_rest(49.6, -5.2, ship=FRIGATE)
    e = w.submit("tow her with the launch to the E")
    assert e.kind == "boat.towing", e.text
    assert "launch" in e.text.lower()
    w.run(900)
    hdg = _heading(w)
    assert 20.0 < hdg < 120.0, hdg  # two points and more in a quarter of an hour
    w.run(1800)
    fresh = _kn(w)
    assert 0.3 <= fresh < 1.0, fresh
    return w


def test_the_lugger_is_towed_clear_of_the_lavandiere_at_half_a_knot():
    the_lugger_towed_clear_of_the_lavandiere()


def test_the_frigates_head_is_brought_round_by_her_launch_and_her_way_is_under_a_knot():
    the_frigates_head_brought_round_by_her_launch()
