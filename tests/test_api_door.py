"""The API door (spec M6 §13; package 42, `freesail/agents/api.py`) against a local HTTP
server speaking the Messages API's shape (`tests/messages_api.py`), never the API: the
key's road through a fake credential store, the door's refusals to start, the request
it sends each turn and what the server saw, a reply cut off asked once more, a refusal
not asked again, another model's reply not passed on, the server's own counts said, the
door as a client of the game from the consent question to the stand-down, the chart's
picture through the door, and the OpenRouter dialect on the local runner's shape. The
model's name is made up, the key a string of the key's shape made here, and the consent
records and the saves go to a temporary folder.
"""

from __future__ import annotations

import io
import json
import re
import subprocess
from pathlib import Path

import pytest

pytest.importorskip("anthropic")
pytest.importorskip("keyring")
pytest.importorskip("fastapi")
httpx = pytest.importorskip("httpx")

from messages_api import (  # noqa: E402
    MODEL,
    Game,
    MessagesServer,
    fake_store,
    finished,
    png,
    run_door,
)

from freesail.agents import api, consent  # noqa: E402
from freesail.agents.agent import A_GLASS_S  # noqa: E402
from freesail.agents.model import DATA, OPERATOR, Reply, ToolCall, Turn  # noqa: E402
from freesail.agents.model import MODEL as MODEL_ROLE  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]

# a key of the key's shape, made here and never written as one
KEY = "sk" + "-ant-" + "api03-" + "Tq7xLmPz" * 6


def text(t: str) -> dict:
    return {"type": "text", "text": t}


def call(name: str, **args) -> dict:
    return {"type": "tool_use", "name": name, "input": args}


def thinking(signature: str = "sig-1") -> dict:
    return {"type": "thinking", "thinking": "", "signature": signature}


def model_for(server: MessagesServer, **kw) -> api.ApiModel:
    m = api.ApiModel(MODEL, KEY, base_url=server.url, **kw)
    m.identity()
    return m


# ---------------------------------------------------------------------------
# The key's road (the security pass, item 2)
# ---------------------------------------------------------------------------


def test_the_key_is_read_from_the_store_first_then_the_environment_then_a_file(
    monkeypatch, tmp_path
):
    store = fake_store(monkeypatch)
    keyfile = tmp_path / "the-key"
    keyfile.write_text("from-the-file-" + "z" * 20 + "\n")
    env = {
        "FREESAIL_API_KEY": "from-the-env-" + "y" * 20,
        "ANTHROPIC_API_KEY": "sdk-own-" + "x" * 20,
    }
    # none in the store: the environment, the game's own name first
    key, where = api.read_key(environ=env, key_file=str(keyfile))
    assert key.startswith("from-the-env") and where == "the environment (FREESAIL_API_KEY)"
    key, where = api.read_key(environ={"ANTHROPIC_API_KEY": "sdk-own-" + "x" * 20})
    assert where == "the environment (ANTHROPIC_API_KEY)"
    # the file third
    key, where = api.read_key(environ={}, key_file=str(keyfile))
    assert key == "from-the-file-" + "z" * 20 and where == f"the file {keyfile}"
    # the store first, whatever the environment says
    store.set_password(api.KEYRING_SERVICE, api.KEYRING_ACCOUNT, KEY)
    key, where = api.read_key(environ=env, key_file=str(keyfile))
    assert key == KEY and where == "the credential store (service freesail, anthropic-api)"
    # none anywhere: words that say where it looked, and how to put it in the store
    store.kept.clear()
    with pytest.raises(api.KeyError_) as none:
        api.read_key(environ={})
    assert "the credential store has none" in str(none.value)
    assert "--store-key" in str(none.value)


def test_store_key_prompts_without_echo_and_writes_nothing_else(monkeypatch, tmp_path):
    store = fake_store(monkeypatch)
    monkeypatch.chdir(tmp_path)
    asked: list[str] = []

    def prompt(words: str) -> str:
        asked.append(words)
        return KEY

    out = io.StringIO()
    assert api.main(["--store-key"], out=out, prompt=prompt) == 0
    assert store.kept == {(api.KEYRING_SERVICE, api.KEYRING_ACCOUNT): KEY}
    assert asked and "not shown as you type" in asked[0]
    assert KEY not in out.getvalue() and "Nothing else was written." in out.getvalue()
    assert list(tmp_path.iterdir()) == []  # no file of any kind
    # the dialect's own account
    assert api.main(["--store-key", "--dialect", "openrouter"], out=out, prompt=prompt) == 0
    assert (api.KEYRING_SERVICE, api.OPENROUTER_ACCOUNT) in store.kept


def test_the_door_refuses_to_start_where_the_key_would_be_written(tmp_path):
    """A key file inside the repository (the records, the saves and the journals are kept
    there); the key in a word the door sends the game; a base URL with a credential in it;
    the SDK's logging on. The words never hold the key."""
    inside = ROOT / "saves" / "the-key"
    words = [
        api.refusal_to_start(KEY, key_file=str(inside), environ={}),
        api.refusal_to_start(KEY, sent=(f"a model {KEY}",), environ={}),
        api.refusal_to_start(KEY, base_url="https://user:pass@proxy.example/", environ={}),
        api.refusal_to_start(KEY, base_url="https://proxy.example/?token=abc", environ={}),
        api.refusal_to_start(KEY, environ={"ANTHROPIC_LOG": "debug"}),
        api.refusal_to_start("short", environ={}),
    ]
    assert all(words) and not any(KEY in w for w in words)
    assert "inside" in words[0] and "--store-key" in words[0]
    assert api.refusal_to_start(KEY, key_file=str(tmp_path / "k"), environ={}) is None
    assert api.refusal_to_start(KEY, base_url="http://127.0.0.1:9", environ={}) is None


def test_the_door_will_not_start_without_a_model_or_a_key_and_says_so(monkeypatch):
    fake_store(monkeypatch)
    out = io.StringIO()
    assert api.main(["--game", "http://testserver"], out=out, environ={}) == 2
    assert "--model" in out.getvalue() and "no default" in out.getvalue()
    out = io.StringIO()
    assert api.main(["--model", MODEL], out=out, environ={}) == 2
    assert "No key for the API" in out.getvalue()
    out = io.StringIO()
    env = {"FREESAIL_API_KEY": KEY}
    assert api.main(["--model", f"x{KEY}"], out=out, environ=env) == 2
    assert "does not start" in out.getvalue() and KEY not in out.getvalue()


# ---------------------------------------------------------------------------
# The wire (item 1): what the door sends per turn, and what it reads back
# ---------------------------------------------------------------------------


def test_the_identity_is_the_name_the_api_reports_and_its_context():
    with MessagesServer(KEY, models={"made-up-alias": MODEL}, context=150_000) as srv:
        m = api.ApiModel("made-up-alias", KEY, base_url=srv.url)
        assert m.identity() == MODEL and m.context_size() == 150_000
        assert srv.requests[0]["path"] == "/v1/models/made-up-alias"
        with pytest.raises(Exception) as unknown:
            api.ApiModel("no-such", KEY, base_url=srv.url).identity()
        assert "knows no model 'no-such'" in str(unknown.value)
        with pytest.raises(Exception) as refused:
            api.ApiModel(MODEL, "wrong-key-" + "w" * 20, base_url=srv.url).identity()
        assert "refused the key (401)" in str(refused.value)


def test_each_request_is_streamed_with_the_brief_and_the_tools_cached_and_the_ids_answered():
    """The brief is the system prompt, cached with the tools; the conversation cached to
    its last block; adaptive thinking with a changed conversation's blocks dropped and not
    refused (the beta in the header); the tool calls answered by the API's own ids; the
    assistant's turn sent back as the API gave it, thinking and all; streamed."""
    replies = [
        {
            "content": [thinking("s-1"), text("Aye."), call("readings")],
            "usage": {"input_tokens": 900, "output_tokens": 40},
        },
        {
            "content": [text("All well.")],
            "usage": {"input_tokens": 60, "cache_read_input_tokens": 880, "output_tokens": 9},
        },
    ]
    with MessagesServer(KEY, replies) as srv:
        m = model_for(srv, effort="high")
        m.offered_tools = ("readings", "journal", "stand_by")
        turns = [
            Turn(OPERATOR, "The brief."),
            Turn(DATA, {"reason": "the start", "readings": {"heading": "S"}, "log": []}),
        ]
        first = m.reply(turns)
        assert (first.text, first.calls) == ("Aye.", (ToolCall("readings", {}),))
        assert first.raw == 'Aye.\n[{"name": "readings", "arguments": {}}]'  # what the scan reads
        assert first.served_tokens == {"prompt": 900, "reply": 40}
        turns += [
            Turn(MODEL_ROLE, first),
            Turn(
                DATA,
                {"tool_results": [{"name": "readings", "args": {}, "result": {"heading": "S"}}]},
            ),
        ]
        second = m.reply(turns)
        assert second.text == "All well." and second.served_tokens == {"prompt": 940, "reply": 9}
        bodies = srv.bodies()
        heads = [r["headers"] for r in srv.requests if r["method"] == "POST"]
    b = bodies[1]
    assert b["model"] == MODEL and b["stream"] is True and b["max_tokens"] == api.REPLY_MAX_TOKENS
    assert b["system"] == [
        {"type": "text", "text": "The brief.", "cache_control": {"type": "ephemeral"}}
    ]
    assert b["cache_control"] == {"type": "ephemeral"}
    assert b["thinking"] == {
        "type": "adaptive",
        "block_binding": {"prefix_mismatch_behavior": "drop_block"},
    }
    assert b["output_config"] == {"effort": "high"}
    assert [t["name"] for t in b["tools"]] == ["readings", "journal", "stand_by"]
    assert set(b["tools"][0]) == {"name", "description", "input_schema"}
    assert all(h["anthropic-beta"] == api.THINKING_BINDING_BETA for h in heads)
    assert all(h["x-api-key"] == KEY for h in heads)
    assistant = b["messages"][1]
    assert assistant["role"] == "assistant"
    assert assistant["content"][0] == {"type": "thinking", "thinking": "", "signature": "s-1"}
    cid = assistant["content"][2]["id"]
    assert b["messages"][2] == {
        "role": "user",
        "content": [{"type": "tool_result", "tool_use_id": cid, "content": '{"heading": "S"}'}],
    }
    assert m.usage.words("so far") == (
        "The API reported, so far, for 2 requests: 1,840 tokens in (880 read from the cache, "
        "0 written to it, 960 not cached) and 49 tokens out."
    )
    # no effort asked: the model's own, and nothing sent for it
    with MessagesServer(KEY, [{"content": [text("Aye.")]}]) as srv:
        model_for(srv).reply(turns[:2])
        assert "output_config" not in srv.bodies()[0]


def test_a_reply_cut_off_is_asked_once_more_then_the_turn_ends_with_nothing_done():
    cut = {"content": [text("I would"), call("say", text="half")], "stop_reason": "max_tokens"}
    turns = [
        Turn(OPERATOR, "The brief."),
        Turn(DATA, {"reason": "the glass", "readings": {}, "log": []}),
    ]
    with MessagesServer(KEY, [cut, {"content": [text("Short now.")]}]) as srv:
        said: list[str] = []
        m = model_for(srv, say=said.append, max_reply=500)
        r = m.reply(turns)
        assert r.text == "Short now." and m.cut_off is None
        notice = srv.bodies()[1]["messages"][-1]["content"][-1]["text"]
        assert notice.startswith("From the API door, not the game: your last reply was cut off")
        assert "(500 tokens)" in notice and "cut off at the reply limit (500 tokens)" in said[0]
    with MessagesServer(KEY, [cut, cut]) as srv:
        m = model_for(srv)
        r = m.reply(turns)
        assert r == Reply() and "was cut off again" in m.cut_off
        assert len(srv.bodies()) == 2


def test_a_refusal_is_not_asked_again_and_another_models_reply_is_not_passed_on():
    turns = [
        Turn(OPERATOR, "The brief."),
        Turn(DATA, {"reason": "the glass", "readings": {}, "log": []}),
    ]
    refusal = {
        "content": [],
        "stop_reason": "refusal",
        "stop_details": {"type": "refusal", "category": "cyber", "explanation": "declined"},
    }
    with MessagesServer(KEY, [refusal]) as srv:
        m = model_for(srv)
        assert m.reply(turns) == Reply()
        assert "safeguards declined the reply" in m.cut_off and "cyber" in m.cut_off
        assert len(srv.bodies()) == 1
    with MessagesServer(KEY, [{"content": [text("Aye.")], "model": "another-model"}]) as srv:
        m = model_for(srv)
        assert m.reply(turns) is None
        assert "another model (another-model)" in m.failed and "consent is per model" in m.failed


def test_the_exchanges_are_bodies_without_headers_and_hold_no_key(tmp_path):
    turns = [
        Turn(OPERATOR, "The brief."),
        Turn(DATA, {"reason": "the glass", "readings": {}, "log": []}),
    ]
    kept = tmp_path / "exchanges.jsonl"
    with MessagesServer(KEY, [{"content": [text(f"I saw {KEY} in a dream")]}]) as srv:
        m = model_for(srv, exchanges_file=str(kept))
        m.reply(turns)
    lines = kept.read_text().splitlines()
    assert len(lines) == 1 and KEY not in lines[0]
    entry = json.loads(lines[0])
    assert set(entry) == {"request", "reply"} and "headers" not in lines[0].lower()
    assert "[the key]" in lines[0]


# ---------------------------------------------------------------------------
# The door as a client of the game (items 1 and 2 together)
# ---------------------------------------------------------------------------


def _session(srv: MessagesServer, game: Game, tmp_path: Path) -> tuple[dict, str]:
    env = {"FREESAIL_API_KEY": KEY}
    got = run_door(
        game,
        [
            "--model",
            MODEL,
            "--base-url",
            srv.url,
            "--session",
            "test",
            "--exchanges",
            str(tmp_path / "x.jsonl"),
        ],
        env,
        inp="\n",
    )
    return got, KEY


def test_the_door_asks_consent_through_the_game_keeps_watch_and_says_what_it_used(
    monkeypatch, tmp_path
):
    fake_store(monkeypatch)
    game = Game(tmp_path)
    game.page()
    replies = [
        {
            "content": [call("answer", text="Yes, I am willing.")],
            "usage": {"input_tokens": 2000, "output_tokens": 30},
        },
        {
            "content": [thinking("s-2"), text("A quiet start."), call("chart")],
            "usage": {"input_tokens": 4000, "output_tokens": 50},
        },
        {
            "content": [text("The chart agrees with the reckoning.")],
            "usage": {"input_tokens": 300, "cache_read_input_tokens": 4000, "output_tokens": 12},
        },
        {
            "content": [call("stand_by", until="a glass")],
            "usage": {"input_tokens": 200, "cache_read_input_tokens": 4300, "output_tokens": 8},
        },
    ]
    with MessagesServer(KEY, replies) as srv:
        got, _ = _session(srv, game, tmp_path)
        game.wait_for(game.floor_is_the_games(1))
        game.driver.tick(A_GLASS_S)
        game.wait_for(lambda: game.harness.agent.standing_by)
        with game.driver.lock:
            game.world.submit("stand down the watcher")
        assert finished(got) == 3
        bodies = srv.bodies()
        requests = list(srv.requests)
    out = got["out"].getvalue()
    # the consent question first, through the game, the record the API's name for the model
    rec = consent.check(MODEL, game.records)
    assert rec is not None and rec.verdict == consent.YES
    record = rec.path.read_text(encoding="utf-8")
    assert "the model's name as its API reports it" in record
    assert rec.runtime == (
        "FreeSail's browser game (freesail.ui.server on port 8000), through the API door "
        "(freesail.agents.api), the Anthropic Messages API, at a base URL of the owner's"
    )
    assert [t["name"] for t in bodies[0]["tools"]] == ["answer"]
    # the station: its brief the system prompt, the door's own words in it, the picture
    # tools offered, the chart's picture an image in the next request
    station = bodies[1]
    assert "This door is the model's own API" in station["system"][0]["text"]
    assert {"chart", "ship_view"} <= {t["name"] for t in station["tools"]}
    shown = bodies[2]["messages"][-1]["content"][0]
    assert shown["type"] == "tool_result"
    image = shown["content"][0]
    assert image["type"] == "image" and image["source"]["media_type"] == "image/png"
    import base64

    assert base64.standard_b64decode(image["source"]["data"]) == png(4, 3)
    assert "4 by 3 pixels" in shown["content"][1]["text"]
    assert game.asked and game.asked[0]["view"] == "chart"
    assert game.lines("agent.note") == [
        "[watcher] A quiet start.",
        "[watcher] The chart agrees with the reckoning.",
    ]
    # the transcript keeps a note that it was shown, never the picture
    h = game.harness
    notes = [n for e in h.transcript for n in e.get("shown", [])]
    assert notes and notes[0]["view"] == "chart" and notes[0]["width"] == 4
    assert "data" not in json.dumps(notes)
    # the server's own counts, said at the end
    assert "The API reported, in all, for 4 requests: 14,800 tokens in" in out
    # the key: in every request's header, in no body, nothing the game keeps or prints
    assert all(r["headers"].get("x-api-key") == KEY for r in requests)
    # nothing of the owner's machine: the SDK's headers for it are left out
    assert not any(
        h in r["headers"] for r in requests for h in ("x-stainless-os", "x-stainless-arch")
    )
    assert not any(KEY in r["body"] for r in requests)
    assert KEY not in out
    kept = [p for p in tmp_path.rglob("*") if p.is_file()]
    assert any(p.suffix == ".json" for p in kept)  # the save the stand-down wrote
    for p in kept:
        assert KEY.encode() not in p.read_bytes(), p


def test_the_door_stands_down_when_the_api_answers_with_another_model(monkeypatch, tmp_path):
    fake_store(monkeypatch)
    game = Game(tmp_path)
    consent.Record(MODEL, "t", "2026-10-10", consent.YES, answer="Yes.").write(game.records)
    with MessagesServer(KEY, [{"content": [text("Aye.")], "model": "another-model"}]) as srv:
        got, _ = _session(srv, game, tmp_path)
        assert finished(got) == 3
    out = got["out"].getvalue()
    assert "another model (another-model)" in out
    assert (
        game.harness.agent.released and "consent is per model" in game.harness.agent.released_reason
    )


# ---------------------------------------------------------------------------
# The OpenRouter dialect (decision 31)
# ---------------------------------------------------------------------------


def test_the_openrouter_dialect_sends_the_key_in_the_header_only():
    seen: list[httpx.Request] = []

    def server(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        if request.url.path == "/api/v1/models":
            return httpx.Response(200, json={"data": [{"id": "made-up/model-7"}]})
        if request.url.path == "/api/v1/chat/completions":
            body = json.loads(request.content)
            reply = {"role": "assistant", "content": "Aye."}
            return httpx.Response(
                200, json={"model": body["model"], "choices": [{"message": reply}]}
            )
        return httpx.Response(404)

    m = api.OpenRouterModel(
        "https://openrouter.test/api",
        KEY,
        model="made-up/model-7",
        transport=httpx.MockTransport(server),
    )
    assert m.identity() == "made-up/model-7"
    r = m.reply(
        [Turn(OPERATOR, "The brief."), Turn(DATA, {"reason": "x", "readings": {}, "log": []})]
    )
    assert r.text == "Aye."
    for req in seen:
        assert req.headers["authorization"] == "Bear" + "er " + KEY
        assert KEY.encode() not in req.content
    assert KEY not in json.dumps(m.exchanges)


# ---------------------------------------------------------------------------
# No key in the repository (item 2)
# ---------------------------------------------------------------------------


def test_no_file_of_the_repository_holds_the_shape_of_a_key():
    """Every file git knows (and the ones it would add) is read for the shapes of a key:
    the SDK's prefix, OpenRouter's, a bearer header with a token, an x-api-key header with
    one."""
    try:
        listed = subprocess.run(
            ["git", "ls-files", "-co", "--exclude-standard"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.splitlines()
    except (OSError, subprocess.CalledProcessError):
        pytest.skip("not a git checkout")
    found: list[str] = []
    for name in listed:
        path = ROOT / name
        if not path.is_file() or path.stat().st_size > 20_000_000:
            continue
        try:
            body = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for shape in api.KEY_SHAPES:
            for m in shape.finditer(body):
                found.append(f"{name}: {m.group(0)[:12]}...")
    assert found == []
    assert re.search(api.KEY_SHAPES[0], KEY)  # the shapes find a key of the shape
