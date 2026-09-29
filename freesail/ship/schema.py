"""The ship file format: what a ship definition may contain, and its validation.

A ship file (YAML, see docs/TechnicalSpec-M0-M2.md §6) lists a hull, spars,
sails and lines, with *role links* between them (`on`, `steps_on`, `yard`,
`mast`, `gaff`, `boom`, `stay`, `of`). This module turns the raw dictionary
into typed specs and rejects anything the engine could not reason about,
with an error written as a sentence naming the file and the part.

Nothing here knows about any particular rig. It knows about part classes and
what each class requires.

An optional `crew:` section (docs/TechnicalSpec-M3.md §2.3) establishes the
ship's company: complement, stations, ratings, posts, idlers by trade and
stores. It is parsed into a `CrewSpec`; a file without it has `crew = None`.

Milestone 3b (docs/TechnicalSpec-M3b.md §6) adds canvas: a sail may give its
`canvas_no` (the number of the canvas it is made of, 1 the heaviest), say
that it starts the voyage in the sail room (`bent: false`: storm canvas and
the occasional sails), and name the sail it is bent `in_place_of` (a storm
mizzen for the spanker). The stores may list the sail room's contents
(`sails:`, each with the sail it is made for, its canvas number and its
condition); the old `spare_sails` count is then derived from the list.

Package 30b (milestone 5) makes the spare spars a store by class: the stores'
`spare_spars` may map a spar class to the number of spares of it on the booms
(`{topmast: 2, studdingsail_boom: 4}`), and the count is then derived from it. A
plain number is still taken: that many spars of no class, which the carpenter can
fit to any spar.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

# ---------------------------------------------------------------------------
# Part classes
# ---------------------------------------------------------------------------

SPAR_CLASSES = frozenset(
    {
        "mast",
        "topmast",
        "topgallant_mast",
        "royal_mast",
        "bowsprit",
        "jib_boom",
        "flying_jib_boom",
        "yard",
        "gaff",
        "boom",
        "studdingsail_boom",
        "lug_yard",
        "lateen_yard",
        "sprit",
    }
)

# Spars that stand on the hull itself and therefore need no `on`/`steps_on`.
ROOT_SPAR_CLASSES = frozenset({"mast", "bowsprit"})

# Spars that behave as a "yard": braced, and carrying a square-family sail.
YARD_LIKE_CLASSES = frozenset({"yard", "lug_yard", "lateen_yard"})

SAIL_CLASSES = frozenset({"square", "gaff", "jibheaded", "lug", "lateen", "sprit", "studding"})

# Role links each sail class must have, and the spar classes each may point at.
SAIL_ROLE_REQUIREMENTS: dict[str, dict[str, frozenset[str]]] = {
    "square": {"yard": frozenset({"yard"})},
    "gaff": {"mast": frozenset({"mast", "topmast"}), "gaff": frozenset({"gaff"})},
    "jibheaded": {},  # needs a stay OR a mast; checked in validate()
    "lug": {"yard": frozenset({"lug_yard"})},
    "lateen": {"yard": frozenset({"lateen_yard"})},
    "sprit": {"mast": frozenset({"mast"}), "sprit": frozenset({"sprit"})},
    # a studding-class sail is spread by a studding sail boom, or (a water sail) laced under
    # a gaff sail's own boom (spec 3b §6.4; Steel 1794 vol. I, 'Sloop's water-sail')
    "studding": {"boom": frozenset({"studdingsail_boom", "boom"})},
}
SAIL_OPTIONAL_ROLES: dict[str, dict[str, frozenset[str]]] = {
    "gaff": {"boom": frozenset({"boom"})},
    "jibheaded": {
        "stay": frozenset(),  # a stay is a line, checked separately
        "mast": frozenset({"mast", "topmast", "topgallant_mast"}),
        "halyard_spar": frozenset(),
    },
    "lug": {"mast": frozenset({"mast", "topmast"})},
    "lateen": {"mast": frozenset({"mast"})},
    "studding": {"yard": frozenset({"yard"})},
}

LINE_CLASSES = frozenset(
    {
        "halyard",
        "throat_halyard",
        "peak_halyard",
        "sheet",
        "tack",
        "brace",
        "lift",
        "clewline",
        "buntline",
        "leechline",
        "bowline",
        "reef_tackle",
        "downhaul",
        "outhaul",
        "vang",
        "guy",
        "stay",
        "shroud",
        "backstay",
    }
)
STANDING_LINE_CLASSES = frozenset({"stay", "shroud", "backstay"})

# What kind of part each line class may be "of".
LINE_TARGET_KINDS: dict[str, frozenset[str]] = {
    "halyard": frozenset({"spar", "sail"}),
    "throat_halyard": frozenset({"spar"}),
    "peak_halyard": frozenset({"spar"}),
    "sheet": frozenset({"sail"}),
    "tack": frozenset({"sail"}),
    "brace": frozenset({"spar"}),
    "lift": frozenset({"spar"}),
    "clewline": frozenset({"sail"}),
    "buntline": frozenset({"sail"}),
    "leechline": frozenset({"sail"}),
    "bowline": frozenset({"sail"}),
    "reef_tackle": frozenset({"sail"}),
    "downhaul": frozenset({"sail", "spar"}),
    "outhaul": frozenset({"sail", "spar"}),
    "vang": frozenset({"spar"}),
    "guy": frozenset({"spar"}),
    "stay": frozenset({"spar"}),
    "shroud": frozenset({"spar"}),
    "backstay": frozenset({"spar"}),
}

SIDES = frozenset({"starboard", "larboard"})

# Spars a fore-and-aft sail is spread on. A ringtail boom run out on one of these, and the
# ringtail or water sail it spreads, lie in the gaff sail's plane and have no fixed side
# (spec 3b §6.4; Kipping 1847, 'Ringtail Sails': it "sets like a topmast studding sail,
# outside of the after-leech of the main-trysail").
FORE_AND_AFT_SPAR_CLASSES = frozenset({"boom", "gaff"})

# The canvas numbers the engine knows the strength of: Luce 1884 App. E pp. 610-611
# (docs/references/Tables.md §2) tabulates Nos. 1 to 9, No. 1 the heaviest.
CANVAS_NUMBERS = range(1, 10)

# Default load ratings (kN) by class, used with a warning when a file omits one.
DEFAULT_SPAR_RATING_KN: dict[str, float] = {
    "mast": 400.0,
    "topmast": 120.0,
    "topgallant_mast": 45.0,
    "royal_mast": 20.0,
    "bowsprit": 250.0,
    "jib_boom": 60.0,
    "flying_jib_boom": 25.0,
    "yard": 80.0,
    "gaff": 50.0,
    "boom": 60.0,
    "studdingsail_boom": 15.0,
    "lug_yard": 40.0,
    "lateen_yard": 60.0,
    "sprit": 30.0,
}
DEFAULT_LINE_RATING_KN: dict[str, float] = {
    "halyard": 40.0,
    "throat_halyard": 30.0,
    "peak_halyard": 25.0,
    "sheet": 35.0,
    "tack": 35.0,
    "brace": 25.0,
    "lift": 20.0,
    "clewline": 12.0,
    "buntline": 8.0,
    "leechline": 8.0,
    "bowline": 12.0,
    "reef_tackle": 15.0,
    "downhaul": 10.0,
    "outhaul": 15.0,
    "vang": 12.0,
    "guy": 15.0,
    "stay": 150.0,
    "shroud": 120.0,
    "backstay": 100.0,
}


# ---------------------------------------------------------------------------
# The crew section (docs/TechnicalSpec-M3.md §2.3)
# ---------------------------------------------------------------------------

# The stations of a ship's company, in the order the watch bill lists them. The first six
# are the seamen's stations; the ratings line divides the seamen among them.
CREW_STATIONS = (
    "forecastle",
    "fore_top",
    "main_top",
    "mizzen_top",
    "afterguard",
    "waisters",
    "marines",
    "idlers",
)
SEAMAN_STATIONS = CREW_STATIONS[:6]

# The ratings a ship file may share its seamen among, best first.
SEAMAN_RATINGS = ("able", "ordinary", "landsman")
RATINGS_SUM_TOLERANCE = 1e-6  # the shares must add up to one within this

# The idlers' trades (spec §2.1): what the `idlers_by_trade` mapping may name.
IDLER_TRADES = (
    "carpenter's crew",
    "sailmaker's crew",
    "cooper",
    "armourer",
    "cook",
    "steward",
    "servant",
    "surgeon's mate",
    "clerk",
    "master-at-arms's party",
)

# The ship's stores (spec §2.3): numbers only in milestone 3.
STORE_KEYS = (
    "water_tons",
    "provisions_days",
    "spare_sails",
    "spare_spars",
    "cordage_fathoms",
    "sails",  # milestone 3b: the sail room's contents, one entry a sail (spec 3b §6.3)
)
SPARE_SAIL_KEYS = ("kind", "canvas_no", "condition")


class ShipFileError(ValueError):
    """A ship file the engine cannot accept. The message is a sentence."""


# ---------------------------------------------------------------------------
# Specs
# ---------------------------------------------------------------------------


@dataclass
class RudderSpec:
    area_m2: float = 2.0
    max_angle_deg: float = 35.0
    rate_deg_s: float = 4.0


@dataclass
class HullSpec:
    length_waterline_m: float
    beam_m: float
    draught_m: float
    displacement_kg: float
    gm_m: float
    clr_x_m: float = 0.0
    lateral_area_m2: float | None = None
    hull_speed_kn: float | None = None
    deck_height_m: float = 1.5
    rudder: RudderSpec = field(default_factory=RudderSpec)


@dataclass
class SparSpec:
    id: str
    cls: str
    x_m: float | None = None
    height_m: float | None = None
    length_m: float | None = None
    on: str | None = None  # the spar this one is hoisted/fixed on (yard on a mast)
    steps_on: str | None = None  # the spar this mast stands on (topmast on lower mast)
    side: str | None = None  # studding sail booms
    brace_limit_deg: float | None = None  # yards
    rake_deg: float | None = None  # masts: positive rakes aft, negative forward (a polacre's fore)
    rating_kn: float | None = None
    # studding sail booms: rigged out at the start or not (spec 3b §7); None takes the default
    rigged_out: bool | None = None

    @property
    def parent(self) -> str | None:
        return self.on or self.steps_on


@dataclass
class SailSpec:
    id: str
    cls: str
    area_m2: float
    x_m: float
    centre_height_m: float
    reef_bands: int = 0
    side: str | None = None  # studding sails
    roles: dict[str, str] = field(default_factory=dict)  # yard/mast/gaff/boom/stay/sprit
    cloth_rating_kn: float | None = None
    canvas_no: int | None = None  # the canvas it is made of, 1 the heaviest (spec 3b §6.1)
    bent: bool = True  # false: the sail starts the voyage in the sail room (spec 3b §6.4)
    in_place_of: str | None = None  # the sail it is bent instead of (a storm mizzen: spanker)


@dataclass
class LineSpec:
    id: str
    cls: str
    of: str
    side: str | None = None
    rating_kn: float | None = None


@dataclass
class PostSpec:
    """A station holder: the post, and a name when the file gives one."""

    post: str
    name: str | None = None


@dataclass
class SpareSailSpec:
    """A sail in the sail room (spec 3b §6.3): the sail it is made for, the canvas it is
    made of, and how worn it is."""

    kind: str  # the id of the sail it is made for: "fore.topsail"
    canvas_no: int | None = None  # None: the same number as the sail it is made for
    condition: float = 100.0  # 0..100, as Sail.condition


@dataclass
class StoresSpec:
    water_tons: float = 0.0
    provisions_days: float = 0.0
    spare_sails: int = 0  # with a `sails` list, derived: the number of sails in it
    spare_spars: int = 0  # with a `spars` mapping, derived: the number of spares in it
    cordage_fathoms: float = 0.0
    sails: list[SpareSailSpec] | None = None  # the sail room, when the file lists it
    spars: dict[str, int] | None = None  # the booms by spar class (package 30b), when given so


@dataclass
class CrewSpec:
    """The ship's company as the ship file establishes it (spec M3 §2.3)."""

    complement: int
    names: str  # which list in data/crew/names.yaml
    stations: dict[str, int]  # every station in CREW_STATIONS order; absent ones are 0
    ratings: dict[str, float]  # share of the seamen by rating, SEAMAN_RATINGS order
    posts: list[PostSpec]
    idlers_by_trade: dict[str, int]  # in the file's order
    stores: StoresSpec = field(default_factory=StoresSpec)

    @property
    def seamen(self) -> int:
        return sum(self.stations[s] for s in SEAMAN_STATIONS)


@dataclass
class ShipSpec:
    name: str
    rig: str
    hull: HullSpec
    spars: list[SparSpec]
    sails: list[SailSpec]
    lines: list[LineSpec]
    groups: dict[str, list[str]]
    aliases: dict[str, str]
    era_notes: str = ""
    source: str = "<memory>"
    warnings: list[str] = field(default_factory=list)
    crew: CrewSpec | None = None  # None: no crew, and the runner has unlimited hands


# ---------------------------------------------------------------------------
# Parsing and validation
# ---------------------------------------------------------------------------

_SAIL_ROLE_KEYS = ("yard", "mast", "gaff", "boom", "stay", "sprit", "halyard_spar")


def _num(d: dict[str, Any], key: str, where: str, source: str, required: bool = True):
    v = d.get(key)
    if v is None:
        if required:
            raise ShipFileError(f"{source}: {where} is missing '{key}'.")
        return None
    if isinstance(v, bool) or not isinstance(v, int | float):
        raise ShipFileError(f"{source}: {where} has '{key}' = {v!r}, which is not a number.")
    return float(v)


def _str(d: dict[str, Any], key: str, where: str, source: str, required: bool = True):
    v = d.get(key)
    if v is None:
        if required:
            raise ShipFileError(f"{source}: {where} is missing '{key}'.")
        return None
    return str(v)


def parse_ship(data: dict[str, Any], source: str = "<memory>") -> ShipSpec:
    """Turn a loaded YAML dictionary into a validated ShipSpec."""
    if not isinstance(data, dict):
        raise ShipFileError(f"{source}: the file is not a mapping at the top level.")
    ship = data.get("ship") or {}
    name = str(ship.get("name") or "").strip()
    if not name:
        raise ShipFileError(f"{source}: 'ship.name' is missing.")
    rig = str(ship.get("rig") or "unspecified")
    era_notes = str(ship.get("era_notes") or "")
    warnings: list[str] = []

    hull = _parse_hull(data.get("hull"), source)
    spars = [_parse_spar(s, i, source) for i, s in enumerate(data.get("spars") or [])]
    sails = [_parse_sail(s, i, source) for i, s in enumerate(data.get("sails") or [])]
    lines = [_parse_line(ln, i, source) for i, ln in enumerate(data.get("lines") or [])]
    groups = {str(k): [str(x) for x in (v or [])] for k, v in (data.get("groups") or {}).items()}
    aliases = {str(k): str(v) for k, v in (data.get("aliases") or {}).items()}

    spec = ShipSpec(
        name=name,
        rig=rig,
        hull=hull,
        spars=spars,
        sails=sails,
        lines=lines,
        groups=groups,
        aliases=aliases,
        era_notes=era_notes,
        source=source,
        warnings=warnings,
        crew=_parse_crew(data["crew"], source) if data.get("crew") is not None else None,
    )
    validate(spec)
    return spec


def _parse_hull(h: Any, source: str) -> HullSpec:
    if not isinstance(h, dict):
        raise ShipFileError(f"{source}: 'hull' is missing.")
    where = "hull"
    r = h.get("rudder") or {}
    rudder = RudderSpec(
        area_m2=_num(r, "area_m2", "hull.rudder", source, required=False) or 2.0,
        max_angle_deg=_num(r, "max_angle_deg", "hull.rudder", source, required=False) or 35.0,
        rate_deg_s=_num(r, "rate_deg_s", "hull.rudder", source, required=False) or 4.0,
    )
    return HullSpec(
        length_waterline_m=_num(h, "length_waterline_m", where, source),
        beam_m=_num(h, "beam_m", where, source),
        draught_m=_num(h, "draught_m", where, source),
        displacement_kg=_num(h, "displacement_kg", where, source),
        gm_m=_num(h, "gm_m", where, source),
        clr_x_m=_num(h, "clr_x_m", where, source, required=False) or 0.0,
        lateral_area_m2=_num(h, "lateral_area_m2", where, source, required=False),
        hull_speed_kn=_num(h, "hull_speed_kn", where, source, required=False),
        deck_height_m=_num(h, "deck_height_m", where, source, required=False) or 1.5,
        rudder=rudder,
    )


def _parse_spar(s: Any, i: int, source: str) -> SparSpec:
    if not isinstance(s, dict):
        raise ShipFileError(f"{source}: spar #{i + 1} is not a mapping.")
    sid = _str(s, "id", f"spar #{i + 1}", source)
    where = f"spar '{sid}'"
    cls = _str(s, "class", where, source)
    if cls not in SPAR_CLASSES:
        raise ShipFileError(
            f"{source}: {where} has class '{cls}', which is not a spar class. "
            f"Known: {', '.join(sorted(SPAR_CLASSES))}."
        )
    side = _str(s, "side", where, source, required=False)
    if side is not None and side not in SIDES:
        raise ShipFileError(f"{source}: {where} has side '{side}'; use starboard or larboard.")
    return SparSpec(
        id=sid,
        cls=cls,
        x_m=_num(s, "x_m", where, source, required=False),
        height_m=_num(s, "height_m", where, source, required=False),
        length_m=_num(s, "length_m", where, source, required=False),
        on=_str(s, "on", where, source, required=False),
        steps_on=_str(s, "steps_on", where, source, required=False),
        side=side,
        brace_limit_deg=_num(s, "brace_limit_deg", where, source, required=False),
        rake_deg=_num(s, "rake_deg", where, source, required=False),
        rating_kn=_num(s, "rating_kn", where, source, required=False),
        rigged_out=_rigged_out(s, cls, where, source),
    )


def _rigged_out(s: dict, cls: str, where: str, source: str) -> bool | None:
    """A studding sail boom's starting state (spec 3b §7), if the file gives one."""
    value = s.get("rigged_out")
    if value is None:
        return None
    if not isinstance(value, bool):
        raise ShipFileError(
            f"{source}: {where} has rigged_out = {value!r}; say true (run out along its yard) "
            "or false (rigged in)."
        )
    if cls != "studdingsail_boom":
        raise ShipFileError(
            f"{source}: {where} is a {cls.replace('_', ' ')}; only a studding sail boom is "
            "rigged out or in."
        )
    return value


def _parse_sail(s: Any, i: int, source: str) -> SailSpec:
    if not isinstance(s, dict):
        raise ShipFileError(f"{source}: sail #{i + 1} is not a mapping.")
    sid = _str(s, "id", f"sail #{i + 1}", source)
    where = f"sail '{sid}'"
    cls = _str(s, "class", where, source)
    if cls not in SAIL_CLASSES:
        raise ShipFileError(
            f"{source}: {where} has class '{cls}', which is not a sail class. "
            f"Known: {', '.join(sorted(SAIL_CLASSES))}."
        )
    side = _str(s, "side", where, source, required=False)
    if side is not None and side not in SIDES:
        raise ShipFileError(f"{source}: {where} has side '{side}'; use starboard or larboard.")
    roles = {k: str(s[k]) for k in _SAIL_ROLE_KEYS if s.get(k) is not None}
    reef = s.get("reef_bands", 0)
    if isinstance(reef, bool) or not isinstance(reef, int) or reef < 0:
        raise ShipFileError(f"{source}: {where} has reef_bands = {reef!r}; use a whole number.")
    bent = s.get("bent", True)
    if not isinstance(bent, bool):
        raise ShipFileError(
            f"{source}: {where} has bent = {bent!r}; say true (bent to its spar) or false "
            f"(in the sail room)."
        )
    return SailSpec(
        id=sid,
        cls=cls,
        area_m2=_num(s, "area_m2", where, source),
        x_m=_num(s, "x_m", where, source),
        centre_height_m=_num(s, "centre_height_m", where, source),
        reef_bands=reef,
        side=side,
        roles=roles,
        cloth_rating_kn=_num(s, "cloth_rating_kn", where, source, required=False),
        canvas_no=_canvas_no(s.get("canvas_no"), where, source),
        bent=bent,
        in_place_of=_str(s, "in_place_of", where, source, required=False),
    )


def _canvas_no(v: Any, where: str, source: str) -> int | None:
    """A canvas number from 1 (the heaviest) to 9, or None when the file gives none."""
    if v is None:
        return None
    if isinstance(v, bool) or not isinstance(v, int) or v not in CANVAS_NUMBERS:
        raise ShipFileError(
            f"{source}: {where} has canvas_no = {v!r}; canvas is numbered 1 (the heaviest) "
            f"to {CANVAS_NUMBERS[-1]} (Luce 1884, App. E)."
        )
    return v


def _parse_line(ln: Any, i: int, source: str) -> LineSpec:
    if not isinstance(ln, dict):
        raise ShipFileError(f"{source}: line #{i + 1} is not a mapping.")
    lid = _str(ln, "id", f"line #{i + 1}", source)
    where = f"line '{lid}'"
    cls = _str(ln, "class", where, source)
    if cls not in LINE_CLASSES:
        raise ShipFileError(
            f"{source}: {where} has class '{cls}', which is not a line class. "
            f"Known: {', '.join(sorted(LINE_CLASSES))}."
        )
    side = _str(ln, "side", where, source, required=False)
    if side is not None and side not in SIDES:
        raise ShipFileError(f"{source}: {where} has side '{side}'; use starboard or larboard.")
    return LineSpec(
        id=lid,
        cls=cls,
        of=_str(ln, "of", where, source),
        side=side,
        rating_kn=_num(ln, "rating_kn", where, source, required=False),
    )


def validate(spec: ShipSpec) -> None:
    """Reject a spec the engine could not reason about. Fills in default ratings with warnings."""
    src = spec.source
    spars = {s.id: s for s in spec.spars}
    sails = {s.id: s for s in spec.sails}
    lines = {ln.id: ln for ln in spec.lines}

    # unique ids across all parts
    seen: dict[str, str] = {}
    for kind, items in (("spar", spec.spars), ("sail", spec.sails), ("line", spec.lines)):
        for it in items:
            if it.id in seen:
                raise ShipFileError(
                    f"{src}: id '{it.id}' is used for both a {seen[it.id]} and a {kind}."
                )
            seen[it.id] = kind

    missing_ratings: dict[tuple[str, str, float], list[str]] = {}

    # spars: parents exist, are spars, classes make sense, chains reach the hull, no cycles
    for s in spec.spars:
        if s.on and s.steps_on:
            raise ShipFileError(f"{src}: spar '{s.id}' has both 'on' and 'steps_on'; use one.")
        parent = s.parent
        if parent is None:
            if s.cls not in ROOT_SPAR_CLASSES:
                raise ShipFileError(
                    f"{src}: spar '{s.id}' is class '{s.cls}' but has no 'on' or 'steps_on'; "
                    f"only a mast or bowsprit stands on the hull by itself."
                )
        elif parent not in spars:
            raise ShipFileError(
                f"{src}: spar '{s.id}' is on '{parent}', but there is no spar with that id."
            )
        if s.cls == "studdingsail_boom" and s.side is None and not _on_fore_and_aft(s, spars):
            raise ShipFileError(f"{src}: studding sail boom '{s.id}' needs a 'side'.")
        if s.rake_deg is not None:
            if s.cls not in ("mast", "topmast", "topgallant_mast", "royal_mast"):
                raise ShipFileError(
                    f"{src}: spar '{s.id}' is a {s.cls}; only a mast takes 'rake_deg'."
                )
            if not -30.0 <= s.rake_deg <= 30.0:
                raise ShipFileError(
                    f"{src}: spar '{s.id}' has rake_deg = {s.rake_deg:g}; a mast rakes between "
                    f"-30 (forward) and 30 (aft) degrees."
                )
        if s.rating_kn is None:
            s.rating_kn = DEFAULT_SPAR_RATING_KN[s.cls]
            missing_ratings.setdefault(("spar", s.cls, s.rating_kn), []).append(s.id)
    for s in spec.spars:
        chain: list[str] = []
        cur: SparSpec | None = s
        while cur is not None:
            if cur.id in chain:
                path = " -> ".join(chain + [cur.id])
                raise ShipFileError(f"{src}: spar '{s.id}' stands on itself through {path}.")
            chain.append(cur.id)
            cur = spars.get(cur.parent) if cur.parent else None

    # sails: class requirements, roles exist and are the right kind
    for sl in spec.sails:
        req = SAIL_ROLE_REQUIREMENTS[sl.cls]
        opt = SAIL_OPTIONAL_ROLES.get(sl.cls, {})
        for role, allowed in req.items():
            target = sl.roles.get(role)
            if target is None:
                raise ShipFileError(
                    f"{src}: sail '{sl.id}' is class '{sl.cls}' but has no '{role}'."
                )
            _check_sail_role(spec, sl, role, target, allowed, spars, lines)
        for role, allowed in opt.items():
            target = sl.roles.get(role)
            if target is not None:
                _check_sail_role(spec, sl, role, target, allowed, spars, lines)
        for role in sl.roles:
            if role not in req and role not in opt:
                raise ShipFileError(
                    f"{src}: sail '{sl.id}' is class '{sl.cls}' and does not take a '{role}'."
                )
        if sl.cls == "studding" and sl.side is None:
            boom = spars.get(sl.roles.get("boom", ""))
            if boom is None or not (
                boom.cls in FORE_AND_AFT_SPAR_CLASSES or _on_fore_and_aft(boom, spars)
            ):
                raise ShipFileError(f"{src}: studding sail '{sl.id}' needs a 'side'.")
        if sl.in_place_of is not None:
            other = sails.get(sl.in_place_of)
            if other is None or other is sl:
                raise ShipFileError(
                    f"{src}: sail '{sl.id}' is bent in place of '{sl.in_place_of}', which is not "
                    f"another sail in the ship."
                )
        if sl.cls == "jibheaded" and "stay" not in sl.roles and "mast" not in sl.roles:
            raise ShipFileError(
                f"{src}: sail '{sl.id}' is jib-headed but names neither a 'stay' to hank to "
                f"nor a 'mast' to hoist on."
            )

    # lines: target exists and is a permitted kind
    for ln in spec.lines:
        kinds = LINE_TARGET_KINDS[ln.cls]
        if ln.of in spars:
            kind = "spar"
        elif ln.of in sails:
            kind = "sail"
        else:
            raise ShipFileError(
                f"{src}: line '{ln.id}' is of '{ln.of}', but there is no spar or sail with that id."
            )
        if kind not in kinds:
            raise ShipFileError(
                f"{src}: line '{ln.id}' is a {ln.cls}, which cannot be of a {kind} ('{ln.of}')."
            )
        if ln.cls == "brace" and spars[ln.of].cls not in YARD_LIKE_CLASSES:
            raise ShipFileError(
                f"{src}: line '{ln.id}' is a brace of '{ln.of}', which is a {spars[ln.of].cls}, "
                f"not a yard."
            )
        if ln.rating_kn is None:
            ln.rating_kn = DEFAULT_LINE_RATING_KN[ln.cls]
            missing_ratings.setdefault(("line", ln.cls, ln.rating_kn), []).append(ln.id)

    for (kind, cls, rating), ids in missing_ratings.items():
        shown = ", ".join(ids[:3]) + (", ..." if len(ids) > 3 else "")
        spec.warnings.append(
            f"{len(ids)} {kind}{'s' if len(ids) > 1 else ''} of class {cls} have no rating_kn "
            f"({shown}); using the default of {rating:g} kN."
        )

    # groups and aliases: members exist; names do not collide with ids
    for g, members in spec.groups.items():
        if g in seen:
            raise ShipFileError(f"{src}: group '{g}' has the same name as a part.")
        for m in members:
            if m not in seen:
                raise ShipFileError(f"{src}: group '{g}' lists '{m}', which is not a part.")
    for a, target in spec.aliases.items():
        if a in seen:
            raise ShipFileError(f"{src}: alias '{a}' has the same name as a part.")
        if target not in seen and target not in spec.groups:
            raise ShipFileError(
                f"{src}: alias '{a}' points at '{target}', which is not a part or a group."
            )

    # the sail room: every sail in it is made for a sail of this ship
    room = spec.crew.stores.sails if spec.crew is not None else None
    for spare in room or []:
        if spare.kind not in sails:
            raise ShipFileError(
                f"{src}: the sail room holds a sail made for '{spare.kind}', which is not a sail "
                f"in the ship."
            )


def _on_fore_and_aft(spar: SparSpec, spars: dict[str, SparSpec]) -> bool:
    """A spar that stands on a gaff sail's boom or gaff (a ringtail boom), which lies in the
    sail's plane and has no side of its own."""
    parent = spars.get(spar.parent) if spar.parent else None
    return parent is not None and parent.cls in FORE_AND_AFT_SPAR_CLASSES


def _check_sail_role(
    spec: ShipSpec,
    sl: SailSpec,
    role: str,
    target: str,
    allowed: frozenset[str],
    spars: dict[str, SparSpec],
    lines: dict[str, LineSpec],
) -> None:
    src = spec.source
    if role == "stay":
        ln = lines.get(target)
        if ln is None or ln.cls not in STANDING_LINE_CLASSES:
            raise ShipFileError(
                f"{src}: sail '{sl.id}' hanks to stay '{target}', "
                f"which is not a stay in the lines list."
            )
        return
    sp = spars.get(target)
    if sp is None:
        raise ShipFileError(
            f"{src}: sail '{sl.id}' names '{target}' as its {role}, but there is no such spar."
        )
    if allowed and sp.cls not in allowed:
        raise ShipFileError(
            f"{src}: sail '{sl.id}' names '{target}' as its {role}, but that is a {sp.cls}; "
            f"expected {' or '.join(sorted(allowed))}."
        )


# ---------------------------------------------------------------------------
# The crew section
# ---------------------------------------------------------------------------


def _count(v: Any, what: str, source: str) -> int:
    """A whole number of men (or casks, or sails), not negative."""
    if isinstance(v, bool) or not isinstance(v, int) or v < 0:
        raise ShipFileError(f"{source}: {what} is {v!r}; it must be a whole number, not negative.")
    return v


def _parse_spare_spars(raw: dict[Any, Any], source: str) -> dict[str, int]:
    """The stores' `spare_spars` given by class (package 30b): each key a spar class, each
    value the number of spares of it on the booms, in the file's order."""
    out: dict[str, int] = {}
    for k, v in raw.items():
        cls = str(k).strip()
        if cls not in SPAR_CLASSES:
            raise ShipFileError(
                f"{source}: the spare spars name the class '{cls}', which is not a spar class. "
                f"Known: {', '.join(sorted(SPAR_CLASSES))}."
            )
        out[cls] = _count(v, f"the number of spare {cls.replace('_', ' ')}s", source)
    return out


def _known(name: Any, known: tuple[str, ...], what: str, source: str) -> str:
    name = str(name)
    if name not in known:
        raise ShipFileError(
            f"{source}: the crew section names {what} '{name}', which is not one the engine "
            f"knows. Known: {', '.join(known)}."
        )
    return name


def _parse_sail_room(raw: Any, source: str) -> list[SpareSailSpec]:
    """The stores' `sails:` list (spec 3b §6.3): each entry a sail in the sail room."""
    if not isinstance(raw, list):
        raise ShipFileError(f"{source}: the sail room ('stores.sails') is not a list of sails.")
    out: list[SpareSailSpec] = []
    for i, e in enumerate(raw):
        where = f"sail #{i + 1} in the sail room"
        if not isinstance(e, dict) or not str(e.get("kind") or "").strip():
            raise ShipFileError(f"{source}: {where} does not say which sail it is made for.")
        for key in e:
            if key not in SPARE_SAIL_KEYS:
                raise ShipFileError(f"{source}: {where} has '{key}', which it does not take.")
        condition = e.get("condition", 100.0)
        if (
            isinstance(condition, bool)
            or not isinstance(condition, int | float)
            or not 0.0 <= condition <= 100.0
        ):
            raise ShipFileError(
                f"{source}: {where} has condition = {condition!r}; a sail's condition runs from "
                f"0 (worn out) to 100 (new)."
            )
        out.append(
            SpareSailSpec(
                kind=str(e["kind"]).strip(),
                canvas_no=_canvas_no(e.get("canvas_no"), where, source),
                condition=float(condition),
            )
        )
    return out


def _parse_crew(c: Any, source: str) -> CrewSpec:
    """Parse and check the ship file's `crew:` section (spec M3 §2.3)."""
    if not isinstance(c, dict):
        raise ShipFileError(f"{source}: 'crew' is not a mapping.")
    for key in c:
        if key not in (
            "complement",
            "names",
            "stations",
            "ratings",
            "posts",
            "idlers_by_trade",
            "stores",
        ):
            raise ShipFileError(f"{source}: the crew section has '{key}', which it does not take.")

    if c.get("complement") is None:
        raise ShipFileError(f"{source}: the crew section is missing 'complement'.")
    complement = _count(c["complement"], "the crew's complement", source)
    if complement == 0:
        raise ShipFileError(f"{source}: the crew's complement is 0; a ship needs hands.")

    names = str(c.get("names") or "").strip()
    if not names:
        raise ShipFileError(
            f"{source}: the crew section is missing 'names', the list the company is drawn from."
        )

    raw_stations = c.get("stations")
    if not isinstance(raw_stations, dict) or not raw_stations:
        raise ShipFileError(f"{source}: the crew section is missing 'stations'.")
    stations = {s: 0 for s in CREW_STATIONS}
    for k, v in raw_stations.items():
        name = _known(k, CREW_STATIONS, "the station", source)
        stations[name] = _count(v, f"the {name} station's number", source)

    seamen = sum(stations[s] for s in SEAMAN_STATIONS)
    raw_ratings = c.get("ratings") or {}
    if not isinstance(raw_ratings, dict):
        raise ShipFileError(f"{source}: the crew's 'ratings' is not a mapping.")
    if seamen and not raw_ratings:
        raise ShipFileError(
            f"{source}: the crew section has {seamen} seamen but no 'ratings' to rate them by."
        )
    ratings = {r: 0.0 for r in SEAMAN_RATINGS}
    for k, v in raw_ratings.items():
        name = _known(k, SEAMAN_RATINGS, "the rating", source)
        if isinstance(v, bool) or not isinstance(v, int | float) or not 0.0 <= v <= 1.0:
            raise ShipFileError(
                f"{source}: the {name} rating's share is {v!r}; a share is a number from 0 to 1."
            )
        ratings[name] = float(v)
    if raw_ratings:
        total = sum(ratings.values())
        if abs(total - 1.0) > RATINGS_SUM_TOLERANCE:
            raise ShipFileError(
                f"{source}: the crew's ratings add up to {total:g}; they are shares of the "
                f"seamen and must add up to one."
            )

    raw_posts = c.get("posts") or []
    if not isinstance(raw_posts, list):
        raise ShipFileError(f"{source}: the crew's 'posts' is not a list.")
    posts: list[PostSpec] = []
    for i, p in enumerate(raw_posts):
        if not isinstance(p, dict) or not str(p.get("post") or "").strip():
            raise ShipFileError(
                f"{source}: post #{i + 1} in the crew section does not say which post it is."
            )
        name = p.get("name")
        posts.append(
            PostSpec(post=str(p["post"]).strip(), name=str(name).strip() if name else None)
        )

    on_stations = sum(stations.values())
    if on_stations + len(posts) != complement:
        raise ShipFileError(
            f"{source}: the crew's stations hold {on_stations} and the posts {len(posts)}, "
            f"which make {on_stations + len(posts)}; the complement is {complement}. "
            f"The stations and the posts together must make up the complement."
        )

    raw_trades = c.get("idlers_by_trade") or {}
    if not isinstance(raw_trades, dict):
        raise ShipFileError(f"{source}: the crew's 'idlers_by_trade' is not a mapping.")
    trades: dict[str, int] = {}
    for k, v in raw_trades.items():
        name = _known(k, IDLER_TRADES, "the trade", source)
        trades[name] = _count(v, f"the number of the {name}", source)
    if sum(trades.values()) != stations["idlers"]:
        raise ShipFileError(
            f"{source}: the crew has {stations['idlers']} idlers, but 'idlers_by_trade' makes "
            f"{sum(trades.values())}; the trades must make up the idlers."
        )

    raw_stores = c.get("stores") or {}
    if not isinstance(raw_stores, dict):
        raise ShipFileError(f"{source}: the crew's 'stores' is not a mapping.")
    stores = StoresSpec()
    for k, v in raw_stores.items():
        name = _known(k, STORE_KEYS, "the store", source)
        if name == "sails":
            stores.sails = _parse_sail_room(v, source)
        elif name == "spare_spars" and isinstance(v, dict):
            stores.spars = _parse_spare_spars(v, source)
            stores.spare_spars = sum(stores.spars.values())
        elif name in ("spare_sails", "spare_spars"):
            setattr(stores, name, _count(v, f"the {name.replace('_', ' ')}", source))
        else:
            if isinstance(v, bool) or not isinstance(v, int | float) or v < 0:
                raise ShipFileError(
                    f"{source}: the store '{name}' is {v!r}; it must be a number, not negative."
                )
            setattr(stores, name, float(v))
    if stores.sails is not None:
        if "spare_sails" in raw_stores and stores.spare_sails != len(stores.sails):
            raise ShipFileError(
                f"{source}: the stores give {stores.spare_sails} spare sails but the sail room "
                f"lists {len(stores.sails)}; give the list alone, and the count follows from it."
            )
        stores.spare_sails = len(stores.sails)

    return CrewSpec(
        complement=complement,
        names=names,
        stations=stations,
        ratings=ratings,
        posts=posts,
        idlers_by_trade=trades,
        stores=stores,
    )
