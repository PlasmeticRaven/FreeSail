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


@pytest.mark.parametrize(
    ("nation", "navy"),
    [
        ("france", "a ship of the French navy"),
        ("spain", "a ship of the Spanish navy"),
        ("united-states", "a ship of the American navy"),
        ("batavian-republic", "a ship of the Dutch navy"),
        ("britain", "a King's ship of Britain"),
    ],
)
def test_a_navy_is_named_by_its_nations_adjective(tmp_path, nation, navy):
    """A King's ship of another nation reads her navy by its nation's adjective (package 75, B2b,
    the lead's ruling of 2026-11-07, words only): the naval cruise's frigate under each colours,
    a King's ship by her wardroom with no intent. Old, by the nation's name: "a ship of the France
    navy", "the Spain navy", "the the United States navy", "the the Batavian Republic navy";
    Britain's "a King's ship of Britain" as before."""
    import copy

    from freesail.world.scenarios import (
        load_scenario,
        make_scenario_world,
        read_scenario_text,
        write_scenario,
    )

    _text, fields = read_scenario_text(ROOT / "data" / "scenarios" / "naval-cruise.yaml")
    fields = copy.deepcopy(fields)
    fields["nation"] = nation
    w = make_scenario_world(load_scenario(write_scenario(fields, tmp_path / "s.yaml")), seed=7)
    assert R.ship_words(w).split(". Her guns")[0].endswith(f"ship-rigged; {navy}")


def test_a_far_hull_is_told_as_herself_not_as_her_files_ship():
    """A crewed far merchant brig is told by her own name, not her file's ship's. Since package
    75 (SW-4, Build-Ships.md §8.4) she sails the merchant brig's own file, her class, guns, people
    and master that file's, where she sailed the brig-sloop's (old: "a brig-sloop of the Diligence
    class; a merchantman of France", the Harpy's file's, commanded by "Captain Pope")."""
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
        "The ship: Nancy, a merchant brig; a merchantman of France. Her guns: 4 long 6-pounders. "
        "Her people: 16 souls by the muster. Commanding: Mr Bradley, merchant; "
    )
    assert "Industry" not in words and "Harpy" not in words and "Captain Pope" not in words


def test_every_committed_ships_class_words_read_as_her_class():
    """Carried fault 24 (found by the Diana's builder; the lead's nudge 84). The razee, the 64 and
    the 74 read "hMS as razeed, 1795", "hMS as built, a 64-gun ship of the Ardent class" and "hMS
    a 74-gun ship of the Arrogant class": her name taken out of her era note's first clause left
    the "HMS" that goes with it, whatever leading capital was made small, and a clause naming her
    state and no class was said as her class. The smack read "a Navy's smack", the "The" of her
    note made "a" before a possessive. Every committed ship's class words now open with an
    article or "H.M.", hold no word made small at its head, no article before a possessive and no
    doubled one; the four by their words (`readings.ship_class_words`)."""
    import re

    from freesail.api.readings import ship_class_words
    from freesail.ship.loader import load_spec

    said = {}
    for path in sorted((ROOT / "data" / "ships").glob("*.yaml")):
        spec = load_spec(path)
        if getattr(spec, "oars", None) is not None:
            continue  # a boat is told by her own words (`readings._boat_words`)
        words = said[path.stem] = ship_class_words(spec, spec.name)
        assert re.match(r"(a|an|the) |H\.M\. ", words), (path.name, words)
        assert not re.search(r"\b[a-z]+[A-Z]", words), (path.name, words)
        assert not re.search(r"\b(a|an) \S+'s\b", words), (path.name, words)
        assert not re.search(r"\b(a|an|the)\s+(a|an|the)\b", words, re.IGNORECASE), words
    assert len(said) == 14
    assert {k: said[k] for k in ("razee-44", "sixty-four", "seventy-four", "smack")} == {
        "razee-44": "an Ardent-class 64 of 1784 cut down to a frigate by the Navy Office's "
        "draught of September 1794, ship-rigged",
        "sixty-four": "a 64-gun ship of the Ardent class",
        "seventy-four": "a 74-gun ship of the Arrogant class",
        "smack": "the Navy's smack",
    }


def test_a_class_opening_with_a_name_of_its_own_keeps_its_capital_and_takes_an_article():
    """Carried fault 24, at its cause for any file: the class's first word was made small whatever
    it was ("hMS"). Now only a leading article is; a class that opens with a word of its own keeps
    it and is given its article ("spanish xebec ..." before)."""
    from types import SimpleNamespace

    from freesail.api.readings import ship_class_words

    spec = SimpleNamespace(
        era_notes="Spanish xebec Murciano of the Mahón station (her lines after Chapelle): ...",
        name="Murciano",
        rig="xebec",
    )
    assert ship_class_words(spec, spec.name) == "a Spanish xebec of the Mahón station"


def test_the_navys_smack_under_a_merchants_papers_is_a_smack():
    """Carried fault 24: the smack out of Falmouth, a merchantman, read "Culloden, a Navy's smack;
    a merchantman of Britain", and with her class mended would read "the Navy's smack; a
    merchantman". Her file's "the Navy's" goes, as its "H.M." does, where she is not a King's
    ship (`readings.ship_words`)."""
    w = _world("smack-falmouth.yaml")
    assert R.ship_words(w).startswith(
        "The ship: Culloden, a smack; a merchantman of Britain. She carries no guns."
    )


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
    # the situation, the first data turn after the brief (package 117), opens with the
    # ship after its own head line
    situation = brief.situation.removeprefix(agent.SITUATION_HEAD).lstrip()
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
    situation = h.brief.situation.removeprefix(agent.SITUATION_HEAD).lstrip()
    assert situation.startswith(words)
    assert h.turns[0].role == OPERATOR and words not in str(h.turns[0].content)
    assert words in h.turns[1].content["situation"]  # the first data turn (package 117)
    # the handover fold keeps the latest brief whole, the ship's words with it
    for _ in range(harness_mod.HANDOVER_KEEP_TURNS + 4):
        w.run(60)
    before = len(h.turns)
    h._fold_handover("the watch so far: nothing to tell")
    assert len(h.turns) < before
    assert h.turns[0].role == OPERATOR and words in h.turns[1].content["situation"]
