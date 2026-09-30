"""The grammar of an order (spec §8.1): from text to an `Order`.

    order       := verb_phrase [ object ] { modifier } [ "," side ] [ "with" [ "the" ] hands ]
                 | "send" [ "the" ] hands [ direction ] "to" order
    hands       := a watch or a station ("larboard watch", "fore topmen"; `hands_selectors`)
    object      := [ "the" ] [ side_word ] noun [ side_word ]
    modifier    := "sharp up" | "square" | "in" | "up" | "aback" | "to the wind"
                 | "on the" tack_word "tack"
                 | count "reef" | count "reefs" | "close" | "reefs"
                 | "a fathom" | count "fathoms" | "a little" | "handsomely" | "roundly"
                 | "home" | "aft"
                 | "to" heading | heading
    heading     := number ["degrees"] | compass-point
                 | count "point"/"points" ("up" | "off" | "to starboard" | "to larboard")
    count       := number | "half" ["a"] | "a half" | number "and a half"
    object      := [ "the" ] [ side_word ] noun { "and" [ "the" ] noun } [ side_word ]

How the parser reads a line:

1. It lower-cases the text, turns hyphens into spaces and drops punctuation
   other than commas and apostrophes. A hands selector ("send the larboard
   watch aloft to ...", "... with the fore topmen") is taken out first and
   carried as the modifier `hands_from`.
2. It matches the longest verb phrase at the start ("take in", "keep her
   full", "brace"), including synonyms from `vocabulary.yaml`. A phrase may
   carry a modifier in itself ("close reef", "haul aft"; `phrase_modifiers`
   in the vocabulary), which is merged with the ones said after it.
3. For a verb that takes a thing, it finds the longest run of words after
   the verb that is a noun of this ship ("fore topsail", "main brace",
   "royals"), with an optional "the" before it and an optional side word
   before or after it ("weather main brace", "main brace, starboard").
   Nouns joined by "and" make a compound object ("the topsails and
   topgallants", "the fore and main yards"; `resolve.compound_span`).
4. Everything left is modifiers, read left to right. A word that is neither
   a modifier nor part of the noun is an error naming the word and the
   nearest words that would have been understood.
5. "Take in" with a number of reefs ("take in one reef in the topsails") is
   a reef, not a taking in.

The parser does not decide what the order *means* for the ship; that is
`verbs.py`. It only produces an `Order`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from freesail import units
from freesail.orders import errors, work
from freesail.orders.errors import OrderError
from freesail.orders.resolve import compound_span, noun_table
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
      brace_mode   "sharp up" | "up" | "in" | "square" | "by the lifts" | "aback" | "to the wind"
      round        True                             "brace round" with no mode said
      tack         "starboard" | "larboard"        from "on the X tack"
      reefs        int                              "two reefs"
      close        True                             "close reefed"
      fathoms      float                            "a fathom", "two fathoms"
      a_little     True
      home         True                             "haul aft", "haul ... home"
      manner       "handsomely" | "roundly" | ...
      heading      float, radians clockwise from north (absolute)
      heading_text what was said for it, for the log
      points       float                            "two points", "half a point"
      direction    "up" | "off" | "starboard" | "larboard"
      hands_from   "starboard" | "larboard" | a station ("fore_top", "afterguard"...)
                   from "send the larboard watch aloft to ..." or "... with the fore
                   topmen": the hands the work is given to (spec M3 §5.1)
      canvas_no    int                              "bend the No. 1 fore topsail"
      heavy        True                             "shift the fore topsail for the heavy one"
      for          a sail's name                    "shift the spanker for the storm mizzen"
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
    tokens, hands_from = _take_hands_selector(norm.split(), vocab)
    norm = " ".join(tokens)
    if not norm or norm == ",":
        raise OrderError("No order given.")
    segments = [seg.split() for seg in norm.split(" , ")]
    segments = [seg for seg in segments if seg]
    if not segments:
        raise OrderError("No order given.")
    words = segments[0]

    verb_phrase, verb = _match_verb(words, vocab)
    rest = words[len(verb_phrase.split()) :]
    if verb == "belay" and verb_phrase in work.STOP_WORDS:
        # a bare "belay" or "avast", or one said of work, belays work (package 29c); said
        # of a line it is the line verb, as it always was
        verb = work.reading(ship, [*rest, *(w for seg in segments[1:] for w in seg)], vocab)
    spec = vocab.verbs[verb]
    if spec.object == "work":
        said = ", ".join(" ".join(seg) for seg in [rest, *segments[1:]] if seg)
        return Order(
            text=norm.replace(" , ", ", "),
            verb=verb,
            verb_phrase=verb_phrase,
            object=said or None,
        )
    if spec.object == "navigation":
        # what the captain says to the master (spec M5 §15, package 33a): the words after
        # the verb are a mark, a place, a position or an allowance, read by
        # `orders.navigation` as they were said (the original text, not the lower-cased
        # form: a mark's name is matched without regard to case, a position by its
        # letters)
        said = " ".join(w for w in [*rest, *(w for seg in segments[1:] for w in seg)] if w != ",")
        return Order(
            text=norm.replace(" , ", ", "),
            verb=verb,
            verb_phrase=verb_phrase,
            object=said or None,
        )
    if spec.object == "query":
        # a question of the ship's stores (package 30b): nothing more is said after it
        extra = [w for w in [*rest, *(w for seg in segments[1:] for w in seg)] if w != ","]
        if extra:
            raise OrderError(
                f"'{verb_phrase}' is a question and takes nothing after it; "
                f"'{' '.join(extra)}' was not understood."
            )
        return Order(text=norm.replace(" , ", ", "), verb=verb, verb_phrase=verb_phrase)
    if spec.level == "driver":
        raise OrderError(
            f"'{verb_phrase}' is a console command, not an order to the ship; "
            f"the ship takes orders such as 'set the topsails' or 'steer south-west'."
        )
    if spec.object == "station":
        raise OrderError(
            f"'{verb_phrase}' is said to an agent's station, and names one: ask the watcher "
            f"how the sails are drawing; stand down the watcher; show the watcher's journal."
        )
    if spec.level == "2":
        raise OrderError(
            f"'{verb_phrase}' is a sentence of the standing dialect, not a plain order: "
            f'standing order "night routine": at sunset then take in the royals.'
        )
    canvas: dict[str, Any] = {}
    if verb in CANVAS_VERBS:
        rest, canvas = _take_canvas_words(rest)

    obj: str | None = None
    side_word: str | None = None
    if spec.object in ("sail", "yards", "line", "wreck"):
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
    for k, v in vocab.phrase_modifiers.get(verb_phrase, {}).items():
        if k in mods and mods[k] != v:
            raise OrderError(
                f"'{verb_phrase}' says how already; '{_said(k, mods[k])}' contradicts it."
            )
        mods[k] = v
    if verb == "take in" and ("reefs" in mods or "close" in mods):
        verb = "reef"  # "take in one reef in the topsails" is a reef, not a taking in
    if hands_from is not None:
        mods["hands_from"] = hands_from
    mods.update(canvas)
    return Order(
        text=norm.replace(" , ", ", "),
        verb=verb,
        verb_phrase=verb_phrase,
        object=obj,
        side_word=side_word,
        modifiers=mods,
    )


# ---------------------------------------------------------------------------
# Canvas: which sail from the sail room (spec 3b §6.3)
# ---------------------------------------------------------------------------

CANVAS_VERBS = ("bend", "shift")
_CANVAS_NUMBER_WORDS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def _canvas_number(words: list[str], i: int) -> int | None:
    """'no 1', 'number 1', 'number one' at `i` (the point of "No. 1" is gone by now)."""
    if i + 1 < len(words) and words[i] in ("no", "number"):
        w = words[i + 1]
        n = int(w) if w.isdigit() else _CANVAS_NUMBER_WORDS.get(w)
        if n is not None and 1 <= n <= 9:
            return n
    return None


def _take_canvas_words(words: list[str]) -> tuple[list[str], dict[str, Any]]:
    """Take out the words that say which sail to bend (spec 3b §6.3): 'the No. 1 fore
    topsail', 'the heavy fore topsail', '... for the heavy one', '... for the No. 2', 'the
    spanker for the storm mizzen'. Returns the words left for the object and the modifiers
    `canvas_no`, `heavy` or `for` (a sail's name, which the shift script resolves)."""
    mods: dict[str, Any] = {}
    out = list(words)
    if "for" in out:
        i = out.index("for")
        after = strip_article(out[i + 1 :])
        if after[:1] in (["a"], ["an"]):
            after = after[1:]
        out = out[:i]
        if after[-1:] == ["one"] and len(after) > 1:
            after = after[:-1]  # "the heavy one", "the No. 1 one"
        number = _canvas_number(after, 0)
        if number is not None and len(after) == 2:
            mods["canvas_no"] = number
        elif after in (["heavy"], ["heavy", "weather"]):
            mods["heavy"] = True
        elif after in (["new"], ["another"], ["spare"], ["new", "spare"]):
            pass  # the best in the sail room, as with no words at all
        elif after:
            mods["for"] = " ".join(after)
        else:
            raise OrderError("For what? Name the sail to bend in its place, or say the heavy one.")
    lead = 1 if out[:1] == ["the"] else 0
    number = _canvas_number(out, lead)
    if number is not None:
        mods["canvas_no"] = number
        del out[lead : lead + 2]
    elif out[lead : lead + 1] == ["heavy"]:
        mods["heavy"] = True
        del out[lead : lead + (2 if out[lead + 1 : lead + 2] == ["weather"] else 1)]
    return out, mods


# ---------------------------------------------------------------------------
# Hands selector
# ---------------------------------------------------------------------------


def _take_hands_selector(words: list[str], vocab: Vocabulary) -> tuple[list[str], str | None]:
    """Take a hands selector out of the words (spec M3 §5.1): the words left, and the
    watch or station named ("larboard", "fore_top"), or None.

    Two forms: "send the larboard watch aloft to furl the main course" (the order is
    what follows "to") and "... with the starboard watch" anywhere after the verb,
    with the comma before it if there is one. "Meet her with the helm" is left alone:
    the helm is not a watch.
    """
    selectors = vocab.hands_selectors
    chosen: str | None = None
    said: str | None = None
    if words and words[0] == "send":
        i = 2 if len(words) > 1 and words[1] == "the" else 1
        phrase = _longest_at(words, i, selectors)
        if phrase:
            j = i + len(phrase.split())
            direction = _longest_at(words, j, vocab.send_directions)
            if direction:
                j += len(direction.split())
            if j + 1 >= len(words) or words[j] != "to":
                raise OrderError(
                    f"Send the {phrase} to do what? Say 'send the {phrase} aloft to loose the "
                    f"fore topsail', or give the order and add 'with the {phrase}'."
                )
            chosen, said = selectors[phrase], phrase
            words = words[j + 1 :]
    i = 1
    while i < len(words):
        if words[i] != "with":
            i += 1
            continue
        k = i + 2 if i + 1 < len(words) and words[i + 1] == "the" else i + 1
        phrase = _longest_at(words, k, selectors)
        if not phrase:
            i += 1
            continue
        if chosen is not None:
            raise OrderError(
                f"Two sets of hands were named (the {said} and the {phrase}); say one."
            )
        chosen, said = selectors[phrase], phrase
        start = i - 1 if words[i - 1] == "," else i
        words = words[:start] + words[k + len(phrase.split()) :]
        i = start
    while words and words[-1] == ",":
        words = words[:-1]
    return words, chosen


# ---------------------------------------------------------------------------
# Verb
# ---------------------------------------------------------------------------


def _said(key: str, value: Any) -> str:
    """The words a modifier stands for, for a sentence about it."""
    if key == "reefs":
        return f"{value:g} reef{'s' if value != 1 else ''}"
    if key == "close":
        return "close"
    if key == "home":
        return "home"
    return str(value)


def _match_verb(words: list[str], vocab: Vocabulary) -> tuple[str, str]:
    """The longest verb phrase at the start of the words, and its canonical verb."""
    keyed = [w.replace("'", "") for w in words]  # "helm's a-lee" is the phrase "helms a lee"
    for phrase in vocab.verb_phrases:
        pw = phrase.split()
        if keyed[: len(pw)] == pw:
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
    if spec.object == "wreck" and (not words or _looks_like_modifiers(words, vocab)):
        return None, None, words  # "clear the wreck": every wreck aboard
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
    span = compound_span(table, ws)
    if span is None:
        return None
    n = span[0]
    phrase = " ".join(ws[:n])  # as said; resolve() reads the compound again
    rest = ws[n:]
    if rest and _side_of_word(rest[0], vocab) and not (len(rest) > 1 and rest[1] == "tack"):
        if side_word is not None and _side_of_word(rest[0], vocab) != side_word:
            raise OrderError(f"Two sides were given ('{side_word}' and '{rest[0]}'); say one.")
        side_word = _side_of_word(rest[0], vocab)
        rest = rest[1:]
    if rest and rest[0] == "and" and len(rest) > 1:
        # "the jib and the spanker" on a ship with no spanker: the part after
        # 'and' is the one that is missing.
        after = strip_article(rest[1:])
        raise errors.unknown_noun(
            " ".join(after[: _first_modifier_index(after, vocab) or len(after)]),
            verb,
            table.names,
        )
    if rest and n < stop:
        # The noun matched short and a word that is no modifier follows:
        # "gaff topsail" on a ship with a gaff but no gaff topsail. The
        # captain meant the longer phrase, and the ship has no such part;
        # the suggestions will show the nearest names it does have.
        raise errors.unknown_noun(" ".join(ws[:stop]), verb, table.names)
    return phrase, side_word, rest


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
    for phrase in vocab.sheet_to:
        out.update(phrase.split())
    for seq in (
        vocab.both_sides,
        vocab.manner,
        vocab.a_little,
        vocab.afresh,
        vocab.reef_close,
        vocab.tack_phrase,
        vocab.haul_home,
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


def _count_at(words: list[str], i: int, vocab: Vocabulary) -> tuple[float, int] | None:
    """A count starting at words[i], with halves: (value, words used) or None.

    "two", "half a" (point), "a half" (point), "two and a half" (points).
    "A point and a half" is read by the caller after the unit.
    """
    w = words[i]
    nxt = words[i + 1] if i + 1 < len(words) else ""
    if w == "half":
        return 0.5, 2 if nxt in ("a", "an") else 1
    c = _count(w, vocab)
    if c is None:
        return None
    if w in ("a", "an") and nxt == "half":
        return 0.5, 2
    if words[i + 1 : i + 4] == ["and", "a", "half"]:
        return c + 0.5, 4
    return c, 1


def _and_a_half(words: list[str], j: int) -> int:
    """3 when 'and a half' starts at words[j], else 0."""
    return 3 if words[j : j + 3] == ["and", "a", "half"] else 0


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

        # "to windward", "to leeward": the side a sheet is hauled on (package 32e)
        st = _longest_at(words, i, vocab.sheet_to)
        if st:
            mods["sheet_to"] = vocab.sheet_to[st]
            i += len(st.split())
            continue

        # "home", "aft", "flat aft": all the way in
        hh = _longest_at(words, i, vocab.haul_home)
        if hh:
            mods["home"] = True
            i += len(hh.split())
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

        # counted things: "two reefs", "a fathom", "three points to starboard",
        # "half a point", "a point and a half"
        counted = _count_at(words, i, vocab)
        c, used = counted if counted else (None, 0)
        if c is not None and i + used < n:
            unit = words[i + used]
            if unit in ("reef", "reefs"):
                mods["reefs"] = int(c)
                i += used + 1
                continue
            if unit in ("fathom", "fathoms"):
                mods["fathoms"] = c + 0.5 * bool(_and_a_half(words, i + used + 1))
                i += used + 1 + _and_a_half(words, i + used + 1)
                continue
            if unit in ("point", "points"):
                mods["points"] = c + 0.5 * bool(_and_a_half(words, i + used + 1))
                i += used + 1 + _and_a_half(words, i + used + 1)
                d = _longest_at(words, i, vocab.point_directions)
                if d:
                    mods["direction"] = vocab.point_directions[d]
                    i += len(d.split())
                continue
            if unit in ("degrees", "degree"):
                mods["heading"] = units.wrap_2pi(units.deg_to_rad(c))
                mods["heading_text"] = f"{c:g} degrees"
                i += used + 1
                continue
        if w == "reefs" and "reefs" not in mods:
            mods["close"] = True  # "shake out the reefs": all of them
            i += 1
            continue
        if w == "reef" and "reefs" not in mods:
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

        # a bare number: "come up two", "come up half" (but not a stray "a")
        if c is not None and w not in ("a", "an"):
            mods["points"] = c
            i += used
            continue

        # a side word on its own (after a comma, usually)
        sw = _side_of_word(w, vocab)
        if sw:
            if side is not None and side != sw:
                raise OrderError(f"Two sides were given ('{side}' and '{sw}'); say one.")
            side = sw
            i += 1
            continue

        # "afresh", "anew": a line rove again (package 31b)
        if w in vocab.afresh:
            mods["afresh"] = True
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
