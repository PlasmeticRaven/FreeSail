"""The World: owns the clock, the wind, the weather, the ship, the log and the order journal.

A World knows nothing about who is driving it. It offers exactly:
load (construct), `submit` an order, `tick` once, read `log`, query `state`,
and `save`. Determinism: same seed, same scenario, same ship, same
(tick, order) journal, same log digest.
"""

from __future__ import annotations

import math
from dataclasses import MISSING, asdict, dataclass, field, fields, replace
from datetime import datetime, timedelta
from typing import Any

from freesail import units
from freesail.core.clock import TICK_SECONDS as TICK_S
from freesail.core.clock import Clock
from freesail.core.events import STATION_ACTORS, Event, Log, Severity
from freesail.core.rng import Rng
from freesail.core.sun import DAY, DEFAULT_LATITUDE_DEG, Sun
from freesail.physics.wind import AIR_MASSES, Wind, WindParams, WindRecord
from freesail.ship.stub import OrderError, PointShip
from freesail.world.geo import Position
from freesail.world.reckoning import NAVIGATION_KINDS

ENGINE_VERSION = "0.0.1"
SAVE_FORMAT = 1

# The build's stamp (package 37d; the review of gate 5c's playtests, section 9 under
# "Replay"): a save and its checkpoint say which build wrote them. `BUILD_NAME` is set by
# hand at each gate (the repository's: m5c-c, from the fold-in of the owner's local
# packages 37b to 37g). The fingerprint of the rules is computed once a process,
# at the first World made (`rules_fingerprint`), from the game's own code and the data a
# replay reads: every `freesail/**/*.py` and every file under `data/` but the chart's
# tiles (`data/charts/tiles/`, binary and large; the manifest that lists them is in), in
# the order of their paths written with forward slashes from the folder that holds
# `freesail/` and `data/`; for each the path, a zero byte, the file's bytes with every
# CR LF made LF (so that a Windows checkout and a Linux one agree), a zero byte; the
# first sixteen hex digits of the SHA-256 of the whole. `ENGINE_VERSION` and
# `SAVE_FORMAT` do not move for it, and a save without a stamp is read as "unstamped,
# before 37d" (`UNSTAMPED_WORDS`). A replay is promised only on the build that wrote the
# save (`core.replay.load`): the same fingerprint.
BUILD_NAME = "m5c-c"
BUILD_RULES_DIGITS = 16
UNSTAMPED_WORDS = "unstamped, before 37d"

_BUILD_RULES: str | None = None


def fingerprint_of(root: Any) -> str:
    """The fingerprint of the rules under a folder that holds `freesail/` and `data/`,
    by the set and the order written above."""
    import hashlib
    from pathlib import Path

    root = Path(root)
    code = root / "freesail"
    data = root / "data"
    tiles = data / "charts" / "tiles"
    files = [p for p in code.rglob("*.py") if "__pycache__" not in p.parts]
    if data.is_dir():
        files += [p for p in data.rglob("*") if p.is_file() and tiles not in p.parents]
    h = hashlib.sha256()
    for name, path in sorted((p.relative_to(root).as_posix(), p) for p in files):
        h.update(name.encode("utf-8") + b"\0")
        h.update(path.read_bytes().replace(b"\r\n", b"\n") + b"\0")
    return h.hexdigest()[:BUILD_RULES_DIGITS]


def rules_fingerprint() -> str:
    """The fingerprint of the rules this process runs by, computed once (some thirty
    milliseconds for two hundred files and four megabytes) and kept."""
    global _BUILD_RULES
    if _BUILD_RULES is None:
        from pathlib import Path

        _BUILD_RULES = fingerprint_of(Path(__file__).resolve().parents[2])
    return _BUILD_RULES


def build_stamp() -> dict[str, str]:
    """This build's stamp as a save and a checkpoint carry it: {"name", "rules"}."""
    return {"name": BUILD_NAME, "rules": rules_fingerprint()}


def build_words(stamp: Any) -> str:
    """A stamp in words, for the doors that load a save: 'm5c-c/37d, rules
    0123456789abcdef', or 'unstamped, before 37d' for a save that carries none."""
    if not isinstance(stamp, dict) or not stamp.get("rules"):
        return UNSTAMPED_WORDS
    return f"{stamp.get('name') or 'unnamed'}, rules {stamp['rules']}"


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
    # The chart (spec M6 §26; package 38): a chart of the manifest's `charts:` by its name
    # (`atlantic-east`: the regions it holds and the corridor under them), loaded in place
    # of `region` when both are given; `region` is kept as the name of a chart of that one
    # region, so that every scenario and save before this field works unchanged. A save
    # from before loads with None.
    chart: str | None = None
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
    # The air mass under a fixed or a pinned wind (spec M5 §3 as revised by package 31b, the
    # owner's ruling at gate 5a): "warm", "neutral" or "unstable", for the gust factor, the
    # squalls and the wander (`physics.wind`). A pinned script's waypoint may say its own
    # (`air_mass` beside its wind), which holds from that waypoint on; when the systems
    # drive the wind their sector says. A save from before loads with neutral.
    air_mass: str = "neutral"
    # The sea and the ship's motion (spec M5 §4, package 31; `freesail.world.sea`,
    # `physics.motion`): kept when the wind has a cause (the systems drive it and no
    # `weather` script pins it), as the sky is, or when the scenario says `sea: true`
    # under a fixed or a pinned wind; `false` keeps none. None: the rule above. A fixed or
    # a pinned wind alone keeps no sea, which is how every truth before this one is
    # measured, so none of them moves. A save from before the sea loads with None.
    sea: bool | None = None
    # The instrument the master takes the noon sight with (spec M5 §14, package 33a;
    # `freesail.world.sights`): "sextant" (the frigate's scenario) or "octant" (the
    # everyday instrument, and the schooner's). A save from before loads with the octant.
    instrument: str = "octant"
    # The set the world has and the master does not know of (spec M5 §13, package 33a): the
    # scenario's stated current as {"knots", "toward_deg"}, moving the truth's position
    # each tick and nothing of the ship's own motion; none by default, until package 34's
    # tide gives the world its streams.
    current: dict[str, float] | None = None
    # The sky pinned (package 33a, for the passage in thick weather, spec M5 §20): {"sky",
    # "weather", "visibility"} in the readings' words, laid over the systems' conditions
    # at the ship every minute; None: the systems' own. Needs weather systems to lay over.
    sky: dict[str, str] | None = None
    # The chronometer (package 33b; spec M5 §14; `freesail.world.sights.Chronometer`): the
    # captain's own, as {"maker", "rated": ISO date, "rate_s_per_day", "drift": "seeded"
    # or seconds a day, "forgotten": [ISO dates]}; None (the default, and every save from
    # before) is a ship without one, whose longitude is by account and by lunar.
    chronometer: dict[str, Any] | None = None
    # The captain's epitome (package 34; spec M5 §16; `freesail.world.tide.Epitome`): the
    # table of high water at full and change his tide is worked from, "norie" (the hours
    # and minutes of the period's tables, a ship of war's) or "moore" (Moore 1799's points
    # of the moon's bearing, the poorer table); None chooses by the ship (a ship of war
    # carries Norie's, the rest Moore's). The world's tide is not a scenario's choice.
    epitome: str | None = None
    # Package 35 (spec M5 §22 to §24, §27): the ship's nation (None: by the names list her
    # company is drawn from, `freesail.world.nations`); her people beyond the muster's
    # ([{"role", "name", "skill", "place"}]); her papers ({"price_lists": [port ids]} she
    # starts with); her cargo and purse ({"purse_pounds", "goods": {good: tons}}); and
    # the ports' state (a list of port ids, or {id: {"closed_to": [...], "letters":
    # [...], "news": [...]}}; None: every port file when the world has a chart). A save
    # from before loads with the defaults.
    nation: str | None = None
    people: list[dict[str, Any]] = field(default_factory=list)
    papers: dict[str, Any] = field(default_factory=dict)
    cargo: dict[str, Any] = field(default_factory=dict)
    ports: Any = None
    # Package 36 (spec M5 §25 to §27): the other sail on the sea at the start, each
    # {"id", "description", "name", "nation", "position", "goal", "colours"}
    # (`freesail.world.ships.vessel_from_spec`), and the world orders by time, each
    # {"at": ISO time, "order": the words} (`freesail.world.orders`), applied by the World
    # at their ticks and journaled at the driver's mark; a replay from the saved scenario
    # applies them again (truth 72). A save from before loads with none.
    ships: list[dict[str, Any]] = field(default_factory=list)
    world_orders: list[dict[str, Any]] = field(default_factory=list)
    # Package 40 (spec M6 §4): the captain's intent in words (`intent: trade tin from
    # Falmouth to Brest`), by which the rules-based captain sails her when no model holds
    # his station; "" for a scenario sailed by its book or by the player alone. `books`
    # names the scenario's standing-orders files, for `the captain` reading, so that a
    # save says by what she was sailed. A save from before loads with neither.
    intent: str = ""
    books: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        # a Scenario unpickled from a checkpoint of an earlier build lacks the fields
        # added since (a default-factory field is no class attribute): each is given its
        # default here, so that the save and the words read as a new game's would
        for f in fields(self):
            if not hasattr(self, f.name):
                if f.default is not MISSING:
                    setattr(self, f.name, f.default)
                elif f.default_factory is not MISSING:
                    setattr(self, f.name, f.default_factory())
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
# The actor a rules-based captain's judgement carries (spec M6 §4; package 40;
# `freesail.world.captains.ACTOR_PREFIX`): a rule's order, like a firing's, not journaled.
CAPTAIN_RULE_PREFIX = "captain's rule "
RULE_ACTOR_PREFIXES = (STANDING_ACTOR_PREFIX, CAPTAIN_RULE_PREFIX)

# The answers to an order that are the asker's alone and never a line of the log (package
# 40b): the master's slate, which an officer works his own reckoning from. `submit` hands
# such an answer back as an Event it does not record; a station reads it in its tool's
# result, and the console and the browser show it to the player who asked.
UNLOGGED_KINDS = frozenset({"query.slate"})

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
    # a station with authority (package 37, the officer of the watch)
    "agent.deck",  # the deck given, taken back, handed over; the captain's word for the watch
    "agent.handover",  # the handover note, said and journaled
)
# `show the <station>'s journal` is answered as `query.journal`, a query like `state`.

# The kinds of an order's own line that are notable rather than routine: the captain's word
# to a station (package 29, the owner's ruling: a `tell` is seen in the log at any speed),
# and work belayed at his word, with how it was left (package 29c).
NOTABLE_ORDER_KINDS = frozenset({"agent.told", "work.belayed", "agent.deck"})


# The key under which the ship holds the actor of the order being carried out (package
# 37g): there while `World.submit` runs the order's handler, and at no other time.
ORDER_ACTOR = "order_actor"


class World:
    # The log's `wind.shift` line (package 37c, the owner's ruling of 2026-10-03, closing
    # the M5 spec's open item 11): the ten-minute mean wind, as the readings and the
    # `a wind shift` event read it, two points from where the log last put it, and held
    # there `WIND_SHIFT_HOLD_S`. The instant wind it read before chattered across the
    # threshold many times a minute in a light, shifting air (the Harpy off Penlee).
    WIND_SHIFT_LOG_THRESHOLD = 2 * units.POINT
    WIND_SHIFT_HOLD_S = 60
    # seconds the mean has stood past the threshold; a class default so that a checkpoint
    # saved before package 37c loads with it
    _wind_shift_held_s = 0
    # Package 37f (the review of gate 5c's playtests, 5.8 and 8.2 under "The log": 31 of
    # game 9's 50 wind-shift lines came with under four knots of wind, 18 of them at
    # anchor in a calm, "Wind veered to S, calm."; and the Speedwell logged 23 shifts in
    # three hours and a half of a gentle breeze among the Scilly Isles, the wind swinging
    # in a slack gradient). A wind with no direction has no shift to log:
    #   - Airs too light: no line while the ten-minute mean is under a light breeze, four
    #     knots, where Beaufort's scale and the log's own words (`units.
    #     describe_wind_strength`) pass from "light airs" to "a light breeze". "Light and
    #     variable airs." is said once when it has been so `WIND_SHIFT_HOLD_S`, and the
    #     next settled wind once, when it has stood a light breeze `WIND_SETTLE_S` (five
    #     minutes; judgement: a puff across a calm is not the wind come back).
    #   - An unsteady wind: one whose mean swings back and forth. A shift that would be
    #     the wind's second turn within `WIND_SWING_S` (an hour; judgement: it has
    #     veered, backed, and now veers again, or the other way about) is not logged as
    #     a shift: "The wind unsteady, backing and veering about NW" is said once, and
    #     nothing more until the mean has stood within the shift's own two points for
    #     `WIND_STEADY_S` (half an hour; judgement), when the settled wind is said once.
    #     A wind that backs before a front and veers at it has turned once, and is
    #     logged as it was.
    # The event `a wind shift` keeps the same floor (`api.readings`): it does not come
    # while `wind_settled` is false. Class defaults, for a checkpoint saved before the
    # package.
    WIND_SHIFT_FLOOR_KN = 4.0
    WIND_SETTLE_S = 300
    WIND_SWING_S = 3600
    WIND_STEADY_S = 1800
    wind_settled = True
    _wind_unsettled_s = 0
    _wind_settling_s = 0
    _wind_unsettled_why = ""  # "light" or "swing" while `wind_settled` is false
    _wind_swing_ref: float | None = None  # where an unsteady wind's mean last stood
    _wind_shifts_said: tuple[tuple[int, int], ...] = ()  # the last shifts logged: tick, sense
    # The builds this game has been played under, oldest first (package 37d): this build's
    # stamp at the start, and each later build's added when it takes the game up from a
    # checkpoint (`core.replay._rebind`); None stands for a build from before the stamp.
    # Saved as `"builds"` beside `"build"`, so that a game begun under one build, loaded
    # from its checkpoint and saved again by another is not taken for the second's own
    # and replayed without a word. None as the class default: a checkpoint from before
    # the stamp loads with it and is given [None, this build].
    played_under: list[Any] | None = None
    # Package 37f, the dragging's lines and "Brought up" after an anchor let go by itself:
    # when each anchor's dragging was last spoken of and how far it had then come, and the
    # seconds she has lain still on a cable not yet said to have brought her up. Class
    # defaults, so that a checkpoint from an earlier build loads with them.
    _drag_said: dict[str, tuple[int, float]] | None = None
    _brought_up_s: int = 0
    # Package 37n (the owner's note 5 of 2026-10-09): the player's pencil on the captain's
    # chart, the lines, rings and notes he lays down in the browser, kept with the game:
    # saved as `"chart_marks"` and taken up again by the door that draws the chart
    # (`freesail.ui.server`); a checkpoint carries them with the rest. Read by nothing in
    # the simulation, the reckoning, the standing orders or a station: not in the log, the
    # journal, the readings or the snapshot. A tuple as the class default, so that a
    # checkpoint from an earlier build loads with none.
    chart_marks: list[dict[str, Any]] | tuple[()] = ()
    # Package 37k: for each anchor whose dragging the log has opened, its come-home
    # figure as last seen and the metres come home since the dragging began, across the
    # spells of it (the physics counts each spell afresh). A class default, as above.
    _drag_seen: dict[str, tuple[float, float]] | None = None

    def __init__(self, seed: int, scenario: Scenario | None = None, ship: Any = None):
        # the build's stamp, worked once at the start (package 37d)
        self.played_under = [build_stamp()]
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
        chart_name = self.scenario.chart or self.scenario.region
        if chart_name:
            from freesail.world.chart import load_chart
            from freesail.world.lookout import Lookout

            if self.origin is None:
                raise ValueError(
                    f"the scenario names the chart region '{chart_name}' but "
                    f"gives no position; a chart needs to know where she is."
                )
            self.chart = load_chart(chart_name)
            if not self.chart.contains(self.origin):
                raise ValueError(
                    f"the position {self.origin} lies outside the chart region "
                    f"'{chart_name}' ({self.chart.bounds_words()})."
                )
            self.lookout = Lookout(self.chart)
        # The tide (spec M5 §16, package 34; `freesail.world.tide`): the world's, wherever
        # the world has a chart, evaluated once a minute at the ship (`_tick_tide`): the
        # height under the lead and over the rocks that cover, the stream as the water's
        # velocity in the physics. No reading gives it. The grounding (§18,
        # `freesail.world.ground`) reads it every tick.
        self.tide: Any = None
        self.tide_state: Any = None
        self.ground: Any = None
        self._tide_was_flood: bool | None = None
        self._dragging: set[str] = set()
        if self.chart is not None:
            from freesail.world.ground import Ground
            from freesail.world.tide import load_tide

            self.tide = _tide_table(load_tide)
            self.ground = Ground(self)
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

            climatology = load_climatology() if self.scenario.climatology else None
            # the box she starts in (package 38; spec M6 §26): by her position, the
            # climatology's default (the Channel) on the plane
            box = (
                climatology.box_at(self.origin.lat_deg, self.origin.lon_deg)
                if climatology is not None and self.origin is not None
                else None
            )
            self.systems = Weather(
                self.scenario.start_time,
                self.rng.stream("weather"),
                seed=self.seed,
                systems=self.scenario.systems,
                climatology=climatology,
                box=box,
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
                # the coast the sea breeze and the coastal fog read (spec M5 §11; W §1.4),
                # and the coast's trend the breeze blows toward (package 37d)
                self.systems.coast = self._coast_of_plane
                self.systems.coast_trend = self._coast_trend_of_plane
        self.wind = Wind(wind_params, self.rng.stream("wind"))
        # the air mass of a fixed or a pinned wind (package 31b): the scenario's, or the
        # script's waypoint's from the first that names one
        if self.scenario.air_mass not in AIR_MASSES:
            raise ValueError(
                f"The scenario says the air is '{self.scenario.air_mass}'; say one of "
                f"{', '.join(AIR_MASSES)}."
            )
        self.wind.air_mass = self.scenario.air_mass
        if self.weather is not None:
            self.wind.air_mass = self.weather.air_mass_at(
                self.scenario.start_time, self.scenario.air_mass
            )
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
        # The reckoning (spec M5 §13 to §15; package 33a; `freesail.world.reckoning`): the
        # captain's account of where she is, kept beside the truth from the first tick
        # wherever the world has a position; the master, the log-line and the lead, the
        # noon sight and the day's work. The orders reach it through `ship.extra`.
        self.navigation: Any = None
        self._nav_pending: list[tuple[str, dict[str, Any]]] = []
        if self.origin is not None:
            from freesail.world.reckoning import Navigation

            if self.scenario.instrument not in ("sextant", "octant"):
                raise ValueError(
                    f"The scenario's instrument is '{self.scenario.instrument}'; say sextant "
                    f"or octant."
                )
            self.navigation = Navigation(self, self.rng.stream("reckoning"))
            if getattr(self.ship, "extra", None) is not None:
                self.ship.extra["navigation"] = self.navigation
        if self.tide is not None:
            self._tick_tide()  # the tide at the start, before the first look
        # The nations, the places with their ledgers, the people, the papers, the ports and
        # the other sail (spec M5 §22 to §25; package 35). The people are built at their
        # first call, the crew being mustered after the World is made (as the master is);
        # the ports load their files when the world has a chart, or when the scenario
        # names them; the vessels are the pilot cutter's list until package 36.
        from freesail.world.nations import load_nations
        from freesail.world.people import People
        from freesail.world.places import Hold, Papers, Places, Purse, Stores
        from freesail.world.ports import Ports
        from freesail.world.ships import Vessels

        self.nations = load_nations()
        self.places = Places(getattr(self.ship, "name", ""))
        self.people = People(self)
        self.papers = Papers(self)
        self.vessels = Vessels(self)
        hold_spec = getattr(getattr(self.ship, "spec", None), "hold", None)
        cargo = self.scenario.cargo or {}
        self.hold = Hold(float(hold_spec.capacity_tons) if hold_spec is not None else 0.0)
        for good, tons in (cargo.get("goods") or {}).items():
            self.hold.goods[str(good)] = float(tons)
        self.purse = Purse(float(cargo.get("purse_pounds", 0.0) or 0.0))
        crew_spec = getattr(getattr(self.ship, "spec", None), "crew", None)
        stores_spec = getattr(crew_spec, "stores", None)
        self.stores = Stores(
            float(getattr(stores_spec, "water_tons", 0.0) or 0.0),
            float(getattr(stores_spec, "provisions_days", 0.0) or 0.0),
        )
        self.ports = Ports(self)
        # The other sail on the sea at the start and the world orders by time (spec M5 §25
        # to §27; package 36; `freesail.world.ships`, `freesail.world.orders`): the ships
        # are the scenario's state, as the people are; the orders are applied at their
        # ticks by `_tick_world_orders` and kept in `world_orders` with their source, the
        # harness's with them (`world_order`).
        self.world_orders: list[dict[str, Any]] = []
        self._scenario_orders: list[tuple[int, str]] = sorted(
            (
                int(
                    (
                        datetime.fromisoformat(str(o["at"])) - self.scenario.start_time
                    ).total_seconds()
                ),
                str(o["order"]),
            )
            for o in self.scenario.world_orders
        )
        self._scenario_order_i = 0
        if self.scenario.ships:
            from freesail.world.ships import vessel_from_spec

            for spec in self.scenario.ships:
                self.vessels.serial += 1
                self.vessels.add(vessel_from_spec(self, dict(spec), self.vessels.serial))
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
        # the player's seat at a station below the captain's (package 40; `agents.seat`):
        # not a harness and not in `agents`; None while he is the captain at the prompt
        self.player_seat: Any = None
        if getattr(self.ship, "extra", None) is not None:
            self.ship.extra["agents"] = self.agents
            self.ship.extra["agent_journals"] = self.agent_journals
        # The rules-based captain (spec M6 §4; package 40; `freesail.world.captains`):
        # named for every ship, with the scenario's book or its intent; his judgements are
        # given only on an intent, when no model holds the captain's station with the deck,
        # after the book on every tick, so that the log reads as a captain's.
        from freesail.world.captains import Captain

        self.captain = Captain(
            self, intent=self.scenario.intent or None, books=tuple(self.scenario.books)
        )
        self.record(
            Severity.NOTABLE,
            "world.start",
            f"{self.scenario.name}. Wind {self.wind.describe()}, "
            f"{units.describe_wind_strength(self.wind.effective_speed)}. "
            f"Heading {units.format_heading(self.ship.heading)}.",
        )
        if self.lookout is not None:
            # the lookout's first look, at the start (spec M5 §12): what is in sight is a
            # reading from tick 0, and a landfall at the start is a line like any other
            for severity, kind, text, data in self.lookout.look(self):
                self.record(severity, kind, text, data=data)

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

    @property
    def tide_height_m(self) -> float:
        """The tide's height above the chart's datum at the ship now (spec M5 §16): the
        truth, under the lead and over the rocks; nothing where the world keeps no tide."""
        return float(self.tide_state.height_m) if self.tide_state is not None else 0.0

    @property
    def at_anchor(self) -> bool:
        tackle = (getattr(self.ship, "extra", None) or {}).get("ground_tackle")
        return bool(tackle) and tackle.at_anchor()

    def _tick_tide(self) -> None:
        """Once a minute (package 34): the tide at the ship, the stream given to the
        physics as the water's velocity, the water over her and over her anchors kept
        up, and at anchor the turn of the tide and an anchor dragging said."""
        pos = self._position
        if pos is None or self.tide is None:
            return
        from freesail.world.sights import greenwich_time

        state = self.tide.at(pos, greenwich_time(self))
        self.tide_state = state
        extra = getattr(self.ship, "extra", None)
        if extra is None:
            return
        extra["water"] = (state.stream_east_ms, state.stream_north_ms)
        extra["tide_state"] = state  # the scripts' riding words read it; never a reading
        depth = self.chart.depth_at(pos) if self.chart is not None else None
        extra["water_depth_m"] = None if depth is None else depth + state.height_m
        extra["bottom"] = self.chart.bottom_near(pos) if self.chart is not None else ""
        tackle = extra.get("ground_tackle")
        if not tackle or not tackle.at_anchor():
            self._tide_was_flood = None
            self._dragging.clear()
            return
        for anchor in tackle.down():
            if anchor.ground_x is None or anchor.ground_y is None:
                continue
            # where the anchor lies on the chart: from the ship's own place and the
            # anchor's offset from her (package 37d, `place_of_plane`); one jump from the
            # scenario's origin by the whole voyage's displacement fell a mile and a half
            # from her at Scilly, and on the land off Cawsand ("Brought up ... in no water")
            at = self.place_of_plane(anchor.ground_x, anchor.ground_y)
            d = self.chart.depth_at(at) if self.chart is not None and at is not None else None
            if d is not None:
                anchor.depth_m = max(0.0, d + state.height_m)
        # the turn of the tide, the ship's exposure of it: the cable slackens and she
        # swings (Luce 1884 App. K; Lever 1808, 'Single Anchor')
        flood = state.flood if not state.slack else None
        if flood is not None and self._tide_was_flood is not None and flood != self._tide_was_flood:
            from freesail.physics.anchor import riding_words

            which = "the flood" if flood else "the ebb"
            self.record(
                Severity.NOTABLE,
                "ship.swung",
                f"The cable slack at the turn; she swings to {which}. "
                f"{riding_words(self.ship, state, self.wind.direction_from)}",
                data={"flood": flood} | state.to_dict(),
            )
        if flood is not None:
            self._tide_was_flood = flood

    def _tick_anchors(self) -> None:
        """Every tick at anchor: an anchor beginning to drag is an urgent line with Luce's
        answers (notable until package 37d), and one holding again a routine line
        (package 34). The judgement of the
        drag over time is the physics' (`physics.anchor.judge_cables`).

        Package 37f (the review of gate 5c's playtests, 10.4: in the Goulet the anchors
        truly came home, two cables in eight hours, and the log said so eighteen times,
        each line urgent, waking the officer and easing the clock). Urgent once, when an
        anchor begins to come home, with the advice that is left to take (not "veer more
        cable" at the bitter end, nor an anchor that is down already). While it goes on,
        a notable line no oftener than `DRAG_REPORT_S`, with how far it has come, and
        only while it is still moving. And when she is brought up by an anchor let go by
        itself, the log says so, as `come to an anchor` always has.

        Package 37k (the review's G8, 37f's own note: on bare rock in a tideway an anchor
        held six minutes and came home again, and each relapse was a new urgent line,
        eight in the Goulet's eight hours with its ground forced to rock): a dragging is
        over only when the anchor has held `DRAG_HOLDS_AGAIN_S`, a quarter of an hour,
        and then the log says "holds again" with how far it came in all; one that comes
        home again within that is the same dragging, with no second urgent line, and its
        metres are counted on from where the first spell left them."""
        from freesail.physics.anchor import (
            DRAG_HOLDS_AGAIN_S,
            DRAG_REPORT_MIN_M,
            DRAG_REPORT_S,
        )

        tackle = (getattr(self.ship, "extra", None) or {}).get("ground_tackle")
        if not tackle:
            return
        said = self._drag_said
        if said is None:
            said = self._drag_said = {}
        seen = self._drag_seen
        if seen is None:
            seen = self._drag_seen = {}
        for anchor in tackle.anchors:
            if not anchor.down:
                self._dragging.discard(anchor.id)
                said.pop(anchor.id, None)
                seen.pop(anchor.id, None)
                continue
            name = f"{anchor.name[:1].upper()}{anchor.name[1:]}"
            if anchor.id in self._dragging:
                # the metres come home since the dragging began: what the physics' figure
                # has grown by since it was last seen, or the whole of it when a new
                # spell has begun its count afresh
                last, total = seen.get(anchor.id, (anchor.drag_m, anchor.drag_m))
                grown = anchor.drag_m - last if anchor.drag_m >= last else anchor.drag_m
                seen[anchor.id] = (anchor.drag_m, total + max(grown, 0.0))
            if anchor.dragging and anchor.id not in self._dragging:
                self._dragging.add(anchor.id)
                said[anchor.id] = (self.clock.tick, anchor.drag_m)
                seen[anchor.id] = (anchor.drag_m, anchor.drag_m)
                # urgent (package 37d; the review of gate 5c's playtests, 8.2 item 13): a
                # dragging anchor is a ship adrift toward whatever lies to leeward, and
                # a station standing by must be woken for it
                self.record(
                    Severity.URGENT,
                    "anchor.dragging",
                    f"{name} is dragging: {_dragging_advice(tackle, anchor)}.",
                    data=anchor.to_dict(),
                )
            elif anchor.dragging:
                total = seen.get(anchor.id, (anchor.drag_m, anchor.drag_m))[1]
                at, far = said.get(anchor.id, (self.clock.tick, total))
                if (
                    self.clock.tick - at >= DRAG_REPORT_S
                    and total - far >= DRAG_REPORT_MIN_M
                    and anchor.hold_s < 60.0
                ):
                    said[anchor.id] = (self.clock.tick, total)
                    self.record(
                        Severity.NOTABLE,
                        "anchor.coming_home",
                        f"{name} still coming home: {_come_home_words(total)} since it began.",
                        data=anchor.to_dict() | {"come_home_m": round(total, 1)},
                    )
            elif anchor.id in self._dragging and anchor.hold_s >= DRAG_HOLDS_AGAIN_S:
                self._dragging.discard(anchor.id)
                came = said.pop(anchor.id, (0, 0.0))[1]
                came = max(came, seen.pop(anchor.id, (0.0, 0.0))[1], anchor.drag_m)
                self.record(
                    Severity.ROUTINE,
                    "anchor.holding",
                    f"{name} holds again, having come home {_come_home_words(came)}."
                    if came >= 1.0
                    else f"{name} holds again.",
                    data=anchor.to_dict(),
                )
        self._say_brought_up(tackle)

    def _say_brought_up(self, tackle: Any) -> None:
        """ "Brought up" for an anchor let go by itself (package 37f; the review's 5.8:
        `let go the anchor` never said it, six stand-bys on the event never fired, and the
        captain needed sixty-seven minutes to be sure she rode). When no anchor's work is
        in hand and the anchor she rides by has not been said to bring her up: its cable
        taut and her way over the ground under three tenths of a metre a second for ten
        seconds (the evolution's own measure), or slack and she lying still for two
        minutes (a calm at slack water), and it not dragging."""
        riding = tackle.riding_by()
        if riding is None or riding.brought_up or riding.heaving or riding.dragging:
            self._brought_up_s = 0
            return
        runner = self.ship.extra.get("evolutions")
        for inst in getattr(runner, "instances", None) or ():
            if inst.evo.id in _ANCHOR_WORK and not inst.waiting:
                self._brought_up_s = 0
                return
        from freesail.evolutions.scripts import _ground_speed

        way = _ground_speed(self.ship)
        if way < (0.3 if riding.taut else 0.1):
            self._brought_up_s += 1
        else:
            self._brought_up_s = 0
        if self._brought_up_s < (10 if riding.taut else 120):
            return
        self._brought_up_s = 0
        riding.brought_up = True
        from freesail.evolutions.scripts import _depth_words, _fathoms_words, _riding

        self.record(
            Severity.NOTABLE,
            "ship.brought_up",
            f"Brought up by {riding.name} in {_depth_words(riding.depth_m)}, "
            f"{_fathoms_words(riding.scope_fathoms)} of cable; {_riding(self.ship, self.wind)}",
            data={"anchor": riding.to_dict(), "evolution": "let_go_anchor"},
        )

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
        dx, dy = x - lx, y - ly
        current = self.scenario.current
        if current:
            # the world's set (package 33a): the scenario's stated current moves her over
            # the ground and nothing of her motion through the water; the tide's stream
            # (package 34) is the physics' business, a water velocity, and sets a point
            # ship here as the stated current does
            kn = float(current.get("knots", 0.0))
            toward = math.radians(float(current.get("toward_deg", 0.0)))
            step = units.knots_to_ms(kn) * TICK_S
            dx += step * math.sin(toward)
            dy += step * math.cos(toward)
        if self.tide_state is not None and getattr(self.ship, "dyn", None) is None:
            dx += self.tide_state.stream_east_ms * TICK_S
            dy += self.tide_state.stream_north_ms * TICK_S
        if dx != 0.0 or dy != 0.0:
            self._position = self._position.advanced(dx, dy)
            self._geo_last = (x, y)

    def place_of_plane(self, x_m: float, y_m: float) -> Position | None:
        """Where a point of the ship's plane (metres east and north of the start) lies on
        the sphere: from the ship's own position and the point's offset from her (package
        37d). The one frame for every point of the plane: her place is carried forward
        tick by tick with the stated current in it (`_tick_geo`), and a point placed by
        one jump from the scenario's origin drifts from it with the miles run (a mile
        and a half at Scilly). `_geo_last` is the plane's point her position stands for.
        None on the endless plane."""
        pos = getattr(self, "_position", None)
        if pos is None:
            if self.origin is None:
                return None
            # the World still being made (the weather's first look comes before her
            # position is set): she lies at the origin
            return self.origin.advanced(x_m - self.ship_x, y_m - self.ship_y)
        lx, ly = self._geo_last
        return pos.advanced(x_m - lx, y_m - ly)

    def plane_of(self, pos: Position) -> tuple[float, float] | None:
        """The point of the ship's plane (metres east and north of the start) where a
        place on the sphere lies, by the same frame as `place_of_plane`; None on the
        endless plane."""
        if self._position is None:
            return None
        dx, dy = self._position.offset_to(pos)
        lx, ly = self._geo_last
        return lx + dx, ly + dy

    def _coast_of_plane(self, x_km: float, y_km: float) -> tuple[float, float] | None:
        """The weather's coast hook (spec M5 §11; W §1.4): for a point of the systems'
        plane, the distance to the nearest coast in kilometres and the bearing toward it
        in degrees, from the chart's distance field; None where the chart has no field.
        The point is placed from the ship's own position (package 37d), so the coast's
        distance at the ship is the chart's at her position."""
        if self.chart is None:
            return None
        pos = self.place_of_plane(x_km * 1000.0, y_km * 1000.0)
        if pos is None:
            return None
        found = self.chart.coast_distance(pos)  # the field alone: microseconds, no name
        if found is None:
            return None
        return found[0] / 1000.0, found[1]

    def _coast_trend_of_plane(self, x_km: float, y_km: float) -> tuple[float, float] | None:
        """The weather's second coast hook (package 37d; W §1.4): for a point of the
        systems' plane, the bearing toward the land as a whole in degrees and how steeply
        the shore's distance rises to seaward there (0 to 1), from the chart's distance
        field differenced over a baseline of kilometres (`chart.Chart.coast_trend`); None
        where the chart has no field. Read only while a sea breeze blows."""
        if self.chart is None:
            return None
        pos = self.place_of_plane(x_km * 1000.0, y_km * 1000.0)
        if pos is None:
            return None
        from freesail.world.weather import SEA_BREEZE_TREND_KM

        return self.chart.coast_trend(pos, SEA_BREEZE_TREND_KM * 1000.0)

    def _tick_chart(self) -> None:
        """Every tick the grounding check (spec M5 §11: short-circuited by the tile's
        minimum depth against the draught, the highest tide and a margin; otherwise the
        keel's cells at bow and stern); once a game minute the lookout (§12)."""
        pos = self._position
        if pos is None:
            return
        # the grounding and its consequences (spec M5 §18, package 34): the tide under
        # the keel and the charted dangers by name
        self.ground.tick()
        self._aground = self.ground.aground
        if self.at_anchor:
            self._tick_anchors()
        if self.lookout is not None and self.clock.ship_time.second == 0:
            for severity, kind, text, data in self.lookout.look(self):
                self.record(severity, kind, text, data=data)

    def _tick_vessels(self) -> None:
        """The other sail (spec M5 §25, package 36): every far-detail vessel once a game
        minute, at the roll-up's cadence and no oftener; a near-detail one every second;
        both before the lookout looks (`_tick_chart`). The lines their own events make
        (a letter brought alongside, a stranger within hail) are recorded here."""
        if self._position is None or not self.vessels.vessels:
            return
        lines = self.vessels.tick_near(self)
        if self.clock.ship_time.second == 0:
            lines = lines + self.vessels.tick(self)
        for severity, kind, text, data in lines:
            self.record(severity, kind, text, data=data)

    # -- the world-order channel (spec M5 §26; package 36) -----------------------------

    def world_order(self, text: str, source: str = "the harness") -> Event:
        """A world order from outside the scenario (the lead's test harness; the director
        of milestone 7b): journaled in `inputs` at this tick with its source, so that a
        replay gives it again, then carried out and logged at the driver's mark."""
        text = " ".join(str(text).split())
        self.inputs.append({"tick": self.clock.tick, "world_order": text, "source": str(source)})
        return self._apply_world_order(text, source)

    def _apply_world_order(self, text: str, source: str) -> Event:
        from freesail.world import orders as world_orders

        order = world_orders.parse(text)
        try:
            words, data = world_orders.apply(self, order)
            result = "done"
        except world_orders.WorldOrderError as e:
            words, data, result = f"not carried out: {str(e).rstrip('.')}", {}, "refused"
        self.world_orders.append(
            {
                "tick": self.clock.tick,
                "source": str(source),
                "order": text,
                "result": result,
                "words": words,
            }
        )
        return self.record(
            Severity.ROUTINE,
            "world.order",
            f"World order ({source}): {words}.",
            actor="driver",
            data={"order": text, "source": str(source), "channel": order.channel, "result": result}
            | data,
        )

    def _tick_world_orders(self) -> None:
        """The scenario's world orders due at this tick, in their order (a function of
        the scenario, applied again by a replay, as the standing orders' firings are)."""
        while (
            self._scenario_order_i < len(self._scenario_orders)
            and self._scenario_orders[self._scenario_order_i][0] <= self.clock.tick
        ):
            _, text = self._scenario_orders[self._scenario_order_i]
            self._scenario_order_i += 1
            self._apply_world_order(text, "the scenario")

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
        pos = getattr(self, "_position", None)
        if pos is not None:
            # where she is, for the climatology's box she is in and the point the next
            # system is drawn about (package 38); nothing on the plane, and nothing at the
            # first look, which comes before her position is set (she is at her start,
            # whose box the systems were seeded from)
            self.systems.locate(pos.lat_deg, pos.lon_deg, self.ship_x_km, self.ship_y_km)
        self.conditions = self.systems.conditions_at(self.ship_x_km, self.ship_y_km, t)
        if self.scenario.sky:
            # the sky pinned by the scenario (package 33a): laid over the systems' words
            self.conditions = replace(
                self.conditions,
                **{
                    k: str(v)
                    for k, v in self.scenario.sky.items()
                    if k in ("sky", "weather", "visibility") and v is not None
                },
            )
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

    def submit(
        self, text: str, actor: str = "captain", said: str | None = None, routine: bool = False
    ) -> Event:
        """Apply an order now, at the current tick. Journal it if accepted.

        A standing order's firing comes with the actor "standing order 'x'" (spec M4 §4):
        it is logged as "By standing order 'x': ..." (`said`, notable) and not journaled,
        since firings are a deterministic function of the seed and the journal. A firing
        on a cadence (`every glass then trim the sheets`, `... sound the well`) is the
        watch's routine work and its line is routine (`routine=True`, the standing runtime
        for an `every` trigger; the lead, 2026-09-30, after package 32e's tending routine
        put fifty-seven notable lines in a day): it stays in the log and the hourly roll-up
        and does not wake a watcher standing by. A query (a kind beginning `query.`, such
        as the book's listing) is answered in the log and not journaled either.
        """
        text = " ".join(text.split())
        # a firing's order, or a rules-based captain's judgement (package 40): logged as
        # the rule's and not journaled, a deterministic function of the seed and the journal
        standing = actor.startswith(RULE_ACTOR_PREFIXES)
        # an agent's station's order (package 37, the officer of the watch): given through
        # `World.submit` with the station's actor and refused by the same grammar, but not
        # journaled, since its replies are its harness's transcript and a replay gives
        # them again at their ticks (spec M4 §11; `freesail.agents.harness`)
        station = actor in STATION_ACTORS
        if not standing and not station:
            self.inputs.append({"tick": self.clock.tick, "actor": actor, "order": text})
        # whose order it is, for the lines that say so (package 37g, item 10: all hands
        # called by the officer of the watch were logged "by the captain's order"): kept
        # on the ship while the order is carried out and no longer (`orders.crew.
        # whose_order`), so it is never in a save or a checkpoint
        extra = getattr(self.ship, "extra", None)
        if isinstance(extra, dict):
            extra[ORDER_ACTOR] = actor
        try:
            try:
                kind, log_text, data = self.ship.handle_order(text)
            finally:
                if isinstance(extra, dict):
                    extra.pop(ORDER_ACTOR, None)
        except OrderError as e:
            head = f"{actor[0].upper()}{actor[1:]}: order" if standing else "Order"
            runtime = self.standing
            if standing and runtime is not None and not runtime.say_refused(text, str(e)):
                # a standing order's order refused as it was at its last firing: said
                # once a watch for each reason, not once a firing (package 37f); the
                # refusal goes back to the runtime all the same, unlogged
                return Event(
                    tick=self.clock.tick,
                    ship_time=self.clock.ship_time,
                    severity=Severity.ROUTINE,
                    kind="order.rejected",
                    text=f"{head} not carried out ({text!r}): {e}",
                    actor=actor,
                    data={"order": text, "reason": str(e), "unsaid": True},
                )
            return self.record(
                Severity.ROUTINE,
                "order.rejected",
                f"{head} not carried out ({text!r}): {e}",
                actor=actor,
                data={"order": text, "reason": str(e)},
            )
        if kind in UNLOGGED_KINDS:
            # a reading for the one who asked and for nobody else (package 40b: the
            # master's slate), answered and not written in the log
            return Event(
                tick=self.clock.tick,
                ship_time=self.clock.ship_time,
                severity=Severity.ROUTINE,
                kind=kind,
                text=log_text,
                actor=actor,
                data=data,
            )
        if kind.startswith("query."):
            return self.record(Severity.ROUTINE, kind, log_text, actor=actor, data=data)
        if not standing and not station:
            self.journal.append((self.clock.tick, actor, text))
        accepted = self.record(
            Severity.NOTABLE if standing and not routine else Severity.ROUTINE,
            "order.accepted",
            f"{said}." if said else f"Order: {text}.",
            actor=actor,
            data={"order": text},
        )
        if kind == "evolution.started" and not data.get("failed"):
            # the evolution runner writes its own "started" line; avoid saying it twice
            self._after_order()
            return accepted
        # notable by its kind, or because the order's own result says so (package 37d: a
        # fix that moved the account more than a mile; `data["notable"]`)
        notable = kind in NOTABLE_ORDER_KINDS or bool(data.get("notable"))
        severity = Severity.NOTABLE if notable else Severity.ROUTINE
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

    def _log_wind_shift(self) -> None:
        """The `wind.shift` line: the ten-minute mean wind two points or more from where
        the log last put it, and held there `WIND_SHIFT_HOLD_S`; not during a squall,
        which has its own line; and not of a wind too light or too unsteady to have a
        direction (package 37f, `_wind_has_a_direction`). The words give the mean's point
        and strength."""
        mean_from = self.wind_record.mean_from()
        if mean_from is None:
            return
        shift = units.wrap_pi(mean_from - self._last_logged_wind_direction)
        if self.wind.in_squall:
            self._wind_shift_held_s = 0
            return
        if not self._wind_has_a_direction(mean_from, shift):
            return
        if abs(shift) >= self.WIND_SHIFT_LOG_THRESHOLD:
            self._wind_shift_held_s += 1
        else:
            self._wind_shift_held_s = 0
            return
        if self._wind_shift_held_s < self.WIND_SHIFT_HOLD_S:
            return
        self._wind_shift_held_s = 0
        mean_speed = self.wind_record.mean_speed() or self.wind.speed
        strength = units.describe_wind_strength(mean_speed)
        tick = self.clock.tick
        sense = 1 if shift > 0 else -1
        recent = [s for s in self._wind_shifts_said if tick - s[0] <= self.WIND_SWING_S]
        senses = [s[1] for s in recent] + [sense]
        turns = sum(1 for was, now in zip(senses, senses[1:], strict=False) if was != now)
        if turns >= 2:
            # the wind's second turn within the hour (it has veered, backed, and veers
            # again, or the other way about): it is unsteady, and that is said in place
            # of the shift
            self.wind_settled = False
            self._wind_unsettled_why = "swing"
            self._wind_swing_ref = mean_from
            self._wind_settling_s = 0
            self._wind_shifts_said = ()
            self.record(
                Severity.NOTABLE,
                "wind.variable",
                f"The wind unsteady, backing and veering about {units.point_name(mean_from)}, "
                f"{strength}.",
                data={"direction_from": mean_from, "mean_kn": _knots(mean_speed)},
            )
            self._last_logged_wind_direction = mean_from
            return
        self._wind_shifts_said = tuple(recent) + ((tick, sense),)
        self.record(
            Severity.NOTABLE,
            "wind.shift",
            f"Wind {'veered' if sense > 0 else 'backed'} to {units.point_name(mean_from)}, "
            f"{strength}.",
            data={"direction_from": mean_from, "shift": shift, "mean": True},
        )
        self._last_logged_wind_direction = mean_from

    def _wind_has_a_direction(self, mean_from: float, shift: float) -> bool:
        """Whether the wind is settled enough to have a shift logged (package 37f; see
        `WIND_SHIFT_FLOOR_KN`), keeping `wind_settled` and saying each change of it once:
        "Light and variable airs." as it falls light, and the wind's point and strength
        when it has settled again, from light airs or from swinging, which is then where
        the next shift is measured from."""
        mean_speed = self.wind_record.mean_speed() or 0.0
        light = units.ms_to_knots(mean_speed) < self.WIND_SHIFT_FLOOR_KN
        if self.wind_settled or self._wind_unsettled_why == "swing":
            # falling light, from a settled wind or from an unsteady one
            if light:
                self._wind_shift_held_s = 0
                self._wind_unsettled_s += 1
                if self._wind_unsettled_s >= self.WIND_SHIFT_HOLD_S:
                    self.wind_settled = False
                    self._wind_unsettled_why = "light"
                    self._wind_unsettled_s = self._wind_settling_s = 0
                    self._wind_shifts_said = ()
                    self.record(
                        Severity.NOTABLE,
                        "wind.variable",
                        "Light and variable airs.",
                        data={"mean_kn": _knots(mean_speed)},
                    )
                return False
            self._wind_unsettled_s = 0
            if self.wind_settled:
                return True
        if self._wind_unsettled_why == "swing":
            # unsteady: settled when the mean has stood within the shift's own two points
            # for `WIND_STEADY_S`
            ref = mean_from if self._wind_swing_ref is None else self._wind_swing_ref
            if abs(units.wrap_pi(mean_from - ref)) >= self.WIND_SHIFT_LOG_THRESHOLD:
                self._wind_swing_ref = mean_from
                self._wind_settling_s = 0
                return False
            self._wind_swing_ref = ref
            self._wind_settling_s += 1
            if self._wind_settling_s < self.WIND_STEADY_S:
                return False
        else:
            # light airs: settled when the mean has stood a light breeze `WIND_SETTLE_S`
            if light:
                self._wind_settling_s = 0
                return False
            self._wind_settling_s += 1
            if self._wind_settling_s < self.WIND_SETTLE_S:
                return False
        self.wind_settled = True
        self._wind_unsettled_why = ""
        self._wind_swing_ref = None
        self._wind_settling_s = self._wind_shift_held_s = 0
        self.record(
            Severity.NOTABLE,
            "wind.shift",
            f"The wind has settled at {units.point_name(mean_from)}, "
            f"{units.describe_wind_strength(mean_speed)}.",
            data={"direction_from": mean_from, "shift": shift, "mean": True, "settled": True},
        )
        self._last_logged_wind_direction = mean_from
        return False

    # -- time ----------------------------------------------------------------

    def tick(self) -> None:
        """Advance the world by one game second."""
        self.clock.advance()
        if self._scenario_order_i < len(self._scenario_orders):
            # the scenario's world orders due now, before the weather moves (package 36)
            self._tick_world_orders()
        if self.systems is not None:
            # the systems move every tick (microseconds: a bell and two segments a system);
            # the sky and the glass are read once a minute (`_observe_weather`)
            self.systems.advance(self.clock.ship_time)
            if self.weather is None:
                self.wind.follow(*self.systems.surface_wind_at(self.ship_x_km, self.ship_y_km))
        if self.weather is not None:
            self.wind.follow(*self.weather.at(self.clock.ship_time))
            self.wind.air_mass = self.weather.air_mass_at(
                self.clock.ship_time, self.scenario.air_mass
            )
        # the ten-minute mean, which the gusts and squalls are drawn as multiples of (spec
        # M5 §3; under every wind since package 31b)
        self.wind.step(1.0, self.wind_record.mean_speed())
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
                data={
                    "factor": self.wind.gust_factor,
                    "mean_kn": round(mean, 1),
                    "air_mass": self.wind.air_mass,
                },
            )
        self._log_wind_shift()
        if self.systems is not None and self.clock.ship_time.second == 0:
            self._tick_weather()
        if self.sea is not None:
            # the sea once a minute, the motion every tick, before the ship feels them
            if self.clock.ship_time.second == 0:
                self._tick_sea()
            self._tick_motion()
        if self.tide is not None and self.clock.ship_time.second == 0:
            # the tide once a minute (spec M5 §16), before the ship feels the stream
            self._tick_tide()
        for note in self.ship.step(1.0, self.wind):
            if len(note) == 3:
                self.record(*note)
            else:
                severity, kind, text, subject, data = note
                if kind in NAVIGATION_KINDS and self.navigation is not None:
                    # the log or the lead is in (package 33a): the reckoning reads it after
                    # the tick's run is on the sphere and says the line itself
                    self._nav_pending.append((kind, dict(data or {})))
                    continue
                self.record(severity, kind, text, subject=subject, data=data)
        # the geographic frame (spec M5 §9): the tick's run turned to latitude and
        # longitude, then the chart's grounding check and the lookout (§11, §12)
        self._tick_geo()
        # the other sail move before the lookout looks (packages 35 and 36)
        self._tick_vessels()
        if self.chart is not None:
            self._tick_chart()
        if self.navigation is not None:
            # the reckoning (spec M5 §13, package 33a): the traverse board, the hourly
            # log, the casts and the noon, after the lookout has looked
            pending, self._nav_pending = self._nav_pending, []
            self.navigation.tick(pending)
        # the ports (spec M5 §23, package 35): the pilot's coming and going once a minute,
        # the yard's and the pool's jobs when due; then the people's tasks done, the moves
        # in hand finished and the letters delivered through the door (§22)
        self.ports.tick()
        for severity, kind, text, data in self.people.tick(self.clock.tick):
            self.record(severity, kind, text, data=data)
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
        # the rules-based captain (spec M6 §4; package 40): his judgements after the book,
        # once a minute, when they are his to give
        captain = getattr(self, "captain", None)
        if captain is not None:
            captain.tick()
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
            # the truth's position, for the tests and the tools; never a reading, and not in
            # the snapshot the client receives (`api.queries.snapshot` gives the reckoning)
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
        anchor_lines: list[str] = []
        if self.at_anchor or self._aground:
            # the ship riding, or aground (package 34), through the registry's words
            anchor_lines.append(self.readings.words("anchor"))
            if self.at_anchor:
                anchor_lines.append(self.readings.words("cable"))
        if self.ports.ports and self.readings["port"] is not None:
            # the port she is in or near, the pilot and the boat (package 35)
            anchor_lines.append(f"Port: {self.readings.words('port')}.")
        return [
            self.clock.stamp(),
            f"Wind {self.wind.describe()}, "
            f"{units.describe_wind_strength(self.wind.effective_speed)}",
            f"{daylight}. {self.sun_times().describe()}",
            *queries.weather_lines(self),
            *queries.lookout_lines(self),
            *queries.reckoning_lines(self),
            *anchor_lines,
            *ship_lines,
            *queries.watch_lines(self),
        ]

    # -- save ----------------------------------------------------------------

    def save(self) -> dict[str, Any]:
        """Everything needed to rebuild this world by replay: seed, scenario, journal."""
        return {
            "format": SAVE_FORMAT,
            "engine": ENGINE_VERSION,
            # the build that wrote this save (package 37d): its name and the fingerprint
            # of its rules; a replay is promised only under the same fingerprint
            "build": build_stamp(),
            # every build the game has been played under, oldest first (null: one from
            # before the stamp); more than this build's when it came by a checkpoint
            "builds": [dict(b) if b else None for b in (self.played_under or [None])],
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
            # the world orders applied, with their ticks and sources, for the reader (spec
            # M5 §26, package 36); a replay applies the scenario's again from the scenario
            # and the harness's from `inputs`
            "world_orders": [dict(o) for o in self.world_orders],
            # the player's pencil on the chart (package 37n), for the chart alone; a replay
            # makes none of it, and the door that draws the chart takes it up from here
            "chart_marks": [dict(m) for m in self.chart_marks],
        }


# The ground-tackle evolutions (`data/evolutions/`): while one is in hand the World does
# not say "Brought up" of itself (the evolution says its own, or the cable is still running).
_ANCHOR_WORK = frozenset(
    {
        "come_to_anchor",
        "let_go_anchor",
        "veer_cable",
        "heave_short",
        "heave_in",
        "weigh_anchor",
        "moor",
        "unmoor",
        "get_under_way",
        "back_anchor",
    }
)


def _come_home_words(metres: float) -> str:
    """How far an anchor has come home, in the log's words: 'three fathoms', 'half a
    cable', 'a cable', 'a cable and a half', 'two cables'."""
    from freesail.world.reckoning import number_words

    halves = int(round(metres / (units.CABLE / 2.0)))
    if halves < 1:
        fathoms = max(1, int(round(units.m_to_fathoms(metres))))
        return f"{number_words(fathoms)} fathom{'s' if fathoms != 1 else ''}"
    whole, half = divmod(halves, 2)
    if whole == 0:
        return "half a cable"
    if whole == 1:
        return "a cable and a half" if half else "a cable"
    return f"{number_words(whole)} cables{' and a half' if half else ''}"


def _dragging_advice(tackle: Any, anchor: Any) -> str:
    """Luce's answers to an anchor coming home, those that are left to take (package 37f:
    "veer more cable" was said at the bitter end, and of the second anchor when it was
    down already): veer more cable, while there is cable; let go another anchor, a bower
    first and then the sheet; back her with the stream, if it is at the bows."""
    from freesail.ship.parts import AnchorState

    advice = []
    if anchor.scope_fathoms < anchor.cable_fathoms - 1.0:
        advice.append("veer more cable")
    ready = (AnchorState.STOWED, AnchorState.READY)
    spare = [
        a
        for a in tackle.anchors
        if a is not anchor and a.state in ready and a.kind in ("bower", "sheet")
    ]
    spare.sort(key=lambda a: 0 if a.kind == "bower" else 1)
    if spare:
        advice.append(f"let go {spare[0].name}")
    stream = next((a for a in tackle.anchors if a.kind == "stream" and a.state in ready), None)
    if stream is not None and anchor.kind != "stream":
        advice.append("back her with the stream")
    if not advice:
        return "the whole of its cable is out and there is no anchor left to let go"
    if len(advice) == 1:
        return advice[0]
    if len(advice) == 2:
        return f"{advice[0]}, or {advice[1]}"
    return f"{advice[0]}; {advice[1]}, or {advice[2]}"


def _knots(speed_ms: float) -> float:
    return round(units.ms_to_knots(speed_ms), 1)


_TIDE: Any = None


def _tide_table(loader: Any) -> Any:
    """The tide's tables, read once and shared between Worlds (pure data; each World
    keeps its own state)."""
    global _TIDE
    if _TIDE is None:
        _TIDE = loader()
    return _TIDE


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
