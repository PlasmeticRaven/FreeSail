"""Events and the ship's log.

Every state change a person could notice is an Event. The Log is the primary
output of the simulation: views, replays, narrators and agents all read it.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, StrEnum
from typing import Any

from freesail import units


class Severity(StrEnum):
    ROUTINE = "routine"
    NOTABLE = "notable"
    URGENT = "urgent"

    @property
    def rank(self) -> int:
        return {"routine": 0, "notable": 1, "urgent": 2}[self.value]


@dataclass(frozen=True)
class Event:
    tick: int
    ship_time: datetime
    severity: Severity
    kind: str
    text: str
    actor: str = "sim"
    subject: str | None = None
    data: dict[str, Any] = field(default_factory=dict)

    def line(self) -> str:
        """The log line as a person reads it."""
        stamp = units.time_stamp(self.ship_time)
        mark = {"routine": " ", "notable": "*", "urgent": "!"}[self.severity.value]
        return f"{mark} {stamp}  {self.text}"

    def to_dict(self) -> dict[str, Any]:
        return {
            "tick": self.tick,
            "ship_time": self.ship_time.isoformat(),
            "severity": self.severity.value,
            "kind": self.kind,
            "text": self.text,
            "actor": self.actor,
            "subject": self.subject,
            "data": self.data,
        }


Subscriber = Callable[[Event], None]


class Log:
    """An append-only list of events with subscribers and a digest."""

    def __init__(self) -> None:
        self._events: list[Event] = []
        self._subscribers: list[Subscriber] = []

    def append(self, event: Event) -> Event:
        self._events.append(event)
        for fn in self._subscribers:
            fn(event)
        return event

    def subscribe(self, fn: Subscriber) -> None:
        self._subscribers.append(fn)

    def unsubscribe(self, fn: Subscriber) -> None:
        self._subscribers.remove(fn)

    def __len__(self) -> int:
        return len(self._events)

    def __iter__(self) -> Iterator[Event]:
        return iter(self._events)

    def __getitem__(self, i: int) -> Event:
        return self._events[i]

    def all(self) -> list[Event]:
        return list(self._events)

    def since(self, tick: int) -> list[Event]:
        """Events with tick strictly greater than `tick`."""
        return [e for e in self._events if e.tick > tick]

    def tail(self, n: int) -> list[Event]:
        return self._events[-n:]

    def of_kind(self, kind: str) -> list[Event]:
        return [e for e in self._events if e.kind == kind]

    def at_least(self, severity: Severity) -> list[Event]:
        return [e for e in self._events if e.severity.rank >= severity.rank]

    def digest(self) -> str:
        """SHA-256 over the canonical serialisation of every event.

        Two worlds that produce the same digest produced the same log. This is
        the determinism and replay contract.
        """
        h = hashlib.sha256()
        for e in self._events:
            h.update(json.dumps(e.to_dict(), sort_keys=True, default=_json_default).encode())
            h.update(b"\n")
        return h.hexdigest()


def _json_default(o: Any) -> Any:
    if isinstance(o, datetime):
        return o.isoformat()
    if isinstance(o, Enum):
        return o.value
    if isinstance(o, float):
        return repr(o)
    raise TypeError(f"cannot serialise {type(o).__name__}")
