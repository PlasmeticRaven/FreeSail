"""The glass on a near ship (spec M7b §21b; package 56).

    the glass on <ship>       what the glass shows of her: her rig and colours as `make
                              her out` gives them, and, by the tiers of her distance in
                              daylight and clear weather, her manoeuvre within two miles,
                              her work within eight cables and the evolution's own words
                              within four; by night only her light, if she shows one
    the glass on the sail     the nearest sail in sight

A reading every station may ask (object `glass`, `agents.agent.Domain.why_not`), answered
from what the lookout has in sight (`world.lookout.Lookout.glass_on`); refused in words
with no sail in sight or none answering to the words.
"""

from __future__ import annotations

from typing import Any

from freesail.orders.errors import OrderError
from freesail.orders.grammar import Order
from freesail.orders.prompt import world_of

__all__ = ["execute"]


def execute(ship: Any, order: Order) -> tuple[str, str, dict[str, Any]]:
    world = world_of(ship)
    lookout = getattr(world, "lookout", None) if world is not None else None
    if lookout is None:
        raise OrderError("There is no lookout aloft to send the glass to.")
    which = " ".join(str(order.object or "").split()).strip(" .") or None
    if which is not None and which.lower() in ("her", "the sail", "the stranger", "the ship"):
        which = None
    text, data = lookout.glass_on(world, which)
    return "lookout.glass", text, {"verb": order.verb, "level": "reading"} | data
