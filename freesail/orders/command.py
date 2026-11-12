"""The order that changes the player's ship (package 60, step 1; the design in
`docs/design/Design-ShipBought.md` §2.6): object `command` in the vocabulary.

    take command of her                     aboard her: she is his ship from here
    take command of the "Fly"               the same, by her name
    ..., and lay the Amazon up              the old ship laid up at the port's anchorage
    ..., and leave the Amazon to Mr Ryan [to <intent>]
                                            the old ship left to her officer, under an
                                            intent where one is given

The act is `world.command.take_up`; the order is its journal (an input like every order), so
that a replay gives the change again at its tick. Replies are `(kind, log_text, data)`.
"""

from __future__ import annotations

import re
from typing import Any

from freesail.orders.errors import OrderError
from freesail.orders.grammar import Order
from freesail.orders.prompt import world_of

__all__ = ["COMMAND_VERBS", "execute", "parse"]

Result = tuple[str, str, dict[str, Any]]

COMMAND_VERBS: tuple[str, ...] = ("take command of",)

_HER = frozenset({"", "her", "this ship", "this one", "the ship she is", "it"})
_LAY = re.compile(
    r"^(?:lay|laying)\s+(?:the\s+)?(?P<ship>.+?)\s+up"
    r"(?:\s+in\s+the\s+charge\s+of\s+(?P<who>.+))?$",
    re.I,
)
_LEAVE = re.compile(
    r"^(?:leave|leaving)\s+(?:the\s+)?(?P<ship>.+?)\s+to\s+"
    r"(?P<who>(?:mr|mister|captain|lieutenant)\.?\s+\S+|the\s+[\w' ]+?|\S+)"
    r"(?:\s+to\s+(?P<intent>.+))?$",
    re.I,
)


def parse(words: str) -> tuple[str, str, str, str]:
    """(the ship's words, how the old ship is settled, the officer's words, the intent)."""
    text = " ".join(str(words).split()).strip().rstrip(".")
    ship, how, who, intent = text, "", "", ""
    m = re.search(r",?\s+and\s+(?=(?:lay|laying|leave|leaving)\b)", text, re.I)
    if m:
        ship, tail = text[: m.start()], text[m.end() :]
        lay = _LAY.match(tail)
        leave = _LEAVE.match(tail)
        if lay:
            how, who = "laid up", (lay.group("who") or "")
        elif leave:
            how, who, intent = "left", leave.group("who"), (leave.group("intent") or "")
        else:
            raise OrderError(
                "Say how the old ship is left: '..., and lay the Amazon up' or '..., and leave the "
                "Amazon to Mr Ryan [to <intent>]'."
            )
    ship = " ".join(ship.replace('"', " ").split())
    return ship, how, who.strip().strip('"'), intent.strip()


def execute(ship: Any, order: Order) -> Result:
    from freesail.world import knowledge
    from freesail.world.command import CommandError, take_up
    from freesail.world.hulls import world_of as root_of
    from freesail.world.movement import hull_of
    from freesail.world.orders import WorldOrderError, hull_named

    world = world_of(ship)
    if world is None or getattr(world, "clock", None) is None:
        raise OrderError("'take command of' wants a ship in a world; this one sails alone.")
    root = root_of(world)
    person = knowledge.players_person(root)
    if person is None:
        raise OrderError("Nobody of yours is at the prompt to take command of a ship.")
    words, how, who, intent = parse(order.object or "")
    key = words.lower().removeprefix("the ")
    if key in _HER:
        hull = hull_of(root, getattr(person, "hull", None))
        if hull is None:
            raise OrderError("You are aboard no ship; name the ship you take command of.")
    else:
        try:
            hull = hull_named(root, words, make=False)
        except WorldOrderError as e:
            raise OrderError(str(e).rstrip(".") + ".") from None
        if hull is root:
            hull = root.players
    try:
        text, data = take_up(root, person, hull, how=how, officer=who, intent=intent)
    except CommandError as e:
        raise OrderError(str(e)) from None
    return "ship.taken_up", text, {"verb": order.verb, "level": 1, **data}
