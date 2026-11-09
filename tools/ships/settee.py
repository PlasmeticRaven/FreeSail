"""The bilander's settee cut to D5 (a) on its yard, and its lines (package 75; the bilander's
design, docs/design/Design-Ship-Bilander.md, cited here as Bil-D, §4.4; the engine's design,
docs/design/Design-ShipsEngineExtensions.md, cited here as Ext, §5.1 and §9.3). Written by the
bilander's builder (B4).

Pure: numbers in, dicts out, importing nothing from the generator (Ext §9.3), so that no second
copy of `gen_ships` arises from it. Every height is metres above the ship's own water and every x
metres forward of the middle of her load line, in the ship module's frame; the ship module writes
the corners above its datum, rates the yard and the lines through `gen_ships`, and files them.
Each check raises `ValueError` with a sentence, never `assert` (which `python -O` strips), so that
a settee that breaks Ext §5.1's contract cannot be written.

- `cut(...)`: the settee by D5 (a) (docs/design/Decisions-ShipsRound2-2026-10.md): the head on
  the yard at its angle to the horizontal, slung a third of the way along it from the throat on
  the mast's raked line; the luff upright under the throat from the tack, the leech and the foot
  each 0.72 of the head and the luff 0.16 of the leech; the clew where the foot from the tack
  meets the leech from the peak, the lower of the two. Corners `[tack, throat, peak, clew]`, the
  area and the centre by the corners.
- `lines(yard_id, sail_id)`: Lescallier's lines for the settee (p. 390, Pl. XVII fig. 7's
  letters; Bil-D §4.4; Ext §5.1), by id, class, what they belong to and side; the ship module
  gives their sizes and rates them.
- `check(...)`: Ext §9.3's checks on the cut and its lines.
"""

from __future__ import annotations

import math

# D5 (a) (Bil-D §4.4; Ext §5.1): the leech and the foot each 0.72 of the head, the luff 0.16 of
# the leech (Gwyn's ratios, Research-Bilander-2026-10.md §2.3), the yard slung a third of the
# way along the head from the throat (Lescallier pp. 377-380 and Steel 1794 vol. I p. 237 for a
# lateen yard; Chapman's 0.32-0.33, measured).
LEECH_OF_HEAD = 0.72
FOOT_OF_HEAD = 0.72
LUFF_OF_LEECH = 0.16
SLING_OF_HEAD = 1.0 / 3.0
# The checks' tolerances (Ext §9.3; Bil-D §4.4): the sling on the mast's raked line within a
# decimetre; each ratio within a hundredth of D5 (a).
ON_THE_LINE_M = 0.1
RATIO_BAND = 0.01

# Lescallier p. 390 with the letters of Pl. XVII fig. 7 (Research-Bilander-2026-10.md §1.2,
# read; Ext §5.1), in the engine's classes: the jeers (drisse, p), a halyard of the yard; the
# derrick (balancine ou martinet, o), a lift of the yard; the peak brace (bras, t), the English
# vangs, a vang a side; the ourses (q), the English bowlines at the heel, a guy a side (a bowline
# is a sail's line in the engine); the tacks (amures, r), a tack a side; one unsided sheet
# (ecoute, s) to the taffrail; and the clewlines and the buntline "comme pour les voiles
# quarrees". (id suffix, class, of: "yard" or "sail", sided)
LINES = (
    ("jeers", "halyard", "yard", False),
    ("derrick", "lift", "yard", False),
    ("vang", "vang", "yard", True),
    ("ourse", "guy", "yard", True),
    ("tack", "tack", "sail", True),
    ("sheet", "sheet", "sail", False),
    ("clewline", "clewline", "sail", True),
    ("buntline", "buntline", "sail", False),
)
SIDES = ("starboard", "larboard")


def area_centroid(pts):
    """A sail's area and the centroid of its corners (x, z), by the shoelace (the generator's
    `_quad_area_centroid`, here so that this module imports nothing of it)."""
    a = cx = cz = 0.0
    n = len(pts)
    for i in range(n):
        x1, z1 = pts[i]
        x2, z2 = pts[(i + 1) % n]
        cross = x1 * z2 - x2 * z1
        a += cross
        cx += (x1 + x2) * cross
        cz += (z1 + z2) * cross
    a *= 0.5
    return abs(a), cx / (6.0 * a), cz / (6.0 * a)


def _meet(p, rp, q, rq):
    """The two points at `rp` from `p` and `rq` from `q` (where the two circles cross)."""
    dx, dz = q[0] - p[0], q[1] - p[1]
    d = math.hypot(dx, dz)
    if d > rp + rq or d < abs(rp - rq) or d == 0.0:
        raise ValueError(
            f"the foot of {rp:.2f} m from the tack and the leech of {rq:.2f} m from the peak "
            f"cannot meet, the two corners standing {d:.2f} m apart."
        )
    a = (rp * rp - rq * rq + d * d) / (2.0 * d)
    h = math.sqrt(max(rp * rp - a * a, 0.0))
    mx, mz = p[0] + a * dx / d, p[1] + a * dz / d
    return [(mx + h * dz / d, mz - h * dx / d), (mx - h * dz / d, mz + h * dx / d)]


def cut(*, head_m, yard_deg, tack_z, mast_x_at, yard_m=None):
    """The settee by D5 (a). `head_m` the head's length, `yard_deg` its angle to the horizontal,
    rising aft; `tack_z` the tack's height above her water; `mast_x_at(z)` the x of the mast's
    raked line at a height above her water. `yard_m`, the yard's length, is the head's when not
    given (Bil-D §4.4: the drawing draws a settee's yard as its head; B5.4's finding). Returns the
    corners [tack, throat, peak, clew] above her water, the sling (x, z), the yard's length, the
    luff, the leech and the foot, the area and the centre (x, z)."""
    if not head_m > 0.0:
        raise ValueError(f"the settee's head is {head_m!r} m; a head is more than nothing.")
    if not 0.0 < yard_deg < 90.0:
        raise ValueError(
            f"the settee's yard stands at {yard_deg!r} degrees; it rises aft at more than nothing "
            "and less than upright."
        )
    leech = LEECH_OF_HEAD * head_m
    foot = FOOT_OF_HEAD * head_m
    luff = LUFF_OF_LEECH * leech
    run = math.cos(math.radians(yard_deg)) * head_m * SLING_OF_HEAD
    rise = math.sin(math.radians(yard_deg)) * head_m * SLING_OF_HEAD
    # the luff upright under the throat, the throat a third of the head from the sling, which is
    # on the mast's raked line: the sling's height fixes its x, and the throat's x is the tack's
    sling_z = tack_z + luff + rise
    sling_x = mast_x_at(sling_z)
    throat = (sling_x + run, sling_z - rise)
    peak = (sling_x - 2.0 * run, sling_z + 2.0 * rise)
    tack = (throat[0], tack_z)
    clew = min(_meet(tack, foot, peak, leech), key=lambda p: p[1])  # the lower
    corners = [tack, throat, peak, clew]
    area, cx, cz = area_centroid(corners)
    return {
        "corners": corners,
        "sling": (sling_x, sling_z),
        "yard_m": head_m if yard_m is None else yard_m,
        "head": head_m,
        "luff": luff,
        "leech": leech,
        "foot": foot,
        "area": area,
        "centre": (cx, cz),
    }


def lines(yard_id, sail_id):
    """Ext §5.1's lines of the settee as written: (id, class, of, side), side None for the
    unsided; each line's id its yard's or its sail's id and its name, a side's after it."""
    out = []
    for name, cls, of, sided in LINES:
        owner = yard_id if of == "yard" else sail_id
        if sided:
            out += [(f"{owner}.{name}.{side}", cls, owner, side) for side in SIDES]
        else:
            out.append((f"{owner}.{name}", cls, owner, None))
    return out


def check(settee, written_lines, *, mast_x_at, taffrail_x, sail_id):
    """Ext §9.3's checks on a cut (`cut`'s dict, its corners as they will be written, rounded)
    and the lines written for its sail, each raised in words: the point a third of the way
    along the head from the throat more than a decimetre off the mast's raked line at its
    height; the peak or the clew abaft the taffrail; a sheet more than one, or sided; a corner's
    ratio more than a hundredth off D5 (a)."""
    tack, throat, peak, clew = settee["corners"]
    sx = throat[0] + (peak[0] - throat[0]) * SLING_OF_HEAD
    sz = throat[1] + (peak[1] - throat[1]) * SLING_OF_HEAD
    off = sx - mast_x_at(sz)
    if abs(off) > ON_THE_LINE_M:
        raise ValueError(
            f"the settee's yard is slung {off:+.2f} m off the mast's raked line at {sz:.2f} m, "
            f"a third of the way from the throat; within {ON_THE_LINE_M:g} m is wanted (Ext "
            "§5.1)."
        )
    for word, corner in (("peak", peak), ("clew", clew)):
        if corner[0] < taffrail_x:
            raise ValueError(
                f"the settee's {word} stands at x {corner[0]:.2f}, abaft the taffrail at "
                f"{taffrail_x:.2f}; its {word} is inboard (Ext §5.1)."
            )
    sheets = [ln for ln in written_lines if ln[1] == "sheet" and ln[2] == sail_id]
    if len(sheets) != 1 or sheets[0][3] is not None:
        raise ValueError(
            f"the settee has {len(sheets)} sheets, sided {[s[3] for s in sheets]}; it has one "
            "unsided sheet, led aft to the taffrail (Ext §5.1)."
        )
    head = math.dist(throat, peak)
    leech = math.dist(peak, clew)
    foot = math.dist(tack, clew)
    luff = math.dist(tack, throat)
    for word, got, want in (
        ("the leech over the head", leech / head, LEECH_OF_HEAD),
        ("the foot over the head", foot / head, FOOT_OF_HEAD),
        ("the luff over the leech", luff / leech, LUFF_OF_LEECH),
    ):
        if abs(got - want) > RATIO_BAND:
            raise ValueError(
                f"the settee's corners give {word} {got:.3f}, against D5 (a)'s {want:g}; "
                f"within {RATIO_BAND:g} is wanted."
            )
