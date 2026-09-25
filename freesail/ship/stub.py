"""The M0 ship: a point with a heading and an ordered speed.

It exists so the core (ticks, log, save, replay, console) can be built and
tested before there is any physics. It understands three orders, parsed by
hand; the real Orders grammar (WP6) replaces this parsing in M1.
"""

from __future__ import annotations

import math
import re
from typing import TYPE_CHECKING, Any

from freesail import units

if TYPE_CHECKING:
    from freesail.physics.wind import Wind


class OrderError(Exception):
    """An order that cannot be carried out. The message is written for the log."""


_NUMBER = re.compile(r"^-?\d+(\.\d+)?$")


class PointShip:
    TURN_RATE = math.radians(2.0)  # rad/s
    ACCELERATION = 0.05  # m/s^2

    def __init__(self, x: float = 0.0, y: float = 0.0, heading: float = 0.0, speed: float = 0.0):
        self.x = x
        self.y = y
        self.heading = units.wrap_2pi(heading)
        self.target_heading = self.heading
        self.speed = speed
        self.ordered_speed = speed
        self.name = "the ship"
        self.settled = True

    # -- simulation ----------------------------------------------------------

    def step(self, dt: float, wind: Wind) -> list[tuple[str, str, str]]:
        """Advance one tick. Returns (severity, kind, text) tuples to log."""
        notes: list[tuple[str, str, str]] = []
        error = units.wrap_pi(self.target_heading - self.heading)
        max_turn = self.TURN_RATE * dt
        if abs(error) <= max_turn:
            self.heading = self.target_heading
            if not self.settled:
                self.settled = True
                notes.append(
                    ("routine", "helm.steady", f"Steady on {units.format_heading(self.heading)}.")
                )
        else:
            self.heading = units.wrap_2pi(self.heading + math.copysign(max_turn, error))
        dv = self.ordered_speed - self.speed
        max_dv = self.ACCELERATION * dt
        self.speed += dv if abs(dv) <= max_dv else math.copysign(max_dv, dv)
        hx, hy = units.heading_vector(self.heading)
        self.x += hx * self.speed * dt
        self.y += hy * self.speed * dt
        return notes

    # -- orders --------------------------------------------------------------

    def handle_order(self, text: str) -> tuple[str, str, dict[str, Any]]:
        """Apply an order. Returns (kind, log text, data) or raises OrderError."""
        words = text.strip().lower().split()
        if not words:
            raise OrderError("No order given.")
        verb = words[0]
        rest = " ".join(words[1:])
        if verb == "steer":
            heading = self._parse_heading(rest)
            self.target_heading = heading
            self.settled = False
            return (
                "helm.order",
                f"Helm ordered: steer {units.format_heading(heading)}.",
                {"target_heading": heading},
            )
        if verb == "speed":
            m = re.match(r"^(-?\d+(?:\.\d+)?)\s*(knots?|kn)?$", rest)
            if not m:
                raise OrderError(f"Speed not understood: '{rest}'. Say 'speed 6 knots'.")
            kn = float(m.group(1))
            if kn < 0:
                raise OrderError("A ship cannot be ordered to make sternway by number.")
            self.ordered_speed = units.knots_to_ms(kn)
            return ("speed.order", f"Speed ordered: {kn:g} knots.", {"ordered_speed": kn})
        if verb == "stop":
            self.ordered_speed = 0.0
            return ("speed.order", "Way ordered off the ship.", {"ordered_speed": 0.0})
        raise OrderError(
            f"'{verb}' is not an order this ship understands. Try 'steer', 'speed' or 'stop'."
        )

    @staticmethod
    def _parse_heading(text: str) -> float:
        t = text.strip().rstrip(".")
        if not t:
            raise OrderError("Steer where? Give a compass point or degrees.")
        t = re.sub(r"\s*(degrees|deg|°)$", "", t)
        if _NUMBER.match(t):
            return units.wrap_2pi(units.deg_to_rad(float(t)))
        point = units.parse_compass_point(t)
        if point is None:
            raise OrderError(f"'{text}' is not a compass point or a number of degrees.")
        return point

    # -- queries -------------------------------------------------------------

    def state(self) -> dict[str, Any]:
        return {
            "x": self.x,
            "y": self.y,
            "heading": self.heading,
            "target_heading": self.target_heading,
            "speed": self.speed,
            "ordered_speed": self.ordered_speed,
        }

    def summary_lines(self) -> list[str]:
        return [
            f"Heading {units.format_heading(self.heading)}"
            + ("" if self.settled else f", coming to {units.format_heading(self.target_heading)}"),
            f"Speed {units.format_speed(self.speed)}"
            + (
                ""
                if abs(self.ordered_speed - self.speed) < 0.01
                else f" (ordered {units.format_speed(self.ordered_speed)})"
            ),
            f"Position {self.x:.0f} m E, {self.y:.0f} m N of the start",
        ]

    def save_ref(self) -> dict[str, Any]:
        return {"type": "point", "x": self.x, "y": self.y, "heading": self.heading}
