"""The grammar in one place, checked against the vocabulary: no order the game takes is
missing from the book, and no form the book gives is refused.

The book is two things that read as one: the library's grammar topic, generated from the
vocabulary, the readings registry, the director's forms and the stand-by's words, and so
complete by construction, which these tests guard; and the primer, written by hand, whose
chapters must name every verb of the vocabulary and every reading of the registry somewhere
(a forms table, a worked example, a sentence), which these tests measure. The forms the
primer's tables give are run through the ship by `test_primer.py`; this file is the other
direction.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from freesail.agents import tools
from freesail.agents.director import WORLD_ORDER_FORMS
from freesail.agents.tripwires import TRIPWIRE_WORDS
from freesail.api import readings as R
from freesail.orders.vocabulary import load_vocabulary

ROOT = Path(__file__).resolve().parents[1]
PRIMER = ROOT / "docs" / "primer"


def _plain(text: str) -> str:
    """Words as the vocabulary keys them: one case, no apostrophes or curly quotes, one
    space between words."""
    text = text.replace("’", "'").replace("‘", "'").replace("'", "").lower()
    return " ".join(re.sub(r"[,:;.!?`]", " ", text).split())


@pytest.fixture(scope="module")
def grammar() -> str:
    from freesail.world.scenarios import load_scenario, make_scenario_world

    world = make_scenario_world(load_scenario(ROOT / "data/scenarios/naval-cruise.yaml"), seed=7)
    return str(tools.library(world, "captain", "grammar", section="all"))


@pytest.fixture(scope="module")
def primer() -> str:
    return _plain("\n".join(p.read_text(encoding="utf-8") for p in PRIMER.glob("*.md")))


# ---------------------------------------------------------------------------
# The library's grammar, complete by construction
# ---------------------------------------------------------------------------


def test_the_grammar_page_names_every_verb_and_synonym_of_the_vocabulary(grammar):
    """Every verb the ship takes, with every synonym, is a line of the order language or
    of the book's orders; the readings' asking forms are the readings part's."""
    vocab = load_vocabulary()
    page = grammar
    for name, spec in vocab.verbs.items():
        if spec.level == "driver" or name in vocab.readings:
            continue
        assert f"  {name}" in page, name
        for syn in spec.synonyms:
            assert syn in page, (name, syn)


def test_the_grammar_page_lists_every_reading_with_what_it_answers(grammar):
    """Every row of the registry is in the readings part by its words with its
    description (every row has one), the aliases the vocabulary adds beside them, and
    the rows the ship has not got named as refused."""
    vocab = load_vocabulary()
    part = grammar[grammar.index("The readings:") : grammar.index("The standing dialect:")]
    for row in R.REGISTRY:
        assert row.description or row.is_absent, row.id
        for w in row.words:
            assert f"'{w}'" in part, (row.id, w)
        if not row.is_absent:
            assert row.description in part, row.id
    for alias, phrase in vocab.reading_aliases.items():
        assert f"'{alias}' is '{phrase}'" in part, alias
    for a in vocab.asking:
        assert f"'{a}'" in part, a


def test_the_grammar_page_has_the_events_the_tripwires_and_the_world_orders(grammar):
    """The standing dialect's triggers name every event; the stand-by part every event,
    interval and tripwire; the world orders every form with its examples."""
    for words in R.EVENTS:
        assert f"'{words}'" in grammar, words
    stand_by = grammar[grammar.index("The stand-by") :]
    for words in TRIPWIRE_WORDS:
        assert f"'{words}'" in stand_by, words
    for words in R.INTERVALS:
        assert f"'{words}'" in stand_by, words
    for f in WORLD_ORDER_FORMS:
        assert f.words in grammar, f.key
        for x in f.examples:
            assert f"e.g. {x}" in grammar, x


def test_the_voice_is_one_part_of_the_grammar(grammar):
    """The deck's conversation and the trumpet in one place: say, say to, tell, ask, the
    lookout's hail, the hail of a sail with the colon optional, and the answer."""
    voice = grammar[grammar.index("The voice:") : grammar.index("The stand-by")]
    for words in (
        "say <words>",
        "say to the <station> <words>",
        "tell the <station> <words>",
        "ask the <station> <question>",
        "hail <words>",
        "hail the <sail> <words>",
        "the colon optional",
        "answer <words>",
    ):
        assert words in voice, words


def test_a_query_reading_is_read_and_never_compared():
    """The readings that are questions in words (the people, the pilot, the port) carry
    the query kind: a condition on one is refused in words that say to ask it, and the
    ground the lead brings up is still compared by its words."""
    from freesail import orders
    from freesail.orders.errors import OrderError
    from tests.test_primer import make_ship

    ship = make_ship("frigate", "plain-sail", "starboard")
    queries = [row for row in R.REGISTRY if row.kind == "query"]
    assert {r.id for r in queries} >= {"people", "pilot", "port", "prices", "captain"}
    assert R.REGISTRY.get("ground").kind == "ground"
    with pytest.raises(OrderError, match="read, not compared in a standing order"):
        orders.handle(ship, 'standing order "p": when the pilot is aboard then heave to')
    kind, _, _ = orders.handle(ship, 'standing order "g": when the ground is sand then heave to')
    assert kind == "standing.given"


# ---------------------------------------------------------------------------
# The primer, measured against the vocabulary
# ---------------------------------------------------------------------------


def _named(primer: str, words: str) -> bool:
    return _plain(words) in primer


def test_every_verb_of_the_vocabulary_is_named_in_the_primer(primer):
    """Every verb the ship takes (the driver's commands aside) is named in some chapter,
    by its name or by a synonym."""
    vocab = load_vocabulary()
    missing = []
    for name, spec in vocab.verbs.items():
        if spec.level == "driver" or name in vocab.readings:
            continue
        if not any(_named(primer, w) for w in (name, *spec.synonyms)):
            missing.append(name)
    assert not missing, f"verbs the primer never names: {missing}"


def test_every_reading_of_the_registry_is_named_in_the_primer(primer):
    """Every reading is named in some chapter by one of its words (a parametric row by
    its words before the parameter)."""
    missing = []
    for row in R.REGISTRY:
        words = [w.split(" <")[0] for w in row.words]
        if not any(_named(primer, w) for w in words):
            missing.append(row.id)
    assert not missing, f"readings the primer never names: {missing}"


def test_every_world_order_form_is_named_in_the_primer(primer):
    """Every world order form's channel word is in the director's chapter."""
    for f in WORLD_ORDER_FORMS:
        head = f.words.split(":")[0].split(" ")[0]
        assert _named(primer, head), f.key


def test_the_primer_names_every_event_and_every_tripwire(primer):
    """The standing dialect's events and the stand-by's tripwires are each named, so a
    reader can find what wakes a station without the library."""
    # an absent event (the world has not got it yet; the book refuses it with its
    # sentence) is the grammar page's "later" list's, as an absent reading is, and
    # not the primer's, which names what wakes a station
    missing = [w for w, s in R.EVENTS.items() if not s.absent and not _named(primer, w)]
    assert not missing, f"events the primer never names: {missing}"
    missing = [w for w in TRIPWIRE_WORDS if not _named(primer, w.split(" <n>")[0])]
    assert not missing, f"tripwires the primer never names: {missing}"
