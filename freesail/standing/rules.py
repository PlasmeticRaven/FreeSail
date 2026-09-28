"""The rule objects of the standing dialect (spec M4 §3 and §4).

A `Rule` is what the dialect parses to and what the Python API (package 26) builds: a
trigger (`when` a condition, with a duration; `at` an event; `every` an interval), an
optional `if` condition checked at the moment of firing, the orders to give, who gave it,
and the state the runtime keeps (standing or belayed, fired how often, the duration and
dwell accumulators). There is one engine: the runtime evaluates every Rule the same way
whoever built it.

Conditions are conjunctions of clauses; a clause is a reading of the registry
(`freesail.api.readings`) and a comparison of the kind that reading admits. A clause is
evaluated against a `ReadingsView` (the physics' own numbers) and a small `memory` the
rule owns, which is where "backs two points" keeps the direction it measures from.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from freesail import units
from freesail.api import readings as R

__all__ = [
    "RANKS",
    "STANDING_DWELL_S",
    "Clause",
    "Comparison",
    "Condition",
    "Rule",
    "Trigger",
    "officer_words",
    "rank_of",
]

# Having fired, a `when` order does not fire again until its condition has been false for
# this long and any evolution it started has ended (spec M4 §3, the second guard against
# thrashing). Five minutes of ship's time: judgement in the spec.
STANDING_DWELL_S = 300

# Who may give a standing order, most senior first (spec M4 §3: the captain by default;
# `by the master` for an officer's). Rank orders precedence when two orders conflict. The
# list is the frigate's quarterdeck as Luce's station bill has it (Luce 1884, ch. XX).
RANKS: tuple[str, ...] = (
    "captain",
    "first lieutenant",
    "lieutenant",
    "master",
    "master's mate",
    "midshipman",
)


def rank_of(officer: str) -> int:
    """0 for the captain, higher for each rank below. Raises ValueError for a stranger."""
    key = " ".join(officer.lower().replace("the ", "", 1).split())
    if key.startswith("the "):
        key = key[4:]
    if key not in RANKS:
        raise ValueError(officer)
    return RANKS.index(key)


def officer_words(officer: str) -> str:
    """'the captain', 'the master', for a sentence."""
    return f"the {officer}"


# ---------------------------------------------------------------------------
# Comparisons and clauses
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Comparison:
    """How a reading is compared: an operation, its value in the reading's nautical unit
    (or a word, or radians for a compass point), and the words as said."""

    op: str  # gt | lt | backs | veers | from | forward_of | abaft | side | point | east_of |
    #          west_of | is | is_not | straining
    value: Any
    text: str


def _sail_is(reading: dict[str, Any], word: str) -> bool:
    state = reading["state"]
    if word == "set":
        return state == "set"
    if word == "drawing":
        return state in ("set", "goose_winged") and not reading["shaking"] and not reading["aback"]
    if word == "shaking":
        return bool(reading["shaking"])
    if word == "aback":
        return bool(reading["aback"])
    if word == "reefed":
        return state == "set" and reading["reefs"] > 0
    return state == word.replace(" ", "_")


@dataclass
class Clause:
    """One reading compared once: 'the true wind exceeds 30 knots'."""

    reading: str  # registry id
    comparison: Comparison
    text: str  # the clause as said, normalised
    params: tuple[str, ...] = ()  # part ids for a parametric reading ("the royals": three)
    phrase: str = ""  # the reading's words as said, for the log

    def _values(self, view: R.ReadingsView) -> list[Any]:
        if self.params:
            return [view.value(self.reading, p) for p in self.params]
        return [view.value(self.reading)]

    def _one(self, value: Any, memory: dict[str, Any]) -> bool:
        if value is None:
            return False
        op, v = self.comparison.op, self.comparison.value
        kind = R.REGISTRY.get(self.reading).kind
        if kind == "speed":
            kn = units.ms_to_knots(value)
            return kn > v if op == "gt" else kn < v
        if kind == "angle":
            deg = units.rad_to_deg(abs(value))
            return deg > v if op == "gt" else deg < v
        if kind == "direction":
            if op == "from":
                return abs(units.wrap_pi(value - v)) <= units.POINT
            key = f"{self.text}:reference"
            if key not in memory:
                memory[key] = value  # measured from the direction when the rule was armed
                return False
            shift = units.wrap_pi(value - memory[key])
            wanted = units.points_to_rad(v)
            return shift >= wanted if op == "veers" else -shift >= wanted
        if kind == "angle_on_bow":
            deg = units.rad_to_deg(abs(value))
            if op == "forward_of":
                return deg < v
            if op == "abaft":
                return deg > v
            if op == "side":
                return R.apparent_side(value) == v
            kn = units.ms_to_knots(value)
            return kn > v if op == "gt" else kn < v
        if kind == "compass":
            if op == "point":
                return units.nearest_point_index(value) == units.nearest_point_index(v)
            diff = units.wrap_pi(value - v)
            return 0 < diff < units.TWO_PI / 2 if op == "east_of" else diff < 0
        if kind == "watch":
            return (value == v) if op == "is" else (value != v)
        if kind == "bells":
            return (value["bells"] == v) if op == "is" else (value["bells"] != v)
        if kind == "daylight":
            return (value == v) if op == "is" else (value != v)
        if kind == "sail":
            return _sail_is(value, v) if op == "is" else not _sail_is(value, v)
        if kind == "strain":
            if op == "straining":
                return value > R.STRAINING_RATIO
            return value > v if op == "gt" else value < v
        if kind == "hands":
            if op in ("gt", "lt"):
                return value["count"] > v if op == "gt" else value["count"] < v
            return (value["words"] == v) if op == "is" else (value["words"] != v)
        return False

    def holds(self, view: R.ReadingsView, memory: dict[str, Any] | None = None) -> bool:
        memory = memory if memory is not None else {}
        values = self._values(view)
        if not values:
            return False
        if self.comparison.op == "is_not":
            return all(self._one(v, memory) for v in values)  # none of them is
        if self.params and len(values) > 1:
            return all(self._one(v, memory) for v in values)  # "the royals are set": all
        return self._one(values[0], memory)

    def describe(self, view: R.ReadingsView) -> str:
        """'the true wind is 24 knots, not under 20 knots', for the log when it fails."""
        reading = R.REGISTRY.get(self.reading)
        values = self._values(view)
        if len(values) == 1:
            # the reading's own words for a value it withholds on purpose (the course and
            # the leeway with no way on, package 28c)
            said = view.words(self.reading, self.params[0] if self.params else None)
        else:
            said = ", ".join(R.describe_value(reading, v) for v in values)
        verb = "are" if len(values) > 1 or reading.kind == "hands" else "is"
        if reading.kind == "direction" and self.comparison.op in ("backs", "veers"):
            return f"{self.phrase} {verb} {said}, and has not {self.comparison.text}"
        return f"{self.phrase} {verb} {said}, not {self.comparison.text}"


@dataclass
class Condition:
    """A conjunction of clauses (spec §3: conjunctions only)."""

    clauses: list[Clause]
    text: str

    def holds(self, view: R.ReadingsView, memory: dict[str, Any] | None = None) -> bool:
        memory = memory if memory is not None else {}
        return all(c.holds(view, memory) for c in self.clauses)

    def failing(self, view: R.ReadingsView, memory: dict[str, Any] | None = None) -> Clause | None:
        memory = memory if memory is not None else {}
        for c in self.clauses:
            if not c.holds(view, memory):
                return c
        return None

    def explain(self, view: R.ReadingsView, memory: dict[str, Any] | None = None) -> str:
        c = self.failing(view, memory)
        return c.describe(view) if c is not None else "the condition holds"

    def readings(self) -> list[str]:
        return list(dict.fromkeys(c.reading for c in self.clauses))


# ---------------------------------------------------------------------------
# Triggers and rules
# ---------------------------------------------------------------------------


@dataclass
class Trigger:
    """`when <condition> [for <duration>]`, `at <event>` or `every <interval>`."""

    kind: str  # "when" | "at" | "every"
    text: str
    condition: Condition | None = None
    duration_s: int = 0
    event: str | None = None  # the event's words, a key of readings.EVENTS
    interval_s: int = 0


@dataclass
class Rule:
    """A standing order: what it waits for, what it does, who gave it, and its state."""

    name: str
    trigger: Trigger
    actions: list[str]
    condition: Condition | None = None  # the ", if" clause, tested at firing
    given_by: str = "captain"
    text: str = ""  # the sentence as given
    source: str = "dialect"  # "dialect", or "python" for package 26's rules
    trusted: bool = False  # a Python rule running in-process (spec §4)
    # -- state kept by the runtime, saved with the book ---------------------------------
    belayed: bool = False
    fired: int = 0
    last_fired_tick: int | None = None
    given_tick: int = 0
    # -- state kept by the runtime, rebuilt by replay --------------------------------------
    armed: bool = True  # a `when` order that may fire (edge-triggered)
    held_s: float = 0.0  # how long the `when` condition has held (the duration)
    clear_s: float = 0.0  # how long it has been false since the last firing (the dwell)
    next_due_tick: int | None = None  # an `every` order's next firing
    memory: dict[str, Any] = field(default_factory=dict)  # clause references
    started: list[Any] = field(default_factory=list)  # runner instances the last firing began
    conflicts: int = 0  # times countermanded

    def __post_init__(self) -> None:
        rank_of(self.given_by)  # a stranger is refused at once
        self.given_by = " ".join(self.given_by.lower().replace("the ", "", 1).split())
        if not self.actions:
            raise ValueError(f"standing order '{self.name}' gives no orders")

    @property
    def rank(self) -> int:
        return rank_of(self.given_by)

    @property
    def officer(self) -> str:
        return officer_words(self.given_by)

    @property
    def key(self) -> str:
        return " ".join(self.name.lower().split())

    def state_words(self, clock: Any = None) -> str:
        """'standing; fired twice, last at Forenoon watch (09:30)' for the book."""
        head = "belayed" if self.belayed else "standing"
        if self.fired == 0:
            return f"{head}; never fired"
        times = {1: "once", 2: "twice"}.get(self.fired, f"{self.fired} times")
        last = ""
        if self.last_fired_tick is not None and clock is not None:
            from datetime import timedelta

            when = clock.start + timedelta(seconds=self.last_fired_tick)
            last = f", last at {units.time_stamp(when)}"
        return f"{head}; fired {times}{last}"

    def body_words(self) -> str:
        """'at sunset then take in the studdingsails; take in the royals'."""
        head = self.trigger.text
        if self.condition is not None:
            head += f", if {self.condition.text}"
        return f"{head} then " + "; ".join(self.actions)

    def save(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "text": self.text,
            "given_by": self.given_by,
            "source": self.source,
            "belayed": self.belayed,
            "fired": self.fired,
            "last_fired_tick": self.last_fired_tick,
            "given_tick": self.given_tick,
        }

    def reset_edge(self) -> None:
        """Forget the duration, the dwell and the clause references: a rule re-armed
        measures 'backs two points' from the wind it sees now."""
        self.held_s = 0.0
        self.clear_s = 0.0
        self.memory.clear()
