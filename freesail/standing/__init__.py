"""Standing orders (spec M4 part 4a): the standing dialect, its rules, the runtime, the book.

    standing order "night routine": at sunset then take in the studdingsails; take in the royals

The pieces, and the seams the later packages use:

- `rules.py`: `Rule`, `Trigger`, `Condition`, `Clause`, `Comparison`, the ranks and
  `STANDING_DWELL_S`. Package 26's Python API builds a `Rule` from the same pieces.
- `grammar.py`: `parse_standing(ship, text)` for the sentence; `parse_condition(text,
  ship)` for a condition alone (the string in `@when`); `recognises(text)` for the
  router in `orders.handle`.
- `runtime.py`: `Runtime(world)`, evaluated by `World.tick`; the book lives on it.
- `book.py`: `Book`, `read_orders_file`.

The readings a rule tests are the registry's (`freesail.api.readings`): the same ones
the client's snapshot shows and an agent asks for.
"""

from __future__ import annotations

from freesail.standing.book import Book, read_orders_file
from freesail.standing.grammar import (
    parse_condition,
    parse_duration,
    parse_standing,
    recognises,
)
from freesail.standing.rules import (
    RANKS,
    STANDING_DWELL_S,
    Clause,
    Comparison,
    Condition,
    Rule,
    Trigger,
)
from freesail.standing.runtime import ACTOR_PREFIX, Runtime

__all__ = [
    "ACTOR_PREFIX",
    "RANKS",
    "STANDING_DWELL_S",
    "Book",
    "Clause",
    "Comparison",
    "Condition",
    "Rule",
    "Runtime",
    "Trigger",
    "parse_condition",
    "parse_duration",
    "parse_standing",
    "read_orders_file",
    "recognises",
]
