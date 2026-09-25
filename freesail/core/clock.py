"""The ship's clock: ticks of one game second, watches and bells."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta

from freesail import units

TICK_SECONDS = 1.0


@dataclass
class Clock:
    """Counts ticks and converts them to ship's time.

    `tick` is the number of whole game seconds elapsed since `start`. Nothing
    happens between ticks; the physics may sub-step inside one, invisibly.
    """

    start: datetime
    tick: int = 0
    _bell_last_tick: int = field(default=-1, repr=False)

    @property
    def ship_time(self) -> datetime:
        return self.start + timedelta(seconds=self.tick)

    def advance(self) -> None:
        self.tick += 1

    def bells(self) -> int | None:
        """Bells struck at this tick, or None. Each tick reports at most once."""
        if self._bell_last_tick == self.tick:
            return None
        n = units.bells_at(self.ship_time)
        if n is not None:
            self._bell_last_tick = self.tick
        return n

    def stamp(self) -> str:
        return units.time_stamp(self.ship_time)

    def watch(self) -> str:
        return units.watch_of(self.ship_time)[1]
