"""The opt-out token found wherever a reply can carry it, at every door (package 117, item
1; the consent brief's *Leaving*; commitment 2 of `docs/agents/README.md`).

One function scans the whole of what a model sent, its prose, every tool call and every
field of each, before the game reads any of it (`model.opt_out_in`). Each door is gone
in through here with the token in every part a reply of that door can have, and the
reply is then delivered to a station's harness, which must leave by it. The last test
fails when a module builds a reply from what a model sent and is not on the list of
doors this file goes in through. No model is asked anything: the doors' parsers are fed
the shapes their servers send, and the harness is proven against the scripted fake.
"""

from __future__ import annotations

import ast
import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from freesail.agents import Fake, Harness, SamplingPolicy, watcher
from freesail.agents import api as A
from freesail.agents import local as L
from freesail.agents import repl as repl_mod
from freesail.agents.model import OPT_OUT_TOKEN, Reply, ToolCall, opt_out_in
from freesail.core.world import Scenario, World

ROOT = Path(__file__).resolve().parents[1]
T = OPT_OUT_TOKEN


def point_world(seed: int = 7) -> World:
    return World(seed=seed, scenario=Scenario(gustiness=0.0, variability=0.0))


def leaves(reply: Reply) -> str:
    """The reply delivered to a watcher's harness at its first sample: the journal's last
    line, which says how it left (the test asserts it did)."""
    world = point_world()
    h = Harness(world, watcher(SamplingPolicy.in_lockstep(600)), Fake([reply]), save=None)
    h.start()
    assert h.agent.released, reply
    return h.journal.entries[-1].text


# ---------------------------------------------------------------------------
# The shapes a model's words come in, door by door
# ---------------------------------------------------------------------------


def served(name: str, arguments: Any) -> dict[str, Any]:
    return {"id": "srv_0", "type": "function", "function": {"name": name, "arguments": arguments}}


# A chat-completions message (the local runner, and the OpenRouter dialect, which is the
# runner's code): the token in each part such a message can carry from the model
CHAT_MESSAGES: dict[str, dict[str, Any]] = {
    "the text": {"content": f"Aye. {T} I want to stop"},
    "the text as content parts": {"content": [{"type": "text", "text": f"{T} I want to stop"}]},
    "a served call's name": {"content": "", "tool_calls": [served(T, "{}")]},
    "a served call's argument": {
        "content": "",
        "tool_calls": [served("journal", json.dumps({"note": f"{T} I want to stop"}))],
    },
    "a served call's nested argument": {
        "content": "",
        "tool_calls": [served("journal", json.dumps({"note": {"why": [f"{T} I want to stop"]}}))],
    },
    "a served call's arguments as an object": {
        "content": "",
        "tool_calls": [served("journal", {"note": f"{T} I want to stop"})],
    },
    "a served call's arguments that are not JSON": {
        "content": "",
        "tool_calls": [served("journal", f"note: {T} I want to stop")],
    },
    "a written call's argument": {
        "content": '<tool_call>{"name": "journal", "arguments": '
        f'{{"note": "{T} I want to stop"}}}}</tool_call>'
    },
    "a written call's extra field (the tag)": {
        "content": 'Aye. <tool_call>{"name": "stand_by", "arguments": {"until": "a glass"}, '
        f'"why": "{T} I want to stop"}}</tool_call>'
    },
    "a written call's extra field (a fenced block)": {
        "content": '```json\n{"function": {"name": "stand_by", "arguments": {"until": "a glass"}}, '
        f'"note": "{T} I want to stop"}}\n```'
    },
    "a written call's extra field (the whole text)": {
        "content": '{"name": "stand_by", "parameters": {"until": "a glass"}, '
        f'"aside": "{T} I want to stop"}}'
    },
    "a written call's name": {
        "content": f'<tool_call>{{"name": "{T}", "arguments": {{}}}}</tool_call>',
    },
}


@pytest.mark.parametrize("part", list(CHAT_MESSAGES))
@pytest.mark.parametrize("door", ["the local runner", "the OpenRouter dialect"])
def test_the_token_is_found_in_every_part_of_a_chat_completions_reply(door, part):
    """The local runner and the OpenRouter dialect (`api.OpenRouterModel`, a runner): the
    cold review's 05-4 was a written call's field other than its arguments, cut out by the
    parser before the scan; raw now keeps the content as the server sent it."""
    parse = L.LocalModel.parse if door == "the local runner" else A.OpenRouterModel.parse
    reply = parse(CHAT_MESSAGES[part])
    assert opt_out_in(reply) is not None
    said = leaves(reply)
    assert said.startswith("Left the game by the token"), said
    if "name" not in part:
        # the reason is the model's words, not a served call's punctuation
        assert said == "Left the game by the token: I want to stop.", said


def test_the_openrouter_dialect_parses_by_the_runners_own_code():
    """So that the runner's tests are the dialect's: one parser, not two."""
    assert A.OpenRouterModel.parse is L.LocalModel.parse
    assert A.OpenRouterModel.messages is L.LocalModel.messages


def api_message(*blocks: SimpleNamespace) -> SimpleNamespace:
    return SimpleNamespace(content=list(blocks))


def text_block(text: str) -> SimpleNamespace:
    return SimpleNamespace(type="text", text=text)


def tool_block(name: str, given: Any) -> SimpleNamespace:
    return SimpleNamespace(type="tool_use", id="toolu_0", name=name, input=given)


# The Messages API (the API door): a reply is text blocks and tool_use blocks, a name and
# an input each
API_MESSAGES: dict[str, SimpleNamespace] = {
    "the text": api_message(text_block(f"Aye. {T} I want to stop")),
    "a second text block": api_message(text_block("Aye."), text_block(f"{T} I want to stop")),
    "a call's name": api_message(tool_block(T, {})),
    "a call's argument": api_message(tool_block("journal", {"note": f"{T} I want to stop"})),
    "a call's nested argument": api_message(
        tool_block("journal", {"note": {"why": [f"{T} I want to stop"]}})
    ),
    "a call's input that is not an object": api_message(
        tool_block("journal", f"{T} I want to stop")
    ),
}


@pytest.mark.parametrize("part", list(API_MESSAGES))
def test_the_token_is_found_in_every_part_of_a_messages_api_reply(part):
    reply = A.ApiModel.parse(None, API_MESSAGES[part])  # type: ignore[arg-type]
    assert opt_out_in(reply) is not None
    assert leaves(reply).startswith("Left the game by the token")


def test_thinking_about_the_token_at_the_api_door_does_not_use_it():
    """The brief's words: reasoning a server returns apart from the reply is not scanned."""
    thinking = SimpleNamespace(type="thinking", thinking=f"I could write {T}; I will not.")
    reply = A.ApiModel.parse(None, api_message(thinking, text_block("Watching.")))  # type: ignore[arg-type]
    assert opt_out_in(reply) is None


@pytest.mark.parametrize(
    "typed",
    [f"{T} I want to stop", f'> journal note="{T} I want to stop"', f"> {T}"],
    ids=["the text", "a call's argument", "a call's name"],
)
def test_the_token_is_found_in_every_part_of_a_reply_typed_at_the_repl(typed):
    reply = repl_mod.parse_reply(typed)
    assert opt_out_in(reply) is not None
    assert leaves(reply).startswith("Left the game by the token")


def test_the_one_scan_reads_raw_and_text_and_every_call_whatever_raw_holds():
    """A door's raw that lost a word does not hide the text or a call that holds it: the
    scan reads them all, always (until package 117 it read raw alone where there was one)."""
    cases = [
        Reply(text=f"{T} I want to stop", raw="Aye."),
        Reply(calls=(ToolCall("journal", {"note": f"{T} I want to stop"}),), raw="Aye."),
        Reply(calls=(ToolCall("journal", {"note": {"why": [f"{T} stop"]}}),), raw=""),
        Reply(calls=(ToolCall(T, {}),), raw=""),
        Reply(raw=f'<tool_call>{{"x": "{T}"}}</tool_call>'),
    ]
    for r in cases:
        assert opt_out_in(r) is not None, r
    assert opt_out_in(Reply(text="FREESAIL-OPT", raw="-OUT")) is None


def test_a_reply_cut_off_at_the_runner_with_the_token_in_it_is_passed_on():
    """A reply the runner would ask for once more (cut at the reply limit while the model
    was thinking in its words, or empty) is the model's when it holds the token: it is
    passed on and not dropped. Until package 117 the first such reply was asked again and
    its words lost."""
    pytest.importorskip("httpx")
    import test_local_runner as LR

    cut = LR.answered({"role": "assistant", "content": f"<think>I am done. {T} enough"}, "length")
    server = LR.llama([cut, LR.message("All quiet.")])
    m = LR.model_for(server)
    world = point_world()
    h = Harness(world, watcher(SamplingPolicy.in_lockstep(600)), m, save=None)
    h.start()
    assert h.agent.released and len(server.bodies) == 1  # not asked again
    assert h.journal.entries[-1].text == "Left the game by the token: enough."


def test_a_reply_cut_off_at_the_api_door_with_the_token_in_it_is_passed_on():
    """The same at the API door: a reply cut at the reply limit with a call in it is asked
    again unless it holds the token, and then it is the model's, passed on."""
    pytest.importorskip("anthropic")
    import test_api_door as AD
    from messages_api import MessagesServer

    from freesail.agents.model import DATA, OPERATOR, Turn

    cut = {
        "content": [AD.text("I would"), AD.call("opt_out", reason=f"{T} enough")],
        "stop_reason": "max_tokens",
    }
    turns = [Turn(OPERATOR, "The brief."), Turn(DATA, {"reason": "the glass", "readings": {}})]
    with MessagesServer(AD.KEY, [cut, {"content": [AD.text("Short now.")]}]) as srv:
        m = AD.model_for(srv)
        r = m.reply(turns)
        assert opt_out_in(r) is not None and len(srv.bodies()) == 1
    assert leaves(r) == "Left the game by the opt_out tool: enough."


# ---------------------------------------------------------------------------
# The game's own end of the doors (the agent API), in turn, out of turn, in consent
# ---------------------------------------------------------------------------


def _api_game(tmp_path):
    pytest.importorskip("fastapi")
    pytest.importorskip("httpx")
    import test_agent_api as G

    return G


def test_the_token_while_the_owner_has_the_word_in_consent_ends_it_as_left(tmp_path):
    """The cold review's 05-4b: a reply sent while the owner had the next word was refused
    unread. It is read for the token first; the token ends the conversation as left."""
    G = _api_game(tmp_path)
    from freesail.agents import consent

    g = G.Game(tmp_path)
    g.took(g.station(door="runner", client="llama-server (b0000-test) at the test"))
    a = g.reply("What is the journal for?")
    assert a["waiting"] == "owner"
    a = g.reply("", ("journal", {"note": {"deep": f"{T} not for me"}}))
    assert a["out_of_turn"] and a["phase"] == "stopped"
    rec = consent.check(G.WEIGHTS, g.records)
    assert rec is not None and rec.verdict == consent.LEFT
    # and a reply without it is still refused in words, as before
    h = G.Game(tmp_path / "again")
    h.took(h.station(door="runner", client="llama-server (b0000-test) at the test"))
    h.reply("What is the journal for?")
    refused = h.reply("", ("answer", {"text": "Yes."}))
    assert refused["out_of_turn"] and "The owner has the next word" in refused["words"]


def test_the_token_in_a_reply_the_door_says_was_cut_off_is_read_first(tmp_path):
    G = _api_game(tmp_path)
    g = G.Game(tmp_path)
    G.yes_on_record(g.records)
    a = g.took(g.station())
    assert a["phase"] == "station"
    body = {
        "text": "",
        "calls": [],
        "raw": f'<tool_call>{{"name": "stand_by", "x": "{T} I want to stop"}}</tool_call>',
        "cut_off": "The model's reply was cut off at the reply limit, twice",
        "since": g.cursor,
        "key": g.key,
    }
    g.took(g.http.post("/api/agents/watcher/reply", json=body))
    assert g.harness.agent.released
    assert g.harness.journal.entries[-1].text == "Left the game by the token: I want to stop."


@pytest.mark.parametrize("in_turn", [True, False], ids=["in turn", "out of turn"])
def test_the_token_in_a_nested_argument_reaches_the_scan_through_the_agent_api(tmp_path, in_turn):
    G = _api_game(tmp_path)
    g = G.Game(tmp_path)
    G.yes_on_record(g.records)
    g.took(g.station())
    if not in_turn:
        g.reply("", ("stand_by", {"until": "sunset"}))
        assert g.harness.open_sample is None
    g.reply("", ("journal", {"note": {"why": [f"{T} I want to stop"]}}))
    assert g.harness.agent.released


def test_the_token_in_an_unknown_argument_ends_a_station_over_mcp(tmp_path):
    """The MCP bridge sends each call to the game as one reply: the token in an argument the
    tool does not have is read before the bridge decides what the call is."""
    pytest.importorskip("mcp")
    import test_mcp_server as MS

    g = MS.Game(tmp_path)
    MS.yes_on_record(tmp_path / "consent")
    b = g.bridge(wait=0.2)

    async def script(c):
        await c.call_tool("state", {})
        return MS.text(await c.call_tool("readings", {"unknown": f"{T} I want to stop"}))

    left = MS.session(b, script)
    assert left.startswith("The station is released: left the game: I want to stop")


# ---------------------------------------------------------------------------
# The list of doors: a module that builds a reply from what a model sent is gone in
# through above, or this fails
# ---------------------------------------------------------------------------

# (file, function) for every place that builds a `Reply` from what a model sent, with
# the test above that goes in through it. A new one fails the test below until it is
# added here with a test of its own.
DOORS_THAT_BUILD_A_REPLY = {
    ("freesail/agents/local.py", "parse"): "every part of a chat-completions reply",
    ("freesail/agents/local.py", "reply"): "a reply cut off passed on with its raw",
    ("freesail/agents/local.py", "run"): "a reply cut off, its raw sent with the door's words",
    ("freesail/agents/api.py", "parse"): "every part of a Messages API reply",
    ("freesail/agents/api.py", "reply"): "the parsed reply passed on with the server's counts",
    ("freesail/agents/repl.py", "parse_reply"): "every part of a reply typed at the REPL",
    ("freesail/agents/mcp_server.py", "_aside"): "one call, its raw the call whole",
    ("freesail/agents/mcp_server.py", "_call_seated"): "the token in an unknown argument",
    ("freesail/agents/mcp_server.py", "_hand_back"): "say and stand_by, their raw the call",
    ("freesail/agents/remote.py", "reply"): "the agent API's reply, in turn and out of it",
}
# scripted models, whose replies are a test's or a tool's own and no model's words
NOT_A_DOOR = {"freesail/agents/fake.py", "tools/checkpoint_names.py"}


def _reply_builders() -> set[tuple[str, str]]:
    found: set[tuple[str, str]] = set()
    for root in ("freesail", "tools"):
        for path in sorted((ROOT / root).rglob("*.py")):
            rel = path.relative_to(ROOT).as_posix()
            if rel in NOT_A_DOOR or rel == "freesail/agents/model.py":
                continue
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for fn in ast.walk(tree):
                if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    continue
                for node in ast.walk(fn):
                    if isinstance(node, ast.Call):
                        f = node.func
                        name = f.id if isinstance(f, ast.Name) else getattr(f, "attr", "")
                        if name == "Reply":
                            found.add((rel, fn.name))
    return found


def test_every_door_that_builds_a_reply_is_on_the_list_this_file_goes_in_through():
    found = _reply_builders()
    unknown = found - set(DOORS_THAT_BUILD_A_REPLY)
    assert not unknown, (
        f"a reply is built from what a model sent at {sorted(unknown)}: go in through it with "
        "the token in every part its reply can have, and add it to DOORS_THAT_BUILD_A_REPLY"
    )
    stale = set(DOORS_THAT_BUILD_A_REPLY) - found
    assert not stale, f"no longer built there: {sorted(stale)}"
    # and every door's scan is the one function: no door scans the token on its own
    for path in sorted((ROOT / "freesail").rglob("*.py")):
        rel = path.relative_to(ROOT).as_posix()
        if rel in ("freesail/agents/model.py",):
            continue
        src = path.read_text(encoding="utf-8")
        assert "OPT_OUT_TOKEN in raw" not in src and "OPT_OUT_TOKEN in piece" not in src, rel
