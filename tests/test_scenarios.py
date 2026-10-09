"""The blocks' scenarios (spec M6 §26; docs/dev/ChartBlocks.md, item 8): each a free
passage of its block's stretch on the whole chart, read and begun in the fast tier; their
runs are measured once and recorded in docs/dev/TuningNotes.md, not pinned (not a gate's).

Package 39a: the Channel east, the frigate from Torbay to Guernsey through the Race.
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
    assert begin(world, sf) >= 10
    assert not [e for e in world.log if e.kind == "order.rejected"]
