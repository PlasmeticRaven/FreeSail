"""Package 32: the geographic frame (spec M5 §9; C §5.1).

The arithmetic of `freesail.world.geo` (the sphere whose minute is the mile, a run
turned to latitude and longitude, bearings and distances, the horizon, the words); the
World keeping the ship's position from her run in metres and the sun reading her
latitude; a scenario without a position being the plane it was, every constant of the
earlier milestones unchanged; the position and the region in the scenario file and in
the save, and a replay following them.
"""

from __future__ import annotations

import math
from datetime import datetime

import pytest

from freesail import units
from freesail.core import replay as replay_mod
from freesail.core.world import Scenario, World
from freesail.world import geo
from freesail.world.geo import Position
from freesail.world.scenarios import ScenarioError, load_scenario

T0 = datetime(1805, 6, 1, 4, 0)


def point_world(seed: int = 3, **kw) -> World:
    return World(seed=seed, scenario=Scenario(start_time=T0, gustiness=0.0, variability=0.0, **kw))


# ---------------------------------------------------------------------------
# The sphere
# ---------------------------------------------------------------------------


def test_a_minute_of_latitude_is_a_nautical_mile_on_the_games_sphere():
    """The radius is chosen so that a degree of latitude is sixty miles of 1852 m, as the
    sun's METRES_PER_DEGREE has it; a run of one mile north moves her one minute."""
    assert math.isclose(math.radians(1.0) * geo.EARTH_RADIUS_M, 60.0 * units.NAUTICAL_MILE)
    p = Position(50.0, -5.0).advanced(0.0, units.NAUTICAL_MILE)
    assert math.isclose(p.lat_deg, 50.0 + 1.0 / 60.0)
    assert p.lon_deg == -5.0


def test_a_run_east_shrinks_with_the_cosine_of_the_latitude():
    """dλ = dx / (R cos φ) (C §5.1): a mile east at 60 N is two minutes of longitude, at
    the equator one."""
    at_sixty = Position(60.0, 0.0).advanced(units.NAUTICAL_MILE, 0.0)
    at_zero = Position(0.0, 0.0).advanced(units.NAUTICAL_MILE, 0.0)
    assert math.isclose(at_sixty.lon_deg, 2.0 / 60.0, rel_tol=1e-3)
    assert math.isclose(at_zero.lon_deg, 1.0 / 60.0, rel_tol=1e-6)


def test_the_run_is_converted_per_tick_and_not_per_region():
    """A hundred miles north then a hundred east, tick by tick, differs from the flat
    plane by the few per cent the study names, because each step reads its own
    latitude; the same run in one step at the start latitude reads the plane."""
    start = Position(48.0, -6.0)
    p = start
    for _ in range(100):
        p = p.advanced(0.0, units.NAUTICAL_MILE)
    for _ in range(100):
        p = p.advanced(units.NAUTICAL_MILE, 0.0)
    flat_lon = start.lon_deg + math.degrees(
        100 * units.NAUTICAL_MILE / (geo.EARTH_RADIUS_M * math.cos(math.radians(48.0)))
    )
    assert math.isclose(p.lat_deg, 48.0 + 100.0 / 60.0)
    # she is at 49° 40' when she turns east, so her hundred miles east are more degrees
    assert p.lon_deg > flat_lon
    assert 0.02 < (p.lon_deg - start.lon_deg) / (flat_lon - start.lon_deg) - 1.0 < 0.04


def test_bearing_and_distance_and_the_way_back():
    lizard = Position(49.9594, -5.2067)
    ushant = Position(48.4600, -5.0950)
    bearing, distance = geo.bearing_and_distance(lizard, ushant)
    assert 170.0 < bearing < 180.0  # Ushant lies a little east of south from the Lizard
    assert 89.0 < distance / units.NAUTICAL_MILE < 91.0
    back = geo.destination(lizard, bearing, distance)
    assert math.isclose(back.lat_deg, ushant.lat_deg, abs_tol=1e-6)
    assert math.isclose(back.lon_deg, ushant.lon_deg, abs_tol=1e-6)
    dx, dy = lizard.offset_to(ushant)
    assert math.isclose(math.hypot(dx, dy), distance, rel_tol=1e-3)
    assert dy < 0 and abs(dx) < abs(dy) / 10


def test_the_horizon_is_the_specs_formula():
    """2.08 (√h_eye + √h_object) miles with heights in metres (spec §11): the frigate's
    lookout at thirty-six metres sees the Lizard's sixty-metre cliff at about twenty-nine
    miles and the sea horizon at twelve and a half."""
    assert math.isclose(geo.horizon_nm(36.0, 60.0), 2.08 * (6.0 + math.sqrt(60.0)))
    assert math.isclose(geo.horizon_nm(36.0), 12.48)
    assert geo.horizon_nm(0.0) == 0.0


def test_positions_and_distances_in_the_periods_words():
    assert str(Position(49.8667, -6.1667)) == "49° 52' N, 6° 10' W"
    assert geo.format_position(Position(-33.9, 151.2)) == "33° 54' S, 151° 12' E"
    assert geo.parse_position("49 52 N 6 10 W") == Position(
        pytest.approx(49.8667, abs=1e-3), pytest.approx(-6.1667, abs=1e-3)
    )
    assert geo.parse_position("49°52'N, 6°10'W").lon_deg < 0
    assert geo.parse_position("48.5 N 5.1 W") == Position(48.5, -5.1)
    with pytest.raises(ValueError):
        geo.parse_position("somewhere off Ushant")
    nm = units.NAUTICAL_MILE
    assert geo.distance_words(0.3 * nm) == "three cables"
    assert geo.distance_words(4.4 * nm) == "four miles and a half"
    assert geo.distance_words(12.0 * nm) == "four leagues"
    assert geo.distance_words(13.6 * nm) == "four leagues and a half"
    # the lookout's estimate: never the truth to a cable
    assert geo.estimate_words(12.4 * nm) == "four leagues"
    assert geo.estimate_words(2.6 * nm) == "three miles"
    assert geo.estimate_words(0.05 * nm) == "a cable"
    assert geo.estimate_words(0.97 * nm) == "a mile"


def test_a_position_reads_from_a_dict_a_string_or_a_pair():
    assert Position.from_dict({"lat_deg": 50.0, "lon_deg": -5.0}) == Position(50.0, -5.0)
    assert Position.from_dict({"lat": 50.0, "lon": -5.0}) == Position(50.0, -5.0)
    assert Position.from_dict("50 00 N 5 00 W") == Position(50.0, -5.0)
    assert Position.from_dict((50.0, -5.0)) == Position(50.0, -5.0)
    with pytest.raises(ValueError):
        Position.from_dict({"lat_deg": 50.0})


# ---------------------------------------------------------------------------
# The World
# ---------------------------------------------------------------------------


def test_a_scenario_without_a_position_is_the_plane_it_was():
    """No position: no geographic position, no chart, no lookout, the sun at the
    scenario's latitude, and the state block as it was (spec M5 §9: every M4 and 5a
    constant unchanged; the truths of test_known_truths.py are the proof at scale)."""
    w = point_world()
    assert w.position is None and w.origin is None
    assert w.chart is None and w.lookout is None
    assert w.sun.latitude_deg == 50.0
    w.submit("steer 090")
    w.run(600)
    assert w.position is None
    assert "position" not in w.state()
    assert w.readings["in_sight"] is None and w.readings["land"] is None
    assert w.readings["depth_of_water"] is None
    assert w.readings.words("depth_of_water").startswith("No chart of these waters")
    assert w.readings.words("in_sight").startswith("No chart of these waters")


def test_the_ship_keeps_her_position_from_her_run_and_the_sun_reads_her_latitude():
    """With a position the World advances her latitude and longitude each tick from
    her run in metres, and the sun's latitude is hers, not the scenario's."""
    w = point_world(
        position={"lat_deg": 49.0, "lon_deg": -6.0}, ship_heading_deg=0.0, ship_speed_kn=10.0
    )
    assert w.origin == Position(49.0, -6.0) and w.position == w.origin
    assert w.sun.latitude_deg == 49.0
    w.run(3600)  # an hour north at ten knots: ten miles, ten minutes of latitude
    assert w.position is not None
    assert math.isclose(w.position.lat_deg, 49.0 + 10.0 / 60.0, abs_tol=1e-3)
    assert math.isclose(w.position.lon_deg, -6.0, abs_tol=1e-6)
    assert w.ship_y == pytest.approx(10.0 * units.NAUTICAL_MILE, rel=1e-3)  # the plane's y, still
    assert w.state()["position"] == w.position.to_dict()
    # the sun follows her: the daylight at her latitude now
    assert w.sun.latitude_deg == pytest.approx(w.position.lat_deg)
    assert w.daylight in ("day", "twilight", "night")


def test_the_position_and_the_region_are_saved_and_a_replay_follows_them():
    w = point_world(
        position={"lat_deg": 49.0, "lon_deg": -6.0}, ship_heading_deg=90.0, ship_speed_kn=6.0
    )
    w.run(1800)
    data = w.save()
    assert data["scenario"]["position"] == {"lat_deg": 49.0, "lon_deg": -6.0}
    assert data["scenario"]["region"] is None
    copy = replay_mod.replay(data, None)
    assert copy.position == w.position and copy.log.digest() == w.log.digest()
    # a save from before the frame loads with none
    old = dict(data["scenario"])
    del old["position"]
    del old["region"]
    assert Scenario.from_dict(old).position is None and Scenario.from_dict(old).region is None


def test_a_region_needs_a_position_and_a_position_inside_it():
    with pytest.raises(ValueError, match="gives no position"):
        point_world(region="channel-west")
    with pytest.raises(ValueError, match="outside the chart region"):
        point_world(region="channel-west", position={"lat_deg": 40.0, "lon_deg": -20.0})
    with pytest.raises(ValueError, match="no chart region named"):
        point_world(region="the-moon", position={"lat_deg": 49.0, "lon_deg": -6.0})


def test_the_scenario_file_reads_the_position_and_the_region(tmp_path):
    p = tmp_path / "off-the-lizard.yaml"
    p.write_text(
        "name: Off the Lizard\nstart: 1805-06-01T10:00\nposition: 49 52 N 5 12 W\n"
        "region: channel-west\nship: {heading_deg: 90}\n",
        encoding="utf-8",
    )
    sf = load_scenario(p)
    assert sf.scenario.position == {
        "lat_deg": pytest.approx(49.8667, abs=1e-3),
        "lon_deg": pytest.approx(-5.2, abs=1e-3),
    }
    assert sf.scenario.region == "channel-west"
    assert sf.scenario.latitude_deg == pytest.approx(49.8667, abs=1e-3)  # the sun's, from it
    assert "She starts at 49° 52' N, 5° 12' W, on the chart of channel-west." in sf.lines()
    q = tmp_path / "bad.yaml"
    q.write_text("name: x\nregion: channel-west\n", encoding="utf-8")
    with pytest.raises(ScenarioError, match="needs a position"):
        load_scenario(q)
    r = tmp_path / "worse.yaml"
    r.write_text("name: x\nposition: nowhere\n", encoding="utf-8")
    with pytest.raises(ScenarioError, match="position"):
        load_scenario(r)


# ---------------------------------------------------------------------------
# Package 38: `chart:` beside `region:` (spec M6 §26)
# ---------------------------------------------------------------------------


def test_the_scenario_file_reads_a_chart_beside_a_region_and_a_save_before_it_loads(tmp_path):
    """`chart: atlantic-east` loads the chart whole; `region:` is a chart of that one
    region as before; a file may say both, the chart winning; a chart needs a position
    too; a save from before the field loads with none."""
    p = tmp_path / "off-lisbon.yaml"
    p.write_text(
        "name: Off Lisbon\nstart: 1805-06-01T10:00\nposition: 38 36 N 9 24 W\n"
        "chart: atlantic-east\nship: {heading_deg: 180}\n",
        encoding="utf-8",
    )
    sf = load_scenario(p)
    assert sf.scenario.chart == "atlantic-east" and sf.scenario.region is None
    assert "on the chart of atlantic-east." in sf.lines()[1]
    w = point_world(chart="atlantic-east", position={"lat_deg": 38.6, "lon_deg": -9.4})
    assert w.chart.name == "atlantic-east" and w.chart.level_at(w.position) == 1
    both = point_world(
        chart="atlantic-east", region="channel-west", position={"lat_deg": 49.0, "lon_deg": -6.0}
    )
    assert both.chart.name == "atlantic-east"
    assert both.chart.regions == ["channel-west", "channel-mid"]  # package 39a
    data = both.save()
    assert data["scenario"]["chart"] == "atlantic-east"
    copy = replay_mod.replay(data, None)
    assert copy.chart.name == "atlantic-east"
    old = dict(data["scenario"])
    del old["chart"]
    assert (
        Scenario.from_dict(old).chart is None and Scenario.from_dict(old).region == "channel-west"
    )
    q = tmp_path / "bad.yaml"
    q.write_text("name: x\nchart: atlantic-east\n", encoding="utf-8")
    with pytest.raises(ScenarioError, match="needs a position"):
        load_scenario(q)
    with pytest.raises(ValueError, match="outside the chart region 'atlantic-east'"):
        point_world(chart="atlantic-east", position={"lat_deg": 55.0, "lon_deg": -20.0})
    with pytest.raises(ValueError, match="no chart region named"):
        point_world(chart="the-moon", position={"lat_deg": 49.0, "lon_deg": -6.0})
