"""A station's acts as inputs (spec M6 §14; decision 36's replay on any build; package 42,
item 3).

Until this package a station's part of a game was replayed from its transcript: its
recorded replies were handed back wherever the replaying build's sampling opened a turn,
so a build that samples otherwise (another wake, another glass, another fold) replays
another game. Now **everything a station puts into the World is journaled at its tick as
an input**, as the driver's lines are, and a replay applies it there whatever the build's
sampling would have asked: the transcript is the record, and no longer the replay's
source.

**What is journaled** (`World.station_acts`; the save's `station_acts`). While a station's
harness acts (its seating, its turn on a tick or an order, a reply delivered, an act from
a door; the entry points carry `frame`), each thing it does to the World is an entry with
the tick and the count of inputs before it (`after_inputs`), in order:

- `seated`: the station taken, its definition and the harness's whole state; a replay
  builds the station here;
- `order`: an order the station gave (`World.submit` with the station's actor, the words
  the log says it in): given again, so that the ship, the book and every station under it
  carry it out again; what it writes into the log is written by giving it, and is not
  journaled apart;
- `line`: a line of the station's in the log (its words, a refusal, a stand-by, a nudge,
  a pause, the deck given back, a leaving), written again as it was;
- `note`: an entry in the station's journal, written again;
- `state`: what changed of the station's state (its agent's counters and the deck, its
  stand-by, its grants, who sits there), set again, before each order the station gives
  and at the end of each act, so that what the player's own orders find of it (the
  deck, a stand-by, a pause) is what they found in play.

A line the World writes of itself, a driver's line and the player's orders are inputs or
consequences of inputs as before, and are not journaled here. An order given inside an
order (the captain's station telling the officer he has the deck) is the outer order's.

**The replay's rule** (`core.replay.replay`): a save whose every station's acts are inputs
(`agents[i].acts`) and which another build wrote is replayed by its acts, each at its tick
after as many inputs as came before it in play; the harness is driven by them (`driven`:
it samples nothing and asks no model) until the replay ends, when it takes up the game
from where it stands, its conversation beginning at its brief when a door takes it over.
A save of this build is replayed from its transcript as it always was, which rebuilds the
station's conversation too (and the REPL's turn mode depends on it); both roads give the
same log (`tests/test_replay.py`). A save from before this package has no acts and
replays as before: from its checkpoint, or on the build that wrote it.

**Anything else a station changes in the World** must come through an order, a line, its
journal or its state, or journal its own entry (`record(world, station, kind, payload)`
with an applier registered in `APPLIERS`); a tool that wrote the World some other way
would replay by its acts without it.
"""

from __future__ import annotations

import contextlib
import dataclasses
import functools
import importlib
from collections.abc import Callable
from typing import Any

__all__ = [
    "APPLIERS",
    "HARNESS_FIELDS",
    "capturing",
    "frame",
    "give",
    "line",
    "note",
    "order",
    "record",
    "saved",
]

# The harness's own fields that are its state beside the agent's (`AgentState`): who sits
# at the station and through which door, what the save says of the seating, the deck held
# while paused, a stand-down the captain ordered and not yet carried out.
HARNESS_FIELDS: tuple[str, ...] = (
    "model_name",
    "door",
    "first_model_name",
    "first_door",
    "budget_tokens",
    "reserve_tokens",
    "stand_by_ends_turn",
    "_deck_was",
    "_stand_down_requested",
    "_start_after_orders",
    "_start_after_inputs",
)

# The agent's fields that are not state to set (the station it serves is the harness's).
SKIPPED = ("station",)


class _Frame:
    __slots__ = ("capture", "station")

    def __init__(self, station: str, capture: bool):
        self.station = station
        self.capture = capture


def _frames(world: Any) -> list[_Frame] | None:
    return getattr(world, "_acts_frames", None)


def capturing(world: Any) -> bool:
    """Whether a station is acting now and what it writes is to be journaled."""
    f = _frames(world)
    return bool(f) and f[-1].capture


def _entry(world: Any, station: str, kind: str, payload: Any) -> None:
    world.station_acts.append(
        {
            "tick": world.clock.tick,
            "after_inputs": len(world.inputs),
            "station": station,
            kind: payload,
        }
    )


@contextlib.contextmanager
def aside(world: Any) -> Any:
    """What is written meanwhile is an input's or the World's own, not a station's act
    (a binding's line, package 41's; a harness's entry point inside it journals its own)."""
    frames = _frames(world)
    if frames is None:
        yield
        return
    frames.append(_Frame(frames[-1].station if frames else "", False))
    try:
        yield
    finally:
        frames.pop()


def record(world: Any, station: str, kind: str, payload: Any) -> None:
    """An act of a kind the appliers know, journaled while a station acts (for a tool
    that changes the World by a road of its own; `APPLIERS`)."""
    if capturing(world):
        _entry(world, station, kind, payload)


# ---------------------------------------------------------------------------
# The hooks the World and the journal call
# ---------------------------------------------------------------------------


def line(world: Any, event: Any) -> None:
    """A line the World logged: journaled when a station is acting and the line is not a
    driver's (which is an input of its own)."""
    if not capturing(world) or event.actor == "driver":
        return
    _entry(
        world,
        _frames(world)[-1].station,  # type: ignore[index]
        "line",
        {
            "severity": event.severity.value,
            "kind": event.kind,
            "text": event.text,
            "actor": event.actor,
            "subject": event.subject,
            "data": encode(dict(event.data or {})),
        },
    )


def order(world: Any, text: str, actor: str, said: str | None, routine: bool) -> Any:
    """An order a station gives, journaled and then given; what it writes is its own."""
    frames = _frames(world)
    assert frames is not None
    _sync(world)  # the stations' state as it stands when the order is given
    _entry(
        world,
        frames[-1].station,
        "order",
        {"order": text, "actor": actor, "said": said, "routine": bool(routine)},
    )
    frames.append(_Frame(frames[-1].station, False))
    try:
        return world.submit(text, actor=actor, said=said, routine=routine)
    finally:
        frames.pop()


def note(world: Any, station: str, entry: Any) -> None:
    """An entry in a station's journal, journaled when a station is acting."""
    if capturing(world):
        _entry(world, station, "note", {"kind": entry.kind, "text": entry.text, "by": entry.by})


# ---------------------------------------------------------------------------
# The entry points of a harness
# ---------------------------------------------------------------------------


def frame(fn: Callable[..., Any]) -> Callable[..., Any]:
    """A harness's entry point: driven by a replay of its acts it does nothing; else what
    it does to the World while it runs is journaled (the module docstring)."""

    @functools.wraps(fn)
    def acting(self: Any, *args: Any, **kwargs: Any) -> Any:
        if self.driven:
            return None
        world = self.world
        frames = _frames(world)
        if frames is None or self.conversation or world.agents.get(self.station.name) is not self:
            return fn(self, *args, **kwargs)
        frames.append(_Frame(self.station.name, True))
        try:
            if self._acts_last is None:
                _seated(world, self)
            return fn(self, *args, **kwargs)
        finally:
            frames.pop()
            if not frames and world.station_acts is not None:
                # at the end of the outermost act (the state is journaled before each
                # order besides, which is all an act in the middle could have read)
                _sync(world)

    return acting


def _seated(world: Any, h: Any) -> None:
    """The station's first act: its definition and its whole state, from which a replay
    builds it. Its acts are whole from here when it had not yet started (a station taken
    in this build); a station that comes from an earlier build's checkpoint has acts
    before this point that are in no list, and its save says so."""
    state = state_of(h)
    h._acts_complete = not h.started
    h._acts_last = state
    _entry(
        world,
        h.station.name,
        "seated",
        {
            "station": h.station.save(),
            "session_kind": h.agent.session_kind,
            "door_note": h.door_note,
            "state": encode(state),
        },
    )


def _held(world: Any) -> list[tuple[str, Any, str]]:
    """What has a state to journal: each recorded station's harness ("state"), and the
    player's seat at a lesser station ("seat_state", package 41), whose state a station's
    act may change (a say heard at the seat, a station's answer to his question)."""
    out = [
        (name, h, "state")
        for name, h in list((getattr(world, "agents", None) or {}).items())
        if getattr(h, "_acts_last", None) is not None
    ]
    seat = getattr(world, "player_seat", None)
    if seat is not None and getattr(world, "station_acts", None) is not None:
        out.append((seat.station.name, seat, "seat_state"))
    return out


def _sync(world: Any) -> None:
    """Each recorded station's state where it changed since it was last journaled."""
    for name, h, kind in _held(world):
        last = getattr(h, "_acts_last", None) or {}
        now = state_of(h)
        changed = {k: v for k, v in now.items() if last.get(k, _MISSING) != v}
        if changed:
            h._acts_last = now
            _entry(world, name, kind, encode(changed))


def saved(world: Any) -> list[dict[str, Any]]:
    """The acts as a save holds them: the list, and each station's state where it changed
    since it was last journaled (a save written in the middle of an act, as a stand-down's
    is, holds the state it saves), without journaling them twice."""
    out = [dict(e) for e in (getattr(world, "station_acts", None) or [])]
    for name, h, kind in _held(world):
        last = getattr(h, "_acts_last", None) or {}
        now = state_of(h)
        changed = {k: v for k, v in now.items() if last.get(k, _MISSING) != v}
        if changed:
            out.append(
                {
                    "tick": world.clock.tick,
                    "after_inputs": len(world.inputs),
                    "station": name,
                    kind: encode(changed),
                }
            )
    return out


_MISSING = object()


def state_of(h: Any) -> dict[str, Any]:
    """A harness's state as journaled: its agent's fields and its own (`HARNESS_FIELDS`),
    the lists and the dictionaries copied."""
    out: dict[str, Any] = {}
    for k, v in vars(h.agent).items():
        if k not in SKIPPED:
            out[f"agent.{k}"] = _copy(v)
    for k in HARNESS_FIELDS:
        if hasattr(h, k):  # the player's seat has some of them only
            out[k] = _copy(getattr(h, k))
    return out


def _copy(v: Any) -> Any:
    if isinstance(v, list):
        return [_copy(x) for x in v]
    if isinstance(v, dict):
        return {k: _copy(x) for k, x in v.items()}
    return v


def apply_state(h: Any, encoded: dict[str, Any]) -> None:
    """A journaled state set on a harness, and the rules-based captain told of it."""
    for k, v in decode(encoded).items():
        if k.startswith("agent."):
            setattr(h.agent, k.removeprefix("agent."), v)
        else:
            setattr(h, k, v)
    sync = getattr(h, "_sync_captain", None)
    if callable(sync):
        sync()


# ---------------------------------------------------------------------------
# A replay's giving
# ---------------------------------------------------------------------------


def give(world: Any, entry: dict[str, Any], build: Callable[[dict[str, Any]], Any]) -> None:
    """One act again, as the replay reaches it. `build` makes a station from its
    `seated` entry (`harness.driven_station`)."""
    station = str(entry.get("station") or "")
    if "seated" in entry:
        h = world.agents.get(station)
        if h is None:
            h = build(entry["seated"])
        apply_state(h, entry["seated"]["state"])
        return
    if "line" in entry:
        d = entry["line"]
        world.record(
            d["severity"],
            d["kind"],
            d["text"],
            actor=d["actor"],
            subject=d.get("subject"),
            data=decode(d.get("data") or {}),
        )
        return
    if "order" in entry:
        d = entry["order"]
        world.submit(d["order"], actor=d["actor"], said=d.get("said"), routine=d.get("routine"))
        return
    if "note" in entry:
        from freesail.agents.journal import Journal

        d = entry["note"]
        world.agent_journals.setdefault(station, Journal(station)).append(
            world, d["text"], kind=d["kind"], by=d.get("by") or ""
        )
        return
    if "state" in entry:
        h = world.agents.get(station)
        if h is not None:
            apply_state(h, entry["state"])
        return
    if "seat_state" in entry:
        seat = getattr(world, "player_seat", None)
        if seat is not None and seat.station.name == station:
            apply_state(seat, entry["seat_state"])
        return
    for kind, applier in APPLIERS.items():
        if kind in entry:
            applier(world, station, entry[kind])
            return


def _working_told(world: Any, station: str, payload: Any) -> None:
    """The master's working told to the station (package 41): the navigation's working
    marked told, as the station's sample marked it in play."""
    nav = getattr(world, "navigation", None)
    w = getattr(nav, "master_working", None) if nav is not None else None
    if isinstance(w, dict):
        w["told"] = True


# Appliers for acts of other kinds (`record`), by kind: `fn(world, station, payload)`.
APPLIERS: dict[str, Callable[[Any, str, Any], None]] = {"working_told": _working_told}


# ---------------------------------------------------------------------------
# The state's encoding: plain JSON, the game's own small classes named
# ---------------------------------------------------------------------------


def encode(v: Any) -> Any:
    if v is None or isinstance(v, (bool, int, float, str)):
        return v
    if isinstance(v, tuple):
        return {"__tuple__": [encode(x) for x in v]}
    if isinstance(v, list):
        return [encode(x) for x in v]
    if isinstance(v, dict):
        return {str(k): encode(x) for k, x in v.items()}
    if dataclasses.is_dataclass(v) and not isinstance(v, type):
        cls = type(v)
        return {
            "__class__": f"{cls.__module__}:{cls.__qualname__}",
            "fields": {f.name: encode(getattr(v, f.name)) for f in dataclasses.fields(v)},
        }
    if hasattr(v, "value") and type(v).__module__.startswith("freesail."):
        return encode(v.value)  # an enum of the game's: its value
    if type(v).__module__ == "numpy" and callable(getattr(v, "item", None)):
        return encode(v.item())  # a number of numpy's, as the log's digest reads it
    return str(v)


def decode(v: Any) -> Any:
    if isinstance(v, list):
        return [decode(x) for x in v]
    if isinstance(v, dict):
        if "__tuple__" in v and len(v) == 1:
            return tuple(decode(x) for x in v["__tuple__"])
        if "__class__" in v and set(v) == {"__class__", "fields"}:
            module, _, name = str(v["__class__"]).partition(":")
            if not module.startswith("freesail."):
                raise ValueError(f"an act names {module}:{name}, which an act may not hold")
            cls: Any = importlib.import_module(module)
            for part in name.split("."):
                cls = getattr(cls, part)
            if not dataclasses.is_dataclass(cls):
                raise ValueError(f"an act names {module}:{name}, which is no record of the game")
            return cls(**{k: decode(x) for k, x in v["fields"].items()})
        return {k: decode(x) for k, x in v.items()}
    return v
