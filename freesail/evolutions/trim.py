"""Tending the sheets of fore-and-aft sails between orders.

A watch on deck does not leave a jib or a spanker sheeted as it was when
set; as the ship's heading or the wind changes they ease or haul the sheet
to keep the sail drawing. Until the crew system (milestone 3) does this as
work, this module does it as a slow automatic adjustment: each set
fore-and-aft sail's sheet angle drifts toward the trim for the present
apparent wind at a modest rate. Square sails are not touched; bracing yards
is always an explicit order.
"""

from __future__ import annotations

from freesail import units
from freesail.ship.graph import Ship

SHEET_RATE = units.deg_to_rad(1.0)  # radians per second the hands can work a sheet
# chord angle = apparent wind angle minus this, per class, clamped to the range
TRIM_OFFSET = {
    "gaff": units.deg_to_rad(25.0),
    "jibheaded": units.deg_to_rad(28.0),
    "lug": units.deg_to_rad(25.0),
    "lateen": units.deg_to_rad(25.0),
    "sprit": units.deg_to_rad(25.0),
}
TRIM_RANGE = {
    "gaff": (units.deg_to_rad(18.0), units.deg_to_rad(85.0)),
    "jibheaded": (units.deg_to_rad(15.0), units.deg_to_rad(60.0)),
    "lug": (units.deg_to_rad(8.0), units.deg_to_rad(85.0)),
    "lateen": (units.deg_to_rad(8.0), units.deg_to_rad(85.0)),
    "sprit": (units.deg_to_rad(8.0), units.deg_to_rad(85.0)),
}


def wanted_sheet_angle(cls: str, apparent_wind_angle: float) -> float:
    lo, hi = TRIM_RANGE[cls]
    return max(lo, min(hi, abs(apparent_wind_angle) - TRIM_OFFSET[cls]))


def tend_sheets(ship: Ship, dt: float) -> None:
    """Move every set fore-and-aft sail's sheet toward its trim, a little per tick."""
    awa = ship.dyn.apparent_wind_angle
    if ship.dyn.apparent_wind_speed < 0.5:
        return
    step = SHEET_RATE * dt
    for sail in ship.sails.values():
        if not sail.is_set or not sail.is_fore_and_aft:
            continue
        wanted = wanted_sheet_angle(sail.cls, awa)
        delta = wanted - sail.sheet_angle
        if abs(delta) <= step:
            sail.sheet_angle = wanted
        else:
            sail.sheet_angle += step if delta > 0 else -step
