"""Books drafted (spec M7b §16; package 53): a standing-orders sheet, a note for the ship's
papers or a manifest to buy and sell several goods at once, written by a person aboard as
a book in the library with his mark.

    draft a book "night orders": standing order "royals": at sunset then take in the
                                 royals; standing order "lead": every glass then heave the
                                 lead
    draft a book "cargo": buy 20 tons of tin; sell 10 tons of salt
    draft a book "the passage": We made the Lizard at noon and spoke the packet.
    post the book "night orders"     the sheet's orders entered in the book, in force
    give the book "cargo" to the boat
                                     the manifest's bargains struck together and the boat
                                     sent once for them all
    the books                        the books drafted, each with its mark
    show the book "the passage"      one book's page

**What a book is** is read from its lines (`;` between them): every line a standing order
(`standing order "x": ...`, or `"x": ...` with the words left out) is a **sheet**; every
line a bargain (`buy <n> tons of <good>`, `sell ...`) is a **manifest**; anything else is a
**note**, kept as written. A sheet's orders and a manifest's bargains are read when it is
drafted, so that a line the ship cannot read refuses the draft in words and nothing is
written. The book carries the mark of the person who drafted it (the giver of the order,
`movement.person_of_actor`: the captain at the prompt, a station's person at his station)
and his rank, the day and the hour, and is served by the library from anywhere (the owner's
ruling of 2026-10-16: the papers kept in a place are dropped), under the topic `books`.

**Its use is functional.** A sheet posted (`post the book`) makes its orders the standing
orders: each entered in the book in the poster's rank, one of the same name that the
poster gave (or any, for the captain) struck and entered anew; a line naming another rank,
or an order of the same name another gave, refuses the posting whole. A manifest given to
the boat trades its goods in one errand (`Ports.trade_list`): every bargain weighed before
any is struck, and the boat sent once. A note is the record and nothing acts on it.

The books are kept on the World (`books_of`), made again by a replay from the orders that
drafted them (each an order, journaled, so a replay drafts it at its tick), and held whole
by a checkpoint.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from freesail import units
from freesail.orders.errors import OrderError
from freesail.orders.vocabulary import load_vocabulary, normalise

__all__ = [
    "MANIFEST",
    "NOTE",
    "SHEET",
    "Book",
    "Books",
    "books_of",
    "handle",
    "read_kind",
    "recognises",
]

SHEET, MANIFEST, NOTE = "standing orders", "manifest", "note"

_KIND_WORDS = {
    SHEET: "a standing-orders sheet",
    MANIFEST: "a manifest",
    NOTE: "a note for the ship's papers",
}

_QUOTES = "\"'“”‘’"
_NAMED = re.compile(r"^\s*[\"“'‘](?P<name>[^\"”'’]+)[\"”'’]\s*(?:by\s+[^:]+)?:")
_BARGAIN = re.compile(r"^\s*(buy|sell)\b", re.I)


@dataclass
class Book:
    """A book drafted: its title, its kind, its lines as written, the drafter's mark and
    rank, when it was drafted, and when it was posted or given to the boat."""

    title: str
    kind: str
    lines: list[str]
    mark: str  # the drafter's name
    rank: str  # his rank, for a sheet's orders ("captain", "first lieutenant")
    tick: int
    stamp: str
    posted: str = ""  # the stamp of its posting or giving, "" while it is not
    by: list[str] = field(default_factory=list)  # who posted or gave it

    @property
    def key(self) -> str:
        return _key(self.title)

    def head(self) -> str:
        kind = _KIND_WORDS.get(self.kind, self.kind)
        n = len(self.lines)
        what = {SHEET: "order", MANIFEST: "bargain", NOTE: "line"}.get(self.kind, "line")
        done = ""
        if self.posted:
            done = (
                f"; given to the boat {self.posted}"
                if self.kind == MANIFEST
                else f"; posted {self.posted}"
            )
        return (
            f"'{self.title}': {kind} of {n} {what}{'s' if n != 1 else ''}, drafted by "
            f"{self.mark} on {self.stamp}{done}"
        )

    def page(self) -> list[str]:
        return [f"The book {self.head()}.", *(f"  {line}" for line in self.lines)]


class Books:
    """The books drafted aboard one World, in the order drafted."""

    def __init__(self) -> None:
        self.items: list[Book] = []

    def find(self, title: str) -> Book | None:
        key = _key(title)
        for b in self.items:
            if b.key == key:
                return b
        loose = [b for b in self.items if key and key in b.key]
        return loose[0] if len(loose) == 1 else None

    def lines(self) -> list[str]:
        if not self.items:
            return ["No books have been drafted aboard."]
        return [f"The books drafted ({len(self.items)}):"] + [f"  {b.head()}." for b in self.items]


def books_of(world: Any) -> Books:
    """The World's books, made at the first call (a checkpoint from before has none)."""
    books = getattr(world, "books", None)
    if books is None:
        books = Books()
        world.books = books
    return books


def _key(title: str) -> str:
    text = str(title).lower()
    for q in _QUOTES:
        text = text.replace(q, "")
    return " ".join(text.split()).removeprefix("the ")


# ---------------------------------------------------------------------------
# The sentences
# ---------------------------------------------------------------------------


def _matched(text: str) -> tuple[str | None, str | None]:
    vocab = load_vocabulary()
    words = normalise(text).split()
    for phrase in vocab.verb_phrases:  # longest first
        verb = vocab.phrase_to_verb[phrase]
        spec = vocab.verbs.get(verb)
        if spec is None or spec.object != "book":
            continue
        pw = phrase.split()
        if words[: len(pw)] == pw:
            return verb, phrase
    return None, None


def recognises(text: str) -> str | None:
    """The book's sentence the text begins with (its verb), or None."""
    return _matched(text)[0]


def _after_phrase(text: str, phrase: str) -> str:
    """The words after the phrase, as said (case and quotes kept)."""
    said = " ".join(str(text).split())
    n = len(phrase.split())
    parts = said.split(" ")
    return " ".join(parts[n:]).strip()


def _title(rest: str, phrase: str) -> tuple[str, str]:
    """The title in quotes at the head of `rest` (or the words before a colon), and what
    follows it."""
    rest = rest.strip()
    if rest and rest[0] in _QUOTES:
        close = next((i for i in range(1, len(rest)) if rest[i] in _QUOTES), -1)
        if close < 0:
            raise OrderError(
                f'The book\'s title wants its closing quote: {phrase} "night orders": ...'
            )
        return rest[1:close].strip(), rest[close + 1 :].strip()
    head, colon, tail = rest.partition(":")
    if colon:
        return head.strip(), ":" + tail
    return rest, ""


def _starts_a_rule(line: str) -> bool:
    return line.lower().startswith("standing order") or _NAMED.match(line) is not None


def read_kind(ship: Any, lines: list[str]) -> tuple[str, list[str]]:
    """What a book's lines make it, and the lines as kept: a sheet (each line a standing
    order, read by the standing grammar), a manifest (each a bargain, read as the market
    reads one) or a note. OrderError in words for a sheet's or a manifest's line the ship
    cannot read."""
    if lines and _starts_a_rule(lines[0]):
        # a standing order's own `;` between its orders (`then take in the royals; take in
        # the topgallants`) is the order's: a segment that begins no new order is its tail
        merged: list[str] = []
        for seg in lines:
            if merged and not _starts_a_rule(seg):
                merged[-1] = f"{merged[-1]}; {seg}"
            else:
                merged.append(seg)
        lines = merged
    if lines and all(_BARGAIN.match(x) for x in lines):
        from freesail.orders import port

        kept = []
        for line in lines:
            verb = line.split()[0].lower()
            for words in port._bargains(line.split(None, 1)[1] if " " in line else ""):
                tons, good = port._tons_and_good(words, verb)
                kept.append(f"{verb} {tons:g} tons of {good}")
        return MANIFEST, kept
    sheet = []
    for line in lines:
        if line.lower().startswith("standing order"):
            sheet.append(line)
        elif _NAMED.match(line):
            sheet.append(f"standing order {line.strip()}")
        else:
            return NOTE, lines
    from freesail.standing import grammar as standing

    for line in sheet:
        try:
            standing.parse_standing(ship, line)
        except OrderError as e:
            raise OrderError(
                f"The sheet's line '{line}' is not a standing order the ship reads: {e}"
            ) from None
    return SHEET, sheet


def _who(ship: Any, world: Any) -> tuple[str, str]:
    """The drafter's or the poster's mark and rank, by the order's actor."""
    from freesail.world.movement import person_of_actor

    actor = str((getattr(ship, "extra", None) or {}).get("order_actor") or "captain")
    if actor.startswith(("standing order ", "captain's rule ")) or actor == "the director":
        raise OrderError("A book is drafted and posted by a person aboard, in his own hand.")
    person = person_of_actor(world, actor)
    if actor == "captain":
        captain = world.people.captain
        return captain.name, "captain"
    if person is None:
        who = actor.split(" (", 1)[0].removeprefix("the ")
        raise OrderError(
            f"Nobody is named at the {who}'s station: a book is drafted in a person's hand."
        )
    station = actor.split(" (", 1)[0].removeprefix("the ").strip()
    rank = ""
    held = (getattr(world, "agents", None) or {}).get(station)
    seat = getattr(world, "player_seat", None)
    if held is not None:
        rank = str(held.station.rank or "")
    elif seat is not None and seat.station.name == station:
        rank = str(seat.station.rank or "")
    if station == "captain":
        rank = "captain"
    return person.name, rank or "first lieutenant"


def _stamp(world: Any) -> str:
    clock = world.clock
    return f"{clock.ship_time:%d %B}, {units.time_stamp(clock.ship_time)}"


def handle(ship: Any, text: str) -> tuple[str, str, dict[str, Any]]:
    """Carry out a book's sentence for `orders.handle`."""
    from freesail.orders.prompt import world_of

    world = world_of(ship)
    if world is None:
        raise OrderError("There is no library aboard: the ship is not in a world.")
    verb, phrase = _matched(text)
    assert verb is not None and phrase is not None
    rest = _after_phrase(text, phrase)
    books = books_of(world)
    if verb == "the books":
        if rest.strip(" ."):
            raise OrderError(f"'the books' takes nothing after it; '{rest}' was not understood.")
        return "query.books", "\n".join(books.lines()), {"books": [b.title for b in books.items]}
    if verb == "draft a book":
        return _draft(ship, world, books, rest, phrase)
    title, after = _title(rest, phrase)
    if verb == "post the book" and phrase.endswith("night orders"):
        title, after = "night orders", rest
    if verb == "give the book" and phrase.endswith("manifest") and not title:
        title = "manifest"
    if not title:
        raise OrderError(f"Which book? Say '{verb} \"<its title>\"'; 'the books' lists them.")
    book = books.find(title)
    if book is None:
        have = ", ".join(f"'{b.title}'" for b in books.items) or "none yet"
        raise OrderError(f"There is no book '{title}' in the library; the books drafted: {have}.")
    if verb == "show the book":
        return "query.books", "\n".join(book.page()), {"book": book.title}
    if verb == "post the book":
        return _post(ship, world, book, after)
    return _give(ship, world, book, after)


def _draft(
    ship: Any, world: Any, books: Books, rest: str, phrase: str
) -> tuple[str, str, dict[str, Any]]:
    title, after = _title(rest, phrase)
    if not title or not after.startswith(":"):
        raise OrderError(
            "Draft what? Say 'draft a book \"night orders\": <its lines, with ; between them>'."
        )
    if books.find(title) is not None and books.find(title).key == _key(title):
        raise OrderError(
            f"There is a book '{title}' in the library already; give the new one another title."
        )
    lines = [" ".join(x.split()) for x in after[1:].split(";") if x.strip()]
    if not lines:
        raise OrderError(f"The book '{title}' wants some lines after the colon.")
    kind, kept = read_kind(ship, lines)
    mark, rank = _who(ship, world)
    stamp = _stamp(world)
    book = Book(title, kind, kept, mark, rank, world.clock.tick, stamp)
    books.items.append(book)
    n = len(kept)
    what = {SHEET: "order", MANIFEST: "bargain", NOTE: "line"}[kind]
    text = (
        f"{mark} drafted a book, '{title}': {_KIND_WORDS[kind]} of {n} {what}"
        f"{'s' if n != 1 else ''}, in the library with his mark."
    )
    return "book.drafted", text, {"title": title, "kind": kind, "mark": mark, "lines": list(kept)}


def _by_rank(line: str, rank: str) -> str:
    """The sheet's line given in the poster's rank: `by the <rank>` put in where it names
    none; a line naming another rank refused."""
    m = re.match(r'^\s*standing\s+order\s*(["“\'][^"”\']*["”\'])\s*(by\s+[^:]*?)?\s*:', line, re.I)
    if m is None:
        return line
    if m.group(2):
        said = " ".join(m.group(2).lower().split()).removeprefix("by ").removeprefix("the ")
        if said != rank:
            raise OrderError(
                f"The sheet's order {m.group(1)} is given by the {said}; it is posted in the "
                f"poster's own rank, the {rank}."
            )
        return line
    if rank == "captain":
        return line
    return f"{line[: m.end(1)]} by the {rank}{line[m.end(1) :]}"


def _post(ship: Any, world: Any, book: Book, after: str) -> tuple[str, str, dict[str, Any]]:
    """The sheet's orders made the standing orders, in the poster's rank."""
    from freesail.standing import grammar as standing

    if after.strip(" ."):
        raise OrderError(f"'post the book' takes the title alone; '{after}' was not understood.")
    if book.kind != SHEET:
        raise OrderError(
            f"'{book.title}' is {_KIND_WORDS[book.kind]}, not a sheet of standing orders; "
            "only a sheet is posted."
        )
    runtime = (getattr(ship, "extra", None) or {}).get("standing")
    if runtime is None:
        raise OrderError("This ship keeps no book of standing orders to post it in.")
    mark, rank = _who(ship, world)
    rules = []
    for line in book.lines:
        rule = standing.parse_standing(ship, _by_rank(line, rank), given_tick=world.clock.tick)
        old = runtime.book.get(rule.name)
        if old is not None and rank != "captain" and old.given_by != rank:
            raise OrderError(
                f"Standing order '{old.name}' is {old.officer}'s; the {rank} posts over his "
                "own orders only, and the sheet is not posted."
            )
        rules.append((rule, old))
    said = []
    for rule, old in rules:
        if old is not None:
            runtime.book.strike(old)
        _kind, words, _data = runtime.book.enter(rule)
        said.append(words.rstrip("."))
    book.posted = _stamp(world)
    book.by.append(mark)
    text = f"{mark} posted the sheet '{book.title}': " + "; ".join(said) + "."
    return (
        "book.posted",
        text,
        {
            "title": book.title,
            "names": [r.name for r, _ in rules],
            "replaced": [r.name for r, old in rules if old is not None],
            "given_by": rank,
        },
    )


def _give(ship: Any, world: Any, book: Book, after: str) -> tuple[str, str, dict[str, Any]]:
    """The manifest's bargains struck together and the boat sent once for them all."""
    from freesail.world import movement

    words = " ".join(after.lower().split()).strip(" .")
    if words and words not in ("to the boat", "to the boat's crew", "to the purser", "to boat"):
        raise OrderError(
            f"A manifest is given to the boat: 'give the book \"{book.title}\" to the boat'."
        )
    if book.kind != MANIFEST:
        raise OrderError(
            f"'{book.title}' is {_KIND_WORDS[book.kind]}, not a manifest; only a manifest is "
            "given to the boat."
        )
    movement.check(ship, "send the boat", "port")
    ports = getattr(world, "ports", None)
    if ports is None or not ports.ports:
        raise OrderError("There is no port to deal with: the ship is not in a world with a chart.")
    bargains = []
    for line in book.lines:
        verb, rest = line.split(None, 1)
        tons, good = rest.split(" tons of ", 1)
        bargains.append((verb, float(tons), good))
    mark = _who(ship, world)[0]
    text, data = ports.trade_list(bargains, said=f"By the manifest '{book.title}'")
    book.posted = _stamp(world)
    book.by.append(mark)
    return (
        "market.bargain",
        text,
        {"verb": "give the book", "level": 1, "title": book.title, "subjects": ["the boat"]} | data,
    )
