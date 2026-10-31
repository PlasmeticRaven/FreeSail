"""H.M. cutter Sherbourne's hull as drawn (package 75, SW-2 with SW-2b.2; docs/design/Build-Ships.md
§5, §5.7, §5.9): her own lines, read off her own draught, for `data/ships/cutter.yaml`.

Every figure is in `docs/design/ships-design/pages-zaz6381.md` §6, in metres, x forward of the
middle of the load line and z above it at each station, each half-breadth with 2 1/2 in of plank;
`tests/test_hull_cutter.py` holds each against that section. Rung S of §5.0 unless a mark says
otherwise. The sheets are Greenwich's, read and cited, never copied (§5.9).

The drawing never feeds the physics (§5.0 principle 8): nothing here moves a figure of the hull,
a spar, a sail or a gun's calibre or place. Where the sheet and the file differ, the notes record
it and the file keeps its own.

`cutter()` calls `add_to` once, and `cutter_armament()` reads `gun_sill` and `rail` for the guns'
heights. It takes the generator's two helpers as arguments, where the other modules of this
package `import gen_ships as g`, so that its figures load with no generator at all, as
`tests/test_hull_cutter.py` reads them.
"""

from __future__ import annotations

import sys

from freesail.ship.profile import interp

DECK = "upper"  # her one deck, flush from the post to the stem (read; Build-Ships.md §5.1)

# The top of the side, the taffrail's side to where it meets the stem head's box (the note's §5.5),
# then the box's after edge to its top: ZAZ6381's upper line, raised as built by CHN0224 and CHN0102
# top to top (the note's §3.4). Sourced; 0.14 m above the draught's.
RAIL_M = [
    [-9.23, 1.83], [-8.28, 1.74], [-7.79, 1.69], [-7.25, 1.65], [-6.19, 1.59], [-5.14, 1.54],
    [-4.08, 1.52], [-3.02, 1.52], [-1.97, 1.53], [-0.92, 1.54], [0.13, 1.58], [1.09, 1.61],
    [2.05, 1.67], [3.10, 1.74], [4.16, 1.84], [5.22, 1.96], [6.27, 2.10], [7.35, 2.26],
    [8.18, 2.41], [8.33, 2.44], [8.34, 2.81],
]  # fmt: skip

# By station: x, the half-breadth at the load line, at the rail (the note's §5.7). Sourced.
BREADTH_M = [
    [-8.21, 0.35, 1.98], [-8.15, 0.54, 2.00], [-8.06, 1.30, 2.02], [-7.79, 1.83, 2.06],
    [-7.25, 2.08, 2.16], [-6.19, 2.37, 2.35], [-5.14, 2.54, 2.50], [-4.08, 2.66, 2.58],
    [-3.02, 2.75, 2.67], [-1.97, 2.82, 2.74], [-0.92, 2.86, 2.78], [0.13, 2.89, 2.83],
    [1.09, 2.89, 2.81], [2.05, 2.88, 2.84], [3.10, 2.81, 2.80], [4.16, 2.64, 2.72],
    [5.22, 2.30, 2.56], [6.27, 1.73, 2.23], [7.35, 0.87, 1.66], [7.66, 0.60, 1.43],
    [7.83, 0.45, 1.26], [7.98, 0.33, 1.07], [8.14, 0.24, 0.86], [8.24, 0.17, 0.69],
    [8.33, 0.11, 0.11],
]  # fmt: skip

# The keel's lower edge (the note's §5.4). Judged from 32 to 50 ft from AP, under the strip's
# border.
KEEL_M = [
    [-8.03, -3.03], [-6.87, -2.98], [-4.54, -2.87], [-2.20, -2.75], [0.13, -2.66], [1.29, -2.60],
    [3.82, -2.47], [7.16, -2.29],
]  # fmt: skip

# The stem's fore edge, low to high (the note's §5.5). Sourced. Its top is the stem head.
STEM_M = [
    [7.16, -2.29], [7.32, -2.21], [7.47, -2.12], [7.60, -2.02], [7.70, -1.91], [7.78, -1.83],
    [7.86, -1.71], [7.99, -1.50], [8.10, -1.30], [8.19, -1.10], [8.27, -0.90], [8.35, -0.70],
    [8.41, -0.50], [8.47, -0.30], [8.52, -0.10], [8.54, 0.00], [8.56, 0.10], [8.60, 0.30],
    [8.62, 0.49], [8.65, 0.69], [8.68, 0.89], [8.69, 1.09], [8.71, 1.28], [8.72, 1.48],
    [8.73, 1.68], [8.74, 1.87], [8.75, 2.07], [8.75, 2.27], [8.75, 2.46], [8.75, 2.66],
    [8.75, 2.81],
]  # fmt: skip

# The post's after edge, the counter and the transom at the middle line, low to high (the note's
# §5.6). Sourced; as built from the counter up on ZAZ6381's x's.
STERN_M = [
    [-8.07, -3.03], [-8.15, -2.62], [-8.27, -1.84], [-8.38, -1.06], [-8.50, -0.29], [-8.57, 0.10],
    [-8.62, 0.49], [-8.67, 0.78], [-8.67, 0.85], [-9.00, 1.05], [-9.30, 1.17], [-9.37, 1.43],
    [-9.44, 1.70], [-9.51, 1.95],
]  # fmt: skip

# The wale's lower and upper edges (the note's §5.1, §5.2). Judged, its name; not raised (§3.4).
WALES_M = [
    [-8.19, 0.20, 0.55], [-7.79, 0.18, 0.52], [-7.25, 0.14, 0.47], [-6.19, 0.07, 0.41],
    [-5.14, 0.03, 0.37], [-4.08, 0.01, 0.35], [-3.02, 0.01, 0.35], [-1.97, 0.03, 0.36],
    [-0.92, 0.05, 0.38], [0.13, 0.09, 0.41], [1.09, 0.13, 0.45], [2.05, 0.19, 0.50],
    [3.10, 0.26, 0.58], [4.16, 0.35, 0.67], [5.22, 0.47, 0.79], [6.27, 0.61, 0.93],
    [7.35, 0.78, 1.10], [8.49, 0.98, 1.31],
]  # fmt: skip

# The deck's top at the middle line, the raised deck in red (the note's §5.3). Judged: the sheet
# draws no beam's round-up, so the deck at the side is not given.
DECK_M = [
    [-8.15, 0.72], [-7.79, 0.70], [-7.25, 0.69], [-6.19, 0.66], [-5.14, 0.64], [-4.08, 0.62],
    [-3.02, 0.62], [-1.97, 0.62], [-0.92, 0.64], [0.13, 0.66], [1.09, 0.70], [2.05, 0.75],
    [3.10, 0.81], [4.16, 0.90], [5.22, 1.00], [6.27, 1.13], [7.35, 1.28], [8.13, 1.41],
]  # fmt: skip

# The sheet's four ports: x by ZAZ6381 and ZAZ6382, the sill the sheet's own "should be 1-3" above
# the deck, checked on CHN0224 (the note's §5.8). Sourced. Each [x, sill, half-breadth at the sill].
SHEET_PORTS_M = [
    [-4.75, 1.01, 2.56], [-2.35, 1.00, 2.77], [0.02, 1.04, 2.86], [3.58, 1.23, 2.79],
]  # fmt: skip
# Where the file's three guns a side stand, between those ports (no gun's x moves: Build-Ships.md
# §5.3): the same sill line and the side at each gun's own x. Judged: the sheet draws no port there.
GUN_PLACES_M = [
    [-3.50, 1.00, 2.69], [-0.50, 1.03, 2.85], [2.50, 1.15, 2.85],
]  # fmt: skip
PORTS_M = sorted(SHEET_PORTS_M + GUN_PLACES_M)
# 1 ft 11 in broad, 1 ft 6 1/2 in deep to the rail's underside (the note's §5.8). Sourced.
PORT_SIZE_M = [0.58, 0.47]

# The height of breadth and the main half-breadth by station (the note's §5.7). Sourced.
BREADTH_LINE_M = [
    [-7.79, 0.54, 2.15], [-7.25, 0.48, 2.26], [-6.19, 0.40, 2.43], [-5.14, 0.33, 2.56],
    [-4.08, 0.26, 2.67], [-3.02, 0.22, 2.76], [-1.97, 0.19, 2.83], [-0.92, 0.20, 2.87],
    [0.13, 0.22, 2.89], [1.09, 0.26, 2.89], [2.05, 0.33, 2.90], [3.10, 0.43, 2.88],
    [4.16, 0.58, 2.80], [5.22, 0.80, 2.64], [6.27, 1.10, 2.30], [7.35, 1.54, 1.70],
]  # fmt: skip

# The section's points by station, on the body plan: the keel's line, each foot, the height of
# breadth and the rail, (z, half-breadth) (the note's §5.7, read on the ink row by row). Sourced.
SECTIONS_M = {
    -7.79: [  # station 17
        [-2.78, 0.17], [-2.44, 0.16], [-2.13, 0.16], [-1.83, 0.16], [-1.52, 0.16], [-1.22, 0.19],
        [-0.91, 0.21], [-0.61, 0.32], [-0.30, 0.65], [0.00, 1.83], [0.30, 2.06], [0.54, 2.15],
        [0.61, 2.14], [0.91, 2.13], [1.22, 2.10], [1.52, 2.07], [1.69, 2.06],
    ],
    -7.25: [  # station 16
        [-2.75, 0.17], [-2.44, 0.16], [-2.13, 0.20], [-1.83, 0.20], [-1.52, 0.21], [-1.22, 0.27],
        [-0.91, 0.41], [-0.61, 0.80], [-0.30, 1.61], [0.00, 2.08], [0.30, 2.23], [0.48, 2.26],
        [0.61, 2.26], [0.91, 2.23], [1.22, 2.20], [1.52, 2.18], [1.65, 2.16],
    ],
    -6.19: [  # station 14
        [-2.69, 0.17], [-2.44, 0.15], [-2.13, 0.20], [-1.83, 0.27], [-1.52, 0.39], [-1.22, 0.59],
        [-0.91, 1.09], [-0.61, 1.71], [-0.30, 2.02], [0.00, 2.37], [0.30, 2.42], [0.40, 2.43],
        [0.61, 2.42], [0.91, 2.40], [1.22, 2.37], [1.59, 2.35],
    ],
    -5.14: [  # station 12
        [-2.64, 0.17], [-2.44, 0.19], [-2.13, 0.26], [-1.83, 0.41], [-1.52, 0.68], [-1.22, 1.12],
        [-0.91, 1.64], [-0.61, 2.07], [-0.30, 2.32], [0.00, 2.54], [0.33, 2.56], [0.61, 2.56],
        [0.91, 2.53], [1.22, 2.49], [1.54, 2.50],
    ],
    -4.08: [  # station 10
        [-2.58, 0.17], [-2.44, 0.15], [-2.13, 0.33], [-1.83, 0.59], [-1.52, 1.02], [-1.22, 1.57],
        [-0.91, 2.02], [-0.61, 2.34], [-0.30, 2.51], [0.00, 2.66], [0.26, 2.67], [0.30, 2.68],
        [0.61, 2.67], [0.91, 2.65], [1.22, 2.62], [1.52, 2.58],
    ],
    -3.02: [  # station 8
        [-2.52, 0.17], [-2.44, 0.15], [-2.13, 0.40], [-1.83, 0.78], [-1.52, 1.34], [-1.22, 1.88],
        [-0.91, 2.26], [-0.61, 2.50], [-0.30, 2.64], [0.00, 2.75], [0.22, 2.76], [0.30, 2.76],
        [0.61, 2.75], [0.91, 2.73], [1.22, 2.70], [1.52, 2.67],
    ],
    -1.97: [  # station 6
        [-2.46, 0.17], [-2.13, 0.47], [-1.83, 1.00], [-1.52, 1.62], [-1.22, 2.08], [-0.91, 2.40],
        [-0.61, 2.61], [-0.30, 2.73], [0.00, 2.82], [0.19, 2.83], [0.30, 2.82], [0.61, 2.82],
        [0.91, 2.80], [1.22, 2.78], [1.53, 2.74],
    ],
    -0.92: [  # station 4
        [-2.40, 0.17], [-2.13, 0.51], [-1.83, 1.14], [-1.52, 1.77], [-1.22, 2.19], [-0.91, 2.48],
        [-0.61, 2.67], [-0.30, 2.78], [0.00, 2.86], [0.20, 2.87], [0.30, 2.88], [0.61, 2.87],
        [0.91, 2.84], [1.22, 2.82], [1.54, 2.78],
    ],
    0.13: [  # station 2
        [-2.35, 0.17], [-2.13, 0.50], [-1.83, 1.19], [-1.52, 1.79], [-1.22, 2.21], [-0.91, 2.51],
        [-0.61, 2.69], [-0.30, 2.81], [0.00, 2.89], [0.22, 2.89], [0.30, 2.89], [0.61, 2.89],
        [0.91, 2.87], [1.22, 2.85], [1.58, 2.83],
    ],
    1.09: [  # station O
        [-2.29, 0.17], [-2.13, 0.45], [-1.83, 1.17], [-1.52, 1.78], [-1.22, 2.19], [-0.91, 2.49],
        [-0.61, 2.68], [-0.30, 2.78], [0.00, 2.89], [0.26, 2.89], [0.30, 2.89], [0.61, 2.89],
        [0.91, 2.87], [1.22, 2.85], [1.61, 2.81],
    ],
    2.05: [  # station B
        [-2.24, 0.17], [-2.13, 0.33], [-1.83, 1.05], [-1.52, 1.68], [-1.22, 2.11], [-0.91, 2.43],
        [-0.61, 2.64], [-0.30, 2.77], [0.00, 2.88], [0.33, 2.90], [0.61, 2.89], [0.91, 2.87],
        [1.22, 2.85], [1.52, 2.84], [1.67, 2.84],
    ],
    3.10: [  # station D
        [-2.18, 0.17], [-1.83, 0.74], [-1.52, 1.39], [-1.22, 1.88], [-0.91, 2.24], [-0.61, 2.50],
        [-0.30, 2.66], [0.00, 2.81], [0.30, 2.87], [0.43, 2.88], [0.61, 2.88], [0.91, 2.86],
        [1.22, 2.84], [1.52, 2.82], [1.74, 2.80],
    ],
    4.16: [  # station F
        [-2.12, 0.17], [-1.83, 0.55], [-1.52, 1.01], [-1.22, 1.50], [-0.91, 1.92], [-0.61, 2.22],
        [-0.30, 2.44], [0.00, 2.64], [0.30, 2.74], [0.58, 2.80], [0.91, 2.77], [1.22, 2.74],
        [1.52, 2.72], [1.84, 2.72],
    ],
    5.22: [  # station H
        [-2.07, 0.17], [-1.83, 0.43], [-1.52, 0.67], [-1.22, 1.05], [-0.91, 1.42], [-0.61, 1.77],
        [-0.30, 2.06], [0.00, 2.30], [0.30, 2.50], [0.61, 2.59], [0.80, 2.64], [0.91, 2.62],
        [1.22, 2.61], [1.52, 2.58], [1.83, 2.55], [1.96, 2.56],
    ],
    6.27: [  # station K
        [-2.01, 0.17], [-1.83, 0.27], [-1.52, 0.30], [-1.22, 0.57], [-0.91, 0.85], [-0.61, 1.15],
        [-0.30, 1.46], [0.00, 1.73], [0.30, 1.97], [0.61, 2.16], [0.91, 2.25], [1.10, 2.30],
        [1.22, 2.28], [1.52, 2.26], [1.83, 2.22], [2.10, 2.23],
    ],
    7.35: [  # station M
        [-1.95, 0.17], [-1.83, 0.16], [-1.52, 0.16], [-1.22, 0.18], [-0.91, 0.27], [-0.61, 0.46],
        [-0.30, 0.65], [0.00, 0.87], [0.30, 1.07], [0.61, 1.30], [0.91, 1.52], [1.22, 1.65],
        [1.54, 1.70], [1.83, 1.69], [2.26, 1.66],
    ],
}  # fmt: skip
GREATEST_STATION_M = 1.09  # O, the middle of the flat of the main breadth (the note's §5.7)

# The only other band of the side, under the rail, so named for the drawing (the note's §5.1).
# Judged.
CHANNEL_WALES_M = [
    [-7.79, 1.37, 1.43], [-7.25, 1.33, 1.38], [-6.19, 1.27, 1.32], [-5.14, 1.22, 1.28],
    [-4.08, 1.20, 1.26], [-3.02, 1.20, 1.25], [-1.97, 1.21, 1.26], [-0.92, 1.23, 1.28],
    [0.13, 1.26, 1.31], [1.09, 1.30, 1.35], [2.05, 1.35, 1.40], [3.10, 1.42, 1.47],
    [4.16, 1.52, 1.57], [5.22, 1.64, 1.69], [6.27, 1.78, 1.83], [7.35, 1.94, 2.00],
]  # fmt: skip

# The solid red curve at the section's half-breadth there (the note's §5.4). Judged, the line's
# identity.
FLOOR_M = [
    [-7.79, -0.71, 0.28], [-6.19, -1.44, 0.45], [-5.14, -1.66, 0.56], [-4.08, -1.88, 0.55],
    [-3.02, -1.97, 0.60], [-1.97, -2.00, 0.70], [-0.92, -1.99, 0.81], [0.13, -1.96, 0.89],
    [1.09, -1.91, 0.97], [2.05, -1.86, 0.97], [3.10, -1.80, 0.80], [4.16, -1.70, 0.74],
    [5.22, -1.56, 0.64], [6.27, -1.24, 0.55],
]  # fmt: skip

# The rabbet along the keel's top and up the stem, half-siding 0.36 ft (the note's §5.4, §5.5).
# Judged: the lower of the keel's two top lines, one half-siding held along her.
RABBET_M = [
    [-7.68, -2.78, 0.11], [-4.92, -2.62, 0.11], [-2.20, -2.48, 0.11], [0.13, -2.35, 0.11],
    [2.85, -2.20, 0.11], [5.76, -2.04, 0.11], [6.67, -1.77, 0.11], [7.10, -1.55, 0.11],
    [7.39, -1.34, 0.11], [7.61, -1.13, 0.11], [7.77, -0.93, 0.11], [7.92, -0.72, 0.11],
    [8.03, -0.52, 0.11], [8.13, -0.32, 0.11], [8.21, -0.12, 0.11], [8.24, -0.02, 0.11],
    [8.28, 0.08, 0.11], [8.34, 0.28, 0.11], [8.38, 0.48, 0.11], [8.41, 0.68, 0.11],
    [8.44, 0.88, 0.11],
]  # fmt: skip

# A square tuck that rounds aft, a flat counter and a flat transom raked about 20° to the line: the
# wing transom's ends for the knuckle, where the side closes to the stern, as the 64's (judgement
# which of the two); no galleries and no lights on any of her sheets; a bare stem, no head (the
# note's §5.5, §5.6).
FORM = {
    "stern": {
        "type": "square",
        "knuckle_z_m": 0.60,
        "transom_hb_m": [1.75, 2.02],
        "round_up_m": 0.07,
    },
    "head": "none",
}

# Each line's word, its weakest point's (Build-Ships.md §5.0 principle 4).
MARKS = {
    "rail_m": "sourced",
    "breadth_m": "sourced",
    "keel_m": "judged",
    "stem_m": "sourced",
    "stern_m": "sourced",
    "wales_m": "judged",  # its name
    "section_m": "sourced",
    "decks_m": "judged",
    "ports_m": "judged",
    "port_size_m": "sourced",
    "breadth_line_m": "sourced",
    "sections_m": "sourced",
    "channel_wales_m": "judged",
    "floor_m": "judged",
    "rabbet_m": "judged",  # the lower of the keel's two top lines, one half-siding held along her
    "form.stern": "sourced",
    "form.stern.knuckle_z_m": "judged",  # which of the two corners
    "form.stern.transom_hb_m": "sourced",
    "form.stern.round_up_m": "sourced",
    "form.head": "sourced",
}

NOTE = "docs/design/ships-design/pages-zaz6381.md"
KEPT = "recorded, not moved (Build-Ships.md §5.0 principle 8)"
NOTES = {
    "profile": "Her own lines, drawn only: RMG ZAZ6381, 'Sherbourn Cutter', June 1763, 1:48, with "
    "ZAZ6382 (hold and deck), CHN0224 and CHN0102 (as built), CHN0103 (the stern, 1:24) "
    f"({NOTE}; read and cited, never copied). x forward of the middle of the load line rabbet "
    "to rabbet, 27.16 ft from the after perpendicular; z above the load line at each station; "
    "metres. The load line is the top green line, unnamed on the sheets: judgement on the "
    "displacement, Steel's five-eighths (1805, OCR l. 15184-15188), the wale and the height of "
    "breadth (the note's §4.2). It lies 3.24 degrees to the page; x stays along the page, a shear "
    "and not a turn. As built: the rail, the deck and the sills of one state (the note's §5.3).",
    "profile.rail_m": "ZAZ6381 (±0.05 ft), the rail's top raised as built: CHN0224 and CHN0102, "
    "1024-px previews at 1.2 in a pixel, top line to top line (the note's §3.4, ±0.1 ft), with the "
    "sills; its last two points where it meets the stem head's box and the box's top (the note's "
    "§5.5). Every height here is the sheet's at its own station, the file's draught and drag "
    "standing beside them.",
    "profile.breadth_m": "ZAZ6381's half-breadth plan by station, with 2 1/2 in of plank "
    "(the extreme 19 ft less the moulded 18 ft 7 in, halved). Abaft station 17 the rail is the "
    "plan's inner line; forward of station M it is that line until it closes on the outer about "
    "52 ft from the after perpendicular, then the one line (the note's §5.7), and last the stem "
    "head's box, 0.7 ft across on ZAZ6382 (the note's §5.5).",
    "profile.keel_m": "The keel's lower edge (±0.1 ft); from 32 to 50 ft from the after "
    "perpendicular it lies under the sheet's strip, its depth taken from where it shows "
    "(judgement).",
    "profile.stem_m": "The stem's fore edge, a plain sweep almost plumb above the water (±0.05 "
    "ft); its top the stem head, standing above the rail.",
    "profile.stern_m": "The post's after edge, the counter and the transom at the middle line "
    "(ZAZ6381); as built from the counter up, off CHN0224 (the note's §5.6); CHN0103 keeps the "
    "rail as first drawn.",
    "profile.wales_m": "The heavy and the thin line low on the side (±0.05 ft): called the wale "
    "by judgement, the chain plates' feet ending in the band. Not raised (the note's §3.4).",
    "profile.section_m": "Station O off the body plan (the note's §5.7), with plank: about 25 "
    "degrees of floor, a slack bilge, nearly wall-sided above.",
    "profile.decks_m": "The raised deck in red, 'Deck rais'd 3 Inches' by letter of 21 June 1763 "
    "(read, tentative), its top at the middle line; judged, no beam's round-up being drawn. The "
    "file's datum stays: an existing file keeps its deck height (Build-Ships.md §5.5).",
    "profile.ports_m.upper": "Seven places on one sill line. Four are the sheet's ports, x -4.75, "
    "-2.35, 0.02 and 3.58 (ZAZ6381 and ZAZ6382), the sill the sheet's own 'should be 1-3', 1 ft 3 "
    "in above the deck, which CHN0224 draws; these are sourced. Three stand where the file's guns "
    "are, x -3.5, -0.5 and 2.5, on that line at the side there: judged, the sheet drawing no port "
    f"at them, the guns' places {KEPT}. All fall under Steel's four to five feet for cutters (p. "
    "124), on her own draught.",
    "profile.port_size_m": "1 ft 11 in broad; 1 ft 6 1/2 in deep, the ports being open to the "
    "rail's underside (the note's §5.8).",
    "profile.breadth_line_m": "The height of breadth, the sheer's dashed line and the body plan's "
    "level lines within a pixel, at the plan's main half-breadth, with plank (the note's §5.7).",
    "profile.sections_m": "Sixteen stations off the body plan, 3 ft 5 1/2 in apart (17 at 1 ft 9 "
    "in abaft 16), each foot of height, with plank (the note's §5.7): ±0.1 ft, ±0.2 ft in the last "
    "foot above the rabbet.",
    "profile.channel_wales_m": "The band of two thin lines under the rail, the only other on the "
    "upper side: so named for the drawing (judgement); as built (the note's §5.1).",
    "profile.floor_m": "The solid red curve from the post to the stem, taken for the rising line "
    "(judgement), not drawn (Build-Ships.md §5.0 principle 11).",
    "profile.rabbet_m": "The rabbet along the keel's top line and up the stem to the water and "
    "above it, half-siding 0.36 ft on the body plan's box (the note's §5.4; judgement: the lower "
    "of the keel's two top lines, one half-siding held along her); not drawn.",
    "profile.form": "Her form (Build-Ships.md §5.1): no fullness, the ends drawn through her "
    "sections.",
    "profile.form.stern": "CHN0103's 'Square Tuck that Rounds Aft' (read), a flat counter and a "
    "flat transom raked about 20 degrees to the line; the form draws the transom flat, so its "
    "round aft is recorded and not drawn (the note's §5.6). The knuckle is the wing transom at its "
    "ends, as the 64's (judgement which of the two; the counter's own corner is in stern_m).",
    "profile.form.head": "No head: a bare stem on all her sheets and on her kin Pitt's (read).",
    "profile.marks": "Each line's word is its weakest point's (Build-Ships.md §5.0 principle 4). "
    "ports_m: the sheet's four sourced, the guns' three judged.",
}
# What the sheets give beside the file's own figures, added to each key's note. No figure moves.
DEPARTURES = {
    "length_waterline_m": "ZAZ6381: her own load line (the note's §7); the keel for tonnage 44 ft "
    "7 in on all three sheets",
    "draught_m": "ZAZ6381: her own depth and drag to the keel, a load line unnamed on the sheet "
    "(the note's §4.4, §7)",
    "displacement_kg": "ZAZ6381: her sections to the load line, reckoned in the note's §4.2",
    "deck_height_m": "ZAZ6381: the deck's top above her load line (the note's §5.3, §7)",
    "rudder": "ZAZ6381: 10 ft deep, 1 ft 4 in to 2 ft 8 in broad, about 20 sq ft under water",
}
MAST_NOTE = (
    f" ZAZ6381 and ZAZ6382: 8 ft 8 in before the middle of the load line, raking 6.9 deg to it: "
    f"{KEPT}."
)
GUNS_NOTE = (
    f" ZAZ6381 has four ports a side, and these places stand between them: {KEPT}. The height is "
    "the sill's at the gun's own x (hull.profile.ports_m.upper)."
)


def gun_sill(x_m):
    """The sill of the triple at a port gun's x, metres above the load line: no gun's place is
    moved, so a gun with no triple of its own is an error here and not a figure read between."""
    for x, sill, _hb in PORTS_M:
        if abs(x - x_m) < 0.005:
            return sill
    raise ValueError(f"the cutter's profile has no port triple at x {x_m:g}.")


def rail(x_m):
    """The top of the side at x, metres above the load line, as `freesail.ship.profile.rail_at`
    reads it from the file."""
    return interp(RAIL_M, x_m)


def add_to(b, hull_profile, hull_form):
    """Her profile and form on the Builder's hull, as its last key, with their notes, and the
    drawn hull's figures beside the file's said on stderr. Returns those sentences."""
    hull = b.doc["hull"]
    sections = [[x, z, hb] for x, points in SECTIONS_M.items() for z, hb in points]
    hull["profile"] = hull_profile(
        RAIL_M,
        BREADTH_M,
        keel=KEEL_M,
        stem=STEM_M,
        stern=STERN_M,
        wales=WALES_M,
        section=SECTIONS_M[GREATEST_STATION_M],
        decks={DECK: DECK_M},
        ports={DECK: PORTS_M},
        port_size={DECK: PORT_SIZE_M},
        breadth_line=BREADTH_LINE_M,
        sections=sections,
        channel_wales=CHANNEL_WALES_M,
        floor=FLOOR_M,
        rabbet=RABBET_M,
    )
    report = []
    hull_form(
        hull,
        form=FORM,
        marks=MARKS,
        measured=[(DECK, x) for x, _sill, _hb in SHEET_PORTS_M],
        report=report,
    )
    b.hull_notes.update(NOTES)
    for key, text in DEPARTURES.items():
        b.hull_notes[key] = f"{b.hull_notes[key]} {text}: {KEPT}."
    b.notes["main.mast"] += MAST_NOTE
    print("the cutter: " + "\nthe cutter: ".join(report), file=sys.stderr)
    return report
