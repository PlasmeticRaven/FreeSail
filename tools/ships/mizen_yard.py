"""The mizen course cut at the mast on its lateen yard, and Steel's driver boomsail bent in its
place (package 75; docs/design/Design-ShipsEngineExtensions.md, cited here as Ext, §3.4 and
§17.2). Written by the 64's builder (B1) and imported by the 74's.

Pure: numbers in, dicts out, importing nothing from the generator (Ext §9.3), so that no second
copy of `gen_ships` arises from it. Every height is metres above the ship's own water and every
x metres forward of the middle of her load line, in the ship module's frame; the ship module
writes them above its datum, rates the spars and the lines through `gen_ships`, and files them.
Each cut raises `ValueError` with a sentence, never `assert`, when what it writes would break
the contract (Ext §3.4, §17.2: "a bad file cannot be written").

- `course(...)`: the yard and the course cut at the mast from Steel's cloths and leeches: the
  tack and the throat on the mast's raked line, the head running aft and up to the peak along
  the yard, the foot level and loose to the clew; corners `[tack, throat, peak, clew]`.
- `driver(...)`: Steel's driver boomsail (Steel 1794 vol. I, DRIVER BOOMSAIL, OCR l.
  13816-13843): the throat the course's, the tack at the boom's jaws down the mast's raked line,
  the head along the mizen yard's line and on past its peak on the driver yard, the foot along
  the level boom; and the boom.
- `least_jaws(...)`: the lowest jaws for the boom that clear what stands under it by its head
  room and keep the driver's after leech within Steel's band.
- `COURSE_LINES`, `DRIVER_LINES`: the lines of each, by id, class, what they belong to and
  whether sided (Ext §3.4; §17.2); the ship module gives their sizes and rates them.
"""

from __future__ import annotations

import math

FOOT_M = 0.3048
YARD_M = 3.0 * FOOT_M
# Steel's cloth in the sail, 22 1/2 in: 24-in canvas less the seam for ships of 50 guns and up
# (Steel 1794 vol. I, the sail-making rules; Ind §5, judgement there), each cloth a vertical
# strip, so that a head's or a foot's cloths give its run fore and aft.
CLOTH_M = 22.5 / 12.0 * FOOT_M
# The checks' tolerances: a corner on its line within a decimetre (Ext §3.4, §17.2); a cut's
# area within a tenth of Steel's rule (Ind §5; Ext §17.2).
ON_THE_LINE_M = 0.1
AREA_BAND = 0.10
# The driver yard's reach: the peak no more than two-thirds of the driver yard beyond the mizen
# yard's peak, Lever's outer halyards being bent to it "about one-third from the inner Arm"
# (Lever 1808, OCR l. 8282-8285; Ext §17.2).
DRIVER_YARD_REACH = 2.0 / 3.0
# The driver's after leech "two to four yards deeper" than the mizen course's (Steel 1794 vol.
# I, DRIVER BOOMSAIL, OCR l. 13816-13843; Ext §17.2's band).
AFTER_LEECH_DEEPER_YD = (2.0, 4.0)

# The course's lines (Ext §3.4; Steel 1794 vol. II p. 37; Lavery 1985 I32): the jeers, a halyard
# of the yard; the lifts and Steel's derrick, lifts of the yard; the vangs; the bowlines at the
# heel, guys of the yard (a bowline is a sail's line in the engine); one unsided sheet to the
# taffrail; one tack forward of the mast. No brace and no brails: the engine has no brail line,
# and the yard is trimmed by the sheet and the vangs (Ext §3.3). (id suffix, class, of, sided)
COURSE_LINES = (
    ("yard.jeers", "halyard", "yard", False),
    ("yard.derrick", "lift", "yard", False),
    ("yard.lift", "lift", "yard", True),
    ("yard.vang", "vang", "yard", True),
    ("yard.bowline", "guy", "yard", True),
    ("course.sheet", "sheet", "course", False),
    ("course.tack", "tack", "course", False),
)
# The driver's lines (Ext §17.2; Steel 1794 vol. I, THE DRIVER or SPANKER SAIL, OCR l.
# 24523-24545): one halyard for Steel's four or five pair; the tack "set tight with a
# luff-tackle" to the throat of the boom; one unsided sheet rove through the boom's end, which
# does the outhauler's work; the downhaul through a block at the middle of the driver yard.
DRIVER_LINES = (
    ("driver.halyard", "halyard", "driver", False),
    ("driver.tack", "tack", "driver", False),
    ("driver.sheet", "sheet", "driver", False),
    ("driver.downhaul", "downhaul", "driver", False),
)


def area_centroid(pts):
    """A polygon's area and the centroid of its corners, (x, z) (the generator's
    `_quad_area_centroid`, here so that nothing is imported from it)."""
    pts = list(pts)
    a = cx = cz = 0.0
    for (x1, z1), (x2, z2) in zip(pts, pts[1:] + pts[:1], strict=True):
        cross = x1 * z2 - x2 * z1
        a += cross
        cx += (x1 + x2) * cross
        cz += (z1 + z2) * cross
    a *= 0.5
    return abs(a), cx / (6.0 * a), cz / (6.0 * a)


def steel_area(head_cloths, foot_cloths, fore_leech_yd, after_leech_yd, cloth_m=CLOTH_M):
    """Steel's rule for the canvas in a driver, a boomsail or a mizen: the mean of the cloths at
    the head and the foot by the mean of the leeches (Steel 1794 vol. I, OCR l. 10891-10897),
    square metres."""
    cloths = 0.5 * (head_cloths + foot_cloths)
    depth = 0.5 * (fore_leech_yd + after_leech_yd) * YARD_M
    return cloths * cloth_m * depth


def mast_line(mast_x, rake_deg, frame_z):
    """The mast's raked line: x at a height above the water, from its x at the frame's height."""
    lean = math.tan(math.radians(rake_deg))

    def at(z):
        return mast_x - lean * (z - frame_z)

    return at


def _off_line(p, a, b):
    """The distance of the point `p` from the line through `a` and `b`."""
    (px, pz), (ax, az), (bx, bz) = p, a, b
    return abs((bx - ax) * (pz - az) - (bz - az) * (px - ax)) / math.hypot(bx - ax, bz - az)


def course(*, mast_x, rake_deg, frame_z, tack_z, steel, yard_length_m, cloth_m=CLOTH_M):
    """The mizen course cut at the mast (Ext §3.4) from Steel's table IV: `steel` the cloths at
    the head and the foot and the fore (mast) and after leeches in yards. Its tack on the mast's
    raked line at `tack_z` above her water, its throat a fore leech above it, its peak an after
    leech above the foot and its head's cloths aft of the throat, the foot level aft to the
    clew; the head runs straight, the yard's line (Ext §2). Returns the corners (x, z), the
    area, centre and Steel's area, and the yard: its truss (the throat) and its whole length,
    the part forward of the mast bare."""
    head_cl, foot_cl, fore_yd, after_yd = steel
    on_mast = mast_line(mast_x, rake_deg, frame_z)
    throat_z = tack_z + fore_yd * YARD_M
    peak_z = tack_z + after_yd * YARD_M
    run = head_cl * cloth_m
    foot = foot_cl * cloth_m
    tack = (on_mast(tack_z), tack_z)
    throat = (on_mast(throat_z), throat_z)
    peak = (throat[0] - run, peak_z)
    clew = (tack[0] - foot, tack_z)
    corners = [tack, throat, peak, clew]
    area, cx, cz = area_centroid(corners)
    head = math.hypot(run, peak_z - throat_z)
    if head >= yard_length_m:
        raise ValueError(
            f"the mizen course's head ({head:.2f} m) is not shorter than its yard "
            f"({yard_length_m:.2f} m): the yard is slung at its truss with its fore part bare."
        )
    for word, (x, z) in (("tack", tack), ("throat", throat)):
        if abs(x - on_mast(z)) > ON_THE_LINE_M:
            raise ValueError(f"the mizen course's {word} is off the mast's line at {z:.2f} m.")
    steel_m2 = steel_area(head_cl, foot_cl, fore_yd, after_yd, cloth_m)
    if abs(area / steel_m2 - 1.0) > AREA_BAND:
        raise ValueError(
            f"the mizen course cut at the mast is {area:.0f} m2 against Steel's {steel_m2:.0f} "
            "m2: outside a tenth (Ext §3.4)."
        )
    return {
        "corners": corners,
        "area": area,
        "x": cx,
        "centre": cz,
        "steel_area": steel_m2,
        "run": run,
        "rise": peak_z - throat_z,
        "head": head,
        "foot": foot,
        "yard": {"truss_z": throat_z, "length_m": yard_length_m, "fore_part": yard_length_m - head},
    }


def driver_corners(crs, *, mast_x, rake_deg, frame_z, jaws_z, steel, cloth_m=CLOTH_M):
    """The driver's four corners on the course `crs` (from `course`) with its boom's jaws at
    `jaws_z`: the throat the course's; the tack down the mast's raked line at the jaws; the
    head along the mizen yard's line from the throat, Steel's head cloths aft (Ext §17.2: the
    head runs straight along the yard and on along the driver yard, whose inner part lies along
    the yard's after end); the foot along the level boom, Steel's foot cloths aft."""
    head_cl, foot_cl, _fore_yd, _after_yd = steel
    on_mast = mast_line(mast_x, rake_deg, frame_z)
    tack_c, throat, peak_c, _clew_c = crs["corners"]
    slope = (peak_c[1] - throat[1]) / (throat[0] - peak_c[0])
    run = head_cl * cloth_m
    peak = (throat[0] - run, throat[1] + run * slope)
    tack = (on_mast(jaws_z), jaws_z)
    clew = (tack[0] - foot_cl * cloth_m, jaws_z)
    return [tack, throat, peak, clew]


def after_leech_band(course_steel):
    """Steel's band for a driver's after leech, metres: two to four yards deeper than the mizen
    course's (`course_steel`, its table row)."""
    after_yd = course_steel[3]
    lo, hi = AFTER_LEECH_DEEPER_YD
    return (after_yd + lo) * YARD_M, (after_yd + hi) * YARD_M


def least_jaws(crs, *, mast_x, rake_deg, frame_z, steel, course_steel, under, cloth_m=CLOTH_M):
    """The lowest jaws, metres above her water, at which a level boom clears every point of
    `under` ((x, z, room): a height it must stand above by `room` over the boom's run) and the
    driver cut on the course `crs` keeps its after leech within Steel's band (Ext §17.2): the
    higher of the two. Returns (jaws, which: "clearance" or "after leech")."""
    clear = max(z + room for _x, z, room in under)
    _lo, hi = after_leech_band(course_steel)

    def leech(j):
        _t, _th, peak, clew = driver_corners(
            crs,
            mast_x=mast_x,
            rake_deg=rake_deg,
            frame_z=frame_z,
            jaws_z=j,
            steel=steel,
            cloth_m=cloth_m,
        )
        return math.hypot(peak[0] - clew[0], peak[1] - clew[1])

    if leech(clear) <= hi:
        return clear, "clearance"
    lo_j, hi_j = clear, crs["yard"]["truss_z"]
    for _ in range(60):  # the after leech shortens as the jaws rise
        mid = 0.5 * (lo_j + hi_j)
        if leech(mid) > hi:
            lo_j = mid
        else:
            hi_j = mid
    return hi_j, "after leech"


def driver(
    crs,
    *,
    mast_x,
    rake_deg,
    frame_z,
    jaws_z,
    steel,
    course_steel,
    boom_length_m,
    driver_yard_m,
    under=(),
    over=(),
    cloth_m=CLOTH_M,
):
    """Steel's driver boomsail bent in the course's place (Ext §17.2), on the course `crs`, its
    boom's jaws at `jaws_z`: `steel` its table row (the cloths at the head and the foot, the
    fore and after leeches in yards) and `course_steel` the course's. The boom lies level from
    its jaws on the mast; it must stand above each of `under` ((x, z, room)) by its room, and
    pass above each of `over` ((x, z)), the taffrail, where its run reaches it. Raises
    `ValueError` with a sentence where §17.2's assertions fail: the throat at the course's and
    the tack on the mast's raked line at the jaws, within 0.1 m; the foot on the boom's line
    and the clew within the boom's length; the peak on the mizen yard's line within 0.1 m,
    abaft and above the yard's peak by no more than two-thirds of the driver yard; the four
    corners' area within a tenth of Steel's rule, and the after leech within Steel's band; the
    boom clear. Returns the corners, the area, centre and Steel's area, the leeches, the boom
    (jaws, length, end) and the driver yard's reach beyond the mizen yard's peak."""
    tack, throat, peak, clew = corners = driver_corners(
        crs,
        mast_x=mast_x,
        rake_deg=rake_deg,
        frame_z=frame_z,
        jaws_z=jaws_z,
        steel=steel,
        cloth_m=cloth_m,
    )
    on_mast = mast_line(mast_x, rake_deg, frame_z)
    c_tack, c_throat, c_peak, _c_clew = crs["corners"]
    if math.dist(throat, c_throat) > ON_THE_LINE_M:
        raise ValueError("the driver's throat is not the mizen course's.")
    if abs(tack[0] - on_mast(jaws_z)) > ON_THE_LINE_M:
        raise ValueError("the driver's tack is off the mast's line at the boom's jaws.")
    if abs(clew[1] - jaws_z) > ON_THE_LINE_M or tack[0] - clew[0] > boom_length_m:
        raise ValueError(
            f"the driver's foot ({tack[0] - clew[0]:.2f} m) is off its boom or longer than it "
            f"({boom_length_m:.2f} m)."
        )
    if _off_line(peak, c_throat, c_peak) > ON_THE_LINE_M:
        raise ValueError("the driver's peak is off the mizen yard's line.")
    beyond = math.dist(peak, c_peak)
    if not (peak[0] < c_peak[0] and peak[1] > c_peak[1]):
        raise ValueError("the driver's peak is not abaft and above the mizen yard's peak.")
    if beyond > DRIVER_YARD_REACH * driver_yard_m:
        raise ValueError(
            f"the driver's peak stands {beyond:.2f} m beyond the mizen yard's peak, more than "
            f"two-thirds of its driver yard ({driver_yard_m:.2f} m): Lever's outer halyards are "
            "bent a third from the driver yard's inner arm."
        )
    area, cx, cz = area_centroid(corners)
    steel_m2 = steel_area(*steel, cloth_m)
    if abs(area / steel_m2 - 1.0) > AREA_BAND:
        raise ValueError(
            f"the driver's four corners give {area:.0f} m2 against Steel's {steel_m2:.0f} m2: "
            "outside a tenth (Ext §17.2)."
        )
    after = math.dist(peak, clew)
    lo, hi = after_leech_band(course_steel)
    if not (lo - 0.01 <= after <= hi + 0.01):
        raise ValueError(
            f"the driver's after leech is {after:.2f} m, outside Steel's two to four yards deeper "
            f"than the mizen course's ({lo:.2f}-{hi:.2f} m)."
        )
    end_x = tack[0] - boom_length_m
    for x, z, room in under:
        if end_x <= x <= tack[0] and jaws_z < z + room - 0.005:
            raise ValueError(
                f"the driver's boom stands {jaws_z - z:.2f} m over what is under it at x {x:.2f} "
                f"m, less than its head room of {room:.2f} m."
            )
    for x, z in over:
        if end_x <= x <= tack[0] and jaws_z <= z:
            raise ValueError(
                f"the driver's boom runs {z - jaws_z:.2f} m under the taffrail at x {x:.2f} m."
            )
    return {
        "corners": corners,
        "area": area,
        "x": cx,
        "centre": cz,
        "steel_area": steel_m2,
        "fore_leech": throat[1] - tack[1],
        "after_leech": after,
        "after_band": (lo, hi),
        "foot": tack[0] - clew[0],
        "head": math.dist(throat, peak),
        "beyond_yard": beyond,
        "boom": {"jaws_z": jaws_z, "length_m": boom_length_m, "end_x": end_x},
    }
