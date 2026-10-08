"""The anchor (spec M5 §18; package 34; decision 30): the ground tackle from the ship's
file by her size, the evolutions as Luce gives them, the cable's physics (the scope, the
holding, the drag, the part), the ship riding to the tide, and the orders and readings
of it. The truth for the anchor in spec M5 §19's manner: she brings up in the depth the
scope allows, rides to the tide, and drags in a gale on short scope."""

from __future__ import annotations

from datetime import datetime

import pytest

from freesail import units
from freesail.api import readings as R
from freesail.api.session import make_world
from freesail.core.world import Scenario
from freesail.physics import anchor as A
from freesail.ship.parts import AnchorState, ground_tackle
from freesail.world.geo import bearing_and_distance

FRIGATE = "data/ships/frigate-36.yaml"
SCHOONER = "data/ships/topsail-schooner.yaml"
CUTTER = "data/ships/cutter.yaml"
BRIG = "data/ships/brig.yaml"
REGION = "channel-west"
CARRICK_ROAD = {"lat_deg": 50.160, "lon_deg": -5.034}  # fourteen fathoms, good holding
OUTER_ROAD = {"lat_deg": 50.133, "lon_deg": -5.035}  # ten fathoms, good ground, room to drag
THE_BAY = {"lat_deg": 50.120, "lon_deg": -5.030}  # twelve fathoms, two miles of sea to leeward


def road_world(
    ship=FRIGATE, heading=335.0, knots=12.0, from_deg=225.0, speed_kn=0.0, where=None, **kw
):
    sc = Scenario(
        start_time=datetime(1805, 6, 10, 10, 0),
        wind_from_deg=from_deg,
        wind_speed_kn=knots,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=heading,
        ship_speed_kn=speed_kn,
        position=where or CARRICK_ROAD,
        region=REGION,
        **kw,
    )
    return make_world(7, ship, sc)


def events(world, kind):
    return [e for e in world.log if e.kind == kind]


# ---------------------------------------------------------------------------
# The tackle from the file
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("path", [FRIGATE, SCHOONER, CUTTER, BRIG])
def test_every_ship_carries_ground_tackle_by_her_size_from_the_generator(path):
    """`tools/gen_ships.py` gives each ship her anchors by her burthen (Luce 1866 ch.
    XIV: the bowers at five hundredweight a hundred tons) and her cables by her beam
    (Steel 1794 vol. II): two bowers at the least, a sheet and a stream over two
    hundred tons, a kedge always."""
    w = road_world(path)
    tackle = ground_tackle(w.ship)
    assert tackle is not None
    kinds = [a.kind for a in tackle.anchors]
    assert kinds.count("bower") == 2 and "kedge" in kinds
    bower = tackle.bowers()[0]
    assert bower.weight_kg > 0 and bower.cable_fathoms >= 120 and bower.cable_kn > 0
    for a in tackle.anchors:
        assert a.state is AnchorState.STOWED and not a.down
    burthen = w.ship.spec.hull.burthen_tons if hasattr(w.ship.spec.hull, "burthen_tons") else None
    if "frigate" in path:
        assert "sheet" in kinds and "stream" in kinds
        assert 2200 < bower.weight_kg < 2600  # some 47 hundredweight for 933 tons
    if "cutter" in path:
        assert "sheet" not in kinds  # under two hundred tons
    assert burthen is None or burthen > 0
    assert w.readings["ground_tackle"]["words"].startswith("The best bower")


def test_the_anchors_are_named_as_the_forecastle_names_them():
    w = road_world()
    tackle = ground_tackle(w.ship)
    assert tackle.by_words("the best bower").id == "best_bower"
    assert tackle.by_words("small bower").id == "small_bower"
    assert tackle.by_words("the sheet anchor").kind == "sheet"
    assert tackle.by_words("stream").kind == "stream"
    assert tackle.by_words("the kedge").kind == "kedge"
    assert tackle.by_words("the second anchor").id == "best_bower"  # none down: the first bower
    assert tackle.by_words("").id == "best_bower"
    assert tackle.by_words("the moon") is None


# ---------------------------------------------------------------------------
# The truth: brings up, rides, drags
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def brought_up():
    """The frigate under plain sail in Carrick Road, brought to an anchor by the one
    order, and left riding through a turn of the tide."""
    w = road_world(speed_kn=3.0)
    w.submit("set plain sail")
    w.run(240)
    e = w.submit("come to an anchor")
    assert e.kind == "order.accepted", e.text
    w.run(40 * 60)
    return w


def test_she_brings_up_in_the_depth_the_scope_allows(brought_up):
    """Luce 1866 ch. XXXIV: the sails in, head to the stronger of wind and tide, the
    anchor let go with the way off her, the cable veered to five times the depth (p. 568),
    the sails furled: brought up, the log says by which anchor, in what depth, with how
    much cable, and how she rides."""
    w = brought_up
    tackle = ground_tackle(w.ship)
    riding = tackle.riding_by()
    assert riding is not None and riding.id == "best_bower"
    let_go = events(w, "ship.anchored")
    up = events(w, "ship.brought_up")
    assert len(let_go) == 1 and len(up) == 1
    assert let_go[0].text.startswith("The best bower let go in ")
    assert up[0].text.startswith("Brought up by the best bower in ")
    assert "fathoms of cable; Riding by the best bower to the" in up[0].text
    # the depth the lead called and the scope the depth wants
    depth_fm = units.m_to_fathoms(riding.depth_m)
    assert 10.0 < depth_fm < 20.0
    wanted = A.scope_wanted_m(let_go[0].data["anchor"]["depth_m"])  # the depth at the let-go
    assert abs(riding.scope_m - wanted) < 2.0 and riding.scope_m <= units.fathoms_to_m(
        riding.cable_fathoms
    )
    assert riding.taut and not riding.dragging
    # every sail in, the helm amidships, her way over the ground gone
    assert not any(s.is_set for s in w.ship.sails.values())
    assert w.at_anchor and w.ship.dyn.speed < 0.6
    # the readings
    assert w.readings.words("anchor").startswith("down, riding by the best bower to the")
    # the helm has no say at anchor, nor a manoeuvre; the book's 'keep her full' is refused
    for text in ("steer N", "bear away a point", "trim sails", "tack ship", "heave to"):
        e = w.submit(text)
        assert e.kind == "order.rejected" and "She is at anchor" in e.text, e.text
    cable = w.readings["cable"]
    assert 0.0 <= float(cable) < 0.5 and "fathoms of the best bower's cable out" in cable.words
    assert "the strain" in w.readings.words("cable")
    assert any(ln.startswith("down, riding") for ln in w.summary_lines())


def test_she_rides_to_the_tide_and_swings_at_the_turn(brought_up):
    """Lever 1808, 'Single Anchor'; Luce 1884 App. K: a ship at single anchor lies to
    the stream, and at the turn of the tide the cable slackens and she swings; the log
    says so, and the readings say which tide she rides to."""
    w = brought_up
    before = w.readings["anchor"]["words"]
    first_flood = w.tide_state.flood
    pos0 = w.position
    heading0 = w.ship.dyn.heading
    swung = None
    for _ in range(9 * 60):
        w.run(60)
        turned = events(w, "ship.swung")
        if turned:
            swung = turned[0]
            break
    assert swung is not None and "The cable slack at the turn; she swings to the" in swung.text
    assert swung.data["flood"] != first_flood
    w.run(2 * 3600)  # she comes round slowly on the young ebb, the wind against it
    after = w.readings["anchor"]["words"]
    assert before != after and ("to the ebb" in after or "to the flood" in after)
    # she swung at the turn: six points and more from where she lay before it (she lies
    # between the wind and the tide, Lever's 'windward tide', and never head to the
    # stream alone in a breeze against it)
    swing = abs(units.wrap_pi(w.ship.dyn.heading - heading0))
    assert swing > units.points_to_rad(6.0), units.rad_to_deg(swing)
    # she has not gone anywhere: within her scope of where she brought up
    assert (
        bearing_and_distance(pos0, w.position)[1] < 2.5 * ground_tackle(w.ship).riding_by().scope_m
    )
    # the account kept still: the master runs no distance at anchor
    acc0 = w.navigation.account_now()
    w.run(3600)
    assert bearing_and_distance(acc0, w.navigation.account_now())[1] < 50.0


def test_she_drags_in_a_gale_on_short_scope_and_a_standing_order_sees_it():
    """Lever 1808 p. 97: with a short scope the cable's pull lifts the anchor; Luce 1866
    ch. XXXIV p. 568: ride by five times the depth. The best bower let go in fourteen
    fathoms with twenty of cable in a gale of forty knots drags; the log says so with
    Luce's answers, and the dialect's `when the anchor is dragging` fires."""
    w = road_world(heading=225.0, knots=40.0, where=OUTER_ROAD)
    w.submit('standing order "dragging": when the anchor is dragging then veer cable')
    w.run(60)
    pos0 = w.position
    e = w.submit("let go the best bower in twenty fathoms")
    assert e.kind == "order.accepted"
    w.run(900)
    dragging = events(w, "anchor.dragging")
    assert dragging and dragging[0].text.startswith("The best bower is dragging: veer more cable")
    assert "let go the small bower, or back her with the stream" in dragging[0].text
    fired = [x for x in w.log if x.actor == "standing order 'dragging'"]
    assert fired, "the standing order on the anchor's reading did not fire"
    anchor = ground_tackle(w.ship).get("best_bower")
    assert anchor.scope_fathoms > 20.0  # the book veered
    assert "dragging" in w.readings["anchor"]["words"] or anchor.scope_fathoms >= 20.0
    # she went to leeward over the ground, anchor and all, more than her scope
    assert bearing_and_distance(pos0, w.position)[1] > units.fathoms_to_m(40.0)
    assert anchor.ground_x is not None and anchor.cable_load_kn >= 0.0


def test_the_cable_parts_when_worn_out_and_the_anchor_is_lost():
    """Spec §7.5's rule on the cable: worn above the rating, parted when worn out, the
    anchor lost and the ship adrift (an urgent line); `the anchor` reads lost."""
    w = road_world(heading=225.0, knots=40.0, where=OUTER_ROAD)
    w.run(60)
    w.submit("let go the best bower in twenty fathoms")
    w.run(120)
    anchor = ground_tackle(w.ship).get("best_bower")
    assert anchor.down
    anchor.cable_condition = 0.5
    anchor.cable_load_kn = anchor.cable_kn * 1.3
    A.judge_cables(w.ship, 60.0)
    assert anchor.state is AnchorState.LOST
    parted = (
        [x for x in w.ship.log_lines() if x.kind == "cable.parted"]
        if hasattr(w.ship, "log_lines")
        else []
    )
    w.run(1)
    parted = events(w, "cable.parted")
    assert parted and parted[0].text.endswith("parted; the anchor is lost, and she is adrift.")
    assert parted[0].severity.value == "urgent"
    assert w.readings["anchor"]["words"] == "lost" or "lost" in w.readings.words("ground_tackle")
    assert not w.at_anchor


# ---------------------------------------------------------------------------
# The evolutions and the orders
# ---------------------------------------------------------------------------


def test_weighing_heaves_short_breaks_out_cats_and_fishes_in_order():
    w = road_world(heading=225.0, knots=10.0, where=THE_BAY)
    w.run(60)
    w.submit("let go the best bower")
    w.run(600)
    anchor = ground_tackle(w.ship).get("best_bower")
    scope0 = anchor.scope_m
    assert anchor.down and scope0 > 3.0 * anchor.depth_m
    e = w.submit("heave short")
    assert e.kind == "order.accepted"
    w.run(2400)
    short = events(w, "cable.hove_short")
    assert short and anchor.scope_m < scope0 and anchor.scope_m <= 1.5 * anchor.depth_m + 1.0
    assert not anchor.heaving
    again = w.submit("heave short")
    assert again.kind == "order.rejected" and "hove short already" in again.text
    e = w.submit("weigh")
    assert e.kind == "order.accepted"
    for _ in range(60):  # under way within the hour; no sail is set, and she drifts after
        w.run(60)
        if events(w, "ship.weighed"):
            break
    kinds = [x.kind for x in w.log if x.kind in ("ship.aweigh", "anchor.catted", "ship.weighed")]
    assert kinds[:1] == ["ship.aweigh"] and kinds[-1] == "ship.weighed"
    assert anchor.state is AnchorState.STOWED and anchor.ground_x is None
    weighed = events(w, "ship.weighed")[0]
    assert weighed.text == "The best bower catted and fished; she is under way."
    assert w.readings["anchor"]["words"] == "at the bows"
    assert w.readings.words("cable") == R.NO_ANCHOR_DOWN_WORDS


def test_veering_and_the_second_anchor_and_backing_with_the_stream():
    w = road_world(heading=225.0, knots=10.0, where=OUTER_ROAD)
    w.run(60)
    w.submit("let go the best bower in thirty fathoms")
    w.run(300)
    tackle = ground_tackle(w.ship)
    best = tackle.get("best_bower")
    assert abs(best.scope_fathoms - 30.0) < 0.5
    w.submit("veer to sixty fathoms")
    w.run(600)
    assert abs(best.scope_fathoms - 60.0) < 0.5 and events(w, "cable.veered")
    w.submit("veer twenty fathoms")
    w.run(600)
    assert abs(best.scope_fathoms - 80.0) < 0.5
    e = w.submit("let go the second anchor")
    assert e.kind == "order.accepted"
    w.run(600)
    assert tackle.get("small_bower").down and len(tackle.down()) == 2
    e = w.submit("back the anchor")
    assert e.kind == "order.accepted"
    w.run(900)
    assert events(w, "anchor.backed")
    assert tackle.get("stream").state is AnchorState.DOWN


def test_the_orders_are_refused_in_words_when_they_cannot_be_done():
    w = road_world(heading=225.0, knots=10.0)
    w.run(60)

    def refused(world, text, words):
        e = world.submit(text)
        assert e.kind == "order.rejected" and words in e.text, e.text

    refused(w, "veer cable", "no anchor is down")
    refused(w, "weigh", "no anchor is down")
    refused(w, "veer to the moon", "Veer how much")
    cutter = road_world(CUTTER, heading=225.0, knots=10.0)
    cutter.run(60)
    refused(cutter, "let go the sheet anchor", "no anchor aboard answers to")
    # no anchoring ground: the small bower's one cable of a hundred and twenty fathoms
    # in sixty of water (the best bower has two bent, and would be let go here)
    deep = make_world(
        7,
        FRIGATE,
        Scenario(
            start_time=datetime(1805, 6, 10, 10, 0),
            wind_from_deg=225.0,
            wind_speed_kn=10.0,
            gustiness=0.0,
            variability=0.0,
            position={"lat_deg": 49.3, "lon_deg": -5.5},
            region=REGION,
        ),
    )
    deep.run(60)
    refused(deep, "let go the small bower", "no anchoring ground here")
    # the plane: no chart, no bottom
    plane = make_world(7, FRIGATE, Scenario(wind_speed_kn=10.0, gustiness=0.0, variability=0.0))
    refused(plane, "let go the anchor", "no bottom here")


@pytest.mark.parametrize("path", [SCHOONER, CUTTER, BRIG])
def test_the_small_vessels_let_go_and_weigh_through_the_same_orders(path):
    w = road_world(path, heading=225.0, knots=10.0, where=OUTER_ROAD)
    w.run(60)
    assert w.submit("let go the anchor").kind == "order.accepted"
    w.run(600)
    assert w.at_anchor and events(w, "ship.anchored")
    assert w.submit("weigh").kind == "order.accepted"
    w.run(3600)
    assert not w.at_anchor and events(w, "ship.weighed")


def test_the_readings_and_events_are_in_the_registry_by_kind():
    """Parity (spec M5 §33 item 3): the anchor's readings are rows of the registry with
    kinds the standing dialect reads, and its events named there."""
    for rid, kind in (
        ("anchor", "ground"),
        ("cable", "strain"),
        ("ground_tackle", "ground"),
        ("tide_by_almanac", "position"),
    ):
        assert R.REGISTRY.get(rid).kind == kind
    assert "the anchor" in R.REGISTRY.words() and "the cable" in R.REGISTRY.words()
    for words, kind in (
        ("the anchor let go", "ship.anchored"),
        ("brought up", "ship.brought_up"),
        ("the anchor aweigh", "ship.aweigh"),
        ("the anchor weighed", "ship.weighed"),
        ("the anchor dragging", "anchor.dragging"),
        ("the cable parted", "cable.parted"),
        ("aground", "ship.aground"),
        ("afloat", "ship.afloat"),
        ("the turn of the tide", "ship.swung"),
    ):
        assert R.EVENTS[words].kind == kind
    w = road_world()
    assert w.readings.words("cable") == R.NO_ANCHOR_DOWN_WORDS
    assert w.readings.words("anchor") == "at the bows"
    plane = make_world(7, FRIGATE, Scenario())
    assert (
        plane.readings["anchor"]["state"] == "at the bows"
    )  # the tackle is the ship's, chart or none


# ---------------------------------------------------------------------------
# Package 37d: a dragging anchor is urgent, and the anchor's depth is read where it lies
# (the review of gate 5c's playtests, 5.8 under "Anchoring", and 8.2 item 13)
# ---------------------------------------------------------------------------


def test_a_dragging_anchor_is_an_urgent_line_and_holding_again_a_routine_one():
    from freesail.core.events import Severity

    w = road_world(heading=225.0, knots=40.0, where=OUTER_ROAD)
    w.run(60)
    assert w.submit("let go the best bower in twenty fathoms").kind == "order.accepted"
    w.run(900)
    dragging = events(w, "anchor.dragging")
    assert dragging and all(e.severity is Severity.URGENT for e in dragging)
    assert all(e.severity is Severity.ROUTINE for e in events(w, "anchor.holding"))


def test_an_anchor_let_go_after_a_run_of_sixty_miles_lies_in_the_depth_the_lead_found():
    """Item 13: the anchor's depth was read at a point found by one jump from the
    scenario's origin by the whole voyage's displacement, which drifts from the ship's
    own place with the miles run: "let go in twelve fathoms and a half" and then "Brought
    up ... in six fathoms and a half"; the Harpy "Brought up ... in no water", her
    anchor's point having fallen on the land. After sixty miles made good to Carrick Road
    the anchor lies in the water the ship is in, to the fathom."""
    from freesail.world.geo import Position

    road = Position(CARRICK_ROAD["lat_deg"], CARRICK_ROAD["lon_deg"])
    w = road_world(heading=0.0, knots=6.0, from_deg=180.0)
    # sixty miles of run in her plane, east and north, as a long passage leaves her: the
    # ship's own place carried to the road, her plane's point sixty miles from its start
    east, north = 45 * units.NAUTICAL_MILE, 40 * units.NAUTICAL_MILE
    w.ship.dyn.x, w.ship.dyn.y = east, north
    w._geo_last = (east, north)
    w._position = road
    by_one_jump = w.origin.advanced(east, north)
    assert bearing_and_distance(by_one_jump, road)[1] > 60 * units.NAUTICAL_MILE
    w.run(60)
    at_ship = w.ship.extra["water_depth_m"]
    assert 8.0 < units.m_to_fathoms(at_ship) < 20.0
    assert w.submit("let go the best bower").kind == "order.accepted"
    w.run(120)
    anchor = ground_tackle(w.ship).get("best_bower")
    assert anchor.down and anchor.ground_x is not None
    # where it lies by the world's one frame, and the water over it by the chart there
    lies = w.place_of_plane(anchor.ground_x, anchor.ground_y)
    assert bearing_and_distance(lies, w.position)[1] < 200.0
    over_it = w.chart.depth_at(lies) + w.tide_height_m
    assert anchor.depth_m == pytest.approx(over_it, abs=0.2)
    assert abs(anchor.depth_m - w.ship.extra["water_depth_m"]) < units.fathoms_to_m(1.5)
    # the old arithmetic put it sixty miles off, in another depth altogether
    elsewhere = w.chart.depth_at(w.origin.advanced(anchor.ground_x, anchor.ground_y))
    assert elsewhere is None or abs(elsewhere + w.tide_height_m - anchor.depth_m) > 1.0
