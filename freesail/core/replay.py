"""Save to disk and rebuild a world by replaying its order journal.

A save is not a snapshot. It is the seed, the scenario, a reference to the
ship, and the list of (tick, actor, order). Replaying it re-runs the
simulation and must produce an identical log; `tests/test_replay.py` holds
the engine to that.
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
    return World(seed=data["seed"], scenario=scenario, ship=ship)


def replay(
    data: dict[str, Any],
    ship_factory: ShipFactory | None = None,
    until_tick: int | None = None,
) -> World:
    """Rebuild a world and run it to `until_tick` (default: the save's end tick),
    re-submitting journaled orders at their ticks."""
    world = build_world(data, ship_factory)
    end = data["end_tick"] if until_tick is None else min(until_tick, data["end_tick"])
    journal = [(int(t), str(a), str(o)) for t, a, o in data["journal"]]
    i = 0
    while True:
        while i < len(journal) and journal[i][0] == world.clock.tick:
            _, actor, text = journal[i]
            world.submit(text, actor=actor)
            i += 1
        if world.clock.tick >= end:
            break
        world.tick()
    return world


def replay_world(world: World, ship_factory: ShipFactory | None = None) -> World:
    """Replay a live world from its own save. Used by the determinism tests."""
    return replay(world.save(), ship_factory)
