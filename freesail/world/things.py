"""Things (spec M7b §17a; package 53b): the people's sibling, a thing with a name, a
description and where it is, and nothing more.

A thing is made from words as a person is: by the director's or the owner's `aboard:`
order (`aboard: a sealed packet, on the cabin table`; `aboard: a cask of brandy, in the
hold`; `freesail.world.orders`) or by the scenario's `things:` list ("a sealed packet, in
the captain's keeping, from the Custom House"). Where it is, is one of three: a person's
**keeping** (it is his, and goes where he goes: aboard, in the boat, ashore at the
counting house), a **place** aboard of §14's (`places.PLACES`: the cabin, the hold, ...)
with the words of its spot in it ("on the table"), or a **place ashore** at a port (the
quay, the counting house) with its spot; and a thing thrown overboard is over the side.
No weight, size or value is kept until a system needs one: the cargo's tons stay the
hold's, and a thing's price is a transaction's that names it.

It is kept by the people's machinery less their needs and their mouths: the registry is
the World's `People` (`People.things`), saved whole in a checkpoint and made again by a
replay from the order or the scenario that made it and the free lines that moved it
(`freesail.orders.free`). It shows in the people's reading ("Mr Veale, clerk: ashore at
Plymouth, at the counting house, a sealed packet in his keeping"), in the places' ("In
the cabin: a sealed packet on the table"), in the places ashore and in the truth; a world
with no thing in it reads as it did.

**Reach** (spec M7b §17a, after §14's earshot): a person reaches a thing in his keeping, or
lying where he is (aboard, in his place or within earshot of it on the open deck; ashore,
at the same place of the same port). A thing is never put into the keeping of a person a
model or the player holds, nor taken out of it, but by that holder's own act: what is
handed to him lies before him for his own hand, and the director leaves a thing where the
holder can take it and says so.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from freesail.world.places import PLACES, earshot, find_port_place, place_words

__all__ = [
    "OVERBOARD",
    "Thing",
    "ThingWordsError",
    "find",
    "held_by",
    "keeper_of",
    "kept_by",
    "lying_aboard",
    "lying_ashore",
    "make",
    "place_of",
    "read_where",
    "reach_why",
    "the_words",
    "things_of",
    "where_words",
]

# A thing thrown over the side: gone from the ship and the shore, kept in the registry so
# that the truth and a replay know what became of it.
OVERBOARD = "overboard"

# The words a thing's name may open with, which `the_words` turns to 'the'.
_ARTICLES = ("a ", "an ", "some ", "one ", "the ")
# The places aboard a thing may be put in, by the words the places are said in, longest
# first ('sail room' before 'room'; the boat, the shore and the pilot's cutter are not).
_PLACE_WORDS: tuple[tuple[str, str], ...] = tuple(
    sorted(
        (
            [(p.name.removeprefix("the "), p.id) for p in PLACES.values() if p.aboard]
            + [("great cabin", "cabin"), ("wardroom", "gunroom"), ("waist", "deck")]
        ),
        key=lambda x: -len(x[0]),
    )
)
# A spot's first word: the preposition that puts a thing in, on or under something.
_SPOT_LEAD = re.compile(
    r"^(?:in|on|under|beneath|behind|inside|into|upon|onto|at|by|beside)\b", re.I
)
_KEEPING = (
    re.compile(r"^(?:in|into)\s+(?:the\s+)?keeping\s+of\s+(?P<who>.+)$", re.I),
    re.compile(r"^in\s+(?P<who>.+?)['’]s\s+keeping$", re.I),
    re.compile(r"^(?:kept|held|carried)\s+by\s+(?P<who>.+)$", re.I),
)
_ASHORE = re.compile(r"^ashore(?:\s+(?:at|in)\s+(?P<port>.+))?$", re.I)
# 'at the counting house at Plymouth', 'on the quay at Falmouth'
_PLACE_AT_PORT = re.compile(
    r"^(?:at|in|on)\s+(?:the\s+)?(?P<pp>.+?)\s+(?:at|of)\s+(?P<port>[\w' -]+)$", re.I
)
_AT_PORT_PLACE = re.compile(r"^(?:at|in|on)\s+(?:the\s+)?(?P<pp>.+)$", re.I)

WHERE_FORMS = (
    "'in the captain's keeping', 'in the keeping of Mr Veale', 'in the hold', 'on the cabin "
    "table', 'ashore at Plymouth, at the counting house'"
)


class ThingWordsError(ValueError):
    """Words that make or move no thing, in words."""


@dataclass
class Thing:
    """A thing aboard or ashore: its name as said ('a sealed packet'), a description (the
    rest of the words that made it: 'from the Custom House'), and where it is: in a
    person's keeping (`keeper`, his id), or lying in a place (`place`: a place aboard,
    'shore' with its `port` and `ashore_at`, or `OVERBOARD`) at a spot said in words
    (`spot`: 'on the table'). Nothing more."""

    id: str
    name: str
    description: str = ""
    keeper: str = ""
    place: str = ""
    spot: str = ""
    port: str | None = None
    ashore_at: str = ""

    @property
    def the(self) -> str:
        """'the sealed packet' for 'a sealed packet'."""
        return the_words(self.name)

    @property
    def head(self) -> str:
        """The thing's noun, its name's last word ('packet')."""
        words = _key(self.name).split()
        return words[-1] if words else ""

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"id": self.id, "name": self.name}
        for k in ("description", "keeper", "place", "spot", "port", "ashore_at"):
            v = getattr(self, k)
            if v:
                d[k] = v
        return d


def the_words(name: str) -> str:
    """A thing's name with 'the' for its article ('the sealed packet')."""
    low = name.lower()
    for a in _ARTICLES:
        if low.startswith(a):
            return "the " + name[len(a) :]
    return name if low.startswith("the ") else f"the {name}"


def _key(words: str) -> str:
    t = str(words).lower().replace("’", "'")
    t = "".join(c if c.isalnum() or c in " '" else " " for c in t)
    t = " ".join(t.split())
    for a in (*_ARTICLES, "my ", "his ", "her ", "this ", "that ", "your ", "our "):
        if t.startswith(a):
            t = t[len(a) :]
            break
    return t


# ---------------------------------------------------------------------------
# The registry
# ---------------------------------------------------------------------------


def things_of(world: Any) -> list[Thing]:
    """The world's things, in the order made (`People.things`; none for a checkpoint
    from before, and none at all where the world keeps no people)."""
    people = getattr(world, "people", None)
    if people is None:
        return []
    if not getattr(people, "_built", True) and getattr(world.scenario, "things", None):
        _ = people.all  # the scenario's things are made with the people, at their muster
    things = getattr(people, "things", None)
    if things is None:
        things = []
        people.things = things
    return things


def keeper_of(world: Any, thing: Thing) -> Any:
    """The person who keeps the thing, or None."""
    if not thing.keeper:
        return None
    people = getattr(world, "people", None)
    if people is None:
        return None
    return next((p for p in people.all if p.id == thing.keeper), None)


def kept_by(world: Any, person: Any) -> list[Thing]:
    """The things in a person's keeping, in the order made."""
    return [t for t in things_of(world) if t.keeper and t.keeper == person.id]


def place_of(world: Any, thing: Thing) -> tuple[str, str | None, str]:
    """Where the thing is now: (the place, the port, the place ashore). In a person's
    keeping it is where he is (his place aboard, 'boat' or 'cutter' off the ship,
    'shore' at his port and his place ashore)."""
    p = keeper_of(world, thing)
    if p is None:
        return thing.place, thing.port, thing.ashore_at
    if p.aboard:
        return world.people.effective_place(p), None, ""
    if p.where == "shore":
        from freesail.world.movement import ashore_at

        return "shore", p.port, ashore_at(world, p)
    return p.where, None, ""


def find(world: Any, words: str) -> list[Thing]:
    """The things the words name ('the packet', 'the sealed packet', 'the brandy'), not
    thrown overboard: its name whole, or its noun, or words all of its name's ending in
    its noun; none when the words name nothing known."""
    key = _key(words)
    if not key:
        return []
    out = []
    for t in things_of(world):
        if t.place == OVERBOARD and not t.keeper:
            continue
        name = _key(t.name)
        words_of = set(name.split())
        said = key.split()
        if key == name or (said and said[-1] == t.head and set(said) <= words_of):
            out.append(t)
            continue
        # 'the cask' or 'the brandy' for 'a cask of brandy': either side of 'of' names it
        if " of " in name and key in name.split(" of ", 1):
            out.append(t)
    return out


def _person(world: Any, words: str) -> Any:
    people = getattr(world, "people", None)
    return people.find(words) if people is not None else None


# ---------------------------------------------------------------------------
# Where, in words
# ---------------------------------------------------------------------------


def _port(world: Any, pid: str | None) -> Any:
    ports = getattr(world, "ports", None)
    if ports is None or not pid:
        return None
    return ports.ports.get(pid)


def _ashore_words(world: Any, port_id: str | None, ashore_at: str, spot: str = "") -> str:
    from freesail.world.movement import ashore_place_words

    port = _port(world, port_id)
    if port is None:
        return "ashore"
    at = ashore_place_words(ashore_at or "quay", port)
    if spot:
        return f"{spot}, ashore at {port.name}, {at}"
    return f"ashore at {port.name}, {at}"


def where_words(world: Any, thing: Thing, keeper_where: bool = True) -> str:
    """Where a thing is in words: 'in Mr Veale's keeping, ashore at Plymouth, at the
    counting house', 'on the table in the cabin', 'in the hold', 'over the side'."""
    p = keeper_of(world, thing)
    if p is not None:
        if not keeper_where:
            return f"in {p.name}'s keeping"
        return f"in {p.name}'s keeping, {world.people.state_words(p)}"
    if thing.place == OVERBOARD:
        return "thrown over the side"
    if thing.place == "shore":
        return _ashore_words(world, thing.port, thing.ashore_at, thing.spot)
    where = place_words(thing.place) if thing.place else "aboard"
    return f"{thing.spot} {where}" if thing.spot else where


def lying_aboard(world: Any) -> dict[str, list[Thing]]:
    """The things lying in each place aboard (in nobody's keeping), by place."""
    out: dict[str, list[Thing]] = {}
    for t in things_of(world):
        if not t.keeper and t.place in PLACES and PLACES[t.place].aboard:
            out.setdefault(t.place, []).append(t)
    return out


def lying_ashore(world: Any, port_id: str) -> dict[str, list[Thing]]:
    """The things lying at each place ashore of a port (in nobody's keeping), by place."""
    out: dict[str, list[Thing]] = {}
    for t in things_of(world):
        if not t.keeper and t.place == "shore" and t.port == port_id:
            out.setdefault(t.ashore_at or "quay", []).append(t)
    return out


def lying_words(t: Thing) -> str:
    """'a sealed packet on the table', 'a cask of brandy': a thing as its place lists it."""
    return f"{t.name} {t.spot}" if t.spot else t.name


# ---------------------------------------------------------------------------
# Reach
# ---------------------------------------------------------------------------


def held_by(world: Any, person: Any) -> str | None:
    """Who holds the person's station ('a model', 'the player at his seat', 'the player
    at the prompt'), or None when nobody does (the rule of reach's question)."""
    from freesail.world.orders import held_stations

    if person is None:
        return None
    try:
        held = held_stations(world)
    except Exception:  # noqa: BLE001  (a world with no stations holds nobody)
        return None
    for _station, name, who in held:
        if name and name == person.name:
            return who
    return None


def _where_of_person(world: Any, person: Any) -> tuple[str, str | None, str]:
    if person.aboard:
        return world.people.effective_place(person), None, ""
    if person.where == "shore":
        from freesail.world.movement import ashore_at

        return "shore", person.port, ashore_at(world, person)
    return person.where, None, ""


def same_place(a: tuple[str, str | None, str], b: tuple[str, str | None, str]) -> bool:
    """Whether two places are within reach of each other: aboard, the same place or the
    open deck's earshot; ashore, the same place of the same port; in the boat, the boat."""
    if a[0] == "shore" or b[0] == "shore":
        return a[0] == b[0] and a[1] == b[1] and (a[2] or "quay") == (b[2] or "quay")
    if a[0] in PLACES and PLACES[a[0]].aboard and b[0] in PLACES and PLACES[b[0]].aboard:
        return b[0] in earshot(a[0]) or a[0] == b[0]
    return a[0] == b[0]


def reach_why(world: Any, person: Any, thing: Thing) -> str | None:
    """Why the person cannot lay hands on the thing, in words, or None when he can: it
    is his, or it lies where he is."""
    if thing.keeper == person.id:
        return None
    other = keeper_of(world, thing)
    if other is not None:
        return f"{thing.the} is in {other.name}'s keeping"
    if thing.place == OVERBOARD:
        return f"{thing.the} went over the side"
    here = _where_of_person(world, person)
    if same_place(here, place_of(world, thing)):
        return None
    return f"{thing.the} is {where_words(world, thing)}"


def person_reach_why(world: Any, giver: Any, other: Any) -> str | None:
    """Why the giver cannot hand a thing to the other, or None when he is within reach."""
    if same_place(_where_of_person(world, giver), _where_of_person(world, other)):
        return None
    return f"{other.name} is {world.people.state_words(other)}, out of your reach"


# ---------------------------------------------------------------------------
# Made from words
# ---------------------------------------------------------------------------


def _place_in(phrase: str) -> tuple[str, str] | None:
    """(the place aboard, the spot's words) a phrase names: 'in the hold' -> ('hold', ''),
    'on the cabin table' -> ('cabin', 'on the table'), 'on the table in the cabin' ->
    ('cabin', 'on the table'); None when it names no place aboard."""
    low = " ".join(phrase.lower().replace("’", "'").split())
    if not _SPOT_LEAD.match(low):
        return None
    for words, pid in _PLACE_WORDS:
        m = re.search(rf"\b(?:the\s+|his\s+|the\s+captain's\s+)?{re.escape(words)}\b", low)
        if m is None:
            continue
        before, after = low[: m.start()].strip(), low[m.end() :].strip()
        # 'on the table in the cabin': the place's own preposition goes with it
        for prep in (" in", " on", " aboard in", " of"):
            if before.endswith(prep) and before != prep.strip():
                before = before[: -len(prep)].strip()
                break
        spot = " ".join(x for x in (before, after) if x)
        if spot in ("in", "on", "into", "inside", "at", "in the", "on the"):
            spot = ""
        elif after and before in ("in", "on", "into", "inside", "at", "under", "beneath"):
            spot = f"{before} the {after}"  # 'on the cabin table' -> 'on the table'
        return pid, spot
    return None


def read_where(world: Any, phrase: str) -> dict[str, Any] | None:
    """The where of a phrase: {keeper}, {place, spot}, or {place: 'shore', port,
    ashore_at}; None when the phrase says no where. ThingWordsError for a keeping that
    names nobody, or a port the world has not got."""
    text = " ".join(str(phrase).split()).strip()
    low = text.lower()
    for rx in _KEEPING:
        m = rx.match(text)
        if m is not None:
            who = m.group("who").strip()
            p = _person(world, who)
            if p is None:
                raise ThingWordsError(
                    f"nobody answering to '{who}' is among the people; a person is made first "
                    "('person: make \"<name>\", <who he is>, <where>')"
                )
            return {"keeper": p.id}
    if low in ("aboard", "on board"):
        return {}
    m = _ASHORE.match(text)
    if m is not None:
        ports = getattr(world, "ports", None)
        words = (m.group("port") or "").strip()
        if words:
            port = ports.find(words) if ports is not None else None
            if port is None:
                raise ThingWordsError(f"'{words}' is no port of the world")
        else:
            near = ports.nearest() if ports is not None else None
            if near is None:
                raise ThingWordsError("ashore where? Say 'ashore at <port>'")
            port = near[0]
        return {"place": "shore", "port": port.id, "ashore_at": "quay"}
    found = _place_in(text)
    if found is not None:
        return {"place": found[0], "spot": found[1]}
    ports = getattr(world, "ports", None)
    m = _PLACE_AT_PORT.match(text)
    if m is not None and ports is not None:
        port = ports.find(m.group("port"))
        if port is not None:
            pp = find_port_place(port, m.group("pp"))
            if pp is not None:
                return {"place": "shore", "port": port.id, "ashore_at": pp.id}
    return None


def make(world: Any, words: str) -> tuple[Thing, dict[str, Any], bool]:
    """A thing from words, '<its name>, <where it is>[, <more of it>]' (`aboard: ...`, a
    scenario's `things:`): (the thing, where as read, whether it is a thing already known
    and moved). A name that opens with 'the' and names a thing known moves it; any other
    makes one. ThingWordsError in words when no where is said or a where names nothing."""
    phrases = [" ".join(x.split()) for x in str(words).split(",") if x.strip()]
    if len(phrases) < 2:
        raise ThingWordsError(f"say what it is and where: '<a thing>, <where>' ({WHERE_FORMS})")
    name = phrases[0].rstrip(".")
    where: dict[str, Any] | None = None
    said: list[str] = []
    for phrase in phrases[1:]:
        phrase = phrase.rstrip(".")
        got = read_where(world, phrase)
        if got is None:
            # a place ashore after 'ashore at <port>': 'at the counting house'
            if where is not None and where.get("place") == "shore":
                m = _AT_PORT_PLACE.match(phrase)
                port = _port(world, where.get("port"))
                pp = find_port_place(port, m.group("pp")) if (m and port is not None) else None
                if pp is not None:
                    where["ashore_at"] = pp.id
                    continue
            said.append(phrase)
            continue
        if not got:
            continue  # 'aboard' said alone
        if where is None:
            where = got
        else:
            said.append(phrase)
    if where is None:
        raise ThingWordsError(f"say where {the_words(name)} is: {WHERE_FORMS}")
    known = find(world, name) if name.lower().startswith("the ") else []
    if len(known) > 1:
        raise ThingWordsError(
            f"'{name}' names {len(known)} things: "
            + "; ".join(f"{t.name}, {where_words(world, t)}" for t in known)
        )
    if known:
        thing = known[0]
        moved = True
    else:
        thing = Thing(_new_id(world, name), name)
        moved = False
        if said:
            thing.description = "; ".join(said)
    return thing, where, moved


def put(thing: Thing, where: dict[str, Any]) -> None:
    """The thing put where the words say: a keeping, a place aboard with its spot, or a
    place ashore."""
    thing.keeper = str(where.get("keeper") or "")
    thing.place = "" if thing.keeper else str(where.get("place") or "")
    thing.spot = "" if thing.keeper else str(where.get("spot") or "")
    thing.port = None if thing.keeper else where.get("port")
    thing.ashore_at = "" if thing.keeper else str(where.get("ashore_at") or "")


def _new_id(world: Any, name: str) -> str:
    base = re.sub(r"[^a-z0-9]+", "_", _key(name)).strip("_") or "thing"
    ids = {t.id for t in things_of(world)}
    if base not in ids:
        return base
    n = 2
    while f"{base}_{n}" in ids:
        n += 1
    return f"{base}_{n}"
