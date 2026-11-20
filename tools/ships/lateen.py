"""The whole lateen's cut, shared by package 90's three lateen hulls (the tartane, the polacre and
the xebec): filled by the tartane's builder (docs/design/Plan-Package90.md §7.1, §7.2) and merged
alone, before the polacre's and the xebec's rigs are written; after that it passes to the
integrator, and an extension of it is a small commit of its own.

Pure: numbers in, dicts out, importing nothing of the generator or the game (the settee's cut,
`tools/ships/settee.py`, is the pattern; Design-ShipsEngineExtensions.md §9.3), reading nothing and
writing nothing. Every height is metres above the ship's own water and every x metres forward of
the middle of her load line, in the ship module's frame; the ship module writes the corners above
its datum, rates the yard and the lines through `gen_ships`, and files them. Each check raises
`ValueError` with a sentence, never `assert` (which `python -O` strips). `SHIP_MODULES` does not
name it, and it has no `build`: the hulls' modules import it.

What a whole lateen is here (its contract: docs/design/Design-Ship-Tartane.md §4.1 and §4.2,
docs/design/Design-Ship-Polacre.md §1.1 and §4.3, docs/design/Design-Ship-Xebec.md §4.2, and
docs/design/Design-Package90-Engine.md §2): a sail of class `lateen` with no `cut_at_mast`, its
head laced along a `lateen_yard` that is slung **a third of its length from its lower end** (the
*car*; the upper end the *penne*) on the mast's raked line (Lescallier 1791 p. 379; Fincham p.
60; Forfait 1788 Table II's yards). The head is the yard less its two ends (Forfait p. 121, read
OCR in Research-Tartane-2026-11.md §3.4). The sail is three-cornered (Lescallier p. 378, "voile
triangulaire"), and it is written with four corners `[tack, throat, peak, clew]`, as the engine's
lugs, settees and the mizen course are and as the viewer draws a whole lateen with its cut
(Ext §6.1, `lugCut`): the throat at the head's lower end on the yard, the tack a short luff
straight under it (the tack's lashing at the car), the peak at the head's upper end, the clew
where the hull's module puts it. A luff of nothing is refused: the drawing's figure of a sail in
its gear runs from the throat to the tack.

- `cut(...)`: the yard at its angle to the horizontal, slung on the mast's raked line at the given
  height; the four corners, the head, the luff, the leech and the foot, the area and the centre.
  The clew is given either as a point (`clew`, where the hull's module leads its sheet) or by the
  leech's and the foot's lengths (`leech_m`, `foot_m`: the lower of the two places where they
  meet, as the settee's).
- `lines(yard_id, sail_id)`: Lescallier p. 379's lines for a whole lateen, in the engine's classes.
- `check(...)`: the contract's checks on a cut and the lines written for its sail.
"""

from __future__ import annotations

import math

# Lescallier p. 379 (a lateen yard slung by its parrel at about a third of its length from the
# car), Fincham p. 60 and Steel 1794 vol. I p. 237: the sling a third of the yard from its lower
# end. Forfait's yards are slung so (Table II; Tar-D decision 7).
SLING_OF_YARD = 1.0 / 3.0
# The checks' tolerances: the sling on the mast's raked line within a decimetre (the settee's,
# Ext §5.1); the head within a centimetre of the yard less its ends.
ON_THE_LINE_M = 0.1
HEAD_BAND_M = 0.01

# Lescallier p. 379 (read OCR, Research-Tartane-2026-11.md §3.1; the bilander's mapping of the
# ourses, Design-Ship-Bilander.md §1.2), in the engine's classes:
# - the jeers (drisse), a `halyard` of the yard, through the calcet's sheave (Forfait p. 121);
# - the two ourses at the car, to windward (the ourse a proue and a poupe), a `guy` a side, as the
#   settee's ourses and the mizen course's bowlines are filed (Ext §3.4);
# - at the penne, to leeward, the brace (oste) on its pendant and the vang (van) on its pendant
#   and fall, which steadies the yard and takes its strain: each a `vang` a side, since a lateen
#   yard is no braced yard (Tar-D §4.1; Xeb-D §4.2; Ext §3.3);
# - one unsided `sheet` of the sail, hauled aft and to leeward (Lescallier p. 379);
# - one `tack` of the sail, the car tacked at the stem or the bow (Forfait p. 121).
# (id suffix, class, of: "yard" or "sail", sided)
LINES = (
    ("jeers", "halyard", "yard", False),
    ("ourse", "guy", "yard", True),
    ("oste", "vang", "yard", True),
    ("van", "vang", "yard", True),
    ("sheet", "sheet", "sail", False),
    ("tack", "tack", "sail", False),
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
    if a == 0.0:
        raise ValueError("the sail's corners enclose nothing; a sail has an area.")
    return abs(a), cx / (6.0 * a), cz / (6.0 * a)


def meet(p, rp, q, rq):
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


def _positive(word, value):
    if not (isinstance(value, (int, float)) and value > 0.0):
        raise ValueError(f"the lateen's {word} is {value!r}; it is more than nothing.")


def cut(
    *,
    yard_m,
    car_end_m,
    penne_end_m,
    yard_deg,
    sling_z,
    mast_x_at,
    luff_m,
    clew=None,
    leech_m=None,
    foot_m=None,
):
    """A whole lateen. `yard_m` the yard's length, `car_end_m` and `penne_end_m` its two ends
    beyond the head (Forfait Table II's "ends"); `yard_deg` the yard's angle to the horizontal,
    its penne aft and up; `sling_z` the sling's height above her water (where the jeers' block
    hangs) and `mast_x_at(z)` the x of the mast's raked line at a height above her water;
    `luff_m` the tack's drop under the throat. The clew is `clew`, a point (x, z), or where
    `leech_m` from the peak and `foot_m` from the tack meet, the lower of the two.

    Returns the corners [tack, throat, peak, clew] above her water, the sling (x, z), the yard's
    two ends (car, penne) as points, the yard's length and angle, the head, the luff, the leech
    and the foot, the area and the centre (x, z)."""
    for word, value in (
        ("yard", yard_m),
        ("luff", luff_m),
        ("sling's height", sling_z),
    ):
        _positive(word, value)
    for word, value in (("end at the car", car_end_m), ("end at the penne", penne_end_m)):
        if not (isinstance(value, (int, float)) and value >= 0.0):
            raise ValueError(f"the lateen yard's {word} is {value!r}; it is nothing or more.")
    if not 0.0 < yard_deg < 90.0:
        raise ValueError(
            f"the lateen yard stands at {yard_deg!r} degrees; it rises aft at more than nothing "
            "and less than upright."
        )
    head = yard_m - car_end_m - penne_end_m
    _positive("head", head)
    fore = SLING_OF_YARD * yard_m
    after = yard_m - fore
    if car_end_m >= fore or penne_end_m >= after:
        raise ValueError(
            f"the lateen yard's ends ({car_end_m:.2f} and {penne_end_m:.2f} m) reach past its "
            f"sling, {fore:.2f} m from the car; the head runs across the sling."
        )
    run, rise = math.cos(math.radians(yard_deg)), math.sin(math.radians(yard_deg))
    sling = (mast_x_at(sling_z), sling_z)
    car = (sling[0] + fore * run, sling[1] - fore * rise)
    penne = (sling[0] - after * run, sling[1] + after * rise)
    throat = (sling[0] + (fore - car_end_m) * run, sling[1] - (fore - car_end_m) * rise)
    peak = (sling[0] - (after - penne_end_m) * run, sling[1] + (after - penne_end_m) * rise)
    tack = (throat[0], throat[1] - luff_m)
    if clew is not None:
        if leech_m is not None or foot_m is not None:
            raise ValueError(
                "the lateen's clew is given twice; give a point, or a leech and a foot."
            )
        clew = (float(clew[0]), float(clew[1]))
    else:
        if leech_m is None or foot_m is None:
            raise ValueError("the lateen's clew is not given; give a point, or a leech and a foot.")
        _positive("leech", leech_m)
        _positive("foot", foot_m)
        clew = min(meet(tack, foot_m, peak, leech_m), key=lambda p: p[1])  # the lower
    corners = [tack, throat, peak, clew]
    area, cx, cz = area_centroid(corners)
    return {
        "corners": corners,
        "sling": sling,
        "car": car,
        "penne": penne,
        "yard_m": yard_m,
        "yard_deg": yard_deg,
        "head": head,
        "luff": luff_m,
        "leech": math.dist(peak, clew),
        "foot": math.dist(tack, clew),
        "area": area,
        "centre": (cx, cz),
    }


def lines(yard_id, sail_id):
    """Lescallier p. 379's lines of a whole lateen as written: (id, class, of, side), side None
    for the unsided; each line's id its yard's or its sail's id and its name, a side's after it."""
    out = []
    for name, cls, of, sided in LINES:
        owner = yard_id if of == "yard" else sail_id
        if sided:
            out += [(f"{owner}.{name}.{side}", cls, owner, side) for side in SIDES]
        else:
            out.append((f"{owner}.{name}", cls, owner, None))
    return out


def check(lateen, written_lines, *, mast_x_at, aft_x, sail_id, yard_m, ends, deck_at=None):
    """The contract's checks on a cut (`cut`'s dict, its corners as they will be written,
    rounded) and the lines written for its sail, each raised in words:
    - the point a third of the yard from the car more than a decimetre off the mast's raked line
      at its height (the yard's ends found from the head's corners and `ends`, (car, penne));
    - the head not the yard less its ends within a centimetre;
    - a luff of nothing (the drawing's figure of the sail in its gear runs from throat to tack);
    - the peak or the clew abaft `aft_x` (the taffrail, or the outrigger's end its sheet leads
      to);
    - with `deck_at(x)`, the deck's height above her water at x, the tack or the clew under it;
    - a sheet more than one, or sided; a tack more than one, or sided."""
    tack, throat, peak, clew = lateen["corners"]
    car_end, penne_end = ends
    head = math.dist(throat, peak)
    if abs(head - (yard_m - car_end - penne_end)) > HEAD_BAND_M:
        raise ValueError(
            f"the lateen's head is {head:.2f} m, against its yard of {yard_m:.2f} m less its ends "
            f"({car_end:.2f} and {penne_end:.2f} m); the head is the yard less its ends (Forfait "
            "p. 121)."
        )
    ux, uz = (throat[0] - peak[0]) / head, (throat[1] - peak[1]) / head  # along, to the car
    car = (throat[0] + car_end * ux, throat[1] + car_end * uz)
    sx = car[0] - SLING_OF_YARD * yard_m * ux
    sz = car[1] - SLING_OF_YARD * yard_m * uz
    off = sx - mast_x_at(sz)
    if abs(off) > ON_THE_LINE_M:
        raise ValueError(
            f"the lateen yard is slung {off:+.2f} m off the mast's raked line at {sz:.2f} m, a "
            f"third of the yard from the car; within {ON_THE_LINE_M:g} m is wanted."
        )
    if not math.dist(tack, throat) > 0.0:
        raise ValueError(
            "the lateen's tack stands on its throat; a whole lateen is written with a short luff "
            "under the throat, its four corners drawn (Ext §6.1)."
        )
    for word, corner in (("peak", peak), ("clew", clew)):
        if corner[0] < aft_x:
            raise ValueError(
                f"the lateen's {word} stands at x {corner[0]:.2f}, abaft {aft_x:.2f}, the "
                f"farthest its sheet leads; its {word} is inboard of it."
            )
    if deck_at is not None:
        for word, corner in (("tack", tack), ("clew", clew)):
            if corner[1] < deck_at(corner[0]):
                raise ValueError(
                    f"the lateen's {word} stands {corner[1]:.2f} m above her water at x "
                    f"{corner[0]:.2f}, under her deck there ({deck_at(corner[0]):.2f} m)."
                )
    for cls in ("sheet", "tack"):
        mine = [ln for ln in written_lines if ln[1] == cls and ln[2] == sail_id]
        if len(mine) != 1 or mine[0][3] is not None:
            raise ValueError(
                f"the lateen has {len(mine)} {cls}s, sided {[s[3] for s in mine]}; a whole lateen "
                f"has one unsided {cls} (Lescallier p. 379)."
            )
