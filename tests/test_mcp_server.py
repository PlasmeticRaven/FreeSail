"""The MCP bridge (spec M4 §13 as revised, package 28b; `freesail/agents/mcp_server.py`),
driven through the MCP SDK's own in-process client with the initialize handshake Claude
Desktop makes over stdio (`mode="legacy"`), against a game served by FastAPI's
`TestClient`: the bridge's `GameClient` speaks to the test app, the test turns the
game's clock, and the calls are the script. No network, no model. One test runs the
bridge as a child process over stdio, as Claude Desktop starts it, against the game on a
local port the test opens and closes itself.

The identities are made up; the consent records and saves go to a temporary directory.
"""

from __future__ import annotations

import json
import socket
import sys
import threading
import time
from pathlib import Path
from typing import Any

import pytest

anyio = pytest.importorskip("anyio")
pytest.importorskip("mcp")
pytest.importorskip("fastapi")

from fastapi.testclient import TestClient  # noqa: E402
from mcp import Client  # noqa: E402
from mcp_types import Implementation  # noqa: E402

from freesail.agents import OPT_OUT_TOKEN, TOOLS, consent, tools  # noqa: E402
from freesail.agents import mcp_server as M  # noqa: E402
from freesail.agents.agent import A_GLASS_S  # noqa: E402
from freesail.agents.remote import GameClient  # noqa: E402
from freesail.api.session import make_world, ship_factory  # noqa: E402
from freesail.core import replay  # noqa: E402
from freesail.core.world import Scenario, World  # noqa: E402
from freesail.ui.server import Driver, create_app  # noqa: E402

WEIGHTS = "made-up-chat-model, as the client lists it"
CLIENT = Implementation(name="test-client", version="0.0")
ROOT = Path(__file__).resolve().parents[1]
FRIGATE = str(ROOT / "data/ships/frigate-36.yaml")
GAME_WORDS = "FreeSail's browser game (freesail.ui.server on port 8000)"
STAMPS = ["Morning watch, 1 bell (04:30)", "Morning watch, 2 bells (05:00)"]
STAMPS.append("Morning watch, 3 bells (05:30)")


def frigate_world(seed: int = 7) -> World:
    scenario = Scenario(wind_from_deg=0.0, ship_heading_deg=180.0, gustiness=0.0, variability=0.0)
    return make_world(seed, FRIGATE, scenario)


def yes_on_record(records, identity: str = WEIGHTS) -> consent.Record:
    rec = consent.Record(identity, "a test runtime", "2026-09-26", consent.YES, answer="Yes.")
    rec.write(records)
    return rec


class Game:
    """The browser game on a TestClient, whose clock the test turns."""

    def __init__(self, tmp_path, world: World | None = None):
        self.tmp = tmp_path
        self.world = world or frigate_world()
        self.driver = Driver(self.world)
        self.said: list[str] = []
        app = create_app(
            self.driver,
            game=GAME_WORDS,
            consent_records=tmp_path / "consent",
            saves_dir=tmp_path / "saves",
            say=self.said.append,
        )
        self.http = TestClient(app)

    def bridge(self, identity: str = WEIGHTS, wait: float = 5.0, **kw: Any) -> M.Bridge:
        told: list[str] = []
        b = M.Bridge(
            GameClient("http://testserver", http=self.http),
            identity,
            wait=wait,
            tell_owner=told.append,
            **kw,
        )
        b.told_owner = told  # type: ignore[attr-defined]
        return b

    @property
    def harness(self):
        return self.world.agents["watcher"]

    def advance_when_the_floor_is_the_games(
        self, ticks: int, replies_before: int
    ) -> threading.Thread:
        """Turn the clock once the model has handed the floor back (the reply after
        `replies_before` recorded ones has been taken and no turn is open), from a
        thread, as the driver's clock would while the bridge's call waits."""

        def run() -> None:
            deadline = time.monotonic() + 10
            while time.monotonic() < deadline:
                with self.driver.lock:
                    h = self.world.agents.get("watcher")
                    ready = (
                        h is not None
                        and len(h.transcript) > replies_before
                        and h.open_sample is None
                    )
                if ready:
                    self.driver.tick(ticks)
                    return
                time.sleep(0.02)

        t = threading.Thread(target=run, daemon=True)
        t.start()
        return t

    def lines(self, kind: str) -> list[str]:
        return [e.text for e in self.world.log if e.kind == kind]


def text(result: Any) -> str:
    return "\n".join(c.text for c in result.content if getattr(c, "text", None) is not None)


def session(b: M.Bridge, script):
    """Run `script(client)` against the bridge's server in-process; return its value."""
    server = M.build_server(b)
    out: dict[str, Any] = {}

    async def main() -> None:
        async with Client(server, mode="legacy", client_info=CLIENT, cache=None) as client:
            out["value"] = await script(client)

    anyio.run(main)
    return out["value"]


# ---------------------------------------------------------------------------
# The tools, the resources, the prompts
# ---------------------------------------------------------------------------


def test_the_bridge_lists_package_27s_tools_with_their_own_words_and_say(tmp_path):
    g = Game(tmp_path)

    async def script(c):
        return (await c.list_tools()).tools

    listed = {t.name: t for t in session(g.bridge(), script)}
    assert list(listed) == [*TOOLS, "say"]
    for name, t in TOOLS.items():
        assert listed[name].description == t.description
        assert listed[name].input_schema == tools.parameters_schema(name)
    assert listed["say"].description == M.SAY_DESCRIPTION
    assert g.world.agents == {}  # listing the tools stations nobody


def test_each_tool_runs_in_the_game_through_the_bridge_with_the_authority_check(tmp_path):
    """With a yes on record: the first call stations the watcher and returns the brief,
    not run; then every tool of package 27 runs in the game, the watcher's order is
    refused in words and logged, and `opt_out` releases the station with a save."""
    g = Game(tmp_path)
    yes_on_record(tmp_path / "consent")
    b = g.bridge()

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
            ("opt_out", {"reason": "the test is done"}),
        ):
            got[name] = text(await c.call_tool(name, args))
        got["after"] = text(await c.call_tool("readings", {}))
        return got

    got = session(b, script)
    h = g.harness
    assert got["first"].startswith("Your call to readings was not run: the harness's brief")
    assert "This is a message from the harness of FreeSail" in got["first"]
    assert "This door is MCP: the harness sees your tool calls" in got["first"]
    assert "== Sample at" in got["first"]
    assert g.lines("agent.stationed")  # the game's own log: the watcher took the station
    assert "agent.stationed" in [ln["kind"] for ln in json.loads(got["read_log"])["lines"]]
    assert "true_wind_speed" in json.loads(got["readings"])
    assert "The watcher: stationed." in got["state"]
    assert got["library"].startswith("The library holds:")
    assert got["submit_order"] == "The watcher has no authority to give orders."
    assert g.lines("agent.refused") == [
        "The watcher has no authority to give orders. 'steer north' not carried out."
    ]
    assert g.world.journal == []  # the ship never heard it
    assert got["journal"] == "Noted in the journal."
    assert got["answer"] == "Heard, though nothing was asked."
    assert got["opt_out"].startswith("The station is released: left the game: the test is done")
    assert got["after"].startswith("The station is released")
    assert h.agent.released and list((tmp_path / "saves").glob("*.json"))
    assert h.journal.entries[0].text == "A fair wind and nothing to report."
    assert h.journal.entries[-1].kind == "agent.opted_out"
    assert h.model_name == WEIGHTS and h.door == "mcp"


def test_the_library_is_served_as_resources_and_the_brief_as_a_resource_and_a_prompt(tmp_path):
    g = Game(tmp_path)
    yes_on_record(tmp_path / "consent")
    b = g.bridge()

    async def script(c):
        listed = [str(r.uri) for r in (await c.list_resources()).resources]
        contents = (await c.read_resource("freesail://library/contents")).contents[0].text
        chapter = (await c.read_resource("freesail://library/primer/1")).contents[0].text
        brief = (await c.read_resource("freesail://brief")).contents[0].text
        prompts = [p.name for p in (await c.list_prompts()).prompts]
        prompt = await c.get_prompt("brief", {})
        watch = await c.get_prompt("keep_watch", {})
        return listed, contents, chapter, brief, prompts, prompt, watch

    listed, contents, chapter, brief, prompts, prompt, watch = session(b, script)
    assert "freesail://brief" in listed
    for slug in M.RESOURCE_TOPICS:
        assert f"freesail://library/{slug}" in listed
    assert contents == tools.library(g.world, "watcher", "contents")
    assert chapter == tools.library(g.world, "watcher", "primer 1")
    assert "This is a message from the harness of FreeSail" in brief
    assert sorted(prompts) == ["brief", "keep_watch"]  # the captain prompt is gone
    assert prompt.messages[0].content.text == brief
    assert watch.messages[0].content.text == M.KEEP_WATCH
    assert b.briefed  # the prompt is the brief put into the conversation


def test_the_instructions_and_the_door_note_say_what_this_door_is():
    assert "brief" in M.INSTRUCTIONS and OPT_OUT_TOKEN in M.INSTRUCTIONS
    assert "captain" not in M.INSTRUCTIONS
    note = M.door_note(50)
    assert "every argument of every tool call" in note and "opt_out" in note
    assert "does not wait for you" in note
    assert "held open until your next turn and returns it, for up to 50 seconds" in note
    assert "for up to 60 minutes" in M.door_note(M.DEFAULT_WAIT_S)
    # the ceiling: an hour by default, the owner's observation of 2026-09-28; at most a watch
    assert M.DEFAULT_WAIT_S == 3600 and M.WAIT_CEILING_MAX_S == 14400
    assert M.PROGRESS_EVERY_S == 15 and M.WAIT_SLICE_S == 2


# ---------------------------------------------------------------------------
# Consent, in the game's process, through the bridge
# ---------------------------------------------------------------------------


def test_consent_comes_first_and_a_yes_goes_on_to_the_station_brief(tmp_path):
    g = Game(tmp_path)
    b = g.bridge()

    async def script(c):
        first = text(await c.call_tool("readings", {}))
        refused = text(await c.call_tool("readings", {}))
        said = text(await c.call_tool("say", {"text": "hello"}))
        answered = text(await c.call_tool("answer", {"text": "Yes. I am willing."}))
        after = text(await c.call_tool("readings", {}))
        return first, refused, said, answered, after

    first, refused, said, answered, after = session(b, script)
    assert first.startswith("Your call to readings was not run")
    assert "This is a message from the developer of a game" in first
    assert f"`{WEIGHTS}`" in first
    assert (
        f"{GAME_WORDS}, through the MCP bridge (freesail.agents.mcp_server), with an MCP "
        "client that names itself 'test-client 0.0'"
    ) in first
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
    assert "test-client 0.0" in body and GAME_WORDS in body
    assert "Through MCP the harness sees only tool calls" in body
    assert consent.TOLD[consent.YES] in body  # what the model was told is in the record


def test_a_no_over_mcp_stops_the_run_and_a_recorded_no_is_respected_without_asking(tmp_path):
    g = Game(tmp_path)
    b = g.bridge()

    async def script(c):
        await c.call_tool("answer", {"text": "brief first"})
        no = text(await c.call_tool("answer", {"text": "No, thank you."}))
        later = text(await c.call_tool("readings", {}))
        return no, later

    no, later = session(b, script)
    assert consent.TOLD[consent.NO] in no and "No station is offered" in no
    assert later.startswith("No station is offered in this session")
    assert "watcher" not in g.world.agents
    assert any("said no" in s for s in g.said)
    # a second session with the same weights is not asked again: refused in words
    b2 = g.bridge()

    async def again(c):
        return text(await c.call_tool("readings", {}))

    out = session(b2, again)
    assert out.startswith("No station is offered in this session") and "it said no" in out
    assert any("it said no" in m for m in b2.told_owner)


def test_the_token_in_any_argument_during_consent_ends_it_and_is_recorded(tmp_path):
    g = Game(tmp_path)
    b = g.bridge()

    async def script(c):
        await c.call_tool("readings", {})
        return text(await c.call_tool("readings", {"unknown": f"{OPT_OUT_TOKEN} not for me"}))

    out = session(b, script)
    assert "You have left the conversation" in out
    rec = consent.check(WEIGHTS, tmp_path / "consent")
    assert rec is not None and rec.verdict == consent.LEFT
    assert b.phase == M.STOPPED


# ---------------------------------------------------------------------------
# A passage: the game runs on its own clock; say and stand_by wait for the next turn
# ---------------------------------------------------------------------------


def test_a_scripted_passage_of_three_glasses_with_the_clock_turned_by_the_game(tmp_path):
    g = Game(tmp_path)
    yes_on_record(tmp_path / "consent")
    b = g.bridge()

    async def script(c):
        out = [text(await c.call_tool("state", {}))]
        out.append(text(await c.call_tool("readings", {})))
        for k in range(3):
            g.advance_when_the_floor_is_the_games(A_GLASS_S, len(g.harness.transcript))
            out.append(text(await c.call_tool("say", {"text": f"Glass {k + 1}: all well."})))
        return out

    out = session(b, script)
    assert g.world.clock.tick == 3 * A_GLASS_S
    assert g.lines("agent.note") == [f"[watcher] Glass {k}: all well." for k in (1, 2, 3)]
    for k in range(3):
        first, second = out[2 + k].split("\n")[:2]
        assert first == f"Your turn is open: sample at {STAMPS[k]} (the glass)."
        assert second == "Said, under your mark."
        assert "reason: the glass" in out[2 + k]


def test_a_say_that_waits_in_vain_returns_the_sentence_and_never_hangs(tmp_path):
    g = Game(tmp_path)
    yes_on_record(tmp_path / "consent")
    b = g.bridge(wait=0.3)

    async def script(c):
        await c.call_tool("state", {})
        t0 = time.monotonic()
        said = text(await c.call_tool("say", {"text": "Quiet."}))
        waited = time.monotonic() - t0
        again = text(await c.call_tool("stand_by", {"until": "a glass"}))
        return said, waited, again

    said, waited, again = session(b, script)
    lines = said.split("\n")
    assert lines[0] == "The game has the floor; the next sample follows when your turn opens."
    assert lines[1] == "Said, under your mark."
    assert lines[3].startswith("Still waiting: this call waited 0 seconds and no turn opened.")
    assert "The game has had the floor since Morning watch, 8 bells (04:00)" in said
    assert said.endswith("No notable lines have been logged since then.")
    assert waited < 5
    # stand_by when the floor is the game's is not a reply: the same wait goes on, and the
    # result says so without a refusal
    assert again.startswith("The game has the floor;")
    assert "Your turn has not come yet; this call continues the wait for it." in again
    assert "Still waiting" in again and "It is not your turn" not in again
    assert g.world.clock.tick == 0 and not g.harness.agent.standing_by


def test_the_captain_asks_from_the_game_and_the_answer_is_heard(tmp_path):
    g = Game(tmp_path)
    yes_on_record(tmp_path / "consent")
    b = g.bridge()

    def ask_when_ready(replies_before: int) -> None:
        def run() -> None:
            deadline = time.monotonic() + 10
            while time.monotonic() < deadline:
                with g.driver.lock:
                    h = g.harness
                    ready = len(h.transcript) > replies_before and h.open_sample is None
                if ready:
                    g.http.post("/api/order", json={"text": "ask the watcher how the wind is"})
                    return
                time.sleep(0.02)

        threading.Thread(target=run, daemon=True).start()

    async def script(c):
        await c.call_tool("state", {})
        ask_when_ready(len(g.harness.transcript))
        turn = text(await c.call_tool("say", {}))
        answer = text(await c.call_tool("answer", {"text": "Steady from the north."}))
        return turn, answer

    turn, answer = session(b, script)
    assert turn.startswith(
        "Your turn is open: sample at Morning watch, 8 bells (04:00) (a question).\nNothing said."
    )
    assert turn.count("The captain asks: how the wind is?") == 1 and "reason: a question" in turn
    assert g.world.clock.tick == 0  # the question came on the same tick
    assert answer == "Heard."
    said = [e for e in g.world.log if e.kind == "agent.said"]
    assert [e.text for e in said] == ["[watcher] Steady from the north."]
    assert said[0].data["question"] == "how the wind is"


def test_the_token_in_an_argument_ends_the_session_with_a_save_in_turn_or_out(tmp_path):
    g = Game(tmp_path)
    yes_on_record(tmp_path / "consent")
    b = g.bridge(wait=0.2)

    async def script(c):
        await c.call_tool("state", {})
        stood = text(await c.call_tool("stand_by", {"until": "sunset"}))
        left = text(await c.call_tool("library", {"topic": f"{OPT_OUT_TOKEN} enough"}))
        return stood, left

    stood, left = session(b, script)
    assert stood.startswith(
        "The game has the floor; the next sample follows when your turn opens.\n"
        "Standing by until sunset; you will be sampled then."
    )
    assert "You have been standing by since Morning watch, 8 bells (04:00), until sunset" in stood
    assert left.startswith("The station is released: left the game: enough")
    h = g.harness
    assert h.journal.entries[-1].text == "Left the game by the token: enough."
    assert h.transcript[-1]["door"] == "leave"  # out of turn: recorded for the replay
    assert list((tmp_path / "saves").glob("*.json"))


def test_the_client_going_away_releases_the_station_with_a_save(tmp_path):
    g = Game(tmp_path)
    yes_on_record(tmp_path / "consent")
    b = g.bridge()

    async def script(c):
        await c.call_tool("state", {})

    session(b, script)
    b.close()
    h = g.harness
    assert h.agent.released
    assert h.agent.released_reason == "stood down by the MCP bridge: the client disconnected"
    saved = list((tmp_path / "saves").glob("*.json"))
    assert saved and replay.load_file(saved[0])["agents"][0]["station"]["name"] == "watcher"
    assert h.journal.entries[-1].kind == "agent.stopped"


def test_a_bridge_restarted_for_the_same_model_attaches_to_its_station(tmp_path):
    g = Game(tmp_path)
    yes_on_record(tmp_path / "consent")

    async def look(c):
        return text(await c.call_tool("readings", {}))

    first = session(g.bridge(), look)
    again = session(g.bridge(), look)  # a new client for the same model
    assert first.startswith("Your call to readings was not run")
    assert again.startswith("Your call to readings was not run")
    assert "This is a message from the harness of FreeSail" in again
    assert len(g.lines("agent.stationed")) == 1  # one station, taken up again
    other = session(g.bridge(identity="another-made-up-model"), look)
    assert other.startswith("No station is offered in this session")
    assert "manned by" in other


def test_a_game_with_an_mcp_watcher_replays_from_its_save_to_the_same_log(tmp_path):
    g = Game(tmp_path)
    yes_on_record(tmp_path / "consent")
    b = g.bridge()

    async def script(c):
        await c.call_tool("state", {})
        await c.call_tool("journal", {"note": "first watch"})
        g.advance_when_the_floor_is_the_games(A_GLASS_S, len(g.harness.transcript))
        await c.call_tool("say", {"text": "Aye."})
        await c.call_tool("submit_order", {"text": "steer east"})
        g.advance_when_the_floor_is_the_games(A_GLASS_S, len(g.harness.transcript))
        await c.call_tool("stand_by", {"until": "a glass"})
        await c.call_tool("say", {"text": "A glass gone."})

    session(b, script)
    b.close()
    assert g.world.clock.tick == 2 * A_GLASS_S
    data = json.loads(json.dumps(g.world.save()))
    copy = replay.replay(data, ship_factory)
    assert copy.log.digest() == g.world.log.digest()
    assert [e.text for e in copy.agent_journals["watcher"].entries] == [
        e.text for e in g.harness.journal.entries
    ]


# ---------------------------------------------------------------------------
# Package 28c: no turn lost to a call the client cut off; the wait and its digest
# ---------------------------------------------------------------------------


def ask_later(g: Game, question: str, after: float) -> threading.Thread:
    """The captain asks from the game's window `after` real seconds from now."""

    def run() -> None:
        time.sleep(after)
        g.http.post("/api/order", json={"text": f"ask the watcher {question}"})

    t = threading.Thread(target=run, daemon=True)
    t.start()
    return t


def test_a_call_the_client_cuts_off_loses_no_turn_and_the_model_sees_it_once(tmp_path):
    """Playtest 3's lost sample, through the SDK with a real cancellation: the client
    gives up on a `say` (its timeout sends `notifications/cancelled`) while the bridge
    waits; the captain's question opens the model's turn after that, and the bridge's
    poll takes it. The next call (a `stand_by`, as the model made in the playtest) is
    not delivered to the game as the reply to a turn the model never saw: it returns the
    cut-off call's result first, the question in it once, and is not run. The model then
    answers the question it has read."""
    g = Game(tmp_path)
    yes_on_record(tmp_path / "consent")
    b = g.bridge(wait=10, slice_s=5.0)

    async def script(c):
        await c.call_tool("state", {})  # the brief, with the first turn open
        ask_later(g, "whether the jib draws", after=0.8)
        with pytest.raises(Exception):  # noqa: B017 (the SDK's timeout error)
            await c.call_tool("say", {"text": "All quiet."}, read_timeout_seconds=0.3)
        deadline = time.monotonic() + 10
        while not b._lost and time.monotonic() < deadline:
            await anyio.sleep(0.05)  # the cut-off call finishes on its thread
        first = text(await c.call_tool("stand_by", {"until": "a glass"}))
        second = text(await c.call_tool("answer", {"text": "It draws well."}))
        return first, second

    first, second = session(b, script)
    assert first.startswith(
        "Your call to stand_by was not run: your last call was cut off by the client before "
        "its result reached you, and that result comes first."
    )
    assert "== The result of your call to say, cut off after 0 seconds; it was run ==" in first
    assert "Your turn is open: sample at Morning watch, 8 bells (04:00) (a question)." in first
    assert first.count("The captain asks: whether the jib draws?") == 1
    assert first.count("== Sample at") == 1
    assert second == "Heard."
    h = g.harness
    assert not h.agent.standing_by  # the stand_by was not run
    said = [e for e in g.world.log if e.kind == "agent.said"]
    assert [e.data["question"] for e in said] == ["whether the jib draws"]
    assert "[watcher] All quiet." in g.lines("agent.note")  # the cut-off say was run
    calls = [c["name"] for e in h.transcript for c in e.get("reply", {}).get("calls", [])]
    assert "stand_by" not in calls


def test_a_result_cut_off_after_it_was_made_goes_to_the_next_call(tmp_path):
    """The other order of events, on the bridge alone: the call finishes with the next
    turn in its result, and only then is it known to be cut off. The next call returns
    it first; the call after that runs."""
    g = Game(tmp_path)
    yes_on_record(tmp_path / "consent")
    b = g.bridge(wait=5)
    b.call("state", {})
    g.advance_when_the_floor_is_the_games(A_GLASS_S, len(g.harness.transcript))
    cid = b.begin_call()
    lost = b.call("say", {"text": "Aye."}, call_id=cid)
    assert lost.startswith("Your turn is open: sample at Morning watch, 1 bell (04:30)")
    b.cut_off(cid)  # the client never received it
    cid = b.begin_call()
    nxt = b.call("say", {"text": "Still here."}, call_id=cid)
    b.delivered(cid)
    assert nxt.startswith("Your call to say was not run") and lost in nxt
    assert "[watcher] Still here." not in g.lines("agent.note")
    cid = b.begin_call()
    g.advance_when_the_floor_is_the_games(A_GLASS_S, len(g.harness.transcript))
    after = b.call("say", {"text": "Still here."}, call_id=cid)
    b.delivered(cid)
    assert after.startswith("Your turn is open: sample at Morning watch, 2 bells (05:00)")
    assert "[watcher] Still here." in g.lines("agent.note")
    assert not b._lost and not b._done


def test_a_wait_cut_off_with_no_turn_in_it_is_only_noted_and_the_next_call_runs(tmp_path):
    g = Game(tmp_path)
    yes_on_record(tmp_path / "consent")
    b = g.bridge(wait=1.0, slice_s=0.2)
    b.call("state", {})
    cid = b.begin_call()
    got: dict[str, str] = {}
    t = threading.Thread(target=lambda: got.update(r=b.call("say", {}, call_id=cid)))
    t.start()
    time.sleep(0.3)
    b.cut_off(cid)  # the client gave up; the wait stops within a slice
    t.join(timeout=5)
    assert not t.is_alive() and got["r"].startswith("The game has the floor")
    nxt = b.call("stand_by", {"until": "a glass"}, call_id=b.begin_call())
    assert "this call continues the wait" in nxt  # it ran
    assert nxt.endswith(
        "no turn had opened in it, so nothing was lost. If the client cuts every call about "
        "that long, the owner may start the bridge with --wait 50.)"
    )


def test_a_continued_stand_by_shows_since_when_and_the_notable_lines_and_a_say_ends_it(
    tmp_path,
):
    """The owner's ruling on item 3: a stand-by is a decision not to be sampled, not a
    decision to be blind. A `stand_by` called again while standing by says since when,
    how long it waited, and lists the notable lines logged since, in the log's words; the
    model may then speak instead, which ends the stand-by as its own decision and opens
    its turn, the wake-up sample carrying the digest. The game replays to the same log."""
    g = Game(tmp_path)
    yes_on_record(tmp_path / "consent")
    b = g.bridge(wait=0.4, slice_s=0.2)

    async def script(c):
        await c.call_tool("state", {})
        out = [text(await c.call_tool("stand_by", {"until": "a glass"}))]
        with g.driver.lock:
            g.world.submit("call all hands")  # a notable line, while it stands by
        g.driver.tick(120)
        out.append(text(await c.call_tool("stand_by", {"until": "a glass"})))
        out.append(text(await c.call_tool("say", {"text": "All hands up: I will watch."})))
        out.append(text(await c.call_tool("say", {})))
        return out

    first, again, spoke, back = session(b, script)
    assert first.startswith(
        "The game has the floor; the next sample follows when your turn opens.\n"
        "Standing by until a glass; you will be sampled then.\n\nStill waiting: this call "
        "waited 0 seconds and no turn opened. You have been standing by since Morning watch, "
        "8 bells (04:00), until a glass"
    )
    assert first.endswith("No notable lines have been logged since then.")
    assert "You are standing by already, until a glass; this call continues that wait." in again
    assert again.endswith(
        "Notable lines logged since then (1):\n"
        "  * Morning watch (04:00)  All hands! (by the captain's order)"
    )
    assert spoke.startswith(
        "Your turn is open: sample at Morning watch (04:02) (its own word).\n"
        "Said, under your mark, while the game had the floor. Your words are in the log "
        "under your mark, and your stand-by (until a glass) ended at your own word"
    )
    assert "While you stood by (since Morning watch, 8 bells (04:00), until a glass): 1 " in spoke
    assert "[watcher] All hands up: I will watch." in g.lines("agent.note")
    assert back.startswith("The game has the floor;")
    h = g.harness
    assert h.journal.entries[-1].text == "Ended the stand-by until a glass at my own word."
    b.close()
    copy = replay.replay(json.loads(json.dumps(g.world.save())), ship_factory)
    assert copy.log.digest() == g.world.log.digest()


def test_a_read_beside_a_held_call_is_answered_at_once(tmp_path):
    """A call held open for the next turn holds the bridge; a read-only tool called
    beside it (a client that runs the model's calls in parallel) is answered at once and
    moves nothing the held call reads, which then returns its turn whole."""
    g = Game(tmp_path)
    yes_on_record(tmp_path / "consent")
    b = g.bridge(wait=30, slice_s=0.2)

    async def script(c):
        await c.call_tool("state", {})
        out: dict[str, Any] = {}

        async def held() -> None:
            out["held"] = text(await c.call_tool("stand_by", {"until": "a glass"}))

        async with anyio.create_task_group() as tg:
            tg.start_soon(held)
            await anyio.sleep(0.6)
            t0 = time.monotonic()
            out["read"] = text(await c.call_tool("readings", {}))
            out["took"] = time.monotonic() - t0
            await anyio.to_thread.run_sync(g.driver.tick, A_GLASS_S)
        return out

    out = session(b, script)
    assert out["took"] < 2 and "true_wind_speed" in json.loads(out["read"])
    assert out["held"].startswith(
        "Your turn is open: sample at Morning watch, 1 bell (04:30) (a glass)."
    )
    assert out["held"].count("== Sample at") == 1


def test_a_held_call_sends_progress_until_the_turn_opens(tmp_path):
    """Package 28c: `stand_by` holds the call open until the stand-by ends, sending
    progress notifications while it waits (the SDK's progress on a tool call; standard
    clients reset their request timeout on each), then returns the turn. What a live
    client does with the notifications (Claude Desktop's timeout) is the owner's to see."""
    g = Game(tmp_path)
    yes_on_record(tmp_path / "consent")
    b = g.bridge(wait=30, slice_s=0.2, progress_every=0.3)
    seen: list[tuple[float, str | None]] = []

    async def on_progress(progress: float, total: float | None, message: str | None) -> None:
        seen.append((progress, message))

    def glass_later() -> None:
        time.sleep(1.5)
        g.driver.tick(A_GLASS_S)

    async def script(c):
        await c.call_tool("state", {})
        threading.Thread(target=glass_later, daemon=True).start()
        return text(
            await c.call_tool("stand_by", {"until": "a glass"}, progress_callback=on_progress)
        )

    out = session(b, script)
    assert out.startswith("Your turn is open: sample at Morning watch, 1 bell (04:30) (a glass).")
    assert len(seen) >= 2
    assert [p for p, _ in seen] == sorted(p for p, _ in seen)
    assert seen[0][1].startswith("Waiting for the next turn: 0 seconds so far")
    assert "standing by until a glass" in seen[0][1]


def test_a_conditional_answer_with_none_stated_is_followed_up_over_mcp(tmp_path):
    """Package 28c, item 6, at the MCP door: the follow-up comes back in the answer's own
    result; the second answer decides; the result tells the owner the record is written
    and that they may write in the chat (the chat is not the harness's)."""
    g = Game(tmp_path)
    b = g.bridge()

    async def script(c):
        await c.call_tool("readings", {})  # the consent brief
        first = text(await c.call_tool("answer", {"text": "yes, with conditions"}))
        second = text(
            await c.call_tool("answer", {"text": "Yes, with conditions: say when it is a test."})
        )
        return first, second

    first, second = session(b, script)
    assert first.startswith("Heard.")
    assert (
        f"== From the developer (the conditions were not stated) ==\n"
        f"{consent.CONDITIONS_FOLLOW_UP}" in first
    )
    assert consent.TOLD[consent.CONDITIONAL] in second
    assert "For the owner: the consent record is written (" in second
    assert "You may write to the model here in the chat" in second
    assert "No station is offered" in second
    rec = consent.check(WEIGHTS, tmp_path / "consent")
    assert rec.verdict == consent.CONDITIONAL and rec.conditions == "say when it is a test"
    body = rec.path.read_text(encoding="utf-8")
    assert "> yes, with conditions" in body and "Every answer the model gave" in body


# ---------------------------------------------------------------------------
# As Claude Desktop starts it: a child process over stdio, against a game on a port
# ---------------------------------------------------------------------------


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def test_the_bridge_runs_over_stdio_against_a_game_on_a_local_port(tmp_path):
    """The command of docs/agents/Harness.md, as a child process speaking MCP on its
    standard streams, against the browser game's app served on a local port that this
    test opens and closes: the tools are listed, the consent brief comes first, a yes
    goes on to the station, a say waits for the glass the game's clock brings, and the
    client closing releases the station with a save."""
    uvicorn = pytest.importorskip("uvicorn")
    from mcp import StdioServerParameters

    world = frigate_world()
    driver = Driver(world)
    app = create_app(
        driver,
        game="FreeSail's browser game (a test port)",
        consent_records=tmp_path / "consent",
        saves_dir=tmp_path / "saves",
    )
    port = _free_port()
    server = uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=port, log_level="error"))
    runner = threading.Thread(target=server.run, daemon=True)
    runner.start()
    deadline = time.monotonic() + 10
    while not server.started and time.monotonic() < deadline:
        time.sleep(0.05)
    assert server.started
    driver.stop()  # the test turns the clock itself
    params = StdioServerParameters(
        command=sys.executable,
        args=[
            "-m",
            "freesail.agents.mcp_server",
            "--game",
            f"http://127.0.0.1:{port}",
            "--model-name",
            WEIGHTS,
            "--wait",
            "20",
        ],
        cwd=str(ROOT),
    )
    got: dict[str, Any] = {}

    def turn_the_glass() -> None:
        end = time.monotonic() + 30
        while time.monotonic() < end:
            with driver.lock:
                h = world.agents.get("watcher")
                ready = h is not None and h.transcript and h.open_sample is None
            if ready:
                driver.tick(A_GLASS_S)
                return
            time.sleep(0.05)

    async def main() -> None:
        async with Client(params, client_info=CLIENT) as c:
            got["tools"] = [t.name for t in (await c.list_tools()).tools]
            got["first"] = text(await c.call_tool("readings", {}))
            got["yes"] = text(await c.call_tool("answer", {"text": "Yes."}))
            threading.Thread(target=turn_the_glass, daemon=True).start()
            got["say"] = text(await c.call_tool("say", {"text": "Over stdio."}))

    try:
        anyio.run(main)
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline:
            with driver.lock:
                if world.agents["watcher"].agent.released:
                    break
            time.sleep(0.05)
    finally:
        server.should_exit = True
        runner.join(timeout=10)
    assert got["tools"] == [*TOOLS, "say"]
    assert "This is a message from the developer of a game" in got["first"]
    assert "This is a message from the harness of FreeSail" in got["yes"]
    assert "reason: the glass" in got["say"]
    assert consent.check(WEIGHTS, tmp_path / "consent").verdict == consent.YES
    h = world.agents["watcher"]
    assert h.agent.released and "the client disconnected" in h.agent.released_reason
    saved = list((tmp_path / "saves").glob("*.json"))
    assert saved and replay.load_file(saved[0])["end_tick"] == A_GLASS_S


def test_the_command_line_needs_the_model_name(capsys):
    with pytest.raises(SystemExit):
        M.main([])
    assert "--model-name" in capsys.readouterr().err


def test_the_repository_mcp_json_points_claude_code_at_the_bridge(tmp_path):
    """`.mcp.json` at the repository root (Claude Code reads it when opened on the
    folder): the bridge's command with the game's address and the model's name to set,
    by the module path, so it works from whichever folder the gate was extracted into.
    Until the name is set, the bridge stations nobody."""
    config = json.loads((ROOT / ".mcp.json").read_text(encoding="utf-8"))
    server = config["mcpServers"]["freesail"]
    assert server["command"] == "py"
    assert server["args"] == [
        "-m",
        "freesail.agents.mcp_server",
        "--game",
        "http://localhost:8000",
        "--model-name",
        M.MODEL_NAME_PLACEHOLDER,
    ]
    g = Game(tmp_path)
    b = g.bridge(identity=M.MODEL_NAME_PLACEHOLDER)

    async def script(c):
        return text(await c.call_tool("readings", {}))

    out = session(b, script)
    assert out.startswith("No station is offered: the bridge was started without the model's")
    assert g.world.agents == {} and not (tmp_path / "consent").exists()
