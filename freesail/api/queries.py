"""Read-only state queries for views and agents: the snapshot and the ship graph.

`snapshot(world)` is the state a view redraws from (spec §9.4): the clock,
the hull's motion, the wind, every sail, spar and line, and the evolutions
in progress. `ship_graph(ship)` is what a view *builds* from once: every
spar with its class, position and dimensions, every sail with its roles
and area, the hull's dimensions, groups and aliases. Both are plain
dictionaries of SI numbers; the client converts for display.

Neither function changes anything. Both work on a World whose ship is the
milestone 0 point ship (no parts): the part lists are then empty.
"""

from __future__ import annotations

from typing import Any

from freesail import units
from freesail.core.world import World
from freesail.physics.sails import SAIL_CLASSES
from freesail.ship.graph import Ship
from freesail.ship.parts import Line, Sail, Spar


def _spar_state(s: Spar) -> str:
    if s.wrecked:
        return "wrecked"
    if s.sent_down:
        return "sent_down"
    return "sound"


def _sail_state(s: Sail) -> str:
    return "wrecked" if s.wrecked else s.state.value


def _bell(world: World) -> dict[str, Any]:
    """The last bell struck: watch name, bells, and whether it is striking now."""
    t = world.clock.ship_time
    start_hour, watch = units.watch_of(t)
    half_hours = (t.hour - start_hour) * 2 + t.minute // 30
    if half_hours == 0:
        bells = 4 if watch == "Last dog watch" else 8
    else:
        bells = half_hours
    return {"watch": watch, "bells": bells, "striking": units.bells_at(t) is not None}


def snapshot(world: World) -> dict[str, Any]:
    """The state a view redraws from. SI units; see spec §9.4."""
    ship = world.ship
    wind = world.wind
    out: dict[str, Any] = {
        "tick": world.clock.tick,
        "ship_time": world.clock.ship_time.isoformat(),
        "stamp": world.clock.stamp(),
        "bell": _bell(world),
        "wind": {
            "true_from": wind.direction_from,
            "true_speed": wind.effective_speed,
            "mean_speed": wind.speed,
            "gust_factor": wind.gust_factor,
        },
    }
    if not isinstance(ship, Ship):
        st = ship.state()
        out["ship"] = {
            "name": st.get("name", "point"),
            "x": st.get("x", 0.0),
            "y": st.get("y", 0.0),
            "heading": st.get("heading", 0.0),
            "speed_through_water": st.get("speed", 0.0),
            "leeway": 0.0,
            "heel": 0.0,
            "rudder": 0.0,
            "weather_helm": 0.0,
            "tack": "starboard",
            "helm_mode": "heading",
            "target_heading": st.get("heading", 0.0),
        }
        out["wind"]["apparent_angle"] = 0.0
        out["wind"]["apparent_speed"] = wind.effective_speed
        out["sails"] = []
        out["spars"] = []
        out["lines"] = []
        out["evolutions_in_progress"] = []
        return out

    d = ship.dyn
    out["ship"] = {
        "name": ship.name,
        "x": d.x,
        "y": d.y,
        "heading": d.heading,
        "speed_through_water": d.speed,
        "leeway": d.leeway,
        "heel": d.heel,
        "rudder": d.rudder,
        "weather_helm": d.weather_helm,
        "tack": d.tack,
        "helm_mode": d.helm_mode.value,
        "target_heading": d.target_heading,
    }
    out["wind"]["apparent_angle"] = d.apparent_wind_angle
    out["wind"]["apparent_speed"] = d.apparent_wind_speed
    out["sails"] = [
        {
            "id": s.id,
            "class": s.cls,
            "state": _sail_state(s),
            "reefs": s.reefs,
            "area_effective": s.area_effective_m2,
            "thrust": s.thrust_kn,
            "side": s.side_force_kn,
            "strain_ratio": s.strain_ratio,
            "backed": s.backed,
            "sheet_angle": s.sheet_angle,
        }
        for s in ship.sails.values()
    ]
    out["spars"] = [
        {
            "id": s.id,
            "class": s.cls,
            "state": _spar_state(s),
            "condition": s.condition,
            "strain_ratio": s.strain_ratio,
            "brace_angle": s.brace_angle,
        }
        for s in ship.spars.values()
    ]
    out["lines"] = [
        {
            "id": ln.id,
            "class": ln.cls,
            "state": ln.state.value,
            "strain_ratio": ln.strain_ratio,
            "hauled": ln.hauled,
        }
        for ln in ship.lines.values()
    ]
    runner = ship.extra.get("evolutions")
    out["evolutions_in_progress"] = list(runner.in_progress()) if runner is not None else []
    return out


def _spar_entry(s: Spar) -> dict[str, Any]:
    return {
        "id": s.id,
        "class": s.cls,
        "x_m": s.x_m,
        "height_m": s.height_m,
        "length_m": s.length_m,
        "parent": s.parent,
        "side": s.side,
        "brace_angle": s.brace_angle,
        "brace_limit": s.brace_limit,
        "rake": s.rake,
        "rating_kn": s.rating_kn,
    }


def _sail_entry(s: Sail) -> dict[str, Any]:
    cls = SAIL_CLASSES.get(s.cls)
    return {
        "id": s.id,
        "class": s.cls,
        "roles": dict(s.roles),
        "area_m2": s.area_m2,
        "x_m": s.x_m,
        "centre_height_m": s.centre_height_m,
        "reef_bands": s.reef_bands,
        "reef_factor": cls.reef_factor if cls is not None else 0.0,
        "side": s.side,
        "state": _sail_state(s),
        "reefs": s.reefs,
        "sheet_angle": s.sheet_angle,
    }


def _line_entry(ln: Line) -> dict[str, Any]:
    return {"id": ln.id, "class": ln.cls, "of": ln.of, "side": ln.side, "state": ln.state.value}


def ship_graph(ship: Ship) -> dict[str, Any]:
    """Everything a drawing needs to build the ship once: parts, dimensions, roles.

    Spars carry their class, `x_m` (root spars only; a child spar stands at its
    parent's x), `height_m`, `length_m`, parent, side and brace angle. Sails
    carry class, roles, area, state, reefs, sheet angle and centre height.
    The hull carries its principal dimensions. SI throughout.
    """
    h = ship.hull.spec
    return {
        "name": ship.name,
        "rig": ship.spec.rig,
        "hull": {
            "length_waterline_m": h.length_waterline_m,
            "beam_m": h.beam_m,
            "draught_m": h.draught_m,
            "deck_height_m": h.deck_height_m,
            "displacement_kg": h.displacement_kg,
            "gm_m": h.gm_m,
            "clr_x_m": h.clr_x_m,
        },
        "spars": [_spar_entry(s) for s in ship.spars.values()],
        "sails": [_sail_entry(s) for s in ship.sails.values()],
        "lines": [_line_entry(ln) for ln in ship.lines.values()],
        "groups": {g: list(m) for g, m in ship.groups.items()},
        "aliases": dict(ship.aliases),
    }
