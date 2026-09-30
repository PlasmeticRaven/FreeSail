"""The true wind: a base with slow variation and gusts on top of it.

The M0 to M2 wind (spec §7.1) is one field over the plane: a base direction and speed, the
direction on a random walk, the speed on a mean-reverting wander, and gusts that multiply
the result. The interface (`direction_from`, `speed_at_height`, `vector_at_height`)
stays whatever moves the base.

**The base has two sources.** A scenario's weather script (spec M4 §19,
`freesail.world.weather_script`) pins it directly (`follow`); milestone 5's weather
systems (spec M5 §2, `freesail.world.weather`) give it a cause: the surface wind at the
ship, which the World hands to `follow` every tick with the sector's air mass. Without
either the base is fixed.

**One rule, by the air mass** (spec M5 §3; the study `docs/design/WeatherSystems.md` §4;
the owner's ruling at gate 5a, decision 28, package 31b): the gust factor is drawn by the
air mass (`GUST_FACTOR_RANGES`: a warm sector 1.10 to 1.20, neutral air 1.15 to 1.30,
unstable air behind a cold front 1.20 to 1.30) as a multiple of the ten-minute mean, which
is how the studies the ranges come from define it (the peak few-second gust over the
eight- to ten-minute mean, W §4, S29 to S31); the top of the unstable range, 1.30 to
1.45, is a squall's, its own event of a few minutes with a veer of a point or two and rain
(`SQUALL_*`); and the direction's walk is mean-reverting about the base with a spread by
the air mass (`WANDER_SPREAD_DEG`). The air mass is the systems' sector when they drive
the wind, and otherwise `DEFAULT_AIR_MASS`, neutral, unless the scenario says (a fixed
wind's `air_mass`, or a pinned waypoint's). The milestone 2 draws (a gust factor of 1.1
to 1.5 whatever the mean, an unbounded walk of the direction), which packages 30 and 31
kept for a fixed or pinned wind so that the M4 truths did not move, are retired; those
truths were re-measured under this rule (docs/dev/TuningNotes.md, M5a, package 31b).
"""

from __future__ import annotations

import math
import random
from collections import deque
from dataclasses import dataclass

from freesail import units

# The mean wind (package 29b, playtest 7's finding 4: a watcher read single gusts as
# changes in the wind, and asked for a mean over the last ten minutes): the true wind
# averaged over ten minutes of ship's time. Ten minutes is the averaging period of the
# modern surface wind report (WMO-No. 8, Guide to Instruments and Methods of Observation,
# the ten-minute mean; an anachronism in 1805, used here as a period, not as an
# instrument), and long against the M2 wind's gusts of five to thirty seconds.
MEAN_WIND_WINDOW_S = 600

# A reading this share of the mean above it is a gust, as far below a lull, and between
# them the wind is at its mean (judgement: a gust is a tenth to three tenths again the
# mean by the air mass, `Wind.step`, so every gust is at least this far above; a lull is
# the mirror). Never less than GUST_MARGIN_FLOOR_KN, so a light air's knot either way is
# not a gust.
GUST_MARGIN = 0.1
GUST_MARGIN_FLOOR_KN = 1.0

# The gust factor by air mass (spec M5 §3; W §4): over the open sea the peak gust over the
# ten-minute mean is about 1.2 to 1.25 and nearly flat with wind speed (Kramer 2013,
# marine sites 1.21 to 1.23; Blaes et al. 2013, 1.23 with 61 per cent of factors between
# 1.2 and 1.3; the Mariners Weather Log 2008 study, 1.25 near neutral; S29 to S31,
# verified), rising as the air becomes less stable and falling toward 1.1 in the stable
# warm sector; over the open sea a factor of 1.5 "is a squall, not a gust". The ranges are
# the study's recommendation from those figures. The WMO table's 1.23 (S32) was not
# reached and is not relied on.
GUST_FACTOR_RANGES: dict[str, tuple[float, float]] = {
    "warm": (1.10, 1.20),
    "neutral": (1.15, 1.30),
    "unstable": (1.20, 1.30),
}
# A squall (W §4): the top of the unstable range, 1.30 to 1.45 of the mean, for a few
# minutes, veering the wind a point or two, with rain. How often: about one an hour in
# the unstable air behind a cold front (judgement; the study gives no rate), and its
# length three to eight minutes ("their own events lasting minutes").
SQUALL_FACTOR_RANGE = (1.30, 1.45)
SQUALL_VEER_POINTS = (1.0, 2.0)
SQUALL_DURATION_S = (180.0, 480.0)
SQUALL_RATE_PER_S = 1.0 / 3600.0

# The direction's mean-reverting wander (spec M5 §3; W §4: "a spread of some 5 to 10
# degrees in unstable air and less in stable"; the study's judgement, not a measured
# figure): the stationary spread of the direction about the base at the default
# variability, by air mass, and the time the wander takes to forget an offset
# (judgement: twenty minutes, the scale of the eddies that turn a ten-minute mean).
WANDER_SPREAD_DEG: dict[str, float] = {"warm": 3.0, "neutral": 5.0, "unstable": 8.0}
WANDER_TIME_CONSTANT_S = 1200.0
# The variability at which the spreads above hold (the scenario's default); a scenario's
# variability scales them, and nought gives no wander, as every truth is measured.
DEFAULT_VARIABILITY = 0.3

# The air mass a wind has when nothing gives it one (package 31b; the owner's ruling at
# gate 5a): a fixed wind, or a wind pinned by a scenario's script whose waypoints say no
# air, is in neutral air, gusting to 1.30 of its mean at most and never squalling. The
# scenario may say otherwise (`Scenario.air_mass`; a waypoint's `air_mass`), and the
# systems' sector says when they drive the wind. The names are `AIR_MASSES`.
DEFAULT_AIR_MASS = "neutral"
AIR_MASSES: tuple[str, ...] = ("warm", "neutral", "unstable")


@dataclass
class WindParams:
    direction_from: float  # radians, where the wind comes from
    speed: float  # m/s at 10 m above the water
    gustiness: float = 0.3  # 0..1: how often gusts come
    variability: float = 0.3  # 0..1: how much direction and speed wander

    @classmethod
    def from_nautical(
        cls,
        direction_from_deg: float,
        speed_knots: float,
        gustiness: float = 0.3,
        variability: float = 0.3,
    ) -> WindParams:
        return cls(
            direction_from=units.deg_to_rad(direction_from_deg),
            speed=units.knots_to_ms(speed_knots),
            gustiness=gustiness,
            variability=variability,
        )


class Wind:
    """Slowly wandering wind with gusts. Deterministic given its stream."""

    SHEAR_EXPONENT = 0.11
    REFERENCE_HEIGHT = 10.0
    MIN_SPEED = 0.25  # m/s, so the wind never dies completely in M0-M2

    def __init__(self, params: WindParams, stream: random.Random):
        self.params = params
        self._stream = stream
        self._direction = units.wrap_2pi(params.direction_from)  # the wandered direction
        self.base_direction = self._direction  # moved only by `follow`
        self.base_speed = max(params.speed, self.MIN_SPEED)
        self.speed = self.base_speed
        self.gust_factor = 1.0
        self.gust_remaining = 0.0
        self.gust_started = False  # set True on the tick a gust begins
        # the air mass at the ship (spec M5 §3): the systems' sector when they drive the
        # wind, else the scenario's, else neutral (package 31b)
        self.air_mass: str = DEFAULT_AIR_MASS
        self._gust_peak = 0.0  # m/s: the gust's peak, a multiple of the ten-minute mean
        self.squall_factor = 1.0
        self.squall_veer = 0.0  # radians, added to the direction while the squall lasts
        self.squall_remaining = 0.0
        self.squall_started = False
        self.squall_ended = False
        self._squall_peak = 0.0

    # -- the direction, with a squall's veer on it ------------------------------

    @property
    def direction_from(self) -> float:
        """Where the wind comes from now, radians in [0, 2 pi): the wandered direction
        plus a squall's veer while one lasts."""
        if self.squall_remaining > 0.0:
            return units.wrap_2pi(self._direction + self.squall_veer)
        return self._direction

    @direction_from.setter
    def direction_from(self, value: float) -> None:
        self._direction = units.wrap_2pi(value)

    @property
    def in_squall(self) -> bool:
        return self.squall_remaining > 0.0

    # -- the weather script and the systems (spec M4 §19, M5 §2) ------------------

    def follow(self, direction_from: float, speed: float) -> None:
        """Move the base wind to the script's or the systems', before `step`: the wind
        turns by what the base turned (the short way round) and its speed changes by what
        the base's did, so the wander about the base and any gust ride on the moving base
        as they ride on a fixed one. Draws nothing from the stream."""
        turn = units.wrap_pi(direction_from - self.base_direction)
        self.base_direction = units.wrap_2pi(direction_from)
        self._direction = units.wrap_2pi(self._direction + turn)
        base = max(speed, self.MIN_SPEED)
        self.speed = max(self.MIN_SPEED, self.speed + (base - self.base_speed))
        self.base_speed = base

    # -- per-tick update -----------------------------------------------------

    def step(self, dt: float = 1.0, mean_speed: float | None = None) -> None:
        """One tick. `mean_speed` is the ten-minute mean (`WindRecord.mean_speed`), which
        the gusts and squalls are drawn as multiples of; None (the first tick, or a wind
        stepped without a World) reads the instant's speed instead."""
        v = self.params.variability
        r = self._stream
        air = self.air_mass or DEFAULT_AIR_MASS
        # direction: mean-reverting about the base (Ornstein-Uhlenbeck), spread by the air
        # mass
        spread = units.deg_to_rad(WANDER_SPREAD_DEG[air]) * (v / DEFAULT_VARIABILITY)
        tau = WANDER_TIME_CONSTANT_S
        offset = units.wrap_pi(self._direction - self.base_direction)
        offset += -offset * dt / tau + r.gauss(0.0, spread * math.sqrt(2.0 * dt / tau))
        self._direction = units.wrap_2pi(self.base_direction + offset)
        # speed: mean-reverting walk about the base speed
        pull = (self.base_speed - self.speed) * 0.0005 * dt
        noise = r.gauss(0.0, 0.01 * v * self.base_speed * math.sqrt(dt))
        self.speed = max(self.MIN_SPEED, self.speed + pull + noise)
        mean = mean_speed if mean_speed is not None else self.speed
        # gusts
        self.gust_started = False
        if self.gust_remaining > 0:
            self.gust_remaining -= dt
            if self.gust_remaining <= 0:
                self.gust_factor = 1.0
                self._gust_peak = 0.0
        elif r.random() < self.params.gustiness * 0.002 * dt:
            self.gust_factor = r.uniform(*GUST_FACTOR_RANGES[air])
            self._gust_peak = mean * self.gust_factor
            self.gust_remaining = r.uniform(5.0, 30.0)
            self.gust_started = True
        # squalls: unstable air only
        self.squall_started = False
        self.squall_ended = False
        if self.squall_remaining > 0:
            self.squall_remaining -= dt
            if self.squall_remaining <= 0:
                self.squall_remaining = 0.0
                self.squall_factor = 1.0
                self.squall_veer = 0.0
                self._squall_peak = 0.0
                self.squall_ended = True
        elif air == "unstable" and r.random() < SQUALL_RATE_PER_S * dt:
            self.squall_factor = r.uniform(*SQUALL_FACTOR_RANGE)
            self.squall_veer = units.points_to_rad(r.uniform(*SQUALL_VEER_POINTS))
            self.squall_remaining = r.uniform(*SQUALL_DURATION_S)
            self._squall_peak = mean * self.squall_factor
            self.squall_started = True

    # -- queries ------------------------------------------------------------

    @property
    def effective_speed(self) -> float:
        """Speed at the reference height including any gust or squall: a gust's or a
        squall's peak is a multiple of the ten-minute mean, never less than the instant."""
        peak = 0.0
        if self.gust_remaining > 0.0:
            peak = self._gust_peak
        if self.squall_remaining > 0.0:
            peak = max(peak, self._squall_peak)
        return max(self.speed, peak)

    def speed_at_height(self, height: float) -> float:
        h = max(height, 1.0)
        return self.effective_speed * (h / self.REFERENCE_HEIGHT) ** self.SHEAR_EXPONENT

    def vector_at_height(self, height: float) -> tuple[float, float]:
        return units.wind_vector(self.direction_from, self.speed_at_height(height))

    def describe(self) -> str:
        return units.format_wind(self.direction_from, self.effective_speed)

    def state(self) -> dict[str, float]:
        return {
            "direction_from": self.direction_from,
            "speed": self.speed,
            "gust_factor": self.gust_factor,
            "effective_speed": self.effective_speed,
        }


class WindRecord:
    """The true wind of the last `MEAN_WIND_WINDOW_S` ticks, for the mean wind reading.

    The World adds the wind once a tick, after it steps; nothing here draws randomness or
    is saved, since a replay adds the same winds again. The mean speed is the plain mean
    of the speeds; the mean direction is the direction of the mean wind vector, so a
    wind that backed and veered about north averages to north and not to south."""

    def __init__(self, window_s: int = MEAN_WIND_WINDOW_S):
        self._speeds: deque[float] = deque(maxlen=window_s)
        self._east: deque[float] = deque(maxlen=window_s)
        self._north: deque[float] = deque(maxlen=window_s)

    def add(self, speed: float, direction_from: float) -> None:
        self._speeds.append(speed)
        self._east.append(speed * math.sin(direction_from))
        self._north.append(speed * math.cos(direction_from))

    def __len__(self) -> int:
        return len(self._speeds)

    def mean_speed(self) -> float | None:
        """Metres a second over the window; None before the first tick."""
        if not self._speeds:
            return None
        return math.fsum(self._speeds) / len(self._speeds)

    def mean_from(self) -> float | None:
        """Radians, where the mean wind comes from; None before the first tick."""
        if not self._speeds:
            return None
        return units.wrap_2pi(math.atan2(math.fsum(self._east), math.fsum(self._north)))


def against_mean(speed: float, mean: float) -> str:
    """'a gust above the mean', 'at the mean' or 'a lull', for a speed against its mean."""
    margin = max(GUST_MARGIN * mean, units.knots_to_ms(GUST_MARGIN_FLOOR_KN))
    if speed >= mean + margin:
        return GUST_WORDS[0]
    if speed <= mean - margin:
        return GUST_WORDS[2]
    return GUST_WORDS[1]


# The label's words, as the readings give them and the dialect compares them.
GUST_WORDS: tuple[str, ...] = ("a gust above the mean", "at the mean", "a lull")
