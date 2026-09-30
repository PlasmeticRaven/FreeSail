"""Weather that comes from somewhere (spec M5 §2; the study `docs/design/WeatherSystems.md`
§1.3, §2(b), §5): pressure systems with fronts, seeded from a monthly climatology or
scripted by a scenario, and the glass, the sky, the weather and the visibility that a ship
reads from them.

**The model** (W §2b). A few systems in and near the box, each a centre with a velocity, a
central anomaly (a low negative, a high positive, hPa), a radius and, for a seeded low, a
life curve of deepening and filling. The pressure at a point is the month's background
plus the sum of the anomalies with a Gaussian radial profile. The geostrophic wind is the
gradient turned ninety degrees (`GEOSTROPHIC_MS_PER_HPA_PER_100KM`); the surface wind is
that turned `SURFACE_TURN_DEG` toward low pressure and scaled by `SURFACE_SCALE`, each
system's part capped in strong curvature by the gradient-wind rule. Two fronts hinge at
each low, a warm front ahead and a cold front behind, each a bearing from the centre, a
length and a width; they turn cyclonically as the low lives, the cold front faster, until
it catches the warm front and the low occludes. A point's **sector** (ahead of the warm
front, the warm sector, behind the cold front, under a high, or open sea between systems)
and its distance to the nearest front fix the sky, the weather, the visibility and the air
mass by the table of W §1.3 (`conditions_at`), and crossing a front adds its veer to the
surface wind (`surface_wind_at`).

**Seeding** (W §5). `data/weather/climatology.yaml` gives, per month, the rate of lows, the
distribution of their tracks, speeds, depths and radii, the probability of a high and its
bearing, and the direction shares of W §1.1 as the check. A system's parameters are drawn
from the month's table from one stream (`rng` stream `weather`) when the scenario starts
and whenever a system leaves the box or its life ends; everything after a draw is
arithmetic, so a day replays tick for tick (truth 55). Nothing is drawn while a scripted
system is present.

**The scenario's systems** (W §5, spec §2). A scripted system is a name, a kind, a radius,
waypoints of position (km east and north of the world's origin, the ship's start),
central pressure and time, and for a low its fronts' initial bearings; it follows its
waypoints exactly as `WeatherScript.at` interpolates the pinned wind, holding the first
before the first and the last after the last.

**What the captain sees.** Nothing here names a front, a centre, an isobar or a
hectopascal in any line a player reads (truth 57): the readings say the glass in inches,
the sky in Beaufort's words with Luce's signs, the weather and the visibility in the
lookout's terms; the veer at a front is a veer of the wind like any other, and the
scenario author and the director alone see the systems by name (W §3).

The sea breeze and coastal fog (W §1.4) read the coast through the World's hook
(`Weather.coast`, package 32): the chart's distance and bearing to the nearest shore. With
no chart there is no coast, and both are inert, as they were before the chart.
"""

from __future__ import annotations

import bisect
import hashlib
import math
import random
from collections import deque
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import yaml

from freesail import units

# Seconds since a fixed naive epoch. `datetime.timestamp()` is not used: on Windows it
# raises OSError for any date before 1970, which is every date in this game (found at
# gate 5a, 2026-09-30, by the owner: 35 tests failing on 1805's scenario). The epoch is
# 1970 so that the values equal the Unix seconds the build machine (UTC) produced, and
# the day's digest and every seeded noise key stand unchanged.
_EPOCH = datetime(1970, 1, 1)


def _seconds(when: datetime) -> float:
    return (when - _EPOCH).total_seconds()


__all__ = [
    "AIR_MASSES",
    "BACKGROUND_HPA",
    "Climatology",
    "Conditions",
    "Glass",
    "HPA_PER_INCH",
    "SKY_WORDS",
    "SURFACE_SCALE",
    "SURFACE_TURN_DEG",
    "System",
    "TENDENCY_WORDS",
    "VISIBILITY_NM",
    "VISIBILITY_WORDS",
    "WEATHER_WORDS",
    "Weather",
    "WeatherError",
    "inches",
    "load_climatology",
    "tendency_words",
]


class WeatherError(ValueError):
    """A scenario's systems that cannot be followed, in words that name the system."""


# ---------------------------------------------------------------------------
# Constants, each with its source (the study's "verified / not verified" list is binding:
# a number from an unverified figure says so here and in docs/dev/TuningNotes.md)
# ---------------------------------------------------------------------------

# The month's background pressure when the climatology gives none (W §2b: "a background,
# say 1015 hPa, seasonal"; the study's figure, a round number and not a table's).
BACKGROUND_HPA = 1015.0

# The surface wind over the sea blows across the isobars toward low pressure at 10 to 20
# degrees and at about two thirds of the geostrophic speed (W §1.3, source S8, verified
# as the textbook statement); the spec fixes the middle of each.
SURFACE_TURN_DEG = 15.0
SURFACE_SCALE = 0.7

# At 50 N a gradient of 1 hPa per 100 km gives a geostrophic wind of 7.2 m/s (W §1.3;
# checked here: 100 Pa over 100 km at an air density of 1.25 kg/m^3 and a Coriolis
# parameter of 1.117e-4 /s at 50 N gives 7.16 m/s).
GEOSTROPHIC_MS_PER_HPA_PER_100KM = 7.2
# The Coriolis parameter at 50 N, for the gradient-wind cap (2 x 7.292e-5 x sin 50).
CORIOLIS_50N = 1.117e-4

# The veer at each front, W §1.3 (source S7, verified): at the warm front the wind veers
# "south to south-west", two points; at the cold front it "veers sharply", "west to
# north-west", four points. Ahead of the warm front the wind backs by the warm front's
# veer over WARM_FRONT_APPROACH_KM as the front nears; behind the cold front its veer
# fades over COLD_FRONT_VEER_FADE_KM into the systems' own turning. Close ahead of the
# cold front "the wind backs a little and freshens" (S7): a point, within the front's band.
WARM_FRONT_VEER_DEG = 22.5
COLD_FRONT_VEER_DEG = 45.0
COLD_FRONT_PRE_BACK_DEG = 11.25

# The fronts' geometry. The study gives the sequence and not the distances, so these are
# judgements from the Norwegian model's proportions (S7; Bjerknes 1919): the warm front's
# cloud and rain run a few hundred kilometres ahead of the surface front up its slope; the
# cold front is a narrow band with showers and clearing behind it; a front runs about a
# thousand kilometres from the centre. Recorded as judgements in docs/dev/TuningNotes.md.
FRONT_LENGTH_KM = 1000.0
WARM_FRONT_APPROACH_KM = 300.0  # the backing, the falling glass, the thickening sky
WARM_FRONT_RAIN_KM = 200.0  # rain sets in and grows steady
WARM_FRONT_GLOOM_KM = 120.0  # nimbostratus: dark and gloomy, visibility down in the rain
COLD_FRONT_BAND_KM = 60.0  # the squally band about the cold front
COLD_FRONT_SHOWERS_KM = 400.0  # the cold unstable air behind: showers, clearing between
COLD_FRONT_VEER_FADE_KM = 400.0
# The fronts turn cyclonically about the centre (bearings falling), the cold front faster
# than the warm, so that the warm sector narrows and the low occludes when the cold front
# catches the warm (S7). Judgement: a wave with a warm sector of a hundred degrees occludes
# in about a day, the life cycle's proportion.
WARM_FRONT_TURN_DEG_PER_H = 2.0
COLD_FRONT_TURN_DEG_PER_H = 6.0

# The box (W §1: about a hundred miles square at 48 to 51 N, 3 to 8 W) and the reach a
# system is followed over: a seeded low is born this far up its track from its closest
# point and leaves when it is this far past it (judgement: a low of 500 km radius is felt
# at twice its radius).
BOX_HALF_KM = 250.0
SYSTEM_REACH_KM = 900.0
# A high sits nearer than this to be "under a high" (in radii; judgement).
UNDER_HIGH_RADII = 1.0

# The glass. One inch of mercury is 33.86 hPa (W §3; the physical constant, 33.8639).
HPA_PER_INCH = 33.86
# The ship's own reading noise: a marine glass pumps in a seaway by "a hundredth or two"
# (W §3); half a hundredth here for the reading itself, and the seaway's pumping (package
# 31, `physics.motion.Motion.pumping`) scales it up to GLASS_PUMP_MAX_IN, the two
# hundredths. Deterministic from the seed and the minute; drawn from no stream.
GLASS_NOISE_IN = 0.005
GLASS_PUMP_MAX_IN = 0.02
# The tendency's words. "A fall of a tenth in three hours means much wind" is common
# sailing-school teaching whose period source the study could not find (W §1.7,
# unverified); it is the threshold of "falling fast" here and says so. Steady within
# three hundredths in three hours (judgement).
TENDENCY_FAST_IN_PER_3H = 0.10
TENDENCY_STEADY_IN_PER_3H = 0.03
TENDENCY_SPAN_H = 3.0
TENDENCY_MIN_RECORD_H = 1.0
GLASS_RECORD_STEP_S = 60

# The visibility in the lookout's terms and the miles each means (judgement; the number
# is what 5b's sighting reads). The horizon is the masthead's, about twelve miles.
VISIBILITY_NM: dict[str, float] = {
    "the horizon": 12.0,
    "a few miles": 4.0,
    "a mile": 1.0,
    "a cable": 0.1,
}
VISIBILITY_WORDS: tuple[str, ...] = tuple(VISIBILITY_NM)

# Beaufort's weather letters as words (W §1.6, source S19, verified): b blue sky, c
# detached clouds, o overcast, g dark gloomy, u ugly or threatening, m misty or hazy, and
# "thick" for the thick weather of fog or heavy rain; and the weather: r rain, d drizzle,
# p passing showers, q squally, t thunder, f fog, with "fine" for none.
SKY_WORDS: tuple[str, ...] = (
    "clear",
    "detached clouds",
    "overcast",
    "dark and gloomy",
    "threatening",
    "hazy",
    "thick",
)
WEATHER_WORDS: tuple[str, ...] = (
    "fine",
    "rain",
    "drizzle",
    "passing showers",
    "squally",
    "thunder",
    "fog",
)
# Luce's signs for the log's colour (Luce 1884, "The Weather, the Barometer, Laws of
# Storms", quoting FitzRoy: "a high dawn, wind"; "hard edged, oily-looking clouds, wind";
# "small inky clouds foretell rain"; "a light scud, driving across heavy clouds, wind and
# rain"; the first signs of change "small, curly, streaked, or spotty clouds").
SKY_SIGNS: dict[str, str] = {
    "high dawn": "a high dawn",
    "hard edged": "hard-edged and oily-looking",
    "inky": "small inky clouds",
    "scud": "a light scud driving across",
    "streaked": "streaked and spotty clouds high up",
}
# The sky's and the weather's noise holds for this many hours before it is drawn afresh
# (judgement: a watch; the words change with the sector and the front's distance sooner).
SKY_NOISE_HOURS = 4
# The log's line when the weather changes, by the weather it becomes, or by (was, now).
WEATHER_LINES: dict[Any, str] = {
    "rain": "Rain set in.",
    "drizzle": "Drizzle.",
    "passing showers": "Passing showers.",
    "squally": "Squally.",
    "thunder": "Thunder.",
    "fog": "Fog came down.",
    "fine": "The weather cleared.",
    ("rain", "fine"): "The rain ceased.",
    ("drizzle", "fine"): "The drizzle ceased.",
    ("passing showers", "fine"): "The showers passed.",
    ("fog", "fine"): "The fog lifted.",
    ("rain", "drizzle"): "The rain turned to drizzle.",
}
TENDENCY_WORDS: tuple[str, ...] = ("steady", "rising", "falling", "rising fast", "falling fast")
AIR_MASSES: tuple[str, ...] = ("warm", "neutral", "unstable")
SECTORS: tuple[str, ...] = ("ahead", "warm", "behind", "high", "open")

# The wind under which a day has no prevailing quarter, for the climatology's count
# (judgement: light airs).
CALM_KN = 1.0

# The sea breeze (W §1.4; Simpson 1994 [S11], the study's summary: "a summer, daylight,
# fine-weather wind of some 10 knots at most, onshore, strongest in mid-afternoon, felt a
# few miles to sea and dying at dusk"; package 32). The study gives the ten knots and the
# shape in words; the numbers below that put the words on the clock are judgements, said
# so in docs/dev/TuningNotes.md: the season May to September, the onset at ten in the
# forenoon and the end at eight in the evening (a June dusk), the peak between them at
# three; full strength within five kilometres of the shore and gone at fifteen ("a few
# miles"); free under a gradient wind of five knots and killed by one of twenty.
SEA_BREEZE_MAX_KN = 10.0
SEA_BREEZE_MONTHS = frozenset({5, 6, 7, 8, 9})
SEA_BREEZE_ONSET_H = 10.0
SEA_BREEZE_END_H = 20.0
SEA_BREEZE_FULL_KM = 5.0
SEA_BREEZE_REACH_KM = 15.0
SEA_BREEZE_GRADIENT_FREE_KN = 5.0
SEA_BREEZE_GRADIENT_CAP_KN = 20.0

# Coastal fog (W §1.4; the ship observations of [S10]: fog west of the United Kingdom in
# nearly 4% of observations in June to August and under 2% in December to February;
# advection fog near the coasts in a stable warm sector or under a high with a slack
# gradient, lifted by a fresh wind). The monthly chance is [S10]'s two figures drawn
# through the year (the months between are the study's shape, unverified in W, and a
# judgement here); the factor is the judgement that the observations' fog falls in the
# hours that meet the conditions, about a sixth of all hours, so the conditional chance
# in a sky block is six times the monthly share; the reach and the wind cap are
# judgements from "near the coasts" and "a fresh wind lifts it". All in TuningNotes.
FOG_CHANCE_BY_MONTH: tuple[float, ...] = (
    0.015,
    0.015,
    0.02,
    0.03,
    0.035,
    0.04,
    0.04,
    0.04,
    0.03,
    0.025,
    0.02,
    0.015,
)
FOG_CONDITIONAL_FACTOR = 6.0
FOG_COAST_KM = 30.0
FOG_MAX_WIND_KN = 12.0


def inches(hpa: float) -> float:
    return hpa / HPA_PER_INCH


def _bearing_deg(dx: float, dy: float) -> float:
    return math.degrees(math.atan2(dx, dy)) % 360.0


def _noise(seed: int, key: str) -> float:
    """A number in [0, 1) that is a function of the seed and the key alone: the little
    seeded noise of the sky and the glass, drawn from no stream (W §5: nothing random
    but the systems' draws)."""
    h = hashlib.blake2b(f"{seed}:{key}".encode(), digest_size=8).digest()
    return int.from_bytes(h, "big") / 2**64


def tendency_words(change_in: float | None) -> str | None:
    """The period's words for a change of the glass over three hours: steady, rising,
    falling, rising fast, falling fast."""
    if change_in is None:
        return None
    if abs(change_in) < TENDENCY_STEADY_IN_PER_3H:
        return "steady"
    fast = abs(change_in) >= TENDENCY_FAST_IN_PER_3H
    word = "rising" if change_in > 0 else "falling"
    return f"{word} fast" if fast else word


# ---------------------------------------------------------------------------
# The climatology
# ---------------------------------------------------------------------------

CLIMATOLOGY_PATH = Path(__file__).resolve().parents[2] / "data" / "weather" / "climatology.yaml"


@dataclass(frozen=True)
class MonthTable:
    """One month's row of `data/weather/climatology.yaml`, as the seeding reads it."""

    month: int
    name: str
    background_hpa: float
    gradient: tuple[
        float, float
    ]  # the mean gradient: hPa per 100 km, and the bearing toward high pressure
    lows_per_month: float
    track_bearing_deg: tuple[float, float]  # mean, spread (the direction a low moves)
    closest_approach_km: tuple[float, float]  # mean, spread; positive north of the box
    speed_kn: tuple[float, float]  # min, max
    central_hpa: tuple[float, float, float]  # mean, spread, floor
    radius_km: tuple[float, float]  # min, max
    life_h: tuple[float, float]  # min, max
    high_probability: float
    high_bearing_deg: tuple[float, float]  # mean, spread (from the box to the centre)
    high_distance_km: tuple[float, float]  # min, max
    high_anomaly_hpa: tuple[float, float]  # min, max
    high_radius_km: tuple[float, float]  # min, max
    high_life_h: tuple[float, float]  # min, max
    check: dict[str, float]  # the direction shares to check against, per cent


@dataclass(frozen=True)
class Climatology:
    months: dict[int, MonthTable]
    provisional: bool
    source: str

    def month(self, m: int) -> MonthTable:
        return self.months[m]


def _pair(d: Mapping[str, Any], *keys: str) -> tuple[float, ...]:
    return tuple(float(d[k]) for k in keys)


def load_climatology(path: str | Path = CLIMATOLOGY_PATH) -> Climatology:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    months: dict[int, MonthTable] = {}
    for m, row in raw["months"].items():
        m = int(m)
        high = row["high"]
        months[m] = MonthTable(
            month=m,
            name=str(row["name"]),
            background_hpa=float(row["background_hpa"]),
            gradient=_pair(row["gradient"], "hpa_per_100km", "high_toward_deg"),
            lows_per_month=float(row["lows_per_month"]),
            track_bearing_deg=_pair(row["track_bearing_deg"], "mean", "spread"),
            closest_approach_km=_pair(row["closest_approach_km"], "mean", "spread"),
            speed_kn=_pair(row["speed_kn"], "min", "max"),
            central_hpa=_pair(row["central_hpa"], "mean", "spread", "floor"),
            radius_km=_pair(row["radius_km"], "min", "max"),
            life_h=_pair(row["life_h"], "min", "max"),
            high_probability=float(high["probability"]),
            high_bearing_deg=_pair(high["bearing_deg"], "mean", "spread"),
            high_distance_km=_pair(high["distance_km"], "min", "max"),
            high_anomaly_hpa=_pair(high["anomaly_hpa"], "min", "max"),
            high_radius_km=_pair(high["radius_km"], "min", "max"),
            high_life_h=_pair(high["life_h"], "min", "max"),
            check={k: float(v) for k, v in row["check"].items()},
        )
    if sorted(months) != list(range(1, 13)):
        raise WeatherError(f"{path}: the climatology needs all twelve months.")
    return Climatology(
        months=months,
        provisional=bool(raw.get("provisional", True)),
        source=str(raw.get("source", "")),
    )


# ---------------------------------------------------------------------------
# Systems
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TrackPoint:
    """A scripted system at one moment: its centre (km east and north of the origin) and
    its central pressure (hPa)."""

    at: datetime
    x_km: float
    y_km: float
    hpa: float

    def to_dict(self) -> dict[str, Any]:
        return {"at": self.at.isoformat(), "x_km": self.x_km, "y_km": self.y_km, "hpa": self.hpa}

    @classmethod
    def from_dict(cls, d: Mapping[str, Any], name: str) -> TrackPoint:
        at = d.get("at")
        if isinstance(at, str):
            at = datetime.fromisoformat(at)
        if not isinstance(at, datetime):
            raise WeatherError(f"System '{name}': a waypoint needs a time ('at'), not {at!r}.")
        try:
            return cls(at, float(d["x_km"]), float(d["y_km"]), float(d["hpa"]))
        except (KeyError, TypeError, ValueError):
            raise WeatherError(
                f"System '{name}': the waypoint at {at.isoformat()} needs 'x_km', 'y_km' and "
                f"'hpa' as numbers."
            ) from None


@dataclass
class System:
    """One pressure system: a centre with a velocity, an anomaly, a radius and, for a low,
    two fronts. Seeded systems move by their velocity and live by their life curve;
    scripted ones follow their track and hold its ends."""

    name: str
    kind: str  # "low" or "high"
    x_km: float
    y_km: float
    vx_kmh: float
    vy_kmh: float
    anomaly_hpa: float  # now
    radius_km: float
    born: datetime
    x0_km: float = 0.0  # where it was born: a seeded system's position is integrated
    y0_km: float = 0.0  # from here, so that the cadence of the calls cannot move it
    life_h: float | None = None  # a seeded system's life; None for a scripted one
    age0_h: float = 0.0  # a seeded low is born already part-grown
    peak_hpa: float = 0.0  # the deepest anomaly of the life curve
    warm_deg: float = 135.0  # the fronts' bearings from the centre at birth (a low)
    cold_deg: float = 225.0
    occluded_at: datetime | None = None
    track: list[TrackPoint] = field(default_factory=list)
    track_times: list[datetime] = field(default_factory=list)  # the track's times, for bisect
    scripted: bool = False
    gone: bool = False

    # -- the fronts ---------------------------------------------------------

    def age_h(self, when: datetime) -> float:
        return self.age0_h + (when - self.born).total_seconds() / 3600.0

    def fronts_at(self, when: datetime) -> tuple[float, float, bool]:
        """(warm bearing, cold bearing, occluded) at `when`, degrees from the centre."""
        if self.kind != "low":
            return 0.0, 0.0, False
        turned = (when - self.born).total_seconds() / 3600.0
        warm = (self.warm_deg - WARM_FRONT_TURN_DEG_PER_H * turned) % 360.0
        cold = (self.cold_deg - COLD_FRONT_TURN_DEG_PER_H * turned) % 360.0
        width0 = (self.cold_deg - self.warm_deg) % 360.0
        closing = (COLD_FRONT_TURN_DEG_PER_H - WARM_FRONT_TURN_DEG_PER_H) * turned
        occluded = closing >= width0
        if occluded:
            cold = warm
        return warm, cold, occluded

    # -- the field ----------------------------------------------------------

    def anomaly_and_gradient(self, x_km: float, y_km: float) -> tuple[float, float, float, float]:
        """(anomaly here, dp/dx, dp/dy in hPa/km, distance in radii) of this system at a
        point: a Gaussian bell of the centre's anomaly with the radius as its scale."""
        dx, dy = x_km - self.x_km, y_km - self.y_km
        r = math.hypot(dx, dy)
        u = r / self.radius_km
        bell = math.exp(-0.5 * u * u)
        p = self.anomaly_hpa * bell
        if r == 0.0:
            return p, 0.0, 0.0, 0.0
        dpdr = -self.anomaly_hpa * u * bell / self.radius_km
        return p, dpdr * dx / r, dpdr * dy / r, u

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "name": self.name,
            "kind": self.kind,
            "radius_km": self.radius_km,
        }
        if self.kind == "low":
            d["fronts"] = {"warm_deg": self.warm_deg, "cold_deg": self.cold_deg}
        if self.scripted:
            d["track"] = [p.to_dict() for p in self.track]
        return d


def _system_from_dict(d: Mapping[str, Any], start: datetime) -> System:
    name = str(d.get("name") or "a system")
    kind = str(d.get("kind") or "low").lower()
    if kind not in ("low", "high"):
        raise WeatherError(f"System '{name}': the kind is 'low' or 'high', not '{kind}'.")
    try:
        radius = float(d.get("radius_km", 500.0))
    except (TypeError, ValueError):
        raise WeatherError(f"System '{name}': 'radius_km' is a number.") from None
    if radius <= 0:
        raise WeatherError(f"System '{name}': a radius of {radius:g} km is no radius.")
    points = [TrackPoint.from_dict(p, name) for p in d.get("track") or []]
    if not points:
        raise WeatherError(f"System '{name}': a scripted system needs a track of waypoints.")
    for a, b in zip(points, points[1:], strict=False):
        if b.at <= a.at:
            raise WeatherError(
                f"System '{name}': the waypoint at {b.at.isoformat()} is not after the one at "
                f"{a.at.isoformat()}; a track runs forward in time."
            )
    fronts = d.get("fronts") or {}
    try:
        warm = float(fronts.get("warm_deg", 135.0)) % 360.0
        cold = float(fronts.get("cold_deg", 225.0)) % 360.0
    except (TypeError, ValueError, AttributeError):
        raise WeatherError(f"System '{name}': 'fronts' is warm_deg and cold_deg.") from None
    first = points[0]
    return System(
        name=name,
        kind=kind,
        x_km=first.x_km,
        y_km=first.y_km,
        vx_kmh=0.0,
        vy_kmh=0.0,
        anomaly_hpa=0.0,  # set by the first advance, from the track and the background
        radius_km=radius,
        born=min(first.at, start),
        warm_deg=warm,
        cold_deg=cold,
        track=points,
        track_times=[p.at for p in points],
        scripted=True,
    )


def _track_at(
    points: list[TrackPoint], times: list[datetime], when: datetime
) -> tuple[float, float, float]:
    """(x, y, hpa) along a track at `when`, linear between waypoints, held at the ends."""
    i = bisect.bisect_right(times, when)
    if i == 0:
        p = points[0]
        return p.x_km, p.y_km, p.hpa
    if i == len(points):
        p = points[-1]
        return p.x_km, p.y_km, p.hpa
    a, b = points[i - 1], points[i]
    f = (when - a.at).total_seconds() / (b.at - a.at).total_seconds()
    return (
        a.x_km + f * (b.x_km - a.x_km),
        a.y_km + f * (b.y_km - a.y_km),
        a.hpa + f * (b.hpa - a.hpa),
    )


# ---------------------------------------------------------------------------
# What a point sees
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Sector:
    """A point's place among the systems: which sector, the nearest low's fronts'
    distances (km, ahead of the warm front and behind the cold front, or none), the
    nearest high in radii."""

    sector: str  # "ahead", "warm", "behind", "high", "open"
    air_mass: str  # "warm", "neutral", "unstable"
    to_warm_km: float | None = None  # distance to the warm front (from either side)
    to_cold_km: float | None = None
    low: System | None = None
    high_radii: float | None = None
    veer_deg: float = 0.0  # the fronts' turning of the surface wind here


@dataclass(frozen=True)
class Conditions:
    """The sky and the weather at a point, in the words the readings give."""

    sector: str
    air_mass: str
    sky: str
    signs: str  # Luce's, or ""
    weather: str
    visibility: str
    pressure_hpa: float

    @property
    def visibility_nm(self) -> float:
        return VISIBILITY_NM[self.visibility]


def _to_segment(dx: float, dy: float, bearing_deg: float, length_km: float) -> tuple[float, float]:
    """(distance from a point to a front's segment, the point's along-front coordinate):
    the front runs from the hinge (the origin of dx, dy) along `bearing_deg` for
    `length_km`."""
    b = math.radians(bearing_deg)
    tx, ty = math.sin(b), math.cos(b)
    along = dx * tx + dy * ty
    if along <= 0.0:
        return math.hypot(dx, dy), along
    if along >= length_km:
        return math.hypot(dx - length_km * tx, dy - length_km * ty), along
    return abs(dx * ty - dy * tx), along


# ---------------------------------------------------------------------------
# The ship's glass
# ---------------------------------------------------------------------------


class Glass:
    """The ship's own glass and its record: the reading in inches, with the ship's noise,
    kept once a minute for three hours so that the tendency is the ship's account and not
    the model's (W §2b: "the tendency is its change over the last three hours, kept by the
    ship's own record"). A ship with no glass has no tendency."""

    def __init__(self, seed: int, window_h: float = TENDENCY_SPAN_H):
        self._seed = seed
        self._window_s = int(window_h * 3600)
        self._record: deque[tuple[datetime, float]] = deque()
        self.reading_in: float | None = None
        self.read_at: datetime | None = None
        self._last_watch_reading: float | None = None

    def read(self, pressure_hpa: float, when: datetime, pumping: float = 1.0) -> float:
        """Read the glass now: the model's pressure in inches plus the ship's noise, kept
        in the record. `pumping` is the seaway's factor on the noise (spec M5 §4,
        `physics.motion.Motion.pumping`): the mercury pumps by a hundredth or two in a
        seaway (W §3), never more than GLASS_PUMP_MAX_IN."""
        minute = int(_seconds(when) // 60)
        amplitude = min(GLASS_NOISE_IN * max(pumping, 1.0), GLASS_PUMP_MAX_IN)
        noise = (2.0 * _noise(self._seed, f"glass:{minute}") - 1.0) * amplitude
        value = round(inches(pressure_hpa) + noise, 2)
        self.reading_in = value
        self.read_at = when
        self._record.append((when, value))
        while self._record and (when - self._record[0][0]).total_seconds() > self._window_s:
            self._record.popleft()
        return value

    def change_over(self, hours: float) -> float | None:
        """The change in inches over the last `hours`, or None before the record is that
        old (the oldest entry inside the span is read; a record younger than an hour is not
        read at all)."""
        if not self._record or self.read_at is None:
            return None
        span = timedelta(hours=hours)
        oldest = self._record[0]
        if (self.read_at - oldest[0]) < timedelta(hours=min(hours, TENDENCY_MIN_RECORD_H)):
            return None
        target = self.read_at - span
        # the first entry at or after the target
        for at, value in self._record:
            if at >= target:
                return round(self.reading_in - value, 2)  # type: ignore[operator]
        return None

    def tendency(self) -> dict[str, Any] | None:
        """{'words', 'three_hours_in', 'one_hour_in'}: the words from the three hours'
        change when the record has it, else from the hour's change scaled to three; None
        before an hour of record."""
        three = self.change_over(TENDENCY_SPAN_H)
        one = self.change_over(1.0)
        if one is None:
            return None
        if three is not None and (self.read_at - self._record[0][0]) >= timedelta(
            hours=TENDENCY_SPAN_H
        ):
            words = tendency_words(three)
        else:
            words = tendency_words(one * TENDENCY_SPAN_H)
        return {"words": words, "three_hours_in": three, "one_hour_in": one}

    def mark_watch(self) -> float | None:
        """At a watch's change: the change since the last change of the watch (None the
        first time), and the reading kept for the next."""
        change = None
        if self._last_watch_reading is not None and self.reading_in is not None:
            change = round(self.reading_in - self._last_watch_reading, 2)
        self._last_watch_reading = self.reading_in
        return change


# ---------------------------------------------------------------------------
# The weather
# ---------------------------------------------------------------------------


class Weather:
    """The systems in and near the box, seeded or scripted, and the field they make.

    `advance(when)` moves the systems (and draws replacements for seeded ones that left or
    died); `pressure_at`, `surface_wind_at`, `sector_at` and `conditions_at` read the field
    at a point. The World calls `advance` and `surface_wind_at` every tick and
    `conditions_at` once a minute.
    """

    LOW_SLOTS = 3

    def __init__(
        self,
        start: datetime,
        stream: random.Random | None,
        seed: int = 0,
        systems: Iterable[Mapping[str, Any]] = (),
        climatology: Climatology | None = None,
        background_hpa: float | None = None,
        gradient: tuple[float, float] | None = None,
    ):
        self.start = start
        self.now = start
        self.seed = int(seed)
        self._stream = stream
        self.climatology = climatology
        self.systems: list[System] = [_system_from_dict(d, start) for d in systems]
        self.scripted = bool(self.systems)
        self.draws = 0  # how many systems have been drawn (the test of "nothing random")
        self.lows_drawn = 0
        # the seeded slots: when each slot's next low is born, and the high's
        self._low_births: list[datetime] = []
        self._high_birth: datetime | None = None
        self._high: System | None = None
        self._serial = 0
        if background_hpa is not None:
            self._background = float(background_hpa)
        elif climatology is not None:
            self._background = climatology.month(start.month).background_hpa
        else:
            self._background = BACKGROUND_HPA
        # The mean gradient the box sits on (the Azores high to the south, the Icelandic
        # low to the north; W §1.1's westerly on a third of days is this flow), as hPa per
        # km east and north; the climatology's by month, a scenario's if it gives one.
        if gradient is None and climatology is not None and not self.scripted:
            gradient = climatology.month(start.month).gradient
        self._gradient = (0.0, 0.0)
        if gradient is not None:
            strength, toward = gradient
            b = math.radians(toward)
            self._gradient = (strength / 100.0 * math.sin(b), strength / 100.0 * math.cos(b))
        if not self.scripted and climatology is not None:
            if stream is None:
                raise WeatherError("Seeding from the climatology needs the world's weather stream.")
            self._seed_at_start()
        self.advance(start)

    # -- the systems' names, for the director and the scenario author only ----

    @property
    def background_hpa(self) -> float:
        return self._background

    def to_list(self) -> list[dict[str, Any]]:
        """The scripted systems as the scenario holds them."""
        return [s.to_dict() for s in self.systems if s.scripted]

    def describe(self) -> list[str]:
        """The systems in words, for the driver's load line (the author's view: names,
        kinds, where they are now; never a log line)."""
        out = []
        for s in self.systems:
            if s.gone:
                continue
            centre = _bearing_deg(s.x_km, s.y_km)
            out.append(
                f"{s.name} ({s.kind}, {self._background + s.anomaly_hpa:.0f} hPa at the centre, "
                f"radius {s.radius_km:.0f} km), {math.hypot(s.x_km, s.y_km):.0f} km to the "
                f"{units.point_name(units.deg_to_rad(centre))} of the start"
            )
        return out

    # -- seeding ------------------------------------------------------------

    def _table(self, when: datetime) -> MonthTable:
        assert self.climatology is not None
        return self.climatology.month(when.month)

    def _seed_at_start(self) -> None:
        """Populate the box at the scenario's start: each low slot gets a low somewhere
        along its transit (so that the day does not open on an empty sky), the high by its
        month's probability."""
        t = self._table(self.start)
        r = self._stream
        assert r is not None
        for _ in range(self.LOW_SLOTS):
            low = self._draw_low(self.start, t)
            # already part-way through its transit: move it along by a share of its reach
            share = r.uniform(0.0, 1.0)
            hours = share * 2.0 * SYSTEM_REACH_KM / math.hypot(low.vx_kmh, low.vy_kmh)
            low.born = self.start - timedelta(hours=hours)
            if low.life_h is not None and low.age_h(self.start) >= low.life_h:
                low.gone = True
                self._low_births.append(self.start + self._low_gap(t))
                continue
            self.systems.append(low)
        if r.random() < t.high_probability:
            self._high = self._draw_high(self.start, t)
            self._high.age0_h = r.uniform(0.0, 0.6) * (self._high.life_h or 1.0)
            self.systems.append(self._high)
        else:
            self._high_birth = self.start + self._high_gap(t)

    def _low_gap(self, t: MonthTable) -> timedelta:
        """The gap before a slot's next low is born: exponential, with the mean set so that
        the slots together deliver the month's rate (the mean transit of a low across its
        reach is taken off the cycle)."""
        r = self._stream
        assert r is not None
        cycle_h = self.LOW_SLOTS * 30.0 * 24.0 / max(t.lows_per_month, 0.1)
        speed_kmh = 0.5 * (t.speed_kn[0] + t.speed_kn[1]) * 1.852
        transit_h = 2.0 * SYSTEM_REACH_KM / speed_kmh
        mean_gap_h = max(cycle_h - transit_h, 1.0)
        return timedelta(hours=r.expovariate(1.0 / mean_gap_h))

    def _high_gap(self, t: MonthTable) -> timedelta:
        r = self._stream
        assert r is not None
        p = min(max(t.high_probability, 0.02), 0.98)
        mean_life = 0.5 * (t.high_life_h[0] + t.high_life_h[1])
        mean_gap_h = mean_life * (1.0 - p) / p
        return timedelta(hours=r.expovariate(1.0 / max(mean_gap_h, 1.0)))

    def _draw_low(self, when: datetime, t: MonthTable) -> System:
        """A low from the month's table: its track (a bearing and a closest approach to
        the box's centre), its speed, its depth, its radius, its life and its fronts; born
        SYSTEM_REACH_KM up its track from the closest point."""
        r = self._stream
        assert r is not None
        self.draws += 1
        self.lows_drawn += 1
        self._serial += 1
        bearing = r.gauss(*t.track_bearing_deg) % 360.0
        closest = r.gauss(*t.closest_approach_km)
        speed_kmh = r.uniform(*t.speed_kn) * 1.852
        mean, spread, floor = t.central_hpa
        deepest = min(r.gauss(mean, spread), t.background_hpa - 4.0)
        deepest = max(deepest, floor) - t.background_hpa  # the anomaly, negative
        radius = r.uniform(*t.radius_km)
        life = r.uniform(*t.life_h)
        age0 = r.uniform(0.15, 0.4) * life
        b = math.radians(bearing)
        tx, ty = math.sin(b), math.cos(b)
        nx, ny = -ty, tx  # the left-hand normal: north of an eastward track
        x0 = closest * nx - SYSTEM_REACH_KM * tx
        y0 = closest * ny - SYSTEM_REACH_KM * ty
        warm = (bearing + 45.0 + r.gauss(0.0, 12.0)) % 360.0
        cold = (bearing + 135.0 + r.gauss(0.0, 15.0)) % 360.0
        return System(
            name=f"low {self._serial}",
            kind="low",
            x_km=x0,
            y_km=y0,
            x0_km=x0,
            y0_km=y0,
            vx_kmh=speed_kmh * tx,
            vy_kmh=speed_kmh * ty,
            anomaly_hpa=0.0,
            radius_km=radius,
            born=when,
            life_h=life,
            age0_h=age0,
            peak_hpa=deepest,
            warm_deg=warm,
            cold_deg=cold,
        )

    def _draw_high(self, when: datetime, t: MonthTable) -> System:
        r = self._stream
        assert r is not None
        self.draws += 1
        self._serial += 1
        bearing = math.radians(r.gauss(*t.high_bearing_deg))
        distance = r.uniform(*t.high_distance_km)
        drift_kmh = r.uniform(2.0, 8.0) * 1.852
        drift = math.radians(r.gauss(t.track_bearing_deg[0], 40.0))
        x0, y0 = distance * math.sin(bearing), distance * math.cos(bearing)
        return System(
            name=f"high {self._serial}",
            kind="high",
            x_km=x0,
            y_km=y0,
            x0_km=x0,
            y0_km=y0,
            vx_kmh=drift_kmh * math.sin(drift),
            vy_kmh=drift_kmh * math.cos(drift),
            anomaly_hpa=0.0,
            radius_km=r.uniform(*t.high_radius_km),
            born=when,
            life_h=r.uniform(*t.high_life_h),
            peak_hpa=r.uniform(*t.high_anomaly_hpa),
        )

    # -- time ---------------------------------------------------------------

    def advance(self, when: datetime) -> None:
        """Move the systems to `when`. Scripted systems read their tracks; seeded ones move
        by their velocity and live by their curve, and a seeded one that has left the box
        or died is dropped and, when its slot's gap has passed, replaced by a draw."""
        self.now = when
        for s in self.systems:
            if s.scripted:
                x, y, hpa = _track_at(s.track, s.track_times, when)
                s.x_km, s.y_km = x, y
                s.anomaly_hpa = hpa - self._background
                continue
        if self.scripted or self.climatology is None:
            return
        self._advance_seeded(when)

    def _advance_seeded(self, when: datetime) -> None:
        t = self._table(when)
        live: list[System] = []
        freed = 0
        for s in self.systems:
            age = s.age_h(when)
            assert s.life_h is not None
            s.anomaly_hpa = s.peak_hpa * math.sin(math.pi * min(max(age / s.life_h, 0.0), 1.0))
            hours = (when - s.born).total_seconds() / 3600.0
            s.x_km = s.x0_km + s.vx_kmh * hours
            s.y_km = s.y0_km + s.vy_kmh * hours
            past = (s.x_km * s.vx_kmh + s.y_km * s.vy_kmh) / max(
                math.hypot(s.vx_kmh, s.vy_kmh), 1e-9
            )
            dead = (
                age >= s.life_h
                or past > SYSTEM_REACH_KM
                or math.hypot(s.x_km, s.y_km) > 4 * SYSTEM_REACH_KM
            )
            if dead:
                s.gone = True
                if s.kind == "high":
                    self._high = None
                    self._high_birth = when + self._high_gap(t)
                else:
                    freed += 1
                continue
            live.append(s)
        self.systems = live
        for _ in range(freed):
            self._low_births.append(when + self._low_gap(t))
        # slots whose gap has passed get their low
        due = [b for b in self._low_births if b <= when]
        self._low_births = [b for b in self._low_births if b > when]
        for _ in due:
            low = self._draw_low(when, t)
            self.systems.append(low)
        if self._high is None and self._high_birth is not None and self._high_birth <= when:
            self._high = self._draw_high(when, t)
            self._high_birth = None
            self.systems.append(self._high)
        for s in self.systems:  # the systems born now: their anomaly by the curve at once
            if s.life_h is not None:
                age = s.age_h(when)
                s.anomaly_hpa = s.peak_hpa * math.sin(math.pi * min(max(age / s.life_h, 0.0), 1.0))

    # -- the field ----------------------------------------------------------

    def pressure_at(self, x_km: float, y_km: float) -> float:
        p = self._background + self._gradient[0] * x_km + self._gradient[1] * y_km
        for s in self.systems:
            p += s.anomaly_and_gradient(x_km, y_km)[0]
        return p

    def geostrophic_at(self, x_km: float, y_km: float) -> tuple[float, float]:
        """The geostrophic wind's velocity (m/s east, north): each system's gradient turned
        ninety degrees with low pressure on the left, capped in strong curvature by the
        gradient-wind rule (Holton, *An Introduction to Dynamic Meteorology*, the gradient
        wind: cyclonic flow is subgeostrophic, anticyclonic flow cannot exceed f r / 4 in
        its geostrophic value)."""
        gx, gy = self._gradient
        vx = -GEOSTROPHIC_MS_PER_HPA_PER_100KM * 100.0 * gy
        vy = GEOSTROPHIC_MS_PER_HPA_PER_100KM * 100.0 * gx
        for s in self.systems:
            _, gx, gy, u = s.anomaly_and_gradient(x_km, y_km)
            g = math.hypot(gx, gy)  # hPa/km
            if g == 0.0:
                continue
            vg = GEOSTROPHIC_MS_PER_HPA_PER_100KM * g * 100.0  # m/s
            r_m = u * s.radius_km * 1000.0
            if r_m > 0.0:
                if s.kind == "low":
                    vg = 2.0 * vg / (1.0 + math.sqrt(1.0 + 4.0 * vg / (CORIOLIS_50N * r_m)))
                else:
                    vg = min(vg, CORIOLIS_50N * r_m / 4.0)
            # k x grad p: (-gy, gx), the wind with low pressure on its left
            vx += vg * (-gy / g)
            vy += vg * (gx / g)
        return vx, vy

    def surface_wind_at(
        self, x_km: float, y_km: float, when: datetime | None = None
    ) -> tuple[float, float]:
        """The surface wind at a point: (direction from, radians; speed, m/s at ten
        metres). The geostrophic wind turned SURFACE_TURN_DEG toward low pressure (to the
        left, in the northern hemisphere) and scaled by SURFACE_SCALE, plus the fronts'
        veer of the point's sector, plus the sea breeze where a coast is known (inert)."""
        vx, vy = self.geostrophic_at(x_km, y_km)
        speed = math.hypot(vx, vy) * SURFACE_SCALE
        if speed == 0.0:
            return 0.0, 0.0
        turn = math.radians(SURFACE_TURN_DEG)
        # rotate the velocity anticlockwise by `turn` (x east, y north)
        c, s_ = math.cos(turn), math.sin(turn)
        wx, wy = vx * c - vy * s_, vx * s_ + vy * c
        direction = units.wind_direction_from(wx, wy)
        sector = self.sector_at(x_km, y_km, when)
        direction = units.wrap_2pi(direction + math.radians(sector.veer_deg))
        bx, by = self.sea_breeze(x_km, y_km, when or self.now)
        if bx or by:
            ax, ay = units.wind_vector(direction, speed)
            direction = units.wind_direction_from(ax + bx, ay + by)
            speed = math.hypot(ax + bx, ay + by)
        return direction, speed

    def sector_at(self, x_km: float, y_km: float, when: datetime | None = None) -> Sector:
        """Which sector a point is in and how far from the fronts (W §1.3): the nearest
        low in radii decides, its fronts by their bearings; under a high when no low's
        front is near; open sea otherwise."""
        when = when or self.now
        best: Sector | None = None
        best_u = math.inf
        high_u: float | None = None
        for s in self.systems:
            if s.kind == "high":
                _, _, _, u = s.anomaly_and_gradient(x_km, y_km)
                if high_u is None or u < high_u:
                    high_u = u
                continue
            dx, dy = x_km - s.x_km, y_km - s.y_km
            r = math.hypot(dx, dy)
            u = r / s.radius_km
            if u >= best_u:
                continue
            warm_b, cold_b, occluded = s.fronts_at(when)
            beta = _bearing_deg(dx, dy)
            width = (cold_b - warm_b) % 360.0
            a = (beta - warm_b) % 360.0
            d_warm, along_w = _to_segment(dx, dy, warm_b, FRONT_LENGTH_KM)
            d_cold, along_c = _to_segment(dx, dy, cold_b, FRONT_LENGTH_KM)
            if not occluded and a < width:
                sector = "warm"
            else:
                e = (a - width) % 360.0
                sector = "behind" if e < (360.0 - width) / 2.0 else "ahead"
            veer = 0.0
            air = "neutral"
            if sector == "warm":
                air = "warm"
                if d_cold < COLD_FRONT_BAND_KM and along_c > 0:
                    veer = -COLD_FRONT_PRE_BACK_DEG * (1.0 - d_cold / COLD_FRONT_BAND_KM)
            elif sector == "ahead":
                if along_w > 0:
                    veer = -WARM_FRONT_VEER_DEG * max(0.0, 1.0 - d_warm / WARM_FRONT_APPROACH_KM)
            else:  # behind the cold front
                if along_c > 0:
                    fade = max(0.0, 1.0 - d_cold / COLD_FRONT_VEER_FADE_KM)
                    veer = COLD_FRONT_VEER_DEG * fade
                    if occluded:
                        veer += WARM_FRONT_VEER_DEG * fade  # both fronts in one
                    if d_cold < COLD_FRONT_SHOWERS_KM:
                        air = "unstable"
            best = Sector(sector, air, d_warm, d_cold, s, None, veer)
            best_u = u
        if best is not None and best.low is not None:
            near_front = (
                (
                    best.sector == "ahead"
                    and best.to_warm_km is not None
                    and best.to_warm_km < WARM_FRONT_APPROACH_KM
                )
                or best.sector == "warm"
                or (
                    best.sector == "behind"
                    and best.to_cold_km is not None
                    and best.to_cold_km < COLD_FRONT_SHOWERS_KM
                )
            )
            if near_front or best_u < 1.5:
                return best
        if high_u is not None and high_u < UNDER_HIGH_RADII:
            return Sector("high", "neutral", None, None, None, high_u, 0.0)
        return best if best is not None and best_u < 2.0 else Sector("open", "neutral")

    def conditions_at(self, x_km: float, y_km: float, when: datetime | None = None) -> Conditions:
        """The sky, the weather and the visibility at a point by the sector table of W §1.3,
        with a little seeded noise by the hour so that two hours differ; and the pressure."""
        when = when or self.now
        sec = self.sector_at(x_km, y_km, when)
        block = int(_seconds(when) // 3600) // SKY_NOISE_HOURS
        n1 = _noise(self.seed, f"sky:{block}")
        n2 = _noise(self.seed, f"weather:{block}")
        jitter = 0.8 + 0.4 * n1  # the distance thresholds move by a fifth either way
        sky, signs, weather, vis = "detached clouds", "", "fine", "the horizon"
        dawn = 3 <= when.hour < 6
        if sec.sector == "ahead":
            d = (sec.to_warm_km if sec.to_warm_km is not None else math.inf) * jitter
            if d > 2 * WARM_FRONT_APPROACH_KM:
                sky, signs = (
                    ("clear", SKY_SIGNS["streaked"]) if n2 < 0.5 else ("detached clouds", "")
                )
            elif d > WARM_FRONT_APPROACH_KM:
                sky, signs = "detached clouds", SKY_SIGNS["streaked"]
            elif d > WARM_FRONT_RAIN_KM:
                sky, signs = "overcast", SKY_SIGNS["high dawn"] if dawn else ""
            elif d > WARM_FRONT_GLOOM_KM:
                sky, weather, vis = "overcast", "rain", "a few miles"
            else:
                sky, weather, vis = "dark and gloomy", "rain", "a mile"
                signs = SKY_SIGNS["scud"] if n2 < 0.5 else ""
        elif sec.sector == "warm":
            d_c = sec.to_cold_km if sec.to_cold_km is not None else math.inf
            if d_c < COLD_FRONT_BAND_KM * jitter:
                sky, weather, vis = "threatening", "rain", "a few miles"
                signs = SKY_SIGNS["inky"]
            else:
                sky = "hazy" if n1 < 0.35 else "overcast"
                weather = "drizzle" if n2 < 0.45 else "fine"
                vis = "a few miles" if weather == "drizzle" or sky == "hazy" else "the horizon"
                if self.coastal_fog(x_km, y_km, when):
                    sky, weather, vis = "thick", "fog", "a cable"
        elif sec.sector == "behind":
            d = (sec.to_cold_km if sec.to_cold_km is not None else math.inf) * jitter
            if d < COLD_FRONT_BAND_KM:
                sky, weather, vis = "dark and gloomy", "squally", "a mile"
                signs = SKY_SIGNS["scud"]
                if n2 < 0.15:
                    weather = "thunder"
            elif d < COLD_FRONT_SHOWERS_KM:
                sky, signs = "detached clouds", SKY_SIGNS["hard edged"]
                if n2 < 0.4:
                    weather, vis = "passing showers", "a few miles"
            else:
                sky = "clear" if n2 < 0.5 else "detached clouds"
        elif sec.sector == "high":
            sky = "hazy" if (when.month in (5, 6, 7, 8) and n1 < 0.4) else "clear"
            vis = "a few miles" if sky == "hazy" else "the horizon"
            if self.coastal_fog(x_km, y_km, when):
                sky, weather, vis = "thick", "fog", "a cable"
        else:  # open sea between systems
            sky = "detached clouds" if n1 < 0.7 else "clear"
        return Conditions(
            sec.sector, sec.air_mass, sky, signs, weather, vis, self.pressure_at(x_km, y_km)
        )

    # -- the coast's hooks (spec M5 §11; package 32): the sea breeze and the fog -------

    # `coast` is the World's hook (package 32): a callable of a point of the plane
    # (km east, km north of the origin) giving the distance to the nearest coast in
    # kilometres and the bearing toward it in degrees, from the chart's distance field,
    # or None where the chart has no field. None (no chart): no coast, no breeze, no fog,
    # and every scenario of the earlier milestones is what it was.
    coast: Any = None

    def coast_distance_km(self, x_km: float, y_km: float) -> float | None:
        """The distance to the nearest coast (spec §11), from the chart through the
        World's hook; None where no coast is known."""
        found = self._coast(x_km, y_km)
        return found[0] if found is not None else None

    def _coast(self, x_km: float, y_km: float) -> tuple[float, float] | None:
        if self.coast is None:
            return None
        return self.coast(x_km, y_km)

    def sea_breeze(self, x_km: float, y_km: float, when: datetime) -> tuple[float, float]:
        """The sea breeze's velocity (m/s east, north) to add to the surface wind (W §1.4,
        Simpson 1994): a summer, daylight, fine-weather onshore wind of some ten knots at
        most, strongest in mid-afternoon, felt a few miles to sea and dying at dusk. The
        onshore direction is the bearing to the nearest coast; the strength is the
        product of the season's, the hour's, the distance's and the gradient's factors
        (`SEA_BREEZE_*`), and it blows only in fine weather away from a low's fronts."""
        found = self._coast(x_km, y_km)
        if found is None:
            return 0.0, 0.0
        distance_km, bearing_deg = found
        if distance_km >= SEA_BREEZE_REACH_KM or when.month not in SEA_BREEZE_MONTHS:
            return 0.0, 0.0
        hour = when.hour + when.minute / 60.0
        if not SEA_BREEZE_ONSET_H < hour < SEA_BREEZE_END_H:
            return 0.0, 0.0
        sector = self.sector_at(x_km, y_km, when)
        fine = sector.sector in ("high", "open") or (
            sector.sector == "behind"
            and sector.to_cold_km is not None
            and sector.to_cold_km > COLD_FRONT_SHOWERS_KM
        )
        if not fine:
            return 0.0, 0.0
        # the hour's hump, from onset to dusk, its peak in mid-afternoon
        span = SEA_BREEZE_END_H - SEA_BREEZE_ONSET_H
        diurnal = math.sin(math.pi * (hour - SEA_BREEZE_ONSET_H) / span)
        # felt a few miles to sea: full inshore, gone at the reach
        reach = (
            1.0
            if distance_km <= SEA_BREEZE_FULL_KM
            else ((SEA_BREEZE_REACH_KM - distance_km) / (SEA_BREEZE_REACH_KM - SEA_BREEZE_FULL_KM))
        )
        # a strong gradient wind overrides it
        gx, gy = self.geostrophic_at(x_km, y_km)
        gradient_kn = units.ms_to_knots(math.hypot(gx, gy) * SURFACE_SCALE)
        if gradient_kn >= SEA_BREEZE_GRADIENT_CAP_KN:
            return 0.0, 0.0
        damping = 1.0 - max(0.0, gradient_kn - SEA_BREEZE_GRADIENT_FREE_KN) / (
            SEA_BREEZE_GRADIENT_CAP_KN - SEA_BREEZE_GRADIENT_FREE_KN
        )
        speed = units.knots_to_ms(SEA_BREEZE_MAX_KN) * diurnal * reach * damping
        if speed <= 0.0:
            return 0.0, 0.0
        toward = math.radians(bearing_deg)
        return speed * math.sin(toward), speed * math.cos(toward)

    def coastal_fog(self, x_km: float, y_km: float, when: datetime) -> bool:
        """Advection fog (W §1.4): near the coasts, in a stable warm sector or under a
        high, with a slack wind (a fresh wind lifts it to low cloud), most often in late
        spring and early summer. Decided once a sky block (`SKY_NOISE_HOURS`) by the
        month's chance from the seed, so a day replays and two hours differ."""
        found = self._coast(x_km, y_km)
        if found is None or found[0] > FOG_COAST_KM:
            return False
        sector = self.sector_at(x_km, y_km, when)
        if sector.sector not in ("warm", "high"):
            return False
        gx, gy = self.geostrophic_at(x_km, y_km)
        if units.ms_to_knots(math.hypot(gx, gy) * SURFACE_SCALE) > FOG_MAX_WIND_KN:
            return False
        block = int(_seconds(when) // 3600) // SKY_NOISE_HOURS
        chance = FOG_CHANCE_BY_MONTH[when.month - 1] * FOG_CONDITIONAL_FACTOR
        return _noise(self.seed, f"fog:{block}") < chance


# ---------------------------------------------------------------------------
# The prevailing quarter of a day, for the climatology's check (W §1.1)
# ---------------------------------------------------------------------------

QUARTERS: tuple[str, ...] = ("N", "E", "S", "W")


def quarter_of(direction_from_rad: float, speed_ms: float) -> str | None:
    """'W' for a wind from 225 to 315 degrees true, and so round; None in light airs."""
    if units.ms_to_knots(speed_ms) < CALM_KN:
        return None
    d = units.rad_to_deg(direction_from_rad) % 360.0
    if 45.0 <= d < 135.0:
        return "E"
    if 135.0 <= d < 225.0:
        return "S"
    if 225.0 <= d < 315.0:
        return "W"
    return "N"


def prevailing(quarters: list[str | None]) -> str | None:
    """The day's prevailing quarter: the one holding the plurality of the day's hours,
    when it holds at least half of them; else none (S1's indices leave about a tenth of
    days with no prevailing quarter)."""
    counts = {q: 0 for q in QUARTERS}
    for q in quarters:
        if q is not None:
            counts[q] += 1
    best = max(QUARTERS, key=lambda q: counts[q])
    if counts[best] * 2 >= len(quarters) and counts[best] > 0:
        return best
    return None
