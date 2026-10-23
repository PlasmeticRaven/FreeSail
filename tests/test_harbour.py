"""The harbour (package 59; spec M7b §21d, §21e; `freesail/ui/harbour.py`,
`client/harbour.html` and `harbour.js`): the launcher as a page of the game's own server.

On FastAPI's `TestClient`: the game page leads to the harbour while no game is in play; the
catalogue; a game started from the page's choices by the server's own `prepare_game` and
taken up in place (one server, the harbour still at its path); the scenario maker's
read, proof (the loader's refusal in the form's words) and save in the player's place; the
desktop client's entries shown first and written on the word; the settings kept without a
key. On a live server: the API door and the local runner started as the server's
subprocesses, one seated and stopped (its station released), one that dies and says so.
In the browser the tests drive (the pre-installed Chromium through Playwright): a game
started with a seat and a director's brief, and the owner's four scenarios read into the
maker's form and written again byte for byte.

The model names are made up; the settings, the records, the saves and the client's file
go to a temporary directory.
"""

from __future__ import annotations

import json
import os
import socket
import sys
import threading
import time
from pathlib import Path
from typing import Any

import pytest

pytest.importorskip("fastapi")
pytest.importorskip("httpx")

from fastapi.testclient import TestClient  # noqa: E402

from freesail import settings as S  # noqa: E402
from freesail.core.world import Scenario, World  # noqa: E402
from freesail.ui.harbour import Harbour  # noqa: E402
from freesail.ui.server import Driver, create_app  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ROOT / "data" / "scenarios"
THE_FOUR = ("smack-falmouth", "lugger-roscoff", "directed-passage", "dispatches-falmouth")
PLACEHOLDER = "placeholder-model-for-the-harbour"  # no model is named here


class Port:
    """A harbour on a world with no game yet, as `py -m freesail` starts one."""

    def __init__(self, tmp: Path, settings: dict[str, Any] | None = None):
        self.tmp = tmp
        self.settings_path = tmp / "player" / "settings.yaml"
        s = S.load_settings(self.settings_path)
        s["places"]["desktop_config"] = str(tmp / "Claude" / "claude_desktop_config.json")
        for k, v in (settings or {}).items():
            s[k] = S._merge(s[k], v)
        S.save_settings(s, self.settings_path)
        self.driver = Driver(World(seed=1805, scenario=Scenario()))
        self.records = tmp / "consent"
        self.harbour = Harbour(
            self.driver,
            settings_path=self.settings_path,
            consent_records=self.records,
            saves_dir=tmp / "saves",
            started=False,
        )
        self.app = create_app(
            self.driver,
            harbour=self.harbour,
            consent_records=self.records,
            saves_dir=tmp / "saves",
        )

    @property
    def place(self) -> Path:
        return self.settings_path.parent / "scenarios"


@pytest.fixture
def port(tmp_path):
    return Port(tmp_path)


@pytest.fixture
def client(port):
    with TestClient(port.app) as c:
        yield c


# ---------------------------------------------------------------------------
# The page, the catalogue and a game started
# ---------------------------------------------------------------------------


def test_with_no_game_the_game_page_leads_to_the_harbour(client):
    r = client.get("/", follow_redirects=False)
    assert r.status_code == 307 and r.headers["location"] == "/harbour"
    page = client.get("/harbour")
    assert page.status_code == 200 and "scenario maker" in page.text
    assert "/client/harbour.js" in page.text
    state = client.get("/api/harbour/state").json()
    assert state["game"]["started"] is False and state["doors"] == []


def test_the_catalogue_lists_the_scenarios_ships_seats_stations_briefs_and_ports(client):
    cat = client.get("/api/harbour/catalogue").json()
    paths = {s["path"] for s in cat["scenarios"]}
    assert {f"data/scenarios/{n}.yaml" for n in THE_FOUR} <= paths
    assert "data/ships/smack.yaml" in cat["ships"] and "director" in cat["seats"]
    assert {"captain", "officer", "director"} <= set(cat["stations"])
    assert {"quiet-passage", "dispatches"} <= set(cat["briefs"])
    falmouth = next(p for p in cat["ports"] if p["id"] == "falmouth")
    assert falmouth["road"] == "Carrick Road" and falmouth["region"] == "channel-west"
    assert "data/standing_orders/starter.orders" in cat["books"]


def test_a_game_started_with_a_seat_and_a_brief_is_the_servers_game_taken_up_in_place(port, client):
    """Truth 7b-108's middle (the whole in test_known_truths): one server, its World
    replaced, the pages told, the clock held, the seat and the director's brief given by
    the server's own start."""
    old = port.driver.world
    told: list[dict[str, Any]] = []
    port.driver.add_listener(told.append)
    refused = client.post("/api/harbour/start", json={})
    assert refused.status_code == 400 and "Choose a scenario" in refused.json()["detail"]
    bad = client.post(
        "/api/harbour/start",
        json={"scenario": "data/scenarios/lesson-falmouth.yaml", "seat": "bosun's cat"},
    )
    assert bad.status_code == 400 and "not seated" in bad.json()["detail"]
    r = client.post(
        "/api/harbour/start",
        json={
            "scenario": "data/scenarios/dispatches-falmouth.yaml",
            "seat": "officer",
            "director_brief": "quiet-passage",
            "pace": "lockstep",
            "time": 10,
        },
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["lines"][0].startswith("Scenario: The dispatches")
    game = body["game"]
    assert game["started"] and game["running"] is False  # held until the driver says go
    assert game["seat"] == "the player at the officer of the watch's station"
    assert game["director"] == "A quiet passage" and game["compression"] == 10
    assert port.driver.world is not old and port.driver.lockstep
    assert {"type": "restart"} in told
    held = client.get("/api/harbour/state").json()["stations"]
    assert [s["holder"] for s in held] == ["the player"]
    assert client.get("/", follow_redirects=False).status_code == 200
    assert client.get("/harbour").status_code == 200  # still there while the game runs
    # the game page's own routes read the new game
    assert client.get("/api/state").json()["driver"]["running"] is False
    assert client.get("/api/ship").json()["name"] == "Sherbourne"


# ---------------------------------------------------------------------------
# The scenario maker
# ---------------------------------------------------------------------------


def test_the_maker_reads_proves_and_saves_in_the_players_place(port, client):
    r = client.get("/api/harbour/scenario", params={"path": "data/scenarios/smack-falmouth.yaml"})
    assert r.status_code == 200
    got = r.json()
    assert got["fields"]["ship"]["file"] == "data/ships/smack.yaml"
    assert got["position_deg"] == [50.1631, -5.0345]
    proved = client.post(
        "/api/harbour/scenario/prove", json={"fields": got["fields"], "source": got["path"]}
    ).json()
    assert proved["lines"][0] == "Scenario: A smack out of Falmouth (this scenario)."
    # a refusal in the form's words: the loader's, with no temporary file named
    bad = dict(got["fields"], ship=dict(got["fields"]["ship"], file="data/ships/nope.yaml"))
    r = client.post("/api/harbour/scenario/prove", json={"fields": bad})
    assert r.status_code == 400 and r.json()["detail"] == "data/ships/nope.yaml: no such ship file."
    r = client.post(
        "/api/harbour/scenario/prove",
        json={"fields": dict(got["fields"], stations={"officer": "somebody"})},
    )
    assert r.status_code == 400 and r.json()["detail"].startswith("stations officer:")
    r = client.post(
        "/api/harbour/scenario/prove",
        json={"fields": dict(got["fields"], orders=["splice the main brace sideways"])},
    )
    assert r.status_code == 400 and "refused" in r.json()["detail"]
    # saved: the same bytes, with nothing changed
    saved = client.post(
        "/api/harbour/scenario",
        json={"fields": got["fields"], "source": got["path"], "name": "smack"},
    ).json()
    assert Path(saved["path"]) == port.place / "smack.yaml"
    assert (port.place / "smack.yaml").read_bytes() == (
        SCENARIOS / "smack-falmouth.yaml"
    ).read_bytes()
    again = client.post("/api/harbour/scenario", json={"fields": got["fields"], "name": "smack"})
    assert again.status_code == 409 and "there already" in again.json()["detail"]
    # listed by the harbour as the player's own, and read back from there
    cat = client.get("/api/harbour/catalogue").json()
    own = [s for s in cat["scenarios"] if s["own"]]
    assert [s["name"] for s in own] == ["A smack out of Falmouth"]
    assert client.get("/api/harbour/scenario", params={"path": own[0]["path"]}).status_code == 200
    # a drafted book goes beside it and is named in its standing orders
    fields = dict(got["fields"], name="A smack with a book of her own")
    made = client.post(
        "/api/harbour/scenario",
        json={
            "fields": fields,
            "name": "booked",
            "book": 'standing order "watch": at sunset then take in the topsail',
        },
    ).json()
    assert Path(made["book"]).read_text(encoding="utf-8").startswith("standing order")
    assert made["book"] in made["text"]


def test_the_maker_reads_only_the_games_scenarios_and_the_players_own(client):
    r = client.get("/api/harbour/scenario", params={"path": "data/ships/smack.yaml"})
    assert r.status_code == 403
    r = client.get("/api/harbour/scenario", params={"path": "/etc/hostname.yaml"})
    assert r.status_code == 403


def test_a_new_scenario_from_the_form_loads_at_the_console_and_reads_back_unchanged(port, client):
    from freesail.ui.console import start_world, station_watcher  # noqa: F401
    from freesail.ui.server import server_parser
    from freesail.world.scenarios import load_scenario

    fields = {
        "name": "A cutter to Plymouth",
        "seed": 7,
        "start": "1805-06-12T05:00",
        "position": {"lat_deg": 50.1631, "lon_deg": -5.0345},
        "region": "channel-west",
        "nation": "britain",
        "ship": {"file": "data/ships/cutter.yaml", "heading_deg": 190, "glass": True},
        "weather": {"wind": [{"at": "1805-06-12T05:00", "from_deg": 225, "knots": 15}]},
        "ships": [
            {
                "id": "lark",
                "description": "cutter",
                "name": "Lark",
                "nation": "britain",
                "position": "49 55 N 5 45 W",
                "goal": "patrolling off the Wolf within 4 miles",
            }
        ],
        "business": False,
        "orders": ["let go the best bower"],
        "stations": {"officer": "player", "director": "model"},
        "director": {"brief": "dispatches"},
    }
    saved = client.post("/api/harbour/scenario", json={"fields": fields, "name": "plymouth"})
    assert saved.status_code == 200, saved.text
    path = Path(saved.json()["path"])
    text = path.read_text(encoding="utf-8")
    assert "business: off" in text and "# The other sail on the sea" in text
    # at the console as a hand-made one: the seat the file's
    args = server_parser().parse_args(["--scenario", str(path)])
    world, sf = start_world(args)
    assert sf.player_seat == "officer" and load_scenario(path).scenario.business == "off"
    # read back into the form and written again unchanged
    got = client.get("/api/harbour/scenario", params={"path": str(path)}).json()
    assert got["fields"]["stations"] == fields["stations"]
    client.post(
        "/api/harbour/scenario",
        json={"fields": got["fields"], "source": str(path), "name": "plymouth"},
    )
    assert path.read_text(encoding="utf-8") == text


def test_the_chart_for_pricking_a_start(client):
    c = client.get("/api/harbour/chart", params={"region": "channel-west"}).json()
    assert c["bounds"] == {"south": 48.0, "north": 51.0, "west": -7.0, "east": -3.0}
    assert len(c["coast"]) > 10 and any(p["id"] == "falmouth" for p in c["ports"])
    assert client.get("/api/harbour/chart", params={"region": "atlantis"}).status_code == 404


# ---------------------------------------------------------------------------
# The settings and the desktop client
# ---------------------------------------------------------------------------


def test_the_settings_are_kept_from_the_form_and_a_key_is_refused(port, client):
    got = client.get("/api/harbour/settings").json()
    assert got["path"] == str(port.settings_path) and got["error"] == ""
    s = got["settings"]
    s["doors"]["api"]["model"] = PLACEHOLDER
    r = client.post("/api/harbour/settings", json={"settings": s})
    assert r.status_code == 200 and r.json()["settings"]["doors"]["api"]["model"] == PLACEHOLDER
    s["doors"]["api"]["api_key"] = "x"
    r = client.post("/api/harbour/settings", json={"settings": s})
    assert r.status_code == 400 and "no key" in r.json()["detail"]
    assert "api_key" not in port.settings_path.read_text(encoding="utf-8")


def test_the_desktop_entries_are_shown_first_and_written_on_the_word(port, client):
    path = port.tmp / "Claude" / "claude_desktop_config.json"
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps({"mcpServers": {"another": {"command": "x"}}}), encoding="utf-8")
    shown = client.post("/api/harbour/desktop", json={"stations": ["captain", "director"]}).json()
    assert sorted(shown["entries"]) == ["freesail-captain", "freesail-director"]
    assert shown["written"] is False and shown["named"] is False
    assert json.loads(path.read_text(encoding="utf-8")) == {
        "mcpServers": {"another": {"command": "x"}}
    }
    assert '"another"' in shown["text"] and S.MODEL_NAME_PLACEHOLDER in shown["text"]
    written = client.post(
        "/api/harbour/desktop", json={"stations": ["captain", "director"], "write": True}
    ).json()
    assert written["written"] and Path(written["backup"]).exists()
    doc = json.loads(path.read_text(encoding="utf-8"))
    assert sorted(doc["mcpServers"]) == ["another", "freesail-captain", "freesail-director"]
    args = doc["mcpServers"]["freesail-director"]["args"]
    assert args[args.index("--station") + 1] == "director"
    state = client.get("/api/harbour/state").json()
    assert state["desktop"]["entries"] == ["freesail-captain", "freesail-director"]
    none = client.post("/api/harbour/desktop", json={"stations": []})
    assert none.status_code == 400


def test_the_shortcut_is_shown_before_it_is_written(client):
    r = client.post("/api/harbour/shortcut", json={}).json()
    assert r["written"] is False and "freesail" in r["text"]


# ---------------------------------------------------------------------------
# The doors as the server's subprocesses, on a live server
# ---------------------------------------------------------------------------


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])


class Live:
    """The harbour's server on a port of this process, as `py -m freesail` serves it."""

    def __init__(self, port: Port):
        import uvicorn

        self.port = port
        self.number = _free_port()
        self.url = f"http://127.0.0.1:{self.number}"
        port.harbour.game_url = self.url
        self.server = uvicorn.Server(
            uvicorn.Config(port.app, host="127.0.0.1", port=self.number, log_level="warning")
        )
        self.thread = threading.Thread(target=self.server.run, daemon=True)
        self.thread.start()
        deadline = time.monotonic() + 20
        while not self.server.started:
            assert time.monotonic() < deadline and self.thread.is_alive()
            time.sleep(0.05)

    def close(self) -> None:
        self.server.should_exit = True
        self.thread.join(timeout=15)


def _until(test: Any, seconds: float = 60.0) -> Any:
    end = time.monotonic() + seconds
    while time.monotonic() < end:
        got = test()
        if got:
            return got
        time.sleep(0.2)
    raise AssertionError("not there in time")


def test_a_door_that_dies_is_said_so_in_its_pane(tmp_path):
    port = Port(tmp_path, {"doors": {"local": {"endpoint": "http://127.0.0.1:9"}}})
    live = Live(port)
    try:
        import httpx

        with httpx.Client(base_url=live.url, timeout=60) as c:
            refused = c.post("/api/harbour/doors", json={"door": "local", "station": "watcher"})
            assert refused.status_code == 400 and "Start a game first" in refused.json()["detail"]
            c.post("/api/harbour/start", json={"scenario": "data/scenarios/lesson-falmouth.yaml"})
            d = c.post("/api/harbour/doors", json={"door": "local", "station": "watcher"}).json()
            assert d["state"] == "running" and d["words"].startswith(
                "The local runner at the watcher"
            )
            out = _until(
                lambda: (
                    (r := c.get(f"/api/harbour/doors/{d['id']}").json())["state"] == "ended" and r
                )
            )
            assert out["code"] == 2  # the local runner's EXIT_UNREACHABLE
            assert out["output"][-1].startswith(
                "== The local runner at the watcher has ended (exit code 2): it could not reach"
            )
            api = c.post("/api/harbour/doors", json={"door": "api", "station": "captain"})
            assert api.status_code == 400 and "Name the API door's model" in api.json()["detail"]
    finally:
        live.close()


def test_the_api_door_started_from_the_harbour_seats_its_station_and_is_stopped(
    tmp_path, monkeypatch
):
    """The API door as the server's subprocess, with its model and flags from the settings
    and its key from the environment it inherits (never the settings): seated at the
    watcher's station through the game's own consent records, shown held by its model in
    the harbour's state, stopped from the harbour with its station released."""
    pytest.importorskip("anthropic")
    from messages_api import MODEL, MessagesServer

    from freesail.agents import consent

    key = "a-test-key-of-no-account-0123456789"
    with MessagesServer(key) as api:
        port = Port(
            tmp_path,
            {"doors": {"api": {"model": MODEL, "flags": ["--base-url", api.url]}}},
        )
        consent.Record(MODEL, "a test runtime", "2026-10-18", consent.YES, answer="Yes.").write(
            port.records
        )
        monkeypatch.setenv("FREESAIL_API_KEY", key)
        monkeypatch.setenv("PYTHON_KEYRING_BACKEND", "keyring.backends.null.Keyring")
        live = Live(port)
        try:
            import httpx

            with httpx.Client(base_url=live.url, timeout=60) as c:
                c.post(
                    "/api/harbour/start", json={"scenario": "data/scenarios/lesson-falmouth.yaml"}
                )
                d = c.post("/api/harbour/doors", json={"door": "api", "station": "watcher"}).json()

                def held() -> Any:
                    st = c.get("/api/harbour/state").json()["stations"]
                    return [s for s in st if s["station"] == "watcher" and s["holder"] == MODEL]

                try:
                    seated = _until(held, 90)
                except AssertionError:
                    out = c.get(f"/api/harbour/doors/{d['id']}").json()["output"]
                    raise AssertionError("\n".join(out)) from None
                assert seated[0]["door"] == "api"
                pane = c.get(f"/api/harbour/doors/{d['id']}").json()
                assert any(
                    "credential store" not in ln and "environment" in ln for ln in pane["output"]
                )
                assert not any(key in ln for ln in pane["output"])
                stopped = c.post(f"/api/harbour/doors/{d['id']}/stop").json()
                assert stopped["state"] == "stopped"
                with port.driver.lock:
                    assert port.driver.world.agents["watcher"].agent.released
                out = c.get(f"/api/harbour/doors/{d['id']}").json()["output"]
                assert out[-1].endswith("stopped from the harbour. ==")
        finally:
            live.close()


# ---------------------------------------------------------------------------
# The page in the browser
# ---------------------------------------------------------------------------


def chromium_path() -> str | None:
    named = os.environ.get("FREESAIL_CHROMIUM")
    if named and Path(named).exists():
        return named
    folder = os.environ.get("PLAYWRIGHT_BROWSERS_PATH")
    if folder and (Path(folder) / "chromium").exists():
        return str(Path(folder) / "chromium")
    return None


@pytest.fixture
def browser_page(tmp_path):
    sync_api = pytest.importorskip("playwright.sync_api", reason="Playwright is not installed")
    port = Port(tmp_path)
    live = Live(port)
    try:
        pw = sync_api.sync_playwright().start()
    except Exception as e:  # noqa: BLE001
        live.close()
        pytest.skip(f"Playwright could not start: {e}")
    try:
        browser = pw.chromium.launch(headless=True, executable_path=chromium_path())
    except Exception as e:  # noqa: BLE001
        pw.stop()
        live.close()
        pytest.skip(f"no browser for Playwright here: {e}")
    errors: list[str] = []
    try:
        pg = browser.new_page(viewport={"width": 1280, "height": 1000})
        pg.on("pageerror", lambda e: errors.append(str(e)))
        yield pg, live, port, errors
    finally:
        browser.close()
        pw.stop()
        live.close()


def test_in_the_browser_a_game_is_started_and_the_four_scenarios_round_trip(browser_page):
    pg, live, port, errors = browser_page
    pg.goto(live.url + "/")
    assert pg.url.endswith("/harbour")
    pg.wait_for_function("window.freesailHarbour && window.freesailHarbour.ready", timeout=60_000)
    assert pg.inner_text("#status") == "no game yet"
    # a game with a seat and a director's brief
    pg.select_option("#s-scenario", "data/scenarios/directed-passage.yaml")
    pg.select_option("#s-seat", "officer")
    pg.select_option("#s-brief", "dispatches")
    pg.click("#btn-start")
    pg.wait_for_selector("#btn-to-game:not([hidden])", timeout=60_000)
    pg.wait_for_function(
        "document.getElementById('g-director').textContent === 'The dispatches'", timeout=10_000
    )
    pg.wait_for_function(
        "document.getElementById('g-stations').textContent.indexOf('officer of the watch') >= 0",
        timeout=10_000,
    )
    assert pg.inner_text("#status") == "a game in play"
    # the maker: each of the owner's scenarios read into the form and saved, byte for byte
    pg.click("nav.tabs button[data-tab=maker]")
    for stem in THE_FOUR:
        pg.select_option("#m-pick", f"data/scenarios/{stem}.yaml")
        pg.click("#btn-m-read")
        pg.wait_for_function(
            f"document.getElementById('m-source').textContent.indexOf('{stem}') >= 0"
        )
        pg.click("#btn-m-save")
        pg.wait_for_function("window.freesailHarbour.busy === true", timeout=10_000)
        pg.wait_for_function("window.freesailHarbour.busy === false", timeout=60_000)
        assert not pg.is_visible("#m-refusal"), pg.inner_text("#m-refusal")
        saved = port.place / f"{stem}.yaml"
        assert saved.read_bytes() == (SCENARIOS / f"{stem}.yaml").read_bytes(), stem
    # one field changed in the form: that field alone written again
    pg.fill('#maker [data-field="seed"]', "11")
    pg.fill("#m-name", "dispatches-11")
    pg.click("#btn-m-save")
    pg.wait_for_function("window.freesailHarbour.busy === true", timeout=10_000)
    pg.wait_for_function("window.freesailHarbour.busy === false", timeout=60_000)
    old = (SCENARIOS / "dispatches-falmouth.yaml").read_text(encoding="utf-8")
    new = (port.place / "dispatches-11.yaml").read_text(encoding="utf-8")
    assert new == old.replace("\nseed: 7\n", "\nseed: 11\n")
    # the game's page reads the game started
    pg.goto(live.url + "/")
    pg.wait_for_function(
        "document.getElementById('status').textContent === 'connected'", timeout=30_000
    )
    assert "schooner" in pg.inner_text("#ship-name")
    assert errors == []


# ---------------------------------------------------------------------------
# Package 67: the director's seats' doors
# ---------------------------------------------------------------------------


def test_the_settings_say_the_models_they_can_call_and_the_seated_doors_fold():
    s = S.check_settings(
        {
            "doors": {
                "api": {
                    "model": PLACEHOLDER,
                    "models": [
                        "placeholder-two",
                        {"name": "placeholder-three", "dialect": "openrouter"},
                    ],
                    "seat_budget_tokens": "2/5",
                }
            }
        }
    )
    assert S.callable_models(s) == {
        PLACEHOLDER: "anthropic",
        "placeholder-two": "anthropic",
        "placeholder-three": "openrouter",
    }
    assert S.seat_budget_tokens("2/5", 200_000) == 80_000
    assert S.seat_budget_tokens("40%", 200_000) == 80_000
    assert S.seat_budget_tokens("0.4", 200_000) == 80_000
    assert S.seat_budget_tokens("60000", 200_000) == 60_000
    assert S.seat_budget_tokens("", 200_000) is None
    with pytest.raises(ValueError):
        S.seat_budget_tokens("most of it", 200_000)
    with pytest.raises(S.SettingsError):
        S.check_settings({"doors": {"api": {"models": [{"name": "x", "dialect": "a fax"}]}}})
    with pytest.raises(S.SettingsError):
        S.check_settings({"doors": {"api": {"seat_budget_tokens": "lots"}}})


def test_the_harbour_starts_a_seats_door_as_the_directors_and_stops_it_when_the_seat_goes(
    tmp_path, monkeypatch
):
    """Package 67, item 2 (without a subprocess: the door's start recorded): a seat held on
    the World in play has the API door started for it, its model the seat's, its dialect
    the settings', `--budget-tokens` the settings' figure, marked the director's and told
    to the director; a seat for a model the settings cannot call is refused at the
    director's door and at the owner's `world:`, the settings' model named to the director
    alone; a seat gone has its door stopped."""
    from freesail.agents import consent
    from freesail.agents import director as D
    from freesail.world.orders import director_seats

    port = Port(
        tmp_path,
        {
            "doors": {
                "api": {
                    "model": PLACEHOLDER,
                    "models": [{"name": "placeholder-two", "dialect": "openrouter"}],
                    "seat_budget_tokens": "0.25",
                }
            }
        },
    )
    started: list[dict[str, Any]] = []
    stopped: list[str] = []

    class FakeDoor:
        def __init__(self, ident: str, argv: list[str]):
            self.id, self.argv, self.running = ident, argv, True
            self.station, self.ship = "officer of the watch", ""

        def stop(self) -> None:
            stopped.append(self.id)
            self.running = False

    def start_door(kind, station, ship="", *, seat="", seat_model="", by=""):
        argv = port.harbour.door_argv(kind, station, ship, seat_model=seat_model)
        ident = f"d{len(started) + 1}"
        started.append({"station": station, "ship": ship, "seat": seat, "by": by, "argv": argv})
        port.harbour.doors[ident] = FakeDoor(ident, argv)
        return {"id": ident}

    monkeypatch.setattr(port.harbour, "start_door", start_door)
    monkeypatch.setattr(port.harbour, "_stop_seat_door", lambda door: door.stop())
    with TestClient(port.app) as c:
        c.post("/api/harbour/start", json={"scenario": "data/scenarios/lesson-falmouth.yaml"})
        w = port.driver.world
        for name in (PLACEHOLDER, "placeholder-two", "placeholder-four"):
            consent.Record(
                name, "a test runtime", "2026-10-23", consent.YES, answer="Yes.", drill="passed"
            ).write(port.records)
        w.consent_records_dir = port.records
        w.scenario.director = {
            "models": [PLACEHOLDER, "placeholder-two", "placeholder-four"],
            "seats": 3,
            "seats_in_voyage": 5,
        }
        D.set_brief(w, "quiet-passage", source="the test")
        refused = D.direct(w, "seat: placeholder-four as officer for 4 samples", by="the test")
        assert refused == (
            "Refused: the settings call no model by that name; the API door's model is "
            f"{PLACEHOLDER}."
        )
        r = c.post(
            "/api/order", json={"text": "world: seat: placeholder-four as master for 4 samples"}
        )
        assert "The seat was not held: the settings call no model by that name" in r.text
        assert director_seats(w) == {}
        said = D.direct(w, "seat: placeholder-two as officer for 4 samples", by="the test")
        assert said.startswith("Done:"), said
        port.harbour.tend_seats()
        port.harbour.tend_seats()  # once a seat, however often it is tended
        assert len(started) == 1
        door = started[0]
        assert door["by"] == "the director" and door["seat"] == "own/officer of the watch"
        argv = door["argv"]
        assert argv[argv.index("--model") + 1] == "placeholder-two"
        assert argv[argv.index("--dialect") + 1] == "openrouter"
        assert argv[argv.index("--station") + 1] == "officer of the watch"
        assert argv[argv.index("--budget-tokens") + 1] == "0.25"
        assert "--ship" not in argv
        assert D.direct(w, "unseat: officer, the passage is quiet", by="the test").startswith(
            "Done"
        )
        port.harbour.tend_seats()
        assert stopped == ["d1"]
        # a door of the owner's own, from the page, carries no seat's flags and no mark
        assert "--budget-tokens" not in port.harbour.door_argv("api", "watcher")


def test_the_doors_of_the_directors_seats_are_marked_in_the_pane(tmp_path):
    from freesail.ui.harbour import Door

    door = Door(
        "d9",
        "api",
        "officer of the watch",
        [sys.executable, "-c", "print('a door')"],
        by="the director",
        seat="own/officer of the watch",
    )
    door.proc.wait(timeout=30)
    door._reader.join(timeout=30)
    state = door.state()
    assert state["by"] == "the director"
    assert state["words"].startswith("The director's seat's API door at the officer of the watch")
    assert Door("d10", "api", "watcher", [sys.executable, "-c", "pass"]).state()["by"] == ""
