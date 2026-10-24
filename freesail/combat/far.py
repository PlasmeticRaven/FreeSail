"""The far fight's measure (spec M7 §11a; package 70, item 9): two ships that meet in anger
beyond the promotion's range resolved by the same tables at coarse steps, with no ship
graph, no crew and no World, so that 74 has a measured ground to build the far fight on.
**Not wired to the far brains**: a far body never takes the engaging transition in this
package (`brains.FarCaptain._enemy_within`); this module is run apart, by the truth that
measures it and by whoever tunes it.

A round is `step_s` of the ship's time (three minutes by default: a drilled ship's two
broadsides, a merchantman's one). In a round each ship fires her engaged broadside at the
other: every gun that is mounted and can reach the range fires `step_s / cycle_s` times,
each shot striking with `shot.hit_chance` at the range by the gun's point blank (the
platform steady, the aim an ordinary crew's), and each hit allotted by the aim's shares
(`hits.AIM_SHARES`) to the hull, the deck or the rigging: a hull hit holes her (a share at
or below the waterline) and hurts men by `hits.MEN_HURT_HULL` scaled by the calibre, a deck
hit hurts men and may dismount a gun (`hits.DISMOUNT_AT_WEIGHT`), a rigging hit cuts her
sail by a share and takes a spar with a small chance. Morale is `morale.Morale`'s law on
the sums; the colours come down when it passes the doctrine's line. Deterministic under the
seed given.

The figures a round keeps are what the far state would carry (`world.ships.Vessel.damage`):
the men killed and wounded, the guns dismounted, the shot holes and the share below the
waterline, the sail cut, the spars gone, the rounds fired; and who struck, and when.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any

from freesail.combat import hits as H
from freesail.combat import morale as M
from freesail.combat import shot as S
from freesail.combat.guns import LIGHT_GUN_SHARE_FLOOR, NUMBERS_POWER, PHASES, REFERENCE_CWT
from freesail.ship.loader import load_spec

__all__ = ["FarShip", "Round", "fight", "far_ship"]

# The rigging hit's shares at far detail (judgement, as `hits.RIGGING_SHARES`): the sail
# cut by this share of her canvas a hit; a spar carried away with this chance.
SAIL_CUT_PER_HIT = 0.04
SPAR_PER_RIGGING_HIT = 0.08
# The men hurt at far detail use the near model's means; spent shot beyond twice point
# blank halve them (`hits.py`'s rule).
SPENT_FACTOR = 0.5


@dataclass
class FarShip:
    """One side of the far fight: her guns by kind, pounder and weight; her complement;
    her length; her doctrine's figures; and the sums the rounds write."""

    name: str
    nation: str
    guns: list[tuple[str, float, float]]  # (kind, pounder, weight_cwt) of the engaged side
    complement: int
    length_m: float
    aim: str = "hull"  # hull | rigging | between
    morale_start: float = M.DEFAULT_START
    strike_below: float = M.DEFAULT_STRIKE_BELOW
    # the sums
    killed: int = 0
    wounded: int = 0
    dismounted: int = 0
    holes: int = 0
    holes_below: int = 0
    sail_cut: float = 0.0
    spars_gone: int = 0
    rounds_fired: int = 0
    struck_at_s: float | None = None
    morale: float = field(default=0.0)

    def __post_init__(self) -> None:
        self.morale = self.morale_start

    @property
    def hurt(self) -> int:
        return self.killed + self.wounded

    @property
    def fit(self) -> int:
        return max(0, self.complement - self.hurt)

    @property
    def broadside_lb(self) -> float:
        return sum(p for _k, p, _w in self.guns)


@dataclass
class Round:
    t_s: float
    fired: tuple[int, int]
    struck: tuple[int, int]
    hurt: tuple[int, int]
    morale: tuple[float, float]


def far_ship(ship_file: str, nation: str, fit: str | None = None, **doctrine: Any) -> FarShip:
    """A far side from her ship file (the engaged broadside: one side's guns and the
    chasers), her complement and her length; the doctrine's figures as given."""
    spec = load_spec(ship_file)
    arm = spec.armament
    fs = arm.fit(fit) if arm is not None else None
    guns: list[tuple[str, float, float]] = []
    if fs is not None:
        for g in fs.guns:
            if g.place == "broadside" and g.side != "starboard":
                continue  # one side's guns fire
            guns.append((g.kind, float(g.pounder), float(g.weight_cwt)))
    complement = int(getattr(spec.crew, "complement", 0) or 0)
    length = float(getattr(spec.hull, "length_m", 0.0) or 0.0)
    return FarShip(
        name=spec.name,
        nation=nation,
        guns=guns,
        complement=complement,
        length_m=length,
        aim=str(doctrine.get("aim", "hull")),
        morale_start=float(doctrine.get("morale_start", M.DEFAULT_START)),
        strike_below=float(doctrine.get("strike_below", M.DEFAULT_STRIKE_BELOW)),
    )


def _cycle_s(kind: str, weight_cwt: float) -> float:
    phases = PHASES.get(kind, PHASES["long"])
    total = sum(s for _n, s in phases)
    if kind == "long" and weight_cwt > 0.0:
        total *= max(LIGHT_GUN_SHARE_FLOOR, min(1.0, weight_cwt / REFERENCE_CWT))
    return total


def _crew_factor(ship: FarShip) -> float:
    """The numbers' factor on the cycle: the fit men over the complement, as the near
    bill's crews go short-handed (a crew at half strength serves the gun at half the
    rate; under a third, not at all)."""
    if ship.complement <= 0:
        return 1.0
    share = ship.fit / ship.complement
    if share < 1.0 / 3.0:
        return math.inf
    return (1.0 / share) ** NUMBERS_POWER  # the near battery's law (`guns.NUMBERS_POWER`)


def _shots(ship: FarShip, step_s: float) -> list[tuple[str, float, float, float]]:
    """(kind, pounder, weight, shots this round) for each mounted gun."""
    factor = _crew_factor(ship)
    if not math.isfinite(factor):
        return []
    out = []
    mounted = ship.guns[: max(0, len(ship.guns) - ship.dismounted)]
    for kind, pounder, weight in mounted:
        out.append((kind, pounder, weight, step_s / (_cycle_s(kind, weight) * factor)))
    return out


def _fire(
    firer: FarShip, mark: FarShip, range_m: float, rng: Any, step_s: float
) -> tuple[int, int]:
    """One round of the firer's broadside at the mark: (shots fired, hits)."""
    fired = 0
    struck = 0
    shares = H.AIM_SHARES.get(_aim_of(firer), H.AIM_SHARES[H.Aim.HULL])
    for kind, pounder, weight, n in _shots(firer, step_s):
        b = S.ballistics_of(kind, pounder)
        if range_m > b.random_m:
            continue
        whole = int(n)
        frac = n - whole
        shots = whole + (1 if rng.random() < frac else 0)
        for _ in range(shots):
            fired += 1
            p = S.hit_chance(
                range_m,
                b,
                max(range_m, b.point_blank_m),
                target_length_m=mark.length_m,
                aspect_rad=math.pi / 2.0,
                aim=1.0,
                scatter_deg=0.0,
            )
            if rng.random() >= p:
                continue
            struck += 1
            _allot(mark, pounder, weight, range_m, b, shares, rng)
    firer.rounds_fired += fired
    return fired, struck


def _aim_of(ship: FarShip) -> Any:
    return {"hull": H.Aim.HULL, "rigging": H.Aim.RIGGING, "between": H.Aim.BETWEEN}.get(
        ship.aim, H.Aim.HULL
    )


def _allot(
    mark: FarShip, pounder: float, weight: float, range_m: float, b: Any, shares, rng
) -> None:
    hull, deck, rigging = shares
    scale = pounder / H.REFERENCE_POUNDER
    if range_m > 2.0 * b.point_blank_m:
        scale *= SPENT_FACTOR
    r = rng.random()
    if r < hull:
        mark.holes += 1
        if rng.random() < H.SHOT_HOLE_BELOW_SHARE + (
            H.SHOT_HOLE_BETWEEN_SHARE if mark.aim == "between" else 0.0
        ):
            mark.holes_below += 1
        _men(mark, H.MEN_HURT_HULL * scale, rng)
    elif r < hull + deck:
        _men(mark, H.MEN_HURT_DECK * scale, rng)
        mounted = len(mark.guns) - mark.dismounted
        if mounted > 0 and rng.random() < H.DECK_HIT_ON_A_GUN:
            kind, gp, gw = mark.guns[mounted - 1]
            p = min(0.85, max(0.03, H.DISMOUNT_AT_WEIGHT * pounder / max(gw, 0.5)))
            if rng.random() < p:
                mark.dismounted += 1
    else:
        mark.sail_cut = min(1.0, mark.sail_cut + SAIL_CUT_PER_HIT)
        if rng.random() < SPAR_PER_RIGGING_HIT:
            mark.spars_gone += 1
        _men(mark, H.MEN_HURT_RIGGING * scale, rng)


def _men(mark: FarShip, mean: float, rng: Any) -> None:
    """Men hurt, a Poisson draw on the mean as the near model's (`hits._casualties`),
    capped by the fit men left; the killed share of them."""
    if mean <= 0.0 or mark.fit <= 0:
        return
    n = 0
    threshold = math.exp(-mean)
    p = 1.0
    while True:
        p *= rng.random()
        if p <= threshold:
            break
        n += 1
    n = min(n, mark.fit)
    killed = sum(1 for _ in range(n) if rng.random() < H.KILLED_SHARE)
    mark.killed += killed
    mark.wounded += n - killed


def _judge(ship: FarShip, enemy: FarShip, under_fire: bool) -> float:
    losses = ship.hurt / max(ship.complement, 1)
    guns_lost = ship.dismounted / max(len(ship.guns), 1)
    masts = min(1.0, ship.spars_gone / 3.0) * 0.5  # a spar at far detail is not a lower mast
    odds = 0.0
    if under_fire and enemy.broadside_lb > 0.0:
        ratio = enemy.broadside_lb / max(ship.broadside_lb, 1.0)
        odds = min(M.ODDS_MOST, M.ODDS_WEIGHT * max(0.0, math.log2(max(ratio, 1.0))))
    value = (
        ship.morale_start
        - M.LOSSES_WEIGHT * losses
        - M.GUNS_WEIGHT * guns_lost
        - M.MASTS_WEIGHT * masts
        - odds
    )
    ship.morale = max(0.0, min(1.0, value))
    return ship.morale


def fight(
    a: FarShip,
    b: FarShip,
    range_m: float,
    rng: Any,
    *,
    minutes: float = 120.0,
    step_s: float = 180.0,
) -> list[Round]:
    """The far fight of `a` and `b` at the range, round by round until one strikes or the
    minutes are out; the rounds' record. `rng` is any `random()` source (an `Rng` stream)."""
    rounds: list[Round] = []
    t = 0.0
    fired_on = {a.name: False, b.name: False}
    while t < minutes * 60.0 and a.struck_at_s is None and b.struck_at_s is None:
        t += step_s
        fa, sa = _fire(a, b, range_m, rng, step_s)
        fb, sb = _fire(b, a, range_m, rng, step_s)
        fired_on[b.name] = fired_on[b.name] or fa > 0
        fired_on[a.name] = fired_on[a.name] or fb > 0
        ma = _judge(a, b, fired_on[a.name])
        mb = _judge(b, a, fired_on[b.name])
        if fired_on[a.name] and ma < a.strike_below:
            a.struck_at_s = t
        if fired_on[b.name] and mb < b.strike_below and a.struck_at_s is None:
            b.struck_at_s = t
        rounds.append(Round(t, (fa, fb), (sa, sb), (a.hurt, b.hurt), (ma, mb)))
    return rounds
