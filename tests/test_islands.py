"""Package 39e: Madeira and the Western Islands (spec M6 §26, block 5 as decision 44
widened it). The two regions stand alone in the ocean beside the coast's blocks, their
marks with the lights dated out of 1805, the Peak of Pico seen to its own horizon in
clear weather, the ports Portuguese and neutral, the gauges read and held, Norie's hours
in the epitome, Fayal's channel stream in the directions, the scenarios loaded, and the
chart tool's tiles written so that the same arrays give the same bytes."""

from __future__ import annotations

import hashlib
import importlib.util
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pytest
import yaml

from freesail import units
from freesail.api.session import make_world
from freesail.core.world import Scenario
from freesail.world import chart as C
from freesail.world import tide as T
from freesail.world.geo import Position, destination, horizon_nm
from freesail.world.scenarios import begin, load_scenario, make_scenario_world

ROOT = Path(__file__).resolve().parents[1]
CHARTS = ROOT / "data" / "charts"
WHOLE = "atlantic-east"
ISLANDS = ["madeira", "azores"]
ISLANDS_PORTS = ["funchal", "porto-santo", "angra", "ponta-delgada", "horta"]
FUNCHAL_ROAD = {"lat_deg": 32.6380, "lon_deg": -16.9060}
ANGRA_ROAD = {"lat_deg": 38.6440, "lon_deg": -27.2160}
FRIGATE = "data/ships/frigate-36.yaml"
SCHOONER = "data/ships/topsail-schooner.yaml"


def build_tool():
    spec = importlib.util.spec_from_file_location(
        "build_charts", ROOT / "tools" / "build_charts.py"
    )
    mod = importlib.util.module_from_spec(spec)
    sys.modules["build_charts"] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def manifest():
    return yaml.safe_load((CHARTS / "manifest.yaml").read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def whole():
    return C.load_chart(WHOLE)


def world_at(where, ship=FRIGATE, **kw):
    sc = Scenario(
        start_time=datetime(1805, 6, 15, 12, 0),
        wind_from_deg=45.0,
        wind_speed_kn=12.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=270.0,
        position=where,
        chart=WHOLE,
        **kw,
    )
    return make_world(7, ship, sc)


def test_the_islands_stand_alone_in_the_chart_after_the_coasts_blocks(manifest, whole):
    """The two regions, built from their own fetches, listed after the coast's blocks;
    none of their tiles is another region's (no neighbour within a degree), their fill
    raised to the chart's datum; the recipe's corridor reaches 32 W (its tiles the
    owner's to commit: package 39e's report)."""
    tool = build_tool()
    assert manifest["charts"][WHOLE]["regions"][-2:] == ISLANDS
    others = {r for r in manifest["regions"] if r not in ISLANDS}
    for name in ISLANDS:
        spec = manifest["regions"][name]
        assert spec["bounds"] == tool.REGIONS[name]["bounds"] and spec["fill_to_chart_datum"]
        assert tool.tiles_listed_elsewhere(name, manifest["regions"]).isdisjoint(
            {f"{lv}/{t['name']}" for lv, ts in spec["tiles"].items() for t in ts}
        )
        for lv, ts in spec["tiles"].items():
            assert ts and all((CHARTS / "tiles" / lv / f"{t['name']}.npz").exists() for t in ts)
        assert not set(spec["harbours"]) & {
            h for o in others for h in manifest["regions"][o]["harbours"]
        }
    assert len(manifest["regions"]["madeira"]["tiles"]["2"]) == 25
    assert len(manifest["regions"]["azores"]["tiles"]["2"]) == 153
    assert tool.CORRIDORS["atlantic-corridor"]["bounds"]["west"] == -32.0
    assert whole.region_at(Position(32.64, -16.91)) == "madeira"
    assert whole.region_at(Position(38.65, -27.22)) == "azores"
    assert whole.level_at(Position(38.645, -27.22)) == 3  # Angra's harbour patch


def test_no_light_of_the_islands_was_lit_in_1805_and_the_peaks_are_marks(whole):
    """Madeira's first light was the Ponta de São Lourenço's of 1870, the Azores' the
    Ponta do Arnel's of 1876 (the encyclopaedia's pages): 1805 sees none of them, by day
    a tower not yet built is nothing; the islands' peaks are the marks."""
    lights = [
        f
        for fid, f in whole.features.items()
        if whole.region_of[fid] in ISLANDS and f.kind == "light"
    ]
    assert len(lights) == 10
    assert all(not f.lit_in(1805) and int(f.lit["from"]) >= 1870 for f in lights)
    assert min(int(f.lit["from"]) for f in lights) == 1870
    assert whole.feature("arnel-light").lit["from"] == 1876
    for f in lights:
        assert C.Chart._seen_as(f, "night", 1805) is None
        assert C.Chart._seen_as(f, "day", 1805) is None
    peak = whole.feature("peak-of-pico")
    assert peak.kind == "hill" and peak.height_m == 2351 and "Tofiño 1789" in peak.source


def test_the_peak_of_pico_is_seen_to_its_own_horizon_in_clear_weather_and_no_farther(whole):
    """The brief: the landfall on Pico's peak, seen from thirty leagues in clear weather
    by the directions (Tofiño 1789: its tangent to the sea's horizon 32 leagues). The
    index search reached the horizon of an object of 300 m only, and the weather's
    clearest visibility is twelve miles: a peak taller than the search's reach is looked
    for wherever she is and, in clear weather, seen to its own geographic horizon."""
    peak = whole.feature("peak-of-pico")
    eye = 35.0
    limit_nm = horizon_nm(eye, peak.height)
    assert 112.0 < limit_nm < 114.0  # thirty-eight leagues from a frigate's masthead
    when = datetime(1805, 6, 19, 12, 0)

    def seen(nm, vis, daylight="day"):
        p = destination(peak.position, 100.0, nm * units.NAUTICAL_MILE)
        return "peak-of-pico" in {s.feature.id for s in whole.in_sight(p, eye, vis, daylight, when)}

    assert seen(limit_nm - 1.0, C.CLEAR_VISIBILITY_NM)
    assert not seen(limit_nm + 1.0, C.CLEAR_VISIBILITY_NM)
    assert seen(96.0, None)  # Tofiño's 32 leagues
    # thicker weather bounds it as it bounds the rest; the night as the land's rule
    assert not seen(10.0, 4.0) and seen(3.0, 4.0)
    assert not seen(5.0, C.CLEAR_VISIBILITY_NM, "night")
    # the Channel's charts hold no feature so tall: nothing its lookout sees moves
    assert C.load_chart("channel-west").tall == [] and C.load_chart("channel-mid").tall == []
    assert "peak-of-pico" in {f.id for f in whole.tall}


def test_the_roads_hold_the_pilots_depths_on_the_modern_grid(whole):
    """Funchal Road in eighteen to thirty fathoms, sand, south-east of the Loo (the
    Oriental Navigator 1801 p. 24); Porto Santo's twelve; Angra's thirty or forty brazas
    east of Monte Brasil and Fayal's thirty-five or forty a mile and a quarter off the
    town (Tofiño 1789), at the grid's depths within the features' rule (half the pilot's
    depth at the least)."""
    for fid, least_m, most_m in (
        ("funchal-road", 30.0, 70.0),
        ("porto-santo-road", 11.0, 40.0),
        ("angra-road", 27.0, 70.0),
        ("horta-road", 30.0, 70.0),
        ("ponta-delgada-road", 30.0, 70.0),
    ):
        f = whole.feature(fid)
        depth = whole.depth_at(f.position)
        assert depth is not None and least_m <= depth <= most_m, (fid, depth)
        assert f.bottom and whole.bottom_near(f.position)
    # the Formigas stand by their feature alone: the grid has no rock there
    formigas = whole.feature("formigas")
    assert whole.depth_at(formigas.position) > 30.0
    assert whole.danger_under(formigas.position, 0.0, 40.0, 5.0) is not None


def test_the_islands_ports_are_portuguese_neutral_and_stand_on_their_own_positions_too():
    """Five ports on 35's machinery, Portuguese: neutral to a King's ship and to an
    American (the nations' table: Portugal at war with nobody in 1805); on the whole
    chart their roads are the islands' features, on the Channel's chart alone their own
    positions, the same place; the datum unverified in every file (no sheet patched)."""
    whole = world_at(FUNCHAL_ROAD, ports=ISLANDS_PORTS)
    for pid in ISLANDS_PORTS:
        port = whole.ports.ports[pid]
        assert port.nation == "portugal" and whole.ports.stance(port) == "neutral"
        for key in ("outer_road", "anchorage", "shore"):
            spot = getattr(port, key)
            if spot.feature_id:
                f = whole.chart.feature(spot.feature_id)
                assert f is not None and f.position.lat_deg == pytest.approx(spot.position.lat_deg)
        doc = yaml.safe_load((ROOT / "data" / "ports" / f"{pid}.yaml").read_text(encoding="utf-8"))
        assert doc["datum"] == "unverified"
    assert whole.ports.nearest()[0].id == "funchal"
    neutral = world_at(FUNCHAL_ROAD, ship=SCHOONER, ports=ISLANDS_PORTS)
    assert all(neutral.ports.stance(neutral.ports.ports[p]) == "neutral" for p in ISLANDS_PORTS)


def test_the_islands_gauges_are_read_and_held_and_norie_gives_their_hours(tide=None):
    """TICON's five gauges of the islands in the eleven's form, held (no mean level was
    read: null, not invented); Norie's Table XLI of 1805 gives Funchal 12h 4m and 7 feet,
    Angra Bay 11h 45m and 8, Fayal Road 2h 20m and 4 1/2 (read from the page images)."""
    doc = yaml.safe_load(T.CONSTITUENTS_PATH.read_text(encoding="utf-8"))
    held = {g["id"]: g for g in doc["held_gauges"] if g["lon_deg"] < -15.0}
    assert list(held) == ["funchal", "ponta-delgada", "angra", "horta", "santa-cruz-das-flores"]
    for g in held.values():
        assert g["mean_level_m"] is None and g["record"].startswith("GESLA-2, UHSLC")
        for name in ("M2", "S2", "N2"):
            assert 0.05 < g[name]["amplitude_m"] < 0.8 and 25.0 < g[name]["phase_deg"] < 90.0
    assert len(doc["gauges"]) == 11 and not set(held) & {g["id"] for g in doc["gauges"]}
    # the springs' range at Funchal by its constants is Norie's seven feet
    springs_ft = (
        2.0 * (held["funchal"]["M2"]["amplitude_m"] + held["funchal"]["S2"]["amplitude_m"]) / 0.3048
    )
    assert springs_ft == pytest.approx(7.0, abs=0.6)
    est = yaml.safe_load(
        (ROOT / "data" / "tides" / "establishments.yaml").read_text(encoding="utf-8")
    )
    rows = {p["name"]: p for p in est["tables"]["norie"]["ports"]}
    assert (
        rows["Funchal"]["hw_h"],
        rows["Funchal"]["hw_m"],
        rows["Funchal"]["spring_rise_ft"],
    ) == (12, 4, 7)
    assert (rows["Angra Bay"]["hw_h"], rows["Angra Bay"]["hw_m"]) == (11, 45)
    assert (rows["Fayal Road"]["hw_h"], rows["Fayal Road"]["hw_m"]) == (2, 20)
    assert not any(
        p.get("rise_judgement")
        for n, p in rows.items()
        if n in ("Funchal", "Angra Bay", "Fayal Road")
    )


def test_fayals_channel_is_in_the_directions_and_the_open_sea_between_has_no_statement():
    """Tofiño's stream between Fayal and Pico (the flood N E, the ebb S W, three miles at
    the most) is an area of the world's and a statement of the master's; the islands'
    water is a box of the directions' own (`book_waters`), where only an area with a
    polygon answers: the open Channel's statement does not reach the ocean."""
    book = T.load_directions()
    channel = book.area_at(Position(38.52, -28.57))
    assert channel is not None and channel.id == "fayal-channel"
    assert (channel.set_point, channel.spring_kn) == ("NE", 3.0) and "Tofiño 1789" in channel.source
    assert book.area_at(Position(38.0, -27.0)) is None  # the islands' box, no area
    assert book.area_at(Position(40.0, -15.0)) is None  # the ocean between
    assert book.area_at(Position(49.3, -5.0)).id == "mid-channel"  # the Channel as before
    assert book.waters == ((36.5, 40.0, -31.5, -24.5),)


def test_a_tile_is_written_with_its_entries_dated_alike_so_the_same_arrays_give_the_same_bytes(
    tmp_path,
):
    """The tool's `save_tile` (package 39e): numpy's `savez_compressed` dated each entry
    with the clock, so a rebuild of the same arrays had other bytes; every tile the tool
    writes now gives the same bytes for the same arrays, read back by `np.load` as
    before."""
    tool = build_tool()
    arrays = {
        "elevation": np.arange(64, dtype=np.int16).reshape(8, 8),
        "dist": np.ones((8, 8), dtype=np.uint16),
        "min_depth_m": np.float32(12.5),
    }
    tool.save_tile(tmp_path / "a.npz", **arrays)
    tool.save_tile(tmp_path / "b.npz", **arrays)
    a, b = (tmp_path / "a.npz").read_bytes(), (tmp_path / "b.npz").read_bytes()
    assert hashlib.sha256(a).digest() == hashlib.sha256(b).digest()
    z = np.load(tmp_path / "a.npz")
    assert z.files == list(arrays) and float(z["min_depth_m"]) == 12.5
    assert np.array_equal(z["elevation"], arrays["elevation"])


@pytest.mark.parametrize("name", ["madeira", "azores"])
def test_the_islands_scenarios_load_on_the_whole_chart_in_the_islands_water(name):
    """The schooner's Funchal to Porto Santo and back, the frigate's Funchal to Angra: a
    free passage each on the whole chart from Funchal Road, its book's places named on
    the chart."""
    sf = load_scenario(ROOT / "data" / "scenarios" / f"{name}.yaml")
    assert sf.scenario.chart == WHOLE and sf.seed == 7
    assert f"data/scenarios/{name}.orders" in sf.standing_orders
    w = make_scenario_world(sf)
    assert w.chart.region_at(w.position) == "madeira"
    assert w.chart.level_at(w.position) == 3  # Funchal's harbour patch
    for place in ("Funchal Road", "Porto Santo Road", "Angra Road"):
        assert w.chart.find_feature(place) is not None, place
    assert {w.ports.stance(p) for p in w.ports.ports.values()} == {"neutral"}
    # the book is read whole, every order accepted by the dialect
    assert begin(w, sf) >= 4
    assert not [e for e in w.log if e.kind == "order.rejected"]
