"""The tide: the world's and the captain's (spec M5 §16; the study
`docs/design/Tides1805.md`, T, §1, §2 and §5, model (b) with the streams tabulated by
area; package 34).

**The world keeps the truth and the captain keeps his account**, for the tide as for the
position. The world's tide is M2, S2 and N2 at the eleven TICON gauges
(`data/tides/constituents.yaml`, CC BY 4.0), interpolated between the gauges on the
complex constants by the inverse square of the distance, with the astronomical arguments
from the moon's and the sun's mean longitudes (Meeus ch. 25 and 47, the same elements
`core/moon.py` keeps), so that springs fall a day or two after full and change of
themselves and the perigean spring exceeds the apogean by a fifth; the streams by area
(`data/tides/streams.yaml`: an axis, a spring rate, a neap rate and a phase against local
high water, from Bowditch 1802's headland table and the published summaries of the
atlases), their rate following the local range the constants give. Evaluated once a
simulated minute by the World (`core/world.py`): the height goes under the lead and over
the rocks that cover, the stream sets the ship in the physics as a water velocity
(`physics/integrate.py`). **No reading gives any of it**: the tests read `Tide.at` from the
world, and the captain has the period's means only (T §5).

**The captain's tide** is the establishment of the port from his epitome
(`data/tides/establishments.yaml`: Norie's hours and minutes for a ship of war, Moore's
points of the moon's bearing for the rest, T §2) and the moon's age from his almanac,
worked by Moore's rule of 48 minutes a day (`Epitome.high_waters`), wrong by up to an
hour as Bowditch admits and by more with an old table; the reading `the tide by the
almanac` (`api/readings.py`) says it in the master's words. The difference between the
two tides is the play (truth 64).

The arithmetic: h(t) = Z0 + Σ f_i A_i cos(V_i(t) + u_i − g_i), the Greenwich phase lag g
as TICON gives it; V_M2 = 2(T + h − s), V_S2 = 2T, V_N2 = 2(T + h − s) − (s − p) with T the
mean sun's hour angle at Greenwich (15° an hour of Universal Time from midnight), s, h and
p the mean longitudes of the moon, the sun and the lunar perigee (Doodson's arguments as
Schureman 1958 tabulates them, Table 2); the nodal factors f and u of M2 and N2 from the
longitude of the moon's node (Schureman: f = 1.0004 − 0.0373 cos N, u = −2.14° sin N),
S2 having none. The sum of the three as a complex number Z is the tide's state: its real
part the height above mean level, its argument the phase (0 at high water, the stream's
clock), its modulus the amplitude now, between neaps and springs, which scales the stream.
Every constant names its source or says "judgement"; the figures the study marks
unverified are marked in the data files and in `docs/dev/TuningNotes.md`.
"""

from __future__ import annotations

import cmath
import math
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

import yaml

from freesail import units
from freesail.core.moon import julian_day
from freesail.world.geo import Position, bearing_and_distance

__all__ = [
    "CONSTITUENTS_PATH",
    "ESTABLISHMENTS_PATH",
    "STREAMS_PATH",
    "Epitome",
    "EpitomePort",
    "Gauge",
    "StreamArea",
    "Tide",
    "TideState",
    "astronomical_arguments",
    "load_tide",
    "local_mean_time",
    "moore_minutes",
    "time_words",
]

TIDES_DIR = Path(__file__).resolve().parents[2] / "data" / "tides"
CONSTITUENTS_PATH = TIDES_DIR / "constituents.yaml"
STREAMS_PATH = TIDES_DIR / "streams.yaml"
ESTABLISHMENTS_PATH = TIDES_DIR / "establishments.yaml"

# The tide is evaluated once a simulated minute (spec M5 §16: "evaluated once a simulated
# minute; five cosines"); the World reads it at the minute's first tick.
TIDE_TICK_S = 60

# The constants interpolated at a position are kept while she stays within this of where
# they were worked (judgement: a hundredth of a degree is a third of a mile, over which the
# interpolation moves by a centimetre and a minute; the ship moves a cable a minute at most).
CONSTANTS_CELL_DEG = 0.01
# The nearest a gauge is taken to be, for the inverse-square weight (a ship moored on the
# gauge itself takes its constants whole).
GAUGE_FLOOR_M = 100.0

# Slack water, "the turn": the stream under a tenth of its rate, which it is within six
# degrees of the tide's phase (twelve minutes) either side of the turn (judgement: what
# the cable slackens at, Luce 1884 App. K: "when the tide is done she will thwart, and
# ride with the chain slack under foot").
SLACK_PHASE_DEG = 6.0


def local_mean_time(when_ut: datetime, lon_deg: float) -> datetime:
    """The mean time of a meridian from Universal Time: east longitude is ahead."""
    return when_ut + timedelta(hours=lon_deg / 15.0)


# ---------------------------------------------------------------------------
# The astronomical arguments
# ---------------------------------------------------------------------------


def _mean_longitudes(t: float) -> tuple[float, float, float, float]:
    """The moon's mean longitude s, the sun's h, the lunar perigee's p and the moon's
    ascending node's N, in degrees, at `t` Julian centuries from J2000 (Meeus eq. 47.1,
    25.2 and 47.7; the first the same formula `core.moon` uses for the moon's L')."""
    s = 218.3164477 + 481267.88123421 * t - 0.0015786 * t * t
    h = 280.46646 + 36000.76983 * t + 0.0003032 * t * t
    p = 83.3532465 + 4069.0137287 * t - 0.0103200 * t * t
    n = 125.0445479 - 1934.1362891 * t + 0.0020754 * t * t
    return s % 360.0, h % 360.0, p % 360.0, n % 360.0


def astronomical_arguments(when_ut: datetime) -> dict[str, tuple[float, float]]:
    """For M2, S2 and N2 at a moment of Universal Time: (V + u, f), the equilibrium
    argument with its nodal correction in degrees, and the node factor."""
    jd = julian_day(when_ut)
    t = (jd - 2451545.0) / 36525.0
    s, h, p, n = _mean_longitudes(t)
    hours = when_ut.hour + when_ut.minute / 60.0 + when_ut.second / 3600.0
    big_t = 15.0 * hours  # the mean sun's hour angle at Greenwich, from midnight
    nr = math.radians(n)
    f_lunar = 1.0004 - 0.0373 * math.cos(nr) + 0.0002 * math.cos(2.0 * nr)
    u_lunar = -2.14 * math.sin(nr)
    tau2 = 2.0 * (big_t + h - s)
    return {
        "M2": ((tau2 + u_lunar) % 360.0, f_lunar),
        "S2": ((2.0 * big_t) % 360.0, 1.0),
        "N2": ((tau2 - (s - p) + u_lunar) % 360.0, f_lunar),
    }


def moon_age_days(when_ut: datetime) -> float:
    """The moon's age by the mean longitudes (the almanac's arithmetic), for the check
    against `core.moon.moon_at`: (s − h) over the lunation's 360 degrees."""
    from freesail.core.moon import LUNATION_DAYS

    jd = julian_day(when_ut)
    t = (jd - 2451545.0) / 36525.0
    s, h, _, _ = _mean_longitudes(t)
    return ((s - h) % 360.0) / 360.0 * LUNATION_DAYS


# ---------------------------------------------------------------------------
# The world's tide
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Gauge:
    id: str
    name: str
    position: Position
    mean_level_m: float
    constants: dict[str, tuple[float, float]]  # name -> (amplitude m, phase lag deg)


@dataclass(frozen=True)
class StreamArea:
    id: str
    name: str
    polygon: tuple[tuple[float, float], ...] | None  # (lat, lon) corners; None: everywhere
    axis_deg: float
    spring_kn: float
    neap_kn: float
    phase_h: float
    source: str = ""

    def contains(self, pos: Position) -> bool:
        if self.polygon is None:
            return True
        return _point_in_polygon(pos.lat_deg, pos.lon_deg, self.polygon)


def _point_in_polygon(lat: float, lon: float, poly: tuple[tuple[float, float], ...]) -> bool:
    inside = False
    n = len(poly)
    for i in range(n):
        y1, x1 = poly[i]
        y2, x2 = poly[(i + 1) % n]
        if (y1 > lat) != (y2 > lat):
            x = x1 + (lat - y1) * (x2 - x1) / (y2 - y1)
            if lon < x:
                inside = not inside
    return inside


@dataclass(frozen=True)
class TideState:
    """The tide at a place and a moment: the height above the chart's datum, the phase
    (degrees, 0 at high water, growing through the ebb to 180 at low water), the
    semidiurnal amplitude now and its neap and spring values (the range is twice these),
    whether it is rising, and the stream as a velocity over the ground."""

    height_m: float
    phase_deg: float
    amplitude_m: float
    neap_amplitude_m: float
    spring_amplitude_m: float
    rising: bool
    stream_east_ms: float
    stream_north_ms: float
    area_id: str
    axis_deg: float
    rate_kn: float  # the area's rate now, between its neap and its spring figure

    @property
    def stream_kn(self) -> float:
        return units.ms_to_knots(math.hypot(self.stream_east_ms, self.stream_north_ms))

    @property
    def stream_toward_deg(self) -> float:
        if self.stream_east_ms == 0.0 and self.stream_north_ms == 0.0:
            return self.axis_deg
        return math.degrees(math.atan2(self.stream_east_ms, self.stream_north_ms)) % 360.0

    @property
    def flood(self) -> bool:
        """Whether the stream runs along its axis (the flood) rather than against it."""
        d = (self.stream_toward_deg - self.axis_deg + 180.0) % 360.0 - 180.0
        return abs(d) < 90.0

    @property
    def slack(self) -> bool:
        """At the turn: the stream under a tenth of the rate it runs at (`SLACK_PHASE_DEG`
        either side of the turn, since cos 84° is a tenth)."""
        return self.stream_kn < 0.1 * self.rate_kn

    @property
    def springs_fraction(self) -> float:
        """0 at mean neaps, 1 at mean springs, beyond either at the perigean and apogean."""
        span = self.spring_amplitude_m - self.neap_amplitude_m
        if span <= 1e-9:
            return 0.5
        return (self.amplitude_m - self.neap_amplitude_m) / span

    def to_dict(self) -> dict[str, Any]:
        return {
            "height_m": round(self.height_m, 2),
            "phase_deg": round(self.phase_deg, 1),
            "amplitude_m": round(self.amplitude_m, 2),
            "rising": self.rising,
            "stream_kn": round(self.stream_kn, 2),
            "stream_toward_deg": round(self.stream_toward_deg, 1),
            "area": self.area_id,
        }


class Tide:
    """The world's tide: the gauges, the stream areas and the arithmetic."""

    def __init__(self, constituents: dict[str, Any], streams: dict[str, Any]):
        self.speeds: dict[str, float] = {
            str(k): float(v["speed_deg_per_h"]) for k, v in constituents["constituents"].items()
        }
        self.gauges: list[Gauge] = []
        for g in constituents["gauges"]:
            consts = {
                name: (float(g[name]["amplitude_m"]), float(g[name]["phase_deg"]))
                for name in self.speeds
            }
            self.gauges.append(
                Gauge(
                    str(g["id"]),
                    str(g["name"]),
                    Position(float(g["lat_deg"]), float(g["lon_deg"])),
                    float(g["mean_level_m"]),
                    consts,
                )
            )
        self.power = float((constituents.get("interpolation") or {}).get("power", 2))
        self.areas: list[StreamArea] = []
        for a in streams["areas"]:
            poly = a.get("polygon")
            self.areas.append(
                StreamArea(
                    str(a["id"]),
                    str(a["name"]),
                    tuple((float(p[0]), float(p[1])) for p in poly) if poly else None,
                    float(a["axis_deg"]),
                    float(a["spring_kn"]),
                    float(a["neap_kn"]),
                    float(a["phase_h"]),
                    str(a.get("source", "")),
                )
            )
        self._cache: dict[tuple[int, int], tuple[float, dict[str, tuple[float, float]]]] = {}

    # -- the constants at a place -------------------------------------------------------

    def constants_at(self, pos: Position) -> tuple[float, dict[str, tuple[float, float]]]:
        """The mean level above datum and the (amplitude, phase lag) of each constituent
        at a position: the inverse-distance-squared mean over the gauges of the complex
        constants A e^{-ig} (the cotidal and corange geometry in its simplest form)."""
        key = (
            int(math.floor(pos.lat_deg / CONSTANTS_CELL_DEG)),
            int(math.floor(pos.lon_deg / CONSTANTS_CELL_DEG)),
        )
        found = self._cache.get(key)
        if found is not None:
            return found
        # Evaluated at the cell's centre, not at the point that happened to ask first: the
        # table is shared between the Worlds of one process, and a value that depended on
        # the first asker made a passage's log depend on the worlds built before it
        # (package 35 found the schooner's pinned digest moving with the suite's order).
        centre = Position(
            (key[0] + 0.5) * CONSTANTS_CELL_DEG,
            (key[1] + 0.5) * CONSTANTS_CELL_DEG,
        )
        total = 0.0
        level = 0.0
        sums: dict[str, complex] = {name: 0j for name in self.speeds}
        for g in self.gauges:
            _, d = bearing_and_distance(centre, g.position)
            w = 1.0 / max(d, GAUGE_FLOOR_M) ** self.power
            total += w
            level += w * g.mean_level_m
            for name, (amp, lag) in g.constants.items():
                sums[name] += w * cmath.rect(amp, -math.radians(lag))
        consts = {}
        for name, z in sums.items():
            z /= total
            consts[name] = (abs(z), (-math.degrees(cmath.phase(z))) % 360.0)
        out = (level / total, consts)
        if len(self._cache) > 256:
            self._cache.clear()
        self._cache[key] = out
        return out

    def area_at(self, pos: Position) -> StreamArea:
        for a in self.areas:
            if a.contains(pos):
                return a
        return self.areas[-1]

    # -- the tide at a place and a moment -----------------------------------------------

    def _z(self, pos: Position, when_ut: datetime) -> tuple[float, complex, float, float]:
        level, consts = self.constants_at(pos)
        args = astronomical_arguments(when_ut)
        z = 0j
        for name, (amp, lag) in consts.items():
            v_u, f = args[name]
            z += cmath.rect(f * amp, math.radians(v_u - lag))
        a_m2, a_s2 = consts["M2"][0], consts["S2"][0]
        return level, z, a_m2 - a_s2, a_m2 + a_s2

    def at(self, pos: Position, when_ut: datetime) -> TideState:
        level, z, neap, spring = self._z(pos, when_ut)
        phase = math.degrees(cmath.phase(z)) % 360.0
        amplitude = abs(z)
        area = self.area_at(pos)
        span = spring - neap
        fraction = (amplitude - neap) / span if span > 1e-9 else 0.5
        rate_kn = area.neap_kn + (area.spring_kn - area.neap_kn) * fraction
        # the flood runs strongest `phase_h` hours after local high water: the stream is a
        # cosine of the height's phase, shifted by the area's phase at M2's rate
        shift = area.phase_h * self.speeds["M2"]
        along = rate_kn * math.cos(math.radians(phase - shift))
        speed = units.knots_to_ms(along)
        axis = math.radians(area.axis_deg)
        rising = math.sin(math.radians(phase)) < 0.0  # the phase grows: past 180 it rises
        return TideState(
            height_m=level + z.real,
            phase_deg=phase,
            amplitude_m=amplitude,
            neap_amplitude_m=neap,
            spring_amplitude_m=spring,
            rising=rising,
            stream_east_ms=speed * math.sin(axis),
            stream_north_ms=speed * math.cos(axis),
            area_id=area.id,
            axis_deg=area.axis_deg,
            rate_kn=rate_kn,
        )

    def height_at(self, pos: Position, when_ut: datetime) -> float:
        level, z, _, _ = self._z(pos, when_ut)
        return level + z.real

    def stream_at(self, pos: Position, when_ut: datetime) -> tuple[float, float]:
        s = self.at(pos, when_ut)
        return s.stream_east_ms, s.stream_north_ms

    def high_waters(
        self, pos: Position, from_ut: datetime, hours: float = 24.0
    ) -> list[tuple[datetime, float]]:
        """The high waters at a place in the hours from `from_ut`: the times (Universal
        Time) and heights above datum, found by the minute and refined on the parabola
        through the three readings about the crest."""
        n = int(hours * 60)
        heights = [self.height_at(pos, from_ut + timedelta(minutes=i)) for i in range(n + 1)]
        out = []
        for i in range(1, n):
            if heights[i] >= heights[i - 1] and heights[i] > heights[i + 1]:
                a, b, c = heights[i - 1], heights[i], heights[i + 1]
                denom = a - 2.0 * b + c
                offset = 0.5 * (a - c) / denom if abs(denom) > 1e-12 else 0.0
                when = from_ut + timedelta(minutes=i + offset)
                out.append((when, b - 0.25 * (a - c) * offset))
        return out

    def establishment_at(self, pos: Position) -> float:
        """The world's own establishment of a place: the hour of high water on the day of
        full and change, local mean time, from the constants alone. At syzygy the
        arguments of M2 and S2 coincide, so the crest falls at the argument of
        A_M2 e^{i g_M2} + A_S2 e^{i g_S2} (the sun's tide pulling the moon's later or
        earlier by its phase difference: the vulgar establishment of Whewell 1833 against
        the corrected, which is the M2 lag alone), at thirty degrees an hour."""
        _, consts = self.constants_at(pos)
        a_m2, g_m2 = consts["M2"]
        a_s2, g_s2 = consts["S2"]
        crest = cmath.rect(a_m2, math.radians(g_m2)) + cmath.rect(a_s2, math.radians(g_s2))
        hours_ut = (math.degrees(cmath.phase(crest)) % 360.0) / self.speeds["S2"]
        return (hours_ut + pos.lon_deg / 15.0) % 12.0


def load_tide(
    constituents: str | Path = CONSTITUENTS_PATH, streams: str | Path = STREAMS_PATH
) -> Tide:
    c = yaml.safe_load(Path(constituents).read_text(encoding="utf-8"))
    s = yaml.safe_load(Path(streams).read_text(encoding="utf-8"))
    return Tide(c, s)


# ---------------------------------------------------------------------------
# The captain's tide: the epitome's table and Moore's rule
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class EpitomePort:
    name: str
    position: Position
    hw_h: int
    hw_m: int
    spring_rise_ft: float | None = None
    bearing: str | None = None  # Moore's table: the moon's bearing at high water
    note: str = ""

    @property
    def establishment_h(self) -> float:
        return self.hw_h + self.hw_m / 60.0

    @property
    def establishment_words(self) -> str:
        return time_words(self.establishment_h, clock=False)


@dataclass
class Epitome:
    """The captain's table of high water at full and change, by port, and the rule he
    works the day's tide by: the epitome's (`norie`) or Moore's (`moore`)."""

    table: str
    title: str
    ports: list[EpitomePort]
    minutes_per_day: float = 48.0
    source: str = field(default="")

    @classmethod
    def load(cls, table: str, path: str | Path = ESTABLISHMENTS_PATH) -> Epitome:
        doc = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
        tables = doc.get("tables") or {}
        if table not in tables:
            known = ", ".join(sorted(tables))
            raise ValueError(f"no epitome table named '{table}' (the tables are {known})")
        t = tables[table]
        ports = [
            EpitomePort(
                str(p["name"]),
                Position(float(p["lat_deg"]), float(p["lon_deg"])),
                int(p["hw_h"]),
                int(p["hw_m"]),
                None if p.get("spring_rise_ft") is None else float(p["spring_rise_ft"]),
                str(p["bearing"]) if p.get("bearing") else None,
                str(p.get("note", "")),
            )
            for p in t["ports"]
        ]
        return cls(
            table, str(t.get("title", table)), ports, float(doc.get("minutes_per_day_of_age", 48))
        )

    def by_name(self, name: str) -> EpitomePort | None:
        key = _key(name)
        for p in self.ports:
            if _key(p.name) == key:
                return p
        return None

    def nearest(self, pos: Position) -> tuple[EpitomePort, float]:
        """The nearest port of the table to a position, and its distance in miles."""
        best = None
        for p in self.ports:
            _, d = bearing_and_distance(pos, p.position)
            if best is None or d < best[1]:
                best = (p, d)
        assert best is not None
        return best[0], best[1] / units.NAUTICAL_MILE

    def high_waters(self, port: EpitomePort, age_days: float, day: date) -> list[datetime]:
        """Moore's rule for the day: the moon's southing `age × 48 minutes` past noon,
        plus the establishment, gives the afternoon's high water; the other tide is
        twelve hours and twenty-five minutes before or after. The two that fall within
        the civil day, in the port's own time (the ship's clock keeps near enough it)."""
        southing_min = moore_minutes(age_days, self.minutes_per_day)
        noon = datetime(day.year, day.month, day.day, 12, 0)
        hw = noon + timedelta(minutes=southing_min + port.establishment_h * 60.0)
        half = timedelta(hours=12, minutes=25)
        candidates = [hw - 2 * half, hw - half, hw, hw + half]
        start = datetime(day.year, day.month, day.day)
        end = start + timedelta(days=1)
        return [t for t in candidates if start <= t < end]


def moore_minutes(age_days: float, minutes_per_day: float = 48.0) -> float:
    """The moon's southing past noon by Moore's rule, in minutes: the age times 48,
    "the quotient will be the hours, and the remainder the minutes" (Moore 1799). The
    age is taken as the master reckons it from the almanac's hour of the change, to the
    quarter of a day (`Navigation.almanac_age_days`): a whole day's age alone puts the
    tide up to 48 minutes out, the day's worth of Moore's rule itself."""
    return (age_days * minutes_per_day) % (24.0 * 60.0)


def time_words(hours: float, clock: bool = True) -> str:
    """'half past four in the afternoon', 'a quarter to five in the morning' for a time
    of day in hours; with `clock` False, '5h 15m', the table's form."""
    if not clock:
        h = int(hours) % 24
        m = int(round((hours - int(hours)) * 60.0))
        if m == 60:
            h, m = h + 1, 0
        return f"{h}h {m:02d}m"
    total = int(round(hours * 60.0)) % (24 * 60)
    h, m = divmod(total, 60)
    quarter = int(round(m / 15.0))
    if quarter == 4:
        h, quarter = (h + 1) % 24, 0
    hour12 = h % 12 or 12
    next12 = (h + 1) % 12 or 12
    if h < 12:
        part = "in the morning" if h >= 4 else "in the middle watch"
    elif h < 17:
        part = "in the afternoon" if h > 12 else "at noon"
    else:
        part = "in the evening" if h < 21 else "at night"
    if quarter == 0:
        head = "noon" if h == 12 else "midnight" if h == 0 else f"{_hour_word(hour12)} o'clock"
        return head if h in (0, 12) else f"{head} {part}"
    if quarter == 1:
        return f"a quarter past {_hour_word(hour12)} {part}"
    if quarter == 2:
        return f"half past {_hour_word(hour12)} {part}"
    return f"a quarter to {_hour_word(next12)} {part}"


_HOUR_WORDS = (
    "twelve", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
    "eleven", "twelve",
)  # fmt: skip


def _hour_word(h: int) -> str:
    return _HOUR_WORDS[h % 12 or 12]


def _key(name: str) -> str:
    words = "".join(c if c.isalnum() or c.isspace() else " " for c in name.lower()).split()
    if words and words[0] == "the":
        words = words[1:]
    return " ".join(words)
