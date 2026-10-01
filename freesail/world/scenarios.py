"""Scenario files (spec M4 §19): a day's setting as data, for `--scenario FILE`.

A scenario file (`data/scenarios/<name>.yaml`) says where and when the day begins, what
ship, and what the weather does, and may name the standing orders read at the start and
the captain's first orders:

    name: The gate's day
    seed: 7                          # the seed a driver uses unless --seed is given
    start: 1805-06-01T04:00          # ship's time at tick 0
    latitude_deg: 50.0               # the sun's (spec M4 §5), on the endless plane
    position: 49 52 N 6 10 W         # or {lat_deg: 49.87, lon_deg: -6.17}: the geographic
                                     # frame (spec M5 §9); the sun then reads the ship's
    region: channel-west             # a chart region of data/charts/manifest.yaml (spec M5
                                     # §10): the depth, the coast, the lookout's features
    ship:
      file: data/ships/frigate-36.yaml
      heading_deg: 180
      speed_kn: 0                    # optional, and x_m, y_m
      glass: true                    # she carries a barometer (spec M5 §5; rare in a small vessel)
      chronometer:                   # the captain's own (spec M5 §14, package 33b); none by default
        {maker: Earnshaw, rated: 1805-05-01, rate_s_per_day: 1.8, drift: seeded}
    wind:
      gustiness: 0.3                 # physics/wind.py's
      variability: 0.3
      air_mass: neutral              # optional: the air under a fixed or pinned wind (spec
                                     # M5 §3; package 31b): warm, neutral or unstable
    weather:                         # spec M5 §2: two forms
      wind:                          # the pinned wind (freesail.world.weather_script)
        - {at: 1805-06-01T04:00, from_deg: 270, knots: 18}
        - {at: 1805-06-01T22:00, from_deg: 315, knots: 36, air_mass: unstable}  # from here on
        - ...
      systems:                       # the systems (freesail.world.weather)
        - name: the low
          kind: low
          radius_km: 450
          fronts: {warm_deg: 140, cold_deg: 300}
          track:
            - {at: 1805-06-01T04:00, x_km: -300, y_km: 500, hpa: 990}
            - ...
      climatology: false             # or seed the month's from data/weather/climatology.yaml
      background: {hpa: 1015, gradient_hpa_per_100km: 1.0, high_toward_deg: 190}   # optional
      sea: true                      # optional: keep the sea and the motion (spec M5 §4)
                                     # under a pinned or a fixed wind too; false keeps none

A bare list under `weather` is the old form, the pinned wind alone. With both forms the
pinned wind wins and the systems give only the sky and the glass; with systems alone the
systems' surface wind at the ship is the base wind (spec M5 §2), and the sea and the
ship's motion are kept with it (spec M5 §4; `sea` above overrides either way).
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
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml

from freesail import units
from freesail.core.world import Scenario, World
from freesail.physics.wind import AIR_MASSES
from freesail.world.geo import Position, format_position
from freesail.world.weather import WeatherError, _system_from_dict
from freesail.world.weather_script import WeatherScript

# The seed a driver uses when neither the command line nor the file names one (the
# drivers' own default, freesail/ui/console.py and server.py).
DEFAULT_SEED = 1805


class ScenarioError(ValueError):
    """A scenario file that cannot be read, in words that name the file and the field."""


def _an(word: str) -> str:
    return f"an {word}" if word[:1] in "aeiou" else f"a {word}"


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
        """What the driver prints when the scenario is loaded (the author's view: the
        systems by name, which no log line ever gives)."""
        out = [f"Scenario: {self.scenario.name} ({self.path})."]
        if self.scenario.position:
            where = format_position(Position.from_dict(self.scenario.position))
            chart = f", on the chart of {self.scenario.region}" if self.scenario.region else ""
            out.append(f"She starts at {where}{chart}.")
        if self.script is not None:
            out += ["The weather: " + self.script.lines()[0]]
            out += ["  " + ln for ln in self.script.lines()[1:]]
        sc = self.scenario
        if sc.air_mass != "neutral" and not (sc.systems and not sc.weather):
            out.append(f"The air {sc.air_mass} under the pinned wind.")
        if sc.systems:
            which = "the sky and the glass" if sc.weather else "the wind, the sky and the glass"
            out.append(f"The systems ({which}):")
            for d in sc.systems:
                track = d.get("track") or []
                first, last = track[0], track[-1]
                out.append(
                    f"  {d['name']} ({d.get('kind', 'low')}, radius "
                    f"{d.get('radius_km', 500):g} km): "
                    f"{first['hpa']:g} hPa at {first['at'][11:16]}, {last['hpa']:g} hPa at "
                    f"{last['at'][11:16]}, {len(track)} waypoints."
                )
        elif sc.climatology:
            out.append(f"The weather from the climatology for {sc.start_time.strftime('%B')}.")
        if sc.glass:
            out.append("She carries a glass.")
        if sc.position:
            out.append(f"The master takes the noon sight with {_an(sc.instrument)}.")
        if sc.chronometer:
            c = sc.chronometer
            rate = float(c.get("rate_s_per_day", 0.0))
            sense = "gaining" if rate >= 0 else "losing"
            drift = c.get("drift", "seeded")
            if drift == "seeded":
                known = "its drift drawn from the seed"
            elif not drift:
                known = "its rate right"
            else:
                known = f"its true rate {drift:+g} s a day from that"
            out.append(
                f"She carries a chronometer by {c.get('maker')}, rated on {c.get('rated')} at "
                f"{sense} {abs(rate):g} s a day by its certificate ({known}: the author's view)."
            )
        if sc.current and sc.current.get("knots"):
            toward = units.point_name(units.deg_to_rad(float(sc.current["toward_deg"])))
            out.append(
                f"A current of {sc.current['knots']:g} knots sets toward {toward} (the author's "
                f"view; the master does not know it)."
            )
        if sc.sky:
            said = ", ".join(f"{k} {v}" for k, v in sc.sky.items())
            out.append(f"The sky pinned: {said}.")
        keeps_sea = sc.sea if sc.sea is not None else bool(sc.systems or sc.climatology)
        keeps_sea = keeps_sea and (sc.sea is not None or not sc.weather)
        if keeps_sea:
            out.append("The sea and the ship's motion are kept.")
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
    if raw.get("position") is not None:
        # the geographic frame (spec M5 §9): the sun reads the ship's latitude from here
        try:
            position = Position.from_dict(raw["position"])
        except (TypeError, ValueError) as e:
            raise ScenarioError(f"{where}, position: {e}") from None
        sc.position = position.to_dict()
        sc.latitude_deg = position.lat_deg
    if raw.get("region") is not None:
        sc.region = str(raw["region"])
        if sc.position is None:
            raise ScenarioError(
                f"{where}: the chart region '{sc.region}' needs a position (49 52 N 6 10 W)."
            )
    ship = raw.get("ship") or {}
    wind = raw.get("wind") or {}
    sc.glass = bool(ship.get("glass", raw.get("glass", False)))
    # the master's instrument for the noon sight (spec M5 §14, package 33a): the ship's
    # line or the file's; the octant unless the file says the sextant
    instrument = ship.get("instrument", raw.get("instrument"))
    if instrument is not None:
        sc.instrument = str(instrument).strip().lower()
        if sc.instrument not in ("sextant", "octant"):
            raise ScenarioError(
                f"{where}, instrument: '{instrument}' is not an instrument; say sextant or octant."
            )
    # the chronometer (package 33b; spec M5 §14; N §4(b)): the captain's own, as
    # {maker, rated, rate_s_per_day, drift: seeded | seconds a day, forgotten: [dates]};
    # on the ship's line or the file's; none by default (rare in a small vessel)
    chron = ship.get("chronometer", raw.get("chronometer"))
    if chron is not None:
        if not isinstance(chron, dict):
            raise ScenarioError(
                f"{where}, chronometer: a mapping of maker, rated, rate_s_per_day and drift."
            )
        try:
            rated = chron.get("rated", sc.start_time.date())
            rated_day = rated if isinstance(rated, date) else date.fromisoformat(str(rated))
            drift = chron.get("drift", "seeded")
            if not (isinstance(drift, str) and drift.strip().lower() == "seeded"):
                drift = float(drift or 0.0)
            else:
                drift = "seeded"
            forgotten = [
                (d if isinstance(d, date) else date.fromisoformat(str(d))).isoformat()
                for d in (chron.get("forgotten") or [])
            ]
            sc.chronometer = {
                "maker": str(chron.get("maker") or "the chronometer"),
                "where": str(chron.get("where") or chron.get("rated_at") or ""),
                "rated": rated_day.isoformat(),
                "rate_s_per_day": float(chron.get("rate_s_per_day", 0.0) or 0.0),
                "drift": drift,
                "forgotten": forgotten,
            }
        except (TypeError, ValueError) as e:
            raise ScenarioError(f"{where}, chronometer: {e}") from None
    # the world's stated current (package 33a; none by default): {knots, toward_deg}
    current = raw.get("current")
    if current is not None:
        if not isinstance(current, dict):
            raise ScenarioError(f"{where}, current: knots and toward_deg.")
        try:
            sc.current = {
                "knots": float(current.get("knots", 0.0)),
                "toward_deg": float(current.get("toward_deg", 0.0)),
            }
        except (TypeError, ValueError):
            raise ScenarioError(f"{where}, current: numbers only.") from None
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
    if wind.get("air_mass") is not None:
        air = str(wind["air_mass"]).strip().lower()
        if air not in AIR_MASSES:
            airs = ", ".join(AIR_MASSES)
            raise ScenarioError(f"{where}, wind air_mass: '{air}' is not an air; say {airs}.")
        sc.air_mass = air
    weather = raw.get("weather") or []
    systems: list[Any] = []
    if isinstance(weather, dict):
        # the M5 form: a mapping of the pinned `wind`, the `systems` and `climatology`
        systems = list(weather.get("systems") or [])
        sc.climatology = bool(weather.get("climatology", False))
        if "sea" in weather and weather["sea"] is not None:
            sc.sea = bool(weather["sea"])
        # the sky pinned (package 33a): {sky, weather, visibility} in the readings' words
        if weather.get("sky") is not None:
            from freesail.world.weather import SKY_WORDS, VISIBILITY_WORDS, WEATHER_WORDS

            pin = weather["sky"]
            if not isinstance(pin, dict):
                raise ScenarioError(f"{where}, weather sky: a mapping of sky, weather, visibility.")
            allowed = {"sky": SKY_WORDS, "weather": WEATHER_WORDS, "visibility": VISIBILITY_WORDS}
            sc.sky = {}
            for k, v in pin.items():
                if k not in allowed:
                    raise ScenarioError(
                        f"{where}, weather sky: '{k}' is not sky, weather or visibility."
                    )
                if str(v) not in allowed[k]:
                    raise ScenarioError(
                        f"{where}, weather sky {k}: '{v}' is not one of {', '.join(allowed[k])}."
                    )
                sc.sky[k] = str(v)
            if not systems and not weather.get("climatology"):
                raise ScenarioError(
                    f"{where}, weather sky: a pinned sky is laid over the systems' weather; "
                    f"give systems or the climatology beside it."
                )
        background = weather.get("background") or {}
        if not isinstance(background, dict):
            raise ScenarioError(
                f"{where}, weather background: hpa, gradient_hpa_per_100km, high_toward_deg."
            )
        try:
            sc.background = {k: float(v) for k, v in background.items()}
        except (TypeError, ValueError):
            raise ScenarioError(f"{where}, weather background: numbers only.") from None
        weather = weather.get("wind") or []
    if not isinstance(weather, list):
        raise ScenarioError(
            f"{where}, weather: a list of wind waypoints, or a mapping of wind, systems and "
            f"climatology."
        )
    given, systems = systems, []
    for i, d in enumerate(given):
        if not isinstance(d, dict):
            raise ScenarioError(
                f"{where}, systems {i + 1}: a system is a mapping (name, kind, radius_km, "
                f"fronts, track)."
            )
        track = []
        for j, w in enumerate(d.get("track") or []):
            if not isinstance(w, dict):
                raise ScenarioError(
                    f"{where}, systems {i + 1}, waypoint {j + 1}: at, x_km, y_km, hpa."
                )
            track.append(
                {
                    **w,
                    "at": _time(
                        w.get("at"), f"{where}, systems {i + 1}, waypoint {j + 1}"
                    ).isoformat(),
                }
            )
        entry = {**d, "track": track}
        try:
            _system_from_dict(entry, sc.start_time)  # refused in words
        except WeatherError as e:
            raise ScenarioError(f"{where}: {e}") from None
        systems.append(entry)
    sc.systems = systems
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
