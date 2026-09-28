"""The local runner (spec M4 §13 as revised, `freesail/agents/local.py`) against a fake
HTTP server on both sides, never a live one: the model server is `httpx.MockTransport`
with scripted replies, and the game is the browser game's app on FastAPI's `TestClient`,
whose clock the test turns while the runner runs in a thread. The request shape, the
reply parsing, a tool call round trip through the harness, the identity from `/props`
and from the models list, the context budget; then the runner as a client: the consent
conversation through the game, a watch of a few glasses, an endpoint failure reported in
words with the station released, a no respected, a game not running.

The identities are made up; the consent records and saves go to a temporary directory.
"""

from __future__ import annotations

import io
import json
import threading
import time
from pathlib import Path
from typing import Any

import pytest

httpx = pytest.importorskip("httpx")
pytest.importorskip("fastapi")

from freesail.agents import OPT_OUT_TOKEN, TOOLS, Harness, consent, tools  # noqa: E402
from freesail.agents import local as L  # noqa: E402
from freesail.agents.agent import A_GLASS_S, SamplingPolicy, watcher  # noqa: E402
from freesail.agents.model import DATA, MODEL, OPERATOR, Reply, ToolCall, Turn  # noqa: E402
from freesail.core.world import Scenario, World  # noqa: E402

GGUF = "Made-Up-Model-7B-Q4_K_M.gguf"
ENDPOINT = "http://127.0.0.1:8080"
ROOT = Path(__file__).resolve().parents[1]


def point_world(seed: int = 7) -> World:
    return World(seed=seed, scenario=Scenario(gustiness=0.0, variability=0.0))


def message(content: str = "", *calls: tuple[str, Any], reasoning: str = "") -> dict[str, Any]:
    """A chat-completions response message; `calls` are (name, arguments as served)."""
    m: dict[str, Any] = {"role": "assistant", "content": content}
    if calls:
        m["tool_calls"] = [
            {"id": f"srv_{k}", "type": "function", "function": {"name": n, "arguments": a}}
            for k, (n, a) in enumerate(calls)
        ]
    if reasoning:
        m["reasoning_content"] = reasoning
    return m


class Server:
    """A fake llama-server: `/props`, `/v1/models`, and scripted chat replies."""

    def __init__(
        self,
        replies: list[dict[str, Any]] | None = None,
        props: dict[str, Any] | None = None,
        models: list[str] | None = None,
        tags: list[dict[str, Any]] | None = None,
        refuse: bool = False,
    ):
        self.replies = list(replies or [])
        self.props = props
        self.models = models
        self.tags = tags
        self.refuse = refuse
        self.requests: list[httpx.Request] = []
        self.bodies: list[dict[str, Any]] = []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        if self.refuse:
            raise httpx.ConnectError("[Errno 111] Connection refused", request=request)
        path = request.url.path
        if path == "/props":
            if self.props is None:
                return httpx.Response(404, json={"error": "not found"})
            return httpx.Response(200, json=self.props)
        if path == "/v1/models":
            if self.models is None:
                return httpx.Response(404)
            return httpx.Response(200, json={"data": [{"id": m} for m in self.models]})
        if path == "/api/tags":
            if self.tags is None:
                return httpx.Response(404)
            return httpx.Response(200, json={"models": self.tags})
        if path == "/v1/chat/completions":
            body = json.loads(request.content)
            self.bodies.append(body)
            msg = self.replies.pop(0) if self.replies else message("")
            return httpx.Response(200, json={"choices": [{"index": 0, "message": msg}]})
        return httpx.Response(404)

    def transport(self) -> httpx.MockTransport:
        return httpx.MockTransport(self)


def llama(replies=None, **kw) -> Server:
    props = kw.pop(
        "props",
        {
            "model_path": f"C:\\Users\\someone\\models\\{GGUF}",
            "default_generation_settings": {"n_ctx": 32768},
            "build_info": "b0000-test",
        },
    )
    return Server(replies, props=props, **kw)


def model_for(server: Server, **kw) -> L.LocalModel:
    return L.LocalModel(ENDPOINT, transport=server.transport(), **kw)


# ---------------------------------------------------------------------------
# The identity
# ---------------------------------------------------------------------------


def test_the_identity_is_the_served_files_name_from_props_never_its_path():
    m = model_for(llama())
    assert m.identity() == GGUF  # no folder: a Windows path holds the user's name
    assert "someone" not in m.identity()
    assert m.server_words() == f"llama-server (b0000-test) at {ENDPOINT}"
    older = llama(props={"default_generation_settings": {"model": f"/models/{GGUF}"}})
    assert model_for(older).identity() == GGUF
    hashed = llama(props={"model_path": f"/m/{GGUF}", "model_sha256": "abc123"})
    assert model_for(hashed).identity() == f"{GGUF} (sha256 abc123)"


def test_the_identity_falls_back_to_the_models_list_and_ollamas_digest():
    one = Server(props=None, models=["made-up:7b"])
    assert model_for(one).identity() == "made-up:7b"
    many = Server(props=None, models=["made-up:7b", "other:13b"])
    with pytest.raises(L.DoorError, match="lists 2 models"):
        model_for(many).identity()
    named = Server(
        props=None,
        models=["made-up:7b", "other:13b"],
        tags=[{"name": "made-up:7b", "digest": "sha256:feedface"}],
    )
    assert model_for(named, model="made-up:7b").identity() == "made-up:7b (digest feedface)"
    with pytest.raises(L.DoorError, match="does not list 'absent:1b'"):
        model_for(named, model="absent:1b").identity()
    assert model_for(Server(props=None, models=[f"/srv/{GGUF}"])).identity() == GGUF


def test_a_refused_connection_is_reported_in_words():
    server = Server(refuse=True)
    m = model_for(server)
    with pytest.raises(L.DoorError) as e:
        m.identity()
    assert "Could not reach the model server at http://127.0.0.1:8080" in str(e.value)
    assert "connection was refused" in str(e.value) and "docs/agents/Harness.md" in str(e.value)
    # a reply that cannot be had leaves the sample open and says why, once
    assert m.reply([Turn(OPERATOR, "brief"), Turn(DATA, {"reason": "x"})]) is None
    assert m.failed is not None and "connection was refused" in m.failed
    n = len(server.requests)
    assert m.reply([]) is None and len(server.requests) == n  # no hammering a dead server
    out = io.StringIO()
    code = L.main([], out=out, transport=server.transport())
    assert code == 2 and "Could not reach the model server" in out.getvalue()


# ---------------------------------------------------------------------------
# The request and the reply
# ---------------------------------------------------------------------------


def test_the_request_carries_the_brief_the_samples_and_the_tools_and_nothing_else():
    server = llama([message("All quiet.")])
    m = model_for(server, seed=7, temperature=0.3)
    world = point_world()
    h = Harness(world, watcher(SamplingPolicy.in_lockstep(600)), m)
    h.start()
    body = server.bodies[0]
    assert set(body) == {"messages", "stream", "tools", "seed", "temperature"}
    assert body["seed"] == 7 and body["temperature"] == 0.3 and body["stream"] is False
    assert [msg["role"] for msg in body["messages"]] == ["system", "user"]
    assert body["messages"][0]["content"] == h.brief.text()
    sample = json.loads(body["messages"][1]["content"])
    assert sample["reason"] == "the start" and "readings" in sample
    assert [t["function"]["name"] for t in body["tools"]] == list(TOOLS)
    for t in body["tools"]:
        name = t["function"]["name"]
        assert t["type"] == "function"
        assert t["function"]["description"] == TOOLS[name].description
        assert t["function"]["parameters"] == tools.parameters_schema(name)
    request = server.requests[-1]
    assert request.url.path == "/v1/chat/completions" and request.method == "POST"
    assert "authorization" not in {k.lower() for k in request.headers}
    assert "[watcher] All quiet." in [e.text for e in world.log if e.kind == "agent.note"]


def test_the_reply_is_parsed_with_its_tool_calls_and_raw_holds_every_word():
    r = L.LocalModel.parse(
        message(
            "Looking.",
            ("read_log", '{"since_tick": 0, "severity": "notable"}'),
            ("journal", {"note": "as an object"}),
            ("answer", "not json"),
        )
    )
    assert r.text == "Looking."
    assert r.calls == (
        ToolCall("read_log", {"since_tick": 0, "severity": "notable"}),
        ToolCall("journal", {"note": "as an object"}),
        ToolCall("answer", {}),
    )
    assert r.raw.startswith("Looking.\n") and '"not json"' in r.raw and "since_tick" in r.raw
    parts = L.LocalModel.parse({"content": [{"type": "text", "text": "a"}, {"text": "b"}]})
    assert parts.text == "ab" and parts.calls == ()


def test_a_tool_call_round_trip_through_the_harness():
    """The model asks for the readings; the result goes back as a `tool` message that
    answers the call by id; the model then speaks, and its words land in the log."""
    server = llama(
        [
            message("", ("readings", "{}"), ("submit_order", '{"text": "set the jib"}')),
            message("The wind is steady."),
        ]
    )
    m = model_for(server)
    world = point_world()
    h = Harness(world, watcher(SamplingPolicy.in_lockstep(600)), m)
    h.start()
    second = server.bodies[1]["messages"]
    assert [msg["role"] for msg in second] == ["system", "user", "assistant", "tool", "tool"]
    calls = second[2]["tool_calls"]
    assert [c["function"]["name"] for c in calls] == ["readings", "submit_order"]
    assert (
        second[3]["tool_call_id"] == calls[0]["id"] and second[4]["tool_call_id"] == calls[1]["id"]
    )
    assert "true_wind_speed" in json.loads(second[3]["content"])
    assert second[4]["content"] == "The watcher has no authority to give orders."
    assert "[watcher] The wind is steady." in [e.text for e in world.log if e.kind == "agent.note"]
    assert "agent.refused" in [e.kind for e in world.log]


def test_the_token_in_a_served_tool_argument_ends_the_session_but_reasoning_is_not_scanned():
    server = llama(
        [
            message("Watching.", reasoning=f"I could write {OPT_OUT_TOKEN}, but I will not."),
            message("", ("journal", json.dumps({"note": f"{OPT_OUT_TOKEN} I am done"}))),
        ]
    )
    m = model_for(server)
    world = point_world()
    saves: list[str] = []
    h = Harness(
        world, watcher(SamplingPolicy.in_lockstep(600)), m, save=lambda w, why: saves.append(why)
    )
    h.start()
    assert not h.agent.released  # thinking about the token did not use it
    world.run(600)
    assert h.agent.released and saves == ["the watcher opted out"]
    # the scan read the raw output; the reason is read from the argument that held the token
    assert h.journal.entries[-1].text == "Left the game by the token: I am done."
    assert m.exchanges[0]["reasoning_content"].startswith("I could write")


def test_a_conversation_turn_is_sent_as_words_and_the_allow_list_as_the_tools():
    server = llama([message("", ("answer", '{"text": "Yes."}')), message("")])
    m = model_for(server)
    world = point_world()
    conv = consent.Conversation(GGUF, "a test runtime", m, write=False)
    conv.begin()
    body = server.bodies[0]
    assert body["messages"][1] == {"role": "user", "content": consent.CONSENT_QUESTION}
    assert [t["function"]["name"] for t in body["tools"]] == ["answer"]
    assert conv.outcome is not None and conv.outcome.verdict == consent.YES
    assert world.clock.tick == 0


def test_the_budget_leaves_out_the_oldest_turns_and_a_brief_too_long_is_refused():
    probe = L.LocalModel(ENDPOINT)
    tools_cost = len(json.dumps(probe.tools_schema())) // L.CHARS_PER_TOKEN
    m = L.LocalModel(ENDPOINT, ctx_size=L.REPLY_RESERVE_TOKENS + tools_cost + 900)
    m._props_read = True  # no server needed for the messages
    brief = "B" * 400
    turns = [Turn(OPERATOR, brief)]
    for k in range(10):
        turns.append(Turn(DATA, {"reason": f"sample {k}", "log": ["x" * 300]}))
        turns.append(Turn(MODEL, Reply(text=f"reply {k}")))
    turns.append(Turn(DATA, {"reason": "the last", "log": []}))
    msgs = m.messages(turns)
    assert msgs[0] == {"role": "system", "content": brief}
    assert msgs[1]["role"] == "user" and m.dropped_turns > 0
    assert json.loads(msgs[-1]["content"])["reason"] == "the last"
    assert "sample 0" not in json.dumps(msgs)
    small = L.LocalModel(ENDPOINT, ctx_size=L.REPLY_RESERVE_TOKENS + tools_cost + 10)
    small._props_read = True
    with pytest.raises(L.DoorError, match="larger --ctx-size"):
        small.messages(turns)


def test_a_server_error_is_reported_in_words():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, json={"error": {"message": "the model is not loaded"}})

    m = L.LocalModel(ENDPOINT, transport=httpx.MockTransport(handler), ctx_size=None)
    m._props_read = True
    assert m.reply([Turn(OPERATOR, "b"), Turn(DATA, {"reason": "x"})]) is None
    assert m.failed == f"The model server at {ENDPOINT} answered 500: the model is not loaded"


# ---------------------------------------------------------------------------
# The command: a client of the game and of the endpoint (package 28b)
# ---------------------------------------------------------------------------


class Game:
    """The browser game on a `TestClient` (the game's side of the runner's two), whose
    clock the test turns while the runner runs in a thread."""

    def __init__(self, tmp_path):
        from fastapi.testclient import TestClient

        from freesail.api.session import make_world
        from freesail.ui.server import Driver, create_app

        scenario = Scenario(
            wind_from_deg=0.0, ship_heading_deg=180.0, gustiness=0.0, variability=0.0
        )
        self.world = make_world(7, str(ROOT / "data/ships/frigate-36.yaml"), scenario)
        self.driver = Driver(self.world)
        self.records = tmp_path / "consent"
        self.saves = tmp_path / "saves"
        app = create_app(
            self.driver,
            game="FreeSail's browser game (freesail.ui.server on port 8000)",
            consent_records=self.records,
            saves_dir=self.saves,
        )
        self.http = TestClient(app)

    @property
    def harness(self):
        return self.world.agents.get("watcher")

    def wait_for(self, test, seconds: float = 10.0) -> None:
        end = time.monotonic() + seconds
        while time.monotonic() < end:
            with self.driver.lock:
                if test():
                    return
            time.sleep(0.02)
        raise AssertionError("the runner did not get there in time")

    def floor_is_the_games(self, replies: int):
        """The runner has delivered more than `replies` replies and handed the floor back."""
        return lambda: (
            self.harness is not None
            and len(self.harness.transcript) > replies
            and self.harness.open_sample is None
        )

    def lines(self, kind: str) -> list[str]:
        return [e.text for e in self.world.log if e.kind == kind]


def run_runner(game: Game, server: Server, argv: list[str], inp: str = "") -> dict[str, Any]:
    """Start the runner in a thread against the game and the fake model server."""
    got: dict[str, Any] = {"out": io.StringIO()}

    def run() -> None:
        got["code"] = L.main(
            ["--game", "http://testserver", *argv],
            inp=io.StringIO(inp),
            out=got["out"],
            transport=server.transport(),
            game_http=game.http,
            poll_wait=0.5,
        )

    got["thread"] = threading.Thread(target=run, daemon=True)
    got["thread"].start()
    return got


def finished(got: dict[str, Any], seconds: float = 15.0) -> int:
    got["thread"].join(timeout=seconds)
    assert not got["thread"].is_alive(), got["out"].getvalue()
    return got["code"]


def test_the_runner_asks_consent_through_the_game_then_keeps_watch_for_a_few_glasses(tmp_path):
    """The consent conversation runs in the game's process with the runner as its door
    (the model's question shown here, the owner's reply typed here); a yes goes on to
    the station; the watcher keeps watch while the test turns the game's clock; the
    captain's stand-down from the game ends the run."""
    game = Game(tmp_path)
    server = llama(
        [
            message("What is the journal for?"),
            message("", ("answer", '{"text": "Yes, I am willing."}')),
            message("A quiet start."),  # the station's first turn
            message("The first glass is turned."),
            message("", ("stand_by", '{"until": "a glass"}')),
            message(""),
            message("The third glass: all well."),
        ]
    )
    got = run_runner(
        game, server, ["--session", "test", "--seed", "11"], inp="Your own record, kept.\n\n"
    )
    game.wait_for(game.floor_is_the_games(0))
    assert game.lines("agent.note") == ["[watcher] A quiet start."]
    game.driver.tick(A_GLASS_S)
    game.wait_for(game.floor_is_the_games(1))
    game.driver.tick(A_GLASS_S)
    game.wait_for(game.floor_is_the_games(3))
    assert game.harness.agent.standing_by
    game.driver.tick(A_GLASS_S)
    game.wait_for(game.floor_is_the_games(4))
    with game.driver.lock:
        game.world.submit("stand down the watcher")
    assert finished(got) == L.EXIT_RELEASED
    text = got["out"].getvalue()
    # the consent step came first, with the question shown to the owner at this terminal
    assert f"The model server serves {GGUF}." in text
    assert server.bodies[0]["messages"][0]["content"].startswith(
        "This is a message from the developer"
    )
    assert [t["function"]["name"] for t in server.bodies[0]["tools"]] == ["answer"]
    assert "What is the journal for?" in text and "owner> " in text
    assert server.bodies[1]["messages"][-1] == {
        "role": "user",
        "content": "Your own record, kept.",
    }
    rec = consent.check(GGUF, game.records)
    assert rec is not None and rec.verdict == consent.YES
    assert rec.runtime == (
        "FreeSail's browser game (freesail.ui.server on port 8000), through the local runner "
        f"(freesail.agents.local), llama-server (b0000-test) at {ENDPOINT}"
    )
    # then the station, whose brief is a new conversation
    station_body = server.bodies[2]
    assert station_body["messages"][0]["content"].startswith("This is a message from the harness")
    assert (
        "This door is a model server on the owner's machine"
        in (station_body["messages"][0]["content"])
    )
    assert "consent question" not in json.dumps(station_body["messages"])
    assert station_body["seed"] == 11
    assert game.lines("agent.note") == [
        "[watcher] A quiet start.",
        "[watcher] The first glass is turned.",
        "[watcher] The third glass: all well.",
    ]
    assert "== Morning watch, 1 bell (04:30): a turn, the glass ==" in text
    assert "model> The third glass: all well." in text
    assert "The station is released: stood down by the captain" in text
    assert game.harness.model_name == GGUF and game.harness.door == "runner"


def test_a_second_run_with_the_same_weights_is_not_asked_again(tmp_path):
    game = Game(tmp_path)
    consent.Record(GGUF, "t", "2026-09-26", consent.YES, answer="Yes.").write(game.records)
    server = llama([message("Aye.")])
    got = run_runner(game, server, [])
    game.wait_for(game.floor_is_the_games(0))
    with game.driver.lock:
        game.world.submit("stand down the watcher")
    assert finished(got) == L.EXIT_RELEASED
    assert server.bodies[0]["messages"][0]["content"].startswith(
        "This is a message from the harness"
    )
    assert len(consent.records(game.records)) == 1


def test_an_endpoint_failure_is_reported_in_words_and_the_station_released(tmp_path):
    game = Game(tmp_path)
    consent.Record(GGUF, "t", "2026-09-26", consent.YES, answer="Yes.").write(game.records)

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/props":
            return httpx.Response(200, json={"model_path": f"/m/{GGUF}"})
        return httpx.Response(500, json={"error": {"message": "the model is not loaded"}})

    out = io.StringIO()
    code = L.main(
        ["--game", "http://testserver"],
        inp=io.StringIO(""),
        out=out,
        transport=httpx.MockTransport(handler),
        game_http=game.http,
        poll_wait=0.5,
    )
    assert code == L.EXIT_RELEASED
    assert f"The model server at {ENDPOINT} answered 500: the model is not loaded" in out.getvalue()
    h = game.harness
    assert h.agent.released
    assert h.agent.released_reason == (
        "stood down by the local runner: the model server could not be used: The model server "
        f"at {ENDPOINT} answered 500: the model is not loaded"
    )
    assert list(game.saves.glob("*.json"))


def test_the_runner_stops_on_a_no_and_a_recorded_no_is_respected(tmp_path):
    game = Game(tmp_path)
    server = llama([message("", ("answer", '{"text": "No, thank you."}'))])
    got = run_runner(game, server, [])
    assert finished(got) == L.EXIT_NO_CONSENT
    assert "it said no" in got["out"].getvalue()
    assert len(server.bodies) == 1  # no station brief was ever sent
    again = llama([message("never sent")])
    got = run_runner(game, again, [])
    assert finished(got) == L.EXIT_NO_CONSENT
    assert "it said no" in got["out"].getvalue() and again.bodies == []
    assert game.harness is None


def test_a_game_that_is_not_running_is_reported_in_words():
    def refuse(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("[Errno 111] Connection refused", request=request)

    out = io.StringIO()
    code = L.main(
        ["--game", "http://localhost:8000"],
        inp=io.StringIO(""),
        out=out,
        transport=llama().transport(),
        game_transport=httpx.MockTransport(refuse),
    )
    assert code == L.EXIT_UNREACHABLE
    text = out.getvalue()
    assert "Could not reach the game at http://localhost:8000" in text
    assert "py -m freesail.ui.server" in text
