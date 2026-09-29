"""The sea state at the ship (spec M5 §4; `docs/design/ThreeDimensions.md`, "sea state as a
field ... tied to the wind's history"): a reduced model, never a wave field.

**The wind sea.** A significant wave height and a period, raised by the wind's ten-minute
mean (`physics.wind.WindRecord`) and read once a simulated minute. The height the wind
would raise given time is the fully developed sea of Pierson and Moskowitz (1964),
`SEA_FULL_M_PER_MS2` times the square of the wind at ten metres; the sea moves toward it
by a first-order lag, `SEA_BUILD_HOURS` when the wind is raising it and `SEA_DECAY_HOURS`
when the wind has dropped. The sea is kept as a vector and the wind sea is its part along
the wind now, so a sea the wind has turned away from is no longer the wind's (it is the
swell the record keeps) and a shift of the wind sees its sea die as the new one builds.
The period comes from the height by the open-sea relation, `SEA_PERIOD_PER_ROOT_M` times
the root of the height.

**The swell.** What a low leaves behind (Falconer 1780, "Swell": "the fluctuating motion of
the sea, which remains after the expiration of a storm"): the wind sea is recorded once
an hour for a day, and the swell is the strongest of those entries decayed over
`SWELL_DECAY_HOURS`, with the direction it had and a longer period than a wind sea's. A
swell that runs with the wind sea is the same water and the greater of the two counts;
one that crosses it by more than `CROSS_SEA_POINTS` makes a confused sea and their
energies add.

**The words** (`words`, `state`): the period's, never the Douglas numbers (the Douglas
scale is 1921; W §3, S28): a smooth sea, a moderate sea, a short chopping sea, a heavy
sea, a very heavy sea; a long swell from the westward, a heavy swell; a confused sea. The
sources are in `SEA_WORDS_SOURCES` and in `docs/primer/09-the-glass-and-the-sky.md`.

Deterministic: nothing here draws from a stream; the same wind gives the same sea, so a
replay gives the same lines. Nothing is saved: a replay raises the sea again from the wind.
The lookout's horizon (`horizon_nm`) is the hook 5b's sighting reads; inert until then.
"""

from __future__ import annotations

import math
from collections import deque
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any

from freesail import units

__all__ = [
    "CROSS_SEA_POINTS",
    "SEA_BUILD_HOURS",
    "SEA_DECAY_HOURS",
    "SEA_FULL_M_PER_MS2",
    "SEA_PERIOD_PER_ROOT_M",
    "SEA_STATE_WORDS",
    "SEA_TICK_S",
    "SEA_WORDS_SOURCES",
    "SWELL_DECAY_HOURS",
    "SWELL_PERIOD_PER_ROOT_M",
    "Sea",
    "SeaReading",
    "quarter_words",
    "sea_state_word",
]

# ---------------------------------------------------------------------------
# Constants, each with its source (docs/dev/TuningNotes.md, M5a: the sea)
# ---------------------------------------------------------------------------

# The fully developed sea for a wind at ten metres: Hs = 0.0247 U10^2 (metres, metres a
# second). Worked here from the Pierson-Moskowitz spectrum's published constants (alpha
# 8.1e-3, beta 0.74, the peak at 0.877 g / U19.5; Pierson and Moskowitz 1964, as WMO-No.
# 702, *Guide to Wave Analysis and Forecasting*, reproduces it): Hs = 4 sqrt(m0) with
# m0 = alpha U^4 / (4 beta g^2) gives 0.0213 U19.5^2, and U19.5 = 1.076 U10 by the power
# law the wind model already uses (`Wind.SHEAR_EXPONENT` 0.11). The derivation was checked
# here; the sources themselves were not read in this package (unverified against the
# page; said so in the tuning notes). Fifteen knots gives 1.5 m, thirty 5.9 m, forty-five
# 13 m, the last a limit a Channel gale of a night does not reach (the lag below).
SEA_FULL_M_PER_MS2 = 0.0247

# The lag toward that height. Judgements bounded by the duration-limited growth of the
# Bretschneider and JONSWAP relations as textbooks give them (a sea of twenty knots fully
# developed in about ten hours, one of forty knots in a day and more; unverified here):
# a build of six hours brings a sea to 63 per cent of its limit in six hours and nine
# tenths in a night; a wind sea dies faster than it grows, its short steep crests going
# first, and the long crests it leaves are the swell below.
SEA_BUILD_HOURS = 6.0
SEA_DECAY_HOURS = 4.0

# The period from the height, seconds per root metre. The fully developed relation is
# 5.0 (from Tp = 0.785 U10 and Hs = 0.0247 U10^2, the same spectrum); a sea still growing
# is steeper, JONSWAP's young seas nearer 3.6 (unverified here). A judgement between
# them for the wind sea (a steepness of one in twenty-five, the significant wave's slope
# seven degrees); the swell, which has lost its steepness, longer (one in fifty-seven).
SEA_PERIOD_PER_ROOT_M = 4.0
SWELL_PERIOD_PER_ROOT_M = 6.0

# The swell decays over a day (the brief; Falconer's swell "remains after the expiration
# of a storm"): its scale, so that a gale's sea is a third of itself half a day on and a
# seventh after a day. Judgement.
SWELL_DECAY_HOURS = 12.0
# The record is kept two days, by which a swell is a fiftieth of itself, so that it goes
# out by its decay and not by the record's end.
SWELL_RECORD_HOURS = 48.0
SWELL_RECORD_STEP_S = 3600

# A swell that crosses the wind sea by more than this makes a confused sea (judgement:
# five points, beyond a cold front's veer of four, so that the sea a front leaves is the
# same water turned and not a cross sea; past that the two trains are plainly two).
CROSS_SEA_POINTS = 5.0

# The sea is read once a simulated minute (spec M5 §4).
SEA_TICK_S = 60

# The share of the wind's full sea the day opens on, as if the wind had blown
# SEA_BUILD_HOURS already: 1 - 1/e (judgement: a scenario opens on a sea already up, not
# on a millpond under a gale).
SEA_START_SHARE = 1.0 - math.exp(-1.0)

# The heights the words turn on, in metres of the combined significant height
# (judgement, laid beside the Douglas bands the words stand where the game never says
# a number: smooth under half a metre; moderate to a metre and a half; a short
# chopping sea to two and a half; heavy to six; very heavy above). A swell counts as a
# swell from a metre.
SMOOTH_UNDER_M = 0.5
MODERATE_UNDER_M = 1.5
SHORT_UNDER_M = 2.5
HEAVY_UNDER_M = 6.0
SWELL_FROM_M = 1.0
# A swell is the sea's word when it stands this much above the wind sea (judgement).
SWELL_DOMINANT_RATIO = 1.5

# The state words the dialect compares (`when the sea is heavy`), in rising order.
SEA_STATE_WORDS: tuple[str, ...] = ("smooth", "moderate", "short", "heavy", "very heavy")

# Where the words come from (the period's; `docs/references/`):
SEA_WORDS_SOURCES: dict[str, str] = {
    "a smooth sea": "Luce 1884, 'In a Gale' ('as taut as in a smooth sea'); Luce 1884, "
    "'Getting Under Way' ('a light breeze with a smooth sea')",
    "a short sea": "Falconer 1780, 'Sea' ('a short sea is when they run irregularly, broken, "
    "and interrupted')",
    "a short chopping sea": "the spec's phrase (M5 §4) from the period's logs; 'chopping' is "
    "not in the repository's references (unverified); Falconer's 'short sea' is",
    "a heavy sea": "Falconer 1780, 'Sea' ('a heavy sea broke over our quarter'); Luce 1884, "
    "'In a Gale' ('in a gale, with a heavy sea, vessels lying to')",
    "a great sea": "Falconer 1780, 'Sea' ('there is a great sea in the offing')",
    "a long swell": "Falconer 1780, 'Sea' ('a long sea implies an uniform and steady motion "
    "of long and extensive waves') and 'Swell'",
    "a heavy swell": "Luce 1884, 'The Weather' ('a heavy swell or confused agitation of the "
    "sea not accounted for in any other way')",
    "a confused sea": "Luce 1884, 'The Weather', the same line",
    "a head sea": "Luce 1884, 'In a Gale' ('by forcing her through a head sea, you strain "
    "every mast and yard'); Falconer 1780, 'Sea' ('to head the sea')",
}


# ---------------------------------------------------------------------------
# Words
# ---------------------------------------------------------------------------

_QUARTERS = (
    "the northward",
    "the north-eastward",
    "the eastward",
    "the south-eastward",
    "the southward",
    "the south-westward",
    "the westward",
    "the north-westward",
)


def quarter_words(direction_from: float) -> str:
    """'the westward', 'the north-westward': the nearest of eight quarters, as a log names
    where a swell comes from."""
    i = int(round(units.rad_to_deg(direction_from) % 360.0 / 45.0)) % 8
    return _QUARTERS[i]


def sea_state_word(height_m: float) -> str:
    """The state word for a combined significant height: smooth, moderate, short, heavy,
    very heavy."""
    if height_m < SMOOTH_UNDER_M:
        return "smooth"
    if height_m < MODERATE_UNDER_M:
        return "moderate"
    if height_m < SHORT_UNDER_M:
        return "short"
    if height_m < HEAVY_UNDER_M:
        return "heavy"
    return "very heavy"


def _base_phrase(state: str) -> str:
    return {
        "smooth": "a smooth sea",
        "moderate": "a moderate sea",
        "short": "a short chopping sea",
        "heavy": "a heavy sea",
        "very heavy": "a very heavy sea",
    }[state]


@dataclass(frozen=True)
class SeaReading:
    """The sea as the registry reads it: the words, the state word the dialect compares,
    and the numbers behind them (5b's sights and the lookout read the numbers)."""

    words: str
    state: str  # one of SEA_STATE_WORDS
    confused: bool
    height_m: float  # the combined significant height
    period_s: float  # the wind sea's, or the swell's when it is the sea
    from_rad: float  # where the dominant train comes from
    sea_m: float  # the wind sea alone
    sea_from_rad: float
    swell_m: float
    swell_from_rad: float
    swell_period_s: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "words": self.words,
            "state": self.state,
            "confused": self.confused,
            "height_m": round(self.height_m, 2),
            "period_s": round(self.period_s, 1),
            "from": self.from_rad,
            "sea_m": round(self.sea_m, 2),
            "swell_m": round(self.swell_m, 2),
            "swell_from": self.swell_from_rad,
            "swell_period_s": round(self.swell_period_s, 1),
        }


# ---------------------------------------------------------------------------
# The sea
# ---------------------------------------------------------------------------


class Sea:
    """The sea at the ship: the sea as a vector of significant height, of which the part
    along the wind is the wind sea; the hourly record the swell is read from; and the
    words. `tick` once a minute with the wind's ten-minute mean; `reading` at any time."""

    def __init__(self, start: datetime, mean_speed_ms: float, mean_from_rad: float):
        self.start = start
        self.now = start
        self.wind_from = units.wrap_2pi(mean_from_rad)
        full = SEA_FULL_M_PER_MS2 * mean_speed_ms * mean_speed_ms
        h0 = SEA_START_SHARE * full
        self._hx = h0 * math.sin(mean_from_rad)
        self._hy = h0 * math.cos(mean_from_rad)
        self._record: deque[tuple[datetime, float, float]] = deque()
        self._record.append((start, h0, self.wind_from))
        self._last_record = start
        self._reading: SeaReading | None = None

    # -- the wind sea -------------------------------------------------------

    @property
    def vector_m(self) -> float:
        """The whole sea vector's height: what the wind has raised, whatever it has
        turned to since."""
        return math.hypot(self._hx, self._hy)

    @property
    def vector_from(self) -> float:
        if self._hx == 0.0 and self._hy == 0.0:
            return self.wind_from
        return units.wrap_2pi(math.atan2(self._hx, self._hy))

    @property
    def sea_m(self) -> float:
        """The wind sea: the part of the sea vector that runs with the wind now. What the
        wind has turned away from is not the wind's sea any more but the swell the record
        keeps, so a shift of the wind sees its sea die as the new one builds."""
        return max(0.0, self._hx * math.sin(self.wind_from) + self._hy * math.cos(self.wind_from))

    @property
    def sea_from(self) -> float:
        return self.wind_from

    @property
    def sea_period_s(self) -> float:
        return SEA_PERIOD_PER_ROOT_M * math.sqrt(self.sea_m)

    def tick(self, when: datetime, mean_speed_ms: float, mean_from_rad: float) -> None:
        """Advance the sea to `when` under the wind's ten-minute mean: the lag toward the
        wind's full sea, build or decay, as a vector; the hourly record kept."""
        dt_h = max((when - self.now).total_seconds(), 0.0) / 3600.0
        self.now = when
        self.wind_from = units.wrap_2pi(mean_from_rad)
        if dt_h > 0.0:
            full = SEA_FULL_M_PER_MS2 * mean_speed_ms * mean_speed_ms
            tx, ty = full * math.sin(mean_from_rad), full * math.cos(mean_from_rad)
            tau = SEA_BUILD_HOURS if full > self.sea_m else SEA_DECAY_HOURS
            k = 1.0 - math.exp(-dt_h / tau)
            self._hx += (tx - self._hx) * k
            self._hy += (ty - self._hy) * k
        if (when - self._last_record).total_seconds() >= SWELL_RECORD_STEP_S:
            self._record.append((when, self.vector_m, self.vector_from))
            self._last_record = when
            horizon = timedelta(hours=SWELL_RECORD_HOURS)
            while self._record and when - self._record[0][0] > horizon:
                self._record.popleft()
        self._reading = None

    # -- the swell ----------------------------------------------------------

    def swell(self) -> tuple[float, float]:
        """(height m, from rad) of the swell: the strongest hour of the last day's record,
        decayed over SWELL_DECAY_HOURS from its hour."""
        best_h, best_from = 0.0, 0.0
        for at, h, from_rad in self._record:
            age_h = max((self.now - at).total_seconds(), 0.0) / 3600.0
            value = h * math.exp(-age_h / SWELL_DECAY_HOURS)
            if value > best_h:
                best_h, best_from = value, from_rad
        return best_h, best_from

    # -- the reading ---------------------------------------------------------

    def reading(self) -> SeaReading:
        if self._reading is not None:
            return self._reading
        sea_m, sea_from, sea_t = self.sea_m, self.sea_from, self.sea_period_s
        swell_m, swell_from = self.swell()
        swell_t = SWELL_PERIOD_PER_ROOT_M * math.sqrt(swell_m)
        crossing = abs(units.wrap_pi(swell_from - sea_from)) > units.points_to_rad(CROSS_SEA_POINTS)
        a_swell = swell_m >= SWELL_FROM_M and swell_m > sea_m * 1.0001
        if a_swell and crossing and sea_m >= SMOOTH_UNDER_M:
            height = math.hypot(sea_m, swell_m)
            confused = True
        else:
            height = max(sea_m, swell_m)
            confused = False
        state = sea_state_word(height)
        swell_leads = a_swell and swell_m >= SWELL_DOMINANT_RATIO * sea_m
        if confused:
            heavy = "heavy " if state in ("heavy", "very heavy") else ""
            words = f"a {heavy}confused sea, the swell from {quarter_words(swell_from)}"
            from_rad, period = (swell_from, swell_t) if swell_m >= sea_m else (sea_from, sea_t)
        elif swell_leads:
            kind = "a heavy swell" if swell_m >= SHORT_UNDER_M else "a long swell"
            tail = f"{kind} from {quarter_words(swell_from)}"
            if sea_m >= SMOOTH_UNDER_M and sea_state_word(sea_m) != state:
                words = f"{_base_phrase(sea_state_word(sea_m))} and {tail}"
            else:
                words = tail
            from_rad, period = swell_from, swell_t
        else:
            words = _base_phrase(state)
            from_rad, period = sea_from, sea_t
        self._reading = SeaReading(
            words=words,
            state=state,
            confused=confused,
            height_m=height,
            period_s=period,
            from_rad=from_rad,
            sea_m=sea_m,
            sea_from_rad=sea_from,
            swell_m=swell_m,
            swell_from_rad=swell_from,
            swell_period_s=swell_t,
        )
        return self._reading

    @property
    def words(self) -> str:
        return self.reading().words

    @property
    def state(self) -> str:
        return self.reading().state

    # -- the hook for 5b: the lookout's horizon ------------------------------------

    def horizon_nm(self, height_of_eye_m: float) -> float:
        """The distance of the sea horizon from a height of eye, in nautical miles: 2.08
        times the root of the height in metres (spec M5 §11's geographic horizon, the
        refracted figure of the navigation tables), the eye lowered by half the sea's
        height for the trough it is in. Inert until 5b's sighting reads it."""
        eye = max(height_of_eye_m - 0.5 * self.reading().height_m, 1.0)
        return 2.08 * math.sqrt(eye)
