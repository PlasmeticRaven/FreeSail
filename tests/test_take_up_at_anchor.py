"""The ship he takes up asleep at her anchor is laid at it whole (package 60, the lead's cut,
ruling 3): one anchor, the first `scripts.cannot_anchor` passes, down on the ground under her
at the scope the chart's depth wants, brought up; nothing set; no way; and an hour later in
ordinary weather she is where she was, not dragging. Where no anchor can hold her, nothing is
done beyond the trunk's wake and her log says why in one line; no evolution is started.

Every hull file is played, each at an anchorage (her far body brought to an anchor by the far
order, with no far captain after it, as a ship he left lies) and in ordinary (laid up by the
world order). The
take-up is `command.take_up` with him put aboard her, as the order does once he is aboard.
"""

from __future__ import annotations

import math

import pytest

from freesail.ship.parts import AnchorState, ground_tackle
from freesail.world import command, knowledge
from freesail.world import crews as K
from freesail.world.ships import DESCRIPTIONS
from tests.test_boat_hull import CARRICK_ROAD
from tests.test_ordnance import at_anchor_in
from tests.test_ship_changed import _wo

# one description for each hull file (the first that names it)
RIGS: dict[str, str] = {}
for _words, _spec in DESCRIPTIONS.items():
    RIGS.setdefault(str(_spec["file"]), _words)
PLACES = ("an anchorage", "ordinary")
# in Carrick Road, where the company tests lay the "Fly" (tests/test_company_moved.py)
LARK_AT = "50 09.9 N 5 02.3 W"
WREN_AT = "50 09.8 N 5 02.2 W"
# how far the ground may come home as the anchor bites (JUDGEMENT: measured 2 to 12 m on the
# thirteen hulls in Carrick Road; a band, not a figure)
BITES_WITHIN_M = 25.0


def _asleep(place: str, words: str = "cutter", name: str = "Lark", where: str = LARK_AT):
    """(the world, her vessel, her hull, his person): a ship of `words` asleep at Falmouth,
    given him; at an anchorage (her far body brought to an anchor by the far order, and no far
    captain after it, as a ship he left lies), or in ordinary (laid up by the world order)."""
    w = at_anchor_in(CARRICK_ROAD)
    w.crewed_settings = {"cap": 0}  # nobody woken but by the take-up
    _wo(
        w,
        f'ship: a {words} "{name}" of Britain at {where}, '
        "bound for Falmouth, intent: bound for Falmouth",
    )
    v = w.sea_vessels.find(name)
    v, hull = K.station_world(w, name)
    assert not hull.awake
    if place == "ordinary":
        _wo(w, f'ship "{name}": in ordinary at Falmouth')
        assert v.brain is None
    else:
        e = hull.submit("come to an anchor", actor="the captain")
        assert e.kind == "ship.anchored", e.text
        # her far captain taken off, as a ship he left lies (a far captain bound for the port
        # she lies in ends her voyage, and the trunk takes her off the sea: the cut's report)
        v.brain = None
    w.run(60)
    assert not hull.awake and v.plan and v.plan[0][0] == "anchor"
    me = knowledge.players_person(w)
    command.give(w, v, me, by="the test")
    return w, v, hull, me


def _take_up(w, hull, me):
    from freesail.world.movement import put_aboard

    put_aboard(w, me, hull, "quarterdeck", by="the boat")
    command.take_up(w, me, hull)
    assert w.players is hull and hull.awake


def _laid(hull):
    """She lies at one anchor on the ground under her, brought up, nothing set, no way."""
    ship = hull.ship
    down = [a for a in ground_tackle(ship).anchors if a.state is AnchorState.DOWN]
    assert len(down) == 1, [(a.id, a.state.value) for a in ground_tackle(ship).anchors]
    a = down[0]
    from freesail.physics.anchor import hawse_position

    hx, hy = hawse_position(ship)  # the cable runs from her hawse to the ground
    off = math.hypot(hx - a.ground_x, hy - a.ground_y)
    assert a.brought_up and off <= a.scope_m + 1.0, (off, a.scope_m)
    assert not [s for s, x in ship.sails.items() if x.is_set]
    from freesail.evolutions.scripts import _ground_speed

    # no way over the ground (the stream runs past a ship held at her anchor)
    assert _ground_speed(ship) < 0.1, _ground_speed(ship)
    return a


@pytest.mark.slow
@pytest.mark.parametrize("place", PLACES)
@pytest.mark.parametrize("words", sorted(RIGS.values()))
def test_a_ship_taken_up_asleep_at_her_anchor_is_laid_at_it_on_every_hull(words, place):
    w, v, hull, me = _asleep(place, words)
    _take_up(w, hull, me)
    a = _laid(hull)
    laid = (a.ground_x, a.ground_y)
    # the anchor bites as she first comes back on her cable (a few metres: `Anchor.drag_m`),
    # and then holds: in the second half hour the ground does not move
    w.run(1800)
    bitten = (a.ground_x, a.ground_y)
    assert math.dist(laid, bitten) < BITES_WITHIN_M, math.dist(laid, bitten)
    w.run(1800)
    b = _laid(hull)
    assert b is a and (b.ground_x, b.ground_y) == bitten and not b.dragging


def test_an_anchor_marked_down_on_ground_a_mile_off_is_laid_again_under_her():
    w, v, hull, me = _asleep("an anchorage")
    ship = hull.ship
    stale = ground_tackle(ship).anchors[0]
    stale.state = AnchorState.DOWN
    stale.ground_x, stale.ground_y = float(ship.dyn.x) + 1852.0, float(ship.dyn.y)
    stale.scope_m = 100.0
    _take_up(w, hull, me)
    _laid(hull)


@pytest.mark.parametrize("case", ["no bottom", "too deep", "every anchor lost"])
def test_where_no_anchor_holds_her_nothing_is_done_but_her_line(case, monkeypatch):
    w, v, hull, me = _asleep("ordinary")
    if case == "no bottom":
        monkeypatch.setattr(hull.chart, "depth_at", lambda position: None)
    elif case == "too deep":
        monkeypatch.setattr(hull.chart, "depth_at", lambda position: 2000.0)
    else:
        for a in ground_tackle(hull.ship).anchors:
            a.state = AnchorState.LOST
    n = len(list(hull.log))
    _take_up(w, hull, me)
    said = [x for x in list(hull.log)[n:] if x.kind == "ship.not_anchored"]
    assert len(said) == 1 and said[0].text.startswith("No anchor of hers will hold her where")
    assert not hull.at_anchor
    runner = hull.ship.extra.get("evolutions")
    assert runner is None or not runner.in_progress()


def test_a_second_take_up_lays_her_again():
    """Taken up from ordinary, left laid up for another ship, asleep, given him again and
    taken up a second time: laid at her anchor again, one anchor on the ground under her."""
    w, lark, lark_hull, me = _asleep("ordinary")
    _take_up(w, lark_hull, me)
    _laid(lark_hull)
    where = WREN_AT
    _wo(
        w,
        f'ship: a cutter "Wren" of Britain at {where}, '
        "bound for Falmouth, intent: bound for Falmouth",
    )
    wren, wren_hull = K.station_world(w, "Wren")
    _wo(w, 'ship "Wren": in ordinary at Falmouth')
    w.run(60)
    command.give(w, wren, me, by="the test")
    from freesail.world.movement import put_aboard

    put_aboard(w, me, wren_hull, "quarterdeck", by="the boat")
    command.take_up(w, me, wren_hull, how="laid up")
    w.crewed_settings = {"cap": 0, "range_nm": -5.0}  # he sails away: she sleeps
    w.run(120)
    assert not lark_hull.awake and lark.plan and lark.plan[0][0] == "anchor"
    command.give(w, lark, me, by="the test")
    _take_up(w, lark_hull, me)
    _laid(lark_hull)


def test_an_errand_for_the_old_ship_at_her_anchor_is_refused_in_words():
    """The cut's ruling 5 (a): an officer left at her anchor keeps her there (nobody aboard
    weighs of his own accord), so an errand given him at the take-up would be accepted and
    never sailed; it is refused, saying what works, nothing changed."""
    from freesail.world.command import CommandError
    from freesail.world.movement import put_aboard

    w, lark, lark_hull, me = _asleep("ordinary")
    put_aboard(w, me, lark_hull, "quarterdeck", by="the boat")
    old = w.players
    assert old.at_anchor
    with pytest.raises(CommandError) as refused:
        command.take_up(
            w, me, lark_hull, how="left", officer="Mr Pearce", intent="bound for Plymouth"
        )
    assert str(refused.value) == (
        "The Sherbourne lies at her anchor, and Mr Pearce will keep her so; nobody aboard her "
        "will weigh of his own accord. Leave her to him, or lay her up."
    ), str(refused.value)
    assert w.players is old  # nothing changed
