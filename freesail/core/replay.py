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
"""

from __future__ import annotations

import gzip
import io
import json
import pickle
from collections.abc import Callable
from pathlib import Path
from typing import Any

from freesail.core.world import SAVE_FORMAT, Scenario, World

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
        while i < len(inputs) and int(inputs[i]["tick"]) == world.clock.tick:
            _give(world, inputs[i])
            i += 1
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
    if world.scenario.region:
        from freesail.world.chart import load_chart

        world.chart = load_chart(world.scenario.region)
        if world.lookout is not None:
            world.lookout.chart = world.chart
        if world.systems is not None:
            world.systems.coast = world._coast_of_plane
    ship = world.ship
    if getattr(ship, "extra", None) is not None and "evolutions" in ship.extra:
        from freesail.api.session import rebind_hooks

        rebind_hooks(ship)
    if world.agents:
        from freesail.agents.fake import Transcript

        for agent in world.agents.values():
            if agent.model is None:
                agent.model = Transcript([])


def matches(header: dict[str, Any], data: dict[str, Any]) -> bool:
    """Whether a checkpoint's header belongs to a save's data."""
    return (
        int(header.get("seed", -1)) == int(data["seed"])
        and int(header.get("end_tick", -1)) == int(data["end_tick"])
        and int(header.get("journal_len", -1)) == len(data["journal"])
        and int(header.get("inputs_len", -1)) == len(data.get("inputs") or [])
    )


def load(path: str | Path, ship_factory: ShipFactory | None = None) -> tuple[World, str]:
    """A saved game at its last tick, from its checkpoint when one lies beside it and
    belongs to it (its log's digest checked), else by replaying its journal. Returns
    the world and how it was loaded: "checkpoint" or "replay"."""
    data = load_file(path)
    cp = checkpoint_path(path)
    if cp.exists():
        try:
            header, world = read_checkpoint(cp)
        except (OSError, ValueError, pickle.UnpicklingError, EOFError, AttributeError):
            header, world = {}, None
        if (
            world is not None
            and matches(header, data)
            and world.log.digest() == header.get("digest")
        ):
            return world, "checkpoint"
    return replay(data, ship_factory), "replay"
