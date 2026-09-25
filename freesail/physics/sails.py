"""STUB: sail forces, to be replaced by package 4.

This file exists only so that package 5 (hull physics and integration) can be
written and tested before the real sail physics lands. It gives the hull no
drive at all: every force and moment is zero. It does keep one small promise
of the real module, filling in the apparent wind at deck level so that the
console's summary line and the helm's full-and-by rule have something to read.

Package 4 replaces this whole file. The only things package 5 relies on are the
names and fields below: `SailForces` with `thrust_n`, `side_n`,
`heel_moment_nm`, `yaw_moment_nm`, `windage_drag_n`, and the call
`compute_sail_forces(ship, wind)`.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from freesail import units
from freesail.physics.wind import Wind
from freesail.ship.graph import Ship


@dataclass
class SailForces:
    thrust_n: float  # along the keel, forward positive
    side_n: float  # to starboard positive
    heel_moment_nm: float  # positive heels to starboard
    yaw_moment_nm: float  # about the hull's centre of lateral resistance, positive to starboard
    windage_drag_n: float  # drag of furled sails, spars and wrecks (already included above)


def compute_sail_forces(ship: Ship, wind: Wind) -> SailForces:
    """STUB. Returns no force; records the deck-level apparent wind in `ship.dyn`."""
    d = ship.dyn
    wx, wy = wind.vector_at_height(ship.hull.spec.deck_height_m)
    ex, ey = units.heading_vector(d.heading)
    # ship velocity over the plane: surge along the heading, sway to starboard of it
    sx = d.u * ex + d.v * ey
    sy = d.u * ey - d.v * ex
    ax, ay = wx - sx, wy - sy
    d.apparent_wind_speed = math.hypot(ax, ay)
    d.apparent_wind_angle = units.relative_bearing(d.heading, units.wind_direction_from(ax, ay))
    return SailForces(0.0, 0.0, 0.0, 0.0, 0.0)
