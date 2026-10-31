"""The smack's hull as drawn (package 75, SW-2 with SW-2b.2; docs/design/Build-Ships.md §5.0 to
§5.3, §5.7): her measured points, and her profile and form through `g.hull_profile` and
`g.hull_form`, as the 64's and the razee's are built (`tools/ships/indefatigable.py`). `smack()`
in `tools/gen_ships.py` calls `add_her_lines` from one place.

Her rung is S† (§5.0 principle 3), each line's word its weakest point's (principle 4): Chapman's
Architectura Navalis Mercatoria (1768),
Pl. LIX No. 3, the English smack, is of her type and not the *Culloden*. The plate gives the water,
the main breadth and the rail by station, the midship section, the keel, the stem, the stern, the
wale, the deck and its own nine frames, the body above and under the water (§5.0 principle 5;
§5.7). Steel's coasting sloop of 60 tons (1805, bodies p. 27) is kept beside them as a check. No
port and no gun is drawn on the plate or in the table, and the file has no gun, so she has no port
triple and no sill (§5.4; §9.1). The stern is raked and rounded, at the plate's own 0.78 m; she has
no head. The figures are the pages note's, docs/design/ships-design/pages-chapman-pl59.md (a `§`
below with no document named is that note's). The Cooke etching of 1829 in docs/references/images/
is for the eye only (§5.8) and gave no point.

**The ruling (the lead, 2026-10-31): the plate's own frames, sourced points over the rule.** §5.7 as
first written put the sloop under the water between the plate's stations, only the plate's midship
section having been read then. The plate's body plan reads whole at the same rung (§4.10, §5.2), and
beside it the sloop is a fuller, deeper body: it does not run fair into the plate's water or its
midship section, and its timbers end on a flat foot, a metre out from the middle line, since the
table gives no lower point and the plate's keel leaves no room for one (§5.2). So `UNDER_WATER` is
"plate", and §5.7's row says so. Both bodies are kept here (§5.0 principle 11), each drawn from one
word, and the hull above the water is the same to the eye under either. The plate's frames draw her
18% under her filed displacement, past §5.0 principle 8's 15%: reported past the line, not moved.

Drawn only (§5.0 principle 8): nothing the physics, the guns or the lee ports read comes from
these lines, and no figure of her file moves for them. What a rule computes from the file's own
keys, the drawn displacement and depth and the keel's drop below the water, goes to the
generator's report (`REPORT`) and her tests, never to a note (the lead's notes of 2026-10-29,
item 2).
"""

from __future__ import annotations

import sys

import gen_ships as g

# Which body stands under the water (the module's docstring): "plate", the plate's own frames, as
# the lead ruled on 2026-10-31; "steel", §5.7 as first written, kept as a check.
UNDER_WATER = "plate"

SWEDISH_FT = 0.2969  # m (§0, Units and datums)

# The plate's own figures at its own size, for principle 7's ratios (§3, §2.3): its load water
# line's length, measured, and its moulded breadth, the dashed sides of its body plan.
PLATE_WATER_M = 11.46
PLATE_BEAM_M = 4.06
# The sloop's for hers (§5.2): her water length, Folio I's row C (judgement, ±1 ft), and her
# extreme breadth, in feet.
SLOOP_WATER_FT = 52.0
SLOOP_BEAM_FT = 16.0 + 8.0 / 12.0
# The side has no source of its own for her (principle 7 asks the sills', and she has none,
# §4.16): the rail's lowest by the beams' ratio, its rise above it by the waterlines' (judgement,
# §5.3).
RAIL_LOWEST_FT = 4.49

# The plate's stations, feet forward of the mid-perpendiculars along the keel (§4.2). H's line is
# 16.38 (corrected: first 16.32); ⊕ is the middle of its two lines, ±0.03.
STATION_X_FT = {
    "14": -16.85,
    "12": -13.81,
    "9": -9.22,
    "6": -4.58,
    "3": 0.02,
    "⊕": 4.34,
    "C": 8.65,
    "F": 13.27,
    "H": 16.38,
}
# Frame H is drawn at its own place, forward of its station line: its water lines, its breadth
# and its head fit the plan's lines at x 16.42 to 16.59, mean 16.47 (§2.5; judgement).
FRAME_X_FT = dict(STATION_X_FT, H=16.47)

# The rail's top line, x, z above the LWL (§4.3, §4.14): the taffrail's sweep to the rail's end,
# the rail by station, and its stop at the stem head's after edge, then that edge's top (§4.5).
RAIL_FT = (
    (-22.42, 6.54),
    (-21.67, 6.08),
    (-21.46, 5.83),
    (-21.29, 5.60),
    (-20.83, 5.52),
    (-19.58, 5.36),
    (-18.33, 5.21),
    (-16.83, 5.05),
    (-13.79, 4.81),
    (-9.20, 4.57),
    (-4.56, 4.49),
    (0.04, 4.58),
    (4.36, 4.79),
    (8.68, 5.22),
    (13.30, 5.90),
    (16.35, 6.54),
    (17.43, 6.83),
    (18.13, 7.04),
    (18.16, 8.26),
)

# Half-breadths from the half-breadth plan (§4.6, §4.9): (the rail, the load water line). At 3 and
# ⊕ the water's is the plan's one light line, the main breadth's (judgement, §4.6).
HALF_BREADTH_FT = {
    "14": (4.31, 3.27),
    "12": (4.98, 4.92),
    "9": (5.72, 5.99),
    "6": (6.18, 6.56),
    "3": (6.39, 6.78),
    "⊕": (6.43, 6.85),
    "C": (6.31, 6.66),
    "F": (5.68, 5.34),
    "H": (4.22, 2.54),
}
# The lines beyond the stations (§4.6): x, the water, the top of the side. Aft, the water closes on
# the post's half-siding at x -18.40 (§4.6, the review's reading).
BEYOND_AFT_FT = (
    (-18.40, 0.26, 3.87),
    (-18.20, 0.56, 3.93),
    (-17.97, 1.36, 4.00),
    (-17.55, 2.40, 4.12),
    (-17.13, 3.00, 4.24),
)
# The lines between two stations, where the run and the entry curve and a straight line from station
# to station stands inside the plan by more than principle 2's 2 px (§4.6, the review's reading): x,
# the water, the rail. At 11.50 the two lie as one.
BETWEEN_FT = ((-15.40, 4.30, 4.67), (11.50, 6.07, 6.07), (14.70, 4.33, 5.20))
# Forward of the rail's stop the top of the side is the stem head's, at its half-siding.
HEAD_HALF_SIDING_FT = 0.30
BEYOND_FORE_FT = (
    (16.96, 1.85, 3.74),
    (17.37, 1.31, 3.32),
    (17.43, 1.25, 3.23),  # at the rail's point, between the lines either side (arithmetic)
    (17.79, 0.87, 2.67),
    (18.13, 0.53, HEAD_HALF_SIDING_FT),
    (18.16, 0.50, HEAD_HALF_SIDING_FT),
    (18.21, 0.45, HEAD_HALF_SIDING_FT),
    (18.41, 0.26, HEAD_HALF_SIDING_FT),
    (18.72, 0.26, HEAD_HALF_SIDING_FT),
)
# The rail on forward of its stop, along the head's side (§4.5, §4.6): x, z, half-breadth, measured
# on the plan's rail line and the profile's; it closes on the head's half-siding about x 18.72. The
# side stands plumb under it, the main breadth and the rail lying as one there, for the second
# band's height (§4.6). So the head stands up narrow out of the bow, not as wide as the rail: each
# station steps in from the rail's top to the head's side, 18.13's a step under the rail's stop.
BOW_RAIL_FT = (
    (18.13, 6.98, 2.00),
    (18.16, 7.05, 1.93),
    (18.21, 7.06, 1.82),
    (18.41, 7.12, 1.30),
    (18.62, 7.18, 0.63),
)
BAND_BELOW_RAIL_FT = 0.70
HEAD_STEP_FT = 0.06  # how the head's side is drawn from the rail's top: all but plumb

KEEL_FT = ((-18.39, -6.52), (17.49, -4.88))  # its lower edge, straight (§4.5)
STEM_FT = (  # its fore edge, the forefoot to the head's fore top (§4.5)
    (17.49, -4.88),
    (17.77, -4.53),
    (18.41, -3.54),
    (18.75, -2.66),
    (18.98, -1.79),
    (19.15, -0.92),
    (19.27, 0.00),
    (19.36, 0.81),
    (19.43, 1.68),
    (19.49, 2.97),
    (19.51, 4.70),
    (19.50, 6.85),
    (19.47, 8.68),
)
STERN_FT = (  # the post's after edge, the counter, the foot, the taffrail at the middle line (§4.5)
    (-18.39, -6.52),
    (-18.60, -5.05),
    (-18.84, -3.33),
    (-19.08, -1.62),
    (-19.31, 0.00),
    (-19.59, 2.29),
    (-20.89, 2.91),
    (-21.30, 3.27),
    (-22.44, 6.54),
)
WALE_FT = (  # x, lower, upper (§4.2): the upper line's end on the counter's curve, the post's
    # scroll, on to its square cut at the stem
    (-19.18, 2.00, 2.03),
    (-18.34, 1.02, 1.93),
    (-16.85, 0.95, 1.77),
    (-13.81, 0.70, 1.53),
    (-9.22, 0.47, 1.31),
    (-4.58, 0.40, 1.25),
    (0.02, 0.49, 1.35),
    (4.34, 0.70, 1.57),
    (8.65, 1.09, 1.97),
    (13.27, 1.77, 2.66),
    (16.38, 2.40, 3.29),
    (18.89, 3.11, 4.04),
)
BAND_FT = (  # the second band, end to end, foot and top (§4.2), as the channel wale (judgement)
    (-20.96, 4.57, 4.83),
    (-16.85, 4.06, 4.36),
    (-13.81, 3.85, 4.09),
    (-9.22, 3.61, 3.87),
    (-4.58, 3.54, 3.79),
    (0.02, 3.60, 3.88),
    (4.34, 3.82, 4.09),
    (8.65, 4.26, 4.52),
    (13.27, 4.97, 5.20),
    (16.38, 5.58, 5.84),
    (18.86, 6.28, 6.54),
)
# The deck at side (§4.4): the after deck, then the fore deck; the waist between has no line.
DECK_FT = (
    (-20.32, 2.62),
    (-19.49, 2.62),
    (-18.23, 2.58),
    (-16.85, 2.55),
    (-16.14, 2.52),
    (-14.47, 2.49),
    (-14.26, 2.48),
    (-6.00, 3.05),
    (-4.58, 3.07),
    (-3.07, 3.10),
    (-0.56, 3.16),
    (0.02, 3.17),
    (4.34, 3.38),
    (6.55, 3.54),
    (8.65, 3.72),
    (11.57, 4.02),
    (13.27, 4.23),
    (14.71, 4.42),
    (16.38, 4.68),
    (17.85, 4.96),
)
# The main breadth by station (§4.11): z, the middle of the band at the frame's greatest
# half-breadth, and that half-breadth, the plan's but at H, whose frame's own stands at its own
# place (4.39; the plan's 4.41 at its station line).
MAIN_BREADTH_FT = {
    "14": (2.15, 4.59),
    "12": (1.77, 5.37),
    "9": (1.38, 6.13),
    "6": (0.91, 6.56),
    "3": (0.60, 6.78),
    "⊕": (1.04, 6.85),
    "C": (1.32, 6.72),
    "F": (2.69, 6.05),
    "H": (4.32, 4.39),
}
# The main breadth between F and H, where the plan's line stands 0.2 ft outside the straight (§4.6):
# x, its half-breadth; its height straight between the frames' (arithmetic).
MAIN_BREADTH_BETWEEN_FT = (14.70, 5.51)

# The frames (§4.10), its table as it stands: z, then the half-breadth at each station, "-" where
# the frame has ended.
FRAME_STATIONS = ("14", "12", "9", "6", "3", "⊕", "C", "F", "H")
FRAMES_TABLE = """
 4.00     -  5.18  5.87  6.28  6.53  6.64  6.57  5.99  4.39
 3.00  4.57  5.31  6.04  6.46  6.70  6.79  6.68  6.05  4.27
 2.00  4.60  5.36  6.12  6.54  6.76  6.83  6.71  6.03  3.88
 1.00  4.40  5.32  6.13  6.58  6.79  6.84  6.71  5.84  3.20
 0.50  4.05  5.17  6.08  6.56  6.79  6.84  6.69  5.63  2.79
-0.58  1.60  4.29  5.74  6.41  6.74  6.80  6.53  4.83  1.90
-1.17  0.70  3.23  5.27  6.21  6.62  6.70  6.32  4.20  1.43
-1.74  0.52  1.93  4.60  5.86  6.41  6.52  5.97  3.51  1.02
-2.33  0.41  1.19  3.61  5.25  6.03  6.20  5.43  2.74  0.61
-2.80  0.36  0.93  2.69  4.54  5.56  5.76  4.75  2.01  0.38
-3.20  0.31  0.75  2.02  3.74  4.94  5.18  3.92  1.43  0.22
-3.60  0.28  0.61  1.47  2.80  4.05  4.27  2.81  0.89  0.15
-3.90  0.25  0.52  1.13  2.11  3.16  3.23  1.83  0.53     -
-4.20  0.23  0.44  0.85  1.48  2.10  1.95  0.85     -     -
-4.50  0.21  0.37  0.61  0.94  1.08     -     -     -     -
-4.80  0.19  0.30  0.40  0.48     -     -     -     -     -
-5.10  0.18  0.24  0.22     -     -     -     -     -     -
-5.40  0.18     -     -     -     -     -     -     -     -
"""
# Each frame's foot on the rabbet, z and half-breadth, where the frame reaches it (§4.10, §4.12).
FRAME_FOOT_FT = {
    "14": (-5.58, 0.21),
    "12": (-5.44, 0.21),
    "9": (-5.23, 0.23),
    "6": (-5.02, 0.25),
    "3": (-4.82, 0.27),
    "⊕": (-4.62, 0.28),
    "C": (-4.42, 0.28),
    "F": (-4.19, 0.28),
}

# The rabbet's upper line along the keel and up the stem, x, z (§4.12), and its half-siding, taken
# along her (judgement).
RABBET_FT = (
    (-16.85, -5.58),
    (-13.81, -5.44),
    (-9.22, -5.23),
    (-4.58, -5.02),
    (0.02, -4.82),
    (4.34, -4.62),
    (8.65, -4.42),
    (12.00, -4.27),
    (13.17, -4.20),
    (14.33, -4.03),
    (15.47, -3.70),
    (16.53, -3.13),
    (17.42, -2.30),
    (17.97, -1.20),
    (18.26, -0.02),
    (18.44, 1.18),
    (18.53, 2.39),
)
RABBET_HALF_SIDING_FT = 0.23
# The floor's line, reserved and not drawn (§4.13, §5.1): the station, z from the profile's heavy
# curve, half-breadth from the frame's crossing of the diagonal. The nearest the plate has to a
# rising line (judgement).
FLOOR_FT = (
    ("14", -0.97, 0.93),
    ("12", -1.91, 1.77),
    ("9", -2.89, 2.69),
    ("6", -3.49, 3.31),
    ("3", -3.79, 3.74),
    ("⊕", -3.80, 3.87),
    ("C", -3.38, 3.60),
    ("F", -2.33, 2.71),
    ("H", -1.16, 1.46),
)
# The stern's form (§4.14). The transom's half-breadth at the rail's end and at its foot stand at
# the plate's own size, in metres, as §5.7 names the first, not carried by the beams' ratio (0.83
# and 0.98 m if they were; the 5 cm is under principle 2's 2 px). The foot's height and its round-up
# are feet, on `stern_m`.
TRANSOM_HB_M = (0.78, 0.93)
KNUCKLE_FT = 2.91
ROUND_UP_FT = 0.36

# Steel's coasting sloop of 60 tons, tables p. 27, as read (§5.2; pages-steel-1805-bodies.md §3.3):
# x on her judged length of 50 ft 3 in, metres; every other figure feet and inches. Timber 4's
# third diagonal goes in as 8 4¼, the fair figure, not the printed 7 4¼ (judgement, §5.2).
STEEL_SLOOP = {
    "water": [[-7.66, "8 7"], [7.66, "6 7"]],
    "diagonals": [
        ["4 6", ["4 11½", "0 0"]],
        ["5 10½", ["6 4½", "0 0"]],
        ["7 7", ["8 3", "0 10½"]],
        ["9 4", ["8 3", "3 2½"]],
        ["12 3", ["8 3", "4 9"]],
    ],
    "timbers": [  # name, x, lower height of breadth, upper, main half-breadth, down the diagonals
        ["13", -6.59, "9 4½", "9 8¼", "6 2", [None, "0 9", "1 10", "3 8", "6 11"]],
        ["12", -5.94, "8 8½", "9 3", "6 6", ["1 3¼", "2 2", "3 7", "5 5", "7 10"]],
        ["10", -4.66, "7 8", "8 6", "7 0", ["2 8", "3 9", "5 5", "7 2", "9 0½"]],
        ["8", -3.42, "6 10½", "8 0", "7 5", ["3 9", "5 0", "6 8", "8 1", "9 9"]],
        ["6", -2.11, "6 4", "7 7", "7 9¼", ["4 7", "6 0", "7 9", "8 11", "10 4"]],
        ["4", -0.85, "6 0½", "7 4", "7 11½", ["5 3", "6 9", "8 4¼", "9 4", "10 8¾"]],
        ["2", 0.47, "5 10½", "7 2½", "8 1", ["5 8", "7 2", "8 9", "9 7", "10 10"]],
        ["O", 1.74, "5 10", "7 2", "8 3", ["5 11", "7 5", "9 0", "9 10", "11 0"]],
        ["A", 2.87, "6 1½", "7 4½", "8 2½", ["5 9½", "7 3½", "8 11", "9 9", "10 11½"]],
        ["C", 4.17, "6 7", "7 8", "7 11½", ["5 2¾", "6 8½", "8 4", "9 3", "10 6"]],
        ["E", 5.44, "7 4", "8 3", "7 3", ["4 2¾", "5 7", "7 2¼", "8 2¾", "9 6"]],
        ["F", 6.08, "7 11¾", "8 7", "6 5", ["3 1½", "4 4", "6 0", "7 1", "8 5"]],
        ["G", 6.72, "8 9", "9 1", "4 9", ["1 1", "2 3", "3 8", "4 10", "6 2½"]],
    ],
}
# Steel's timber O, her dead flat, falls within 3 cm of the plate's ⊕ at her length; the plate's
# section stands there and hers is left out (§5.7, "the plate's section ruling at midships").
SLOOP_DEAD_FLAT = "O"

# Each line's rung (§5.0 principles 3, 4): S† where the whole of it is the plate's or the table's by
# principle 7's factors; judged where its weakest point is a judgement, which its note names. The
# side's height is judged, so every line that ends on the rail takes that word (the note's §5.1).
MARKS = {
    "rail_m": "judged",  # the side's height, her having no sill
    "breadth_m": "judged",  # the water at 3 and ⊕
    "keel_m": "stand-in",
    "stem_m": "judged",  # above the rail's lowest, the side's height
    "stern_m": "judged",  # the taffrail, the side's height
    "wales_m": "judged",  # which band is the main wale
    "section_m": "judged",  # its top, the rail, the side's height
    "decks_m": "judged",
    "breadth_line_m": "judged",  # frame H's place
    "sections_m": "judged",  # frame H's place; the rail along the head, the side's height
    "channel_wales_m": "judged",
    "floor_m": "judged",
    "rabbet_m": "judged",
    "form.stern": "stand-in",
    "form.stern.knuckle_z_m": "stand-in",
    "form.stern.transom_hb_m": "judged",  # the plate's own, not carried by the beams' ratio
    "form.stern.round_up_m": "stand-in",
    "form.head": "stand-in",
}

NOTES = {
    "profile": "Her lines, drawn only (Build-Ships.md §5; §5.7): Chapman 1768, Architectura "
    "Navalis Mercatoria, Pl. LIX No. 3, the English smack, of her type and not a vessel of hers "
    "(docs/design/ships-design/pages-chapman-pl59.md, 'the note' below), carried to her by §5.0 "
    "principle 7: every x by the ratio of the waterlines, hers to the plate's 11.46 m; every "
    "half-breadth and every height of the body by the ratio of the beams, hers to the plate's "
    "4.06 m moulded. x forward of the plate's mid-perpendiculars along the keel and z above its "
    "top water line, taken as her load line (judgement, the note's §3), square to the keel, in the "
    "plate's own frame, not turned level with the water. Feet in these notes are Swedish feet of "
    "0.2969 m (the note's Units and datums). No figure the physics or the guns read comes from "
    "these lines; where they differ from the file it is recorded, not moved.",
    "profile.rail_m": "The top of the side, from the taffrail's sweep to the stem head (the note's "
    "§4.3, §4.5, §4.14), its last two points the rail's stop at the head's after edge and the "
    "head's top there. Its height is judged: principle 7 takes her side from her own source for "
    "the sills and she has none, so the rail's lowest by the beams' ratio, with the frames it "
    "stands on, and its rise by the waterlines'.",
    "profile.breadth_m": "The half-breadths at the water and at the top of the side, read on the "
    "plate's half-breadth plan by station, between them where its lines curve most, and beyond "
    "(the note's §4.6, §4.9). Moulded, no plank added, "
    "so that the drawn hull is her file's beam (principle 7's last sentence). At stations 3 and ⊕ "
    "the water's is the "
    "plan's one light line, the main breadth's (judgement; the frames at the water agree). From "
    "the rail's stop forward the top of the side is the stem head, at its half-siding; the rail "
    "runs on along it in sections_m (the note's §4.6).",
    "profile.keel_m": "The keel's lower edge, straight from the post's heel to the forefoot (the "
    "note's §4.5, §4.12). Her drawn drag and depth are the plate's and are recorded, not moved.",
    "profile.stem_m": "The stem's fore edge, plumb from about 1 m above the water and squared off "
    "at the head (the note's §4.5); above the rail's lowest, heights by the side's rule, as the "
    "rail's.",
    "profile.stern_m": "The post's after edge, the counter meeting it, the transom's foot at its "
    "corner and at the middle line, and its raked face to the taffrail at the middle line (the "
    "note's §4.5, §4.14); the taffrail's height by the side's rule, as the rail's.",
    "profile.wales_m": "The side's band with the heavy lower edge, ending on the counter's curve "
    "above a scroll at the post and cut square at the stem, drawn heavy across the body plan (the "
    "note's §4.1, §4.2). That it is the main wale is judgement on Steel's rule, its lower edge a "
    "few inches above the load line; the other band is a moulding a quarter of its depth.",
    "profile.section_m": "The plate's ⊕ frame, moulded, the mean of its two halves, from the "
    "rabbet to the rail (the note's §4.10). No plank is added, so that the drawn hull is her "
    "file's beam (principle 7's last sentence). The rail at its top by the side's rule, as the "
    "rail's.",
    "profile.decks_m.upper": "The deck at side (the note's §4.4): the plate's after deck from the "
    "transom and its fore deck to the stem, joined straight across the waist, where no deck line "
    "is drawn, the plate's dashed outline there not identified (judgement: no other deck word fits "
    "an open waist). The file's deck_height_m stays its own datum, recorded, not moved.",
    "profile.breadth_line_m": "The plate's main breadth by station, its height the middle of the "
    "band within 0.015 ft of each frame's greatest half-breadth, ±0.4 ft (the note's §4.11); "
    "Steel's stands lower and is not drawn (§5.7: the plate's). H at its frame's own place, not "
    "its station line's (the note's §2.5, judgement); one point between F and H, its height "
    "straight between theirs (the note's §4.6, arithmetic).",
    "profile.channel_wales_m": "The plate's second band, end to end, on which its channel lies "
    "(the note's §4.1, §4.2); that it stands for a channel wale is judgement. No channel key "
    "exists; the channel and its three deadeyes a side are in the note's §4.8.",
    "profile.floor_m": "Reserved, not drawn: the plate's one diagonal, the nearest it has to a "
    "rising line (judgement): z on the profile's heavy curve, the half-breadth at the frame's "
    "crossing (the note's §4.13).",
    "profile.rabbet_m": "Reserved, not drawn: the upper of the two close lines along the keel and "
    "up the stem, taken as the rabbet's upper edge, the half-siding 0.23 ft along her (judgement; "
    "the note's §4.12).",
    "profile.form": "No fullness: the sections_m draw the ends.",
    "profile.form.stern": "Raked and rounded above a short rounded counter (the note's §4.14), as "
    "§5.7 gives it. The transom's half-breadths are the plate's own, 2.64 ft at the rail's end and "
    "3.12 ft at the foot, as §5.7 names the first, not carried by the beams' ratio (judgement, the "
    "difference under principle 2's 2 px); the knuckle is the foot at its corner and the round-up "
    "the foot's rise to the middle line. No galleries and no lights: none is drawn, and her type "
    "did not certainly carry them (§5.0 principle 9).",
    "profile.form.head": "None: the stem stands up squared, with no knee, rails, figure or billet "
    "(the note's §4.16).",
    "profile.marks": "Each line's rung (Build-Ships.md §5.0 principles 3 and 4): stand-in, S†, her "
    "type's plate or table and not a vessel of hers, scaled; judged, a judgement at its weakest "
    "point, which its note names.",
}
BOW_NOTE = (
    "Last, the plate's rail on along the stem head's side, its heights by the side's rule, so that "
    "the head stands up narrow out of the bow (the note's §4.6)."
)
SECTIONS_NOTES = {
    "steel": "Above the water, the plate's frames (the note's §4.10; Build-Ships.md §5.0 principle "
    "5), at the sloop's timbers, straight between the stations either side (arithmetic). Under the "
    "water, §5.7 as first written: Steel 1805's coasting sloop of 60 tons, tables p. 27 "
    "(ships-design/pages-steel-1805-bodies.md §3.3) through g.from_steel_table, x by the ratio "
    "of the waterlines, hers to the sloop's judged 52 ft, and the rest by the ratio of the beams, "
    "hers to the sloop's 16 ft 8 in; its points below the water alone, its timber O left out for "
    "the plate's ⊕ frame, which rules at midships, as read but for timber 4's third diagonal (8 "
    "4¼ for the printed 7 4¼, judgement). The other body, kept as a check: the plate's own frames "
    "are the body as ruled; the sloop is another vessel in form, fuller and deeper under the "
    "water; it does not run fair into the plate's water or its section, and its timbers end on a "
    "flat foot (the note's §2.5, §5.2). " + BOW_NOTE,
    "plate": "The plate's nine frames by station, from the body plan (the note's §4.10), each "
    "moulded, low to high, frame H at its own place (judgement, the note's §2.5); they meet the "
    "half-breadth plan's three water lines and the second photograph (the note's §2.5). Sourced "
    "points over the rule, at the same rung as Steel's coasting sloop of 60 tons, which §5.7 first "
    "wrote here: ruled by the lead (the note's "
    "§5.2), and the sloop's rows are kept in tools/ships/hull_smack.py as a check. " + BOW_NOTE,
}

# The generator's report: what a rule computes from the file's own keys (the module's docstring).
REPORT: list[str] = []


def frames_ft() -> dict[str, list[tuple[float, float]]]:
    """The frames of `FRAMES_TABLE` by station, feet, (z, half-breadth), low to high, each foot on
    the rabbet first where it has one."""
    rows = [line.split() for line in FRAMES_TABLE.strip().splitlines()]
    frames = {}
    for i, station in enumerate(FRAME_STATIONS, start=1):
        points = sorted((float(r[0]), float(r[i])) for r in rows if r[i] != "-")
        frames[station] = ([FRAME_FOOT_FT[station]] if station in FRAME_FOOT_FT else []) + points
    return frames


def plate_section(body, side) -> list[list[float]]:
    """The ⊕ frame as `section_m`, [z, half-breadth], low to high: its foot on the rabbet, the
    frame, the water at the plan's half-breadth and the rail at the frame's head."""
    points = [[body(z), body(hb)] for z, hb in frames_ft()["⊕"]]
    upper = next(i for i, (z, _hb) in enumerate(points) if z > 0.0)
    rail, water = HALF_BREADTH_FT["⊕"]
    points.insert(upper, [0.0, body(water)])
    points.append([side(4.79), body(rail)])
    return points


def plate_frames(x_m, body) -> list[list[float]]:
    """The plate's nine frames as `sections_m`, [x, z, half-breadth] (§4.10, §5.3), each station
    low to high: the body as ruled."""
    return [
        [x_m(FRAME_X_FT[station]), body(z), body(hb)]
        for station, points in frames_ft().items()
        for z, hb in points
    ]


def steel_body(hull: dict, x_mid: float, section, x_m, body) -> list[list[float]]:
    """§5.7 as first written, the check, as `sections_m`: the sloop's table through
    `g.from_steel_table`, by its own ratios (§5.2), under the water alone; its dead flat left out,
    and the plate's ⊕ frame at midships, x `x_mid`, in its place, `section` being that frame as
    `section_m`; above the water, the plate's frames (`frames_above_water`)."""
    length_ratio = hull["length_waterline_m"] / (SLOOP_WATER_FT * g.FT)
    beam_ratio = hull["beam_m"] / (SLOOP_BEAM_FT * g.FT)
    parts, _marks = g.from_steel_table(
        STEEL_SLOOP, length_ratio=length_ratio, beam_ratio=beam_ratio
    )
    dead_flat = next(t[1] for t in STEEL_SLOOP["timbers"] if t[0] == SLOOP_DEAD_FLAT)
    dead_flat = round(dead_flat * length_ratio, 2)
    below = [p for p in parts["sections"] if p[1] < 0.0 and p[0] != dead_flat]
    mid = [[x_mid, z, hb] for z, hb in section if z < 0.0]
    above = frames_above_water(x_m, body, sorted({p[0] for p in below} | {x_mid}))
    return sorted(below + mid + above, key=lambda p: (p[0], p[1]))


def plan_off_straight(ft, ft0, ft1) -> tuple[float, float]:
    """How far the plan's water and rail stand off the straight between two stations, `ft0` and
    `ft1`, at `ft`, all in feet."""
    from freesail.ship.profile import interp

    plan = sorted(
        BEYOND_AFT_FT
        + BETWEEN_FT
        + tuple((STATION_X_FT[st], w, r) for st, (r, w) in HALF_BREADTH_FT.items())
    )
    t = (ft - ft0) / (ft1 - ft0)

    def off(i):
        line = [(p[0], p[i]) for p in plan]
        return interp(line, ft) - (interp(line, ft0) * (1.0 - t) + interp(line, ft1) * t)

    return off(1), off(2)


def frames_above_water(x_m, body, timbers) -> list[list[float]]:
    """The plate's frames above the water, for the sloop's body, which has none of its own there
    (§5.0 principle 5), as `sections_m` at the sloop's `timbers`, x in metres, since a station with
    a point given is carried from no other: as read where a timber falls on a station, else straight
    between the two stations either side at each height both reach, moved by how far the plan's
    water and rail stand off the straight there (arithmetic). The stations between the timbers are
    then carried from them, above the water and below it alike (`freesail/ship/form.py`)."""
    from freesail.ship.profile import interp

    frames = {st: dict(pts) for st, pts in frames_ft().items()}
    places = [(st, round(x_m(FRAME_X_FT[st]), 2)) for st in FRAME_STATIONS]
    points = []
    for x in timbers:
        on = [st for st, place in places if place == x]
        if on:
            points += [[x, body(z), body(hb)] for z, hb in frames[on[0]].items() if z > 0.0]
            continue
        i = next(k for k, (_st, place) in enumerate(places) if place > x)
        (st0, x0), (st1, x1) = places[i - 1], places[i]
        t = (x - x0) / (x1 - x0)
        ft = x / x_m(1.0)
        off_water, off_rail = plan_off_straight(ft, FRAME_X_FT[st0], FRAME_X_FT[st1])
        top = interp(RAIL_FT, ft)
        for z in sorted(frames[st0].keys() & frames[st1].keys()):
            if z > 0.0:
                hb = frames[st0][z] + (frames[st1][z] - frames[st0][z]) * t
                points.append([x, body(z), body(hb + off_water + (off_rail - off_water) * z / top)])
    return points


def bow_rail(x_m, side, body) -> list[list[float]]:
    """The rail forward of its stop, as `sections_m`: each station the plumb side under it, its top
    and the head's side rising from it."""
    points = []
    for x, z, hb in BOW_RAIL_FT:
        points += [
            [x_m(x), side(z - BAND_BELOW_RAIL_FT), body(hb)],
            [x_m(x), side(z), body(hb)],
            [x_m(x), side(z + HEAD_STEP_FT), body(HEAD_HALF_SIDING_FT)],
        ]
    return points


def breadth_line(x_m, body) -> list[list[float]]:
    """The main breadth as `breadth_line_m`: by station at each frame's own place, and the one point
    between F and H, its height straight between theirs."""
    line = [[FRAME_X_FT[st], z, hb] for st, (z, hb) in MAIN_BREADTH_FT.items()]
    x, hb = MAIN_BREADTH_BETWEEN_FT
    (x0, z0, _h0), (x1, z1, _h1) = line[-2:]
    line.insert(-1, [x, z0 + (z1 - z0) * (x - x0) / (x1 - x0), hb])
    return [[x_m(px), body(z), body(h)] for px, z, h in line]


def add_her_lines(hull: dict, notes: dict) -> None:
    """Her profile, form and marks into her hull mapping and their notes into her hull notes, her
    drawn figures into `REPORT` and the generator's stderr. Nothing else of the hull changes."""
    length_ratio = hull["length_waterline_m"] / PLATE_WATER_M
    beam_ratio = hull["beam_m"] / PLATE_BEAM_M

    def x_m(x_ft):
        return x_ft * SWEDISH_FT * length_ratio

    def body(z_ft):
        """A height or half-breadth of the body: the beams' ratio (principle 7)."""
        return z_ft * SWEDISH_FT * beam_ratio

    def side(z_ft):
        """A height of the side: its lowest by the beams' ratio, its rise by the waterlines'."""
        return (RAIL_LOWEST_FT * beam_ratio + (z_ft - RAIL_LOWEST_FT) * length_ratio) * SWEDISH_FT

    def stem_z(z_ft):
        return side(z_ft) if z_ft > RAIL_LOWEST_FT else body(z_ft)

    breadth = (
        [[x_m(x), body(w), body(r)] for x, w, r in BEYOND_AFT_FT]
        + sorted(
            [[x_m(STATION_X_FT[st]), body(w), body(r)] for st, (r, w) in HALF_BREADTH_FT.items()]
            + [[x_m(x), body(w), body(r)] for x, w, r in BETWEEN_FT]
        )
        + [[x_m(x), body(w), body(r)] for x, w, r in BEYOND_FORE_FT]
    )
    stern = [[x_m(x), body(z)] for x, z in STERN_FT[:-1]]
    stern.append([x_m(STERN_FT[-1][0]), side(STERN_FT[-1][1])])
    section = plate_section(body, side)
    under_water = {
        "steel": lambda: steel_body(hull, round(x_m(STATION_X_FT["⊕"]), 2), section, x_m, body),
        "plate": lambda: plate_frames(x_m, body),
    }[UNDER_WATER]()
    hull["profile"] = g.hull_profile(
        [[x_m(x), side(z)] for x, z in RAIL_FT],
        breadth,
        keel=[[x_m(x), body(z)] for x, z in KEEL_FT],
        stem=[[x_m(x), stem_z(z)] for x, z in STEM_FT],
        stern=stern,
        wales=[[x_m(x), body(lo), body(hi)] for x, lo, hi in WALE_FT],
        section=section,
        decks={"upper": [[x_m(x), body(z)] for x, z in DECK_FT]},
        breadth_line=breadth_line(x_m, body),
        sections=under_water + bow_rail(x_m, side, body),
        channel_wales=[[x_m(x), body(lo), body(hi)] for x, lo, hi in BAND_FT],
        floor=[[x_m(STATION_X_FT[st]), body(z), body(hb)] for st, z, hb in FLOOR_FT],
        rabbet=[[x_m(x), body(z), body(RABBET_HALF_SIDING_FT)] for x, z in RABBET_FT],
    )
    form = {
        "stern": {
            "type": "raked",
            "knuckle_z_m": body(KNUCKLE_FT),
            "transom_hb_m": list(TRANSOM_HB_M),
            "round_up_m": body(ROUND_UP_FT),
        },
        "head": "none",
    }
    REPORT.clear()
    REPORT.append(
        f"her ratios: lengths {length_ratio:.4f}, the waterlines'; the body {beam_ratio:.4f}, the "
        f"beams'; the body under the water '{UNDER_WATER}'."
    )
    g.hull_form(hull, form=form, marks=MARKS, measured=(), report=REPORT)
    keel = hull["profile"]["keel_m"]
    at_middle = keel[0][1] + (keel[1][1] - keel[0][1]) * -keel[0][0] / (keel[1][0] - keel[0][0])
    REPORT.append(
        f"her keel's lower edge {-keel[0][1]:.2f} m below the water at its heel, "
        f"{-at_middle:.2f} m at the middle and {-keel[1][1]:.2f} m at the forefoot, against the "
        f"file's mean draught of {hull['draught_m']:g} m: recorded, not moved."
    )
    REPORT.append("her port triples: none; no port and no gun is drawn, and the file has no gun.")
    notes.update(NOTES)
    notes["profile.sections_m"] = SECTIONS_NOTES[UNDER_WATER]
    for line in REPORT:
        print(f"smack: {line}", file=sys.stderr)
