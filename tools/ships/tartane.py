"""The tartane, a Provençal coaster under a great lateen and a square topsail, and the coastguard
tartane of the same hull (package 90, the first hull; her builder).

Her design is docs/design/Design-Ship-Tartane.md (cited here as Tar-D), from her research note,
docs/design/Research-Tartane-2026-11.md (Tar), her measuring note,
docs/design/ships-design/pages-tartane.md (Pages), and the engine's note for her lateens,
docs/design/Design-Package90-Engine.md (Eng). One module writes two files, one class in two roles
(Tar-D decision 1; Build-Ships.md §5.0 principle 10; the plan's §4 row 12): `tartane.yaml`, the
trader of ten, and `coastguard-tartane.yaml`, the guarda-costa of thirty-four with Chapman's eight
4-pounders. `particulars()` gives her hull in the file's frame and raises in words where a check
of Tar-D §1 fails; `write(out_dir, p, role)` builds and dumps one file; `build(out_dir)` is the
generator's hook (`tools/gen_ships.py`, `SHIP_MODULES`). Her two lateens are cut by
`tools/ships/lateen.py`, pure.

**Her sources, each converted once.**
- Forfait 1788, Table II, the *Humble* of 100 tonneaux with topsail and mizen (column 2; read on
  the page image, IA leaf n179: Tar §2.1), in pieds, pouces and lignes, the pied du roi 0.3248 m
  (`period.PIED_DU_ROI_M`): her length and breadth, her masts, yards and their places, the
  éperon (ruled 10½ pieds, the lead's ruling 3 of 2026-11-20), her sail and its centre (the
  checks).
- Chapman 1768, Pl. LVII No. 16, the French tartane, measured at her scale (Pages §6, rung S†,
  `stand-in`): every line of her profile in metres in the file's frame, built on H, the line the
  sheet marks (the lead's ruling 1), lengths by 1.100 and sections by 1.268 (Pages §3.4). The
  plate's half-breadths are moulded (Pages §9); her file's are outside the plank, by
  `PLANK_POUCES` (JUDGEMENT), as the house's are (the cutter's, the bilander's).
- Chapman 1768, Pl. LXII No. 16 (Pages §7), another rig of the type: the checks on her main's
  rake and her yard.

**The frame (Pages, "Units and datums").** x in metres forward of the middle of her load
waterline on H, z in metres above H; her post and her stem at the water at x -9.23 and +9.25.
Her datum, `deck_height_m`, is the deck at side at the midship station, 0.54 m (the lead's
ruling 2). A spar's `height_m` is its head (a yard's, its sling) above the datum, a bowsprit's its
outer end's; a sail's `corners_m` are above the datum, its `centre_height_m` above the water.

**Her notes (the lead's notes of 2026-10-29, item 2).** The file's notes carry sources,
departures and judgements. A figure a rule computes from the file's own keys (an area from a cut,
a rating, the drawn displacement, a port's gap) is printed by `her_report()` and held by her
tests, where it cannot go stale.

**Keys her file does not carry yet** (each a guard of `tests/test_probes_90.py` until its step
is merged): `dipping` on her two whole lateens (A1a), the hull's `helm: tiller` (A3), her boat
`towed` (A4). Her topsail on a pole main is a course to the engine until A5 and A6. They are
added when those steps are merged into the package's branch.

The module is imported only by the generator's entry block, after `gen_ships` is made the running
script, and takes every helper as `g.<name>`. No function or table of the generator is changed;
every other file stays byte for byte as it is.

Marks as Tar-D's: read, measured, computed, JUDGEMENT. The images are not in the repository.
"""

from __future__ import annotations

import math
import os
import re
import sys
from dataclasses import dataclass

import gen_ships as g

from ships import lateen, period

FT = g.FT
PIED = period.PIED_DU_ROI_M


def pieds(p: float, po: float = 0.0, li: float = 0.0) -> float:
    """Pieds, pouces and lignes du roi to metres (12 pouces to the pied, 12 lignes to the
    pouce), unrounded."""
    return (p + po / 12.0 + li / 144.0) * PIED


def cm(v: float) -> float:
    """A figure to the centimetre (never a "-0.0")."""
    return round(v, 2) + 0.0


# ---------------------------------------------------------------------------
# Forfait 1788, Table II, column 2: "L'Humble id. de 100 tonneaux, avec hunier & tapecul" (read,
# page image, IA leaf n179, p. 134; Tar §2.1). Each figure as the table prints it, (pieds,
# pouces, lignes); the ratios beside them are the table's and not used.
# ---------------------------------------------------------------------------

HUMBLE = {
    "length": (62.75, 0, 0),  # 62¾ pieds; which length (on deck or stem to post) unstated
    "breadth": (20 + 1 / 3, 0, 0),  # 20⅓
    "main": (59, 0, 0),  # heel to head
    "main_diameter": (0, 22, 0),
    "main_head": (26, 0, 0),  # the ton, its head above the hounds
    "main_place": (10, 5, 0),  # before the middle
    "mizen": (30, 0, 0),
    "mizen_diameter": (0, 10, 0),
    "mizen_head": (6, 0, 0),
    "mizen_place": (15, 2, 0),  # abaft the middle
    "eperon": (10.5, 0, 0),  # 10½: the lead's ruling 3 (the printed ratio, 0.151, the misprint)
    "lateen_yard": (75, 0, 0),
    "lateen_yard_diameter": (0, 9.25, 0),
    "lateen_yard_ends": ((1.5, 0, 0), (0.75, 0, 0)),  # at the penne, at the car
    "topsail_yard": (32, 0, 0),
    "topsail_yard_diameter": (0, 6.25, 0),
    "mizen_yard": (47, 0, 0),
    "mizen_yard_diameter": (0, 6, 0),
    "mizen_yard_ends": ((1, 0, 0), (1, 0, 0)),  # one figure printed, taken for each end
    "sail_sq_pieds": 2237.5,  # with the topgallant
    "centre_before_middle": (3, 4, 11),  # the centre of effort, before the middle
    "centre_height": (25, 2, 9),  # its height, above the load water line (JUDGEMENT on the datum)
    "tonneaux": 100,
}
# The *Espiègle*'s and the square-sail column's yard of 41 pieds, 8½ pouces, the tréou's (Tar §2.1;
# Tar-D decision 9).
TREOU_YARD = (41, 0, 0)


def humble(key: str) -> float:
    """A figure of the *Humble*'s column in metres."""
    return pieds(*HUMBLE[key])


LENGTH = humble("length")  # 20.38 m
BREADTH = humble("breadth")  # 6.61 m
# The topgallant the *Humble* carries and her file does not (Tar-D §4.1): its share of Forfait's
# sail, about 20 m² (JUDGEMENT, Tar-D §4.5), taken off before her sail is checked against his.
TOPGALLANT_SHARE_M2 = 20.0
SAIL_BAND = 0.15  # Tar-D §4.5: within ±15% of Forfait's
FORFAIT_SAIL_M2 = HUMBLE["sail_sq_pieds"] * PIED * PIED


# ---------------------------------------------------------------------------
# Chapman 1768, Pl. LVII No. 16 at her scale (Pages §6.2, §6.3, §6.4; measured, S†): every point
# in the file's frame, built on H, metres; half-breadths moulded, as the plate draws them.
# ---------------------------------------------------------------------------

# The top of the side, taffrail to stem head; the waist bulwark's upright after end at x -7.06
# given as two points a centimetre apart (Pages §5.2, §6.2).
RAIL_M = [
    [-9.72, 3.30], [-9.15, 3.04], [-8.49, 2.76], [-7.84, 2.51], [-7.19, 2.28], [-7.07, 2.24],
    [-7.06, 2.61], [-6.53, 2.46], [-5.88, 2.32], [-5.23, 2.18], [-4.57, 2.06], [-3.92, 1.96],
    [-3.27, 1.88], [-2.61, 1.82], [-1.96, 1.78], [-1.31, 1.75], [-0.65, 1.73], [0.00, 1.71],
    [0.65, 1.74], [1.31, 1.78], [1.96, 1.83], [2.61, 1.90], [3.27, 1.98], [3.92, 2.07],
    [4.57, 2.18], [5.23, 2.30], [5.88, 2.43], [6.53, 2.58], [7.19, 2.49], [7.84, 2.54],
    [8.49, 2.72], [9.15, 2.98], [9.80, 3.33], [10.13, 3.53], [10.38, 3.67],
]  # fmt: skip
# By station: x, the half-breadth at the water on H (carried down from the plan's load waterline
# on H' by the sections' flare: Pages §4.3) and at the rail; the rail's at aft 2, aft 1, fore 7 and
# fore 8 interpolated between traced frames (Pages §5.1, JUDGEMENT there). Moulded.
BREADTH_MOULDED = [
    [-8.02, 0.86, 1.62], [-7.04, 1.57, 2.26], [-6.06, 2.16, 2.62], [-5.10, 2.58, 2.81],
    [-4.13, 2.88, 2.92], [-3.16, 3.08, 2.97], [-2.19, 3.20, 3.00], [-1.21, 3.26, 3.02],
    [-0.23, 3.27, 3.04], [0.73, 3.26, 3.02], [1.70, 3.21, 2.99], [2.67, 3.10, 2.94],
    [3.64, 2.90, 2.88], [4.62, 2.57, 2.77], [5.59, 2.14, 2.63], [6.56, 1.56, 2.30],
    [7.53, 0.94, 1.85], [8.50, 0.40, 1.29],
]  # fmt: skip
# The deck at side, the plate's dashed line, to where it ends at x 7.19 (Pages §5.2).
DECK_M = [
    [-9.15, 1.77], [-8.49, 1.62], [-7.84, 1.49], [-7.19, 1.37], [-6.53, 1.25], [-5.88, 1.14],
    [-5.23, 1.03], [-4.57, 0.95], [-3.92, 0.86], [-3.27, 0.79], [-2.61, 0.73], [-1.96, 0.66],
    [-1.31, 0.60], [-0.65, 0.55], [0.00, 0.53], [0.65, 0.54], [1.31, 0.59], [1.96, 0.66],
    [2.61, 0.71], [3.27, 0.78], [3.92, 0.85], [4.57, 0.95], [5.23, 1.05], [5.88, 1.17],
    [6.53, 1.30], [7.19, 1.45],
]  # fmt: skip
# The war tartane's four ports a side: x, sill, half-breadth at the sill, moulded (Pages §5.7).
PORTS_MOULDED = [[-4.66, 1.37, 2.89], [-1.94, 1.11, 3.14], [3.21, 1.18, 3.02], [5.93, 1.57, 2.39]]
# Chapman's 1.61 by 1.45 ft: the width by the lengths' factor, the depth by the sections' (Pages
# §5.7; the builder's choice of the two it offers, JUDGEMENT).
PORT_SIZE = [0.52, 0.54]
# The keel's lower edge (Pages §6.2).
KEEL_M = [[-8.91, -2.43], [0.00, -2.38], [6.71, -2.32]]
# The base line, the keel's upper edge (Pages §6.2); its half-siding not measured: the house's
# keel siding of the moulded breadth (`g.KEEL_SIDING_OF_BREADTH`, JUDGEMENT).
RABBET_Z = [[-8.80, -2.20], [0.00, -2.14], [6.50, -2.08]]
# The forefoot, the stem's fore face and the stem head (Pages §5.4, §6.2).
STEM_M = [
    [6.71, -2.32], [6.82, -2.26], [7.43, -1.88], [7.91, -1.51], [8.32, -1.13], [8.66, -0.75],
    [8.97, -0.38], [9.25, 0.00], [9.47, 0.34], [9.72, 0.69], [9.95, 1.03], [10.19, 1.37],
    [10.45, 1.71], [10.57, 3.03], [10.58, 4.74],
]  # fmt: skip
# The knee's and the beak's lower edge, from where it leaves the stem to the eye (Pages §6.2).
HEAD_M = [
    [10.77, 2.06], [11.34, 2.40], [11.82, 2.54], [12.28, 2.63], [12.75, 2.68], [13.22, 2.72],
    [13.68, 2.75], [14.15, 2.79], [14.36, 2.85],
]  # fmt: skip
# The post's after face, the heel to the taffrail (Pages §5.5, §6.2).
STERN_M = [
    [-8.91, -2.43], [-9.06, -1.33], [-9.21, -0.21], [-9.23, 0.00], [-9.36, 0.82], [-9.51, 1.84],
    [-9.65, 2.85], [-9.72, 3.30],
]  # fmt: skip
# The wale: x, its lower edge, its upper edge (Pages §5.3, §6.2).
WALES_M = [
    [-8.49, 1.70, 1.86], [-7.84, 1.44, 1.60], [-7.19, 1.20, 1.36], [-6.53, 0.97, 1.14],
    [-5.88, 0.76, 0.93], [-5.23, 0.58, 0.74], [-4.57, 0.41, 0.57], [-3.92, 0.26, 0.42],
    [-3.27, 0.13, 0.30], [-2.61, 0.04, 0.21], [-1.96, -0.05, 0.13], [-1.31, -0.11, 0.11],
    [-0.65, -0.17, 0.09], [0.00, -0.20, 0.06], [0.65, -0.18, 0.04], [1.31, -0.14, 0.03],
    [1.96, -0.05, 0.11], [2.61, 0.04, 0.20], [3.27, 0.13, 0.29], [3.92, 0.25, 0.42],
    [4.57, 0.40, 0.56], [5.23, 0.56, 0.72], [5.88, 0.76, 0.92], [6.53, 0.97, 1.14],
    [7.19, 1.20, 1.37], [7.84, 1.47, 1.63], [8.49, 1.75, 1.91],
]  # fmt: skip
# The midship frame, at x -0.23: z, half-breadth, moulded (Pages §6.2).
SECTION_MOULDED = [
    [-2.07, 1.09], [-1.88, 2.05], [-1.69, 2.42], [-1.51, 2.64], [-1.32, 2.81], [-1.13, 2.93],
    [-0.94, 3.02], [-0.75, 3.09], [-0.56, 3.15], [-0.38, 3.19], [-0.19, 3.23], [0.00, 3.26],
    [0.19, 3.27], [0.38, 3.29], [0.56, 3.30], [0.75, 3.30], [0.94, 3.25], [1.13, 3.19],
    [1.31, 3.12], [1.50, 3.06], [1.69, 3.03], [1.71, 3.04],
]  # fmt: skip
# The traced frames: x, then (z, half-breadth) from the base line (or where traced) to the rail,
# moulded (Pages §6.3). Not traced, and so not given: aft 1 and 2, fore 7, 8 and 10.
SECTIONS_MOULDED = {
    -8.02: [[-0.19, 0.93], [0.17, 0.97], [0.51, 1.10], [0.86, 1.25], [1.20, 1.36], [1.54, 1.45],
            [1.88, 1.52], [2.22, 1.58], [2.58, 1.62]],
    -7.04: [[0.17, 1.66], [0.52, 1.81], [0.86, 1.94], [1.21, 2.05], [1.55, 2.13], [1.89, 2.20],
            [2.24, 2.24], [2.38, 2.26]],
    -6.06: [[-2.07, 0.25], [-1.69, 0.69], [-1.32, 1.11], [-0.94, 1.48], [-0.56, 1.79],
            [-0.19, 2.03], [0.17, 2.21], [0.52, 2.34], [0.87, 2.44], [1.22, 2.50], [1.56, 2.56],
            [1.91, 2.59], [2.26, 2.62], [2.37, 2.62]],
    -5.10: [[-2.07, 0.38], [-1.69, 1.05], [-1.32, 1.57], [-0.94, 1.97], [-0.56, 2.26],
            [-0.19, 2.46], [0.18, 2.61], [0.53, 2.71], [0.88, 2.78], [1.23, 2.82], [1.58, 2.82],
            [1.93, 2.82], [2.16, 2.81]],
    -4.13: [[-2.07, 0.51], [-1.69, 1.47], [-1.32, 2.06], [-0.94, 2.40], [-0.56, 2.64],
            [-0.19, 2.82], [0.18, 2.92], [0.53, 2.98], [0.89, 3.01], [1.24, 2.99], [1.59, 2.95],
            [1.95, 2.91], [1.99, 2.91]],
    -3.16: [[-2.07, 0.71], [-1.69, 1.86], [-1.32, 2.38], [-0.94, 2.68], [-0.56, 2.87],
            [-0.19, 3.00], [0.18, 3.08], [0.54, 3.13], [0.90, 3.15], [1.25, 3.07], [1.61, 2.99],
            [1.88, 2.97]],
    0.73: [[-2.07, 1.31], [-1.69, 2.33], [-1.32, 2.73], [-0.94, 2.95], [-0.56, 3.09],
           [-0.19, 3.18], [0.19, 3.24], [0.56, 3.27], [0.94, 3.24], [1.31, 3.10], [1.68, 3.02],
           [1.75, 3.02]],
    1.70: [[-2.07, 1.02], [-1.69, 2.20], [-1.32, 2.62], [-0.94, 2.87], [-0.56, 3.02],
           [-0.19, 3.12], [0.18, 3.19], [0.55, 3.22], [0.92, 3.19], [1.28, 3.06], [1.65, 2.99],
           [1.83, 2.99]],
    2.67: [[-2.07, 0.73], [-1.69, 1.93], [-1.32, 2.41], [-0.94, 2.68], [-0.56, 2.87],
           [-0.19, 3.00], [0.18, 3.09], [0.54, 3.14], [0.90, 3.12], [1.26, 3.03], [1.63, 2.96],
           [1.90, 2.94]],
    3.64: [[-2.07, 0.53], [-1.69, 1.57], [-1.32, 2.09], [-0.94, 2.41], [-0.56, 2.64],
           [-0.19, 2.80], [0.18, 2.92], [0.54, 3.00], [0.89, 3.02], [1.25, 2.97], [1.61, 2.90],
           [1.96, 2.88], [2.05, 2.88]],
    4.62: [[-2.07, 0.34], [-1.69, 1.14], [-1.32, 1.66], [-0.94, 2.03], [-0.56, 2.29],
           [-0.19, 2.48], [0.18, 2.63], [0.53, 2.74], [0.88, 2.81], [1.23, 2.81], [1.58, 2.77],
           [1.94, 2.76], [2.19, 2.77]],
    5.59: [[0.52, 2.37], [0.87, 2.49], [1.22, 2.56], [1.57, 2.58], [1.92, 2.59], [2.26, 2.62],
           [2.37, 2.63]],
    8.50: [[0.51, 0.53], [0.86, 0.69], [1.20, 0.84], [1.54, 0.96], [1.89, 1.08], [2.23, 1.19],
           [2.57, 1.27], [2.71, 1.29]],
}  # fmt: skip

# Her drawn body (Pages §4.3, measured, ±6%): moulded to H, 134.6 t; with the keel below the base
# line, 135.2 t; KB 1.48 m, BM 1.66 m, KM 3.15 m on H. The plate draws no plank (Pages §9).
DRAWN_MOULDED_WITH_KEEL_T = 135.2
DRAWN_BAND = 0.06
KM_M = 3.15
SEA_T_PER_M3 = 1.026  # Pages §4.3's sea water
# Her plank, 2½ pouces (JUDGEMENT): no plank is drawn or stated for a trading tartane; Forfait's
# tartanes are a navy constructor's, and the house's small hulls carry 2½ in (the cutter's,
# ZAZ6381's extreme less its moulded breadth; Steel 1805's collier's, the bilander's). The range
# 2 to 3 pouces, recorded with the displacement it gives (the lead's ruling of 2026-11-20, nudge
# 30: the body as drawn, outside the plank, at the line her draught is given on, H).
PLANK_POUCES = 2.5
PLANK_RANGE_POUCES = (2.0, 3.0)
PLANK_M = pieds(0, PLANK_POUCES)

# Forfait's places are taken from the middle of her perpendiculars (Table II), which stands at x
# +0.49 in her frame (Pages §6.4, computed).
MIDDLE_X = 0.49
# Her post and stem at the water, and the taffrail (Pages §5.4, §5.5).
POST_X = -9.23
STEM_X = 9.25
TAFFRAIL_X = -9.72
STEM_HEAD = (10.58, 4.74)
# Her deck at side at the masts' places, and the keel's upper edge there (Pages §6.4, measured).
MAST_DECK = {"main": (0.85, -2.12), "mizzen": (0.93, -2.17)}
# A keelson of 0.25 m under each heel (JUDGEMENT; none is drawn: Pages §6.4).
KEELSON_M = 0.25
DATUM = 0.54  # `deck_height_m`: the deck at side at the midship station (the lead's ruling 2)
# The beak's middle line, level at 2.85 m above the water to the eye (Pages §5.4): the berthelot
# lies on it.
BEAK_Z = 2.85

# Her hull block (Tar-D §2; the lead's rulings 1, 2 and 4 of 2026-11-20): every figure on H.
LWL = 18.47
DRAUGHT = 2.38
LATERAL_AREA = 40.9
HULL_SPEED_KN = 10.4
GM = 0.8
# Her helm (Tar-D §2; the house's way, as the cutter's and the bilander's): clr_x_m set for a
# little weather helm close-hauled and abeam under plain sail in 15 kn (seed 7, the known truths'
# settle), by quarter metres (docs/dev/TuningNotes.md, the tartane's section): at 0.0, 9.7 degrees
# of lee helm close-hauled and 5.1 abeam; at +1.5, 1.9 and 0.5 of lee helm; at +2.0, 0.25 and 0.8
# of weather helm; at +2.25, 1.25 and 1.4; at +2.5 she luffed head to wind close-hauled in the
# settle. +2.0 taken, a quarter metre short of the most.
CLR_X_M = 2.0
RUDDER = {"area_m2": 1.3, "max_angle_deg": 35, "rate_deg_s": 5.0, "span_m": 2.3}


def interp(pts, x):
    """A line's height at x, straight between its points and held at its ends."""
    if x <= pts[0][0]:
        return pts[0][1]
    if x >= pts[-1][0]:
        return pts[-1][1]
    for (x0, z0), (x1, z1) in zip(pts, pts[1:], strict=False):
        if x0 <= x <= x1:
            return z0 + (z1 - z0) * (x - x0) / (x1 - x0) if x1 != x0 else z1
    return pts[-1][1]


def deck_at(x: float) -> float:
    """Her deck at side above the water at x: the dashed line, held at its ends (Pages §5.2)."""
    return interp(DECK_M, x)


def stem_x_at(z: float) -> float:
    """The stem's fore face's x at a height above the water (Pages §5.4)."""
    pts = [[zz, xx] for xx, zz in STEM_M]
    return interp(pts, z)


def outside(hb: float) -> float:
    """A moulded half-breadth outside the plank."""
    return hb + PLANK_M


# ---------------------------------------------------------------------------
# Her hull: the block, the profile, the drawn displacement outside the plank
# ---------------------------------------------------------------------------


def girth(points) -> float:
    """A section's girth along its points (z, half-breadth), the water at z 0 the top: one side,
    from its lowest point up to the water, metres."""
    pts = sorted(points)
    below = [p for p in pts if p[0] <= 0.0]
    above = [p for p in pts if p[0] > 0.0]
    if above and below:
        (z0, h0), (z1, h1) = below[-1], above[0]
        below.append((0.0, h0 + (h1 - h0) * (0.0 - z0) / (z1 - z0)))
    return sum(math.dist(a, b) for a, b in zip(below, below[1:], strict=False))


def plank_volume(plank_m: float) -> tuple[float, float]:
    """The plank's volume under H, both sides, and her wetted girth's integral, m² (JUDGEMENT on
    the method): each fully traced frame's girth from the rabbet to the water (Pages §6.3, the
    midship frame §6.2), with the keel's half-siding's step, its own; at the stations not traced
    to the rabbet, the traced frames' girth as a share of their depth and half-breadth at the water
    (the mean share) on the station's own; nothing at the post's and the stem's faces; trapezoids
    between. The plank's volume is the girth's integral times the plank, a side each."""
    rabbet = interp(RABBET_Z, 0.0)
    keel = interp(KEEL_M, 0.0)
    traced = {x: pts for x, pts in SECTIONS_MOULDED.items() if pts[0][0] <= -2.0}
    traced[-0.23] = SECTION_MOULDED
    shares = []
    girths = {}
    for x, pts in traced.items():
        gth = girth(pts)
        hb = interp([[s[0], s[2]] for s in BREADTH_MOULDED], x)
        depth = -interp(RABBET_Z, x)
        girths[x] = gth
        shares.append(gth / (depth + hb))
    share = sum(shares) / len(shares)
    for x, hb, _rail in BREADTH_MOULDED:
        if not any(abs(x - t) < 0.01 for t in girths):
            girths[x] = share * (-interp(RABBET_Z, x) + hb)
    xs = [POST_X, *sorted(girths), STEM_X]
    gs = [0.0, *(girths[x] for x in sorted(girths)), 0.0]
    area = sum((xs[i + 1] - xs[i]) * (gs[i] + gs[i + 1]) / 2.0 for i in range(len(xs) - 1))
    del rabbet, keel
    return 2.0 * area * plank_m, area


def displacement_t(plank_pouces: float) -> float:
    """Her drawn displacement outside a plank of so many pouces, tonnes: Pages §4.3's body with
    its keel, and the plank's volume in sea water."""
    vol, _ = plank_volume(pieds(0, plank_pouces))
    return DRAWN_MOULDED_WITH_KEEL_T + vol * SEA_T_PER_M3


HULL_NOTES = {
    "length_waterline_m": "18.47 m: Chapman's waterline on H, the post's after face to the stem's "
    "fore face, 56.55 Swedish ft (16.79 m), over his 62.39 ft between the perpendiculars, laid on "
    "Forfait's 62¾ pieds (20.38 m: Table II, the Humble); measured (Pages §4.1), accepted by the "
    "lead (ruling 4 of 2026-11-20). The design's 19.0 m was his length between the perpendiculars "
    "taken for his waterline.",
    "beam_m": "20⅓ pieds, Forfait 1788 Table II (the Humble, read on the page image), 6.604 m at "
    "the tree's pied du roi of 0.3248 m (her design's 6.61 at 0.32484). Taken as her "
    "moulded breadth, as Chapman's 17 7/12 ft is (the sections' factor, 1.268, makes his drawn "
    "breadth hers: Pages §3.4); outside the plank she is broader by the plank a side (her report).",
    "draught_m": "The mean to the keel's lower edge at the middle of her waterline on H, the line "
    "the sheet marks (the lead's rulings 1 and 4 of 2026-11-20): 2.43 m at the post, 2.32 m at the "
    "stem, a drag of 0.11 m (Pages §4.2, measured). Chapman's stated 6⅔ ft is his after draught on "
    "H', the steeper line (2.40 m mean there); the design's 2.50 m was it taken as level.",
    "displacement_kg": "Her body as drawn, outside the plank, at H, the line her draught is given "
    "on (the lead's ruling of 2026-11-20, nudge 30): Chapman's body measured to H with its keel, "
    "135.2 t (±6%: Pages §4.3), and a plank of 2½ pouces, JUDGEMENT (2 to 3 pouces give the "
    "range in her report). Every other figure of the hull is reckoned to H likewise.",
    "gm_m": "JUDGEMENT (Tar-D §2): a broad, shallow hull (Forfait p. 125, 'their relative breadth "
    "always very great') under a high centre of effort (p. 123). Her KM on H is 3.15 m, measured "
    "(Pages §4.3: KB 1.48, BM 1.66), so the figure puts her centre of gravity 2.35 m above the "
    "keel's lower edge, about at her water.",
    "clr_x_m": "Set for her helm as the house sets it (the cutter's, the bilander's), by quarter "
    "metres: a little weather helm close-hauled and abeam under plain sail in 15 kn, 0.25 and 0.8 "
    "degrees measured (at 0.0, 9.7 and 5.1 of lee helm; at +2.5 she luffed head to wind "
    "close-hauled): docs/dev/TuningNotes.md, the tartane's section. Her drawn lateral plane's "
    "centroid is in her report; the figure is the engine's balance, not a drawn point.",
    "lateral_area_m2": "The profile under H (the post's after face, the keel's lower edge and the "
    "stem's fore face, no rudder drawn): 40.9 m², measured (Pages §5.6), accepted by the lead "
    "(ruling 4). It fills 0.93 of her waterline times her draught, as the other drawn hulls do; "
    "the generator's 0.85 rule would give 37.4.",
    "hull_speed_kn": "The files' rule, 1.34 x the root of her waterline in feet, 60.6 ft "
    "(computed; accepted, the lead's ruling 4).",
    "deck_height_m": "The deck at side at the midship station, the plate's dashed line, 0.54 m "
    "(Pages §5.2; the lead's ruling 2 of 2026-11-20): her readers, the wind on the deck and the "
    "hull and the lookout's eye, hold none a flooding edge or a freeboard. Her deck rises to 1.77 "
    "m aft and 1.45 m where the line ends forward; her waist bulwark's top stands 1.72 m above "
    "the water amidships, by the plate (no key).",
    "rudder": "No rudder is drawn on Pl. LVII No. 16 (Pages §5.5, §9): the cutter's blade by her "
    "length and draught, 1.3 m², its span her after draught less the heel (JUDGEMENT); 35 degrees "
    "the period's stop, a tiller's rate, the cutter's (JUDGEMENT).",
}

PROFILE_NOTES = {
    "profile": "Her lines (Build-Ships.md §5.0-§5.3; Tar-D §3): Chapman 1768, Pl. LVII No. 16, the "
    "French tartane, measured on the Sjöhistoriska museet's photograph (Pages; never copied) and "
    "scaled to her, lengths by 1.100 and sections by 1.268, heights above the water by principle "
    "7's split (Pages §3.4): rung S†, the type's only lines. Her load line is H, the line the "
    "sheet marks (the lead's ruling 1); every point is in its frame. The half-breadths are the "
    "plate's moulded ones and the plank, 2½ pouces a side (JUDGEMENT).",
    "profile.rail_m": "The top of the side, taffrail to stem head: aft, the rail from the "
    "taffrail; the waist bulwark from its upright after end at x -7.06 (two points a centimetre "
    "apart), its top 1.72 m above the water amidships, to the bow rail by the stem head (Pages "
    "§5.2). A war tartane's bulwark, kept for the trader (JUDGEMENT: the plate is her lines). A "
    "point at each traced frame's station at the line's own height to the centimetre, each frame's "
    "head cut there (Pages §5.1).",
    "profile.breadth_m": "By the plate's stations: the half-breadth at the water on H (the plan's "
    "load waterline carried down from H' by the sections' flare, Pages §4.3) and at the rail (the "
    "body plan's frames cut at the profile's rail; aft 2, aft 1, fore 7 and fore 8 interpolated "
    "between traced frames, JUDGEMENT), each with the plank.",
    "profile.keel_m": "The keel's lower edge, the post's heel to the forefoot (Pages §6.2).",
    "profile.stem_m": "The forefoot, the stem's fore face raking forward through the water at x "
    "9.25, and the tall stem head, its top 4.74 m above the water (Pages §5.4).",
    "profile.stern_m": "The post's after face, raked 8.4 degrees from the square of the keel, "
    "straight to the taffrail: a sharp stern, the planking closing on the post (Pages §5.5).",
    "profile.wales_m": "The wale, a band 0.16 m deep straddling the load line amidships (Pages "
    "§5.3).",
    "profile.section_m": "The midship frame at x -0.23 (Pages §6.2), with the plank: the greatest "
    "breadth 0.56 to 0.75 m above the water, 0.26 m of tumblehome to the rail.",
    "profile.decks_m": "Her one deck at side, the plate's dashed line, low amidships under the "
    "waist bulwark; it ends at x 7.19, forward of which the plate draws no deck (Pages §5.2). No "
    "raised after deck is drawn (the lead's ruling 7).",
    "profile.ports_m": "The war tartane's four ports a side, two pairs with the waist clear "
    "between them (Pages §5.7, measured; the lead's ruling 7): x, the sill, and the half-breadth "
    "at the sill from the traced frames, with the plank.",
    "profile.port_size_m": "Chapman's 1.61 by 1.45 ft: the width by the lengths' factor, the depth "
    "by the sections' (Pages §5.7; JUDGEMENT on the choice).",
    "profile.head_m": "The knee and the beak, from where it leaves the stem to the eye, level "
    "beyond the stem (Pages §5.4); the berthelot laid on it to its point, 10½ pieds beyond the "
    "stem head by the lead's ruling 3.",
    "profile.sections_m": "The body plan's traced frames, aft 8 to aft 3, fore 1 to fore 6 and "
    "fore 9, at whole feet of Chapman's height, with the plank (Pages §6.3); aft 1 and 2, fore 7, "
    "8 and 10 not traced.",
    "profile.rabbet_m": "The base line, the keel's upper edge (Pages §6.2); its half-siding the "
    "house's share of the moulded breadth (JUDGEMENT: not measured). Kept, not drawn.",
    "profile.form": "Her form (Build-Ships.md §5.1): no fullness beyond the default, her sections "
    "drawing the ends.",
    "profile.form.stern": "Round, closed on the post with no transom (Pages §5.5; JUDGEMENT on the "
    "schema's word).",
    "profile.form.head": "A plain knee and beak to an eye, no carving drawn (Pages §5.4); Falconer "
    "1780's CAGOUILLE, the scroll at a tartane's prow, in words only (principle 9).",
    "profile.marks": "Each line's rung (Build-Ships.md §5.0 principles 3 and 4): stand-in, S†, "
    "Chapman's plate of her type at her scale; judged, a judgement at its weakest point.",
}

MARKS = {
    "rail_m": "stand-in",
    "breadth_m": "stand-in",
    "keel_m": "stand-in",
    "stem_m": "stand-in",
    "stern_m": "stand-in",
    "wales_m": "stand-in",
    "section_m": "stand-in",
    "decks_m": "stand-in",
    "ports_m": "stand-in",
    "port_size_m": "judged",
    "head_m": "stand-in",
    "sections_m": "stand-in",
    "rabbet_m": "judged",
    "form.fullness": "judged",
    "form.stern": "stand-in",
    "form.head": "stand-in",
}


@dataclass
class Particulars:
    """Her figures in the file's frame: the hull block and its notes, the profile's lines, and
    the drawn displacement outside the plank with its range."""

    hull: dict
    hull_notes: dict
    lines: dict
    drawn_t: float
    drawn_range_t: tuple[float, float]


MIDSHIP_X = -0.23  # the midship frame's station (Pages §6.2)
# The frames' heads within this of the profile's rail are the rail (Pages §5.1: the body plan's
# frames cut at the profile's rail; the two traced apart, their heights to the plate's rounding).
ON_THE_RAIL_M = 0.03


def rail_at_stations() -> list[list[float]]:
    """The profile's rail with a point at each traced frame's station and the midship frame's, at
    the rail's own height there to the centimetre, so that each frame's head stands on it: the rail
    line itself moved by no more than its rounding."""
    stations = [*SECTIONS_MOULDED, MIDSHIP_X]
    added = [[x, cm(interp(RAIL_M, x))] for x in stations if not any(p[0] == x for p in RAIL_M)]
    return sorted([list(p) for p in RAIL_M] + added, key=lambda p: (p[0], p[1]))


def headed_at_the_rail(x: float, points) -> list[list[float]]:
    """A traced frame's points (z, half-breadth) with its head on the profile's rail at its
    station: a head within `ON_THE_RAIL_M` of it is the rail; one under it by more is carried
    straight up to it. Aft 7 (x -7.04) is that one: it stands 0.05 ft forward of the waist
    bulwark's upright after end (Pages §5.2), and its frame is cut at the lower rail, 2.38 m, where
    the side's top there is the bulwark's, 2.60 m (JUDGEMENT: the bulwark's end on the frame's
    head, its half-breadth the frame's)."""
    rail = cm(interp(RAIL_M, x))
    pts = [list(p) for p in points]
    z, hb = pts[-1]
    if abs(z - rail) <= ON_THE_RAIL_M:
        pts[-1] = [rail, hb]
    elif z < rail:
        pts.append([rail, hb])
    else:
        raise ValueError(
            f"the frame at x {x:g} stands {z - rail:.2f} m above her rail there; a frame's head "
            "is cut at the profile's rail (Pages §5.1)."
        )
    return pts


def hull_lines(armed: bool) -> dict:
    """The profile's lines as `g.hull_profile` takes them, every half-breadth with the plank, each
    frame's head on the rail; the ports and their size only for the armed file (the trader is no
    war tartane). At a traced frame's station the breadth's half-breadth at the rail is the frame's
    head's, the one measure (Pages §5.1: the rail's half-breadth is the body plan's frame cut at
    the profile's rail), where the two tables differ by their rounding."""
    half_siding = g.KEEL_SIDING_OF_BREADTH * BREADTH / 2.0
    sections = {x: headed_at_the_rail(x, pts) for x, pts in SECTIONS_MOULDED.items()}
    lines = {
        "rail": rail_at_stations(),
        "breadth": [
            [x, outside(w), outside(sections[x][-1][1] if x in sections else r)]
            for x, w, r in BREADTH_MOULDED
        ],
        "keel": KEEL_M,
        "stem": STEM_M,
        "stern": STERN_M,
        "wales": WALES_M,
        "section": [[z, outside(hb)] for z, hb in headed_at_the_rail(MIDSHIP_X, SECTION_MOULDED)],
        "decks": {"upper": DECK_M},
        "head": HEAD_M,
        "sections": [[x, z, outside(hb)] for x in sorted(sections) for z, hb in sections[x]],
        "rabbet": [[x, z, half_siding] for x, z in RABBET_Z],
    }
    if armed:
        lines["ports"] = {"upper": [[x, s, outside(hb)] for x, s, hb in PORTS_MOULDED]}
        lines["port_size"] = {"upper": list(PORT_SIZE)}
    return lines


def particulars(armed: bool) -> Particulars:
    """Her figures in the file's frame, and the checks of Tar-D §1 that need no rig raised in
    words (never an `assert`, which `python -O` strips) before the file is written."""
    # her design's 20.38 by 6.61 m (Tar-D decision 3): the breadth's 6.61 is 20⅓ pieds at the
    # pied's 0.32484 m; at the tree's 0.3248 (`period.PIED_DU_ROI_M`) it is 6.604, within a cm
    if abs(LENGTH - 20.38) > 0.01 or abs(BREADTH - 6.61) > 0.01:
        raise ValueError(
            f"Forfait's Humble converts to {LENGTH:.3f} by {BREADTH:.3f} m; 20.38 by 6.61 is "
            "her design's (Tar-D decision 3), within a centimetre."
        )
    drawn = displacement_t(PLANK_POUCES)
    low, high = (displacement_t(p) for p in PLANK_RANGE_POUCES)
    hull = {
        "length_waterline_m": LWL,
        "beam_m": cm(BREADTH),
        "draught_m": DRAUGHT,
        "displacement_kg": float(round(drawn * 1000.0, -2)),
        "gm_m": GM,
        "clr_x_m": CLR_X_M,
        "lateral_area_m2": LATERAL_AREA,
        "hull_speed_kn": HULL_SPEED_KN,
        "deck_height_m": DATUM,
        "rudder": dict(RUDDER),
    }
    return Particulars(
        hull=hull,
        hull_notes=dict(HULL_NOTES),
        lines=hull_lines(armed),
        drawn_t=drawn,
        drawn_range_t=(low, high),
    )


def profile_into(p: Particulars, report: list) -> dict:
    """Her profile and shape keys added to `p.hull` through `g.hull_profile` and `g.hull_form`,
    their notes to `p.hull_notes`; the drawn hull and each port triple's gap reported. The ports
    are measured at her plate (Pages §5.7), so a gap over the form's tolerance raises."""
    ln = dict(p.lines)
    rail, breadth = ln.pop("rail"), ln.pop("breadth")
    p.hull["profile"] = g.hull_profile(rail, breadth, **ln)
    form = {"fullness": [1.0, 1.0], "stern": {"type": "round"}, "head": "knee"}
    marks = {k: v for k, v in MARKS.items() if k.removesuffix("_m") in ln or "." in k}
    marks.update({k: MARKS[k] for k in ("rail_m", "breadth_m")})
    # the ports measured within the form's tolerance: the first three; the fourth's half-breadth
    # at its sill is read between fore 6 and fore 9, fore 7 and 8 not traced (±0.3 ft, ±0.09 m:
    # Pages §5.7), so its gap is reported and not held
    held = [("upper", x) for x, _s, _h in PORTS_MOULDED if x < 5.0]
    measured = tuple(held) if "ports" in ln else ()
    gaps = g.hull_form(p.hull, form=form, marks=marks, measured=measured, report=report)
    p.hull_notes.update(PROFILE_NOTES)
    return gaps


# ---------------------------------------------------------------------------
# Her Builder: the shared helpers' computed figures kept out of her notes (the bilander's)
# ---------------------------------------------------------------------------


class HerBuilder(g.Builder):
    """The generator's Builder, with the figures its shared helpers compute from her own keys kept
    out of her notes (the lead's notes of 2026-10-29, item 2): a spar's rating is its
    `rating_kn`. What each rule is and what it read stays."""

    RATED = re.compile(r" -> [0-9.]+ kN")

    def rate_spars(self):
        """`Builder.rate_spars`, its figures left in the file's `rating_kn` alone."""
        super().rate_spars()
        self.notes = {key: self.RATED.sub("", note) for key, note in self.notes.items()}


# ---------------------------------------------------------------------------
# The rig (Tar-D §4): masts, the two lateens, the topsail and the tréou, the head
# ---------------------------------------------------------------------------

# Her main's rake, degrees, positive aft: ONE figure (the owner's rule of 2026-11-20: "Use the
# rake which provides the better sailing characteristic, upright, or slightly forward raked").
# Measured both ways, upright (0) and 3 degrees forward (-3), on the tree as it stands
# (docs/dev/TuningNotes.md, the tartane's section): upright sails the better, her polar 0.05 to
# 0.06 kn faster at every angle in 15 kn, her best way to windward 1.92 kn against 1.89, close-
# hauled and abeam 0.07 and 0.08 kn faster at a matched helm, 2 degrees less lee helm at one
# balance; her tack and her wear split between the two by heading, a knife's edge. Upright taken;
# Chapman's Pl. LXII No. 16 draws the main upright (0.6 to 1.1 degrees aft, ±0.5: Pages §7); the
# design had 3 forward.
MAIN_RAKE_DEG = 0.0
# The mizen raked aft 10 degrees: JUDGEMENT on Forfait p. 128 (the lateen xebec's after mast
# "panché vers l'arrière"); no plate of Chapman's draws a tartane's mizen (Pages §7; the lead's
# ruling 7).
MIZEN_RAKE_DEG = 10.0
# The hounds, where the lateen's halyard block hangs, at the foot of the ton (the mast less its
# head: Tar §2.1, JUDGEMENT on the reading; Forfait p. 121 has the yard hoisted until its halyard
# block touches the one aloft); the yard slung there.
# The topsail's yard hoisted on the main's head to 3 pieds under the masthead (JUDGEMENT: its tye
# through the calcet's sheave; Tar-D §4.1 "about 15.5 m above the deck").
TOPSAIL_YARD_BELOW_HEAD = pieds(3)
# A lateen's tack a short drop under its throat, the tack's lashing at the car (JUDGEMENT; the
# sail is three-cornered, Lescallier p. 378, written with four corners for the drawing).
LUFF_M = 0.3
# The bouffette, bent to the great yard in the great lateen's place in a blow (Lescallier pp.
# 394-395; Forfait p. 129): two-thirds of its area (JUDGEMENT, Tar-D §4.1), cut alike about the
# throat.
BOUFFETTE_SHARE = 2.0 / 3.0
# Her mizen's sheet rove through an outrigger over the stern, the lugger's bout-dehors de tapecul
# (Forfait Table VII, 0.364 of the length, two-thirds of it outboard: the lugger's file),
# carried to her length (JUDGEMENT on the carrying, Tar-D §4.2): no part of the engine's, its end
# the farthest her mizen's sheet leads.
OUTRIGGER_OF_LENGTH = 0.364
OUTRIGGER_OUTBOARD = 2.0 / 3.0
# The jib's foot on the deck, 3 pieds above it at its clew (the cutter's foresail's 3 ft).
JIB_CLEW_ABOVE_DECK = pieds(3)
# Fincham 1843 art. 87, the cutter's foresail on her stay (the cutter's file): the luff 0.85 of
# the stay, the foot 0.9 of the stay's distance from the mast, the leech 0.8 of the luff.
JIB_LUFF_OF_STAY = 0.85
JIB_FOOT_OF_SPAN = 0.9
JIB_LEECH_OF_LUFF = 0.8
STORM_JIB_SHARE = 2.0 / 3.0  # Steel 1794 p. 190, the sloop's: two-thirds of the first jib
# The cutter's topsail rule (the cutter's file; Steel 1794 p. 125, 'Sloop's topsail'): the head
# 0.82 of its yard, the foot 0.9 of the square-sail yard below it, here the tréou's (Tar-D §4.1).
TOPSAIL_HEAD_OF_YARD = 0.82
FOOT_OF_YARD_BELOW = 0.9
# The tréou (Tar-D §4.1): as broad as its yard, 0.9 of it at the head (the cutter's square sail's
# 0.9 x its yard x its depth), from its yard at the hounds to the bulwark's top at the mast
# (JUDGEMENT: "from its yard to near the deck").
TREOU_BREADTH_OF_YARD = 0.9
BRACE_LIMIT_DEG = {"main.topsail.yard": 64, "main.treou.yard": 58}  # the cutter's (JUDGEMENT)

CANVAS = {
    "lateen": (2, "JUDGEMENT: no period number for a lateen found; the lugger's lug's, the "
               "cutter's mainsail's No. 1 or 2 (Steel 1794 p. 120)"),
    "mizen": (3, "JUDGEMENT: a lighter lateen than the great sail, the lugger's mizen's"),
    "topsail": g.CUTTER_CANVAS["topsail"],
    "treou": g.CUTTER_CANVAS["square_sail"],
    "jib": g.CUTTER_CANVAS["jib"],
    "storm jib": g.CUTTER_CANVAS["storm jib"],
    "bouffette": (1, "JUDGEMENT: the storm lateen, of the heaviest, as the lugger's taille-vent"),
}  # fmt: skip

# Rope sizes, inches of circumference (JUDGEMENT: no table of a tartane's rigging found; the
# lugger's and the cutter's sizes for like gear, her yards the longer), rated by Luce 1866 ch. IV
# as every line is: (circumference, parts).
LATEEN_ROPE = {
    "main": {"halyard": (4.5, 2), "guy": (3.0, 1), "vang": (2.5, 1), "sheet": (3.5, 2),
             "tack": (3.5, 1)},
    "mizzen": {"halyard": (3.0, 2), "guy": (2.0, 1), "vang": (2.0, 1), "sheet": (2.5, 2),
               "tack": (2.5, 1)},
}  # fmt: skip
SHROUDS = {"main": (6.0, 3), "mizzen": (3.5, 2)}  # a side
BOUFFETTE_ROPE = {"sheet": (3.5, 2), "tack": (3.5, 1)}
JIB_ROPE = {"halyard": (3.0, 2), "sheet": (3.0, 1), "downhaul": (2.5, 1)}
JIB_STAY_IN = 5.0
DESIGN_WIND = dict(g.DESIGN_WIND_KN, lateen=45.0, treou=22.0)  # a lateen as a lug (the lugger's)


@dataclass
class Mast:
    """A mast's line in the frame: its x at the deck at side, its rake, its heel, its hounds and
    its head above the water."""

    name: str
    x_deck: float
    deck_z: float
    rake_deg: float
    heel_z: float
    length: float
    head: float

    def x_at(self, z: float) -> float:
        """The mast's raked line's x at a height above the water."""
        return self.x_deck - math.tan(math.radians(self.rake_deg)) * (z - self.deck_z)

    def up(self, along: float) -> float:
        """The height above the water of the point `along` metres up the mast from its heel."""
        return self.heel_z + along * math.cos(math.radians(self.rake_deg))

    @property
    def hounds_z(self) -> float:
        return self.up(self.length - self.head)

    @property
    def head_z(self) -> float:
        return self.up(self.length)


def masts(rake_deg: float | None = None) -> dict[str, Mast]:
    """Her two masts at Forfait's places from the middle of her perpendiculars, each heel on a
    keelson over the keel's upper edge (Pages §6.4); her main at `MAIN_RAKE_DEG` unless a rake is
    given (read when called, so that the one figure rules every reader)."""
    rake_deg = MAIN_RAKE_DEG if rake_deg is None else rake_deg
    out = {}
    for name, place, sign, length, head, rake in (
        ("main", "main_place", 1.0, "main", "main_head", rake_deg),
        ("mizzen", "mizen_place", -1.0, "mizen", "mizen_head", MIZEN_RAKE_DEG),
    ):
        deck_z, keel_z = MAST_DECK[name]
        out[name] = Mast(
            name=name,
            x_deck=MIDDLE_X + sign * humble(place),
            deck_z=deck_z,
            rake_deg=rake,
            heel_z=keel_z + KEELSON_M,
            length=humble(length),
            head=humble(head),
        )
    return out


def car_at_the_stem(m: Mast) -> float:
    """The great yard's angle to the horizontal at which its car comes to the stem's fore face,
    the car tacked at the stem (Forfait p. 121; Tar-D §4.1), degrees: by halving."""
    fore = lateen.SLING_OF_YARD * humble("lateen_yard")
    sx, sz = m.x_at(m.hounds_z), m.hounds_z

    def beyond(deg):
        car = (sx + fore * math.cos(math.radians(deg)), sz - fore * math.sin(math.radians(deg)))
        return car[0] - stem_x_at(car[1])

    lo, hi = 1.0, 89.0
    if beyond(lo) <= 0.0 or beyond(hi) >= 0.0:
        raise ValueError("the great yard's car cannot be brought to the stem from its sling.")
    for _ in range(60):
        mid = (lo + hi) / 2.0
        if beyond(mid) > 0.0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def lateen_cuts(m: dict[str, Mast]) -> dict:
    """Her two lateens and the bouffette (Tar-D §4.1, §4.2), by `lateen.cut`:
    - the great lateen on its 75-pied yard slung at the main's hounds on its raked line, its car
      tacked at the stem (Forfait p. 121), the angle so found; its head the yard less its ends;
      its clew on the deck at the foot of the mast (Forfait p. 121, as her design reads it, R);
    - the mizen lateen cut alike, "semblable" to the main's (Forfait pp. 124-125): its 47-pied
      yard at the great yard's angle (JUDGEMENT), slung at the mizen's hounds, its clew on the
      deck at the mizen's foot, its sheet to the outrigger over the stern;
    - the bouffette, two-thirds of the great lateen's area, cut alike about its throat."""
    main, miz = m["main"], m["mizzen"]
    deg = car_at_the_stem(main)
    out = {"yard_deg": deg}
    for name, mast, yard, ends in (
        ("main", main, "lateen_yard", "lateen_yard_ends"),
        ("mizzen", miz, "mizen_yard", "mizen_yard_ends"),
    ):
        penne, car = (pieds(*e) for e in HUMBLE[ends])
        out[name] = lateen.cut(
            yard_m=humble(yard),
            car_end_m=car,
            penne_end_m=penne,
            yard_deg=deg,
            sling_z=mast.hounds_z,
            mast_x_at=mast.x_at,
            luff_m=LUFF_M,
            clew=(mast.x_deck, mast.deck_z),
        )
    great = out["main"]
    k = math.sqrt(BOUFFETTE_SHARE)
    tack, throat, peak, clew = great["corners"]

    def about_throat(p):
        return (throat[0] + k * (p[0] - throat[0]), throat[1] + k * (p[1] - throat[1]))

    corners = [tack, throat, about_throat(peak), about_throat(clew)]
    area, cx, cz = lateen.area_centroid(corners)
    out["bouffette"] = {"corners": corners, "area": area, "centre": (cx, cz)}
    return out


def outrigger_end() -> float:
    """The outrigger's end over the stern, x: two-thirds of it outboard of the taffrail."""
    return TAFFRAIL_X - OUTRIGGER_OUTBOARD * OUTRIGGER_OF_LENGTH * LENGTH


def square_cuts(m: dict[str, Mast]) -> dict:
    """Her topsail and her tréou on her main (Tar-D §4.1): their yards' heights above the water,
    their areas, their centres (x, z)."""
    main = m["main"]
    ts_yard_z = main.head_z - TOPSAIL_YARD_BELOW_HEAD
    hounds = main.hounds_z
    ts_yard, treou_yard = humble("topsail_yard"), pieds(*TREOU_YARD)
    depth = ts_yard_z - hounds
    head, foot = TOPSAIL_HEAD_OF_YARD * ts_yard, FOOT_OF_YARD_BELOW * treou_yard
    ts_area = (head + foot) / 2.0 * depth
    ts_z = hounds + depth / 2.0
    rail = interp(RAIL_M, main.x_deck)
    tr_depth = hounds - rail
    tr_area = TREOU_BREADTH_OF_YARD * treou_yard * tr_depth
    tr_z = hounds - 0.45 * tr_depth  # the cutter's square sail's centre, 0.45 under its yard
    return {
        "main.topsail": {
            "yard_z": ts_yard_z,
            "area": ts_area,
            "centre": (main.x_at(ts_z), ts_z),
            "depth": depth,
            "head": head,
            "foot": foot,
        },
        "main.treou": {
            "yard_z": hounds,
            "area": tr_area,
            "centre": (main.x_at(tr_z), tr_z),
            "depth": tr_depth,
        },
    }


def jib_cut(m: dict[str, Mast]) -> dict:
    """Her one great jib (Tar-D §4.3, decision 11) from the berthelot's end to the main's hounds:
    the cutter's foresail rule on her stay (Fincham art. 87), its tack at the berthelot's end, its
    head on the stay, its clew on the foot's line 3 pieds above her deck; its storm jib two-thirds
    of it (Steel 1794 p. 190)."""
    main = m["main"]
    tack = (STEM_HEAD[0] + humble("eperon"), BEAK_Z)
    top = (main.x_at(main.hounds_z), main.hounds_z)
    stay = math.dist(tack, top)
    luff = JIB_LUFF_OF_STAY * stay
    foot = JIB_FOOT_OF_SPAN * (tack[0] - main.x_deck)
    leech = JIB_LEECH_OF_LUFF * luff
    s = (luff + foot + leech) / 2.0
    area = math.sqrt(s * (s - luff) * (s - foot) * (s - leech))
    head = (
        tack[0] + (top[0] - tack[0]) * luff / stay,
        tack[1] + (top[1] - tack[1]) * luff / stay,
    )
    cx = tack[0] - foot
    clew = (cx, deck_at(cx) + JIB_CLEW_ABOVE_DECK)
    centre = ((tack[0] + head[0] + clew[0]) / 3.0, (tack[1] + head[1] + clew[1]) / 3.0)
    return {
        "corners": [tack, head, clew],
        "area": area,
        "centre": centre,
        "stay": stay,
        "luff": luff,
        "foot": foot,
        "leech": leech,
        "storm": STORM_JIB_SHARE * area,
    }


def above_datum(z: float) -> float:
    return cm(z - DATUM)


def written(corners) -> list[list[float]]:
    """Corners above the datum, to the centimetre, as the file writes them."""
    return [[cm(x), cm(z - DATUM)] for x, z in corners]


def as_water(corners) -> list[tuple[float, float]]:
    """Written corners back above the water."""
    return [(x, z + DATUM) for x, z in corners]


def check_rig(m: dict[str, Mast], cuts: dict, squares: dict, jib: dict) -> list[str]:
    """Tar-D §1's checks on her rig, each raised in words: the great lateen's sling a third along
    its yard within 0.1 m of the main's raked line, its peak and clew inboard of the taffrail; the
    mizen's peak and clew inboard of the outrigger's end; each lateen's tack and clew on or above
    her deck; the sum of her plain sail within Tar-D §4.5's band of Forfait's, his topgallant's
    share off. Returns the report's sentences."""
    out = []
    lines = {
        name: lateen.lines(f"{name}.lateen_yard", f"{name}.lateen") for name in ("main", "mizzen")
    }
    for name, aft_x, yard, ends in (
        ("main", TAFFRAIL_X, "lateen_yard", "lateen_yard_ends"),
        ("mizzen", outrigger_end(), "mizen_yard", "mizen_yard_ends"),
    ):
        cut = dict(cuts[name], corners=as_water(written(cuts[name]["corners"])))
        penne, car = (pieds(*e) for e in HUMBLE[ends])
        lateen.check(
            cut,
            lines[name],
            mast_x_at=m[name].x_at,
            aft_x=aft_x,
            sail_id=f"{name}.lateen",
            yard_m=humble(yard),
            ends=(car, penne),
            deck_at=lambda x: deck_at(x) - 0.006,  # the corners as written, to the centimetre
        )
    plain = (
        cuts["main"]["area"]
        + cuts["mizzen"]["area"]
        + squares["main.topsail"]["area"]
        + jib["area"]
    )
    want = FORFAIT_SAIL_M2 - TOPGALLANT_SHARE_M2
    off = plain / want - 1.0
    if abs(off) > SAIL_BAND:
        raise ValueError(
            f"her plain sail is {plain:.1f} m², {off:+.1%} of Forfait's Humble less his "
            f"topgallant ({want:.1f} m²); within ±{SAIL_BAND:.0%} is wanted (Tar-D §4.5)."
        )
    out.append(
        f"her plain sail {plain:.1f} m² against Forfait's {FORFAIT_SAIL_M2:.1f} m² less the "
        f"topgallant's {TOPGALLANT_SHARE_M2:g} ({want:.1f}): {off:+.1%}, within ±{SAIL_BAND:.0%}."
    )
    return out


PROV = " Provisional (truth 9), see gen_ships.py."


# ---------------------------------------------------------------------------
# The two files: her name, her era note and header, her role's company and guns
# ---------------------------------------------------------------------------

TRADER, COASTGUARD = "trader", "coastguard"
FILES = {TRADER: "tartane.yaml", COASTGUARD: "coastguard-tartane.yaml"}
PEOPLE = {TRADER: "tartane", COASTGUARD: "coastguard-tartane"}
# Her name, a saint's, as Provençal tartanes were named (Tar-D decision 20: Saint-Pierre
# proposed, JUDGEMENT; the owner's question 6, answered as picked); the guarda-costa the same
# saint in the Spanish service's words (JUDGEMENT).
NAMES = {TRADER: "Saint-Pierre", COASTGUARD: "San Pedro"}

RIG_WORDS = (
    "a Provençal tartane under a great lateen and a square topsail: one main mast à calcet, "
    "{rake}, with a whole lateen on a 75-pied yard slung at a third and a loose-footed square "
    "topsail on its head, a diminutive mizen raked aft with its lateen sheeted to an outrigger "
    "over the stern, one great jib on the berthelot over the éperon, and a square tréou set "
    "flying before the wind"
)


def rake_words(rake: float) -> str:
    if rake == 0.0:
        return "upright"
    return f"raked {abs(rake):g} degrees {'aft' if rake > 0 else 'forward'}"


def era_notes(role: str) -> str:
    """Her era note; its first clause, before its colon, is the class her readings serve
    (`api.readings.ship_class_words`)."""
    rig = RIG_WORDS.format(rake=rake_words(MAIN_RAKE_DEG))
    hull = (
        " Forfait 1788's Humble of 100 tonneaux with topsail and mizen, 62¾ by 20⅓ pieds (20.38 "
        "by 6.60 m; Traité de la mâture, Table II), drawn on Chapman 1768's French tartane (Pl. "
        "LVII No. 16) scaled to her; her draught 2.38 m on her load line, her waterline 18.47 m."
    )
    if role == TRADER:
        return (
            rig[0].upper()
            + rig[1:]
            + "."
            + hull
            + " Unarmed, a trader of ten: her master and mate, six seamen, a boy and a cook. "
            "Undated. See tools/ships/tartane.py for every figure's source."
        )
    return (
        "A Spanish guarda-costa tartane, the same hull as the trader: "
        + rig
        + "."
        + hull
        + " Chapman's eight 4-pounders and four swivels on the war tartane's four ports a side, "
        "and a company of thirty-four, the Treasury's coastguard (the navy's from 1802 to April "
        "1805: Winfield et al. 2023, pp. 168-169). Undated. See tools/ships/tartane.py for every "
        "figure's source."
    )


def header(role: str) -> str:
    what = (
        "a Provençal coaster under a great lateen and a square topsail"
        if role == TRADER
        else "the Spanish guarda-costa of the same hull, with Chapman's eight 4-pounders"
    )
    return (
        f"# The tartane {NAMES[role]}: {what};\n"
        "# Forfait 1788's Humble (Table II) drawn on Chapman 1768's French tartane (Pl. LVII\n"
        "# No. 16, measured at her scale on the museum's photograph and never copied).\n"
        "# Generated by tools/gen_ships.py (tools/ships/tartane.py, her lateens by\n"
        "# tools/ships/lateen.py); edit those and rerun, do not edit this file. Her design:\n"
        "# docs/design/Design-Ship-Tartane.md. Rope: the lugger's and the cutter's for like gear\n"
        "# (judgement). Spar ratings are provisional, set for truth 9 with the M1 sail curves;\n"
        "# see the script. Canvas: Steel 1794 vol. I; cloth ratings from the number by Luce\n"
        "# App. E. Units: metres, m2, kg, kN. Comments mark judgements.\n"
    )


def write(out_dir: str, p: Particulars, role: str) -> dict:
    """Build one of her files and dump it to `out_dir`: the hull, the masts and yards, the two
    lateens, the topsail and the tréou, the head, the storm canvas, the groups and the aliases
    (Tar-D §4's order); then her company and stores, the coastguard's guns and bill, the hold,
    the pumps and the boat (the house's order), and her description. Returns her report's
    figures."""
    report: list[str] = []
    gaps = profile_into(p, report)
    rep: dict = {"hull": report, "gaps": gaps}
    b = HerBuilder(NAMES[role], "tartane", era_notes(role), p.hull, p.hull_notes)
    m = masts()
    cuts = lateen_cuts(m)
    squares = square_cuts(m)
    jib = jib_cut(m)
    rep["rig"] = check_rig(m, cuts, squares, jib)
    rep.update(masts=m, cuts=cuts, squares=squares, jib=jib)
    spars(b, m, cuts, squares, jib)
    sails(b, m, cuts, squares, jib)
    groups_and_aliases(b)
    ground_tackle(b, role)
    company(b, role)
    if role == COASTGUARD:
        guns = her_guns(p.hull["profile"])
        armament(b, guns)
        quarter_bill(b, guns)
        rep["bill"] = at_the_guns(guns)
    hold_pumps_boat(b, role)
    b.descriptions([DESCRIPTION[role]])
    b.dump(os.path.join(out_dir, FILES[role]), header(role))
    rep["plain"] = sum(
        next(s["area_m2"] for s in b.doc["sails"] if s["id"] == sid)
        for sid in b.doc["groups"]["plain sail"]
    )
    return rep


def loads(cuts: dict, squares: dict, jib: dict) -> dict[str, tuple[float, float, str]]:
    """Each working sail's (area, centre above her water, curve class) for the spars' ratings."""
    out = {
        "main.lateen": (cuts["main"]["area"], cuts["main"]["centre"][1], "lateen"),
        "mizzen.lateen": (cuts["mizzen"]["area"], cuts["mizzen"]["centre"][1], "lateen"),
        "jib": (jib["area"], jib["centre"][1], "jibheaded"),
    }
    for sid, sq in squares.items():
        out[sid] = (sq["area"], sq["centre"][1], "square")
    return {k: (round(a), round(z, 1), c) for k, (a, z, c) in out.items()}


def spars(b, m: dict[str, Mast], cuts: dict, squares: dict, jib: dict) -> None:
    """Her spars (Tar-D §4.1-§4.3): the main à calcet, a pole with no topmast, its great lateen
    yard, its topsail yard on its head and the tréou's yard at its hounds; the mizen and its
    lateen yard; the éperon with the berthelot. A mast's `x_m` is its line at the datum, its
    `height_m` its head above the datum; a yard's `height_m` its sling's."""
    ld = loads(cuts, squares, jib)
    dw = DESIGN_WIND
    main, miz = m["main"], m["mizzen"]
    b.spar(
        "main.mast",
        "mast",
        x_m=cm(main.x_at(DATUM)),
        rake_deg=MAIN_RAKE_DEG or None,
        height_m=above_datum(main.head_z),
        rating_kn=g.design_kn(
            [ld["main.lateen"], ld["main.topsail"], ld["main.treou"], ld["jib"]], dw["lower"]
        ),
        note="the main mast à calcet, 59 pieds heel to head, 22 pouces at the deck, its head (the "
        "ton) 26 pieds, stepped 10 pieds 5 pouces before the middle (Forfait 1788 Table II, the "
        "Humble); short and stout, its head a square block pierced with sheaves for the halyards, "
        "no stays (Lescallier 1791 pp. 376-377): a pole, with no topmast, the topsail's yard "
        "hoisted on its head. Its heel on a keelson over the keel's upper edge (JUDGEMENT: none "
        "drawn), 2.72 m below the deck at side (Pages §6.4). Its rake: "
        f"{rake_words(MAIN_RAKE_DEG)}, by the owner's rule of 2026-11-20 (the better sailing of "
        "upright and slightly forward, measured: docs/dev/TuningNotes.md, the tartane's section); "
        "Chapman's Pl. LXII No. 16 draws a tartane's main upright (0.6 to 1.1 degrees aft, Pages "
        "§7)." + PROV,
    )
    b.spar(
        "main.lateen_yard",
        "lateen_yard",
        on="main.mast",
        length_m=cm(humble("lateen_yard")),
        height_m=above_datum(cuts["main"]["sling"][1]),
        rating_kn=g.design_kn([ld["main.lateen"]], dw["lateen"]),
        note="the great lateen yard, the antenne, 75 pieds, 9¼ pouces in the slings, its ends 1½ "
        "pieds at the penne and ¾ at the car (Forfait 1788 Table II, 1.195 of her length: longer "
        "than the vessel); of two pieces of fir fished together, slung by its parrel a third of "
        "its length from the car (Lescallier 1791 pp. 378-379) at the main's hounds, where its "
        "jeers' block hangs at the foot of the ton (Tar §2.1, JUDGEMENT on the reading; Forfait p. "
        "121); height_m the sling. Peaked so that the car is tacked at the stem (Forfait p. 121), "
        "an angle her report gives; Chapman's Pl. LXII peaks his tartane's main yard about 55 "
        "degrees on another rig (Pages §7, recorded). Not braced: its trim is its sheet's, its "
        "ourses' and its vangs'.",
    )
    b.spar(
        "main.topsail.yard",
        "yard",
        on="main.mast",
        length_m=cm(humble("topsail_yard")),
        height_m=above_datum(squares["main.topsail"]["yard_z"]),
        brace_limit_deg=BRACE_LIMIT_DEG["main.topsail.yard"],
        rating_kn=g.design_kn([ld["main.topsail"]], dw["topsail"]),
        note="the topsail yard, 32 pieds, 6¼ pouces (Forfait 1788 Table II, the Humble), hoisted "
        "on the main's own head, its tye through the calcet's sheave, 3 pieds under the masthead "
        "(JUDGEMENT): on the pole main, no topmast. The Humble's topgallant yard, 24½ pieds, is "
        "not crossed: no topgallant (Tar-D §4.1; the owner's picture, Monleón's print and Röding "
        "show none). Braced 64 degrees from square, the cutter's topsail yard's (JUDGEMENT)."
        + PROV,
    )
    b.spar(
        "main.treou.yard",
        "yard",
        on="main.mast",
        length_m=cm(pieds(*TREOU_YARD)),
        height_m=above_datum(squares["main.treou"]["yard_z"]),
        brace_limit_deg=BRACE_LIMIT_DEG["main.treou.yard"],
        rating_kn=g.design_kn([ld["main.treou"]], dw["treou"]),
        note="the tréou's yard, 41 pieds, 8½ pouces (Forfait 1788 Table II: the Espiègle's square "
        "yard and the square-sail column's), hoisted to the main's hounds, where it spreads the "
        "topsail's foot when it is up (the cutter's square-sail yard's place). Not crossed in "
        "plain sail: sent up with the tréou and struck with it, the period's way of setting it "
        "flying (Tar-D decision 9; the owner's reading of the prints, 2026-11-19: no yard under "
        "the topsail), so its sail is set flying. Braced 58 degrees from square, the cutter's "
        "square-sail yard's (JUDGEMENT)." + PROV,
    )
    b.spar(
        "mizzen.mast",
        "mast",
        x_m=cm(miz.x_at(DATUM)),
        rake_deg=MIZEN_RAKE_DEG,
        height_m=above_datum(miz.head_z),
        rating_kn=g.design_kn([ld["mizzen.lateen"]], dw["lower"]),
        note="the mizen (Forfait's tapecul, the Levant's misaine), 30 pieds heel to head, 10 "
        "pouces, its head 6 pieds, stepped 15 pieds 2 pouces abaft the middle (Forfait 1788 Table "
        "II, the Humble), raked aft 10 degrees (JUDGEMENT on Forfait p. 128: the lateen xebec's "
        "after mast 'panché vers l'arrière'; no plate of Chapman's draws a tartane's mizen, Pages "
        "§7, the lead's ruling 7). Its heel on a keelson, 2.85 m below the deck at side (Pages "
        "§6.4; JUDGEMENT on the keelson). Added to lateen vessels 'to bring them to the wind' "
        "(Lescallier p. 393)." + PROV,
    )
    b.spar(
        "mizzen.lateen_yard",
        "lateen_yard",
        on="mizzen.mast",
        length_m=cm(humble("mizen_yard")),
        height_m=above_datum(cuts["mizzen"]["sling"][1]),
        rating_kn=g.design_kn([ld["mizzen.lateen"]], dw["lateen"]),
        note="the mizen's lateen yard, 47 pieds, 6 pouces, its ends a pied (Forfait 1788 Table II; "
        "one figure printed, taken for each end), slung a third of its length from the car at the "
        "mizen's hounds, peaked as the great yard (JUDGEMENT: the sail 'semblable' to the main's, "
        "Forfait pp. 124-125); height_m the sling. Its peak stands over the stern, inside the "
        "outrigger's end.",
    )
    b.spar(
        "bowsprit",
        "bowsprit",
        x_m=STEM_HEAD[0],
        length_m=cm(humble("eperon")),
        height_m=above_datum(BEAK_Z),
        rating_kn=g.design_kn([ld["jib"]], dw["lower"]),
        note="the éperon, the beak, with the berthelot laid on it (Forfait p. 125; Lescallier p. "
        "393): 10½ pieds beyond the stem head (Forfait 1788 Table II; the lead's ruling 3 of "
        "2026-11-20, the printed ratio 0.151 the misprint, JUDGEMENT), level on Chapman's plate, "
        "its middle line 2.85 m above the water (Pages §5.4); Chapman's beak, scaled, 3.53 m to "
        "the berthelot's point (the cross-check). A fixed spar; its end the jib's tack and the "
        "forward ourse's lead (Lescallier p. 393)." + PROV,
    )
    for name, mast in (("main", "main.mast"), ("mizzen", "mizzen.mast")):
        circ, parts = SHROUDS[name]
        b.sided(
            f"{name}.shrouds",
            "shroud",
            mast,
            rating=g.rope_kn(circ, parts),
            note=f"the {name} mast's column shrouds (haubans à colonne), {parts} a side of "
            f"{circ:g} in (JUDGEMENT on the count and the size): a pendant from the masthead, a "
            "single block at its foot and a runner set up by a tackle to the gunwale, cast off "
            "when the yard is changed round the mast (Lescallier pp. 377-378; Röding).",
        )
    b.line(
        "jib.stay",
        "stay",
        "main.mast",
        rating=g.rope_kn(JIB_STAY_IN),
        note="the line the jib's luff lies along, from the main's hounds to the berthelot's end; "
        "the jib sets flying, hoisted by its halyard with its tack at the berthelot's end, as the "
        f"cutter's (the cutter's file). {JIB_STAY_IN:g} in (JUDGEMENT).",
    )


def lateen_lines(b, name: str) -> None:
    """A lateen's lines by `lateen.lines` (Lescallier p. 379), each rated from its size."""
    rope = LATEEN_ROPE[name]
    words = {
        "jeers": "the jeers (drisse) through the calcet's sheave (Forfait p. 121)",
        "ourse": "the ourses (à proue, à poupe) at the car to windward, the forward one to the "
        "berthelot's end (Lescallier pp. 379, 393): a guy a side, as the settee's are filed",
        "oste": "the brace (oste) at the penne on its pendant: a vang a side, a lateen yard being "
        "no braced yard",
        "van": "the vang (van) at the penne on its pendant and fall, which steadies the yard and "
        "takes its strain: a vang a side",
        "sheet": "the one sheet, hauled aft and to leeward (Lescallier p. 379)",
        "tack": "the tack, the car tacked at the stem (Forfait p. 121)",
    }
    seen = set()
    for lid, cls, of, side in lateen.lines(f"{name}.lateen_yard", f"{name}.lateen"):
        circ, parts = rope[cls]
        part = lid.split(".")[-2] if side else lid.split(".")[-1]
        note = None
        if part not in seen:
            seen.add(part)
            note = f"{words[part]}; {circ:g} in" + (f", {parts} parts" if parts > 1 else "")
            note += " (JUDGEMENT)."
        b.line(lid, cls, of, side=side, rating=g.rope_kn(circ, parts), note=note, parts=parts)


def sails(b, m: dict[str, Mast], cuts: dict, squares: dict, jib: dict) -> None:
    """Her sails (Tar-D §4): the great lateen, the topsail, the tréou set flying, the mizen
    lateen, the one jib; in the sail room the bouffette and the storm jib."""
    deg = cuts["yard_deg"]
    great = cuts["main"]
    corners = written(great["corners"])
    area, cx, cz = lateen.area_centroid(as_water(corners))
    b.sail(
        "main.lateen",
        "lateen",
        yard="main.lateen_yard",
        area_m2=round(area),
        reef_bands=1,
        x_m=cm(cx),
        centre_height_m=round(cz, 1),
        canvas_no=CANVAS["lateen"][0],
        cloth_rating_kn=g.cloth(round(area), CANVAS["lateen"][0]),
        corners_m=corners,
        note=f"the great lateen (la mestre), whole, three-cornered (Lescallier p. 378), cut by "
        "tools/ships/lateen.py: its head the yard less its ends, 72¾ pieds (Forfait p. 121); the "
        f"yard peaked {deg:.1f} degrees so that the car is tacked at the stem, and the clew on the "
        "deck at the foot of the mast (Forfait p. 121, as her design reads it, R; Tar §3.4); the "
        "tack a short luff under the throat, the car's lashing (JUDGEMENT), so that it is written "
        "with four corners for the drawing. Plainly: the design's 100 to 140 m² (JUDGEMENT) is "
        "missed, its own rule giving less; her plain sail meets Forfait's (her report). One reef "
        "band (Lescallier p. 379: oblique in the period; the engine's band parallel to the foot). "
        "Whole, with no cut_at_mast; its side (dipping) waits on the engine's step A1a."
        + g.canvas_note(CANVAS["lateen"]),
    )
    ts = squares["main.topsail"]
    b.sail(
        "main.topsail",
        "square",
        yard="main.topsail.yard",
        area_m2=round(ts["area"]),
        reef_bands=1,
        x_m=cm(ts["centre"][0]),
        centre_height_m=round(ts["centre"][1], 1),
        canvas_no=CANVAS["topsail"][0],
        cloth_rating_kn=g.cloth(round(ts["area"]), CANVAS["topsail"][0]),
        note="the topsail (le hunier), square, loose-footed, cut by the cutter's topsail rule "
        "(the cutter's file; Steel 1794 p. 125, 'Sloop's topsail') between its yard and the "
        "main's hounds: its head 0.82 of its yard, its foot 0.9 of the tréou's yard, the square-"
        "sail yard below it; its sheets to the deck, no lower yard set in plain sail (Tar-D "
        "decision 8; the owner's reading of the prints, 2026-11-19). On a pole main it is a course "
        "to the engine until the steps A5 and A6. One reef band (the cutter's topsail's)."
        + g.canvas_note(CANVAS["topsail"]),
    )
    tr = squares["main.treou"]
    b.sail(
        "main.treou",
        "square",
        yard="main.treou.yard",
        area_m2=round(tr["area"]),
        x_m=cm(tr["centre"][0]),
        centre_height_m=round(tr["centre"][1], 1),
        canvas_no=CANVAS["treou"][0],
        cloth_rating_kn=g.cloth(round(tr["area"]), CANVAS["treou"][0]),
        flying=True,
        note="the tréou, the square sail set before the wind and in too much wind (Lescallier pp. "
        "395, 401; Falconer 1780, TREOU, SQUARE-SAIL; Steel: 'like a cross-jack'), never in plain "
        "sail; as broad as its yard, 0.9 of it, from its yard at the hounds to the bulwark's top "
        "at the mast (JUDGEMENT: 'from its yard to near the deck'). Set flying, its yard sent up "
        "with it and struck with it (Tar-D decision 9), never reefed aloft."
        + g.canvas_note(CANVAS["treou"]),
    )
    miz = cuts["mizzen"]
    corners = written(miz["corners"])
    area, cx, cz = lateen.area_centroid(as_water(corners))
    b.sail(
        "mizzen.lateen",
        "lateen",
        yard="mizzen.lateen_yard",
        area_m2=round(area),
        reef_bands=1,
        x_m=cm(cx),
        centre_height_m=round(cz, 1),
        canvas_no=CANVAS["mizen"][0],
        cloth_rating_kn=g.cloth(round(area), CANVAS["mizen"][0]),
        corners_m=corners,
        note="the mizen lateen, whole, 'semblable' to the great lateen and smaller (Forfait pp. "
        "124-125), cut by the same rule (Forfait p. 121): its head the yard less its ends, the "
        "yard peaked as the great yard (JUDGEMENT), the clew on the deck at the foot of its mast; "
        f"its sheet led to the outrigger over the stern, whose end stands {outrigger_end():.2f} m "
        "in her frame, two-thirds of the lugger's bout-dehors de tapecul outboard (Forfait Table "
        "VII, 0.364 of the length; JUDGEMENT on the carrying). Plainly: the design's 30 to 45 m² "
        "(JUDGEMENT) is missed, its own rule giving less. Worked as a ship's mizen going about and "
        "kept set hove to (Tar-D §4.2; the plan's §4 row 4); its side waits on the step A1a."
        + g.canvas_note(CANVAS["mizen"]),
    )
    tack, head, clew = jib["corners"]
    b.sail(
        "jib",
        "jibheaded",
        stay="jib.stay",
        area_m2=round(jib["area"]),
        x_m=cm(jib["centre"][0]),
        centre_height_m=round(jib["centre"][1], 1),
        canvas_no=CANVAS["jib"][0],
        cloth_rating_kn=g.cloth(round(jib["area"]), CANVAS["jib"][0]),
        corners_m=written(jib["corners"]),
        note="the one great jib (le foc: Lescallier p. 401; Steel, 'a large jib'; Röding) from "
        "the berthelot's end to the main's hounds, one headsail on the owner's reading of the "
        "prints (2026-11-19; Tar-D decision 11): cut by the cutter's foresail rule on her stay "
        "(Fincham 1843 art. 87): the luff 0.85 of the stay, the foot 0.9 of the stay's span to "
        "the mast, the leech 0.8 of the luff; its clew 3 pieds above her deck. No reef bands: "
        "the storm jib is shifted for it." + g.canvas_note(CANVAS["jib"]),
    )
    bf = cuts["bouffette"]
    corners = written(bf["corners"])
    area, cx, cz = lateen.area_centroid(as_water(corners))
    b.sail(
        "main.bouffette",
        "lateen",
        yard="main.lateen_yard",
        area_m2=round(area),
        x_m=cm(cx),
        centre_height_m=round(cz, 1),
        canvas_no=CANVAS["bouffette"][0],
        cloth_rating_kn=g.cloth(round(area), CANVAS["bouffette"][0]),
        corners_m=corners,
        bent=False,
        in_place_of="main.lateen",
        note="the bouffette, a smaller lateen bent to the great yard in the great lateen's place "
        "in a blow (Lescallier pp. 394-395, the galley's; Forfait p. 129), as the lugger's "
        "taille-vent: two-thirds of the great lateen's area, cut alike about its throat "
        "(JUDGEMENT, Tar-D §4.1); in the sail room." + g.canvas_note(CANVAS["bouffette"]),
    )
    storm = round(jib["storm"])
    b.sail(
        "storm_jib",
        "jibheaded",
        stay="jib.stay",
        area_m2=storm,
        x_m=cm(jib["centre"][0]),
        centre_height_m=round(jib["centre"][1] * 0.9, 1),
        canvas_no=CANVAS["storm jib"][0],
        cloth_rating_kn=g.storm_cloth(storm),
        bent=False,
        in_place_of="jib",
        note="the storm jib, two-thirds of the jib (Steel 1794 p. 190, the sloop's), the "
        "cutter's pattern (JUDGEMENT, Tar-D §4.3); in the sail room."
        + g.canvas_note(CANVAS["storm jib"], storm=True),
    )
    # -- their lines ---------------------------------------------------------------------
    lateen_lines(b, "main")
    lateen_lines(b, "mizzen")
    g.square_sail_lines(
        b, "main.topsail", "main.topsail.yard", g.CUTTER_ROPE["topsail"], hoisting=True, reef=True
    )
    g.square_sail_lines(
        b, "main.treou", "main.treou.yard", g.CUTTER_ROPE["square_sail"], hoisting=True
    )
    for lid, cls, (circ, parts) in (
        ("main.bouffette.sheet", "sheet", BOUFFETTE_ROPE["sheet"]),
        ("main.bouffette.tack", "tack", BOUFFETTE_ROPE["tack"]),
    ):
        b.line(lid, cls, "main.bouffette", rating=g.rope_kn(circ, parts), parts=parts)
    for sid in ("jib", "storm_jib"):
        b.line(f"{sid}.halyard", "halyard", sid, rating=g.rope_kn(*JIB_ROPE["halyard"]), parts=2)
        b.sided(f"{sid}.sheet", "sheet", sid, rating=g.rope_kn(*JIB_ROPE["sheet"]))
        b.line(f"{sid}.downhaul", "downhaul", sid, rating=g.rope_kn(*JIB_ROPE["downhaul"]))


def groups_and_aliases(b) -> None:
    """Her groups and aliases (Tar-D §4.4): no "courses", her lateen being no course (the gale's
    reduction must not reef it as one). Her design's "lateens" group, for `shift the lateens` and
    the practice's orders, waits on the step A1b that builds those orders: a one-word family of
    sails is one the standing book's fitting knows (`standing.book.SAIL_FAMILIES`, truth 7-625:
    "a new one is added on purpose"), which A1b adds with it."""
    b.group("plain sail", ["main.lateen", "main.topsail", "mizzen.lateen", "jib"])
    b.group("all sail", ["main.lateen", "main.topsail", "main.treou", "mizzen.lateen", "jib"])
    b.group("square sails", ["main.topsail", "main.treou"])
    b.group("fore-and-aft sails", ["main.lateen", "mizzen.lateen", "jib"])
    b.group("headsails", ["jib"])
    b.group("jibs", ["jib"])
    b.group("topsails", ["main.topsail"])
    b.group("storm canvas", ["storm_jib"])
    b.group("yards", ["main.topsail.yard", "main.treou.yard"])
    b.group("main yards", ["main.topsail.yard", "main.treou.yard"])
    b.group("topsail yards", ["main.topsail.yard"])
    b.group("lower masts", ["main.mast", "mizzen.mast"])
    for words, target in (
        ("mainsail", "main.lateen"),
        ("main sail", "main.lateen"),
        ("the mainsail", "main.lateen"),
        ("the lateen", "main.lateen"),
        ("the great lateen", "main.lateen"),
        ("great lateen", "main.lateen"),
        ("mestre", "main.lateen"),
        ("mizen", "mizzen.lateen"),
        ("mizzen", "mizzen.lateen"),
        ("the mizen", "mizzen.lateen"),
        ("the mizen lateen", "mizzen.lateen"),
        ("mizen lateen", "mizzen.lateen"),
        ("main yard", "main.lateen_yard"),
        ("the antenna", "main.lateen_yard"),
        ("lateen yard", "main.lateen_yard"),
        ("square sail", "main.treou"),
        ("the square sail", "main.treou"),
        ("treou", "main.treou"),
        ("the treou", "main.treou"),
        ("tréou", "main.treou"),
        ("the tréou", "main.treou"),
        ("topsail", "main.topsail"),
        ("the topsail", "main.topsail"),
        ("bouffette", "main.bouffette"),
        ("the bouffette", "main.bouffette"),
        ("head sails", "headsails"),
    ):
        b.alias(words, target)


# ---------------------------------------------------------------------------
# Her company, her stores, her ground tackle, her boat (Tar-D §6, §11)
# ---------------------------------------------------------------------------

# The trader, ten (Tar-D decision 15, §6.1; JUDGEMENT within eight to twelve: Winfield's tartanas
# give no men, VR-Sp §9, so ten stands by the owner's word): the master (patron) and the mate
# (second), each heading a watch (ruling 11, the narrower form), six able seamen, three a watch, a
# boy (mousse), ordinary, and a cook. The coastguard, thirty-four (§6.3; JUDGEMENT, inside the
# Spanish místicos' 23 to 72, Winfield et al. 2023 pp. 1195-1201): the trader's ten for the sail
# and three a gun for Chapman's eight 4-pounders, her master (her commander) and a mate as posts.
COMPANY = {
    TRADER: {
        "complement": 10,
        "stations": {"forecastle": 3, "afterguard": 4, "idlers": 1},
        "ratings": {"able": 0.86, "ordinary": 0.14, "landsman": 0.0},
        "idlers": {"cook": 1},
        "water_tons": 3,
        "provisions_days": 30,
        "cordage_fathoms": 60,
        "shot_plugs": 2,
    },
    COASTGUARD: {
        "complement": 34,
        "stations": {"forecastle": 9, "afterguard": 9, "waisters": 11, "idlers": 3},
        "ratings": {"able": 0.55, "ordinary": 0.30, "landsman": 0.15},
        "idlers": {"cook": 1, "steward": 1, "carpenter's crew": 1},
        "water_tons": 4,
        "provisions_days": 30,
        "cordage_fathoms": 80,
        "shot_plugs": 8,
    },
}
STATION_WORDS = {
    "forecastle": "Hands per station, both watches together (Tar-D §6; JUDGEMENT): she has no "
    "tops, and her hands work aloft from the deck stations, as the cutter's. Forecastlemen, for "
    "the jib, the anchors and the great lateen's car and ourses",
    "afterguard": "Afterguard, at the lateens' sheets, the mizen and the helm",
    "waisters": "Waisters, the guns' crews beyond the sail's hands",
    "idlers": "Idlers: the trades below",
}
# Her burthen for the house's rules of tackle and hold (Tar-D §11): Forfait's 100 tonneaux taken
# as tons (JUDGEMENT: the tonneau de mer of 2,000 livres is about the long ton).
BURTHEN_TONS = float(HUMBLE["tonneaux"])
BOAT_M = 4.5  # her one boat, about 4.5 m (Tar-D §11, JUDGEMENT on its size)


def company(b, role: str) -> None:
    """Her crew section (Tar-D §6), the people drawn at muster from her wardroom file (§6.4), and
    her stores beside them (§11). Her complement checked against her posts and stations."""
    c = COMPANY[role]
    posts, drawn = g.wardroom(PEOPLE[role])
    on_stations = sum(c["stations"].values())
    if len(posts) + on_stations != c["complement"]:
        raise ValueError(
            f"tartane: her {len(posts)} posts and {on_stations} hands on station make "
            f"{len(posts) + on_stations}, not her {c['complement']}."
        )
    complement_words = {
        TRADER: "Ten (Tar-D decision 15, §6.1): the master (patron) and the mate (second), six "
        "able seamen in two watches of three, a boy and a cook. JUDGEMENT within eight to twelve: "
        "Winfield's tartanas give no men (Winfield et al. 2023 pp. 1252-1253; VR-Sp §9), the prize "
        "papers the route; ten by the owner's word on what is not found.",
        COASTGUARD: "Thirty-four (Tar-D §6.3): three a gun for Chapman's eight 4-pounders "
        "(Falconer's crew for a small gun, the bilander's rule, D31 (c)) and the trader's ten for "
        "the sail, her master (her commander) and a mate as posts. JUDGEMENT: the tartanas' "
        "entries give no men; inside the Spanish navy's místicos' 23 to 72 for one to twelve guns "
        "(Winfield et al. 2023 pp. 1195-1201; VR-Sp §11), Terrible's 31 to 48 the nearest.",
    }[role]
    entries = [
        (("complement",), c["complement"], complement_words),
        (
            ("names",),
            "spanish",
            "Her people's names from the spanish list in data/crew/names.yaml (N1), which reads "
            "her as Spain's where a scenario gives no nation (world/nations.py); a scenario names "
            "her nation and her people as it will.",
        ),
    ]
    for st, n in c["stations"].items():
        words = STATION_WORDS[st] + f": {n}."
        entries.append((("stations", st), n, words))
    entries += [
        (
            ("ratings", "able"),
            c["ratings"]["able"],
            "Share of the seamen by rating (JUDGEMENT): "
            + (
                "a coaster's able seamen and her boy ordinary (Tar-D §6.1)."
                if role == TRADER
                else "a guarda-costa's mixed company."
            )
            + f" Able: {c['ratings']['able']:.2f}.",
        ),
        (("ratings", "ordinary"), c["ratings"]["ordinary"], None),
        (("ratings", "landsman"), c["ratings"]["landsman"], None),
    ]
    entries += [
        (
            ("posts", post),
            None,
            (
                f"Station holders by post (spec M3 2.3): {' and '.join(posts)}, as "
                f"data/people/{PEOPLE[role]}.yaml gives them; names are drawn at muster."
            )
            if i == 0
            else None,
        )
        for i, post in enumerate(posts)
    ]
    for i, (trade, n) in enumerate(c["idlers"].items()):
        entries.append(
            (
                ("idlers_by_trade", trade),
                n,
                "How the idlers are made up (JUDGEMENT)." if i == 0 else None,
            )
        )
    entries += [
        (
            ("stores", "water_tons"),
            c["water_tons"],
            f"Water for a month: {c['complement']} men at a gallon a day, and some over "
            "(JUDGEMENT; Tar-D §11).",
        ),
        (
            ("stores", "provisions_days"),
            c["provisions_days"],
            "Provisions: a month, a coaster's passage and its delays (JUDGEMENT).",
        ),
        (("stores", "spare_spars"), {}, None),
        (("stores", "cordage_fathoms"), c["cordage_fathoms"], "Spare rope (JUDGEMENT)."),
        (
            ("stores", "shot_plugs"),
            c["shot_plugs"],
            g.SHOT_PLUGS_NOTE
            + (" A small trader's 2, the smack's." if role == TRADER else " The cutter's 8."),
        ),
        *g.ration_entries(
            "a coaster's articles promised the like, as the merchant brig's (judgement: no scale "
            "of the period's Mediterranean service is in the references)"
            if role == TRADER
            else "a King's coastguard victualled as the King's ships (judgement)"
        ),
    ]
    b.crew(entries)
    b.people(
        "The named people beyond the posts (package 35, spec M5 §22): the boy as the messenger; "
        f"see data/people/{PEOPLE[role]}.yaml.",
        drawn,
    )
    b.spare_spars(
        "The booms: a spare yard (Tar-D §11; JUDGEMENT after Luce 1866 ch. XVII, scaled down); "
        "see tools/ships/tartane.py.",
        [("yard", 1, "A spare topsail yard (JUDGEMENT, after Luce 1866).")],
    )
    canvas = {s["id"]: s["canvas_no"] for s in b.doc["sails"]}
    b.sail_room(
        "The sail room (spec 3b §6.3): her spare sails (Tar-D §11); see tools/ships/tartane.py.",
        [
            (
                "main.lateen",
                canvas["main.lateen"],
                "A second great lateen and jib, the sails she wears out ('shift the mainsail for "
                "a new one', Tar-D §5.4 item 5; JUDGEMENT).",
            ),
            ("jib", canvas["jib"], None),
            (
                "main.bouffette",
                canvas["main.bouffette"],
                "The bouffette and the storm jib, her storm canvas (Tar-D §11; spec 3b §6.4).",
            ),
            ("storm_jib", canvas["storm_jib"], None),
        ],
    )


def ground_tackle(b, role: str) -> None:
    """Her ground tackle by the house's rule on her burthen, beam and draught (Tar-D §11; the
    merchant brig's and the bilander's): two bowers and a kedge under 200 tons."""
    del role
    g.ground_tackle_for(b, BURTHEN_TONS, BREADTH / FT, DRAUGHT / FT)
    b.tackle_notes[("anchors", "best_bower")] += (
        " Her burthen Forfait's 100 tonneaux taken as tons (JUDGEMENT); her anchor let go by a "
        "watch too small for it calls all hands (package 116, let_go_anchor's too_few)."
    )


def hold_pumps_boat(b, role: str) -> None:
    """Her hold a trader's half of her burthen, a cruiser's tenth for the coastguard; two hand
    pumps; her one boat, about 4.5 m (Tar-D §11), by the house's rule's figures for its kind."""
    trader = role == TRADER
    g.hold_for(
        b,
        BURTHEN_TONS,
        not trader,
        "a coaster's hold, her trade: judgement, the merchant brig's share"
        if trader
        else "a coastguard's stores and prizes: judgement, a ship of war's share",
    )
    b.pumps(
        g.PUMPS_NOTE + " Two hand pumps, as the bilander's (JUDGEMENT).",
        g.pump_entries(0, 2, ["the starboard pump", "the larboard pump"]),
    )
    launch = g.LAUNCH_LENGTH_FACTOR * math.sqrt(LENGTH / FT) * g.SMALL_VESSEL_BOAT_FACTOR
    b.boats(
        g.BOATS_NOTE,
        g.boat_entries(
            LENGTH / FT,
            False,
            [
                (
                    "boat",
                    "yawl",
                    "the boat",
                    BOAT_M / FT / launch,
                    "Her one boat, about 4.5 m (Tar-D §11, decision 19; JUDGEMENT on its size), a "
                    "yawl by the house's kinds; towed astern on passage by her design, which the "
                    "boat's towed key says once the engine's step A4 is merged.",
                ),
            ],
        ),
    )


# ---------------------------------------------------------------------------
# The coastguard's guns, magazine and quarter bill (Tar-D §7; package 81's checklist)
# ---------------------------------------------------------------------------

GUN_POUNDER = 4
GUN_CWT = g.LONG_GUN_CWT[GUN_POUNDER]  # the 4-pounder of 6 ft, 12½ cwt (the house's table)
SWIVELS_X = (-6.53, -8.49)  # two a side aft (JUDGEMENT; none is drawn: Pages §5.7)
SWIVEL_COUNT = 4
SMALL_ARMS = 6
BOARDERS = 12
GUNS_NOTE = (
    "Chapman's eight 4-pounders and four swivels (Chapman 1768 Pl. LVII No. 16, the reprint's "
    "table, read there: VesselReferences-2026-10.md §3.1), a French war tartane's, until "
    "Winfield's Spanish rows replace them: the tartanas give no guns (Winfield et al. 2023 pp. "
    "1252-1253; VR-Sp §9), the místicos' 4- to 12-pounders the Spanish check (VR-Sp §11). Each in "
    "the war tartane's own port (Pages §5.7, measured), numbered from forward, its height the "
    "sill's; the 4-pounder of 6 ft, 12½ cwt, the house's (from memory), four men to the pair "
    "(Falconer's crew for a 4-pounder)."
)


def rail_at(x: float) -> float:
    return interp(RAIL_M, x)


def her_guns(profile: dict) -> list:
    """The coastguard's fit: a 4-pounder in each of the four ports a side, numbered from
    forward, its height the port's sill; four swivels on the rail aft, two a side."""
    ports = sorted(profile["ports_m"]["upper"], key=lambda t: -t[0])
    guns = []
    for i, (x, sill, _hb) in enumerate(ports, start=1):
        guns += g.broadside_pair(
            i,
            "long",
            GUN_POUNDER,
            GUN_CWT,
            x,
            sill,
            GUNS_NOTE if i == 1 else None,
            deck="upper",
            round_to=0.01,
        )
    on_the_rail = g.swivels(
        SWIVEL_COUNT,
        list(SWIVELS_X),
        0.0,
        "Four half-pounder swivels on the rail aft, two a side (Chapman's four; JUDGEMENT on "
        "their places, none drawn: Pages §5.7), a man each when a man is spare.",
        round_to=0.01,
    )
    for gun, _note in on_the_rail:
        gun["height_m"] = cm(rail_at(gun["x_m"]))
    return guns + on_the_rail


def armament(b, guns) -> None:
    magazine = g.fit_magazine(guns, {"long": g.HIRED_ROUNDS, "swivel": g.SWIVEL_ROUNDS})
    b.armament(
        "The armament (spec M7 7; package 70): one fit, Chapman's war tartane's guns, the "
        "coastguard's (Tar-D §7); every figure's source is in tools/ships/tartane.py.",
        "long guns",
        [
            (
                "long guns",
                "Chapman 1768 Pl. LVII No. 16, the reprint's table (eight 4-pounders, four "
                "swivels), read there; the ports measured on the plate (Pages §5.7)",
                guns,
                magazine,
                "The guarda-costa's fit: eight long 4-pounders and four swivels; a revenue "
                "cruiser's allowance of shot, the hired cutter's (JUDGEMENT).",
            )
        ],
    )


def at_the_guns(guns) -> int:
    """The men her fit wants at the beat: one crew to a broadside pair, a man to each swivel."""
    one_side = [gun for gun, _ in guns if gun["place"] != "broadside" or gun["side"] == g.SIDES[0]]
    return sum(gun["crew"] for gun in one_side)


def quarter_bill(b, guns) -> None:
    b.quarter_bill(
        g.QUARTER_BILL_NOTE,
        [
            (
                "forecastle",
                3,
                "The trimmers: three of the forecastlemen for the jib and the great lateen's car "
                "(JUDGEMENT).",
            ),
            ("afterguard", 3, "Three of the afterguard at the lateens' sheets (JUDGEMENT)."),
        ],
        1,
        2,
        "sail before guns",
        {
            "helm": "One man at the tiller (JUDGEMENT; she steers with a tiller, Pl. LXII's short "
            "spar over the stern).",
            "powder": "Two of the waisters to pass the cartridges (JUDGEMENT, the cutter's).",
            "priority": g.PRIORITY_NOTE,
        },
        small_arms=SMALL_ARMS,
        boarders=BOARDERS,
        small_arms_note="Six of her best shots with the stand of arms' muskets (JUDGEMENT, the "
        "cutter's); she bears no marines.",
        boarders_note="Twelve of her seamen with cutlass and pistol (JUDGEMENT: a coastguard "
        "boards a smuggler).",
        filling=g.filling_party(guns),
    )


# ---------------------------------------------------------------------------
# Her descriptions (Tar-D §8, §9), in her own files by SW-4's form
# ---------------------------------------------------------------------------

DESCRIPTION = {
    TRADER: (
        "tartane",
        "a tartane",
        "a tartane, a coaster under her great lateen, deep laden",
        "The tops make her out a tartane: one great lateen yard longer than her hull peaked high "
        "over a short mast, a small square topsail at its head and a diminutive mizen; the period "
        "named the type on sight (Falconer 1780, TARTANE: the sail 'extremely large'); judgement "
        "on the words (Tar-D §9). 'Deep laden' the merchantman's look, as the merchant brig's and "
        "the bilander's. Unarmed, her file's default; a merchant's role (Build-Ships.md §8.2). Her "
        "fisherman's description waits on a fishing-grounds file of the Gulf of Lion (the card).",
        g.UNARMED,
        ["merchant"],
    ),
    COASTGUARD: (
        "guarda-costa tartane",
        "a tartane",
        "a King's tartane, armed, a guarda-costa",
        "At four miles a tartane, as the trader; within a mile and a half the glass makes her "
        "out armed and a King's, 'a guarda-costa', the period English for a Spanish vessel of "
        "that service (James's 'garda-costa'; judgement on the words, Tar-D §9; the lead's lean, "
        "nudge 18). Her fit her file's default, Chapman's long guns; the revenue role, the revenue "
        "cutter's book read from thresholds (Tar-D §8; Build-Ships.md §8.2).",
        "long guns",
        ["revenue"],
    ),
}


# ---------------------------------------------------------------------------
# The generator's report and the hook
# ---------------------------------------------------------------------------


def centre_of_effort(rep: dict) -> tuple[float, float, float]:
    """Her plain sail's area and centre (x, z above her water), from her cuts."""
    parts = [
        (rep["cuts"]["main"]["area"], *rep["cuts"]["main"]["centre"]),
        (rep["cuts"]["mizzen"]["area"], *rep["cuts"]["mizzen"]["centre"]),
        (rep["squares"]["main.topsail"]["area"], *rep["squares"]["main.topsail"]["centre"]),
        (rep["jib"]["area"], *rep["jib"]["centre"]),
    ]
    area = sum(a for a, _, _ in parts)
    return area, sum(a * x for a, x, _ in parts) / area, sum(a * z for a, _, z in parts) / area


def lateral_centroid() -> float:
    """Her drawn lateral plane's centroid's x under H: the post, the keel and the stem."""
    pts = [(POST_X, 0.0), *[(x, z) for x, z in reversed(STERN_M) if z <= 0.0]]
    pts += [(x, z) for x, z in KEEL_M] + [(x, z) for x, z in STEM_M if z <= 0.0]
    pts = [(x, z) for x, z in pts]
    _a, cx, _cz = lateen.area_centroid(pts)
    return cx


def her_report(p: Particulars, rep: dict, role: str) -> str:
    """The generator's report: what her rules compute from her file's own keys, printed as her
    file is written and held by her tests (the lead's notes of 2026-10-29, item 2)."""
    w = FILES[role].removesuffix(".yaml")
    out = [f"{w}: {line}" for line in rep["hull"]]
    low, high = p.drawn_range_t
    _, girth_area = plank_volume(PLANK_M)
    out.append(
        f"{w}: her body drawn to H with its keel {DRAWN_MOULDED_WITH_KEEL_T:g} t moulded (Pages "
        f"§4.3, ±{DRAWN_BAND:.0%}); her wetted girth's integral {girth_area:.1f} m² a side, a "
        f"plank of {PLANK_POUCES:g} pouces adding {p.drawn_t - DRAWN_MOULDED_WITH_KEEL_T:.1f} t: "
        f"{p.drawn_t:.1f} t outside the plank, filed; {low:.1f} to {high:.1f} t on "
        f"{PLANK_RANGE_POUCES[0]:g} to {PLANK_RANGE_POUCES[1]:g} pouces."
    )
    out.append(
        f"{w}: her breadth outside the plank {BREADTH + 2.0 * PLANK_M:.2f} m against her "
        f"beam_m, Forfait's {BREADTH:.2f} moulded."
    )
    out.append(f"{w}: her drawn lateral plane's centroid x {lateral_centroid():+.2f}.")
    m = rep["masts"]
    for name, mast in m.items():
        out.append(
            f"{w}: the {name} mast at x {mast.x_deck:.2f} on the deck, raked {mast.rake_deg:+g} "
            f"degrees: heel {mast.heel_z:.2f}, hounds {mast.hounds_z:.2f}, head {mast.head_z:.2f} "
            f"m above her water ({mast.hounds_z - mast.deck_z:.2f} and "
            f"{mast.head_z - mast.deck_z:.2f} above her deck there)."
        )
    cuts = rep["cuts"]
    out.append(
        f"{w}: the great yard peaked {cuts['yard_deg']:.1f} degrees to tack its car at the stem, "
        "against Chapman's Pl. LXII 55 (another rig, recorded)."
    )
    for name in ("main", "mizzen", "bouffette"):
        c = cuts[name]
        corners = ", ".join(f"({x:.2f}, {z:.2f})" for x, z in c["corners"])
        out.append(
            f"{w}: the {name} lateen {c['area']:.1f} m², its centre ({c['centre'][0]:.2f}, "
            f"{c['centre'][1]:.2f}); tack, throat, peak, clew above her water {corners}."
        )
    for sid, sq in rep["squares"].items():
        out.append(
            f"{w}: {sid} {sq['area']:.1f} m², {sq['depth']:.2f} m deep, its yard "
            f"{sq['yard_z']:.2f} m above her water."
        )
    jib = rep["jib"]
    out.append(
        f"{w}: the jib {jib['area']:.1f} m² on a stay of {jib['stay']:.2f} m; the storm jib "
        f"{jib['storm']:.1f} m²."
    )
    out.append(f"{w}: the outrigger's end at x {outrigger_end():.2f}.")
    out += [f"{w}: {line}" for line in rep["rig"]]
    area, cx, cz = centre_of_effort(rep)
    fx = MIDDLE_X + humble("centre_before_middle")
    fz = humble("centre_height")
    out.append(
        f"{w}: her plain sail's centre ({cx:.2f}, {cz:.2f}) on {area:.1f} m², against Forfait's "
        f"({fx:.2f}, {fz:.2f}) on the Humble's whole sail with its topgallant: reported, not "
        "tuned to (Tar-D §4.5)."
    )
    out.append(f"{w}: plain sail as filed {rep['plain']} m².")
    if "bill" in rep:
        out.append(f"{w}: her guns want {rep['bill']} men at the beat, a side's pairs and swivels.")
    return "\n".join(out)


def build(out_dir: str) -> None:
    """Write her two files to `out_dir`, `tartane.yaml` and `coastguard-tartane.yaml`, through
    `write()`; the checks of Tar-D §1 raised before each is written."""
    for role, armed in ((TRADER, False), (COASTGUARD, True)):
        p = particulars(armed)
        rep = write(out_dir, p, role)
        print(her_report(p, rep, role), file=sys.stderr)
