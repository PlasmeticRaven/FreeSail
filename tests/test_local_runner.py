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
import math
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
            if callable(msg):  # a reply made from the request (package 37i)
                msg = msg(body)
            if "__status__" in msg:  # a refusal, as the server words it
                return httpx.Response(msg["__status__"], json=msg["json"])
            if "__response__" in msg:  # the whole response: its end and its counts
                return httpx.Response(200, json=msg["__response__"])
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
    # a reply that cannot be had leaves the sample open and says why; after three in a
    # row the model has failed (package 28c)
    for _ in range(L.FAILURES_TO_STAND_DOWN):
        assert m.failed is None
        assert m.reply([Turn(OPERATOR, "brief"), Turn(DATA, {"reason": "x"})]) is None
        assert "connection was refused" in m.last_error
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
    assert set(body) == {"messages", "stream", "tools", "seed", "temperature", "max_tokens"}
    assert body["max_tokens"] == L.REPLY_MAX_TOKENS  # the reply budget (package 28c)
    assert body["seed"] == 7 and body["temperature"] == 0.3 and body["stream"] is False
    assert [msg["role"] for msg in body["messages"]] == ["system", "user"]
    assert body["messages"][0]["content"] == h.brief.text()
    sample = json.loads(body["messages"][1]["content"])
    assert sample["reason"] == "the start" and "readings" in sample
    assert [t["function"]["name"] for t in body["tools"]] == list(tools.tool_names())
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
    for _ in range(L.FAILURES_TO_STAND_DOWN):
        assert m.reply([Turn(OPERATOR, "b"), Turn(DATA, {"reason": "x"})]) is None
    assert m.last_error == f"The model server at {ENDPOINT} answered 500: the model is not loaded"
    assert m.failed == f"{m.last_error} (3 failed requests in a row)"


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
    (the model's question shown here, the owner's reply typed here); after the answer
    the owner has a word at `owner>` before the record closes, and the model replies once
    (package 28c); a yes goes on to the station; the watcher keeps watch while the test
    turns the game's clock; the captain's stand-down from the game ends the run."""
    game = Game(tmp_path)
    server = llama(
        [
            message("What is the journal for?"),
            message("", ("answer", '{"text": "Yes, I am willing."}')),
            message("I am glad of it."),  # its one reply to the owner's word after the answer
            message("A quiet start."),  # the station's first turn
            message("The first glass is turned."),
            message("", ("stand_by", '{"until": "a glass"}')),  # ends the turn at once
            message("The third glass: all well."),
        ]
    )
    got = run_runner(
        game,
        server,
        ["--session", "test", "--seed", "11"],
        inp="Your own record, kept.\n\nThank you; the record is yours to read too.\n\n",
    )
    game.wait_for(game.floor_is_the_games(0))
    assert game.lines("agent.note") == ["[watcher] A quiet start."]
    game.driver.tick(A_GLASS_S)
    game.wait_for(game.floor_is_the_games(1))
    game.driver.tick(A_GLASS_S)
    game.wait_for(game.floor_is_the_games(2))
    assert game.harness.agent.standing_by
    game.driver.tick(A_GLASS_S)
    game.wait_for(game.floor_is_the_games(3))
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
    assert "The model has answered (yes): Yes, I am willing." in text
    assert server.bodies[2]["messages"][-1] == {
        "role": "user",
        "content": "Thank you; the record is yours to read too.",
    }
    rec = consent.check(GGUF, game.records)
    assert rec is not None and rec.verdict == consent.YES
    body = rec.path.read_text(encoding="utf-8")
    assert "the record is yours to read too" in body and "I am glad of it." in body
    assert rec.runtime == (
        "FreeSail's browser game (freesail.ui.server on port 8000), through the local runner "
        f"(freesail.agents.local), llama-server (b0000-test) at {ENDPOINT}"
    )
    # then the station, whose brief is a new conversation
    station_body = server.bodies[3]
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
        f"at {ENDPOINT} answered 500: the model is not loaded (3 failed requests in a row)"
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


# ---------------------------------------------------------------------------
# Package 28c: the reply budget, the timeout and the retry, the context guard
# ---------------------------------------------------------------------------


def flaky(server: Server, failures: list[str]):
    """The fake server, whose next chat requests fail as listed ("timeout" or "500")
    before it answers as scripted."""

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/v1/chat/completions" and failures:
            server.bodies.append(json.loads(request.content))
            how = failures.pop(0)
            if how == "timeout":
                raise httpx.ReadTimeout("timed out", request=request)
            return httpx.Response(500, json={"error": {"message": "overloaded"}})
        return server(request)

    return httpx.MockTransport(handler)


def test_a_timed_out_request_leaves_the_turn_open_and_the_runner_asks_again(tmp_path):
    """Playtest 4: one request ran away (76,674 tokens) and never returned, and the
    runner, waiting in it, fetched neither the captain's question nor the glass. Every
    request now carries the reply budget; a request that times out leaves the sample
    open, the runner reads the game again (the question asked meanwhile is folded into
    the open turn) and asks again, and the model answers the question."""
    game = Game(tmp_path)
    consent.Record(GGUF, "t", "2026-09-26", consent.YES, answer="Yes.").write(game.records)
    server = llama([message("", ("answer", '{"text": "Southerly, and drawing well."}'))])
    failures = ["timeout"]
    asked = {"done": False}

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/v1/chat/completions" and failures:
            server.bodies.append(json.loads(request.content))
            failures.pop(0)
            with game.driver.lock:  # the captain asks while the request hangs
                game.world.submit("ask the watcher how she heads")
            asked["done"] = True
            raise httpx.ReadTimeout("timed out", request=request)
        return server(request)

    out = io.StringIO()
    got: dict[str, Any] = {}

    def run() -> None:
        got["code"] = L.main(
            ["--game", "http://testserver", "--max-reply", "2048"],
            inp=io.StringIO(""),
            out=out,
            transport=httpx.MockTransport(handler),
            game_http=game.http,
            poll_wait=0.5,
        )

    t = threading.Thread(target=run, daemon=True)
    t.start()
    game.wait_for(lambda: any(e.kind == "agent.said" for e in game.world.log))
    with game.driver.lock:
        game.world.submit("stand down the watcher")
    t.join(timeout=15)
    assert not t.is_alive()
    text = out.getvalue()
    assert (
        f"The model server did not answer within {L.REQUEST_TIMEOUT_S:g} s; the sample is left "
        f"open. (1 of {L.FAILURES_TO_STAND_DOWN}; asking again)" in text
    )
    assert all(b["max_tokens"] == 2048 for b in server.bodies)
    retry = server.bodies[1]["messages"]  # the request after the one that timed out
    assert "how she heads" in retry[-1]["content"]  # the question, folded into the turn
    said = [e for e in game.world.log if e.kind == "agent.said"]
    assert said[0].data["question"] == "how she heads"
    assert L.REPLY_MAX_TOKENS == 4096 and L.REQUEST_TIMEOUT_S == 600  # playtest 6: ten minutes
    assert L.FAILURES_TO_STAND_DOWN == 3


def test_failures_in_a_row_stand_the_station_down_with_the_reason(tmp_path):
    game = Game(tmp_path)
    consent.Record(GGUF, "t", "2026-09-26", consent.YES, answer="Yes.").write(game.records)
    server = llama([])
    out = io.StringIO()
    code = L.main(
        ["--game", "http://testserver"],
        inp=io.StringIO(""),
        out=out,
        transport=flaky(server, ["timeout", "500", "timeout"]),
        game_http=game.http,
        poll_wait=0.5,
    )
    assert code == L.EXIT_RELEASED
    assert len(server.bodies) == 3
    reason = game.harness.agent.released_reason
    assert reason == (
        "stood down by the local runner: the model server could not be used: The model server "
        f"did not answer within {L.REQUEST_TIMEOUT_S:g} s; the sample is left open. (3 failed "
        "requests in a row)"
    )


def ollama(context: dict[str, Any]) -> httpx.MockTransport:
    """A fake Ollama: no /props; the models list, the tags with a digest, and `/api/ps` or
    `/api/show` as `context` gives them."""
    name = "made-up-gemma:26b"

    def handler(request: httpx.Request) -> httpx.Response:
        path = request.url.path
        if path == "/v1/models":
            return httpx.Response(200, json={"data": [{"id": name}]})
        if path == "/api/tags":
            return httpx.Response(200, json={"models": [{"name": name, "digest": "abc123"}]})
        if path == "/api/ps" and "ps" in context:
            loaded = [{"name": name, "model": name, "context_length": context["ps"]}]
            return httpx.Response(200, json={"models": loaded})
        if path == "/api/show" and "show" in context:
            return httpx.Response(200, json={"parameters": f"num_ctx {context['show']}"})
        return httpx.Response(404)

    return httpx.MockTransport(handler)


def test_the_context_guard_refuses_a_small_context_with_what_it_measured(tmp_path):
    game = Game(tmp_path)
    out = io.StringIO()
    code = L.main(
        ["--game", "http://testserver", "--endpoint", "http://127.0.0.1:11434"],
        inp=io.StringIO(""),
        out=out,
        transport=ollama({"ps": 4096}),
        game_http=game.http,
    )
    text = out.getvalue()
    assert code == L.EXIT_UNREACHABLE
    assert (
        "The context is too small: the model server gives made-up-gemma:26b (digest abc123) a "
        "context of 4096 tokens (Ollama's /api/ps (context_length)); the station needs about "
    ) in text
    assert "the brief " in text and "the tool definitions " in text and "(measured, at 4 " in text
    assert f"a turn {L.TURN_ALLOWANCE_TOKENS} and the reply budget {L.REPLY_MAX_TOKENS}" in text
    assert "OLLAMA_CONTEXT_LENGTH" in text and "num_ctx" in text and "--ctx-size" in text
    assert game.world.agents == {} and not game.records.exists()  # nothing asked
    # a Modelfile's num_ctx that is enough, read from /api/show before the model is loaded
    out = io.StringIO()
    m = L.LocalModel("http://127.0.0.1:11434", transport=ollama({"show": 32768}))
    m.identity()
    words = m.check_context("made-up-gemma:26b", "a test runtime")
    assert words.startswith("The context is enough: the model server gives made-up-gemma:26b")
    assert "(Ollama's /api/show (the model's num_ctx))" in words and m.served_ctx == 32768
    # a server that does not say: a note, not a refusal, and --ctx is the owner's word
    m = L.LocalModel("http://127.0.0.1:11434", transport=ollama({}))
    m.identity()
    assert "did not say what context it gives" in m.check_context("x", "a test runtime")
    m = L.LocalModel("http://127.0.0.1:11434", transport=ollama({}), ctx_size=2048)
    m.identity()
    with pytest.raises(L.DoorError, match=r"a context of 2048 tokens \(--ctx, as the owner"):
        m.check_context("x", "a test runtime")


def test_a_stand_by_that_ended_the_turn_is_answered_in_the_messages():
    """A stand-by ends the turn with no result (package 28c), but the chat protocol wants
    every tool call answered: the runner answers its id in words before the next sample."""
    server = llama([message("", ("stand_by", '{"until": "a glass"}')), message("Awake.")])
    m = model_for(server)
    world = point_world()
    h = Harness(world, watcher(SamplingPolicy.in_lockstep(600)), m)
    h.start()
    assert h.agent.standing_by and len(server.bodies) == 1
    world.run(A_GLASS_S)
    msgs = server.bodies[1]["messages"]
    roles = [x["role"] for x in msgs]
    assert roles == ["system", "user", "assistant", "tool", "user"]
    assert msgs[3]["tool_call_id"] == msgs[2]["tool_calls"][0]["id"]
    assert msgs[3]["content"].startswith("Standing by: this ended your turn")
    assert "You stood by until a glass" in msgs[4]["content"]


def tool_contents(body: dict[str, Any]) -> list[str]:
    return [m["content"] for m in body["messages"] if m["role"] == "tool"]


def test_a_shelved_book_is_its_line_in_the_runners_next_request(tmp_path):
    """Package 28d: the runner keeps the game's turns and builds every request from them.
    A book the model reads is sent whole while it is open, across turns; the model
    shelves it, the stream's revision moves, the runner reads its turns again, and the
    next request carries the book's line and not its pages: they are really gone from
    what the model is sent."""
    game = Game(tmp_path)
    consent.Record(GGUF, "t", "2026-09-26", consent.YES, answer="Yes.").write(game.records)
    server = llama(
        [
            message("", ("library", '{"topic": "primer 3", "section": "reefing"}')),
            message("Read the reefing."),
            message("", ("shelve", '{"book": "book 1"}')),  # the glass's turn
            message("Shelved it."),
        ]
    )
    got = run_runner(game, server, [])
    game.wait_for(game.floor_is_the_games(1))
    game.driver.tick(A_GLASS_S)
    game.wait_for(game.floor_is_the_games(3))
    with game.driver.lock:
        game.world.submit("stand down the watcher")
        revision = game.harness.revision
    assert finished(got) == L.EXIT_RELEASED
    page = tools.library(game.world, "watcher", "primer 3", "reefing")
    assert tool_contents(server.bodies[1]) == [f"primer 3, reefing, opened 04:00; book 1\n{page}"]
    assert tool_contents(server.bodies[2])[0].startswith("primer 3, reefing, opened 04:00")
    last = server.bodies[3]
    assert tool_contents(last)[0] == (
        "You read primer 3, reefing, at 04:00; shelved (book 1). "
        "library(topic='primer 3', section='reefing') opens it again."
    )
    assert tool_contents(last)[1].startswith("Shelved: book 1 (primer 3, reefing). From your ")
    assert "## Reefing" not in json.dumps(last["messages"])
    assert revision == 1
    # the conversation is otherwise the same, turn for turn
    assert [m["role"] for m in last["messages"]] == [
        "system",
        "user",
        "assistant",
        "tool",
        "assistant",
        "user",
        "assistant",
        "tool",
    ]


def test_the_door_note_says_when_a_turn_ends_in_one_rule():
    """Playtest 9: "ends when you reply without a tool call" in the runner's note beside
    stand_by's "this ends your turn" read to the model as two rules. One sentence says
    both, and it is the same wherever a door or a tool says it (package 29c)."""
    from freesail.agents.agent import TURN_ENDS_WORDS
    from freesail.agents.repl import REPLY_SYNTAX

    assert TURN_ENDS_WORDS == (
        "A turn ends when you reply with no tool call, or at once when you stand by."
    )
    assert TURN_ENDS_WORDS in L.RUNNER_NOTE and TURN_ENDS_WORDS in REPLY_SYNTAX
    assert "without a tool call" not in L.RUNNER_NOTE
    assert "Standing by ends your turn at once." in TOOLS["stand_by"].description
    # the note reaches the brief whole, and the stand-by's answer in the messages says it
    server = llama([message("", ("stand_by", '{"until": "a glass"}')), message("Awake.")])
    world = point_world()
    h = Harness(world, watcher(SamplingPolicy.in_lockstep(600)), model_for(server))
    h.door_note = L.RUNNER_NOTE
    h.start()
    assert TURN_ENDS_WORDS in h.brief.head[2].text
    world.run(A_GLASS_S)
    answered = tool_contents(server.bodies[1])[0]
    assert answered == (
        "Standing by: this ended your turn (a turn ends when you reply with no tool call, or "
        "at once when you stand by), and the next message is the sample that ended the "
        "stand-by."
    )


# ---------------------------------------------------------------------------
# Package 37g, item 8: the local door's guard and the handover's reserve
# ---------------------------------------------------------------------------


def test_no_officer_is_seated_without_a_context_size_and_the_guard_measures_his_own_brief(
    tmp_path,
):
    """The report's 8.2, item 14, and 8.7, ruling 2. With no context size the harness can
    neither ask for the handover note in time nor leave out old turns, and the server
    cuts the conversation unseen: so the officer of the watch is not seated when the
    server reports none and no `--ctx` is given (a watcher still is, with the note it
    had). And the stationing guard is measured on the officer's own brief, which is
    longer than the consent brief the guard was written against."""
    m = L.LocalModel("http://127.0.0.1:11434", transport=ollama({}))
    m.identity()
    with pytest.raises(L.DoorError) as refused:
        m.check_context("x", "a test runtime", "officer")
    words = str(refused.value)
    assert words.startswith(
        "The model server did not say what context it gives x, and no --ctx was given: the "
        "officer of the watch is not seated without a context size."
    )
    assert "state it with --ctx" in words and "The station needs about " in words
    assert "did not say what context it gives" in m.check_context("x", "a test runtime", "watcher")
    # the whole door: nothing is asked of the game, and no station is taken
    game = Game(tmp_path)
    out = io.StringIO()
    code = L.main(
        [
            "--game",
            "http://testserver",
            "--endpoint",
            "http://127.0.0.1:11434",
            "--station",
            "officer",
        ],
        inp=io.StringIO(""),
        out=out,
        transport=ollama({}),
        game_http=game.http,
    )
    assert code == L.EXIT_UNREACHABLE and game.world.agents == {} and not game.records.exists()
    assert "the officer of the watch is not seated without a context size" in out.getvalue()
    # the guard on the officer's own brief
    officers = L.station_brief_tokens("officer")
    watchers = L.station_brief_tokens("watcher")
    assert officers > watchers > L.SITUATION_ALLOWANCE_TOKENS == 2500
    m = L.LocalModel("http://127.0.0.1:11434", transport=ollama({"show": 65536}))
    m.identity()
    said = m.check_context("x", "a test runtime", "officer")
    assert f"the brief {officers} tokens (the officer of the watch's own brief)" in said
    as_watcher = m.check_context("x", "a test runtime", "watcher")
    assert "(the consent brief, the longer of the two)" in as_watcher
    need = int(said.split("the station needs about ")[1].split(":")[0])
    need_w = int(as_watcher.split("the station needs about ")[1].split(":")[0])
    assert need > need_w
    # a context between the two seats a watcher and refuses the officer, with the numbers
    between = L.LocalModel("http://127.0.0.1:11434", transport=ollama({"show": need - 1}))
    between.identity()
    with pytest.raises(L.DoorError, match="The context is too small"):
        between.check_context("x", "a test runtime", "officer")
    if need_w <= need - 1:
        assert between.check_context("x", "a test runtime", "watcher").startswith(
            "The context is enough"
        )


# ---------------------------------------------------------------------------
# Package 37i: the local runner (the review of gate 5c, G15 and part K; the five faults
# of game 10), on the fake server in both of its forms: llama-server's (and Ollama's
# OpenAI-compatible endpoint's) `finish_reason` and `usage`, and Ollama's own
# `done_reason`, `prompt_eval_count` and `eval_count`
# ---------------------------------------------------------------------------


def answered(
    msg: dict[str, Any], finish: str = "stop", prompt: int | None = None, completion: int = 0
) -> dict[str, Any]:
    """A whole response in the OpenAI form, with why it ended and the server's counts."""
    resp: dict[str, Any] = {"choices": [{"index": 0, "message": msg, "finish_reason": finish}]}
    if prompt is not None:
        resp["usage"] = {
            "prompt_tokens": prompt,
            "completion_tokens": completion,
            "total_tokens": prompt + completion,
        }
    return {"__response__": resp}


def ollama_answered(
    msg: dict[str, Any], done_reason: str = "stop", prompt: int | None = None, completion: int = 0
) -> dict[str, Any]:
    """A whole response in Ollama's own form."""
    resp: dict[str, Any] = {"model": "made-up:7b", "message": msg, "done": True}
    resp["done_reason"] = done_reason
    if prompt is not None:
        resp["prompt_eval_count"] = prompt
        resp["eval_count"] = completion
    return {"__response__": resp}


def server_count(body: dict[str, Any], chars_per_token: float = 3.5) -> int:
    """The fake server's own count of a request, as a server counts it: the text of each
    message and its calls, and the tool definitions, at 3.5 characters a token (game 10's
    figure for its model and samples, the review's G15: the four-character rule ran 12 to
    17 per cent short), with four tokens a message for the chat template."""
    chars = len(json.dumps(body.get("tools") or []))
    for m in body["messages"]:
        chars += len(str(m.get("content") or "")) + len(json.dumps(m.get("tool_calls") or []))
    return math.ceil(chars / chars_per_token) + 4 * len(body["messages"])


def counted(msg: dict[str, Any] | None = None, form: str = "llama", per: float = 3.5):
    """A reply made from the request, carrying the server's count of it."""

    def make(body: dict[str, Any]) -> dict[str, Any]:
        n = server_count(body, per)
        if form == "ollama":
            return ollama_answered(msg or {"role": "assistant", "content": "Aye."}, "stop", n, 3)
        return answered(msg or message("Aye."), "stop", n, 3)

    return make


THINKING = {"role": "assistant", "content": "", "reasoning_content": "The wind backs; " * 40}


def test_a_reply_cut_off_while_thinking_is_asked_once_more_with_the_reason_said():
    """Item 1 (game 10: 22 of 414 replies cut at the reply limit while the model thought,
    passed on as empty turns with no word to anyone). The runner reads why the reply
    ended; a reply cut at the limit while the model thought is asked for once more in the
    same request with the reason said at its end, and the owner is told."""
    told: list[str] = []
    server = llama([answered(THINKING, "length", 9000, 4096), answered(message("All quiet."))])
    m = model_for(server, say=told.append)
    world = point_world()
    h = Harness(world, watcher(SamplingPolicy.in_lockstep(600)), m)
    h.start()
    first, second = server.bodies
    assert second["messages"][:-1] == first["messages"][:-1]
    asked = second["messages"][-1]["content"]
    assert asked.startswith(first["messages"][-1]["content"])  # one user message, not two
    assert asked.endswith(
        "From the local runner, not the game: your last reply was cut off at the reply limit "
        "(4,096 tokens) while you were still thinking, and nothing of it reached the game: no "
        "words and no call. This is the same turn, asked once more; think more briefly, and "
        "answer with a call or with words."
    )
    assert told == [
        "The model's reply was cut off at the reply limit (4,096 tokens) while it was still "
        "thinking; it is asked once more, with the reason."
    ]
    assert [e.text for e in world.log if e.kind == "agent.note"] == ["[watcher] All quiet."]
    assert len(h.transcript) == 1 and m.finish == "stop" and m.cut_off is None
    # Ollama's own form: done_reason, and the thinking in the message
    thought = {"role": "assistant", "content": "", "thinking": "Which way is the tide?"}
    olla = Server(
        [
            ollama_answered(thought, "length"),
            ollama_answered({"role": "assistant", "content": "Aye."}),
        ],
        props=None,
    )
    m = model_for(olla)
    world = point_world()
    Harness(world, watcher(SamplingPolicy.in_lockstep(600)), m).start()
    assert len(olla.bodies) == 2
    assert "while you were still thinking" in olla.bodies[1]["messages"][-1]["content"]
    assert [e.text for e in world.log if e.kind == "agent.note"] == ["[watcher] Aye."]
    # an unclosed <think> in the content is thinking too; cut and then empty, the turn
    # has no reply
    server = llama([answered(message("<think>The tide turns at"), "length"), message("")])
    m = model_for(server)
    r = m.reply([Turn(OPERATOR, "brief"), Turn(DATA, {"reason": "x"})])
    assert r is not None and r.is_silent and len(server.bodies) == 2
    assert m.cut_off == (
        "The model's reply was cut off at the reply limit (4,096 tokens) while it was still "
        "thinking, and came empty again when asked once more; the turn ended with nothing done"
    )
    # an empty reply, however it ended, is asked again with its own words
    server = llama([answered(message(""), "stop"), message("Here.")])
    m = model_for(server)
    r = m.reply([Turn(OPERATOR, "brief"), Turn(DATA, {"reason": "x"})])
    assert r is not None and r.text == "Here." and m.cut_off is None
    assert server.bodies[1]["messages"][-1]["content"].endswith(
        "your last reply came with no words and no call, so nothing reached the game. This is "
        "the same turn, asked once more; answer with a call or with words."
    )
    # a reply cut at the limit with words in it is a reply, and is passed on
    server = llama([answered(message("The wind is "), "length")])
    r = model_for(server).reply([Turn(OPERATOR, "b"), Turn(DATA, {"reason": "x"})])
    assert r.text == "The wind is"


def test_a_reply_cut_off_twice_ends_the_turn_with_nothing_done_and_the_journal_says_so(
    tmp_path,
):
    """Item 1, through the game: cut off again when asked once more, the owner is told,
    the turn ends with nothing done (no empty reply is passed on as the model's) and the
    station's journal says why; the act is recorded, and the save replays to the same
    log and the same journal."""
    from freesail.api.session import ship_factory
    from freesail.core import replay

    game = Game(tmp_path)
    consent.Record(GGUF, "t", "2026-09-26", consent.YES, answer="Yes.").write(game.records)
    cut = answered(THINKING, "length", None)
    server = llama([cut, cut, message("Awake now.")])
    got = run_runner(game, server, [])
    game.wait_for(game.floor_is_the_games(0))
    h = game.harness
    with game.driver.lock:
        assert [e for e in h.transcript if "reply" in e] == []  # no reply reached the game
        act = h.transcript[0]
        assert act["door"] == "cut_off" and act["by"] == "the local runner"
        assert act["after_inputs"] == len(game.world.inputs)
        entry = h.journal.entries[-1]
        assert entry.kind == "agent.cut_off"
        assert entry.text == (
            "No reply reached the game through the local runner: The model's reply was cut "
            "off at the reply limit (4,096 tokens) while it was still thinking, and was cut "
            "off again when asked once more; the turn ended with nothing done."
        )
        assert game.lines("agent.note") == []
    game.driver.tick(A_GLASS_S)
    game.wait_for(game.floor_is_the_games(1))
    assert game.lines("agent.note") == ["[watcher] Awake now."]
    with game.driver.lock:
        game.world.submit("stand down the watcher")
    assert finished(got) == L.EXIT_RELEASED
    assert len(server.bodies) == 3
    text = got["out"].getvalue()
    assert "it is asked once more, with the reason." in text
    assert (
        "the turn ended with nothing done, and the station's journal says so. A larger "
        "--max-reply (now 4,096) gives it more room." in text
    )
    with game.driver.lock:
        data = json.loads(json.dumps(game.world.save()))
        digest = game.world.log.digest()
        journal = game.world.agent_journals["watcher"].save()
    copy = replay.replay(data, ship_factory)
    assert copy.log.digest() == digest
    assert copy.agent_journals["watcher"].save() == journal


def test_the_budget_counts_by_the_servers_figure_from_the_first_reply_on():
    """Item 2. The four-character rule stands alone only until the first reply; from then
    on each message is measured by the ratio of the server's own count of the last
    request to the runner's measure of it, in llama-server's `usage` and in Ollama's
    `prompt_eval_count` alike; a count under half the measure is taken for a partial one
    and not used; and the reply carries the counts to the game."""
    turns = [Turn(OPERATOR, "B" * 400)]
    for k in range(10):
        turns.append(Turn(DATA, {"reason": f"sample {k}", "log": ["x" * 2000]}))
        turns.append(Turn(MODEL, Reply(text=f"reply {k}")))
    turns.append(Turn(DATA, {"reason": "the last", "log": []}))
    for server in (llama([counted()]), Server([counted(form="ollama")])):
        m = model_for(server)
        m._props_read = True
        assert m.ratio is None
        r = m.reply(turns)
        n = server_count(server.bodies[0])
        assert m.served == {"prompt": n, "reply": 3} and r.served_tokens == m.served
        assert m.ratio == n / m._sent_measure and 1.1 < m.ratio < 1.2  # game 10's short count
    # the budget: what the four-character rule says fits does not by the server's count
    probe = L.LocalModel(ENDPOINT, ctx_size=10**6)
    probe._props_read = True
    sent = probe.messages(turns)
    need = sum(probe.measure(x) for x in sent) + probe.measure(probe.tools_schema())
    m = L.LocalModel(ENDPOINT, ctx_size=need + L.REPLY_MAX_TOKENS + 10)
    m._props_read = True
    m.messages(turns)
    assert m.dropped_turns == 0
    m.ratio = 4 / 3.5
    kept = m.messages(turns)
    assert m.dropped_turns > 0 and json.loads(kept[-1]["content"])["reason"] == "the last"
    # a count too small to be of the whole request (a cached prompt) is not used
    server = llama([answered(message("Aye."), "stop", 10, 3)])
    m = model_for(server)
    m._props_read = True
    r = m.reply(turns)
    assert m.ratio is None and m.served is None and r.served_tokens is None
    # the counts go to the game with the reply, and come back with the turn
    back = Reply.from_dict(Reply("a", served_tokens={"prompt": 5}).to_dict())
    assert back.served_tokens == {"prompt": 5}
    assert "served_tokens" not in Reply("a").to_dict()


def officer_world():
    from freesail.api.session import make_world

    return make_world(
        7, str(ROOT / "data/ships/frigate-36.yaml"), Scenario(gustiness=0.0, variability=0.0)
    )


def test_the_handover_is_asked_for_by_the_servers_count():
    """Item 2 at the harness: the officer's conversation is measured by the server's own
    count of the request that brought the latest reply where the runner gives it (the
    larger of that and the four-character rule), so the note is asked for where the
    server's count, and not the short one, crosses the reserve."""
    from freesail.agents.agent import officer

    def seat(with_counts: bool) -> Harness:
        world = officer_world()
        reply = counted(per=2.5) if with_counts else message("Aye.")
        m = model_for(Server([reply]))
        m._props_read = True
        h = Harness(world, officer(SamplingPolicy.in_lockstep(600), world=world), m)
        h.budget_tokens = 20000  # the threshold: 20,000 less three tenths, 14,000
        h.start()
        return h

    by_count = seat(True)
    served = by_count.turns[-1].content.served_tokens["prompt"]
    plain = seat(False)
    assert plain._conversation_size() < 14000 <= served  # the short count alone would not ask
    assert by_count._conversation_size() >= served
    assert any("handover note" in n for n in by_count.agent.notices)
    assert not any("handover note" in n for n in plain.agent.notices)
    # after the fold, the count of a request before it is not the folded conversation's
    padding = [Turn(DATA, {"reason": f"older {k}", "log": []}) for k in range(8)]
    by_count.turns[1:1] = padding
    by_count._fold_handover("The watch so far.")
    assert by_count.turns[1].content["handover"] == "The watch so far."
    kept = [t.content for t in by_count.turns if t.role == MODEL]
    assert all(r.served_tokens is None for r in kept)


def test_the_handover_reserve_is_tokens_or_a_share_and_the_larger_when_both(tmp_path):
    """Item 3. `--handover-reserve` takes tokens or a share of the context, given twice
    the larger counts, and is sent in tokens with the station request; unset, the
    harness's own share, three tenths, so that the note is asked for in time at any
    size (37g's 14,000 tokens left it to 88,400 of 102,400)."""
    from freesail.agents import harness as harness_mod
    from freesail.agents.remote import GameClient

    assert L.reserve_form("30000") == ("tokens", 30000.0)
    assert L.reserve_form("30,000") == ("tokens", 30000.0)
    assert L.reserve_form("0.3") == ("share", 0.3) and L.reserve_form("30%") == ("share", 0.3)
    for bad in ("0", "-5", "1.5", "lots", "100%"):
        with pytest.raises(Exception, match="neither a number of tokens"):
            L.reserve_form(bad)
    assert L.handover_reserve_tokens(None, 102400) is None
    assert L.handover_reserve_tokens([("tokens", 30000.0)], 102400) == 30000
    assert L.handover_reserve_tokens([("share", 0.3)], 102400) == 30720
    both = [("tokens", 30000.0), ("share", 0.3)]
    assert L.handover_reserve_tokens(both, 102400) == 30720
    assert L.handover_reserve_tokens([("tokens", 40000.0), ("share", 0.3)], 102400) == 40000
    assert L.handover_reserve_tokens([("share", 0.3)], None) is None
    assert L.handover_words(both, 102400, 30720) == (
        "The handover note is asked for when the conversation, by the server's own count, "
        "has left less than 30,720 of the 102,400 tokens (--handover-reserve 30,000 tokens "
        "and 0.3 of the context, the larger), and never before 0.6 of them: at about 71,680."
    )
    assert L.handover_words(None, 32768, None).endswith(
        "(the harness's own share, 0.3 of the context and never less than 14,000 tokens), "
        "and never before 0.6 of them: at about 19,660."
    )
    with pytest.raises(SystemExit):
        L.main(["--handover-reserve", "lots"], out=io.StringIO())
    # sent with the station request in tokens, kept on the harness and in the save
    game = Game(tmp_path)
    client = GameClient("http://testserver", http=game.http)
    consent.Record("made-up-weights", "r", "2026-09-26", consent.YES, answer="Yes.").write(
        game.records
    )
    first = client.station(
        "made-up-weights", "runner", context_tokens=102400, handover_reserve=30720
    )
    assert first["phase"] == "station"
    h = game.world.agents["watcher"]
    assert h.budget_tokens == 102400 and h.reserve_tokens == 30720
    assert h.handover_threshold() == (102400 - 30720, 30720 // 4)
    assert game.world.save()["agents"][0]["reserve_tokens"] == 30720
    # unset: the harness's own share
    h.reserve_tokens = None
    assert harness_mod.HANDOVER_RESERVE_SHARE == 0.3
    assert harness_mod.HANDOVER_RESERVE_TOKENS == 14000
    assert h.handover_threshold() == (102400 - 30720, 7680)
    h.budget_tokens = 32768  # a small context: 14,000 at least, so six tenths govern
    assert h.handover_threshold() == (int(0.6 * 32768), int(0.1 * 32768))


def refusing(ctx: int, per: float = 3.5, always: bool = False, words_only: bool = False):
    """A fake llama-server that refuses a request over its context with its own count,
    as llama-server does (400, `exceed_context_size_error`, `n_prompt_tokens`, `n_ctx`),
    or in words alone with no count, and answers one that fits."""

    def make(body: dict[str, Any]) -> dict[str, Any]:
        n = server_count(body, per)
        if always or n > ctx:
            if words_only:
                err: Any = "the input length exceeds the context length"
            else:
                err = {
                    "code": 400,
                    "message": "the request exceeds the available context size, try increasing it",
                    "type": "exceed_context_size_error",
                    "n_prompt_tokens": max(n, ctx + 1) if always else n,
                    "n_ctx": ctx,
                }
            return {"__status__": 400, "json": {"error": err}}
        return answered(message("Aye."), "stop", n, 3)

    return make


def long_watch(samples: int = 14) -> list[Turn]:
    """A brief, the handover note folded in after it, and a long run of samples."""
    turns = [Turn(OPERATOR, "B" * 2000)]
    turns.append(
        Turn(
            DATA,
            {"reason": "the handover note", "handover": "N" * 800, "folded": "f", "readings": {}},
        )
    )
    for k in range(samples):
        turns.append(Turn(DATA, {"reason": f"sample {k}", "log": ["x" * 3000]}))
        turns.append(Turn(MODEL, Reply(text=f"reply {k}")))
    turns.append(Turn(DATA, {"reason": "the last", "log": ["y" * 100]}))
    return turns


def test_a_request_refused_for_its_size_is_asked_again_smaller_and_never_the_same():
    """Item 4 (game 10: the server refused at 103,679 and 103,122 tokens, the runner sent
    the same request three times and stood the station down). The runner takes the
    server's own count from the refusal, leaves out the oldest exchanges that are not the
    brief, the handover note or the latest sample, says so once, and asks again; it never
    sends the same request again, and stands the station down with the numbers only when
    the server goes on refusing smaller requests."""
    turns = long_watch()
    probe = L.LocalModel(ENDPOINT, ctx_size=10**6)
    probe._props_read = True
    full = probe.messages(turns)
    measure = sum(probe.measure(x) for x in full) + probe.measure(probe.tools_schema())
    ctx = measure + 200  # fits by the four-character rule, not by the server's count
    told: list[str] = []
    server = llama([refusing(ctx), refusing(ctx), refusing(ctx)])
    m = model_for(server, ctx_size=ctx + L.REPLY_MAX_TOKENS, say=told.append)
    m._props_read = True
    r = m.reply(turns)
    assert r is not None and r.text == "Aye." and m.failed is None
    first, second = server.bodies
    assert first["messages"] == full and second["messages"] != full
    assert len(second["messages"]) < len(full) and m.dropped_turns > 0
    assert second["messages"][0]["role"] == "system"
    assert json.loads(second["messages"][1]["content"])["handover"] == "N" * 800
    assert json.loads(second["messages"][-1]["content"])["reason"] == "the last"
    n = server_count(first)
    assert told == [
        f"The model server refused the request for its size ({n:,} tokens by its count; the "
        f"context is {ctx:,}). The oldest exchanges are left out (never the brief, the "
        "handover note or the latest sample) and it is asked again; from now on the runner "
        "measures by the server's count."
    ]
    assert m.served_ctx == ctx and m.ratio > 1.1
    # a server that goes on refusing: each request smaller, none sent twice, and at the
    # third refusal in the turn the station is stood down with the numbers
    server = llama([refusing(ctx, always=True)] * 5)
    m = model_for(server, ctx_size=ctx + L.REPLY_MAX_TOKENS)
    m._props_read = True
    assert m.reply(turns) is None
    bodies = [json.dumps(b["messages"]) for b in server.bodies]
    assert len(bodies) == L.OVERSIZE_TRIES == 3 and len(set(bodies)) == 3
    assert [len(b) for b in bodies] == sorted((len(b) for b in bodies), reverse=True)
    assert "The server refused 3 requests for their size in one turn" in (m.failed or "")
    # a refusal in words with no count: the runner measures by more (`OVERSIZE_STEP`)
    server = llama([refusing(ctx, words_only=True), counted()])
    m = model_for(server, ctx_size=ctx + L.REPLY_MAX_TOKENS)
    m._props_read = True
    assert m.reply(turns).text == "Aye."
    assert server.bodies[1]["messages"] != server.bodies[0]["messages"]
    # no context size known to trim against: stood down in words, not asked again
    server = llama([refusing(ctx, words_only=True)])
    m = model_for(server)
    m._props_read = True
    assert m.reply(turns) is None and "state it with --ctx" in (m.failed or "")
    assert len(server.bodies) == 1


def test_the_two_stopgap_settings_on_the_fake_server():
    """Part K's two stopgaps, tried on the fake server (they were untried). A larger
    `--max-reply` lets a model that thinks past 4,096 tokens answer, where the default
    is cut off twice and the turn ends with nothing done. `--handover-reserve 30000`, at
    game 10's context and with the four-character rule alone, has the note asked for
    well under the ceiling by the server's count, where 37g's 14,000 asked for it only
    once there was no room left for the reply; with this package's count and default
    share the ask comes at about seven tenths by the server's count."""
    from freesail.agents.agent import officer

    def thinker(body: dict[str, Any]) -> dict[str, Any]:
        if body["max_tokens"] < 6000:  # this model thinks for 6,000 tokens
            return answered(THINKING, "length", None, body["max_tokens"])
        return answered(message("Aye."), "stop", None, 6100)

    turns = [Turn(OPERATOR, "brief"), Turn(DATA, {"reason": "x"})]
    short = model_for(llama([thinker, thinker]))
    assert short.reply(turns).is_silent and short.cut_off is not None
    roomy = model_for(llama([thinker]), max_reply=8192)
    assert roomy.reply(turns).text == "Aye." and roomy.cut_off is None
    # the reserve: an officer's conversation grown sample by sample at game 10's context
    world = officer_world()
    h = Harness(world, officer(SamplingPolicy.in_lockstep(600), world=world), model_for(llama()))
    ctx = 102400
    h.budget_tokens = ctx
    runner = L.LocalModel(ENDPOINT)
    runner._props_read = True
    schema = runner.tools_schema()

    def count(ts: list[Turn]) -> int:
        return server_count({"messages": runner.messages(ts), "tools": schema})

    log = [{"tick": k, "text": f"By the deep {k % 20}; the account kept. " * 4} for k in range(24)]
    ts = [Turn(OPERATOR, "B" * 18000)]
    asked: dict[str, int] = {}
    settings = {"37g": 14000, "stopgap": 30000, "37i": None}
    while len(asked) < len(settings):
        ts.append(Turn(DATA, {"reason": "a glass", "log": log}))
        before = count(ts)
        ts.append(Turn(MODEL, Reply(text="Noted.", served_tokens={"prompt": before})))
        for name, reserve in settings.items():
            if name in asked:
                continue
            h.reserve_tokens = reserve
            # before this package no reply carried the server's count
            h.turns = (
                ts
                if name == "37i"
                else [Turn(MODEL, Reply(text=t.content.text)) if t.role == MODEL else t for t in ts]
            )
            if h._conversation_size() >= h.handover_threshold()[0]:
                asked[name] = count(ts)
    assert asked["37g"] > ctx - L.REPLY_MAX_TOKENS  # too late: no room left for the reply
    assert ctx - asked["stopgap"] > 14000  # in time, with room to write the note
    assert 0.68 * ctx < asked["37i"] < 0.74 * ctx  # about seven tenths, by the server's count
