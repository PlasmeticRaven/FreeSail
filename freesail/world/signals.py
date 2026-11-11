"""Colours, the signal books, a signal hoisted and read, and the private signal (spec M7
§1 to §3; package 71; `docs/design/Design-Signals.md`).

**The books** (`Books`, `load_books`): one root a directory under `data/signals/`, the same
six files in each (`book.yaml` the declaration and the flags' figures, `numerary.yaml` the
day signals, `telegraphic.yaml` the dictionary, `night_fog.yaml`, `convoy.yaml`,
`private.yaml` the private table's form); a nation names its root and its system in
`data/nations.yaml` (`signals: {root, system}`), and `basic` is the foundation every nation
stands on. An entry maps to what a rules captain under the sender's orders does (`does`).

**Colours** (`Colours`) are a state of every body: `shown` (her own), `none`, `false`
(another nation's, the ruse the law allowed until the first shot), `struck`, `distress`
(the ensign union down); the lookout gives the nation *shown*, never the true one.

**A signal is a thing hoisted** (`Hoist`): the book, the numbers or the thing shown, the
meaning, by whom, since when, hauled down when, answered by whom; it breaks out at the end
of its hoist's minute and flies on the sender's body, where every lookout near enough with
light enough sees it (`read_flying`), reads it a minute later if the ship's library holds
that book, and a rules captain answers it and, when the sender commands him
(`under_orders_of`), acts on it (`obey`).

**The private signal** (`private_table`): a small table per nation per month drawn under
the seed from the root's form; the challenge and the reply are hoists of the `private`
book, the reply judged by the challenger against his table (`judge_private`).

The per-ship state is a `Locker` (`ship.extra["signals"]` on a near body; the far `Vessel`
carries the same objects, so that a crewed ship and her far body are one): the colours, the
hoists flying and made, the lights, the fog signals kept, what has been seen and read, and
the private challenges awaiting their answer.
"""

from __future__ import annotations

import math
import random
import re
import zlib
from dataclasses import dataclass, field
from functools import cache
from pathlib import Path
from typing import Any

import yaml

from freesail import units

__all__ = [
    "BOOK_FILES",
    "COLOURS_STATES",
    "LIGHT_SEEN_NM",
    "SIGNALS_DIR",
    "Books",
    "Colours",
    "Entry",
    "Hoist",
    "Locker",
    "PrivateTable",
    "books_for",
    "books_for_nation",
    "colours_of",
    "flying_of",
    "load_books",
    "locker_of",
    "private_table",
    "read_flying",
]

SIGNALS_DIR = Path(__file__).resolve().parents[2] / "data" / "signals"
BOOK_FILES = ("book", "numerary", "telegraphic", "night_fog", "convoy", "private")

COLOURS_STATES = ("shown", "none", "false", "struck", "distress", "truce")

# The book a signal is made from by the light: the numerary by day, the night book by
# night, the fog book when the visibility is under a mile (the flags are not to be seen).
BOOKS_BY_LIGHT = {"day": "numerary", "night": "night", "fog": "fog"}

# A light seen at night: a lantern on a clear night at three miles (judgement after the
# period's lights: a stern lantern was made out at a league in clear weather), within the
# visibility; the hull's loom is the mile the lookout has (`lookout.GLASS_NIGHT_NM`).
LIGHT_SEEN_NM = 3.0
# A gun heard in fog, and a bell (judgement: a gun carries three miles in still air, a
# ship's bell a mile).
GUN_HEARD_NM = 3.0
BELL_HEARD_NM = 1.0
# The ships in succession perform the order this long after the one before them has (the
# time a ship takes to go about; judgement, said in the tuning notes).
SUCCESSION_GAP_S = 180
# A hoist bent on but not yet run up (the hands at other work): it breaks out when the
# evolution begins (`MakeSignalScript.begin`), and never of itself.
NOT_YET = 10**12

_ROLES_WITH_TABLE = ("kings-ship", "cruiser", "commodore")


# ---------------------------------------------------------------------------
# The books
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Entry:
    """One signal of a book: its number (the numerary's and the convoy's), its meaning and
    the other words that mean it, what a commanded captain does, its qualifiers, whether
    the ships under orders perform it one after another, the thing shown or fired (the
    night and fog books), and where it comes from."""

    book: str  # numerary | night | fog | convoy
    number: int | None
    meaning: str
    also: tuple[str, ...]
    does: dict[str, Any]
    qualifiers: tuple[str, ...] = ()
    in_succession: bool = False
    show: str = ""  # the night book: the lights, false fires and rockets shown
    fire: str = ""  # the fog book: the guns, muskets, bell and drum fired
    source: str = ""
    made: bool = False
    original: str = ""  # the nation's own phrase, where known

    @property
    def words(self) -> tuple[str, ...]:
        return (self.meaning.lower(), *(w.lower() for w in self.also))


@dataclass
class PrivateTable:
    nation: str
    year: int
    month: int
    day_challenge: str
    day_reply: str
    night_challenge: str
    night_reply: str
    adjective: str = ""  # the nation's word for the page ('British'); the id when unset

    def challenge(self, light: str) -> str:
        return self.night_challenge if light == "night" else self.day_challenge

    def reply(self, light: str) -> str:
        return self.night_reply if light == "night" else self.day_reply

    def lines(self) -> list[str]:
        when = f"{_MONTHS[self.month - 1]} {self.year}"
        return [
            f"The private signals for {when}, to be made to every strange sail and answered by "
            f"every ship of the {self.adjective or self.nation} service; good until the month "
            "turns.",
            f"By day: the challenge, {self.day_challenge}; the reply, {self.day_reply}.",
            f"By night: the challenge, {self.night_challenge}; the reply, {self.night_reply}.",
        ]


_MONTHS = (
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
)


class BookFileError(ValueError):
    """A signal book the loader cannot accept. The message is a sentence."""


@dataclass
class Books:
    """A nation's signal books, from one root."""

    root: str
    nation: str
    system: str
    sources: list[str]
    flags: dict[str, Any]
    hoist_s: int
    read_s: int
    read_nm: float
    glass_factor: float
    flies_s: int
    numerary: list[Entry]
    night: list[Entry]
    fog: list[Entry]
    convoy: list[Entry]
    words: dict[int, str]  # the telegraphic dictionary, number to word
    alphabet: dict[str, int]
    telegraph: bool
    private_form: dict[str, Any]
    carried_by: tuple[str, ...]
    answer_wait_s: int
    # the dictionary's words by every form its printed entries give ('Expect-ed-ing-ation':
    # expect, expected, expecting, expectation), to the entry's number (package 76)
    forms: dict[str, int] = field(default_factory=dict)
    # how a numbered signal is hoisted (package 76): 'numerary', a flag a figure (the British
    # book: No. 245 three flags), or 'table', two flags, the upper and the lower, read as a
    # cell of a square table whatever its number (du Pavillon's, Mazarredo's)
    hoist_form: str = "numerary"

    # -- finding an entry --------------------------------------------------------------

    def book(self, name: str) -> list[Entry]:
        return {
            "numerary": self.numerary,
            "night": self.night,
            "fog": self.fog,
            "convoy": self.convoy,
        }[name]

    def by_number(self, number: int, book: str = "numerary") -> Entry | None:
        for e in self.book(book):
            if e.number == number:
                return e
        return None

    def find(self, words: str, book: str = "numerary") -> tuple[Entry, dict[str, Any]] | None:
        """The entry the words mean, longest match first, and the qualifiers read from
        the words after the match ('enemy in sight bearing NW': the compass; 'No. 3 to
        chase': a ship; a number); None when no entry answers."""
        said = _norm(words)
        if not said:
            return None
        m = re.match(r"^(?:no\.?|number)\s*(\d+)$", said)
        if m is not None:
            e = self.by_number(int(m.group(1)), book)
            return (e, {}) if e is not None else None
        best: tuple[Entry, str, str] | None = None
        for e in self.book(book):
            for w in e.words:
                if said == w or said.startswith(w + " "):
                    if best is None or len(w) > len(best[1]):
                        best = (e, w, said[len(w) :].strip())
        if best is None:
            return None
        entry, _, rest = best
        return entry, _qualifiers(rest, entry.qualifiers)

    # -- the telegraphic sentence ------------------------------------------------------

    def encode(self, sentence: str) -> list[tuple[int, str]]:
        """Popham's: the sentence as hoists, a word of the dictionary a hoist, a word it
        lacks spelt letter by letter; raises BookFileError when the book has no
        dictionary."""
        if not self.telegraph or not self.words:
            raise BookFileError(
                f"the {self.nation} book has no telegraphic dictionary; a signal is made by its "
                "meaning from the numerary ('make the signal to chase')"
            )
        by_word = self.forms or word_forms(self.words)
        out: list[tuple[int, str]] = []
        for raw in re.findall(r"[A-Za-z']+", sentence):
            w = raw.lower().replace("'", "")
            if w in by_word:
                out.append((by_word[w], raw))
                continue
            for ch in raw.upper():
                letter = "I" if ch == "J" else ch
                n = self.alphabet.get(letter)
                if n is not None:
                    out.append((n, ch))
        return out

    # -- the private table ---------------------------------------------------------------

    def private_table(self, nation: str, year: int, month: int, seed: int) -> PrivateTable:
        return private_table(self, nation, year, month, seed)

    def table_carried_by(self, role: str) -> bool:
        return str(role or "") in self.carried_by


def _norm(words: str) -> str:
    s = " ".join(str(words or "").lower().replace("’", "'").split())
    s = s.strip(" .,:;!")
    for lead in ("the signal to ", "the signal for ", "the signal ", "to ", "for "):
        if s.startswith(lead) and len(s) > len(lead):
            s = s[len(lead) :]
            break
    return s.strip(" :,")


def _entry_forms(entry: str) -> tuple[list[str], list[str]]:
    """A printed entry of Popham's vocabulary as its words: the heads (each word before a
    hyphen, the alternatives a comma parts: 'Man, men') and the forms its endings make
    ('Expect-ed-ing-ation': expected, expecting, expectation; 'Ever-y-thing-where': every,
    everything, everywhere; 'Copy-ies-ied-ing': copies, copied, copying). The endings are
    the book's; the joining by the common rules (a final e dropped before a vowel, a final y
    turned to i) is the loader's. A head stands for its number and person too ('expects' is
    Expect's hoist, 269 on 21 October 1805): Popham, p. 7, "In verbs, the number, person,
    tense, and mood, must be applied to the sense of the sentence"."""
    heads: list[str] = []
    forms: list[str] = []
    for alt in str(entry).split(","):
        parts = [p.strip().lower().replace("'", "") for p in alt.strip().split("-")]
        parts = [p for p in parts if p and p.isalpha()]
        if not parts:
            continue
        base = parts[0]
        heads.append(base)
        plural_y = base.endswith("y") and base[-2:-1] not in "aeiou"
        forms.append(base[:-1] + "ies" if plural_y else base + "s")
        if base.endswith(("s", "sh", "ch", "x", "o")):
            forms.append(base + "es")
        prev = base
        for end in parts[1:]:
            made = []
            for stem in dict.fromkeys((base, prev)):
                if stem.endswith("e") and end[0] in "aeiou":
                    made.append(stem[:-1] + end)
                if stem.endswith("y") and end[0] == "i":
                    made.append(stem[:-1] + end)
                made.append(stem + end)
            forms.extend(made)
            if len(end) <= 2 and end in ("y", "s", "d", "r", "n", "t", "ly", "al"):
                prev = made[-1]
    return heads, forms


def word_forms(words: dict[int, str]) -> dict[str, int]:
    """Every word the dictionary's entries give, to its number: the heads first, then the
    forms the endings make where no head has the word already."""
    out: dict[str, int] = {}
    derived: list[tuple[str, int]] = []
    for n in sorted(words):
        heads, forms = _entry_forms(words[n])
        for h in heads:
            out.setdefault(h, n)
        derived.extend((f, n) for f in forms)
    for f, n in derived:
        out.setdefault(f, n)
    return out


_COMPASS = re.compile(
    r"\b(?:bearing\s+|to\s+the\s+|in\s+the\s+direction\s+)?"
    r"((?:north|south|east|west|n|s|e|w)(?:[ -]?(?:north|south|east|west|n|s|e|w)){0,2}"
    r"(?:\s*by\s*(?:north|south|east|west|n|s|e|w))?(?:\s*(?:ward|wards))?)\b"
)


def _qualifiers(rest: str, wanted: tuple[str, ...]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    rest = rest.strip(" :,")
    if not rest:
        return out
    if "compass" in wanted:
        m = _COMPASS.search(rest)
        if m is not None:
            try:
                rad = units.parse_course(m.group(1).replace("ward", "").strip())
                out["compass"] = units.point_name(rad)
                out["compass_deg"] = round(units.rad_to_deg(rad) % 360.0, 1)
            except Exception:  # noqa: BLE001 - not a course after all
                pass
    if "number" in wanted:
        m = re.search(r"\b(\d+)\b", rest)
        if m is not None:
            out["number"] = int(m.group(1))
    if "ship" in wanted:
        m = re.search(r"(?:no\.?\s*|number\s*)(\d+)|\bthe\s+([A-Z][\w'-]+)", rest)
        if m is not None:
            out["ship"] = m.group(1) or m.group(2)
    if "place" in wanted:
        m = re.search(r"(?:at|for|to|off)\s+(.+)$", rest)
        out["place"] = (m.group(1) if m else rest).strip()
    if not out:
        out["words"] = rest
    return out


def _entries(raw: Any, book: str, path: Path) -> list[Entry]:
    out: list[Entry] = []
    for i, d in enumerate(raw or []):
        if not isinstance(d, dict) or not d.get("meaning"):
            raise BookFileError(f"{path}: entry {i + 1} of {book} wants a meaning")
        does = d.get("does") or {}
        if not isinstance(does, dict):
            raise BookFileError(f"{path}: entry {i + 1} of {book}: `does` is a mapping")
        out.append(
            Entry(
                book=book,
                number=int(d["number"]) if d.get("number") is not None else None,
                meaning=str(d["meaning"]),
                also=tuple(str(x) for x in (d.get("also") or [])),
                does=dict(does),
                qualifiers=tuple(str(x) for x in (d.get("qualifiers") or [])),
                in_succession=bool(d.get("in_succession", False)),
                show=str(d.get("show") or ""),
                fire=str(d.get("fire") or ""),
                source=str(d.get("source") or ""),
                made=bool(d.get("made", False)),
                original=str(d.get("original") or ""),
            )
        )
    numbers = [e.number for e in out if e.number is not None]
    if len(numbers) != len(set(numbers)):
        raise BookFileError(f"{path}: the {book} book gives one number to two signals")
    return out


@cache
def load_books(root: str = "basic", base: str | None = None) -> Books:
    """A root's six files, read once."""
    folder = (Path(base) if base else SIGNALS_DIR) / root
    if not folder.is_dir():
        raise BookFileError(f"no signal books under {folder}; the roots are {roots()}")
    docs: dict[str, dict[str, Any]] = {}
    for name in BOOK_FILES:
        path = folder / f"{name}.yaml"
        if not path.exists():
            raise BookFileError(f"{folder}: the root wants {name}.yaml (every root has the six)")
        docs[name] = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    head = docs["book"]
    flags = dict(head.get("flags") or {})
    tele = docs["telegraphic"]
    words = {int(k): str(v) for k, v in (tele.get("words") or {}).items()}
    alphabet = {str(k).upper(): int(v) for k, v in (tele.get("alphabet") or {}).items()}
    nf = docs["night_fog"]
    private = docs["private"]
    return Books(
        root=root,
        nation=str(head.get("nation") or root),
        system=str(head.get("system") or "basic"),
        sources=[str(s) for s in (head.get("sources") or [])],
        flags=flags,
        hoist_s=int(head.get("hoist_s", 60)),
        read_s=int(head.get("read_s", 60)),
        read_nm=float(head.get("read_nm", 2.0)),
        glass_factor=float(head.get("glass_factor", 1.5)),
        flies_s=int(head.get("flies_s", 1800)),
        numerary=_entries(docs["numerary"].get("entries"), "numerary", folder / "numerary.yaml"),
        night=_entries(nf.get("night"), "night", folder / "night_fog.yaml"),
        fog=_entries(nf.get("fog"), "fog", folder / "night_fog.yaml"),
        convoy=_entries(docs["convoy"].get("entries"), "convoy", folder / "convoy.yaml"),
        words=words,
        alphabet=alphabet,
        telegraph=bool(tele.get("telegraph_flag", False)) and bool(words),
        private_form=dict(private),
        carried_by=tuple(str(r) for r in (private.get("carried_by") or _ROLES_WITH_TABLE)),
        answer_wait_s=int(private.get("answer_wait_s", 300)),
        forms=word_forms(words),
        hoist_form=_hoist_form(head, folder),
    )


HOIST_FORMS = ("numerary", "table")


def _hoist_form(head: dict[str, Any], folder: Path) -> str:
    form = str(head.get("hoist_form") or "numerary")
    if form not in HOIST_FORMS:
        raise BookFileError(f"{folder}/book.yaml: hoist_form is one of {HOIST_FORMS}, not {form!r}")
    return form


def roots() -> list[str]:
    return sorted(p.name for p in SIGNALS_DIR.iterdir() if p.is_dir())


def books_for_nation(nations: Any, nation_id: str) -> Books:
    """The books a nation reads: her root by the table, `basic` where she names none."""
    root = "basic"
    if nations is not None:
        try:
            root = str(nations.get(nation_id).signals_root or "basic")
        except KeyError:
            root = "basic"
    try:
        return load_books(root)
    except BookFileError:
        return load_books("basic")


def books_for(world: Any) -> Books:
    """The books of this World's ship, by her nation."""
    return books_for_nation(getattr(world, "nations", None), own_nation(world))


def own_nation(world: Any) -> str:
    ports = getattr(world, "dealings", None)
    nation = getattr(ports, "ship_nation", None) if ports is not None else None
    if not nation:
        nation = getattr(getattr(world, "scenario", None), "nation", None)
    return str(nation or "britain")


# ---------------------------------------------------------------------------
# The private table, drawn under the seed
# ---------------------------------------------------------------------------


def private_table(books: Books, nation: str, year: int, month: int, seed: int) -> PrivateTable:
    """The month's challenge and reply, by day and by night, drawn from the root's form
    by a stream seeded with the world's seed, the nation, the year and the month: two
    ships of one nation in one world hold the same table, a replay has it again, and
    another nation's draw from the same form is another table."""
    key = f"{seed}:{nation}:{year}:{month:02d}:private"
    rng = random.Random(zlib.crc32(key.encode("utf-8")))
    form = books.private_form

    def fill(template: str, pools: dict[str, Any]) -> str:
        used: dict[str, list[str]] = {}

        def pick(m: re.Match[str]) -> str:
            slot = m.group(1)
            pool = [str(x) for x in (pools.get(slot) or [slot])]
            taken = used.setdefault(slot, [])
            choices = [x for x in pool if x not in taken] or pool
            x = choices[rng.randrange(len(choices))]
            taken.append(x)
            return x

        return re.sub(r"\{(\w+)\}", pick, template).replace("one lights", "one light")

    day = dict(form.get("day") or {})
    night = dict(form.get("night") or {})
    dpools = dict(day.get("pools") or {})
    npools = dict(night.get("pools") or {})
    return PrivateTable(
        nation=nation,
        year=int(year),
        month=int(month),
        day_challenge=fill(str(day.get("challenge") or "a {flag} at the {place}"), dpools),
        day_reply=fill(str(day.get("reply") or "a {flag} at the {place}"), dpools),
        night_challenge=fill(str(night.get("challenge") or "{n} lights at the {place}"), npools),
        night_reply=fill(str(night.get("reply") or "{n} lights at the {place}"), npools),
    )


# ---------------------------------------------------------------------------
# Colours, hoists and the locker
# ---------------------------------------------------------------------------


@dataclass
class Colours:
    """A ship's colours as a state (spec M7 §1): `state` one of COLOURS_STATES, `nation`
    the nation whose colours she shows (her own under `shown` and `distress`, the other's
    under `false`, '' under `none` and `struck`), `since` the tick, and the tick of her
    first shot under false or no colours (the pirate's act, told once)."""

    state: str = "shown"
    nation: str = ""
    since: int = 0
    fired_under_false: int | None = None
    adjective: str = ""  # the words of the nation shown, for a reader with no table in hand
    flag: str = ""
    # package 74 (spec M7 §18): a prize wears her captor's colours over her own for a day
    # after the taking (`over`: the nation whose colours fly under; `over_since` the tick),
    # the period's sign of a prize; "" and 0 else, and in a checkpoint from before
    over: str = ""
    over_since: int = 0

    @property
    def shows(self) -> bool:
        return self.state in ("shown", "false", "distress", "truce")

    @property
    def shown_nation(self) -> str:
        """The nation a lookout makes out from them: '' when none are to be read, and ''
        under a flag of truce (package 74: a cartel is nobody's enemy and nobody's prize)."""
        return self.nation if self.shows and self.state != "truce" else ""

    def words(self, nations: Any) -> str:
        """'British colours, the red ensign'; 'no colours'; 'her colours struck'; 'the
        ensign union down'."""
        if self.state == "struck":
            return "her colours struck"
        if self.state == "none" or not self.nation:
            return "a stranger, her colours not made out"
        n = None
        if nations is not None:
            try:
                n = nations.get(self.nation)
            except KeyError:
                n = None
        adjective = n.adjective if n is not None else (self.adjective or self.nation)
        short = n.flag if n is not None else self.flag
        flag = f", {short}" if short else ""
        if self.state == "distress":
            return f"{adjective} colours{flag}, the ensign union down"
        if self.state == "truce":
            # a cartel (package 74, the design's §3.4; the lead's ruling with packages 76 and
            # 81: the state word `truce`, the words "a flag of truce")
            return "a flag of truce"
        over = getattr(self, "over", "")
        if over and self.state == "shown":
            # a prize: her captor's colours hoisted over her own (package 74)
            under = None
            if nations is not None:
                try:
                    under = nations.get(over)
                except KeyError:
                    under = None
            return f"{adjective} colours{flag} over {under.adjective if under else over}"
        return f"{adjective} colours{flag}"

    def to_dict(self) -> dict[str, Any]:
        return {"state": self.state, "nation": self.nation, "since": self.since}


def set_colours(colours: Colours, nations: Any, state: str, nation_id: str, tick: int) -> None:
    """The colours changed: the state, the nation shown and its words from the table."""
    if state not in COLOURS_STATES:
        raise ValueError(f"no colours state '{state}'")
    colours.state = state
    colours.since = int(tick)
    if state in ("none", "struck"):
        return
    colours.nation = str(nation_id or colours.nation)
    n = None
    if nations is not None:
        try:
            n = nations.get(colours.nation)
        except KeyError:
            n = None
    if n is not None:
        colours.adjective, colours.flag = n.adjective, n.flag


def colours_seen(body: Any) -> tuple[bool, str, str, str]:
    """What a lookout may read of a body's colours: (shown at all, the nation shown, its
    adjective, its flag's word); the truth is `body.nation`, which this never gives."""
    c = colours_of(body)
    if not c.shows or not c.nation:
        return False, "", "", ""
    return True, c.nation, c.adjective or c.nation, c.flag


@dataclass
class Hoist:
    """A signal flying: see the module's head."""

    book: str  # numerary | telegraphic | night | fog | convoy | private | reply | answer
    meaning: str
    by: str  # the sender's id ('the ship' for the player's)
    since: int  # the tick the order was given
    breaks_out: int  # the tick it is to be seen from (the hoist's minute)
    numbers: tuple[int, ...] = ()
    shown: str = ""  # the thing shown or fired, or the private signal's words
    qualifiers: dict[str, Any] = field(default_factory=dict)
    does: dict[str, Any] = field(default_factory=dict)
    in_succession: bool = False
    root: str = "basic"  # the sender's books' root (the reader needs the same book)
    to: str | None = None  # addressed to one ship by her pennants
    down: int | None = None  # hauled down at
    answered_by: set[str] = field(default_factory=set)
    words_made: list[str] = field(default_factory=list)  # a telegraphic sentence's hoists
    serial: int = 0
    complete_at: int | None = None  # a telegraphic sentence's last hoist up; else breaks_out
    form: str = "numerary"  # the book's hoist_form: how the flags look to a lookout without it
    # package 76 (item 8): a private challenge made in a named nation's form (the *Java*'s
    # move), answered only by a ship of that nation; '' for 71's own challenge, as before
    form_nation: str = ""
    # package 102 (step 3): where it flies, one of the colours' place words (`flags.py`
    # `place_ok`: a masthead, a truck, the peak, a yardarm); '' at the main, as every hoist
    # was before. A plain default, left out of the pickle and the record while unset, so that
    # a save from before loads and every hoist's line reads as it did.
    place: str = ""

    def __getstate__(self) -> dict[str, Any]:
        """Its state for the checkpoint, its place only where it has one (package 102)."""
        state = dict(self.__dict__)
        if not state.get("place"):
            state.pop("place", None)
        return state

    @property
    def done_at(self) -> int:
        return self.complete_at if self.complete_at is not None else self.breaks_out

    @property
    def key(self) -> str:
        return f"{self.by}:{self.since}:{self.serial}"

    def flying(self, tick: int) -> bool:
        return self.down is None and tick >= self.breaks_out

    def words(self) -> str:
        """'No. 16, engage the enemy more closely'; 'two guns: tack together'."""
        if self.book in ("numerary", "convoy") and self.numbers:
            head = "No. " + " ".join(str(n) for n in self.numbers)
            return f"{head}, {_lower(self.meaning)}"
        if self.book == "telegraphic":
            return f"the telegraphic signal: {self.meaning}"
        if self.book in ("night", "fog"):
            return f"{self.shown}: {_lower(self.meaning)}"
        if self.book == "private":
            return f"the private signal, {self.shown}"
        if self.book == "reply":
            return f"the private signal's reply, {self.shown}"
        if self.book == "answer":
            return self.meaning
        return self.meaning

    def flags_words(self) -> str:
        """What a lookout without the book sees: 'three flags at the main' (package 102: at
        its place where it has one, 'at the fore', 'at the main yardarm')."""
        at = _at_words(getattr(self, "place", ""))
        if self.book == "telegraphic":
            return "the telegraph flag over a hoist of flags"
        if self.book in ("numerary", "convoy"):
            if self.form == "table":
                # two flags a signal, the upper and the lower, whatever the cell's number
                return f"{_count(2 * max(1, len(self.numbers)))} flags at the {at}"
            n = len(str(self.numbers[0])) if self.numbers else 1
            return f"{_count(n)} flag{'s' if n > 1 else ''} at the {at}"
        if self.book in ("private", "reply"):
            return self.shown
        if self.book == "answer":
            return "the answering pendant"
        return self.shown

    def to_dict(self) -> dict[str, Any]:
        return {
            "book": self.book,
            "meaning": self.meaning,
            "by": self.by,
            "since": self.since,
            "numbers": list(self.numbers),
            "shown": self.shown,
            "to": self.to,
            "down": self.down,
            "answered_by": sorted(self.answered_by),
            # written only where it is not the numerary's, so that no British or basic
            # signal's record changes with the field (package 76)
            **({"form": self.form} if self.form != "numerary" else {}),
            # written only where it flies other than at the main (package 102)
            **({"place": self.place} if getattr(self, "place", "") else {}),
        }


def _at_words(place: str) -> str:
    """A hoist's place as the lookout says it: 'main' for none (every hoist before package
    102) and for the main's mastheads; 'fore', 'mizen'; 'main yardarm'; 'peak'."""
    if not place:
        return "main"
    if place.endswith(" masthead") or place.endswith(" truck"):
        return place.split(" ")[0]
    return place


def _lower(s: str) -> str:
    return s[:1].lower() + s[1:] if s else s


def _count(n: int) -> str:
    return ("one", "two", "three", "four", "five")[n - 1] if 1 <= n <= 5 else str(n)


@dataclass
class Locker:
    """The signal locker of one ship: her colours, the hoists flying and made, her lights
    and her fog signals, what her people have seen and read, and the private challenges
    awaiting an answer. One object for a ship's two bodies."""

    colours: Colours = field(default_factory=Colours)
    flying: list[Hoist] = field(default_factory=list)
    made: list[Hoist] = field(default_factory=list)
    lights: str = "none"  # none | stern lantern | top lights | a lantern at her nets
    fog_signals: bool = False
    fog_since: int | None = None
    seen: dict[str, int] = field(default_factory=dict)  # hoist key -> tick seen
    read: dict[str, int] = field(default_factory=dict)  # hoist key -> tick read
    answered: set[str] = field(default_factory=set)  # hoist keys answered
    obeyed: dict[str, int] = field(default_factory=dict)  # hoist key -> tick performed
    challenges: dict[str, dict[str, Any]] = field(default_factory=dict)  # by ship id
    serial: int = 0
    # what other ships' signals were read (for `the signals` reading), newest last
    log: list[dict[str, Any]] = field(default_factory=list)
    # package 76 (item 8): what flies where, as the viewer reads it (`{place, name, words,
    # drawing}`), set by the rules from the nation's colours.yaml (`freesail/world/flags.py`);
    # None until set, when the viewer serves its own plain ensign; and the flags ordered
    # beside the file's (`hoist the broad pendant`, `... a second ensign`, `... the jack`)
    flies: list[dict[str, Any]] | None = None
    ordered_flags: list[str] = field(default_factory=list)

    def next_serial(self) -> int:
        self.serial += 1
        return self.serial

    def hoist(self, h: Hoist) -> Hoist:
        h.serial = self.next_serial()
        self.flying.append(h)
        self.made.append(h)
        if len(self.made) > 40:
            del self.made[:-40]
        return h

    def haul_down(self, tick: int, book: str | None = None) -> list[Hoist]:
        down = [h for h in self.flying if h.down is None and (book is None or h.book == book)]
        for h in down:
            h.down = tick
        self.flying = [h for h in self.flying if h.down is None]
        return down

    def tidy(self, tick: int, flies_s: int) -> None:
        """A numerary signal left flying a glass comes down of itself; an answer after
        five minutes; a telegraphic sentence two minutes after its last hoist is up (its
        words were hauled down one by one as they were made); a private signal after ten;
        a hoist bent on and never run up (the hands never had) after a glass."""
        for h in self.flying:
            if h.down is not None:
                continue
            if h.breaks_out >= NOT_YET:
                if tick - h.since >= flies_s:
                    h.down = tick
                continue
            life = flies_s
            since = h.breaks_out
            if h.book in ("answer", "reply"):
                life = 300
            elif h.book == "telegraphic":
                life, since = 120, h.done_at  # NOT_YET while the hoists are going up
            elif h.book == "private":
                life = 600
            if since < NOT_YET and tick - since >= life:
                h.down = tick
        self.flying = [h for h in self.flying if h.down is None]

    def flying_now(self, tick: int) -> list[Hoist]:
        return [h for h in self.flying if h.flying(tick)]


def locker_of(ship: Any) -> Locker:
    """The ship's locker, made on first asking (a near body); the far body's is the
    vessel's own (`vessel_locker`)."""
    extra = getattr(ship, "extra", None)
    if extra is None:
        return Locker()
    locker = extra.get("signals")
    if locker is None:
        locker = extra["signals"] = Locker()
    return locker


def vessel_locker(vessel: Any) -> Locker:
    """The far vessel's locker (the same object as her crewed World's while she is
    promoted: `crews.promote` hands it over)."""
    locker = getattr(vessel, "signals", None)
    if locker is None:
        locker = Locker(
            colours=Colours(
                state="shown" if getattr(vessel, "shows_colours", True) else "none",
                nation=str(getattr(vessel, "nation", "") or ""),
                adjective=str(getattr(vessel, "nation_adjective", "") or ""),
                flag=str(getattr(vessel, "flag", "") or ""),
            )
        )
        vessel.signals = locker
    return locker


def colours_of(body: Any) -> Colours:
    """The colours of any body: a near ship (its locker's) or a far vessel (hers)."""
    if hasattr(body, "extra") and hasattr(body, "spars"):
        return locker_of(body).colours
    return vessel_locker(body).colours


def flying_of(body: Any, tick: int) -> list[Hoist]:
    if hasattr(body, "extra") and hasattr(body, "spars"):
        return locker_of(body).flying_now(tick)
    return vessel_locker(body).flying_now(tick)


# ---------------------------------------------------------------------------
# Making a signal
# ---------------------------------------------------------------------------


def light_now(world: Any) -> str:
    """'day', 'night' or 'fog' (the visibility under a mile), which chooses the book."""
    conditions = getattr(world, "conditions", None)
    vis = getattr(conditions, "visibility_nm", None) if conditions is not None else None
    if vis is not None and float(vis) < 1.0:
        return "fog"
    daylight = str(getattr(world, "daylight", "day"))
    return "night" if daylight == "night" else "day"


def make_hoist(
    locker: Locker,
    books: Books,
    entry: Entry,
    qualifiers: dict[str, Any],
    by: str,
    tick: int,
    to: str | None = None,
    at_once: bool = False,
) -> Hoist:
    """A signal of a book made now: it breaks out after the hoist's minute (at once for a
    far body that has no hands to count, with the minute added instead)."""
    numbers: tuple[int, ...] = ()
    shown = ""
    if entry.book in ("numerary", "convoy") and entry.number is not None:
        numbers = (entry.number,)
        if qualifiers.get("number") is not None:
            numbers = (entry.number, int(qualifiers["number"]))
    elif entry.book == "night":
        shown = entry.show
    elif entry.book == "fog":
        shown = entry.fire
    meaning = entry.meaning
    if qualifiers.get("compass"):
        meaning = f"{meaning}, {qualifiers['compass']}"
    elif qualifiers.get("place"):
        meaning = f"{meaning}: {qualifiers['place']}"
    elif qualifiers.get("ship"):
        meaning = f"{meaning} (to {qualifiers['ship']})"
    h = Hoist(
        book=entry.book,
        meaning=meaning,
        by=by,
        since=tick,
        breaks_out=tick if at_once else tick + books.hoist_s,
        numbers=numbers,
        shown=shown,
        qualifiers=dict(qualifiers),
        does=dict(entry.does),
        in_succession=entry.in_succession,
        root=books.root,
        to=to,
        form=books.hoist_form,
    )
    return locker.hoist(h)


def make_private(
    locker: Locker,
    books: Books,
    table: PrivateTable,
    light: str,
    by: str,
    tick: int,
    reply: bool = False,
    to: str | None = None,
    wrong: str = "",
    at_once: bool = False,
    form_nation: str = "",
) -> Hoist:
    shown = wrong or (table.reply(light) if reply else table.challenge(light))
    h = Hoist(
        book="reply" if reply else "private",
        meaning="the private signal's reply" if reply else "the private signal",
        by=by,
        since=tick,
        breaks_out=tick if at_once else tick + books.hoist_s,
        shown=shown,
        root=books.root,
        to=to,
        form_nation=form_nation,
    )
    return locker.hoist(h)


def make_answer(
    locker: Locker, books: Books, by: str, tick: int, to: str, what: str = "", at_once: bool = False
) -> Hoist:
    """The answering pendant (or the negative, 'cannot comply')."""
    h = Hoist(
        book="answer",
        meaning=what or "the answering pendant: the signal seen and understood",
        by=by,
        since=tick,
        breaks_out=tick if at_once else tick + books.hoist_s,
        shown="the answering pendant" if not what else what,
        root=books.root,
        to=to,
    )
    return locker.hoist(h)


def wrong_reply(books: Books, nation: str, year: int, month: int, seed: int, light: str) -> str:
    """A bluffed reply to a private signal: the form filled by another draw, which is
    wrong by every table but its own (a privateer's guess)."""
    table = private_table(books, f"bluff-{nation}", year, month, seed)
    return table.reply(light)


# ---------------------------------------------------------------------------
# Reading what flies
# ---------------------------------------------------------------------------


@dataclass
class Seen:
    """What a reader makes of a hoist this minute: the line's kind, text and data, and the
    hoist, for the lookout to record and the captain to act on."""

    kind: str
    text: str
    data: dict[str, Any]
    hoist: Hoist
    read: bool  # the meaning known (the book held)


def read_flying(
    reader: Locker,
    reader_books: Books,
    sender_id: str,
    sender_words: str,
    hoists: list[Hoist],
    distance_m: float,
    light: str,
    glass: bool,
    tick: int,
    reader_id: str,
    held_books: tuple[str, ...] = (),
) -> list[Seen]:
    """What the reader's people see of a sender's flying hoists at this distance in this
    light: 'she makes a signal' when a hoist is first seen, its meaning `read_s` later
    when the reader holds the sender's book (her own root, or a captured one), and the
    private signal's words by their form; nothing beyond the flags' range. A fog signal
    (a gun) is heard at `GUN_HEARD_NM`; a night signal's lights seen at `LIGHT_SEEN_NM`."""
    out: list[Seen] = []
    nm = distance_m / units.NAUTICAL_MILE
    for h in hoists:
        if not h.flying(tick):
            continue
        if h.book == "fog":
            reach = GUN_HEARD_NM
        elif light == "night" or h.book == "night":
            reach = LIGHT_SEEN_NM
        else:
            reach = reader_books.read_nm * (reader_books.glass_factor if glass else 1.0)
        if light == "fog" and h.book != "fog":
            reach = min(reach, 0.5)  # flags in a fog: under half a mile (judgement)
        if nm > reach:
            continue
        key = h.key
        first = key not in reader.seen
        if first:
            reader.seen[key] = tick
        can_read = h.book in ("answer", "private", "reply") or h.root in (
            reader_books.root,
            *held_books,
        )
        if h.book == "fog" and first:
            text = f"{_cap(sender_words)} fires {h.shown}"
            if can_read:
                text += f": {_lower(h.meaning)}."
            else:
                text += " in the fog, a signal we cannot read."
            out.append(
                Seen(
                    "signal.read" if can_read else "signal.seen",
                    text,
                    {"id": sender_id, "hoist": h.to_dict(), "read": can_read},
                    h,
                    can_read,
                )
            )
            if can_read:
                reader.read[key] = tick
            continue
        if first:
            if h.book == "answer":
                text = f"{_cap(sender_words)} hoists the answering pendant."
                reader.read[key] = tick
                out.append(
                    Seen("signal.answered", text, {"id": sender_id, "hoist": h.to_dict()}, h, True)
                )
                continue
            if h.book in ("private", "reply"):
                what = "the private signal" if h.book == "private" else "a reply: "
                text = (
                    f"{_cap(sender_words)} makes {what}{h.shown if h.book == 'reply' else ''}"
                    + (f": {h.shown}." if h.book == "private" else ".")
                )
                reader.read[key] = tick
                out.append(
                    Seen(
                        "signal.private" if h.book == "private" else "signal.private_reply",
                        text,
                        {"id": sender_id, "hoist": h.to_dict()},
                        h,
                        True,
                    )
                )
                continue
            flags = h.flags_words()
            text = f"{_cap(sender_words)} makes a signal: {flags}"
            text += "." if can_read else ", a signal we cannot read: not of our book."
            out.append(
                Seen(
                    "signal.seen",
                    text,
                    {"id": sender_id, "hoist": h.to_dict(), "read": False, "ours": can_read},
                    h,
                    False,
                )
            )
            continue
        if (
            can_read
            and key not in reader.read
            and tick - reader.seen[key] >= reader_books.read_s
            and tick >= h.done_at + reader_books.read_s
        ):
            reader.read[key] = tick
            text = f"{_cap(sender_words)}'s signal is {h.words()}."
            if h.to is not None and h.to == reader_id:
                text = f"{_cap(sender_words)}'s signal, to us: {h.words()}."
            out.append(
                Seen(
                    "signal.read",
                    text,
                    {
                        "id": sender_id,
                        "hoist": h.to_dict(),
                        "read": True,
                        "to_us": h.to == reader_id,
                    },
                    h,
                    True,
                )
            )
    return out


def _cap(words: str) -> str:
    return words[:1].upper() + words[1:]


def note_seen(reader: Locker, seen: list[Seen], tick: int) -> None:
    """The reader's own record of what was read this minute, for the captain's judgement
    and `the signals` reading (newest last, forty kept)."""
    for s in seen:
        reader.log.append(
            {
                "tick": tick,
                "by": s.data.get("id"),
                "key": s.hoist.key,
                "kind": s.kind,
                "book": s.hoist.book,
                "meaning": s.hoist.meaning,
                "words": s.text,
                "to_us": bool(s.data.get("to_us")),
                "hoist": s.hoist,
                "handled": False,
            }
        )
    if len(reader.log) > 40:
        del reader.log[:-40]


# ---------------------------------------------------------------------------
# The private signal judged
# ---------------------------------------------------------------------------


def judge_private(
    locker: Locker,
    table: PrivateTable,
    light: str,
    other_id: str,
    reply: Hoist | None,
    tick: int,
    wait_s: int,
) -> str | None:
    """The challenger's verdict on a stranger challenged: 'right', 'wrong', 'none' (the
    wait out with no reply), or None while he waits. The challenge is the locker's own
    record of whom he challenged and when."""
    c = locker.challenges.get(other_id)
    if c is None or c.get("verdict"):
        return None
    if reply is not None and reply.breaks_out >= c["tick"]:
        expected = table.reply(light)
        verdict = "right" if _norm_words(reply.shown) == _norm_words(expected) else "wrong"
        c["verdict"] = verdict
        c["judged"] = tick
        return verdict
    if tick - int(c["tick"]) >= wait_s:
        c["verdict"] = "none"
        c["judged"] = tick
        return "none"
    return None


def _norm_words(s: str) -> str:
    return " ".join(str(s or "").lower().replace(",", " ").split())


# ---------------------------------------------------------------------------
# Obeying
# ---------------------------------------------------------------------------


def commanded_by(reader_vessel_or_world: Any, sender_id: str) -> bool:
    """Whether the sender's signals command this ship: she is `under the orders of` him
    (the scenario's or the director's word), or the signal was addressed to her."""
    boss = getattr(reader_vessel_or_world, "under_orders_of", None)
    if boss is None:
        vessel = getattr(reader_vessel_or_world, "vessel", None)
        boss = getattr(vessel, "under_orders_of", None)
    return bool(boss) and str(boss) == str(sender_id)


def order_of(h: Hoist) -> str | None:
    """The dialect's order a commanded captain gives for the hoist, the qualifiers
    filled, or None when the entry is news, an answer, a state or a release."""
    does = h.does or {}
    text = does.get("order")
    if not text:
        return None
    q = h.qualifiers or {}
    text = str(text)
    if "{compass}" in text:
        if not q.get("compass"):
            return None
        text = text.replace("{compass}", str(q["compass"]))
    if "{place}" in text:
        if not q.get("place"):
            return None
        text = text.replace("{place}", str(q["place"]))
    if "{number}" in text:
        text = text.replace("{number}", str(q.get("number", "")))
    return text


def succession_rank(
    sea_vessels: list[Any], reader_id: str, sender_id: str, squadrons: Any = None
) -> tuple[int, Any]:
    """The reader's place among the ships under the sender's orders (her set's order of
    sailing when she is in one, package 72; else the scenario's and the director's order of
    their making: the leader first), and the ship before her."""
    under = [v for v in sea_vessels if str(getattr(v, "under_orders_of", "") or "") == sender_id]
    sq = squadrons.of(reader_id) if squadrons is not None else None
    if sq is not None:
        by_id = {str(v.id): v for v in sea_vessels}
        ordered = [by_id[m] for m in sq.under(sender_id) if m in by_id]
        if any(str(v.id) == reader_id for v in ordered):
            under = ordered
    ids = [str(v.id) for v in under]
    if reader_id not in ids:
        return 0, None
    i = ids.index(reader_id)
    return i, (under[i - 1] if i > 0 else None)


def predecessor_done(prev: Any, key: str, tick: int) -> bool:
    """Whether the ship before her in the succession has performed the signal and had
    her time to come round (`SUCCESSION_GAP_S`)."""
    if prev is None:
        return True
    locker = vessel_locker(prev)
    t = locker.obeyed.get(key)
    return t is not None and tick - t >= SUCCESSION_GAP_S


_LIGHT_ORDERS = (
    "show no lights",
    "hoist the top lights",
    "hoist a stern lantern",
    "hoist the lights",
)


def far_perform(world: Any, vessel: Any, order: str) -> str:
    """A commanded far body performs an order of the few the signals give: put about or
    wear (her course mirrored about the wind's eye), heave to and fill away, make and
    shorten sail, anchor and weigh, steer a course, close the flag (keep company with
    the sender), shape a course for a place; the line for her story. Returns the words of
    what she did ('' when the order is none she has)."""
    low = " ".join(str(order).lower().split())
    wind_from, wind_ms = vessel._wind_at(world)
    wind_kn = units.ms_to_knots(float(wind_ms))
    plan = vessel.plan
    if low in ("put her about", "tack", "tack ship", "wear ship", "wear"):
        heading = float(vessel.heading_deg)
        new = (2.0 * float(wind_from) - heading) % 360.0
        from freesail.world.geo import destination

        company = [leg for leg in plan if leg[0] in ("company", "station")]
        reach = (1.0 if company else 30.0) * units.NAUTICAL_MILE
        far = destination(vessel.position, new, reach)
        vessel.saved_plan = vessel.saved_plan or list(plan)
        vessel.plan = [("to", far, f"the other tack ({units.point_name(math.radians(new))})")]
        if company:
            # a ship keeping company goes about, stands on a mile on the new tack and closes
            # her commodore again (the least relation); a member of a set takes up her
            # station leg again after it (package 72: the set's stations turn with him)
            vessel.plan.append(company[0])
        vessel.tack = 0.0
        return ("went about" if low.startswith(("put", "tack")) else "wore") + (
            f", her head {units.point_name(math.radians(new))}"
        )
    if low in ("heave to", "bring to", "lie to"):
        if not plan or plan[0][0] != "lie_to":
            vessel.saved_plan = list(plan)
            vessel.plan = [("lie_to", math.inf)]
        return "hove to"
    if low in ("fill away", "fill", "fill and make sail"):
        if plan and plan[0][0] == "lie_to":
            vessel.plan = list(vessel.saved_plan or [])
            vessel.saved_plan = None
            vessel.lying_to_s = 0.0
        return "filled away"
    if low in ("make sail", "make all sail", "set plain sail", "shake out the reefs"):
        vessel.sail_order = "under plain sail"
        return "made sail"
    if low in (
        "shorten sail",
        "take in a reef in the topsails",
        "close reef the topsails",
        "reef the topsails",
    ):
        vessel.sail_order = "under reefed topsails"
        return "shortened sail"
    if low in ("come to an anchor", "anchor", "let go the anchor"):
        if not (plan and plan[0][0] == "anchor"):
            vessel.saved_plan = list(plan)
        vessel.plan = [("anchor", "")]
        return "came to an anchor"
    if low in ("weigh anchor", "weigh", "get under way", "heave short"):
        if plan and plan[0][0] == "anchor":
            vessel.plan = list(vessel.saved_plan or [])
            vessel.saved_plan = None
        return "weighed"
    if low.startswith("steer "):
        words = low.removeprefix("steer ").strip()
        try:
            rad = units.parse_course(words)
        except Exception:  # noqa: BLE001 - 'two points to starboard'
            m = re.match(r"(\w+) points? to (starboard|larboard|port)", words)
            if m is None:
                return ""
            n = {"one": 1, "two": 2, "three": 3, "four": 4, "1": 1, "2": 2, "3": 3, "4": 4}.get(
                m.group(1), 2
            )
            sign = 1.0 if m.group(2) == "starboard" else -1.0
            rad = math.radians((float(vessel.heading_deg) + sign * n * 11.25) % 360.0)
        from freesail.world.geo import destination

        course_deg = units.rad_to_deg(rad) % 360.0
        far = destination(vessel.position, course_deg, 30.0 * units.NAUTICAL_MILE)
        vessel.saved_plan = vessel.saved_plan or list(plan)
        vessel.plan = [("to", far, f"a course {units.point_name(rad)}")]
        vessel.tack = 0.0
        return f"steered {units.point_name(rad)}"
    if low in ("close the flag", "shape a course for the flag", "close the commodore"):
        boss = str(getattr(vessel, "under_orders_of", "") or "")
        if getattr(vessel, "squadron", "") and plan and plan[0][0] == "station":
            # package 72: a member of a set closes by the set's order (close order is the
            # set's formation, which the commander's signal has set); her station leg stands
            return "closed on the commodore in her station"
        if boss == "the ship":
            vessel.saved_plan = vessel.saved_plan or list(plan)
            vessel.plan = [("company", 2.0 * units.CABLE)]
            return "closed the commodore"
        vessel.saved_plan = vessel.saved_plan or list(plan)
        vessel.plan = [("chase", boss, 2.0 * units.CABLE)]
        return "closed the commodore"
    if low in ("keep her full and by", "haul your wind"):
        off = units.rad_to_deg(units.wrap_pi(math.radians(float(vessel.heading_deg) - wind_from)))
        side = 1.0 if off >= 0 else -1.0
        new = (float(wind_from) + side * vessel.polar.beat_deg(wind_kn)) % 360.0
        from freesail.world.geo import destination

        far = destination(vessel.position, new, 30.0 * units.NAUTICAL_MILE)
        vessel.saved_plan = vessel.saved_plan or list(plan)
        vessel.plan = [("to", far, f"by the wind ({units.point_name(math.radians(new))})")]
        return "hauled her wind"
    if low.startswith(("keep her full and by on the",)):
        tack = "starboard" if "starboard" in low else "larboard"
        # the wind on the starboard side: her head to larboard of the eye
        side = -1.0 if tack == "starboard" else 1.0
        new = (float(wind_from) + side * vessel.polar.beat_deg(wind_kn)) % 360.0
        from freesail.world.geo import destination

        far = destination(vessel.position, new, 30.0 * units.NAUTICAL_MILE)
        vessel.saved_plan = vessel.saved_plan or list(plan)
        vessel.plan = [("to", far, f"by the wind on the {tack} tack")]
        return f"hauled her wind on the {tack} tack"
    if low.startswith("shape a course for "):
        from freesail.world.ships import place_position

        found = place_position(world, low.removeprefix("shape a course for ").strip())
        if found is None:
            return ""
        vessel.saved_plan = None
        vessel.plan = [("to", found[0], found[1])]
        return f"shaped a course for {found[1]}"
    if low in ("hoist the colours", "hoist our colours", "hoist your true colours"):
        c = vessel_locker(vessel).colours
        c.state, c.nation, c.since = "shown", str(vessel.nation), int(world.clock.tick)
        return "hoisted her colours"
    if low in ("hoist false colours",):
        return ""  # a far body under orders shows what her captain's doctrine says
    if low in _LIGHT_ORDERS:
        vessel_locker(vessel).lights = (
            "none" if "no lights" in low else "top lights" if "top" in low else "stern lantern"
        )
        return "her lights " + ("doused" if "no lights" in low else "hoisted")
    return ""


# ---------------------------------------------------------------------------
# This World's own
# ---------------------------------------------------------------------------


def player_locker(world: Any) -> Locker:
    """This World's own ship's locker, her colours filled with her nation at the first
    asking (a King's ship wears them from the start; the scenario may say `none`)."""
    locker = locker_of(world.ship)
    if not locker.colours.nation:
        scenario = getattr(world, "scenario", None)
        state = str(getattr(scenario, "colours", "") or "shown")
        set_colours(locker.colours, getattr(world, "nations", None), state, own_nation(world), 0)
    return locker


def own_id(world: Any) -> str:
    """This World's ship's id as the other sail know her: her vessel's, or 'the ship'."""
    vessel = getattr(world, "vessel", None)
    return str(vessel.id) if vessel is not None else "the ship"


def held_books(world: Any) -> tuple[str, ...]:
    """The roots of the signal books in the ship's library beside her nation's own (a
    captured book, 74's prize; the scenario's `papers: {signal_books: [france]}`)."""
    papers = getattr(getattr(world, "scenario", None), "papers", None) or {}
    held = papers.get("signal_books") if isinstance(papers, dict) else None
    return tuple(str(x) for x in (held or []))


def has_glass(world: Any) -> bool:
    """Whether a glass is aboard for the flags: the scenario's, or any crewed ship's
    captain's (the far brain has one on the sail he has in hand)."""
    if getattr(world, "parent", None) is not None:
        return True  # another hull: her captain's glass
    return bool(getattr(getattr(world, "scenario", None), "glass", False))


def root_seed(world: Any) -> int:
    """The world's seed for the private table: a crewed World's is her parent's, so that
    the two ships of one nation in one world hold one table."""
    parent = getattr(world, "parent", None)
    return int(getattr(parent if parent is not None else world, "seed", 0) or 0)


def table_of(world: Any) -> PrivateTable | None:
    """The private table this World's ship carries this month: her nation's, when the
    scenario's papers give it (`papers: {private_signals: true}`; `false` takes it away)
    or her captain's role is one the table is issued to (the root's `carried_by`: a King's
    ship, a cruiser, a commodore); None in a merchantman, a packet, a privateer, a
    fisherman or a prize."""
    books = books_for(world)
    nation = own_nation(world)
    papers = getattr(getattr(world, "scenario", None), "papers", None) or {}
    given = papers.get("private_signals") if isinstance(papers, dict) else None
    if given is False:
        return None
    carried = bool(given)
    if not carried:
        captain = getattr(world, "captain", None)
        role = str(getattr(captain, "role", "") or "")
        if not role:
            vessel = getattr(world, "vessel", None)
            brain = getattr(vessel, "brain", None)
            role = str(getattr(brain, "role", "") or "")
        carried = books.table_carried_by(role)
    if not carried:
        return None
    now = world.clock.ship_time
    nations = getattr(world, "nations", None)
    table = private_table(books, nation, now.year, now.month, root_seed(world))
    try:
        table.adjective = nations.get(nation).adjective if nations is not None else ""
    except KeyError:
        table.adjective = ""
    return table


def vessel_table(world: Any, vessel: Any) -> PrivateTable | None:
    """A far vessel's table: her nation's when her brain's role is issued one."""
    brain = getattr(vessel, "brain", None)
    role = str(getattr(brain, "role", "") or "")
    books = books_for_nation(getattr(world, "nations", None), str(vessel.nation))
    if not books.table_carried_by(role):
        return None
    now = world.clock.ship_time
    return private_table(books, str(vessel.nation), now.year, now.month, root_seed(world))


def held_tables(world: Any) -> dict[str, PrivateTable]:
    """The private tables this World's ship holds this month, by nation (package 76, item 8,
    the *Java*'s move): her own nation's where she carries it (`table_of`), and the table of
    each book in her library (`held_books`: an ally's carried by the scenario's papers, a
    captured one by 74's road; a root or the id of a nation standing on basic), each the same
    draw the ships of that nation hold."""
    out: dict[str, PrivateTable] = {}
    own = table_of(world)
    if own is not None:
        out[own.nation] = own
    nations = getattr(world, "nations", None)
    now = world.clock.ship_time
    for held in held_books(world):
        # a root ('spain') or a nation standing on basic ('portugal'): her books and her name
        if held in roots():
            books = load_books(held)
            nation = books.nation
        else:
            try:
                nation = nations.get(held).id if nations is not None else ""
            except KeyError:
                continue
            books = books_for_nation(nations, nation)
        if not nation or nation in out or nation == "basic":
            continue
        table = private_table(books, nation, now.year, now.month, root_seed(world))
        try:
            table.adjective = nations.get(nation).adjective if nations is not None else ""
        except KeyError:
            table.adjective = ""
        out[nation] = table
    return out


def far_order_words(world: Any, vessel: Any, text: str) -> tuple[str, str, dict[str, Any]] | None:
    """A far body's order of the colours, the lights or the signals, for the director's
    hand (`crews.far_order`): (kind, the line, data), or None when the words are none of
    these. A signal is made by its meaning from her nation's book, at once (no hands to
    count on a far body; the minute to run it up kept)."""
    import re

    low = " ".join(str(text).lower().split()).rstrip(".")
    tick = int(world.clock.tick)
    locker = vessel_locker(vessel)
    nations = getattr(world, "nations", None)
    m = re.match(
        r"^(?:hoist|show)\s+(?:the\s+|a\s+)?(?P<n>false|[a-z-]+)\s+(?:colours|ensign|flag)$", low
    )
    if m and m.group("n") not in ("the", "our", "her", "true", "your"):
        word = m.group("n")
        if word == "false":
            enemies = nations.enemies_of(str(vessel.nation)) if nations is not None else []
            nid = enemies[0] if enemies else None
        else:
            found = nations.find(word) if nations is not None else None
            nid = found.id if found is not None else None
        if nid is None:
            from freesail.orders.errors import OrderError

            raise OrderError(f"'{word}' names no nation of the table for her colours.")
        if nid == str(vessel.nation):
            set_colours(locker.colours, nations, "shown", nid, tick)
            return (
                "colours.changed",
                f"Her own colours hoisted: {locker.colours.words(nations)}.",
                {},
            )
        set_colours(locker.colours, nations, "false", nid, tick)
        return "colours.changed", f"False colours hoisted: {locker.colours.words(nations)}.", {}
    done = far_perform(world, vessel, low)
    if done and low in (
        "hoist the colours",
        "hoist our colours",
        "hoist your true colours",
        "show no lights",
        "hoist the top lights",
        "hoist a stern lantern",
        "hoist the lights",
    ):
        return "colours.changed" if "colours" in low else "lights.changed", f"{_cap(done)}.", {}
    if low in ("haul down the colours", "haul down the ensign"):
        set_colours(locker.colours, nations, "none", "", tick)
        return "colours.changed", "The colours hauled down: she shows none.", {}
    m = re.match(r"^(?:make|hoist)\s+(?:the|a)\s+signal(?:\s*[:,]\s*|\s+)(?P<words>.+)$", low)
    if m:
        books = books_for_nation(nations, str(vessel.nation))
        light = light_now(world)
        book = BOOKS_BY_LIGHT[light]
        found = books.find(m.group("words"), book)
        if found is None and book == "numerary":
            found = books.find(m.group("words"), "convoy")
        if found is None:
            from freesail.orders.errors import OrderError

            raise OrderError(f"'{m.group('words')}' is no signal of her {book} book.")
        entry, qualifiers = found
        h = make_hoist(locker, books, entry, qualifiers, str(vessel.id), tick)
        return (
            "signal.made",
            f"The signal made: {h.words()} (up in a minute).",
            {"hoist": h.to_dict()},
        )
    if low in ("answer the signal", "hoist the answering pendant", "hoist the answering pennant"):
        last = next(
            (e for e in reversed(locker.log) if e.get("kind") in ("signal.read", "signal.seen")),
            None,
        )
        if last is None:
            from freesail.orders.errors import OrderError

            raise OrderError("No signal has been seen to answer.")
        books = books_for_nation(nations, str(vessel.nation))
        make_answer(locker, books, str(vessel.id), tick, str(last["by"]))
        return "signal.made", "The answering pendant hoisted.", {}
    if low in ("haul down the signal", "haul it down", "haul down the signals"):
        down = locker.haul_down(tick)
        return "signal.down", f"The signal hauled down ({len(down)}).", {}
    return None
