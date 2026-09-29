"""Events and the ship's log.

Every state change a person could notice is an Event. The Log is the primary
output of the simulation: views, replays, narrators and agents all read it.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass, field
from datetime import datetime, timedelta
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


# ---------------------------------------------------------------------------
# The roll-up (spec M4 §20 and open item 8): a view over the store, never a change to it
# ---------------------------------------------------------------------------

# At this compression and above the log rolls up (spec §20: "At sixty and above the log
# rolls up routine entries into hourly summaries"): an hour of the ship's clock passes in
# a minute of the player's, some tens of routine lines a minute, more than a person reads.
ROLLUP_FROM = 60
# The roll-up's period, in seconds of the ship's clock: the hour (spec §20).
ROLLUP_PERIOD_S = 3600

# The actors whose routine lines are never rolled up: the captain's own orders and what the
# driver says (a save, a file read, the compression eased), which the player typed or
# caused and looks for (package 29's judgement: an order vanishing into "orders given twice"
# would read as lost).
KEPT_ACTORS = frozenset({"captain", "driver"})

ROLLUP_KIND = "log.rollup"


def rolls_up(compression: float) -> bool:
    """Whether the log is rolled up at this compression (`ROLLUP_FROM`)."""
    return compression >= ROLLUP_FROM


def kept(e: Event) -> bool:
    """A line the roll-up shows as it is: notable and urgent lines, and the captain's and
    the driver's own."""
    return e.severity is not Severity.ROUTINE or e.actor in KEPT_ACTORS


@dataclass(frozen=True)
class Rollup:
    """An hour's routine lines, summed up in the log's voice. `start` and `end` are the
    hour's bounds on the ship's clock; `first_tick` and `last_tick` the ticks of the first
    and last line summed, so a reader can ask the store for them (`/api/log?since=&until=`);
    `so_far` when the hour was not over (the compression came down, or a reader will not
    see it close)."""

    start: datetime
    end: datetime
    first_tick: int
    last_tick: int
    count: int
    text: str
    counts: dict[str, int] = field(default_factory=dict)
    so_far: bool = False

    kind = ROLLUP_KIND
    severity = Severity.ROUTINE

    @property
    def tick(self) -> int:
        return self.last_tick

    @property
    def stamp(self) -> str:
        """'Forenoon watch (09:00-10:00)': the watch and the hour the lines fell in."""
        _, watch = units.watch_of(self.start)
        until = "on" if self.so_far else self.end.strftime("%H:%M")
        return f"{watch} ({self.start.strftime('%H:%M')}-{until})"

    def line(self) -> str:
        """The console's line: '=' marks a roll-up, as '*' a notable line."""
        return f"= {self.stamp}  {self.text}"

    def to_dict(self) -> dict[str, Any]:
        """For the wire and a model's sample: shaped like an event's, with the hour."""
        return {
            "tick": self.last_tick,
            "ship_time": self.end.isoformat(),
            "severity": Severity.ROUTINE.value,
            "kind": ROLLUP_KIND,
            "text": self.text,
            "actor": "log",
            "subject": None,
            "data": {
                "start": self.start.isoformat(),
                "end": self.end.isoformat(),
                "first_tick": self.first_tick,
                "last_tick": self.last_tick,
                "count": self.count,
                "counts": dict(self.counts),
                "so_far": self.so_far,
            },
            "stamp": self.stamp,
        }


Shown = Event | Rollup


def _hour_of(t: datetime) -> datetime:
    return t.replace(minute=0, second=0, microsecond=0)


class RollupView:
    """The roll-up as it happens: feed it each event with the compression of the moment,
    and it returns what to show now. Below `ROLLUP_FROM`, every event as it is. At and
    above, the lines `kept` pass at once and the rest of each hour is held, shown as one
    `Rollup` when the first line of the next hour arrives (the bell at the hour, which
    every hour has) or when the compression comes down (the hour so far). The console,
    the server (and through it the client) and each agent's samples keep one of these, so
    all of them show the same lines for the same hour (parity: spec M4 §20, open item 8)."""

    def __init__(self) -> None:
        self._held: list[Event] = []
        self._hour: datetime | None = None

    @property
    def holding(self) -> int:
        return len(self._held)

    def feed(self, e: Event, compression: float) -> list[Shown]:
        out: list[Shown] = []
        hour = _hour_of(e.ship_time)
        if self._held and (hour != self._hour or not rolls_up(compression)):
            out.append(self._let_go(so_far=hour == self._hour))
        if rolls_up(compression) and not kept(e):
            if not self._held:
                self._hour = hour
            self._held.append(e)
            return out
        out.append(e)
        return out

    def flush(self) -> list[Shown]:
        """The hour held so far, if any, as a `Rollup` (the compression came down, or the
        view is being closed)."""
        return [self._let_go(so_far=True)] if self._held else []

    def _let_go(self, so_far: bool) -> Rollup:
        r = summarise(self._held, so_far=so_far)
        self._held = []
        self._hour = None
        return r


def rollup(events: Iterable[Event], compression: float, so_far: bool = False) -> list[Shown]:
    """The log as shown at a compression: every event below `ROLLUP_FROM`; at and above,
    the kept lines and an hourly `Rollup` of the rest. The hour still open is summed up
    only with `so_far` (a reader who will not see it close); otherwise it is left for the
    live view that will."""
    view = RollupView()
    out: list[Shown] = []
    for e in events:
        out.extend(view.feed(e, compression))
    if so_far:
        out.extend(view.flush())
    return out


def shown_dict(x: Shown) -> dict[str, Any]:
    """A shown line for the wire, with the stamp people read."""
    if isinstance(x, Rollup):
        return x.to_dict()
    d = x.to_dict()
    d["stamp"] = units.time_stamp(x.ship_time)
    return d


# -- the words of a roll-up: from the events' kinds and counts, never a language model ----

_TIMES = {1: "once", 2: "twice", 3: "three times"}
_GUST = re.compile(r"(\d+) knots")
_STANDING = "standing order "


def _times(n: int) -> str:
    return _TIMES.get(n, f"{n} times")


def _lower_first(text: str) -> str:
    return text[:1].lower() + text[1:] if text else text


def _named(texts: list[str], suffix: str) -> str:
    """'the fore course and the main course filled again' from 'Fore course filled again.'"""
    names: list[str] = []
    for t in texts:
        name = t.rstrip(".").removesuffix(suffix).strip()
        name = name if name.lower().startswith("the ") else "the " + _lower_first(name)
        if name not in names:
            names.append(name)
    if len(names) > 1:
        return ", ".join(names[:-1]) + " and " + names[-1] + " " + suffix
    return f"{names[0]} {suffix}"


def _book_name(e: Event) -> str:
    """The standing order's name from its actor ("standing order 'night routine'")."""
    name = e.actor.removeprefix(_STANDING) if e.actor.startswith(_STANDING) else ""
    if not name and e.text.count("'") >= 2:
        name = e.text.split("'")[1]
    return name.strip("'")


def _phrases(by_kind: dict[str, list[Event]]) -> list[str]:
    """The hour's routine lines in words, each from its kind and its count; what no rule
    names is counted at the end."""
    out: list[str] = []
    take = by_kind.pop
    for kind, verb in (("yard.braced_round", "braced round"), ("yard.braced_up", "braced up")):
        if kind in by_kind:
            out.append(f"{verb} {_times(len(take(kind)))}")
    if "sail.trimmed" in by_kind:
        out.append(f"trimmed sails {_times(len(take('sail.trimmed')))}")
    if "sail.filled" in by_kind:
        out.append(_named([e.text for e in take("sail.filled")], "filled again"))
    if "sail.drawing" in by_kind:
        out.append(_named([e.text for e in take("sail.drawing")], "drawing again"))
    if "line.slacked" in by_kind:
        n = len(take("line.slacked"))
        out.append(f"let go {'a bowline' if n == 1 else f'{n} bowlines'} as the yards came in")
    for kind, words in (("crew.all_hands_up", "all hands up"), ("crew.piped_down", "piped down")):
        if kind in by_kind:
            out.append(f"{words} {_times(len(take(kind)))}")
    for kind, words in (("crew.idlers_up", "idlers up"), ("crew.idlers_down", "idlers below")):
        if kind in by_kind:
            take(kind)
            out.append(words)
    if "watch.relieved" in by_kind:
        last = take("watch.relieved")[-1].text.rstrip(".")
        if last.lower().startswith(("eight bells. ", "four bells. ")):
            last = last.split(". ", 1)[1]
        out.append(_lower_first(last))
    work = [k for k in by_kind if k.startswith("evolution.")]
    if work:
        n = sum(len(take(k)) for k in work)
        out.append(f"the hands at their work ({n} {'step' if n == 1 else 'steps'})")
    for e in take("standing.held", []):
        out.append(f"standing order '{_book_name(e)}' held, its condition not met")
    rejected = take("order.rejected", [])
    by_book = [e for e in rejected if e.actor.startswith(_STANDING)]
    if by_book:
        names: list[str] = []
        for e in by_book:
            name = _book_name(e)
            if name not in names:
                names.append(name)
        said = " and ".join(f"'{n}'" for n in names)
        which = "standing order" if len(names) == 1 else "standing orders"
        out.append(f"{which} {said} found nothing to do {_times(len(by_book))}")
    others = len(rejected) - len(by_book)
    if others:
        out.append(f"{others} {'order' if others == 1 else 'orders'} not carried out")
    if "order.accepted" in by_kind:
        n = len(take("order.accepted"))
        out.append(f"{n} {'order' if n == 1 else 'orders'} given")
    for kind in [k for k in by_kind if k.startswith("agent.")]:
        events = take(kind)
        station = events[0].actor.removeprefix("the ") or "station"
        what = "spoke" if kind == "agent.note" else kind.removeprefix("agent.").replace("_", " ")
        out.append(f"the {station} {what} {_times(len(events))}")
    if "ship.leeway" in by_kind:
        out.append(_lower_first(take("ship.leeway")[-1].text.rstrip(".")))
    if "wind.gust" in by_kind:
        gusts = take("wind.gust")
        speeds = [(int(m.group(1)), e) for e in gusts if (m := _GUST.search(e.text))]
        top = ""
        if speeds:
            knots, strongest = max(speeds, key=lambda x: x[0])
            top = f", the strongest {knots} knots"
            mean = (strongest.data or {}).get("mean_kn")
            if mean is not None:  # the mean wind it blew over (package 29b)
                top += f" on a mean of {mean:.0f}"
        out.append(f"{'a gust' if len(gusts) == 1 else f'{len(gusts)} gusts'}{top}")
    take("clock.bell", None)  # the bells are the hour itself
    rest = sum(len(v) for v in by_kind.values())
    if rest:
        out.append(f"{rest} other {'entry' if rest == 1 else 'entries'}")
    return out


def summarise(events: list[Event], so_far: bool = False) -> Rollup:
    """One hour's routine lines as a `Rollup`, its text in the log's voice: 'Braced round
    twice, the starboard watch relieved the deck, 3 gusts, the strongest 30 knots; 37
    routine entries.'"""
    by_kind: dict[str, list[Event]] = {}
    for e in events:
        by_kind.setdefault(e.kind, []).append(e)
    counts = {k: len(v) for k, v in by_kind.items()}
    phrases = _phrases(dict(by_kind))
    n = len(events)
    body = ", ".join(phrases)
    body = (body[:1].upper() + body[1:] + "; ") if body else ""
    entries = f"{n} routine {'entry' if n == 1 else 'entries'}{' so far' if so_far else ''}"
    start = _hour_of(events[0].ship_time)
    return Rollup(
        start=start,
        end=start + timedelta(seconds=ROLLUP_PERIOD_S),
        first_tick=events[0].tick,
        last_tick=events[-1].tick,
        count=n,
        text=f"{body}{entries}.",
        counts=counts,
        so_far=so_far,
    )
