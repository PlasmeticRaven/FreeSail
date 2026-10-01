"""The moon (spec M5 §14; package 33b): a low-precision moon good to a degree, for the
lunar's conditions, the night's light and the tide's age (package 34).

Meeus, *Astronomical Algorithms* (2nd ed., 1998), by chapter: the moon's mean elements
(ch. 47, eq. 47.1 to 47.6) and the leading terms of its longitude and latitude (Table
47.A and 47.B, the twenty-four and thirteen largest, which leave the position within a
few hundredths of a degree); the sun's geometric longitude (ch. 25, eq. 25.2 to 25.5, the
low-accuracy method); the obliquity's first two terms (ch. 22, eq. 22.2); the ecliptic to
the equator (ch. 13, eq. 13.3 and 13.4); the sidereal time at Greenwich (ch. 12, eq. 12.4);
the altitude and azimuth (ch. 13, eq. 13.5 and 13.6, the azimuth here from the north);
the angular separation (ch. 17, eq. 17.1); the mean lunation for the moon's age (ch. 49,
eq. 49.1, 29.530588861 days); the illuminated fraction (ch. 48, eq. 48.1 and 48.2); and
the stars' precession from J2000 (ch. 21, eq. 21.4, the approximate form). The Julian Day
from the calendar date is ch. 7, eq. 7.1. Nutation, aberration, the moon's distance and
its parallax are left out: a degree is the brief's accuracy, and the engine never clears
a distance (the lunar's result is drawn, `freesail.world.sights`). The time wanted is
Universal Time; the World's clock keeps the mean time of the meridian she started on,
and `freesail.world.sights` converts.

The lunar stars are the nine the *Nautical Almanac* tabulated distances for (the sun
beside them; N §2, de Grijs 2020 §5): their J2000 places from memory of the catalogue
and not read from a page (unverified; a tenth of a degree would not matter here).
Checked against the JPL Horizons ephemeris for June 1805 and against Meeus's example
47.a (`tests/test_moon.py`; `docs/dev/TuningNotes.md`, package 33b).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime

__all__ = ["LUNAR_STARS", "LUNATION_DAYS", "Moon", "julian_day", "moon_at", "phase_words"]

LUNATION_DAYS = 29.530588861  # Meeus ch. 49, eq. 49.1: the mean synodic month
# The nine lunar stars, J2000 right ascension and declination in degrees.
LUNAR_STARS: dict[str, tuple[float, float]] = {
    "Hamal": (31.793, 23.462),
    "Aldebaran": (68.980, 16.509),
    "Pollux": (116.329, 28.026),
    "Regulus": (152.093, 11.967),
    "Spica": (201.298, -11.161),
    "Antares": (247.352, -26.432),
    "Altair": (297.696, 8.868),
    "Fomalhaut": (344.413, -29.622),
    "Markab": (346.190, 15.205),
}
_LON_TERMS = (  # Table 47.A: (D, M, M', F, coefficient × 1e-6 degrees), E on the M terms
    (0, 0, 1, 0, 6288774), (2, 0, -1, 0, 1274027), (2, 0, 0, 0, 658314), (0, 0, 2, 0, 213618),
    (0, 1, 0, 0, -185116), (0, 0, 0, 2, -114332), (2, 0, -2, 0, 58793), (2, -1, -1, 0, 57066),
    (2, 0, 1, 0, 53322), (2, -1, 0, 0, 45758), (0, 1, -1, 0, -40923), (1, 0, 0, 0, -34720),
    (0, 1, 1, 0, -30383), (2, 0, 0, -2, 15327), (0, 0, 1, 2, -12528), (0, 0, 1, -2, 10980),
    (4, 0, -1, 0, 10675), (0, 0, 3, 0, 10034), (4, 0, -2, 0, 8548), (2, 1, -1, 0, -7888),
    (2, 1, 0, 0, -6766), (1, 0, -1, 0, -5163), (1, 1, 0, 0, 4987), (2, -1, 1, 0, 4036),
)  # fmt: skip
_LAT_TERMS = (  # Table 47.B
    (0, 0, 0, 1, 5128122), (0, 0, 1, 1, 280602), (0, 0, 1, -1, 277693), (2, 0, 0, -1, 173237),
    (2, 0, -1, 1, 55413), (2, 0, -1, -1, 46271), (2, 0, 0, 1, 32573), (0, 0, 2, 1, 17198),
    (2, 0, 1, -1, 9266), (0, 0, 2, -1, 8822), (2, -1, 0, -1, 8216), (2, 0, -2, -1, 4324),
    (2, 0, 1, 1, 4200),
)  # fmt: skip


def julian_day(when_ut: datetime) -> float:
    """Meeus eq. 7.1 for a Gregorian date, with the day's fraction."""
    y, m = when_ut.year, when_ut.month
    d = when_ut.day + (when_ut.hour + when_ut.minute / 60.0 + when_ut.second / 3600.0) / 24.0
    if m <= 2:
        y, m = y - 1, m + 12
    a = y // 100
    b = 2 - a + a // 4
    return math.floor(365.25 * (y + 4716)) + math.floor(30.6001 * (m + 1)) + d + b - 1524.5


def _moon_ecliptic(t: float) -> tuple[float, float]:
    """The moon's geocentric longitude and latitude in degrees (ch. 47)."""
    lp = 218.3164477 + 481267.88123421 * t - 0.0015786 * t * t + t**3 / 538841
    d = 297.8501921 + 445267.1114034 * t - 0.0018819 * t * t + t**3 / 545868
    m = 357.5291092 + 35999.0502909 * t - 0.0001536 * t * t
    mp = 134.9633964 + 477198.8675055 * t + 0.0087414 * t * t + t**3 / 69699
    f = 93.2720950 + 483202.0175233 * t - 0.0036539 * t * t - t**3 / 3526000
    e = 1.0 - 0.002516 * t - 0.0000074 * t * t
    args = (math.radians(d), math.radians(m), math.radians(mp), math.radians(f))

    def total(terms: tuple[tuple[int, int, int, int, int], ...]) -> float:
        s = 0.0
        for kd, km, kmp, kf, c in terms:
            arg = kd * args[0] + km * args[1] + kmp * args[2] + kf * args[3]
            s += c * e ** abs(km) * math.sin(arg)
        return s * 1e-6

    return (lp + total(_LON_TERMS)) % 360.0, total(_LAT_TERMS)


def _sun_longitude(t: float) -> float:
    """The sun's geometric longitude in degrees (ch. 25, low accuracy)."""
    l0 = 280.46646 + 36000.76983 * t + 0.0003032 * t * t
    m = math.radians(357.52911 + 35999.05029 * t - 0.0001537 * t * t)
    c = (
        (1.914602 - 0.004817 * t) * math.sin(m)
        + (0.019993 - 0.000101 * t) * math.sin(2 * m)
        + 0.000289 * math.sin(3 * m)
    )
    return (l0 + c) % 360.0


def _equatorial(lon_deg: float, lat_deg: float, t: float) -> tuple[float, float]:
    """Right ascension and declination in degrees from ecliptic coordinates (eq. 13.3,
    13.4) with the mean obliquity (eq. 22.2's first two terms)."""
    eps = math.radians(23.439291 - 0.013004 * t)
    lam, bet = math.radians(lon_deg), math.radians(lat_deg)
    ra = math.atan2(math.sin(lam) * math.cos(eps) - math.tan(bet) * math.sin(eps), math.cos(lam))
    dec = math.asin(math.sin(bet) * math.cos(eps) + math.cos(bet) * math.sin(eps) * math.sin(lam))
    return math.degrees(ra) % 360.0, math.degrees(dec)


def _star(name: str, t: float) -> tuple[float, float]:
    """A lunar star's place at the date, precessed from J2000 (eq. 21.4: m 46.1244 and n
    20.0431 seconds of arc a year)."""
    ra0, dec0 = LUNAR_STARS[name]
    years = t * 100.0
    a, d = math.radians(ra0), math.radians(dec0)
    ra = ra0 + years * (46.1244 + 20.0431 * math.sin(a) * math.tan(d)) / 3600.0
    dec = dec0 + years * 20.0431 * math.cos(a) / 3600.0
    return ra % 360.0, dec


def _horizontal(ra: float, dec: float, lat: float, lon_east: float, jd: float, t: float):
    """Altitude and azimuth (from the north, clockwise) in degrees (eq. 12.4, 13.5, 13.6)."""
    theta = 280.46061837 + 360.98564736629 * (jd - 2451545.0) + 0.000387933 * t * t
    h = math.radians((theta + lon_east - ra) % 360.0)
    phi, de = math.radians(lat), math.radians(dec)
    alt = math.asin(math.sin(phi) * math.sin(de) + math.cos(phi) * math.cos(de) * math.cos(h))
    az = math.atan2(math.sin(h), math.cos(h) * math.sin(phi) - math.tan(de) * math.cos(phi))
    return math.degrees(alt), (math.degrees(az) + 180.0) % 360.0


def _separation(ra1: float, dec1: float, ra2: float, dec2: float) -> float:
    """The angular distance between two bodies in degrees (eq. 17.1)."""
    a1, d1, a2, d2 = (math.radians(x) for x in (ra1, dec1, ra2, dec2))
    c = math.sin(d1) * math.sin(d2) + math.cos(d1) * math.cos(d2) * math.cos(a1 - a2)
    return math.degrees(math.acos(max(-1.0, min(1.0, c))))


def phase_words(age_days: float) -> str:
    """'new', 'a young moon', 'the first quarter', 'waxing', 'full', 'waning', 'the last
    quarter', 'an old moon': the phase by the age (judgement on the quarters' days)."""
    a = age_days
    if a < 1.0 or a > LUNATION_DAYS - 1.0:
        return "new"
    if a < 6.4:
        return "a young moon"
    if a < 8.4:
        return "the first quarter"
    if a < 13.8:
        return "waxing"
    if a < 15.8:
        return "full"
    if a < 21.2:
        return "waning"
    if a < 23.2:
        return "the last quarter"
    return "an old moon"


@dataclass(frozen=True)
class Moon:
    """The moon over a place at a moment: its age and phase, how much is lit, where it
    stands, and its distance from the sun and from each lunar star, with the sun's and
    the stars' altitudes beside (the lunar wants both bodies up)."""

    age_days: float
    fraction: float  # illuminated, 0 to 1
    altitude_deg: float
    azimuth_deg: float
    sun_altitude_deg: float
    sun_azimuth_deg: float
    sun_distance_deg: float
    stars: dict[str, tuple[float, float]]  # name -> (distance from the moon, altitude)

    @property
    def phase(self) -> str:
        return phase_words(self.age_days)

    @property
    def up(self) -> bool:
        return self.altitude_deg > 0.0


def moon_at(when_ut: datetime, lat_deg: float, lon_east_deg: float) -> Moon:
    """The moon at Universal Time `when_ut` over the place."""
    jd = julian_day(when_ut)
    t = (jd - 2451545.0) / 36525.0
    lon_m, lat_m = _moon_ecliptic(t)
    lon_s = _sun_longitude(t)
    ra_m, dec_m = _equatorial(lon_m, lat_m, t)
    ra_s, dec_s = _equatorial(lon_s, 0.0, t)
    elongation = (lon_m - lon_s) % 360.0
    psi = math.radians(elongation)
    fraction = (1.0 - math.cos(psi) * math.cos(math.radians(lat_m))) / 2.0
    alt, az = _horizontal(ra_m, dec_m, lat_deg, lon_east_deg, jd, t)
    s_alt, s_az = _horizontal(ra_s, dec_s, lat_deg, lon_east_deg, jd, t)
    stars = {}
    for name in LUNAR_STARS:
        ra, dec = _star(name, t)
        stars[name] = (
            _separation(ra_m, dec_m, ra, dec),
            _horizontal(ra, dec, lat_deg, lon_east_deg, jd, t)[0],
        )
    return Moon(
        age_days=elongation / 360.0 * LUNATION_DAYS,
        fraction=fraction,
        altitude_deg=alt,
        azimuth_deg=az,
        sun_altitude_deg=s_alt,
        sun_azimuth_deg=s_az,
        sun_distance_deg=_separation(ra_m, dec_m, ra_s, dec_s),
        stars=stars,
    )
