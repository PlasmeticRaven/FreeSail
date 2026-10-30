"""The ship herself, said plainly (the owner's word of 2026-10-27: models at a station
were almost never told what ship they were on, and reasoned it out).

Every station's brief opens its situation with the ship: her name, her rig and class, her
service and nation, her fit of guns, her people's number, who commands, and the ports of
her voyage; a reading `the ship` (`what ship`, `my ship`, `this ship`) answers the same at
any time, from her file, her papers and her muster. A brief kept whole across a fold keeps
the words; a station on another hull is told that hull.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from freesail.agents import agent, director, tools
from freesail.agents.agent import Brief
from freesail.api import readings as R

ROOT = Path(__file__).resolve().parents[1]


def _world(name: str):
    from freesail.world.scenarios import load_scenario, make_scenario_world

    return make_scenario_world(load_scenario(ROOT / "data" / "scenarios" / name), seed=7)


def test_the_ship_reading_says_her_name_class_service_nation_guns_people_and_commander():
    w = _world("naval-cruise.yaml")
    words = R.ship_words(w)
    assert words.startswith(
        "The ship: Amazon, a 36-gun 18-pounder frigate of the Amazon class, ship-rigged; a "
        "King's ship of Britain. Her guns: 26 long 18-pounders, 10 32-pounder carronades, 4 "
        "long 9-pounders. Her people: 264 souls by the muster. Commanding: Captain Bowen, "
    )
    assert words.endswith("The ports of her voyage: Falmouth, Plymouth and Brest.")
    for ask in ("the ship", "what ship", "my ship", "this ship", "what ship is this"):
        said = w.submit(ask)
        assert said.kind == "query.reading" and words in said.text, ask
    assert R.REGISTRY.get("ship").kind == "query"
    # a hired cutter in trade: the hull's lines a King's cutter's, she a merchantman
    c = _world("dispatches-falmouth.yaml")
    cw = R.ship_words(c)
    assert cw.startswith(
        "The ship: Sherbourne, an armed cutter; a merchantman of Britain. Her guns: "
    )
    assert "Her people: 30 souls by the muster." in cw and "Commanding: Mr Bowen, merchant" in cw
    # the convoy's escort
    e = R.ship_words(_world("convoy-six.yaml"))
    assert e.startswith(
        "The ship: Harpy, H.M. brig-sloop of the Diligence class; a King's ship of Britain, "
        "the convoy's escort."
    )


def test_a_far_hull_is_told_as_herself_not_as_her_files_ship():
    from tests.test_brains import put
    from tests.test_crews import hove_to_world

    w = hove_to_world()
    v = put(
        w,
        "merchant brig",
        "france",
        "49 30.2 N 5 30 W",
        "bound for Brest",
        intent="bound for Brest",
        name="Nancy",
    )
    w.run(61)
    words = R.ship_words(v.crew)
    assert words.startswith(
        "The ship: Nancy, a brig-sloop of the Diligence class; a merchantman of France. "
    )
    assert "Harpy" not in words and "Captain Pope" in words


STATIONS = ("watcher", "officer", "captain", "master", "lookout", "passenger")


@pytest.mark.parametrize("which", STATIONS)
def test_every_stations_brief_opens_its_situation_with_the_ship(which: str):
    w = _world("naval-cruise.yaml")
    station = getattr(agent, which)(world=w)
    brief = Brief.build(
        station,
        "a play session",
        ["(the log is empty)"],
        {"the wind": "N, 15 knots"},
        tools.tool_names(),
        voyage=agent.voyage_words(w) if which == "captain" else "",
        ship=R.ship_words(w),
    )
    situation = next(i.text for i in brief.head if i.name == "situation")
    assert situation.startswith("The ship: Amazon, a 36-gun 18-pounder frigate of the Amazon class")
    assert "Commanding: Captain Bowen" in situation
    # the director, above the game, is told no ship of its own
    d = Brief.build(
        director.director(world=w),
        "a play session",
        ["(the log is empty)"],
        {},
        tools.tool_names(director=True),
    )
    assert "The ship: Amazon" not in d.text()


def test_the_harness_gives_the_ship_at_the_seating_and_keeps_it_across_a_fold():
    from freesail.agents import harness as harness_mod
    from freesail.agents.model import OPERATOR
    from tests.test_agents import call, reply, stationed

    w = _world("naval-cruise.yaml")
    script = [reply("", call("readings")) for _ in range(harness_mod.HANDOVER_KEEP_TURNS + 6)]
    h, fake, _ = stationed(w, script, st=agent.officer(world=w))
    words = "The ship: Amazon, a 36-gun 18-pounder frigate of the Amazon class"
    situation = next(i.text for i in h.brief.head if i.name == "situation")
    assert situation.startswith(words)
    assert h.turns[0].role == OPERATOR and words in str(h.turns[0].content)
    # the handover fold keeps the latest brief whole, the ship's words with it
    for _ in range(harness_mod.HANDOVER_KEEP_TURNS + 4):
        w.run(60)
    before = len(h.turns)
    h._fold_handover("the watch so far: nothing to tell")
    assert len(h.turns) < before
    assert h.turns[0].role == OPERATOR and words in str(h.turns[0].content)
