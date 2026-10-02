"""Other sail at far detail (spec M5 §25; package 35 builds the smallest honest form for
the pilot cutter, package 36 the dozen ships and their descriptions).

A **vessel** here is a hull from a ship file (for her rig's height, which decides where
she is first seen) moving along a plan at a speed the wind allows, in the world's frame:
a position, a heading, a few numbers, ticked once a game minute. She is never promoted
to the full part-and-crew model in this package (proposal §5.2's "near" level is 36's
or later). What the ship models of her is what the lookout can see: a sail at the
horizon distance her rig's height and the visibility give, hailed by a bearing first
("Sail ho!") and by her rig only as she nears (`RIG_MADE_OUT_NM`), then by what she is
when she is close (`MADE_OUT_NM`). The lookout's distance by estimation applies to her
as to the land (`freesail.world.lookout`, drawn from a stream of her own, `sail`, so
that a sail in sight never moves the land's draws and the pinned passages' ticks).

**The pilot cutter** (package 35; spec M5 §23; `docs/design/VesselCandidates.md`) is
the first vessel: 32b's cutter, which comes off from the port when a ship is in the
pilot's cruising ground, closes her, lies to under her lee while the pilot boards, and
goes back (`freesail.world.ports.Ports`). What 36 inherits: `Vessel` and `Vessels`,
`world.vessels` ticked once a minute before the lookout looks, the lookout's `sail`
sightings and their hails, the reading `a sail in sight` and the event `a sail sighted`;
36 adds the plans (trade this route, patrol this station), the nation's colours as the
lookout makes them out (`Vessel.colours`), the descriptions at far detail, and the
sighting of the player's ship by them.
"""

from __future__ import annotations

import functools
import math
from dataclasses import dataclass, field
from typing import Any

from freesail import units
from freesail.world.chart import Feature, Sighting
from freesail.world.geo import Position, bearing_and_distance, horizon_nm

__all__ = [
    "CUTTER_SPEED_KN",
    "MADE_OUT_NM",
    "RIG_MADE_OUT_NM",
    "VESSEL_TICK_S",
    "WIND_SPEED_FRACTION",
    "Vessel",
    "Vessels",
    "rig_height_m",
]

# A vessel at far detail is moved once a game minute, as the lookout looks (judgement:
# a cutter at six knots moves a cable in a minute, which is the sighting's precision).
VESSEL_TICK_S = 60
# A pilot cutter's pace on her errand, knots, capped by the wind: a Channel cutter's
# ordinary sailing (the type's records of ten knots are the big cutters' with a press
# of sail; judgement, docs/design/VesselCandidates.md) and about half the wind's speed in
# a moderate breeze, no vessel going faster than the wind allows (judgement).
CUTTER_SPEED_KN = 6.0
WIND_SPEED_FRACTION = 0.5
VESSEL_MIN_SPEED_KN = 1.5  # she has steerage way in the lightest air that moves her (judgement)
# Within this a sail's rig is made out ("a cutter"), and within `MADE_OUT_NM` what she is
# and whose ("the Falmouth pilot's cutter, her number on her mainsail"): judgement on
# the eye's power from a frigate's masthead by day; the night's limit is the land's.
RIG_MADE_OUT_NM = 4.0
MADE_OUT_NM = 1.5
# A vessel making for the ship closes to this part of the distance asked (judgement: a
# cutter rounding to under a frigate's lee comes a cable and a half when two were named).
ARRIVE_FRACTION = 0.75


@functools.lru_cache(maxsize=8)
def rig_height_m(ship_file: str) -> float:
    """The height of a vessel's masthead above the water from her ship file, which
    decides her horizon (truth 67): the deck's height plus the tallest chain of masts."""
    from freesail.ship.graph import Ship
    from freesail.ship.loader import load_spec
    from freesail.world.lookout import height_of_eye

    try:
        return float(height_of_eye(Ship(load_spec(ship_file))))
    except Exception:  # a file not found or not a rig: a small vessel's masthead (judgement)
        return 15.0


@dataclass
class Vessel:
    """A vessel at far detail: who she is, where she is, and her plan."""

    id: str
    name: str  # as the lookout names her when made out: "the Falmouth pilot's cutter"
    kind: str  # her rig's word when made out at a distance: "a cutter"
    ship_file: str
    nation: str
    position: Position
    heading_deg: float = 0.0
    speed_kn: float = CUTTER_SPEED_KN
    colours: str = ""  # the words of her colours when made out (36 reads them)
    purpose: str = ""  # "standing out from the land", for the hail when her rig is made out
    # the plan: a list of legs, each ("to", Position), ("to_ship",), ("lie_to", seconds)
    # or ("home", Position); the first is the one in hand, and the vessel is done when
    # the list is empty
    plan: list[tuple[Any, ...]] = field(default_factory=list)
    done: bool = False
    distance_run_m: float = 0.0
    lying_to_s: float = 0.0
    alongside: bool = False  # within hail of the ship, lying under her lee

    @property
    def height_m(self) -> float:
        return rig_height_m(self.ship_file)

    def pace_ms(self, wind_speed_ms: float) -> float:
        kn = min(
            self.speed_kn,
            max(VESSEL_MIN_SPEED_KN, WIND_SPEED_FRACTION * units.ms_to_knots(wind_speed_ms)),
        )
        return units.knots_to_ms(kn)

    def tick(self, world: Any, dt: float) -> None:
        """Move along the plan for `dt` seconds."""
        if self.done or not self.plan:
            self.done = True
            return
        leg = self.plan[0]
        kind = leg[0]
        if kind == "lie_to":
            self.lying_to_s += dt
            if self.lying_to_s >= float(leg[1]):
                self.lying_to_s = 0.0
                self.plan.pop(0)
            return
        if kind == "to_ship":
            target = world.position
            if target is None:
                self.plan.pop(0)
                return
            # she runs in to a little under the hailing distance asked, so that a ship
            # under way is caught and not followed for ever at exactly that distance
            arrive_m = (float(leg[1]) if len(leg) > 1 else units.CABLE * 2.0) * ARRIVE_FRACTION
        else:
            target = leg[1]
            arrive_m = units.CABLE
        bearing, distance = bearing_and_distance(self.position, target)
        step = self.pace_ms(float(world.wind.effective_speed)) * dt
        self.heading_deg = bearing
        if distance <= arrive_m + 1.0:  # a metre: she stops at the mark
            self.plan.pop(0)
            if kind == "home":
                self.done = True
            return
        if step >= distance - arrive_m:
            step = max(0.0, distance - arrive_m)
        rad = math.radians(bearing)
        self.position = self.position.advanced(step * math.sin(rad), step * math.cos(rad))
        self.distance_run_m += step

    def seen_as_feature(self, distance_m: float) -> Feature:
        """The feature the lookout sees at this distance: 'a sail' beyond
        `RIG_MADE_OUT_NM`, her rig within it, and what she is within `MADE_OUT_NM`."""
        nm = distance_m / units.NAUTICAL_MILE
        if nm <= MADE_OUT_NM:
            name = self.name
        elif nm <= RIG_MADE_OUT_NM:
            name = f"{self.kind} {self.purpose}".strip() if self.purpose else self.kind
        else:
            name = "a sail"
        return Feature(
            f"sail:{self.id}",
            "sail",
            name,
            self.position.lat_deg,
            self.position.lon_deg,
            modern=self.id,
            height_m=self.height_m,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "kind": self.kind,
            "nation": self.nation,
            "position": self.position.to_dict(),
            "heading_deg": round(self.heading_deg, 1),
            "speed_kn": self.speed_kn,
            "plan": [str(leg[0]) for leg in self.plan],
            "done": self.done,
            "alongside": self.alongside,
        }


class Vessels:
    """The vessels of one World, ticked once a game minute (`World.tick`), and what the
    lookout can see of them."""

    def __init__(self) -> None:
        self.vessels: list[Vessel] = []

    def add(self, vessel: Vessel) -> Vessel:
        self.vessels.append(vessel)
        return vessel

    def get(self, vessel_id: str) -> Vessel | None:
        for v in self.vessels:
            if v.id == vessel_id:
                return v
        return None

    def active(self) -> list[Vessel]:
        return [v for v in self.vessels if not v.done]

    def tick(self, world: Any, dt: float = float(VESSEL_TICK_S)) -> None:
        for v in self.vessels:
            if not v.done:
                v.tick(world, dt)
        self.vessels = [v for v in self.vessels if not v.done]

    def in_sight(
        self, pos: Position, height_of_eye_m: float, visibility_nm: float | None, daylight: str
    ) -> list[Sighting]:
        """The vessels in sight from the masthead: within the horizon her rig's height
        and the eye give (truth 67), within the weather's visibility, by day; at night a
        sail is seen only close aboard, as the land is (`chart.NIGHT_LAND_NM`)."""
        from freesail.world.chart import NIGHT_LAND_NM

        vis_nm = math.inf if visibility_nm is None else float(visibility_nm)
        out: list[Sighting] = []
        for v in self.vessels:
            if v.done:
                continue
            bearing, distance = bearing_and_distance(pos, v.position)
            nm = distance / units.NAUTICAL_MILE
            limit = min(vis_nm, horizon_nm(height_of_eye_m, v.height_m))
            if daylight != "day":
                limit = min(limit, NIGHT_LAND_NM)
            if nm <= limit:
                out.append(Sighting(v.seen_as_feature(distance), bearing, distance, "sail"))
        out.sort(key=lambda s: s.distance_m)
        return out
