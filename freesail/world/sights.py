"""The sights (spec M5 §14; N §1 to §5; packages 33a and 33b): the noon latitude by the
sun's meridian altitude, taken at the sun's noon if the sky allows and refused in cloud,
with the instrument's error and the horizon's; the chronometer and the time sight for
the longitude; the lunar; the amplitude and the azimuth for the variation.

The sun model (`freesail.core.sun`) has the declination and the moment of the meridian
passage; the master's arithmetic (the altitude corrected for dip, refraction and the
semi-diameter, the declination from the Almanac, Falconer 1780, 'Quadrant') is his, and
the game models its outcome: the true latitude plus an error drawn from the seed. The
sextant reads to a minute, the octant to two or three (N §3, from Falconer's 'Quadrant'
and the Oxford History of Science Museum's note that the octant stayed the cheap
everyday instrument for latitude); the horizon in haze or swell two to five minutes; "call
it 2 to 5 miles with a good horizon, none in cloud" (N §3). The scenario says which
instrument the ship carries (`Scenario.instrument`: the frigate a sextant, the schooner
an octant); the sea's motion of 5a widens the horizon's error, the hook package 31 left
inert now read. Double altitudes when noon is clouded are not built (spec §32).

**The chronometer** (package 33b; spec §14; N §2) is a scenario item, the captain's own
(`Scenario.chronometer`: the maker, the date it was rated ashore, the rate its certificate
gives, and the drift of the true rate from it, seeded or stated), wound daily by the
master at eight in the morning (Luce 1884, the ship's routine at sea: "8:00 A.M. ...
report chronometers wound"), dead when not wound. **The time sight** (`take a sight for
the longitude`) is a morning or afternoon altitude of the sun with the latitude and the
declination giving the local hour angle, the longitude against the chronometer's
Greenwich time: the game draws its outcome, the true longitude plus the rate's error
times the days since rating plus the sight's own two or three miles (N §4(b)), refused in
cloud or with the sun too low or too near the meridian. **The lunar** (`take a lunar`; N
§4(c), §5) checks its conditions from the moon (`freesail.core.moon`) and, allowed,
occupies the master and two mates for a quarter of an hour and gives, an hour later, a
result *drawn and not computed*: the true longitude plus an error from the seed scaled by
the master's skill, the sea and the moon's rate. The engine never clears a distance.
**The amplitude and the azimuth** (`observe an amplitude`, `observe an azimuth`; decision
30; N §3, Falconer 1780, 'Azimuth-compass' and 'Variation') give the variation by
observation, the sun's bearing by compass against its true bearing, to a degree.

The ship's clock keeps the mean time of the meridian she started on (`core/sun.py`);
Greenwich time is that clock plus the start meridian's westing in time, which the
chronometer keeps and the sights compare. Every result is drawn from the truth the world
keeps (`world.position`) plus a seeded error, never computed from the model's own
geometry; the tests read the truth from the world.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Any

from freesail.core.moon import LUNAR_STARS, LUNATION_DAYS, Moon, moon_at
from freesail.world.geo import Position, format_position

__all__ = [
    "AMPLITUDE_ELEVATION_DEG",
    "AMPLITUDE_SIGMA_DEG",
    "AZIMUTH_MIN_ALTITUDE_DEG",
    "AZIMUTH_NOON_GUARD_H",
    "AZIMUTH_SIGMA_DEG",
    "CHRONOMETER_FAULT_S",
    "CHRONOMETER_RUN_HOURS",
    "CHRONOMETER_WIND_HOUR",
    "Chronometer",
    "HAZE_HORIZON_NM",
    "LUNAR_BODY_MIN_ALTITUDE_DEG",
    "LUNAR_CLEARING_MINUTES",
    "LUNAR_DISTANCE_MAX_DEG",
    "LUNAR_DISTANCE_MIN_DEG",
    "LUNAR_MIN_AGE_DAYS",
    "LUNAR_MOON_MIN_ALTITUDE_DEG",
    "LUNAR_ON_DECK_MINUTES",
    "LUNAR_RATE_REFERENCE_DEG_PER_H",
    "LUNAR_SEA_M",
    "LUNAR_SIGMA_GOOD_DEG",
    "LUNAR_SIGMA_POOR_DEG",
    "LUNAR_SKILL_GOOD",
    "LUNAR_SKILL_POOR",
    "LUNAR_TRUST_SIGMAS",
    "Lunar",
    "MOONLIT_FRACTION",
    "MOONLIT_MIN_ALTITUDE_DEG",
    "RATE_DOUBT_S_PER_DAY",
    "RATE_DRIFT_MAX_S_PER_DAY",
    "RATE_DRIFT_MIN_S_PER_DAY",
    "RATING_OFFSET_SIGMA_S",
    "TIME_SIGHT_MIN_ALTITUDE_DEG",
    "TIME_SIGHT_NOON_GUARD_H",
    "TIME_SIGHT_SIGMA_NM",
    "TIME_SIGHT_WORK_MINUTES",
    "TimeSight",
    "Variation",
    "amplitude_or_azimuth",
    "greenwich_time",
    "lunar_body",
    "lunar_result",
    "moon_now",
    "moonlit",
    "time_sight",
    "HORIZON_SEA_NM_PER_M",
    "HORIZON_SIGMA_NM",
    "INSTRUMENTS",
    "OCTANT_SIGMA_NM",
    "SEXTANT_SIGMA_NM",
    "SIGHT_ON_DECK_MINUTES",
    "SKY_HIDES_THE_SUN",
    "WEATHER_HIDES_THE_SUN",
    "NoonResult",
    "Sight",
    "instrument_sigma_nm",
    "noon_sight",
    "sky_allows",
]

# The instrument's error, one sigma, in minutes of altitude which are miles of latitude:
# "sextant to a minute, octant to two or three" (N §3).
SEXTANT_SIGMA_NM = 1.0
OCTANT_SIGMA_NM = 2.5
INSTRUMENTS: tuple[str, ...] = ("sextant", "octant")
# The horizon's error with a good horizon, one sigma (judgement: N §3's "2 to 5 miles
# with a good horizon" taken as the whole error with a sextant, so the horizon's part is
# what makes two miles with the sextant's one); a hazy sky adds a mile (judgement); and
# the sea's motion widens it by half a mile for every metre of sea (judgement: N §3's
# "the horizon in haze or swell two to five minutes", the five with an octant in a
# three-metre sea).
HORIZON_SIGMA_NM = 1.7
HAZE_HORIZON_NM = 1.0
HORIZON_SEA_NM_PER_M = 0.5
# The master is on deck with his instrument for the last quarter of an hour before the
# sun's noon, watching the altitude rise to its greatest (judgement: the practice of
# "waiting for the sun to dip"); the day's work follows below (`reckoning.DAYS_WORK_MINUTES`).
SIGHT_ON_DECK_MINUTES = 15
# The sky that hides the sun at noon (Beaufort's words as the readings give them, spec M5
# §5): overcast, dark and gloomy, threatening and thick hide it; hazy lets it through with
# a worse horizon; and rain, drizzle, fog and thunder hide it whatever the sky says.
SKY_HIDES_THE_SUN = frozenset({"overcast", "dark and gloomy", "threatening", "thick"})
WEATHER_HIDES_THE_SUN = frozenset({"rain", "drizzle", "fog", "thunder"})
# The master's skill scales the instrument's error: a skilled master (0.9) reads his
# instrument at three fifths of its error, a poor one (0.5) at the whole (judgement).
SKILL_REFERENCE = 0.5


def instrument_sigma_nm(instrument: str) -> float:
    if instrument == "sextant":
        return SEXTANT_SIGMA_NM
    if instrument == "octant":
        return OCTANT_SIGMA_NM
    raise ValueError(f"no such instrument as {instrument!r}; say sextant or octant")


def sky_allows(conditions: Any) -> tuple[bool, str]:
    """Whether the sun can be observed under these conditions (None: no weather is kept,
    and the sun of the plane always shows), and the refusal's words when not."""
    if conditions is None:
        return True, ""
    if conditions.weather in WEATHER_HIDES_THE_SUN:
        return False, f"the sun was hid at noon in {conditions.weather}"
    if conditions.sky in SKY_HIDES_THE_SUN:
        return False, "the sun was hid at noon"
    return True, ""


@dataclass(frozen=True)
class Sight:
    """A noon latitude as the master reports it: the latitude, the instrument, and the
    doubt he puts on it (one sigma, miles)."""

    latitude_deg: float
    instrument: str
    sigma_nm: float
    tick: int

    @property
    def words(self) -> str:
        return format_position(Position(self.latitude_deg, 0.0)).split(",")[0]

    def to_dict(self) -> dict[str, Any]:
        return {
            "latitude_deg": round(self.latitude_deg, 5),
            "instrument": self.instrument,
            "sigma_nm": round(self.sigma_nm, 2),
            "tick": self.tick,
        }


@dataclass(frozen=True)
class NoonResult:
    sight: Sight | None
    refusal: str  # "" when the sight was had


def noon_sight(world: Any, master: Any, stream: random.Random) -> NoonResult:
    """The sight at the sun's noon: the true latitude plus the seeded error of the
    instrument, the master's skill, the horizon and the sea; or the refusal."""
    conditions = getattr(world, "conditions", None)
    allowed, why = sky_allows(conditions)
    if not allowed:
        return NoonResult(None, why)
    pos = world.position
    if pos is None:
        return NoonResult(None, "no sea to take a sight on")
    instrument = str(getattr(world.scenario, "instrument", "octant") or "octant")
    skill = float(getattr(master, "skill", 0.7))
    factor = max(0.5, 1.0 - (skill - SKILL_REFERENCE))
    s_instrument = instrument_sigma_nm(instrument) * factor
    s_horizon = HORIZON_SIGMA_NM
    if conditions is not None and conditions.sky == "hazy":
        s_horizon += HAZE_HORIZON_NM
    sea = getattr(world, "sea", None)
    if sea is not None:
        s_horizon += HORIZON_SEA_NM_PER_M * float(sea.reading().height_m)
    sigma = math.hypot(s_instrument, s_horizon)
    error_nm = stream.gauss(0.0, sigma)
    lat = pos.lat_deg + error_nm / 60.0
    return NoonResult(Sight(lat, instrument, sigma, world.clock.tick), "")


# ---------------------------------------------------------------------------
# The chronometer (package 33b; spec M5 §14; N §2, §3, §4(b))
# ---------------------------------------------------------------------------

# A marine chronometer of the period is a two-day movement, wound daily and run down
# after about fifty-six hours (judgement: the common two-day box chronometer; no page
# read for the hours). The master winds it at eight in the morning, when the watch is
# relieved: "8:00 A.M. Relieve watch, wheel and look-out, report chronometers wound"
# (Luce 1884, ch. XX, the ship's routine at sea).
CHRONOMETER_RUN_HOURS = 56.0
CHRONOMETER_WIND_HOUR = 8
# The rating ashore leaves "a one-time offset from the rating" (N §3): two seconds one
# sigma, drawn once (judgement on the words).
RATING_OFFSET_SIGMA_S = 2.0
# The true rate's drift from the certificate's, "rate wrong by 1 to 3 seconds a day
# (Bligh's K2)" (N §3; Bligh logged K2 "between 1.1 and three seconds" a day, N §2), drawn
# once per chronometer in either sense when the scenario says `drift: seeded`; a stated
# number is the drift itself, and none is a rate that is right.
RATE_DRIFT_MIN_S_PER_DAY = 1.0
RATE_DRIFT_MAX_S_PER_DAY = 3.0
# The master's trust in his chronometer widens with the days since rating by a second a
# day (judgement: the low end of N §3's "one to three"; four seconds of time is a mile of
# longitude at the equator, two-thirds of a mile at 50 N, N §2).
RATE_DOUBT_S_PER_DAY = 1.0
# Under this much the master finds no fault in the chronometer by a lunar (judgement: a
# lunar's own half-minute of arc is a minute of time, N §2).
CHRONOMETER_FAULT_S = 20.0

# The time sight: "the sight's own two or three miles" (N §4(b)), one sigma; the sun
# above ten degrees (judgement: refraction uncertain low down) and more than an hour and
# a half from the meridian, where the hour angle changes slowly against the altitude (a
# morning or afternoon sight, N §4(b); the guard a judgement); the master below twenty
# minutes working it (judgement: Norie's tables open on the table).
TIME_SIGHT_SIGMA_NM = 2.5
TIME_SIGHT_MIN_ALTITUDE_DEG = 10.0
TIME_SIGHT_NOON_GUARD_H = 1.5
TIME_SIGHT_WORK_MINUTES = 20

# The lunar (N §2, §4(c), §5). The moon "well clear of the horizon", fifteen degrees
# (N §4(c), "more than, say, fifteen degrees high"); no lunar within three days of new
# moon ("near new moon there is no lunar for three or four days", N §2; truth 61); a body
# at a tabulated distance, the sun "between roughly 40 and 120 degrees from the moon by
# day" (N §4(c)) and a star by night at the same range (judgement); the body above ten
# degrees for its altitude (judgement). A quarter of an hour on deck with the sextant
# for a set of distances (N §2) and the clearing below in an hour: "half an hour to an
# hour of arithmetic", a figure the study marks UNVERIFIED (no 1805 diary timing it;
# the twenty minutes a modern practitioner's), so this constant is provisional and says
# so in TuningNotes. The spread: a quarter of a degree for a good master on a quiet day,
# a degree for a poor one in a seaway (N §2, §4(c): "10 to 39 miles at 50 N"); the skill
# ends are the ship files' deck skills (judgement); the seaway doubles the spread at two
# metres of sea (judgement); the moon's rate against the body, half a degree an hour
# against the stars (N §2), widens it when the distance closes slowly. The master's
# stated trust is two sigma ("which Mr. Ellis would trust within twenty miles").
LUNAR_MOON_MIN_ALTITUDE_DEG = 15.0
LUNAR_MIN_AGE_DAYS = 3.0
LUNAR_DISTANCE_MIN_DEG = 40.0
LUNAR_DISTANCE_MAX_DEG = 120.0
LUNAR_BODY_MIN_ALTITUDE_DEG = 10.0
LUNAR_ON_DECK_MINUTES = 15
LUNAR_CLEARING_MINUTES = 60
LUNAR_SIGMA_GOOD_DEG = 0.25
LUNAR_SIGMA_POOR_DEG = 1.0
LUNAR_SKILL_GOOD = 0.9
LUNAR_SKILL_POOR = 0.5
LUNAR_SEA_M = 2.0
LUNAR_RATE_REFERENCE_DEG_PER_H = 0.5
LUNAR_TRUST_SIGMAS = 2.0

# The amplitude and the azimuth (decision 30; N §3: "an azimuth observation gets it to a
# degree"; Falconer 1780, 'Azimuth-compass': the brass edge "divided into degrees and
# halves"). The amplitude is taken with the sun's centre about the horizon, between a
# degree and a half under and three above (judgement: a quarter of an hour either side
# of sunrise and sunset); a degree one sigma. The azimuth by day wants the sun's altitude
# worked too and is a little worse, a degree and a half (judgement), with the sun above
# five degrees and an hour or more from the meridian, where its bearing changes fastest
# against the altitude (judgement).
AMPLITUDE_ELEVATION_DEG = (-1.5, 3.0)
AMPLITUDE_SIGMA_DEG = 1.0
AZIMUTH_SIGMA_DEG = 1.5
AZIMUTH_MIN_ALTITUDE_DEG = 5.0
AZIMUTH_NOON_GUARD_H = 1.0

# A moonlit night for the lookout (spec §14, "the night's light"): the moon up ten
# degrees and more than half lit (judgement).
MOONLIT_MIN_ALTITUDE_DEG = 10.0
MOONLIT_FRACTION = 0.5

_SECONDS_PER_DEG = 240.0  # four minutes of time to a degree of longitude


def greenwich_time(world: Any, when: datetime | None = None) -> datetime:
    """Greenwich mean time for a moment of the ship's clock, which keeps the mean time
    of the meridian she started on (`core/sun.py`): the clock plus the start meridian's
    westing in time; the clock itself on the plane."""
    t = world.clock.ship_time if when is None else when
    origin = getattr(world, "origin", None)
    if origin is None:
        return t
    return t - timedelta(hours=origin.lon_deg / 15.0)


def moon_now(world: Any) -> Moon | None:
    """The moon over the ship now (`core.moon.moon_at`); None on the plane."""
    pos = getattr(world, "position", None)
    if pos is None:
        return None
    return moon_at(greenwich_time(world), pos.lat_deg, pos.lon_deg)


def moonlit(moon: Moon | None) -> bool:
    """Whether the night is moonlit: the moon up and more than half full."""
    return (
        moon is not None
        and moon.altitude_deg >= MOONLIT_MIN_ALTITUDE_DEG
        and moon.fraction >= MOONLIT_FRACTION
    )


@dataclass
class Chronometer:
    """The captain's chronometer: its maker, the day it was rated ashore and the rate
    on its certificate (what the master applies), the true rate's drift from it and the
    rating's offset (what the world keeps and nobody aboard knows), when it was last
    wound, and whether it is going."""

    maker: str
    rated: date
    rate_s_per_day: float  # the certificate's
    drift_s_per_day: float  # the truth's departure from the certificate
    offset_s: float  # the rating's own error
    wound_at: datetime
    going: bool = True
    set_error_s: float = 0.0  # set at sea by the account after running down
    forgotten: tuple[date, ...] = ()  # the days the master forgets to wind it (scenario)
    wound_days: list[date] = field(default_factory=list)
    where: str = ""  # where it was rated: "Plymouth"

    @classmethod
    def from_scenario(
        cls, spec: dict[str, Any], start: datetime, stream: random.Random
    ) -> Chronometer:
        """From the scenario's `chronometer:` item; the drift and the offset drawn from
        the `chronometer` stream when the scenario says `drift: seeded`."""
        rated = spec.get("rated")
        rated_day = (
            rated if isinstance(rated, date) else date.fromisoformat(str(rated or start.date()))
        )
        drift = spec.get("drift", "seeded")
        if isinstance(drift, str) and drift.strip().lower() == "seeded":
            sense = 1.0 if stream.random() < 0.5 else -1.0
            drift_s = sense * stream.uniform(RATE_DRIFT_MIN_S_PER_DAY, RATE_DRIFT_MAX_S_PER_DAY)
        else:
            drift_s = float(drift or 0.0)
        offset = stream.gauss(0.0, RATING_OFFSET_SIGMA_S)
        forgotten = tuple(
            d if isinstance(d, date) else date.fromisoformat(str(d))
            for d in (spec.get("forgotten") or ())
        )
        return cls(
            maker=str(spec.get("maker") or "the chronometer"),
            rated=rated_day,
            rate_s_per_day=float(spec.get("rate_s_per_day", 0.0) or 0.0),
            drift_s_per_day=drift_s,
            offset_s=offset,
            wound_at=start,
            forgotten=forgotten,
            where=str(spec.get("where") or ""),
        )

    @property
    def name(self) -> str:
        return self.maker if self.maker.lower().startswith("the ") else f"the {self.maker}"

    def days_since_rated(self, when: datetime) -> float:
        rated = datetime(self.rated.year, self.rated.month, self.rated.day)
        return (when - rated).total_seconds() / 86400.0

    def error_s(self, when: datetime) -> float:
        """What the master's Greenwich time by this chronometer, the certificate's rate
        allowed, is out by: positive is fast."""
        return self.offset_s + self.drift_s_per_day * self.days_since_rated(when) + self.set_error_s

    def masters_gmt(self, gmt_true: datetime, when: datetime) -> datetime:
        return gmt_true + timedelta(seconds=self.error_s(when))

    def doubt_nm(self, when: datetime, lat_deg: float) -> float:
        """The master's trust in it, one sigma in miles of longitude at the latitude: a
        second a day since rating (`RATE_DOUBT_S_PER_DAY`)."""
        seconds = RATE_DOUBT_S_PER_DAY * max(0.0, self.days_since_rated(when))
        return seconds / _SECONDS_PER_DEG * 60.0 * math.cos(math.radians(lat_deg))

    def wind(self, now: datetime) -> str:
        """Wound: the line (a chronometer that had run down is set going again by
        `Navigation.wind_chronometer`, which sets its error from the account)."""
        self.wound_at = now
        if now.date() not in self.wound_days:
            self.wound_days.append(now.date())
        return f"Wound {self.name}."

    def tick(self, now: datetime) -> str | None:
        """The master winds it at eight in the morning unless the scenario has him
        forget; run down past its hours it stops, and the line says so once."""
        if (
            self.going
            and now.hour == CHRONOMETER_WIND_HOUR
            and now.minute == 0
            and now.second == 0
            and now.date() not in self.wound_days
            and now.date() not in self.forgotten
        ):
            return self.wind(now)
        if self.going and (now - self.wound_at).total_seconds() > CHRONOMETER_RUN_HOURS * 3600.0:
            self.going = False
            return f"{_head(self.name)} has run down: it was not wound."
        return None

    def words(self, world: Any) -> str:
        """`the chronometer`: its time at Greenwich as the master reads it, the days
        since rating, and its winding."""
        now = world.clock.ship_time
        days = int(self.days_since_rated(now))
        if not self.going:
            return f"{self.name} is dead, not having been wound; {days} days from its rating"
        gmt = self.masters_gmt(greenwich_time(world), now)
        since = (now - self.wound_at).total_seconds()
        if self.wound_at.date() == now.date():
            wound = "wound this morning"
        elif since <= 36 * 3600:
            wound = "wound yesterday"
        else:
            wound = "not wound since the day before yesterday"
        return (
            f"{self.name} reads {gmt:%Hh %Mm %Ss} at Greenwich, {days} days from its rating, "
            f"{wound}"
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "maker": self.maker,
            "rated": self.rated.isoformat(),
            "rate_s_per_day": self.rate_s_per_day,
            "going": self.going,
            "wound_at": self.wound_at.isoformat(),
        }


def _head(name: str) -> str:
    return name[:1].upper() + name[1:]


# ---------------------------------------------------------------------------
# The time sight
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TimeSight:
    """A longitude by chronometer as the master reports it: the longitude, his trust in
    it (one sigma, miles), the days since rating, and the moment."""

    longitude_deg: float
    sigma_nm: float
    days_since_rated: int
    tick: int
    forenoon: bool

    @property
    def words(self) -> str:
        return _lon_words(self.longitude_deg)

    def to_dict(self) -> dict[str, Any]:
        return {
            "longitude_deg": round(self.longitude_deg, 5),
            "sigma_nm": round(self.sigma_nm, 2),
            "days_since_rated": self.days_since_rated,
            "tick": self.tick,
            "forenoon": self.forenoon,
        }


def _lon_words(lon_deg: float) -> str:
    return format_position(Position(0.0, lon_deg)).split(", ")[1]


def _skill_factor(master: Any) -> float:
    skill = float(getattr(master, "skill", 0.7))
    return max(0.5, 1.0 - (skill - SKILL_REFERENCE))


def _sun_hours_from_noon(world: Any) -> float:
    """How many hours the ship's clock stands from the sun's meridian passage today."""
    t = world.clock.ship_time
    transit = world._sun_now().transit(t, world.ship_x)
    return abs((t - transit).total_seconds()) / 3600.0


def time_sight(
    world: Any, master: Any, chronometer: Chronometer | None, stream: random.Random
) -> tuple[TimeSight | None, str]:
    """`take a sight for the longitude`: the sight, or the refusal's words."""
    if chronometer is None:
        return None, "there is no chronometer aboard; the longitude is by account and by lunar"
    if not chronometer.going:
        return None, f"{chronometer.name} is dead, not having been wound"
    conditions = getattr(world, "conditions", None)
    allowed, why = sky_allows(conditions)
    if not allowed:
        return None, why.replace(" at noon", "")
    pos = world.position
    if pos is None:
        return None, "no sea to take a sight on"
    t = world.clock.ship_time
    altitude = world._sun_now().elevation_deg(t, world.ship_x)
    if altitude < TIME_SIGHT_MIN_ALTITUDE_DEG:
        return None, "the sun is too low for a time sight"
    if _sun_hours_from_noon(world) < TIME_SIGHT_NOON_GUARD_H:
        return None, "the sun is too near the meridian for a time sight; wait for the afternoon"
    lat = pos.lat_deg
    sigma_nm = TIME_SIGHT_SIGMA_NM * _skill_factor(master)
    lon = chronometer_longitude(world, master, chronometer, stream)
    trust = math.hypot(sigma_nm, chronometer.doubt_nm(t, lat))
    days = int(chronometer.days_since_rated(t))
    transit = world._sun_now().transit(t, world.ship_x)
    return TimeSight(lon, trust, days, world.clock.tick, t < transit), ""


def chronometer_longitude(
    world: Any, master: Any, chronometer: Chronometer, stream: random.Random
) -> float:
    """The longitude the chronometer gives at this moment, drawn: the truth plus the
    chronometer's error in time (fast is west) plus the sight's own miles."""
    pos = world.position
    t = world.clock.ship_time
    minute_nm = math.cos(math.radians(pos.lat_deg))  # a minute of longitude in miles here
    sigma_nm = TIME_SIGHT_SIGMA_NM * _skill_factor(master)
    error_deg = -chronometer.error_s(t) / _SECONDS_PER_DEG
    error_deg += stream.gauss(0.0, sigma_nm) / (60.0 * minute_nm)
    return pos.lon_deg + error_deg


# ---------------------------------------------------------------------------
# The lunar
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Lunar:
    """A longitude by lunar as the master reports it: the body, the longitude, his trust
    (one sigma, miles), the moment the distances were taken and the chronometer's
    longitude at that moment if there was one, for the error by lunar."""

    body: str
    longitude_deg: float
    sigma_nm: float
    tick: int
    chronometer_longitude_deg: float | None

    @property
    def words(self) -> str:
        return _lon_words(self.longitude_deg)

    @property
    def trust_words(self) -> str:
        miles = max(5, int(5 * round(LUNAR_TRUST_SIGMAS * self.sigma_nm / 5.0)))
        return f"within {miles} miles"

    @property
    def chronometer_fast_s(self) -> float | None:
        """How far the chronometer is fast by this lunar, in seconds of time (negative
        is slow): a chronometer's longitude west of the lunar's is a fast chronometer."""
        if self.chronometer_longitude_deg is None:
            return None
        return (self.longitude_deg - self.chronometer_longitude_deg) * _SECONDS_PER_DEG

    def to_dict(self) -> dict[str, Any]:
        return {
            "body": self.body,
            "longitude_deg": round(self.longitude_deg, 5),
            "sigma_nm": round(self.sigma_nm, 2),
            "tick": self.tick,
            "chronometer_longitude_deg": (
                None
                if self.chronometer_longitude_deg is None
                else round(self.chronometer_longitude_deg, 5)
            ),
        }


def lunar_body(world: Any, moon: Moon | None, asked: str | None) -> tuple[str | None, str]:
    """The body for a lunar now, or the refusal in the registry's words ("No lunar to be
    had: the moon is two days old"). `asked` is "the sun", a star's name, or None for
    whatever serves: the sun by day, the highest star in distance by night."""
    if moon is None:
        return None, "there is no sea to take a lunar on"
    conditions = getattr(world, "conditions", None)
    allowed, _why = sky_allows(conditions)
    if not allowed:
        weather = getattr(conditions, "weather", "")
        what = (
            f"the sky is thick with {weather}"
            if weather in WEATHER_HIDES_THE_SUN
            else "the sky is thick"
        )
        return None, f"No lunar to be had: {what}"
    age = moon.age_days
    from_change = LUNATION_DAYS - age
    if age < LUNAR_MIN_AGE_DAYS or from_change < LUNAR_MIN_AGE_DAYS:
        young = age < LUNAR_MIN_AGE_DAYS
        n = int(round(age if young else from_change))
        days = "a day" if n <= 1 else f"{_small(n)} days"
        side = "old" if young else "from the change"
        return None, f"No lunar to be had: the moon is {days} {side}"
    if moon.altitude_deg <= 0.0:
        return None, "No lunar to be had: the moon is down"
    if moon.altitude_deg < LUNAR_MOON_MIN_ALTITUDE_DEG:
        return None, (
            f"No lunar to be had: the moon is too low, {_small(int(round(moon.altitude_deg)))} "
            f"degrees up"
        )
    key = (asked or "").strip().lower()
    for word in ("of ", "the "):
        if key.startswith(word):
            key = key[len(word) :].strip()
    sun_ok = (
        moon.sun_altitude_deg >= LUNAR_BODY_MIN_ALTITUDE_DEG
        and LUNAR_DISTANCE_MIN_DEG <= moon.sun_distance_deg <= LUNAR_DISTANCE_MAX_DEG
    )
    night = moon.sun_altitude_deg < 0.0
    stars = {
        name: (dist, alt)
        for name, (dist, alt) in moon.stars.items()
        if night
        and alt >= LUNAR_BODY_MIN_ALTITUDE_DEG
        and LUNAR_DISTANCE_MIN_DEG <= dist <= LUNAR_DISTANCE_MAX_DEG
    }
    if key in ("", "sun", "a star", "star"):
        if key not in ("a star", "star") and sun_ok:
            return "the sun", ""
        if stars:
            return max(stars, key=lambda n: stars[n][1]), ""
        if not night:
            return None, (
                f"No lunar to be had: the sun is not in distance, "
                f"{_small(int(round(moon.sun_distance_deg)))} degrees from the moon"
            )
        return None, "No lunar to be had: no star in distance of the moon is up"
    names = {n.lower(): n for n in LUNAR_STARS}
    if key not in names:
        known = ", ".join(LUNAR_STARS)
        return None, f"The Almanac has no distances for {asked!r}; its stars are {known}"
    name = names[key]
    if not night:
        return None, f"No lunar to be had of {name} by day; the sun is up"
    dist, alt = moon.stars[name]
    if alt < LUNAR_BODY_MIN_ALTITUDE_DEG:
        return None, f"No lunar to be had: {name} is not up"
    if not LUNAR_DISTANCE_MIN_DEG <= dist <= LUNAR_DISTANCE_MAX_DEG:
        return None, (
            f"No lunar to be had: {name} is not in distance, {_small(int(round(dist)))} "
            f"degrees from the moon"
        )
    return name, ""


def _small(n: int) -> str:
    from freesail.world.reckoning import number_words

    return number_words(n)


def lunar_result(
    world: Any,
    master: Any,
    stream: random.Random,
    body: str,
    chronometer_lon_deg: float | None,
) -> Lunar:
    """The lunar's result, drawn and not computed: the true longitude plus an error from
    the seed with a spread set by the master's skill, the sea's height and the moon's
    rate against the body."""
    pos = world.position
    skill = float(getattr(master, "skill", 0.7))
    span = LUNAR_SKILL_GOOD - LUNAR_SKILL_POOR
    # a good master at the good spread; a poor one in a seaway at the poor one, half of
    # it the skill's and half the sea's
    poor_over_good = LUNAR_SIGMA_POOR_DEG / LUNAR_SIGMA_GOOD_DEG
    skill_factor = 1.0 + max(0.0, LUNAR_SKILL_GOOD - skill) / span * (poor_over_good / 2.0 - 1.0)
    sea = getattr(world, "sea", None)
    height = float(sea.reading().height_m) if sea is not None else 0.0
    sea_factor = 1.0 + height / LUNAR_SEA_M
    gmt = greenwich_time(world)
    now = moon_at(gmt, pos.lat_deg, pos.lon_deg)
    later = moon_at(gmt + timedelta(hours=1), pos.lat_deg, pos.lon_deg)
    if body == "the sun":
        rate = abs(later.sun_distance_deg - now.sun_distance_deg)
    else:
        rate = abs(later.stars[body][0] - now.stars[body][0])
    rate_factor = min(2.0, max(1.0, LUNAR_RATE_REFERENCE_DEG_PER_H / max(rate, 1e-3)))
    sigma_deg = LUNAR_SIGMA_GOOD_DEG * skill_factor * sea_factor * rate_factor
    lon = pos.lon_deg + stream.gauss(0.0, sigma_deg)
    sigma_nm = sigma_deg * 60.0 * math.cos(math.radians(pos.lat_deg))
    return Lunar(body, lon, sigma_nm, world.clock.tick, chronometer_lon_deg)


# ---------------------------------------------------------------------------
# The variation by observation
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Variation:
    """The variation the master allows: the chart's, or his own by observation."""

    deg_west: float
    by: str  # "the chart of 1794", "amplitude", "azimuth"
    day: date | None = None

    @property
    def words(self) -> str:
        v = abs(self.deg_west)
        d, m = divmod(round(v * 2) / 2.0, 1.0)
        minutes = " 30'" if m else ""
        side = "W" if self.deg_west >= 0 else "E"
        when = f", {self.day.day} {self.day:%B}" if self.day is not None else ""
        return f"{int(d)}°{minutes} {side} by {self.by}{when}"

    def to_dict(self) -> dict[str, Any]:
        return {
            "deg_west": self.deg_west,
            "by": self.by,
            "day": None if self.day is None else self.day.isoformat(),
            "words": self.words,
        }


def amplitude_or_azimuth(
    world: Any, errors: Any, stream: random.Random, amplitude: bool, true_variation_deg: float
) -> tuple[Variation | None, str, dict[str, Any]]:
    """`observe an amplitude` at sunrise or sunset, or `observe an azimuth` by day: the
    sun's bearing by compass against its true bearing gives the variation to a degree
    (N §3). Returns (the variation, the refusal, the figures)."""
    conditions = getattr(world, "conditions", None)
    allowed, why = sky_allows(conditions)
    if not allowed:
        return None, why.replace(" at noon", ""), {}
    pos = world.position
    if pos is None:
        return None, "no sea to observe the sun on", {}
    t = world.clock.ship_time
    sun = moon_at(greenwich_time(world), pos.lat_deg, pos.lon_deg)
    altitude = world._sun_now().elevation_deg(t, world.ship_x)
    if amplitude:
        lo, hi = AMPLITUDE_ELEVATION_DEG
        if not lo <= altitude <= hi:
            where = "under the horizon" if altitude < lo else "well up"
            return None, f"the sun is {where}; an amplitude is taken as it rises or sets", {}
        sigma = AMPLITUDE_SIGMA_DEG
    else:
        if altitude < AZIMUTH_MIN_ALTITUDE_DEG:
            return None, "the sun is too low for an azimuth", {}
        if _sun_hours_from_noon(world) < AZIMUTH_NOON_GUARD_H:
            return None, "the sun is too near the meridian for an azimuth", {}
        sigma = AZIMUTH_SIGMA_DEG
    heading = float(world.ship.heading)
    true_bearing = sun.sun_azimuth_deg
    by_compass = (
        true_bearing + true_variation_deg + errors.deviation_deg(heading) + stream.gauss(0.0, sigma)
    ) % 360.0
    found = (by_compass - true_bearing + 180.0) % 360.0 - 180.0
    found = round(found * 2.0) / 2.0  # the brass edge divided into degrees and halves
    rising = sun.sun_azimuth_deg < 180.0
    var = Variation(found, "amplitude" if amplitude else "azimuth", t.date())
    data = {
        "true_bearing_deg": round(true_bearing, 1),
        "compass_bearing_deg": round(by_compass, 1),
        "altitude_deg": round(altitude, 2),
        "rising": rising,
    }
    return var, "", data
