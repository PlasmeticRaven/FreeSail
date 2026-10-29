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
    assert list(world.dealings.ports) == [
        "torbay",
        "dartmouth",
        "weymouth",
        "alderney",
        "st-peter-port",
        "st-helier",
    ]
    assert {world.dealings.stance(p) for p in world.dealings.ports.values()} == {"open"}
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
    assert list(world.dealings.ports) == ["gibraltar", "tarifa", "algeciras", "ceuta", "tangier"]
    assert world.dealings.stance(world.dealings.ports["gibraltar"]) == "open"
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
    assert list(world.dealings.ports) == ["oporto", "lisbon"]
    assert {world.dealings.stance(p) for p in world.dealings.ports.values()} == {"neutral"}
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


def test_a_scenario_ship_takes_a_free_intent_which_the_rules_captain_does_not_sail(tmp_path):
    """2026-10-27: a scenario's ship takes `free_intent:` in any words, the goal a model
    at her captain's station is told (world orders are the director's, so a scenario is
    where the player gives it). The rules-based captain does not sail by it, even where
    its words are a form he knows: she lies to, and is not taken off the sea as a voyage
    done. The scenario's lines say so. An intent and a free intent together, or an empty
    one, are refused in words when the scenario is read."""
    from freesail.world.captains import FREE
    from freesail.world.scenarios import ScenarioError

    base = CHANNEL_EAST.read_text(encoding="utf-8")
    goal = "find the smuggler's lugger said to be running brandy into Cawsand"
    p = tmp_path / "free.yaml"
    p.write_text(
        base
        + "\nships:\n"
        + "  - {description: cutter, name: Raven, nation: britain, position: 50 25 N 3 27 W,\n"
        + f'     goal: "bound for Dartmouth", free_intent: "{goal}"}}\n'
        + "  - {description: cutter, name: Lark, nation: britain, position: 50 24 N 3 26 W,\n"
        + '     goal: "bound for Dartmouth", free_intent: "bound for Dartmouth"}\n',
        encoding="utf-8",
    )
    sf = load_scenario(p)
    assert any(
        f"Free intent: {goal} (the rules-based captain will not follow it)" in ln
        for ln in sf.lines()
    )
    world = make_scenario_world(sf)
    raven, lark = world.vessels.find("Raven"), world.vessels.find("Lark")
    assert raven.brain.intent.kind == FREE and raven.brain.intent.words == goal
    assert raven.intent_words == goal
    # a form he knows, given as a free intent, is free all the same
    assert lark.brain.intent.kind == FREE
    world.run(120)
    for v in (raven, lark):
        assert not v.done and v.plan and v.plan[0][0] == "lie_to"
    for bad, words in (
        ('intent: "bound for Dartmouth", free_intent: "anything"', "not both"),
        ('free_intent: "  "', "the ship's goal in words"),
    ):
        p.write_text(
            base
            + "\nships:\n"
            + "  - {description: cutter, name: Raven, nation: britain, position: 50 25 N 3 27 W,\n"
            + f'     goal: "bound for Dartmouth", {bad}}}\n',
            encoding="utf-8",
        )
        try:
            load_scenario(p)
        except ScenarioError as e:
            assert words in str(e), str(e)
        else:
            raise AssertionError(bad)


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


def test_a_merchant_brig_free_sails_a_merchant_brigs_own_file():
    """Package 68 (the cold review of 2026-10-22, R-63): "A merchant brig, free" sailed H.M.
    brig-sloop Harpy's file (121 men with 20 marines, a commander and a surgeon, the Navy's
    books and a 32-ton hold) under the American colours, and the director called her a
    king's ship. She sails a merchant brig's own file through tools/gen_ships.py: the
    Harpy's hull and rig, a master's and mates' company of sixteen, no marines, a
    merchant's stores and the trader's hold."""
    import yaml

    sf = load_scenario("data/scenarios/merchant-brig.yaml")
    assert sf.ship_file == "data/ships/merchant-brig.yaml"
    with open("data/ships/merchant-brig.yaml", encoding="utf-8") as f:
        doc = yaml.safe_load(f)
    crew = doc["crew"]
    assert crew["complement"] == 16 and "marines" not in crew["stations"]
    assert crew["names"] == "american" and crew["ration"]["table"] == "navy"
    assert doc["hold"]["capacity_tons"] > 100
    with open("data/ships/brig.yaml", encoding="utf-8") as f:
        harpy = yaml.safe_load(f)
    assert doc["hull"] == harpy["hull"] and doc["spars"] == harpy["spars"]
    world = make_scenario_world(sf)
    begin(world, sf)
    roles = [p.role for p in world.people.all]
    assert roles[:5] == ["master", "mate", "second mate", "boatswain", "carpenter"]
    assert world.people.captain.role == "master"
    assert not set(roles) & {"commander", "lieutenant", "surgeon", "purser", "gunner"}


# Package 79b: the Channel's east block, the frigate from the Downs to Spithead.
SPITHEAD = ROOT / "data" / "scenarios" / "spithead.yaml"


def test_spithead_is_a_passage_on_the_whole_chart_from_the_downs_to_spithead():
    """The scenario names the chart, starts at anchor in the Downs on the block's harbour
    patch, loads the block's eight ports and its own book, and its marks are the chart's:
    Spithead by name in the patch west of 1 W, the Strait's water between, the Channel's
    weather box over the whole of it."""
    sf = load_scenario(SPITHEAD)
    sc = sf.scenario
    assert sc.chart == "atlantic-east" and sf.seed == 7 and sc.nation == "britain"
    assert sf.standing_orders == ["data/scenarios/spithead.orders"]
    world = make_scenario_world(sf)
    chart = world.chart
    assert "channel-east" in chart.regions
    start = world.position
    assert chart.region_at(start) == "channel-east" and chart.level_at(start) == 3  # the Downs
    assert 9.0 < chart.depth_at(start) < 20.0  # seven or eight fathoms
    assert list(world.dealings.ports) == [
        "downs",
        "dover",
        "portsmouth",
        "poole",
        "boulogne",
        "calais",
        "dunkirk",
        "le-havre",
    ]
    road = chart.find_feature("Spithead")
    assert road is not None and road.id == "spithead"
    assert chart.level_at(road.position) == 3 and chart.region_at(road.position) == "channel-mid"
    _, run_m = bearing_and_distance(start, road.position)
    assert 100.0 < run_m / 1852.0 < 125.0  # some hundred and twelve miles direct
    strait = Position(51.0, 1.45)
    assert world.tide.area_at(strait).id == "strait-of-dover"
    from freesail.world.weather import load_climatology

    assert load_climatology().box_at(51.05, 2.37).name == "channel"
    assert begin(world, sf) >= 10
    assert not [e for e in world.log if e.kind == "order.rejected"]


# Package 79c: the Mediterranean west, the frigate from Gibraltar bay to Port Mahon.
MAHON = ROOT / "data" / "scenarios" / "mahon.yaml"


def test_mahon_is_a_passage_on_the_whole_chart_from_gibraltar_road_to_port_mahon():
    """The scenario names the chart, starts at anchor in Gibraltar road (the Strait's patch),
    loads Gibraltar and the block's eight ports and its own book, every order of which is
    taken, and its mark is the chart's: the anchorage off the mouth of Port Mahon by name in
    the Balearics' patch, some five hundred and ten miles direct, the block's two regions
    and its own weather box between."""
    sf = load_scenario(MAHON)
    sc = sf.scenario
    assert sc.chart == "atlantic-east" and sf.seed == 7 and sc.nation == "britain"
    assert sf.standing_orders == ["data/scenarios/mahon.orders"]
    world = make_scenario_world(sf)
    chart = world.chart
    assert {"mediterranean-west", "balearics"} <= set(chart.regions)
    start = world.position
    assert chart.region_at(start) == "strait" and chart.level_at(start) == 3
    assert list(world.dealings.ports) == [
        "gibraltar",
        "algeciras",
        "malaga",
        "almeria",
        "cartagena",
        "ivica",
        "palma",
        "port-mahon",
        "oran",
        "algiers",
    ]
    mouth = chart.find_feature("the anchorage off the mouth of Port Mahon")
    assert mouth is not None and mouth.id == "mahon-outer-road"
    assert chart.level_at(mouth.position) == 3 and chart.region_at(mouth.position) == "balearics"
    _, run_m = bearing_and_distance(start, mouth.position)
    assert 490.0 < run_m / 1852.0 < 530.0  # some five hundred and ten miles direct
    from freesail.world.weather import load_climatology

    clim = load_climatology()
    assert clim.box_at(36.6, -3.0).name == clim.box_at(39.86, 4.32).name == "mediterranean-west"
    assert begin(world, sf) >= 10
    assert not [e for e in world.log if e.kind == "order.rejected"]
