"""Orders, the imperative dialect: one line of text becomes one action on the ship.

    from freesail import orders
    ship.order_handler = orders.handle

`handle(ship, text)` is the whole interface. It parses the text against
this ship's vocabulary (`grammar.py`), finds the parts it names
(`resolve.py`), and carries it out through the verb table (`verbs.py`):
starting an evolution, moving a line, or setting a helm target. It returns
`(kind, log_text, data)` for the World to log, or raises `OrderError`
(`errors.py`) with a sentence saying what was understood, what was not,
and the nearest things that would have been.

Group evolutions ("make all sail", "shorten sail") are lists of ordinary
orders in `data/vocabulary.yaml`; `handle` runs each in turn, passing over
the ones this ship has no parts for, and reports the rest on one line.
"""

from __future__ import annotations

from typing import Any

from freesail.evolutions.runner import gerund
from freesail.orders import errors, verbs
from freesail.orders.errors import (
    AmbiguousNounError,
    NothingToDoError,
    OrderError,
    UnknownNounError,
)
from freesail.orders.grammar import Order, parse
from freesail.orders.resolve import Resolution, build_noun_table, noun_table
from freesail.orders.resolve import resolve as resolve_noun
from freesail.orders.vocabulary import Vocabulary, load_vocabulary
from freesail.ship.graph import Ship

__all__ = [
    "AmbiguousNounError",
    "NothingToDoError",
    "Order",
    "OrderError",
    "Resolution",
    "UnknownNounError",
    "Vocabulary",
    "build_noun_table",
    "handle",
    "load_vocabulary",
    "noun_table",
    "parse",
    "resolve_noun",
]


def handle(ship: Ship, text: str) -> tuple[str, str, dict[str, Any]]:
    """Carry out one order. Matches `Ship.order_handler`; raises OrderError."""
    vocab = load_vocabulary()
    order = parse(ship, text, vocab)
    if order.verb in vocab.group_evolutions:
        return _group_evolution(ship, order, vocab)
    return verbs.execute(ship, order, vocab)


def _group_evolution(
    ship: Ship, order: Order, vocab: Vocabulary
) -> tuple[str, str, dict[str, Any]]:
    """Run the orders listed for a group evolution, one after another.

    An order naming a part this ship does not have is passed over (a
    schooner has no royals to set). One that fails for another reason is
    reported. If nothing at all could be started, the order is rejected.
    """
    done: list[dict[str, Any]] = []
    texts: list[str] = []
    failed: list[str] = []
    ordered: set[str] = set()  # subjects already given an order by an earlier line
    # the work in words, for the one line the runner writes if the group must wait for
    # hands: "setting plain sail"
    first, _, rest = order.verb.partition(" ")
    group = f"{gerund(first)} {rest}".strip()
    for line in vocab.group_evolutions[order.verb]:
        try:
            sub = parse(ship, line, vocab)
        except UnknownNounError:
            continue
        except OrderError as e:
            failed.append(f"'{line}': {e}")
            continue
        if sub.verb in vocab.group_evolutions:
            raise OrderError(
                f"The group evolution '{order.verb}' lists '{line}', which is itself a group "
                f"evolution; vocabulary.yaml must list plain orders."
            )
        if "hands_from" in order.modifiers:
            sub.modifiers["hands_from"] = order.modifiers["hands_from"]
        try:
            kind, text, data = verbs.execute(ship, sub, vocab, frozenset(ordered), group)
        except (UnknownNounError, NothingToDoError):
            continue
        except OrderError as e:
            failed.append(f"'{line}': {e}")
            continue
        done.append({"order": line, "kind": kind, "data": data})
        texts.append(text)
        ordered.update(data.get("subjects", []))
        ordered.update(data.get("failed_subjects", []))
    if not done:
        detail = errors.sentence_list(failed) or "there is nothing in this ship it applies to"
        raise OrderError(f"Could not {order.verb}: {detail}.")
    text = f"{order.verb[0].upper()}{order.verb[1:]}: " + " ".join(texts)
    if failed:
        text += " Not done: " + errors.sentence_list(failed) + "."
    data = {
        "verb": order.verb,
        "level": 1,
        "group": True,
        "orders": done,
        "subjects": [s for d in done for s in d["data"].get("subjects", [])],
        "failed": failed,
    }
    return "evolution.started", text, data
