"""The fishing orders (spec M7b §21a; package 56): what the master of a fishing vessel says
of the gear, the catch and the quay.

    shoot the trawl / haul the trawl   the beam trawl over and towed with the tide under
                                       easy sail; hove up by the winch, the take struck
                                       below (data/evolutions/shoot_trawl.yaml, haul_trawl)
    shoot the nets / haul the nets     the drift nets shot at sunset and ridden to through
                                       the night; hauled at the capstan
    shoot the seine / haul the seine   the boat rows the sean round a shoal in a bay, by
                                       day; the fish tucked into the boat and struck below
    set the lines / haul the lines     the longlines paid out across the tide under easy
                                       sail; hauled by short tacks, the cod into the well
    shoot the gear / haul the gear     the gear the ground she is on wants in this month,
                                       of the gear she carries (the rules-based captain's)
    sell the catch                     the catch landed and sold at the fish quay of the
                                       port she lies in, the spoiled thrown over the side
    the catch                          what fish is aboard, where and for how long
    the fishing grounds                the grounds about her, their fish and their seasons

Each shot is refused in words when she carries no such gear (the smack and the lugger
carry their files' and no other), is on no ground the master knows, finds nothing of it in
season or at this hour, or has more wind than the gear is worked in; a haul when the gear
is not in the water. While the gear is out a sail beyond its allowance is refused in words
(`world.fishing.sail_allowed`, through `orders.verbs`). The work itself is the gear's
evolution through the runner, holding the gear and not the ship.
"""

from __future__ import annotations

from typing import Any

from freesail import units
from freesail.orders.errors import OrderError
from freesail.orders.grammar import Order
from freesail.orders.prompt import world_of

__all__ = ["execute"]

Result = tuple[str, str, dict[str, Any]]

# The verb's gear kind and action.
_GEAR_VERBS: dict[str, tuple[str, str]] = {
    "shoot the trawl": ("trawl", "shoot"),
    "haul the trawl": ("trawl", "haul"),
    "shoot the nets": ("drift nets", "shoot"),
    "haul the nets": ("drift nets", "haul"),
    "shoot the seine": ("seine", "shoot"),
    "haul the seine": ("seine", "haul"),
    "set the lines": ("lines", "shoot"),
    "haul the lines": ("lines", "haul"),
    "shoot the gear": ("", "shoot"),
    "haul the gear": ("", "haul"),
}


def _fishery(world: Any) -> Any:
    fishery = getattr(world, "fishery", None) if world is not None else None
    if fishery is None:
        raise OrderError(
            "She carries no fishing gear: her file lists none. The smack and the lugger "
            "carry the trawl, the nets, the seine or the lines."
        )
    return fishery


def execute(ship: Any, order: Order) -> Result:
    from freesail.world import fishing

    world = world_of(ship)
    verb = order.verb
    data: dict[str, Any] = {"verb": verb, "level": 1}
    if verb == "the catch":
        fishery = getattr(world, "fishery", None) if world is not None else None
        if fishery is None:
            return "query.fishing", "She carries no fishing gear and no fish.", data
        return (
            "query.fishing",
            f"The catch: {fishery.words(world.clock.tick)}.",
            data | {"tons": round(fishery.catch.tons(), 3)},
        )
    if verb == "the fishing grounds":
        return "query.fishing", _grounds_words(world), data
    if verb == "sell the catch":
        return _sell(world, data)
    kind, action = _GEAR_VERBS[verb]
    fishery = _fishery(world)
    if action == "haul":
        out = fishery.out
        if out is None:
            raise OrderError("No gear is in the water to haul.")
        if kind and out.kind != kind:
            raise OrderError(f"The {kind} is not in the water; {out.name} is.")
        if out.state == "hauling":
            raise OrderError(f"The hands are hauling {out.name} already.")
        return _start(ship, world, fishery, out.kind, "haul", out.ground_id, data)
    if fishery.out is not None:
        raise OrderError(f"{_cap(fishery.out.name)} is in the water; haul it first.")
    ground = fishing.ground_at(world, world.position)
    if ground is None:
        near = fishing.nearest_grounds(world, world.position, 2)
        said = (
            "; ".join(f"{g.name}, {_miles(nm)} off" for nm, g in near if nm < 60)
            or "none within the chart"
        )
        raise OrderError(f"She is on no fishing ground the master knows. The nearest: {said}.")
    when = world.clock.ship_time
    if not kind:
        kind = fishing.gear_for(fishery, ground, when) or ""
        if not kind:
            raise OrderError(
                f"Nothing on {ground.name} is in season this month for the gear she carries "
                f"({', '.join(fishery.kinds())})."
            )
    gear = fishery.carries(kind)
    if gear is None:
        raise OrderError(
            f"She carries no {kind}: her gear is {', '.join(g.name for g in fishery.gear)}."
        )
    if kind not in ground.gear_kinds():
        raise OrderError(
            f"{_cap(ground.name)} is no ground for {gear.name}; it is worked with "
            f"{', '.join(ground.gear_kinds()) or 'nothing'}."
        )
    if not ground.in_season(kind, when.month):
        raise OrderError(
            f"Nothing is taken on {ground.name} by {gear.name} in "
            f"{fishing.MONTH_NAMES[when.month - 1]}: {ground.season_words(kind)}."
        )
    if not fishing.fishing_now(ground, kind, when, str(world.daylight)):
        raise OrderError(
            f"Not at this hour: on {ground.name} {gear.name} takes {ground.season_words(kind)}."
        )
    wind_kn = units.ms_to_knots(float(world.wind.base_speed))
    most = float(fishing.gear_spec(kind).get("most_wind_kn", 25))
    if wind_kn > most:
        raise OrderError(
            f"Too much wind to work {gear.name}: {wind_kn:.0f} knots, and it is worked in "
            f"{most:.0f} at the most."
        )
    if kind == "seine":
        ports = getattr(world, "ports", None)
        if ports is not None and getattr(ports, "boat", None) is not None and ports.boat.away:
            raise OrderError("The boat is away; the seine is shot from her.")
    return _start(ship, world, fishery, kind, "shoot", ground.id, data | {"ground": ground.id})


def _start(
    ship: Any, world: Any, fishery: Any, kind: str, action: str, ground: str, data: dict
) -> Result:
    from freesail.orders.verbs import runner_of
    from freesail.world import fishing

    evo = fishing.evolution_of(kind, action)
    text = runner_of(ship).start(
        ship, evo, "her", {"gear": kind, "action": action, "ground": ground}
    )
    return "fishing.order", text, data | {"evolution": evo, "gear": kind}


def _sell(world: Any, data: dict[str, Any]) -> Result:
    from freesail.world import fishing

    fishery = _fishery(world)
    ports = getattr(world, "ports", None)
    port = ports.in_port() if ports is not None and getattr(ports, "ports", None) else None
    if port is None:
        raise OrderError("She is not in port; the fish are sold on a quay.")
    if ports.stance(port) in ("hostile", "closed"):
        raise OrderError(f"{port.name} is {ports.stance(port)} to her; nothing is sold there.")
    if ports.boat.away:
        raise OrderError("The boat is away; the catch is landed by her.")
    try:
        text, record = fishing.sell_catch(world, fishery, port)
    except ValueError as e:
        raise OrderError(str(e)) from None
    return "fishing.sold", text, data | record


def _grounds_words(world: Any) -> str:
    from freesail.world import fishing

    if world is None or world.position is None:
        return "The master knows no grounds from here."
    near = fishing.nearest_grounds(world, world.position, 4)
    if not near:
        return "The master knows no fishing grounds on this chart."
    parts = []
    for nm, g in near:
        kinds = g.gear_kinds()
        seasons = "; ".join(f"{k}: {g.season_words(k)}" for k in kinds)
        parts.append(f"{_cap(g.name)}, {_miles(nm)} off ({seasons})")
    return "The grounds about her: " + ". ".join(parts) + "."


def _miles(nm: float) -> str:
    if nm < 1.0:
        return "within a mile"
    return f"{nm:.0f} miles"


def _cap(text: str) -> str:
    return text[:1].upper() + text[1:]
