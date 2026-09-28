"""Scenario files (spec M4 §19): a day's setting as data, for `--scenario FILE`.

A scenario file (`data/scenarios/<name>.yaml`) says where and when the day begins, what
ship, and what the weather does, and may name the standing orders read at the start and
the captain's first orders:

    name: The gate's day
    seed: 7                          # the seed a driver uses unless --seed is given
    start: 1805-06-01T04:00          # ship's time at tick 0
    latitude_deg: 50.0               # the sun's (spec M4 §5)
    ship:
      file: data/ships/frigate-36.yaml
      heading_deg: 180
      speed_kn: 0                    # optional, and x_m, y_m
    wind:
      gustiness: 0.3                 # physics/wind.py's, as the M2 wind
      variability: 0.3
    weather:                         # the script (freesail.world.weather_script)
      - {at: 1805-06-01T04:00, from_deg: 270, knots: 18}
      - ...
    standing_orders:                 # files read at the start, in order
      - data/standing_orders/starter.orders
    orders:                          # the captain's first orders, given at tick 0
      - set plain sail

Everything the World needs goes into its `Scenario` (the script included), so a save
holds it and a replay follows it; the standing orders and the first orders are given as
orders, journaled like any, so a replay gives them again. A driver builds the World with
`start`: the ship, the watcher (if asked for) and then the files and the orders, which is
the order `--standing-orders` has always kept.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

from freesail.core.world import Scenario, World
from freesail.world.weather_script import WeatherScript

# The seed a driver uses when neither the command line nor the file names one (the
# drivers' own default, freesail/ui/console.py and server.py).
DEFAULT_SEED = 1805


class ScenarioError(ValueError):
    """A scenario file that cannot be read, in words that name the file and the field."""


@dataclass
class ScenarioFile:
    """A scenario file read: the World's `Scenario`, and what the driver does with it."""

    path: str
    scenario: Scenario
    seed: int | None = None
    ship_file: str | None = None
    standing_orders: list[str] = field(default_factory=list)
    orders: list[str] = field(default_factory=list)

    @property
    def script(self) -> WeatherScript | None:
        return WeatherScript.from_list(self.scenario.weather) if self.scenario.weather else None

    def lines(self) -> list[str]:
        """What the driver prints when the scenario is loaded."""
        out = [f"Scenario: {self.scenario.name} ({self.path})."]
        if self.script is not None:
            out += ["The weather: " + self.script.lines()[0]]
            out += ["  " + ln for ln in self.script.lines()[1:]]
        return out


def _time(value: Any, where: str) -> datetime:
    if isinstance(value, datetime):
        return value
    try:
        return datetime.fromisoformat(str(value))
    except ValueError:
        raise ScenarioError(f"{where}: '{value}' is not a time like 1805-06-01T04:00.") from None


def load_scenario(path: str | Path) -> ScenarioFile:
    """Read a scenario file. Raises `ScenarioError` (or `OSError`) in words."""
    p = Path(path)
    raw = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    if not isinstance(raw, dict):
        raise ScenarioError(f"{p}: a scenario file is a mapping of fields.")
    where = str(p)
    sc = Scenario()
    sc.name = str(raw.get("name") or p.stem)
    if "start" in raw:
        sc.start_time = _time(raw["start"], f"{where}, start")
    if "latitude_deg" in raw:
        sc.latitude_deg = float(raw["latitude_deg"])
    ship = raw.get("ship") or {}
    wind = raw.get("wind") or {}
    try:
        sc.ship_heading_deg = float(ship.get("heading_deg", sc.ship_heading_deg))
        sc.ship_speed_kn = float(ship.get("speed_kn", sc.ship_speed_kn))
        sc.ship_x = float(ship.get("x_m", sc.ship_x))
        sc.ship_y = float(ship.get("y_m", sc.ship_y))
        sc.gustiness = float(wind.get("gustiness", sc.gustiness))
        sc.variability = float(wind.get("variability", sc.variability))
        sc.wind_from_deg = float(wind.get("from_deg", sc.wind_from_deg))
        sc.wind_speed_kn = float(wind.get("knots", sc.wind_speed_kn))
    except (TypeError, ValueError, AttributeError) as e:
        raise ScenarioError(f"{where}: {e}") from None
    weather = raw.get("weather") or []
    if weather:
        entries = []
        for i, w in enumerate(weather):
            if not isinstance(w, dict):
                raise ScenarioError(f"{where}, weather {i + 1}: a waypoint is at, from_deg, knots.")
            entries.append({**w, "at": _time(w.get("at"), f"{where}, weather {i + 1}")})
        try:
            script = WeatherScript.from_list(entries)
        except ValueError as e:
            raise ScenarioError(f"{where}: {e}") from None
        sc.weather = script.to_list()
        first = script.waypoints[0]
        # the fixed wind fields say the wind at the start, for anyone reading the save
        sc.wind_from_deg, sc.wind_speed_kn = first.from_deg, first.knots
    seed = raw.get("seed")
    return ScenarioFile(
        path=str(path),
        scenario=sc,
        seed=int(seed) if seed is not None else None,
        ship_file=str(ship["file"]) if ship.get("file") else None,
        standing_orders=[str(x) for x in raw.get("standing_orders") or []],
        orders=[str(x) for x in raw.get("orders") or []],
    )


def make_scenario_world(sf: ScenarioFile, seed: int | None = None, ship: str | None = None):
    """The World of a scenario file, at tick 0, with nothing given yet: the seed is the
    command line's, else the file's, else `DEFAULT_SEED`; the ship the command line's,
    else the file's, else the point ship."""
    from freesail.api.session import make_world

    use_seed = seed if seed is not None else sf.seed if sf.seed is not None else DEFAULT_SEED
    ship_file = ship or sf.ship_file
    if ship_file:
        return make_world(use_seed, ship_file, sf.scenario)
    return World(seed=use_seed, scenario=sf.scenario)


def begin(world: World, sf: ScenarioFile) -> int:
    """Give the scenario's standing orders files and first orders to the World, as the
    captain's orders (journaled). Returns how many orders were given."""
    from freesail.ui.console import read_standing_orders

    n = 0
    for path in sf.standing_orders:
        n += read_standing_orders(world, path)
    for text in sf.orders:
        world.submit(text)
        n += 1
    return n
