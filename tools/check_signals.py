"""Check every signal root under data/signals/ (spec M7 §3; package 76, step 6;
docs/design/Design-Signals.md, "As built out").

    python tools/check_signals.py            every root
    python tools/check_signals.py spain      the roots named

A root passes when 71's loader reads it (its six books present, every book's numbers unique,
its hoist form one the engine knows) and its seventh file, colours.yaml, loads (81's place
words, the occasions' flags named in the file); when every entry's `does` is an order a ship
takes or a form 71's design names, a state, an answer, `closer`, `release` or `news`; when every
qualifier is one the engine fills, and an order's blanks are among them; when every entry
names its source, and an entry whose source calls itself made is marked made and an entry not
marked made cites a page of the period; when the private form draws a table and names roles
the captains have; and when every nation whose line names the root reads it under her own
name. Prints each failure in words; exits 1 when there is one. The same as a test
parametrized over the roots (`tests/test_signals.py`), so a root added later is checked by
tests that do not know its name.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DOES_KEYS = {"order", "state", "news", "answer", "closer", "release"}
STATES = {"chasing", "engaging", "on passage", "investigating a stranger"}
ANSWERS = {"affirmative", "negative", "not understood", "cannot comply", "annulled"}
QUALIFIERS = {"compass", "number", "ship", "place"}  # what `signals._qualifiers` fills
# the orders 71's design names that the far body performs itself (`signals.far_perform`):
# keeping company with the commodore, and the reefs shaken out (the dialect's words for the
# near body are 'shake out the reefs in the topsails'; found by package 76 and reported)
DESIGN_ORDERS = {"close the flag", "shake out the reefs"}
# the blanks an order may carry, filled from the qualifier of the same name (`signals.order_of`)
BLANKS = {
    "{compass}": ("compass", "NW"),
    "{place}": ("place", "Falmouth"),
    "{number}": ("number", "3"),
}
PERIOD = re.compile(r"\b1[78]\d\d\b")
# a source that calls its entry made ('made', '...; made', 'the number made', 'the cell made'),
# and not a quotation's 'made sail'
CALLS_ITSELF_MADE = re.compile(
    r"(?:^made\b|;\s*made\b|\bthe (?:cell|cells|number|numbers|hoist|hoists) made\b|\bmade$)"
)


def _a_ship() -> Any:
    """A frigate to parse the orders against: some verbs read her gear (the reefs, the
    studding sails), which a frigate has and a cutter has not."""
    from freesail.api.session import make_world
    from freesail.core.world import Scenario

    world = make_world(7, "data/ships/frigate-36.yaml", Scenario())
    return world.ship


def _order_ok(ship: Any, text: str, cache: dict[str, str | None]) -> str | None:
    """None when the order is one a ship takes or a design's form; else why not."""
    if text in DESIGN_ORDERS:
        return None
    if text in cache:
        return cache[text]
    from freesail.orders.grammar import parse

    filled = text
    for blank, (_q, sample) in BLANKS.items():
        filled = filled.replace(blank, sample)
    why = None
    try:
        parse(ship, filled)
    except Exception as e:  # noqa: BLE001 - the dialect's refusal is the finding
        why = f"'{text}' is no order a ship takes ({e})"
    cache[text] = why
    return why


def check_root(
    root: str, ship: Any = None, cache: dict[str, str | None] | None = None
) -> list[str]:
    """The failures of one root, each a sentence; [] when it passes."""
    from freesail.world import flags as F
    from freesail.world import signals as S
    from freesail.world.captains import ROLES
    from freesail.world.nations import load_nations

    out: list[str] = []
    cache = {} if cache is None else cache
    try:
        books = S.load_books(root)
    except S.BookFileError as e:
        return [f"{root}: {e}"]
    try:
        F.load_colours(root)
    except S.BookFileError as e:
        out.append(f"{root}: {e}")
    if ship is None:
        ship = _a_ship()
    for book in ("numerary", "night", "fog", "convoy"):
        for e in books.book(book):
            where = f"{root}, {book}, '{e.meaning}'"
            extra = set(e.does) - DOES_KEYS
            if extra:
                out.append(f"{where}: `does` names {sorted(extra)}, none of {sorted(DOES_KEYS)}")
            if "state" in e.does and e.does["state"] not in STATES:
                out.append(f"{where}: the state '{e.does['state']}' is none the captain takes")
            if "answer" in e.does and e.does["answer"] not in ANSWERS:
                out.append(f"{where}: the answer '{e.does['answer']}' is none the engine reads")
            if "order" in e.does:
                text = str(e.does["order"])
                why = _order_ok(ship, text, cache)
                if why:
                    out.append(f"{where}: {why}")
                for blank, (q, _sample) in BLANKS.items():
                    if blank in text and q not in e.qualifiers:
                        out.append(f"{where}: the order's {blank} wants the qualifier '{q}'")
            bad = set(e.qualifiers) - QUALIFIERS
            if bad:
                out.append(f"{where}: qualifiers {sorted(bad)} are none the engine fills")
            if not e.source:
                out.append(f"{where}: no source named")
            elif CALLS_ITSELF_MADE.search(e.source) and not e.made:
                out.append(f"{where}: the source calls it made and it is not marked made")
            elif not e.made and not PERIOD.search(e.source):
                out.append(f"{where}: not marked made, and its source cites no page of the period")
            if book in ("numerary", "convoy") and e.number is None:
                out.append(f"{where}: a numbered book's entry with no number")
    form = books.private_form or {}
    for light in ("day", "night"):
        part = form.get(light) or {}
        if not part.get("challenge") or not part.get("reply"):
            out.append(f"{root}, private: no {light} challenge and reply")
    roles = set(books.carried_by) - set(ROLES)
    if roles:
        out.append(
            f"{root}, private: carried_by names {sorted(roles)}, none of the captains' roles"
        )
    if books.telegraph and not books.words:
        out.append(f"{root}: the telegraph flag declared and no dictionary")
    for n in load_nations().nations.values():
        if n.signals_root == root and root != "basic":
            if books.nation != n.id:
                out.append(f"{root}: {n.id} reads it, and it declares the nation '{books.nation}'")
    return out


def main(argv: list[str]) -> int:
    from freesail.world import signals as S

    roots = argv or S.roots()
    ship = _a_ship()
    cache: dict[str, str | None] = {}
    failed = 0
    for root in roots:
        problems = check_root(root, ship, cache)
        books = S.load_books(root) if not problems or "load" not in problems[0] else None
        if problems:
            failed += 1
            print(f"{root}: {len(problems)} failure(s)")
            for p in problems:
                print(f"  {p}")
        elif books is not None:
            made = sum(1 for e in books.numerary if e.made)
            n = len(books.numerary)
            print(
                f"{root}: passes ({books.system}, {books.hoist_form}; numerary {n} entries, "
                f"{made} made; night {len(books.night)}, fog {len(books.fog)}, convoy "
                f"{len(books.convoy)}; {len(books.words)} words)"
            )
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
