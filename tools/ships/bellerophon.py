"""HMS *Bellerophon*, the Arrogant-class 74 of 1786 on the Bellona-class draughts (package 75, the
fourth ship; her builder B7).

Her design is docs/design/Design-Ship-Bellerophon.md (cited here as Bel-D), from her research note
docs/design/Research-74-2026-10.md (Bel), the engine's design for her mizen course and driver and
her yards under the bowsprit (docs/design/Design-ShipsEngineExtensions.md, Ext, §3, §4 and §17)
and the owner's answers (Bel §13.1; Bel-D §17.0). One module writes one file,
`data/ships/seventy-four.yaml` (Bel-D decision 1): `write(out_dir)` builds and dumps her file and
`build(out_dir)` is the generator's hook (`tools/gen_ships.py`, `SHIP_MODULES`). Her mizen course
and her driver are cut by `tools/ships/mizen_yard.py` and her yards under the bowsprit by
`tools/ships/spritsail_yards.py`, each pure; nothing is imported from another ship's module
(Bel-D decision 3), so B1's patterns are copied here, the duplication reported (Bel-D §18 item 11).

**Built so far (Bel-D §13, steps 1 to 4).** Her hull block and profile with its shape keys (§2,
§3); the masts with Steel's long pole-heads (§4.1, §4.2); the yards, studding-sail booms, braces
and rope (§4.3); the square sails (§4.4); the mizen course on its lateen yard (§4.5); the driver
and its boom (§4.6); the head with the spritsail and sprit-topsail yards (§4.7); the staysails,
the studding sails, the storm and occasional canvas, the groups and the aliases (§4.8); her
three fits with their magazines (§5); her company of 590, her marines, her quarter bill with the
marines it keeps, her flag party, her people file's posts and drawn roles (§6); her stores, sail
room, ground tackle, boats, pumps and hold (§7); her description (§8). Her bill by deck (B7.b,
§6.4) is her step 6's and reads the bill's `marines`, which nothing reads before it. At her step 7
(B7.d, §5.2, on the lead's word) her guns are numbered by deck, each deck from No. 1, their ids
re-keyed by deck and her armament's `numbering` set, the 64's with hers.

**The frame (Bel-D §1.4).** The figures at the top are in the drawings' own frame, as the sources
give them: feet forward of AP (ZAZ1357's red dashed after perpendicular) and feet above WL1 (its
top green waterline), or above the keel's top or K where a measure was taken from them. They are
converted once: x in metres forward of the mid-perpendicular, 84 ft before AP; z in metres above
the Channel line, her water, parallel to WL1 and `CHANNEL_FT` above it, where her drawn lowest
lower-deck sill stands the Bellona's reported 5 ft 2 in clear (Bel-D §2.2; the owner's "Agreed",
§17.0). The engine has no trim, so a height above the water at its own station is what it
believes. A spar's `height_m` and a sail's `corners_m` are written above her datum, her upper deck
at the middle, 3.16 m (D18 (a), the deck being continuous: Bel-D §2.3); a sail's centre above the
water.

**Her measuring (Bel-D §3.7, step 1).** Taken on the held images (owner-notes/seventyfour/rmg/:
ZAZ1357 at full resolution, 26397 x 8557 px; ZAZ1359, 19752 x 5770; ZAZ1361 and ZAZ1363) with the
research's registration (the checker's: ZAZ1357 at 99.82 px to the foot, AP at 7445.75 px, WL1
fitted; ZAZ1359 at 100.015 px to the foot by its strip, AP at its strong line at 1800.1 px, its
stations 30 to 8 within 0.25 ft of ZAZ1357's) and on the owner's photographs of Lavery's drawings,
by scratch scripts outside the repository; the images are not in the repository. Each figure
below names its sheet and its check. The tasks not taken are said so where they bear.

**Her notes (the lead's notes of 2026-10-29, item 2).** The file's notes carry sources,
departures and judgements. A figure a rule computes from the file's own keys (an area from a cut,
a rating, a rope's size, a drawn displacement, a port's gap) is printed by `her_report()`, the
generator's report, and held by her tests, where it cannot go stale. `HerBuilder` keeps the shared
helpers' such figures out of her notes.

The module is imported only by the generator's entry block, after `gen_ships` is made the running
script, and takes every helper as `g.<name>`. No function or table of the generator is changed;
every other file stays byte for byte as it is.

Marks: measured (off a held image, with its check), read (the page or its image), read (OCR),
read (owner's book), judgement.
"""

from __future__ import annotations

import math
import os
import re
import sys

import gen_ships as g

from ships import mizen_yard, period, spritsail_yards

FT = g.FT

# Her flips (Bel-D §0; Ext §17.8), each the fallback a late piece would cost one constant: the
# mizen course cut at the mast on her lateen yard (B3.1), the yards under the bowsprit (B3.2) and
# Steel's driver boomsail (B3.5), each built and merged before her window.
MIZEN_COURSE = "gated"
BOWSPRIT_YARDS = True
DRIVER = True

# ---------------------------------------------------------------------------
# The drawings' frame: her water and the keel (Bel-D §1.4, §2.2)
# ---------------------------------------------------------------------------

# Her water, the Channel line: WL1 + 5.44 ft - 5 ft 2 in, where the drawn lowest lower-deck sill
# (L7, 5.44 ft above WL1: measured, two readers, Bel §3.1) stands the 5 ft 2 in the Bellona
# reported at her best Channel draught in 1763 (Lavery 1985 p. 9, Table 2, read (owner's book)).
CHANNEL_FT = 5.44 - 62.0 / 12.0
# The mid-perpendicular, the file's x = 0: half the 168 ft between the perpendiculars.
MIDSHIPS_FT = 84.0
# WL1 above K (the strip's top border) at AP, at the middle and at FP (measured, the checker: Bel
# §3.2.2).
WL1_ABOVE_K_FT = [(0.0, 21.84), (84.0, 20.93), (168.0, 20.10)]
# WL1 above the keel's top at the middle and its drag over the 168 ft (Bel §3.2.2): the base of
# the body plan, from which its heights are measured.
WL1_ABOVE_KEEL_TOP_MID_FT = 18.89
DRAG_FT = 1.72


def interp(points, x):
    """The value at `x` of a line of (x, value) points, straight between them and held at the
    first and the last beyond them."""
    if x <= points[0][0]:
        return points[0][1]
    for (x0, v0), (x1, v1) in zip(points, points[1:], strict=False):
        if x <= x1:
            return v0 + (v1 - v0) * (x - x0) / (x1 - x0)
    return points[-1][1]


def x_m(x_ft):
    """Feet forward of AP as the file's x, metres forward of the mid-perpendicular."""
    return (x_ft - MIDSHIPS_FT) * FT


def z_m(z_ft):
    """Feet above WL1 as the file's z, metres above her water, the Channel line."""
    return (z_ft - CHANNEL_FT) * FT


def k_ft(x_ft):
    """K at `x_ft`, feet above WL1 (below it)."""
    return -interp(WL1_ABOVE_K_FT, x_ft)


def keel_top_ft(x_ft):
    """The keel's top at `x_ft`, feet above WL1 (below it): the body plan's base."""
    return -(WL1_ABOVE_KEEL_TOP_MID_FT + DRAG_FT * (MIDSHIPS_FT - x_ft) / 168.0)


def pt(x_ft, z_ft):
    """A point in the drawings' frame as the file's [x, z]."""
    return [x_m(x_ft), z_m(z_ft)]


# ---------------------------------------------------------------------------
# The decks (Bel-D §3.2, §3.5; tasks 5 and 8): (ft from AP, ft above WL1)
# ---------------------------------------------------------------------------

# Each deck at the middle line, the surface the mean of the top and middle of the three red lines
# ZAZ1357 draws for it (measured, both readers within 0.03 ft, Bel §3.3; task 8: the depth in hold
# from ZAZ1359's limber strake lands midway between those lines, the checker), aft and forward on
# the top line where only it was read (Bel-D §3.2's figures): the lower deck 1.47 m aft, 0.95 at
# the middle, 1.60 at 165 ft; the upper 3.65, 3.16, 3.80; the quarterdeck from the stern to its
# breast at 78-80 ft. The forecastle measured at 125 and 140 ft (the mean of its top and middle
# lines, Bel §3.3) and carried on its slope from its after end at about 121 ft to 162 ft (Dragon's
# plan, 1363F: "from about 119 to 164 ft"; judgement beyond the two).
DECKS_FT = {
    "lower": [(2.0, 5.08), (84.0, 3.395), (165.0, 5.51)],
    "upper": [(2.0, 12.24), (84.0, 10.645), (165.0, 12.74)],
    "quarterdeck": [(2.0, 19.24), (60.0, 17.72), (79.0, 17.22)],
    "forecastle": [(121.0, 17.80), (125.0, 17.915), (140.0, 18.35), (162.0, 18.99)],
}
# The poop, the roundhouse deck, measured in task 5 (Bel-D §3.5 judged it to about 23 ft from AP,
# 1 ft 3 in under its rail, no sheet read having drawn it): ZAZ1359's inboard profile draws it in
# red, the alteration taken as fitted (Bel §3.3), its beams hung under it, from the stern timbers
# about 11 ft abaft AP to its breast beam 36.75 ft before AP; ZAZ1357's sheer draws the same red
# pair at the same heights within 0.15 ft along its whole length (the two sheets' registrations
# differ by 0.18 ft at the quarterdeck) and its red end post at 36.74 ft. Its middle line, the mean
# of ZAZ1357's red pair (the top and middle lines, as every deck of hers), feet above WL1. ZAZ1359
# draws one more beam in green, carrying it to 39.0 ft, green being that sheet's colour for the
# Arrogants' alterations (Bel §5.2); unlabelled, it is recorded and not taken (judgement). The
# mizen (26.8 ft) and the wheel (about 31 ft) stand under it, the captain's cabin and the coach
# under its after part (Dragon's quarterdeck plan, 1363F: Bel §3.4), as Steel has a 74's ("the
# round-house beams ... the foremost stantion of the steering wheel, and the mizen mast": Steel
# 1805, OCR l. 17620-17621, read (OCR)).
POOP_MIDDLE_LINE_FT = [
    (-11.3, 26.50), (-10.0, 26.45), (-8.0, 26.34), (-6.0, 26.24), (-4.0, 26.125),
    (-2.0, 26.02), (2.0, 25.845), (6.0, 25.655), (10.0, 25.48), (16.0, 25.24),
    (20.0, 25.095), (24.0, 24.96), (28.0, 24.815), (32.0, 24.69), (36.0, 24.575),
    (36.75, 24.55),
]  # fmt: skip
# The roundhouse beams round up 10 in for a 74 (Steel 1805, the tables of dimensions, ROUNDHOUSE,
# 'BEAMS ... to round up', OCR l. 39678, the 80's and the 74's alike; read (OCR), garbled): the
# deck at the side so much under its middle line (rule).
POOP_ROUND_UP_FT = 10.0 / 12.0
POOP_GREEN_BREAST_FT = 39.0

# ---------------------------------------------------------------------------
# The ports and their sills (Bel-D §3.3; tasks 4 and 6): (ft from AP, sill ft above WL1)
# ---------------------------------------------------------------------------

# The lower deck: fourteen a side, centres and sills measured on ZAZ1357 (both readers; the
# checker's boxes, Bel §3.1, §3.3); Dragon's gun-deck plan (1361F) puts L7-L9 within 0.1 ft.
LOWER_PORTS_FT = [
    (12.21, 6.74), (23.00, 6.37), (33.78, 6.07), (44.61, 5.82), (55.41, 5.68), (66.26, 5.54),
    (76.95, 5.44), (88.90, 5.45), (99.77, 5.55), (110.60, 5.75), (121.41, 6.00), (132.18, 6.33),
    (142.99, 6.71), (153.84, 7.13),
]  # fmt: skip
# The upper deck: fourteen a side, the red altered places taken as fitted (Bel §3.3; the
# checker's red centres for 1-6, the seventh tentative), their sills measured.
UPPER_PORTS_FT = [
    (7.33, 13.50), (18.02, 13.06), (28.81, 12.70), (39.63, 12.43), (50.38, 12.22), (61.24, 12.10),
    (72.60, 12.00), (83.63, 11.95), (94.71, 12.07), (105.59, 12.22), (116.45, 12.48),
    (127.20, 12.81), (138.04, 13.20), (149.49, 13.67),
]  # fmt: skip
# The quarterdeck: seven a side at ZAZ1357's places (Q1-Q2 black, Q3-Q7 red), sills measured
# (Bel §3.3); Dragon's plan puts them 0.46-0.65 ft further forward, recorded.
QUARTERDECK_PORTS_FT = [
    (8.70, 20.16), (18.51, 19.76), (28.19, 19.44), (37.41, 19.16), (46.50, 18.96), (56.11, 18.79),
    (65.79, 18.66),
]  # fmt: skip
# The forecastle: two a side on Dragon's plan (1363F) at about 139 and 153 ft (Bel §3.3, one
# reader, ±1.5 ft; task 6, read again at full resolution: two a side, 13.6 ft apart at the sheet's
# 100 px to the foot), where ZAZ1357 draws timberheads; their sills the forecastle deck and 1 ft,
# the quarterdeck's standing 1.0-1.1 ft over their deck (judgement). No chase port is drawn (1361F,
# 1362F: Bel §3.4); Elephant's as-built decks (J2938) were not read.
FORECASTLE_PORTS_X_FT = (139.0, 153.0)
FORECASTLE_SILL_ABOVE_DECK_FT = 1.0
# The 1795 fit's places over the rail (Bel-D §3.3, §5.1, judgement): the forecastle carronade's at
# 128 ft and the poop's three a side at 4, 12 and 20 ft from AP, each triple 2 in under the rail,
# the gun firing over it (the 64's convention).
FORECASTLE_CARRONADE_X_FT = 128.0
POOP_PLACES_X_FT = (4.0, 12.0, 20.0)
OVER_THE_RAIL_M = 0.05
# The ports' sizes, width by depth (Bel §3.3, measured): the lower 3 ft 4 3/4 in by 2 ft 8 1/2 in
# (the checker's fourteen boxes 3.38-3.42 by 2.71-2.73 ft), the upper 2 ft 9 in by 2 ft 7 1/2 in,
# the quarterdeck 2 ft 7 in by 2 ft 4 in; the forecastle's and the roundhouse's as the
# quarterdeck's (judgement), the roundhouse's drawing no port: its triples are gun places over the
# rail, 2 in under it, which the viewer's rule reads by the side's own test against the deck's size
# (Build-Ships.md §6's postscript, item 3; the 64's).
PORT_SIZE_FT = {
    "lower": (3.0 + 4.75 / 12.0, 2.0 + 8.5 / 12.0),
    "upper": (2.75, 2.0 + 7.5 / 12.0),
    "quarterdeck": (2.0 + 7.0 / 12.0, 2.0 + 4.0 / 12.0),
    "forecastle": (2.0 + 7.0 / 12.0, 2.0 + 4.0 / 12.0),
    "roundhouse": (2.0 + 7.0 / 12.0, 2.0 + 4.0 / 12.0),
}

# ---------------------------------------------------------------------------
# The body plan (tasks 3 and 4): her sections above the water, moulded, by station
# ---------------------------------------------------------------------------

# Each section traced on ZAZ1357's body plan (its base the keel's top, 5507.5 px; its middle line
# 2930.5 px; the sheet's background levelled) from where it crosses WL1, its crossing there seeded
# by the half-breadth plan's WL1 at its station (Bel §3.2.3) and followed upward a tenth of a foot
# at a time, the traces overlaid on the sheet and looked at: (ft above WL1 at the station,
# half-breadth moulded ft), at the frame stations' places on the sheer plan (measured, the stations'
# lines found by column there: the after body's 26 at 14.85 ft, 24 at 20.27, 20 at 31.10, 18 at
# 36.52, 16 at 41.94, 14 at 47.34, 12 at 52.70, 10 at 58.11, 8 at 63.61, 6 at 69.02, 4 at 74.30, 2
# at 79.70 and the two lettered (3) and (2) at 85.06 and 87.62; the dead flat at 91.61, the mean of
# the two bodies' traces; the fore body's at 97.04, 102.50, 107.95, 113.33, 118.75, 124.10, 129.50,
# 140.27, 145.66, 151.08 and 156.46, the last seeded by its own crossing on WL1, 15.0 ft, the
# half-breadth plan's WL1 not read there). Re-traced at the review (2026-11-10) from 41.94 to 129.50
# ft: the first trace had dropped the dead flat's own line where it stands 22.98-23.13 ft out
# (taken there for the breadth line), carried the stations about the middle on the line inside it
# from 2 to 8 ft above WL1 and 52.70 on 47.34's, and run 41.94 to 58.11 and 129.50 on the
# outermost line in the topsides. Each line followed a pixel row at a time on the sheet's red
# channel levelled, its slope carried, and each station set on its line by the lines' order (the
# sections nest, the dead flat outermost: in the after body 63.61 the line inside it below 27 ft
# above the keel, then 58.11, 52.70, 47.34 and 41.94 one line in each; 69.02 to 87.62 on the dead
# flat's; in the fore body 97.04 to 118.75 on the dead flat's, 124.10 and 129.50 the next two, the
# untraced 134.9 the third); where two lines run together, within about 0.03 ft, both on that one,
# overlaid on the sheet and looked at. The second method: the midship section the checker measured
# on its own (Bel §3.2.4: 22.76 ft at the midship sill, 24.3 ft above the keel; 22.6 at 25, 22.28
# at 26, 21.91 at 27, 21.45 at 28), within 0.01 ft of the re-traced dead flat from 24.3 to 27 ft and
# 0.05 at 28, where the table's rows stand 2 ft apart. At WL1 every line from 47 to 92 ft stands
# 0.14-0.18 ft outside the half-breadth plan's WL1, the dead flat's 23.06 ft against 22.92 (its
# moulded breadth 46 ft 1 in, Bel §3.2.4, the body plan's); the file's WL1 stays the half-breadth
# plan's (judgement). The stations abaft 14.85 ft, the fore body's at 134.9 ft and those forward of
# 156.46 ft were not traced cleanly (the traces left their curves) and are left out.
BODY_PLAN_FT = {
    14.85: [(2.0, 16.24), (4.0, 17.1), (5.0, 17.35), (6.0, 17.48), (7.0, 17.48), (8.0, 17.41),
            (10.0, 17.08), (12.0, 16.43), (13.0, 15.97), (14.0, 15.46), (15.0, 15.03)],
    20.27: [(2.0, 19.32), (4.0, 19.6), (5.0, 19.63), (6.0, 19.59), (7.0, 19.48), (8.0, 19.32),
            (10.0, 18.76), (12.0, 17.84), (13.0, 17.24), (14.0, 16.66), (15.0, 16.18)],
    31.1: [(2.0, 21.03), (4.0, 21.09), (5.0, 21.06), (6.0, 20.96), (7.0, 20.8), (8.0, 20.55),
           (10.0, 19.83), (12.0, 18.69), (13.0, 17.99), (14.0, 17.41), (15.0, 16.92)],
    36.52: [(2.0, 21.63), (4.0, 21.64), (5.0, 21.58), (6.0, 21.46), (7.0, 21.26), (8.0, 20.98),
            (10.0, 20.17), (12.0, 18.93), (13.0, 18.23), (14.0, 17.66), (15.0, 17.19)],
    41.94: [(2.0, 22.11), (4.0, 22.09), (5.0, 22.01), (6.0, 21.85), (7.0, 21.62), (8.0, 21.31),
            (10.0, 20.44), (12.0, 19.12), (13.0, 18.43), (14.0, 17.88), (15.0, 17.43)],
    47.34: [(2.0, 22.43), (4.0, 22.39), (5.0, 22.29), (6.0, 22.12), (7.0, 21.86), (8.0, 21.53),
            (10.0, 20.6), (12.0, 19.22), (13.0, 18.59), (14.0, 18.06), (15.0, 17.63)],
    52.7: [(2.0, 22.68), (4.0, 22.61), (5.0, 22.48), (6.0, 22.3), (7.0, 22.02), (8.0, 21.66),
           (10.0, 20.69), (12.0, 19.32), (13.0, 18.69), (14.0, 18.17), (15.0, 17.76)],
    58.11: [(2.0, 22.84), (4.0, 22.75), (5.0, 22.62), (6.0, 22.42), (7.0, 22.13), (8.0, 21.77),
            (10.0, 20.77), (12.0, 19.35), (13.0, 18.75), (14.0, 18.27), (15.0, 17.86)],
    63.61: [(2.0, 22.97), (4.0, 22.87), (5.0, 22.73), (6.0, 22.51), (7.0, 22.23), (8.0, 21.86),
            (10.0, 20.81), (12.0, 19.42), (13.0, 18.83), (14.0, 18.33), (15.0, 17.93)],
    69.02: [(2.0, 23.06), (4.0, 22.97), (5.0, 22.81), (6.0, 22.59), (7.0, 22.29), (8.0, 21.89),
            (10.0, 20.84), (12.0, 19.45), (13.0, 18.86), (14.0, 18.36), (15.0, 17.96)],
    74.3: [(2.0, 23.07), (4.0, 22.98), (5.0, 22.82), (6.0, 22.6), (7.0, 22.31), (8.0, 21.91),
           (10.0, 20.88), (12.0, 19.5), (13.0, 18.88), (14.0, 18.38), (15.0, 17.98)],
    79.7: [(2.0, 23.07), (4.0, 22.98), (5.0, 22.83), (6.0, 22.62), (7.0, 22.32), (8.0, 21.93),
           (10.0, 20.91), (12.0, 19.52), (13.0, 18.91), (14.0, 18.41), (15.0, 18)],
    85.06: [(2.0, 23.07), (4.0, 22.99), (5.0, 22.84), (6.0, 22.63), (7.0, 22.34), (8.0, 21.96),
            (10.0, 20.94), (12.0, 19.56), (13.0, 18.95), (14.0, 18.43), (15.0, 18.02)],
    87.62: [(2.0, 23.07), (4.0, 22.99), (5.0, 22.85), (6.0, 22.64), (7.0, 22.35), (8.0, 21.97),
            (10.0, 20.95), (12.0, 19.58), (13.0, 18.97), (14.0, 18.44), (15.0, 18.03)],
    91.61: [(2.0, 23.05), (4.0, 22.98), (5.0, 22.85), (6.0, 22.65), (7.0, 22.36), (8.0, 21.99),
            (10.0, 21), (12.0, 19.57), (13.0, 18.91), (14.0, 18.36), (15.0, 17.94)],
    97.04: [(2.0, 23.04), (4.0, 22.98), (5.0, 22.86), (6.0, 22.66), (7.0, 22.37), (8.0, 22.02),
            (10.0, 21.04), (12.0, 19.58), (13.0, 18.87), (14.0, 18.29), (15.0, 17.86)],
    102.5: [(2.0, 23.04), (4.0, 22.98), (5.0, 22.86), (6.0, 22.68), (7.0, 22.39), (8.0, 22.04),
            (10.0, 21.08), (12.0, 19.63), (13.0, 18.9), (14.0, 18.32), (15.0, 17.88)],
    107.95: [(2.0, 23.04), (4.0, 22.99), (5.0, 22.87), (6.0, 22.69), (7.0, 22.41), (8.0, 22.06),
             (10.0, 21.11), (12.0, 19.68), (13.0, 18.94), (14.0, 18.35), (15.0, 17.91)],
    113.33: [(2.0, 23.04), (4.0, 22.99), (5.0, 22.87), (6.0, 22.7), (7.0, 22.43), (8.0, 22.08),
             (10.0, 21.15), (12.0, 19.72), (13.0, 18.97), (14.0, 18.38), (15.0, 17.93)],
    118.75: [(2.0, 23.04), (4.0, 22.99), (5.0, 22.88), (6.0, 22.71), (7.0, 22.44), (8.0, 22.1),
             (10.0, 21.17), (12.0, 19.77), (13.0, 19.01), (14.0, 18.41), (15.0, 17.95)],
    124.1: [(2.0, 22.96), (4.0, 22.92), (5.0, 22.83), (6.0, 22.66), (7.0, 22.42), (8.0, 22.12),
            (10.0, 21.2), (12.0, 19.82), (13.0, 19.04), (14.0, 18.44), (15.0, 17.97)],
    129.5: [(2.0, 22.8), (4.0, 22.77), (5.0, 22.7), (6.0, 22.55), (7.0, 22.33), (8.0, 22.03),
            (10.0, 21.17), (12.0, 19.86), (13.0, 19.05), (14.0, 18.4), (15.0, 17.92)],
    140.27: [(2.0, 21.78), (4.0, 21.82), (5.0, 21.79), (6.0, 21.7), (7.0, 21.54), (8.0, 21.3),
             (10.0, 20.57), (12.0, 19.52), (13.0, 18.76), (14.0, 18.09), (15.0, 17.61)],
    145.66: [(2.0, 20.69), (4.0, 20.78), (5.0, 20.77), (6.0, 20.72), (7.0, 20.6), (8.0, 20.41),
             (10.0, 19.79), (12.0, 18.82), (13.0, 18.16), (14.0, 17.6), (15.0, 17.15)],
    151.08: [(2.0, 18.83), (4.0, 19.08), (5.0, 19.11), (6.0, 19.08), (7.0, 19.0), (8.0, 18.87),
             (10.0, 18.36), (12.0, 17.56), (13.0, 17.06), (14.0, 16.66), (15.0, 16.33)],
    156.46: [(2.0, 15.8), (4.0, 16.23), (5.0, 16.35), (6.0, 16.4), (7.0, 16.39), (8.0, 16.31),
             (10.0, 15.97), (12.0, 15.45), (13.0, 15.25), (14.0, 15.11), (15.0, 15.01)],
}  # fmt: skip
# The plank outside the moulded lines, 4 1/2 in (the 64's; Steel's 5-in plank less judgement:
# Bel-D §3.4), so that a triple's half-breadth is the side's outside the plank, where the outer
# sill meets the water as she heels (judgement).
PLANK_FT = 4.5 / 12.0
# Above the traced band the side tumbles home as the dead flat's traced top does, 0.38 ft of
# half-breadth to the foot (33 to 35 ft above the keel), carried up to the quarterdeck's and the
# forecastle's sills and the top of the side (judgement on the traced sections).
TUMBLEHOME_PER_FT = 0.38

# The midship section, moulded (ft above the keel's top, half-breadth): the floor, the bilge and
# the dead flat traced on ZAZ1357's body plan to 25 ft (the research's trace, Bel §3.2.4: the
# floor rising 0.3-0.4 ft from 3 to 8 ft out, 3.4-4.6 degrees by that rise, the research's "2-3
# degrees" a slip; these points rise 0.41 ft from 3.3 to 8.7 ft out, 4.3 degrees), the tumblehome
# to 28 ft the checker's (Bel §3.2.4), and above it to the waist rail at 35 ft traced here (task 3:
# the dead flat of `BODY_PLAN_FT`, both bodies' traces within 0.2 ft).
SECTION_FT = [
    (0.0, 0.85), (0.6, 3.3), (0.71, 5.1), (0.86, 6.9), (1.01, 8.7), (1.22, 9.9), (1.56, 11.1),
    (2.09, 12.3), (2.79, 13.5), (3.65, 14.7), (4.68, 15.9), (5.84, 17.1), (7.16, 18.3),
    (8.61, 19.5), (9.89, 20.42), (11.5, 21.36), (13.1, 22.09), (14.7, 22.57), (16.3, 22.87),
    (17.0, 22.96), (23.0, 22.95), (24.0, 22.81), (24.3, 22.76), (25.0, 22.6), (26.0, 22.28),
    (27.0, 21.91), (28.0, 21.45), (29.0, 20.88), (30.0, 20.18), (31.0, 19.43), (32.0, 18.8),
    (33.0, 18.28), (34.0, 17.86), (35.0, 17.53),
]  # fmt: skip

# ---------------------------------------------------------------------------
# The profile's lines (Bel-D §3.2; tasks 1, 2, 3 and 5)
# ---------------------------------------------------------------------------

# The top of the side, from the taffrail to the beakhead bulkhead, (ft from AP, ft above WL1),
# measured on ZAZ1357 by columns (task 3; Bel §3.3's figures, read again: within 0.2 ft at every
# station forward of the drift): the taffrail's crown 13 ft abaft AP, 30.25 ft above WL1 (task 1),
# where the top rail meets the stern at 11.5 ft abaft; the poop's rail, over its red raised deck
# where that stands higher than the black rail (the red line, ZAZ1357, to the poop's breast at 36.75
# ft; judgement that the side was raised with the deck); the black rail to the drift's scroll at
# 40.2 ft; the quarterdeck's rail to its breast at 72-79 ft; the waist rail, 16.1-16.7 ft; the
# forecastle's from its breast at about 120.5 ft to the beakhead bulkhead, about 12.5 ft before the
# foremast (Dragon's upper deck, 1362F: Bel §3.4). Between 8.5 ft abaft and 3.7 ft before AP the
# quarter gallery's finishing covers the rail, and it is taken straight across (judgement).
RAIL_FT = [
    (-13.05, 30.25), (-11.5, 28.55), (-8.0, 27.13), (6.0, 26.41), (8.0, 26.18), (10.0, 25.95),
    (12.0, 25.75), (16.0, 25.34), (20.0, 25.10), (24.0, 24.96), (28.0, 24.82), (32.0, 24.69),
    (36.0, 24.58), (36.75, 24.55), (37.0, 23.47), (39.0, 23.24), (40.2, 22.40), (42.0, 22.07),
    (46.0, 21.81), (50.0, 21.58), (55.0, 21.33), (60.0, 21.07), (64.0, 20.89), (68.0, 20.72),
    (72.0, 19.40), (76.0, 19.26), (78.5, 18.40), (79.5, 16.25), (84.0, 16.13), (100.0, 16.15),
    (110.0, 16.35), (115.0, 16.50), (119.5, 16.70), (120.5, 18.30), (122.0, 18.77),
    (125.0, 18.98), (130.0, 19.25), (135.0, 19.54), (140.0, 19.62), (145.0, 20.23),
    (150.0, 20.62), (155.0, 21.04), (158.0, 21.29), (161.6, 21.30),
]  # fmt: skip
# The stem's fore edge, (ft from AP, ft above WL1), low to high (task 2): the foremost of the two
# lines ZAZ1357 draws along the stem proper, abaft the knee and the gripe, traced row by row (the
# sheet's background levelled), from its foot boxed into the keel's top at the main keel's square
# fore end, 157.7 ft, through WL1 at 169.02 ft (Bel §3.2.6's "168.2-169.0", its two readers each on
# one of the two lines), to 7 ft above WL1; behind the cheeks and the head it is carried on its
# rake to the stem head under the bowsprit, 170.13 ft and 16.25 ft above WL1, where both sheets
# begin the bowsprit's lower edge (task 7, within 0.05 ft: ZAZ1357 170.13, ZAZ1359 170.10).
STEM_FT = [
    (157.7, None), (159.35, -17.0), (160.86, -16.0), (162.08, -15.0), (163.11, -14.0),
    (164.0, -13.0), (164.76, -12.0), (165.47, -11.0), (166.07, -10.0), (166.61, -9.0),
    (167.06, -8.0), (167.49, -7.0), (167.85, -6.0), (168.14, -5.0), (168.36, -4.0),
    (168.55, -3.0), (168.74, -2.0), (168.89, -1.0), (169.02, 0.0), (169.22, 2.0), (169.40, 4.0),
    (169.55, 6.0), (169.62, 7.0), (169.80, 10.0), (170.0, 13.0), (170.13, 16.25),
]  # fmt: skip
STEM_HEAD_FT = STEM_FT[-1]
# The knee of the head's fore edge, (ft from AP, ft above WL1), low to high (task 2): the gripe's,
# the cutwater's and the knee's, from K at the main keel's square fore end through the forefoot to
# the head's top under the bowsprit, traced row by row on ZAZ1357 (its background levelled): below
# WL1 within 0.1 ft of Bel §3.2.6's two readers at every depth they give (0 at 172.0-172.5, 2.9 at
# 170.9-171.2, 9.9 at 167.7, 14.9 at 165.1, 17.9 at 163.1-163.4, 18.9 at 161.9-162.0); above it
# 183.5 ft at its most forward, 15-16 ft above WL1, falling back to 182.5 ft at its top, 22 ft above
# WL1, under the figure. Lavery 1985 D7 (the head from the side, her class's own drawing, the
# owner's photograph) shows the same sweep, compared by eye.
HEAD_FT = [
    (157.7, None), (160.97, -19.5), (161.9, -19.0), (163.06, -18.0), (163.89, -17.0),
    (164.55, -16.0), (165.15, -15.0), (165.7, -14.0), (166.21, -13.0), (166.7, -12.0),
    (167.65, -10.0), (168.56, -8.0), (169.46, -6.0), (170.39, -4.0), (171.40, -2.0),
    (172.51, 0.0), (173.74, 2.0), (175.14, 4.0), (176.82, 6.0), (178.82, 8.0), (180.82, 10.0),
    (182.45, 12.0), (183.26, 14.0), (183.51, 16.0), (183.28, 18.0), (183.06, 20.0),
    (182.53, 22.0),
]  # fmt: skip
# The post's after face and the stern to the taffrail, (ft from AP, ft above WL1), low to high
# (task 1): the post's heel 0.37 ft before AP on K and its after face 0.80 ft abaft AP at WL1,
# raking 3.4 degrees (traced on ZAZ1357; Bel §3.2.6's 0.36-0.39 and 0.85 within 0.05 ft); the
# counter's knuckle at the wing transom, 7.42 ft above WL1 at the middle line (`WING_TRANSOM_FT`);
# the counter and the stern's after edge traced row by row from there to the taffrail's crown, 13.05
# ft abaft AP and 30.25 ft above WL1 (the quarter gallery and its drop, and the quarter piece, left
# out; ±0.2 ft; read again on a registered grid of feet, the same). ZAZ1359's inboard profile draws
# the stern's top without the crown's arch, 28.75 ft above WL1 at 13.9 ft abaft AP, and its rail
# 0.3 ft under ZAZ1357's at 11.5 ft abaft: recorded, ZAZ1357's elevation taken.
STERN_FT = [
    (0.37, None), (-0.80, 0.0), (-1.24, 7.42), (-1.69, 9.0), (-2.48, 10.0), (-3.80, 11.0),
    (-6.58, 12.0), (-6.91, 13.0), (-7.48, 14.0), (-7.72, 15.0), (-8.69, 16.0), (-8.79, 17.0),
    (-9.04, 18.0), (-9.18, 19.0), (-9.36, 20.0), (-9.95, 22.0), (-10.54, 24.0), (-11.19, 26.0),
    (-12.06, 28.0), (-12.83, 29.0), (-13.05, 30.25),
]  # fmt: skip
# K under the post's heel and at the main keel's square fore end (Bel §3.2.1, §3.2.6).
KEEL_FT = (0.37, 157.7)
# The main wale (task 3 did not trace it along the length): at 81 ft its lower edge 0.27-0.37 ft
# below WL1 and its upper edge 3.9-4.0 ft above it (the checker, Bel §3.3), carried along the
# length parallel to the lower deck's sills (judgement), 10 to 160 ft.
MAIN_WALE_AT_81_FT = (-0.32, 3.95)
# The channel wale (likewise): 8.6 to 11.2 ft above WL1 at midships, between the lower port tops
# and the upper sills (the researcher, Bel §3.3), carried parallel to the upper deck's sills
# (judgement), 10 to 160 ft.
CHANNEL_WALE_MID_FT = (8.6, 11.2)

# WL1's half-breadths by station, moulded (Bel §3.2.3, the checker's corrected WL1: ±0.15 ft from
# 20 to 140 ft and ±0.5 at the ends), (ft from AP, ft).
WL1_HALF_BREADTHS = [
    (10.0, 13.94), (20.0, 18.53), (30.0, 20.43), (40.0, 21.62), (50.0, 22.41), (60.0, 22.73),
    (70.0, 22.90), (80.0, 22.92), (90.0, 22.92), (100.0, 22.91), (110.0, 22.91), (120.0, 22.87),
    (130.0, 22.66), (135.0, 22.14), (140.0, 21.45), (145.0, 20.39), (150.0, 18.71),
    (155.0, 16.06),
]  # fmt: skip
# WL1 to WL5 by station (Bel §3.2.3, measured), moulded, ft; WL1 at 160 ft not resolved (under
# 13.7 ft), so that station gives WL2-WL5 alone.
WATERLINES = {
    10.0: (13.94, 7.67, 3.27, 1.61, 0.79),
    20.0: (18.53, 14.99, 8.91, 4.28, 1.76),
    30.0: (20.43, 18.53, 14.17, 8.36, 3.45),
    40.0: (21.62, 20.38, 17.26, 12.46, 6.09),
    50.0: (22.41, 21.47, 19.10, 15.34, 9.46),
    60.0: (22.73, 22.10, 20.20, 17.03, 12.31),
    70.0: (22.90, 22.41, 20.88, 18.02, 14.02),
    80.0: (22.92, 22.54, 21.14, 18.50, 14.65),
    90.0: (22.92, 22.54, 21.16, 18.56, 14.76),
    100.0: (22.91, 22.54, 21.12, 18.56, 14.71),
    110.0: (22.91, 22.51, 21.08, 18.34, 14.25),
    120.0: (22.87, 22.28, 20.65, 17.64, 12.99),
    130.0: (22.66, 21.66, 19.53, 16.08, 10.61),
    140.0: (21.45, 20.08, 17.35, 13.13, 7.13),
    150.0: (18.71, 16.64, 13.15, 8.43, 3.41),
    160.0: (None, 9.21, 5.88, 2.75, 0.58),
}
# WL2 to WL5 below WL1 (Bel §3.2.2: WL1 18.89 ft above the keel's top at midships, WL2-WL5 at
# 15.12, 11.38, 7.58 and 3.85).
WL_BELOW_WL1_FT = (0.0, 3.77, 7.51, 11.31, 15.04)

# The stern (task 1; form.stern): the wing transom, the transom's foot, its line traced across the
# body plan from the middle line to its end, 7.42 ft above WL1 at the middle line and 7.15 ft at its
# ends, 15.0 ft out, so rounded up 0.28 ft (the sheer's tuck rail ending in its scroll at 7.3-7.6 ft
# above WL1, 0.67 ft abaft AP, the check; Bel §3.3's two readings of the counter's knuckle, 5.8 ft
# and 7.5-7.9 ft, settled for the second); the stern's outline seen from aft, the side counter
# timbers' (ft above WL1 at AP, half-breadth moulded), from the wing transom's end to the
# taffrail's side, 9.9 ft out at 28.4 ft above WL1 (the body plan's innermost line of the after
# body, traced row by row, ±0.05 ft).
WING_TRANSOM_FT = (7.42, 7.15, 15.0)
STERN_OUTLINE_FT = [
    (7.15, 15.0), (7.8, 14.96), (8.3, 14.9), (9.3, 14.57), (10.3, 13.96), (10.8, 13.51),
    (11.3, 12.95), (12.3, 12.6), (14.3, 12.26), (16.3, 11.91), (18.3, 11.58), (20.3, 11.25),
    (22.3, 10.91), (24.3, 10.57), (26.3, 10.25), (27.3, 10.08), (28.4, 9.91),
]  # fmt: skip
# The quarter galleries, two tiers (ft from AP aft and forward, ft above WL1 low and high): from 8.5
# ft abaft to 3.7 ft before AP, the lower at the upper deck 14.5-17.7 ft, the upper at the
# quarterdeck 21.7-24.6 ft (ZAZ1357, one reader ±0.3 ft: Bel §3.3; read again here, the lights'
# frames 15.0-18.4 and 21.4-25.0 ft); Lavery 1985 D2 (her class's own drawing, 1/96) draws the same
# two tiers of three lights over a drop.
QUARTER_GALLERIES_FT = [(-8.5, 3.7, 14.5, 17.7), (-8.5, 3.7, 21.7, 24.6)]
# The stern lights, two bands (ft above WL1 low and high, count, half-breadth ft): Lavery 1985 D1
# (the stern's decorations, 1/96, her class's own drawing, the owner's photograph): the wardroom's
# eight lights at the upper deck between pilasters, and the screen bulkhead's eight at the
# quarterdeck behind the breast rail, the foot space rail between; their heights the quarter
# gallery's tiers on ZAZ1357; their spread D1's proportions, each band's width against the stern's
# at the upper counter rail (0.95 and 0.84 of it; the photograph foreshortened in height, so read
# across only), laid on the body plan's outline there, 12.65 ft out: within 12.0 and 10.6 ft of the
# middle line (judgement on those proportions). Steel 1805's 74 (Folio LI, task 11) is not taken:
# the class's own drawing ranks before it.
STERN_LIGHTS_FT = [(14.5, 17.7, 8, 12.0), (21.7, 24.6, 8, 10.6)]

# ---------------------------------------------------------------------------
# The rig (Bel-D §4.1-§4.3)
# ---------------------------------------------------------------------------

# The masts at the upper deck (ft from AP), their heels above the keel's top and their rakes
# (measured, the checker on ZAZ1357 and ZAZ1359: Bel §5.2): the fore at 150.27 ft carried 1 ft 2 in
# aft by the Arrogant alteration noted on ZAZ1359 "for the Bellerophon" among others (read: Bel
# §5.2), upright; the main at 74.79 ft raked 1.44 degrees; the mizen at 26.80 ft raked 2.91. The
# heels on ZAZ1359: the main's shoulder 5.11 ft, the fore's 5.9 (5.5-6.3), the mizen's tenon end
# 7.85 ft (7.8-7.9), each above the keel's top.
MASTS = {
    "fore": (150.27 - 14.0 / 12.0, 5.9, 0.0),
    "main": (74.79, 5.11, 1.44),
    "mizzen": (26.80, 7.85, 2.91),
}
# Dragon's masts and yards (Lavery 1985 p. 19, Table 10, an NMM draught of the class's own time,
# about 1760: read (owner's book); Bel §13.4), feet; where Table 10 lacks a spar, Steel 1794 vol. I
# p. 49's 74 column, a mast scaled 0.973 and a yard 1.00 (Bel-D §4.1, judgement: Dragon's masts run
# 0.97-0.98 of Steel's and her yards 0.99-1.01). The main mast printed 30 yards read as 36: Lavery's
# mast drawings give the main 1.125 times the fore, 107 ft 7 in, and Steel's rule on her design 107
# ft 4 1/2 in (Bel §13.5; judgement on a misprint).
SPARS_FT = {
    "mast": {"main": 108.0, "fore": 95.0 + 8.0 / 12.0, "mizzen": 93.5},
    "topmast": {"main": 64.0 + 10.0 / 12.0, "fore": 57.75, "mizzen": 47.0 + 8.0 / 12.0},
    # the mizen's Steel's 24 ft 6 in x 0.973: Table 10 has none, the mizen topgallant coming in
    # only in 1770 (Lavery I23)
    "topgallant_mast": {"main": 33.0, "fore": 28.0 + 10.0 / 12.0, "mizzen": 24.5 * 0.973},
    "yard": {"main": 96.0 + 8.0 / 12.0, "fore": 84.0 + 4.0 / 12.0, "mizzen": 61.5},  # crossjack
    "topsail_yard": {"main": 70.5, "fore": 61.5, "mizzen": 46.0 + 1.0 / 12.0},
    # the mizen topgallant yard Steel's 31 ft 6 in (Table 10 has none)
    "tg_yard": {"main": 45.0 + 10.0 / 12.0, "fore": 40.0, "mizzen": 31.5},
    # the royal yards Steel's: Table 10, of about 1760, has none (royals on all three masts:
    # Majestic at the Nile, NRS vol. 2 p. 65: Bel §5.6)
    "royal_yard": {"main": 35.0, "fore": 31.0, "mizzen": 23.0},
    "mizen_yard": 86.5,
    "bowsprit": 66.0,
    "jib_boom": 48.0,
}
DIAMETER_IN = {"mizen_yard": 15.375, "spritsail_yard": 12.75, "sprit_topsail_yard": 8.5}
# Steel's heads (vol. I, OCR l. 4697-4699, read (OCR); p. 42): the main and fore masts' heads 5 in
# to every yard of the mast's length; the mizen mast's and the main and fore topmasts' 4 in; the
# mizen topmast's and every topgallant mast's 3 1/2 in.
HEAD_IN_PER_YARD = {
    "mast": {"main": 5.0, "fore": 5.0, "mizzen": 4.0},
    "topmast": {"main": 4.0, "fore": 4.0, "mizzen": 3.5},
    "topgallant_mast": {"main": 3.5, "fore": 3.5, "mizzen": 3.5},
}
# Steel's long pole-head (Steel 1794 vol. I p. 16, OCR l. 2934-2942, and p. 42, OCR l. 4701-4702;
# Bel-D §4.2; the owner's "Agreed", Bel-D §17.0): the table's topgallant length is the mast with a
# square head of 3 1/2 in to a yard; the long pole-head takes the head's place, set up from the
# stop, two-thirds of the length to the stop; the hounds three-fifths of the square head below it.
LONG_POLE_OF_STOP = 2.0 / 3.0
HOUNDS_OF_STOP = 3.0 / 5.0

# The bowsprit (task 7): its steeve 31.6 degrees, measured on ZAZ1357 (its two drawn edges fitted
# over 15 ft, 31.6 and 31.8 degrees; the sheet's dark lines projected, 31.5), checked on ZAZ1359
# (projected, 32.3; its heel to its root, 31.8): steeper than the 64's 27, which Bel-D §4.7 took as
# the fallback. Its heel at 155.4 ft from AP, its step before the foremast on ZAZ1359 (measured;
# the green alteration's 154.0 ft beside it, recorded), its root on the stem head (`STEM_HEAD_FT`),
# so that 17.3 ft of it lie inboard along its steeve and 48.7 ft of Table 10's 66 ft stand outboard
# (Luce's third inboard would give 44 ft).
BOWSPRIT_STEEVE_DEG = 31.6
BOWSPRIT_HEEL_FT = 155.4
# The jib-boom: 7/12 of it outboard (Luce 1866 ch. VII, the frigate's rule; judgement for her).
JIB_BOOM_OUTBOARD = 7.0 / 12.0
# The yards under the bowsprit (Ext §4.1; `spritsail_yards.cut`): Table 10's yards, 61 ft 6 in and
# 40 ft 0 in (Bel-D §4.3: her class's list before Steel's column, 62 ft 0 in and 40 ft 6 in), and
# Steel's sails (table IV, the 74 column: Bel §5.6), the sprit course 29 cloths at the head and the
# foot and 8 yards deep, the sprit topsail 18 1/2 and 29 1/2 and 10 yards deep; slung and hung as
# the 64's (judgement, the engine's fixture's).
SPRITSAIL = {"yard_m": 61.5 * FT, "head_cloths": 29.0, "foot_cloths": 29.0, "depth_yd": 8.0}
SPRIT_TOPSAIL = {"yard_m": 40.0 * FT, "head_cloths": 18.5, "foot_cloths": 29.5, "depth_yd": 10.0}
SPRITSAIL_STATION = 0.85
SPRITSAIL_HANG_M = 0.8
SPRIT_TOPSAIL_HANG_M = 0.5
SPRIT_BRACE_LIMIT_DEG = 30
SPRITSAIL_CANVAS = (2, f"{g.STEEL_SM}, 'Spritsail course': No. 2 or 3, the first taken")
SPRIT_TOPSAIL_CANVAS = (6, f"{g.STEEL_SM}, 'Spritsail topsail': No. 6 or 7, the first taken")

# Steel's sail table IV, the 74 column (Steel 1794 vol. I p. *149, read on both copies' page
# images: Bel §5.6): cloths at the head and the foot and the depth in yards (the mizen topsail's the
# mean of its middle, 13 3/4, and its clue, 14). Each cloth 22 1/2 in in the sail: 24-in canvas less
# Steel's seam for ships of 50 guns and up (Ind §5, judgement). Unscaled: her class's yards are
# Steel's within 1% (Bel §13.4; Bel-D §4.4).
STEEL_SAILS = {
    "main.course": (46.0, 48.0, 15.75),
    "fore.course": (40.0, 38.0, 13.0),
    "main.topsail": (30.0, 47.0, 19.75),
    "fore.topsail": (26.0, 41.0, 17.5),
    "mizzen.topsail": (20.5, 30.0, 13.875),
    "main.topgallant": (21.5, 30.5, 10.0),
    "fore.topgallant": (18.5, 26.5, 8.75),
    "mizzen.topgallant": (15.0, 21.0, 7.25),
    "main.royal": (17.0, 22.0, 7.5),
    "fore.royal": (15.0, 19.0, 6.75),
    "mizzen.royal": (11.0, 15.0, 5.5),
}
CLOTH_IN_SAIL_FT = 22.5 / 12.0
# The triangular headsails of the same table: the cloths in the foot and the leech in yards.
STEEL_HEADSAILS = {
    "fore.staysail": (22.0, 13.0),
    "fore.topmast_staysail": (21.0, 17.5),
    "jib": (26.0, 25.0),
}
# The staysails between the masts in the same table (Bel §5.6): its row in words; its figures, the
# cloths at the head and at the foot, the bunt and the after leech in yards (the main staysail a
# triangle); and its area by Steel's rule for the canvas, m2, with Bel-D §4.4's band, ±10% the
# triangle and ±25% the four-sided. Steel's 74 has no mizen topgallant staysail; she carries none.
STEEL_BETWEEN = {
    "main.staysail": ("0 / 31 cloths, leech 15 3/4 yards", (0.0, 31.0, None, 15.75), 128.0, 0.10),
    "main.topmast_staysail": (
        "25 / 27 cloths, bunt 9 1/2, after leech 24 yards",
        (25.0, 27.0, 9.5, 24.0),
        228.0,
        0.25,
    ),
    "middle_staysail": (
        "24 / 24 cloths, bunt 7 1/2, after leech 16 1/2 yards",
        (24.0, 24.0, 7.5, 16.5),
        150.0,
        0.25,
    ),
    "main.topgallant_staysail": (
        "21 / 21 cloths, bunt 6, after leech 15 1/2 yards",
        (21.0, 21.0, 6.0, 15.5),
        118.0,
        0.25,
    ),
    "mizzen.staysail": (
        "20 1/2 / 22 1/2 cloths, bunt 9, after leech 13 1/2 yards",
        (20.5, 22.5, 9.0, 13.5),
        126.0,
        0.25,
    ),
    "mizzen.topmast_staysail": (
        "19 / 20 cloths, bunt 6 1/2, after leech 14 1/2 yards",
        (19.0, 20.0, 6.5, 14.5),
        107.0,
        0.25,
    ),
}
# The mizen course (Steel's table IV, the 74 column: Bel §5.6): 16 cloths at the head and 17 at the
# foot, its fore (mast) leech 11 yards and its after leech 21.
STEEL_MIZEN_COURSE = (16.0, 17.0, 11.0, 21.0)
# Steel's driver boomsail (the same column; Ext §17.2): 25 1/2 cloths at the head and 32 1/2 at the
# foot, its fore leech 11 yards and its after leech 24.
STEEL_DRIVER = (25.5, 32.5, 11.0, 24.0)
# The mizen course's tack (Bel-D §4.5; task 5): set so that the throat stands where Lavery's I32
# (her class's mizen course and yard: the owner's photograph) draws it, about 42 ft above the deck
# the mast stands through, Steel's 11-yard fore leech below it: 9 ft above that deck. Bel-D §4.5
# first named the deck her quarterdeck, her poop then judged to end abaft the mizen; task 5
# measured the poop over the mizen to 36.75 ft, and I32 draws its deck running unbroken from the
# taffrail past the mast, so the deck is her poop, its middle line at the mast, where the tack is
# seized: the lead's ruling (2) of 2026-11-10, the design's "quarterdeck" the slip and Steel's
# "within 6 or 7 feet" the general rule beside it (the figures of the other readings are in the
# generator's report).
MIZEN_TACK_ABOVE_DECK_FT = 9.0
# The head room the driver's boom stands above the poop's middle line over its run, where the boom
# passes (Bel-D §4.6, §17.2 item 13; the lead's answer (13)): 6 ft first, to 5 ft only where a check
# breaks; past that, a report with the figures and `DRIVER = False` until the lead rules.
HEAD_ROOM_FT = (6.0, 5.0)
# The driver's boom (Bel-D §4.6; Steel 1794 vol. I p. 40, 'Driver boom, the same length as the
# main-topsail-yard', and the fore topsail yard's diameter): her own main topsail yard's 70 ft 6 in
# by 12 3/4 in. Steel's driver yard, not filed (Ext §17.2), her fore topgallant yard's 40 ft.
DRIVER_BOOM_FT = 70.5
DRIVER_YARD_FT = 40.0
# The mizen yard's lines in Steel's list for a 74 (Steel 1794 vol. II p. 37, the page image held:
# Bel §5.4, Ext §3.4), not read to their sizes here: the 64's sizes scaled with her rope
# (judgement, `mizen_course`).

# Steel's reef bands for her rate (Steel 1794 vol. I, the sail-making articles, read (OCR); Bel
# §5.6): two in each course; four in the main topsail (three or four, the four taken), three in the
# fore and mizen topsails; one in the mizen course a fifth up its mast leech; none in the driver.
REEFS = {"course": 2, "topsail": {"main": 4, "fore": 3, "mizzen": 3}, "topgallant": 0, "royal": 0}

# The brace limits, degrees from square: the frigate-36's (Fincham 1843 art. 102, the long ships'
# upper values, two degrees more a level aloft), as the owner accepted them for the 64 (2026-10-29:
# "Reasonable", the lee topmast backstays eased when braced sharp up; Bel-D §4.3). Task 10, against
# her own lee rigging from her channels (Bel §3.3) and her file's masts (measured here, by the plan
# bearing and again by a sweep of the yard's arm, agreeing to 0.01 deg): the lower yards, slung 2 ft
# under the hounds with their axis 2 ft before the mast's (1 1/2 ft the cross-jack's; judgement),
# meet the foremost lee shroud only at 71 (fore), 72 (main) and 67 (cross-jack) degrees; the
# foremost lee topmast backstay, set up, would stop the fore yard at about 56, the main at 60 and
# the cross-jack at 47 (her shrouds ten, seven the mizen's, and three backstays, two the mizen's,
# spaced evenly along each channel, their deadeyes 2 ft outside the plank: judgement). No limit is
# changed by them (the owner's word only).
BRACE_PLANS = {
    "fore": [("course", 62), ("topsail", 64), ("topgallant", 66), ("royal", 68)],
    "main": [("course", 64), ("topsail", 66), ("topgallant", 68), ("royal", 70)],
    "mizzen": [("topsail", 62), ("topgallant", 64), ("royal", 66)],
}
CROSSJACK_BRACE_DEG = 60
# Her channels (Bel §3.3, measured, the researcher): main 39-74 ft from AP at 17.2 ft above WL1,
# fore 119-148 ft at 16.8 ft, mizen 11-24 ft at 19.8 ft.
CHANNELS_FT = {
    "fore": (119.0, 148.0, 16.8),
    "main": (39.0, 74.0, 17.2),
    "mizzen": (11.0, 24.0, 19.8),
}
# The shrouds a side (the 64's count on ZAZ1407's main channel, ten, and the razee's mizen's seven:
# judgement for her, her channels' deadeyes not counted).
SHROUDS = {"fore": 10, "main": 10, "mizzen": 7}

# The frigate-36's plain sail, m2, against which her rope is scaled (Bel-D §4.3).
FRIGATE_PLAIN_SAIL_M2 = 1584.0

# Her studding sails, the frigate-36's set (Bel-D §4.4): Steel's table IV, the 74 column (Bel §5.6),
# cloths at the head and the foot and the depth in yards; and Steel's p. 40 rules on her own yards
# for the booms (Bel-D §4.3): the lower boom five-ninths of the main yard, the topmast booms half
# the lower yards, the topgallant booms half the topsail yards. Steel's main lower studding sail (19
# / 19 / 18 1/2, 184 m2) against the one pair of lower booms is not built, as the 64's.
STUDDING = {
    ("fore", "lower"): (18.0, 18.0, 15.0, 5.0 / 9.0 * (96.0 + 8.0 / 12.0)),
    ("fore", "topmast"): (14.0, 18.0, 18.5, 0.5 * (84.0 + 4.0 / 12.0)),
    ("fore", "topgallant"): (10.0, 14.0, 9.25, 0.5 * 61.5),
    ("main", "topmast"): (15.0, 19.0, 23.75, 0.5 * (96.0 + 8.0 / 12.0)),
    ("main", "topgallant"): (11.0, 15.0, 10.25, 0.5 * 70.5),
}
STEEL_STUDDING_FT = {"lower": "53-9", "fore topmast": "42-6", "main topmast": "48-6"}

# The storm canvas's heights above the deck she works it from (the frigate-36's, judgement there;
# Steel's): the mizen stay's collar 12 ft up the main mast; the mizzen storm staysail's head 0.6 of
# the way up the stay and its clew 7 ft above the deck; the storm mizzen's tack 4 ft up its stay,
# its luff 0.8 of the stay's run to the hounds, its foot 0.45 of the driver boom.
MIZEN_STAY_COLLAR_FT = 12.0
STORM_STAYSAIL_HEAD_OF_STAY = 0.6
STORM_STAYSAIL_CLEW_FT = 7.0
STORM_MIZZEN_TACK_FT = 4.0
STORM_MIZZEN_LUFF_OF_RUN = 0.8
STORM_MIZZEN_FOOT_OF_BOOM = 0.45
SAVE_ALL_OF_BOOM = 0.6

# What the cuts compute from the file's own keys, for the generator's report (`her_report`).
REPORT: dict = {}


# ---------------------------------------------------------------------------
# Her hull's figures (Bel-D §2.1)
# ---------------------------------------------------------------------------


def datum_ft():
    """Her datum, her upper deck at the middle (D18 (a)), feet above her water."""
    return interp(DECKS_FT["upper"], MIDSHIPS_FT) - CHANNEL_FT


DATUM = round(datum_ft() * FT, 2)

HULL = {
    "length_waterline_m": 51.2,
    "beam_m": 14.25,
    "draught_m": 6.46,
    "displacement_kg": 2600000.0,
    "gm_m": 1.36,
    "clr_x_m": 4.8,
    "lateral_area_m2": 330.0,
    "hull_speed_kn": 12.0,
    "rudder": {"area_m2": 9.82, "max_angle_deg": 35, "rate_deg_s": 3.0, "span_m": 6.67},
}
HULL_NOTES = {
    "length_waterline_m": "168 ft between the perpendiculars, the length on the gun deck "
    "(ZAZ1357's table, read; 167.97 ft measured, Bel §3.2.1); D29 (b)'s rule, as the 64's. At WL1 "
    "the post's after face stands 0.8 ft abaft AP and the stem proper meets the water at 169.0 ft "
    "(measured): 51.5-51.8 m post to stem proper, 52.8 m to the knee's outer sweep.",
    "beam_m": "46 ft 9 in extreme, the design's and the Arrogants' contract (ZAZ1357's table, "
    "read; ZAZ1070, read; answer 4); 46 ft 1 in moulded (measured, Bel §3.2.4). Elephant as built "
    "46 ft 11 1/2 in (tentative); Charnock's 47 ft 4 in not supported (Bel §3.6).",
    "draught_m": "21 ft 2 1/2 in mean to K at her water, the Channel line (Bel-D §2.2): WL1's "
    "20.93 ft and the line's 0.27 ft. The Bellona reported 21 ft 6 in and 22 ft 10 in at her best "
    "Channel draught in 1763, mean 22 ft 2 in (Lavery 1985 p. 9, Table 2, read (owner's book)): "
    "the drawn hull stands about a foot shallower at the same freeboard, the reports' datum open "
    "(Bel-D §2.2; the owner's 'Agreed', §17.0). The Audacious 21 ft 0 in (Steel 1805 p. 212).",
    "displacement_kg": "2,600 t: judgement within the drawn lines' band at her line, 2,568-2,638 t "
    "(Bel §3.2.5's 2,475-2,543 tons of 35 cu ft with plank and appendages at WL1, and the slice to "
    "the Channel line at 16.0 tons an inch: Bel-D §2.1), within Bel's H1 band, 2,490-2,900 t. The "
    "Audacious 2,821 t (Steel 1805 p. 212).",
    "gm_m": "4 ft 5 7/10 in: the Bombay Castle's, a Slade 74 of like size, 'certainly stiff "
    "enough' (Steel 1805 p. 141, page image; Bel §3.2.5); KM about 7.8 m above K (measured, ±0.2 "
    "m).",
    "clr_x_m": "Tuned against the helm's truths (6 and 17; Bel-D §9, the second knob) with her "
    "rig whole, at her step 5. Her start, 5.5 m, the measured centroid of the plane the file "
    "counts (to K, no rudder: 0.46-0.57 m abaft the mid-perpendicular, Bel §3.2.6) with the 64's "
    "lead at her stage A, 11.8% of her waterline, ahead of it (judgement), took her aback getting "
    "under way from rest in truth 17's form. Brought aft to the most weather helm that form holds "
    "in 15 and 16 kn, as the 64's (judgement: the Bellona's 'weatherly helm', Lavery 1985 p. 9, "
    "Table 2). Measured, old beside new, in docs/dev/TuningNotes.md, and held by her tests.",
    "lateral_area_m2": "3,503 sq ft below WL1 to K (measured, Bel §3.2.6) and the slice to the "
    "Channel line; the rudder left out, as the frigate's and the 64's.",
    "hull_speed_kn": "No period figure: judgement within 11.5-13.0 (Bel-D §9, the first knob), "
    "toward the owner's first goal of about 11 kn best (answer 14). Kept at her step 5: her best "
    "in 25 kn is that goal, no band asks more, and no end of the band closes the close-hauled gap "
    "against the Bellona's reports (Lavery 1985 p. 9, Table 2), which is the physics' (the lead's "
    "answer (12)).",
    "deck_height_m": "Her upper deck at the middle, the mean of its drawn top and middle lines, "
    "10.77 and 10.52 ft above WL1 (measured, Bel §3.3; task 8: the depth in hold lands between "
    "them), 10.37 ft above her water: the uppermost continuous deck, D18 (a), the datum of every "
    "spar height and every sail's corners (Bel-D §2.3).",
    "rudder": "104.8 sq ft and 21.6 ft below WL1 (measured, Bel §3.2.6), with the slice over its "
    "3.4-ft breadth at the line; 35 degrees and 3 deg/s the frigate-36's (judgement).",
}


# ---------------------------------------------------------------------------
# The ports' half-breadths and the decks at the side
# ---------------------------------------------------------------------------


def _station_hb(xs_, z_ft):
    """A traced section's half-breadth moulded at `z_ft` above WL1, above its trace by the
    tumblehome (judgement)."""
    row = BODY_PLAN_FT[xs_]
    top_z, top_hb = row[-1]
    if z_ft > top_z:
        return top_hb - TUMBLEHOME_PER_FT * (z_ft - top_z)
    return interp(row, z_ft)


def stern_x_ft(z_ft):
    """The stern's after edge at `z_ft` above WL1, feet from AP (`STERN_FT`, task 1)."""
    return interp(sorted((z, x) for x, z in STERN_FT if z is not None), z_ft)


def body_plan_hb(x_ft, z_ft):
    """The side's half-breadth moulded at `x_ft` from AP and `z_ft` above WL1 on the traced
    sections (`BODY_PLAN_FT`): straight between the two either side in x, along each trace in z.
    Abaft the aftmost traced station and above the wing transom's ends, straight between that
    station and the stern's outline seen from aft (`STERN_OUTLINE_FT`) at the stern's after edge
    for that height (judgement: the side counter timbers taken at the stern's middle line); else
    beyond the traced stations the end two's carried on (judgement)."""
    xs = sorted(BODY_PLAN_FT)
    if x_ft < xs[0] and z_ft > WING_TRANSOM_FT[1]:
        xs_ = stern_x_ft(z_ft)
        h0, h1 = interp(STERN_OUTLINE_FT, z_ft), _station_hb(xs[0], z_ft)
        if x_ft <= xs_:
            return h0
        return h0 + (h1 - h0) * (x_ft - xs_) / (xs[0] - xs_)
    if x_ft <= xs[0] or x_ft >= xs[-1]:
        a, b = (xs[0], xs[1]) if x_ft <= xs[0] else (xs[-2], xs[-1])
    else:
        a, b = next((a, b) for a, b in zip(xs, xs[1:], strict=False) if a <= x_ft <= b)
    ha, hb = _station_hb(a, z_ft), _station_hb(b, z_ft)
    return ha + (hb - ha) * (x_ft - a) / (b - a)


def traced(x_ft, z_ft):
    """Whether a port's half-breadth at `x_ft` and `z_ft` is read inside the traced band, its
    stations either side both traced to its height, and so measured; else it is judgement."""
    xs = sorted(BODY_PLAN_FT)
    if not xs[0] <= x_ft <= xs[-1]:
        return False
    a, b = next((a, b) for a, b in zip(xs, xs[1:], strict=False) if a <= x_ft <= b)
    return z_ft <= min(BODY_PLAN_FT[a][-1][0], BODY_PLAN_FT[b][-1][0])


def port_hb(x_ft, z_ft):
    """A port's half-breadth outside the plank at its sill, feet."""
    return body_plan_hb(x_ft, z_ft) + PLANK_FT


def poop_middle_ft(x_ft):
    """The poop deck at the middle line at `x_ft`, feet above WL1 (task 5)."""
    return interp(POOP_MIDDLE_LINE_FT, x_ft)


def rail_ft(x_ft):
    """The top of the side at `x_ft`, feet above WL1."""
    return interp(RAIL_FT, x_ft)


def deck_ft(word, x_ft):
    """A deck at `x_ft`, feet above WL1: the poop's at the side, the rest at the middle line."""
    if word == "roundhouse":
        return poop_middle_ft(x_ft) - POOP_ROUND_UP_FT
    return interp(DECKS_FT[word], x_ft)


def deck_worked_ft(x_ft):
    """The deck she is worked from at `x_ft`, feet above WL1: the poop's middle line over its
    extent, else the quarterdeck's or the forecastle's over theirs, else the upper deck (the
    waist)."""
    if POOP_MIDDLE_LINE_FT[0][0] <= x_ft <= POOP_MIDDLE_LINE_FT[-1][0]:
        return poop_middle_ft(x_ft)
    for word in ("quarterdeck", "forecastle"):
        pts = DECKS_FT[word]
        if pts[0][0] <= x_ft <= pts[-1][0]:
            return interp(pts, x_ft)
    return interp(DECKS_FT["upper"], x_ft)


def over_the_rail_sill_ft(x_ft):
    """A gun place over the rail: its sill 2 in under the rail (the 64's convention, judgement)."""
    return rail_ft(x_ft) - OVER_THE_RAIL_M / FT


def port_triples():
    """Her ports by deck, (ft from AP, sill ft above WL1, half-breadth ft outside the plank), and
    the triples measured: the lower and upper decks' read on the traced body plan at their sills
    (task 4), but where a port stands abaft the traced stations (judgement); the quarterdeck's and
    the forecastle's above the trace, and the gun places over the rail, judgement."""
    out, measured = {}, []
    for word, ports in (("lower", LOWER_PORTS_FT), ("upper", UPPER_PORTS_FT)):
        out[word] = [(x, sill, port_hb(x, sill)) for x, sill in ports]
        measured += [(word, round(x_m(x), 2)) for x, sill in ports if traced(x, sill)]
    out["quarterdeck"] = [(x, s, port_hb(x, s)) for x, s in QUARTERDECK_PORTS_FT]
    fc = []
    for x in sorted((FORECASTLE_CARRONADE_X_FT, *FORECASTLE_PORTS_X_FT)):
        if x == FORECASTLE_CARRONADE_X_FT:
            sill = over_the_rail_sill_ft(x)
        else:
            sill = deck_ft("forecastle", x) + FORECASTLE_SILL_ABOVE_DECK_FT
        fc.append((x, sill, port_hb(x, sill)))
    out["forecastle"] = fc
    out["roundhouse"] = [
        (x, over_the_rail_sill_ft(x), port_hb(x, over_the_rail_sill_ft(x)))
        for x in POOP_PLACES_X_FT
    ]
    return out, measured


PORT_NOTES = {
    "lower": "The gun deck's fourteen a side, centres and sills measured on ZAZ1357 at full "
    "resolution (both readers, Bel §3.1, §3.3); the half-breadth at each sill read on the body "
    "plan's sections traced either side of the port (task 4), with 4 1/2 in of plank; the "
    "aftmost's carried on from the two aftmost traced sections (judgement)",
    "upper": "The upper deck's fourteen a side at the red altered places taken as fitted, sills "
    "measured (Bel §3.3; the seventh's place tentative); the half-breadth read on the traced "
    "sections as the lower deck's, with the plank; the aftmost's taken between the aftmost traced "
    "section and the stern's outline seen from aft (judgement)",
    "quarterdeck": "Seven a side at ZAZ1357's places (Q1-Q2 black, Q3-Q7 red), sills measured (Bel "
    "§3.3); Dragon's plan puts them 0.46-0.65 ft further forward. Q1 and Q2 under the poop, in the "
    "captain's cabin and the coach. The half-breadth the traced sections' top carried up by the "
    "dead flat's tumblehome (judgement), with the plank; Q1's, abaft the traced sections, taken "
    "toward the stern's outline seen from aft (judgement)",
    "forecastle": "Two a side at 139 and 153 ft on Dragon's plan (Bel §3.3, one reader; task 6, "
    "two a side read again at full resolution), their sills the forecastle deck and 1 ft "
    "(judgement); and the 1795 fit's carronade place at 128 ft (Bel-D §5.1, judgement), 2 in under "
    "the rail, the gun firing over it. The half-breadths as the quarterdeck's (judgement)",
    "roundhouse": "The 1795 fit's three carronade places a side on the poop at 4, 12 and 20 ft "
    "from AP (Bel-D §5.1, judgement): gun places over the rail, not ports, no source drawing one "
    "(Bel-D §3.3; the lead's answer (14)), each 2 in under the rail; the half-breadths as the "
    "quarterdeck's (judgement)",
}


# ---------------------------------------------------------------------------
# The file's hull block
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


def waterline_at(x_ft, i):
    """Waterline `i` (0 for WL1) at `x_ft` from AP, half-breadth moulded, straight between the
    stations Bel §3.2.3 reads it at; None beyond them or where it is not resolved."""
    pts = [(x, row[i]) for x, row in WATERLINES.items() if row[i] is not None]
    if i == 0:
        pts = list(WL1_HALF_BREADTHS)
    if not pts[0][0] <= x_ft <= pts[-1][0]:
        return None
    return interp(pts, x_ft)


# WL1 at station W (156.46 ft), where the half-breadth plan's WL1 is not read (Bel §3.2.3 gives it
# to 155 ft): the body plan's crossing there, the trace's seed (task 4), 15.0 ft moulded (the
# checker's WL1 falling 0.66 ft a foot from 154 to 155 ft gives 15.1, the check).
WL1_AT_W_FT = (156.46, 15.0)


def breadth_stations():
    """`breadth_m`'s stations, (ft from AP, WL1's half-breadth moulded): the traced frame stations,
    so that no station of the water's and the rail's half-breadths alone stands between two traced
    ones, and abaft them Bel §3.2.3's 10-ft station."""
    out = [(10.0, interp(WL1_HALF_BREADTHS, 10.0))]
    for x in sorted(BODY_PLAN_FT):
        hb = waterline_at(x, 0)
        out.append((x, WL1_AT_W_FT[1] if hb is None or x == WL1_AT_W_FT[0] else hb))
    return out


def section_points():
    """Her sourced section points (ft from AP, ft above WL1, half-breadth moulded), each station
    low to high: at each traced frame station (task 4) WL1 to WL5 read there off Bel §3.2.3's
    waterlines, straight between the stations it gives them at, and the traced section above the
    water, a foot under the top of the side at the most; beyond the traced stations the waterlines
    at Bel §3.2.3's own stations, 10 and 160 ft. So every station that carries points carries the
    side above the water as traced, and no station of the waterlines alone stands between two traced
    ones, where the rule would draw the side in their place."""
    out = []
    xs = sorted(BODY_PLAN_FT)
    for x, row in WATERLINES.items():
        if xs[0] <= x <= xs[-1]:
            continue
        out += sorted(
            ((x, -WL_BELOW_WL1_FT[i], hb) for i, hb in enumerate(row) if hb is not None),
            key=lambda q: q[1],
        )
    for x, row in BODY_PLAN_FT.items():
        below = [(x, -WL_BELOW_WL1_FT[i], waterline_at(x, i)) for i in range(5)]
        top = rail_ft(x) - 1.0
        out += sorted((q for q in below if q[2] is not None), key=lambda q: q[1])
        out += [(x, z, hb) for z, hb in row if z <= top]
    return sorted(out, key=lambda q: (q[0], q[1]))


def main_breadth_points():
    """The widest point of each traced section above the water (ft from AP, ft above WL1,
    half-breadth moulded), the lowest of equal widths (task 3): the trace begins 2 ft above WL1,
    so that where the dead flat runs below it the main breadth is taken at the trace's lowest
    point (Bel §3.2.4: the dead flat to 4.6 ft above WL1 at the middle; judgement on the trace)."""
    out = []
    for x, row in BODY_PLAN_FT.items():
        z, hb = max(row, key=lambda q: (q[1], -q[0]))
        out.append((x, z, hb))
    return out


def rail_hb_ft(x_ft):
    """The half-breadth at the top of the side outside the plank, feet: the traced side carried up
    to the rail by the tumblehome; abaft the traced stations toward the stern's outline, forward
    of them the end two's carried on toward the stem (`body_plan_hb`; judgement)."""
    return port_hb(x_ft, rail_ft(x_ft))


def sill_parallel(band, ports, at=81.0):
    """A band (ft above WL1, low and high) at `at` ft from AP carried along the length parallel to a
    deck's sills (`ports`, (x, sill)), at stations 10 ft apart from 10 to 160 ft (judgement)."""
    lo0, hi0 = band
    s0 = interp(ports, at)
    out = []
    for x in range(10, 161, 10):
        d = interp(ports, float(x)) - s0
        out.append((float(x), lo0 + d, hi0 + d))
    return out


def check_hull(hull, triples):
    """Bel-D §1.5's checks on her hull, raised before any file is written: the lowest lower-deck
    sill
    1.57 ± 0.01 m above her water and its triple's half-breadth within 0.03 m of 7.04 m; the
    displacement within Bel's H1 band, 2,490-2,900 t."""
    lowest = min(triples["lower"], key=lambda t: t[1])
    sill = round(z_m(lowest[1]), 2)
    if abs(sill - 1.57) > 0.01 + 1e-9:
        raise ValueError(
            f"her lowest lower-deck sill stands {sill:.2f} m above her water, not 1.57."
        )
    hb = round(lowest[2] * FT, 2)
    if abs(hb - 7.04) > 0.03 + 1e-9:
        raise ValueError(
            f"her lowest lower-deck sill's half-breadth is {hb:.2f} m, not within 0.03 m of 7.04."
        )
    t = hull["displacement_kg"] / 1000.0
    if not 2490.0 <= t <= 2900.0:
        raise ValueError(f"her displacement, {t:.0f} t, is outside Bel's H1 band, 2,490-2,900 t.")


def hull_block():
    """Her hull dict with its profile as the last key (Build-Ships.md §5.1), and its notes."""
    hull = dict(HULL)
    hull["deck_height_m"] = DATUM
    rudder = hull.pop("rudder")
    hull["rudder"] = rudder
    notes = dict(HULL_NOTES)

    def k(x_ft):
        return [x_m(x_ft), z_m(k_ft(x_ft))]

    def keel_top(x_ft):
        return [x_m(x_ft), z_m(keel_top_ft(x_ft))]

    stem = [keel_top(x) if z is None else pt(x, z) for x, z in STEM_FT]
    stern = [k(x) if z is None else pt(x, z) for x, z in STERN_FT]
    head = [k(x) if z is None else pt(x, z) for x, z in HEAD_FT]
    rail = [pt(x, z) for x, z in RAIL_FT]
    breadth = [[x_m(x), (hb + PLANK_FT) * FT, rail_hb_ft(x) * FT] for x, hb in breadth_stations()]
    wales = [
        [x_m(x), z_m(lo), z_m(hi)]
        for x, lo, hi in sill_parallel(MAIN_WALE_AT_81_FT, LOWER_PORTS_FT)
    ]
    channel_wales = [
        [x_m(x), z_m(lo), z_m(hi)]
        for x, lo, hi in sill_parallel(CHANNEL_WALE_MID_FT, UPPER_PORTS_FT, at=MIDSHIPS_FT)
    ]
    mid_keel = keel_top_ft(MIDSHIPS_FT)
    section = [[z_m(h + mid_keel), (hb + PLANK_FT) * FT] for h, hb in SECTION_FT]
    decks = {word: [pt(x, z) for x, z in pts] for word, pts in DECKS_FT.items()}
    decks["roundhouse"] = [pt(x, z - POOP_ROUND_UP_FT) for x, z in POOP_MIDDLE_LINE_FT]
    triples, measured = port_triples()
    ports = {word: [[x_m(x), z_m(s), hb * FT] for x, s, hb in t] for word, t in triples.items()}
    sizes = {word: [w * FT, d * FT] for word, (w, d) in PORT_SIZE_FT.items()}
    sections = [[x_m(x), z_m(z), (hb + PLANK_FT) * FT] for x, z, hb in section_points()]
    breadth_line = [pt(x, z) + [(hb + PLANK_FT) * FT] for x, z, hb in main_breadth_points()]
    hull["profile"] = g.hull_profile(
        rail,
        breadth,
        keel=[k(x) for x in KEEL_FT],
        stem=stem,
        stern=stern,
        wales=wales,
        section=section,
        decks=decks,
        ports=ports,
        port_size=sizes,
        head=head,
        breadth_line=breadth_line,
        sections=sections,
        channel_wales=channel_wales,
    )
    notes.update(PROFILE_NOTES)
    for word, text in PORT_NOTES.items():
        notes[f"profile.ports_m.{word}"] = text + "."
    middle, knuckle, end_hb = WING_TRANSOM_FT
    form = {
        "fullness": [1.0, 1.0],
        "stern": {
            "type": "square",
            "knuckle_z_m": z_m(knuckle),
            "transom_hb_m": [
                (STERN_OUTLINE_FT[-1][1] + PLANK_FT) * FT,
                (end_hb + PLANK_FT) * FT,
            ],
            "round_up_m": (middle - knuckle) * FT,
            "galleries_m": [
                [x_m(aft), x_m(fore), z_m(low), z_m(high)]
                for aft, fore, low, high in QUARTER_GALLERIES_FT
            ],
            "lights_m": [[z_m(low), z_m(high), n, hb * FT] for low, high, n, hb in STERN_LIGHTS_FT],
        },
        "head": "figure",
    }
    drawn = REPORT.setdefault("hull", [])
    drawn.clear()
    REPORT["gaps"] = g.hull_form(
        hull, form=form, marks=MARKS, measured=tuple(measured), report=drawn
    )
    REPORT["measured"] = measured
    REPORT["triples"] = triples
    check_hull(hull, triples)
    return hull, notes


# Each line's rung (Build-Ships.md §5.0 principles 3 and 4), its weakest point named.
MARKS = {
    "rail_m": "judged",  # straight across the gallery; the poop's rail at its deck's middle line
    "breadth_m": "judged",  # the rail's half-breadths above the traced band
    "keel_m": "sourced",
    "stem_m": "judged",  # behind the head, from 7 ft above WL1 to the stem head
    "stern_m": "sourced",
    "wales_m": "judged",  # along the length
    "section_m": "sourced",
    "decks_m": "judged",  # the forecastle carried on its slope; the poop's at the side by rule
    "ports_m": "judged",  # the quarterdeck's, the forecastle's and the places over the rail
    "port_size_m": "judged",  # the forecastle's and the roundhouse's
    "head_m": "sourced",
    "breadth_line_m": "judged",  # the trace's lowest point where the dead flat runs below it
    "sections_m": "judged",  # the waterlines carried straight between Bel's stations
    "channel_wales_m": "judged",  # along the length
    "form.fullness": "judged",  # the default rule beyond the stations sections_m carries
    "form.stern": "sourced",
    "form.stern.knuckle_z_m": "sourced",
    "form.stern.transom_hb_m": "sourced",
    "form.stern.round_up_m": "sourced",
    "form.stern.galleries_m": "sourced",
    "form.stern.lights_m": "judged",  # the spread by D1's proportions
    "form.head": "sourced",
}

PROFILE_NOTES = {
    "profile": "Her side, decks and ports (Bel-D §3; Build-Ships.md §5.1): x forward of the "
    "mid-perpendicular, z above her water, the Channel line, metres; every point measured on her "
    "class's draughts but where its line's note says judgement.",
    "profile.rail_m": "The top of the side, from the taffrail's crown 13 ft abaft AP to the "
    "beakhead bulkhead about 12.5 ft before the foremast, measured on ZAZ1357 by columns (within "
    "0.2 ft of Bel §3.3 at every station forward of the drift): the poop's rail, raised with its "
    "red deck where that stands above the black rail (judgement), to the poop's breast at 36.75 "
    "ft; the black rail to the drift's scroll at 40.2 ft; the quarterdeck's to its breast at 72-79 "
    "ft; the waist; the forecastle's from its breast at about 120.5 ft. Taken straight across the "
    "quarter gallery's finishing, 8.5 ft abaft to 3.7 ft before AP (judgement). Judged at its "
    "weakest: from 8 ft abaft AP to 6 ft before it straight across, and from 6 to 36.75 ft the "
    "poop's rail at its red deck's middle line, 0.2-1.0 ft over the black rail ZAZ1357 draws there "
    "(24.82 against 24.20 ft above WL1 at 28 ft; 24.58 against 23.56 at 36 ft).",
    "profile.breadth_m": "By station: the half-breadth at WL1 (measured, Bel §3.2.3, the checker's "
    "WL1), with 4 1/2 in of plank; at the top of the side the traced sections' carried up to the "
    "rail by the dead flat's tumblehome (task 4), and beyond them carried on (judgement): the "
    "half-breadth plan's top-timber line was not traced.",
    "profile.keel_m": "K, the strip's top border, from the post's heel to the main keel's square "
    "fore end, 157.7 ft (Bel §3.2.1, §3.2.6).",
    "profile.stem_m": "The stem's fore edge, the foremost of the stem proper's two lines on "
    "ZAZ1357, abaft the knee and the gripe, traced from its foot on the keel's top at 157.7 ft "
    "through WL1 at 169.0 ft to 7 ft above it (task 2), then carried on its rake behind the head "
    "to the stem head under the bowsprit, 170.13 ft and 16.25 ft above WL1, where both sheets "
    "begin the bowsprit's lower edge (judgement between).",
    "profile.stern_m": "The post's after face (0.37 ft before AP at the heel, 0.8 ft abaft it at "
    "WL1, raking 3.4 degrees), the counter from the wing transom 7.42 ft above WL1 at the middle "
    "line, and the stern's after edge to the taffrail's crown, 13.05 ft abaft AP and 30.25 ft "
    "above WL1: traced on ZAZ1357 by rows (task 1; ±0.2 ft; the quarter gallery and the quarter "
    "piece left out).",
    "profile.wales_m": "The main wale: at 81 ft from 0.32 ft below WL1 to 3.95 ft above it (the "
    "checker, Bel §3.3), carried along the length parallel to the lower deck's sills (judgement: "
    "not traced along the length).",
    "profile.section_m": "The midship section, plank on: the floor, the bilge and the dead flat "
    "traced on ZAZ1357's body plan (the research's trace, Bel §3.2.4: the floor rising 0.3-0.4 ft "
    "from 3 to 8 ft out, 3.4-4.6 degrees, the research's '2-3 degrees' a slip), "
    "its tumblehome to 28 ft the checker's, and above it to the waist rail traced here (task 3).",
    "profile.decks_m": "Each deck at the middle line, the surface the mean of the top and middle "
    "of its three red lines (measured, Bel §3.3; task 8), over its extent; the forecastle's "
    "measured at 125 and 140 ft and carried on its slope (judgement). The poop, the roundhouse "
    "deck, at the side: its middle line measured on ZAZ1359 and ZAZ1357 in red within 0.15 ft "
    "(task 5), from the stern timbers to its breast beam at 36.75 ft, less Steel's 10-in round-up "
    "of a 74's roundhouse beams (Steel 1805, the tables of dimensions, OCR l. 39678: rule). The "
    "period called it the poop (Bel-D §3.5). ZAZ1359's green beam carrying it to 39.0 ft is "
    "recorded, not taken (judgement).",
    "profile.port_size_m": "Width by depth: the lower 3 ft 4 3/4 in by 2 ft 8 1/2 in, the upper 2 "
    "ft 9 in by 2 ft 7 1/2 in, the quarterdeck 2 ft 7 in by 2 ft 4 in (measured, Bel §3.3); the "
    "forecastle's and the poop's as the quarterdeck's (judgement, as the 64's), no port being "
    "drawn on the poop: its triples are gun places over the rail, 2 in under it, which a port's "
    "depth against the side there shows (Build-Ships.md §6's postscript). The quarterdeck's two "
    "foremost, Q6 and Q7, are drawn cut to the rail's lower edge, about 2 ft 3 in and 1 ft 11 in "
    "deep (measured on ZAZ1357), under the one size filed, so that the viewer draws No. 29, Q7's "
    "gun, over the rail.",
    "profile.head_m": "The knee of the head's fore edge, the gripe's, the cutwater's and the "
    "knee's, from K at the main keel's square fore end to the head's top under the figure, 22 ft "
    "above WL1 at 182.5 ft: traced on ZAZ1357 by rows (task 2), within 0.1 ft of Bel §3.2.6's two "
    "readers below the water; Lavery 1985 D7, her class's head from the side, the check by eye.",
    "profile.breadth_line_m": "The main breadth by traced station, the widest of each section "
    "traced on ZAZ1357's body plan and its height, the lowest of equal widths; where the dead flat "
    "runs below the trace, which begins 2 ft above WL1, the trace's lowest point (task 3, "
    "judgement on the trace), with the plank. The half-breadth plan's main-breadth line was not "
    "traced (Bel §3.2.3 reads it at 40, 140 and 150 ft: 21.82, 21.75, 19.43). Judged at its "
    "weakest: 21 of its 26 points at the trace's lowest point, 2 ft above WL1.",
    "profile.sections_m": "WL1 to WL5 at each traced frame station, read off Bel §3.2.3's "
    "waterlines (measured at 10 to 160 ft from AP: ±0.15 ft, ±0.5 at the ends; straight between "
    "its stations, judgement), each waterline 3.77 ft below the last, and Bel §3.2.3's own 10 and "
    "160 ft beyond the traced stations; above the water the body plan's sections traced at the "
    "frame stations from 14.85 to 156.46 ft (task 4), a foot under the top of the side at the "
    "most; each with 4 1/2 in of plank. Judged at its weakest: the waterlines carried straight "
    "between Bel §3.2.3's stations to the frame stations.",
    "profile.channel_wales_m": "The channel wale, between the lower port tops and the upper sills: "
    "8.6-11.2 ft above WL1 at midships (the researcher, Bel §3.3), carried along the length "
    "parallel to the upper deck's sills (judgement: not traced).",
    "profile.form.stern": "Square. The knuckle, the transom's foot where the side closes to it, "
    "the wing transom at its ends, 7.15 ft above WL1, rounded up 0.28 ft to 7.42 at the middle "
    "line, 15.0 ft out; the transom's half-breadths 15.0 ft at the knuckle and 9.9 ft at the "
    "taffrail's side, on the side counter timbers' outline seen from aft, each with the plank: "
    "traced on ZAZ1357's body plan (task 1), the sheer's tuck rail ending at 7.3-7.6 ft the check. "
    "Two tiers of quarter gallery (ZAZ1357, Bel §3.3; Lavery 1985 D2). Two bands of eight stern "
    "lights, the wardroom's and the screen bulkhead's (Lavery 1985 D1, her class's stern, read on "
    "the owner's photograph), at the galleries' tiers, spread by D1's proportions (judgement on "
    "them).",
    "profile.form.fullness": "The default rule, [1, 1], abaft 10 ft and forward of 160 ft, "
    "beyond the stations sections_m carries (Bel-D §3.6; judgement).",
    "profile.form.head": "A figure on the knee of the head: Lavery 1985 D7, D8 and D11 draw her "
    "class's head and its figurehead (the owner's photographs); carving and paint stay in words.",
    "profile.marks": "Each line's rung (Build-Ships.md §5.0 principles 3 and 4): sourced, measured "
    "on her class's draughts (ZAZ1357, ZAZ1359) or drawn by Lavery from them; judged, a judgement "
    "at its weakest point, which the line's note names.",
}


# ---------------------------------------------------------------------------
# The rig's geometry
# ---------------------------------------------------------------------------


def fmt_ft(v):
    """Feet as the period writes them, feet and inches to the nearest inch."""
    feet = math.floor(v + 1e-9)
    inches = round((v - feet) * 12.0)
    if inches == 12:
        feet, inches = feet + 1, 0
    return f"{feet} ft {inches} in" if inches else f"{feet} ft"


def head_ft(length_ft, in_per_yard):
    """A mast's head by Steel's rule, so many inches to every yard of its length, feet."""
    return length_ft / 3.0 * in_per_yard / 12.0


def mast_geometry():
    """Each mast's geometry in feet above her datum, keyed as the frigate's (Bel-D §4.1, §4.2): the
    lower masthead (`above`) from the heel on its step and Table 10's length; the yards' heights by
    the frigate's rules (the lower yards 2 ft under the hounds, the topsail yards at the topmast's
    hounds, the topgallants under the stop, the royals a foot under the long pole's head)."""
    datum = DATUM / FT
    geom, mast_x, rake = {}, {}, {}
    for name, (x, heel, r) in MASTS.items():
        L = SPARS_FT["mast"][name]
        head = head_ft(L, HEAD_IN_PER_YARD["mast"][name])
        above = (keel_top_ft(x) + heel + L - CHANNEL_FT) - datum
        T = SPARS_FT["topmast"][name]
        t_head = head_ft(T, HEAD_IN_PER_YARD["topmast"][name])
        t_hoist = T - head
        G = SPARS_FT["topgallant_mast"][name]
        g_square = head_ft(G, HEAD_IN_PER_YARD["topgallant_mast"][name])
        to_stop = G - g_square
        pole = LONG_POLE_OF_STOP * to_stop
        g_hoist = to_stop - t_head
        tg_hounds = HOUNDS_OF_STOP * g_square
        geom[name] = {
            "length": L,
            "above": above,
            "head": head,
            "t_len": T,
            "t_head": t_head,
            "t_hoist": t_hoist,
            "g_len": G,
            "g_hoist": g_hoist,
            "r_hoist": pole,
            "yard": SPARS_FT["yard"][name],
            "topsail_yard": SPARS_FT["topsail_yard"][name],
            "tg_yard": SPARS_FT["tg_yard"][name],
            "royal_yard": SPARS_FT["royal_yard"][name],
            "yard_h": above - head - 2.0,
            "topsail_h": above + t_hoist - t_head,
            "tg_h": above + t_hoist + g_hoist - tg_hounds,
            "royal_h": above + t_hoist + g_hoist + pole - 1.0,
        }
        mast_x[name] = round(x_m(x), 2)
        rake[name] = r
    return geom, mast_x, rake


def sail_of(mast, level):
    """A square sail's id by its mast and level: `main.course`, `fore.topsail`."""
    return f"{mast}.{level}"


def mizzen_lift_in(rope_scale):
    """The lifts of the mizzen's lower yards, inches: a course's lift, the mizzen's share of the
    frigate's rope, scaled with hers (judgement)."""
    rope = g.FRIGATE_ROPE["course"]["lift"] * g.FRIGATE_MAST_ROPE_FACTOR["mizzen"]
    return g.quarter(rope * rope_scale)


def under_the_run(line, aft_x, fore_x, room):
    """The points of `line` (a deck, (ft from AP, ft above WL1)) under a run from `aft_x` to
    `fore_x` (metres, the file's x), each (x, z above her water, room), the line's height at both
    ends of the run among them: what a sail's foot or a boom passing over the deck must stand above
    by `room`."""
    pts = [(x_m(xf), z_m(z)) for xf, z in line]
    lo, hi = pts[0][0], pts[-1][0]
    out = [(x, z, room) for x, z in pts if aft_x <= x <= fore_x]
    for x in (aft_x, fore_x):
        if lo <= x <= hi:
            xf = x / FT + MIDSHIPS_FT
            out.append((x, z_m(interp(line, xf)), room))
    return out


# ---------------------------------------------------------------------------
# The mizen course and the driver (Bel-D §4.5, §4.6)
# ---------------------------------------------------------------------------


def course_on(tack_z, mast_x_m, rake_deg):
    """The mizen course cut at the mast with its tack at `tack_z` (`mizen_yard.course`)."""
    return mizen_yard.course(
        mast_x=mast_x_m,
        rake_deg=rake_deg,
        frame_z=DATUM,
        tack_z=tack_z,
        steel=STEEL_MIZEN_COURSE,
        yard_length_m=SPARS_FT["mizen_yard"] * FT,
    )


def foot_clear(crs):
    """What the course's level foot stands over her poop's middle line, at the least, over its
    run."""
    tack, _throat, _peak, clew = crs["corners"]
    under = under_the_run(POOP_MIDDLE_LINE_FT, clew[0], tack[0], 0.0)
    return min(tack[1] - z for _x, z, _r in under)


def mizen_course_cut(mast_x_m, rake_deg):
    """Her mizen course cut at the mast (`mizen_yard.course`; Ext §3.4) from Steel's table IV: its
    tack `MIZEN_TACK_ABOVE_DECK_FT` above her poop's middle line at the mast, to the centimetre
    above;
    (x, z above her water) in metres, with its area and centre. Raises `ValueError` where the foot
    would not then clear the poop at the middle line (the clew check: Bel-D §1.5). The design's
    reading (9 ft above the quarterdeck) and Steel's words (6 ft 6 in above the deck the mast stands
    through) are cut beside it for the report."""
    x_ft = MASTS["mizzen"][0]
    deck = z_m(poop_middle_ft(x_ft))
    tack_z = math.ceil((deck + MIZEN_TACK_ABOVE_DECK_FT * FT) * 100.0 - 1e-9) / 100.0
    crs = course_on(tack_z, mast_x_m, rake_deg)
    clear = foot_clear(crs)
    if clear <= 0.0:
        raise ValueError(
            f"her mizen course's foot stands {clear:.2f} m over her poop's middle line: its clew "
            "must clear it (the clew check: Bel-D §1.5)."
        )
    others = {}
    quarterdeck = z_m(interp(DECKS_FT["quarterdeck"], x_ft))
    for words, z in (
        ("9 ft above the quarterdeck (Bel-D §4.5 as written)", quarterdeck + 9.0 * FT),
        (
            "6 ft 6 in above the poop (Steel's words from the deck the mast stands through)",
            deck + 6.5 * FT,
        ),
    ):
        z = math.ceil(z * 100.0 - 1e-9) / 100.0
        alt = course_on(z, mast_x_m, rake_deg)
        others[words] = {
            "tack": z,
            "clear": foot_clear(alt),
            "area": alt["area"],
            "centre": alt["centre"],
            "cut": alt,
        }
    return {
        "corners": crs["corners"],
        "area": round(crs["area"]),
        "x": round(crs["x"], 1),
        "centre": round(crs["centre"], 1),
        "deck": deck,
        "quarterdeck": quarterdeck,
        "cut": crs,
        "clear": clear,
        "others": others,
    }


def driver_cut(crs, mast_x_m, rake_deg):
    """Steel's driver on her course `crs` (`mizen_yard.driver`; Ext §17.2), its boom's jaws the
    least that give the boom `HEAD_ROOM_FT`'s first figure of head room over her poop's middle line
    over its run and keep its after leech within Steel's band, the head room going to the second
    figure only where a check breaks; clear over her taffrail's crown. Raises `ValueError` where
    none
    holds (Bel-D §4.6: then a report to the lead and `DRIVER = False`)."""
    boom = DRIVER_BOOM_FT * FT
    mast_at = mizen_yard.mast_line(mast_x_m, rake_deg, DATUM)
    taff_x, taff_z = RAIL_FT[0]
    taffrail = (x_m(taff_x), z_m(taff_z))
    kw = {
        "mast_x": mast_x_m,
        "rake_deg": rake_deg,
        "frame_z": DATUM,
        "steel": STEEL_DRIVER,
        "course_steel": STEEL_MIZEN_COURSE,
    }
    tried = []
    for room_ft in HEAD_ROOM_FT:
        room = room_ft * FT
        fore = mast_at(crs["corners"][0][1])
        under = under_the_run(POOP_MIDDLE_LINE_FT, fore - boom, fore, room)
        jaws, why = mizen_yard.least_jaws(crs, under=under, **kw)
        jaws = math.ceil(jaws * 100.0 - 1e-9) / 100.0
        try:
            d = mizen_yard.driver(
                crs,
                jaws_z=jaws,
                boom_length_m=boom,
                driver_yard_m=DRIVER_YARD_FT * FT,
                under=under,
                over=[taffrail],
                **kw,
            )
        except ValueError as e:
            tried.append(f"{room_ft:g} ft: {e}")
            continue
        d["head_room_ft"], d["set_by"], d["under"], d["taffrail"] = room_ft, why, under, taffrail
        return d
    raise ValueError(
        "her driver cannot be cut on her course within the head room the lead allows over her poop "
        "(Ext §17.2; the lead's answer (13)): " + "; ".join(tried)
    )


def mizen_course(b, mz, rope_scale):
    """Her mizen course on her mizen yard (Bel-D §4.5; Ext §3.4): the lateen cut at the mast on the
    whole yard, a `lateen_yard` slung at its truss with its fore part bare, and the lines of Ext
    §3.4
    (`mizen_yard.COURSE_LINES`). Returns the course's id."""
    if MIZEN_COURSE != "gated":
        raise ValueError(f"MIZEN_COURSE is {MIZEN_COURSE!r}: she has no stage A, only 'gated'.")
    corners = [[round(x, 2), round(z - DATUM, 2)] for x, z in mz["corners"]]
    throat = mz["corners"][1]
    canvas = g.FRIGATE_CANVAS["mizzen.spanker"]
    load = [(mz["area"], mz["centre"], "gaff")]
    yard = b.spar(
        "mizzen.yard",
        "lateen_yard",
        on="mizzen.mast",
        length_m=g.ft(SPARS_FT["mizen_yard"]),
        height_m=round(throat[1] - DATUM, 2),
        rating_kn=g.design_kn(load, g.DESIGN_WIND_KN["gaff"]),
        note=f"the mizen yard, {fmt_ft(SPARS_FT['mizen_yard'])} by 15 3/8 in (Lavery 1985 p. 19, "
        "Table 10, Dragon's: read (owner's book); Steel's 84 ft 0 in, p. 49), a lateen yard slung "
        "at its truss with its lifts and derrick, its fore part bare (Lavery 1985 I31-I32; Ext "
        "§3.4): height_m its truss, the course's throat. Not braced: it has vangs in place of "
        "braces and bowlines at its heel, its sail trimmed by the sheet (Ext §3.3; Falconer 1780, "
        "VANGS and BRACE).",
    )
    sail = b.sail(
        "mizzen.course",
        "lateen",
        yard=yard,
        mast="mizzen.mast",
        cut_at_mast=True,
        area_m2=mz["area"],
        reef_bands=1,
        x_m=mz["x"],
        centre_height_m=mz["centre"],
        canvas_no=canvas[0],
        cloth_rating_kn=g.cloth(mz["area"], canvas[0]),
        corners_m=corners,
        note="mizen course, a lateen cut at the mast (answers 2 and 3 as revised, Bel §13.5; Ext "
        "§3.4), the four-sided loose-footed sail the owner rules, on the gaff's curve and trim in "
        "the physics (Ext §3.1): Steel's table IV, the 74 (16 cloths at the head, 17 at the foot, "
        "its fore leech 11 yards and its after leech 21; Bel §5.6), 22 1/2 in a cloth, its luff "
        "laced to the mast, its head along the yard to the peak, its foot level and loose "
        "(tools/ships/mizen_yard.py); corners [tack, throat, peak, clew]. Its tack 9 ft above her "
        "poop at the mast, so that its throat stands where Lavery's I32, her class's mizen course "
        "and yard, draws it, about 42 ft above the deck the mast stands through (Ext §2, §17.1), "
        "Steel's 11-yard fore leech below it (Bel-D §4.5). Plainly: Bel-D §4.5 first named that "
        "deck her quarterdeck, her poop then judged to end abaft the mizen, the slip (the lead's "
        "ruling (2) of 2026-11-10): her poop is measured over the mizen to 36.75 ft from AP, and "
        "I32 draws its deck running unbroken from the taffrail past the mast, so the 9 ft are "
        "taken above the poop, as ruled. Steel's 'within 6 or 7 feet of the deck' (OCR l. "
        "11441-11442) is the general rule beside it. One reef band a fifth up its mast leech "
        "(Steel, OCR l. 11448)." + g.canvas_note(canvas),
    )
    # the lines of Ext §3.4: the 64's sizes (Steel's 64 list, read in part) scaled from her rope to
    # hers (judgement: Steel's 74 list, vol. II p. 37, held as a page image, is not read here to its
    # sizes)
    lift = mizzen_lift_in(rope_scale)
    scale = rope_scale / RUN_64_ROPE_SCALE
    sizes = {
        "yard.jeers": (g.quarter(4.5 * rope_scale), 3),
        "yard.derrick": (g.quarter(4.0 * scale), 4),
        "yard.lift": (lift, 1),
        "yard.vang": (g.quarter(4.0 * scale), 1),
        "yard.bowline": (g.quarter(3.0 * scale), 1),
        "course.sheet": (g.quarter(5.0 * rope_scale), 2),
        "course.tack": (g.quarter(3.5 * rope_scale), 1),
    }
    notes = {
        "yard.jeers": "the mizen yard's jeers at its truss (Steel 1794 vol. II p. 37, the 74's "
        "list; Ext §3.4); the frigate's spanker throat halyard's size and purchase scaled by her "
        "rope (judgement).",
        "yard.derrick": "Steel's derrick between the slings and the peak (Steel 1794 vol. II p. "
        "37, the 74's list; vol. I p. 207), a lift of the yard (Ext §3.4): the 64's 4 in in double "
        "blocks scaled by her rope against the 64's (judgement).",
        "yard.vang": "the vang pendants, the 64's 4 in scaled by her rope against the 64's "
        "(judgement), one line a side with its falls.",
        "yard.lift": "the mizen yard's lifts (Lavery 1985 I31-I32), as the crossjack's "
        "(judgement): every yard's lifts are carried (the owner's answer, Build-Ships.md §19.1 "
        "item 7).",
        "yard.bowline": "the bowlines at the yard's heel (Steel 1794 vol. II p. 37, the 74's list; "
        "Lavery 1985 I32), filed as guys of the yard, a bowline being a sail's line in the engine "
        "(Ext §3.4); the 64's 3 in scaled by her rope against the 64's (judgement).",
        "course.sheet": "the course's one sheet, to the taffrail (Ext §3.4); the frigate's spanker "
        "sheet's size and purchase scaled by her rope (judgement).",
        "course.tack": "the course's tack, forward of the mast (Ext §3.4); the frigate's spanker "
        "outhaul's size scaled by her rope (judgement).",
    }
    of = {"yard": yard, "course": sail}
    for suffix, cls, owner, sided in mizen_yard.COURSE_LINES:
        size, parts = sizes[suffix]
        lid = f"mizzen.{suffix}"
        rating = g.rope_kn(size, parts)
        if sided:
            b.sided(lid, cls, of[owner], rating=rating, note=notes.get(suffix))
        else:
            b.line(
                lid,
                cls,
                of[owner],
                rating=rating,
                note=notes.get(suffix),
                parts=parts if cls == "sheet" else None,
            )
    return sail


# The 64's rope scale (her plain sail over the frigate's, the root: the generator's report for
# sixty-four.yaml, 1.08), against which her mizen yard's and her driver's lines read from the 64's
# list are scaled (judgement).
RUN_64_ROPE_SCALE = 1.08


def mizen_driver(b, d, rope_scale):
    """Steel's driver boomsail and its boom (`DRIVER`; Ext §17.2), filed after the course so that
    the
    yard's sail stays the course, in the course's place and in the sail room. Returns its id."""
    corners = [[round(x, 2), round(z - DATUM, 2)] for x, z in d["corners"]]
    area = round(d["area"])
    centre = round(d["centre"], 1)
    jaws = d["boom"]["jaws_z"]
    load = [(area, centre, "gaff")]
    set_by = (
        "and the least that also keeps the driver's after leech within Steel's band, two to four "
        "yards deeper than the course's (Steel 1794 vol. I, DRIVER BOOMSAIL; Ext §17.2), "
        if d["set_by"] == "after leech"
        else ""
    )
    boom = b.spar(
        "mizzen.boom",
        "boom",
        on="mizzen.mast",
        length_m=g.ft(DRIVER_BOOM_FT),
        height_m=round(jaws - DATUM, 2),
        horse_m=round(0.5 * HULL["beam_m"], 1),
        rigged_out=d["boom"]["rigged_out"],
        rating_kn=g.design_kn(load, g.DESIGN_WIND_KN["gaff"]),
        note=f"driver boom {fmt_ft(DRIVER_BOOM_FT)} by 12 3/4 in, her main topsail yard's length "
        "and her fore topsail yard's diameter (Steel 1794 vol. I p. 40: 'Driver boom, the same "
        "length as the main-topsail-yard'; Bel-D §4.6; Ext's 70 ft 0 in was Steel's column's "
        "yard). Rigged in on the booms while the driver is in the sail room, and out with the sail "
        "only while it is bent (Ext §17.11). Level, its jaws on the mast at the least height that "
        f"gives it {d['head_room_ft']:g} ft of head room over her poop's middle line, where it "
        "passes (Bel-D §4.6; task 5; the lead's answer (13): the head room first, to 5 ft), "
        f"{set_by}clear over her taffrail's crown. Steel's topping lifts and guy pendants (OCR l. "
        "23103-23121) are not filed as lines, as the frigate files none on her spanker boom. "
        "horse_m " + g.HORSE_NOTE,
    )
    canvas = (5, f"{g.STEEL_SM}, 'Driver': No. 5 or 6 (OCR l. 13819), the first taken")
    jaws_by = (
        "the jaws set by the after leech's band over the boom's head room (the boom's note)"
        if d["set_by"] == "after leech"
        else "the jaws set by the boom's head room (the boom's note)"
    )
    sail = b.sail(
        "mizzen.driver",
        "lateen",
        yard="mizzen.yard",
        mast="mizzen.mast",
        boom=boom,
        cut_at_mast=True,
        bent=False,
        in_place_of="mizzen.course",
        area_m2=area,
        reef_bands=0,
        x_m=round(d["x"], 1),
        centre_height_m=centre,
        canvas_no=canvas[0],
        cloth_rating_kn=g.cloth(area, canvas[0]),
        corners_m=corners,
        note="Steel's driver boomsail (Steel 1794 vol. I, DRIVER BOOMSAIL, OCR l. 13816-13843; Ext "
        "§17; the owner's choice of 2026-10-28), 'occasionally hoisted ... in light fair winds': a "
        "lateen cut at the mast on the mizen yard and its boom, in the sail room, bent in the "
        "mizen course's place by the shift of the one for the other (Ext §17.3: the period bent it "
        "beside the course; one after sail bent is the game's choice). Steel's table IV, the 74: "
        "25 1/2 cloths at the head and 32 1/2 at the foot, its fore leech 11 yards and its after "
        "leech 24 (Bel §5.6), 22 1/2 in a cloth, unscaled (Bel-D §4.6); its throat the course's, "
        "its tack at the boom's jaws, its head along the mizen yard's line and on past the yard's "
        "peak on Steel's driver yard (her fore topgallant yard's 40 ft 0 in, p. 40; not filed, it "
        "went aloft with the sail: Ext §17.2), its "
        f"foot along the boom; corners [tack, throat, peak, clew]; {jaws_by}. Vanguard, an "
        "Arrogant, 'Set driver' at the Nile (NRS vol. 2 p. 53). No reef band: Steel names none."
        + g.canvas_note(canvas),
    )
    # Steel's lines (vol. I, THE DRIVER or SPANKER SAIL, OCR l. 24523-24545; Ext §17.2): his 74's
    # list gives the driver halyards 3 1/2 in (vol. II p. 37: Bel §5.4); the rest the 64's sizes
    # scaled by her rope against the 64's (judgement)
    scale = rope_scale / RUN_64_ROPE_SCALE
    steel_in = {
        "driver.halyard": (
            3.5,
            1,
            "Steel's two pair of 3 1/2 in for the 74 (vol. II p. 37: Bel §5.4)",
        ),
        "driver.tack": (
            g.quarter(3.0 * scale),
            1,
            "'set tight with a luff-tackle' to the boom's throat",
        ),
        "driver.sheet": (
            g.quarter(3.0 * scale),
            2,
            "rove through the boom's end to the clew, its luff tackle to the taffrail, doing the "
            "outhauler's work",
        ),
        "driver.downhaul": (
            g.quarter(2.0 * scale),
            1,
            "through a block at the middle of the driver yard",
        ),
    }
    for suffix, cls, _owner, _sided in mizen_yard.DRIVER_LINES:
        size, parts, words = steel_in[suffix]
        b.line(
            f"mizzen.{suffix}",
            cls,
            sail,
            rating=g.rope_kn(size, parts),
            parts=parts if cls == "sheet" else None,
            note=f"the driver's {cls} (Steel 1794 vol. I, THE DRIVER or SPANKER SAIL; Ext §17.2): "
            f"{words}; the 64's sizes scaled by her rope where Steel's 74 is not read (judgement).",
        )
    return sail


# ---------------------------------------------------------------------------
# The head (Bel-D §4.7)
# ---------------------------------------------------------------------------


def triangle_on_stay(low, high, foot, leech):
    """A triangular staysail on its stay as her headsails are cut from Steel's table IV (judgement
    on
    Steel's figures, as the 64's): its tack at `low` on the stay, its luff up the stay toward
    `high`,
    its foot and leech, metres, square to each other at the clew, the clew below and abaft the stay;
    cut to the stay where its luff is longer, Steel's proportions kept (the spars rule:
    Build-Ships.md §19.1 item 5). Returns the corners [tack, peak, clew], the foot and the leech as
    cut, and the share of Steel's sides kept."""
    luff = math.hypot(foot, leech)
    run = math.hypot(high[0] - low[0], high[1] - low[1])
    fit = min(1.0, run / luff)
    foot, leech, luff = foot * fit, leech * fit, luff * fit
    ux, uz = (high[0] - low[0]) / run, (high[1] - low[1]) / run
    nx, nz = (-uz, ux) if ux > 0 else (uz, -ux)
    if nz > 0:
        nx, nz = -nx, -nz
    peak = (low[0] + luff * ux, low[1] + luff * uz)
    ca, sa = foot / luff, leech / luff
    clew = (low[0] + foot * (ca * ux + sa * nx), low[1] + foot * (ca * uz + sa * nz))
    return [low, peak, clew], foot, leech, fit


def head_geometry(geom, mast_x, rake):
    """The bowsprit, the jib-boom and the headsails' triangles, metres above her water (task 7): the
    bowsprit's root on the stem head, steeved `BOWSPRIT_STEEVE_DEG`, its outboard part Table 10's
    length less its part inboard of the stem head from its heel; the jib-boom along it. The fore
    stay
    to a collar half way out the bowsprit's outboard part, the fore topmast stay to its end and the
    jib's stay to the jib-boom's (the 64's leads; judgement). Each headsail a triangle on its stay
    from its tack at the stay's foot, Steel's leech and foot square at the clew."""
    stem_x, stem_z = STEM_HEAD_FT
    root = (x_m(stem_x), z_m(stem_z))
    c, s = math.cos(math.radians(BOWSPRIT_STEEVE_DEG)), math.sin(math.radians(BOWSPRIT_STEEVE_DEG))
    inboard = (stem_x - BOWSPRIT_HEEL_FT) / c
    outboard = SPARS_FT["bowsprit"] - inboard
    jib_out = JIB_BOOM_OUTBOARD * SPARS_FT["jib_boom"]

    def along(d_ft):
        return (root[0] + d_ft * c * FT, root[1] + d_ft * s * FT)

    tip = along(outboard)
    jib_tip = along(outboard + jib_out)
    fore = geom["fore"]

    def at_mast(h_ft):
        z = DATUM + h_ft * FT
        return (mast_x["fore"] - math.tan(math.radians(rake["fore"])) * (z - DATUM), z)

    stays = {
        "fore.staysail": (
            "fore.stay",
            along(outboard / 2.0),
            at_mast(fore["above"] - fore["head"]),
        ),
        "fore.topmast_staysail": (
            "fore.topmast.stay",
            tip,
            at_mast(fore["above"] + fore["t_hoist"] - fore["t_head"]),
        ),
        "jib": ("jib.stay", jib_tip, at_mast(fore["above"] + fore["t_hoist"] - fore["t_head"])),
    }
    sails = {}
    for sid, (stay, low, high) in stays.items():
        foot_cl, leech_yd = STEEL_HEADSAILS[sid]
        corners, foot, leech, fit = triangle_on_stay(
            low, high, foot_cl * CLOTH_IN_SAIL_FT * FT, 3.0 * leech_yd * FT
        )
        sails[sid] = {
            "stay": stay,
            "corners": corners,
            "area": round(0.5 * foot * leech),
            "x": round(sum(q[0] for q in corners) / 3.0, 1),
            "centre": round(sum(q[1] for q in corners) / 3.0, 1),
            "foot_cl": foot_cl,
            "leech_yd": leech_yd,
            "fit": fit,
            "table": round(0.5 * foot * leech / (fit * fit)),
        }
    return {
        "root": root,
        "outboard": outboard,
        "inboard": inboard,
        "tip": tip,
        "jib_out": jib_out,
        "jib_tip": jib_tip,
        "sails": sails,
    }


HEAD_CANVAS = {
    "fore.staysail": (2, f"{g.STEEL_SM}, 'Fore staysail': No. 1 to 3, the middle taken (Ind §5)"),
    "fore.topmast_staysail": g.FRIGATE_CANVAS["fore.topmast_staysail"],
    "jib": g.FRIGATE_CANVAS["jib"],
}


def write_head(b, head, rope_scale):
    """The bowsprit, the jib-boom, their stays and the headsails (Bel-D §4.7). Returns the
    headsails'
    ids, the fore staysail first."""
    loads = {sid: (h["area"], h["centre"], "jibheaded") for sid, h in head["sails"].items()}
    bowsprit = b.spar(
        "bowsprit",
        "bowsprit",
        x_m=round(head["root"][0], 2),
        length_m=g.ft(head["outboard"]),
        height_m=round(head["tip"][1] - DATUM, 1),
        rating_kn=g.design_kn(list(loads.values()), g.DESIGN_WIND_KN["lower"]),
        note=f"bowsprit {fmt_ft(SPARS_FT['bowsprit'])} by 34 1/8 in (Lavery 1985 p. 19, Table 10, "
        f"Dragon's: read (owner's book)), steeved {BOWSPRIT_STEEVE_DEG:g} deg (task 7: measured on "
        "ZAZ1357's drawn edges, 31.5-31.8; ZAZ1359 31.8-32.3), rooted on the stem head, where both "
        "sheets begin its lower edge and the viewer draws its heel: x_m its root, length_m its "
        "part outboard of the stem head from its heel at the step before the foremast (ZAZ1359, "
        "155.4 ft from AP), height_m its end above the datum. The spritsail yard slung under it "
        "and the sprit-topsail yard under the jib-boom (D8 (b); Ext §4.1; "
        "tools/ships/spritsail_yards.py).",
    )
    jib_boom = b.spar(
        "jib_boom",
        "jib_boom",
        on=bowsprit,
        length_m=g.ft(head["jib_out"]),
        height_m=round(head["jib_tip"][1] - DATUM, 1),
        rating_kn=g.design_kn([loads["jib"]], g.DESIGN_WIND_KN["jib_boom"]),
        note=f"jib-boom {fmt_ft(SPARS_FT['jib_boom'])} by 14 1/8 in (Table 10's 'flying jib boom' "
        "row taken as the jib-boom, Bel-D §4.1, judgement), 7/12 of it outboard along the "
        "bowsprit's steeve (Luce, the frigate's rule; judgement).",
    )
    for lid, of, size, text in (
        (
            "fore.topmast.stay",
            "fore.topmast",
            7.5,
            "to the bowsprit's end; the fore topmast staysail sets on it",
        ),
        (
            "jib.stay",
            "fore.topmast",
            5.0,
            "from the fore topmast head to the jib-boom's end: the jib sets on it (Steel's was set "
            "flying on its traveller)",
        ),
        ("bobstay", bowsprit, 12.0, None),
        ("martingale", jib_boom, 5.0, None),
    ):
        size = g.quarter(size * rope_scale)
        b.line(
            lid,
            "stay",
            of,
            rating=g.rope_kn(size),
            note=f"the frigate-36's scaled by her rope (judgement){'; ' + text if text else ''}.",
        )
    out = []
    for sid, h in head["sails"].items():
        canvas = HEAD_CANVAS[sid]
        s = b.sail(
            sid,
            "jibheaded",
            stay=h["stay"],
            area_m2=h["area"],
            x_m=h["x"],
            centre_height_m=h["centre"],
            canvas_no=canvas[0],
            cloth_rating_kn=g.cloth(h["area"], canvas[0]),
            corners_m=[[round(x, 2), round(z - DATUM, 2)] for x, z in h["corners"]],
            note=f"{sid.replace('_', ' ').replace('.', ' ')}, a triangle (Steel's table IV, the "
            f"74: {h['foot_cl']:g} cloths in the foot, {h['leech_yd']:g} yards in the leech; Bel "
            "§5.6): its tack at its stay's foot, its luff up the stay, foot and leech square at "
            "the clew (judgement on Steel's figures, as the 64's)"
            + (
                ", cut to her stay, short of Steel's in each side, the spars ruling (the owner's "
                "answer, Build-Ships.md §19.1 item 5)"
                if h["fit"] < 1.0
                else ""
            )
            + "; corners [tack, peak, clew]."
            + g.canvas_note(canvas),
        )
        size = g.quarter(3.5 * rope_scale)
        b.line(f"{sid}.halyard", "halyard", s, rating=g.rope_kn(size, 2))
        b.sided(f"{sid}.sheet", "sheet", s, rating=g.rope_kn(size))
        b.line(f"{sid}.downhaul", "downhaul", s, rating=g.rope_kn(g.quarter(size * 0.8)))
        out.append(s)
    return out


def head_yards(b, head, rope_scale):
    """The yards under the bowsprit (D8 (b); Bel-D §4.7; Ext §4.1; `spritsail_yards.cut`), on the
    line
    her bowsprit and jib-boom have: Table 10's spritsail and sprit-topsail yards with Steel's sprit
    course and sprit topsail; their lines `square_sail_lines` at her fore topsail's and fore
    topgallant's sizes, and the guys of Lavery I28; no halyard to the spritsail yard, which hangs in
    slings (Ext §4.1). Returns the sails' ids; with `BOWSPRIT_YARDS = False`, none."""
    if not BOWSPRIT_YARDS:
        return []
    cut = spritsail_yards.cut(
        root=head["root"],
        steeve_deg=BOWSPRIT_STEEVE_DEG,
        bowsprit_out_m=head["outboard"] * FT,
        jib_out_m=head["jib_out"] * FT,
        spritsail=SPRITSAIL,
        sprit_topsail=SPRIT_TOPSAIL,
        station=SPRITSAIL_STATION,
        hang=SPRITSAIL_HANG_M,
        topsail_hang=SPRIT_TOPSAIL_HANG_M,
    )
    REPORT["sprit"] = cut
    upper, lower = cut["sprit_topsail.yard"], cut["spritsail.yard"]
    along = math.hypot(
        round(upper["x"], 2) - round(lower["x"], 2),
        round(upper["z"] - DATUM, 2) - round(lower["z"] - DATUM, 2),
    )
    REPORT["sprit_drawn"] = (
        along,
        *spritsail_yards.drawn_by_slant(
            round(cut["sprit_topsail"]["area"]),
            g.ft(SPRIT_TOPSAIL["yard_m"] / FT),
            g.ft(SPRITSAIL["yard_m"] / FT),
            along,
        ),
    )
    braced = (
        f"braces {SPRIT_BRACE_LIMIT_DEG} deg from square, from the yard's arms to the fore top and "
        "the fore stay (Steel 1794 vol. I pp. 196-197; Lavery 1985 I30; judgement, as the engine's "
        "fixture); kept out of the file's yard groups, braced by name, by 'brace sharp up' and "
        "'trim sails' (Ext §4.2 as built)"
    )
    rope = g.FRIGATE_ROPE
    factor = g.FRIGATE_MAST_ROPE_FACTOR["fore"] * rope_scale

    def write_one(sid, yard_id, on, by, row, canvas, reef, hoisting, words_yard, words_sail):
        y, s = cut[yard_id], cut[sid]
        area = round(s["area"])
        centre = round(s["centre"], 1)
        yard = b.spar(
            yard_id,
            "yard",
            on=on,
            x_m=round(y["x"], 2),
            length_m=g.ft(row["yard_m"] / FT),
            height_m=round(y["z"] - DATUM, 2),
            brace_limit_deg=SPRIT_BRACE_LIMIT_DEG,
            rating_kn=g.design_kn([(area, centre, "square")], g.DESIGN_WIND_KN[by]),
            note=f"{words_yard} x_m and height_m its slings (Ext §4.1); {braced}.",
        )
        sail = b.sail(
            sid,
            "square",
            yard=yard,
            area_m2=area,
            reef_bands=reef,
            x_m=round(s["x"], 1),
            centre_height_m=centre,
            canvas_no=canvas[0],
            cloth_rating_kn=g.cloth(area, canvas[0]),
            note=f"{words_sail}{g.canvas_note(canvas)}",
        )
        sizes = {cls: g.quarter(c * factor) for cls, c in rope[by].items()}
        g.square_sail_lines(b, sail, yard, sizes, hoisting=hoisting, reef=(reef > 0))
        b.sided(
            f"{yard}.guy",
            "guy",
            yard,
            rating=g.rope_kn(sizes["brace"]),
            note=f"the {yard_id.split('.')[0].replace('_', ' ')} yard's guys (Lavery 1985 I28), "
            "the braces' size (judgement).",
        )
        return sail

    return [
        write_one(
            "spritsail",
            "spritsail.yard",
            "bowsprit",
            "topsail",
            SPRITSAIL,
            SPRITSAIL_CANVAS,
            2,
            False,
            "spritsail yard 61 ft 6 in by 12 3/4 in (Lavery 1985 p. 19, Table 10, the bowsprit's "
            "row: Bel §13.4; Steel's 62 ft 0 in, Ext §4.1's), slung under the bowsprit near the "
            "cap (Steel 1794 vol. I pp. 196-197; Lavery 1985 I30), "
            f"{SPRITSAIL_STATION:g} of the way out its outboard part and {SPRITSAIL_HANG_M:g} m "
            "under its line (judgement, both, as the 64's); no halyard, it hanging in slings (Ext "
            "§4.1);",
            "spritsail (the sprit course): Steel's table IV, the 74 (29 cloths, 8 yards deep; Bel "
            "§5.6), 22 1/2 in a cloth, hanging from its yard, square, its foot clear of the water "
            "at no heel (tools/ships/spritsail_yards.py). Two diagonal reef bands in Steel, filed "
            "and reefed as a square sail's (Ext §4.1). Out of plain sail, so the polar never sets "
            "it (Ext §4.1). At the Nile she wore clear of L'Orient 'setting her spritsail' (James "
            "vol. 2 p. 180, read (OCR)).",
        ),
        write_one(
            "sprit_topsail",
            "sprit_topsail.yard",
            "jib_boom",
            "topgallant",
            SPRIT_TOPSAIL,
            SPRIT_TOPSAIL_CANVAS,
            0,
            True,
            "sprit-topsail yard 40 ft 0 in by 8 1/2 in (Lavery 1985 p. 19, Table 10, the "
            "jib-boom's row: Bel §13.4; Steel's 40 ft 6 in), hung under the jib-boom by its parral "
            "(Steel p. 197), where its sail's depth from the spritsail yard is Steel's, near the "
            "boom's end (judgement on "
            f"Steel's figures; {SPRIT_TOPSAIL_HANG_M:g} m under its line, judgement); its halyard "
            "stands for the traveller's outhauler (Falconer 1780, SPRITSAIL-TOPSAIL; Lavery 1985 "
            "I29);",
            "sprit topsail: Steel's table IV, the 74 (18 1/2 cloths at the head, 29 1/2 at the "
            "foot, 10 yards deep; Bel §5.6), 22 1/2 in a cloth, its head on its yard and its foot "
            "spread on the spritsail yard's arms (Steel, SPRITSAIL TOPSAIL), the sail's plane "
            "sloping forward from the one to the other (tools/ships/spritsail_yards.py). No reef "
            "band (Lever 1808, OCR l. 7354-7356). Out of plain sail (Ext §4.1).",
        ),
    ]


# ---------------------------------------------------------------------------
# The staysails between the masts (Bel-D §4.4)
# ---------------------------------------------------------------------------


def steels_staysail_words(sid, area):
    """The words a staysail between the masts adds to its note: Steel's table IV figure for the 74
    and the band Bel-D §4.4 holds it in, raised before any file is written if the cut falls outside
    it."""
    row, _figures, steel, band = STEEL_BETWEEN[sid]
    gap = area / steel - 1.0
    if abs(gap) > band:
        raise ValueError(
            f"her {sid} is cut to {area} m2, {gap:+.0%} of Steel's {steel:.0f} for a 74, outside "
            f"Bel-D §4.4's ±{band:.0%}."
        )
    return (
        f" Steel's table IV, the 74 ({row}; Bel §5.6): about {steel:.0f} m2, the cut within Bel-D "
        f"§4.4's ±{band:.0%}."
    )


def between_the_masts(b, geom, mast_x, rake):
    """The staysails between the masts (Bel-D §4.4), the 64's pattern on her figures: the main
    staysail a triangle on its own stay; the main topmast staysail by Steel's rules on her spars;
    the
    middle, the main topgallant, the mizen and the mizen topmast staysails cut to Steel's table IV,
    as
    the owner chose for the 64 (2026-10-29: Indf §17); no mizen topgallant staysail. Every height
    above her datum. Returns the sails, the main mast's first."""
    canvas = g.FRIGATE_CANVAS

    def mx(name, z):
        return mast_x[name] - math.tan(math.radians(rake[name])) * z

    def head(gm, level):
        lift = (gm["t_hoist"] if level >= 1 else 0) + (gm["g_hoist"] if level >= 2 else 0)
        return g.ft(gm["above"] + lift)

    def at(name, level):
        z = head(geom[name], level)
        return (mx(name, z), z)

    def before_the_top(name, level=0):
        gm = geom[name]
        yard = gm["yard"] if level == 0 else gm["topsail_yard"]
        return mx(name, head(gm, level)) + g.TOP_REACH_OF_YARD * g.ft(yard)

    def steel(sid):
        head_cl, foot_cl, bunt_yd, leech_yd = STEEL_BETWEEN[sid][1]
        cloths = 0.5 * (head_cl + foot_cl)
        return g.ft(3.0 * leech_yd), g.ft(cloths * CLOTH_IN_SAIL_FT), g.ft(3.0 * bunt_yd), cloths

    def from_the_table(sid, stay, upper, lower, peak_x, rope_in, where):
        leech, foot, bunt, cloths = steel(sid)
        corners = g.stay_sail_cut(upper, lower, leech, peak_x=peak_x, foot=foot)
        g.staysail_from_cut(b, sid, stay, corners, DATUM, canvas[sid], rope_in, "")
        b.notes[sid] = (
            f"{sid.replace('_', ' ').replace('.', ' ')}, four-sided, square on the foot, cut to "
            "Steel's table IV, the 74, as the owner chose for the 64 (2026-10-29; Indf §17): the "
            f"table's after leech and foot ({cloths:g} cloths of 22 1/2 in, the head's and the "
            "foot's halved, as Steel's rule for the canvas squares them), the bunt as the stay "
            f"leaves it (the table's {bunt:.1f} m); {where}" + g.canvas_note(canvas[sid])
        )
        return sid

    out = []
    gm, gf = geom["main"], geom["fore"]
    main_top = before_the_top("main")
    stay = b.line(
        "main.staysail.stay",
        "stay",
        "main.mast",
        rating=g.rope_kn(9.0),
        note="the main staysail stay, from the main mast head to a luff round the foremast (Steel "
        "1794 vol. I, 'The main-staysail'); 9 in, judgement.",
    )
    (xu, zu), (xl, zl) = at("main", 0), (mx("fore", 1.0), 1.0)
    tack_z = 0.2 * g.ft(gm["above"])
    tack = (xu + (tack_z - zu) * (xl - xu) / (zl - zu), tack_z)
    _head_cl, foot_cl, _bunt_yd, leech_yd = STEEL_BETWEEN["main.staysail"][1]
    corners, _foot, _leech, _fit = triangle_on_stay(
        tack, (xu, zu), foot_cl * CLOTH_IN_SAIL_FT * FT, 3.0 * leech_yd * FT
    )
    sid = "main.staysail"
    g.staysail_from_cut(b, sid, stay, corners, DATUM, canvas[sid], 3.5, "")
    b.notes[sid] = (
        "main staysail, a triangle, cut to Steel's table IV, the 74, as the owner chose for the 64 "
        f"(2026-10-29; Indf §17): {foot_cl:g} cloths of 22 1/2 in in the foot and {leech_yd:g} "
        "yards in the leech, square at the clew, its luff up the stay from its tack, as her "
        "headsails are cut (judgement on Steel's figures); its tack at the stay over the boats on "
        "the booms (a fifth of the main mast's height above the deck, judgement), its peak before "
        "the main top; corners [tack, peak, clew]. 'This sail is seldom used in large vessels' "
        "(Steel)." + g.canvas_note(canvas[sid])
    )
    out.append(sid)
    # the main topmast staysail, the generator's rule on her spars: the leech 4 or 5 yards deeper
    # than the main topsail, its foot a cloth or two more than the leech's yards (Steel)
    leech_yd = (gm["topsail_h"] - gm["yard_h"]) / 3.0 + 4.5
    corners = g.stay_sail_cut(
        at("main", 1),
        at("fore", 0),
        g.ft(3.0 * leech_yd),
        peak_x=main_top,
        foot=g.ft((leech_yd + 1.5) * g.CLOTH_FT),
    )
    out.append(
        g.staysail_from_cut(
            b,
            "main.topmast_staysail",
            "main.topmast.stay",
            corners,
            DATUM,
            canvas["main.topmast_staysail"],
            3.0,
            "the leech 4 or 5 yards deeper than the main topsail, a cloth or two more in the foot "
            "than the leech's yards (Steel; the mean of each taken), the bunt as the stay leaves "
            "it (Steel: two-fifths of the leech), its peak before the main top.",
        )
    )
    mid_stay = b.line(
        "middle_staysail.stay",
        "stay",
        "main.topmast",
        rating=g.rope_kn(4.0),
        note="the middle staysail stay, from the main topmast head to a grommet round the fore "
        "topmast under the parral (Steel 1794 vol. I, 'The middle-staysail'), a third of the "
        "topmast's hoist above the fore cap (judgement); size judgement.",
    )
    low_z = g.ft(gf["above"] + 0.35 * gf["t_hoist"])
    out.append(
        from_the_table(
            "middle_staysail",
            mid_stay,
            at("main", 1),
            (mx("fore", low_z), low_z),
            main_top,
            2.5,
            "its peak before the main top (the generator's, judgement).",
        )
    )
    tg_stay = b.line(
        "main.topgallant.stay",
        "stay",
        "main.topgallant_mast",
        rating=g.rope_kn(3.5),
        note="the main topgallant stay, through a block at the fore topmast head and down to the "
        "fore top (Steel 1794 vol. I, 'The main-topgallant-stay'); 3.5 in, judgement; the main "
        "topgallant staysail sets on it.",
    )
    out.append(
        from_the_table(
            "main.topgallant_staysail",
            tg_stay,
            at("main", 2),
            at("fore", 1),
            before_the_top("main", 1),
            2.0,
            "its peak before the topmast cross-trees (the generator's, judgement).",
        )
    )
    mizen_top = before_the_top("mizzen")
    upper = at("mizzen", 0)
    leech, foot, bunt, _cloths = steel("mizzen.staysail")
    fall = (leech - bunt) / foot
    tan_main = math.tan(math.radians(rake["main"]))
    collar_z = (upper[1] - fall * (mast_x["main"] - upper[0])) / (1.0 - fall * tan_main)
    collar = (mx("main", collar_z), collar_z)
    stay = b.line(
        "mizzen.staysail.stay",
        "stay",
        "mizzen.mast",
        rating=g.rope_kn(6.0),
        note="the mizen staysail stay (Steel 1794 vol. I, 'The mizen-staysail': it clinches round "
        "the head of the mizen-mast and reeves through a collar lashed round the main-mast); 6 in, "
        "judgement; the collar where Steel's table IV bunt falls under its leech and foot "
        "(judgement), the staysail on the span above it.",
    )
    out.append(
        from_the_table(
            "mizzen.staysail",
            stay,
            upper,
            collar,
            mizen_top,
            3.0,
            "its peak before the mizen top (the generator's, judgement).",
        )
    )
    mts_stay = b.line(
        "mizzen.topmast.stay",
        "stay",
        "mizzen.topmast",
        rating=g.rope_kn(4.5),
        note="the mizen topmast stay, to a collar at the fore part of the main mast 'close up to "
        "the bibs' (Steel 1794 vol. I, 'The mizen topmast-stay'); 4.5 in, judgement; the mizen "
        "topmast staysail sets on it.",
    )
    bibs = g.ft(gm["above"] - gm["head"])
    out.append(
        from_the_table(
            "mizzen.topmast_staysail",
            mts_stay,
            at("mizzen", 1),
            (mx("main", bibs), bibs),
            mizen_top,
            3.0,
            "its peak before the mizen top (the generator's, judgement).",
        )
    )
    return out


# ---------------------------------------------------------------------------
# The studding sails, the storm canvas and the occasional sails (Bel-D §4.4, §4.8)
# ---------------------------------------------------------------------------


def studding_sails(b, geom, mast_x, rake, rope_scale):
    """The studding sails, the frigate-36's set on Steel's figures for a 74: the fore lower and the
    fore and main topmast and topgallant, a pair each, on booms by Steel's p. 40 rules on her yards;
    the topgallant studding sails as deep as the topgallants they spread. The lower boom at the fore
    channel, the topmast booms on the lower yard, the topgallant booms on the topsail yard. Returns
    the sails' ids."""
    channel_m = round(z_m(CHANNELS_FT["fore"][2]) - DATUM, 1)
    out = []
    for (name, level), (head_cl, foot_cl, depth_yd, boom_ft) in STUDDING.items():
        gm = geom[name]
        parent, hung, boom_h = {
            "lower": (f"{name}.yard", gm["yard_h"], channel_m),
            "topmast": (f"{name}.topsail.yard", gm["topsail_h"], g.ft(gm["yard_h"])),
            "topgallant": (f"{name}.topgallant.yard", gm["tg_h"], g.ft(gm["topsail_h"])),
        }[level]
        head_w, foot_w = head_cl * CLOTH_IN_SAIL_FT, foot_cl * CLOTH_IN_SAIL_FT
        if level == "topgallant":
            depth = gm["tg_h"] - gm["topsail_h"]
            how = (
                "as deep as the topgallant it spreads, cut to the spars as the topgallants are "
                f"(the owner's answer, Build-Ships.md §19.1 item 5); the table's {depth_yd:g} yards"
            )
        else:
            depth = 3.0 * depth_yd
            how = f"{depth_yd:g} yards deep"
        area = round((head_w + foot_w) / 2.0 * depth * FT * FT)
        drop = depth * (head_w + 2.0 * foot_w) / (3.0 * (head_w + foot_w))
        centre = round(DATUM + (hung - drop) * FT, 1)
        canvas = g.FRIGATE_CANVAS[f"{level} studding"]
        size = g.quarter({"lower": 3.0, "topmast": 2.5, "topgallant": 2.0}[level] * rope_scale)
        rule = {
            "lower": "five-ninths of the main yard), goose-necked at the fore channel (Luce 1884 "
            "p. 137), 16.8 ft above WL1 (Bel §3.3)",
            "topmast": "half the lower yard it is rigged on)",
            "topgallant": "half the topsail yard it is rigged on)",
        }[level]
        for side in g.SIDES:
            first = side == g.SIDES[0]
            boom = b.spar(
                f"{name}.{level}.studdingsail_boom.{side}",
                "studdingsail_boom",
                on=parent,
                side=side,
                length_m=g.ft(boom_ft),
                height_m=boom_h,
                rating_kn=g.design_kn([(area, centre, "studding")], g.DESIGN_WIND_KN["studding"]),
                note=(
                    f"{name} {level} studding-sail boom {fmt_ft(boom_ft)} (Steel 1794 vol. I p. "
                    f"40: {rule}; rated for its sail in {g.DESIGN_WIND_KN['studding']:.0f} kn."
                    if first
                    else None
                ),
            )
            sid = b.sail(
                f"{name}.{level}.studdingsail.{side}",
                "studding",
                boom=boom,
                yard=parent,
                side=side,
                area_m2=area,
                x_m=g.raked_x(mast_x[name], rake[name], centre, deck_m=DATUM),
                centre_height_m=centre,
                canvas_no=canvas[0],
                cloth_rating_kn=g.cloth(area, canvas[0]),
                note=(
                    f"{name} {level} studding sail: Steel's table IV, the 74 (Bel §5.6), "
                    f"{head_cl:g} cloths at the head and {foot_cl:g} at the foot, {how}; its head "
                    "on its yard at the yardarm of the sail it spreads." + g.canvas_note(canvas)
                    if first
                    else None
                ),
            )
            b.line(f"{sid}.halyard", "halyard", sid, rating=g.rope_kn(size))
            b.line(f"{sid}.tack", "tack", sid, rating=g.rope_kn(size))
            b.line(f"{sid}.sheet", "sheet", sid, rating=g.rope_kn(g.quarter(size * 0.8)))
            b.line(f"{sid}.downhaul", "downhaul", sid, rating=g.rope_kn(g.quarter(size * 0.7)))
            out.append(sid)
    return out


def storm_canvas(b, geom, mast_x, rake, bow, after_sail, rope_scale):
    """The storm canvas, the frigate-36's pattern on her figures (Bel-D §4.8), every sail in the
    sail
    room: the fore storm staysail on the fore stay, the mizzen storm staysail on the mizen stay, the
    storm mizzen on its own stay abaft the mizen mast, bent in place of the mizen course. Each fixed
    height taken above the deck she works it from (`deck_worked_ft`: her poop over its extent).
    Returns the sails' ids, the storm staysails first."""
    storm = g.FRIGATE_CANVAS["storm"]

    def deck_at(x):
        return z_m(deck_worked_ft(x / FT + MIDSHIPS_FT))

    def on_mast(name, z):
        return mast_x[name] - math.tan(math.radians(rake[name])) * (z - DATUM)

    def storm_sail(sid, stay, corners, words, **kw):
        area, cx, cz = g._quad_area_centroid(corners)
        area = round(area)
        return b.sail(
            sid,
            "jibheaded",
            stay=stay,
            area_m2=area,
            x_m=round(cx, 1),
            centre_height_m=round(cz, 1),
            canvas_no=storm[0],
            cloth_rating_kn=g.storm_cloth(area),
            bent=False,
            corners_m=[[round(x, 2), round(z - DATUM, 2)] for x, z in corners],
            note=f"{sid.replace('_', ' ').replace('.', ' ')}, {words}; in the sail room."
            + g.canvas_note(storm, storm=True),
            **kw,
        )

    fss = storm_sail(
        "fore.storm_staysail",
        "fore.stay",
        bow["sails"]["fore.staysail"]["corners"],
        "Steel's fore staysail cut as her working one is (table IV, the 74: 22 cloths in the foot, "
        "13 yards in the leech), of storm canvas, on the fore stay (Luce 1884 ch. X: 'The "
        "storm-staysails set on the respective lower-stays'); corners [tack, peak, clew]",
    )
    size = g.quarter(3.5 * rope_scale)
    b.line("fore.storm_staysail.halyard", "halyard", fss, rating=g.rope_kn(size, 2))
    b.sided("fore.storm_staysail.sheet", "sheet", fss, rating=g.rope_kn(size, 3))
    b.line(
        "fore.storm_staysail.downhaul",
        "downhaul",
        fss,
        rating=g.rope_kn(g.quarter(2.75 * rope_scale)),
    )
    gz = geom["mizzen"]
    collar_z = deck_at(mast_x["main"]) + MIZEN_STAY_COLLAR_FT * FT
    collar = (on_mast("main", collar_z), collar_z)
    top_z = DATUM + (gz["above"] - gz["head"]) * FT
    top = (on_mast("mizzen", top_z), top_z)
    f = STORM_STAYSAIL_HEAD_OF_STAY
    head = (collar[0] + f * (top[0] - collar[0]), collar[1] + f * (top[1] - collar[1]))
    clew = (head[0], deck_at(head[0]) + STORM_STAYSAIL_CLEW_FT * FT)
    mss = storm_sail(
        "mizzen.storm_staysail",
        "mizzen.stay",
        [collar, head, clew],
        "on the mizen stay (Luce 1884 ch. X): its tack at the stay's collar on the main mast, 12 "
        "ft above the quarterdeck (Steel, 'Mizen-stay'), its head 0.6 of the way up the stay, its "
        "clew under the head 7 ft above the deck she works it from there (Steel's mizen staysail; "
        "the frigate-36's, 0.6 judgement); corners [tack, peak, clew]",
    )
    size = g.quarter(3.0 * rope_scale)
    b.line("mizzen.storm_staysail.halyard", "halyard", mss, rating=g.rope_kn(size, 2))
    b.sided("mizzen.storm_staysail.sheet", "sheet", mss, rating=g.rope_kn(size, 3))
    b.line(
        "mizzen.storm_staysail.downhaul",
        "downhaul",
        mss,
        rating=g.rope_kn(g.quarter(2.5 * rope_scale)),
    )
    b.line(
        "storm_mizzen.stay",
        "stay",
        "mizzen.mast",
        rating=g.rope_kn(g.quarter(5.0 * rope_scale)),
        note="the storm mizzen's stay abaft the mizen mast, under its after trestle-tree (Luce "
        "1884 ch. X); the jib stay's, scaled by her rope (judgement).",
    )
    filed_tack = deck_at(mast_x["mizzen"]) + STORM_MIZZEN_TACK_FT * FT
    foot = STORM_MIZZEN_FOOT_OF_BOOM * DRIVER_BOOM_FT * FT
    rail = under_the_run(RAIL_FT, on_mast("mizzen", filed_tack) - foot, mast_x["mizzen"], 0.0)
    tack_z = max([filed_tack] + [z for _x, z, _r in rail])
    if tack_z > filed_tack:
        tack_z = math.ceil(tack_z * 100.0 - 1e-9) / 100.0
    luff = STORM_MIZZEN_LUFF_OF_RUN * (top_z - tack_z)
    tack = (on_mast("mizzen", tack_z), tack_z)
    peak = (on_mast("mizzen", tack_z + luff), tack_z + luff)
    sm = storm_sail(
        "storm_mizzen",
        "storm_mizzen.stay",
        [tack, peak, (tack[0] - foot, tack_z)],
        "triangular (Luce 1884 ch. X; Steel 1794 'Storm mizen'): its luff up its stay from a tack "
        "4 ft above her poop at the mast, or at her rail over the foot's run where that stands "
        "higher (judgement, as the 64's), 0.8 of the stay's run to the hounds; its foot towards "
        "the taffrail, 0.45 of the driver boom by Steel's rule (the main topsail yard's length, p. "
        "40), as the frigate-36's is of her spanker boom (judgement); bent in place of the mizen "
        "course; corners [tack, peak, clew]",
        in_place_of=after_sail,
    )
    b.line("storm_mizzen.halyard", "halyard", sm, rating=g.rope_kn(g.quarter(3.0 * rope_scale), 2))
    b.line(
        "storm_mizzen.sheet",
        "sheet",
        sm,
        rating=g.rope_kn(g.quarter(3.5 * rope_scale), 3),
        parts=3,
    )
    b.line("storm_mizzen.downhaul", "downhaul", sm, rating=g.rope_kn(g.quarter(2.5 * rope_scale)))
    return [fss, mss, sm]


def save_alls(b, mast_x, rope_scale):
    """A save-all under each fore lower studding-sail boom, the frigate-36's pattern (Luce 1884 ch.
    XXIII; Steel 1794 vol. I: 'Some ships have a water-sail'): its head along 0.6 of the boom, down
    from the boom at the fore channel to half a metre off the water (judgement); in the sail room.
    No
    ringtail: the boom carries the driver, and no source gives a 74's (Bel-D §4.8, judgement)."""
    boom_ft = STUDDING[("fore", "lower")][3]
    depth = z_m(CHANNELS_FT["fore"][2]) - 0.5
    area = round(SAVE_ALL_OF_BOOM * boom_ft * FT * depth)
    canvas = g.FRIGATE_CANVAS["save-all"]
    out = []
    for side in g.SIDES:
        sa = b.sail(
            f"fore.save_all.{side}",
            "studding",
            boom=f"fore.lower.studdingsail_boom.{side}",
            yard="fore.yard",
            side=side,
            area_m2=area,
            x_m=round(mast_x["fore"], 1),
            centre_height_m=round(0.5 + depth / 2.0, 1),
            canvas_no=canvas[0],
            cloth_rating_kn=g.cloth(area, canvas[0]),
            bent=False,
            note=(
                "save-all under the fore lower studding sail boom (Luce 1884): its head along 0.6 "
                "of the boom, down from the boom at the fore channel to half a metre off the water "
                "(the frigate-36's, judgement); in the sail room." + g.canvas_note(canvas)
                if side == g.SIDES[0]
                else None
            ),
        )
        size = g.quarter(2.0 * rope_scale)
        b.line(f"{sa}.halyard", "halyard", sa, rating=g.rope_kn(size))
        b.line(f"{sa}.tack", "tack", sa, rating=g.rope_kn(size))
        b.line(f"{sa}.sheet", "sheet", sa, rating=g.rope_kn(g.quarter(1.75 * rope_scale)))
        out.append(sa)
    return out


# ---------------------------------------------------------------------------
# The guns (Bel-D §5)
# ---------------------------------------------------------------------------

# Her three fits (Bel-D §5.1, decision 14; the names accepted by the lead, answer (9)) in the
# file's order, and the default, the owner's (answer 3: 1795-1805, 82 pieces).
FIT_1793 = "arrogant class 1793"
FIT_1795 = "arrogant class 1795"
FIT_1812 = "as the bellona 1812"
DEFAULT_FIT = FIT_1795
# Her guns' numbers (Bel-D §5.2; B7.d, on the lead's word, (3) of the answers to her §17.2): by
# deck, each deck's places from forward from No. 1, as the period numbered each deck (the
# Regulations 1808 printing, the Gunner, p. 215): the lower 1-14, the upper 1-14, the
# quarterdeck 1-7, the forecastle's two ports 1-2 and the 1795 carronade's place over its rail 3,
# the poop's three places 1-3; her armament's `numbering` says so, and each gun's id names its deck
# (`gun.lower.3.starboard`). A place keeps its number in every fit; a fit that leaves a place
# empty leaves a gap. Before B7.d she numbered on across her decks, the lower deck first (lower
# 1-14, upper 15-28, quarterdeck 29-35, forecastle 36-38, poop 39-41).
GUN_DECKS = ("lower", "upper", "quarterdeck", "forecastle", "roundhouse")
NUMBERING = "by deck"
# Bel-D §1.5's figures for each fit, raised on before her file is written: its pieces, and its
# broadside by 70's rule (one side's broadside guns and every chaser: combat/far.py), James's 781
# and 867 lb (vol. 1, Abstracts No. 1 and 3, page images) and the 1812 list's 938 (Bel-D §5.5).
FIT_FIGURES = {FIT_1793: (74, 781), FIT_1795: (82, 867), FIT_1812: (78, 938)}
# The Regulations' allowance for exercise counts her upper deck's 28 eighteen-pounders, a third
# in a ship of two decks (the Regulations 1806, the Gunner, Art. XXI: Bel-D §5.4).
UPPER_DECK_GUNS = 28
ARMAMENT_NOTE = (
    "The armament (spec M7 7; package 70; docs/design/Design-Ship-Bellerophon.md §5): the "
    "guns as parts of the graph by their place, in her three fits, each on its port of the hull's "
    "profile or its place over the rail to the centimetre, its deck named (Build-Ships.md §4.4); "
    "their weights by Adye 1804 (pp. 72, 155) and, where Adye gives no such pattern, Lavery 1985 "
    "Table 17; their crews by Falconer 1780 and Douglas 1829; the magazine's allowance by kind "
    "and calibre, the charges Table No. 29's. The degrees the sources allow beyond the three, "
    "for an editor to reason within (Bel-D §5.6), none of them a fit: on the quarterdeck and "
    "forecastle a long 9 or 12 in the wake of the shrouds and a 32-pounder carronade elsewhere, "
    "the long guns within four, at most six, of those established (the order of 17 March 1797, "
    "James vol. 2 pp. 119-120); on the poop none to six carronades; the two gun decks' 56 fixed. "
    "Numbered by deck, each deck's pairs from No. 1 forward as the period numbered each deck (the "
    "Regulations 1808 printing, the Gunner, p. 215), a pair keeping one number where the period "
    "numbered each gun, so her gun is said with its deck; the `numbering` below says so (Bel-D "
    "§5.2, B7.d). Every figure's source is in tools/ships/bellerophon.py."
)


def long_cwt(pounder, length, of_1812=False):
    """A long gun's weight, cwt, by her design's rule (Bel-D §5.3, judgement): its pattern's,
    Adye's where Adye gives it (1804 p. 155: `period.ADYE_LONG_GUN_CWT`), else Lavery's Table 17
    for its date (`period.LAVERY_LONG_GUN_CWT`). The 1812 fit's long guns are Lavery's types of
    1812, which Adye's table of 1804 does not hold: the 9-ft 18-pounder of 42 cwt (Adye's 9-ft gun
    is the 40-cwt one of 1761) and the 12-pounders of 9 ft and 7 ft 6 in, 34 and 29 cwt (Adye's 32
    and 29 1/4, as package 81 read p. 155; the Bellona's two 9-ft 12s weighed about 34 at Chatham,
    Lavery 1985 Table 19); the 8 ft 6 in nine of 1761 Lavery's, Adye giving none."""
    adye = period.ADYE_LONG_GUN_CWT.get(pounder, {})
    if length in adye and not of_1812:
        return adye[length]
    return period.LAVERY_LONG_GUN_CWT[pounder][length]


def places_of(profile):
    """Each deck's places from forward as (number, x, sill), metres as the profile has them, so
    that a gun on one stands on its triple (Build-Ships.md §4.4), numbered by deck from No. 1
    (`GUN_DECKS`, B7.d)."""
    out = {}
    for deck in GUN_DECKS:
        ports = sorted(profile["ports_m"][deck], key=lambda t: -t[0])
        out[deck] = [(1 + i, x, sill) for i, (x, sill, _hb) in enumerate(ports)]
    return out


def by_deck_id(gun):
    """A gun's id with its deck (Bel-D §5.2 item 2, B7.d): `gun.lower.3.starboard`, since each deck
    has its own No. 3 and `g.broadside_pair` writes `gun.3.starboard`."""
    return f"gun.{gun['deck']}.{gun['number']}.{gun['side']}"


def pairs(places, deck, kind, pounder, cwt, note):
    """Broadside pairs at `places`, each gun on its triple to the centimetre with its deck named,
    its crew the period's to the pair (Bel-D §5.3): Falconer's for a long gun "when the ship is well
    manned, so as to fight both sides at once occasionally" (1780, QUARTERS), Douglas's four for a
    carronade of any nature (1829, art. 136); the note on the first. Each id re-keyed by its deck
    after the call (`by_deck_id`), as the crew is."""
    crew = period.FALCONER_CREW[pounder] if kind == "long" else period.DOUGLAS_CARRONADE_CREW
    out = []
    for i, (number, x, sill) in enumerate(places):
        made = g.broadside_pair(
            number, kind, pounder, cwt, x, sill, note if i == 0 else None, deck=deck, round_to=0.01
        )
        for gun, _ in made:
            gun["id"] = by_deck_id(gun)  # reassigned, so that the key keeps its place
            gun["crew"] = crew  # reassigned, so that the key keeps its place (Indf §5.2)
        out += made
    return out


CARRONADE_WORDS = (
    "four men to the pair, its captain, two privates and a provider (Douglas 1829 art. 136), the "
    "marines first at the beat to quarters (crew/quarters.py)"
)


def her_fits(profile):
    """Her three fits (Bel-D §5.1-§5.3) as (name, source, guns, note), in the file's order."""
    p = places_of(profile)
    lower = pairs(
        p["lower"],
        "lower",
        "long",
        32,
        long_cwt(32, (9, 6)),
        "The lower deck's twenty-eight long 32-pounders, fourteen a side: the 9 ft 6 in gun of 55 "
        "cwt (Adye 1804 p. 155; Lavery 1985 p. 21, Table 17, 1760-1812; answer 12), each on its "
        "port, its x and its sill to the centimetre (Bel-D §5.2); thirteen men to the pair, who "
        "fight whichever side bears (Falconer 1780, QUARTERS). Numbered by deck from forward, "
        "each deck from No. 1 as the period numbered each deck, a gun at a time, where a pair here "
        "keeps one number (the Regulations 1808 printing, the Gunner, p. 215: Bel-D §5.2, B7.d).",
    )
    upper_40 = pairs(
        p["upper"],
        "upper",
        "long",
        18,
        long_cwt(18, (9, 0)),
        "The upper deck's twenty-eight long 18-pounders: the 9 ft gun of 40 cwt (Adye 1804 p. "
        "155; Lavery 1985 Table 17, 1761; answer 12); nine men to the pair (Falconer 1780, "
        "QUARTERS).",
    )
    quarterdeck_9s = pairs(
        p["quarterdeck"],
        "quarterdeck",
        "long",
        9,
        long_cwt(9, (7, 6)),
        "The quarterdeck's fourteen long 9-pounders, seven a side, Q1 and Q2 under the poop: the "
        "7 ft 6 in gun of 24 cwt 2 qr (Adye 1804 p. 155; answer 12); six men to the pair "
        "(Falconer 1780).",
    )
    forecastle_9s = pairs(
        p["forecastle"][:2],
        "forecastle",
        "long",
        9,
        long_cwt(9, (8, 6)),
        "The forecastle's four long 9-pounders, two a side in its two ports: the 8 ft 6 in gun of "
        "27 1/2 cwt, the Bellona's own forecastle guns of 1761 (Lavery 1985 p. 21, Table 18, the "
        "longer nines taken as the forecastle's, judgement; Table 17 gives the 27 1/2 cwt, Table "
        "18 prints 27), her class's list taken before answer 12's pattern (Bel-D §5.3); six men "
        "to the pair.",
    )
    of_1793 = lower + upper_40 + quarterdeck_9s + forecastle_9s
    of_1795 = (
        of_1793
        + pairs(
            p["forecastle"][2:],
            "forecastle",
            "carronade",
            32,
            period.ADYE_CARRONADE_CWT[32],
            "The forecastle's two 32-pounder carronades of the Order of 19 November 1794, one a "
            "side over the rail abaft its fore port (the place judgement, Bel-D §5.1): 17 cwt 0 qr "
            f"14 lb, the 4 ft 0 1/2 in carronade (Adye 1804 p. 72); {CARRONADE_WORDS}.",
        )
        + pairs(
            p["roundhouse"],
            "roundhouse",
            "carronade",
            18,
            period.ADYE_CARRONADE_CWT[18],
            "The poop's six 18-pounder carronades, three a side over its rail: the Order's six as "
            "James tabulates the small 74s (vol. 1 p. 256 and Abstract No. 3); she threw 'four "
            "poop carronades' overboard in June 1795, the calibre not given (vol. 1 pp. 265-266); "
            "the places judgement (Bel-D §5.1). 9 cwt, the 3 ft 3 in carronade (Adye 1804 p. 72); "
            "four men to the pair (Douglas 1829 art. 136).",
        )
    )
    quarterdeck = p["quarterdeck"]
    forecastle = p["forecastle"]
    roundhouse = p["roundhouse"]
    of_1812 = (
        lower
        + pairs(
            p["upper"],
            "upper",
            "long",
            18,
            long_cwt(18, (9, 0), of_1812=True),
            "The upper deck's twenty-eight long 18-pounders of 1812: the 9 ft gun of 42 cwt, "
            "Lavery's type of 1812 (1985 p. 21, Table 17), which Adye lacks; the Bellona's "
            "twenty-eight weighed 41 1/8 to 42 7/8 cwt at Chatham (p. 22, Table 19); nine men to "
            "the pair (Falconer 1780).",
        )
        + pairs(
            quarterdeck[:3],
            "quarterdeck",
            "long",
            12,
            long_cwt(12, (7, 6)),
            "The quarterdeck's six long 12-pounders at its three foremost ports a side, in the "
            "wake of the main shrouds, long guns at the shrouds by the order of 17 March 1797 "
            "(James vol. 2 pp. 119-120, read (OCR); the ports by the measured channels, "
            "judgement): the 7 ft 6 in gun of 29 cwt (Lavery 1985 p. 21, Table 17, 1812; Table "
            "19's six); seven men to the pair (Falconer 1780).",
        )
        + pairs(
            quarterdeck[3:],
            "quarterdeck",
            "carronade",
            32,
            period.ADYE_CARRONADE_CWT[32],
            "The quarterdeck's eight 32-pounder carronades at its four after ports a side, Q2 in "
            "the wake of the mizen shrouds taking a carronade against the order's letter, the list "
            "leaving four long guns a side (Bel-D §5.1, judgement): 17 cwt 0 qr 14 lb (Adye 1804 "
            "p. 72; the Bellona's weighed 17 1/4 to 18 cwt, Lavery 1985 Table 19, a pattern's "
            f"weight taken over the founders' scatter, Bel-D §5.3); {CARRONADE_WORDS}.",
        )
        + pairs(
            forecastle[:1],
            "forecastle",
            "carronade",
            32,
            period.ADYE_CARRONADE_CWT[32],
            "The forecastle's two 32-pounder carronades at its fore ports (Lavery 1985 Table 19; "
            "the ports by the 1797 order, judgement); four men to the pair.",
        )
        + pairs(
            forecastle[1:2],
            "forecastle",
            "long",
            12,
            long_cwt(12, (9, 0)),
            "The forecastle's two long 12-pounders at its after ports, in the wake of the fore "
            "shrouds (the 1797 order; judgement): the 9 ft gun of 34 cwt (Lavery 1985 Table 17, "
            "1812; Table 19's two); seven men to the pair.",
        )
        + pairs(
            roundhouse[:1],
            "roundhouse",
            "carronade",
            18,
            period.ADYE_CARRONADE_CWT[18],
            "The poop's two 18-pounder carronades at its foremost places (Lavery 1985 Table 19; "
            "the places judgement): 9 cwt (Adye 1804 p. 72; the Bellona's 9 3/4 and 10 1/8, Table "
            "19); four men to the pair.",
        )
        + pairs(
            roundhouse[1:2],
            "roundhouse",
            "carronade",
            12,
            period.ADYE_CARRONADE_CWT[12],
            "The poop's two 12-pounder carronades beside them, its aftmost places empty: Table 19 "
            "names their founder, and Lavery's Table 17 dates a 74's 12-pounder carronades to "
            "1793 and 1812; the poop is judgement, the boats' guns the other reading (Bel-D "
            "§5.1). 5 cwt 3 qr 10 lb, the 2 ft 2 in carronade (Adye 1804 p. 72), by her design's "
            "rule, Adye's weight where Adye gives one, over Table 17's 6 cwt (the Bellona's "
            "weighed 6 1/2 cwt, Table 19); four men to the pair.",
        )
    )
    crews = "Adye 1804 pp. 72 and 155, the pieces; Falconer 1780 (QUARTERS) and Douglas 1829 (art. "
    crews += "136), the crews"

    def own(guns):
        """A fit's guns its own mappings, that no two fits share one (the dump would alias it)."""
        return [(dict(gun), note) for gun, note in guns]

    return [
        (
            FIT_1793,
            "James, Naval History vol. 1, Abstract No. 1 (page image); RMG ZAZ0890, the armament "
            "block (read); Lavery, The 74-Gun Ship Bellona (1985), p. 21, Tables 17-18 (read "
            f"(owner's book)); {crews}",
            own(of_1793),
            "The class's establishment as James gives it: 28 x 32-pounders on the lower deck, 28 x "
            "18-pounders on the upper deck, 14 x 9-pounders on the quarterdeck and 4 x 9-pounders "
            "on the forecastle, 74 pieces (James vol. 1, Abstract No. 1; ZAZ0890's armament block; "
            "the Bellona's of 1761, Lavery 1985 p. 21, Table 18).",
        ),
        (
            FIT_1795,
            "The Admiralty Order of 19 November 1794 as James tabulates the small 74s (Naval "
            "History vol. 1 p. 256 and Abstract No. 3, page images); Lavery 1985 p. 21, Tables "
            f"17-18 (read (owner's book)); {crews}",
            own(of_1795),
            "The Order of 19 November 1794, compulsory for ships coming forward to be fitted: "
            "those of 1793 with 2 x 32-pounder carronades on the forecastle and 6 x 18-pounder "
            "carronades on the poop, 82 pieces (James vol. 1 p. 256 and Abstract No. 3). The "
            "default, 1795-1805 (answer 3).",
        ),
        (
            FIT_1812,
            "Lavery, The 74-Gun Ship Bellona (1985), p. 22, Table 19, the Bellona's guns at "
            "Chatham, 6 January 1812, after TNA ADM 160/54 (p. 23; read (owner's book)); the order "
            "of 17 March 1797 (James, Naval History vol. 2 pp. 119-120, read (OCR)), the places; "
            f"{crews}",
            own(of_1812),
            "As the Bellona at Chatham, 6 January 1812: 28 x 32-pounders, 28 x 18-pounders, 8 x "
            "12-pounders, 10 x 32-pounder, 2 x 18-pounder and 2 x 12-pounder carronades, 78 pieces "
            "(Lavery 1985 p. 22, Table 19), long guns in the wake of the shrouds by the 1797 order "
            "and carronades elsewhere (the places judgement, Bel-D §5.1). Her late fit, for Basque "
            "Roads in 1815 (Bel-D §11); Maitland's Bellerophon then had long 9s at the shrouds, "
            "not 12s (Maitland 1826 p. 79, read (OCR)).",
        ),
    ]


def broadside_lb(guns):
    """A fit's broadside by 70's rule (combat/far.py): one side's broadside guns and every
    chaser."""
    one_side = [gun for gun, _ in guns if gun["place"] != "broadside" or gun["side"] == g.SIDES[0]]
    return sum(gun["pounder"] for gun in one_side)


def check_fits(fits, profile):
    """Bel-D §1.5's checks on her guns, raised before her file is written: every broadside gun of
    every fit on a triple of its deck to the centimetre, its deck named (Build-Ships.md §4.4), its
    id its deck's, number's and side's (B7.d); the pieces of each fit 74, 82 and 78, and the
    broadsides by 70's rule 781, 867 and 938 lb."""
    triples = {
        deck: {(round(x, 2), round(s, 2)) for x, s, _ in t}
        for deck, t in profile["ports_m"].items()
    }
    for name, _, guns, _ in fits:
        for gun, _ in guns:
            deck = gun.get("deck")
            if deck is None or (gun["x_m"], gun["height_m"]) not in triples.get(deck, set()):
                raise ValueError(
                    f"her fit '{name}' puts {gun['id']} at x {gun['x_m']} m, {gun['height_m']} m "
                    f"above her water, on no triple of its deck ({deck})."
                )
            if gun["id"] != by_deck_id(gun):
                raise ValueError(f"her fit '{name}' keys {gun['id']}, not {by_deck_id(gun)}.")
        pieces, lb = len(guns), broadside_lb(guns)
        if (pieces, lb) != FIT_FIGURES[name]:
            raise ValueError(
                f"her fit '{name}' mounts {pieces} pieces with a broadside of {lb} lb, not "
                f"{FIT_FIGURES[name][0]} and {FIT_FIGURES[name][1]} (Bel-D §1.5)."
            )


def default_guns(fits):
    """The default fit's guns, against which her quarter bill and her stores are set."""
    return next(guns for name, _, guns, _ in fits if name == DEFAULT_FIT)


def armament(b, fits):
    """Her fits and their magazines (Bel-D §5.4): `fit_magazine` with the King's allowance
    (judgement, as every King's file), the charges Table No. 29's through `charge_lb` (SW-1),
    the exercise a two-decker's, a third of her upper deck's guns. Her guns numbered by deck
    (B7.d): the armament's `numbering` set after the call, the generator's own taking no such
    key (Bel-D §12.1), its words in the section's note."""
    exercise = g.exercise_allowance(UPPER_DECK_GUNS, decks=2)
    rounds = {"long": g.KINGS_ROUNDS, "carronade": g.KINGS_ROUNDS}
    b.armament(
        ARMAMENT_NOTE,
        DEFAULT_FIT,
        [
            (name, source, guns, g.fit_magazine(guns, rounds, exercise), note)
            for name, source, guns, note in fits
        ],
    )
    b.doc["armament"]["numbering"] = NUMBERING
    for name, *_ in fits:
        b.armament_notes[("magazine", name, "exercise_charges")] = period.TWO_DECKS_EXERCISE_NOTE
    REPORT["fits"] = {
        name: (
            len(guns),
            broadside_lb(guns),
            sum(gun["crew"] for gun, _ in guns if gun["side"] == g.SIDES[0]),
        )
        for name, _, guns, _ in fits
    }


# ---------------------------------------------------------------------------
# The company, the marines, the quarter bill and the flag (Bel-D §6)
# ---------------------------------------------------------------------------

# Her company on the Regulations' table of officers and ratings of 31 December 1806 (1808
# printing p. 165 and IA leaves 455-460, the page images read row by row: Bel §4.3), the 590
# column (answer 10), in the 64's form (Bel-D §6.1): the posts her people file's sixteen; the
# marines 111 (§6.2); the idlers the column's rows by trade, 44, and judgement where they say so;
# the seamen the rest, shared among the six stations as the frigate-36's 182 are (28, 24, 30,
# 14, 50 and 36: judgement, as Indf §6.2), the column's petty officers, mates, midshipmen and
# first- and second-class boys among them.
COMPLEMENT = 590
COLUMN = 74
POSTS = 16
MARINES = 111
FRIGATE_SEAMEN = {
    "forecastle": 28,
    "fore_top": 24,
    "main_top": 30,
    "mizzen_top": 14,
    "afterguard": 50,
    "waisters": 36,
}
IDLERS = {
    "carpenter's crew": (
        11,
        "the carpenter's mate and crew of eight, the caulker and the caulker's mate",
    ),
    "sailmaker's crew": (4, "the sailmaker's mate and crew of two, and the ropemaker"),
    "cooper": (1, "a cooper, for the casks (judgement: the column pays one and numbers none)"),
    "armourer": (3, "the armourer and two armourer's mates"),
    "cook": (2, "the ship's cook and the cook's mate"),
    "steward": (
        3,
        "the purser's steward and the steward's mate, and a gunroom steward (judgement)",
    ),
    "servant": (
        14,
        "the boys of the third class, who replaced the officers' servants in 1794 (James vol. 1 "
        "pp. 256-257, page image; judgement, as the 64's servants)",
    ),
    "surgeon's mate": (2, "the two assistant surgeons"),
    "clerk": (2, "the captain's clerk and the schoolmaster"),
    "master-at-arms's party": (2, "the two ship's corporals"),
}
MARINES_NOTE = (
    "the 590 column's captain, three lieutenants, three serjeants, two corporals and two "
    "drummers, 11, and 100 privates: in March 1803 the Mars embarked '100 rank and file' and the "
    "Spartiate 'a captain and 100 marines' (Naval Chronicle vol. IX p. 245, page image; Bel "
    "§4.4), within her dates and at the foot of answer 11's 100-110; the Bellona carried 90 "
    "privates in 1761 (Lavery 1985 p. 17, Table 7). Soldiers served in their place in 1794-95 "
    "(James vol. 1 p. 155 n. 1); a file carries one company"
)
# The quarter bill beyond the trimmers (Bel-D §6.3): the frigate-36's two at the helm and no
# powder beyond the idlers; her small-arms men the frigate-36's share of her seamen, 20 of 182;
# her boarders a quarter of the seamen (`gen_ships.BOARDERS_NOTE`); all judgement as hers. The
# filling party the 590 column's eighteen quarter gunners (Bel-D §5.4).
HELM = 2
SMALL_ARMS_OF_SEAMEN = 20.0 / 182.0
BOARDERS_OF_SEAMEN = 0.25
FILLING = 18
# The trimmers' shares by station, the frigate-36's 8, 10, 12, 6 and 8 of her 44 (judgement).
TRIMMER_SHARES = {"forecastle": 8, "fore_top": 10, "main_top": 12, "mizzen_top": 6, "afterguard": 8}
# Her stores beside the company (Bel-D §7; judgement, the 64's method): the frigate-36's 100
# tons of water for her 264 and her 600 fathoms of spare rope, carried by the complement, the
# rope to fifty fathoms; four months' provisions.
FRIGATE_COMPLEMENT = 264.0
PROVISIONS_DAYS = 120


def half_up(v):
    """A count to the nearest whole man, a half up."""
    return math.floor(v + 0.5)


def shares(total, weights):
    """`total` men split by `weights` to whole men, the largest remainders taking the odd ones
    (a tie to the station first in the bill)."""
    whole = sum(weights.values())
    exact = {k: total * w / whole for k, w in weights.items()}
    out = {k: math.floor(v) for k, v in exact.items()}
    for k in sorted(exact, key=lambda k: out[k] - exact[k])[: total - sum(out.values())]:
        out[k] += 1
    return out


def seamen_by_station():
    """Her seamen by station: the complement less the posts, the marines and the idlers, shared
    by the frigate-36's stations."""
    idlers = sum(n for n, _ in IDLERS.values())
    return shares(COMPLEMENT - POSTS - MARINES - idlers, FRIGATE_SEAMEN)


def her_people_file():
    """Her people file, `data/people/seventy-four.yaml`, read as the generator reads a wardroom
    file (`gen_ships.wardroom`): the raw entries."""
    with open(os.path.join(g.PEOPLE_DIR, "seventy-four.yaml"), encoding="utf-8") as f:
        return (g.yaml.safe_load(f) or {}).get("wardroom") or []


def at_the_guns(guns, marines):
    """The men one side's guns of a fit take, the chasers included (each chaser its own crew,
    a broadside pair one: `parts.Gun.pair_key`), and how many of them are marines, who take the
    carronades first (crew/quarters.py)."""
    one_side = [gun for gun, _ in guns if gun["place"] != "broadside" or gun["side"] == g.SIDES[0]]
    men = sum(gun["crew"] for gun in one_side)
    carronades = sum(gun["crew"] for gun in one_side if gun["kind"] == "carronade")
    return men, min(carronades, marines)


def company(b, guns):
    """Her crew section (Bel-D §6.1-§6.2), the posts and the people drawn at muster from her
    people file (§6.8), and the stores beside them: water, provisions and cordage by her
    complement, a shot plug to each of the default fit's `guns` (§7), the spare spars and the
    sail room by the frigate-36's method."""
    posts, drawn = g.wardroom("seventy-four")
    if len(posts) != POSTS:
        raise ValueError(f"her people file gives {len(posts)} posts, not her {POSTS} (Bel-D §6.1).")
    seamen = seamen_by_station()
    idlers = sum(n for n, _ in IDLERS.values())
    column = period.REGULATIONS_COLUMNS[COLUMN]
    water = half_up(100.0 * COMPLEMENT / FRIGATE_COMPLEMENT)
    cordage = 50 * half_up(600.0 * COMPLEMENT / FRIGATE_COMPLEMENT / 50.0)
    stations_note = (
        "Hands per station, both watches together: her seamen, the complement less the posts, the "
        "marines and the idlers, shared among the six stations as the frigate-36's 182 are (28, "
        "24, 30, 14, 50 and 36: judgement, Bel-D §6.1), the column's petty officers, mates, "
        "midshipmen and first- and second-class boys among them, the boys in the afterguard as "
        "landsmen (spec M3 9 item 6). Forecastlemen: the head, anchors and headsails; the best "
        "older seamen (Luce 1884 ch. XX)."
    )
    entries = [
        (
            ("complement",),
            COMPLEMENT,
            "The 74's establishment of 590 men and boys, the Regulations' table of 31 December "
            "1806 (1808 printing p. 165, the 590 column, read row by row on the page images: Bel "
            "§4.3; answer 10). The widows' men are counted as men, so the file is 4 over James's "
            "net 586; more hands may be signed on in the game. The brief's 'three times the "
            "frigate's' is a figure of speech the sources do not bear: 590 against her 264 (Bel "
            "§9).",
        ),
        (("names",), "english", "A King's ship: the english list in data/crew/names.yaml."),
        (("stations", "forecastle"), seamen["forecastle"], stations_note),
        (("stations", "fore_top"), seamen["fore_top"], "Fore topmen."),
        (("stations", "main_top"), seamen["main_top"], "Main topmen, the largest top."),
        (("stations", "mizzen_top"), seamen["mizzen_top"], "Mizzen topmen."),
        (
            ("stations", "afterguard"),
            seamen["afterguard"],
            "Afterguard, the boys included (spec M3 9 item 6: boys count as landsmen).",
        ),
        (("stations", "waisters"), seamen["waisters"], "Waisters."),
        (
            ("stations", "marines"),
            MARINES,
            f"Marines: {MARINES_NOTE}. Their kit is the nation's (data/nations.yaml). They stand "
            "watch and work as afterguard, never aloft (Luce 1884 ch. XX; the Regulations p. "
            "422).",
        ),
        (
            ("stations", "idlers"),
            idlers,
            "Idlers: the trades below (Luce 1884 ch. XX: they stand no night watches).",
        ),
        (
            ("ratings", "able"),
            0.30,
            "Share of the seamen (not marines, idlers or officers) by rating: the frigate-36's "
            "(judgement, Bel-D §6.1); the Bellona's company of 1761 is in her notes (Lavery 1985 "
            "p. 17, Table 7). Able: 0.30.",
        ),
        (("ratings", "ordinary"), 0.40, "Ordinary: 0.40, judgement."),
        (("ratings", "landsman"), 0.30, "Landsmen: 0.30, judgement."),
    ]
    entries += [
        (
            ("posts", post),
            None,
            (
                "Station holders by post (spec M3 2.3): the commissioned officers, the column's "
                f"{sum(1 for x in posts if x.endswith('lieutenant'))} lieutenants, its master, "
                "second master, surgeon, carpenter, boatswain, gunner, purser and chaplain (the "
                f"Regulations 1806 p. 165, the {column} column, its first row), and the sailmaker "
                "and the master-at-arms, posts in the frigate's and the 64's files; the posts are "
                "free words, so the second master and the chaplain stand as written (Bel-D §6.1). "
                "Her people file (data/people/seventy-four.yaml) gives them. Names are drawn at "
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
                f"How the idlers are made up, the {column} column's rows by trade (the "
                "Regulations 1806; Bel §4.3) and judgement where it says so; they must sum to the "
                "idlers. "
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
            water,
            "Water: the frigate-36's 100 tons for her 264 carried by the complement, in "
            "iron-hooped casks (Bel-D §7; judgement, the 64's method), as many weeks at a gallon a "
            "man a day as hers. Steel's 80 'as fitted for sea with six months' provision' carried "
            "620 tons of provisions and water for 700 men (1805 pp. 197-198, read (OCR)), the "
            "period's check.",
        ),
        (
            ("stores", "provisions_days"),
            PROVISIONS_DAYS,
            "Provisions: four months at full allowance for the complement, as the frigate-36's "
            "(judgement).",
        ),
        (("stores", "spare_spars"), {}, None),  # the booms, by class: below
        (
            ("stores", "cordage_fathoms"),
            cordage,
            "Spare rope in the boatswain's store: the frigate-36's 600 fathoms carried by the "
            "complement, to fifty fathoms (Bel-D §7; judgement).",
        ),
        (
            ("stores", "shot_plugs"),
            len(guns),
            g.SHOT_PLUGS_NOTE + " One a gun of her default fit (Bel-D §7).",
        ),
        *g.ration_entries("a King's ship"),
    ]
    b.crew(entries)
    # the named few beyond the posts (package 35), each drawn from a station at muster, the
    # counts above unchanged; the roles and their notes are her people file's (Bel-D §6.8)
    b.people(
        "The named people beyond the posts (package 35, spec M5 §22): each drawn from a station "
        "at muster, the counts above unchanged; see data/people/seventy-four.yaml.",
        drawn,
    )
    # the booms (package 30b): the frigate-36's, by Luce's stowage (gen_ships.frigate_crew), on
    # her own spars: Dragon's list gives one jib-boom (Lavery 1985 Table 10)
    b.spare_spars(
        "The booms: the spare spars by class, as the frigate-36's (Luce 1866 ch. XVII, 'Stowing "
        "Booms'; Luce 1884 ch. XI; Steel 1794 vol. I, 'Lashing of Booms'), of her own spars "
        "(Bel-D §7); see tools/ships/bellerophon.py.",
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
            (
                "jib_boom",
                1,
                "The spare jib-boom, amidships (Luce 1866); Dragon's list gives her one jib-boom "
                "(Lavery 1985 Table 10, its 'flying jib boom' row).",
            ),
        ],
    )
    sail_room(b)


def sail_room(b):
    """Her sail room by the frigate-36's method (Luce 1884 ch. X p. 171; gen_ships.frigate_crew)
    on her own sails (Bel-D §7): the second of each working sail of the frigate's list that she
    carries, the heavy-weather foresail and topsails of No. 1, one of each storm sail, and her
    occasional sails, the driver's spare among them (Ext §17.7)."""
    canvas = {s["id"]: s["canvas_no"] for s in b.doc["sails"]}
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
        "mizzen.course",
        "fore.topmast_staysail",
    ]
    heavy = ["fore.course", "fore.topsail", "main.topsail"]
    storm = ["fore.storm_staysail", "mizzen.storm_staysail", "storm_mizzen"]
    occasional = [k for k in ("mizzen.driver",) if k in canvas] + [
        f"fore.save_all.{s}" for s in g.SIDES
    ]

    def first(text, i):
        return text if i == 0 else None

    b.sail_room(
        "The sail room (spec 3b §6.3): Luce's allowance for a frigate (1884 ch. X p. 171), as "
        "the frigate-36's and the 64's, on her own sails (Bel-D §7), every sail new; see "
        "tools/ships/bellerophon.py.",
        [
            (
                k,
                canvas[k],
                first(
                    "The second of each working sail, of the working number (Luce p. 171); she "
                    "has one jib and no flying jib, and her mizen course stands for the frigate's "
                    "spanker.",
                    i,
                ),
            )
            for i, k in enumerate(working)
        ]
        + [
            (
                k,
                1,
                first(
                    "The heavy-weather foresail and fore and main topsails, of No. 1 (Luce p. 171, "
                    "the table's note).",
                    i,
                ),
            )
            for i, k in enumerate(heavy)
        ]
        + [
            (k, canvas[k], first("Storm canvas, one of each (Luce p. 171).", i))
            for i, k in enumerate(storm)
        ]
        + [
            (
                k,
                canvas[k],
                first(
                    "The occasional sails, one each (spec 3b §6.4): her driver, Steel's boomsail, "
                    "set in the mizen course's place (Ext §17), and the save-alls.",
                    i,
                ),
            )
            for i, k in enumerate(occasional)
        ],
    )


def quarter_bill(b, guns):
    """Her quarter bill set against the default fit (Bel-D §6.3): the trimmers what her seamen
    leave when one side's long guns and the wheel are manned, the marines taking the carronades,
    split by the frigate-36's shares; the bill's `marines` (her stage 0c's key) the marines kept
    in their division, the rest of them, written after the generator's call, which takes no such
    key (Bel-D §12.1), as B1's module reassigns the filling's note after the same call."""
    seamen = sum(seamen_by_station().values())
    men, marines_at = at_the_guns(guns, MARINES)
    total = seamen - (men - marines_at) - HELM
    trimmers = shares(total, TRIMMER_SHARES)
    kept = MARINES - marines_at
    REPORT["bill"] = (seamen, men, marines_at, total, kept)
    b.quarter_bill(
        g.QUARTER_BILL_NOTE,
        [
            (
                "forecastle",
                trimmers["forecastle"],
                f"The trimmers: what her seamen leave when one side's guns of '{DEFAULT_FIT}' and "
                "the wheel are manned, the marines taking the carronades, split by the "
                "frigate-36's trimmer shares, 8, 10, 12, 6 and 8 of 44 (Bel-D §6.3; judgement, as "
                "Indf §6.4). Of the forecastlemen, for the head sails and the fore braces (Luce "
                "1884 ch. XX: the forecastlemen 'the best older seamen').",
            ),
            ("fore_top", trimmers["fore_top"], "Of the fore topmen, for the fore braces aloft."),
            ("main_top", trimmers["main_top"], "Of the main topmen, the largest top."),
            (
                "mizzen_top",
                trimmers["mizzen_top"],
                "Of the mizzen topmen, for the crossjack braces and the mizen course.",
            ),
            (
                "afterguard",
                trimmers["afterguard"],
                "Of the afterguard, at the main sheet and the after braces.",
            ),
        ],
        HELM,
        0,
        "sail before guns",
        {
            "helm": "Two quartermasters at the wheel (Luce 1884 ch. XX, the quartermasters), as "
            "the frigate-36's (judgement).",
            "powder": "The powder beyond the idlers: none; her fourteen boys among the idlers, "
            "her cooks, stewards, clerks, the cooper, the armourers and the sailmaker's crew "
            "pass the cartridges (Falconer 1780, QUARTERS: 'often a boy to bring powder'; "
            "judgement, as the frigate-36's).",
            "priority": g.PRIORITY_NOTE,
        },
        small_arms=half_up(seamen * SMALL_ARMS_OF_SEAMEN),
        boarders=half_up(seamen * BOARDERS_OF_SEAMEN),
        small_arms_note="Seamen with the muskets of the stand of arms, the frigate-36's share of "
        "her seamen (20 of 182; judgement, as Indf §6.4). Falconer's men to the small arms by the "
        "Admiralty's order, 80 for a third rate of 70 guns and 100 for one of 80 (1780, QUARTERS, "
        "OCR l. 14335-14372), and the Regulations' hundred seamen of a 74 trained to the muskets "
        "for service ashore (p. 142, page image), stand for the whole party, marines and seamen.",
        boarders_note="The boarders by the bill, a quarter of her seamen told off from the guns' "
        "crews (Luce 1884 ch. XX; judgement, the shared rule), with the marines, who board with "
        "the bayonet.",
        filling=FILLING,
    )
    b.crew_notes[("quarter_bill", "filling")] = (
        g.FILLING_NOTE + " Hers are the Regulations' eighteen quarter gunners of the "
        f"{period.REGULATIONS_COLUMNS[COLUMN]} column (the 1808 printing p. 165: Bel §4.3), which "
        "Falconer's one to every four cannon gives on the 1793 establishment's 74 pieces, the "
        "carronades never rated cannon (Bel-D §5.4); Lavery's 1766 allowance, one to every four "
        "guns (1985 p. 17, Table 6), the same."
    )
    b.doc["crew"]["quarter_bill"]["marines"] = kept
    b.crew_notes[("quarter_bill", "marines")] = (
        "The marines the bill keeps in their division at the beat (her stage 0c's key, Bel-D "
        "§12.1): her marines but those at the default fit's carronades, quartered on the poop and "
        "the forecastle or gangway, at the great guns only in distant cannonading (Falconer 1780, "
        "QUARTERS), as her marines stood on her poop on 1 June 1794 (the Molloy minutes, read "
        "(OCR): Bel §4.4). Read by her bill by deck (Bel-D §6.4, B7.b); until it, the beat takes "
        "her marines to the guns as every ship's."
    )


def flag_party(b):
    """The rear-admiral's flag party in her crew's `flag:` (her stage 0c's key; Bel-D §17.0, the
    owner's answer, which replaced §6.6's pick): the entries of her people file marked `flag`, in
    its order, each a post in the posts' form (stage 0c's laid form, for the lead to confirm); the
    places and outlines her people file's, as every post's are."""
    party = [str(e["role"]) for e in her_people_file() if e.get("flag")]
    if len(party) != FLAG_PARTY:
        raise ValueError(f"her people file's flag party is {len(party)}, not {FLAG_PARTY}.")
    b.doc["crew"]["flag"] = [{"post": role} for role in party]
    b.crew_notes[("flag",)] = (
        "The flag party she bears beyond her company when a scenario hoists a rear-admiral's flag "
        "in her (Bel-D §17.0, the owner's answer: the rear-admiral and their people in the ship "
        "file, so that models may be stationed as them): the rear-admiral, their "
        "flag lieutenant and secretary, and their servants, the 'customary supernumeraries' James "
        "adds for a rear-admiral (vol. 1 p. 156, OCR l. 12961-12963; Bel §4.3: 609 under Pasley's "
        "flag on 1 June 1794), the party's make-up and its servants judgement, no establishment "
        "of a rear-admiral's retinue having been read; counted in no station and not in her 590. "
        "Inert: the world code that brings them aboard is a package of its own (the lead's answer "
        "(15)). Their stations, places and outlines are in data/people/seventy-four.yaml."
    )


# James's customary supernumeraries for a rear-admiral (vol. 1 p. 156): the flag party in all.
FLAG_PARTY = 15


def check_company(b):
    """Bel-D §1.5's checks on her company, raised before her file is written: the company's sum
    590, the marines 111, the idlers by trade summing to the idlers, and the bill's `marines` no
    more than the marines."""
    crew = b.doc["crew"]
    st = crew["stations"]
    total = len(crew["posts"]) + sum(st.values())
    if total != COMPLEMENT or crew["complement"] != COMPLEMENT:
        raise ValueError(f"her company sums to {total}, not {COMPLEMENT} (Bel-D §6.1).")
    if st["marines"] != MARINES:
        raise ValueError(f"her marines are {st['marines']}, not {MARINES} (Bel-D §6.2).")
    if sum(crew["idlers_by_trade"].values()) != st["idlers"]:
        raise ValueError("her idlers by trade do not sum to her idlers (Bel-D §6.1).")
    if not 0 <= crew["quarter_bill"]["marines"] <= st["marines"]:
        raise ValueError("her bill keeps more marines than she bears (Bel-D §6.3).")


# ---------------------------------------------------------------------------
# Ground tackle, boats, pumps and hold (Bel-D §7)
# ---------------------------------------------------------------------------

# The ground tackle (answer 13), through `Builder.ground_tackle` directly, never the generator's
# rule, which gives a 74 two bowers and overstates them by 14-20% (Bel §5.7): Steel's "Smaller
# 74 Guns" anchors, the same as Lavery's Table 4 about 1800 (`period.STEEL_ANCHORS[74]`), on
# Lavery's cables of 100 fathoms (`period.LAVERY_74_CABLES`), laid three on the best bower and two
# on the small as on the Channel service (Lever 1808 p. 67, as the generator cites it), one on the
# sheet and one on the spare; the spare anchor of the kind `sheet`, as the 64's.
BOWER_CABLES = {"best_bower": 3, "small_bower": 2, "sheet": 1, "spare_anchor": 1}
# Her burthen, the design's 1,604 tons (ZAZ1357's table, 1,603 89/94 tons, read; Elephant's
# contract column, ZAZ1070: Bel §3.6), which the hold's rule reads.
BURTHEN_TONS = 1604.0
# Her boats, a 74's allowance about 1800 (Lavery 1985 p. 16, Table 5, read (owner's book)), each
# (id, kind, name, length in feet, note); their breadth, oars and tons by the generator's factors
# on her lengths (`boat_line`), since `boat_entries` takes Luce's lengths from the ship's.
BOATS = [
    (
        "launch",
        "launch",
        "the launch",
        31.0,
        "The launch of 31 ft (Lavery 1985 p. 16, Table 5, a 74's boats about 1800); the "
        "longboat's work, the water and the anchors (Steel 1794 vol. I: the stream anchor 'sent "
        "in the long-boat'); her breadth a quarter of her length, her oars a thwart to three "
        "feet and her tons by the generator's rule for a boat herself (judgement).",
    ),
    (
        "barge",
        "barge",
        "the barge",
        32.0,
        "Table 5's larger pinnace, of 32 ft, the captain's boat, doing the barge's work and filed "
        "as the barge (judgement, Bel-D §7; the owner's 'six or seven, with a barge', answer 13).",
    ),
    ("pinnace", "pinnace", "the pinnace", 28.0, "The pinnace, Table 5's smaller, of 28 ft."),
    ("first_cutter", "cutter", "the first cutter", 25.0, "The first of two cutters of 25 ft."),
    ("second_cutter", "cutter", "the second cutter", 25.0, "The second cutter of 25 ft."),
    (
        "small_cutter",
        "cutter",
        "the small cutter",
        18.0,
        "The small cutter of 18 ft, the boat at the stern davits (judgement in the place).",
    ),
]
# Her pumps (task 9): four chain pumps in the well round the main mast, two abaft it and two
# before it, at about 70.4 and 77.2 ft from AP (Dragon's gun-deck plan, 1361F, read; the well
# ZAZ1360, read: Bel §3.4); and two hand pumps (judgement, as the 64's).
PUMP_NAMES = [
    "the starboard after chain pump",
    "the larboard after chain pump",
    "the starboard fore chain pump",
    "the larboard fore chain pump",
    "the starboard hand pump",
    "the larboard hand pump",
]


def ground_tackle(b):
    """Her anchors and cables (Bel-D §7), through `Builder.ground_tackle`."""
    steel = period.STEEL_ANCHORS[74]
    cables = period.LAVERY_74_CABLES
    laid = sum(BOWER_CABLES.values())
    if (
        len(BOWER_CABLES) != steel["bowers"]
        or not laid == steel["bower_cables"] == cables["bower_cables"]
    ):
        raise ValueError(
            f"Steel's 74 has {steel['bowers']} bowers and {steel['bower_cables']} bower cables; "
            f"BOWER_CABLES lays {sum(BOWER_CABLES.values())} on {len(BOWER_CABLES)} (Bel-D §7)."
        )
    bower = round(steel["bower_cwt"] * g.CWT_KG)
    cable = cables["bower_cable_in"]
    stream = cables["stream_cable_in"]
    hawser = g.KEDGE_HAWSER_OF_BOWER * cable
    fathoms = period.LAVERY_74_CABLE_FATHOMS
    bowers = {
        "best_bower": (
            "bower",
            "the best bower",
            f"The bowers: four of {steel['bower_cwt']:g} cwt, Steel's 'Smaller 74 Guns' (Steel "
            "1794 vol. I, the anchor table, page image: Bel §5.7) and Lavery's four of about 1800 "
            f"(1985 p. 15, Table 4, read (owner's book)); seven cables of {cable:g} in and 100 "
            "fathoms (Table 4, after NMM SPB 15; Steel's 74 '23 or 22' in), rated as every rope by "
            "Luce 1866 ch. IV, laid three on the best bower and two on the small, 'three Cables on "
            "the best Bower, two on the small Bower' (Lever 1808 p. 67). The 64 took Falconer's "
            "120 fathoms a cable; her class's own list gives 100, and it is taken. Steel 1805's 71 "
            "cwt for every 74 (Folio LVII, page image), and Table 4's viols and messenger, which "
            "the file has no key for, are in her notes.",
        ),
        "small_bower": ("bower", "the small bower", None),
        "sheet": ("sheet", "the sheet anchor", "The sheet anchor, a bower's size, on one cable."),
        "spare_anchor": (
            "sheet",
            "the spare anchor",
            "The spare anchor, the fourth bower, on the seventh cable (Steel's 74 has shank "
            "painters for four: vol. II p. 39, page image); of the kind 'sheet', the schema's "
            "kinds being four, as the 64's.",
        ),
    }
    anchors = [
        (aid, kind, name, float(bower), fathoms * BOWER_CABLES[aid], cable, g.rope_kn(cable), text)
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
            f"The stream anchor of {steel['stream_cwt']:g} cwt (Steel's 'Smaller 74 Guns'; Lavery "
            f"Table 4), on Table 4's stream cable of {stream:g} in and 100 fathoms (Steel's "
            f"{steel['stream_cable_in']:g} in, 'A Cordage Table').",
        ),
        (
            "kedge",
            "kedge",
            "the kedge",
            float(round(steel["kedge_cwt"] * g.CWT_KG)),
            fathoms,
            hawser,
            g.rope_kn(hawser),
            f"The kedge of {steel['kedge_cwt']:g} cwt (the same tables), on a hawser of half the "
            "bower cable's size, the house rule (gen_ships.KEDGE_HAWSER_OF_BOWER; judgement), of "
            "her cables' length (judgement).",
        ),
    ]
    b.ground_tackle(
        "The ground tackle (package 34, spec M5 §18): four bowers, a stream and a kedge by Steel "
        "1794 and Lavery 1985 (answer 13; Bel-D §7), every figure's source in "
        "tools/ships/bellerophon.py; chain cable is later than 1805.",
        anchors,
        chain=False,
    )


def boat_line(bid, kind, name, length_ft, text):
    """A boat's line from her sourced length by the generator's own factors (`boat_entries`'s):
    her breadth a quarter of her length, a thwart to three feet of it, a man to an oar and one at
    the tiller, her tons by Luce's weight rule for the boat herself."""
    breadth = length_ft * g.BOAT_BREADTH_OF_LENGTH
    oars = max(2, int(length_ft / g.BOAT_FEET_PER_OAR) // 2 * 2)
    weight_lb = (
        breadth * breadth * length_ft * g.BOAT_WEIGHT_FACTORS.get(kind, g.BOAT_WEIGHT_DEFAULT)
    )
    tons = round(max(0.1, weight_lb / g.LB_PER_TON), 1)
    return (bid, kind, name, float(length_ft), oars, oars + 1, tons, text)


def boats_pumps_hold(b):
    """Her hold by her burthen, her pumps, four chain and two hand, and her six boats (Bel-D
    §7)."""
    g.hold_for(
        b,
        BURTHEN_TONS,
        True,
        "1,604 tons, the design's burthen (ZAZ1357's table, 1,603 89/94 tons, read; Elephant's "
        "contract column, ZAZ1070: Bel §3.6); a ship of war's hold is her own stores and ballast: "
        "judgement",
    )
    b.pumps(
        g.PUMPS_NOTE + " Hers four chain pumps in the well round the main mast, two abaft it and "
        "two before it (Dragon's gun deck, 1361F, read: task 9; the well ZAZ1360, read: Bel §3.4), "
        "and two hand pumps (judgement, as the 64's).",
        g.pump_entries(4, 2, PUMP_NAMES),
    )
    b.boats(
        "The boats (package 35, spec M5 §23): a 74's allowance about 1800, their lengths Lavery "
        "1985 p. 16, Table 5 (read (owner's book)); their breadth, oars and tons by the "
        "generator's factors on those lengths (a quarter of the length, a thwart to three feet, "
        "Luce's weight rule for the boat herself); see tools/ships/bellerophon.py.",
        [boat_line(*entry) for entry in BOATS],
    )


# ---------------------------------------------------------------------------
# Her description (Bel-D §8.1; SW-4's form)
# ---------------------------------------------------------------------------

DESCRIPTION = (
    "seventy-four",
    "a ship of the line",
    "a seventy-four, a ship of the line, fourteen ports a tier",
    "A third rate (Falconer 1780, RATES), of James's small class of 74s, under 1,700 tons (vol. 1 "
    "p. 451 note M*, read (OCR)): what the glass makes out, her two tiers of fourteen ports a side "
    "(Bel §3.3). Her rig's word is a ship of the line: her size and her two tiers are what a "
    "lookout tells first of one, at her rig's distance (the lead's ruling of 2026-11-12, (1); "
    "JUDGEMENT on the distance; before it, the frigate's word). Her default fit serves "
    "a far ship of her, filed here as every row since SW-4 files its fit (Bel-D §8.1 had none, "
    "the default serving either way); her roles a King's ship's and, where she leads a squadron, "
    "a commodore's, as the frigate's (Build-Ships.md §8.2); she sails by the first, a row filed "
    "since package 75 (brains.INTENT_RULED_ROWS, the lead's ruling).",
    DEFAULT_FIT,
    ["kings-ship", "commodore"],
)


# ---------------------------------------------------------------------------
# The file
# ---------------------------------------------------------------------------

# Her lee helm lying a-try (the lead's ruling (1) of 2026-11-10 at 19:30, B7: lie a-try from way
# on), `lie_a_try`'s own timing key on her file (`ShipSpec.timing`): the evolution's 5 degrees
# left her lying 86.5 to 101.4 degrees off at 3.57 kn from way on in 35 kn, and 87.6 at 3.52 with
# what it hands furled, where she lies about five points at 1.30 kn from rest. Measured (seed 7;
# docs/dev/TuningNotes.md, "The lead's rulings of 2026-11-10, built"): with what lie a-try hands
# furled, the least helm that settles her inside five to six and a half points under 2 kn is 17.5
# (70.6 at 1.96 kn), 19 lies 68.9 at 1.91 and 20 lies 67.6 at 1.88; from rest truth 28's form
# holds at every figure to 35. 20 taken (judgement), Luce's "helm a-lee" a little more than the
# frigate's: her clr_x_m (4.8) and truth 17 as the lead has them.
LIE_A_TRY_HELM_DEG = 20
LIE_A_TRY_NOTE = (
    "Her own figure for an evolution's timing, over its file's (the runner's): lying a-try, the "
    "helm a-lee 20 degrees where the evolution's file gives 5, the figure that brings her up from "
    "way on in a gale to six points with under 2 knots of way once what it hands is furled, where "
    "at 5 she lay eight points off at 3.5 knots; from rest she lies five points as before "
    "(measured: docs/dev/TuningNotes.md; judgement)."
)

ERA_NOTES = (
    "HMS Bellerophon, a 74-gun ship of the Arrogant class (Slade's design of 1758 on the Bellona's "
    "lines): ordered 1782, launched by Graves at Frindsbury in 1786, at the Glorious First of "
    "June, the Nile and Trafalgar, and Napoleon's at Basque Roads in 1815. 168 ft on the gun deck, "
    "46 ft 9 in extreme by the design and the contract, 1604 tons. Hull measured on her class's "
    "draughts (ZAZ1357, ZAZ1359; Research-74-2026-10.md); masts and yards Dragon's (Lavery 1985 "
    "Table 10), sails by Steel 1794 table IV, the 74 column; see tools/ships/bellerophon.py for "
    "every figure and judgement."
)
HEADER = (
    "# HMS Bellerophon, 1786: a 74-gun ship of the Arrogant class (Slade, 1758).\n"
    "# Generated by tools/gen_ships.py (tools/ships/bellerophon.py); edit those and\n"
    "# rerun, do not edit this file. Hull and profile: measured on her class's draughts\n"
    "# (RMG ZAZ1357, ZAZ1359; docs/design/Research-74-2026-10.md), her water the line\n"
    "# where her lowest lower-deck port stands the Bellona's reported 5 ft 2 in clear.\n"
    "# Spars: Dragon's (Lavery 1985 Table 10), her topgallant masts with Steel's long\n"
    "# pole-heads. Sails: Steel's table IV, the 74 column, the topgallants and royals cut\n"
    "# to the spars (the owner's rule). Her mizen course cut at the mast, her driver and\n"
    "# her yards under the bowsprit: tools/ships/mizen_yard.py and spritsail_yards.py\n"
    "# (docs/design/Design-ShipsEngineExtensions.md §3, §4, §17).\n"
    "# Units: metres, m2, kg, kN. Comments mark each judgement.\n"
)


def write(out_dir):
    """Build her file in full and dump it to `out_dir`."""
    hull, hull_notes = hull_block()
    b = HerBuilder("Bellerophon", "ship", ERA_NOTES, hull, hull_notes)
    geom, mast_x, rake = mast_geometry()

    yard_lengths = {"course": "yard", "topsail": "topsail_yard", "topgallant": "tg_yard"}
    yard_lengths["royal"] = "royal_yard"
    yard_heights = {"course": "yard_h", "topsail": "topsail_h", "topgallant": "tg_h"}
    yard_heights["royal"] = "royal_h"
    level_of_spar = {"course": "lower", "topsail": "topsail", "topgallant": "topgallant"}
    level_of_spar["royal"] = "royal"
    below = {"topgallant": "topsail_h", "royal": "tg_h"}

    # -- the square sails: Steel's below the topmast caps, cut to the spars above them -----------
    def cut(sid, level, gm):
        head_cl, foot_cl, depth_yd = STEEL_SAILS[sid]
        head_w, foot_w = head_cl * CLOTH_IN_SAIL_FT, foot_cl * CLOTH_IN_SAIL_FT
        hung = gm[yard_heights[level]]
        depth = hung - gm[below[level]] if level in below else 3.0 * depth_yd
        area = round((head_w + foot_w) / 2.0 * depth * FT * FT)
        drop = depth * (head_w + 2.0 * foot_w) / (3.0 * (head_w + foot_w))
        centre = round(DATUM + (hung - drop) * FT, 1)
        table = round((head_w + foot_w) / 2.0 * 3.0 * depth_yd * FT * FT)
        return area, centre, head_cl, foot_cl, depth_yd, depth, table

    areas = {}
    for name, levels in BRACE_PLANS.items():
        for level, _ in levels:
            sid = sail_of(name, level)
            areas[sid] = cut(sid, level, geom[name])
    REPORT["square"] = areas

    # the after sail and the head, each cut first so that her rope can be scaled by her plain sail
    mizen = mizen_course_cut(mast_x["mizzen"], rake["mizzen"])
    bow = head_geometry(geom, mast_x, rake)
    plain = (
        sum(areas[s][0] for s in areas if not s.endswith(".royal"))
        + sum(h["area"] for sid, h in bow["sails"].items() if sid != "fore.staysail")
        + mizen["area"]
    )
    # her rope: the frigate's scaled by the root of her plain sail over the frigate's, so that a
    # line's rating grows with the sail it works (Bel-D §4.3; judgement, as the 64's)
    rope_scale = math.sqrt(plain / FRIGATE_PLAIN_SAIL_M2)
    REPORT["rope"] = (plain, rope_scale)

    yards_by_level = {"course": [], "topsail": [], "topgallant": [], "royal": []}
    sails_by_level = {"course": [], "topsail": [], "topgallant": [], "royal": []}
    prov = " Provisional (truth 9), see gen_ships.py."
    for name in ("fore", "main", "mizzen"):
        gm = geom[name]
        x_ft, heel, _r = MASTS[name]
        x = mast_x[name]
        lv = {lvl: areas[sail_of(name, lvl)] for lvl, _ in BRACE_PLANS[name]}
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
            carried["lower"].append((mizen["area"], mizen["centre"], "gaff"))
        source = (
            "Lavery 1985 p. 19, Table 10, Dragon's, the main read as 36 yards (Bel-D §4.1)"
            if name == "main"
            else "Lavery 1985 p. 19, Table 10, Dragon's"
        )
        lower = b.spar(
            f"{name}.mast",
            "mast",
            x_m=x,
            rake_deg=rake[name],
            height_m=g.ft(gm["above"]),
            rating_kn=g.design_kn(carried["lower"], g.DESIGN_WIND_KN["lower"]),
            note=f"{name} lower mast {fmt_ft(gm['length'])} ({source}), its head "
            f"{fmt_ft(gm['head'])} by Steel's rule; its heel {heel:.2f} ft above the keel's top "
            f"and its place at the upper deck {x_ft:.2f} ft from AP, raking {rake[name]} deg "
            "(measured, ZAZ1357 and ZAZ1359: Bel §5.2)"
            + (
                ", carried 1 ft 2 in aft of the sheer draught's place by the Arrogant alteration "
                "ZAZ1359 notes 'for the Bellerophon' (read: Bel §5.2)"
                if name == "fore"
                else ""
            )
            + f".{prov}",
        )
        top = b.spar(
            f"{name}.topmast",
            "topmast",
            steps_on=lower,
            height_m=g.ft(gm["t_hoist"]),
            rating_kn=g.design_kn(carried["topsail"], g.DESIGN_WIND_KN["topsail"]),
            note=f"{name} topmast {fmt_ft(gm['t_len'])} (Lavery 1985 Table 10), its hoist above "
            f"the lower cap the length less the lower mast head, its head {fmt_ft(gm['t_head'])} "
            f"by Steel's rule.{prov}",
        )
        tg_source = (
            "Steel's 24 ft 6 in scaled 0.973, Table 10 having no mizen topgallant (Bel-D §4.1)"
            if name == "mizzen"
            else "Lavery 1985 Table 10"
        )
        tg = b.spar(
            f"{name}.topgallant_mast",
            "topgallant_mast",
            steps_on=top,
            height_m=g.ft(gm["g_hoist"]),
            rating_kn=g.design_kn(carried["topgallant"], g.DESIGN_WIND_KN["topgallant"]),
            note=f"{name} topgallant mast {fmt_ft(gm['g_len'])} ({tg_source}) with its royal pole, "
            "one stick: its height the listed length less its square head of 3 1/2 in to a yard, "
            "up to the stop, above the topmast cap; Steel's long pole-head, two-thirds of the "
            "length to the stop, set up from the stop above it (Steel 1794 vol. I p. 16, OCR l. "
            "2934-2942, and p. 42, OCR l. 4701-4702, read as Bel-D §4.2 reads them, judgement; the "
            "owner's 'Agreed', Bel-D §17.0)."
            f"{prov}",
        )
        royal = b.spar(
            f"{name}.royal_mast",
            "royal_mast",
            steps_on=tg,
            height_m=g.ft(gm["r_hoist"]),
            rating_kn=g.design_kn(carried["royal"], g.DESIGN_WIND_KN["royal"]),
            note=f"{name} royal pole, the topgallant mast's own long pole-head (Steel 1794 vol. I "
            "p. 16 and p. 42; Bel-D §4.2), filed as a royal mast stepped on it as the frigate-36 "
            f"files hers, so that the royal yard has its own spar.{prov}",
        )
        on_spar = {"course": lower, "topsail": top, "topgallant": tg, "royal": royal}
        factor = g.FRIGATE_MAST_ROPE_FACTOR[name] * rope_scale
        for level, limit in BRACE_PLANS[name]:
            yard_id = f"{name}.{level}.yard" if level != "course" else f"{name}.yard"
            sail_id = sail_of(name, level)
            area, centre, head_cl, foot_cl, depth_yd, _depth, table = areas[sail_id]
            yard_src = (
                "Steel 1794 vol. I p. 49, the 74 (Table 10 has none)"
                if level == "royal" or (name == "mizzen" and level == "topgallant")
                else "Lavery 1985 Table 10"
            )
            yard = b.spar(
                yard_id,
                "yard",
                on=on_spar[level],
                length_m=g.ft(gm[yard_lengths[level]]),
                height_m=g.ft(gm[yard_heights[level]]),
                brace_limit_deg=limit,
                rating_kn=g.design_kn(
                    carried[level_of_spar[level]], g.DESIGN_WIND_KN[level_of_spar[level]]
                ),
                note=f"{name} {level} yard {fmt_ft(gm[yard_lengths[level]])} ({yard_src}); braces "
                f"{limit} deg from square (the frigate-36's, Fincham 1843 art. 102; as the owner "
                f"kept them for the 64, 2026-10-29: Bel-D §4.3).{prov}",
            )
            reef = REEFS[level] if not isinstance(REEFS[level], dict) else REEFS[level][name]
            canvas = g.FRIGATE_CANVAS[sail_id]
            if level in ("topgallant", "royal"):
                how = (
                    "cut between its yard and the yard below as the spars stand on Steel's long "
                    "pole-heads (Bel-D §4.2), on Steel's cloths "
                    f"({head_cl:g} at the head, {foot_cl:g} at the foot): the spars rule over the "
                    "sail table (the owner's answer, Build-Ships.md §19.1 item 5), short of table "
                    f"IV's {depth_yd:g} yards deep"
                )
            else:
                how = (
                    f"Steel's table IV, the 74: {head_cl:g} cloths at the head, {foot_cl:g} at the "
                    f"foot, {depth_yd:g} yards deep, 22 1/2 in a cloth in the sail (Bel §5.6; "
                    f"unscaled, Bel-D §4.4); {reef} reef band{'s' if reef != 1 else ''} (Steel)"
                )
            sail = b.sail(
                sail_id,
                "square",
                yard=yard,
                area_m2=area,
                reef_bands=reef,
                flying=True if level == "royal" else None,
                x_m=g.raked_x(x, rake[name], centre, deck_m=DATUM),
                centre_height_m=centre,
                canvas_no=canvas[0],
                cloth_rating_kn=g.cloth(area, canvas[0]),
                note=f"{name} {level}: {how}."
                + (" Set flying (Steel 1794 vol. I p. 214)." if level == "royal" else "")
                + g.canvas_note(canvas),
            )
            sizes = {cls: g.quarter(c * factor) for cls, c in g.FRIGATE_ROPE[level].items()}
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
        shrouds = SHROUDS[name]
        shroud_size = g.quarter((9.5 if name != "mizzen" else 6.5) * rope_scale)
        b.sided(
            f"{name}.shrouds",
            "shroud",
            lower,
            rating=g.rope_kn(shroud_size, shrouds),
            note=f"{shrouds} shrouds a side, the 64's count (judgement: her channels' deadeyes not "
            "counted); the frigate-36's size scaled by her rope (judgement).",
        )
        bs_size = g.quarter((6.0 if name != "mizzen" else 4.5) * rope_scale)
        b.sided(f"{name}.topmast.backstay", "backstay", top, rating=g.rope_kn(bs_size, 2))

    gz = geom["mizzen"]
    b.spar(
        "mizzen.crossjack.yard",
        "yard",
        on="mizzen.mast",
        length_m=g.ft(gz["yard"]),
        height_m=g.ft(gz["yard_h"]),
        brace_limit_deg=CROSSJACK_BRACE_DEG,
        rating_kn=g.design_kn(
            [(areas["mizzen.topsail"][0], areas["mizzen.topsail"][1], "square")],
            g.DESIGN_WIND_KN["lower"],
        ),
        note=f"crossjack yard {fmt_ft(gz['yard'])} (Lavery 1985 Table 10); crosses no sail, "
        f"spreads the mizzen topsail's foot; braces {CROSSJACK_BRACE_DEG} deg from square (the "
        "frigate-36's; judgement).",
    )
    b.sided(
        "mizzen.crossjack.yard.brace",
        "brace",
        "mizzen.crossjack.yard",
        rating=g.rope_kn(g.quarter(5.0 * g.FRIGATE_MAST_ROPE_FACTOR["mizzen"] * rope_scale)),
    )
    b.sided(
        "mizzen.crossjack.yard.lift",
        "lift",
        "mizzen.crossjack.yard",
        rating=g.rope_kn(mizzen_lift_in(rope_scale)),
        note="the crossjack's lifts, as a course's (judgement): every yard's lifts are carried, "
        "and drawn (the owner's answer, Build-Ships.md §19.1 item 7).",
    )

    # -- the after sail: the mizen course cut at the mast and the driver in its place
    # ---------------
    after_sail = mizen_course(b, mizen, rope_scale)
    driver_sail = None
    if DRIVER:  # the course filed first, so that the yard's sail stays it (Ext §17.2)
        d = driver_cut(mizen["cut"], mast_x["mizzen"], rake["mizzen"])
        driver_sail = mizen_driver(b, d, rope_scale)
        REPORT["driver"] = d
    REPORT["after_sail"] = mizen

    # -- the head --------------------------------------------------------------------------------
    headsails = write_head(b, bow, rope_scale)
    sprit_sails = head_yards(b, bow, rope_scale)
    REPORT["head"] = bow

    # -- the stays the masts stand by (the frigate's, scaled; judgement) ---------------------------
    for sid, of, size, text in (
        (
            "fore.stay",
            "fore.mast",
            15.0,
            "to a collar half way out the bowsprit's outboard part (judgement); the fore staysail "
            "and the fore storm staysail set on it",
        ),
        ("main.stay", "main.mast", 16.0, None),
        ("main.topmast.stay", "main.topmast", 7.5, None),
        (
            "mizzen.stay",
            "mizzen.mast",
            10.0,
            "from the mizen mast head to a collar on the main mast twelve feet above the "
            "quarterdeck (Steel 1794 vol. I, 'Mizen-stay'); the mizzen storm staysail sets on it",
        ),
    ):
        size = g.quarter(size * rope_scale)
        b.line(
            sid,
            "stay",
            of,
            rating=g.rope_kn(size),
            note=f"the frigate-36's scaled by her rope (judgement){'; ' + text if text else ''}.",
        )

    # -- the staysails between the masts --------------------------------------------------------
    between = between_the_masts(b, geom, mast_x, rake)
    cut_areas = {s["id"]: s["area_m2"] for s in b.doc["sails"]}
    for sid in between:
        b.notes[sid] += steels_staysail_words(sid, cut_areas[sid])

    # -- the studding sails, the storm canvas and the occasional sails ----------------------------
    stuns = studding_sails(b, geom, mast_x, rake, rope_scale)
    storm = storm_canvas(b, geom, mast_x, rake, bow, after_sail, rope_scale)
    saves = save_alls(b, mast_x, rope_scale)

    # -- groups (the frigate-36's set, with the names the engine reads: Bel-D §4.8) ---------------
    square = sum(sails_by_level.values(), [])
    b.group("courses", sails_by_level["course"])
    b.group("topsails", sails_by_level["topsail"])
    b.group("topgallants", sails_by_level["topgallant"])
    b.group("royals", list(sails_by_level["royal"]))
    b.group("headsails", headsails)
    b.group("jibs", ["jib"])
    b.group("staysails", headsails[:2] + between)
    b.group("staysails between the masts", between)
    b.group("studdingsails", stuns)
    b.group("square sails", square)
    b.group("fore-and-aft sails", headsails + between + [after_sail])
    light_staysails = [s for s in between if s not in ("main.staysail", "mizzen.staysail")]
    b.group("light sails", sails_by_level["royal"] + light_staysails + stuns)
    b.group("lying-to staysails", ["main.staysail"])
    # the polar reads this group alone (world/ships.py): courses, topsails, topgallants, the fore
    # topmast staysail and the jib, and the mizen course, as the frigate's
    b.group(
        "plain sail",
        sails_by_level["course"]
        + sails_by_level["topsail"]
        + sails_by_level["topgallant"]
        + headsails[1:]
        + [after_sail],
    )
    b.group("all sail", square + headsails + between + [after_sail] + stuns + sprit_sails)
    if sprit_sails:  # their own group, which the engine does not read (Ext §4.1)
        b.group("spritsails", sprit_sails)
    for name in ("fore", "main", "mizzen"):
        b.group(
            f"{name} yards",
            [y for lvl in yards_by_level for y in yards_by_level[lvl] if y.startswith(name + ".")]
            + (["mizzen.crossjack.yard"] if name == "mizzen" else []),
        )
    b.group(
        "yards",
        [y for lvl in yards_by_level for y in yards_by_level[lvl]] + ["mizzen.crossjack.yard"],
    )
    b.group("lower yards", yards_by_level["course"] + ["mizzen.crossjack.yard"])
    b.group("topsail yards", yards_by_level["topsail"])
    b.group("topgallant yards", yards_by_level["topgallant"])
    b.group("royal yards", yards_by_level["royal"])
    b.group(
        "head yards",
        [y for lvl in yards_by_level for y in yards_by_level[lvl] if y.startswith("fore.")],
    )
    b.group(
        "after yards",
        [y for lvl in yards_by_level for y in yards_by_level[lvl] if not y.startswith("fore.")]
        + ["mizzen.crossjack.yard"],
    )
    b.group("lower masts", ["fore.mast", "main.mast", "mizzen.mast"])
    b.group("topmasts", ["fore.topmast", "main.topmast", "mizzen.topmast"])
    b.group(
        "topgallant masts",
        ["fore.topgallant_mast", "main.topgallant_mast", "mizzen.topgallant_mast"],
    )
    b.group("royal masts", ["fore.royal_mast", "main.royal_mast", "mizzen.royal_mast"])
    # aliases: what an officer of 1795 would say (Falconer 1780; Lever 1827), the frigate-36's and
    # the 64's; the first a part has is its name in the log (evolutions/runner.py, part_name)
    for word in ("mizzen course", "mizen course", "mizzen", "mizen"):
        b.alias(word, "mizzen.course")
    for word in ("mizzen yard", "mizen yard"):
        b.alias(word, "mizzen.yard")
    if driver_sail:
        for word in ("driver", "spanker", "driver boomsail"):
            b.alias(word, driver_sail)
        for word in ("driver boom", "spanker boom"):
            b.alias(word, "mizzen.boom")
    b.alias("foresail", "fore.course")
    b.alias("mainsail", "main.course")
    b.alias("fore yard", "fore.yard")
    b.alias("main yard", "main.yard")
    b.alias("crossjack yard", "mizzen.crossjack.yard")
    b.alias("cro'jack yard", "mizzen.crossjack.yard")
    b.alias("crossjack", "mizzen.crossjack.yard")
    if sprit_sails:  # the period's words; "spritsail" and its yard are their ids'
        for word in ("sprit topsail", "spritsail topsail"):
            b.alias(word, "sprit_topsail")
        for word in ("sprit topsail yard", "spritsail topsail yard"):
            b.alias(word, "sprit_topsail.yard")
    b.alias("fore staysail", "fore.staysail")
    b.alias("fore topmast staysail", "fore.topmast_staysail")
    b.alias("main topmast staysail", "main.topmast_staysail")
    b.alias("main staysail", "main.staysail")
    b.alias("main topgallant staysail", "main.topgallant_staysail")
    for word in ("mizzen", "mizen"):
        b.alias(f"{word} staysail", "mizzen.staysail")
        b.alias(f"{word} topmast staysail", "mizzen.topmast_staysail")
    b.alias("stuns'ls", "studdingsails")
    b.alias("studding sails", "studdingsails")
    b.alias("kites", "studdingsails")
    b.alias("head sails", "headsails")
    b.alias("topgallant sails", "topgallants")
    b.alias("upper yards", "topgallant yards")
    # the sail room's own canvas (milestone 3b): "storm canvas" and "occasional sails" are the
    # groups freesail.ship.parts reads for the muster's sail-room line
    b.group("storm canvas", storm)
    b.group("storm staysails", storm[:2])
    b.group("occasional sails", ([driver_sail] if driver_sail else []) + saves)
    b.group("save-alls", saves)
    b.alias("save-all", "save-alls")
    for (name, level), _ in STUDDING.items():
        b.group(
            f"{name} {level} studdingsails", [f"{name}.{level}.studdingsail.{s}" for s in g.SIDES]
        )
    for name in ("fore", "main"):
        for cls in ("sheet", "tack", "bowline"):
            b.group(f"{name} {cls}s", [f"{name}.course.{cls}.{s}" for s in g.SIDES])
            b.alias(f"{name} {cls}", f"{name} {cls}s")
    for name in ("fore", "main", "mizzen"):
        b.group(f"{name} topsail bowlines", [f"{name}.topsail.bowline.{s}" for s in g.SIDES])
        b.alias(f"{name} top bowline", f"{name} topsail bowlines")

    # -- the ground tackle, the company, the guns and the stores (Bel-D §5-§7), in the 64's
    # order; her description at far detail (§8) -------------------------------------------------
    fits = her_fits(hull["profile"])
    check_fits(fits, hull["profile"])
    guns = default_guns(fits)
    ground_tackle(b)
    company(b, guns)
    armament(b, fits)
    quarter_bill(b, guns)
    flag_party(b)
    check_company(b)
    boats_pumps_hold(b)
    b.descriptions([DESCRIPTION])
    b.timing(LIE_A_TRY_NOTE, {"lie_a_try": {"helm_deg": LIE_A_TRY_HELM_DEG}})
    b.dump(os.path.join(out_dir, "seventy-four.yaml"), HEADER)


def her_report() -> str:
    """The generator's report: what her rules compute from the file's own keys, printed as the file
    is written and held by her tests, so that it does not stand in the file's notes to go stale (the
    lead's notes of 2026-10-29, item 2)."""
    out = [f"seventy-four: {line}" for line in REPORT.get("hull", ())]
    measured = REPORT.get("measured", [])
    out.append(
        "seventy-four: port triples measured on the traced body plan, asserted within 0.05 m of "
        f"the drawn side: {len(measured)} (" + ", ".join(f"{w} {x:g}" for w, x in measured) + ")."
    )
    if "rope" in REPORT:
        plain, scale = REPORT["rope"]
        out.append(f"seventy-four: plain sail {plain:.0f} m2, her rope's scale {scale:.3f}.")
    sq = REPORT.get("square", {})
    for sid, (area, centre, _h, _f, _d, depth, table) in sq.items():
        if sid.endswith((".topgallant", ".royal")):
            out.append(
                f"seventy-four: {sid}: {area} m2 cut to the spars, {depth / 3.0:.2f} yards deep "
                f"against table IV's ({table} m2), {area / table:.0%} of it; centre {centre} m."
            )
    mz = REPORT.get("after_sail")
    if mz:
        out.append(
            f"seventy-four: mizen course: tack {mz['corners'][0][1]:.2f} m above her water, "
            f"{(mz['corners'][0][1] - mz['deck']) / FT:.1f} ft above her poop's middle line at the "
            f"mast; its foot {mz['clear']:.2f} m over that line, at the least; {mz['area']} m2, "
            f"centre {mz['centre']} m; throat {mz['corners'][1][1]:.2f} m."
        )
        for words, o in mz["others"].items():
            out.append(
                f"seventy-four: mizen course, the other reading, {words}: tack {o['tack']:.2f} m, "
                f"its foot {o['clear']:.2f} m over the poop's middle line, {o['area']:.0f} m2, "
                f"centre {o['centre']:.2f} m."
            )
    d = REPORT.get("driver")
    if d:
        out.append(
            f"seventy-four: driver: jaws {d['boom']['jaws_z']:.2f} m, set by the {d['set_by']} at "
            f"{d['head_room_ft']:g} ft of head room; fore leech {d['fore_leech']:.2f} m, after "
            f"leech {d['after_leech']:.2f} m (Steel's band "
            f"{d['after_band'][0]:.2f}-{d['after_band'][1]:.2f}); {d['area']:.0f} m2 against "
            f"Steel's {d['steel_area']:.1f}; centre {d['centre']:.2f} m; {d['beyond_yard']:.2f} m "
            f"beyond the yard's peak; the boom {d['boom']['jaws_z'] - d['taffrail'][1]:.2f} m over "
            "the taffrail's crown."
        )
    hd = REPORT.get("head")
    if hd:
        out.append(
            f"seventy-four: bowsprit: {hd['inboard']:.1f} ft inboard along its steeve, "
            f"{hd['outboard']:.1f} ft outboard; its end {hd['tip'][1]:.2f} m above her water."
        )
        for sid, h in hd["sails"].items():
            out.append(f"seventy-four: {sid}: {h['area']} m2, {h['fit']:.0%} of Steel's sides.")
    st = REPORT.get("sprit", {})
    if "sprit_topsail" in st:
        s = st["sprit_topsail"]
        along, head, foot = REPORT["sprit_drawn"]
        out.append(
            f"seventy-four: sprit topsail: {s['area']:.0f} m2; the yards {s['gap']:.2f} m apart by "
            f"height, {s['slant']:.2f} m along the slant, {along:.2f} m as filed; drawn head "
            f"{head:.2f}, foot {foot:.2f}."
        )
        out.append(
            f"seventy-four: spritsail: foot {st['spritsail']['foot_z']:.2f} m above her water."
        )
    for name, (pieces, lb, men) in REPORT.get("fits", {}).items():
        out.append(
            f"seventy-four: fit '{name}': {pieces} pieces, a broadside of {lb} lb by 70's rule, "
            f"{men} men at one side's guns."
        )
    if "bill" in REPORT:
        seamen, men, marines_at, total, kept = REPORT["bill"]
        out.append(
            f"seventy-four: the quarter bill on '{DEFAULT_FIT}': her {seamen} seamen, {men} men at "
            f"the guns, {marines_at} of them marines at the carronades, and {HELM} at the wheel "
            f"leave {total} trimmers; the bill keeps {kept} marines in their division."
        )
    return "\n".join(out)


def build(out_dir: str) -> None:
    """Write her file to `out_dir`, `seventy-four.yaml`, through `write()`; Bel-D §1.5's checks
    raised before it is written."""
    REPORT.clear()
    write(out_dir)
    print(her_report(), file=sys.stderr)
