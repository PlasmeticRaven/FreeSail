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

The guns' cycle itself is no order's: it runs in `combat.guns.Battery` while hands and
powder last (item 1's design: a standing intention, logged when it changes something). The
hands come from the quarter bill (`crew.quarters`): the orders here are refused in words
until the hands are at quarters (`beat to quarters`, or `clear for action`), and `cast
loose the guns` has the crews cast them loose. The boarders are 73's (the vocabulary
refuses them in words). A gun's number is the pair's (No. 3 is the third pair from
forward, either side); a place is the bow chaser, the stern chaser or a swivel.
"""

from __future__ import annotations

import re
from typing import Any

from freesail import units
from freesail.combat.guns import Aim, Battery, FireMode, battery_of
from freesail.crew.quarters import quarters_of
from freesail.orders.errors import OrderError
from freesail.orders.grammar import Order
from freesail.orders.prompt import world_of
from freesail.ship.parts import Charge, Gun

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
        _side_of(said)  # the side's words; the mark is the moment's
    elif order.verb == "fire" and said:
        _fire_words(ship, said, dry=True)


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
    side, rest = _side_of(said)
    rest = rest.strip()
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
        ports = getattr(world, "ports", None)
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
        f"'fire No. 3 gun', 'fire the bow chaser', 'fire a shot across her bows' or 'fire a "
        f"gun to leeward'; '{said}' names no gun of hers."
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
                battery.single.append(gid)
            names.append(ship.guns[gid].name)
        data["guns"] = list(what["guns"])
        return "guns.fire", f"{_cap(_and(names))} to fire as soon as ready.", data
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
        ship.extra["colours"] = "struck"
        battery.mode = FireMode.HOLD
    enemy = battery.target_words or "the enemy"
    text = (
        f"The colours are struck: the ensign comes down and the guns fall silent; she lies to "
        f"for {enemy}. What follows (the prize crew, the prisoners, the captive's channel) is "
        f"not in this game yet."
    )
    return "action.struck", text, {"verb": "strike the colours", "level": 1, "by_rule": False}


# -- words ---------------------------------------------------------------------------------


def _and(items: list[str]) -> str:
    if len(items) <= 1:
        return "".join(items)
    return ", ".join(items[:-1]) + " and " + items[-1]


def _cap(s: str) -> str:
    return s[:1].upper() + s[1:]


def range_cables(m: float) -> str:
    return f"{m / units.CABLE:.1f} cables" if hasattr(units, "CABLE") else f"{m:.0f} m"
