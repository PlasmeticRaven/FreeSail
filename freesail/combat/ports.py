"""The lee ports (package 75; docs/design/Build-Ships.md §3.1 item 17, §7): a gun's port shut
when the sea comes to its sill, and opened again when the sill stands clear of it.

**The rule** (§7.1, built by the gun deck's builder, B8): for a gun placed broadside, bow or
stern (`PORT_PLACES`; a pivot and a rail gun fire over the rail and have no port), the dip is
the heel toward the gun's side plus the roll's amplitude, never below nought; the sill
lowered is the gun's `height_m` less the side's half-breadth at the sill
(`ship.profile.half_breadth_at_sill`, else half the beam) times the sine of the dip; the port
is shut when the sill lowered is within `shot.PORT_SHUT_M` of the water
(`shot.lee_port_shut`), and opened again when it stands `PORT_REOPEN_M` clear of that, so
that a port does not flicker in a gust. The roll is the ship's own (`Firer.roll_deg`, from
her World's motion).

**Stage 0** lays the hook alone: `update` is called once a tick at the head of
`guns.Battery.tick`, the battery leaves out of its work and its fire every gun in
`Battery._shut`, and `update` shuts and opens nothing, so the set stays empty and nothing
moves. The events the rule will say (`guns.ports_shut`, `guns.ports_opened`) are registered
in `api/practice_readings.py`, absent until the rule is built, and never emitted yet.
"""

from __future__ import annotations

from typing import Any

__all__ = ["PORT_PLACES", "PORT_REOPEN_M", "update"]

# The places of a gun that fires through a port in the side, the bow or the stern (a pivot
# and a rail gun fire over the rail: docs/design/Proposal-PivotGun.md §4.4); the schema's
# gun deck rule reads the same three (`schema._PORT_GUN_PLACES`).
PORT_PLACES: tuple[str, ...] = ("broadside", "bow", "stern")
# A shut port is opened again when its sill lowered stands this far clear of the shut
# line: six inches (judgement), so that a port does not open and shut with each gust.
PORT_REOPEN_M = 0.15


def update(battery: Any, firer: Any) -> tuple[frozenset[str], frozenset[str]]:
    """The battery's ports this tick against the rule (the module's head): the ids of the
    guns whose ports were shut this tick and of those opened, each set once a change of
    state, the battery's `_shut` set to the guns now shut. Stage 0's hook: nothing is shut
    or opened, and the two sets are empty."""
    return frozenset(), frozenset()
