"""Build the chart data of `data/charts/` from the open sources and the hand-made period
files (spec M5 §10; the study `docs/design/ChartData.md` §5.4; package 32).

    python tools/build_charts.py [--cache DIR] [--region channel-west] [--world]
                                 [--atlantic] [--skip-fetch] [--report FILE]

Run by a developer, never by the game. The steps, as the study lists them:

1. **Fetch** each source of the region's recipe into a cache outside the repository
   (`--cache`, default `.cache/charts` under the repository root, which git ignores),
   recording the URL, the date and the checksum for the manifest, and refusing any
   source whose licence is not in `ALLOWED_LICENCES` (public domain, CC BY, Licence
   Ouverte, OGL, LGPL, and named per-source permissions; ODbL is not in the list).
   GEBCO_2025's area extract comes from GEBCO's grid subsetting application by its
   queue API; GEBCO's eight global GeoTIFF tiles from CEDA's archive; EMODnet's DTM 2024
   by its ERDDAP service as classic netCDF subsets.
2. **Resample** to the level grids with numpy alone (no GDAL or rasterio is installed on
   the build machine; the readers for ESRI ASCII, classic netCDF and plain TIFF are
   below): EMODnet (elevation relative to lowest astronomical tide) for level 2 and the
   coast, GEBCO (relative to mean sea level) for levels 0 and 1 and under everything.
3. **Overrides**: rasterise each period polygon at levels 2 and 3 with its depth turned
   to metres below chart datum by the sheet's unit and datum, and splice the period
   shoreline where an override says so (Plymouth without the breakwater; Falmouth
   without the docks). Where an override and the modern grid disagree in open water by
   more than `OVERRIDE_TOLERANCE_M`, the place is printed.
4. **Derive** the distance-to-shore field (a chamfer transform of the land mask at levels
   2 and 3), a per-tile minimum depth, and the 0.25° feature index.
5. **Write** the tiles, the coast, the manifest with the attribution block the game shows
   in its about text, and a report.

The tiles are `tiles/<level>/<south_sec>_<west_sec>.npz`, named by their south-west
corner in integer arc-seconds (an integer at every level, since a tile's span is 512
cells of a whole or half arc-second), so the game finds a tile by integer arithmetic on
the position (C §5.5). Each holds `elevation` as int16 in the level's unit (decimetres
at levels 2 and 3; metres at levels 0 and 1, where the abyss is beyond an int16 of
decimetres), positive up and relative to the level's datum, `NODATA` where unknown, and
at levels 2 and 3 `dist`, the distance to the nearest shore in north-south cells as
uint16. The runtime reads them with numpy and nothing else (`freesail/world/chart.py`).
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import math
import re
import struct
import sys
import time
import urllib.request
import zipfile
import zlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[1]
CHARTS_DIR = ROOT / "data" / "charts"
DEFAULT_CACHE = ROOT / ".cache" / "charts"
LICENCE_DIR = ROOT / "docs" / "references" / "licences"

# The levels (C §5.2): the cell in arc-seconds, and the unit the int16 holds.
LEVELS: dict[int, dict[str, Any]] = {
    # The world in two-metre steps with its land clipped at fifty metres above the sea:
    # the picture of the globe keeps its coast and loses its mountains, and the level's
    # 153 tiles compress to about 26 MB instead of 40 (measured; the study's "about 25").
    0: {
        "cell_sec": 150.0,
        "unit_m": 2.0,
        "land_clip_m": 50.0,
        "use": "the world's picture and coarse depth",
    },
    1: {"cell_sec": 30.0, "unit_m": 1.0, "use": "the Atlantic: passages and landfalls"},
    2: {"cell_sec": 3.0, "unit_m": 0.1, "use": "a region: coast and approaches"},
    3: {"cell_sec": 0.5, "unit_m": 0.1, "use": "harbour patches"},
}
TILE = 512
NODATA = -32768
# The nautical mile as a minute of arc: the metres in a second of latitude (freesail.units).
M_PER_SEC_LAT = 1852.0 / 60.0

# Where an override and the modern grid disagree in open water by more than this, the
# tool prints the place (C §5.4 step 3): a real change or a misread fathom.
OVERRIDE_TOLERANCE_M = 3.0

FATHOM_M = 1.8288  # six feet of 0.3048 m
# The brasse of the Dépôt de la Marine: five pieds du roi of 0.3248 m (C §3.3, marked
# unverified there: 1.624 m; the sheet's own legend is read when a French override is
# built, and the override records the unit it used).
BRASSE_M = 1.624
UNIT_M = {"metres": 1.0, "m": 1.0, "fathoms": FATHOM_M, "feet": 0.3048, "brasses": BRASSE_M}

# ---------------------------------------------------------------------------
# Sources and licences (C §2, §6)
# ---------------------------------------------------------------------------

# Licence ids the tiles may carry (C §5.4 step 1). The text of each is kept under
# docs/references/licences/ and named in the manifest. Not here, on purpose: ODbL.
ALLOWED_LICENCES: dict[str, str] = {
    "public-domain": "public domain",
    "CC-BY-4.0": "Creative Commons Attribution 4.0 International",
    "Licence-Ouverte-2.0": "Licence Ouverte / Open Licence 2.0 (Etalab)",
    "OGL-3.0": "Open Government Licence v3.0",
    "LGPL-3.0": "GNU Lesser General Public License v3.0",
    "SHOM-IGN-Histolitt": "SHOM-IGN Histolitt conditions (named per-source permission)",
}

SOURCES: dict[str, dict[str, Any]] = {
    "gebco_2025": {
        "name": "GEBCO_2025 Grid",
        "licence": "public-domain",
        "licence_text": "docs/references/licences/gebco-terms-of-use.md",
        "attribution": (
            "GEBCO Compilation Group (2025) GEBCO 2025 Grid "
            "(doi:10.5285/37c52e96-24ea-67ce-e063-7086abc05f29)"
        ),
        "datum": "mean sea level",
        "home": "https://www.gebco.net/data-products/gridded-bathymetry-data/gebco2025-grid",
        "used_for": ["level 0 (the world)", "level 1 (the Atlantic)", "the land under level 2"],
    },
    "emodnet_dtm_2024": {
        "name": "EMODnet Bathymetry DTM 2024",
        "licence": "CC-BY-4.0",
        "licence_text": "docs/references/licences/cc-by-4.0.txt",
        "attribution": (
            "EMODnet Bathymetry Consortium (2024): EMODnet Digital Bathymetry (DTM 2024), "
            "https://doi.org/10.12770/cf51df64-56f9-4a99-b1aa-36b8d7b743a1. "
            "Do not use for navigation."
        ),
        "datum": "lowest astronomical tide",
        "home": "https://emodnet.ec.europa.eu/en/emodnet-bathymetry-dtm-2024-release",
        "used_for": ["level 2 (the region's depth and coast)", "level 3 (the harbour patches)"],
    },
    "shom_homonim": {
        "name": "SHOM MNT bathymétrique de façade Atlantique (projet HOMONIM), 100 m",
        "licence": "Licence-Ouverte-2.0",
        "licence_text": "docs/references/licences/licence-ouverte-2.0.md",
        "attribution": (
            "Shom, MNT bathymétrique de façade Atlantique (projet HOMONIM), Licence Ouverte 2.0"
        ),
        "datum": "lowest astronomical tide (the PBMA package) or mean sea level (the NM package)",
        "home": "https://www.data.gouv.fr/en/datasets/mnt-bathymetrique-de-facade-atlantique-projet-homonim-1",
        "used_for": ["the French cross-check (not fetched in this build: see the manifest)"],
    },
    "histolitt": {
        "name": "SHOM-IGN Histolitt coastline",
        "licence": "SHOM-IGN-Histolitt",
        "licence_text": "docs/references/licences/shom-ign-histolitt.md",
        "attribution": "© IGN-Shom 2009",
        "datum": "highest astronomical tide (the shoreline)",
        "home": "https://www.data.gouv.fr/fr/datasets/shom-ign-trait-de-cote-histolitt-r",
        "used_for": [
            "the French shoreline where needed (not fetched in this build: see the manifest)"
        ],
    },
}

# ---------------------------------------------------------------------------
# The regions' recipes
# ---------------------------------------------------------------------------

REGIONS: dict[str, dict[str, Any]] = {
    "channel-west": {
        "title": "The western Channel and the Western Approaches, Falmouth to Ushant",
        "bounds": {"south": 48.0, "north": 51.0, "west": -7.0, "east": -3.0},
        # the EMODnet subset fetched: the tiles that meet the bounds, whole
        "fetch": {"south": 47.75, "north": 51.25, "west": -7.30, "east": -2.50},
        # the level-3 harbour patches (C §5.2: 15' x 15' each), as tile groups
        "harbours": {
            "falmouth-helford": {"south": 50.02, "north": 50.27, "west": -5.22, "east": -4.90},
            "plymouth-cawsand": {"south": 50.28, "north": 50.42, "west": -4.28, "east": -4.05},
            "scilly": {"south": 49.85, "north": 49.99, "west": -6.42, "east": -6.22},
            "brest-iroise": {"south": 48.25, "north": 48.42, "west": -4.85, "east": -4.40},
        },
    },
}

WORLD = {"level": 0, "south": -90.0, "north": 90.0, "west": -180.0, "east": 180.0}
ATLANTIC = {"level": 1, "south": -60.0, "north": 70.0, "west": -100.0, "east": 20.0}

GEBCO_APP = "https://download.gebco.net"
GEBCO_ZIP_URL = (
    "https://dap.ceda.ac.uk/bodc/gebco/global/gebco_2025/ice_surface_elevation/geotiff/"
    "gebco_2025_geotiff.zip"
)
EMODNET_ERDDAP = "https://erddap.emodnet.eu/erddap/griddap/bathymetry_dtm_2024.nc"


# ---------------------------------------------------------------------------
# Fetching
# ---------------------------------------------------------------------------


@dataclass
class Fetched:
    path: Path
    url: str
    retrieved: str
    sha256: str
    bytes: int

    def record(self) -> dict[str, Any]:
        return {
            "url": self.url,
            "retrieved": self.retrieved,
            "sha256": self.sha256,
            "bytes": self.bytes,
            "file": self.path.name,
        }


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()


def _today() -> str:
    return dt.date.today().isoformat()


def fetch_url(url: str, path: Path, skip: bool, log: Any) -> Fetched:
    """Fetch `url` to `path` unless it is cached (or `skip` says not to fetch at all)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    stamp = path.with_suffix(path.suffix + ".fetched")
    if path.exists() and path.stat().st_size > 0:
        retrieved = stamp.read_text().strip() if stamp.exists() else _today()
        log(f"  cached: {path.name} ({path.stat().st_size:,} bytes)")
    elif skip:
        raise SystemExit(f"--skip-fetch and {path.name} is not in the cache; fetch it first")
    else:
        log(f"  fetching {url}")
        t0 = time.time()
        req = urllib.request.Request(url, headers={"User-Agent": "FreeSail chart build (urllib)"})
        with urllib.request.urlopen(req, timeout=600) as r, open(path, "wb") as f:
            while True:
                chunk = r.read(1 << 22)
                if not chunk:
                    break
                f.write(chunk)
        retrieved = _today()
        stamp.write_text(retrieved)
        log(f"  {path.stat().st_size:,} bytes in {time.time() - t0:.0f} s")
    return Fetched(path, url, retrieved, sha256_of(path), path.stat().st_size)


def fetch_gebco_extract(box: dict[str, float], cache: Path, skip: bool, log: Any) -> Fetched:
    """GEBCO's area extract in ESRI ASCII from the subsetting app's queue API (read from
    the app's client script: POST /api/queue with a basket, poll /api/queue/status, GET
    /api/queue/download)."""
    name = f"gebco_2025_s{box['south']}_n{box['north']}_w{box['west']}_e{box['east']}_ascii.zip"
    path = cache / "gebco" / name
    url = f"{GEBCO_APP}/api/queue (gebco_2025_global, ascii, {box})"
    if path.exists() and path.stat().st_size > 0:
        return fetch_url(url, path, skip, log)
    if skip:
        raise SystemExit(f"--skip-fetch and {name} is not in the cache")
    log(f"  asking {GEBCO_APP} for the extract {box}")
    grids = _get_json(f"{GEBCO_APP}/api/grids")
    formats = _get_json(f"{GEBCO_APP}/api/formats")
    grid = next(g for g in grids if g["name"] == "gebco_2025_global")
    source = next(s for s in grid["data_sources"] if s["name"] == "gebco_2025")
    fmt = next(f for f in formats if f["name"] == "ascii")
    basket = {
        "id": "0",
        "email": None,
        "submission_date": dt.datetime.now().isoformat(timespec="seconds"),
        "processing_status": "new",
        "items": [
            {
                "id": 0,
                "grid_id": grid["id"],
                "data_source_ids": [source["id"]],
                "formats": [fmt["id"]],
                "left": box["west"],
                "right": box["east"],
                "top": box["north"],
                "bottom": box["south"],
            }
        ],
    }
    req = urllib.request.Request(
        f"{GEBCO_APP}/api/queue",
        data=json.dumps(basket).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        basket_id = json.load(r)["basketId"]
    t0 = time.time()
    while True:
        status = _get_json(f"{GEBCO_APP}/api/queue/status/{basket_id}")
        if status.get("status") == "finished":
            break
        if status.get("error"):
            raise SystemExit(f"GEBCO's queue refused the extract: {status}")
        if time.time() - t0 > 1800:
            raise SystemExit("GEBCO's queue did not finish in half an hour")
        time.sleep(10)
    return fetch_url(f"{GEBCO_APP}/api/queue/download/{basket_id}", path, skip, log)


def _get_json(url: str) -> Any:
    with urllib.request.urlopen(url, timeout=120) as r:
        return json.load(r)


def fetch_emodnet(var: str, box: dict[str, float], cache: Path, skip: bool, log: Any) -> Fetched:
    """A classic-netCDF subset of EMODnet's DTM 2024 from its ERDDAP griddap service."""
    name = (
        f"emodnet_dtm2024_{var}_{box['south']:.2f}_{box['north']:.2f}_"
        f"{box['west']:.2f}_{box['east']:.2f}.nc"
    )
    url = (
        f"{EMODNET_ERDDAP}?{var}%5B({box['south']}):({box['north']})%5D"
        f"%5B({box['west']}):({box['east']})%5D"
    )
    return fetch_url(url, cache / "emodnet" / name, skip, log)


# ---------------------------------------------------------------------------
# Readers: ESRI ASCII, classic netCDF, plain TIFF
# ---------------------------------------------------------------------------


@dataclass
class Grid:
    """A regular grid of cell-centred values: `south`/`west` are the outer corner in
    degrees, `cell` the cell in degrees, `values` rows south to north (row 0 is the
    southernmost), columns west to east; NaN where unknown."""

    south: float
    west: float
    cell: float
    values: np.ndarray  # float32, rows south-north

    @property
    def rows(self) -> int:
        return self.values.shape[0]

    @property
    def cols(self) -> int:
        return self.values.shape[1]

    @property
    def north(self) -> float:
        return self.south + self.rows * self.cell

    @property
    def east(self) -> float:
        return self.west + self.cols * self.cell

    def sample(self, lats: np.ndarray, lons: np.ndarray) -> np.ndarray:
        """Bilinear values at the cell-centre coordinates `lats` (a vector, south to
        north) x `lons` (a vector), separably; NaN outside the grid or where a corner is
        unknown. Returns an array of shape (len(lats), len(lons))."""
        fr = (lats - self.south) / self.cell - 0.5
        fc = (lons - self.west) / self.cell - 0.5
        r0 = np.floor(fr).astype(np.int64)
        c0 = np.floor(fc).astype(np.int64)
        wr = (fr - r0).astype(np.float32)
        wc = (fc - c0).astype(np.float32)
        r0c = np.clip(r0, 0, self.rows - 1)
        r1c = np.clip(r0 + 1, 0, self.rows - 1)
        c0c = np.clip(c0, 0, self.cols - 1)
        c1c = np.clip(c0 + 1, 0, self.cols - 1)
        v = self.values
        top = v[r1c][:, c0c] * (1 - wc)[None, :] + v[r1c][:, c1c] * wc[None, :]
        bottom = v[r0c][:, c0c] * (1 - wc)[None, :] + v[r0c][:, c1c] * wc[None, :]
        out = bottom * (1 - wr)[:, None] + top * wr[:, None]
        # nearest where a corner is unknown, so the shore is not eaten by NaN
        nearest = v[np.clip(np.rint(fr).astype(np.int64), 0, self.rows - 1)][
            :, np.clip(np.rint(fc).astype(np.int64), 0, self.cols - 1)
        ]
        out = np.where(np.isnan(out), nearest, out)
        outside = (fr < -0.5) | (fr > self.rows - 0.5)
        out[outside, :] = np.nan
        outside_c = (fc < -0.5) | (fc > self.cols - 0.5)
        out[:, outside_c] = np.nan
        return out.astype(np.float32)


def read_esri_ascii(path: Path) -> Grid:
    """An ESRI ASCII raster (six header lines, rows north to south) as a Grid."""
    with open(path, encoding="ascii") as f:
        header: dict[str, float] = {}
        for _ in range(6):
            key, value = f.readline().split()
            header[key.lower()] = float(value)
        values = np.loadtxt(f, dtype=np.float32)
    ncols, nrows = int(header["ncols"]), int(header["nrows"])
    assert values.shape == (nrows, ncols), values.shape
    cell = header["cellsize"]
    if "xllcorner" in header:
        west, south = header["xllcorner"], header["yllcorner"]
    else:
        west, south = header["xllcenter"] - cell / 2, header["yllcenter"] - cell / 2
    nodata = header.get("nodata_value", -9999.0)
    values[values == nodata] = np.nan
    return Grid(south, west, cell, values[::-1].copy())


def read_netcdf_classic(path: Path) -> dict[str, Any]:
    """A classic netCDF file (CDF-1, CDF-2 or CDF-5, as ERDDAP writes them): the
    dimensions, the variables' attributes and their data as numpy arrays."""
    with open(path, "rb") as f:
        data = f.read()
    magic, version = data[:3], data[3]
    if magic != b"CDF" or version not in (1, 2, 5):
        raise ValueError(f"{path}: not a classic netCDF file")
    offset_size = 8 if version in (2, 5) else 4
    pos = 4

    def u32() -> int:
        nonlocal pos
        v = struct.unpack(">I", data[pos : pos + 4])[0]
        pos += 4
        return v

    def u64() -> int:
        nonlocal pos
        v = struct.unpack(">Q", data[pos : pos + 8])[0]
        pos += 8
        return v

    def count() -> int:
        return u64() if version == 5 else u32()

    def name() -> str:
        nonlocal pos
        n = count()
        s = data[pos : pos + n].decode("utf-8")
        pos += n + (-n) % 4
        return s

    types = {
        1: ("b", 1),
        2: ("S", 1),
        3: (">i2", 2),
        4: (">i4", 4),
        5: (">f4", 4),
        6: (">f8", 8),
        7: (">u1", 1),
        8: (">u2", 2),
        9: (">u4", 4),
        10: (">i8", 8),
        11: (">u8", 8),
    }

    def values() -> Any:
        nonlocal pos
        typ = u32()
        n = count()
        dtype, size = types[typ]
        raw = data[pos : pos + n * size]
        pos += n * size + (-(n * size)) % 4
        if typ == 2:
            return raw.decode("utf-8", errors="replace")
        return np.frombuffer(raw, dtype=dtype, count=n)

    def attributes() -> dict[str, Any]:
        tag = u32()
        n = count()
        out: dict[str, Any] = {}
        if tag == 0:
            return out
        for _ in range(n):
            key = name()
            out[key] = values()
        return out

    count()  # numrecs
    tag = u32()
    ndims = count()
    dims: list[tuple[str, int]] = []
    if tag == 10:
        for _ in range(ndims):
            dims.append((name(), count()))
    attributes()  # global attributes
    tag = u32()
    nvars = count()
    variables: dict[str, Any] = {}
    if tag == 11:
        for _ in range(nvars):
            vname = name()
            nd = count()
            dimids = [count() for _ in range(nd)]
            attrs = attributes()
            typ = u32()
            vsize = count()
            begin = u64() if offset_size == 8 else u32()
            dtype, size = types[typ]
            shape = tuple(dims[i][1] for i in dimids)
            n = int(np.prod(shape)) if shape else 1
            arr = np.frombuffer(data, dtype=dtype, count=n, offset=begin).reshape(shape)
            variables[vname] = {"attrs": attrs, "data": arr, "dims": [dims[i][0] for i in dimids]}
            del vsize
    return {"dims": dict(dims), "variables": variables}


def emodnet_grid(path: Path, var: str) -> Grid:
    """An ERDDAP subset of EMODnet's DTM as a Grid (rows south to north)."""
    nc = read_netcdf_classic(path)
    lat = nc["variables"]["latitude"]["data"].astype(np.float64)
    lon = nc["variables"]["longitude"]["data"].astype(np.float64)
    v = nc["variables"][var]["data"].astype(np.float32)
    if lat[0] > lat[-1]:
        lat, v = lat[::-1], v[::-1]
    cell = float(np.round((lat[-1] - lat[0]) / (len(lat) - 1), 12))
    return Grid(float(lat[0] - cell / 2), float(lon[0] - cell / 2), cell, np.ascontiguousarray(v))


class Tiff:
    """The little a plain GeoTIFF needs: one image, one sample, int16 or float32,
    stripped or tiled, uncompressed or deflate, with the pixel scale and the tie point.
    Enough for GEBCO's tiles and extracts; not a general TIFF reader."""

    TYPES = {
        1: ("B", 1),
        2: ("c", 1),
        3: ("H", 2),
        4: ("I", 4),
        5: ("II", 8),
        11: ("f", 4),
        12: ("d", 8),
        16: ("Q", 8),
    }

    def __init__(self, f: Any):
        self.f = f
        head = f.read(8)
        self.order = "<" if head[:2] == b"II" else ">"
        if head[2:4] not in (b"\x2a\x00", b"\x00\x2a"):
            raise ValueError("not a classic TIFF")
        ifd = struct.unpack(self.order + "I", head[4:8])[0]
        f.seek(ifd)
        n = struct.unpack(self.order + "H", f.read(2))[0]
        self.tags: dict[int, Any] = {}
        entries = [struct.unpack(self.order + "HHII", f.read(12)) for _ in range(n)]
        for tag, typ, cnt, val in entries:
            fmt, size = self.TYPES.get(typ, ("B", 1))
            total = size * cnt
            if total <= 4:
                raw = struct.pack(self.order + "I", val)[:total]
            else:
                f.seek(val)
                raw = f.read(total)
            if typ == 2:
                self.tags[tag] = raw.rstrip(b"\0").decode("latin-1")
            elif typ == 5:
                self.tags[tag] = [a / b for a, b in struct.iter_unpack(self.order + "II", raw)]
            else:
                self.tags[tag] = list(struct.unpack(self.order + fmt * cnt, raw))
        self.width = self.tags[256][0]
        self.height = self.tags[257][0]
        self.bits = self.tags[258][0]
        self.compression = self.tags.get(259, [1])[0]
        self.sample_format = self.tags.get(339, [1])[0]
        self.predictor = self.tags.get(317, [1])[0]
        if self.tags.get(277, [1])[0] != 1:
            raise ValueError("one sample per pixel only")
        if self.sample_format == 2 and self.bits == 16:
            self.dtype = np.dtype(self.order + "i2")
        elif self.sample_format == 3 and self.bits == 32:
            self.dtype = np.dtype(self.order + "f4")
        elif self.sample_format == 1 and self.bits == 16:
            self.dtype = np.dtype(self.order + "u2")
        else:
            raise ValueError(f"sample format {self.sample_format} at {self.bits} bits")
        scale = self.tags.get(33550)
        tie = self.tags.get(33922)
        self.cell = float(scale[0]) if scale else None
        self.west = float(tie[3]) if tie else None
        self.north = float(tie[4]) if tie else None
        nodata = self.tags.get(42113)
        self.nodata = float(nodata) if nodata not in (None, "") else None

    def _block(self, offset: int, count: int, shape: tuple[int, int]) -> np.ndarray:
        self.f.seek(offset)
        raw = self.f.read(count)
        if self.compression in (8, 32946):
            raw = zlib.decompress(raw)
        elif self.compression != 1:
            raise ValueError(f"compression {self.compression} is not read here")
        arr = np.frombuffer(raw, dtype=self.dtype, count=shape[0] * shape[1]).reshape(shape)
        if self.predictor == 2:
            arr = np.cumsum(arr, axis=1, dtype=arr.dtype)
        return arr

    def rows(self, r0: int, r1: int) -> np.ndarray:
        """Rows r0 to r1 (top-down, as the file has them) as an array."""
        if 322 in self.tags:  # tiled
            tw, th = self.tags[322][0], self.tags[323][0]
            offsets, counts = self.tags[324], self.tags[325]
            across = math.ceil(self.width / tw)
            out = np.empty((r1 - r0, self.width), dtype=self.dtype)
            for ty in range(r0 // th, math.ceil(r1 / th)):
                for tx in range(across):
                    k = ty * across + tx
                    tile = self._block(offsets[k], counts[k], (th, tw))
                    y0, y1 = max(r0, ty * th), min(r1, (ty + 1) * th)
                    x1 = min(self.width, (tx + 1) * tw)
                    out[y0 - r0 : y1 - r0, tx * tw : x1] = tile[
                        y0 - ty * th : y1 - ty * th, : x1 - tx * tw
                    ]
            return out
        rps = self.tags.get(278, [self.height])[0]
        offsets, counts = self.tags[273], self.tags[279]
        out = np.empty((r1 - r0, self.width), dtype=self.dtype)
        for s in range(r0 // rps, math.ceil(r1 / rps)):
            rows_here = min(rps, self.height - s * rps)
            strip = self._block(offsets[s], counts[s], (rows_here, self.width))
            y0, y1 = max(r0, s * rps), min(r1, s * rps + rows_here)
            out[y0 - r0 : y1 - r0] = strip[y0 - s * rps : y1 - s * rps]
        return out


def decimate_tiff(path: Path, factor: int, log: Any) -> Grid:
    """A GEBCO GeoTIFF tile decimated by `factor` (the block mean, NaN-aware) as a Grid,
    read strip by strip so that a 933 MB tile needs no more memory than its output."""
    with open(path, "rb") as f:
        t = Tiff(f)
        out_rows, out_cols = t.height // factor, t.width // factor
        out = np.empty((out_rows, out_cols), dtype=np.float32)
        step = factor * 16
        for r0 in range(0, out_rows * factor, step):
            r1 = min(r0 + step, out_rows * factor)
            block = t.rows(r0, r1).astype(np.float32)
            if t.nodata is not None:
                block[block == t.nodata] = np.nan
            b = block.reshape((r1 - r0) // factor, factor, out_cols, factor)
            with np.errstate(invalid="ignore"):
                out[r0 // factor : r1 // factor] = np.nanmean(b, axis=(1, 3))
        cell = t.cell * factor
        south = t.north - t.height * t.cell
        west = t.west
    log(f'  {path.name}: {t.width}x{t.height} at {t.cell * 3600:.1f}" -> {out_cols}x{out_rows}')
    return Grid(south, west, cell, out[::-1].copy())


# ---------------------------------------------------------------------------
# The level grids and tiles
# ---------------------------------------------------------------------------


def tile_span_sec(level: int) -> float:
    return LEVELS[level]["cell_sec"] * TILE


def tile_corner_sec(level: int, lat: float, lon: float) -> tuple[int, int]:
    """The south-west corner, in integer arc-seconds, of the tile under a point."""
    span = tile_span_sec(level)
    ty = math.floor((lat + 90.0) * 3600.0 / span)
    tx = math.floor((lon + 180.0) * 3600.0 / span)
    return int(round(-90 * 3600 + ty * span)), int(round(-180 * 3600 + tx * span))


def tile_name(south_sec: int, west_sec: int) -> str:
    return f"{south_sec}_{west_sec}"


def tiles_over(
    level: int, south: float, north: float, west: float, east: float
) -> list[tuple[int, int]]:
    """The tiles of a level that meet a box, as (south_sec, west_sec) corners."""
    span = tile_span_sec(level)
    s0, w0 = tile_corner_sec(level, south, west)
    out = []
    s = s0
    while s < north * 3600.0:
        w = w0
        while w < east * 3600.0:
            out.append((int(round(s)), int(round(w))))
            w += span
        s += span
    return out


def cell_centres(level: int, south_sec: int, west_sec: int) -> tuple[np.ndarray, np.ndarray]:
    cell = LEVELS[level]["cell_sec"] / 3600.0
    lats = south_sec / 3600.0 + (np.arange(TILE) + 0.5) * cell
    lons = west_sec / 3600.0 + (np.arange(TILE) + 0.5) * cell
    return lats, lons


def to_int16(values: np.ndarray, unit_m: float) -> np.ndarray:
    scaled = np.rint(values / unit_m)
    out = np.where(np.isnan(scaled), NODATA, np.clip(scaled, -32767, 32767)).astype(np.int16)
    return out


def differenced(values: np.ndarray) -> np.ndarray:
    """Horizontal differencing (TIFF's predictor 2) before compression: a sea floor
    that changes by decimetres between neighbours compresses to a third of the size of
    the values themselves. The runtime undoes it with a cumulative sum at load
    (`freesail.world.chart.Tile.load`); int16 wraps and unwraps exactly."""
    d = np.diff(values.astype(np.int32), axis=1, prepend=0)
    return (d & 0xFFFF).astype(np.uint16).view(np.int16)


# ---------------------------------------------------------------------------
# The distance to the shore (C §5.4 step 4): a chamfer transform in metres
# ---------------------------------------------------------------------------


def distance_field(land: np.ndarray, cell_ns_m: float, cell_ew_m: float) -> np.ndarray:
    """The distance in metres from each cell to the nearest land cell: a two-pass
    chamfer transform with the metric lengths of the axial, diagonal and knight moves
    (Borgefors' 5-7-11 mask with true lengths; its error against the Euclidean is about
    two per cent at the worst angle). Rows are swept in Python, each row's in-row
    propagation done by a running minimum, so a region of seventeen million cells takes
    seconds. Land cells read 0; cells with no land anywhere read the field's ceiling."""
    rows, cols = land.shape
    big = np.float32(1e9)
    d = np.where(land, np.float32(0.0), big).astype(np.float32)
    a, b = np.float32(cell_ew_m), np.float32(cell_ns_m)
    c = np.float32(math.hypot(cell_ew_m, cell_ns_m))
    k1 = np.float32(math.hypot(2 * cell_ew_m, cell_ns_m))  # two across, one up
    k2 = np.float32(math.hypot(cell_ew_m, 2 * cell_ns_m))  # one across, two up
    idx = np.arange(cols, dtype=np.float32)

    def in_row(row: np.ndarray) -> np.ndarray:
        # left to right then right to left: d[c] = min_k (d[k] + a |c - k|)
        left = np.minimum.accumulate(row - a * idx) + a * idx
        right = (np.minimum.accumulate((row + a * idx)[::-1]) - a * idx[::-1])[::-1]
        return np.minimum(left, right)

    def shifted(row: np.ndarray, by: int) -> np.ndarray:
        out = np.full_like(row, big)
        if by > 0:
            out[by:] = row[:-by]
        elif by < 0:
            out[:by] = row[-by:]
        else:
            out[:] = row
        return out

    for r in range(rows):  # forward: from the rows below (south)
        row = d[r]
        if r >= 1:
            p = d[r - 1]
            row = np.minimum(row, p + b)
            row = np.minimum(row, shifted(p, 1) + c)
            row = np.minimum(row, shifted(p, -1) + c)
            row = np.minimum(row, shifted(p, 2) + k1)
            row = np.minimum(row, shifted(p, -2) + k1)
        if r >= 2:
            q = d[r - 2]
            row = np.minimum(row, shifted(q, 1) + k2)
            row = np.minimum(row, shifted(q, -1) + k2)
        d[r] = in_row(row)
    for r in range(rows - 1, -1, -1):  # backward: from the rows above (north)
        row = d[r]
        if r + 1 < rows:
            p = d[r + 1]
            row = np.minimum(row, p + b)
            row = np.minimum(row, shifted(p, 1) + c)
            row = np.minimum(row, shifted(p, -1) + c)
            row = np.minimum(row, shifted(p, 2) + k1)
            row = np.minimum(row, shifted(p, -2) + k1)
        if r + 2 < rows:
            q = d[r + 2]
            row = np.minimum(row, shifted(q, 1) + k2)
            row = np.minimum(row, shifted(q, -1) + k2)
        d[r] = in_row(row)
    return d


# ---------------------------------------------------------------------------
# The coast (C §5.2): the zero contour of the elevation as polylines
# ---------------------------------------------------------------------------


def contour_segments(values: np.ndarray, lats: np.ndarray, lons: np.ndarray) -> np.ndarray:
    """The zero contour of a cell-centred field by marching squares with linear
    interpolation: an array of segments (n, 2, 2) as (lon, lat) pairs. Cells with an
    unknown corner give no segment."""
    v = values
    rows, cols = v.shape
    known = ~np.isnan(v)
    inside = (v > 0.0) & known
    # the four corners of each 2x2 window: sw, se, ne, nw
    sw, se = inside[:-1, :-1], inside[:-1, 1:]
    ne, nw = inside[1:, 1:], inside[1:, :-1]
    ok = known[:-1, :-1] & known[:-1, 1:] & known[1:, 1:] & known[1:, :-1]
    case = (sw * 1 + se * 2 + ne * 4 + nw * 8) & 15
    active = ok & (case != 0) & (case != 15)
    ii, jj = np.nonzero(active)
    if len(ii) == 0:
        return np.zeros((0, 2, 2))
    vsw, vse = v[ii, jj], v[ii, jj + 1]
    vne, vnw = v[ii + 1, jj + 1], v[ii + 1, jj]

    def cross(v0: np.ndarray, v1: np.ndarray) -> np.ndarray:
        d = v1 - v0
        with np.errstate(divide="ignore", invalid="ignore"):
            t = np.where(d != 0.0, -v0 / d, 0.5)
        return np.clip(t, 0.0, 1.0)

    lat0, lat1 = lats[ii], lats[ii + 1]
    lon0, lon1 = lons[jj], lons[jj + 1]
    # the crossing on each edge: bottom (sw-se), right (se-ne), top (nw-ne), left (sw-nw)
    bottom = np.stack([lon0 + cross(vsw, vse) * (lon1 - lon0), lat0], axis=1)
    right = np.stack([lon1, lat0 + cross(vse, vne) * (lat1 - lat0)], axis=1)
    top = np.stack([lon0 + cross(vnw, vne) * (lon1 - lon0), lat1], axis=1)
    left = np.stack([lon0, lat0 + cross(vsw, vnw) * (lat1 - lat0)], axis=1)
    edges = {"b": bottom, "r": right, "t": top, "l": left}
    # marching squares: which edges each case joins (the saddles 5 and 10 split by the
    # centre's mean, as the usual disambiguation)
    table: dict[int, list[tuple[str, str]]] = {
        1: [("l", "b")],
        2: [("b", "r")],
        3: [("l", "r")],
        4: [("r", "t")],
        6: [("b", "t")],
        7: [("l", "t")],
        8: [("t", "l")],
        9: [("t", "b")],
        11: [("t", "r")],
        12: [("r", "l")],
        13: [("r", "b")],
        14: [("b", "l")],
    }
    c = case[ii, jj]
    out = []
    for k, pairs in table.items():
        m = c == k
        if not m.any():
            continue
        for e0, e1 in pairs:
            out.append(np.stack([edges[e0][m], edges[e1][m]], axis=1))
    centre = (vsw + vse + vne + vnw) / 4.0
    for k in (5, 10):
        m = c == k
        if not m.any():
            continue
        high = centre[m] > 0.0
        if k == 5:  # sw and ne inside
            first = [("l", "t"), ("b", "r")]
            second = [("l", "b"), ("t", "r")]
        else:  # se and nw inside
            first = [("b", "l"), ("r", "t")]
            second = [("b", "r"), ("l", "t")]
        for pairs, sel in ((first, high), (second, ~high)):
            if not sel.any():
                continue
            for e0, e1 in pairs:
                out.append(np.stack([edges[e0][m][sel], edges[e1][m][sel]], axis=1))
    return np.concatenate(out, axis=0)


def chain_segments(segments: np.ndarray, precision: float = 1e-7) -> list[np.ndarray]:
    """Join segments end to end into polylines (closed where they close)."""
    n = len(segments)
    if n == 0:
        return []
    keys = np.round(segments / precision).astype(np.int64)
    ends: dict[tuple[int, int], list[int]] = {}
    for i in range(n):
        for e in (0, 1):
            ends.setdefault((int(keys[i, e, 0]), int(keys[i, e, 1])), []).append(i)
    used = np.zeros(n, dtype=bool)
    lines: list[np.ndarray] = []
    for start in range(n):
        if used[start]:
            continue
        used[start] = True
        line = [segments[start, 0], segments[start, 1]]
        # extend forward from the end, then backward from the start
        for direction in (1, 0):
            while True:
                tip = line[-1] if direction == 1 else line[0]
                key = (int(round(tip[0] / precision)), int(round(tip[1] / precision)))
                nxt = None
                for i in ends.get(key, ()):
                    if not used[i]:
                        nxt = i
                        break
                if nxt is None:
                    break
                used[nxt] = True
                k0 = (int(keys[nxt, 0, 0]), int(keys[nxt, 0, 1]))
                other = segments[nxt, 1] if k0 == key else segments[nxt, 0]
                if direction == 1:
                    line.append(other)
                else:
                    line.insert(0, other)
        lines.append(np.array(line))
    return lines


def simplify(points: np.ndarray, tolerance: float) -> np.ndarray:
    """Douglas-Peucker on a polyline of (x, y) in degrees, `tolerance` in degrees of
    the same scale (the caller scales longitude by cos(lat) first if it cares)."""
    if len(points) < 3:
        return points
    keep = np.zeros(len(points), dtype=bool)
    keep[0] = keep[-1] = True
    stack = [(0, len(points) - 1)]
    while stack:
        i, j = stack.pop()
        if j <= i + 1:
            continue
        p, q = points[i], points[j]
        seg = q - p
        length2 = float(seg @ seg)
        mid = points[i + 1 : j]
        if length2 == 0.0:
            dist = np.hypot(mid[:, 0] - p[0], mid[:, 1] - p[1])
        else:
            t = np.clip(((mid - p) @ seg) / length2, 0.0, 1.0)
            proj = p + t[:, None] * seg
            dist = np.hypot(mid[:, 0] - proj[:, 0], mid[:, 1] - proj[:, 1])
        k = int(np.argmax(dist))
        if dist[k] > tolerance:
            keep[i + 1 + k] = True
            stack.append((i, i + 1 + k))
            stack.append((i + 1 + k, j))
    return points[keep]


# ---------------------------------------------------------------------------
# Overrides (C §5.2, §5.4 step 3): the period's polygons rasterised
# ---------------------------------------------------------------------------


@dataclass
class Patch:
    override: str
    name: str
    kind: str  # "depth", "drying", "land", "sea"
    polygon: np.ndarray  # (n, 2) of (lat, lon)
    elevation_m: float  # relative to chart datum, positive up
    source: str
    note: str = ""


def load_overrides(region: str) -> tuple[list[Patch], list[dict[str, Any]]]:
    """Every override file of a region as patches with their elevation in metres
    relative to chart datum, and the files' own records for the manifest."""
    folder = CHARTS_DIR / "overrides" / region
    patches: list[Patch] = []
    records: list[dict[str, Any]] = []
    for path in sorted(folder.glob("*.yaml")) if folder.exists() else []:
        doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        unit = UNIT_M[str(doc.get("units", "fathoms")).lower()]
        above = float(doc.get("datum_above_chart_datum_m", 0.0))
        for p in doc.get("patches") or []:
            kind = str(p.get("kind", "depth"))
            if kind == "depth":
                elevation = -(float(p["depth"]) * unit + above)
            elif kind == "drying":
                elevation = float(p["drying_height"]) * unit + above
            elif kind == "land":
                elevation = float(p.get("height_m", 5.0))
            elif kind == "sea":
                elevation = -(float(p["depth"]) * unit + above)
            else:
                raise SystemExit(f"{path}: patch kind {kind!r} is not depth, drying, land or sea")
            poly = np.array([[float(a), float(b)] for a, b in p["polygon"]], dtype=np.float64)
            if len(poly) < 3:
                raise SystemExit(f"{path}: patch {p.get('name')!r} needs three points")
            patches.append(
                Patch(
                    path.stem,
                    str(p.get("name", "")),
                    kind,
                    poly,
                    elevation,
                    str(p.get("source") or doc.get("source") or ""),
                    str(p.get("note", "")),
                )
            )
        records.append(
            {
                "file": f"overrides/{region}/{path.name}",
                "sheet": doc.get("sheet"),
                "source": doc.get("source"),
                "units": doc.get("units"),
                "datum": doc.get("datum"),
                "datum_above_chart_datum_m": above,
                "control_points": doc.get("control_points"),
                "patches": len(doc.get("patches") or []),
            }
        )
    return patches, records


def point_in_polygon(lats: np.ndarray, lons: np.ndarray, poly: np.ndarray) -> np.ndarray:
    """An even-odd test of the grid of cell centres `lats` x `lons` against a polygon
    of (lat, lon) vertices: a boolean array (len(lats), len(lons))."""
    inside = np.zeros((len(lats), len(lons)), dtype=bool)
    n = len(poly)
    LAT, LON = np.meshgrid(lats, lons, indexing="ij")
    for i in range(n):
        y0, x0 = poly[i]
        y1, x1 = poly[(i + 1) % n]
        if y0 == y1:
            continue
        cond = (LAT > min(y0, y1)) & (LAT <= max(y0, y1))
        xcross = x0 + (LAT - y0) * (x1 - x0) / (y1 - y0)
        inside ^= cond & (LON < xcross)
    return inside


def apply_patches(
    elevation: np.ndarray, lats: np.ndarray, lons: np.ndarray, patches: list[Patch], log: Any
) -> tuple[np.ndarray, np.ndarray]:
    """Rasterise the patches over a tile's elevation (metres, positive up); returns the
    new elevation and a mask of the cells an override wrote. Prints the places where a
    depth patch and the modern grid disagree in open water beyond OVERRIDE_TOLERANCE_M."""
    out = elevation.copy()
    written = np.zeros(elevation.shape, dtype=bool)
    lat_min, lat_max = lats[0], lats[-1]
    lon_min, lon_max = lons[0], lons[-1]
    for p in patches:
        if (
            p.polygon[:, 0].max() < lat_min
            or p.polygon[:, 0].min() > lat_max
            or p.polygon[:, 1].max() < lon_min
            or p.polygon[:, 1].min() > lon_max
        ):
            continue
        # only the cells under the polygon's box are tested
        r0 = int(np.searchsorted(lats, p.polygon[:, 0].min()))
        r1 = int(np.searchsorted(lats, p.polygon[:, 0].max())) + 1
        c0 = int(np.searchsorted(lons, p.polygon[:, 1].min()))
        c1 = int(np.searchsorted(lons, p.polygon[:, 1].max())) + 1
        sub = point_in_polygon(lats[r0:r1], lons[c0:c1], p.polygon)
        if not sub.any():
            continue
        mask = np.zeros(elevation.shape, dtype=bool)
        mask[r0:r1, c0:c1] = sub
        if p.kind == "depth":
            modern = elevation[mask]
            sea = modern[(modern < 0) & ~np.isnan(modern)]
            if len(sea):
                diff = float(np.nanmean(sea) - p.elevation_m)
                if abs(diff) > OVERRIDE_TOLERANCE_M:
                    log(
                        f"  note: {p.override}/{p.name}: the period depth is "
                        f"{-p.elevation_m:.1f} m, the modern grid {-np.nanmean(sea):.1f} m "
                        f"(a difference of {diff:+.1f} m)"
                    )
        out[mask] = p.elevation_m
        written |= mask
    return out, written


# ---------------------------------------------------------------------------
# Features (C §5.2): checked, indexed
# ---------------------------------------------------------------------------

FEATURE_KINDS = frozenset(
    {
        "headland",
        "island",
        "rock",
        "ledge",
        "bank",
        "shoal",
        "drying",
        "tower",
        "castle",
        "church",
        "beacon",
        "mill",
        "light",
        "place",
        "anchorage",
        "road",
        "transit",
        "bottom",
        "mark",
        "hill",
        "town",
    }
)


def load_features(region: str) -> tuple[list[dict[str, Any]], Path]:
    path = CHARTS_DIR / "features" / f"{region}.yaml"
    doc = yaml.safe_load(path.read_text(encoding="utf-8")) if path.exists() else {}
    features = list((doc or {}).get("features") or [])
    seen: set[str] = set()
    for f in features:
        for key in ("id", "kind", "name", "lat_deg", "lon_deg", "source", "says"):
            if key not in f:
                raise SystemExit(f"{path}: feature {f.get('id')!r} lacks {key!r}")
        if f["kind"] not in FEATURE_KINDS:
            raise SystemExit(f"{path}: feature {f['id']!r} kind {f['kind']!r} unknown")
        if f["id"] in seen:
            raise SystemExit(f"{path}: feature id {f['id']!r} given twice")
        seen.add(f["id"])
        if not str(f["source"]).strip():
            raise SystemExit(f"{path}: feature {f['id']!r} cites no source")
    return features, path


INDEX_CELL_DEG = 0.25


def index_cell(lat: float, lon: float) -> str:
    return f"{math.floor(lat / INDEX_CELL_DEG)},{math.floor(lon / INDEX_CELL_DEG)}"


def build_index(features: list[dict[str, Any]]) -> dict[str, Any]:
    cells: dict[str, list[str]] = {}
    for f in features:
        cells.setdefault(index_cell(float(f["lat_deg"]), float(f["lon_deg"])), []).append(f["id"])
    return {"cell_deg": INDEX_CELL_DEG, "cells": dict(sorted(cells.items()))}


# ---------------------------------------------------------------------------
# The build
# ---------------------------------------------------------------------------


class Build:
    def __init__(self, cache: Path, skip_fetch: bool, report: list[str]):
        self.cache = cache
        self.skip_fetch = skip_fetch
        self.report = report
        self.fetched: dict[str, list[Fetched]] = {k: [] for k in SOURCES}
        self.manifest: dict[str, Any] = {}

    def log(self, line: str) -> None:
        print(line, flush=True)
        self.report.append(line)

    # -- the region ----------------------------------------------------------------

    def build_region(self, region: str) -> dict[str, Any]:
        recipe = REGIONS[region]
        b = recipe["bounds"]
        fb = recipe["fetch"]
        self.log(f"Region {region}: {recipe['title']}")
        self.log("Fetching the sources:")
        gebco = fetch_gebco_extract(
            {
                "south": fb["south"] - 0.1,
                "north": fb["north"] + 0.1,
                "west": fb["west"] - 0.1,
                "east": fb["east"] + 0.1,
            },
            self.cache,
            self.skip_fetch,
            self.log,
        )
        self.fetched["gebco_2025"].append(gebco)
        emod = fetch_emodnet("elevation", fb, self.cache, self.skip_fetch, self.log)
        emod_max = fetch_emodnet("elevation_max", fb, self.cache, self.skip_fetch, self.log)
        self.fetched["emodnet_dtm_2024"] += [emod, emod_max]
        self.log("Reading them:")
        with zipfile.ZipFile(gebco.path) as z:
            asc = next(n for n in z.namelist() if n.endswith(".asc"))
            with z.open(asc) as f:
                tmp = self.cache / "gebco" / asc
                tmp.write_bytes(f.read())
        g_gebco = read_esri_ascii(tmp)
        g_emod = emodnet_grid(emod.path, "elevation")
        g_emod_max = emodnet_grid(emod_max.path, "elevation_max")
        self.log(
            f'  GEBCO {g_gebco.cols}x{g_gebco.rows} at {g_gebco.cell * 3600:.1f}"; '
            f'EMODnet {g_emod.cols}x{g_emod.rows} at {g_emod.cell * 3600:.2f}"'
        )
        patches, override_records = load_overrides(region)
        features, features_path = load_features(region)
        self.log(
            f"  {len(patches)} override patches in {len(override_records)} files; "
            f"{len(features)} features"
        )
        # level 2: the region whole
        out: dict[str, Any] = {
            "title": recipe["title"],
            "bounds": dict(b),
            "levels": [2, 3],
            "tiles": {},
            "coast": f"coast/{region}.geojson",
            "features": f"features/{region}.yaml",
            "index": f"features/{region}.index.json",
            "overrides": override_records,
            "harbours": recipe["harbours"],
        }
        coast_lines: list[dict[str, Any]] = []
        out["tiles"]["2"] = self._build_level(
            2,
            tiles_over(2, b["south"], b["north"], b["west"], b["east"]),
            g_emod,
            g_emod_max,
            g_gebco,
            patches,
            coast_lines,
            region,
        )
        level3: list[dict[str, Any]] = []
        for hname, hb in recipe["harbours"].items():
            self.log(f"  harbour patch {hname}")
            level3 += self._build_level(
                3,
                tiles_over(3, hb["south"], hb["north"], hb["west"], hb["east"]),
                g_emod,
                g_emod_max,
                g_gebco,
                patches,
                None,
                region,
                harbour=hname,
            )
        out["tiles"]["3"] = level3
        # the coast
        coast_path = CHARTS_DIR / "coast" / f"{region}.geojson"
        coast_path.parent.mkdir(parents=True, exist_ok=True)
        coast_path.write_text(
            json.dumps(
                {"type": "FeatureCollection", "features": coast_lines}, separators=(",", ":")
            ),
            encoding="utf-8",
        )
        points = sum(len(f["geometry"]["coordinates"]) for f in coast_lines)
        self.log(
            f"  coast: {len(coast_lines)} pieces, {points} points, "
            f"{coast_path.stat().st_size:,} bytes"
        )
        # the index
        index_path = CHARTS_DIR / "features" / f"{region}.index.json"
        index_path.parent.mkdir(parents=True, exist_ok=True)
        index_path.write_text(json.dumps(build_index(features), indent=0), encoding="utf-8")
        kinds: dict[str, int] = {}
        for f in features:
            kinds[f["kind"]] = kinds.get(f["kind"], 0) + 1
        self.log("  features by kind: " + ", ".join(f"{k} {n}" for k, n in sorted(kinds.items())))
        out["feature_count"] = len(features)
        out["features_by_kind"] = dict(sorted(kinds.items()))
        return out

    def _build_level(
        self,
        level: int,
        tiles: list[tuple[int, int]],
        g_emod: Grid,
        g_emod_max: Grid,
        g_gebco: Grid,
        patches: list[Patch],
        coast_lines: list[dict[str, Any]] | None,
        region: str,
        harbour: str | None = None,
    ) -> list[dict[str, Any]]:
        """The tiles of one level over the region or a harbour patch: EMODnet sampled,
        GEBCO under it where EMODnet is unknown, the overrides written, the distance
        field derived over the whole block (so a shore beyond a tile's edge counts), and
        each tile written with its minimum depth."""
        cell_sec = LEVELS[level]["cell_sec"]
        unit_m = LEVELS[level]["unit_m"]
        souths = sorted({s for s, _ in tiles})
        wests = sorted({w for _, w in tiles})
        rows = len(souths) * TILE
        cols = len(wests) * TILE
        south0, west0 = souths[0], wests[0]
        lats = south0 / 3600.0 + (np.arange(rows) + 0.5) * cell_sec / 3600.0
        lons = west0 / 3600.0 + (np.arange(cols) + 0.5) * cell_sec / 3600.0
        self.log(f"  level {level}: {len(tiles)} tiles, {cols}x{rows} cells")
        elev = g_emod.sample(lats, lons)
        under = g_gebco.sample(lats, lons)
        # GEBCO under everything: where EMODnet is unknown (the land, mostly) GEBCO's
        # height relative to mean sea level stands, a few metres high against LAT on land
        # and never read for depth there
        unknown = np.isnan(elev)
        elev = np.where(unknown, under, elev)
        shoal = g_emod_max.sample(lats, lons)
        elev, written = apply_patches(elev, lats, lons, patches, self.log)
        shoal = np.where(written, elev, shoal)
        land = (elev > 0.0) & ~np.isnan(elev)
        mid_lat = math.radians(float(lats[rows // 2]))
        cell_ns = cell_sec * M_PER_SEC_LAT
        cell_ew = cell_ns * math.cos(mid_lat)
        t0 = time.time()
        dist = distance_field(land, cell_ns, cell_ew)
        self.log(f"    distance field in {time.time() - t0:.1f} s")
        if coast_lines is not None:
            t0 = time.time()
            segs = contour_segments(elev, lats, lons)
            lines = chain_segments(segs)
            tol = 0.0003  # about 30 m of latitude
            scale = math.cos(mid_lat)
            for line in lines:
                scaled = np.column_stack([line[:, 0] * scale, line[:, 1]])
                keep = simplify(scaled, tol)
                if len(keep) < 2:
                    continue
                coords = [[round(float(x / scale), 5), round(float(y), 5)] for x, y in keep]
                coast_lines.append(
                    {
                        "type": "Feature",
                        "geometry": {"type": "LineString", "coordinates": coords},
                        "properties": {"source": "emodnet_dtm_2024", "level": level},
                    }
                )
            self.log(
                f"    coast: {len(segs)} segments, {len(lines)} lines in {time.time() - t0:.1f} s"
            )
        records = []
        folder = CHARTS_DIR / "tiles" / str(level)
        folder.mkdir(parents=True, exist_ok=True)
        for s, w in tiles:
            r0 = int(round((s - south0) / cell_sec))
            c0 = int(round((w - west0) / cell_sec))
            block = elev[r0 : r0 + TILE, c0 : c0 + TILE]
            shoal_block = shoal[r0 : r0 + TILE, c0 : c0 + TILE]
            dblock = dist[r0 : r0 + TILE, c0 : c0 + TILE]
            sea = (block < 0.0) & ~np.isnan(block)
            if sea.any():
                shoalest = np.where(np.isnan(shoal_block), block, shoal_block)
                min_depth = float(-np.max(shoalest[sea]))
            else:
                min_depth = float("nan")
            dist_cells = np.clip(np.rint(dblock / cell_ns), 0, 65535).astype(np.uint16)
            name = tile_name(s, w)
            path = folder / f"{name}.npz"
            np.savez_compressed(
                path,
                elevation=differenced(to_int16(block, unit_m)),
                predictor=np.int16(2),
                dist=dist_cells,
                level=np.int16(level),
                unit_m=np.float32(unit_m),
                cell_sec=np.float32(cell_sec),
                south_sec=np.int64(s),
                west_sec=np.int64(w),
                nodata=np.int16(NODATA),
                min_depth_m=np.float32(min_depth),
                overridden=written[r0 : r0 + TILE, c0 : c0 + TILE],
            )
            records.append(
                {
                    "name": name,
                    "south_sec": s,
                    "west_sec": w,
                    "min_depth_m": None if math.isnan(min_depth) else round(min_depth, 1),
                    "bytes": path.stat().st_size,
                    **({"harbour": harbour} if harbour else {}),
                }
            )
        total = sum(r["bytes"] for r in records)
        self.log(
            f"    written: {len(records)} tiles, {total:,} bytes compressed "
            f"({len(tiles) * TILE * TILE * 4:,} raw)"
        )
        return records

    # -- the world and the Atlantic ----------------------------------------------------

    def build_gebco_levels(self, world: bool, atlantic: bool) -> dict[str, Any]:
        """Levels 0 and 1 from GEBCO's eight global GeoTIFF tiles: decimated by ten
        for the world (2.5'), by two for the Atlantic (30\"); the world committed, the
        Atlantic left in the tiles folder for the developer and not committed."""
        out: dict[str, Any] = {}
        if not (world or atlantic):
            return out
        self.log("The world and the Atlantic from GEBCO's global tiles:")
        z = fetch_url(
            GEBCO_ZIP_URL,
            self.cache / "gebco" / "gebco_2025_geotiff.zip",
            self.skip_fetch,
            self.log,
        )
        self.fetched["gebco_2025"].append(z)
        jobs = []
        if world:
            jobs.append((0, 10, WORLD))
        if atlantic:
            jobs.append((1, 2, ATLANTIC))
        with zipfile.ZipFile(z.path) as zf:
            names = sorted(n for n in zf.namelist() if n.endswith(".tif"))
            for level, factor, box in jobs:
                self.log(f"  level {level}: decimating by {factor}")
                grids = []
                for n in names:
                    m = re.match(
                        r"gebco_2025_n(-?[\d.]+)_s(-?[\d.]+)_w(-?[\d.]+)_e(-?[\d.]+)\.tif", n
                    )
                    north, south, west, east = (float(x) for x in m.groups())
                    if (
                        east <= box["west"]
                        or west >= box["east"]
                        or north <= box["south"]
                        or south >= box["north"]
                    ):
                        continue
                    tmp = self.cache / "gebco" / n
                    if not tmp.exists():
                        with zf.open(n) as src, open(tmp, "wb") as dst:
                            while True:
                                chunk = src.read(1 << 24)
                                if not chunk:
                                    break
                                dst.write(chunk)
                    grids.append(decimate_tiff(tmp, factor, self.log))
                out[str(level)] = self._write_gebco_level(level, grids, box)
        return out

    def _write_gebco_level(
        self, level: int, grids: list[Grid], box: dict[str, float]
    ) -> dict[str, Any]:
        cell_sec = LEVELS[level]["cell_sec"]
        unit_m = LEVELS[level]["unit_m"]
        folder = CHARTS_DIR / "tiles" / str(level)
        folder.mkdir(parents=True, exist_ok=True)
        tiles = tiles_over(level, box["south"], box["north"], box["west"], box["east"])
        records = []
        for s, w in tiles:
            lats, lons = cell_centres(level, s, w)
            block = np.full((TILE, TILE), np.nan, dtype=np.float32)
            for g in grids:
                if lats[-1] < g.south or lats[0] > g.north or lons[-1] < g.west or lons[0] > g.east:
                    continue
                # the decimated grid's cells are the level's cells exactly: take them
                r = np.rint((lats - g.south) / g.cell - 0.5).astype(np.int64)
                c = np.rint((lons - g.west) / g.cell - 0.5).astype(np.int64)
                rok = (r >= 0) & (r < g.rows)
                cok = (c >= 0) & (c < g.cols)
                sub = g.values[np.clip(r, 0, g.rows - 1)][:, np.clip(c, 0, g.cols - 1)]
                take = rok[:, None] & cok[None, :]
                block = np.where(take & np.isnan(block), sub, block)
            if np.all(np.isnan(block)):
                continue
            sea = (block < 0.0) & ~np.isnan(block)
            min_depth = float(-np.max(block[sea])) if sea.any() else float("nan")
            if not sea.any():
                continue  # tiles all land dropped: the picture keeps its coast (C §5.3)
            clip = LEVELS[level].get("land_clip_m")
            if clip is not None:
                block = np.where(block > clip, np.float32(clip), block)
            name = tile_name(s, w)
            path = folder / f"{name}.npz"
            np.savez_compressed(
                path,
                elevation=differenced(to_int16(block, unit_m)),
                predictor=np.int16(2),
                level=np.int16(level),
                unit_m=np.float32(unit_m),
                cell_sec=np.float32(cell_sec),
                south_sec=np.int64(s),
                west_sec=np.int64(w),
                nodata=np.int16(NODATA),
                min_depth_m=np.float32(min_depth),
            )
            records.append(
                {
                    "name": name,
                    "south_sec": s,
                    "west_sec": w,
                    "min_depth_m": None if math.isnan(min_depth) else round(min_depth, 1),
                    "bytes": path.stat().st_size,
                }
            )
        total = sum(r["bytes"] for r in records)
        self.log(f"    level {level}: {len(records)} tiles, {total:,} bytes compressed")
        return {"level": level, "bounds": dict(box), "tiles": records, "bytes": total}

    # -- the manifest ----------------------------------------------------------------

    def write_manifest(
        self, regions: dict[str, Any], gebco_levels: dict[str, Any], notes: dict[str, Any]
    ) -> Path:
        for sid, s in SOURCES.items():
            if s["licence"] not in ALLOWED_LICENCES:
                raise SystemExit(f"source {sid} carries the licence {s['licence']}, not allowed")
        sources = {}
        for sid, s in SOURCES.items():
            sources[sid] = {
                "name": s["name"],
                "licence": s["licence"],
                "licence_name": ALLOWED_LICENCES[s["licence"]],
                "licence_text": s["licence_text"],
                "attribution": s["attribution"],
                "datum": s["datum"],
                "home": s["home"],
                "used_for": s["used_for"],
                "fetched": [f.record() for f in self.fetched[sid]],
                "status": "fetched" if self.fetched[sid] else "not fetched in this build",
            }
        hand = sorted((CHARTS_DIR / "features").glob("*.yaml")) + sorted(
            (CHARTS_DIR / "overrides").glob("*/*.yaml")
        )
        h = hashlib.sha256(Path(__file__).read_bytes())
        for p in hand:
            h.update(p.read_bytes())
        for fs in self.fetched.values():
            for f in fs:
                h.update(f.sha256.encode())
        attribution = (
            "Chart data built from open sources, not for navigation. "
            + " ".join(SOURCES[sid]["attribution"] for sid in ("gebco_2025", "emodnet_dtm_2024"))
            + " The period features and patches are transcribed from the charts and pilots "
            "named in data/charts/features and data/charts/overrides, whose scans are not "
            "distributed here."
        )
        manifest = {
            "format": 1,
            "built": _today(),
            "tool": "tools/build_charts.py",
            "build_hash": h.hexdigest()[:16],
            "levels": {
                str(k): {
                    "cell_sec": v["cell_sec"],
                    "tile_cells": TILE,
                    "unit_m": v["unit_m"],
                    "use": v["use"],
                    "datum": SOURCES["gebco_2025"]["datum"]
                    if k < 2
                    else SOURCES["emodnet_dtm_2024"]["datum"],
                }
                for k, v in LEVELS.items()
            },
            "nodata": NODATA,
            "regions": regions,
            "world": gebco_levels.get("0"),
            "atlantic": (
                {**gebco_levels["1"], "committed": False} if "1" in gebco_levels else None
            ),
            "sources": sources,
            "attribution": attribution,
            "notes": notes,
        }
        path = CHARTS_DIR / "manifest.yaml"
        path.write_text(
            "# The chart data's manifest (spec M5 §10; C §5.2), written by tools/build_charts.py.\n"
            "# Every source with its licence, attribution, URL, retrieval date and checksum; the\n"
            "# regions and their tiles; the attribution block the game shows in its about text.\n"
            + yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True, width=100),
            encoding="utf-8",
        )
        return path


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument(
        "--cache", type=Path, default=DEFAULT_CACHE, help="the fetch cache, outside the repository"
    )
    ap.add_argument(
        "--region", action="append", default=None, help="a region to build (default: all)"
    )
    ap.add_argument("--world", action="store_true", help="build level 0 from GEBCO's global tiles")
    ap.add_argument("--atlantic", action="store_true", help="build level 1 (not committed)")
    ap.add_argument(
        "--reuse-world",
        action="store_true",
        help="keep the world level as the last manifest lists it, instead of decimating the "
        "globe again (a region's rebuild after a change of its hand-made files)",
    )
    ap.add_argument("--skip-fetch", action="store_true", help="use the cache only; refuse to fetch")
    ap.add_argument("--report", type=Path, default=None, help="write the report here too")
    ap.add_argument(
        "--notes",
        type=Path,
        default=None,
        help="a YAML file of notes for the manifest (the C §7 checks)",
    )
    args = ap.parse_args(argv)
    report: list[str] = []
    build = Build(args.cache, args.skip_fetch, report)
    args.cache.mkdir(parents=True, exist_ok=True)
    regions = {}
    for region in args.region or list(REGIONS):
        regions[region] = build.build_region(region)
    gebco_levels = build.build_gebco_levels(args.world, args.atlantic)
    if args.reuse_world and "0" not in gebco_levels:
        # the world level as the last manifest lists it, its tiles checked present
        last = yaml.safe_load((CHARTS_DIR / "manifest.yaml").read_text(encoding="utf-8"))
        world = (last or {}).get("world")
        if world:
            for t in world["tiles"]:
                if not (CHARTS_DIR / "tiles" / "0" / f"{t['name']}.npz").exists():
                    raise SystemExit(f"--reuse-world: the tile {t['name']} is missing; run --world")
            gebco_levels["0"] = world
            for f in (last.get("sources") or {}).get("gebco_2025", {}).get("fetched", []):
                if f.get("file", "").endswith("gebco_2025_geotiff.zip"):
                    build.fetched["gebco_2025"].append(
                        Fetched(Path(f["file"]), f["url"], f["retrieved"], f["sha256"], f["bytes"])
                    )
            build.log("The world level kept as the last manifest lists it (--reuse-world).")
    notes_path = args.notes or CHARTS_DIR / "unverified-checks.yaml"
    notes = yaml.safe_load(notes_path.read_text(encoding="utf-8")) if notes_path.exists() else {}
    path = build.write_manifest(regions, gebco_levels, notes)
    build.log(f"Manifest written: {path}")
    if args.report:
        args.report.write_text("\n".join(report) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
