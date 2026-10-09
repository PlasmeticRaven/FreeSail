"""Save to disk and rebuild a world by replaying its order journal.

A save is not a snapshot. It is the seed, the scenario, a reference to the
ship, and the list of (tick, actor, order). Replaying it re-runs the
simulation and must produce an identical log; `tests/test_replay.py` holds
the engine to that.

Since package 29 a save also holds its `inputs` (`World.inputs`): every order in the
order it was given, refused and queries too, and the lines a driver wrote, so that a
replay at any tick of a played day reproduces the log a player watched, refusals and all.
A save without them replays its journal, as before.

**The checkpoint** (package 33a; the cold review's item 6). The journal stays the
definition of a save; a checkpoint is a shortcut written beside it: the world's whole
state at the save's tick (the ship's parts and dynamics, the crew, the routine, the
runner's instances mid-way, the standing book with its rules' state, the weather and the
sea, the reckoning, the agents' journals and turns, the rng streams' states, the log),
which `load` reads in a fraction of a second where a replay of a four-day passage takes
minutes. It is written by `save_to_file` beside the JSON (`<name>.checkpoint`) and read
by `load`, which takes it only when it belongs to the save beside it (the same seed,
end tick and journal) and its log's digest is the one it was written with, and replays
the journal otherwise; `tests/test_checkpoint.py` proves that a world loaded from the
checkpoint and a world replayed to the same tick carry on to the same digest for a
watch. The state is Python's pickle of the object graph with the hooks that do not
pickle left out (the ship's stepper and order handler, the chart's shared tiles, the
log's subscribers, an agent's live door) and put back at the load; it is read through
an unpickler that admits the game's own classes and the standard library's plain
types and nothing else, so a checkpoint from elsewhere cannot run code here.

**The build's stamp and the load's rule** (package 37d; the review of gate 5c's
playtests, sections 6 and 9). A save and its checkpoint's header say which build wrote
them (`"build": {"name", "rules"}`, `core.world.build_stamp`), and a save says every
build its game was played under (`"builds"`). A save is exact from its checkpoint, and a
replay is promised only on the build that wrote it: `load_report` says which road it took
and why a checkpoint was not taken (none beside the save; not this save's; could not be
read, with the error's words, whatever the error), and `check_replay` refuses to replay
another build's game with a station's transcript in it (`ReplayRefused`, in plain words)
unless it is asked to (`replay_anyway`; `--replay-anyway` at every door). A checkpoint is
a picture of the program's own objects, so every new field on a class it holds has a
plain class default, and `tests/fixtures/saves/` keeps old checkpoints as tests.
"""

from __future__ import annotations

import gzip
import io
import json
import pickle
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from freesail.core.world import SAVE_FORMAT, Scenario, World, build_stamp, build_words

ShipFactory = Callable[[dict[str, Any], Scenario], Any]

CHECKPOINT_FORMAT = 1
CHECKPOINT_SUFFIX = ".checkpoint"


def checkpoint_path(path: str | Path) -> Path:
    """The checkpoint beside a save: `day.json` has `day.checkpoint`."""
    return Path(path).with_suffix(CHECKPOINT_SUFFIX)


def save_to_file(world: World, path: str | Path, checkpoint: bool = True) -> Path:
    """Write the save (the journal, the definition) and, beside it, the checkpoint (the
    shortcut); a checkpoint that cannot be taken (a rule holding something that will not
    pickle) is left out and the save stands alone, as it always did."""
    path = Path(path)
    path.write_text(json.dumps(world.save(), indent=2))
    if checkpoint:
        try:
            write_checkpoint(world, checkpoint_path(path))
        except (pickle.PicklingError, TypeError, AttributeError):
            cp = checkpoint_path(path)
            if cp.exists():
                cp.unlink()
    return path


def load_file(path: str | Path) -> dict[str, Any]:
    data = json.loads(Path(path).read_text())
    if data.get("format") != SAVE_FORMAT:
        raise ValueError(f"{path}: save format {data.get('format')} is not {SAVE_FORMAT}")
    return data


def build_world(data: dict[str, Any], ship_factory: ShipFactory | None = None) -> World:
    """Construct the world at tick 0 from a save, without running it."""
    scenario = Scenario.from_dict(data["scenario"])
    ship = ship_factory(data["ship_ref"], scenario) if ship_factory else None
    world = World(seed=data["seed"], scenario=scenario, ship=ship)
    # Systems that need the World itself (the crew, mustered from its seed and kept by its
    # clock) are attached now, before the first order, as `make_world` attaches them.
    on_world = (getattr(ship, "extra", None) or {}).pop("on_world", None)
    if on_world is not None:
        on_world(world)
    if data.get("agents"):
        # the agents at their stations (spec M4 §11): each is stationed when the replay
        # reaches its tick and its recorded replies are played back, so the log is the same
        from freesail.agents.harness import restore

        restore(world, data)
    return world


def replay(
    data: dict[str, Any],
    ship_factory: ShipFactory | None = None,
    until_tick: int | None = None,
) -> World:
    """Rebuild a world and run it to `until_tick` (default: the save's end tick),
    re-submitting journaled orders at their ticks."""
    world = build_world(data, ship_factory)
    end = data["end_tick"] if until_tick is None else min(until_tick, data["end_tick"])
    inputs = data.get("inputs")
    if inputs is None:
        inputs = [{"tick": t, "actor": a, "order": o} for t, a, o in data["journal"]]
    i = 0
    while True:
        # between two ticks, before this tick's inputs: a station's acts from outside the
        # loop are made here and after an input, where a door made them in play, and never
        # inside the World's tick (package 37i: game 10's last save replayed one line short
        # when a standing order's firing inside the tick made the door's stand-down early)
        for agent in list(world.agents.values()):
            agent.on_between_ticks()
        while i < len(inputs) and int(inputs[i]["tick"]) == world.clock.tick:
            _give(world, inputs[i])
            i += 1
            # a station seated after this input, whatever it was (package 37d: a driver's
            # line and a refused order are inputs and no orders), is seated here
            for agent in list(world.agents.values()):
                agent.on_input()
        if world.clock.tick >= end:
            break
        world.tick()
    return world


def _give(world: World, entry: dict[str, Any]) -> None:
    """One input again: an order to the ship, a world order from outside the scenario
    (package 36: at its tick with its source, truth 72), or a driver's line to the log."""
    if "order" in entry:
        world.submit(str(entry["order"]), actor=str(entry["actor"]))
        return
    if "world_order" in entry:
        world.world_order(str(entry["world_order"]), source=str(entry.get("source", "")))
        return
    line = entry["line"]
    world.record_driver(line["severity"], line["kind"], line["text"], line.get("data"))


def replay_world(world: World, ship_factory: ShipFactory | None = None) -> World:
    """Replay a live world from its own save. Used by the determinism tests."""
    return replay(world.save(), ship_factory)


# ---------------------------------------------------------------------------
# The checkpoint (package 33a)
# ---------------------------------------------------------------------------


class _Pickler(pickle.Pickler):
    """Pickles the world's graph with the parts that are not state left out: the chart's
    shared tiles (reloaded by region), the readings' cached view, the log's subscribers,
    the ship's two hooks (rebound by the composer), an agent's live model and save
    callback (the driver gives them again). Everything else is the state itself."""

    def reducer_override(self, obj: Any) -> Any:  # type: ignore[override]
        cls = type(obj)
        name = f"{cls.__module__}.{cls.__qualname__}"
        if name == "freesail.core.world.World":
            state = dict(obj.__dict__)
            state["chart"] = None
            state["_readings_view"] = None
            state["_readings_key"] = None
            state.pop("load_report", None)  # how this run was loaded is not the game's state
            return _new, (cls,), state
        if name == "freesail.core.events.Log":
            state = dict(obj.__dict__)
            state["_subscribers"] = []
            return _new, (cls,), state
        if name == "freesail.ship.graph.Ship":
            state = dict(obj.__dict__)
            state["stepper"] = None
            state["order_handler"] = None
            return _new, (cls,), state
        if name == "freesail.world.lookout.Lookout":
            state = dict(obj.__dict__)
            state["chart"] = None
            return _new, (cls,), state
        if name == "freesail.agents.harness.Harness":
            state = dict(obj.__dict__)
            state["model"] = None
            state["save_fn"] = None
            return _new, (cls,), state
        return NotImplemented


def _new(cls: type) -> Any:
    return cls.__new__(cls)


# What a checkpoint may name: the game's own classes and the standard library's plain
# types that its state is made of. Anything else is refused, so a checkpoint from
# elsewhere cannot run code here.
_ALLOWED_MODULES = ("freesail.",)
_ALLOWED_EXACT = {
    ("freesail.core.replay", "_new"),
    ("copyreg", "_reconstructor"),
    ("builtins", "set"),
    ("builtins", "frozenset"),
    ("builtins", "list"),
    ("builtins", "dict"),
    ("builtins", "tuple"),
    ("builtins", "object"),
    ("builtins", "bytearray"),
    ("builtins", "bytes"),
    ("builtins", "str"),
    ("builtins", "int"),
    ("builtins", "float"),
    ("builtins", "bool"),
    ("builtins", "complex"),
    ("builtins", "range"),
    ("builtins", "slice"),
    ("builtins", "getattr"),
    ("random", "Random"),
    ("_random", "Random"),
    ("collections", "OrderedDict"),
    ("collections", "deque"),
    ("collections", "defaultdict"),
    ("datetime", "datetime"),
    ("datetime", "date"),
    ("datetime", "timedelta"),
    ("datetime", "time"),
    ("datetime", "timezone"),
    ("pathlib", "PosixPath"),
    ("pathlib", "WindowsPath"),
    ("pathlib", "PurePosixPath"),
    ("pathlib", "PureWindowsPath"),
    ("enum", "EnumType"),
    ("enum", "EnumMeta"),
}
_ALLOWED_PREFIXES = ("numpy",)


class _Unpickler(pickle.Unpickler):
    def find_class(self, module: str, name: str) -> Any:
        if (
            (module, name) in _ALLOWED_EXACT
            or module.startswith(_ALLOWED_MODULES)
            or module.startswith(_ALLOWED_PREFIXES)
        ):
            return super().find_class(module, name)
        raise pickle.UnpicklingError(
            f"the checkpoint names {module}.{name}, which a checkpoint may not hold"
        )


def checkpoint_bytes(world: World) -> bytes:
    """The world's state as a checkpoint, in memory (the tests time it)."""
    buf = io.BytesIO()
    _Pickler(buf, protocol=pickle.HIGHEST_PROTOCOL).dump(world)
    return buf.getvalue()


def write_checkpoint(world: World, path: str | Path) -> Path:
    """Write the world's whole state beside its save. The header names the save it
    belongs to: the seed, the end tick, the journal's length and the log's digest."""
    path = Path(path)
    header = {
        "format": CHECKPOINT_FORMAT,
        "engine": world.save()["engine"],
        "build": build_stamp(),  # the build that wrote it (package 37d)
        "seed": world.seed,
        "end_tick": world.clock.tick,
        "journal_len": len(world.journal),
        "inputs_len": len(world.inputs),
        "digest": world.log.digest(),
    }
    body = checkpoint_bytes(world)
    with gzip.open(path, "wb", compresslevel=1) as f:
        f.write(json.dumps(header).encode("utf-8") + b"\n")
        f.write(body)
    return path


def read_checkpoint(path: str | Path) -> tuple[dict[str, Any], World]:
    """The checkpoint's header and the world it holds, with its hooks rebound: the chart
    by its region, the lookout's chart, the coast hook, the ship's stepper and order
    handler, and each agent's model a spent transcript for the driver to replace."""
    with gzip.open(path, "rb") as f:
        header = json.loads(f.readline().decode("utf-8"))
        if header.get("format") != CHECKPOINT_FORMAT:
            raise ValueError(
                f"{path}: checkpoint format {header.get('format')} is not {CHECKPOINT_FORMAT}"
            )
        world = _Unpickler(f).load()
    _rebind(world)
    return header, world


def _rebind(world: World) -> None:
    # the builds the game has been played under (package 37d): this one joins them when it
    # takes the game up; a checkpoint from before the stamp has none, and begins with None
    lineage = [None] if world.played_under is None else list(world.played_under)
    here = build_stamp()
    if not lineage or lineage[-1] != here:
        lineage.append(here)
    world.played_under = lineage
    if world.scenario.region:
        from freesail.world.chart import load_chart

        world.chart = load_chart(world.scenario.region)
        if world.lookout is not None:
            world.lookout.chart = world.chart
        if world.systems is not None:
            world.systems.coast = world._coast_of_plane
            world.systems.coast_trend = world._coast_trend_of_plane
    ship = world.ship
    if getattr(ship, "extra", None) is not None and "evolutions" in ship.extra:
        from freesail.api.session import rebind_hooks

        rebind_hooks(ship)
    if world.agents:
        # a station loaded from its checkpoint has played its transcript already: it gets
        # a spent `Playback`, as a replayed one has once its replies are given, so that the
        # agent API knows it for a loaded station its model may take over (package 37b;
        # with a bare `Transcript` the desk took it for the game's own scripted agent and
        # refused every door: "manned already in this game ... --watcher fake")
        from freesail.agents.harness import Playback

        for agent in world.agents.values():
            if agent.model is None:
                agent.model = Playback(world, [])


def matches(header: dict[str, Any], data: dict[str, Any]) -> bool:
    """Whether a checkpoint's header belongs to a save's data."""
    return (
        int(header.get("seed", -1)) == int(data["seed"])
        and int(header.get("end_tick", -1)) == int(data["end_tick"])
        and int(header.get("journal_len", -1)) == len(data["journal"])
        and int(header.get("inputs_len", -1)) == len(data.get("inputs") or [])
    )


# ---------------------------------------------------------------------------
# The load's rule and its words (package 37d; the review of gate 5c's playtests, section
# 6 under "The cost CHANGES does not state" and section 9 under "Replay")
# ---------------------------------------------------------------------------
#
# A save is exact from its checkpoint, and a replay is promised only on the build that
# wrote it. A station's orders are not in the journal: a replay hands its recorded replies
# back where today's rules open a sample, so under another build's rules (what wakes a
# station, what is urgent, how the wind and the account behave) the replies land elsewhere
# and the game replayed is not the game that was played. So `load` says which road it
# took and why, and does not replay another build's game with a station's transcript in
# it unless it is told to (`replay_anyway`; every door's `--replay-anyway`).

# why a checkpoint was not taken, as `LoadReport.checkpoint` says it
NO_CHECKPOINT = "there is no checkpoint beside the save"
NOT_THIS_SAVES = "the checkpoint beside it is not this save's"
COULD_NOT_BE_READ = "the checkpoint beside it could not be read"
NOT_ASKED = "this door replays a save from its journal and reads no checkpoint"


class ReplayRefused(ValueError):
    """A replay that would not be the game that was played, refused in plain words (the
    build that wrote the save, this build, why the checkpoint was not used); `report` is
    the load's report. A door prints the words and stops, or replays with
    `replay_anyway`."""

    def __init__(self, report: LoadReport):
        super().__init__(" ".join(report.words))
        self.report = report


@dataclass
class LoadReport:
    """What a load did, for the door that asked: the road ("checkpoint", "replay", or
    "refused"), the stamp of the build that wrote the save (None: unstamped) and of the
    checkpoint taken, whether each is this build's, why a checkpoint was not taken ("" when
    it was), the stations whose transcripts the save holds with the count of their
    recorded replies, and the words to print, a line each."""

    path: str
    how: str = "replay"
    build: dict[str, Any] | None = None
    same_build: bool = False
    checkpoint_build: dict[str, Any] | None = None
    checkpoint: str = ""
    transcripts: dict[str, int] = field(default_factory=dict)
    anyway: bool = False
    words: list[str] = field(default_factory=list)


def stamp_of(data: dict[str, Any]) -> dict[str, Any] | None:
    """The stamp a save or a checkpoint's header carries, or None for one written before
    package 37d."""
    stamp = data.get("build")
    return dict(stamp) if isinstance(stamp, dict) and stamp.get("rules") else None


def same_build(stamp: dict[str, Any] | None) -> bool:
    """Whether a stamp is this build's: the same fingerprint of the rules (the name is
    set by hand and is for the reader)."""
    return stamp is not None and stamp.get("rules") == build_stamp()["rules"]


def played_under(data: dict[str, Any]) -> list[dict[str, Any] | None]:
    """Every build a save's game was played under, oldest first (`"builds"`; None for one
    from before the stamp): the build that wrote it alone, for a save without the list."""
    builds = data.get("builds")
    if not isinstance(builds, list) or not builds:
        return [stamp_of(data)]
    return [dict(b) if isinstance(b, dict) and b.get("rules") else None for b in builds]


def transcripts_in(data: dict[str, Any]) -> dict[str, int]:
    """The stations whose transcripts a save holds, each with the count of its recorded
    replies and stops: what a replay would hand back."""
    out: dict[str, int] = {}
    for record in data.get("agents") or []:
        entries = record.get("transcript") or []
        if entries:
            out[str((record.get("station") or {}).get("name") or "station")] = len(entries)
    return out


def _transcript_words(transcripts: dict[str, int]) -> str:
    names = [
        f"the {name}'s transcript ({n} {'reply' if n == 1 else 'replies'})"
        for name, n in transcripts.items()
    ]
    return ", ".join(names[:-1]) + (" and " if len(names) > 1 else "") + names[-1]


def check_replay(
    data: dict[str, Any], path: str | Path = "", replay_anyway: bool = False, why: str = NOT_ASKED
) -> LoadReport:
    """The rule for a replay of a save's data, before it is run (`why`: why its
    checkpoint is not used): the report with its words, or `ReplayRefused` for a save from
    another build, or unstamped, that holds a station's transcript and was not asked for
    with `replay_anyway`."""
    stamp = stamp_of(data)
    # this build's own game: written by it, and played under no other on the way (a game
    # taken up from another build's checkpoint and saved again is not)
    others = [b for b in played_under(data) if not same_build(b)]
    report = LoadReport(
        str(path),
        "replay",
        stamp,
        same_build(stamp) and not others,
        checkpoint=why,
        transcripts=transcripts_in(data),
        anyway=replay_anyway,
    )
    here = build_words(build_stamp())
    if report.same_build:
        report.words = [f"Replayed from its journal: {why}. The save is this build's ({here})."]
        return report
    if same_build(stamp):
        wrote = (
            f"The save was written by this build ({here}), but the game in it was played in "
            f"part under another ({build_words(others[0])}) and taken up from its checkpoint."
        )
    else:
        wrote = f"The save was written by another build ({build_words(stamp)}); this is {here}."
    if not report.transcripts:
        report.words = [
            wrote,
            f"It was replayed from its journal under this build's rules, since {why}: the "
            "log may differ from the one that was watched.",
        ]
        return report
    held = _transcript_words(report.transcripts)
    differs = (
        f"It holds {held}, and a replay under this build's rules would not be the game that "
        "was played: a station's orders are not in the journal, and its recorded replies are "
        "handed back wherever today's rules open a sample."
    )
    if replay_anyway:
        report.words = [
            wrote,
            f"Replayed all the same, as asked (--replay-anyway), since {why}.",
            f"{differs} Read its log as another game from the same beginning.",
        ]
        return report
    report.how = "refused"
    report.words = [
        f"Not replayed: {path}." if str(path) else "Not replayed.",
        wrote,
        f"Its checkpoint was not used: {why}.",
        differs,
        "Load it under the build that wrote it, or with its checkpoint beside it (a save is "
        "exact from its checkpoint); to replay it all the same, say --replay-anyway.",
    ]
    raise ReplayRefused(report)


def load_report(
    path: str | Path, ship_factory: ShipFactory | None = None, replay_anyway: bool = False
) -> tuple[World, LoadReport]:
    """A saved game at its last tick with the report of how it was loaded: from its
    checkpoint when one lies beside it, belongs to it and reads (its log's digest
    checked); else by replaying its journal under `check_replay`'s rule, which refuses
    (`ReplayRefused`) another build's game with a station's transcript in it unless
    `replay_anyway`. Every failure to read a checkpoint is "could not be read", with the
    error's words."""
    data = load_file(path)
    cp = checkpoint_path(path)
    why = NO_CHECKPOINT
    if cp.exists():
        try:
            header, world = read_checkpoint(cp)
        except Exception as e:  # noqa: BLE001  (an import error, a class reshaped, a bad file)
            header, world = {}, None
            said = " ".join(str(e).split()) or "no words"
            why = f"{COULD_NOT_BE_READ} ({type(e).__name__}: {said})"
        if world is not None:
            if not matches(header, data):
                why = (
                    f"{NOT_THIS_SAVES} (it was written at tick {header.get('end_tick')} of "
                    f"seed {header.get('seed')} after {header.get('inputs_len')} inputs; the "
                    f"save ends at tick {data['end_tick']} of seed {data['seed']} after "
                    f"{len(data.get('inputs') or [])})"
                )
            elif world.log.digest() != header.get("digest"):
                why = (
                    f"{COULD_NOT_BE_READ} (the log it holds has not the digest it was written with)"
                )
            else:
                stamp = stamp_of(data)
                written_by = stamp_of(header)
                report = LoadReport(
                    str(path),
                    "checkpoint",
                    stamp,
                    same_build(stamp),
                    checkpoint_build=written_by,
                    transcripts=transcripts_in(data),
                )
                if not same_build(written_by):
                    report.words = [
                        f"The checkpoint was written by another build "
                        f"({build_words(written_by)}) and is read by this one "
                        f"({build_words(build_stamp())}): the game goes on from where it "
                        "was saved, under this build's rules."
                    ]
                return world, report
    report = check_replay(data, path, replay_anyway, why)
    world = replay(data, ship_factory)
    # the player's pencil on the chart (package 37n): a replay makes none of it, and a
    # load gives the save's back as the save has it, so that a game loaded at the console
    # and saved again keeps it; the browser's server reads and cleans it for the chart
    # (`ui.server.take_marks`)
    world.chart_marks = [dict(m) for m in data.get("chart_marks") or [] if isinstance(m, dict)]
    return world, report


def load(
    path: str | Path, ship_factory: ShipFactory | None = None, replay_anyway: bool = False
) -> tuple[World, str]:
    """A saved game at its last tick, from its checkpoint when one lies beside it and
    belongs to it (its log's digest checked), else by replaying its journal. Returns
    the world and how it was loaded: "checkpoint" or "replay" (`load_report` gives the
    whole report; the rule and the refusal are its)."""
    world, report = load_report(path, ship_factory, replay_anyway)
    return world, report.how
