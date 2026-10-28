"""The orders of the gun deck (spec M7 §8, §8a; package 70; `docs/design/Design-WorkInAction.md`).

    engage her to starboard         the mark and the side: a standing intention the battery
    engage the brig to larboard     keeps (the engaged side's guns served and fired at her);
    engage on both sides            'her' or nothing is the enemy nearest, else the sail nearest
    load with round shot            the charge the guns are loaded with from now (round, chain,
                                    grape, double, a blank cartridge); a loaded gun keeps its
                                    charge until it is fired
    run out / run in the guns       whether the guns are run out when loaded (run in, they are
                                    kept loaded behind closed ports; a tack is the easier)
    aim at her rigging              the aim's doctrine: the rigging, the hull, or between wind
                                    and water
    fire as they bear               the firing's doctrine: each gun as it is loaded and bears
    fire by divisions               (the period's independent fire); the forward and the
    hold your fire                  after division by turns; or no gun fires but by name or
                                    at the word
    fire on the up roll             the gun captain's moment: the up-roll for the rigging, the
    fire on the down roll           down-roll for the hull (spec M7 §9)
    fire                            the broadside at the word: the engaged side's guns that
    fire the starboard broadside    are loaded and bear, together, once; a side named fires
    fire No. 3 gun                  that side; a gun by its number or its place fires once;
    fire the bow chaser             a shot across her bows and a gun to leeward strike nothing
    fire a shot across her bows     and say so
    fire a gun to leeward
    cease firing                    the firing's doctrine back to hold; the mark is kept
    strike the colours              never refused: the colours come down, the guns fall silent
                                    and she lies to; the consequence told (what follows is 74's)

Practice at the great guns (practice and resupply, between packages 72 and 73;
docs/design/Build-PracticeAndResupply.md §3.3, §6):

    heave a cask overboard          an empty cask with a flag on a staff over the side from
                                    the quarter (the lee one unless one is named) for a mark;
                                    refused by night and with no chart
    engage the cask to starboard    the cask the mark ('the mark' and 'the target' mean it
                                    while one is in the water, and a sail otherwise)
    engage a mark four cables on    a notional mark at a bearing (the bow, the beam or the
      the starboard beam            quarter, where a gun of hers bears) and a range, by
                                    night and in fog as by day
    exercise the guns               the guns served in dumb show, without powder and no shot
    exercise the starboard battery  leaving the ship; a loaded gun is run out and pointed only
    cease exercising                the dumb show over (and piped down from quarters)
    fill cartridges                 the gunner to fill cartridges from the powder below, and
    cease filling                   to fill no more until he is ordered

The heave and the gunner's two are given out of quarters as well; the rest want the hands
at quarters, as every order of the gun deck does.

The guns' cycle itself is no order's: it runs in `combat.guns.Battery` while hands and
powder last (item 1's design: a standing intention, logged when it changes something). The
hands come from the quarter bill (`crew.quarters`): the orders here are refused in words
until the hands are at quarters (`beat to quarters`, or `clear for action`), and `cast
loose the guns` has the crews cast them loose. The boarders are 73's (the vocabulary
refuses them in words). A gun's number is the pair's (No. 3 is the third pair from
forward, either side); a place is the bow chaser, the stern chaser or a swivel.
"""

from __future__ import annotations

import math
import re
from typing import Any

from freesail import units
from freesail.combat import marks
from freesail.combat import shot as S
from freesail.combat.guns import (
    Aim,
    Battery,
    FireMode,
    battery_of,
    pivot_arc,
)
from freesail.crew.model import number_words
from freesail.crew.quarters import quarters_of
from freesail.orders import numbers
from freesail.orders.errors import OrderError
from freesail.orders.grammar import Order
from freesail.orders.prompt import world_of
from freesail.ship.parts import BARREL_LB, Charge, Gun, fit_levels, gun_words, kind_rank, magazine

__all__ = ["GUNNERY_VERBS", "check", "execute", "guns_named"]

Result = tuple[str, str, dict[str, Any]]

GUNNERY_VERBS: tuple[str, ...] = (
    "engage",
    "load",
    "run out the guns",
    "run in the guns",
    "aim at",
    "fire as they bear",
    "fire by divisions",
    "hold your fire",
    "fire on the roll",
    "fire",
    "cease firing",
    "strike the colours",
    "guns before sail",
    "sail before guns",
    # practice and resupply (between packages 72 and 73)
    "heave a cask overboard",
    "exercise the guns",
    "cease exercising",
    "fill cartridges",
    "cease filling",
)

_SIDES = {
    "starboard": "starboard",
    "larboard": "larboard",
    "port": "larboard",
    "both": "both",
    "both sides": "both",
    "either side": "both",
}
_CHARGES = {
    "round": Charge.ROUND,
    "round shot": Charge.ROUND,
    "roundshot": Charge.ROUND,
    "ball": Charge.ROUND,
    "shot": Charge.ROUND,
    "chain": Charge.CHAIN,
    "chain shot": Charge.CHAIN,
    "bar shot": Charge.CHAIN,
    "bar": Charge.CHAIN,
    "grape": Charge.GRAPE,
    "grape shot": Charge.GRAPE,
    "grapeshot": Charge.GRAPE,
    "canister": Charge.GRAPE,
    "case": Charge.GRAPE,
    "case shot": Charge.GRAPE,
    "double": Charge.DOUBLE,
    "double shot": Charge.DOUBLE,
    "two round shot": Charge.DOUBLE,
    "blank": Charge.BLANK,
    "a blank": Charge.BLANK,
    "blank cartridge": Charge.BLANK,
    "a blank cartridge": Charge.BLANK,
    "powder": Charge.BLANK,
    "powder alone": Charge.BLANK,
}
_AIMS = {
    "rigging": Aim.RIGGING,
    "her rigging": Aim.RIGGING,
    "the rigging": Aim.RIGGING,
    "her masts": Aim.RIGGING,
    "the masts": Aim.RIGGING,
    "her spars": Aim.RIGGING,
    "her sails": Aim.RIGGING,
    "aloft": Aim.RIGGING,
    "high": Aim.RIGGING,
    "hull": Aim.HULL,
    "her hull": Aim.HULL,
    "the hull": Aim.HULL,
    "her deck": Aim.HULL,
    "her guns": Aim.HULL,
    "low": Aim.HULL,
    "between wind and water": Aim.BETWEEN,
    "her waterline": Aim.BETWEEN,
    "the waterline": Aim.BETWEEN,
    "between": Aim.BETWEEN,
}
_HER = (
    "her",
    "him",
    "the enemy",
    "the stranger",
    "the chase",
    "the sail",
    "the mark",
    "the target",
)
_GUN_NUMBER = re.compile(r"^(?:the\s+)?(?:no|number|num)?\s*(\d+)\s*(?:gun|carronade)?$")
_WORD_NUMBERS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
}


# -- the entry -----------------------------------------------------------------------------


def execute(ship: Any, order: Order) -> Result:
    battery = battery_of(ship)
    if battery is None:
        raise OrderError("She carries no guns.")
    verb = order.verb
    said = " ".join(str(order.object or "").split()).strip(" .")
    if verb == "strike the colours":
        return _strike(ship, battery, said)
    if verb == "cease firing":
        return _cease(ship, battery)
    # practice and resupply: the cask over the side, and the gunner's filling, are no work
    # of the gun crews'
    if verb == "heave a cask overboard":
        return _heave(ship, battery, said)
    if verb == "fill cartridges":
        return _fill(ship, True)
    if verb == "cease filling":
        return _fill(ship, False)
    quarters = quarters_of(ship)
    if quarters is None or not quarters.at_quarters:
        raise OrderError(
            "The hands are not at quarters: beat to quarters (or clear for action) first, "
            "and cast loose the guns."
        )
    if verb == "engage":
        return _engage(ship, battery, said)
    if verb == "load":
        return _load(ship, battery, said)
    if verb == "run out the guns":
        return _run_out(ship, battery, True)
    if verb == "run in the guns":
        return _run_out(ship, battery, False)
    if verb == "aim at":
        return _aim(ship, battery, said)
    if verb == "fire as they bear":
        return _mode(ship, battery, FireMode.AS_THEY_BEAR)
    if verb == "fire by divisions":
        return _mode(ship, battery, FireMode.BY_DIVISIONS)
    if verb == "hold your fire":
        return _mode(ship, battery, FireMode.HOLD)
    if verb == "fire on the roll":
        return _roll(ship, battery, order.verb_phrase)
    if verb == "fire":
        return _fire(ship, battery, said)
    if verb in ("guns before sail", "sail before guns"):
        return _priority(ship, quarters, verb)
    if verb == "exercise the guns":
        return _exercise(ship, battery, order.verb_phrase, said)
    if verb == "cease exercising":
        return _cease_exercise(ship, battery)
    raise OrderError(f"'{verb}' is in the vocabulary but has no meaning at the guns yet.")


def check(ship: Any, order: Order) -> None:
    """A standing order's action read whole (`orders.read_whole`): the words after the
    verb that must make sense now, with nothing done."""
    said = " ".join(str(order.object or "").split()).strip(" .")
    if order.verb == "load" and said:
        _charge_of(said)
    elif order.verb == "aim at" and said:
        _aim_of(said)
    elif order.verb == "engage" and said:
        if _NOTIONAL.match(said):
            _notional_of(ship, said)  # a notional mark: its range and its bearing
        else:
            _side_of(said)  # the side's words; the mark is the moment's
    elif order.verb == "fire" and said:
        _fire_words(ship, said, dry=True)
    elif order.verb == "heave a cask overboard" and said:
        _heave_side(ship, said)
    elif order.verb == "exercise the guns":
        _exercise_side(order.verb_phrase, said, strict=True)


# -- the mark and the side -----------------------------------------------------------------


def _side_of(said: str) -> tuple[str | None, str]:
    """('starboard', the words left) for 'the brig to starboard', 'on both sides'."""
    words = said.split()
    for n in (3, 2, 1):
        if len(words) >= n:
            tail = " ".join(words[-n:])
            for lead in ("to the ", "to ", "on the ", "on ", "from the ", "from ", ""):
                if tail.startswith(lead) and tail[len(lead) :] in _SIDES:
                    return _SIDES[tail[len(lead) :]], " ".join(words[:-n]).strip()
    for w in words:
        if w in ("starboard", "larboard", "port"):
            raise OrderError(
                f"Engage her to which side? Say 'engage her to {w}' (the side's guns are "
                f"the ones served) or 'engage her on both sides'."
            )
    return None, said


def _engage(ship: Any, battery: Battery, said: str) -> Result:
    # practice and resupply: a notional mark's words before the side's (`_side_of` refuses
    # a bare 'starboard' among them), and the cask's before the sail's
    notional = _notional_of(ship, said)
    if notional is not None:
        return _engage_notional(ship, battery, notional)
    side, rest = _side_of(said)
    rest = rest.strip()
    if _names_the_cask(ship, rest):
        return _engage_cask(ship, battery, side)
    target_id, words = _mark(ship, rest)
    changed = []
    if target_id != battery.target:
        battery.target = target_id
        battery.target_words = words
        changed.append(f"the mark {words}")
    if side is not None and side != battery.engaged:
        battery.engaged = side
        changed.append(f"the {side} battery" if side != "both" else "both batteries")
    elif side is None and battery.engaged is None:
        raise OrderError(
            f"Engage {words} to which side? Say 'engage her to starboard' or 'to larboard', "
            f"or 'on both sides'."
        )
    if battery.mode is FireMode.HOLD:
        changed.append("the guns to fire as they bear")
        battery.mode = FireMode.AS_THEY_BEAR
    if battery.exercise:
        battery.end_exercise()  # practice and resupply: an engage ends the dumb show
        changed.append("the exercise over")
    if not changed:
        return (
            "guns.engage",
            f"She is engaging {words} to {battery.engaged} already.",
            {"verb": "engage", "level": 1, "target": target_id, "side": battery.engaged},
        )
    text = f"Engage {words} to {battery.engaged}: " + ", ".join(changed) + "."
    if battery.engaged == "both":
        text = f"Engage {words} on both sides: " + ", ".join(changed) + "."
    data = {"verb": "engage", "level": 1, "target": target_id, "side": battery.engaged}
    return "guns.engage", text, data


def _mark(ship: Any, words: str) -> tuple[str, str]:
    """The sail the words name among those in sight: 'her' or nothing is the nearest
    enemy, else the nearest sail; a rig's word, a name or an id otherwise."""
    world = world_of(ship)
    lookout = getattr(world, "lookout", None) if world is not None else None
    if world is None or lookout is None:
        raise OrderError("There is no sail in sight to engage: the ship sails alone.")
    items = list(lookout.strangers(world, float(ship.heading)).get("items") or [])
    if not items:
        raise OrderError("There is no sail in sight to engage.")
    want = words.lower().strip()
    for lead in ("the ", "a "):
        if want.startswith(lead) and want not in _HER:
            want = want[len(lead) :]
    if not want or words.lower() in _HER:
        nations = getattr(world, "nations", None)
        ports = getattr(world, "dealings", None)
        own = getattr(ports, "ship_nation", None)
        enemies = [
            i
            for i in items
            if i.get("nation")
            and own
            and nations is not None
            and nations.at_war(str(i["nation"]), str(own))
        ]
        fired = _fired_on(world)
        enemies += [i for i in items if i.get("id") in fired and i not in enemies]
        pick = enemies[0] if enemies else items[0]
        return str(pick["id"]), _name_of(world, pick)
    for i in items:
        v = world.vessels.get(str(i["id"])) if hasattr(world, "vessels") else None
        names = {str(i["id"]).lower(), str(i.get("known") or "").lower()}
        if v is not None:
            names |= {str(v.name).lower(), str(getattr(v, "kind", "")).lower().removeprefix("a ")}
            names.add(str(getattr(v, "what", "") or "").lower().removeprefix("a "))
        if want in names or any(n and (want in n or n in want) for n in names if len(n) > 2):
            return str(i["id"]), _name_of(world, i)
    seen = ", ".join(_name_of(world, i) for i in items)
    raise OrderError(f"No sail in sight answers to '{words}'; in sight: {seen}.")


def _name_of(world: Any, item: dict[str, Any]) -> str:
    lookout = getattr(world, "lookout", None)
    if lookout is not None:
        try:
            name = lookout.sail_name(f"sail:{item['id']}", "")
            if name:
                return name
        except Exception:  # noqa: BLE001
            pass
    return str(item.get("known") or "the sail")


def _fired_on(world: Any) -> set[str]:
    captain = getattr(world, "captain", None)
    fired = getattr(captain, "fired_on", None) if captain is not None else None
    return set(fired or ())


# -- the standing intentions ---------------------------------------------------------------


def _charge_of(said: str) -> Charge:
    w = said.lower().strip()
    for lead in ("the guns with ", "with ", "the guns ", "them with "):
        if w.startswith(lead):
            w = w[len(lead) :]
    w = w.strip()
    if w in _CHARGES:
        return _CHARGES[w]
    raise OrderError(
        f"Load with what? Say round shot, chain, grape, double (two round shot) or a blank "
        f"cartridge; '{said}' is none of them."
    )


def _load(ship: Any, battery: Battery, said: str) -> Result:
    charge = _charge_of(said) if said else Charge.ROUND
    words = {
        Charge.ROUND: "round shot",
        Charge.CHAIN: "chain shot",
        Charge.GRAPE: "grape",
        Charge.DOUBLE: "double shot",
        Charge.BLANK: "blank cartridge",
    }[charge]
    if charge is battery.charge:
        return (
            "guns.load",
            f"The guns are loading with {words} already.",
            {"verb": "load", "level": 1, "charge": str(charge)},
        )
    battery.charge = charge
    return (
        "guns.load",
        f"Load with {words}: the guns take it from now; a gun loaded keeps its charge "
        f"until it is fired.",
        {"verb": "load", "level": 1, "charge": str(charge)},
    )


def _run_out(ship: Any, battery: Battery, out: bool) -> Result:
    if battery.run_out_wanted == out:
        state = "run out as they are loaded" if out else "kept run in"
        return (
            "guns.run_out",
            f"The guns are {state} already.",
            {"verb": "run out the guns" if out else "run in the guns", "level": 1},
        )
    battery.run_out_wanted = out
    if out:
        text = "Run out: the crews run the guns out as they are loaded."
    else:
        text = (
            "Run in: the guns are kept loaded and run in behind the ports; nothing fires "
            "until they are run out again."
        )
        for g in ship.guns.values():
            if g.kind != "swivel":
                g.run_out = False
    verb = "run out the guns" if out else "run in the guns"
    return "guns.run_out", text, {"verb": verb, "level": 1}


def _aim_of(said: str) -> Aim:
    w = said.lower().strip()
    if w in _AIMS:
        return _AIMS[w]
    if _is_mark_words(w):
        # practice and resupply: `fire at the mark` is an `aim at` synonym
        raise OrderError(
            f"Aim at what? Say her rigging, her hull, or between wind and water; '{said}' is "
            f"none of them; to fire at the mark, say 'engage the mark to starboard' and 'fire'."
        )
    raise OrderError(
        f"Aim at what? Say her rigging, her hull, or between wind and water; '{said}' is "
        f"none of them."
    )


def _aim(ship: Any, battery: Battery, said: str) -> Result:
    aim = _aim_of(said) if said else Aim.HULL
    if aim is battery.aim:
        return (
            "guns.aim",
            f"The guns are laid for {_aim_words(aim)} already.",
            {"verb": "aim at", "level": 1, "aim": str(aim)},
        )
    battery.aim = aim
    return (
        "guns.aim",
        f"Aim at {_aim_words(aim)}: the gun captains lay for it from now.",
        {"verb": "aim at", "level": 1, "aim": str(aim)},
    )


def _aim_words(aim: Aim) -> str:
    words = {
        Aim.HULL: "her hull",
        Aim.RIGGING: "her rigging",
        Aim.BETWEEN: "between wind and water",
    }
    return words[aim]


def _mode(ship: Any, battery: Battery, mode: FireMode) -> Result:
    words = {
        FireMode.AS_THEY_BEAR: "Fire as they bear: each gun as it is loaded and bears.",
        FireMode.BY_DIVISIONS: "Fire by divisions: the forward and the after guns by turns.",
        FireMode.HOLD: "Hold your fire: no gun fires but by name or at the word.",
    }[mode]
    if battery.mode is mode:
        return (
            "guns.mode",
            f"The guns are {'holding their fire' if mode is FireMode.HOLD else f'firing {mode}'} "
            f"already.",
            {"verb": "fire mode", "level": 1, "mode": str(mode)},
        )
    battery.mode = mode
    battery.word = None
    return "guns.mode", words, {"verb": "fire mode", "level": 1, "mode": str(mode)}


def _roll(ship: Any, battery: Battery, phrase: str) -> Result:
    up = "up" in phrase.split()
    down = "down" in phrase.split()
    if not up and not down:
        raise OrderError(
            "Fire on which roll? Say 'fire on the up roll' or 'fire on the down roll'."
        )
    want = "up" if up else "down"
    if battery.roll_doctrine == want:
        return (
            "guns.roll",
            f"The gun captains fire on the {want}-roll already.",
            {"verb": "fire on the roll", "level": 1, "roll": want},
        )
    battery.roll_doctrine = want
    why = "for her rigging" if want == "up" else "for her hull"
    return (
        "guns.roll",
        f"Fire on the {want}-roll ({why}): the gun captains wait for it.",
        {"verb": "fire on the roll", "level": 1, "roll": want},
    )


# -- the one-shot orders -------------------------------------------------------------------


def _fire_words(ship: Any, said: str, dry: bool = False) -> dict[str, Any]:
    """What 'fire ...' names: {} for the word; {'side': ...} for a broadside by side;
    {'guns': [ids]} for a gun by number or place; {'across': True}, {'leeward': True}."""
    w = said.lower().strip()
    for lead in ("the ", "a ", "away "):
        if w.startswith(lead):
            w = w[len(lead) :]
    if not w or w in ("broadside", "all", "away", "the guns", "guns"):
        return {}
    if re.search(r"across\s+(?:her|his|the)\s+bows?", w) or w in ("warning shot", "a warning shot"):
        return {"across": True}
    if "leeward" in w or "to lee" in w or w in ("gun to leeward", "a gun to leeward"):
        return {"leeward": True}
    if "windward" in w or "weather gun" in w:
        return {"leeward": True, "windward": True}
    for name, side in (("starboard", "starboard"), ("larboard", "larboard"), ("port", "larboard")):
        if w in (
            f"{name} broadside",
            f"{name} battery",
            f"{name} guns",
            f"{name} side",
            name,
            f"{name} carronades",
        ):
            return {"side": side}
    if w in ("both broadsides", "both batteries", "both sides"):
        return {"side": "both"}
    guns = _guns_named(ship, w)
    if guns:
        return {"guns": guns}
    raise OrderError(
        f"Fire what? Say 'fire' for the broadside at the word, 'fire the starboard broadside', "
        f"'fire No. 3 gun', 'fire the bow chaser', 'fire the pivot gun', 'fire a shot across "
        f"her bows' or 'fire a gun to leeward'; '{said}' names no gun of hers."
    )


def guns_named(ship: Any, words: str) -> list[str]:
    """The guns the words name ('No. 3 starboard gun', 'the bow chaser', 'the swivels'),
    by id; empty when none (the director's `aboard:` slot and `say as` read it too)."""
    w = " ".join(str(words).lower().split())
    for lead in ("the ", "a "):
        if w.startswith(lead):
            w = w[len(lead) :]
    return _guns_named(ship, w)


def _guns_named(ship: Any, w: str) -> list[str]:
    guns: dict[str, Gun] = getattr(ship, "guns", {}) or {}
    words = w.replace(".", " ").split()
    words = [str(_WORD_NUMBERS.get(x, x)) for x in words]
    w2 = " ".join(words)
    side = None
    for name, s in (("starboard", "starboard"), ("larboard", "larboard"), ("port", "larboard")):
        if name in words:
            side = s
            w2 = " ".join(x for x in words if x != name)
    m = _GUN_NUMBER.match(w2)
    if m:
        n = int(m.group(1))
        out = [
            g.id
            for g in guns.values()
            if g.place == "broadside" and g.number == n and (side is None or g.side == side)
        ]
        return out
    place = None
    # PROVISIONAL (2026-10-25): the pivot gun, the long Tom
    if "pivot" in words or w2 in ("long tom", "tom"):
        return [g.id for g in guns.values() if g.place == "pivot"][:1]
    if "bow" in words or "chaser" in words and "stern" not in words:
        place = "bow"
    if "stern" in words:
        place = "stern"
    if "swivel" in words or "swivels" in words:
        place = "rail"
    if place is not None:
        out = [g.id for g in guns.values() if g.place == place and (side is None or g.side == side)]
        if "chasers" not in words and "swivels" not in words and len(out) > 1 and side is None:
            out = out[:1]  # 'the bow chaser': the first of the pair
        return out
    return []


def _fire(ship: Any, battery: Battery, said: str) -> Result:
    what = _fire_words(ship, said)
    data: dict[str, Any] = {"verb": "fire", "level": 1}
    if what.get("across") or what.get("leeward"):
        # a single gun, the shot to strike nothing: the chaser that bears, else the first
        # gun loaded on the engaged or the lee side
        gun = _a_gun_for_a_signal(
            ship, battery, lee=bool(what.get("leeward")), windward=bool(what.get("windward"))
        )
        battery.serve_by_name(gun.id)
        battery.single.append(gun.id)
        battery.across_bows = bool(what.get("across"))
        if what.get("across"):
            text = f"A shot across her bows: {gun.name} fires as soon as it is ready."
        elif what.get("windward"):
            text = (
                f"A gun to windward: {gun.name} fires as soon as it is ready "
                f"(the signal of defiance)."
            )
        else:
            text = (
                f"A gun to leeward: {gun.name} fires as soon as it is ready (the signal of amity)."
            )
        data.update({"gun": gun.id, "across_bows": bool(what.get("across"))})
        return "guns.fire", text, data
    if what.get("guns"):
        names = []
        for gid in what["guns"]:
            if gid not in battery.single:
                battery.serve_by_name(gid)
                battery.single.append(gid)
            names.append(ship.guns[gid].name)
        data["guns"] = list(what["guns"])
        return "guns.fire", f"{_cap(_and(names))} to fire as soon as ready.", data
    if battery.exercise:
        # practice and resupply: the dumb show fires no gun at the word; a gun by name and
        # the gun to leeward fire as they did
        raise OrderError(
            "The battery is exercising in dumb show: no gun is fired at the word; say "
            "'cease exercising' first."
        )
    side = what.get("side") or battery.engaged
    if side is None:
        raise OrderError(
            "Fire which broadside? No side is engaged: say 'engage her to starboard' first, "
            "or 'fire the starboard broadside'."
        )
    if battery.target is None:
        raise OrderError("Fire at what? No mark is engaged: say 'engage her to starboard' first.")
    battery.word = side
    ready = [
        g
        for g in ship.guns.values()
        if battery.ready(g) and (side == "both" or g.side == side or g.place != "broadside")
    ]
    data.update({"side": side, "ready": len(ready)})
    which = "both broadsides" if side == "both" else f"the {side} broadside"
    if not ready:
        return (
            "guns.fire",
            f"Fire {which}: no gun of it is loaded and run out yet; the word stands until "
            f"one bears.",
            data,
        )
    return "guns.fire", f"Fire {which}: {len(ready)} guns ready to go together as they bear.", data


def _a_gun_for_a_signal(ship: Any, battery: Battery, lee: bool, windward: bool) -> Gun:
    guns = [g for g in ship.guns.values() if g.serves and g.cast_loose]
    if not guns:
        guns = [g for g in ship.guns.values() if g.serves]
    if not guns:
        raise OrderError("She has no gun that can be fired.")
    heel = float(getattr(ship.dyn, "heel", 0.0))
    lee_side = "starboard" if heel > 0.0 else "larboard"
    if windward:
        lee_side = "larboard" if lee_side == "starboard" else "starboard"
    chasers = [g for g in guns if g.place in ("bow", "stern")]
    if chasers and not lee:
        return chasers[0]
    on_side = [g for g in guns if g.side == lee_side] if lee else guns
    pool = on_side or guns
    loaded = [g for g in pool if battery.ready(g)]
    return (loaded or pool)[0]


def _priority(ship: Any, quarters: Any, verb: str) -> Result:
    """The fighting book's priority (spec M7 §8a): under `sail before guns` sail work short
    of hands takes them from the guns by the bill; under `guns before sail` nothing is lent
    and the sail work waits or goes short with the trimmers alone."""
    if quarters.priority == verb:
        return (
            "guns.priority",
            f"The bill stands at {verb} already.",
            {"verb": verb, "level": 1, "priority": verb},
        )
    quarters.priority = verb
    words = (
        "the sail work takes its hands from the guns as it needs them, and the guns go short"
        if verb == "sail before guns"
        else "the guns keep their crews, and sail work has the trimmers alone"
    )
    return (
        "guns.priority",
        f"{verb.capitalize()}: {words}.",
        {"verb": verb, "level": 1, "priority": verb},
    )


def _cease(ship: Any, battery: Battery) -> Result:
    was = battery.mode
    battery.mode = FireMode.HOLD
    battery.word = None
    battery.single = []
    battery.across_bows = False
    if was is FireMode.HOLD:
        return (
            "guns.cease",
            "The guns are silent already.",
            {"verb": "cease firing", "level": 1},
        )
    return (
        "guns.cease",
        "Cease firing: the guns are loaded and run out and no gun fires but at the word.",
        {"verb": "cease firing", "level": 1},
    )


def _strike(ship: Any, battery: Battery, said: str) -> Result:
    if said and not any(w in said for w in ("colour", "flag", "ensign")):
        raise OrderError(
            f"Strike what? 'Strike the colours' hauls down the ensign; the topmasts are "
            f"'strike the topmasts'; '{said}' is neither."
        )
    if ship.extra.get("struck"):
        return (
            "action.struck",
            "The colours are struck already.",
            {"verb": "strike the colours", "level": 1},
        )
    world = world_of(ship)
    from freesail.combat.action import strike

    if world is not None:
        strike(world, by_rule=False, words="by the captain's order")
    else:
        ship.extra["struck"] = True
        from freesail.world.signals import locker_of, set_colours

        set_colours(locker_of(ship).colours, None, "struck", "", 0)
        battery.mode = FireMode.HOLD
    enemy = battery.target_words or "the enemy"
    text = (
        f"The colours are struck: the ensign comes down and the guns fall silent; she lies to "
        f"for {enemy}. What follows (the prize crew, the prisoners, the captive's channel) is "
        f"not in this game yet."
    )
    return "action.struck", text, {"verb": "strike the colours", "level": 1, "by_rule": False}


# -- practice at the great guns (practice and resupply, between packages 72 and 73) --------

# A notional mark's words, read before the side's: 'a mark four cables on the starboard
# beam', 'the notional mark 2 cables off the larboard quarter'.
_NOTIONAL = re.compile(
    r"^(?:a|the)\s+(?:notional\s+)?mark\s+(.+?)\s+cables?\s+(?:on|off|broad on)\s+the\s+"
    r"(starboard|larboard|port)\s+(bow|beam|quarter)$"
)
# Where a notional mark lies from her head (judgement): four points on the bow, eight on
# the beam, twelve on the quarter.
_NOTIONAL_DEG = {"bow": 45.0, "beam": 90.0, "quarter": 135.0}
# The words that name the mark for practice (`aim at`'s refusal, and the cask's engage).
_MARK_WORDS = frozenset({"mark", "the mark", "a mark", "cask", "the cask", "the target", "target"})
_CASK_ONLY = frozenset({"cask", "the cask", "a cask"})
_MARK_OR_CASK = frozenset({"mark", "the mark", "target", "the target"})
# The words a heave may be given with beside its side.
_HEAVE_FILLER = frozenset(
    {"from", "the", "over", "off", "quarter", "side", "for", "a", "mark", "to", "on", "of"}
)
# The words an exercise may be given with beside its side.
_EXERCISE_FILLER = frozenset(
    {"the", "guns", "great", "battery", "batteries", "side", "sides", "to", "on", "in"}
    | {"dumb", "show", "at", "a", "both", "starboard", "larboard", "port"}
)
_FIRE_WORDS = {
    FireMode.AS_THEY_BEAR: "the guns to fire as they bear",
    FireMode.BY_DIVISIONS: "the guns to fire by divisions",
    FireMode.AT_THE_WORD: "the guns to fire at the word",
    FireMode.HOLD: "the guns holding their fire",
}
# The notional mark the refusals suggest is laid on the beam at four cables, or at the
# whole cables her longest random shot reaches when that is less (`_example`).
EXAMPLE_CABLES = 4


def _is_mark_words(w: str) -> bool:
    return w in _MARK_WORDS or w.startswith(("the mark ", "a mark "))


def _names_the_cask(ship: Any, words: str) -> bool:
    """'the cask' always names the cask; 'the mark' and 'the target' only while one is in
    the water, and a sail otherwise (decision 22: a rules captain's 'her' never picks a
    cask)."""
    w = " ".join(words.lower().split())
    if w in _CASK_ONLY:
        return True
    return w in _MARK_OR_CASK and marks.cask_in_water(ship) is not None


def _cables_words(n: float) -> str:
    """'four cables', 'one cable', 'two and a half cables', '2.3 cables'."""
    whole = int(n)
    if abs(n - whole) < 1e-9:
        return f"{number_words(whole)} cable{'' if whole == 1 else 's'}"
    if abs(n - whole - 0.5) < 1e-9 and whole >= 1:
        return f"{number_words(whole)} and a half cables"
    return f"{n:g} cables"


def _kinds_of(ship: Any, guns: list[Gun] | None = None) -> dict[str, float]:
    """Her guns' kinds in the deck's words, plural, with each one's random shot in metres,
    the longest first: of all her guns, or of `guns`."""
    reach: dict[str, float] = {}
    every = getattr(ship, "guns", {}).values() if guns is None else guns
    for g in every:
        words = f"{g.kind_words}s"
        if words not in reach:
            reach[words] = S.ballistics_of(g.kind, g.pounder).random_m
    return dict(sorted(reach.items(), key=lambda kv: -kv[1]))


def _example(ship: Any, side: str = "starboard") -> str:
    """The notional mark the refusals suggest: on the beam, where the broadside bears, at
    four cables, or at the whole cables her longest random shot reaches when that is less
    (the King's cutter's 12-pounder carronades throw 3.95 cables: three), and never nearer
    than the cable a mark is laid at."""
    reach = _kinds_of(ship)
    longest = max(reach.values(), default=EXAMPLE_CABLES * units.CABLE)
    n = max(1, min(EXAMPLE_CABLES, int(longest / units.CABLE + 1e-9)))
    return f"engage a mark {_cables_words(float(n))} on the {side} beam"


def _guns_bearing(ship: Any, relative_deg: float) -> list[Gun]:
    """Her guns that can bear on a notional mark at this bearing from her head, which it
    keeps as she turns: each gun by its arc (`Battery.bears`), and a pivot gun by its arc
    over either side alone, being trained round to the mark (`Battery._train_pivots`)."""
    battery = (getattr(ship, "extra", None) or {}).get("battery")
    if not isinstance(battery, Battery):
        battery = Battery(ship)  # a stand-in kept nowhere: the arcs are the guns' own
    rad = math.radians(relative_deg)
    bearing = []
    for g in getattr(ship, "guns", {}).values():
        if g.place == "pivot":
            lo, hi = pivot_arc(g)
            if lo <= abs(relative_deg) <= hi:
                bearing.append(g)
        elif battery.bears(g, rad):
            bearing.append(g)
    return bearing


def _notional_of(ship: Any, said: str) -> tuple[float, float, str, str, list[str]] | None:
    """A notional mark's words read: (degrees from her head, starboard positive; the range
    in metres; the side; the mark's words; her guns' kinds that do not carry so far), or
    None when the words are not a notional mark's. The mark keeps its bearing from her
    head, so some gun must bear on it there (no broadside gun bears on the bow or the
    quarter, nor a chaser; a swivel or a pivot may). The range runs from a cable to the
    longest random shot of the guns that bear (`Battery._fire` fires no gun beyond its
    own)."""
    m = _NOTIONAL.match(" ".join(said.lower().split()))
    if m is None:
        return None
    n, rest = numbers.number_in(m.group(1))
    if n is None or rest.strip():
        raise OrderError(
            f"A mark how many cables off? Say '{_example(ship)}'; '{m.group(1)}' is no "
            f"number of cables."
        )
    side = "starboard" if m.group(2) == "starboard" else "larboard"
    point = m.group(3)
    relative = _NOTIONAL_DEG[point] * (1.0 if side == "starboard" else -1.0)
    range_m = float(n) * units.CABLE
    cables = _cables_words(float(n))
    every = _kinds_of(ship)
    if not every:
        raise OrderError("She carries no guns.")
    bearing = _guns_bearing(ship, relative)
    if not bearing:
        # practice and resupply (from the review): a mark no gun can ever bear on is
        # refused, since no shot would be fired at it (the words are judgement)
        beam = f"engage a mark {cables} on the {side} beam"
        within = units.CABLE - 1e-6 <= range_m <= max(every.values()) + 1e-6
        raise OrderError(
            f"No gun of hers bears on the {side} {point}, and a notional mark keeps its "
            f"bearing from her head as she turns: say '{beam if within else _example(ship, side)}'."
        )
    if range_m < units.CABLE - 1e-6:
        raise OrderError(
            f"A notional mark is laid no nearer than a cable: say 'engage a mark one cable on "
            f"the {side} {point}' or further off."
        )
    reach = _kinds_of(ship, bearing)
    longest_words, longest = next(iter(reach.items()))
    if range_m > longest + 1e-6:
        said_cables = longest / units.CABLE
        figure = f"{said_cables:.1f}"
        if round(said_cables, 1) >= float(n):
            figure = f"{said_cables:.2f}"  # 3.95 is not "4.0" against four cables asked
        # her longest gun names itself; a shorter one is named as the longest that bears
        that = "" if longest_words == next(iter(every)) else f" that bears on the {side} {point}"
        raise OrderError(
            f"No gun of hers{that} carries {cables}: her {longest_words}' random shot is "
            f"{figure} cables."
        )
    short = [words for words, r in reach.items() if r < range_m]
    words = f"the mark {cables} on the {side} {point}"
    return relative, range_m, side, words, short


def _engage_notional(
    ship: Any, battery: Battery, notional: tuple[float, float, str, str, list[str]]
) -> Result:
    relative, range_m, side, words, short = notional
    world = world_of(ship)
    marks.lay_notional(world if world is not None else _ShipAlone(ship), relative, range_m, words)
    cables = words.removeprefix("the mark ").split(" on the ")[0]
    extra = f"; her {_and(short)} do not carry {cables}" if short else ""
    return _engage_mark(ship, battery, marks.NOTIONAL_ID, words, side, extra, say_side=False)


class _ShipAlone:
    """A ship with no World, for `marks.lay_notional` (which reads `world.ship` alone)."""

    def __init__(self, ship: Any) -> None:
        self.ship = ship


def _engage_cask(ship: Any, battery: Battery, side: str | None) -> Result:
    p = marks.practice_of(ship)
    cask = p.cask if p is not None else None
    if cask is not None and cask.gone == "struck":
        raise OrderError("The mark is knocked to pieces: heave another cask overboard for a mark.")
    if cask is None or cask.gone:
        raise OrderError(
            "There is no cask in the water: say 'heave a cask overboard' first, or "
            f"'{_example(ship)}'."
        )
    world = world_of(ship)
    if world is None or not marks.cask_in_sight(world, cask):
        raise OrderError("The mark is not in sight from the masthead.")
    if side is None and battery.engaged is None:
        raise OrderError(
            "Engage the cask to which side? Say 'engage the cask to starboard' or 'to "
            "larboard', or 'on both sides'."
        )
    return _engage_mark(ship, battery, cask.id, "the cask", side, "")


def _engage_mark(
    ship: Any,
    battery: Battery,
    target_id: str,
    words: str,
    side: str | None,
    extra: str,
    say_side: bool = True,
) -> Result:
    """The battery laid for a mark: the mark and the side, the guns to fire as they bear
    when they were holding, and the dumb show over; the answer says the battery's state."""
    exercising = battery.exercise is not None
    already = (
        battery.target == target_id
        and battery.target_words == words
        and (side is None or side == battery.engaged)
        and battery.mode is not FireMode.HOLD
        and not exercising
    )
    battery.target = target_id
    battery.target_words = words
    if side is not None:
        battery.engaged = side
    if battery.mode is FireMode.HOLD:
        battery.mode = FireMode.AS_THEY_BEAR
    if exercising:
        battery.end_exercise()
    engaged = battery.engaged or "both"
    data = {
        "verb": "engage",
        "level": 1,
        "target": target_id,
        "side": engaged,
        "mark": "notional" if target_id == marks.NOTIONAL_ID else "cask",
    }
    where = "on both sides" if engaged == "both" else f"to {engaged}"
    if already:
        return "guns.engage", f"She is engaging {words} {where} already.", data
    battery_words = "both batteries" if engaged == "both" else f"the {engaged} battery"
    parts = [battery_words, _FIRE_WORDS[battery.mode]]
    if exercising:
        parts.append("the exercise over")
    head = f"Engage {words} {where}" if say_side else f"Engage {words}"
    return "guns.engage", f"{head}: " + ", ".join(parts) + extra + ".", data


def _exercise_side(phrase: str, said: str, strict: bool = False) -> str | None:
    """The side the exercise names in its verb's words and after them: 'starboard',
    'larboard', 'both', or None for none said. `strict` (a standing order read whole)
    refuses words that are neither a side nor the dumb show's."""
    words = f"{phrase} {said}".lower().replace(",", " ").split()
    side = None
    if "both" in words:
        side = "both"
    elif "starboard" in words:
        side = "starboard"
    elif "larboard" in words or "port" in words:
        side = "larboard"
    if strict and said:
        if any(w not in _EXERCISE_FILLER for w in said.lower().replace(",", " ").split()):
            raise OrderError(
                "Exercise which guns? Say 'exercise the guns', 'exercise the starboard "
                f"battery' or 'exercise both batteries'; '{said}' is none of them."
            )
    return side


def _exercise(ship: Any, battery: Battery, phrase: str, said: str) -> Result:
    """The guns exercised in dumb show (`Battery.begin_exercise`): allowed at quarters
    before the guns are cast loose, so that the cycle begins empty (decision 21); never
    while a sail is engaged."""
    if battery.target and not marks.is_mark(battery.target):
        raise OrderError(
            f"She is engaged with {battery.target_words or 'the enemy'}; the guns are not "
            f"exercised in dumb show while an enemy is engaged."
        )
    side = _exercise_side(phrase, said) or battery.engaged or "both"
    which = "both batteries" if side == "both" else f"the {side} battery"
    data: dict[str, Any] = {"verb": "exercise the guns", "level": 1, "side": side}
    if battery.exercise == side:
        verb = "are" if side == "both" else "is"
        return "guns.exercise", f"{_cap(which)} {verb} exercising in dumb show already.", data
    loaded = list(battery.begin_exercise(side) or [])
    text = (
        f"Exercise {which} in dumb show: the guns served without powder, and no shot leaves "
        "the ship"
    )
    if len(loaded) == 1:
        text += "; the one gun loaded keeps its charge and is run out and pointed only"
    elif loaded:
        text += (
            f"; the {len(loaded)} guns loaded keep their charges and are run out and pointed only"
        )
    text += "."
    if not any(g.cast_loose for g in ship.guns.values() if g.serves):
        text += " The guns are not yet cast loose: say 'cast loose the guns'."
    data["loaded"] = loaded
    return "guns.exercise", text, data


def _cease_exercise(ship: Any, battery: Battery) -> Result:
    data = {"verb": "cease exercising", "level": 1}
    if not battery.exercise:
        return "guns.exercise", "The guns are not being exercised.", data
    battery.end_exercise()
    return (
        "guns.exercise",
        "Cease exercising: the dumb show is over; the empty guns are left run in and "
        "unprimed, and a loaded gun keeps its charge.",
        data,
    )


def _heave_side(ship: Any, said: str) -> str:
    """The quarter the cask goes over from: the one named, else the lee one by her heel
    (positive to starboard), as the log is hove from the lee quarter."""
    heel = float(getattr(getattr(ship, "dyn", None), "heel", 0.0) or 0.0)
    lee = "starboard" if heel > 0.0 else "larboard"
    weather = "larboard" if lee == "starboard" else "starboard"
    words = said.lower().replace(",", " ").split()
    for w in words:
        if w == "starboard":
            return "starboard"
        if w in ("larboard", "port"):
            return "larboard"
        if w in ("lee", "leeward"):
            return lee
        if w in ("weather", "windward"):
            return weather
    if any(w not in _HEAVE_FILLER for w in words):
        raise OrderError(
            "Heave it over from which quarter? Say 'heave a cask overboard from the starboard "
            "quarter', or name none for the lee quarter."
        )
    return lee


def _heave(ship: Any, battery: Battery, said: str) -> Result:
    """`heave a cask overboard`: two hands at the quarter for a minute (`heave_mark`, the
    runner's, holding nothing of the ship's), the cask still in the water given up. Refused
    with no chart (nothing could see it) and by night (the masthead would not)."""
    world = world_of(ship)
    if (
        world is None
        or getattr(world, "lookout", None) is None
        or getattr(world, "position", None) is None
    ):
        raise OrderError(
            "The ship sails alone, with no chart: a cask over the side could not be seen. "
            f"Say '{_example(ship)}'."
        )
    if str(world.daylight) == "night":
        raise OrderError(
            "It is dark: a cask over the side would not be seen from the masthead; a "
            f"notional mark serves by night ('{_example(ship)}')."
        )
    side = _heave_side(ship, said)
    data = {"verb": "heave a cask overboard", "level": 1, "side": side}
    runner = (getattr(ship, "extra", None) or {}).get("evolutions")
    if runner is None or not hasattr(runner, "instances"):
        marks.drop_cask(world, side)
        return (
            "evolution.started",
            f"The mark is over the side from the {side} quarter, an empty cask with a flag on "
            "a staff.",
            data,
        )
    line = runner.start(ship, "heave_mark", "her", {"side": side})
    marks.abandon(world, battery)
    return "evolution.started", line, data


def _levels(ship: Any, mag: Any) -> dict[tuple[str, float], int]:
    """The fit's filled allowance by kind and calibre: the magazine's own (`level`), else
    the fit's (`fit_levels`)."""
    level = getattr(mag, "level", None)
    if isinstance(level, dict) and level:
        return {(str(k[0]), float(k[1])): int(n) for k, n in level.items()}
    return fit_levels(getattr(ship, "fit_spec", None))


def _kind_words(ship: Any, kind: str, pounder: float) -> str:
    """'12-pounder carronades', 'long 18-pounders', 'long 12-pounder' for the one gun: the
    guns of a kind and calibre, counted on her deck (`parts.gun_words`; the review's
    finding: the privateer's one pivot gun was 'the long 12-pounders'), more where she
    carries none."""
    n = sum(
        1
        for g in getattr(ship, "guns", {}).values()
        if g.kind == kind and float(g.pounder) == float(pounder)
    )
    return gun_words(kind, pounder, n or 2)


def _barrels_words(lb: float) -> str:
    """'2 barrels below', '1 barrel and 31 pounds below', 'no powder below'."""
    whole = int(max(0.0, lb) // BARREL_LB)
    rest = int(round(max(0.0, lb) - whole * BARREL_LB))
    if rest >= int(BARREL_LB):
        whole, rest = whole + 1, 0
    parts = []
    if whole:
        parts.append(f"{whole} barrel{'' if whole == 1 else 's'}")
    if rest:
        parts.append(f"{rest} pound{'' if rest == 1 else 's'}")
    return (" and ".join(parts) + " below") if parts else "no powder below"


def _fill(ship: Any, fill: bool) -> Result:
    """`fill cartridges` and `cease filling`: the gunner's filling let go or held (the
    magazine's `filling_held`, which the filling reads); `fill cartridges` asks him to
    report the cartridges filled to the allowance (`report_filled`)."""
    mag = magazine(ship)
    levels = _levels(ship, mag)
    order = sorted(levels, key=lambda k: (kind_rank(k[0]), -k[1]))
    filled = {k: mag.filled_of(k[0], k[1]) for k in order}
    short = [k for k in order if filled[k] < levels[k]]
    powder = float(getattr(mag, "powder_lb", 0.0) or 0.0)
    can = [k for k in short if powder >= mag.charge_of(k[0], k[1])]
    below = _barrels_words(powder)
    verb = "fill cartridges" if fill else "cease filling"
    data: dict[str, Any] = {
        "verb": verb,
        "level": 1,
        "short": len(short),
        "powder_lb": round(powder, 1),
    }
    if not fill:
        in_hand = bool(can) and not mag.filling_held
        mag.filling_held = True
        if not in_hand:
            return "guns.fill_order", "The gunner is not filling.", data
        return (
            "guns.fill_order",
            "The gunner fills no more cartridges until he is ordered; the magazine shut.",
            data,
        )
    mag.filling_held = False
    if not short:
        each = ", ".join(f"{filled[k]} for the {_kind_words(ship, *k)}" for k in order)
        return (
            "guns.fill_order",
            f"The cartridges are filled to the allowance already: {each}; {below}.",
            data,
        )
    if not can:
        if powder > 1e-9:
            # some powder below, under every short kind's charge: said so, with what is
            # there, as the magazine's reading and the gunner's report say it (the review's
            # finding: 3 pounds below was "no powder below")
            return (
                "guns.fill_order",
                f"The powder below is too little to fill another cartridge: {below}; the "
                "filled cartridges are all she has.",
                data,
            )
        return (
            "guns.fill_order",
            "There is no powder below to fill: the filled cartridges are all she has.",
            data,
        )
    mag.report_filled = True
    each = ", ".join(f"{filled[k]} of {levels[k]} for the {_kind_words(ship, *k)}" for k in short)
    return (
        "guns.fill_order",
        f"The gunner fills cartridges from the powder below: {each}, {below}; by day, and at "
        "quarters with a man of the powder to spare.",
        data,
    )


# -- words ---------------------------------------------------------------------------------


def _and(items: list[str]) -> str:
    if len(items) <= 1:
        return "".join(items)
    return ", ".join(items[:-1]) + " and " + items[-1]


def _cap(s: str) -> str:
    return s[:1].upper() + s[1:]


def range_cables(m: float) -> str:
    return f"{m / units.CABLE:.1f} cables" if hasattr(units, "CABLE") else f"{m:.0f} m"
