"""Belaying work (package 29c, playtest 8): the captain's word to stop work in hand or
waiting, which is gone and not paused.

    belay <the work>        the work as the log names it, or the order that gave it, or
                            its kind, or its subject: "belay reefing the mainsail", "belay
                            reef the mainsail", "belay the reef", "belay the mainsail"
                            (every job on that sail); `cancel ...`, `avast ...` the same
    belay that              the last order given whose work is still in hand or waiting;
                            a bare "belay" or "avast", "cancel that" the same
    belay all work          everything in hand or waiting, the ship left as she is;
                            "belay all", "cancel all orders" and the rest the same

`belay` is also the line verb ("belay the main sheet"), and the grammar asks `reading`
which it is: a bare `belay` is `belay that`; words that name a line of the ship are the
line verb, as they always were; words that read as work (a verb or a gerund of one, a
kind of work, a part that is not a line) are `belay <the work>`; anything else is left to
the line verb, whose refusal names the nearest lines. `belay that` and `belay all work`
are verb phrases of their own in `data/vocabulary.yaml`, with their synonyms.

The runner does the belaying (`Runner.belay`): the hands are released, the evolution is
removed, and each piece of work is left as its last finished step left it; this module
finds the work the words name and writes the one line that says what was belayed and
how it was left. The manoeuvres' belay (decision 25: "Belayed setting the royals: all
hands about ship") is another thing, in the runner, and keeps its line.
"""

from __future__ import annotations

from typing import Any

from freesail.evolutions.runner import Instance, gerund, part_name
from freesail.orders import errors, grammar, resolve
from freesail.orders.errors import OrderError
from freesail.orders.vocabulary import Vocabulary, load_vocabulary, normalise, strip_article
from freesail.ship.graph import Ship
from freesail.ship.parts import Line, Sail

__all__ = ["ALL_WORK", "THAT", "WORK", "WORK_VERBS", "execute", "reading"]

# The canonical verbs, as `data/vocabulary.yaml` names them.
WORK = "belay the work"
THAT = "belay that"
ALL_WORK = "belay all work"
WORK_VERBS = (WORK, THAT, ALL_WORK)

# The line verb's phrases that are also the bare word to stop: said alone they are
# `belay that`, and said of work they belay it ("avast reefing the mainsail").
STOP_WORDS = ("belay", "avast")

# Words that join a kind of work to its subject: "the reef in the mainsail".
_JOINING = ("in", "on", "of", "at", "to", "for")

Result = tuple[str, str, dict[str, Any]]


# ---------------------------------------------------------------------------
# Which verb a bare 'belay' is
# ---------------------------------------------------------------------------


def reading(ship: Ship, words: list[str], vocab: Vocabulary | None = None) -> str:
    """For the line verb said as `belay` or `avast` with `words` after it: the verb the
    order is. `THAT` when nothing follows; "belay" (the line verb) when the words name a
    line of this ship, or read as nothing at all (its refusal names the nearest lines);
    `WORK` when they read as work."""
    vocab = vocab or load_vocabulary()
    words = [w for w in words if w != ","]
    if not words:
        return THAT
    if _names_a_line(ship, words, vocab):
        return "belay"
    if _reads_as_work(ship, words, vocab):
        return WORK
    return "belay"


def _names_a_line(ship: Ship, words: list[str], vocab: Vocabulary) -> bool:
    try:
        phrase, _side, _rest = grammar._match_object(
            ship, words, vocab, "belay", vocab.verbs["belay"]
        )
    except OrderError:
        return False
    if phrase is None:
        return False
    noun = resolve.noun_table(ship).lookup(phrase)
    ids = list(noun.ids) if noun is not None else []
    return bool(ids) and all(isinstance(ship.parts.get(i), Line) for i in ids)


def _reads_as_work(ship: Ship, words: list[str], vocab: Vocabulary) -> bool:
    ws = strip_article(words)
    if not ws:
        return False
    if ws[0] in vocab.work_nouns or _gerund_phrase(ws, vocab) is not None:
        return True
    try:
        grammar._match_verb(ws, vocab)
        return True
    except OrderError:
        pass
    return _part_ids(ship, ws, vocab) is not None


# ---------------------------------------------------------------------------
# Carrying it out
# ---------------------------------------------------------------------------


def execute(ship: Ship, order: grammar.Order, vocab: Vocabulary | None = None) -> Result:
    """Belay the work the order names. Raises OrderError, with the work in hand listed,
    when there is none to belay or the words name none of it."""
    from freesail.orders.verbs import runner_of

    vocab = vocab or load_vocabulary()
    runner = runner_of(ship)
    work = runner.work()
    if not work:
        raise OrderError("There is no work in hand or waiting to belay.")
    if order.verb == ALL_WORK:
        chosen, said = work, "all work"
    elif order.verb == THAT:
        chosen, said = runner.last_order_work(), "that"
    else:
        text = order.object or ""
        if not text.strip():
            raise OrderError(
                "Belay which work? Name it as the log does ('belay reefing the mainsail'), "
                "by its kind or its sail ('belay the reef', 'belay the mainsail'), or say "
                f"'belay that' or 'belay all work'. {_listing(runner, work)}"
            )
        chosen, said = _named(ship, runner, work, text, vocab)
    belayed = runner.belay(ship, chosen)
    text = _line(order.verb, belayed)
    data = {
        "verb": order.verb,
        "level": 1,
        "said": said,
        "belayed": belayed,
        "subjects": [b["subject"] for b in belayed],
    }
    return "work.belayed", text, data


def _line(verb: str, belayed: list[dict[str, Any]]) -> str:
    """'Belayed reefing the mainsail; nothing done, it was waiting for hands.', or for
    several, each with how it was left in brackets."""
    if len(belayed) == 1 and verb != ALL_WORK:
        b = belayed[0]
        return f"Belayed {b['doing']}; {b['left']}."
    items = [f"{b['doing']} ({b['left']})" for b in belayed]
    head = "Belayed all work, the ship left as she is: " if verb == ALL_WORK else "Belayed "
    return head + errors.join_names(items, "and", limit=len(items)) + "."


def _listing(runner: Any, work: list[Instance]) -> str:
    """'The work in hand: reefing the mainsail (waiting for hands) and bracing the fore
    yard.'"""
    items = []
    for inst in work:
        how = (
            " (waiting for hands)"
            if inst.waiting_for == "hands"
            else " (waiting its turn)"
            if inst.waiting
            else ""
        )
        items.append(f"{runner.doing(inst)}{how}")
    return "The work in hand: " + errors.join_names(items, "and", limit=len(items)) + "."


# ---------------------------------------------------------------------------
# The work the words name
# ---------------------------------------------------------------------------


def _named(
    ship: Ship, runner: Any, work: list[Instance], text: str, vocab: Vocabulary
) -> tuple[list[Instance], str]:
    """The work in hand or waiting that `text` names, and the words as read. Tried in
    turn, the first reading that understands the words deciding: the work exactly as the
    log names it ('reefing the mainsail'); an order, as it was given or with a gerund at
    its head made its verb again ('reef the mainsail, one reef with the idlers',
    'reefing the mainsail'); a kind of work and its subject ('the reef in the mainsail');
    a part ('the mainsail', every job on it)."""
    norm = " ".join(normalise(text).replace(" , ", " ").split())
    exact = [i for i in work if norm == normalise(runner.doing(i))]
    if exact:
        return exact, norm
    words = strip_article(normalise(text).split())
    readings = [
        lambda: _by_order(ship, work, _as_order_text(words, vocab), vocab),
        lambda: _by_kind(ship, work, words, vocab),
        lambda: _by_part(ship, work, words, vocab),
    ]
    for read in readings:
        got = read()
        if got is None:
            continue
        chosen, what = got
        if chosen:
            return chosen, norm
        raise OrderError(f"Nothing in hand or waiting is {what}. {_listing(runner, work)}")
    raise OrderError(
        f"Nothing in hand or waiting answers to '{norm}': name the work as the log does, "
        f"its kind ('the reef') or its sail. {_listing(runner, work)}"
    )


def _gerund_phrase(words: list[str], vocab: Vocabulary) -> str | None:
    """The verb phrase whose gerund begins the words ('taking in' for 'take in'), or
    None. The longest wins."""
    for phrase in vocab.verb_phrases:  # longest first
        pw = phrase.split()
        if len(pw) > len(words) or not pw:
            continue
        said = [gerund(pw[0]), *pw[1:]]
        if words[: len(said)] == said:
            return phrase
    return None


def _as_order_text(words: list[str], vocab: Vocabulary) -> str:
    """The words as an order: a gerund at their head made its verb again."""
    phrase = _gerund_phrase(words, vocab)
    if phrase is None:
        return " ".join(words)
    return " ".join([*phrase.split(), *words[len(phrase.split()) :]])


def _evolution_ids(verb: str, vocab: Vocabulary) -> set[str]:
    """The evolutions an order's verb starts: 'reef' -> reef_square, reef_gaff."""
    if verb == "trim":
        return {str(vocab.evolutions["brace"])}
    mapping = vocab.evolutions.get(verb)
    if isinstance(mapping, dict):
        return {str(v) for v in mapping.values()}
    if isinstance(mapping, str):
        return {mapping}
    return set()


def _subject_ids(ship: Ship, ids: list[str]) -> set[str]:
    """The parts named, and the yard of every sail among them (a sail's brace)."""
    out = set(ids)
    for pid in ids:
        part = ship.parts.get(pid)
        if isinstance(part, Sail):
            yard = ship.yard_of(part)
            if yard is not None:
                out.add(yard.id)
    return out


def _matching(work: list[Instance], evos: set[str], subjects: set[str] | None) -> list[Instance]:
    return [
        i
        for i in work
        if (not evos or i.evo.id in evos)
        and (
            subjects is None
            or i.subject_id in subjects
            or str(i.params.get("sail") or "") in subjects
        )
    ]


def _by_order(
    ship: Ship, work: list[Instance], text: str, vocab: Vocabulary
) -> tuple[list[Instance], str] | None:
    """The words as an order ('reef the mainsail, one reef with the idlers'): its
    evolutions on its subjects. None if they are not an order that starts work."""
    try:
        order = grammar.parse(ship, text, vocab)
    except OrderError:
        return None
    if order.verb in WORK_VERBS:
        return None
    lines = vocab.group_evolutions.get(order.verb)
    if lines is not None:
        chosen: list[Instance] = []
        for line in lines:
            got = _by_order(ship, work, line, vocab)
            for inst in got[0] if got else []:
                if inst not in chosen:
                    chosen.append(inst)
        return chosen, _gerund_words(order.verb)
    evos = _evolution_ids(order.verb, vocab)
    if not evos:
        return None
    subjects: set[str] | None = None
    what = _gerund_words(order.verb)
    if order.object:
        try:
            res = resolve.resolve(ship, order.object, order.side_word, order.verb)
        except OrderError:
            return None
        subjects = _subject_ids(ship, list(res.ids))
        name = part_name(ship, res.ids[0]) if len(res.ids) == 1 else res.name
        what = f"{what} the {name}"
    return _matching(work, evos, subjects), what


def _by_kind(
    ship: Ship, work: list[Instance], words: list[str], vocab: Vocabulary
) -> tuple[list[Instance], str] | None:
    """A kind of work ('the reef', 'the reefs', 'the tack'), and its subject after 'in',
    'on' or 'of' if one is named ('the reef in the mainsail')."""
    if not words or words[0] not in vocab.work_nouns:
        return None
    verb = vocab.work_nouns[words[0]]
    evos = _evolution_ids(verb, vocab)
    rest = words[1:]
    if rest and rest[0] in _JOINING:
        rest = rest[1:]
    subjects: set[str] | None = None
    what = _gerund_words(verb)
    if rest:
        ids = _part_ids(ship, strip_article(rest), vocab)
        if ids is None:
            return None
        subjects = _subject_ids(ship, ids)
        what = f"{what} the {' '.join(strip_article(rest))}"
    return _matching(work, evos, subjects), what


def _by_part(
    ship: Ship, work: list[Instance], words: list[str], vocab: Vocabulary
) -> tuple[list[Instance], str] | None:
    """A part: every job whose subject it is ('the mainsail'; 'the topsails')."""
    ids = _part_ids(ship, words, vocab)
    if ids is None:
        return None
    return _matching(work, set(), set(ids)), "on the " + " ".join(words)


def _part_ids(ship: Ship, words: list[str], vocab: Vocabulary) -> list[str] | None:
    """The parts the words name, all of them and nothing more, or None."""
    words = [w for w in words if w != ","]
    if not words:
        return None
    try:
        phrase, side, rest = grammar._match_object(ship, words, vocab, "set", vocab.verbs["set"])
    except OrderError:
        return None
    if phrase is None or rest:
        return None
    try:
        res = resolve.resolve(ship, phrase, side, "belay")
    except OrderError:
        noun = resolve.noun_table(ship).lookup(phrase)
        return list(noun.ids) if noun is not None else None
    return list(res.ids)


def _gerund_words(verb: str) -> str:
    first, _, rest = verb.partition(" ")
    return f"{gerund(first)} {rest}".strip()
