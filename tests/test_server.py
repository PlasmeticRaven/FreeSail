"""The server's routes and websocket, and the snapshot and ship-graph shapes."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from freesail.api import queries
from freesail.api.session import make_world
from freesail.core.world import Scenario, World
from freesail.ui.server import CLIENT_DIR, Driver, create_app, snapshot_interval

ROOT = Path(__file__).resolve().parents[1]
SHIPS = [ROOT / "data/ships/frigate-36.yaml", ROOT / "data/ships/topsail-schooner.yaml"]

SNAPSHOT_SHIP_KEYS = {
    "name",
    "x",
    "y",
    "heading",
    "speed_through_water",
    "leeway",
    "heel",
    "rudder",
    "weather_helm",
    "tack",
    "helm_mode",
    "target_heading",
}
SNAPSHOT_WIND_KEYS = {
    "true_from",
    "true_speed",
    "mean_speed",
    "gust_factor",
    "apparent_angle",
    "apparent_speed",
}
SNAPSHOT_SAIL_KEYS = {
    "id",
    "class",
    "state",
    "reefs",
    "area_effective",
    "thrust",
    "side",
    "strain_ratio",
    "backed",
    "sheet_angle",
}
SNAPSHOT_SPAR_KEYS = {"id", "class", "state", "condition", "strain_ratio", "brace_angle"}
SNAPSHOT_LINE_KEYS = {"id", "class", "state", "strain_ratio", "hauled"}
GRAPH_SPAR_KEYS = {
    "id",
    "class",
    "x_m",
    "height_m",
    "length_m",
    "parent",
    "side",
    "brace_angle",
    "brace_limit",
    "rating_kn",
}
GRAPH_SAIL_KEYS = {
    "id",
    "class",
    "roles",
    "area_m2",
    "x_m",
    "centre_height_m",
    "reef_bands",
    "reef_factor",
    "side",
    "state",
    "reefs",
    "sheet_angle",
}


def world_for(path: Path, heading: float = 293.0) -> World:
    return make_world(
        7, path, Scenario(wind_from_deg=0.0, wind_speed_kn=15.0, ship_heading_deg=heading)
    )


@pytest.fixture(params=SHIPS, ids=[p.stem for p in SHIPS])
def world(request) -> World:
    return world_for(request.param)


@pytest.fixture
def client(world):
    driver = Driver(world)
    app = create_app(driver)
    with TestClient(app) as c:
        yield c


# -- queries ---------------------------------------------------------------------


def test_snapshot_shape(world):
    world.submit("set plain sail")
    world.run(30)
    snap = queries.snapshot(world)
    assert {"tick", "ship_time", "stamp", "bell", "ship", "wind", "sails", "spars", "lines"} <= set(
        snap
    )
    assert snap["tick"] == 30
    assert SNAPSHOT_SHIP_KEYS <= set(snap["ship"])
    assert SNAPSHOT_WIND_KEYS <= set(snap["wind"])
    assert len(snap["sails"]) == len(world.ship.sails)
    assert len(snap["spars"]) == len(world.ship.spars)
    assert len(snap["lines"]) == len(world.ship.lines)
    for s in snap["sails"]:
        assert SNAPSHOT_SAIL_KEYS <= set(s)
    for s in snap["spars"]:
        assert SNAPSHOT_SPAR_KEYS <= set(s)
        assert s["state"] in {"sound", "wrecked", "sent_down"}
    for ln in snap["lines"]:
        assert SNAPSHOT_LINE_KEYS <= set(ln)
    assert snap["evolutions_in_progress"], "set plain sail should be in hand"
    evo = snap["evolutions_in_progress"][0]
    assert {"id", "subject", "step", "remaining_s", "waiting"} <= set(evo)
    assert snap["bell"]["watch"] == "Morning watch"
    assert snap["bell"]["bells"] == 8
    json.dumps(snap)  # serialisable


def test_snapshot_is_si(world):
    snap = queries.snapshot(world)
    assert abs(snap["ship"]["heading"] - 5.1138) < 0.01  # 293 degrees in radians
    assert abs(snap["wind"]["true_speed"] - 7.7167) < 0.01  # 15 knots in m/s


def test_ship_graph_shape(world):
    g = queries.ship_graph(world.ship)
    assert {"name", "rig", "hull", "spars", "sails", "lines", "groups", "aliases"} <= set(g)
    assert {"length_waterline_m", "beam_m", "draught_m", "deck_height_m"} <= set(g["hull"])
    for s in g["spars"]:
        assert GRAPH_SPAR_KEYS <= set(s)
    for s in g["sails"]:
        assert GRAPH_SAIL_KEYS <= set(s)
        for role, target in s["roles"].items():
            ids = {p["id"] for p in g["spars"]} | {ln["id"] for ln in g["lines"]}
            assert target in ids, f"{s['id']} role {role} -> {target} is not a part"
    root_classes = {"mast", "bowsprit"}
    for s in g["spars"]:
        if s["parent"] is None:
            assert s["class"] in root_classes
        else:
            assert s["parent"] in {p["id"] for p in g["spars"]}
    square = [s for s in g["sails"] if s["class"] == "square"]
    assert square and all(s["reef_factor"] > 0 for s in square)
    json.dumps(g)


def test_snapshot_reflects_state_changes(world):
    world.submit("set plain sail")
    world.run(900)
    world.submit("brace sharp up on the starboard tack")
    world.run(120)
    snap = queries.snapshot(world)
    set_ids = {s["id"] for s in snap["sails"] if s["state"] == "set"}
    assert set(world.ship.groups["plain sail"]) <= set_ids
    yards = [s for s in snap["spars"] if s["class"] == "yard"]
    assert all(s["brace_angle"] > 0.3 for s in yards)


def test_snapshot_on_the_point_ship():
    w = World(seed=1)
    snap = queries.snapshot(w)
    assert snap["sails"] == [] and snap["spars"] == []
    assert SNAPSHOT_SHIP_KEYS <= set(snap["ship"])


# -- the driver ------------------------------------------------------------------


def test_snapshot_interval_cadence():
    assert snapshot_interval(1) == 1
    assert snapshot_interval(9.9) == 1
    assert snapshot_interval(10) == 10
    assert snapshot_interval(60) == 60
    assert snapshot_interval(600) == 60


def test_driver_emits_snapshots_at_the_cadence():
    d = Driver(world_for(SHIPS[0]), compression=10)
    got: list[dict] = []
    d.add_listener(got.append)
    d.running = True
    d._run_ticks(30)
    snaps = [m for m in got if m["type"] == "snapshot"]
    assert [m["snapshot"]["tick"] for m in snaps] == [10, 20, 30]
    d.submit("set the jib")
    events = [m for m in got if m["type"] == "event"]
    assert [e["event"]["kind"] for e in events][:1] == ["order.accepted"]
    assert got[-1]["type"] == "snapshot", "an order is followed by a snapshot at once"


def test_driver_tick_holds_the_clock():
    d = Driver(world_for(SHIPS[1]))
    d.running = True
    d.tick(5)
    assert d.running is False
    assert d.world.clock.tick == 5


# -- routes ------------------------------------------------------------------------


def test_index_serves_the_client(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "FreeSail" in r.text
    assert "projection.js" in r.text
    for name in ("app.js", "projection.js", "shipview.js", "log.js", "map.js", "style.css"):
        assert client.get(f"/client/{name}").status_code == 200, name


def test_client_has_no_network_dependencies():
    for path in CLIENT_DIR.iterdir():
        text = path.read_text()
        assert "http://" not in text.replace("http://www.w3.org/2000/svg", "")
        assert "https://" not in text
        assert "cdn" not in text.lower()


def test_api_ship_and_state(client):
    ship = client.get("/api/ship").json()
    assert ship["spars"] and ship["sails"]
    state = client.get("/api/state").json()
    assert state["tick"] == 0
    assert state["driver"] == {
        "running": False,
        "compression": 1.0,
        "snapshot_every": 1,
        # the pace rule (package 41): the rule, the rate now and the samples open
        "pace": {"rule": "pace", "compression": 1.0, "rate": 1.0, "held": False, "open": []},
    }
    assert len(state["sails"]) == len(ship["sails"])


def test_post_order_and_driver(client):
    r = client.post("/api/order", json={"text": "set the topsails"})
    assert r.status_code == 200
    e = r.json()
    assert e["kind"] == "order.accepted"
    assert "stamp" in e
    r = client.post("/api/order", json={"text": "splice the mainbrace"})
    assert r.json()["kind"] == "order.rejected"
    assert client.post("/api/order", json={"text": ""}).status_code == 400

    r = client.post("/api/driver", json={"action": "tick", "value": 120})
    assert r.json()["running"] is False
    assert client.get("/api/state").json()["tick"] == 120
    r = client.post("/api/driver", json={"action": "time", "value": 60})
    assert r.json() == {
        "running": False,
        "compression": 60.0,
        "snapshot_every": 60,
        "pace": {"rule": "pace", "compression": 60.0, "rate": 60.0, "held": False, "open": []},
    }
    r = client.post("/api/driver", json={"action": "go"})
    assert r.json()["running"] is True
    r = client.post("/api/driver", json={"action": "hold"})
    assert r.json()["running"] is False
    assert client.post("/api/driver", json={"action": "dance"}).status_code == 400
    assert client.post("/api/driver", json={"action": "time", "value": "x"}).status_code == 400

    log = client.get("/api/log").json()
    assert any(e["kind"] == "order.accepted" and e["tick"] == 0 for e in log)
    later = client.get("/api/log", params={"since": 0}).json()
    assert later and all(e["tick"] > 0 for e in later)


def test_websocket_streams_events_and_snapshots(client):
    with client.websocket_connect("/ws") as ws:
        hello = ws.receive_json()
        assert hello["type"] == "hello"
        assert hello["ship"]["spars"]
        assert hello["snapshot"]["tick"] == 0
        assert hello["log"][0]["kind"] == "world.start"

        client.post("/api/order", json={"text": "set the jib"})
        kinds = []
        for _ in range(4):
            m = ws.receive_json()
            if m["type"] == "event":
                kinds.append(m["event"]["kind"])
            if m["type"] == "snapshot":
                break
        assert "order.accepted" in kinds

        client.post("/api/driver", json={"action": "tick", "value": 3})
        ticks = []
        while True:
            m = ws.receive_json()
            if m["type"] == "snapshot":
                ticks.append(m["snapshot"]["tick"])
                if m["snapshot"]["tick"] == 3 and not m["snapshot"]["driver"]["running"]:
                    break
        assert ticks[:3] == [1, 2, 3]  # every tick at 1x

        ws.send_json({"type": "order", "text": "set the fore topsail"})
        seen = False
        for _ in range(6):
            m = ws.receive_json()
            if m["type"] == "event" and "fore topsail" in m["event"]["text"]:
                seen = True
                break
        assert seen


# -- saving from the browser session ---------------------------------------------------


def test_save_from_the_order_box_and_the_driver(tmp_path):
    """`save PATH` typed in the order box writes the same file the console's `save`
    writes, says so in the log, and is not journaled (a replay must not re-save); the
    driver action and the download route give the same save."""
    world = world_for(SHIPS[0])
    driver = Driver(world)
    app = create_app(driver)
    with TestClient(app) as client:
        client.post("/api/order", json={"text": "set the jib"})
        client.post("/api/driver", json={"action": "tick", "value": 5})
        journal_before = list(world.journal)

        target = tmp_path / "voyage.json"
        r = client.post("/api/order", json={"text": f"save {target}"})
        assert r.status_code == 200
        assert r.json()["kind"] == "driver.saved"
        assert "tick 5" in r.json()["text"]
        assert target.exists()
        assert world.journal == journal_before

        saved = json.loads(target.read_text())
        assert saved["seed"] == world.seed
        assert saved["journal"][-1][2] == "set the jib"

        second = tmp_path / "again.json"
        r = client.post("/api/driver", json={"action": "save", "value": str(second)})
        assert r.status_code == 200
        assert json.loads(second.read_text())["journal"] == saved["journal"]

        r = client.get("/api/save")
        assert r.status_code == 200
        assert r.headers["content-disposition"].startswith("attachment;")
        assert r.json()["journal"] == saved["journal"]

        r = client.post("/api/order", json={"text": "save"})
        assert r.json()["kind"] == "driver.refused"
        r = client.post(
            "/api/order", json={"text": f"save {tmp_path / 'no' / 'such' / 'dir' / 'x.json'}"}
        )
        assert r.json()["kind"] == "driver.refused"


# -- package 29: --load and --scenario on the server (spec M4 §19, §21) -----------------


def server_args(**kw):
    import argparse

    base = {"ship": None, "seed": None, "wind": None, "heading": None, "load": None}
    base["scenario"] = None
    base.update(kw)
    return argparse.Namespace(**base)


def test_the_server_loads_a_save_and_goes_on(tmp_path):
    """`--load SAVE` on the server, as the console has had since M0 (the lead's promise at
    gate 4a): the save is replayed to its last tick, the digest is the saved game's, and
    the game goes on from there."""
    from freesail.core import replay
    from freesail.ui.server import build_world

    world = world_for(SHIPS[0])
    world.submit("set plain sail")
    world.run(120)
    world.submit("splice the mainbrace")  # refused, and replayed as refused (package 29)
    world.run(60)
    path = replay.save_to_file(world, tmp_path / "day.json")
    loaded = build_world(server_args(load=str(path)))
    assert loaded.clock.tick == 180
    assert loaded.log.digest() == world.log.digest()
    driver = Driver(loaded)
    with TestClient(create_app(driver)) as client:
        assert client.get("/api/state").json()["tick"] == 180
        client.post("/api/order", json={"text": "set the royals"})
        client.post("/api/driver", json={"action": "tick", "value": 30})
        assert client.get("/api/state").json()["tick"] == 210
    world.submit("set the royals")
    world.run(30)
    assert loaded.log.digest() == world.log.digest(), "the loaded game goes on as the original"


def test_the_server_starts_from_a_scenario_file():
    from freesail.ui.server import build_world

    world = build_world(server_args(scenario="data/scenarios/gate-4c-day.yaml"))
    assert world.seed == 7 and world.weather is not None
    assert world.scenario.name == "The gate's day"
    other = build_world(server_args(scenario="data/scenarios/gate-4c-day.yaml", seed=3))
    assert other.seed == 3


def test_a_save_on_the_server_replays_with_its_line(tmp_path):
    """The server's `save PATH` line is a driver's line (`World.record_driver`): a later
    save replays it where it was, and a refusal too, so the digests agree after a save."""
    from freesail.api.session import ship_factory
    from freesail.core import replay

    world = world_for(SHIPS[0])
    driver = Driver(world)
    e = driver.save(str(tmp_path / "one.json"))
    assert e.kind == "driver.saved" and "the log's digest is" in e.text
    world.run(30)
    assert driver.submit("state of the tide").kind == "order.rejected"
    world.run(30)
    copy = replay.replay(world.save(), ship_factory)
    assert copy.log.digest() == world.log.digest()


# -- package 33d: the browser's shelf ------------------------------------------------------


def test_the_completion_route_is_the_consoles_completer(client, world):
    """`/api/complete?line=` (package 33d; `docs/design/Presentation.md`): the console's
    completer behind the order line, the same words, less the console's own commands that
    the browser's order line does not take."""
    from freesail.orders.complete import suggestions
    from freesail.ui.server import CONSOLE_ONLY

    for line in ("set the f", "reef the fore topsail ", "brace ", "s", 'standing order "x": '):
        got = client.get("/api/complete", params={"line": line}).json()
        assert got["line"] == line
        want = [s for s in suggestions(world.ship, line, 30) if s not in CONSOLE_ONLY][:12]
        assert got["suggestions"] == want and want, line
    assert (
        "set the fore topsail"
        in client.get("/api/complete", params={"line": "set the fore t"}).json()["suggestions"]
    )
    for line in ("", "l", "st", "m", "h", "q", "re"):
        offered = client.get("/api/complete", params={"line": line}).json()["suggestions"]
        assert not set(offered) & set(CONSOLE_ONLY), line
    assert (
        len(client.get("/api/complete", params={"line": "", "limit": 3}).json()["suggestions"]) == 3
    )
    n = len(world.log)
    client.get("/api/complete", params={"line": "set "})
    assert len(world.log) == n, "a completion is a read, never a line in the log"


def test_the_library_routes_serve_every_topic_and_section_as_the_tool_does(client, world):
    """`/api/library` is the model's `library` tool's own page (the same text from the same
    Markdown), and `/api/library/topics` names every topic the contents names with every
    section it lists, each of which the tool serves by the words given (package 33d:
    nothing served the model cannot ask for, nothing it can ask for withheld)."""
    from freesail.agents import tools

    index = client.get("/api/library/topics").json()["topics"]
    keys = [t["key"] for t in index]
    assert keys[0] == "primer" and {"catalogue", "grammar", "the ship", "tools"} <= set(keys)
    assert "standing orders" in keys and any(k.startswith("primer 3") for k in keys)
    contents = client.get("/api/library").json()
    assert contents["text"] == str(tools.library(world, "captain", "contents"))
    assert contents["reopen"] == "library(topic='contents')"
    for top in index:
        page = client.get("/api/library", params={"topic": top["key"]}).json()
        assert page["text"] == str(tools.library(world, "watcher", top["key"])), top["key"]
        assert not page["text"].startswith("The library has no topic"), top["key"]
        for sec in top["sections"]:
            got = client.get(
                "/api/library", params={"topic": top["key"], "section": sec["ask"]}
            ).json()
            assert " has no section " not in got["text"], (top["key"], sec)
            assert " sections of " not in got["text"].split("\n")[0], (top["key"], sec)
            assert got["text"] == str(tools.library(world, "watcher", top["key"], sec["ask"]))
    # find, across the whole library and within a topic, as the tool's find=
    found = client.get("/api/library", params={"find": "goose-wing"}).json()
    assert found["text"] == str(tools.library(world, "captain", "contents", find="goose-wing"))
    assert "paragraph" in found["text"] and found["reopen"] == "library(find='goose-wing')"
    inner = client.get("/api/library", params={"topic": "primer 3", "find": "reef"}).json()
    assert inner["text"].startswith("'reef' in primer 3")
    none = client.get("/api/library", params={"find": "zzyzx"}).json()
    assert none["text"].startswith("Nothing in the library matches")
    refused = client.get("/api/library", params={"topic": "the stars"}).json()
    assert refused["text"].startswith("The library has no topic 'the stars'")


def test_the_ship_papers_are_the_librarys_papers_topic_and_nothing_waits(client, world):
    """`/api/library/papers` (package 35; spec M5 §22): the ship's papers are the library's
    `papers` topic, the same pages the model's `library(topic='papers')` serves, each by
    handle with its keeper, its place and its last entry, read without a line in the log;
    the stores' pages are the words their queries answer at the order line, from the
    same stores; and nothing waits any more (the two entries of package 33d are gone)."""
    from freesail.agents import tools
    from freesail.ship.parts import cordage, ground_tackle

    n = len(world.log)
    data = client.get("/api/library/papers").json()
    assert len(world.log) == n, "reading the papers writes nothing"
    by = {p["handle"]: p for p in data["papers"]}
    assert list(by) == [
        "the sailmaker's account",
        "the manifest",
        "the purser's books",
        "the boatswain's store book",
        "the booms' list",
        "the establishment of ground tackle",
        "the epitome's table of the establishments",
        "the price list",
    ]
    assert by["the booms' list"]["lines"] == queries.booms_lines(world)
    assert by["the sailmaker's account"]["lines"] == queries.sail_room_lines(world)
    assert by["the boatswain's store book"]["lines"] == cordage(world.ship).inventory_lines()
    assert by["the establishment of ground tackle"]["lines"] == ground_tackle(world.ship).describe()
    for handle, query in (
        ("the booms' list", "the booms"),
        ("the sailmaker's account", "the sail room"),
        ("the boatswain's store book", "the boatswain's store"),
        ("the establishment of ground tackle", "the ground tackle"),
    ):
        answered = world.submit(query)  # the same words at the order line
        assert answered.kind.startswith("query.")
        assert answered.text == "\n".join(by[handle]["lines"])
    assert "kept by the sailmaker in the sail room" in by["the sailmaker's account"]["words"]
    # the purser keeps the manifest in a ship of war; the mate in a merchantman
    keeper = "purser" if world.people.find("the purser") is not None else "mate"
    assert f"kept by the {keeper} in the hold" in by["the manifest"]["words"]
    assert by["the manifest"]["ask"] == "library(topic='papers', section='the manifest')"
    # the same page the model reads, by handle
    page = tools.library(world, "watcher", "papers", section="manifest")
    assert page.splitlines()[1:] == by["the manifest"]["lines"]
    assert data["waiting"] == []
    point = Driver(World(seed=1))
    with TestClient(create_app(point)) as c:
        bare = c.get("/api/library/papers").json()
        assert bare["papers"] == [] and bare["words"] and bare["waiting"] == []


def watched_driver(**kw) -> Driver:
    """The frigate with the scripted watcher (sampled every glass and on notable lines),
    the clock running at 60x."""
    from freesail.ui.console import station_watcher

    world = world_for(SHIPS[0])
    station_watcher(world, "fake")
    driver = Driver(world, compression=60, **kw)
    driver.running = True
    return driver


def test_ease_on_station_eases_the_clock_on_a_sample_and_says_so():
    """`--ease-on-station` (package 33d; playtest 12, the owner's note 3): the scripted
    watcher's sample at the glass eases the clock to 1x, as an urgent line would; the log
    says so in a driver's line, routine and kept, which a replay writes again so the
    digests agree. Off, nothing eases and no line is written."""
    from freesail.api.session import ship_factory
    from freesail.core import replay

    off = watched_driver()
    off._run_ticks(1900)
    assert off.compression == 60 and off.world.clock.tick == 1900
    assert not [e for e in off.world.log.all() if e.kind == "driver.eased"]

    on = watched_driver(ease_on_station=True)
    assert on.state()["ease_on_station"] is True
    on._run_ticks(1900)
    world = on.world
    assert world.clock.tick == 1800, "eased at the glass, the rest of the batch not run"
    assert on.compression == 1.0
    eased = [e for e in world.log.all() if e.kind == "driver.eased"]
    assert len(eased) == 1
    line = eased[0]
    assert line.text == "Compression eased to 1x: the watcher is sampled."
    assert line.actor == "driver" and line.severity.value == "routine" and line.tick == 1800
    assert line.data == {
        "from": 60.0,
        "to": 1.0,
        "tick": 1800,
        "station": "watcher",
        "why": "sampled",
    }
    assert on.state()["eased"]["why"] == "station"
    # the line is the driver's (World.record_driver): in the inputs, so a replay makes it
    assert any(i.get("line", {}).get("kind") == "driver.eased" for i in world.inputs)
    world.run(30)
    copy = replay.replay(world.save(), ship_factory)
    assert copy.log.digest() == world.log.digest()
    # at 1x it does not ease again, and the player's speed clears the notice
    on.set_compression(60)
    assert "eased" not in on.state()


def test_ease_on_station_when_a_station_speaks_and_the_option_by_the_driver(tmp_path):
    """A question put to the watcher is answered on the order; the answer eases the clock
    (its turn opening, `sampled`, comes first). The instruments' option is the driver's
    action `ease_on_station`, and the state says it only when it is on."""
    driver = watched_driver()
    with TestClient(create_app(driver)) as client:
        driver.running = True
        assert "ease_on_station" not in client.get("/api/state").json()["driver"]
        r = client.post("/api/driver", json={"action": "ease_on_station", "value": True})
        assert r.json()["ease_on_station"] is True
        driver.running = True
        client.post("/api/order", json={"text": "ask the watcher how the sails are drawing"})
        assert driver.compression == 1.0
        lines = [e for e in driver.world.log.all() if e.kind == "driver.eased"]
        assert len(lines) == 1 and lines[0].text.startswith("Compression eased to 1x: the watcher")
        r = client.post("/api/driver", json={"action": "ease_on_station", "value": "off"})
        assert "ease_on_station" not in r.json()
        client.post("/api/driver", json={"action": "time", "value": 60})
        driver.running = True
        client.post("/api/order", json={"text": "ask the watcher how the sails are drawing"})
        assert driver.compression == 60.0


def test_the_server_takes_the_ease_on_station_flag():
    """`--ease-on-station` on the command line reaches the driver (`main`)."""
    import inspect

    from freesail.ui import server

    src = inspect.getsource(server.main)
    assert '"--ease-on-station"' in src and "ease_on_station=args.ease_on_station" in src


def test_the_chart_block_is_unchanged_by_the_zoom():
    """Zoom and pan are the client's (package 33d): `/api/chart` is the chart block as
    package 32 made it, the same keys and the same coast."""
    from freesail.ui.server import build_world

    world = build_world(server_args(scenario="data/scenarios/gate-5b-passage.yaml"))
    with TestClient(create_app(Driver(world))) as client:
        chart = client.get("/api/chart").json()
    assert set(chart) == set(queries.chart_block(world))
    assert {"region", "title", "bounds", "coast", "features"} <= set(chart)
    assert chart["coast"] == json.loads(json.dumps(queries.chart_block(world)["coast"]))


def test_the_client_has_the_shelf(client):
    """The page carries the hint line, the library pane and its script, the option and the
    map's buttons; the pop-out window is served beside it."""
    page = client.get("/").text
    for needle in ('id="hint"', 'id="library-panel"', "library.js", 'id="opt-ease-on-station"'):
        assert needle in page, needle
    assert 'id="btn-map-centre"' in page and 'id="btn-map-fit"' in page
    pop = client.get("/client/library.html")
    assert pop.status_code == 200 and "library.js" in pop.text
    assert client.get("/client/library.js").status_code == 200


# -- package 37n: the player's pencil on the chart -------------------------------------------

LINE = {"kind": "line", "points": [{"lat": 49.95, "lon": -5.2}, {"lat": 50.0, "lon": -5.1}]}
RING = {"kind": "ring", "points": [{"lat": 49.97, "lon": -5.18}], "radius_m": 1852.0}
NOTE = {"kind": "note", "points": [{"lat": 49.96, "lon": -5.15}], "text": "  the Manacles?  "}


def test_the_marks_are_laid_listed_and_rubbed_out():
    """A line, a ring and a note go to the server, come back with their ids on the hello
    and on the socket, and are rubbed out one by one or all together; nothing of them is in
    the log, the journal, the inputs or the snapshot, and the game's digest does not move."""
    world = world_for(SHIPS[0])
    digest = world.log.digest()
    with TestClient(create_app(Driver(world))) as client:
        with client.websocket_connect("/ws") as ws:
            assert ws.receive_json()["marks"] == []
            first = client.post("/api/marks", json=LINE).json()
            assert first["id"] == "m1" and first["points"] == LINE["points"]
            pushed = ws.receive_json()
            while pushed["type"] != "marks":
                pushed = ws.receive_json()
            assert [m["id"] for m in pushed["marks"]] == ["m1"]
        assert client.post("/api/marks", json=RING).json()["radius_m"] == 1852.0
        assert client.post("/api/marks", json=NOTE).json()["text"] == "the Manacles?"
        marks = client.get("/api/marks").json()["marks"]
        assert [m["kind"] for m in marks] == ["line", "ring", "note"]
        assert [m["id"] for m in marks] == ["m1", "m2", "m3"]
        with client.websocket_connect("/ws") as ws:
            assert [m["id"] for m in ws.receive_json()["marks"]] == ["m1", "m2", "m3"]
        snap = client.get("/api/state").json()
        assert "chart_marks" not in snap and "Manacles" not in json.dumps(snap)
        assert client.delete("/api/marks/m2").json()["marks"][1]["id"] == "m3"
        assert client.delete("/api/marks/m2").status_code == 404
        assert client.post("/api/marks", json=RING).json()["id"] == "m4"  # never reused
        assert client.delete("/api/marks").json() == {"marks": []}
    assert world.log.digest() == digest
    assert not world.journal and not world.inputs
    assert all("Manacles" not in e.text for e in world.log.all())


@pytest.mark.parametrize(
    "bad",
    [
        {"kind": "arrow", "points": [{"x": 0, "y": 0}]},
        {"kind": "line", "points": [{"lat": 50, "lon": -5}]},
        {"kind": "line", "points": [{"lat": 50, "lon": -5}, {"x": 0, "y": 0}]},
        {"kind": "ring", "points": [{"x": 0, "y": 0}], "radius_m": -3},
        {"kind": "ring", "points": [{"x": 0, "y": 0}]},
        {"kind": "note", "points": [{"x": 0, "y": 0}], "text": "   "},
        {"kind": "note", "points": [{"x": "NaN", "y": 0}], "text": "here"},
        {"kind": "note", "points": [{"lat": 95, "lon": 0}], "text": "here"},
    ],
)
def test_a_mark_that_does_not_read_is_refused_in_words(client, bad):
    r = client.post("/api/marks", json=bad)
    assert r.status_code == 400 and r.json()["detail"]
    assert client.get("/api/marks").json() == {"marks": []}


@pytest.mark.parametrize("checkpoint", [True, False], ids=["checkpoint", "replay"])
def test_the_marks_are_saved_and_loaded_with_the_game(tmp_path, checkpoint):
    """The marks are in the save the server writes (and in the download), and come back
    when the server takes the save up, whether from its checkpoint or by a replay; the
    replay itself makes none, and the loaded game's digest is the saved game's."""
    from freesail.api.session import ship_factory
    from freesail.core import replay
    from freesail.ui.server import build_world

    world = world_for(SHIPS[0])
    with TestClient(create_app(Driver(world))) as client:
        for mark in (LINE, RING, NOTE):
            client.post("/api/marks", json=mark)
        client.post("/api/driver", json={"action": "tick", "value": 30})
        assert len(client.get("/api/save").json()["chart_marks"]) == 3
    path = replay.save_to_file(world, tmp_path / "pencil.json", checkpoint=checkpoint)
    saved = json.loads(path.read_text())
    assert [m["id"] for m in saved["chart_marks"]] == ["m1", "m2", "m3"]
    assert not replay.replay(saved, ship_factory).chart_marks  # a replay makes none of them
    loaded = build_world(server_args(load=str(path)))
    assert loaded.loaded_from == ("checkpoint" if checkpoint else "replay")
    assert loaded.chart_marks == saved["chart_marks"]
    assert loaded.log.digest() == world.log.digest()
    with TestClient(create_app(Driver(loaded))) as client:
        assert client.post("/api/marks", json=LINE).json()["id"] == "m4"


def test_the_client_has_the_charts_tools(client):
    """The map's buttons, the list of marks and its inputs are on the page; the chart's
    script carries the rose, the pencil and the bearings' clean-up."""
    page = client.get("/").text
    for needle in (
        'id="btn-map-rose"',
        'data-tool="line"',
        'data-tool="ring"',
        'data-tool="note"',
        'id="marks-pane"',
        'id="mark-note-text"',
        'id="mark-ring-nm"',
    ):
        assert needle in page, needle
    script = client.get("/client/map.js").text
    for needle in ("drawRose", "drawMarks", "bearingsShown", "BEARING_FULL_S", "BEARING_DROP_S"):
        assert needle in script, needle
