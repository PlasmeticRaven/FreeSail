"""The ship's stations as data, bound at run time (spec M6 §11 as built; package 41, the
owner's word of 2026-10-10 through the lead).

A station is a post a model or the player may hold through a door: the watcher's, the
officer of the watch's, the captain's, the master's, the lookout's, a passenger's. Which
stations a ship has, and which person of her company holds each, is a **binding on the
World** (`World.stations`, this class), never a table in code: the wardroom file's
`stations:` (`data/people/<ship>.yaml`, `People.holder`) is only its starting state, and
two operations move it, which the harness uses now and a world order will drive later
(M7b's `person: "Mr Fox" comes aboard as master`, on the existing `person:` channel):

- `bind(name, person, kind=...)`: the station named is bound to a person of the ship's
  company (or to nobody named, as the watcher's and a passenger's may be); a station
  bound is one a door may ask for, and its brief is built from the person's own outline
  (`Person.outline`: his rank, his station aboard, his history), so that a person made
  from words later carries what a station's brief needs.
- `unbind(name, why)`: the station is no longer aboard; a model holding it is released
  with a line saying why, as `stand down` does, and a door asking for it afterwards is
  refused in words.

What a station of each **kind** may do (its domain, its brief's form, its policy) is
code (`freesail.agents.agent.STATION_FACTORIES`, by the kind's name); which stations a
ship has, under which names and held by whom, is this data. A station's name is its
kind's by default (`master`), and a binding may give another name to a station of a
kind (a second passenger as `supercargo`), so that the set is the ship's own.

Nothing here makes a person from words or gives the story's reasons: those are the
director's (M7b). The save carries the bindings made (`to_dict`, `load`), and a
checkpoint carries the object. **Each bind and unbind is an input** (package 42): kept in
`World.inputs` at its tick (`{"binding": {"op", "name", "person", "kind", "why"}}`) and
made again there by a replay (`core.replay._give`, with `quiet`), by either of its roads,
so that a binding made by hand, or by the world order to come, replays with the game; a
station a binding stands down journals its acts inside it, which a replay by the acts
gives in their place.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from freesail.core.events import Severity

if TYPE_CHECKING:
    from freesail.core.world import World
    from freesail.world.people import Person

__all__ = ["BOUND_KIND", "UNBOUND_KIND", "Binding", "Stations"]

BOUND_KIND = "station.bound"
UNBOUND_KIND = "station.unbound"


@dataclass(frozen=True)
class Binding:
    """One station aboard: its name (as the log and the doors name it), its kind (the
    name of a factory in `agent.STATION_FACTORIES`), and the person who holds it by
    name ("" for nobody named: the watcher's, a passenger's before anyone is aboard)."""

    name: str
    kind: str
    person: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "kind": self.kind, "person": self.person}


def _key(words: str) -> str:
    return " ".join(str(words or "").lower().split())


class Stations:
    """The binding on one World. Lazy where the wardroom is: the people are mustered
    after the World is made, so a station bound by nobody's hand is read from the
    wardroom file when it is asked for, and a binding made by hand stands over it."""

    def __init__(self, world: World) -> None:
        self.world = world
        self._bound: dict[str, Binding] = {}  # made by hand, by station name
        self._unbound: set[str] = set()

    # -- the kinds --------------------------------------------------------------------

    @staticmethod
    def kinds() -> tuple[str, ...]:
        from freesail.agents.agent import STATION_FACTORIES

        return tuple(STATION_FACTORIES)

    @staticmethod
    def _factory(kind: str) -> Any:
        from freesail.agents.agent import STATION_FACTORIES

        return STATION_FACTORIES.get(kind)

    # -- what is aboard -----------------------------------------------------------------

    def names(self) -> tuple[str, ...]:
        """The stations aboard now: every kind's own station unless unbound, and the
        stations bound by hand under other names, in the kinds' order then the hand's."""
        out = [k for k in self.kinds() if k not in self._unbound]
        for name in self._bound:
            if name not in out and name not in self._unbound:
                out.append(name)
        return tuple(out)

    def aboard(self, name: str) -> bool:
        return _key(name) in self.names()

    def binding(self, name: str) -> Binding | None:
        """The station's binding, or None when it is not aboard."""
        key = _key(name)
        if key in self._unbound:
            return None
        if key in self._bound:
            return self._bound[key]
        if key in self.kinds():
            person = self._file_holder(key)
            return Binding(key, key, person.name if person is not None else "")
        return None

    def kind_of(self, name: str) -> str | None:
        b = self.binding(name)
        return b.kind if b is not None else None

    def factory(self, name: str) -> Any:
        """The factory that makes the station's `Station` (`agent.STATION_FACTORIES`), or
        None when no such station is aboard."""
        b = self.binding(name)
        return self._factory(b.kind) if b is not None else None

    def _file_holder(self, name: str) -> Person | None:
        people = getattr(self.world, "people", None)
        if people is None:
            return None
        try:
            return people.holder(name)
        except Exception:  # a people's build that cannot run binds nobody
            return None

    def holder(self, name: str) -> Person | None:
        """The person who holds the station by the binding: one bound by hand, by his
        name among the people; else the wardroom file's (`People.holder`); None for a
        station bound to nobody named or not aboard."""
        key = _key(name)
        if key in self._unbound:
            return None
        if key in self._bound:
            who = self._bound[key].person
            people = getattr(self.world, "people", None)
            return people.find(who) if (who and people is not None) else None
        return self._file_holder(key)

    def words(self) -> list[str]:
        """Each station aboard with its holder, for `the stations` and the owner."""
        out = []
        for name in self.names():
            b = self.binding(name)
            if b is None:
                continue
            kind = f", a {b.kind}'s" if b.kind != b.name else ""
            held = f" ({b.person})" if b.person else " (nobody named)"
            out.append(f"the {name}{kind}{held}")
        return out

    # -- the two operations -----------------------------------------------------------

    def _input(self, op: str, name: str, **rest: Any) -> None:
        """The binding's change kept as an input (package 42), before it is made, so that
        what it makes (a station stood down) is journaled after it."""
        world = self.world
        inputs = getattr(world, "inputs", None)
        if inputs is not None:
            entry = {"op": op, "name": name, **{k: v for k, v in rest.items() if v}}
            inputs.append({"tick": world.clock.tick, "binding": entry})

    def bind(
        self,
        name: str,
        person: Person | str | None,
        kind: str | None = None,
        quiet: bool = False,
    ) -> str:
        """Bind a station to a person (one of the ship's company, by his `Person` or his
        name; None or "" for nobody named). `kind` names the station's kind for a new
        name (a station named as its kind needs none); a kind that is none is refused in
        words. A station held while it is bound anew keeps its holder: the person the
        station is bound to changes under him, and his next brief names the new one.
        Returns the log's line, which is recorded."""
        key = _key(name)
        if not key:
            raise ValueError("A station wants a name to be bound under.")
        kind = _key(kind) if kind else (self._bound[key].kind if key in self._bound else key)
        if kind not in self.kinds():
            raise ValueError(
                f"There is no kind of station '{kind}'; the kinds: {', '.join(self.kinds())}."
            )
        who = ""
        if person:
            who = str(getattr(person, "name", person))
            people = getattr(self.world, "people", None)
            if people is not None and people.find(who) is None:
                raise ValueError(f"{who} is not one of the ship's company; nobody by that name.")
        if not quiet:
            self._input("bind", key, person=who, kind=kind)
        self._unbound.discard(key)
        self._bound[key] = Binding(key, kind, who)
        held = (f" ({who})" if who else " (nobody named)") + (
            f", a {kind}'s station" if kind != key else ""
        )
        text = f"The {key}'s station is bound{held}."
        self._record(
            Severity.ROUTINE,
            BOUND_KIND,
            text,
            data={"station": key, "kind": kind, "person": who},
        )
        return text

    def unbind(self, name: str, why: str = "", quiet: bool = False) -> str:
        """The station is no longer aboard: a model holding it is released with a line
        saying why, as `stand down` does (the game saved, the station's journal kept),
        the player's seat at it stood down, and a door asking for it afterwards refused
        in words. Returns the log's line, which is recorded."""
        key = _key(name)
        if key not in self.names():
            raise ValueError(f"There is no {key}'s station aboard to unbind.")
        world = self.world
        why = " ".join(str(why or "").split()) or "the station is no longer aboard"
        if not quiet:
            self._input("unbind", key, why=why)
        reason = f"the {key}'s station is unbound: {why}"
        held = (getattr(world, "agents", None) or {}).get(key)
        if held is not None and not held.agent.released:
            held.stand_down(reason, by="the ship")
        seat = getattr(world, "player_seat", None)
        if seat is not None and seat.station.name == key and not seat.agent.released:
            seat.request_stand_down(reason, by="the ship")
        self._bound.pop(key, None)
        self._unbound.add(key)
        text = f"The {key}'s station is unbound: {why}."
        self._record(Severity.ROUTINE, UNBOUND_KIND, text, data={"station": key, "why": why})
        return text

    def _record(self, *args: Any, **kw: Any) -> Any:
        """The binding's own line: the input's, never a station's act, even when a
        station's act made the change (package 42)."""
        from freesail.core import acts

        with acts.aside(self.world):
            return self.world.record(*args, **kw)

    # -- the save -----------------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        return {
            "bound": [b.to_dict() for b in self._bound.values()],
            "unbound": sorted(self._unbound),
        }

    def load(self, d: dict[str, Any] | None) -> None:
        if not d:
            return
        for entry in d.get("bound") or []:
            b = Binding(
                str(entry["name"]),
                str(entry.get("kind") or entry["name"]),
                str(entry.get("person") or ""),
            )
            self._bound[b.name] = b
        self._unbound = {str(n) for n in d.get("unbound") or []}
