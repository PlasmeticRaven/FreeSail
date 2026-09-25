"""The ship file format: what a ship definition may contain, and its validation.

A ship file (YAML, see docs/TechnicalSpec-M0-M2.md §6) lists a hull, spars,
sails and lines, with *role links* between them (`on`, `steps_on`, `yard`,
`mast`, `gaff`, `boom`, `stay`, `of`). This module turns the raw dictionary
into typed specs and rejects anything the engine could not reason about,
with an error written as a sentence naming the file and the part.

Nothing here knows about any particular rig. It knows about part classes and
what each class requires.
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
    "studding": {"boom": frozenset({"studdingsail_boom"})},
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


@dataclass
class LineSpec:
    id: str
    cls: str
    of: str
    side: str | None = None
    rating_kn: float | None = None


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
    )


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
    )


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
        if s.cls == "studdingsail_boom" and s.side is None:
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
            raise ShipFileError(f"{src}: studding sail '{sl.id}' needs a 'side'.")
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
