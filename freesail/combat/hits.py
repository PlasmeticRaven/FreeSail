"""A hit resolved into the part graph and the muster (spec M7 §9, rule 1; package 70).

No second model of the ship exists for the fight: a shot that strikes changes a state the
game already has, by the cause the director's hand uses today (`aboard: the fore topmast
is found sprung` and a shot that springs it end in the same state): a line parted
(`strain._part_line`, the sail coming down as it does now), a spar sprung or carried away
(`strain._wreck_spar`, the wreck cleared as it is), a sail holed (`Sail.holed_m2`, its area
cut), a gun dismounted (`Gun.dismounted`, a part out of the bill), a boat stove, the wheel
or the tiller ropes shot away (`ship.extra["helm_lost"]`, the helm held where it was until
73's repair), **a shot hole at or below the waterline written as state for 73's well to
read** (`ship.extra["shot_holes"]`: the side, the place along the hull, the height against
the waterline, the hole's size; no water flows from it here), and **men killed and
wounded written to the muster** (`Sailor.fit` false, `Sailor.hurt`), which takes them off
the bill; a named person hurt is a line of his own.

Where a shot lands is the aim's doctrine (spec M7 §9): at the hull (the British habit: the
hull, the guns, the men on the gun deck), at the rigging (the French: the sails, the spars
and the lines), or between wind and water; chain works on the rigging, grape on the men,
the double-shotted broadside at pistol shot on everything. The shares are judgements
(`AIM_SHARES`); what a hit does within its part is weighed by the part's stoutness against
the shot's weight (a 12-pound ball through a topgallant mast brings it down, through a
lower mast wounds it), and the casualties by the calibre and the men at the part struck
(Douglas 1820 on the effect of shot; the period's butcher's bills, about one killed to two
or three wounded, from memory). Every figure is named in the tuning notes and tuned in
play; nothing is made deadlier for the game's sake (rule 6).

Deterministic under the gunnery stream the action hands in.
"""

from __future__ import annotations

import math
from typing import Any

from freesail.combat import marks
from freesail.combat.guns import Aim, Battery, Target
from freesail.crew.model import Sailor, Station
from freesail.physics import strain as ST
from freesail.ship.parts import Charge, Gun, Line, LineState, SailState, Spar

__all__ = [
    "AIM_SHARES",
    "KILLED_SHARE",
    "SHOT_HOLE_BELOW_SHARE",
    "resolve_shot",
    "shot_diameter_m",
]

# Where a hit lands by the aim: the shares of hull, deck (the guns and the men there) and
# rigging (judgement on the doctrines of §9: the British fired into the hull, the French
# high).
AIM_SHARES: dict[Aim, tuple[float, float, float]] = {
    Aim.HULL: (0.55, 0.25, 0.20),
    Aim.RIGGING: (0.12, 0.13, 0.75),
    Aim.BETWEEN: (0.65, 0.20, 0.15),
}
# Within the rigging: lines, sails and spars (judgement: the running rigging is the most
# of what a ball meets aloft; chain and bar shot were for it).
RIGGING_SHARES = (0.45, 0.35, 0.20)
# A shot that goes high lands in the rigging when it lands at all.
# The share of hull hits at or below the waterline: a few when she shows her lee side,
# more when the mark heels her bottom toward the gun (the weather side presented:
# judgement), most under "between wind and water".
SHOT_HOLE_BELOW_SHARE = 0.12
SHOT_HOLE_HEEL_SHARE = 0.25  # added at fifteen degrees of heel with the bottom presented
SHOT_HOLE_BETWEEN_SHARE = 0.30  # added under the aim "between wind and water"
HEEL_REFERENCE_DEG = 15.0
# The men hurt by a hit, means by the place struck for an 18-pound shot at close range,
# scaled by the calibre (judgement after Douglas on the effect of shot and splinters, and
# the butcher's bills of 1805: a frigate's broadside of thirteen struck at pistol shot cost
# the mark a dozen men): the hull between decks the worst, the deck less, the rigging
# nobody at quarters but by a block falling. Grape triples the deck's and the hull's
# toward the men. Spent shot (beyond twice point blank) half.
MEN_HURT_HULL = 1.5
MEN_HURT_DECK = 1.0
MEN_HURT_RIGGING = 0.15
GRAPE_FACTOR = 3.0
REFERENCE_POUNDER = 18.0
# Of the men hurt, the share killed outright (judgement on the bills: one to two or three).
KILLED_SHARE = 0.3
# A gun struck: dismounted with this chance at a shot weight (pounds) equal to the gun's
# weight in hundredweight (a 12-pound ball against a 6-cwt carronade dismounts it four
# times in five; a 3-pound ball against the same once in four; an 18 against a 42-cwt
# long gun once in five: Douglas 1820, part I, on dismounting by heavy shot and seldom by
# light), else the carriage is wounded by this much condition (judgement). Of the shot that
# come across the deck, this share strike a carriage at all (judgement: the guns and their
# carriages take a third of the deck's length at the side).
DISMOUNT_AT_WEIGHT = 0.5
DECK_HIT_ON_A_GUN = 0.35
GUN_WOUND = 30.0
# A spar struck: carried away with a chance by the shot's weight against the spar's rating
# (a stout lower mast of hundreds of kN against a topgallant mast of thirty; judgement),
# else sprung by so much condition.
SPAR_SPRUNG = 40.0
# A sail holed: round shot a hole that tears so much, chain and bar twice (judgement after
# Douglas; a 5-inch ball makes a 5-inch hole that splits to a cloth or two in the wind).
HOLE_ROUND_M2 = 0.6
HOLE_CHAIN_M2 = 1.5
# The wheel or the tiller ropes shot away: this share of the hits on the after deck
# (judgement; the quarterdeck's helm was the first mark of a raking broadside).
HELM_SHOT_SHARE = 0.06
# A boat stove on the booms: this share of the hits on the midship deck of a ship with boats.
BOAT_STOVE_SHARE = 0.10


def shot_diameter_m(pounder: float) -> float:
    """The ball's diameter from its weight: 5.04 inches for the 18-pounder (iron,
    the gunner's rule; Douglas), as the cube root of the weight."""
    return 0.0254 * 5.04 * (max(pounder, 0.25) / 18.0) ** (1.0 / 3.0)


def resolve_shot(
    battery: Battery,
    gun: Gun,
    charge: Charge,
    target: Target,
    *,
    high: bool,
    rng: Any,
    tick: int,
) -> list[str]:
    """A shot that struck the mark: where it lands by the aim and what it does there,
    written to the mark's state. Returns what the firer's people could see of it (a spar
    coming down, a sail holed), for the battery's minute line; the mark's own log carries
    the rest through her damage keeper (`action.py`). A mark for practice is the marks'
    (practice and resupply, between packages 72 and 73): the cask knocked to staves, and
    nothing drawn (`marks.struck`)."""
    if marks.is_mark(target.id):
        return marks.struck(battery, gun, target, tick)
    body = target.body
    if body is None:
        return []
    if not hasattr(body, "parts"):
        # a far vessel (rule 5's coarse fight, 74's; package 70 keeps the sum)
        _far_hit(body, gun, charge)
        return []
    ship = body
    keeper = _damage(ship)
    pounder = gun.pounder
    aim = battery.aim
    hull_s, deck_s, rig_s = AIM_SHARES[aim]
    if charge is Charge.CHAIN:
        rig_s *= 2.0
    elif charge is Charge.GRAPE:
        deck_s *= 2.0
        rig_s *= 0.5
    if high:
        hull_s, deck_s, rig_s = hull_s * 0.2, deck_s * 0.5, rig_s + hull_s * 0.8 + deck_s * 0.5
    total = hull_s + deck_s + rig_s
    draw = rng.random() * total
    spent = target.range_m > 2.0 * _point_blank(gun)
    scale = pounder / REFERENCE_POUNDER * (0.5 if spent else 1.0)
    grape = GRAPE_FACTOR if charge is Charge.GRAPE else 1.0
    seen: list[str] = []
    # where along her length: uniform over the length she presents (the ball strikes
    # anywhere from stem to stern)
    length = float(getattr(getattr(ship, "hull", None), "length", target.length_m) or 40.0)
    x_m = (rng.random() - 0.5) * length
    side = _struck_side(target)
    if draw < hull_s:
        between = aim is Aim.BETWEEN
        seen += _hull_hit(ship, keeper, gun, target, x_m, side, scale, grape, between, rng, tick)
    elif draw < hull_s + deck_s:
        seen += _deck_hit(ship, keeper, gun, charge, target, x_m, side, scale, grape, rng, tick)
    else:
        seen += _rigging_hit(ship, keeper, gun, charge, pounder, scale, rng, tick)
    keeper.hits += 1
    return seen


# -- the hull -----------------------------------------------------------------------------


def _hull_hit(ship, keeper, gun, target, x_m, side, scale, grape, between, rng, tick) -> list[str]:
    """A shot into the hull: a hole above or below the water (the state for 73's well),
    splinters among the men between decks nearest it."""
    heel_toward = _heel_toward_gun(target, side)
    p_below = SHOT_HOLE_BELOW_SHARE
    if heel_toward > 0.0:
        p_below += SHOT_HOLE_HEEL_SHARE * min(1.0, heel_toward / HEEL_REFERENCE_DEG)
    if between:
        p_below += SHOT_HOLE_BETWEEN_SHARE
    below = rng.random() < p_below
    z_m = -(0.2 + rng.random() * 0.8) if below else (0.3 + rng.random() * 1.5)
    hole = {
        "tick": tick,
        "side": side,
        "x_m": round(x_m, 1),
        "z_m": round(z_m, 2),  # against the waterline upright, negative below
        "diameter_m": round(shot_diameter_m(gun.pounder), 3),
        "pounder": gun.pounder,
    }
    keeper.holes.append(hole)
    keeper.minute.append(
        ("hole", f"a shot {'between wind and water' if below else 'through the side'} to {side}")
    )
    _casualties(ship, keeper, MEN_HURT_HULL * scale * grape, x_m, "hull", rng, tick)
    return ["A shot struck her between wind and water."] if below else []


def _deck_hit(ship, keeper, gun, charge, target, x_m, side, scale, grape, rng, tick) -> list[str]:
    """A shot on the deck: a gun struck (dismounted or wounded), the helm, a boat, or the
    men there."""
    seen: list[str] = []
    length = float(getattr(getattr(ship, "hull", None), "length", 40.0) or 40.0)
    aft = x_m < -length / 4.0
    guns = [
        g
        for g in getattr(ship, "guns", {}).values()
        if ((g.side == side and g.place == "broadside") or g.place == "pivot") and not g.dismounted
    ]
    if aft and rng.random() < HELM_SHOT_SHARE and not ship.extra.get("helm_lost"):
        ship.extra["helm_lost"] = "the wheel shot away"
        ship.note(
            "urgent",
            "helm.shot_away",
            "The wheel is shot away; the helm is lost until the relieving tackles are rove.",
            None,
            {"tick": tick},
        )
        keeper.minute.append(("helm", "the wheel shot away"))
        _casualties(ship, keeper, MEN_HURT_DECK * scale * grape, x_m, "deck", rng, tick)
        return seen
    boats = list(getattr(getattr(ship, "spec", None), "boats", []) or [])
    stove = ship.extra.setdefault("boats_stove", [])
    whole = [b for b in boats if b.id not in stove]
    if abs(x_m) < length / 4.0 and whole and rng.random() < BOAT_STOVE_SHARE:
        boat = whole[0]
        stove.append(boat.id)
        ship.note(
            "notable",
            "boat.stove",
            f"{boat.name[:1].upper()}{boat.name[1:]} is stove on the booms by a shot.",
            None,
            {"boat": boat.id},
        )
        keeper.minute.append(("boat", f"{boat.name} stove"))
        return seen
    if guns and rng.random() < DECK_HIT_ON_A_GUN:
        g = min(guns, key=lambda g: abs(g.x_m - x_m))
        weight = max(g.weight_cwt, 0.5)
        p = min(0.85, max(0.03, DISMOUNT_AT_WEIGHT * gun.pounder / weight))
        if rng.random() < p:
            g.dismounted = True
            g.loaded = None
            g.run_out = False
            g.primed = False
            ship.note(
                "urgent",
                "gun.dismounted",
                f"{_cap(g.name)} is dismounted by a shot, the carriage knocked to pieces.",
                g.id,
                {"gun": g.id},
            )
            keeper.minute.append(("gun", f"{g.name} dismounted"))
            seen.append(f"A gun on her {side} side is struck.")
            mean = (MEN_HURT_DECK * scale + 1.0) * grape
            _casualties(ship, keeper, mean, g.x_m, "gun", rng, tick)
        else:
            g.condition = max(0.0, g.condition - GUN_WOUND)
            keeper.minute.append(("gun", f"{g.name}'s carriage struck"))
            _casualties(ship, keeper, MEN_HURT_DECK * scale * grape, g.x_m, "gun", rng, tick)
        return seen
    _casualties(ship, keeper, MEN_HURT_DECK * scale * grape, x_m, "deck", rng, tick)
    keeper.minute.append(("deck", "a shot across the deck"))
    return seen


def _rigging_hit(ship, keeper, gun, charge, pounder, scale, rng, tick) -> list[str]:
    """A shot aloft: a line parted, a sail holed or a spar carried away or sprung, by the
    rigging's shares and the part's stoutness."""
    seen: list[str] = []
    lines = [
        ln
        for ln in ship.lines.values()
        if ln.state is not LineState.PARTED and not ln.wrecked and _line_weight(ln) > 0
    ]
    sails = [s for s in ship.sails.values() if s.state in ST.ALOFT_STATES and not s.wrecked]
    spars = [s for s in ship.spars.values() if not s.wrecked and not s.sent_down]
    weights = list(RIGGING_SHARES)
    if not lines:
        weights[0] = 0.0
    if not sails:
        weights[1] = 0.0
    if not spars:
        weights[2] = 0.0
    total = sum(weights)
    if total <= 0.0:
        return seen
    draw = rng.random() * total
    st = ST.strain_state(ship)
    if draw < weights[0]:
        ln = _weighted(lines, [_line_weight(x) for x in lines], rng)
        ST._part_line(ship, st, ln, 0.0, how="shot away")
        keeper.minute.append(("line", f"{ST._name(ship, ln.id, False)} shot away"))
        if ln.cls in ST.HALYARD_CLASSES or ln.cls == "stay":
            seen.append("A sail of hers came down.")
    elif draw < weights[0] + weights[1]:
        sail = _weighted(sails, [max(s.area_m2, 1.0) for s in sails], rng)
        hole = HOLE_CHAIN_M2 if charge is Charge.CHAIN else HOLE_ROUND_M2
        hole *= max(0.5, pounder / REFERENCE_POUNDER) ** 0.5
        sail.holed_m2 = min(sail.area_m2, sail.holed_m2 + hole)
        keeper.minute.append(("sail", f"a shot through the {ST._name(ship, sail.id, False)}"))
        if sail.holed_share >= 0.5 and sail.state is SailState.SET:
            seen.append(f"Her {ST._name(ship, sail.id, False)} is shot to rags.")
    else:
        spar = _weighted(spars, [_spar_weight(s) for s in spars], rng)
        stout = max(float(spar.rating_kn), 1.0) / 10.0  # kN tens against pounds, judgement
        soft = 0.5 if charge is Charge.GRAPE else 1.0
        p = min(0.9, max(0.02, 0.9 * pounder / max(stout, 1.0) * soft))
        if rng.random() < p:
            ST._wreck_spar(ship, st, spar, 0.0, how="shot away")
            keeper.minute.append(("spar", f"the {ST._name(ship, spar.id, False)} shot away"))
            seen.append(f"Her {ST._name(ship, spar.id, False)} came down.")
        else:
            spar.condition = max(0.0, spar.condition - SPAR_SPRUNG * min(1.0, pounder / 18.0))
            keeper.minute.append(("spar", f"the {ST._name(ship, spar.id, False)} wounded"))
    _casualties(ship, keeper, MEN_HURT_RIGGING * scale, 0.0, "rigging", rng, tick)
    return seen


# -- the men -----------------------------------------------------------------------------


# The quarterdeck is the most exposed place (spec M7 §16a; the owner's note 7): of the
# men hurt by a hit on the after deck, this share fall on the quarterdeck's people (the
# posts, the helmsmen, a station holder's person) rather than the hands (judgement: a
# frigate's quarterdeck in close action lost its captain or a lieutenant in a good third
# of the recorded actions; James's returns).
QUARTERDECK_SHARE = 0.2


def _casualties(ship, keeper, mean: float, x_m: float, where: str, rng, tick) -> int:
    """So many men hurt, drawn about the mean (a Poisson draw by the inverse method on the
    stream), from the men at the part struck: the gun crews nearest along the hull first,
    then the powder, the trimmers and the rest; on the after deck the quarterdeck's people
    by their share (package 73); each killed with `KILLED_SHARE`, else wounded (light or
    grave, the health keeper's: `crew/health.py`), written to the muster and off the bill.
    Returns how many."""
    crew = ship.extra.get("crew")
    if crew is None or mean <= 0.0:
        return 0
    n = _poisson(mean, rng)
    if n <= 0:
        return 0
    quarters = ship.extra.get("quarters")
    candidates: list[Sailor] = []
    if quarters is not None and getattr(quarters, "at_quarters", False):
        crews = sorted(quarters.crews.values(), key=lambda gc: abs(gc.x_m - x_m))
        for gc in crews:
            candidates += [s for s in gc.hands if s.fit]
        for name in ("powder", "trimmers", "helm", "marines"):
            candidates += [s for s in quarters.divisions.get(name, []) if s.fit]
    if not candidates:
        candidates = [s for s in crew.on_deck(_clock_of(ship)) if s.fit]
    if not candidates:
        candidates = [s for s in crew.sailors if s.fit]
    length = float(getattr(getattr(ship, "hull", None), "length", 40.0) or 40.0)
    aft = where in ("deck", "gun") and x_m < -length / 4.0
    quarterdeck = [s for s in crew.by_station[Station.QUARTERDECK] if s.fit] if aft else []
    hurt = 0
    taken: set[str] = set()
    # the quarterdeck's share is drawn on the health's stream, not the gunnery's, so that
    # the shot's own sequence runs as 70 and 71 left it (package 73)
    qd_rng = None
    if quarterdeck:
        from freesail.orders.prompt import world_of

        world = world_of(ship)
        qd_rng = world.rng.stream("health") if world is not None else None
    for _ in range(n):
        pool = candidates
        if quarterdeck and qd_rng is not None and qd_rng.random() < QUARTERDECK_SHARE:
            pool = quarterdeck
        s = next((x for x in pool if x.id not in taken and x.fit), None)
        if s is None:
            s = next((x for x in candidates if x.id not in taken and x.fit), None)
        if s is None:
            break
        taken.add(s.id)
        killed = rng.random() < KILLED_SHARE
        hit_man(ship, s, killed, rng, tick)
        hurt += 1
        if killed:
            keeper.killed += 1
        else:
            keeper.wounded += 1
        keeper.minute_men.append(s)
    return hurt


def hit_man(ship: Any, s: Sailor, killed: bool, rng: Any, tick: int, how: str = "") -> None:
    """One man struck: the health keeper's states (killed, or wounded light or grave with
    the wound in words, a person's station told); 70's two words where the ship sails
    in no world."""
    from freesail.orders.prompt import world_of

    world = world_of(ship)
    health = getattr(world, "health", None) if world is not None else None
    if health is not None:
        health.hit(s, killed, rng, tick, how=how)
        return
    s.fit = False
    s.hurt = "killed" if killed else "wounded"
    s.hurt_tick = tick
    s.at = None


def _poisson(mean: float, rng) -> int:
    limit = math.exp(-mean)
    k, p = 0, 1.0
    while True:
        p *= rng.random()
        if p <= limit:
            return k
        k += 1
        if k > 50:
            return k


# -- the far body (rule 5's measure; 74 builds the fight) -----------------------------------


def _far_hit(vessel: Any, gun: Gun, charge: Charge) -> None:
    d = vessel.damage
    d["hits"] = d.get("hits", 0) + 1
    d["weight_lb"] = d.get("weight_lb", 0.0) + gun.pounder * (2 if charge is Charge.DOUBLE else 1)


# -- helpers --------------------------------------------------------------------------


class Damage:
    """The mark's damage as her people report it (`action.py` reads it): the shot holes,
    the butcher's bill, the hits counted, and this minute's happenings for the one line."""

    def __init__(self) -> None:
        self.hits = 0
        self.killed = 0
        self.wounded = 0
        self.holes: list[dict[str, Any]] = []
        self.minute: list[tuple[str, str]] = []
        self.minute_men: list[Sailor] = []
        self.struck_by: dict[str, int] = {}  # firer id -> the last tick her shot came
        self.opened_by: set[str] = set()  # the firers whose opening fire was said
        self.warned_by: set[str] = set()  # the firers whose shot across the bows was said
        self.first_struck_tick: int | None = None


def _damage(ship: Any) -> Damage:
    extra = ship.extra
    d = extra.get("damage")
    if not isinstance(d, Damage):
        d = Damage()
        extra["damage"] = d
    return d


def damage_of(ship: Any) -> Damage | None:
    extra = getattr(ship, "extra", None)
    if extra is None:
        return None
    return _damage(ship)


def _struck_side(target: Target) -> str:
    """The side of the mark the shot strikes: the one toward the gun."""
    import math as _m

    from freesail import units

    rel = units.wrap_pi(target.bearing_rad + _m.pi - target.heading_rad)
    return "starboard" if rel >= 0.0 else "larboard"


def _heel_toward_gun(target: Target, side: str) -> float:
    """Degrees of the mark's heel that present her bottom to the gun: heel away from the
    struck side (positive to starboard)."""
    heel = target.heel_deg
    if side == "starboard":
        return max(0.0, -heel)
    return max(0.0, heel)


def _point_blank(gun: Gun) -> float:
    from freesail.combat.shot import ballistics_of

    return ballistics_of(gun.kind, gun.pounder).point_blank_m


def _line_weight(ln: Line) -> float:
    return {
        "brace": 3.0,
        "sheet": 3.0,
        "halyard": 2.0,
        "throat_halyard": 1.5,
        "peak_halyard": 1.5,
        "stay": 2.0,
        "shroud": 2.0,
        "backstay": 1.0,
        "lift": 1.0,
        "tack": 1.0,
        "bowline": 0.5,
        "clewline": 0.5,
        "buntline": 0.3,
    }.get(ln.cls, 0.5)


def _spar_weight(spar: Spar) -> float:
    """A spar's exposure to shot aloft: the upper spars most (judgement)."""
    return {
        "royal_mast": 3.0,
        "topgallant_mast": 3.0,
        "royal_yard": 2.0,
        "topmast": 2.0,
        "yard": 2.0,
        "gaff": 2.0,
        "boom": 1.5,
        "lug_yard": 2.0,
        "jib_boom": 1.5,
        "flying_jib_boom": 1.5,
        "mast": 0.6,
        "bowsprit": 0.6,
    }.get(spar.cls, 1.0)


def _weighted(items: list[Any], weights: list[float], rng) -> Any:
    total = sum(weights)
    draw = rng.random() * total
    acc = 0.0
    for item, w in zip(items, weights, strict=True):
        acc += w
        if draw < acc:
            return item
    return items[-1]


def _clock_of(ship: Any) -> Any:
    from datetime import datetime

    runner = ship.extra.get("evolutions")
    clock = getattr(runner, "clock", None)
    return clock if clock is not None else datetime(1805, 6, 1, 4, 0, 0)


def _cap(words: str) -> str:
    return words[:1].upper() + words[1:]
