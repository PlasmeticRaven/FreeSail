"""A hull a model holds is not half blind at far detail (package 82b, item 4;
`Design-DoorAndVisitor.md` §5).

A hull whose captain's station a model holds through a door ranks with the dealings and is
held over the cap, up to `crews.HELD_OVER_CAP` such hulls; past the allowance the cap holds
as before. Where she must sleep, her plan keeps her off the dangers: a leg standing for a
charted rock is put about by the plan's own order, said in her log as an urgent line that
her captain's sample carries. A hull nobody holds through a door keeps the far plan as it was.
"""

from __future__ import annotations

import json

from freesail.agents import Fake, Harness, SamplingPolicy
from freesail.agents.agent import captain as captain_station
from freesail.agents.model import Reply
from freesail.world import crews as K
from tests.test_crews import hove_to_world


def _seat(crew, door="runner", seen=None):
    """A fake at her captain's station, through `door` ("" for none: a test's harness)."""

    def act(last, turns):
        if seen is not None:
            seen.append(json.dumps(last))
        return Reply(text="Aye.")

    policy = SamplingPolicy.in_lockstep(3600, "notable", "urgent")
    h = Harness(crew, captain_station(policy, 3600, world=crew), Fake([act], loop=True))
    h.model_name, h.door = "the fake", door
    h.start()
    return h


def _sail(w, name, where):
    for words in (
        f'ship: a merchant brig "{name}" of Britain at {where}, bound for Falmouth',
        f'ship "{name}": intent bound for Falmouth',
        f'ship "{name}": order heave to for a watch',
    ):
        e = w.world_order(words)
        assert e.data.get("result") == "done", e.text


def test_a_hull_a_model_holds_is_held_over_the_cap_up_to_the_allowance():
    w = hove_to_world()  # the frigate at 49 30 N 5 30 W
    names = [f"B{i}" for i in range(6)]
    for i, name in enumerate(names):
        _sail(w, name, f"49 {31 + 0.5 * i:.1f} N 5 30 W")  # one to three and a half miles
    w.run(61)
    ships = [w.vessels.find(n) for n in names]
    crewed = lambda: [v.name for v in K.crewed(w)]  # noqa: E731
    assert crewed() == names[:3]  # the cap: the nearest three
    # a model at the fourth's captain's station: she is held over the cap, and nobody sleeps
    for k, held in ((3, names[:4]), (4, names[:5])):
        _, crew = K.station_world(w, names[k])
        _seat(crew)
        assert K.model_held(ships[k])
        w.run(60)
        assert crewed() == held, k
    # the allowance spent: a third held hull takes the farthest unheld one's place, as a
    # stationed hull does under the cap
    _, crew = K.station_world(w, names[5])
    _seat(crew)
    w.run(60)
    assert crewed() == [names[0], names[1], names[3], names[4], names[5]]
    assert ships[2].crew.shape == "far"
    # a harness through no door (a test's) is stationed, not held: the cap's old order
    assert not K.model_held(ships[2])


def wolf(door="runner"):
    """A brig twenty-nine miles from the frigate, asleep, steered north for the Wolf two
    and a half miles off with a fake at her captain's station through `door`."""
    w = hove_to_world()
    for words in (
        'ship: a merchant brig "Ruth" of Britain at 49 54.5 N 5 48.5 W, bound for Falmouth',
        'ship "Ruth": intent bound for Falmouth',
    ):
        e = w.world_order(words)
        assert e.data.get("result") == "done", e.text
    w.run(61)
    v = w.vessels.find("Ruth")
    _, crew = K.station_world(w, "Ruth")
    seen: list[str] = []
    _seat(crew, door, seen)
    with w.as_hull(crew):
        e = crew.submit("steer north", actor="the captain")
    assert e.kind == "helm.set" and crew.shape == "far", e.text
    return w, v, crew, seen


def _danger(crew):
    return [e for e in crew.log if e.kind == "plan.danger"]


def test_a_far_held_hull_standing_for_a_rock_is_put_about_and_her_captain_called():
    w, v, crew, seen = wolf()
    for _ in range(40):
        w.run(60)
        if _danger(crew):
            break
    line = _danger(crew)
    assert len(line) == 1 and line[0].severity.value == "urgent"
    assert "The Wolf ahead by the chart" in line[0].text and "went about" in line[0].text
    assert v.plan[0][0] == "to" and "other tack" in str(v.plan[0][2])
    assert crew.shape == "far"  # asleep still, the plan's order
    w.run(600)
    assert 170.0 <= v.heading_deg <= 190.0  # her head S, off the rock
    assert any("plan puts her about" in s for s in seen)  # her captain's sample has it
    assert len(_danger(crew)) == 1


def test_a_far_hull_held_through_no_door_keeps_the_far_plan_as_it_was():
    w, v, crew, seen = wolf(door="")
    assert not K.model_held(v)
    w.run(40 * 60)
    assert not _danger(crew)
