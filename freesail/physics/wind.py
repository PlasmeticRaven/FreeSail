"""The true wind: a single field over the plane with slow variation and gusts.

This is the M0 to M2 wind (spec §7.1). Moving weather systems arrive in M5 and
will replace the random walk with something that has a reason; the interface
(`direction_from`, `speed_at_height`, `vector_at_height`) stays.

A scenario's weather script (spec M4 §19, `freesail.world.weather_script`) moves the
**base** the wind wanders about (`follow`): the direction's walk and the speed's
mean-reverting wander are kept as offsets from the base, and the gusts multiply the
result, exactly as they do about a fixed base. Without a script nothing here changes.
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
# them the wind is at its mean (judgement: the M2 wind's gusts are a tenth to a half again
# the base, `Wind.step`, so every gust is at least this far above; a lull is the mirror).
# Never less than GUST_MARGIN_FLOOR_KN, so a light air's knot either way is not a gust.
GUST_MARGIN = 0.1
GUST_MARGIN_FLOOR_KN = 1.0


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
        self.direction_from = units.wrap_2pi(params.direction_from)
        self.base_direction = self.direction_from  # moved only by `follow`
        self.base_speed = max(params.speed, self.MIN_SPEED)
        self.speed = self.base_speed
        self.gust_factor = 1.0
        self.gust_remaining = 0.0
        self.gust_started = False  # set True on the tick a gust begins

    # -- the weather script (spec M4 §19) ------------------------------------

    def follow(self, direction_from: float, speed: float) -> None:
        """Move the base wind to the script's, before `step`: the wind turns by what the
        base turned (the short way round) and its speed changes by what the base's did,
        so the wander about the base and any gust ride on the scripted wind as they ride
        on a fixed one. Draws nothing from the stream."""
        turn = units.wrap_pi(direction_from - self.base_direction)
        self.base_direction = units.wrap_2pi(direction_from)
        self.direction_from = units.wrap_2pi(self.direction_from + turn)
        base = max(speed, self.MIN_SPEED)
        self.speed = max(self.MIN_SPEED, self.speed + (base - self.base_speed))
        self.base_speed = base

    # -- per-tick update -----------------------------------------------------

    def step(self, dt: float = 1.0) -> None:
        v = self.params.variability
        r = self._stream
        # direction: random walk, radians; ~1 point per hour at variability 1
        self.direction_from = units.wrap_2pi(
            self.direction_from + r.gauss(0.0, 0.0002 * v * math.sqrt(dt))
        )
        # speed: mean-reverting walk about the base speed
        pull = (self.base_speed - self.speed) * 0.0005 * dt
        noise = r.gauss(0.0, 0.01 * v * self.base_speed * math.sqrt(dt))
        self.speed = max(self.MIN_SPEED, self.speed + pull + noise)
        # gusts
        self.gust_started = False
        if self.gust_remaining > 0:
            self.gust_remaining -= dt
            if self.gust_remaining <= 0:
                self.gust_factor = 1.0
        elif r.random() < self.params.gustiness * 0.002 * dt:
            self.gust_factor = r.uniform(1.1, 1.5)
            self.gust_remaining = r.uniform(5.0, 30.0)
            self.gust_started = True

    # -- queries ------------------------------------------------------------

    @property
    def effective_speed(self) -> float:
        """Speed at the reference height including any gust."""
        return self.speed * self.gust_factor

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
