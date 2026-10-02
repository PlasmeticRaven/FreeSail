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

import functools
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from freesail import units
from freesail.crew import bill
from freesail.crew.model import Crew, fatigue_words
from freesail.physics.hull import WAY_ON_KN
from freesail.physics.motion import MOTION_STATE_WORDS
from freesail.physics.strain import DECAY_RATIO
from freesail.ship.parts import Dynamics, HelmMode, Line, Sail, SailState, Spar
from freesail.world.sea import SEA_STATE_WORDS
from freesail.world.weather import (
    SKY_WORDS,
    TENDENCY_WORDS,
    VISIBILITY_WORDS,
    WEATHER_WORDS,
)

if TYPE_CHECKING:
    from freesail.core.world import World

__all__ = [
    "EVENTS",
    "FATIGUE_DECIMALS",
    "GLASS_UNWATCHED_WORDS",
    "INTERVALS",
    "KINDS",
    "MOTION_STATE_WORDS",
    "NO_CHART_WORDS",
    "NO_GLASS_WORDS",
    "NO_TACKLE_WORDS",
    "NO_ANCHOR_DOWN_WORDS",
    "NO_RECKONING_WORDS",
    "NO_SEA_WORDS",
    "NO_WAY_WORDS",
    "NO_WEATHER_WORDS",
    "SEA_STATE_WORDS",
    "SKY_WORDS",
    "TENDENCY_WORDS",
    "VISIBILITY_WORDS",
    "WEATHER_WORDS",
    "READING_SPEED_FLOOR_KN",
    "Angle",
    "STERNWAY_WORDS",
    "REGISTRY",
    "Reading",
    "ReadingsView",
    "Registry",
    "SAIL_STATE_WORDS",
    "STRAINING_RATIO",
    "WATCH_NAMES",
    "event_matches",
    "reading_words",
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
    "direction": "a direction: backs, veers or shifts N points, is from a compass point",
    "gust": "the wind against its ten-minute mean: is a gust, is at the mean, is a lull",
    "angle_on_bow": "an angle on the bow: is forward of or abaft N degrees or the beam",
    "compass": "a compass heading: is a point, is east of or west of a point",
    "angle": "an angle in degrees: exceeds, is over, is under, is below",
    "watch": "a watch: is the middle watch, is not the first watch",
    "bells": "the bells: is eight bells",
    "daylight": "day, twilight or night: is night, is not day",
    "sail": "a sail's state: is set, is shaking, is aback, is furled, is blown out",
    "strain": "the strain: exceeds the rating, exceeds 1.2, is straining",
    "hands": "the hands: exceeds N, are fresh, are tired, are worn out",
    "glass": "the glass in inches: exceeds, is over, is under, is below 29.5",
    "tendency": "the glass's tendency: is steady, is rising, is falling, is falling fast, "
    "is turning",
    "sky": "the sky: is clear, is overcast, is dark and gloomy, is threatening, is hazy",
    "weather": "the weather: is fine, is rain, is drizzle, is squally, is fog",
    "visibility": "the visibility: is the horizon, is a few miles, is a mile, is a cable",
    "sea": "the sea: is smooth, is moderate, is short, is heavy, is very heavy, is confused, "
    "gets up",
    "motion": "the motion: is easy, is rolling, is rolling heavily, is pitching, is labouring",
    "sight": "what the lookout sees: is in sight, is not in sight",
    "depth": "a depth in fathoms: exceeds, is over, is under, is below 10 fathoms",
    # the reckoning's readings (spec M5 §15, package 33a)
    "position": "a position by account: is north of 49 30 N, is south of, is east of 6 W, "
    "is west of",
    "distance": "a distance in miles: exceeds, is over, is under, is below 20 miles",
    "ground": "the ground the lead brings up: is sand, is mud, is not rock",
    "person": "a person's place: is on deck, is below",
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

# Under this much headway the course she makes and her leeway are not readings at all
# (playtest 1: "Leeway 145°" from a standing start; playtest 3: the course NW by W with
# the heading E by N, in stays). Judgement: half a knot, the same floor as the hull's
# `LEEWAY_MIN_SPEED` (physics/hull.py, 0.25 m/s), below which the physics reads leeway as
# nil (physics/hull.py WAY_ON_KN, the one number); the primer's chapter 2 says leeway has
# no meaning without way on. Headway is the
# speed ahead through the water (`Dynamics.u`), so a ship making sternway reads so too.
# The log's leeway line keeps the same floor (`physics/integrate.py`).
READING_SPEED_FLOOR_KN = WAY_ON_KN
NO_WAY_WORDS = "no way on; course and leeway not meaningful"
STERNWAY_WORDS = "making sternway; course and leeway not meaningful"

DAYLIGHT_WORDS: tuple[str, ...] = ("day", "twilight", "night")

# The weather's readings (spec M5 §5) when the ship cannot give them: a ship with no glass
# has neither the glass nor its tendency (W §1.7: in 1805 a glass aboard is the captain's
# own, and a small vessel may have none; the scenario says); the tendency wants an hour's
# record; a scenario without weather systems keeps no sky. Lower-case, as NO_WAY_WORDS.
NO_GLASS_WORDS = "the ship carries no glass"
GLASS_UNWATCHED_WORDS = "the glass has not been watched an hour yet"
NO_WEATHER_WORDS = "no weather is kept in this scenario; the sky comes with its systems"
# The sea and the motion (spec M5 §4) are kept when the wind has a cause, or when the
# scenario asks for them; a fixed or a pinned wind alone keeps no sea.
NO_SEA_WORDS = "no sea is kept in this scenario; the sea comes with the wind's cause"

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
    # the words for a value of None that the reading gives on purpose (the course with
    # no way on), read over the World; None: `describe_value`'s "not to be had"
    none_words: Callable[[Any], str | None] | None = None

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

    def words(self, id: str, param: str | None = None) -> str:
        """A reading in words, as an agent reads it (`reading_words`)."""
        return reading_words(self._registry.get(id), self.value(id, param), self._world)


# ---------------------------------------------------------------------------
# Getters over the World. Each reads the physics' own number and nothing else.
# ---------------------------------------------------------------------------


def _dyn(world: Any) -> Dynamics | None:
    return getattr(world.ship, "dyn", None)


def _true_wind_speed(world: Any, _: str | None) -> float:
    return world.wind.effective_speed  # m/s at the reference height, gust included


def _true_wind_from(world: Any, _: str | None) -> float:
    return world.wind.direction_from  # radians, where it comes from


def _wind_record(world: Any) -> Any:
    return getattr(world, "wind_record", None)


def _mean_wind_speed(world: Any, _: str | None) -> float:
    """The true wind's speed over the last ten minutes (`physics.wind.WindRecord`); the
    instant's before the first tick."""
    record = _wind_record(world)
    mean = record.mean_speed() if record is not None else None
    return world.wind.effective_speed if mean is None else mean


def _mean_wind_from(world: Any, _: str | None) -> float:
    record = _wind_record(world)
    mean = record.mean_from() if record is not None else None
    return world.wind.direction_from if mean is None else mean


def _against_mean(world: Any, _: str | None) -> str:
    """The instant's true wind against its ten-minute mean, in words: 'a gust above the
    mean', 'at the mean' or 'a lull' (`physics.wind.against_mean`)."""
    from freesail.physics.wind import against_mean

    return against_mean(world.wind.effective_speed, _mean_wind_speed(world, None))


def _before_the_clock(world: Any) -> bool:
    """No tick has run: the physics has not yet written the ship's apparent wind, and the
    dynamics still hold their zeros (playtest 3: 0 knots of apparent wind in a 15-knot
    breeze at 04:00, corrected once the clock ran)."""
    return world.clock.tick == 0


def _apparent_now(world: Any) -> tuple[float, float]:
    """The apparent wind on deck as the sails model computes it each substep, where the
    helmsman's eye is (`sails._apparent` at the deck height and WIND_EYE_HEIGHT_M): the
    same function over the same state, read without writing anything, for a ship that
    has not yet had a tick."""
    from freesail.physics import sails as sails_mod

    ship = world.ship
    flow = sails_mod._apparent(
        ship, world.wind, ship.hull.spec.deck_height_m + sails_mod.WIND_EYE_HEIGHT_M
    )
    return flow.awa, flow.speed


def _apparent_wind_angle(world: Any, _: str | None) -> float:
    d = _dyn(world)
    if d is None:
        return 0.0
    if _before_the_clock(world):
        return _apparent_now(world)[0]
    return d.apparent_wind_angle  # signed radians, + starboard


def _apparent_wind_speed(world: Any, _: str | None) -> float:
    d = _dyn(world)
    if d is None:
        return world.wind.effective_speed
    if _before_the_clock(world):
        return _apparent_now(world)[1]
    return d.apparent_wind_speed


def _heading(world: Any, _: str | None) -> float:
    return world.ship.heading


def _no_way(world: Any) -> bool:
    """Headway under `READING_SPEED_FLOOR_KN` (a ship with dynamics only; the point ship
    of the early milestones has no leeway and its course is the one ordered)."""
    d = _dyn(world)
    return d is not None and d.u < units.knots_to_ms(READING_SPEED_FLOOR_KN)


def _no_way_words(world: Any) -> str | None:
    d = _dyn(world)
    if d is None or not _no_way(world):
        return None
    return STERNWAY_WORDS if d.u <= -units.knots_to_ms(READING_SPEED_FLOOR_KN) else NO_WAY_WORDS


def _course(world: Any, _: str | None) -> float | None:
    """The course ordered: the helm's target when steering a heading, else the heading
    she has (full and by, or a rudder order, has no course but the one she makes). None
    with no way on (`READING_SPEED_FLOOR_KN`): in stays, or gathering way from rest, the
    course is not meaningful and the words say so."""
    d = _dyn(world)
    if d is None:
        return getattr(world.ship, "target_heading", world.ship.heading)
    if _no_way(world):
        return None
    return d.target_heading if d.helm_mode is HelmMode.HEADING else d.heading


def _speed(world: Any, _: str | None) -> float:
    d = _dyn(world)
    return d.speed if d is not None else world.ship.speed


def _leeway(world: Any, _: str | None) -> float | None:
    """The physics' leeway; None with no way on (`READING_SPEED_FLOOR_KN`)."""
    d = _dyn(world)
    if d is None:
        return 0.0
    if _no_way(world):
        return None
    return d.leeway


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


def _glass_of(world: Any) -> Any:
    return getattr(world, "glass", None)


def _conditions_of(world: Any) -> Any:
    return getattr(world, "conditions", None)


def _glass(world: Any, _: str | None) -> float | None:
    """The glass in inches to the hundredth, as the vernier reads, with the ship's own
    reading noise (`world.weather.Glass`); None without a glass."""
    glass = _glass_of(world)
    return glass.reading_in if glass is not None else None


def _tendency(world: Any, _: str | None) -> dict[str, Any] | None:
    """The glass's change over the last three hours and the last hour, in inches, and the
    period's words for it: steady, rising, falling, rising fast, falling fast; from the
    ship's own record, so None without a glass or before an hour of record."""
    glass = _glass_of(world)
    return glass.tendency() if glass is not None else None


def _no_glass_words(world: Any) -> str | None:
    glass = _glass_of(world)
    if glass is None:
        return NO_GLASS_WORDS
    return GLASS_UNWATCHED_WORDS


def _sky(world: Any, _: str | None) -> dict[str, Any] | None:
    """Beaufort's letters as words, with Luce's signs for the log's colour; from the
    sector and the distance to the front (`world.weather.Weather.conditions_at`)."""
    c = _conditions_of(world)
    return {"words": c.sky, "signs": c.signs} if c is not None else None


def _weather(world: Any, _: str | None) -> str | None:
    c = _conditions_of(world)
    return c.weather if c is not None else None


def _visibility(world: Any, _: str | None) -> dict[str, Any] | None:
    """How far a sail can be seen, in the lookout's terms, and the miles that means (the
    number 5b's sighting reads)."""
    c = _conditions_of(world)
    return {"words": c.visibility, "miles": c.visibility_nm} if c is not None else None


def _no_weather_words(world: Any) -> str | None:
    return NO_WEATHER_WORDS if _conditions_of(world) is None else None


def _sea(world: Any, _: str | None) -> dict[str, Any] | None:
    """The sea in the period's words with the state word the dialect compares and the
    numbers behind them (`world.sea.Sea.reading`); None where no sea is kept."""
    sea = getattr(world, "sea", None)
    return sea.reading().to_dict() if sea is not None else None


def _motion(world: Any, _: str | None) -> dict[str, Any] | None:
    """The ship's motion in words, with the roll, the pitch and the heave behind them
    (`physics.motion.Motion.reading`); None where no sea is kept."""
    motion = getattr(world, "motion", None)
    return motion.reading().to_dict() if motion is not None else None


def _no_sea_words(world: Any) -> str | None:
    return NO_SEA_WORDS if getattr(world, "sea", None) is None else None


# The chart's readings (spec M5 §11, §12; package 32): what the lookout sees, whether the
# land is among it, and the depth of water by the chart; a world without a chart region
# reads None for all three, in NO_CHART_WORDS.
NO_CHART_WORDS = "No chart of these waters: the world has no coast here yet."


def _lookout_of(world: Any) -> Any:
    return getattr(world, "lookout", None)


def _in_sight(world: Any, _: str | None) -> dict[str, Any] | None:
    """The last look's sightings in the lookout's words (`world.lookout.Lookout.reading`):
    the count, the words and each item with its bearing and estimated distance; None
    without a chart."""
    lookout = _lookout_of(world)
    return lookout.reading(float(world.ship.heading)) if lookout is not None else None


def _land(world: Any, _: str | None) -> dict[str, Any] | None:
    """Whether any land (a headland, an island, a mark, a light, a danger) is in sight,
    with the nearest; None without a chart."""
    lookout = _lookout_of(world)
    return lookout.land(float(world.ship.heading)) if lookout is not None else None


def _depth_of_water(world: Any, _: str | None) -> float | None:
    """The depth of water by the chart at the ship's position, in metres at the datum
    (the tide of package 34 goes on top): the world's own number, which the lead of
    package 33 casts for with its error and its age; None without a chart or where the
    chart has nothing."""
    chart = getattr(world, "chart", None)
    pos = getattr(world, "position", None)
    if chart is None or pos is None:
        return None
    return chart.depth_at(pos)


def _no_chart_words(world: Any) -> str | None:
    return NO_CHART_WORDS if getattr(world, "chart", None) is None else None


# The reckoning's readings (spec M5 §13, §15; package 33a; `world.reckoning.Navigation`):
# the captain's account and never the truth. A world with no position keeps no
# reckoning, and every row reads None in NO_RECKONING_WORDS.
NO_RECKONING_WORDS = (
    "No reckoning is kept: the scenario gives no position, and there is no sea here."
)


def _navigation_of(world: Any) -> Any:
    return getattr(world, "navigation", None)


def _reckoning(world: Any, _: str | None) -> dict[str, Any] | None:
    """`the reckoning`: the position by account, in degrees and in words."""
    nav = _navigation_of(world)
    return nav.reckoning_reading() if nav is not None else None


def _reckoning_uncertainty(world: Any, _: str | None) -> dict[str, Any] | None:
    """`the reckoning's uncertainty`: the master's words, and behind them the larger of
    the east-west and north-south doubts in metres (the dialect compares it in miles)."""
    nav = _navigation_of(world)
    if nav is None:
        return None
    r = nav.reckoning
    worst = max(r.sigma_east_nm, r.sigma_north_nm)
    return {
        "metres": units.nm_to_m(worst),
        "words": r.uncertainty_words,
        "east_nm": r.sigma_east_nm,
        "north_nm": r.sigma_north_nm,
    }


def _no_reckoning_words(world: Any) -> str | None:
    return NO_RECKONING_WORDS if _navigation_of(world) is None else None


def _depth(world: Any, _: str | None) -> float | None:
    """`the depth`: the last cast's depth in metres (the lead's, with its error and its
    age; distinct from the chart's `the depth of water`); None before a cast."""
    nav = _navigation_of(world)
    return nav.depth_reading() if nav is not None else None


def _no_cast_words(world: Any) -> str | None:
    nav = _navigation_of(world)
    return NO_RECKONING_WORDS if nav is None else nav.no_cast_words()


def _ground(world: Any, _: str | None) -> dict[str, Any] | None:
    """`the ground`: what the arming brought up at the last cast, with its age."""
    nav = _navigation_of(world)
    return nav.ground_reading() if nav is not None else None


def _bearing_of(world: Any, param: str | None) -> float | None:
    """`the bearing of <mark>`: a mark in sight, its bearing by compass as the master
    lays it down, in radians; None when not in sight."""
    nav = _navigation_of(world)
    if nav is None:
        return None
    found = nav.bearing_reading(param)
    return None if found is None else float(found["bearing"])


def _not_in_sight_words(world: Any) -> str | None:
    if _navigation_of(world) is None:
        return NO_RECKONING_WORDS
    return "not in sight"


def _run_since_noon(world: Any, _: str | None) -> dict[str, Any] | None:
    """`the distance run since noon`, by account."""
    nav = _navigation_of(world)
    if nav is None:
        return None
    since = nav.since_noon_reading()
    if since is None:
        return None  # no noon yet: `_no_noon_words` says the run since the departure
    run, _ = since
    return {"metres": units.nm_to_m(run), "words": _miles(run)}


def _course_made_good(world: Any, _: str | None) -> float | None:
    """`the course made good` since noon, by account, in radians; None with no distance
    made, or before the first noon."""
    nav = _navigation_of(world)
    if nav is None:
        return None
    since = nav.since_noon_reading()
    if since is None or since[1] is None:
        return None
    return units.deg_to_rad(since[1])


def _no_noon_words(world: Any) -> str | None:
    nav = _navigation_of(world)
    return NO_RECKONING_WORDS if nav is None else nav.no_noon_words()


def _latitude_by_observation(world: Any, _: str | None) -> dict[str, Any] | None:
    """`the latitude by observation`: today's noon latitude; None without a sight."""
    nav = _navigation_of(world)
    if nav is None:
        return None
    lat = nav.latitude_reading()
    if lat is None:
        return None
    from freesail.world.geo import Position, format_position

    return {"lat_deg": lat, "words": format_position(Position(lat, 0.0)).split(",")[0]}


def _no_sight_words(world: Any) -> str | None:
    nav = _navigation_of(world)
    return NO_RECKONING_WORDS if nav is None else nav.no_sight_words()


def _master(world: Any, _: str | None) -> dict[str, Any] | None:
    """`the master`: his name and his place (spec §22's minimum), and what occupies him."""
    nav = _navigation_of(world)
    if nav is None:
        return None
    m = nav.master
    busy = f", at the {m.occupied_with}" if m.occupied_with else ""
    return m.to_dict() | {"words": f"{m.name}, {m.place}{busy}"}


def _miles(nm: float) -> str:
    n = round(nm)
    if n <= 0:
        return "half a mile" if nm >= 0.25 else "no distance"
    return "a mile" if n == 1 else f"{n} miles"


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
# The mean wind (package 29b, playtest 7's finding 4), beside the instant's: a watcher
# that reads a single gust as a rise of the wind has the ten minutes' mean and the label.
REGISTRY.add(
    Reading(
        "mean_true_wind_speed",
        ("the mean wind", "the mean true wind"),
        "speed",
        "knots",
        _mean_wind_speed,
        description="the true wind's speed over the last ten minutes, gusts and lulls in it",
    )
)
REGISTRY.add(
    Reading(
        "mean_true_wind_from",
        ("the mean wind", "the mean true wind"),
        "direction",
        "points",
        _mean_wind_from,
        description="where the true wind has come from over the last ten minutes",
    )
)
REGISTRY.add(
    Reading(
        "true_wind_against_mean",
        ("the true wind", "the wind"),
        "gust",
        "",
        _against_mean,
        description="the true wind now against its ten-minute mean: a gust, the mean, a lull",
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
REGISTRY.add(
    Reading(
        "course",
        ("the course",),
        "compass",
        "",
        _course,
        description="the course ordered, or the heading she makes; none with no way on",
        none_words=_no_way_words,
    )
)
REGISTRY.add(Reading("speed", ("the speed",), "speed", "knots", _speed))
REGISTRY.add(
    Reading(
        "leeway",
        ("the leeway",),
        "angle",
        "degrees",
        _leeway,
        description="the leeway she makes; none with no way on",
        none_words=_no_way_words,
    )
)
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
# The weather's readings (spec M5 §5, package 30). `the glass` is two rows behind one
# phrase, as the true wind is: its height in inches and its tendency in words; a ship
# without a glass reads None for both, in NO_GLASS_WORDS, and the dialect's `when the
# glass is falling fast then shorten sail` parses on any ship and fires on none without.
REGISTRY.add(
    Reading(
        "glass",
        ("the glass", "the barometer"),
        "glass",
        "inches",
        _glass,
        description="the glass in inches to the hundredth, with the ship's own reading noise",
        none_words=_no_glass_words,
    )
)
REGISTRY.add(
    Reading(
        "tendency",
        ("the glass", "the barometer", "the tendency"),
        "tendency",
        "",
        _tendency,
        description="the glass's change over three hours and one hour, in the period's words",
        none_words=_no_glass_words,
    )
)
REGISTRY.add(
    Reading(
        "sky",
        ("the sky",),
        "sky",
        "",
        _sky,
        description="the sky in Beaufort's words, with the signs Luce lists",
        none_words=_no_weather_words,
    )
)
REGISTRY.add(
    Reading(
        "weather",
        ("the weather",),
        "weather",
        "",
        _weather,
        description="the weather: fine, rain, drizzle, passing showers, squally, thunder, fog",
        none_words=_no_weather_words,
    )
)
REGISTRY.add(
    Reading(
        "visibility",
        ("the visibility",),
        "visibility",
        "",
        _visibility,
        description="how far a sail can be seen: the horizon, a few miles, a mile, a cable",
        none_words=_no_weather_words,
    )
)
# The sea and the motion (spec M5 §4, package 31): the period's words with a state word
# the dialect compares (`when the sea is heavy then ...`), None in NO_SEA_WORDS where the
# scenario keeps no sea.
REGISTRY.add(
    Reading(
        "sea",
        ("the sea",),
        "sea",
        "",
        _sea,
        description="the sea in the period's words: smooth, moderate, a short chopping sea, "
        "heavy, a long swell, a confused sea",
        none_words=_no_sea_words,
    )
)
REGISTRY.add(
    Reading(
        "motion",
        ("the motion", "the ship's motion"),
        "motion",
        "",
        _motion,
        description="how she moves in it: easy, rolling, rolling heavily, pitching into it, "
        "labouring heavily",
        none_words=_no_sea_words,
    )
)
# The chart's readings (spec M5 §11, §12; package 32): the lookout's sightings, the land,
# and the depth of water by the chart (distinct from `the depth` of the lead's last cast,
# which package 33 raises). None in NO_CHART_WORDS where the scenario names no region.
REGISTRY.add(
    Reading(
        "in_sight",
        ("what is in sight", "the sightings"),
        "sight",
        "",
        _in_sight,
        description="what the lookout has in sight, by compass bearing and estimated distance",
        none_words=_no_chart_words,
    )
)
REGISTRY.add(
    Reading(
        "land",
        ("the land",),
        "sight",
        "",
        _land,
        description="whether any land, mark or light is in sight, and the nearest",
        none_words=_no_chart_words,
    )
)
REGISTRY.add(
    Reading(
        "depth_of_water",
        ("the depth of water", "the water"),
        "depth",
        "fathoms",
        _depth_of_water,
        description="the depth of water by the chart at the datum, in fathoms",
        none_words=_no_chart_words,
    )
)
# The reckoning's readings (spec M5 §15; package 33a): the captain's account, never the
# truth; each None in NO_RECKONING_WORDS on the endless plane, and with its own absent
# words where the account has nothing yet (no cast, no sight, nothing in sight).
REGISTRY.add(
    Reading(
        "reckoning",
        ("the reckoning", "the dead reckoning", "the position by account"),
        "position",
        "",
        _reckoning,
        description="the position by account: '49° 52' N, 6° 10' W by account'",
        none_words=_no_reckoning_words,
    )
)
REGISTRY.add(
    Reading(
        "reckoning_uncertainty",
        ("the reckoning's uncertainty", "the reckonings uncertainty", "the uncertainty"),
        "distance",
        "miles",
        _reckoning_uncertainty,
        description="how far the master would not trust the reckoning, in his words",
        none_words=_no_reckoning_words,
    )
)
REGISTRY.add(
    Reading(
        "depth",
        ("the depth",),
        "depth",
        "fathoms",
        _depth,
        description="the depth by the last cast of the lead, in fathoms",
        none_words=_no_cast_words,
    )
)
REGISTRY.add(
    Reading(
        "ground",
        ("the ground", "the bottom"),
        "ground",
        "",
        _ground,
        description="the ground the arming brought up at the last cast, with its age",
        none_words=_no_cast_words,
    )
)
REGISTRY.add(
    Reading(
        "bearing_of",
        ("the bearing of <mark>",),
        "compass",
        "",
        _bearing_of,
        parametric="mark",
        description="the bearing by compass of a mark in sight, as the master lays it down",
        none_words=_not_in_sight_words,
    )
)
REGISTRY.add(
    Reading(
        "run_since_noon",
        ("the distance run since noon", "the run since noon", "the distance run"),
        "distance",
        "miles",
        _run_since_noon,
        description="the distance run since noon, by account; none before the first noon",
        none_words=_no_noon_words,
    )
)
REGISTRY.add(
    Reading(
        "course_made_good",
        ("the course made good",),
        "compass",
        "",
        _course_made_good,
        description="the course made good since noon, by account",
        none_words=_no_noon_words,
    )
)
REGISTRY.add(
    Reading(
        "latitude_by_observation",
        ("the latitude by observation", "the observed latitude", "the latitude"),
        "position",
        "",
        _latitude_by_observation,
        description="today's latitude by the noon sight",
        none_words=_no_sight_words,
    )
)
REGISTRY.add(
    Reading(
        "master",
        ("the master",),
        "person",
        "",
        _master,
        description="the master: his name, his place and what occupies him",
        none_words=_no_reckoning_words,
    )
)
# `a sail in sight` was registered absent here from milestone 4 to package 34; package 35
# registers it below as a reading of the lookout's (the pilot cutter the first sail).

# ---------------------------------------------------------------------------
# Package 33c: the manoeuvre in hand (playtest 13's brig: the trim rules belayed by hand
# through a night hove to, for want of `if she is not hove to`). A row of its own, in this
# block, changing nothing above.
# ---------------------------------------------------------------------------

KINDS["manoeuvre"] = (
    "the manoeuvre in hand: is hove to, is not hove to, is tacking, is wearing, is none"
)

# The manoeuvres by their evolutions' ids (`data/evolutions/`), in the gerund the log says
# them in; a manoeuvre is in hand from its first step to its last.
MANOEUVRE_WORDS: dict[str, str] = {
    "tack": "tacking",
    "wear": "wearing",
    "heave_to": "heaving to",
    "lie_a_try": "heaving to",
    "fill_away": "filling away",
    "boxhaul": "box hauling",
    "wear_short_round": "wearing short round",
    "back_and_fill": "backing and filling",
    "scud": "bearing up to scud",
}
# What she is doing when no manoeuvre is in hand: lying to, or nothing.
HOVE_TO_WORDS = "hove to"
NO_MANOEUVRE_WORDS = "none"


def _manoeuvre(world: Any, _: str | None) -> str:
    """`the manoeuvre in hand`: the manoeuvre the hands are at (tacking, wearing, heaving
    to, filling away), from the evolution runner's work in hand; else 'hove to' while she
    lies to (the heave-to's record on the ship, `ship.extra["hove_to"]`, which filling away
    clears), else 'none'."""
    extra = getattr(world.ship, "extra", None) or {}
    runner = extra.get("evolutions")
    for inst in getattr(runner, "instances", None) or ():
        words = MANOEUVRE_WORDS.get(inst.evo.id)
        if words is not None and not inst.waiting:
            return words
    return HOVE_TO_WORDS if "hove_to" in extra else NO_MANOEUVRE_WORDS


REGISTRY.add(
    Reading(
        "manoeuvre_in_hand",
        ("the manoeuvre in hand", "the manoeuvre"),
        "manoeuvre",
        "",
        _manoeuvre,
        description="the manoeuvre in hand: hove to, heaving to, tacking, wearing, filling "
        "away, or none",
    )
)


# ---------------------------------------------------------------------------
# Package 33b: the chronometer, the moon, the lunar, the variation, and the chart in the
# captain's hands (spec M5 §14, §15; decision 30). Each row reads the account and never
# the truth; each None in its own words. The kinds are the dialect's own: a longitude
# by chronometer or by lunar is a position ("is west of 6 W"), the chronometer and its
# error by lunar are distances (the master's trust and the error in miles of longitude:
# "when the chronometer exceeds 10 miles then take a lunar"), the moon a sight ("is in
# sight": up and the sky clear), the variation an angle whose words carry its source.
# ---------------------------------------------------------------------------


class Angle(float):
    """An angle in radians that carries its words (the variation: '24° W by amplitude,
    10 June'); the dialect compares the number, an agent reads the words."""

    words: str = ""

    def __new__(cls, value: float, words: str = "") -> Angle:
        self = super().__new__(cls, value)
        self.words = words
        return self


def _chronometer(world: Any, _: str | None) -> dict[str, Any] | None:
    """`the chronometer`: its time at Greenwich, the days since rated, its winding; the
    master's trust in miles of longitude behind it; None without one."""
    nav = _navigation_of(world)
    return nav.chronometer_reading() if nav is not None else None


def _no_chronometer_words(world: Any) -> str | None:
    nav = _navigation_of(world)
    return NO_RECKONING_WORDS if nav is None else nav.no_chronometer_words()


def _longitude_by_chronometer(world: Any, _: str | None) -> dict[str, Any] | None:
    """`the longitude by chronometer`: today's time sight with the days since rated and
    the master's trust; None without one today."""
    nav = _navigation_of(world)
    return nav.longitude_by_chronometer_reading() if nav is not None else None


def _no_time_sight_words(world: Any) -> str | None:
    nav = _navigation_of(world)
    return NO_RECKONING_WORDS if nav is None else nav.no_time_sight_words()


def _longitude_by_lunar(world: Any, _: str | None) -> dict[str, Any] | None:
    """`the longitude by lunar`: the last lunar, with its date and the master's trust."""
    nav = _navigation_of(world)
    return nav.longitude_by_lunar_reading() if nav is not None else None


def _no_lunar_words(world: Any) -> str | None:
    nav = _navigation_of(world)
    return NO_RECKONING_WORDS if nav is None else nav.no_lunar_words()


def _chronometer_error(world: Any, _: str | None) -> dict[str, Any] | None:
    """`the chronometer's error by lunar`: the last lunar against the chronometer."""
    nav = _navigation_of(world)
    return nav.chronometer_error_reading() if nav is not None else None


def _no_chronometer_error_words(world: Any) -> str | None:
    nav = _navigation_of(world)
    return NO_RECKONING_WORDS if nav is None else nav.no_chronometer_error_words()


def _moon(world: Any, _: str | None) -> dict[str, Any] | None:
    """`the moon`: its age and phase, up or not, in distance of a body or not."""
    nav = _navigation_of(world)
    return nav.moon_reading() if nav is not None else None


def _variation(world: Any, _: str | None) -> Angle | None:
    """`the variation` the master allows, west positive, with its source and date."""
    nav = _navigation_of(world)
    if nav is None:
        return None
    return Angle(nav.variation_reading(), nav.variation.words)


def _bearing_by_chart(world: Any, param: str | None) -> float | None:
    """`the bearing of <mark> by the chart`: from the account to any charted feature,
    in sight or not, by compass; None where the chart has no such name."""
    nav = _navigation_of(world)
    found = nav.by_chart(param) if nav is not None and param else None
    return None if found is None else float(found["bearing"])


@functools.lru_cache(maxsize=256)
def _pricked(words: str) -> Any:
    """A point pricked on the chart from its words, or None; read once per words (a
    book's rule asks every tick)."""
    import re

    from freesail.world.geo import parse_position

    try:
        return parse_position(re.sub(r"\b(degrees?|minutes?)\b", " ", words))
    except ValueError:
        return None


def _distance_to(world: Any, param: str | None) -> dict[str, Any] | None:
    """`the distance to <mark>`: from the account to any charted feature, by account; or
    to a point pricked on the chart ('48 20 N 4 36 W': the books' waypoints, package 36),
    likewise by account."""
    nav = _navigation_of(world)
    if nav is None or not param:
        return None
    found = nav.by_chart(param)
    if found is None:
        from freesail.world.geo import bearing_and_distance, format_position

        pricked = _pricked(param)
        if pricked is None:
            return None
        now = nav.account_now()
        bearing, dist = bearing_and_distance(now, pricked)
        from freesail.world.reckoning import miles_words

        return {
            "name": format_position(pricked),
            "bearing_deg": round(bearing, 1),
            "metres": dist,
            "words": f"{miles_words(dist / units.NAUTICAL_MILE)} by account",
        }
    return found | {"metres": found["metres"], "words": found["distance_words"]}


def _not_charted_words(world: Any) -> str | None:
    if _navigation_of(world) is None:
        return NO_RECKONING_WORDS
    return "not on the chart"


def _dangers(world: Any, param: str | None) -> dict[str, Any] | None:
    """`the dangers`: the charted dangers within ten miles of the account (or within
    the miles said), the nearest first; the nearest's distance behind the words."""
    nav = _navigation_of(world)
    if nav is None:
        return None
    within = None
    if param:
        digits = "".join(c for c in param if c.isdigit() or c == ".")
        within = float(digits) if digits else None
    return nav.dangers(within)


def _no_dangers_words(world: Any) -> str | None:
    nav = _navigation_of(world)
    return NO_RECKONING_WORDS if nav is None else nav.no_dangers_words()


REGISTRY.add(
    Reading(
        "chronometer",
        ("the chronometer",),
        "distance",
        "miles",
        _chronometer,
        description="the chronometer: its time at Greenwich, the days since rated, its "
        "winding; the master's trust in miles of longitude",
        none_words=_no_chronometer_words,
    )
)
REGISTRY.add(
    Reading(
        "longitude_by_chronometer",
        ("the longitude by chronometer", "the longitude"),
        "position",
        "",
        _longitude_by_chronometer,
        description="today's longitude by the time sight, with the days since rated and "
        "the master's trust",
        none_words=_no_time_sight_words,
    )
)
REGISTRY.add(
    Reading(
        "longitude_by_lunar",
        ("the longitude by lunar", "the longitude by the lunar"),
        "position",
        "",
        _longitude_by_lunar,
        description="the last longitude by lunar, with its date and the master's trust",
        none_words=_no_lunar_words,
    )
)
REGISTRY.add(
    Reading(
        "chronometer_error_by_lunar",
        (
            "the chronometer's error by lunar",
            "the chronometers error by lunar",
            "the chronometer's error",
            "the chronometers error",
        ),
        "distance",
        "miles",
        _chronometer_error,
        description="the chronometer against the last lunar: gaining or losing on its rate, "
        "in seconds of time and miles of longitude",
        none_words=_no_chronometer_error_words,
    )
)
REGISTRY.add(
    Reading(
        "moon",
        ("the moon",),
        "sight",
        "",
        _moon,
        description="the moon: its age and phase, up or not, in distance of a body or not",
        none_words=_no_reckoning_words,
    )
)
REGISTRY.add(
    Reading(
        "variation",
        ("the variation", "the variation of the compass"),
        "angle",
        "degrees",
        _variation,
        description="the variation the master allows, by the chart or by observation, "
        "with its date",
        none_words=_no_reckoning_words,
    )
)
REGISTRY.add(
    Reading(
        "bearing_by_chart",
        ("the bearing of <mark> by the chart", "the bearing by the chart of <mark>"),
        "compass",
        "",
        _bearing_by_chart,
        parametric="mark",
        description="the bearing by compass from the account to any charted feature, in "
        "sight or not",
        none_words=_not_charted_words,
    )
)
REGISTRY.add(
    Reading(
        "distance_to",
        ("the distance to <mark>", "the distance of <mark>"),
        "distance",
        "miles",
        _distance_to,
        parametric="mark",
        description="the distance from the account to any charted feature, by account",
        none_words=_not_charted_words,
    )
)
REGISTRY.add(
    Reading(
        "dangers",
        ("the dangers", "the charted dangers"),
        "distance",
        "miles",
        _dangers,
        description="the charted dangers within ten miles of the account, the nearest first, "
        "by name, bearing and distance; the nearest's distance is the number",
        none_words=_no_dangers_words,
    )
)


# ---------------------------------------------------------------------------
# Package 34: the tide as the captain has it, the anchor and the cable (spec M5 §16, §18)
# ---------------------------------------------------------------------------
# No reading gives the world's tide: `the tide by the almanac` is the master's, from the
# epitome's establishment and Moore's rule on the moon's age (decision 29). The anchor's
# and the cable's readings are the ship's own state (the forecastle sees the cable and
# the buoy), and the ground's when she is aground.

NO_TACKLE_WORDS = "She carries no ground tackle: this ship's file lists no anchors."
NO_ANCHOR_DOWN_WORDS = "no anchor is down"


def _tide_by_almanac(world: Any, _: str | None) -> dict[str, Any] | None:
    """`the tide by the almanac`: high water today at the nearest place of the master's
    table, by the establishment and the moon's age; never the world's tide."""
    nav = _navigation_of(world)
    return nav.tide_by_almanac() if nav is not None else None


def _tackle_of(world: Any) -> Any:
    from freesail.ship.parts import ground_tackle

    return ground_tackle(world.ship)


def _anchor(world: Any, _: str | None) -> dict[str, Any] | None:
    """`the anchor`: down (riding by which, to the flood or the ebb, the cable out),
    aweigh, catted, at the bows, lost; aground, where and how she struck. None for a
    ship with no ground tackle."""
    tackle = _tackle_of(world)
    if tackle is None:
        return None
    from freesail.physics.anchor import riding_words
    from freesail.ship.parts import AnchorState

    aground = (getattr(world.ship, "extra", None) or {}).get("aground")
    if aground:
        words = f"aground, {aground.get('where', 'the ground under her')}"
        if aground.get("bottom"):
            words += f" on {aground['bottom']}"
        return {"words": words, "state": "aground", "anchor": None} | dict(aground)
    riding = tackle.riding_by()
    if riding is not None:
        state = getattr(world, "tide_state", None)
        how = riding_words(world.ship, state, world.wind.direction_from)
        how = how[:1].lower() + how[1:]
        words = f"down, {how.rstrip('.')}, {riding.scope_fathoms:.0f} fathoms out"
        if riding.dragging:
            words = f"dragging; {words}"
        moored = len([a for a in tackle.down() if a.kind == "bower"]) >= 2  # package 35
        if moored:
            words = f"moored with two anchors; {words}"
        return {"words": words, "state": "down", "anchor": riding.id, "moored": moored} | (
            riding.to_dict()
        )
    # no anchor down: the one furthest along in its evolution, else the best bower
    order = (AnchorState.AWEIGH, AnchorState.CATTED, AnchorState.READY, AnchorState.LOST)
    for st in order:
        for a in tackle.anchors:
            if a.state is st:
                return {
                    "words": a.state.value,
                    "state": a.state.value,
                    "anchor": a.id,
                } | a.to_dict()
    bowers = tackle.bowers() or tackle.anchors
    a = bowers[0]
    return {"words": a.state.value, "state": a.state.value, "anchor": a.id} | a.to_dict()


def _no_tackle_words(world: Any) -> str | None:
    return NO_TACKLE_WORDS if _tackle_of(world) is None else None


def _cable(world: Any, _: str | None) -> Angle | None:
    """`the cable`: the riding cable's scope and strain against its rating, taut or
    slack; the number is the strain, as a line's. None with no anchor down."""
    tackle = _tackle_of(world)
    if tackle is None:
        return None
    riding = tackle.riding_by()
    if riding is None:
        return None
    ratio = riding.cable_strain_ratio
    lie = "bar-taut" if riding.taut else "slack"
    words = (
        f"{riding.scope_fathoms:.0f} fathoms of the {riding.name.replace('the ', '')}'s "
        f"{tackle.cable_words} out, {lie}, the strain {ratio:.2f} of the rating"
    )
    if riding.cable_condition < 99.5:
        words += f", the {tackle.cable_words} worn to {riding.cable_condition:.0f}"
    return Angle(ratio, words)


def _no_cable_words(world: Any) -> str | None:
    return NO_TACKLE_WORDS if _tackle_of(world) is None else NO_ANCHOR_DOWN_WORDS


def _ground_tackle(world: Any, _: str | None) -> dict[str, Any] | None:
    """`the ground tackle`: every anchor, its weight, its cable and its state."""
    tackle = _tackle_of(world)
    if tackle is None:
        return None
    return {"words": " ".join(tackle.describe()), "anchors": [a.to_dict() for a in tackle.anchors]}


REGISTRY.add(
    Reading(
        "tide_by_almanac",
        ("the tide by the almanac", "high water by the almanac", "the tide"),
        "position",
        "",
        _tide_by_almanac,
        description="high water today at the nearest place of the master's table, by the "
        "establishment and the moon's age (the master's tide, never the world's)",
        none_words=_no_reckoning_words,
    )
)
REGISTRY.add(
    Reading(
        "anchor",
        ("the anchor",),
        "ground",
        "",
        _anchor,
        description="the anchor: down (riding by which, to the flood or the ebb, the cable "
        "out), dragging, aweigh, catted, at the bows, lost; or aground, where",
        none_words=_no_tackle_words,
    )
)
REGISTRY.add(
    Reading(
        "cable",
        ("the cable",),
        "strain",
        "",
        _cable,
        description="the riding cable: the scope, taut or slack, the strain against its "
        "rating (the number)",
        none_words=_no_cable_words,
    )
)
REGISTRY.add(
    Reading(
        "ground_tackle",
        ("the ground tackle",),
        "ground",
        "",
        _ground_tackle,
        description="the anchors and their cables, each with its weight and state",
        none_words=_no_tackle_words,
    )
)


# ---------------------------------------------------------------------------
# Package 35: the people, the places and their ledgers, the port and the other sail
# (spec M5 §22 to §25). Every row's words are the world's own (`freesail.world.people`,
# `places`, `ports`, the lookout's `sail`); nothing is computed a second way, and the
# truth is not in them (the pilot's tide is the port's own, which he knows as a man who
# lives by it: the one way the world's tide reaches the captain, through a person).
# ---------------------------------------------------------------------------

NO_PEOPLE_WORDS = "no people are kept: the ship is not in a world"
NO_PILOT_WORDS = "no pilot aboard"
NO_PORT_WORDS = "no port within the pilot's cruising ground"
NO_HOLD_WORDS = "no hold is kept: the ship's file gives her no room for a cargo"


def _people(world: Any, _: str | None) -> dict[str, Any] | None:
    people = getattr(world, "people", None)
    if people is None:
        return None
    return {
        "words": " ".join(people.describe()),
        "count": len(people.all),
        "people": [p.to_dict() | {"state": people.state_words(p)} for p in people.all],
    }


def _no_people_words(world: Any) -> str | None:
    return NO_PEOPLE_WORDS


def _where_is(world: Any, param: str | None) -> dict[str, Any] | None:
    """`where is <person>`: his name and his state; the standing dialect compares his
    place as the master's (is on deck, is below)."""
    people = getattr(world, "people", None)
    if people is None or not param:
        return None
    found = people.where_is(param)
    if found is None:
        return None
    where = found["place"]
    if not found.get("aboard", True):
        place = "ashore"
    elif where in ("quarterdeck", "deck", "tops"):
        place = "on deck"
    else:
        place = "below"
    return found | {"where": where, "place": place}


def _places(world: Any, _: str | None) -> dict[str, Any] | None:
    """`the places`: the names in the words (every sample carries them, so the static
    descriptions ride in `items`, where the prompt's answer and the pane find them)."""
    from freesail.world.places import PLACES

    places = getattr(world, "places", None)
    if places is None:
        return None
    return {
        "words": ", ".join(p.name for p in PLACES.values()),
        "items": {p.id: {"name": p.name, "description": p.description} for p in PLACES.values()},
        "described": places.describe(),
    }


def _ports_of(world: Any) -> Any:
    ports = getattr(world, "ports", None)
    return ports if ports is not None and ports.ports else None


def _pilot(world: Any, _: str | None) -> dict[str, Any] | None:
    ports = _ports_of(world)
    return ports.pilot_reading() if ports is not None else None


def _no_pilot_words(world: Any) -> str | None:
    return NO_PILOT_WORDS


def _port(world: Any, _: str | None) -> dict[str, Any] | None:
    ports = _ports_of(world)
    return ports.port_words() if ports is not None else None


def _no_port_words(world: Any) -> str | None:
    return (
        NO_PORT_WORDS
        if _ports_of(world) is not None
        else NO_CHART_WORDS[:1].lower() + NO_CHART_WORDS[1:]
    )


def _boat(world: Any, _: str | None) -> dict[str, Any] | None:
    ports = getattr(world, "ports", None)
    return ports.boat_reading() if ports is not None else None


def _boats(world: Any, _: str | None) -> dict[str, Any] | None:
    ports = getattr(world, "ports", None)
    return {"words": ports.boats_words()} if ports is not None else None


def _prices(world: Any, _: str | None) -> dict[str, Any] | None:
    ports = _ports_of(world)
    return ports.prices_reading() if ports is not None else None


def _no_prices_words(world: Any) -> str | None:
    ports = _ports_of(world)
    return ports.no_prices_words() if ports is not None else NO_PORT_WORDS


def _manifest(world: Any, _: str | None) -> dict[str, Any] | None:
    hold = getattr(world, "hold", None)
    if hold is None or hold.capacity_tons <= 0:
        return None
    return {
        "words": hold.words(),
        "capacity_tons": hold.capacity_tons,
        "stowed_tons": round(hold.stowed_tons, 2),
        "room_tons": round(hold.room_tons, 2),
        "goods": dict(hold.goods),
    }


def _no_hold_words(world: Any) -> str | None:
    return NO_HOLD_WORDS


def _purse(world: Any, _: str | None) -> dict[str, Any] | None:
    purse = getattr(world, "purse", None)
    if purse is None:
        return None
    return {"words": purse.words(), "pounds": round(purse.pounds, 2)}


def _stores(world: Any, _: str | None) -> dict[str, Any] | None:
    stores = getattr(world, "stores", None)
    if stores is None:
        return None
    return {
        "words": stores.words(),
        "water_tons": stores.water_tons,
        "provisions_days": stores.provisions_days,
    }


def _epitome(world: Any, _: str | None) -> dict[str, Any] | None:
    papers = getattr(world, "papers", None)
    if papers is None or getattr(world, "navigation", None) is None:
        return None
    page = papers.page("the epitome's table of the establishments")
    return {"words": " ".join(page.lines), "lines": list(page.lines), "as_of": page.as_of}


def _sail_in_sight(world: Any, _: str | None) -> dict[str, Any] | None:
    lookout = _lookout_of(world)
    return lookout.sail(float(world.ship.heading)) if lookout is not None else None


def _strangers(world: Any, _: str | None) -> dict[str, Any] | None:
    """`the strangers` (spec M5 §25; package 36): every sail in sight with her bearing,
    her distance by estimation and what has been made out of her; never her position."""
    lookout = _lookout_of(world)
    return lookout.strangers(world, float(world.ship.heading)) if lookout is not None else None


def _stranger_in_sight(world: Any, _: str | None) -> dict[str, Any] | None:
    """`a stranger in sight` (package 36): the strangers alone, a sail being one until
    her colours are made out for the ship's own nation's."""
    lookout = _lookout_of(world)
    if lookout is None:
        return None
    ports = getattr(world, "ports", None)
    own = ports.ship_nation if ports is not None else None
    return lookout.stranger(world, float(world.ship.heading), own)


REGISTRY.add(
    Reading(
        "people",
        ("the people",),
        "ground",
        "",
        _people,
        description="the named people aboard, each by name and role with his place and state",
        none_words=_no_people_words,
    )
)
REGISTRY.add(
    Reading(
        "where_is",
        ("where is <person>",),
        "person",
        "",
        _where_is,
        parametric="person",
        description="a person by his role or his name: his place and state (is on deck, is below)",
        none_words=_no_people_words,
    )
)
REGISTRY.add(
    Reading(
        "places",
        ("the places",),
        "ground",
        "",
        _places,
        description="the places aboard, each a name and a description",
        none_words=_no_people_words,
    )
)
REGISTRY.add(
    Reading(
        "pilot",
        ("the pilot",),
        "ground",
        "",
        _pilot,
        description="the pilot aboard: his name and port, and when the tide serves by his word",
        none_words=_no_pilot_words,
    )
)
REGISTRY.add(
    Reading(
        "port",
        ("the port",),
        "ground",
        "",
        _port,
        description="the port she is in or near: its stance to her, the pilot, the cutter and "
        "the boat",
        none_words=_no_port_words,
    )
)
REGISTRY.add(
    Reading(
        "boat",
        ("the boat",),
        "ground",
        "",
        _boat,
        description="the ship's boat: alongside, or away on its errand and where",
        none_words=_no_people_words,
    )
)
REGISTRY.add(
    Reading(
        "boats",
        ("the boats",),
        "ground",
        "",
        _boats,
        description="the boats she carries, each with its length, oars and crew",
        none_words=_no_people_words,
    )
)
REGISTRY.add(
    Reading(
        "prices",
        ("the prices",),
        "ground",
        "",
        _prices,
        description="the prices at the port she lies in, as the purser last brought them off",
        none_words=_no_prices_words,
    )
)
REGISTRY.add(
    Reading(
        "manifest",
        ("the manifest",),
        "ground",
        "",
        _manifest,
        description="the hold: the cargo in it by tons and the room left",
        none_words=_no_hold_words,
    )
)
REGISTRY.add(
    Reading(
        "purse",
        ("the purse",),
        "ground",
        "",
        _purse,
        description="the money aboard, in pounds",
        none_words=_no_people_words,
    )
)
REGISTRY.add(
    Reading(
        "stores",
        ("the stores",),
        "ground",
        "",
        _stores,
        description="the purser's stores: water by the ton, provisions by the day",
        none_words=_no_people_words,
    )
)
REGISTRY.add(
    Reading(
        "epitome",
        ("the epitome",),
        "ground",
        "",
        _epitome,
        description="the epitome's table of the establishments: high water at full and change "
        "by port",
        none_words=_no_reckoning_words,
    )
)
REGISTRY.add(
    Reading(
        "sail_in_sight",
        ("a sail in sight",),
        "sight",
        "",
        _sail_in_sight,
        description="other sail in sight: in sight or not, each with the lookout's words",
        none_words=_no_chart_words,
    )
)
REGISTRY.add(
    Reading(
        "stranger_in_sight",
        ("a stranger in sight", "a stranger"),
        "sight",
        "",
        _stranger_in_sight,
        description="a sail in sight not known for the ship's own nation: every sail until "
        "her colours are made out, and one under none or another nation's after",
        none_words=_no_chart_words,
    )
)
REGISTRY.add(
    Reading(
        "strangers",
        ("the strangers", "what sail is in sight"),
        "sight",
        "",
        _strangers,
        description="every sail in sight: her bearing, her distance by estimation and what "
        "has been made out of her (her rig, her course, her colours or none)",
        none_words=_no_chart_words,
    )
)


# ---------------------------------------------------------------------------
# Events, for `at` (spec §2)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class EventSpec:
    """A log kind the runtime watches for, and a test on the event's data where the kind
    alone is not enough ("eight bells" is a `clock.bell` with eight in it); `also`, more
    kinds that are the same event ("a change in the sky" is the sky's line or the
    weather's).

    Or, where the log has no line for it, a reading's change (package 31c): `watch` is a
    condition in the standing dialect's words, and the event is that condition coming to
    hold, each time it does ("the glass falling fast" is the tendency coming to "falling
    fast"). One condition serves both watchers: a stand-by (`agents.harness`) and a
    standing order's `at` (`standing.rules.event_condition`, which the runtime evaluates as
    a `when`), so the dialect has the event for nothing and the two cannot disagree."""

    words: str
    kind: str
    test: Callable[[dict[str, Any]], bool] | None = None
    absent: str | None = None  # registered but not yet raised by anything in the world
    data: dict[str, Any] = field(default_factory=dict)
    also: tuple[str, ...] = ()
    watch: str | None = None  # the dialect's condition whose coming to hold is the event


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
# a squall (spec M5 §3): the wind's own event in unstable air, logged by name
_event(EventSpec("a squall", "weather.squall"))
# The weather's other events to stand by for (package 31c; playtest 11's finding 3: "the
# watcher's work is weather, but I can't stand by for a wind shift, the glass turning or
# falling fast, the sea getting up, or a change in the sky"). The sky's and the weather's
# words each have a line in the log when they change; the rest are the readings' changes,
# watched as conditions (`EventSpec.watch`), since the log says a shift only past two
# points of the wind itself and never the glass's tendency.
#   a wind shift: the ten minutes' mean wind a point or more from where it stood when the
#     watch for it began (a stand-by, a standing order), and afresh from each shift; the
#     mean and not the wind itself, which wanders a point either way in any breeze (the
#     day under systems: W and W by N by turns all its forenoon)
#   the glass falling fast: its tendency coming to "falling fast" (a tenth in three hours)
#   the glass turning: the last hour's change against the three hours' (`rules`,
#     GLASS_TURN_IN): the rise after the low, the fall after the high
#   (the glass's two once a fall or a turn: again only after an hour without, since its
#     words hover about their thresholds; `standing.rules.EVENT_SETTLE_S`)
#   the sea getting up: its words changing upward (a short sea to a heavy one)
_event(EventSpec("a wind shift", "", watch="the mean wind shifts 1 point"))
_event(EventSpec("the glass falling fast", "", watch="the glass is falling fast"))
_event(EventSpec("the glass turning", "", watch="the glass is turning"))
_event(EventSpec("the sea getting up", "", watch="the sea gets up"))
_event(EventSpec("a change in the sky", "weather.sky", also=("weather.change",)))
# The lookout's sighting (package 32 raised the line; package 33a names the event), a
# landfall (the look that first raises the land), a sounding (the lead's cast, package
# 33a), and noon (the day's work, the log-book's page turned).
_event(EventSpec("a sighting", "lookout.sighting"))
_event(EventSpec("a landfall", "lookout.sighting", lambda data: bool(data.get("landfall"))))
_event(EventSpec("a sounding", "sounding"))
_event(EventSpec("noon", "reckoning.noon"))
# the manoeuvres' ends, for a passage's book (package 33a: `at filled away then steer N
# by E`, after the fill-away has left the helm), by the evolutions' own kinds
_event(EventSpec("hove to", "ship.hove_to"))
_event(EventSpec("filled away", "ship.filled_away"))
# and the tack's and the wear's ends (the lead, before gate 5b: the passage wears at the
# outer road and heaves to on the seaward tack, `at wore then heave to on the starboard
# tack`, since a ship lying to forereaches and a bay is a lee shore)
_event(EventSpec("tacked", "ship.tacked"))
_event(EventSpec("wore", "ship.wore"))
# Package 33b: a danger sighted (the lookout's hail of a rock or a ledge), a bearing
# steady and closing (the lookout's collision rule, `lookout.closing`), a lunar cleared
# and a longitude by chronometer had (the reckoning's lines), the chronometer run down
# (a scenario event: it was not wound), and the variation observed.
_event(
    EventSpec("a danger sighted", "lookout.sighting", lambda data: data.get("seen_as") == "danger")
)
_event(EventSpec("a bearing steady and closing", "lookout.closing"))
_event(EventSpec("a lunar", "reckoning.lunar"))
_event(EventSpec("a longitude by chronometer", "reckoning.time_sight"))
_event(EventSpec("the chronometer run down", "chronometer.dead"))
_event(EventSpec("the variation observed", "reckoning.variation"))
# Package 34: the anchor's evolutions' ends and the ground's events (spec M5 §18), by the
# evolutions' and the World's kinds (`data/evolutions/*anchor*.yaml`, `world/ground.py`).
_event(EventSpec("the anchor let go", "ship.anchored"))
_event(EventSpec("brought up", "ship.brought_up"))
_event(EventSpec("the anchor aweigh", "ship.aweigh"))
_event(EventSpec("the anchor weighed", "ship.weighed"))
_event(EventSpec("under way", "ship.weighed"))
_event(EventSpec("the anchor dragging", "anchor.dragging"))
_event(EventSpec("the cable parted", "cable.parted"))
_event(EventSpec("aground", "ship.aground"))
_event(EventSpec("the ground taken", "ship.aground"))
_event(EventSpec("afloat", "ship.afloat"))
_event(EventSpec("the turn of the tide", "ship.swung"))
# which way she swung (package 36; the merchant passage's book takes the Goulet on the
# flood and not on the ebb): the same line, read by its data
_event(EventSpec("the turn to the flood", "ship.swung", lambda data: data.get("flood") is True))
_event(EventSpec("the turn to the ebb", "ship.swung", lambda data: data.get("flood") is False))
# Package 35: the people's, the port's and the other sail's events (spec M5 §22 to §25),
# by the World's kinds (`world/people.py`, `world/ports.py`, the lookout's sail).
_event(EventSpec("a sail sighted", "lookout.sighting", lambda data: data.get("seen_as") == "sail"))
_event(EventSpec("sail ho", "lookout.sighting", lambda data: data.get("seen_as") == "sail"))
_event(EventSpec("the pilot aboard", "port.pilot_aboard"))
_event(EventSpec("the pilot refused", "port.pilot_refused"))
_event(EventSpec("the pilot off", "port.pilot_left"))
_event(EventSpec("the boat away", "boat.away"))
_event(EventSpec("the boat alongside", "boat.alongside"))
_event(EventSpec("a message", "message.received"))
_event(EventSpec("a letter", "message.received"))
_event(EventSpec("moored", "ship.moored"))
_event(EventSpec("unmoored", "ship.unmoored"))
_event(EventSpec("the kedge laid", "ship.kedged"))
_event(EventSpec("got under way", "ship.under_way"))
EVENTS["under way"] = EventSpec("under way", "ship.weighed", also=("ship.under_way",))
_event(EventSpec("the hands entered", "crew.entered"))
_event(EventSpec("the yard's stores aboard", "yard.done"))
# Package 36: the other sail's events (spec M5 §25), by the lookout's kinds
# (`world/lookout.py`): what the tops make out as she nears, her colours made out, a sail
# lost from the horizon; and a vessel within hail (`world/ships.py`).
_event(EventSpec("a sail made out", "lookout.made_out"))
_event(
    EventSpec(
        "a stranger's colours made out", "lookout.made_out", lambda data: bool(data.get("colours"))
    )
)
_event(EventSpec("a sail lost", "lookout.sail_lost"))
_event(EventSpec("a sail within hail", "sail.within_hail"))
# and the pilot cutter's hail (package 35's kind; the merchant passage's book shortens
# sail on it, as the cutter asks) and the cargo's coming aboard and going ashore
_event(EventSpec("the pilot's hail", "port.pilot_hail"))
_event(EventSpec("the cargo aboard", "market.bought"))


def event_matches(spec: EventSpec, kind: str, data: dict[str, Any]) -> bool:
    """Whether a log line of `kind` with `data` is the event. An event that is a reading's
    change (`EventSpec.watch`) is never a line: its watcher evaluates its condition."""
    if not kind or (kind != spec.kind and kind not in spec.also):
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


def reading_words(reading: Reading, value: Any, world: Any = None) -> str:
    """A reading's value in words for an agent: `describe_value`, or, for a value of
    None the reading gives on purpose, its own words (the course and the leeway with no
    way on: `NO_WAY_WORDS`)."""
    if value is None and reading.none_words is not None and world is not None:
        words = reading.none_words(world)
        if words:
            return words
    return describe_value(reading, value)


def describe_value(reading: Reading, value: Any) -> str:
    """A reading's value in words, for the log's 'the true wind is 24 knots'."""
    if value is None:
        return "not to be had"
    # package 33b: a number that carries its own words (`Angle`, the variation)
    if getattr(value, "words", None):
        return str(value.words)
    kind = reading.kind
    if kind == "speed":
        return f"{units.ms_to_knots(value):.0f} knots"
    if kind == "direction":
        return f"from {units.point_name(value)}"
    if kind == "angle_on_bow":
        # the points of sail of the primer's chapter 2: on the bow, on the beam, abaft
        # the beam on the quarter, astern (`units.wind_bearing_words`)
        return f"{units.rad_to_deg(abs(value)):.0f} degrees {units.wind_bearing_words(value)}"
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
    if kind == "gust":
        return str(value)
    if kind == "glass":
        return f"{value:.2f} inches"
    if kind == "tendency":
        return tendency_in_words(value)
    if kind == "sky":
        return f"{value['words']}, {value['signs']}" if value.get("signs") else str(value["words"])
    if kind == "weather":
        return str(value)
    if kind in ("visibility", "sea", "motion"):
        return str(value["words"])
    if kind == "sight":
        return str(value["words"])
    if kind == "depth":
        # the chart's depth in the lead's terms: fathoms to the half (a mark or a deep)
        from freesail.world.chart import fathoms_words

        return fathoms_words(value)
    if kind in ("position", "distance", "person"):
        return str(value["words"])
    if kind == "ground":
        return str(value.get("said") or value["words"])
    if isinstance(value, float):
        return f"{value:g}"
    return str(value)


def _inches_words(change: float) -> str:
    """'fallen three hundredths', 'risen a tenth': a change of the glass in words."""
    n = round(abs(change) * 100)
    if n == 0:
        return "steady"
    verb = "risen" if change > 0 else "fallen"
    amount = {1: "a hundredth", 10: "a tenth", 20: "two tenths"}.get(n, f"{n} hundredths")
    return f"{verb} {amount}"


def tendency_in_words(value: dict[str, Any]) -> str:
    """'falling; fallen five hundredths in three hours, two in the last hour'."""
    words = str(value["words"])
    three, one = value.get("three_hours_in"), value.get("one_hour_in")
    parts = []
    if three is not None:
        parts.append(f"{_inches_words(three)} in three hours")
    if one is not None:
        parts.append(f"{_inches_words(one)} in the last hour")
    return f"{words}; {', '.join(parts)}" if parts else words
