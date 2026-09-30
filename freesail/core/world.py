"""The World: owns the clock, the wind, the weather, the ship, the log and the order journal.

A World knows nothing about who is driving it. It offers exactly:
load (construct), `submit` an order, `tick` once, read `log`, query `state`,
and `save`. Determinism: same seed, same scenario, same ship, same
(tick, order) journal, same log digest.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta
from typing import Any

from freesail import units
from freesail.core.clock import Clock
from freesail.core.events import Event, Log, Severity
from freesail.core.rng import Rng
from freesail.core.sun import DAY, DEFAULT_LATITUDE_DEG, Sun
from freesail.physics.wind import Wind, WindParams, WindRecord
from freesail.ship.stub import OrderError, PointShip
from freesail.world.geo import Position

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
    # The geographic frame (spec M5 §9, package 32; `freesail.world.geo`): where the ship
    # starts, as {"lat_deg", "lon_deg"}, in place of the bare latitude the sun used. With a
    # position the World keeps her latitude and longitude, advanced at the end of each tick
    # from the tick's run in metres, and the sun reads the ship's latitude; `latitude_deg`
    # is set from it at load. None: the endless plane of the earlier milestones, `ship_x`
    # and `ship_y` metres from the start, every constant as it was. A save from before the
    # frame loads with None.
    position: dict[str, float] | None = None
    # The chart region (spec M5 §10; `freesail.world.chart`): a region of data/charts/ by
    # its name in the manifest, loaded when the scenario names one and the position lies
    # in it; the depth, the coast, the features in sight and the grounding check read it.
    # None: no chart, and the queries read None ("no chart of these waters").
    region: str | None = None
    # The weather script (spec M4 §19, `freesail.world.weather_script`): waypoints as plain
    # dictionaries ({"at": ISO time, "from_deg": degrees, "knots": knots}), saved with the
    # scenario and so followed again by a replay. Empty: the fixed wind above. With a
    # script, the wind at the start is the script's and `wind_from_deg` and
    # `wind_speed_kn` are not read. A save from before the script loads with none.
    weather: list[dict[str, Any]] = field(default_factory=list)
    # The weather systems (spec M5 §2, `freesail.world.weather`, package 30): scripted
    # systems as plain dictionaries ({"name", "kind", "radius_km", "fronts", "track":
    # [{"at", "x_km", "y_km", "hpa"}, ...]}), followed exactly and saved with the scenario;
    # `climatology` seeds systems from the month's table instead when none is scripted.
    # With systems and no `weather` script the systems' surface wind at the ship is the
    # base wind; with both, the pinned script wins and the systems give only the sky and
    # the glass. Neither: no sky, no glass, the wind as it was.
    systems: list[dict[str, Any]] = field(default_factory=list)
    climatology: bool = False
    # The background under scripted systems: {"hpa": the mean pressure, "gradient_hpa_per_100km",
    # "high_toward_deg"}; empty means 1015 hPa and no gradient (`weather.BACKGROUND_HPA`).
    background: dict[str, Any] = field(default_factory=dict)
    # Whether the ship carries a glass (spec M5 §5; W §1.7: the captain's own in 1805, rare
    # in a small vessel); the scenario says, and without one the glass and its tendency
    # are not to be had.
    glass: bool = False
    # The sea and the ship's motion (spec M5 §4, package 31; `freesail.world.sea`,
    # `physics.motion`): kept when the wind has a cause (the systems drive it and no
    # `weather` script pins it), as the sky is, or when the scenario says `sea: true`
    # under a fixed or a pinned wind; `false` keeps none. None: the rule above. A fixed or
    # a pinned wind alone keeps no sea, which is how every truth before this one is
    # measured, so none of them moves. A save from before the sea loads with None.
    sea: bool | None = None

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

# The motion's words must hold this long before the log says they changed (spec M5 §4;
# judgement: five minutes, so a roll hovering about "rolling" and "rolling easily" is
# not a line a minute).
MOTION_WORDS_HOLD_S = 300

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
# to a station (package 29, the owner's ruling: a `tell` is seen in the log at any speed),
# and work belayed at his word, with how it was left (package 29c).
NOTABLE_ORDER_KINDS = frozenset({"agent.told", "work.belayed"})


class World:
    WIND_SHIFT_LOG_THRESHOLD = 2 * units.POINT

    def __init__(self, seed: int, scenario: Scenario | None = None, ship: Any = None):
        self.seed = int(seed)
        self.scenario = scenario or Scenario()
        self.clock = Clock(self.scenario.start_time)
        self.rng = Rng(self.seed)
        self.log = Log()
        # The geographic frame (spec M5 §9): with a `position` the ship's latitude and
        # longitude are kept and advanced at the end of each tick from her run in metres
        # (`freesail.world.geo`), and the sun reads her latitude; without one the plane is
        # what it was and the sun reads the scenario's latitude.
        self.origin: Position | None = (
            Position.from_dict(self.scenario.position) if self.scenario.position else None
        )
        # The chart (spec M5 §10, §11) and the lookout (§12), when the scenario names a
        # region: the depth under the keel, the grounding check every tick, the coast for
        # the weather's sea breeze and fog, and what is in sight once a minute.
        self.chart: Any = None
        self.lookout: Any = None
        self._aground: bool = False
        if self.scenario.region:
            from freesail.world.chart import load_chart
            from freesail.world.lookout import Lookout

            if self.origin is None:
                raise ValueError(
                    f"the scenario names the chart region '{self.scenario.region}' but "
                    f"gives no position; a chart needs to know where she is."
                )
            self.chart = load_chart(self.scenario.region)
            if not self.chart.contains(self.origin):
                raise ValueError(
                    f"the position {self.origin} lies outside the chart region "
                    f"'{self.scenario.region}' ({self.chart.bounds_words()})."
                )
            self.lookout = Lookout(self.chart)
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
        # The weather systems (spec M5 §2): scripted by the scenario or seeded from the
        # month's climatology, from the world's own `weather` stream (never the wind's).
        self.systems: Any = None
        self.glass: Any = None
        self.conditions: Any = None  # the sky and the weather at the ship, once a minute
        self._last_conditions: Any = None
        self.sea: Any = None  # the sea and the motion (spec M5 §4), made below
        self.motion: Any = None
        if self.scenario.systems or self.scenario.climatology:
            from freesail.world.weather import Glass, Weather, load_climatology

            self.systems = Weather(
                self.scenario.start_time,
                self.rng.stream("weather"),
                seed=self.seed,
                systems=self.scenario.systems,
                climatology=load_climatology() if self.scenario.climatology else None,
                background_hpa=self.scenario.background.get("hpa"),
                gradient=(
                    (
                        float(self.scenario.background.get("gradient_hpa_per_100km", 0.0)),
                        float(self.scenario.background.get("high_toward_deg", 0.0)),
                    )
                    if "gradient_hpa_per_100km" in self.scenario.background
                    else None
                ),
            )
            if self.scenario.glass:
                self.glass = Glass(self.seed)
            if self.chart is not None:
                # the coast the sea breeze and the coastal fog read (spec M5 §11; W §1.4)
                self.systems.coast = self._coast_of_plane
        self.wind = Wind(wind_params, self.rng.stream("wind"))
        # the true wind of the last ten minutes, for the mean wind reading (package 29b)
        self.wind_record = WindRecord()
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
        if self.systems is not None:
            self._observe_weather(first=True)
            if self.weather is None:
                # the systems' wind is the base: the wind starts on it (spec M5 §2)
                direction, speed = self.systems.surface_wind_at(self.ship_x_km, self.ship_y_km)
                self.wind = Wind(
                    WindParams(direction, speed, wind_params.gustiness, wind_params.variability),
                    self.rng.stream("wind"),
                )
                self.wind.air_mass = self.conditions.air_mass
        self._last_logged_wind_direction = self.wind.direction_from
        # The sea and the motion (spec M5 §4): the sea raised by the wind's ten-minute
        # mean once a minute, the motion relaxed toward what it gives every tick; the
        # ship's physics, strain and crew read the motion through `ship.extra["motion"]`.
        self._last_sea_words: str | None = None
        self._last_motion_words: str | None = None
        self._motion_pending: tuple[str, int] | None = None
        keeps_sea = self.scenario.sea
        if keeps_sea is None:
            keeps_sea = self.systems is not None and self.weather is None
        if keeps_sea:
            from freesail.physics.motion import Motion, Particulars
            from freesail.world.sea import Sea

            self.sea = Sea(self.clock.ship_time, self.wind.base_speed, self.wind.base_direction)
            self.motion = Motion(Particulars.of(self.ship))
            self._last_sea_words = self.sea.words
            self._last_sea_height = self.sea.reading().height_m
            self._last_motion_words = self.motion.words
            if getattr(self.ship, "extra", None) is not None:
                self.ship.extra["motion"] = self.motion
        # The sun (spec M4 §5): `daylight` is read from it through the registry, and the
        # World raises `sun.rise` and `sun.set` on the tick the phase crosses into and out
        # of day. The phase at the start is read and not announced: a sunrise that fell
        # before or at tick 0 (the default scenario opens at 04:00 on 1 June at 50 N, four
        # minutes after sunrise) is not an event of this log, so the first event is the
        # first crossing after the start, and a rule given at the start cannot fire on a
        # sun that rose before the book was opened.
        # The ship's position on the sphere (spec M5 §9): the origin at the start, then
        # advanced at the end of each tick from her run since the tick before.
        self._position: Position | None = self.origin
        self._geo_last: tuple[float, float] = (self.ship_x, self.ship_y)
        self.sun = Sun(
            self.origin.lat_deg if self.origin is not None else self.scenario.latitude_deg
        )
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
    def ship_y(self) -> float:
        """Metres north of the start."""
        dyn = getattr(self.ship, "dyn", None)
        if dyn is not None:
            return float(dyn.y)
        return float(getattr(self.ship, "y", 0.0))

    @property
    def ship_x_km(self) -> float:
        return self.ship_x / 1000.0

    @property
    def ship_y_km(self) -> float:
        return self.ship_y / 1000.0

    @property
    def position(self) -> Position | None:
        """Where she is on the sphere (spec M5 §9): the truth, which no reading gives
        (33's reckoning is the captain's account of it); None on the endless plane."""
        return self._position

    def _sun_now(self) -> Sun:
        """The sun at the ship's latitude now: the scenario's on the plane, hers with a
        position (the sun of spec M4 §5 "now reads the ship's", spec M5 §9)."""
        pos = self._position
        if pos is None or pos.lat_deg == self.sun.latitude_deg:
            return self.sun
        self.sun = Sun(pos.lat_deg)
        return self.sun

    @property
    def daylight(self) -> str:
        """'day', 'twilight' or 'night' now, from the sun at the ship's latitude and her
        easting (`freesail.core.sun`). The registry's `daylight` row reads this."""
        return self._sun_now().phase(self.clock.ship_time, self.ship_x)

    def sun_times(self) -> Any:
        """Today's dawn, sunrise, sunset and dusk by the clock (`sun.SunTimes`)."""
        return self._sun_now().times(self.clock.ship_time, self.ship_x)

    # -- the geographic frame and the chart (spec M5 §9 to §12) -----------------------

    def _tick_geo(self) -> None:
        """The tick's run in metres turned to latitude and longitude (C §5.1), at the end
        of the tick; nothing on the plane."""
        if self._position is None:
            return
        x, y = self.ship_x, self.ship_y
        lx, ly = self._geo_last
        if x != lx or y != ly:
            self._position = self._position.advanced(x - lx, y - ly)
            self._geo_last = (x, y)

    def _coast_of_plane(self, x_km: float, y_km: float) -> tuple[float, float] | None:
        """The weather's coast hook (spec M5 §11; W §1.4): for a point of the systems'
        plane, the distance to the nearest coast in kilometres and the bearing toward it
        in degrees, from the chart's distance field; None where the chart has no field."""
        if self.chart is None or self.origin is None:
            return None
        pos = self.origin.advanced(x_km * 1000.0, y_km * 1000.0)
        coast = self.chart.coast_at(pos)
        if coast is None:
            return None
        return coast.distance_m / 1000.0, coast.bearing_deg

    def _tick_chart(self) -> None:
        """Every tick the grounding check (spec M5 §11: short-circuited by the tile's
        minimum depth against the draught, the highest tide and a margin; otherwise the
        keel's cells at bow and stern); once a game minute the lookout (§12)."""
        pos = self._position
        if pos is None:
            return
        touched = self.chart.aground(
            pos,
            self.ship.heading,
            _ship_length_m(self.ship),
            _ship_draught_m(self.ship),
            _ship_heel(self.ship),
            tide_m=0.0,  # the tide of package 34 goes here
        )
        if touched is not None and not self._aground:
            self._aground = True
            self.record(
                Severity.URGENT,
                "ship.aground",
                touched.words,
                data=touched.to_dict()
                | {"speed_kn": round(units.ms_to_knots(_ship_speed(self.ship)), 1)},
            )
        elif touched is None and self._aground:
            self._aground = False
            self.record(Severity.NOTABLE, "ship.afloat", "She is off, and afloat again.")
        if self.lookout is not None and self.clock.ship_time.second == 0:
            for severity, kind, text, data in self.lookout.look(self):
                self.record(severity, kind, text, data=data)

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

    # -- the weather (spec M5 §2, §3, §5) ------------------------------------------

    def _observe_weather(self, first: bool = False) -> None:
        """Once a minute: the sky and the weather at the ship from the systems, the glass
        read into the ship's record, the wind's air mass set from the sector (when the
        systems drive the wind)."""
        t = self.clock.ship_time
        self.conditions = self.systems.conditions_at(self.ship_x_km, self.ship_y_km, t)
        if self.glass is not None:
            # the mercury pumps with the ship's motion (spec M5 §4)
            pumping = self.motion.pumping if self.motion is not None else 1.0
            self.glass.read(self.conditions.pressure_hpa, t, pumping)
        if self.weather is None and not first:
            self.wind.air_mass = self.conditions.air_mass
        if first:
            self._last_conditions = self.conditions
            if self.glass is not None:
                self.glass.mark_watch()  # the reference for the first change of the watch

    def _tick_weather(self) -> None:
        """The minute's weather lines: the sky and the weather when they change, the
        hour's line with the glass, and at the watch's change the glass's fall or rise
        since the watch before (spec M5 §5). No line names a front or a centre."""
        from freesail.world.weather import WEATHER_LINES

        self._observe_weather()
        t = self.clock.ship_time
        now, was = self.conditions, self._last_conditions
        if was is not None and now.sky != was.sky:
            signs = f", {now.signs}" if now.signs else ""
            self.record(
                Severity.ROUTINE,
                "weather.sky",
                f"The sky {now.sky}{signs}.",
                data={"sky": now.sky, "signs": now.signs, "visibility": now.visibility},
            )
        if was is not None and now.weather != was.weather:
            text = WEATHER_LINES.get((was.weather, now.weather)) or WEATHER_LINES[now.weather]
            self.record(
                Severity.NOTABLE if now.weather == "fog" else Severity.ROUTINE,
                "weather.change",
                text,
                data={"weather": now.weather, "was": was.weather, "visibility": now.visibility},
            )
        self._last_conditions = now
        if t.minute != 0:
            return
        hour = units.WATCHES
        watch_change = any(t.hour == start for start, _, _ in hour)
        signs = f", {now.signs}" if now.signs else ""
        text = f"{now.sky.capitalize()}{signs}, {now.weather}"
        data: dict[str, Any] = {
            "sky": now.sky,
            "signs": now.signs,
            "weather": now.weather,
            "visibility": now.visibility,
        }
        if self.glass is not None and self.glass.reading_in is not None:
            reading = self.glass.reading_in
            data["glass_in"] = reading
            data["change_in"] = self.glass.change_over(1.0)
            text += f"; the glass {reading:.2f}"
            if watch_change:
                change = self.glass.mark_watch()
                data["since_watch_in"] = change
                if change is not None:
                    since = units.watch_of(t - timedelta(minutes=1))[1].lower()
                    text += f", {_hundredths(change)} since the {since}"
        if self.sea is not None:
            # the sea by the hour (spec M5 §4), for the roll-up
            data["sea"] = self.sea.words
            data["motion"] = self.motion.words
            text += f"; {self.sea.words}, {self.motion.words}"
        self.record(Severity.ROUTINE, "weather.hour", text + ".", data=data)

    # -- the sea and the motion (spec M5 §4) --------------------------------------

    def _tick_sea(self) -> None:
        """Once a minute: the sea raised by the wind's ten-minute mean, and a line when
        its words change; the motion's words likewise."""
        record = self.wind_record
        mean = record.mean_speed()
        mean_from = record.mean_from()
        if mean is None or mean_from is None:
            mean, mean_from = self.wind.base_speed, self.wind.base_direction
        self.sea.tick(self.clock.ship_time, mean, mean_from)
        words = self.sea.words
        if words != self._last_sea_words:
            reading = self.sea.reading()
            rising = reading.height_m > self._last_sea_height
            self.record(
                Severity.ROUTINE,
                "sea.change",
                _sea_line(words, rising, reading.confused),
                data={"sea": words, "state": reading.state, "height_m": round(reading.height_m, 2)},
            )
            self._last_sea_words = words
        self._last_sea_height = self.sea.reading().height_m

    def _tick_motion(self) -> None:
        """Every tick: the motion toward what the sea gives on her heading; a line when
        its words have changed and held for MOTION_WORDS_HOLD_S (a roll hovering about a
        word's threshold is not a line every minute)."""
        self.motion.tick(1.0, self.sea, self.ship.heading)
        if self.clock.ship_time.second != 0:
            return
        words = self.motion.words
        if words == self._last_motion_words:
            self._motion_pending = None
            return
        if self._motion_pending is None or self._motion_pending[0] != words:
            self._motion_pending = (words, self.clock.tick)
        if self.clock.tick - self._motion_pending[1] >= MOTION_WORDS_HOLD_S:
            self._motion_pending = None
            reading = self.motion.reading()
            self.record(
                Severity.ROUTINE,
                "motion.change",
                _motion_line(words),
                data={
                    "motion": words,
                    "state": reading.state,
                    "roll_deg": round(reading.roll_deg, 1),
                    "pitch_deg": round(reading.pitch_deg, 1),
                },
            )
            self._last_motion_words = words

    def _log_squall(self) -> None:
        """A squall (spec M5 §3): notable at its start, with its veer and its wind, and at
        its end."""
        wind = self.wind
        kn = units.ms_to_knots(wind.effective_speed)
        if wind.squall_started:
            points = units.rad_to_points(wind.squall_veer)
            n = round(points)
            self.record(
                Severity.NOTABLE,
                "weather.squall",
                f"A squall: the wind veers {'a point' if n == 1 else f'{n} points'} to "
                f"{units.point_name(wind.direction_from)} and freshens to {kn:.0f} knots, "
                f"with rain.",
                data={
                    "factor": wind.squall_factor,
                    "veer_points": round(points, 2),
                    "knots": round(kn),
                    "mean_kn": round(units.ms_to_knots(self.wind_record.mean_speed() or 0.0), 1),
                    "air_mass": wind.air_mass,
                },
            )
        else:
            self.record(
                Severity.NOTABLE,
                "weather.squall_over",
                f"The squall passed; the wind {units.point_name(wind.direction_from)}, "
                f"{kn:.0f} knots.",
                data={"knots": round(kn)},
            )

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
        if self.systems is not None:
            # the systems move every tick (microseconds: a bell and two segments a system);
            # the sky and the glass are read once a minute (`_observe_weather`)
            self.systems.advance(self.clock.ship_time)
            if self.weather is None:
                self.wind.follow(*self.systems.surface_wind_at(self.ship_x_km, self.ship_y_km))
        if self.weather is not None:
            self.wind.follow(*self.weather.at(self.clock.ship_time))
        # the ten-minute mean, which the systems' regime draws its gusts and squalls as
        # multiples of (spec M5 §3); the M2 regime reads nothing and stays as it was
        mean = self.wind_record.mean_speed() if self.wind.air_mass is not None else None
        self.wind.step(1.0, mean)
        self.wind_record.add(self.wind.effective_speed, self.wind.direction_from)
        if self.wind.squall_started or self.wind.squall_ended:
            self._log_squall()
        if self.wind.gust_started:
            mean = units.ms_to_knots(self.wind_record.mean_speed() or self.wind.speed)
            self.record(
                Severity.ROUTINE,
                "wind.gust",
                f"A gust: {units.ms_to_knots(self.wind.effective_speed):.0f} knots, the mean "
                f"{mean:.0f}.",
                data={"factor": self.wind.gust_factor, "mean_kn": round(mean, 1)}
                | ({"air_mass": self.wind.air_mass} if self.wind.air_mass else {}),
            )
        shift = units.wrap_pi(self.wind.direction_from - self._last_logged_wind_direction)
        if abs(shift) >= self.WIND_SHIFT_LOG_THRESHOLD and not self.wind.in_squall:
            sense = "veered" if shift > 0 else "backed"
            self.record(
                Severity.NOTABLE,
                "wind.shift",
                f"Wind {sense} to {units.point_name(self.wind.direction_from)}, "
                f"{units.describe_wind_strength(self.wind.effective_speed)}.",
                data={"direction_from": self.wind.direction_from, "shift": shift},
            )
            self._last_logged_wind_direction = self.wind.direction_from
        if self.systems is not None and self.clock.ship_time.second == 0:
            self._tick_weather()
        if self.sea is not None:
            # the sea once a minute, the motion every tick, before the ship feels them
            if self.clock.ship_time.second == 0:
                self._tick_sea()
            self._tick_motion()
        for note in self.ship.step(1.0, self.wind):
            if len(note) == 3:
                self.record(*note)
            else:
                severity, kind, text, subject, data = note
                self.record(severity, kind, text, subject=subject, data=data)
        # the geographic frame (spec M5 §9): the tick's run turned to latitude and
        # longitude, then the chart's grounding check and the lookout (§11, §12)
        self._tick_geo()
        if self.chart is not None:
            self._tick_chart()
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
        out = {
            "tick": self.clock.tick,
            "ship_time": self.clock.ship_time.isoformat(),
            "stamp": self.clock.stamp(),
            "wind": self.wind.state(),
            "ship": self.ship.state(),
        }
        if self._position is not None:
            # the truth's position, for the tests and the tools; never a reading
            out["position"] = self._position.to_dict()
        return out

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
            *queries.weather_lines(self),
            *queries.lookout_lines(self),
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


def _ship_length_m(ship: Any) -> float:
    """The waterline length, for the keel's cells at bow and stern; a point ship has
    none and is checked at one cell."""
    hull = getattr(ship, "hull", None)
    return float(hull.spec.length_waterline_m) if hull is not None else 0.0


def _ship_draught_m(ship: Any) -> float:
    hull = getattr(ship, "hull", None)
    return float(hull.spec.draught_m) if hull is not None else 0.0


def _ship_heel(ship: Any) -> float:
    dyn = getattr(ship, "dyn", None)
    return float(dyn.heel) if dyn is not None else 0.0


def _ship_speed(ship: Any) -> float:
    dyn = getattr(ship, "dyn", None)
    return float(dyn.speed) if dyn is not None else float(getattr(ship, "speed", 0.0))


def _sea_line(words: str, rising: bool, confused: bool) -> str:
    """The log's line when the sea's words change: 'A heavy sea getting up.', 'A short
    chopping sea, the sea going down.', 'A confused sea, the swell from the westward.'"""
    head = words[:1].upper() + words[1:]
    if confused:
        return f"{head}."
    return f"{head} getting up." if rising else f"{head}, the sea going down."


def _motion_line(words: str) -> str:
    """'Rolling heavily.', 'Pitching into it.', 'She is easy.'"""
    if words == "easy":
        return "She is easy in it."
    return words[:1].upper() + words[1:] + "."


def _hundredths(change_in: float) -> str:
    """'fallen three hundredths', 'risen a tenth', 'steady': a change of the glass in the
    log's words (inches to the hundredth, as the vernier reads)."""
    n = round(abs(change_in) * 100)
    if n == 0:
        return "steady"
    verb = "risen" if change_in > 0 else "fallen"
    if n == 1:
        amount = "a hundredth"
    elif n == 10:
        amount = "a tenth"
    elif n == 20:
        amount = "two tenths"
    else:
        amount = f"{n} hundredths"
    return f"{verb} {amount}"
