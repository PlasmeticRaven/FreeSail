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

from own_page import PageClient  # noqa: E402

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
    with PageClient(port.app) as c:
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


def test_the_scenarios_stand_on_their_shelves_and_the_boats_are_no_ship_to_start_in(port, client):
    """Package 96b, step 1 (docs/design/Design-Harbour.md §3.2): the catalogue gives each
    scenario its shelf and its sentence in the shelves' order, the player's own first; the
    gates' and the tests' scenarios on a shelf marked hidden; a scenario of the game that
    the shelves' file does not name on the last shelf, shown; the ship's boats out of the
    ships offered for a bare start."""
    port.place.mkdir(parents=True, exist_ok=True)
    (port.place / "mine.yaml").write_text("name: A passage of mine\n", encoding="utf-8")
    cat = client.get("/api/harbour/catalogue").json()
    by_id = {s["id"]: s for s in cat["shelves"]}
    assert [s["id"] for s in cat["shelves"]][:3] == ["yours", "first", "lessons"]
    assert by_id["tests"]["hidden"] is True
    assert not any(s["hidden"] for s in cat["shelves"] if s["id"] != "tests")
    assert "unsorted" not in by_id  # every scenario of the game is named on a shelf
    entries = {Path(s["path"]).stem: s for s in cat["scenarios"]}
    assert entries["mine"]["shelf"] == "yours" and entries["mine"]["own"] is True
    assert cat["scenarios"][0]["path"].endswith("mine.yaml")
    assert entries["gate-4c-day"]["shelf"] == "tests"
    assert entries["squadron"]["shelf"] == "tests" and entries["tender"]["shelf"] == "tests"
    assert entries["first-action"]["shelf"] == "actions" and entries["first-action"]["says"]
    lessons = [Path(s["path"]).stem for s in cat["scenarios"] if s["shelf"] == "lessons"]
    assert lessons == ["lesson-landfall", "lesson-reckoning", "lesson-falmouth", "lesson-lee-shore"]
    assert [s["order"] for s in cat["scenarios"]] == list(range(len(cat["scenarios"])))
    # the boats are carried by the ships, and are not ships to start in
    assert "data/ships/frigate-36.yaml" in cat["ships"]
    assert not [s for s in cat["ships"] if "boat-" in s]
    # a scenario the file does not name is never hidden: the last shelf, shown
    shelved = port.harbour._shelve(
        [
            {"path": "data/scenarios/a-new-one.yaml", "name": "A new one", "own": False},
            {"path": "data/scenarios/gate-4c-day.yaml", "name": "The gate's day", "own": False},
        ]
    )
    assert [s["id"] for s in shelved] == ["tests", "unsorted"]
    assert shelved[-1]["hidden"] is False


def test_the_first_game_is_the_primers_chapter_7_and_its_log_is_the_bare_ships(client):
    """Package 96b, step 2 (docs/design/Design-Harbour.md §3.3): the first panel's game is
    the scenario "A first passage", the primer's chapter 7 made startable from the page.
    The chapter's own command is a bare frigate with `--seed 7 --wind 0,15 --heading 293`;
    the scenario gives the same log line for line through the chapter's first block (plain
    sail, braced sharp up, eight minutes), but for the opening line, which carries the
    scenario's name where the bare ship's says "Open water"."""
    from freesail.api.session import make_world
    from freesail.world.scenarios import begin, load_scenario, make_scenario_world

    cat = client.get("/api/harbour/catalogue").json()
    first = cat["first_game"]
    assert first["path"] == "data/scenarios/first-passage.yaml"
    assert first["name"] == "A first passage" and len(first["says"]) == 3
    entry = next(s for s in cat["scenarios"] if s["path"] == first["path"])
    assert entry["shelf"] == "first" and cat["scenarios"][0] == entry
    reckoning = next(s for s in cat["scenarios"] if s["path"].endswith("lesson-reckoning.yaml"))
    assert reckoning["seat"] == "officer" and entry["seat"] == ""

    bare = Scenario()
    bare.wind_from_deg, bare.wind_speed_kn, bare.ship_heading_deg = 0.0, 15.0, 293.0
    a = make_world(7, "data/ships/frigate-36.yaml", bare)
    sf = load_scenario(SCENARIOS / "first-passage.yaml")
    assert sf.seed == 7 and not sf.standing_orders and not sf.orders
    b = make_scenario_world(sf)
    begin(b, sf)
    for w in (a, b):
        w.submit("set plain sail")
        w.submit("brace sharp up on the starboard tack")
        w.run(480)
    la = [(e.tick, e.kind, e.text) for e in a.log]
    lb = [(e.tick, e.kind, e.text) for e in b.log]
    assert la[0][2].startswith("Open water.") and lb[0][2].startswith("A first passage.")
    assert la[0][2].split(". ", 1)[1] == lb[0][2].split(". ", 1)[1]
    assert la[1:] == lb[1:] and len(la) > 20


def test_the_state_lists_the_saves_by_name_newest_first_and_opens_none(port, client):
    saves = port.tmp / "saves"
    saves.mkdir(parents=True, exist_ok=True)
    (saves / "older.json").write_text("not a save: its name alone is listed", encoding="utf-8")
    (saves / "newer.json").write_text("{}", encoding="utf-8")
    os.utime(saves / "older.json", (1_700_000_000, 1_700_000_000))
    (saves / "newer.checkpoint").write_text("", encoding="utf-8")
    (saves / "notes.txt").write_text("", encoding="utf-8")
    state = client.get("/api/harbour/state").json()["saves"]
    assert state["place"] == str(saves.resolve())
    assert [s["name"] for s in state["saves"]] == ["newer", "older"]
    assert state["saves"][1]["written"].startswith("2023-11-1")


def test_a_scenario_says_what_it_is_before_it_is_started_and_who_may_be_gone_aboard(client):
    """Package 96b, step 3: the page asks what a scenario is before the start: its own
    lines as a driver prints them (the file's path left out), and the other ships with a
    captain of their own, which the player may be aboard from the first minute."""
    r = client.get("/api/harbour/scenario", params={"path": "data/scenarios/tender.yaml"}).json()
    assert r["lines"][0] == "Scenario: The tender, Torbay for Plymouth and home."
    assert any(ln.startswith("She starts at") for ln in r["lines"]) and r["refusal"] == ""
    assert r["aboard"] == ["Raven"]
    first = client.get(
        "/api/harbour/scenario", params={"path": "data/scenarios/first-passage.yaml"}
    ).json()
    assert first["aboard"] == [] and first["lines"] == ["Scenario: A first passage."]


def test_a_game_is_started_aboard_another_ship_and_a_bare_ship_with_her_wind_and_heading(
    port, client
):
    """Package 96b, step 3: what the command line alone could say (`--ship NAME`, `--wind`,
    `--heading`) said from the page's start; each refused in words when it is not so."""
    r = client.post(
        "/api/harbour/start", json={"scenario": "data/scenarios/tender.yaml", "aboard": "Raven"}
    )
    assert r.status_code == 200, r.text
    assert "Following the Raven." in r.json()["lines"]
    assert r.json()["game"]["chosen"]["aboard"] == "Raven"
    with port.driver.lock:
        assert port.driver.world.followed_words == "Raven"
    r = client.post(
        "/api/harbour/start", json={"scenario": "data/scenarios/tender.yaml", "aboard": "Nobody"}
    )
    assert r.status_code == 400 and "Nobody" in r.json()["detail"]
    # a bare ship with the primer's chapter 7 wind and heading
    r = client.post(
        "/api/harbour/start",
        json={"ship": "data/ships/frigate-36.yaml", "seed": 7, "wind": "0, 15", "heading": "293"},
    )
    assert r.status_code == 200, r.text
    with port.driver.lock:
        opening = next(e.text for e in port.driver.world.log if e.kind == "world.start")
    assert opening == "Open water. Wind N, 15 knots, a moderate breeze. Heading WNW (293°)."
    for bad in ({"wind": "north"}, {"wind": "400,15"}, {"wind": "10"}, {"heading": "999"}):
        r = client.post("/api/harbour/start", json={"ship": "data/ships/cutter.yaml", **bad})
        assert r.status_code == 400, (bad, r.text)
        assert "wind" in r.json()["detail"] or "heading" in r.json()["detail"]


def test_the_catalogue_gives_each_kind_her_file_fit_and_roles_and_each_file_her_fits(client):
    """Package 96b, step 5: what the ship's card fills its blanks from, the game's own
    (`world.ships.description`, each ship file's `armament`): nothing invented by the page."""
    cat = client.get("/api/harbour/catalogue").json()
    kinds = {k["id"]: k for k in cat["kinds"]}
    assert list(kinds) == cat["descriptions"]
    revenue = kinds["revenue cutter"]
    assert revenue["file"] == "data/ships/cutter.yaml" and revenue["fit"] == "long guns"
    assert revenue["roles"] == ["revenue"] and "cutter" in revenue["rig"]
    assert kinds["merchant brig"]["roles"] == ["merchant", "packet", "indiaman"]
    assert kinds["sixty-four"]["roles"] == []  # her file gives her kind none
    cutter = cat["fits"]["data/ships/cutter.yaml"]
    assert cutter == {"fits": ["carronades", "long guns"], "default": "carronades"}
    assert len(cat["fits"]["data/ships/seventy-four.yaml"]["fits"]) == 3
    assert set(cat["fits"]) == set(cat["ships"])  # every ship offered, and no boat


def test_the_proof_says_a_fit_her_kind_has_not_and_a_heading_read_by_nothing(client):
    """Package 96b, step 5 (the design's traps 4 and 5): the loader takes another ship's
    fit unchecked and refuses her only when she is promoted, and reads her heading
    nowhere; the maker's proof says both, and proves the scenario as the game does."""
    fields = client.get(
        "/api/harbour/scenario", params={"path": "data/scenarios/first-action.yaml"}
    ).json()["fields"]
    r = client.post("/api/harbour/scenario/prove", json={"fields": fields})
    assert r.status_code == 200 and not [ln for ln in r.json()["lines"] if "To know" in ln]
    fields["ships"][0]["fit"] = "forty carronades"
    fields["ships"][0]["heading_deg"] = 90
    r = client.post("/api/harbour/scenario/prove", json={"fields": fields})
    assert r.status_code == 200, r.text
    said = [ln for ln in r.json()["lines"] if "To know" in ln]
    assert len(said) == 2 and "forty carronades" in said[0] and "is none of her file's" in said[0]
    assert "heading is read by nothing" in said[1]
    fields["ships"][0]["fit"] = "unarmed"
    del fields["ships"][0]["heading_deg"]
    r = client.post("/api/harbour/scenario/prove", json={"fields": fields})
    assert not [ln for ln in r.json()["lines"] if "To know" in ln]


def test_the_shelves_file_names_only_scenarios_that_are_there_and_each_once():
    from freesail.ui.harbour import SHELVES_FILE, Harbour

    # the page's own, with the page's files: not among the scenarios (the tests that walk
    # them would take it for one), and not under data/ at all (the range's audit classes
    # every dated key there, and the rules' fingerprint hashes every file there)
    assert SHELVES_FILE.parent != SCENARIOS
    assert ROOT / "data" not in SHELVES_FILE.parents
    assert SHELVES_FILE == ROOT / "client" / "harbour-shelves.yaml" and SHELVES_FILE.is_file()
    assert not (ROOT / "data" / "harbour").exists()
    named = [s["file"] for shelf in Harbour.shelves(None) for s in shelf["scenarios"]]
    assert len(named) == len(set(named))
    there = {p.stem for p in SCENARIOS.glob("*.yaml")}
    assert set(named) <= there, sorted(set(named) - there)
    assert all(s["says"] for shelf in Harbour.shelves(None) for s in shelf["scenarios"])


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

    @property
    def page(self) -> dict[str, str]:
        """The headers of the game's own page (package 115): its origin and its mark."""
        return {"x-freesail-page": self.port.app.state.guard.token, "origin": self.url}

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

        with httpx.Client(base_url=live.url, timeout=60, headers=live.page) as c:
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

            with httpx.Client(base_url=live.url, timeout=60, headers=live.page) as c:
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
    pg.click("nav.tabs button[data-tab=game]")
    pg.select_option("#s-scenario", "data/scenarios/directed-passage.yaml")
    pg.select_option("#s-seat", "officer")
    assert not pg.is_visible("#s-brief")  # behind "more for this game" (package 96b, step 3)
    pg.click("#s-more summary")
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
    # one field changed in the form: that field alone written again (the part opened
    # first: the sheet is folded, package 96b, step 4)
    assert not pg.is_visible('#maker [data-field="seed"]')
    pg.click("#maker fieldset[data-part=day] > legend")
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


def test_in_the_browser_the_list_is_by_shelf_and_the_tests_scenarios_come_with_the_tick(
    browser_page,
):
    """Package 96b, step 1: the page's scenarios by shelf, the lessons first; no gate's day
    in the list until the tick box asks for the scenarios kept for tests and gates; the
    sentence of the scenario chosen said under the list; no boat among the ships."""
    pg, live, port, errors = browser_page
    pg.goto(live.url + "/harbour")
    pg.wait_for_function("window.freesailHarbour && window.freesailHarbour.ready", timeout=60_000)
    pg.click("nav.tabs button[data-tab=game]")
    shelves = pg.eval_on_selector_all("#s-scenario optgroup", "els => els.map(e => e.label)")
    assert shelves[:2] == ["Begin here", "Lessons"] and "Kept for tests and gates" not in shelves
    listed = pg.eval_on_selector_all("#s-scenario option", "els => els.map(e => e.value)")
    assert listed[:2] == [
        "data/scenarios/first-passage.yaml",
        "data/scenarios/lesson-landfall.yaml",
    ]
    assert "data/scenarios/gate-4c-day.yaml" not in listed
    assert "data/scenarios/squadron.yaml" not in listed
    assert "chapter 7" in pg.inner_text("#s-says")
    pg.select_option("#s-scenario", "data/scenarios/first-action.yaml")
    assert "privateer" in pg.inner_text("#s-says") and "first-action.yaml" in pg.inner_text(
        "#s-says"
    )
    pg.check("#s-tests")
    listed = pg.eval_on_selector_all("#s-scenario option", "els => els.map(e => e.value)")
    assert "data/scenarios/gate-4c-day.yaml" in listed
    assert pg.input_value("#s-scenario") == "data/scenarios/first-action.yaml"  # the choice kept
    made = pg.eval_on_selector_all("#m-pick option", "els => els.map(e => e.value)")
    assert "data/scenarios/gate-4c-day.yaml" in made
    pg.uncheck("#s-tests")
    listed = pg.eval_on_selector_all("#s-scenario option", "els => els.map(e => e.value)")
    assert "data/scenarios/gate-4c-day.yaml" not in listed
    ships = pg.eval_on_selector_all("#s-ship option", "els => els.map(e => e.value)")
    assert "data/ships/cutter.yaml" in ships and not [s for s in ships if "boat-" in s]
    assert errors == []


def test_in_the_browser_the_page_opens_on_begin_and_the_first_game_is_one_button(browser_page):
    """Package 96b, step 2: a fresh page opens on the first panel, with no form on it: the
    first game named, the four lessons numbered in the primer's order, no saved game where
    there is none, and the way to all the games. The first game's button starts it and
    goes to the game's page, the clock held; back at the harbour the panel leads with the
    game in play."""
    pg, live, port, errors = browser_page
    pg.goto(live.url + "/")
    pg.wait_for_function("window.freesailHarbour && window.freesailHarbour.ready", timeout=60_000)
    assert pg.is_visible("section[data-page=begin]") and not pg.is_visible("#start-form")
    assert (
        pg.locator("section[data-page=begin] input, section[data-page=begin] select").count() == 0
    )
    assert pg.inner_text("#btn-b-first") == "begin: A first passage"
    assert "chapter 7" in pg.inner_text("#b-first-says")
    lessons = pg.eval_on_selector_all("#b-lessons button", "els => els.map(e => e.textContent)")
    assert lessons == [
        "A landfall on one headland",
        "The officer's own reckoning, off the Lizard",
        "Pilot water, Black Head to Falmouth road",
        "A night off a lee shore, the Nare Head to the Deadman",
    ]
    assert not pg.is_visible("#b-save") and not pg.is_visible("#b-playing")
    pg.click("#btn-b-all")
    assert pg.is_visible("#start-form")
    pg.click("nav.tabs button[data-tab=begin]")
    pg.click("#btn-b-first")
    pg.wait_for_function(
        "document.getElementById('ship-name') && "
        "document.getElementById('status').textContent === 'connected'",
        timeout=60_000,
    )
    assert not pg.url.endswith("/harbour")
    with port.driver.lock:
        assert port.driver.world.scenario.name == "A first passage"
        assert not port.driver.running and port.driver.world.clock.tick == 0
    pg.goto(live.url + "/harbour")
    pg.wait_for_function("window.freesailHarbour && window.freesailHarbour.ready", timeout=60_000)
    pg.click("nav.tabs button[data-tab=begin]")
    pg.wait_for_selector("#b-playing:not([hidden])", timeout=10_000)
    assert "A first passage" in pg.inner_text("#b-playing-says")
    assert "held" in pg.inner_text("#b-playing-says")
    # a lesson that is the officer's own seats the player at the officer's station
    pg.click("#b-lessons button[data-path='data/scenarios/lesson-reckoning.yaml']")
    pg.wait_for_function(
        "document.getElementById('status').textContent === 'connected'", timeout=60_000
    )
    with port.driver.lock:
        seat = port.driver.world.player_seat
        assert seat is not None and "officer" in seat.station.name
    assert errors == []


def test_in_the_browser_a_game_says_what_it_is_and_a_save_is_taken_up_from_the_list(
    browser_page,
):
    """Package 96b, step 3: the new game's panel as three choices and "more": the scenario
    chosen says its own lines before the start; the ships to be aboard are offered where
    the scenario has one; the rest is behind a step; a bare ship takes a wind and a
    heading; and a saved game is picked from the list of the saves place."""
    pg, live, port, errors = browser_page
    pg.goto(live.url + "/harbour")
    pg.wait_for_function("window.freesailHarbour && window.freesailHarbour.ready", timeout=60_000)
    pg.click("nav.tabs button[data-tab=game]")
    pg.wait_for_function(
        "document.getElementById('s-lines').textContent.indexOf('A first passage') >= 0"
    )
    assert not pg.is_visible("#s-aboard") and not pg.is_visible("#s-seed")
    assert not pg.is_visible("#s-wind") and not pg.is_visible("#s-load-pick")
    pg.check("#s-tests")
    pg.select_option("#s-scenario", "data/scenarios/tender.yaml")
    pg.wait_for_selector("#s-aboard", state="visible", timeout=10_000)
    assert "Brixham" in pg.inner_text("#s-lines") or "50°" in pg.inner_text("#s-lines")
    pg.select_option("#s-aboard", "Raven")
    pg.click("#btn-start")
    pg.wait_for_selector("#btn-to-game:not([hidden])", timeout=60_000)
    assert "Following the Raven." in pg.inner_text("#start-words")
    # a save written by the game in play is in the list, and is taken up from it
    assert port.driver.save("step-three").kind == "driver.saved"
    pg.select_option("#s-from", "load")
    pg.wait_for_function(
        "Array.prototype.some.call(document.getElementById('s-load-pick').options, "
        "function (o) { return o.value === 'step-three'; })",
        timeout=10_000,
    )
    assert str(port.tmp / "saves") in pg.inner_text("#s-load-says")
    pg.select_option("#s-load-pick", "step-three")
    assert pg.input_value("#s-load") == "step-three"
    pg.click("#btn-start")
    pg.wait_for_function(
        "document.getElementById('start-words').textContent.indexOf('step-three') >= 0",
        timeout=60_000,
    )
    assert "refusal" not in (pg.get_attribute("#start-words", "class") or "")
    # a bare ship: her wind and her heading beside her
    pg.select_option("#s-from", "ship")
    assert pg.is_visible("#s-wind") and not pg.is_visible("#s-lines")
    pg.select_option("#s-ship", "data/ships/frigate-36.yaml")
    pg.fill("#s-wind", "0,15")
    pg.fill("#s-heading", "293")
    pg.click("#btn-start")
    pg.wait_for_function(
        "document.getElementById('g-title').textContent === 'Open water'", timeout=60_000
    )
    with port.driver.lock:
        opening = next(e.text for e in port.driver.world.log if e.kind == "world.start")
    assert "Wind N, 15 knots" in opening and "(293°)" in opening
    assert errors == []


def test_in_the_browser_the_sheet_is_folded_and_each_part_says_what_is_set(browser_page):
    """Package 96b, step 4 (docs/design/Design-Harbour.md §2.3): "change this scenario" on
    the game tab reads it into the sheet; every part is closed to a line written from the
    fields, so that the whole scenario reads with nothing opened (the squadron and the
    weather's system that the form has no field for among them); a part's name opens it,
    and a field changed changes its line; saved with nothing changed it is the same file;
    a written brief touched in the form keeps the examples the form does not show; and the
    game in play is a line at the head of every tab."""
    pg, live, port, errors = browser_page
    pg.goto(live.url + "/harbour")
    pg.wait_for_function("window.freesailHarbour && window.freesailHarbour.ready", timeout=60_000)
    assert pg.inner_text("#in-play-line") == "no game yet" and not pg.is_visible("#g-title")
    pg.click("nav.tabs button[data-tab=game]")
    pg.select_option("#s-scenario", "data/scenarios/blockade.yaml")
    pg.click("#btn-s-change")
    pg.wait_for_function("document.getElementById('m-source').textContent.indexOf('blockade') >= 0")
    assert pg.is_visible("#maker") and pg.is_visible("#in-play-line")
    parts = pg.eval_on_selector_all(
        "#maker fieldset[data-part]", "els => els.map(e => e.getAttribute('data-part'))"
    )
    assert parts == [
        "day",
        "ship",
        "start",
        "papers",
        "weather",
        "ships",
        "sea",
        "orders",
        "stations",
    ]
    assert pg.locator("#maker fieldset[data-part]:not(.folded)").count() == 0
    assert not pg.is_visible('#maker [data-field="seed"]') and not pg.is_visible("#m-ships")

    def line(part: str) -> str:
        return pg.inner_text(f'#maker [data-line="{part}"]')

    assert (
        line("day") == '"The blockade of Brest blown off"; 12 June 1805, 10:00; seed 7; of Britain.'
    )
    assert line("ship").startswith("The frigate-36; her file's own fit of guns; a glass aboard")
    assert "on the chart of channel-west; heading 20°" in line("start")
    assert "one weather system written out (the low)" in line("weather").lower()
    assert line("ships") == (
        "Three ships: Naiad of Britain, a frigate; Nimble of Britain, a brig-sloop; "
        "Hortense of France, a frigate; the inshore squadron, a squadron in line ahead."
    )
    assert line("sea").startswith("Four ports: brest, falmouth, plymouth, torbay")
    assert "first order: set plain sail" in line("orders") and "Ushant" in line("orders")
    assert line("stations") == "You are the captain; nobody else is said; no director."
    # a part opened by its name; a field changed changes its line
    pg.click("#maker fieldset[data-part=day] > legend")
    assert pg.is_visible('#maker [data-field="seed"]')
    pg.fill('#maker [data-field="seed"]', "11")
    assert "seed 11" in line("day")
    pg.click("#btn-m-open")
    assert pg.is_visible("#m-ships") and pg.is_visible("#m-chart")
    pg.click("#btn-m-close")
    assert pg.locator("#maker fieldset[data-part]:not(.folded)").count() == 0
    # read again and saved with nothing changed: the same file, the squadron and all
    pg.click("#btn-m-read")
    pg.wait_for_function("window.freesailHarbour.foldLines && true")
    pg.wait_for_function(
        "document.querySelector('#maker [data-line=day]').textContent.indexOf('seed 7') >= 0"
    )
    pg.click("#btn-m-save")
    pg.wait_for_function("window.freesailHarbour.busy === true", timeout=10_000)
    pg.wait_for_function("window.freesailHarbour.busy === false", timeout=60_000)
    assert not pg.is_visible("#m-refusal"), pg.inner_text("#m-refusal")
    assert (port.place / "blockade.yaml").read_bytes() == (SCENARIOS / "blockade.yaml").read_bytes()
    # a brief written out, with examples the form has no field for: the tone changed in the
    # form, and the examples are written again with it
    own = port.place / "briefed.yaml"
    own.write_text(
        (SCENARIOS / "first-passage.yaml").read_text(encoding="utf-8")
        + "director:\n  brief:\n    name: Mine\n    tone: quiet\n"
        + "    limits: {nobody_dies: true, a_limit_of_mine: 3}\n"
        + "    examples:\n      - 'ship \"Nancy\": order heave to'\n",
        encoding="utf-8",
    )
    fields = pg.evaluate(
        """async (path) => {
            const h = window.freesailHarbour;
            await h.readScenario(path);
            const tone = document.querySelector('#m-brief-written [data-brief=tone]');
            tone.value = 'a quiet passage indeed';
            tone.dispatchEvent(new Event('input', { bubbles: true }));
            return h.collect();
        }""",
        str(own),
    )
    brief = fields["director"]["brief"]
    assert brief["tone"] == "a quiet passage indeed" and brief["name"] == "Mine"
    assert brief["examples"] == ['ship "Nancy": order heave to']
    assert brief["limits"] == {"nobody_dies": True, "a_limit_of_mine": 3}
    assert "Mine" in line("stations")
    assert errors == []


def test_in_the_browser_every_ship_is_set_up_on_her_card_and_the_scenario_made_is_played(
    browser_page,
):
    """Package 96b, step 5 (docs/design/Design-Harbour.md §2.4; its step's own trial): a
    scenario made from the form with the player's cutter named and under long guns, a
    revenue cutter under her kind's own guns and a French privateer lugger under British
    colours, each on a card whose blanks are her kind's own words; proved, saved, and
    started: the file says what was chosen and the game has the three ships. What the
    game does not take is said on the card, greyed. A scenario read with what the card
    has no plain field for (a place written as latitude and longitude) is saved the same."""
    pg, live, port, errors = browser_page
    pg.goto(live.url + "/harbour")
    pg.wait_for_function("window.freesailHarbour && window.freesailHarbour.ready", timeout=60_000)
    pg.click("nav.tabs button[data-tab=maker]")
    pg.click("#btn-m-new")
    pg.click("#btn-m-open")
    pg.select_option("#m-port", "falmouth")
    fits = pg.eval_on_selector_all("#m-ship-fit option", "els => els.map(e => e.value)")
    assert fits == ["", "carronades", "long guns", "unarmed"]
    pg.select_option("#m-ship-fit", "long guns")
    pg.fill('#maker [data-field="ship.name"]', "Swift")
    pg.select_option('#maker [data-field="papers.service"]', "kings")
    assert pg.locator("#maker fieldset[data-part=ship] p.not-yet").count() == 3
    for kind, name, nation, colours, bearing in (
        ("revenue cutter", "Vigilant", "britain", "", "160"),
        ("privateer lugger", "Furet", "france", "britain", "200"),
    ):
        pg.click("#btn-m-ship-add")
        card = pg.locator("#m-ships .ship-card").last
        card.locator("[data-col=description]").select_option(kind)
        card.locator("[data-col=name]").fill(name)
        card.locator("[data-col=nation]").select_option(nation)
        card.locator("[data-col=goal]").fill("bound for Plymouth")
        assert not card.locator("[data-col=role]").is_visible()
        card.locator("summary").click()
        if colours:
            card.locator("[data-col=colours]").select_option(colours)
        card.locator(".card-bearing").fill(bearing)
        card.locator(".card-miles").fill("6")
        card.locator(".card-put").click()
        assert card.locator("[data-col=position]").input_value().startswith("50 4.1 N")
        assert card.locator("p.not-yet").count() == 3
    first = pg.locator("#m-ships .ship-card").first
    assert "long guns" in first.locator(".card-says").inner_text()
    assert first.locator("[data-col=role] option").all_text_contents()[1:] == ["revenue"]
    assert first.locator("[data-col=fit] option").first.inner_text() == "her kind's own (long guns)"
    pg.click("#btn-m-close")
    assert pg.inner_text('#maker [data-line="ships"]') == (
        "Two ships: Vigilant of Britain, a revenue cutter; "
        "Furet of France, a privateer lugger under the colours of Britain."
    )
    assert "Swift; her fit long guns; a King's ship" in pg.inner_text('#maker [data-line="ship"]')
    pg.fill("#m-name", "two-cutters")
    pg.click("#btn-m-save")
    pg.wait_for_function("window.freesailHarbour.busy === true", timeout=10_000)
    pg.wait_for_function("window.freesailHarbour.busy === false", timeout=60_000)
    assert not pg.is_visible("#m-refusal"), pg.inner_text("#m-refusal")
    import yaml

    made = yaml.safe_load((port.place / "two-cutters.yaml").read_text(encoding="utf-8"))
    assert made["ship"]["name"] == "Swift" and made["ship"]["fit"] == "long guns"
    assert made["papers"] == {"service": "kings"}
    assert [(s["description"], s["name"], s.get("colours")) for s in made["ships"]] == [
        ("revenue cutter", "Vigilant", None),
        ("privateer lugger", "Furet", "britain"),
    ]
    r = pg.evaluate(
        """async (path) => {
            const r = await fetch('/api/harbour/start', {method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({scenario: path})});
            return r.status;
        }""",
        str(port.place / "two-cutters.yaml"),
    )
    assert r == 200
    with port.driver.lock:
        world = port.driver.world
        assert world.ship.name == "Swift"
        assert {"Furet", "Vigilant"} <= {v.name for v in world.vessels.vessels}
    # the tender: the Raven's place is written as latitude and longitude, which the card
    # shows and does not change; her goal changed, the rest of her entry is as it was
    fields = pg.evaluate(
        """async () => {
            const h = window.freesailHarbour;
            await h.readScenario('data/scenarios/tender.yaml');
            const card = document.querySelector('#m-ships .ship-card');
            const where = card.querySelector('[data-col=position]');
            const goal = card.querySelector('[data-col=goal]');
            goal.value = goal.value + ' ';
            goal.dispatchEvent(new Event('input', { bubbles: true }));
            return {disabled: where.disabled, ships: h.collect().ships, was: h.loaded.fields.ships};
        }"""
    )
    assert fields["ships"] == fields["was"]
    assert fields["disabled"] == isinstance(fields["was"][0]["position"], dict)
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
    with PageClient(port.app) as c:
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
