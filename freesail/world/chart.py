"""The chart: the truth's sea under the keel and the shore about her (spec M5 §10, §11;
the study `docs/design/ChartData.md` §5.2, §5.5; package 32).

`data/charts/` holds what `tools/build_charts.py` wrote: a manifest naming the regions,
the levels and every source with its licence; depth tiles as int16 in the level's unit,
positive up and relative to the level's datum (lowest astronomical tide at the two finer
levels, mean sea level at the two coarser), with a distance-to-shore field and a per-tile
minimum depth at levels 2 and 3; the coast as polylines; the hand-made features and
overrides with their sources. This module reads it with numpy and pyyaml and nothing
else, and answers the four questions of C §1, each cheap:

- **depth here**: the finest level with a tile under the point, bilinear between the
  four nearest cell centres across tile edges, the tiles held in a small cache;
- **aground**: short-circuited by the tile's minimum depth against the draught, the
  highest tide of these waters and a margin (`AGROUND_HIGHEST_TIDE_M`, `AGROUND_MARGIN_M`),
  otherwise the keel's cells at bow and stern against the draught, the heel and the
  tide's height (0 until package 34 supplies it);
- **nearest coast**: the distance field and its gradient, a name from the features index;
- **in sight of what**: the features within the geographic horizon from the masthead by
  the 0.25° index, then by the visibility and the daylight, then by each feature's own
  rule: a light at night by its range and its date, a mark by day, a danger close-to.

**The world keeps the truth.** Nothing here is a reading in itself: `freesail.api.readings`
registers what the captain may ask (what is in sight, the land, the depth of water), and
`freesail.world.lookout` turns a sighting into the lookout's words by compass bearing and
an estimated distance. The truth tiles are never drawn: the browser's chart draws the
coast and the features (`freesail.api.queries.chart_block`).
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
import yaml

from freesail import units
from freesail.world.geo import Position, bearing_and_distance, horizon_nm

__all__ = [
    "AGROUND_HIGHEST_TIDE_M",
    "AGROUND_MARGIN_M",
    "CHARTS_DIR",
    "Chart",
    "ChartError",
    "CoastReading",
    "DANGER_SEEN_NM",
    "Feature",
    "Grounding",
    "NIGHT_LAND_NM",
    "Sighting",
    "TWILIGHT_FACTOR",
    "load_chart",
    "load_manifest",
]

CHARTS_DIR = Path(__file__).resolve().parents[2] / "data" / "charts"

# The grounding check's short-circuit (spec M5 §11; C §5.5): a tile whose shoalest
# sounding is deeper than the draught plus the highest tide plus a margin needs nothing
# more. The highest tide of these waters is Brest's spring range of about seven metres
# (T §1; the study's figures, to be pinned by package 34 with the tide); the margin is a
# judgement of two metres for the heel and the sea.
AGROUND_HIGHEST_TIDE_M = 7.0
AGROUND_MARGIN_M = 2.0

# What the lookout sees by the feature's own rule (spec §11, §12): a danger (a rock or a
# ledge above water) is made out within three miles by day, judgement; the land at night
# within a mile when the weather is clear, judgement (a dark coast close aboard); at
# twilight the marks are seen at half the day's range, judgement.
DANGER_SEEN_NM = 3.0
NIGHT_LAND_NM = 1.0
TWILIGHT_FACTOR = 0.5

# Default heights above the sea for the horizon where a feature gives none (metres):
# a headland a low cliff, a town its roofs, a rock its head at high water.
DEFAULT_HEIGHT_M: dict[str, float] = {
    "headland": 30.0,
    "island": 30.0,
    "hill": 100.0,
    "town": 15.0,
    "place": 10.0,
    "castle": 25.0,
    "tower": 20.0,
    "church": 25.0,
    "mill": 15.0,
    "beacon": 10.0,
    "mark": 10.0,
    "light": 20.0,
    "rock": 3.0,
    "ledge": 2.0,
    "drying": 1.0,
    "shoal": 0.0,
    "bank": 0.0,
    "anchorage": 0.0,
    "road": 0.0,
    "transit": 0.0,
    "bottom": 0.0,
}

# The kinds a lookout can raise: marks by day, lights by night, dangers close-to.
MARK_KINDS = frozenset(
    {
        "headland",
        "island",
        "hill",
        "town",
        "place",
        "castle",
        "tower",
        "church",
        "mill",
        "beacon",
        "mark",
        "light",
    }
)
LAND_KINDS = frozenset({"headland", "island", "hill", "town", "place"})
DANGER_KINDS = frozenset({"rock", "ledge", "drying"})


class ChartError(ValueError):
    """A chart that cannot be read, in words that name the file."""


def fathoms_words(depth_m: float) -> str:
    """A depth in the lead's words, to the half fathom: 'seven fathoms', 'two fathoms and
    a half', 'half a fathom'; 'dry at the datum' for a height above it."""
    fathoms = units.m_to_fathoms(depth_m)
    if fathoms < 0.0:
        return "dry at the datum"
    halves = round(fathoms * 2.0)
    whole, half = divmod(halves, 2)
    small = {
        1: "one",
        2: "two",
        3: "three",
        4: "four",
        5: "five",
        6: "six",
        7: "seven",
        8: "eight",
        9: "nine",
        10: "ten",
        11: "eleven",
        12: "twelve",
    }
    if whole == 0:
        return "half a fathom" if half else "no water"
    words = f"{small.get(whole, str(whole))} fathom{'s' if whole != 1 else ''}"
    return f"{words} and a half" if half else words


_fathoms_words = fathoms_words


# ---------------------------------------------------------------------------
# Features
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Feature:
    """A named thing of the coast (C §5.2): the period's name and the modern one, its
    position, its height above the sea for the horizon, its date if a light, the source
    cited in the references' form and the line the log can say."""

    id: str
    kind: str
    name: str
    lat_deg: float
    lon_deg: float
    modern: str = ""
    height_m: float | None = None
    extent_m: float = 0.0
    lit: dict[str, Any] | None = None  # {"from": year, "until": year|None, "range_nm", ...}
    source: str = ""
    says: str = ""
    view: str = ""
    marks: tuple[str, ...] = ()  # a transit's two marks
    bearing_deg: float | None = None  # a transit's bearing
    bottom: str = ""  # a bottom note's ground
    depth_fathoms: float | None = None  # a bank's or an anchorage's depth as the pilot gives it

    @property
    def position(self) -> Position:
        return Position(self.lat_deg, self.lon_deg)

    @property
    def height(self) -> float:
        if self.height_m is not None:
            return float(self.height_m)
        return DEFAULT_HEIGHT_M.get(self.kind, 10.0)

    def lit_in(self, year: int) -> bool:
        """Whether this light was lit in `year` (a light's date, so 1805 sees St Agnes
        and not the Bishop); False for anything but a light."""
        if self.kind != "light" or not self.lit:
            return False
        start = self.lit.get("from")
        end = self.lit.get("until")
        if start is not None and year < int(start):
            return False
        return end is None or year < int(end)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Feature:
        return cls(
            id=str(d["id"]),
            kind=str(d["kind"]),
            name=str(d["name"]),
            lat_deg=float(d["lat_deg"]),
            lon_deg=float(d["lon_deg"]),
            modern=str(d.get("modern", "")),
            height_m=None if d.get("height_m") is None else float(d["height_m"]),
            extent_m=float(d.get("extent_m", 0.0) or 0.0),
            lit=dict(d["lit"]) if d.get("lit") else None,
            source=str(d.get("source", "")),
            says=str(d.get("says", "")),
            view=str(d.get("view", "")),
            marks=tuple(str(m) for m in (d.get("marks") or ())),
            bearing_deg=None if d.get("bearing_deg") is None else float(d["bearing_deg"]),
            bottom=str(d.get("bottom", "")),
            depth_fathoms=None if d.get("depth_fathoms") is None else float(d["depth_fathoms"]),
        )

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {
            "id": self.id,
            "kind": self.kind,
            "name": self.name,
            "modern": self.modern,
            "lat_deg": self.lat_deg,
            "lon_deg": self.lon_deg,
            "height_m": self.height,
            "source": self.source,
            "says": self.says,
        }
        if self.lit:
            out["lit"] = dict(self.lit)
        if self.marks:
            out["marks"] = list(self.marks)
            out["bearing_deg"] = self.bearing_deg
        if self.bottom:
            out["bottom"] = self.bottom
        if self.depth_fathoms is not None:
            out["depth_fathoms"] = self.depth_fathoms
        if self.view:
            out["view"] = self.view
        return out


@dataclass(frozen=True)
class Sighting:
    """A feature in sight: its true bearing and its distance (the truth; the lookout
    estimates), and how it is seen ("light", "land", "mark" or "danger")."""

    feature: Feature
    bearing_deg: float
    distance_m: float
    seen_as: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.feature.id,
            "name": self.feature.name,
            "kind": self.feature.kind,
            "seen_as": self.seen_as,
            "bearing_deg": round(self.bearing_deg, 1),
            "distance_m": round(self.distance_m),
        }


@dataclass(frozen=True)
class CoastReading:
    """The nearest shore: how far, which way (degrees true, toward it) and, when the
    index has one, its name."""

    distance_m: float
    bearing_deg: float
    name: str | None = None
    feature_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "distance_m": round(self.distance_m),
            "bearing_deg": round(self.bearing_deg, 1),
            "name": self.name,
            "feature_id": self.feature_id,
        }


@dataclass(frozen=True)
class Grounding:
    """She has taken the ground (spec M5 §11, §18): the water under the keel where she
    touched, her draught there, which end, and the ground if a bottom note knows it."""

    depth_m: float
    draught_m: float
    where: str  # "forward", "aft" or "amidships"
    bottom: str = ""

    @property
    def words(self) -> str:
        """'She has taken the ground forward, on sand: two fathoms and a half of water by
        the chart, and she draws fifteen feet.'"""
        ground = f", on {self.bottom}" if self.bottom else ""
        feet = units.m_to_feet(self.draught_m)
        return (
            f"She has taken the ground {self.where}{ground}: "
            f"{_fathoms_words(max(0.0, self.depth_m))} of water by the chart, and she draws "
            f"{feet:.0f} feet."
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "depth_m": round(self.depth_m, 2),
            "draught_m": round(self.draught_m, 2),
            "where": self.where,
            "bottom": self.bottom,
        }


# ---------------------------------------------------------------------------
# Tiles and levels
# ---------------------------------------------------------------------------


@dataclass
class Tile:
    """One tile as the build wrote it: elevation int16 in `unit_m`, positive up, `nodata`
    where unknown; `dist` (levels 2 and 3) the distance to the shore in north-south
    cells; the shoalest sounding of the tile in metres (NaN where all land)."""

    level: int
    south_sec: int
    west_sec: int
    cell_sec: float
    unit_m: float
    nodata: int
    elevation: np.ndarray
    dist: np.ndarray | None
    min_depth_m: float

    @classmethod
    def load(cls, path: Path) -> Tile:
        with np.load(path) as z:
            elevation = z["elevation"]
            if "predictor" in z.files and int(z["predictor"]) == 2:
                # the build's horizontal differencing undone: int16 wraps exactly
                elevation = np.cumsum(elevation.view(np.uint16), axis=1, dtype=np.uint16).view(
                    np.int16
                )
            return cls(
                level=int(z["level"]),
                south_sec=int(z["south_sec"]),
                west_sec=int(z["west_sec"]),
                cell_sec=float(z["cell_sec"]),
                unit_m=float(z["unit_m"]),
                nodata=int(z["nodata"]),
                elevation=np.ascontiguousarray(elevation),
                dist=z["dist"] if "dist" in z.files else None,
                min_depth_m=float(z["min_depth_m"]),
            )

    @property
    def cells(self) -> int:
        return int(self.elevation.shape[0])


class Level:
    """One level's tiles under a folder, found by integer arithmetic on the position and
    held in a small cache once loaded."""

    def __init__(
        self,
        level: int,
        cell_sec: float,
        tile_cells: int,
        unit_m: float,
        folder: Path,
        names: set[str],
        cache_size: int = 16,
    ):
        self.level = level
        self.cell_sec = cell_sec
        self.tile_cells = tile_cells
        self.span_sec = cell_sec * tile_cells
        self.unit_m = unit_m
        self.folder = folder
        self.names = names  # the tiles the manifest lists
        self._cache: dict[tuple[int, int], Tile] = {}
        self._order: list[tuple[int, int]] = []
        self.cache_size = cache_size

    def corner_of_cell(self, row: int, col: int) -> tuple[int, int]:
        """The tile corner (south_sec, west_sec) holding the global cell (row, col)."""
        ty, tx = row // self.tile_cells, col // self.tile_cells
        return (
            int(round(-90 * 3600 + ty * self.span_sec)),
            int(round(-180 * 3600 + tx * self.span_sec)),
        )

    def global_cell(self, lat: float, lon: float) -> tuple[float, float]:
        """The fractional global cell row and column of a point (cell centres at .5)."""
        row = (lat + 90.0) * 3600.0 / self.cell_sec
        col = (lon + 180.0) * 3600.0 / self.cell_sec
        return row, col

    def tile(self, south_sec: int, west_sec: int) -> Tile | None:
        key = (south_sec, west_sec)
        t = self._cache.get(key)
        if t is not None:
            return t
        name = f"{south_sec}_{west_sec}"
        if name not in self.names:
            return None
        path = self.folder / f"{name}.npz"
        if not path.exists():
            return None
        t = Tile.load(path)
        self._cache[key] = t
        self._order.append(key)
        if len(self._order) > self.cache_size:
            old = self._order.pop(0)
            self._cache.pop(old, None)
        return t

    def tile_at(self, lat: float, lon: float) -> Tile | None:
        row, col = self.global_cell(lat, lon)
        return self.tile(*self.corner_of_cell(int(math.floor(row)), int(math.floor(col))))

    def has(self, lat: float, lon: float) -> bool:
        row, col = self.global_cell(lat, lon)
        s, w = self.corner_of_cell(int(math.floor(row)), int(math.floor(col)))
        return f"{s}_{w}" in self.names

    def value(self, row: int, col: int) -> float | None:
        """The elevation in metres at a global cell (row, col), None where unknown."""
        s, w = self.corner_of_cell(row, col)
        t = self.tile(s, w)
        if t is None:
            return None
        r = row - int(round((s + 90 * 3600) / self.cell_sec))
        c = col - int(round((w + 180 * 3600) / self.cell_sec))
        v = int(t.elevation[r, c])
        if v == t.nodata:
            return None
        return v * t.unit_m

    def elevation_at(self, lat: float, lon: float) -> float | None:
        """Bilinear between the four cell centres about a point, across tile edges; the
        nearest cell where a corner is unknown; None where all four are."""
        fr, fc = self.global_cell(lat, lon)
        fr -= 0.5
        fc -= 0.5
        r0, c0 = int(math.floor(fr)), int(math.floor(fc))
        wr, wc = fr - r0, fc - c0
        v00 = self.value(r0, c0)
        v01 = self.value(r0, c0 + 1)
        v10 = self.value(r0 + 1, c0)
        v11 = self.value(r0 + 1, c0 + 1)
        corners = (v00, v01, v10, v11)
        if all(v is not None for v in corners):
            return (
                v00 * (1 - wr) * (1 - wc)
                + v01 * (1 - wr) * wc
                + v10 * wr * (1 - wc)
                + v11 * wr * wc
            )
        nearest = self.value(int(round(fr)), int(round(fc)))
        if nearest is not None:
            return nearest
        for v in corners:
            if v is not None:
                return v
        return None

    def dist_at(self, lat: float, lon: float) -> tuple[float, float] | None:
        """The distance to the shore in metres and the bearing toward it, from the
        distance field and its gradient over the neighbouring cells; None without a
        field or a tile."""
        fr, fc = self.global_cell(lat, lon)
        r, c = int(math.floor(fr)), int(math.floor(fc))
        centre = self._dist_cell(r, c)
        if centre is None:
            return None
        cell_ns = self.cell_sec * units.NAUTICAL_MILE / 60.0
        cell_ew = cell_ns * math.cos(math.radians(lat))
        # the gradient by central differences, one cell either way, in the same units
        e = self._dist_cell(r, c + 1)
        w = self._dist_cell(r, c - 1)
        n = self._dist_cell(r + 1, c)
        s = self._dist_cell(r - 1, c)
        gx = ((e if e is not None else centre) - (w if w is not None else centre)) / 2.0
        gy = ((n if n is not None else centre) - (s if s is not None else centre)) / 2.0
        # the field grows away from the shore: the shore lies down the gradient
        dx, dy = -gx * cell_ns / cell_ew, -gy
        if dx == 0.0 and dy == 0.0:
            bearing = 0.0
        else:
            bearing = math.degrees(math.atan2(dx, dy)) % 360.0
        return centre * cell_ns, bearing

    def _dist_cell(self, row: int, col: int) -> float | None:
        s, w = self.corner_of_cell(row, col)
        t = self.tile(s, w)
        if t is None or t.dist is None:
            return None
        r = row - int(round((s + 90 * 3600) / self.cell_sec))
        c = col - int(round((w + 180 * 3600) / self.cell_sec))
        return float(t.dist[r, c])


# ---------------------------------------------------------------------------
# The chart
# ---------------------------------------------------------------------------


def load_manifest(root: Path = CHARTS_DIR) -> dict[str, Any]:
    path = root / "manifest.yaml"
    if not path.exists():
        raise ChartError(f"no chart data: {path} is missing (run tools/build_charts.py)")
    doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(doc, dict) or "regions" not in doc:
        raise ChartError(f"{path}: not a chart manifest")
    return doc


_CHARTS: dict[tuple[str, str], Chart] = {}


def load_chart(region: str, root: Path = CHARTS_DIR) -> Chart:
    """The chart of a region by its name in the manifest, shared between Worlds (the
    tiles are read-only; each World keeps its own position)."""
    key = (str(root), region)
    chart = _CHARTS.get(key)
    if chart is None:
        chart = Chart(region, load_manifest(root), root)
        _CHARTS[key] = chart
    return chart


class Chart:
    def __init__(self, region: str, manifest: dict[str, Any], root: Path = CHARTS_DIR):
        regions = manifest.get("regions") or {}
        if region not in regions:
            known = ", ".join(sorted(regions)) or "none"
            raise ChartError(f"no chart region named '{region}' (the manifest has: {known})")
        self.region = region
        self.manifest = manifest
        self.root = root
        self.spec = regions[region]
        b = self.spec["bounds"]
        self.bounds = (float(b["south"]), float(b["north"]), float(b["west"]), float(b["east"]))
        # the levels, finest first, with the tiles the manifest lists
        self.levels: list[Level] = []
        level_specs = manifest.get("levels") or {}
        listed: dict[int, set[str]] = {}
        for lv, tiles in (self.spec.get("tiles") or {}).items():
            listed[int(lv)] = {t["name"] for t in tiles}
        world = manifest.get("world")
        if world and world.get("tiles"):
            listed[int(world["level"])] = {t["name"] for t in world["tiles"]}
        atlantic = manifest.get("atlantic")
        if atlantic and atlantic.get("tiles"):
            names = {t["name"] for t in atlantic["tiles"]}
            folder = root / "tiles" / str(atlantic["level"])
            # the Atlantic is not committed: only the tiles actually present count
            listed[int(atlantic["level"])] = {n for n in names if (folder / f"{n}.npz").exists()}
        for lv in sorted(listed, reverse=True):
            spec = level_specs.get(str(lv)) or {}
            self.levels.append(
                Level(
                    lv,
                    float(spec.get("cell_sec")),
                    int(spec.get("tile_cells", 512)),
                    float(spec.get("unit_m", 1.0)),
                    root / "tiles" / str(lv),
                    listed[lv],
                )
            )
        # the features and their index
        self.features: dict[str, Feature] = {}
        fpath = root / self.spec["features"]
        if fpath.exists():
            doc = yaml.safe_load(fpath.read_text(encoding="utf-8")) or {}
            for d in doc.get("features") or []:
                f = Feature.from_dict(d)
                self.features[f.id] = f
        ipath = root / self.spec.get("index", "")
        if self.spec.get("index") and ipath.exists():
            idx = json.loads(ipath.read_text(encoding="utf-8"))
            self.index_cell_deg = float(idx.get("cell_deg", 0.25))
            self.index: dict[str, list[str]] = dict(idx.get("cells") or {})
        else:
            self.index_cell_deg = 0.25
            self.index = {}
            for f in self.features.values():
                self.index.setdefault(self._cell_key(f.lat_deg, f.lon_deg), []).append(f.id)
        self.coast_path = root / self.spec.get("coast", "")

    # -- geometry ---------------------------------------------------------------------

    def contains(self, pos: Position) -> bool:
        s, n, w, e = self.bounds
        return s <= pos.lat_deg <= n and w <= pos.lon_deg <= e

    def bounds_words(self) -> str:
        s, n, w, e = self.bounds
        return (
            f"{s:g} to {n:g} N, {abs(w):g} to {abs(e):g} W"
            if e <= 0
            else f"{s:g}-{n:g} N, {w:g}-{e:g} E"
        )

    def _cell_key(self, lat: float, lon: float) -> str:
        d = self.index_cell_deg
        return f"{math.floor(lat / d)},{math.floor(lon / d)}"

    def _finest_level(self, pos: Position) -> Level | None:
        for lv in self.levels:
            if lv.has(pos.lat_deg, pos.lon_deg):
                return lv
        return None

    # -- depth here (C §5.5) ------------------------------------------------------------

    def elevation_at(self, pos: Position) -> float | None:
        """The bed's height in metres above the datum (negative under water), from the
        finest level with a tile here; None where no level knows."""
        for lv in self.levels:
            if not lv.has(pos.lat_deg, pos.lon_deg):
                continue
            v = lv.elevation_at(pos.lat_deg, pos.lon_deg)
            if v is not None:
                return v
        return None

    def depth_at(self, pos: Position) -> float | None:
        """The depth of water at the datum in metres, positive down (negative for a
        height above it: the shore, a drying rock); None where the chart has nothing."""
        e = self.elevation_at(pos)
        return None if e is None else -e

    def tile_min_depth(self, pos: Position) -> float | None:
        """The shoalest sounding of the finest tile under the point (NaN-free: None
        where the tile is all land or there is none)."""
        lv = self._finest_level(pos)
        if lv is None:
            return None
        t = lv.tile_at(pos.lat_deg, pos.lon_deg)
        if t is None or math.isnan(t.min_depth_m):
            return None
        return t.min_depth_m

    # -- aground (spec §11) -------------------------------------------------------------

    def aground(
        self,
        pos: Position,
        heading_rad: float,
        length_m: float,
        draught_m: float,
        heel_rad: float,
        tide_m: float = 0.0,
        beam_m: float = 0.0,
    ) -> Grounding | None:
        """Whether the keel touches: the short-circuit first, then the keel's cells at bow
        and stern against the draught, the heel and the tide's height."""
        if draught_m <= 0.0:
            return None
        floor = self.tile_min_depth(pos)
        if floor is None:
            # all land, or no tile: only a point under the shore can touch
            e = self.elevation_at(pos)
            if e is None or -e - draught_m + tide_m >= 0.0:
                return None
        elif floor + tide_m > draught_m + AGROUND_HIGHEST_TIDE_M + AGROUND_MARGIN_M:
            return None
        # the heel dips the bilge: half the beam times the sine of the heel, judgement
        keel = draught_m + 0.5 * beam_m * abs(math.sin(heel_rad))
        half = 0.5 * length_m
        hx, hy = math.sin(heading_rad) * half, math.cos(heading_rad) * half
        places = (
            ("forward", pos.advanced(hx, hy)),
            ("aft", pos.advanced(-hx, -hy)),
            ("amidships", pos),
        )
        worst: tuple[str, float] | None = None
        for where, p in places:
            d = self.depth_at(p)
            if d is None:
                continue
            water = d + tide_m
            if water < keel and (worst is None or water < worst[1]):
                worst = (where, water)
        if worst is None:
            return None
        where, water = worst
        return Grounding(water, draught_m, where, self.bottom_near(pos))

    def bottom_near(self, pos: Position, within_m: float = 3000.0) -> str:
        """The ground from the nearest bottom note within `within_m`, or ''."""
        best = None
        for f in self.nearby(pos, within_m, {"bottom", "anchorage"}):
            if f.bottom:
                _, d = bearing_and_distance(pos, f.position)
                if best is None or d < best[0]:
                    best = (d, f.bottom)
        return best[1] if best else ""

    # -- nearest coast (C §5.5) ---------------------------------------------------------

    def coast_distance(self, pos: Position) -> tuple[float, float] | None:
        """The distance in metres and the bearing toward the nearest shore, from the
        distance field of the finest level that has one: the field's own read and its
        gradient, microseconds, which the weather's hook reads every tick."""
        for lv in self.levels:
            if not lv.has(pos.lat_deg, pos.lon_deg):
                continue
            found = lv.dist_at(pos.lat_deg, pos.lon_deg)
            if found is not None:
                return found
        return None

    def coast_at(self, pos: Position) -> CoastReading | None:
        """The nearest shore with a name from the index: the nearest headland, island
        or place within twice the distance (and at least a mile), preferring one that
        lies the way the shore lies. Read when the log wants a name, not every tick."""
        found = self.coast_distance(pos)
        if found is None:
            return None
        distance_m, bearing_deg = found
        name = None
        fid = None
        radius = max(2.0 * distance_m, units.NAUTICAL_MILE)
        best = None
        for f in self.nearby(pos, radius, LAND_KINDS):
            b, d = bearing_and_distance(pos, f.position)
            off = abs(units.wrap_pi(math.radians(b - bearing_deg)))
            score = d * (1.0 + off)
            if best is None or score < best[0]:
                best = (score, f)
        if best is not None:
            name, fid = best[1].name, best[1].id
        return CoastReading(distance_m, bearing_deg, name, fid)

    # -- features -------------------------------------------------------------------

    def feature(self, fid: str) -> Feature | None:
        return self.features.get(fid)

    def nearby(self, pos: Position, radius_m: float, kinds: Any = None) -> list[Feature]:
        """The features within `radius_m` by the index, of the given kinds (any if
        None), unsorted."""
        d = self.index_cell_deg
        dlat = radius_m / (60.0 * units.NAUTICAL_MILE)
        dlon = dlat / max(0.1, math.cos(math.radians(pos.lat_deg)))
        r0 = math.floor((pos.lat_deg - dlat) / d)
        r1 = math.floor((pos.lat_deg + dlat) / d)
        c0 = math.floor((pos.lon_deg - dlon) / d)
        c1 = math.floor((pos.lon_deg + dlon) / d)
        out: list[Feature] = []
        for r in range(r0, r1 + 1):
            for c in range(c0, c1 + 1):
                for fid in self.index.get(f"{r},{c}", ()):
                    f = self.features.get(fid)
                    if f is None or (kinds is not None and f.kind not in kinds):
                        continue
                    _, dist = bearing_and_distance(pos, f.position)
                    if dist <= radius_m:
                        out.append(f)
        return out

    # -- in sight of what (spec §11, §12) ---------------------------------------------

    def in_sight(
        self,
        pos: Position,
        height_of_eye_m: float,
        visibility_nm: float | None,
        daylight: str,
        when: datetime,
    ) -> list[Sighting]:
        """The features in sight from a height of eye: within the geographic horizon,
        within the weather's visibility, and by each feature's own rule; nearest first."""
        vis_nm = math.inf if visibility_nm is None else float(visibility_nm)
        eye_nm = horizon_nm(height_of_eye_m)
        # the farthest anything could be seen bounds the index search
        reach_nm = min(vis_nm, eye_nm + horizon_nm(0.0, 300.0))
        if daylight != "day":
            reach_nm = min(vis_nm, max(reach_nm, 30.0))
        out: list[Sighting] = []
        year = when.year
        for f in self.nearby(pos, reach_nm * units.NAUTICAL_MILE):
            seen_as = self._seen_as(f, daylight, year)
            if seen_as is None:
                continue
            bearing, distance = bearing_and_distance(pos, f.position)
            nm = distance / units.NAUTICAL_MILE
            limit = min(vis_nm, horizon_nm(height_of_eye_m, f.height))
            if seen_as == "light":
                rng = float((f.lit or {}).get("range_nm") or 0.0)
                limit = min(vis_nm, horizon_nm(height_of_eye_m, f.height), rng or math.inf)
            elif seen_as == "danger":
                limit = min(limit, DANGER_SEEN_NM)
            elif daylight == "twilight":
                limit = min(limit, max(NIGHT_LAND_NM, limit * TWILIGHT_FACTOR))
            elif daylight == "night":
                limit = min(limit, NIGHT_LAND_NM)
            if nm <= limit:
                out.append(Sighting(f, bearing, distance, seen_as))
        out.sort(key=lambda s: s.distance_m)
        return out

    @staticmethod
    def _seen_as(f: Feature, daylight: str, year: int) -> str | None:
        if f.kind == "light":
            if daylight != "day" and f.lit_in(year):
                return "light"
            # a tower not yet built is nothing; one built (lit or since put out) is a
            # mark by day
            built = f.lit and f.lit.get("from") is not None and year >= int(f.lit["from"])
            return "mark" if daylight == "day" and built else None
        if f.kind in DANGER_KINDS:
            return "danger" if daylight == "day" else None
        if f.kind in LAND_KINDS:
            return "land"
        if f.kind in MARK_KINDS:
            return "mark" if daylight != "night" else None
        return None

    # -- for the browser's chart (spec §17, the first half) ---------------------------

    def coast_lines(self) -> list[list[list[float]]]:
        """The coast as polylines of [lon, lat], as the build wrote them."""
        if not self.coast_path.exists():
            return []
        doc = json.loads(self.coast_path.read_text(encoding="utf-8"))
        return [f["geometry"]["coordinates"] for f in doc.get("features", [])]

    def attribution(self) -> str:
        return str(self.manifest.get("attribution", ""))


# keep the dataclass import used for future fields
_ = field
