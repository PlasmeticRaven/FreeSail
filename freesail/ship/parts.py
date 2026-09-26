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
    UNBENT = "unbent"  # no sail on the yard: unbent and sent down to the sail room
    GOOSE_WINGED = "goose_winged"  # a course or topsail with the lee clew hauled up, half drawing


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
    rigged_out: bool = True  # studding sail booms: run out along the yard, ready for the sail
    # Milestone 3b (spec 3b §3). `brace_limit` above is the limit the rigging allows
    # now, and every reader reads it; `rigged_brace_limit` is the ship file's, with the
    # lower rigging as rigged. They differ only for a lower yard whose mast has its
    # catharpins swiftered in (see `sync_catharpins`).
    rigged_brace_limit: float = 0.0  # radians, for yards: the ship file's brace_limit_deg
    swiftered_in: bool = False  # lower masts: the catharpins swiftered in
    # Lower masts: the strain model's allowance for the catharpins, set by strain.py each
    # tick while they are swiftered in; 1.0 when the lower rigging stands as rigged.
    rating_factor: float = 1.0

    @classmethod
    def from_spec(cls, s: SparSpec) -> Spar:
        limit = units.deg_to_rad(s.brace_limit_deg or 0.0)
        return cls(
            id=s.id,
            cls=s.cls,
            rating_kn=s.rating_kn or 0.0,
            x_m=s.x_m or 0.0,
            height_m=s.height_m or 0.0,
            length_m=s.length_m or 0.0,
            parent=s.parent,
            side=s.side,
            brace_limit=limit,
            rake=units.deg_to_rad(s.rake_deg or 0.0),
            rigged_brace_limit=limit,
        )

    @property
    def is_yard(self) -> bool:
        return self.cls in {"yard", "lug_yard", "lateen_yard"}

    @property
    def strain_ratio(self) -> float:
        rating = self.rating_kn * self.rating_factor
        return self.load_kn / rating if rating > 0 else 0.0


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
        line = cls(id=ln.id, cls=ln.cls, rating_kn=ln.rating_kn or 0.0, of=ln.of, side=ln.side)
        if line.cls == "bowline":
            # Rove, with its fall clear on deck, but not hauled out: a bowline is hauled
            # on a wind by hands and let go again when the yards come in (spec 3b §4).
            line.state = LineState.FREE
        return line

    @property
    def is_standing(self) -> bool:
        return self.cls in {"stay", "shroud", "backstay"}

    @property
    def bowline_hauled(self) -> bool:
        """A bowline hauled out and belayed, holding its sail's leech taut forward (spec
        3b §4). Eased, let go, slacked or parted, it holds nothing."""
        return (
            self.cls == "bowline" and self.state is LineState.BELAYED and self.hauled >= 1.0 - 1e-9
        )


# ---------------------------------------------------------------------------
# Catharpins (spec 3b §3)
# ---------------------------------------------------------------------------

# Swiftering in the catharpins draws the lower shrouds in below the top, so that the
# lower yard can be braced sharper before its lee yardarm and its sail come against
# the lee rigging: Steel 1794, vol. I, CATHARPINS ("Short ropes, to keep the lower
# shrouds in tight, after they are braced in by swifter, and to afford room to brace
# the yards sharp"); Lever 1808, fig. 182 (the shrouds "bowsed in" by a swifter and the
# legs seized); Fincham 1843, art. 102 (Hardy's short ship, by "such measures as would
# allow the yards to be braced sharper up", lay a point closer). How much sharper no
# source says: four degrees is judgement, less than the short ship's gain over the long
# ships in art. 102, which her other measures shared. The topmast rigging is not
# touched, so only the lower yard gains.
CATHARPIN_GAIN_DEG = 4.0


def lower_yards(ship: Any, mast: Spar) -> list[Spar]:
    """The yards slung on a lower mast itself: a ship's course yard, the crossjack.
    A topsail schooner's masts have none (her topsail yard is on the fore topmast)."""
    return [y for y in ship.spars.values() if y.parent == mast.id and y.is_yard]


def sync_catharpins(ship: Any) -> list[tuple[Spar, float]]:
    """Make every lower yard's brace limit agree with its mast's catharpins.

    The mast's `swiftered_in` is the state; its lower yards' `brace_limit` follows it,
    `CATHARPIN_GAIN_DEG` beyond the ship file's while swiftered in. A yard braced
    sharper than the limit it is left with (the catharpins eased with the yard sharp
    up) comes in to it, as the shrouds going out bear it in. Returns the yards that
    came in, each with the angle it came in from, for the log. Idempotent: the strain
    model calls it every tick, and whatever reads a limit may call it first."""
    came_in: list[tuple[Spar, float]] = []
    gain = units.deg_to_rad(CATHARPIN_GAIN_DEG)
    for mast in ship.spars.values():
        if mast.cls != "mast":
            continue
        for yard in lower_yards(ship, mast):
            if yard.rigged_brace_limit <= 0.0:
                continue  # the file gives this yard no limit; nothing to gain or keep
            limit = yard.rigged_brace_limit + (gain if mast.swiftered_in else 0.0)
            yard.brace_limit = limit
            if abs(yard.brace_angle) > limit + 1e-9:
                came_in.append((yard, yard.brace_angle))
                yard.brace_angle = math.copysign(limit, yard.brace_angle)
    return came_in


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
