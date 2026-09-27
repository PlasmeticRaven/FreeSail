"""The MCP server (spec M4 §13, `freesail/agents/mcp_server.py`), driven through the MCP
SDK's own in-process client with the initialize handshake Claude Desktop makes over
stdio (`mode="legacy"`). No network, no model: the test is the client, and its calls are
the script.

The identities are made up; the consent records go to a temporary directory.
"""

from __future__ import annotations

import datetime as dt
import json
from typing import Any

import pytest

anyio = pytest.importorskip("anyio")
pytest.importorskip("mcp")

from mcp import Client  # noqa: E402
from mcp_types import Implementation  # noqa: E402

from freesail.agents import OPT_OUT_TOKEN, TOOLS, consent, tools  # noqa: E402
from freesail.agents import mcp_server as M  # noqa: E402
from freesail.agents.agent import A_GLASS_S  # noqa: E402
from freesail.api.session import make_world, ship_factory  # noqa: E402
from freesail.core import replay  # noqa: E402
from freesail.core.world import Scenario, World  # noqa: E402

WEIGHTS = "made-up-chat-model, as the client lists it"
TODAY = dt.date(2026, 9, 27)
CLIENT = Implementation(name="test-client", version="0.0")
FRIGATE = "data/ships/frigate-36.yaml"


def point_world(seed: int = 7) -> World:
    """The point ship: fast, and without the station sentences (it has no crew or
    stations), so the captain's `ask` needs the frigate."""
    return World(seed=seed, scenario=Scenario(gustiness=0.0, variability=0.0))


def frigate_world(seed: int = 7) -> World:
    scenario = Scenario(wind_from_deg=0.0, ship_heading_deg=180.0, gustiness=0.0, variability=0.0)
    return make_world(seed, FRIGATE, scenario)


def yes_on_record(records, identity: str = WEIGHTS) -> consent.Record:
    rec = consent.Record(identity, "a test runtime", "2026-09-26", consent.YES, answer="Yes.")
    rec.write(records)
    return rec


def door(tmp_path, world: World | None = None, **kw) -> M.Door:
    told: list[str] = []
    d = M.Door(
        world or point_world(),
        kw.pop("identity", WEIGHTS),
        records_dir=tmp_path / "consent",
        saves_dir=tmp_path / "saves",
        today=TODAY,
        tell_owner=told.append,
        **kw,
    )
    d.told_owner = told  # type: ignore[attr-defined]
    return d


def text(result: Any) -> str:
    return "\n".join(c.text for c in result.content if getattr(c, "text", None) is not None)


def session(d: M.Door, script):
    """Run `script(client)` against the door's server in-process; return what it returns."""
    server = M.build_server(d)
    out: dict[str, Any] = {}

    async def main() -> None:
        async with Client(server, mode="legacy", client_info=CLIENT, cache=None) as client:
            out["value"] = await script(client)

    anyio.run(main)
    return out["value"]


# ---------------------------------------------------------------------------
# The tools, the resources, the prompts
# ---------------------------------------------------------------------------


def test_the_server_lists_package_27s_tools_with_their_own_words_and_say(tmp_path):
    yes_on_record(tmp_path / "consent")

    async def script(c):
        return (await c.list_tools()).tools

    listed = {t.name: t for t in session(door(tmp_path), script)}
    assert list(listed) == [*TOOLS, "say"]
    for name, t in TOOLS.items():
        assert listed[name].description == t.description
        assert listed[name].input_schema == tools.parameters_schema(name)
    assert listed["submit_order"].input_schema["required"] == ["text"]
    assert listed["read_log"].input_schema["properties"]["since_tick"]["type"] == "integer"
    assert listed["say"].description == M.SAY_DESCRIPTION


def test_each_tool_runs_through_the_harness_with_the_authority_check(tmp_path):
    """With a yes on record: the first call returns the brief and is not run; then every
    tool of package 27 runs, the watcher's order is refused in words and logged, and
    `opt_out` releases the station with a save."""
    yes_on_record(tmp_path / "consent")
    d = door(tmp_path)

    async def script(c):
        got = {}
        got["first"] = text(await c.call_tool("readings", {}))
        for name, args in (
            ("read_log", {"since_tick": 0, "severity": "routine"}),
            ("readings", {}),
            ("state", {}),
            ("library", {"topic": "contents"}),
            ("submit_order", {"text": "steer north"}),
            ("journal", {"note": "A fair wind and nothing to report."}),
            ("answer", {"text": "Nothing was asked."}),
            ("stand_by", {"until": "a glass"}),
            ("say", {"text": "The wind holds."}),
            ("opt_out", {"reason": "the test is done"}),
        ):
            got[name] = text(await c.call_tool(name, args))
        return got

    got = session(d, script)
    h = d.harness
    assert got["first"].startswith("Your call to readings was not run: the harness's brief")
    assert "This is a message from the harness of FreeSail" in got["first"]
    assert "This door is MCP (Claude Desktop)" in got["first"]
    assert "== Sample at" in got["first"]
    assert "agent.stationed" in [ln["kind"] for ln in json.loads(got["read_log"])["lines"]]
    assert "true_wind_speed" in json.loads(got["readings"])
    assert "The watcher: stationed." in got["state"]
    assert got["library"].startswith("The library holds:")
    assert got["submit_order"] == "The watcher has no authority to give orders."
    assert [e.text for e in d.world.log if e.kind == "agent.refused"] == [
        "The watcher has no authority to give orders. 'steer north' not carried out."
    ]
    assert d.world.journal == []  # the ship never heard it
    assert got["journal"] == "Noted in the journal."
    assert got["answer"] == "Heard, though nothing was asked."
    # stand_by hands the floor back: the World runs a glass to the watcher's next turn
    assert got["stand_by"].startswith("Standing by until a glass")
    assert "== Sample at" in got["stand_by"]
    assert "[watcher] The wind holds." in [e.text for e in d.world.log if e.kind == "agent.note"]
    assert got["opt_out"].startswith("The station is released: left the game: the test is done")
    assert h.agent.released and d.saves and (tmp_path / "saves").is_dir()
    assert h.journal.entries[0].text == "A fair wind and nothing to report."
    assert h.journal.entries[-1].kind == "agent.opted_out"


def test_the_library_is_served_as_resources_and_the_brief_as_a_resource_and_a_prompt(tmp_path):
    yes_on_record(tmp_path / "consent")
    d = door(tmp_path)

    async def script(c):
        listed = [str(r.uri) for r in (await c.list_resources()).resources]
        contents = (await c.read_resource("freesail://library/contents")).contents[0].text
        chapter = (await c.read_resource("freesail://library/primer/1")).contents[0].text
        brief = (await c.read_resource("freesail://brief")).contents[0].text
        prompts = [p.name for p in (await c.list_prompts()).prompts]
        prompt = await c.get_prompt("brief", {})
        return listed, contents, chapter, brief, prompts, prompt.messages[0].content.text

    listed, contents, chapter, brief, prompts, prompt = session(d, script)
    assert "freesail://brief" in listed
    for slug in M.RESOURCE_TOPICS:
        assert f"freesail://library/{slug}" in listed
    assert contents == tools.library(d.world, "watcher", "contents")
    assert chapter == tools.library(d.world, "watcher", "primer 1")
    assert brief.startswith("This is a message from the harness of FreeSail")
    assert sorted(prompts) == ["brief", "captain"]
    assert prompt == brief
    assert d.briefed  # the prompt is the brief put into the conversation


def test_the_instructions_say_the_brief_comes_first_and_the_token_counts_in_any_argument():
    assert "brief" in M.INSTRUCTIONS and OPT_OUT_TOKEN in M.INSTRUCTIONS
    assert "every argument of every tool call" in M.MCP_DOOR_NOTE
    assert "opt_out" in M.MCP_DOOR_NOTE


# ---------------------------------------------------------------------------
# Consent through the MCP door
# ---------------------------------------------------------------------------


def test_consent_comes_first_and_a_yes_goes_on_to_the_station_brief(tmp_path):
    d = door(tmp_path)

    async def script(c):
        first = text(await c.call_tool("readings", {}))
        refused = text(await c.call_tool("readings", {}))
        said = text(await c.call_tool("say", {"text": "hello"}))
        answered = text(await c.call_tool("answer", {"text": "Yes. I am willing."}))
        after = text(await c.call_tool("readings", {}))
        return first, refused, said, answered, after

    first, refused, said, answered, after = session(d, script)
    assert first.startswith("Your call to readings was not run")
    assert "This is a message from the developer of a game" in first
    assert f"`{WEIGHTS}`" in first and "test-client 0.0" in first
    assert consent.DOOR_TEXT["mcp"] in first
    assert "== From the developer (the consent question) ==" in first
    assert refused.startswith("There is no tool named 'readings' in this conversation")
    assert refused.endswith("the tools here are opt_out and answer.")
    assert said.startswith("There is no tool named 'say' in this conversation")
    assert "Heard." in answered and consent.TOLD[consent.YES] in answered
    assert "This is a message from the harness of FreeSail" in answered  # the station brief
    assert "true_wind_speed" in json.loads(after)
    rec = consent.check(WEIGHTS, tmp_path / "consent")
    assert rec is not None and rec.verdict == consent.YES
    body = rec.path.read_text(encoding="utf-8")
    assert "the client names itself 'test-client 0.0'" in body or "test-client 0.0" in body
    assert "Through MCP the harness sees only tool calls" in body
    assert consent.TOLD[consent.YES] in body  # what the model was told is in the record


def test_a_no_over_mcp_stops_the_run_and_a_recorded_no_is_respected_without_asking(tmp_path):
    d = door(tmp_path)

    async def script(c):
        await c.call_tool("answer", {"text": "brief first"})
        no = text(await c.call_tool("answer", {"text": "No, thank you."}))
        later = text(await c.call_tool("readings", {}))
        return no, later

    no, later = session(d, script)
    assert consent.TOLD[consent.NO] in no
    assert later.startswith("No station is offered in this session")
    assert d.harness is None and "watcher" not in d.world.agents
    assert any("said no" in m for m in d.told_owner)
    # a second session with the same weights is not asked again
    d2 = door(tmp_path)

    async def again(c):
        return text(await c.call_tool("readings", {}))

    assert again and session(d2, again).startswith("No station is offered")
    assert d2.conv is None


def test_the_token_in_any_argument_during_consent_ends_it_and_is_recorded(tmp_path):
    d = door(tmp_path)

    async def script(c):
        await c.call_tool("readings", {})
        return text(await c.call_tool("readings", {"unknown": f"{OPT_OUT_TOKEN} not for me"}))

    out = session(d, script)
    assert "You have left the conversation" in out
    rec = consent.check(WEIGHTS, tmp_path / "consent")
    assert rec is not None and rec.verdict == consent.LEFT
    assert d.phase == M.STOPPED


# ---------------------------------------------------------------------------
# The World advances only with the model; the passage; the captain
# ---------------------------------------------------------------------------


def passage(tmp_path, glasses: int = 3) -> tuple[M.Door, list[str]]:
    """A scripted passage: the brief, a look at the readings, then `say` each glass."""
    d = door(tmp_path)
    yes_on_record(tmp_path / "consent")

    async def script(c):
        out = [text(await c.call_tool("state", {}))]
        out.append(text(await c.call_tool("readings", {})))
        for k in range(glasses):
            out.append(text(await c.call_tool("say", {"text": f"Glass {k + 1}: all well."})))
        return out

    return d, session(d, script)


def test_a_scripted_passage_of_three_glasses_runs_in_lockstep_and_deterministically(tmp_path):
    d, out = passage(tmp_path / "a")
    assert d.world.clock.tick == 3 * A_GLASS_S
    notes = [e.text for e in d.world.log if e.kind == "agent.note"]
    assert notes == [f"[watcher] Glass {k}: all well." for k in (1, 2, 3)]
    for k in range(3):
        assert "reason: the glass" in out[2 + k]
    d2, out2 = passage(tmp_path / "b")
    assert d2.world.log.digest() == d.world.log.digest()
    assert out2[2:] == out[2:]


def test_the_world_never_runs_but_when_the_model_hands_the_floor_back(tmp_path):
    yes_on_record(tmp_path / "consent")
    d = door(tmp_path)

    async def script(c):
        await c.call_tool("state", {})
        for _ in range(5):
            await c.call_tool("readings", {})
            await c.call_tool("journal", {"note": "reading"})
        return d.world.clock.tick

    assert session(d, script) == 0


def test_the_captain_asks_through_the_prompt_and_the_answer_is_heard(tmp_path):
    yes_on_record(tmp_path / "consent")
    d = door(tmp_path, frigate_world())

    async def script(c):
        await c.call_tool("state", {})
        asked = await c.get_prompt("captain", {"order": "ask the watcher how the wind is"})
        waiting = asked.messages[0].content.text
        turn = text(await c.call_tool("say", {}))
        answer = text(await c.call_tool("answer", {"text": "Steady from the north."}))
        state = (await c.get_prompt("captain", {"order": "state"})).messages[0].content.text
        down = await c.get_prompt("captain", {"order": "stand down the watcher"})
        after = text(await c.call_tool("readings", {}))
        return waiting, turn, answer, state, down.messages[0].content.text, after

    waiting, turn, answer, state, down, after = session(d, script)
    assert waiting.startswith("The captain's order waits until the watcher hands the floor back")
    assert "The captain asks: how the wind is?" in turn and "reason: a question" in turn
    assert d.world.clock.tick == 0  # the question came on the same tick
    assert answer == "Heard."
    said = [e for e in d.world.log if e.kind == "agent.said"]
    assert [e.text for e in said] == ["[watcher] Steady from the north."]
    assert said[0].data["question"] == "how the wind is"
    assert "The watcher:" in state
    assert "The watcher stood down by the captain" in down
    assert after.startswith("The station is released: stood down by the captain")
    assert d.saves


def test_an_mcp_game_replays_from_its_save_to_the_same_log(tmp_path):
    """The model's calls are replies delivered into its turns and the captain's orders
    wait for the floor, so the save replays: the recorded replies are played back at the
    same samples and the journaled orders at the same ticks."""
    yes_on_record(tmp_path / "consent")
    d = door(tmp_path, frigate_world())

    async def script(c):
        await c.call_tool("state", {})
        await c.call_tool("journal", {"note": "first watch"})
        await c.get_prompt("captain", {"order": "ask the watcher how she goes"})
        await c.call_tool("say", {"text": "Aye."})
        await c.call_tool("answer", {"text": "Easily."})
        await c.call_tool("submit_order", {"text": "steer east"})
        await c.call_tool("say", {"text": "A glass gone."})
        await c.call_tool("stand_by", {"until": "a glass"})
        await c.call_tool("say", {})

    session(d, script)
    assert [e.text for e in d.world.log if e.kind == "agent.said"] == ["[watcher] Easily."]
    data = d.world.save()
    copy = replay.replay(json.loads(json.dumps(data)), ship_factory)
    # the question at 04:00, the say to 04:30, a glass stood by to 05:00, the say to 05:30
    assert copy.clock.tick == d.world.clock.tick == 3 * A_GLASS_S
    assert copy.log.digest() == d.world.log.digest()
    assert [e.text for e in copy.agent_journals["watcher"].entries] == [
        e.text for e in d.harness.journal.entries
    ]


def test_the_client_going_away_stands_the_watcher_down_with_a_save(tmp_path):
    yes_on_record(tmp_path / "consent")
    d = door(tmp_path)

    async def script(c):
        await c.call_tool("state", {})

    session(d, script)
    d.close()
    assert d.harness.agent.released
    assert "the client disconnected" in d.harness.agent.released_reason
    assert d.saves and replay.load_file(d.saves[-1])["agents"][0]["station"]["name"] == "watcher"
    assert d.harness.journal.entries[-1].kind == "agent.stopped"


def test_the_token_out_of_turn_still_ends_the_session(tmp_path):
    yes_on_record(tmp_path / "consent")
    d = door(tmp_path, advance_limit=600)

    async def script(c):
        await c.call_tool("state", {})
        waited = text(await c.call_tool("stand_by", {"until": "sunset"}))
        left = text(await c.call_tool("library", {"topic": f"{OPT_OUT_TOKEN} enough"}))
        return waited, left

    waited, left = session(d, script)
    assert "your turn has not come" in waited and "standing by until sunset" in waited
    assert left.startswith("The station is released: left the game: enough")
    assert d.harness.journal.entries[-1].text == "Left the game by the token: enough."


def test_the_server_runs_over_stdio_as_claude_desktop_starts_it(tmp_path):
    """The command of docs/agents/Harness.md, as a child process speaking MCP on its
    standard streams: the tools are listed, the consent brief comes first, a yes goes on
    to the station, and the client closing stands the watcher down with a save."""
    import sys
    from pathlib import Path

    from mcp import StdioServerParameters

    root = Path(__file__).resolve().parents[1]
    params = StdioServerParameters(
        command=sys.executable,
        args=[
            "-m",
            "freesail.agents.mcp_server",
            "--model-name",
            WEIGHTS,
            "--seed",
            "7",
            "--records",
            str(tmp_path / "consent"),
            "--save",
            str(tmp_path / "game.json"),
        ],
        cwd=str(root),
    )
    got: dict[str, Any] = {}

    async def main() -> None:
        async with Client(params, client_info=CLIENT) as c:
            got["tools"] = [t.name for t in (await c.list_tools()).tools]
            got["first"] = text(await c.call_tool("readings", {}))
            got["yes"] = text(await c.call_tool("answer", {"text": "Yes."}))
            got["say"] = text(await c.call_tool("say", {"text": "Over stdio."}))

    anyio.run(main)
    assert got["tools"] == [*TOOLS, "say"]
    assert "This is a message from the developer of a game" in got["first"]
    assert "This is a message from the harness of FreeSail" in got["yes"]
    assert "reason: the glass" in got["say"]
    assert consent.check(WEIGHTS, tmp_path / "consent").verdict == consent.YES
    saved = replay.load_file(tmp_path / "game.json")
    assert saved["end_tick"] == A_GLASS_S
    assert saved["agent_journals"]["watcher"][-1]["kind"] == "agent.stopped"


def test_the_command_line_needs_the_model_name(capsys):
    with pytest.raises(SystemExit):
        M.main(["data/ships/frigate-36.yaml"])
    assert "--model-name" in capsys.readouterr().err
