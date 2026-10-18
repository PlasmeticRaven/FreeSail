"""Fishing (package 56; spec M7b §21a): the grounds, the gear's fishing, the catch, the
well and the hold's salt, and the fish quays.

The owner, 2026-10-17: a player who wants to fish at the level the game can reasonably
simulate may; not a fishing simulation, but researched grounds, real catches to market,
the period's evolutions and the well's spoilage. So:

- **the grounds** are data (`data/fishing/<region>.yaml`), each keyed to a feature of the
  chart where it has one (the business's grounds, `business.grounds()`, among them) or
  pricked at a position with its source, with its fish by the gear that takes them, the
  months, the hour (by night, by day or at any hour) and the yield, tons an hour of the
  gear fishing; a bottom or a bank the tables do not name keeps the default of
  `data/fishing/fish.yaml` (`default_ground`);
- **one catch function** (`take`): the tons of each fish a gear takes on a ground in a
  stretch of time at an hour, a season and a wind, called once a minute for the player's
  ship and a crewed fisherman (`Fishery.tick`, the gear in the water) and for the far
  body of the business's fisherman (`far_work`), so that the smack the player sails and
  the business's are one thing at two details (truth 106);
- **the catch aboard** (`Catch`): lots of fish in the well (alive, for the days a fish
  that lives there lives; the hours a fish that does not keeps in its running water) or
  in the hold (salted where salt is aboard, a third of the fish's weight; else spoiling
  in so many hours, fewer in summer), the spoilage said in the log once a day and when a
  lot turns, and at the sale;
- **the quays** (`fish.yaml` `markets:`): a port that buys fish takes the sound lots at
  its price, fresh or salted, and credits the purse (`sell_catch`); spoiled fish go over
  the side.

The gear a vessel carries is her file's (`gear:`, from `tools/gen_ships.py`); the gear's
evolutions are `data/evolutions/shoot_*.yaml` and `haul_*.yaml` (`evolutions.scripts.
FishingGearScript`), the orders `orders.fishing`. Nothing of this exists on a ship with no
gear and no catch: the World's `fishery` is None, and nothing of a recorded passage moves.
"""

from __future__ import annotations

import functools
import math
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

from freesail import units
from freesail.core.events import Severity
from freesail.world.geo import Position, bearing_and_distance

__all__ = [
    "FISHING_DIR",
    "Catch",
    "Fishery",
    "GearOut",
    "Ground",
    "Lot",
    "evolution_of",
    "find_ground",
    "ground_at",
    "grounds",
    "load_fishing",
    "take",
]

FISHING_DIR = Path(__file__).resolve().parents[2] / "data" / "fishing"
# The summer months for the hold's spoilage (judgement: May to September, the warm months).
SUMMER_MONTHS = frozenset({5, 6, 7, 8, 9})
# The change of light: the drift nets take half as much again at the twilight (Holdsworth
# 1874 pp. 98 to 99: the fish "especially likely to 'strike' the net" just after sunset
# and before sunrise); a day gear takes half at the twilight (judgement).
TWILIGHT_NIGHT = 1.5
TWILIGHT_DAY = 0.5
# The wind's effect on the gear's work: full up to this part of its most wind, falling to
# half at the most, nothing beyond (judgement: the hands and the gear in a seaway).
WIND_FULL_PART = 0.6
# The evolutions of each kind of gear: (shoot, haul), by their files' ids.
EVOLUTIONS: dict[str, tuple[str, str]] = {
    "trawl": ("shoot_trawl", "haul_trawl"),
    "drift nets": ("shoot_nets", "haul_nets"),
    "seine": ("shoot_seine", "haul_seine"),
    "lines": ("set_lines", "haul_lines"),
}
# A ground's reach when the order names none: the ground's own radius; a ship within it
# fishes there.
DAY_LINE_HOUR = 8  # the catch's day line at eight in the morning (judgement: the forenoon)


@functools.lru_cache(maxsize=2)
def load_fishing(root: str = str(FISHING_DIR)) -> dict[str, Any]:
    """The fish, the gear, the quays and every region's grounds, read once."""
    base = Path(root)
    data = yaml.safe_load((base / "fish.yaml").read_text(encoding="utf-8")) or {}
    regions: dict[str, list[dict[str, Any]]] = {}
    for path in sorted(base.glob("*.yaml")):
        if path.name == "fish.yaml":
            continue
        doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        regions[str(doc.get("region") or path.stem)] = list(doc.get("grounds") or [])
    data["regions"] = regions
    return data


def evolution_of(kind: str, action: str) -> str:
    """The evolution's id for a kind of gear and an action (`shoot` or `haul`)."""
    shoot, haul = EVOLUTIONS[kind]
    return shoot if action == "shoot" else haul


def gear_spec(kind: str) -> dict[str, Any]:
    return dict(load_fishing().get("gear", {}).get(kind) or {})


def fish_spec(name: str) -> dict[str, Any]:
    return dict(load_fishing().get("fish", {}).get(name) or {})


def fish_words(name: str) -> str:
    return str(fish_spec(name).get("words") or name)


# ---------------------------------------------------------------------------
# The grounds
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Entry:
    """One fish of a ground: the gear that takes it, its months, its hour and its yield."""

    fish: str
    gear: str
    months: frozenset[int]
    when: str  # night, day or any
    tons_per_hour: float
    source: str = ""


@dataclass(frozen=True)
class Ground:
    """A fishing ground: its id and name, where it lies and how far it reaches, the
    chart's feature it is keyed to (or none), and its fish."""

    id: str
    name: str
    position: Position
    radius_nm: float
    feature: str = ""
    entries: tuple[Entry, ...] = ()
    source: str = ""
    named: bool = True  # False: a bottom or a bank the tables do not name (the default)

    def gear_kinds(self) -> list[str]:
        out: list[str] = []
        for e in self.entries:
            if e.gear not in out and e.tons_per_hour > 0:
                out.append(e.gear)
        return out

    def in_season(self, gear: str, month: int) -> list[Entry]:
        return [
            e for e in self.entries if e.gear == gear and month in e.months and e.tons_per_hour > 0
        ]

    def season_words(self, gear: str) -> str:
        """'pilchards July to December by day; mackerel June to August by day'."""
        parts = []
        for e in self.entries:
            if e.gear != gear or e.tons_per_hour <= 0:
                continue
            parts.append(f"{fish_words(e.fish)} {_months_words(e.months)} {_when_words(e.when)}")
        return "; ".join(parts) or "nothing"


def _months(raw: Any) -> frozenset[int]:
    if raw in ("all", None):
        return frozenset(range(1, 13))
    return frozenset(int(m) for m in raw)


def _entries(raw: list[dict[str, Any]]) -> tuple[Entry, ...]:
    return tuple(
        Entry(
            fish=str(e["fish"]),
            gear=str(e["gear"]),
            months=_months(e.get("months", "all")),
            when=str(e.get("when") or "any"),
            tons_per_hour=float(e.get("tons_per_hour", 0.0)),
            source=str(e.get("source") or ""),
        )
        for e in raw
    )


MONTH_NAMES = (
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
)


def _months_words(months: frozenset[int]) -> str:
    if len(months) == 12:
        return "all the year"
    ms = sorted(months)
    # a run that wraps the year (October to April)
    for start in ms:
        run = [((start - 1 + i) % 12) + 1 for i in range(len(ms))]
        if set(run) == set(ms):
            return f"{MONTH_NAMES[run[0] - 1]} to {MONTH_NAMES[run[-1] - 1]}"
    return ", ".join(MONTH_NAMES[m - 1] for m in ms)


def _when_words(when: str) -> str:
    return {"night": "by night", "day": "by day"}.get(when, "at any hour")


def grounds(world: Any) -> list[Ground]:
    """The tables' grounds of the chart's regions the world has, by their ids; a ground
    keyed to a feature the chart has not got is left out."""
    chart = getattr(world, "chart", None)
    cache = getattr(chart, "_fishing_grounds", None) if chart is not None else None
    if cache is not None:
        return cache
    regions = list(getattr(chart, "regions", ()) or ()) if chart is not None else []
    data = load_fishing()
    out: list[Ground] = []
    for region in regions:
        for raw in data["regions"].get(region, []):
            fid = str(raw.get("feature") or "")
            if fid:
                f = chart.feature(fid) if chart is not None else None
                if f is None:
                    continue
                pos = f.position
            else:
                p = raw["position"]
                pos = Position(float(p["lat_deg"]), float(p["lon_deg"]))
            out.append(
                Ground(
                    id=str(raw["id"]),
                    name=str(raw["name"]),
                    position=pos,
                    radius_nm=float(raw.get("radius_nm", 2.0)),
                    feature=fid,
                    entries=_entries(list(raw.get("fish") or [])),
                    source=str(raw.get("source") or ""),
                )
            )
    if chart is not None:
        try:
            chart._fishing_grounds = out
        except AttributeError:  # a chart that takes no attribute: read each time
            pass
    return out


def default_ground(feature: Any) -> Ground:
    """A bottom or a bank the tables do not name, worked by the business's fishermen: the
    default fish of `fish.yaml` (package 43b's ground, now with a yield)."""
    return Ground(
        id=str(feature.id),
        name=str(feature.name),
        position=feature.position,
        radius_nm=2.0,
        feature=str(feature.id),
        entries=_entries(list(load_fishing().get("default") or [])),
        source="the default of data/fishing/fish.yaml",
        named=False,
    )


def _key(words: str) -> str:
    return " ".join(str(words).lower().replace("'", "").split()).removeprefix("the ")


def find_ground(world: Any, words: str) -> Ground | None:
    """A ground by its id, its name or its feature's id or name."""
    key = _key(words)
    chart = getattr(world, "chart", None)
    for g in grounds(world):
        names = {_key(g.id), _key(g.name), _key(g.feature)}
        if g.feature and chart is not None:
            f = chart.feature(g.feature)
            if f is not None:
                names.add(_key(f.name))
        if key in names:
            return g
    return None


def ground_at(world: Any, pos: Position | None, slack: float = 1.0) -> Ground | None:
    """The ground she is on: the nearest whose radius (times `slack`) reaches her; a
    bottom or a bank of the business's grounds that the tables do not name, within two
    miles, keeps the default; None off every ground."""
    if pos is None:
        return None
    best: tuple[float, Ground] | None = None
    for g in grounds(world):
        nm = bearing_and_distance(pos, g.position)[1] / units.NAUTICAL_MILE
        if nm <= g.radius_nm * slack and (best is None or nm < best[0]):
            best = (nm, g)
    if best is not None:
        return best[1]
    chart = getattr(world, "chart", None)
    if chart is None:
        return None
    named = {g.feature for g in grounds(world) if g.feature}
    from freesail.world.business import load_business

    lo, hi = (load_business().get("fishing") or {}).get("depth_fathoms", [10, 80])
    for fid in sorted(getattr(chart, "features", {}) or {}):
        f = chart.features[fid]
        if f.kind not in ("bottom", "bank") or fid in named:
            continue
        nm = bearing_and_distance(pos, f.position)[1] / units.NAUTICAL_MILE
        if nm > 2.0 * slack:
            continue
        depth = chart.depth_at(f.position)
        if depth is None or not (lo <= units.m_to_fathoms(depth) <= hi):
            continue
        if nm <= 2.0 * slack and (best is None or nm < best[0]):
            best = (nm, default_ground(f))
    return best[1] if best is not None else None


def nearest_grounds(world: Any, pos: Position, n: int = 3) -> list[tuple[float, Ground]]:
    out = []
    for g in grounds(world):
        nm = bearing_and_distance(pos, g.position)[1] / units.NAUTICAL_MILE
        out.append((nm, g))
    out.sort(key=lambda x: x[0])
    return out[:n]


# ---------------------------------------------------------------------------
# The one catch function (truth 106: the same at both details)
# ---------------------------------------------------------------------------


def hour_factor(when: str, daylight: str) -> float:
    """The part of a fish's yield taken at this hour: a night fish by night, half as
    much again at the change of light, nothing by day; a day fish the reverse, half at
    the twilight; an any-hour fish always."""
    if when == "night":
        return {"night": 1.0, "twilight": TWILIGHT_NIGHT}.get(daylight, 0.0)
    if when == "day":
        return {"day": 1.0, "twilight": TWILIGHT_DAY}.get(daylight, 0.0)
    return 1.0


def wind_factor(kind: str, wind_kn: float) -> float:
    """The part the gear takes in this wind: full to `WIND_FULL_PART` of its most, half
    at the most, nothing beyond."""
    most = float(gear_spec(kind).get("most_wind_kn", 25.0))
    if wind_kn > most:
        return 0.0
    full = most * WIND_FULL_PART
    if wind_kn <= full:
        return 1.0
    return 1.0 - 0.5 * (wind_kn - full) / max(most - full, 1e-6)


def way_factor(kind: str, way_kn: float | None) -> float:
    """The trawl fishes only with the way it wants (Holdsworth pp. 77 to 78); the other
    gear at any. None: the way not known (the far body, at the gear's own)."""
    band = gear_spec(kind).get("way_kn")
    if not band or way_kn is None:
        return 1.0
    lo, hi = float(band[0]), float(band[1])
    return 1.0 if lo <= way_kn <= hi else 0.0


def take(
    ground: Ground,
    kind: str,
    when: datetime,
    daylight: str,
    wind_kn: float,
    seconds: float,
    way_kn: float | None = None,
) -> dict[str, float]:
    """The tons of each fish the gear of this kind takes on this ground in `seconds` at
    this hour, season and wind (and way, for the trawl): the one catch function, called
    a minute at a time at either detail."""
    out: dict[str, float] = {}
    hours = float(seconds) / 3600.0
    weather = wind_factor(kind, wind_kn) * way_factor(kind, way_kn)
    if weather <= 0.0 or hours <= 0.0:
        return out
    for e in ground.in_season(kind, when.month):
        tons = e.tons_per_hour * hours * hour_factor(e.when, daylight) * weather
        if tons > 0.0:
            out[e.fish] = out.get(e.fish, 0.0) + tons
    return out


def fishing_now(ground: Ground, kind: str, when: datetime, daylight: str) -> bool:
    """Whether the gear takes anything on the ground at this hour and season."""
    return any(hour_factor(e.when, daylight) > 0 for e in ground.in_season(kind, when.month))


# ---------------------------------------------------------------------------
# The gear in the water
# ---------------------------------------------------------------------------


@dataclass
class GearOut:
    """A piece of gear shot: which, on what ground, since when, how long it has fished,
    and what is in it (tons by fish) until it is hauled."""

    gear_id: str
    kind: str
    name: str
    ground_id: str
    shot_tick: int
    fished_s: float = 0.0
    taken: dict[str, float] = field(default_factory=dict)
    state: str = "fishing"  # fishing; hauling

    def full(self) -> bool:
        return self.fished_s >= float(gear_spec(self.kind).get("hours_a_shot", 6)) * 3600.0

    def doing_words(self) -> str:
        """'towing her trawl', 'riding to her nets': the work in hand's words."""
        return str(gear_spec(self.kind).get("at_it") or f"at her {self.kind}")

    def words(self) -> str:
        hours = self.fished_s / 3600.0
        return f"{self.doing_words()} ({_hours_words(hours)} fishing)"


def _hours_words(hours: float) -> str:
    if hours < 1.0:
        return f"{int(round(hours * 60))} minutes"
    n = round(hours * 2) / 2
    return f"{n:g} hour{'s' if n != 1 else ''}"


def _tons_words(tons: float) -> str:
    if tons < 0.05:
        cwt = int(round(tons * 20))
        return f"{cwt} hundredweight" if cwt else "a few fish"
    n = round(tons, 1)
    return f"{n:g} ton{'s' if n != 1 else ''}"


# ---------------------------------------------------------------------------
# The catch aboard
# ---------------------------------------------------------------------------


@dataclass
class Lot:
    """Fish of one kind stowed at one time: where (the well or the hold), whether salted,
    when caught, and the tick it spoils at (None: it keeps, salted)."""

    fish: str
    tons: float
    where: str  # well, hold
    caught_tick: int
    spoils_tick: int | None
    salted: bool = False
    spoiled: bool = False
    alive: bool = False  # in the well and living there

    def words(self) -> str:
        what = f"{_tons_words(self.tons)} of {fish_words(self.fish)}"
        if self.spoiled:
            return f"{what}, spoiled"
        if self.salted:
            return f"{what} in salt"
        if self.where == "well":
            return f"{what} in the well" + (", alive" if self.alive else "")
        return f"{what} in the hold, unsalted"


@dataclass
class Catch:
    """The catch aboard a vessel: the lots in the well and the hold, the well's and the
    hold's room, and the spoilage."""

    well_tons: float = 0.0
    hold_tons: float = 0.0
    lots: list[Lot] = field(default_factory=list)
    landed: list[dict[str, Any]] = field(default_factory=list)  # the sales, for the record

    def tons(self, where: str | None = None, sound: bool = True) -> float:
        return sum(
            lot.tons
            for lot in self.lots
            if (where is None or lot.where == where) and (not sound or not lot.spoiled)
        )

    def in_well(self) -> float:
        return sum(lot.tons for lot in self.lots if lot.where == "well")

    def in_hold(self) -> float:
        return sum(lot.tons for lot in self.lots if lot.where == "hold")

    def stow(
        self, taken: dict[str, float], tick: int, when: datetime, salt: float | None = None
    ) -> tuple[list[Lot], float, float]:
        """The haul struck below: into the well first, then the hold, salted while the
        salt lasts (`salt` tons aboard, None for none to be had); what will not stow goes
        back over the side. Returns (the lots made, the tons over the side, the salt
        used)."""
        data = load_fishing()
        per_ton = float(data.get("salt_per_ton", 0.33))
        made: list[Lot] = []
        lost = 0.0
        salt_used = 0.0
        hold_room = max(0.0, self.hold_tons - self.in_hold())
        for fish in sorted(taken):
            tons = float(taken[fish])
            if tons <= 1e-6:
                continue
            spec = fish_spec(fish)
            room = max(0.0, self.well_tons - self.in_well())
            into_well = min(tons, room)
            if into_well > 1e-6:
                if spec.get("well"):
                    life = int(float(spec.get("well_days", 4)) * 86400)
                    alive = True
                else:
                    life = int(float(spec.get("well_hours", 12)) * 3600)
                    alive = False
                lot = Lot(fish, into_well, "well", tick, tick + life, alive=alive)
                self.lots.append(lot)
                made.append(lot)
                tons -= into_well
            into_hold = min(tons, hold_room)
            if into_hold > 1e-6:
                hold_room -= into_hold
                tons -= into_hold
                salted_tons = 0.0
                if salt is not None and salt - salt_used > 1e-6:
                    salted_tons = min(into_hold, (salt - salt_used) / per_ton)
                if salted_tons > 1e-6:
                    lot = Lot(fish, salted_tons, "hold", tick, None, salted=True)
                    self.lots.append(lot)
                    made.append(lot)
                    salt_used += salted_tons * per_ton
                if into_hold - salted_tons > 1e-6:
                    lot = Lot(
                        fish,
                        into_hold - salted_tons,
                        "hold",
                        tick,
                        tick + keeps_s(fish, when),
                    )
                    self.lots.append(lot)
                    made.append(lot)
            lost += max(0.0, tons)
        return made, lost, salt_used

    def turn(self, tick: int) -> list[Lot]:
        """The lots spoiled by now (each once)."""
        out = []
        for lot in self.lots:
            if not lot.spoiled and lot.spoils_tick is not None and tick >= lot.spoils_tick:
                lot.spoiled = True
                lot.alive = False
                out.append(lot)
        return out

    def words(self, tick: int | None = None) -> str:
        if not self.lots:
            return "no fish aboard"
        parts = []
        for lot in self.lots:
            w = lot.words()
            if tick is not None and not lot.spoiled and lot.spoils_tick is not None:
                left = (lot.spoils_tick - tick) / 3600.0
                w += f", good for {_hours_words(max(0.0, left))} more"
            parts.append(w)
        return "; ".join(parts)

    def value(self, port_id: str, tick: int | None = None) -> tuple[float, list[str]]:
        """What the sound lots fetch at a quay, in pounds, and the words of each sale."""
        factor = market_factor(port_id)
        if factor is None:
            return 0.0, []
        total = 0.0
        words = []
        for lot in self.lots:
            if lot.spoiled:
                continue
            price = price_of(lot.fish, lot.salted) * factor
            total += price * lot.tons
            words.append(f"{lot.words()} at {_pounds(price)} a ton")
        return total, words


def keeps_s(fish: str, when: datetime) -> int:
    """The seconds an unsalted fish keeps in the hold at this time of the year."""
    hours = fish_spec(fish).get("keeps_hours") or {}
    season = "summer" if when.month in SUMMER_MONTHS else "winter"
    return int(float(hours.get(season, 24)) * 3600)


def market_factor(port_id: str) -> float | None:
    m = (load_fishing().get("markets") or {}).get(port_id)
    return None if m is None else float(m.get("factor", 1.0))


def price_of(fish: str, salted: bool) -> float:
    price = fish_spec(fish).get("price") or {}
    return float(price.get("salted" if salted else "fresh", 0.0))


def _pounds(pounds: float) -> str:
    from freesail.world.places import pounds_words

    return pounds_words(pounds)


# ---------------------------------------------------------------------------
# The fishery of a vessel: the gear she carries, the gear out, the catch
# ---------------------------------------------------------------------------


@dataclass
class Fishery:
    """A fishing vessel's fishery, one object for her two bodies: the gear she carries,
    the gear in the water, the catch aboard, and the day's line. The player's World and a
    crewed fisherman's keep it as `world.fishery`; the far body as `vessel.fishing`."""

    gear: list[Any] = field(default_factory=list)  # her file's GearSpecs
    out: GearOut | None = None
    catch: Catch = field(default_factory=Catch)
    day_said: int = -1  # the day of the year the catch's day line was last said
    # the far body's gear cycle (`far_work`): the phase and its seconds
    far_phase: str = ""
    far_phase_s: float = 0.0

    @classmethod
    def of_spec(cls, spec: Any) -> Fishery | None:
        """A fishery for a ship of this file, or None when she carries no gear."""
        gear = list(getattr(spec, "gear", None) or [])
        if not gear:
            return None
        hold = getattr(spec, "hold", None)
        well_m3 = float(getattr(hold, "well_m3", 0.0) or 0.0) if hold is not None else 0.0
        hold_tons = float(getattr(hold, "capacity_tons", 0.0) or 0.0) if hold is not None else 0.0
        per = float(load_fishing().get("well_tons_per_m3", 0.33))
        return cls(gear=gear, catch=Catch(well_tons=round(well_m3 * per, 2), hold_tons=hold_tons))

    def carries(self, kind: str) -> Any:
        for g in self.gear:
            if g.kind == kind:
                return g
        return None

    def kinds(self) -> list[str]:
        return [g.kind for g in self.gear]

    def words(self, tick: int | None = None) -> str:
        """The fishery in words: the gear out and the catch aboard."""
        parts = []
        if self.out is not None:
            parts.append(self.out.words())
        parts.append(self.catch.words(tick))
        return "; ".join(parts)

    # -- the World's minute ------------------------------------------------------------

    def tick(self, world: Any) -> list[tuple[Severity, str, str, dict[str, Any]]]:
        """Once a minute: the gear out fishing by the one catch function; the lots turned
        by now; the catch's day line."""
        lines: list[tuple[Severity, str, str, dict[str, Any]]] = []
        now = world.clock.tick
        when = world.clock.ship_time
        out = self.out
        if out is not None and out.state == "fishing":
            ground = ground_named(world, out.ground_id)
            if ground is not None and not out.full():
                dyn = getattr(getattr(world, "ship", None), "dyn", None)
                way = units.ms_to_knots(float(getattr(dyn, "u", 0.0) or 0.0)) if dyn else None
                got = take(
                    ground,
                    out.kind,
                    when,
                    str(world.daylight),
                    units.ms_to_knots(float(world.wind.base_speed)),
                    60.0,
                    way_kn=way,
                )
                for fish, tons in got.items():
                    out.taken[fish] = out.taken.get(fish, 0.0) + tons
            out.fished_s += 60.0
        for lot in self.catch.turn(now):
            lines.append(
                (
                    Severity.NOTABLE,
                    "fishing.spoiled",
                    f"The {fish_words(lot.fish)} in the {lot.where} have spoiled: "
                    f"{_tons_words(lot.tons)}, fit for nothing but the farmers' dung.",
                    {"fish": lot.fish, "tons": round(lot.tons, 3), "where": lot.where},
                )
            )
        day = when.timetuple().tm_yday
        if (
            self.catch.lots
            and when.hour == DAY_LINE_HOUR
            and when.minute == 0
            and day != self.day_said
        ):
            self.day_said = day
            lines.append(
                (
                    Severity.ROUTINE,
                    "fishing.catch",
                    f"The catch this morning: {self.catch.words(now)}.",
                    {"tons": round(self.catch.tons(), 3)},
                )
            )
        return lines


def ground_named(world: Any, gid: str) -> Ground | None:
    for g in grounds(world):
        if g.id == gid:
            return g
    chart = getattr(world, "chart", None)
    f = chart.feature(gid) if chart is not None else None
    return default_ground(f) if f is not None else None


def salt_aboard(world: Any) -> float | None:
    hold = getattr(world, "hold", None)
    if hold is None:
        return None
    tons = float(hold.goods.get("salt", 0.0) or 0.0)
    return tons if tons > 0 else None


def haul_into(world: Any, fishery: Fishery) -> tuple[str, dict[str, Any]]:
    """The gear's take struck below at the haul's end: into the well and the hold (the
    hold's salt used and broken out of the manifest); the line's words and data."""
    out = fishery.out
    if out is None:
        return "Nothing was in the gear.", {}
    taken = {f: t for f, t in out.taken.items() if t > 1e-6}
    fishery.out = None
    rig_gear_drag(world, fishery)
    when = world.clock.ship_time
    salt = salt_aboard(world)
    lots, lost, salt_used = fishery.catch.stow(taken, world.clock.tick, when, salt)
    if salt_used > 0 and getattr(world, "hold", None) is not None:
        world.hold.break_out("salt", min(salt_used, world.hold.goods.get("salt", 0.0)))
    total = sum(taken.values())
    data = {
        "gear": out.kind,
        "ground": out.ground_id,
        "taken": {f: round(t, 3) for f, t in taken.items()},
        "tons": round(total, 3),
        "hours": round(out.fished_s / 3600.0, 2),
        "over_the_side": round(lost, 3),
        "salted": round(salt_used / max(float(load_fishing().get("salt_per_ton", 0.33)), 1e-6), 3),
    }
    if total <= 1e-6:
        return f"Hauled {out.name}: nothing in it after {_hours_words(out.fished_s / 3600)}.", data
    what = ", ".join(f"{_tons_words(t)} of {fish_words(f)}" for f, t in sorted(taken.items()))
    where = "; ".join(lot.words() for lot in lots) or "nothing stowed"
    text = f"Hauled {out.name}: {what}. Struck down: {where}."
    if lost > 1e-6:
        text += f" {_tons_words(lost).capitalize()} would not stow and went back over the side."
    return text, data


# ---------------------------------------------------------------------------
# The sale at a fish quay
# ---------------------------------------------------------------------------


def sell_catch(world: Any, fishery: Fishery, port: Any) -> tuple[str, dict[str, Any]]:
    """The catch landed at the quay of a port that buys fish: the sound lots sold at its
    price, the purse credited; the spoiled thrown over the side; said with the spoilage.
    Raises ValueError in words when the port buys none or there is nothing to sell."""
    factor = market_factor(port.id)
    if factor is None:
        raise ValueError(f"{port.name} has no fish quay; the fish are bought at {quays_words()}.")
    catch = fishery.catch
    if not catch.lots:
        raise ValueError("There is no fish aboard to sell.")
    total, words = catch.value(port.id)
    spoiled = [lot for lot in catch.lots if lot.spoiled]
    sold = [lot for lot in catch.lots if not lot.spoiled]
    now = world.clock.tick
    if total > 0 and getattr(world, "purse", None) is not None:
        world.purse.take(total, f"the catch sold at {port.name}", now)
    record = {
        "port": port.id,
        "pounds": round(total, 2),
        "sold": _by_fish(sold),
        "spoiled": _by_fish(spoiled),
        "tick": now,
    }
    catch.landed.append(record)
    catch.lots = []
    text = f"The catch landed on the quay at {port.name}"
    if words:
        text += f" and sold: {'; '.join(words)}; {_pounds(total)} in all"
    else:
        text += ", and nothing of it sound to sell"
    if spoiled:
        gone = ", ".join(f"{_tons_words(lot.tons)} of {fish_words(lot.fish)}" for lot in spoiled)
        text += f". Spoiled and thrown over the side: {gone}"
    purse = getattr(world, "purse", None)
    if purse is not None:
        text += f". The purse: {purse.words()}"
    return text + ".", record


def _by_fish(lots: list[Lot]) -> dict[str, float]:
    """The tons of each fish in the lots, for the sale's record."""
    out: dict[str, float] = {}
    for lot in lots:
        out[lot.fish] = round(out.get(lot.fish, 0.0) + lot.tons, 3)
    return out


def quays_words() -> str:
    names = sorted((load_fishing().get("markets") or {}).keys())
    return ", ".join(n.replace("-", " ").title() for n in names)


def land_far(world: Any, vessel: Any, port: Any) -> dict[str, Any] | None:
    """The business's fisherman home: her catch sold at her port's quay at the same
    price as the player's, the sale kept for the record (`Business.drawn`)."""
    fishery = getattr(vessel, "fishing", None)
    if fishery is None or not fishery.catch.lots:
        return None
    if market_factor(port.id) is None:
        return None
    total, _ = fishery.catch.value(port.id)
    record = {
        "port": port.id,
        "pounds": round(total, 2),
        "sold": _by_fish([lot for lot in fishery.catch.lots if not lot.spoiled]),
        "spoiled": _by_fish([lot for lot in fishery.catch.lots if lot.spoiled]),
        "tick": world.clock.tick,
    }
    fishery.catch.landed.append(record)
    fishery.catch.lots = []
    return record


# ---------------------------------------------------------------------------
# The far body's gear (the business's fisherman at far detail; truth 106)
# ---------------------------------------------------------------------------


def evolution_timing(evo_id: str) -> dict[str, float]:
    from freesail.evolutions import registry

    evo = registry.get(evo_id)
    return dict(getattr(evo, "timing", {}) or {}) if evo is not None else {}


def gear_for(fishery: Fishery, ground: Ground, when: datetime) -> str | None:
    """The kind of gear she works this ground with in this month: the first of the
    ground's gear in season that her file carries."""
    for kind in ground.gear_kinds():
        if fishery.carries(kind) is not None and ground.in_season(kind, when.month):
            return kind
    return None


def far_fishery(vessel: Any) -> Fishery | None:
    fishery = getattr(vessel, "fishing", None)
    if fishery is None:
        from freesail.ship.loader import load_ship

        try:
            spec = load_ship(vessel.ship_file).spec
        except Exception:  # noqa: BLE001 - a file that will not load fishes nothing
            return None
        fishery = Fishery.of_spec(spec)
        vessel.fishing = fishery
    return fishery


def ground_of_vessel(world: Any, vessel: Any) -> Ground | None:
    brain = getattr(vessel, "brain", None)
    intent = getattr(brain, "intent", None)
    if intent is not None and intent.kind == "fish":
        g = ground_named(world, intent.destination)
        if g is not None:
            return g
    return ground_at(world, vessel.position, slack=2.0)


def far_work(world: Any, vessel: Any, seconds: float) -> None:
    """A minute of the far fisherman's gear on her ground, by the same evolutions' times
    and the same catch function as the player's: shot when the gear fishes at the hour
    (`fishing_now`), fishing until the shot is full or the hour no longer serves, hauled,
    and the take struck below; nothing is a line of the player's log."""
    fishery = far_fishery(vessel)
    if fishery is None:
        return
    ground = ground_of_vessel(world, vessel)
    if ground is None:
        return
    when = world.clock.ship_time
    daylight = str(world.daylight)
    wind_kn = units.ms_to_knots(float(vessel._wind_at(world)[1]))
    out = fishery.out
    if out is not None and out.state == "hauling" and fishery.far_phase == "":
        # a haul begun at full detail and the ship demoted: the far body finishes it
        fishery.far_phase = "haul:"
        fishery.far_phase_s = 0.0
    if out is None and fishery.far_phase == "":
        kind = gear_for(fishery, ground, when)
        if kind is None or not fishing_now(ground, kind, when, daylight):
            return
        if wind_factor(kind, wind_kn) <= 0.0:
            return
        fishery.far_phase = f"shoot:{kind}"
        fishery.far_phase_s = 0.0
        return
    if fishery.far_phase.startswith("shoot:"):
        kind = fishery.far_phase.split(":", 1)[1]
        fishery.far_phase_s += seconds
        if fishery.far_phase_s >= _shoot_s(kind):
            g = fishery.carries(kind)
            fishery.out = GearOut(g.id, kind, g.name, ground.id, world.clock.tick)
            fishery.far_phase = ""
        return
    if fishery.far_phase.startswith("haul:"):
        fishery.far_phase_s += seconds
        if fishery.far_phase_s >= _haul_s(out.kind if out else "lines"):
            haul_into(world, fishery)
            fishery.far_phase = ""
        return
    if out is not None and out.state == "fishing":
        if not out.full():
            got = take(ground, out.kind, when, daylight, wind_kn, seconds)
            for fish, tons in got.items():
                out.taken[fish] = out.taken.get(fish, 0.0) + tons
        out.fished_s += seconds
        if should_haul(out, ground, when, daylight):
            out.state = "hauling"
            fishery.far_phase = "haul:"
            fishery.far_phase_s = 0.0


def should_haul(out: GearOut, ground: Ground, when: datetime, daylight: str) -> bool:
    """The gear is hauled when the shot is full, or when it has fished and the hour no
    longer serves (the night's nets at daybreak, the seine at dusk)."""
    if out.full():
        return True
    return out.fished_s > 0 and not fishing_now(ground, out.kind, when, daylight)


def _shoot_s(kind: str) -> float:
    return float(evolution_timing(evolution_of(kind, "shoot")).get("shoot_s", 900.0))


def _haul_s(kind: str) -> float:
    return float(evolution_timing(evolution_of(kind, "haul")).get("haul_s", 1800.0))


def trip_done_far(world: Any, vessel: Any) -> None:
    """Her hours on the ground done: the gear out hauled at once (its take struck
    below), so that she goes home with what she caught."""
    fishery = getattr(vessel, "fishing", None)
    if fishery is None:
        return
    if fishery.out is not None:
        haul_into(world, fishery)
    fishery.far_phase = ""
    fishery.far_phase_s = 0.0


def sail_allowed(fishery: Fishery | None, ship: Any, sail_id: str) -> str | None:
    """Why a sail may not be set while the gear is out (the gear's allowance), or None."""
    if fishery is None or fishery.out is None:
        return None
    allowed_words = gear_spec(fishery.out.kind).get("sails") or []
    allowed: set[str] = set()
    groups = getattr(ship, "groups", {}) or {}
    aliases = getattr(getattr(ship, "spec", None), "aliases", {}) or {}
    for w in allowed_words:
        w = str(w)
        if w in groups:
            allowed.update(groups[w])
        target = aliases.get(w)
        if target is not None:
            allowed.update(groups.get(target, [target]))
        if w in getattr(ship, "sails", {}):
            allowed.add(w)
    if sail_id in allowed:
        return None
    at = str(gear_spec(fishery.out.kind).get("at_it") or "at her gear")
    return (
        f"she is {at}; the {fishery.out.name.removeprefix('the ')} allows "
        f"{', '.join(str(w) for w in allowed_words) or 'no sail'} and no more. Haul "
        f"{fishery.out.name} first"
    )


def heading_words(deg: float) -> str:
    return units.point_name(math.radians(deg))


# ---------------------------------------------------------------------------
# The rules-based captain of a crewed fisherman (the fishermen promoted; spec M7b §21a)
# ---------------------------------------------------------------------------

# He shapes a course back for his ground when the ship has drawn this many of its radii
# from it with no gear out, once a glass at most (judgement).
BACK_TO_GROUND_RADII = 1.5
BACK_TO_GROUND_EVERY_S = 1800


def captain_work(captain: Any, p: Any) -> None:
    """A crewed fisherman's captain on his ground, once a minute (package 56): the trip's
    hours counted as the far brain counts them (one brain, two bodies); the gear the
    ground wants shot when it fishes at the hour, the ship hove to riding to it (the
    trawl towed under the sail she has), hauled when the shot is full or the hour no
    longer serves; and, the hours done, the gear hauled and the course home, as the far
    brain's `_fishing`. Every act an order through the channel (`Captain.give`); what he
    reads is his own ship's: the readings, his gear and his catch."""
    from freesail.world.captains import load_doctrine, plain_position

    world = captain.world
    intent = captain.intent
    fishery = getattr(world, "fishery", None)
    if intent is None or intent.kind != "fish" or fishery is None:
        return
    vessel = getattr(world, "vessel", None)
    brain = getattr(vessel, "brain", None) if vessel is not None else None
    b = brain._business if brain is not None else captain._business
    last = b.get("fishing_tick")
    b["fishing_s"] = float(b.get("fishing_s", 0.0)) + (
        0.0 if last is None else float(p.tick - int(last))
    )
    b["fishing_tick"] = p.tick
    runner = (getattr(world.ship, "extra", None) or {}).get("evolutions")
    gear_work = {e for pair in EVOLUTIONS.values() for e in pair}
    if any(i.evo.id in gear_work for i in getattr(runner, "instances", None) or ()):
        return  # the hands are at the gear
    out = fishery.out
    when = world.clock.ship_time
    daylight = str(world.daylight)
    if b["fishing_s"] >= float(intent.hours or 0.0) * 3600.0:
        if out is not None:
            captain.give("haul the gear", why="the trip's hours done")
            return
        ports = getattr(world, "ports", None)
        found = (
            ports.find(intent.origin)
            if ports is not None and getattr(ports, "ports", None)
            else None
        )
        name = found.name if found is not None else intent.origin
        captain.set_intent(f"run home to {name}")
        captain.role = "fisherman"
        captain.doctrine = load_doctrine("fisherman")
        return
    ground = ground_named(world, intent.destination) or ground_at(world, world.position, 2.0)
    if ground is None:
        return
    if out is None:
        mark = plain_position(ground.position)
        found = world.readings.value("distance_to", mark)
        nm = (
            float(found["metres"]) / units.NAUTICAL_MILE
            if isinstance(found, dict) and found.get("metres") is not None
            else 0.0
        )
        if nm > ground.radius_nm * BACK_TO_GROUND_RADII:
            if p.tick - int(b.get("back_to_ground", -(10**9))) >= BACK_TO_GROUND_EVERY_S:
                b["back_to_ground"] = p.tick
                if p.manoeuvre == "hove to":
                    captain.give("fill away", why="back to the ground")
                else:
                    captain.give(f"shape a course for {mark}", why="back to the ground")
            return
        kind = gear_for(fishery, ground, when)
        if kind is None or not fishing_now(ground, kind, when, daylight):
            return
        if wind_factor(kind, p.wind_kn) <= 0.0:
            return
        if b.get("shot_tried") == p.tick // 600:
            return  # once in ten minutes, if the order was refused
        b["shot_tried"] = p.tick // 600
        captain.give("shoot the gear", why=f"on {ground.name}")
        return
    if out.state != "fishing":
        return
    if should_haul(out, ground, when, daylight):
        captain.give("haul the gear", why="the shot fished")
        return
    if out.kind != "trawl" and p.manoeuvre not in ("hove to", "heaving to"):
        if b.get("hove_for") != out.shot_tick:
            b["hove_for"] = out.shot_tick
            captain.give("heave to", why=f"riding to {out.name}")


# The trawl's drag on her way, in newtons for a metre a second squared (judgement, set so
# that the smack under her plain sail in a moderate breeze tows at two to three knots, as
# Holdsworth's smacks towed "from half a knot to a knot and a half faster than the tide",
# pp. 77 to 78; docs/dev/TuningNotes.md, package 56). The other gear puts no drag on her:
# she rides to the nets or the lines hove to, and the seine is the boat's.
TRAWL_DRAG = 1200.0


def rig_gear_drag(world: Any, fishery: Fishery | None) -> None:
    """The trawl's drag on the ship while it is down (`physics.integrate` reads
    `ship.extra["gear_drag"]`), and none when it is up."""
    extra = getattr(getattr(world, "ship", None), "extra", None)
    if not isinstance(extra, dict):
        return
    if fishery is not None and fishery.out is not None and fishery.out.kind == "trawl":
        extra["gear_drag"] = TRAWL_DRAG
    else:
        extra.pop("gear_drag", None)
