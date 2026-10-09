"""The geographic frame (spec M5 §9; the study `docs/design/ChartData.md` §5.1).

The world frame is latitude and longitude on the sphere whose minute of arc is the
nautical mile (WGS 84 for the data; the game says nothing of datums). The ship's
motion each tick stays in metres in her own local frame, and the World converts the
tick's run at its end (C §5.1):

    dφ = dy / R,   dλ = dx / (R cos φ)

so that the conversion is per tick and not per region: at 48 to 51 N a hundred-mile box
treated as flat is wrong by a few per cent between its north and south edges. A scenario
that gives no `position` keeps the endless plane of milestones 0 to 5a: `ship_x` and
`ship_y` are metres from the start there as they always were, and nothing here is read.

Also here: the bearing and distance between two positions (the haversine and the initial
great-circle bearing, for the lookout and the log), the geographic horizon from a height
of eye (spec §11: 2.08 (√h_eye + √h_object) miles with heights in metres), positions in
degrees and minutes when the game says them at all, and distances in the log's words:
cables, miles and leagues, with the lookout's estimate to the nearest mile or league (the
estimate is the period's, never the truth to a cable).
"""

from __future__ import annotations

import math
import re
import unicodedata
from dataclasses import dataclass
from functools import lru_cache
from typing import Any

from freesail import units

__all__ = [
    "EARTH_RADIUS_M",
    "name_words",
    "HORIZON_NM_PER_ROOT_METRE",
    "LEAGUE_M",
    "Position",
    "bearing_and_distance",
    "destination",
    "distance_words",
    "estimate_words",
    "format_position",
    "horizon_nm",
    "parse_position",
]

# The sphere on which a minute of arc of the meridian is the nautical mile of 1852 m
# (`units.NAUTICAL_MILE`; `core.sun.METRES_PER_DEGREE` is sixty of them): 6,366,707 m.
# The WGS 84 mean radius is 6,371,009 m, seven parts in ten thousand more; the sun, the
# chart and the log all count in the nautical mile, so this is the radius that keeps a
# mile a mile.
EARTH_RADIUS_M = 60.0 * units.NAUTICAL_MILE * 180.0 / math.pi

# A league of three nautical miles, the log's unit for a distance off (Falconer 1780,
# "League": three miles).
LEAGUE_M = 3.0 * units.NAUTICAL_MILE

# The geographic horizon: d (nautical miles) = 2.08 (√h_eye + √h_object), heights in
# metres (spec M5 §11; C §5.5). Bowditch's 1.17 √h(feet) is the same figure with the
# standard refraction (1.17 √(h/0.3048) = 2.12 √h; 2.08 is the study's rounding and is
# kept as the spec's number).
HORIZON_NM_PER_ROOT_METRE = 2.08


@dataclass(frozen=True)
class Position:
    """A point on the sphere: latitude and longitude in degrees, north and east
    positive."""

    lat_deg: float
    lon_deg: float

    def advanced(self, dx_m: float, dy_m: float) -> Position:
        """This position after a run of `dx_m` east and `dy_m` north (C §5.1): the
        latitude first, the longitude at the mean latitude of the step."""
        if dx_m == 0.0 and dy_m == 0.0:
            return self
        lat = self.lat_deg + math.degrees(dy_m / EARTH_RADIUS_M)
        mid = math.radians(0.5 * (self.lat_deg + lat))
        scale = math.cos(mid)
        if abs(scale) < 1e-9:
            lon = self.lon_deg
        else:
            lon = self.lon_deg + math.degrees(dx_m / (EARTH_RADIUS_M * scale))
        return Position(lat, _wrap_lon(lon))

    def offset_to(self, other: Position) -> tuple[float, float]:
        """Metres east and north from here to `other` on the flat approximation at the
        mean latitude: for the short ranges of a lookout and a chart tile."""
        mid = math.radians(0.5 * (self.lat_deg + other.lat_deg))
        dy = math.radians(other.lat_deg - self.lat_deg) * EARTH_RADIUS_M
        dlon = _wrap_lon(other.lon_deg - self.lon_deg)
        dx = math.radians(dlon) * EARTH_RADIUS_M * math.cos(mid)
        return dx, dy

    def to_dict(self) -> dict[str, float]:
        return {"lat_deg": self.lat_deg, "lon_deg": self.lon_deg}

    @classmethod
    def from_dict(cls, d: Any) -> Position:
        if isinstance(d, Position):
            return d
        if isinstance(d, str):
            return parse_position(d)
        if isinstance(d, (list, tuple)) and len(d) == 2:
            return cls(float(d[0]), float(d[1]))
        if isinstance(d, dict):
            lat = d.get("lat_deg", d.get("lat", d.get("latitude_deg")))
            lon = d.get("lon_deg", d.get("lon", d.get("longitude_deg")))
            if lat is None or lon is None:
                raise ValueError(
                    "a position is {lat_deg, lon_deg}, or a string like 49 52 N 6 10 W"
                )
            return cls(float(lat), float(lon))
        raise ValueError(f"not a position: {d!r}")

    def __str__(self) -> str:
        return format_position(self)


def _wrap_lon(lon: float) -> float:
    return ((lon + 180.0) % 360.0) - 180.0


def name_words(name: str) -> list[str]:
    """A name's words as a name is matched (package 37l; the review of gate 5c's
    playtests, G17: "The lavandiere is not in sight; did you mean the Lavandière?"):
    lower case, its accents folded ('Béniguet' is 'beniguet'), its apostrophes dropped
    ("St Anthony's" is 'st anthonys', said with the apostrophe or without), every other
    mark of punctuation a space. Remembered by the name: a book's `the distance to
    <place>` asks it of the same names every tick."""
    return list(_name_words(str(name)))


@lru_cache(maxsize=8192)
def _name_words(name: str) -> tuple[str, ...]:
    folded = name.lower()
    if not folded.isascii():
        folded = unicodedata.normalize("NFKD", folded)
        folded = "".join(c for c in folded if not unicodedata.combining(c))
    folded = folded.replace("'", "").replace("\u2019", "").replace("\u2018", "")
    return tuple("".join(c if c.isalnum() or c.isspace() else " " for c in folded).split())


def bearing_and_distance(a: Position, b: Position) -> tuple[float, float]:
    """The initial great-circle bearing from `a` to `b` in degrees true (0 to 360) and
    the distance in metres by the haversine, on the game's sphere."""
    la, lb = math.radians(a.lat_deg), math.radians(b.lat_deg)
    dlon = math.radians(_wrap_lon(b.lon_deg - a.lon_deg))
    dlat = lb - la
    h = math.sin(dlat / 2) ** 2 + math.cos(la) * math.cos(lb) * math.sin(dlon / 2) ** 2
    h = min(1.0, max(0.0, h))
    distance = 2.0 * EARTH_RADIUS_M * math.asin(math.sqrt(h))
    y = math.sin(dlon) * math.cos(lb)
    x = math.cos(la) * math.sin(lb) - math.sin(la) * math.cos(lb) * math.cos(dlon)
    bearing = math.degrees(math.atan2(y, x)) % 360.0
    return bearing, distance


def destination(a: Position, bearing_deg: float, distance_m: float) -> Position:
    """The position `distance_m` along the great circle from `a` on `bearing_deg`."""
    la = math.radians(a.lat_deg)
    lo = math.radians(a.lon_deg)
    theta = math.radians(bearing_deg)
    d = distance_m / EARTH_RADIUS_M
    lb = math.asin(math.sin(la) * math.cos(d) + math.cos(la) * math.sin(d) * math.cos(theta))
    lon = lo + math.atan2(
        math.sin(theta) * math.sin(d) * math.cos(la), math.cos(d) - math.sin(la) * math.sin(lb)
    )
    return Position(math.degrees(lb), _wrap_lon(math.degrees(lon)))


def horizon_nm(height_of_eye_m: float, height_of_object_m: float = 0.0) -> float:
    """How far an object of one height is seen from an eye at another, in nautical
    miles, by the geographic horizon (spec §11)."""
    eye = max(0.0, height_of_eye_m)
    obj = max(0.0, height_of_object_m)
    return HORIZON_NM_PER_ROOT_METRE * (math.sqrt(eye) + math.sqrt(obj))


# ---------------------------------------------------------------------------
# Words
# ---------------------------------------------------------------------------


def format_position(pos: Position, seconds: bool = False) -> str:
    """'49° 52' N, 6° 10' W': degrees and minutes as a log gives a position; with
    `seconds`, to the second (for the tests and the chart's features file)."""
    return f"{_dm(pos.lat_deg, 'N', 'S', seconds)}, {_dm(pos.lon_deg, 'E', 'W', seconds)}"


def _dm(value: float, positive: str, negative: str, seconds: bool) -> str:
    hemisphere = positive if value >= 0 else negative
    v = abs(value)
    if seconds:
        total = round(v * 3600.0)
        d, rest = divmod(total, 3600)
        m, s = divmod(rest, 60)
        return f"{d}° {m:02d}' {s:02d}\" {hemisphere}"
    total = round(v * 60.0)
    d, m = divmod(total, 60)
    return f"{d}° {m:02d}' {hemisphere}"


_POS_RE = re.compile(
    r"""^\s*(\d+(?:\.\d+)?)\s*[°\s]\s*(?:(\d+(?:\.\d+)?)\s*['′]?\s*)?([NS])\s*,?\s*
        (\d+(?:\.\d+)?)\s*[°\s]\s*(?:(\d+(?:\.\d+)?)\s*['′]?\s*)?([EW])\s*$""",
    re.X | re.I,
)


def parse_position(text: str) -> Position:
    """'49 52 N 6 10 W', '49°52'N, 6°10'W' or '49.87 N 6.17 W' as a position."""
    m = _POS_RE.match(text)
    if m is None:
        raise ValueError(f"not a position like 49 52 N 6 10 W: {text!r}")
    lat = float(m.group(1)) + float(m.group(2) or 0.0) / 60.0
    lon = float(m.group(4)) + float(m.group(5) or 0.0) / 60.0
    if m.group(3).upper() == "S":
        lat = -lat
    if m.group(6).upper() == "W":
        lon = -lon
    return Position(lat, lon)


def _count_words(n: int, singular: str, plural: str) -> str:
    small = {
        1: "one",
        2: "two",
        3: "three",
        4: "four",
        5: "five",
        6: "six",
        7: "seven",
        8: "eight",
        9: "nine",
        10: "ten",
        11: "eleven",
        12: "twelve",
    }
    if n == 1:
        return f"a {singular}"
    return f"{small.get(n, str(n))} {plural}"


def distance_words(distance_m: float) -> str:
    """A distance in the log's words: cables under a mile ('three cables'), miles to the
    half mile under two leagues ('four miles and a half'), leagues to the half league
    beyond ('five leagues')."""
    nm = distance_m / units.NAUTICAL_MILE
    if nm < 0.95:
        cables = max(1, round(nm * 10.0))
        if cables >= 10:
            return "a mile"
        return _count_words(cables, "cable", "cables")
    if nm < 6.0:
        halves = round(nm * 2.0)
        whole, half = divmod(halves, 2)
        words = _count_words(whole, "mile", "miles") if whole else ""
        if half:
            words = f"{words} and a half" if whole else "half a mile"
        return words
    halves = round(nm / 3.0 * 2.0)
    whole, half = divmod(halves, 2)
    words = _count_words(whole, "league", "leagues") if whole else ""
    if half:
        words = f"{words} and a half" if whole else "half a league"
    return words


def estimate_words(distance_m: float) -> str:
    """The lookout's estimate of a distance off (spec §12: the estimate the period's,
    to the nearest league or mile, not the truth): under a mile in cables, under two
    leagues to the nearest mile, beyond to the nearest league."""
    nm = distance_m / units.NAUTICAL_MILE
    if nm < 0.95:
        cables = max(1, round(nm * 10.0))
        return _count_words(cables, "cable", "cables") if cables < 10 else "a mile"
    if nm < 6.0:
        return _count_words(max(1, round(nm)), "mile", "miles")
    return _count_words(max(2, round(nm / 3.0)), "league", "leagues")
