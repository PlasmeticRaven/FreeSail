"""The port's orders (spec M5 §23; package 35): the boat, the market, the yard and the
crew pool, in port.

    send the boat ashore [with the purser | with <person> | with a letter]
                                    the boat away to the quay and back with the prices,
                                    the letters waiting and whoever went
    buy <n> tons of <good>          at the port's price now; the boat brings it off
    sell <n> tons of <good>         the goods landed by the boat; the purse credited
    demand <item> from the yard     a spar, a suit of sails, cordage: the yard's job with
                                    its time and cost
    take in water [<n> tons]        the water completed from the quay or the yard
    take in provisions [for <n> days]
    enter <n> <rating> seamen       hands from the pool at a bounty, come off after a delay

Each is a verb of `data/vocabulary.yaml` with the object `port`: the grammar takes the
words after the verb as they are, and this module reads a number, a good, an item or a
rating from them and hands the order to the World's ports (`freesail.world.ports.Ports`),
which refuse in words when she is not in port, the prices are not known, the boat is
away, the hold is full or the purse short.
"""

from __future__ import annotations

import re
from typing import Any

from freesail.orders.errors import OrderError
from freesail.orders.grammar import Order
from freesail.orders.prompt import world_of

__all__ = ["NO_PORTS_WORDS", "execute", "number_in"]

NO_PORTS_WORDS = "There is no port to deal with: the ship is not in a world with a chart."

Result = tuple[str, str, dict[str, Any]]

_NUMBER_WORDS = {
    "a": 1,
    "an": 1,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "fifteen": 15,
    "twenty": 20,
    "twenty five": 25,
    "thirty": 30,
    "forty": 40,
    "fifty": 50,
    "sixty": 60,
    "eighty": 80,
    "a hundred": 100,
    "two hundred": 200,
    "three hundred": 300,
    "seventy": 70,
    "ninety": 90,
    "hundred": 100,
}


def number_in(text: str) -> tuple[float | None, str]:
    """A number in the words (digits or words), and the words without it."""
    low = " ".join(text.lower().split())
    m = re.search(r"\b(\d+(?:\.\d+)?)\b", low)
    if m:
        return float(m.group(1)), (low[: m.start()] + " " + low[m.end() :]).strip()
    for words, n in sorted(_NUMBER_WORDS.items(), key=lambda kv: -len(kv[0])):
        if re.search(rf"\b{words}\b", low):
            return float(n), re.sub(rf"\b{words}\b", " ", low, count=1).strip()
    return None, low


def _ports(ship: Any) -> Any:
    world = world_of(ship)
    ports = getattr(world, "ports", None) if world is not None else None
    if ports is None or not ports.ports:
        raise OrderError(NO_PORTS_WORDS)
    return ports


def _yard_item(ports: Any, rest: str) -> str | None:
    """The yard's item named in the words, if the port she lies in supplies it."""
    port = ports.in_port()
    if port is None:
        return None
    words = re.sub(r"\b(from|the|yard|chandlers|a|an|spare)\b", " ", rest.lower())
    words = " ".join(words.split())
    return words if words and port.dockyard.find(words) is not None else None


def _tons_and_good(rest: str, verb: str) -> tuple[float, str]:
    n, left = number_in(rest)
    if n is None:
        raise OrderError(f"How many tons? Say '{verb} twenty tons of tin'.")
    left = re.sub(r"\b(tons?|of|the)\b", " ", left)
    good = " ".join(left.split())
    if not good:
        raise OrderError(f"{verb.capitalize()} what? Say '{verb} twenty tons of tin'.")
    return n, good


def execute(ship: Any, order: Order) -> Result:
    """Carry out a port order. The verb is the vocabulary's key."""
    verb = order.verb
    rest = (order.object or "").strip()
    ports = _ports(ship)
    if verb == "send the boat":
        phrase = order.verb_phrase
        words = rest
        for lead in ("with the", "with", "for"):
            if phrase.endswith(" " + lead):
                words = f"{lead} {rest}"
                break
        text, data = ports.send_boat(words)
        return (
            "evolution.started",
            text,
            {"verb": verb, "level": 1, "subjects": ["the boat"]} | data,
        )
    if verb == "buy" and _yard_item(ports, rest) is not None:
        # 'buy a suit of sails', 'buy a topmast from the chandlers': the yard's business
        text, data = ports.demand(_yard_item(ports, rest), None)
        return "yard.demanded", text, {"verb": verb, "level": 1} | data
    if verb == "buy" and re.search(
        r"\b(chandlers|yard|sails?|spars?|topmast|cordage)\b", rest.lower()
    ):
        # the yard's kind of thing at a port whose yard has none of it: the yard's refusal,
        # naming what it supplies, not the market's with the words garbled (35b's finding)
        words = re.sub(r"\b(from|the|yard|chandlers|a|an|spare)\b", " ", rest.lower())
        text, data = ports.demand(" ".join(words.split()), None)
        return "yard.demanded", text, {"verb": verb, "level": 1} | data
    if verb in ("buy", "sell"):
        tons, good = _tons_and_good(rest, verb)
        text, data = ports.trade(verb, tons, good)
        return "market.bargain", text, {"verb": verb, "level": 1} | data
    if verb == "demand":
        words = re.sub(r"\b(from|the|yard|chandlers|a|an|spare)\b", " ", rest.lower())
        words = " ".join(words.split())
        if not words:
            raise OrderError("Demand what? Say 'demand a topmast from the yard'.")
        n, left = number_in(words)
        item = left if n is not None else words
        if n is not None and ("water" in item or "provision" in item):
            text, data = ports.demand(item, n)
        else:
            text, data = ports.demand(item, None)
        return "yard.demanded", text, {"verb": verb, "level": 1} | data
    if verb == "take in water":
        n, _ = number_in(rest)
        if n is None:
            # 'take in water' alone completes her water to the ship file's allowance
            stores = getattr(world_of(ship), "stores", None)
            spec = getattr(getattr(ship, "spec", None), "crew", None)
            full = float(getattr(getattr(spec, "stores", None), "water_tons", 0.0) or 0.0)
            have = stores.water_tons if stores is not None else 0.0
            if full and have >= full - 0.5 and ports.in_port() is not None:
                raise OrderError(
                    f"Her water is complete: {have:g} tons in the ground tier. Say 'take in "
                    f"twenty tons of water' to stow more."
                )
            n = full - have if full else 10.0
        text, data = ports.demand("water", n)
        return "yard.demanded", text, {"verb": verb, "level": 1} | data
    if verb == "take in provisions":
        n, _ = number_in(rest)
        if n is None:
            n = 30.0
        text, data = ports.demand("provisions", n)
        return "yard.demanded", text, {"verb": verb, "level": 1} | data
    if verb == "enter":
        n, left = number_in(rest)
        if n is None:
            raise OrderError("Enter how many? Say 'enter six able seamen'.")
        rating = " ".join(
            w for w in left.split() if w not in ("hands", "men", "seamen", "seaman", "the")
        )
        if not rating:
            rating = "ordinary"
        text, data = ports.enter_hands(int(n), rating)
        return "crew.entering", text, {"verb": verb, "level": 1} | data
    raise OrderError(f"'{verb}' is not a port order this ship knows.")
