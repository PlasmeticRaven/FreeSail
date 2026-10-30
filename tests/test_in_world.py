"""The primer and the library are in-world documents, for whoever reads them.

The rule (the orders-and-library review's first item): the primer (`docs/primer/`) and the
library's topics as the game serves them (the catalogue, the grammar, the world page, the
tools' words, the ship's papers), with the stations' briefs and the brief head a model is
given, are read by a human or a model at any station, in any scenario, on any ship.
Nothing in them may be true only for one scenario, one signal book, one ship, one voyage
or one stage of the build: no reference to a milestone, a package, a gate, a builder, the
owner's rulings, the lead, a playtest, a review, a vendor's or a model's name, or the
development at all. What was cut and is still worth keeping is in
`docs/dev/PrimerRedactions.md`.

This test is the rule enforced: every source below is scanned for the forbidden words and
patterns, and fails naming the line when one returns. The allow-list is for the few words
that are in-world too, each with its reason:

- "the owner" is the owner of the game at the door, a party the consent brief names (his
  grant, his key, his sentences, his word reaching a station as the owner's); what is
  forbidden is the project's owner ruling, noting, judging or playing, which the patterns
  below catch by their verbs and nouns.
- "the lead" is the sounding lead; the project's lead is caught by his possessives and verbs.
- "seed 7" is the game's own seed, which chapter 6 explains and chapter 18's lessons name.
- "MCP" names a door of the harness (the bridge), not a vendor.
- the shipped scenarios' file names, which a reader needs to load them, even where a
  file's name carries a word from the build (`gate-4c-day.yaml`).
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
PRIMER = ROOT / "docs" / "primer"

# Each a regular expression and the reason it is forbidden.
FORBIDDEN: tuple[tuple[str, str], ...] = (
    (r"\bmilestones?\b", "a milestone is a stage of the build"),
    (r"\bpackages?\s+\d", "a package is a stage of the build"),
    (r"\bpackages?\b(?! of)", "a package is a stage of the build"),
    (r"\bgates?\b", "a gate is the build's"),
    (r"\bgate's\b", "a gate is the build's"),
    (r"\bbuilders?\b", "the builder is the build's"),
    (r"\bplaytests?\b", "a playtest is the build's"),
    (
        r"\bthe lead's (?:own|notes?|playtests?|first|judgement|words?|answers?|seat|"
        r"reading|routing|sweeps|reviews?|sessions?|branch|hand|use|smoke|runs?|rulings?|"
        r"machine|watch|head|test)\b",
        "the project's lead",
    ),
    (
        r"\bthe lead (?:ran|played|tried|gave|found|sat|adds|merges?|reviews|"
        r"runs|routed|routing|answers?|notes?|playtest|tests?|own|first|machine|judgement|"
        r"words?|cannot|measured|mended|accepts|accepted|took|put|has|had|lost|reproduces?|"
        r"sits|and the owner|or the owner)\b",
        "the project's lead",
    ),
    (
        r"\b(?:report(?:ed|s)?|named|booked|left|carried|open|questions?|routed|noted|"
        r"findings?|filed) (?:to|for) the lead\b",
        "the project's lead",
    ),
    (
        r"\bthe owner's (?:rulings?|notes?|word of|words of|first|playtests?|findings?|"
        r"questions?|proposals?|reviews?|ask|caution|principles|interview|local|machine|"
        r"models|testing|debrief|reading|refinement|rule of|seam|scenario|tests?|tree|copy|"
        r"fix|fixes|baseline|choice|judgement|session|hashes|approved|decision)",
        "the project's owner",
    ),
    (
        r"\bthe owner (?:ran|said|asked|found|judging|judged|approves|approved|corrected|"
        r"put it|wanted|weighing|reached|tried|saw|looked|noticed|reproduce|runs|ruled|"
        r"played|plays|2026)\b",
        "the project's owner",
    ),
    (
        r"\b(?:rulings?|notes?|word|findings?|decisions?|proposals?|questions?|principles) "
        r"of the owner\b",
        "the project's owner",
    ),
    (r"\bthe owner and the lead\b|\bthe lead and the owner\b", "the project's owner"),
    (r"\bthe owner is judging\b", "the project's owner"),
    (r"\bspec\b", "the specification is the build's"),
    (r"§", "a section mark cites the build's documents"),
    (r"\bM\d[a-c]?\b", "a milestone's number"),
    (r"\btruths?\s+\d", "a pinned truth is the build's"),
    (r"\bdecisions?\s+\d", "a numbered decision is the build's"),
    (r"\bruling", "a ruling is the build's"),
    (r"\btuning notes\b|\bTuningNotes\b|\bWorkPackages\b", "the build's notes"),
    (r"docs/dev|docs/design|docs/playtests|docs/gates|\btests/", "the build's folders"),
    (r"\bcold review\b|\bthe review\b", "a review is the build's"),
    (r"\b2026\b", "a date of the build"),
    (r"\bthis build\b|\bthe build\b", "the build"),
    (r"\bplaytest\b", "a playtest is the build's"),
    (
        r"\b(?:Claude|Anthropic|OpenAI|OpenRouter|GPT|Gemini|Gemma|Llama|Qwen|Mistral|"
        r"Opus|Sonnet|Haiku|Fable|Mythos|Ollama|Hermes|DeepSeek|Grok)\b",
        "a vendor's or a model's name: the documents speak of 'a model' and 'the officer'",
    ),
)
_RX = tuple((re.compile(p, re.I), why) for p, why in FORBIDDEN)

# Literal phrases taken out of a line before it is scanned, each in-world (the module's
# words say why).
ALLOWED: tuple[str, ...] = (
    "data/scenarios/gate-4c-day.yaml",
    "data/scenarios/gate-5b-passage.orders",
    "the lead's last cast",
    "the lead's cast",
    "the lead's arming",
    "the lead's last",
    "library(topic='standing orders')",
)


def hits(text: str) -> list[str]:
    out: list[str] = []
    for i, line in enumerate(text.splitlines(), 1):
        probe = line
        for word in ALLOWED:
            probe = probe.replace(word, " ")
        found = [why for rx, why in _RX if rx.search(probe)]
        if found:
            out.append(f"line {i}: {'; '.join(sorted(set(found)))}: {line.strip()[:160]}")
    return out


# ---------------------------------------------------------------------------
# The sources
# ---------------------------------------------------------------------------


def _world(name: str):
    from freesail.world.scenarios import load_scenario, make_scenario_world

    sf = load_scenario(ROOT / "data" / "scenarios" / name)
    return make_scenario_world(sf, seed=7)


@pytest.fixture(scope="module")
def kings_ship():
    """A King's ship with her signal books and the private signals among her papers."""
    return _world("naval-cruise.yaml")


@pytest.fixture(scope="module")
def cutter():
    """A hired cutter: the merchant words, no private signals."""
    return _world("dispatches-falmouth.yaml")


PRIMER_FILES = sorted(p.name for p in PRIMER.glob("*.md"))


@pytest.mark.parametrize("name", PRIMER_FILES)
def test_the_primer_is_in_world(name: str):
    text = (PRIMER / name).read_text(encoding="utf-8")
    found = hits(text)
    assert not found, f"{name} is not in-world:\n" + "\n".join(found)


def _brief_constants() -> dict[str, str]:
    from freesail.agents import agent, director
    from freesail.world import seats

    out: dict[str, str] = {}
    for n in dir(agent):
        v = getattr(agent, n)
        if isinstance(v, str) and (n.endswith("_BRIEF") or n.endswith("_WORDS")):
            out[f"agent.{n}"] = v
    for n in ("DIRECTOR_BRIEF", "SEAT_AND_CHANNEL_BRIEF"):
        out[f"director.{n}"] = getattr(director, n)
    out["director.NO_BRIEF_WORDS"] = "\n".join(director.NO_BRIEF_WORDS)
    out["seats.VOICE_BRIEF"] = seats.VOICE_BRIEF
    return out


@pytest.mark.parametrize("name", sorted(_brief_constants()))
def test_the_station_briefs_are_in_world(name: str):
    found = hits(_brief_constants()[name])
    assert not found, f"{name} is not in-world:\n" + "\n".join(found)


def _tool_words() -> dict[str, str]:
    from freesail.agents.tools import TOOLS

    return {
        f"tool.{t.name}": "\n".join(
            [t.description, t.at_director, *(f"{k}: {v}" for k, v in t.params.items())]
        )
        for t in TOOLS.values()
    }


@pytest.mark.parametrize("name", sorted(_tool_words()))
def test_the_tools_words_are_in_world(name: str):
    found = hits(_tool_words()[name])
    assert not found, f"{name} is not in-world:\n" + "\n".join(found)


TOPICS = (
    "contents",
    "primer",
    "catalogue",
    "grammar",
    "the ship",
    "papers",
    "the world",
    "tools",
    "standing orders",
    "books",
)


@pytest.mark.parametrize("key", TOPICS)
def test_the_library_topics_are_in_world_on_a_kings_ship(kings_ship, key: str):
    from freesail.agents import tools

    page = tools.library(kings_ship, "captain", key, section="all")
    found = hits(str(page))
    assert not found, f"library(topic={key!r}) is not in-world:\n" + "\n".join(found)


@pytest.mark.parametrize("key", ("papers", "the ship", "contents"))
def test_the_library_topics_are_in_world_on_a_cutter(cutter, key: str):
    from freesail.agents import tools

    page = tools.library(cutter, "captain", key, section="all")
    found = hits(str(page))
    assert not found, f"library(topic={key!r}) on the cutter is not in-world:\n" + "\n".join(found)


def test_every_primer_chapter_is_served_and_listed(kings_ship):
    """Every chapter the library serves is a file of the primer, and every chapter file
    is served: the book and the library are one."""
    from freesail.agents import tools

    served = {n for n, _ in tools._primer_chapters()}
    files = {p.stem.split("-", 1)[0].lstrip("0") or "0" for p in PRIMER.glob("[0-9]*-*.md")}
    assert served == files
    contents = str(tools.library(kings_ship, "captain", "primer"))
    for n in sorted(served, key=int):
        assert f"primer {n}:" in contents


STATIONS = ("watcher", "officer", "captain", "master", "lookout", "passenger", "director")


@pytest.mark.parametrize("which", STATIONS)
def test_the_brief_head_is_in_world(kings_ship, which: str):
    """The head the harness builds for a station (the disclosure, the token, the
    documentation, the authority with the person's outline, the situation with the
    voyage's words) carries nothing of the build."""
    from freesail.agents import agent, director, tools
    from freesail.agents.agent import Brief

    if which == "director":
        station = director.director(world=kings_ship)
        names = tools.tool_names(director=True)
        voyage = ""
    else:
        station = getattr(agent, which)(world=kings_ship)
        names = tools.tool_names()
        voyage = agent.voyage_words(kings_ship)
    brief = Brief.build(
        station,
        "a play session",
        ["(the log is empty)"],
        {"the wind": "N, 15 knots"},
        names,
        voyage=voyage,
    )
    found = hits(brief.text())
    assert not found, f"the {which}'s brief is not in-world:\n" + "\n".join(found)


def test_the_starter_briefs_are_in_world():
    """The director's starter briefs as the station brief carries them."""
    from freesail.agents import director

    for name in director.starter_briefs():
        brief = director.resolve_brief(name, "a starter")
        found = hits(brief.body())
        assert not found, f"the starter brief {name!r} is not in-world:\n" + "\n".join(found)


def test_the_rule_has_teeth():
    assert hits("Since package 57 the royals are set flying.")
    assert hits("The owner's ruling of 2026-10-09.")
    assert hits("a model through the API door of a named vendor, Claude")
    assert not hits("The owner is always at the door; his words reach you as the owner's.")
    assert not hits("heave the lead; the lead and the log; a cast of the lead")
    assert not hits("The logs are from seed 7 with a north wind of 15 knots.")
