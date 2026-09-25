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
