"""The regatta (spec M6 §21; package 44, `tools/regatta.py`; truth 90): a course read and
its places found on the chart; the judge's marks and line from the truth; the score, the
run's log and row and the date's table, which name no model; a short course sailed by the
rules-based captain and by the scripted captain at lockstep; a model through the local
runner's door and the API door (against a fake model server and the fake Messages server,
never a model), seated only with its consent on record and refused in words without it;
a human's game replayed and judged; and, slow, the first course sailed by the rules-based
captain and the fake, both scored, the rules-based captain's run replaying to its digest.

The identities are made up; the consent records, the runs and the saves go to a temporary
folder.
"""

from __future__ import annotations

import io
import json
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

import regatta as RG  # noqa: E402

from freesail.agents import consent  # noqa: E402
from freesail.core.events import Severity  # noqa: E402
from freesail.world.geo import Position  # noqa: E402

COURSES = sorted((ROOT / "data" / "regatta").glob("*.yaml"))
FIRST = ROOT / "data" / "regatta" / "ushant-to-falmouth.yaml"
GGUF = "Made-Up-Model-7B-Q4_K_M.gguf"

# A short course for the fast tests: the passage's start off Ushant, a line a mile and a
# half to the northward with a half-mile radius, an hour to reach it.
SHORT = """\
name: A short course off Ushant
scenario: data/scenarios/gate-5b-passage.yaml
seed: 7
start_orders: [set plain sail]
standing_orders: []
finish: {at: 48 31.5 N 5 02 W, radius_nm: 0.5}
time_limit_hours: 1
marks: []
intent: bound for Falmouth
fake:
  first: [steer N, trim sails]
  each_glass: [trim sails]
"""


@pytest.fixture
def short_course(tmp_path):
    p = tmp_path / "short-course.yaml"
    p.write_text(SHORT)
    return RG.load_course(p)


def test_every_course_reads_and_says_its_start_finish_limit_and_agents():
    """The three courses of the first table: each names its scenario, a finish with a
    radius, a limit, the rules-based captain's intent and the fake's orders."""
    assert {p.stem for p in COURSES} >= {
        "ushant-to-falmouth",
        "falmouth-to-bertheaume",
        "falmouth-to-funchal",
    }
    for p in COURSES:
        c = RG.load_course(p)
        assert (ROOT / c.scenario).exists(), c.scenario
        assert c.radius_nm > 0 and c.time_limit_s > 0
        assert c.intent and c.fake["first"], p
    funchal = RG.load_course(ROOT / "data" / "regatta" / "falmouth-to-funchal.yaml")
    assert [m.name for m in funchal.marks] == ["Ushant", "Cape Finisterre"]
    assert "funchal" in (funchal.ports or [])


def test_a_course_may_be_sailed_in_another_ship(short_course):
    """`ship:` in the course (or `--ship` for one run) puts another ship file on the same
    course, so that a new hull sails it beside the others."""
    course = RG.load_course(short_course.path)
    course.ship = "data/ships/cutter.yaml"
    world = RG.course_world(course)
    assert world.ship.save_ref()["path"].endswith("cutter.yaml")
    assert RG.course_world(short_course).ship.save_ref()["path"].endswith("frigate-36.yaml")


def test_a_course_file_without_its_finish_is_refused_in_words(tmp_path):
    p = tmp_path / "bad.yaml"
    p.write_text("name: x\nscenario: data/scenarios/gate-5b-passage.yaml\ntime_limit_hours: 1\n")
    with pytest.raises(RG.CourseError, match="says its finish"):
        RG.load_course(p)


def _world_at(lat: float, lon: float, tick: int = 0) -> Any:
    return SimpleNamespace(
        position=Position(lat, lon),
        clock=SimpleNamespace(tick=tick),
        ship=SimpleNamespace(extra={}),
    )


def test_the_judge_rounds_a_mark_when_her_track_crosses_its_line_and_then_finishes():
    """A mark is rounded when her track crosses the line laid from it to seaward, and only
    then does the finish count; a ship that passes inside the mark (between it and the
    land, the other side of the line's origin) has not rounded it."""
    course = RG.Course(
        id="t",
        path="t",
        name="t",
        scenario="",
        seed=7,
        start={},
        ports=None,
        start_orders=[],
        standing_orders=[],
        finish_at="",
        finish=Position(47.0, -5.0),
        radius_nm=1.0,
        time_limit_s=10_000,
        marks=[RG.Mark("the rock", Position(48.0, -5.0), 270.0, 10.0)],
        intent="",
        fake={"first": [], "each_glass": []},
    )
    # sailing south a mile inside (east of) the rock: the line, laid west, is not crossed
    w = _world_at(48.2, -4.97)
    judge = RG.Judge(course, w)
    for i, lat in enumerate((48.1, 48.0, 47.9, 47.2, 47.0)):
        w.position, w.clock.tick = Position(lat, -4.97), i + 1
        judge.tick(w)
    assert judge.rounded == [] and not judge.done
    # outside it, five miles to the west: rounded, and then the line
    w = _world_at(48.2, -5.12)
    judge = RG.Judge(course, w)
    for i, (lat, lon) in enumerate(((48.1, -5.12), (47.9, -5.12), (47.3, -5.0), (47.01, -5.0))):
        w.position, w.clock.tick = Position(lat, lon), i + 1
        judge.tick(w)
    assert judge.rounded == [("the rock", 2)] and judge.finished_tick == 4
    # a time limit ends the run whether or not she is in
    assert RG.Judge(course, _world_at(48.0, -6.0, 10_000)).tick(_world_at(48.0, -6.0, 10_000))


def test_the_short_course_under_the_rules_and_the_fake_scores_both_and_writes_the_table(
    short_course, tmp_path
):
    """The rules-based captain and the scripted captain sail the short course at lockstep
    and finish; each run writes its log and row, the date's table names both by kind and
    door, finishers first, and the save of each replays to the run's digest."""
    from freesail.api.session import ship_factory
    from freesail.core import replay

    runs = tmp_path / "runs" / "2026-10-16"
    saves = tmp_path / "saves"
    said: list[str] = []
    rows = []
    for agent, run in (("rules", RG.run_rules), ("fake", RG.run_fake)):
        world, judge = run(short_course, say=said.append)
        assert judge.done and judge.finished_tick < 3600, agent
        row = RG.score(short_course, world, judge, agent)
        assert row["finished"] and row["elapsed"].endswith(" m") and row["groundings"] == []
        RG.write_run(runs, row, world, saves_dir=saves)
        rows.append(row)
        save = Path(row["save"]) if Path(row["save"]).is_absolute() else ROOT / row["save"]
        data = replay.load_file(save)
        assert replay.replay(data, ship_factory).log.digest()[:16] == row["digest"], agent
    table = (runs / "table.md").read_text()
    assert "## A short course off Ushant" in table
    assert "the rules-based captain" in table and "the scripted captain" in table
    assert (runs / "short-course" / "rules.log").read_text().startswith("# A short course")
    assert json.loads((runs / "short-course" / "fake.json").read_text())["agent"] == "fake"
    # a second run of the same agent the same day is kept beside the first
    world, judge = RG.run_fake(short_course, say=said.append)
    RG.write_run(runs, RG.score(short_course, world, judge, "fake"), world, saves_dir=saves)
    assert (runs / "short-course" / "fake-2.json").exists()


def test_a_model_is_named_by_its_kind_and_door_never_by_its_name(short_course, tmp_path):
    """The row and the log put a model's name as its kind of agent: the repository names
    no model (the package's rule)."""
    world, judge = RG.run_fake(short_course, say=lambda w: None)
    world.record(Severity.ROUTINE, "agent.note", f"[captain] {GGUF}: well.", actor="the captain")
    row = RG.score(short_course, world, judge, "local", identity=GGUF)
    runs = tmp_path / "runs" / "2026-10-16"
    RG.write_run(runs, row, world, identity=GGUF, saves_dir=None)
    text = "".join(p.read_text() for p in runs.rglob("*") if p.is_file())
    assert GGUF not in text and "a local model through its runner" in text


# ---------------------------------------------------------------------------
# The doors: a model through the local runner and the API door, never a model
# ---------------------------------------------------------------------------


class FakeLlama:
    """A fake `llama-server` for the local runner: its props and a scripted captain who
    steers north and trims at his first turn and stands by until a glass at every other."""

    def __init__(self) -> None:
        self.turns = 0

    def __call__(self, request: Any) -> Any:
        import httpx

        path = request.url.path
        if path == "/props":
            return httpx.Response(
                200,
                json={
                    "model_path": f"/models/{GGUF}",
                    "default_generation_settings": {"n_ctx": 131072},
                    "build_info": "b0000-test",
                },
            )
        if path == "/v1/chat/completions":
            body = json.loads(request.content)
            self.turns += 1
            calls = []
            if self.turns == 1:
                calls.append(("submit_order", {"text": "steer N"}))
            if body["messages"][-1]["role"] != "tool":
                calls.append(("stand_by", {"until": "a glass"}))
            message = {
                "role": "assistant",
                "content": "" if calls else "Very well.",
                "tool_calls": [
                    {
                        "id": f"c{self.turns}_{k}",
                        "type": "function",
                        "function": {"name": n, "arguments": json.dumps(a)},
                    }
                    for k, (n, a) in enumerate(calls)
                ],
            }
            if not calls:
                message.pop("tool_calls")
            return httpx.Response(200, json={"choices": [{"index": 0, "message": message}]})
        return httpx.Response(404)


def _yes_on_record(records: Path, identity: str) -> None:
    records.mkdir(parents=True, exist_ok=True)
    consent.Record(
        identity, "a test runtime", "2026-10-16", consent.YES, answer="Yes.", drill="passed"
    ).write(records)


def test_the_regatta_refuses_a_model_whose_consent_is_not_on_record(short_course, tmp_path):
    """No record for the model: the regatta refuses it in words before the gun, puts no
    consent question, writes no record and no run."""
    pytest.importorskip("fastapi")
    httpx = pytest.importorskip("httpx")
    records = tmp_path / "consent"
    records.mkdir()
    out = io.StringIO()
    world, judge, identity, code = RG.run_door(
        short_course,
        "local",
        [],
        records_dir=records,
        saves_dir=tmp_path / "saves",
        out=out,
        transport=httpx.MockTransport(FakeLlama()),
        say=lambda w: print(w, file=out),
    )
    assert identity == "" and code == 5 and world.clock.tick == 0
    assert "The regatta runs no model whose consent is not on record" in out.getvalue()
    assert "no consent is on record for them" in out.getvalue()
    assert list(records.iterdir()) == []  # nothing written: the question is a game's


def test_a_local_model_with_consent_on_record_sails_the_course_through_its_runner(
    short_course, tmp_path
):
    """The local runner, as a client of the game the regatta hosts, seated at the
    captain's station with the model's consent on record: the clock holds at the gun until
    the station is taken and for every turn after (lockstep), the model's order sails her
    to the line, and the station is stood down when the course is run."""
    pytest.importorskip("fastapi")
    httpx = pytest.importorskip("httpx")
    records = tmp_path / "consent"
    _yes_on_record(records, GGUF)
    server = FakeLlama()
    out = io.StringIO()
    world, judge, identity, code = RG.run_door(
        short_course,
        "local",
        ["--seed", "7"],
        records_dir=records,
        saves_dir=tmp_path / "saves",
        out=out,
        transport=httpx.MockTransport(server),
        poll_wait=0.05,
        say=lambda w: print(w, file=out),
    )
    assert identity == GGUF, out.getvalue()
    assert judge.done and judge.finished_tick < 3600, out.getvalue()
    assert code == 3  # released: the regatta stood the station down at the end
    stationed = [e.text for e in world.log if e.kind == "agent.stationed"]
    assert stationed and stationed[0].startswith("The captain takes the station")
    by_him = [e.text for e in world.log if e.actor == "the captain" and e.kind == "order.accepted"]
    assert any("steering n" in t.lower() for t in by_him), by_him
    # the station is told it is in a race, not play with a human captain (package 42b)
    from freesail.agents.agent import SESSION_RACE

    h = world.agents["captain"]
    assert h.agent.session_kind == SESSION_RACE
    assert f"This session is {SESSION_RACE}." in h.brief.text()
    row = RG.score(short_course, world, judge, "local", identity=identity)
    assert row["kind"] == "a local model through its runner" and row["finished"]


def test_a_hosted_model_with_consent_on_record_sails_the_course_through_the_api_door(
    short_course, tmp_path, monkeypatch
):
    """The API door against the fake Messages server, the key from a fake credential
    store: seated, sailing at lockstep, stood down at the end; without a record, refused."""
    pytest.importorskip("fastapi")
    pytest.importorskip("anthropic")
    pytest.importorskip("keyring")
    from messages_api import MODEL, MessagesServer, fake_store

    from freesail.agents import api

    key = "sk" + "-ant-" + "api03-" + "Rg7xLmPz" * 6
    store = fake_store(monkeypatch)
    store.set_password(api.KEYRING_SERVICE, api.KEYRING_ACCOUNT, key)
    turns = {"n": 0}

    def answer(body: dict) -> dict:
        turns["n"] += 1
        last = body["messages"][-1]["content"]
        after_tool = isinstance(last, list) and any(
            b.get("type") == "tool_result" for b in last if isinstance(b, dict)
        )
        content = []
        if turns["n"] == 1:
            order = {"text": "steer N"}
            content.append({"type": "tool_use", "name": "submit_order", "input": order})
        if not after_tool:
            content.append({"type": "tool_use", "name": "stand_by", "input": {"until": "a glass"}})
        return {"content": content or [{"type": "text", "text": "Very well."}]}

    records = tmp_path / "consent"
    with MessagesServer(key, [answer] * 50) as server:
        out = io.StringIO()
        refused = RG.run_door(
            short_course,
            "api",
            ["--model", MODEL, "--base-url", server.url],
            records_dir=records,
            saves_dir=tmp_path / "saves",
            out=out,
            environ={},
            say=lambda w: print(w, file=out),
        )
        assert refused[2] == "" and refused[3] == 5, out.getvalue()
        _yes_on_record(records, MODEL)
        out = io.StringIO()
        world, judge, identity, code = RG.run_door(
            short_course,
            "api",
            ["--model", MODEL, "--base-url", server.url],
            records_dir=records,
            saves_dir=tmp_path / "saves",
            out=out,
            environ={},
            poll_wait=0.05,
            say=lambda w: print(w, file=out),
        )
    assert identity == MODEL, out.getvalue()
    assert judge.done, out.getvalue()
    row = RG.score(short_course, world, judge, "api", identity=identity)
    assert row["kind"] == "a hosted model through the API door" and row["finished"]


def test_a_humans_game_of_the_course_is_replayed_and_judged(short_course, tmp_path):
    """The course at the gun as a save (`--start-save`), the human's orders given on it at
    the console, the save replayed by its journal and judged as it sails; a save of
    another start is refused in words."""
    from freesail.core import replay

    start = RG.start_save(short_course, tmp_path / "gun.json")
    world, _how = replay.load(start)
    world.run(60)
    world.submit("steer N")
    world.run(1500)
    played = replay.save_to_file(world, tmp_path / "played.json", checkpoint=False)
    replayed, judge = RG.run_replay(short_course, played, say=lambda w: None)
    assert judge.done and judge.finished_tick < 1560
    assert replayed.clock.tick == judge.finished_tick
    row = RG.score(short_course, replayed, judge, "replay")
    assert row["kind"] == "a human's game replayed" and row["finished"]
    other = tmp_path / "other.json"
    data = json.loads(played.read_text())
    data["scenario"]["ship_heading_deg"] = 10.0
    other.write_text(json.dumps(data))
    with pytest.raises(RG.CourseError, match="its start differs"):
        RG.run_replay(short_course, other, say=lambda w: None)


def test_the_command_runs_a_course_and_writes_nothing_with_no_write(short_course, tmp_path):
    out = io.StringIO()
    code = RG.main([short_course.path, "--agent", "fake", "--no-write"], out=out)
    assert code == 0 and "Finished in" in out.getvalue()
    assert RG.main([short_course.path, "--agent", "fake", "--fake", "nope"], out=out) == 2
    assert "no fake 'nope'" in out.getvalue()


# ---------------------------------------------------------------------------
# Truth 90 (slow): the first course under the rules-based captain and the fake
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def first_course_runs():
    course = RG.load_course(FIRST)
    rules = RG.run_rules(course, say=lambda w: None)
    fake = RG.run_fake(course, say=lambda w: None)
    return course, rules, fake


def test_truth_90_the_regatta_runs_the_5b_passage_under_the_rules_and_a_fake_and_scores_both(
    first_course_runs,
):
    """Spec M6 §21 and truth 90: "The regatta runs the 5b passage under the rules-based
    captain and a scripted fake and scores both; the rules-based captain's run replays to
    its digest." Both scored; the rules-based captain finishes within the limit, aground
    never; his run's save replays to the same digest at the finish."""
    from freesail.api.session import ship_factory
    from freesail.core import replay

    course, (rw, rj), (fw, fj) = first_course_runs
    rules = RG.score(course, rw, rj, "rules")
    fake = RG.score(course, fw, fj, "fake")
    assert rules["finished"] and rules["groundings"] == [] and rules["damage"] == []
    assert rules["elapsed_s"] < course.time_limit_s
    assert fake["ran_s"] > 0 and (fake["finished"] or fake["miles_to_go"] > 0)
    again = replay.replay(rw.save(), ship_factory)
    assert again.clock.tick == rj.finished_tick
    assert again.log.digest() == rw.log.digest()
