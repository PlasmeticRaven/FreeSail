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
    "CHANGE_OPS",
    "EVENT_SETTLE_S",
    "GLASS_TURN_IN",
    "RANKS",
    "STANDING_DWELL_S",
    "Clause",
    "Comparison",
    "Condition",
    "EventCondition",
    "Rule",
    "Trigger",
    "event_condition",
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
    "mate",  # the schooner's and the cutter's, who keeps the watch under the master (package 37)
    "master's mate",
    "midshipman",
)


# The glass is turning when the last hour's change goes against the three hours' by this
# much, each way at least (package 31c, "the glass turning"). The glass reads to the
# hundredth and pumps a hundredth or two in a seaway (W §3; `world.weather.GLASS_PUMP_MAX_IN`),
# so a turn is three hundredths in the hour against three or more in the three hours the
# other way, the same three hundredths that divide steady from rising or falling there
# (`TENDENCY_STEADY_IN_PER_3H`). Judgement, checked on the day under systems at seed 7,
# watched a minute at a time: it turns at 01:53 on the second day, fifty minutes after the
# low's bottom at 29.66, where the watcher of playtest 11 saw "the glass began to rise",
# and once (`EVENT_SETTLE_S`); not once in the steady forenoon, where the hour's change
# wanders a hundredth or two either way, nor at 08:30 the next morning, where the pumping
# of a very heavy sea dips it two hundredths.
GLASS_TURN_IN = 0.03


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

    op: str  # gt | lt | backs | veers | shifts | from | forward_of | abaft | side | point |
    #          east_of | west_of | is | is_not | straining
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


def _sea_is(reading: dict[str, Any], word: str) -> bool:
    """The sea's state word (spec M5 §4; `world.sea.SeaReading`): 'heavy' holds for a
    very heavy sea too, 'confused' is the swell across the wind."""
    if word == "confused":
        return bool(reading["confused"])
    if word == "heavy":
        return reading["state"] in ("heavy", "very heavy")
    return reading["state"] == word


def _glass_turning(tendency: dict[str, Any]) -> bool:
    """The last hour's change against the three hours', each at least `GLASS_TURN_IN`:
    the rise after a fall, or the fall after a rise."""
    one, three = tendency.get("one_hour_in"), tendency.get("three_hours_in")
    if one is None or three is None:
        return False
    # to the hundredth, as the glass reads: the record's differences carry float noise
    one, three = round(one, 2), round(three, 2)
    return one * three < 0 and abs(one) >= GLASS_TURN_IN and abs(three) >= GLASS_TURN_IN


def _sea_rank(reading: dict[str, Any]) -> int:
    """The sea's state word as a rank, smooth lowest (`readings.SEA_STATE_WORDS`)."""
    from freesail.world.sea import SEA_STATE_WORDS

    state = reading.get("state")
    return SEA_STATE_WORDS.index(state) if state in SEA_STATE_WORDS else -1


def _motion_is(reading: dict[str, Any], word: str) -> bool:
    """The motion's state word (`physics.motion.MotionReading`): 'rolling' holds for
    rolling heavily too; 'rolling heavily' and 'pitching heavily' want the heavy word;
    'heavy' is any heavy motion; 'labouring' is both together."""
    state, heavy = reading["state"], bool(reading["heavy"])
    if word == "heavy":
        return heavy
    if word.endswith(" heavily"):
        return state == word[: -len(" heavily")] and heavy
    if word == "labouring":
        return state == "labouring"
    return state == word


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
            if op == "shifts":  # either way: (points veered, points backed)
                veer, back = v
                return shift >= units.points_to_rad(veer) or -shift >= units.points_to_rad(back)
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
        if kind in ("daylight", "gust", "weather"):
            return (value == v) if op == "is" else (value != v)
        if kind == "tendency" and v == "turning":
            turning = _glass_turning(value)
            return turning if op == "is" else not turning
        if kind in ("tendency", "sky", "visibility"):
            return (value["words"] == v) if op == "is" else (value["words"] != v)
        if kind == "sea" and op == "gets_up":
            # measured from the sea when the rule was armed, as a wind's shift is, and
            # afresh after each firing (`spend_shift`)
            key = f"{self.text}:reference"
            if key not in memory:
                memory[key] = _sea_rank(value)
                return False
            return _sea_rank(value) > memory[key]
        if kind in ("sea", "motion"):
            holds = _sea_is(value, v) if kind == "sea" else _motion_is(value, v)
            return holds if op == "is" else not holds
        if kind == "glass":
            return value > v if op == "gt" else value < v
        if kind == "sight":  # the land (package 32): the lookout's word, in sight or not
            if isinstance(value, dict) and "in_sight" in value:
                # a sail in sight, the strangers (packages 35 and 36): the row's own flag,
                # since its words carry the nearest sail after "in sight"
                seen = bool(value["in_sight"])
            else:
                words = value["words"] if isinstance(value, dict) else str(value)
                seen = words == "in sight"
            holds = seen if v == "in sight" else not seen
            return holds if op == "is" else not holds
        if kind == "depth":  # the depth of water by the chart, or the lead's, in fathoms
            fm = units.m_to_fathoms(value)
            return fm > v if op == "gt" else fm < v
        # the reckoning's readings (package 33a): by account, never the truth
        if kind == "distance":
            nm = units.m_to_nm(value["metres"])
            return nm > v if op == "gt" else nm < v
        if kind == "position":
            if op in ("north_of", "south_of"):
                lat = value.get("lat_deg")
                if lat is None:
                    return False
                return lat > v if op == "north_of" else lat < v
            lon = value.get("lon_deg")
            if lon is None:
                return False
            return lon > v if op == "east_of" else lon < v
        if kind == "ground":
            holds = v in str(value["words"])
            return holds if op == "is" else not holds
        if kind == "person":
            holds = value["place"] == v
            return holds if op == "is" else not holds
        if kind == "manoeuvre":
            # package 33c: 'she is hove to' holds from the moment the heave-to begins
            # until she fills away, so a trim rule sleeps through the manoeuvre too
            holds = value in ("hove to", "heaving to") if v == "hove to" else value == v
            return holds if op == "is" else not holds
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

    def spend_shift(self, view: R.ReadingsView, memory: dict[str, Any]) -> None:
        """A wind's shift that fired the rule is spent: the next is measured from the
        direction now (package 29b, "trim on a shift": a wind veering steadily through a
        night is trimmed to point by point)."""
        if self.comparison.op in CHANGE_OPS:
            value = self._values(view)[0]
            if value is not None:
                ref = _sea_rank(value) if self.comparison.op == "gets_up" else value
                memory[f"{self.text}:reference"] = ref

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
        if reading.kind == "direction" and self.comparison.op in ("backs", "veers", "shifts"):
            done = self.comparison.text
            for now, then in (("backs", "backed"), ("veers", "veered"), ("shifts", "shifted")):
                done = done.replace(now, then)
            return f"{self.phrase} {verb} {said}, and has not {done}"
        if self.comparison.op == "gets_up":
            return f"{self.phrase} {verb} {said}, and has not got up"
        if self.comparison.op == "is_not" or (
            self.comparison.op == "is" and self.comparison.text in said
        ):
            # "she is hove to", not "she is hove to, not not hove to"; "the land is not in
            # sight", not "the land is not in sight, not in sight" (package 33c)
            return f"{self.phrase} {verb} {said}"
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


@dataclass
class EventCondition(Condition):
    """An event that is a reading's change (`readings.EventSpec.watch`, package 31c): its
    condition coming to hold, each time it does. `holds` is true on the tick it comes to
    hold, not while it goes on holding, and false at the first look, which sets what a
    change is measured from (the glass already falling fast is not the glass coming to
    fall fast). At each coming to hold a change the condition measures (the wind's shift,
    the sea getting up) is measured afresh from there, so a steady veer is an event at
    each point. A standing order's `at` evaluates it as its `when` condition (`Trigger`),
    a stand-by once a tick (`agents.harness`); each keeps its own memory."""

    def holds(self, view: R.ReadingsView, memory: dict[str, Any] | None = None) -> bool:
        memory = memory if memory is not None else {}
        # every clause is read, so that each sets its reference at the first look
        now = all([c.holds(view, memory) for c in self.clauses])
        key, quiet = f"{self.text}:held", f"{self.text}:false since"
        was = memory.get(key)
        memory[key] = now
        if not now:
            if was is not False:
                # false from here; false at the first look is false long enough
                memory[quiet] = view.tick if was else None
            return False
        if was is not False:
            return False  # the first look, or holding still
        since = memory.get(quiet)
        change = any(c.comparison.op in CHANGE_OPS for c in self.clauses)
        if not change and since is not None and view.tick - since < EVENT_SETTLE_S:
            return False  # the same event come again inside the settle
        for c in self.clauses:
            c.spend_shift(view, memory)
        return True


# The comparisons that measure a change from a reference, spent when they fire.
CHANGE_OPS: tuple[str, ...] = ("backs", "veers", "shifts", "gets_up")

# An event that is a state coming to hold (the glass falling fast, the glass turning) comes
# again only once its condition has been false this long (package 31c). The glass's words
# hover about their thresholds: on the day under systems at seed 7 the tendency sat about
# a tenth in three hours from 21:00 to 21:52, "falling fast" coming and going eight times,
# and the hour's change about three hundredths for an hour after the low; a fall that
# eases for a few minutes and comes again inside the hour is the same fall. An hour, the
# glass's own span (the tendency is read by the hour and the three hours; judgement). A
# change measured from a reference (the wind's shift, the sea getting up) has none, since
# it is measured afresh from each: each point of a steady veer is an event.
EVENT_SETTLE_S = 3600

# The events' conditions, parsed once (their clauses keep no state; the memory is the
# caller's).
_EVENT_CONDITIONS: dict[str, Condition] = {}


def event_condition(words: str) -> EventCondition | None:
    """The condition of an event that is a reading's change, by the event's words; None
    for an event the log says (a bell, a squall) or no event at all."""
    spec = R.EVENTS.get(words)
    if spec is None or spec.watch is None:
        return None
    base = _EVENT_CONDITIONS.get(words)
    if base is None:
        from freesail.standing.grammar import parse_condition

        base = _EVENT_CONDITIONS[words] = parse_condition(spec.watch)
    return EventCondition(list(base.clauses), base.text)


# ---------------------------------------------------------------------------
# Triggers and rules
# ---------------------------------------------------------------------------


@dataclass
class Trigger:
    """`when <condition> [for <duration>]`, `at <event>` or `every <interval>`.

    `at` an event that is a reading's change ("at the glass falling fast", package 31c) is
    kept as a `when` of the event's condition (`event_condition`): the runtime evaluates it
    with the `when` orders, edge and dwell alike, and the book says it as it was given."""

    kind: str  # "when" | "at" | "every"
    text: str
    condition: Condition | None = None
    duration_s: int = 0
    event: str | None = None  # the event's words, a key of readings.EVENTS
    interval_s: int = 0

    def __post_init__(self) -> None:
        if self.kind == "at" and self.event is not None:
            watched = event_condition(self.event)
            if watched is not None:
                self.kind = "when"
                self.condition = watched


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
    # -- package 33c -----------------------------------------------------------------------
    # held until the world has a reading one of its orders is on: the registry's absent
    # sentence ("The ship has no well to sound yet; ..."); never fired while it is set
    held: str | None = None
    # the ship's watch of the last "not carried out" line of a failing `if`, so that the
    # line is said the first time and then once a watch (spec M5 open item 15)
    held_line_watch: tuple[str, str] | None = None

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
        if self.held is not None and not self.belayed:
            return f"held: {self.held[:1].lower()}{self.held[1:].rstrip('.')}"
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
        """Forget the duration, the dwell and the clause references: a rule given or
        resumed measures 'backs two points' from the wind it sees now."""
        self.held_s = 0.0
        self.clear_s = 0.0
        self.memory.clear()
        self.held_line_watch = None

    def spend_shifts(self, view: R.ReadingsView) -> None:
        """At a firing: every wind's shift the trigger waits for is measured afresh from
        the direction now (`Clause.spend_shift`)."""
        cond = self.trigger.condition
        for clause in cond.clauses if cond is not None else ():
            clause.spend_shift(view, self.memory)
