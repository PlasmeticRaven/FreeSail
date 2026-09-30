"""Nouns: turning "the weather main brace" into a part of this ship.

At the first order a ship receives, this module builds its *noun table*
(spec §6.5) and keeps it in `ship.extra["orders.nouns"]`. The table maps
every phrase a captain might say to the parts it names:

- every part id, as written (`fore.topsail`) and as words ("fore topsail");
- every alias and every group from the ship file;
- **generated names**: the id's words with the contractions of
  `vocabulary.yaml` applied ("fore tops'l"), and with an inner "yard"
  dropped for lines ("main brace" for `main.yard.brace.starboard`);
- **alias-derived names** for lines: if "mainsail" is an alias of
  `main.sail`, then "mainsail sheet" and "main sheet" (from the alias "the
  main") name `main.sail.sheet`, and "spanker peak halyard" names the
  peak halyard of the spanker's gaff;
- **families**: a sided part's name without its side ("main brace" names
  both main braces; the side word picks one), and the **plural** of a sided
  line's family ("main braces", "fore topsail sheets"), which means both
  sides unless a side word says otherwise;
- **shorthands**: the tail of an id ("topsail" for every `*.topsail`),
  which is unambiguous on a schooner with one topsail and rejected with the
  candidates on a frigate with three; a plural shorthand ("topsail sheets")
  names all of them;
- an alias that points at a group of exactly one starboard and one larboard
  line ("main sheet" for the main course's sheets) is entered as a family,
  so that it asks for its side like any other sided line.

Compound objects join nouns with "and": "the topsails and topgallants", "the
jib and the spanker", and, distributed, "the fore and main yards" (the fore
yards and the main yards). `compound_span` reads them; the grammar and
`resolve` both use it so that they agree on where the object ends.

Sides: `starboard`, `larboard` (`port` is accepted and echoed as larboard),
`weather` and `lee`, which resolve from the ship's current tack at the
moment the order is parsed, and `both sides`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from itertools import product

from freesail.orders import errors
from freesail.orders.vocabulary import Vocabulary, key, load_vocabulary, strip_article
from freesail.ship.graph import Ship
from freesail.ship.parts import Line, Part, Sail, Spar

SIDE_WORDS = ("starboard", "larboard")

# Precedence when one phrase is generated more than once: higher wins.
_EXPLICIT = 3  # a part id, an alias, a group name from the ship file
_GENERATED = 2  # a generated full name, an alias-derived name, or a sided family
_SHORTHAND = 1  # the tail of an id; may collect several parts

_MAX_VARIANTS = 96  # cap on contraction combinations per name, to keep the table small

# Shorthand tails beginning with these words are matched but never suggested
# ("yard brace", "sail sheet" are not how anyone speaks).
_GENERIC_TAIL_WORDS = frozenset({"yard", "sail", "mast", "gaff", "boom", "stay"})


@dataclass
class Noun:
    """What a phrase names: one or more part ids and how the phrase matched."""

    ids: list[str]
    kind: str  # "part" | "group" | "family" | "shorthand"
    name: str  # what to call the match in a sentence: "main brace", "topsails"
    rank: int = _GENERATED
    plural: bool = False  # "main braces": both sides unless a side word says otherwise


@dataclass
class NounTable:
    entries: dict[str, Noun] = field(default_factory=dict)
    _names: list[str] = field(default_factory=list)  # candidates for spelling suggestions

    def lookup(self, phrase: str) -> Noun | None:
        return self.entries.get(key(phrase))

    def add(self, phrase: str, noun: Noun, suggest: bool = True) -> None:
        """Enter a phrase. `suggest` says whether it may be offered as a spelling hint.

        Contracted spellings ("fore tops'l") and raw ids ("fore.topsail") are
        matched but not suggested; the plain words are the better hint.
        """
        k = key(phrase)
        if not k:
            return
        existing = self.entries.get(k)
        if existing is None:
            self.entries[k] = noun
            if suggest and phrase not in self._names:
                self._names.append(phrase)
            return
        if noun.rank > existing.rank:
            self.entries[k] = noun
        elif noun.rank == existing.rank:
            # Two different parts generated the same phrase: it is now ambiguous.
            merged = [i for i in existing.ids] + [i for i in noun.ids if i not in existing.ids]
            if merged != existing.ids:
                kind = existing.kind if existing.kind == noun.kind else "shorthand"
                plural = existing.plural and noun.plural
                self.entries[k] = Noun(merged, kind, existing.name, existing.rank, plural)

    @property
    def names(self) -> list[str]:
        """Phrases worth suggesting: full names, and shorthands that name one thing."""
        out: list[str] = []
        for phrase in self._names:
            noun = self.entries.get(key(phrase))
            if noun is None:
                continue
            if noun.kind == "shorthand":
                words = phrase.split()
                if len(noun.ids) != 1 or len(words) < 2 or words[0] in _GENERIC_TAIL_WORDS:
                    continue
            out.append(phrase)
        return out


@dataclass
class Resolution:
    """The outcome of resolving an object phrase: the parts, and the side that was meant."""

    ids: list[str]
    kind: str
    name: str
    side: str | None  # "starboard" | "larboard" | "both" | None, after weather/lee resolution
    side_word: str | None  # the word the captain used ("weather", "port"), for the log


# ---------------------------------------------------------------------------
# Words of a part id
# ---------------------------------------------------------------------------


def id_segments(part_id: str) -> list[str]:
    """`fore.topmast_staysail` -> ['fore', 'topmast_staysail'] (dots split, underscores kept)."""
    return part_id.split(".")


def segment_words(segment: str) -> list[str]:
    return [w for w in segment.replace("_", " ").split() if w]


def words_of(segments: list[str]) -> list[str]:
    return [w for s in segments for w in segment_words(s)]


def part_side(ship: Ship, part_id: str) -> str | None:
    """The side a part belongs to: its own `side`, or a side word in its id.

    A studding sail's halyard has no `side` of its own, but its id
    (`fore.topmast.studdingsail.starboard.halyard`) says which sail it serves.
    """
    part = ship.parts[part_id]
    side = getattr(part, "side", None)
    if side:
        return side
    for seg in id_segments(part_id):
        if seg in SIDE_WORDS:
            return seg
    return None


def base_segments(part_id: str) -> list[str]:
    """The id's segments with any side segment removed."""
    return [s for s in id_segments(part_id) if s not in SIDE_WORDS]


def _drop_inner(segments: list[str], vocab: Vocabulary) -> list[str]:
    """Drop droppable words ('yard') unless last: main.yard.brace -> main brace."""
    n = len(segments)
    return [s for i, s in enumerate(segments) if i == n - 1 or s not in vocab.droppable_inner_words]


def _family_words(ship: Ship, part_id: str, vocab: Vocabulary) -> list[str]:
    segs = base_segments(part_id)
    if isinstance(ship.parts[part_id], Line) and len(segs) > 1:
        segs = _drop_inner(segs, vocab)
    return words_of(segs)


def display_name(ship: Ship, part_id: str) -> str:
    """The name a part is called by in the log: 'starboard main brace', 'fore topsail'.

    Without the article; callers add 'the'. Group names are returned as given.
    """
    if part_id not in ship.parts:
        return part_id.replace(".", " ").replace("_", " ")
    side = part_side(ship, part_id)
    name = " ".join(_family_words(ship, part_id, load_vocabulary()))
    return f"{side} {name}" if side else name


def family_name(ship: Ship, part_id: str) -> str:
    """The display name without the side: 'main brace' for either main brace."""
    return " ".join(_family_words(ship, part_id, load_vocabulary()))


# ---------------------------------------------------------------------------
# Building the table
# ---------------------------------------------------------------------------


def _variants(words: list[str], vocab: Vocabulary) -> list[str]:
    """Every spelling of a word list under the contraction rules, the plain one first."""
    choices: list[list[str]] = []
    for w in words:
        alts = [w] + [a for a in vocab.contractions.get(w, ()) if a != w]
        choices.append(alts)
    out: list[str] = []
    for combo in product(*choices):
        out.append(" ".join(combo))
        if len(out) >= _MAX_VARIANTS:
            break
    return out


def _side_spellings(side: str) -> tuple[str, ...]:
    return ("larboard", "port") if side == "larboard" else ("starboard",)


def pluralise(phrase: str) -> str:
    """'main brace' -> 'main braces'; a word already plural is left alone."""
    words = phrase.split()
    if not words or words[-1].endswith("s"):
        return phrase
    return " ".join(words[:-1] + [words[-1] + "s"])


def singularise(phrase: str) -> str | None:
    """'main yards' -> 'main yard', or None when the last word is not plural."""
    words = phrase.split()
    if not words or not words[-1].endswith("s") or len(words[-1]) < 3:
        return None
    return " ".join(words[:-1] + [words[-1][:-1]])


def _enter(
    table: NounTable,
    ship: Ship,
    part_id: str,
    words: list[str],
    vocab: Vocabulary,
    rank: int = _GENERATED,
    kind: str = "part",
) -> None:
    """Enter one word-list name for a part, in every spelling, with its side forms.

    A sided part gets "starboard <name>" and "<name> starboard" as exact
    names and "<name>" as a family (both sides, to be picked by a side
    word). `kind` is "part" for a full name or "shorthand" for a tail.
    """
    side = part_side(ship, part_id)
    fam = " ".join(_family_words(ship, part_id, vocab))
    shown = f"{side} {fam}" if side else fam
    # A sided line's names take a plural that means both sides: "main braces".
    plural_line = side is not None and isinstance(ship.parts[part_id], Line)
    for v, phrase in enumerate(_variants(words, vocab)):
        plain = v == 0
        if kind == "shorthand":
            table.add(phrase, Noun([part_id], "shorthand", " ".join(words), rank), suggest=plain)
            if plural_line:
                many = pluralise(" ".join(words))
                table.add(pluralise(phrase), Noun([part_id], "shorthand", many, rank, True), False)
            continue
        if side:
            for sw in _side_spellings(side):
                table.add(
                    f"{sw} {phrase}", Noun([part_id], "part", shown, rank), plain and sw == side
                )
                table.add(f"{phrase} {sw}", Noun([part_id], "part", shown, rank), suggest=False)
            table.add(phrase, Noun([part_id], "family", fam, rank), suggest=plain)
            if plural_line:
                table.add(
                    pluralise(phrase), Noun([part_id], "family", pluralise(fam), rank, True), False
                )
        else:
            table.add(phrase, Noun([part_id], "part", fam, rank), suggest=plain)


def build_noun_table(ship: Ship, vocab: Vocabulary | None = None) -> NounTable:
    """Build the noun table for a ship. Cheap; done once per ship and cached."""
    vocab = vocab or load_vocabulary()
    table = NounTable()

    # 1. Part ids, generated full names, families, shorthands.
    for part_id, part in ship.parts.items():
        side = part_side(ship, part_id)
        fam = " ".join(_family_words(ship, part_id, vocab))
        table.add(
            part_id, Noun([part_id], "part", f"{side} {fam}" if side else fam, _EXPLICIT), False
        )
        segs = base_segments(part_id)
        _enter(table, ship, part_id, words_of(segs), vocab)
        if isinstance(part, Line) and _drop_inner(segs, vocab) != segs:
            _enter(table, ship, part_id, words_of(_drop_inner(segs, vocab)), vocab)
        for k in range(1, len(segs)):
            tail = segs[-k:]
            _enter(table, ship, part_id, words_of(tail), vocab, _SHORTHAND, "shorthand")
            if isinstance(part, Line) and _drop_inner(tail, vocab) != tail:
                _enter(
                    table,
                    ship,
                    part_id,
                    words_of(_drop_inner(tail, vocab)),
                    vocab,
                    _SHORTHAND,
                    "shorthand",
                )

    # 2. Groups and aliases from the ship file (explicit: they win).
    for gname, members in ship.groups.items():
        words = strip_article(key(gname).split())
        for v, phrase in enumerate(_variants(words, vocab)):
            table.add(phrase, Noun(list(members), "group", " ".join(words), _EXPLICIT), v == 0)
    for aname, target in ship.aliases.items():
        words = strip_article(key(aname).split())
        shown = " ".join(words)
        pair = _sided_pair(ship, target)
        if pair is not None:
            # "main sheet" for the main course's two sheets: a family, asking
            # for its side; "starboard main sheet" and "main sheets" follow.
            for v, phrase in enumerate(_variants(words, vocab)):
                table.add(phrase, Noun(list(pair.values()), "family", shown, _EXPLICIT), v == 0)
                many = Noun(list(pair.values()), "family", pluralise(shown), _EXPLICIT, True)
                table.add(pluralise(phrase), many)
                for side, pid in pair.items():
                    part_noun = Noun([pid], "part", f"{side} {shown}", _EXPLICIT)
                    for sw in _side_spellings(side):
                        table.add(f"{sw} {phrase}", part_noun, suggest=False)
                        table.add(f"{phrase} {sw}", part_noun, suggest=False)
            continue
        if target in ship.groups:
            noun = Noun(list(ship.groups[target]), "group", shown, _EXPLICIT)
        else:
            side = part_side(ship, target)
            fam = " ".join(_family_words(ship, target, vocab))
            noun = Noun([target], "part", f"{side} {fam}" if side else fam, _EXPLICIT)
        for v, phrase in enumerate(_variants(words, vocab)):
            table.add(phrase, noun, v == 0)
        # 3. Lines of an aliased part take the alias too: "mainsail sheet", "main sheet".
        if target in ship.parts:
            for line_id, tail in _lines_under(ship, target):
                _enter(table, ship, line_id, words + words_of(tail), vocab)
    return table


def _sided_pair(ship: Ship, group: str) -> dict[str, str] | None:
    """{'starboard': id, 'larboard': id} when a group is one line each side of a family."""
    members = ship.groups.get(group)
    if not members or len(members) != 2:
        return None
    pair: dict[str, str] = {}
    for pid in members:
        part = ship.parts.get(pid)
        side = part_side(ship, pid) if part is not None else None
        if not isinstance(part, Line) or side is None or side in pair:
            return None
        pair[side] = pid
    if len(pair) != 2 or len({family_name(ship, i) for i in pair.values()}) != 1:
        return None
    return pair


def compound_span(table: NounTable, words: list[str]) -> tuple[int, list[str]] | None:
    """The nouns at the start of `words`, joined by 'and': (words used, the phrases).

    The longest single noun is taken first; if 'and' follows, another noun
    is read after it ("topsails and topgallants", "the jib and the
    spanker"). When no noun starts the words, the part before the first
    'and' is distributed over the part after it: "fore and main yards" is
    the fore yards and the main yards, "fore and main topsails" the fore
    topsail and the main topsail. On the right-hand side a plural is also
    tried in the singular ("main topsails" for "main topsail"). Returns None
    when no noun is found at all.
    """
    for n in range(len(words), 0, -1):
        phrase = " ".join(words[:n])
        if table.lookup(phrase) is None:
            continue
        used, phrases = n, [phrase]
        more = _after_and(table, words[n:])
        if more is not None:
            used += more[0]
            phrases += more[1]
        return used, phrases
    # distribution: "fore and main yards"
    if "and" not in words[1:]:
        return None
    i = words.index("and", 1)
    left = words[:i]
    tail = strip_article(words[i + 1 :])
    right = _right_side(table, tail)
    if right is None:
        return None
    r_used, r_phrases = right
    r_words = r_phrases[0].split()
    for k in range(1, len(r_words)):
        cand = " ".join(left + r_words[-k:])
        if table.lookup(cand) is not None:
            used = i + 1 + (len(words) - i - 1 - len(tail)) + r_used
            return used, [cand] + r_phrases
    return None


def _after_and(table: NounTable, rest: list[str]) -> tuple[int, list[str]] | None:
    """A further noun after a leading 'and', with the words consumed including it."""
    if len(rest) < 2 or rest[0] != "and":
        return None
    tail = strip_article(rest[1:])
    more = _right_side(table, tail)
    if more is None:
        return None
    return 1 + (len(rest) - 1 - len(tail)) + more[0], more[1]


def _right_side(table: NounTable, words: list[str]) -> tuple[int, list[str]] | None:
    """A noun (or chain) at the start of words, trying a plural in the singular too."""
    for n in range(len(words), 0, -1):
        phrase = " ".join(words[:n])
        singular = singularise(phrase)
        found = phrase if table.lookup(phrase) is not None else None
        if found is None and singular is not None and table.lookup(singular) is not None:
            found = singular
        if found is None:
            continue
        used, phrases = n, [found]
        more = _after_and(table, words[n:])
        if more is not None:
            used += more[0]
            phrases += more[1]
        return used, phrases
    return None


def _lines_under(ship: Ship, part_id: str) -> list[tuple[str, list[str]]]:
    """(line id, tail segments) for each line of a part, and of a sail's yard, gaff or boom.

    The tail is the line's id after the part it belongs to, with any side
    removed: for `main.yard.brace.starboard` under `main.yard` it is ['brace'].
    """
    part = ship.parts[part_id]
    owners: list[str] = [part_id]
    if isinstance(part, Sail):
        for role in ("yard", "gaff", "boom"):
            spar = ship.spar_of_role(part, role)
            if spar is not None:
                owners.append(spar.id)
    out: list[tuple[str, list[str]]] = []
    for owner in owners:
        for ln in ship.lines_of(owner):
            if ln.is_standing:
                continue
            tail = [s for s in id_segments(ln.id) if s not in SIDE_WORDS]
            prefix = id_segments(owner)
            if tail[: len(prefix)] == prefix:
                tail = tail[len(prefix) :]
            else:
                tail = [ln.cls]
            out.append((ln.id, tail))
    return out


def noun_table(ship: Ship) -> NounTable:
    """This ship's noun table, built on first use and kept in `ship.extra`."""
    table = ship.extra.get("orders.nouns")
    if table is None:
        table = build_noun_table(ship)
        ship.extra["orders.nouns"] = table
    return table


# ---------------------------------------------------------------------------
# Sides
# ---------------------------------------------------------------------------


def other_side(side: str) -> str:
    return "larboard" if side == "starboard" else "starboard"


def resolve_side(ship: Ship, word: str | None) -> str | None:
    """'weather' and 'lee' become starboard or larboard from the current tack; 'port' larboard."""
    if word is None:
        return None
    if word == "both":
        return "both"
    if word == "weather":
        return ship.dyn.tack
    if word == "lee":
        return other_side(ship.dyn.tack)
    if word == "port":
        return "larboard"
    return word


def side_phrase(side: str | None, side_word: str | None) -> str:
    """How the log names a resolved side: 'starboard (weather)' when weather was said."""
    if side is None or side == "both":
        return ""
    if side_word in ("weather", "lee"):
        return f"{side} ({side_word})"
    return side


# ---------------------------------------------------------------------------
# Resolving an object phrase
# ---------------------------------------------------------------------------


def resolve(ship: Ship, phrase: str, side_word: str | None, verb: str) -> Resolution:
    """Turn an object phrase and an optional side word into part ids.

    Raises OrderError when the phrase names nothing (with the nearest names),
    when it could name several things (with the candidates), or when a side
    is given for a thing that has none.
    """
    table = noun_table(ship)
    noun = table.lookup(phrase)
    if noun is None:
        words = phrase.split()
        span = compound_span(table, words) if "and" in words else None
        if span is None or span[0] != len(words):
            raise errors.unknown_noun(phrase, verb, table.names)
        return _resolve_compound(ship, phrase, span[1], side_word, verb)
    side = resolve_side(ship, side_word)
    ids = list(noun.ids)
    sided = [i for i in ids if part_side(ship, i)]
    if side is None and noun.plural and len(sided) > 1:
        side = "both"  # "the main braces": both, unless a side word says which

    if side is not None:
        if not sided:
            raise errors.OrderError(
                f"The {noun.name} has no {side_word} side; "
                f"sides belong to braces, sheets, studding sails and the like."
            )
        if side == "both":
            return Resolution(ids, noun.kind, noun.name, side, side_word)
        # Keep the parts on that side. Members of a group with no side of
        # their own ("set all sail, starboard") are kept too.
        kept = [i for i in ids if part_side(ship, i) in (None, side)]
        if not any(part_side(ship, i) == side for i in kept):
            have = part_side(ship, sided[0])
            raise errors.OrderError(
                f"The {noun.name} is on the {have} side, not the {side}"
                f"{'' if side == side_word else f' ({side_word})'}."
            )
        return Resolution(kept, noun.kind, noun.name, side, side_word)

    if noun.kind == "family" and len(ids) > 1:
        if _fore_and_aft_sheets(ship, ids):
            # "haul the jib sheet" (package 32e): a fore-and-aft sail's pair of sheets named
            # without a side means the working one (the lee sheet; "to windward" the
            # weather); the verb picks it (orders/verbs.py, `_pick_sheets`)
            return Resolution(ids, noun.kind, noun.name, None, None)
        raise errors.OrderError(
            f"Which {noun.name}: the starboard, the larboard (the weather or the lee), "
            f"or both sides? ('{verb}' was understood.)"
        )
    if noun.kind == "shorthand" and len(ids) > 1:
        families: list[str] = []
        for i in ids:
            fam = family_name(ship, i)
            if fam not in families:
                families.append(fam)
        if len(families) == 1:
            raise errors.OrderError(
                f"Which {families[0]}: the starboard, the larboard (the weather or the lee), "
                f"or both sides? ('{verb}' was understood.)"
            )
        raise errors.ambiguous_noun(" ".join(phrase.split()), families, verb)
    return Resolution(ids, noun.kind, noun.name, None, None)


def _fore_and_aft_sheets(ship: Ship, ids: list[str]) -> bool:
    """True when the ids are the two sheets of one fore-and-aft sail."""
    sails: set[str] = set()
    for pid in ids:
        part = ship.parts.get(pid)
        if not isinstance(part, Line) or part.cls != "sheet":
            return False
        sail = ship.parts.get(part.of)
        if not isinstance(sail, Sail) or not sail.is_fore_and_aft:
            return False
        sails.add(sail.id)
    return len(sails) == 1


def _resolve_compound(
    ship: Ship, phrase: str, phrases: list[str], side_word: str | None, verb: str
) -> Resolution:
    """'the topsails and topgallants': each noun resolved on its own, the parts joined."""
    ids: list[str] = []
    names: list[str] = []
    side: str | None = None
    for p in phrases:
        res = resolve(ship, p, side_word, verb)
        ids.extend(i for i in res.ids if i not in ids)
        names.append(res.name)
        side = side or res.side
    kind = "group" if len(ids) > 1 else "part"
    return Resolution(ids, kind, errors.join_names(names, "and", limit=len(names)), side, side_word)


# ---------------------------------------------------------------------------
# Small queries the verbs use
# ---------------------------------------------------------------------------


def kind_of(part: Part) -> str:
    """'sail', 'yard', 'spar' or 'line', for sentences."""
    if isinstance(part, Sail):
        return "sail"
    if isinstance(part, Spar):
        return "yard" if part.is_yard else part.cls.replace("_", " ")
    if isinstance(part, Line):
        return "standing rigging" if part.is_standing else "line"
    return "part"


def the(ship: Ship, part_id: str) -> str:
    """'the fore topsail', for sentences."""
    return "the " + display_name(ship, part_id)
