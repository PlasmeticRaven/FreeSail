"""The free lines (spec M7b §17a; package 53b): a short list of verbs that take any words
after them and do what the game can with them, no more, saying so in the log in the words
as used.

    give <thing> to <person>        the thing into his keeping (`hand ... to ...` the same;
                                    `give <person> <thing>` too)
    show <thing> to <person>        said, and nothing moves
    take <thing>                    a thing lying where he is into his own keeping
    stow <thing> in <place>         the thing put down: in a place aboard he is in or within
    hide <thing> in <place>         earshot of, or at the spot the words say in his own place
    put <thing> in/on <place>       ('on the table', 'in the bread locker'); ashore, at the
                                    place of the port he is at
    open <thing>, read <thing>      said, and nothing moves
    throw <thing> overboard         the thing over the side

beside the needs' `eat` and `drink` (package 54), which take any words after the verb and
are answered to the person alone as they always were (the vocabulary's `free_lines`).

**What the game does with them.** The giver is the order's person (`movement.
person_of_actor`: the captain at the prompt, a station's person at his station); a rule,
a standing order's firing and the director have no hands aboard and are refused in words.
Where the words name a thing known (`world.things`) within his reach (in his keeping, or
lying where he is) and, for a giving, a person within his reach (in his place or within
earshot of it aboard, at the same place of the same port ashore), the thing moves and the
log says where it is now ("By the captain, on the quarterdeck: gave the packet to Mr
Veale; the sealed packet is in Mr Veale's keeping."). Where they do not, or the verb moves
nothing (show, open, read), the line is accepted as said and nothing moves, the log saying
**"as said; nothing of the ship's changed"** in those words with the reason when a thing or
a person was named, so that the record and the replay stay honest and no model learns that
the ship did what it only said. A thing handed to a person a model or the player holds is
not put into his keeping without his own act: it lies before him, for his own hand to take.

**Heard where it is said.** A free line is a notable line of the log (`free.line`), heard
by the stations held within earshot of the giver as a word on deck (`Harness.hear`, the
stand-by's "a word on deck"), and read by the director in his sample as he reads the deck's
conversation. It is journaled as the order it is, so that a replay says it again and moves
the thing again.
"""

from __future__ import annotations

import re
from typing import Any

from freesail.orders.errors import OrderError
from freesail.orders.prompt import world_of

__all__ = ["AS_SAID", "FREE_KIND", "PAST", "execute", "hand_line"]

Result = tuple[str, str, dict[str, Any]]

# The log's kind for a free line, and the words of a line accepted as said.
FREE_KIND = "free.line"
AS_SAID = "as said; nothing of the ship's changed"

# Each free verb phrase in the past, for the log's line in the words as used.
PAST: dict[str, str] = {
    "give": "gave",
    "hand": "handed",
    "show": "showed",
    "take": "took",
    "pick up": "picked up",
    "stow": "stowed",
    "hide": "hid",
    "conceal": "concealed",
    "put": "put",
    "open": "opened",
    "unseal": "unsealed",
    "break the seal of": "broke the seal of",
    "read": "read",
    "throw": "threw",
    "toss": "tossed",
}

# The words a thing is put in, on or under something by (stow, hide, put).
_PUT_PREPS = ("in", "into", "on", "onto", "under", "inside", "behind", "beneath", "upon", "at")
_OVERBOARD = re.compile(
    r"^(?P<thing>.+?)\s+(?:overboard|over\s+board|over\s+the\s+side|into\s+the\s+sea)\.?$", re.I
)


def hand_line(text: str) -> bool:
    """Whether words the sail's `hand` could not read are a giving: `hand <thing> to
    <person>` (a bare `hand` is the sail's, `take in`; package 53b)."""
    low = " ".join(str(text).lower().split())
    return low.startswith("hand ") and " to " in low


def _said_words(text: str, phrase: str) -> tuple[str, str]:
    """(the words after the verb as said, the line's words in the past): 'give the packet
    to Mr Veale' -> ('the packet to Mr Veale', 'gave the packet to Mr Veale')."""
    raw = " ".join(str(text).split()).rstrip(".")
    n = len(phrase.split())
    rest = " ".join(raw.split(" ")[n:]).strip()
    past = PAST.get(phrase, phrase)
    return rest, f"{past} {rest}".strip()


def _who(world: Any, person: Any) -> str:
    return "the captain" if person is world.people.captain else person.name


def execute(ship: Any, text: str, verb: str, phrase: str) -> Result:
    """A free line given by the person of the order's actor: the thing moved where the words
    name one within reach, else the line as said; (the log's kind, its words, its data)."""
    from freesail.world import movement
    from freesail.world import things as TH

    world = world_of(ship)
    if world is None or getattr(world, "people", None) is None:
        raise OrderError("There is nobody here to do it: the ship is not in a world.")
    actor = str((getattr(ship, "extra", None) or {}).get("order_actor") or "captain")
    person = movement.person_of_actor(world, actor)
    if person is None:
        raise OrderError(
            f"'{' '.join(str(text).split())}' is a person's own, said where he stands; a "
            "standing order, a rule and the director have no hands aboard."
        )
    rest, done = _said_words(text, phrase)
    if not rest:
        raise OrderError(f"{phrase.capitalize()} what? Say the words after '{phrase}'.")
    moved, outcome, why, thing, to = _carry_out(world, person, verb, rest)
    where = movement.where_words(world, person)
    who = _who(world, person)
    if moved:
        line = f"By {who}, {where}: {done}; {outcome}."
    else:
        line = f"By {who}, {where}: {done}, {AS_SAID}" + (f" ({why})." if why else ".")
    heard = _hearers(world, person)
    for h in heard:
        h.hear(line)
    here = TH._where_of_person(world, person)
    data: dict[str, Any] = {
        "verb": verb,
        "said": " ".join(str(text).split()),
        "person": person.name,
        "place": here[0],
        "moved": moved,
        "heard_by": [h.station.name for h in heard],
        "notable": True,
    }
    if thing is not None:
        data["thing"] = thing.id
    if to is not None:
        data["to"] = to.name
    return FREE_KIND, line, data


def _carry_out(world: Any, person: Any, verb: str, rest: str) -> tuple[bool, str, str, Any, Any]:
    """(moved, the outcome's words, the reason nothing moved or "", the thing, the person
    given to) for a free line's words."""
    from freesail.world import things as TH

    if verb in ("give", "show"):
        thing, to = _thing_and_person(world, rest)
        if thing is None:
            return False, "", "", None, to
        if to is None:
            return (
                False,
                "",
                f"nobody named is among the people; {thing.the} stays as it was",
                thing,
                None,
            )
        if verb == "show":
            return False, "", "", thing, to
        if to is person:
            return False, "", f"{thing.the} is yours to give, not to take", thing, to
        why = TH.reach_why(world, person, thing) or TH.person_reach_why(world, person, to)
        if why:
            return False, "", why, thing, to
        held = TH.held_by(world, to)
        if held:
            place, port, ashore_at, hull = TH._where_of_person(world, to)
            TH.put(
                thing,
                {
                    "place": place,
                    "spot": f"before {to.name}",
                    "port": port,
                    "ashore_at": ashore_at,
                    "hull": hull,
                },
            )
            return (
                True,
                f"{thing.the} lies before {to.name}, for his own hand to take ('take "
                f"{thing.the.removeprefix('the ')}')",
                "",
                thing,
                to,
            )
        TH.put(thing, {"keeper": to.id})
        return True, f"{thing.the} is in {_who(world, to)}'s keeping", "", thing, to
    if verb in ("open", "read"):
        thing = _one(world, person, rest)
        return False, "", "" if thing is not None else "", thing, None
    if verb == "take":
        words = re.split(r"\s+from\s+", rest, maxsplit=1, flags=re.I)[0]
        thing = _one(world, person, words) or _one(world, person, rest)
        if thing is None:
            return False, "", "", None, None
        if thing.keeper == person.id:
            return False, "", f"{thing.the} is in your keeping already", thing, None
        why = TH.reach_why(world, person, thing)
        if why:
            return False, "", why, thing, None
        TH.put(thing, {"keeper": person.id})
        return True, f"{thing.the} is in {_who(world, person)}'s keeping", "", thing, None
    if verb == "throw":
        m = _OVERBOARD.match(rest)
        thing = (
            _one(world, person, m.group("thing")) if m is not None else _one(world, person, rest)
        )
        if thing is None:
            return False, "", "", None, None
        if m is None:
            return (
                False,
                "",
                f"{thing.the} goes nowhere but over the side by these words",
                thing,
                None,
            )
        if not person.aboard and person.where != "boat":
            return False, "", "you are ashore, with no side to throw it over", thing, None
        why = TH.reach_why(world, person, thing)
        if why:
            return False, "", why, thing, None
        TH.put(thing, {"place": TH.OVERBOARD})
        return True, f"{thing.the} went over the side", "", thing, None
    # stow, hide, put
    thing, dest = _thing_and_dest(world, person, rest)
    if thing is None:
        return False, "", "", None, None
    if not dest:
        return False, "", f"say where: '{verb} {thing.the} in the hold'", thing, None
    why = TH.reach_why(world, person, thing)
    if why:
        return False, "", why, thing, None
    where, why = _destination(world, person, dest)
    if where is None:
        return False, "", why, thing, None
    TH.put(thing, where)
    return True, f"{thing.the} is {TH.where_words(world, thing)}", "", thing, None


def _one(world: Any, person: Any, words: str) -> Any:
    """The one thing the words name, the one within his reach where they name several;
    None when they name none, or several within reach."""
    from freesail.world import things as TH

    found = TH.find(world, words)
    if len(found) <= 1:
        return found[0] if found else None
    near = [t for t in found if TH.reach_why(world, person, t) is None]
    return near[0] if len(near) == 1 else None


def _thing_and_person(world: Any, rest: str) -> tuple[Any, Any]:
    """(the thing, the person) of 'the packet to Mr Veale' or 'Mr Veale the packet'; either
    None where the words name none."""
    from freesail.world import things as TH

    people = world.people
    words = rest.split()
    low = [w.lower() for w in words]
    thing = person = None
    for i in range(len(words) - 1, 0, -1):
        if low[i] != "to":
            continue
        t = TH.find(world, " ".join(words[:i]))
        p = people.find_anywhere(" ".join(words[i + 1 :]))
        if t or p:
            thing = thing or (t[0] if len(t) == 1 else None)
            person = person or p
        if len(t) == 1 and p is not None:
            return t[0], p
    for i in range(1, len(words)):
        p = people.find_anywhere(" ".join(words[:i]))
        t = TH.find(world, " ".join(words[i:]))
        if p is not None and len(t) == 1:
            return t[0], p
    if thing is None:
        t = TH.find(world, rest)
        thing = t[0] if len(t) == 1 else None
    return thing, person


def _thing_and_dest(world: Any, person: Any, rest: str) -> tuple[Any, str]:
    """(the thing, the words of where it goes) of 'the packet in the bread locker'."""
    words = rest.split()
    for i in range(1, len(words)):
        if words[i].lower() not in _PUT_PREPS:
            continue
        thing = _one(world, person, " ".join(words[:i]))
        if thing is not None:
            return thing, " ".join(words[i:])
    return _one(world, person, rest), ""


def _destination(world: Any, person: Any, dest: str) -> tuple[dict[str, Any] | None, str]:
    """Where the words put a thing down, within the giver's reach: a place aboard he is in
    or within earshot of, or a spot in his own place; ashore, his place of the port or a
    spot in it. (None, the reason) where the words name a place out of his reach."""
    from freesail.world import things as TH
    from freesail.world.places import PLACES, find_port_place

    here = TH._where_of_person(world, person)
    if here[0] == "shore":
        port = TH._port(world, here[1])
        pp = None
        m = re.match(r"^(?:in|into|on|at|inside)\s+(?:the\s+)?(?P<pp>.+)$", dest, re.I)
        if port is not None and m is not None:
            pp = find_port_place(port, m.group("pp"))
        if pp is not None and pp.id != (here[2] or "quay"):
            return None, f"{pp.name} is not where you are; go there first"
        return {
            "place": "shore",
            "port": here[1],
            "ashore_at": here[2] or "quay",
            "spot": "" if pp is not None else dest,
        }, ""
    found = TH._place_in(dest)
    if found is not None:
        place, spot = found
        if not TH.same_place(here, (place, None, "", here[3])):
            return None, f"{PLACES[place].name} is not where you are; go there first"
        return {"place": place, "spot": spot, "hull": here[3]}, ""
    return {"place": here[0], "spot": dest, "hull": here[3]}, ""


def _hearers(world: Any, person: Any) -> list[Any]:
    """The stations held within the giver's reach (his place or its earshot aboard, his
    place of the port ashore), not his own: a free line is heard where it is said."""
    from freesail.agents.agent import DIRECTOR
    from freesail.agents.harness import _stations_held
    from freesail.world import things as TH

    here = TH._where_of_person(world, person)
    out = []
    for h in _stations_held(world):
        name = getattr(h.station, "person", "") or ""
        if h.station.name == DIRECTOR or not name or name == person.name:
            continue
        other = world.people.find(name)
        if other is None or other is person:
            continue
        if TH.same_place(here, TH._where_of_person(world, other)):
            out.append(h)
    return out
