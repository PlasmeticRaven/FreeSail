"""Compose a sailing world: load a ship, attach evolutions, physics and Orders.

This is the one place that knows how the packages fit together (see
docs/dev/M1-WorkPackages.md, "Integration"). Everything else talks to the
World and the Ship through their small interfaces.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from freesail import units
from freesail.core.world import Scenario, World
from freesail.ship.graph import Ship
from freesail.ship.loader import load_ship


def attach_systems(ship: Ship) -> Ship:
    """Give a bare Ship its evolution runner, physics stepper and order handler."""
    from freesail.evolutions.runner import Runner
    from freesail.evolutions.trim import tend_sheets
    from freesail.orders import handle as handle_order
    from freesail.physics import integrate

    runner = Runner(ship)

    def stepper(s: Ship, dt: float, wind: Any) -> None:
        runner.step(s, dt, wind)
        tend_sheets(s, dt)
        integrate.step(s, dt, wind)

    ship.stepper = stepper
    ship.order_handler = handle_order
    return ship


def make_ship(path: str | Path, scenario: Scenario | None = None) -> Ship:
    ship = attach_systems(load_ship(path))
    if scenario is not None:
        ship.dyn.x = scenario.ship_x
        ship.dyn.y = scenario.ship_y
        ship.dyn.heading = units.wrap_2pi(units.deg_to_rad(scenario.ship_heading_deg))
        ship.dyn.target_heading = ship.dyn.heading
        ship.dyn.u = units.knots_to_ms(scenario.ship_speed_kn)
        ship.dyn.speed = ship.dyn.u
    return ship


def make_world(seed: int, ship_path: str | Path, scenario: Scenario | None = None) -> World:
    scenario = scenario or Scenario()
    world = World(seed=seed, scenario=scenario, ship=make_ship(ship_path, scenario))
    ship = world.ship
    if getattr(ship, "spec", None) is not None and ship.spec.crew is not None:
        from freesail.crew import muster

        # The muster is a function of the seed, like everything else (spec M3 §2.4).
        ship.extra["crew"] = muster(ship.spec.crew, world.rng.stream("muster"), ship_name=ship.name)
    return world


def ship_factory(ship_ref: dict[str, Any], scenario: Scenario) -> Any:
    """For replay: rebuild the ship a save refers to. Point ships return None (the default)."""
    if ship_ref.get("type") == "file":
        return make_ship(ship_ref["path"], scenario)
    return None
