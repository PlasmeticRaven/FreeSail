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
    region: channel-west             # the region she starts in, on the whole chart that
                                     # holds it (spec M6 §26; package 45: `atlantic-east`
                                     # for every region of the line), or
    chart: atlantic-east             # a chart of the manifest's `charts:` outright, or a
                                     # region's name as a chart of that one region (package
                                     # 38's reading, which only a test should want)
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
    nation: britain                  # the ship's nation (spec M5 §24; package 35); by her
                                     # company's names list when not said
    people:                          # people beyond the muster's posts (§22; package 35)
      - {role: supercargo, name: Mr Pentreath, place: cabin}
    papers: {price_lists: [falmouth]}   # the price lists she starts with (§22)
    cargo: {purse_pounds: 500, goods: {tin: 20}}   # the purse and the hold (§23)
    ports:                           # the ports' state (§23, §27): a list of ids, or each
      brest: {closed_to: [], letters: [{text: "...", origin: Brest}], news: ["..."]}
    ships:                           # the other sail on the sea at the start (§25; package 36)
      - {id: two-brothers, description: merchant brig, name: Two Brothers, nation: britain,
         position: 49 50 N 5 30 W, goal: "trading Falmouth to the Lizard", colours: shown}
    world_orders:                    # orders to the world by time (§26; freesail.world.orders)
      - {at: 1805-06-12T14:00, order: 'message: at Brest from the Prefect maritime: "..."'}
    director:                        # the director (spec M6 §23; M7b §4, package 50)
      brief: quiet-passage           # the player's brief: a starter's name (data/director/
                                     # briefs/), a file, or the mapping itself; the station
                                     # is bound on the World when the game is made
      models: [the model's exact name]   # the owner's grant of seats on other ships (43)
      seats: 1
      seats_in_voyage: 3
    standing_orders:                 # files read at the start, in order
      - data/standing_orders/starter.orders
    orders:                          # the captain's first orders, given at tick 0
      - set plain sail
    stations:                        # who holds the stations (package 59): `player` the
      officer: player                # player's seat (as --seat, which wins), `model` a
      captain: model                 # model's door (the harbour offers it), `rules` the
      director: model                # game's own; one seat for the player at most

The papers may be given whole (§27) under `papers:`: `chart: {year: 1804}`, `epitome:
norie`, `almanac: 1805`, `chronometer: {...}` (the ship's line wins where both say),
`price_lists: [falmouth]`.

Everything the World needs goes into its `Scenario` (the script included), so a save
holds it and a replay follows it; the standing orders and the first orders are given as
orders, journaled like any, so a replay gives them again. A driver builds the World with
`start`: the ship, the watcher (if asked for) and then the files and the orders, which is
the order `--standing-orders` has always kept.

A scenario is written as well as read (package 59; spec M7b §21e): `write_scenario` puts a
mapping of these fields in a file of this form, with the comments a hand would want; given
the text the mapping was read from, it keeps every top-level block of that text whose value
is unchanged, comments and all, and writes again only the blocks that changed, so that a
file read into the harbour's scenario maker and written with nothing changed is the same
file, byte for byte.
"""

from __future__ import annotations

import json
import re
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
    # who holds the stations (package 59): the station's name to player, model or rules
    stations: dict[str, str] = field(default_factory=dict)

    @property
    def player_seat(self) -> str | None:
        """The station the file seats the player at (`stations: {officer: player}`), as
        `--seat` would; None when he is the captain at the prompt or the file says nothing.
        A seat given on the command line wins."""
        for name, holder in self.stations.items():
            if holder == "player" and name != "captain":
                return name
        return None

    @property
    def script(self) -> WeatherScript | None:
        return WeatherScript.from_list(self.scenario.weather) if self.scenario.weather else None

    def lines(self) -> list[str]:
        """What the driver prints when the scenario is loaded (the author's view: the
        systems by name, which no log line ever gives)."""
        out = [f"Scenario: {self.scenario.name} ({self.path})."]
        if self.scenario.position:
            where = format_position(Position.from_dict(self.scenario.position))
            name = self.scenario.chart or self.scenario.region
            chart = f", on the chart of {name}" if name else ""
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
        # package 35: the nation, the cargo and the ports (the author's view)
        if sc.nation:
            out.append(f"She is of {sc.nation.replace('-', ' ')}.")
        cargo = sc.cargo or {}
        if cargo.get("purse_pounds") or cargo.get("goods"):
            goods = ", ".join(f"{t:g} tons of {g}" for g, t in (cargo.get("goods") or {}).items())
            out.append(
                f"The purse holds £{cargo.get('purse_pounds', 0):g}"
                + (f"; the hold {goods}." if goods else ".")
            )
        if sc.ports is not None:
            names = list(sc.ports) if not isinstance(sc.ports, dict) else list(sc.ports)
            out.append(f"The ports: {', '.join(names) if names else 'none'}.")
        # package 36: the other sail and the world orders (the author's view: the truth
        # of where each ship is put and what she is about, which no log line gives)
        if sc.ships:
            out.append(f"Other sail on the sea at the start: {len(sc.ships)}.")
            for s in sc.ships:
                out.append(
                    f"  {s.get('description')} {s.get('name', '')} of {s.get('nation', 'britain')}"
                    f" at {s.get('position')}, {s.get('goal')}."
                )
        if sc.world_orders:
            out.append(f"World orders by time: {len(sc.world_orders)}.")
            for o in sc.world_orders:
                out.append(f"  {str(o['at'])[5:16]}  {o['order']}")
        return out


def guard_lines(world: Any) -> list[str]:
    """The far-detail guard's words on the other sail at the start (package 43; spec M6
    §19), for the driver to print with the scenario's lines, the author's view: a ship
    without a brain whose goal's straight legs cross the land (a ship with a brain is
    refused at the making instead, her captain's plan being the planner's). Nothing of
    this is a line of the log."""
    vessels = getattr(world, "vessels", None)
    out: list[str] = []
    for v in getattr(vessels, "vessels", None) or []:
        if v.warning:
            out.append(
                f"  The far-detail guard: {v.name} ({v.goal}) {v.warning} at far detail, where "
                "no ship takes the ground; give her a way by marks, or a captain (intent:)."
            )
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
    if raw.get("chart") is not None:
        # the chart whole (spec M6 §26; package 38): the file may say either or both, the
        # chart winning; a region's name is a chart of that one region
        sc.chart = str(raw["chart"])
    if (sc.chart or sc.region) and sc.position is None:
        raise ScenarioError(
            f"{where}: the chart region '{sc.chart or sc.region}' needs a position "
            f"(49 52 N 6 10 W)."
        )
    ship = raw.get("ship") or {}
    wind = raw.get("wind") or {}
    sc.glass = bool(ship.get("glass", raw.get("glass", False)))
    # the papers whole (spec M5 §27; package 36): the epitome and the chronometer may be
    # given under `papers:` beside the chart's year and the almanac; the ship's line wins
    papers_raw = raw.get("papers") or {}
    if not isinstance(papers_raw, dict):
        raise ScenarioError(
            f"{where}, papers: a mapping (chart, epitome, almanac, chronometer, price_lists)."
        )
    # the master's epitome for the tide (spec M5 §16, package 34): the ship's line or the
    # file's; a table of data/tides/establishments.yaml (norie, moore); none, the ship's
    # kind chooses (a ship of war Norie's, a merchantman Moore's)
    epitome = ship.get("epitome", raw.get("epitome", papers_raw.get("epitome")))
    if epitome is not None:
        sc.epitome = str(epitome).strip().lower()
        if sc.epitome not in ("norie", "moore"):
            raise ScenarioError(
                f"{where}, epitome: '{epitome}' is not a table of the establishments; say "
                f"norie or moore."
            )
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
    chron = ship.get("chronometer", raw.get("chronometer", papers_raw.get("chronometer")))
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
    # Package 35 (spec M5 §22 to §24, §27): the ship's nation, her people beyond the
    # muster, her papers, her cargo and purse, and the ports' state.
    nation = ship.get("nation", raw.get("nation"))
    if nation is not None:
        from freesail.world.nations import load_nations

        found = load_nations().find(str(nation))
        if found is None:
            raise ScenarioError(
                f"{where}, nation: '{nation}' is not a nation of data/nations.yaml."
            )
        sc.nation = found.id
    people = raw.get("people") or []
    if not isinstance(people, list):
        raise ScenarioError(f"{where}, people: a list of {{role, name, skill, place}}.")
    for i, p in enumerate(people):
        if not isinstance(p, dict) or not str(p.get("role") or "").strip():
            raise ScenarioError(f"{where}, people {i + 1}: a person is a mapping with a role.")
    sc.people = [dict(p) for p in people]
    sc.papers = {str(k): v for k, v in papers_raw.items() if k not in ("epitome", "chronometer")}
    cargo = raw.get("cargo") or {}
    if not isinstance(cargo, dict):
        raise ScenarioError(f"{where}, cargo: a mapping of purse_pounds and goods.")
    try:
        goods = {str(g): float(t) for g, t in (cargo.get("goods") or {}).items()}
        sc.cargo = {"purse_pounds": float(cargo.get("purse_pounds", 0.0) or 0.0), "goods": goods}
    except (TypeError, ValueError, AttributeError):
        raise ScenarioError(
            f"{where}, cargo: purse_pounds a number, goods a mapping of tons."
        ) from None
    if raw.get("ports") is not None:
        ports_raw = raw["ports"]
        if isinstance(ports_raw, list):
            sc.ports = [str(x) for x in ports_raw]
        elif isinstance(ports_raw, dict):
            sc.ports = {str(k): dict(v or {}) for k, v in ports_raw.items()}
        else:
            raise ScenarioError(
                f"{where}, ports: a list of port ids, or a mapping of each port's state."
            )
    # Package 36 (spec M5 §25 to §27): the other sail on the sea at the start, and the
    # world orders by time, each refused in words here rather than at the tick
    ships_raw = raw.get("ships") or []
    if not isinstance(ships_raw, list):
        raise ScenarioError(
            f"{where}, ships: a list of {{id, description, name, nation, position, goal}}."
        )
    from freesail.world.ships import DESCRIPTIONS, description_key

    for i, s in enumerate(ships_raw):
        if not isinstance(s, dict):
            raise ScenarioError(f"{where}, ships {i + 1}: a ship is a mapping.")
        if description_key(str(s.get("description") or s.get("kind") or "")) is None:
            raise ScenarioError(
                f"{where}, ships {i + 1}: '{s.get('description')}' is no description; say one "
                f"of {', '.join(DESCRIPTIONS)}."
            )
        if s.get("position") is None or not str(s.get("goal") or "").strip():
            raise ScenarioError(f"{where}, ships {i + 1}: a ship needs a position and a goal.")
    sc.ships = [{str(k): v for k, v in s.items()} for s in ships_raw]
    # the crewed promotion's budget (the lead, 2026-10-17): `crewed: {cap: N, range_nm: X}`
    if raw.get("crewed") is not None:
        from freesail.world.crews import crewed_settings_of

        sc.crewed = crewed_settings_of(raw["crewed"], where)
    # the world's business (package 43b; spec M6 §19): on, off or a density; off when not said
    if raw.get("business") is not None:
        from freesail.world.business import business_density

        try:
            density = business_density(raw["business"])
        except ValueError as e:
            raise ScenarioError(f"{where}, {e}") from None
        sc.business = "off" if density <= 0.0 else ("on" if density == 1.0 else density)
    orders_raw = raw.get("world_orders") or []
    if not isinstance(orders_raw, list):
        raise ScenarioError(f"{where}, world_orders: a list of {{at, order}}.")
    from freesail.world import orders as world_orders

    for i, o in enumerate(orders_raw):
        if not isinstance(o, dict) or o.get("at") is None or not str(o.get("order") or ""):
            raise ScenarioError(f"{where}, world_orders {i + 1}: at and order.")
        at = _time(o["at"], f"{where}, world_orders {i + 1}")
        text = " ".join(str(o["order"]).split())
        try:
            world_orders.parse(text)
        except world_orders.WorldOrderError as e:
            raise ScenarioError(f"{where}, world_orders {i + 1}: {e}") from None
        sc.world_orders.append({"at": at.isoformat(), "order": text})
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
    standing_orders = [str(x) for x in raw.get("standing_orders") or []]
    # Package 40 (spec M6 §4): the captain's intent beside the book (`intent:`), read
    # against the chart and the ports when the world is made (`freesail.world.captains`);
    # the books' names kept with the scenario for `the captain` reading
    if raw.get("intent") is not None:
        sc.intent = " ".join(str(raw["intent"]).split())
        if not isinstance(raw["intent"], str) or not sc.intent:
            raise ScenarioError(f"{where}, intent: the captain's intent in words.")
    sc.books = list(standing_orders)
    # Package 43 (spec M6 §23): the owner's grant to the director
    if raw.get("director") is not None:
        grant = raw["director"]
        if not isinstance(grant, dict):
            raise ScenarioError(f"{where}, director: a mapping of models, seats, seats_in_voyage.")
        try:
            sc.director = {
                "models": [str(x) for x in (grant.get("models") or [])],
                "seats": int(grant.get("seats", 1) or 0),
                "seats_in_voyage": int(grant.get("seats_in_voyage", grant.get("seats", 1)) or 0),
            }
        except (TypeError, ValueError):
            raise ScenarioError(
                f"{where}, director: seats and seats_in_voyage are numbers."
            ) from None
        if grant.get("brief") is not None:
            # package 50 (spec M7b §4): the player's brief for the director, a starter's
            # name, a file's path or the mapping itself, read now so that a bad one is
            # refused at the load and kept as read so that the save carries it whole
            from freesail.agents.director import resolve_brief

            try:
                brief = resolve_brief(grant["brief"], source=f"the scenario ({where})")
            except (ValueError, OSError) as e:
                raise ScenarioError(f"{where}, director.brief: {e}") from None
            sc.director["brief"] = brief.to_dict()
    return ScenarioFile(
        path=str(path),
        scenario=sc,
        seed=int(seed) if seed is not None else None,
        ship_file=str(ship["file"]) if ship.get("file") else None,
        standing_orders=standing_orders,
        orders=[str(x) for x in raw.get("orders") or []],
        stations=_stations(raw.get("stations"), where),
    )


# Who may hold a station in a scenario file (package 59): the player's seat, a model's
# door, or the game's own (the rules-based captain, a station nobody holds).
STATION_HOLDERS = ("player", "model", "rules")


def _stations(value: Any, where: str) -> dict[str, str]:
    """`stations:`, read: each station's holder, one seat for the player at most."""
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise ScenarioError(
            f"{where}, stations: a mapping of each station to who holds it "
            f"({', '.join(STATION_HOLDERS)})."
        )
    out: dict[str, str] = {}
    for k, v in value.items():
        name = " ".join(str(k).lower().split())
        holder = " ".join(str(v).lower().split())
        if holder not in STATION_HOLDERS:
            raise ScenarioError(
                f"{where}, stations {name}: '{v}' is not a holder; say "
                f"{', '.join(STATION_HOLDERS[:-1])} or {STATION_HOLDERS[-1]}."
            )
        out[name] = holder
    players = [k for k, v in out.items() if v == "player"]
    if len(players) > 1:
        raise ScenarioError(
            f"{where}, stations: the player holds one station, not {' and '.join(players)}."
        )
    return out


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


# ---------------------------------------------------------------------------
# Writing a scenario (package 59; spec M7b §21e): the harbour's scenario maker
# ---------------------------------------------------------------------------

# The fields in the order a new file is written in (the docstring's); a field not named
# here goes at the end. And the comment a hand would want above each section.
FIELD_ORDER: tuple[str, ...] = (
    "name",
    "seed",
    "start",
    "latitude_deg",
    "position",
    "region",
    "chart",
    "nation",
    "ship",
    "wind",
    "intent",
    "people",
    "papers",
    "cargo",
    "ports",
    "business",
    "crewed",
    "current",
    "weather",
    "ships",
    "world_orders",
    "standing_orders",
    "orders",
    "stations",
    "director",
)

SECTION_COMMENTS: dict[str, str] = {
    "position": "Where she lies at the start: a port's road from the chart, or a place pricked "
    "on it, with the chart's region.",
    "ship": "The ship: her file, her heading, the glass and the master's instrument.",
    "intent": "The captain's intent (spec M6 §4): the rules captain sails by it when nobody "
    "holds the station; a model captain reads it as his night orders.",
    "people": "People beyond the muster's posts.",
    "papers": "The ship's papers: the chart's year, the epitome, the almanac, the price lists.",
    "cargo": "The purse and the hold.",
    "ports": "The ports in play, and their state at the start.",
    "business": "The world's business (spec M6 §19): the trade, the fishermen and the cruisers "
    "drawn under the seed.",
    "crewed": "The crewed promotion's budget: how many ships beside hers are fully crewed at "
    "once, and within how many miles.",
    "weather": "The weather: the month's climatology, or the wind pinned by the hour (the "
    "primer's forms).",
    "ships": "The other sail on the sea at the start, each with her intent.",
    "world_orders": "The world orders by time.",
    "standing_orders": "The standing orders read at the start.",
    "orders": "The captain's first orders, given at tick 0.",
    "stations": "Who holds the stations: player (your seat), model (a model's door), rules "
    "(the game's own).",
    "director": "The director above the game (spec M7b §4): the player's brief, a starter's "
    "name, a file or the brief itself, with its limits.",
}

_KEY_LINE = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*:(?:\s|$)")
_FLOW_DICT_MAX = 60  # characters: a mapping of plain values this short is written on one line
_FLOW_LIST_MAX = 90  # and a list of plain values


def scenario_value(value: Any) -> Any:
    """A scenario's value as JSON carries it (the harbour's form): dates and times as their
    ISO words, tuples as lists, a mapping's keys as words."""
    if isinstance(value, datetime | date):
        return value.isoformat()
    if isinstance(value, dict):
        return {str(k): scenario_value(v) for k, v in value.items()}
    if isinstance(value, list | tuple):
        return [scenario_value(v) for v in value]
    return value


def _same_value(v: Any) -> Any:
    """A value for comparing what a form sent with what a file held: a whole float is its
    integer (a form's 190 is a file's 190.0); a boolean stays a boolean."""
    v = scenario_value(v)
    if isinstance(v, bool) or v is None or isinstance(v, str):
        return v
    if isinstance(v, int | float):
        f = float(v)
        return int(f) if f.is_integer() else f
    if isinstance(v, dict):
        return {k: _same_value(x) for k, x in v.items()}
    if isinstance(v, list):
        return [_same_value(x) for x in v]
    return v


def same_fields(a: Any, b: Any) -> bool:
    """Whether two scenarios' fields (or two fields) say the same, as `_same_value` reads them."""
    return json.dumps(_same_value(a), sort_keys=True) == json.dumps(_same_value(b), sort_keys=True)


def read_scenario_text(path: str | Path) -> tuple[str, dict[str, Any]]:
    """A scenario file's text and its fields as the harbour's form takes them. Raises
    `ScenarioError` (or `OSError`) in words."""
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    try:
        raw = yaml.safe_load(text) or {}
    except yaml.YAMLError as e:
        raise ScenarioError(f"{p}: not a YAML file ({e}).") from None
    if not isinstance(raw, dict):
        raise ScenarioError(f"{p}: a scenario file is a mapping of fields.")
    return text, scenario_value(raw)


def _flow(value: Any) -> str:
    """One value in YAML's flow form, on one line."""
    text = yaml.safe_dump(
        value, default_flow_style=True, width=1 << 20, allow_unicode=True, sort_keys=False
    ).strip()
    if text.endswith("\n..."):
        text = text[: -len("\n...")].strip()
    elif text == "...":
        text = ""
    return text


def _plain(value: Any) -> bool:
    return not isinstance(value, dict | list)


def _flat(value: Any) -> bool:
    """A mapping or a list that may go on one line: plain values, or (in a mapping) lists
    of plain values."""
    if isinstance(value, dict):
        return all(
            _plain(v) or (isinstance(v, list) and all(_plain(x) for x in v)) for v in value.values()
        )
    if isinstance(value, list):
        return all(_plain(v) for v in value)
    return True


def _emit(key: str, value: Any, indent: int) -> list[str]:
    """The lines of `key: value` at an indent, in the hand's form: a plain value on the key's
    line; a short plain mapping or list in flow; a list of mappings an item a line, in flow
    where the item is plain and else as a block; any other mapping as a block."""
    pad = " " * indent
    if isinstance(value, bool) and key == "business":
        return [f"{pad}{key}: {'on' if value else 'off'}"]  # the hand's words, read the same
    if isinstance(value, str) and len(value) > _FLOW_LIST_MAX - indent:
        folded = _folded(key, value, indent)
        if folded:
            return folded
    if _plain(value) or not value:
        return [f"{pad}{key}: {_flow(value)}".rstrip()]
    if isinstance(value, dict):
        flow = _flow(value)
        if _flat(value) and len(flow) <= _FLOW_DICT_MAX:
            return [f"{pad}{key}: {flow}"]
        out = [f"{pad}{key}:"]
        for k, v in value.items():
            out += _emit(str(k), v, indent + 2)
        return out
    if all(_plain(v) for v in value):
        flow = _flow(value)
        sentences = any(isinstance(v, str) and " " in v for v in value)
        if len(flow) <= _FLOW_LIST_MAX and not sentences:
            return [f"{pad}{key}: {flow}"]
        return [f"{pad}{key}:"] + [f"{pad}  - {_flow(v)}" for v in value]
    out = [f"{pad}{key}:"]
    for item in value:
        out += _emit_item(item, indent + 2)
    return out


def _folded(key: str, value: str, indent: int, width: int = 92) -> list[str] | None:
    """A long sentence as a hand writes it, folded (`key: >-` and the words wrapped
    beneath), or None where folding would not read back as the same words (a line break,
    a double space, a space at either end)."""
    if "\n" in value or "  " in value or value != value.strip() or "\t" in value:
        return None
    pad = " " * (indent + 2)
    lines: list[str] = []
    line = ""
    for w in value.split(" "):
        if line and len(pad) + len(line) + 1 + len(w) > width:
            lines.append(pad + line)
            line = w
        else:
            line = f"{line} {w}" if line else w
    lines.append(pad + line)
    out = [f"{' ' * indent}{key}: >-"] + lines
    try:
        back = yaml.safe_load("\n".join(ln[indent:] for ln in out))
    except yaml.YAMLError:
        return None
    return out if back == {key: value} else None


def _flow_wrapped(prefix: str, value: dict[str, Any], width: int = 92) -> list[str]:
    """A plain mapping in flow after `prefix`, wrapped between its entries at `width` as a
    hand wraps the other sail's lines, the next lines under the brace's first entry."""
    entries = [_flow({k: v})[1:-1] for k, v in value.items()]
    lines: list[str] = []
    line = prefix + "{"
    for i, e in enumerate(entries):
        piece = e + ("}" if i == len(entries) - 1 else ",")
        if i and len(line) + 1 + len(piece) > width:
            lines.append(line)
            line = " " * (len(prefix) + 1) + piece
        else:
            line += ("" if i == 0 else " ") + piece
    lines.append(line)
    return lines


def _emit_item(item: Any, indent: int) -> list[str]:
    pad = " " * indent
    if isinstance(item, dict) and item and _flat(item):
        return _flow_wrapped(f"{pad}- ", item)
    if not isinstance(item, dict) or not item:
        return [f"{pad}- {_flow(item)}"]
    out: list[str] = []
    for i, (k, v) in enumerate(item.items()):
        lines = _emit(str(k), v, indent + 2)
        if i == 0:
            lines[0] = f"{pad}- {lines[0].lstrip()}"
        out += lines
    return out


def _comment_lines(words: str, width: int = 92) -> list[str]:
    out: list[str] = []
    line = "#"
    for w in words.split():
        if len(line) + 1 + len(w) > width:
            out.append(line)
            line = "#"
        line += " " + w
    out.append(line)
    return out


def _section(key: str, value: Any) -> list[str]:
    """A field's lines with its section's comment above it."""
    words = SECTION_COMMENTS.get(key)
    return (_comment_lines(words) if words else []) + _emit(key, value, 0)


def _header(raw: dict[str, Any], path: str | None) -> list[str]:
    name = str(raw.get("name") or "a scenario")
    where = Path(path).as_posix() if path else "<this file>"
    return [
        *_comment_lines(
            f"FreeSail: {name}. Made with the harbour's scenario maker (py -m freesail; "
            "package 59) in the form a hand writes (freesail/world/scenarios.py names every "
            "field), so that it may be edited here as well as in the harbour. Given to either "
            "driver with --scenario:"
        ),
        f"#     py -m freesail.ui.server --scenario {where}",
        f"#     py -m freesail.ui.console --scenario {where}",
        "",
    ]


def _ordered(raw: dict[str, Any]) -> list[str]:
    known = [k for k in FIELD_ORDER if k in raw]
    return known + [k for k in raw if k not in FIELD_ORDER]


@dataclass
class _Block:
    """A top-level field of a file's text, by line: its comments just above it, its key's
    line, and one past its body's last line."""

    key: str
    lead: int
    start: int
    end: int


def _blocks(lines: list[str]) -> list[_Block]:
    """The top-level fields of a file's lines. A field's leading comments are the comment
    lines at the margin just above its key, with no blank line between; its body runs to
    its last indented line before the next field's comments (a margin comment or a blank
    line after it belongs to the space between)."""
    starts = [(m.group(1), i) for i, ln in enumerate(lines) if (m := _KEY_LINE.match(ln))]
    blocks: list[_Block] = []
    for key, i in starts:
        floor = blocks[-1].start + 1 if blocks else 0
        lead = i
        while lead - 1 >= floor and lines[lead - 1].startswith("#"):
            lead -= 1
        blocks.append(_Block(key, lead, i, i + 1))
    for n, b in enumerate(blocks):
        stop = blocks[n + 1].lead if n + 1 < len(blocks) else len(lines)
        for j in range(b.start + 1, stop):
            if lines[j].strip() and not lines[j].startswith("#"):
                b.end = j + 1
    return blocks


def _inline_comment(line: str) -> str:
    """A field's comment beside it on its one line (`position: {...}   # Carrick Road`),
    found where cutting it leaves the same value; '' when there is none."""
    body = line.rstrip("\n")
    for m in reversed(list(re.finditer(r"\s+#", body))):
        try:
            if yaml.safe_load(body[: m.start()]) == yaml.safe_load(body):
                return body[m.start() :]
        except yaml.YAMLError:
            continue
    return ""


def scenario_text(
    raw: dict[str, Any], original: str | None = None, path: str | Path | None = None
) -> str:
    """The text of a scenario file holding the fields `raw` (spec M7b §21e). Without
    `original`, a new file in the hand's form: a header saying how to start it, each
    section under its comment. With the text the fields were read from, that text with the
    changed fields alone written again: a field unchanged keeps its lines and the comments
    above and beside it (so nothing changed is the same text, byte for byte); a field taken
    out goes with its comments; a field put in goes after the field it follows in the
    hand's order, under its section's comment. Proved before it is returned: the text read
    back says the same fields, else `ScenarioError`."""
    raw = {str(k): v for k, v in raw.items()}
    if original is None or not _blocks(original.splitlines(keepends=True)):
        lines = _header(raw, str(path) if path else None)
        for i, key in enumerate(_ordered(raw)):
            if i and key in SECTION_COMMENTS:
                lines.append("")
            lines += _section(key, raw[key]) if key in SECTION_COMMENTS else _emit(key, raw[key], 0)
        text = "\n".join(lines) + "\n"
    else:
        text = _rewrite(raw, original)
    try:
        back = yaml.safe_load(text) or {}
    except yaml.YAMLError as e:  # pragma: no cover - a fault of the writer's
        raise ScenarioError(f"the scenario's text is not YAML ({e}).") from None
    if not same_fields(back, raw):
        raise ScenarioError("the scenario's text does not read back as its fields.")
    return text


def _rewrite(raw: dict[str, Any], original: str) -> str:
    try:
        old = yaml.safe_load(original) or {}
    except yaml.YAMLError:
        old = {}
    old = old if isinstance(old, dict) else {}
    lines = original.splitlines(keepends=True)
    if lines and not lines[-1].endswith("\n"):
        lines[-1] += "\n"
    blocks = _blocks(lines)
    present = {b.key for b in blocks}
    order = _ordered(raw)
    # the fields put in, each after the nearest field before it in the hand's order
    added: dict[str, list[str]] = {}
    for key in order:
        if key in present:
            continue
        before = (
            [k for k in FIELD_ORDER[: FIELD_ORDER.index(key)] if k in present]
            if (key in FIELD_ORDER)
            else [b.key for b in blocks]
        )
        anchor = before[-1] if before else ""
        added.setdefault(anchor, [])
        added[anchor] += ["\n"] + [ln + "\n" for ln in _section(key, raw[key])]
    out = list(lines[: blocks[0].lead])
    if "" in added:
        out += added[""][1:] + ["\n"]
    for n, b in enumerate(blocks):
        stop = blocks[n + 1].lead if n + 1 < len(blocks) else len(lines)
        tail = lines[b.end : stop]
        if b.key not in raw:
            if tail and not tail[0].strip():
                tail = tail[1:]  # the field cut, with its comments and the blank line after
        elif b.key in old and same_fields(old[b.key], raw[b.key]):
            out += lines[b.lead : b.end]
        else:
            new = _emit(b.key, raw[b.key], 0)
            if b.end - b.start == 1 and len(new) == 1:
                new[0] += _inline_comment(lines[b.start])  # its comment beside it, kept
            out += lines[b.lead : b.start] + [ln + "\n" for ln in new]
        out += added.get(b.key, [])
        out += tail
    return "".join(out)


def newline_of(path: str | Path) -> str:
    """The line ending a file was written with ('\\r\\n' where Windows wrote it), so that
    one written again keeps it; '\\n' for a file that is not there."""
    try:
        return "\r\n" if b"\r\n" in Path(path).read_bytes() else "\n"
    except OSError:
        return "\n"


def write_scenario(
    raw: dict[str, Any], path: str | Path, original: str | None = None, newline: str = "\n"
) -> Path:
    """Write a scenario's file (`scenario_text`), making its folder, with the line ending
    given (the original's, `newline_of`), never the platform's by default."""
    p = Path(path)
    text = scenario_text(raw, original, path=p)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8", newline=newline) as f:
        f.write(text)
    return p
