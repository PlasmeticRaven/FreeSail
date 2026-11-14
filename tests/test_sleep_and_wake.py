"""A sleep and a wake change nothing of how a ship lies (package 60; the lead's fourth reading
of 96ccd4d2, ruled by the owner's word: one cause, one test, a table played whole).

Each cell: the cutter Raven under a rules captain begins at anchor in Carrick Road, lying to
(hove to by the order) or under way at sea; with no far captain, with one who plans a passage,
or with one bound nowhere; she is put to sleep, asleep a minute or across a turn of the tide,
with or without a checkpoint written and read while she sleeps; and woken. Then:

- `how_she_lies` gives one answer asleep and awake, and the same as before she slept unless her
  captain moved her (a captain who plans a passage may);
- her tackle agrees with her place: an anchor down only where she lies at anchor, and its ground
  under her (within her scope);
- over the next half hour she behaves as she is said to lie: at her anchor within her scope,
  lying to with under a knot of way, under way sailing (unless her captain gives an order that
  changes it, which is his moving her);
- the wake adds no line but its own (`crew.promoted`).
"""

from __future__ import annotations

import math

import pytest

from freesail import units
from freesail.core import replay
from freesail.ship.parts import AnchorState, ground_tackle
from freesail.world import crews as K
from freesail.world.geo import bearing_and_distance
from freesail.world.sights import greenwich_time
from tests.test_crews import _held_far_cutter, hove_to_world

STARTS = ("at anchor", "lying to", "under way")
CAPTAINS = ("none", "passage", "nowhere")
SLEEPS = ("a minute", "a turn of the tide")
CHECKPOINTS = (False, True)
# off the Lizard in open water, for a ship lying to or under way
AT_SEA = "49 52 N 5 20 W"


def _begin(start: str, captain: str):
    """(world, vessel, her hull) awake and lying as `start` says, her captain as `captain`."""
    from freesail.world.geo import parse_position

    w = hove_to_world()
    if start == "at anchor":
        where = w.ports.find("Falmouth").anchorage.position
    else:
        where = parse_position(AT_SEA)
    v, crew = _held_far_cutter(w, where)
    if start == "at anchor":
        assert crew.submit("come to an anchor", actor="the captain").kind == "ship.anchored"
    crew.captain.seated = False
    w._position = where
    w.crewed_settings = {"cap": 0}  # nobody promoted or demoted but by the test's hand
    intent = {
        "none": "",
        "passage": "bound for Plymouth",
        "nowhere": "wait here for the frigate's orders",
    }[captain]
    if start == "at anchor" and captain == "nowhere":
        intent = "bound for Falmouth"  # come to the port she is bound for: bound nowhere more
    K.promote(w, v)
    if start == "lying to":
        crew.submit("set plain sail", actor="the captain")
        w.run(240)
        crew.submit("heave to", actor="the captain")
        for _ in range(20):
            w.run(60)
            if crew.ship.extra.get("hove_to"):
                break
        assert crew.ship.extra.get("hove_to"), "she never came to be hove to"
        # the cell begins once she lies to steadily: nothing in hand, and her captain's
        # business with the manoeuvre done (a fill away he had waiting for the heave-to to
        # finish is his, before she sleeps, not the sleep's)
        steady = 0
        for _ in range(40):
            w.run(60)
            runner = crew.ship.extra["evolutions"]
            quiet = not runner.in_progress() and not crew.captain._business.get("filling")
            steady = steady + 1 if quiet and crew.ship.extra.get("hove_to") else 0
            if steady >= 3:
                break
        assert steady >= 3, "she never came to lie to steadily"
    elif start == "under way":
        # bound somewhere, so that her captain sails her (bound nowhere, he heaves her to)
        assert w.world_order('ship "Raven": intent bound for Plymouth').data["result"] == "done"
        w.run(600)
    else:
        w.run(60)
    # her captain's intent given once she lies as the cell begins (a captain who plans a
    # passage fills away from lying to, and that is his moving her, not the sleep's)
    if intent:
        assert w.world_order(f'ship "Raven": intent {intent}').data["result"] == "done"
    if captain == "none":
        v.brain = None
    return w, v, crew


def _anchors_under_her(crew) -> bool:
    """Every anchor down has its ground within her scope of her (her tackle agrees with her
    place)."""
    ship = crew.ship
    for a in ground_tackle(ship).anchors:
        if a.state is not AnchorState.DOWN:
            continue
        if a.ground_x is None or a.ground_y is None:
            return False
        off = math.hypot(float(ship.dyn.x) - a.ground_x, float(ship.dyn.y) - a.ground_y)
        if off > a.scope_m + 60.0:
            return False
    return True


def _captain_moved_her(lines) -> bool:
    return any(
        x.kind == "order.accepted" and "By the captain" in x.text and "lead" not in x.text
        for x in lines
    )


@pytest.mark.slow
@pytest.mark.parametrize("checkpoint", CHECKPOINTS, ids=["", "checkpoint"])
@pytest.mark.parametrize("sleep", SLEEPS)
@pytest.mark.parametrize("captain", CAPTAINS)
@pytest.mark.parametrize("start", STARTS)
def test_a_sleep_and_a_wake_change_nothing_of_how_she_lies(
    start, captain, sleep, checkpoint, tmp_path
):
    w, v, crew = _begin(start, captain)
    before = K.how_she_lies(v)
    assert before == start, (before, start)
    K.demote(w, v)
    asleep = K.how_she_lies(v)
    if sleep == "a minute":
        w.run(60)
    else:
        flood = w.tide.at(crew.position, greenwich_time(w)).flood
        for _ in range(48):
            w.run(600)
            if w.tide.at(crew.position, greenwich_time(w)).flood != flood:
                break
    asleep_late = K.how_she_lies(v)
    if checkpoint:
        cp = replay.write_checkpoint(w, tmp_path / "asleep.checkpoint")
        _header, w = replay.read_checkpoint(cp)
        v = w.sea_vessels.find("Raven")
        crew = v.crew
    w._position = crew.position
    n = len(list(crew.log))
    K.promote(w, v)
    awake = K.how_she_lies(v)
    said = [x for x in list(crew.log)[n:] if x.kind != "crew.promoted"]
    moved = asleep_late != before
    if moved:
        # her captain moved her while she slept: the evolution that brings her near body to
        # lie as he left her is worked by her hands, and how she lies is asked when it is done
        w.run(600)
        awake = K.how_she_lies(v)
    # one answer asleep and awake, and the same as before unless her captain moved her (her
    # far brain, by his intent, while she slept: a ship with no far captain is never moved)
    assert asleep_late == awake, (asleep, asleep_late, awake)
    if captain == "none":
        assert not moved, (before, asleep, asleep_late, awake)
    # her tackle agrees with her place
    assert crew.at_anchor == (awake == K.AT_ANCHOR), (awake, crew.at_anchor)
    assert _anchors_under_her(crew)
    # the wake adds no line but its own (where her captain moved her while she slept, the
    # evolution that brings her near body to lie as he left her is the wake's own work)
    if not moved:
        assert not said, [f"{x.kind}: {x.text}" for x in said]
    # the next half hour as she is said to lie
    where = crew.position
    n = len(list(crew.log))
    fastest = 0.0
    for _ in range(30):
        w.run(60)
        fastest = max(fastest, abs(float(crew.ship.dyn.u)))
    moved = bearing_and_distance(where, crew.position)[1]
    lines = list(crew.log)[n:]
    assert _anchors_under_her(crew)
    if _captain_moved_her(lines):
        return
    if awake == K.AT_ANCHOR:
        scope = ground_tackle(crew.ship).riding_by().scope_m
        assert crew.at_anchor and moved < scope + 60.0, (moved, scope)
    elif awake == K.LYING_TO:
        assert units.ms_to_knots(fastest) < 1.0, units.ms_to_knots(fastest)
    else:
        assert moved > 300.0, moved
