"""The sun (spec M4 §5): sunrise, sunset and civil twilight from the date and the ship's
latitude, and the `daylight` reading behind `is day`, `is twilight`, `is night`.

Source: the NOAA Global Monitoring Laboratory's "General Solar Position Calculations"
(the equations behind the NOAA Solar Calculator, gml.noaa.gov/grad/solcalc), which are
Spencer's 1971 Fourier series in the day of the year for the sun's declination and the
equation of time, and the hour angle of sunrise from

    cos(ha) = cos(zenith) / (cos(lat) cos(decl)) - tan(lat) tan(decl)

with the zenith 90.833° for sunrise and sunset (the sun's upper limb on the horizon:
refraction 0.567° and the semi-diameter 0.267°) and 96° for civil twilight. NOAA gives
the series' accuracy as within a minute or two of the almanac between 1901 and 2099, and
a few minutes is plenty for a ship (spec §5); 1805 is outside that span by a century,
which is worth well under a minute at these latitudes. The equation of time is
*included*: it is part of the same series and moves sunrise and sunset by up to a quarter
of an hour through the year.

Time. The ship's clock keeps the mean time of the meridian she started on, as a ship's
deck clock does; it is not reset as she sails. Her longitude is her east-west position
(`ship_x`, metres east of the start) turned to degrees at the scenario's latitude, so the
sun rises four minutes of clock time earlier for every degree she has made to the east.
On the endless plane longitude is zero at the start. NOAA's formulas take longitude east
positive and give the result in the time of a stated meridian, which is what the clock is.

Daylight is read from the sun's elevation at the moment (`phase`): *day* above -0.833°,
*twilight* between that and -6° (civil twilight, morning and evening), *night* below. The
World raises `sun.rise` and `sun.set` on the tick the phase crosses into and out of day,
so an `at sunrise` order fires on the sun's own tick; the same declination and equation
of time give `times`, the clock times of the day's dawn, sunrise, sunset and dusk, for the
console and the tuning notes. At a latitude where the sun does not set (or does not rise)
that day, `times` says so in a sentence and there is no crossing and no event.
"""

from __future__ import annotations

import calendar
import math
from dataclasses import dataclass
from datetime import date, datetime, timedelta

from freesail import units

__all__ = [
    "CIVIL_TWILIGHT_ZENITH_DEG",
    "DAY",
    "DEFAULT_LATITUDE_DEG",
    "METRES_PER_DEGREE",
    "NIGHT",
    "SUNRISE_ZENITH_DEG",
    "TWILIGHT",
    "Sun",
    "SunTimes",
    "declination_and_equation_of_time",
]

# The Channel: spec M4 §5's default latitude for the scenario.
DEFAULT_LATITUDE_DEG = 50.0

# The sun's zenith angle at sunrise and sunset: 90° plus refraction (0.567°) plus the
# semi-diameter (0.267°), the upper limb on the sea horizon (NOAA, "General Solar
# Position Calculations"; the Nautical Almanac's convention).
SUNRISE_ZENITH_DEG = 90.833
# Civil twilight: the sun's centre 6° below the horizon (NOAA; the Nautical Almanac).
CIVIL_TWILIGHT_ZENITH_DEG = 96.0

# A degree of latitude, and of longitude at the equator: sixty nautical miles of 1852 m
# (the nautical mile is a minute of arc of the meridian, units.nm_to_m).
METRES_PER_DEGREE = 60.0 * units.nm_to_m(1.0)

DAY = "day"
TWILIGHT = "twilight"
NIGHT = "night"


def declination_and_equation_of_time(when: datetime) -> tuple[float, float]:
    """The sun's declination (radians) and the equation of time (minutes) at `when`,
    by Spencer's series as NOAA gives them. The fractional year takes the hour, so the
    elevation is continuous through the day."""
    days_in_year = 366 if calendar.isleap(when.year) else 365
    day_of_year = when.timetuple().tm_yday
    hour = when.hour + when.minute / 60.0 + when.second / 3600.0
    gamma = 2.0 * math.pi / days_in_year * (day_of_year - 1 + (hour - 12.0) / 24.0)
    eqtime = 229.18 * (
        0.000075
        + 0.001868 * math.cos(gamma)
        - 0.032077 * math.sin(gamma)
        - 0.014615 * math.cos(2 * gamma)
        - 0.040849 * math.sin(2 * gamma)
    )
    decl = (
        0.006918
        - 0.399912 * math.cos(gamma)
        + 0.070257 * math.sin(gamma)
        - 0.006758 * math.cos(2 * gamma)
        + 0.000907 * math.sin(2 * gamma)
        - 0.002697 * math.cos(3 * gamma)
        + 0.00148 * math.sin(3 * gamma)
    )
    return decl, eqtime


@dataclass(frozen=True)
class SunTimes:
    """The clock times of one day's civil dawn, sunrise, sunset and civil dusk. A time
    is None when the sun does not cross that altitude that day; `sentence` says why."""

    day: date
    dawn: datetime | None
    sunrise: datetime | None
    sunset: datetime | None
    dusk: datetime | None
    sentence: str | None = None

    def describe(self) -> str:
        if self.sentence:
            return self.sentence
        assert self.sunrise and self.sunset and self.dawn and self.dusk
        return (
            f"Sunrise {self.sunrise:%H:%M}, sunset {self.sunset:%H:%M}; "
            f"civil twilight from {self.dawn:%H:%M} and until {self.dusk:%H:%M}."
        )


@dataclass(frozen=True)
class Sun:
    """The sun over a ship at one latitude. Pure functions of the time and the ship's
    easting, so two runs give one log."""

    latitude_deg: float = DEFAULT_LATITUDE_DEG

    def longitude_deg(self, ship_x_m: float = 0.0) -> float:
        """Degrees east of the start meridian for `ship_x_m` metres east, at this
        latitude (a degree of longitude shrinks with the cosine of the latitude)."""
        scale = math.cos(math.radians(self.latitude_deg))
        if scale < 1e-9:
            return 0.0  # at the pole every direction is south; the clock's meridian stands
        return ship_x_m / (METRES_PER_DEGREE * scale)

    # -- the moment ------------------------------------------------------------------------

    def elevation_deg(self, when: datetime, ship_x_m: float = 0.0) -> float:
        """The sun's elevation above the horizon in degrees at `when` (clock time)."""
        decl, eqtime = declination_and_equation_of_time(when)
        minutes = when.hour * 60.0 + when.minute + when.second / 60.0
        true_solar = minutes + eqtime + 4.0 * self.longitude_deg(ship_x_m)
        hour_angle = math.radians(true_solar / 4.0 - 180.0)
        lat = math.radians(self.latitude_deg)
        cos_zenith = math.sin(lat) * math.sin(decl) + math.cos(lat) * math.cos(decl) * math.cos(
            hour_angle
        )
        cos_zenith = max(-1.0, min(1.0, cos_zenith))
        return 90.0 - math.degrees(math.acos(cos_zenith))

    def phase(self, when: datetime, ship_x_m: float = 0.0) -> str:
        """'day', 'twilight' or 'night' at `when`: the `daylight` reading."""
        elevation = self.elevation_deg(when, ship_x_m)
        if elevation > 90.0 - SUNRISE_ZENITH_DEG:
            return DAY
        if elevation > 90.0 - CIVIL_TWILIGHT_ZENITH_DEG:
            return TWILIGHT
        return NIGHT

    # -- the day ---------------------------------------------------------------------------

    def _hour_angle_deg(self, zenith_deg: float, decl: float) -> float | None:
        lat = math.radians(self.latitude_deg)
        denominator = math.cos(lat) * math.cos(decl)
        if abs(denominator) < 1e-12:
            return None
        cos_ha = math.cos(math.radians(zenith_deg)) / denominator - math.tan(lat) * math.tan(decl)
        if cos_ha < -1.0 or cos_ha > 1.0:
            return None  # the sun never reaches that altitude today
        return math.degrees(math.acos(cos_ha))

    def transit(self, day: date | datetime, ship_x_m: float = 0.0) -> datetime:
        """The sun's meridian passage on `day` in clock time: the ship's noon, when the
        log-book's page turns and the latitude is taken (spec M5 §14; package 33a). From
        the equation of time at that day's noon and the ship's easting, as `times` has it:
        720 minutes less the longitude's four minutes a degree and the equation."""
        d = day.date() if isinstance(day, datetime) else day
        noon = datetime(d.year, d.month, d.day, 12, 0, 0)
        _, eqtime = declination_and_equation_of_time(noon)
        minutes = 720.0 - 4.0 * self.longitude_deg(ship_x_m) - eqtime
        return datetime(d.year, d.month, d.day) + timedelta(seconds=round(minutes * 60.0))

    def meridian_altitude_deg(self, day: date | datetime) -> float:
        """The sun's altitude at its meridian passage on `day`: 90° less the difference of
        the latitude and the declination, the arithmetic of the noon sight (Falconer 1780,
        'Quadrant'; the master's, not the game's, which draws the sight's outcome)."""
        d = day.date() if isinstance(day, datetime) else day
        noon = datetime(d.year, d.month, d.day, 12, 0, 0)
        decl, _ = declination_and_equation_of_time(noon)
        return 90.0 - abs(self.latitude_deg - math.degrees(decl))

    def times(self, day: date | datetime, ship_x_m: float = 0.0) -> SunTimes:
        """Dawn, sunrise, sunset and dusk on `day`, in clock time, from the declination
        and equation of time at that day's noon (NOAA's simplification, good to a
        minute at these latitudes)."""
        d = day.date() if isinstance(day, datetime) else day
        noon = datetime(d.year, d.month, d.day, 12, 0, 0)
        decl, eqtime = declination_and_equation_of_time(noon)
        lon = self.longitude_deg(ship_x_m)
        midnight = datetime(d.year, d.month, d.day)

        def at(minutes: float) -> datetime:
            return midnight + timedelta(minutes=minutes)

        ha_rise = self._hour_angle_deg(SUNRISE_ZENITH_DEG, decl)
        ha_dawn = self._hour_angle_deg(CIVIL_TWILIGHT_ZENITH_DEG, decl)
        if ha_rise is None:
            up = self.elevation_deg(noon, ship_x_m) > 90.0 - SUNRISE_ZENITH_DEG
            words = (
                "The sun does not set today at this latitude."
                if up
                else "The sun does not rise today at this latitude."
            )
            return SunTimes(d, None, None, None, None, words)
        sunrise = at(720.0 - 4.0 * (lon + ha_rise) - eqtime)
        sunset = at(720.0 - 4.0 * (lon - ha_rise) - eqtime)
        if ha_dawn is None:
            # the sun sets but never gets six degrees under: twilight all night
            return SunTimes(
                d,
                None,
                sunrise,
                sunset,
                None,
                f"Sunrise {sunrise:%H:%M}, sunset {sunset:%H:%M}; twilight lasts the night "
                "at this latitude.",
            )
        dawn = at(720.0 - 4.0 * (lon + ha_dawn) - eqtime)
        dusk = at(720.0 - 4.0 * (lon - ha_dawn) - eqtime)
        return SunTimes(d, dawn, sunrise, sunset, dusk)
