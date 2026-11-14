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

COMMAND_VERBS: tuple[str, ...] = ("take command of", "transfer")

# `transfer <who> [from the "Y"] to the "X"[, and lay the Y up]` (step 2, the design's §6.2)
_TRANSFER = re.compile(
    r"^(?P<who>.+?)(?:\s+from\s+(?P<giver>.+?))?\s+to\s+(?P<to>.+?)"
    r"(?:,?\s+and\s+(?:lay|laying)\s+(?:the\s+)?(?P<lay>.+?)\s+up)?$",
    re.I,
)

# Package 109's words for a prize (its refused phrase 'take command', made this order's own
# refusal by package 60): command of a prize is taken by possession, not by words.
PRIZE_WORDS = (
    "Command of a prize is not taken by words: her prize master and prize crew are put aboard "
    "her by 'take possession of her'; to go aboard another ship yourself, 'go to the boat' and "
    "'pull for' her."
)

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


def parse(words: str, old: str = "old ship") -> tuple[str, str, str, str]:
    """(the ship's words, how the old ship is settled, the officer's words, the intent); `old`,
    the name of the ship he commands, for the refusal's example."""
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
                f"Say how the {old} is left: '..., and lay the {old} up', or '..., and leave "
                f"the {old} to' an officer of hers and what she is to do."
            )
    ship = " ".join(ship.replace('"', " ").split())
    return ship, how, who.strip().strip('"'), intent.strip()


def execute(ship: Any, order: Order) -> Result:
    from freesail.world import knowledge
    from freesail.world.command import CommandError, take_up
    from freesail.world.hulls import world_of as root_of
    from freesail.world.movement import hull_of

    if order.verb == "transfer":
        return _transfer(ship, order)
    world = world_of(ship)
    if world is None or getattr(world, "clock", None) is None:
        raise OrderError("She sails alone: there is no other ship here to take command of.")
    root = root_of(world)
    person = knowledge.players_person(root)
    if person is None:
        raise OrderError("You are aboard no ship here to take command of another.")
    words, how, who, intent = parse(order.object or "", _ship_name(root))
    key = words.lower().removeprefix("the ")
    if key == "prize" or key.endswith(" prize") or key.startswith("prize "):
        raise OrderError(PRIZE_WORDS)
    if key in _HER:
        hull = hull_of(root, getattr(person, "hull", None))
        if hull is None:
            raise OrderError("You are aboard no ship; name the ship you take command of.")
    else:
        hull = ship_for_him(root, words)
    if _prize_not_condemned(hull):
        raise OrderError(PRIZE_WORDS)
    try:
        text, data = take_up(root, person, hull, how=how, officer=who, intent=intent, said=False)
    except CommandError as e:
        raise OrderError(str(e)) from None
    return "ship.taken_up", text, {"verb": order.verb, "level": 1, **data}


def _transfer(ship: Any, order: Order) -> Result:
    """`transfer ... to the "Fly"` (step 2; `world.transfer.transfer`)."""
    from freesail.world import knowledge
    from freesail.world.hulls import world_of as root_of
    from freesail.world.transfer import TransferError, transfer

    world = world_of(ship)
    if world is None or getattr(world, "clock", None) is None:
        raise OrderError("She sails alone: there is no other ship here to move her people to.")
    root = root_of(world)
    person = knowledge.players_person(root)
    if person is None:
        raise OrderError("You are aboard no ship here to move her people.")
    # the words after the verb as said, their commas kept (the order's `object` has them read
    # away, and a list of names is read by them: the lead's second reading of 4dda3dfe)
    said = str(order.text or "")
    phrase = str(order.verb_phrase or "")
    if phrase and said.lower().startswith(phrase.lower()):
        said = said[len(phrase) :]
    else:
        said = str(order.object or "")
    text = " ".join(said.split()).strip().rstrip(".")
    m = _TRANSFER.match(text)
    if m is None:
        mine = _ship_name(root)
        raise OrderError(
            f"Say whom and to which ship: 'transfer twenty hands to the {mine}', 'transfer the "
            f"people and the hands to the {mine}', or name them."
        )

    def named(words: str) -> Any:
        return ship_for_him(root, words)

    receiver = named(m.group("to"))
    giver = named(m.group("giver")) if m.group("giver") else None
    lay = m.group("lay")
    if lay:
        laid = named(lay)
        if giver is not None and laid is not giver:
            raise OrderError("The ship laid up by a transfer is the one her people leave.")
        giver = laid
    try:
        said, data = transfer(root, person, receiver, m.group("who"), giver=giver, lay_up=bool(lay))
    except TransferError as e:
        raise OrderError(str(e)) from None
    return "company.transfer", said, {"verb": order.verb, "level": 1, **data}


def _ship_name(root: Any) -> str:
    """The name of the ship he commands, for a refusal's example."""
    from freesail.world.movement import hull_name

    players = getattr(root, "players", None)
    return hull_name(players).removeprefix("the ") if players is not None else "ship"


def ship_for_him(root: Any, words: str) -> Any:
    """The ship his order names (package 60, the lead's second reading of 4dda3dfe, item 4):
    the ship he commands by her name or 'the ship'; another by her hull's id, her name, or as
    her lookout names her in sight; refused in the world's words, naming no sail he has not
    seen: a name he knows of no ship by, a ship with no hull of her own (beyond a boat's reach,
    asleep and never boarded), an observed world."""
    from freesail.world.lookout import vessel_in_sight

    said = " ".join(str(words).replace('"', " ").split())
    key = said.lower().removeprefix("the ")
    if getattr(root, "observed", False):
        raise OrderError("You command no ship here.")
    players = getattr(root, "players", None)
    own = _ship_name(root).lower()
    if key in ("ship", "us", "her", "this ship", "our ship", own):
        return players
    hulls = getattr(root, "hulls", None) or {}
    if key in hulls:
        return hulls[key]
    vessels = getattr(root, "vessels", None)
    vessel = vessels.find(said) if vessels is not None else None
    if vessel is None:
        vessel = vessel_in_sight(root, said)
    name = " ".join(w[:1].upper() + w[1:] for w in key.split()) or "that ship"
    if vessel is None or vessel.done:
        raise OrderError(f"You know of no ship called the {name} hereabouts.")
    if vessel.crew is None:
        raise OrderError(f"The {vessel.name} lies beyond a boat's reach of you.")
    return vessel.crew


def _prize_not_condemned(hull: Any) -> bool:
    """A prize the court has not condemned (74's record): taken by possession, not by words."""
    from freesail.world import prizes as P

    vessel = getattr(hull, "vessel", None)
    if vessel is None or not P.is_prize(vessel):
        return False
    rec = P.record_of(vessel) or {}
    return str((rec.get("court") or {}).get("sentence") or "") != "condemned"
