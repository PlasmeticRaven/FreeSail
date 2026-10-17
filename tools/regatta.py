"""The regatta (spec M6 §21; the proposal's §7.5; package 44): a fixed seed, a fixed course,
a set of agents sailing it, and a score.

    py tools/regatta.py data/regatta/ushant-to-falmouth.yaml --agent rules
    py tools/regatta.py data/regatta/ushant-to-falmouth.yaml --agent fake
    py tools/regatta.py data/regatta/ushant-to-falmouth.yaml --agent local -- \\
        --endpoint http://127.0.0.1:8080 --seed 7
    py tools/regatta.py data/regatta/ushant-to-falmouth.yaml --agent api -- \\
        --model "THE MODEL'S NAME, AS THE API NAMES IT" --effort high
    py tools/regatta.py data/regatta/ushant-to-falmouth.yaml --agent replay --save SAVE.json
    py tools/regatta.py --table docs/playtests/regatta/2026-10-16

**A course** (`data/regatta/<id>.yaml`) is a scenario with a start, a finish line (a place
and a radius), a time limit and marks to round. Its `scenario` gives the ship, the seed,
the time, the weather, the people, the ports and the other sail; what is the scenario's
own captain and not the course's (its book of standing orders and its first orders) is
left out, and the course says instead what every agent is given at the gun
(`start_orders`, the ship as she starts; `standing_orders`, a book every agent starts
with) and may move the start (`start`: `at`, `position`, `heading_deg`, `speed_kn`), the
ports and the ship (`ship`, another ship file on the same course; `--ship` the same for one
run, so that the lugger and the smack of package 43b may sail a course beside the others).
A mark is rounded when her true track crosses the line laid from it to seaward
(`ray_deg` for `ray_nm`); the finish is hers when her true position is within the radius
of the place with every mark rounded in order. The truth is the judge's alone: nothing of
it reaches an agent but what the readings already give.

**The agents.** `rules`: the rules-based captain on the course's `intent` and nobody seated.
`fake`: the scripted captain (`freesail/agents/fake.py`, `captain_on_the_course`) at the
captain's station with the course's `fake:` orders (`--fake NAME` one of its `fakes:`).
`local` and `api`: a model at the captain's station through its door (the local runner,
the API door), the door's own flags after `--`; the game is hosted here and the door runs
beside it as its client, as in the doors' tests, so one command runs a course. `replay`: a
human's game of the course, a save (`--save`) replayed by its journal and judged as it
sails. Every agent runs at lockstep: the scripted ones answer within the tick, and for a
door the clock holds while it has the floor (spec M6 §12). A model whose consent is not on
record is refused in words before the gun, and no consent conversation is begun here
(`Desk.on_record_only`): the question is put in a game.

**The score**: the elapsed time from the gun to the line, with the damage (spars carried
away, sails blown out, lines and cables parted), the groundings, the crew's fatigue (the
company's mean at the end, and the most an hour's mean reached) and the purse as columns.
Each run writes its log (the play log, every line as the log has it, a model's name put
as its kind of agent so that no model is named in the repository) and its row
(`<agent>.json`) under `docs/playtests/regatta/<date>/<course>/`, and the date's table
(`table.md`) is written again from every row of the date. The save of the run goes to
`saves/regatta/` (git ignores it), from which the run replays to its digest.
"""

from __future__ import annotations

import argparse
import datetime as dt
import io
import json
import math
import sys
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from freesail import units  # noqa: E402
from freesail.world.geo import Position, bearing_and_distance, parse_position  # noqa: E402

# Where the runs are kept (spec M6 §21), and where their saves go.
RUNS_DIR = REPO_ROOT / "docs" / "playtests" / "regatta"
SAVES_DIR = REPO_ROOT / "saves" / "regatta"

# The agents, by the word on the command line, and how the table names each: by its kind
# and its door, never by a model's name.
AGENTS: dict[str, tuple[str, str]] = {
    "rules": ("the rules-based captain", "in the game, on the course's intent"),
    "fake": ("the scripted captain", "in the game, at the captain's station"),
    "local": ("a local model through its runner", "the local runner"),
    "api": ("a hosted model through the API door", "the API door"),
    "replay": ("a human's game replayed", "a save's journal"),
}

# The log's kinds that are damage done to the ship (the strain's and the anchor's lines).
DAMAGE_KINDS: tuple[str, ...] = (
    "spar.carried_away",
    "sail.blown_out",
    "line.parted",
    "cable.parted",
)
GROUNDING_KIND = "ship.aground"

# How long the regatta waits for a door to take the station before the gun, in real
# seconds (a door asks its model server or the API who it is and checks the context first).
SEAT_WAIT_S = 300.0
# How many ticks run between two looks at a door's floor (it is looked at again after
# every tick that opens a sample, so this only bounds the lock's holding).
DOOR_BATCH_TICKS = 600
# How often the hourly figures (the crew's fatigue) are read, in ticks.
HOUR_S = 3600


class CourseError(ValueError):
    """A course file that cannot be read, in words that name the file and the field."""


@dataclass
class Mark:
    """A mark to round: its name, where it is, the side it is left on (words for the
    table), and the line laid from it to seaward that her track must cross."""

    name: str
    position: Position
    ray_deg: float
    ray_nm: float
    leave: str = ""


@dataclass
class Course:
    id: str
    path: str
    name: str
    scenario: str
    seed: int | None
    start: dict[str, Any]
    ports: list[str] | None
    start_orders: list[str]
    standing_orders: list[str]
    finish_at: str
    finish: Position
    radius_nm: float
    time_limit_s: int
    marks: list[Mark]
    intent: str
    fake: dict[str, list[str]]
    fakes: dict[str, dict[str, list[str]]] = field(default_factory=dict)
    ship: str | None = None  # another ship file than the scenario's


def _place(world: Any, words: str, where: str) -> tuple[str, Position]:
    """A place a course names: a chart feature by its name or id, or a position."""
    chart = getattr(world, "chart", None)
    feature = chart.find_feature(words) if chart is not None else None
    if feature is not None:
        return feature.name, feature.position
    try:
        return words, parse_position(words)
    except ValueError:
        raise CourseError(f"{where}: the chart knows no place '{words}'.") from None


def load_course(path: str | Path) -> Course:
    """A course file read; the places are checked against the chart by `course_world`."""
    path = Path(path)
    try:
        raw = yaml.safe_load(path.read_text()) or {}
    except (OSError, yaml.YAMLError) as e:
        raise CourseError(f"{path}: {e}") from None
    where = str(path)
    for key in ("name", "scenario", "finish", "time_limit_hours"):
        if key not in raw:
            raise CourseError(f"{where}: a course says its {key}.")
    finish = raw["finish"] or {}
    if not isinstance(finish, dict) or "at" not in finish:
        raise CourseError(f"{where}, finish: say where, {{at: <place>, radius_nm: <miles>}}.")
    marks = []
    for m in raw.get("marks") or []:
        if not isinstance(m, dict) or "at" not in m or "ray_deg" not in m:
            raise CourseError(f"{where}, marks: each is {{at, leave, ray_deg, ray_nm}}.")
        marks.append(
            Mark(
                str(m["at"]),
                Position(0.0, 0.0),
                float(m["ray_deg"]),
                float(m.get("ray_nm", 20.0)),
                str(m.get("leave") or ""),
            )
        )
    fake = raw.get("fake") or {}
    fakes = {str(k): dict(v or {}) for k, v in (raw.get("fakes") or {}).items()}
    return Course(
        id=path.stem,
        path=str(path),
        name=str(raw["name"]),
        scenario=str(raw["scenario"]),
        seed=int(raw["seed"]) if raw.get("seed") is not None else None,
        start=dict(raw.get("start") or {}),
        ports=[str(p) for p in raw["ports"]] if raw.get("ports") else None,
        start_orders=[str(x) for x in raw.get("start_orders") or []],
        standing_orders=[str(x) for x in raw.get("standing_orders") or []],
        finish_at=str(finish["at"]),
        finish=Position(0.0, 0.0),
        radius_nm=float(finish.get("radius_nm", 1.0)),
        time_limit_s=int(float(raw["time_limit_hours"]) * 3600),
        marks=marks,
        intent=str(raw.get("intent") or ""),
        fake={k: [str(x) for x in fake.get(k) or []] for k in ("first", "each_glass")},
        fakes={
            name: {k: [str(x) for x in d.get(k) or []] for k in ("first", "each_glass")}
            for name, d in fakes.items()
        },
        ship=str(raw["ship"]) if raw.get("ship") else None,
    )


def course_world(course: Course, intent: str = "") -> Any:
    """The course's World at the gun: the scenario with its own captain left out and the
    course's start, the agent's intent (the rules-based captain's only), the course's book
    and its start orders given at tick 0, the places looked up on the chart."""
    from freesail.world.scenarios import begin, load_scenario, make_scenario_world

    sf = load_scenario(REPO_ROOT / course.scenario)
    sc = sf.scenario
    start = course.start
    if start.get("at"):
        sc.start_time = dt.datetime.fromisoformat(str(start["at"]))
    if start.get("position"):
        p = parse_position(str(start["position"]))
        sc.position = {"lat_deg": p.lat_deg, "lon_deg": p.lon_deg}
        sc.latitude_deg = p.lat_deg
    if start.get("heading_deg") is not None:
        sc.ship_heading_deg = float(start["heading_deg"])
    if start.get("speed_kn") is not None:
        sc.ship_speed_kn = float(start["speed_kn"])
    if course.ports is not None:
        sc.ports = list(course.ports)
    sc.intent = intent
    sc.books = list(course.standing_orders)
    sf.standing_orders = list(course.standing_orders)
    sf.orders = list(course.start_orders)
    world = make_scenario_world(sf, seed=course.seed, ship=course.ship)
    _name, course.finish = _place(world, course.finish_at, f"{course.path}, finish")
    for m in course.marks:
        m.name, m.position = _place(world, m.name, f"{course.path}, marks")
    begin(world, sf)
    return world


# ---------------------------------------------------------------------------
# The judge: the marks and the line, from the truth, tick by tick
# ---------------------------------------------------------------------------


def _local_nm(origin: Position, p: Position) -> tuple[float, float]:
    """`p` east and north of `origin`, in miles, on the plane tangent there."""
    east = (p.lon_deg - origin.lon_deg) * 60.0 * math.cos(math.radians(origin.lat_deg))
    north = (p.lat_deg - origin.lat_deg) * 60.0
    return east, north


def _crosses(a0: tuple[float, float], a1: tuple[float, float], b1: tuple[float, float]) -> bool:
    """Whether the segment a0-a1 crosses the segment from the origin to b1."""

    def side(p: tuple[float, float], q: tuple[float, float], r: tuple[float, float]) -> float:
        return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])

    o = (0.0, 0.0)
    d1, d2 = side(o, b1, a0), side(o, b1, a1)
    d3, d4 = side(a0, a1, o), side(a0, a1, b1)
    return d1 * d2 < 0.0 and d3 * d4 < 0.0


class Judge:
    """The course's judge: each tick, from her true position (which no agent reads), the
    next mark rounded when her track crosses its line, and the finish when she is within
    the radius with every mark rounded; the crew's fatigue read each hour."""

    def __init__(self, course: Course, world: Any):
        self.course = course
        self.rounded: list[tuple[str, int]] = []
        self.finished_tick: int | None = None
        self.last: Position | None = world.position
        self.purse_at_gun = _purse(world)
        self.fatigue_most = _fatigue(world)
        self.radius_m = course.radius_nm * units.NAUTICAL_MILE

    @property
    def done(self) -> bool:
        return self.finished_tick is not None

    def tick(self, world: Any) -> bool:
        """Judge the tick just run; True when she has finished or the time is up."""
        now = world.position
        tick = world.clock.tick
        if now is not None and self.finished_tick is None:
            if self.last is not None and len(self.rounded) < len(self.course.marks):
                mark = self.course.marks[len(self.rounded)]
                a0 = _local_nm(mark.position, self.last)
                a1 = _local_nm(mark.position, now)
                r = math.radians(mark.ray_deg)
                b1 = (mark.ray_nm * math.sin(r), mark.ray_nm * math.cos(r))
                if _crosses(a0, a1, b1):
                    self.rounded.append((mark.name, tick))
            if len(self.rounded) == len(self.course.marks):
                _, d = bearing_and_distance(now, self.course.finish)
                if d <= self.radius_m:
                    self.finished_tick = tick
        self.last = now
        if tick % HOUR_S == 0:
            self.fatigue_most = max(self.fatigue_most, _fatigue(world))
        return self.finished_tick is not None or tick >= self.course.time_limit_s


def _purse(world: Any) -> float | None:
    purse = getattr(world, "purse", None)
    return None if purse is None else float(purse.pounds)


def _fatigue(world: Any) -> float:
    """The company's mean fatigue now, 0 to 1."""
    crew = (getattr(world.ship, "extra", None) or {}).get("crew")
    sailors = list(getattr(crew, "sailors", None) or ())
    if not sailors:
        return 0.0
    return sum(s.fatigue for s in sailors) / len(sailors)


# ---------------------------------------------------------------------------
# The score
# ---------------------------------------------------------------------------


def hours_words(seconds: int) -> str:
    """'14 h 50 m'."""
    h, rest = divmod(int(seconds), 3600)
    return f"{h} h {rest // 60:02d} m"


def score(
    course: Course,
    world: Any,
    judge: Judge,
    agent: str,
    *,
    label: str = "",
    note: str = "",
    identity: str = "",
) -> dict[str, Any]:
    """The run's row: who sailed, whether and when she finished, and the columns."""
    from freesail.crew.model import fatigue_words

    kind, door = AGENTS[agent]
    log = world.log
    damage = [e for e in log if e.kind in DAMAGE_KINDS]
    grounded = [e for e in log if e.kind == GROUNDING_KIND]
    fatigue = _fatigue(world)
    purse = _purse(world)
    change = None if purse is None or judge.purse_at_gun is None else purse - judge.purse_at_gun
    row: dict[str, Any] = {
        "course": course.id,
        "course_name": course.name,
        "agent": agent,
        "label": label or agent,
        "kind": kind,
        "door": door,
        "note": note,
        "seed": world.seed,
        "finished": judge.finished_tick is not None,
        "elapsed_s": judge.finished_tick,
        "elapsed": hours_words(judge.finished_tick) if judge.finished_tick is not None else "",
        "ran_s": world.clock.tick,
        "time_limit_s": course.time_limit_s,
        "marks": [{"mark": m, "tick": t} for m, t in judge.rounded],
        "damage": [redact(e.text, identity, kind) for e in damage],
        "groundings": [{"tick": e.tick, "text": redact(e.text, identity, kind)} for e in grounded],
        "fatigue": round(fatigue, 3),
        "fatigue_words": fatigue_words(fatigue),
        "fatigue_most": round(judge.fatigue_most, 3),
        "purse": None if purse is None else round(purse, 2),
        "purse_change": None if change is None else round(change, 2),
        "lines": len(log),
        "digest": log.digest()[:16],
    }
    if judge.finished_tick is None:
        _, d = bearing_and_distance(world.position, course.finish)
        row["miles_to_go"] = round(d / units.NAUTICAL_MILE, 1)
    return row


def redact(text: str, identity: str, kind: str) -> str:
    """A model's name put as its kind of agent (the repository names no model)."""
    return text.replace(identity, kind) if identity else text


# ---------------------------------------------------------------------------
# The agents
# ---------------------------------------------------------------------------


def run_rules(course: Course, say: Any = print) -> tuple[Any, Judge]:
    """The rules-based captain on the course's intent, nobody seated."""
    if not course.intent:
        raise CourseError(f"{course.path}: the rules-based captain wants the course's intent.")
    world = course_world(course, intent=course.intent)
    judge = Judge(course, world)
    _sail(world, judge, say)
    return world, judge


def fake_orders(course: Course, name: str | None = None) -> dict[str, list[str]]:
    if not name:
        return course.fake
    if name not in course.fakes:
        raise CourseError(
            f"{course.path}: no fake '{name}'; the course has "
            + (", ".join(f"'{k}'" for k in course.fakes) or "none but its own")
            + "."
        )
    return course.fakes[name]


def run_fake(course: Course, name: str | None = None, say: Any = print) -> tuple[Any, Judge]:
    """The scripted captain at the captain's station, in the game, sampled every glass and
    on the notable and urgent lines in lockstep (it answers within the tick)."""
    from freesail.agents import Harness, SamplingPolicy
    from freesail.agents.agent import A_GLASS_S, SESSION_RACE, captain
    from freesail.agents.fake import captain_on_the_course

    orders = fake_orders(course, name)
    world = course_world(course)
    station = captain(SamplingPolicy.in_lockstep(A_GLASS_S, "notable", "urgent"), world=world)
    h = Harness(
        world,
        station,
        captain_on_the_course(orders["first"], orders["each_glass"]),
        session_kind=SESSION_RACE,
        save=lambda w, why: "",
    )
    h.model_name = "the scripted captain"
    h.start()
    judge = Judge(course, world)
    _sail(world, judge, say)
    return world, judge


def run_replay(course: Course, save: str | Path, say: Any = print) -> tuple[Any, Judge]:
    """A human's game of the course, replayed by its journal and judged as it sails: the
    save must be of this course's start (its scenario, its seed), played from the gun."""
    from freesail.api.session import ship_factory
    from freesail.core import replay as replay_mod

    data = replay_mod.load_file(save)
    gun = course_world(course)
    ours = gun.save()
    if data.get("seed") != ours.get("seed"):
        raise CourseError(f"{save} is not a game of this course: its seed differs.")
    if data.get("scenario") != ours.get("scenario"):
        raise CourseError(
            f"{save} is not a game of this course: its start differs (play it from the "
            f"course's own start: py tools/regatta.py {course.path} --start-save FILE)."
        )
    judge = Judge(course, gun)
    world = replay_mod.replay(data, ship_factory, on_tick=judge.tick)
    return world, judge


def start_save(course: Course, path: str | Path) -> Path:
    """The course at the gun as a save, for a human to load at the console or the browser
    (`--load`) and sail; the save he makes then is the replay agent's."""
    from freesail.core import replay as replay_mod

    world = course_world(course)
    return replay_mod.save_to_file(world, path)


def _sail(world: Any, judge: Judge, say: Any) -> None:
    """Run the World until the judge says she is in or the time is up."""
    t0 = time.monotonic()
    while True:
        world.tick()
        if judge.tick(world):
            break
        if world.clock.tick % (6 * HOUR_S) == 0:
            say(_progress(world, judge, t0))


def _progress(world: Any, judge: Judge, t0: float) -> str:
    _, d = bearing_and_distance(world.position, judge.course.finish)
    rate = world.clock.tick / max(time.monotonic() - t0, 1e-6)
    return (
        f"  {world.clock.stamp()}: {d / units.NAUTICAL_MILE:.1f} miles to the line, "
        f"{len(judge.rounded)} of {len(judge.course.marks)} marks rounded ({rate:.0f} ticks a "
        "second)."
    )


def run_door(
    course: Course,
    agent: str,
    door_argv: list[str],
    *,
    records_dir: str | Path | None = None,
    saves_dir: str | Path = SAVES_DIR,
    out: Any = None,
    transport: Any = None,
    base_url_server: Any = None,
    environ: dict[str, str] | None = None,
    seat_wait_s: float = SEAT_WAIT_S,
    poll_wait: float = 0.5,
    say: Any = print,
) -> tuple[Any, Judge, str, int]:
    """A model at the captain's station through its door (`local` or `api`): the game is
    hosted here (the browser game's app, served to the door in this process), the door
    runs in a thread as its client with its own flags, the regatta holds the clock at the
    gun until the station is taken and in lockstep after, and stands the station down when
    the course is run. A model whose consent is not on record is refused before the gun.
    Returns the world, the judge, the identity the door seated, and the door's exit code
    (`local.EXIT_NO_CONSENT` when refused, the run not made)."""
    from fastapi.testclient import TestClient

    from freesail.agents import consent as consent_mod
    from freesail.ui.console import check_agents_unattended
    from freesail.ui.server import Driver, create_app

    world = course_world(course)
    driver = Driver(world, lockstep=True)
    app = create_app(
        driver,
        game=f"FreeSail's regatta (tools/regatta.py, {course.id})",
        consent_records=records_dir if records_dir is not None else consent_mod.RECORDS_DIR,
        saves_dir=saves_dir,
        say=lambda words: say(words),
    )
    desk = driver.desk
    desk.on_record_only = True  # the regatta runs no model without its consent on record
    desk.race = True  # and tells it the session is a race (package 42b)
    http = TestClient(app)
    out = out or sys.stdout
    argv = ["--game", "http://regatta", "--station", "captain", *door_argv]
    got: dict[str, Any] = {}

    def door() -> None:
        if agent == "local":
            from freesail.agents import local

            got["code"] = local.main(
                argv, out=out, transport=transport, game_http=http, poll_wait=poll_wait
            )
        else:
            from freesail.agents import api

            got["code"] = api.main(
                argv,
                inp=io.StringIO(""),
                out=out,
                game_http=http,
                poll_wait=poll_wait,
                environ=environ,
            )

    thread = threading.Thread(target=door, daemon=True)
    thread.start()
    # the gun waits for the station to be taken (or the door to end, refused)
    end = time.monotonic() + seat_wait_s
    seat = None
    while time.monotonic() < end and thread.is_alive():
        with driver.lock:
            seat = desk.seats.get("captain")
            if seat is not None and seat.harness is not None:
                break
        time.sleep(0.02)
    if seat is None or seat.harness is None:
        thread.join(timeout=5.0)
        return world, Judge(course, world), "", int(got.get("code", 2))
    identity = seat.model_name
    judge = Judge(course, world)
    t0 = time.monotonic()
    while True:
        with driver.lock:
            for _ in range(DOOR_BATCH_TICKS):
                if desk.holding() is not None:
                    break
                world.tick()
                if judge.tick(world):
                    break
                if world.clock.tick % (6 * HOUR_S) == 0:
                    say(_progress(world, judge, t0))
            check_agents_unattended(world)
            over = judge.done or world.clock.tick >= course.time_limit_s
            held = desk.holding() is not None
        if over:
            break
        if held:
            time.sleep(0.005)
    with driver.lock:
        h = world.agents.get("captain")
        if h is not None and not h.agent.released:
            world.submit("stand down the captain")
    thread.join(timeout=30.0)
    return world, judge, identity, int(got.get("code", 0))


# ---------------------------------------------------------------------------
# The records: a run's log and row, the date's table
# ---------------------------------------------------------------------------


def write_run(
    runs_dir: str | Path,
    row: dict[str, Any],
    world: Any,
    identity: str = "",
    saves_dir: str | Path | None = SAVES_DIR,
) -> Path:
    """Write the run's log and row under `<runs_dir>/<course>/`, its save under
    `saves_dir`, and the date's table again; returns the row's file."""
    from freesail.core import replay as replay_mod

    folder = Path(runs_dir) / row["course"]
    folder.mkdir(parents=True, exist_ok=True)
    label = row["label"]
    n = 2
    while (folder / f"{label}.json").exists() and not row.get("replace"):
        label = f"{row['label']}-{n}"
        n += 1
    row["label"] = label
    if saves_dir is not None:
        Path(saves_dir).mkdir(parents=True, exist_ok=True)
        p = Path(saves_dir) / f"{Path(runs_dir).name}-{row['course']}-{label}.json"
        replay_mod.save_to_file(world, p, checkpoint=False)
        row["save"] = _rel(p)
    lines = [redact(e.line(), identity, row["kind"]) for e in world.log]
    head = (
        f"# {row['course_name']} ({row['course']}), {row['kind']} ({row['door']}); seed "
        f"{row['seed']}; {len(lines)} lines, the digest {row['digest']}"
    )
    (folder / f"{label}.log").write_text("\n".join([head, *lines]) + "\n")
    path = folder / f"{label}.json"
    path.write_text(json.dumps(row, indent=2) + "\n")
    write_table(runs_dir)
    return path


def _rel(p: Path) -> str:
    try:
        return str(p.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(p)


COLUMNS = (
    "Agent",
    "Door",
    "Finished",
    "Elapsed",
    "Marks",
    "Damage",
    "Grounding",
    "Fatigue (end, most)",
    "Purse",
    "Lines, digest",
)


def table_lines(runs_dir: str | Path) -> list[str]:
    """The date's table, a course at a time, the finishers first by their time."""
    runs_dir = Path(runs_dir)
    rows = [json.loads(p.read_text()) for p in sorted(runs_dir.glob("*/*.json"))]
    out = [
        f"# The regatta, {runs_dir.name}",
        "",
        "Each course run at lockstep under each agent by `tools/regatta.py` (spec M6 §21). "
        "Elapsed is from the gun to the line, her true position within the finish's radius "
        "with every mark rounded; a run not finished says how far she had to go at the limit. "
        "Damage is the spars carried away, the sails blown out and the lines and cables "
        "parted; fatigue the company's mean (0 fresh, 1 worn out) at the end and the most an "
        "hour's mean reached; the purse is at the end, with its change since the gun. The "
        "logs and rows are beside this file, a folder to a course.",
    ]
    by_course: dict[str, list[dict[str, Any]]] = {}
    for r in rows:
        by_course.setdefault(r["course"], []).append(r)
    # the courses by their length (their limits), the agents finishers first by their time
    ordered = sorted(by_course.items(), key=lambda kv: (kv[1][0]["time_limit_s"], kv[0]))
    for course_id, course_rows in ordered:
        course_rows.sort(
            key=lambda r: (not r["finished"], r["elapsed_s"] or 0, r.get("miles_to_go") or 0)
        )
        first = course_rows[0]
        out += [
            "",
            f"## {first['course_name']} (`data/regatta/{course_id}.yaml`)",
            "",
            f"Seed {first['seed']}; the limit {hours_words(first['time_limit_s'])}.",
            "",
            "| " + " | ".join(COLUMNS) + " |",
            "|" + "---|" * len(COLUMNS),
        ]
        for r in course_rows:
            out.append("| " + " | ".join(_cells(r)) + " |")
        notes = [r for r in course_rows if r.get("note")]
        if notes:
            out.append("")
            out += [f"- {r['label']}: {r['note']}" for r in notes]
    return out


def _cells(r: dict[str, Any]) -> list[str]:
    who = r["kind"] + (f" ({r['label']})" if r["label"] != r["agent"] else "")
    finished = "yes" if r["finished"] else f"no, {r.get('miles_to_go', '?')} miles to go"
    elapsed = r["elapsed"] or f"(ran {hours_words(r['ran_s'])})"
    marks = ", ".join(f"{m['mark']} {hours_words(m['tick'])}" for m in r["marks"]) or "none"
    damage = (
        f"{len(r['damage'])}: " + "; ".join(_clause(d) for d in r["damage"][:3])
        if r["damage"]
        else "none"
    )
    if len(r["damage"]) > 3:
        damage += "; ..."
    first = r["groundings"][0] if r["groundings"] else None
    ground = (
        f"{len(r['groundings'])}, the first at {hours_words(first['tick'])}: "
        f"{_clause(first['text'])}"
        if first
        else "none"
    )
    fatigue = f"{r['fatigue']:.2f} ({r['fatigue_words']}), {r['fatigue_most']:.2f}"
    if r["purse"] is None:
        purse = "none"
    else:
        change = r["purse_change"] or 0.0
        moved = (
            f"£{-change:,.0f} spent"
            if change < 0
            else f"£{change:,.0f} gained"
            if change > 0
            else "as at the gun"
        )
        purse = f"£{r['purse']:,.0f} ({moved})"
    return [
        who,
        r["door"],
        finished,
        elapsed,
        marks,
        damage,
        ground,
        fatigue,
        purse,
        f"{r['lines']}, `{r['digest']}`",
    ]


def _clause(text: str) -> str:
    """A log line's first clause, for a cell: 'She has taken the ground forward: two
    fathoms ...' is 'She has taken the ground forward, two fathoms ...' to its first stop."""
    head = text.split(";")[0].split(". ")[0].rstrip(".")
    return head.replace(": ", ", ", 1)


def write_table(runs_dir: str | Path) -> Path:
    path = Path(runs_dir) / "table.md"
    path.write_text("\n".join(table_lines(runs_dir)) + "\n")
    return path


# ---------------------------------------------------------------------------
# The command
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None, *, out: Any = None, **door_kw: Any) -> int:
    out = out or sys.stdout
    argv = list(sys.argv[1:] if argv is None else argv)
    door_argv: list[str] = []
    if "--" in argv:
        i = argv.index("--")
        argv, door_argv = argv[:i], argv[i + 1 :]
    ap = argparse.ArgumentParser(
        description="FreeSail: the regatta, a course sailed by an agent and scored (spec M6 §21)"
    )
    ap.add_argument("course", nargs="?", help="the course file (data/regatta/<id>.yaml)")
    ap.add_argument("--agent", choices=list(AGENTS), help="who sails her")
    ap.add_argument("--fake", default=None, help="one of the course's other fakes, by name")
    ap.add_argument("--save", default=None, help="the replay agent's save")
    ap.add_argument("--ship", default=None, help="another ship file on the course (one run)")
    ap.add_argument("--label", default="", help="the run's name in the table (never a model's)")
    ap.add_argument("--note", default="", help="a note for the table, under the course")
    ap.add_argument("--date", default=None, help="the date's folder (default today)")
    ap.add_argument("--out", default=str(RUNS_DIR), help="where the dates' folders are")
    ap.add_argument("--consent-records", default=None, help="where consent records are read")
    ap.add_argument("--start-save", default=None, help="write the course at the gun as a save")
    ap.add_argument("--table", default=None, help="write a date's table again from its rows")
    ap.add_argument("--no-write", action="store_true", help="score the run and write nothing")
    args = ap.parse_args(argv)

    def say(words: str) -> None:
        print(words, file=out, flush=True)

    if args.table:
        say(f"Wrote {write_table(args.table)}.")
        return 0
    if not args.course:
        ap.error("a course file, or --table DATE_FOLDER")
    try:
        course = load_course(args.course)
        if args.ship:
            course.ship = args.ship
        if args.start_save:
            say(f"The course at the gun, saved to {start_save(course, args.start_save)}.")
            return 0
        if not args.agent:
            ap.error("--agent: rules, fake, local, api or replay")
        kind, door = AGENTS[args.agent]
        say(f"The regatta: {course.name} ({course.path}), {kind} ({door}).")
        identity = ""
        if args.agent == "rules":
            world, judge = run_rules(course, say)
        elif args.agent == "fake":
            world, judge = run_fake(course, args.fake, say)
        elif args.agent == "replay":
            if not args.save:
                ap.error("--agent replay wants --save SAVE.json, a game of the course")
            world, judge = run_replay(course, args.save, say)
        else:
            world, judge, identity, code = run_door(
                course,
                args.agent,
                door_argv,
                records_dir=args.consent_records,
                out=out,
                say=say,
                **door_kw,
            )
            if not identity:
                say("The door did not take the station; no run was made, and nothing written.")
                return code or 2
    except CourseError as e:
        say(str(e))
        return 2
    label = args.label or (args.fake.replace(" ", "-") if args.fake else args.agent)
    row = score(course, world, judge, args.agent, label=label, note=args.note, identity=identity)
    if args.fake:
        row["note"] = row["note"] or f"the course's fake '{args.fake}'"
    words = (
        f"Finished in {row['elapsed']}"
        if row["finished"]
        else f"Not finished at the limit, {row.get('miles_to_go')} miles to go"
    )
    say(
        f"{words}; damage {len(row['damage'])}, groundings {len(row['groundings'])}, "
        f"fatigue {row['fatigue']:.2f}; {row['lines']} lines, the digest {row['digest']}."
    )
    if args.no_write:
        return 0
    date = args.date or dt.date.today().isoformat()
    path = write_run(Path(args.out) / date, row, world, identity)
    say(f"Wrote {path} and the date's table beside it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
