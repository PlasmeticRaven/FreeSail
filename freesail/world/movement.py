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

from freesail.orders.errors import OrderError
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
    "within_hail",
]

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
    ports = getattr(world, "ports", None)
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
    ports = getattr(world, "ports", None)
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

    def side(p: Any) -> str:
        if p is None or p.aboard or p.where in ("boat", "cutter"):
            return "aboard"
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


def go(world: Any, person: Any, verb: str, words: str = "") -> tuple[str, str, dict[str, Any]]:
    """`go below`, `come on deck`, `go to the <place>`, `go aloft` for the person who
    gives it: (the log's kind, its words, its data); OrderError in words for a place his
    duty does not allow, one that is none, or the place he is in already."""
    words = " ".join(str(words or "").split())
    if not person.aboard:
        if person.where == "shore":
            return _go_ashore_place(world, person, verb, words)
        raise OrderError(f"You are {place_words(person.where)}; wait until you are aboard.")
    if person.occupied:
        raise OrderError(f"You are at the {person.task}; it is not left for a walk about the ship.")
    if verb == "go below":
        place_id = "cabin" if "cabin" in words.lower() else _berth(person, world)
    elif verb == "come on deck":
        place_id = _on_deck(person, world)
    elif verb == "go aloft":
        place_id = "tops"
    else:
        low = words.lower().removeprefix("the ").strip()
        if low in ("deck", "on deck", "upper deck"):
            place_id = _on_deck(person, world)
        elif low in ("below", "my berth", "berth"):
            place_id = _berth(person, world)
        else:
            found = Places().find(low)
            if found is None and low in ("wardroom", "the wardroom"):
                found = PLACES["gunroom"]
            ports = getattr(world, "ports", None)
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
    if person.where == place_id or (place_id in DECK_PLACES and person.where == place_id):
        raise OrderError(f"You are {place_words(place_id)} already.")
    person.where = place_id
    person.up = place_id in DECK_PLACES or person.up
    text = _moved_line(person, place_id)
    return PERSON_MOVED, text, {"person": person.to_dict(), "place": place_id}


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
    ports = getattr(world, "ports", None)
    if not person.aboard:
        raise OrderError(f"You are {where_words(world, person)} already.")
    if person.mirror is not None and person is not world.people.captain:
        raise OrderError(
            f"You keep the reckoning, {person.name}; the master does not leave the ship."
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
    ports = getattr(world, "ports", None)
    if ports is None or not ports.ports:
        raise OrderError("There is no port, and no waterman to hire.")
    return ports.waterman(person)


def come_aboard(world: Any, person: Any) -> tuple[str, str, dict[str, Any]]:
    """`come aboard`: the boat sent for him from the ship lying at his port."""
    ports = getattr(world, "ports", None)
    if person.aboard:
        raise OrderError(f"You are aboard already, {place_words(person.where)}.")
    if person.where != "shore":
        raise OrderError(f"You are {place_words(person.where)}; the boat brings you aboard.")
    if ports is None or not ports.ports:
        raise OrderError("There is no ship's boat to send for you.")
    return ports.fetch_person(person)
