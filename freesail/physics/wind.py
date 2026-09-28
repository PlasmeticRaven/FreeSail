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
from dataclasses import dataclass

from freesail import units


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
