"""People in places (spec M7b §14 and §17; package 53): a person's place as an aspect of
his state, tied to what he can do there.

A place is not a simulation of its own (the owner, 2026-10-16: "the goal of locations
needn't be super deep simulation of each location, but just an aspect of each person's
status, as well as tying in to the actions they can perform"). The places are the ship's
(`places.PLACES`) and the port's ashore (`places.port_places`); a person is in one
(`Person.where`, with `Person.ashore_at` for the place ashore and `Person.port` for the
port), and this module is the verbs that move him and the checks that tie what he may do
to where he is.

**Who goes.** The giver of the order is the one who goes: the player at the prompt is the
captain (`People.captain`), the player at his seat and a model at its station are the
station's person (`World.stations.holder`), by the order's actor (`core.world.
ORDER_ACTOR`). A standing order's firing, the rules-based captain's judgement and the
director have no person and no place, and nothing here checks them. Nothing moves a
person's place by itself but the boat and the watch's routine (the bill's sleepers, read
by `People.effective_place`, and the man sent for, who comes where he was called).

**The verbs.** `go below` (the captain to his cabin, as always; anyone else to his berth
below: the gunroom, or his trade's place), `come on deck` (the quarterdeck for the
captain and the officers, the deck for the rest), `go to the <place>` (aboard, any place
his duty allows; ashore, any of the port's places), `go aloft`, `go ashore` (by the
boat, at a port's reach, landing him at the quay and leaving him there) and `come
aboard` (the boat sent for him from the ship lying at his port). His duty allows every
place aboard but the captain's cabin, which is the captain's and his servants' and is
reached by being sent for; a man who has the deck does not go ashore with it, and the
man who keeps the reckoning does not leave the ship.

**What he can do where he is** (`check`). The deck's orders (the sails, the yards and the
lines, the helm and the course, the anchors, the hands' work) are given from the
quarterdeck or the deck: from anywhere else they are refused in words naming the way back
("You are in the cabin; go on deck to give the helm an order."). The market is ashore in
person or by the boat from aboard (`market_way`); the boat is sent from aboard. Every
other order (the people's, the port's business by the boat, the reckoning's, the book,
the deck's conversation, the readings) is given from anywhere he is, and a book is read
from anywhere (the owner's ruling of 2026-10-16: the papers kept in a place are dropped).

**The reach** (`within_hail`, spec M7b §17): every stationed person may tell and ask any
person aboard, or ashore with him at the same port; aboard and ashore are out of hail of
each other, and a letter by the boat is the way.
"""

from __future__ import annotations

from typing import Any

from freesail.core.events import Severity
from freesail.orders.errors import OrderError
from freesail.world.people import WRITING
from freesail.world.places import (
    DEFAULT_ASHORE,
    PLACES,
    Places,
    find_port_place,
    place_words,
    port_places,
)

__all__ = [
    "BERTH_BELOW",
    "CABIN_ROLES",
    "DECK_NAVIGATION",
    "DECK_OBJECTS",
    "DECK_PLACES",
    "SIGNALS",
    "HELM_OBJECTS",
    "MOVE_VERBS",
    "PERSON_MOVED",
    "ashore_place_words",
    "ashore_words",
    "check",
    "come_aboard",
    "go",
    "go_ashore",
    "is_deck_order",
    "market_way",
    "person_of_actor",
    "places_ashore",
    "put_aboard",
    "where_am_i",
    "within_hail",
]

# A boat's pull between two ships at sea (package 82; the design's §2): the hail's reach
# doubled and a little, a mile; a boat is not sent across the sea (judgement). The port's
# reach (`orders.BOAT_REACH_NM`, six miles) is the shore's and the lighter's.
BOAT_BETWEEN_NM = 1.0

# The people's verbs that move the giver (`data/vocabulary.yaml`, object `person`).
MOVE_VERBS: tuple[str, ...] = (
    "go below",
    "come on deck",
    "go to",
    "go aloft",
    "go ashore",
    "come aboard",
)

# The line of a person moved about the ship or ashore (the captain's own `go below` and
# `come on deck` keep theirs, `captain.below` and `captain.on_deck`).
PERSON_MOVED = "person.moved"

# The vocabulary's object of the colours and the signals (`orders.signals`, package 71).
SIGNALS = "signals"

# The places aloft (the tops and the masthead), from which a man comes down before he goes
# down the side into the boat (package 98)
ALOFT_PLACES: frozenset[str] = frozenset({"tops", "masthead"})

# The places the deck's orders are given from (spec M7b §14: "the helm only on deck").
DECK_PLACES: frozenset[str] = frozenset({"quarterdeck", "deck"})

# The deck's orders by the vocabulary's object (`data/vocabulary.yaml`): the sails, the
# yards, the lines, the helm and the course, the evolutions said with nothing after them
# (tack, wear, heave to, all hands), the wreck, the hands' work and the ground tackle.
DECK_OBJECTS: frozenset[str] = frozenset(
    {
        "sail",
        "yards",
        "line",
        "heading",
        "points",
        "none",
        "wreck",
        "work",
        "anchor",
        "gunnery",
        "damage",  # package 73: the pumps and the carpenter's work are the deck's orders
        "fight",  # package 73: the marines and the boarders
        # package 98, step 6 (the owner's ruling of 2026-11-09): the colours, the signals,
        # the private signal, the lights and a hail across the water, by the deck's rule;
        # word passed from below to the deck to make them is a later step's
        SIGNALS,
    }
)
# The master's verbs that are the helm's: the course shaped, the chase given, the ship put
# about. The rest of his (the log and the lead, the sights, the reckoning worked below)
# are the reckoning's and given where he is.
DECK_NAVIGATION: frozenset[str] = frozenset({"put her about", "shape a course for", "give chase"})
# The orders that are the helm's, for the refusal's words.
HELM_OBJECTS: frozenset[str] = frozenset({"heading", "points"})
HELM_VERBS: frozenset[str] = DECK_NAVIGATION | frozenset(
    {
        "keep her full",
        "steady",
        "meet her",
        "right the helm",
        "helm a-lee",
        "helm a-weather",
        "tack ship",
        "wear ship",
        "heave to",
        "fill away",
        "box haul",
        "wear short round",
        "box her off",
        "scud",
    }
)

# Where a person goes when he goes below (judgement: his berth): the captain to his
# cabin, the wardroom's officers and the standing officers to the gunroom, a man of the
# muster by his trade to his trade's place (`people.TRADE_PLACES`), anyone else to the
# gunroom.
BERTH_BELOW = "gunroom"

# The roles whose place the captain's cabin is beside the captain's own (judgement: his
# clerk and his servants; a supernumerary berthed aft by the words that made him is
# allowed by his outline's place).
CABIN_ROLES: frozenset[str] = frozenset({"captain", "commander", "clerk", "steward", "servant"})


# ---------------------------------------------------------------------------
# Who
# ---------------------------------------------------------------------------


def person_of_actor(world: Any, actor: str | None) -> Any:
    """The person who gives an order by its actor: the captain for the player at the
    prompt ("captain"), the station's person for a model at its station ("the officer of
    the watch") or the player at his seat ("the master (the player)"); None for a
    standing order's firing, a rule, the driver, the director and a station bound to
    nobody named, who have no place."""
    actor = str(actor or "")
    people = getattr(world, "people", None)
    if people is None or not actor:
        return None
    if actor == "captain":
        from freesail.world import knowledge
        from freesail.world.captive import captive_person

        captive = captive_person(world)
        if captive is not None and getattr(world, "is_followed", True):
            # the player's person a captive (package 74, the design's §3.1): the followed
            # hull's prompt is his wherever it is, never the prize master's; another hull's
            # "captain" is her own captain's hand (the director's, a test's)
            return captive
        if getattr(world, "is_followed", True):
            from freesail.world.captive import remembered_person

            me = remembered_person(world)
            if me is not None and not getattr(me, "aboard", True):
                # the player's person freed and ashore while his prompt follows the hull that
                # held him (package 74, step 6; the design's §7): the prompt is his (decision
                # 62), not that hull's captain's
                return me
        visitor = knowledge.players_visitor(world)
        if visitor is not None:
            # the player aboard another ship as a visitor (decision 62; package 65, step 4):
            # the prompt is his and not her captain's
            return visitor
        try:
            return people.captain
        except IndexError:
            return None
    if not actor.startswith("the "):
        return None
    station = actor.split(" (", 1)[0].removeprefix("the ").strip()
    if station == "director":
        return None
    stations = getattr(world, "stations", None)
    if stations is None:
        return None
    try:
        return stations.holder(station)
    except Exception:  # a people's build that cannot run holds nobody
        return None


def _mustered(world: Any) -> bool:
    """Whether the people have been mustered (`People._build`). Until they are, nobody
    has moved from his place (every move musters them), so the place's checks have nothing
    to say and do not muster them for nothing: a world in which nobody moves is as it
    was, line for line."""
    people = getattr(world, "people", None)
    return people is not None and bool(getattr(people, "_built", True))


# ---------------------------------------------------------------------------
# Where, in words
# ---------------------------------------------------------------------------


def ashore_place_words(place_id: str, port: Any = None) -> str:
    """'on the quay', 'in the tavern', 'at the market' for a place ashore."""
    name = place_id.replace("_", " ")
    if port is not None:
        found = port_places(port).get(place_id)
        if found is not None:
            name = found.name.removeprefix("the ")
    if place_id == "quay":
        return f"on the {name}"
    if place_id in ("tavern",):
        return f"in the {name}"
    return f"at the {name}"


def _port_of(world: Any, person: Any) -> Any:
    ports = getattr(world, "dealings", None)
    pid = getattr(person, "port", None)
    if ports is None or not pid:
        return None
    return ports.ports.get(pid)


def ashore_at(world: Any, person: Any) -> str:
    """The place ashore a person ashore is at: where he went, else where his role is
    found (`places.ashore_place_of`), else the quay."""
    said = str(getattr(person, "ashore_at", "") or "")
    if said:
        return said
    port = _port_of(world, person)
    if port is None:
        return DEFAULT_ASHORE
    from freesail.world.places import ashore_place_of

    return ashore_place_of(port, getattr(person, "role", ""))


def ashore_words(world: Any, person: Any) -> str:
    """'ashore at Falmouth, at the market' for a person ashore at a port; 'ashore' for one
    the boat has landed on an errand and will bring off again."""
    port = _port_of(world, person)
    if port is None:
        return "ashore"
    return f"ashore at {port.name}, {ashore_place_words(ashore_at(world, person), port)}"


def where_words(world: Any, person: Any) -> str:
    """Where he is, for a refusal: 'in the cabin', 'ashore at Falmouth, on the quay'."""
    if not person.aboard and person.where == "shore":
        return ashore_words(world, person)
    return place_words(person.where)


# ---------------------------------------------------------------------------
# What he can do where he is
# ---------------------------------------------------------------------------


# What a visitor aboard another ship may order from her deck (decision 62): his own body's
# moves, his needs, a question or a reading, a free line, a word said (the stations'
# sentences are not orders of the vocabulary and come another way).
VISITOR_VERBS = frozenset(
    # package 60: `take command of` her is given aboard her as a visitor, the act's own; and
    # `transfer` her people to his ship, aboard either (step 2)
    {
        "go to",
        "go below",
        "come on deck",
        "go aloft",
        "come aboard",
        "go ashore",
        "take command of",
        "transfer",
    }
)
VISITOR_OBJECTS = frozenset({"query", "needs", "free"})
# What a captive's prompt performs (package 74; the owner's play of 2026-11-09), and nothing
# else: his body's moves about the places his parole gives him (`_within_liberty`), his
# needs, a question or a reading his place allows, a free line, and a word said (the
# stations' `say to`, `ask` and `tell`: `CAPTIVE_STATION_VERBS`). He does not go ashore nor
# aboard another ship at his own word, hails nobody, makes no signal, gives no standing
# order and keeps none of her books.
CAPTIVE_VERBS = frozenset({"go to", "go below", "come on deck", "go aloft"})
CAPTIVE_STATION_VERBS = frozenset({"say", "ask", "tell"})
CAPTIVE_LEAVING_VERBS = frozenset({"go ashore", "come aboard"})


def _captives_own(verb: str, obj: str) -> bool:
    return obj in VISITOR_OBJECTS or verb in CAPTIVE_VERBS


def captive_at_prompt(ship: Any, leaving: bool = False) -> str | None:
    """The captive's refusal for an order given at this ship's prompt, or None when its
    giver is no captive (or no person stands behind it): for the orders that are read before
    the vocabulary's (a hail, a signal, the colours, a standing order, a book, a station
    stood down), which the place's `check` never sees."""
    from freesail.orders.prompt import world_of

    world = world_of(ship)
    if world is None or not _mustered(world):
        return None
    actor = (getattr(ship, "extra", None) or {}).get("order_actor") or "captain"
    person = person_of_actor(world, actor)
    if person is None:
        return None
    from freesail.world.captive import captive_words
    from freesail.world.hearing import own_hull

    return captive_words(world, person, hull_of(world, own_hull(world)), leaving=leaving)


def hand_on_her(world: Any, actor: str | None) -> bool:
    """Whether an order given at this hull's prompt is the player's hand on her captain
    (decision 41: the rules captain stands aside at it): only where its giver is one of her
    own company and a free man. A captive's words and readings aboard his captor, and a
    visitor's aboard another ship, are a person's own and never a hand on her captain
    (package 74, the owner's play of 2026-11-09: a prisoner's 'say to Captain Penrose Yes.'
    stood the captor's captain aside, and she lay aback and took the ground with nobody
    commanding her). True where no person stands behind the actor, as before; and where
    the people have not been mustered (`_mustered`: nobody has moved, so nobody is a captive
    or a visitor, and asking for her captain would muster them for nothing and change a
    world in which nobody moves: truth 7-279's passage took the ground by it)."""
    if not _mustered(world):
        return True
    person = person_of_actor(world, actor)
    if person is None:
        return True
    from freesail.world.captive import captive_of, is_captive
    from freesail.world.hearing import own_hull

    rec = captive_of(world)
    if is_captive(person) or (rec is not None and rec.get("person") == person.name):
        return False
    here = hull_of(world, own_hull(world))
    home_id = str(getattr(person, "home", "") or "")
    if here is None or not home_id or is_boat_hull(here):
        return True
    return str(here.id) == home_id


def _visitors_own(verb: str, obj: str) -> bool:
    return obj in VISITOR_OBJECTS or verb in VISITOR_VERBS


def is_deck_order(verb: str, obj: str) -> bool:
    """Whether an order is the deck's: given from the quarterdeck or the deck alone."""
    return obj in DECK_OBJECTS or verb in DECK_NAVIGATION


def _what(verb: str, obj: str) -> str:
    if obj in HELM_OBJECTS or verb in HELM_VERBS:
        return "give the helm an order"
    if obj == "sail":
        return "make or take in sail"
    if obj == "anchor":
        return "work the ground tackle"
    return "give an order of the deck"


def check(ship: Any, verb: str, obj: str) -> None:
    """The place's check of an order (spec M7b §14; truth 100): the deck's orders from the
    quarterdeck or the deck, the boat sent from aboard, a man sent for from aboard, by the
    giver of the order where he is; refused in words naming the way back. Nothing for an
    order with no person behind it (`person_of_actor`)."""
    from freesail.orders.prompt import world_of

    world = world_of(ship)
    if world is None or not _mustered(world):
        return
    # the captain's own where the order came with no actor (`orders.handle` called
    # directly, as the primer's and the API's tests call it)
    actor = (getattr(ship, "extra", None) or {}).get("order_actor") or "captain"
    person = person_of_actor(world, actor)
    if person is None:
        return
    here = hull_of(world, getattr(person, "hull", None)) if person.aboard else None
    home_id = str(getattr(person, "home", "") or "")
    if not _captives_own(verb, obj):
        # a captive (package 74, the design's §3.1): no deck is his, this one least of all,
        # and his own ship's is a prize's; the words name his state. His going ashore or
        # aboard another ship is refused him in his own words too (the owner's play of
        # 2026-11-09: 'go ashore' met the free man's "bring her to an anchor")
        from freesail.world.captive import captive_words
        from freesail.world.hearing import own_hull

        prompt_hull = hull_of(world, own_hull(world))
        said = captive_words(world, person, prompt_hull, leaving=verb in CAPTIVE_LEAVING_VERBS)
        if said:
            raise OrderError(said)
    if (
        here is not None
        and not is_boat_hull(here)  # his own ship's boat is his to command
        and home_id
        and str(here.id) != home_id
        and not _visitors_own(verb, obj)
        and obj != SIGNALS  # his own hail and signal, as the refusal below says (package 98)
    ):
        # a visitor aboard another ship (decision 62; package 65, step 4): a passenger's
        # reach, as a seated visitor's domain gives it (`agent.VISITOR_DOMAIN`)
        home = hull_of(world, home_id)
        raise OrderError(
            f"You are aboard the {hull_name(here)} as a visitor"
            f"{', of the ' + hull_name(home) if home is not None else ''}: a visitor aboard "
            "another ship gives no order of her deck, and none of his own ship's from there "
            "(hail her, make a signal or send a letter); 'go to the boat' takes you off in "
            "your own boat where she lies alongside, 'come aboard' sends hers for you."
        )
    if verb in BELAY_VERBS and _in_the_boat_at_the_side(world, person):
        # a person in the boat that has not left the ship's side (package 109; the owner's
        # play of 2026-11-12, note 1) may belay her, and is on deck again when she is stood
        # down (`dealings._boat_kept`)
        return
    if is_deck_order(verb, obj):
        # where he went by his own word: the master's reckoning takes him below to his
        # sights and his day's work by its own rule (his mirror), which is not his going
        # below, and the captain who is the schooner's master gives his orders from there
        # as he always did (the owner's wardroom save, replayed: package 53)
        here = person.place if (person.mirror is not None and person.aboard) else person.where
        if person.aboard and here in DECK_PLACES:
            return
        if not person.aboard and person.where == "shore":
            raise OrderError(
                f"You are {ashore_words(world, person)}; come aboard to {_what(verb, obj)}."
            )
        if not person.aboard:
            raise OrderError(
                f"You are {place_words(person.where)}; you must be aboard and on deck to "
                f"{_what(verb, obj)}."
            )
        raise OrderError(f"You are {place_words(here)}; go on deck to {_what(verb, obj)}.")
    if not person.aboard and verb in ("send the boat", "send for"):
        what = "send the boat" if verb == "send the boat" else "send for a man aboard"
        raise OrderError(
            f"You are {where_words(world, person)}; you cannot {what} from there. 'come "
            "aboard' sends the boat for you."
        )


# The verbs that belay work (`data/vocabulary.yaml`, package 29c), which a person in the
# boat at the ship's side may give of her (package 109).
BELAY_VERBS = frozenset({"belay that", "belay the work", "belay all work"})


def _in_the_boat_at_the_side(world: Any, person: Any) -> bool:
    """Whether the person sits in the ship's boat on an errand that has not left her side:
    waiting for her hands, or hoisting out (package 109)."""
    if person.aboard or person.where != "boat":
        return False
    dealings = getattr(world, "dealings", None)
    boat = getattr(dealings, "boat", None)
    if boat is None or not boat.away or boat.phase != "hoisting out":
        return False
    return str(person.id) in {str(p) for p in boat.people}


def market_way(world: Any, actor: str | None) -> Any:
    """How the giver deals at the market (spec M7b §14; truth 101): None by the boat from
    aboard (as always), or the person himself when he is ashore at the market; refused in
    words when he is ashore elsewhere, or in the boat."""
    person = person_of_actor(world, actor) if _mustered(world) else None
    if person is None or person.aboard:
        return None
    if person.where != "shore":
        raise OrderError(
            f"You are {place_words(person.where)}; the market is dealt with aboard by the "
            "boat, or ashore in person."
        )
    port = _port_of(world, person)
    if port is None:
        raise OrderError("You are ashore on the boat's errand; the market is the purser's.")
    if ashore_at(world, person) != "market":
        raise OrderError(
            f"You are {ashore_words(world, person)}; go to the market to buy and sell in person."
        )
    return person


def places_ashore(world: Any, person: Any = None) -> tuple[str, dict[str, Any]]:
    """`the places ashore`: the places of the port the asker is ashore at, or of the port
    the ship lies in, each with what is done there and who is found there, the world's
    people ashore at each by name (spec M7b §14; package 53). Refused in words at sea."""
    ports = getattr(world, "dealings", None)
    port = None
    if person is not None and not person.aboard and person.where == "shore":
        port = _port_of(world, person)
    if port is None and ports is not None and ports.ports:
        port = ports.in_port()
    if port is None:
        raise OrderError(
            "She is not in port: the places ashore are a port's, asked at anchor in its "
            "roads or ashore."
        )
    lines = ports.places_lines(port)
    return f"The places ashore at {port.name}: " + " ".join(lines), {
        "port": port.id,
        "places": lines,
    }


def within_hail(world: Any, a: Any, b: Any) -> bool:
    """Whether two people are within hail of each other (spec M7b §17): both aboard, or
    both ashore at one port; a person in the boat or the pilot's cutter alongside hails
    the ship as aboard. A person not among the people (None) is taken as aboard."""

    from freesail.world.hearing import own_hull

    def side(p: Any) -> str:
        if p is None:
            return f"aboard:{own_hull(world)}"
        if p.aboard:
            return f"aboard:{getattr(p, 'hull', None) or own_hull(world)}"
        if p.where in ("boat", "cutter"):
            return f"aboard:{getattr(p, 'home', '') or own_hull(world)}"
        return f"ashore:{getattr(p, 'port', '') or ''}"

    return side(a) == side(b)


# ---------------------------------------------------------------------------
# The verbs
# ---------------------------------------------------------------------------


def _berth(person: Any, world: Any) -> str:
    from freesail.world.people import TRADE_PLACES

    if person is world.people.captain:
        return "cabin"
    outline = getattr(person, "outline", None)
    if person.role in TRADE_PLACES:
        return TRADE_PLACES[person.role]
    if outline is not None and outline.place and PLACES.get(outline.place, PLACES["deck"]).below:
        return outline.place
    return BERTH_BELOW


def _on_deck(person: Any, world: Any) -> str:
    """Where a man comes on deck: the quarterdeck for the captain, the officers and the
    master; the deck for the rest (the boatswain, the carpenter, a man of the muster)."""
    from freesail.world.people import WATCH_KEEPERS

    officers = {"captain", "commander", "master", "first lieutenant", "pilot", *WATCH_KEEPERS}
    if person is world.people.captain or person.role in officers:
        return "quarterdeck"
    outline = getattr(person, "outline", None)
    if outline is not None and outline.place == "quarterdeck":
        return "quarterdeck"
    return "deck"


def _duty_allows(world: Any, person: Any, place_id: str) -> str | None:
    """Why his duty does not allow the place, or None when it does."""
    if place_id == "cabin":
        outline = getattr(person, "outline", None)
        if (
            person is world.people.captain
            or person.role in CABIN_ROLES
            or (outline is not None and outline.place == "cabin")
        ):
            return None
        return (
            "The cabin is the captain's; a man goes there when the captain sends for him "
            "('send for')."
        )
    return None


def _deck_kept(world: Any, person: Any, place_id: str) -> str | None:
    """Why a man with the deck does not go below (package 65; the lead's ruling of
    2026-10-31: the period's officer of the watch did not leave the deck, and a man with the
    deck is not blind below), or None: the place is not below, he has not the deck, or the
    deck is the captain's by right (he goes below as he always did, the deck the officer's
    or the book's). Aloft is allowed: the deck is kept from the tops, in sight of it."""
    place = PLACES.get(place_id)
    if place is None or not place.below:
        return None
    held = harness_of(world, person) or seat_of_person(world, person)
    if held is None:
        return None
    holder = held[1]
    agent = getattr(holder, "agent", None)
    if agent is None or not getattr(agent, "has_deck", False):
        return None
    domain = getattr(getattr(holder, "station", None), "domain", None)
    if domain is not None and getattr(domain, "is_captains", False):
        return None
    name = str(getattr(getattr(holder, "station", None), "name", "") or "the officer")
    return (
        f"You have the deck: it is not left for {place.name}. Hand it over first "
        f"(hand_over), or the captain takes it ('I have the deck'); the {name} with the deck "
        "keeps the deck."
    )


def _moved_line(person: Any, place_id: str) -> str:
    if place_id in DECK_PLACES:
        return f"{person.name} came on deck" + (
            ", to the quarterdeck." if place_id == "quarterdeck" else "."
        )
    if place_id == "tops":
        return f"{person.name} went aloft into the tops."
    p = PLACES[place_id]
    if p.below:
        return f"{person.name} went below to {p.name}."
    return f"{person.name} went to {p.name}."


def _within_liberty(world: Any, person: Any, verb: str, words: str, liberty: tuple) -> bool:
    """Whether a captive's move keeps to the places his parole gives him (the design's
    §3.2): the quarterdeck by day only."""
    if not liberty:
        return False
    low = " ".join(str(words or "").lower().split()).removeprefix("the ").strip()
    if verb == "go below":
        want = "cabin" if "cabin" in low else "gunroom"
    elif verb == "come on deck" or low in ("deck", "on deck", "upper deck", "quarterdeck"):
        want = "quarterdeck"
    elif verb == "go aloft":
        return False
    else:
        found = Places().find(low)
        if found is None and low in ("wardroom",):
            found = PLACES["gunroom"]
        want = found.id if found is not None else ""
    if want not in liberty:
        return False
    if want == "quarterdeck":
        light = getattr(getattr(world, "conditions", None), "light", None)
        if callable(light):
            try:
                light = light(world.clock.tick)
            except Exception:  # noqa: BLE001
                light = None
        if str(light or "").lower() == "night":
            return False
    return True


def go(world: Any, person: Any, verb: str, words: str = "") -> tuple[str, str, dict[str, Any]]:
    """`go below`, `come on deck`, `go to the <place>`, `go aloft` for the person who
    gives it: (the log's kind, its words, its data); OrderError in words for a place his
    duty does not allow, one that is none, or the place he is in already."""
    words = " ".join(str(words or "").split())
    if not person.aboard:
        if person.where == "shore":
            return _go_ashore_place(world, person, verb, words)
        raise OrderError(f"You are {place_words(person.where)}; wait until you are aboard.")
    confined = str(getattr(person, "confined_to", "") or "")
    liberty = tuple(getattr(person, "liberty", ()) or ())
    if confined and not _within_liberty(world, person, verb, words, liberty):
        # a prisoner (package 74, spec M7 §19): confined to his place by his parole or his
        # captor's word; the deck is not his to walk beyond the liberty his parole gives
        where = PLACES[confined].name if confined in PLACES else confined
        given = (
            " Your parole gives you "
            + ", ".join(PLACES[x].name for x in liberty if x in PLACES)
            + (" (the quarterdeck by day)." if "quarterdeck" in liberty else ".")
            if liberty
            else ""
        )
        raise OrderError(
            f"You are a prisoner, confined to {where}; the ship is not yours to walk about."
            f"{given} You may speak ('say to the captain: ...')."
        )
    if person.occupied and person.task != WRITING:
        raise OrderError(f"You are at the {person.task}; it is not left for a walk about the ship.")
    if person.occupied and person.task == WRITING and person.mirror is None:
        # the captain's writing is his own to leave (package 65, step 6)
        person.occupied_until = None
        person.occupied_with = ""
    if verb == "go below":
        place_id = "cabin" if "cabin" in words.lower() else _berth(person, world)
    elif verb == "come on deck":
        place_id = _on_deck(person, world)
    elif verb == "go aloft":
        place_id = "tops"
    else:
        low = words.lower().removeprefix("the ").strip()
        if _names_a_boat(world, person, low):
            # `go to the boat` (package 82, item 4; `world.boats`): the boat manned as a hull
            # of the world and the person put aboard her, his station following
            from freesail.world import boats

            return boats.go_to_boat(world, person, low)
        if low in ("deck", "on deck", "upper deck"):
            place_id = _on_deck(person, world)
        elif low in ("below", "my berth", "berth"):
            place_id = _berth(person, world)
        else:
            found = Places().find(low)
            if found is None and low in ("wardroom", "the wardroom"):
                found = PLACES["gunroom"]
            ports = getattr(world, "dealings", None)
            port = ports.in_port() if ports is not None and ports.ports else None
            ashore = find_port_place(port, low) if port is not None else None
            if found is None and ashore is not None:
                raise OrderError(
                    f"{ashore.name[:1].upper()}{ashore.name[1:]} is ashore at {port.name}; "
                    "'go ashore' first, and the boat lands you at the quay."
                )
            if found is None:
                aboard = ", ".join(p.name for p in PLACES.values() if p.aboard)
                raise OrderError(
                    f"'{words}' is no place aboard; the places are {aboard}. Say 'go to the "
                    "gunroom', 'go below', 'come on deck'."
                )
            if not found.aboard:
                if found.id == "shore":
                    raise OrderError("Say 'go ashore': the boat lands you at the quay.")
                raise OrderError(
                    f"{found.name[:1].upper()}{found.name[1:]} is not a place to walk to; "
                    "'go ashore' goes by the boat."
                )
            place_id = found.id
    why = _duty_allows(world, person, place_id)
    if why is not None:
        raise OrderError(why)
    why = _deck_kept(world, person, place_id)
    if why is not None:
        raise OrderError(why)
    if person.where == place_id or (place_id in DECK_PLACES and person.where == place_id):
        raise OrderError(f"You are {place_words(place_id)} already.")
    person.where = place_id
    person.up = place_id in DECK_PLACES or person.up
    text = _moved_line(person, place_id)
    return PERSON_MOVED, text, {"person": person.to_dict(), "place": place_id}


def _names_a_boat(world: Any, person: Any, low: str) -> bool:
    """Whether the words of `go to <the words>` name a boat of his ship's (package 82)."""
    from freesail.world.boats import BOAT_WORDS

    key = low.removeprefix("my ").removeprefix("her ").strip()
    if key in BOAT_WORDS:
        return True
    here = hull_of(world, getattr(person, "hull", None))
    spec = getattr(getattr(here, "ship", None), "spec", None) if here is not None else None
    for b in getattr(spec, "boats", None) or []:
        if key in (b.name.lower().removeprefix("the "), b.id.lower().replace("_", " ")):
            return True
    return False


def _go_ashore_place(
    world: Any, person: Any, verb: str, words: str
) -> tuple[str, str, dict[str, Any]]:
    """A person ashore moves among the port's places (`go to the market`)."""
    port = _port_of(world, person)
    if port is None:
        raise OrderError("You are ashore on the boat's errand; it brings you off again.")
    if verb != "go to":
        raise OrderError(
            f"You are {ashore_words(world, person)}; 'come aboard' sends the boat for you."
        )
    found = find_port_place(port, words)
    if found is None:
        names = ", ".join(p.name for p in port_places(port).values())
        raise OrderError(f"{port.name} has no '{words}'; its places are {names}.")
    if ashore_at(world, person) == found.id:
        raise OrderError(f"You are {ashore_place_words(found.id, port)} already.")
    person.ashore_at = found.id
    text = f"{person.name} went to {found.name} at {port.name}: {found.done}."
    return (
        PERSON_MOVED,
        text,
        {"person": person.to_dict(), "port": port.id, "ashore_at": found.id},
    )


def go_ashore(world: Any, person: Any) -> tuple[str, str, dict[str, Any]]:
    """`go ashore`: the boat lands him at the quay of the port she lies in, and comes back
    without him (spec M7b §14, "by the boat, at a port's reach")."""
    ports = getattr(world, "dealings", None)
    if not person.aboard:
        raise OrderError(f"You are {where_words(world, person)} already.")
    if person.mirror is not None and person is not world.people.captain:
        raise OrderError(
            f"You keep the reckoning, {person.name}; the master does not leave the ship."
        )
    aloft = str(getattr(person, "where", "") or "")  # by his own word, as `come on deck` reads
    if aloft in ALOFT_PLACES:
        # the boat is not reached from the tops (package 98, the lead's addition (c))
        raise OrderError(
            f"You are {place_words(aloft)}; come down on deck first ('come on deck') and then "
            "go ashore."
        )
    agents = getattr(world, "agents", None) or {}
    for name, harness in agents.items():
        st = getattr(harness, "station", None)
        if (
            st is not None
            and st.person == person.name
            and getattr(harness.agent, "deck", False)
            and name != "captain"
        ):
            raise OrderError(f"You have the deck as the {name}; hand it over before you go ashore.")
    seat = getattr(world, "player_seat", None)
    if (
        seat is not None
        and not seat.agent.released
        and seat.station.person == person.name
        and getattr(seat.agent, "deck", False)
    ):
        raise OrderError("You have the deck; hand it over before you go ashore.")
    if ports is None or not ports.ports:
        raise OrderError(
            "There is no shore within a boat's pull: the ship is not in a world with ports."
        )
    return ports.land_person(person)


def by_waterman(world: Any, person: Any) -> tuple[str, str, dict[str, Any]]:
    """`hire a waterman` (package 68, R-62): a shore boat between the ship and the
    quay of the port she lies at, her own boat away or not (`Ports.waterman`)."""
    ports = getattr(world, "dealings", None)
    if ports is None or not ports.ports:
        raise OrderError("There is no port, and no waterman to hire.")
    return ports.waterman(person)


def come_aboard(world: Any, person: Any) -> tuple[str, str, dict[str, Any]]:
    """`come aboard`: the boat sent for him from the ship lying at his port."""
    ports = getattr(world, "dealings", None)
    if person.aboard:
        home_id = str(getattr(person, "home", "") or "")
        if home_id and str(getattr(person, "hull", "") or "") != home_id:
            # a visitor in another hull (package 82): her boat takes him home, where his
            # own ship lies within a boat's pull; else the words say the way
            home = hull_of(world, home_id)
            if home is None:
                raise OrderError(
                    f"You are aboard the {hull_name(hull_of(world, person.hull))}; your own "
                    "ship has no hull on this sea to go back to."
                )
            if ports is None:
                raise OrderError("There is no boat here to take you back to your ship.")
            text, data = ports.send_boat_to(home, [person], [])
            return (
                "evolution.started",
                text,
                {"ship": home.id, "errand": "to_ship", "people": [person.id]} | data,
            )
        raise OrderError(f"You are aboard already, {place_words(person.where)}.")
    if person.where != "shore":
        raise OrderError(f"You are {place_words(person.where)}; the boat brings you aboard.")
    if ports is None or not ports.ports:
        raise OrderError("There is no ship's boat to send for you.")
    return ports.fetch_person(person)


# ---------------------------------------------------------------------------
# A person moved between hulls (package 82; `docs/design/Design-BoatAndPersonAboard.md` §2)
# ---------------------------------------------------------------------------


def hull_of(world: Any, hull_id: str | None) -> Any:
    """A hull of the one world by her id, or None (ashore, in a boat, a hull not made)."""
    if not hull_id:
        return None
    hulls = getattr(world, "hulls", None) or {}
    return hulls.get(str(hull_id))


def hull_name(hull: Any) -> str:
    return str(getattr(getattr(hull, "ship", None), "name", "") or getattr(hull, "id", "") or "")


def is_boat_hull(hull: Any) -> bool:
    """Whether a hull is a ship's boat manned as a hull (package 82, item 4): her file has oars."""
    ship = getattr(hull, "ship", None)
    return getattr(getattr(ship, "spec", None), "oars", None) is not None


def seat_of_person(world: Any, person: Any) -> tuple[Any, Any] | None:
    """(the hull it is on, the player's seat) when the player holds a station through a
    seat whose person is `person`, on any hull of the game (package 82, item 2); None
    otherwise."""
    name = str(getattr(person, "name", "") or "")
    for hull in list((getattr(world, "hulls", None) or {}).values()):
        seat = getattr(hull, "player_seat", None)
        if seat is None or seat.agent.released:
            continue
        named = str(getattr(seat.station, "person", "") or "")
        if named == name:
            return hull, seat  # his voice, or his own station made for him by name
        if named:
            continue  # a station that names another (package 82b: never by the holder)
        try:
            holder = hull.stations.holder(seat.station.name)
        except Exception:  # noqa: BLE001  (a muster that cannot run binds nobody)
            holder = None
        if holder is person:
            return hull, seat
    return None


def harness_of(world: Any, person: Any) -> tuple[Any, Any] | None:
    """(the hull it is in, the harness) of the station a person holds through a door, on
    any hull of the game (package 82: a harness lives where its person is); None when no
    model holds him. A station that names its person is his by that name alone (package
    82b): the binding's holder of a hull is read through the people of the hull whose block
    is running, so while his boat's arrival runs in his own hull's block another hull's
    "captain" read as him, and her captain's harness was carried into the visitor's station
    (one harness at two stations; the owner's notes of 2026-11-01 and 11-05)."""
    from freesail.agents.harness import harnesses_of

    name = str(getattr(person, "name", "") or "")
    for hull, h in harnesses_of(world):
        if getattr(h.agent, "released", False):
            continue
        named = str(getattr(h.station, "person", "") or "")
        if named == name:
            return hull, h
        if named:
            continue
        stations = getattr(hull, "stations", None)
        try:
            holder = stations.holder(h.station.name) if stations is not None else None
        except Exception:  # noqa: BLE001  (a people's build that cannot run binds nobody)
            holder = None
        if holder is person:
            return hull, h
    return None


def visitor_words(station: Any, home: Any, host: Any) -> str:
    """A visitor's station in words (package 82b, item 2; `Design-DoorAndVisitor.md` §3): his
    own station's name, his ship's and his host's, "officer of the watch, of the Raven,
    aboard the Amazon". `station` a `Station` or its name, `home` and `host` hulls or names."""
    from freesail.agents.agent import station_name

    words = station_name(str(getattr(station, "name", station) or ""))
    of = hull_name(home) if not isinstance(home, str) else home
    at = hull_name(host) if not isinstance(host, str) else host
    return f"{words}, of the {of}, aboard the {at}"


def visitor_name(world: Any, person: Any, host: Any, home_station: Any = None) -> str:
    """The station a visitor holds in `host` (package 82b, item 2): `visitor_words` as a
    station's key, lower-case as every station's name is, from his own station at home
    (`home_station`); his voice's name (package 67's, his own name) when he holds none.
    Never a station of the host's own, nor one that a prefix of it names: the comma follows
    his station's words. One function for the binding, the unbinding and the replay."""
    from freesail.world.seats import _voice_name

    if home_station is None or not str(getattr(home_station, "name", home_station) or ""):
        return _voice_name(person)
    home = hull_of(world, getattr(person, "home", "")) or str(getattr(person, "home", "") or "")
    return " ".join(visitor_words(home_station, home, host).lower().split())


def visitor_forms(name: str) -> tuple[str, ...]:
    """The words a visitor's station is addressed by in the host's sentences, as the
    sentences' `normalise` gives them (a comma spaced): his station's whole name, with its
    commas or without, and "<his station> of the <his ship>" (package 82b, item 2); none for
    a name that is not a visitor's."""
    if ", of the " not in name or ", aboard the " not in name:
        return ()
    station, _, rest = name.partition(", of the ")
    ship = rest.rpartition(", aboard the ")[0]
    whole = name.replace(",", " , ")
    short = f"{station} of the {ship}"
    forms = (whole, name.replace(",", ""), f"{station} , of the {ship}", short)
    return tuple(" ".join(f.split()) for f in forms)


def visiting_station(hull: Any, person: Any, policy: Any = None, home_station: Any = None) -> Any:
    """The station a visitor holds in a hull not his own (the design's §2): his voice, a
    station of the passenger's kind named by his own station, his ship and hers (package
    82b: `visitor_name`; his own name where he holds no station at home), bound to him
    quietly for as long as he is in her; he reads her deck as a passenger reads it and
    gives none of her orders."""
    import dataclasses

    from freesail.agents.agent import VISITOR_DOMAIN
    from freesail.world.seats import VOICE_ACTOR, VOICE_KIND, voice_station

    name = visitor_name(hull.world, person, hull, home_station)
    stations = hull.stations
    if stations.holder(name) is not person:
        stations.bind(name, person, kind=VOICE_KIND, quiet=True, actor=VOICE_ACTOR)
    station = voice_station(hull, name, policy)
    home = hull_of(hull.world, getattr(person, "home", ""))
    role = str(getattr(person, "role", "") or "a person")
    brief = VISITOR_BRIEF.format(
        person=person.name,
        role=role,
        home=hull_name(home) if home is not None else "your own ship",
        hull=hull_name(hull),
    )
    return dataclasses.replace(station, brief=brief, domain=VISITOR_DOMAIN)


# A visitor's brief (package 82): what a model whose person is aboard another ship has and
# has not there, in the consent brief's voice; the station's kind is the passenger's.
VISITOR_BRIEF = (
    "You are {person}, {role} of the {home}, aboard the {hull} as a visitor: your station has "
    "gone with you from your own ship, and here you have a passenger's reach and no more. You "
    "read every reading and every query of the {hull} ('where am I' says where you stand), "
    "speak and ask by the deck's conversation, give and take what lies before you, keep your "
    "journal, stand by until an event or a bell, and leave. You give no order of her deck, and "
    "none of the {home}'s from here: hail her, make a signal or send a letter. Your own station "
    "on the {home} stands bound to you meanwhile; 'come aboard' sends the {hull}'s boat to take "
    "you home where the {home} lies within a boat's pull, and your station is yours again with "
    "its whole surface when you are aboard her. There is no deck at this station.\n\n"
    "Two ways to stop, which are not one another:\n"
    "- Stand down: stand_down(note). The game is saved, your note is journaled, and the "
    "station is released.\n"
    "- Withdraw: the token, or opt_out, as said above.\n\n"
    "Candour: say what you see and what you do; an order refused is a refusal in words."
)


def _unbind_visit(hull: Any, person: Any, why: str, name: str = "") -> None:
    """A visitor's voice unbound from the hull he left (its harness taken out first, so
    that the unbinding stands nobody down), by the name it was bound under there (package
    82b: the station's name before the move; his own name's voice when none is given)."""
    from freesail.world.seats import VOICE_KIND, _voice_name

    name = name or _voice_name(person)
    stations = getattr(hull, "stations", None)
    if stations is None or not stations.aboard(name) or stations.kind_of(name) != VOICE_KIND:
        return
    agents = getattr(hull, "agents", None)
    if isinstance(agents, dict) and name in agents:
        return  # a model holds the voice by a seat of its own: not this move's to end
    stations.unbind(name, why=why, quiet=True)


def put_aboard(
    world: Any,
    person: Any,
    hull: Any,
    place: str = "quarterdeck",
    *,
    seat: str = "follows",
    why: str = "",
    by: str = "",
    said: bool = True,
) -> tuple[str, str, dict[str, Any]]:
    """**One function for every change of a person's hull** (package 82; the design's §2):
    by the boat alongside another ship, by boarding (the deck won), by capture (74's
    captive) or by the director's word. His whereabouts hers (`Person.hull`, his place in
    her, nothing of the shore); a station he holds through a door goes with him (`seat`
    "follows": the harness carried into her as his voice there, or as his own station
    again when she is his home; "stands down": stood down with `why`, the handover's rule,
    for a captive); his own station on his home hull stands bound to him meanwhile. Said
    in her log (notable, `person.aboard`, with the hull he came from) and in the log of the
    hull he left (routine, `person.moved`) when `said`. Returns the arrival's (kind, text,
    data)."""
    from freesail.core.events import Severity

    hid = str(getattr(hull, "id", "") or "")
    was = hull_of(world, getattr(person, "hull", None))
    was_where = str(getattr(person, "where", "") or "")
    if was is hull:
        return "person.aboard", f"{person.name} is aboard the {hull_name(hull)} already.", {}
    whence = ""
    if was is not None:
        came_from = hull_name(was)  # "the Amazon's launch" carries its own article
        the = "" if came_from.lower().startswith("the ") else "the "
        whence = f" from {the}{came_from}"
    elif was_where in ("boat", "cutter"):
        home = hull_of(world, getattr(person, "home", ""))
        whence = f" from the {hull_name(home)}'s boat" if home is not None else " from the boat"
    elif was_where == "shore":
        whence = " from the shore"
    person.hull = hid
    person.where = place
    person.port = None
    person.ashore_at = ""
    held = harness_of(world, person)
    if held is not None:
        from_hull, h = held
        if seat == "stands down":
            h.stand_down(why or f"put aboard the {hull_name(hull)}", by=by or "the handover")
        else:
            home_id = str(getattr(person, "home", "") or "")
            was_name = str(getattr(h.station, "name", "") or "")
            if hid == home_id and h.visiting:
                # home again: his own station his, the voice he held unbound where he was
                own_id, own_station = h._home
                h.move_to(hull, own_station, None)
                if from_hull is not None and str(getattr(from_hull, "id", "")) != own_id:
                    _unbind_visit(
                        from_hull,
                        person,
                        f"{person.name} went aboard the {hull_name(hull)}",
                        was_name,
                    )
            elif hid != home_id:
                # a visitor: his voice in her, his own station kept for his return
                home = h._home or (str(getattr(from_hull, "id", "") or ""), h.station)
                station = visiting_station(hull, person, h.policy, home[1])
                h.move_to(hull, station, home)
                if from_hull is not None and str(getattr(from_hull, "id", "")) != home[0]:
                    _unbind_visit(
                        from_hull,
                        person,
                        f"{person.name} went aboard the {hull_name(hull)}",
                        was_name,
                    )
    seated = seat_of_person(world, person)
    if seated is not None:
        # the player's seat goes with its person as a harness does (package 82, item 2)
        from_hull, s = seated
        if seat == "stands down":
            s.stand_down_quietly(why or f"put aboard the {hull_name(hull)}")
        else:
            home_id = str(getattr(person, "home", "") or "")
            was_name = str(getattr(s.station, "name", "") or "")
            if hid == home_id and s.visiting:
                own_id, own_station = s._home
                s.move_to(hull, own_station, None)
                if from_hull is not None and str(getattr(from_hull, "id", "")) != own_id:
                    _unbind_visit(
                        from_hull,
                        person,
                        f"{person.name} went aboard the {hull_name(hull)}",
                        was_name,
                    )
            elif hid != home_id:
                home = s._home or (str(getattr(from_hull, "id", "") or ""), s.station)
                s.move_to(hull, visiting_station(hull, person, home_station=home[1]), home)
                if from_hull is not None and str(getattr(from_hull, "id", "")) != home[0]:
                    _unbind_visit(
                        from_hull,
                        person,
                        f"{person.name} went aboard the {hull_name(hull)}",
                        was_name,
                    )
    data = {
        "person": person.name,
        "ship": hid,
        "from": str(getattr(was, "id", "") or ""),
        "by": by,
    }
    text = f"{person.name} came aboard{whence}."
    _drivers_follow(world, person, hull)
    if said:
        left = was
        if left is None and was_where in ("boat", "cutter"):
            left = hull_of(world, getattr(person, "home", ""))  # from his ship's boat
        if left is not None and left is not hull:
            left.record(
                Severity.ROUTINE,
                PERSON_MOVED,
                f"{person.name} went aboard the {hull_name(hull)}.",
                data={"person": person.to_dict(), "ship": hid},
            )
        hull.record(Severity.NOTABLE, "person.aboard", text, data=data)
    return "person.aboard", text, data


def _drivers_follow(world: Any, person: Any, hull: Any) -> None:
    """The prompt follows the player's person's body (decision 62; package 65, step 4):
    when he is the player's one person (`knowledge.players_person`) and his hull changes,
    the drivers follow him into it, as `boats.follow_boat` has them follow him into the
    boat: a routine line `hull.followed` of her log, a consequence of his order and never
    a driver's input, so that a replay moves it the same. The owner's `follow` stands for
    his own choice."""
    from freesail.world import knowledge
    from freesail.world.hulls import Hull

    root = world
    while isinstance(root, Hull):
        root = root.world  # the one World behind a façade (`followed` is the World's)
    hulls = getattr(root, "hulls", None)
    if not isinstance(hulls, dict) or str(getattr(hull, "id", "")) not in hulls:
        return
    if getattr(root, "followed", None) == hull.id:
        return
    try:
        his = knowledge.players_person(root)
    except Exception:  # noqa: BLE001  (a world whose people cannot be read)
        his = None
    if his is not person:
        return
    root.followed = str(hull.id)
    with root.as_hull(hull):
        root.record(
            Severity.ROUTINE,
            "hull.followed",
            f"The drivers follow {person.name} aboard the {hull_name(hull)}: her readings are his.",
            data={"ship": str(hull.id), "person": person.name},
        )


def where_am_i(world: Any, person: Any) -> str:
    """Where a person is, for the reading `where am I` (package 82): aboard his own hull
    and his place; aboard another as a visitor, hers named; in a boat; ashore at his port's
    place."""
    if person is None:
        return "nobody is named at your station, and nobody is anywhere"
    if not getattr(person, "aboard", True):
        if person.where == "shore":
            return ashore_words(world, person)
        home = hull_of(world, getattr(person, "home", ""))
        whose = f"the {hull_name(home)}'s " if home is not None else "the "
        return f"in {whose}boat" if person.where == "boat" else place_words(person.where)
    here = hull_of(world, getattr(person, "hull", None))
    if here is not None and is_boat_hull(here):
        # in a boat manned as a hull (package 82, item 4): hers named, the oars' or the
        # lug's state, and the coxswain's mark
        from freesail.physics.oars import oars_of

        oars = oars_of(here.ship)
        how = oars.words() if oars is not None else "under oars"
        mark = dict(getattr(oars, "pulling_for", {}) or {})
        for_words = ""
        if mark.get("fast"):
            for_words = f", made fast alongside {mark.get('name') or 'the ship'}"
        elif mark.get("alongside"):
            for_words = ", pulling for the ship"
        elif mark.get("quay"):
            for_words = ", pulling for the quay"
        elif mark:
            for_words = f", pulling for {mark.get('name') or 'the mark'}"
        return f"in {hull_name(here)}, {how}{for_words}"
    people = getattr(here, "people", None) if here is not None else getattr(world, "people", None)
    try:
        place = people.effective_place(person) if people is not None else person.where
    except Exception:  # noqa: BLE001  (a world whose people cannot be read)
        place = getattr(person, "where", "")
    words = place_words(place) if place else "aboard"
    home_id = str(getattr(person, "home", "") or "")
    if here is not None and (getattr(person, "confined_to", "") or getattr(person, "liberty", ())):
        # a prisoner aboard her (package 74, the design's §3.1): his state and his own ship
        from freesail.world.captive import state_words

        home = hull_of(world, home_id) if home_id and str(here.id) != home_id else None
        of = f", of the {hull_name(home)}" if home is not None else ""
        return f"aboard the {hull_name(here)}, {words}, {state_words(world, person)}{of}"
    if here is not None and home_id and str(here.id) != home_id:
        home = hull_of(world, home_id)
        of = f", of the {hull_name(home)}" if home is not None else ""
        # his station there, by its own name, his ship's and hers (package 82b, item 2)
        held = harness_of(world, person) or seat_of_person(world, person)
        home_at = getattr(held[1], "_home", None) if held is not None else None
        station = ""
        if isinstance(home_at, tuple):
            station = f", standing as the {visitor_words(home_at[1], home or home_id, here)}"
        return f"aboard the {hull_name(here)}, {words}, a visitor{of}{station}"
    if here is not None:
        return f"aboard the {hull_name(here)}, {words}"
    return words
