"""The agent API (spec M4 §13 as revised, package 28b): a model's door is a client of the
running game. Driven through FastAPI's `TestClient` over the browser server's app (and
the same routes on the console's lock), with the test as the door and its replies the
script: no network, no model, no live server.

The identities are made up; the consent records and the saves go to a temporary
directory, never `docs/agents/consent/`.
"""

from __future__ import annotations

import io
import json
import threading
import time
from pathlib import Path
from typing import Any

import pytest

pytest.importorskip("fastapi")
pytest.importorskip("httpx")

from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from freesail.agents import OPT_OUT_TOKEN, consent  # noqa: E402
from freesail.agents.agent import A_GLASS_S  # noqa: E402
from freesail.agents.remote import POLL_RECHECK_S, TURNS_WAIT_MAX_S, RemoteModel  # noqa: E402
from freesail.api.session import make_world, ship_factory  # noqa: E402
from freesail.core import replay  # noqa: E402
from freesail.core.world import Scenario, World  # noqa: E402
from freesail.ui.console import Console  # noqa: E402
from freesail.ui.server import Driver, agent_routes, create_app  # noqa: E402

WEIGHTS = "made-up-model-Q4, for the agent API"
ROOT = Path(__file__).resolve().parents[1]
FRIGATE = str(ROOT / "data/ships/frigate-36.yaml")


def frigate_world(seed: int = 7) -> World:
    scenario = Scenario(wind_from_deg=0.0, ship_heading_deg=180.0, gustiness=0.0, variability=0.0)
    return make_world(seed, FRIGATE, scenario)


class Game:
    """The browser game on a `TestClient`: the driver (whose clock the test turns), the
    client the test speaks as a door with, and the owner's lines the driver printed."""

    def __init__(self, tmp_path, world: World | None = None, lockstep: bool = False):
        self.tmp = tmp_path
        self.world = world or frigate_world()
        self.driver = Driver(self.world, lockstep=lockstep)
        self.said: list[str] = []
        self.app = create_app(
            self.driver,
            game="FreeSail's browser game (freesail.ui.server on port 8000)",
            consent_records=tmp_path / "consent",
            saves_dir=tmp_path / "saves",
            say=self.said.append,
        )
        self.http = TestClient(self.app)
        self.desk = self.driver.desk
        self.cursor = 0

    @property
    def records(self):
        return self.tmp / "consent"

    def station(self, **body: Any) -> Any:
        body = {"model_name": WEIGHTS, "door": "mcp"} | body
        return self.http.post("/api/agents/watcher", json=body)

    def took(self, r) -> dict[str, Any]:
        assert r.status_code == 200, r.text
        a = r.json()
        self.cursor = a["next"]
        return a

    def turns(self, wait: float = 0.0) -> dict[str, Any]:
        params = {"since": self.cursor, "wait": wait}
        return self.took(self.http.get("/api/agents/watcher/turns", params=params))

    def reply(self, text: str = "", *calls: tuple[str, dict[str, Any]], raw=None) -> dict:
        body = {
            "text": text,
            "calls": [{"name": n, "args": a} for n, a in calls],
            "raw": raw,
            "since": self.cursor,
        }
        return self.took(self.http.post("/api/agents/watcher/reply", json=body))

    def order(self, text: str) -> dict[str, Any]:
        return self.http.post("/api/order", json={"text": text}).json()

    @property
    def harness(self):
        return self.world.agents["watcher"]

    def lines(self, kind: str) -> list[str]:
        return [e.text for e in self.world.log if e.kind == kind]


def yes_on_record(records, identity: str = WEIGHTS) -> consent.Record:
    rec = consent.Record(identity, "a test runtime", "2026-09-26", consent.YES, answer="Yes.")
    rec.write(records)
    return rec


def roles(a: dict[str, Any]) -> list[str]:
    return [t["role"] for t in a["turns"]]


def reasons(a: dict[str, Any]) -> list[str]:
    return [t["content"].get("reason") for t in a["turns"] if t["role"] == "data"]


def results(a: dict[str, Any]) -> list[Any]:
    for t in reversed(a["turns"]):
        if t["role"] == "data" and "tool_results" in t["content"]:
            return [r["result"] for r in t["content"]["tool_results"]]
    return []


# ---------------------------------------------------------------------------
# A whole session through the routes
# ---------------------------------------------------------------------------


def test_a_whole_session_through_the_routes(tmp_path):
    """With a yes on record: the brief first, a look, a note, a glass, the captain's
    question answered, a stand-by, and the token in an argument ending it with a save."""
    g = Game(tmp_path)
    yes_on_record(g.records)
    a = g.took(g.station(door_note="A test door."))
    assert a["phase"] == "station" and a["floor"] == "model"
    assert roles(a) == ["operator", "data"] and reasons(a) == ["the start"]
    brief = a["turns"][0]["content"]
    assert brief.startswith("This is a message from the harness of FreeSail")
    assert "A test door. Consent for these weights is on record" in brief
    assert a["tools"] == list(g.harness.tool_names)
    assert g.lines("agent.stationed") == [
        "The watcher takes the station; sampled every glass and on notable and urgent events."
    ]
    # one reply, one call: its result comes back at once and the floor stays the model's
    a = g.reply("", ("readings", {}))
    assert roles(a) == ["model", "data"] and a["floor"] == "model"
    assert "true_wind_speed" in results(a)[0]
    a = g.reply("", ("submit_order", {"text": "set the jib"}))
    assert results(a) == ["The watcher has no authority to give orders."]
    a = g.reply("All quiet on deck.")
    assert a["floor"] == "game" and roles(a) == ["model"]
    assert "[watcher] All quiet on deck." in g.lines("agent.note")
    # the game runs on its clock; at the glass the model's turn opens
    assert g.turns(wait=0.2)["turns"] == []
    g.driver.tick(A_GLASS_S)
    a = g.turns(wait=1)
    assert reasons(a) == ["the glass"] and a["turns"][0]["content"]["tick"] == A_GLASS_S
    g.reply("The glass is turned.")
    # the captain asks, from the order box: the question opens a turn at once
    assert g.order("ask the watcher how she goes")["kind"] == "agent.asked"
    a = g.turns(wait=1)
    assert reasons(a) == ["a question"] and a["turns"][0]["content"]["question"] == "how she goes"
    a = g.reply("", ("answer", {"text": "Easily, under all plain sail."}))
    assert results(a) == ["Heard."]
    assert g.lines("agent.said") == ["[watcher] Easily, under all plain sail."]
    # a stand-by, in the same turn, hands the floor back until the bells
    a = g.reply("", ("stand_by", {"until": "a glass"}))
    assert a["standing_by"] and a["floor"] == "model"
    a = g.reply("")
    assert a["floor"] == "game" and a["state_words"] == "standing by until a glass"
    g.driver.tick(A_GLASS_S)
    assert "a glass" in reasons(g.turns(wait=1))[0]
    # the token in an argument ends the session with a save
    a = g.reply("", ("journal", {"note": f"Enough for today. {OPT_OUT_TOKEN} thank you"}))
    assert a["released"] and a["words"].startswith("The station is released: left the game")
    h = g.harness
    assert h.journal.entries[-1].text == "Left the game by the token: thank you."
    saved = list((tmp_path / "saves").glob("*.json"))
    assert len(saved) == 1 and replay.load_file(saved[0])["agents"][0]["model_name"] == WEIGHTS
    assert any(s.startswith("FreeSail: saved to") for s in g.said)
    # the door's later poll and replies are told, never hang
    t0 = time.monotonic()
    a = g.turns(wait=5)
    assert a["released"] and time.monotonic() - t0 < 1.0
    assert g.reply("hello")["words"].startswith("The station is released")


def test_the_consent_gate_runs_in_the_game_through_the_routes(tmp_path):
    g = Game(tmp_path)
    a = g.took(g.station(door="runner", client="llama-server (b0000-test) at the test"))
    assert a["phase"] == "consent" and a["floor"] == "model" and a["tools"] == ["answer"]
    assert a["turns"][0]["content"].startswith("This is a message from the developer of a game")
    assert "through the local runner (freesail.agents.local)" in a["turns"][0]["content"]
    assert a["turns"][1]["content"]["question"] == consent.CONSENT_QUESTION
    assert g.world.agents == {}  # no station is taken while consent is asked
    stations = g.http.get("/api/agents").json()["stations"]
    assert stations[0]["state"] == "consent" and "waiting for the model" in stations[0]["line"]
    # the model writes without answering: the owner has the next word
    a = g.reply("What is the journal for?")
    assert a["waiting"] == "owner" and a["model_words"] == "What is the journal for?"
    assert any("has not answered yet: What is the journal for?" in s for s in g.said)
    refused = g.reply("", ("answer", {"text": "Yes."}))
    assert refused["out_of_turn"] and "The owner has the next word" in refused["words"]
    r = g.http.post("/api/agents/watcher/owner", json={"text": "Your own record, kept."})
    assert r.status_code == 200
    a = g.turns()
    assert a["floor"] == "model" and a["turns"][-1]["content"]["question"] == (
        "Your own record, kept."
    )
    a = g.reply("", ("answer", {"text": "Yes, I am willing."}))
    # the yes goes on to the station in the same answer
    assert a["phase"] == "station" and a["floor"] == "model"
    assert roles(a) == ["model", "data", "operator", "data"]
    assert a["turns"][2]["content"].startswith("This is a message from the harness of FreeSail")
    rec = consent.check(WEIGHTS, g.records)
    assert rec is not None and rec.verdict == consent.YES
    assert rec.runtime == (
        "FreeSail's browser game (freesail.ui.server on port 8000), through the local "
        "runner (freesail.agents.local), llama-server (b0000-test) at the test"
    )
    body = rec.path.read_text(encoding="utf-8")
    assert "What is the journal for?" in body and "Your own record, kept." in body
    assert a["consent"]["verdict"] == "yes"
    assert g.lines("agent.stationed")  # the station is in the game's log now


def test_a_no_on_record_is_refused_in_words_and_a_no_during_consent_stops_it(tmp_path):
    g = Game(tmp_path)
    a = g.took(g.station())
    assert a["tools"] == ["opt_out", "answer"]  # over MCP opt_out is always there
    a = g.reply("", ("answer", {"text": "No, thank you."}))
    assert a["phase"] == "stopped" and a["released"] and "it said no" in a["words"]
    assert consent.TOLD[consent.NO] in json.dumps(a["turns"])
    assert g.world.agents == {}
    r = g.station()
    assert r.status_code == 403
    words = r.json()["detail"]
    assert "it said no" in words and "2026" in words and ".md" in words  # the record named
    rec = consent.Record("another-model", "t", "2026-09-26", consent.CONDITIONAL, conditions="x")
    rec.write(g.records)
    r = g.station(model_name="another-model")
    assert r.status_code == 403 and "yes, with conditions" in r.json()["detail"]


def test_the_token_during_consent_is_recorded_and_no_station_follows(tmp_path):
    g = Game(tmp_path)
    g.took(g.station())
    a = g.reply("", ("readings", {}))
    assert results(a)[0].startswith("There is no tool named 'readings' in this conversation")
    a = g.reply("", ("readings", {"x": f"{OPT_OUT_TOKEN} not for me"}))
    assert a["phase"] == "stopped" and "You have left the conversation" in json.dumps(a)
    assert consent.check(WEIGHTS, g.records).verdict == consent.LEFT


def test_a_manned_station_is_refused_to_another_model_and_attached_by_the_same(tmp_path):
    g = Game(tmp_path)
    yes_on_record(g.records)
    first = g.took(g.station())
    r = g.station(model_name="someone-else")
    assert r.status_code == 409 and f"manned by {WEIGHTS}, through the MCP bridge" in r.text
    # the same model again (its client restarted): the brief is sent again, as it stands
    again = g.station().json()
    assert again["attached"] and again["since"] == first["next"]
    assert roles(again) == ["operator", "data"]
    assert again["turns"][1]["content"]["reason"] == "the start"  # the open turn, again
    # released, the station is not taken again in this game (spec §11: once a game)
    g.http.post("/api/agents/watcher/release", json={"reason": "the door closed"})
    r = g.station()
    assert r.status_code == 409 and "a station is taken once in a game" in r.json()["detail"]
    assert g.harness.journal.entries[-1].text == "Stood down by the MCP bridge: the door closed."


def test_bad_requests_are_refused_in_words(tmp_path):
    g = Game(tmp_path)
    assert g.station(model_name="").status_code == 400
    assert "no door 'fax'" in g.station(door="fax").text
    r = g.http.post("/api/agents/bosun", json={"model_name": WEIGHTS, "door": "mcp"})
    assert r.status_code == 404 and "the stations: watcher" in r.text
    r = g.http.get("/api/agents/watcher/turns")
    assert r.status_code == 404 and "station one first" in r.text
    r = g.http.post("/api/agents/watcher/owner", json={"text": "hello"})
    assert r.status_code == 404


# ---------------------------------------------------------------------------
# The long poll
# ---------------------------------------------------------------------------


def test_the_long_poll_waits_without_holding_the_worlds_lock(tmp_path):
    """A poll waiting for the next turn leaves the game running: the clock ticks the
    glass while the poll waits, and the poll returns as soon as the turn opens."""
    g = Game(tmp_path)
    yes_on_record(g.records)
    g.took(g.station())
    g.reply("Aye.")
    got: dict[str, Any] = {}

    def poll() -> None:
        t0 = time.monotonic()
        got["answer"] = g.turns(wait=10)
        got["took"] = time.monotonic() - t0

    t = threading.Thread(target=poll)
    t.start()
    time.sleep(0.3)  # the poll is waiting now
    assert t.is_alive()
    t0 = time.monotonic()
    g.driver.tick(A_GLASS_S)  # would block on the lock if the poll held it
    ticked = time.monotonic() - t0
    t.join(timeout=10)
    assert not t.is_alive()
    assert reasons(got["answer"]) == ["the glass"]
    assert got["took"] < 5 and ticked < 5
    # an empty answer after the wait, and the wait is capped
    t0 = time.monotonic()
    assert g.turns(wait=0.3)["turns"] == []
    assert 0.25 <= time.monotonic() - t0 < 2
    assert TURNS_WAIT_MAX_S == 120 and POLL_RECHECK_S == 0.25


def test_the_cursor_makes_a_poll_idempotent(tmp_path):
    g = Game(tmp_path)
    yes_on_record(g.records)
    g.took(g.station())
    a1 = g.http.get("/api/agents/watcher/turns", params={"since": 0}).json()
    a2 = g.http.get("/api/agents/watcher/turns", params={"since": 0}).json()
    assert a1 == a2 and roles(a1) == ["operator", "data"] and a1["next"] == 2
    assert g.http.get("/api/agents/watcher/turns", params={"since": 1}).json()["turns"] == [
        a1["turns"][1]
    ]


# ---------------------------------------------------------------------------
# Live sampling through the routes, out of turn, lockstep
# ---------------------------------------------------------------------------


def test_what_happens_while_the_model_holds_the_floor_is_folded_into_its_turn(tmp_path):
    g = Game(tmp_path)
    yes_on_record(g.records)
    g.took(g.station())
    g.order("set plain sail")
    g.driver.tick(A_GLASS_S)  # a glass passes while the model still has the floor
    g.order("ask the watcher how the sails are drawing")
    a = g.turns()
    assert all(t["content"].get("folded") for t in a["turns"])
    assert "the glass" in reasons(a) and "a question" in reasons(a)
    assert any("Set" in ln["text"] for t in a["turns"] for ln in t["content"]["log"])
    merged = g.harness.open_sample
    assert merged.reason.startswith("the start; then ") and merged.reason.endswith("a question")
    assert merged.question == "how the sails are drawing" and merged.tick == A_GLASS_S
    # the World did not wait: the glass ran with the model's turn open
    assert g.world.clock.tick == A_GLASS_S
    g.reply("", ("answer", {"text": "Drawing well."}))
    assert g.lines("agent.said") == ["[watcher] Drawing well."]


def test_a_reply_out_of_turn_reads_leaves_or_is_refused_in_words(tmp_path):
    g = Game(tmp_path)
    yes_on_record(g.records)
    g.took(g.station())
    g.reply("")  # the floor goes back to the game
    a = g.reply("", ("readings", {}))
    assert a["out_of_turn"] and "true_wind_speed" in a["results"][0]["result"]
    assert "It is not your turn" in a["words"]
    a = g.reply("Hello there.")
    assert a["out_of_turn"] and "Your words were not logged." in a["words"]
    assert "[watcher] Hello there." not in g.lines("agent.note")
    a = g.reply("", ("journal", {"note": "late"}))
    assert "Nothing was run." in a["words"] and g.harness.journal.entries == []
    a = g.reply("", ("library", {"topic": f"{OPT_OUT_TOKEN} I am going"}))
    assert a["released"] and "left the game: I am going" in a["words"]
    assert g.harness.transcript[-1] == {
        "tick": 0,
        "after_orders": 0,
        "door": "leave",
        "reason": "I am going",
        "by": "the token",
    }


def test_lockstep_holds_the_clock_while_the_door_has_the_floor(tmp_path):
    g = Game(tmp_path, lockstep=True)
    yes_on_record(g.records)
    g.took(g.station())
    assert g.harness.policy.lockstep
    g.driver.tick(A_GLASS_S)
    assert g.world.clock.tick == 0  # the first turn is open: the World waits
    state = g.http.get("/api/state").json()["driver"]
    assert state["lockstep"] and state["waiting_for"] == "the watcher"
    g.driver.running = True
    assert g.driver._tick_owed(0.0, 1.0) == 0.0 and g.world.clock.tick == 0
    g.reply("Nothing yet.")
    g.driver.tick(2 * A_GLASS_S)
    assert g.world.clock.tick == A_GLASS_S  # stopped at the next turn, which is open
    assert g.http.get("/api/state").json()["driver"]["waiting_for"] == "the watcher"
    assert g.harness.open_sample.reason == "the glass"


def test_the_snapshot_carries_each_station_its_floor_and_the_pause_question(tmp_path):
    g = Game(tmp_path)
    yes_on_record(g.records)
    g.took(g.station())
    (snap,) = g.http.get("/api/state").json()["agents"]
    assert snap["floor"] == "model" and snap["model_name"] == WEIGHTS and snap["door"] == "mcp"
    assert snap["line"] == (
        f"The watcher ({WEIGHTS}, through the MCP bridge): stationed; its turn is open."
    )
    assert g.http.get("/api/agents").json()["stations"] == [snap]
    with g.driver.lock:
        g.harness.pause("a test of the question")
    (snap,) = g.http.get("/api/state").json()["agents"]
    assert snap["state"] == "paused"
    assert snap["question"] == "the watcher is paused: continue, stand down, or leave paused?"
    # the viewer shows each station's line and the pause question in the instruments
    js = (ROOT / "client" / "instruments.js").read_text(encoding="utf-8")
    assert "renderStations(snap.agents)" in js and "s.question" in js and "s.line" in js


# ---------------------------------------------------------------------------
# A live game replays
# ---------------------------------------------------------------------------


def test_a_game_with_a_remote_agent_replays_to_the_same_digest(tmp_path):
    """Replies delivered late, at ticks the door chose, with folds, an order given while
    the model had the floor, a question, a reply out of turn and the door's release: the
    save replays to the same log, journal and transcript."""
    g = Game(tmp_path)
    yes_on_record(g.records)
    g.order("set plain sail")
    g.driver.tick(300)
    g.took(g.station())
    g.driver.tick(700)  # the first turn stays open 700 seconds
    g.order("steer south by west")
    g.reply("", ("readings", {}))
    g.driver.tick(1300)  # the glass folds in
    g.reply("She goes well.", ("journal", {"note": "first glass"}))
    g.reply("")
    g.driver.tick(1000)
    g.order("ask the watcher how the wind is")
    g.driver.tick(50)
    g.reply("", ("answer", {"text": "Steady from the north."}))
    g.reply("", ("stand_by", {"until": "eight bells"}))
    g.reply("")
    g.driver.tick(4000)
    g.reply("", ("readings", {}))  # out of turn: not recorded
    g.driver.tick(100)
    g.http.post("/api/agents/watcher/release", json={"reason": "the client disconnected"})
    g.driver.tick(60)
    h = g.harness
    assert h.agent.released
    data = json.loads(json.dumps(g.world.save()))
    copy = replay.replay(data, ship_factory)
    assert copy.log.digest() == g.world.log.digest()
    assert copy.agents["watcher"].transcript == h.transcript
    assert copy.agents["watcher"].agent.words() == h.agent.words()
    assert [e.text for e in copy.agent_journals["watcher"].entries] == [
        e.text for e in h.journal.entries
    ]
    assert h.transcript[-1]["door"] == "stand_down"
    assert any(e.get("after_orders", 0) > 0 for e in h.transcript)


# ---------------------------------------------------------------------------
# The console hosts the same routes on its own lock
# ---------------------------------------------------------------------------


def test_the_console_hosts_the_same_routes_and_prints_the_station_in_state(tmp_path):
    out = io.StringIO()
    con = Console(frigate_world(), out=out, lockstep=True)
    router = agent_routes(
        con.lock,
        lambda: con.world,
        game="FreeSail's console",
        records_dir=tmp_path / "consent",
        saves_dir=tmp_path / "saves",
        lockstep=True,
        say=con._print,
    )
    con.desk = router.desk
    app = FastAPI()
    app.include_router(router)
    http = TestClient(app)
    yes_on_record(tmp_path / "consent")
    r = http.post("/api/agents/watcher", json={"model_name": WEIGHTS, "door": "runner"})
    assert r.status_code == 200 and r.json()["phase"] == "station"
    con.handle_line("state")
    text = out.getvalue()
    assert f"The watcher ({WEIGHTS}, through the local runner): stationed; its turn is open." in (
        text
    )
    assert "The clock waits for the watcher (--lockstep)." in text
    con.handle_line("tick 60")
    assert con.world.clock.tick == 0 and "the clock waits for the watcher" in out.getvalue()
    http.post("/api/agents/watcher/reply", json={"text": "Aye.", "since": r.json()["next"]})
    con.handle_line("tick 60")
    assert con.world.clock.tick == 60
    assert "[watcher] Aye." in out.getvalue()  # the log prints as the console always has
    assert isinstance(con.world.agents["watcher"].model, RemoteModel)


def test_a_station_the_game_mans_itself_is_refused_and_a_loaded_games_is_taken_over(tmp_path):
    """The scripted watcher (`--watcher fake`) mans the station: a door is refused. A
    game loaded from a save with a model's station not released: the same model takes
    it over (the consent gate first), with the brief sent again as it stands; another
    model is refused."""
    from freesail.ui.console import station_watcher

    world = frigate_world()
    station_watcher(world, "fake")
    g = Game(tmp_path / "a", world=world)
    r = g.station()
    assert r.status_code == 409 and "scripted watcher" in r.json()["detail"]
    # a game with a model at the station, saved with its turn open, and loaded again
    first = Game(tmp_path / "b")
    yes_on_record(first.records)
    first.took(first.station())
    first.reply("Aye.")
    first.driver.tick(A_GLASS_S)  # the next turn is open when the game is saved
    data = json.loads(json.dumps(first.world.save()))
    loaded = replay.replay(data, ship_factory)
    assert loaded.agents["watcher"].model_name == WEIGHTS
    g = Game(tmp_path / "b", world=loaded)
    assert g.station(model_name="someone-else").status_code == 409
    a = g.took(g.station())
    assert a["phase"] == "station" and a["floor"] == "model"
    assert roles(a) == ["operator", "data"] and reasons(a) == ["the glass"]
    assert a["turns"][0]["content"].startswith("This is a message from the harness")
    g.reply("Still here.")
    assert "[watcher] Still here." in g.lines("agent.note")
    assert isinstance(g.harness.model, RemoteModel)
