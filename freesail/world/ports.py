"""Ports (spec M5 §23; package 35): Falmouth, Plymouth and Brest as places with a
pilot, roads and a mooring, a boat's landing, a market, a yard or the chandlers, a crew
pool and a stance toward each nation, each a file of `data/ports/` on one machinery.

**Arriving** is a sequence the log tells and the readings carry. When a ship is under
way in a port's pilot's cruising ground by day, the pilot cutter (32b's cutter at far
detail, `freesail.world.ships`) comes off from the port's quay and closes her; the
lookout sights her as he sights anything ("Sail ho!", a bearing first, her rig as she
nears); within hail she hails for a pilot, and within two cables, the ship under easy
sail, the pilot comes aboard as a person (`freesail.world.people`) with his skill, his
words (the channel, the marks, the anchorage, when the tide serves: his tide is the
port's own, which he knows as a man who lives by it, the one way the world's tide
reaches the captain, through a person; decision 30) and the port's news; the cutter
lies to under the lee and goes back. A port **closed** to the ship's nation refuses her
in the pilot's words from the cutter (truth 70); a **hostile** port sends no pilot. Then
the anchorage, the boat and the shore. **Leaving** is the reverse: `get under way` as
Luce has it (`freesail.evolutions.scripts.GetUnderWayScript`), the pilot's course out,
and the pilot off into his cutter beyond the outer road, his certificate signed and the
pilotage paid from the purse (the Regulations of 1806, the Pilot's articles).

**The boat** (`send the boat ashore`, `data/evolutions/send_boat.yaml`) is a passage by
distance at a boat's pace with hands and time, hoisted out and in, carrying a person, a
message or a purchase; what it brings back comes aboard at the gangway and reaches the
captain where he is through the messenger and the door (truth 68). **The market** is a
list of goods with a price each that moves by a small rules table (`Market.price`:
the season by the month, the war by the nations table, the supply by what has been sold
to the port and bought from it); `buy <n> tons of <good>` and `sell` go by the boat and
move the hold (from the ship file through the generator) and the purse; `the prices` are
known once the boat has been ashore and the purser has brought the list off (a paper,
`freesail.world.places.Papers`). **The dockyard** supplies a spar, a suit of sails,
cordage, water and provisions with a time and a cost against the ship's stores (the
frigate's from the King's yard by demand and survey, the schooner's from the chandlers
at a price). **The crew pool** gives hands by rating at a bounty and a delay, mustered
into the crew of milestone 3 with names from the muster's own lists.

Every constant below names its source or says judgement; the prices in the port files
are from memory and the files say so. Everything here is a function of the seed and
the journal: the pilot's name is drawn from the `people` stream, the recruits' from
`recruits`; a replay has them again, and a checkpoint holds the whole.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import yaml

from freesail import units
from freesail.core.events import Severity
from freesail.world.geo import Position, bearing_and_distance
from freesail.world.people import Message, Person
from freesail.world.places import Hold, Purse, pounds_words

__all__ = [
    "BOAT_ASHORE_S",
    "BOAT_HOIST_IN_S",
    "BOAT_HOIST_OUT_S",
    "BOAT_PACE_KN",
    "IN_PORT_NM",
    "PILOT_AGAIN_H",
    "PILOT_BOARDS_UNDER_KN",
    "PILOT_BOARDS_WITHIN_M",
    "PILOT_HAIL_WITHIN_M",
    "PILOT_LIES_TO_S",
    "PILOT_OFF_BEYOND_NM",
    "PORTS_DIR",
    "SUPPLY_CAP",
    "SUPPLY_FLOOR",
    "SUPPLY_PER_TON",
    "SUPPLY_RECOVERY_PER_DAY",
    "WAR_FACTOR",
    "BoatState",
    "Dockyard",
    "Good",
    "Job",
    "Market",
    "PilotSpec",
    "Port",
    "Ports",
    "Spot",
    "load_port",
    "port_files",
]

PORTS_DIR = Path(__file__).resolve().parents[2] / "data" / "ports"

# -- the pilot and his cutter (judgement throughout; no page times a pilot's boarding) --
# The cutter runs alongside within two cables and the pilot boards from her boat.
PILOT_BOARDS_WITHIN_M = 2.0 * units.CABLE
# He boards with the ship under easy sail: over this speed over the ground the cutter
# hails her to shorten sail and keeps company (judgement: a pilot's boat alongside a
# frigate at eight knots is a drowned pilot).
PILOT_BOARDS_UNDER_KN = 6.0
# Within four cables the cutter hails.
PILOT_HAIL_WITHIN_M = 4.0 * units.CABLE
# The cutter comes off to a ship with way on her, a knot through the water or more (a
# ship drifting under bare poles is not making for the port).
PILOT_COMES_OFF_OVER_KN = 1.0
# A port whose pilot refused her, or left her, is not tried again for six hours.
PILOT_AGAIN_H = 6.0
# The cutter lies to under the lee ten minutes after the boarding, then goes back.
PILOT_LIES_TO_S = 600
# Outward bound the pilot leaves her a mile beyond the outer road (the Regulations: the
# captain's certificate names the port or channel he conducted her out of).
PILOT_OFF_BEYOND_NM = 1.0
# At anchor within two miles of the port's roads or mooring she is in port: the boat
# goes ashore, the market and the yard serve her.
IN_PORT_NM = 2.0
# -- the boat (judgement) --
# A boat's crew pull four knots on an errand (no page times a boat's crew; a man-of-war's
# cutter double-banked did better for a spurt and worse over an hour).
BOAT_PACE_KN = 4.0
# Hoisting a boat out with the yard and stay tackles, and in again (Luce 1866, 'Boats',
# 'Hoisting out boats' gives the sequence; the time is judgement).
BOAT_HOIST_OUT_S = 300
BOAT_HOIST_IN_S = 300
# The business ashore by errand, seconds: a letter left or fetched, the purser's turn
# round the market for the prices, a passenger landed, a purchase weighed and carted to
# the quay, a draft of recruits brought down (judgement).
BOAT_ASHORE_S = {
    "message": 1800,
    "prices": 1800,
    "person": 900,
    "purchase": 3600,
    "sale": 3600,
    "yard": 1800,
    "recruits": 1800,
}
# Goods bought or sold go between the quay and the ship by the port's lighter, not by
# the boat's trips: three minutes a ton (twenty tons an hour, judgement; the boat itself
# carries under a ton), added to the boat's time ashore.
LIGHTER_S_PER_TON = 180
# -- the market's rules table (judgement; docs/dev/TuningNotes.md, package 35) --
# supply: each ton sold to the port lowers its price by this fraction, each ton bought
# from it raises it the same, between a floor and a cap; the glut or the want clears by
# a seventh a day (a week).
SUPPLY_PER_TON = 0.01
SUPPLY_RECOVERY_PER_DAY = 1.0 / 7.0
SUPPLY_FLOOR = 0.5
SUPPLY_CAP = 2.0
# war: a good whose origin is a nation the port's own is at war with is dearer by half
# (the smuggler's premium on French brandy in Cornwall; judgement in the figure).
WAR_FACTOR = 1.5
# Prices are given to the half pound, as a clerk's list.
PRICE_ROUND = 0.5
# The recruits come off by the boat in a draft once the delay is up.
RECRUIT_RATINGS = ("able", "ordinary", "landsman")


# ---------------------------------------------------------------------------
# The port as data
# ---------------------------------------------------------------------------


@dataclass
class Spot:
    """A place of the port on the chart: the roads, the mooring, the quay."""

    name: str
    position: Position
    depth_m: float | None = None
    bottom: str = ""
    feature_id: str = ""
    deep_draught_ft: float | None = None  # a ship drawing more goes to the anchorage instead

    @property
    def depth_words(self) -> str:
        from freesail.world.chart import fathoms_words

        return "no depth given" if self.depth_m is None else fathoms_words(self.depth_m)


@dataclass
class PilotSpec:
    station: str
    cruising_nm: float
    by_night: bool
    cutter_file: str
    names: tuple[str, ...]
    skill: float
    fee_pounds: float
    cast: str
    course_out_deg: float
    words: dict[str, str]


@dataclass
class Good:
    good: str
    price: float
    origin: str | None
    season: dict[int, float]
    note: str = ""


@dataclass
class Market:
    """The port's goods and the rules that move their prices."""

    currency: str
    goods: dict[str, Good]
    net_sold: dict[str, float] = field(default_factory=dict)  # tons sold to the port, less bought
    settled_tick: int = 0  # when the supply last recovered a day's worth

    def recover(self, tick: int) -> None:
        """The glut or the want clears by `SUPPLY_RECOVERY_PER_DAY` each day."""
        days = (tick - self.settled_tick) / 86400.0
        if days < 1.0:
            return
        whole = int(days)
        self.settled_tick += whole * 86400
        keep = (1.0 - SUPPLY_RECOVERY_PER_DAY) ** whole
        self.net_sold = {g: t * keep for g, t in self.net_sold.items() if abs(t * keep) > 0.01}

    def factors(
        self, good: Good, when: datetime, nations: Any, port_nation: str
    ) -> dict[str, float]:
        season = float(good.season.get(when.month, 1.0))
        war = (
            WAR_FACTOR
            if good.origin and nations is not None and nations.at_war(good.origin, port_nation)
            else 1.0
        )
        supply = 1.0 - SUPPLY_PER_TON * self.net_sold.get(good.good, 0.0)
        supply = min(SUPPLY_CAP, max(SUPPLY_FLOOR, supply))
        return {"season": season, "war": war, "supply": supply}

    def price(self, name: str, when: datetime, nations: Any, port_nation: str) -> float:
        good = self.goods[name]
        f = self.factors(good, when, nations, port_nation)
        raw = good.price * f["season"] * f["war"] * f["supply"]
        return max(PRICE_ROUND, round(raw / PRICE_ROUND) * PRICE_ROUND)

    def listing(self, when: datetime, nations: Any, port_nation: str) -> list[tuple[str, float]]:
        return [(name, self.price(name, when, nations, port_nation)) for name in self.goods]

    def find(self, words: str) -> Good | None:
        key = " ".join(str(words).lower().replace("-", " ").split())
        for name, good in self.goods.items():
            if key in (name, name + "s", name.rstrip("s")):
                return good
        return None

    def sold_to_port(self, name: str, tons: float) -> None:
        self.net_sold[name] = self.net_sold.get(name, 0.0) + float(tons)

    def bought_from_port(self, name: str, tons: float) -> None:
        self.net_sold[name] = self.net_sold.get(name, 0.0) - float(tons)


@dataclass
class YardItem:
    item: str
    hours: float = 0.0
    pounds: float = 0.0
    pounds_per_100m2: float = 0.0
    pounds_per_fathom: float = 0.0
    hours_per_ton: float = 0.0
    pounds_per_ton: float = 0.0
    hours_per_day: float = 0.0
    pounds_per_man_day: float = 0.0
    note: str = ""


@dataclass
class Dockyard:
    kind: str  # "yard" (the King's, by demand) or "chandlers" (at a price)
    items: dict[str, YardItem]

    def find(self, words: str) -> YardItem | None:
        key = " ".join(str(words).lower().replace("-", " ").replace("_", " ").split())
        for name, item in self.items.items():
            if key in (name.replace("_", " "), name, "a " + name.replace("_", " ")):
                return item
        if key in ("spar", "a spar", "topmast", "a topmast"):
            return self.items.get("topmast")
        if key in ("sails", "sail", "a suit of sails", "suit of sails", "canvas"):
            return self.items.get("suit of sails")
        if key in ("rope", "cordage", "hemp"):
            return self.items.get("cordage")
        return None


@dataclass
class Port:
    id: str
    name: str
    nation: str
    source: str
    outer_road: Spot
    anchorage: Spot
    mooring: Spot
    shore: Spot
    pilot: PilotSpec
    tide: dict[str, Any]
    market: Market
    dockyard: Dockyard
    crew_pool: dict[str, dict[str, float]]
    closed_to: list[str] = field(default_factory=list)
    letters: list[Message] = field(default_factory=list)  # waiting at the port for the ship
    news: list[str] = field(default_factory=list)  # what the pilot tells, beside the wars
    path: str = ""

    def spots(self) -> list[Spot]:
        return [self.outer_road, self.anchorage, self.mooring]

    def mooring_for(self, draught_m: float) -> Spot:
        """Where she moors: the inner harbour, or the anchorage when she draws too much."""
        deep = self.mooring.deep_draught_ft
        if deep is not None and units.m_to_feet(draught_m) > deep:
            return self.anchorage
        return self.mooring

    def nearest_spot(self, pos: Position) -> tuple[Spot, float]:
        best = None
        for spot in self.spots():
            _, d = bearing_and_distance(pos, spot.position)
            if best is None or d < best[1]:
                best = (spot, d)
        assert best is not None
        return best[0], best[1] / units.NAUTICAL_MILE


def port_files(root: Path = PORTS_DIR) -> dict[str, Path]:
    return {p.stem: p for p in sorted(root.glob("*.yaml"))}


def load_port(path: str | Path, chart: Any = None, state: dict[str, Any] | None = None) -> Port:
    """A port from its file, its spots placed from the chart's features where the file
    names one (`feature:`), else from its own latitude and longitude; `state` is the
    scenario's for this port (closures, letters waiting, news)."""
    p = Path(path)
    doc = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    where = str(p)

    def spot(key: str) -> Spot:
        raw = doc.get(key) or {}
        if not isinstance(raw, dict):
            raise ValueError(f"{where}: '{key}' is not a mapping")
        fid = str(raw.get("feature") or "")
        feature = chart.feature(fid) if chart is not None and fid else None
        if feature is not None:
            pos = feature.position
            depth = (
                units.fathoms_to_m(float(feature.depth_fathoms))
                if feature.depth_fathoms is not None
                else None
            )
            bottom = feature.bottom
        else:
            if raw.get("lat_deg") is None or raw.get("lon_deg") is None:
                if fid:
                    raise ValueError(
                        f"{where}: '{key}' names the feature '{fid}', which the chart has not, "
                        "and gives no lat_deg and lon_deg"
                    )
                raise ValueError(f"{where}: '{key}' gives no feature and no lat_deg and lon_deg")
            pos = Position(float(raw["lat_deg"]), float(raw["lon_deg"]))
            depth = None
            bottom = ""
        if raw.get("depth_fathoms") is not None:
            depth = units.fathoms_to_m(float(raw["depth_fathoms"]))
        if raw.get("bottom"):
            bottom = str(raw["bottom"])
        name = str(raw.get("name") or (feature.name if feature is not None else key))
        deep = raw.get("deep_draught_ft")
        return Spot(name, pos, depth, bottom, fid, None if deep is None else float(deep))

    pr = doc.get("pilot") or {}
    pilot = PilotSpec(
        station=str(pr.get("station") or ""),
        cruising_nm=float(pr.get("cruising_nm", 6.0)),
        by_night=bool(pr.get("comes_off_by_night", False)),
        cutter_file=str(pr.get("cutter") or "data/ships/cutter.yaml"),
        names=tuple(str(n) for n in (pr.get("names") or ["the pilot"])),
        skill=float(pr.get("skill", 0.9)),
        fee_pounds=float(pr.get("fee_pounds", 0.0)),
        cast=str(pr.get("cast") or "starboard"),
        course_out_deg=float(pr.get("course_out_deg", 180.0)),
        words={str(k): str(v) for k, v in (pr.get("words") or {}).items()},
    )
    mk = doc.get("market") or {}
    goods: dict[str, Good] = {}
    for g in mk.get("goods") or []:
        season = {int(k): float(v) for k, v in (g.get("season") or {}).items()}
        goods[str(g["good"])] = Good(
            str(g["good"]), float(g["price"]), g.get("origin"), season, str(g.get("note", ""))
        )
    market = Market(str(mk.get("currency") or "pounds"), goods)
    dy = doc.get("dockyard") or {}
    items = {}
    for it in dy.get("items") or []:
        name = str(it["item"])
        items[name] = YardItem(
            item=name,
            hours=float(it.get("hours", 0.0)),
            pounds=float(it.get("pounds", 0.0)),
            pounds_per_100m2=float(it.get("pounds_per_100m2", 0.0)),
            pounds_per_fathom=float(it.get("pounds_per_fathom", 0.0)),
            hours_per_ton=float(it.get("hours_per_ton", 0.0)),
            pounds_per_ton=float(it.get("pounds_per_ton", 0.0)),
            hours_per_day=float(it.get("hours_per_day", 0.0)),
            pounds_per_man_day=float(it.get("pounds_per_man_day", 0.0)),
            note=str(it.get("note", "")),
        )
    dockyard = Dockyard(str(dy.get("kind") or "chandlers"), items)
    pool = {
        str(k): {kk: float(vv) for kk, vv in (v or {}).items()}
        for k, v in (doc.get("crew_pool") or {}).items()
    }
    state = state or {}
    closed = [str(x) for x in (doc.get("closed_to") or [])]
    closed += [str(x) for x in (state.get("closed_to") or []) if str(x) not in closed]
    letters = []
    for letter in state.get("letters") or []:
        if isinstance(letter, str):
            letters.append(Message(letter, str(doc.get("name") or p.stem)))
        else:
            letters.append(
                Message(
                    str(letter.get("text") or ""),
                    str(letter.get("origin") or doc.get("name") or p.stem),
                    str(letter.get("to") or "captain"),
                )
            )
    return Port(
        id=str(doc.get("id") or p.stem),
        name=str(doc.get("name") or p.stem),
        nation=str(doc.get("nation") or ""),
        source=str(doc.get("source") or ""),
        outer_road=spot("outer_road"),
        anchorage=spot("anchorage"),
        mooring=spot("mooring"),
        shore=spot("shore"),
        pilot=pilot,
        tide=dict(doc.get("tide") or {}),
        market=market,
        dockyard=dockyard,
        crew_pool=pool,
        closed_to=closed,
        letters=letters,
        news=[str(x) for x in (state.get("news") or [])],
        path=where,
    )


# ---------------------------------------------------------------------------
# The ports of one World
# ---------------------------------------------------------------------------


@dataclass
class BoatState:
    """The ship's boat on an errand, as data (a checkpoint holds it)."""

    away: bool = False
    boat_id: str = ""
    boat_name: str = "the boat"
    errand: str = ""
    port_id: str = ""
    carrying: list[dict[str, Any]] = field(default_factory=list)  # what goes ashore
    bringing: list[dict[str, Any]] = field(default_factory=list)  # what comes back
    phase: str = ""
    since_tick: int = 0
    people: list[str] = field(default_factory=list)  # person ids in the boat

    def words(self) -> str:
        if not self.away:
            return f"{self.boat_name} at the booms"
        return f"{self.boat_name} away {_errand_words(self.errand)}, {self.phase}"


@dataclass
class Job:
    """Something the port does for the ship in its own time: the yard's spar, the
    recruits' draft. Data only, applied by kind when due (`Ports._apply_job`)."""

    due_tick: int
    kind: str
    port_id: str
    payload: dict[str, Any] = field(default_factory=dict)
    words: str = ""


class Ports:
    """The ports of one World: loaded by the scenario's `ports:` (every file of
    `data/ports/` when the world has a chart and the scenario says nothing), the pilot's
    coming and going, the boat's errands, the market, the yard and the crew pool."""

    def __init__(self, world: Any) -> None:
        self.world = world
        self.ports: dict[str, Port] = {}
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
        self._load()

    # -- loading -----------------------------------------------------------------------

    def _load(self) -> None:
        world = self.world
        wanted = getattr(world.scenario, "ports", None)
        files = port_files()
        states: dict[str, dict[str, Any]] = {}
        if wanted is None:
            ids = list(files) if world.chart is not None else []
        elif isinstance(wanted, dict):
            ids = list(wanted)
            states = {str(k): dict(v or {}) for k, v in wanted.items()}
        else:
            ids = [str(x) for x in wanted]
        for pid in ids:
            path = files.get(pid)
            if path is None:
                raise ValueError(
                    f"no port file for '{pid}' in {PORTS_DIR} (the ports are {', '.join(files)})"
                )
            self.ports[pid] = load_port(path, world.chart, states.get(pid))
        # the price lists the ship starts with (the scenario's `papers: price_lists`)
        papers = getattr(world.scenario, "papers", None) or {}
        for pid in papers.get("price_lists") or []:
            if pid in self.ports:
                self._write_price_list(self.ports[pid], at_start=True)

    # -- the ship against the ports ----------------------------------------------------

    @property
    def ship_nation(self) -> str:
        nation = getattr(self.world.scenario, "nation", None)
        if nation:
            return str(nation)
        spec = getattr(getattr(self.world.ship, "spec", None), "crew", None)
        names = getattr(spec, "names", "english") if spec is not None else "english"
        return self.world.nations.nation_of_names(names)

    def stance(self, port: Port) -> str:
        return self.world.nations.stance(port.nation, self.ship_nation, port.closed_to)

    def nearest(self, within_nm: float | None = None) -> tuple[Port, float] | None:
        """The nearest port by its roads, and the miles to them."""
        pos = self.world.position
        if pos is None or not self.ports:
            return None
        best = None
        for port in self.ports.values():
            _, d = port.nearest_spot(pos)
            if best is None or d < best[1]:
                best = (port, d)
        if best is None or (within_nm is not None and best[1] > within_nm):
            return None
        return best

    def in_port(self) -> Port | None:
        """The port she lies in: at anchor within `IN_PORT_NM` of its roads or mooring."""
        if not self.world.at_anchor:
            return None
        found = self.nearest(IN_PORT_NM)
        return found[0] if found else None

    def find(self, words: str) -> Port | None:
        key = " ".join(str(words).lower().split()).removeprefix("the ")
        for port in self.ports.values():
            if key in (port.id, port.name.lower()):
                return port
        return None

    def to_shore_m(self, port: Port) -> float:
        pos = self.world.position
        return bearing_and_distance(pos, port.shore.position)[1] if pos is not None else 0.0

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
        if world.clock.ship_time.second == 0 and self.ports and world.position is not None:
            self._tick_pilot(now)

    def _record(
        self, severity: Severity, kind: str, text: str, data: dict[str, Any] | None = None
    ) -> None:
        self.world.record(severity, kind, text, data=data or {})

    # -- the pilot -------------------------------------------------------------------------

    def _cutter(self) -> Any:
        return self.world.vessels.get(self.cutter_id) if self.cutter_id else None

    def _launch_cutter(self, port: Port, errand: str) -> None:
        from freesail.world.ships import Vessel

        self._counter += 1
        vessel = Vessel(
            id=f"{port.id}-pilot-cutter-{self._counter}",
            name=f"the {port.name} pilot's cutter",
            kind="a cutter",
            ship_file=port.pilot.cutter_file,
            nation=port.nation,
            position=port.shore.position,
            purpose="standing out from the land",
            colours=self.world.nations.get(port.nation).colours,
            plan=[("to_ship", PILOT_BOARDS_WITHIN_M)],
        )
        self.world.vessels.add(vessel)
        self.cutter_id = vessel.id
        self.cutter_port = port.id
        self.cutter_errand = errand
        self.cutter_hailed = False

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

    def _tick_pilot(self, now: int) -> None:
        world = self.world
        cutter = self._cutter()
        if cutter is None and self.cutter_id is not None:
            # she is home: the errand is over
            self.cutter_id = self.cutter_port = self.cutter_errand = None
        if self.pilot is None and cutter is None:
            found = self.nearest()
            if found is None:
                return
            port, _ = found
            _, d_anch = bearing_and_distance(world.position, port.anchorage.position)
            if d_anch / units.NAUTICAL_MILE > port.pilot.cruising_nm:
                return
            if (
                world.at_anchor or world.ship.extra.get("aground")
                if hasattr(world.ship, "extra")
                else world.at_anchor
            ):
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
            if dist <= PILOT_HAIL_WITHIN_M and not self.cutter_hailed:
                self.cutter_hailed = True
                if self.cutter_errand == "bring":
                    text = (
                        f"The cutter hailed: a pilot for {port.name}; shorten sail and he will "
                        f"come aboard."
                    )
                else:
                    text = "The cutter hailed: she has come off for the pilot."
                self._record(Severity.ROUTINE, "port.pilot_hail", text, {"port": port.id})
            if dist <= PILOT_BOARDS_WITHIN_M and self._ground_speed_kn() <= PILOT_BOARDS_UNDER_KN:
                cutter.alongside = True
                if self.cutter_errand == "bring":
                    self._pilot_boards(port, cutter, now)
                else:
                    self._pilot_leaves(port, cutter, now)
            return
        if self.pilot is not None and cutter is None and not world.at_anchor:
            port = self.ports[self.pilot_port or ""]
            _, d_road = bearing_and_distance(world.position, port.outer_road.position)
            _, d_anch = bearing_and_distance(world.position, port.anchorage.position)
            d_nm = d_anch / units.NAUTICAL_MILE
            last = self._last_distance_nm.get(port.id)
            self._last_distance_nm[port.id] = d_nm
            road_nm = bearing_and_distance(port.anchorage.position, port.outer_road.position)[1]
            beyond = d_nm > road_nm / units.NAUTICAL_MILE + PILOT_OFF_BEYOND_NM
            if (
                beyond
                and last is not None
                and d_nm > last
                and d_road / units.NAUTICAL_MILE < port.pilot.cruising_nm
            ):
                self._launch_cutter(port, "fetch")

    def _pilot_boards(self, port: Port, cutter: Any, now: int) -> None:
        world = self.world
        stance = self.stance(port)
        nation = world.nations.get(self.ship_nation)
        if stance == "closed":
            text = (
                f"The pilot hailed from the cutter: {port.name} is closed to {nation.people} "
                f"by the port's order; you will get no pilot here, and the batteries will not "
                f"let you pass. The cutter bore up for the land."
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
        self._last_distance_nm.pop(port.id, None)
        head = (
            f"The pilot, {pilot.name} of {port.name}, came aboard from the cutter and took "
            f"charge of her"
        )
        if stance == "neutral":
            head += f" ({nation.adjective} colours being no bar at {port.name})"
        self._record(
            Severity.NOTABLE,
            "port.pilot_aboard",
            head + ".",
            {"port": port.id, "pilot": pilot.to_dict(), "stance": stance},
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
        for letter in list(port.letters):
            letter.carried_by = "the pilot cutter"
            for severity, kind, text, data in world.people.message_aboard(letter):
                self._record(severity, kind, text, data)
            port.letters.remove(letter)
        cutter.plan = [("lie_to", PILOT_LIES_TO_S), ("home", port.shore.position)]
        cutter.alongside = False
        self.cutter_errand = None

    def _pilot_leaves(self, port: Port, cutter: Any, now: int) -> None:
        world = self.world
        pilot = self.pilot
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
        self._record(
            Severity.NOTABLE,
            "port.pilot_left",
            f"{pilot.name} left her in the cutter, clear of {port.outer_road.name}{paid}.",
            {"port": port.id, "pilot": pilot.to_dict(), "fee_pounds": fee},
        )
        self.pilot = None
        self.pilot_port = None
        self.pilot_since = None
        self.declined_until[port.id] = now + int(PILOT_AGAIN_H * 3600)
        cutter.plan = [("home", port.shore.position)]
        cutter.alongside = False
        self.cutter_errand = None

    # -- the pilot's words -----------------------------------------------------------------

    def _tide_words(self, port: Port) -> str:
        """When the tide serves, in the pilot's words: the port's own high water, which
        he knows (the world's tide at the roads, said to the quarter hour)."""
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
        low = hw - timedelta(hours=6, minutes=12)
        enter_on = str(port.tide.get("enter_on", "flood"))
        now = world.clock.ship_time
        when = time_words(hw.hour + hw.minute / 60.0)
        rise = units.m_to_feet(height)
        if enter_on == "flood":
            if low <= now < hw:
                serves = "the flood is making now and serves"
            else:
                serves = (
                    f"the flood will serve from about {time_words(low.hour + low.minute / 60.0)}"
                )
        else:
            serves = f"the ebb will serve from about {when}"
        return f"high water at {port.name} about {when}, {rise:.0f} feet above the datum; {serves}"

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

    def news_words(self, port: Port) -> str:
        parts = list(port.news)
        wars = self.world.nations.wars_words()
        parts.append(wars[:1].upper() + wars[1:] + ".")
        return " ".join(parts)

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

    def port_words(self) -> dict[str, Any] | None:
        """`the port`: the nearest port within the pilot's cruising ground or in which she
        lies, its stance to her, the pilot, the cutter and the boat."""
        found = self.nearest()
        if found is None:
            return None
        port, d_nm = found
        pos = self.world.position
        if d_nm > max(port.pilot.cruising_nm, 10.0):
            return {
                "words": f"no port within the pilot's cruising ground; the nearest is {port.name}, "
                f"{d_nm:.0f} miles off",
                "port": port.id,
                "stance": self.stance(port),
                "distance_nm": round(d_nm, 1),
                "pilot": None,
            }
        stance = self.stance(port)
        spot, d_spot = port.nearest_spot(pos)
        bearing = bearing_and_distance(pos, spot.position)[0]
        if self.in_port() is port:
            where = f"at anchor in {port.name}, {spot.name}"
        else:
            point = units.point_name(math.radians(bearing))
            where = f"{port.name}, {spot.name} bearing {point}, {d_spot:.1f} miles"
        bits = [where, f"the port {stance} to {self.world.nations.get(self.ship_nation).people}"]
        if self.pilot is not None:
            bits.append(f"the pilot {self.pilot.name} aboard")
        cutter = self._cutter()
        if cutter is not None:
            bits.append(
                "the pilot cutter "
                + ("alongside" if cutter.alongside else "standing out toward her")
            )
        bits.append(self.boat.words())
        return {
            "words": "; ".join(bits),
            "port": port.id,
            "stance": stance,
            "distance_nm": round(d_spot, 2),
            "pilot": self.pilot.to_dict() if self.pilot else None,
            "boat_away": self.boat.away,
        }

    def pilot_reading(self) -> dict[str, Any] | None:
        if self.pilot is None or self.pilot_port is None:
            return None
        port = self.ports[self.pilot_port]
        return {
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

    def _write_price_list(self, port: Port, at_start: bool = False) -> list[tuple[str, float]]:
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
                    "the price list", f"the prices at {port.name} brought off by the boat"
                )
                self._record(Severity.ROUTINE, "paper.written", line, {"paper": "the price list"})
        return listed

    def price_of(self, port: Port, good: str) -> float:
        world = self.world
        port.market.recover(world.clock.tick)
        return port.market.price(good, world.clock.ship_time, world.nations, port.nation)

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
            raise OrderError(f"{port.name}'s market has no {good_words}; it deals in {names}.")
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
            Job(due, "yard", port.id, {"item": item.item, "qty": qty, "words": words, "cost": cost})
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
            Job(due, "recruits", port.id, {"n": taken, "rating": rating, "bounty": bounty})
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
        port = self.ports.get(job.port_id)
        if port is None:
            return
        if job.kind == "yard":
            item, qty, words = job.payload["item"], float(job.payload["qty"]), job.payload["words"]
            ship = world.ship
            from freesail.ship.parts import SpareSail, booms, cordage, sail_room

            if item == "water":
                world.stores.water_tons += qty
                done = f"{words} came off from the quay and was started into the ground tier"
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
        return runner.start(world.ship, "send_boat", "her", {"errand": errand, "port": port.id})

    def send_boat(self, words: str) -> tuple[str, dict[str, Any]]:
        """`send the boat ashore [with the purser | with <person> | for the prices | with
        a letter]`: the boat away to the port's quay; what it does there is its errand."""
        from freesail.orders.errors import OrderError

        world = self.world
        port = self.in_port()
        if port is None:
            found = self.nearest(IN_PORT_NM * 2.5)
            if found is not None and not world.at_anchor:
                raise OrderError(
                    f"She is under way; bring her to an anchor in {found[0].name}'s roads "
                    f"before the boat goes ashore."
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
        m_with = _after(low, ("with the ", "with ", "carrying the ", "carrying "))
        if m_with:
            person = world.people.find(m_with)
            if person is not None and person.role not in ("captain",):
                if not person.aboard:
                    raise OrderError(f"{person.name} is {world.people.state_words(person)}.")
                if person.occupied:
                    raise OrderError(f"{person.name} is at the {person.task}.")
                people.append(person.id)
                person.aboard = False
                person.where = "boat"
                errand = "person" if errand == "prices" and person.role != "purser" else errand
        if any(w in low for w in ("water", "provisions", "yard", "recruits", "hands")):
            errand = "yard"
        text = self._send_boat(port, errand, carrying, people)
        return text, {"port": port.id, "errand": errand, "people": people}

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


def _cap(text: str) -> str:
    return text[:1].upper() + text[1:]


def _after(text: str, leads: tuple[str, ...]) -> str:
    for lead in leads:
        i = text.find(lead)
        if i >= 0:
            rest = text[i + len(lead) :].strip()
            for stop in (" for ", " to ", " with "):
                j = rest.find(stop)
                if j > 0:
                    rest = rest[:j]
            return rest.strip(" .")
    return ""


def _errand_words(errand: str) -> str:
    return {
        "prices": "for the prices and what news there is",
        "message": "with a letter",
        "person": "for the prices and what news there is",
        "purchase": "for the goods bought",
        "sale": "with the goods sold",
        "yard": "to the yard",
        "recruits": "for the hands entered",
    }.get(errand, errand)


def _hours_words(hours: float) -> str:
    if hours < 1.0:
        return f"{max(1, round(hours * 60))} minutes"
    if abs(hours - round(hours)) < 0.05:
        n = round(hours)
        return f"{n} hour{'s' if n != 1 else ''}"
    return f"{hours:.1f} hours"


def _and(names: list[str]) -> str:
    if len(names) <= 1:
        return "".join(names)
    return ", ".join(names[:-1]) + " and " + names[-1]
