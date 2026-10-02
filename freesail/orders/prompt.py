"""A reading asked at the prompt (package 33c; playtest 12, the gate report's item 2).

    the reckoning                     the registry's words for it, as a query line
    what is the reckoning's uncertainty
    ask the master the reckoning
    the bearing of the Lizard         a mark in sight, by any of its words
    the fore topsail                  a sail's state by its name; a part's strain
    sightings                         a reading's words without their article

A reading is a row of the readings registry (`freesail.api.readings`): what the
instruments show, a standing order tests and a model's `readings` tool gives. Typed at
the prompt, alone or after one of the vocabulary's asking words (`reading_words` in
`data/vocabulary.yaml`), it is answered in the log as a query line, kind `query.reading`,
routine and never journaled, as `the booms` and `the sail room` are. Parity is
structural: the answer is `ReadingsView.words`, the registry's words read from the same
view the World hands the standing orders, the snapshot and an agent, and nothing more;
an absent reading answers with the registry's absent sentence. The console and the
browser reach it by one path, `World.submit`.

The vocabulary makes a query verb of every registry phrase (`vocabulary._reading_verbs`),
so the parser and the completer know them as they know `the booms`; a sail or a part by
its name, and a reading's words without their article, are read here when the parser
finds no verb in the words (`answer_unparsed`).
"""

from __future__ import annotations

from typing import Any

from freesail.api import readings as R
from freesail.orders import resolve
from freesail.orders.errors import OrderError
from freesail.orders.grammar import Order
from freesail.orders.vocabulary import Vocabulary, load_vocabulary, normalise
from freesail.ship.graph import Ship

__all__ = ["KIND", "absent_named", "answer", "answer_unparsed", "world_of"]

# The log kind of a reading's answer: a query, which the World logs and does not journal.
KIND = "query.reading"

NO_WORLD_WORDS = "There are no readings to be had: the ship is not in a world."

Result = tuple[str, str, dict[str, Any]]


def world_of(ship: Any) -> Any:
    """The World a ship sails in, through the standing orders' runtime the World attaches
    to every ship it makes (`ship.extra["standing"]`); None for a ship alone."""
    runtime = (getattr(ship, "extra", None) or {}).get("standing")
    return getattr(runtime, "world", None)


def _view(ship: Any) -> tuple[Any, R.ReadingsView]:
    world = world_of(ship)
    if world is None:
        raise OrderError(NO_WORLD_WORDS)
    return world, world.readings


def _sentence(head: str, words: str) -> str:
    text = f"{head[:1].upper()}{head[1:]}: {words}"
    return text if text.endswith((".", "!", "?")) else text + "."


def answer(ship: Ship, order: Order, raw: str = "", vocab: Vocabulary | None = None) -> Result:
    """The answer to a reading's query verb (`vocab.readings`), in the registry's words."""
    vocab = vocab or load_vocabulary()
    phrase = vocab.readings[order.verb]
    if "<" in phrase:
        if phrase.startswith("the bearing of"):
            return _bearing_of(ship, phrase, order.object or "", raw)
        return _with_words(ship, phrase, order.object or "", raw)
    return _phrase(ship, phrase)


def _with_words(ship: Any, phrase: str, said: str, raw: str) -> Result:
    """A parametric reading other than the bearing (package 35: `where is <person>`): the
    row read with the words after the phrase's head, in the registry's words."""
    row = next(r for r in R.REGISTRY.by_words(phrase))
    head = phrase.split(" <")[0]
    words = _said_after(raw, head) or said
    if not words.strip():
        raise OrderError(
            f"{head[:1].upper()}{head[1:]} whom? Name a person by his role or his name."
        )
    world, view = _view(ship)
    value = view.value(row.id, words)
    if value is None:
        raise OrderError(f"Nobody aboard answers to '{words}'; 'the people' lists them.")
    return (
        KIND,
        _sentence(f"{head} {words}", R.reading_words(row, value, world)),
        {
            "reading": [row.id],
            "words": words,
        },
    )


def _phrase(ship: Any, phrase: str) -> Result:
    rows = R.REGISTRY.by_words(phrase)
    present = [r for r in rows if not r.is_absent]
    if not present:
        sentence = rows[0].absent or f"The ship has no reading '{phrase}' yet."
        lowered = sentence[:1].lower() + sentence[1:]
        return KIND, _sentence(phrase, lowered), {"reading": [r.id for r in rows], "absent": True}
    _, view = _view(ship)
    said: list[str] = []
    for row in present:
        w = view.words(row.id)
        if w not in said:
            said.append(w)
    return KIND, _sentence(phrase, ", ".join(said)), {"reading": [r.id for r in present]}


def _bearing_of(ship: Any, phrase: str, mark: str, raw: str) -> Result:
    """`the bearing of <mark>`: the registry's row read with the mark in sight that the
    words name (`navigation.mark_in_sight`: any of its words when one mark answers)."""
    from freesail.orders.navigation import mark_in_sight

    row = next(r for r in R.REGISTRY.by_words(phrase))
    said = _said_after(raw, "bearing of") or mark
    if not said.strip():
        raise OrderError("The bearing of what? Name a mark in sight, or say the land or the light.")
    world, view = _view(ship)
    nav = getattr(world, "navigation", None)
    name = said
    if nav is not None and getattr(world, "lookout", None) is not None:
        found = mark_in_sight(nav, said, refuse=False)
        if found is not None:
            name = found
    value = view.value(row.id, name)
    words = R.reading_words(row, value, world)
    return KIND, _sentence(f"the bearing of {name}", words), {"reading": [row.id], "mark": name}


def _said_after(raw: str, words: str) -> str:
    """The words of `raw` after `words`, as typed (a mark's name keeps its capitals)."""
    low = " ".join(raw.lower().split())
    i = low.find(words)
    return " ".join(raw.split())[i + len(words) :].strip(" ?.!") if i >= 0 else ""


# ---------------------------------------------------------------------------
# What the parser found no verb in
# ---------------------------------------------------------------------------


def _without_asking(words: list[str], vocab: Vocabulary) -> list[str]:
    """The words with an asking word taken off their head ('what is', 'ask the master')."""
    for a in sorted((a.split() for a in vocab.asking), key=len, reverse=True):
        if words[: len(a)] == a and len(words) > len(a):
            return words[len(a) :]
    return words


def answer_unparsed(ship: Ship, text: str, vocab: Vocabulary | None = None) -> Result | None:
    """For words the parser found no order in: the answer when they ask for a reading
    without its article ('sightings', 'reckoning') or name a sail or a part of this ship
    ('the fore topsail', 'what is the main topmast'); refused in the registry's absent
    sentence when they name a reading the ship has not got ('sound the well'); else None,
    and the parser's refusal stands."""
    vocab = vocab or load_vocabulary()
    words = [w.replace("'", "") for w in normalise(text).split() if w != ","]
    if not words:
        return None
    asked = _without_asking(words, vocab)
    if asked[:1] != ["the"]:
        verb = vocab.phrase_to_verb.get(" ".join(["the", *asked]))
        if verb in vocab.readings and "<" not in vocab.readings[verb]:
            return _phrase(ship, vocab.readings[verb])
    sentence = absent_named(text)
    if sentence is not None:
        raise OrderError(sentence)
    if hasattr(ship, "parts") and world_of(ship) is not None:
        return _part(ship, asked, vocab)
    return None


def absent_named(text: str) -> str | None:
    """The registry's sentence for an absent reading the words name ('sound the well':
    the ship has no well to sound yet), or None."""
    norm = f" {normalise(text)} "
    for row in R.REGISTRY:
        if row.is_absent and any(f" {w} " in norm for w in row.words):
            return row.absent
    return None


def _part(ship: Ship, words: list[str], vocab: Vocabulary) -> Result | None:
    """A sail by name, or a group of them: each sail's state in the registry's words (the
    `readings` tool's `sails`); any other part: its strain, the registry's `the <part>`."""
    from freesail.orders import grammar

    try:
        phrase, side, rest = grammar._match_object(ship, words, vocab, "set", vocab.verbs["set"])
    except OrderError:
        return None
    if phrase is None or rest:
        return None
    try:
        res = resolve.resolve(ship, phrase, side, "the reading")
    except OrderError:
        noun = resolve.noun_table(ship).lookup(phrase)
        if noun is None:
            return None
        ids = list(noun.ids)
        name = phrase
    else:
        ids = list(res.ids)
        name = res.name if len(ids) > 1 else resolve.display_name(ship, ids[0])
    world, view = _view(ship)
    sails = getattr(ship, "sails", {})
    if all(i in sails for i in ids):
        row = R.REGISTRY.get("sail")
        each = [(i, R.describe_value(row, view.value("sail", i))) for i in ids]
        reading = ["sail"]
    else:
        row = R.REGISTRY.get("strain")
        each = [(i, view.words("strain", i)) for i in ids]
        reading = ["strain"]
    if len(each) == 1:
        text = _sentence(f"the {resolve.display_name(ship, each[0][0])}", each[0][1])
    else:
        listed = "; ".join(f"the {resolve.display_name(ship, i)} {w}" for i, w in each)
        text = _sentence(f"the {name}", listed)
    return KIND, text, {"reading": reading, "parts": ids}
