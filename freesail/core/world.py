"""The World: owns the clock, the wind, the ship, the log and the order journal.

A World knows nothing about who is driving it. It offers exactly:
load (construct), `submit` an order, `tick` once, read `log`, query `state`,
and `save`. Determinism: same seed, same scenario, same ship, same
(tick, order) journal, same log digest.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any

from freesail import units
from freesail.core.clock import Clock
from freesail.core.events import Event, Log, Severity
from freesail.core.rng import Rng
from freesail.physics.wind import Wind, WindParams
from freesail.ship.stub import OrderError, PointShip

ENGINE_VERSION = "0.0.1"
SAVE_FORMAT = 1


@dataclass
class Scenario:
    """Starting conditions. Small on purpose; geography arrives in M5."""

    name: str = "Open water"
    start_time: datetime = datetime(1805, 6, 1, 4, 0, 0)
    wind_from_deg: float = 225.0
    wind_speed_kn: float = 15.0
    gustiness: float = 0.3
    variability: float = 0.3
    ship_x: float = 0.0
    ship_y: float = 0.0
    ship_heading_deg: float = 0.0
    ship_speed_kn: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["start_time"] = self.start_time.isoformat()
        return d

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Scenario:
        d = dict(d)
        d["start_time"] = datetime.fromisoformat(d["start_time"])
        return cls(**d)


JournalEntry = tuple[int, str, str]  # (tick, actor, order text)


class World:
    WIND_SHIFT_LOG_THRESHOLD = 2 * units.POINT

    def __init__(self, seed: int, scenario: Scenario | None = None, ship: Any = None):
        self.seed = int(seed)
        self.scenario = scenario or Scenario()
        self.clock = Clock(self.scenario.start_time)
        self.rng = Rng(self.seed)
        self.log = Log()
        self.wind = Wind(
            WindParams.from_nautical(
                self.scenario.wind_from_deg,
                self.scenario.wind_speed_kn,
                self.scenario.gustiness,
                self.scenario.variability,
            ),
            self.rng.stream("wind"),
        )
        self.ship = ship or PointShip(
            x=self.scenario.ship_x,
            y=self.scenario.ship_y,
            heading=units.deg_to_rad(self.scenario.ship_heading_deg),
            speed=units.knots_to_ms(self.scenario.ship_speed_kn),
        )
        self.journal: list[JournalEntry] = []
        if getattr(self.ship, "extra", None) is not None:
            self.ship.extra["rng"] = self.rng  # named streams for strain and later systems
        self._last_logged_wind_direction = self.wind.direction_from
        self.record(
            Severity.NOTABLE,
            "world.start",
            f"{self.scenario.name}. Wind {self.wind.describe()}, "
            f"{units.describe_wind_strength(self.wind.effective_speed)}. "
            f"Heading {units.format_heading(self.ship.heading)}.",
        )

    # -- logging -------------------------------------------------------------

    def record(
        self,
        severity: Severity | str,
        kind: str,
        text: str,
        actor: str = "sim",
        subject: str | None = None,
        data: dict[str, Any] | None = None,
    ) -> Event:
        sev = severity if isinstance(severity, Severity) else Severity(severity)
        return self.log.append(
            Event(
                tick=self.clock.tick,
                ship_time=self.clock.ship_time,
                severity=sev,
                kind=kind,
                text=text,
                actor=actor,
                subject=subject,
                data=data or {},
            )
        )

    # -- orders --------------------------------------------------------------

    def submit(self, text: str, actor: str = "captain") -> Event:
        """Apply an order now, at the current tick. Journal it if accepted."""
        text = " ".join(text.split())
        try:
            kind, log_text, data = self.ship.handle_order(text)
        except OrderError as e:
            return self.record(
                Severity.ROUTINE,
                "order.rejected",
                f"Order not carried out ({text!r}): {e}",
                actor=actor,
                data={"order": text, "reason": str(e)},
            )
        self.journal.append((self.clock.tick, actor, text))
        accepted = self.record(
            Severity.ROUTINE,
            "order.accepted",
            f"Order: {text}.",
            actor=actor,
            data={"order": text},
        )
        if kind == "evolution.started" and not data.get("failed"):
            # the evolution runner writes its own "started" line; avoid saying it twice
            return accepted
        return self.record(Severity.ROUTINE, kind, log_text, actor=actor, data=data)

    # -- time ----------------------------------------------------------------

    def tick(self) -> None:
        """Advance the world by one game second."""
        self.clock.advance()
        self.wind.step(1.0)
        if self.wind.gust_started:
            self.record(
                Severity.ROUTINE,
                "wind.gust",
                f"A gust: {units.ms_to_knots(self.wind.effective_speed):.0f} knots.",
                data={"factor": self.wind.gust_factor},
            )
        shift = units.wrap_pi(self.wind.direction_from - self._last_logged_wind_direction)
        if abs(shift) >= self.WIND_SHIFT_LOG_THRESHOLD:
            sense = "veered" if shift > 0 else "backed"
            self.record(
                Severity.NOTABLE,
                "wind.shift",
                f"Wind {sense} to {units.point_name(self.wind.direction_from)}, "
                f"{units.describe_wind_strength(self.wind.effective_speed)}.",
                data={"direction_from": self.wind.direction_from, "shift": shift},
            )
            self._last_logged_wind_direction = self.wind.direction_from
        for note in self.ship.step(1.0, self.wind):
            if len(note) == 3:
                self.record(*note)
            else:
                severity, kind, text, subject, data = note
                self.record(severity, kind, text, subject=subject, data=data)
        # the watch routine (spec M3 §4): watch changes, all hands, fatigue and rest
        routine = (getattr(self.ship, "extra", None) or {}).get("routine")
        if routine is not None:
            for note in routine.tick(self.ship, 1.0):
                if len(note) == 3:
                    self.record(*note)
                else:
                    severity, kind, text, subject, data = note
                    self.record(severity, kind, text, subject=subject, data=data)
        bells = self.clock.bells()
        if bells is not None:
            self.record(
                Severity.ROUTINE,
                "clock.bell",
                f"{units.format_bells(bells).capitalize()}.",
                data={"bells": bells},
            )

    def run(self, ticks: int) -> None:
        for _ in range(ticks):
            self.tick()

    # -- queries -------------------------------------------------------------

    def state(self) -> dict[str, Any]:
        return {
            "tick": self.clock.tick,
            "ship_time": self.clock.ship_time.isoformat(),
            "stamp": self.clock.stamp(),
            "wind": self.wind.state(),
            "ship": self.ship.state(),
        }

    def summary_lines(self) -> list[str]:
        """The console's `state`: the clock, the wind, the ship's own lines and, with a
        crew, the watch (spec M3 §5.2). The ship's 'Sail set' line is written afresh so
        that it shows the milestone 3 states (goose-winged, unbent, spars sent down)."""
        from freesail.api import queries

        ship_lines = list(self.ship.summary_lines())
        if hasattr(self.ship, "sails"):
            ship_lines = [
                queries.sail_set_line(self.ship) if ln.startswith("Sail set:") else ln
                for ln in ship_lines
            ]
        return [
            self.clock.stamp(),
            f"Wind {self.wind.describe()}, "
            f"{units.describe_wind_strength(self.wind.effective_speed)}",
            *ship_lines,
            *queries.watch_lines(self),
        ]

    # -- save ----------------------------------------------------------------

    def save(self) -> dict[str, Any]:
        """Everything needed to rebuild this world by replay: seed, scenario, journal."""
        return {
            "format": SAVE_FORMAT,
            "engine": ENGINE_VERSION,
            "seed": self.seed,
            "scenario": self.scenario.to_dict(),
            "ship_ref": self.ship.save_ref(),
            "end_tick": self.clock.tick,
            "journal": [list(entry) for entry in self.journal],
        }
