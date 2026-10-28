"""The regimes of a nation's ships (spec M7 §22; package 72; docs/design/Design-Squadrons.md):
in port, in ordinary, on station, on passage, in convoy or escorting, on blockade, in chase,
each a few rules in data (`data/regimes.yaml`) and each nation's knobs in `data/nations.yaml`
(`naval:`). This module holds the two that are the far body's own minute: **a ship in
ordinary** (a hull at a port's anchorage with no company and no intent, `Vessel.regime ==
"in ordinary"`), commissioned with a delay by the director (`ship "X": commissioned for
<intent>`) or by the business, and **the sortie** (a nation that keeps port and slips out
when the blockade is blown off: her ship in ordinary with a `sortie` intent sails when no
enemy man of war has been within the regime's distance of the port's outer road for the
regime's minutes). The convoys, the blockades and the stations the business draws by the
same data (`business.py`); the set's books are `data/squadrons/`.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from freesail import units
from freesail.world.geo import bearing_and_distance

__all__ = ["REGIMES", "commission", "load_regimes", "minute", "regime_knob", "put_in_ordinary"]

REGIMES_PATH = Path(__file__).resolve().parents[2] / "data" / "regimes.yaml"
REGIMES: tuple[str, ...] = (
    "in port",
    "in ordinary",
    "on station",
    "on passage",
    "in convoy",
    "escorting",
    "on blockade",
    "in chase",
)

_LOADED: dict[str, Any] | None = None


def load_regimes(path: str | Path = REGIMES_PATH) -> dict[str, Any]:
    global _LOADED
    if _LOADED is None or str(path) != str(REGIMES_PATH):
        raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
        data = {str(k): (v or {}) for k, v in (raw.get("regimes") or {}).items()}
        if str(path) == str(REGIMES_PATH):
            _LOADED = data
        return data
    return _LOADED


def regime_knob(regime: str, key: str, default: Any = None) -> Any:
    raw = (load_regimes().get(regime) or {}).get(key)
    if isinstance(raw, dict) and "value" in raw:
        return raw["value"]
    return default if raw is None else raw


def naval_of(world: Any, nation_id: str) -> dict[str, Any]:
    """A nation's `naval:` knobs, {} for a nation with none."""
    nations = getattr(world, "nations", None)
    try:
        nation = nations.get(nation_id) if nations is not None else None
    except KeyError:
        nation = None
    return dict(getattr(nation, "naval", None) or {})


# ---------------------------------------------------------------------------
# In ordinary, and the commission
# ---------------------------------------------------------------------------


def put_in_ordinary(world: Any, vessel: Any, port: Any, sortie: str = "") -> None:
    """A hull laid up at the port's anchorage: no brain, the anchor plan, the regime."""
    vessel.brain = None
    vessel.intent_words = ""
    vessel.plan = [("anchor", port.id)]
    vessel.saved_plan = None
    vessel.cycle = False
    vessel.state = "in port"
    vessel.regime = "in ordinary"
    vessel.sortie = " ".join(str(sortie or "").split())
    vessel.commission_tick = -1
    vessel.goal = f"in ordinary at {port.name}"


def commission(world: Any, vessel: Any, intent: str, port: Any = None, delay_s: int = 0) -> str:
    """A ship in ordinary commissioned for an intent: at once, or after the delay (then
    her captain takes her out when it is up). Returns the words for the record; raises
    ValueError in words when the intent is none a captain knows."""
    from freesail.world.captains import read_intent

    words = " ".join(str(intent).split())
    read_intent(world, words)  # refused in words now, not at the tick
    tick = int(world.clock.tick)
    if delay_s > 0:
        vessel.regime = "in ordinary"
        vessel.sortie = words
        vessel.commission_tick = tick + int(delay_s)
        _story(
            vessel,
            tick,
            f"commissioned for {words}: her company raising, to sail in {_hours(delay_s)}",
        )
        return f"commissioned for {words}; she sails in {_hours(delay_s)}"
    _sail(world, vessel, words, port)
    return f"commissioned for {words}; under way"


def _sail(world: Any, vessel: Any, words: str, port: Any) -> None:
    from freesail.world.brains import FarCaptain

    tick = int(world.clock.tick)
    if port is None:
        port = _port_of(world, vessel)
    vessel.regime = ""
    vessel.sortie = ""
    vessel.commission_tick = -1
    vessel.intent_words = words
    vessel.brain = FarCaptain(world, vessel, words)
    if port is not None:
        vessel.brain._departing = port.id
    vessel.brain._plan()
    vessel.saved_plan = None
    vessel.cycle = False
    vessel.state = "on passage"
    vessel.done = False
    _story(vessel, tick, f"commissioned and under way: {words}")


def _port_of(world: Any, vessel: Any) -> Any:
    ports = getattr(world, "dealings", None)
    best = None
    for port in (getattr(ports, "ports", None) or {}).values():
        _, d = bearing_and_distance(vessel.position, port.anchorage.position)
        if best is None or d < best[1]:
            best = (port, d)
    return best[0] if best is not None and best[1] <= 3.0 * units.NAUTICAL_MILE else None


def _hours(seconds: int) -> str:
    h = int(round(seconds / 3600.0))
    return f"{h} hours" if h != 1 else "an hour"


def _story(vessel: Any, tick: int, words: str) -> None:
    story = list(getattr(vessel, "story", ()) or ())
    story.append((tick, words))
    vessel.story = tuple(story[-30:])


# ---------------------------------------------------------------------------
# The minute: the commissions due and the sorties
# ---------------------------------------------------------------------------

_MAN_OF_WAR_ROLES = frozenset({"kings-ship", "cruiser", "commodore"})
_MAN_OF_WAR_DESCRIPTIONS = frozenset({"frigate", "brig-sloop"})


def _blockade_station_of(world: Any, port: Any) -> tuple[Any, float] | None:
    """The port's blockade station as (position, radius m), from its file's
    `blockade_station` (the feature and its miles), None for a port with none."""
    station = dict(getattr(port, "blockade_station", None) or {})
    chart = getattr(world, "chart", None)
    feature = chart.feature(str(station.get("feature") or "")) if chart is not None else None
    if feature is None:
        return None
    from freesail.world.geo import Position

    pos = Position(float(feature.lat_deg), float(feature.lon_deg))
    return pos, float(station.get("within_nm") or 6.0) * units.NAUTICAL_MILE


def _in_the_offing(world: Any, port: Any, pos: Any, within_nm: float) -> bool:
    """Within the regime's miles of the port's outer road, or on the port's blockade
    station (within its miles of its feature): either is the offing the port's look-outs
    see a blockader in."""
    if bearing_and_distance(port.outer_road.position, pos)[1] <= within_nm * units.NAUTICAL_MILE:
        return True
    station = _blockade_station_of(world, port)
    return station is not None and bearing_and_distance(station[0], pos)[1] <= station[1]


def _enemy_men_of_war_near(world: Any, port: Any, nation: str, within_nm: float) -> bool:
    nations = getattr(world, "nations", None)
    if nations is None:
        return False
    for o in world.vessels.vessels:
        if getattr(o, "done", False) or not nations.at_war(str(o.nation), nation):
            continue
        brain = getattr(o, "brain", None)
        role = getattr(brain, "role", "") if brain is not None else ""
        if (
            role not in _MAN_OF_WAR_ROLES
            and str(getattr(o, "description", "")) not in _MAN_OF_WAR_DESCRIPTIONS
        ):
            continue
        if _in_the_offing(world, port, o.position, within_nm):
            return True
    # the player's own ship, a King's ship of a nation at war with hers
    pos = getattr(world, "position", None)
    ports = getattr(world, "dealings", None)
    own = str(getattr(ports, "ship_nation", "") or "") if ports is not None else ""
    if pos is not None and own and nations.at_war(own, nation):
        from freesail.world.captains import _is_kings_ship

        if _is_kings_ship(world) and _in_the_offing(world, port, pos, within_nm):
            return True
    return False


def _wind_kn_at(world: Any, pos: Any) -> float:
    """The wind's speed in knots at a place: the systems' surface wind where the world has
    the field, else the one wind of the pinned scenario."""
    systems = getattr(world, "systems", None)
    if systems is not None and getattr(world, "weather", None) is None:
        plane = world.plane_of(pos) if hasattr(world, "plane_of") else None
        if plane is not None:
            try:
                _, ms = systems.surface_wind_at(plane[0] / 1000.0, plane[1] / 1000.0)
                return float(ms) / units.KNOT
            except Exception:  # noqa: BLE001
                pass
    wind = getattr(world, "wind", None)
    return float(getattr(wind, "speed", 0.0) or 0.0) / units.KNOT if wind is not None else 0.0


def minute(world: Any) -> list[tuple[Any, ...]]:
    """Once a minute: a commission whose delay is up sails her; a ship in ordinary with a
    sortie, of a nation that slips out when the blockade is blown off, sails when the
    offing has been clear of the enemy's men of war for the regime's minutes."""
    sea = getattr(world, "vessels", None)
    if sea is None:
        return []
    tick = int(world.clock.tick)
    lines: list[tuple[Any, ...]] = []
    for v in list(sea.vessels):
        if getattr(v, "done", False) or getattr(v, "regime", "") != "in ordinary":
            continue
        due = int(getattr(v, "commission_tick", -1) or -1)
        if due >= 0:
            if tick >= due and v.sortie:
                try:
                    _sail(world, v, v.sortie, None)
                except ValueError as e:
                    _story(v, tick, f"cannot sail for '{v.sortie}': {e}")
                    v.sortie, v.commission_tick = "", -1
            continue
        sortie = str(getattr(v, "sortie", "") or "")
        if not sortie:
            continue
        knobs = naval_of(world, str(v.nation))
        if not knobs.get("slips_out_when_blown_off"):
            continue
        port = _port_of(world, v)
        if port is None:
            continue
        within = float(regime_knob("in ordinary", "slip_out_clear_nm", 10.0))
        clear_s = float(regime_knob("in ordinary", "slip_out_clear_minutes", 60)) * 60.0
        wind_max = float(regime_knob("in ordinary", "slip_out_wind_max_kn", 27.0))
        memo = v.__dict__.setdefault("_sortie_memo", {})
        if _enemy_men_of_war_near(world, port, str(v.nation), within):
            memo["clear_since"] = None
            continue
        if _wind_kn_at(world, port.outer_road.position) > wind_max:
            # the gale that blew the blockade off keeps her in too: she waits for it to
            # moderate, and the hour of the offing clear is counted from then
            memo["clear_since"] = None
            continue
        since = memo.get("clear_since")
        if since is None:
            memo["clear_since"] = tick
            continue
        if tick - int(since) >= clear_s:
            try:
                _sail(world, v, sortie, port)
            except ValueError as e:
                # a sortie no captain can read (the knobs' words against this chart): said
                # in her story once, and she stays in ordinary
                _story(v, tick, f"cannot sail for '{sortie}': {e}")
                v.sortie = ""
                continue
            _story(
                v,
                tick,
                f"the offing clear of the enemy for {_hours(int(clear_s))}: slipped out of "
                f"{port.name}",
            )
            lines.append(
                (
                    _severity(),
                    "regime.sortie",
                    f"{v.name} slips out of {port.name}, the blockade off its station: {sortie}.",
                    {"id": v.id, "port": port.id, "intent": sortie},
                )
            )
    return lines


def _severity() -> Any:
    from freesail.core.events import Severity

    return Severity.ROUTINE
