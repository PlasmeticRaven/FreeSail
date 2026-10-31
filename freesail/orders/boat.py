"""The boat's orders (package 82, item 4; the design's §5.3): the oars and the mast of a
ship's boat manned as a hull of the world (`freesail/world/boats.py`), and the ship's
orders about her boat.

In the boat (her hull current at the prompt, or a station's through its door): `give way`
(the full stroke; `give way together`), `easy all` (half), `lie on your oars` (the oars out,
no stroke), `boat your oars` (the oars in), `out oars`, `pull for <the ship | the shore |
the quay | a sail by her name | a point of the compass | a position>` (the coxswain steers
for it and keeps steering as it bears, the helm set each minute by the truth's bearing),
`step the mast` and `unstep the mast` (the mast up or down; the lug cannot be set with the
mast down and the oars cannot be pulled with the lug drawing, which is the period's practice
and the words of the refusals), `come alongside` (she pulls for her ship and, within a boat's
length, is hoisted in). The lug itself is the engine's: `set the lug`, `take in the lug`.
On the ship: `cut the boat adrift`. Each is refused in words on a hull that is no boat, or
about a boat she has not got. The thrust the oars give is `physics/oars.py`'s.
"""

from __future__ import annotations

import re
from typing import Any

from freesail import units
from freesail.orders.errors import OrderError
from freesail.orders.grammar import Order
from freesail.orders.prompt import world_of
from freesail.physics.oars import EASY, FULL, LYING_ON, oars_of, stroke_words

__all__ = ["BOAT_VERBS", "SHIP_VERBS", "execute"]

Result = tuple[str, str, dict[str, Any]]

# The verbs given in the boat, and the ship's about her boat (the vocabulary's keys).
BOAT_VERBS = frozenset(
    {
        "give way",
        "easy all",
        "lie on your oars",
        "boat your oars",
        "out oars",
        "pull for",
        "step the mast",
        "unstep the mast",
        "come alongside",
    }
)
SHIP_VERBS = frozenset({"cut the boat adrift"})

_POSITION = re.compile(r"\d+\s*\d*\s*[NS]\b.*\d+\s*\d*\s*[EW]\b", re.I)


def execute(ship: Any, order: Order) -> Result:
    """Carry out a boat order. The verb is the vocabulary's key."""
    verb = order.verb
    rest = " ".join((order.object or "").split())
    world = world_of(ship)
    if world is None:
        raise OrderError("There is no world about her; the boat's orders want one.")
    if verb in SHIP_VERBS:
        return _ship_order(world, verb, rest)
    oars = oars_of(ship)
    if oars is None:
        raise OrderError(
            f"'{order.verb_phrase}' is the boat's order: this hull has no oars. In the boat "
            "('go to the boat'), the lug, the oars and the helm are hers."
        )
    if verb == "give way":
        return _stroke(ship, oars, FULL, "Give way together: the full stroke.")
    if verb == "easy all":
        return _stroke(ship, oars, EASY, "Easy all: a light stroke.")
    if verb == "lie on your oars":
        if not oars.out:
            raise OrderError("The oars are in; 'out oars' first.")
        oars.stroke = LYING_ON
        return "boat.oars", "Lie on your oars: the oars out and the stroke stopped.", _data(oars)
    if verb == "out oars":
        if _lug_drawing(ship):
            raise OrderError("The lug is drawing; take it in before the oars are shipped.")
        oars.out = True
        oars.manned = oars.number
        oars.stroke = LYING_ON
        said = f"Out oars: {oars.number} oars shipped, the men lying on them."
        return "boat.oars", said, _data(oars)
    if verb == "boat your oars":
        if not oars.out:
            raise OrderError("The oars are in already.")
        oars.out = False
        oars.manned = 0
        oars.stroke = LYING_ON
        oars.pulling_for = {}
        return "boat.oars", "Boat your oars: the oars tossed and laid in.", _data(oars)
    if verb == "pull for":
        return _pull_for(world, ship, oars, rest)
    if verb == "step the mast":
        return _mast(ship, up=True)
    if verb == "unstep the mast":
        return _mast(ship, up=False)
    if verb == "come alongside":
        from freesail.world import boats

        text = boats.come_alongside(world, world.own)
        return "boat.alongside", text, _data(oars)
    raise OrderError(f"'{verb}' is no order of the boat's.")


def check_sail_order(ship: Any, order: Order) -> None:
    """A sail order in the boat (package 82, item 4): the lug cannot be set with the mast
    unstepped, in the period's words rather than the engine's for a mast sent down."""
    if order.verb != "set" or oars_of(ship) is None:
        return
    masts = [s for s in ship.spars.values() if s.cls == "mast"]
    if masts and all(m.sent_down for m in masts):
        raise OrderError("The mast is unstepped and laid along the thwarts; 'step the mast' first.")


def _stroke(ship: Any, oars: Any, stroke: float, said: str) -> Result:
    if _lug_drawing(ship):
        raise OrderError("The lug is drawing; take it in before the men pull.")
    if not oars.out:
        oars.out = True
        oars.manned = oars.number
        said = f"Out oars; {said[:1].lower()}{said[1:]}"
    oars.stroke = stroke
    tired = f" The men have {oars.hours:.1f} hours at the oars." if oars.hours >= 0.5 else ""
    return "boat.oars", f"{said}{tired}", _data(oars)


def _pull_for(world: Any, ship: Any, oars: Any, rest: str) -> Result:
    """`pull for <mark>`: the coxswain's mark, and the oars out and giving way."""
    from freesail.world import boats

    if not rest:
        raise OrderError(
            "Pull for what? Say 'pull for the ship', 'pull for the quay', 'pull for the "
            "Amazon', a point ('pull for NE') or a position."
        )
    # under the lug the coxswain steers for the mark and the men keep their oars in (the
    # period's practice; `make for the ship`); under oars they give way for it
    sailing = _lug_drawing(ship)
    low = rest.lower().removeprefix("the ").strip(" .")
    hull = world.own
    mark: dict[str, Any] = {}
    name = low
    if low in ("ship", "our ship", "her", "home", "the ship"):
        own = boats.ship_of(world, hull)
        if own is None:
            raise OrderError("She is no ship's boat: there is no ship to pull for.")
        mark = {"hull": str(own.id)}
        name = f"the {boats.hull_name_of(own)}"
    elif low in ("shore", "quay", "land", "the shore", "the quay", "beach"):
        dealings = getattr(hull, "dealings", None)
        found = dealings.nearest(12.0) if dealings is not None else None
        if found is None:
            raise OrderError("No shore within a boat's pull by account; say a sail or a point.")
        port, _nm = found
        mark = {"quay": str(port.id)}
        name = f"the quay at {port.name}"
    elif _POSITION.search(rest):
        from freesail.world.geo import parse_position

        try:
            pos = parse_position(rest)
        except ValueError as e:
            raise OrderError(str(e)) from None
        mark = {"lat_deg": pos.lat_deg, "lon_deg": pos.lon_deg, "name": rest}
    else:
        point = units.parse_compass_point(low)
        if point is not None:
            # a point of the compass: the coxswain steers it, no mark to come up with
            from freesail.ship.parts import HelmMode

            dyn = ship.dyn
            dyn.target_heading = units.wrap_2pi(point)
            if hasattr(dyn, "helm_mode"):
                dyn.helm_mode = HelmMode.HEADING
            oars.pulling_for = {}
            if sailing:
                return (
                    "boat.helm",
                    f"Steering {units.format_heading(point)} under the lug.",
                    _data(oars),
                )
            oars.out, oars.manned, oars.stroke = True, oars.number, FULL
            return (
                "boat.oars",
                f"Pulling {units.format_heading(point)}: the oars out, giving way.",
                _data(oars),
            )
        other = None
        for h in (getattr(world, "hulls", None) or {}).values():
            if h is hull:
                continue
            if boats.hull_name_of(h).lower().removeprefix("the ") == low:
                other = h
                break
        if other is not None:
            mark = {"hull": str(other.id)}
            name = f"the {boats.hull_name_of(other)}"
        else:
            v = world.vessels.find(rest)
            if v is None or v.done:
                raise OrderError(
                    f"No sail or shore answers to {rest!r}; say 'the ship', 'the quay', a sail "
                    "by her name, a point or a position."
                )
            mark = {"vessel": str(v.id), "name": v.name}
            name = v.name
    oars.pulling_for = mark
    if sailing:
        boats.tick_boat(world)  # the first turn of the helm at once
        return "boat.helm", f"Making for {name} under the lug.", _data(oars)
    oars.out, oars.manned, oars.stroke = True, oars.number, FULL
    boats.tick_boat(world)  # the first turn of the helm at once
    return "boat.oars", f"Pull for {name}: the oars out, giving way together.", _data(oars)


def _mast(ship: Any, up: bool) -> Result:
    masts = [s for s in ship.spars.values() if s.cls == "mast"]
    if not masts:
        raise OrderError("She has no mast to step.")
    mast = masts[0]
    if up:
        if not mast.sent_down:
            raise OrderError("The mast is stepped already.")
        mast.sent_down = False
        return (
            "boat.mast",
            "The mast stepped and the lug bent to its yard, ready to hoist ('set the lug').",
            {"mast": mast.id, "stepped": True},
        )
    if mast.sent_down:
        raise OrderError("The mast is down already.")
    if _lug_drawing(ship):
        raise OrderError("The lug is set; take it in before the mast comes down.")
    mast.sent_down = True
    said = "The mast unstepped and laid along the thwarts."
    return "boat.mast", said, {"mast": mast.id, "stepped": False}


def _lug_drawing(ship: Any) -> bool:
    from freesail.ship.parts import SailState

    return any(
        getattr(s, "cls", "") == "lug" and s.state == SailState.SET for s in ship.sails.values()
    )


def _ship_order(world: Any, verb: str, rest: str) -> Result:
    from freesail.world import boats

    if verb == "cut the boat adrift":
        hull = world.own
        if boats.is_boat(hull):
            raise OrderError("You are in the boat; she is cut adrift from the ship, not from her.")
        text = boats.cut_adrift(world, hull)
        return "boat.lost", text, {"how": "cut adrift"}
    raise OrderError(f"'{verb}' is no order about the boat.")


def _data(oars: Any) -> dict[str, Any]:
    return {
        "oars": int(oars.manned),
        "out": bool(oars.out),
        "stroke": stroke_words(oars.stroke),
        "hours": round(float(oars.hours), 2),
    }
