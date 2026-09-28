"""The World: owns the clock, the wind, the ship, the log and the order journal.

A World knows nothing about who is driving it. It offers exactly:
load (construct), `submit` an order, `tick` once, read `log`, query `state`,
and `save`. Determinism: same seed, same scenario, same ship, same
(tick, order) journal, same log digest.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any

from freesail import units
from freesail.core.clock import Clock
from freesail.core.events import Event, Log, Severity
from freesail.core.rng import Rng
from freesail.core.sun import DAY, DEFAULT_LATITUDE_DEG, Sun
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
    # The sun's latitude (spec M4 §5): 50 N, the Channel. Saved and restored with the rest;
    # a save from before the sun loads with the default.
    latitude_deg: float = DEFAULT_LATITUDE_DEG
    # The weather script (spec M4 §19, `freesail.world.weather_script`): waypoints as plain
    # dictionaries ({"at": ISO time, "from_deg": degrees, "knots": knots}), saved with the
    # scenario and so followed again by a replay. Empty: the fixed wind above. With a
    # script, the wind at the start is the script's and `wind_from_deg` and
    # `wind_speed_kn` are not read. A save from before the script loads with none.
    weather: list[dict[str, Any]] = field(default_factory=list)

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

# What came into the World from outside between ticks, in the order it came (package 29,
# spec M4 §21: "save at any tick ... replay reproduces the digest"): every order given by
# anyone but a standing order, whether the ship carried it out, refused it or answered it
# as a query, and every line a driver wrote into the log (a save, a file of standing
# orders read, the compression eased on an alarm). `journal` keeps the orders carried out,
# as it always has; `inputs` is what a replay gives again, so that a refusal, a query and a
# driver's line are in the replayed log where they were in the original. Entries are
# {"tick", "actor", "order"} or {"tick", "line": {severity, kind, text, actor, data}}.
InputEntry = dict[str, Any]

# The actor a standing order's firing carries (spec M4 §4); `freesail.standing.runtime`
# writes it and the World knows a firing by it.
STANDING_ACTOR_PREFIX = "standing order "

# The log kinds an agent's harness writes (spec M4 §11, §12), listed in one place. Every
# one is written by `freesail.agents.harness` (or by a tool it runs) with the actor
# "the <station>", and the text of a note or an answer opens with the station's mark,
# "[watcher] ...", inline in the log (owner's ruling).
AGENT_LOG_KINDS: tuple[str, ...] = (
    "agent.stationed",  # an agent took a station; its policy in words
    "agent.note",  # the free text of a reply: the watcher's narration, routine
    "agent.said",  # an `answer` to an `ask`, notable
    "agent.asked",  # the captain's `ask the <station> ...` (an order, journaled)
    "agent.told",  # the captain's `tell the <station> ...` (an order, journaled), notable
    "agent.stand_down",  # the captain's `stand down the <station>` (an order, journaled)
    "agent.resume",  # the captain's `resume the <station>` (an order, journaled)
    "agent.refused",  # a tool call the station's authority does not allow
    "agent.stood_by",  # `stand_by(until=...)`: sampling suspended until the event or the bells
    "agent.resumed",  # sampling taken up again, after standing by or a pause
    "agent.nudged",  # the welfare detector fired once: the model told what was seen
    "agent.paused",  # the pattern went on: sampling paused, the human asked
    "agent.stopped",  # stood down: by the captain, or unattended past the bound
    "agent.opted_out",  # the token seen, or `opt_out` called
)
# `show the <station>'s journal` is answered as `query.journal`, a query like `state`.

# The kinds of an order's own line that are notable rather than routine: the captain's word
# to a station (package 29, the owner's ruling: a `tell` is seen in the log at any speed).
NOTABLE_ORDER_KINDS = frozenset({"agent.told"})


class World:
    WIND_SHIFT_LOG_THRESHOLD = 2 * units.POINT

    def __init__(self, seed: int, scenario: Scenario | None = None, ship: Any = None):
        self.seed = int(seed)
        self.scenario = scenario or Scenario()
        self.clock = Clock(self.scenario.start_time)
        self.rng = Rng(self.seed)
        self.log = Log()
        # The weather script (spec M4 §19): the base wind at every tick, from the scenario.
        self.weather: Any = None
        wind_params = WindParams.from_nautical(
            self.scenario.wind_from_deg,
            self.scenario.wind_speed_kn,
            self.scenario.gustiness,
            self.scenario.variability,
        )
        if self.scenario.weather:
            from freesail.world.weather_script import WeatherScript

            self.weather = WeatherScript.from_list(self.scenario.weather)
            direction, speed = self.weather.at(self.scenario.start_time)
            wind_params.direction_from, wind_params.speed = direction, speed
        self.wind = Wind(wind_params, self.rng.stream("wind"))
        self.ship = ship or PointShip(
            x=self.scenario.ship_x,
            y=self.scenario.ship_y,
            heading=units.deg_to_rad(self.scenario.ship_heading_deg),
            speed=units.knots_to_ms(self.scenario.ship_speed_kn),
        )
        self.journal: list[JournalEntry] = []
        self.inputs: list[InputEntry] = []
        # The compression the driver runs the clock at (game seconds a real second). The
        # World never reads it: the log's views do (the roll-up in an agent's samples, spec
        # M4 §20 and open item 8), and the driver sets it. Not saved, not in the digest.
        self.compression: float = 1.0
        if getattr(self.ship, "extra", None) is not None:
            self.ship.extra["rng"] = self.rng  # named streams for strain and later systems
        self._last_logged_wind_direction = self.wind.direction_from
        # The sun (spec M4 §5): `daylight` is read from it through the registry, and the
        # World raises `sun.rise` and `sun.set` on the tick the phase crosses into and out
        # of day. The phase at the start is read and not announced: a sunrise that fell
        # before or at tick 0 (the default scenario opens at 04:00 on 1 June at 50 N, four
        # minutes after sunrise) is not an event of this log, so the first event is the
        # first crossing after the start, and a rule given at the start cannot fire on a
        # sun that rose before the book was opened.
        self.sun = Sun(self.scenario.latitude_deg)
        self._daylight = self.daylight
        # The readings (spec M4 §2): one view per tick and per order, read by the standing
        # orders, the snapshot and the agents alike.
        self._readings_key: tuple[int, int] | None = None
        self._readings_view: Any = None
        # The standing orders' runtime and book (spec M4 §3, §4), evaluated last in `tick`.
        from freesail.standing.runtime import Runtime

        self.standing = Runtime(self)
        if getattr(self.ship, "extra", None) is not None:
            self.ship.extra["standing"] = self.standing
        # The agents at their stations (spec M4 §11), by station name, in the order they
        # were stationed: each is a `freesail.agents.harness.Harness`, called after the
        # standing orders on every tick (`on_tick`) and after every order (`on_order`, for
        # `ask`). The orders module reaches them through `ship.extra["agents"]` as it
        # reaches the book. Journals outlive their agents (a released station's journal
        # is still shown and saved), so they are kept apart, by station name.
        self.agents: dict[str, Any] = {}
        self.agent_journals: dict[str, Any] = {}
        if getattr(self.ship, "extra", None) is not None:
            self.ship.extra["agents"] = self.agents
            self.ship.extra["agent_journals"] = self.agent_journals
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

    # -- the sun -------------------------------------------------------------

    @property
    def ship_x(self) -> float:
        """Metres east of the start: the ship's own easting, whatever ship she is."""
        dyn = getattr(self.ship, "dyn", None)
        if dyn is not None:
            return float(dyn.x)
        return float(getattr(self.ship, "x", 0.0))

    @property
    def daylight(self) -> str:
        """'day', 'twilight' or 'night' now, from the sun at the ship's latitude and her
        easting (`freesail.core.sun`). The registry's `daylight` row reads this."""
        return self.sun.phase(self.clock.ship_time, self.ship_x)

    def sun_times(self) -> Any:
        """Today's dawn, sunrise, sunset and dusk by the clock (`sun.SunTimes`)."""
        return self.sun.times(self.clock.ship_time, self.ship_x)

    def _tick_sun(self) -> None:
        phase = self.daylight
        was = self._daylight
        if phase == was:
            return
        self._daylight = phase
        if was == DAY and phase != DAY:
            self.record(Severity.NOTABLE, "sun.set", "Sunset.", data={"daylight": phase})
        elif phase == DAY and was != DAY:
            self.record(Severity.NOTABLE, "sun.rise", "Sunrise.", data={"daylight": phase})

    # -- readings ------------------------------------------------------------

    @property
    def readings(self) -> Any:
        """The readings registry's view of this world now (`freesail.api.readings`).

        Cached per tick and per order: the key is the tick and the log's length, since an
        order can change a line's state at once and every order writes a log line. The
        standing orders' runtime takes one view for a whole pass; the snapshot and an
        agent's `readings()` read the same one.
        """
        from freesail.api.readings import REGISTRY

        key = (self.clock.tick, len(self.log))
        if self._readings_key != key:
            self._readings_view = REGISTRY.at(self)
            self._readings_key = key
        return self._readings_view

    # -- orders --------------------------------------------------------------

    def submit(self, text: str, actor: str = "captain", said: str | None = None) -> Event:
        """Apply an order now, at the current tick. Journal it if accepted.

        A standing order's firing comes with the actor "standing order 'x'" (spec M4 §4):
        it is logged as "By standing order 'x': ..." (`said`, notable) and not journaled,
        since firings are a deterministic function of the seed and the journal. A query
        (a kind beginning `query.`, such as the book's listing) is answered in the log
        and not journaled either.
        """
        text = " ".join(text.split())
        standing = actor.startswith(STANDING_ACTOR_PREFIX)
        if not standing:
            self.inputs.append({"tick": self.clock.tick, "actor": actor, "order": text})
        try:
            kind, log_text, data = self.ship.handle_order(text)
        except OrderError as e:
            head = f"{actor[0].upper()}{actor[1:]}: order" if standing else "Order"
            return self.record(
                Severity.ROUTINE,
                "order.rejected",
                f"{head} not carried out ({text!r}): {e}",
                actor=actor,
                data={"order": text, "reason": str(e)},
            )
        if kind.startswith("query."):
            return self.record(Severity.ROUTINE, kind, log_text, actor=actor, data=data)
        if not standing:
            self.journal.append((self.clock.tick, actor, text))
        accepted = self.record(
            Severity.NOTABLE if standing else Severity.ROUTINE,
            "order.accepted",
            f"{said}." if said else f"Order: {text}.",
            actor=actor,
            data={"order": text},
        )
        if kind == "evolution.started" and not data.get("failed"):
            # the evolution runner writes its own "started" line; avoid saying it twice
            self._after_order()
            return accepted
        severity = Severity.NOTABLE if kind in NOTABLE_ORDER_KINDS else Severity.ROUTINE
        event = self.record(severity, kind, log_text, actor=actor, data=data)
        self._after_order()
        return event

    def record_driver(
        self,
        severity: Severity | str,
        kind: str,
        text: str,
        data: dict[str, Any] | None = None,
    ) -> Event:
        """A line a driver writes into the log between ticks (a save, a file read, the
        compression eased on an alarm), with the actor "driver". Kept in `inputs`, so a
        replay writes it again at the same point and the digests agree."""
        sev = severity if isinstance(severity, Severity) else Severity(severity)
        line = {"severity": sev.value, "kind": kind, "text": text, "data": dict(data or {})}
        self.inputs.append({"tick": self.clock.tick, "line": line})
        return self.record(sev, kind, text, actor="driver", data=dict(data or {}))

    def _after_order(self) -> None:
        """An order was carried out and logged: the agents may act on it now (a question
        put by `ask` is answered on the tick it was asked, spec M4 §12)."""
        for agent in list(self.agents.values()):
            agent.on_order()

    # -- time ----------------------------------------------------------------

    def tick(self) -> None:
        """Advance the world by one game second."""
        self.clock.advance()
        if self.weather is not None:
            self.wind.follow(*self.weather.at(self.clock.ship_time))
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
        # the sun (spec M4 §5): sunrise and sunset, before the book so that `at sunset`
        # fires on the sun's own tick
        self._tick_sun()
        # the standing orders (spec M4 §4): last, on the tick's settled readings
        self.standing.tick()
        # the agents (spec M4 §11): after the book, so a sample carries the tick whole
        for agent in list(self.agents.values()):
            agent.on_tick()

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
        daylight = str(self.readings["daylight"]).capitalize()  # through the registry
        return [
            self.clock.stamp(),
            f"Wind {self.wind.describe()}, "
            f"{units.describe_wind_strength(self.wind.effective_speed)}",
            f"{daylight}. {self.sun_times().describe()}",
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
            # every order and driver's line in the order they came, which a replay gives
            # again (package 29); a save without it replays its journal
            "inputs": [dict(entry) for entry in self.inputs],
            # the book of standing orders (spec M4 §3): the orders' text and state, for the
            # reader; a replay re-enters them from the journal
            "standing_orders": self.standing.book.save(),
            # the agents (spec M4 §11): each station, its policy, its transcript (the
            # model's replies, which a replay plays back) and its journal
            "agents": [agent.save() for agent in self.agents.values()],
            "agent_journals": {name: j.save() for name, j in self.agent_journals.items()},
        }
