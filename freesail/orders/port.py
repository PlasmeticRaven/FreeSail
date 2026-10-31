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
    take in powder and shot         the magazine completed, of the Ordnance or the merchants
                                    (practice and resupply, between packages 72 and 73;
                                    `orders.ordnance`); `buy` and `demand` whose words name
                                    powder or shot are the same order's
    take the pilot                  the answer to the pilot boat's hail (package 37h): she
                                    shortens sail or heaves to as the hail asked, and he
                                    boards when the boat can put him aboard
    decline the pilot               the boat sent back to her station (`we need no pilot`)
    hail the pilot                  a pilot's boat in sight hailed, and the pilot taken

Each is a verb of `data/vocabulary.yaml` with the object `port`: the grammar takes the
words after the verb as they are, and this module reads a number, a good, an item or a
rating from them and hands the order to the World's ports (`freesail.world.dealings.Dealings`),
which refuse in words when she is not in port, the prices are not known, the boat is
away, the hold is full or the purse short.
"""

from __future__ import annotations

import re
from typing import Any

from freesail.orders import numbers
from freesail.orders import ordnance as ordnance_orders
from freesail.orders.errors import OrderError
from freesail.orders.grammar import Order
from freesail.orders.prompt import world_of

__all__ = ["CONN_VERBS", "NO_PORTS_WORDS", "PILOT_VERBS", "check", "execute", "number_in"]

NO_PORTS_WORDS = "There is no port to deal with: the ship is not in a world with a chart."

Result = tuple[str, str, dict[str, Any]]

# The pilot's orders (package 37h), the port's business as the boat and the market are
PILOT_VERBS = ("take the pilot", "decline the pilot", "hail the pilot")
# The pilot's conn (package 45): given, and taken back
CONN_VERBS = ("let the pilot take her in", "let the pilot take her out", "i have the conn")


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
    ports = getattr(world, "dealings", None) if world is not None else None
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


_TO_SHIP = re.compile(
    r"^(?:(?P<with>with\s+(?:the\s+)?)?(?P<before>.*?)\s+)?(?:to|aboard|alongside)\s+"
    r"(?:the\s+)?(?P<ship>[\w' -]+?)(?:\s+with\s+(?P<carry>.+?))?(?:\s+for\s+(?P<fetch>.+?))?\s*$",
    re.I,
)


def _boat_to_ship(world: Any, phrase: str, rest: str) -> tuple[Any, list[Any], list[Any]] | None:
    """`send the boat to the <ship> [with <persons>] [for <persons>]` (package 82): the
    hull named, the persons of this company she carries and the persons of hers she is
    sent for; None when the words name no ship on the sea (the shore's errands then)."""
    from freesail.world.movement import hull_of
    from freesail.world.orders import WorldOrderError, hull_named

    text = " ".join(f"{phrase} {rest}".split())
    for lead in ("send the boat ashore", "send a boat ashore", "send the boat", "send a boat"):
        if text.lower().startswith(lead):
            text = text[len(lead) :].strip()
            break
    m = _TO_SHIP.match(text)
    if m is None or not m.group("ship"):
        return None
    name = m.group("ship").strip()
    low = name.lower()
    if low in ("shore", "quay", "port", "yard", "market") or low.startswith(("shore ", "quay ")):
        return None
    # the hull named, made only when the boat goes (the lead's finding on step 1: a refused
    # order left a far body promoted for nothing): a ship with no hull yet is measured by
    # her far body and refused beyond a boat's pull before any hull is made
    try:
        target = hull_named(world, name, make=False)
    except WorldOrderError as e:
        if "no hull of her own yet" not in str(e):
            return None
        from freesail import units
        from freesail.world.geo import bearing_and_distance, distance_words
        from freesail.world.movement import BOAT_BETWEEN_NM

        vessel = world.vessels.find(name.strip('"'))
        here = getattr(world, "position", None)
        if vessel is None or here is None:
            return None
        metres = bearing_and_distance(here, vessel.position)[1]
        if metres / units.NAUTICAL_MILE > BOAT_BETWEEN_NM:
            raise OrderError(
                f"The {vessel.name} is {distance_words(metres)} off, beyond a boat's pull "
                f"({BOAT_BETWEEN_NM:g} mile); close her first."
            ) from None
        target = hull_named(world, name)  # within reach: her hull made as the boat goes
    if target is world or target is getattr(world, "own", None):
        raise OrderError("The boat is sent to another ship, not to her own.")
    if not isinstance(target, type(getattr(world, "own", None))):
        target = hull_of(world, getattr(target, "id", None)) or target
    carrying: list[Any] = []
    fetching: list[Any] = []
    before = (m.group("before") or "").strip() if m.group("with") else ""
    for words in (before, m.group("carry") or ""):
        for who in _names(words):
            # a visitor aboard by his name first (package 82, item 2: the seat's person
            # sent home in the host's boat), then the company's own
            p = world.people.find_aboard(who) if hasattr(world.people, "find_aboard") else None
            if p is None:
                p = world.people.find(who)
            if p is None:
                raise OrderError(
                    f"Nobody aboard answers to '{who}'; the boat is not sent. The people: "
                    f"{', '.join(x.name for x in world.people.all if x.aboard)}."
                )
            if p not in carrying:
                carrying.append(p)
    her_people = getattr(target, "people", None)
    for who in _names(m.group("fetch") or ""):
        p = her_people.find(who) if her_people is not None else None
        if p is None and her_people is not None and hasattr(her_people, "find_aboard"):
            p = her_people.find_aboard(who)
        if p is None:
            raise OrderError(
                f"Nobody aboard the {getattr(getattr(target, 'ship', None), 'name', 'other ship')} "
                f"answers to '{who}'; the boat is not sent."
            )
        if p not in fetching:
            fetching.append(p)
    return target, carrying, fetching


def _names(words: str) -> list[str]:
    out: list[str] = []
    for name in re.split(r"\s*,\s*|\s+and\s+", " ".join(str(words).split()).strip(" .")):
        name = name.strip()
        if name:
            out.append(name)
    return out


def execute(ship: Any, order: Order) -> Result:
    """Carry out a port order. The verb is the vocabulary's key."""
    verb = order.verb
    rest = (order.object or "").strip()
    if verb == ordnance_orders.TAKE_IN or (
        verb in ("buy", "demand") and ordnance_orders.names_powder(rest)
    ):
        # powder and shot (practice and resupply, between packages 72 and 73): the supply's
        # order, before the yard's and the market's (no market trades powder), and read
        # before the ports so that a ship with no guns is told so first
        return ordnance_orders.execute(ship, order)
    ports = _ports(ship)
    if verb in CONN_VERBS:
        # package 45: the pilot conns her in or out along his port's track; `I have the
        # conn` (or any helm order of the officer's) takes her back
        if verb == "i have the conn":
            text = ports.take_conn_back()
            return "port.conn", text, {"verb": verb, "level": 1, "conn": False}
        text = ports.give_conn(inward=verb.endswith(" in"))
        return "port.conn", text, {"verb": verb, "level": 1, "conn": True}
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
        to_ship = _boat_to_ship(world_of(ship), phrase, rest)
        if to_ship is not None:
            # package 82: the boat to another ship lying within a boat's pull, with the
            # persons named and for the persons named
            target, carrying, fetching = to_ship
            text, data = ports.send_boat_to(target, carrying, fetching)
            return (
                "evolution.started",
                text,
                {"verb": verb, "level": 1, "subjects": ["the boat"]} | data,
            )
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
        from freesail.world import movement

        actor = (ship.extra or {}).get("order_actor") or "captain"
        person = movement.market_way(world_of(ship), actor)
        if person is not None:
            # ashore at the market, in person (spec M7b §14; package 53, truth 101): the
            # prices read there, the goods by the port's lighter, no boat
            read = [(verb, *_tons_and_good(words, verb)) for words in bargains]
            text, data = ports.trade_list(read, person=person)
            return "market.bargain", text, {"verb": verb, "level": 1} | data
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
    if verb == ordnance_orders.TAKE_IN or (
        verb in ("buy", "demand") and ordnance_orders.names_powder(rest)
    ):
        # powder and shot (practice and resupply): the quantities and the guns named
        ordnance_orders.check(ship, order)
    elif verb in ("buy", "sell") and not re.search(
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
