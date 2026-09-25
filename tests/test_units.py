import math
from datetime import datetime

import pytest

from freesail import units


def test_compass_points_round_trip():
    for i, abbr in enumerate(units.COMPASS_ABBREVIATIONS):
        angle = i * units.POINT
        assert units.nearest_point_index(angle) == i
        assert units.point_name(angle) == abbr
        assert units.parse_compass_point(abbr) == pytest.approx(angle)
        assert units.parse_compass_point(units.COMPASS_NAMES[i]) == pytest.approx(angle)


@pytest.mark.parametrize(
    "text, expected_abbr",
    [
        ("south-west by west", "SW by W"),
        ("southwest by west", "SW by W"),
        ("SOUTH WEST BY WEST", "SW by W"),
        ("nor'-east", "NE"),
        ("sou'west", "SW"),
        ("north", "N"),
        ("wsw", "WSW"),
    ],
)
def test_parse_compass_point_variants(text, expected_abbr):
    angle = units.parse_compass_point(text)
    assert angle is not None
    assert units.point_name(angle) == expected_abbr


def test_parse_compass_point_rejects_nonsense():
    assert units.parse_compass_point("upwards") is None
    assert units.parse_compass_point("") is None


def test_point_full_names():
    assert units.point_full_name("N") == "north"
    assert units.point_full_name("NNE") == "north-north-east"
    assert units.point_full_name("NE by N") == "north-east by north"


def test_wrap():
    assert units.wrap_pi(math.pi * 3) == pytest.approx(math.pi)
    assert units.wrap_pi(-math.pi * 0.5) == pytest.approx(-math.pi * 0.5)
    assert units.wrap_2pi(-0.1) == pytest.approx(2 * math.pi - 0.1)


def test_wind_vector_conventions():
    # A north wind blows toward the south.
    vx, vy = units.wind_vector(0.0, 10.0)
    assert vx == pytest.approx(0.0, abs=1e-9)
    assert vy == pytest.approx(-10.0)
    # A west wind blows toward the east.
    vx, vy = units.wind_vector(units.deg_to_rad(270), 5.0)
    assert vx == pytest.approx(5.0)
    assert vy == pytest.approx(0.0, abs=1e-9)
    # Round trip.
    for deg in (0, 45, 123, 270, 359):
        d = units.deg_to_rad(deg)
        vx, vy = units.wind_vector(d, 7.0)
        assert units.wind_direction_from(vx, vy) == pytest.approx(units.wrap_2pi(d), abs=1e-9)


def test_heading_vector():
    x, y = units.heading_vector(0.0)
    assert (x, y) == pytest.approx((0.0, 1.0))
    x, y = units.heading_vector(units.deg_to_rad(90))
    assert (x, y) == pytest.approx((1.0, 0.0))
    assert units.vector_heading(1.0, 0.0) == pytest.approx(units.deg_to_rad(90))


def test_relative_bearing_sign():
    heading = units.deg_to_rad(10)
    assert units.relative_bearing(heading, units.deg_to_rad(40)) > 0  # to starboard
    assert units.relative_bearing(heading, units.deg_to_rad(340)) < 0  # to larboard


@pytest.mark.parametrize(
    "hhmm, watch, bells",
    [
        ("00:00", "Middle watch", 8),
        ("00:30", "Middle watch", 1),
        ("03:30", "Middle watch", 7),
        ("04:00", "Morning watch", 8),
        ("09:30", "Forenoon watch", 3),
        ("12:00", "Afternoon watch", 8),
        ("16:00", "First dog watch", 8),
        ("17:30", "First dog watch", 3),
        ("18:00", "Last dog watch", 4),
        ("19:30", "Last dog watch", 3),
        ("20:00", "First watch", 8),
        ("23:30", "First watch", 7),
    ],
)
def test_bells(hhmm, watch, bells):
    h, m = map(int, hhmm.split(":"))
    dt = datetime(1805, 6, 1, h, m)
    assert units.watch_of(dt)[1] == watch
    assert units.bells_at(dt) == bells


def test_bells_only_on_half_hours():
    assert units.bells_at(datetime(1805, 6, 1, 9, 31)) is None
    assert units.bells_at(datetime(1805, 6, 1, 9, 30, 1)) is None


def test_time_stamp():
    assert units.time_stamp(datetime(1805, 6, 1, 9, 30)) == "Forenoon watch, 3 bells (09:30)"
    assert units.time_stamp(datetime(1805, 6, 1, 9, 37)) == "Forenoon watch (09:37)"
    assert units.time_stamp(datetime(1805, 6, 1, 0, 30)) == "Middle watch, 1 bell (00:30)"


def test_conversions():
    assert units.ms_to_knots(units.knots_to_ms(12.0)) == pytest.approx(12.0)
    assert units.m_to_fathoms(units.fathoms_to_m(5.0)) == pytest.approx(5.0)
    assert units.m_to_feet(1.0) == pytest.approx(3.28084, rel=1e-4)
    assert units.describe_wind_strength(units.knots_to_ms(15)) == "a moderate breeze"
    assert units.describe_wind_strength(units.knots_to_ms(45)) == "a strong gale"
