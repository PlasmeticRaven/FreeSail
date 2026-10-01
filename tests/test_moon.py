"""Package 33b: the moon (spec M5 §14; `freesail.core.moon`).

A low-precision moon good to a degree, checked against Meeus's worked example (ch. 47,
example 47.a) and against the JPL Horizons ephemeris for June 1805 (the geocentric
longitude and latitude of date, the illuminated fraction, and the sun's and the moon's
altitude and azimuth over 50 N 5 W); the age and the phase words; the lunar stars.
"""

from __future__ import annotations

import math
from datetime import datetime

from freesail.core import moon as M

# JPL Horizons, the moon seen from the earth's centre at 0h UT, June 1805: the
# ecliptic longitude and latitude of date (ObsEcLon, ObsEcLat) and the illuminated
# fraction (Illu%), read on 2026-10-01 (docs/dev/TuningNotes.md, package 33b).
HORIZONS_1805 = {
    1: (116.6178744, -0.8763483, 15.73342),
    5: (171.9049585, -4.7212298, 57.13360),
    10: (234.1316186, -4.1464142, 95.41322),
    12: (257.9361029, -2.5111494, 99.90206),
    20: (354.8196736, 4.8979787, 53.01145),
    27: (95.2406570, 1.0309687, 0.00955),
}


def test_meeus_example_47a():
    """Meeus, example 47.a: 1992 April 12 at 0h TD, the apparent longitude 133.162655°
    and latitude -3.229126°, the right ascension 134.688470° and declination
    13.768368°; the short method's few terms land within a hundredth of a degree."""
    jd = M.julian_day(datetime(1992, 4, 12))
    assert jd == 2448724.5
    t = (jd - 2451545.0) / 36525.0
    lon, lat = M._moon_ecliptic(t)
    assert abs(lon - 133.162655) < 0.01 and abs(lat + 3.229126) < 0.01
    ra, dec = M._equatorial(lon, lat, t)
    assert abs(ra - 134.688470) < 0.02 and abs(dec - 13.768368) < 0.02


def test_june_1805_against_horizons():
    """The moon's place and its light through a lunation in June 1805 against JPL
    Horizons: within a few hundredths of a degree and half a per cent of light; the
    full moon of the 12th and the new moon of the 27th by the age."""
    for day, (h_lon, h_lat, h_lit) in HORIZONS_1805.items():
        m = M.moon_at(datetime(1805, 6, day), 50.0, -5.0)
        jd = M.julian_day(datetime(1805, 6, day))
        lon, lat = M._moon_ecliptic((jd - 2451545.0) / 36525.0)
        assert abs((lon - h_lon + 180.0) % 360.0 - 180.0) < 0.02, day
        assert abs(lat - h_lat) < 0.02, day
        assert abs(m.fraction * 100.0 - h_lit) < 0.5, day
    assert M.moon_at(datetime(1805, 6, 12), 50.0, -5.0).phase == "full"
    assert M.moon_at(datetime(1805, 6, 27), 50.0, -5.0).phase == "new"
    assert M.moon_at(datetime(1805, 6, 5), 50.0, -5.0).phase == "the first quarter"
    assert M.moon_at(datetime(1805, 6, 20), 50.0, -5.0).phase == "the last quarter"
    age = M.moon_at(datetime(1805, 6, 10), 50.0, -5.0).age_days
    assert 12.0 < age < 13.5


def test_altitude_and_azimuth_over_the_channel():
    """Horizons for an observer at 50 N 5 W on 10 June 1805: the sun at 12:30 UT at
    azimuth 185.6° and 62.9° up, at 04:30 UT rising at 55.0° and 1.9° up; the moon at
    0h UT at azimuth 201.1° and 13.7° up (topocentric: the parallax takes a degree off
    the geocentric altitude the model gives, which is within the brief's degree)."""
    noon = M.moon_at(datetime(1805, 6, 10, 12, 30), 50.0, -5.0)
    assert abs(noon.sun_azimuth_deg - 185.6) < 1.0 and abs(noon.sun_altitude_deg - 62.9) < 0.5
    rise = M.moon_at(datetime(1805, 6, 10, 4, 30), 50.0, -5.0)
    assert abs(rise.sun_azimuth_deg - 55.0) < 1.0 and abs(rise.sun_altitude_deg - 1.9) < 0.7
    midnight = M.moon_at(datetime(1805, 6, 10, 0, 0), 50.0, -5.0)
    assert abs(midnight.azimuth_deg - 201.1) < 1.0 and abs(midnight.altitude_deg - 13.7) < 1.5
    assert midnight.up and not rise.up  # the moon sets about 04:00 that morning


def test_the_lunar_stars_and_their_precession():
    """The Almanac's nine lunar stars; their places precessed from J2000 to 1805 move
    by two to three degrees (Meeus eq. 21.4), and the distance from the moon to each
    is a great-circle separation under 180°."""
    assert len(M.LUNAR_STARS) == 9 and "Aldebaran" in M.LUNAR_STARS and "Antares" in M.LUNAR_STARS
    t = (M.julian_day(datetime(1805, 6, 10)) - 2451545.0) / 36525.0
    for name, (ra0, dec0) in M.LUNAR_STARS.items():
        ra, dec = M._star(name, t)
        moved = M._separation(ra0, dec0, ra, dec)
        assert 2.0 < moved < 3.2, (name, moved)
    m = M.moon_at(datetime(1805, 6, 10), 50.0, -5.0)
    assert all(0.0 <= d <= 180.0 for d, _alt in m.stars.values())
    # the moon near full lies opposite the sun: Antares is close to it that night
    assert m.stars["Antares"][0] < 15.0 and m.sun_distance_deg > 150.0


def test_phase_words_cover_the_lunation():
    words = {M.phase_words(a / 2.0) for a in range(0, 60)}
    assert words == {
        "new",
        "a young moon",
        "the first quarter",
        "waxing",
        "full",
        "waning",
        "the last quarter",
        "an old moon",
    }
    assert math.isclose(M.LUNATION_DAYS, 29.530588861)
