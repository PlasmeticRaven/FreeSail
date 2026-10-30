"""A hull's dealings with the ports (package 84, step 3; `docs/design/Design-OneWorld.md`
§2.4): the ship's half of what was one `Ports` class, the pilot and his conn, the cutter,
the boat and its errands, the price lists, the bargains, the yard and the pool, the jobs,
kept per hull on `world.dealings` (`Hull.dealings`); the port files, the markets, the
stances and the places ashore are the world's (`freesail.world.ports.Ports`), one for the
game and shared by a crewed ship's World, so that she deals with the same ports the
player's ship does: her own pilot, her own boat, her own price lists, the one market.
The constants and the words are `ports.py`'s, read from there; the method text is as it
was in `Ports` (the history is that file's), with the world's half reached through
`self.world.ports`.
"""

from __future__ import annotations

import math
import random
import re
from datetime import datetime, timedelta
from typing import Any

from freesail import units
from freesail.core.events import Severity
from freesail.world import ordnance
from freesail.world.geo import Position, bearing_and_distance, destination, distance_words
from freesail.world.people import Message, Person
from freesail.world.places import Hold, Purse, pounds_words
from freesail.world.ports import (
    _ERRAND_WORDS,
    BOAT_ASHORE_S,
    BOAT_HOIST_IN_S,
    BOAT_HOIST_OUT_S,
    BOAT_PACE_KN,
    IN_PORT_NM,
    LIGHTER_S_PER_TON,
    PILOT_ACTOR,
    PILOT_AGAIN_H,
    PILOT_AT_STATION_M,
    PILOT_BOARDS_UNDER_KN,
    PILOT_BOARDS_WITHIN_M,
    PILOT_COMES_OFF_OVER_KN,
    PILOT_COMMITTED_S,
    PILOT_COMPANY_M,
    PILOT_CONN_AHEAD_M,
    PILOT_CONN_KEEP_OFF_RAD,
    PILOT_CONN_MARK_M,
    PILOT_CONN_ON_THE_LINE_M,
    PILOT_CONN_TURN_RAD,
    PILOT_FIX_EVERY_S,
    PILOT_FIX_SIGMA_NM,
    PILOT_HAIL_AGAIN_S,
    PILOT_HAIL_WITHIN_M,
    PILOT_JOIN_BERTH_NM,
    PILOT_JOIN_OFFING_NM,
    PILOT_JUDGE_WAY_KN,
    PILOT_LEG_INSIDE_M,
    PILOT_LETS_GO_FACTOR,
    PILOT_LIE_MARGIN_RAD,
    PILOT_LIES_TO_S,
    PILOT_OFF_BEYOND_NM,
    PILOT_SAG_LEAST_RAD,
    PILOT_SET_WIND_MARGIN_RAD,
    PILOT_STANDS_OUT_KN,
    PILOT_STREAM_MOST_RAD,
    PILOT_STREAM_WAY_KN,
    PILOT_THICK_AHEAD_S,
    PILOT_THICK_NM,
    PILOT_TRIM_EVERY_S,
    PILOT_TRIM_FIRST_S,
    PILOT_TRIM_POINTS,
    PILOT_TURN_HIGH_LEAST_RAD,
    PILOT_TURN_HIGH_MOST_M,
    PILOT_UNDER_KEEL_M,
    PILOT_WAIT_AHEAD_S,
    PILOT_WAIT_HORIZON_H,
    PILOT_WAIT_LOOK_S,
    PILOT_WAIT_MOST_FATHOMS,
    PILOT_WAIT_REFUSED_S,
    PILOT_WAIT_WEIGH_S,
    PILOT_WAITS_SAY_S,
    PILOT_WARN_ABEAM_M,
    PILOT_WARN_AGAIN_S,
    PILOT_WARN_AHEAD_S,
    PILOT_WARN_MIN_M,
    PILOT_WEIGH_AHEAD_S,
    RECRUIT_RATINGS,
    WATERMAN_FARE_POUNDS,
    WATERMAN_KN,
    WATERMAN_TURN_S,
    BoatState,
    Job,
    Port,
    _and,
    _beyond_the_leg,
    _cap,
    _errand_words,
    _hours_words,
    _off_the_leg,
    _possessive,
    _wind_from_over_the_water,
)

__all__ = ["Dealings"]


class Dealings:
    """**One hull's dealings with the ports** (package 84, step 3; the design's §2.4):
    the pilot's coming and going and his conn, the cutter sent for her, her boat and its
    errands, her price lists, her bargains at the market, the yard's work and the hands
    she enters, her jobs and the port she last lay in. The ports themselves (the files,
    the markets, the stances, the places, who is found ashore) are the world's
    (`freesail.world.ports.Ports`, `world.ports`), read through her under the names the
    one class had (`ports`, `find`, `stance`, `nearest`, `in_port`, ...), so that the
    grammar, the readings and the boat's scripts read `world.dealings` as they read
    `world.ports`. Her World is `world` (a crewed ship's own); her hull `hull_id`."""

    # Package 37h's state, each with a plain class default so that a checkpoint written
    # before it loads (`core.replay`): the answer to the boat's hail ("take", "decline" or
    # none yet), how many times she has hailed and when last, what her hail asked ("shorten
    # sail", "heave to" or nothing), when she last said what she waits for; whether the
    # pilot aboard has asked for his boat, whether he came aboard inward bound, the
    # dangers he has named, when he last warned of shoal water, and whether he has said
    # that he cannot see his marks.
    # Package 45, the same: the pilot's fix and his conn, none in a checkpoint from before
    fix_tick: int | None = None
    fix_said: bool = False
    conn: bool = False
    conn_inward: bool = True
    conn_track: tuple = ()  # reassigned as a list by `give_conn`, never mutated in place
    conn_i: int = 0
    conn_heading: float | None = None
    conn_bearing: float | None = None
    conn_order_tick: int | None = None
    conn_leg_from: Position | None = None  # where the leg in hand begins (package 45c)
    # package 43b: a turning mark taken high for the set on the leg after it, by its index
    conn_aims: dict | None = None
    conn_trim_tick: int = -(10**9)  # when he last had the yards trimmed to his course (45c)
    # package 58b: his wait for the stream or the wind (the hour he looks for, when he last
    # looked, the leg that would not serve, whether she is weighing again), None under way
    # on his track; and the tick he had the yards trimmed for a turn toward the wind before
    # putting the helm over
    conn_wait: dict | None = None
    conn_trim_first: int | None = None
    conn_judged: tuple | None = None  # (the mark's index, the tick) he last judged his legs at
    conn_wait_for: dict | None = None  # the hour he weighed for, his legs judged for it till then
    hail_answer: str = ""
    hail_count: int = 0
    hail_tick: int | None = None
    hail_wants: str = ""
    waits_said_tick: int | None = None
    pilot_boat_asked: bool = False
    pilot_inward: bool = True
    warned: tuple[str, ...] = ()
    shoal_warned_tick: int | None = None
    thick_said: bool = False
    lay_in: str | None = None  # the port she last lay in, until she is out of its ground

    def __init__(self, world: Any) -> None:
        self.world = world
        self.pilot: Person | None = None
        self.pilot_port: str | None = None
        self.pilot_since: int | None = None
        self.cutter_id: str | None = None
        self.cutter_port: str | None = None
        self.cutter_errand: str | None = None  # "bring" or "fetch"
        self.cutter_hailed: bool = False
        self.declined_until: dict[str, int] = {}
        self.price_lists: dict[str, tuple[int, str, list[tuple[str, float]]]] = {}
        self.boat = BoatState()
        self.jobs: list[Job] = []
        self._last_distance_nm: dict[str, float] = {}
        self._counter = 0
        # the pilot's fix and his conn (package 45)
        self.fix_tick: int | None = None
        self.fix_said = False
        self.conn = False
        self.conn_inward = True
        self.conn_track: list[tuple[str, Position]] = []
        self.conn_i = 0
        self.conn_heading: float | None = None
        self.conn_bearing: float | None = None  # the mark's bearing the course was given for
        self.conn_order_tick: int | None = None
        # the price lists the ship starts with (the scenario's `papers: price_lists`)
        papers = getattr(world.scenario, "papers", None) or {}
        for pid in papers.get("price_lists") or []:
            if pid in self.ports:
                self._write_price_list(self.ports[pid], at_start=True)

    @property
    def coarse(self) -> bool:
        """Whether her hull's physics sleep (package 84, step 4; the design's §2.5): a
        station's World kept in the far shape, the far body moving her. Then the boat's
        errand is a job of the port with the boat's time, her anchor the far body's, and the
        pilot's conn not hers (the pilot as a job to the anchorage is step 5's)."""
        return getattr(self.world, "shape", "full") == "far"

    @property
    def anchored(self) -> bool:
        """Whether she is at anchor: her tackle awake; asleep, the far body's anchor leg or
        its state."""
        if self.coarse:
            v = getattr(self.world, "vessel", None)
            plan = getattr(v, "plan", None) or []
            if plan and plan[0][0] == "anchor":
                return True
            return str(getattr(v, "state", "") or "") in ("at anchor", "in port")
        return bool(self.world.at_anchor)

    @property
    def pilot_offered(self) -> bool:
        """Whether the port's pilot comes off for her unasked (package 84, step 3): for a
        ship whose captain can answer his hail, the player's or one a station holds; a
        crewed stranger under her rules captain is not offered one until step 4 gives him
        the port's acts by doctrine (until then his boat would hail twice and bear away, a
        sail on the player's sea for nothing)."""
        world = self.world
        if getattr(world, "parent", None) is None:
            return True
        return any(not h.agent.released for h in (getattr(world, "agents", None) or {}).values())

    # -- the world's ports, read through her (the names a reader of the old `Ports` had) ----

    @property
    def hull_id(self) -> str:
        return str(getattr(getattr(self.world, "own", None), "id", "") or "")

    @property
    def ports(self) -> dict[str, Port]:
        """The port files of the world (`world.ports.ports`)."""
        return self.world.ports.ports

    def find(self, words: str) -> Port | None:
        return self.world.ports.find(words)

    def blockades(self) -> list[dict[str, Any]]:
        return self.world.ports.blockades()

    def watched_by(self, port: Port) -> str | None:
        return self.world.ports.watched_by(port)

    def price_of(self, port: Port, good: str) -> float:
        return self.world.ports.price_of(port, good)

    def places_lines(self, port: Port) -> list[str]:
        return self.world.ports.places_lines(port)

    def news_words(self, port: Port) -> str:
        return self.world.ports.news_words(port)

    def stance(self, port: Port) -> str:
        """The port's stance toward her (`Ports.stance` with her nation)."""
        return self.world.ports.stance(port, self.ship_nation)

    def nearest(self, within_nm: float | None = None) -> tuple[Port, float] | None:
        """The nearest port by its roads to where she is, and the miles to them."""
        return self.world.ports.nearest_to(self.world.position, within_nm)

    def in_port(self) -> Port | None:
        """The port she lies in: at anchor within the port's reach (`Port.reach_nm`,
        `IN_PORT_NM` by default) of its roads or mooring."""
        if not self.anchored:
            return None
        return self.world.ports.in_port_at(self.world.position)

    def to_shore_m(self, port: Port) -> float:
        return self.world.ports.to_shore_from(self.world.position, port)

    # -- the ship against the ports ----------------------------------------------------

    @property
    def ship_nation(self) -> str:
        nation = getattr(self.world.scenario, "nation", None)
        if nation:
            return str(nation)
        spec = getattr(getattr(self.world.ship, "spec", None), "crew", None)
        names = getattr(spec, "names", "english") if spec is not None else "english"
        return self.world.nations.nation_of_names(names)

    # -- the tick ------------------------------------------------------------------------

    def tick(self) -> None:
        """Every tick: the jobs due; once a minute (after the vessels have moved, before
        the lookout looks), the pilot's coming and going."""
        world = self.world
        now = world.clock.tick
        if self.jobs:
            due = [j for j in self.jobs if j.due_tick <= now]
            if due:
                self.jobs = [j for j in self.jobs if j.due_tick > now]
                for job in due:
                    self._apply_job(job)
        if self.jobs and world.clock.ship_time.second == 0:
            # practice and resupply (between packages 72 and 73): a hoy alongside a ship that
            # has weighed goes back at once, and the galley fire is lit as she goes
            # (`ordnance.left_behind`); nothing when no hoy is alongside
            gone = ordnance.left_behind(self)
            if gone:
                self.jobs = [j for j in self.jobs if all(j is not g for g in gone)]
                for job in gone:
                    self._apply_job(job)
        if self.coarse:
            return  # asleep: her jobs alone (the boat's errands by the plan's time; step 4)
        if world.clock.ship_time.second == 0 and self.ports and world.position is not None:
            self._tick_pilot(now)
        if self.boat.away and world.clock.ship_time.second == 0:
            self._boat_kept()

    def _record(
        self, severity: Severity, kind: str, text: str, data: dict[str, Any] | None = None
    ) -> None:
        self.world.record(severity, kind, text, data=data or {})

    # -- the pilot -------------------------------------------------------------------------

    def _cutter(self) -> Any:
        return self.world.vessels.get(self.cutter_id) if self.cutter_id else None

    def _launch_cutter(self, port: Port, errand: str, start: Position | None = None) -> None:
        from freesail.world.ships import Vessel

        self._counter += 1
        common = {
            "id": f"{port.id}-pilot-{port.pilot.craft}-{self._counter}",
            "ship_file": port.pilot.cutter_file,
            "nation": port.nation,
            # from the pilots' station, the outer road, where the cutter cruises for ships
            # (package 36: she sails by her own polar now, and from the shore of Brest she
            # beat out through the Goulet six hours for a ship in the Iroise; the
            # cruising ground is measured from the same road); for a pilot put off at the
            # anchor within, from the quay (package 37h)
            "position": start if start is not None else port.outer_road.position,
            "colours": self.world.nations.get(port.nation).colours,
            "plan": [("to_ship", PILOT_BOARDS_WITHIN_M)],
        }
        if port.pilot.vessel:
            # a boat under oars and sail (35b's gig, the town's boat): `ships.Vessel.boat_of`
            vessel = Vessel.boat_of(port.id, port.pilot.vessel, **common)
        else:
            vessel = Vessel(
                name=f"the {port.name} pilot's cutter",
                kind="a cutter",
                purpose="standing out from the land",
                **common,
            )
        self.world.vessels.add(vessel)
        self.cutter_id = vessel.id
        self.cutter_port = port.id
        self.cutter_errand = errand
        self.cutter_hailed = False
        self._hail_reset()

    def _hail_reset(self) -> None:
        self.hail_answer = ""
        self.hail_count = 0
        self.hail_tick = None
        self.hail_wants = ""
        self.waits_said_tick = None

    def _ground_speed_kn(self) -> float:
        ship = self.world.ship
        dyn = getattr(ship, "dyn", None)
        if dyn is None:
            return units.ms_to_knots(float(getattr(ship, "speed", 0.0)))
        from freesail.physics.integrate import water_velocity

        wx, wy = water_velocity(ship)
        ex, ey = units.heading_vector(dyn.heading)
        return units.ms_to_knots(
            math.hypot(dyn.u * ex + dyn.v * ey + wx, dyn.u * ey - dyn.v * ex + wy)
        )

    def _ground_velocity(self) -> tuple[float, float]:
        """Her way over the ground, metres a second east and north (the truth: the pilot
        knows where his water is taking her)."""
        ship = self.world.ship
        dyn = getattr(ship, "dyn", None)
        if dyn is None:
            speed = float(getattr(ship, "speed", 0.0))
            heading = float(getattr(ship, "heading", 0.0))
            return speed * math.sin(heading), speed * math.cos(heading)
        from freesail.physics.integrate import water_velocity

        wx, wy = water_velocity(ship)
        ex, ey = units.heading_vector(dyn.heading)
        return dyn.u * ex + dyn.v * ey + wx, dyn.u * ey - dyn.v * ex + wy

    def _way_kn(self) -> float:
        """Her way through the water, knots: a ship with none is not under way, whatever
        the stream does with her."""
        ship = self.world.ship
        dyn = getattr(ship, "dyn", None)
        speed = float(dyn.speed) if dyn is not None else float(getattr(ship, "speed", 0.0))
        return units.ms_to_knots(speed)

    def _under_sail(self) -> bool:
        """Standing in under sail: a ship drifting under bare poles has a knot of way
        to leeward and is not making for the port; a ship without sails modelled is
        taken as under way by her way alone."""
        sails = getattr(self.world.ship, "sails", None)
        if not sails:
            return True
        return any(getattr(s, "is_set", False) for s in sails.values())

    def _aground(self) -> bool:
        extra = getattr(self.world.ship, "extra", None)
        return bool(extra.get("aground")) if isinstance(extra, dict) else False

    def _tick_pilot(self, now: int) -> None:
        world = self.world
        cutter = self._cutter()
        if cutter is None and self.cutter_id is not None:
            # she is home: the errand is over
            self.cutter_id = self.cutter_port = self.cutter_errand = None
            self.cutter_hailed = False
            self._hail_reset()
        self._note_lay_in()
        if self.pilot is not None and self.pilot_port in self.ports:
            # aboard, he has her by his marks, warns of the dangers ahead in his own
            # water (package 37h) and conns her when he has the conn (package 45)
            self._fix(self.ports[self.pilot_port], now)
            self._warn(self.ports[self.pilot_port], now)
            if self.conn:
                self._conn(self.ports[self.pilot_port], now)
        if self.pilot is None and cutter is None:
            if not self.pilot_offered:
                return
            found = self.nearest()
            if found is None:
                return
            port, _ = found
            # the cruising ground is measured from the pilot's station, the outer road
            # (package 36: Brest's pilots met ships in the Iroise, seven miles from the
            # road of Bertheaume, not from the Bay within the Goulet)
            _, d_station = bearing_and_distance(world.position, port.outer_road.position)
            if d_station / units.NAUTICAL_MILE > port.pilot.cruising_nm:
                return
            if self.anchored or self._aground():
                return
            if self.declined_until.get(port.id, 0) > now:
                return
            if world.daylight != "day" and not port.pilot.by_night:
                return
            if self.stance(port) == "hostile":
                return
            if self._way_kn() < PILOT_COMES_OFF_OVER_KN or not self._under_sail():
                return
            self._launch_cutter(port, "bring")
            return
        if cutter is not None and self.cutter_errand in ("bring", "fetch"):
            port = self.ports[self.cutter_port or ""]
            _, dist = bearing_and_distance(world.position, cutter.position)
            if not self.cutter_hailed and dist <= PILOT_HAIL_WITHIN_M:
                self._hail(port, cutter, now)
            if not self.cutter_hailed:
                # a ship that outsails the boat before she can hail her is let go when she
                # is beyond twice the cruising ground from the station (package 45: the
                # Falmouth cutter chased the schooner a hundred miles to Ushant and hailed
                # her there); the boat goes home, and no six hours are held against her
                _, d_station = bearing_and_distance(world.position, port.outer_road.position)
                if d_station > PILOT_LETS_GO_FACTOR * port.pilot.cruising_nm * units.NAUTICAL_MILE:
                    cutter.plan = [("home", port.outer_road.position)]
                    cutter.alongside = False
                    self.cutter_errand = None
                    self._hail_reset()
                    self._record(
                        Severity.ROUTINE,
                        "port.pilot_gone",
                        f"The {port.name} {port.pilot.craft}, left astern, bore away for "
                        f"{port.outer_road.name}.",
                        {"port": port.id, "unanswered": False, "left_astern": True},
                    )
                return
            if self.cutter_errand == "fetch" or self.hail_answer == "take":
                # he boards (or leaves) a ship under six knots within two cables, as
                # package 35 had it; a faster ship has the boat in company until she is
                # slow enough, and the boat says what she waits for; taken and still too
                # fast at the interval, she hails once more, for her to heave to
                if (
                    self.cutter_errand == "bring"
                    and self.hail_count < 2
                    and self.hail_tick is not None
                    and now - self.hail_tick >= PILOT_HAIL_AGAIN_S
                    and self._ground_speed_kn() > PILOT_BOARDS_UNDER_KN
                ):
                    self._hail(port, cutter, now, again=True)
                    return
                if dist <= PILOT_BOARDS_WITHIN_M:
                    if self._ground_speed_kn() <= PILOT_BOARDS_UNDER_KN:
                        cutter.alongside = True
                        if self.cutter_errand == "bring":
                            self._pilot_boards(port, cutter, now)
                        else:
                            self._pilot_leaves(port, cutter, now)
                    else:
                        self._waits(port, now)
                return
            # unanswered (package 37h; the owner's ruling of 7 October 2026): the boat
            # keeps company, hails once more, and bears away for her station
            if self.hail_tick is not None and now - self.hail_tick >= PILOT_HAIL_AGAIN_S:
                if self.hail_count < 2:
                    self._hail(port, cutter, now, again=True)
                else:
                    self._bear_away(port, cutter, now, unanswered=True)
            return
        if self.pilot is not None and (cutter is None or self.cutter_errand is None):
            port = self.ports[self.pilot_port or ""]
            if self.anchored:
                self._put_off_at_anchor(port, now)
                return
            if self.pilot_boat_asked:
                return  # he has asked for his boat once (package 37h)
            # the cutter comes off for him again while the one that brought him is still
            # going home (package 36: a frigate under topsails was past the cruising
            # ground before the first was in, and the pilot stayed aboard)
            _, d_road = bearing_and_distance(world.position, port.outer_road.position)
            _, d_anch = bearing_and_distance(world.position, port.anchorage.position)
            d_nm = d_anch / units.NAUTICAL_MILE
            last = self._last_distance_nm.get(port.id)
            self._last_distance_nm[port.id] = d_nm
            road_nm = bearing_and_distance(port.anchorage.position, port.outer_road.position)[1]
            beyond = d_nm > road_nm / units.NAUTICAL_MILE + PILOT_OFF_BEYOND_NM
            # an inward pilot is put off at the anchor; outward only if she stands out to
            # sea again under way, not as she drifts hove to for him (package 37h: the 5b
            # schooner, hove to off the outer road, opened her distance and he asked for
            # his boat)
            standing_out = not self.pilot_inward or self._way_kn() >= PILOT_STANDS_OUT_KN
            if (
                beyond
                and standing_out
                and last is not None
                and d_nm > last
                and d_road / units.NAUTICAL_MILE < port.pilot.cruising_nm
            ):
                self._launch_cutter(port, "fetch")
                self.pilot_boat_asked = True
                # the pilot asks for sail to be shortened as his boat comes off (package
                # 36: a schooner with her sheets tended outran the cutter and carried the
                # Falmouth pilot to the Iroise); the same line as the boat's hail, so
                # that a book which shortens sail at the pilot's hail does so now; notable,
                # as the boat's own hail is (package 37d)
                self._record(
                    Severity.NOTABLE,
                    "port.pilot_hail",
                    f"The pilot asks for sail to be shortened: his {port.pilot.craft} is "
                    f"coming off for him.",
                    {"port": port.id, "asks": True, "errand": "fetch"},
                )

    def _note_lay_in(self) -> None:
        """The port she lies in at anchor, kept until she is beyond its pilot's ground:
        a pilot who boards her before then takes her out (package 37h)."""
        if self.anchored:
            port = self.in_port()
            spot = port.nearest_spot(self.world.position)[0] if port is not None else None
            if port is not None and spot is not port.outer_road:
                # within, in the anchorage or the mooring: the outer road is where a ship
                # from sea waits for her pilot and her tide to go in
                self.lay_in = port.id
            return
        port = self.ports.get(self.lay_in or "")
        if port is None:
            return
        _, d = bearing_and_distance(self.world.position, port.outer_road.position)
        if d / units.NAUTICAL_MILE > port.pilot.cruising_nm:
            self.lay_in = None

    # -- the hail and its answer (package 37h) ---------------------------------------------

    def _hail(self, port: Port, cutter: Any, now: int, again: bool = False) -> None:
        """The boat's hail within four cables: for the pilot she brings, asking her to
        shorten sail when she is too fast for him to board and to heave to at the second
        hail, never either at anchor; or, come off for the pilot aboard, saying so. From
        the hail the boat keeps company with her (`ships.Vessel`'s `company` leg)."""
        craft = port.pilot.craft
        if self.cutter_errand == "bring" and self.stance(port) == "closed":
            # a port closed to her nation: the pilot hails his refusal from the boat
            # (truth 70), with nothing to answer
            self.cutter_hailed = True
            self._pilot_boards(port, cutter, now)
            return
        self.cutter_hailed = True
        cutter.plan = [("company", PILOT_COMPANY_M)]
        if self.cutter_errand == "fetch":
            self._record(
                Severity.NOTABLE,
                "port.pilot_hail",
                f"The {craft} hailed: she has come off for the pilot.",
                {"port": port.id, "errand": "fetch"},
            )
            return
        wants = ""
        if not self.anchored and self._ground_speed_kn() > PILOT_BOARDS_UNDER_KN:
            wants = "heave to" if again else "shorten sail"
        self.hail_count += 1
        self.hail_tick = now
        self.hail_wants = wants
        ask = f"; {wants} and he will come aboard" if wants else ", if you will take him"
        if again and self.hail_answer == "take":
            text = (
                f"The {craft} hailed again: she cannot put the pilot aboard at "
                f"{self._ground_speed_kn():.0f} knots; heave to and he will come aboard."
            )
        elif again:
            text = (
                f"The {craft} hailed again: a pilot for {port.name}{ask}. Unanswered, she "
                f"will bear away for {port.outer_road.name}."
            )
        else:
            text = f"The {craft} hailed: a pilot for {port.name}{ask}."
        # notable (package 37d; the review of gate 5c's playtests, 8.2 item 13): a hail
        # from a boat alongside is a thing the deck must answer
        self._record(
            Severity.NOTABLE,
            "port.pilot_hail",
            text,
            {"port": port.id, "errand": "bring", "wants": wants, "again": again},
        )

    def _waits(self, port: Port, now: int) -> None:
        """The boat in company with a ship too fast for him: what she waits for, at most
        once in `PILOT_WAITS_SAY_S` (the review of gate 5c, G10, game 9 at Brest)."""
        if self.waits_said_tick is not None and now - self.waits_said_tick < PILOT_WAITS_SAY_S:
            return
        self.waits_said_tick = now
        craft = port.pilot.craft
        knots = self._ground_speed_kn()
        doing = "put the pilot aboard" if self.cutter_errand == "bring" else "take the pilot off"
        self._record(
            Severity.NOTABLE,
            "port.pilot_waits",
            f"The {craft} keeps company: she cannot {doing} at {knots:.0f} knots, and waits "
            f"for her to shorten sail or heave to.",
            {"port": port.id, "errand": self.cutter_errand},
        )

    def _bear_away(self, port: Port, cutter: Any, now: int, unanswered: bool) -> str:
        """The boat sent back to her station: her hail unanswered (the line said here),
        or the pilot declined (the words returned, for the order's own line)."""
        craft = port.pilot.craft
        words = (
            f"the {craft} bore away for {port.outer_road.name}; no pilot will come off "
            f"from {port.name} for six hours"
        )
        if unanswered:
            self._record(
                Severity.NOTABLE,
                "port.pilot_gone",
                f"The {craft} bore away for {port.outer_road.name}, her hail unanswered; no "
                f"pilot will come off from {port.name} for six hours.",
                {"port": port.id, "unanswered": True},
            )
        cutter.plan = [("home", port.outer_road.position)]
        cutter.alongside = False
        self.cutter_errand = None
        self.declined_until[port.id] = now + int(PILOT_AGAIN_H * 3600)
        self._hail_reset()
        return words

    def _boat_in_sight(self, cutter: Any) -> bool:
        lookout = getattr(self.world, "lookout", None)
        sightings = getattr(lookout, "sightings", None) or []
        if any(s.feature.id == f"sail:{cutter.id}" for s in sightings):
            return True
        _, dist = bearing_and_distance(self.world.position, cutter.position)
        return dist <= PILOT_HAIL_WITHIN_M

    def answer_pilot(self, verb: str) -> tuple[str, dict[str, Any], str]:
        """`take the pilot`, `decline the pilot`, `hail the pilot` (package 37h): the
        answer to the boat's hail, or the ship's own hail to a boat in sight. Returns the
        line, its data, and the manoeuvre the hail asked that the order is to carry out
        ("shorten sail", "heave to" or nothing, when she is still too fast for him);
        refused in words when there is no boat to answer."""
        from freesail.orders.errors import OrderError

        world = self.world
        if self.pilot is not None:
            port = self.ports.get(self.pilot_port or "")
            where = f" of {port.name}" if port is not None else ""
            raise OrderError(
                f"The pilot, {self.pilot.name}{where}, is aboard already; he is put off at "
                "the anchor, or outward a mile beyond the outer road."
            )
        cutter = self._cutter()
        if cutter is None or self.cutter_errand != "bring":
            why = "no pilot's boat is in sight"
            found = self.nearest()
            if found is not None:
                port, _ = found
                until = self.declined_until.get(port.id, 0)
                if until > world.clock.tick:
                    when = world.clock.ship_time + timedelta(seconds=until - world.clock.tick)
                    why += (
                        f"; the {port.name} {port.pilot.craft} bore away, and none comes off "
                        f"before {units.time_stamp(when)}"
                    )
            raise OrderError(
                f"There is no pilot to {verb.split()[0]}: {why}. A pilot comes off by day "
                "to a ship under way in his port's ground, and hails her."
            )
        port = self.ports[self.cutter_port or ""]
        craft = port.pilot.craft
        if verb == "hail the pilot" and not self._boat_in_sight(cutter):
            raise OrderError(
                f"The {port.name} {craft} is not in sight yet to hail; she is standing out "
                "toward her, and hails when she is within four cables."
            )
        if verb == "decline the pilot":
            gone = self._bear_away(port, cutter, world.clock.tick, unanswered=False)
            text = f"Waved off the pilot: we need no pilot for {port.name}; {gone}."
            return text, {"port": port.id, "answer": "decline"}, ""
        self.hail_answer = "take"
        if not self.cutter_hailed:
            # the ship hails first, or answers before the boat's hail: she closes now
            self.cutter_hailed = True
            self.hail_count = max(1, self.hail_count)
            self.hail_tick = world.clock.tick
        cutter.plan = [("company", PILOT_COMPANY_M)]
        wants = ""
        if not self.anchored and self._ground_speed_kn() > PILOT_BOARDS_UNDER_KN:
            wants = self.hail_wants or "shorten sail"
        already = wants and self._in_hand(wants)
        head = (
            f"Hailed the {craft}: we will take the pilot for {port.name}"
            if verb == "hail the pilot"
            else f"Answered the {craft}: we will take the pilot for {port.name}"
        )
        if already:
            # the captain has the sail coming in, or her hove to, already: not twice
            doing = "the sail is coming in" if wants == "shorten sail" else "she is heaving to"
            text = head + f"; {doing} already, as she asks."
            return text, {"port": port.id, "answer": "take", "wants": wants}, ""
        text = head + (f"; {wants}, as she asks." if wants else ".")
        return text, {"port": port.id, "answer": "take", "wants": wants}, wants

    def _in_hand(self, wants: str) -> bool:
        """Whether what the hail asks is in hand already: sail being taken in, reefed or
        furled for "shorten sail", the heave-to for "heave to" (the book or the captain
        gave it before the answer)."""
        extra = getattr(self.world.ship, "extra", None) or {}
        runner = extra.get("evolutions") if isinstance(extra, dict) else None
        work = runner.work() if runner is not None and hasattr(runner, "work") else []
        ids = [str(getattr(getattr(i, "evo", None), "id", "")) for i in work]
        if wants == "heave to":
            return "heave_to" in ids
        return any(i.startswith(("take_in", "reef", "furl")) for i in ids)

    def waiting_words(self) -> str | None:
        """What the pilot's boat is doing, for the readings when no pilot is aboard."""
        cutter = self._cutter()
        if cutter is None or self.cutter_errand != "bring":
            return None
        port = self.ports.get(self.cutter_port or "")
        if port is None:
            return None
        craft = f"the {port.name} {port.pilot.craft}"
        if not self.cutter_hailed:
            return f"no pilot aboard; {craft} is standing out toward her"
        if self.hail_answer == "take":
            return f"no pilot aboard; {craft} keeps company to put him aboard"
        return (
            f"no pilot aboard; {craft} has hailed and waits for an answer ('take the "
            "pilot' or 'decline the pilot')"
        )

    # -- aboard, and leaving ---------------------------------------------------------------

    def _pilot_boards(self, port: Port, cutter: Any, now: int) -> None:
        world = self.world
        stance = self.stance(port)
        nation = world.nations.get(self.ship_nation)
        if stance == "closed":
            craft = port.pilot.craft
            by = port.blockaded_by
            if by is not None and world.nations.at_war(by, self.ship_nation):
                # package 39d: closed by the blockade, not by the port's order
                watchers = world.nations.get(by)
                text = (
                    f"The pilot hailed from the {craft}: {port.name} is blockaded by the "
                    f"{watchers.adjective} squadron; no pilot will take {nation.people} in "
                    f"past their ships. The {craft} bore up for the land."
                )
            else:
                text = (
                    f"The pilot hailed from the {craft}: {port.name} is closed to "
                    f"{nation.people} by the port's order; you will get no pilot here, and "
                    f"the batteries will not let you pass. The {craft} bore up for the land."
                )
            self._record(
                Severity.NOTABLE,
                "port.pilot_refused",
                text,
                {"port": port.id, "stance": stance, "nation": self.ship_nation},
            )
            cutter.plan = [("home", port.shore.position)]
            cutter.alongside = False
            self.cutter_errand = None
            self.declined_until[port.id] = now + int(PILOT_AGAIN_H * 3600)
            self._hail_reset()
            return
        stream = world.rng.stream("people")
        surname = stream.choice(list(port.pilot.names))
        self._counter += 1
        pilot = Person(
            f"pilot-{port.id}-{self._counter}",
            f"Mr {surname}",
            "pilot",
            port.pilot.skill,
            place="quarterdeck",
            port=port.id,
        )
        world.people.add(pilot)
        self.pilot = pilot
        self.pilot_port = port.id
        self.pilot_since = now
        self.pilot_boat_asked = False
        self.warned = ()
        self.shoal_warned_tick = None
        self.thick_said = False
        self._last_distance_nm.pop(port.id, None)
        # outward bound from the port she last lay in, else inward (package 37h: he
        # pilots her and does not con her; "took charge of her" was the one phrase
        # package 35 gave him, and he took charge of nothing)
        self.pilot_inward = self.lay_in != port.id
        head = (
            f"The pilot, {pilot.name} of {port.name}, came aboard from the {port.pilot.craft} "
            f"to pilot her {'in' if self.pilot_inward else 'out'}"
        )
        if stance == "neutral":
            head += f" ({nation.adjective} colours being no bar at {port.name})"
        self._record(
            Severity.NOTABLE,
            "port.pilot_aboard",
            head + ".",
            {
                "port": port.id,
                "pilot": pilot.to_dict(),
                "stance": stance,
                "inward": self.pilot_inward,
            },
        )
        self._record(
            Severity.NOTABLE,
            "port.pilot_words",
            f"The pilot says: {self.pilot_words(port)}",
            {"port": port.id, "words": self.pilot_words(port)},
        )
        news = self.news_words(port)
        if news:
            self._record(
                Severity.ROUTINE, "port.news", f"The pilot's news: {news}", {"port": port.id}
            )
            # what his news changed of the war the ship knows is entered in her papers, as
            # a price is (the owner's fifth note)
            papers = getattr(world, "papers", None)
            if papers is not None:
                for line in papers.news_heard(f"the pilot off {port.name}"):
                    self._record(
                        Severity.NOTABLE, "paper.written", line, {"paper": "the news of the war"}
                    )
        for letter in list(port.letters):
            letter.carried_by = f"the pilot {port.pilot.craft}"
            for severity, kind, text, data in world.people.message_aboard(letter):
                self._record(severity, kind, text, data)
            port.letters.remove(letter)
        cutter.plan = [("lie_to", PILOT_LIES_TO_S), ("home", port.shore.position)]
        cutter.alongside = False
        self.cutter_errand = None
        self._hail_reset()

    def _put_off_at_anchor(self, port: Port, now: int) -> None:
        """At anchor in his port's anchorage or mooring, brought up, his charge is done:
        he asks for his boat once, and it comes off for him from the quay (package 37h;
        the Brest pilot of the review's game 1 never left and was never paid). Anchored
        in the outer road he stays: she waits there for the tide or the wind to go in."""
        if self.pilot_boat_asked or self._ground_speed_kn() > 0.5:
            return
        if self.conn and self.conn_wait is not None:
            return  # brought up by him to wait for the stream (package 58b): not his berth
        pos = self.world.position
        spot, d_nm = port.nearest_spot(pos)
        if spot is port.outer_road or d_nm > IN_PORT_NM:
            return
        self.pilot_boat_asked = True
        self._record(
            Severity.NOTABLE,
            "port.pilot_boat",
            f"The pilot asks for his {port.pilot.craft}: she is brought up in {spot.name}, "
            f"and his charge is done.",
            {"port": port.id, "spot": spot.name},
        )
        self._launch_cutter(port, "fetch", start=port.shore.position)

    def _pilot_leaves(self, port: Port, cutter: Any, now: int) -> None:
        world = self.world
        pilot = self.pilot
        if self.conn:
            self._conn_off("he is put off", said=False)
        self.fix_said = False
        self.fix_tick = None
        assert pilot is not None
        fee = port.pilot.fee_pounds
        paid = ""
        purse = getattr(world, "purse", None)
        if purse is not None and fee > 0:
            try:
                purse.pay(fee, f"pilotage, {port.name}", now)
                paid = f"; the pilotage, {pounds_words(fee)}, paid and his certificate signed"
            except ValueError:
                paid = (
                    f"; his certificate signed for {pounds_words(fee)} of pilotage, the purse "
                    f"being empty"
                )
        world.people.remove(pilot)
        if self.anchored:
            spot, _ = port.nearest_spot(world.position)
            where = f"at the anchor in {spot.name}"
        else:
            where = f"clear of {port.outer_road.name}"
        self._record(
            Severity.NOTABLE,
            "port.pilot_left",
            f"{pilot.name} left her in the {port.pilot.craft}, {where}{paid}.",
            {"port": port.id, "pilot": pilot.to_dict(), "fee_pounds": fee},
        )
        self.pilot = None
        self.pilot_port = None
        self.pilot_since = None
        self.pilot_boat_asked = False
        self.warned = ()
        self.declined_until[port.id] = now + int(PILOT_AGAIN_H * 3600)
        cutter.plan = [("home", port.shore.position)]
        cutter.alongside = False
        self.cutter_errand = None
        self._hail_reset()

    # -- his warnings (package 37h) ----------------------------------------------------------

    def _warn(self, port: Port, now: int) -> None:
        """The pilot aboard, under way within his port's ground: a charted danger ahead
        on her true track with too little water over it, by name and once, or the water
        shoaling ahead to less than a fathom under her keel, at most once in ten minutes;
        each an urgent line saying on which hand the deeper water lies. In thick weather
        he says once that he cannot see his marks, and warns by the lead and the time run
        (nearer, and without the bearing). From the true chart and the tide's height now
        (he knows his water); never put into a reading."""
        from freesail.world.chart import fathoms_words

        world = self.world
        chart = getattr(world, "chart", None)
        pos = world.position
        if chart is None or pos is None or self.anchored:
            return
        _, d_nm = port.nearest_spot(pos)
        if d_nm > port.pilot.cruising_nm:
            return
        conditions = getattr(world, "conditions", None)
        visibility = getattr(conditions, "visibility_nm", None) if conditions else None
        thick = visibility is not None and float(visibility) < PILOT_THICK_NM
        if thick and not self.thick_said:
            self.thick_said = True
            self._record(
                Severity.NOTABLE,
                "port.pilot_thick",
                "The pilot cannot see his marks in this weather; he will warn by the lead "
                "and the time run, and asks for the lead kept going and the anchor ready.",
                {"port": port.id},
            )
        elif not thick:
            self.thick_said = False
        east, north = self._ground_velocity()
        speed = math.hypot(east, north)
        if speed < units.knots_to_ms(0.5):
            return
        track = math.degrees(math.atan2(east, north)) % 360.0
        ahead = max(
            PILOT_WARN_MIN_M, speed * (PILOT_THICK_AHEAD_S if thick else PILOT_WARN_AHEAD_S)
        )
        tide = float(getattr(world, "tide_height_m", 0.0) or 0.0)
        hull = getattr(world.ship, "hull", None)
        draught = float(hull.spec.draught_m) if hull is not None else 0.0
        wants = draught + PILOT_UNDER_KEEL_M
        lead = "The pilot, by the lead and the time run" if thick else "The pilot warns"
        # the hands as a pilot names them, from the ship's head (package 45c: they were
        # the track's, the course over the ground, which the stream sets her along)
        dyn = getattr(world.ship, "dyn", None)
        head = float(dyn.heading) if dyn is not None else math.radians(track)

        def hand_of(bearing_deg: float) -> str:
            rel = units.wrap_pi(math.radians(bearing_deg) - head)
            return "starboard" if rel >= 0.0 else "larboard"

        for f, along, _off, _side in chart.dangers_ahead(
            pos, track, ahead, PILOT_WARN_ABEAM_M, tide, wants
        ):
            if f.id in self.warned:
                continue
            self.warned = (*self.warned, f.id)
            danger_hand = hand_of(bearing_and_distance(pos, f.position)[0])
            deeper = "larboard" if danger_hand == "starboard" else "starboard"
            where = f"{distance_words(max(along, units.CABLE))} ahead"
            text = f"{lead}: {f.name} {where}; the deeper water is to {deeper}."
            if not thick:
                # the hand and the mark as a pilot would say them (package 45, item 2b):
                # the danger's bearing relative to her head, the hand to leave it on,
                # and plainly when it lies on the hand he names as the deeper one
                from freesail.world.lookout import relative_words

                dyn = getattr(world.ship, "dyn", None)
                heading = float(dyn.heading) if dyn is not None else math.radians(track)
                brg, _ = bearing_and_distance(pos, f.position)
                rel = units.wrap_pi(math.radians(brg) - heading)
                where += ", " + relative_words(rel)
                leave = "starboard" if deeper == "larboard" else "larboard"
                plural = f.name.lower().endswith("s") and not f.name.lower().endswith("ss")
                them = "them" if plural else "it"
                lies = "lie" if plural else "lies"
                if (rel > 0) == (deeper == "starboard") and abs(rel) < math.pi / 2:
                    # on the bow he would haul to: keep her off till it is passed
                    bow = "starboard" if rel > 0 else "larboard"
                    text = (
                        f"{lead}: keep her off, {f.name} {lies} under the {bow} bow, "
                        f"{distance_words(max(along, units.CABLE))} ahead; leave {them} to "
                        f"{leave}, and do not haul to {deeper} till {them if plural else 'it'} "
                        f"{'are' if plural else 'is'} abaft the beam."
                    )
                else:
                    text = (
                        f"{lead}: {f.name} {where}; leave {them} to {leave}, the deeper water "
                        f"is to {deeper}."
                    )
            self._record(
                Severity.URGENT,
                "port.pilot_warns",
                text,
                {"port": port.id, "danger": f.id, "deeper": deeper, "thick": thick},
            )
            return
        if self.shoal_warned_tick is not None and now - self.shoal_warned_tick < PILOT_WARN_AGAIN_S:
            return
        shoal = chart.shoal_ahead(pos, track, ahead, wants, tide)
        if shoal is None:
            return
        along, depth, side = shoal
        self.shoal_warned_tick = now
        water = depth + tide
        what = "the shore" if water <= 0.0 else f"shoal water, {fathoms_words(water)},"
        deeper = hand_of(track + 90.0 * side) if side else None
        hand = f"the deeper water is to {deeper}" if deeper else "the deeper water is astern"
        self._record(
            Severity.URGENT,
            "port.pilot_warns",
            f"{lead}: {what} {distance_words(along)} ahead; {hand}.",
            {"port": port.id, "danger": "", "deeper": deeper or "astern", "thick": thick},
        )

    # -- the pilot's fix and his conn (package 45) --------------------------------------------

    def _fix(self, port: Port, now: int) -> None:
        """Aboard and in sight of his marks within his port's ground, the pilot has her by
        them: the account brought to the truth with a cable's doubt every five minutes,
        said once as his fix and not again until he leaves or the weather thickens; by
        the lead and the time run in thick weather, no fix (`_warn`)."""
        from freesail.world.geo import format_position

        world = self.world
        nav = getattr(world, "navigation", None)
        pos = world.position
        if nav is None or pos is None or self.anchored or self._aground():
            return
        _, d_nm = port.nearest_spot(pos)
        if d_nm > port.pilot.cruising_nm:
            return
        conditions = getattr(world, "conditions", None)
        visibility = getattr(conditions, "visibility_nm", None) if conditions else None
        if visibility is not None and float(visibility) < PILOT_THICK_NM:
            self.fix_said = False  # said again when his marks come back
            return
        if self.fix_tick is not None and now - self.fix_tick < PILOT_FIX_EVERY_S:
            return
        self.fix_tick = now
        nav.bring_up()
        nav.reckoning.set_position(
            pos, now, sigma_nm=PILOT_FIX_SIGMA_NM, what="the pilot's fix by his marks"
        )
        if not self.fix_said:
            self.fix_said = True
            self._record(
                Severity.NOTABLE,
                "port.pilot_fix",
                f"The pilot has her by his marks: {format_position(pos)}; the account is "
                "brought to it, and he keeps it there while his marks are in sight.",
                {"port": port.id, "lat_deg": pos.lat_deg, "lon_deg": pos.lon_deg},
            )

    def _track_marks(self, port: Port, which: str) -> list[tuple[str, Position]]:
        from freesail.world.captains import _mark

        out: list[tuple[str, Position]] = []
        for words in port.tracks.get(which) or []:
            m = _mark(self.world, str(words))
            if m is not None:
                out.append(m)
        return out

    def give_conn(self, inward: bool) -> str:
        """`let the pilot take her in` / `... out` (package 45, item 2c): the pilot conns
        her along his port's track from where she is, inward to the anchorage, outward
        to the outer road and the sea; refused in words with no pilot aboard."""
        from freesail.orders.errors import OrderError

        world = self.world
        if self.pilot is None or self.pilot_port not in self.ports:
            raise OrderError(
                "No pilot is aboard to take her; a pilot comes off by day to a ship under way "
                "in his port's ground, and hails her."
            )
        port = self.ports[self.pilot_port]
        pos = world.position
        if inward:
            joined = self._joined_track(port, pos)
            if isinstance(joined, str):
                raise OrderError(joined)
            self.conn_track = joined
        else:
            marks = self._track_marks(port, "to_sea")
            if not marks:
                marks = [(port.outer_road.name, port.outer_road.position)]
            # the marks already astern of her are not conned for: a mark farther from the
            # track's end than she is herself has been passed
            goal = marks[-1][1]
            here = bearing_and_distance(pos, goal)[1] if pos is not None else math.inf
            keep = [m for m in marks[:-1] if bearing_and_distance(m[1], goal)[1] < here]
            self.conn_track = [*keep, marks[-1]]
        self.conn_i = 0
        self.conn_aims = {}
        self.conn_inward = inward
        self.conn_heading = None
        self.conn_bearing = None
        self.conn_leg_from = pos
        self.conn_wait = None
        self.conn_judged = None
        self.conn_trim_first = None
        self.conn_wait_for = None
        self.conn = True
        way = "in" if inward else "out"
        words = (
            f"The pilot, {self.pilot.name}, has the conn to take her {way}: by "
            f"{len(self.conn_track)} mark{'s' if len(self.conn_track) != 1 else ''} to "
            f"{self.conn_track[-1][0]}; 'I have the conn', or a helm order, takes her back."
        )
        self._conn(port, world.clock.tick)
        return words

    def inward_track(self, port: Port) -> list[tuple[str, Position]]:
        """The pilot's track inward (package 45c): his station, the port's `in` marks and
        the anchorage, each as (words, position); the station left out where it is the
        anchorage itself (Rochefort's road of Aix)."""
        from freesail.world.captains import _mark

        track: list[tuple[str, Position]] = []
        station = _mark(self.world, port.pilot.station) if port.pilot.station else None
        if station is None:
            station = (port.outer_road.name, port.outer_road.position)
        track.append(station)
        for m in self._track_marks(port, "in"):
            if bearing_and_distance(track[-1][1], m[1])[1] > units.CABLE:
                track.append(m)
        end = port.anchorage
        if bearing_and_distance(track[-1][1], end.position)[1] > units.CABLE:
            track.append((end.name, end.position))
        return track

    def _joined_track(self, port: Port, pos: Position | None) -> list[tuple[str, Position]] | str:
        """The marks the pilot cons her by inward (package 45c): from the station along his
        track when she is at it; from the end of the nearest leg she is already inside of;
        else by a clear line to the first mark of his track ahead of her (the station or
        one beyond it), and on from there; else by a joining leg round the land to the station, laid
        with the captain's planner; or the words of his refusal when no clear joining leg
        is to be had."""
        from freesail.world.captains import Planner

        track = self.inward_track(port)
        if pos is None:
            return track[1:] or track
        station_words, station = track[0]
        if bearing_and_distance(pos, station)[1] <= PILOT_AT_STATION_M:
            return track[1:] or track
        inside: list[tuple[float, int]] = []
        for i in range(len(track) - 1):
            off, share = _off_the_leg(track[i][1], track[i + 1][1], pos)
            if 0.0 <= share <= 1.0 and off <= PILOT_LEG_INSIDE_M:
                inside.append((off, i))
        if inside:
            _, i = min(inside)
            return track[i + 1 :]
        planner = Planner(self.world)
        offing, berth = PILOT_JOIN_OFFING_NM, PILOT_JOIN_BERTH_NM
        # at the first mark of his track ahead of her that a clear line reaches (package
        # 45c): ahead by the leg she lies nearest, its end when she is abreast of it or
        # beyond its start, its start when she is short of it; she is conned there and on
        # along the track, and not back to the station to windward of her (the owner's
        # merchantman south of the Goulet's track, sent back NNE for Bertheaume, stood on
        # close-hauled onto the north shore; from the Goulet's mouth, taken aback and set
        # onto the Fillettes). A first version took the shortest clear way by the track,
        # which joined it at its fifth mark by a line between the Mingan and the Fillettes.
        first = 0
        if len(track) > 1:
            legs = [_off_the_leg(track[k][1], track[k + 1][1], pos) for k in range(len(track) - 1)]

            def _off(k: int) -> float:
                off, share = legs[k]
                if 0.0 <= share <= 1.0:
                    return off
                end = track[k][1] if share < 0.0 else track[k + 1][1]
                return bearing_and_distance(pos, end)[1]

            k = min(range(len(legs)), key=_off)
            first = k + 1 if legs[k][1] > 0.0 else k
        for k in range(first, len(track)):
            skip_end = PILOT_AT_STATION_M if k == 0 else units.CABLE
            if planner.clear(pos, track[k][1], offing, berth, skip_end):
                return track[k:]
        joining: list[tuple[str, Position]] = []
        skip = PILOT_AT_STATION_M  # the station's own water, his ground
        if not planner.clear(pos, station, offing, berth, skip):
            joining = planner._round_headland(pos, station, offing, berth, skip)
            legs = [pos, *(m[1] for m in joining), station]
            if not joining or not all(
                planner.clear(a, b, offing, berth, skip if b is station else units.CABLE)
                for a, b in zip(legs, legs[1:], strict=False)
            ):
                name = self.pilot.name if self.pilot is not None else "The pilot"
                return (
                    f"{name}: bring her to the station first, {station_words}, and I will take "
                    "her in; from here I know no clear way to my track."
                )
        return [*joining, *track]

    def take_conn_back(self, why: str = "") -> str:
        """`I have the conn`: the officer takes her back from the pilot, who stands by and
        still warns of his water."""
        from freesail.orders.errors import OrderError

        if not self.conn:
            raise OrderError("The pilot has not the conn; she is yours already.")
        self._conn_off(why or "the conn taken back")
        name = self.pilot.name if self.pilot is not None else "the pilot"
        return f"I have the conn; {name} stands by and will still warn of his water."

    def _conn_off(self, why: str, said: bool = True) -> None:
        self.conn = False
        self.conn_leg_from = None
        self.conn_heading = None
        self.conn_bearing = None
        self.conn_order_tick = None
        self.conn_track = []
        self.conn_i = 0
        self.conn_wait = None
        self.conn_judged = None
        self.conn_trim_first = None
        self.conn_wait_for = None
        if said and self.pilot is not None:
            self._record(
                Severity.NOTABLE,
                "port.pilot_conn",
                f"The pilot gives her up: {why}.",
                {"port": self.pilot_port, "conn": False, "why": why},
            )

    def _conn(self, port: Port, now: int) -> None:
        """Once a tick while the pilot has the conn: a helm order of the officer's takes
        her back; a mark passed within two cables (or abeam) is left for the next; the
        course for the mark in hand is given when it is first wanted or has drawn half
        a point; at the last mark he says where to let go and his conn is done."""
        from freesail.ship.parts import HelmMode

        world = self.world
        ship = world.ship
        dyn = getattr(ship, "dyn", None)
        pos = world.position
        if dyn is None or pos is None:
            return
        # a helm order of anyone but the pilot since his last takes her back (the helm's
        # own "kept her away" moves the target too, so the log's orders are read and not
        # the target): "I have the conn" by its own order, a course or a manoeuvre by its
        log = getattr(world, "log", None)
        if log is not None and self.conn_order_tick is not None:
            for e in log.since(self.conn_order_tick):
                if e.tick <= self.conn_order_tick and e.kind != "helm.set":
                    continue
                if e.actor == PILOT_ACTOR:
                    continue
                # a course of the player's own book, standing from before he was given her
                # (the merchant passage's five-minute course for the road took her back
                # from him ninety seconds after the book itself gave him the conn, and she
                # grounded in the Goulet with nobody conning): the pilot has the conn, and
                # gives his course again at once; the officer's own hand takes her back
                book = str(e.actor).startswith("standing order '")
                if e.kind == "helm.set":
                    if book:
                        self.conn_bearing = None
                        continue
                    self._conn_off("you have her, sir (the helm was given another course)")
                    return
                if e.kind == "order.accepted":
                    order = str((e.data or {}).get("order") or "")
                    if order.split(" ")[:1] in (["tack"], ["wear"], ["heave"], ["steer"]) or (
                        order.startswith(("keep her", "shape a course", "put her about"))
                    ):
                        if book:
                            self.conn_bearing = None
                            continue
                        self._conn_off("you have her, sir (the helm was given another course)")
                        return
        if self.conn_wait is not None:
            # waiting for the stream or the wind (package 58b, item 6): at anchor he looks at
            # the water every few minutes and weighs when his legs serve; coming to her
            # anchor, or weighing until she has way, he gives no course
            if self.anchored:
                self._wait_at_anchor(port, now)
                return
            if not self.conn_wait.get("weighing"):
                return  # coming to her anchor
            from freesail.orders.navigation import gathering_way

            if gathering_way(ship):
                return
            self.conn_wait = None
            self.conn_bearing = None
            # his track joined again from where she lies: the stream may have set her past
            # a mark while she came to and rode, and a mark astern is not conned for
            joined = self._joined_track(port, pos) if self.conn_inward else None
            if isinstance(joined, list) and joined:
                self.conn_track, self.conn_i, self.conn_aims = joined, 0, {}
            self.conn_leg_from = pos
            # committed for the slack he weighed for: his legs judged for half an hour on
            # while she gathers way and stands for his first mark
            from freesail.world.sights import greenwich_time

            ahead = greenwich_time(world) + timedelta(seconds=PILOT_WEIGH_AHEAD_S)
            self.conn_wait_for = {
                "at": ahead.isoformat(),
                "until_tick": now + PILOT_COMMITTED_S,
            }
            self._record(
                Severity.NOTABLE,
                "port.pilot_conn",
                "The pilot has her under way again on his track.",
                {"port": port.id, "conn": True, "waited": True},
            )
        if self.anchored:
            self._conn_off("she is at anchor", said=False)
            return
        if self._legs_judged(port, pos, now):
            return  # a leg ahead will not serve: he brings her up and waits
        while self.conn_i < len(self.conn_track):
            words, mark = self.conn_track[self.conn_i]
            # his turning mark taken high for the set on the leg after it (package 43b)
            mark = self._turn_high(self.conn_i, mark)
            brg, dist = bearing_and_distance(pos, mark)
            leg_from = self.conn_leg_from or pos
            heading = float(dyn.heading)
            abaft = abs(units.wrap_pi(math.radians(brg) - heading)) > math.pi / 2.0
            last = self.conn_i == len(self.conn_track) - 1
            # beyond the mark along his leg (package 45c): the stream sets her past a
            # turning mark a cable or two off it, and he takes up the next leg there and
            # does not haul her back to a mark astern of her; the berth the same, within
            # the station's reach of it
            beyond = _beyond_the_leg(leg_from, mark, pos)
            reach = PILOT_AT_STATION_M if last else 6.0 * units.CABLE
            if dist <= PILOT_CONN_MARK_M or ((beyond or (abaft and not last)) and dist <= reach):
                self.conn_i += 1
                self.conn_leg_from = mark  # the next leg begins at the mark passed (45c)
                if last:
                    berth = port.pilot.words.get("anchorage", "") if port.pilot.words else ""
                    self._record(
                        Severity.NOTABLE,
                        "port.pilot_berth",
                        f"The pilot: this is the berth, {words}; let go when you please."
                        + (f" {berth}" if berth and self.conn_inward else ""),
                        {"port": port.id, "mark": words},
                    )
                    self._conn_off("her berth is under her", said=False)
                    return
                continue
            # leg by leg (package 45c): he cons her along the leg from the mark before,
            # for a point on it a little ahead of her, and not straight for the mark from
            # wherever the stream has set her (the frigate in the Goulet's mouth, set a
            # cable south of his turning mark, was steered for the next across the Mingan)
            brg = self._along_the_leg(leg_from, mark, pos, brg)
            wanted = math.radians(brg)
            # a danger on the line to the mark (package 45): he keeps her off it on the
            # hand his own warning names, two points from the line, till it is passed
            kept_off = self._conn_keep_off(port, pos, brg, dist)
            if kept_off is not None:
                wanted, words = kept_off[0], f"{words}, leaving {kept_off[1]}"
            # the line is the one she is to make good over the ground; he allows for the
            # stream across it (package 45c: in the Goulet's flood the schooner, conned for
            # her mark by its bearing at two knots through the water, was set bodily onto
            # the Mingan)
            wanted = self._for_the_stream(wanted)
            lies = self._as_she_will_lie(wanted)
            if lies is not None:
                wanted, words = lies, f"{words}, as near as she will lie"
            from freesail.orders.navigation import manoeuvre_in_hand

            if manoeuvre_in_hand(ship) is not None:
                # going about or wearing for his course: the manoeuvre has it, and he gives
                # none over it (package 58b: cast the wrong way from her anchor, she was
                # given a new course each minute of the wear and worn by turns)
                return
            from freesail.orders.navigation import COURSE_PENDING

            held = (getattr(ship, "extra", None) or {}).get(COURSE_PENDING)
            if (
                isinstance(held, dict)
                and self.conn_bearing is not None
                and abs(units.wrap_pi(wanted - self.conn_bearing)) < PILOT_CONN_TURN_RAD
            ):
                # his course held by the helm till she has way for it (through the eye or
                # by the stern): given again each minute it was held again each minute,
                # and she never came round (package 58b, the intent scenario in the Goulet)
                return
            fresh = self.conn_bearing is None or dyn.helm_mode is not HelmMode.HEADING
            # the course given again when the mark's bearing has drawn half a point from
            # the bearing it was last given for, so that a bearing on a point's edge does
            # not have him ordering E and E by N by turns
            if fresh or abs(units.wrap_pi(wanted - self.conn_bearing)) >= PILOT_CONN_TURN_RAD:
                self._conn_order(port, wanted, words, now)
            return

    def _turn_high(self, i: int, mark: Position) -> Position:
        """Where he steers for the conn track's mark `i` (package 43b): the mark itself, or
        a point off it to the side the stream sets from when the leg after it will not be
        made good (`_made_good_on`): as far off as she will sag over that leg, at most
        `PILOT_TURN_HIGH_MOST_M`, into clear water on a clear line. Reckoned afresh each
        time he looks while she stands for the mark, and kept once it is taken high."""
        aims = self.conn_aims
        if aims is None:
            aims = self.conn_aims = {}
        if aims.get(i) is not None:
            return aims[i]  # once taken high, kept so for the leg
        if i + 1 >= len(self.conn_track):
            return mark  # the berth: no turn after it
        nxt = self.conn_track[i + 1][1]
        leg_brg, length = bearing_and_distance(mark, nxt)
        if length < units.CABLE:
            return mark
        made = self._made_good_on(math.radians(leg_brg))
        if made is None:
            return mark
        sag = units.wrap_pi(made - math.radians(leg_brg))
        if abs(sag) < PILOT_TURN_HIGH_LEAST_RAD:
            return mark
        off_m = min(PILOT_TURN_HIGH_MOST_M, length * abs(math.tan(sag)))
        # the set carries her to the right of the leg (sag clockwise): take the mark to its left
        side = -90.0 if sag > 0.0 else 90.0
        start = self.conn_leg_from or self.world.position
        for share in (1.0, 0.75, 0.5, 0.25):
            aim = destination(mark, (leg_brg + side) % 360.0, off_m * share)
            if self._water_for(aim) and (start is None or self._clear_line(start, aim)):
                aims[i] = aim
                return aim
        return mark

    def _made_good_on(self, line: float) -> float | None:
        """Her course made good over the ground (radians true) when conned for `line`
        under this wind and stream, as the pilot reckons it (package 43b): None when she
        lies the course the stream's allowance asks; else the course she lies on the
        line's side of the wind, with her way and the stream added."""
        ship = self.world.ship
        dyn = getattr(ship, "dyn", None)
        wind = getattr(self.world, "wind", None)
        if dyn is None or wind is None:
            return None
        from freesail.evolutions.scripts import close_hauled_true_angle
        from freesail.physics.integrate import water_velocity

        wanted = self._for_the_stream(line)
        wind_from = _wind_from_over_the_water(self.world, wind)
        closest = close_hauled_true_angle(ship) + PILOT_LIE_MARGIN_RAD + PILOT_SET_WIND_MARGIN_RAD
        x = units.wrap_pi(wanted - wind_from)
        if abs(x) >= closest:
            return None
        heading = units.wrap_2pi(wind_from + (1.0 if x >= 0.0 else -1.0) * closest)
        way = max(float(dyn.u), units.knots_to_ms(PILOT_STREAM_WAY_KN))
        wx, wy = water_velocity(ship)
        east = way * math.sin(heading) + wx
        north = way * math.cos(heading) + wy
        return units.wrap_2pi(math.atan2(east, north))

    def _water_for(self, pos: Position) -> bool:
        """Water enough under her there now, a fathom beneath her keel (package 43b)."""
        chart = getattr(self.world, "chart", None)
        if chart is None:
            return True
        depth = chart.depth_at(pos)
        if depth is None:
            return False
        tide = float(getattr(self.world, "tide_height_m", 0.0) or 0.0)
        hull = getattr(self.world.ship, "hull", None)
        draught = float(hull.spec.draught_m) if hull is not None else 0.0
        return float(depth) + tide >= draught + PILOT_UNDER_KEEL_M

    def _clear_line(self, a: Position, b: Position) -> bool:
        """The line from `a` to `b` clear of the shore and the charted dangers in the
        pilot's own water (his joining leg's offing and berth; package 43b)."""
        from freesail.world.captains import Planner

        return Planner(self.world).clear(
            a, b, PILOT_JOIN_OFFING_NM, PILOT_JOIN_BERTH_NM, units.CABLE
        )

    def _for_the_stream(self, line: float) -> float:
        """The heading that makes good `line` (radians true) over the ground against the
        stream where she is, as the pilot knows his water (package 45c): the stream's part
        across the line taken out by her way through the water, reckoned at no less than
        `PILOT_STREAM_WAY_KN`, the allowance no more than `PILOT_STREAM_MOST_RAD`."""
        ship = self.world.ship
        dyn = getattr(ship, "dyn", None)
        if dyn is None:
            return line
        from freesail.physics.integrate import water_velocity

        wx, wy = water_velocity(ship)
        # the stream across the line, positive to the right of it
        across = wx * math.cos(line) - wy * math.sin(line)
        way = max(float(dyn.u), units.knots_to_ms(PILOT_STREAM_WAY_KN))
        allow = math.asin(max(-1.0, min(1.0, across / way)))
        allow = max(-PILOT_STREAM_MOST_RAD, min(PILOT_STREAM_MOST_RAD, allow))
        return units.wrap_2pi(line - allow)

    def _as_she_will_lie(self, wanted: float) -> float | None:
        """The course nearest `wanted` she will lie, full and by on the tack she is on,
        when `wanted` is nearer the wind than that (package 45c): a pilot does not con a
        ship into the wind's eye (the frigate in the Goulet's mouth, the wind at WNW, was
        given NW by turns and taken aback onto the Fillettes); None when she lies it. The
        wind is the one she sails in, over the water (item 19 of package 68)."""
        from freesail.evolutions.scripts import close_hauled_true_angle

        wind = getattr(self.world, "wind", None)
        if wind is None:
            return None
        wind_from = _wind_from_over_the_water(self.world, wind)
        closest = close_hauled_true_angle(self.world.ship) + PILOT_LIE_MARGIN_RAD
        x = units.wrap_pi(wanted - wind_from)
        if abs(x) >= closest:
            return None
        own = units.wrap_pi(float(self.world.ship.dyn.heading) - wind_from)
        sign = 1.0 if (own if abs(own) > 1e-6 else x) >= 0.0 else -1.0
        lie = units.wrap_2pi(wind_from + sign * closest)
        other = units.wrap_2pi(wind_from - sign * closest)
        # the tack she is on, unless its lie is more than eight points from the course he
        # wants and the other tack's is not (package 58b: cast the wrong way from her anchor,
        # she was given the lie of her own tack, away from his mark, and worn by turns)
        if abs(units.wrap_pi(lie - wanted)) > math.pi / 2.0 >= abs(units.wrap_pi(other - wanted)):
            return other
        return lie

    # -- the conn in a stream (package 58b, item 6) -------------------------------------

    def _stream_at(self, pos: Position, when_ut: datetime) -> tuple[float, float]:
        """The stream over the ground at a place of his water at a moment (m/s east, north),
        as the pilot knows it; none without a tide."""
        tide = getattr(self.world, "tide", None)
        if tide is None:
            return 0.0, 0.0
        state = tide.at(pos, when_ut)
        return float(state.stream_east_ms), float(state.stream_north_ms)

    def _leg_made(self, a: Position, b: Position, when_ut: datetime) -> tuple[bool, Position]:
        """Whether she makes the leg from `a` to `b` good under the wind as it stands and the
        stream his water has on the leg at `when_ut`, and where she is when she has run it
        (package 58b, item 6). She lies the course that allows for the stream, or sags off
        the leg by less than `PILOT_SAG_LEAST_RAD`: made, at `b`. Nearer the wind than she
        lies and sagging more: made only if her sagging track over the leg's length has water
        a fathom beneath her keel all along it and passes no danger within
        `PILOT_WARN_ABEAM_M` with less water over it than she draws; then she is where the
        track ends, off the mark, and the next leg is judged from there (so that a sag that
        leaves her above a danger is found on the leg after). Her way is reckoned at
        `PILOT_JUDGE_WAY_KN`."""
        from freesail.evolutions.scripts import close_hauled_true_angle

        world = self.world
        ship = world.ship
        wind = getattr(world, "wind", None)
        chart = getattr(world, "chart", None)
        brg, length = bearing_and_distance(a, b)
        if getattr(ship, "dyn", None) is None or wind is None or length < units.CABLE:
            return True, b
        mid = destination(a, brg, length / 2.0)
        wx, wy = self._stream_at(mid, when_ut)
        line = math.radians(brg)
        way = units.knots_to_ms(PILOT_JUDGE_WAY_KN)
        across = wx * math.cos(line) - wy * math.sin(line)
        allow = math.asin(max(-1.0, min(1.0, across / way)))
        wanted = units.wrap_2pi(
            line - max(-PILOT_STREAM_MOST_RAD, min(PILOT_STREAM_MOST_RAD, allow))
        )
        vx, vy = wind.vector_at_height(10.0)
        if math.hypot(vx - wx, vy - wy) < 1e-9:
            return True, b
        wind_from = units.wind_direction_from(vx - wx, vy - wy)
        closest = close_hauled_true_angle(ship) + PILOT_LIE_MARGIN_RAD
        x = units.wrap_pi(wanted - wind_from)
        if abs(x) >= closest:
            return True, b
        heading = units.wrap_2pi(wind_from + (1.0 if x >= 0.0 else -1.0) * closest)
        east, north = way * math.sin(heading) + wx, way * math.cos(heading) + wy
        made = math.atan2(east, north)
        sag = units.wrap_pi(made - line)
        if abs(sag) < PILOT_SAG_LEAST_RAD:
            return True, b
        if abs(sag) >= math.pi / 3.0 or chart is None:
            return False, b
        run = length / math.cos(sag)
        made_deg = math.degrees(made) % 360.0
        end = destination(a, made_deg, run)
        tide = float(getattr(world, "tide_height_m", 0.0) or 0.0)
        hull = getattr(ship, "hull", None)
        draught = float(hull.spec.draught_m) if hull is not None else 0.0
        wants = draught + PILOT_UNDER_KEEL_M
        if chart.dangers_ahead(a, made_deg, run, PILOT_WARN_ABEAM_M, tide, wants):
            return False, end
        steps = max(1, int(run // (units.CABLE / 2.0)))
        water = all(
            self._water_for(destination(a, made_deg, run * k / steps)) for k in range(1, steps + 1)
        )
        return water, end

    def _foul_leg(self, pos: Position, when_ut: datetime) -> int | None:
        """The index in his track of the first mark whose leg will not be made good, judged
        from the mark in hand on, each leg from where the one before leaves her (`_leg_made`)
        and for the time she comes to it from `when_ut` at `PILOT_JUDGE_WAY_KN`; None when
        every leg serves."""
        way = units.knots_to_ms(PILOT_JUDGE_WAY_KN)
        if self.conn_i >= len(self.conn_track):
            return None
        # the open water to his mark in hand is hers to work as she can (he cons her for it
        # as near as she will lie); his legs from mark to mark are judged, from where each
        # leaves her, for the time she comes to it at her way over the ground
        start = self.conn_track[self.conn_i][1]
        when = when_ut + timedelta(seconds=bearing_and_distance(pos, start)[1] / way)
        for i in range(self.conn_i + 1, len(self.conn_track)):
            mark = self.conn_track[i][1]
            made, end = self._leg_made(start, mark, when)
            if not made:
                return i
            when = when + timedelta(seconds=bearing_and_distance(start, mark)[1] / way)
            start = end
        return None

    def _legs_judged(self, port: Port, pos: Position, now: int) -> bool:
        """His legs judged ahead before he stands into them (package 58b, item 6), when he
        takes up a mark and every `PILOT_WAIT_LOOK_S` between: True when one will not be
        made good and he has brought her up to wait for it to serve."""
        last = self.conn_judged
        if last is not None and last[0] == self.conn_i and now - int(last[1]) < PILOT_WAIT_LOOK_S:
            return False
        committed = (self.conn_wait_for or {}).get("until_tick")
        if committed is not None and now < int(committed):
            return False  # weighed for the slack: he takes her in on it
        said = (
            bool(last[2])
            if last is not None and len(last) > 2 and last[0] == self.conn_i
            else False
        )
        self.conn_judged = (self.conn_i, now, said)
        from freesail.world.sights import greenwich_time

        now_ut = greenwich_time(self.world)
        # judged for the hour he weighed for while it is still to come, so that a leg he
        # weighed to take at the slack is not judged foul on the way to it
        target = (self.conn_wait_for or {}).get("at")
        if target:
            at = datetime.fromisoformat(str(target))
            if at > now_ut:
                now_ut = at
            else:
                self.conn_wait_for = None
        foul = self._foul_leg(pos, now_ut)
        if foul is None:
            return False
        return self._bring_up_to_wait(port, pos, now, now_ut, foul, said)

    def _waiting_words(self, foul: int, now_ut: datetime) -> tuple[str, str]:
        """(why the leg will not serve, in his words; the stream's word, flood or ebb)."""
        words, mark = self.conn_track[foul]
        start = self.world.position if foul == self.conn_i else self.conn_track[foul - 1][1]
        brg, length = bearing_and_distance(start, mark)
        mid = destination(start, brg, length / 2.0)
        wx, wy = self._stream_at(mid, now_ut)
        tide = getattr(self.world, "tide", None)
        state = tide.at(mid, now_ut) if tide is not None else None
        flood = "flood" if state is None or state.rising else "ebb"
        knots = units.ms_to_knots(math.hypot(wx, wy))
        wind = getattr(self.world, "wind", None)
        wind_words = (
            f"the wind at {units.point_name(float(wind.direction_from))}"
            if wind is not None
            else ""
        )
        from freesail.world.reckoning import rate_words

        stream = f"the {flood} running {rate_words(knots)}" if knots >= 0.25 else "slack water"
        return f"she will not lie up for {words} with {stream} and {wind_words}", flood

    def _bring_up_to_wait(
        self, port: Port, pos: Position, now: int, now_ut: datetime, foul: int, said: bool
    ) -> bool:
        """She is brought up where she is to wait for the stream or the wind (package 58b,
        item 6), the hour he looks for said; in more water than `PILOT_WAIT_MOST_FATHOMS` he
        says he cannot, once for the leg, and cons her on as before."""
        world = self.world
        why, flood = self._waiting_words(foul, now_ut)
        chart = getattr(world, "chart", None)
        depth = chart.depth_at(pos) if chart is not None and pos is not None else None
        fathoms = None if depth is None else units.m_to_fathoms(float(depth))
        name = self.pilot.name if self.pilot is not None else "The pilot"
        if fathoms is None or fathoms > PILOT_WAIT_MOST_FATHOMS:
            if not said:
                self.conn_judged = (self.conn_i, now, True)
                self._record(
                    Severity.NOTABLE,
                    "port.pilot_waits",
                    f"The pilot: {why}; there is too much water here to bring her up, and I "
                    "take her on as near as she will lie.",
                    {"port": port.id, "waits": False, "mark": self.conn_track[foul][0]},
                )
            return False
        when = None
        steps = int(PILOT_WAIT_HORIZON_H * 3600 // PILOT_WAIT_AHEAD_S)
        for k in range(1, steps + 1):
            t = now_ut + timedelta(seconds=k * PILOT_WAIT_AHEAD_S)
            if self._foul_leg(pos, t) is None:
                when = t
                break
        from freesail.world.tide import time_words

        if when is not None:
            local = when + (world.clock.ship_time - now_ut)
            hour = time_words(local.hour + local.minute / 60.0)
            wait = f"wait for the {flood} to slacken, about {hour}"
        else:
            wait = "wait for the wind to serve"
        depth_words = f"{fathoms:.0f} fathoms"
        e = world.submit(
            "come to an anchor",
            actor=PILOT_ACTOR,
            said=f"The pilot: {why}; we bring her up here in {depth_words} and {wait}, sir",
        )
        if e.kind == "order.rejected":
            self._conn_off(f"she could not be brought up ({e.data.get('reason', '')})")
            return True
        self.conn_wait = {
            "since": now,
            "look": now,
            "mark": self.conn_track[foul][0],
            "until": None if when is None else when.isoformat(),
            "weighing": False,
        }
        self._record(
            Severity.NOTABLE,
            "port.pilot_waits",
            f"{name} brings her up to wait: {wait}.",
            {"port": port.id, "waits": True, "mark": self.conn_track[foul][0]},
        )
        return True

    def _anchoring(self) -> bool:
        """Coming to her anchor still (the evolution in hand or waiting for hands)."""
        extra = getattr(self.world.ship, "extra", None) or {}
        runner = extra.get("evolutions") if isinstance(extra, dict) else None
        work = runner.work() if runner is not None and hasattr(runner, "work") else []
        ids = {str(getattr(getattr(i, "evo", None), "id", "")) for i in work}
        return bool(ids & {"come_to_anchor", "let_go_anchor"})

    def _wait_at_anchor(self, port: Port, now: int) -> None:
        """At anchor waiting (package 58b, item 6): every `PILOT_WAIT_LOOK_S` he looks at the
        water; when his legs serve he has her got under way on the tack the first leg
        wants, and takes her in when she has gathered way."""
        wait = self.conn_wait or {}
        world = self.world
        if wait.get("weighing"):
            if now - int(wait.get("weighing_tick") or now) < PILOT_WAIT_WEIGH_S:
                return
            wait["weighing"] = False  # the weighing never came: he looks again
        if now - int(wait.get("look") or now) < PILOT_WAIT_LOOK_S:
            return
        tackle = (getattr(world.ship, "extra", None) or {}).get("ground_tackle")
        riding = tackle.riding_by() if tackle is not None else None
        if (
            riding is None
            or not riding.brought_up
            or riding.dragging
            or self._ground_speed_kn() > 0.5
            or self._anchoring()
        ):
            return  # not yet brought up: he looks when she rides
        wait["look"] = now
        from freesail.world.sights import greenwich_time

        pos = world.position
        if pos is None or self.conn_i >= len(self.conn_track):
            return
        # the legs judged for when she will be under way and in them, not for now: the
        # weighing takes half an hour and more (from 114000 he weighed at "the stream serves
        # now", and the ebb had made against his first leg by the time she had cast)
        under_way_at = greenwich_time(world) + timedelta(seconds=PILOT_WEIGH_AHEAD_S)
        if self._foul_leg(pos, under_way_at) is not None:
            return
        wind = getattr(world, "wind", None)
        brg, _ = bearing_and_distance(pos, self.conn_track[self.conn_i][1])
        heading = math.radians(brg)
        tack = "starboard"
        if wind is not None and units.wrap_pi(float(wind.direction_from) - heading) < 0.0:
            tack = "larboard"
        point = units.point_name(heading)
        e = world.submit(
            f"get under way on the {tack} tack and steer {point}",
            actor=PILOT_ACTOR,
            said=f"The pilot: the stream will serve for {wait.get('mark', 'my track')} by the "
            "time she has weighed; we weigh and take her in",
        )
        if e.kind != "order.rejected":
            wait["weighing"] = True
            wait["weighing_tick"] = now
        else:
            # refused (her boat away, say): the refusal is the line, and he looks again in
            # half an hour, not at every look
            wait["look"] = now + PILOT_WAIT_REFUSED_S - PILOT_WAIT_LOOK_S

    def _along_the_leg(self, a: Position, b: Position, pos: Position, to_mark: float) -> float:
        """The bearing the pilot steers for along the leg from `a` to `b`: a point on the
        leg `PILOT_CONN_AHEAD_M` beyond where she is abreast of it, or the mark itself when
        that is nearer (package 45c); the mark's own bearing when the leg has no length or
        she is past its end."""
        leg_brg, length = bearing_and_distance(a, b)
        if length < units.CABLE:
            return to_mark
        _off, share = _off_the_leg(a, b, pos)
        along = max(0.0, share) * length + PILOT_CONN_AHEAD_M
        if along >= length:
            return to_mark
        aim = destination(a, leg_brg, along)
        return bearing_and_distance(pos, aim)[0]

    def _conn_keep_off(
        self, port: Port, pos: Position, brg_deg: float, to_mark_m: float = math.inf
    ) -> tuple[float, str] | None:
        """The course to steer for the mark with a charted danger on the line kept off
        (package 45): the first danger `dangers_ahead` finds on the line to the mark
        within the warning distance (as `_warn` reads it, with the water the ship wants)
        has the course laid `PILOT_CONN_KEEP_OFF_RAD` toward the deeper water from the
        line, and the words say which hand it is left on; None with the line clear. A
        first version conned her straight for Carrick Road from the outer road and ran
        her onto the Black Rock while the pilot warned of it."""
        chart = getattr(self.world, "chart", None)
        if chart is None:
            return None
        east, north = self._ground_velocity()
        speed = max(math.hypot(east, north), units.knots_to_ms(2.0))
        # no farther than his mark (package 45c): past it the track turns, and the line
        # run on beyond a turning mark found the Goulet's north shore and laid her off it
        # toward the Mingan
        ahead = min(max(PILOT_WARN_MIN_M, speed * PILOT_WARN_AHEAD_S), to_mark_m + units.CABLE)
        tide = float(getattr(self.world, "tide_height_m", 0.0) or 0.0)
        hull = getattr(self.world.ship, "hull", None)
        draught = float(hull.spec.draught_m) if hull is not None else 0.0
        wants = draught + PILOT_UNDER_KEEL_M
        # a danger the line itself runs over (within its own extent, a cable for a rock),
        # not one it passes clear of: his track through the north pass of the Goulet
        # leaves the Mingan two cables to starboard, and a keep-off at the warning's berth
        # laid her two points onto the north shore's ledge (package 45c)
        found = chart.dangers_ahead(pos, brg_deg, ahead, PILOT_CONN_ON_THE_LINE_M, tide, wants)
        if found:
            f, _along, _off, side = found[0]
            deeper = "larboard" if side > 0 else "starboard"
            leave = "starboard" if deeper == "larboard" else "larboard"
            turn = -1.0 if deeper == "larboard" else 1.0
            course = units.wrap_2pi(math.radians(brg_deg) + turn * PILOT_CONN_KEEP_OFF_RAD)
            return course, f"{f.name} to {leave}"
        # the water shoaling on the line (the depth field, as his warning reads it): the
        # course laid off toward the deeper side the same way
        shoal = chart.shoal_ahead(pos, brg_deg, ahead, wants, tide)
        if shoal is None:
            return None
        _along, _depth, side = shoal
        if side == 0:
            return None
        deeper = "starboard" if side > 0 else "larboard"
        turn = 1.0 if side > 0 else -1.0
        course = units.wrap_2pi(math.radians(brg_deg) + turn * PILOT_CONN_KEEP_OFF_RAD)
        return course, f"the shoal water to {'larboard' if side > 0 else 'starboard'}"

    def _conn_order(self, port: Port, wanted: float, mark: str, now: int) -> None:
        world = self.world
        dyn = world.ship.dyn
        point = units.point_name(wanted)
        turn = units.wrap_pi(wanted - float(dyn.heading))
        points = abs(turn) / units.POINT
        if points < 0.25:
            how = "steady as she goes"
        else:
            side = "starboard" if turn > 0 else "port"
            if points < 0.75:
                count = "half a point"
            elif points < 1.5:
                count = "a point"
            else:
                count = f"{int(round(points))} points"
            how = f"{side} {count}"
        said = f"The pilot: {how}; steer {point} for {mark}"
        # a turn toward the wind has the yards trimmed for it first (package 58b, item 6;
        # from 114000 his turn of five points to NNE, the yards still for the wind on the
        # quarter, laid her aback within a minute): the trim now, the helm a minute later
        trimmed_first = False
        wind = getattr(world, "wind", None)
        if points >= PILOT_TRIM_POINTS and wind is not None:
            wind_from = _wind_from_over_the_water(world, wind)
            off_new = abs(units.wrap_pi(wanted - wind_from))
            off_now = abs(units.wrap_pi(float(dyn.heading) - wind_from))
            # his own turn toward the wind, onto a course by the wind (within eight points
            # of it): not a sheer of hers to be met at once, nor a reach
            own_turn = (
                self.conn_bearing is None
                or abs(units.wrap_pi(float(dyn.heading) - self.conn_bearing))
                < PILOT_TRIM_POINTS * units.POINT
            )
            if own_turn and off_new <= 8.0 * units.POINT and off_new < off_now - units.POINT:
                if self.conn_trim_first is None:
                    self.conn_trim_first = now
                    off_pts = off_new / units.POINT
                    trim = (
                        "trim for close hauled"
                        if off_pts <= 8.0
                        else "trim for the wind abeam"
                        if off_pts <= 11.0
                        else "trim for the wind large"
                    )
                    world.submit(
                        trim,
                        actor=PILOT_ACTOR,
                        said=f"The pilot: {trim}, before I put her head to {point}",
                        routine=True,
                    )
                    self.conn_trim_tick = now
                    return
                if now - self.conn_trim_first < PILOT_TRIM_FIRST_S:
                    return
                trimmed_first = True
        self.conn_trim_first = None
        # his routine corrections are routine lines (package 43b; 45c's open item 3: the
        # intent scenario's conn from Bertheaume added two hundred and forty lines to its
        # log, his course every few minutes a notable line); a turn of `PILOT_TRIM_POINTS`
        # and more stays notable, and his warnings are what they were
        quiet = points < PILOT_TRIM_POINTS
        e = world.submit(f"steer {point}", actor=PILOT_ACTOR, said=said, routine=quiet)
        if e.kind == "order.rejected":
            self._conn_off(f"his course was refused ({e.data.get('reason', '')})")
            return
        # the helm's own target as the order laid it (by compass, as `steer` lays a
        # point), so that the officer's hand is known from a change of it and nothing else
        from freesail.ship.parts import HelmMode

        if dyn.helm_mode is HelmMode.HEADING:
            self.conn_heading = float(dyn.target_heading)
        else:
            self.conn_heading = units.parse_course(point)
        self.conn_order_tick = now
        self.conn_bearing = wanted
        if (
            points >= PILOT_TRIM_POINTS
            and not trimmed_first
            and now - self.conn_trim_tick >= PILOT_TRIM_EVERY_S
        ):
            self.conn_trim_tick = now
            # a turn of two points and more: the yards and sheets trimmed to it at his word
            # (package 45c; the owner's merchantman, put five points up for the Goulet's
            # track with her yards for a broad reach, was taken aback and set onto the
            # Fillettes by the flood)
            world.submit(
                "trim sails", actor=PILOT_ACTOR, said="The pilot: trim to it", routine=True
            )

    # -- the pilot's words -----------------------------------------------------------------

    def _stream_turn(self, port: Port, now_ut: datetime, flood: bool) -> datetime | None:
        """The next turn of the stream at the port's outer road to the flood (or the
        ebb), Universal Time; None while it is running that way now (package 37h: the
        pilot's "flood" is the world's own stream in his road, where package 35 said it
        from his high water less six hours and twelve minutes, three hours before the
        game's own turn off Plymouth). Found by ten minutes over a tide and to the minute
        about the turn."""
        tide = self.world.tide
        where = port.outer_road.position
        if tide.at(where, now_ut).flood == flood:
            return None
        step = timedelta(minutes=10)
        t = now_ut
        for _ in range(int(13 * 6)):
            nxt = t + step
            if tide.at(where, nxt).flood == flood:
                for m in range(1, 11):
                    when = t + timedelta(minutes=m)
                    if tide.at(where, when).flood == flood:
                        return when
                return nxt
            t = nxt
        return None

    def _tide_words(self, port: Port) -> str:
        """When the tide serves, in the pilot's words: the port's own high water, which
        he knows (the world's tide at the roads, said to the quarter hour), and the turn of
        the stream in his road to the flood or the ebb he goes in on (package 37h)."""
        world = self.world
        tide = getattr(world, "tide", None)
        if tide is None:
            return "the tide he keeps in his head"
        from freesail.world.sights import greenwich_time
        from freesail.world.tide import time_words

        now_ut = greenwich_time(world)
        waters = tide.high_waters(port.anchorage.position, now_ut, 25.0)
        if not waters:
            return "no high water he can name today"
        hw_ut, height = waters[0]
        offset = (
            timedelta(hours=world.origin.lon_deg / 15.0)
            if world.origin is not None
            else timedelta()
        )
        hw = hw_ut + offset
        enter_on = str(port.tide.get("enter_on", "flood"))
        when = time_words(hw.hour + hw.minute / 60.0)
        rise = units.m_to_feet(height)
        turn = self._stream_turn(port, now_ut, enter_on == "flood")
        if turn is None:
            serves = f"the {enter_on} is making now and serves"
        else:
            local = turn + offset
            serves = (
                f"the {enter_on} will serve from about "
                f"{time_words(local.hour + local.minute / 60.0)}"
            )
        return (
            f"high water at {port.name} about {when}, the tide rising some {rise:.0f} feet; "
            f"{serves}"
        )

    def pilot_words(self, port: Port | None = None) -> str:
        """`the pilot`: the channel, the marks, the anchorage and when the tide serves."""
        if port is None:
            if self.pilot_port is None:
                return "no pilot aboard"
            port = self.ports[self.pilot_port]
        w = port.pilot.words
        return " ".join(
            x
            for x in (
                w.get("channel", ""),
                w.get("marks", ""),
                w.get("anchorage", ""),
                _cap(self._tide_words(port)) + ".",
            )
            if x
        )

    def answer(self, question: str) -> str:
        """`ask the pilot <question>`: by the words of the question."""
        if self.pilot is None or self.pilot_port is None:
            return "There is no pilot aboard to ask."
        port = self.ports[self.pilot_port]
        q = question.lower()
        w = port.pilot.words
        if any(k in q for k in ("tide", "flood", "ebb", "high water", "serve", "when")):
            return f"{self.pilot.name}: {self._tide_words(port)}."
        if any(
            k in q for k in ("channel", "way in", "passage", "go in", "take her in", "entrance")
        ):
            return f"{self.pilot.name}: {w.get('channel', 'he knows the channel')}"
        if any(k in q for k in ("mark", "bearing", "lead", "leading")):
            return f"{self.pilot.name}: {w.get('marks', 'he knows the marks')}"
        if any(k in q for k in ("anchor", "road", "berth", "moor", "lie")):
            return f"{self.pilot.name}: {w.get('anchorage', 'he knows the roads')}"
        if any(k in q for k in ("news", "war", "peace", "port", "town", "fleet", "enemy")):
            return f"{self.pilot.name}: {self.news_words(port)}"
        if any(k in q for k in ("tack", "cast", "under way", "out", "leave", "sail")):
            cast = port.pilot.cast
            course = units.point_name(math.radians(port.pilot.course_out_deg))
            return (
                f"{self.pilot.name}: cast her on the {cast} tack and stand out {course} "
                f"by the pilot's course; {self._tide_words(port)}."
            )
        return f"{self.pilot.name}: {self.pilot_words(port)}"

    # -- readings' words ---------------------------------------------------------------------

    def nearest_by_account(self) -> tuple[Port, float, Any] | None:
        """The nearest port by its roads from the position by account (package 37j), the
        miles to them and the spot; None without a reckoning or a port."""
        nav = getattr(self.world, "navigation", None)
        if nav is None or not self.ports:
            return None
        here = nav.account_now()
        best = None
        for port in self.ports.values():
            spot, d = port.nearest_spot(here)
            if best is None or d < best[1]:
                best = (port, d, spot)
        return best

    def port_words(self) -> dict[str, Any] | None:
        """`the port`: the nearest port within the pilot's cruising ground or in which she
        lies, its stance to her, the pilot, the cutter and the boat. Since package 37j by
        the captain's means (the review's G4: it gave the true bearing and distance of
        the port's road to a tenth of a mile, and the officers steered by it): its bearing
        and distance from the position by account, with the account's doubt, as `shape a
        course for` gives them, and beyond the pilot's ground what the chart and the
        account allow. At anchor in a port she is in it, as anyone aboard can see."""
        from freesail.world.geo import distance_words
        from freesail.world.reckoning import doubt_miles_words

        found = self.nearest_by_account()
        if found is None:
            return None
        port, d_nm, spot = found
        nav = self.world.navigation
        here = nav.account_now()
        bearing = bearing_and_distance(here, spot.position)[0]
        point = units.point_name(math.radians(bearing))
        good = doubt_miles_words(float(nav.doubt_now()["semi_major_nm"]))
        stance = self.stance(port)
        if d_nm > max(port.pilot.cruising_nm, 10.0) and self.in_port() is None:
            return {
                "words": f"no port within the pilot's cruising ground by account; the nearest "
                f"is {port.name}, {point} by account, {distance_words(d_nm * units.NAUTICAL_MILE)}"
                f", the account good to {good}",
                "port": port.id,
                "stance": stance,
                "reach_nm": port.reach_nm,
                "distance_nm": round(d_nm, 1),
                "by": "account",
                "pilot": None,
            }
        in_port = self.in_port()
        if in_port is not None:
            # at anchor in a port she is in it, and in the road she let go in, as anyone
            # aboard can see: the port's business is the world's, and says no figure
            port, spot = in_port, in_port.nearest_spot(self.world.position)[0]
            stance = self.stance(port)
            where = f"at anchor in {port.name}, {spot.name}"
        else:
            where = (
                f"{port.name}, {spot.name} bearing {point} by account, "
                f"{distance_words(d_nm * units.NAUTICAL_MILE)}, the account good to {good}"
            )
        bits = [where, f"the port {stance} to {self.world.nations.get(self.ship_nation).people}"]
        by = port.blockaded_by
        if by is not None:
            # package 39d: a blockaded port says who watches it
            bits.append(f"blockaded by the {self.world.nations.get(by).adjective}")
        if self.pilot is not None:
            bits.append(f"the pilot {self.pilot.name} aboard")
        cutter = self._cutter()
        if cutter is not None:
            if cutter.alongside:
                doing = "alongside"
            elif cutter.plan and cutter.plan[0][0] == "company":
                # package 37h: hailed, she keeps company
                doing = "keeping company"
                if self.cutter_errand == "bring" and self.hail_answer != "take":
                    doing += ", her hail unanswered"
            elif self.cutter_errand in ("bring", "fetch"):
                doing = "standing out toward her"
            else:
                doing = "going back"
            bits.append(f"the pilot {port.pilot.craft} {doing}")
        bits.append(self.boat.words())
        # practice and resupply (between packages 72 and 73): the hoy with her powder, while
        # its job is in hand at this port, and only then, so that the reading is otherwise
        # what it was
        hoy = ordnance.hoy_words(self, port.id)
        if hoy is not None:
            bits.append(hoy[0])
        out = {
            "words": "; ".join(bits),
            "port": port.id,
            "stance": stance,
            "distance_nm": round(d_nm, 2),
            "by": "account",
            "pilot": self.pilot.to_dict() if self.pilot else None,
            "boat_away": self.boat.away,
        }
        if by is not None:
            # package 39d: only a blockaded port's reading carries its state, so an open
            # port's reading is what it was
            out.update({"state": port.state, "blockaded_by": by})
        if hoy is not None:
            out["hoy"] = hoy[1]
        return out

    def pilot_reading(self) -> dict[str, Any] | None:
        if self.pilot is None or self.pilot_port is None:
            return None
        port = self.ports[self.pilot_port]
        return {
            "conn": self.conn,
            "words": f"{self.pilot.name} of {port.name} aboard; {self._tide_words(port)}",
            "name": self.pilot.name,
            "port": port.id,
            "skill": self.pilot.skill,
            "since_tick": self.pilot_since,
            "cast": port.pilot.cast,
            "course_out_deg": port.pilot.course_out_deg,
        }

    def prices_reading(self) -> dict[str, Any] | None:
        """`the prices`: the last list the boat brought off, or for the port she lies in."""
        port = self.in_port()
        if port is not None and port.id in self.price_lists:
            tick, when, listed = self.price_lists[port.id]
            return {
                "words": f"at {port.name} ({when}): "
                + ", ".join(f"{g} {pounds_words(p)} a ton" for g, p in listed),
                "port": port.id,
                "prices": dict(listed),
                "when": when,
            }
        if self.price_lists:
            pid, (tick, when, listed) = list(self.price_lists.items())[-1]
            return {
                "words": f"the last list, {self.ports[pid].name} ({when}): "
                + ", ".join(f"{g} {pounds_words(p)} a ton" for g, p in listed),
                "port": pid,
                "prices": dict(listed),
                "when": when,
            }
        return None

    def no_prices_words(self) -> str:
        port = self.in_port()
        if port is None:
            return "no prices are known: the boat has not been ashore in any port"
        return f"the prices at {port.name} are not known until the boat has been ashore"

    # -- the price list, the market -------------------------------------------------------

    def _write_price_list(
        self, port: Port, at_start: bool = False, why: str = ""
    ) -> list[tuple[str, float]]:
        world = self.world
        port.market.recover(world.clock.tick)
        listed = port.market.listing(world.clock.ship_time, world.nations, port.nation)
        clock = world.clock
        when = f"{clock.ship_time:%d %B}, {units.time_stamp(clock.ship_time)}"
        self.price_lists[port.id] = (clock.tick, when, listed)
        if not at_start:
            papers = getattr(world, "papers", None)
            if papers is not None:
                line = papers.write(
                    "the price list", why or f"the prices at {port.name} brought off by the boat"
                )
                self._record(Severity.ROUTINE, "paper.written", line, {"paper": "the price list"})
        return listed

    def trade(self, verb: str, tons: float, good_words: str) -> tuple[str, dict[str, Any]]:
        """`buy <n> tons of <good>` and `sell <n> tons of <good>`: the bargain made at
        the port's price now, the purse moved, and the boat sent for the goods (the hold
        is changed when the boat is back, `_boat_back`); refused in words when she is
        not in port, the prices are not known, the boat is away, the hold is full or the
        purse short."""
        from freesail.orders.errors import OrderError

        world = self.world
        port = self.in_port()
        if port is None:
            raise OrderError(
                "She is not in port; the market is ashore and the boat has nowhere to go."
            )
        if self.stance(port) in ("hostile", "closed"):
            raise OrderError(
                f"{port.name} is {self.stance(port)} to her; there is no trading there."
            )
        if port.id not in self.price_lists:
            raise OrderError(
                f"The prices at {port.name} are not known; send the boat ashore first, and the "
                "purser will bring the list off."
            )
        if self.boat.away:
            raise OrderError(
                f"{self.boat.boat_name[:1].upper()}{self.boat.boat_name[1:]} is away; wait for her."
            )
        good = port.market.find(good_words)
        if good is None:
            names = ", ".join(port.market.goods)
            raise OrderError(
                f"{_possessive(port.name)} market has no {good_words}; it deals in {names}."
            )
        if tons <= 0:
            raise OrderError("How many tons? Say 'buy twenty tons of tin'.")
        price = self.price_of(port, good.good)
        sum_pounds = price * tons
        hold: Hold = world.hold
        purse: Purse = world.purse
        now = world.clock.tick
        if verb == "buy":
            if tons > hold.room_tons + 1e-9:
                raise OrderError(
                    f"There is room in the hold for {hold.room_tons:g} tons and no more; "
                    f"{tons:g} tons of {good.good} will not stow."
                )
            if sum_pounds > purse.pounds + 1e-9:
                raise OrderError(
                    f"{tons:g} tons of {good.good} at {pounds_words(price)} a ton is "
                    f"{pounds_words(sum_pounds)}, and the purse holds {purse.words()}."
                )
            purse.pay(sum_pounds, f"{tons:g} tons of {good.good} at {port.name}", now)
            port.market.bought_from_port(good.good, tons)
            self._send_boat(
                port,
                "purchase",
                [{"kind": "purchase", "good": good.good, "tons": tons, "pounds": sum_pounds}],
            )
            text = (
                f"Bought {tons:g} tons of {good.good} at {port.name} at {pounds_words(price)} "
                f"a ton, {pounds_words(sum_pounds)} paid; the boat goes for it. The purse: "
                f"{purse.words()}."
            )
        else:
            have = hold.goods.get(good.good, 0.0)
            if tons > have + 1e-9:
                raise OrderError(
                    f"The hold has {have:g} tons of {good.good}, not {tons:g}; the manifest "
                    f"says so."
                )
            hold.break_out(good.good, tons)
            purse.take(sum_pounds, f"{tons:g} tons of {good.good} sold at {port.name}", now)
            port.market.sold_to_port(good.good, tons)
            self._send_boat(
                port,
                "sale",
                [{"kind": "sale", "good": good.good, "tons": tons, "pounds": sum_pounds}],
            )
            text = (
                f"Sold {tons:g} tons of {good.good} at {port.name} at {pounds_words(price)} a ton, "
                f"{pounds_words(sum_pounds)} taken; the boat lands it. The purse: {purse.words()}."
            )
        papers = getattr(world, "papers", None)
        if papers is not None:
            line = papers.write(
                "the manifest",
                f"{tons:g} tons of {good.good} {'bought' if verb == 'buy' else 'sold'} at "
                f"{port.name}",
            )
            self._record(Severity.ROUTINE, "paper.written", line, {"paper": "the manifest"})
        return text, {
            "port": port.id,
            "good": good.good,
            "tons": tons,
            "price_pounds": price,
            "sum_pounds": sum_pounds,
            "purse_pounds": round(purse.pounds, 2),
        }

    def trade_together(
        self, verb: str, bargains: list[tuple[float, str]]
    ) -> tuple[str, dict[str, Any]]:
        """Several bargains said in one order (`buy 20 tons of salt fish and 8 tons of
        pilchards`; package 37l, game 10, where it was read as one cargo named "salt fish
        and 8 pilchards"): each struck at the port's price now, as `trade` strikes one, and
        the boat sent once for them all. Every bargain is read and weighed before any is
        struck (the goods, the room in the hold and the purse for them together), so that
        one that cannot be struck refuses the order whole and nothing is paid."""
        from freesail.orders.errors import OrderError

        world = self.world
        port = self.in_port()
        if port is None:
            raise OrderError(
                "She is not in port; the market is ashore and the boat has nowhere to go."
            )
        if self.stance(port) in ("hostile", "closed"):
            raise OrderError(
                f"{port.name} is {self.stance(port)} to her; there is no trading there."
            )
        if port.id not in self.price_lists:
            raise OrderError(
                f"The prices at {port.name} are not known; send the boat ashore first, and the "
                "purser will bring the list off."
            )
        if self.boat.away:
            raise OrderError(
                f"{self.boat.boat_name[:1].upper()}{self.boat.boat_name[1:]} is away; wait for her."
            )
        hold: Hold = world.hold
        purse: Purse = world.purse
        struck: list[tuple[str, float, float, float]] = []  # good, tons, price, sum
        for tons, good_words in bargains:
            good = port.market.find(good_words)
            if good is None:
                names = ", ".join(port.market.goods)
                raise OrderError(
                    f"{_possessive(port.name)} market has no {good_words}; it deals in {names}."
                )
            if tons <= 0:
                raise OrderError(f"How many tons of {good.good}? Say 'buy twenty tons of tin'.")
            price = self.price_of(port, good.good)
            struck.append((good.good, tons, price, price * tons))
        total_tons = sum(t for _, t, _, _ in struck)
        total_pounds = sum(x for _, _, _, x in struck)
        if verb == "buy":
            if total_tons > hold.room_tons + 1e-9:
                raise OrderError(
                    f"There is room in the hold for {hold.room_tons:g} tons and no more; the "
                    f"{total_tons:g} tons bought together will not stow."
                )
            if total_pounds > purse.pounds + 1e-9:
                raise OrderError(
                    f"The bargains together are {pounds_words(total_pounds)}, and the purse "
                    f"holds {purse.words()}."
                )
        else:
            for good_name, _tons, _, _ in struck:
                have = hold.goods.get(good_name, 0.0)
                wanted = sum(t for g, t, _, _ in struck if g == good_name)
                if wanted > have + 1e-9:
                    raise OrderError(
                        f"The hold has {have:g} tons of {good_name}, not {wanted:g}; the "
                        "manifest says so."
                    )
        now = world.clock.tick
        items: list[dict[str, Any]] = []
        said: list[str] = []
        for good_name, tons, price, sum_pounds in struck:
            if verb == "buy":
                purse.pay(sum_pounds, f"{tons:g} tons of {good_name} at {port.name}", now)
                port.market.bought_from_port(good_name, tons)
                items.append(
                    {"kind": "purchase", "good": good_name, "tons": tons, "pounds": sum_pounds}
                )
            else:
                hold.break_out(good_name, tons)
                purse.take(sum_pounds, f"{tons:g} tons of {good_name} sold at {port.name}", now)
                port.market.sold_to_port(good_name, tons)
                items.append(
                    {"kind": "sale", "good": good_name, "tons": tons, "pounds": sum_pounds}
                )
            said.append(f"{tons:g} tons of {good_name} at {pounds_words(price)} a ton")
        self._send_boat(port, "purchase" if verb == "buy" else "sale", items)
        listed = "; ".join(said)
        if verb == "buy":
            text = (
                f"Bought at {port.name}: {listed}; {pounds_words(total_pounds)} paid in all; the "
                f"boat goes for it. The purse: {purse.words()}."
            )
        else:
            text = (
                f"Sold at {port.name}: {listed}; {pounds_words(total_pounds)} taken in all; the "
                f"boat lands it. The purse: {purse.words()}."
            )
        papers = getattr(world, "papers", None)
        if papers is not None:
            for good_name, tons, _, _ in struck:
                line = papers.write(
                    "the manifest",
                    f"{tons:g} tons of {good_name} {'bought' if verb == 'buy' else 'sold'} at "
                    f"{port.name}",
                )
                self._record(Severity.ROUTINE, "paper.written", line, {"paper": "the manifest"})
        return text, {
            "port": port.id,
            "bargains": [
                {"good": g, "tons": t, "price_pounds": pr, "sum_pounds": x}
                for g, t, pr, x in struck
            ],
            "sum_pounds": total_pounds,
            "purse_pounds": round(purse.pounds, 2),
        }

    # -- the yard and the crew pool ---------------------------------------------------------

    def demand(self, item_words: str, quantity: float | None) -> tuple[str, dict[str, Any]]:
        """`demand a topmast from the yard`, `take in twenty tons of water`, `take in
        provisions for thirty days`, `buy a suit of sails`: the yard's job with its time
        and its cost, the stores or the booms moved when it is done."""
        from freesail.orders.errors import OrderError

        world = self.world
        port = self.in_port()
        if port is None:
            raise OrderError("She is not in port; there is no yard to demand it of.")
        if self.stance(port) in ("hostile", "closed"):
            raise OrderError(
                f"{port.name} is {self.stance(port)} to her; the yard will not serve her."
            )
        item = port.dockyard.find(item_words)
        if item is None:
            names = ", ".join(port.dockyard.items)
            raise OrderError(f"The yard at {port.name} has no {item_words}; it supplies {names}.")
        ship = world.ship
        crew = ship.extra.get("crew") if hasattr(ship, "extra") else None
        complement = crew.complement if crew is not None else 0
        qty = float(quantity) if quantity else 1.0
        if item.item == "water":
            hours, cost = item.hours_per_ton * qty, item.pounds_per_ton * qty
            words = f"{qty:g} tons of water"
        elif item.item == "provisions":
            hours, cost = item.hours_per_day * qty, item.pounds_per_man_day * qty * complement
            words = f"provisions for {qty:g} days"
        elif item.item == "cordage":
            fathoms = qty if quantity else 120.0
            hours, cost = item.hours, item.pounds_per_fathom * fathoms
            qty = fathoms
            words = f"{fathoms:g} fathoms of cordage"
        elif item.item == "suit of sails":
            area = (
                sum(float(s.area_m2) for s in ship.sails.values())
                if hasattr(ship, "sails")
                else 0.0
            )
            hours, cost = item.hours, item.pounds_per_100m2 * area / 100.0
            words = "a suit of sails"
        else:
            hours, cost = item.hours, item.pounds
            words = f"a spare {item.item.replace('_', ' ')}"
        kind = port.dockyard.kind
        purse: Purse = world.purse
        now = world.clock.tick
        if cost > 0:
            if cost > purse.pounds + 1e-9:
                raise OrderError(
                    f"{words} costs {pounds_words(cost)} and the purse holds {purse.words()}."
                )
            purse.pay(cost, f"{words} from the {kind} at {port.name}", now)
        due = now + int(hours * 3600)
        self.jobs.append(
            Job(
                due,
                "yard",
                port.id,
                {"item": item.item, "qty": qty, "words": words, "cost": cost},
                hull=self.hull_id,
            )
        )
        how = (
            "by demand on the King's yard, surveyed and vouched"
            if kind == "yard"
            else f"from the chandlers for {pounds_words(cost)}"
        )
        text = (
            f"Demanded {words} {how} at {port.name}; it will be alongside in {_hours_words(hours)}."
        )
        return text, {
            "port": port.id,
            "item": item.item,
            "quantity": qty,
            "hours": hours,
            "cost_pounds": cost,
            "due_tick": due,
        }

    def enter_hands(self, n: int, rating: str) -> tuple[str, dict[str, Any]]:
        """`enter ten able seamen`: the hands the port's pool has at its bounty, come off
        by the boat after the pool's delay and mustered into the crew."""
        from freesail.orders.errors import OrderError

        world = self.world
        port = self.in_port()
        if port is None:
            raise OrderError("She is not in port; there are no hands to be had at sea.")
        if self.stance(port) in ("hostile", "closed"):
            raise OrderError(f"{port.name} is {self.stance(port)} to her; no hands will enter.")
        rating = (
            rating.strip()
            .lower()
            .removesuffix(" seamen")
            .removesuffix(" seaman")
            .removesuffix(" men")
        )
        rating = {"landsmen": "landsman", "able bodied": "able", "ab": "able"}.get(rating, rating)
        if rating not in RECRUIT_RATINGS:
            raise OrderError(
                f"'{rating}' is not a rating hands enter at; say able, ordinary or landsmen."
            )
        pool = port.crew_pool.get(rating)
        if not pool or pool.get("hands", 0) <= 0:
            raise OrderError(f"No {rating} hands are to be had at {port.name}.")
        crew = world.ship.extra.get("crew") if hasattr(world.ship, "extra") else None
        if crew is None:
            raise OrderError(
                "There is no ship's company mustered in this ship to enter hands into."
            )
        n = int(n)
        if n <= 0:
            raise OrderError("How many? Say 'enter six able seamen'.")
        have = int(pool.get("hands", 0))
        taken = min(n, have)
        bounty = float(pool.get("pounds", 0.0)) * taken
        purse: Purse = world.purse
        if bounty > purse.pounds + 1e-9:
            raise OrderError(
                f"{taken} {rating} at {pounds_words(pool.get('pounds', 0.0))} bounty each is "
                f"{pounds_words(bounty)}; the purse holds {purse.words()}."
            )
        now = world.clock.tick
        if bounty > 0:
            purse.pay(bounty, f"bounty for {taken} {rating} at {port.name}", now)
        pool["hands"] = have - taken
        delay_h = float(pool.get("delay_h", 12.0))
        due = now + int(delay_h * 3600)
        self.jobs.append(
            Job(
                due,
                "recruits",
                port.id,
                {"n": taken, "rating": rating, "bounty": bounty},
                hull=self.hull_id,
            )
        )
        short = "" if taken == n else f" ({n} asked; {port.name} has no more)"
        text = (
            f"Entered {taken} {rating} at {port.name} at "
            f"{pounds_words(pool.get('pounds', 0.0))} bounty each{short}; "
            f"they come off in {_hours_words(delay_h)}."
        )
        return text, {
            "port": port.id,
            "n": taken,
            "rating": rating,
            "bounty_pounds": bounty,
            "due_tick": due,
        }

    def _apply_job(self, job: Job) -> None:
        world = self.world
        if job.kind == "boat_to":
            # the boat at another hull and back (package 82): no port's job
            self._boat_to_job(job)
            return
        port = self.ports.get(job.port_id)
        if port is None:
            return
        if job.kind == "waterman":
            # the waterman's pull done (package 68): landed at the quay, or aboard
            p = world.people.find(str(job.payload.get("person") or ""))
            if p is None or p.where != "boat":
                return
            if job.payload.get("to") == "shore":
                p.aboard, p.where, p.port, p.ashore_at = False, "shore", port.id, "quay"
                self._record(
                    Severity.NOTABLE,
                    "person.ashore",
                    f"{p.name} landed at {port.shore.name} from a waterman's boat.",
                    {"person": p.name, "port": port.id},
                )
            else:
                p.aboard, p.where = True, "quarterdeck"
                self._record(
                    Severity.NOTABLE,
                    "person.aboard",
                    f"{p.name} came aboard from a waterman's boat.",
                    {"person": p.name, "port": port.id},
                )
            return
        if job.kind == "boat":
            # the sleeping hull's boat at the quay and back (step 4): the script's phases
            # run by the job's time
            if not self.boat.away:
                return
            stage = str(job.payload.get("stage") or "")
            phases = ("ashore",) if stage == "ashore" else ("returning", "alongside")
            for phase in phases:
                for severity, kind, text, data in self.boat_phase(phase):
                    self._record(severity, kind, text, data)
            return
        if job.kind == "yard":
            item, qty, words = job.payload["item"], float(job.payload["qty"]), job.payload["words"]
            ship = world.ship
            from freesail.ship.parts import SpareSail, booms, cordage, sail_room

            if item == "water":
                world.stores.water_tons += qty
                done = f"{words} came off from the quay and was started into the ground tier"
                # watered: the foul casks started and filled sweet, and the days since she
                # watered counted afresh (the director's `aboard:` table reads them)
                if getattr(world.stores, "foul", False):
                    world.stores.foul = False
                    done += ", the foul water started overboard and the casks filled sweet"
                world.stores.watered_tick = world.clock.tick
                paper = "the purser's books"
            elif item == "provisions":
                world.stores.provisions_days += qty
                done = f"{words} came off and were stowed"
                paper = "the purser's books"
            elif item == "cordage":
                cordage(ship).fathoms += qty
                done = f"{words} came off from the ropehouse into the boatswain's store"
                paper = "the boatswain's store book"
            elif item == "suit of sails":
                room = sail_room(ship)
                for sail_id, sail in ship.sails.items():
                    room.stow(SpareSail(sail_id, getattr(sail, "canvas_no", None), 100.0))
                done = (
                    "a suit of sails came off from the loft and was struck down into the sail room"
                )
                paper = "the sailmaker's account"
            else:
                store = booms(ship)
                store.counts[item] = store.counts.get(item, 0) + 1
                done = f"{words} came off and was got in on the booms"
                paper = "the booms' list"
            self._record(
                Severity.NOTABLE,
                "yard.done",
                f"{done[:1].upper()}{done[1:]}.",
                {"port": port.id, **job.payload},
            )
            papers = getattr(world, "papers", None)
            if papers is not None:
                self._record(
                    Severity.ROUTINE, "paper.written", papers.write(paper, done), {"paper": paper}
                )
        elif job.kind == "recruits":
            self._muster_recruits(port, int(job.payload["n"]), str(job.payload["rating"]))
        elif job.kind == "ordnance":
            # the hoy with the powder and shot, alongside and then stowed (practice and
            # resupply, between packages 72 and 73; `world.ordnance`)
            ordnance.apply_job(self, job, port)
        elif job.kind == "lighter":
            # package 53: the goods bought at the market in person, off by the port's lighter
            for item in job.payload.get("items") or []:
                good, tons = str(item["good"]), float(item["tons"])
                try:
                    world.hold.stow(good, tons)
                    said = (
                        f"{tons:g} tons of {good} came off by the lighter from {port.name} "
                        f"and were struck down into the hold; the manifest {world.hold.words()}."
                    )
                except ValueError as e:
                    said = (
                        f"{tons:g} tons of {good} came off by the lighter, but {e}; it lies "
                        "on deck."
                    )
                self._record(
                    Severity.NOTABLE,
                    "market.bought",
                    said,
                    {"port": port.id, "good": good, "tons": tons, "by": "lighter"},
                )

    def _muster_recruits(self, port: Port, n: int, rating: str) -> None:
        from freesail.crew.model import RATING_SKILL, Rating, Sailor, Station, Watch
        from freesail.crew.muster import abbreviate, name_lists

        world = self.world
        crew = world.ship.extra.get("crew")
        if crew is None:
            return
        nation = world.nations.get(port.nation)
        lists = name_lists()
        names_key = nation.names if nation.names in lists else "english"
        given, surnames = lists[names_key]
        stream: random.Random = world.rng.stream("recruits")
        used = {s.name for s in crew.sailors}
        r = Rating(rating)
        deck, aloft = RATING_SKILL[r]
        start = len(crew.sailors)
        entered = []
        for i in range(n):
            name = f"{abbreviate(stream.choice(given))} {stream.choice(surnames)}"
            while name in used:
                name = f"{abbreviate(stream.choice(given))} {stream.choice(surnames)}"
            used.add(name)
            station = Station.WAISTERS if r is Rating.LANDSMAN else Station.AFTERGUARD
            watch = (Watch.STARBOARD, Watch.LARBOARD)[(start + i) % 2]
            sailor = Sailor(
                id=f"s{start + i + 1:03d}",
                name=name,
                rating=r,
                station=station,
                watch=watch,
                skill_aloft=aloft + stream.uniform(-0.05, 0.05),
                skill_deck=deck + stream.uniform(-0.05, 0.05),
            )
            crew.sailors.append(sailor)
            entered.append(sailor.name)
        crew.reindex()
        word = {"able": "able seamen", "ordinary": "ordinary seamen", "landsman": "landsmen"}[
            rating
        ]
        self._record(
            Severity.NOTABLE,
            "crew.entered",
            f"Entered {n} {word} from {port.name}, come off in the boat: {', '.join(entered)}; "
            f"the company is {crew.complement}.",
            {"port": port.id, "n": n, "rating": rating, "names": entered},
        )

    # -- the boat ---------------------------------------------------------------------------

    def boat_spec(self) -> Any:
        """The boat sent on an errand: the largest the ship carries (the launch or the
        long-boat; judgement: the errands here are cargo and water)."""
        boats = getattr(getattr(self.world.ship, "spec", None), "boats", None) or []
        return max(boats, key=lambda b: (b.tons, b.length_ft)) if boats else None

    def _send_boat(
        self,
        port: Port,
        errand: str,
        carrying: list[dict[str, Any]],
        people: list[str] | None = None,
    ) -> str:
        """Start the boat's evolution (`data/evolutions/send_boat.yaml`) on its errand."""
        from freesail.orders.errors import OrderError

        world = self.world
        boat = self.boat_spec()
        if boat is None:
            raise OrderError("She carries no boat: the ship's file lists none.")
        if self.boat.away:
            raise OrderError(f"{boat.name[:1].upper()}{boat.name[1:]} is away already.")
        runner = world.ship.extra.get("evolutions")
        if runner is None:
            raise OrderError("There is no one to man the boat: no evolution runner is fitted.")
        if self.coarse:
            return self._send_boat_coarse(port, boat, errand, carrying, list(people or []))
        was = self.boat
        self.boat = BoatState(
            away=True,
            boat_id=boat.id,
            boat_name=boat.name,
            errand=errand,
            port_id=port.id,
            carrying=list(carrying),
            phase="hoisting out",
            since_tick=world.clock.tick,
            people=list(people or []),
        )
        try:
            return runner.start(world.ship, "send_boat", "her", {"errand": errand, "port": port.id})
        except OrderError:
            # the order refused (package 45c): the boat stays at the booms, and nobody is
            # left sitting in her
            self.boat = was
            self._people_back(people or [])
            raise

    def _send_boat_coarse(
        self, port: Port, boat: Any, errand: str, carrying: list[dict[str, Any]], people: list[str]
    ) -> str:
        """The boat's errand on a sleeping hull (package 84, step 4; the design's §2.5): a job
        of the port with the boat's time and no hands, hoisted out, the pull to the quay at the
        boat's pace, the business ashore by its errand, the pull back and the boat hoisted in,
        two jobs at their ticks (`_apply_job`, "boat": the boat ashore, and back), each doing
        what the boat's script does at that phase (`boat_phase`); the log says her away now."""
        world = self.world
        now = int(world.clock.tick)
        pull_s = self.to_shore_m(port) / units.knots_to_ms(BOAT_PACE_KN)
        ashore_s = float(BOAT_ASHORE_S.get(errand, BOAT_ASHORE_S["message"]))
        ashore_at = now + BOAT_HOIST_OUT_S + int(pull_s)
        back_at = ashore_at + int(ashore_s) + int(pull_s) + BOAT_HOIST_IN_S
        self.boat = BoatState(
            away=True,
            boat_id=boat.id,
            boat_name=boat.name,
            errand=errand,
            port_id=port.id,
            carrying=list(carrying),
            phase="pulling for the shore",
            since_tick=now,
            people=list(people),
        )
        self.jobs.append(Job(ashore_at, "boat", port.id, {"stage": "ashore"}, hull=self.hull_id))
        self.jobs.append(Job(back_at, "boat", port.id, {"stage": "back"}, hull=self.hull_id))
        minutes = max(1, round((back_at - now) / 60))
        tail = (
            f"; back alongside in some {minutes} minutes (the boat's pull by the plan: her "
            "hull sleeps)."
        )
        text = ""
        for severity, kind, line, data in self.boat_phase("away"):
            if kind == "boat.away":
                # the World says an evolution's start by its runner's line, which a sleeping
                # hull has not got: the boat's own line carries the time instead
                line = line.rstrip(".") + tail
                text = line
            self._record(severity, kind, line, data | {"back_at": back_at})
        return text

    def send_boat(self, words: str) -> tuple[str, dict[str, Any]]:
        """`send the boat ashore [with the purser | with <person> | for the prices | with
        a letter]`: the boat away to the port's quay; what it does there is its errand."""
        from freesail.orders.errors import OrderError

        world = self.world
        port = self.in_port()
        if port is None:
            found = self.nearest(IN_PORT_NM * 2.5)
            if found is not None and not self.anchored:
                raise OrderError(
                    f"She is under way; bring her to an anchor in "
                    f"{_possessive(found[0].name)} roads before the boat goes ashore."
                )
            raise OrderError("She is not in port; there is no shore within a boat's pull.")
        if self.stance(port) == "hostile":
            raise OrderError(f"{port.name} is hostile to her; a boat sent in would be taken.")
        low = words.lower()
        errand = "prices"
        people: list[str] = []
        carrying: list[dict[str, Any]] = []
        if "letter" in low or "message" in low or "dispatch" in low or "despatch" in low:
            errand = "message"
            carrying.append({"kind": "letter_out", "text": words})
        for person in self._passengers(words):
            if not person.aboard:
                raise OrderError(f"{person.name} is {world.people.state_words(person)}.")
            if person.occupied:
                raise OrderError(f"{person.name} is at the {person.task}.")
        for person in self._passengers(words):
            people.append(person.id)
            person.aboard = False
            person.where = "boat"
            errand = "person" if errand == "prices" and person.role != "purser" else errand
        if any(w in low for w in ("water", "provisions", "yard", "recruits", "hands")):
            errand = "yard"
        text = self._send_boat(port, errand, carrying, people)
        return text, {"port": port.id, "errand": errand, "people": people}

    def _passengers(self, words: str) -> list[Any]:
        """The people named after 'with' in `send the boat ashore with ...` (package 68;
        the cold review of 2026-10-22, R-62: "with the captain and Mr Pearce" dropped both
        and the errand fell back to "for the prices"): each name found among the people, or
        the order refused in words, the boat not sent. The captain goes ashore by his own
        word. Words of the errand ('a letter', 'water') name nobody and are passed over."""
        from freesail.orders.errors import OrderError

        low = " " + " ".join(str(words).lower().split())
        i = low.find(" with ")
        if i < 0:
            return []
        rest = low[i + len(" with ") :]
        for stop in (" for ", " to "):
            j = rest.find(stop)
            if j > 0:
                rest = rest[:j]
        found: list[Any] = []
        for name in re.split(r"\s*,\s*|\s+and\s+(?:with\s+)?|\s+with\s+", rest.strip(" .")):
            name = name.strip()
            if not name or any(w in name for w in _ERRAND_WORDS):
                continue
            person = self.world.people.find(name)
            if person is None:
                raise OrderError(
                    f"Nobody aboard answers to '{name}'; the boat is not sent. The people: "
                    f"{', '.join(p.name for p in self.world.people.all if p.aboard)}."
                )
            if person is self.world.people.captain:
                raise OrderError(
                    "The captain goes ashore by his own word, 'go ashore' in the boat or 'hire "
                    "a waterman'; the others go by 'send the boat ashore with <name>'; the "
                    "boat is not sent."
                )
            if person not in found:
                found.append(person)
        return found

    def _people_back(self, people: list[str]) -> None:
        for pid in people:
            p = self.world.people.find(pid)
            if p is not None:
                p.aboard = True
                p.where = "deck"

    def _boat_kept(self) -> None:
        """The boat's state kept with her work (package 45c; the owner's note 3 of gate
        m6a-2, "the ghosted boat"): once a minute, a boat said to be away whose work is no
        longer in the runner's hands (the order belayed, or refused or failed when its turn
        came after waiting on the hands as the ship came to) is not left "hoisting out" for
        ever, refusing every boat order after it: she was never hoisted out, she is at the
        booms again, whoever was to go in her is on deck, and the log says so. A boat
        already away is not belayed (`orders.work`), so that she cannot vanish from the
        water; were she found so, she is brought alongside as on her return."""
        if self.boat.errand == "to_ship":
            return  # the boat at another hull (package 82): the port's jobs keep her
        runner = self.world.ship.extra.get("evolutions")
        if runner is None:
            return
        if any(i.evo.id == "send_boat" for i in getattr(runner, "instances", [])):
            return
        name = self.boat.boat_name
        head = f"{name[:1].upper()}{name[1:]}"
        port = self.ports.get(self.boat.port_id)
        if self.boat.phase != "hoisting out" and port is not None:
            for severity, kind, text, data in self._boat_back(port):
                self._record(severity, kind, text, data)
            return
        people = [
            self.world.people.find(pid).name
            for pid in self.boat.people
            if self.world.people.find(pid) is not None
        ]
        self._people_back(self.boat.people)
        errand = _errand_words(self.boat.errand)
        self.boat = BoatState(boat_name=name, boat_id=self.boat.boat_id)
        who = f"; {_and(people)} on deck again" if people else ""
        self._record(
            Severity.NOTABLE,
            "boat.stood_down",
            f"{head} was not sent away {errand}: the work to send her was belayed or could not "
            f"be carried out; she is at the booms{who}. Send her again when you please.",
            {"boat": self.boat.boat_id, "people": list(people)},
        )

    def boat_phase(self, phase: str) -> list[tuple[Severity, str, str, dict[str, Any]]]:
        """The boat's script says where it is (`SendBoatScript`): the lines, and what the
        boat does ashore and brings back."""
        world = self.world
        port = self.ports.get(self.boat.port_id)
        if port is None:
            return []
        self.boat.phase = {
            "away": "pulling for the shore",
            "ashore": "at the quay",
            "returning": "pulling back to the ship",
        }.get(phase, phase)
        name = self.boat.boat_name
        head = f"{name[:1].upper()}{name[1:]}"
        lines: list[tuple[Severity, str, str, dict[str, Any]]] = []
        if phase == "away":
            who = ""
            if self.boat.people:
                names = [
                    world.people.find(pid).name
                    for pid in self.boat.people
                    if world.people.find(pid)
                ]
                who = f" with {_and(names)}" if names else ""
            lines.append(
                (
                    Severity.NOTABLE,
                    "boat.away",
                    f"{head} away for {port.shore.name}{who}, {_errand_words(self.boat.errand)}.",
                    {"port": port.id, "errand": self.boat.errand},
                )
            )
        elif phase == "ashore":
            lines.append(
                (
                    Severity.ROUTINE,
                    "boat.ashore",
                    f"{head} landed at {port.shore.name}.",
                    {"port": port.id},
                )
            )
            for pid in self.boat.people:
                p = world.people.find(pid)
                if p is not None:
                    p.where = "shore"
            lines.extend(self._land_and_take_off(port))
            # the business ashore: the purser's list, the letters waiting, a purchase
            self.boat.bringing = []
            if (
                self.boat.errand in ("prices", "person", "message", "yard")
                or port.id not in self.price_lists
            ):
                self.boat.bringing.append({"kind": "prices"})
            for letter in list(port.letters):
                self.boat.bringing.append(
                    {
                        "kind": "letter",
                        "text": letter.text,
                        "origin": letter.origin,
                        "to": letter.to,
                    }
                )
                port.letters.remove(letter)
            for item in self.boat.carrying:
                if item["kind"] == "purchase":
                    self.boat.bringing.append(item)
            self.boat.carrying = []
        elif phase == "returning":
            for pid in self.boat.people:
                p = world.people.find(pid)
                if p is not None:
                    p.where = "boat"
            lines.append(
                (
                    Severity.ROUTINE,
                    "boat.returning",
                    f"{head} shoved off from the quay.",
                    {"port": port.id},
                )
            )
        elif phase == "alongside":
            lines.extend(self._boat_back(port))
        return lines

    def _boat_back(self, port: Port) -> list[tuple[Severity, str, str, dict[str, Any]]]:
        world = self.world
        name = self.boat.boat_name
        head = f"{name[:1].upper()}{name[1:]}"
        lines: list[tuple[Severity, str, str, dict[str, Any]]] = [
            (
                Severity.NOTABLE,
                "boat.alongside",
                f"{head} alongside from the shore and hoisted in.",
                {"port": port.id, "errand": self.boat.errand},
            )
        ]
        for pid in self.boat.people:
            p = world.people.find(pid)
            if p is not None:
                p.aboard = True
                p.where = "deck"
                lines.append(
                    (
                        Severity.ROUTINE,
                        "person.came",
                        f"{p.name} came aboard from the boat.",
                        p.to_dict(),
                    )
                )
        for item in self.boat.bringing:
            kind = item.get("kind")
            if kind == "prices":
                listed = self._write_price_list(port)
                said = ", ".join(f"{g} {pounds_words(p)}" for g, p in listed[:4])
                papers = getattr(world, "papers", None)
                keeper = "purser"
                if papers is not None:
                    try:
                        keeper = papers.page("the price list").keeper
                    except KeyError:
                        pass
                lines.append(
                    (
                        Severity.ROUTINE,
                        "market.prices",
                        f"The {keeper}'s list of the prices at {port.name} is aboard: {said} a "
                        f"ton, and the rest.",
                        {"port": port.id, "prices": dict(listed)},
                    )
                )
                # the rumours of the quay (package 43b; the owner's note 24), where the
                # world's business is on
                business = getattr(world, "business", None)
                rumour = business.rumour(port) if business is not None else ""
                if rumour:
                    lines.append((Severity.ROUTINE, "port.rumour", rumour, {"port": port.id}))
            elif kind == "letter":
                message = Message(
                    str(item["text"]),
                    str(item.get("origin") or port.name),
                    str(item.get("to") or "captain"),
                    name,
                )
                lines.extend(world.people.message_aboard(message))
            elif kind == "purchase":
                good, tons = str(item["good"]), float(item["tons"])
                try:
                    world.hold.stow(good, tons)
                    lines.append(
                        (
                            Severity.NOTABLE,
                            "market.bought",
                            f"{tons:g} tons of {good} hoisted in and struck down into the "
                            f"hold; the manifest {world.hold.words()}.",
                            {"port": port.id, "good": good, "tons": tons},
                        )
                    )
                except ValueError as e:
                    lines.append(
                        (
                            Severity.NOTABLE,
                            "market.bought",
                            f"{tons:g} tons of {good} came off, but {e}; it lies on deck.",
                            {"port": port.id, "good": good, "tons": tons},
                        )
                    )
        self.boat = BoatState(boat_name=name, boat_id=self.boat.boat_id)
        return lines

    # -- the boat between hulls (package 82; the design's §2) ------------------------------

    def send_boat_to(
        self,
        target: Any,
        carrying: list[Any],
        fetching: list[Any],
        by_the_director: bool = False,
    ) -> tuple[str, dict[str, Any]]:
        """`send the boat to the <ship> [with <persons>] [for <persons>]`: the boat away
        to another hull lying within a boat's pull (`movement.BOAT_BETWEEN_NM`), the
        persons she carries put aboard her when she is alongside and the persons she is
        sent for stepping into her there, back alongside and hoisted in; two jobs of the
        port's kind at the boat's pace (`Job(kind="boat_to")`), on an awake hull as on a
        sleeping one, since a boat's pull between two ships wants no hands' evolution to
        show. Refused in words with no boat, the boat away, the other hull beyond the
        reach, or nobody to carry or fetch."""
        from freesail.orders.errors import OrderError
        from freesail.world.movement import BOAT_BETWEEN_NM, hull_name

        world = self.world
        boat = self.boat_spec()
        if boat is None:
            raise OrderError("She carries no boat: the ship's file lists none.")
        if self.boat.away:
            raise OrderError(f"{boat.name[:1].upper()}{boat.name[1:]} is away already.")
        if target is None or getattr(target, "position", None) is None or world.position is None:
            raise OrderError("The other ship is not on this sea within a boat's pull.")
        her = hull_name(target)
        if str(getattr(target, "id", "")) == str(self.hull_id):
            raise OrderError("The boat is sent to another ship, not to her own.")
        metres = bearing_and_distance(world.position, target.position)[1]
        nm = metres / units.NAUTICAL_MILE
        if nm > BOAT_BETWEEN_NM and not by_the_director:
            # the director's word carries the doubt (`orders.doubt`) and performs: the
            # boat's pull takes the time the distance gives
            raise OrderError(
                f"The {her} is {distance_words(metres)} off, beyond a boat's pull "
                f"({BOAT_BETWEEN_NM:g} mile); close her first."
            )
        if not carrying and not fetching:
            raise OrderError(
                f"Send the boat to the {her} with whom, or for whom? Say 'send the boat to the "
                f"{her} with Mr Pope', or '... for Mr Pope'."
            )
        for person in carrying:
            if not person.aboard or str(person.hull) != str(self.hull_id):
                raise OrderError(f"{person.name} is {world.people.state_words(person)}.")
            if person.occupied:
                raise OrderError(f"{person.name} is at the {person.task}.")
        for person in fetching:
            if str(getattr(person, "hull", "") or "") != str(target.id):
                raise OrderError(f"{person.name} is not aboard the {her}.")
        now = int(world.clock.tick)
        pull_s = int(metres / units.knots_to_ms(BOAT_PACE_KN))
        alongside_at = now + BOAT_HOIST_OUT_S + pull_s
        back_at = alongside_at + 300 + pull_s + BOAT_HOIST_IN_S  # five minutes alongside her
        for person in carrying:
            person.hull = None
            person.where = "boat"
        self.boat = BoatState(
            away=True,
            boat_id=boat.id,
            boat_name=boat.name,
            errand="to_ship",
            port_id="",
            phase=f"pulling for the {her}",
            since_tick=now,
            people=[p.id for p in carrying],
            landing=tuple(p.id for p in carrying),
            fetching=tuple(p.id for p in fetching),
            to_hull=str(target.id),
            to_name=her,
        )
        self.jobs.append(
            Job(
                alongside_at,
                "boat_to",
                "",
                {"stage": "alongside", "hull": str(target.id)},
                hull=self.hull_id,
            )
        )
        self.jobs.append(
            Job(
                back_at, "boat_to", "", {"stage": "back", "hull": str(target.id)}, hull=self.hull_id
            )
        )
        head = f"{boat.name[:1].upper()}{boat.name[1:]}"
        who = ""
        if carrying:
            who = f" with {_and([p.name for p in carrying])}"
        for_whom = f", for {_and([p.name for p in fetching])}" if fetching else ""
        minutes = max(1, round((back_at - now) / 60))
        text = (
            f"{head} away for the {her}{who}{for_whom}; alongside her in some "
            f"{max(1, round((alongside_at - now) / 60))} minutes, back in some {minutes}."
        )
        self._record(
            Severity.NOTABLE,
            "boat.away",
            text,
            {"ship": str(target.id), "errand": "to_ship", "people": [p.id for p in carrying]},
        )
        return text, {"to": str(target.id), "back_at": back_at}

    def _boat_to_job(self, job: Job) -> None:
        """The boat's two stages at another hull (`send_boat_to`): alongside her, the
        persons carried put aboard her (`movement.put_aboard`, their stations following)
        and the persons fetched stepping into the boat; back, the boat alongside her own
        ship and hoisted in, whoever is in her aboard again."""
        from freesail.world.movement import hull_name, hull_of, put_aboard

        world = self.world
        registry = getattr(world, "registry", None)
        if not self.boat.away or self.boat.errand != "to_ship":
            return
        target = hull_of(world, job.payload.get("hull"))
        name = self.boat.boat_name
        head = f"{name[:1].upper()}{name[1:]}"
        persons = {p.id: p for p in (registry.persons() if registry is not None else [])}
        stage = job.payload.get("stage")
        if stage == "alongside":
            if target is None:
                self._record(
                    Severity.NOTABLE,
                    "boat.returning",
                    f"{head} found no ship where the {self.boat.to_name} lay; she pulls back.",
                    {"ship": str(job.payload.get("hull") or "")},
                )
                self.boat.phase = "pulling back to the ship"
                return
            her = hull_name(target)
            self.boat.phase = f"alongside the {her}"
            self._record(
                Severity.ROUTINE,
                "boat.ashore",
                f"{head} alongside the {her}.",
                {"ship": str(target.id)},
            )
            for pid in self.boat.landing:
                p = persons.get(pid)
                if p is None:
                    continue
                self.boat.people = [x for x in self.boat.people if x != pid]
                put_aboard(world, p, target, "quarterdeck", by=f"the {hull_name(world.own)}'s boat")
            self.boat.landing = ()
            for pid in self.boat.fetching:
                p = persons.get(pid)
                if p is None or str(getattr(p, "hull", "") or "") != str(target.id):
                    continue
                p.hull = None
                p.where = "boat"
                p.port = None
                self.boat.people = [*self.boat.people, pid]
                target.record(
                    Severity.ROUTINE,
                    "person.moved",
                    f"{p.name} went down into the {hull_name(world.own)}'s boat.",
                    data={"person": p.to_dict(), "ship": str(self.hull_id)},
                )
            self.boat.fetching = ()
            self.boat.phase = "pulling back to the ship"
            return
        if stage == "back":
            lines: list[tuple[Severity, str, str, dict[str, Any]]] = [
                (
                    Severity.NOTABLE,
                    "boat.alongside",
                    f"{head} alongside from the {self.boat.to_name or 'other ship'} and "
                    "hoisted in.",
                    {"ship": str(self.boat.to_hull), "errand": "to_ship"},
                )
            ]
            own = world.own
            for pid in list(self.boat.people):
                p = persons.get(pid)
                if p is None:
                    continue
                put_aboard(world, p, own, "deck", by="the boat", said=False)
                lines.append(
                    (
                        Severity.ROUTINE,
                        "person.came",
                        f"{p.name} came aboard from the boat.",
                        p.to_dict(),
                    )
                )
            self.boat = BoatState(boat_name=name, boat_id=self.boat.boat_id)
            for severity, kind, text, data in lines:
                self._record(severity, kind, text, data)

    def boat_reading(self) -> dict[str, Any]:
        boat = self.boat_spec()
        if boat is None:
            return {"words": "no boat: the ship's file lists none", "away": False}
        if not self.boat.away:
            self.boat.boat_name = boat.name
        return {
            "words": self.boat.words(),
            "away": self.boat.away,
            "errand": self.boat.errand,
            "phase": self.boat.phase,
            "boat": boat.id,
        }

    def boats_words(self) -> str:
        boats = getattr(getattr(self.world.ship, "spec", None), "boats", None) or []
        if not boats:
            return "she carries no boats"
        return ", ".join(
            f"{b.name} ({b.length_ft:g} ft, {b.oars} oars, {b.crew} hands)" for b in boats
        )

    # -- people in places (package 53; spec M7b §14) ---------------------------------------

    def land_person(self, person: Any) -> tuple[str, str, dict[str, Any]]:
        """`go ashore`: the boat away to the quay of the port she lies in with him, who
        stays there when she comes back (`BoatState.landing`); refused in words when she
        is not in port, the port is hostile or the boat is away."""
        from freesail.orders.errors import OrderError

        port = self.in_port()
        if port is None:
            found = self.nearest(IN_PORT_NM * 2.5)
            if found is not None and not self.anchored:
                raise OrderError(
                    f"She is under way; bring her to an anchor in "
                    f"{_possessive(found[0].name)} roads before you go ashore."
                )
            raise OrderError("She is not in port; there is no shore within a boat's pull.")
        if self.stance(port) == "hostile":
            raise OrderError(f"{port.name} is hostile to her; a boat sent in would be taken.")
        if person.occupied:
            raise OrderError(f"You are at the {person.task}.")
        was_where = person.where
        person.aboard = False
        person.where = "boat"
        try:
            text = self._send_boat(port, "landing", [], [person.id])
        except OrderError:
            person.aboard, person.where = True, was_where
            raise
        self.boat.landing = (person.id,)
        return (
            "evolution.started",
            text,
            {"port": port.id, "errand": "landing", "people": [person.id], "subjects": ["the boat"]},
        )

    def waterman(self, person: Any) -> tuple[str, str, dict[str, Any]]:
        """`hire a waterman` (package 68; the cold review of 2026-10-22, R-62): a shore
        boat from the quay of the port she lies in, whether her own boat is away or not,
        takes the person ashore from the ship, or off to her from the quay where he
        stands, for a shilling a head from the purse; he is in the waterman's boat for the
        pull and lands, or comes aboard, when it is done (a job of the port's, `_apply_job`).
        Refused in words where she lies at no port, the port is hostile, or he is busy."""
        from freesail.orders.errors import OrderError
        from freesail.world.geo import bearing_and_distance

        world = self.world
        port = self.in_port()
        if port is None:
            raise OrderError(
                "She lies at no port: there is no waterman to hire, only her own boat at a "
                "port's reach."
            )
        if self.stance(port) == "hostile":
            raise OrderError(f"{port.name} is hostile to her; no waterman will come off.")
        if person.occupied:
            raise OrderError(f"You are at the {person.task}.")
        if person.aboard:
            to = "shore"
        elif person.where == "shore" and person.port == port.id:
            to = "ship"
        else:
            raise OrderError(
                f"You are {world.people.state_words(person)}; a waterman takes a person "
                "between the ship and the quay of the port she lies at."
            )
        purse = getattr(world, "purse", None)
        now = world.clock.tick
        if purse is not None:
            try:
                purse.pay(WATERMAN_FARE_POUNDS, f"a waterman's fare, {port.name}", now)
            except ValueError as e:
                raise OrderError(f"No waterman's fare: {e}.") from None
        here = getattr(world, "position", None)
        metres = bearing_and_distance(here, port.shore.position)[1] if here is not None else 0.0
        pull_s = int(metres / units.knots_to_ms(WATERMAN_KN)) + WATERMAN_TURN_S
        due = now + pull_s
        was = person.where
        person.aboard, person.where = False, "boat"
        if to == "ship":
            person.ashore_at = ""
        self.jobs.append(
            Job(
                due,
                "waterman",
                port.id,
                {"person": person.id, "to": to, "was": was},
                hull=self.hull_id,
            )
        )
        minutes = max(1, round(pull_s / 60))
        if to == "shore":
            text = (
                f"A waterman hired from {port.shore.name}: {person.name} goes down into his "
                f"boat, the fare a shilling; landed in some {minutes} minutes."
            )
        else:
            text = (
                f"A waterman hired at {port.shore.name}: {person.name} goes off to the ship in "
                f"his boat, the fare a shilling; aboard in some {minutes} minutes."
            )
        return (
            "person.waterman",
            text,
            {"port": port.id, "person": person.name, "to": to, "due_tick": due},
        )

    def fetch_person(self, person: Any) -> tuple[str, str, dict[str, Any]]:
        """`come aboard`: the boat sent from the ship lying at his port to take him off the
        quay (`BoatState.fetching`); refused in words when she does not lie there or the
        boat is away."""
        from freesail.orders.errors import OrderError

        port = self.ports.get(person.port or "")
        here = self.in_port()
        if port is None or here is None or here.id != port.id:
            at = port.name if port is not None else "this port"
            raise OrderError(
                f"The ship does not lie at {at}; no boat of hers can take you off. A "
                "letter, or a passage in another, is the way."
            )
        if self.boat.away:
            name = self.boat.boat_name
            raise OrderError(f"{name[:1].upper()}{name[1:]} is away; wait for her at the quay.")
        text = self._send_boat(port, "fetch", [], [])
        self.boat.fetching = (person.id,)
        return (
            "evolution.started",
            f"{person.name} sent off for the boat from {port.shore.name}: {text}",
            {"port": port.id, "errand": "fetch", "people": [person.id], "subjects": ["the boat"]},
        )

    def _land_and_take_off(self, port: Port) -> list[tuple[Severity, str, str, dict[str, Any]]]:
        """At the quay: the people she landed to stay go ashore, and the people waiting to
        come off step into her (package 53); a thing lying in the boat is landed on the
        quay (package 68; the cold review's D8: a thing put in the boat stayed aboard)."""
        world = self.world
        lines: list[tuple[Severity, str, str, dict[str, Any]]] = []
        from freesail.world import things as things_mod

        own = str(getattr(getattr(world, "own", None), "id", "") or "")
        for t in things_mod.things_of(world):
            if t.keeper or t.place != things_mod.IN_THE_BOAT or (t.hull and t.hull != own):
                continue
            t.place, t.port, t.ashore_at, t.spot, t.hull = "shore", port.id, "quay", "", None
            lines.append(
                (
                    Severity.ROUTINE,
                    "thing.landed",
                    f"{t.the[:1].upper()}{t.the[1:]} landed from the boat at {port.shore.name}.",
                    {"thing": t.id, "port": port.id},
                )
            )
        for pid in getattr(self.boat, "landing", ()) or ():
            p = world.people.find(pid)
            if p is None:
                continue
            self.boat.people = [x for x in self.boat.people if x != pid]
            p.aboard, p.where, p.port, p.ashore_at = False, "shore", port.id, "quay"
            lines.append(
                (
                    Severity.NOTABLE,
                    "person.ashore",
                    f"{p.name} landed at {port.shore.name}.",
                    {"person": p.name, "port": port.id},
                )
            )
        self.boat.landing = ()
        for pid in getattr(self.boat, "fetching", ()) or ():
            p = world.people.find(pid)
            if p is None or p.aboard or p.where != "shore" or p.port != port.id:
                continue
            p.where, p.ashore_at = "boat", ""
            self.boat.people = [*self.boat.people, pid]
            lines.append(
                (
                    Severity.ROUTINE,
                    "person.moved",
                    f"{p.name} stepped into the boat at {port.shore.name}.",
                    {"person": p.name, "port": port.id},
                )
            )
        self.boat.fetching = ()
        return lines

    def trade_list(
        self, bargains: list[tuple[str, float, str]], person: Any = None, said: str = ""
    ) -> tuple[str, dict[str, Any]]:
        """Bargains to buy and to sell struck together (package 53; spec M7b §14 and §16):
        `(verb, tons, good words)` each. By the boat from aboard in one errand (a drafted
        manifest given to the boat), or in person at the market by `person` ashore, who
        reads the prices there and whose purchases come off by the port's lighter. Every
        bargain is read and weighed before any is struck (the goods, the room in the hold
        net of what is sold, the purse net of what is taken), so that one that cannot be
        struck refuses the whole and nothing is paid. `said` heads the line ("By the
        manifest 'cargo'")."""
        from freesail.orders.errors import OrderError

        world = self.world
        here = self.in_port()
        if person is not None:
            port = self.ports.get(person.port or "")
            if port is None:
                raise OrderError("You are ashore on the boat's errand; the market is the purser's.")
            if here is None or here.id != port.id:
                raise OrderError(
                    f"The ship does not lie at {port.name}; there is nothing to send the goods "
                    "off to, or to land them from."
                )
        else:
            port = here
            if port is None:
                raise OrderError(
                    "She is not in port; the market is ashore and the boat has nowhere to go."
                )
        if self.stance(port) in ("hostile", "closed"):
            raise OrderError(
                f"{port.name} is {self.stance(port)} to her; there is no trading there."
            )
        if person is None:
            if port.id not in self.price_lists:
                raise OrderError(
                    f"The prices at {port.name} are not known; send the boat ashore first, and "
                    "the purser will bring the list off."
                )
            if self.boat.away:
                raise OrderError(
                    f"{self.boat.boat_name[:1].upper()}{self.boat.boat_name[1:]} is away; wait "
                    "for her."
                )
        hold: Hold = world.hold
        purse: Purse = world.purse
        struck: list[tuple[str, str, float, float, float]] = []  # verb, good, tons, price, sum
        for verb, tons, good_words in bargains:
            good = port.market.find(good_words)
            if good is None:
                names = ", ".join(port.market.goods)
                raise OrderError(
                    f"{_possessive(port.name)} market has no {good_words}; it deals in {names}."
                )
            if tons <= 0:
                raise OrderError(f"How many tons of {good.good}? Say 'buy twenty tons of tin'.")
            price = self.price_of(port, good.good)
            struck.append((verb, good.good, tons, price, price * tons))
        bought = [x for x in struck if x[0] == "buy"]
        sold = [x for x in struck if x[0] == "sell"]
        for _v, good_name, _t, _p, _x in sold:
            have = hold.goods.get(good_name, 0.0)
            wanted = sum(t for _, g, t, _, _ in sold if g == good_name)
            if wanted > have + 1e-9:
                raise OrderError(
                    f"The hold has {have:g} tons of {good_name}, not {wanted:g}; the manifest "
                    "says so."
                )
        room = hold.room_tons + sum(t for _, _, t, _, _ in sold)
        tons_in = sum(t for _, _, t, _, _ in bought)
        if tons_in > room + 1e-9:
            raise OrderError(
                f"There is room in the hold for {room:g} tons and no more; the {tons_in:g} tons "
                "bought will not stow."
            )
        paid = sum(x for _, _, _, _, x in bought)
        taken = sum(x for _, _, _, _, x in sold)
        if paid > purse.pounds + taken + 1e-9:
            raise OrderError(
                f"The goods bought are {pounds_words(paid)}, and the purse holds "
                f"{purse.words()}"
                + (f" with {pounds_words(taken)} from the sales" if taken else "")
                + "."
            )
        now = world.clock.tick
        if person is not None:
            # the prices read at the market, and the list his to bring off
            self._write_price_list(
                port, why=f"the prices at {port.name} read at the market by {person.name}"
            )
        items: list[dict[str, Any]] = []
        for _v, good_name, tons, _p, sum_pounds in sold:
            hold.break_out(good_name, tons)
            purse.take(sum_pounds, f"{tons:g} tons of {good_name} sold at {port.name}", now)
            port.market.sold_to_port(good_name, tons)
            items.append({"kind": "sale", "good": good_name, "tons": tons, "pounds": sum_pounds})
        for _v, good_name, tons, _p, sum_pounds in bought:
            purse.pay(sum_pounds, f"{tons:g} tons of {good_name} at {port.name}", now)
            port.market.bought_from_port(good_name, tons)
            items.append(
                {"kind": "purchase", "good": good_name, "tons": tons, "pounds": sum_pounds}
            )
        parts = []
        if bought:
            parts.append(
                "bought "
                + "; ".join(
                    f"{t:g} tons of {g} at {pounds_words(pr)} a ton" for _, g, t, pr, _ in bought
                )
            )
        if sold:
            parts.append(
                "sold "
                + "; ".join(
                    f"{t:g} tons of {g} at {pounds_words(pr)} a ton" for _, g, t, pr, _ in sold
                )
            )
        money = []
        if paid:
            money.append(f"{pounds_words(paid)} paid")
        if taken:
            money.append(f"{pounds_words(taken)} taken")
        due = None
        if person is not None:
            head = f"{person.name} at the market of {port.name}, in person"
            if bought:
                buys = [i for i in items if i["kind"] == "purchase"]
                pull_s = self.to_shore_m(port) / (BOAT_PACE_KN * units.KNOT)
                due = now + int(BOAT_ASHORE_S["purchase"] + tons_in * LIGHTER_S_PER_TON + pull_s)
                self.jobs.append(Job(due, "lighter", port.id, {"items": buys}, hull=self.hull_id))
                carried = "the lighter brings it off"
            else:
                carried = "the goods landed by the lighter"
        else:
            head = said or f"At {port.name}"
            errand = "purchase" if bought else "sale"
            self._send_boat(port, errand, items)
            carried = "the boat goes for it" if bought else "the boat lands it"
        text = (
            f"{head}: {'; and '.join(parts)}; {', '.join(money) or 'nothing paid'}; "
            f"{carried}. The purse: {purse.words()}."
        )
        papers = getattr(world, "papers", None)
        if papers is not None:
            for verb, good_name, tons, _p, _x in struck:
                line = papers.write(
                    "the manifest",
                    f"{tons:g} tons of {good_name} {'bought' if verb == 'buy' else 'sold'} at "
                    f"{port.name}",
                )
                self._record(Severity.ROUTINE, "paper.written", line, {"paper": "the manifest"})
        data: dict[str, Any] = {
            "port": port.id,
            "bargains": [
                {"verb": v, "good": g, "tons": t, "price_pounds": pr, "sum_pounds": x}
                for v, g, t, pr, x in struck
            ],
            "paid_pounds": paid,
            "taken_pounds": taken,
            "purse_pounds": round(purse.pounds, 2),
            "by": "person" if person is not None else "boat",
        }
        if due is not None:
            data["due_tick"] = due
        return text, data
