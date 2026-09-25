"""Runtime parts: the state of every spar, sail and line, and the hull's motion.

Specs (schema.py) say what a part *is*. Parts here say what state it is *in*:
set or furled, braced to what angle, how loaded, how worn. Physics reads
these; evolutions and level-0 orders change them.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from freesail import units
from freesail.ship.schema import HullSpec, LineSpec, SailSpec, SparSpec


class SailState(StrEnum):
    FURLED = "furled"  # stowed on its spar
    IN_THE_GEAR = "in_the_gear"  # hauled up by clewlines and buntlines, not furled
    LOOSED = "loosed"  # gaskets off, hanging
    SHEETED = "sheeted"  # sheets home but not hoisted (topsails) / not fully drawing
    SET = "set"  # drawing
    BLOWN_OUT = "blown_out"  # cloth gone


class LineState(StrEnum):
    BELAYED = "belayed"
    FREE = "free"  # let go, running
    PARTED = "parted"


@dataclass
class Part:
    id: str
    cls: str
    rating_kn: float
    condition: float = 100.0  # 0..100
    load_kn: float = 0.0  # current load, set by physics each substep
    wrecked: bool = False

    @property
    def strain_ratio(self) -> float:
        return self.load_kn / self.rating_kn if self.rating_kn > 0 else 0.0


@dataclass
class Spar(Part):
    x_m: float = 0.0
    height_m: float = 0.0
    length_m: float = 0.0
    parent: str | None = None
    side: str | None = None
    brace_limit: float = 0.0  # radians, for yards
    rake: float = 0.0  # radians, for masts: positive aft, negative forward
    brace_angle: float = 0.0  # radians; 0 square, +ve = braced up for the starboard tack
    sent_down: bool = False  # struck below (topgallant masts in a gale)

    @classmethod
    def from_spec(cls, s: SparSpec) -> Spar:
        return cls(
            id=s.id,
            cls=s.cls,
            rating_kn=s.rating_kn or 0.0,
            x_m=s.x_m or 0.0,
            height_m=s.height_m or 0.0,
            length_m=s.length_m or 0.0,
            parent=s.parent,
            side=s.side,
            brace_limit=units.deg_to_rad(s.brace_limit_deg or 0.0),
            rake=units.deg_to_rad(s.rake_deg or 0.0),
        )

    @property
    def is_yard(self) -> bool:
        return self.cls in {"yard", "lug_yard", "lateen_yard"}


@dataclass
class Sail(Part):
    area_m2: float = 0.0
    x_m: float = 0.0
    centre_height_m: float = 0.0
    reef_bands: int = 0
    side: str | None = None
    roles: dict[str, str] = field(default_factory=dict)
    cloth_rating_kn: float = 0.0
    state: SailState = SailState.FURLED
    reefs: int = 0
    sheet_angle: float = 0.0  # radians from the centreline; fore-and-aft sails
    # physics outputs, refreshed each substep
    backed: bool = False
    force_kn: float = 0.0
    thrust_kn: float = 0.0
    side_force_kn: float = 0.0
    area_effective_m2: float = 0.0

    @classmethod
    def from_spec(cls, s: SailSpec) -> Sail:
        cloth = s.cloth_rating_kn if s.cloth_rating_kn is not None else 0.9 * s.area_m2
        return cls(
            id=s.id,
            cls=s.cls,
            rating_kn=cloth,
            area_m2=s.area_m2,
            x_m=s.x_m,
            centre_height_m=s.centre_height_m,
            reef_bands=s.reef_bands,
            side=s.side,
            roles=dict(s.roles),
            cloth_rating_kn=cloth,
        )

    @property
    def is_set(self) -> bool:
        return self.state is SailState.SET and not self.wrecked

    @property
    def is_fore_and_aft(self) -> bool:
        return self.cls in {"gaff", "jibheaded", "lug", "lateen", "sprit"}

    def describe_state(self) -> str:
        if self.wrecked:
            return "wrecked"
        if self.state is SailState.SET and self.reefs:
            return f"set, {self.reefs} reef{'s' if self.reefs > 1 else ''}"
        return self.state.value.replace("_", " ")


@dataclass
class Line(Part):
    of: str = ""
    side: str | None = None
    state: LineState = LineState.BELAYED
    hauled: float = 1.0  # 0 = fully eased, 1 = hauled home (halyards, sheets)

    @classmethod
    def from_spec(cls, ln: LineSpec) -> Line:
        return cls(id=ln.id, cls=ln.cls, rating_kn=ln.rating_kn or 0.0, of=ln.of, side=ln.side)

    @property
    def is_standing(self) -> bool:
        return self.cls in {"stay", "shroud", "backstay"}


@dataclass
class Hull:
    spec: HullSpec
    water_in_well_m: float = 0.0

    @property
    def length(self) -> float:
        return self.spec.length_waterline_m

    @property
    def hull_speed(self) -> float:
        """Metres per second. Default 1.34 * sqrt(LWL in feet) knots."""
        if self.spec.hull_speed_kn is not None:
            return units.knots_to_ms(self.spec.hull_speed_kn)
        return units.knots_to_ms(1.34 * math.sqrt(units.m_to_feet(self.spec.length_waterline_m)))

    @property
    def lateral_area(self) -> float:
        if self.spec.lateral_area_m2 is not None:
            return self.spec.lateral_area_m2
        return 0.75 * self.spec.length_waterline_m * self.spec.draught_m

    @property
    def wetted_area(self) -> float:
        """A rough estimate from principal dimensions (Denny-Mumford style)."""
        L, B, T = self.spec.length_waterline_m, self.spec.beam_m, self.spec.draught_m
        return L * (1.7 * T + 0.7 * B)


class HelmMode(StrEnum):
    HEADING = "heading"  # steer a compass heading
    RUDDER = "rudder"  # hold a rudder angle (helm a-lee, hard over)
    FULL_AND_BY = "full_and_by"  # keep her as close to the wind as she will lie, full


@dataclass
class Dynamics:
    """The ship's motion state. Physics owns the numbers; orders set the targets."""

    x: float = 0.0
    y: float = 0.0
    heading: float = 0.0  # radians clockwise from north
    u: float = 0.0  # surge, m/s (forward +)
    v: float = 0.0  # sway, m/s (to starboard +)
    r: float = 0.0  # yaw rate, rad/s (clockwise +)
    heel: float = 0.0  # radians, +ve = heeled to starboard
    rudder: float = 0.0  # radians, +ve = rudder to starboard (turns the ship to starboard)
    helm_mode: HelmMode = HelmMode.HEADING
    target_heading: float = 0.0
    target_rudder: float = 0.0
    steady: bool = True
    # readings refreshed by physics each tick
    speed: float = 0.0  # through the water, m/s
    leeway: float = 0.0  # radians, +ve = set to starboard
    weather_helm: float = 0.0  # radians, positive when she wants to round up (weather helm)
    apparent_wind_angle: float = 0.0  # radians, +ve on the starboard bow
    apparent_wind_speed: float = 0.0

    @property
    def tack(self) -> str:
        """The side the wind is on: 'starboard' or 'larboard'."""
        return "starboard" if self.apparent_wind_angle >= 0 else "larboard"

    def state(self) -> dict[str, Any]:
        return {
            "x": self.x,
            "y": self.y,
            "heading": self.heading,
            "speed": self.speed,
            "u": self.u,
            "v": self.v,
            "r": self.r,
            "leeway": self.leeway,
            "heel": self.heel,
            "rudder": self.rudder,
            "weather_helm": self.weather_helm,
            "helm_mode": self.helm_mode.value,
            "target_heading": self.target_heading,
            "apparent_wind_angle": self.apparent_wind_angle,
            "apparent_wind_speed": self.apparent_wind_speed,
        }
