"""The readings registry (spec M4 §2): what a rule may test, an instrument may show and
an agent may ask for, through one door.

Parity is structural: a standing order's condition, the client's snapshot and (package
27) an agent's `readings()` tool all read a `ReadingsView` from `World.readings`, and
that view reads the rows registered here. Nothing the three consumers see comes from
anywhere else, so a reading added here is at once a word the grammar knows, a number
the snapshot carries and a fact an agent can ask for.

A `Reading` has an id, the words the grammar accepts for it ("the true wind"), the
nautical unit the grammar speaks in, a getter over the World that returns the SI value
the physics keeps (metres a second, radians), and a comparison kind that says which
comparisons make sense of it (`KINDS` below). Some rows are *parametric*: `the <sail>`
is one row read with a sail's id, `the strain` one row read with no part (the worst
ratio aboard) or with a part's id. The readings the world does not have yet (the well,
the glass, the depth, a sail in sight) are registered as *absent* with the sentence the
parser says, so the grammar can name them and refuse them in words.

The value of a row is the physics' own number at the moment it is read: nothing here is
computed a second way. `World.readings` caches a view per tick (and per order, since an
order can change a line's state at once), so a rule that reads twenty readings a tick
costs twenty attribute reads.

Events (`EVENTS`, for `at`) name a log kind and, where it matters, a test on the event's
data; intervals (`INTERVALS`, for `every`) are seconds of ship's time.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from freesail import units
from freesail.crew import bill
from freesail.crew.model import Crew, fatigue_words
from freesail.physics.strain import DECAY_RATIO
from freesail.ship.parts import Dynamics, HelmMode, Line, Sail, SailState, Spar

if TYPE_CHECKING:
    from freesail.core.world import World

__all__ = [
    "EVENTS",
    "FATIGUE_DECIMALS",
    "INTERVALS",
    "KINDS",
    "REGISTRY",
    "Reading",
    "ReadingsView",
    "Registry",
    "SAIL_STATE_WORDS",
    "STRAINING_RATIO",
    "WATCH_NAMES",
    "event_matches",
    "sail_reading",
]

# Fatigue means are given to three places: finer than the eye can use, coarse enough that a
# snapshot does not change every tick for a hand standing idle (package 20's judgement; the
# snapshot's `crew` block and the `hands on deck` reading share it).
FATIGUE_DECIMALS = 3

# A part "is straining" above the ratio at which the strain model wears it and warns the
# log: strain.py's DECAY_RATIO (spec M2 §5.3), named here so that the two stay one.
STRAINING_RATIO = DECAY_RATIO

# The comparison kinds and the comparisons each admits. The standing grammar refuses a
# comparison its reading's kind does not list, naming the word ("'the true wind' cannot be
# 'shaking'; a wind is compared in knots or points.").
KINDS: dict[str, str] = {
    "speed": "a speed in knots: exceeds, is over, is under, is below",
    "direction": "a direction: backs or veers N points, is from a compass point",
    "angle_on_bow": "an angle on the bow: is forward of or abaft N degrees or the beam",
    "compass": "a compass heading: is a point, is east of or west of a point",
    "angle": "an angle in degrees: exceeds, is over, is under, is below",
    "watch": "a watch: is the middle watch, is not the first watch",
    "bells": "the bells: is eight bells",
    "daylight": "day, twilight or night: is night, is not day",
    "sail": "a sail's state: is set, is shaking, is aback, is furled, is blown out",
    "strain": "the strain: exceeds the rating, exceeds 1.2, is straining",
    "hands": "the hands: exceeds N, are fresh, are tired, are worn out",
    "absent": "not a reading the ship has yet",
}

# The words a sail's state is compared with (spec §2: is shaking, is aback, is set, is
# furled, is blown out), and the part states behind them. "drawing" is set and neither
# shaking nor aback; "reefed" is set with a reef in.
SAIL_STATE_WORDS: tuple[str, ...] = (
    "set",
    "drawing",
    "shaking",
    "aback",
    "furled",
    "blown out",
    "in the gear",
    "loosed",
    "sheeted",
    "unbent",
    "goose winged",
    "reefed",
    "wrecked",
)

WATCH_NAMES: tuple[str, ...] = tuple(name.lower() for _, _, name in units.WATCHES)

DAYLIGHT_WORDS: tuple[str, ...] = ("day", "twilight", "night")

FATIGUE_WORDS: tuple[str, ...] = ("fresh", "tired", "worn out")


# ---------------------------------------------------------------------------
# Rows
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Reading:
    """One row of the registry. `getter(world, param)` returns the SI value, or raises
    nothing: a reading the world cannot give returns None and the grammar's comparison
    reads false. `absent` is the sentence the parser says for a reading the ship has not
    got yet; such a row has no getter."""

    id: str
    words: tuple[str, ...]
    kind: str
    unit: str  # the nautical unit the grammar speaks in: "knots", "degrees", "points", ""
    getter: Callable[[Any, str | None], Any] | None = None
    parametric: str | None = None  # "sail" or "part": the row is read with a part's id
    absent: str | None = None
    description: str = ""

    @property
    def is_absent(self) -> bool:
        return self.absent is not None


class Registry:
    """The rows in registration order, looked up by id or by their words."""

    def __init__(self) -> None:
        self._rows: dict[str, Reading] = {}

    def add(self, reading: Reading) -> Reading:
        """Register a row. A row registered again under the same id replaces the first,
        which is how package 26 turns `daylight` from absent into a reading: the words
        stay, the getter arrives."""
        if reading.kind not in KINDS:
            raise ValueError(f"reading '{reading.id}': kind '{reading.kind}' is not one of KINDS")
        if reading.absent is None and reading.getter is None:
            raise ValueError(f"reading '{reading.id}' has neither a getter nor an absent sentence")
        self._rows[reading.id] = reading
        return reading

    def add_absent(self, id: str, words: tuple[str, ...], sentence: str) -> Reading:
        return self.add(Reading(id=id, words=words, kind="absent", unit="", absent=sentence))

    def get(self, id: str) -> Reading:
        return self._rows[id]

    def __contains__(self, id: str) -> bool:
        return id in self._rows

    def __iter__(self):
        return iter(self._rows.values())

    def ids(self) -> list[str]:
        return list(self._rows)

    def words(self) -> list[str]:
        """Every phrase the grammar accepts, longest first (the parser matches longest)."""
        out: list[str] = []
        for r in self._rows.values():
            for w in r.words:
                if w not in out:
                    out.append(w)
        return sorted(out, key=lambda w: (-len(w.split()), -len(w), w))

    def by_words(self, phrase: str) -> list[Reading]:
        """The rows behind a phrase, in registration order ("the true wind" is two: its
        speed and its direction; the grammar picks the one the comparison suits)."""
        return [r for r in self._rows.values() if phrase in r.words]

    def at(self, world: World) -> ReadingsView:
        return ReadingsView(self, world)


class ReadingsView:
    """The readings of one World at one moment, read lazily and remembered.

    `view["speed"]` or `view.value("speed")` is the SI value; `view.value("sail",
    "fore.royal")` a parametric row's. `view.as_dict()` gives every non-parametric
    reading (for an agent's `readings()` tool and for tests). The World hands out one view
    per tick and per order (`World.readings`), so every rule of a tick reads the same
    numbers. A rule's Python body (package 26) is handed this object and nothing else of
    the World.
    """

    def __init__(self, registry: Registry, world: World):
        self._registry = registry
        self._world = world
        self._cache: dict[tuple[str, str | None], Any] = {}

    @property
    def tick(self) -> int:
        return self._world.clock.tick

    def reading(self, id: str) -> Reading:
        return self._registry.get(id)

    def value(self, id: str, param: str | None = None) -> Any:
        key = (id, param)
        if key not in self._cache:
            row = self._registry.get(id)
            if row.getter is None:
                self._cache[key] = None
            else:
                self._cache[key] = row.getter(self._world, param)
        return self._cache[key]

    def __getitem__(self, id: str) -> Any:
        return self.value(id)

    def get(self, id: str, default: Any = None) -> Any:
        if id not in self._registry:
            return default
        v = self.value(id)
        return default if v is None else v

    def as_dict(self) -> dict[str, Any]:
        """Every non-parametric reading's value, by id, in registration order."""
        return {r.id: self.value(r.id) for r in self._registry if r.parametric is None}


# ---------------------------------------------------------------------------
# Getters over the World. Each reads the physics' own number and nothing else.
# ---------------------------------------------------------------------------


def _dyn(world: Any) -> Dynamics | None:
    return getattr(world.ship, "dyn", None)


def _true_wind_speed(world: Any, _: str | None) -> float:
    return world.wind.effective_speed  # m/s at the reference height, gust included


def _true_wind_from(world: Any, _: str | None) -> float:
    return world.wind.direction_from  # radians, where it comes from


def _apparent_wind_angle(world: Any, _: str | None) -> float:
    d = _dyn(world)
    return d.apparent_wind_angle if d is not None else 0.0  # signed radians, + starboard


def _apparent_wind_speed(world: Any, _: str | None) -> float:
    d = _dyn(world)
    return d.apparent_wind_speed if d is not None else world.wind.effective_speed


def _heading(world: Any, _: str | None) -> float:
    return world.ship.heading


def _course(world: Any, _: str | None) -> float:
    """The course ordered: the helm's target when steering a heading, else the heading
    she has (full and by, or a rudder order, has no course but the one she makes)."""
    d = _dyn(world)
    if d is None:
        return getattr(world.ship, "target_heading", world.ship.heading)
    return d.target_heading if d.helm_mode is HelmMode.HEADING else d.heading


def _speed(world: Any, _: str | None) -> float:
    d = _dyn(world)
    return d.speed if d is not None else world.ship.speed


def _leeway(world: Any, _: str | None) -> float:
    d = _dyn(world)
    return d.leeway if d is not None else 0.0


def _heel(world: Any, _: str | None) -> float:
    d = _dyn(world)
    return d.heel if d is not None else 0.0


def _helm(world: Any, _: str | None) -> float:
    d = _dyn(world)
    return d.rudder if d is not None else 0.0


def _watch(world: Any, _: str | None) -> str:
    return world.clock.watch().lower()


def _daylight(world: Any, _: str | None) -> str | None:
    """'day', 'twilight' or 'night' from the sun model (`freesail.core.sun`, spec §5),
    read through the World so that the standing orders, the snapshot and the agents see
    one sun; a world without one (a bare stub) reads None."""
    return getattr(world, "daylight", None)


def _bells(world: Any, _: str | None) -> dict[str, Any]:
    """The last bell struck: watch name, bells, and whether it is striking now (the
    snapshot's `bell` block; spec §9.4)."""
    t = world.clock.ship_time
    start_hour, watch = units.watch_of(t)
    half_hours = (t.hour - start_hour) * 2 + t.minute // 30
    if half_hours == 0:
        bells = 4 if watch == "Last dog watch" else 8
    else:
        bells = half_hours
    return {"watch": watch, "bells": bells, "striking": units.bells_at(t) is not None}


def sail_reading(ship: Any, sail: Sail) -> dict[str, Any]:
    """A sail's state as the grammar and the snapshot both read it: its part state
    ("set", "furled", "blown_out", ..., "wrecked"), whether it is shaking, whether it is
    aback, and its reefs.

    *Aback* is the physics' own flag (`sail.backed`, spec M1 §4). *Shaking* is a studding
    sail shivering (`sail.shivering`, spec 3b §7) or any drawing sail with the apparent
    wind inside its luff: the angle at which the physics says it just fills, its chord's
    angle from the centreline plus its class's luff angle, less a hauled bowline's gain,
    plus the bagginess of worn canvas (physics/sails.py, the ship's luff angle; the same
    terms, per sail). A backed sail is aback, not shaking.
    """
    from freesail.physics import sails as sails_mod
    from freesail.physics.strain import baggy_luff

    state = "wrecked" if sail.wrecked else sail.state.value
    drawing = sail.state in (SailState.SET, SailState.GOOSE_WINGED) and not sail.wrecked
    shaking = False
    if drawing and not sail.backed:
        if sail.shivering:
            shaking = True
        else:
            cls = sails_mod.SAIL_CLASSES.get(sail.cls)
            if cls is not None:
                luff = sails_mod._chord_angle(ship, sail) + cls.luff_angle + baggy_luff(sail)
                if sails_mod.hauled_weather_bowline(ship, sail) is not None:
                    luff -= units.deg_to_rad(sails_mod.BOWLINE_LUFF_GAIN_DEG)
                awa = abs(ship.dyn.apparent_wind_angle)
                # a sail set with its yard square before the wind is not shaking because
                # the wind is aft of its chord; only a wind forward of the luff shakes it
                shaking = awa < luff and ship.dyn.apparent_wind_speed > 0.0
    return {
        "state": state,
        "shaking": shaking,
        "aback": bool(sail.backed) and drawing,
        "reefs": sail.reefs,
    }


def _sail(world: Any, param: str | None) -> dict[str, Any] | None:
    ship = world.ship
    sails = getattr(ship, "sails", None)
    if not sails or param is None:
        return None
    sail = sails.get(param)
    if sail is None:
        target = ship.aliases.get(param)
        sail = sails.get(target) if target else None
    return sail_reading(ship, sail) if sail is not None else None


def _out_of_action(part: Any) -> bool:
    if part.wrecked:
        return True
    if isinstance(part, Spar):
        return part.sent_down
    if isinstance(part, Line):
        return part.state.value == "parted"
    if isinstance(part, Sail):
        return part.state not in (SailState.SET, SailState.GOOSE_WINGED)
    return False


def _strain(world: Any, param: str | None) -> float | None:
    """A part's strain ratio (load over rating), or with no part the worst aboard among
    the parts in action: the ratio the strain model warns above DECAY_RATIO and wrecks
    above CARRY_AWAY_RATIO (physics/strain.py)."""
    ship = world.ship
    parts = getattr(ship, "parts", None)
    if not parts:
        return None if param else 0.0
    if param is not None:
        part = parts.get(param) or parts.get(ship.aliases.get(param, ""))
        return part.strain_ratio if part is not None else None
    worst = 0.0
    for part in parts.values():
        if not _out_of_action(part):
            worst = max(worst, part.strain_ratio)
    return worst


def _crew(world: Any) -> Crew | None:
    extra = getattr(world.ship, "extra", None) or {}
    crew = extra.get("crew")
    return crew if isinstance(crew, Crew) else None


def _mean_fatigue(sailors: list[Any]) -> float:
    if not sailors:
        return 0.0
    return round(sum(s.fatigue for s in sailors) / len(sailors), FATIGUE_DECIMALS)


def _hands_on_deck(world: Any, _: str | None) -> dict[str, Any]:
    crew = _crew(world)
    if crew is None:
        return {"count": 0, "fatigue": 0.0, "words": "fresh"}
    deck = bill.on_deck(crew, world.clock)
    mean = _mean_fatigue(deck)
    return {"count": len(deck), "fatigue": mean, "words": fatigue_words(mean)}


def _watch_below(world: Any, _: str | None) -> dict[str, Any]:
    crew = _crew(world)
    if crew is None:
        return {"count": 0, "fatigue": 0.0, "words": "fresh"}
    below = bill.below(crew, world.clock)
    mean = _mean_fatigue(below)
    return {"count": len(below), "fatigue": mean, "words": fatigue_words(mean)}


# ---------------------------------------------------------------------------
# The registry, with every row of spec §2
# ---------------------------------------------------------------------------

REGISTRY = Registry()

REGISTRY.add(
    Reading(
        "true_wind_speed",
        ("the true wind", "the wind"),
        "speed",
        "knots",
        _true_wind_speed,
        description="the true wind's speed at ten metres, gusts included",
    )
)
REGISTRY.add(
    Reading(
        "true_wind_from",
        ("the true wind", "the wind"),
        "direction",
        "points",
        _true_wind_from,
        description="where the true wind comes from",
    )
)
REGISTRY.add(
    Reading(
        "apparent_wind_angle",
        ("the apparent wind",),
        "angle_on_bow",
        "degrees",
        _apparent_wind_angle,
        description="the apparent wind's angle on the bow, starboard positive",
    )
)
REGISTRY.add(
    Reading(
        "apparent_wind_speed",
        ("the apparent wind",),
        "speed",
        "knots",
        _apparent_wind_speed,
        description="the apparent wind's speed",
    )
)
REGISTRY.add(Reading("heading", ("the heading",), "compass", "", _heading))
REGISTRY.add(Reading("course", ("the course",), "compass", "", _course))
REGISTRY.add(Reading("speed", ("the speed",), "speed", "knots", _speed))
REGISTRY.add(Reading("leeway", ("the leeway",), "angle", "degrees", _leeway))
REGISTRY.add(Reading("heel", ("the heel",), "angle", "degrees", _heel))
REGISTRY.add(Reading("helm", ("the helm",), "angle", "degrees", _helm))
REGISTRY.add(Reading("watch", ("the watch",), "watch", "", _watch))
REGISTRY.add(Reading("time", ("the time",), "bells", "", _bells))
REGISTRY.add(
    Reading(
        "daylight",
        ("daylight",),
        "daylight",
        "",
        _daylight,
        description="day, twilight or night, from the sun at the ship's latitude",
    )
)
REGISTRY.add(
    Reading(
        "sail",
        ("the <sail>",),
        "sail",
        "",
        _sail,
        parametric="sail",
        description="a sail's state: set, shaking, aback, furled, blown out",
    )
)
REGISTRY.add(
    Reading(
        "strain",
        ("the strain", "the <part>"),
        "strain",
        "",
        _strain,
        parametric="part",
        description="the worst strain ratio aboard, or a part's",
    )
)
REGISTRY.add(Reading("hands_on_deck", ("the hands on deck",), "hands", "", _hands_on_deck))
REGISTRY.add(Reading("watch_below", ("the watch below",), "hands", "", _watch_below))
REGISTRY.add_absent(
    "well",
    ("the well",),
    "The ship has no well to sound yet; that reading comes with the world.",
)
REGISTRY.add_absent(
    "glass",
    ("the glass",),
    "The ship has no glass yet; that reading comes with the world.",
)
REGISTRY.add_absent(
    "depth",
    ("the depth",),
    "The ship has no lead line yet; that reading comes with the world.",
)
REGISTRY.add_absent(
    "sail_in_sight",
    ("a sail in sight",),
    "There is nothing to sight yet; that reading comes with the world.",
)


# ---------------------------------------------------------------------------
# Events, for `at` (spec §2)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class EventSpec:
    """A log kind the runtime watches for, and a test on the event's data where the kind
    alone is not enough ("eight bells" is a `clock.bell` with eight in it)."""

    words: str
    kind: str
    test: Callable[[dict[str, Any]], bool] | None = None
    absent: str | None = None  # registered but not yet raised by anything in the world
    data: dict[str, Any] = field(default_factory=dict)


def _bells_test(n: int) -> Callable[[dict[str, Any]], bool]:
    return lambda data: data.get("bells") == n


_BELL_WORDS = {
    1: "one bell",
    2: "two bells",
    3: "three bells",
    4: "four bells",
    5: "five bells",
    6: "six bells",
    7: "seven bells",
    8: "eight bells",
}

EVENTS: dict[str, EventSpec] = {}


def _event(spec: EventSpec) -> None:
    EVENTS[spec.words] = spec


# The sun's two events are package 26's to raise (kinds agreed here so that a rule given
# now fires when the sun arrives).
_event(EventSpec("sunset", "sun.set"))
_event(EventSpec("sunrise", "sun.rise"))
for _n, _w in _BELL_WORDS.items():
    _event(EventSpec(_w, "clock.bell", _bells_test(_n)))
_event(EventSpec("the change of the watch", "watch.relieved"))
_event(EventSpec("a strain warning", "strain.warning"))
_event(EventSpec("a sail shaking", "sail.shivering"))
_event(EventSpec("a spar carrying away", "spar.carried_away"))
_event(EventSpec("a sail blown out", "sail.blown_out"))
_event(EventSpec("all hands called", "crew.all_hands"))
_event(EventSpec("the watch piped down", "crew.piped_down"))
_event(
    EventSpec(
        "a sighting",
        "sighting",
        absent="There is nothing to sight yet; sightings come with the world.",
    )
)
_event(
    EventSpec(
        "a sounding",
        "sounding",
        absent="The ship has no lead line yet; soundings come with the world.",
    )
)


def event_matches(spec: EventSpec, kind: str, data: dict[str, Any]) -> bool:
    if kind != spec.kind:
        return False
    return spec.test(data) if spec.test is not None else True


# ---------------------------------------------------------------------------
# Intervals, for `every` (spec §2): seconds of ship's time
# ---------------------------------------------------------------------------

# "A watch" as an interval is the four-hour watch; the dog watches are the two halves of
# one (Luce 1884, ch. XX; judgement: an order given "every watch" is meant four-hourly).
INTERVALS: dict[str, int] = {
    "a minute": 60,
    "minute": 60,
    "a bell": 1800,
    "bell": 1800,
    "a glass": 1800,
    "glass": 1800,
    "half an hour": 1800,
    "half hour": 1800,
    "the half hour": 1800,
    "an hour": 3600,
    "hour": 3600,
    "a watch": 14400,
    "watch": 14400,
}


def apparent_side(angle: float) -> str:
    """'starboard' or 'larboard' for a signed apparent wind angle."""
    return "starboard" if angle >= 0 else "larboard"


def describe_value(reading: Reading, value: Any) -> str:
    """A reading's value in words, for the log's 'the true wind is 24 knots'."""
    if value is None:
        return "not to be had"
    kind = reading.kind
    if kind == "speed":
        return f"{units.ms_to_knots(value):.0f} knots"
    if kind == "direction":
        return f"from {units.point_name(value)}"
    if kind == "angle_on_bow":
        return f"{units.rad_to_deg(abs(value)):.0f} degrees on the {apparent_side(value)} bow"
    if kind == "compass":
        return units.format_heading(value)
    if kind == "angle":
        return f"{units.rad_to_deg(abs(value)):.0f} degrees"
    if kind == "watch":
        return f"the {value}"
    if kind == "bells":
        return f"{units.format_bells(value['bells'])} in the {value['watch'].lower()}"
    if kind == "sail":
        if value["aback"]:
            return "aback"
        if value["shaking"]:
            return "shaking"
        return str(value["state"]).replace("_", " ")
    if kind == "strain":
        return f"{value:.2f} of the rating"
    if kind == "hands":
        return f"{value['count']} hands, {value['words']}"
    if isinstance(value, float):
        return f"{value:g}"
    return str(value)
