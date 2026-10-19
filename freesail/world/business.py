"""The world's business (spec M6 §19: "the world generates the business: the small step
now, the loop later"; package 43b).

A scenario that says `business: on` (or a density, `business: 0.5`) has the region it
starts in peopled with ships drawn under the seed, each with an intent and a captain of her
own (package 43's brains, `freesail.world.brains`), on top of whatever ships it names:

- **the trade of the region's ports**: a cargo carried from a port where its price is low to
  one where it is high, by the ports' own market tables as of the day (`Market.price`; the
  ratio at least `price_ratio_least`), under a flag the port of destination will take (her
  own nation's, else a neutral's), in a hull of her nation's trade (`trader_kinds`); some
  lying in the ports at the start, bound away, some coming in at the chart's edges;
- **the fishermen** on the grounds the coast's features give (a `bottom` or a `bank` the
  lead finds at sea, `fishing.depth_fathoms`, off the coast), a smack or a lugger of the
  nearest port that sells fish, on a trip of some hours and home again (the `fish` intent
  and the fisherman's doctrine, `data/captains/fisherman.yaml`), her catch by the grounds'
  tables (`data/fishing/`, `world.fishing`: the same catch at the same rate as the player's,
  sold at her home's fish quay, truth 106), and crewed like any other ship near the player
  since package 56;
- **the cruisers** of the nations at war on the stations the cruiser's doctrine names for
  her nation (`data/captains/cruiser.yaml`, `stations:`) within the region.

Over the day a trader arrives at an edge or sails from a port, and a fisherman puts out,
by a draw once an hour (`arrivals_per_hour`), up to `most_ships`. A ship whose business is
done goes in at her port of destination and is gone from the sea (the brains' own rule), or,
bound beyond the region, leaves it at the edge (`Business.tick` puts her out of the world a
mile beyond it). Nothing of the draw is a line of the player's log: the ships are seen as
the lookout sees any sail, and the record is `Business.drawn`, which the tests and the notes
read. The figures and the names are `data/business.yaml`'s, every one judgement.

**The rumours** (the owner's note 24): the boat sent ashore for the prices brings back two
or three words of prices high or low at the ports the market knows, drawn from those ports'
own tables as of the day, said as rumour (`Business.rumour`, `ports.Ports._boat_back`).

The recorded passages and the trials say `business: off` (the default when a scenario says
nothing), so that they are the ships they name and pin as before; the draw is a function of
the seed and its own stream, `business`, so that it moves no other draw.
"""

from __future__ import annotations

import functools
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from freesail import units
from freesail.world.captains import plain_position
from freesail.world.geo import Position, bearing_and_distance
from freesail.world.ships import land_crossing

__all__ = ["BUSINESS_PATH", "Business", "business_density", "load_business", "port_means_pounds"]

BUSINESS_PATH = Path(__file__).resolve().parents[2] / "data" / "business.yaml"
# The draw's cadence: once an hour of ship's time (judgement: the roll-up's hours).
DRAW_EVERY_S = 3600
# A ship bound beyond the region leaves it this far beyond the edge (judgement: a mile,
# beyond the region's charted water where her far body has nothing more to do).
GONE_BEYOND_NM = 1.0
# A ship drawn at an edge comes in this far inside it (judgement: two miles, at sea).
EDGE_IN_NM = 2.0
# An outward-bound ship's mark lies this far beyond the edge (judgement: past the mile at
# which she is put out of the world, so that she is gone before she reaches it).
BEYOND_NM = 5.0
# The edge points tried for a ship coming in, the farthest first, before the draw gives her up.
EDGE_TRIES = 4
# The routes drawn for a trader before the draw gives her up (judgement).
TRADE_TRIES = 4


@functools.lru_cache(maxsize=2)
def load_business(path: str = str(BUSINESS_PATH)) -> dict[str, Any]:
    """The business's figures and names (`data/business.yaml`), read once."""
    return yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}


def business_density(value: Any) -> float:
    """The scenario's `business:` as a density: off (and nothing said) 0, on 1, a number
    itself; refused in words otherwise."""
    if value is None or value is False:
        return 0.0
    if value is True:
        return 1.0
    words = str(value).strip().lower()
    if words in ("", "off", "no", "none", "false"):
        return 0.0
    if words in ("on", "yes", "true"):
        return 1.0
    try:
        density = float(words)
    except ValueError:
        raise ValueError(
            f"business: '{value}' is no density; say on, off, or a number such as 0.5"
        ) from None
    if density < 0.0:
        raise ValueError(f"business: {density:g} is less than nothing")
    return density


def port_means_pounds(world: Any, port: Any) -> float | None:
    """The most a hand at a port pays in one sum, by the business's figures (package 53b;
    spec M7b §17a, the doubt of a sum beyond a port's means): the largest cargo the
    business carries (`cargo_tons`' upper figure) at the dearest price of the port's market
    as of the day, a whole trader's lading bought outright. None for a port whose market
    deals in nothing, which bounds no sum. Judgement: the business keeps no figure of a
    port's money, and a merchant's sum beyond a full cargo of the port's dearest good is
    beyond what the period's counting house paid across a table."""
    goods = getattr(getattr(port, "market", None), "goods", None) or {}
    if not goods:
        return None
    tons = float((load_business().get("cargo_tons") or [30, 120])[-1])
    prices = []
    for name, good in goods.items():
        try:
            # the price as of the day, read and nothing settled (a doubt changes nothing)
            prices.append(
                float(port.market.price(name, world.clock.ship_time, world.nations, port.nation))
            )
        except Exception:  # noqa: BLE001  (a port read outside its world: the table's price)
            prices.append(float(good.price))
    return max(prices) * tons if prices else None


@dataclass
class Drawn:
    """A ship the business drew: her id, what she is about, where she began, and how her
    business ended (for the record the tests and the notes read)."""

    id: str
    tick: int
    kind: str  # trade, fishing, cruiser
    description: str
    nation: str
    name: str
    intent: str
    where: str
    carries: str = ""
    ended: str = ""
    ended_tick: int | None = None
    landed: str = ""  # a fisherman's catch sold at her home (package 56)

    def to_dict(self) -> dict[str, Any]:
        return {k: v for k, v in self.__dict__.items() if v not in ("", None)}


@dataclass
class Business:
    """The region's business: the draw at the start and once an hour, the ships put out
    of the world beyond the edge, and the rumours of the quay."""

    world: Any
    density: float
    region: str = ""
    bounds: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0)  # south, north, west, east
    drawn: list[Drawn] = field(default_factory=list)
    serial: int = 0
    last_draw: int = 0
    # the routes from port to port whose plans the guard refused, and the ports whose
    # tracks to sea it refuses: not drawn again (the draw's cost is the planning)
    refused: set[tuple[str, str]] = field(default_factory=set)
    _leaves: dict[str, bool] = field(default_factory=dict)

    # -- the stream and the data ---------------------------------------------------------

    @property
    def data(self) -> dict[str, Any]:
        return load_business()

    def _rng(self) -> Any:
        return self.world.rng.stream("business")

    def _n(self, key: str) -> int:
        """A population figure at the density, rounded by the draw."""
        base = float(self.data.get("population", {}).get(key, 0)) * self.density
        whole = int(base)
        return whole + (1 if self._rng().random() < base - whole else 0)

    # -- the region --------------------------------------------------------------------

    def start(self) -> None:
        """The region the player starts in, and the first draw."""
        world = self.world
        chart = getattr(world, "chart", None)
        pos = world.position
        if chart is None or pos is None:
            return
        region = chart.region_at(pos)
        if region is not None:
            self.region = region
            self.bounds = tuple(chart.region_bounds[region])  # type: ignore[assignment]
        else:
            self.bounds = tuple(chart.bounds)  # type: ignore[assignment]
        self.last_draw = world.clock.tick
        for _ in range(self._n("traders_in_port")):
            self._trader(in_port=True)
        for _ in range(self._n("traders_at_sea")):
            self._trader(in_port=False)
        for _ in range(self._n("fishermen")):
            self._fisherman(at_start=True)
        self._cruisers()

    def inside(self, pos: Position, margin_nm: float = 0.0) -> bool:
        s, n, w, e = self.bounds
        dlat = margin_nm / 60.0
        dlon = margin_nm / (60.0 * max(math.cos(math.radians(pos.lat_deg)), 0.2))
        return s - dlat <= pos.lat_deg <= n + dlat and w - dlon <= pos.lon_deg <= e + dlon

    def ports(self) -> list[Any]:
        """The ports of the region with a market, in the order of their ids."""
        ports = getattr(self.world, "ports", None)
        if ports is None or not getattr(ports, "ports", None):
            return []
        return [
            p
            for _pid, p in sorted(ports.ports.items())
            if self.inside(p.outer_road.position) and p.market.goods
        ]

    # -- the tick ------------------------------------------------------------------------

    def tick(self) -> None:
        """Once a minute with the vessels: the ships beyond the edge put out of the world,
        the business's ended in the record, and the draw once an hour."""
        world = self.world
        now = world.clock.tick
        live = {v.id: v for v in world.vessels.vessels}
        for d in self.drawn:
            if d.ended:
                continue
            v = live.get(d.id)
            if v is None or v.done:
                d.ended, d.ended_tick = "gone in at her port", now
                continue
            if not self.inside(v.position, GONE_BEYOND_NM) and self._bound_away(v):
                v.done = True
                d.ended, d.ended_tick = "left at the edge", now
        if now - self.last_draw < DRAW_EVERY_S:
            return
        self.last_draw = now
        rates = self.data.get("arrivals_per_hour", {})
        most = int(self.data.get("most_ships", 16) * max(self.density, 1.0))
        at_sea = sum(1 for d in self.drawn if not d.ended)
        rng = self._rng()
        if at_sea < most and rng.random() < float(rates.get("trader", 0.0)) * self.density:
            self._trader(in_port=rng.random() < 0.5)
        if at_sea < most and rng.random() < float(rates.get("fisherman", 0.0)) * self.density:
            self._fisherman(at_start=False)

    def _bound_away(self, v: Any) -> bool:
        """Whether a ship's business takes her beyond the region: her plan's last mark
        is outside it, or she has none."""
        plan = getattr(v, "plan", None) or []
        marks = [leg[1] for leg in plan if len(leg) > 1 and isinstance(leg[1], Position)]
        return not marks or not self.inside(marks[-1])

    # -- the trade -----------------------------------------------------------------------

    def routes(self) -> list[tuple[float, Any, Any, str]]:
        """The cargoes worth carrying between the region's ports as of today: (the ratio of
        the prices, the port bought in, the port sold in, the good), the best first."""
        world = self.world
        when = world.clock.ship_time
        nations = world.nations
        ports = self.ports()
        least = float(self.data.get("price_ratio_least", 1.3))
        out: list[tuple[float, Any, Any, str]] = []
        for a in ports:
            for b in ports:
                if a is b:
                    continue
                for good in a.market.goods:
                    if good not in b.market.goods:
                        continue
                    pa = a.market.price(good, when, nations, a.nation)
                    pb = b.market.price(good, when, nations, b.nation)
                    if pa > 0 and pb / pa >= least:
                        out.append((round(pb / pa, 3), a, b, good))
        out.sort(key=lambda r: (-r[0], r[1].id, r[2].id, r[3]))
        return out

    def _flag_for(self, a: Any, b: Any) -> str | None:
        """The flag a cargo from port `a` to port `b` sails under: `a`'s nation when `b`
        takes it, else a neutral both take, drawn; None when none will."""
        nations = self.world.nations

        def takes(port: Any, nation: str) -> bool:
            blockade = getattr(port, "blockaded_by", None)
            stance = nations.stance(port.nation, nation, port.closed_to, blockaded_by=blockade)
            return stance in ("open", "neutral")

        if takes(b, a.nation) and takes(a, a.nation):
            return a.nation
        neutrals = [str(n) for n in self.data.get("neutrals", []) if takes(a, n) and takes(b, n)]
        if not neutrals:
            return None
        return neutrals[int(self._rng().random() * len(neutrals)) % len(neutrals)]

    def _pick(self, table: str, nation: str) -> str:
        kinds = self.data.get(table, {})
        options = kinds.get(nation) or kinds.get("default") or ["merchant brig"]
        return str(options[int(self._rng().random() * len(options)) % len(options)])

    def _name(self, nation: str) -> str:
        names = self.data.get("names", {})
        options = names.get(nation) or names.get("default") or ["Fortune"]
        used = {v.name for v in self.world.vessels.vessels}
        rng = self._rng()
        for _ in range(8):
            name = str(options[int(rng.random() * len(options)) % len(options)])
            if name not in used:
                return name
        return f"{options[0]} {self.serial}"

    def _trader(self, in_port: bool) -> None:
        """A merchantman drawn: a route by the prices (the better ratios the likelier),
        in port at its origin bound away, or at an edge bound in for its destination; a
        route whose plan the far-detail guard refuses (across the land, `land_crossing`)
        is drawn again, `TRADE_TRIES` times at most."""
        for _ in range(TRADE_TRIES):
            if self._trader_once(in_port) is not None:
                return

    def _trader_once(self, in_port: bool) -> Any:
        routes = [
            r
            for r in self.routes()
            if (r[1].id, r[2].id) not in self.refused and self._arrives_clear(r[2])
        ]
        if in_port:
            routes = [r for r in routes if self._leaves_clear(r[1])]
        if not routes:
            return None
        rng = self._rng()
        weights = [r[0] for r in routes]
        x = rng.random() * sum(weights)
        chosen = routes[-1]
        for route in routes:
            x -= route[0]
            if x <= 0.0:
                chosen = route
                break
        _ratio, a, b, good = chosen
        flag = self._flag_for(a, b)
        if flag is None:
            return None
        lo, hi = self.data.get("cargo_tons", [30, 120])
        tons = int(lo + (hi - lo) * rng.random())
        description = self._pick("trader_kinds", flag)
        name = self._name(flag)
        intent = f"trade {tons} tons of {good} from {a.name} to {b.name}"
        vessel = None
        if in_port and rng.random() < float(self.data.get("outward_bound_share", 0.0)):
            # outward bound with her cargo for a market beyond the region (judgement: the
            # ocean trade the Channel's ports load for): her intent a mark beyond an edge
            # open to the sea, where she leaves the region (`tick`)
            for edge in self._edge_points(a.outer_road.position)[:EDGE_TRIES]:
                beyond = self._beyond(edge)
                vessel = self._put(
                    "trade",
                    description,
                    flag,
                    name,
                    a.anchorage.position,
                    f"bound for {plain_position(beyond)}",
                    f"{tons} tons of {good}, outward bound",
                    f"at anchor in {a.anchorage.name}",
                    departing=a.id,
                )
                if vessel is not None:
                    break
        elif in_port:
            # lying at the port's anchorage, whence her captain's plan goes out by its track
            vessel = self._put(
                "trade",
                description,
                flag,
                name,
                a.anchorage.position,
                intent,
                f"{tons} tons of {good}",
                f"at anchor in {a.anchorage.name}",
                departing=a.id,
            )
        else:
            # at the edge, the farthest of the edge points drawn whose plan in keeps off
            # the land (a point on the Bristol Channel's side has Cornwall between it and
            # Brest: the guard refuses her, and the next is tried)
            first = self._approach(b)[0][1]
            edges = [
                p
                for p in self._edge_points(first)
                if not land_crossing(self.world, p, [("to", first, "the approach")])
            ]
            for where in edges[:EDGE_TRIES]:
                vessel = self._put(
                    "trade",
                    description,
                    flag,
                    name,
                    where,
                    f"bound for {b.name}",
                    f"{tons} tons of {good}",
                    f"at the edge, {where}",
                )
                if vessel is not None:
                    break
        if vessel is None and in_port:
            # the guard refused her plan from this port to that: not drawn again
            self.refused.add((a.id, b.id))
        if vessel is not None and in_port:
            # lying at her anchorage, her business in port part done (the brains' wait)
            self._anchored_in(vessel, a)
        return vessel

    def _approach(self, port: Any) -> list[tuple[Any, ...]]:
        """The port's way in from the sea as the far body's plan: its track from the sea,
        its road, its inner track to the anchorage (`Planner.legs_for`'s, without the sea
        route to its first mark)."""
        from freesail.world.brains import _plan_of_legs
        from freesail.world.captains import Planner

        planner = Planner(self.world)
        plan = _plan_of_legs(planner._port_track(port, "from_sea"))
        road = ("to", port.outer_road.position, port.outer_road.name)
        if not any(len(leg) > 1 and leg[1] == road[1] for leg in plan):
            plan.append(road)
        plan += _plan_of_legs(planner._port_track(port, "in"))
        anchorage = ("to", port.anchorage.position, port.anchorage.name)
        if not any(len(leg) > 1 and leg[1] == anchorage[1] for leg in plan):
            plan.append(anchorage)
        return plan

    def _arrives_clear(self, port: Any) -> bool:
        """Whether the port's way in from the sea keeps off the land at far detail (the
        guard's straight lines: St Mary's road behind the islands does not), so that a
        ship drawn bound for it can be planned in; kept for the day."""
        key = f"in:{port.id}"
        if key not in self._leaves:
            plan = self._approach(port)
            self._leaves[key] = not land_crossing(self.world, plan[0][1], plan[1:])
        return self._leaves[key]

    def _leaves_clear(self, port: Any) -> bool:
        """Whether the port's own track to sea keeps off the land from its anchorage at
        far detail (the guard's straight lines; Roscoff's out by the Isle of Bas does
        not), so that a ship drawn lying there can be planned out; kept for the day."""
        if port.id not in self._leaves:
            from freesail.world.brains import _plan_of_legs
            from freesail.world.captains import Planner

            plan = _plan_of_legs(Planner(self.world)._port_track(port, "to_sea")) or [
                ("to", port.outer_road.position, port.outer_road.name)
            ]
            self._leaves[port.id] = not land_crossing(self.world, port.anchorage.position, plan)
        return self._leaves[port.id]

    def _edge_points(self, target: Position) -> list[Position]:
        """Points `EDGE_IN_NM` inside the region's edges, drawn under the seed, at sea (deep
        water three miles off the coast), the farthest from the target first (judgement: a
        ship coming in has come from beyond the region, the farther the likelier)."""
        s, n, w, e = self.bounds
        rng = self._rng()
        inside = EDGE_IN_NM / 60.0
        candidates = []
        for _ in range(12):
            side = int(rng.random() * 4) % 4
            t = rng.random()
            if side == 0:
                p = Position(s + inside, w + t * (e - w))
            elif side == 1:
                p = Position(n - inside, w + t * (e - w))
            elif side == 2:
                p = Position(s + t * (n - s), w + inside / max(math.cos(math.radians(s)), 0.2))
            else:
                p = Position(s + t * (n - s), e - inside / max(math.cos(math.radians(s)), 0.2))
            if self._at_sea(p):
                candidates.append(p)
        candidates.sort(key=lambda p: -bearing_and_distance(p, target)[1])
        return candidates

    def _beyond(self, p: Position) -> Position:
        """A point `EDGE_IN_NM` inside an edge carried across it to `BEYOND_NM` outside:
        the mark an outward-bound ship steers for, beyond the region."""
        s, n, w, e = self.bounds
        coslat = max(math.cos(math.radians(p.lat_deg)), 0.2)
        gaps = [
            (p.lat_deg - s, 0),
            (n - p.lat_deg, 1),
            ((p.lon_deg - w) * coslat, 2),
            ((e - p.lon_deg) * coslat, 3),
        ]
        side = min(gaps)[1]
        out = BEYOND_NM / 60.0
        if side == 0:
            return Position(s - out, p.lon_deg)
        if side == 1:
            return Position(n + out, p.lon_deg)
        if side == 2:
            return Position(p.lat_deg, w - out / coslat)
        return Position(p.lat_deg, e + out / coslat)

    def _at_sea(self, p: Position) -> bool:
        chart = getattr(self.world, "chart", None)
        if chart is None:
            return True
        depth = chart.depth_at(p)
        found = chart.coast_distance(p) if depth is not None else None
        return depth is not None and depth > 20.0 and (found is None or found[0] > 3 * 1852.0)

    # -- the fishermen ---------------------------------------------------------------------

    def grounds(self) -> list[tuple[Any, Any]]:
        """The fishing grounds of the region and their homes: (the feature, the port that
        sells fish nearest it within `home_within_nm`), by the features' ids."""
        world = self.world
        chart = getattr(world, "chart", None)
        if chart is None:
            return []
        fishing = self.data.get("fishing", {})
        lo, hi = fishing.get("depth_fathoms", [10, 80])
        off = float(fishing.get("off_the_coast_nm", 2))
        home_nm = float(fishing.get("home_within_nm", 45))
        goods = set(fishing.get("goods", []))
        homes = [p for p in self.ports() if goods & set(p.market.goods)]
        out: list[tuple[Any, Any]] = []
        for fid in sorted(chart.features):
            f = chart.features[fid]
            if f.kind not in ("bottom", "bank") or not self.inside(f.position):
                continue
            depth = chart.depth_at(f.position)
            if depth is None or not (lo <= units.m_to_fathoms(depth) <= hi):
                continue
            found = chart.coast_distance(f.position)
            if found is not None and found[0] / units.NAUTICAL_MILE < off:
                continue
            near = [
                (bearing_and_distance(f.position, p.outer_road.position)[1], p.id, p) for p in homes
            ]
            near = [x for x in near if x[0] / units.NAUTICAL_MILE <= home_nm]
            if near:
                out.append((f, min(near)[2]))
        return out

    def _fisherman(self, at_start: bool) -> None:
        grounds = self.grounds()
        if not grounds:
            return
        rng = self._rng()
        ground, home = grounds[int(rng.random() * len(grounds)) % len(grounds)]
        fishing = self.data.get("fishing", {})
        lo, hi = fishing.get("trip_hours", [8, 30])
        hours = int(lo + (hi - lo) * rng.random())
        description = self._pick("fisher_kinds", home.nation)
        name = self._name(home.nation)
        intent = f"fish on {ground.name} for {hours} hours from {home.name}"
        if at_start:
            where, said = ground.position, f"on {ground.name}"
        else:
            where, said = home.anchorage.position, f"in {home.anchorage.name}"
        vessel = self._put(
            "fishing",
            description,
            home.nation,
            name,
            where,
            intent,
            "",
            said,
            departing="" if at_start else home.id,
        )
        if vessel is not None and not at_start:
            self._anchored_in(vessel, home)

    # -- the cruisers ----------------------------------------------------------------------

    def _cruisers(self) -> None:
        """A cruiser of each nation at war on a station of hers within the region, by the
        cruiser's doctrine (`stations:`)."""
        from freesail.world.captains import CAPTAINS_DIR

        raw = yaml.safe_load((CAPTAINS_DIR / "cruiser.yaml").read_text(encoding="utf-8")) or {}
        stations = raw.get("stations") or {}
        nations = self.world.nations
        chart = self.world.chart
        per_side = self._n("cruisers_per_side")
        for nation in sorted(stations):
            if not any(nations.at_war(nation, other) for other in nations.nations):
                continue
            mine = []
            for entry in stations[nation] or []:
                f = chart.find_feature(str(entry["place"]))
                if f is not None and self.inside(f.position):
                    mine.append((entry, f))
            rng = self._rng()
            for _ in range(min(per_side, len(mine))):
                entry, f = mine.pop(int(rng.random() * len(mine)) % len(mine))
                within = float(entry.get("within_nm", 10))
                intent = f"keep the station off {f.name} within {within:g} miles"
                from freesail.world.captains import station_off

                where = station_off(self.world, f.position, within)
                self._put(
                    "cruiser",
                    str(entry.get("kind") or "brig-sloop"),
                    nation,
                    self._name(nation) if nation not in ("britain", "france") else "",
                    where,
                    intent,
                    "",
                    f"on her station off {f.name}",
                    colours=entry.get("colours", "shown"),
                )

    # -- putting a ship on the sea -----------------------------------------------------

    def _put(
        self,
        kind: str,
        description: str,
        nation: str,
        name: str,
        where: Position,
        intent: str,
        carries: str,
        said: str,
        colours: str = "shown",
        departing: str = "",
    ) -> Any:
        from freesail.world.ships import vessel_from_spec

        world = self.world
        vid = f"business-{self.serial + 1}"
        if not name:
            name = self._name(nation) if kind != "cruiser" else self._cruiser_name(nation)
        spec = {
            "id": vid,
            "description": description,
            "name": name,
            "nation": nation,
            "position": where.to_dict(),
            "goal": "bound for Falmouth",  # replaced by the intent's plan
            "intent": intent,
            "colours": colours,
        }
        if departing:
            spec["departing"] = departing
        from freesail.world.ships import SAILING_FACTOR_MIN

        spec["sailing_factor"] = SAILING_FACTOR_MIN + (1.0 - SAILING_FACTOR_MIN) * (
            self._rng().random()
        )
        try:
            vessel = vessel_from_spec(world, spec, world.vessels.serial + 1)
        except ValueError:
            return None  # a plan the guard refuses (across the land): not drawn
        self.serial += 1
        world.vessels.serial += 1
        world.vessels.add(vessel)
        self.drawn.append(
            Drawn(vid, world.clock.tick, kind, description, nation, name, intent, said, carries)
        )
        return vessel

    def _cruiser_name(self, nation: str) -> str:
        names = self.data.get("cruiser_names", {}).get(nation) or self.data.get("names", {}).get(
            nation
        )
        if not names:
            return f"the {nation} cruiser"
        rng = self._rng()
        return str(names[int(rng.random() * len(names)) % len(names)])

    def _anchored_in(self, vessel: Any, port: Any) -> None:
        """A ship drawn lying in a port: at anchor at its anchorage, her business there
        part done (the brains' `IN_PORT_WAIT_S` begun some hours before the draw)."""
        lo, hi = self.data.get("in_port_hours_drawn", [1, 11])
        hours = lo + (hi - lo) * self._rng().random()
        vessel.saved_plan = None
        vessel.plan = [("anchor", port.id)]
        brain = vessel.brain
        if brain is not None:
            brain._departing = port.id
            brain.state = None
            brain.planned = True
            brain._business["drawn_in_port_s"] = hours * 3600.0
            brain._state_entered = None
            brain._drawn_wait = int(hours * 3600.0)

    # -- the rumours of the quay -------------------------------------------------------

    def rumour(self, port: Any) -> str:
        """Two or three words of prices high or low at the ports the market knows (the
        owner's note 24): the ports within `rumours.within_nm`, their goods that this
        port's market also lists, a price told when it is `rumours.ratio` above or below
        this port's own, as of the day; drawn under the seed; "" when there is none."""
        world = self.world
        ports = getattr(world, "ports", None)
        if ports is None:
            return ""
        cfg = self.data.get("rumours", {})
        within = float(cfg.get("within_nm", 250)) * units.NAUTICAL_MILE
        ratio = float(cfg.get("ratio", 1.3))
        when = world.clock.ship_time
        nations = world.nations
        told: list[tuple[str, str, str]] = []
        for _pid, other in sorted(ports.ports.items()):
            if other is port:
                continue
            apart = bearing_and_distance(port.outer_road.position, other.outer_road.position)[1]
            if apart > within:
                continue
            for good in sorted(port.market.goods):
                if good not in other.market.goods:
                    continue
                here = port.market.price(good, when, nations, port.nation)
                there = other.market.price(good, when, nations, other.nation)
                if here <= 0:
                    continue
                if there / here >= ratio:
                    told.append((good, "dear", other.name))
                elif here / max(there, 1e-9) >= ratio:
                    told.append((good, "cheap", other.name))
        if not told:
            return ""
        rng = self._rng()
        lo, hi = cfg.get("how_many", [2, 3])
        n = min(len(told), int(lo + (hi - lo + 1) * rng.random()))
        picked = []
        pool = list(told)
        for _ in range(n):
            picked.append(pool.pop(int(rng.random() * len(pool)) % len(pool)))
        words = [f"{good} {how} at {where}" for good, how, where in picked]
        said = ", ".join(words[:-1]) + (" and " if len(words) > 1 else "") + words[-1]
        return f"The talk on the quay, as the boat's crew heard it: {said}. Rumour, no more."

    def to_dict(self) -> dict[str, Any]:
        return {
            "density": self.density,
            "region": self.region,
            "drawn": [d.to_dict() for d in self.drawn],
        }
