"""The orders of the marines, the small arms and the fight on deck (spec M7 §11, §11a;
package 73; the design in `docs/design/Design-WaterAndHealth.md`): object `fight` in the
vocabulary.

    marines, fire by volley      the detachment's standing intention within musket shot
    marines, fire at will        (`freesail/combat/small_arms.py`)
    marines, hold your fire
    marines to the tops          the book's share of the detachment sent aloft as marksmen
    marines to the gangways      and brought down again
    serve out the small arms     the cutlasses, pikes, pistols and tomahawks to the boarders
                                 (an evolution of five minutes with the gunner's party)
    small arms, fire at will     the small-arms men's muskets within musket shot
    small arms, hold your fire
    lay her aboard               the helm closing her to pistol shot and under (the chase's
                                 course, with the boarding's word)
    grapple her                  the grapnels thrown within thirty metres (an evolution)
    cast off the grapnels        the ships freed
    boarders away                the boarders over the side: the fight on deck
    repel boarders               the gun crews up, the guns silent, the deck held

Replies are `(kind, log_text, data)` like every verb's.
"""

from __future__ import annotations

from dataclasses import replace
from typing import Any

from freesail.crew.model import Station, number_words
from freesail.evolutions import registry
from freesail.orders.errors import OrderError
from freesail.orders.grammar import Order
from freesail.orders.prompt import world_of

__all__ = ["FIGHT_VERBS", "execute"]

Result = tuple[str, str, dict[str, Any]]

FIGHT_VERBS: tuple[str, ...] = (
    "marines fire by volley",
    "marines fire at will",
    "marines hold your fire",
    "marines to the tops",
    "marines to the gangways",
    "serve out the small arms",
    "small arms fire at will",
    "small arms hold your fire",
    "lay her aboard",
    "grapple her",
    "cast off the grapnels",
    "boarders away",
    "repel boarders",
)


def _world(ship: Any, verb: str) -> Any:
    world = world_of(ship)
    if world is None or getattr(world, "clock", None) is None:
        raise OrderError(f"'{verb}' wants a ship in a world; this one sails alone.")
    return world


def _start(ship: Any, evo_id: str, params: dict[str, Any], verb: str) -> Result:
    if registry.get(evo_id) is None:
        raise OrderError(f"There is no such evolution as '{evo_id}'.")
    runner = ship.extra.get("evolutions")
    if runner is None:
        raise OrderError(f"'{verb}' is work for the hands, and this ship has no runner for it.")
    text = runner.start(ship, evo_id, "ship", params)
    kind = "evolution.queued" if "will follow" in text else "evolution.started"
    return kind, text, {"verb": verb, "level": 1, "evolution": evo_id}


def _marines(ship: Any, verb: str) -> list[Any]:
    crew = ship.extra.get("crew")
    if crew is None:
        raise OrderError(f"'{verb}' wants a ship's company, and none is mustered.")
    marines = list(crew.by_station.get(Station.MARINES, []))
    if not marines:
        raise OrderError(
            "She carries no marines: her small arms are the ship's company's ('serve out the "
            "small arms')."
        )
    return marines


def _at_quarters(ship: Any) -> None:
    quarters = ship.extra.get("quarters")
    if quarters is None or not getattr(quarters, "at_quarters", False):
        raise OrderError("The company is not at quarters: 'beat to quarters' first.")


def execute(ship: Any, order: Order) -> Result:
    from freesail.combat import boarding
    from freesail.combat.small_arms import kit_of, marines_of, musketry_of, small_arms_count

    verb = order.verb
    world = _world(ship, verb)
    m = musketry_of(ship)
    data: dict[str, Any] = {"verb": verb, "level": 1}
    # -- the marines ------------------------------------------------------------------------
    if verb in ("marines fire by volley", "marines fire at will", "marines hold your fire"):
        _marines(ship, verb)
        mode = {"marines fire by volley": "volley", "marines fire at will": "at will"}.get(
            verb, "hold"
        )
        if mode != "hold":
            _at_quarters(ship)
        if m.mode == mode:
            said = {
                "volley": "firing by volley",
                "at will": "firing at will",
                "hold": "holding their fire",
            }[mode]
            raise OrderError(f"The marines are {said} already.")
        quarters = ship.extra.get("quarters")
        moved = 0
        if mode != "hold":
            moved = quarters.marines_to_arms() if quarters is not None else 0
        m.mode = mode
        kit = kit_of(world)
        n = len(marines_of(ship))
        if mode != "hold" and n == 0:
            m.mode = "hold"
            raise OrderError("No marine is fit to stand to his musket.")
        guns = (
            f" ({number_words(moved)} from the carronades, which go short by them)" if moved else ""
        )
        if mode == "volley":
            text = (
                f"Marines, fire by volley! {number_words(n)} muskets{guns}, a volley every "
                f"{int(kit.get('volley_s', 25))} seconds within musket shot of a near deck."
            )
        elif mode == "at will":
            text = (
                f"Marines, fire at will! {number_words(n)} muskets{guns}, each man at his own "
                "rate within musket shot."
            )
        else:
            back = 0
            if not m.in_tops and quarters is not None:
                back = quarters.marines_to_guns()
            text = "Marines, hold your fire! The muskets grounded" + (
                f"; {number_words(back)} back to the carronades." if back else "."
            )
        return "marines.fire", text, data | {"mode": mode, "muskets": n, "moved": moved}
    if verb in ("marines to the tops", "marines to the gangways"):
        _marines(ship, verb)
        _at_quarters(ship)
        aloft = verb == "marines to the tops"
        if m.in_tops == aloft:
            raise OrderError(
                "The marines are in the tops already."
                if aloft
                else "The marines are on deck already."
            )
        quarters = ship.extra.get("quarters")
        if aloft and quarters is not None:
            quarters.marines_to_arms()
        m.in_tops = aloft
        kit = kit_of(world)
        n = len(marines_of(ship))
        if aloft and n == 0:
            m.in_tops = False
            raise OrderError("No marine is fit to go aloft.")
        share = int(round(n * float(kit.get("tops_share", 0.2) or 0.0)))
        if aloft:
            text = (
                f"Marines to the tops! {number_words(share)} of the {number_words(n)} sent aloft "
                "as "
                "marksmen, carried up by the topmen; the rest on the poop and the gangways."
            )
        else:
            text = "Marines down from the tops to the poop and the gangways."
        return "marines.tops", text, data | {"in_tops": aloft, "aloft": share}
    # -- the small arms ------------------------------------------------------------------------
    if verb == "serve out the small arms":
        if m.served:
            raise OrderError("The small arms are served out already.")
        return _start(ship, "serve_small_arms", {}, verb)
    if verb in ("small arms fire at will", "small arms hold your fire"):
        if not m.served:
            raise OrderError("The small arms are in the chests: 'serve out the small arms' first.")
        at_will = verb == "small arms fire at will"
        if at_will:
            _at_quarters(ship)
        mode = "at will" if at_will else "hold"
        if m.small_arms_mode == mode:
            raise OrderError(
                "The small-arms men are firing at will already."
                if at_will
                else "The small arms are silent already."
            )
        m.small_arms_mode = mode
        n = small_arms_count(ship)
        text = (
            f"Small-arms men, fire at will! {number_words(n)} muskets of the stand of arms "
            "within musket shot."
            if at_will
            else "Small arms, hold your fire!"
        )
        return "small_arms.fire", text, data | {"mode": mode, "muskets": n}
    # -- the fight on deck ---------------------------------------------------------------------
    if verb == "lay her aboard":
        from freesail.orders import navigation

        ship.extra["laying_aboard"] = int(world.clock.tick)
        which = order.object or None
        if which is None:
            # the mark engaged, by the lookout's name for her, so the helm goes after her
            # and not the nearest stranger
            from freesail.combat.guns import battery_of

            battery = battery_of(ship)
            tid = getattr(battery, "target", None) if battery is not None else None
            lookout = getattr(world, "lookout", None)
            if tid and lookout is not None:
                try:
                    which = lookout.sail_name(f"sail:{tid}", "") or None
                except Exception:  # noqa: BLE001
                    which = None
        chase = replace(order, verb="give chase", verb_phrase="give chase", object=which)
        kind, text, more = navigation.execute(ship, chase)
        text = (
            "To lay her aboard: "
            + text
            + " (The helm closes her to pistol shot and under; 'grapple her' within thirty metres.)"
        )
        return kind, text, more | {"verb": verb, "laying_aboard": True}
    if verb == "grapple her":
        if boarding.grappled_to(ship):
            raise OrderError("She is grappled already.")
        from freesail.combat.guns import battery_of

        battery = battery_of(ship)
        target = getattr(battery, "target", None) if battery is not None else None
        return _start(ship, "grapple", {"target": target}, verb)
    if verb == "cast off the grapnels":
        text = boarding.cast_off(world)
        return "ship.cast_off", text, data
    if verb == "boarders away":
        text = boarding.boarders_away(world)
        return "action.boarders", text, data
    if verb == "repel boarders":
        text = boarding.repel(world)
        return "action.repel", text, data
    raise OrderError(f"'{verb}' is not an order of the fight.")
