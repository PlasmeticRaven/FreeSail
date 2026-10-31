"""The frigate-36's hull as drawn (package 75, SW-2 with SW-2b.2; docs/design/Build-Ships.md §5.0
to §5.3, §5.7, §5.9): her measured points, and her profile and form through `g.hull_profile` and
`g.hull_form`, as the 64's and the razee's are built (`tools/ships/indefatigable.py`). `frigate()`
in `tools/gen_ships.py` calls `add_her_lines` from one place and hands `sill` to
`frigate_armament`.

Her rung is S (§5.0 principle 3): the *Amazon* class's own lines, Rule's design of 1794, ZAZ2587
(the contract draught, filed under *Emerald*) and ZAZ2559 (*Amazon*'s own copy), each a check on
the other, with the frames ZAZ2588 and ZAZ2560 and the inboard profiles ZAZ2589 and ZAZ2561. Every
point is the pages note's, docs/design/ships-design/pages-zaz2587.md §8 (`§` below without a
document's name is that note's), in its frame: x metres forward of the middle of WL1, z metres above
WL1 at the point's own station, half-breadths with the 4 in of plank. Each sheet is 1280 px wide,
and §3.5 says plainly what that gives: a clean line to 0.05-0.1 ft between sheets, ±0.15 ft besides
for WL1, a half-breadth to ±0.1 ft, ±0.3-0.4 ft where lines cross and at the ends. The images stay
in the reference cache, read and cited, never copied.

**Drawn at the sheet's length.** Sourced points win (§5.0 principle 5), and principle 7's scaling is
for a stand-in. So she is drawn 143.5 ft rabbet to rabbet at WL1 and 18 ft 6 in to K at the middle,
beside the file's 137 ft and 15 ft, and the file's masts and guns keep their places on her. All of
it is recorded and none of it moved (§9.1; the lead's point 6, 2026-10-31).

**Drawn only** (§5.0 principle 8; Build-Ships.md §5.6). Nothing the physics or the gunnery reads
comes from these lines. A gun's `x_m`, calibre and number are the file's, and the frigate's
quarterdeck stands INCORRECT by the owner's ruling (Build-Ships.md §11): `PORTS` are triples at the
file's own guns, the sheet's sill line and side at each gun's x, and `SHEET_PORTS` keeps the sheet's
own ports for package 81 (§5.0 principle 11). What a rule computes from the file's own keys, the
drawn displacement and depth, the triples' gaps to the drawn side and Steel's 36 old beside new,
goes to `REPORT`, the generator's stderr and her tests, never to a note (the lead's notes of
2026-10-29, item 2).
"""

from __future__ import annotations

import sys

import gen_ships as g

from freesail.ship.profile import interp

# -- §8.1, the first form ------------------------------------------------------------------------

# The top of the side, taffrail to stem head (§5.2, §5.6): the upper horn of the taffrail, the
# quarterdeck's rail, its scroll down to the waist, the waist rail, the scroll up to the forecastle
# and that rail (S; ZAZ2589, ±0.05 ft).
RAIL = [
    [-25.27, 6.03], [-24.99, 6.01], [-24.81, 5.55], [-23.98, 5.49], [-23.15, 5.45], [-22.32, 5.41],
    [-21.5, 5.37], [-20.81, 5.33], [-19.32, 5.26], [-17.85, 5.2], [-16.36, 5.13], [-14.87, 5.08],
    [-13.41, 5.02], [-11.91, 4.98], [-10.42, 4.94], [-8.94, 4.91], [-7.45, 4.87], [-5.97, 4.85],
    [-4.52, 4.82], [-3.01, 4.81], [-2.66, 4.8], [-2.65, 3.9], [-2.28, 3.73], [-2.07, 3.67],
    [-1.95, 3.49], [-1.2, 3.51], [0.27, 3.5], [1.76, 3.5], [3.26, 3.51], [4.72, 3.52],
    [6.21, 3.55], [7.69, 3.58], [9.17, 3.62], [9.78, 3.63], [9.85, 3.74], [10.05, 3.85],
    [10.21, 3.94], [10.43, 4.01], [10.66, 4.01], [12.15, 4.06], [13.62, 4.11], [15.11, 4.18],
    [16.59, 4.25], [18.07, 4.32], [19.57, 4.41], [21.01, 4.52], [22.56, 4.62],
]  # fmt: skip

# By station, [x, the half-breadth at WL1, at the top of the side], from the post's rabbet to the
# stem's at WL1 (judged by its weakest points, §6.1: WL1 from station 20 to H is taken 0.05 ft
# inside the main breadth; the rail is the top-timber line but for O to S+2, the body plan's).
BREADTH = [
    [-21.88, 0.27, 3.83], [-20.81, 2.16, 4.03], [-19.32, 3.81, 4.28], [-17.85, 4.46, 4.46],
    [-16.36, 4.8, 4.71], [-14.87, 5.07, 4.87], [-13.41, 5.28, 5.0], [-11.91, 5.45, 5.11],
    [-10.42, 5.56, 5.22], [-8.94, 5.64, 5.31], [-7.45, 5.7, 5.36], [-5.97, 5.74, 5.39],
    [-4.52, 5.77, 5.42], [-3.01, 5.8, 5.43], [-1.2, 5.8, 5.42], [0.27, 5.8, 5.42],
    [1.76, 5.8, 5.42], [3.26, 5.8, 5.43], [4.72, 5.8, 5.43], [6.21, 5.8, 5.42], [7.69, 5.78, 5.42],
    [9.17, 5.74, 5.43], [10.66, 5.66, 5.36], [12.15, 5.55, 5.28], [13.62, 5.38, 5.13],
    [15.11, 5.02, 4.96], [16.59, 4.58, 4.77], [18.07, 3.88, 4.43], [19.57, 2.77, 3.85],
    [20.63, 1.69, 2.76], [21.3, 0.86, 2.02], [21.74, 0.29, 1.41], [21.87, 0.25, 1.31],
]  # fmt: skip

# K, the false keel's lower edge, from the post's heel to the knee's foot (S; §5.4).
KEEL = [
    [-21.65, -5.86], [-12.77, -5.77], [-3.63, -5.67], [5.52, -5.58], [14.66, -5.49],
    [19.31, -5.44],
]  # fmt: skip

# The stem's fore edge, its foot boxed into the keel to the stem head (S; §5.5).
STEM = [
    [17.53, -5.13], [18.36, -4.85], [18.65, -4.57], [19.4, -4.15], [20.0, -3.72], [20.47, -3.31],
    [20.8, -2.89], [21.09, -2.47], [21.33, -2.06], [21.51, -1.64], [21.68, -1.22], [21.81, -0.81],
    [21.92, -0.39], [22.04, 0.02], [22.12, 0.43], [22.19, 0.85], [22.26, 1.26], [22.32, 1.68],
    [22.38, 2.09], [22.43, 2.51], [22.49, 2.92], [22.54, 3.33], [22.58, 3.75], [22.62, 4.16],
    [22.66, 4.58],
]  # fmt: skip

# The post's after face, the counters, the taffrail to its upper horn (S; §5.6, ZAZ2587's outer
# line, ±0.2 ft).
STERN = [
    [-21.65, -5.84], [-21.71, -5.51], [-21.78, -4.95], [-21.84, -4.39], [-21.88, -3.84],
    [-21.95, -3.28], [-22.0, -2.72], [-22.09, -2.16], [-22.12, -1.6], [-22.21, -1.05],
    [-22.26, -0.49], [-22.32, -0.04], [-22.34, 0.18], [-22.37, 0.63], [-22.43, 1.07],
    [-22.47, 1.52], [-22.52, 1.74], [-22.71, 1.97], [-23.05, 2.19], [-23.33, 2.41], [-23.83, 2.63],
    [-23.96, 2.85], [-24.15, 3.07], [-24.39, 3.29], [-24.43, 3.51], [-24.51, 3.74], [-24.58, 3.96],
    [-24.66, 4.18], [-24.71, 4.41], [-24.86, 4.63], [-25.05, 4.85], [-25.2, 5.07], [-25.28, 5.29],
    [-25.39, 5.74], [-25.27, 6.03],
]  # fmt: skip

# The main wale, [x, lower edge, upper edge] (§5.7; judged: the upper edge at its two ends and at
# stations 6 and 4, at its measured breadth).
WALES = [
    [-21.88, 1.13, 2.26], [-21.56, 1.01, 2.14], [-20.81, 0.84, 1.96], [-19.32, 0.73, 1.85],
    [-17.85, 0.63, 1.75], [-16.36, 0.54, 1.66], [-14.87, 0.45, 1.58], [-13.41, 0.38, 1.5],
    [-11.91, 0.31, 1.43], [-10.42, 0.25, 1.37], [-8.94, 0.2, 1.32], [-7.45, 0.15, 1.27],
    [-5.97, 0.12, 1.24], [-4.52, 0.08, 1.2], [-3.01, 0.04, 1.16], [-1.2, 0.02, 1.14],
    [0.27, 0.01, 1.13], [1.76, 0.01, 1.13], [3.26, 0.01, 1.13], [4.72, 0.02, 1.15],
    [6.21, 0.05, 1.18], [7.69, 0.09, 1.22], [9.17, 0.13, 1.25], [10.66, 0.18, 1.3],
    [12.15, 0.23, 1.35], [13.62, 0.28, 1.41], [15.11, 0.35, 1.47], [16.59, 0.42, 1.54],
    [18.07, 0.5, 1.62], [19.57, 0.59, 1.71], [22.02, 0.69, 1.82],
]  # fmt: skip

# The midship section, [z, half-breadth], the body plan's outer heavy line (S; §6.2, ±0.05 ft).
SECTION = [
    [-5.05, 0.37], [-5.03, 0.43], [-4.93, 0.55], [-4.88, 0.78], [-4.81, 1.22], [-4.73, 1.89],
    [-4.65, 2.34], [-4.5, 2.79], [-4.31, 3.24], [-4.15, 3.51], [-3.98, 3.74], [-3.81, 3.89],
    [-3.59, 4.15], [-3.31, 4.39], [-3.03, 4.6], [-2.75, 4.78], [-2.47, 4.94], [-2.19, 5.1],
    [-1.91, 5.25], [-1.63, 5.38], [-1.35, 5.5], [-1.08, 5.61], [-0.8, 5.69], [-0.52, 5.75],
    [-0.24, 5.79], [0.04, 5.8], [0.32, 5.79], [0.6, 5.83], [0.88, 5.82], [1.16, 5.79],
    [1.44, 5.78], [1.72, 5.73], [2.0, 5.65], [2.28, 5.58], [2.55, 5.51], [2.83, 5.46],
    [3.06, 5.43],
]  # fmt: skip

# Each deck at side: the second red line and 0.25 ft (§5.3, judged: the sills then stand at Steel's
# heights above it); to its ends where only the top line can be read, the lines' gap carried on.
DECKS = {
    "lower": [
        [-21.31, 0.14], [-20.81, 0.13], [-19.32, 0.07], [-17.85, 0.01], [-16.36, -0.04],
        [-14.87, -0.09], [-13.41, -0.13], [-11.91, -0.18], [-10.42, -0.21], [-8.94, -0.24],
        [-7.45, -0.27], [-5.98, -0.29], [-4.52, -0.31], [-3.01, -0.32], [-1.2, -0.33],
        [0.27, -0.33], [1.76, -0.33], [3.25, -0.32], [4.72, -0.31], [6.22, -0.29], [7.69, -0.26],
        [9.17, -0.24], [10.66, -0.2], [12.15, -0.16], [13.62, -0.12], [15.11, -0.07],
        [16.59, -0.02], [18.07, 0.03], [19.56, 0.1], [21.67, 0.16],
    ],
    "upper": [
        [-22.52, 2.1], [-20.81, 2.04], [-19.32, 1.98], [-17.85, 1.92], [-16.36, 1.86],
        [-14.87, 1.81], [-13.41, 1.76], [-11.91, 1.72], [-10.42, 1.68], [-8.94, 1.65],
        [-7.45, 1.62], [-5.98, 1.59], [-4.52, 1.58], [-3.01, 1.56], [-1.2, 1.55], [0.27, 1.55],
        [1.76, 1.56], [3.25, 1.57], [4.72, 1.59], [6.22, 1.61], [7.69, 1.63], [9.17, 1.66],
        [10.66, 1.7], [12.15, 1.74], [13.62, 1.78], [15.11, 1.82], [16.59, 1.87], [18.07, 1.92],
        [19.56, 1.97], [22.04, 2.08],
    ],
    "quarterdeck": [
        [-24.63, 4.3], [-23.44, 4.25], [-20.81, 4.14], [-19.32, 4.07], [-17.85, 4.01],
        [-16.36, 3.95], [-14.87, 3.89], [-13.41, 3.84], [-11.91, 3.8], [-10.42, 3.75],
        [-8.94, 3.72], [-7.45, 3.68], [-5.98, 3.66], [-4.52, 3.63], [-3.01, 3.62], [-2.44, 3.61],
    ],
    "forecastle": [
        [10.42, 3.73], [10.66, 3.74], [12.15, 3.77], [13.62, 3.82], [15.11, 3.86], [16.59, 3.91],
        [18.07, 3.97], [19.56, 4.03], [22.13, 4.15],
    ],
}  # fmt: skip

# -- §8.2, §8.3, the ports ------------------------------------------------------------------------

# The ports as the sheets have them (S for x and sill; §7): for the record and for package 81,
# whose ports these are. Not written to the file, whose guns stand elsewhere.
SHEET_PORTS = {
    "upper": [
        [-18.57, 2.59, 4.53], [-15.66, 2.48, 4.93], [-12.69, 2.39, 5.22], [-9.71, 2.31, 5.37],
        [-6.74, 2.25, 5.49], [-3.78, 2.22, 5.55], [-0.45, 2.19, 5.6], [2.48, 2.2, 5.6],
        [5.47, 2.23, 5.6], [8.44, 2.28, 5.57], [11.41, 2.35, 5.46], [14.37, 2.44, 5.22],
        [17.34, 2.54, 4.54],
    ],
    "quarterdeck": [
        [-21.49, 4.47, 3.9], [-18.18, 4.51, 4.42], [-14.9, 4.37, 4.87], [-12.02, 4.08, 5.1],
        [-9.01, 4.19, 5.31], [-6.35, 4.13, 5.38],
    ],
}  # fmt: skip

# The triples at the file's own guns (§8.3; Build-Ships.md §5.3: no gun's x_m moves). `upper`, the
# sheet's sill line and side at each gun's x; `quarterdeck`, the deck at side and the sheet's own
# height above it, 0.95 ft for a carronade, 1.55 ft for a long gun; `forecastle`, on no drawn port,
# 2 in under the rail (§7.3, the 64's rule). Every half-breadth is judgement on measured lines.
PORTS = {
    "upper": [
        [-16.5, 2.51, 4.84], [-13.8, 2.42, 5.13], [-11.0, 2.35, 5.3], [-8.2, 2.28, 5.44],
        [-5.5, 2.24, 5.52], [-2.8, 2.21, 5.57], [0.0, 2.19, 5.6], [2.8, 2.2, 5.6],
        [5.5, 2.23, 5.6], [8.2, 2.28, 5.57], [11.0, 2.34, 5.48], [13.8, 2.42, 5.31],
        [16.5, 2.51, 4.83],
    ],
    "quarterdeck": [
        [-17.5, 4.28, 4.52], [-14.0, 4.15, 4.95], [-10.5, 4.05, 5.21], [-7.0, 3.97, 5.37],
        [-4.5, 4.11, 5.42],
    ],
    "forecastle": [
        [14.0, 4.08, 5.08], [17.5, 4.25, 4.56],
    ],
}  # fmt: skip

# §7.1, §7.2, §8.3: the upper deck's measured on six sheets; the quarterdeck's the sheet's gun ports
# (its carronade ports 0.91 by 0.90); the forecastle's the quarterdeck's (judgement).
PORT_SIZE = {"upper": [0.88, 0.75], "quarterdeck": [0.69, 0.71], "forecastle": [0.69, 0.71]}

# -- §8.4, the shape keys ------------------------------------------------------------------------

# The knee of the head's fore edge, from its foot on K to its top (S; §5.5, ZAZ2587, ±0.3 ft).
HEAD = [
    [19.31, -5.41], [19.94, -5.05], [20.23, -4.77], [20.42, -4.49], [20.62, -4.21], [20.79, -3.92],
    [20.94, -3.64], [21.07, -3.36], [21.22, -3.08], [21.35, -2.8], [21.47, -2.52], [21.59, -2.24],
    [21.7, -1.96], [21.86, -1.68], [22.02, -1.39], [22.18, -1.11], [22.35, -0.83], [22.52, -0.55],
    [22.73, -0.27], [22.95, 0.01], [23.18, 0.3], [23.46, 0.58], [23.73, 0.86], [24.03, 1.15],
    [24.39, 1.43], [24.81, 1.77], [25.21, 2.06], [25.54, 2.34], [25.78, 2.62], [26.0, 2.9],
    [26.15, 3.19], [26.25, 3.47], [26.33, 3.75], [26.43, 4.03], [26.52, 4.31], [26.58, 4.59],
    [26.65, 4.87], [26.66, 5.15],
]  # fmt: skip

# The main breadth, [x, the upper height of breadth, the main half-breadth] (S; §5.7, §6.1; forward
# of x +15 the height ±0.3 ft).
BREADTH_LINE = [
    [-19.32, 1.37, 4.57], [-17.85, 1.3, 4.83], [-16.36, 1.2, 5.04], [-14.87, 1.13, 5.23],
    [-13.41, 1.06, 5.37], [-11.91, 0.99, 5.47], [-10.42, 0.93, 5.57], [-8.94, 0.88, 5.65],
    [-7.45, 0.84, 5.72], [-5.97, 0.82, 5.76], [-4.52, 0.82, 5.79], [-3.01, 0.82, 5.81],
    [-1.2, 0.82, 5.82], [0.27, 0.84, 5.82], [1.76, 0.86, 5.81], [3.26, 0.87, 5.81],
    [4.72, 0.9, 5.82], [6.21, 0.92, 5.81], [7.69, 0.95, 5.8], [9.17, 1.0, 5.76],
    [10.66, 1.05, 5.7], [12.15, 1.14, 5.62], [13.62, 1.23, 5.5], [15.11, 1.34, 5.26],
    [16.59, 1.54, 4.9], [18.07, 1.63, 4.34], [19.57, 1.87, 3.41],
]  # fmt: skip

# The section points by station, x: [[z, half-breadth], ...] low to high, built from the waterlines
# as the 64's (Indf §3.5 item 8), the body plan being too crowded under the breadth (§3.5): WL5 to
# WL1 where they exist, each 3.32 ft below the last; between the water and the breadth, at the
# eleven stations §6.3 follows there, the body plan's own rows from 20.4 ft above K (measured; at
# station 32 up to the sill, its height of breadth being unread), where a chord from the water to
# the next point would miss the line by up to 1.27 m; the upper height of breadth, the side at the
# sill's height (judged, §6.1) and the top of the timbers or forward the rail.
SECTIONS = {
    -20.81: [[-3.04, 0.28], [-2.02, 0.43], [-1.01, 0.77], [0.0, 2.16], [0.37, 3.56], [0.64, 3.91],
             [0.92, 4.12], [1.19, 4.23], [1.47, 4.24], [1.74, 4.23], [2.04, 4.21], [2.32, 4.17],
             [2.68, 4.14], [4.82, 4.03]],
    -19.32: [[-4.05, 0.33], [-3.04, 0.51], [-2.02, 0.93], [-1.01, 1.88], [0.0, 3.81], [0.38, 4.27],
             [0.66, 4.42], [0.93, 4.51], [1.21, 4.54], [1.37, 4.57], [2.62, 4.42], [4.72, 4.28]],
    -17.85: [[-4.05, 0.45], [-3.04, 0.83], [-2.02, 1.6], [-1.01, 3.05], [0.0, 4.46], [0.4, 4.66],
             [0.67, 4.76], [0.95, 4.81], [1.3, 4.83], [2.56, 4.64], [4.62, 4.46]],
    -16.36: [[-4.05, 0.59], [-3.04, 1.22], [-2.02, 2.32], [-1.01, 3.86], [0.0, 4.8], [0.41, 4.98],
             [0.69, 5.02], [0.96, 5.02], [1.2, 5.04], [2.5, 4.86], [4.53, 4.71]],
    -14.87: [[-4.05, 0.8], [-3.04, 1.7], [-2.02, 3.02], [-1.01, 4.39], [0.0, 5.07], [0.43, 5.19],
             [0.7, 5.25], [0.98, 5.23], [1.13, 5.23], [2.45, 5.01], [4.45, 4.87]],
    -13.41: [[-4.05, 1.06], [-3.04, 2.19], [-2.02, 3.6], [-1.01, 4.76], [0.0, 5.28], [0.44, 5.36],
             [0.72, 5.37], [1.06, 5.37], [2.4, 5.18], [4.38, 5.0]],
    -11.91: [[-4.05, 1.37], [-3.04, 2.69], [-2.02, 4.04], [-1.01, 5.03], [0.0, 5.45], [0.99, 5.47],
             [2.36, 5.26], [4.32, 5.11]],
    -10.42: [[-4.05, 1.73], [-3.04, 3.16], [-2.02, 4.4], [-1.01, 5.22], [0.0, 5.56], [0.93, 5.57],
             [2.32, 5.34], [4.26, 5.22]],
    -8.94: [[-4.05, 2.11], [-3.04, 3.55], [-2.02, 4.66], [-1.01, 5.31], [0.0, 5.64], [0.88, 5.65],
            [2.29, 5.41], [4.21, 5.31]],
    -7.45: [[-4.05, 2.48], [-3.04, 3.87], [-2.02, 4.86], [-1.01, 5.46], [0.0, 5.7], [0.84, 5.72],
            [2.26, 5.48], [4.16, 5.36]],
    -5.97: [[-4.05, 2.8], [-3.04, 4.12], [-2.02, 5.01], [-1.01, 5.55], [0.0, 5.74], [0.82, 5.76],
            [2.23, 5.51], [4.12, 5.39]],
    -4.52: [[-4.05, 3.09], [-3.04, 4.31], [-2.02, 5.1], [-1.01, 5.59], [0.0, 5.77], [0.82, 5.79],
            [2.22, 5.54], [4.07, 5.42]],
    -3.01: [[-4.05, 3.31], [-3.04, 4.45], [-2.02, 5.17], [-1.01, 5.61], [0.0, 5.8], [0.82, 5.81],
            [2.2, 5.57], [3.9, 5.43]],
    -1.2: [[-4.05, 3.48], [-3.04, 4.54], [-2.02, 5.19], [-1.01, 5.62], [0.0, 5.8], [0.82, 5.82],
           [2.19, 5.59], [3.07, 5.42]],
    0.27: [[-4.05, 3.59], [-3.04, 4.59], [-2.02, 5.2], [-1.01, 5.62], [0.0, 5.8], [0.84, 5.82],
           [2.19, 5.6], [3.08, 5.42]],
    1.76: [[-4.05, 3.63], [-3.04, 4.61], [-2.02, 5.2], [-1.01, 5.62], [0.0, 5.8], [0.86, 5.81],
           [2.2, 5.6], [3.07, 5.42]],
    3.26: [[-4.05, 3.63], [-3.04, 4.6], [-2.02, 5.2], [-1.01, 5.62], [0.0, 5.8], [0.87, 5.81],
           [2.21, 5.6], [3.08, 5.43]],
    4.72: [[-4.05, 3.56], [-3.04, 4.57], [-2.02, 5.18], [-1.01, 5.62], [0.0, 5.8], [0.9, 5.82],
           [2.23, 5.6], [3.09, 5.43]],
    6.21: [[-4.05, 3.42], [-3.04, 4.5], [-2.02, 5.14], [-1.01, 5.59], [0.0, 5.8], [0.92, 5.81],
           [2.25, 5.6], [3.11, 5.42]],
    7.69: [[-4.05, 3.2], [-3.04, 4.38], [-2.02, 5.07], [-1.01, 5.55], [0.0, 5.78], [0.95, 5.8],
           [2.27, 5.58], [3.15, 5.42]],
    9.17: [[-4.05, 2.88], [-3.04, 4.2], [-2.02, 4.95], [-1.01, 5.47], [0.0, 5.74], [1.0, 5.76],
           [2.3, 5.55], [3.2, 5.43]],
    10.66: [[-4.05, 2.52], [-3.04, 3.96], [-2.02, 4.79], [-1.01, 5.36], [0.0, 5.66], [1.05, 5.7],
            [2.34, 5.49], [4.01, 5.36]],
    12.15: [[-4.05, 2.08], [-3.04, 3.61], [-2.02, 4.54], [-1.01, 5.18], [0.0, 5.55], [1.14, 5.62],
            [2.38, 5.42], [4.06, 5.28]],
    13.62: [[-4.05, 1.66], [-3.04, 3.16], [-2.02, 4.2], [-1.01, 4.92], [0.0, 5.38], [0.72, 5.5],
            [0.99, 5.51], [1.23, 5.5], [2.42, 5.33], [4.11, 5.13]],
    15.11: [[-4.05, 1.24], [-3.04, 2.6], [-2.02, 3.7], [-1.01, 4.53], [0.0, 5.02], [0.73, 5.25],
            [1.01, 5.24], [1.34, 5.26], [2.46, 5.12], [4.18, 4.96]],
    16.59: [[-4.05, 0.86], [-3.04, 1.97], [-2.02, 3.04], [-1.01, 3.94], [0.0, 4.58], [0.75, 4.87],
            [1.02, 4.89], [1.3, 4.91], [1.54, 4.9], [2.51, 4.81], [4.25, 4.77]],
    18.07: [[-4.05, 0.52], [-3.04, 1.32], [-2.02, 2.24], [-1.01, 3.13], [0.0, 3.88], [0.76, 4.25],
            [1.04, 4.29], [1.31, 4.31], [1.63, 4.34], [2.56, 4.28], [4.32, 4.43]],
    19.57: [[-4.05, 0.33], [-3.04, 0.64], [-2.02, 1.3], [-1.01, 2.04], [0.0, 2.77], [0.78, 3.27],
            [1.05, 3.35], [1.33, 3.4], [1.6, 3.43], [1.87, 3.41], [2.61, 3.43], [4.41, 3.85]],
}  # fmt: skip

# Reserved, not drawn (§5.0 principle 11): the rising line in the sheer with the floor's
# half-breadth (§5.7, §6.1; what the line is, judged), and the rabbet with its half-siding (§5.4,
# §5.5).
FLOOR = [
    [-4.52, -3.52, 0.34], [-3.01, -4.07, 0.81], [-1.2, -4.6, 1.14], [0.27, -4.86, 1.31],
    [1.76, -5.09, 1.39], [3.25, -5.08, 1.42], [4.72, -5.05, 1.41], [6.22, -4.87, 1.32],
    [7.69, -4.63, 1.18], [9.17, -4.16, 0.87], [10.66, -3.49, 0.37],
]  # fmt: skip
RABBET = [
    [-21.12, -5.4, 0.14], [-18.87, -5.37, 0.19], [-15.82, -5.34, 0.19], [-3.63, -5.22, 0.19],
    [8.56, -5.09, 0.19], [16.18, -5.02, 0.19], [18.36, -4.57, 0.15], [19.18, -4.15, 0.15],
    [19.76, -3.73, 0.15], [20.23, -3.31, 0.15], [20.59, -2.89, 0.15], [20.9, -2.47, 0.15],
    [21.15, -2.06, 0.15], [21.35, -1.64, 0.15], [21.52, -1.23, 0.15], [21.66, -0.81, 0.15],
    [21.77, -0.4, 0.15], [21.87, 0.02, 0.15], [21.96, 0.43, 0.15], [22.04, 0.85, 0.15],
    [22.11, 1.26, 0.15], [22.17, 1.68, 0.15], [22.23, 2.09, 0.15], [22.29, 2.5, 0.15],
    [22.34, 2.92, 0.15], [22.39, 3.33, 0.15], [22.44, 3.75, 0.15], [22.49, 4.16, 0.15],
    [22.53, 4.57, 0.15],
]  # fmt: skip

# -- §8.5, the form and the marks ----------------------------------------------------------------

FORM = {
    "stern": {
        "type": "square",
        "knuckle_z_m": 1.25,  # sourced: the wing transom's ends, §5.6
        # sourced: at the taffrail, at the knuckle: 10.2 and 12.65 ft and the plank, §5.6
        "transom_hb_m": [3.21, 3.96],
        "round_up_m": 0.12,  # sourced: the wing transom's 0.40 ft
        "galleries_m": [[-23.99, -20.67, 2.62, 4.11]],  # sourced: the one tier, ZAZ2587 and ZAZ2559
        "lights_m": [[3.22, 4.01, 5, 2.6]],  # judged: no stern elevation on the sheets (§5.6)
    },
    "head": "figure",  # judged: the knee is drawn blank; its reach is head_m's, sourced
}

# Each line's rung, its weakest point's word (§5.0 principle 4; §8.5): the note on each line says
# where along her the weak points are.
MARKS = {
    "rail_m": "judged",  # the inboard sheets' heavy line in the waist taken for the rail, §3.3
    "breadth_m": "judged",
    "keel_m": "judged",  # that the strip's top border is the false keel's lower edge, §5.4
    "stem_m": "sourced",
    "stern_m": "sourced",
    "wales_m": "judged",
    "section_m": "sourced",
    "decks_m": "judged",
    "ports_m": "judged",
    "port_size_m": "judged",
    "head_m": "sourced",
    "breadth_line_m": "sourced",
    "sections_m": "judged",
    "floor_m": "judged",
    "rabbet_m": "judged",  # what the base line is; a half-siding held between its two places, §5.4
    "form.stern": "sourced",
    "form.stern.knuckle_z_m": "sourced",
    "form.stern.transom_hb_m": "sourced",
    "form.stern.round_up_m": "sourced",
    "form.stern.galleries_m": "sourced",
    "form.stern.lights_m": "judged",
    "form.head": "judged",
}

# Steel's 36, the stand-in until these sheets were read (Build-Ships.md §5.7), kept as a check, old
# beside new (§5.0 principle 12; §9.2): metres on Steel's load line
# (ships-design/pages-steel-1805-bodies.md §4, §5.3).
STEEL_36 = {
    "the sill at midships": 2.34,
    "the rail at the dead flat": 3.27,
    "the upper deck at side, its least": 1.61,
    "the quarterdeck at side at its breast": 3.67,
    "the taffrail's top": 5.92,
    "the wale's lower edge at the dead flat": 0.07,
}
DEAD_FLAT_X = 3.25  # the middle of her dead flat, ⊕ (§5.2)

NOTES = {
    "profile": (
        "Her side, decks and ports, drawn only (Build-Ships.md §5.1, §5.7): the Amazon class's own "
        "lines, ZAZ2587 and ZAZ2559 (RMG, read and cited, Crown copyright), each a check on the "
        "other, with the frames ZAZ2588 and ZAZ2560 and the inboard profiles ZAZ2589 and ZAZ2561; "
        "docs/design/ships-design/pages-zaz2587.md gives every figure with its mark. x forward of "
        "the middle of WL1, z above WL1 at each station, metres. WL1, the top green line, is taken "
        "as the load line: judgement, no sheet labels it. Plainly, recorded, not moved (§5.0 "
        "principles 5 and 8; the lead, 2026-10-31): she is drawn at the sheet's length and depth "
        "(the note's §4.3, §9.1), beside the length and draught above, and the masts and guns keep "
        "their places on her, the sheet's being the note's §5.8 and §7. Steel's 36, her stand-in "
        "until these were read, stands beside them as a check, old beside new (the note's §9.2)."
    ),
    "profile.rail_m": (
        "The top of the side from the upper of the two horns the draughts draw at the taffrail "
        "(their names judgement), along the quarterdeck's rail, the scroll down to the waist, the "
        "waist rail, the scroll up to the forecastle and its rail to the stem head: measured on "
        "ZAZ2589, checked on ZAZ2561, ZAZ2588 and ZAZ2560 and the draughts (±0.05 ft, and ±0.15 ft "
        "for WL1's own fit; the waist's top ±0.15 ft, the inboard sheets' heavy line there taken "
        "for the rail by judgement, the note's §3.3)."
    ),
    "profile.breadth_m": (
        "By station, from the post's rabbet to the stem's at WL1, the half-breadths at WL1 and at "
        "the top of the side, on ZAZ2587's plan and ZAZ2559's (measured, ±0.1 ft, ±0.3-0.4 ft at "
        "the ends), each with 4 in of plank. Judged at its weakest points: from station 20 to H "
        "WL1 runs in the main-breadth line and is taken from the midship section, 0.05 ft inside "
        "it; the top of the side is the top-timber line, which stands under the rail in the waist "
        "and at the plank-sheer aft, and for O to S+2 the body plan's half-breadth at the rail."
    ),
    "profile.keel_m": (
        "K, the false keel's lower edge (that the strip's top border is that edge, judgement: the "
        "note's §5.4), from the post's heel to the knee's foot, straight as drawn: falling aft "
        "against WL1 by the 1.46 ft of drag the sheets draw (measured)."
    ),
    "profile.stem_m": (
        "The stem's fore edge, from its foot boxed into the keel to the stem head: measured by "
        "rows on ZAZ2589, within 0.3 ft on ZAZ2587."
    ),
    "profile.stern_m": (
        "The post's after face, the two counters and the stern to the taffrail's upper horn, on "
        "ZAZ2587's outer line (measured, ±0.2 ft; the quarter gallery and the rudder left out)."
    ),
    "profile.wales_m": (
        "The main wale, 3 ft 8 in broad: its lower edge tracked on ZAZ2587 and ZAZ2559 (±0.05 ft), "
        "on WL1 within an inch amidships as Steel's rule puts it; its upper edge the faint line "
        "above it, judgement on that line's name, and at the two ends and at stations 6 and 4 set "
        "at the measured breadth."
    ),
    "profile.section_m": (
        "The midship section, the body plan's outer heavy line on ZAZ2587, both sides (measured, "
        "±0.05 ft; ZAZ2559 within 0.1 ft), with 4 in of plank, from the keel's top to the top of "
        "the timbers."
    ),
    "profile.decks_m": (
        "Each deck at side, over its extent: the second of the two red lines each deck is drawn "
        "with and 0.25 ft of plank (measured on ZAZ2589 and ZAZ2561; the deck at side judgement: "
        "the sills then stand at Steel's 36's heights above it). At the upper and lower decks' "
        "ends the top line alone can be read and the lines' gap is carried on (judgement). The "
        "lower deck has no ports and is kept by principle 11."
    ),
    "profile.ports_m.upper": (
        "At the file's own guns, whose x are kept (Build-Ships.md §5.3), not at the sheet's "
        "thirteen ports a side, which stand 9 ft 9 in apart: the note's §8.2, for package 81. The "
        "sheet's sill line at each gun's x (measured on six sheets, ±0.05 ft and ±0.15 ft for "
        "WL1), and the side at that height from the midship section and the body plan's topsides, "
        "with the plank (judgement on measured lines), as the 64's are."
    ),
    "profile.ports_m.quarterdeck": (
        "At the file's pairs 14 to 17, carronades, and 19, long 9-pounders, none on a port of the "
        "sheet's six a side (the note's §8.2): the deck at side and the sheet's own height above "
        "it, 0.95 ft at a carronade port and 1.55 ft at a gun port (measured); the half-breadth "
        "the top-timber line's, with the plank (judgement). Her quarterdeck stands INCORRECT by "
        "the owner's ruling (Build-Ships.md §11), and these follow its pairs as they are."
    ),
    "profile.ports_m.forecastle": (
        "At the file's pair 18 and its bow chasers. No sheet draws a port on the forecastle, her "
        "guns firing over the rail (judgement): the sill 2 in under the rail, the 64's rule, the "
        "half-breadth the side's at that height (judgement)."
    ),
    "profile.port_size_m": (
        "The upper deck's measured on six sheets, 2 ft 11 in by 2 ft 5 1/2 in; the quarterdeck's "
        "the sheet's gun ports, its carronade ports 3 ft by 2 ft 11 1/2 in; the forecastle's the "
        "quarterdeck's (judgement)."
    ),
    "profile.head_m": (
        "The knee of the head's fore edge, a thin line on the two draughts only, from its foot on "
        "K to its top (measured on ZAZ2587, ±0.3 ft; ZAZ2559 alike)."
    ),
    "profile.breadth_line_m": (
        "The main breadth by station: the upper of the two dashed heights of breadth on the sheer "
        "plans, at the plan's main half-breadth with the plank (measured; the heights ±0.3 ft "
        "forward of station Q, where the lines cross)."
    ),
    "profile.sections_m": (
        "The section points by station, built from the waterlines as the 64's were (Indf §3.5 item "
        "8), the body plan being too crowded under the breadth at this resolution: WL5 to WL1 "
        "where they exist, each 3.32 ft below the last (measured); between the water and the "
        "breadth, at the eleven stations where the body plan's lines can be followed there, its "
        "own rows (measured on ZAZ2587 and ZAZ2559, the note's §6.3); the upper height of breadth, "
        "the side at the sill's height (judgement on measured lines, the note's §6.1, its weakest "
        "point) and the top of the timbers or forward the rail."
    ),
    "profile.floor_m": (
        "Reserved, not drawn (§5.0 principle 11): the rising line in the sheer with the floor's "
        "half-breadth in the plan (measured; what the lines are, judgement)."
    ),
    "profile.rabbet_m": (
        "Reserved, not drawn: the heavy base line along the keel and up the stem (measured; that "
        "it is the rabbet, judgement: the note's §5.4), its half-siding read at the body plan's "
        "keel box and at the plan's ends and held along each (judgement)."
    ),
    "profile.form": (
        "Her form (Build-Ships.md §5.1): no fullness, the ends under the water drawn through her "
        "waterlines by station."
    ),
    "profile.form.stern": (
        "Square, with two counters. The knuckle is the wing transom at its ends, 4 ft 1 in above "
        "WL1, rounded up 5 in at the middle line; the transom's half-breadths 10 ft 2 in at the "
        "taffrail and 12 ft 8 in at the knuckle, moulded, and the plank (both body plans, ±0.1 "
        "ft), drawn straight between them, the form holding no more. "
        "Plainly: the sheer's outline leaves the post 1.2 ft above the wing transom, not "
        "reconciled, as on the 64. The one gallery tier as both draughts draw it. No sheet draws a "
        "stern elevation: the lights are judgement by Steel's sheer-draught method (1805 pp. "
        "250-251; §5.0 principle 9), five by the 64's count, from the upper counter at the middle "
        "line, which ends the stern below (Steel, OCR l. 15378-15382), to the top of the gallery's "
        "aftmost light, tagged on the owner's sheets."
    ),
    "profile.form.head": (
        "A figure on the knee of the head: judgement, her type certainly carrying one (§5.0 "
        "principle 9, §5.7); ZAZ2587 and ZAZ2559 draw the knee blank, with no figure."
    ),
    "profile.marks": (
        "Each line's rung (Build-Ships.md §5.0 principles 3 and 4): sourced, measured on the "
        "class's own draughts; judged, a judgement at its weakest point, which the line's note "
        "names."
    ),
}

# What the generator prints as her file is written, never in a note (the module's head).
REPORT: list[str] = []


def sill(deck: str, x: float) -> float:
    """A port gun's height: the sill of its deck's triple at its own x (Build-Ships.md §5.3), for
    `frigate_armament`. A gun off every triple is refused, never placed between two."""
    for px, z, _hb in PORTS[deck]:
        if abs(px - x) < 0.005:
            return z
    raise ValueError(f"the frigate-36's {deck} deck has no port triple at x {x:g}.")


def add_her_lines(hull: dict, notes: dict) -> None:
    """Her profile, form and marks into her hull mapping, last of its keys, and their notes into
    her hull notes; her drawn figures into `REPORT` and the generator's stderr. Nothing else of the
    hull changes (§5.0 principle 8)."""
    hull["profile"] = g.hull_profile(
        RAIL,
        BREADTH,
        keel=KEEL,
        stem=STEM,
        stern=STERN,
        wales=WALES,
        section=SECTION,
        decks=DECKS,
        ports=PORTS,
        port_size=PORT_SIZE,
        head=HEAD,
        breadth_line=BREADTH_LINE,
        sections=[[x, z, hb] for x, points in SECTIONS.items() for z, hb in points],
        floor=FLOOR,
        rabbet=RABBET,
    )
    REPORT.clear()
    # no triple's half-breadth was measured at its port (§7.1), so none is `measured`: every gap
    # is reported and none raises, as the 64's; her test holds them within the 0.05 m all the same
    g.hull_form(hull, form=FORM, marks=MARKS, measured=(), report=REPORT)
    REPORT.extend(_beside_the_file(hull))
    notes.update(NOTES)
    for line in REPORT:
        print(f"frigate-36: {line}", file=sys.stderr)


def _beside_the_file(hull: dict) -> list[str]:
    """Her sheet's figures beside the file's, and Steel's 36 old beside new: recorded, not moved
    (§5.0 principles 8 and 12; §9)."""
    now = {
        "the sill at midships": min(z for _x, z, _hb in PORTS["upper"]),
        "the rail at the dead flat": interp(RAIL, DEAD_FLAT_X),
        "the upper deck at side, its least": min(z for _x, z in DECKS["upper"]),
        "the quarterdeck at side at its breast": DECKS["quarterdeck"][-1][1],
        "the taffrail's top": STERN[-1][1],
        "the wale's lower edge at the dead flat": min(lo for _x, lo, _hi in WALES),
    }
    beside = "; ".join(f"{word} {STEEL_36[word]:g} m, now {z:.2f} m" for word, z in now.items())
    water = BREADTH[-1][0] - BREADTH[0][0]
    return [
        f"her WL1 drawn {water:.2f} m rabbet to rabbet against the file's length_waterline_m of "
        f"{hull['length_waterline_m']:g} m, and K {-interp(KEEL, 0.0):.2f} m under it at the "
        f"middle against the file's draught of {hull['draught_m']:g} m: recorded, not moved.",
        f"Steel's 36 old beside new: {beside}.",
    ]
