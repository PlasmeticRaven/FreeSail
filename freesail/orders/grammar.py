"""The grammar of an order (spec §8.1): from text to an `Order`.

    order       := verb_phrase [ object ] { modifier } [ "," side ]
    object      := [ "the" ] [ side_word ] noun [ side_word ]
    modifier    := "sharp up" | "square" | "in" | "up"
                 | "on the" tack_word "tack"
                 | count "reef" | count "reefs" | "close"
                 | "a fathom" | count "fathoms" | "a little" | "handsomely" | "roundly"
                 | "to" heading | heading
    heading     := number ["degrees"] | compass-point
                 | count "point"/"points" ("up" | "off" | "to starboard" | "to larboard")

How the parser reads a line:

1. It lower-cases the text, turns hyphens into spaces and drops punctuation
   other than commas and apostrophes.
2. It matches the longest verb phrase at the start ("take in", "keep her
   full", "brace"), including synonyms from `vocabulary.yaml`.
3. For a verb that takes a thing, it finds the longest run of words after
   the verb that is a noun of this ship ("fore topsail", "main brace",
   "royals"), with an optional "the" before it and an optional side word
   before or after it ("weather main brace", "main brace, starboard").
4. Everything left is modifiers, read left to right. A word that is neither
   a modifier nor part of the noun is an error naming the word and the
   nearest words that would have been understood.

The parser does not decide what the order *means* for the ship; that is
`verbs.py`. It only produces an `Order`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from freesail import units
from freesail.orders import errors
from freesail.orders.errors import OrderError
from freesail.orders.resolve import noun_table
from freesail.orders.vocabulary import (
    VerbSpec,
    Vocabulary,
    load_vocabulary,
    normalise,
    strip_article,
)
from freesail.ship.graph import Ship


@dataclass
class Order:
    """A parsed order. `modifiers` holds whatever qualifiers were given.

    Modifier keys that may appear:
      brace_mode   "sharp up" | "up" | "in" | "square" | "by the lifts"
      tack         "starboard" | "larboard"        from "on the X tack"
      reefs        int                              "two reefs"
      close        True                             "close reefed"
      fathoms      float                            "a fathom", "two fathoms"
      a_little     True
      manner       "handsomely" | "roundly" | ...
      heading      float, radians clockwise from north (absolute)
      heading_text what was said for it, for the log
      points       float                            "two points"
      direction    "up" | "off" | "starboard" | "larboard"
    """

    text: str  # the normalised order
    verb: str  # canonical verb name
    verb_phrase: str  # the words that matched it
    object: str | None = None  # the noun phrase as spoken, without 'the' or side
    side_word: str | None = None  # starboard | larboard | port | weather | lee | both
    modifiers: dict[str, Any] = field(default_factory=dict)

    @property
    def spec(self) -> VerbSpec:
        return load_vocabulary().verbs[self.verb]


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def parse(ship: Ship, text: str, vocab: Vocabulary | None = None) -> Order:
    """Parse one order against this ship's vocabulary. Raises OrderError."""
    vocab = vocab or load_vocabulary()
    norm = normalise(text).replace("°", " degrees ")
    norm = " ".join(norm.split())
    if not norm or norm == ",":
        raise OrderError("No order given.")
    segments = [seg.split() for seg in norm.split(" , ")]
    segments = [seg for seg in segments if seg]
    if not segments:
        raise OrderError("No order given.")
    words = segments[0]

    verb_phrase, verb = _match_verb(words, vocab)
    spec = vocab.verbs[verb]
    if spec.level == "driver":
        raise OrderError(
            f"'{verb_phrase}' is a console command, not an order to the ship; "
            f"the ship takes orders such as 'set the topsails' or 'steer south-west'."
        )
    rest = words[len(verb_phrase.split()) :]

    obj: str | None = None
    side_word: str | None = None
    if spec.object in ("sail", "yards", "line"):
        obj, side_word, rest = _match_object(ship, rest, vocab, verb, spec)

    tail = list(rest)
    for seg in segments[1:]:
        tail.extend(seg)
    mods, side_from_mods = _parse_modifiers(tail, vocab, verb)
    if side_from_mods is not None:
        if side_word is not None and side_from_mods != side_word:
            raise OrderError(
                f"Two sides were given ('{side_word}' and '{side_from_mods}'); say one."
            )
        side_word = side_from_mods
    return Order(
        text=norm.replace(" , ", ", "),
        verb=verb,
        verb_phrase=verb_phrase,
        object=obj,
        side_word=side_word,
        modifiers=mods,
    )


# ---------------------------------------------------------------------------
# Verb
# ---------------------------------------------------------------------------


def _match_verb(words: list[str], vocab: Vocabulary) -> tuple[str, str]:
    """The longest verb phrase at the start of the words, and its canonical verb."""
    for phrase in vocab.verb_phrases:
        pw = phrase.split()
        if words[: len(pw)] == pw:
            return phrase, vocab.phrase_to_verb[phrase]
    raise errors.unknown_verb(" ".join(words), vocab.verb_names)


# ---------------------------------------------------------------------------
# Object
# ---------------------------------------------------------------------------


def _side_of_word(word: str, vocab: Vocabulary) -> str | None:
    """The side word a token stands for, or None.

    'stbd' becomes 'starboard' and 'windward' becomes 'weather', but 'port'
    is kept as 'port' so the log can echo it as larboard; resolve.py turns
    it into the larboard side.
    """
    if word == "port":
        return "port"
    return vocab.sides.get(word)


def _match_object(
    ship: Ship, words: list[str], vocab: Vocabulary, verb: str, spec: VerbSpec
) -> tuple[str | None, str | None, list[str]]:
    """Find the noun phrase after the verb. Returns (phrase, side word, remaining words).

    The noun usually follows the verb at once ("set the fore topsail sharp
    up"), but modifiers may lead it ("shake out two reefs in the fore
    topsail"): leading modifier words are stepped over and handed back with
    the rest, minus a preposition that only joined them to the noun.
    """
    words = strip_article(list(words))
    table = noun_table(ship)
    leading_words = set(vocab.numbers) | set(vocab.brace_modes) | _LEADING_WORDS
    leading: list[str] = []
    start = 0
    while start <= len(words):
        found = _noun_at(table, words[start:], vocab, verb)
        if found is not None:
            phrase, side_word, rest = found
            if len(leading) >= 2 and leading[-1] in _PREPOSITIONS:
                leading.pop()
            return phrase, side_word, leading + rest
        if start < len(words) and (words[start] in leading_words or words[start].isdigit()):
            leading.append(words[start])
            start += 1
            continue
        break
    if spec.object == "yards" and (not words or _looks_like_modifiers(words, vocab)):
        return None, None, words  # "brace sharp up": every yard
    if not words:
        raise OrderError(f"{verb.capitalize()} what? {_examples(ship, spec.object)}")
    ws = _strip_side(words, vocab)[1]
    stop = _first_modifier_index(ws, vocab)
    phrase = " ".join(ws[:stop]) if stop > 0 else " ".join(ws)
    raise errors.unknown_noun(phrase, verb, table.names)


_PREPOSITIONS = ("in", "of", "from", "on")
# Words that may come between the verb and the noun ("shake out two reefs in the
# topsail", "brace in the fore yards"), besides numbers and brace modes.
_LEADING_WORDS = frozenset({"reef", "reefs", "in", "of", "from", "on", "all", "close"})


def _strip_side(words: list[str], vocab: Vocabulary) -> tuple[str | None, list[str]]:
    """A leading side word ('weather main brace'), unless it begins 'starboard tack'."""
    words = strip_article(words)
    if words and _side_of_word(words[0], vocab) and not (len(words) > 1 and words[1] == "tack"):
        return _side_of_word(words[0], vocab), strip_article(words[1:])
    return None, words


def _noun_at(
    table, words: list[str], vocab: Vocabulary, verb: str
) -> tuple[str, str | None, list[str]] | None:
    """The longest noun at the start of `words`, or None. Raises for a noun the ship lacks."""
    side_word, ws = _strip_side(words, vocab)
    if not ws:
        return None
    stop = _first_modifier_index(ws, vocab)
    for n in range(len(ws), 0, -1):
        phrase = " ".join(ws[:n])
        noun = table.lookup(phrase)
        if noun is None:
            continue
        rest = ws[n:]
        if rest and _side_of_word(rest[0], vocab) and not (len(rest) > 1 and rest[1] == "tack"):
            if side_word is not None and _side_of_word(rest[0], vocab) != side_word:
                raise OrderError(f"Two sides were given ('{side_word}' and '{rest[0]}'); say one.")
            side_word = _side_of_word(rest[0], vocab)
            rest = rest[1:]
        if rest and n < stop:
            # The noun matched short and a word that is no modifier follows:
            # "gaff topsail" on a ship with a gaff but no gaff topsail. The
            # captain meant the longer phrase, and the ship has no such part;
            # the suggestions will show the nearest names it does have.
            raise errors.unknown_noun(" ".join(ws[:stop]), verb, table.names)
        return phrase, side_word, rest
    return None


def _examples(ship: Ship, kind: str) -> str:
    from freesail.orders.resolve import display_name

    if kind == "line":
        names = [display_name(ship, i) for i in list(ship.lines)[:3]]
        return "Name a line, such as " + errors.join_names(f"the {n}" for n in names) + "."
    if kind == "yards":
        return "Name a yard or say 'the yards'."
    sails = [display_name(ship, i) for i in list(ship.sails)[:2]]
    groups = list(ship.groups)[:2]
    return (
        "Name a sail or a group of sails, such as "
        + errors.join_names([f"the {n}" for n in sails] + [f"the {g}" for g in groups])
        + "."
    )


def _modifier_words(vocab: Vocabulary) -> set[str]:
    out: set[str] = set()
    for group in (
        vocab.brace_modes,
        vocab.sides,
        vocab.numbers,
        vocab.point_directions,
    ):
        for phrase in group:
            out.update(phrase.split())
    for seq in (
        vocab.both_sides,
        vocab.manner,
        vocab.a_little,
        vocab.reef_close,
        vocab.tack_phrase,
    ):
        for phrase in seq:
            out.update(phrase.split())
    out.update({"reef", "reefs", "fathom", "fathoms", "point", "points", "to", "degrees", "tack"})
    return out


def _first_modifier_index(words: list[str], vocab: Vocabulary) -> int:
    mw = _modifier_words(vocab)
    for i, w in enumerate(words):
        if w in mw or w.isdigit():
            return i
    return len(words)


def _looks_like_modifiers(words: list[str], vocab: Vocabulary) -> bool:
    return _first_modifier_index(words, vocab) == 0


# ---------------------------------------------------------------------------
# Modifiers
# ---------------------------------------------------------------------------


def _count(word: str, vocab: Vocabulary) -> float | None:
    if word.isdigit():
        return float(word)
    try:
        if word.replace(".", "", 1).isdigit():
            return float(word)
    except ValueError:
        pass
    return vocab.numbers.get(word)


def _starts_with(words: list[str], i: int, phrase: str) -> bool:
    pw = phrase.split()
    return words[i : i + len(pw)] == pw


def _longest_at(words: list[str], i: int, phrases) -> str | None:
    best: str | None = None
    for p in phrases:
        if _starts_with(words, i, p) and (best is None or len(p.split()) > len(best.split())):
            best = p
    return best


def _parse_modifiers(
    words: list[str], vocab: Vocabulary, verb: str
) -> tuple[dict[str, Any], str | None]:
    """Read modifiers left to right. Returns (modifiers, side word or None)."""
    mods: dict[str, Any] = {}
    side: str | None = None
    unknown: list[str] = []
    i = 0
    n = len(words)
    while i < n:
        w = words[i]

        # "on the starboard tack", "starboard tack"
        tp = _longest_at(words, i, vocab.tack_phrase)
        j = i + (len(tp.split()) if tp else 0)
        if j + 1 < n and words[j + 1] == "tack" and words[j] in vocab.sides:
            t = vocab.sides[words[j]]
            if t not in ("starboard", "larboard"):
                raise OrderError(
                    f"'{words[j]} tack' is not a tack; a ship is on the starboard or the "
                    f"larboard tack."
                )
            mods["tack"] = t
            i = j + 2
            continue

        # "both sides"
        bs = _longest_at(words, i, vocab.both_sides)
        if bs:
            side = "both"
            i += len(bs.split())
            continue

        # brace modes
        bm = _longest_at(words, i, vocab.brace_modes)
        if bm and not (bm == "up" and i > 0 and words[i - 1] in ("point", "points")):
            mods["brace_mode"] = bm
            i += len(bm.split())
            continue

        # "close", "close reefed"
        rc = _longest_at(words, i, vocab.reef_close)
        if rc:
            mods["close"] = True
            i += len(rc.split())
            continue

        # "a little", manner words
        al = _longest_at(words, i, vocab.a_little)
        if al:
            mods["a_little"] = True
            i += len(al.split())
            continue
        if w in vocab.manner:
            mods["manner"] = w
            i += 1
            continue

        # counted things: "two reefs", "a fathom", "three points to starboard"
        c = _count(w, vocab)
        if c is not None and i + 1 < n:
            unit = words[i + 1]
            if unit in ("reef", "reefs"):
                mods["reefs"] = int(c)
                i += 2
                continue
            if unit in ("fathom", "fathoms"):
                mods["fathoms"] = c
                i += 2
                continue
            if unit in ("point", "points"):
                mods["points"] = c
                i += 2
                d = _longest_at(words, i, vocab.point_directions)
                if d:
                    mods["direction"] = vocab.point_directions[d]
                    i += len(d.split())
                continue
            if unit in ("degrees", "degree"):
                mods["heading"] = units.wrap_2pi(units.deg_to_rad(c))
                mods["heading_text"] = f"{c:g} degrees"
                i += 2
                continue
        if w in ("reef", "reefs") and "reefs" not in mods:
            mods["reefs"] = 1  # "reef the topsail, reef" is odd, but harmless
            i += 1
            continue

        # a heading: "to south west by west", "245", "sw by w"
        skip_to = 0
        if w in ("to", "for", "towards", "toward") and i + 1 < n:
            skip_to = 2 if words[i + 1] == "the" and i + 2 < n else 1
        h = _match_heading(words, i + skip_to, vocab)
        if h is not None:
            heading, text, used = h
            mods["heading"] = heading
            mods["heading_text"] = text
            i += skip_to + used
            continue

        # a bare number: "come up two" (but not a stray "a")
        if c is not None and w not in ("a", "an"):
            mods["points"] = c
            i += 1
            continue

        # a side word on its own (after a comma, usually)
        sw = _side_of_word(w, vocab)
        if sw:
            if side is not None and side != sw:
                raise OrderError(f"Two sides were given ('{side}' and '{sw}'); say one.")
            side = sw
            i += 1
            continue

        unknown.append(w)
        i += 1

    if unknown:
        known = sorted(
            _modifier_words(vocab) | set(vocab.phrase_to_verb) | set(units.COMPASS_NAMES)
        )
        raise errors.unknown_words(unknown, verb, known)
    return mods, side


def _match_heading(words: list[str], i: int, vocab: Vocabulary) -> tuple[float, str, int] | None:
    """A heading starting at words[i]: (radians, text as said, words used) or None."""
    if i >= len(words):
        return None
    w = words[i]
    c = _count(w, vocab)
    if c is not None and w[0].isdigit():
        used = 1
        if i + 1 < len(words) and words[i + 1] in ("degrees", "degree"):
            used = 2
        return units.wrap_2pi(units.deg_to_rad(c)), f"{c:g} degrees", used
    # compass point: try the longest run first (up to five words: "north east by north")
    for k in range(min(5, len(words) - i), 0, -1):
        phrase = " ".join(words[i : i + k])
        angle = units.parse_compass_point(phrase)
        if angle is not None:
            return angle, units.point_name(angle, full=True), k
    return None
