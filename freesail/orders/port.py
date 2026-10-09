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
    take the pilot                  the answer to the pilot boat's hail (package 37h): she
                                    shortens sail or heaves to as the hail asked, and he
                                    boards when the boat can put him aboard
    decline the pilot               the boat sent back to her station (`we need no pilot`)
    hail the pilot                  a pilot's boat in sight hailed, and the pilot taken

Each is a verb of `data/vocabulary.yaml` with the object `port`: the grammar takes the
words after the verb as they are, and this module reads a number, a good, an item or a
rating from them and hands the order to the World's ports (`freesail.world.ports.Ports`),
which refuse in words when she is not in port, the prices are not known, the boat is
away, the hold is full or the purse short.
"""

from __future__ import annotations

import re
from typing import Any

from freesail.orders import numbers
from freesail.orders.errors import OrderError
from freesail.orders.grammar import Order
from freesail.orders.prompt import world_of

__all__ = ["NO_PORTS_WORDS", "PILOT_VERBS", "check", "execute", "number_in"]

NO_PORTS_WORDS = "There is no port to deal with: the ship is not in a world with a chart."

Result = tuple[str, str, dict[str, Any]]

# The pilot's orders (package 37h), the port's business as the boat and the market are
PILOT_VERBS = ("take the pilot", "decline the pilot", "hail the pilot")


def number_in(text: str) -> tuple[float | None, str]:
    """A number in the words (figures or words, by the one reader for numbers,
    `orders.numbers`; package 37l), and the words without it."""
    return numbers.number_in(text)


# The provisions' time in the words (package 37l: `take in provisions for sixteen days`
# was read as no number and took thirty): days, weeks or months, a month thirty days.
_DAYS_IN = {"day": 1, "days": 1, "week": 7, "weeks": 7, "month": 30, "months": 30}


def _days(rest: str) -> float | None:
    """How many days of provisions the words ask for ('for sixteen days', 'for a month',
    'six weeks', '30'); None when they say none; refused in words they cannot be read."""
    words = [w for w in rest.lower().replace("-", " ").split() if w not in ("for", "the", "of")]
    if not words:
        return None
    got = numbers.read(words, 0)
    if got is not None:
        n, used = got
        unit = words[used : used + 1]
        if not unit and used == len(words):
            return n
        if unit and unit[0] in _DAYS_IN and used + 1 == len(words):
            return n * _DAYS_IN[unit[0]]
    raise OrderError(
        f"'{rest.strip()}' is not a time to provision for; say 'take in provisions for "
        "thirty days', 'for six weeks' or 'for a month'."
    )


def _bargains(rest: str) -> list[str]:
    """The words of a buying or a selling as one bargain or several ('20 tons of salt
    fish and 8 tons of pilchards': two; package 37l, game 10, where it was one cargo
    named "salt fish and 8 pilchards"): split at each 'and' that a number of tons
    follows."""
    words = rest.split()
    low = [w.lower() for w in words]
    parts: list[list[str]] = [[]]
    for k, w in enumerate(words):
        if low[k] == "and" and parts[-1]:
            got = numbers.read(low, k + 1)
            if got is not None and low[k + 1 + got[1] : k + 2 + got[1]] in (["ton"], ["tons"]):
                parts.append([])
                continue
        parts[-1].append(w)
    return [" ".join(p) for p in parts if p]


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
    if verb in PILOT_VERBS:
        # package 37h: the answer to the pilot's hail; she shortens sail or heaves to as
        # the hail asked when she is still too fast for him to board
        text, data, wants = ports.answer_pilot(verb)
        if wants:
            from freesail import orders

            try:
                orders.handle(ship, wants)
            except OrderError as e:
                text += f" ('{wants}' not carried out: {e})"
        return "port.pilot_answered", text, {"verb": verb, "level": 1} | data
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
        bargains = _bargains(rest)
        if len(bargains) == 1:
            tons, good = _tons_and_good(rest, verb)
            text, data = ports.trade(verb, tons, good)
            return "market.bargain", text, {"verb": verb, "level": 1} | data
        # several bargains in one order (package 37l): read whole, weighed together, and
        # struck together, the boat sent once for them all
        read = [_tons_and_good(words, verb) for words in bargains]
        text, data = ports.trade_together(verb, read)
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
        n = _days(rest)
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


def check(ship: Any, order: Order) -> None:
    """Read a port order whole without carrying it out (package 37l): its tons and its
    goods, its days of provisions, its hands; whether she is in port, the prices and the
    purse are the order's own business when it fires."""
    verb = order.verb
    rest = (order.object or "").strip()
    if verb in ("buy", "sell") and not re.search(
        r"\b(chandlers|yard|sails?|spars?|topmast|cordage)\b", rest.lower()
    ):
        for words in _bargains(rest):
            _tons_and_good(words, verb)
    elif verb == "take in provisions":
        _days(rest)
    elif verb == "enter":
        n, _ = number_in(rest)
        if n is None:
            raise OrderError("Enter how many? Say 'enter six able seamen'.")
