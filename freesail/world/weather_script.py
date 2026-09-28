"""The weather script (spec M4 §19): a scenario's timeline of the wind.

A script is a list of waypoints, each a ship's time, the direction the wind comes from
and its speed. Between two waypoints the wind turns and freshens (or eases) linearly in
time: the direction the short way round the compass, so a wind scripted from west to
north-west veers four points, and one from north-west to west backs them. Before the
first waypoint the wind is the first's; after the last it holds the last's.

What the script sets is the **base** wind, the one the wind model wanders about
(`physics.wind.Wind.follow`): the gustiness and the slow wander of direction and speed
ride on the scripted base exactly as they ride on a fixed one (spec §19: "with the
gustiness the wind model already has"). A turn the script makes is a turn of the true
wind like any other, so the log's `Wind veered to ...` lines and the readings'
`backs N points` and `veers N points` see it.

**Scenario data.** The script is part of the `Scenario` (its `weather`, a list of plain
dictionaries), so it is saved with the game beside the seed, and a replay, which rebuilds
the World from the scenario and the seed, follows the same script tick for tick. It is
given to the drivers in a scenario file (`freesail.world.scenarios`, `--scenario FILE`).

**The director's channel** (proposal §7.6; milestone 7b, spec M4 §24 item 3). The same
waypoints are what a director will write at run time: a world order such as "the wind to
back to south-west and rise to a gale by the middle watch" becomes a waypoint appended to
the script at the tick it is given, journaled as that tick's order, so a replay appends it
at the same tick and follows the same wind. Nothing here needs to change for that but an
`append` that refuses a waypoint earlier than the clock; this package does not build it.
"""

from __future__ import annotations

import bisect
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from freesail import units


class ScriptError(ValueError):
    """A weather script that cannot be followed, in words that name the waypoint."""


@dataclass(frozen=True)
class Waypoint:
    """The wind at one moment of the script: from `from_deg` (degrees true, where the wind
    comes from) at `knots` (at the reference height of ten metres, as `WindParams`)."""

    at: datetime
    from_deg: float
    knots: float

    def to_dict(self) -> dict[str, Any]:
        return {"at": self.at.isoformat(), "from_deg": self.from_deg, "knots": self.knots}

    @classmethod
    def from_dict(cls, d: Mapping[str, Any]) -> Waypoint:
        at = d.get("at")
        if isinstance(at, str):
            at = datetime.fromisoformat(at)
        if not isinstance(at, datetime):
            raise ScriptError(f"A waypoint needs a time ('at'), not {at!r}.")
        try:
            from_deg = float(d["from_deg"])
            knots = float(d["knots"])
        except (KeyError, TypeError, ValueError):
            raise ScriptError(
                f"The waypoint at {at.isoformat()} needs 'from_deg' and 'knots' as numbers."
            ) from None
        if knots < 0:
            raise ScriptError(f"The waypoint at {at.isoformat()} has a wind of {knots} knots.")
        return cls(at=at, from_deg=from_deg % 360.0, knots=knots)

    def describe(self) -> str:
        """'W, 18 knots (a fresh breeze) at 04:00 on 1 June'."""
        speed = units.knots_to_ms(self.knots)
        return (
            f"{units.point_name(units.deg_to_rad(self.from_deg))}, {self.knots:g} knots "
            f"({units.describe_wind_strength(speed)}) at {self.at.strftime('%H:%M')} "
            f"on {self.at.day} {self.at.strftime('%B')}"
        )


class WeatherScript:
    """The waypoints in time order, and the base wind at any moment between them."""

    def __init__(self, waypoints: Iterable[Waypoint]):
        points = list(waypoints)
        if not points:
            raise ScriptError("A weather script needs at least one waypoint.")
        for a, b in zip(points, points[1:], strict=False):
            if b.at <= a.at:
                raise ScriptError(
                    f"The waypoint at {b.at.isoformat()} is not after the one at "
                    f"{a.at.isoformat()}; a script runs forward in time."
                )
        self.waypoints: tuple[Waypoint, ...] = tuple(points)
        self._times = [p.at for p in points]

    @classmethod
    def from_list(cls, entries: Iterable[Mapping[str, Any]]) -> WeatherScript:
        return cls(Waypoint.from_dict(e) for e in entries)

    def to_list(self) -> list[dict[str, Any]]:
        return [p.to_dict() for p in self.waypoints]

    def at(self, when: datetime) -> tuple[float, float]:
        """The base wind at `when`: (direction from, radians in [0, 2 pi); speed, m/s)."""
        i = bisect.bisect_right(self._times, when)
        if i == 0:
            p = self.waypoints[0]
            return units.wrap_2pi(units.deg_to_rad(p.from_deg)), units.knots_to_ms(p.knots)
        if i == len(self.waypoints):
            p = self.waypoints[-1]
            return units.wrap_2pi(units.deg_to_rad(p.from_deg)), units.knots_to_ms(p.knots)
        a, b = self.waypoints[i - 1], self.waypoints[i]
        f = (when - a.at).total_seconds() / (b.at - a.at).total_seconds()
        a_dir = units.deg_to_rad(a.from_deg)
        turn = units.wrap_pi(units.deg_to_rad(b.from_deg) - a_dir)  # the short way round
        direction = units.wrap_2pi(a_dir + f * turn)
        knots = a.knots + f * (b.knots - a.knots)
        return direction, units.knots_to_ms(knots)

    def lines(self) -> list[str]:
        """The script in words, a line a waypoint, for the console and the gate report."""
        out = []
        for a, b in zip(self.waypoints, self.waypoints[1:], strict=False):
            turn = units.rad_to_points(
                units.wrap_pi(units.deg_to_rad(b.from_deg) - units.deg_to_rad(a.from_deg))
            )
            how = []
            if abs(turn) >= 0.5:
                sense = "veering" if turn > 0 else "backing"
                n = round(abs(turn))
                how.append(f"{sense} {n} point{'s' if n != 1 else ''}")
            if b.knots > a.knots:
                how.append("freshening")
            elif b.knots < a.knots:
                how.append("easing")
            out.append(f"From {a.describe()}, " + (" and ".join(how) or "steady") + ";")
        out.append(f"to {self.waypoints[-1].describe()}.")
        return out
