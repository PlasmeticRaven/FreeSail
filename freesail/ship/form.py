"""The hull as drawn (package 75, stage 0H; docs/design/Build-Ships.md §3.5, §5.0, §5.3).

A ship file's `hull.profile` (`schema.HullProfile`) gives the hull's lines as points: the rail,
the half-breadths at the water and at the rail by station, the keel, the stem, the stern and the
midship section, and from stage 0H the shape keys beside them: the main breadth by station,
sourced section points, the stern's form and the fullness of the ends. This module turns them
into the hull the viewer draws, a section at each station from the keel (or §6's cut) up to the
rail and the ends closed to the stem and the stern, by §5.3's rule. It is pure and drawn only:
`/api/ship` serves its stations, and the generator's checks and the tests read it; nothing the
physics, the guns or the lee ports read is taken from it, and no port triple is ever written
from it (§5.0 principle 8).

Where the file gives a point it is drawn as given (§5.0 principle 5): `breadth_m`'s water and
rail, `breadth_line_m`'s main breadth, `sections_m`'s sourced points and `rail_m`'s top of the
side are passed through. The rule fills between and beyond them; it is the design's own, so a
line drawn by it is marked `judged` in a file:
- under the water, `section_m`'s shape scaled to the station's depth and to its half-breadth at
  the water, blended toward a straight V from the keel's edge as the ends are neared;
- above it, `section_m`'s upper shape fitted between the water, the main breadth and the rail,
  the main breadth lifted toward the ends by Steel's rule for the heights of breadth;
- between two stations of sourced points, the rule's section moved by their departures from the
  rule, straight between them, so that the side runs fair from one to the next.

A profile without `section_m` is drawn as §6's three points a station, as the viewer drew the
side before. Against measured lines it was not tuned on (the 64's and Lynx's), the rule is off
by a mean of 0.12-0.15 m in the band that 15 degrees of heel lifts out of the water
(tests/test_hull_form.py), and by a mean of 0.28-0.53 m over the whole body (Build-Ships.md §5.3,
measured in the session's scratch): enough for this pass, not for careening, so sourced points
replace it wherever they exist.

x is forward of midships and z above the file's waterline, in metres, as the profile has them;
a half-breadth is the distance out from the middle line. A station is its points (x, z, hb),
from its lowest up to the top of the side. The first and the last of `stations(spec)` close the
ends, along the stern and along the stem's fore edge, and their x changes with z. A station at a
rail point beyond the others (over a counter, or along the bow to the stem head) starts where
the end's line crosses its x, not at the keel.
"""

from __future__ import annotations

import math
from bisect import bisect_right
from collections.abc import Sequence
from dataclasses import dataclass
from functools import lru_cache
from typing import TYPE_CHECKING

from freesail.ship.profile import interp, rail_at
from freesail.units import RHO_WATER

if TYPE_CHECKING:
    from freesail.ship.schema import HullProfile, HullSpec

# §6's three points, the side the viewer drew before the form (client/projection.js,
# `hullFigures`): the side cut 0.8 m below the water at 0.92 of the water's half-breadth, the
# water and the rail (Build-Ships.md §6; judgement, the viewer's).
CUT_Z_M = -0.8
CUT_SHARE = 0.92
# The stations' gaps are kept under a sixteenth of the waterline's length (§5.3 step 1).
STATION_GAPS = 16
# The parallel body: under the water the blend toward the V is nothing within a quarter of the
# half-length each side of the greatest section, and rises straight to all of it at the
# waterline's ends (§5.3 step 3; judgement). The body is centred on the greatest section, not on
# midships, as the hull's design (§7) and its re-run measured it: the same mean, a smaller worst.
BODY_SHARE = 0.25
# Steel's rule for the heights of breadth (1805, OCR l. 15190-15194): the main breadth a few
# inches above the load line amidships, lifted toward the ends, to about the hawse holes forward
# and a little above the wing transom aft. As a share of the rail's height above the water,
# Steel's 36's: about a quarter at the greatest section, 0.70 at the foremost station and 0.45
# at the aftmost (measured: ships-design/pages-steel-1805-bodies.md §3.1, §5.2, 0.80 of 3.27 m
# at dead flat, 2.72 of 3.89 m at timber X, 1.92 of 4.27 m at timber 30).
BREADTH_LIFT_MID = 0.25
BREADTH_LIFT_FORE = 0.70
BREADTH_LIFT_AFT = 0.45
# The lift, and the main breadth's excess over the rail (the tumblehome), go from the greatest
# section's to the end stations' by f squared, f the body's share as under the water but
# reaching one at the end stations (judgement, measured on Steel's 36: the height of breadth so
# drawn within a mean of 0.06 m, where f alone leaves 0.15 m).
BREADTH_FADE_POWER = 2.0
# The fullness of the run and the entry where the file gives none: the default rule (§5.1).
DEFAULT_FULLNESS = (1.0, 1.0)
# The knuckle, the transom's foot, where a square or raked stern gives none: the water
# (judgement; a file with a transom names its knuckle, Build-Ships.md §5.1).
DEFAULT_KNUCKLE_Z_M = 0.0
# Recorded beside the file, never moved (§5.0 principle 8): a drawn displacement more than this
# share off the filed one, and a port triple more than this off the drawn side at its sill
# (§5.2: the generator's check, not a refusal).
DISPLACEMENT_RECORD_SHARE = 0.15
PORT_GAP_M = 0.05
# A given point is drawn through within a millimetre (§14.1).
THROUGH_M = 0.001
# The drawn displacement is summed over this many levels from the lowest point to the water.
DISPLACEMENT_LEVELS = 64
# The outlines for the pair check (§5.6): abeam, and ahead and astern (the fore body and the
# after body seen end on).
VIEWS = ("abeam", "ahead", "astern")

Point = tuple[float, float, float]
Station = tuple[Point, ...]

_EPS = 1e-9


# ---------------------------------------------------------------------------
# What the module gives
# ---------------------------------------------------------------------------


def stations(spec: HullSpec) -> tuple[Station, ...]:
    """The drawn hull by §5.3's rule, aft to forward: the stern's closure, a section at each
    station from its lowest point up to the top of the side, and the stem's closure. Each
    section is its points (x, z, hb), z rising; a closure's x follows the stern or the stem up.
    The sections at rail points beyond the others start where the end's line crosses them."""
    return _built(spec).stations


def half_breadth_at(spec: HullSpec, x: float, z: float) -> float:
    """The drawn side's half-breadth at x and z, metres: straight between two stations at the
    same height, and between the end station and the stem's or the stern's line toward the
    ends; nothing outside the hull (above the side, below it, or beyond the ends). Read by the
    tests and the generator's gap check, never by the physics or the lee ports."""
    return _half_breadth(_built(spec), float(x), float(z))


def outline(spec: HullSpec, view: str) -> tuple[tuple[float, float], ...]:
    """The drawn hull's outline in one view of `VIEWS`, a closed polygon normalised so that two
    hulls can be laid one over the other (§5.6, the pair check): abeam (x by the waterline's
    length, z by the freeboard above the water and the draught below it), from the taffrail
    along the top of the side to the stem head, down the stem's fore edge, aft along the bottom
    and up the stern's line; ahead and astern, the fore body's and the after body's widest at
    each height (the half-breadth by half the beam, on both sides; z as abeam)."""
    if view not in VIEWS:
        raise ValueError(f"the outline is drawn {', '.join(VIEWS)}, not '{view}'.")
    built = _built(spec)
    length, half_beam = spec.length_waterline_m, 0.5 * spec.beam_m
    freeboard = _top_at(built.profile, built.x_greatest)

    def up(z: float) -> float:
        return z / freeboard if z >= 0.0 else z / spec.draught_m

    if view == "abeam":
        aft, fore = built.stations[0], built.stations[-1]
        pts = [(s[-1][0], s[-1][1]) for s in built.stations]  # the tops, the closures' too
        pts += [(q[0], q[1]) for q in reversed(fore[:-1])]  # down the stem's fore edge
        pts += [(s[0][0], s[0][1]) for s in reversed(built.regular)]  # aft along the bottom
        pts += [(q[0], q[1]) for q in aft[:-1]]  # up the post, the counter and the stern
        ring = [pt for i, pt in enumerate(pts) if i == 0 or pt != pts[i - 1]]
        return tuple((x / length, up(z)) for x, z in ring)
    fore = view == "ahead"
    body = [
        s
        for s in built.stations[1:-1]
        if (s[0][0] >= built.x_greatest if fore else s[0][0] <= built.x_greatest)
    ]
    body.append(built.stations[-1] if fore else built.stations[0])
    levels = sorted({p[1] for s in body for p in s})
    widest = []
    for z in levels:
        over = [_hb_on(s, z) for s in body if s[0][1] - _EPS <= z <= s[-1][1] + _EPS]
        widest.append((max(over) if over else 0.0, z))
    side = [(hb / half_beam, up(z)) for hb, z in widest]
    return tuple(side + [(-u, v) for u, v in reversed(side)])


def drawn_displacement_kg(spec: HullSpec) -> float:
    """The drawn hull's displacement, kg: its volume under the water by levels from its lowest
    point, each level's waterplane straight between the stations, in sea water. Recorded beside
    the filed displacement, never put in its place (§5.0 principle 8)."""
    return _displacement(_built(spec))


def check(spec: HullSpec) -> list[str]:
    """The drawn hull checked against its file (§5.3; the generator's `hull_form` runs it):
    every figure finite, every section rising and no half-breadth less than nothing, no place
    given two half-breadths by two lines, every given point drawn through within a millimetre
    and the top of the side through every rail point between the ends, each else raising
    ValueError in words. What it returns are the lines the generator records in the notes,
    never moves: the drawn displacement and depth beside the filed ones, and each port triple's
    gap to the drawn side at its sill (§5.0 principle 8)."""
    built = _built(spec)
    p = built.profile
    for s in built.stations:
        for (x, z, hb), nxt in zip(s, s[1:] + (None,), strict=True):
            if not all(math.isfinite(v) for v in (x, z, hb)):
                raise ValueError(f"the drawn hull has a point {[x, z, hb]!r} that is not finite.")
            if hb < 0.0:
                raise ValueError(f"the drawn hull has a half-breadth of {hb:g} m at x {x:g}.")
            if nxt is not None and nxt[1] < z:
                raise ValueError(f"the drawn section at x {x:g} goes down from z {z:g}.")
    # every given point by its place, a sourced point first, then the main breadth's, then the
    # plan's: the first is drawn (`_station`), and a second that differs is refused
    given: dict[tuple[float, float], list[tuple[str, float]]] = {}
    for key, line in (("sections_m", p.sections_m), ("breadth_line_m", p.breadth_line_m)):
        for x, z, hb in line:
            given.setdefault((x, z), []).append((key, hb))
    for x, hw, hr in p.breadth_m:
        for z, hb in ((0.0, hw), (_top_at(p, x), hr)):
            given.setdefault((x, z), []).append(("breadth_m", hb))
    for (x, z), said in given.items():
        key, hb = said[0]
        for other, hb_other in said[1:]:
            if abs(hb_other - hb) > THROUGH_M:
                raise ValueError(
                    f"{key} and {other} give the half-breadth at x {x:g}, z {z:g} as {hb:g} m "
                    f"and {hb_other:g} m; a place given by two lines is given alike."
                )
        drawn = _half_breadth(built, x, z)
        if abs(drawn - hb) > THROUGH_M:
            raise ValueError(
                f"the drawn side misses {key}'s point at x {x:g}, z {z:g}: {drawn:.3f} m "
                f"against {hb:g} m."
            )
    # the top of the side through every rail point between the ends' lines at its height
    aft, fore = built.stations[0], built.stations[-1]
    tops = [(s[-1][0], s[-1][1]) for s in built.stations]
    for x, z in p.rail_m:
        if not _x_on(aft, z) + _EPS < x < _x_on(fore, z) - _EPS:
            continue
        drawn = interp(tops, x)
        if abs(drawn - z) > THROUGH_M:
            raise ValueError(
                f"the drawn top of the side misses rail_m's point at x {x:g}: z {drawn:.3f} m "
                f"against {z:g} m."
            )
    notes = []
    drawn_kg, filed_kg = _displacement(built), spec.displacement_kg
    share = drawn_kg / filed_kg - 1.0 if filed_kg else 0.0
    off = abs(share) > DISPLACEMENT_RECORD_SHARE
    notes.append(
        f"drawn displacement {drawn_kg / 1000.0:.0f} t against the filed "
        f"{filed_kg / 1000.0:.0f} t ({share:+.0%})"
        + (f", more than {DISPLACEMENT_RECORD_SHARE:.0%} off: recorded, not moved" if off else "")
    )
    deepest = min(pt[1] for pt in _station_at(built, built.x_greatest))
    notes.append(
        f"drawn {-deepest:.2f} m deep at the greatest section (x {built.x_greatest:g}) against "
        f"the file's draught of {spec.draught_m:g} m"
    )
    for word, triples in p.ports_m:
        for x, sill, hb in triples:
            gap = _half_breadth(built, x, sill) - hb
            over = f", over {PORT_GAP_M:g} m" if abs(gap) > PORT_GAP_M else ""
            notes.append(
                f"the {word} port at x {x:g}: the drawn side {gap:+.2f} m off its half-breadth "
                f"at the sill{over}"
            )
    return notes


# ---------------------------------------------------------------------------
# The rule (§5.3)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class _Built:
    """A profile drawn: its stations as served (the closures first and last, the stations at
    rail points beyond the others next to them), the regular sections the side is drawn
    straight between, the greatest section's x, and the profile itself."""

    profile: HullProfile
    stations: tuple[Station, ...]
    regular: tuple[Station, ...]
    x_greatest: float


@dataclass(frozen=True)
class _Rule:
    """What every station of one profile reads: its lines, the greatest section's x, the
    waterline's ends, the end stations, the midship section's figures and the fullness."""

    p: HullProfile
    draught: float
    x_greatest: float
    x_aft_end: float
    x_fore_end: float
    x_first: float
    x_last: float
    section: tuple[tuple[float, float], ...]  # (z, hb), z rising; empty: §6's three points
    run: float
    entry: float


def _built(spec: HullSpec) -> _Built:
    p = getattr(spec, "profile", None)
    if p is None:
        raise ValueError("a hull with no profile has no drawn form; the viewer draws its lens.")
    return _build(p, float(spec.draught_m), float(spec.length_waterline_m))


@lru_cache(maxsize=32)
def _build(p: HullProfile, draught: float, length: float) -> _Built:
    """The profile drawn (§5.3 steps 1 to 7). Kept for the profile, which is frozen, so that the
    server, the generator and the tests draw each hull once."""
    xs = _station_xs(p, length)
    rule = _rule(p, draught, xs)
    regular = []
    for x in xs:
        station = _station(rule, x)
        if station is not None:
            regular.append(station)
    if p.sections_m:
        regular = _carried(rule, regular)
    aft = _stern_closure(rule, regular[0])
    fore = _stem_closure(rule, regular[-1])
    abaft, before = _end_stations(p, aft, regular, fore)
    return _Built(
        profile=p,
        stations=(aft, *abaft, *regular, *before, fore),
        regular=tuple(regular),
        x_greatest=rule.x_greatest,
    )


def _rule(p: HullProfile, draught: float, xs: list[float]) -> _Rule:
    breadths = p.breadth_m
    greatest = max(hw for _x, hw, _hr in breadths)
    tied = [x for x, hw, _hr in breadths if hw == greatest]
    x_greatest = 0.5 * (tied[0] + tied[-1])  # the middle of a flat of greatest breadth
    fullness = p.form.fullness if p.form is not None and p.form.fullness else DEFAULT_FULLNESS
    return _Rule(
        p=p,
        draught=draught,
        x_greatest=x_greatest,
        x_aft_end=_end_x(p, "aft", 0.0),
        x_fore_end=_end_x(p, "fore", 0.0),
        x_first=xs[0],
        x_last=xs[-1],
        section=tuple(sorted(p.section_m)),
        run=fullness[0],
        entry=fullness[1],
    )


def _station_xs(p: HullProfile, length: float) -> list[float]:
    """§5.3 step 1: the x's of `breadth_m`, `sections_m` and `breadth_line_m`, and the rail's
    within theirs, so that the drawn top of the side passes through every rail point there and
    its steps stand; then stations added evenly where a gap is a sixteenth of the waterline's
    length or more. The rail's points beyond them are `_end_stations`'."""
    xs = {b[0] for b in p.breadth_m} | {s[0] for s in p.sections_m}
    xs |= {b[0] for b in p.breadth_line_m}
    lo, hi = min(xs), max(xs)
    xs |= {r[0] for r in p.rail_m if lo <= r[0] <= hi}
    xs_sorted = sorted(xs)
    gap = length / STATION_GAPS
    out = []
    for a, b in zip(xs_sorted, xs_sorted[1:], strict=False):
        out.append(a)
        n = math.ceil((b - a) / gap - _EPS)
        out.extend(a + (b - a) * k / n for k in range(1, n))
    out.append(xs_sorted[-1])
    return out


def _station(rule: _Rule, x: float, *, with_sourced: bool = True) -> Station | None:
    """The section at x (§5.3 steps 2 to 5 and 7), or None where the station lies beyond the
    hull at the water and at the rail both; `with_sourced` False, the bare rule's, as though
    the file gave no sourced point at x."""
    p = rule.p
    hb_w, hb_r = _water_and_rail(rule, x)
    if hb_w <= 0.0 and hb_r <= 0.0:
        return None
    z_r = _top_at(p, x)
    sourced = [(z, hb) for sx, z, hb in p.sections_m if sx == x] if with_sourced else []
    breadth = _main_breadth(rule, x, hb_w, hb_r, z_r, sourced)
    if rule.section:
        raw = _below(rule, x, hb_w) + _above(rule, hb_w, hb_r, z_r, breadth)
    else:  # step 7: §6's three points
        raw = [(CUT_Z_M, CUT_SHARE * hb_w), (0.0, hb_w), (z_r, hb_r)]
    # the given points, the sourced first: a sourced point wins over the plan's at its height
    anchors: dict[float, float] = {}
    for z, hb in sourced:
        anchors.setdefault(z, hb)
    if breadth is not None:
        anchors.setdefault(breadth[0], breadth[1])
    anchors.setdefault(0.0, hb_w)
    anchors.setdefault(z_r, hb_r)
    return tuple((x, z, hb) for z, hb in _through(raw, sorted(anchors.items())))


def _carried(rule: _Rule, regular: list[Station]) -> list[Station]:
    """§5.3 step 5 between the stations of sourced points and beyond them: a station with no
    sourced point of its own takes the rule's section moved, at each height, by its sourced
    neighbours' departures from the rule (the side drawn there less the bare rule's), straight
    in x between the two either side of it; beyond the outermost, that one's faded straight to
    nothing at the end station (judgement). So the rule fills between them and meets them, with
    no step where a sourced station stands among the rule's. The station's own given points,
    `breadth_m`'s and `breadth_line_m`'s at its x, are then drawn through again."""
    p = rule.p
    own = {x for x, _z, _hb in p.sections_m}
    xs = [s[0][0] for s in regular]
    src = [i for i, x in enumerate(xs) if x in own]
    if not src:
        return regular
    bare = {i: _station(rule, xs[i], with_sourced=False) for i in src}

    def departure(i: int, z: float) -> float:
        return _hb_on(regular[i], z) - _hb_on(bare[i], z)

    out = list(regular)
    for i, s in enumerate(regular):
        x = xs[i]
        if x in own:
            continue
        aft = [j for j in src if j < i]
        ahead = [j for j in src if j > i]
        if aft and ahead:
            a, b = aft[-1], ahead[0]
            weights = [(a, (xs[b] - x) / (xs[b] - xs[a])), (b, (x - xs[a]) / (xs[b] - xs[a]))]
        elif aft:  # forward of the foremost: faded to the foremost station
            a, end = aft[-1], len(xs) - 1
            weights = [(a, (xs[end] - x) / (xs[end] - xs[a]))]
        else:  # abaft the aftmost: faded to the aftmost station
            b = ahead[0]
            weights = [(b, (x - xs[0]) / (xs[b] - xs[0]))]
        low, top = s[0][1], s[-1][1]
        near = {xs[j] for j, _w in weights}
        levels = {pt[1] for pt in s}
        levels |= {z for sx, z, _hb in p.sections_m if sx in near and low < z < top}
        raw = [
            (z, max(_hb_on(s, z) + math.fsum(w * departure(j, z) for j, w in weights), 0.0))
            for z in sorted(levels)
        ]
        anchors: dict[float, float] = {}
        for bx, hw, hr in p.breadth_m:
            if bx == x:
                anchors.update({0.0: hw, top: hr})
        for bx, bz, bhb in p.breadth_line_m:
            if bx == x and bz < top:
                anchors.setdefault(bz, bhb)
        if anchors:
            raw = _through(raw, sorted(anchors.items()))
        out[i] = tuple((x, z, hb) for z, hb in raw)
    return out


def _water_and_rail(rule: _Rule, x: float) -> tuple[float, float]:
    """The half-breadths at the water and at the rail at x: `breadth_m`'s within its stations;
    beyond them, straight from its end station to the stem's or the stern's line at the water's
    and the rail's heights (to the transom there, above a transom stern's knuckle)."""
    p = rule.p
    lo, hi = p.breadth_m[0], p.breadth_m[-1]
    if lo[0] <= x <= hi[0]:
        return interp([(b[0], b[1]) for b in p.breadth_m], x), interp(
            [(b[0], b[2]) for b in p.breadth_m], x
        )
    side, end, way = ("fore", hi, 1.0) if x > hi[0] else ("aft", lo, -1.0)
    out = []
    for z, hb in ((0.0, end[1]), (_top_at(p, x), end[2])):
        x_end, hb_end = _end_x(p, side, z), _end_hb(p, side, z)
        if way * (x_end - x) <= 0.0:
            out.append(0.0)  # at or beyond the line
        else:
            out.append(hb + (hb_end - hb) * (x - end[0]) / (x_end - end[0]))
    return out[0], out[1]


def _top_at(p: HullProfile, x: float) -> float:
    """The drawn top of the side at x: `rail_m`'s within its points (`profile.rail_at`, which
    the swivels and pivots read and which this leaves alone); forward of its last point, where
    the stem head stands forward of it (a rail ending at a beakhead bulkhead, Build-Ships.md
    §5.1), straight from that point down to the stem head, `stem_m`'s top, as §6 closes the
    bow; abaft its first point likewise to the stern's top. Held beyond the stem head and the
    taffrail."""
    rail = p.rail_m
    for line, (x_r, z_r), way in ((p.stem_m, rail[-1], 1.0), (p.stern_m, rail[0], -1.0)):
        if line and way * (x - x_r) > 0.0 and way * (line[-1][0] - x_r) > 0.0:
            x_s, z_s = line[-1]
            return z_r + (z_s - z_r) * min(1.0, (x - x_r) / (x_s - x_r))
    return rail_at(p, x)


def _main_breadth(
    rule: _Rule,
    x: float,
    hb_w: float,
    hb_r: float,
    z_r: float,
    sourced: list[tuple[float, float]],
) -> tuple[float, float] | None:
    """§5.3 step 2: the main breadth at x, (z, hb): `breadth_line_m`'s within its stations, else
    by default (`judged`) Steel's heights of breadth and `section_m`'s greatest half-breadth,
    its excess over the rail faded to nothing at the end stations (beyond the line's stations,
    the default moved to meet its end); None without either, or where a sourced point above the
    water stands in for the default."""
    line = rule.p.breadth_line_m
    if line and line[0][0] <= x <= line[-1][0]:
        z = interp([(b[0], b[1]) for b in line], x)
        hb = interp([(b[0], b[2]) for b in line], x)
        return (z, hb) if z < z_r else None
    default = _default_breadth(rule, x, hb_w, hb_r, z_r)
    if default is None or any(sz > 0.0 for sz, _hb in sourced):
        return None
    z, hb = default
    if line:
        end = line[0] if x < line[0][0] else line[-1]
        at_end = _water_and_rail(rule, end[0])
        meet = _default_breadth(rule, end[0], at_end[0], at_end[1], _top_at(rule.p, end[0]))
        if meet is None:
            return None
        z, hb = z + end[1] - meet[0], hb + end[2] - meet[1]
    return (z, hb) if 0.0 < z < z_r else None


def _default_breadth(
    rule: _Rule, x: float, hb_w: float, hb_r: float, z_r: float
) -> tuple[float, float] | None:
    """The main breadth by default (`judged`): lifted from a quarter of the rail's height at the
    greatest section toward Steel's 36's shares at the end stations, and `section_m`'s greatest
    half-breadth, its excess over the rail at the greatest section faded to nothing there. None
    where the section is widest at or below the water or at its top."""
    sec = rule.section
    if not sec:
        return None
    widest = max(hb for _z, hb in sec)
    z_widest = max(z for z, hb in sec if hb == widest)
    if not 0.0 < z_widest < sec[-1][0]:
        return None
    f = _fraction(rule, x, rule.x_first, rule.x_last) ** BREADTH_FADE_POWER
    end = BREADTH_LIFT_FORE if x > rule.x_greatest else BREADTH_LIFT_AFT
    z = (BREADTH_LIFT_MID + (end - BREADTH_LIFT_MID) * f) * z_r
    excess = widest - _water_and_rail(rule, rule.x_greatest)[1]
    return z, max(hb_r + excess * (1.0 - f), hb_w, hb_r)


def _below(rule: _Rule, x: float, hb_w: float) -> list[tuple[float, float]]:
    """§5.3 step 3, under the water: `section_m`'s points below it scaled to the station's depth
    (by the keel's depth here against at the greatest section) and to its half-breadth at the
    water, blended toward a straight V from the keel's edge to the water by f^p, p the run's
    fullness abaft the greatest section and the entry's before it."""
    below = [(z, hb) for z, hb in rule.section if z < 0.0]
    if not below:
        return [(0.0, hb_w)]
    at_water = interp(rule.section, 0.0)
    k_z = _depth(rule, x) / _depth(rule, rule.x_greatest)
    k_y = hb_w / at_water if at_water > 0.0 else 0.0
    power = rule.entry if x > rule.x_greatest else rule.run
    w = _fraction(rule, x, rule.x_aft_end, rule.x_fore_end) ** power
    # the V's foot: the section's lowest point, the keel's edge, never wider than the water's
    # half-breadth here (judgement: near the ends the V narrows to the keel, never out from it)
    z_keel, hb_keel = below[0][0] * k_z, min(below[0][1], hb_w)
    out = []
    for z, hb in below:
        z_here = z * k_z
        v = hb_keel + (hb_w - hb_keel) * (z_here - z_keel) / -z_keel
        out.append((z_here, hb * k_y * (1.0 - w) + v * w))
    out.append((0.0, hb_w))
    return out


def _above(
    rule: _Rule, hb_w: float, hb_r: float, z_r: float, breadth: tuple[float, float] | None
) -> list[tuple[float, float]]:
    """§5.3 step 4, above the water: `section_m`'s upper shape fitted between the water, the main
    breadth and the rail. The section is taken in two pieces, the water to its own main breadth
    and that to its top (one piece, the water to its top, where the station has no main breadth
    or the section is widest at or below the water or at its top); each piece's ends are put on
    the station's, and each of its points keeps its offset from the piece's chord, in proportion
    to the station's main breadth against the section's, so that its tumblehome or its flare
    keeps its curve. In two pieces no point stands out beyond the wider of its piece's ends: the
    main breadth is the widest of the side, or the rail where she flares."""
    sec = rule.section
    top = sec[-1]
    widest = max(hb for _z, hb in sec)
    z_widest = max(z for z, hb in sec if hb == widest)
    water = (0.0, interp(sec, 0.0))
    if breadth is not None and 0.0 < breadth[0] < z_r and 0.0 < z_widest < top[0]:
        pieces = [
            (water, (z_widest, widest), (0.0, hb_w), breadth),
            ((z_widest, widest), top, breadth, (z_r, hb_r)),
        ]
        scale, bounded = breadth[1] / widest, True
    else:
        pieces = [(water, top, (0.0, hb_w), (z_r, hb_r))]
        scale, bounded = max(hb_w, hb_r) / widest, False
    out = []
    for (z0, h0), (z1, h1), (y0, g0), (y1, g1) in pieces:
        for z, hb in sec:
            if z0 < z <= z1:
                t = (z - z0) / (z1 - z0)
                off = hb - (h0 + (h1 - h0) * t)
                here = g0 + (g1 - g0) * t + off * scale
                out.append((y0 + (y1 - y0) * t, min(here, max(g0, g1)) if bounded else here))
    return out


def _through(
    raw: list[tuple[float, float]], anchors: list[tuple[float, float]]
) -> list[tuple[float, float]]:
    """§5.3 step 5: the rule's section `raw` brought through every given point: between two of
    them it is moved by the difference at each, straight in z, so that its own shape between
    them is kept; below the lowest it is scaled to meet it. (z, hb) rising, none less than
    nothing."""
    raw = sorted(raw)
    moves = [(z, hb - interp(raw, z)) for z, hb in anchors]
    z0, hb0 = anchors[0]
    at_low = interp(raw, z0)
    levels = sorted({z for z, _hb in raw} | {z for z, _hb in anchors})
    out = []
    for z in levels:
        here = interp(raw, z)
        if z < z0:
            hb = here * hb0 / at_low if at_low > 0.0 else here + moves[0][1]
        else:
            hb = here + interp(moves, z)
        out.append((z, max(hb, 0.0)))
    return out


def _fraction(rule: _Rule, x: float, x_aft: float, x_fore: float) -> float:
    """f: nothing within the body (a quarter of the half-length each side of the greatest
    section), rising straight to one at `x_aft` and `x_fore`, held beyond them."""
    half = 0.5 * (rule.x_fore_end - rule.x_aft_end)
    lo = rule.x_greatest - BODY_SHARE * half
    hi = rule.x_greatest + BODY_SHARE * half
    if lo <= x <= hi:
        return 0.0
    if x < lo:
        return 1.0 if x_aft >= lo else min(1.0, (lo - x) / (lo - x_aft))
    return 1.0 if x_fore <= hi else min(1.0, (x - hi) / (x_fore - hi))


def _depth(rule: _Rule, x: float) -> float:
    """The hull's depth below the water at x: the keel's (`keel_m`, else the draught), less
    where the stem's fore edge or the post comes up through it at x, forward of the forefoot
    and abaft the heel."""
    p = rule.p
    bottom = interp(p.keel_m, x) if p.keel_m else -rule.draught
    cuts = []
    if p.stem_m and x > p.stem_m[0][0]:  # forward of the forefoot
        cuts.append(_z_where(p.stem_m, x))
    if p.stern_m and x < p.stern_m[0][0]:  # abaft the heel
        cuts.append(_z_where(p.stern_m, x))
    for z in cuts:
        if z is not None:
            bottom = max(bottom, z)
    return max(-bottom, _EPS)


def _z_where(line: Sequence[Sequence[float]], x: float) -> float | None:
    """The lowest z at which a line of [x, z] points, low to high, passes x; None if it never
    does."""
    for (x0, z0), (x1, z1) in zip(line, line[1:], strict=False):
        if min(x0, x1) - _EPS <= x <= max(x0, x1) + _EPS:
            return z0 if abs(x1 - x0) < _EPS else z0 + (z1 - z0) * (x - x0) / (x1 - x0)
    return None


# ---------------------------------------------------------------------------
# The ends (§5.3 step 6)
# ---------------------------------------------------------------------------


def _end_x(p: HullProfile, side: str, z: float) -> float:
    """The end's line at height z: the stem's fore edge forward, the post, the counter and the
    taffrail aft (`stem_m`, `stern_m`, held beyond their ends); without one, the farther of the
    rail's and the half-breadths' end, straight up."""
    line = p.stem_m if side == "fore" else p.stern_m
    if line:
        return interp([(pt[1], pt[0]) for pt in line], z)
    if side == "fore":
        return max(p.breadth_m[-1][0], p.rail_m[-1][0])
    return min(p.breadth_m[0][0], p.rail_m[0][0])


def _end_hb(p: HullProfile, side: str, z: float) -> float:
    """The half-breadth the side closes to at the end's line, height z: nothing at the stem and
    the post, and at a round stern; the transom's above a square or raked stern's knuckle,
    straight from its half-breadth there to the taffrail's."""
    stern = p.form.stern if p.form is not None else None
    if side == "fore" or stern is None or stern.transom_hb_m is None or not p.stern_m:
        return 0.0
    knuckle = stern.knuckle_z_m if stern.knuckle_z_m is not None else DEFAULT_KNUCKLE_Z_M
    if z < knuckle:
        return 0.0
    taffrail = p.stern_m[-1][1]
    top, foot = stern.transom_hb_m
    t = min(1.0, (z - knuckle) / (taffrail - knuckle)) if taffrail > knuckle else 1.0
    return foot + (top - foot) * t


def _stern_closure(rule: _Rule, first: Station) -> Station:
    """The stern's closure, from the aftmost station's lowest height up to the taffrail: along
    the post to the centreline below the knuckle, along the transom above it (§5.3 step 6)."""
    return _closure(rule.p, "aft", first[0][1])


def _stem_closure(rule: _Rule, last: Station) -> Station:
    """The stem's closure, from the foremost station's lowest height up to the stem head, along
    the stem's fore edge to the centreline (§5.3 step 6)."""
    return _closure(rule.p, "fore", last[0][1])


def _closure(p: HullProfile, side: str, z_low: float) -> Station:
    line = p.stem_m if side == "fore" else p.stern_m
    if line:
        top = line[-1][1]
        levels = [z_low] + [pt[1] for pt in line if z_low < pt[1] < top] + [top]
    else:
        top = p.rail_m[-1][1] if side == "fore" else p.rail_m[0][1]
        levels = [z_low, max(top, z_low)]
    stern = p.form.stern if side == "aft" and p.form is not None else None
    if stern is not None and stern.transom_hb_m is not None and line:
        knuckle = stern.knuckle_z_m if stern.knuckle_z_m is not None else DEFAULT_KNUCKLE_Z_M
        if z_low < knuckle < top:
            levels.append(knuckle)
    out: list[Point] = []
    for z in sorted(set(levels)):
        x, hb = _end_x(p, side, z), _end_hb(p, side, z)
        if hb > 0.0 and out and out[-1][2] == 0.0:
            out.append((x, z, 0.0))  # the knuckle: the post's top, then the transom's foot
        out.append((x, z, hb))
    return tuple(out)


def _end_stations(
    p: HullProfile, aft: Station, regular: list[Station], fore: Station
) -> tuple[list[Station], list[Station]]:
    """The stations at `rail_m`'s points abaft and forward of the regular ones and inside the
    end's line at the rail's height (the rail over a counter, or along the bow to the stem
    head), so that the drawn top of the side passes through every rail point: the abaft ones
    and the forward ones, each aft to forward."""
    first, last = regular[0][0][0], regular[-1][0][0]
    abaft, before = [], []
    for x, _z in p.rail_m:
        if x < first:
            station = _end_station(p, aft, regular[0], x)
            if station is not None:
                abaft.append(station)
        elif x > last:
            station = _end_station(p, fore, regular[-1], x)
            if station is not None:
                before.append(station)
    return abaft, before


def _end_station(p: HullProfile, end: Station, station: Station, x: float) -> Station | None:
    """The side at x between the end station and the end's line, as `_toward_end` draws it:
    from where the end's line crosses x (the counter, the post or the stem) up to the top of
    the side, at the end's and the end station's heights between; None where x stands on or
    beyond the end's line at the top of the side."""
    way = 1.0 if x > station[0][0] else -1.0
    top = _top_at(p, x)
    if way * (_x_on(end, top) - x) <= _EPS:
        return None
    low = station[0][1]
    for (x0, z0, _h0), (x1, z1, _h1) in zip(end, end[1:], strict=False):
        if way * (x0 - x) >= 0.0:
            low = max(low, z0)
            break
        if way * (x1 - x) >= 0.0:
            low = max(low, z0 + (z1 - z0) * (x - x0) / (x1 - x0))
            break
    if low >= top - _EPS:
        return None
    levels = {low, top} | {pt[1] for pt in end + station if low < pt[1] < top}
    return tuple((x, z, _toward_end(end, station, x, z, p)) for z in sorted(levels))


# ---------------------------------------------------------------------------
# Reading the drawn hull
# ---------------------------------------------------------------------------


def _hb_on(station: Station, z: float) -> float:
    """A station's half-breadth at height z, held at its lowest and its highest; where two of
    its points stand at one height (a transom's foot), the upper is taken from that height up."""
    zs = [pt[1] for pt in station]
    if z <= zs[0]:
        return station[0][2]
    if z >= zs[-1]:
        return station[-1][2]
    i = bisect_right(zs, z) - 1
    (_x0, z0, h0), (_x1, z1, h1) = station[i], station[i + 1]
    if z == z0 or z1 <= z0:
        return h0
    return h0 + (h1 - h0) * (z - z0) / (z1 - z0)


def _x_on(station: Station, z: float) -> float:
    """A closure's x at height z, held at its lowest and its highest."""
    zs = [pt[1] for pt in station]
    if z <= zs[0]:
        return station[0][0]
    if z >= zs[-1]:
        return station[-1][0]
    i = bisect_right(zs, z) - 1
    (x0, z0, _h0), (x1, z1, _h1) = station[i], station[i + 1]
    return x0 if z1 <= z0 else x0 + (x1 - x0) * (z - z0) / (z1 - z0)


def _station_at(built: _Built, x: float) -> Station:
    """The regular station nearest x."""
    return min(built.regular, key=lambda s: abs(s[0][0] - x))


def _half_breadth(built: _Built, x: float, z: float) -> float:
    regular = built.regular
    xs = [s[0][0] for s in regular]
    if x < xs[0]:
        return _toward_end(built.stations[0], regular[0], x, z, built.profile)
    if x > xs[-1]:
        return _toward_end(built.stations[-1], regular[-1], x, z, built.profile)
    if len(regular) == 1:
        a = b = regular[0]
        t = 0.0
    else:
        i = min(bisect_right(xs, x) - 1, len(regular) - 2)
        a, b = regular[i], regular[i + 1]
        t = (x - xs[i]) / (xs[i + 1] - xs[i])
    top = a[-1][1] + (b[-1][1] - a[-1][1]) * t
    low = a[0][1] + (b[0][1] - a[0][1]) * t
    if z > top + _EPS or z < low - _EPS:
        return 0.0
    return _hb_on(a, z) + (_hb_on(b, z) - _hb_on(a, z)) * t


def _toward_end(end: Station, station: Station, x: float, z: float, p: HullProfile) -> float:
    """Between the end station and the stem's or the stern's line: straight at each height from
    the station's half-breadth to the line's, the line's own on it (a transom's above its
    knuckle); the side's top the top of the side (`_top_at`, through the rail's points there)
    and its foot straight from the station's to the line's own; nothing beyond the line."""
    x_s = station[0][0]
    way = 1.0 if x > x_s else -1.0
    x_end = _x_on(end, z)
    if way * (x_end - x) < -_EPS or way * (x_end - x_s) <= 0.0:
        return 0.0
    t = min(1.0, (x - x_s) / (x_end - x_s))
    top = _top_at(p, x)
    low = _toward(station[0][1], end[0][1], x, x_s, end[0][0])
    if z > top + _EPS or z < low - _EPS:
        return 0.0
    return _hb_on(station, z) + (_hb_on(end, z) - _hb_on(station, z)) * t


def _toward(v_s: float, v_end: float, x: float, x_s: float, x_end: float) -> float:
    if abs(x_end - x_s) < _EPS:
        return v_s
    t = min(1.0, max(0.0, (x - x_s) / (x_end - x_s)))
    return v_s + (v_end - v_s) * t


def _displacement(built: _Built) -> float:
    low = min(pt[1] for s in built.stations for pt in s)
    if low >= 0.0:
        return 0.0
    aft, regular, fore = built.stations[0], built.regular, built.stations[-1]
    areas = []
    for k in range(DISPLACEMENT_LEVELS + 1):
        z = low * (1.0 - k / DISPLACEMENT_LEVELS)
        line = [(s[0][0], _half_breadth(built, s[0][0], z)) for s in regular]
        # each end's line where it stands beyond the end station at this height (at the
        # forefoot or the heel it may not: the waterplane then ends at the station)
        x_aft, x_fore = _x_on(aft, z), _x_on(fore, z)
        if x_aft < line[0][0]:
            line.insert(0, (x_aft, _end_reach(aft, regular[0], z)))
        if x_fore > line[-1][0]:
            line.append((x_fore, _end_reach(fore, regular[-1], z)))
        areas.append(
            sum((x1 - x0) * (h0 + h1) for (x0, h0), (x1, h1) in zip(line, line[1:], strict=False))
        )  # both sides: twice the half-breadth's trapezoids, each half the sum
    dz = -low / DISPLACEMENT_LEVELS
    volume = dz * (0.5 * areas[0] + sum(areas[1:-1]) + 0.5 * areas[-1])
    return volume * RHO_WATER


def _end_reach(end: Station, station: Station, z: float) -> float:
    """The half-breadth on the end's line at height z, where the side reaches it there."""
    if z < station[0][1] - _EPS or z > end[-1][1] + _EPS:
        return 0.0
    return _hb_on(end, z)
