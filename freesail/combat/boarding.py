"""The fight on deck (spec M7 §11, §11a; package 73; the design in
`docs/design/Design-WaterAndHealth.md`): the grapple, the boarders away, the rounds and
the deck carried or the boarders repulsed.

The ground for it: `lay her aboard` (the helm closing to pistol shot and under: the chase's
course) and `grapple her` (`grapple`, an evolution: eight hands and two minutes within
`GRAPPLE_RANGE_M`; Falconer 1780, GRAPPLING) write `extra["grappled_to"]` on both ships
and the integrator holds both as the ground holds a ship (`physics/integrate.py`), so the
two lie locked and drift together for the minutes the fight takes; `cast off the grapnels`
frees them. Two hulls within pistol shot overlap on the chart until the collision is built
(78's); said here once.

The sides: the attacker's boarders are the quarter bill's `boarders` told off from the
guns' crews (Luce 1884 ch. XX) with the marines; the defenders every fit man on the upper
deck not at the pumps, the powder or the surgeon's work when `repel boarders` has been
given (the guns silent, the defence at its whole strength), else the marines, the helm, the
trimmers and the quarterdeck. The rounds: from the crossing, once a minute while grappled,
each side's strength is its men times their arms (the small arms served out 1.0, not 0.5;
the marines with the bayonet by their kit; soldiers of the line theirs) times its temper
(the ship's morale, 70's figure) times its cover (the defenders behind the bulwarks and
nettings 1.3 in the first round, the boarders crossing 0.8); before the first round the
defenders' marines' volley and the guns bearing on the boarders' deck tell; each round each
side loses a Poisson draw about `ROUND_LOSS` times the other's strength over ten (a
boarding of fifty against forty costs each side five or six men a minute and is decided in
five to ten: the period's boardings were short), the fallen killed three in ten and wounded
else, written to the muster. The deck is carried when the defenders' strength falls under
`CARRIED_RATIO` of the boarders' or their temper under its line (the colours struck by the
boarders' hand: `action.strike`; the prize crew is 74's); the boarders are repulsed when
theirs falls under the same share of the defenders' or their temper under its line (they
cast off, their temper the worse by `REPULSE_COST`); a deck contested past `CONTEST_ROUNDS`
is a repulse. The log carries a line a round on both ships and the end.

Every figure is judgement with its reason; nothing here is measured against a source
closer than the actions' narratives (James, the single-ship actions; the boardings of the
Hermione's cutting out and of the privateers).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any

from freesail.core.events import Severity
from freesail.crew.model import Sailor, Station, number_words

__all__ = [
    "BOARD_RANGE_M",
    "CARRIED_RATIO",
    "CONTEST_ROUNDS",
    "GRAPPLE_RANGE_M",
    "REPULSE_COST",
    "ROUND_LOSS",
    "Fight",
    "boarders_away",
    "boarders_of",
    "cast_off",
    "defenders_of",
    "describe",
    "fight_of",
    "grapple",
    "grappled_to",
    "tick",
]

# The helm's close law for `lay her aboard`: within this she is laid aboard (pistol shot
# and under; judgement), and the grapnels are thrown within this (Falconer 1780,
# GRAPPLING: the grapnels on chains thrown into the enemy's rigging and chains).
BOARD_RANGE_M = 25.0
GRAPPLE_RANGE_M = 30.0
ROUND_S = 60
ROUND_LOSS = 1.0
CARRIED_RATIO = 0.5
CONTEST_ROUNDS = 15
REPULSE_COST = 0.1
FIRST_ROUND_ATTACK = 0.8  # the boarders crossing
FIRST_ROUND_DEFENCE = 1.3  # behind the bulwarks and the nettings
KILLED_SHARE = 0.3
# The crossing: the defenders' marines' volley at the boarders coming over (each musket at
# point blank, the kit's chance five times its fifty-yard figure) and the guns bearing on
# the boarders' deck, loaded, each telling on so many men (grape or whatever is in them;
# judgement).
CROSSING_MUSKET_HIT = 5.0
CROSSING_GUN_MEAN = 1.0
BLOW_WORDS = (
    "a cutlass cut on the head",
    "a cutlass cut on the arm",
    "a pike thrust in the side",
    "a pike thrust in the thigh",
    "a pistol ball in the breast",
    "a pistol ball in the shoulder",
    "a blow of a tomahawk",
    "a musket butt on the head",
    "a bayonet in the body",
)


@dataclass
class Fight:
    """One fight on deck, one object on both ships (`ship.extra["fight"]`)."""

    attacker: Any  # the boarders' ship (a Ship)
    defender: Any
    attacker_world: Any
    defender_world: Any
    attacker_id: str
    defender_id: str
    started_tick: int
    round: int = 0
    last_round_tick: int = -(10**9)
    over: str = ""  # "", "carried", "repulsed", "contested"
    lost_attack: int = 0
    lost_defence: int = 0
    repelling: bool = False
    lines: list[str] = field(default_factory=list)

    def side_of(self, ship: Any) -> str:
        return "attacker" if ship is self.attacker else "defender"


def fight_of(ship: Any) -> Fight | None:
    f = (getattr(ship, "extra", None) or {}).get("fight")
    return f if isinstance(f, Fight) else None


def grappled_to(ship: Any) -> str:
    return str((getattr(ship, "extra", None) or {}).get("grappled_to") or "")


def _own_id(world: Any) -> str:
    from freesail.world.brains import PLAYER_ID

    vessel = getattr(world, "vessel", None)
    return str(vessel.id) if vessel is not None else PLAYER_ID


def _words_in(world: Any, ship_id: str, fallback: str) -> str:
    from freesail.combat.action import _words_in

    return _words_in(world, ship_id, fallback)


def _poisson(mean: float, rng: Any) -> int:
    if mean <= 0.0:
        return 0
    limit = math.exp(-mean)
    k, p = 0, 1.0
    while True:
        p *= rng.random()
        if p <= limit:
            return k
        k += 1
        if k > 60:
            return k


def _morale(ship: Any) -> Any:
    from freesail.combat.morale import morale_of

    return morale_of(ship)


# -- the grapple ------------------------------------------------------------------------------


def grapple(world: Any, target: Any, say: bool = True) -> str:
    """Both ships grappled: the state on both, the integrator holding both, a line in each
    log (the own line left to the evolution's done line when `say` is false)."""
    ship = world.ship
    body = target.body
    own = _own_id(world)
    ship.extra["grappled_to"] = str(target.id)
    if getattr(body, "extra", None) is not None:
        body.extra["grappled_to"] = own
    text = (
        f"Grappled to {target.words}: the grapnels fast in her chains and her rigging, the "
        "two ships locked together and drifting as one. ('boarders away' to board her, "
        "'cast off the grapnels' to free her.)"
    )
    if say:
        world.record(Severity.URGENT, "ship.grappled", text, data={"to": str(target.id)})
    tw = target.world
    if tw is not None and tw is not world:
        who = _words_in(tw, own, "the enemy")
        tw.record(
            Severity.URGENT,
            "ship.grappled",
            f"{who[:1].upper()}{who[1:]} has grappled us: her grapnels are fast in our chains "
            "and rigging, the two ships locked together.",
            data={"to": own},
        )
    return text


def cast_off(world: Any) -> str:
    """The grapnels cast off, the ships free; the boarders recalled if ours are on her deck
    (a repulse at our own word), refused while hers are on ours."""
    from freesail.orders.errors import OrderError

    ship = world.ship
    other_id = grappled_to(ship)
    if not other_id:
        raise OrderError("She is grappled to nobody.")
    f = fight_of(ship)
    if f is not None and not f.over and f.defender is ship:
        raise OrderError(
            "Her boarders are on our deck: repel them before the grapnels are cast off."
        )
    other = _other_body(world, other_id)
    if f is not None and not f.over and f.attacker is ship:
        _end(f, "repulsed", "the boarders recalled at the word and the grapnels cast off")
        return (
            "The boarders are recalled over the side and the grapnels cast off; she is free of her."
        )
    ship.extra.pop("grappled_to", None)
    if other is not None and getattr(other, "extra", None) is not None:
        other.extra.pop("grappled_to", None)
    return "The grapnels are cast off: the ships are free of each other."


def _other_body(world: Any, other_id: str) -> Any:
    from freesail.combat.action import _body_of

    try:
        return _body_of(world, other_id)
    except Exception:  # noqa: BLE001
        return None


def _other_world(world: Any, other_id: str) -> Any:
    from freesail.world.brains import PLAYER_ID

    parent = getattr(world, "parent", None)
    if other_id == PLAYER_ID and parent is not None:
        return parent
    sea = parent.vessels if parent is not None else getattr(world, "vessels", None)
    v = sea.get(other_id) if sea is not None else None
    crew = getattr(v, "crew", None) if v is not None else None
    return crew if crew is not None and getattr(crew, "shape", "full") == "full" else None


# -- the sides ------------------------------------------------------------------------------


def boarders_of(ship: Any, world: Any) -> list[tuple[Sailor, float]]:
    """The attacker's boarders with each man's arms factor: the marines by their kit, the
    bill's boarders from the guns' crews with the small arms served out or not."""
    from freesail.combat.small_arms import (
        boarders_count,
        kit_of,
        marines_of,
        musketry_of,
        small_arms_of,
    )

    crew = ship.extra.get("crew")
    if crew is None:
        return []
    kit = kit_of(world)
    arms = small_arms_of(world)
    m = musketry_of(ship)
    seaman = float(arms.get("served_factor", 1.0) if m.served else arms.get("unserved_factor", 0.5))
    out: list[tuple[Sailor, float]] = [
        (s, float(kit.get("boarding", 1.2))) for s in marines_of(ship)
    ]
    taken = {s.id for s, _ in out}
    n = boarders_count(ship)
    pool = [
        s
        for s in crew.sailors
        if s.fit
        and s.id not in taken
        and s.station not in (Station.MARINES, Station.QUARTERDECK, Station.IDLERS)
    ]
    # the most skilled on deck first: the boarders are the best men of the guns' crews
    pool.sort(key=lambda s: (-float(getattr(s, "skill_deck", 0.0) or 0.0), s.id))
    out += [(s, seaman) for s in pool[:n]]
    return out


def defenders_of(ship: Any, world: Any, repelling: bool) -> list[tuple[Sailor, float]]:
    """The defenders: every fit man on deck but the powder's, the carpenter's and the
    surgeon's when `repel boarders` is given, else the marines, the helm, the trimmers,
    the quarterdeck and the small-arms men."""
    from freesail.combat.small_arms import (
        kit_of,
        marines_of,
        musketry_of,
        small_arms_count,
        small_arms_of,
    )
    from freesail.crew.quarters import CARPENTER, HELM, POWDER, SURGEON, TRIMMERS

    crew = ship.extra.get("crew")
    if crew is None:
        return []
    kit = kit_of(world)
    arms = small_arms_of(world)
    m = musketry_of(ship)
    seaman = float(arms.get("served_factor", 1.0) if m.served else arms.get("unserved_factor", 0.5))
    out: list[tuple[Sailor, float]] = [
        (s, float(kit.get("boarding", 1.2))) for s in marines_of(ship)
    ]
    taken = {s.id for s, _ in out}
    quarters = ship.extra.get("quarters")
    at_quarters = quarters is not None and getattr(quarters, "at_quarters", False)
    rest: list[Sailor] = []
    if repelling or not at_quarters:
        below = set()
        if at_quarters:
            for name in (POWDER, CARPENTER, SURGEON):
                below |= {s.id for s in quarters.divisions.get(name, [])}
        rest = [s for s in crew.sailors if s.fit and s.id not in taken and s.id not in below]
    else:
        for name in (HELM, TRIMMERS):
            rest += [s for s in quarters.divisions.get(name, []) if s.fit and s.id not in taken]
        rest += [
            s for s in crew.by_station.get(Station.QUARTERDECK, []) if s.fit and s.id not in taken
        ]
        n = small_arms_count(ship)
        others = [
            s
            for s in crew.sailors
            if s.fit
            and s.id not in taken
            and s not in rest
            and s.station not in (Station.MARINES, Station.IDLERS)
        ]
        rest += others[:n]
    out += [(s, seaman) for s in rest]
    return out


def _strength(men: list[tuple[Sailor, float]], temper: float, cover: float) -> float:
    return sum(f for _, f in men) * max(0.05, temper) * cover


# -- the boarders away ------------------------------------------------------------------------


def boarders_away(world: Any) -> str:
    """The boarders over the side: the fight begun, the crossing's fire told, the first
    round at the next minute."""
    from freesail.orders.errors import OrderError

    ship = world.ship
    other_id = grappled_to(ship)
    if not other_id:
        raise OrderError(
            "She is grappled to nobody: lay her aboard and 'grapple her' before the boarders "
            "are called away."
        )
    f = fight_of(ship)
    if f is not None and not f.over:
        if f.attacker is ship:
            raise OrderError("The boarders are on her deck already; the fight is going on.")
        raise OrderError("Her boarders are on our deck: 'repel boarders'.")
    body = _other_body(world, other_id)
    if body is None or getattr(body, "extra", None) is None or body.extra.get("crew") is None:
        raise OrderError("She is a far sail with no company modelled to fight; nothing to board.")
    if body.extra.get("struck"):
        raise OrderError(
            "She has struck already: taking possession (the prize crew, the prisoners) is not "
            "yet in the game."
        )
    quarters = ship.extra.get("quarters")
    if quarters is None or not getattr(quarters, "at_quarters", False):
        raise OrderError("The company is not at quarters: 'beat to quarters' first.")
    tick = int(world.clock.tick)
    other_world = _other_world(world, other_id)
    from freesail.combat.small_arms import musketry_of

    quarters.marines_to_arms()

    dq = body.extra.get("quarters")
    if dq is not None and getattr(dq, "at_quarters", False) and hasattr(dq, "marines_to_arms"):
        dq.marines_to_arms()
    f = Fight(
        attacker=ship,
        defender=body,
        # the attacker's hull, not the World (package 84, step 6): the round runs in
        # whichever hull ticks first in the minute, and a World's names are hers then
        attacker_world=getattr(world, "own", world),
        defender_world=other_world,
        attacker_id=_own_id(world),
        defender_id=other_id,
        started_tick=tick,
        repelling=bool(musketry_of(body).repelling),
    )
    ship.extra["fight"] = f
    body.extra["fight"] = f
    ours = boarders_of(ship, world)
    rng = world.rng.stream("gunnery")
    crossing = _crossing_fire(f, rng, tick)
    who = _words_in(world, other_id, "the enemy")
    text = (
        f"Boarders away! {number_words(len(ours))} over the side on to {who}'s deck, the "
        f"marines with the bayonet" + (f"; {crossing}" if crossing else "") + "."
    )
    if other_world is not None and other_world is not world:
        defenders = defenders_of(body, other_world, f.repelling)
        whose = _words_in(other_world, f.attacker_id, "the enemy")
        other_world.record(
            Severity.URGENT,
            "action.boarded",
            f"{whose[:1].upper()}{whose[1:]}'s boarders are coming over the side! "
            f"{number_words(len(defenders))} of ours to meet them at the gangways"
            + ("" if f.repelling else " ('repel boarders' brings the gun crews up)")
            + ".",
            data={"defenders": len(defenders), "by": f.attacker_id},
        )
    f.last_round_tick = tick
    return text


def _crossing_fire(f: Fight, rng: Any, tick: int) -> str:
    """The defenders' marines' volley and the guns bearing as the boarders come over."""
    from freesail.combat.small_arms import kit_of, marines_of, strike_a_man

    dw = f.defender_world
    kit = kit_of(dw) if dw is not None else {"hit_at_50_yd": 0.04}
    marines = marines_of(f.defender)
    mean = len(marines) * float(kit.get("hit_at_50_yd", 0.04)) * CROSSING_MUSKET_HIT
    guns_told = 0
    if not f.repelling:
        guns = getattr(f.defender, "guns", {}) or {}
        quarters = f.defender.extra.get("quarters")
        manned = set()
        if quarters is not None:
            for gc in quarters.crews.values():
                if gc.hands:
                    manned |= set(gc.guns)
        side = _side_facing(f.defender, f.attacker)
        for gid, g in guns.items():
            if gid in manned and getattr(g, "side", "") == side and getattr(g, "loaded", False):
                guns_told += 1
        mean += guns_told * CROSSING_GUN_MEAN
    fell = _poisson(mean, rng)
    for _ in range(fell):
        how = "a musket ball in the breast" if rng.random() < 0.5 else "grape as he came over"
        strike_a_man(
            f.attacker, _side_facing(f.attacker, f.defender), rng, tick, how, f.defender_id, 0.0
        )
    f.lost_attack += fell
    parts = []
    if marines:
        parts.append("her marines' volley from behind the nettings")
    if guns_told:
        parts.append(f"{number_words(guns_told)} gun{'s' if guns_told != 1 else ''} bearing")
    if not parts:
        return ""
    return (
        " and ".join(parts) + f" cost {number_words(fell)} of ours in the crossing"
        if fell
        else " and ".join(parts) + " told on nobody"
    )


def _side_facing(ship: Any, other: Any) -> str:
    """The side of `ship` that `other` lies on: by the two headings and positions where
    the Worlds know them, else starboard."""
    try:
        from freesail.world.geo import bearing_and_distance

        w1 = _world_of(ship)
        w2 = _world_of(other)
        if w1 is None or w2 is None or w1.position is None or w2.position is None:
            return "starboard"
        bearing, _ = bearing_and_distance(w1.position, w2.position)
        heading = float(ship.dyn.heading)
        rel = (math.radians(bearing) - heading + math.pi) % (2.0 * math.pi) - math.pi
        return "starboard" if rel >= 0.0 else "larboard"
    except Exception:  # noqa: BLE001
        return "starboard"


def _world_of(ship: Any) -> Any:
    from freesail.orders.prompt import world_of

    return world_of(ship)


# -- the rounds ---------------------------------------------------------------------------------


def tick(world: Any) -> None:
    """One round a minute while the fight lasts; whichever of the two Worlds ticks first
    in the minute runs it."""
    ship = world.ship
    f = fight_of(ship)
    if f is None or f.over:
        return
    t = int(world.clock.tick)
    if t - f.last_round_tick < ROUND_S:
        return
    f.last_round_tick = t
    f.round += 1
    _round(f, t)


def _round(f: Fight, tick: int) -> None:
    from freesail.combat.small_arms import strike_a_man

    aw, dw = f.attacker_world, f.defender_world
    rng = aw.rng.stream("gunnery")
    first = f.round == 1
    ours = boarders_of(f.attacker, aw)
    theirs = defenders_of(f.defender, dw if dw is not None else aw, f.repelling)
    ma, md = _morale(f.attacker), _morale(f.defender)
    sa = _strength(ours, float(ma.value), FIRST_ROUND_ATTACK if first else 1.0)
    sd = _strength(theirs, float(md.value), FIRST_ROUND_DEFENCE if first else 1.0)
    lose_a = min(len(ours), _poisson(ROUND_LOSS * sd / 10.0, rng))
    lose_d = min(len(theirs), _poisson(ROUND_LOSS * sa / 10.0, rng))
    side_a = _side_facing(f.attacker, f.defender)
    side_d = _side_facing(f.defender, f.attacker)
    for _ in range(lose_a):
        how = BLOW_WORDS[int(rng.random() * len(BLOW_WORDS)) % len(BLOW_WORDS)]
        strike_a_man(f.attacker, side_a, rng, tick, how, f.defender_id, 0.1)
    for _ in range(lose_d):
        how = BLOW_WORDS[int(rng.random() * len(BLOW_WORDS)) % len(BLOW_WORDS)]
        strike_a_man(f.defender, side_d, rng, tick, how, f.attacker_id, 0.3)
    f.lost_attack += lose_a
    f.lost_defence += lose_d
    # the sides as they stand after the round
    ours = boarders_of(f.attacker, aw)
    theirs = defenders_of(f.defender, dw if dw is not None else aw, f.repelling)
    sa = _strength(ours, float(ma.value), 1.0)
    sd = _strength(theirs, float(md.value), 1.0)
    line_a = (
        f"The boarders are on her deck: the fight at the gangways (round {f.round}); "
        f"{number_words(lose_a)} of ours down, {number_words(lose_d)} of theirs."
    )
    line_d = (
        f"Her boarders are on our deck: the fight at the gangways (round {f.round}); "
        f"{number_words(lose_d)} of ours down, {number_words(lose_a)} of theirs."
    )
    data = {
        "round": f.round,
        "lost_attack": lose_a,
        "lost_defence": lose_d,
        "strength_attack": round(sa, 1),
        "strength_defence": round(sd, 1),
        "boarders": len(ours),
        "defenders": len(theirs),
        "temper_attack": round(float(ma.value), 2),
        "temper_defence": round(float(md.value), 2),
    }
    aw.record(Severity.URGENT, "action.boarding", line_a, data=data)
    if dw is not None and dw is not aw:
        dw.record(Severity.URGENT, "action.boarding", line_d, data=data)
    if not theirs or sd < CARRIED_RATIO * sa or float(md.value) < float(md.strike_below):
        _end(f, "carried", "")
    elif not ours or sa < CARRIED_RATIO * sd or float(ma.value) < float(ma.strike_below):
        _end(f, "repulsed", "the boarders driven back over the side")
    elif f.round >= CONTEST_ROUNDS:
        _end(f, "contested", "the deck contested past a quarter of an hour, the boarders drawn off")


def _end(f: Fight, how: str, why: str) -> None:
    from freesail.combat import action

    f.over = how
    aw, dw = f.attacker_world, f.defender_world
    tick = int(aw.clock.tick)
    who = _words_in(aw, f.defender_id, "the enemy")
    if how == "carried":
        aw.record(
            Severity.URGENT,
            "action.carried",
            f"Her deck is carried: {who}'s colours come down by our boarders' hand "
            f"({number_words(f.lost_attack)} of ours lost in the boarding, "
            f"{number_words(f.lost_defence)} of hers); the prize crew and the prisoners are "
            "not yet in the game.",
            data={"lost_attack": f.lost_attack, "lost_defence": f.lost_defence, "tick": tick},
        )
        if dw is not None:
            action.strike(dw, by_rule=False, words="carried by boarding")
        else:
            f.defender.extra["struck"] = tick
        return
    m = _morale(f.attacker)
    m.repulses = float(getattr(m, "repulses", 0.0)) + REPULSE_COST
    f.attacker.extra.pop("grappled_to", None)
    f.defender.extra.pop("grappled_to", None)
    kind = "action.repulsed"
    aw.record(
        Severity.URGENT,
        kind,
        f"The boarders are repulsed: {why}; the grapnels cast off ({number_words(f.lost_attack)} "
        f"of ours lost, {number_words(f.lost_defence)} of hers). The hands' temper the worse "
        "for it.",
        data={"lost_attack": f.lost_attack, "lost_defence": f.lost_defence, "how": how},
    )
    if dw is not None and dw is not aw:
        whose = _words_in(dw, f.attacker_id, "the enemy")
        dw.record(
            Severity.URGENT,
            kind,
            f"{whose[:1].upper()}{whose[1:]}'s boarders are repulsed and driven back over the "
            f"side; the grapnels cast off ({number_words(f.lost_defence)} of ours lost, "
            f"{number_words(f.lost_attack)} of theirs).",
            data={"lost_attack": f.lost_attack, "lost_defence": f.lost_defence, "how": how},
        )


def repel(world: Any) -> str:
    """`repel boarders`: the gun crews come up, the guns fall silent, the defence at its
    whole strength; a standing state until the guns are cast loose again."""
    from freesail.combat.guns import FireMode, battery_of
    from freesail.combat.small_arms import musketry_of

    ship = world.ship
    m = musketry_of(ship)
    quarters = ship.extra.get("quarters")
    if quarters is None or not getattr(quarters, "at_quarters", False):
        from freesail.orders.errors import OrderError

        raise OrderError("The company is not at quarters: 'beat to quarters' first.")
    m.repelling = True
    quarters.marines_to_arms()
    battery = battery_of(ship)
    if battery is not None:
        battery.mode = FireMode.HOLD
    f = fight_of(ship)
    if f is not None and not f.over and f.defender is ship:
        f.repelling = True
    n = len(defenders_of(ship, world, True))
    text = (
        f"Repel boarders! The gun crews up from the guns with the pikes and the cutlasses, "
        f"the marines at the gangways: {number_words(n)} to hold the deck. The guns are silent "
        "while they do."
    )
    return text


def describe(world: Any, ship: Any) -> dict[str, Any]:
    """The boarders and the fight for the reading."""
    from freesail.combat.small_arms import musketry_of

    crew = ship.extra.get("crew")
    if crew is None:
        return {"words": "no ship's company is mustered", "boarders": 0}
    ours = boarders_of(ship, world)
    m = musketry_of(ship)
    other = grappled_to(ship)
    f = fight_of(ship)
    arms = (
        "the small arms served out"
        if m.served
        else "the small arms in the chests ('serve out the small arms')"
    )
    words = f"{number_words(len(ours))} boarders by the bill, {arms}"
    if other:
        words += f"; grappled to {_words_in(world, other, 'the enemy')}"
    if f is not None:
        side = f.side_of(ship)
        if not f.over:
            words += f"; the fight on deck, round {f.round}: " + (
                f"ours on her deck, {number_words(f.lost_attack)} of ours down and "
                f"{number_words(f.lost_defence)} of hers"
                if side == "attacker"
                else f"hers on our deck, {number_words(f.lost_defence)} of ours down and "
                f"{number_words(f.lost_attack)} of hers"
            )
        else:
            words += f"; the last fight {f.over}"
    if m.repelling:
        words += "; the gun crews up to repel boarders, the guns silent"
    return {
        "words": words,
        "boarders": len(ours),
        "served": m.served,
        "grappled_to": other,
        "fight": None if f is None else {"round": f.round, "over": f.over, "side": f.side_of(ship)},
        "repelling": m.repelling,
    }
