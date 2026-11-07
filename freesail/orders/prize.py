"""The orders of the prize (spec M7 §18; package 74; the design in
`docs/design/Design-Prizes.md` §2): object `prize` in the vocabulary.

    take possession of her          the prize crew and a prize master put aboard a ship
    take possession of the <ship>   struck within a boat's pull (`prizes.possess`)
    take the prisoners aboard       her prisoners into our hold by the boat (all of them)
    take <n> of the prisoners aboard  so many of them
    burn the prize                  a prize not worth manning burnt: her people taken
    burn the <ship>                 aboard, the prize crew home, the vessel gone
    scuttle the prize               the same, sunk

Replies are `(kind, log_text, data)` like every verb's.
"""

from __future__ import annotations

import re
from typing import Any

from freesail import units
from freesail.orders.errors import OrderError
from freesail.orders.grammar import Order
from freesail.orders.prompt import world_of

__all__ = ["PRIZE_VERBS", "execute"]

Result = tuple[str, str, dict[str, Any]]

PRIZE_VERBS: tuple[str, ...] = (
    "take possession of",
    "take the prisoners aboard",
    "burn the prize",
    "scuttle the prize",
)

_N_OF = re.compile(r"^(?P<n>[\w-]+)\s+of\s+(?:the\s+)?prisoners", re.I)
_HER_WORDS = frozenset({"", "her", "him", "the prize", "the enemy", "the chase", "the ship", "it"})


def _world(ship: Any, verb: str) -> Any:
    world = world_of(ship)
    if world is None or getattr(world, "clock", None) is None:
        raise OrderError(f"'{verb}' wants a ship in a world; this one sails alone.")
    return world


def _own_vessel(world: Any) -> Any:
    """This hull's vessel of the sea: hers (`Hull.vessel`), or the player's own brought up
    to her truth."""
    v = getattr(world, "vessel", None)
    if v is not None:
        return v
    sea = getattr(world, "vessels", None)
    shadow = getattr(sea, "player_shadow", None)
    return shadow(world) if shadow is not None else None


def _sea(world: Any) -> Any:
    parent = getattr(world, "parent", None)
    return parent.vessels if parent is not None else getattr(world, "vessels", None)


def _distance_nm(world: Any, v: Any) -> float:
    from freesail.world.geo import bearing_and_distance

    here = getattr(world, "position", None)
    if here is None or getattr(v, "position", None) is None:
        return float("inf")
    return bearing_and_distance(here, v.position)[1] / units.NAUTICAL_MILE


def _struck_mark(world: Any, words: str, verb: str) -> Any:
    """The ship named, or the struck mark in hand: the battery's mark where she has struck,
    else the nearest struck enemy within a boat's pull."""
    from freesail.world.movement import BOAT_BETWEEN_NM
    from freesail.world.prizes import is_prize

    sea = _sea(world)
    if sea is None:
        raise OrderError("There is no other sail on this sea to take possession of.")
    own = _own_vessel(world)
    own_id = str(getattr(own, "id", "") or "")
    low = " ".join(str(words or "").lower().split()).rstrip(".")
    if low not in _HER_WORDS:
        v = sea.find(words) if hasattr(sea, "find") else None
        if v is None:
            raise OrderError(f"No ship named {words!r} is in sight.")
        return v
    battery = (getattr(getattr(world, "ship", None), "extra", None) or {}).get("battery")
    target = getattr(battery, "target", None) if battery is not None else None
    if target:
        v = sea.get(str(target))
        if v is not None and getattr(v, "struck", False) and not is_prize(v):
            return v
    struck = [
        v
        for v in list(getattr(sea, "vessels", []) or [])
        if getattr(v, "struck", False)
        and not v.done
        and str(v.id) != own_id
        and not is_prize(v)
        and _distance_nm(world, v) <= BOAT_BETWEEN_NM
    ]
    if not struck:
        raise OrderError(
            f"No ship has struck to us within a boat's pull ({BOAT_BETWEEN_NM:g} mile); "
            f"'{verb}' wants a struck enemy close aboard, or a ship named."
        )
    return min(struck, key=lambda v: _distance_nm(world, v))


def _our_prize(world: Any, words: str, verb: str) -> Any:
    from freesail.world.movement import BOAT_BETWEEN_NM
    from freesail.world.prizes import prizes_of

    own = _own_vessel(world)
    sea = _sea(world)
    low = " ".join(str(words or "").lower().split()).rstrip(".")
    if low not in _HER_WORDS and sea is not None:
        v = sea.find(words) if hasattr(sea, "find") else None
        if v is None:
            raise OrderError(f"No ship named {words!r} is in sight.")
        return v
    mine = prizes_of(world, str(getattr(own, "id", "") or ""))
    near = [v for v in mine if _distance_nm(world, v) <= BOAT_BETWEEN_NM]
    if not near:
        raise OrderError(
            f"No prize of ours lies within a boat's pull ({BOAT_BETWEEN_NM:g} mile)"
            + (" (we have none)" if not mine else "")
            + f"; '{verb}' wants one close aboard, or a ship named."
        )
    return min(near, key=lambda v: _distance_nm(world, v))


def _boat_ready(world: Any) -> None:
    dealings = getattr(world, "dealings", None)
    boat = getattr(dealings, "boat", None)
    if boat is None:
        return
    if getattr(boat, "lost", None):
        raise OrderError("The boat is lost; nothing crosses to her without one.")
    if getattr(boat, "away", False):
        name = str(getattr(boat, "boat_name", "the boat") or "the boat")
        raise OrderError(f"{name[:1].upper()}{name[1:]} is away; wait for her.")


def execute(ship: Any, order: Order) -> Result:
    from freesail.world import prizes as P
    from freesail.world.movement import BOAT_BETWEEN_NM

    verb = order.verb
    words = str(order.object or "")
    world = _world(ship, verb)
    if ship.extra.get("struck"):
        raise OrderError("Our own colours are struck: nothing of a prize is ours to order.")
    own = _own_vessel(world)
    if own is None:
        raise OrderError("She is no vessel of the sea; there is nothing to take possession of.")
    if verb == "take possession of":
        mark = _struck_mark(world, words, verb)
        if P.is_prize(mark):
            raise OrderError(f"The {mark.name} is a prize already.")
        if not getattr(mark, "struck", False):
            raise OrderError(f"The {mark.name} has not struck; her colours are flying.")
        d = _distance_nm(world, mark)
        if d > BOAT_BETWEEN_NM:
            raise OrderError(
                f"The {mark.name} lies {d:.1f} miles off, beyond a boat's pull "
                f"({BOAT_BETWEEN_NM:g} mile); close her first."
            )
        _boat_ready(world)
        rec = P.possess(world, own, mark, by="taken possession of", said=False)
        return (
            "prize.taken",
            f"Possession taken of the {mark.name}: {rec.get('master') or 'a prize master'} and "
            f"{rec.get('crew', 0)} hands put aboard her, {rec.get('prisoners', 0)} of her people "
            "prisoners.",
            {"verb": verb, "level": 1, "prize": str(mark.id)}
            | {k: v for k, v in rec.items() if k in ("crew", "prisoners", "master", "goal")},
        )
    if verb == "take the prisoners aboard":
        n: int | None = None
        m = _N_OF.match(words)
        rest = words
        if m:
            from freesail.orders.numbers import read_all

            n = read_all(m.group("n"))
            if n is None or n <= 0:
                raise OrderError(f"'{m.group('n')}' is no number of prisoners.")
            rest = words[m.end() :].strip(" ,")
            rest = rest.removeprefix("aboard").strip()
            rest = rest.removeprefix("from").removeprefix("out of").strip()
        else:
            rest = rest.removeprefix("from").removeprefix("out of").strip()
        prize = _our_prize(world, rest, verb)
        _boat_ready(world)
        took = P.take_prisoners_aboard(world, own, prize, n, said=False)
        if took == 0:
            raise OrderError(f"The {prize.name} has no prisoners left in her to take.")
        return (
            "prize.prisoners_aboard",
            f"{took} of the {prize.name}'s people taken aboard by the boat and confined below.",
            {"verb": verb, "level": 1, "prize": str(prize.id), "taken": took},
        )
    if verb in ("burn the prize", "scuttle the prize"):
        prize = _our_prize(world, words, verb)
        if not P.is_prize(prize) or str((P.record_of(prize) or {}).get("captor")) != str(own.id):
            raise OrderError(f"The {prize.name} is no prize of ours.")
        if _distance_nm(world, prize) > BOAT_BETWEEN_NM:
            raise OrderError(f"The {prize.name} lies beyond a boat's pull; close her first.")
        _boat_ready(world)
        how = "burnt" if verb == "burn the prize" else "scuttled"
        text = P.burn(world, own, prize, how=how, said=False)
        return "prize.burnt", text, {"verb": verb, "level": 1, "prize": str(prize.id), "how": how}
    raise OrderError(f"'{verb}' is no order of the prize's.")
