"""The *Prince de Neufchatel*, the American privateer hermaphrodite brig built at New York in
1812-13 and taken on 28 December 1814 (package 75, the second ship; her builder B2).

Her design is docs/design/Design-Ship-PrinceDeNeufchatel.md (cited here as Neuf-D), from her
research note docs/design/Research-PrinceDeNeufchatel-2026-10.md (Neuf) and the owner's answers
(docs/design/Decisions-ShipsRound2-2026-10.md; Neuf-D §17). One module writes one file,
`data/ships/hermaphrodite-brig.yaml` (Neuf-D decision 1): `particulars()` gives her figures in
the file's frame from the data below and raises in words where a check of Neuf-D §1.5 fails,
`write(out_dir, p)` builds and dumps her file, `main_topgallant(...)` writes her main topgallant
on its two light yards, and `build(out_dir)` is the generator's hook (`tools/gen_ships.py`,
`SHIP_MODULES`).

**Built so far (Neuf-D §13, steps 1 to 4 and 6).** Her hull block and profile with her shape
keys (§2, §3); her masts, yards and square sails, the fore gaff sail, the main with its gaff, boom
and gaff topsail, the main topgallant on its two light yards, the head and its three headsails
(§4.1 to §4.6); the staysails between the masts, the studding sails, the storm canvas, the groups
and the aliases (§4.7, §4.8); her one fit, each gun on its port's triple, and its magazine (§5);
her company of 130, her marines, her people drawn from her wardroom file
(data/people/hermaphrodite-brig.yaml) and her quarter bill (§6); her ground tackle by Steel's row,
her boats, pumps, hold and stores (§7); her description at far detail with its fit and role (§8),
whose index row is in freesail/world/ships.py. Her polar is tuned at her road's step 5.

**Her main topgallant (D10; the lead's ruling of 2026-11-06 on Neuf-D §12.2a).** Written from her
first commit on its two light yards on the main topmast and its pole (§4.5), with no schema key:
the engine's rule (`Ship.on_schooner_mast`, B3.4) reads a yard on an after mast with no yard on
its lower mast as a fore-and-after's, so she handles as a fore-and-after with four fore yards and
the main's two light yards her after yards. Neuf-D's `MAIN_TOPGALLANT` flip, its "out" stage and
D10(a)'s key are superseded by that ruling; there is no flip. The sail is in her "royals" with
the fore royal, so that "make all sail" sets it and "shorten sail" takes it in (B3.4's finding).

**The frame (Neuf-D §1.4).** The figures below are in her sheets' frame, as the sources give them:
x in feet forward of the after rabbet at her sailing-trim line on RMG ZAZ6177 (her lines), z in
feet above that line at the station; the masts, yards, sails and head spars from RMG ZAZ6179
(her sail plan), whose waterline is level, in feet above it. They are converted once: x in
metres forward of the middle of the waterline between the rabbets, 107.3 ft long; z in metres
above her water at the station (her water slopes 1.63 degrees to her keel's rabbet, and the
engine has no trim). A spar's `height_m` and a sail's `corners_m` are then taken above the
datum, her flush deck at side at mid-length (1.16 m); a sail's centre stays above the water.
The figures come in at the measured value, rounded early (Indf §16, risk 4).

**The join (Neuf-D §1.4, §3.7 task 1).** Neuf gives her ports and masts in feet forward of the
post at deck height, an origin abaft the after rabbet the lines are measured from:
`POST_AT_DECK_FT`, the design's 0.85 ft, through which every port and mast goes. Task 1's
checker measured it again on the ports and found more (docs/dev/TuningNotes.md, "The *Prince de
Neufchatel*"): the difference is over the design's 0.3 ft, which is reported to the lead before
it is written, so the design's figure stands here until the lead rules on it.

**Her notes (the lead's notes of 2026-10-29, item 2).** The file's notes carry sources,
departures and judgements. A figure a rule computes from the file's own keys (an area from a
cut, a rating, a rope's size, a drawn displacement, a port's gap) is printed by `her_report()`,
the generator's report, and held by her tests, where it cannot go stale.

The module is imported only by the generator's entry block, after `gen_ships` is made the
running script, and takes every helper as `g.<name>` (Indf §1.2). No function or table of the
generator is changed; every other file stays byte for byte as it is.

Marks as the design's: measured (on the held 1280-px images, ZAZ6177 at 7.05 px/ft and ZAZ6179
at 6.52 px/ft, by the research's registration), read (the page or its image), read (OCR),
judgement. The images are not in the repository.
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

# ---------------------------------------------------------------------------
# The frame: her lines (ZAZ6177) and the file
# ---------------------------------------------------------------------------

# Her waterline between the rabbets at her sailing-trim line, D29 (b): 107.3 ft (x 321.6 to 1078.3
# px on ZAZ6177, measured, +-0.5 ft: Neuf §2.4). The file's x = 0 is its middle.
LWL_FT = 107.3
MIDDLE_FT = LWL_FT / 2.0
# Neuf's ports and masts are given forward of the post at deck height (Neuf §2.7); that origin
# lies this far abaft the after rabbet (measured at both end ports: Neuf-D §1.4; the checker's
# figure is reported, not written: the module's docstring, "The join").
POST_AT_DECK_FT = 0.85
# The datum: her flush deck at side at mid-length, 3.8 ft above her line (measured, +-0.3 ft:
# Neuf §2.7; the red line traced for the design gives 3.75 ft); Build-Ships.md §5.5's rule for a
# new file; D18 moot for her, a flush deck giving one datum under every option (Neuf-D §2.2).
DATUM_FT = 3.8
# The plank: 2 in, 25 ft 8 in extreme less 25 ft 4 in moulded on ZAZ6177's table (judgement:
# Neuf §2.5); her lines are drawn moulded (Neuf §2.2).
PLANK_FT = 2.0 / 12.0


def x_m(x_ft):
    """Feet forward of the after rabbet to the file's metres forward of midships."""
    return (x_ft - MIDDLE_FT) * FT


def x_from_post(x_ft):
    """Feet forward of the post at deck height (Neuf's origin) to the file's x."""
    return x_m(x_ft - POST_AT_DECK_FT)


def z_m(z_ft):
    """Feet to metres."""
    return z_ft * FT


DATUM_M = round(z_m(DATUM_FT), 2)


def above_datum(z_water_m):
    """A height above her water, metres, as the file's spars and corners have it."""
    return z_water_m - DATUM_M


def interp(points, x):
    """Straight between (x, y) points, held beyond them."""
    if x <= points[0][0]:
        return points[0][1]
    for (x0, y0), (x1, y1) in zip(points, points[1:], strict=False):
        if x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return points[-1][1]


# -- her waterlines by station (Neuf §2.4, measured, +-0.1 ft): half-breadths moulded, ft, at
# 10-ft stations from the after rabbet along her line; WL2 and WL3 drawn parallel to it, 2.63 and
# 5.27 ft below (Neuf §2.3). Every line runs into the rabbets at about 0.3 ft.
STATIONS_FT = (10, 20, 30, 40, 50, 60, 70, 80, 90, 100)
LWL_HB = (6.29, 9.45, 10.80, 11.52, 11.90, 12.23, 11.97, 11.37, 9.50, 5.26)
WL2_HB = (2.72, 6.11, 8.57, 9.71, 10.34, 10.37, 10.01, 9.02, 6.82, 3.12)
WL3_HB = (1.25, 2.78, 4.61, 5.86, 6.40, 6.26, 5.64, 4.57, 3.17, 1.03)
WL2_BELOW_FT = 2.63
WL3_BELOW_FT = 5.27
END_HB_FT = 0.3
# Her top breadth, moulded, ft, by distance from the post (Neuf §2.4, measured, not re-measured),
# taken as the rail's half-breadth (judgement: the body plan draws her topsides near upright;
# Neuf-D §3.7 task 4 reads the top-timber line).
TOP_BREADTH = (
    (2.0, 8.3),
    (12.0, 9.1),
    (26.0, 10.8),
    (41.0, 11.7),
    (55.0, 12.4),
    (65.0, 12.55),
    (76.0, 12.3),
    (83.0, 11.8),
    (96.0, 9.2),
    (101.0, 6.9),
    (104.0, 5.1),
)
# Forward of Neuf's last reading nothing is read: the rail's half-breadth at the fore rabbet,
# moulded, is the trend from 104 ft to the stem's siding at the stem head (judgement), so that
# the bow is not drawn full to the stem (Neuf-D §3.2).
STEM_RAIL_HB_FT = 2.13
# The dead-flat section, ft: height above the rabbet against half-breadth, moulded (Neuf §2.4,
# measured): the straight floor rising 27 degrees and the firm bilge; her line 8.21 ft above the
# body plan's base there.
DEAD_FLAT = (
    (0.0, 0.37),
    (0.92, 1.79),
    (2.06, 3.91),
    (3.19, 6.33),
    (4.33, 8.45),
    (5.46, 10.07),
    (6.60, 11.15),
    (7.73, 11.86),
    (8.21, 12.17),
    (10.0, 12.48),
)
DEAD_FLAT_LWL_ABOVE_BASE_FT = 8.21

# -- her side and decks, (ft from the after rabbet, ft above her line), measured on ZAZ6177 for
# the design (Neuf-D §3.2, +-0.3 ft) and re-traced by task 1's checker (the tuning notes) --------
# The top of her side traced by column, the columns of the mast stumps and deck fittings dropped;
# the taffrail first, the rail's fore end last.
RAIL = (
    (-5.27, 9.45),
    (-0.19, 8.40),
    (11.10, 8.17),
    (18.18, 7.94),
    (25.30, 7.87),
    (32.39, 7.51),
    (42.30, 7.51),
    (51.39, 7.74),
    (62.21, 7.78),
    (73.50, 7.68),
    (80.59, 7.87),
    (89.21, 8.43),
    (96.20, 8.92),
    (102.60, 9.09),
    (106.31, 9.12),
)
# The deck at side, the red line: Neuf §2.7's five (the stern 5.0 ft, lowest at the main 3.4-3.5,
# mid-length 3.8, the foremast 4.4, the bow 5.6) and the points between them traced for the design.
DECK_AT_SIDE = (
    (-1.01, 4.99),
    (6.90, 4.76),
    (11.10, 4.40),
    (26.71, 4.07),
    (38.10, 3.44),
    (43.71, 3.41),
    (MIDDLE_FT, DATUM_FT),
    (62.21, 3.84),
    (80.59, 4.07),
    (86.00, 4.40),
    (96.20, 5.18),
    (104.70, 5.51),
    (106.31, 5.61),
)
# The stem's fore edge, low to high, measured at 5x: its foot on the false keel judged, straight
# below the lowest traced point (the second); the curve meeting her line at the rabbet's x; the
# point where the head rails meet it; the stem head, where the bowsprit's lower edge crosses the
# bow (Neuf-D §3.2).
STEM = (
    (101.91, -9.15),
    (103.32, -5.09),
    (105.59, -2.46),
    (LWL_FT, 0.0),
    (108.44, 3.02),
    (108.93, 5.87),
    (108.87, 6.66),
    (108.28, 7.71),
)
# The stern, low to high: the post's heel (by its after edge's raked line, 11-12 degrees, produced
# to the false keel's bottom), the post's after edge at her water (the hinge line, Neuf §2.6's 12.1
# degrees), the transom's foot just abaft the post's head and the taffrail (Neuf-D §3.5).
STERN = (
    (1.45, -11.75),
    (-POST_AT_DECK_FT, 0.0),
    (-2.35, 4.66),
    (-5.27, 9.45),
)
# The false keel's bottom, the scale bar's border (Neuf §2.3): its depths at the perpendiculars
# 11 ft 8 3/4 in aft and 9 ft 0 in forward (measured); the post's heel and the gripe's foot.
KEEL = ((1.45, -11.75), (101.91, -9.15))
# The keel's rabbet, drawn straight and level on the sheet: 10.1 ft below her line at the post and
# 7.5 ft at the forefoot (Neuf §2.3), its middle at the dead flat on the line between; the keel
# sided 0.7-0.8 ft (Neuf §2.3), its half 0.36 ft.
RABBET_ENDS = ((1.45, -10.1), (101.91, -7.5))
RABBET_DEAD_FLAT_X_FT = 54.40
KEEL_HALF_SIDING_FT = 0.36
# The knee of the head's fore edge: from where the head rails meet the stem to its top, about 7 ft
# before the stem (measured).
HEAD = ((108.87, 6.66), (115.79, 8.99))
# The transom (Neuf-D §3.5, measured): its face raking from its foot (STERN's third point) to the
# taffrail with no counter; on the body plan 16.1 ft across its top corners and 16.6 ft at its
# knuckle, its top arched about 0.35 ft, so that it tumbles home above the knuckle as every
# transom does. The knuckle's breadth is the re-reading at the knuckle's height (B2's, taken by
# the lead's ruling of 2026-11-07): the sides near plumb, 16.6-16.8 ft across from 4.0 to 7.0 ft
# above her water, the horizontal line at 4.6-5.1 ft where her knuckle stands (4.65 ft); the
# first reading's 15.8 ft was taken at 3.2-3.9 ft, below the knuckle, where the outline rounds in
# (the half-breadths 2.46 and 2.41 m before, 2.46 and 2.53 now).
TRANSOM_HB_FT = (8.07, 8.30)
TRANSOM_ROUND_UP_FT = 0.35

# -- her ports (Neuf §2.7; Neuf-D §3.3) ------------------------------------------------------
# Eleven a side, lids drawn, the same on ZAZ6178; "pierced for 22 guns, and mounting 18" (Naval
# Chronicle vol. 33 p. 72, read). Their centres in ft forward of the post at deck height (Neuf
# §2.7, measured, +-0.5 ft), from forward; each sill the port frame's lower edge at the
# half-maximum in its middle ten columns, ft above her line (measured for the design, +-0.3 ft;
# re-measured by task 1's checker on ZAZ6177 and ZAZ6178: the tuning notes).
PORTS_FROM_POST = (101.7, 92.5, 83.1, 74.2, 64.5, 54.9, 45.5, 36.0, 26.4, 17.2, 7.8)
SILLS_FT = (6.68, 5.97, 5.20, 5.20, 5.06, 4.92, 4.94, 4.94, 5.09, 5.39, 5.84)
# The port's size, the eleven's mean: 2 ft 8 in wide by 2.48 ft deep (measured; Neuf's 2.7 by 2.4,
# +-0.3 ft). The end ports are shallower, 2.18 ft forward and 2.05 ft aft (measured).
PORT_SIZE_FT = (2.0 + 8.0 / 12.0, 2.48)
# The small ports, one about 4.6 ft abaft each gun port, 0.7-0.85 ft square, probably sweep ports
# (Neuf §2.7, measured; Chapelle 1930 p. 13): at these x px on ZAZ6177 (in the note, not drawn;
# D11 (a)).
SWEEP_PORTS_PX = (338, 403, 468, 533, 602, 668, 735, 798, 870, 937, 1002)

# ---------------------------------------------------------------------------
# Her rig (ZAZ6179, measured, the yards drawn as half-lengths and doubled: Neuf §1.2, §3.2-§3.3;
# D37 (a)); Fincham 1843 p. 78's first example "rigged as brig forward and schooner aft" (read on
# the page image; p. 72's proportions on 110.6 x 25.6 ft where p. 78 lists none) only for spars
# the sheet does not draw (Neuf-D decision 10)
# ---------------------------------------------------------------------------

# The masts: x at the deck, ft forward of the post (Neuf §2.7, the middle of each measured range:
# the main 42.3-42.6, the fore 85.9-86.4; ZAZ6179 gives them 43.9 ft apart); rake from the upright
# with her water level (ZAZ6179, measured, +-0.7 deg); the heel below her water, the lower mast
# heel to hounds and its head (ZAZ6179, measured, +-1 ft); the cap above her water: the fore's by
# its length and rake, the main's read on the sheet (79.4 by length and rake).
MASTS = {
    "fore": {
        "from_post_ft": 86.15,
        "rake_deg": 10.3,
        "heel_ft": 6.1,
        "hounded_ft": 58.4,
        "head_ft": 10.1,
        "cap_ft": None,
    },
    "main": {
        "from_post_ft": 42.45,
        "rake_deg": 12.4,
        "heel_ft": 7.4,
        "hounded_ft": 80.5,
        "head_ft": 8.4,
        "cap_ft": 79.6,
    },
}
# The upper masts, ft, (to the hounds, the head or pole above them) (ZAZ6179, measured): the fore
# topmast 34.8 (29.8 and a 5.1-ft head); the fore topgallant with its royal pole in one, 29.6
# (19.3 and a 10.4-ft pole; the fore's upper masts not re-measured, Neuf §3.2); the main topmast
# 39.6 (27.5 and a 12.1-ft pole). Each heels at the hounds of the mast below.
UPPER = {
    "fore": {"topmast": (29.8, 5.1), "topgallant": (19.3, 10.4)},
    "main": {"topmast": (27.5, 12.1)},
}
FORE_TOPMAST_FT = 34.8
FORE_TOPGALLANT_FT = 29.6
# The trucks above her water (ZAZ6179, measured): the check of the masts' lengths and rakes.
TRUCKS_FT = {"fore": 110.4, "main": 110.1}

# The yards: length ft and height above her water ft (ZAZ6179, measured; doubled, +-1.5 ft).
YARDS = {
    "fore.yard": (65.0, 47.2),
    "fore.topsail.yard": (46.8, 78.5),
    "fore.topgallant.yard": (26.0, 97.7),
    "fore.royal.yard": (24.5, 108.1),
    # her main topgallant's two light yards (Neuf-D §4.5): 34.4-35 and 23.6-25 ft doubled
    "main.topsail.yard": (34.7, 95.7),
    "main.topgallant.yard": (24.3, 107.5),
}
# The gaffs: length ft, jaws above her water ft, peaked degrees above the level (ZAZ6179,
# measured, +-0.7 ft; the fore gaff's peak judgement, Neuf §1.2; the main's 24.0 degrees, §3.2).
GAFFS = {"fore": (32.9, 46.9, 27.0), "main": (37.3, 64.4, 24.0)}
# The main boom: length ft, above her water at the mast and at its end ft (measured). It overhangs
# the taffrail 19.6 ft (measured).
MAIN_BOOM_FT = (64.2, 10.4, 16.4)
# The head (Neuf §1.2, measured on ZAZ6179): the bowsprit 22.4 ft outboard from the stem to the
# cap, steeved about 15 degrees (14.9 on ZAZ6177 for the drag); the jibboom 38.7 ft heel to end;
# the flying jibboom about 11 ft beyond it (+-3 ft), its end 57.2 ft ahead of the stem head. The
# ends' heights above her water, the bowsprit's cap 15.2 ft, the jibboom's end 22.8 ft and the
# flying jibboom's 25.5 ft, and each boom's reach beyond the spar below, the jibboom 26.2 ft and the
# flying jibboom 11.1 ft, measured on ZAZ6179 by task 1's checker (the tuning notes).
BOWSPRIT_OUT_FT = 22.4
BOWSPRIT_STEEVE_DEG = 15.0
JIBBOOM_FT = 38.7
HEAD_SPAR_ENDS_FT = {"bowsprit": 15.2, "jib_boom": 22.8, "flying_jib_boom": 25.5}
JIB_BOOM_BEYOND_FT = 26.2
FLYING_JIB_BOOM_BEYOND_FT = 11.1
# Where her sail plan draws the bowsprit over the stem, about 10 ft above her water (ZAZ6179,
# measured by the checker): the fore stay's foot (judgement), her lines' stem head lower.
BOWSPRIT_AT_STEM_FT = 10.0
# The studding-sail booms (Neuf §1.2, measured): run out 16.1 ft beyond the fore yardarm and 6.9
# ft beyond the fore topsail yardarm; the swinging boom, the lower studding sail's foot, not
# drawn: Fincham p. 78's 43.01 ft (judgement for hers).
STUNS_BOOM_FT = {"fore.yard": 16.1, "fore.topsail.yard": 6.9}
SWINGING_BOOM_FT = 43.0

# The sails' areas measured on ZAZ6179 from the corners, sq ft, +-10-15% (Neuf §3.3; the mainsail,
# the fore gaff sail and the main staysail re-measured; the flying jib and the main topmast
# staysail on its upper foot read by task 5's checker, Neuf-D §3.7, with the main staysail again:
# the tuning notes): the check of each sail as cut (Neuf-D §1.5).
SAILS_MEASURED_SQFT = {
    "main.sail": 2780,
    "fore.course": 2000,
    "fore.topsail": 1700,
    "fore.sail": 1660,
    "fore.topgallant": 580,
    "main.staysail": 530,
    "main.gaff_topsail": 470,
    "main.topgallant": 300,
    "fore.royal": 250,
    "fore.lower.studdingsail": 665,
    "flying_jib": 447,
    "main.topmast_staysail": 398,
}
SAIL_TOLERANCE = 0.15
# The fore course: 33.3 ft deep, its foot 14 ft above her water (measured).
COURSE_DEPTH_FT = 33.3
# The fore gaff sail (Neuf §1.2, measured, +-0.6 ft): luff about 37.9 ft, its clew 2.7-2.9 ft
# abaft the mainmast's line and 12.6 ft above her water, its foot about 46.6 ft drawn curved.
FORE_GAFF_LUFF_FT = 37.9
FORE_GAFF_CLEW_FT = (2.8, 12.6)
# The mainsail (Neuf §3.3, re-measured): luff 55, head 35, leech 65, foot 62 ft; its head along
# the gaff from the jaws, its foot along the boom from the mast.
MAINSAIL_FT = {"head": 35.0, "foot": 62.0}
# The fore lower studding sail, drawn solid: about 19 ft wide and 35 ft deep under the fore yard
# (Neuf §1.2, measured).
LOWER_STUNS_FT = (19.0, 35.0)
# The flying jib (task 5's reading on ZAZ6179, Neuf-D §3.7: the tuning notes): its tack at the
# flying jibboom's end, its head 41.3 ft above the tack and 54.1 ft abaft it, its clew level with
# the tack and 21.0 ft abaft it, the foot's roach 17 sq ft over its chord. The jib's clew is not
# read: its area the design's working figure (Neuf-D §4.3: 121 m2, judgement, with the fore
# staysail's working 93 closing Fincham's remainder of 2,200-2,400 sq ft for the jib and the fore
# topmast staysail, Neuf §2.8). The fore staysail's clew is not read either, and its working 93
# m2 was that same derivation of the design's own, not her sail plan's figure: as a triangle with
# a level foot from its tack up the fore stay to the fore hounds its clew stood 7.4 m abaft the
# fore mast. Corrected by the lead's ruling of 2026-11-07 to the triangle that fits, its leech
# down the fore mast to its foot (`head_sails`): 46 m2.
FLYING_JIB_FT = {"head_above": 41.3, "head_aft": 54.1, "clew_aft": 21.0, "roach_sqft": 17.0}
HEADSAIL_WORKING_M2 = {"jib": 121}
# The staysails between the masts (task 5's reading on ZAZ6179): the main staysail's stay from
# the main mast's hounds to the fore mast 13 ft above her water, its head on it 47.4 ft above her
# water, its clew 8.1 ft above her water and 6.9 ft forward of the head; the main topmast
# staysail's stay from the main topmast's hounds to the fore topmast's, its peak on it 91.2 ft
# above her water, its leech upright to its foot, drawn at two heights, 72.9 and 44.9 ft.
MAIN_STAYSAIL_FT = {"stay_fore": 13.0, "head": 47.4, "clew": 8.1, "clew_forward": 6.9}
MAIN_TOPMAST_STAYSAIL_FT = {"peak": 91.2, "upper_foot": 72.9, "lower_foot": 44.9}

# Fincham 1843 p. 78 (and p. 72's proportions where p. 78 lists none), ft: the guard of Neuf-D
# §1.5 against a mistyped figure, each spar the sheet draws within FINCHAM_GUARD_FT of his; the
# fore gaff (his 37.1), the royal yard (21.3) and the flying jibboom (15.6) differ as drawn and are
# noted (D37 (a)), not checked.
FINCHAM = {
    "main hounded": (79.6, "p. 72: 3.11 x the breadth"),
    "fore hounded": (58.4, "p. 72: 0.734 of the main"),
    "main topmast": (40.3, "p. 72: 28.2 hounded and a 12.1 pole"),
    "fore topmast": (35.2, "p. 72: 30.4 and a 4.7 head"),
    "fore topgallant and royal pole": (30.5, "p. 72: 19.7 and a 10.8 pole"),
    "jibboom": (38.9, "p. 72: 1.21 x the bowsprit on the hounded reading"),
    "main boom": (64.46, "p. 78"),
    "main gaff": (37.1, "p. 78"),
    "fore yard": (63.25, "p. 78"),
    "fore topsail yard": (46.52, "p. 78"),
    "fore topgallant yard": (26.67, "p. 78"),
    "main topsail yard": (36.3, "p. 78"),
    "main topgallant yard": (23.22, "p. 78"),
}
FINCHAM_GUARD_FT = 2.0

# Winfield 1793-1817 pp. 335-336 (the owner's copy, read): keel for tonnage 93 ft 8 1/4 in,
# breadth extreme 25 ft 8 in, burthen 328 22/94 tons; the Navy's rule's check within a ton
# (Neuf-D §1.5).
TONNAGE = {
    "keel_ft": 93.0 + 8.25 / 12.0,
    "beam_ft": 25.0 + 8.0 / 12.0,
    "burthen": 328.0 + 22.0 / 94.0,
}
# The masts' spacing at the deck (Neuf §2.7: 43.6-43.9 ft; ZAZ6179's 43.9).
MAST_SPACING_FT = (43.6, 43.9)

# Brace limits, degrees from square: the brig-sloop's fore by level (brig.yaml: the fore yard 60,
# the royal 66; judgement as hers), the main's two light yards 60 and 62 (judgement): no source
# gives hers (Neuf-D §4.2).
BRACE_LIMITS = {
    "fore.yard": 60,
    "fore.topsail.yard": 62,
    "fore.topgallant.yard": 64,
    "fore.royal.yard": 66,
    "main.topsail.yard": 60,
    "main.topgallant.yard": 62,
}
# The fore channel's chain plates on ZAZ6177, x 817 to 927 px (Neuf §1.2, measured), by the
# research's registration: the lee shrouds' lead aft, for the fore yard's brace limit's check
# (Neuf-D §4.2).
FORE_CHANNEL_AFT_PX = 817.0
ZAZ6177_PX_PER_FT, ZAZ6177_RABBET_PX = 7.05, 321.6

# Reefs (Neuf-D §4.3): the fore course 2 and the fore gaff sail 2 (Cobb p. 95, "a double reefed
# foresail", which foresail not said); the fore topsail 3 (the brig's); the mainsail 3 ("closely
# reefed", Cobb p. 95; the schooner's 3); the gaff topsail, the topgallants and the royal none.
REEFS = {"fore.course": 2, "fore.sail": 2, "fore.topsail": 3, "main.sail": 3}

# The horse across her transom for the main sheet: its span the transom's inside breadth, about
# 4.6 m on a transom 16.1 ft across its top (judgement).
HORSE_M = 4.6

# Her rope (Neuf-D §4.2): the brig-sloop's line sizes for the fore and the head, the topsail
# schooner's for the main and the gaffs, each scaled by the root of her sail on that mast over
# theirs (judgement, as Indf scales the frigate's). Theirs, m2, from brig.yaml and
# topsail-schooner.yaml: the brig's fore square sails 94, 114, 46 and 28; her three headsails 33,
# 57 and 31; her main topgallant 45; her main's square sails and spanker 94, 121, 45, 28 and 162
# (for the main stay alone, the schooner filing none); the schooner's fore sail 147, her mainsail
# 198 and gaff topsail 40.
THEIRS_M2 = {
    "brig fore": 94 + 114 + 46 + 28,
    "brig head": 33 + 57 + 31,
    "brig main topgallant": 45,
    "brig main": 94 + 121 + 45 + 28 + 162,
    "schooner fore sail": 147,
    "schooner main": 198 + 40,
}

# What her rules compute from her own keys, for `her_report()`.
REPORT: dict = {}


# ---------------------------------------------------------------------------
# Her particulars: the figures in the file's frame, and the checks of Neuf-D §1.5
# ---------------------------------------------------------------------------


@dataclass
class Particulars:
    """Her figures in the file's frame, metres: the hull block and its notes, the profile's lines
    ([x, z] above her water, a port [x, sill, half-breadth], the breadth [x, at her water, at the
    rail]), each lower mast's place at the datum and its rake, and above her water each spar's top
    as its height is filed and each mast's hounds (`the_masts`)."""

    hull: dict
    hull_notes: dict
    rail: list
    breadth: list
    decks: list
    ports: list
    stem: list
    stern: list
    keel: list
    rabbet: list
    head: list
    section: list
    sections: list
    mast_x: dict
    rake: dict
    caps: dict
    hounds: dict


def top_breadth(x_rabbet_ft):
    """Her top breadth's half-breadth, moulded, ft, at a station ft from the after rabbet."""
    return interp(TOP_BREADTH, x_rabbet_ft + POST_AT_DECK_FT)


def lwl_hb(x_ft):
    """Her sailing-trim line's half-breadth, moulded, ft, at a station from the after rabbet:
    Neuf's stations, run straight into the rabbets."""
    pts = [(0.0, END_HB_FT), *zip(STATIONS_FT, LWL_HB, strict=True), (LWL_FT, END_HB_FT)]
    return interp(pts, x_ft)


def particulars():
    """Her figures in the file's frame, and the checks of Neuf-D §1.5 raised in words (never an
    `assert`, which `python -O` strips) before the file is written."""
    check_tonnage()
    # her breadth: her line at the 10-ft stations and the rabbets, and a station added at Neuf's
    # last top breadth (104 ft from the post), her line taken straight there between the 100-ft
    # station and the rabbet as the form draws it between stations (judgement); the rail the top
    # breadth through the join, the after station's Neuf's 2-ft reading carried aft (judgement)
    stations = [0.0, *STATIONS_FT, TOP_BREADTH[-1][0] - POST_AT_DECK_FT, LWL_FT]
    breadth = []
    for x in stations:
        if x == 0.0:
            rail_hb = TOP_BREADTH[0][1]
        elif x == LWL_FT:
            rail_hb = STEM_RAIL_HB_FT
        else:
            rail_hb = top_breadth(x)
        breadth.append([x_m(x), (lwl_hb(x) + PLANK_FT) * FT, (rail_hb + PLANK_FT) * FT])
    ports = []
    for from_post, sill in zip(PORTS_FROM_POST, SILLS_FT, strict=True):
        x = from_post - POST_AT_DECK_FT
        ports.append([x_m(x), z_m(sill), (top_breadth(x) + PLANK_FT) * FT])
    ports.sort()  # aft to forward, as the schema has a deck's ports
    check_ports(ports)
    # the rabbet: straight and level on the sheet, its middle on the line through its ends
    (xa, za), (xf, zf) = RABBET_ENDS
    zmid = za + (zf - za) * (RABBET_DEAD_FLAT_X_FT - xa) / (xf - xa)
    half = KEEL_HALF_SIDING_FT * FT
    rabbet = [
        [x_m(x), z_m(z), half] for x, z in ((xa, za), (RABBET_DEAD_FLAT_X_FT, zmid), (xf, zf))
    ]
    section = [[z_m(h - DEAD_FLAT_LWL_ABOVE_BASE_FT), (hb + PLANK_FT) * FT] for h, hb in DEAD_FLAT]
    sections = []
    for x, lwl, wl2, wl3 in zip(STATIONS_FT, LWL_HB, WL2_HB, WL3_HB, strict=True):
        for below, hb in ((WL3_BELOW_FT, wl3), (WL2_BELOW_FT, wl2), (0.0, lwl)):
            sections.append([x_m(x), z_m(-below), (hb + PLANK_FT) * FT])
    mast_x, rake, caps, hounds = the_masts()
    check_masts(mast_x, caps)
    hull, notes = hull_block()
    return Particulars(
        hull=hull,
        hull_notes=notes,
        rail=[[x_m(x), z_m(z)] for x, z in RAIL],
        breadth=breadth,
        decks=[[x_m(x), z_m(z)] for x, z in DECK_AT_SIDE],
        ports=ports,
        stem=[[x_m(x), z_m(z)] for x, z in STEM],
        stern=[[x_m(x), z_m(z)] for x, z in STERN],
        keel=[[x_m(x), z_m(z)] for x, z in KEEL],
        rabbet=rabbet,
        head=[[x_m(x), z_m(z)] for x, z in HEAD],
        section=section,
        sections=sections,
        mast_x=mast_x,
        rake=rake,
        caps=caps,
        hounds=hounds,
    )


def the_masts():
    """Each lower mast's place at the deck and its rake, and, metres above her water, each
    spar's top as its height is filed (`caps`: the hoists the vertical heights between them, the
    rake's cosine applied, Neuf-D §4.1) and each mast's hounds (`hounds`). Each upper mast heels
    at the hounds of the one below, the doubling its head. The lower caps; the fore topmast's cap
    above its head; the fore topgallant's hounds, where its royal pole begins, and the pole's top;
    the main topmast's hounds, where its pole begins, and the pole's top."""
    mast_x, rake, caps, hounds = {}, {}, {}, {}
    for name, m in MASTS.items():
        mast_x[name] = round(x_from_post(m["from_post_ft"]), 2)
        rake[name] = m["rake_deg"]
        c = math.cos(math.radians(m["rake_deg"]))
        by_length = (m["hounded_ft"] + m["head_ft"]) * c - m["heel_ft"]
        cap = m["cap_ft"] if m["cap_ft"] is not None else by_length
        if abs(cap - by_length) > 1.0:
            raise ValueError(
                f"neufchatel: the {name} mast's cap is read {cap:g} ft above her water and its "
                f"length and rake give {by_length:.1f}; they agree within a foot on her sheet."
            )
        caps[f"{name}.mast"] = z_m(cap)
        at = cap - m["head_ft"] * c  # the lower mast's hounds
        hounds[f"{name}.mast"] = z_m(at)
        for level, (to_hounds, head) in UPPER[name].items():
            spar = f"{name}.topmast" if level == "topmast" else f"{name}.topgallant_mast"
            at += to_hounds * c
            hounds[spar] = z_m(at)
            # the stick's top: its head above its hounds, the pole for the last of its mast
            if name == "fore" and level == "topmast":
                caps[spar] = z_m(at + head * c)
            else:
                caps[spar] = z_m(at)
                pole = "fore.royal_mast" if name == "fore" else "main.topgallant_mast"
                caps[pole] = z_m(at + head * c)
    return mast_x, rake, caps, hounds


def check_tonnage():
    """The Navy's rule on Winfield's keel for tonnage and extreme breadth, within a ton of his
    burthen (Neuf-D §1.5)."""
    t = TONNAGE
    tons = t["keel_ft"] * t["beam_ft"] * (t["beam_ft"] / 2.0) / 94.0
    if abs(tons - t["burthen"]) > 1.0:
        raise ValueError(
            f"neufchatel: the Navy's rule on a keel of {t['keel_ft']:.4f} ft and a breadth of "
            f"{t['beam_ft']:.4f} ft gives {tons:.2f} tons, more than a ton off Winfield's "
            f"{t['burthen']:.2f} (pp. 335-336); a figure is mistyped."
        )
    REPORT.setdefault("checks", []).append(
        f"the Navy's rule on Winfield's keel and breadth gives {tons:.2f} tons against his "
        f"{t['burthen']:.2f}."
    )


def check_ports(ports):
    """The eleven port triples a side, increasing in x (Neuf-D §1.5); every gun of the fit on
    one within 0.01 m is checked with the fit (her road's step 4)."""
    if len(ports) != len(SILLS_FT) or len(ports) != 11:
        raise ValueError(f"neufchatel: {len(ports)} port triples a side; her sheets draw eleven.")
    xs = [round(p[0], 2) for p in ports]
    if any(b <= a for a, b in zip(xs, xs[1:], strict=False)):
        raise ValueError(
            f"neufchatel: her port triples' x do not increase aft to forward, {xs}; a figure is "
            "mistyped."
        )


def check_masts(mast_x, caps):
    """The masts 43.6-43.9 ft apart at the deck (Neuf-D §1.5), and each truck by her masts'
    lengths and rakes within a foot of the sheet's."""
    apart = (mast_x["fore"] - mast_x["main"]) / FT
    lo, hi = MAST_SPACING_FT
    if not lo - 0.05 <= apart <= hi + 0.05:
        raise ValueError(
            f"neufchatel: her masts stand {apart:.2f} ft apart at the deck; Neuf §2.7 measures "
            f"{lo:g}-{hi:g} ft."
        )
    for name, truck in TRUCKS_FT.items():
        top = caps["fore.royal_mast" if name == "fore" else "main.topgallant_mast"] / FT
        if abs(top - truck) > 1.0:
            raise ValueError(
                f"neufchatel: the {name} truck by her masts' lengths and rakes stands {top:.1f} "
                f"ft above her water; ZAZ6179 draws it at {truck:g} ft."
            )
    REPORT.setdefault("checks", []).append(
        f"her masts {apart:.2f} ft apart at the deck; her trucks by their masts' lengths and "
        f"rakes {caps['fore.royal_mast'] / FT:.1f} and {caps['main.topgallant_mast'] / FT:.1f} ft "
        "above her water."
    )


def check_fincham(spars):
    """Each spar the sheet draws within FINCHAM_GUARD_FT of Fincham's figure where both exist,
    but the three that differ (Neuf-D §1.5): a guard against a mistyped figure, not evidence that
    his first example is her (Neuf §3.4). `spars` names hers as FINCHAM does, in feet."""
    off = []
    for name, (his, page) in FINCHAM.items():
        hers = spars[name]
        if abs(hers - his) > FINCHAM_GUARD_FT:
            off.append(f"the {name}, {hers:g} ft against his {his:g} ({page})")
    if off:
        raise ValueError(
            "neufchatel: a spar differs from Fincham 1843 by more than "
            f"{FINCHAM_GUARD_FT:g} ft: {'; '.join(off)}; a figure is mistyped, or the difference "
            "is hers and wants its note (D37 (a))."
        )


def check_sails(cut):
    """Each sail as cut on her spars within SAIL_TOLERANCE of its area measured on ZAZ6179
    (Neuf-D §1.5; Neuf §3.3's +-10-15%). `cut` is {sail id: m2}."""
    off, lines = [], []
    for sid, sqft in SAILS_MEASURED_SQFT.items():
        measured = sqft * FT * FT
        ratio = cut[sid] / measured
        lines.append(f"{sid} {cut[sid]:.0f} m2 against {measured:.0f} ({ratio - 1.0:+.0%})")
        if abs(ratio - 1.0) > SAIL_TOLERANCE:
            off.append(f"{sid}, {cut[sid]:.0f} m2 cut against {measured:.0f} measured")
    if off:
        raise ValueError(
            "neufchatel: a sail as cut on her spars is more than "
            f"{SAIL_TOLERANCE:.0%} off its area on ZAZ6179: {'; '.join(off)}."
        )
    REPORT.setdefault("checks", []).append("her sails as cut: " + "; ".join(lines) + ".")


# ---------------------------------------------------------------------------
# The hull block (Neuf-D §2) and the profile with her shape keys (§3)
# ---------------------------------------------------------------------------

HULL_FIGURES = {
    "length_waterline_m": round(LWL_FT * FT, 1),
    "beam_m": round(TONNAGE["beam_ft"] * FT, 2),
    "draught_m": round(10.36 * FT, 2),
    "displacement_kg": 288000.0,
    "gm_m": 2.1,
    "clr_x_m": -0.6,
    "lateral_area_m2": 102.0,
    "hull_speed_kn": 12.9,
    "deck_height_m": DATUM_M,
    "rudder": {"area_m2": 2.61, "max_angle_deg": 35, "rate_deg_s": 4.0, "span_m": 3.58},
}

HULL_NOTES = {
    "length_waterline_m": "107.3 ft between the post's and the stem's rabbets at her sailing-trim "
    "line (D29 (b); measured on RMG ZAZ6177, +-0.5 ft: Neuf §2.4); 110.1 ft over the post's after "
    "side and the gripe's fore side (measured); 110 ft 8 in on deck (Winfield 1793-1817 pp. "
    "335-336).",
    "beam_m": "25 ft 8 in extreme (Winfield pp. 335-336; ZAZ6177's table '25-8?', read, "
    "tentative); 25 ft 4 in moulded (the table); her line 24.47 ft moulded, 24.8 ft outside the "
    "plank (measured: Neuf §2.4).",
    "draught_m": "10 ft 4 1/2 in mean to the false keel's bottom at the sailing-trim line drawn on "
    "her own lines, 'Draught of Water when in sailing Trim' (ZAZ6177, read): 11 ft 8 3/4 in aft, "
    "9 ft 0 in forward (measured, +-0.25 ft; ZAZ6179 gives about 11.8 and 9.25 independently); "
    "about 0.5 ft less if the faint line is the keel's bottom (Neuf §2.3). D38 (a), D29 (b).",
    "displacement_kg": "Measured at her sailing-trim line, +-10 t (Neuf §2.5: the moulded volume "
    "off the three traced waterlines and the rabbets, the plank, keel and rudder added). The "
    "weight budget for 130 men, 18 guns and stores is about 315 t (judgement): the drawn trim is "
    "plausible, perhaps a little light.",
    "gm_m": "D23 (a): the metacentre 1.59 m above her line (measured, +-0.15 m: Neuf §2.5); "
    "Fincham 1843 p. 19's class ratios on his first example give 2.12 m for a brig of 10 guns and "
    "2.40 for one of 18, the weight budget about 2.2 (judgement). Kept at her tuning, within "
    "2.0-2.2 (Neuf-D §9): no account gives her heel (docs/dev/TuningNotes.md).",
    "clr_x_m": "Tuned against the helm (Neuf-D §9; docs/dev/TuningNotes.md, old beside new), so "
    "that she carries a little weather helm close-hauled in 15 kn and a little with the wind "
    "abeam (judgement): ahead of the geometric centre of the plane the file counts, -0.80 m "
    "without the rudder (measured, Neuf §2.6), by 0.2 m. Her helm falls from close-hauled to the "
    "beam, so that with her fore staysail the 46 m2 that fits forward of her fore mast no single "
    "figure holds both of the helm's bands as first set: each band is widened by 0.2 degrees and "
    "the centre re-tuned to this figure (the owner's ruling for the lead, 2026-11-08). +0.3 to "
    "start; +0.1 before the fore staysail was corrected from its working 93 m2.",
    "lateral_area_m2": "1,100 sq ft to the false keel's bottom, keel, gripe and post counted and "
    "the rudder not (measured, +-5%: Neuf §2.6; D29 (b)); 97 m2 on the faint line and 105 with "
    "the rudder.",
    "hull_speed_kn": "D24 (a): the topsail schooner's 11.5 (on Lynx's hull, the same type) "
    "carried by the root of the waterlines, 107.3 to 85 ft; kept at her tuning, her best in a "
    "strong breeze inside her accounts' band across the whole of 12.5-13.9 (Neuf-D §9: 12.5 a "
    "little under the brig's carried by her length, 13.9 the 1.34 root-length rule the "
    "schooner's note calls too generous; judgement on both bounds; docs/dev/TuningNotes.md).",
    "deck_height_m": "Her flush deck at side at mid-length, 3.8 ft above her line (measured, +-0.3 "
    "ft: Neuf §2.7), Build-Ships.md §5.5's rule for a new file; 'a flush deck fore and aft' (Cobb "
    "1841 p. 38, read), so that D18's options give one datum (Neuf-D §2.2). Cobb's 'trunk of the "
    "quarter deck' (p. 103) is read as a cabin trunk aft, not a deck (judgement), and is not in "
    "the profile.",
    "rudder": "The blade below her line, 28.1 sq ft, its span 11.7 ft to the heel (measured, Neuf "
    "§2.6; ZAZ6179's dashed blade 11.9 ft); the angle and the rate the topsail schooner's "
    "(judgement: no source gives them).",
}

PROFILE_NOTES = {
    "profile": "Her side, decks and ports (Neuf-D §3; Build-Ships.md §5.1): x forward of the "
    "middle of her waterline between the rabbets, z above her sailing-trim line at each station, "
    "metres; measured on RMG ZAZ6177 (her lines, taken off at Deptford in 1815; 7.05 px/ft, +-0.3 "
    "ft) but where a line's note says judgement. Her ports and masts are Neuf's figures forward of "
    "the post at deck height, through the join to the after rabbet (tools/ships/neufchatel.py, "
    "POST_AT_DECK_FT).",
    "profile.rail_m": "The top of her side, ZAZ6177 traced by column, the columns of the mast "
    "stumps and the deck fittings dropped (measured for the design, re-traced by the checker on "
    "both sheets of her lines: aft of her fore channels they agree; forward of them the re-trace "
    "stands higher, reported: docs/dev/TuningNotes.md). About 4 ft above the deck at side (Neuf "
    "§2.7). ZAZ6179, her sail plan, draws it about 7.8 ft above her water at the main and 8.4 at "
    "the fore (measured by the checker), against the lines' 7.5 and 8.1: the lines' figure stands.",
    "profile.breadth_m": "Her line's half-breadths at the 10-ft stations and the rabbets "
    "(measured, +-0.1 ft: Neuf §2.4) and her top breadth's by distance from the post (measured, "
    "not re-measured: Neuf §2.4) through the join, taken as the rail's (judgement: the body plan "
    "draws her topsides near upright); a station added at Neuf's last reading, 104 ft from the "
    "post, her line straight there between the 100-ft station and the rabbet (judgement); forward "
    "of it nothing is read and the rail at the stem is the trend to the stem's siding "
    "(judgement); the after station's rail Neuf's 2-ft reading carried aft. Each with 2 in of "
    "plank (Neuf §2.5). Neuf-D §3.7 task 4 reads the top-timber line.",
    "profile.keel_m": "The false keel's bottom, the scale bar's border on ZAZ6177 (Neuf §2.3; D29 "
    "(b)), 11 ft 8 3/4 in below her line aft and 9 ft 0 in forward at the perpendiculars "
    "(measured); the post's heel by its after edge's raked line produced to it (measured); its "
    "fore end at the gripe's foot, judged straight below the lowest traced point of the stem "
    "(Neuf-D §3.2), the weak point: Neuf-D §3.7 task 2 traces it.",
    "profile.stem_m": "The stem's fore edge as drawn on ZAZ6177, measured at 5x, from the forefoot "
    "to where the head rails meet it and to where the bowsprit's lower edge crosses the bow, the "
    "stem head; its foot on the false keel judged (the weak point), and whether the curve at her "
    "water is the rabbet or the fore edge (Neuf's 110.1 ft over the post and the gripe puts the "
    "fore edge up to 1.95 ft forward of the rabbet) is Neuf-D §3.7 task 2's.",
    "profile.stern_m": "The post's heel; the post's after edge at her water, the hinge line "
    "raking 12.1 degrees (Neuf §2.6); the transom's foot just abaft the post's head; the "
    "taffrail. A flat transom raking from its foot to the taffrail with no counter (measured on "
    "ZAZ6177, re-traced by the checker on ZAZ6177 and ZAZ6178 within 0.2 ft at both ends). "
    "Build-Ships.md §5.7's row gives her stern 'square, about 17 ft': the measure is a raked "
    "transom of 16.1 ft at its corners (Neuf-D §3.5, said plainly; the row amended at her merge, "
    "the lead's ruling).",
    "profile.section_m": "The dead-flat section (measured on ZAZ6177's body plan: Neuf §2.4), her "
    "line taken 8.21 ft above the body plan's base there, with 2 in of plank: the straight floor "
    "rising 27 degrees and the firm bilge. The profile's rabbet stands 8.6-8.7 ft below her line "
    "at that station (the checker's reading of both sheets of her lines), so the section's foot "
    "stands about 0.4 ft above the profile's rabbet: kept in the body plan's own frame (Neuf-D "
    "§3.2).",
    "profile.decks_m": "Her flush deck at side, the red line on ZAZ6177: Neuf §2.7's five points "
    "(the stern 5.0 ft above her line, the lowest at the main 3.4-3.5, mid-length 3.8, the "
    "foremast 4.4, the bow 5.6; measured, +-0.3 ft) and the points between them traced for the "
    "design. The step of about 0.8 ft in the red line near the mainmast (Neuf §2.7, unresolved) "
    "is not drawn.",
    "profile.ports_m": "Her eleven gun ports a side, lids drawn, the same on ZAZ6178; 'pierced "
    "for 22 guns, and mounting 18' (Naval Chronicle vol. 33 p. 72, read).",
    "profile.ports_m.upper": "Each port's x Neuf's centre forward of the post at deck height "
    "(measured, +-0.5 ft) through the join; its sill the port frame's lower edge at the "
    "half-maximum in its middle ten columns (measured, +-0.3 ft; the checker's reading of both "
    "sheets of her lines confirms nine of the eleven within 0.05 ft and reads the third from "
    "forward 0.4 ft higher, reported: docs/dev/TuningNotes.md); its half-breadth the top breadth "
    "at the port's station with 2 in of plank (judgement, an upper bound, until Neuf-D §3.7 task 3 "
    "reads the body plan at each sill). The two squares at the top of the transom on both body "
    "plans (tentative) take no gun and are no triples. The small ports, one about 4.6 ft abaft "
    "each gun port and 0.7-0.85 ft square, probably sweep ports (D11 (a); Chapelle 1930 p. 13), "
    "are not drawn: x " + ", ".join(str(px) for px in SWEEP_PORTS_PX) + " px on ZAZ6177.",
    "profile.port_size_m": "The eleven's mean, 2 ft 8 in wide and 2 ft 6 in deep to the inch "
    "(measured; Neuf's 2.7 by 2.4 ft, +-0.3). The end ports are shallower, 2.18 ft forward and "
    "2.05 ft aft (measured): drawn at the mean their tops stand a few centimetres above the "
    "traced rail, for package 81, which draws the ports.",
    "profile.head_m": "The knee of the head's fore edge, from where the head rails meet the stem "
    "to its top, about 7 ft before the stem (measured on ZAZ6177).",
    "profile.sections_m": "Her three waterlines by station (Neuf §2.3-§2.4, measured, +-0.1 ft): "
    "her sailing-trim line and WL2 and WL3 drawn parallel to it 2.63 and 5.27 ft below, at the "
    "10-ft stations from the after rabbet, each with 2 in of plank.",
    "profile.rabbet_m": "The keel's rabbet, drawn straight and level on ZAZ6177 (Neuf §2.3): 10.1 "
    "ft below her line at the post and 7.5 ft at the forefoot, its middle on the line between "
    "(Neuf's 8.63 ft at that station agrees within 0.11 ft, the checker's 8.60-8.67 likewise); the "
    "keel sided 0.7-0.8 ft (measured). Kept, not drawn (Build-Ships.md §5.0 principle 11).",
    "profile.form": "Her form (Build-Ships.md §5.1): the ends under the water by the design's "
    "default rule (judgement: only the dead flat is drawn below WL3); her stern raked; her head a "
    "knee.",
    "profile.form.stern": "A flat transom along stern_m's rake with no counter (Build-Ships.md "
    "§5.1, raked; measured on ZAZ6177): its foot 4.65 ft above her water just abaft the post's "
    "head, 16.1 ft across its top corners and 16.6 ft at its knuckle on the body plan, so that it "
    "tumbles home above the knuckle, its top arched about 0.35 ft (measured; the checker reads "
    "16.0-16.6 ft on both body plans). The knuckle's breadth is read at the knuckle's height, the "
    "sides near plumb at 16.6-16.8 ft from 4.0 to 7.0 ft above her water (re-read on ZAZ6177's "
    "body plan); the first reading's 15.8 ft, below the knuckle, made the transom wider at its "
    "top than at its foot (2.46 and 2.41 m before, 2.46 and 2.53 now). Reed's modern model "
    "(Winfield pp. 335-336's photograph) shows the same raked transom, for the eye only.",
    "profile.form.head": "A knee: its head rails are drawn; a small terminal at its top is not "
    "resolved at 1280 px, so no billet, scroll or figure is drawn (Build-Ships.md §5.0 principle "
    "9: nothing invented).",
    "profile.marks": "Each line's rung in one word (Build-Ships.md §5.0 principles 3 and 4), the "
    "word of its weakest point: the keel and the stem judged at the gripe's foot, the ports and "
    "the breadth at the top breadth taken for the rail's and the sill's half-breadths, the form's "
    "fullness the default rule and the head's word its terminal unread.",
}

MARKS = {
    "rail_m": "sourced",
    "breadth_m": "judged",
    "keel_m": "judged",
    "stem_m": "judged",
    "stern_m": "sourced",
    "section_m": "sourced",
    "decks_m": "sourced",
    "ports_m": "judged",
    "port_size_m": "sourced",
    "head_m": "sourced",
    "sections_m": "sourced",
    "rabbet_m": "sourced",
    "form.fullness": "judged",
    "form.stern": "sourced",
    # the transom's foot, its breadths at its corners and its foot, and its top's arch, each
    # measured on ZAZ6177's profile and body plan (Neuf-D §3.5); the foot and the breadth
    # re-traced by task 1's checker on both sheets of her lines
    "form.stern.knuckle_z_m": "sourced",
    "form.stern.transom_hb_m": "sourced",
    "form.stern.round_up_m": "sourced",
    "form.head": "judged",
}


def hull_block():
    """Her hull dict, in the house's key order, and its notes (Neuf-D §2.1); `profile_into` adds
    the profile as its last key."""
    return dict(HULL_FIGURES), dict(HULL_NOTES)


def profile_into(p):
    """Her profile and shape keys added to `p.hull` through `g.hull_profile` and `g.hull_form`,
    their notes to `p.hull_notes`; the drawn hull and every triple's gap to the drawn side
    reported (none of the triples' half-breadths was measured at its port: Neuf-D §3.5)."""
    p.hull["profile"] = g.hull_profile(
        p.rail,
        p.breadth,
        keel=p.keel,
        stem=p.stem,
        stern=p.stern,
        section=p.section,
        decks={"upper": p.decks},
        ports={"upper": p.ports},
        port_size={"upper": [PORT_SIZE_FT[0] * FT, PORT_SIZE_FT[1] * FT]},
        head=p.head,
        sections=p.sections,
        rabbet=p.rabbet,
    )
    form = {
        "fullness": [1.0, 1.0],
        "stern": {
            "type": "raked",
            "knuckle_z_m": p.stern[2][1],
            "transom_hb_m": [TRANSOM_HB_FT[0] * FT, TRANSOM_HB_FT[1] * FT],
            "round_up_m": TRANSOM_ROUND_UP_FT * FT,
        },
        "head": "knee",
    }
    drawn = REPORT.setdefault("hull", [])
    drawn.clear()
    REPORT["gaps"] = g.hull_form(p.hull, form=form, marks=MARKS, measured=(), report=drawn)
    p.hull_notes.update(PROFILE_NOTES)


# ---------------------------------------------------------------------------
# Her Builder: the shared helpers' computed figures kept out of her notes
# ---------------------------------------------------------------------------


class HerBuilder(g.Builder):
    """The generator's Builder, with the figures its shared helpers compute from her own keys
    kept out of her notes (the lead's notes of 2026-10-29, item 2): a spar's rating, which is its
    `rating_kn`, and a bowline's size, which is in its rating. What each rule is and what it read
    stays. No other file's notes are touched."""

    RATED = re.compile(r" -> [0-9.]+ kN")
    BOWLINE = re.compile(r"(lighter rope than the sheet), [0-9.]+ in \(judgement\)")

    def _plain_of_figures(self, note):
        note = self.RATED.sub("", note)
        return self.BOWLINE.sub(r"\1 (judgement)", note)

    def rate_spars(self):
        """`Builder.rate_spars`, its figures left in the file's `rating_kn` alone."""
        super().rate_spars()
        self.notes = {key: self._plain_of_figures(note) for key, note in self.notes.items()}


# ---------------------------------------------------------------------------
# The rig's geometry, metres in the file's frame
# ---------------------------------------------------------------------------


def mast_at(p, name, z_water):
    """The x of a lower mast's line, carried up by its rake, at a height above her water."""
    return p.mast_x[name] - math.tan(math.radians(p.rake[name])) * (z_water - DATUM_M)


def area_and_centre(corners):
    """Area m2 and centroid (x, z) of a sail's corners [(x, z), ...]."""
    return g._quad_area_centroid(corners)


def scaled_sizes(sizes, factor):
    """Rope sizes scaled and set to the quarter inch."""
    return {cls: g.quarter(c * factor) for cls, c in sizes.items()}


def trapezoid_m2(head_ft, foot_ft, depth_ft):
    return (head_ft + foot_ft) / 2.0 * depth_ft * FT * FT


SQUARE_PLAN = (
    ("fore.course", "fore.yard", None, 0.9),
    ("fore.topsail", "fore.topsail.yard", "fore.yard", 0.82),
    ("fore.topgallant", "fore.topgallant.yard", "fore.topsail.yard", 0.89),
    ("fore.royal", "fore.royal.yard", "fore.topgallant.yard", 0.89),
    ("main.topgallant", "main.topgallant.yard", "main.topsail.yard", 0.89),
)


def square_cuts():
    """Her square sails by the brig-sloop's method on her yards (Neuf-D §4.3; `brig()` in the
    generator): the head 0.9 of a course's yard and 0.82 of a topsail's and 0.89 of a
    topgallant's or a royal's, the foot 0.9 of the yard below (the course's its head), as deep as
    the hoist between the yards (the course its measured depth); the course's centre 0.45 of its
    depth under its yard, the others' half-way between the yards. Each sail's (area m2, centre
    above her water m, depth ft)."""
    out = {}
    for sid, yard, below, head_of in SQUARE_PLAN:
        length, h = YARDS[yard]
        head = head_of * length
        if below is None:
            depth, foot, centre_ft = COURSE_DEPTH_FT, head, h - 0.45 * COURSE_DEPTH_FT
        else:
            depth = h - YARDS[below][1]
            foot = 0.9 * YARDS[below][0]
            centre_ft = YARDS[below][1] + 0.5 * depth
        out[sid] = (trapezoid_m2(head, foot, depth), z_m(centre_ft), depth)
    return out


def fore_gaff_corners(p):
    """The fore gaff sail's corners [tack, throat, peak, clew], (x, z above her water), metres
    (Neuf-D §4.4; Neuf §1.2, measured): the throat at the gaff's jaws on the mast, the peak at the
    gaff's end peaked as drawn, the tack the luff's length down the mast, the clew abaft the
    mainmast's line at its measured height."""
    length, jaws, peak_deg = GAFFS["fore"]
    zt = z_m(jaws)
    throat = (mast_at(p, "fore", zt), zt)
    a = math.radians(peak_deg)
    peak = (throat[0] - z_m(length * math.cos(a)), zt + z_m(length * math.sin(a)))
    zk = zt - z_m(FORE_GAFF_LUFF_FT * math.cos(math.radians(p.rake["fore"])))
    tack = (mast_at(p, "fore", zk), zk)
    abaft, high = FORE_GAFF_CLEW_FT
    zc = z_m(high)
    clew = (mast_at(p, "main", zc) - z_m(abaft), zc)
    return [tack, throat, peak, clew]


def mainsail_corners(p):
    """The mainsail's corners [tack, throat, peak, clew] from her spars (Neuf-D §4.3): the tack at
    the boom's jaws on the mast, the throat at the gaff's jaws, the peak its head along the gaff,
    the clew its foot along the boom."""
    _length, jaws, peak_deg = GAFFS["main"]
    boom, at_mast, at_end = MAIN_BOOM_FT
    zk = z_m(at_mast)
    tack = (mast_at(p, "main", zk), zk)
    zt = z_m(jaws)
    throat = (mast_at(p, "main", zt), zt)
    a = math.radians(peak_deg)
    head = MAINSAIL_FT["head"]
    peak = (throat[0] - z_m(head * math.cos(a)), zt + z_m(head * math.sin(a)))
    rise = math.asin((at_end - at_mast) / boom)
    foot = MAINSAIL_FT["foot"]
    clew = (tack[0] - z_m(foot * math.cos(rise)), zk + z_m(foot * math.sin(rise)))
    return [tack, throat, peak, clew]


def gaff_topsail_corners(p):
    """The gaff topsail's corners [tack, head, clew] (Neuf-D §4.3; Neuf §1.2): its tack at the main
    gaff's jaws, its luff up the topmast to the topmast's hounds, its clew at the gaff's peak."""
    length, jaws, peak_deg = GAFFS["main"]
    zt = z_m(jaws)
    tack = (mast_at(p, "main", zt), zt)
    a = math.radians(peak_deg)
    clew = (tack[0] - z_m(length * math.cos(a)), zt + z_m(length * math.sin(a)))
    zh = p.hounds["main.topmast"]
    return [tack, (mast_at(p, "main", zh), zh), clew]


def head_spars(p):
    """The stem head (x, z above her water) and the head's three spars as (end x, end z above her
    water, length outboard of the spar below), metres: the bowsprit from the stem head to its cap,
    the jibboom and the flying jibboom each beyond the spar below, at the ends' heights read on
    ZAZ6179 (Neuf-D §4.6)."""
    root = (p.stem[-1][0], p.stem[-1][1])
    run = z_m(BOWSPRIT_OUT_FT) * math.cos(math.radians(BOWSPRIT_STEEVE_DEG))
    out = {"bowsprit": (root[0] + run, z_m(HEAD_SPAR_ENDS_FT["bowsprit"]), z_m(BOWSPRIT_OUT_FT))}
    for spar, below, beyond in (
        ("jib_boom", "bowsprit", JIB_BOOM_BEYOND_FT),
        ("flying_jib_boom", "jib_boom", FLYING_JIB_BOOM_BEYOND_FT),
    ):
        bx, bz, _ = out[below]
        z = z_m(HEAD_SPAR_ENDS_FT[spar])
        reach = z_m(beyond)
        out[spar] = (bx + math.sqrt(max(reach * reach - (z - bz) ** 2, 0.0)), z, reach)
    return root, out


def head_sails(p, root, head):
    """Her three headsails (Neuf-D §4.6), each {area m2, centre x and z above her water}: the
    flying jib as read on ZAZ6179 by task 5 (placed from the flying jibboom's end as drawn, its
    centre its corners', the foot's roach added to their area); the jib and the fore staysail cut
    on her spars as triangles from the tack up the stay to the stay's head and aft along a level
    foot (judgement, until task 5 reads their clews), the fore staysail tacked where the bowsprit
    lies over the stem and the jib at the jibboom's end, each centre its triangle's centroid. The
    jib's area is the design's working figure, its clew where that area puts it (the reviews of
    2026-11-07: the schooner's rule, 0.35 of a foot of 0.35 of her waterline, put its centre above
    its own stay and forward of the flying jib's). The fore staysail's is the triangle that fits
    forward of the fore mast, its clew on the mast at the tack's height (the lead's ruling of
    2026-11-07: the working 93 m2, a derivation of the design's own, put its clew 7.4 m abaft the
    mast, its centre by the schooner's rule 0.35 of a foot of 0.4 of her waterline abaft the
    tack)."""
    fx, fz, _ = head["flying_jib_boom"]
    jx, jz, _ = head["jib_boom"]
    fj = FLYING_JIB_FT
    corners = [
        (fx, fz),
        (fx - z_m(fj["head_aft"]), fz + z_m(fj["head_above"])),
        (fx - z_m(fj["clew_aft"]), fz),
    ]
    a, cx, cz = area_and_centre(corners)
    out = {"flying_jib": {"area": a + fj["roach_sqft"] * FT * FT, "x": cx, "z": cz}}
    for sid, tack, stay_head in (
        ("jib", (jx, jz), p.hounds["fore.topmast"]),
        ("fore.staysail", (root[0], z_m(BOWSPRIT_AT_STEM_FT)), p.hounds["fore.mast"]),
    ):
        top = (mast_at(p, "fore", stay_head), stay_head)
        if sid == "jib":
            area = float(HEADSAIL_WORKING_M2[sid])
            clew_x = tack[0] - 2.0 * area / (top[1] - tack[1])
        else:
            clew_x = mast_at(p, "fore", tack[1])
            area = 0.5 * (tack[0] - clew_x) * (top[1] - tack[1])
        x = (tack[0] + top[0] + clew_x) / 3.0
        out[sid] = {"area": area, "x": x, "z": (2.0 * tack[1] + top[1]) / 3.0, "stay": (tack, top)}
    check_head_sails(p, out)
    return out


def check_head_sails(p, heads):
    """Each headsail cut on her spars stands inside its sail (Neuf-D §1.5; the reviews of
    2026-11-07): its centre below its stay and forward of the fore mast at the centre's height,
    and the jib's abaft the flying jib's, the jib tacking abaft it on the longer stay."""
    off = []
    for sid in ("jib", "fore.staysail"):
        h = heads[sid]
        tack, top = h["stay"]
        stay_z = tack[1] + (tack[0] - h["x"]) * (top[1] - tack[1]) / (tack[0] - top[0])
        if h["z"] >= stay_z:
            off.append(f"the {sid}'s centre {h['z'] - stay_z:.2f} m above its stay")
        if h["x"] <= mast_at(p, "fore", h["z"]):
            off.append(f"the {sid}'s centre abaft the fore mast")
    if heads["jib"]["x"] >= heads["flying_jib"]["x"]:
        off.append("the jib's centre forward of the flying jib's")
    if off:
        raise ValueError(f"neufchatel: a headsail stands outside its sail: {'; '.join(off)}.")


def corners_above_datum(corners):
    """Corners (x, z above her water) as the file's [x, z above the datum], to the centimetre."""
    return [[round(x, 2) + 0.0, round(above_datum(z), 2) + 0.0] for x, z in corners]


# ---------------------------------------------------------------------------
# Writing her file
# ---------------------------------------------------------------------------

# Her era note's first clause, before its parenthesis, is the class her readings serve
# (`api.readings.ship_class_words`, in-world: tests/test_in_world.py), as the privateer schooner's
# is; her capture and her taking off, which no scenario of her years has happened yet, come after.
ERA_NOTES = (
    "A Baltimore privateer hermaphrodite brig of 1812, built at New York (Winfield, British "
    "Warships in the Age of Sail 1793-1817, pp. 335-336; her lines and sail plan, RMG ZAZ6177 and "
    "ZAZ6179): the American privateer Prince de Neufchatel of 328 tons, built in 1812-13, "
    "eighteen guns and 130 men, taken by Leander, Newcastle and Acasta on 28 December 1814 and "
    "taken off at Deptford in 1815; flush-decked, on her own lines, with a brig's square foremast "
    "and a schooner's main, a large loose-footed fore gaff sail lapping the mainmast. Her hull "
    "from her lines, her rig from her sail plan with the yards doubled, Fincham 1843 p. 78 only "
    "for spars it does not draw; see tools/ships/neufchatel.py for every figure's source."
)


HEADER = (
    "# The Prince de Neufchatel: the American privateer hermaphrodite brig of 1812-1814, 328\n"
    "# tons, taken in December 1814 (Winfield 1793-1817 pp. 335-336; RMG ZAZ6177, her lines, and\n"
    "# ZAZ6179, her sail plan, measured on the museum's images and never copied). Generated by\n"
    "# tools/gen_ships.py (tools/ships/neufchatel.py); edit those and rerun, do not edit this\n"
    "# file. Her design: docs/design/Design-Ship-PrinceDeNeufchatel.md. Rope: the brig-sloop's\n"
    "# and the topsail schooner's scaled to her sail (judgement). Spar ratings are provisional,\n"
    "# set for truth 9 with the M1 sail curves; see the script. Canvas: Steel 1794 vol. I; cloth\n"
    "# ratings from the number by Luce App. E. Units: metres, m2, kg, kN. Comments mark\n"
    "# judgements.\n"
)

PROV = " Provisional (truth 9), see gen_ships.py."


def write(out_dir, p):
    """Build her file in full and dump it to `out_dir`."""
    profile_into(p)
    b = HerBuilder("Prince de Neufchatel", "hermaphrodite brig", ERA_NOTES, p.hull, p.hull_notes)
    dw = dict(g.DESIGN_WIND_KN, gaff_topsail=22.0)

    cuts = square_cuts()
    fg_corners = fore_gaff_corners(p)
    ms_corners = mainsail_corners(p)
    gt_corners = gaff_topsail_corners(p)
    gaff_cut = {}
    for sid, corners, mast, back in (
        ("fore.sail", fg_corners, "fore", None),
        ("main.sail", ms_corners, "main", None),
        ("main.gaff_topsail", gt_corners, "main", 0.3 * z_m(GAFFS["main"][0])),
    ):
        a, _cx, cz = area_and_centre(corners)
        if back is None:
            # the topsail schooner's rule: 0.4 of the foot abaft the raked mast at the centre
            foot = math.hypot(corners[0][0] - corners[3][0], corners[0][1] - corners[3][1])
            back = 0.4 * foot
        gaff_cut[sid] = (round(a), mast_at(p, mast, cz) - back, cz)
    root, head = head_spars(p)
    heads = head_sails(p, root, head)

    # her rope's scales (Neuf-D §4.2): her sail on that mast over theirs
    fore_square = sum(cuts[s][0] for s in ("fore.course", "fore.topsail", "fore.topgallant"))
    fore_square += cuts["fore.royal"][0]
    main_sail = gaff_cut["main.sail"][0] + gaff_cut["main.gaff_topsail"][0]
    scale = {
        "fore": math.sqrt(fore_square / THEIRS_M2["brig fore"]),
        "head": math.sqrt(sum(round(h["area"]) for h in heads.values()) / THEIRS_M2["brig head"]),
        "fore gaff": math.sqrt(gaff_cut["fore.sail"][0] / THEIRS_M2["schooner fore sail"]),
        "main": math.sqrt(main_sail / THEIRS_M2["schooner main"]),
        "main topgallant": math.sqrt(
            cuts["main.topgallant"][0] / THEIRS_M2["brig main topgallant"]
        ),
        "main stay": math.sqrt(main_sail / THEIRS_M2["brig main"]),
    }
    REPORT["rope"] = scale
    loads = {sid: (round(a), c, "square") for sid, (a, c, _d) in cuts.items()}
    loads["fore.sail"] = (gaff_cut["fore.sail"][0], gaff_cut["fore.sail"][2], "gaff")
    loads["main.sail"] = (gaff_cut["main.sail"][0], gaff_cut["main.sail"][2], "gaff")
    loads["main.gaff_topsail"] = (
        gaff_cut["main.gaff_topsail"][0],
        gaff_cut["main.gaff_topsail"][2],
        "jibheaded",
    )

    the_lower_and_upper_masts(b, p, loads, dw)
    fore_yards, fore_squares = the_fore(b, p, cuts, loads, scale, dw)
    fg, ms, gt = the_gaff_sails(b, p, gaff_cut, fg_corners, ms_corners, loads, scale, dw)
    main_yards, mtg = main_topgallant(b, p, cuts, scale, loads, dw)
    headsails = head_and_stays(b, p, root, head, heads, scale, dw)
    between = between_the_masts(b, p)
    stuns = studding_sails(b, p, cuts, scale, dw)
    storm = storm_canvas(b, p, ms_corners, heads, scale)

    # every sail cut on her spars against the sheet's (Neuf-D §1.5); the spars against Fincham's
    areas = {s["id"]: s["area_m2"] for s in b.doc["sails"]}
    areas["fore.lower.studdingsail"] = areas["fore.lower.studdingsail.starboard"]
    check_sails(areas)
    check_fincham(
        {
            "main hounded": MASTS["main"]["hounded_ft"],
            "fore hounded": MASTS["fore"]["hounded_ft"],
            "main topmast": sum(UPPER["main"]["topmast"]),
            "fore topmast": FORE_TOPMAST_FT,
            "fore topgallant and royal pole": FORE_TOPGALLANT_FT,
            "jibboom": JIBBOOM_FT,
            "main boom": MAIN_BOOM_FT[0],
            "main gaff": GAFFS["main"][0],
            "fore yard": YARDS["fore.yard"][0],
            "fore topsail yard": YARDS["fore.topsail.yard"][0],
            "fore topgallant yard": YARDS["fore.topgallant.yard"][0],
            "main topsail yard": YARDS["main.topsail.yard"][0],
            "main topgallant yard": YARDS["main.topgallant.yard"][0],
        }
    )
    sails = {
        "fore": fore_squares,
        "gaff": (fg, ms, gt),
        "main topgallant": mtg,
        "head": headsails,
        "between": between,
        "stuns": stuns,
        "storm": storm,
    }
    groups_and_aliases(b, fore_yards, main_yards, sails)
    REPORT["plain"] = sum(areas[s] for s in b.doc["groups"]["plain sail"])
    REPORT["brace"] = brace_check(p)

    # -- her guns, her company and her stores (Neuf-D §5-§7), in the house's order; her
    # description at far detail (§8) ---------------------------------------------------------
    guns = her_guns(p.hull["profile"])
    ground_tackle(b)
    company(b, guns)
    armament(b, guns)
    quarter_bill(b, guns)
    boats_pumps_hold(b)
    b.descriptions([DESCRIPTION])
    b.dump(os.path.join(out_dir, "hermaphrodite-brig.yaml"), HEADER)


def the_lower_and_upper_masts(b, p, loads, dw):
    """Her masts (Neuf-D §4.1): the fore a brig's with a top, its topmast, and its topgallant and
    royal pole in one stick filed as two; the main a schooner's pole mast with crosstrees, its
    topmast and pole in one stick filed as two."""
    fore_sails = ["fore.course", "fore.topsail", "fore.topgallant", "fore.royal"]
    b.spar(
        "fore.mast",
        "mast",
        x_m=p.mast_x["fore"],
        rake_deg=p.rake["fore"],
        height_m=round(above_datum(p.caps["fore.mast"]), 2),
        rating_kn=g.design_kn([loads[s] for s in fore_sails + ["fore.sail"]], dw["lower"]),
        note="fore lower mast, a brig's, with a top (Cobb 1841 p. 91): 58.4 ft heel to hounds and "
        "a 10.1-ft head, 68.5 ft (ZAZ6179, measured, +-1 ft; Fincham 1843 p. 72's first example "
        "58.4 hounded), stepped 6.1 ft below her water (measured), raking 10.3 deg with her water "
        "level (measured; Fincham's 28 in in 12 ft); its cap by its length and rake. x_m its place "
        "at the deck, Neuf's 85.9-86.4 ft forward of the post at deck height (Neuf §2.7) through "
        "the join; Fincham's 0.3 of the waterline before the middle. The fore channel's seven "
        f"chain plates a side on ZAZ6177 (x 817-927 px, measured).{PROV}",
    )
    b.spar(
        "fore.topmast",
        "topmast",
        steps_on="fore.mast",
        height_m=round(p.caps["fore.topmast"] - p.caps["fore.mast"], 2),
        rating_kn=g.design_kn([loads[s] for s in fore_sails[1:]], dw["topsail"]),
        note="fore topmast 34.8 ft, 29.8 to the hounds and a 5.1-ft head (ZAZ6179, measured, not "
        "re-measured: Neuf §3.2; Fincham p. 72's 35.2), its heel at the lower mast's hounds; "
        f"height_m its vertical hoist above the lower cap.{PROV}",
    )
    b.spar(
        "fore.topgallant_mast",
        "topgallant_mast",
        steps_on="fore.topmast",
        height_m=round(p.caps["fore.topgallant_mast"] - p.caps["fore.topmast"], 2),
        rating_kn=g.design_kn([loads[s] for s in fore_sails[2:]], dw["topgallant"]),
        note="fore topgallant mast, 19.3 ft to its hounds (ZAZ6179, measured, not re-measured), "
        "one stick with the royal pole above it, 29.6 ft in all (Fincham's 30.5), filed as two "
        "as the frigate files hers, so that the trim's levels see each yard on its own spar "
        f"(Indf §4.1).{PROV}",
    )
    b.spar(
        "fore.royal_mast",
        "royal_mast",
        steps_on="fore.topgallant_mast",
        height_m=round(p.caps["fore.royal_mast"] - p.caps["fore.topgallant_mast"], 2),
        rating_kn=g.design_kn([loads["fore.royal"]], dw["royal"]),
        note="fore royal mast: the topgallant mast's 10.4-ft pole (ZAZ6179, measured), one stick "
        f"with it; the fore truck drawn 110.4 ft above her water.{PROV}",
    )
    main_sails = ["main.sail", "main.gaff_topsail", "main.topgallant"]
    b.spar(
        "main.mast",
        "mast",
        x_m=p.mast_x["main"],
        rake_deg=p.rake["main"],
        height_m=round(above_datum(p.caps["main.mast"]), 2),
        rating_kn=g.design_kn([loads[s] for s in main_sails], dw["lower"]),
        note="main lower mast, a schooner's pole mast with crosstrees and no top: 'her mainmast "
        "towering high in one piece, with no top as when square rigged, the cross-trees being the "
        "first landing place' (Cobb 1841 p. 91, read); 'her mainmast was rigged as a schooner' "
        "(p. 38). 80.5 ft heel to hounds and an 8.4-ft head, 88.9 ft (ZAZ6179, measured, +-1 ft; "
        "Fincham p. 72's 79.6 hounded), stepped 7.4 ft below her water (measured), raking 12.4 deg "
        "with her water level (measured; Fincham's 33 in in 12 ft); its cap 79.6 ft above her "
        "water read on the sheet (79.4 by its length and rake). x_m its place at the deck, Neuf's "
        "42.3-42.6 ft forward of the post at deck height through the join; Fincham's 0.11 of the "
        "waterline abaft the middle. Her main's three chain plates a side on ZAZ6177 (x 537-620 "
        f"px, measured).{PROV}",
    )
    b.spar(
        "main.topmast",
        "topmast",
        steps_on="main.mast",
        height_m=round(p.caps["main.topmast"] - p.caps["main.mast"], 2),
        rating_kn=g.design_kn([loads[s] for s in main_sails[1:]], dw["gaff_topsail"]),
        note="main topmast 39.6 ft, 27.5 to the hounds and a 12.1-ft pole (ZAZ6179, measured; "
        "Fincham p. 72's 28.2 and 12.1), one stick, filed as two: the topmast to its hounds and "
        "the pole as main.topgallant_mast, so that the trim's levels see each of the main "
        "topgallant's two yards on its own spar (Neuf-D §4.1). Cobb calls it the "
        "'top-gallantmast' (p. 91), housed in the gale to a little above the lower masthead. The "
        f"gaff topsail's luff on it, which comes in early.{PROV}",
    )
    b.spar(
        "main.topgallant_mast",
        "topgallant_mast",
        steps_on="main.topmast",
        height_m=round(p.caps["main.topgallant_mast"] - p.caps["main.topmast"], 2),
        rating_kn=g.design_kn([loads["main.topgallant"]], dw["topgallant"]),
        note="main topgallant 'mast': the main topmast's 12.1-ft pole (ZAZ6179, measured), one "
        "stick with it, on which the main topgallant's upper light yard is crossed; the main truck "
        f"drawn 110.1 ft above her water.{PROV}",
    )


SQUARE_WORDS = {
    "fore.course": "the fore course, a working square sail ('the foresail, on the windward "
    "yard-arm', Cobb 1841 pp. 106-107; 'sheeted down the foresail', p. 105), 33.3 ft deep, its "
    "foot 14 ft above her water (ZAZ6179, measured; 2,000 sq ft as drawn); cut by the brig-sloop's "
    "rule, head and foot 0.9 of its yard; two reefs (Cobb p. 95, 'a double reefed foresail', "
    "which foresail not said).",
    "fore.topsail": "the fore topsail, 30.8 ft deep as drawn (ZAZ6179, measured; 1,700 sq ft); cut "
    "by the brig-sloop's rule between its yard and the fore yardarms, its head 0.82 of its yard; "
    "three reefs (the brig's).",
    "fore.topgallant": "the fore topgallant, 18.6 ft deep as drawn (ZAZ6179, measured; 580 sq ft); "
    "cut by the brig-sloop's rule, its head 0.89 of its yard.",
    "fore.royal": "the fore royal, 10.4 ft deep as drawn (ZAZ6179, measured; 250 sq ft); cut by "
    "the brig-sloop's rule, its head 0.89 of its yard; set flying, as the brig's royals "
    "(judgement).",
    "main.topgallant": "the main topgallant, a square sail about 11.8 ft deep between the main's "
    "two light yards (ZAZ6179, measured: Neuf §1.2; 300 sq ft as drawn); Reed's modern model shows "
    "a small square sail at the main masthead (for the eye only). Cut by the brig-sloop's rule, "
    "its head 0.89 of its yard and its foot 0.9 of the lower light yard, to whose arms it is "
    "sheeted; no reef bands. In 'royals' with the fore royal, so that 'make all sail' sets it and "
    "'shorten sail' takes it in, and never in plain sail, the topgallants, the topsails or the "
    "courses (Neuf-D §4.5; B3.4's finding).",
}

YARD_WORDS = {
    "fore.yard": "Fincham p. 78's 63.25",
    "fore.topsail.yard": "Fincham p. 78's 46.52",
    "fore.topgallant.yard": "the second round's roughly 27.5; Fincham p. 78's 26.67",
    "fore.royal.yard": "Fincham p. 78's 21.3; its proportion, 0.94 of the topgallant yard, noted, "
    "not changed (D37 (a))",
}


def the_fore(b, p, cuts, loads, scale, dw):
    """The fore's four yards and square sails on the brig-sloop's loop (Neuf-D §1.3, §4.2-§4.3),
    a royal above as the brig files hers; their lines by `square_sail_lines`, the brig-sloop's
    fore sizes scaled by the root of her fore square sails over the brig's."""
    plan = (
        ("fore.yard", "fore.mast", "course", "lower", "fore.course"),
        ("fore.topsail.yard", "fore.topmast", "topsail", "topsail", "fore.topsail"),
        (
            "fore.topgallant.yard",
            "fore.topgallant_mast",
            "topgallant",
            "topgallant",
            "fore.topgallant",
        ),
        ("fore.royal.yard", "fore.royal_mast", "royal", "royal", "fore.royal"),
    )
    order = [sid for *_, sid in plan]
    yards, squares = [], []
    for i, (yard_id, mast_id, level, spar_level, sid) in enumerate(plan):
        length, h = YARDS[yard_id]
        limit = BRACE_LIMITS[yard_id]
        yard = b.spar(
            yard_id,
            "yard",
            on=mast_id,
            length_m=round(z_m(length), 2),
            height_m=round(above_datum(z_m(h)), 2),
            brace_limit_deg=limit,
            rating_kn=g.design_kn([loads[s] for s in order[i:]], dw[spar_level]),
            note=f"fore {level} yard about {length:g} ft, drawn as a half-length and doubled, "
            f"{h:g} ft above her water (ZAZ6179, measured; {YARD_WORDS[yard_id]}); braces {limit} "
            "deg from square, the brig-sloop's fore by level (judgement as hers: no source gives "
            f"hers).{PROV}",
        )
        area, centre, _depth = cuts[sid]
        canvas = g.BRIG_CANVAS[sid]
        reef = REEFS.get(sid, 0)
        sail = b.sail(
            sid,
            "square",
            yard=yard,
            area_m2=round(area),
            reef_bands=reef,
            flying=True if level == "royal" else None,
            x_m=g.raked_x(p.mast_x["fore"], p.rake["fore"], round(centre, 1), DATUM_M),
            centre_height_m=round(centre, 1),
            canvas_no=canvas[0],
            cloth_rating_kn=g.cloth(round(area), canvas[0]),
            note=SQUARE_WORDS[sid] + g.canvas_note(canvas),
        )
        sizes = {
            cls: c * g.BRIG_ROPE_SCALE * g.BRIG_MAST_ROPE_FACTOR["fore"]
            for cls, c in g.FRIGATE_ROPE[level].items()
        }
        g.square_sail_lines(
            b,
            sail,
            yard,
            scaled_sizes(sizes, scale["fore"]),
            hoisting=(level != "course"),
            course=(level == "course"),
            reef=(reef > 0),
            bowline=(level == "topsail"),
        )
        yards.append(yard)
        squares.append(sail)
    return yards, squares


def the_gaff_sails(b, p, gaff_cut, fg_corners, ms_corners, loads, scale, dw):
    """The fore gaff sail on the topsail schooner's foresail (D21 (a); Neuf-D §4.4) and the main's
    gaff, boom, mainsail and gaff topsail on the schooner's (Neuf-D §1.3), the schooner's lines
    scaled by the root of her sail over the schooner's (Neuf-D §4.2)."""
    fgaff = b.spar(
        "fore.gaff",
        "gaff",
        on="fore.mast",
        length_m=round(z_m(GAFFS["fore"][0]), 2),
        height_m=round(above_datum(z_m(GAFFS["fore"][1])), 2),
        rating_kn=g.design_kn([loads["fore.sail"]], dw["gaff"]),
        note="fore gaff 32.9 ft, its jaws 46.9 ft above her water just below the fore yard, "
        "peaked about 27 deg (ZAZ6179, measured; the peak judgement: Neuf §1.2). Fincham p. 78 "
        "gives 37.1, the main gaff's; hers is shorter as drawn (D37 (a)).",
    )
    area, x, z = gaff_cut["fore.sail"]
    canvas = g.SCHOONER_CANVAS["fore.sail"]
    fg = b.sail(
        "fore.sail",
        "gaff",
        mast="fore.mast",
        gaff=fgaff,
        area_m2=area,
        reef_bands=REEFS["fore.sail"],
        x_m=round(x, 1),
        centre_height_m=round(z, 1),
        canvas_no=canvas[0],
        cloth_rating_kn=g.cloth(area, canvas[0]),
        corners_m=corners_above_datum(fg_corners),
        note="the fore gaff sail, Cobb's 'fore-and-aft foresail' (1841 pp. 33-34, 79), under "
        "which she lay to in the gale: boomless and loose-footed, lapping the main (D21 (a)), its "
        "gaff 32.9 ft, its luff about 37.9 ft down the mast, its clew 2.7-2.9 ft abaft the "
        "mainmast's line and 12.6 ft above her water (ZAZ6179, measured: Neuf §1.2; 1,660 sq ft "
        "+-10% as drawn), its foot drawn curved; corners [tack, throat, peak, clew] above the "
        "datum. Built on the topsail schooner's foresail: its centre 0.4 of the foot abaft the "
        "raked mast (the schooner's rule), its height its corners'; its sheet shifted round the "
        "mainmast in stays as hers is. Two reefs (Cobb p. 95, 'a double reefed foresail', which "
        "foresail not said). The viewer draws a gaff without corners at 35 deg and a loose foot "
        "1.5 m above the datum, recorded (Neuf-D §4.4)." + g.canvas_note(canvas),
    )
    fgs = scaled_sizes({"halyard": 3.0, "sheet": 3.5, "tack": 3.5}, scale["fore gaff"])
    b.line(
        "fore.gaff.throat_halyard",
        "throat_halyard",
        fgaff,
        rating=g.rope_kn(fgs["halyard"], 4),
        note="the topsail schooner's foresail's lines scaled by the root of her fore gaff sail "
        "over the schooner's (judgement, Neuf-D §4.2).",
    )
    b.line("fore.gaff.peak_halyard", "peak_halyard", fgaff, rating=g.rope_kn(fgs["halyard"], 4))
    b.sided("fore.sail.sheet", "sheet", fg, rating=g.rope_kn(fgs["sheet"]))
    b.line("fore.sail.tack", "tack", fg, rating=g.rope_kn(fgs["tack"]))
    mgaff = b.spar(
        "main.gaff",
        "gaff",
        on="main.mast",
        length_m=round(z_m(GAFFS["main"][0]), 2),
        height_m=round(above_datum(z_m(GAFFS["main"][1])), 2),
        rating_kn=g.design_kn([loads["main.sail"]], dw["gaff"]),
        note="main gaff 37.3 ft, its jaws 64.4 ft above her water, peaked 24 deg, its peak about "
        "79.5 ft (ZAZ6179, measured; Fincham p. 78's 37.1). Fincham 1843 art. 91 puts the nock of "
        "a brig forward and schooner aft 2.3 to 2.5 x the breadth above the water; hers 2.51 "
        "(Neuf §3.3).",
    )
    mboom = b.spar(
        "main.boom",
        "boom",
        on="main.mast",
        length_m=round(z_m(MAIN_BOOM_FT[0]), 2),
        height_m=round(above_datum(z_m(MAIN_BOOM_FT[1])), 2),
        horse_m=HORSE_M,
        rating_kn=g.design_kn([loads["main.sail"]], dw["gaff"]),
        note="main boom 64.2 ft, 10.4 ft above her water at the mast and 16.4 at its end, "
        "overhanging the taffrail 19.6 ft (ZAZ6179, measured; Fincham p. 78's 64.46). horse_m is "
        "the horse across the stern for the sheet to travel on (Steel 1794 vol. I, p. 167, HORSE: "
        "'a thick iron rod, fastened at the ends to the inside of the stern of vessels that carry "
        "a fore and aft mainsail, for the main sheet to travel on'), across her transom, 16.1 ft "
        "at its top (measured), its span the transom's inside breadth, about 4.6 m (judgement); "
        "the sheet's geometry reads it (evolutions/trim.py).",
    )
    area, x, z = gaff_cut["main.sail"]
    canvas = g.SCHOONER_CANVAS["main.sail"]
    ms = b.sail(
        "main.sail",
        "gaff",
        mast="main.mast",
        gaff=mgaff,
        boom=mboom,
        area_m2=area,
        reef_bands=REEFS["main.sail"],
        x_m=round(x, 1),
        centre_height_m=round(z, 1),
        canvas_no=canvas[0],
        cloth_rating_kn=g.cloth(area, canvas[0]),
        corners_m=corners_above_datum(ms_corners),
        note="the mainsail, a schooner's on gaff and boom, Cobb's 'fore-and-aft mainsail' (1841 "
        "p. 95): luff 55, head 35, leech 65 and foot 62 ft (ZAZ6179, re-measured: Neuf §3.3; "
        "2,780 sq ft as drawn); its head along the gaff from the jaws and its foot along the boom "
        "from the mast, corners [tack, throat, peak, clew] above the datum. Its centre 0.4 of the "
        "foot abaft the raked mast (the schooner's rule), its height its corners'. Three reefs "
        "('closely reefed', Cobb p. 95; the schooner's three)." + g.canvas_note(canvas),
    )
    mss = scaled_sizes(
        {"throat": 3.5, "peak": 3.0, "sheet": 4.0, "outhaul": 2.5, "vang": 2.5}, scale["main"]
    )
    b.line(
        "main.gaff.throat_halyard",
        "throat_halyard",
        mgaff,
        rating=g.rope_kn(mss["throat"], 4),
        note="the topsail schooner's main's lines scaled by the root of her mainsail and gaff "
        "topsail over the schooner's (judgement, Neuf-D §4.2).",
    )
    b.line("main.gaff.peak_halyard", "peak_halyard", mgaff, rating=g.rope_kn(mss["peak"], 5))
    b.line(
        "main.sail.sheet",
        "sheet",
        ms,
        rating=g.rope_kn(mss["sheet"], 3),
        parts=3,
        note="a threefold purchase, as the schooner's.",
    )
    b.line("main.sail.outhaul", "outhaul", ms, rating=g.rope_kn(mss["outhaul"]))
    b.sided("main.gaff.vang", "vang", mgaff, rating=g.rope_kn(mss["vang"]))
    area, x, z = gaff_cut["main.gaff_topsail"]
    canvas = g.SCHOONER_CANVAS["main.gaff_topsail"]
    gt = b.sail(
        "main.gaff_topsail",
        "jibheaded",
        mast="main.topmast",
        area_m2=area,
        x_m=round(x, 1),
        centre_height_m=round(z, 1),
        canvas_no=canvas[0],
        cloth_rating_kn=g.cloth(area, canvas[0]),
        note="the main gaff topsail, nearly jib-headed, the American form (Chapelle 1930 pp. "
        "174-175; D10's note): drawn from the gaff's peak to a short head spar of 4.3-4.6 ft "
        "angled aft from near the topmast's hounds (ZAZ6179, measured; 470 sq ft as drawn), its "
        "head spar recorded, not modelled; cut from the gaff's jaws up the topmast to its hounds "
        "and out to the gaff's peak; its centre 0.3 of the gaff abaft the raked mast (the "
        "schooner's rule), its height its corners'." + g.canvas_note(canvas),
    )
    gts = g.quarter(2.5 * scale["main"])
    b.line("main.gaff_topsail.halyard", "halyard", gt, rating=g.rope_kn(gts))
    b.line("main.gaff_topsail.sheet", "sheet", gt, rating=g.rope_kn(gts))
    b.line("main.gaff_topsail.tack", "tack", gt, rating=g.rope_kn(gts))
    return fg, ms, gt


def main_topgallant(b, p, cuts, scale, loads, dw):
    """Her main topgallant on its two light yards (Neuf-D §4.5; D10 as ruled on 2026-11-06, the
    rule in the key's place): the lower light yard at the topmast's hounds, carrying no sail, the
    topgallant's sheets at its arms, its lifts and braces a yard's; the upper on the topmast's
    pole with a halyard; the square sail between them. No key: the engine's rule reads the two
    yards as a fore-and-after's main's, her after yards (`Ship.on_schooner_mast`, B3.4). Returns
    the two yards, lower first, and the sail."""
    tg_sizes = {
        cls: c * g.BRIG_ROPE_SCALE * g.BRIG_MAST_ROPE_FACTOR["main"]
        for cls, c in g.FRIGATE_ROPE["topgallant"].items()
    }
    sizes = scaled_sizes(tg_sizes, scale["main topgallant"])
    length, h = YARDS["main.topsail.yard"]
    lower = b.spar(
        "main.topsail.yard",
        "yard",
        on="main.topmast",
        length_m=round(z_m(length), 2),
        height_m=round(above_datum(z_m(h)), 2),
        brace_limit_deg=BRACE_LIMITS["main.topsail.yard"],
        rating_kn=g.design_kn([loads["main.topgallant"]], dw["topgallant"]),
        note="the main's lower light yard, 34.4-35 ft doubled, at the topmast's hounds 95.7 ft "
        "above her water (ZAZ6179, measured: Neuf §1.2; Fincham p. 78's main topsail yard 36.3); "
        "it carries no sail, the main topgallant's sheets going to its arms, and is filed because "
        "her plan draws it and the sail's foot is sheeted to it (Neuf-D §4.5); its lifts and "
        "braces a yard's, rated for the topgallant's sheet load. Braces 60 deg from square "
        "(judgement). No key: a yard on a mast with no yard on its lower mast is a "
        "fore-and-after's after yard by the engine's rule (the lead's ruling of "
        f"2026-11-06).{PROV}",
    )
    b.sided(
        "main.topsail.yard.brace",
        "brace",
        lower,
        rating=g.rope_kn(sizes["brace"]),
        note="the light yards' lines the brig-sloop's main topgallant's, scaled by the root of "
        "her main topgallant over the brig's (judgement, Neuf-D §4.2).",
    )
    b.sided("main.topsail.yard.lift", "lift", lower, rating=g.rope_kn(sizes["lift"]))
    length, h = YARDS["main.topgallant.yard"]
    upper = b.spar(
        "main.topgallant.yard",
        "yard",
        on="main.topgallant_mast",
        length_m=round(z_m(length), 2),
        height_m=round(above_datum(z_m(h)), 2),
        brace_limit_deg=BRACE_LIMITS["main.topgallant.yard"],
        rating_kn=g.design_kn([loads["main.topgallant"]], dw["topgallant"]),
        note="the main's upper light yard, 23.6-25 ft doubled, near the truck 107.5 ft above her "
        "water (ZAZ6179, measured; Fincham p. 78's main topgallant yard 23.22); with a halyard. "
        "Braces 62 deg from square (judgement). Fincham's main square-sail yard of 48.4 ft beneath "
        f"is not drawn on her plan and is not carried (D10 (d)).{PROV}",
    )
    area, centre, _depth = cuts["main.topgallant"]
    canvas = g.BRIG_CANVAS["main.topgallant"]
    sail = b.sail(
        "main.topgallant",
        "square",
        yard=upper,
        area_m2=round(area),
        reef_bands=0,
        x_m=g.raked_x(p.mast_x["main"], p.rake["main"], round(centre, 1), DATUM_M),
        centre_height_m=round(centre, 1),
        canvas_no=canvas[0],
        cloth_rating_kn=g.cloth(round(area), canvas[0]),
        note=SQUARE_WORDS["main.topgallant"] + g.canvas_note(canvas),
    )
    g.square_sail_lines(b, sail, upper, sizes, hoisting=True)
    return [lower, upper], sail


HEAD_WORDS = {
    "flying_jib": "the flying jib on the flying jib stay, its corners as drawn on ZAZ6179 (read by "
    "the checker, Neuf-D §3.7 task 5: its head 66.5-67.1 ft above her water, its clew and tack "
    "about 25.5, its foot 21 ft with a little roach, about 447 sq ft), placed from the flying "
    "jibboom's end as drawn. Three headsails are drawn, the count tentative (D35).",
    "jib": "the jib on the jib stay, from the fore topmast head to the jibboom's end (read on "
    "ZAZ6179 by the checker), its clew not read: its area the design's working figure, 121 m2, "
    "cut on her spars (judgement, Neuf-D §4.3 and §4.6, until task 5 reads it): its tack at the "
    "jibboom's end, its centre a triangle's from the tack up its stay to the fore topmast's "
    "hounds and aft along a level foot to the clew its area gives (judgement): the topsail "
    "schooner's rule, its centre 0.35 of a foot of 0.35 of her waterline abaft the tack, put it "
    "above its own stay and forward of the flying jib's. Cobb's jib was "
    "'closely reefed' (1841 p. 95), but no evolution reefs a jib (data/evolutions/): filed "
    "without reef bands, the storm jib standing in, and reported for a later package (Neuf-D "
    "§17, lead item 7).",
    "fore.staysail": "the fore staysail on the fore stay, tacked where the bowsprit lies over "
    "the stem at the height ZAZ6179 draws it (judgement), its clew not read: cut as the triangle "
    "that fits forward of the fore mast, its luff up the fore stay to the fore hounds, its foot "
    "level from the tack to the mast and its leech down the mast (judgement, until task 5 reads "
    "it), its centre that triangle's. The design's working 93 m2 (Neuf-D §4.3, §4.6) was a "
    "derivation of its own, closing Fincham's remainder for the jib and the fore topmast "
    "staysail with the jib (Neuf §2.8), not her sail plan's figure, which is not read: so "
    "triangled its clew stood 7.4 m abaft the fore mast. Corrected to the triangle that fits, "
    "the lead's ruling of 2026-11-07.",
}


def head_and_stays(b, p, root, head, heads, scale, dw):
    """The head's spars, the stays, shrouds and backstays, and the three headsails on the
    brig-sloop's head (Neuf-D §4.6), the brig's standing rigging and head sails' lines scaled by
    the root of her fore square sails and of her headsails over the brig's (Neuf-D §4.2)."""
    head_loads = {sid: (round(h["area"]), h["z"], "jibheaded") for sid, h in heads.items()}
    _bx, bz, bl = head["bowsprit"]
    bowsprit = b.spar(
        "bowsprit",
        "bowsprit",
        x_m=round(root[0], 2),
        length_m=round(bl, 2),
        height_m=round(above_datum(bz), 2),
        rating_kn=g.design_kn(list(head_loads.values()), dw["lower"]),
        note="bowsprit 22.4 ft outboard from the stem to the cap, steeved about 15 deg (ZAZ6179, "
        "measured: Neuf §1.2; 14.9 deg on ZAZ6177 for the drag; Fincham's 36 in in 12 ft, 14.0 "
        "deg); housed 9.0 ft (Fincham's 0.35 of the breadth; judgement for hers). x_m its root at "
        "the stem head, length_m its part outboard, height_m its cap above the datum where "
        "ZAZ6179 draws it (measured by the checker): her sail plan draws the bowsprit over the "
        "stem about 10 ft above her water, her lines' stem head lower, Neuf-D §3.7 task 7 reading "
        "its heel. 'The Jack', a spar drawn under the bowsprit near its cap (14.6-15.0 ft, or 30 "
        "if halved), the lower studding sail's leech running down to it, is not built (D8 (b) as "
        "answered: the 64's and the bilander's yards only; Neuf-D §4.6).",
    )
    _jx, jz, jl = head["jib_boom"]
    jib_boom = b.spar(
        "jib_boom",
        "jib_boom",
        on=bowsprit,
        length_m=round(jl, 2),
        height_m=round(above_datum(jz), 2),
        rating_kn=g.design_kn([head_loads["jib"], head_loads["flying_jib"]], dw["jib_boom"]),
        note="jibboom 38.7 ft heel to end (ZAZ6179, measured: Neuf §1.2; Fincham's 38.9 on the "
        "hounded reading), 26.2 ft of it beyond the bowsprit's cap and its end 22.8 ft above her "
        f"water (measured on ZAZ6179 by the checker).{PROV}",
    )
    _fx, fz, fl = head["flying_jib_boom"]
    b.spar(
        "flying_jib_boom",
        "flying_jib_boom",
        on=jib_boom,
        length_m=round(fl, 2),
        height_m=round(above_datum(fz), 2),
        rating_kn=g.design_kn([head_loads["flying_jib"]], dw["flying_jib_boom"]),
        note="flying jibboom about 11 ft beyond the jibboom (+-3 ft), its end 57.2 ft ahead of the "
        "stem head (ZAZ6179, measured: Neuf §1.2) and 25.5 ft above her water (measured by the "
        f"checker); Fincham's 15.6 noted (D37 (a)).{PROV}",
    )
    f, hd, m = scale["fore"], scale["head"], scale["main"]
    b.line(
        "fore.stay",
        "stay",
        "fore.mast",
        rating=g.rope_kn(g.quarter(11.0 * f)),
        note="from the fore mast's hounds to the bowsprit at the stem; the fore staysail and the "
        "fore storm staysail set on it. The fore's and the head's standing rigging the "
        "brig-sloop's scaled by the root of her fore square sails over the brig's (judgement, "
        "Neuf-D §4.2).",
    )
    b.line("fore.topmast.stay", "stay", "fore.topmast", rating=g.rope_kn(g.quarter(6.0 * f)))
    b.line(
        "jib.stay",
        "stay",
        "fore.topmast",
        rating=g.rope_kn(g.quarter(4.0 * hd)),
        note="from the fore topmast head to the jibboom's end (ZAZ6179, read by the checker): the "
        "jib sets on it.",
    )
    b.line(
        "flying_jib.stay",
        "stay",
        "fore.topgallant_mast",
        rating=g.rope_kn(g.quarter(3.0 * hd)),
        note="from the fore topgallant mast head to the flying jibboom's end (ZAZ6179, read by the "
        "checker): the flying jib sets on it.",
    )
    b.line(
        "main.stay",
        "stay",
        "main.mast",
        rating=g.rope_kn(g.quarter(12.0 * scale["main stay"])),
        note="from the main mast's hounds to the fore mast 13 ft above her water (ZAZ6179, read by "
        "the checker), as a brig's (Steel 1794 vol. I, 'The main-staysail'); the main staysail "
        "sets on it. The brig-sloop's main stay scaled by the root of her main's sail over the "
        "brig's main (judgement: the schooner files none).",
    )
    b.line(
        "main.topmast.stay",
        "stay",
        "main.topmast",
        rating=g.rope_kn(g.quarter(4.0 * m)),
        note="from the main topmast's hounds to the fore topmast's (ZAZ6179, read by the checker): "
        "the main topmast staysail sets on it. The main's standing rigging the topsail schooner's "
        "scaled by the root of her mainsail and gaff topsail over the schooner's (judgement, "
        "Neuf-D §4.2).",
    )
    b.line("bobstay", "stay", bowsprit, rating=g.rope_kn(g.quarter(9.0 * hd)))
    b.line("martingale", "stay", jib_boom, rating=g.rope_kn(g.quarter(4.0 * hd)))
    b.sided(
        "fore.shrouds",
        "shroud",
        "fore.mast",
        rating=g.rope_kn(g.quarter(7.5 * f), 4),
        note="four shrouds a side of the fore channel's seven chain plates (ZAZ6177, measured; "
        "four shrouds and three backstays, judgement).",
    )
    b.sided(
        "fore.topmast.backstay",
        "backstay",
        "fore.topmast",
        rating=g.rope_kn(g.quarter(5.0 * f), 3),
        note="three backstays a side, the fore channel's other three chain plates (judgement).",
    )
    b.sided(
        "main.shrouds",
        "shroud",
        "main.mast",
        rating=g.rope_kn(g.quarter(6.5 * m), 3),
        note="three shrouds a side, the main's three chain plates (ZAZ6177, measured; judgement).",
    )
    b.sided(
        "main.topmast.backstay",
        "backstay",
        "main.topmast",
        rating=g.rope_kn(g.quarter(3.5 * m)),
        note="one backstay a side, set up to the main channel (judgement).",
    )
    sizes = {"fore.staysail": 3.0, "jib": 3.0, "flying_jib": 2.0}
    stays = {"fore.staysail": "fore.stay", "jib": "jib.stay", "flying_jib": "flying_jib.stay"}
    out = []
    for sid in ("fore.staysail", "jib", "flying_jib"):
        h = heads[sid]
        area = round(h["area"])
        canvas = g.SCHOONER_CANVAS[sid]
        s = b.sail(
            sid,
            "jibheaded",
            stay=stays[sid],
            area_m2=area,
            x_m=round(h["x"], 1),
            centre_height_m=round(h["z"], 1),
            canvas_no=canvas[0],
            cloth_rating_kn=g.cloth(area, canvas[0]),
            note=HEAD_WORDS[sid] + g.canvas_note(canvas),
        )
        size = g.quarter(sizes[sid] * hd)
        b.line(f"{sid}.halyard", "halyard", s, rating=g.rope_kn(size, 2))
        b.sided(
            f"{sid}.sheet",
            "sheet",
            s,
            rating=g.rope_kn(size),
            note=(
                "the brig-sloop's head sails' lines scaled by the root of her three headsails "
                "over the brig's (judgement, Neuf-D §4.2)."
                if sid == "fore.staysail"
                else None
            ),
        )
        b.line(f"{sid}.downhaul", "downhaul", s, rating=g.rope_kn(g.quarter(size * 0.8)))
        out.append(s)
    return out


def staysail(b, sid, stay, corners, canvas, rope_in, words):
    """A staysail of these corners (x, z above her water) on its stay: its area and centre from
    its corners, filed with them above the datum; its halyard, sheets and downhaul, the size
    raised to bear its cloth as `g.staysail_from_cut` raises it (judgement)."""
    area_m2, cx, cz = area_and_centre(corners)
    area = round(area_m2)
    s = b.sail(
        sid,
        "jibheaded",
        stay=stay,
        area_m2=area,
        x_m=round(cx, 1),
        centre_height_m=round(cz, 1),
        canvas_no=canvas[0],
        cloth_rating_kn=g.cloth(area, canvas[0]),
        corners_m=corners_above_datum(corners),
        note=words + g.canvas_note(canvas),
    )
    bear = math.ceil(4.0 * math.sqrt(0.5 * g.cloth(area, canvas[0]) / g.ROPE_KN_PER_SQ_IN)) / 4.0
    rope_in = max(rope_in, bear)
    b.line(f"{sid}.halyard", "halyard", s, rating=g.rope_kn(rope_in, 2))
    b.sided(
        f"{sid}.sheet",
        "sheet",
        s,
        rating=g.rope_kn(rope_in),
        note="to bear its sail: its working load half the cloth's rating (judgement).",
    )
    b.line(f"{sid}.downhaul", "downhaul", s, rating=g.rope_kn(g.quarter(rope_in * 0.8)))
    return s


def on_line(a, b_, z):
    """The point at height z on the line through a and b_ (x, z)."""
    return (a[0] + (z - a[1]) * (b_[0] - a[0]) / (b_[1] - a[1]), z)


def between_the_masts(b, p):
    """The main staysail and the main topmast staysail on her plan (Neuf-D §4.7), cut on her
    stays as drawn (ZAZ6179, read by the checker); no middle or main topgallant staysail. The
    brig-sloop's sizes (`gen_ships.between_the_masts`, brig), raised to bear the cloth."""
    ms = MAIN_STAYSAIL_FT
    upper = (mast_at(p, "main", p.hounds["main.mast"]), p.hounds["main.mast"])
    zl = z_m(ms["stay_fore"])
    tack = (mast_at(p, "fore", zl), zl)
    head = on_line(upper, tack, z_m(ms["head"]))
    clew = (head[0] + z_m(ms["clew_forward"]), z_m(ms["clew"]))
    main_ss = staysail(
        b,
        "main.staysail",
        "main.stay",
        [tack, head, clew],
        g.BRIG_CANVAS["main.staysail"],
        3.0,
        "the main staysail, a triangle on the main stay as drawn (ZAZ6179, read by the checker: "
        "its head on the stay 47.4 ft above her water, its tack at the stay's foot on the fore "
        "mast 13 ft above her water, its clew 8.1 ft above her water and 6.9 ft forward of the "
        "head; 530-540 sq ft, Neuf §3.3, whose '60 ft' for the head is 47 ft by its own pixel); "
        "corners [tack, peak, clew] above the datum. It shares the space between the masts with "
        "the fore gaff sail, she setting one or the other (judgement); never in plain sail; lying "
        "to under it is 'a mean between the two others' (Steel 1794 vol. II).",
    )
    mts = MAIN_TOPMAST_STAYSAIL_FT
    top = (mast_at(p, "main", p.hounds["main.topmast"]), p.hounds["main.topmast"])
    fore_top = (mast_at(p, "fore", p.hounds["fore.topmast"]), p.hounds["fore.topmast"])
    peak = on_line(top, fore_top, z_m(mts["peak"]))
    zf = z_m(mts["upper_foot"])
    clew = (peak[0], zf)
    tack = (mast_at(p, "fore", zf), zf)
    # the luff up the fore topmast to the stay's fore end at its hounds (the reviews of
    # 2026-11-07: a nock on the stay carried forward of its end stood clear of the raked mast)
    nock = fore_top
    main_tss = staysail(
        b,
        "main.topmast_staysail",
        "main.topmast.stay",
        [tack, nock, peak, clew],
        g.BRIG_CANVAS["main.topmast_staysail"],
        2.5,
        "the main topmast staysail, 'large', its luff on the main topmast stay to the fore topmast "
        "crosstrees and its leech upright just forward of the main (ZAZ6179, read by the checker: "
        "its peak on the stay 91.2 ft above her water); its foot drawn dashed at two heights, 72.9 "
        "and 44.9 ft above her water. The upper foot is taken (judgement, Neuf-D §4.7: it clears "
        "the fore gaff sail's peak, 61.7 ft, so both can stand; the lower would lie over the gaff "
        "sail, and as drawn makes about 1,330 sq ft against the upper's 400); its tack at the fore "
        "topmast. Corners [tack, nock, peak, clew] above the datum (D35: the build picks one of "
        "the staysail's two drawn feet and marks it).",
    )
    return [main_ss, main_tss]


def studding_sails(b, p, cuts, scale, dw):
    """The fore's three pairs of studding sails on the brig's ids, parents and lines (Neuf-D §4.7;
    D35 (b) limited); none on the main (none drawn). Each boom the one spreading its sail's foot
    at the yard below, as the brig-sloop's file has them: the lower studding sail's the swinging
    boom, the topmast studding sail's the fore yard's boom, the topgallant studding sail's the
    fore topsail yard's."""
    fx, rake = p.mast_x["fore"], p.rake["fore"]
    _ts_area, ts_c, ts_depth = cuts["fore.topsail"]
    _tg_area, tg_c, tg_depth = cuts["fore.topgallant"]
    lower_w, lower_d = LOWER_STUNS_FT
    yard_h = YARDS["fore.yard"][1]
    plan = (
        (
            "lower",
            "fore.yard",
            SWINGING_BOOM_FT,
            above_datum(z_m(yard_h - lower_d)),
            lower_w * lower_d * FT * FT,
            z_m(yard_h - 0.5 * lower_d),
            "the fore lower studding sail, drawn solid, about 19 ft wide and 35 ft deep under the "
            "fore yard (ZAZ6179, measured: Neuf §1.2), its head spread on the fore yard's boom and "
            "its foot on the swinging boom; its outer leech drawn down to 'the Jack' (not built).",
            "the swinging boom, the lower studding sail's foot: Fincham 1843 p. 78's 43.01 ft (not "
            "drawn; judgement for hers), at the sail's foot",
        ),
        (
            "topmast",
            "fore.topsail.yard",
            STUNS_BOOM_FT["fore.yard"],
            above_datum(z_m(yard_h)),
            0.4 * YARDS["fore.topsail.yard"][0] * ts_depth * FT * FT,
            ts_c,
            "the fore topmast studding sail, drawn dashed (ZAZ6179): by the brig-sloop's "
            "proportion on her spars, 0.4 of the topsail yard wide and as deep as the topsail "
            "(judgement, until Neuf-D §3.7 task 5 reads its outline).",
            "the fore yard's studding-sail boom, run out 16.1 ft beyond the yardarm (ZAZ6179, "
            "measured), spreading the topmast studding sail's foot at the fore yard as the "
            "brig-sloop's file has it; Neuf-D §4.7 puts this sail on the topsail yard's boom, read "
            "here by the engine's pattern, a studding sail's boom the one at its foot",
        ),
        (
            "topgallant",
            "fore.topgallant.yard",
            STUNS_BOOM_FT["fore.topsail.yard"],
            above_datum(z_m(YARDS["fore.topsail.yard"][1])),
            0.4 * YARDS["fore.topgallant.yard"][0] * tg_depth * FT * FT,
            tg_c,
            "the fore topgallant studding sail, partly made out on ZAZ6179 (the owner's choice, "
            "D35 (b)): by the brig-sloop's proportion on her spars (judgement, until task 5 reads "
            "it).",
            "the fore topsail yard's studding-sail boom, run out 6.9 ft beyond the yardarm "
            "(ZAZ6179, measured), spreading the topgallant studding sail's foot at the topsail "
            "yard as the brig-sloop's file has it",
        ),
    )
    stuns = []
    for level, parent, boom_ft, boom_h, area_m2, centre, sail_words, boom_words in plan:
        area = round(area_m2)
        canvas = g.BRIG_CANVAS[f"{level} studding"]
        size = g.quarter({"lower": 2.5, "topmast": 2.0, "topgallant": 1.75}[level] * scale["fore"])
        for side in g.SIDES:
            first = side == g.SIDES[0]
            boom = b.spar(
                f"fore.{level}.studdingsail_boom.{side}",
                "studdingsail_boom",
                on=parent,
                side=side,
                length_m=round(z_m(boom_ft), 2),
                height_m=round(boom_h, 2),
                rating_kn=g.design_kn([(area, centre, "studding")], dw["studding"]),
                note=(
                    f"{boom_words}; rated for its sail in {dw['studding']:.0f} kn.{PROV}"
                    if first
                    else None
                ),
            )
            sid = b.sail(
                f"fore.{level}.studdingsail.{side}",
                "studding",
                boom=boom,
                yard=parent,
                side=side,
                area_m2=area,
                x_m=g.raked_x(fx, rake, round(centre, 1), DATUM_M),
                centre_height_m=round(centre, 1),
                canvas_no=canvas[0],
                cloth_rating_kn=g.cloth(area, canvas[0]),
                note=(sail_words + g.canvas_note(canvas) if first else None),
            )
            b.line(f"{sid}.halyard", "halyard", sid, rating=g.rope_kn(size))
            b.line(f"{sid}.tack", "tack", sid, rating=g.rope_kn(size))
            b.line(f"{sid}.sheet", "sheet", sid, rating=g.rope_kn(g.quarter(size * 0.8)))
            b.line(f"{sid}.downhaul", "downhaul", sid, rating=g.rope_kn(g.quarter(size * 0.7)))
            stuns.append(sid)
    return stuns


def storm_canvas(b, p, ms_corners, heads, scale):
    """Her storm canvas in the sail room (Neuf-D §4.8): the brig's fore storm staysail on the
    fore stay, the schooner's storm trysail on the main gaff and boom in place of the mainsail,
    and the schooner's storm jib in place of the jib. Cobb (1841, read): in the gale 'the
    top-gallantmasts were housed and the yards on deck' (p. 78), she lay to under the fore gaff
    sail (p. 79), scudded under bare poles at about ten knots (p. 90), then lay to 'under her
    storm-staysail only', 'close reefed as it was' (p. 91)."""
    storm = g.BRIG_CANVAS["storm"]
    fore_yard = YARDS["fore.yard"][0]
    fss_foot = 0.9 * fore_yard / 2.0 + 4.0
    fss_leech = 0.42 * fore_yard
    fss_area = round(0.5 * fss_foot * fss_leech * FT * FT)
    f = scale["fore"]
    fss = b.sail(
        "fore.storm_staysail",
        "jibheaded",
        stay="fore.stay",
        area_m2=fss_area,
        x_m=round(p.mast_x["fore"] + 1.0 + fss_foot * FT / 3.0, 1),
        centre_height_m=round(DATUM_M + (1.5 + fss_leech * FT / 3.0), 1),
        canvas_no=storm[0],
        cloth_rating_kn=g.storm_cloth(fss_area),
        bent=False,
        note="the fore storm staysail on the fore stay, the brig-sloop's (Luce 1884 ch. X), cut as "
        "the frigate's on her fore yard: Kipping's fore staysail, its foot half the course's head "
        "and 4 ft, its leech the course's depth by the frigate's rule; in the sail room. Cobb's "
        "'storm-staysail' (1841 p. 91), under which she lay to." + g.canvas_note(storm, storm=True),
    )
    b.line("fore.storm_staysail.halyard", "halyard", fss, rating=g.rope_kn(g.quarter(3.0 * f), 2))
    b.sided("fore.storm_staysail.sheet", "sheet", fss, rating=g.rope_kn(g.quarter(3.0 * f), 3))
    b.line("fore.storm_staysail.downhaul", "downhaul", fss, rating=g.rope_kn(g.quarter(2.5 * f)))
    # the storm trysail: Steel's sloop's storm mainsail, as the schooner's, on her mainsail's
    tack, throat, _peak, _clew = ms_corners
    hoist_ft = math.hypot(throat[0] - tack[0], throat[1] - tack[1]) / FT
    st_head = 0.4 * MAINSAIL_FT["head"]
    st_foot = 3.0 * st_head
    st_luff = 0.85 * hoist_ft
    st_leech = st_luff * 9.0 / 8.0
    st_area = round((st_head + st_foot) / 2.0 * (st_luff + st_leech) / 2.0 * FT * FT)
    st_z = tack[1] + 0.45 * st_luff * FT
    canvas = g.SCHOONER_CANVAS["storm trysail"]
    m = scale["main"]
    st = b.sail(
        "storm_trysail",
        "gaff",
        mast="main.mast",
        gaff="main.gaff",
        boom="main.boom",
        area_m2=st_area,
        reef_bands=3,
        x_m=round(mast_at(p, "main", st_z) - 0.4 * st_foot * FT, 1),
        centre_height_m=round(st_z, 1),
        canvas_no=canvas[0],
        cloth_rating_kn=g.storm_cloth(st_area),
        bent=False,
        in_place_of="main.sail",
        note="the storm trysail, Steel 1794's sloop's storm mainsail as the topsail schooner's: "
        "the head two-fifths of the mainsail's, the foot three times the head, the luff 0.85 of "
        "the mainsail's (judgement within Steel's three-fourths to the whole), the after leech an "
        "eighth deeper; three reef bands; bent to the main gaff and boom in place of the mainsail; "
        "in the sail room." + g.canvas_note(canvas, storm=True),
    )
    b.line("storm_trysail.sheet", "sheet", st, rating=g.rope_kn(g.quarter(4.0 * m), 3), parts=3)
    b.line("storm_trysail.outhaul", "outhaul", st, rating=g.rope_kn(g.quarter(2.5 * m)))
    jib = heads["jib"]
    sj_area = round(2.0 / 3.0 * round(jib["area"]))
    canvas = g.SCHOONER_CANVAS["storm jib"]
    hd = scale["head"]
    sj = b.sail(
        "storm_jib",
        "jibheaded",
        stay="jib.stay",
        area_m2=sj_area,
        x_m=round(jib["x"], 1),
        centre_height_m=round(jib["z"] * math.sqrt(2.0 / 3.0), 1),
        canvas_no=canvas[0],
        cloth_rating_kn=g.storm_cloth(sj_area),
        bent=False,
        in_place_of="jib",
        note="the storm jib, two-thirds of the jib (Steel 1794, the sloop's jibs: 'used in stormy "
        "weather, in lieu of a larger one'), as the topsail schooner's; hanked to the jib stay in "
        "place of the jib, its centre as much lower as it is smaller (judgement); in the sail "
        "room. It stands in for Cobb's closely reefed jib (1841 p. 95), no evolution reefing a "
        "jib." + g.canvas_note(canvas, storm=True),
    )
    b.line("storm_jib.halyard", "halyard", sj, rating=g.rope_kn(g.quarter(3.0 * hd), 2))
    b.sided("storm_jib.sheet", "sheet", sj, rating=g.rope_kn(g.quarter(3.0 * hd)))
    b.line("storm_jib.downhaul", "downhaul", sj, rating=g.rope_kn(g.quarter(2.5 * hd)))
    return [fss, st, sj]


def groups_and_aliases(b, fore_yards, main_yards, sails):
    """Her groups with the names the engine reads (Neuf-D §4.8, on the brig's and the schooner's
    patterns; the engine reads 'plain sail', 'courses', 'topsails', 'headsails', 'jibs', 'gaff
    sails', 'staysails', 'storm canvas', 'storm staysails' and 'lying-to staysails' by name, the
    rest through the orders' nouns) and her aliases in her sources' words."""
    course, topsail, topgallant, royal = sails["fore"]
    fg, ms, gt = sails["gaff"]
    mtg = sails["main topgallant"]
    headsails = sails["head"]
    fss, jib, flying = headsails
    between = sails["between"]
    main_ss, main_tss = between
    stuns, storm = sails["stuns"], sails["storm"]
    # decision 14: the brig's and the schooner's plain sail together
    b.group("plain sail", [course, topsail, topgallant, fg, ms, fss, jib])
    b.group("courses", [course])
    b.group("topsails", [topsail])
    b.group("topgallants", [topgallant])
    # the main topgallant with the fore royal, so that "make all sail" sets it and "shorten sail"
    # takes it in by "the royals" (B3.4's finding); never by plain sail, the topgallants, the
    # topsails or the courses (Neuf-D §4.5)
    b.group("royals", [royal, mtg])
    b.group("square sails", [course, topsail, topgallant, royal, mtg])
    b.group("headsails", headsails)
    b.group("jibs", [jib, flying])
    b.group("gaff sails", [fg, ms])
    b.group("fore-and-aft sails", headsails + between + [fg, ms, gt])
    # the brig-sloop's "staysails", the fore staysail and those between the masts: the vocabulary's
    # "set the staysails" and the captains' head sails read it (world/captains.py)
    b.group("staysails", [fss, *between])
    b.group("staysails between the masts", between)
    b.group("studdingsails", stuns)
    b.group("light sails", [royal, mtg, gt, flying, main_tss, *stuns])
    b.group("lying-to staysails", [main_ss])
    b.group("storm canvas", storm)
    b.group("storm staysails", storm[:1])
    b.group(
        "all sail",
        [course, topsail, topgallant, royal, mtg, fg, ms, gt, *headsails, *between, *stuns],
    )
    b.group("yards", fore_yards + main_yards)
    b.group("fore yards", fore_yards)
    b.group("head yards", fore_yards)
    b.group("main yards", main_yards)
    b.group("after yards", main_yards)
    b.group("lower yards", fore_yards[:1])
    b.group("topsail yards", fore_yards[1:2])
    b.group("topgallant yards", fore_yards[2:3])
    b.group("royal yards", fore_yards[3:])
    b.group("lower masts", ["fore.mast", "main.mast"])
    b.group("topmasts", ["fore.topmast", "main.topmast"])
    b.group("topgallant masts", ["fore.topgallant_mast", "main.topgallant_mast"])
    b.group("royal masts", ["fore.royal_mast"])
    for level in ("lower", "topmast", "topgallant"):
        b.group(f"fore {level} studdingsails", [f"fore.{level}.studdingsail.{s}" for s in g.SIDES])
    for cls in ("sheet", "tack", "bowline"):
        b.group(f"fore {cls}s", [f"fore.course.{cls}.{s}" for s in g.SIDES])
        b.alias(f"fore {cls}", f"fore {cls}s")
    b.group("fore topsail bowlines", [f"fore.topsail.bowline.{s}" for s in g.SIDES])
    b.alias("fore top bowline", "fore topsail bowlines")
    # her sources' words (Neuf-D §4.8): "foresail" is the course (Cobb 1841 pp. 105-107), as the
    # brig's, not the topsail schooner's gaff foresail
    for alias, target in (
        ("foresail", course),
        ("fore course", course),
        ("fore-and-aft foresail", fg),
        ("fore gaff sail", fg),
        ("gaff foresail", fg),
        # its lines in the same words, so that the log never calls them the foresail's, her
        # course's (strain's names read a part's first plain alias; the reviews of 2026-11-07)
        ("starboard fore-and-aft foresail sheet", "fore.sail.sheet.starboard"),
        ("larboard fore-and-aft foresail sheet", "fore.sail.sheet.larboard"),
        ("fore-and-aft foresail tack", "fore.sail.tack"),
        ("mainsail", ms),
        ("fore-and-aft mainsail", ms),
        ("gaff topsail", gt),
        ("main gaff topsail", gt),
        ("main topgallant", mtg),
        ("main topgallant sail", mtg),
        ("fore staysail", fss),
        ("main staysail", main_ss),
        ("main topmast staysail", main_tss),
        ("fore yard", fore_yards[0]),
        ("stuns'ls", "studdingsails"),
        ("studding sails", "studdingsails"),
        ("kites", "studdingsails"),
        ("head sails", "headsails"),
        ("topgallant sails", "topgallants"),
    ):
        b.alias(alias, target)


# ---------------------------------------------------------------------------
# Her guns, her company and her stores (Neuf-D §5-§8; her road's step 4)
# ---------------------------------------------------------------------------

# Her one fit and its name (D22 (a); Neuf-D §5.1): the Admiralty's record of her, undated and
# most likely as taken, since she was never commissioned (judgement); the house names a fit by
# its year.
DEFAULT_FIT = "as taken 1814"
# Her pieces (Neuf-D §5.3): Adye 1804's long 6-pounder of 8 ft 0 in, the longer of his two, for
# the reach a chase gun is carried for (judgement); the 6 ft of 16 cwt 2 qr in the note.
LONG_6_PATTERN = (8, 0)
# Where they stand, from forward (Neuf-D §5.2; judgement by D22's leave): the long 6s in the
# foremost port a side as bow chasers, the carronades in the next eight, numbered 1 to 8 from
# forward, the two aftmost ports empty by the cabin trunk and the tiller under the main boom.
CHASE_PORT = 1
CARRONADE_PORTS = tuple(range(2, 10))
EMPTY_PORTS = (10, 11)

GUNS_NOTE = (
    "The armament (spec M7 7; package 70's shape; docs/design/Design-Ship-PrinceDeNeufchatel.md "
    "§5): her one fit, each gun on its port of the hull's profile to the centimetre with its deck "
    "named (Build-Ships.md §4.4, §6's checklist); the weights by Adye 1804 (pp. 72, 155) and the "
    "crews by Douglas 1829 and Falconer 1780 (D31 (c)); the magazine a private ship of war's. "
    "Every figure's source is in tools/ships/neufchatel.py."
)
FIT_SOURCE = (
    "Winfield, British Warships in the Age of Sail 1793-1817, pp. 335-336 (the Admiralty's record "
    "of her, undated); Niles' Weekly Register vol. VII p. 284; Cobb 1841 vol. I p. 39; Naval "
    "Chronicle vol. 33 p. 72; Adye 1804 pp. 72 and 155, the pieces; Douglas 1829 (art. 136) and "
    "Falconer 1780 (QUARTERS), the crews"
)
FIT_NOTE = (
    "Her one fit (D22 (a)): 16 x 12-pounder carronades and 2 long 6-pounders, 18 pieces, no pivot "
    "(Winfield pp. 335-336, the Admiralty's record, most likely as taken: judgement). Eighteen "
    "guns sailing from Boston on 21 December 1814 (Niles vol. VII p. 284), in Cobb (p. 39) and in "
    "the Naval Chronicle ('pierced for 22 guns, and mounting 18', vol. 33 p. 72); 18 in October "
    "(James vol. 6 p. 237). Cobb's 'nine and eighteen pounders' (p. 39) is one witness 26 years "
    "on, and no other source gives them; 17 guns in October (Niles vol. VII p. 120; Coggeshall "
    "1856 p. 241) and 14 by her log (Stevens 1915 p. 26); the 12-lb bags of musket balls of the "
    "boat action (Stevens p. 27) fit 12-pounder carronades (judgement). No pivot: no source "
    "names one and none is drawn, though none of her sheets is a deck plan (Neuf §2.7). Her small "
    "arms blunderbusses, muskets and boarding pikes (Coggeshall p. 241); her guns double shotted "
    "with canister and bags of musket balls (Coggeshall 1861 p. 468; Stevens p. 27), grape to the "
    "engine. The default."
)
CARRONADES_NOTE = (
    "Sixteen 12-pounder carronades, eight a side in the second to the ninth ports from forward "
    "(the places judgement: no source places her guns; Neuf-D §5.2), each on its port, its x and "
    "its sill to the centimetre: Adye 1804's 12-pounder of 2 ft 2 in, 5 cwt 3 qr 10 lb (p. 72, "
    "the page image read); four men to the pair, its captain, two privates and a provider "
    "(Douglas 1829 art. 136; D31 (c)). Numbered from forward, as the house numbers."
)
CHASERS_NOTE = (
    "Her two long 6-pounders as bow chasers in the foremost port a side, where her side is fine "
    "and a gun trains well forward (judgement, by D22's leave: the Admiralty's record of her reads "
    "as a brig-sloop's, whose 6-pounders stand at the bow as chase guns, and a privateer's long "
    "guns bring a prize to at long shot; no bow port is drawn on her): Adye 1804's 6-pounder of 8 "
    "ft 0 in, 22 cwt (p. 155, the page image read), the longer of his two for a chase gun's reach "
    "(judgement; the 6 ft 0 in of 16 cwt 2 qr the other); five men each (Falconer 1780, QUARTERS). "
    "Her two aftmost ports a side stand empty, by the cabin trunk and the tiller under the main "
    "boom (judgement): 'mounting 18' in 22 ports leaves four empty."
)
# Her cartridges' powder (Neuf-D §5.4): the Regulations' Table No. 29 through `charge_lb` since
# the shared work SW-1 filled the table (Build-Ships.md §10), the same to the ounce as the
# engine's shares gave her two calibres before it; the figures not overridden. Her own note,
# which cites the table as read, is kept over the shared one for Adye's page beside it, the
# shares cited at `CHARGE_SHARE`, since `charge_lb` now gives the table first.
CHARGES_NOTE = (
    "A cartridge's powder in pounds, to the ounce: the service charges of cylinder powder for one "
    "shot, the Regulations 1806 (1808 printing), Table No. 29, read on the page image "
    "(Build-Ships.md §10): the long 6-pounder 2 lb, the 12-pounder carronade 1 lb, which Adye 1804 "
    "p. 72 gives too. The engine's shares of the shot, a third for a long gun and a twelfth for a "
    "carronade (freesail/ship/parts.py, CHARGE_SHARE), give each of them to the ounce."
)


def her_guns(profile):
    """Her fit's guns (Neuf-D §5.2-§5.3), each on its port's triple of the upper deck as the
    profile has it, to the centimetre: the carronades by `g.broadside_pair`, numbered from
    forward, then the bow chasers by `g.chasers`, each crew reassigned to the period's (assigning
    an existing key keeps the key order, Indf §5.2)."""
    ports = [(x, sill) for x, sill, _hb in reversed(profile["ports_m"]["upper"])]
    carronade_cwt = period.ADYE_CARRONADE_CWT[12]
    long_cwt = period.ADYE_LONG_GUN_CWT[6][LONG_6_PATTERN]
    guns = []
    for number, port in enumerate(CARRONADE_PORTS, start=1):
        x, sill = ports[port - 1]
        made = g.broadside_pair(
            number,
            "carronade",
            12,
            carronade_cwt,
            x,
            sill,
            CARRONADES_NOTE if number == 1 else None,
            deck="upper",
            round_to=0.01,
        )
        for gun, _ in made:
            gun["crew"] = period.DOUGLAS_CARRONADE_CREW
        guns += made
    x, sill = ports[CHASE_PORT - 1]
    made = g.chasers("bow", "long", 6, long_cwt, x, sill, CHASERS_NOTE, deck="upper", round_to=0.01)
    for gun, _ in made:
        gun["crew"] = period.FALCONER_CREW[6]
    guns += made
    check_guns_on_triples(guns, profile)
    return guns


def check_guns_on_triples(guns, profile):
    """Every gun of the fit on a port triple of its deck within 0.01 m, by its x and its height
    (Neuf-D §1.5; Build-Ships.md §6's checklist, item 2), and no two guns of a side on one."""
    triples = profile["ports_m"]
    taken = set()
    for gun, _ in guns:
        on = [
            i
            for i, (x, sill, _hb) in enumerate(triples[gun["deck"]])
            if abs(gun["x_m"] - x) <= 0.01 and abs(gun["height_m"] - sill) <= 0.01
        ]
        if not on:
            raise ValueError(
                f"neufchatel: {gun['id']} stands at x {gun['x_m']:g} m, {gun['height_m']:g} m "
                f"above her water, on no port triple of her {gun['deck']} deck within 0.01 m."
            )
        if (gun["side"], on[0]) in taken:
            raise ValueError(f"neufchatel: {gun['id']} stands in a port another gun has.")
        taken.add((gun["side"], on[0]))


def armament(b, guns):
    """Her fit and its magazine (Neuf-D §5.4): the privateer schooner's allowance, 40 round, 6
    grape and 4 chain a gun (`g.HIRED_ROUNDS`; judgement: a private ship of war's magazine
    smaller than a King's), no charges for exercise (the Regulations bind King's ships), the
    charges' note her own."""
    magazine = g.fit_magazine(guns, {"long": g.HIRED_ROUNDS, "carronade": g.HIRED_ROUNDS})
    b.armament(GUNS_NOTE, DEFAULT_FIT, [(DEFAULT_FIT, FIT_SOURCE, guns, magazine, FIT_NOTE)])
    b.armament_notes[("magazine", DEFAULT_FIT, "charges")] = CHARGES_NOTE


# Her company, 130 (D36 (a); Neuf-D §6.1): "From Boston, 18 guns, 130 men" (Niles' Weekly
# Register vol. VII p. 284, read). The posts her wardroom file's (data/people/); the marines,
# the idlers and the seamen's stations judgement as below.
COMPLEMENT = 130
MARINES = 16
SEAMEN = {"forecastle": 20, "fore_top": 24, "afterguard": 30, "waisters": 20}
IDLERS = {
    "carpenter's crew": (2, "two of the carpenter's crew"),
    "sailmaker's crew": (1, "one of the sailmaker's"),
    "cooper": (1, "a cooper, for her water and provision casks"),
    "armourer": (1, "an armourer, for her blunderbusses, muskets and pikes"),
    "cook": (1, "a cook"),
    "steward": (1, "a steward, Cobb's 'purser's steward' (p. 75)"),
    "servant": (1, "a servant"),
}
# Her seamen by rating (Neuf-D §6.1; judgement): more landsmen than the privateer schooner's
# prime seamen, her December crew drawn to sea by the prize money of her last cruise (Cobb p. 39).
RATINGS = {"able": 0.35, "ordinary": 0.35, "landsman": 0.30}
# The quarter bill beyond the gun crews (Neuf-D §6.4; judgement): the trimmers the brig-sloop's
# twenty-seven carried by her plain sail against the brig's (the generator's report gives the
# arithmetic), split by each mast's work; one at the tiller and two waisters at the powder, the
# privateer schooner's; the small-arms men her sixteen marines and ten seamen, a fifth of her
# company, and the boarders two thirds of it, each the privateer schooner's share.
BRIG_TRIMMERS = 27
# The brig-sloop's plain sail, m2, from brig.yaml: her courses 94 and 94, topsails 114 and 121,
# topgallants 46 and 45, fore topmast staysail 33, jib 57 and spanker 162.
BRIG_PLAIN_M2 = 94 + 94 + 114 + 121 + 46 + 45 + 33 + 57 + 162
TRIMMERS = {"forecastle": 9, "fore_top": 11, "afterguard": 15}
HELM = 1
POWDER = 2
SMALL_ARMS = 26
BOARDERS = 85
# Her stores (Neuf-D §7; judgement): water a gallon a man a day for two months, about 35 tons;
# provisions for three months, her 1814 cruise from Cherbourg on 4 July to Boston on 15 October
# (Stevens 1915 p. 26; Niles vol. VII p. 120); the brig-sloop's spare rope; a shot plug a gun.
WATER_TONS = 35
PROVISIONS_DAYS = 90
CORDAGE_FATHOMS = 300


def company(b, guns):
    """Her crew section (Neuf-D §6.1-§6.2, §6.5), the people drawn at muster from her wardroom
    file (§6.3), and her stores beside them (§7): water, provisions, cordage, a shot plug a gun of
    `guns`, the spare spars by the brig-sloop's list on her own spars, and her sail room by the
    topsail schooner's method."""
    posts, drawn = g.wardroom("hermaphrodite-brig")
    seamen = sum(SEAMEN.values())
    idlers = sum(n for n, _ in IDLERS.values())
    if len(posts) + seamen + MARINES + idlers != COMPLEMENT:
        raise ValueError(
            f"neufchatel: her {len(posts)} posts, {seamen} seamen, {MARINES} marines and {idlers} "
            f"idlers make {len(posts) + seamen + MARINES + idlers}, not her {COMPLEMENT}."
        )
    stations_note = (
        "Hands per station, both watches together: her seamen, the complement less the posts, "
        "the marines and the idlers (Neuf-D §6.1; the shares judgement): the fore top the "
        "larger for her four fore yards and the studding sails, the afterguard for the great "
        "mainsail and the gaffs; no main top, her main a schooner's with crosstrees and no top "
        "(Cobb 1841 p. 91), as the topsail schooner's. Nine prize-masters among the afterguard's "
        "able seamen (Cobb p. 40), one of them drawn by name below: a post stands on the "
        "quarterdeck and never hauls (crew/muster.py), and prizes are package 74's, which takes "
        "its prize crews from her company. Her people's nations were mixed (Cobb p. 42; Stevens "
        "1915 p. 27). Forecastlemen: the head, the anchors and the headsails."
    )
    entries = [
        (
            ("complement",),
            COMPLEMENT,
            "'From Boston, 18 guns, 130 men' (Niles' Weekly Register vol. VII p. 284, 31 December "
            "1814, read); 130 in Collier's report as reprinted (D36 (a)). Emmons 1853's 127 (p. "
            "190), James's '120 or 130 men' in October (vol. 6 p. 237) and Cobb's 163 'all told' "
            "(1841 p. 39) beside it. Her large crew for prizes (the brief) is this company: about "
            "seven men a gun, with nine prize-masters to take her prizes in.",
        ),
        (
            ("names",),
            "american",
            "An American privateer's crew: the american list in data/crew/names.yaml (D39 with the "
            "brief); her file names no nation, the list's being the United States' where a "
            "scenario names none (world/nations.py), and a scenario's `nation:` wins.",
        ),
        (("stations", "forecastle"), SEAMEN["forecastle"], stations_note),
        (
            ("stations", "fore_top"),
            SEAMEN["fore_top"],
            "Fore topmen, for her four fore yards and the studding sails.",
        ),
        (
            ("stations", "afterguard"),
            SEAMEN["afterguard"],
            "Afterguard, at the main sheet and the gaffs, the boys among them as landsmen (spec "
            "M3 9 item 6).",
        ),
        (("stations", "waisters"), SEAMEN["waisters"], "Waisters."),
        (
            ("stations", "marines"),
            MARINES,
            "Marines: Cobb was put 'with seven others' in the long boat at quarters with muskets, "
            "'the first intimation I had of being drafted into the marine corps' (1841 p. 73, "
            "read); Coggeshall counts 'officers and marines' (1856 p. 241). At least eight; "
            "sixteen is judgement, the long boat's eight and as many forward (Neuf-D §6.2). "
            "Landsmen with muskets, not a detachment as a King's ship's; no marine officer, none "
            "being named. Their kit the scenario's nation's (data/nations.yaml: the United "
            "States' basic).",
        ),
        (
            ("stations", "idlers"),
            idlers,
            "Idlers: the trades below (Luce 1884 ch. XX: they stand no night watches).",
        ),
        (
            ("ratings", "able"),
            RATINGS["able"],
            "Share of the seamen (not marines, idlers or officers) by rating: judgement (Neuf-D "
            "§6.1). The privateer schooner ships prime seamen; her December crew did not: the "
            "prize money of her last cruise drew 'many, who otherwise never would have gone to "
            "sea' (Cobb 1841 p. 39), and Cobb was a green hand. Able: 0.35.",
        ),
        (("ratings", "ordinary"), RATINGS["ordinary"], "Ordinary: 0.35, judgement."),
        (("ratings", "landsman"), RATINGS["landsman"], "Landsmen: 0.30, judgement."),
    ]
    entries += [
        (
            ("posts", post),
            None,
            (
                "Station holders by post (spec M3 2.3): her December crew's, 'besides the "
                "captain, we had five lieutenants, nine prize-masters, quarter-masters, "
                "sailing-masters, boatswains, gunners, carpenters, and sail-makers in profusion' "
                "(Cobb 1841 p. 40, read), one of each warrant (judgement), and the surgeon (pp. "
                "75-76); their mates petty officers in the stations (judgement). Her wardroom "
                "file (data/people/hermaphrodite-brig.yaml) gives them; names are drawn at "
                "muster unless a post gives one."
            )
            if i == 0
            else None,
        )
        for i, post in enumerate(posts)
    ]
    entries += [
        (
            ("idlers_by_trade", trade),
            n,
            (
                "How the idlers are made up (Neuf-D §6.1; judgement); they must sum to the idlers. "
                if i == 0
                else ""
            )
            + f"{text[0].upper() + text[1:]}: {n}.",
        )
        for i, (trade, (n, text)) in enumerate(IDLERS.items())
    ]
    entries += [
        (
            ("stores", "water_tons"),
            WATER_TONS,
            "Water for two months at a gallon a man a day (judgement, Neuf-D §7); her hold was "
            "'cleared away underneath the deck, except the water and provision casks' for prize "
            "goods (Cobb 1841 p. 40).",
        ),
        (
            ("stores", "provisions_days"),
            PROVISIONS_DAYS,
            "Provisions for three months (judgement): her cruise of 1814 ran from Cherbourg on 4 "
            "July to Boston on 15 October (Stevens 1915 p. 26; Niles vol. VII p. 120).",
        ),
        (("stores", "spare_spars"), {}, None),  # the booms, by class: below
        (
            ("stores", "cordage_fathoms"),
            CORDAGE_FATHOMS,
            "Spare rope in the boatswain's store: the brig-sloop's (judgement).",
        ),
        (
            ("stores", "shot_plugs"),
            len(guns),
            g.SHOT_PLUGS_NOTE + " One a gun of her fit.",
        ),
        *g.ration_entries("a private ship of war's articles promised the like (judgement)"),
    ]
    b.crew(entries)
    b.people(
        "The named people beyond the posts (package 35, spec M5 §22): each drawn from a station "
        "at muster, the counts above unchanged; see data/people/hermaphrodite-brig.yaml.",
        drawn,
    )
    b.spare_spars(
        "The booms: the spare spars by class, the brig-sloop's list (Luce 1866 ch. XVII, 'Stowing "
        "Booms', scaled to a brig-sloop) on her own spars (Neuf-D §7; judgement); see "
        "tools/ships/neufchatel.py.",
        [
            (
                "topmast",
                1,
                "A spare topmast (judgement, after Luce 1866 and the brig-sloop's).",
            ),
            ("topgallant_mast", 1, "A stump topgallant mast (judgement, after Luce 1866)."),
            ("yard", 1, "A spare topsail yard (judgement, after Luce 1866)."),
            (
                "studdingsail_boom",
                2,
                "A pair of topmast studding-sail booms for her fore (judgement, after Luce).",
            ),
            ("jib_boom", 1, "The spare jib-boom (Luce 1866)."),
        ],
    )
    canvas = {s["id"]: s["canvas_no"] for s in b.doc["sails"]}
    b.sail_room(
        "The sail room (spec 3b §6.3) by the topsail schooner's method (Neuf-D §7), every sail "
        "new; see tools/ships/neufchatel.py.",
        [
            (
                "fore.sail",
                canvas["fore.sail"],
                "A second fore gaff sail, fore topsail and jib, the sails a privateer on a cruise "
                "could least do without, as the topsail schooner's (spec 3b §6.3, judgement).",
            ),
            ("fore.topsail", canvas["fore.topsail"], None),
            ("jib", canvas["jib"], None),
            (
                "fore.storm_staysail",
                canvas["fore.storm_staysail"],
                "Storm canvas, one of each (spec 3b §6.4).",
            ),
            ("storm_trysail", canvas["storm_trysail"], None),
            ("storm_jib", canvas["storm_jib"], None),
        ],
    )


def at_the_guns(guns):
    """The men her fit takes at the beat: one crew to a broadside pair, and one to each chaser,
    which is its own crew (`parts.Gun.pair_key`)."""
    one_side = [gun for gun, _ in guns if gun["place"] != "broadside" or gun["side"] == g.SIDES[0]]
    return sum(gun["crew"] for gun in one_side)


def quarter_bill(b, guns):
    """Her quarter bill set against her fit (Neuf-D §6.4): the trimmers, the tiller, the powder,
    the filling party, the priority, the small-arms men and the boarders; the arithmetic in the
    generator's report."""
    seamen = sum(SEAMEN.values())
    plain = sum(s["area_m2"] for s in b.doc["sails"] if s["id"] in b.doc["groups"]["plain sail"])
    REPORT["bill"] = (seamen, at_the_guns(guns), plain)
    b.quarter_bill(
        g.QUARTER_BILL_NOTE,
        [
            (
                "forecastle",
                TRIMMERS["forecastle"],
                "The trimmers: the brig-sloop's twenty-seven (brig.yaml's bill) carried by her "
                "plain sail against the brig's, a quarter more (Neuf-D §6.4; the arithmetic in "
                "the generator's report), split by each mast's work (judgement). Of the "
                "forecastlemen, for the headsails and the fore tacks and sheets.",
            ),
            ("fore_top", TRIMMERS["fore_top"], "Of the fore topmen, for her four fore yards."),
            (
                "afterguard",
                TRIMMERS["afterguard"],
                "Of the afterguard, at the main sheet, the gaffs and the fore gaff sail's sheet.",
            ),
        ],
        HELM,
        POWDER,
        "sail before guns",
        {
            "helm": "One man at the tiller, as the privateer schooner's (judgement).",
            "powder": "Two of the waisters to pass the cartridges, as the privateer schooner's "
            "(judgement).",
            "priority": g.PRIORITY_NOTE + " Hers the privateer schooner's: her trade was running "
            "and chasing (Neuf-D §6.4).",
        },
        small_arms=SMALL_ARMS,
        boarders=BOARDERS,
        small_arms_note="Her sixteen marines and ten seamen with the muskets and blunderbusses "
        "(Coggeshall 1856 p. 241): a fifth of her company, the privateer schooner's share of "
        "hers (judgement, Neuf-D §6.4).",
        boarders_note="Boarders with cutlass, pistol and pike, two thirds of her company: the "
        "privateer schooner's share, 'a privateer's company boards almost whole' (judgement, "
        "Neuf-D §6.4).",
        filling=g.filling_party(guns),
    )
    b.crew_notes[("quarter_bill", "filling")] = (
        g.FILLING_NOTE + " Her eighteen pieces give four (Neuf-D §5.4)."
    )


# Her ground tackle (Neuf-D §7): Steel 1794's row for "14 Guns, 300 Tons", the nearest to her
# 328 tons, and the cordage table's "Sloops" column (`period.STEEL_ANCHORS[14]`); her five bower
# cables laid two on the best bower, two on the small and one on the sheet (judgement: Lever's
# "three Cables on the best Bower, two on the small" is a ship of the line's, Indf §7).
BOWER_CABLES = {"best_bower": 2, "small_bower": 2, "sheet": 1}
# Her burthen and her length on deck (Winfield 1793-1817 pp. 335-336: 328 22/94 tons; 110 ft 8
# in), which the hold's and the boats' rules read.
BURTHEN_TONS = 328.0
DECK_LENGTH_FT = 110.0 + 8.0 / 12.0


def ground_tackle(b):
    """Steel's anchors and cables for a vessel of 14 guns and 300 tons (Neuf-D §7), through
    `Builder.ground_tackle`; the house's rule (Luce 1866) set aside, its figures for her in the
    generator's report."""
    steel = period.STEEL_ANCHORS[14]
    if len(BOWER_CABLES) != steel["bowers"] or sum(BOWER_CABLES.values()) != steel["bower_cables"]:
        raise ValueError(
            f"neufchatel: Steel's row has {steel['bowers']} bowers and {steel['bower_cables']} "
            f"bower cables; BOWER_CABLES lays {sum(BOWER_CABLES.values())} on {len(BOWER_CABLES)}."
        )
    bower = float(round(steel["bower_cwt"] * g.CWT_KG))
    cable, stream = steel["bower_cable_in"], steel["stream_cable_in"]
    hawser = g.KEDGE_HAWSER_OF_BOWER * cable
    fathoms = g.CABLE_FATHOMS
    bowers = {
        "best_bower": (
            "bower",
            "the best bower",
            f"The bowers: Steel's three of {steel['bower_cwt']:g} cwt for '14 Guns, 300 Tons', the "
            "row nearest her 328 tons (Steel 1794 vol. I, the anchor table, the page image read: "
            "Neuf-D §7; the house prefers Steel, D33); the cables the cordage table's 'Sloops' "
            f"column, five of {cable:g} in (read; the column judgement, the table having none for "
            "14 guns, its '20 guns' column six of 14 1/2 in), rated as every rope by Luce 1866 ch. "
            "IV, laid two on the best bower, two on the small and one on the sheet (judgement), "
            "120 fathoms a cable (Falconer 1780, CABLE). Steel's table is the Navy's; no source "
            "gives a privateer's. The house's rule (Luce 1866 ch. XIV, the generator's "
            "ground_tackle_for) is set aside for the period's own table on her tonnage.",
        ),
        "small_bower": ("bower", "the small bower", None),
        "sheet": (
            "sheet",
            "the sheet anchor",
            "The sheet anchor, Steel's third bower, on one cable.",
        ),
    }
    anchors = [
        (aid, kind, name, bower, fathoms * BOWER_CABLES[aid], cable, g.rope_kn(cable), text)
        for aid, (kind, name, text) in bowers.items()
    ]
    anchors += [
        (
            "stream",
            "stream",
            "the stream anchor",
            float(round(steel["stream_cwt"] * g.CWT_KG)),
            fathoms,
            stream,
            g.rope_kn(stream),
            f"The stream anchor, Steel's {steel['stream_cwt']:g} cwt for the row, on the 'Sloops' "
            f"stream cable of {stream:g} in (Steel 1794 vol. I, the anchor and cordage tables, "
            "read).",
        ),
        (
            "kedge",
            "kedge",
            "the kedge",
            float(round(steel["kedge_cwt"] * g.CWT_KG)),
            fathoms,
            hawser,
            g.rope_kn(hawser),
            "The kedge, Steel's 3 cwt 2 qr for the row, on a hawser of half the bower cable's "
            "size, the house rule (gen_ships.KEDGE_HAWSER_OF_BOWER; judgement).",
        ),
    ]
    b.ground_tackle(
        "The ground tackle (package 34, spec M5 §18): Steel's anchors and cables for a vessel of "
        "14 guns and 300 tons (Steel 1794 vol. I; Neuf-D §7), every figure's source in "
        "tools/ships/neufchatel.py; chain cable is later than her years.",
        anchors,
        chain=False,
    )
    # the house's rule on her burthen, beam and draught, for the report (Neuf-D §7)
    hull = b.doc["hull"]
    REPORT["luce"] = (
        round(g.BOWER_CWT_PER_100_TONS * BURTHEN_TONS / 100.0, 1),
        round(2.0 / 3.0 * hull["draught_m"] / FT + hull["beam_m"] / FT, 1),
        round(g.CABLE_IN_PER_FOOT_OF_BEAM * hull["beam_m"] / FT * 2.0) / 2.0,
    )


def boats_pumps_hold(b):
    """Her hold at a trader's share of her burthen, her two hand pumps, and her long boat and
    yawl by Luce's rule on her length as the privateer schooner's (Neuf-D §7)."""
    g.hold_for(
        b,
        BURTHEN_TONS,
        False,
        "328 tons, Winfield 1793-1817 pp. 335-336; a trader's share, her hold 'cleared away "
        "underneath the deck, except the water and provision casks' for prize goods (Cobb 1841 p. "
        "40): a privateer built to fill, where a ship of war's share would leave a fifth of it "
        "(judgement)",
    )
    b.pumps(
        g.PUMPS_NOTE + " Hers 'the pumps' (Cobb 1841 p. 55): two hand pumps, the privateer "
        "schooner's (judgement for the kind and the count).",
        g.pump_entries(0, 2, ["the starboard pump", "the larboard pump"]),
    )
    b.boats(
        g.BOATS_NOTE,
        g.boat_entries(
            DECK_LENGTH_FT,
            False,
            [
                (
                    "long_boat",
                    "long-boat",
                    "the long-boat",
                    1.0,
                    "The long-boat, 'which stood amidships of the deck' (Cobb 1841 p. 73, read), "
                    "a fifth under Luce's rule for a ship of war on her 110 ft 8 in on deck "
                    "(Winfield pp. 335-336), as the privateer schooner's (judgement for a "
                    "privateer).",
                ),
                (
                    "yawl",
                    "yawl",
                    "the yawl",
                    0.8,
                    "The yawl at the stern (judgement: Reed's modern model shows a boat there, "
                    "Winfield pp. 335-336's photograph, for the eye only; Falconer, YAWL), as the "
                    "privateer schooner's.",
                ),
            ],
        ),
    )


# Her description at far detail (D15 (a); Neuf-D §8), in her own file by SW-4's form
# (Build-Ships.md §8.1, §8.2): the tops make out a brig, the glass her two masts' rigs and her
# ports; her fit her one fit, her file's default, so that a far ship of hers carries nothing new;
# a privateer's role (`captains.ROLES`, its book data/captains/privateer.yaml).
DESCRIPTION = (
    "hermaphrodite brig",
    "a brig",
    "a hermaphrodite brig, a brig's foremast and a schooner's main, long and low, pierced for "
    "eleven guns a side",
    "'Hermaphrodite rigged' (Niles vol. VII p. 120; Cobb 1841 p. 38; Coggeshall 1856 p. 241), "
    "Rankine's word for the rig (via Chapelle 1930 p. 164); 'lying low in the water' (Cobb p. 38); "
    "'pierced for 22 guns' (Naval Chronicle vol. 33 p. 72). The Admiralty's 'American Schooner' "
    "(RMG ZAZ6177, ZAZ6179) and Winfield's schooner (pp. 335-336); her log's 'privateer brig' "
    "(Stevens 1915 p. 26). At four miles the tops make out a brig, her square fore the brig's "
    "(D15 (a); judgement on the words). Her one fit, her file's default; a privateer's role "
    "(Build-Ships.md §8.2).",
    DEFAULT_FIT,
    ["privateer"],
)


def brace_check(p):
    """The fore yard against the lee shrouds (Neuf-D §4.2, as Indf §4.2 does): the plan bearing,
    degrees abaft the beam, of the aftmost fore shroud from the yard's truss at the fore yard's
    height, the shrouds led from the hounds to the fore channel's after end at the rail. Reported,
    not ruled: no source gives her brace limit."""
    aft_ft = (FORE_CHANNEL_AFT_PX - ZAZ6177_RABBET_PX) / ZAZ6177_PX_PER_FT
    x_aft = x_m(aft_ft)
    z_rail = interp([(x_m(x), z_m(z)) for x, z in RAIL], x_aft)
    hb = (top_breadth(aft_ft) + PLANK_FT) * FT
    zh = p.hounds["fore.mast"]
    zy = z_m(YARDS["fore.yard"][1])
    f = (zh - zy) / (zh - z_rail)
    shroud_x = mast_at(p, "fore", zh) + (x_aft - mast_at(p, "fore", zh)) * f
    dx = mast_at(p, "fore", zy) - shroud_x
    return math.degrees(math.atan2(dx, hb * f))


def her_report() -> str:
    """The generator's report: what her rules compute from her file's own keys, printed as her
    file is written and held by her tests (the lead's notes of 2026-10-29, item 2)."""
    out = [f"hermaphrodite-brig: {line}" for line in REPORT.get("checks", [])]
    out += [f"hermaphrodite-brig: {line}" for line in REPORT.get("hull", [])]
    if "rope" in REPORT:
        scales = ", ".join(f"{k} {v:.3f}" for k, v in REPORT["rope"].items())
        out.append(f"hermaphrodite-brig: her rope's scales, {scales}.")
    if "plain" in REPORT:
        out.append(f"hermaphrodite-brig: plain sail {REPORT['plain']} m2.")
    if "brace" in REPORT:
        out.append(
            "hermaphrodite-brig: the aftmost lee fore shroud at the fore yard's height bears "
            f"{REPORT['brace']:.0f} deg abaft the beam from the yard's truss (her fore yard braced "
            f"to {BRACE_LIMITS['fore.yard']})."
        )
    if "bill" in REPORT:
        seamen, men, plain = REPORT["bill"]
        out.append(
            f"hermaphrodite-brig: the quarter bill on '{DEFAULT_FIT}': her plain sail {plain:.0f} "
            f"m2 against the brig-sloop's {BRIG_PLAIN_M2:.0f} carries the brig's {BRIG_TRIMMERS} "
            f"trimmers to {BRIG_TRIMMERS * plain / BRIG_PLAIN_M2:.1f} ({sum(TRIMMERS.values())} "
            f"written); of her {seamen} seamen, the beat takes {men} to her guns (a crew to each "
            f"carronade pair and to each chaser) and {HELM} to the tiller."
        )
    if "luce" in REPORT:
        bower, beam_rule, cable = REPORT["luce"]
        out.append(
            "hermaphrodite-brig: the house's rule set aside for Steel's row (Luce 1866 ch. XIV, "
            f"gen_ships.ground_tackle_for): bowers of {bower:g} cwt by five to the hundred tons "
            f"({beam_rule:g} by the beam rule) and a cable of {cable:g} in, against Steel's "
            f"{period.STEEL_ANCHORS[14]['bower_cwt']:g} cwt and "
            f"{period.STEEL_ANCHORS[14]['bower_cable_in']:g} in."
        )
    return "\n".join(out)


def build(out_dir: str) -> None:
    """Write her file to `out_dir`, `hermaphrodite-brig.yaml`, through `write()`; the checks of
    Neuf-D §1.5 raised before it is written."""
    REPORT.clear()
    write(out_dir, particulars())
    print(her_report(), file=sys.stderr)
