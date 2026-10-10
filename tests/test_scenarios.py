"""The blocks' scenarios (spec M6 §26; docs/dev/ChartBlocks.md, item 8): each a free
passage of its block's stretch on the whole chart, read and begun in the fast tier; their
runs are measured once and recorded in docs/dev/TuningNotes.md, not pinned (not a gate's).

Package 39a: the Channel east, the frigate from Torbay to Guernsey through the Race.
Package 39f: the Strait, the frigate from off Cape Trafalgar to Gibraltar road.
"""

from __future__ import annotations

from pathlib import Path

from freesail.world.geo import Position, bearing_and_distance
from freesail.world.scenarios import begin, load_scenario, make_scenario_world

ROOT = Path(__file__).resolve().parents[1]
CHANNEL_EAST = ROOT / "data" / "scenarios" / "channel-east.yaml"


def test_the_channel_east_is_a_passage_on_the_whole_chart_from_torbay_to_guernsey():
    """The scenario names the chart (`chart: atlantic-east`), starts in Brixham road on the
    Channel east's harbour patch, loads its six British ports and its own book, and its
    marks are the chart's: the Great Road of Guernsey by name, the Race's water deep."""
    sf = load_scenario(CHANNEL_EAST)
    sc = sf.scenario
    assert sc.chart == "atlantic-east" and sf.seed == 7
    assert sf.standing_orders == ["data/scenarios/channel-east.orders"]
    world = make_scenario_world(sf)
    chart = world.chart
    assert chart.name == "atlantic-east" and "channel-mid" in chart.regions
    start = world.position
    assert chart.level_at(start) == 3  # the dartmouth-torbay harbour patch
    assert 9.0 < chart.depth_at(start) < 16.0  # Brixham road, six fathoms or so
    assert list(world.ports.ports) == [
        "torbay",
        "dartmouth",
        "weymouth",
        "alderney",
        "st-peter-port",
        "st-helier",
    ]
    assert {world.ports.stance(p) for p in world.ports.ports.values()} == {"open"}
    road = chart.find_feature("the Great Road of Guernsey")
    assert road is not None and road.id == "guernsey-great-road"
    _, run_m = bearing_and_distance(start, road.position)
    assert 60.0 < run_m / 1852.0 < 75.0  # sixty-eight miles direct, some ninety by the Race
    race = Position(49.70, -2.06)
    assert chart.region_at(race) == "channel-mid" and chart.depth_at(race) > 30.0
    assert world.tide.area_at(race).id == "alderney-race"
    # the book is read whole, every order accepted by the dialect
    # the weather: the Strait's southern half lies in no box and takes the nearest
    from freesail.world.weather import load_climatology

    boxes = load_climatology()
    assert boxes.box_at(36.2, -5.5).name == boxes.box_at(35.7, -5.5).name == "portugal"
    assert not boxes.boxes["portugal"].contains(35.7, -5.5)
    assert begin(world, sf) >= 10
    assert not [e for e in world.log if e.kind == "order.rejected"]


# Package 39f: the Strait, the frigate from off Cape Trafalgar to Gibraltar road.
STRAIT = ROOT / "data" / "scenarios" / "strait.yaml"


def test_the_strait_is_a_passage_on_the_whole_chart_from_off_trafalgar_to_gibraltar_road():
    """The scenario names the chart, starts under way in the block's own water five miles
    south-west of Cape Trafalgar (Cadiz bay is the block `portugal`'s), loads the block's
    five ports and its own book, and its marks are the chart's: Gibraltar road by name,
    the middle of the Strait with its current setting east under her."""
    sf = load_scenario(STRAIT)
    sc = sf.scenario
    assert sc.chart == "atlantic-east" and sf.seed == 7 and sc.nation == "britain"
    assert sf.standing_orders == ["data/scenarios/strait.orders"]
    world = make_scenario_world(sf)
    chart = world.chart
    assert "strait" in chart.regions
    start = world.position
    assert chart.region_at(start) == "strait" and start.lat_deg < 36.4
    assert chart.depth_at(start) > 20.0
    assert list(world.ports.ports) == ["gibraltar", "tarifa", "algeciras", "ceuta", "tangier"]
    assert world.ports.stance(world.ports.ports["gibraltar"]) == "open"
    road = chart.find_feature("Gibraltar road")
    assert road is not None and road.id == "gibraltar-road"
    _, run_m = bearing_and_distance(start, road.position)
    assert 35.0 < run_m / 1852.0 < 45.0  # thirty-nine miles direct, some forty-five by the book
    middle = Position(35.96, -5.55)
    assert world.tide.area_at(middle).id == "strait-middle"
    assert world.tide.area_at(middle).current_kn == 2.0
    assert begin(world, sf) >= 10
    assert not [e for e in world.log if e.kind == "order.rejected"]
