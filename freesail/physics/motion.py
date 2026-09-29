"""The ship's motion in a seaway (spec M5 §4; `docs/design/ThreeDimensions.md`): three
reduced quantities, roll, pitch and heave, each a number with a time constant. No
six-degree body is integrated, no wave is followed; nothing here moves the ship on the
plane. It is what the hands and the gear feel.

**Roll** comes from the sea on the beam against the ship's stability: the significant
wave's slope, magnified by how near the sea's period lies to the ship's own roll period
(a driven oscillator, `ROLL_DAMPING`), scaled by how much of the sea is on the beam and
by `MOTION_GAIN` for the heaviest waves of a train, and capped. The roll period is the
ship's natural one, from her beam and her metacentric height (`ROLL_GYRATION_OF_BEAM`).
**Pitch** comes from the sea ahead or astern: the slope again, by how much of the sea is
on the bow, and by how long the waves are against the ship (a ship does not pitch to a
sea shorter than herself, `PITCH_WAVE_LENGTHS`). **Heave** is half the wave's height by
the same length rule. A swell drives each with its own bearing and period, and the two
trains add as squares.

**Consequences**, each one line where it lands: the crew factor aloft by the roll
(`crew.hands.seaway_factor`); the strain model's load factor on spars and gear
(`load_factor`; `physics.strain.apply_strain`); the hull's added resistance in a head sea
(`resistance_factor`; `physics.integrate`); the glass pumping (`pumping`;
`world.weather.Glass.read`); the sights' error (`sight_error_factor`, inert until 5b).

The words (`words`, `state`) are the period's: easy; rolling easily, rolling, rolling
heavily; pitching a little, pitching into it, pitching heavily into it; labouring heavily
when both are heavy (Falconer 1780, "Rolling", "Sea-boat" ("without labouring heavily, or
straining her masts and rigging"); Luce 1884, "In a Gale" ("when a vessel labors much in a
seaway"; "if the pitching is hard and quick"), and "the ship is rolling heavily" in his
boat chapter).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

from freesail import units
from freesail.world.sea import CROSS_SEA_POINTS, SMOOTH_UNDER_M

__all__ = [
    "HEAD_SEA_RESISTANCE_PER_M",
    "MOTION_GAIN",
    "MOTION_STATE_WORDS",
    "MOTION_TIME_CONSTANT_S",
    "Motion",
    "MotionReading",
    "PITCH_HEAVY_DEG",
    "ROLL_DAMPING",
    "ROLL_HEAVY_DEG",
    "ROLL_MAX_DEG",
    "STRAIN_PITCH_PER_DEG",
    "STRAIN_ROLL_PER_DEG",
    "Particulars",
]

# ---------------------------------------------------------------------------
# Constants (docs/dev/TuningNotes.md, M5a: the motion)
# ---------------------------------------------------------------------------

# The natural roll period: T = 2 pi k / sqrt(g GM) with the transverse radius of gyration
# k a fraction of the beam (the naval architect's rule of thumb, 0.35 to 0.40 of the beam
# for a laden ship; the "Weiss formula" T = 0.8 B / sqrt(GM) is the same at 0.40; not
# read from a text in this package, unverified). The frigate (beam 11.7 m, GM 1.3 m):
# 8.2 s; the schooner (7.3 m, 1.0 m): 5.8 s.
ROLL_GYRATION_OF_BEAM = 0.40
# The roll's damping ratio as the driven oscillator reads it. A bare hull of 1805 (no
# bilge keels) is lightly damped, textbook values 0.05 to 0.15 (unverified), but the sea
# is not one wave: its periods spread about the peak, and a reduced model with one period
# must carry that spread here, so the ratio is set at a fifth, a magnification of two and
# a half at resonance (judgement; a regular wave's five would roll her on her beam ends
# in a moderate sea, which the period's logs do not report).
ROLL_DAMPING = 0.20
# The roll a captain names is the heavier rolls of the watch, not the significant: the
# highest tenth of a train's waves are 1.27 times the significant height (the Rayleigh
# distribution of wave heights, the standard result; unverified against a page here).
# Applied to the roll, the pitch and the heave alike.
MOTION_GAIN = 1.27
ROLL_MAX_DEG = 35.0
# A ship rolls some in a following sea, on the quarter: the share of the beam's roll a
# sea right ahead or astern still gives (judgement).
ROLL_OFF_BEAM_SHARE = 0.3
# A ship pitches fully to waves this many times her waterline length and long, and
# hardly to waves shorter than herself (judgement; the shape of the pitch response).
PITCH_WAVE_LENGTHS = 2.0
# The motions build and die over a dozen periods (judgement): the time constant of the
# reduced quantities.
MOTION_TIME_CONSTANT_S = 90.0

# The words turn here (judgement: a frigate's lee ports are near the water at twelve
# degrees of roll to each side, her lee guns under at twenty; a pitch of seven degrees
# puts the bowsprit into it).
ROLL_EASY_DEG = 3.0
ROLL_ROLLING_DEG = 6.0
ROLL_HEAVY_DEG = 12.0
PITCH_EASY_DEG = 2.0
PITCH_HEAVY_DEG = 7.0

# The strain model's extra load by the motion (spec M5 §4; Luce 1884, 'In a Gale': "when
# a vessel labors much in a seaway ... the [jerk] of the masts will either carry away the
# braces and sheets or spring the yards"; "by forcing her through a head sea, you strain
# every mast and yard"): a factor on the wind's load on spars and gear, judgement, with
# a dead band so that a smooth sea changes nothing (the strain truths are measured
# without a sea): twenty degrees of roll adds a fifth, ten of pitch about an eighth;
# capped at two fifths. Set so that the gate's day under systems costs the frigate
# canvas in the squalls of the gale and no spar before it (docs/dev/TuningNotes.md, M5a).
STRAIN_ROLL_PER_DEG = 0.01
STRAIN_PITCH_PER_DEG = 0.015
STRAIN_DEAD_BAND_DEG = 2.0
STRAIN_FACTOR_MAX = 1.4

# The hull's added resistance in a head sea (spec M5 §4): a fraction per metre of
# combined significant height above a smooth sea's (`sea.SMOOTH_UNDER_M`, so that a
# smooth sea adds nothing) on the bow, by the square of the cosine of the sea's angle on
# the bow (judgement bounded by the involuntary speed loss of small ships in head seas as
# the modern rules of thumb give it, a tenth to a quarter in Beaufort six to seven,
# unverified; Luce: "by forcing her through a head sea ..."). A three-metre head sea adds
# a quarter to the resistance, which costs about a tenth of the speed.
HEAD_SEA_RESISTANCE_PER_M = 0.10

# The glass pumps in a seaway by "a hundredth or two" (W §3): the reading noise
# (`weather.GLASS_NOISE_IN`, half a hundredth) grows by this per degree of roll and
# pitch together, to the glass's own cap (`weather.GLASS_PUMP_MAX_IN`, two hundredths):
# ten degrees of motion doubles and a half the noise, twenty reaches the cap.
GLASS_PUMP_PER_DEG = 0.15

# The sights' error grows with the motion (spec M5 §14: "the sea state"): a factor 5b's
# noon sight and lunar read, one on a quiet day and about three in a heavy seaway
# (judgement from the study's "a quarter of a degree for a good master on a quiet day, a
# degree ... in a seaway", N §5). Inert until then.
SIGHT_ERROR_PER_DEG = 0.1

MOTION_STATE_WORDS: tuple[str, ...] = ("easy", "rolling", "pitching", "labouring")


# ---------------------------------------------------------------------------
# The ship's particulars the motion needs
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Particulars:
    """What the motion reads of the hull: the beam, the metacentric height and the
    waterline length. The defaults stand in for a ship without a hull (the point ship of
    the early milestones): the frigate's."""

    beam_m: float = 11.7
    gm_m: float = 1.3
    length_m: float = 41.8

    @classmethod
    def of(cls, ship: Any) -> Particulars:
        hull = getattr(ship, "hull", None)
        spec = getattr(hull, "spec", None)
        if spec is None:
            return cls()
        return cls(
            beam_m=float(spec.beam_m),
            gm_m=float(spec.gm_m),
            length_m=float(spec.length_waterline_m),
        )

    @property
    def roll_period_s(self) -> float:
        k = ROLL_GYRATION_OF_BEAM * self.beam_m
        gm = max(self.gm_m, 0.05)
        return 2.0 * math.pi * k / math.sqrt(units.G * gm)


# ---------------------------------------------------------------------------
# The reading
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MotionReading:
    words: str
    state: str  # one of MOTION_STATE_WORDS
    heavy: bool
    roll_deg: float
    roll_period_s: float
    pitch_deg: float
    heave_m: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "words": self.words,
            "state": self.state,
            "heavy": self.heavy,
            "roll_deg": round(self.roll_deg, 1),
            "roll_period_s": round(self.roll_period_s, 1),
            "pitch_deg": round(self.pitch_deg, 1),
            "heave_m": round(self.heave_m, 2),
        }


def motion_words(
    roll_deg: float, pitch_deg: float, following: bool = False
) -> tuple[str, str, bool]:
    """(words, state, heavy) for a roll and a pitch amplitude in degrees; `following`
    when the sea that pitches her is from abaft the beam (she pitches with the sea under
    her stern, Falconer's "sending ... into the hollow", not into it)."""
    rolling = roll_deg >= ROLL_EASY_DEG
    pitching = pitch_deg >= PITCH_EASY_DEG
    roll_heavy = roll_deg >= ROLL_HEAVY_DEG
    pitch_heavy = pitch_deg >= PITCH_HEAVY_DEG
    if roll_heavy and pitch_heavy:
        return "labouring heavily", "labouring", True
    if not rolling and not pitching:
        return "easy", "easy", False
    # the greater against its own scale leads
    if roll_deg / ROLL_HEAVY_DEG >= pitch_deg / PITCH_HEAVY_DEG:
        if roll_heavy:
            return "rolling heavily", "rolling", True
        if roll_deg >= ROLL_ROLLING_DEG:
            return "rolling", "rolling", False
        return "rolling easily", "rolling", False
    where = ", the sea under her stern" if following else " into it"
    if pitch_heavy:
        return f"pitching heavily{where}", "pitching", True
    if pitch_deg >= 0.5 * PITCH_HEAVY_DEG:
        return f"pitching{where}", "pitching", False
    return "pitching a little", "pitching", False


# ---------------------------------------------------------------------------
# The motion
# ---------------------------------------------------------------------------


def _slope_deg(height_m: float, period_s: float) -> float:
    """The significant wave's maximum slope in degrees: pi H / L with L = g T^2 / 2 pi."""
    if height_m <= 0.0 or period_s <= 0.0:
        return 0.0
    length = units.G * period_s * period_s / (2.0 * math.pi)
    return units.rad_to_deg(math.pi * height_m / length)


def _wave_length(period_s: float) -> float:
    return units.G * period_s * period_s / (2.0 * math.pi)


class Motion:
    """The ship's reduced motion: roll, pitch and heave, relaxed toward what the sea
    gives on her heading. `tick` every tick; the readers below."""

    def __init__(self, particulars: Particulars):
        self.particulars = particulars
        self.roll_deg = 0.0
        self.pitch_deg = 0.0
        self.heave_m = 0.0
        self.roll_period_s = particulars.roll_period_s
        # the sea's angle on the bow that the last tick read, for the head-sea factor
        self._head_sea_m = 0.0
        self._following = False  # the sea from abaft the beam

    # -- the targets ---------------------------------------------------------

    def _train(
        self, height_m: float, period_s: float, from_rad: float, heading: float
    ) -> tuple[float, float, float]:
        """(roll, pitch, heave) one wave train would give: the slope magnified for the
        roll, the length rule for the pitch and the heave."""
        if height_m <= 0.0:
            return 0.0, 0.0, 0.0
        slope = _slope_deg(height_m, period_s)
        # the sea's angle on the bow: 0 right ahead, pi right astern
        bearing = units.relative_bearing(heading, from_rad)
        on_beam = abs(math.sin(bearing))
        on_bow = abs(math.cos(bearing))
        # roll: a driven oscillator at the ratio of the ship's period to the wave's
        r = self.roll_period_s / period_s
        magnification = 1.0 / math.sqrt((1.0 - r * r) ** 2 + (2.0 * ROLL_DAMPING * r) ** 2)
        beam_share = ROLL_OFF_BEAM_SHARE + (1.0 - ROLL_OFF_BEAM_SHARE) * on_beam
        roll = min(ROLL_MAX_DEG, MOTION_GAIN * slope * magnification * beam_share)
        # pitch and heave: by the wave's length against the ship's
        length_share = min(
            1.0, _wave_length(period_s) / (PITCH_WAVE_LENGTHS * self.particulars.length_m)
        )
        pitch = MOTION_GAIN * slope * on_bow * length_share
        heave = MOTION_GAIN * 0.5 * height_m * length_share
        return roll, pitch, heave

    def targets(self, sea: Any, heading: float) -> tuple[float, float, float]:
        """What the sea gives on this heading: the wind sea's train and the swell's. A
        swell running with the wind sea is the same water (the greater of the two, as the
        sea's words count it); one crossing it is a second train, and the two add as
        squares."""
        r = sea.reading()
        a = self._train(r.sea_m, sea.sea_period_s, r.sea_from_rad, heading)
        b = self._train(r.swell_m, r.swell_period_s, r.swell_from_rad, heading)
        crossing = abs(units.wrap_pi(r.swell_from_rad - r.sea_from_rad)) > units.points_to_rad(
            CROSS_SEA_POINTS
        )
        if crossing:
            return math.hypot(a[0], b[0]), math.hypot(a[1], b[1]), math.hypot(a[2], b[2])
        return max(a[0], b[0]), max(a[1], b[1]), max(a[2], b[2])

    # -- the tick ---------------------------------------------------------------

    def tick(self, dt: float, sea: Any, heading: float) -> None:
        roll, pitch, heave = self.targets(sea, heading)
        k = 1.0 - math.exp(-dt / MOTION_TIME_CONSTANT_S)
        self.roll_deg += (roll - self.roll_deg) * k
        self.pitch_deg += (pitch - self.pitch_deg) * k
        self.heave_m += (heave - self.heave_m) * k
        # the sea on the bow, for the hull's added resistance: the combined height by the
        # square of the cosine of its angle on the bow (nothing from abaft the beam)
        r = sea.reading()
        bearing = units.relative_bearing(heading, r.from_rad)
        c = math.cos(bearing)
        over_smooth = max(0.0, r.height_m - SMOOTH_UNDER_M)  # a smooth sea adds nothing
        self._head_sea_m = over_smooth * c * c if c > 0.0 else 0.0
        self._following = c < 0.0

    # -- the readers: each consequence reads one number here -------------------------

    @property
    def load_factor(self) -> float:
        """The strain model's factor on the wind's load on spars and gear: 1.0 in a smooth
        sea (the dead band), rising with the roll and the pitch to STRAIN_FACTOR_MAX."""
        roll = max(0.0, self.roll_deg - STRAIN_DEAD_BAND_DEG)
        pitch = max(0.0, self.pitch_deg - STRAIN_DEAD_BAND_DEG)
        if roll == 0.0 and pitch == 0.0:
            return 1.0
        return min(
            STRAIN_FACTOR_MAX, 1.0 + STRAIN_ROLL_PER_DEG * roll + STRAIN_PITCH_PER_DEG * pitch
        )

    @property
    def resistance_factor(self) -> float:
        """The hull's factor on its resistance ahead in a head sea."""
        return 1.0 + HEAD_SEA_RESISTANCE_PER_M * self._head_sea_m

    @property
    def pumping(self) -> float:
        """The factor on the glass's reading noise: 1.0 at rest; the glass caps the
        product at its two hundredths (`weather.Glass.read`)."""
        return 1.0 + GLASS_PUMP_PER_DEG * (self.roll_deg + self.pitch_deg)

    @property
    def sight_error_factor(self) -> float:
        """The factor on a sight's error (spec M5 §14); read by nothing until 5b."""
        return 1.0 + SIGHT_ERROR_PER_DEG * (self.roll_deg + self.pitch_deg)

    def reading(self) -> MotionReading:
        words, state, heavy = motion_words(self.roll_deg, self.pitch_deg, self._following)
        return MotionReading(
            words=words,
            state=state,
            heavy=heavy,
            roll_deg=self.roll_deg,
            roll_period_s=self.roll_period_s,
            pitch_deg=self.pitch_deg,
            heave_m=self.heave_m,
        )

    @property
    def words(self) -> str:
        return self.reading().words
