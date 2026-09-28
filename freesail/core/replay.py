"""Save to disk and rebuild a world by replaying its order journal.

A save is not a snapshot. It is the seed, the scenario, a reference to the
ship, and the list of (tick, actor, order). Replaying it re-runs the
simulation and must produce an identical log; `tests/test_replay.py` holds
the engine to that.

Since package 29 a save also holds its `inputs` (`World.inputs`): every order in the
order it was given, refused and queries too, and the lines a driver wrote, so that a
replay at any tick of a played day reproduces the log a player watched, refusals and all.
A save without them replays its journal, as before.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

from freesail.core.world import SAVE_FORMAT, Scenario, World

ShipFactory = Callable[[dict[str, Any], Scenario], Any]


def save_to_file(world: World, path: str | Path) -> Path:
    path = Path(path)
    path.write_text(json.dumps(world.save(), indent=2))
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
    """One input again: an order to the ship, or a driver's line to the log."""
    if "order" in entry:
        world.submit(str(entry["order"]), actor=str(entry["actor"]))
        return
    line = entry["line"]
    world.record_driver(line["severity"], line["kind"], line["text"], line.get("data"))


def replay_world(world: World, ship_factory: ShipFactory | None = None) -> World:
    """Replay a live world from its own save. Used by the determinism tests."""
    return replay(world.save(), ship_factory)
