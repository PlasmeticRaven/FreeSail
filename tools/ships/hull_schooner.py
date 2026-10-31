"""The schooners' hull (package 75, SW-2 with SW-2b.2; docs/design/Build-Ships.md §5.0, §5.7): the
one hull of `topsail-schooner.yaml` and `privateer-schooner.yaml`, one class in two roles (the
owner, 2026-10-28; §5.0 principle 10), called from `gen_ships.schooner` and read by
`gen_ships.schooner_armament` for her guns' heights. It writes no file.

Her points are Lynx's draught as H.M. schooner Musquidobit, taken off at Portsmouth in May 1816 in
Chapelle's redrawings (The Baltimore Clipper, 1930, fig. 17 and the two plates after p. 83), as
measured in docs/design/ships-design/pages-chapelle-fig17.md (the note): the lists here are its
§6.1 and §5.8, in Lynx's own frame, x forward of the mid-perpendiculars along the load line and z
above that line, moulded, metres. The files stand for the type and not for Lynx, so the rung is S†
(§5.7) and every line is `stand-in` but those marked: `add_hull` scales them by §5.0 principle 7
(the note's §6.2) to the file's own length and beam and gives the note's §6.4. A line takes the word
of its weakest point (principle 4), `judged`: her deck at side, her main breadth, her ports and the
rail's half-breadth, and, the two steps of the note's §6.2 being judgement, every line with a height
above the water.

The drawing never feeds the physics (§5.0 principle 8): no hull figure, spar, sail, gun's calibre
or gun's x_m is read from here. A gun's height is, as §5.3 has it, and nothing reads that yet.
"""

from __future__ import annotations

import sys

import gen_ships as g

from freesail.ship.profile import interp

FT = 0.3048
# The factors' sources (the note's §6.2): Lynx's load line from rabbet to rabbet and her extreme
# breadth (read: 24 ft 0 in), over which the file's own length and beam give k_L and k_B; the plank
# on, the extreme breadth less the moulded, halved (read: 2 in); and the lowest sill of the plate,
# port 3's 3 ft 1 in (measured 3.11 ft, ±0.05 ft: the note's §5.4), which stands where the plate has
# it, her own sheet over Spider's 3 ft 5 in of 1835 (the lead's ruling, 2026-10-31; Build-Ships.md
# §5.4): so the side's height takes no lift, and only the sheer's rise above that sill is scaled.
LYNX_LOAD_LINE_M = 26.84
LYNX_BEAM_M = 24.0 * FT
PLANK_M = 2.0 / 12.0 * FT
LOWEST_SILL_PLATE_M = 0.948

# The note's §6.1. The rail cap's top, taffrail to stem head.
RAIL = [
    [-15.88, 2.44], [-13.00, 2.23], [-11.90, 2.17], [-10.71, 2.10], [-9.57, 2.04], [-8.42, 1.98],
    [-7.24, 1.94], [-6.08, 1.91], [-4.93, 1.89], [-3.77, 1.88], [-2.59, 1.87], [-1.44, 1.87],
    [-0.30, 1.87], [0.87, 1.88], [2.03, 1.90], [3.16, 1.94], [4.33, 1.98], [5.48, 2.03],
    [6.61, 2.08], [7.78, 2.15], [8.92, 2.23], [10.09, 2.30], [11.20, 2.38], [12.35, 2.47],
    [13.51, 2.57], [14.30, 2.64], [14.86, 2.70],
]  # fmt: skip
# [x, at the line, at the rail], each on the plane of the station; the last is station 23, in the
# stem, its water figure the stem's half-siding, which takes no plank.
BREADTH = [
    [-12.86, 0.34, 2.57], [-11.75, 0.97, 2.70], [-10.58, 1.70, 2.81], [-9.44, 2.23, 2.91],
    [-8.29, 2.59, 3.00], [-7.11, 2.86, 3.10], [-5.96, 3.03, 3.19], [-4.81, 3.18, 3.26],
    [-3.65, 3.27, 3.34], [-2.47, 3.33, 3.41], [-1.32, 3.40, 3.46], [-0.18, 3.45, 3.51],
    [0.99, 3.47, 3.54], [2.15, 3.47, 3.56], [3.29, 3.44, 3.55], [4.46, 3.36, 3.55],
    [5.61, 3.23, 3.48], [6.74, 3.03, 3.36], [7.92, 2.72, 3.18], [9.06, 2.30, 2.97],
    [10.24, 1.78, 2.66], [11.36, 1.20, 2.25], [12.51, 0.54, 1.64], [13.67, 0.12, 0.90],
]  # fmt: skip
# The sill line, [x, z, half-breadth of the plan's heavy line] by station, from the knuckle forward:
# the z's scale the side (§6.2); the half-breadths are the triples' at the guns' places.
SILL_LINE = [
    [-14.77, 1.34, None], [-12.94, 1.29, 2.56], [-11.83, 1.23, 2.69], [-10.65, 1.17, 2.82],
    [-9.51, 1.11, 2.94], [-8.36, 1.06, 3.05], [-7.18, 1.03, 3.14], [-6.02, 0.99, 3.23],
    [-4.87, 0.97, 3.31], [-3.71, 0.96, 3.39], [-2.53, 0.95, 3.45], [-1.38, 0.94, 3.51],
    [-0.24, 0.96, 3.56], [0.93, 0.97, 3.60], [2.09, 1.00, 3.61], [3.22, 1.03, 3.60],
    [4.39, 1.08, 3.56], [5.54, 1.14, 3.49], [6.67, 1.20, 3.38], [7.83, 1.26, 3.21],
    [8.98, 1.33, 2.95], [10.15, 1.41, 2.58], [11.26, 1.49, 2.07], [12.41, 1.58, 1.43],
    [13.57, 1.67, 0.67],
]  # fmt: skip
# The keel's lower edge, the post's heel to the forefoot.
KEEL = [
    [-11.54, -3.91], [-8.93, -3.76], [-4.63, -3.52], [-0.34, -3.28], [3.95, -3.04], [8.24, -2.80],
    [10.60, -2.65],
]  # fmt: skip
# The stem's fore edge, the forefoot to the stem head; the knee of the head is apart.
STEM = [
    [10.60, -2.65], [10.98, -2.49], [12.08, -1.77], [12.91, -1.06], [13.55, -0.37], [13.85, 0.00],
    [14.21, 0.53], [14.26, 0.75], [14.39, 0.98], [14.48, 1.20], [14.58, 1.42], [14.65, 1.64],
    [14.71, 1.77], [14.67, 2.07], [14.75, 2.29], [14.82, 2.51], [14.86, 2.70],
]  # fmt: skip
# The knee of the head's fore edge, from where it leaves the stem to under the bowsprit.
HEAD = [
    [14.21, 0.53], [14.35, 0.76], [14.48, 0.98], [14.61, 1.21], [14.75, 1.43], [14.88, 1.55],
    [15.00, 1.62], [15.13, 1.65], [15.26, 1.70], [15.32, 1.73], [15.38, 1.80], [15.41, 1.85],
]  # fmt: skip
# The post's after edge, the post's head at the knuckle, the transom's lower corner, the taffrail.
STERN = [
    [-11.54, -3.91], [-12.11, -2.91], [-12.73, -1.87], [-13.36, -0.83], [-13.87, 0.00],
    [-14.11, 0.41], [-14.77, 1.34], [-15.22, 1.62], [-15.88, 2.44],
]  # fmt: skip
KNUCKLE = STERN[6]  # the band's side, where the sill line ends (§5.3, §5.9)
# [x, z, half-siding], the post, the keel and the stem (§5.11). Not drawn (principle 11).
RABBET = [
    [-13.79, 0.54, 0.09], [-13.55, 0.23, 0.09], [-13.32, -0.07, 0.09], [-13.09, -0.38, 0.09],
    [-12.63, -1.00, 0.09], [-12.23, -1.62, 0.09], [-11.76, -2.24, 0.09], [-11.27, -2.85, 0.09],
    [-10.86, -3.44, 0.11], [-8.52, -3.36, 0.11], [-4.23, -3.09, 0.11], [0.06, -2.82, 0.11],
    [4.35, -2.56, 0.11], [8.64, -2.29, 0.11], [9.71, -2.15, 0.11], [10.77, -1.84, 0.12],
    [11.81, -1.36, 0.12], [12.84, -0.63, 0.12], [13.85, 0.48, 0.12], [14.38, 1.41, 0.12],
    [14.50, 1.74, 0.12],
]  # fmt: skip
# The deck at side: the middle line off leaf 109, less the class's round up (judgement, §5.5).
DECK_SIDE = [
    [-14.44, 1.16], [-13.00, 1.09], [-11.90, 1.05], [-10.71, 1.00], [-9.57, 0.95], [-8.42, 0.90],
    [-7.24, 0.88], [-6.08, 0.86], [-4.93, 0.84], [-3.77, 0.83], [-2.59, 0.82], [-1.44, 0.82],
    [-0.30, 0.82], [0.87, 0.82], [2.03, 0.83], [3.16, 0.86], [4.33, 0.89], [5.48, 0.93],
    [6.61, 0.97], [7.78, 1.02], [8.92, 1.08], [10.09, 1.13], [11.20, 1.18], [12.35, 1.24],
    [13.51, 1.30], [14.06, 1.33],
]  # fmt: skip
# The midship section, station 13, [z, half-breadth]: the keel's lower edge and the rabbet at the
# half-siding, which take no plank, then the body plan, the waterlines and the rail.
SECTION_X = 2.15
SECTION_SIDING_POINTS = 2
SECTION = [
    [-3.14, 0.11], [-2.69, 0.11], [-2.40, 0.50], [-1.90, 1.41], [-1.38, 2.27], [-0.71, 3.12],
    [0.00, 3.47], [0.35, 3.55], [0.70, 3.61], [1.00, 3.61], [1.91, 3.56],
]  # fmt: skip
# The main breadth, [x, z, half-breadth], stations 2 to 16 (§5.7): the height a smooth curve through
# bands on a flat section (judgement), the half-breadth as read.
MAIN_BREADTH = [
    [-10.58, 1.15, 2.83], [-9.44, 1.06, 2.95], [-8.29, 1.00, 3.05], [-7.11, 0.95, 3.15],
    [-5.96, 0.90, 3.25], [-4.81, 0.88, 3.35], [-3.65, 0.86, 3.39], [-2.47, 0.85, 3.45],
    [-1.32, 0.84, 3.52], [-0.18, 0.84, 3.57], [0.99, 0.85, 3.60], [2.15, 0.87, 3.61],
    [3.29, 0.89, 3.61], [4.46, 0.91, 3.58], [5.61, 0.95, 3.51],
]  # fmt: skip
# The sections by station, the note's §5.8: x, then [z, half-breadth] up to the sill line. Station
# 23's first point is the stem's half-siding, which takes no plank.
SECTIONS = {
    -12.86: [[0.45, 0.79], [0.90, 2.11], [1.29, 2.57]],
    -11.75: [[-1.90, 0.12], [-0.71, 0.40], [0.43, 1.71], [0.86, 2.48], [1.22, 2.70]],
    -10.58: [[-2.90, 0.11], [-2.40, 0.16], [-1.90, 0.26], [-1.38, 0.41], [-0.71, 0.81],
             [0.41, 2.36], [0.82, 2.73], [1.16, 2.83]],
    -9.44: [[-2.90, 0.14], [-2.40, 0.25], [-1.90, 0.40], [-1.38, 0.65], [-0.71, 1.24],
            [0.39, 2.66], [0.77, 2.90], [1.10, 2.95]],
    -8.29: [[-2.90, 0.17], [-2.40, 0.33], [-1.90, 0.55], [-1.38, 0.92], [-0.71, 1.70],
            [0.37, 2.87], [0.74, 3.02], [1.06, 3.05]],
    -7.11: [[-2.90, 0.21], [-2.40, 0.43], [-1.90, 0.74], [-1.38, 1.23], [-0.71, 2.10],
            [0.36, 3.02], [0.72, 3.14], [1.02, 3.15]],
    -5.96: [[-2.90, 0.22], [-2.40, 0.53], [-1.90, 0.92], [-1.38, 1.50], [-0.71, 2.40],
            [0.35, 3.17], [0.69, 3.25], [0.99, 3.23]],
    -4.81: [[-2.40, 0.60], [-1.90, 1.11], [-1.38, 1.75], [-0.71, 2.64], [0.34, 3.29],
            [0.68, 3.34], [0.97, 3.32]],
    -3.65: [[-2.40, 0.69], [-1.90, 1.30], [-1.38, 1.96], [-0.71, 2.82], [0.33, 3.34],
            [0.67, 3.39], [0.96, 3.39]],
    -2.47: [[-2.40, 0.70], [-1.90, 1.38], [-1.38, 2.11], [-0.71, 2.95], [0.33, 3.41],
            [0.66, 3.44], [0.95, 3.45]],
    -1.32: [[-2.40, 0.68], [-1.90, 1.39], [-1.38, 2.22], [-0.71, 3.04], [0.33, 3.48],
            [0.66, 3.51], [0.94, 3.51]],
    -0.18: [[-2.40, 0.59], [-1.90, 1.40], [-1.38, 2.29], [-0.71, 3.11], [0.33, 3.54],
            [0.67, 3.57], [0.96, 3.56]],
    0.99: [[-2.40, 0.51], [-1.90, 1.42], [-1.38, 2.32], [-0.71, 3.14], [0.34, 3.53],
           [0.68, 3.57], [0.97, 3.60]],
    2.15: [[-2.40, 0.50], [-1.90, 1.41], [-1.38, 2.27], [-0.71, 3.12], [0.35, 3.55],
           [0.70, 3.61], [1.00, 3.61]],
    3.29: [[-1.90, 1.26], [-1.38, 2.14], [-0.71, 3.04], [0.36, 3.53], [0.72, 3.61], [1.04, 3.60]],
    4.46: [[-1.90, 1.13], [-1.38, 1.96], [-0.71, 2.89], [0.38, 3.44], [0.76, 3.57], [1.08, 3.55]],
    5.61: [[-1.90, 0.98], [-1.38, 1.72], [-0.71, 2.63], [0.40, 3.39], [0.80, 3.49], [1.14, 3.48]],
    6.74: [[-1.90, 0.72], [-1.38, 1.42], [-0.71, 2.32], [0.42, 3.28], [0.84, 3.38], [1.20, 3.37]],
    7.92: [[-1.90, 0.49], [-1.38, 1.09], [-0.71, 1.95], [0.44, 3.05], [0.89, 3.20], [1.27, 3.19]],
    9.06: [[-1.90, 0.33], [-1.38, 0.76], [-0.71, 1.53], [0.47, 2.73], [0.93, 2.92], [1.33, 2.92]],
    10.24: [[-1.38, 0.44], [-0.71, 1.06], [0.49, 2.27], [0.99, 2.52], [1.41, 2.54]],
    11.36: [[-1.38, 0.15], [-0.71, 0.61], [0.52, 1.64], [1.05, 1.97], [1.49, 2.02]],
    12.51: [[-0.71, 0.11], [0.55, 0.88], [1.11, 1.16], [1.59, 1.36]],
    13.67: [[0.39, 0.12], [1.67, 0.60]],
}  # fmt: skip
# The plate's seven ports a side, [x, sill, half-breadth], aft to forward (§5.4). Width and depth
# (§6.3): the mean width, and the mean opening from the sill to the rail's heavy line, in feet.
PORTS = [
    [-11.25, 1.20, 2.75], [-7.20, 1.03, 3.14], [-2.16, 0.95, 3.47], [0.97, 0.97, 3.60],
    [4.98, 1.11, 3.52], [8.80, 1.32, 2.99], [11.82, 1.53, 1.76],
]  # fmt: skip
PORT_WIDTH_M = 0.633
PORT_DEPTH_M = 2.68 * FT
# The ports no gun of either fit stands in, by their places in PORTS (ports 1, 3 and 5), and the
# places of the guns the privateer's two fits stand on, x forward of midships in the file's frame.
# No gun's x_m moves (Build-Ships.md §5.3), and every port gun stands on a triple of its deck (§4.4;
# truth 7-185): so a gun's port is a triple at the gun's x, on the same measured sill line, in place
# of the plate's port it was filed for (§6.3). The second port stands at two places, one for each
# fit, so the seven are eight triples.
PORTS_WITH_NO_GUN = (0, 2, 4)
GUN_PLACES = (-8.40, -7.50, 0.00, 8.40, 10.50)
# The transom's half-breadths, taffrail and knuckle, by the lines plate (the body plan's 2.35 and
# 2.37 m recorded, §5.9), and the foot's round up, measured on the body plan.
TRANSOM_HB = (7.40 * FT, 7.48 * FT)
ROUND_UP_M = 0.57 * FT

# The heights above the water take §6.2's two judged steps (`_Scale.z`), so every line that has one
# is judged; a line wholly under the water, and the knuckle, on the sill line itself, are not.
MARKS = {
    "rail_m": "judged",  # above the sill line, the sections' factor
    "breadth_m": "judged",  # the plan's thin outer line, taken for the rail
    "keel_m": "stand-in",
    "stem_m": "judged",  # above the water, §6.2's two steps
    "stern_m": "judged",  # above the water, §6.2's two steps
    "section_m": "judged",  # above the water, §6.2's two steps
    "decks_m": "judged",
    "ports_m": "judged",
    "port_size_m": "stand-in",
    "head_m": "judged",  # above the water, §6.2's two steps
    "breadth_line_m": "judged",
    "sections_m": "judged",  # above the water, §6.2's two steps
    "rabbet_m": "judged",  # above the water, §6.2's two steps
    "form.stern": "stand-in",
    "form.stern.knuckle_z_m": "stand-in",
    "form.stern.transom_hb_m": "stand-in",
    "form.stern.round_up_m": "stand-in",
    "form.head": "stand-in",
}

NOTES = {
    "profile": (
        "Her side, deck and ports (Build-Ships.md §5.1), one hull in the two schooners' files, one "
        "class in two roles (the owner, 2026-10-28; §5.0 principle 10). A stand-in for the type, "
        "S† (§5.7): Lynx's draught as H.M. schooner Musquidobit, taken off at Portsmouth in May "
        "1816, in Chapelle's redrawings (The Baltimore Clipper, 1930, fig. 17 and the two plates "
        "after p. 83), measured in docs/design/ships-design/pages-chapelle-fig17.md (the note "
        "below) and scaled by §5.0 principle 7 to this file's length and beam: lengths by the load "
        "lines, hers over Lynx's 26.84 m rabbet to rabbet; sections by the breadths, hers over "
        "Lynx's 24 ft 0 in extreme; 2 in of plank; the side's height from the plate's own lowest "
        "sill (the ports' note). Between the water and the sill line a height goes straight, above "
        "it by the sections' factor (judgement, the note's §6.2). x forward of the middle of the "
        "load line, z above the load water, metres. Her drawn depth and displacement are the "
        "generator's report, recorded beside the file's, not moved (principle 8). No wale and no "
        "rising line are drawn on the plates, so no line is given for either (read); the owner's "
        "photographs of the replica are for the eye only (§5.8)."
    ),
    "profile.rail_m": (
        "The rail cap's top on the sheer plan, taffrail to stem head (measured). The bulwark "
        "above the sill line keeps the plate's height by the sections' factor (judgement). A "
        "small cap stands higher at the taffrail; it is recorded in the note's §5.3 and not drawn."
    ),
    "profile.breadth_m": (
        "The half-breadth plan's load line and thin outer line (the rail: judgement), plank on, "
        "each on a plane square to the water. The last station stands in the stem: its water "
        "figure is the stem's half-siding."
    ),
    "profile.keel_m": (
        "The keel's lower edge, the post's heel to the forefoot (measured). The drag is Lynx's, "
        "kept, not the file's mean draught (principle 7)."
    ),
    "profile.stem_m": (
        "The stem's own fore edge (measured), up past the bowsprit's underside to the rail's fore"
        " end; the knee of the head stands apart in its own line."
    ),
    "profile.stern_m": (
        "The post's after edge, the post's head, the transom's lower corner and the taffrail "
        "(measured; between post and rudder a tentative reading of close lines). The drawn face "
        "rakes about 38 degrees from the upright (Build-Ships.md §5.7); the chord from the "
        "taffrail to the post's head, about 45 degrees, crosses the foot's band and is no drawn "
        "line. The rudder is not a line of this key."
    ),
    "profile.section_m": (
        "Station 13, the dead flat, keel to rail (measured): the body plan below and between the "
        "plate's waterlines, the keel's half-siding at its foot."
    ),
    "profile.decks_m": (
        "The deck at side: its middle line traced on the inboard plate, flush, less the class's "
        "round up of 5 1/2 in (Chapelle p. 168), since neither plate draws one (judgement; "
        "Steel's schooner has 5 in and Flying Fish about 11). So the line takes the word judged. "
        "deck_height_m stays this file's datum, never read from here (Build-Ships.md §5.5)."
    ),
    "profile.ports_m.upper": (
        "Each a port's x, its sill, and the sill line's half-breadth there (measured on the "
        "plate, plank on; forward of about station 16 the plan's heavy line stands inside the "
        "section at the sill's height, recorded in the note's §5.1). The lowest of the plate's "
        "sills, its 3 ft 1 in, stands where the plate has it (Build-Ships.md §5.4, as the lead "
        "ruled: her own sheet over a later ship's), Steel's schooner's figure to the inch, the "
        "sheer's rise above it by the length ratio. Spider's 3 ft 5 in of 1835 (Chapelle pp. "
        "166-167) is recorded in the note's §5.4. "
        "Departure: the plate has seven ports a side. No gun's x_m moves (§5.3) and every "
        "port gun stands on a triple (§4.4), so ports 1, 3 and 5, which no gun of either fit "
        "stands in, are the plate's, and the others stand at the guns' own places on the same "
        "sill line, the second at two places, one for each fit: eight triples for seven ports, "
        "so the line takes the word judged, and only the plate's three are named as measured. The "
        "two transom ports are no triples."
    ),
    "profile.port_size_m.upper": (
        "The plate's ports, the mean width and the mean opening from the sill to the rail's heavy"
        " line (measured): cut through the bulwark, with no port head below the rail."
    ),
    "profile.head_m": (
        "The knee of the head's fore edge, from where a joint leaves the stem to under the "
        "bowsprit (measured). A small knee with nothing standing on it: no figure, no rails, no "
        "trail boards (read)."
    ),
    "profile.breadth_line_m": (
        "The main breadth, stations 2 to 16: the widest of each section off the body plan "
        "(measured). The section is flat within an inch over a band, so its height is a smooth "
        "curve through the bands (judgement); no line on any sheet marks it. Abaft station 2 and "
        "forward of station 16 the section is widest at or above the sill line."
    ),
    "profile.sections_m": (
        "The sections by station, the rung's own points drawn through (principle 5): the plate's "
        "WL3, WL2 and sill line, the body plan between and below them (±0.15 ft below WL3, worse "
        "at stations 9 to 16, where the outer sections merge). Forward of about station 16 the "
        "sill line's point is the plan's heavy line, a little inside the section."
    ),
    "profile.rabbet_m": (
        "The heavier line of the pair, kept and not drawn (principle 11); tentative on the post, "
        "where the pair's order changes, and stepped at the heel."
    ),
    "profile.form": ("Her ends. No fullness: the ends are drawn through the sections."),
    "profile.form.stern": (
        "Raked and flat, with neither lights nor galleries on any sheet (read). The knuckle is "
        "the band's side, where the sill line ends; below the band the hull's short counter has "
        "no key. The transom's half-breadths are the lines plate's, plank on; the body plan and "
        "the deck plan's second line stand 0.1 m wider (recorded). The round up is the foot's. "
        "Its two ports are not triples: neither fit puts a gun in them."
    ),
    "profile.form.head": ('A small knee, "a small head for the gammoning" (Chapelle p. 83).'),
    "profile.marks": (
        "Each line's rung (§5.0 principle 4): stand-in for what is measured on Lynx's plates and "
        "scaled by principle 7's own factors; judged for each line whose weakest point is a "
        "judgement: every height above the water, by the steps in the profile's note, and the "
        "rail's half-breadth, the deck, the main breadth and the ports by their own notes."
    ),
}


class _Scale:
    """§5.0 principle 7 as the note's §6.2 has it: from Lynx's frame to the file's."""

    def __init__(self, length_m, beam_m):
        self.k_l = length_m / LYNX_LOAD_LINE_M
        self.k_b = beam_m / LYNX_BEAM_M

    def x(self, x):
        return x * self.k_l

    def hb(self, hb):
        """A half-breadth, the plank on."""
        return (hb + PLANK_M) * self.k_b

    def sill(self, x):
        """The sill line at Lynx's x: its lowest where the plate has it, its rise by the length
        ratio."""
        return LOWEST_SILL_PLATE_M + self.k_l * (interp(SILL_LINE, x) - LOWEST_SILL_PLATE_M)

    def z(self, x, z):
        """A height at Lynx's x: below the water by the sections' factor; between the water and the
        sill line straight, so that the water keeps its half-breadths and the side meets the sill
        line; above the sill line by the sections' factor (judgement, §6.2)."""
        if z <= 0.0:
            return z * self.k_b
        s = interp(SILL_LINE, x)
        if z <= s:
            return z * self.sill(x) / s
        return self.sill(x) + (z - s) * self.k_b

    def point(self, x, z):
        return [self.x(x), self.z(x, z)]


def _triples(scale):
    """The ports of her deck, aft to forward: the plate's where no gun stands, a gun's own place on
    the plate's sill line where one does (the note's §6.3, §6.4)."""
    plate = [
        [scale.x(PORTS[i][0]), scale.sill(PORTS[i][0]), scale.hb(PORTS[i][2])]
        for i in PORTS_WITH_NO_GUN
    ]
    heavy_line = [[x, hb] for x, _z, hb in SILL_LINE if hb is not None]
    guns = []
    for x in GUN_PLACES:
        lynx = x / scale.k_l
        guns.append([x, scale.sill(lynx), scale.hb(interp(heavy_line, lynx))])
    return sorted(plate + guns)


def _profile_parts(scale):
    """`g.hull_profile`'s arguments: the rail, the breadth, and the rest as parts."""
    xs = scale.x
    rail = [scale.point(x, z) for x, z in RAIL]
    last = BREADTH[-1]
    breadth = [[xs(x), scale.hb(w), scale.hb(r)] for x, w, r in BREADTH[:-1]]
    breadth.append([xs(last[0]), last[1] * scale.k_b, scale.hb(last[2])])
    sections = []
    for x, points in SECTIONS.items():
        for i, (z, hb) in enumerate(points):
            siding = x == BREADTH[-1][0] and i == 0
            sections.append([xs(x), scale.z(x, z), hb * scale.k_b if siding else scale.hb(hb)])
    section = [
        [scale.z(SECTION_X, z), hb * scale.k_b if i < SECTION_SIDING_POINTS else scale.hb(hb)]
        for i, (z, hb) in enumerate(SECTION)
    ]
    parts = {
        "keel": [scale.point(x, z) for x, z in KEEL],
        "stem": [scale.point(x, z) for x, z in STEM],
        "stern": [scale.point(x, z) for x, z in STERN],
        "section": section,
        "decks": {"upper": [scale.point(x, z) for x, z in DECK_SIDE]},
        "ports": {"upper": _triples(scale)},
        "port_size": {"upper": [PORT_WIDTH_M * scale.k_l, PORT_DEPTH_M * scale.k_b]},
        "head": [scale.point(x, z) for x, z in HEAD],
        "breadth_line": [[xs(x), scale.z(x, z), scale.hb(hb)] for x, z, hb in MAIN_BREADTH],
        "sections": sections,
        "rabbet": [[xs(x), scale.z(x, z), hs * scale.k_b] for x, z, hs in RABBET],
    }
    return rail, breadth, parts


def add_hull(b, file_word):
    """Her profile, form and marks as the hull's last key, and each line's note, through the
    generator's helpers (Build-Ships.md §5.3). What the rules compute from the file's own keys goes
    to the generator's report on the standard error, under `file_word`, never into a note (the
    lead's ruling)."""
    hull = b.doc["hull"]
    scale = _Scale(hull["length_waterline_m"], hull["beam_m"])
    rail, breadth, parts = _profile_parts(scale)
    hull["profile"] = g.hull_profile(rail, breadth, **parts)
    form = {
        "stern": {
            "type": "raked",
            "knuckle_z_m": scale.z(*KNUCKLE),
            "transom_hb_m": [scale.hb(hb) for hb in TRANSOM_HB],
            "round_up_m": ROUND_UP_M * scale.k_b,
        },
        "head": "knee",
    }
    report = []
    # the plate's three ports are measured, so a gap over 0.05 m raises for each; the five at the
    # guns' places are reported, as the cutter's three, and her test holds them all the same (§6.3)
    measured = [("upper", round(scale.x(PORTS[i][0]), 2)) for i in PORTS_WITH_NO_GUN]
    g.hull_form(hull, form=form, marks=MARKS, measured=measured, report=report)
    b.hull_notes.update(NOTES)
    print("\n".join(f"{file_word}: {line}" for line in report), file=sys.stderr)


def port_sill(hull, x):
    """The sill of the port at a gun's x, from the hull's own triples: a port gun stands on a triple
    of its deck, and no gun's place moves (Build-Ships.md §4.4, §5.3)."""
    for tx, sill, _hb in hull["profile"]["ports_m"]["upper"]:
        if abs(tx - x) < 0.005:
            return sill
    raise ValueError(f"the schooners' upper deck has no port at x {x:g}: a gun's x_m never moves.")


def rail_z(hull, x):
    """The top of the side at a pivot's or a swivel's x (Build-Ships.md §5.3)."""
    return round(interp(hull["profile"]["rail_m"], x), 2)


def on_the_rail(hull, guns):
    """Rail guns as `g.swivels` makes them, each set on the rail at its own x."""
    for gun, _note in guns:
        gun["height_m"] = rail_z(hull, gun["x_m"])
    return guns
