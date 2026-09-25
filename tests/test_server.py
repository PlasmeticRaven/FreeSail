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
    assert state["driver"] == {"running": False, "compression": 1.0, "snapshot_every": 1}
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
    assert r.json() == {"running": False, "compression": 60.0, "snapshot_every": 60}
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
