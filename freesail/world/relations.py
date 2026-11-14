"""Whether she is still what I hold her to be (package 75, the lead's readings of cda12ec9, the far
fight's (F2) to (F5); the owner's word of 2026-11-14 on mends for the cause, not the symptom).

A ship holds another in a relation from one minute to the next: a mark she fights, a struck enemy
she closes to take, her own prize, her commander and the consorts of her set. Each relation was set
when the thing it stood on was so, and each reader asked of it only the part it was written for
(the mark on the sea; the struck mark not yet his; the commander on the sea), so that the relation
outlived what it stood on: a mark taken by another, struck to another or gone (a second captor in
`taking possession` for good); a prize fired into the minute she was made (`far_action._pairs`);
a set whose other members are prizes, gone or done, or a commander two hundred miles off or struck
(`Judgement._alone`). This module is the one answer, `still(world, holder, other, what)`, asked in
every place such a relation is held, for both bodies: the far brain (`brains.FarCaptain`), the
rules captain (`captains.Captain` and the judgement they share), the far rounds and the prizes. It
reads the sea's truth, as the far brain and the prizes do (the far body is the truth), and it is
the road by which `captains.py` asks after another ship.

The relations (`what`):

- `MARK`: an enemy she fights: on the sea, her colours not struck, nobody's prize (a prize under a
  prize crew is taken back by coming up alongside, `squadrons.far_captures`, and is never fought by
  the rounds), and still an enemy to her by what she knows of her (the shot, the hail, the private
  signal, her own nation's prize: `Judgement._known_enemy`), else by the colours she shows now; a
  ship showing no colours and known nothing of is held as she was.
- `STRUCK`: a struck enemy she closes to take possession of: on the sea, struck, nobody's prize
  yet, and struck to her, or to no one known, or to one who is no longer there to take her
  (`damage["struck_to"]`, written by the far rounds' strike): gone, struck, a prize, or beyond the
  miles at which she could still take her, the distance `SUPPORT` keeps for her taker
  (`in_company_nm`; JUDGEMENT: a ship could take her who could still support her; the
  whole-change review of 80e703c7, gundeck-4). The strike's record ends with the strike: her
  colours given back (`prizes._set_colours`, the one road by which a struck ship's colours go up
  again, taken or retaken) end `struck_to` and `struck_tick`, so that a later strike by a road
  that names no taker (the near action, the cut-out, a world order) is to no one known (engine-2).
- `PRIZE`: her own prize: on the sea, a prize neither retaken nor restored, her record's captor
  hers (`prizes.prizes_of`'s rule).
- `SUPPORT`: one who could support her: her commander, a consort of her set, a man of war covering
  her, her captor's people near: on the sea, not struck, nobody's prize, and within the miles given,
  by default the distance at which her set still holds a member of it (`in_company_nm`: the set's
  book's `lost_nm`, beyond which "she is lost to the set and sails for the destination alone"; for
  a ship under orders in no set, the squadron book's, eight miles, "beyond a frigate's flags with
  the glass").

What a captain knows of a ship (`Judgement._known_enemy`: her shot at him, `fired_on`; a pirate's
act seen, `pirates`; the private signal or the hail, `recognised`) is of the people she had when he
learned it. When she changes hands (taken, retaken, restored: `prizes._nation_words`, the one road
by which a ship's nation changes) she is a new party: `changed_hands` makes every judge on the sea
(`judges`: each ship's far brain and her hull's captain, and the player's World's) forget what he
knew of her, and her own judges forget what they knew of others, so that `MARK` and every other
reader of that knowledge judge her and her people by what they show and do from then on (the
whole-change review of 80e703c7, gundeck-1: a far prize retaken by a cruiser of her own nation
fought her rescuer a minute later and struck to her, her brain holding the cruiser an enemy by the
private signal answered while she was in French hands, and the cruiser holding her one by the prize
crew's shot). JUDGEMENT: her own people's knowledge from before she was taken goes with the prize
crew's; what is not stamped with the hands it was learned under cannot be sorted.
"""

from __future__ import annotations

from typing import Any

from freesail import units
from freesail.world.geo import bearing_and_distance
from freesail.world.ships import PLAYER_ID

__all__ = [
    "MARK",
    "PRIZE",
    "RELATIONS",
    "STRUCK",
    "SUPPORT",
    "changed_hands",
    "in_company_nm",
    "judges",
    "ship_of",
    "still",
]

# What a judge knows of other ships by their ids (`Judgement._known_enemy`): the ships that fired on
# him and the ships he saw fire under false or no colours (sets), and what the private signal or the
# hail made of them (a mapping).
KNOWLEDGE_SETS = ("fired_on", "pirates")
KNOWLEDGE_MAPS = ("recognised",)

MARK = "mark"
STRUCK = "struck"
PRIZE = "prize"
SUPPORT = "support"
RELATIONS: tuple[str, ...] = (MARK, STRUCK, PRIZE, SUPPORT)


def _root(world: Any) -> Any:
    """The parent World of a crewed ship's World, a Hull's World, or the World itself."""
    parent = getattr(world, "parent", None)
    if parent is not None:
        return parent
    from freesail.world.hulls import world_of

    return world_of(world)


class _PlayersShip:
    """The player's ship where her shadow on the sea is not made (`Vessels.player_shadow`): her
    place, her colours struck or not and the nation she shows, read from her World."""

    def __init__(self, root: Any) -> None:
        from freesail.world.signals import player_locker

        ship = getattr(root, "ship", None)
        dealings = getattr(root, "dealings", None)
        colours = player_locker(root).colours
        self.id = PLAYER_ID
        self.position = root.position
        self.struck = bool("struck" in (getattr(ship, "extra", None) or {}))
        self.nation = str(getattr(dealings, "ship_nation", "") or "")
        self.nation_shown = colours.nation if colours.shows and colours.nation else None
        self.prize = None
        self.damage: dict[str, Any] = {}
        self.done = False


def ship_of(world: Any, sid: Any) -> Any:
    """The ship of id `sid` while she is on the sea: a vessel of the sea not `done`; the player's
    ship (`PLAYER_ID`) while she has a place, her shadow where it is made. None for any other."""
    if not sid:
        return None
    root = _root(world)
    sea = getattr(root, "vessels", None)
    v = sea.get(str(sid)) if sea is not None and hasattr(sea, "get") else None
    if v is not None:
        return None if getattr(v, "done", False) else v
    if str(sid) == PLAYER_ID and getattr(root, "position", None) is not None:
        return _PlayersShip(root)
    return None


def _struck(v: Any) -> bool:
    if str(getattr(v, "id", "")) == PLAYER_ID and not isinstance(v, _PlayersShip):
        # the shadow mirrors the World's `extra["struck"]` (a tick, nought at the first)
        return bool(getattr(v, "struck", False)) or _players_struck(v)
    return bool(getattr(v, "struck", False))


def _players_struck(v: Any) -> bool:
    hull = getattr(v, "crew", None)
    ship = getattr(hull, "ship", None)
    return "struck" in (getattr(ship, "extra", None) or {})


def _a_prize(v: Any) -> bool:
    from freesail.world.prizes import is_prize

    return is_prize(v)


def in_company_nm(world: Any, sid: Any) -> float:
    """The miles within which a ship is still in company with her set: her set's book's
    `lost_nm`; for a ship in no set, the squadron book's (a set of the default kind's)."""
    from freesail.world.squadrons import Squadron

    sets = getattr(_root(world), "squadrons", None)
    sq = sets.of(str(sid)) if sets is not None and hasattr(sets, "of") else None
    if sq is None:
        sq = Squadron(id="", name="")
    return float(sq.lost_nm)


def _enemy_to(root: Any, holder: Any, judge: Any, other: Any) -> bool:
    """Whether `other` is an enemy to the holder by what the holder knows: her judge's knowledge
    first (`Judgement._known_enemy`: the shot, the pirate's act, the private signal, the hail, a
    prize of her own nation), else the colours `other` shows now against the holder's nation; with
    none shown and nothing known, as she was held."""
    oid = str(getattr(other, "id", "") or "")
    if judge is not None and hasattr(judge, "_known_enemy"):
        known = judge._known_enemy({"id": oid})
        if known is not None:
            return bool(known)
    shown = getattr(other, "nation_shown", None)
    if not shown:
        return True
    nation = ""
    if judge is not None:
        from freesail.world.signalling import _own_nation

        try:
            nation = _own_nation(judge)
        except Exception:  # noqa: BLE001 - a judge with no world of its own
            nation = ""
    if not nation:
        nation = str(getattr(holder, "nation", "") or "")
    nations = getattr(root, "nations", None)
    if nations is None or not nation:
        return True
    return bool(nations.at_war(str(shown), nation))


def still(
    world: Any,
    holder: Any,
    other: Any,
    what: str,
    *,
    judge: Any = None,
    within_nm: float | None = None,
) -> bool:
    """Whether the ship `other` (a vessel or an id) is still what `holder` (a vessel or an id: the
    far body's, a crewed hull's, or the player's `PLAYER_ID`) holds her to be, by the relation
    `what` (the module's head). `judge` is the captain whose knowledge decides an enemy (by
    default the holder's far brain); `within_nm` the miles of `SUPPORT` (by default the holder's
    `in_company_nm`). A ship gone from the sea is nothing to anybody."""
    if what not in RELATIONS:
        raise ValueError(f"'{what}' is no relation: {', '.join(RELATIONS)}")
    root = _root(world)
    hid = str(getattr(holder, "id", holder) or "")
    oid = str(getattr(other, "id", other) or "")
    if not oid or oid == hid:
        return False
    o = other if not isinstance(other, str) else ship_of(root, oid)
    if o is None or getattr(o, "done", False):
        return False
    if what == PRIZE:
        from freesail.world.prizes import record_of

        rec = record_of(o)
        return bool(rec) and _a_prize(o) and str(rec.get("captor")) == hid
    if what == STRUCK:
        if not _struck(o) or _a_prize(o):
            return False
        to = str((getattr(o, "damage", None) or {}).get("struck_to") or "")
        if not to or to == hid:
            return True
        taker = ship_of(root, to)
        if taker is None or _struck(taker) or _a_prize(taker):
            return True
        if getattr(taker, "position", None) is None or getattr(o, "position", None) is None:
            return False
        _, d = bearing_and_distance(taker.position, o.position)
        return d > in_company_nm(root, to) * units.NAUTICAL_MILE
    if _struck(o) or _a_prize(o):
        return False
    her = holder if not isinstance(holder, str) else ship_of(root, hid)
    if what == MARK:
        if judge is None:
            judge = getattr(her, "brain", None)
        return _enemy_to(root, her, judge, o)
    # SUPPORT
    if her is None or getattr(her, "position", None) is None or o.position is None:
        return False
    nm = float(within_nm) if within_nm is not None else in_company_nm(root, hid)
    _, d = bearing_and_distance(her.position, o.position)
    return d <= nm * units.NAUTICAL_MILE


def judges(world: Any) -> list[Any]:
    """Every captain on the sea whose knowledge decides an enemy (`Judgement._known_enemy`): each
    ship's far brain and her hull's captain where she is crewed, and the player's World's captain;
    each once."""
    root = _root(world)
    out: list[Any] = []
    seen: set[int] = set()

    def add(judge: Any) -> None:
        if judge is not None and id(judge) not in seen:
            seen.add(id(judge))
            out.append(judge)

    sea = getattr(root, "vessels", None)
    for v in list(getattr(sea, "vessels", None) or []):
        add(getattr(v, "brain", None))
        hull = getattr(v, "crew", None)
        add(getattr(hull, "captain", None) if hull is not None else None)
    add(getattr(root, "captain", None))
    return out


def _own_judges(root: Any, vessel: Any) -> list[Any]:
    out = [getattr(vessel, "brain", None)]
    hull = getattr(vessel, "crew", None)
    out.append(getattr(hull, "captain", None) if hull is not None else None)
    if str(getattr(vessel, "id", "")) == PLAYER_ID:
        out.append(getattr(root, "captain", None))
    return [j for j in out if j is not None]


def changed_hands(world: Any, vessel: Any) -> None:
    """She has changed hands (the module's head): what every judge on the sea knew of her by her
    shot, a pirate's act, the signal or the hail is forgotten, and what her own judges knew of any
    ship. Called by `prizes._nation_words`, the one road by which a ship's nation changes."""
    root = _root(world)
    sid = str(getattr(vessel, "id", "") or "")
    own = {id(j) for j in _own_judges(root, vessel)}
    for judge in [*judges(root), *_own_judges(root, vessel)]:
        mine = id(judge) in own
        for name in KNOWLEDGE_SETS:
            held = getattr(judge, name, None)
            if isinstance(held, set):
                if mine:
                    held.clear()
                else:
                    held.discard(sid)
        for name in KNOWLEDGE_MAPS:
            held = getattr(judge, name, None)
            if isinstance(held, dict):
                if mine:
                    held.clear()
                else:
                    held.pop(sid, None)
