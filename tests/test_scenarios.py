"""The blocks' scenarios (spec M6 §26; docs/dev/ChartBlocks.md, item 8): each a free
passage of its block's stretch on the whole chart, read and begun in the fast tier; their
runs are measured once and recorded in docs/dev/TuningNotes.md, not pinned (not a gate's).

Package 39a: the Channel east, the frigate from Torbay to Guernsey through the Race.
Package 39d: Portugal and Cadiz, the schooner from Oporto to Lisbon.
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


# Package 39d: Portugal and Cadiz, the schooner from Oporto to Lisbon.
PORTUGAL = ROOT / "data" / "scenarios" / "portugal.yaml"


def test_portugal_is_a_passage_on_the_whole_chart_from_oporto_to_the_road_of_belem():
    """The scenario names the chart, starts in the road off the bar of Oporto on the
    block's harbour patch, loads Oporto and Lisbon (Portuguese, neutral to the American)
    and its own book; the road of Belém is the chart's by name, the bar of Lisbon the
    block's water with its stream; the book is read whole."""
    sf = load_scenario(PORTUGAL)
    sc = sf.scenario
    assert sc.chart == "atlantic-east" and sf.seed == 7
    assert sf.standing_orders == ["data/scenarios/portugal.orders"]
    world = make_scenario_world(sf)
    chart = world.chart
    assert "portugal" in chart.regions and chart.region_at(world.position) == "portugal"
    start = world.position
    assert chart.level_at(start) == 3  # the oporto-douro harbour patch
    assert 10.0 < chart.depth_at(start) < 25.0
    assert list(world.ports.ports) == ["oporto", "lisbon"]
    assert {world.ports.stance(p) for p in world.ports.ports.values()} == {"neutral"}
    road = chart.find_feature("the road of Belém")
    assert road is not None and road.id == "belem-road"
    _, run_m = bearing_and_distance(start, road.position)
    assert 145.0 < run_m / 1852.0 < 160.0  # a hundred and fifty miles direct
    bar = Position(38.655, -9.33)
    assert chart.depth_at(bar) > 10.0 and world.tide.area_at(bar).id == "tagus-bar"
    assert begin(world, sf) >= 10
    assert not [e for e in world.log if e.kind == "order.rejected"]


# ---------------------------------------------------------------------------
# Package 59 (spec M7b §21e): a scenario written as well as read
# ---------------------------------------------------------------------------

SCENARIOS = ROOT / "data" / "scenarios"
THE_FOUR = ("smack-falmouth", "lugger-roscoff", "directed-passage", "dispatches-falmouth")


def test_every_scenario_of_the_game_is_written_again_byte_for_byte_with_nothing_changed():
    """The maker's promise (truth 7b-109's half): the text a file's fields were read from,
    written with those same fields, is the same text, every comment kept."""
    from freesail.world.scenarios import read_scenario_text, scenario_text

    files = sorted(SCENARIOS.glob("*.yaml"))
    assert len(files) > 25
    for path in files:
        text, fields = read_scenario_text(path)
        assert scenario_text(fields, text) == text, path.name


def test_a_change_rewrites_its_own_field_and_keeps_every_other_line_and_comment():
    from freesail.world.scenarios import read_scenario_text, scenario_text

    text, fields = read_scenario_text(SCENARIOS / "directed-passage.yaml")
    fields["seed"] = 9
    fields["position"] = {"lat_deg": 50.0, "lon_deg": -5.1}
    fields["stations"] = {"officer": "player", "captain": "model"}
    del fields["ships"]
    out = scenario_text(fields, text)
    old, new = text.splitlines(), out.splitlines()
    assert "seed: 9" in new and "seed: 7" not in new
    # the comment beside the position kept on its new line
    assert any(
        ln.startswith("position: {lat_deg: 50.0, lon_deg: -5.1}") and "Imray 1874" in ln
        for ln in new
    )
    # the other sail gone with its comment; the stations put in before the director
    assert "ships:" not in new and not any("merchant passage's dozen" in ln for ln in new)
    assert new.index("stations: {officer: player, captain: model}") < new.index("director:")
    # every other line as it was, the header and the weather's comments among them
    kept = [ln for ln in old if ln in new]
    assert old[:12] == new[:12] and len(kept) > len(old) - 40


def test_a_new_scenario_is_in_the_hands_form_and_loads_as_the_hand_written_one(tmp_path):
    """Written from the fields alone (a new file), each of the owner's scenarios loads to
    the same Scenario as its hand-written file, and reads back to itself."""
    from freesail.world.scenarios import read_scenario_text, scenario_text, write_scenario

    for stem in THE_FOUR:
        text, fields = read_scenario_text(SCENARIOS / f"{stem}.yaml")
        path = write_scenario(fields, tmp_path / f"{stem}.yaml")
        new = path.read_text(encoding="utf-8")
        assert new.startswith("# FreeSail: ") and "py -m freesail.ui.server --scenario" in new
        assert "# The ship: her file" in new
        assert (
            load_scenario(path).scenario.__dict__
            == load_scenario(SCENARIOS / f"{stem}.yaml").scenario.__dict__
        )
        again_text, again = read_scenario_text(path)
        assert scenario_text(again, again_text) == new


def test_a_windows_written_file_keeps_its_line_endings(tmp_path):
    from freesail.world.scenarios import newline_of, read_scenario_text, write_scenario

    src = tmp_path / "crlf.yaml"
    src.write_bytes((SCENARIOS / "smack-falmouth.yaml").read_bytes().replace(b"\n", b"\r\n"))
    text, fields = read_scenario_text(src)
    assert newline_of(src) == "\r\n"
    out = write_scenario(fields, tmp_path / "out.yaml", text, newline=newline_of(src))
    assert out.read_bytes() == src.read_bytes()


def test_the_stations_and_who_holds_them_are_read_and_the_players_seat_given(tmp_path):
    from freesail.world.scenarios import ScenarioError

    p = tmp_path / "s.yaml"
    p.write_text("name: s\nstations: {captain: model, officer: player, director: model}\n")
    sf = load_scenario(p)
    assert sf.stations == {"captain": "model", "officer": "player", "director": "model"}
    assert sf.player_seat == "officer"
    p.write_text("name: s\nstations: {captain: player}\n")
    assert load_scenario(p).player_seat is None  # the captain at the prompt is no seat
    for bad, words in (
        ("stations: {officer: player, director: player}", "one station"),
        ("stations: {officer: somebody}", "not a holder"),
        ("stations: [officer]", "a mapping"),
    ):
        p.write_text(f"name: s\n{bad}\n")
        try:
            load_scenario(p)
        except ScenarioError as e:
            assert words in str(e)
        else:
            raise AssertionError(bad)


def test_a_scenarios_seat_is_the_players_at_either_driver_unless_the_flag_says_otherwise(
    tmp_path,
):
    from freesail.ui.server import prepare_game, server_parser

    p = tmp_path / "seated.yaml"
    text = (SCENARIOS / "lesson-falmouth.yaml").read_text(encoding="utf-8")
    p.write_text(text + "\nstations: {officer: player}\n", encoding="utf-8")
    args = server_parser().parse_args(["--scenario", str(p)])
    world = prepare_game(args, say=lambda line: None)
    assert world.player_seat.station.name == "officer of the watch"
    args = server_parser().parse_args(["--scenario", str(p), "--seat", "captain"])
    world = prepare_game(args, say=lambda line: None)
    assert getattr(world, "player_seat", None) is None  # the flag wins over the file
