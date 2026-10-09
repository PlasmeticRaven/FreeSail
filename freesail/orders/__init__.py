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

A reading asked at the prompt (`the reckoning`, `what is the glass`, a sail by its name;
package 33c) is a query answered in the registry's words by `prompt.py`.
"""

from __future__ import annotations

from typing import Any

from freesail.evolutions.runner import gerund
from freesail.orders import errors, prompt, verbs
from freesail.orders.errors import (
    AmbiguousNounError,
    NothingToDoError,
    OrderError,
    UnknownNounError,
    UnknownVerbError,
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
    "read_whole",
    "resolve_noun",
]


def handle(ship: Ship, text: str) -> tuple[str, str, dict[str, Any]]:
    """Carry out one order. Matches `Ship.order_handler`; raises OrderError.

    A sentence of the standing dialect (`standing order "x": ...` and the book's orders,
    spec M4 §3) is handed to `freesail.standing.grammar`, which reads the trigger and the
    condition and parses the orders after `then` with this grammar at give time. A
    sentence to an agent's station (spec M4 §12) is handed to `freesail.orders.stations`.
    """
    from freesail.orders import stations
    from freesail.standing import grammar as standing
    from freesail.world import orders as world_channel

    if world_channel.recognises(text):
        # a world order at the captain's prompt (spec M5 §26, truth 71; package 36): the
        # channel is the scenario's and the director's, never the captain's grammar's;
        # refused in the vocabulary's words
        raise OrderError(load_vocabulary().world_order_refusal or world_channel.REFUSAL)
    if standing.recognises(text):
        return standing.handle(ship, text)
    book = standing.bare_book_sentence(ship, text)
    if book is not None:
        # `belay "blind lead"`: a standing order by its name, without the words
        # 'standing order' (package 33c)
        return standing.handle(ship, book)
    if stations.recognises(text, ship):
        # a sentence to an agent's station (spec M4 §12): `ask the watcher ...`, `stand
        # down the watcher`, `resume the watcher`, `show the watcher's journal`
        return stations.handle(ship, text)
    vocab = load_vocabulary()
    refused = vocab.refused(text)
    if refused is not None:
        # words the ship does not take, refused with what to say instead or with the
        # milestone they belong to (package 37l; `refused_phrases` in the vocabulary)
        raise OrderError(refused)
    try:
        order = parse(ship, text, vocab)
    except UnknownVerbError:
        # no verb in the words: a reading said without its article, a sail or a part by
        # name, or an absent reading (package 33c, `orders.prompt`); else the refusal
        answered = prompt.answer_unparsed(ship, text, vocab)
        if answered is None:
            raise
        return answered
    except UnknownNounError:
        # 'take in twenty tons of water', 'take in provisions for thirty days': the sail
        # verb's words with no sail in them, the port's business (package 35)
        stores = _stores_order(text)
        if stores is None:
            raise
        order = stores
    if order.verb in vocab.readings:
        # a reading asked at the prompt (package 33c): a query, in the registry's words
        return prompt.answer(ship, order, text, vocab)
    runner = ship.extra.get("evolutions") if hasattr(ship, "extra") else None
    giving = getattr(runner, "giving", None)
    if giving is None:
        return _carry_out(ship, order, vocab)
    with giving(text):  # its evolutions carry the order's number, for `belay that`
        return _carry_out(ship, order, vocab)


def read_whole(ship: Ship, text: str, vocab: Vocabulary | None = None) -> Order:
    """Read an order whole without carrying it out (package 37l; the review of gate 5c's
    playtests, G9: a standing order's action had its first word read when it was given
    and no more, so that `take a fix as soon as a bearing can be taken` was entered and
    refused at every change of the watch). The words are parsed, and then read as the
    order's own reader reads them: a sail, a yard or a line by its name (ambiguous or
    unknown, refused); a mark, the marks of a fix, a place or a position
    (`navigation.check`); an anchor, its fathoms and its course (`ground_tackle.check`); a
    person (`people.check`); tons, days and hands (`port.check`). What depends on the
    moment (what is in sight, an anchor down, the hands, the port) is left to the order
    when it is carried out. Returns the order; raises OrderError in words."""
    vocab = vocab or load_vocabulary()
    refused = vocab.refused(text)
    if refused is not None:
        raise OrderError(refused)
    order = parse(ship, text, vocab)
    if order.verb in vocab.group_evolutions or order.verb in vocab.readings:
        return order
    kind = vocab.verbs[order.verb].object
    if kind == "navigation":
        from freesail.orders import navigation

        navigation.check(ship, order)
    elif kind == "anchor":
        from freesail.orders import ground_tackle

        ground_tackle.check(ship, order)
    elif kind == "person":
        from freesail.orders import people

        people.check(ship, order)
    elif kind == "port":
        from freesail.orders import port

        port.check(ship, order)
    elif kind in ("sail", "yards", "line", "wreck") and order.object:
        try:
            resolve_noun(ship, order.object, order.side_word, order.verb)
        except (AmbiguousNounError, UnknownNounError):
            raise
        except OrderError:
            pass  # a refusal of the moment (the tack for 'weather'), not of the words
    return order


def _carry_out(ship: Ship, order: Order, vocab: Vocabulary) -> tuple[str, str, dict[str, Any]]:
    if order.verb in vocab.group_evolutions:
        return _group_evolution(ship, order, vocab)
    if vocab.verbs[order.verb].object == "navigation":
        # what the captain says to the master (spec M5 §15, package 33a)
        from freesail.orders import navigation

        if order.object and order.verb in LEAD_VERBS:
            # "sound the well" (package 33c): the well is a reading the ship has not got
            # yet, and the registry says so; the lead is not hove for it
            absent = prompt.absent_named(order.object)
            if absent is not None:
                raise OrderError(absent)
        return navigation.execute(ship, order)
    if vocab.verbs[order.verb].object == "anchor":
        # the ground tackle's orders (spec M5 §18, package 34), and the port's evolutions
        # on it (package 35: get under way, moor, unmoor, lay out a kedge)
        from freesail.orders import ground_tackle

        return ground_tackle.execute(ship, order)
    if vocab.verbs[order.verb].object == "person":
        # the people's orders (spec M5 §22, package 35)
        from freesail.orders import people

        return people.execute(ship, order)
    if vocab.verbs[order.verb].object == "port":
        # the port's orders (spec M5 §23, package 35)
        from freesail.orders import port

        return port.execute(ship, order)
    if order.verb == "set" and ("reefs" in order.modifiers or "close" in order.modifiers):
        return _set_reefed(ship, order, vocab)
    return verbs.execute(ship, order, vocab)


def _stores_order(text: str) -> Order | None:
    """'take in twenty tons of water' as the port's `take in water` with the words after
    the verb as said, or None when the words are not the stores'."""
    low = " ".join(text.lower().split())
    if not low.startswith("take in "):
        return None
    rest = low.removeprefix("take in ").strip()
    words = rest.split()
    if "water sail" in rest:
        return None  # a sail, not the stores (package 37l)
    if any(w in ("water",) for w in words):
        verb = "take in water"
    elif any(w in ("provisions", "provision") for w in words):
        verb = "take in provisions"
    else:
        return None
    return Order(text=low, verb=verb, verb_phrase="take in", object=rest)


# The navigation verbs that heave a lead (`data/vocabulary.yaml`).
LEAD_VERBS: tuple[str, ...] = ("heave the lead", "heave the deep sea lead")


def _set_reefed(ship: Ship, order: Order, vocab: Vocabulary) -> tuple[str, str, dict[str, Any]]:
    """`set the mainsail, one reef` (package 33c; playtest 13's cutter): the sail set and
    then reefed, two evolutions in turn on the one sail, as the runner takes two orders on
    one subject (a reef wants the sail set, and waits its turn behind the setting). A
    sail with no reef bands is set and the line says it was not reefed, and why."""
    reef_mods = {k: v for k, v in order.modifiers.items() if k in ("reefs", "close", "hands_from")}
    set_mods = {k: v for k, v in order.modifiers.items() if k not in ("reefs", "close")}
    as_set = Order(order.text, "set", "set", order.object, order.side_word, set_mods)
    as_reef = Order(order.text, "reef", "reef", order.object, order.side_word, reef_mods)
    kind, set_text, set_data = verbs.execute(ship, as_set, vocab)
    try:
        _, reef_text, reef_data = verbs.execute(ship, as_reef, vocab)
    except OrderError as e:
        return kind, f"{set_text} Not reefed: {str(e).rstrip('.')}.", set_data | {"reef": str(e)}
    data = {
        "verb": "set",
        "level": 1,
        "orders": [set_data, reef_data],
        "subjects": list(set_data.get("subjects", [])),
        "failed": list(set_data.get("failed", [])) + list(reef_data.get("failed", [])),
    }
    return kind, f"{set_text} {reef_text}", data


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
