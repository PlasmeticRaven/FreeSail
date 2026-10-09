"""The ground, by its orders and its lines (package 37f, part two; the review of gate 5c's
playtests, 5.8, 8.2 and 10.4, 10.5).

An anchor's name honoured by `veer`, `heave short`, `heave in` and `weigh`, and "to" kept
when one is named; `let go` saying its scope and taking one, with the warnings as the
anchor goes; `heave in`; the dragging said once and then by how far she has come; the
ground's words taken as the mean of the grounds they name, and a note for every port's
road; `come to an anchor in twelve fathoms`, "Brought up" after `let go`, and the water at
low water against her draught; what a ship at anchor or aground may still do; and the
fore-and-aft cast.

The moored state is of this package's own making (a brig moored in Carrick Road by the
game's own orders), since the game's saves are the owner's and are not test fixtures.
"""

from __future__ import annotations

import math
import re
from datetime import datetime

import pytest

from freesail import units
from freesail.api.session import make_world
from freesail.core import replay
from freesail.core.events import Severity
from freesail.core.world import Scenario, _dragging_advice
from freesail.physics import anchor as A
from freesail.ship.parts import AnchorState, ground_tackle

FRIGATE = "data/ships/frigate-36.yaml"
SCHOONER = "data/ships/topsail-schooner.yaml"
CUTTER = "data/ships/cutter.yaml"
BRIG = "data/ships/brig.yaml"
CARRICK_ROAD = {"lat_deg": 50.160, "lon_deg": -5.034}  # sixteen fathoms, mud
OUTER_ROAD = {"lat_deg": 50.133, "lon_deg": -5.035}  # nine fathoms, nine cables from the land
ST_JUST_POOL = {"lat_deg": 50.1826, "lon_deg": -5.0282}  # ten fathoms, a cable from the land
CROSS_ROAD = {"lat_deg": 50.178, "lon_deg": -5.027}  # eight fathoms, two cables from the land
OFF_THE_ENTRANCE = {"lat_deg": 50.082, "lon_deg": -5.000}  # thirty fathoms
A_SHOAL = {"lat_deg": 50.1460, "lon_deg": -5.0328}  # two fathoms at the chart's datum
ON_THE_GROUND = {"lat_deg": 50.156, "lon_deg": -5.020}  # dry at St Mawes
THE_GOULET = {"lat_deg": 48.3399, "lon_deg": -4.5776}  # twenty fathoms, rock and mud


def road_world(
    ship=BRIG, where=None, heading=200.0, knots=12.0, from_deg=225.0, speed_kn=0.0, hour=10, **kw
):
    sc = Scenario(
        start_time=datetime(1805, 6, 10, hour, 0),
        wind_from_deg=from_deg,
        wind_speed_kn=knots,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=heading,
        ship_speed_kn=speed_kn,
        position=where or CARRICK_ROAD,
        region="channel-west",
        **kw,
    )
    return make_world(7, ship, sc)


def events(world, kind):
    return [e for e in world.log if e.kind == kind]


def run_until(world, kinds, minutes):
    kinds = (kinds,) if isinstance(kinds, str) else kinds
    for _ in range(minutes * 6):
        world.run(10)
        for kind in kinds:
            if events(world, kind):
                return events(world, kind)[-1]
    raise AssertionError(f"no {kinds} in {minutes} minutes")


def at_anchor(ship=BRIG, where=None, **kw):
    w = road_world(ship, where, **kw)
    w.run(60)
    assert w.submit("let go the best bower").kind == "order.accepted"
    w.run(300)
    assert w.at_anchor
    return w


def scopes(world):
    return {a.id: round(a.scope_fathoms) for a in ground_tackle(world.ship).anchors if a.down}


@pytest.fixture(scope="module")
def moored_brig(tmp_path_factory):
    """The brig moored in Carrick Road by `let go` and `moor`: eighty-two fathoms on each
    bower, riding by the best bower. Kept as a checkpoint, and each test takes a fresh
    copy of her."""
    w = at_anchor(BRIG)
    assert w.submit("moor").kind == "order.accepted"
    run_until(w, "ship.moored", 90)
    w.run(600)
    assert scopes(w) == {"best_bower": 82, "small_bower": 82}
    assert ground_tackle(w.ship).riding_by().id == "best_bower"
    return replay.write_checkpoint(w, tmp_path_factory.mktemp("moored") / "brig.ckpt")


def moored(path):
    return replay.read_checkpoint(path)[1]


# ---------------------------------------------------------------------------
# Items 5, 6 and 8: the anchor named, "to", and `heave in`
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "order, anchor, fathoms",
    [
        # "to" is kept wherever the anchor's name stands (item 6)
        ("veer to 90 fathoms", "best_bower", 90),
        ("veer the best bower to 90 fathoms", "best_bower", 90),
        ("veer to 90 fathoms on the best bower", "best_bower", 90),
        ("veer the small bower to 90 fathoms", "small_bower", 90),
        ("veer to 90 fathoms on the small bower", "small_bower", 90),
        # and a bare number is so much more
        ("veer 10 fathoms", "best_bower", 92),
        ("veer the small bower 10 fathoms", "small_bower", 92),
        ("veer 10 fathoms on the small bower", "small_bower", 92),
        # `heave in` to a scope, or so much, with or without the anchor's name (item 8)
        ("heave in to 70 fathoms", "best_bower", 70),
        ("heave in 10 fathoms", "best_bower", 72),
        ("heave in the small bower to 70 fathoms", "small_bower", 70),
        ("heave in 10 fathoms on the small bower", "small_bower", 72),
    ],
)
def test_the_cable_worked_is_the_named_anchors_and_to_is_kept(moored_brig, order, anchor, fathoms):
    """Game 9, moored: `veer the small bower to 80 fathoms` veered the best bower, and
    `veer the best bower to 80 fathoms` veered eighty more. Each order works the anchor it
    names (the anchor she rides by when it names none), to the scope or by the length it
    says, and leaves the other cable as it was."""
    w = moored(moored_brig)
    assert w.submit(order).kind == "order.accepted"
    w.run(600)
    other = "small_bower" if anchor == "best_bower" else "best_bower"
    assert scopes(w) == {anchor: fathoms, other: 82}
    name = ground_tackle(w.ship).get(anchor).name
    said = events(w, "cable.hove_in" if order.startswith("heave") else "cable.veered")[-1]
    assert said.text.split(".")[0].endswith(f"on {name}") or f"on {name}," in said.text


def test_the_refusals_name_the_anchor_she_rides_by_and_what_would_do_it(moored_brig):
    w = moored(moored_brig)
    # a "to" that is less than what is out is refused, with the order that does it
    e = w.submit("veer to 60 fathoms")
    assert e.kind == "order.rejected"
    assert "the best bower has eighty-two fathoms out already" in e.data["reason"]
    assert "heave in to 60 fathoms" in e.data["reason"]
    # an anchor that is not down: never another anchor in silence
    for order in ("veer the sheet anchor to 90 fathoms", "weigh the kedge", "heave in the kedge"):
        e = w.submit(order)
        assert e.kind == "order.rejected", order
        assert "is at the bows, not down; she rides by the best bower" in e.data["reason"]
    # `heave in` below the depth is a weighing, and is sent to its own orders
    e = w.submit("heave in to 5 fathoms")
    assert e.kind == "order.rejected"
    assert "would have the best bower off the ground" in e.data["reason"]
    assert "'weigh'" in e.data["reason"] and "'heave short'" in e.data["reason"]
    # `heave short` takes no number, and says what does (item 8)
    e = w.submit("heave short 20 fathoms")
    assert e.kind == "order.rejected"
    assert "'Heave short' takes no number" in e.data["reason"]
    assert "heave in to 20 fathoms" in e.data["reason"]
    e = w.submit("weigh 20 fathoms")
    assert e.kind == "order.rejected" and "takes no number" in e.data["reason"]
    assert scopes(w) == {"best_bower": 82, "small_bower": 82}


def test_heave_short_takes_the_anchor_named_and_veers_the_other_cable_as_it_comes(moored_brig):
    """She cannot come over one anchor while the other's cable holds her back: the other
    is veered as the first comes in, and the line says so."""
    w = moored(moored_brig)
    assert w.submit("heave short the small bower").kind == "order.accepted"
    short = run_until(w, "cable.hove_short", 45)
    assert short.text.startswith("Hove short on the small bower: ")
    assert "the best bower's cable veered to a hundred and" in short.text
    now = scopes(w)
    assert now["small_bower"] < 12 and now["best_bower"] > 100
    assert ground_tackle(w.ship).riding_by().id == "best_bower"


def test_weigh_weighs_the_anchor_named_and_says_what_she_rides_by(moored_brig):
    """Game 9, moored: `weigh the small bower` weighed the best bower."""
    w = moored(moored_brig)
    assert w.submit("weigh the small bower").kind == "order.accepted"
    weighed = run_until(w, "ship.weighed", 60)
    assert events(w, "ship.aweigh")[-1].text == "The small bower is aweigh."
    assert weighed.text.startswith(
        "The small bower catted and fished; she rides by the best bower, a hundred and"
    )
    tackle = ground_tackle(w.ship)
    assert not tackle.get("small_bower").down and tackle.get("best_bower").down
    assert tackle.riding_by().id == "best_bower" and w.at_anchor


def test_weighing_an_anchor_she_cannot_come_over_is_refused_in_words(moored_brig):
    """Where the other cable will not reach, the order is refused in words that name the
    anchor she rides by and what would do it (in game 9's last state the small bower's
    hundred and twenty fathoms could not let her come over the best bower)."""
    w = moored(moored_brig)
    tackle = ground_tackle(w.ship)
    tackle.get("small_bower").cable_fathoms = 100.0  # a shorter cable bent to it
    for order in ("weigh", "weigh the best bower"):
        e = w.submit(order)
        assert e.kind == "order.rejected", order
        why = e.data["reason"]
        assert why.startswith("the best bower cannot be hove up while the small bower holds her")
        assert "of the small bower's cable, which is a hundred fathoms in all" in why
        assert "Weigh the small bower first, or unmoor; she rides by the best bower" in why
    assert w.submit("weigh the small bower").kind == "order.accepted"


# ---------------------------------------------------------------------------
# Item 7: `let go` says its scope, and takes one
# ---------------------------------------------------------------------------


def test_let_go_says_what_it_will_do_as_the_order_is_given():
    """Game 9: it veered five times the depth of itself, a hundred and twenty-eight
    fathoms in twenty-six and a half, which the officer met as a veer that "ran past its
    number". The default stays, by the owner's ruling, and the first line says it."""
    w = road_world(where=OUTER_ROAD)
    w.run(60)
    assert w.submit("let go the best bower").kind == "order.accepted"
    w.run(2)
    first = events(w, "evolution.started")[-1]
    assert first.text.endswith(
        "Let go the best bower in nine fathoms; veering to forty-five fathoms, five times "
        "the depth."
    )
    assert not events(w, "anchor.scope_warning")  # nine cables from the land
    w.run(400)
    assert scopes(w) == {"best_bower": 45}


@pytest.mark.parametrize(
    "order",
    [
        "let go the best bower and veer to 30 fathoms",
        "let go the best bower with 30 fathoms",
        "let go the best bower and veer 30 fathoms",
    ],
)
def test_let_go_takes_a_scope_and_veers_to_that_and_no_further(order):
    w = road_world(where=OUTER_ROAD)
    w.run(60)
    assert w.submit(order).kind == "order.accepted"
    w.run(2)
    assert events(w, "evolution.started")[-1].text.endswith(
        "Let go the best bower in nine fathoms; veering to thirty fathoms and no further."
    )
    w.run(400)
    assert scopes(w) == {"best_bower": 30}
    assert ground_tackle(w.ship).get("best_bower").scope_fathoms == pytest.approx(30.0, abs=0.1)


def test_come_to_an_anchor_takes_a_scope_likewise():
    w = road_world(where=OUTER_ROAD)
    w.run(60)
    assert w.submit("come to an anchor and veer to 30 fathoms").kind == "order.accepted"
    up = run_until(w, "ship.brought_up", 40)
    assert events(w, "ship.anchored")[-1].text.endswith("veering to thirty fathoms and no further.")
    assert "thirty fathoms of cable" in up.text and scopes(w) == {"best_bower": 30}


def test_the_scope_is_warned_of_when_she_will_swing_within_a_cable_of_the_land():
    """Notable, as the order is given, by the lookout's judgement of the nearest land:
    in game 9 the officer veered a hundred and twenty-eight fathoms in a berth two cables
    from the shore."""
    w = road_world(where=ST_JUST_POOL)
    w.run(60)
    land = w.lookout.nearest_land(float(w.ship.heading))
    assert land["metres"] < 2 * units.CABLE
    assert w.submit("let go the best bower").kind == "order.accepted"
    w.run(2)
    (warned,) = events(w, "anchor.scope_warning")
    assert warned.severity is Severity.NOTABLE
    assert re.fullmatch(
        r"With fifty-(one|two) fathoms out she will swing within a cable of the land to the "
        r"[A-Za-z -]+\.",
        warned.text,
    ), warned.text
    # two cables from the land the scope the depth wants keeps her clear, and is not
    # warned of; a hundred fathoms there is
    w = road_world(where=CROSS_ROAD)
    w.run(60)
    assert 1.5 * units.CABLE < w.lookout.nearest_land(float(w.ship.heading))["metres"]
    assert w.submit("let go the best bower").kind == "order.accepted"
    w.run(2)
    assert events(w, "evolution.started")[-1].text.endswith("five times the depth.")
    assert not events(w, "anchor.scope_warning")
    w = road_world(where=CROSS_ROAD)
    w.run(60)
    assert w.submit("let go the best bower and veer to 100 fathoms").kind == "order.accepted"
    w.run(2)
    (warned,) = events(w, "anchor.scope_warning")
    assert warned.text.startswith(
        "With a hundred fathoms out she will swing within a cable of the land to the "
    )


def test_the_scope_is_warned_of_when_it_is_more_than_the_cable_she_has():
    w = road_world(where=OFF_THE_ENTRANCE)
    w.run(60)
    depth = units.m_to_fathoms(w.ship.extra["water_depth_m"])
    assert 25.0 < depth < 35.0  # five times it is more than a cable of a hundred and twenty
    assert w.submit("let go the small bower").kind == "order.accepted"
    w.run(2)
    assert "veering all the cable bent to it, a hundred and twenty fathoms, where five times" in (
        events(w, "evolution.started")[-1].text
    )
    (warned,) = events(w, "anchor.scope_warning")
    assert warned.severity is Severity.NOTABLE
    assert warned.text.startswith(
        "The small bower has a hundred and twenty fathoms of cable bent to it, and five times "
        "the depth wants a hundred and "
    )
    assert warned.text.endswith("she will have all of it and no more.")
    # a number beyond the cable is refused outright, as it was
    e = road_world(where=OUTER_ROAD)
    e.run(60)
    no = e.submit("let go the kedge and veer to 150 fathoms")
    assert no.kind == "order.rejected" and "has but a hundred and twenty fathoms" in no.text


# ---------------------------------------------------------------------------
# Item 9: the dragging line
# ---------------------------------------------------------------------------


def come_home(world, seconds, every=1, metres=0.2):
    """Run the world with its riding anchor made to come home `metres` in each `every`th
    second, as the cable's physics marks it when the pull is more than the ground holds."""
    anchor = ground_tackle(world.ship).riding_by()
    for t in range(seconds):
        if t % every == 0:
            anchor.came_home = True
            anchor.moved_m += metres
        world.tick()


def test_a_dragging_is_urgent_once_and_then_says_how_far_she_has_come():
    """Game 9 in the Goulet: eighteen urgent lines in eight hours, each waking the officer.
    Urgent once, when the anchor begins to come home; while it goes on a notable line a
    quarter of an hour at most with how far; "holds again" after a quarter of an hour
    still (five minutes until package 37k), and then the next drag is a new one."""
    w = at_anchor(FRIGATE)
    n0 = len(w.log.all())
    come_home(w, 35 * 60)
    said = [e for e in w.log.all()[n0:] if e.kind.startswith("anchor.")]
    assert [e.kind for e in said] == ["anchor.dragging", "anchor.coming_home", "anchor.coming_home"]
    assert said[0].severity is Severity.URGENT
    assert said[0].text.startswith("The best bower is dragging: veer more cable")
    assert all(e.severity is Severity.NOTABLE for e in said[1:])
    assert said[1].tick - said[0].tick >= 15 * 60 and said[2].tick - said[1].tick >= 15 * 60
    assert said[1].text == "The best bower still coming home: a cable since it began."
    assert said[2].text == "The best bower still coming home: two cables since it began."
    # a quarter of an hour without moving (package 37k; five minutes before): it holds
    # again, and the line says how far it came
    n1 = len(w.log.all())
    w.run(14 * 60)
    assert not [e for e in w.log.all()[n1:] if e.kind.startswith("anchor.")]
    w.run(90)
    (holds,) = [e for e in w.log.all()[n1:] if e.kind.startswith("anchor.")]
    assert holds.kind == "anchor.holding" and holds.severity is Severity.ROUTINE
    assert holds.text == "The best bower holds again, having come home two cables and a half."
    # and the next drag is a new one
    n2 = len(w.log.all())
    come_home(w, 3 * 60)
    (again,) = [e for e in w.log.all()[n2:] if e.kind.startswith("anchor.")]
    assert again.kind == "anchor.dragging" and again.severity is Severity.URGENT


def test_a_dragging_that_relapses_within_a_quarter_of_an_hour_is_the_same_dragging():
    """Package 37k (the review's G8; 37f's own note): on bare rock in a tideway an anchor
    held six minutes and came home again, and each relapse was a new urgent line (eight
    in the Goulet's eight hours). An anchor that comes home again within a quarter of an
    hour of its last moving is the same dragging: one urgent line, its metres counted on,
    and "holds again" only when it has held a quarter of an hour."""
    w = at_anchor(FRIGATE)
    n0 = len(w.log.all())
    for _ in range(4):
        come_home(w, 3 * 60, metres=0.5)  # ninety metres in three minutes
        w.run(8 * 60)  # holding eight minutes: past the physics' five, inside the quarter
    said = [e for e in w.log.all()[n0:] if e.kind.startswith("anchor.")]
    assert [e.kind for e in said if e.severity is Severity.URGENT] == ["anchor.dragging"]
    assert not [e for e in said if e.kind == "anchor.holding"]
    # the notable line counts every spell's metres since the dragging began
    coming = [e for e in said if e.kind == "anchor.coming_home"]
    assert coming and coming[-1].text.endswith("since it began.")
    assert coming[-1].data["come_home_m"] > 2 * 90.0  # three spells' metres, not one's
    n1 = len(w.log.all())
    w.run(8 * 60)  # sixteen minutes held in all
    (holds,) = [e for e in w.log.all()[n1:] if e.kind.startswith("anchor.")]
    assert holds.kind == "anchor.holding"
    # four spells of ninety metres: a little short of two cables (185 m a cable)
    assert holds.text == "The best bower holds again, having come home two cables."


def test_an_anchor_that_creeps_a_second_now_and_then_is_not_said_to_drag():
    """The old judgement added every second an anchor had ever crept until five minutes'
    holding together wiped them, so that an anchor snubbed once in two minutes was
    "dragging" in two hours, its cable slack as the line was written."""
    w = at_anchor(FRIGATE)
    n0 = len(w.log.all())
    come_home(w, 3 * 3600, every=120)
    assert not [e for e in w.log.all()[n0:] if e.kind.startswith("anchor.")]
    anchor = ground_tackle(w.ship).riding_by()
    assert not anchor.dragging


def test_the_advice_names_only_what_is_left_to_do():
    """Not "veer more cable" at the bitter end, nor an anchor that is down already."""
    w = at_anchor(FRIGATE)
    tackle = ground_tackle(w.ship)
    best = tackle.get("best_bower")
    assert _dragging_advice(tackle, best) == (
        "veer more cable; let go the small bower, or back her with the stream"
    )
    best.scope_m = units.fathoms_to_m(best.cable_fathoms)  # the bitter end
    assert _dragging_advice(tackle, best) == "let go the small bower, or back her with the stream"
    tackle.get("small_bower").state = AnchorState.DOWN
    assert _dragging_advice(tackle, best) == "let go the sheet anchor, or back her with the stream"
    for a in tackle.anchors:
        a.state = AnchorState.DOWN
    assert _dragging_advice(tackle, best) == (
        "the whole of its cable is out and there is no anchor left to let go"
    )


def test_the_goulets_eight_hours_give_at_most_five_lines_the_first_urgent():
    """The like of game 9's eight hours in the Goulet, from its own state built in a
    scripted world: the brig brought up off the Mingan on 16 June 1805 at 16:42, in twenty
    fathoms on rock and mud, three anchors down by the evening, through the Goulet's tide.
    Where the game had eighteen urgent lines (and this state, before the package, eight),
    at most five lines of the dragging and the holding, the first of them urgent."""
    sc = Scenario(
        start_time=datetime(1805, 6, 16, 16, 40),
        wind_from_deg=225.0,
        wind_speed_kn=6.0,
        gustiness=0.3,
        variability=0.3,
        ship_heading_deg=60.0,
        ship_speed_kn=1.0,
        position=THE_GOULET,
        region="channel-west",
    )
    w = make_world(7, BRIG, sc)
    plan = {
        120: "let go the best bower",
        420: "let go the small bower",
        4 * 3600: "let go the sheet anchor",
    }
    for t in range(1, 8 * 3600 + 1):
        if t in plan:
            assert w.submit(plan[t]).kind == "order.accepted"
        w.tick()
    assert ground_tackle(w.ship).get("best_bower").bottom == "rock and mud"
    said = [e for e in w.log.all() if e.kind.startswith("anchor.") and "warning" not in e.kind]
    assert 1 <= len(said) <= 5
    assert said[0].kind == "anchor.dragging" and said[0].severity is Severity.URGENT
    assert len([e for e in said if e.severity is Severity.URGENT]) <= 2


# ---------------------------------------------------------------------------
# Item 10: the ground's words
# ---------------------------------------------------------------------------


def test_a_note_of_two_grounds_is_the_mean_of_them_and_not_the_worst():
    """A rule, not a table: `GROUND_HOLDING` keeps its figures."""
    hold = dict(A.GROUND_HOLDING)
    assert A.ground_factor("rock") == hold["rock"] and A.ground_factor("mud") == hold["mud"]
    assert A.ground_factor("rock and mud") == pytest.approx((hold["rock"] + hold["mud"]) / 2)
    assert A.ground_factor("sand and rock") == pytest.approx((hold["sand"] + hold["rock"]) / 2)
    assert A.ground_factor("sand and mud") == pytest.approx((hold["sand"] + hold["mud"]) / 2)
    assert A.ground_factor("muddy ground, and sand") == A.ground_factor("sand and mud")
    assert A.ground_factor("rocky") == hold["rock"]  # one ground said twice is one ground
    assert A.ground_factor("rock, rocky") == hold["rock"]
    assert A.ground_factor("") == A.ground_factor("nothing the table knows")


def test_every_ports_road_and_anchorage_has_its_note_of_the_bottom():
    """Brest road had none though the pilot says mud: an anchor let go before the town
    lay on no note at all, and held as on unknown ground. On the whole chart, which holds
    every port's water (package 39b: Biscay north's ports beside the Channel's)."""
    w = road_world(FRIGATE, where={"lat_deg": 49.80, "lon_deg": -5.20}, chart="atlantic-east")
    bare = []
    for pid, port in w.ports.ports.items():
        for label in ("outer_road", "anchorage", "mooring"):
            spot = getattr(port, label, None)
            if spot is None or spot.position is None:
                continue
            if not w.chart.bottom_near(spot.position):
                bare.append((pid, label))
    assert bare == []
    brest = w.ports.ports["brest"]
    assert w.chart.bottom_near(brest.mooring.position) == "mud"
    assert w.chart.feature("brest-road").bottom == "mud"


# ---------------------------------------------------------------------------
# Item 11: three small anchoring faults
# ---------------------------------------------------------------------------


def test_come_to_an_anchor_in_twelve_fathoms_stands_on_till_the_lead_calls_it():
    """As the primer has it: the depth is where she lets go, and the scope is its own."""
    w = road_world(
        FRIGATE,
        where={"lat_deg": 50.105, "lon_deg": -5.030},
        heading=0.0,
        knots=10.0,
        from_deg=200.0,
        speed_kn=3.0,
    )
    w.submit("set topsails")
    w.submit("steer north")
    w.run(300)
    assert units.m_to_fathoms(w.ship.extra["water_depth_m"]) > 12.5
    e = w.submit("come to an anchor in twelve fathoms and veer to 50 fathoms")
    assert e.kind == "order.accepted", e.text
    up = run_until(w, ("ship.brought_up", "evolution.failed"), 120)
    assert up.kind == "ship.brought_up", up.text
    assert any("The lead calls twelve fathoms" in e.text for e in events(w, "evolution.step"))
    let_go = events(w, "ship.anchored")[-1]
    assert 11.0 <= units.m_to_fathoms(let_go.data["anchor"]["depth_m"]) <= 12.6
    assert scopes(w) == {"best_bower": 50}


def test_let_go_the_anchor_logs_brought_up_when_she_is():
    """Game 9: `let go the anchor` never said it, six stand-bys on the event never fired,
    and the captain needed sixty-seven minutes to be sure she rode."""
    w = road_world(where=OUTER_ROAD)
    w.run(60)
    assert w.submit("let go the anchor").kind == "order.accepted"
    up = run_until(w, "ship.brought_up", 15)
    assert up.severity is Severity.NOTABLE
    assert up.text.startswith(
        "Brought up by the best bower in nine fathoms, forty-five fathoms of cable; Riding by"
    )
    w.run(1800)
    assert len(events(w, "ship.brought_up")) == 1  # said once


def test_the_water_at_low_water_is_set_against_her_draught_as_the_anchor_goes():
    """By the master's own tide, never the world's: notable, when what the lead finds less
    the fall he reckons to low water is less than she draws."""
    w = road_world(FRIGATE, where=A_SHOAL, hour=16, knots=8.0)
    w.run(60)
    depth = w.ship.extra["water_depth_m"]
    fall = w.navigation.tide_height_by_master_m()
    draught = w.ship.hull.spec.draught_m
    assert depth > draught + 2.0 and depth - fall < draught  # afloat now, aground at low water
    assert w.submit("let go the best bower").kind == "order.accepted"
    w.run(2)
    (warned,) = events(w, "anchor.depth_warning")
    assert warned.severity is Severity.NOTABLE
    assert warned.text.startswith("By the master's tide there will be ")
    assert warned.text.endswith(f"here at low water, and she draws {round(draught / 0.3048)} feet.")
    # in sixteen fathoms there is nothing to say
    deep = road_world(FRIGATE, hour=16)
    deep.run(60)
    deep.submit("let go the best bower")
    deep.run(2)
    assert not events(deep, "anchor.depth_warning")


# ---------------------------------------------------------------------------
# Item 12: what a ship at anchor, or aground, may do
# ---------------------------------------------------------------------------

SHIPS_WORK = (
    "square the yards",
    "brace the yards square",
    "brace the yards sharp up on the larboard tack",
    "loose sails to dry",
    "back the main topsail",
    "send down the topgallant yards",
    "send down the topgallant masts",
)
HELM_AND_MANOEUVRES = (
    "steer west",
    "come up a point",
    "bear away two points",
    "keep her full",
    "steady",
    "right the helm",
    "helm a lee",
    "trim sails",
    "tack ship",
    "wear ship",
    "heave to",
    "fill away",
    "box haul",
    "wear short round",
    "lie a try",
    "scud",
    "back and fill",
)


def test_a_ship_at_anchor_may_hand_her_sails_and_square_her_yards():
    """Game 9: `furl all sail`, `furl sails`, `square the yards` and `brace the yards
    square` were each refused as "She is at anchor; ... must wait till she weighs." """
    w = at_anchor(FRIGATE)
    for order in SHIPS_WORK:
        e = w.submit(order)
        assert e.kind == "order.accepted", (order, e.text)
        w.run(2)
    # furling is taken on its merits: with every sail in, the answer is that and no other
    for order in ("furl all sail", "furl sails"):
        w2 = at_anchor(FRIGATE)
        e = w2.submit(order)
        assert "at anchor" not in e.text and "Every sail is furled already" in e.text
        assert w2.submit("loose sails to dry").kind == "order.accepted"
        w2.run(600)
        assert w2.submit(order).kind == "order.accepted", order
    # the helm's orders and the manoeuvres wait till she weighs, as before
    for order in HELM_AND_MANOEUVRES:
        e = w.submit(order)
        assert e.kind == "order.rejected", order
        assert e.data["reason"].startswith("She is at anchor; '"), (order, e.text)
        assert e.data["reason"].endswith("' must wait till she weighs."), (order, e.text)


def test_a_ship_aground_may_do_the_same_and_no_manoeuvre():
    w = road_world(FRIGATE, where=ON_THE_GROUND)
    w.run(5)
    assert w.ship.extra.get("aground")
    for order in ("square the yards", "brace the yards square", "loose sails to dry"):
        assert w.submit(order).kind == "order.accepted", order
        w.run(2)
    e = w.submit("furl all sail")
    assert "aground" not in e.text
    for order in ("steer west", "tack ship", "wear ship", "heave to", "trim sails"):
        e = w.submit(order)
        assert e.kind == "order.rejected", order
        assert e.data["reason"].startswith("She is aground; '")
        assert e.data["reason"].endswith("' must wait till she floats.")


# ---------------------------------------------------------------------------
# Item 13: the fore-and-aft cast
# ---------------------------------------------------------------------------


def wind_on_bow(world):
    return math.degrees(units.wrap_pi(world.wind.direction_from - world.ship.dyn.heading))


@pytest.mark.parametrize("ship", [SCHOONER, CUTTER])
@pytest.mark.parametrize("tack", ["starboard", "larboard"])
def test_a_fore_and_after_casts_on_the_tack_ordered(ship, tack):
    """Luce 1884, ch. XXXIV, 'Getting under way.--Schooners': the main boom steadied over
    to the side she is to cast toward, the head sheets aft on the other, the helm for the
    stern-board. In the playtests all three of a schooner's casts timed out, her mainsail
    flat aft and her jib to leeward, and each was logged "She has paid off"; from this
    berth she lies with the wind a point or two on her starboard bow, and before the package's
    last mending cast on the starboard tack whichever was ordered."""
    w = at_anchor(ship, where=OUTER_ROAD)
    assert 0.0 < wind_on_bow(w) < 35.0
    assert w.submit(f"get under way on the {tack} tack").kind == "order.accepted"
    aweigh = run_until(w, "ship.aweigh", 30)
    steps = [e.text for e in events(w, "evolution.step")]
    lee = "larboard" if tack == "starboard" else "starboard"
    assert any(f"the main boom steadied over to {lee}" in s for s in steps)
    assert any("hoist away the jib, its sheet to windward" in s for s in steps)
    done = run_until(w, ("ship.under_way", "evolution.failed"), 20)
    assert done.kind == "ship.under_way", done.text
    assert done.text.startswith(f"Under way on the {tack} tack, ")
    (cast,) = [e for e in events(w, "evolution.step") if "paid off" in e.text]
    assert cast.text.startswith("She has paid off; right the helm, draw the jib")
    assert cast.tick - aweigh.tick < 180  # she casts in a minute or so, not at the timeout
    side = wind_on_bow(w)
    assert (side > 45.0) if tack == "starboard" else (side < -45.0)


def pinned_cast(ship, tack, points_off, seconds):
    """Get under way with her head held `points_off` from the wind (+ the wind on her
    starboard bow) from the moment the anchor is aweigh, as a stream or a spring might
    hold her, and run `seconds` of the cast."""
    w = at_anchor(ship, where=OUTER_ROAD)
    assert w.submit(f"get under way on the {tack} tack").kind == "order.accepted"
    aweigh = run_until(w, "ship.aweigh", 30)
    while w.clock.tick < aweigh.tick + seconds:
        if events(w, "ship.under_way") or events(w, "evolution.failed"):
            break
        w.ship.dyn.heading = units.wrap_2pi(
            w.wind.direction_from - math.radians(points_off * 11.25)
        )
        w.ship.dyn.r = 0.0
        w.tick()
    return w, aweigh


def test_paid_off_is_never_said_on_a_timeout():
    """A ship that hangs head to wind is not said to have cast: she is given till the
    evolution gives up, and it then fails in words, the anchor aweigh."""
    w, aweigh = pinned_cast(SCHOONER, "larboard", 0.5, 1000)
    assert not [e for e in events(w, "evolution.step") if "paid off" in e.text]
    assert not events(w, "ship.under_way")
    (failed,) = events(w, "evolution.failed")
    assert failed.tick - aweigh.tick >= 900
    assert "from the wind and will not cast, the best bower aweigh" in failed.text
    assert "let go again, or cast her by hand" in failed.text


def test_a_cast_the_wrong_way_is_said_and_she_is_got_under_way_on_that_tack():
    w, aweigh = pinned_cast(SCHOONER, "larboard", 5.0, 430)
    (cast,) = [e for e in events(w, "evolution.step") if "paid off" in e.text]
    assert cast.tick - aweigh.tick >= 420
    assert cast.text.startswith(
        "She would not cast on the larboard tack: she has paid off on the starboard; "
    )
    done = run_until(w, ("ship.under_way", "evolution.failed"), 20)
    assert done.kind == "ship.under_way" and "on the starboard tack" in done.text


def test_a_cast_that_stops_short_says_how_far_she_has_paid_off():
    w, aweigh = pinned_cast(SCHOONER, "larboard", -5.0, 430)
    (cast,) = [e for e in events(w, "evolution.step") if "paid off" in e.text]
    assert cast.tick - aweigh.tick >= 420
    assert cast.text.startswith("She has paid off five points and no further; ")
    done = run_until(w, ("ship.under_way", "evolution.failed"), 20)
    assert done.kind == "ship.under_way" and "on the larboard tack" in done.text


def test_the_square_riggers_cast_as_they_did():
    w = at_anchor(BRIG, where=OUTER_ROAD)
    assert w.submit("get under way on the larboard tack").kind == "order.accepted"
    run_until(w, "ship.aweigh", 30)
    steps = [e.text for e in events(w, "evolution.step")]
    assert any("the head yards abox" in s for s in steps)
    assert not any("main boom" in s for s in steps)
    done = run_until(w, ("ship.under_way", "evolution.failed"), 30)
    assert done.kind == "ship.under_way" and "on the larboard tack" in done.text
