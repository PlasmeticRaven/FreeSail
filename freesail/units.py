"""Units, angles, compass points and bells.

This is the only module that converts between the simulation's SI units and the
nautical units shown to people. Physics works in metres, seconds, kilograms,
newtons and radians. The log, the client and Orders speak knots, feet, fathoms,
compass points, degrees and bells.

Conventions (see docs/TechnicalSpec-M0-M2.md §4):

- Coordinates: x east, y north, metres.
- Heading: radians clockwise from north, 0 = north.
- Wind *direction* is where the wind comes FROM (a north wind blows from the
  north). A wind *vector* points where the air moves. The two conversion
  functions below are the only place that flip happens.
"""

from __future__ import annotations

import math
from datetime import datetime

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

KNOT = 0.514444  # metres per second
FOOT = 0.3048  # metres
FATHOM = 1.8288  # metres (6 feet)
CABLE = 185.2  # metres (one tenth of a nautical mile)
NAUTICAL_MILE = 1852.0  # metres
LONG_TON = 1016.0469  # kilograms
G = 9.80665  # m/s^2
RHO_AIR = 1.225  # kg/m^3
RHO_WATER = 1025.0  # kg/m^3

POINT = math.pi / 16  # one compass point, 11.25 degrees, in radians
TWO_PI = 2 * math.pi


# ---------------------------------------------------------------------------
# Scalar conversions
# ---------------------------------------------------------------------------


def knots_to_ms(knots: float) -> float:
    return knots * KNOT


def ms_to_knots(ms: float) -> float:
    return ms / KNOT


def feet_to_m(feet: float) -> float:
    return feet * FOOT


def m_to_feet(m: float) -> float:
    return m / FOOT


def fathoms_to_m(fathoms: float) -> float:
    return fathoms * FATHOM


def m_to_fathoms(m: float) -> float:
    return m / FATHOM


def m_to_nm(m: float) -> float:
    return m / NAUTICAL_MILE


def nm_to_m(nm: float) -> float:
    return nm * NAUTICAL_MILE


def deg_to_rad(deg: float) -> float:
    return math.radians(deg)


def rad_to_deg(rad: float) -> float:
    return math.degrees(rad)


def points_to_rad(points: float) -> float:
    return points * POINT


def rad_to_points(rad: float) -> float:
    return rad / POINT


# ---------------------------------------------------------------------------
# Angles
# ---------------------------------------------------------------------------


def wrap_pi(angle: float) -> float:
    """Wrap an angle in radians to the range (-pi, pi]."""
    return -((-angle + math.pi) % TWO_PI - math.pi)


def wrap_2pi(angle: float) -> float:
    """Wrap an angle in radians to the range [0, 2*pi)."""
    return angle % TWO_PI


def heading_vector(heading: float) -> tuple[float, float]:
    """Unit vector (x east, y north) of a heading in radians clockwise from north."""
    return math.sin(heading), math.cos(heading)


def vector_heading(x: float, y: float) -> float:
    """Heading in [0, 2*pi) of a vector (x east, y north)."""
    return wrap_2pi(math.atan2(x, y))


def wind_vector(direction_from: float, speed: float) -> tuple[float, float]:
    """Velocity vector of air for a wind FROM `direction_from` at `speed`.

    A north wind (direction_from = 0) blows toward the south: (0, -speed).
    """
    toward = direction_from + math.pi
    return speed * math.sin(toward), speed * math.cos(toward)


def wind_direction_from(vx: float, vy: float) -> float:
    """Direction a wind comes FROM, given the velocity vector of the air."""
    return wrap_2pi(math.atan2(vx, vy) + math.pi)


def relative_bearing(heading: float, direction: float) -> float:
    """Angle of `direction` relative to `heading`, in (-pi, pi]: positive to starboard."""
    return wrap_pi(direction - heading)


# ---------------------------------------------------------------------------
# Compass points
# ---------------------------------------------------------------------------

COMPASS_ABBREVIATIONS: tuple[str, ...] = (
    "N", "N by E", "NNE", "NE by N", "NE", "NE by E", "ENE", "E by N",
    "E", "E by S", "ESE", "SE by E", "SE", "SE by S", "SSE", "S by E",
    "S", "S by W", "SSW", "SW by S", "SW", "SW by W", "WSW", "W by S",
    "W", "W by N", "WNW", "NW by W", "NW", "NW by N", "NNW", "N by W",
)  # fmt: skip

_CARDINAL_WORDS = {"N": "north", "E": "east", "S": "south", "W": "west"}


def _expand_letters(letters: str) -> str:
    """'NNE' -> 'north-north-east', 'NE' -> 'north-east', 'N' -> 'north'."""
    return "-".join(_CARDINAL_WORDS[c] for c in letters)


def point_full_name(abbreviation: str) -> str:
    """'NE by N' -> 'north-east by north'."""
    parts = abbreviation.split(" by ")
    if len(parts) == 1:
        return _expand_letters(parts[0])
    return f"{_expand_letters(parts[0])} by {_expand_letters(parts[1])}"


COMPASS_NAMES: tuple[str, ...] = tuple(point_full_name(a) for a in COMPASS_ABBREVIATIONS)


def _normalise_point_text(text: str) -> str:
    t = text.strip().lower()
    # tolerate "nor'east", "sou'-west" style contractions before dropping apostrophes
    t = t.replace("nor'", "north ").replace("sou'", "south ")
    t = t.replace("-", " ").replace("'", "")
    return " ".join(t.split())


def _build_point_lookup() -> dict[str, int]:
    lookup: dict[str, int] = {}
    for i, abbr in enumerate(COMPASS_ABBREVIATIONS):
        lookup[_normalise_point_text(abbr)] = i
        lookup[_normalise_point_text(abbr).replace(" ", "")] = i
        full = _normalise_point_text(COMPASS_NAMES[i])
        lookup[full] = i
        lookup[full.replace(" ", "")] = i
    return lookup


_POINT_LOOKUP = _build_point_lookup()


def parse_compass_point(text: str) -> float | None:
    """Return the heading in radians of a compass point name, or None if not one.

    Accepts abbreviations ('SW by W'), full names ('south-west by west'), and
    loose spellings ('southwest by west').
    """
    key = _normalise_point_text(text)
    idx = _POINT_LOOKUP.get(key)
    if idx is None:
        idx = _POINT_LOOKUP.get(key.replace(" ", ""))
    if idx is None:
        return None
    return idx * POINT


# A course with a half or a quarter point (package 37l; the review of gate 5c's playtests,
# G17: `steer south by west half west` was steered west, its last word, and the ship was
# taken aback). The card of the period has 128 quarter points, each named from a point
# toward a point within eight points of it: "S by W ½ W", "NE ¾ N", "W ¼ S" (Bowditch's
# table; Falconer 1780, *Compass*). The fraction is said in words or figures ("half",
# "a quarter", "three quarters", "1/2", "½"; the order's normalising has turned the
# figures and the signs into the words by now).
FRACTION_WORDS: dict[tuple[str, ...], float] = {
    ("half",): 0.5,
    ("a", "half"): 0.5,
    ("quarter",): 0.25,
    ("a", "quarter"): 0.25,
    ("one", "quarter"): 0.25,
    ("three", "quarters"): 0.75,
    ("three", "quarter"): 0.75,
}
FRACTION_SIGNS = {0.25: "¼", 0.5: "½", 0.75: "¾"}
# after the fraction, the words that may name it a point's ("half a point west")
_OF_A_POINT = (("a", "point"), ("of", "a", "point"), ("point",))


class CourseError(ValueError):
    """Words that begin a course and cannot be read whole: a fraction with no point to
    reckon it toward, or toward a point that is no way to reckon it."""


def _point_at(words: list[str], i: int) -> tuple[int, int] | None:
    """The compass point (its index, 0 to 31) said at words[i], the longest run of up to
    five words that names one, and the words it took; None when none begins there."""
    for k in range(min(5, len(words) - i), 0, -1):
        idx = _POINT_LOOKUP.get(_normalise_point_text(" ".join(words[i : i + k])))
        if idx is None:
            idx = _POINT_LOOKUP.get(_normalise_point_text("".join(words[i : i + k])))
        if idx is not None:
            return idx, k
    return None


def read_course(words: list[str], i: int = 0) -> tuple[float, str, int] | None:
    """A course said at words[i]: a compass point, with a half or a quarter point
    toward another ('south by west half west', 'wnw half w', 'ne by n quarter n', 'w
    three quarters s'); (the heading in radians, its name as the card has it, 'S by W ½
    W', and the words it took), or None when no point begins there. Raises `CourseError`
    in words when a fraction follows the point and cannot be read whole, so that the
    order is refused and never steered to part of what was said."""
    base = _point_at(words, i)
    if base is None:
        return None
    idx, used = base
    j = i + used
    frac = None
    for said, value in sorted(FRACTION_WORDS.items(), key=lambda kv: -len(kv[0])):
        if tuple(words[j : j + len(said)]) == said:
            frac, j = value, j + len(said)
            break
    name = COMPASS_ABBREVIATIONS[idx]
    if frac is None:
        return idx * POINT, name, used
    for tail in _OF_A_POINT:
        if tuple(words[j : j + len(tail)]) == tail:
            j += len(tail)
            break
    said = " ".join(words[i:j])
    toward = _point_at(words, j)
    if toward is None:
        raise CourseError(
            f"'{said}' toward which point? Say the point the {_fraction_words(frac)} is "
            f"reckoned toward, as '{point_full_name(name)} {_fraction_words(frac)} "
            f"{_toward_example(idx)}'."
        )
    to_idx, to_used = toward
    diff = (to_idx - idx) % 32
    if diff == 0 or diff in range(9, 24):
        raise CourseError(
            f"'{said} {' '.join(words[j : j + to_used])}' is no course: "
            f"{_fraction_phrase(frac)} is reckoned from {name} toward a point within eight "
            f"points of it, as '{point_full_name(name)} {_fraction_words(frac)} "
            f"{_toward_example(idx)}'."
        )
    sign = 1.0 if diff <= 8 else -1.0
    angle = wrap_2pi(idx * POINT + sign * frac * POINT)
    shown = f"{name} {FRACTION_SIGNS[frac]} {COMPASS_ABBREVIATIONS[to_idx]}"
    return angle, shown, j + to_used - i


def _fraction_words(frac: float) -> str:
    return {0.25: "quarter", 0.5: "half", 0.75: "three quarters"}[frac]


def _fraction_phrase(frac: float) -> str:
    return {0.25: "a quarter point", 0.5: "half a point", 0.75: "three quarters of a point"}[frac]


def _toward_example(idx: int) -> str:
    """The cardinal point the next quarter of the card lies toward, clockwise: 'west'
    after S by W."""
    return ("east", "south", "west", "north")[(idx // 8) % 4]


def parse_course(text: str) -> float | None:
    """A course in words, whole ('S by W 1/2 W', 'south by west half west', 'NE'), in
    radians; None when the words are not one course and nothing more. `CourseError`
    when a fraction cannot be read (`read_course`)."""
    t = text.lower().replace("½", " half ").replace("¼", " quarter ").replace("¾", " 3/4 ")
    t = t.replace("1/2", " half ").replace("1/4", " quarter ").replace("3/4", " three quarters ")
    words = t.replace("-", " ").split()
    if not words:
        return None
    got = read_course(words, 0)
    if got is None or got[2] != len(words):
        return None
    return got[0]


def nearest_point_index(angle: float) -> int:
    """Index (0..31) of the compass point nearest to an angle in radians."""
    return int(round(wrap_2pi(angle) / POINT)) % 32


def point_name(angle: float, full: bool = False) -> str:
    """Name of the compass point nearest an angle in radians."""
    idx = nearest_point_index(angle)
    return COMPASS_NAMES[idx] if full else COMPASS_ABBREVIATIONS[idx]


def format_heading(angle: float) -> str:
    """'SW by W (236°)' style display of a heading in radians."""
    deg = rad_to_deg(wrap_2pi(angle))
    return f"{point_name(angle)} ({deg:.0f}°)"


# Where a wind on the ship lies, in the points of sail of the primer's chapter 2 (Lever,
# figures 397 and 398; Falconer, *Large*): forward of the beam it is on the bow; at eight
# points, on the beam; from nine to fourteen points, abaft the beam, on the quarter; from
# fifteen, astern. Each band runs to half a point either side of its points (judgement:
# the nearest point names it, as a sailor would), and the last half point either side of
# dead aft is right astern.
BOW_UNDER_POINTS = 7.5
BEAM_UNDER_POINTS = 8.5
QUARTER_UNDER_POINTS = 14.5
RIGHT_ASTERN_FROM_POINTS = 15.5


def wind_bearing_words(angle: float) -> str:
    """Where a wind at `angle` radians off the bow (positive on the starboard side) lies,
    in words: 'on the larboard bow', 'on the starboard beam', 'on the larboard quarter,
    abaft the beam', 'astern, a little on the starboard quarter', 'right astern'."""
    a = wrap_pi(angle)
    side = "starboard" if a >= 0 else "larboard"
    points = abs(a) / POINT
    if points < BOW_UNDER_POINTS:
        return f"on the {side} bow"
    if points < BEAM_UNDER_POINTS:
        return f"on the {side} beam"
    if points < QUARTER_UNDER_POINTS:
        return f"on the {side} quarter, abaft the beam"
    if points < RIGHT_ASTERN_FROM_POINTS:
        return f"astern, a little on the {side} quarter"
    return "right astern"


# ---------------------------------------------------------------------------
# Watches and bells
# ---------------------------------------------------------------------------

# (start hour inclusive, end hour exclusive, name)
WATCHES: tuple[tuple[int, int, str], ...] = (
    (0, 4, "Middle watch"),
    (4, 8, "Morning watch"),
    (8, 12, "Forenoon watch"),
    (12, 16, "Afternoon watch"),
    (16, 18, "First dog watch"),
    (18, 20, "Last dog watch"),
    (20, 24, "First watch"),
)


def watch_of(dt: datetime) -> tuple[int, str]:
    """Return (start hour, name) of the watch containing `dt`."""
    h = dt.hour
    for start, end, name in WATCHES:
        if start <= h < end:
            return start, name
    raise AssertionError("hour out of range")


def bells_at(dt: datetime) -> int | None:
    """Number of bells struck at `dt` if it falls on a half hour, else None.

    Bells count half hours since the start of the watch. On the hour that
    begins a watch, eight bells are struck (the end of the previous watch);
    at the start of the last dog watch, four. This is the Royal Navy
    convention of the period.
    """
    if dt.second != 0 or dt.minute % 30 != 0:
        return None
    start, name = watch_of(dt)
    half_hours = (dt.hour - start) * 2 + dt.minute // 30
    if half_hours == 0:
        return 4 if name == "Last dog watch" else 8
    return half_hours


def format_bells(n: int) -> str:
    return "1 bell" if n == 1 else f"{n} bells"


def time_stamp(dt: datetime) -> str:
    """'Forenoon watch, 3 bells (09:30)' or 'Forenoon watch (09:37)'."""
    _, name = watch_of(dt)
    bells = bells_at(dt)
    clock = dt.strftime("%H:%M")
    if bells is None:
        return f"{name} ({clock})"
    return f"{name}, {format_bells(bells)} ({clock})"


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------


def format_speed(ms: float) -> str:
    return f"{ms_to_knots(ms):.1f} kn"


def format_wind(direction_from: float, speed_ms: float) -> str:
    return f"{point_name(direction_from)}, {ms_to_knots(speed_ms):.0f} knots"


def describe_wind_strength(speed_ms: float) -> str:
    """Period-flavoured wind strength words, roughly on the Beaufort scale."""
    kn = ms_to_knots(speed_ms)
    if kn < 1:
        return "calm"
    if kn < 4:
        return "light airs"
    if kn < 7:
        return "a light breeze"
    if kn < 11:
        return "a gentle breeze"
    if kn < 17:
        return "a moderate breeze"
    if kn < 22:
        return "a fresh breeze"
    if kn < 28:
        return "a strong breeze"
    if kn < 34:
        return "a moderate gale"
    if kn < 41:
        return "a fresh gale"
    if kn < 48:
        return "a strong gale"
    if kn < 56:
        return "a whole gale"
    if kn < 64:
        return "a storm"
    return "a hurricane"
