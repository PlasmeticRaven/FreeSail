"""Shot: the simple ballistic and the hit chance (spec M7 §9; package 70).

A fired gun produces shot with a range by its kind, calibre and elevation, and a chance
to strike by the range band, the mark's size and aspect, the crew's aim, the roll and the
sea. Every figure here is a judgement set beside its source, as §34 leaves them to this
package, and is tuned in play:

- **Point blank** (the first graze with the gun laid level, Douglas, *A Treatise on Naval
  Gunnery*, 1820, part II): about three to four hundred yards for the long guns, less for
  the small calibres and the carronades (the 12-pounder carronade's about 230 yards, the
  32-pounder's about 330; the long 18-pounder's about 380); **random shot** (the extreme
  range at the quoin's most elevation): the long 18-pounder about a mile, the 32-pounder
  carronade a little over a thousand yards at five degrees (Douglas's tables, from memory
  and UNVERIFIED against a page). The range curve between is a judgement anchored on the
  two.
- **Elevation**: the quoin gives a long gun some ten degrees up and three or four down
  (Douglas; the carriage's); a carronade on its screw about the same; a swivel what its
  man gives it. **The heel adds to the lee battery's depression and the weather battery's
  elevation** (the owner's note 6; the famous reason the gages differ), and the gun answers
  only so far: beyond the quoin's limit the lee gun fires into the water close aboard and
  the weather gun over.
- **A lee port whose sill is within a foot of the water is shut** (`PORT_SHUT_M`), and
  its gun silent: the sill at the gun's `height_m` upright, lowered by the heel over the
  half-beam.
- **The hit chance by band** (judgement; Douglas on the practice: at close range nearly
  every shot tells, at random shot one in twenty or thirty): nine in ten at pistol shot,
  falling to about one in two at point blank, one in five at twice it, a few in a hundred
  at the extreme; times the mark's size (her length against a frigate's) and her aspect
  (end-on a narrow mark), the crew's aim (their mean rating against the ordinary seaman's,
  the untrained merchant crew the worse), and the steadiness of the platform (the roll's
  scatter, halved when the gun captain fires on the roll the doctrine says, and the sea's
  height), each a judgement named in the tuning notes.

Deterministic: the draws are the caller's stream (`World.rng.stream("gunnery")`).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

from freesail import units

__all__ = [
    "BAND_WORDS",
    "PISTOL_SHOT_M",
    "PORT_SHUT_M",
    "Ballistics",
    "ballistics_of",
    "effective_elevation",
    "hit_chance",
    "lee_port_shut",
    "range_at",
    "range_words",
    "steadiness",
]

YARD = 0.9144
# Pistol shot, the period's phrase for a ship within fifty yards (judgement on the usage;
# "within pistol shot" of the logs); musket shot a hundred yards.
PISTOL_SHOT_M = 50.0 * YARD
MUSKET_SHOT_M = 100.0 * YARD
# A lee port whose sill is within this of the water is shut (spec M7 §9: "within a foot").
PORT_SHUT_M = 0.3048


@dataclass(frozen=True)
class Ballistics:
    """A gun's figures: point blank and random shot in metres, the quoin's limits."""

    point_blank_m: float
    random_m: float
    elevation_max_deg: float
    depression_max_deg: float


def ballistics_of(kind: str, pounder: float) -> Ballistics:
    """The figures by kind and calibre (the module's head for the sources)."""
    if kind == "carronade":
        # the 12-pounder's 230 yards and the 32-pounder's 330 (Douglas, from memory): a
        # hundred yards for the doubling and a half of the calibre, judgement between
        pb = 230.0 + 70.0 * math.log2(max(pounder, 1.0) / 12.0)
        far = 800.0 + 200.0 * math.log2(max(pounder, 1.0) / 12.0)  # the 32-pounder's 1,087
        return Ballistics(pb * YARD, far * YARD, 11.0, 5.0)
    if kind == "swivel":
        return Ballistics(100.0 * YARD, 400.0 * YARD, 20.0, 20.0)
    # the long guns: the 3-pounder about 250 yards, the 18-pounder about 380, the
    # 32-pounder about 420 (Douglas, from memory; the curve judgement); random shot a mile
    # for the 18-pounder, less for the small guns
    pb = 250.0 + 50.0 * math.log2(max(pounder, 1.0) / 3.0)
    far = 1200.0 + 310.0 * math.log2(max(pounder, 1.0) / 3.0)  # the 18-pounder's 2,000
    return Ballistics(pb * YARD, far * YARD, 10.0, 4.0)


def range_at(b: Ballistics, elevation_deg: float) -> float:
    """The shot's range at this effective elevation (the quoin's and the heel's together):
    point blank level, the random shot at the quoin's most, and depressed into the water
    short of point blank; beyond the limits, the limit's range (the gun cannot be laid
    further)."""
    e = max(-b.depression_max_deg, min(b.elevation_max_deg, elevation_deg))
    if e >= 0.0:
        return b.point_blank_m + (b.random_m - b.point_blank_m) * (e / b.elevation_max_deg) ** 0.9
    # depressed: the shot strikes the water short, a fifth of point blank at the most
    # depression (judgement)
    share = 1.0 + 0.8 * (e / b.depression_max_deg)
    return max(0.0, b.point_blank_m * share)


def effective_elevation(gun_elevation_deg: float, heel_deg: float, lee_side: bool) -> float:
    """The quoin's elevation with the heel added: the lee battery depressed by the heel,
    the weather battery raised (spec M7 §9)."""
    return gun_elevation_deg - heel_deg if lee_side else gun_elevation_deg + heel_deg


def lee_port_shut(sill_height_m: float, heel_deg: float, half_beam_m: float) -> bool:
    """Whether a lee port is shut: its sill, lowered by the heel over the half-beam,
    within `PORT_SHUT_M` of the water."""
    lowered = sill_height_m - half_beam_m * math.sin(math.radians(abs(heel_deg)))
    return lowered <= PORT_SHUT_M


def steadiness(roll_deg: float, sea_height_m: float, on_the_roll: bool) -> float:
    """The platform's scatter in degrees of elevation: the roll's amplitude (half of it
    when the gun captain fires on the roll the doctrine names: the up-roll for the rigging,
    the down-roll for the hull; judgement) and the sea's height (half a degree a metre;
    judgement)."""
    roll = roll_deg * (0.5 if on_the_roll else 1.0)
    return roll + 0.5 * max(0.0, sea_height_m)


def hit_chance(
    range_m: float,
    b: Ballistics,
    reach_m: float,
    *,
    target_length_m: float,
    aspect_rad: float,
    aim: float,
    scatter_deg: float,
    size: float | None = None,
) -> float:
    """The chance one shot strikes the mark (the module's head). `reach_m` is the range
    the gun's effective elevation gives (`range_at`): a shot that falls short strikes
    nothing, and one laid to carry far beyond the mark goes high (through the rigging or
    over, which `hits.py` reads as a hit on the rigging where it is a hit at all).
    `aspect_rad` is the mark's heading against the line of fire (0 end-on, pi/2 beam-on);
    `aim` the crew's mean deck skill over the ordinary seaman's; `scatter_deg` from
    `steadiness`. `size`, when given, is the mark's size term in place of the hull's (a
    cask's, below the hull's floor: practice and resupply, between packages 72 and 73;
    `combat.marks.CASK_SIZE`); None keeps the hull's, and every figure as it was."""
    if range_m <= 0.0 or reach_m <= 0.0:
        return 0.0
    if range_m > reach_m * 1.05 or range_m > b.random_m:
        return 0.0  # short of her, or beyond the gun's throw
    r = range_m / b.point_blank_m
    if r <= 0.25:
        base = 0.9
    elif r <= 1.0:
        base = 0.9 - 0.4 * (r - 0.25) / 0.75  # 0.5 at point blank
    elif r <= 2.0:
        base = 0.5 - 0.3 * (r - 1.0)  # 0.2 at twice point blank
    else:
        rmax = max(b.random_m / b.point_blank_m, 2.5)
        base = max(0.03, 0.2 * (1.0 - (r - 2.0) / (rmax - 2.0)))
    if size is None:
        size = min(1.3, max(0.5, math.sqrt(max(target_length_m, 5.0) / 40.0)))
    aspect = 0.6 + 0.4 * abs(math.sin(aspect_rad))
    quality = min(1.2, max(0.6, aim))
    steady = 1.0 / (1.0 + 0.05 * max(0.0, scatter_deg) * max(r, 0.5))
    return min(0.98, base * size * aspect * quality * steady)


# The bands in the period's words, for the log (judgement on the usage).
BAND_WORDS: tuple[tuple[float, str], ...] = (
    (PISTOL_SHOT_M, "pistol shot"),
    (MUSKET_SHOT_M, "musket shot"),
    (units.CABLE * 0.5, "half a cable"),
    (units.CABLE * 1.5, "a cable"),
)


def range_words(range_m: float) -> str:
    """'pistol shot', 'musket shot', 'half a cable', 'a cable', 'three cables', 'a mile and
    a half', 'two miles'."""
    for limit, words in BAND_WORDS:
        if range_m <= limit:
            return words
    cables = range_m / units.CABLE
    if cables < 9.5:
        return f"{int(round(cables))} cables"
    miles = range_m / units.NAUTICAL_MILE
    half = round(miles * 2) / 2
    if half == 1.0:
        return "a mile"
    if half == 1.5:
        return "a mile and a half"
    return f"{half:g} miles"


def aspect_of(target_heading_rad: float, bearing_from_target_rad: float) -> float:
    """The mark's aspect to a shot coming from `bearing_from_target_rad` (true): the
    angle between her head and the line of fire, 0 end-on, pi/2 beam-on."""
    rel = abs(units.wrap_pi(bearing_from_target_rad - target_heading_rad))
    return rel if rel <= math.pi / 2 else math.pi - rel


def aim_of(hands: list[Any]) -> float:
    """The crew's aim: their mean deck skill over the ordinary seaman's (`RATING_SKILL`);
    an empty crew the ordinary's."""
    from freesail.crew.model import RATING_SKILL, Rating

    reference = RATING_SKILL[Rating.ORDINARY][0]
    if not hands:
        return 1.0
    return sum(float(getattr(s, "skill_deck", reference)) for s in hands) / len(hands) / reference
