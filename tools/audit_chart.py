"""The chart's audit (package 111): every block looked over on purpose, as the game reads it.

    python tools/audit_chart.py [--full] [--step DEG] [--known] [--check LETTERS]

The chart's builders each found a wart by chance (water that answers and that no region
owns, the Channel's tide in the Mediterranean, weather boxes that meet where the regions
do not, vessels sailing over the land); this tool looks for every such thing in every
block, through the game's own readers (`freesail/world/chart.py`, `tide.py`, the weather's
`load_climatology`, `ports.load_port`, `scenarios.load_scenario`) and nothing of its own
but the arithmetic of what it reports. It changes nothing. The checks, by letter:

(a) **water nobody owns**: the cells of a region's level-2 and level-3 tiles that are
    water and that no region's bounds hold (every cell of every tile that reaches past the
    bounds, read whole); and the bounds two regions both claim.
(b) **the seams**: within a region's bounds, water that no tile of level 2 or 3 answers
    (the corridor's thirty seconds alone, or nothing); and the coast's level-2 lines that
    end with tiles all about them and no other line to meet, across a seam or within a
    region.
(c) **the tide**: on a grid over each region's water, the gauges that answer and how far
    off the nearest is; water whose tide comes mostly from a gauge of another sea, or from
    beyond the reach (`interpolation.reach_nm`), and a level that is not its sea's (no
    gauge of the blend with a level read, the eleven's taken; or a Mediterranean level
    above `MED_LEVEL_MOST_M`).
(d) **the weather**: water that lies in no box of the climatology and takes the nearest,
    and a region whose water more than one box answers (the boxes' edges and the
    regions' parting).
(e) **the streams**: a region's water outside every box of `book_limits`, or with no
    statement of the directions within them, or with no stream area of the world's; and
    a stream area whose polygon holds no water.
(f) **the ports**: each port's road, anchorage and mooring on the water (or, where its
    file has it dry, on ground no higher than the file says) and its shore by the land;
    the depth the file gives against the chart's; each spot inside a region's bounds;
    its nations in the table and its dated rows whole; and **reachable**: a way
    in from open water to its anchorage and out again that crosses no land by the game's
    own test (`ships.land_crossing` over `ships.approach_plan` and the track to sea).
(g) **the marks**: a headland, town, light or other mark ashore standing in the water,
    a rock or shoal standing on the land, beyond the grid's reach of the shore
    (`MARK_REACH_CELLS`, a cable at the least), unless it stands on a rock or an island
    the features give; and a light with no years.
(h) **the scenarios**: each one's start inside its chart and on its water, and the ports
    it names present.

**The ratchet** (`data/charts/audit-known.yaml`): every finding of the first run listed by
its key, with its place, its reason in a line and whose it is; `tests/test_chart_audit.py`
passes on those and fails on any finding not listed (a sampled grid in the fast tier, the
full sweep in the slow), so that every later block comes in clean or says what it adds.
A finding's key names its check, its region or port and what it is, and not its count:
the count is the report's, and the known list's `most` is the full sweep's ceiling.

Figures marked JUDGEMENT are the audit's own choices of what counts as a finding.
"""

from __future__ import annotations

import argparse
import glob
import math
import sys
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from freesail import units  # noqa: E402
from freesail.world import tide as T  # noqa: E402
from freesail.world.chart import (  # noqa: E402
    CHARTS_DIR,
    Chart,
    Tile,
    chart_holding,
    load_chart,
    load_manifest,
)
from freesail.world.geo import Position, bearing_and_distance, destination  # noqa: E402
from freesail.world.weather import load_climatology  # noqa: E402

KNOWN_PATH = ROOT / "data" / "charts" / "audit-known.yaml"
PORTS_DIR = ROOT / "data" / "ports"
SCENARIOS_DIR = ROOT / "data" / "scenarios"
NATIONS_PATH = ROOT / "data" / "nations.yaml"
CHART_NAME = "atlantic-east"

# The grids (JUDGEMENT): the fast tier's sampled grid a quarter of a degree (some four
# thousand points over the regions' bounds, a few seconds); the slow tier's full sweep a
# twentieth, the grid the tiles' fill raise reads the tide on (`mean_level_grid`, package 93).
SAMPLED_STEP_DEG = 0.25
FULL_STEP_DEG = 0.05

# The seas a region's tide is of (JUDGEMENT, from the gauges' ranges as the constituents'
# file gives them: the Channel's and Biscay's and Portugal's metres, the islands' half
# metre, the Mediterranean's centimetres). A gauge's sea is its first block's; the eleven
# are the Channel's. The Strait meets both the Atlantic and the Mediterranean. Every region
# of the manifest and every tide region is named here, so that each new block names its sea
# as it comes in: a region the table lacks is a finding (`c-no-sea`), its water's tide not
# judged, never taken for a sea it is not of (the lead's word, package 111; package 112's
# seas will be its source later).
SEAS: dict[str, str] = {
    "channel-west": "atlantic",
    "channel-mid": "atlantic",
    "channel-east": "atlantic",
    "solent": "atlantic",
    "biscay-north": "atlantic",
    "biscay-south": "atlantic",
    "portugal": "atlantic",
    "strait": "strait",
    "madeira": "madeira",
    "azores": "azores",
    "mediterranean-west": "mediterranean",
    "balearics": "mediterranean",
    "gulf-of-lion": "mediterranean",
    "ligurian-sea": "mediterranean",
    "tyrrhenian": "mediterranean",
    "catalan-coast": "mediterranean",
    "sardinian-sea": "mediterranean",
    "tunis-coast": "mediterranean",
    "asinara-west": "mediterranean",
    # package 105: Sicily and Malta, and the two tide regions over its tiles' water that no
    # region's bounds hold
    "sicily": "mediterranean",
    "gulf-of-hammamet": "mediterranean",
    "calabria-north": "mediterranean",
    # package 106a: the Canaries and the Salvages, an ocean's tide of their own
    "canaries": "canaries",
    "salvages": "salvages",
}
MEDITERRANEAN = "mediterranean"
# The Salvages, between Madeira and the Canaries, are served by both groups' gauges (package
# 106a's ruling: Santa Cruz of Tenerife's and Funchal's).
SEAS_THAT_MEET = {
    "strait": {"atlantic", "mediterranean", "strait"},
    "salvages": {"madeira", "canaries", "salvages"},
}
# A share of the blend's weight from gauges of another sea above which the water's tide
# is called another sea's (JUDGEMENT: the larger part).
OTHER_SEA_SHARE = 0.5
# The Mediterranean's mean level above its datum is a few decimetres at every gauge read
# (Málaga's 0.43 m the most, the file's); a level above this over it is not its sea's
# (JUDGEMENT: twice the most read).
MED_LEVEL_MOST_M = 1.0

# A mark of the land standing in the water, or a danger on the land, within this many cells
# of the finest level from the other is the grid's grain and no finding (JUDGEMENT: a
# headland's point a cell or two off the grid's shore is what a sixteenth of a minute does).
MARK_REACH_CELLS = 3.0
# and never nearer than a cable, where the finest level is a harbour patch's half second
# (JUDGEMENT: a town or a castle given at its quay, a rock at its foot, is no finding)
MARK_REACH_LEAST_M = units.CABLE
SHORE_MARK_KINDS = frozenset(
    {"headland", "town", "light", "hill", "castle", "tower", "church", "mill"}
)
WATER_MARK_KINDS = frozenset({"rock", "ledge", "drying", "shoal", "bank"})
# A light whose name says it is a vessel's is afloat by her nature (the features give no
# other word for it; JUDGEMENT).
AFLOAT_LIGHT_WORDS = ("light-vessel", "lightvessel", "light vessel", "floating light")

# A port's shore spot afloat farther than this from the land is on the wrong side of the
# shore (JUDGEMENT: two cables, a boat's pull to the landing).
SHORE_AFLOAT_M = 2.0 * units.CABLE
# A spot's depth as the file gives it against the chart's (JUDGEMENT): a finding where the
# chart has less than half the file's figure and two fathoms less, or more than twice it
# and ten fathoms more (the period's soundings against the modern grid at its datum).
DEPTH_SHOAL_SHARE = 0.5
# A spot its file gives as drying (a negative depth: a harbour where she takes the ground)
# is a finding only where the grid's ground stands higher than the file's figure by more
# than this (JUDGEMENT: a metre, the grid's grain against a pilot's half fathom).
DRY_MARGIN_M = 1.0
DEPTH_SHOAL_M = units.fathoms_to_m(2.0)
DEPTH_DEEP_SHARE = 2.0
DEPTH_DEEP_M = units.fathoms_to_m(10.0)
# Open water for a port's way in (JUDGEMENT): a point this far out on one of sixteen
# bearings from the way's first mark, in water this deep, the line to it clear of the land.
OPEN_WATER_NM = 6.0
OPEN_WATER_DEPTH_M = 20.0

# A stream area's polygon tried for water on a grid of this many points a side over its
# box (JUDGEMENT).
AREA_GRID = 12

# A coast line's end that meets another within this many level-2 cells is met (JUDGEMENT).
COAST_MEET_CELLS = 1.5
# A level-2 tile's span, degrees: water nobody owns within this of another region's bounds
# is a sliver between the two, else open water beyond the region.
TILE_SPAN_DEG = 1536.0 / 3600.0
# The positions a finding names (the worst first).
WORST = 3

LETTERS = "abcdefgh"


@dataclass
class Finding:
    """One finding: its check's letter, its key (the ratchet's: the check, the region or
    the port, and what it is; never a count), where it is, how many cells or points, the
    words, and the worst positions."""

    check: str
    key: str
    region: str
    count: int
    words: str
    worst: list[str] = field(default_factory=list)

    def line(self) -> str:
        where = f" (worst: {'; '.join(self.worst)})" if self.worst else ""
        return f"[{self.check}] {self.key}: {self.words}; {self.count}{where}"


@dataclass
class Audit:
    findings: list[Finding] = field(default_factory=list)
    info: list[str] = field(default_factory=list)
    seconds: dict[str, float] = field(default_factory=dict)

    def add(self, f: Finding) -> None:
        self.findings.append(f)

    def keys(self) -> set[str]:
        return {f.key for f in self.findings}


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------


def fmt(lat: float, lon: float) -> str:
    """A position in the audit's words: degrees and minutes to the tenth."""

    def part(v: float, pos: str, neg: str) -> str:
        a = abs(v)
        d = int(a)
        m = (a - d) * 60.0
        if m >= 59.95:
            d, m = d + 1, 0.0
        return f"{d}°{m:04.1f}′{pos if v >= 0 else neg}"

    return f"{part(lat, 'N', 'S')} {part(lon, 'E', 'W')}"


def boxes_of(manifest: dict[str, Any]) -> dict[str, tuple[float, float, float, float]]:
    return {
        r: tuple(float(s["bounds"][k]) for k in ("south", "north", "west", "east"))
        for r, s in (manifest.get("regions") or {}).items()
    }


def in_box(lat: float, lon: float, b: tuple[float, float, float, float]) -> bool:
    return b[0] <= lat <= b[1] and b[2] <= lon <= b[3]


def sea_of(region: str) -> str | None:
    """The sea a region's tide is of, or None where `SEAS` does not name it."""
    return SEAS.get(region)


def grid_points(box: tuple[float, float, float, float], step: float) -> list[tuple[float, float]]:
    """The grid's points within a box, at the cells' centres of `step`, from its south-west
    corner, ordered by the level-2 tile they fall in (the tiles' cache holds sixteen)."""
    s, n, w, e = box
    rows = max(1, int(math.floor((n - s) / step + 1e-9)))
    cols = max(1, int(math.floor((e - w) / step + 1e-9)))
    pts = [(s + (i + 0.5) * step, w + (j + 0.5) * step) for i in range(rows) for j in range(cols)]
    span = 1536.0 / 3600.0
    pts.sort(key=lambda p: (math.floor(p[0] / span), math.floor(p[1] / span), p))
    return pts


def spread(cells: list[tuple[float, float, float]], n: int = WORST) -> list[tuple[float, float]]:
    """The worst `n` of (score, lat, lon), largest score first, a tenth of a degree apart."""
    out: list[tuple[float, float]] = []
    for _, lat, lon in sorted(cells, reverse=True):
        if all(abs(lat - a) + abs(lon - b) > 0.1 for a, b in out):
            out.append((lat, lon))
        if len(out) >= n:
            break
    return out


class Water:
    """The chart's water at a point, as the game reads it, cached by the point."""

    def __init__(self, chart: Chart):
        self.chart = chart
        self._elev: dict[tuple[float, float], float | None] = {}

    def elevation(self, lat: float, lon: float) -> float | None:
        key = (round(lat, 7), round(lon, 7))
        if key not in self._elev:
            self._elev[key] = self.chart.elevation_at(Position(lat, lon))
        return self._elev[key]

    def is_water(self, lat: float, lon: float) -> bool:
        e = self.elevation(lat, lon)
        return e is not None and e < 0.0


def finest_level(chart: Chart, lat: float, lon: float) -> Any:
    for lv in chart.levels:
        if lv.has(lat, lon):
            return lv
    return None


def distance_to(chart: Chart, pos: Position, land: bool, reach_m: float = 3000.0) -> float:
    """The distance in metres from a point to the nearest cell of the finest level under it
    that is land (`land` True) or known water (False), searched within `reach_m`; infinite
    when none is found there."""
    lv = finest_level(chart, pos.lat_deg, pos.lon_deg)
    if lv is None:
        return math.inf
    fr, fc = lv.global_cell(pos.lat_deg, pos.lon_deg)
    row, col = int(math.floor(fr)), int(math.floor(fc))
    cell_ns = lv.cell_m
    cell_ew = cell_ns * max(0.1, math.cos(math.radians(pos.lat_deg)))
    reach = int(math.ceil(reach_m / cell_ns)) + 1
    across = int(math.ceil(reach_m / cell_ew)) + 1
    r0, c0 = row - reach, col - across
    mask, _ = lv.land_window(r0, row + reach + 1, c0, col + across + 1)
    if not land:
        known = np.zeros_like(mask)
        n = lv.tile_cells
        for ty in range(r0 // n, (row + reach) // n + 1):
            for tx in range(c0 // n, (col + across) // n + 1):
                t = lv.tile(
                    int(round(-90 * 3600 + ty * lv.span_sec)),
                    int(round(-180 * 3600 + tx * lv.span_sec)),
                )
                if t is None:
                    continue
                a, b = max(r0, ty * n), min(row + reach + 1, (ty + 1) * n)
                c, d = max(c0, tx * n), min(col + across + 1, (tx + 1) * n)
                block = t.elevation[a - ty * n : b - ty * n, c - tx * n : d - tx * n]
                known[a - r0 : b - r0, c - c0 : d - c0] = (block <= 0) & (block != t.nodata)
        mask = known
    rr, cc = np.nonzero(mask)
    if not len(rr):
        return math.inf
    dy = (rr + (r0 + 0.5 - fr)) * cell_ns
    dx = (cc + (c0 + 0.5 - fc)) * cell_ew
    d = float(np.sqrt((dx * dx + dy * dy).min()))
    return d if d <= reach_m else math.inf


# ---------------------------------------------------------------------------
# (a) water nobody owns
# ---------------------------------------------------------------------------


def _side(cell_lat: np.ndarray, cell_lon: np.ndarray, box: tuple[float, ...]) -> np.ndarray:
    """Which side of its owner's bounds each cell lies beyond, as a word."""
    s, n, w, e = box
    ns = np.where(cell_lat > n, "north", np.where(cell_lat < s, "south", ""))
    ew = np.where(cell_lon > e, "east", np.where(cell_lon < w, "west", ""))
    out = np.char.add(ns.astype("U5"), np.where((ns != "") & (ew != ""), "-", ""))
    return np.char.add(out, ew.astype("U4"))


def check_unowned(
    audit: Audit, manifest: dict[str, Any], root: Path = CHARTS_DIR, tide: T.Tide | None = None
) -> None:
    boxes = boxes_of(manifest)
    levels = manifest.get("levels") or {}
    groups: dict[tuple[str, str], list[Any]] = {}
    for region, spec in (manifest.get("regions") or {}).items():
        own = boxes[region]
        for lv, tiles in (spec.get("tiles") or {}).items():
            cell = float(levels[str(lv)]["cell_sec"]) / 3600.0
            n = int(levels[str(lv)].get("tile_cells", 512))
            for t in tiles:
                s = int(t["south_sec"]) / 3600.0
                w = int(t["west_sec"]) / 3600.0
                nn, ee = s + n * cell, w + n * cell
                if any(
                    b[0] <= s and nn <= b[1] and b[2] <= w and ee <= b[3] for b in boxes.values()
                ):
                    continue  # the tile lies whole within one region's bounds
                lat = s + (np.arange(n) + 0.5) * cell
                lon = w + (np.arange(n) + 0.5) * cell
                owned = np.zeros((n, n), dtype=bool)
                for b in boxes.values():
                    la = (lat >= b[0]) & (lat <= b[1])
                    lo = (lon >= b[2]) & (lon <= b[3])
                    if la.any() and lo.any():
                        owned |= np.outer(la, lo)
                if owned.all():
                    continue
                tile = Tile.load(root / "tiles" / str(lv) / f"{t['name']}.npz")
                water = (tile.elevation < 0) & (tile.elevation != tile.nodata)
                bad = water & ~owned
                if not bad.any():
                    continue
                rr, cc = np.nonzero(bad)
                sides = _side(lat[rr], lon[cc], own)
                for side in np.unique(sides):
                    k = sides == side
                    la, lo = lat[rr[k]], lon[cc[k]]
                    beyond = np.maximum.reduce(
                        [
                            own[0] - la,
                            la - own[1],
                            (own[2] - lo) * np.cos(np.radians(la)),
                            (lo - own[3]) * np.cos(np.radians(la)),
                        ]
                    )
                    near = np.zeros(len(la), dtype=bool)
                    for other, b in boxes.items():
                        if other == region:
                            continue
                        dlat = np.maximum.reduce([b[0] - la, np.zeros_like(la), la - b[1]])
                        dlon = np.maximum.reduce([b[2] - lo, np.zeros_like(lo), lo - b[3]])
                        near |= np.maximum(dlat, dlon) <= TILE_SPAN_DEG
                    g = groups.setdefault(
                        (region, str(side) or "within"), [0, [], [9e9, -9e9, 9e9, -9e9], 0.0, 0]
                    )
                    g[4] += int(near.sum())
                    g[0] += int(k.sum())
                    g[3] += (
                        float(k.sum())
                        * (cell * 60.0) ** 2
                        * math.cos(math.radians(float(la.mean())))
                    )
                    top = np.argsort(beyond)[-WORST:]
                    g[1] += [(float(beyond[i]), float(la[i]), float(lo[i])) for i in top]
                    g[2] = [
                        min(g[2][0], float(la.min())),
                        max(g[2][1], float(la.max())),
                        min(g[2][2], float(lo.min())),
                        max(g[2][3], float(lo.max())),
                    ]
    for (region, side), (count, cells, ext, sq_nm, near) in sorted(groups.items()):
        others = [
            r
            for r, b in boxes.items()
            if r != region
            and b[0] - TILE_SPAN_DEG <= ext[1]
            and ext[0] <= b[1] + TILE_SPAN_DEG
            and b[2] - TILE_SPAN_DEG <= ext[3]
            and ext[2] <= b[3] + TILE_SPAN_DEG
        ]
        if near * 2 > count:
            beside = f", beside the bounds of {', '.join(sorted(others))}"
        else:
            beside = ", open water beyond it" + (
                f" ({100 * near // count}% of it within a tile of {', '.join(sorted(others))})"
                if near
                else ""
            )
        worst = spread(cells)
        answers = ""
        if tide is not None and worst:
            # what the tide is there: outside every block the eleven alone (package 89)
            g, nm = tide.nearest_gauge(Position(*worst[0]))
            m2 = tide.constants_at(Position(*worst[0]))[1]["M2"][0]
            answers = f"; its tide the eleven's, M2 {m2:.2f} m, the nearest {g.id} {nm:.0f} miles"
        audit.add(
            Finding(
                "a",
                f"a-unowned:{region}:{side}",
                region,
                count,
                f"water of {region}'s tiles {side} of its bounds that no region holds, "
                f"{sq_nm:.0f} square miles, {ext[0]:.3f} to {ext[1]:.3f} N and "
                f"{ext[2]:.3f} to {ext[3]:.3f} E{beside}{answers}",
                [fmt(a, b) for a, b in worst],
            )
        )


def check_overlaps(audit: Audit, manifest: dict[str, Any], water: Water, step: float) -> None:
    boxes = boxes_of(manifest)
    names = list(boxes)
    for i, a in enumerate(names):
        for b in names[i + 1 :]:
            A, B = boxes[a], boxes[b]
            s, n = max(A[0], B[0]), min(A[1], B[1])
            w, e = max(A[2], B[2]), min(A[3], B[3])
            if n - s <= 1e-9 or e - w <= 1e-9:
                continue  # apart, or abutting on an edge
            pts = grid_points((s, n, w, e), min(step, (n - s) / 2, (e - w) / 2))
            wet = [(lat, lon) for lat, lon in pts if water.is_water(lat, lon)]
            audit.add(
                Finding(
                    "a",
                    f"a-overlap:{a}+{b}",
                    a,
                    len(wet),
                    f"the bounds of {a} and {b} both claim {s:g} to {n:g} N and {w:g} to {e:g} E "
                    f"(the first in the chart's order answers `region_at` there)",
                    [fmt(*p) for p in wet[:WORST]],
                )
            )


# ---------------------------------------------------------------------------
# (b) the seams
# ---------------------------------------------------------------------------


def check_untiled(audit: Audit, chart: Chart, water: Water, step: float) -> None:
    """Water within a region's bounds that no level-2 or level-3 tile answers."""
    for region in chart.regions:
        box = chart.region_bounds[region]
        coarse: list[tuple[float, float, float]] = []
        nothing: list[tuple[float, float, float]] = []
        for lat, lon in grid_points(box, step):
            lv = finest_level(chart, lat, lon)
            if lv is not None and lv.level >= 2:
                continue
            if lv is None:
                nothing.append((0.0, lat, lon))
            elif water.is_water(lat, lon):
                coarse.append((-float(water.elevation(lat, lon) or 0.0), lat, lon))
        if coarse:
            audit.add(
                Finding(
                    "b",
                    f"b-coarse:{region}",
                    region,
                    len(coarse),
                    f"water within {region}'s bounds that no tile of the region answers, "
                    "the corridor's thirty seconds alone",
                    [fmt(a, b) for a, b in spread(coarse)],
                )
            )
        if nothing:
            audit.add(
                Finding(
                    "b",
                    f"b-nothing:{region}",
                    region,
                    len(nothing),
                    f"points within {region}'s bounds where the chart answers nothing at all",
                    [fmt(a, b) for a, b in spread(nothing)],
                )
            )


def check_coast(audit: Audit, chart: Chart) -> None:
    """The coast's level-2 lines whose ends meet no other line's, with tiles all about."""
    lv2 = next((lv for lv in chart.levels if lv.level == 2), None)
    if lv2 is None:
        return
    import json

    ends: list[tuple[float, float, str]] = []
    for region, path in zip(chart.regions, chart.coast_paths, strict=False):
        if not path.exists():
            continue
        doc = json.loads(path.read_text(encoding="utf-8"))
        for f in doc.get("features") or []:
            if int((f.get("properties") or {}).get("level", 2)) != 2:
                continue
            coords = f["geometry"]["coordinates"]
            if len(coords) < 2 or coords[0] == coords[-1]:
                continue  # a ring closes on itself
            for lon, lat in (coords[0], coords[-1]):
                ends.append((float(lat), float(lon), region))
    if not ends:
        return
    cell = lv2.cell_sec / 3600.0
    tol = COAST_MEET_CELLS * cell
    pts = np.array([(a, b) for a, b, _ in ends])
    order = np.lexsort((pts[:, 1], pts[:, 0]))
    met = np.zeros(len(ends), dtype=bool)
    sorted_lat = pts[order, 0]
    for i in order:
        lo = np.searchsorted(sorted_lat, pts[i, 0] - tol, "left")
        hi = np.searchsorted(sorted_lat, pts[i, 0] + tol, "right")
        cand = order[lo:hi]
        cand = cand[cand != i]
        if (
            len(cand)
            and (
                np.abs(pts[cand, 1] - pts[i, 1])
                <= tol / max(0.1, math.cos(math.radians(pts[i, 0])))
            ).any()
        ):
            met[i] = True
    region_of_tile: dict[str, str] = {}
    for r in chart.regions:
        for t in (chart.region_specs[r].get("tiles") or {}).get("2", []) or (
            chart.region_specs[r].get("tiles") or {}
        ).get(2, []):
            region_of_tile.setdefault(str(t["name"]), r)
    groups: dict[str, list[tuple[float, float, float]]] = defaultdict(list)
    for i in np.nonzero(~met)[0]:
        lat, lon, region = ends[int(i)]
        about = [
            (lat + dy * 2 * cell, lon + dx * 2 * cell) for dy in (-1, 0, 1) for dx in (-1, 0, 1)
        ]
        if not all(lv2.has(a, b) for a, b in about):
            continue  # at the edge of the level's tiles: nothing beyond to meet
        owners = set()
        for a, b in about:
            row, col = lv2.global_cell(a, b)
            s, w = lv2.corner_of_cell(int(math.floor(row)), int(math.floor(col)))
            owners.add(region_of_tile.get(f"{s}_{w}", region))
        across = sorted(owners - {region})
        key = f"b-coast:{region}" + (f"/{across[0]}" if across else "")
        groups[key].append((0.0, lat, lon))
    for key, cells in sorted(groups.items()):
        region = key.split(":", 1)[1].split("/")[0]
        across = key.split("/")[1] if "/" in key else ""
        where = f"across the seam with {across}" if across else f"within {region}'s tiles"
        audit.add(
            Finding(
                "b",
                key,
                region,
                len(cells),
                f"ends of {region}'s coast lines that meet no other line, {where}",
                [fmt(a, b) for a, b in spread([(-i, a, b) for i, (_, a, b) in enumerate(cells)])],
            )
        )


# ---------------------------------------------------------------------------
# (c) the tide
# ---------------------------------------------------------------------------


def check_tide(audit: Audit, chart: Chart, tide: T.Tide, water: Water, step: float) -> None:
    gauge_sea: dict[str, str] = {}
    for g in tide.gauges:
        gauge_sea[g.id] = "atlantic"
    unnamed: dict[str, list[str]] = defaultdict(list)
    for g in tide.block_gauges:
        sea_g = sea_of(g.blocks[0])
        if sea_g is None:
            unnamed[g.blocks[0]].append(g.id)
        gauge_sea[g.id] = sea_g or f"(no sea named: {g.blocks[0]})"
    for block, ids in sorted(unnamed.items()):
        if block not in chart.regions:
            audit.add(
                Finding(
                    "c",
                    f"c-no-sea:{block}",
                    block,
                    len(ids),
                    f"the tide region {block}, whose gauges are {', '.join(ids)}, names no "
                    "sea in the audit's table of seas (`SEAS`): its gauges' sea is not judged",
                )
            )
    for region in chart.regions:
        sea = sea_of(region)
        if sea is None:
            audit.add(
                Finding(
                    "c",
                    f"c-no-sea:{region}",
                    region,
                    1,
                    f"{region} names no sea in the audit's table of seas (`SEAS`): its "
                    "tide is not judged until the block names its sea",
                )
            )
            continue
        accept = SEAS_THAT_MEET.get(sea, {sea})
        far: list[tuple[float, float, float]] = []
        other: list[tuple[float, float, float]] = []
        level_not: list[tuple[float, float, float]] = []
        answering: dict[str, int] = defaultdict(int)
        nearest_most = 0.0
        points = 0
        for lat, lon in grid_points(chart.region_bounds[region], step):
            if not water.is_water(lat, lon):
                continue
            points += 1
            pos = Position(lat, lon)
            level, consts, nearest_nm, is_far = tide.constants_about(pos)
            centre = Position(
                (math.floor(lat / T.CONSTANTS_CELL_DEG) + 0.5) * T.CONSTANTS_CELL_DEG,
                (math.floor(lon / T.CONSTANTS_CELL_DEG) + 0.5) * T.CONSTANTS_CELL_DEG,
            )
            gauges = tide.gauges_at(centre)
            dist = [bearing_and_distance(centre, g.position)[1] for g in gauges]
            within = [(g, d) for g, d in zip(gauges, dist, strict=True) if d <= tide.reach_m]
            if not within:
                within = [min(zip(gauges, dist, strict=True), key=lambda x: x[1])]
            weights = [(g, 1.0 / max(d, T.GAUGE_FLOOR_M) ** tide.power) for g, d in within]
            total = sum(w for _, w in weights)
            alien = sum(w for g, w in weights if gauge_sea[g.id] not in accept) / total
            nearest_g = min(within, key=lambda x: x[1])[0]
            answering[nearest_g.id] += 1
            nearest_most = max(nearest_most, nearest_nm)
            if is_far:
                far.append((nearest_nm, lat, lon))
            if alien > OTHER_SEA_SHARE:
                other.append((alien, lat, lon))
            levelled = any(g.mean_level_m is not None for g, _ in within)
            if not levelled and sea != "atlantic":
                level_not.append((level, lat, lon))
            elif sea == MEDITERRANEAN and level > MED_LEVEL_MOST_M:
                level_not.append((level, lat, lon))
        if points:
            names = ", ".join(f"{g} {n}" for g, n in sorted(answering.items(), key=lambda x: -x[1]))
            audit.info.append(
                f"(c) {region}: {points} water points; the nearest gauge answering: {names}; "
                f"the farthest water from its nearest gauge {nearest_most:.0f} miles"
            )
        for key, cells, words in (
            ("far", far, "water beyond the reach of every gauge that serves it, the nearest alone"),
            ("other-sea", other, f"water whose tide is mostly gauges of another sea than {sea}'s"),
            (
                "level",
                level_not,
                f"water whose mean level is not {sea}'s (no gauge of the blend with its level "
                f"read, or above {MED_LEVEL_MOST_M:g} m in the Mediterranean)",
            ),
        ):
            if cells:
                audit.add(
                    Finding(
                        "c",
                        f"c-{key}:{region}",
                        region,
                        len(cells),
                        f"{words} ({max(c[0] for c in cells):.2f} at the worst)",
                        [fmt(a, b) for a, b in spread(cells)],
                    )
                )


# ---------------------------------------------------------------------------
# (d) the weather
# ---------------------------------------------------------------------------


def check_weather(audit: Audit, chart: Chart, climatology: Any, water: Water, step: float) -> None:
    for region in chart.regions:
        none: list[tuple[float, float, float]] = []
        boxes: dict[str, int] = defaultdict(int)
        points = 0
        for lat, lon in grid_points(chart.region_bounds[region], step):
            if not water.is_water(lat, lon):
                continue
            points += 1
            box = climatology.box_at(lat, lon)
            boxes[box.name] += 1
            if not box.contains(lat, lon):
                none.append((box.distance_deg(lat, lon), lat, lon))
        if none:
            nearest = sorted({climatology.box_at(a, b).name for _, a, b in none})
            audit.add(
                Finding(
                    "d",
                    f"d-no-box:{region}",
                    region,
                    len(none),
                    f"water of {region} in no box of the climatology, taking the nearest "
                    f"({', '.join(nearest)})",
                    [fmt(a, b) for a, b in spread(none)],
                )
            )
        if len(boxes) > 1 and points:
            shares = ", ".join(
                f"{b} {100.0 * n / points:.0f}%"
                for b, n in sorted(boxes.items(), key=lambda x: -x[1])
            )
            audit.add(
                Finding(
                    "d",
                    f"d-split:{region}",
                    region,
                    points,
                    f"{region}'s water answered by more than one box: {shares}",
                )
            )


# ---------------------------------------------------------------------------
# (e) the streams
# ---------------------------------------------------------------------------


def check_streams(
    audit: Audit, chart: Chart, tide: T.Tide, directions: T.Directions, water: Water, step: float
) -> None:
    for region in chart.regions:
        no_book: list[tuple[float, float, float]] = []
        no_statement: list[tuple[float, float, float]] = []
        no_stream: list[tuple[float, float, float]] = []
        for lat, lon in grid_points(chart.region_bounds[region], step):
            if not water.is_water(lat, lon):
                continue
            pos = Position(lat, lon)
            inside = any(
                s <= lat <= n and w <= lon <= e
                for s, n, w, e in (directions.boxes or (directions.limits,))
            )
            if not inside:
                no_book.append((0.0, lat, lon))
            elif directions.area_at(pos) is None:
                no_statement.append((0.0, lat, lon))
            if tide.area_at(pos) is T.NO_STREAM:
                no_stream.append((0.0, lat, lon))
        for key, cells, words in (
            (
                "no-book",
                no_book,
                f"water of {region} outside every box of the directions' `book_limits`",
            ),
            (
                "no-statement",
                no_statement,
                f"water of {region} within the directions' limits with no statement",
            ),
            ("no-stream", no_stream, f"water of {region} in no stream area of the world's"),
        ):
            if cells:
                audit.add(
                    Finding(
                        "e",
                        f"e-{key}:{region}",
                        region,
                        len(cells),
                        words,
                        [
                            fmt(a, b)
                            for a, b in spread([(-i, a, b) for i, (_, a, b) in enumerate(cells)])
                        ],
                    )
                )
    for area in tide.areas:
        if area.polygon is None:
            continue
        lats = [p[0] for p in area.polygon]
        lons = [p[1] for p in area.polygon]
        s, n, w, e = min(lats), max(lats), min(lons), max(lons)
        inner = []
        for i in range(AREA_GRID):
            for j in range(AREA_GRID):
                lat = s + (i + 0.5) * (n - s) / AREA_GRID
                lon = w + (j + 0.5) * (e - w) / AREA_GRID
                if T._point_in_polygon(lat, lon, area.polygon):
                    inner.append((lat, lon))
        wet = sum(1 for lat, lon in inner if water.is_water(lat, lon))
        if inner and wet == 0:
            audit.add(
                Finding(
                    "e",
                    f"e-area-land:{area.id}",
                    area.chart,
                    len(inner),
                    f"the stream area {area.id} holds no water at any of its {len(inner)} points",
                    [fmt(*inner[len(inner) // 2])],
                )
            )


# ---------------------------------------------------------------------------
# (f) the ports
# ---------------------------------------------------------------------------


def _open_water_from(chart: Chart, water: Water, p: Position) -> bool:
    """Whether open water lies within `OPEN_WATER_NM` of a point by a straight line clear of
    the land, on one of sixteen bearings."""
    from freesail.world.ships import land_crossing

    world = SimpleNamespace(chart=chart)
    for k in range(16):
        q = destination(p, 22.5 * k, OPEN_WATER_NM * units.NAUTICAL_MILE)
        e = water.elevation(q.lat_deg, q.lon_deg)
        if e is None or -e < OPEN_WATER_DEPTH_M:
            continue
        if not land_crossing(world, p, [("to", q, "the offing")]):
            return True
    return False


def _crossing_point(chart: Chart, start: Position, plan: list[tuple[Any, ...]]) -> Position | None:
    """Where the first leg the land guard refuses meets the land: `ships.land_crossing`'s
    own test, leg by leg, for the point (the guard says only the leg)."""
    a = start
    for leg in plan:
        if len(leg) < 2 or not isinstance(leg[1], Position):
            continue
        try:
            hit = chart.line_shore(
                a, leg[1], units.CABLE, skip_start_m=units.CABLE, skip_end_m=units.CABLE
            )
        except Exception:  # noqa: BLE001 - as the guard: beyond the chart's field
            hit = None
        if hit is not None and hit[2]:
            return hit[1]
        a = leg[1]
    return None


def _dated_rows(nations: tuple[dict[str, Any], ...]) -> list[str]:
    """What is not whole in a port's dated rows: a row whose dates run backward, two rows
    that overlap, a day between two rows that no row holds, a row with no source."""
    faults = []
    for row in nations:
        if row.get("since") and row.get("until") and row["since"] > row["until"]:
            faults.append(f"{row['nation']}'s row ends before it begins")
        if not str(row.get("source") or "").strip():
            faults.append(f"{row['nation']}'s row gives no source")
    rows = sorted(nations, key=lambda r: r.get("since") or date.min)
    for a, b in zip(rows, rows[1:], strict=False):
        end = a.get("until")
        start = b.get("since")
        if end is None or start is None:
            faults.append(f"{a['nation']}'s row and {b['nation']}'s overlap (an open end)")
        elif start <= end:
            faults.append(f"{a['nation']}'s row and {b['nation']}'s overlap")
        elif (start - end).days > 1:
            faults.append(f"no row holds {end} to {start}")
    return faults


def check_ports(
    audit: Audit,
    chart: Chart,
    water: Water,
    ports_dir: Path = PORTS_DIR,
    nations_path: Path = NATIONS_PATH,
) -> None:
    from freesail.world.ports import load_port
    from freesail.world.ships import approach_plan, land_crossing

    table = yaml.safe_load(nations_path.read_text(encoding="utf-8")) or {}
    known_nations = set((table.get("nations") or {}).keys())
    world = SimpleNamespace(chart=chart, dealings=None)
    harbour_boxes: dict[str, list[tuple[float, float, float, float]]] = {
        r: [
            tuple(float(b[k]) for k in ("south", "north", "west", "east"))
            for b in (chart.region_specs[r].get("harbours") or {}).values()
        ]
        for r in chart.regions
    }
    for path in sorted(ports_dir.glob("*.yaml")):
        pid = path.stem
        try:
            port = load_port(path, chart)
        except Exception as e:  # noqa: BLE001 - said as a finding
            audit.add(Finding("f", f"f-load:{pid}", "", 1, f"the port file does not load: {e}"))
            continue
        home = chart.region_at(port.anchorage.position) or ""
        for which in ("outer_road", "anchorage", "mooring", "shore"):
            spot = getattr(port, which)
            p = spot.position
            e = water.elevation(p.lat_deg, p.lon_deg)
            where = fmt(p.lat_deg, p.lon_deg)
            sw = which.replace("_", " ")
            if which != "shore":
                if e is None:
                    audit.add(
                        Finding(
                            "f",
                            f"f-off-chart:{pid}:{which}",
                            home,
                            1,
                            f"{port.name}'s {sw} lies where the chart answers nothing",
                            [where],
                        )
                    )
                    continue
                dries_m = -spot.depth_m if spot.depth_m is not None and spot.depth_m < 0 else None
                if dries_m is not None and e <= dries_m + DRY_MARGIN_M:
                    pass  # a drying harbour by its file, and the grid's ground no higher
                elif e >= 0.0:
                    to_water = distance_to(chart, p, land=False)
                    audit.add(
                        Finding(
                            "f",
                            f"f-dry:{pid}:{which}",
                            home,
                            1,
                            f"{port.name}'s {sw} stands on ground {e:.1f} m above the datum"
                            + (f" where its file has it dry {dries_m:.1f} m" if dries_m else "")
                            + f", {to_water:.0f} m from the nearest water",
                            [where],
                        )
                    )
                elif spot.depth_m is not None:
                    chart_m = -e
                    file_m = spot.depth_m
                    if (
                        chart_m < DEPTH_SHOAL_SHARE * file_m and chart_m < file_m - DEPTH_SHOAL_M
                    ) or (chart_m > DEPTH_DEEP_SHARE * file_m and chart_m > file_m + DEPTH_DEEP_M):
                        audit.add(
                            Finding(
                                "f",
                                f"f-depth:{pid}:{which}",
                                home,
                                1,
                                f"{port.name}'s {sw}: the file gives "
                                f"{units.m_to_fathoms(file_m):.0f} fathoms, the chart "
                                f"{units.m_to_fathoms(chart_m):.1f}",
                                [where],
                            )
                        )
            else:
                if e is not None and e < 0.0:
                    off = chart.nearest_shore(p)
                    d = off.distance_m if off is not None else math.inf
                    if d > SHORE_AFLOAT_M:
                        audit.add(
                            Finding(
                                "f",
                                f"f-shore-afloat:{pid}",
                                home,
                                1,
                                f"{port.name}'s shore lies in {-e:.1f} m of water, "
                                f"{d:.0f} m from the land",
                                [where],
                            )
                        )
            region = chart.region_of.get(spot.feature_id) if spot.feature_id else None
            if region is not None:
                if not in_box(p.lat_deg, p.lon_deg, chart.region_bounds[region]) and not any(
                    in_box(p.lat_deg, p.lon_deg, b) for b in harbour_boxes[region]
                ):
                    audit.add(
                        Finding(
                            "f",
                            f"f-region:{pid}:{which}",
                            region,
                            1,
                            f"{port.name}'s {sw} (the feature {spot.feature_id} of "
                            f"{region}'s file) lies outside {region}'s bounds and harbours "
                            f"(in {chart.region_at(p) or 'no region'})",
                            [where],
                        )
                    )
            elif chart.region_at(p) is None:
                audit.add(
                    Finding(
                        "f",
                        f"f-region:{pid}:{which}",
                        home,
                        1,
                        f"{port.name}'s {sw} lies inside no region's bounds",
                        [where],
                    )
                )
        names = {port.nation} | {str(r["nation"]) for r in port.nations}
        if port.blockade:
            names.add(str(port.blockade.get("by") or ""))
        names |= set(port.closed_to)
        for nation in sorted(n for n in names if n and n not in known_nations):
            audit.add(
                Finding(
                    "f",
                    f"f-nation:{pid}:{nation}",
                    home,
                    1,
                    f"{port.name} names the nation '{nation}', which the nations' table has not",
                )
            )
        for fault in _dated_rows(port.nations):
            audit.add(
                Finding("f", f"f-dated:{pid}", home, 1, f"{port.name}'s dated nations: {fault}")
            )
        # reachable: in from open water by the way the business plans, and out by its track
        try:
            plan = approach_plan(world, port)
        except Exception as e:  # noqa: BLE001
            audit.add(
                Finding("f", f"f-in:{pid}", home, 1, f"{port.name}'s way in cannot be planned: {e}")
            )
            continue
        first = plan[0][1]
        from_sea = (
            "its track from the sea" if port.tracks.get("from_sea") else "no track; its outer road"
        )
        if not _open_water_from(chart, water, first):
            audit.add(
                Finding(
                    "f",
                    f"f-open:{pid}",
                    home,
                    1,
                    f"{port.name}'s way in begins where no open water lies within "
                    f"{OPEN_WATER_NM:g} miles by a line clear of the land "
                    f"({from_sea})",
                    [fmt(first.lat_deg, first.lon_deg)],
                )
            )
        crossing = land_crossing(world, first, plan[1:])
        if crossing:
            hit = _crossing_point(chart, first, plan[1:])
            audit.add(
                Finding(
                    "f",
                    f"f-in:{pid}",
                    home,
                    1,
                    f"{port.name}'s way in from the sea {crossing} "
                    f"({'by its tracks' if port.tracks else 'no tracks'})",
                    [fmt(hit.lat_deg, hit.lon_deg)] if hit else [],
                )
            )
        from freesail.world.brains import _plan_of_legs
        from freesail.world.captains import Planner

        out = _plan_of_legs(Planner(world)._port_track(port, "to_sea")) or [
            ("to", port.outer_road.position, port.outer_road.name)
        ]
        to_sea = (
            "by its track to sea" if port.tracks.get("to_sea") else "no track; to its outer road"
        )
        crossing = land_crossing(world, port.anchorage.position, out)
        if crossing:
            hit = _crossing_point(chart, port.anchorage.position, out)
            audit.add(
                Finding(
                    "f",
                    f"f-out:{pid}",
                    home,
                    1,
                    f"{port.name}'s way out from its anchorage {crossing} ({to_sea})",
                    [fmt(hit.lat_deg, hit.lon_deg)] if hit else [],
                )
            )


# ---------------------------------------------------------------------------
# (g) the marks
# ---------------------------------------------------------------------------


def _on_charted_ground(chart: Chart, f: Any, reach_m: float) -> bool:
    """Whether a mark stands on ground the features give (a rock, a ledge, a drying head or
    an island the grid lacks) within that ground's extent, or the grid's reach, of it."""
    for g in chart.features.values():
        # every feature, not the index's (an index not rebuilt from its file lacks some)
        if abs(g.lat_deg - f.lat_deg) > 0.03 or abs(g.lon_deg - f.lon_deg) > 0.05:
            continue
        if g.id == f.id or not (g.is_ground or g.kind == "island"):
            continue
        if bearing_and_distance(f.position, g.position)[1] <= max(g.extent_m, reach_m):
            return True
    return False


def check_marks(audit: Audit, chart: Chart, water: Water) -> None:
    for fid, f in sorted(chart.features.items()):
        region = chart.region_of.get(fid, "")
        if f.kind == "light" and (not f.lit or f.lit.get("from") is None):
            audit.add(
                Finding(
                    "g", f"g-light-undated:{fid}", region, 1, f"the light {f.name} has no years"
                )
            )
        if f.kind not in SHORE_MARK_KINDS and f.kind not in WATER_MARK_KINDS:
            continue
        e = water.elevation(f.lat_deg, f.lon_deg)
        if e is None:
            audit.add(
                Finding(
                    "g",
                    f"g-off-chart:{fid}",
                    region,
                    1,
                    f"the {f.kind} {f.name} lies where the chart answers nothing",
                    [fmt(f.lat_deg, f.lon_deg)],
                )
            )
            continue
        lv = finest_level(chart, f.lat_deg, f.lon_deg)
        reach = max(MARK_REACH_CELLS * lv.cell_m, MARK_REACH_LEAST_M)
        if f.kind in SHORE_MARK_KINDS and e < 0.0:
            if f.kind == "light" and any(w in f.name.lower() for w in AFLOAT_LIGHT_WORDS):
                continue  # a light-vessel is afloat by her nature
            if _on_charted_ground(chart, f, reach):
                continue  # on a rock or an island the features give, which the grid lacks
            d = distance_to(chart, f.position, land=True)
            if d > reach:
                audit.add(
                    Finding(
                        "g",
                        f"g-afloat:{fid}",
                        region,
                        1,
                        f"the {f.kind} {f.name} stands in {-e:.1f} m of water, "
                        f"{'beyond 3 km' if math.isinf(d) else f'{d:.0f} m'} from the grid's land",
                        [fmt(f.lat_deg, f.lon_deg)],
                    )
                )
        elif f.kind in WATER_MARK_KINDS and e > 0.0:
            d = distance_to(chart, f.position, land=False)
            if d > reach:
                audit.add(
                    Finding(
                        "g",
                        f"g-ashore:{fid}",
                        region,
                        1,
                        f"the {f.kind} {f.name} lies on ground {e:.1f} m above the datum, "
                        f"{'beyond 3 km' if math.isinf(d) else f'{d:.0f} m'} from the grid's water",
                        [fmt(f.lat_deg, f.lon_deg)],
                    )
                )


# ---------------------------------------------------------------------------
# (h) the scenarios
# ---------------------------------------------------------------------------


def check_scenarios(
    audit: Audit, scenarios_dir: Path = SCENARIOS_DIR, ports_dir: Path = PORTS_DIR
) -> None:
    from freesail.world.scenarios import load_scenario

    port_ids = {p.stem for p in ports_dir.glob("*.yaml")}
    holding: dict[str, str] = {}
    for path in sorted(glob.glob(str(scenarios_dir / "**" / "*.yaml"), recursive=True)):
        name = Path(path).relative_to(scenarios_dir).with_suffix("").as_posix()
        try:
            sf = load_scenario(path)
        except Exception as e:  # noqa: BLE001
            audit.add(Finding("h", f"h-load:{name}", "", 1, f"the scenario does not load: {e}"))
            continue
        sc = sf.scenario if hasattr(sf, "scenario") else sf
        ports = sc.ports if isinstance(sc.ports, list) else list((sc.ports or {}).keys())
        for pid in sorted(set(ports) - port_ids):
            audit.add(
                Finding(
                    "h",
                    f"h-port:{name}:{pid}",
                    "",
                    1,
                    f"the scenario names the port '{pid}', which has no file",
                )
            )
        if not (sc.chart or sc.region) or not sc.position:
            continue
        # as the World reads it: `chart:` a chart outright, else the chart holding `region:`
        if not sc.chart and sc.region not in holding:
            holding[sc.region] = chart_holding(sc.region)
        where = sc.chart or holding[sc.region]
        try:
            chart = load_chart(where)
        except Exception as e:  # noqa: BLE001
            audit.add(
                Finding(
                    "h",
                    f"h-chart:{name}",
                    "",
                    1,
                    f"the scenario's chart '{where}' does not load: {e}",
                )
            )
            continue
        p = Position(float(sc.position["lat_deg"]), float(sc.position["lon_deg"]))
        if not chart.contains(p):
            audit.add(
                Finding(
                    "h",
                    f"h-outside:{name}",
                    "",
                    1,
                    f"the scenario starts outside its chart {chart.name}",
                    [fmt(p.lat_deg, p.lon_deg)],
                )
            )
            continue
        e = chart.elevation_at(p)
        there = (
            "where the chart answers nothing"
            if e is None
            else f"on ground {e:.1f} m above the datum"
        )
        if e is None or e >= 0.0:
            audit.add(
                Finding(
                    "h",
                    f"h-dry:{name}",
                    chart.region_at(p) or "",
                    1,
                    f"the scenario starts {there}",
                    [fmt(p.lat_deg, p.lon_deg)],
                )
            )


# ---------------------------------------------------------------------------
# The whole
# ---------------------------------------------------------------------------


def run(step: float = SAMPLED_STEP_DEG, letters: str = LETTERS) -> Audit:
    """The audit of the trunk's chart at the grid `step` (degrees), over the checks
    `letters`."""
    audit = Audit()
    manifest = load_manifest()
    chart = load_chart(CHART_NAME)
    water = Water(chart)

    def timed(name: str, fn: Any, *args: Any) -> None:
        t0 = time.perf_counter()
        fn(*args)
        audit.seconds[name] = audit.seconds.get(name, 0.0) + time.perf_counter() - t0

    tide = T.load_tide()
    if "a" in letters:
        timed("a", check_unowned, audit, manifest, CHARTS_DIR, tide)
        timed("a", check_overlaps, audit, manifest, water, step)
    if "b" in letters:
        timed("b", check_untiled, audit, chart, water, step)
        timed("b", check_coast, audit, chart)
    if "c" in letters:
        timed("c", check_tide, audit, chart, tide, water, step)
    if "d" in letters:
        timed("d", check_weather, audit, chart, load_climatology(), water, step)
    if "e" in letters:
        timed("e", check_streams, audit, chart, tide, T.load_directions(), water, step)
    if "f" in letters:
        timed("f", check_ports, audit, chart, water)
    if "g" in letters:
        timed("g", check_marks, audit, chart, water)
    if "h" in letters:
        timed("h", check_scenarios, audit)
    return audit


def load_known(path: Path = KNOWN_PATH) -> dict[str, dict[str, Any]]:
    """The known list: each finding owned by its key, with its place, its reason in a line,
    whose it is and the full sweep's ceiling on its count (`most`)."""
    doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    out: dict[str, dict[str, Any]] = {}
    for entry in doc.get("known") or []:
        out[str(entry["key"])] = dict(entry)
    return out


def unlisted(audit: Audit, known: dict[str, dict[str, Any]]) -> list[Finding]:
    return [f for f in audit.findings if f.key not in known]


def over_ceiling(audit: Audit, known: dict[str, dict[str, Any]]) -> list[Finding]:
    return [
        f
        for f in audit.findings
        if f.key in known
        and known[f.key].get("most") is not None
        and f.count > int(known[f.key]["most"])
    ]


def report(audit: Audit, known: dict[str, dict[str, Any]] | None = None) -> str:
    lines = []
    by_region: dict[str, list[Finding]] = defaultdict(list)
    for f in audit.findings:
        by_region[f.region or "(the files)"].append(f)
    for region in sorted(by_region):
        lines.append(f"== {region}")
        for f in sorted(by_region[region], key=lambda f: (f.check, f.key)):
            mark = ""
            if known is not None:
                mark = "  " if f.key in known else "! "
            lines.append(f"{mark}{f.line()}")
    lines.append("== what answers")
    lines += audit.info
    lines.append(
        "== seconds: " + ", ".join(f"({k}) {v:.1f}" for k, v in sorted(audit.seconds.items()))
    )
    counts: dict[str, int] = defaultdict(int)
    for f in audit.findings:
        counts[f.check] += 1
    lines.append("== findings by check: " + ", ".join(f"({k}) {counts[k]}" for k in LETTERS))
    return "\n".join(lines)


def known_entries(audit: Audit) -> list[dict[str, Any]]:
    """The findings as the known list's entries, for its first writing by hand: the key,
    the place, the count as `most`; the reason and the owner are the writer's."""
    return [
        {"key": f.key, "place": f.worst[0] if f.worst else f.region, "most": f.count}
        for f in sorted(audit.findings, key=lambda f: f.key)
    ]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--full", action="store_true", help="the full sweep (the slow tier's grid)")
    ap.add_argument("--step", type=float, default=None, help="the grid in degrees")
    ap.add_argument("--check", default=LETTERS, help="the checks by letter (abcdefgh)")
    ap.add_argument(
        "--known", action="store_true", help="mark the findings the known list lacks with !"
    )
    ap.add_argument(
        "--entries", action="store_true", help="print the findings as known-list entries"
    )
    args = ap.parse_args(argv)
    step = args.step or (FULL_STEP_DEG if args.full else SAMPLED_STEP_DEG)
    audit = run(step, args.check)
    if args.entries:
        print(yaml.safe_dump(known_entries(audit), sort_keys=False, allow_unicode=True, width=200))
        return 0
    known = load_known() if args.known else None
    print(report(audit, known))
    if known is not None:
        new = unlisted(audit, known)
        print(f"== {len(new)} finding(s) the known list lacks")
        return 1 if new else 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
