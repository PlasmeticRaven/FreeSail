"""Package 32: the chart data and the queries (spec M5 §10, §11; the study
docs/design/ChartData.md §5).

The manifest and its sources (every licence in the allowed list, every feature and
override citing a source, the region's tiles present and under the size the brief sets);
the tiles' arithmetic (the tile under a point by integer arithmetic, the predictor's round
trip, bilinear across a tile edge); the four queries against the real data (depth here,
aground short-circuited, nearest coast, in sight of what); the period patches in the
tiles; the readings on a ship with a chart and without; and the coast-distance hook
bringing the sea breeze and the coastal fog alive on a summer afternoon off Falmouth.
Truth 65 and the pace truth are in test_known_truths.py.
"""

from __future__ import annotations

import importlib.util
import math
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import numpy as np
import pytest
import yaml

from freesail import units
from freesail.api import readings as R
from freesail.api.session import make_world
from freesail.core.world import Scenario, World
from freesail.world import chart as C
from freesail.world.chart import Chart, Feature, load_chart, load_manifest
from freesail.world.geo import Position, destination
from freesail.world.weather import (
    FOG_COAST_KM,
    SEA_BREEZE_MAX_KN,
    SEA_BREEZE_REACH_KM,
    Weather,
)

ROOT = Path(__file__).resolve().parents[1]
CHARTS = ROOT / "data" / "charts"
FRIGATE = "data/ships/frigate-36.yaml"
SCHOONER = "data/ships/topsail-schooner.yaml"
REGION = "channel-west"

# The brief's budget for the committed region (C §5.3; package 32): the region's tiles and
# coast under 25 MB compressed. The world and the Atlantic levels are the tool's and are
# not committed (spec M5 §10).
REGION_BUDGET_BYTES = 25 * 1024 * 1024

LIZARD = Position(49.9594, -5.2067)
OFF_THE_LIZARD = Position(49.90, -5.20)
CARRICK_ROADS = Position(50.160, -5.0355)  # the deep water of the Road, off Trefusis
MID_CHANNEL = Position(49.5, -5.0)


def build_tool():
    """The build tool as a module, for its allowed-licence list and its tile arithmetic."""
    spec = importlib.util.spec_from_file_location(
        "build_charts", ROOT / "tools" / "build_charts.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module  # the dataclasses look their module up here
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def chart() -> Chart:
    return load_chart(REGION)


@pytest.fixture(scope="module")
def manifest() -> dict:
    return load_manifest()


def chart_world(
    lat: float,
    lon: float,
    ship: str = FRIGATE,
    heading: float = 0.0,
    start: datetime = datetime(1805, 6, 1, 10, 0),
    seed: int = 7,
    **kw,
) -> World:
    sc = Scenario(
        start_time=start,
        wind_from_deg=270.0,
        wind_speed_kn=12.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=heading,
        position={"lat_deg": lat, "lon_deg": lon},
        region=REGION,
        **kw,
    )
    return make_world(seed, ship, sc)


# ---------------------------------------------------------------------------
# The manifest, the sources and the hand-made files (C §5.4 step 5's test)
# ---------------------------------------------------------------------------


def test_every_source_in_the_manifest_has_an_allowed_licence_with_its_text_kept(manifest):
    tool = build_tool()
    assert "ODbL" not in " ".join(tool.ALLOWED_LICENCES)
    sources = manifest["sources"]
    assert {"gebco_2025", "emodnet_dtm_2024"} <= set(sources)
    for sid, s in sources.items():
        assert s["licence"] in tool.ALLOWED_LICENCES, sid
        assert (ROOT / s["licence_text"]).exists(), s["licence_text"]
        assert s["attribution"] and s["home"]
        for f in s["fetched"]:
            assert len(f["sha256"]) == 64 and f["bytes"] > 0 and f["retrieved"]
    # the two sources the tiles are cut from were fetched; the two cross-checks say so
    assert sources["gebco_2025"]["fetched"] and sources["emodnet_dtm_2024"]["fetched"]
    assert sources["shom_homonim"]["status"].startswith("not fetched")
    assert (
        "Not for navigation" in manifest["attribution"]
        or "not for navigation" in manifest["attribution"]
    )


def test_every_feature_and_every_override_cites_a_source():
    tool = build_tool()
    features, _ = tool.load_features(REGION)
    assert len(features) >= 150
    for f in features:
        assert str(f["source"]).strip(), f["id"]
        assert str(f["says"]).strip(), f["id"]
        assert f["kind"] in tool.FEATURE_KINDS
    patches, records = tool.load_overrides(REGION)
    assert len(records) == 5 and len(patches) >= 5
    for r in records:
        assert r["sheet"] and r["source"] and r["units"] and r["datum"]
        assert r["control_points"] and len(r["control_points"]) >= 5
    for p in patches:
        assert p.source.strip(), p.name
    names = {r["file"].split("/")[-1] for r in records}
    assert names == {
        "falmouth-helford.yaml",
        "plymouth-cawsand.yaml",
        "scilly.yaml",
        "brest-iroise.yaml",
        "roscoff.yaml",  # package 35b
    }


def test_the_lights_are_dated_so_that_1805_sees_st_agnes_and_not_the_bishop(chart):
    lights = [f for f in chart.features.values() if f.kind == "light"]
    assert len(lights) >= 10
    for f in lights:
        assert f.lit and f.lit.get("from"), f.id
        assert f.lit.get("range_nm"), f.id
    lit_1805 = sorted(f.id for f in lights if f.lit_in(1805))
    assert lit_1805 == [
        "eddystone",
        "lizard-lights",
        "longships-light",
        "st-agnes-light",
        "st-mathieu-light",
        "stiff-light",
    ]
    assert chart.feature("bishop-rock-light").lit_in(1860)
    assert not chart.feature("bishop-rock-light").lit_in(1805)
    assert chart.feature("st-agnes-light").lit_in(1805) and not chart.feature(
        "st-agnes-light"
    ).lit_in(1912)


def test_the_regions_tiles_are_present_committed_and_under_the_brief_size(manifest):
    region = manifest["regions"][REGION]
    total = 0
    for level, tiles in region["tiles"].items():
        for t in tiles:
            path = CHARTS / "tiles" / str(level) / f"{t['name']}.npz"
            assert path.exists(), path
            total += path.stat().st_size
    total += (CHARTS / region["coast"]).stat().st_size
    total += (CHARTS / region["features"]).stat().st_size
    assert total < REGION_BUDGET_BYTES, f"{total / 1e6:.1f} MB"
    # the world and the Atlantic are built by the tool and never committed (spec M5 §10):
    # the manifest says so, and no tile of theirs is in the repository's files
    tool = build_tool()
    for key, level, flag in (("world", 0, "--world"), ("atlantic", 1, "--atlantic")):
        entry = manifest[key]
        assert entry["level"] == level and entry["committed"] is False
        assert flag in entry["built_by"]
        for t in entry.get("tiles") or []:
            # a tile the tool made here is named by its corner in whole seconds
            s, w = int(t["south_sec"]), int(t["west_sec"])
            assert t["name"] == tool.tile_name(s, w)
            assert (s + 90 * 3600) % tool.tile_span_sec(level) == 0
    tracked = subprocess.run(
        ["git", "ls-files", "data/charts/tiles/0", "data/charts/tiles/1"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    ).stdout.split()
    assert tracked == []


# ---------------------------------------------------------------------------
# The tiles' arithmetic
# ---------------------------------------------------------------------------


def test_a_tile_is_found_by_integer_arithmetic_on_the_position_and_its_corner_is_whole_seconds():
    tool = build_tool()
    for level in (0, 1, 2, 3):
        s, w = tool.tile_corner_sec(level, 49.9594, -5.2067)
        span = tool.tile_span_sec(level)
        assert (s + 90 * 3600) % span == 0 and (w + 180 * 3600) % span == 0
        assert s <= 49.9594 * 3600 < s + span and w <= -5.2067 * 3600 < w + span
    chart = load_chart(REGION)
    finest = chart.levels[0]
    assert finest.level == 3
    row, col = finest.global_cell(49.9594, -5.2067)
    s, w = finest.corner_of_cell(int(row), int(col))
    assert s == tool.tile_corner_sec(3, 49.9594, -5.2067)[0]
    assert w == tool.tile_corner_sec(3, 49.9594, -5.2067)[1]


def test_the_predictors_round_trip_is_exact_and_the_tile_carries_its_metadata(chart):
    tool = build_tool()
    rng = np.random.default_rng(7)
    values = rng.integers(-32000, 32000, size=(64, 64), dtype=np.int32).astype(np.int16)
    packed = tool.differenced(values)
    back = np.cumsum(packed.view(np.uint16), axis=1, dtype=np.uint16).view(np.int16)
    assert np.array_equal(back, values)
    tile = chart.levels[1].tile_at(49.90, -5.20)  # level 2 under the Lizard's offing
    assert tile is not None and tile.level == 2 and tile.cells == 512
    assert math.isclose(tile.unit_m, 0.1, rel_tol=1e-6)
    assert tile.dist is not None and tile.dist.dtype == np.uint16
    assert tile.elevation.dtype == np.int16 and tile.nodata == -32768
    assert -200.0 < tile.min_depth_m < 200.0


def test_depth_here_is_bilinear_and_continuous_across_a_tile_edge(chart):
    level = chart.levels[1]  # level 2: the whole region
    s, w = level.corner_of_cell(*(int(x) for x in level.global_cell(49.60, -5.30)))
    edge_lat = (s + level.span_sec) / 3600.0  # the northern edge of that tile
    last = None
    for k in range(-20, 21):
        lat = edge_lat + k * 0.00002
        d = level.elevation_at(lat, -5.30)
        assert d is not None
        if last is not None:
            assert abs(d - last) < 2.0, (lat, d, last)
        last = d


# ---------------------------------------------------------------------------
# The queries against the data (C §5.5)
# ---------------------------------------------------------------------------


def test_depth_here_off_the_lizard_in_carrick_roads_and_in_mid_channel(chart):
    off = chart.depth_at(OFF_THE_LIZARD)
    roads = chart.depth_at(CARRICK_ROADS)
    mid = chart.depth_at(MID_CHANNEL)
    assert 70.0 < off < 90.0 and 8.0 < roads < 40.0 and 85.0 < mid < 100.0
    assert chart.depth_at(Position(50.153, -5.070)) < 0  # Falmouth town stands above the datum
    # beyond the region nothing answers unless the tool's world level was built here (it
    # is never committed): then it answers coarsely
    atlantic = Position(45.0, -20.0)
    if chart._finest_level(atlantic) is None:
        assert chart.depth_at(atlantic) is None
    else:
        assert chart._finest_level(atlantic).level == 0 and chart.depth_at(atlantic) > 3000.0
    # the finest level answers first: the harbour patch under Carrick Roads
    assert chart._finest_level(CARRICK_ROADS).level == 3
    assert chart._finest_level(MID_CHANNEL).level == 2


def test_the_tiles_minimum_depth_short_circuits_the_grounding_check_at_sea(chart):
    assert chart.tile_min_depth(MID_CHANNEL) > 4.6 + C.AGROUND_HIGHEST_TIDE_M + C.AGROUND_MARGIN_M
    assert chart.aground(MID_CHANNEL, 0.0, 41.8, 4.6, 0.0, 0.0, 10.0) is None
    t0 = time.perf_counter()
    for _ in range(2000):
        chart.aground(MID_CHANNEL, 0.0, 41.8, 4.6, 0.0, 0.0, 10.0)
    each = (time.perf_counter() - t0) / 2000
    assert each < 100e-6, f"{each * 1e6:.0f} microseconds a check at sea"
    # inshore the keel's cells are read: the frigate afloat in the Roads, aground on the shore
    assert chart.aground(CARRICK_ROADS, 0.0, 41.8, 4.6, 0.0, 0.0, 10.0) is None
    ashore = chart.aground(Position(50.153, -5.070), 0.0, 41.8, 4.6, 0.0, 0.0, 10.0)
    assert ashore is not None and ashore.where in ("forward", "aft", "amidships")
    assert "taken the ground" in ashore.words and "feet" in ashore.words
    # the tide's height (package 34's) lifts her: the schooner over a two-fathom patch
    shoal = Position(50.1530, -5.0400)  # the Governor, a two-fathom patch (Imray)
    assert (
        chart.aground(shoal, 0.0, 25.9, 3.3, 0.0, tide_m=0.0) is not None
        or chart.depth_at(shoal) > 3.3
    )
    assert chart.aground(shoal, 0.0, 25.9, 3.3, 0.0, tide_m=5.0) is None


def test_nearest_coast_from_the_distance_field_with_a_name_from_the_index(chart):
    coast = chart.coast_at(OFF_THE_LIZARD)
    assert coast is not None
    assert 5000.0 < coast.distance_m < 8000.0
    assert coast.bearing_deg < 45.0 or coast.bearing_deg > 315.0  # the Lizard lies north
    assert coast.name == "the Lizard" and coast.feature_id == "lizard-point"
    ashore = chart.coast_at(Position(50.153, -5.070))
    assert ashore is not None and ashore.distance_m == 0.0
    mid = chart.coast_at(MID_CHANNEL)
    assert mid is not None and 40000.0 < mid.distance_m < 70000.0
    # the field alone (the weather's hook every tick) is microseconds; the name is for the log
    assert chart.coast_distance(OFF_THE_LIZARD) == (coast.distance_m, coast.bearing_deg)
    t0 = time.perf_counter()
    for _ in range(1000):
        chart.coast_distance(OFF_THE_LIZARD)
    assert (time.perf_counter() - t0) / 1000 < 150e-6
    t0 = time.perf_counter()
    for _ in range(200):
        chart.coast_at(OFF_THE_LIZARD)
    assert (time.perf_counter() - t0) / 200 < 2e-3


def test_in_sight_of_what_by_the_horizon_the_daylight_and_the_features_own_rules(chart):
    eye = 36.0
    ten_miles_south = destination(LIZARD, 180.0, 10 * units.NAUTICAL_MILE)
    by_day = chart.in_sight(ten_miles_south, eye, None, "day", datetime(1805, 6, 1, 12, 0))
    ids = {s.feature.id for s in by_day}
    assert "lizard-point" in ids and "lizard-lights" in ids
    lizard = next(s for s in by_day if s.feature.id == "lizard-point")
    assert 350.0 < lizard.bearing_deg or lizard.bearing_deg < 10.0
    assert abs(lizard.distance_m - 10 * units.NAUTICAL_MILE) < 200.0
    assert lizard.seen_as == "land"
    # at night only the lights, by their range and their date
    by_night = chart.in_sight(ten_miles_south, eye, None, "night", datetime(1805, 6, 1, 23, 30))
    assert {s.seen_as for s in by_night} == {"light"}
    assert {s.feature.id for s in by_night} == {"lizard-lights"}
    # the weather's visibility caps everything
    thick = chart.in_sight(ten_miles_south, eye, 1.0, "day", datetime(1805, 6, 1, 12, 0))
    assert thick == []
    # beyond the horizon of a low rock, the rock is not seen even by day
    far = chart.in_sight(
        destination(LIZARD, 180.0, 40 * units.NAUTICAL_MILE),
        eye,
        None,
        "day",
        datetime(1805, 6, 1, 12, 0),
    )
    assert far == []
    # a danger is made out only close-to
    near_manacles = destination(Position(50.0470, -5.0440), 120.0, 2 * units.NAUTICAL_MILE)
    dangers = [
        s
        for s in chart.in_sight(near_manacles, eye, None, "day", datetime(1805, 6, 1, 12, 0))
        if s.seen_as == "danger"
    ]
    assert any(s.feature.id == "the-manacles" for s in dangers)


def test_the_period_patches_are_in_the_tiles(chart):
    # Plymouth without the breakwater: water where the modern grid has the work
    over_the_breakwater = Position(50.3345, -4.1500)
    d = chart.depth_at(over_the_breakwater)
    assert d is not None and 8.0 < d < 14.0, (
        d
    )  # about six fathoms at low water springs, plus the datum shift
    # Falmouth without the docks: water off Pendennis' north foot
    docks = Position(50.1540, -5.0545)
    d = chart.depth_at(docks)
    assert d is not None and 1.0 < d < 5.0, d
    # the overrides' tiles are flagged
    tile = chart.levels[0].tile_at(50.3345, -4.1500)
    assert tile is not None and tile.level == 3
    # the Iroise's bottom note is what the lead brings up off Brest
    assert "shells" in chart.bottom_near(Position(48.25, -4.90), within_m=20000.0)


def test_features_are_read_with_their_words_and_their_index(chart):
    f = chart.feature("the-manacles")
    assert isinstance(f, Feature) and f.kind == "ledge" and f.name == "the Manacles"
    assert "White 1835" in f.source and f.says.startswith("The Manacles")
    assert f.view.startswith("Serres 1801")
    near = {x.id for x in chart.nearby(Position(50.14, -5.03), 3000.0)}
    assert {"black-rock-falmouth", "pendennis-castle", "st-anthony-head"} <= near
    transit = chart.feature("manacles-clearing-mark")
    # package 33b (playtest 12): the near mark is the Helford's Nare Point, not the
    # Roseland's Nare Head, which stays on the chart east of Falmouth
    assert transit.kind == "transit" and list(transit.marks) == ["nare-point", "mawnan-church"]
    assert all(chart.feature(m) is not None for m in transit.marks)
    assert chart.feature("nare-point").name == "Nare Point"
    assert chart.feature("nare-head").modern.startswith("Nare Head (Roseland)")
    assert chart.feature("nare-head").lat_deg > chart.feature("nare-point").lat_deg + 0.1


# ---------------------------------------------------------------------------
# The World, the readings and the log
# ---------------------------------------------------------------------------


def test_the_readings_on_a_ship_with_a_chart_and_on_one_without():
    with_chart = chart_world(50.12, -5.03)
    r = with_chart.readings
    assert 15.0 < r["depth_of_water"] < 25.0
    assert r.words("depth_of_water").endswith("fathoms") or "and a half" in r.words(
        "depth_of_water"
    )
    assert r["land"]["in_sight"] is True and r["land"]["nearest"]["id"] in {
        "pendennis-castle",
        "black-rock-falmouth",
        "st-anthony-head",
        "pendennis-point",
        "st-mawes-castle",
    }
    assert r["in_sight"]["count"] >= 3 and "bearing" in r["in_sight"]["words"]
    assert [x.kind for x in R.REGISTRY.by_words("the land")] == ["sight"]
    assert [x.kind for x in R.REGISTRY.by_words("the depth of water")] == ["depth"]
    assert not R.REGISTRY.get("depth").is_absent  # the lead's cast, package 33a's
    assert with_chart.readings["depth"] is None  # no cast yet
    without = make_world(7, SCHOONER, Scenario(gustiness=0.0, variability=0.0))
    assert without.readings["depth_of_water"] is None and without.readings["land"] is None
    assert without.readings.words("land") == R.NO_CHART_WORDS
    # the snapshot carries the lookout and the reckoning, and not the truth's position
    # (spec §17; package 33a took it out): the truth is in the world and the tests only
    from freesail.api import queries

    snap = queries.snapshot(with_chart)
    assert "position" not in snap and snap["lookout"]["count"] >= 3
    assert snap["reckoning"]["words"].endswith("by account")
    assert snap["ship"]["x"] is None and snap["ship"]["y"] is None
    assert queries.snapshot(without)["reckoning"] is None
    assert queries.snapshot(without)["lookout"] is None
    block = queries.chart_block(with_chart)
    assert block["region"] == REGION and len(block["coast"]) > 100 and len(block["features"]) >= 150
    assert queries.chart_block(without) is None
    assert any(line.startswith("In sight:") for line in with_chart.summary_lines())


def test_the_dialect_reads_the_land_and_the_depth_of_water():
    """The rows `the land` and `the depth of water` (kinds `sight` and `depth`, package 32)
    are the standing dialect's for nothing, as every reading is (spec M5 §15; the two hunks
    the package's report named, applied by the lead at the merge after 31c landed): `when
    the land is in sight`, `when the land is not in sight`, `when the depth of water is under
    10 fathoms`, evaluated against the world's own readings."""
    from freesail.standing.grammar import parse_condition

    inshore = chart_world(50.12, -5.03)  # Falmouth's mouth: land in sight, shallow water
    offing = chart_world(49.0, -6.5)  # the Channel's mouth: nothing in sight, deep water
    for text, near, far in (
        ("the land is in sight", True, False),
        ("the land is not in sight", False, True),
        ("the depth of water is under 30 fathoms", True, False),
        ("the depth of water exceeds 30 fathoms", False, True),
    ):
        c = parse_condition(text, inshore.ship)
        assert c.holds(inshore.readings, {}) is near, text
        assert c.holds(offing.readings, {}) is far, text


def test_she_takes_the_ground_and_the_log_says_so_once_and_comes_off_again():
    w = chart_world(50.12, -5.03, heading=0.0)
    w.submit("set plain sail")
    for _ in range(4 * 3600):
        w.tick()
        if w._aground:
            break
    strikes = [e for e in w.log if e.kind == "ship.aground"]
    assert len(strikes) == 1 and strikes[0].severity.value == "urgent"
    assert (
        strikes[0].text.startswith("She has taken the ground") and "by the chart" in strikes[0].text
    )
    assert (
        strikes[0].data["depth_m"] <= strikes[0].data["draught_m"]
        and strikes[0].data["speed_kn"] > 0
    )
    # nothing stops her yet (package 34's consequences): she sails on and comes off
    w.run(600)
    assert len([e for e in w.log if e.kind == "ship.aground"]) == 1
    # the plane knows nothing of the ground
    plain = make_world(7, FRIGATE, Scenario(gustiness=0.0, variability=0.0, ship_heading_deg=0.0))
    plain.submit("set plain sail")
    plain.run(1800)
    assert not any(e.kind == "ship.aground" for e in plain.log)


def test_a_save_on_the_chart_replays_to_the_same_digest():
    from freesail.api.session import ship_factory
    from freesail.core import replay as replay_mod

    w = chart_world(49.90, -5.20, heading=45.0)
    w.submit("set plain sail")
    w.run(1500)
    data = w.save()
    assert data["scenario"]["region"] == REGION
    copy = replay_mod.replay(data, ship_factory)
    assert copy.position == w.position and copy.log.digest() == w.log.digest()
    assert [e.text for e in copy.log if e.kind == "lookout.sighting"] == [
        e.text for e in w.log if e.kind == "lookout.sighting"
    ]


# ---------------------------------------------------------------------------
# The coast-distance hook: the sea breeze and the coastal fog (W §1.4)
# ---------------------------------------------------------------------------


def high_over_the_channel(start: datetime) -> list[dict]:
    return [
        {
            "name": "the high",
            "kind": "high",
            "radius_km": 1200,
            "track": [{"at": start.isoformat(), "x_km": 0, "y_km": 0, "hpa": 1028}],
        }
    ]


def test_the_sea_breeze_blows_onshore_on_a_summer_afternoon_off_falmouth_and_not_at_night():
    """W §1.4: a summer, daylight, fine-weather wind of some ten knots at most, onshore,
    strongest in mid-afternoon, felt a few miles to sea and dying at dusk. Under a high
    with a slack gradient three kilometres off Falmouth at three in the afternoon the
    breeze blows toward the shore; at three in the morning, thirty kilometres out, and
    in January, there is none."""
    noon = datetime(1805, 6, 15, 12, 0)
    off_falmouth = (50.12, -5.03)  # three kilometres south of the harbour's mouth
    w = chart_world(*off_falmouth, ship=SCHOONER, start=noon, systems=high_over_the_channel(noon))
    assert w.systems is not None and w.systems.coast is not None
    coast = w.systems.coast_distance_km(0.0, 0.0)
    assert coast is not None and coast < SEA_BREEZE_REACH_KM
    at = datetime(1805, 6, 15, 15, 0)
    bx, by = w.systems.sea_breeze(0.0, 0.0, at)
    speed_kn = units.ms_to_knots(math.hypot(bx, by))
    assert 4.0 < speed_kn <= SEA_BREEZE_MAX_KN
    # onshore: toward the coast's bearing
    _, bearing = w.systems.coast(0.0, 0.0)
    breeze_toward = math.degrees(math.atan2(bx, by)) % 360.0
    assert abs(units.wrap_pi(math.radians(breeze_toward - bearing))) < math.radians(15.0)
    assert w.systems.sea_breeze(0.0, 0.0, datetime(1805, 6, 15, 3, 0)) == (0.0, 0.0)
    assert w.systems.sea_breeze(0.0, 0.0, datetime(1805, 1, 15, 15, 0)) == (0.0, 0.0)
    far_x = 0.0
    far_y = -40.0  # forty kilometres to seaward
    assert w.systems.sea_breeze(far_x, far_y, at) == (0.0, 0.0)
    # the surface wind at the ship carries it: the wind at three has an onshore part the
    # wind at three in the morning has not
    d_pm, s_pm = w.systems.surface_wind_at(0.0, 0.0, at)
    d_am, s_am = w.systems.surface_wind_at(0.0, 0.0, datetime(1805, 6, 15, 3, 0))
    assert (d_pm, s_pm) != (d_am, s_am)
    # without a chart the same systems give no breeze at all (the plane is what it was)
    plain = World(
        seed=7,
        scenario=Scenario(
            start_time=noon, gustiness=0.0, variability=0.0, systems=high_over_the_channel(noon)
        ),
    )
    assert plain.systems.coast is None and plain.systems.sea_breeze(0.0, 0.0, at) == (0.0, 0.0)


def test_coastal_fog_comes_near_the_coast_in_slack_stable_air_and_never_on_the_plane():
    """W §1.4: advection fog near the coasts in a stable warm sector or under a high with a
    slack gradient, most often in late spring and early summer; a fresh wind lifts it.
    Under a high off Falmouth in June some sky block of a fortnight brings fog; forty
    kilometres out, or in a fresh gradient, none; on the plane never."""
    start = datetime(1805, 6, 1, 0, 0)
    w = chart_world(50.12, -5.03, ship=SCHOONER, start=start, systems=high_over_the_channel(start))
    assert w.systems.coast_distance_km(0.0, 0.0) < FOG_COAST_KM
    hours = [start.replace(day=1 + h // 24, hour=h % 24) for h in range(14 * 24)]
    foggy = [t for t in hours if w.systems.coastal_fog(0.0, 0.0, t)]
    assert foggy, "no fog in a fortnight of June under a high off Falmouth"
    assert len(foggy) < len(hours) // 2
    assert not any(w.systems.coastal_fog(0.0, -70.0, t) for t in hours)  # seventy km out
    plain = Weather(start, None, seed=7, systems=high_over_the_channel(start))
    assert not any(plain.coastal_fog(0.0, 0.0, t) for t in hours)
    # the conditions carry it into the sky and the visibility, and the log
    w.run(1)
    seen = False
    for t in foggy[:1]:
        c = w.systems.conditions_at(0.0, 0.0, t)
        seen = c.weather == "fog" and c.visibility == "a cable" and c.sky == "thick"
    assert seen


def test_the_manifest_lists_the_c7_checks_and_the_chart_document_names_every_source(manifest):
    notes = manifest.get("notes") or {}
    assert notes and "unverified" in yaml.safe_dump(notes).lower()
    doc = (ROOT / "docs" / "references" / "Charts.md").read_text(encoding="utf-8")
    for sid, s in manifest["sources"].items():
        assert s["name"].split(",")[0].split(" (")[0] in doc, sid
    for name in ("Faden", "White", "Imray", "Mackenzie", "Spence", "Bellin"):
        assert name in doc


def test_the_manifest_tool_prints_every_source_and_the_attribution(capsys):
    """Spec M5 §20: a tool that prints the chart data's manifest and attribution
    (`tools/chart_manifest.py`): every source by name with its licence and its status, the
    region, the world and the Atlantic as not committed, and the attribution the game shows."""
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "chart_manifest", ROOT / "tools" / "chart_manifest.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    assert mod.main([]) == 0
    out = capsys.readouterr().out
    for words in (
        "GEBCO_2025 Grid",
        "EMODnet",
        "public domain",
        "channel-west",
        "not committed",
        "Attribution, as the game shows it",
    ):
        assert words in out, words
