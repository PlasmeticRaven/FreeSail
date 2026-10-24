"""The action's readings and events (spec M7 §8a, §9, §10; package 70), registered in the
readings registry (`api.readings.REGISTRY`, `EVENTS`) from this module, which `readings`
imports at its end.

The rows, each a state in words the dialect compares by `is <words>` and `is not <words>`
(the kind `state`, as the ground is compared) and a station reads in its sample:

    the guns          the battery: cast loose or secured, how many loaded, run out and
                      primed, the side engaged, the charge, the aim and the firing's
                      doctrine, the guns dismounted ('is cast loose', 'is not engaged')
    the damage        what the carpenter and the boatswain report: the spars and lines
                      shot away, the sails holed, the shot holes and where, the helm
                      ('is none', 'is not none')
    the bill          the butcher's bill and the hands' temper: the killed and wounded of
                      the complement, the figure's words ('is steady', 'is wavering')
    the magazine      the cartridges and shot by calibre, as the gunner counts them
    the enemy         the mark engaged, in the lookout's words, with her bearing and her
                      colours as made out, and 'struck' when they are down
    the range         the range of the mark by the lookout's estimate, in cables (a
                      distance: 'is under 3 cables', 'exceeds half a mile')
    the colours       the ship's own: 'flying' or 'struck' ('when the colours are struck')
    the quarter bill  the bill as beaten: each division and each gun's crew, or 'not at
                      quarters'

The events, for `at` and a stand-by: `she opens fire` (`action.fired_at`), `a warning
shot` (`action.warning_shot`), `a shot strikes` (`action.hit`), `a man killed`, `a hand
hurt`, `a gun dismounted`, `a spar shot away` (the hit's kinds), `her colours come down`
and `the enemy strikes` (`action.enemy_struck`), `the colours struck` (`action.struck`),
`quarters` (the beat, `crew.quarters`), `cleared for action` (`ship.cleared`), `the guns cast
loose`, `the guns secured`, `the magazine empty`, `a broadside fired` (`action.fired`).
"""

from __future__ import annotations

from typing import Any

from freesail import units
from freesail.api import readings as R
from freesail.crew.model import number_words

__all__ = ["ACTION_ROWS", "CABLE_M", "idle_rows", "register"]

# The action's rows a sample carries only while something is afoot (the brief's item 8: the
# samples kept small enough that a model's thinking does not cost it a broadside): at
# quarters, or damaged, or with men hurt, or a mark engaged, or the colours struck, the row
# rides; idle, it is left out, and its first appearance is itself the delta.
ACTION_ROWS: tuple[str, ...] = (
    "damage",
    "bill",
    "magazine",
    "enemy",
    "range",
    "colours",
    "quarter_bill",
)


def idle_rows(world: Any) -> set[str]:
    """The action's rows to leave out of a sample now: all of them while she is not at
    quarters, undamaged, nobody hurt, no mark engaged and the colours flying; `guns` always
    rides (one line)."""
    ship = getattr(world, "ship", None)
    if ship is None:
        return set(ACTION_ROWS)
    extra = getattr(ship, "extra", None) or {}
    q = extra.get("quarters")
    if q is not None and getattr(q, "at_quarters", False):
        return set()
    if extra.get("struck"):
        return set()
    battery = extra.get("battery")
    if battery is not None and getattr(battery, "target", None):
        return set()
    keeper = extra.get("damage")
    if keeper is not None and (keeper.hits or keeper.holes):
        return set()
    crew = extra.get("crew")
    if crew is not None and any(s.hurt for s in crew.sailors):
        return set()
    return set(ACTION_ROWS)


CABLE_M = units.NAUTICAL_MILE / 10.0  # the cable of a tenth of a mile (608 feet)


# -- the rows ------------------------------------------------------------------------------


def _battery(world: Any) -> Any:
    ship = getattr(world, "ship", None)
    extra = getattr(ship, "extra", None)
    if extra is None or not getattr(ship, "guns", None):
        return None
    from freesail.combat.guns import battery_of

    return battery_of(ship)


def _quarters(world: Any) -> Any:
    ship = getattr(world, "ship", None)
    if ship is None or not getattr(ship, "guns", None):
        return None
    from freesail.crew.quarters import quarters_of

    return quarters_of(ship)


def _no_guns_words(world: Any) -> str | None:
    ship = getattr(world, "ship", None)
    if ship is not None and not getattr(ship, "guns", None):
        return "she carries no guns"
    return None


def _guns(world: Any, _: str | None) -> dict[str, Any] | None:
    battery = _battery(world)
    if battery is None:
        return None
    ship = world.ship
    guns = list(ship.guns.values())
    serving = [g for g in guns if g.serves]
    loaded = sum(1 for g in serving if g.loaded)
    run_out = sum(1 for g in serving if g.run_out or (g.kind == "swivel" and g.loaded))
    primed = sum(1 for g in serving if g.primed)
    dismounted = [g for g in guns if g.dismounted]
    cast = any(g.cast_loose for g in serving)
    kinds = _kinds_words(guns)
    parts = [kinds, "cast loose" if cast else "secured"]
    if cast:
        parts.append(f"{loaded} loaded, {run_out} run out, {primed} primed")
        if battery.engaged:
            side = "both sides" if battery.engaged == "both" else f"the {battery.engaged} side"
            at = f" at {battery.target_words}" if battery.target_words else ""
            parts.append(f"engaged on {side}{at}")
        else:
            parts.append("not engaged")
        parts.append(f"loading with {_charge_words(battery.charge)}")
        parts.append(f"laid for {_aim_words(battery.aim)}")
        mode = str(battery.mode)
        parts.append("holding fire" if mode == "hold" else f"firing {mode}")
        if battery.roll_doctrine:
            parts.append(f"on the {battery.roll_doctrine}-roll")
    if dismounted:
        names = _and([g.name for g in dismounted])
        parts.append(f"{number_words(len(dismounted))} dismounted ({names})")
    return {
        "words": "; ".join(parts),
        "count": len(serving),
        "cast_loose": cast,
        "loaded": loaded,
        "run_out": run_out,
        "primed": primed,
        "engaged": battery.engaged,
        "target": battery.target,
        "charge": str(battery.charge),
        "aim": str(battery.aim),
        "mode": str(battery.mode),
        "dismounted": [g.id for g in dismounted],
        "rounds_fired": battery.rounds_fired,
    }


def _kinds_words(guns: list[Any]) -> str:
    counts: dict[str, int] = {}
    for g in guns:
        if not g.serves and not g.dismounted:
            continue
        counts[g.kind_words] = counts.get(g.kind_words, 0) + 1
    return ", ".join(f"{n} {k}{'s' if n != 1 else ''}" for k, n in counts.items()) or "no guns"


def _charge_words(charge: Any) -> str:
    return {
        "round": "round shot",
        "chain": "chain shot",
        "grape": "grape",
        "double": "double shot",
        "blank": "blank cartridge",
    }.get(str(charge), str(charge))


def _aim_words(aim: Any) -> str:
    return {"hull": "her hull", "rigging": "her rigging"}.get(str(aim), str(aim))


def _damage(world: Any, _: str | None) -> dict[str, Any] | None:
    ship = getattr(world, "ship", None)
    if ship is None:
        return None
    from freesail.combat.hits import damage_of

    keeper = damage_of(ship)
    items: list[str] = []
    # a point ship (the readings' tests) has no part graph: undamaged
    spars = [s for s in (getattr(ship, "spars", None) or {}).values() if s.wrecked]
    if spars:
        items.append(f"{_and([_part_name(ship, s.id) for s in spars])} carried away")
    lines = [
        ln
        for ln in (getattr(ship, "lines", None) or {}).values()
        if getattr(ln.state, "value", ln.state) == "parted"
    ]
    if lines:
        items.append(f"{number_words(len(lines))} line{'s' if len(lines) != 1 else ''} parted")
    sails = (getattr(ship, "sails", None) or {}).values()
    holed = [s for s in sails if getattr(s, "holed_m2", 0.0) > 0.0]
    if holed:
        items.append(f"{_and([_part_name(ship, s.id) for s in holed])} holed")
    holes = list(keeper.holes) if keeper is not None else []
    if holes:
        below = sum(1 for h in holes if float(h.get("z_m", 1.0)) <= 0.0)
        words = f"{number_words(len(holes))} shot hole{'s' if len(holes) != 1 else ''} in the side"
        if below:
            words += f", {number_words(below)} at or below the waterline"
        items.append(words)
    dismounted = [g for g in getattr(ship, "guns", {}).values() if g.dismounted]
    if dismounted:
        items.append(f"{_and([g.name for g in dismounted])} dismounted")
    extra = getattr(ship, "extra", None) or {}
    if extra.get("helm_lost"):
        items.append("the helm shot away")
    if extra.get("boats_stove"):
        items.append("a boat stove")
    words = "; ".join(items) if items else "none"
    return {
        "words": words,
        "count": len(items),
        "spars": [s.id for s in spars],
        "lines": [ln.id for ln in lines],
        "sails_holed": [s.id for s in holed],
        "holes": holes,
        "dismounted": [g.id for g in dismounted],
        "helm_lost": bool(extra.get("helm_lost")),
        "hits": keeper.hits if keeper is not None else 0,
    }


def _part_name(ship: Any, pid: str) -> str:
    try:
        from freesail.orders.resolve import display_name

        return f"the {display_name(ship, pid)}"
    except Exception:  # noqa: BLE001
        return pid


def _bill(world: Any, _: str | None) -> dict[str, Any] | None:
    ship = getattr(world, "ship", None)
    crew = getattr(ship, "extra", {}).get("crew") if ship is not None else None
    if crew is None:
        return None
    killed = [s for s in crew.sailors if s.hurt == "killed"]
    wounded = [s for s in crew.sailors if s.hurt and s.hurt != "killed"]
    complement = len(crew.sailors)
    morale = ship.extra.get("morale")
    temper = morale.words if morale is not None else "steady"
    if not killed and not wounded:
        words = f"nobody hurt of {complement}; the hands {temper}"
    else:
        said = []
        if killed:
            said.append(f"{number_words(len(killed))} killed")
        if wounded:
            said.append(f"{number_words(len(wounded))} wounded")
        words = f"{' and '.join(said)} of {complement}; the hands {temper}"
    return {
        "words": words,
        "killed": len(killed),
        "wounded": len(wounded),
        "complement": complement,
        "fit": sum(1 for s in crew.sailors if s.fit),
        "temper": temper,
        "morale": round(float(morale.value), 2) if morale is not None else None,
        "names": [(s.name, s.hurt) for s in killed + wounded],
    }


def _magazine(world: Any, _: str | None) -> dict[str, Any] | None:
    ship = getattr(world, "ship", None)
    if ship is None or not getattr(ship, "guns", None):
        return None
    from freesail.ship.parts import magazine

    mag = magazine(ship)
    lines = mag.describe()
    return {"words": " ".join(lines) if lines else "empty", "lines": lines}


def _enemy(world: Any, _: str | None) -> dict[str, Any] | None:
    battery = _battery(world)
    if battery is None or battery.target is None:
        return {"words": "none engaged", "id": None, "struck": False}
    from freesail.combat.action import target_of

    t = target_of(world, battery.target)
    words = battery.target_words or "the mark"
    struck = False
    vessel = None
    sea = getattr(world, "vessels", None)
    if sea is not None:
        vessel = sea.get(battery.target)
        if vessel is None and battery.target == "the ship":
            parent = getattr(world, "parent", None)
            vessel = parent.vessels.player_shadow(parent) if parent is not None else None
    if vessel is not None:
        struck = bool(getattr(vessel, "struck", False))
    rel = ""
    if t is not None:
        rel = _relative_words(world, t.bearing_rad)
    est = _estimate_m(world, battery.target)
    rng = f"{est / CABLE_M:.1f} cables" if est is not None else ""
    bits = [words]
    if rng:
        bits.append(rng + (f" {rel}" if rel else ""))
    elif rel:
        bits.append(rel)
    if struck:
        bits.append("struck")
    return {
        "words": ", ".join(bits),
        "id": battery.target,
        "struck": struck,
        "range_m": est,
        "relative": rel,
    }


def _relative_words(world: Any, bearing_rad: float) -> str:
    from freesail.world.lookout import relative_words

    return relative_words(bearing_rad - float(world.ship.heading))


def _estimate_m(world: Any, target_id: str) -> float | None:
    """The mark's range by the lookout's estimate, else by the truth (a ship without a
    lookout aloft)."""
    lookout = getattr(world, "lookout", None)
    if lookout is not None:
        for s in getattr(lookout, "sightings", ()):
            if getattr(getattr(s, "feature", None), "modern", None) == target_id:
                judged = getattr(s, "judged_m", None)
                if judged is not None:
                    return float(judged)
    from freesail.combat.action import target_of

    t = target_of(world, target_id)
    return float(t.range_m) if t is not None else None


def _range(world: Any, _: str | None) -> dict[str, Any] | None:
    battery = _battery(world)
    if battery is None or battery.target is None:
        return None
    est = _estimate_m(world, battery.target)
    if est is None:
        return None
    return {"metres": est, "words": range_words(est)}


def range_words(m: float) -> str:
    """A range in the period's words: pistol shot within a cable's third, then cables to
    a mile, then miles."""
    if m < CABLE_M / 3.0:
        return "pistol shot"
    if m < CABLE_M * 1.5:
        return "a cable"
    if m < units.NAUTICAL_MILE:
        return f"{m / CABLE_M:.0f} cables"
    nm = m / units.NAUTICAL_MILE
    return f"{nm:.1f} miles" if nm < 3 else f"{nm:.0f} miles"


def _no_mark_words(world: Any) -> str | None:
    battery = _battery(world)
    if battery is None:
        return _no_guns_words(world) or "she carries no guns"
    if battery.target is None:
        return "no mark is engaged"
    return "the mark is out of the lookout's sight"


def _colours(world: Any, _: str | None) -> dict[str, Any] | None:
    ship = getattr(world, "ship", None)
    if ship is None:
        return None
    struck = bool((getattr(ship, "extra", None) or {}).get("struck"))
    return {"words": "struck" if struck else "flying", "struck": struck}


def _quarter_bill(world: Any, _: str | None) -> dict[str, Any] | None:
    q = _quarters(world)
    if q is None:
        return None
    lines = q.describe()
    if not q.at_quarters:
        return {"words": "not at quarters", "at_quarters": False, "lines": lines}
    return {"words": " ".join(lines), "at_quarters": True, "lines": lines}


def _and(items: list[str]) -> str:
    if len(items) <= 1:
        return "".join(items)
    return ", ".join(items[:-1]) + " and " + items[-1]


# -- the registration ----------------------------------------------------------------------


def register() -> None:
    R.KINDS["state"] = (
        "a state in words: is cast loose, is struck, is not engaged, is none (the words of "
        "the reading, as the ground is compared)"
    )
    R.REGISTRY.add(
        R.Reading(
            "guns",
            ("the guns", "the battery", "the carronades"),
            "state",
            "",
            _guns,
            description="the battery: cast loose or secured, how many loaded, run out and "
            "primed, the side engaged and at whom, the charge, the aim, the firing's "
            "doctrine, the guns dismounted",
            none_words=_no_guns_words,
        )
    )
    R.REGISTRY.add(
        R.Reading(
            "damage",
            ("the damage", "the damage report", "the carpenter's report"),
            "state",
            "",
            _damage,
            description="the damage as her people report it: spars carried away, lines "
            "parted, sails holed, shot holes and where against the waterline, guns "
            "dismounted, the helm; 'none'",
        )
    )
    R.REGISTRY.add(
        R.Reading(
            "bill",
            ("the bill", "the butcher's bill", "the butchers bill", "the casualties"),
            "state",
            "",
            _bill,
            description="the butcher's bill: the killed and the wounded of the complement, "
            "and the hands' temper (steady, firm, shaken, wavering)",
        )
    )
    R.REGISTRY.add(
        R.Reading(
            "magazine",
            ("the magazine", "the powder", "the shot lockers"),
            "state",
            "",
            _magazine,
            description="the magazine as the gunner counts it: cartridges and shot by calibre",
            none_words=_no_guns_words,
        )
    )
    R.REGISTRY.add(
        R.Reading(
            "enemy",
            ("the enemy", "the mark"),
            "state",
            "",
            _enemy,
            description="the mark engaged, in the lookout's words, her range in cables by "
            "his estimate and where she bears; 'struck' when her colours are down; 'none "
            "engaged'",
            none_words=_no_guns_words,
        )
    )
    R.REGISTRY.add(
        R.Reading(
            "range",
            ("the range", "the range of the enemy", "the range of the mark", "the enemy's range"),
            "distance",
            "",
            _range,
            description="the range of the mark engaged by the lookout's estimate (a distance: "
            "'is under 3 cables', 'exceeds half a mile')",
            none_words=_no_mark_words,
        )
    )
    R.REGISTRY.add(
        R.Reading(
            "colours",
            ("the colours", "our colours", "the ensign"),
            "state",
            "",
            _colours,
            description="the ship's own colours: flying, or struck",
        )
    )
    R.REGISTRY.add(
        R.Reading(
            "quarter_bill",
            ("the quarter bill", "quarters"),
            "state",
            "",
            _quarter_bill,
            description="the quarter bill as beaten: each division and each gun's crew; "
            "'not at quarters'",
            none_words=_no_guns_words,
        )
    )
    # the events (spec §2's `at`; package 70)
    ev = R.EventSpec
    for spec in (
        ev("she opens fire", "action.fired_at"),
        ev("the enemy opens fire", "action.fired_at"),
        ev("a warning shot", "action.warning_shot"),
        ev("a shot across the bows", "action.warning_shot"),
        ev("a shot strikes", "action.hit"),
        ev("a hit", "action.hit"),
        ev("a man killed", "action.hit", lambda d: int(d.get("killed") or 0) > 0),
        ev(
            "a hand hurt",
            "action.hit",
            lambda d: int(d.get("killed") or 0) + int(d.get("wounded") or 0) > 0,
        ),
        ev("a gun dismounted", "action.hit", lambda d: "gun" in (d.get("kinds") or ())),
        ev("a spar shot away", "action.hit", lambda d: "spar" in (d.get("kinds") or ())),
        ev("the helm shot away", "action.hit", lambda d: "helm" in (d.get("kinds") or ())),
        ev("her colours come down", "action.enemy_struck"),
        ev("the enemy strikes", "action.enemy_struck"),
        ev("she strikes", "action.enemy_struck"),
        ev("the colours struck", "action.struck"),
        # the words after `at`: "at quarters" in the book (the key held the "at" itself
        # until the owner's first action, when the fighting book's two orders on it were
        # refused at the load; the lead, 2026-10-24)
        ev("quarters", "crew.quarters"),
        ev("the beat to quarters", "crew.quarters"),
        ev("cleared for action", "ship.cleared"),
        ev("the guns cast loose", "guns.cast_loose"),
        ev("the guns secured", "guns.secured"),
        ev("the magazine empty", "guns.magazine_empty"),
        ev("a broadside fired", "action.fired"),
        ev("the guns fired", "action.fired"),
    ):
        R.EVENTS[spec.words] = spec
