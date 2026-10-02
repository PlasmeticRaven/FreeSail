"""The standing dialect's grammar (spec M4 §3), an extension of `orders/grammar.py`.

    standing order "<name>" [by the <officer>]: <trigger> [, if <condition>]
                                                then <order> [; <order> ...]

    trigger   := when <condition> [for <duration>] | at <event> | every <interval>
    condition := <reading> <comparison> [and <reading> <comparison> ...]
    comparison:= exceeds <n> <unit> | is over ... | is under ... | is below ...
               | is forward of <n> degrees | is abaft <n> degrees | is abaft the beam
               | is forward of the beam | backs <n> points | veers <n> points
               | veers <n> points or backs <n> points | shifts <n> points
               | is from <point> | is <state> | is not <state> | are <fatigue word>
               | is the <watch> | is <n> bells | is east of <point> | is straining
               | exceeds the rating | is under <n> inches | is falling fast | is overcast
               | is turning (the glass) | gets up (the sea)
    order     := an order of the ship | tell the <station> <words> | ask the <station> <question>
    duration  := <n> minutes | <n> seconds | a glass | a bell | half an hour | an hour | ...
    interval  := glass | bell | hour | watch | <n> minutes | half an hour | ...

The sentence is read from the raw text (the quotes around the name and the colon after
it are the sentence's own punctuation, which the imperative grammar's normalisation
drops), then the trigger and condition from the same normalised words the imperative
grammar reads, with its number words and its noun table, and the orders after `then` by
`orders.grammar.parse` itself, at give time, so that a misspelt sail is refused when the
standing order is given and not when it fires. Every refusal names the word. A word or a
question to a station after `then` (`tell the watcher ...`, `ask the watcher ...`,
package 31c) is resolved at give time by `orders.stations.for_standing` to a station
aboard, or refused ("there is no lookout aboard yet"); its words are free text.

An `at` of the weather's events that are the readings' changes ("at the glass falling
fast", package 31c) is kept as a `when` of the event's condition (`rules.Trigger`), which
fires at each coming to hold; `is turning` (the glass) and `gets up` (the sea) are the
comparisons those events are written in, and the dialect has them for itself too.

The readings a condition may name are the registry's (`freesail.api.readings`) and this
ship's sails and parts by their ordinary names; the comparisons each admits are decided
by the reading's kind. `parse_condition` is the seam package 26's Python API uses: a
condition given as dialect text, parsed alone.

The book's sentences (`standing orders`, `show standing order "x"`, `belay standing
order "x"`, `resume standing order "x"`, `belay all standing orders`, `strike standing
order "x"`) are recognised here too and carried out by the book (`book.py`) through
`handle`.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from freesail import units
from freesail.api import readings as R
from freesail.orders import errors, resolve
from freesail.orders import grammar as imperative
from freesail.orders.errors import OrderError
from freesail.orders.vocabulary import Vocabulary, load_vocabulary, normalise, strip_article
from freesail.physics.wind import GUST_WORDS
from freesail.standing.rules import (
    RANKS,
    Clause,
    Comparison,
    Condition,
    Rule,
    Trigger,
)

__all__ = [
    "BOOK_VERBS",
    "STANDING_VERBS",
    "BookCommand",
    "handle",
    "parse_condition",
    "parse_duration",
    "parse_standing",
    "recognises",
]

# The sentences of the dialect, longest first so that "belay all standing orders" is not
# read as "belay" a line, nor "standing orders" as "standing order".
BOOK_VERBS: tuple[str, ...] = (
    "belay all standing orders",
    "strike standing order",
    "resume standing order",
    "belay standing order",
    "show standing order",
    "standing orders",
)
STANDING_VERBS: tuple[str, ...] = ("standing order", *BOOK_VERBS)

_QUOTES = "\"'“”‘’"


def recognises(text: str) -> str | None:
    """The standing sentence the text begins with (its canonical verb), or None for an
    imperative order. The words are the vocabulary's verbs of object `standing` and their
    synonyms, longest first, so 'belay all standing orders' is not 'belay' a line."""
    return _matched(text)[0]


def _matched(text: str, vocab: Vocabulary | None = None) -> tuple[str | None, str | None]:
    """(canonical verb, the phrase as said) for a standing sentence, else (None, None)."""
    vocab = vocab or load_vocabulary()
    words = normalise(text).split()
    for phrase in vocab.verb_phrases:  # longest first
        verb = vocab.phrase_to_verb[phrase]
        if vocab.verbs[verb].object != "standing":
            continue
        pw = phrase.split()
        if words[: len(pw)] == pw:
            return verb, phrase
    return None, None


# ---------------------------------------------------------------------------
# The sentence
# ---------------------------------------------------------------------------


def _quoted_name(text: str, after: str) -> tuple[str, str]:
    """The name in quotes after `after`, and the text following its closing quote."""
    m = re.match(rf"^\s*{after}\s*", text, re.I)
    rest = text[m.end() :] if m else text
    if not rest or rest[0] not in _QUOTES:
        raise OrderError(
            f'A standing order is named in quotes: {after} "night routine": at sunset then '
            f"take in the royals."
        )
    close = -1
    for i in range(1, len(rest)):
        if rest[i] in _QUOTES:
            close = i
            break
    if close < 0:
        raise OrderError("The standing order's name wants its closing quote.")
    name = " ".join(rest[1:close].split())
    if not name:
        raise OrderError("A standing order needs a name between the quotes.")
    return name, rest[close + 1 :]


def _officer(text: str) -> tuple[str, str]:
    """'by the master: ...' -> ('master', ' ...'); no officer -> ('captain', text)."""
    m = re.match(r"^\s*by\s+(?:the\s+|a\s+)?(?P<who>[A-Za-z'’ ]+?)\s*(?=:)", text)
    if m is None:
        return "captain", text
    who = " ".join(m.group("who").lower().replace("’", "'").split())
    if who not in RANKS:
        raise OrderError(
            f"'{who}' is no officer who gives standing orders; say the captain, the first "
            f"lieutenant, a lieutenant, the master, the mate, a master's mate or a midshipman."
        )
    return who, text[m.end() :]


def parse_standing(
    ship: Any, text: str, given_tick: int = 0, vocab: Vocabulary | None = None
) -> Rule:
    """Parse `standing order "name": ...` against this ship. Raises OrderError."""
    vocab = vocab or load_vocabulary()
    sentence = " ".join(text.split())
    name, rest = _quoted_name(sentence, "standing order")
    officer, rest = _officer(rest)
    rest = rest.lstrip()
    if not rest.startswith(":"):
        raise OrderError(
            f"After the name say a colon and then when, at or every: standing order "
            f'"{name}": when the true wind exceeds 30 knots for 2 minutes then ...'
        )
    body = rest[1:].strip()
    m = re.search(r"\bthen\b", body, re.I)
    if m is None:
        raise OrderError(
            f"A standing order says what to do after 'then': standing order \"{name}\": "
            f"{body or '...'} then take in the royals."
        )
    head, tail = body[: m.start()], body[m.end() :]
    trigger, condition = _parse_head(head, ship, vocab, name)
    actions, held = _parse_actions(tail, ship, vocab, name)
    rule = Rule(
        name=name,
        trigger=trigger,
        actions=actions,
        condition=condition,
        given_by=officer,
        text=sentence,
        given_tick=given_tick,
        held=held,
    )
    return rule


def _parse_head(
    head: str, ship: Any, vocab: Vocabulary, name: str
) -> tuple[Trigger, Condition | None]:
    tokens = normalise(head).split()
    if not tokens:
        raise OrderError(
            f"Standing order '{name}' says nothing to wait for; say when, at or every."
        )
    # the ", if <condition>" tested at firing
    condition: Condition | None = None
    for j in range(1, len(tokens)):
        if tokens[j] == "if" and (tokens[j - 1] == "," or tokens[0] in ("at", "every")):
            cond_tokens = tokens[j + 1 :]
            if not cond_tokens:
                raise OrderError(f"Standing order '{name}': 'if' what? Name a reading.")
            condition = _parse_condition_tokens(cond_tokens, ship, vocab)
            tokens = tokens[:j]
            break
    while tokens and tokens[-1] == ",":
        tokens = tokens[:-1]
    kind = tokens[0]
    rest = tokens[1:]
    if kind == "when":
        if not rest:
            raise OrderError(f"Standing order '{name}': when what? Name a reading.")
        duration = 0
        if "for" in rest[1:]:
            i = len(rest) - 1 - rest[::-1].index("for")
            if i + 1 >= len(rest):
                raise OrderError(f"Standing order '{name}': for how long? Say 'for 2 minutes'.")
            duration = parse_duration(rest[i + 1 :], vocab)
            rest = rest[:i]
        cond = _parse_condition_tokens(rest, ship, vocab)
        text = f"when {cond.text}" + (f" for {_duration_words(duration)}" if duration else "")
        return Trigger("when", text, condition=cond, duration_s=duration), condition
    if kind == "at":
        words = " ".join(rest)
        spec = R.EVENTS.get(words) or R.EVENTS.get("the " + words)
        if spec is None:
            known = list(R.EVENTS)
            hint = errors.suggest(words, known, article="") or "."
            raise OrderError(
                f"'at {words}' names no event the ship knows{hint} The events are "
                f"{errors.join_names(known, 'and', limit=len(known))}."
            )
        if spec.absent:
            raise OrderError(spec.absent)
        return Trigger("at", f"at {spec.words}", event=spec.words), condition
    if kind == "every":
        if not rest:
            raise OrderError(f"Standing order '{name}': every what? A glass, an hour, a watch.")
        seconds = parse_duration(rest, vocab, every=True)
        return Trigger("every", f"every {' '.join(rest)}", interval_s=seconds), condition
    raise OrderError(
        f"A standing order begins with when, at or every, not '{kind}': "
        f'standing order "{name}": when the true wind exceeds 30 knots then ...'
    )


def _parse_actions(
    tail: str, ship: Any, vocab: Vocabulary, name: str
) -> tuple[list[str], str | None]:
    """The orders after `then`, each parsed now; and, when one of them is on a reading the
    ship has not got yet (`sound the well`), the registry's sentence for it: the standing
    order is entered and held until the world has that reading (package 33c; spec M4 §24
    item 4: the starter's `sound the well` was refused at every start since milestone 4a,
    a line of noise in every log)."""
    from freesail.orders import stations

    parts = [p.strip(" .") for p in tail.split(";")]
    actions = [" ".join(p.split()) for p in parts if p.strip()]
    if not actions:
        raise OrderError(f"Standing order '{name}' gives no order after 'then'.")
    absent = [r for r in R.REGISTRY if r.is_absent]
    held: str | None = None
    for order in actions:
        # a word or a question to a station (package 31c): resolved now to a station
        # aboard, its words free text, and delivered as the captain's own when it fires
        try:
            addressed = stations.for_standing(ship, order)
        except OrderError as e:
            raise OrderError(f"In standing order '{name}', '{order}' is refused: {e}") from None
        if addressed is not None:
            continue
        norm = f" {normalise(order)} "
        missing = next((r for r in absent if any(f" {w} " in norm for w in r.words)), None)
        if missing is not None:
            held = held or missing.absent
            continue
        if recognises(order):
            raise OrderError(
                f"In standing order '{name}', '{order}' is a standing order itself; the orders "
                f"after 'then' are plain orders to the ship."
            )
        try:
            imperative.parse(ship, order, vocab)
        except OrderError as e:
            raise OrderError(f"In standing order '{name}', '{order}' is refused: {e}") from None
    return actions, held


# ---------------------------------------------------------------------------
# Durations and intervals
# ---------------------------------------------------------------------------

_UNIT_SECONDS = {
    "second": 1,
    "seconds": 1,
    "minute": 60,
    "minutes": 60,
    "hour": 3600,
    "hours": 3600,
    "glass": 1800,
    "glasses": 1800,
    "bell": 1800,
    "bells": 1800,
    "watch": 14400,
    "watches": 14400,
}


def parse_duration(tokens: list[str], vocab: Vocabulary | None = None, every: bool = False) -> int:
    """'2 minutes', 'a glass', 'half an hour', 'an hour', 'two hours' -> seconds."""
    vocab = vocab or load_vocabulary()
    words = " ".join(tokens)
    if words in R.INTERVALS:
        return R.INTERVALS[words]
    if tokens and tokens[0] == "the" and " ".join(tokens[1:]) in R.INTERVALS:
        return R.INTERVALS[" ".join(tokens[1:])]
    if tokens:
        counted = imperative._count_at(tokens, 0, vocab)
        if counted is not None:
            value, used = counted
            unit = tokens[used] if used < len(tokens) else ""
            if unit in _UNIT_SECONDS and used + 1 == len(tokens):
                seconds = int(round(value * _UNIT_SECONDS[unit]))
                if seconds <= 0:
                    raise OrderError(f"'{words}' is no time at all.")
                return seconds
    what = "an interval" if every else "a duration"
    raise OrderError(
        f"'{words}' is not {what} the ship keeps; say minutes, a glass, half an hour, an hour "
        f"or a watch."
    )


def _duration_words(seconds: int) -> str:
    if seconds % 3600 == 0 and seconds >= 3600:
        n = seconds // 3600
        return "an hour" if n == 1 else f"{n} hours"
    if seconds % 60 == 0:
        n = seconds // 60
        return "a minute" if n == 1 else f"{n} minutes"
    return f"{seconds} seconds"


# ---------------------------------------------------------------------------
# Conditions
# ---------------------------------------------------------------------------


def parse_condition(text: str, ship: Any = None, vocab: Vocabulary | None = None) -> Condition:
    """Parse a condition alone: 'the true wind exceeds 30 knots and the heel is over 15
    degrees'. Package 26's `@when("...")` calls this. Without a ship, only the registry's
    readings may be named; a sail by name needs the ship."""
    tokens = normalise(text).split()
    if not tokens:
        raise OrderError("No condition given.")
    return _parse_condition_tokens(tokens, ship, vocab or load_vocabulary())


_STOP = frozenset({"and", "for", "then", ","})
# the words that open a condition on the distance to a place (package 36)
_DISTANCE_HEADS = ("the distance to", "distance to", "the distance of", "distance of")
# the words that may follow a sail's or a part's name in a condition (package 32b)
_AFTER_PART = frozenset({"is", "are", "isn't", "aren't", "exceeds", "exceed"}) | _STOP

# What each kind is compared with, for the refusal that names the word.
_HOW = {
    "speed": ("a speed", "in knots"),
    "direction": (
        "a wind",
        "in points ('backs two points', 'veers 1 point or backs 1 point') or 'is from' a "
        "compass point",
    ),
    "angle_on_bow": (
        "the apparent wind",
        "in degrees on the bow: 'is forward of 55 degrees', 'is abaft the beam'",
    ),
    "compass": ("a heading", "with a compass point: 'is east of south-west'"),
    "angle": ("an angle", "in degrees"),
    "watch": ("the watch", "by its name: 'is the middle watch'"),
    "bells": ("the time", "in bells: 'is eight bells'"),
    "daylight": ("daylight", "as day, twilight or night"),
    "sail": ("a sail", "by its state: is set, is shaking, is aback, is furled, is blown out"),
    "strain": ("the strain", "against the rating: 'exceeds the rating', 'is straining'"),
    "hands": ("the hands", "by their number or their fatigue: 'are worn out'"),
    "gust": ("the wind against its mean", "as a gust, at the mean or a lull: 'is a lull'"),
    "glass": ("the glass", "in inches: 'is under 29.5 inches'"),
    "sight": ("the land", "as in sight or not in sight"),
    "depth": ("the depth of water", "in fathoms: 'is under 10 fathoms'"),
    "position": (
        "a position by account",
        "against a latitude or a longitude: 'is north of 49 30 N', 'is west of 6 W'",
    ),
    "distance": ("a distance", "in miles: 'exceeds 20 miles'"),
    "ground": ("the ground", "by what the lead brings up: 'is sand', 'is not rock'"),
    "person": ("a person", "by his place: 'is on deck', 'is below'"),
    "tendency": (
        "the glass",
        "by its tendency: is steady, is rising, is falling, is falling fast, is rising fast, "
        "is turning",
    ),
    "sky": (
        "the sky",
        "by its look: is clear, is overcast, is dark and gloomy, is threatening, is hazy, is thick",
    ),
    "weather": (
        "the weather",
        "by its kind: is fine, is rain, is drizzle, is passing showers, is squally, is thunder, "
        "is fog",
    ),
    "visibility": (
        "the visibility",
        "by how far a sail is seen: is the horizon, is a few miles, is a mile, is a cable",
    ),
    "sea": (
        "the sea",
        "by its state: is smooth, is moderate, is short, is heavy, is very heavy, is confused; "
        "or 'gets up'",
    ),
    "motion": (
        "the motion",
        "by how she moves: is easy, is rolling, is rolling heavily, is pitching, is "
        "pitching heavily, is labouring",
    ),
    # package 33c
    "manoeuvre": (
        "the manoeuvre in hand",
        "by what she is about: is hove to, is not hove to, is tacking, is wearing, is "
        "heaving to, is filling away, is none",
    ),
}


def _how_compared(candidates: list[R.Reading]) -> tuple[str, str]:
    kinds = [c.kind for c in candidates]
    if set(kinds) == {"speed", "direction", "gust"}:
        return "a wind", "in knots or points, or as a gust, at the mean or a lull"
    if set(kinds) == {"speed", "direction"}:
        return "a wind", "in knots or points"
    if set(kinds) == {"glass", "tendency"}:
        return (
            "the glass",
            "in inches ('is under 29.5 inches') or by its tendency (is steady, is rising, is "
            "falling, is falling fast, is turning)",
        )
    if set(kinds) == {"sail", "strain"}:
        return (
            "a sail",
            "by its state (is set, is shaking, is aback, is furled, is blown out) or its strain",
        )
    if set(kinds) == {"angle_on_bow", "speed"}:
        return "the apparent wind", "in degrees on the bow or in knots"
    return _HOW.get(kinds[0], ("it", "otherwise"))


@dataclass
class _Match:
    phrase: str  # the reading's words as said
    candidates: list[R.Reading]
    params: tuple[str, ...]
    used: int


# The ship herself as a condition's subject (package 33c): "if she is hove to" is the
# manoeuvre in hand compared.
_SHE = {"she": "the manoeuvre in hand"}


def _match_reading(tokens: list[str], i: int, ship: Any, vocab: Vocabulary) -> _Match:
    if tokens[i] in _SHE:
        return _Match(tokens[i], R.REGISTRY.by_words(_SHE[tokens[i]]), (), 1)
    # the distance to a charted place, or to a point pricked on the chart, by account
    # (package 36; the passages' books: "when the distance to the Lizard is under 4
    # miles"): the parametric row read with the place's words as its parameter, which
    # run to the comparison's first word
    for head in _DISTANCE_HEADS:
        hw = head.split()
        if tokens[i : i + len(hw)] != hw:
            continue
        j = i + len(hw)
        k = j
        while k < len(tokens) and tokens[k] not in _AFTER_PART:
            k += 1
        place = " ".join(tokens[j:k])
        if place:
            rows = R.REGISTRY.by_words("the distance to <mark>")
            return _Match(f"the distance to {place}", rows, (place,), k - i)
    # the registry's words, longest first, with or without the article: "the true wind" or
    # "true wind", "daylight" or "the daylight" (package 33c; playtest 13's brig, "the
    # daylight is night" refused where "daylight is night" was taken)
    for phrase in R.REGISTRY.words():
        if "<" in phrase:
            continue
        pw = phrase.split()
        forms = [pw]
        if pw[0] == "the":
            forms.append(pw[1:])
        elif pw[0] not in ("what", "a"):
            forms.append(["the", *pw])
        for form in forms:
            if tokens[i : i + len(form)] == form:
                rows = R.REGISTRY.by_words(phrase)
                return _Match(phrase, rows, (), len(form))
    # a sail or a part of this ship by name: "the fore royal", "the royals", "the fore
    # royal yard", "the starboard fore topmast studdingsail"
    if ship is not None and hasattr(ship, "parts"):
        ws = strip_article(tokens[i:])
        side_word, ws2 = imperative._strip_side(ws, vocab)
        table = resolve.noun_table(ship)
        for n in range(min(6, len(ws2)), 0, -1):
            phrase = " ".join(ws2[:n])
            if table.lookup(phrase) is None:
                continue
            # Package 32b: the name must be followed by its comparison, or a shorter
            # name inside a longer one is taken ("the fore topsail is shaking" on the
            # cutter, whose 'the fore' is her staysail and who has no fore topsail, read
            # as 'the fore' compared 'topsail shaking'); an unknown name falls through to
            # the refusal below, which suggests the nearest.
            if n < len(ws2) and ws2[n] not in _AFTER_PART:
                continue
            res = resolve.resolve(ship, phrase, side_word, "standing order")
            ids = tuple(res.ids)
            if all(pid in ship.sails for pid in ids):
                rows = [R.REGISTRY.get("sail"), R.REGISTRY.get("strain")]
            else:
                rows = [R.REGISTRY.get("strain")]
            said = (
                ("the " if tokens[i] == "the" else "")
                + (f"{side_word} " if side_word else "")
                + phrase
            )
            used = (len(tokens) - i) - (len(ws2) - n)
            return _Match(said, rows, ids, used)
    # nothing: name the nearest readings
    stop = next((k for k in range(i, len(tokens)) if tokens[k] in _STOP), len(tokens))
    said = " ".join(tokens[i:stop])
    known = [w for w in R.REGISTRY.words() if "<" not in w]
    if ship is not None and hasattr(ship, "sails"):
        known += [f"the {resolve.display_name(ship, s)}" for s in ship.sails]
    hint = errors.suggest(said, known, article="") or "."
    raise OrderError(
        f"'{said}' is not a reading the ship has{hint} A condition names the true wind, the "
        f"apparent wind, the heading, the speed, the heel, the watch, the strain, the hands "
        f"on deck, the glass, the sky, the weather, the sea, the motion, or a sail by name."
    )


def _number(tokens: list[str], i: int, vocab: Vocabulary) -> tuple[float, int] | None:
    if i >= len(tokens):
        return None
    return imperative._count_at(tokens, i, vocab)


_GT = (
    "exceeds",
    "is over",
    "is above",
    "is more than",
    "is greater than",
    "are more than",
    "are over",
    "are above",
    "exceed",
    "number more than",
)
_LT = (
    "is under",
    "is below",
    "is less than",
    "is fewer than",
    "are under",
    "are below",
    "are fewer than",
    "are less than",
    "is short of",
)
_SPEED_UNITS = ("knots", "knot", "kn")
_ANGLE_UNITS = ("degrees", "degree")
_COUNT_UNITS = ("hands", "men", "hand", "man")
_GLASS_UNITS = ("inches", "inch")
_DEPTH_UNITS = ("fathoms", "fathom", "fm")
_DISTANCE_UNITS = ("miles", "mile", "leagues", "league")


def _lat_or_lon(
    tokens: list[str], i: int, stop: int, latitude: bool
) -> tuple[float, str, int] | None:
    """'49 30 n', '49.5', '6 10 w' at tokens[i]: degrees (signed north and east), the
    words said, and the tokens used; None when no number is there."""
    j = i
    if j >= stop:
        return None
    try:
        value = float(tokens[j])
    except ValueError:
        return None
    j += 1
    if j < stop and tokens[j] in ("degrees", "degree"):
        j += 1
    if j < stop:
        try:
            minutes = float(tokens[j])
            value += minutes / 60.0
            j += 1
        except ValueError:
            pass
    if j < stop and tokens[j] in ("minutes", "minute"):
        j += 1
    letters = ("n", "s") if latitude else ("e", "w")
    if j < stop and tokens[j] in letters:
        if tokens[j] in ("s", "w"):
            value = -value
        j += 1
    elif not latitude:
        value = -value  # the Channel: a bare longitude is west
    return value, " ".join(tokens[i:j]), j - i


def _starts(tokens: list[str], i: int, phrase: str) -> int:
    pw = phrase.split()
    return len(pw) if tokens[i : i + len(pw)] == pw else 0


def _longest(tokens: list[str], i: int, phrases) -> tuple[str | None, int]:
    best, n = None, 0
    for p in phrases:
        k = _starts(tokens, i, p)
        if k > n:
            best, n = p, k
    return best, n


def _compass_at(tokens: list[str], i: int) -> tuple[float, str, int] | None:
    j = i + 1 if tokens[i : i + 1] == ["the"] else i
    for k in range(min(5, len(tokens) - j), 0, -1):
        phrase = " ".join(tokens[j : j + k])
        angle = units.parse_compass_point(phrase)
        if angle is not None:
            return angle, units.point_name(angle, full=True), (j - i) + k
    return None


def _pick(candidates: list[R.Reading], kinds: tuple[str, ...]) -> R.Reading | None:
    for c in candidates:
        if c.kind in kinds:
            return c
    return None


def _parse_comparison(
    tokens: list[str], i: int, match: _Match, vocab: Vocabulary
) -> tuple[R.Reading, Comparison, int]:
    """The comparison at tokens[i] for the reading matched. Returns the reading chosen
    among the phrase's candidates, the comparison, and the words used."""
    cands = match.candidates
    if all(c.is_absent for c in cands):
        raise OrderError(cands[0].absent or f"The ship has no reading '{match.phrase}' yet.")
    cands = [c for c in cands if not c.is_absent]
    stop = next((k for k in range(i, len(tokens)) if tokens[k] in _STOP), len(tokens))
    tail = tokens[i:stop]
    tail_words = " ".join(tail)

    def refuse(said: str | None = None) -> OrderError:
        quoted = (
            said
            if said is not None
            else " ".join(w for w in tail if w not in ("is", "are")) or tail_words
        )
        what, how = _how_compared(cands)
        return OrderError(f"'{match.phrase}' cannot be '{quoted}'; {what} is compared {how}.")

    if not tail:
        what, how = _how_compared(cands)
        raise OrderError(
            f"'{match.phrase}' compared how? {what[0].upper()}{what[1:]} is compared {how}."
        )

    # -- the strain's own words
    for phrase in ("exceeds the rating", "is over the rating", "is above the rating"):
        n = _starts(tokens, i, phrase)
        if n:
            row = _pick(cands, ("strain",))
            if row is None:
                raise refuse()
            return row, Comparison("gt", 1.0, "over the rating"), n
    for phrase in ("is straining", "are straining"):
        n = _starts(tokens, i, phrase)
        if n:
            row = _pick(cands, ("strain",))
            if row is None:
                raise refuse()
            return row, Comparison("straining", R.STRAINING_RATIO, "straining"), n

    # -- the reckoning's readings (package 33a): a position against a latitude or a
    # longitude; the ground by its words; a person by his place
    row = _pick(cands, ("position",))
    if row is not None:
        for phrase, op in (
            ("is north of", "north_of"),
            ("is south of", "south_of"),
            ("is east of", "east_of"),
            ("is west of", "west_of"),
        ):
            n = _starts(tokens, i, phrase)
            if n:
                parsed = _lat_or_lon(tokens, i + n, stop, op in ("north_of", "south_of"))
                if parsed is None:
                    what = "latitude" if op in ("north_of", "south_of") else "longitude"
                    raise OrderError(
                        f"'{match.phrase} {phrase[3:]}' what {what}? Say "
                        f"'{phrase[3:]} {'49 30 N' if what == 'latitude' else '6 10 W'}'."
                    )
                value, said, used = parsed
                return row, Comparison(op, value, f"{phrase[3:]} {said}"), n + used
        raise refuse()
    row = _pick(cands, ("ground",))
    if row is not None:
        for phrase, op in (("is not", "is_not"), ("is", "is")):
            n = _starts(tokens, i, phrase)
            if n:
                words = tokens[i + n : stop]
                if not words:
                    raise OrderError(f"'{match.phrase} {phrase}' what ground? Say sand, mud, rock.")
                ground = " ".join(words)
                said = f"{'not ' if op == 'is_not' else ''}{ground}"
                return row, Comparison(op, ground, said), n + len(words)
        raise refuse()
    row = _pick(cands, ("person",))
    if row is not None:
        for phrase, op, place in (
            ("is on deck", "is", "on deck"),
            ("is not on deck", "is_not", "on deck"),
            ("is below", "is", "below"),
            ("is not below", "is_not", "below"),
        ):
            n = _starts(tokens, i, phrase)
            if n:
                return row, Comparison(op, place, phrase[3:]), n
        raise refuse()

    # -- the apparent wind: forward of, abaft, on the bow
    for phrase, op in (
        ("is forward of the beam", "forward_of"),
        ("is before the beam", "forward_of"),
        ("is abaft the beam", "abaft"),
        ("is aft of the beam", "abaft"),
    ):
        n = _starts(tokens, i, phrase)
        if n:
            row = _pick(cands, ("angle_on_bow",))
            if row is None:
                raise refuse()
            return row, Comparison(op, 90.0, phrase[3:]), n
    for phrase, op in (
        ("is forward of", "forward_of"),
        ("is abaft", "abaft"),
        ("is aft of", "abaft"),
    ):
        n = _starts(tokens, i, phrase)
        if n:
            row = _pick(cands, ("angle_on_bow",))
            if row is None:
                raise refuse()
            num = _number(tokens, i + n, vocab)
            if num is None:
                raise OrderError(f"'{match.phrase} {phrase[3:]}' how many degrees?")
            value, used = num
            unit = tokens[i + n + used] if i + n + used < stop else ""
            if unit in ("points", "point"):
                value, unit_words = (
                    units.rad_to_deg(units.points_to_rad(value)),
                    f"{value:g} points",
                )
                used += 1
            elif unit in _ANGLE_UNITS:
                unit_words = f"{value:g} degrees"
                used += 1
            elif unit:
                raise OrderError(f"'{match.phrase}' is compared in degrees on the bow, not {unit}.")
            else:
                unit_words = f"{value:g} degrees"
            return row, Comparison(op, float(value), f"{phrase[3:]} {unit_words}"), n + used
    for phrase, side in (
        ("is on the starboard bow", "starboard"),
        ("is on the starboard side", "starboard"),
        ("is on the starboard quarter", "starboard"),
        ("is on the larboard bow", "larboard"),
        ("is on the larboard side", "larboard"),
        ("is on the larboard quarter", "larboard"),
        ("is on the port bow", "larboard"),
        ("is on the port side", "larboard"),
    ):
        n = _starts(tokens, i, phrase)
        if n:
            row = _pick(cands, ("angle_on_bow",))
            if row is None:
                raise refuse()
            return row, Comparison("side", side, phrase[3:]), n

    # -- the wind's direction: backs, veers, shifts (either way), is from; and "veers one
    #    point or backs one point", the one 'or' the dialect has: the two ways one reading
    #    turns, which is a shift (package 29b, the starter's "trim on a shift")
    for verb in ("backs", "veers", "hauls", "shifts"):
        n = _starts(tokens, i, verb)
        if n:
            row = _pick(cands, ("direction",))
            if row is None:
                raise refuse()
            op = {"backs": "backs", "shifts": "shifts"}.get(verb, "veers")
            value, used = _points(tokens, i + n, match.phrase, verb, vocab)
            said = _points_said(value)
            if op == "shifts":
                return (
                    row,
                    Comparison("shifts", (float(value), float(value)), f"shifts {said}"),
                    n + used,
                )
            k = i + n + used
            other = "veers" if op == "backs" else "backs"
            if tokens[k : k + 2] == ["or", other]:
                more, more_used = _points(tokens, k + 2, match.phrase, other, vocab)
                veer, back = (
                    (float(value), float(more)) if op == "veers" else (float(more), float(value))
                )
                text = f"{op} {said} or {other} {_points_said(more)}"
                return row, Comparison("shifts", (veer, back), text), n + used + 2 + more_used
            return row, Comparison(op, float(value), f"{op} {said}"), n + used
    # -- the sea getting up (package 31c): its state word higher than when the order stood,
    #    and afresh after each firing, as a wind's shift is measured
    for phrase in ("is getting up", "gets up"):
        n = _starts(tokens, i, phrase)
        if n:
            row = _pick(cands, ("sea",))
            if row is None:
                raise refuse()
            return row, Comparison("gets_up", None, "gets up"), n
    n = _starts(tokens, i, "is from")
    if n:
        row = _pick(cands, ("direction",))
        if row is None:
            raise refuse()
        cp = _compass_at(tokens, i + n)
        if cp is None:
            raise OrderError(
                f"'{match.phrase} is from' what point? Say a compass point, such as the north-west."
            )
        angle, name, used = cp
        return row, Comparison("from", angle, f"from the {name}"), n + used

    # -- a heading: east of, west of, a point
    for phrase, op in (("is east of", "east_of"), ("is west of", "west_of")):
        n = _starts(tokens, i, phrase)
        if n:
            row = _pick(cands, ("compass",))
            if row is None:
                raise refuse()
            cp = _compass_at(tokens, i + n)
            if cp is None:
                raise OrderError(f"'{match.phrase} {phrase[3:]}' what point? Say a compass point.")
            angle, name, used = cp
            return row, Comparison(op, angle, f"{phrase[3:]} {name}"), n + used

    # -- is / is not / are / are not a word: a watch, the bells, daylight, a sail's state,
    #    the hands' fatigue, or a compass point
    for head in ("is not", "are not", "is", "are"):
        n = _starts(tokens, i, head)
        if not n:
            continue
        op = "is_not" if head.endswith("not") else "is"
        rest = tokens[i + n : stop]
        j = i + n
        # the watch
        row = _pick(cands, ("watch",))
        if row is not None:
            name, k = _longest(
                tokens, j + (1 if tokens[j : j + 1] == ["the"] else 0), R.WATCH_NAMES
            )
            if name:
                k += 1 if tokens[j : j + 1] == ["the"] else 0
                return (
                    row,
                    Comparison(op, name, f"{'not ' if op == 'is_not' else ''}the {name}"),
                    n + k,
                )
            raise refuse()
        # the bells
        row = _pick(cands, ("bells",))
        if row is not None:
            num = _number(tokens, j, vocab)
            if num is not None:
                value, used = num
                unit = tokens[j + used] if j + used < stop else ""
                if unit in ("bells", "bell") and 1 <= value <= 8 and value == int(value):
                    return (
                        row,
                        Comparison(
                            op,
                            int(value),
                            f"{'not ' if op == 'is_not' else ''}{units.format_bells(int(value))}",
                        ),
                        n + used + 1,
                    )
            raise refuse()
        # daylight
        row = _pick(cands, ("daylight",))
        if row is not None:
            word, k = _longest(tokens, j, R.DAYLIGHT_WORDS)
            if word:
                return row, Comparison(op, word, f"{'not ' if op == 'is_not' else ''}{word}"), n + k
            raise refuse()
        # a sail's state
        row = _pick(cands, ("sail",))
        if row is not None:
            word, k = _longest(tokens, j, R.SAIL_STATE_WORDS)
            if word:
                return row, Comparison(op, word, f"{'not ' if op == 'is_not' else ''}{word}"), n + k
            # a sail may strain too: "the fore royal is straining" was caught above
            raise refuse()
        # the manoeuvre in hand (package 33c): "she is hove to", "the manoeuvre in hand
        # is tacking", "is none"
        row = _pick(cands, ("manoeuvre",))
        if row is not None:
            word, k = _longest(tokens, j, _MANOEUVRE_SAID)
            if word:
                value = _MANOEUVRE_SAID[word]
                said = f"{'not ' if op == 'is_not' else ''}{value}"
                return row, Comparison(op, value, said), n + k
            raise refuse()
        # the hands: a fatigue word, or a number below ("are under 40")
        row = _pick(cands, ("hands",))
        if row is not None:
            word, k = _longest(tokens, j, R.FATIGUE_WORDS)
            if word:
                return row, Comparison(op, word, f"{'not ' if op == 'is_not' else ''}{word}"), n + k
            break
        # the true wind against its ten-minute mean (package 29b): a gust, the mean, a lull
        row = _pick(cands, ("gust",))
        if row is not None:
            word, k = _longest(tokens, j, _GUST_SAID)
            if word:
                value = _GUST_SAID[word]
                said = f"{'not ' if op == 'is_not' else ''}{value}"
                return row, Comparison(op, value, said), n + k
        # the weather's words (spec M5 §5): the glass's tendency, the sky, the weather, the
        # visibility; a number after 'is' falls through to the inches below
        for kind, table in (
            ("tendency", _TENDENCY_SAID),
            ("sky", _SKY_SAID),
            ("weather", _WEATHER_SAID),
            ("visibility", _VISIBILITY_SAID),
            ("sea", _SEA_SAID),
            ("motion", _MOTION_SAID),
            ("sight", _SIGHT_SAID),
        ):
            row = _pick(cands, (kind,))
            if row is None:
                continue
            word, k = _longest(tokens, j, table)
            if word:
                value = table[word]
                said = f"{'not ' if op == 'is_not' else ''}{value}"
                return row, Comparison(op, value, said), n + k
            if kind != "tendency":
                raise refuse()
        # a heading is a point
        row = _pick(cands, ("compass",))
        if row is not None and op == "is":
            cp = _compass_at(tokens, j)
            if cp is not None:
                angle, name, used = cp
                return row, Comparison("point", angle, name), n + used
            raise refuse()
        if not rest:
            raise refuse(head)
        # "is 30 knots"? only with over/under; say so below
        break

    # -- numbers: exceeds, is over, is under, is below
    for phrases, op in ((_GT, "gt"), (_LT, "lt")):
        phrase, n = _longest(tokens, i, phrases)
        if not phrase:
            continue
        num = _number(tokens, i + n, vocab)
        if num is None:
            raise OrderError(f"'{match.phrase} {phrase}' what number?")
        value, used = num
        unit = tokens[i + n + used] if i + n + used < stop else ""
        if unit in _SPEED_UNITS:
            row = _pick(cands, ("speed",))
            if row is None:
                raise OrderError(f"'{match.phrase}' is compared in {_unit_of(cands)}, not knots.")
            return (
                row,
                Comparison(op, float(value), f"{phrase.split()[-1]} {value:g} knots"),
                n + used + 1,
            )
        if unit in _ANGLE_UNITS:
            row = _pick(cands, ("angle",))
            if row is None:
                if _pick(cands, ("angle_on_bow",)) is not None:
                    raise OrderError(
                        f"'{match.phrase}' is compared on the bow: say 'is forward of {value:g} "
                        f"degrees' or 'is abaft {value:g} degrees'."
                    )
                raise OrderError(f"'{match.phrase}' is compared in {_unit_of(cands)}, not degrees.")
            return (
                row,
                Comparison(op, float(value), f"{phrase.split()[-1]} {value:g} degrees"),
                n + used + 1,
            )
        if unit in _COUNT_UNITS:
            row = _pick(cands, ("hands",))
            if row is None:
                raise OrderError(f"'{match.phrase}' is compared in {_unit_of(cands)}, not hands.")
            return (
                row,
                Comparison(op, float(value), f"{phrase.split()[-1]} {value:g}"),
                n + used + 1,
            )
        if unit in _GLASS_UNITS:
            row = _pick(cands, ("glass",))
            if row is None:
                raise OrderError(f"'{match.phrase}' is compared in {_unit_of(cands)}, not inches.")
            return (
                row,
                Comparison(op, float(value), f"{phrase.split()[-1]} {value:g} inches"),
                n + used + 1,
            )
        if unit in _DEPTH_UNITS:
            row = _pick(cands, ("depth",))
            if row is None:
                raise OrderError(f"'{match.phrase}' is compared in {_unit_of(cands)}, not fathoms.")
            return (
                row,
                Comparison(op, float(value), f"{phrase.split()[-1]} {value:g} fathoms"),
                n + used + 1,
            )
        if unit in _DISTANCE_UNITS:
            row = _pick(cands, ("distance",))
            if row is None:
                raise OrderError(f"'{match.phrase}' is compared in {_unit_of(cands)}, not miles.")
            miles = float(value) * (3.0 if unit.startswith("league") else 1.0)
            return (
                row,
                Comparison(op, miles, f"{phrase.split()[-1]} {value:g} {unit}"),
                n + used + 1,
            )
        if unit and unit not in _STOP:
            raise OrderError(f"'{match.phrase}' is compared in {_unit_of(cands)}, not {unit}.")
        # no unit said: the reading's own
        row = _pick(cands, ("speed", "angle", "strain", "hands", "glass", "depth", "distance"))
        if row is None:
            raise refuse()
        unit_words = {
            "speed": " knots",
            "angle": " degrees",
            "strain": "",
            "hands": "",
            "glass": " inches",
            "depth": " fathoms",
            "distance": " miles",
        }[row.kind]
        return (
            row,
            Comparison(op, float(value), f"{phrase.split()[-1]} {value:g}{unit_words}"),
            n + used,
        )

    raise refuse()


def _points(
    tokens: list[str], i: int, phrase: str, verb: str, vocab: Vocabulary
) -> tuple[float, int]:
    """'two points', 'a point and a half' at tokens[i]: the number and the words used."""
    num = _number(tokens, i, vocab)
    if num is None:
        raise OrderError(f"'{phrase} {verb}' how many points?")
    value, used = num
    unit = tokens[i + used] if i + used < len(tokens) else ""
    if unit not in ("point", "points"):
        raise OrderError(f"A wind {verb} in points: '{phrase} {verb} two points'.")
    used += 1
    more = imperative._and_a_half(tokens, i + used)
    return (value + 0.5 if more else value), used + more


def _points_said(value: float) -> str:
    """ "2 points", "1 point", "1.5 points"."""
    return f"{value:g} {'point' if value == 1 else 'points'}"


# The words for the wind against its mean, as said, and the reading's value for each.
_GUST_SAID: dict[str, str] = {
    "a gust above the mean": GUST_WORDS[0],
    "a gust above its mean": GUST_WORDS[0],
    "a gust": GUST_WORDS[0],
    "at the mean": GUST_WORDS[1],
    "at its mean": GUST_WORDS[1],
    "the mean": GUST_WORDS[1],
    "a lull": GUST_WORDS[2],
}


# The weather's words as said, and the reading's value for each (spec M5 §5): the period's
# words for the glass, Beaufort's for the sky and the weather, the lookout's for how far.
_TENDENCY_SAID: dict[str, str] = {w: w for w in R.TENDENCY_WORDS}
# the glass turning (package 31c): the last hour's change against the three hours'
# (`rules.GLASS_TURN_IN`), not a word of the tendency itself
_TENDENCY_SAID["turning"] = "turning"
_SKY_SAID: dict[str, str] = {w: w for w in R.SKY_WORDS}
_SKY_SAID.update({"cloudy": "overcast", "gloomy": "dark and gloomy", "misty": "hazy"})
_WEATHER_SAID: dict[str, str] = {w: w for w in R.WEATHER_WORDS}
_WEATHER_SAID.update(
    {
        "raining": "rain",
        "drizzling": "drizzle",
        "showers": "passing showers",
        "showery": "passing showers",
        "squalls": "squally",
        "foggy": "fog",
        "fair": "fine",
    }
)
_VISIBILITY_SAID: dict[str, str] = {w: w for w in R.VISIBILITY_WORDS}
_VISIBILITY_SAID.update({"the horizon": "the horizon", "a cable's length": "a cable"})
# The sea's and the motion's words (spec M5 §4): the state word each is compared by
# (rules._sea_is, rules._motion_is), and the ways of saying it.
_SEA_SAID: dict[str, str] = {w: w for w in R.SEA_STATE_WORDS}
_SEA_SAID.update(
    {
        "chopping": "short",
        "short and chopping": "short",
        "a short chopping sea": "short",
        "rough": "heavy",
        "high": "very heavy",
        "confused": "confused",
        "cross": "confused",
        "a cross sea": "confused",
        "a confused sea": "confused",
        "calm": "smooth",
    }
)
# the land (package 32): in sight or not, the lookout's word
_SIGHT_SAID: dict[str, str] = {
    "in sight": "in sight",
    "not in sight": "not in sight",
    "out of sight": "not in sight",
}
_MOTION_SAID: dict[str, str] = {w: w for w in R.MOTION_STATE_WORDS}
_MOTION_SAID.update(
    {
        "rolling heavily": "rolling heavily",
        "pitching heavily": "pitching heavily",
        "labouring heavily": "labouring",
        "laboring": "labouring",
        "laboring heavily": "labouring",
        "heavy": "heavy",
        "quiet": "easy",
        "steady": "easy",
    }
)


# The manoeuvre in hand's words as said (package 33c), and the reading's value for each.
_MANOEUVRE_SAID: dict[str, str] = {w: w for w in R.MANOEUVRE_WORDS.values()}
_MANOEUVRE_SAID.update(
    {
        R.HOVE_TO_WORDS: R.HOVE_TO_WORDS,
        "lying to": R.HOVE_TO_WORDS,
        "lying hove to": R.HOVE_TO_WORDS,
        R.NO_MANOEUVRE_WORDS: R.NO_MANOEUVRE_WORDS,
        "nothing": R.NO_MANOEUVRE_WORDS,
        "going about": "tacking",
        "in stays": "tacking",
        "box hauling": "box hauling",
    }
)


def _unit_of(cands: list[R.Reading]) -> str:
    kinds = {c.kind for c in cands}
    if kinds & {"glass"}:
        return "inches"
    if kinds & {"depth"}:
        return "fathoms"
    if kinds & {"distance"}:
        return "miles"
    if kinds & {"speed"}:
        return "knots"
    if kinds & {"angle"}:
        return "degrees"
    if kinds & {"strain"}:
        return "a ratio of the rating"
    if kinds & {"hands"}:
        return "hands"
    return _how_compared(cands)[1]


def _parse_condition_tokens(tokens: list[str], ship: Any, vocab: Vocabulary) -> Condition:
    clauses: list[Clause] = []
    i = 0
    while i < len(tokens):
        match = _match_reading(tokens, i, ship, vocab)
        j = i + match.used
        if j >= len(tokens):
            what, how = _how_compared(
                [c for c in match.candidates if not c.is_absent] or match.candidates
            )
            if all(c.is_absent for c in match.candidates):
                raise OrderError(match.candidates[0].absent or "")
            raise OrderError(
                f"'{match.phrase}' compared how? {what[0].upper()}{what[1:]} is compared {how}."
            )
        row, comparison, used = _parse_comparison(tokens, j, match, vocab)
        k = j + used
        text = " ".join(tokens[i:k])
        clauses.append(Clause(row.id, comparison, text, match.params, match.phrase))
        if k >= len(tokens):
            break
        if tokens[k] != "and":
            raise OrderError(
                f"After '{text}' I expected 'and', 'for' or 'then', not '{tokens[k]}'."
            )
        i = k + 1
        if i >= len(tokens):
            raise OrderError(f"After '{text} and' name another reading.")
    return Condition(clauses, " and ".join(c.text for c in clauses))


# ---------------------------------------------------------------------------
# The book's sentences
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class BookCommand:
    verb: str  # a member of BOOK_VERBS
    name: str | None


def parse_book_command(text: str) -> BookCommand:
    verb, phrase = _matched(text)
    if verb is None or verb == "standing order" or phrase is None:
        raise OrderError(f"'{text}' is not one of the book's orders.")
    said = " ".join(text.split())
    rest = said[len(" ".join(said.split()[: len(phrase.split())])) :]
    if verb in ("standing orders", "belay all standing orders"):
        if rest.strip(" .?"):
            raise OrderError(
                f"'{verb}' takes nothing after it; to name one say 'show standing order \"x\"'."
            )
        return BookCommand(verb, None)
    rest = rest.strip()
    if rest and rest[0] in _QUOTES:
        name, after = _quoted_name(rest, "")
        if after.strip(" ."):
            raise OrderError(f"'{verb}' names one standing order; '{after.strip()}' was left over.")
    else:
        name = " ".join(rest.strip(" .").split())
    if not name:
        raise OrderError(f"'{verb}' which? Name it in quotes: {verb} \"night routine\".")
    return BookCommand(verb, name)


# The book's verbs said bare before a standing order's name (package 33c; playtest 13's
# brig: `belay "blind lead"` was read as a line called the blind lead).
_BARE_BOOK = {
    "belay": "belay standing order",
    "avast": "belay standing order",
    "resume": "resume standing order",
    "show": "show standing order",
    "strike": "strike standing order",
}


def bare_book_sentence(ship: Any, text: str) -> str | None:
    """`belay "blind lead"`, `resume "trim by the wind"`, `show "night routine"`: the
    book's sentence the words mean, when they say a standing order's name in quotes (which
    the book then finds case-blind and by any distinct part of its name, `Book.find`), or
    the whole name of one in the book without them; None for anything else, so that
    `belay the main sheet` is still the line verb."""
    runtime = (getattr(ship, "extra", None) or {}).get("standing")
    if runtime is None:
        return None
    said = " ".join(text.split())
    first, _, rest = said.partition(" ")
    verb = _BARE_BOOK.get(first.lower())
    rest = rest.strip()
    if verb is None or not rest:
        return None
    if rest[0] in _QUOTES:
        try:
            name, after = _quoted_name(rest, "")
        except OrderError:
            return None
        if after.strip(" ."):
            return None
        return f'{verb} "{name}"'
    rule = runtime.book.get(rest.strip(" ."))
    return f'{verb} "{rule.name}"' if rule is not None else None


def handle(ship: Any, text: str) -> tuple[str, str, dict[str, Any]]:
    """Carry out a standing sentence for `orders.handle`: enter a standing order in the
    book, or list, show, belay or resume. Needs the runtime the world attached
    (`ship.extra['standing']`)."""
    runtime = (getattr(ship, "extra", None) or {}).get("standing")
    if runtime is None:
        raise OrderError(
            "This ship keeps no book of standing orders; the world was made without one."
        )
    verb = recognises(text)
    if verb == "standing order":
        rule = parse_standing(ship, text, given_tick=runtime.world.clock.tick)
        return runtime.book.enter(rule)
    command = parse_book_command(text)
    return runtime.book.carry_out(command)
