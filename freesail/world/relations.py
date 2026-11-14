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
  her, her captor's people near: on the sea, not struck, nobody's prize, of her side (her own
  nation or an ally of it, by the nations both truly are: the sea's truth, as her callers' own
  rules of "a ship of her nation" read it; the lead's last list of 2026-11-14, item 4: a French 74
  a mile from a British frigate supported her), and within the miles given, by default the
  distance at which her set still holds a member of it (`in_company_nm`: the set's book's
  `lost_nm`, beyond which "she is lost to the set and sails for the destination alone"; for a ship
  under orders in no set, the squadron book's, eight miles, "beyond a frigate's flags with the
  glass").

The holder is asked about as the other is (the lead's last list, item 4): a holder who is not on the
sea (no id, an id the sea has not, a ship `done`) holds nobody in any relation; a holder struck
fights nobody (`MARK`), takes nobody (`STRUCK`) and is supported by nobody (`SUPPORT`: her strike
is past their help), and keeps her prizes (`PRIZE`: her prize crews hold them until they are
retaken; JUDGEMENT), so that no caller asks it again.

**Who has fired on whom** (the lead's last list, item 2) is one record, kept on the sea's World
(`fired`, `fired_on`, `has_fired`): by the ids of the sea (a vessel's, the player's ship's
`PLAYER_ID`), never by a name two ships may share; written by every road a ship fires on another
(the near battery, `combat.action._fired_on`; the far rounds and the far reply,
`combat.far_action`), read by every judge of the ship fired on (`Judgement.fired_on` is her row of
it, her far brain's and her hull's captain's alike) and so by `MARK`, far as near: package 70's rule
"she fired on me: an enemy whatever her colours". Before it the far rounds kept a book of their own
by the ships' names (`root._far_rounds`) and never wrote the judges' sets, so that an enemy who
hoisted false colours in a far fight ended the action of the ship she was firing into; and the far
brain's set and her hull's captain's were two, neither carried to the other at the promotion or the
demotion.

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

Every relation held on her ends there too, the cause being one (the lead's last list, item 3: a
relation held after what it stood on is gone): the sail spoken and the chase given up
(`spoken_ids`, `given_up`, read raw by `Judgement._spoken`: a cruiser who spoke her or gave her up
never looked at her again once the enemy took her, and so never retook her), the player's having
spoken her (`Vessel.spoken`, the lookout's flag); the shots of the one record, fired by her or at
her; the orders she sailed under (`under_orders_of`, hers and her hull's: a French prize crew left
"to her commander's book", the British commander's) and the orders of every ship under hers; the
far rounds' book of each pair she is in (`root._far_rounds`); and every near battery laid on her
(`combat.action`): its World is told she has changed hands, and its next tick asks `MARK` of her as
she now is, holding the fire and telling the deck why where she is no mark (the lead's last list,
item 5).
"""

from __future__ import annotations

from typing import Any

from freesail import units
from freesail.world.geo import bearing_and_distance
from freesail.world.ships import PLAYER_ID

__all__ = [
    "CHANGED_HANDS",
    "FIRED_ON",
    "MARK",
    "PRIZE",
    "RELATIONS",
    "STRUCK",
    "SUPPORT",
    "changed_hands",
    "fired",
    "fired_on",
    "has_fired",
    "in_company_nm",
    "judges",
    "ship_of",
    "still",
]

# What a judge knows of other ships by their ids beyond the one record of shots (`FIRED_ON`): the
# ships he saw fire under false or no colours, the sails he has spoken and the chases he has given
# up (sets: `Judgement._known_enemy`, `Judgement._spoken`), and what the private signal or the hail
# made of them (a mapping).
KNOWLEDGE_SETS = ("pirates", "spoken_ids", "given_up")
KNOWLEDGE_MAPS = ("recognised",)

# The one record of who has fired on whom (the module's head), on the sea's World: the id of each
# ship fired on, to the ids of the ships that have fired on her.
FIRED_ON = "_fired_on"
# A ship's World told that the mark of her battery has changed hands (`changed_hands`), for the
# battery's next tick to judge (`combat.action._watch_changed_hands`): the ids, in her ship's
# `extra`.
CHANGED_HANDS = "mark_changed_hands"

MARK = "mark"
STRUCK = "struck"
PRIZE = "prize"
SUPPORT = "support"
RELATIONS: tuple[str, ...] = (MARK, STRUCK, PRIZE, SUPPORT)


def _root(world: Any) -> Any:
    """The sea's World: a crewed ship's hull's (her `parent` the player's hull, whose World it is),
    a Hull's, or the World itself; the one place the one record is kept."""
    from freesail.world.hulls import world_of

    parent = getattr(world, "parent", None)
    return world_of(parent if parent is not None else world)


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


def _id(x: Any) -> str:
    return str(getattr(x, "id", x) or "")


def _book(world: Any) -> dict[str, set[str]]:
    """The one record of who has fired on whom, on the sea's World (made at the first shot)."""
    root = _root(world) if world is not None else None
    d = getattr(root, "__dict__", None)
    if d is None:
        return {}
    book = d.get(FIRED_ON)
    if book is None:
        book = d[FIRED_ON] = {}
    return book


def fired(world: Any, firer: Any, target: Any) -> None:
    """She (`firer`, a vessel or an id) fired on `target`: written in the one record, by every road
    a ship fires on another (the module's head)."""
    fid, tid = _id(firer), _id(target)
    if fid and tid and fid != tid:
        _book(world).setdefault(tid, set()).add(fid)


def fired_on(world: Any, target: Any) -> set[str]:
    """The ids of the ships that have fired on `target`: her row of the one record, the set itself
    (`Judgement.fired_on`), so that what her judges add to it is the record's."""
    return _book(world).setdefault(_id(target), set())


def has_fired(world: Any, firer: Any, target: Any) -> bool:
    """Whether `firer` has fired on `target`, by the one record."""
    return _id(firer) in _book(world).get(_id(target), ())


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
    elif has_fired(root, oid, getattr(holder, "id", "")):
        return True  # she fired on the holder: the one record, read with no judge to ask
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


def _of_her_side(root: Any, her: Any, other: Any) -> bool:
    """Whether `other` is of her side: her own nation or an ally of it, by the nations both truly
    are (the module's head, `SUPPORT`)."""
    a = str(getattr(her, "nation", "") or "")
    b = str(getattr(other, "nation", "") or "")
    if not a or not b:
        return False
    if a == b:
        return True
    nations = getattr(root, "nations", None)
    return bool(nations is not None and hasattr(nations, "allied") and nations.allied(a, b))


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
    `in_company_nm`). A ship gone from the sea is nothing to anybody, and holds nobody; a holder
    struck holds nobody but her prizes (the module's head)."""
    if what not in RELATIONS:
        raise ValueError(f"'{what}' is no relation: {', '.join(RELATIONS)}")
    root = _root(world)
    hid = str(getattr(holder, "id", holder) or "")
    oid = str(getattr(other, "id", other) or "")
    if not oid or not hid or oid == hid:
        return False
    o = other if not isinstance(other, str) else ship_of(root, oid)
    if o is None or getattr(o, "done", False):
        return False
    her = holder if not isinstance(holder, str) else ship_of(root, hid)
    if her is None or getattr(her, "done", False):
        return False
    if what != PRIZE and _struck(her):
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
    if what == MARK:
        if judge is None:
            judge = getattr(her, "brain", None)
        return _enemy_to(root, her, judge, o)
    # SUPPORT
    if not _of_her_side(root, her, o):
        return False
    if getattr(her, "position", None) is None or o.position is None:
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
        add(getattr(v, "_signal_reader", None))  # the least captain of a ship with no brain
        hull = getattr(v, "crew", None)
        add(getattr(hull, "captain", None) if hull is not None else None)
    add(getattr(root, "captain", None))
    return out


def _own_judges(root: Any, vessel: Any) -> list[Any]:
    out = [getattr(vessel, "brain", None), getattr(vessel, "_signal_reader", None)]
    hull = getattr(vessel, "crew", None)
    out.append(getattr(hull, "captain", None) if hull is not None else None)
    if str(getattr(vessel, "id", "")) == PLAYER_ID:
        out.append(getattr(root, "captain", None))
    return [j for j in out if j is not None]


def changed_hands(world: Any, vessel: Any) -> None:
    """She has changed hands (the module's head): what every judge on the sea knew of her by her
    shot, a pirate's act, the signal, the hail, a speaking or a chase given up is forgotten, and
    what her own judges knew of any ship; and every relation held on her ends: the one record's
    shots by her and at her, the player's having spoken her, the orders she sailed under and the
    orders of the ships under hers, the far rounds' book of her pairs, and the near batteries laid
    on her are told (the lead's last list, items 2, 3 and 5). Called by `prizes._nation_words`,
    the one road by which a ship's nation changes."""
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
    if not sid:
        return
    # the one record: who fired on her, and whom she fired on
    book = _book(root)
    book.pop(sid, None)
    for firers in book.values():
        firers.discard(sid)
    # the player's lookout's flag: spoken within hail by the player's ship
    if getattr(vessel, "spoken", False):
        vessel.spoken = False
    # the orders she sailed under, and the orders of every ship under hers
    sea = getattr(root, "vessels", None)
    ships = list(getattr(sea, "vessels", None) or [])
    for v in [vessel, *ships]:
        boss = str(getattr(v, "under_orders_of", "") or "")
        if boss and (v is vessel or boss == sid):
            v.under_orders_of = ""
            hull = getattr(v, "crew", None)
            if hull is not None and getattr(hull, "under_orders_of", ""):
                hull.under_orders_of = ""
    held = str(getattr(root, "under_orders_of", "") or "")
    if held and (held == sid or sid == PLAYER_ID):
        root.under_orders_of = ""  # the player's ship under hers, or the player's ship herself
    # the far rounds' book of each pair she is in
    rounds = getattr(root, "__dict__", {}).get("_far_rounds")
    if isinstance(rounds, dict):
        for key in [k for k in rounds if sid in str(k).split("|")]:
            del rounds[key]
    # the near batteries laid on her: the next tick of each judges her as she now is
    for hw in [root, *(getattr(v, "crew", None) for v in ships)]:
        ship = getattr(hw, "ship", None) if hw is not None else None
        extra = getattr(ship, "extra", None)
        battery = extra.get("battery") if isinstance(extra, dict) else None
        if battery is not None and str(getattr(battery, "target", "") or "") == sid:
            extra.setdefault(CHANGED_HANDS, set()).add(sid)
