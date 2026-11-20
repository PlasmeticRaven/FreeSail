"""The corvette *Diana*, a Danish light frigate of 1804 in the Spanish navy (package 90, the fourth
hull; her builder).

Her design is docs/design/Design-Ship-Diana.md (Dia-D), revised 2026-11-20 on her measuring and
the lead's rulings of that day (nudge 24), from her research note
docs/design/Research-Diana-2026-11.md (Dia) and the note of her measuring,
docs/design/ships-design/pages-diana.md (Pages). One module writes one file,
`data/ships/corvette-20.yaml` (Dia-D decision 1): `particulars()` gathers her figures and raises
her checks in words, `write(out_dir, p)` builds and dumps her file, and `build(out_dir)` is the
generator's hook (`tools/gen_ships.py`, `SHIP_MODULES`).

**Her sources, and the frame (Dia-D §1.3).** Her hull is the Spanish navy's own plan of her, "the
corvette of war la Diana, of 20 carronades of 30", 1809-1810 (Biblioteca Virtual de Defensa,
record 1037832, PB-021, of the Archivo Histórico de la Armada; measured on the library's larger
image, 16,868 x 5,949 px at 96.1 px a pie, outside the repository: Pages §1, §3). Its table is in
its own units, pies de Burgos and toneladas of 2,000 libras, converted once at the book's pie and
libra (Winfield et al. 2023, pp. 41-46: VesselReferences-2026-11-Spanish.md §7). Her figures in
the profile are Pages §6.2's metres as measured, in the file's frame: x forward of the middle of
her load line, between the post's after face and the stem's fore face on the arrowed line; z
above that line and square to it. The line is the arrowed line as drawn, inclined to the keel by
0.46 degrees, 0.27 m of drag (the lead's ruling 1 of 2026-11-20): her load line. The engine has
no trim, so a height above the water at its own station is what it believes. A spar's `height_m`
and a sail's `corners_m` stand above her datum, the deck at side at the middle, 1.33 m (D18 (a),
her one deck flush from end to end; the upper red line, the lead's ruling 5: JUDGEMENT); a
sail's centre above the water.

**Her rig (Dia-D §4).** No spar of hers survives. Every spar is Luce's chain, the generator's
frigate rule (Luce 1866 ch. VII), on her own particulars, her main mast (LWL + breadth) / 2 heel
to head, with her own heels and her plan's places and rakes; Falconer's yard and Chapman's and
Steel's 20-gun column the checks (Pages §7). Her sails are the frigate-36's set by the same chain:
the generator's `frigate()` is copied here with her figures in place of its constants, as the
seventy-four's module copied it (nothing is imported from another ship's module; the
duplication reported, Dia-D §1.2). Where the frigate's function carries a figure of its own hull
(a headsail's area and place, the spanker's), it is the frigate's scaled by her chain, its
length by her chain's ratio (`Particulars.scale`) and its area by its square, as her design's
probe did (Dia-D §9).

**Her notes (the lead's notes of 2026-10-29, item 2).** The file's notes carry sources,
departures and judgements. A figure a rule computes from the file's own keys (a rating, a
rope's size, a drawn displacement, a port's gap) is printed by `her_report()`, the generator's
report, and held by her tests. `HerBuilder` keeps the shared helpers' such figures out of her
notes.

The module is imported only by the generator's entry block, after `gen_ships` is made the running
script, and takes every helper as `g.<name>`. No function or table of the generator is changed;
every other file stays byte for byte as it is.

Marks: measured (off the plan's larger image, Pages), read (the page or its image), computed,
judgement, JUDGEMENT where it is a figure the file carries.
"""

from __future__ import annotations

import math
import os
import re
import sys
from dataclasses import dataclass

import gen_ships as g

from ships import period

FT = g.FT
REPORT: dict = {}

# ---------------------------------------------------------------------------
# Her units and her table (Dia §2.3; Pages §2.2; VesselReferences-2026-11-Spanish.md §7)
# ---------------------------------------------------------------------------

# The pie de Burgos, 278.635 mm, and the libra castellana, 0.4608 kg: the book's own (Winfield et
# al. 2023, pp. 41-46, read (owner's book): VR-Sp §7). A tonelada of the table is 2,000 libras,
# as its own carry proves (281 t 1,462 lb and 258 t 1,229 lb make 540 t 691 lb); the book's
# "about 1,150 kg" ton of weight is not its own 2,000 libras (921.6 kg, computed: VR-Sp §7).
PIE_M = 0.278635
LIBRA_KG = 0.4608
TONELADA_LIBRAS = 2000

# The plan's table (read on the larger image, Pages §2.2): the bodies in toneladas and libras, and
# the dimensions in pies and pulgadas.
TABLE = {
    "fore": (281, 1462),
    "aft": (258, 1229),
    "difference": (23, 233),
    "total": (540, 691),
}
ESLORA_PIES = 124.0
MANGA_PIES = 32.0 + 6.0 / 12.0
PUNTAL_PIES = 16.0

# Winfield et al. 2023, p. 930, her whole entry (read (owner's book): VR-Sp §5, §17): the book's
# metres for the table's pies, her 335 toneladas de arqueo (a capacity, not a weight) and her men.
WINFIELD = {"length_m": 34.55, "beam_m": 9.06, "depth_m": 4.46, "arqueo": 335, "men": 167}

# Her burthen by the old English measure on her gun deck and breadth, for the generator's helpers,
# whose tables are English (Dia-D §2, "Her tons"): (113.4 - 3/5 x 29.7) x 29.7 x 14.86 / 94.
BURTHEN_TONS = 449.0
GUNDECK_FT = ESLORA_PIES * PIE_M / FT

# ---------------------------------------------------------------------------
# Her hull's lines (Pages §6.2: measured on the larger image, the corrected frame, metres)
# ---------------------------------------------------------------------------

# The stations, x and the half-breadth at the line and at the rail, aft 11 to fore 11 (Pages
# §5.1, §6.2; every 4.506 pies, 1.255 m); the half-breadths as drawn (Pages §6.4).
BREADTH = [
    [-14.36, 1.55, 2.85], [-13.10, 2.22, 3.23], [-11.86, 2.83, 3.50], [-10.60, 3.34, 3.74],
    [-9.36, 3.72, 3.94], [-8.11, 3.98, 4.08], [-6.88, 4.15, 4.19], [-5.63, 4.29, 4.28],
    [-4.37, 4.39, 4.33], [-3.12, 4.45, 4.36], [-1.87, 4.49, 4.38], [-0.62, 4.51, 4.42],
    [0.63, 4.53, 4.42], [1.89, 4.53, 4.40], [3.13, 4.52, 4.38], [4.36, 4.49, 4.35],
    [5.61, 4.44, 4.30], [6.87, 4.36, 4.24], [8.12, 4.23, 4.18], [9.37, 4.06, 4.07],
    [10.62, 3.80, 3.96], [11.87, 3.45, 3.77], [13.12, 2.95, 3.56], [14.38, 2.26, 3.21],
    [15.63, 1.34, 2.59],
]  # fmt: skip

# The waterlines under her line at each station, (z, half-breadth) of WL2, WL3 and WL4 (Pages
# §5.1: the half-breadth plan's lines at the heights the sheer gives them; WL4 forward of fore 3
# joined to the rabbet by eye beyond fore 4, +-0.05 m).
WATERLINES = [
    [(-0.79, 0.75), (-1.60, 0.29), (-2.42, 0.09)],
    [(-0.79, 1.21), (-1.60, 0.49), (-2.43, 0.16)],
    [(-0.79, 1.72), (-1.60, 0.76), (-2.43, 0.25)],
    [(-0.79, 2.33), (-1.60, 1.10), (-2.43, 0.37)],
    [(-0.79, 2.86), (-1.60, 1.52), (-2.43, 0.54)],
    [(-0.79, 3.30), (-1.60, 1.97), (-2.43, 0.72)],
    [(-0.79, 3.63), (-1.60, 2.45), (-2.43, 0.93)],
    [(-0.79, 3.90), (-1.60, 2.87), (-2.43, 1.17)],
    [(-0.80, 4.08), (-1.60, 3.19), (-2.43, 1.42)],
    [(-0.80, 4.20), (-1.61, 3.42), (-2.43, 1.64)],
    [(-0.80, 4.28), (-1.61, 3.57), (-2.43, 1.82)],
    [(-0.80, 4.32), (-1.61, 3.66), (-2.43, 1.94)],
    [(-0.80, 4.34), (-1.61, 3.68), (-2.43, 1.98)],
    [(-0.80, 4.33), (-1.61, 3.66), (-2.43, 1.96)],
    [(-0.80, 4.31), (-1.61, 3.59), (-2.43, 1.84)],
    [(-0.80, 4.26), (-1.61, 3.47), (-2.43, 1.69)],
    [(-0.80, 4.18), (-1.61, 3.30), (-2.43, 1.53)],
    [(-0.80, 4.04), (-1.61, 3.05), (-2.43, 1.33)],
    [(-0.81, 3.82), (-1.61, 2.71), (-2.44, 1.12)],
    [(-0.81, 3.53), (-1.61, 2.30), (-2.44, 0.93)],
    [(-0.81, 3.15), (-1.62, 1.86), (-2.44, 0.73)],
    [(-0.81, 2.65), (-1.62, 1.43), (-2.44, 0.54)],
    [(-0.81, 2.05), (-1.62, 1.02), (-2.44, 0.36)],
    [(-0.81, 1.37), (-1.62, 0.60), (-2.44, 0.20)],
    [(-0.81, 0.64), (-1.62, 0.21), (-2.44, 0.09)],
]  # fmt: skip

# The top of her side, taffrail to stem head (Build-Ships.md §5.1): the taffrail's top, the stern's
# last point (Pages §5.5), then the bulwark rail's upper edge (Pages §5.2, §6.2; +-0.02 m). The
# bulwark rail's after end, (-18.82, 3.52), stands 0.25 m abaft her upright upper stern at its
# height, the stern's reading not closing (Pages §5.5): in her note, not a point of her side.
RAIL = [
    [-18.63, 4.03], [-18.0, 3.43], [-17.0, 3.33], [-16.0, 3.23], [-15.0, 3.13], [-14.36, 3.08],
    [-13.10, 2.99], [-11.86, 2.91], [-10.60, 2.84], [-9.36, 2.79], [-8.11, 2.75], [-6.88, 2.71],
    [-5.63, 2.68], [-4.37, 2.66], [-3.12, 2.64], [-1.87, 2.63], [-0.62, 2.62], [0.63, 2.62],
    [1.89, 2.63], [3.13, 2.64], [4.36, 2.65], [5.61, 2.68], [6.87, 2.72], [8.12, 2.76],
    [9.37, 2.81], [10.62, 2.89], [11.87, 2.97], [13.12, 3.06], [14.38, 3.19], [15.63, 3.34],
    [16.0, 3.39], [17.0, 3.54], [17.3, 3.59],
]  # fmt: skip

# The hammock rail's top (Pages §5.2, §6.2): no key in the profile; in her note (Dia-D §3.2).
HAMMOCK_RAIL = [
    [-18.84, 3.99], [-17.0, 3.88], [-15.0, 3.69], [-12.0, 3.47], [-8.0, 3.30], [-4.0, 3.20],
    [0.0, 3.17], [4.0, 3.20], [8.0, 3.30], [12.0, 3.52], [14.0, 3.68], [16.0, 3.91], [17.3, 4.10],
]  # fmt: skip

# Her deck at side, the upper red line (the lead's ruling 5: JUDGEMENT, Pages §5.2), traced; its
# first three points the research note's, re-referenced to the line (computed).
DECK = [
    [-16.78, 1.84], [-15.31, 1.69], [-12.87, 1.59], [-12.0, 1.53], [-10.0, 1.47], [-8.0, 1.42],
    [-6.0, 1.38], [-4.0, 1.35], [-2.0, 1.33], [0.0, 1.33], [2.0, 1.35], [4.0, 1.37], [6.0, 1.41],
    [8.0, 1.46], [10.0, 1.52], [12.0, 1.60], [14.0, 1.70], [15.0, 1.76], [16.0, 1.85],
    [17.0, 1.93],
]  # fmt: skip

# Her eleven ports a side, aft to forward, [x of the port's centre, sill, half-breadth at the
# sill] (Pages §5.7: the sheet's own centres; the sills +-0.01 m, the half-breadths +-0.03 m
# read on the body plan, +-0.05 at ports 1 and 10; the bow port's half-breadth JUDGEMENT,
# +-0.2 m). Numbered here as Pages numbers them, port 1 aftmost and port 11 the bow port.
PORTS = [
    [-13.49, 2.11, 3.19], [-10.69, 1.93, 3.77], [-7.81, 1.82, 4.14], [-4.93, 1.75, 4.34],
    [-2.06, 1.72, 4.42], [0.80, 1.72, 4.46], [3.65, 1.75, 4.42], [6.42, 1.82, 4.33],
    [9.37, 1.91, 4.14], [12.27, 2.06, 3.74], [15.96, 2.38, 2.1],
]  # fmt: skip
BOW_PORT = 11
PORT_SIZE = [0.83, 0.66]  # measured: 286.5 by 229 px, the median of the clean ports
MIDSHIP_PORT = 6  # her lee port (Dia-D §10): 1.72 m over 4.46 m

# Two places over the rail by the mizen for the 1817 fit's after obuses (Dia-D §5.1, §5.2 item 2:
# JUDGEMENT), between ports 1 and 2, a sill 2 in under the rail (as the 74's `OVER_THE_RAIL_M`).
OVER_THE_RAIL_X = -12.09
OVER_THE_RAIL_M = 0.05

# K, the false keel's lower edge (Pages §4.1, §4.2: a false keel by judgement), from the post's
# heel to the knee's foot: the line her draught and her lateral plane are counted to (D29 (b)).
# The keel's lower edge, 0.15 m above it, runs from (-16.54, -3.75) to the forefoot (13.84, -3.51).
K = [[-16.54, -3.91], [14.65, -3.66]]
KEEL_LOWER_EDGE = [[-16.54, -3.75], [13.84, -3.51]]
# The rabbet line (a ruled line on the sheet, straight: Pages §3.3, §4.1) and the rabbet's
# half-siding, 0.33 pie, the body plan's keel section (Pages §4.3 item 3).
RABBET = [[-16.55, -3.40], [13.45, -3.15]]
RABBET_HALF_SIDING_M = 0.33 * PIE_M

# The stem's fore face from the forefoot to the stem head (Pages §5.4, traced).
STEM = [
    [13.84, -3.51], [14.80, -3.25], [15.25, -3.00], [15.56, -2.75], [15.83, -2.50],
    [16.06, -2.25], [16.26, -2.00], [16.59, -1.50], [16.86, -1.00], [17.07, -0.50],
    [17.23, 0.00], [17.37, 0.50], [17.47, 1.00], [17.54, 1.50], [17.60, 2.00], [17.64, 2.50],
    [17.67, 3.00], [17.69, 3.50], [17.69, 4.00], [17.31, 5.09],
]  # fmt: skip
# The stem head, by eye +-0.05 m at (17.30, 5.09) (Pages §5.4), is filed a centimetre forward of
# the rail's end at x 17.30, within its reading, so that the drawn top of the side ends on the
# rail and rises there to the head (judgement; `freesail/ship/form.py` draws the side's top to the
# stem head beyond the rail's last point, and the two at one x would give the rail's end two tops).
STEM_HEAD = STEM[-1]

# The knee of the head's fore edge, from K to its scroll (Pages §5.4, §6.2).
HEAD = [
    [14.65, -3.66], [15.56, -3.25], [15.88, -3.00], [16.12, -2.75], [16.32, -2.50],
    [16.48, -2.25], [16.64, -2.00], [16.92, -1.50], [17.16, -1.00], [17.37, -0.50],
    [17.60, 0.00], [17.83, 0.50], [18.10, 1.00], [18.45, 1.50], [18.93, 2.00], [19.62, 2.50],
    [20.33, 3.00], [20.51, 3.15], [20.65, 3.49], [20.52, 3.64],
]  # fmt: skip

# The post's heel at K, the post's after face, the counter's tuck, the knuckle, the upright upper
# stern and the taffrail's top (Pages §5.5: measured; what each line is, JUDGEMENT).
STERN = [
    [-16.54, -3.91], [-16.54, -3.40], [-17.23, 0.00], [-17.78, 2.65], [-18.57, 3.20],
    [-18.57, 3.60], [-18.63, 4.03],
]  # fmt: skip
KNUCKLE_Z = 3.20
# The transom's half-breadth at the taffrail and at the knuckle: the body plan's aftermost upright
# line, 7.0 and 7.13 pies (Pages §5.5; JUDGEMENT, the stern's reading not closing).
TRANSOM_HB = [1.95, 1.99]
# Her stern lights: none filed (JUDGEMENT; the lead's ruling of nudge 32). None is drawn on her plan
# (Dia-D §3.1), and a band over her knuckle would stand partly above her bulwark rail with no
# cabin under a quarterdeck behind it, she being flush-decked; the flush-decked brig files none.
# Until the owner's sheets show them. (Old, her first five commits: a judged band of four,
# [3.25, 3.85, 4, 1.50], by Steel 1805 p. 240's "the great cabin windows only".)

# The main wale, [x, lower edge, upper edge] (Pages §5.3, traced).
WALES = [
    [-16.0, 0.66, 1.38], [-15.0, 0.51, 1.31], [-14.0, 0.40, 1.22], [-13.0, 0.33, 1.14],
    [-12.0, 0.26, 1.08], [-11.0, 0.20, 1.03], [-10.0, 0.15, 1.01], [-9.0, 0.11, 0.97],
    [-8.0, 0.08, 0.94], [-7.0, 0.06, 0.92], [-6.0, 0.04, 0.90], [-5.0, 0.02, 0.88],
    [-4.0, 0.02, 0.88], [-3.0, 0.01, 0.87], [-2.0, 0.01, 0.86], [-1.0, 0.01, 0.87],
    [0.0, 0.02, 0.88], [1.0, 0.03, 0.88], [2.0, 0.03, 0.89], [3.0, 0.04, 0.90], [4.0, 0.06, 0.91],
    [5.0, 0.09, 0.94], [6.0, 0.11, 0.96], [7.0, 0.14, 0.99], [8.0, 0.18, 1.03], [9.0, 0.23, 1.08],
    [10.0, 0.28, 1.13], [11.0, 0.35, 1.20], [12.0, 0.43, 1.27], [13.0, 0.51, 1.36],
    [14.0, 0.61, 1.47], [15.0, 0.74, 1.59], [16.0, 0.89, 1.74], [17.0, 1.06, 1.90],
]  # fmt: skip

# The midship station "m" as drawn, (z, half-breadth), from the rabbet to the rail (Pages §6.2);
# its area to the line 20.16 m2, Cm 0.68 (computed).
SECTION = [
    [-3.26, 0.09], [-3.19, 0.25], [-3.12, 0.41], [-2.98, 0.73], [-2.85, 1.04], [-2.71, 1.36],
    [-2.43, 1.97], [-2.15, 2.64], [-1.87, 3.21], [-1.59, 3.70], [-1.31, 3.99], [-1.03, 4.22],
    [-0.76, 4.33], [-0.48, 4.43], [-0.20, 4.49], [0.00, 4.53], [0.50, 4.51], [0.92, 4.50],
    [1.47, 4.47], [2.03, 4.44], [2.62, 4.42],
]  # fmt: skip

# ---------------------------------------------------------------------------
# Her hull block (Dia-D §2, the rulings of 2026-11-20)
# ---------------------------------------------------------------------------

LWL_M = 34.47  # the post's after face to the stem's fore face on the line (Pages §4.1)
BEAM_M = WINFIELD["beam_m"]
DRAUGHT_M = 3.78  # the mean to K (ruling 1; the lead's note of 09:40, item (1))
DRAUGHT_AFT_M, DRAUGHT_FORE_M = 3.91, 3.65
DATUM_M = 1.33  # the deck at side at the middle (ruling 5)
LATERAL_AREA_M2 = 122.2  # the post's after face, K, the knee's fore edge, no rudder (ruling 4)
GM_M = 1.75  # JUDGEMENT (Dia-D decision 4), tuned: the design's 1.5 (docs/dev/TuningNotes.md)
CLR_X_M = 2.8  # tuned for her helm: 2.5 to start (docs/dev/TuningNotes.md)
HULL_SPEED_KN = 11.8
RUDDER = {"area_m2": 3.0, "max_angle_deg": 35, "rate_deg_s": 3.0, "span_m": 3.9}

# The drawn displacement to her line (Pages §4.3, §4.5, computed), tonnes: moulded; with the keel,
# post, stem and gripe; and outside 3 and 4 pulgadas of plank (JUDGEMENT). Her file's mass is the
# body as drawn outside the plank at the line as drawn, one figure of that range (the lead's
# ruling of 2026-11-20, nudge 30): the middle, at 3.5 pulgadas (JUDGEMENT), 469.6 t, filed to the
# tonne; the table's 498.0 t beside it in her note.
DRAWN_T = {"moulded": 435.6, "with the keel": 441.7, "3 pulgadas": 465.6, "4 pulgadas": 473.6}
PLANK_PULGADAS = 3.5

# ---------------------------------------------------------------------------
# Her masts (Dia-D §4.1; Pages §6.2, re-referenced, computed)
# ---------------------------------------------------------------------------

# Each lower mast: its x at the deck and the deck's z there, its heel's z, and its rake in the
# line's frame (the plan's places and rakes, rung A; each rake 0.5 deg more aft than on the sheet,
# the line sloping 0.53 deg on the image).
MASTS = {
    "fore": {"x": 12.50, "deck": 1.62, "heel": -1.66, "rake": 0.5},
    "main": {"x": -2.29, "deck": 1.36, "heel": -2.18, "rake": 5.5},
    "mizzen": {"x": -11.38, "deck": 1.48, "heel": -1.87, "rake": 6.0},
}
BOWSPRIT_STEEVE_DEG = 21.5  # to the line (the plan's 21 deg, +0.5 in the line's frame)

# The frigate-36's main mast by the same chain, (137 + 38.33) / 2 ft (`gen_ships.frigate`), which
# her chain is set against: her spars are the frigate's times `Particulars.scale`, her sails' areas
# its square.
FRIGATE_MAIN_LEN_FT = (round(0.957 * 143.2) + 38.33) / 2.0
FRIGATE_DECK_M = g.FRIGATE_DECK_M
FRIGATE_PLAIN_SAIL_M2 = 1584.0  # the frigate-36's plain sail, against which her rope is scaled

# The frigate's figures of its own hull, scaled to hers (`frigate()`; Dia-D §9's probe): the
# spanker (167 m2 with its centre 9.8 m above the frigate's water, 5.0 m abaft its mizen), and
# the three headsails, (id, stay, m2, x forward of its bowsprit's root at x 21.0, centre above its
# water, the spar its tack is on and that spar's end above the frigate's datum, `height_m`): each
# headsail's centre stands 2.2, 2.2 and 3.2 m above its tack's spar end in the frigate, and hers
# that height scaled above her own spar's end, on her plan's steeve (the lead's reader of her
# first hash: the frigate's heights above its deck had put her centres at or below her tacks).
FRIGATE_SPANKER = (167.0, 9.8, 5.0)
FRIGATE_BOWSPRIT_X = 21.0
FRIGATE_HEADS = [
    ("fore.topmast_staysail", "fore.topmast.stay", 75.0, 24.0, 10.0, "bowsprit", 6.0),
    ("jib", "jib.stay", 130.0, 31.0, 12.0, "jib_boom", 8.0),
    ("flying_jib", "flying_jib.stay", 70.0, 37.0, 14.0, "flying_jib_boom", 9.0),
]
# The spanker's boom over her taffrail: its height above her datum, the frigate's 2.4 m raised
# to clear her taffrail's top (4.03 m above her water) by 0.2 m (JUDGEMENT).
BOOM_HEIGHT_M = 2.9


# ---------------------------------------------------------------------------
# Her particulars, and the checks of Dia-D §1.3
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Particulars:
    """Her figures in the file's frame, metres, converted once: the hull block and its notes, the
    profile's lines, and each lower mast's place, deck, heel and rake; the table's figures in its
    own units beside the metres they give."""

    hull: dict
    hull_notes: dict
    length_m: float
    beam_m: float
    depth_m: float
    displacement_kg: float
    table_kg: float
    main_len_ft: float
    scale: float
    masts: dict


def libras(toneladas, lb):
    """A table's figure in libras: its toneladas at 2,000 and its libras."""
    return toneladas * TONELADA_LIBRAS + lb


def check_table():
    """The table's arithmetic (Dia-D §1.3): the two bodies sum to the total, and their
    difference is the table's."""
    fore, aft = libras(*TABLE["fore"]), libras(*TABLE["aft"])
    if fore + aft != libras(*TABLE["total"]):
        raise ValueError(
            f"her table's bodies, {fore} and {aft} libras, do not sum to its total, "
            f"{libras(*TABLE['total'])}."
        )
    if fore - aft != libras(*TABLE["difference"]):
        raise ValueError(
            f"her table's bodies differ by {fore - aft} libras, not by its difference, "
            f"{libras(*TABLE['difference'])}."
        )


def check_winfield():
    """Winfield's metres within 0.01 m of the table's pies at the book's pie (Dia-D §1.3)."""
    for what, pies, metres in (
        ("length", ESLORA_PIES, WINFIELD["length_m"]),
        ("breadth", MANGA_PIES, WINFIELD["beam_m"]),
        ("depth", PUNTAL_PIES, WINFIELD["depth_m"]),
    ):
        if abs(pies * PIE_M - metres) > 0.01:
            raise ValueError(
                f"her {what} of {pies:g} pies is {pies * PIE_M:.3f} m at the book's pie, not "
                f"within 0.01 m of Winfield's {metres:g}."
            )


def check_masts():
    """Every mast's heel below the deck at the mast and above K under it (Dia-D §1.3)."""
    for name, m in MASTS.items():
        k = interp(K, m["x"])
        if not k < m["heel"] < m["deck"]:
            raise ValueError(
                f"her {name} mast's heel stands at z {m['heel']:g} m, not between K under it "
                f"({k:.2f}) and the deck at side over it ({m['deck']:g})."
            )


def check_ports():
    """Her midship lee port at 21.1 deg (the lead's ruling 6), and every port's sill between the
    deck and the rail at its x."""
    x, sill, hb = PORTS[MIDSHIP_PORT - 1]
    angle = math.degrees(math.atan2(sill, hb))
    if abs(angle - 21.1) > 0.05:
        raise ValueError(f"her midship lee port dips at {angle:.2f} deg, not 21.1.")
    for i, (x, sill, _hb) in enumerate(PORTS, start=1):
        if not interp(DECK, x) < sill < interp(RAIL, x):
            raise ValueError(f"her port {i}'s sill, {sill:g} m at x {x:g}, is not on her side.")


def interp(points, x):
    """Straight between the points (x, z), held at the ends."""
    pts = sorted(points)
    if x <= pts[0][0]:
        return pts[0][1]
    for (x0, z0), (x1, z1) in zip(pts, pts[1:], strict=False):
        if x <= x1:
            return z0 + (z1 - z0) * (x - x0) / (x1 - x0)
    return pts[-1][1]


def particulars():
    """Her figures in the file's frame, and the checks of Dia-D §1.3 raised in words (never an
    `assert`, which `python -O` strips) before the file is written."""
    check_table()
    check_winfield()
    check_masts()
    check_ports()
    table_kg = round(libras(*TABLE["total"]) * LIBRA_KG, -3)
    lo, hi = DRAWN_T["3 pulgadas"], DRAWN_T["4 pulgadas"]
    displacement = round((lo + (hi - lo) * (PLANK_PULGADAS - 3.0)) * 1000.0, -3)
    lwl_ft, beam_ft = LWL_M / FT, BEAM_M / FT
    main_len = (lwl_ft + beam_ft) / 2.0
    hull, notes = hull_block(displacement)
    return Particulars(
        hull=hull,
        hull_notes=notes,
        length_m=ESLORA_PIES * PIE_M,
        beam_m=MANGA_PIES * PIE_M,
        depth_m=PUNTAL_PIES * PIE_M,
        displacement_kg=displacement,
        table_kg=table_kg,
        main_len_ft=main_len,
        scale=main_len / FRIGATE_MAIN_LEN_FT,
        masts=MASTS,
    )


def hull_block(displacement):
    """Her hull dict in the house's key order, and its notes (Dia-D §2); `profile_into` adds the
    profile as its last key."""
    hull = {
        "length_waterline_m": LWL_M,
        "beam_m": BEAM_M,
        "draught_m": DRAUGHT_M,
        "displacement_kg": displacement,
        "gm_m": GM_M,
        "clr_x_m": CLR_X_M,
        "lateral_area_m2": LATERAL_AREA_M2,
        "hull_speed_kn": HULL_SPEED_KN,
        "deck_height_m": DATUM_M,
        "rudder": dict(RUDDER),
    }
    return hull, dict(HULL_NOTES)


HULL_NOTES = {
    "length_waterline_m": "The post's after face to the stem's fore face on her line, 11,886.8 px "
    "at 96.1 a pie on the plan's larger image (measured, Pages §4.1): 124 pies x 0.99. The table's "
    "eslora of 124 pies is 34.55 m at the book's pie (Winfield et al. 2023, pp. 41-46 and p. 930), "
    "the gun deck from post to stem (Dia §2.2-§2.3); 34.83 m to the knee's fore edge (computed); "
    "between the rabbets about 33.6 m, not re-measured (Dia-D §17.2 item 8).",
    "beam_m": "Winfield's metres for the table's manga of 32 pies 6 pulgadas, extreme (Winfield et "
    "al. 2023, p. 930); the body plan's frame 32.47 pies (measured, Pages §3.1), its sections 4.53 "
    "m a side at the line amidships (Pages §5.1).",
    "draught_m": "Her load line is the plan's arrowed line as drawn (the lead's ruling 1 of "
    "2026-11-20), inclined to the keel by 0.46 deg, 0.27 m of drag (measured, Pages §4.1-§4.2). "
    "The mean to K, the false keel's lower edge (a false keel by judgement, Pages §4.1), as the "
    "hulls drawn from their draughts file theirs (D29 (b); the lead's note of 2026-11-20, 09:40): "
    "3.91 m at the post's after face and 3.65 m at the stem's fore face. To the keel's lower edge "
    "3.63 m (3.76, 3.49). The engine has no trim: she floats level at the mean.",
    "displacement_kg": "Her body as drawn, outside the plank, at her line as drawn (the lead's "
    "ruling of 2026-11-20, nudge 30, for every hull drawn from her plan): every other figure of "
    "her file, her draught, her breadth at the water, her lateral area, is reckoned to that line. "
    "Drawn to it (measured, computed, Pages §4.3): 435.6 t moulded, 441.7 t with the keel, post, "
    "stem and gripe, 465.6 to 473.6 t outside a plank of 3 to 4 pulgadas, the plank JUDGEMENT, no "
    "source found (Pages §4.5); the middle of that range taken, at 3.5 pulgadas (JUDGEMENT). "
    "Beside it, the plan's table: 540 toneladas 691 libras at 2,000 libras the tonelada and the "
    "book's libra of 0.4608 kg (Winfield et al. 2023, pp. 41-46), 498.0 t (computed), most likely "
    "reckoned on a level line at her after draught (499 t, its bodies 1.10 to 1 against the "
    "table's 1.089: the lead's ruling 3, JUDGEMENT), not at the line she is drawn floating at; "
    "filed until nudge 30.",
    "gm_m": "JUDGEMENT: her captain's 'stiff' (Meyer's report, Roos 1957 p. 94: Dia §6), set so "
    "that under plain sail in 22 knots she heels no more than 1.15 times the frigate-36 (Dia-D "
    "§9, decision 4; truth C), the frigate's 1.3 m scaled by her breadth heeling her half again "
    "as much; tuned from the design's 1.5, measured old beside new in docs/dev/TuningNotes.md, "
    "'Package 90, the Diana', and held by her tests.",
    "clr_x_m": "Tuned for her captain's 'steers splendidly' (Meyer, Roos 1957 p. 94) by her helm's "
    "truth (Dia-D §14, truth D), from the frigate's lead scaled by her length (Dia-D §2), so that "
    "she carries weather helm within the truth's band, near the frigate-36's, and lies to without "
    "falling aback; measured old beside new in docs/dev/TuningNotes.md, 'Package 90, the Diana', "
    "and held by her tests. Her going about is not tuned by it: more weather helm takes her round "
    "sooner, and further forward she misses stays.",
    "lateral_area_m2": "Measured by the method of the hulls drawn from their draughts (the lead's "
    "ruling 4 of 2026-11-20; D29 (b)): the post's after face, K and the knee's fore edge, the "
    "rudder left out (Pages §5.6), as the 64's, the razee's, the 74's and the Neufchatel's. Beside "
    "it: 120.0 m2 to the keel's lower edge and the stem's fore face, 125.2 m2 with the rudder, "
    "and 104.4 m2 by the generator's 0.85 rule on her first particulars.",
    "hull_speed_kn": "The frigate-36's 13.0 by the root of her length over the frigate's, "
    "sqrt(34.47 / 41.8): 11.8 (computed); Meyer's 10 to 11 knots with the wind two or three "
    "points abaft the beam in a fresh breeze (Roos 1957 p. 94) the check (truth B).",
    "deck_height_m": "Her deck at side at the middle, the upper of the plan's three red lines "
    "(measured, Pages §5.2): the lead's ruling 5 leaves which is hers to her design, which takes "
    "the upper by her guns' sills, 0.38 to 0.50 m above it at ports 1 to 10, the nearest of the "
    "three to a carronade's port (Steel 1805 Folios XLII and XLVI: pages-steel-1805-bodies.md §4; "
    "JUDGEMENT). Her one deck, flush from end to end: the datum of every spar height and every "
    "sail's corners (D18 (a)).",
    "rudder": "The plan's blade under the line, 3.0 m2 (measured, Pages §5.5), its span from the "
    "line to its heel on K, (-17.47, -3.90); 35 degrees and 3 deg/s the frigate-36's (judgement).",
}

# Each line's rung (Build-Ships.md §5.0 principles 3 and 4): her own plan for every line (Dia-D
# §3.4), the judgements in it named in each line's note; no stern lights filed (nudge 32).
MARKS = {
    "rail_m": "sourced",
    "breadth_m": "sourced",
    "keel_m": "sourced",
    "stem_m": "sourced",
    "stern_m": "sourced",
    "wales_m": "sourced",
    "section_m": "sourced",
    "decks_m": "sourced",
    "ports_m": "sourced",
    "port_size_m": "sourced",
    "head_m": "sourced",
    "sections_m": "judged",  # the water at each port's station, carried between two stations
    "rabbet_m": "sourced",
    "form.fullness": "judged",  # the default rule beyond the end stations sections_m carries
    "form.stern": "sourced",
    "form.stern.knuckle_z_m": "sourced",
    "form.stern.transom_hb_m": "sourced",
    "form.head": "sourced",
}

PROFILE_NOTES = {
    "profile": "Her side, deck and ports (Dia-D §3; Build-Ships.md §5.1): x forward of the middle "
    "of her line, z above it and square to it, metres; every point measured on her own plan "
    "(BVD 1037832, PB-021, the larger image at 96.1 px a pie: Pages §6.2), the corrected frame "
    "taking out the sheet's bow and the level datum the first reading took (Pages §3.3, §4.1, §8).",
    "profile.rail_m": "The top of her side from the taffrail's top, the stern's last point, then "
    "the bulwark rail's upper edge to the stem head, traced (Pages §5.2, §5.5). The solid side is "
    "the rail (JUDGEMENT); the bulwark rail's after end, (-18.82, 3.52), stands abaft her upright "
    "upper stern at its height, the stern's reading not closing, and is not a point of it; the "
    "hammock rail above it, 3.17 m at the middle to 3.99 m at the stern and 4.10 m at the bow, has "
    "no key.",
    "profile.breadth_m": "The half-breadths at the line and at the rail at the plan's 25 stations, "
    "aft 11 to fore 11 every 4.506 pies (measured, Pages §5.1): the half-breadth plan's at the "
    "line, the body plan's sections at the rail's height. As drawn; whether moulded or outside "
    "the plank is JUDGEMENT (Pages §6.4).",
    "profile.keel_m": "K, the false keel's lower edge, from the post's heel to the knee's foot "
    "(measured, Pages §4.1, §4.2; a false keel by judgement, as ZAZ4491's K): the line her "
    "draught and her lateral area are counted to (D29 (b)). The keel's lower edge, 0.15 m above "
    "it, runs from (-16.54, -3.75) to the forefoot at (13.84, -3.51). Both slope in the frame, "
    "she being drawn trimmed by the stern.",
    "profile.stem_m": "The stem's fore face from the forefoot, where the keel's lower edge leaves "
    "its line, to the stem head, a post with a rounded head over the rail (traced, Pages §5.4); "
    "the head read by eye at (17.30, 5.09), +-0.05 m, filed a centimetre forward of the rail's "
    "end, where the drawn side ends on the rail and rises to it (judgement within the reading).",
    "profile.stern_m": "The post's heel at K, the post's after face raked 10.5 deg to the line's "
    "square, the counter's tuck, the knuckle where a sloping counter meets an upright upper "
    "stern, that stern's top and the taffrail's (measured, Pages §5.5); what each line is, "
    "JUDGEMENT, the stern's reading the weakest of the measuring.",
    "profile.wales_m": "The main wale, a band of three strakes, both edges traced the whole length "
    "(Pages §5.3); its lower edge on the line amidships within 2 cm. From x -16 aft the band "
    "follows the side's after edge.",
    "profile.section_m": "The midship station 'm' as drawn on the body plan, from the rabbet to "
    "the rail (measured, Pages §6.2); whether over the plank, JUDGEMENT (Pages §6.4).",
    "profile.decks_m.upper": "Her deck at side, the upper of the three red lines (the lead's "
    "ruling 5: JUDGEMENT, by her guns' sills, Pages §5.2), traced forward of x -12; its three "
    "points abaft that the research note's, re-referenced to the line (computed), the stern's "
    "inboard works crowding it there.",
    "profile.ports_m.upper": "Her eleven ports a side, the sheet's own centres, each sill and the "
    "half-breadth at it read on the body plan between the stations either side (measured, Pages "
    "§5.7): ports 1 (aftmost) to 10 her broadside's, 11 the bow port, whose half-breadth is "
    "JUDGEMENT (+-0.2 m); and a place over the rail between ports 1 and 2, a sill 2 in under the "
    "rail, for the 1817 fit's after obuses (Dia-D §5.2 item 2: JUDGEMENT on the place).",
    "profile.port_size_m.upper": "0.83 by 0.66 m, 286.5 by 229 px, the median of the clean ports "
    "(measured, Pages §5.7): the plan's ports alike.",
    "profile.head_m": "The knee of the head's fore edge from K to its scroll, its foot, fore side "
    "and top, over the body plan's frame (measured, Pages §5.4): two head rails and the cheeks "
    "run from the bow to it, bobstay holes along the knee, no figure (read).",
    "profile.sections_m": "The half-breadth plan's waterlines WL2, WL3 and WL4 at every station, "
    "at the heights the sheer gives them (measured, Pages §5.1; the sheet's two directions agree "
    "within 0.2 pie at the midship station, Pages §3.2); WL4 forward of fore 3 joined to the "
    "rabbet by eye beyond fore 4 (+-0.05 m). And at each of ports 1 to 10 the body plan's "
    "half-breadth at the sill (measured, Pages §5.7), over the line's half-breadth there carried "
    "straight between the stations either side (judgement): the side held out at the sills toward "
    "her ends, where the default rule's flare drew it up to 0.41 m inside them.",
    "profile.rabbet_m": "The rabbet line, ruled straight on the sheet (Pages §3.3, §4.1), with the "
    "rabbet's half-siding of 0.33 pie from the body plan's keel section (measured, Pages §4.3); "
    "then up the stem's rabbet, read in Pages §5.4, not filed.",
    "profile.form": "Her stern square on the body plan's aftermost upright line, its knuckle the "
    "sheer's (Pages §5.5: JUDGEMENT, the reading not closing), with no round-up read, no quarter "
    "gallery and no stern lights filed: none is drawn on her plan, and a band over her knuckle "
    "would stand partly above her bulwark rail, she being flush-decked, as the brig files none "
    "(JUDGEMENT, until the owner's sheets show them); her head a scroll on the knee, no figure "
    "(read: the lead's ruling 6). The ends beyond the end stations by the default rule.",
}


def profile_into(p):
    """Her profile and shape keys added to `p.hull` through `g.hull_profile` and `g.hull_form`,
    their notes to `p.hull_notes`; ports 1 to 10's triples measured at their sills (Pages §5.7),
    so a gap over 0.05 m to the drawn side raises for them, and the bow port's and the place
    over the rail are reported."""
    ports = [list(t) for t in PORTS]
    rail_z = interp(RAIL, OVER_THE_RAIL_X)
    rail_hb = interp([(x, hr) for x, _hw, hr in BREADTH], OVER_THE_RAIL_X)
    ports.append([OVER_THE_RAIL_X, round(rail_z - OVER_THE_RAIL_M, 2), round(rail_hb, 2)])
    ports.sort()
    sections = [
        [x, z, hb]
        for (x, _hw, _hr), wls in zip(BREADTH, WATERLINES, strict=True)
        for z, hb in sorted(wls)
    ]
    # each measured port's sill read on the body plan (Pages §5.7), its station's water the
    # half-breadth plan's line carried straight between the stations either side (judgement)
    water = [(x, hw) for x, hw, _hr in BREADTH]
    for x, sill, hb in PORTS[: BOW_PORT - 1]:
        sections += [[x, 0.0, round(interp(water, x), 2)], [x, sill, hb]]
    sections.sort()
    p.hull["profile"] = g.hull_profile(
        RAIL,
        BREADTH,
        keel=K,
        stem=STEM,
        stern=STERN,
        wales=WALES,
        section=SECTION,
        decks={"upper": DECK},
        ports={"upper": ports},
        port_size={"upper": PORT_SIZE},
        head=HEAD,
        sections=sections,
        rabbet=[[x, z, RABBET_HALF_SIDING_M] for x, z in RABBET],
    )
    form = {
        "fullness": [1.0, 1.0],
        "stern": {
            "type": "square",
            "knuckle_z_m": KNUCKLE_Z,
            "transom_hb_m": list(TRANSOM_HB),
        },
        "head": "scroll",
    }
    measured = tuple(("upper", x) for x, _s, _h in PORTS[: BOW_PORT - 1])
    drawn = REPORT.setdefault("hull", [])
    drawn.clear()
    REPORT["gaps"] = g.hull_form(p.hull, form=form, marks=MARKS, measured=measured, report=drawn)
    p.hull_notes.update(PROFILE_NOTES)
    return p.hull["profile"]


# ---------------------------------------------------------------------------
# Her Builder: the shared helpers' computed figures kept out of her notes
# ---------------------------------------------------------------------------


class HerBuilder(g.Builder):
    """The generator's Builder, with the figures its shared helpers compute from her own keys
    kept out of her notes (the lead's notes of 2026-10-29, item 2): a spar's rating, a bowline's
    size and a staysail's sheet's, a staysail's area and sides. What each rule is and what it read
    stays. The other files keep their notes as they are."""

    RATED = re.compile(r" -> [0-9.]+ kN")
    BOWLINE = re.compile(r"(lighter rope than the sheet), [0-9.]+ in \(judgement\)")
    SHEET = re.compile(r"^[0-9.]+ in, to bear its sail")
    CUT = re.compile(
        r"^(.*? staysail) [0-9.]+ m2, (four-sided|triangular|a triangle), square on the foot "
        r"\(Steel 1794 vol\. I, Sail-making\): leech [0-9.]+ m,"
        r"(?: bunt [0-9.]+ m \([0-9.]+ of the leech\),)? foot [0-9.]+ m(?: \([0-9]+ cloths\))?; "
    )

    def _plain_of_figures(self, note):
        note = self.RATED.sub("", note)
        note = self.BOWLINE.sub(r"\1 (judgement)", note)
        note = self.SHEET.sub("to bear its sail", note)
        return self.CUT.sub(r"\1, \2, square on the foot (Steel 1794 vol. I, Sail-making): ", note)

    def rate_spars(self):
        """`Builder.rate_spars`, its figures left in the file's `rating_kn` alone."""
        super().rate_spars()
        self.notes = {key: self._plain_of_figures(note) for key, note in self.notes.items()}


# ---------------------------------------------------------------------------
# Her rig (Dia-D §4): Luce's chain on her particulars, the frigate's function copied
# ---------------------------------------------------------------------------

MAST_RATIO = {"fore": 0.9, "main": 1.0, "mizzen": 13.0 / 15.0}
YARD_RATIO = {"fore": 0.9, "main": 1.0, "mizzen": 5.0 / 7.0}
TOPMAST_RATIO = {"fore": 0.9, "main": 1.0, "mizzen": 5.0 / 7.0}
LEVELS = ("course", "topsail", "topgallant", "royal")
YARD_LENGTHS = {"course": "yard", "topsail": "topsail_yard", "topgallant": "tg_yard"}
YARD_LENGTHS["royal"] = "royal_yard"
YARD_HEIGHTS = {"course": "yard_h", "topsail": "topsail_h", "topgallant": "tg_h"}
YARD_HEIGHTS["royal"] = "royal_h"
LEVEL_OF_SPAR = {"course": "lower", "topsail": "topsail", "topgallant": "topgallant"}
LEVEL_OF_SPAR["royal"] = "royal"
# Her brace limits, the frigate-36's level for level (Fincham 1843 art. 102, the long ships'
# upper values; two degrees a level aloft): no source gives hers (Dia-D §4.1).
BRACE_PLANS = {
    "fore": [("course", 62), ("topsail", 64), ("topgallant", 66), ("royal", 68)],
    "main": [("course", 64), ("topsail", 66), ("topgallant", 68), ("royal", 70)],
    "mizzen": [("topsail", 62), ("topgallant", 64), ("royal", 66)],
}
CROSSJACK_BRACE_DEG = 60
REEFS = {"course": 1, "topsail": 3, "topgallant": 0, "royal": 0}
HEAD_OF_YARD = {"course": 0.9, "topsail": 0.82, "topgallant": 0.89, "royal": 0.89}
COURSE_DROP_OF_YARD = 0.42
SHROUDS = {"fore": (9.5, 9), "main": (9.5, 9), "mizzen": (6.5, 6)}
BACKSTAY_IN = {"fore": 6.0, "main": 6.0, "mizzen": 4.5}
STAYS_IN = {
    "fore.stay": 15.0,
    "fore.topmast.stay": 7.5,
    "jib.stay": 5.0,
    "flying_jib.stay": 3.5,
    "main.stay": 16.0,
    "main.topmast.stay": 7.5,
    "bobstay": 12.0,
    "martingale": 5.0,
    "mizzen.stay": 10.0,
    "storm_mizzen.stay": 5.0,
}


def mast_geometry(p):
    """Each mast's geometry in feet, its heights above her datum, keyed as the frigate's
    (`gen_ships.frigate`): Luce's chain on her main mast, (LWL + breadth) / 2 heel to head, the
    fore 9/10 of it and the mizen 13/15 of the main's height above the deck (Luce 1866 ch. VII),
    each lower mast standing on its own heel (Dia-D §4.1), where the frigate's stood 14 ft below
    its deck; the topmasts 3/5 of the main mast, the topgallant masts half the topmasts and the
    royal masts two-thirds of those; the yards 10/11 of the main mast, the topsail yards 3/4 of
    the lower, the topgallant yards 9/14 of the topsail yards and the royals two-thirds of the
    topgallants; the lower yards two feet under the hounds, the topsail yards at the topmasts'
    hounds, the topgallants and royals by the frigate's rules."""
    main_len = p.main_len_ft
    datum = DATUM_M / FT
    main = MASTS["main"]
    main_above_deck = main_len - (main["deck"] - main["heel"]) / FT
    geom = {}
    for name, m in MASTS.items():
        heel_to_deck = (m["deck"] - m["heel"]) / FT
        if name == "mizzen":
            above_deck = main_above_deck * MAST_RATIO[name]
            length = above_deck + heel_to_deck
        else:
            length = main_len * MAST_RATIO[name]
            above_deck = length - heel_to_deck
        above = above_deck + m["deck"] / FT - datum
        head = length / 6.0
        t_len = 0.6 * main_len * TOPMAST_RATIO[name]
        t_head = t_len / 6.0
        t_hoist = t_len - head
        g_len = t_len / 2.0
        g_head = g_len / 6.0
        g_hoist = g_len - t_head
        r_len = 2.0 * g_len / 3.0
        r_hoist = r_len - g_head
        yard = (10.0 / 11.0) * main_len * YARD_RATIO[name]
        topsail_yard = 0.75 * yard
        tg_yard = (9.0 / 14.0) * topsail_yard
        royal_yard = (2.0 / 3.0) * tg_yard
        geom[name] = {
            "length": length,
            "heel_to_deck": heel_to_deck,
            "above": above,
            "head": head,
            "t_len": t_len,
            "t_hoist": t_hoist,
            "g_hoist": g_hoist,
            "r_hoist": r_hoist,
            "yard": yard,
            "topsail_yard": topsail_yard,
            "tg_yard": tg_yard,
            "royal_yard": royal_yard,
            "yard_h": above - head - 2.0,
            "topsail_h": above + t_hoist - t_head,
            "tg_h": above + t_hoist + g_hoist - g_head,
            "royal_h": above + t_hoist + g_hoist + r_hoist - 1.0,
        }
    return geom


def trapezoid(head_ft, foot_ft, depth_ft):
    """A square sail's area in m2 from its head, foot and depth in feet, to the whole metre."""
    return round((head_ft + foot_ft) / 2.0 * depth_ft * FT * FT)


def square_areas(geom):
    """Each square sail's area and centre above her water by the frigate's rules: a course's drop
    0.42 of its yard and its head 0.9 of it, each sail above it between its yard and the yardarms
    below (`gen_ships.frigate`)."""
    areas = {}
    for name, gm in geom.items():
        levels = {}
        if name != "mizzen":
            depth = COURSE_DROP_OF_YARD * gm["yard"]
            levels["course"] = (
                trapezoid(0.9 * gm["yard"], 0.9 * gm["yard"], depth),
                round(DATUM_M + (gm["yard_h"] - 0.45 * depth) * FT, 1),
            )
        depth = gm["topsail_h"] - gm["yard_h"]
        levels["topsail"] = (
            trapezoid(0.82 * gm["topsail_yard"], 0.9 * gm["yard"], depth),
            round(DATUM_M + (gm["yard_h"] + 0.5 * depth) * FT, 1),
        )
        depth = gm["tg_h"] - gm["topsail_h"]
        levels["topgallant"] = (
            trapezoid(0.89 * gm["tg_yard"], 0.9 * gm["topsail_yard"], depth),
            round(DATUM_M + (gm["topsail_h"] + 0.5 * depth) * FT, 1),
        )
        depth = gm["royal_h"] - gm["tg_h"]
        levels["royal"] = (
            trapezoid(0.89 * gm["royal_yard"], 0.9 * gm["tg_yard"], depth),
            round(DATUM_M + (gm["tg_h"] + 0.5 * depth) * FT, 1),
        )
        areas[name] = levels
    return areas


def spanker_figures(p):
    """The spanker's area, centre above her water and x: the frigate's scaled by her chain."""
    area, centre, abaft = FRIGATE_SPANKER
    m = MASTS["mizzen"]
    a = round(area * p.scale * p.scale)
    c = round(DATUM_M + (centre - FRIGATE_DECK_M) * p.scale, 1)
    x = g.raked_x(m["x"] - abaft * p.scale, m["rake"], c, deck_m=m["deck"])
    return a, c, x


def head_spar_ends(p):
    """Her bowsprit's, jib-boom's and flying jib-boom's outboard lengths in feet and their ends'
    heights above her water: the bowsprit 5/8 of the main mast, a third of it inboard; the
    jib-boom 6/7 of the bowsprit, 7/12 of it outboard (Luce); the flying jib-boom 2/3 of the
    jib-boom's outboard part (judgement); rooted on her stem head and steeved as her plan has it."""
    bowsprit_out = 5.0 / 8.0 * p.main_len_ft * 2.0 / 3.0
    jib_boom_out = 6.0 / 7.0 * 5.0 / 8.0 * p.main_len_ft * 7.0 / 12.0
    flying_out = 2.0 / 3.0 * jib_boom_out
    rise = math.sin(math.radians(BOWSPRIT_STEEVE_DEG))
    root_z = STEM_HEAD[1]
    lengths = {"bowsprit": bowsprit_out, "jib_boom": jib_boom_out, "flying_jib_boom": flying_out}
    ends, out = {}, 0.0
    for spar, length in lengths.items():
        out += length
        ends[spar] = root_z + g.ft(out) * rise
    return lengths, ends


def head_figures(p):
    """The three headsails, (id, stay, area, x, centre above her water): the frigate's scaled by
    her chain, its area by the square, its place from its bowsprit's root to hers, the stem head,
    and its centre's height above the end of the spar its tack is on to hers."""
    _lengths, ends = head_spar_ends(p)
    out = []
    for sid, stay, area, x, h, spar, spar_h in FRIGATE_HEADS:
        above_tack = h - (FRIGATE_DECK_M + spar_h)
        out.append(
            (
                sid,
                stay,
                round(area * p.scale * p.scale),
                round(STEM_HEAD[0] + (x - FRIGATE_BOWSPRIT_X) * p.scale, 1),
                round(ends[spar] + above_tack * p.scale, 1),
            )
        )
    return out


def plain_sail_m2(p, geom):
    """Her plain sail as the frigate's group names it: the courses, topsails and topgallants, the
    fore topmast staysail and the jib, and the spanker."""
    areas = square_areas(geom)
    square = sum(
        areas[name][level][0]
        for name in areas
        for level in ("course", "topsail", "topgallant")
        if level in areas[name]
    )
    heads = sum(a for sid, _s, a, _x, _h in head_figures(p) if sid != "flying_jib")
    return square + heads + spanker_figures(p)[0]


def rig(b, p, geom, rope_scale):
    """Her masts, yards, square sails, standing rigging, the crossjack, the spanker and the head
    (Dia-D §4.1, §4.2): `gen_ships.frigate`'s, her figures in place of its constants. Returns the
    square sails and yards by level, the headsails and the spanker."""
    main_len = p.main_len_ft
    areas = square_areas(geom)
    sp_area, sp_centre, sp_x = spanker_figures(p)
    prov = " Provisional (truth 9), see gen_ships.py."
    yards_by_level = {level: [] for level in LEVELS}
    sails_by_level = {level: [] for level in LEVELS}
    mast_rule = {
        "main": "Luce 1866 ch. VII: (LWL + breadth) / 2, heel to head",
        "fore": "Luce: 9/10 of the main",
        "mizzen": "Luce: 13/15 of the main's height above the deck",
    }

    def sized(cls_sizes, factor):
        return {cls: g.quarter(c * factor * rope_scale) for cls, c in cls_sizes.items()}

    for name in ("fore", "main", "mizzen"):
        gm, m = geom[name], MASTS[name]
        lv = areas[name]
        carried = {
            level: [(lv[lev][0], lv[lev][1], "square") for lev in lv if lev in above_levels]
            for level, above_levels in (
                ("lower", ("course", "topsail", "topgallant", "royal")),
                ("topsail", ("topsail", "topgallant", "royal")),
                ("topgallant", ("topgallant", "royal")),
                ("royal", ("royal",)),
            )
        }
        if name == "mizzen":
            carried["lower"].append((sp_area, sp_centre, "gaff"))
        lower = b.spar(
            f"{name}.mast",
            "mast",
            x_m=m["x"],
            rake_deg=m["rake"],
            height_m=g.ft(gm["above"]),
            rating_kn=g.design_kn(carried["lower"], g.DESIGN_WIND_KN["lower"]),
            note=f"{name} lower mast by {mast_rule[name]}, on her own particulars (Dia-D §4.1), "
            "standing on its heel at the plan's step: its place at the deck and its rake the "
            "plan's (measured, Pages §6.2, re-referenced to the line), its heel the plan's in "
            "place of the frigate's 14 ft from the step to the deck; Steel 1794 vol. I p. 50's "
            f"20-gun column (Pages §7) and Babron's corvette (Dia-D §4.1) the checks.{prov}",
        )
        top = b.spar(
            f"{name}.topmast",
            "topmast",
            steps_on=lower,
            height_m=g.ft(gm["t_hoist"]),
            rating_kn=g.design_kn(carried["topsail"], g.DESIGN_WIND_KN["topsail"]),
            note=f"{name} topmast (Luce: 3/5 of the main mast"
            + ("" if name == "main" else (", 9/10 of it" if name == "fore" else ", 5/7 of it"))
            + f"), its hoist above the lower cap the length less the lower mast head.{prov}",
        )
        tg = b.spar(
            f"{name}.topgallant_mast",
            "topgallant_mast",
            steps_on=top,
            height_m=g.ft(gm["g_hoist"]),
            rating_kn=g.design_kn(carried["topgallant"], g.DESIGN_WIND_KN["topgallant"]),
            note=f"{name} topgallant mast: half the topmast (Luce), above the topmast cap.{prov}",
        )
        royal = b.spar(
            f"{name}.royal_mast",
            "royal_mast",
            steps_on=tg,
            height_m=g.ft(gm["r_hoist"]),
            rating_kn=g.design_kn(carried["royal"], g.DESIGN_WIND_KN["royal"]),
            note=f"{name} royal mast: 2/3 of the topgallant mast (Luce), above its head; Steel's "
            f"20-gun column sets the royals on the topgallant masts' poles (Pages §7).{prov}",
        )
        on_spar = {"course": lower, "topsail": top, "topgallant": tg, "royal": royal}
        for level, limit in BRACE_PLANS[name]:
            yard_id = f"{name}.{level}.yard" if level != "course" else f"{name}.yard"
            sail_id = f"{name}.{level}" if level != "course" else f"{name}.course"
            area, centre = lv[level]
            rule = {
                "course": "10/11 of the main mast (Luce; Falconer: 0.575 of the gundeck)",
                "topsail": "3/4 of the lower yard (Luce)",
                "topgallant": "9/14 of the topsail yard (Luce)",
                "royal": "2/3 of the topgallant yard (judgement; Luce's 9/20 is the later small "
                "royal)",
            }[level]
            yard = b.spar(
                yard_id,
                "yard",
                on=on_spar[level],
                length_m=g.ft(gm[YARD_LENGTHS[level]]),
                height_m=g.ft(gm[YARD_HEIGHTS[level]]),
                brace_limit_deg=limit,
                rating_kn=g.design_kn(
                    carried[LEVEL_OF_SPAR[level]], g.DESIGN_WIND_KN[LEVEL_OF_SPAR[level]]
                ),
                note=f"{name} {level} yard, {rule}; braces {limit} deg from square, the "
                "frigate-36's (Fincham 1843 art. 102, the long ships' upper value"
                f"{'' if level == 'course' else ', two degrees a level aloft'}; no source gives "
                f"hers).{prov}",
            )
            reef = REEFS[level]
            canvas = g.FRIGATE_CANVAS[sail_id]
            sail = b.sail(
                sail_id,
                "square",
                yard=yard,
                area_m2=area,
                reef_bands=reef,
                flying=True if level == "royal" else None,
                x_m=g.raked_x(m["x"], m["rake"], centre, deck_m=m["deck"]),
                centre_height_m=centre,
                canvas_no=canvas[0],
                cloth_rating_kn=g.cloth(area, canvas[0]),
                note=f"{name} {level}: between its yard and the yardarms below, its head "
                f"{HEAD_OF_YARD[level]:.2f} of the yard (the frigate-36's cut on her yards)."
                + g.canvas_note(canvas),
            )
            sizes = sized(g.FRIGATE_ROPE[level], g.FRIGATE_MAST_ROPE_FACTOR[name])
            g.square_sail_lines(
                b,
                sail,
                yard,
                sizes,
                hoisting=(level != "course"),
                course=(level == "course"),
                reef=(reef > 0),
                bowline=(level == "topsail"),
            )
            yards_by_level[level].append(yard)
            sails_by_level[level].append(sail)
        shroud_in, count = SHROUDS[name]
        size = g.quarter(shroud_in * rope_scale)
        b.sided(
            f"{name}.shrouds",
            "shroud",
            lower,
            rating=g.rope_kn(size, count),
            note=f"{count} shrouds a side, the frigate-36's count, their size hers by her rope's "
            "scale (Luce 1866 ch. VIII: first rates 10 1/2 in, one inch less per class; "
            "judgement).",
        )
        b.sided(
            f"{name}.topmast.backstay",
            "backstay",
            top,
            rating=g.rope_kn(g.quarter(BACKSTAY_IN[name] * rope_scale), 2),
        )

    gz = geom["mizzen"]
    b.spar(
        "mizzen.crossjack.yard",
        "yard",
        on="mizzen.mast",
        length_m=g.ft(gz["yard"]),
        height_m=g.ft(gz["yard_h"]),
        brace_limit_deg=CROSSJACK_BRACE_DEG,
        rating_kn=g.design_kn(
            [(areas["mizzen"]["topsail"][0], areas["mizzen"]["topsail"][1], "square")],
            g.DESIGN_WIND_KN["lower"],
        ),
        note="crossjack yard, 5/7 of the main yard (Luce; Falconer: equal to the fore topsail "
        "yard), dry: crosses no sail and spreads the mizzen topsail's foot (Dia-D §4.2); braces "
        "60 deg from square, the frigate-36's (Fincham 1843 art. 102).",
    )
    b.sided(
        "mizzen.crossjack.yard.brace",
        "brace",
        "mizzen.crossjack.yard",
        rating=g.rope_kn(g.quarter(5.0 * g.FRIGATE_MAST_ROPE_FACTOR["mizzen"] * rope_scale)),
    )
    # the spanker: boom 1/2 the main mast, gaff 4/5 of the boom (Luce)
    boom_ft = 0.5 * main_len
    gaff_ft = 0.8 * boom_ft
    gaff = b.spar(
        "mizzen.gaff",
        "gaff",
        on="mizzen.mast",
        length_m=g.ft(gaff_ft),
        height_m=g.ft(gz["above"] - gz["head"] - 3.0),
        rating_kn=g.design_kn([(sp_area, sp_centre, "gaff")], g.DESIGN_WIND_KN["gaff"]),
        note="spanker gaff, 4/5 of the boom (Luce); Steel's 20-gun mizen yard of 28 ft 6 in its "
        "length's check (Pages §7).",
    )
    boom = b.spar(
        "mizzen.boom",
        "boom",
        on="mizzen.mast",
        length_m=g.ft(boom_ft),
        height_m=BOOM_HEIGHT_M,
        horse_m=round(0.5 * BEAM_M, 1),
        rating_kn=g.design_kn([(sp_area, sp_centre, "gaff")], g.DESIGN_WIND_KN["gaff"]),
        note="spanker boom, half the main mast (Luce; Steel's 20-gun driver boom of 45 ft 6 in is "
        "longer, Pages §7), its height the frigate-36's raised to clear her taffrail's top by "
        "0.2 m (judgement); horse_m " + g.HORSE_NOTE,
    )
    spanker = b.sail(
        "mizzen.spanker",
        "gaff",
        mast="mizzen.mast",
        gaff=gaff,
        boom=boom,
        area_m2=sp_area,
        reef_bands=2,
        x_m=sp_x,
        centre_height_m=sp_centre,
        canvas_no=g.FRIGATE_CANVAS["mizzen.spanker"][0],
        cloth_rating_kn=g.cloth(sp_area, g.FRIGATE_CANVAS["mizzen.spanker"][0]),
        note="spanker (driver), the frigate-36's scaled by her chain (Dia-D §4.2): foot 0.9 of the "
        "boom, head 0.9 of the gaff, hoist from boom to jaws, gaff peaked 40 degrees; centre 0.4 "
        "of the boom abaft the mast." + g.canvas_note(g.FRIGATE_CANVAS["mizzen.spanker"]),
    )

    def r(size, parts=1):
        return g.rope_kn(g.quarter(size * rope_scale), parts)

    b.line("mizzen.gaff.throat_halyard", "throat_halyard", gaff, rating=r(4.5, 3))
    b.line("mizzen.gaff.peak_halyard", "peak_halyard", gaff, rating=r(4.0, 4))
    b.line("mizzen.spanker.sheet", "sheet", spanker, rating=r(5.0, 2), parts=2)
    b.line("mizzen.spanker.outhaul", "outhaul", spanker, rating=r(3.5))
    b.sided("mizzen.gaff.vang", "vang", gaff, rating=r(3.5))

    # the head: bowsprit 5/8 of the main mast, one third inboard; jib-boom 6/7 of the bowsprit,
    # 7/12 of it outboard (Luce); flying jib-boom 2/3 of the jib-boom's outboard part
    # (judgement). length_m is the outboard part, x_m the bowsprit's root at the stem head and
    # height_m each spar's end above her datum along the plan's steeve (as the 74's).
    lengths, above_water = head_spar_ends(p)
    bowsprit_out, jib_boom_out, flying_out = (
        lengths[s] for s in ("bowsprit", "jib_boom", "flying_jib_boom")
    )
    root_x = STEM_HEAD[0]
    ends = {spar: z - DATUM_M for spar, z in above_water.items()}
    heads = head_figures(p)
    head_loads = {sid: (area, h, "jibheaded") for sid, _st, area, _x, h in heads}
    bowsprit = b.spar(
        "bowsprit",
        "bowsprit",
        x_m=root_x,
        length_m=g.ft(bowsprit_out),
        height_m=round(ends["bowsprit"], 1),
        rating_kn=g.design_kn(list(head_loads.values()), g.DESIGN_WIND_KN["lower"]),
        note="bowsprit, 5/8 of the main mast, a third of it inboard (Luce); Steel's 20-gun 43 ft "
        f"6 in its check (Pages §7). Steeved {BOWSPRIT_STEEVE_DEG:g} deg to her line, the plan's "
        "21 deg and the line's 0.5 (Dia-D §4.1), rooted on the stem head: x_m its root, length_m "
        "its part outboard, height_m its end above the datum.",
    )
    jib_boom = b.spar(
        "jib_boom",
        "jib_boom",
        on=bowsprit,
        length_m=g.ft(jib_boom_out),
        height_m=round(ends["jib_boom"], 1),
        rating_kn=g.design_kn(
            [head_loads["jib"], head_loads["flying_jib"]], g.DESIGN_WIND_KN["jib_boom"]
        ),
        note="jib-boom, 6/7 of the bowsprit, 7/12 of it outboard along the steeve (Luce); Steel's "
        f"31 ft 0 in its check (Pages §7).{prov}",
    )
    b.spar(
        "flying_jib_boom",
        "flying_jib_boom",
        on=jib_boom,
        length_m=g.ft(flying_out),
        height_m=round(ends["flying_jib_boom"], 1),
        rating_kn=g.design_kn([head_loads["flying_jib"]], g.DESIGN_WIND_KN["flying_jib_boom"]),
        note=f"flying jib-boom, 2/3 of the jib-boom's outboard part (judgement).{prov}",
    )
    b.line(
        "fore.stay",
        "stay",
        "fore.mast",
        rating=r(STAYS_IN["fore.stay"]),
        note="the frigate-36's 15 in by her rope's scale (judgement; Luce: an 8 in collar 'for a "
        "frigate').",
    )
    b.line(
        "fore.topmast.stay",
        "stay",
        "fore.topmast",
        rating=r(STAYS_IN["fore.topmast.stay"]),
        note="the frigate-36's 7.5 in by her rope's scale; carries the fore topmast staysail.",
    )
    b.line(
        "jib.stay",
        "stay",
        "fore.topmast",
        rating=r(STAYS_IN["jib.stay"]),
        note="the frigate-36's 5 in by her rope's scale, from the fore topmast head to the "
        "jib-boom end: the jib sets on it.",
    )
    b.line(
        "flying_jib.stay",
        "stay",
        "fore.topgallant_mast",
        rating=r(STAYS_IN["flying_jib.stay"]),
        note="the frigate-36's 3.5 in by her rope's scale, from the fore topgallant mast head to "
        "the flying jib-boom end.",
    )
    b.line(
        "main.stay",
        "stay",
        "main.mast",
        rating=r(STAYS_IN["main.stay"]),
        note="the frigate-36's 16 in by her rope's scale (judgement).",
    )
    b.line("main.topmast.stay", "stay", "main.topmast", rating=r(STAYS_IN["main.topmast.stay"]))
    b.line("bobstay", "stay", bowsprit, rating=r(STAYS_IN["bobstay"]))
    b.line("martingale", "stay", jib_boom, rating=r(STAYS_IN["martingale"]))
    headsails = []
    for sid, stay, area, x, h in heads:
        s = b.sail(
            sid,
            "jibheaded",
            stay=stay,
            area_m2=area,
            x_m=x,
            centre_height_m=h,
            canvas_no=g.FRIGATE_CANVAS[sid][0],
            cloth_rating_kn=g.cloth(area, g.FRIGATE_CANVAS[sid][0]),
            note=f"{sid.replace('_', ' ').replace('.', ' ')}: the frigate-36's, its area, its "
            "place from the bowsprit's root and its height scaled by her chain (Dia-D §4.2; the "
            "frigate's judgement from the stay's run)." + g.canvas_note(g.FRIGATE_CANVAS[sid]),
        )
        size = {"fore.topmast_staysail": 3.5, "jib": 3.5, "flying_jib": 2.5}[sid]
        b.line(f"{sid}.halyard", "halyard", s, rating=r(size, 2))
        b.sided(f"{sid}.sheet", "sheet", s, rating=r(size))
        b.line(f"{sid}.downhaul", "downhaul", s, rating=r(size * 0.8))
        headsails.append(s)
    return yards_by_level, sails_by_level, headsails, spanker, boom_ft, gaff_ft


def mast_x_and_rake():
    """Each lower mast's x at the deck and its rake, as the shared helpers take them."""
    return {n: m["x"] for n, m in MASTS.items()}, {n: m["rake"] for n, m in MASTS.items()}


def staysails_between(b, geom):
    """The staysails between the masts by Steel's list for a ship (`gen_ships.between_the_masts`,
    package 57), on her geometry and above her datum."""
    mast_x, rake = mast_x_and_rake()
    kw = dict(
        geom=geom,
        mast_x=mast_x,
        rake_deg=rake,
        deck_height=DATUM_M,
        canvas=g.FRIGATE_CANVAS,
        brig=False,
    )
    between = g.between_the_masts(b, ahead="fore", after="main", **kw)
    between += g.between_the_masts(b, ahead="main", after="mizzen", **kw)
    return between


def studding_sails(b, geom, rope_scale):
    """The studding sails on fore and main, lower (fore only), topmast and topgallant: 0.4 of the
    yard they hang from wide and as deep as the sail beside them, their booms half that yard
    (`gen_ships.frigate`; Dia-D §4.2). Their figures are the generator's copy of the sail-force
    law's as item 37 left it (Dia-D §4.4)."""
    areas = square_areas(geom)
    prov = " Provisional (truth 9), see gen_ships.py."
    stuns = []
    for name in ("fore", "main"):
        m, gm = MASTS[name], geom[name]
        cut = {
            "lower": round(0.4 * gm["yard"] * 0.9 * COURSE_DROP_OF_YARD * gm["yard"] * FT * FT),
            "topmast": round(0.4 * gm["topsail_yard"] * (gm["topsail_h"] - gm["yard_h"]) * FT * FT),
            "topgallant": round(0.4 * gm["tg_yard"] * (gm["tg_h"] - gm["topsail_h"]) * FT * FT),
        }
        for level, parent_yard, boom_len, boom_h, centre in (
            (
                "lower",
                f"{name}.yard",
                0.5 * gm["yard"],
                1.0,
                areas[name]["course"][1] if name == "fore" else 0.0,
            ),
            (
                "topmast",
                f"{name}.topsail.yard",
                0.5 * gm["topsail_yard"],
                g.ft(gm["yard_h"]),
                areas[name]["topsail"][1],
            ),
            (
                "topgallant",
                f"{name}.topgallant.yard",
                0.5 * gm["tg_yard"],
                g.ft(gm["topsail_h"]),
                areas[name]["topgallant"][1],
            ),
        ):
            if name == "main" and level == "lower":
                continue
            area = cut[level]
            canvas = g.FRIGATE_CANVAS[f"{level} studding"]
            for side in g.SIDES:
                boom = b.spar(
                    f"{name}.{level}.studdingsail_boom.{side}",
                    "studdingsail_boom",
                    on=parent_yard,
                    side=side,
                    length_m=g.ft(boom_len),
                    height_m=boom_h,
                    rating_kn=g.design_kn(
                        [(area, centre, "studding")], g.DESIGN_WIND_KN["studding"]
                    ),
                    note=(
                        f"{name} {level} studding-sail boom, half the yard it is rigged on (Luce); "
                        "rated for its sail in the studding sails' design wind."
                        f"{prov}"
                        if side == g.SIDES[0]
                        else None
                    ),
                )
                sid = b.sail(
                    f"{name}.{level}.studdingsail.{side}",
                    "studding",
                    boom=boom,
                    yard=parent_yard,
                    side=side,
                    area_m2=area,
                    x_m=g.raked_x(m["x"], m["rake"], centre, deck_m=m["deck"]),
                    centre_height_m=centre,
                    canvas_no=canvas[0],
                    cloth_rating_kn=g.cloth(area, canvas[0]),
                    note=(
                        f"{name} {level} studding sail: 0.4 of the yard wide, as deep as the sail "
                        "beside it (the frigate-36's judgement)." + g.canvas_note(canvas)
                        if side == g.SIDES[0]
                        else None
                    ),
                )
                size = {"lower": 3.0, "topmast": 2.5, "topgallant": 2.0}[level]
                b.line(
                    f"{sid}.halyard", "halyard", sid, rating=g.rope_kn(g.quarter(size * rope_scale))
                )
                b.line(f"{sid}.tack", "tack", sid, rating=g.rope_kn(g.quarter(size * rope_scale)))
                b.line(
                    f"{sid}.sheet",
                    "sheet",
                    sid,
                    rating=g.rope_kn(g.quarter(size * 0.8 * rope_scale)),
                )
                b.line(
                    f"{sid}.downhaul",
                    "downhaul",
                    sid,
                    rating=g.rope_kn(g.quarter(size * 0.7 * rope_scale)),
                )
                stuns.append(sid)
    return stuns


def storm_and_occasional(b, p, geom, boom_ft, gaff_ft, rope_scale):
    """The storm canvas and the occasional sails, every one in the sail room (`bent: false`), as
    the frigate-36's (milestone 3b, package 22; spec 3b §6.4): the fore and mizzen storm
    staysails, the storm mizzen in place of the spanker, the ringtail and the save-alls; cut on
    her spars by the frigate's rules, its own hull's figures (the spanker's hoist) scaled by her
    chain."""
    mast_x, _rake = mast_x_and_rake()
    storm_canvas = g.FRIGATE_CANVAS["storm"]

    def r(size, parts=1):
        return g.rope_kn(g.quarter(size * rope_scale), parts)

    b.line(
        "mizzen.stay",
        "stay",
        "mizzen.mast",
        rating=r(STAYS_IN["mizzen.stay"]),
        note="mizzen stay, from the mizzen mast head to a collar on the main mast twelve feet "
        "above the deck (Steel 1794 vol. I, 'Mizen-stay'); the mizzen storm staysail sets on it. "
        "The frigate-36's 10 in by her rope's scale (judgement).",
    )
    gf = geom["fore"]
    fss_foot = 0.9 * gf["yard"] / 2.0 + 4.0
    fss_leech = COURSE_DROP_OF_YARD * gf["yard"]
    fss_area = round(0.5 * fss_foot * fss_leech * FT * FT)
    fss_clew_x = mast_x["fore"] + 1.0
    fss_centre = round(DATUM_M + (1.5 + fss_leech * FT / 3.0), 1)
    fss = b.sail(
        "fore.storm_staysail",
        "jibheaded",
        stay="fore.stay",
        area_m2=fss_area,
        x_m=round(fss_clew_x + fss_foot * FT / 3.0, 1),
        centre_height_m=fss_centre,
        canvas_no=storm_canvas[0],
        cloth_rating_kn=g.storm_cloth(fss_area),
        bent=False,
        note="fore storm staysail on the fore stay (Luce 1884 ch. X): Kipping's fore staysail, a "
        "right-angled triangle, its foot half the fore course's head cloths and two, its leech the "
        "course's depth; the clew just before the fore mast and the foot 5 ft above the deck "
        "(judgement); in the sail room." + g.canvas_note(storm_canvas, storm=True),
    )
    b.line("fore.storm_staysail.halyard", "halyard", fss, rating=r(3.5, 2))
    b.sided("fore.storm_staysail.sheet", "sheet", fss, rating=r(3.5, 3))
    b.line("fore.storm_staysail.downhaul", "downhaul", fss, rating=r(2.75))
    gz = geom["mizzen"]
    run_ft = (mast_x["main"] - mast_x["mizzen"]) / FT
    rise_ft = gz["above"] - gz["head"] - 12.0
    head_x, head_z = -0.6 * run_ft, 12.0 + 0.6 * rise_ft
    mss_area = round(0.5 * abs(head_x * (7.0 - 12.0) - (head_z - 12.0) * head_x) * FT * FT)
    mss = b.sail(
        "mizzen.storm_staysail",
        "jibheaded",
        stay="mizzen.stay",
        area_m2=mss_area,
        x_m=round(mast_x["main"] + (2.0 * head_x / 3.0) * FT, 1),
        centre_height_m=round(DATUM_M + (12.0 + head_z + 7.0) / 3.0 * FT, 1),
        canvas_no=storm_canvas[0],
        cloth_rating_kn=g.storm_cloth(mss_area),
        bent=False,
        note="mizzen storm staysail on the mizzen stay (Luce 1884 ch. X): tack at the main mast "
        "collar, head 0.6 up the stay, clew 7 ft above the deck (Steel's mizzen staysail; 0.6 "
        "judgement); in the sail room." + g.canvas_note(storm_canvas, storm=True),
    )
    b.line("mizzen.storm_staysail.halyard", "halyard", mss, rating=r(3.0, 2))
    b.sided("mizzen.storm_staysail.sheet", "sheet", mss, rating=r(3.0, 3))
    b.line("mizzen.storm_staysail.downhaul", "downhaul", mss, rating=r(2.5))
    b.line(
        "storm_mizzen.stay",
        "stay",
        "mizzen.mast",
        rating=r(STAYS_IN["storm_mizzen.stay"]),
        note="the storm mizzen's vertical stay under the mizzen's after trestle-tree (Luce 1884 "
        "ch. X); the frigate-36's 5 in by her rope's scale (judgement).",
    )
    sm_luff = 0.8 * (gz["above"] - gz["head"] - 4.0)
    sm_foot = 0.45 * boom_ft
    sm_area = round(0.5 * sm_luff * sm_foot * FT * FT)
    sm = b.sail(
        "storm_mizzen",
        "jibheaded",
        stay="storm_mizzen.stay",
        area_m2=sm_area,
        x_m=round(mast_x["mizzen"] - sm_foot / 3.0 * FT, 1),
        centre_height_m=round(DATUM_M + (4.0 + sm_luff / 3.0) * FT, 1),
        canvas_no=storm_canvas[0],
        cloth_rating_kn=g.storm_cloth(sm_area),
        bent=False,
        in_place_of="mizzen.spanker",
        note="storm mizzen, triangular (Luce 1884 ch. X; Steel 1794 'Storm mizen'): its luff on "
        "its vertical stay 0.8 of the mast head's height above the tack, its foot towards the "
        "taffrail 0.45 of the spanker boom (judgement); bent in place of the spanker; in the sail "
        "room." + g.canvas_note(storm_canvas, storm=True),
    )
    b.line("storm_mizzen.halyard", "halyard", sm, rating=r(3.0, 2))
    b.line("storm_mizzen.sheet", "sheet", sm, rating=r(3.5, 3), parts=3)
    b.line("storm_mizzen.downhaul", "downhaul", sm, rating=r(2.5))
    storm = [fss, mss, sm]

    # the ringtail abaft the spanker (Luce 1884 ch. XXIII; Kipping 1847, 'Ringtail Sails'): its
    # depth the spanker's after leech, the frigate's 41-ft hoist scaled by her chain and the
    # gaff's rise at its 40-degree peak; 5 cloths in the head and 7 in the foot (Kipping's brig's)
    rt_depth = 41.0 * p.scale + 0.9 * gaff_ft * math.sin(math.radians(40.0))
    rt_head, rt_foot = 10.0, 14.0
    rt_area = round((rt_head + rt_foot) / 2.0 * rt_depth * FT * FT)
    rt_boom_ft = rt_foot * 4.0 / 3.0
    rt_centre = round(DATUM_M + BOOM_HEIGHT_M + 0.45 * rt_depth * FT, 1)
    m = MASTS["mizzen"]
    rt_boom = b.spar(
        "ringtail_boom",
        "studdingsail_boom",
        on="mizzen.boom",
        length_m=g.ft(rt_boom_ft),
        height_m=BOOM_HEIGHT_M,
        rating_kn=g.design_kn([(rt_area, rt_centre, "studding")], g.DESIGN_WIND_KN["studding"]),
        note="ringtail boom, run out on the driver boom (Kipping's sliding gunter-boom; Steel 1794 "
        "vol. I, 'Ringtail-boom'): the ringtail's foot and a third that bears on the boom "
        "(judgement); rated for its sail as a studding sail boom. Provisional (truth 9), see "
        "gen_ships.py.",
    )
    rt_canvas = g.FRIGATE_CANVAS["ringtail"]
    rt = b.sail(
        "ringtail",
        "studding",
        boom=rt_boom,
        area_m2=rt_area,
        x_m=round(
            g.raked_x(m["x"], m["rake"], rt_centre, deck_m=m["deck"])
            - (0.9 * boom_ft + rt_foot / 2.0) * FT,
            1,
        ),
        centre_height_m=rt_centre,
        canvas_no=rt_canvas[0],
        cloth_rating_kn=g.cloth(rt_area, rt_canvas[0]),
        bent=False,
        note="ringtail (Kipping, Luce 1884): the depth of the spanker's after leech it borders, 5 "
        "cloths in the head and 7 in the foot (Kipping's brig's); a studding-class sail with no "
        "side, lying in the spanker's plane; in the sail room." + g.canvas_note(rt_canvas),
    )
    b.line("ringtail.halyard", "halyard", rt, rating=r(2.5))
    b.line("ringtail.tack", "tack", rt, rating=r(2.5))
    b.line("ringtail.sheet", "sheet", rt, rating=r(2.0))
    occasional = [rt]
    lower_boom_ft = 0.5 * geom["fore"]["yard"]
    sa_depth = DATUM_M + 1.0 - 0.5
    sa_area = round(0.6 * lower_boom_ft * FT * sa_depth)
    sa_centre = round(0.5 + sa_depth / 2.0, 1)
    sa_canvas = g.FRIGATE_CANVAS["save-all"]
    save_alls = []
    for side in g.SIDES:
        sa = b.sail(
            f"fore.save_all.{side}",
            "studding",
            boom=f"fore.lower.studdingsail_boom.{side}",
            yard="fore.yard",
            side=side,
            area_m2=sa_area,
            x_m=round(mast_x["fore"], 1),
            centre_height_m=sa_centre,
            canvas_no=sa_canvas[0],
            cloth_rating_kn=g.cloth(sa_area, sa_canvas[0]),
            bent=False,
            note=(
                "save-all under the fore lower studding sail boom (Luce 1884): head along 0.6 of "
                "the boom, down to half a metre off the water (judgement); in the sail room."
                + g.canvas_note(sa_canvas)
                if side == g.SIDES[0]
                else None
            ),
        )
        b.line(f"{sa}.halyard", "halyard", sa, rating=r(2.0))
        b.line(f"{sa}.tack", "tack", sa, rating=r(2.0))
        b.line(f"{sa}.sheet", "sheet", sa, rating=r(1.75))
        save_alls.append(sa)
    occasional += save_alls
    return storm, occasional, save_alls


def groups_and_aliases(
    b,
    yards_by_level,
    sails_by_level,
    headsails,
    between,
    spanker,
    stuns,
    storm,
    occasional,
    save_alls,
):
    """Her groups and aliases, the frigate-36's (`gen_ships.frigate`): what an officer of her day
    would say (Falconer 1780; Lever 1827), in the game's English."""
    b.group("courses", sails_by_level["course"])
    b.group("topsails", sails_by_level["topsail"])
    b.group("topgallants", sails_by_level["topgallant"])
    b.group("royals", sails_by_level["royal"])
    b.group("headsails", headsails)
    b.group("jibs", headsails[1:])
    b.group("staysails", headsails[:1] + between)
    b.group("staysails between the masts", between)
    b.group("studdingsails", stuns)
    b.group("square sails", sum(sails_by_level.values(), []))
    b.group("fore-and-aft sails", headsails + between + [spanker])
    light_staysails = [s for s in between if s not in ("main.staysail", "mizzen.staysail")]
    b.group("light sails", sails_by_level["royal"] + [headsails[2]] + light_staysails + stuns)
    b.group("lying-to staysails", ["main.staysail"])
    b.group(
        "plain sail",
        sails_by_level["course"]
        + sails_by_level["topsail"]
        + sails_by_level["topgallant"]
        + headsails[:2]
        + [spanker],
    )
    b.group("all sail", sum(sails_by_level.values(), []) + headsails + between + [spanker] + stuns)
    every_yard = [y for lvl in yards_by_level for y in yards_by_level[lvl]]
    for name in ("fore", "main", "mizzen"):
        b.group(
            f"{name} yards",
            [y for y in every_yard if y.startswith(name + ".")]
            + (["mizzen.crossjack.yard"] if name == "mizzen" else []),
        )
    b.group("yards", every_yard + ["mizzen.crossjack.yard"])
    b.group("lower yards", yards_by_level["course"] + ["mizzen.crossjack.yard"])
    b.group("topsail yards", yards_by_level["topsail"])
    b.group("topgallant yards", yards_by_level["topgallant"])
    b.group("royal yards", yards_by_level["royal"])
    b.group("head yards", [y for y in every_yard if y.startswith("fore.")])
    b.group(
        "after yards",
        [y for y in every_yard if not y.startswith("fore.")] + ["mizzen.crossjack.yard"],
    )
    b.group("lower masts", ["fore.mast", "main.mast", "mizzen.mast"])
    b.group("topmasts", ["fore.topmast", "main.topmast", "mizzen.topmast"])
    b.group(
        "topgallant masts",
        ["fore.topgallant_mast", "main.topgallant_mast", "mizzen.topgallant_mast"],
    )
    b.group("royal masts", ["fore.royal_mast", "main.royal_mast", "mizzen.royal_mast"])
    b.alias("spanker", "mizzen.spanker")
    b.alias("driver", "mizzen.spanker")
    b.alias("mizzen", "mizzen.spanker")
    b.alias("foresail", "fore.course")
    b.alias("mainsail", "main.course")
    b.alias("fore yard", "fore.yard")
    b.alias("main yard", "main.yard")
    b.alias("crossjack yard", "mizzen.crossjack.yard")
    b.alias("cro'jack yard", "mizzen.crossjack.yard")
    b.alias("crossjack", "mizzen.crossjack.yard")
    b.alias("spanker boom", "mizzen.boom")
    b.alias("driver boom", "mizzen.boom")
    b.alias("spanker gaff", "mizzen.gaff")
    b.alias("fore topmast staysail", "fore.topmast_staysail")
    b.alias("main topmast staysail", "main.topmast_staysail")
    b.alias("main staysail", "main.staysail")
    b.alias("main topgallant staysail", "main.topgallant_staysail")
    for word in ("mizzen", "mizen"):
        b.alias(f"{word} staysail", "mizzen.staysail")
        b.alias(f"{word} topmast staysail", "mizzen.topmast_staysail")
        b.alias(f"{word} topgallant staysail", "mizzen.topgallant_staysail")
    b.alias("stuns'ls", "studdingsails")
    b.alias("studding sails", "studdingsails")
    b.alias("kites", "studdingsails")
    b.alias("head sails", "headsails")
    b.alias("topgallant sails", "topgallants")
    b.alias("upper yards", "topgallant yards")
    b.group("storm canvas", storm)
    b.group("storm staysails", storm[:2])
    b.group("occasional sails", occasional)
    b.group("save-alls", save_alls)
    b.alias("save-all", "save-alls")
    for name in ("fore", "main"):
        for level in ("lower", "topmast", "topgallant"):
            if name == "main" and level == "lower":
                continue
            b.group(
                f"{name} {level} studdingsails",
                [f"{name}.{level}.studdingsail.{s}" for s in g.SIDES],
            )
    for name in ("fore", "main"):
        for cls in ("sheet", "tack", "bowline"):
            b.group(f"{name} {cls}s", [f"{name}.course.{cls}.{s}" for s in g.SIDES])
            b.alias(f"{name} {cls}", f"{name} {cls}s")
    for name in ("fore", "main", "mizzen"):
        b.group(f"{name} topsail bowlines", [f"{name}.topsail.bowline.{s}" for s in g.SIDES])
        b.alias(f"{name} top bowline", f"{name} topsail bowlines")


# ---------------------------------------------------------------------------
# Her guns (Dia-D §5; package 81's checklist): four fits, the default the plan's own
# ---------------------------------------------------------------------------

FIT_1807 = "danish 1807"
FIT_1809 = "as captured 1809"
FIT_1810 = "carronadas de a 30 1810"
FIT_1817 = "1817"
DEFAULT_FIT = FIT_1810
FIT_PIECES = {FIT_1807: 20, FIT_1809: 20, FIT_1810: 20, FIT_1817: 24}
# The guns' weights, cwt (Dia-D §5.2 item 4): no source gives hers. The 30-pounder carronade
# Adye's 32-pounder pattern and the 24-pounder his 24 (Adye 1804 p. 72: `period`); the long 12
# Adye's of 9 ft 6 in (p. 155: `period`); the long 8 about 23, drawn on the long 9's pattern, and
# the obús about 3 (JUDGEMENT, both).
CWT = {
    ("carronade", 30): period.ADYE_CARRONADE_CWT[32],
    ("carronade", 24): period.ADYE_CARRONADE_CWT[24],
    ("long", 12): period.ADYE_LONG_GUN_CWT[12][(9, 6)],
    ("long", 8): 23.0,
    ("carronade", 3): 3.0,
}
# The men to a pair by D31 (c), the period's sources: a carronade's four (Douglas, art. 136:
# `period.DOUGLAS_CARRONADE_CREW`), a long gun's by Falconer's QUARTERS (`period.FALCONER_CREW`:
# the 12's seven, and the 8 the 9's six, judgement), the obús two (JUDGEMENT, Dia-D §5.3).
CREW = {
    ("carronade", 30): period.DOUGLAS_CARRONADE_CREW,
    ("carronade", 24): period.DOUGLAS_CARRONADE_CREW,
    ("long", 12): period.FALCONER_CREW[12],
    ("long", 8): period.FALCONER_CREW[9],
    ("carronade", 3): 2,
}
POUNDS_NOTE = (
    "Each gun's pounds as her navy named it (the owner's decision 9, Plan-Package90.md §0): a "
    "Spanish 30-pounder fires 30 Spanish pounds, about 30 1/2 English at the book's libra of "
    "0.4608 kg (Winfield et al. 2023, pp. 41-46), a Danish 30-pounder about 33 English (Dia-D "
    "§17.1 question 2), the game's range and weight of broadside reading them a little light."
)


def places():
    """Her gun places, [x, sill, half-breadth] by the plan's port numbers (1 aftmost to 11, the
    bow port), and the place over the rail by the mizen as 'rail'."""
    out = {i: list(t) for i, t in enumerate(PORTS, start=1)}
    out["rail"] = [
        OVER_THE_RAIL_X,
        round(interp(RAIL, OVER_THE_RAIL_X) - OVER_THE_RAIL_M, 2),
        round(interp([(x, hr) for x, _hw, hr in BREADTH], OVER_THE_RAIL_X), 2),
    ]
    return out


def pair(number, kind, pounder, place, note):
    """The two guns of one number on a place of her deck, starboard then larboard, as (mapping,
    note) entries: x and sill the place's to the centimetre, the crew and weight by her rules."""
    x, sill, _hb = place
    out = []
    for i, side in enumerate(g.SIDES):
        gun = {
            "id": f"gun.{number}.{side}",
            "kind": kind,
            "pounder": pounder,
            "place": "broadside",
            "number": number,
            "side": side,
            "x_m": round(x, 2),
            "height_m": round(sill, 2),
            "crew": CREW[(kind, pounder)],
            "weight_cwt": CWT[(kind, pounder)],
            "deck": "upper",
        }
        out.append((gun, note if i == 0 else None))
    return out


def fit(spec):
    """A fit's guns from [(port or 'rail', kind, pounder, note)], numbered from forward as the
    period numbered a deck's guns, a pair a number."""
    at = places()
    ordered = sorted(spec, key=lambda s: -at[s[0]][0])
    guns = []
    for number, (port, kind, pounder, note) in enumerate(ordered, start=1):
        guns += pair(number, kind, pounder, at[port], note)
    return guns


def noted(guns, kind_pounder, note):
    """The note set on the foremost gun of the kind and calibre in a fit's (mapping, note) list."""
    for i, (gun, _n) in enumerate(guns):
        if (gun["kind"], gun["pounder"]) == kind_pounder:
            guns[i] = (gun, note)
            return
    raise ValueError(f"the fit has no {kind_pounder[1]}-pounder {kind_pounder[0]} to note.")


def her_fits():
    """Her four fits (Dia-D §5.1), as (name, source, guns, note), in the file's order, the
    dates'."""
    carronade_30 = (
        "A 30-pounder carronade a side in each of ports 1 to 10 (the plan's port numbers, 1 "
        "aftmost), each on its port to the centimetre (package 81's checklist), the 32-pounder's "
        "pattern of 17 cwt 0 qr 14 lb (Adye 1804 p. 72; judgement, no source giving hers); four "
        "men to the pair (Douglas, art. 136: D31 (c)). " + POUNDS_NOTE
    )
    danish = fit(
        [(port, "carronade", 30, None) for port in range(2, 10)]
        + [(1, "long", 8, None), (10, "long", 8, None)]
    )
    danish[0] = (
        danish[0][0],
        "The Danish fit's long 8-pounders in ports 10 and 1 (JUDGEMENT: no "
        "source places them), drawn as the long 9's pattern, about 23 cwt (JUDGEMENT); six "
        "men to the pair, Falconer's for a 9 (QUARTERS: D31 (c)).",
    )
    danish[2] = (
        danish[2][0],
        "The Danish fit's sixteen 30-pounder carronades in ports 2 to 9 "
        "(Roos 1957 p. 94), on the 32-pounder's pattern (Adye 1804 p. 72); four men to "
        "the pair (Douglas). " + POUNDS_NOTE,
    )
    captured = fit([(port, "carronade", 24, None) for port in range(1, 11)])
    captured[0] = (
        captured[0][0],
        "A 24-pounder carronade a side in each of ports 1 to 10 "
        "(Winfield et al. 2023, p. 930), Adye's 24 of 13 cwt (p. 72; judgement, no "
        "source giving hers); four men to the pair (Douglas). " + POUNDS_NOTE,
    )
    plan = fit([(port, "carronade", 30, None) for port in range(1, 11)])
    plan[0] = (plan[0][0], carronade_30)
    # her 1817 fit by the measuring note's port numbers, port 1 aftmost (Pages §5.7): the long 12s
    # forward and amidships, in ports 5 to 10, and the carronades in the after ports, 1 to 4, where
    # a ship with a quarterdeck carried hers (JUDGEMENT either way, her design's word; the lead's
    # ruling of nudge 32)
    of_1817 = fit(
        [(11, "carronade", 3, None), ("rail", "carronade", 3, None)]
        + [(port, "carronade", 30, None) for port in range(1, 5)]
        + [(port, "long", 12, None) for port in range(5, 11)]
    )
    noted(
        of_1817,
        ("carronade", 3),
        "The 1817 fit's four 3-pounder obuses (Winfield et al. 2023, p. 930), carried as "
        "carronades (Plan-Package90.md §0, Part E): two in the bow ports and two over the rail by "
        "the mizen, between ports 1 and 2 (JUDGEMENT, both places); about 3 cwt and two men to the "
        "pair (JUDGEMENT).",
    )
    noted(
        of_1817,
        ("long", 12),
        "The 1817 fit's twelve long 12-pounders forward and amidships, in ports 5 to 10 by the "
        "measuring note's numbering, port 1 aftmost (JUDGEMENT on the ports: the lead's ruling of "
        "nudge 32), Adye's 12 of 9 ft 6 in, 34 cwt (p. 155); seven men to the pair (Falconer, "
        "QUARTERS: D31 (c)). The long guns weigh more on her deck than the carronades of her other "
        "fits, and higher in her; her GM is one for every fit (Dia-D §5.3).",
    )
    noted(
        of_1817,
        ("carronade", 30),
        "The 1817 fit's eight 30-pounder carronades in the after ports, 1 to 4 (JUDGEMENT on the "
        "ports), the 32-pounder's pattern (Adye 1804 p. 72); four men to the pair (Douglas). "
        + POUNDS_NOTE,
    )
    return [
        (
            FIT_1807,
            "Roos 1957 p. 94 (her papers) and the caption of the drawing of her signed 'Thomsen "
            "pinx 1809', p. 101 (Dia §4, §8); the owner's decision 7 (Plan-Package90.md §0)",
            danish,
            "The Danish light frigate's armament when she came into Cartagena in 1807: sixteen "
            "30-pounder carronades and four long 8-pounders (Roos 1957 p. 94); for a scenario "
            "under Danish colours.",
        ),
        (
            FIT_1809,
            "Winfield et al. 2023, p. 930, her entry (VesselReferences-2026-11-Spanish.md §5, §17)",
            captured,
            "Twenty 24-pounder carronades, 'as captured' (Winfield p. 930; the book names no "
            "source for it).",
        ),
        (
            FIT_1810,
            "The Spanish navy's plan of her, 'the corvette of war la Diana, of 20 carronades of "
            "30' (BVD record 1037832, PB-021); Winfield et al. 2023, p. 930",
            plan,
            "The plan's own fit, the one her lines are drawn for, and her default (Dia-D §5.1): "
            "twenty 30-pounder carronades, ten a side.",
        ),
        (
            FIT_1817,
            "Winfield et al. 2023, p. 930",
            of_1817,
            "Her armament of 1817 (Winfield p. 930): twelve long 12-pounders, eight 30-pounder "
            "carronades and four 3-pounder obuses, the obús carried as a carronade.",
        ),
    ]


def check_fits(fits, profile):
    """Every gun of every fit on a triple of its deck to the centimetre (Build-Ships.md §5.3;
    package 81's checklist), and each fit's pieces (Dia-D §5.1), raised in words."""
    triples = {(round(x, 2), round(s, 2)) for x, s, _ in profile["ports_m"]["upper"]}
    for name, _src, guns, _note in fits:
        for gun, _n in guns:
            if (gun["x_m"], gun["height_m"]) not in triples:
                raise ValueError(
                    f"her fit '{name}' puts {gun['id']} at x {gun['x_m']} m, {gun['height_m']} m "
                    "above her water, on no triple of her deck."
                )
        if len(guns) != FIT_PIECES[name]:
            raise ValueError(
                f"her fit '{name}' mounts {len(guns)} pieces, not {FIT_PIECES[name]} (Dia-D §5.1)."
            )


def broadside_lb(guns):
    """A fit's broadside by package 70's rule: the shot of the guns of one side."""
    return sum(gun["pounder"] for gun, _ in guns if gun["side"] == g.SIDES[0])


def armament(b, fits):
    """Her fits and their magazines: `fit_magazine` with the King's allowance (judgement, as every
    man-of-war's file), the charges Table No. 29's through `charge_lb` where it names the gun and
    its kind's share where it does not (a 30-pounder carronade, an 8 and a 3: `charge_lb`), the
    exercise a ship of one deck's, a fourth of her guns."""
    rounds = {"long": g.KINGS_ROUNDS, "carronade": g.KINGS_ROUNDS}
    b.armament(
        "The armament (spec M7 7; package 70): her four fits by their dates (Dia-D §5.1), the "
        "default the plan's own; the guns as parts of the graph by their place, each on its port "
        "(package 81's checklist), with its crew by the period's sources (D31 (c)) and the "
        "magazine's allowance by kind and calibre. Every figure's source is in "
        "tools/ships/diana.py.",
        DEFAULT_FIT,
        [
            (
                name,
                source,
                guns,
                g.fit_magazine(guns, rounds, g.exercise_allowance(len(guns))),
                note,
            )
            for name, source, guns, note in fits
        ],
    )
    REPORT["fits"] = {
        name: (
            len(guns),
            broadside_lb(guns),
            sum(gun["crew"] for gun, _ in guns if gun["side"] == g.SIDES[0]),
            sum(gun["weight_cwt"] for gun, _ in guns) * g.CWT_KG / 1000.0,
        )
        for name, _s, guns, _n in fits
    }


# ---------------------------------------------------------------------------
# Her company (Dia-D §6), the quarter bill, the people
# ---------------------------------------------------------------------------

COMPLEMENT = 167
STATIONS = {
    "forecastle": 14,
    "fore_top": 12,
    "main_top": 15,
    "mizzen_top": 7,
    "afterguard": 25,
    "waisters": 18,
    "marines": 50,
    "idlers": 16,
}
# The frigate-36's idlers by trade (`gen_ships.frigate_crew`), shared to her sixteen by the largest
# remainders, ties to the first listed (computed; JUDGEMENT, as her stations are: Dia-D §6.1); a
# trade the share leaves none of (the armourer, the clerk) is not written.
FRIGATE_IDLERS = {
    "carpenter's crew": 6,
    "sailmaker's crew": 3,
    "cooper": 1,
    "armourer": 1,
    "cook": 2,
    "steward": 3,
    "servant": 8,
    "surgeon's mate": 2,
    "clerk": 1,
    "master-at-arms's party": 3,
}
TRIMMERS = {"forecastle": 8, "fore_top": 10, "main_top": 12, "mizzen_top": 6, "afterguard": 8}
FRIGATE_COMPLEMENT = 264
POSTS, DRAWN = g.wardroom("corvette-20")


def shares(total, weights):
    """`total` shared by `weights` by the largest remainders, ties to the first listed."""
    whole = sum(weights.values())
    raw = {k: total * w / whole for k, w in weights.items()}
    out = {k: int(math.floor(v)) for k, v in raw.items()}
    left = total - sum(out.values())
    for k in sorted(raw, key=lambda k: -(raw[k] - out[k]))[:left]:
        out[k] += 1
    return out


def company(b):
    """Her crew section (Dia-D §6.1): her 167 (Winfield et al. 2023, p. 930), ten posts and the
    stations of the design's table, her soldiers the 1788 regulation's fifty for her rate; her
    names Spanish (N1)."""
    if sum(STATIONS.values()) + len(POSTS) != COMPLEMENT:
        raise ValueError(
            f"her stations, {sum(STATIONS.values())}, and her {len(POSTS)} posts do not make her "
            f"{COMPLEMENT}."
        )
    idlers = shares(STATIONS["idlers"], FRIGATE_IDLERS)
    posts_note = (
        "Station holders by post (spec M3 2.3): her commissioned officers, a teniente de navío "
        "commanding, as the regulation of 1788 and her plan have it (Dia-D §6.1), then the "
        "standing and warrant officers; their words the game's English. Names are drawn at muster "
        "unless a post gives one."
    )
    b.crew(
        [
            (
                ("complement",),
                COMPLEMENT,
                "Winfield et al. 2023, p. 930: 167 men for the Spanish ship; the Danish 161 aboard "
                "in 1807 within 4% (Roos 1957 p. 90), so one company serves every fit (JUDGEMENT, "
                "Dia-D §6.1). The regulation of 1 January 1788 gives a corvette of 18 to 22 guns "
                "138 in peace (p. 1446 and following: VR-Sp §15).",
            ),
            (
                ("names",),
                "spanish",
                "Her people's names Spanish: the spanish list in data/crew/names.yaml (package 90, "
                "N1), which reads as Spain's where a scenario gives her no nation.",
            ),
            (
                ("stations", "forecastle"),
                STATIONS["forecastle"],
                "Hands per station, both watches together: her design's table (Dia-D §6.1), the "
                "107 left beside her fifty soldiers and ten posts shared on her first draft's "
                "seven stations (the frigate-36's shares scaled to her company) by the largest "
                "remainders, the main top's and the idlers' tie given to the idlers (computed in "
                "the design; JUDGEMENT until her establishment's shares are read). Forecastlemen: "
                "the head, anchors and headsails.",
            ),
            (("stations", "fore_top"), STATIONS["fore_top"], "Fore topmen."),
            (("stations", "main_top"), STATIONS["main_top"], "Main topmen, the largest top."),
            (("stations", "mizzen_top"), STATIONS["mizzen_top"], "Mizzen topmen."),
            (
                ("stations", "afterguard"),
                STATIONS["afterguard"],
                "Afterguard, the boys included (spec M3 9 item 6: boys count as landsmen).",
            ),
            (("stations", "waisters"), STATIONS["waisters"], "Waisters."),
            (
                ("stations", "marines"),
                STATIONS["marines"],
                "Her soldiers: the regulation of 1 January 1788's forty infantry and ten "
                "infantry-artillery for a corvette of 18 to 22 guns (Winfield et al. 2023, p. 1446 "
                "and following: VR-Sp §15), the count sourced and its place in her 167 JUDGEMENT; "
                "Spain's kit (data/marines.yaml, `spanish`). They stand watch and work as "
                "afterguard, never aloft. The Danes carried a petty officer and ten soldiers (Roos "
                "1957 p. 94).",
            ),
            (
                ("stations", "idlers"),
                STATIONS["idlers"],
                "Idlers: the trades below, who stand no night watches (Luce 1884 ch. XX).",
            ),
            (
                ("ratings", "able"),
                0.30,
                "Share of the seamen by rating: the frigate-36's (judgement). Able: 0.30.",
            ),
            (("ratings", "ordinary"), 0.40, "Ordinary: 0.40, judgement."),
            (("ratings", "landsman"), 0.30, "Landsmen: 0.30, judgement."),
        ]
        + [(("posts", post), None, posts_note if i == 0 else None) for i, post in enumerate(POSTS)]
        + [
            (
                ("idlers_by_trade", trade),
                n,
                "How the idlers are made up; they must sum to the idlers: the frigate-36's trades "
                "shared to her sixteen by the largest remainders (computed; JUDGEMENT)."
                if i == 0
                else None,
            )
            for i, (trade, n) in enumerate((t, n) for t, n in idlers.items() if n)
        ]
        + [
            (
                ("stores", "water_tons"),
                63,
                "Water: the frigate-36's 100 tons for 264 brought to her 167, about four months "
                "(judgement).",
            ),
            (
                ("stores", "provisions_days"),
                120,
                "Provisions: four months at full allowance for the complement (judgement).",
            ),
            (("stores", "spare_spars"), {}, None),
            (
                ("stores", "cordage_fathoms"),
                400,
                "Spare rope in the boatswain's store: the frigate-36's 600 by her sail "
                "(judgement).",
            ),
            (
                ("stores", "shot_plugs"),
                25,
                g.SHOT_PLUGS_NOTE + " The frigate-36's 40 by her company: 25.",
            ),
            *g.ration_entries("a man-of-war's, no Spanish table being in the tree (judgement)"),
        ]
    )
    b.people(
        "The named people beyond the posts (package 35, spec M5 §22): each drawn from their "
        "station at muster, the counts above unchanged (data/people/corvette-20.yaml).",
        DRAWN,
    )
    b.spare_spars(
        "The booms: the spare spars by class, the frigate-36's (Luce 1866 ch. XVII, 'Stowing "
        "Booms'; Luce 1884 ch. XI); see tools/ships/diana.py.",
        [
            ("topmast", 2, "The fore and main topmasts, one in each pile (Luce 1866)."),
            (
                "topgallant_mast",
                2,
                "A stump fore and a stump main topgallant mast, one in each pile (Luce 1866).",
            ),
            ("yard", 2, "The spare fore and main topsail yards, on the quarters (Luce 1866)."),
            (
                "studdingsail_boom",
                4,
                "The fore and main topmast studding-sail booms, a pair in each pile (Luce 1866; "
                "the pair judgement).",
            ),
            ("jib_boom", 1, "The spare jib-boom, amidships (Luce 1866)."),
            ("flying_jib_boom", 1, "The flying jib-boom, in the port pile (Luce 1866)."),
        ],
    )
    sail_room(b)
    REPORT["idlers"] = idlers


def sail_room(b):
    """The sail room (spec 3b §6.3): the frigate-36's, Luce's allowance for a frigate (1884 ch. X
    p. 171): the second of each working sail, the heavy-weather ones of No. 1, the storm canvas
    and the occasional sails."""
    working = [
        "main.course",
        "mizzen.topsail",
        "fore.topgallant",
        "main.topgallant",
        "mizzen.topgallant",
        "fore.royal",
        "main.royal",
        "mizzen.royal",
        "jib",
        "flying_jib",
        "mizzen.spanker",
        "fore.topmast_staysail",
    ]
    heavy = ["fore.course", "fore.topsail", "main.topsail"]
    storm = ["fore.storm_staysail", "mizzen.storm_staysail", "storm_mizzen"]
    occasional = [("ringtail", "ringtail")] + [(f"fore.save_all.{s}", "save-all") for s in g.SIDES]

    def first(notes, i):
        return notes if i == 0 else None

    canvas = g.FRIGATE_CANVAS
    b.sail_room(
        "The sail room (spec 3b §6.3): Luce's allowance for a frigate (1884 ch. X p. 171), the "
        "frigate-36's, every sail new; see tools/ships/diana.py.",
        [
            (k, canvas[k][0], first("The second of each working sail (Luce p. 171).", i))
            for i, k in enumerate(working)
        ]
        + [
            (
                k,
                1,
                first(
                    "The heavy-weather foresail and fore and main topsails, of No. 1 (Luce "
                    "p. 171, the table's note).",
                    i,
                ),
            )
            for i, k in enumerate(heavy)
        ]
        + [
            (k, canvas["storm"][0], first("Storm canvas, one of each (Luce p. 171).", i))
            for i, k in enumerate(storm)
        ]
        + [
            (k, canvas[c][0], first("The occasional sails, one each (spec 3b §6.4).", i))
            for i, (k, c) in enumerate(occasional)
        ],
    )


def quarter_bill(b, guns, plain):
    """Her quarter bill (spec M7 8a; package 70): the frigate-36's trimmers by station brought to
    her plain sail, two at the wheel, the small-arms men and the boarders the frigate's shares of
    her company (judgement), the filling party by Falconer."""
    trimmers = {st: round(n * plain / FRIGATE_PLAIN_SAIL_M2) for st, n in TRIMMERS.items()}
    small_arms = round(20 * COMPLEMENT / FRIGATE_COMPLEMENT)
    boarders = round(60 * COMPLEMENT / FRIGATE_COMPLEMENT)
    b.quarter_bill(
        g.QUARTER_BILL_NOTE,
        [
            (
                st,
                n,
                "The trimmers: the frigate-36's by station brought to her plain sail (judgement, "
                "as the 74's and the Neufchatel's)."
                if i == 0
                else None,
            )
            for i, (st, n) in enumerate(trimmers.items())
        ],
        2,
        0,
        "sail before guns",
        {
            "helm": "Two at the wheel (judgement: a frigate-built ship of 1804, Dia-D §6.4).",
            "powder": "The powder beyond the idlers: none; her stewards, servants, cooper and "
            "the sailmaker's crew pass the cartridges (judgement, as the frigate-36's).",
            "priority": g.PRIORITY_NOTE,
        },
        small_arms=small_arms,
        boarders=boarders,
        small_arms_note="The small-arms men: the frigate-36's share of her company (judgement).",
        boarders_note="The boarders by the bill, told off from the guns' crews with her soldiers: "
        "the frigate-36's share of her company (judgement).",
        filling=g.filling_party(guns),
    )
    REPORT["bill"] = (trimmers, small_arms, boarders)


# ---------------------------------------------------------------------------
# Her ground tackle, boats, pumps and hold (Dia-D §7)
# ---------------------------------------------------------------------------


def stores(b):
    """By the generator's helpers on her burthen of 449 tons by the old English measure (Dia-D
    §2), whose tables are English: the anchors and cables (Luce 1866 ch. XIV; Steel 1794's
    20-gun column not read: Dia-D §7, open), the hold, two chain pumps and two hand pumps, and a
    launch, a cutter and a jolly boat by the frigate's allowance at her size (JUDGEMENT)."""
    g.ground_tackle_for(b, BURTHEN_TONS, BEAM_M / FT, DRAUGHT_M / FT)
    g.hold_for(
        b,
        BURTHEN_TONS,
        True,
        "a ship of war's hold is her own stores and ballast: "
        "judgement; her 335 toneladas de arqueo (Winfield p. 930) a capacity, not a weight",
    )
    b.pumps(
        g.PUMPS_NOTE,
        g.pump_entries(
            2,
            2,
            [
                "the starboard chain pump",
                "the larboard chain pump",
                "the starboard hand pump",
                "the larboard hand pump",
            ],
        ),
    )
    b.boats(
        g.BOATS_NOTE,
        g.boat_entries(
            GUNDECK_FT,
            True,
            [
                (
                    "launch",
                    "launch",
                    "the launch",
                    1.0,
                    "The launch by Luce's rule on her 124-pie gun deck (JUDGEMENT: the frigate's "
                    "allowance at her size, Dia-D §7); the Danes' launch was put down in 1807 "
                    "(Roos 1957 p. 99).",
                ),
                (
                    "cutter",
                    "cutter",
                    "the cutter",
                    0.9,
                    "The cutter, 0.9 of the launch (Luce's rule).",
                ),
                (
                    "jolly_boat",
                    "jolly boat",
                    "the jolly boat",
                    g.JOLLY_BOAT_OF_LAUNCH,
                    "The jolly boat, the small boat at the stern davits (judgement in the size).",
                ),
            ],
        ),
    )


# ---------------------------------------------------------------------------
# Her description, and the file
# ---------------------------------------------------------------------------

DESCRIPTION = (
    "corvette",
    "a ship",
    "a corvette, flush-decked, eleven ports a side",
    "The Spanish navy's corvette of 1809 to 1817, the Danish light frigate Diana of 1804 (Winfield "
    "et al. 2023, p. 930; Roos 1957 p. 94): what the glass makes out, one tier of eleven ports in "
    "a flush side and three masts square-rigged on a small hull; the tops make her out a ship "
    "(Dia-D §8, the made-out rule; the lead's to rule on her rank at the rig's distance, Dia-D "
    "§17.2 item 1). Her default fit serves a far ship of her; her roles a King's ship's, and a "
    "cruiser's against an enemy's trade or privateers on a coast, her prize doctrine read from "
    "data/captains/cruiser.yaml (Dia-D §8.1).",
    DEFAULT_FIT,
    ["kings-ship", "cruiser"],
)

ERA_NOTES = (
    "The Diana, a light frigate of the Danish navy built at Copenhagen in 1804, taken by Spain at "
    "Cartagena in September 1809 and kept as a corvette to 1832 (Winfield et al. 2023, p. 930; "
    "Roos 1957). 124 pies by 32 pies 6 pulgadas by 16, 540 toneladas 691 libras on her plan's "
    "table; 167 men. Hull and profile measured on the Spanish navy's plan of her of 1809-1810 "
    "(BVD 1037832, PB-021; docs/design/ships-design/pages-diana.md), her load line the arrowed "
    "line as drawn; masts and yards by Luce's chain on her particulars, sails the frigate-36's set "
    "by the same chain; see tools/ships/diana.py for every figure and judgement."
)
HEADER = (
    "# The corvette Diana, 1809-1817: the Danish light frigate of 1804 in the Spanish navy.\n"
    "# Generated by tools/gen_ships.py (tools/ships/diana.py); edit those and rerun, do not\n"
    "# edit this file. Hull and profile: measured on the Spanish navy's plan of her, 'the\n"
    "# corvette of war la Diana, of 20 carronades of 30' (BVD 1037832, PB-021;\n"
    "# docs/design/ships-design/pages-diana.md), her load line the arrowed line as drawn.\n"
    "# Spars: Luce 1866 ch. VII's chain on her particulars, Steel 1794's 20-gun column the\n"
    "# check. Sails and rope: the frigate-36's by the same chain. Units: metres, m2, kg, kN.\n"
    "# Comments mark each judgement.\n"
)


def write(out_dir, p):
    """Build her file in full and dump it to `out_dir`."""
    profile = profile_into(p)
    b = HerBuilder("Diana", "ship", ERA_NOTES, p.hull, p.hull_notes)
    geom = mast_geometry(p)
    plain = plain_sail_m2(p, geom)
    rope_scale = math.sqrt(plain / FRIGATE_PLAIN_SAIL_M2)
    REPORT["rope"] = (plain, rope_scale)
    REPORT["geom"] = geom
    yards_by_level, sails_by_level, headsails, spanker, boom_ft, gaff_ft = rig(
        b, p, geom, rope_scale
    )
    between = staysails_between(b, geom)
    stuns = studding_sails(b, geom, rope_scale)
    storm, occasional, save_alls = storm_and_occasional(b, p, geom, boom_ft, gaff_ft, rope_scale)
    groups_and_aliases(
        b,
        yards_by_level,
        sails_by_level,
        headsails,
        between,
        spanker,
        stuns,
        storm,
        occasional,
        save_alls,
    )
    fits = her_fits()
    check_fits(fits, profile)
    guns = next(guns for name, _s, guns, _n in fits if name == DEFAULT_FIT)
    company(b)
    stores(b)
    armament(b, fits)
    quarter_bill(b, guns, plain)
    b.descriptions([DESCRIPTION])
    b.dump(os.path.join(out_dir, "corvette-20.yaml"), HEADER)


def her_report() -> str:
    """The generator's report: what her rules compute from her file's own keys, printed as her
    file is written and held by her tests (the lead's notes of 2026-10-29, item 2)."""
    out = [f"corvette-20: {line}" for line in REPORT.get("hull", [])]
    if "rope" in REPORT:
        plain, scale = REPORT["rope"]
        out.append(
            f"corvette-20: plain sail {plain} m2 against the frigate-36's "
            f"{FRIGATE_PLAIN_SAIL_M2:.0f}; her rope's scale {scale:.3f}."
        )
    if "geom" in REPORT:
        for name, gm in REPORT["geom"].items():
            out.append(
                f"corvette-20: the {name} mast {gm['length']:.1f} ft heel to head "
                f"({gm['length'] * FT:.2f} m), {gm['heel_to_deck']:.1f} ft heel to deck; its yard "
                f"{gm['yard']:.1f} ft ({gm['yard'] * FT:.2f} m)."
            )
    if "fits" in REPORT:
        for name, (pieces, lb, crew, tonnes) in REPORT["fits"].items():
            out.append(
                f"corvette-20: the fit '{name}', {pieces} pieces, a broadside of {lb} lb, "
                f"{crew} at the guns of a side, {tonnes:.1f} t of guns."
            )
    if "bill" in REPORT:
        trimmers, small_arms, boarders = REPORT["bill"]
        out.append(
            f"corvette-20: the quarter bill's trimmers {sum(trimmers.values())} "
            f"({', '.join(f'{k} {v}' for k, v in trimmers.items())}), {small_arms} small-arms men "
            f"and {boarders} boarders."
        )
    if "idlers" in REPORT:
        out.append(
            "corvette-20: her idlers by trade, "
            + ", ".join(f"{k} {v}" for k, v in REPORT["idlers"].items())
            + "."
        )
    return "\n".join(out)


def build(out_dir: str) -> None:
    """Write her file to `out_dir`, `corvette-20.yaml`, through `write()`; the checks of Dia-D
    §1.3 raised before it is written."""
    REPORT.clear()
    write(out_dir, particulars())
    print(her_report(), file=sys.stderr)
