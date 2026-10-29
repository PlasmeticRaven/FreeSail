"""Who heard a word (package 66; spec M7b §14's earshot, the dispatches test's findings 17
and the captain's debrief: "nothing confirmed that Veale had heard me").

A word is heard where it is said: aboard, by everyone within earshot of the place
(`places.earshot`: the quarterdeck, the deck and the galley open to one another, every
other place alone); ashore, by everyone at the same place of the same port (the counting
house is not the market). These functions read the people and the stations as they stand
and change nothing. They are kept apart from the people's registry (`people.py`), whose
movement of persons is another package's, so that each is read alone.

    spot_of(world, person)        where a person hears: ("aboard", hull, place), ("ashore",
                                  port, place ashore) or ("boat", hull)
    station_spot(world, station)  the same for a station (its person's, else its place)
    within_hearing(said, other)   whether a word said at one spot is heard at another
    people_hearing(world, spot)   the named people within hearing of a word said there,
                                  of every hull (the world's one registry)
    stations_everywhere(world)    the stations held on every World of the game
    heard_words(...)              'heard by the captain and Mr Veale, at the counting
                                  house' or 'heard by nobody: the captain is at the market'
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "heard_words",
    "own_hull",
    "people_hearing",
    "said_tail",
    "spot_of",
    "spot_words",
    "station_spot",
    "stations_everywhere",
    "within_hearing",
]

Spot = tuple[str, ...]

# How many people a result names before it counts the rest (judgement: a frigate's
# quarterdeck holds a dozen named officers, and one line is wanted).
HEARD_NAMED_MAX = 4


def own_hull(world: Any) -> str:
    """The id of a World's own hull (`world.own.id`), "" for a stub without one."""
    return str(getattr(getattr(world, "own", None), "id", "") or "")


def company_of(world: Any, person: Any) -> Any:
    """The company (`People`) a person is read by: his home hull's, through the world's
    one registry (package 84, step 2), else the World's own."""
    registry = getattr(world, "registry", None)
    home = getattr(person, "home", "")
    if registry is not None and home:
        found = registry.people_of(home)
        if found is not None:
            return found
    return getattr(world, "people", None)


def spot_of(world: Any, person: Any) -> Spot:
    """Where a person hears: ("aboard", the hull he is in, his place) by his own company's
    reading of it, or ("ashore", his port's id, his place ashore); ("boat", his home hull)
    in his ship's boat, ("cutter", ...) in the pilot's. Two persons at the market at
    Plymouth hear each other whichever hull brought them (package 84, step 2)."""
    if not getattr(person, "aboard", True):
        where = str(getattr(person, "where", "") or "")
        if where == "shore":
            from freesail.world.movement import ashore_at

            return ("ashore", str(getattr(person, "port", "") or ""), ashore_at(world, person))
        return (where or "boat", str(getattr(person, "home", "") or own_hull(world)))
    people = company_of(world, person)
    try:
        place = people.effective_place(person) if people is not None else person.where
    except Exception:  # noqa: BLE001  (a world whose people cannot be read)
        place = getattr(person, "where", "quarterdeck")
    hull = getattr(person, "hull", None)
    if not isinstance(hull, str) or not hull:
        hull = own_hull(world)  # a voice of the ship's, or a person before his adoption
    return ("aboard", hull, "quarterdeck" if place == "deck" else str(place))


def station_spot(world: Any, station: str) -> Spot:
    """Where a station hears: its person's spot, else the station's own place aboard (the
    lookout at the masthead; `agent.place_of`)."""
    from freesail.agents.agent import CAPTAIN, place_of

    stations = getattr(world, "stations", None)
    person = None
    if stations is not None:
        try:
            person = stations.holder(station)
        except Exception:  # noqa: BLE001  (a people's build that cannot run binds nobody)
            person = None
    if person is None and station == CAPTAIN:
        people = getattr(world, "people", None)
        try:
            person = people.captain if people is not None else None
        except Exception:  # noqa: BLE001  (a world with no muster)
            person = None
    if person is not None:
        return spot_of(world, person)
    place = place_of(world, station)
    if place == "shore":
        return ("ashore", "", "")
    return ("aboard", own_hull(world), "quarterdeck" if place == "deck" else place)


def within_hearing(said: Spot, other: Spot) -> bool:
    """Whether a word said at `said` is heard at `other`: aboard the same hull within
    earshot of the place, ashore at the same place of the same port, in a boat in the
    same boat."""
    from freesail.world.places import earshot

    if not said or not other or said[0] != other[0]:
        return False
    if said[0] == "aboard":
        return (
            len(said) == 3
            and len(other) == 3
            and said[1] == other[1]
            and (other[2] in earshot(said[2]))
        )
    return said == other


def people_hearing(world: Any, said: Spot, exclude: Any = None) -> list[Any]:
    """The named people of the world's one registry within hearing of a word said at
    `said`, the speaker (`exclude`) left out: every hull's, so that a word ashore reaches
    whoever is at that place of that port (package 84, step 2)."""
    people = getattr(world, "people", None)
    if people is None:
        return []
    try:
        everyone = list(getattr(people, "everyone", None) or people.all)
    except Exception:  # noqa: BLE001  (a world with no muster)
        return []
    return [p for p in everyone if p is not exclude and within_hearing(said, spot_of(world, p))]


def stations_everywhere(world: Any) -> list[tuple[Any, Any]]:
    """The stations held now on every World of the game, as (the World, the harness or the
    player's seat): the parent's and each crewed ship's (package 84, step 2; the one
    registry's hearing wants the hearers of every hull)."""
    from freesail.agents.harness import _stations_held

    parent = getattr(world, "parent", None) or world
    hulls = list((getattr(parent, "hulls", None) or {}).values())
    if not hulls:
        return [(parent, h) for h in _stations_held(parent)]
    # every hull once (package 84, step 9: the player's ship is a vessel of the sea too, so
    # a walk over the vessels' hulls would count the followed hull twice)
    return [(hull, h) for hull in hulls for h in _stations_held(hull)]


def spot_words(world: Any, spot: Spot) -> str:
    """'on the quarterdeck', 'ashore at Plymouth, at the counting house', 'in the boat'."""
    from freesail.world.places import place_words

    if spot and spot[0] == "aboard":
        words = place_words(spot[2] if len(spot) == 3 else spot[1])
        if len(spot) == 3 and spot[1] and spot[1] != own_hull(world):
            registry = getattr(world, "registry", None)
            company = registry.people_of(spot[1]) if registry is not None else None
            name = getattr(getattr(company, "world", None), "ship", None)
            words = f"aboard the {getattr(name, 'name', spot[1]) or spot[1]}, {words}"
        return words
    if spot and spot[0] == "ashore":
        from freesail.world.movement import ashore_place_words

        ports = getattr(world, "ports", None)
        port = (getattr(ports, "ports", None) or {}).get(spot[1]) if ports is not None else None
        name = port.name if port is not None else "the port"
        return f"ashore at {name}, {ashore_place_words(spot[2], port)}"
    return place_words(spot[0]) if spot else ""


def _name_of(world: Any, person: Any) -> str:
    people = getattr(world, "people", None)
    try:
        if people is not None and people.captain is person:
            return "the captain"
    except Exception:  # noqa: BLE001  (a world with no muster)
        pass
    return str(getattr(person, "name", "") or "someone")


def _and(items: list[str]) -> str:
    if len(items) <= 1:
        return "".join(items)
    return ", ".join(items[:-1]) + " and " + items[-1]


def heard_words(
    world: Any,
    said: Spot,
    speaker: Any = None,
    stations: list[str] | tuple[str, ...] = (),
    absent: Any = None,
) -> str:
    """Who heard a word said at `said`, for the result of the order that said it: 'heard
    by the captain and Mr Veale, at the counting house'; with nobody, 'heard by nobody, in
    the gunroom', and where `absent` names a person wanted (the station's person the
    director spoke to, or the asker's addressee), where he is: 'heard by nobody: the
    captain is ashore at Plymouth, at the market'. `stations` are the stations held that
    heard it, named when no person of theirs is among the people."""
    heard = people_hearing(world, said, exclude=speaker)
    # the stations held that heard it first (their holders are who the words reach), by
    # their person's name, then the rest of the people within hearing
    names: list[str] = []
    named: list[Any] = []
    reg = getattr(world, "stations", None)
    for st in stations:
        try:
            bound = reg.holder(st) if reg is not None else None
        except Exception:  # noqa: BLE001  (a people's build that cannot run binds nobody)
            bound = None
        if bound is not None and bound is not speaker:
            if all(p is not bound for p in named):
                named.append(bound)
                names.append(_name_of(world, bound))
        else:
            names.append(f"the {st}")
    for p in heard:
        if all(q is not p for q in named):
            names.append(_name_of(world, p))
    where = spot_words(world, said)
    if names:
        shown = names[:HEARD_NAMED_MAX]
        more = len(names) - len(shown)
        if more:
            shown.append(f"{more} more")
        return f"heard by {_and(shown)}, {where}"
    if absent is not None:
        return (
            f"heard by nobody: {_name_of(world, absent)} is "
            f"{spot_words(world, spot_of(world, absent))}"
        )
    return f"heard by nobody, {where}"


# The kinds whose result says who heard the words: a `say` (the player's, a station's) and
# the lookout's hail; and the question put to a person nobody holds, which says until when
# it waits for an answer.
SAID_KINDS = ("agent.spoke", "agent.hail")
ASKED_KIND = "agent.asked"


def said_tail(world: Any, e: Any) -> str:
    """What the result of an order that said words adds after its line (package 66; the
    log's line is not changed, so that no recorded passage moves): who heard a `say` or a
    hail ('Heard by the captain and Mr Veale, at the counting house.'), and for a question
    put to a person nobody holds while a director is seated, that it waits for his answer
    until the glass is out. '' for any other line."""
    data = getattr(e, "data", None) or {}
    kind = getattr(e, "kind", "")
    if kind in SAID_KINDS:
        station = str(data.get("station") or "captain")
        if data.get("hail") or kind == "agent.hail":
            spot: Spot = ("aboard", own_hull(world), "quarterdeck")
        else:
            spot = station_spot(world, station)
        reg = getattr(world, "stations", None)
        try:
            speaker = reg.holder(station) if reg is not None else None
        except Exception:  # noqa: BLE001
            speaker = None
        words = heard_words(world, spot, speaker, list(data.get("heard_by") or ()))
        return f"{words[:1].upper()}{words[1:]}."
    if kind == ASKED_KIND and data.get("unheld") and data.get("question"):
        from datetime import timedelta

        from freesail.agents.director import QUESTION_BOUND_S

        until = (world.clock.ship_time + timedelta(seconds=QUESTION_BOUND_S)).strftime("%H:%M")
        return (
            f"The question is put; his answer is awaited until {until}, when the glass is "
            "out, and you will be told if none comes."
        )
    return ""
