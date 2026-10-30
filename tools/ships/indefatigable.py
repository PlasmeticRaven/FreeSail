"""HMS *Indefatigable*, the 64 of 1784 and the razee of 1795 (package 75, the first ship; her
builder B1).

Her design is docs/design/Design-Ship-Indefatigable.md (cited here as Indf), from the research
note docs/design/Research-Indefatigable-2026-10.md (Ind) and the owner's answers
(docs/design/Decisions-ShipsRound2-2026-10.md; docs/design/Build-Ships.md §19.1). One module
writes two files, the 64 first and the razee derived from her as data (Indf §1): `sixty_four()`
gives the 64's particulars, `write(out_dir, p)` builds and dumps one file from them, and
`build(out_dir)` is the generator's hook (`tools/gen_ships.py`, `SHIP_MODULES`). `razeed(p)`
derives the razee from the 64's particulars by the dockyard's steps, and the same `write()`
builds her file (Indf §1.5). Built so far (Indf §13, steps 1 to 5): both hulls, profiles and
sills, masts, yards with their lifts, square sails, the 64's stand-in mizen course and the
razee's spanker, the head, the staysails between the masts, the studding sails, the storm and
occasional canvas, the groups and the aliases; the fits with their guns on the profile's ports,
the magazines, the company and the quarter bill, the people drawn from her wardroom files
(data/people/sixty-four.yaml, razee-44.yaml), the stores, the sail room, the ground tackle, the
boats, the pumps, the hold and her description at far detail. Step 6 tuned each hull's centre
of lateral resistance against the helm's truths and measured both polars
(docs/dev/TuningNotes.md); her tests and her truths are tests/test_indefatigable.py. The refinement
of stage A (the lead's notes of 2026-10-29, item 7; Indf §3.5 item 9 and §17's answers of that
day) separated the stem's fore edge from the knee of the head, ended the rail where her side
ends at the beakhead, cut four of the staysails between the masts to Steel's table IV and left
out the mizen topgallant staysail, and recorded the owner's answers where they bear.

**Her shape (stage B's step 7, taken first as the hull's pilot: Build-Ships.md §2.6; Indf §3.5
item 8).** Both files carry the shape keys of stage 0H through `g.hull_profile` and
`g.hull_form` (`hull_block`): her waterlines by station as sourced section points, her main
breadth at its drawn height, her channel wale, the knee of the head, the square stern with its
quarter galleries and lights, the figure on the head, and every line's rung. They are drawn
only: no figure the physics, the guns or the lee ports read is taken from them, and no port
triple is written from the drawing (Build-Ships.md §5.0 principle 8); each port's gap to the
drawn side is in the generator's report (`her_report`).

**Her rig at stage B (Indf §13 step 7; the lead's notes of 2026-10-29, item 2).** Her mizen
course cut at the mast on her whole mizen yard and Steel's driver in the sail room in its place
(`tools/ships/mizen_yard.py`; `MIZEN_COURSE`, `DRIVER`); the yards under the bowsprit
(`tools/ships/spritsail_yards.py`; `BOWSPRIT_YARDS`), the 64's two and the razee's spritsail
yard; the bowsprit rooted on the stem head at her 27 degrees, the jib-boom and the stays' leads
following; her topgallants and royals by Steel's long pole-heads (pp. 16, 42), both files, the
razee's upper masts being the 64's; and the clew check: the 64's course and driver's boom clear of
her roundhouse deck and the razee's spanker boom clear of her short roundhouse, each by the head
room (`HEAD_ROOM_FT`).

**Her notes (the lead's notes of 2026-10-29, item 2).** The files' notes carry sources, departures
and judgements. A figure a rule computes from the file's own keys (a drawn displacement, a port's
gap, an area from a cut, a rating, a rope's size, a count of men) is printed by `her_report()`, the
generator's report, and held by her tests, where it cannot go stale; what her tuning measured is
in docs/dev/TuningNotes.md. `HerBuilder` keeps the shared helpers' such figures out of her notes,
and no note of the eight is touched.

**The owner's two changes of 2026-10-29, the razee's alone (the 64's file byte for byte as it
was).** D18 (c): her datum is her old upper deck at midships, not her gun deck (`the_datum`;
Indf §2.2), her rig cut where (a) cut it and written above the new datum (`Particulars.frame_z`,
`above_datum`, `mast_x_at_datum`), so that nothing above her water moves; what moves is what
reads the datum or a height written above it, the deck's wind's eye, the lower masts' windage,
the blanket's reach and the spanker sheet's lead (`her_hull`, deck_height_m's note). Her short
roundhouse, as she was in 1796 (Build-Ships.md
§19.1 item 18): the 64's quarterdeck kept over her cabin from her stern to the beam abaft the
mizen, its rail, her taffrail on the 64's stern line and her stern up to it, measured on ZAZ2371
and ZAZ2375 where they give them (`RAZEE_ROUNDHOUSE_FT`, `the_upper_works`), so that her stern
lights and quarter gallery stand under her taffrail where her cabin is. Neither moves a gun, a
fit or how she sails but by the datum the owner chose.

The module is imported only by the generator's entry block, after `gen_ships` is made the
running script, and takes every helper as `g.<name>` (Indf §1.2). No function or table of the
generator is changed; the eight files stay byte for byte as they are.

**The frame (Indf §1.4).** The figures at the top are in the drawings' own frame, as the sources
give them: feet forward of the after perpendicular (AP), feet above K (the bottom of the band
under the keel), or feet above WL1, the 64's load line, where a measure was taken from it. They
are converted once: x in metres forward of the middle of the load waterline, 80 ft forward of AP;
z in metres above the variant's own load water at that station (the water is inclined to the
keel by the drawn drag, and the engine has no trim). A spar's `height_m` and a sail's
`corners_m` are then taken above the datum, the D18 line at midships (the 64's upper deck; the
razee's old upper deck, D18 (c)), as the file's convention has them, and a lower mast's `x_m` is
its place at that height; a sail's centre and a gun's height stay above the water. The rig is
cut above the deck she is worked from at midships, her frame, which is the datum but in the
razee's (her gun deck), and written above the datum from there.

**The gates (Indf §0).** Three flips hold what waited on the engine extensions, each a
change of its own: `MIZEN_COURSE` ("gated", the lateen cut at the mast; "stand-in", stage A's
loose-footed gaff-class sail on the after part of her mizen yard), `BOWSPRIT_YARDS` (False
writes no yards under the bowsprit) and `DRIVER` (the driver boomsail the owner chose: Indf
§4.4; the engine design's §17; only with the gated course). Every id is final from stage A, so
stage B renames nothing.

Marks as the design's: measured (on the held page images, or arithmetic on the notes' measured
figures), read, read (OCR), judgement. The measurements of Indf §3.5 were taken on the held
images (ZAZ1407 at full resolution, ZAZ1280 at 3840 px) by the research's method, the checker's
registration of ZAZ1407 (AP at 7405.9 px, 99.97 px to the foot, WL1 and K fitted lines); the
images are not in the repository. Taken: items 1, 5, 6 and 7, and the 64's part of items 2
and 3. Not taken: the half-breadth at each port's sill on 1407T's body plan (item 2), and on
ZAZ2371, whose 1280 px give about 6 1/2 px to the foot, the razee's head and forecastle rail
(item 3) and her quarterdeck and forecastle sills (item 4); those figures are judgement on the
64's measured lines, and their notes say so. Her roundhouse, its rail and her taffrail were
measured on ZAZ2371 on 2026-10-29 (`RAZEE_ROUNDHOUSE_FT`).
"""

from __future__ import annotations

import math
import os
import re
import sys
from dataclasses import dataclass, replace

import gen_ships as g

from ships import mizen_yard, period, spritsail_yards

FT = g.FT

# Her stage-B flips (Indf §0; Ext §17.2), each a change of its own, measured old beside new.
# The 64's mizen course (Indf §4.4): "gated", the lateen cut at the mast on her whole mizen yard
# (Ext §3.4; `mizen_yard.course`), since the engine's lateen step (B3.1); "stand-in", stage A's
# loose-footed gaff-class sail on the yard's after part, kept to measure the step against.
MIZEN_COURSE = "gated"
# The yards under the bowsprit (D8 (b); Indf §4.6, §17 item 5 as answered; Ext §4.1;
# `spritsail_yards.cut`): the 64's spritsail and sprit-topsail yards and the razee's spritsail
# yard, since the engine keeps a yard under the bowsprit out of her head yards (B3.2).
BOWSPRIT_YARDS = True
# Steel's driver boomsail (Indf §4.4; Ext §17; `mizen_yard.driver`), the owner's choice of
# 2026-10-28: in the sail room, in the mizen course's place, with its boom; the 64's alone, and
# only with the course cut at the mast (a lateen's yard must be a `lateen_yard`), since the
# engine's step B3.5.
DRIVER = True

# ---------------------------------------------------------------------------
# The drawings' frame: the load line and the decks
# ---------------------------------------------------------------------------

# WL1, the top green waterline of ZAZ1407, taken as the 64's load line: 21.22-21.27 ft above K
# at AP and 20.16-20.26 ft at 160 ft forward of it, the keel dragging 1.04 ft over the 160 ft
# (measured, 1407F and the checker: Ind §2.3.1). The mean of each band at AP and the drawn drag.
WL1_AT_AP_FT = 21.245
WL1_DRAG_FT = 1.04
# The middle of the load waterline, the file's x = 0: WL1 rabbet to rabbet, D29 (b) (Ind §2.4).
MIDSHIPS_FT = 80.0


def wl1_above_k(x_ft):
    """WL1's height above K at `x_ft` forward of AP, feet."""
    return WL1_AT_AP_FT - WL1_DRAG_FT * x_ft / 160.0


# The decks at the middle line, feet above K, at (ft from AP, ft above K): measured on ZAZ1280
# by the checker, ±0.4 ft for which edge of the drawn deck is its surface, agreeing with ZAZ1407
# and ZAZ2371 at midships to 3 in (Ind §2.3.5): aft at 2-6 ft, midships at 86-110 ft (taken at
# the middle of the load line, as Indf §3.2), forward at 140-150 ft. The 64's quarterdeck from
# the stern to its breast at 73.1-73.3 ft, ended here at 72.0 ft, where the side's scroll ends
# the quarterdeck's rail (measured on 1407F; the deck at the side is below its rail there); the
# forecastle from about 119.7 ft (Ind §2.3.5, measured, 1280T).
DECKS_64 = {
    "lower": [(4.0, 25.42), (80.0, 23.83), (145.0, 24.17)],
    "upper": [(4.0, 32.58), (80.0, 31.29), (145.0, 31.33)],
    "quarterdeck": [(4.0, 39.5), (72.0, 39.5 + (38.0 - 39.5) * (72.0 - 4.0) / (73.2 - 4.0))],
    "forecastle": [(119.7, 37.55), (145.0, 37.55)],
}

# ---------------------------------------------------------------------------
# The ports and their sills (Indf §3.3, §3.5 item 1): (ft from AP, sill ft above WL1)
# ---------------------------------------------------------------------------

# The gun deck (the 64's lower deck): thirteen a side, centres and sills measured on ZAZ1407 at
# full resolution by the checker's method (each port's box found by its edges, its sill a dark
# run's centroid, the height above WL1 at the port's own x), all thirteen: the five Ind §2.3.7
# gives (6.09, 5.35, 5.02, 5.30, 6.03 ft at ports 1, 4, 7, 10 and 13 from aft) found again to the
# hundredth, the eight between measured where Indf §3.3 interpolated them (within 0.02 m of it).
# Each port 3 ft 2 in-3 ft 4 in wide and 2 ft 8 in deep (measured: 3.27 by 2.66 ft the mean).
LOWER_SILLS = [
    (10.80, 6.09),
    (21.93, 5.79),
    (33.03, 5.55),
    (44.12, 5.35),
    (55.25, 5.20),
    (66.32, 5.10),
    (78.82, 5.02),
    (89.88, 5.08),
    (100.99, 5.16),
    (112.10, 5.30),
    (123.24, 5.50),
    (134.38, 5.72),
    (145.32, 6.03),
]
LOWER_PORT_FT = (3.27, 2.66)
# The 64's upper deck: thirteen a side at Ind §2.3.7's centres, all thirteen sills measured on
# 1407F at full resolution by the same finder (Ind's "11 ft 11 in at midships, not re-measured"
# is port 5's 11.90; the midship ports stand at 11.67-11.74). 2.80 by 2.61 ft the mean.
UPPER_SILLS = [
    (6.00, 12.96),
    (16.62, 12.64),
    (27.44, 12.34),
    (38.57, 12.10),
    (49.68, 11.90),
    (60.79, 11.77),
    (71.72, 11.69),
    (84.39, 11.67),
    (95.45, 11.74),
    (106.52, 11.88),
    (117.64, 12.07),
    (128.81, 12.29),
    (139.93, 12.59),
]
UPPER_PORT_FT = (2.80, 2.61)
# The 64's quarterdeck: six a side measured on 1407F at full resolution, the five of Ind
# §2.3.7 (about 21.5 to 60.8 ft, tentative there) and its doubtful sixth at about 12 ft, a clean
# box of the same size under the roundhouse; each cut down from the rail, 2.52 by 2.27 ft (the
# mean). Her fit's five a side are her guns' (Winfield 1793-1817 p. 99); the sixth is drawn.
QUARTERDECK_SILLS = [
    (11.91, 19.14),
    (21.40, 18.87),
    (32.30, 18.58),
    (41.77, 18.38),
    (51.18, 18.22),
    (60.72, 18.11),
]
QUARTERDECK_PORT_FT = (2.52, 2.27)
# The 64's forecastle: one a side at about 140.4 ft (Ind §2.3.7, measured on 1407T, tentative).
# On 1407F at full resolution no port is drawn there, the forecastle's rail standing 1 ft 3 in-
# 1 ft 9 in above its deck, so her forecastle gun fires over the rail (judgement); its sill the
# deck and 0.41 m (Indf §3.3, judgement), the quarterdeck's port size (judgement).
FORECASTLE_PORT_X_FT = 140.4
FORECASTLE_SILL_ABOVE_DECK_M = 0.41
# The class's carronades of 1794, never hers (Winfield 1793-1817 p. 99: two 24-pounders on the
# forecastle, six 18-pounders on the roundhouse; Indf §5.1), whose ports no draught of hers
# shows: the forecastle's one a side at +14.6 m, 127.9 ft from AP, and the roundhouse's three a
# side between -23 and -17 m, about 9 ft 10 in apart (Indf §5.1, judgement), their port size the
# quarterdeck's (judgement). The roundhouse's deck at the side 1 ft 3 in under its rail: on
# ZAZ1280 at 3840 px the line under the rail stands 1.20-1.27 ft below it from 4 to 32 ft from
# AP, measured from the quarterdeck's first port, whose sill and the rail above it agree with
# 1407F's within 0.05 ft (measured here; judgement that it is the deck), from abaft AP to the
# roundhouse's breast at 34.4 ft, where its rail's scroll ends (RAIL).
FORECASTLE_CARRONADE_X_FT = 127.9
ROUNDHOUSE_PORTS_FT = (4.54, 14.38, 24.23)
ROUNDHOUSE_BELOW_RAIL_FT = 1.25
ROUNDHOUSE_FT = (-10.61, 34.40)
# On a deck whose rail stands less than a port's sill above it (the 64's forecastle, its rail
# 1 ft 2 in-1 ft 9 in above the deck on 1407F, and her roundhouse), the gun fires over the
# rail: its sill taken 2 in under the rail, so that the gun's height is the rail's (judgement).
OVER_THE_RAIL_M = 0.05

# ---------------------------------------------------------------------------
# The side's half-breadths (Indf §3.3, §3.5 item 2): feet, moulded, at (ft from AP, hb)
# ---------------------------------------------------------------------------

# WL1's half-breadths (measured, 1407T and 1407F, the checker within 0.06-0.19 ft: Ind §2.3.2):
# 0.6 at the post, 12.19 to 21.75 between, 0.63 at 160 ft.
WL1_HALF_BREADTHS = [
    (0.0, 0.6),
    (10.0, 12.19),
    (20.0, 16.65),
    (30.0, 18.8),
    (40.0, 20.06),
    (50.0, 20.8),
    (60.0, 21.31),
    (70.0, 21.6),
    (80.0, 21.72),
    (90.0, 21.75),
    (100.0, 21.75),
    (110.0, 21.75),
    (120.0, 21.47),
    (130.0, 20.5),
    (140.0, 17.68),
    (150.0, 11.70),
    (155.0, 6.87),
]
# The half-breadth plan's main-breadth line, the hull's greatest breadth at each station, and
# its top-timber line, the breadth at the top of the side (16.96 ft at midships: the midship
# section's 17.0 at 34.6 ft above the rabbet, the waist rail's height); both tracked on 1407F at
# full resolution from midships both ways, read at round stations (measured here, ±0.1 ft).
MAIN_BREADTH = [
    (0.0, 13.44), (10.0, 15.56), (20.0, 17.45), (30.0, 19.04), (40.0, 20.18), (50.0, 20.85),
    (60.0, 21.31), (70.0, 21.61), (80.0, 21.72), (90.0, 21.74), (100.0, 21.74), (110.0, 21.74),
    (120.0, 21.46), (125.0, 21.12), (130.0, 20.55), (135.0, 19.64), (140.0, 18.33),
    (145.0, 16.37), (150.0, 13.60), (155.0, 9.44), (160.0, 2.95),
]  # fmt: skip
TOP_TIMBER = [
    (-5.0, 10.38), (0.0, 11.14), (10.0, 12.53), (20.0, 13.76), (30.0, 14.78), (40.0, 15.58),
    (50.0, 16.20), (60.0, 16.61), (70.0, 16.86), (80.0, 16.96), (90.0, 16.96), (100.0, 16.96),
    (110.0, 16.96), (120.0, 16.76), (125.0, 16.53), (130.0, 16.22), (135.0, 15.79),
    (140.0, 15.25), (145.0, 14.55), (150.0, 13.61), (155.0, 12.40),
]  # fmt: skip
# The plank outside the moulded lines, 4 1/2 in (Steel's 5-in plank, Ind §2.3.3; Indf §3.3).
PLANK_FT = 4.5 / 12.0
# At a gun-deck sill the side stands a little inside its greatest breadth: at midships the
# section is 21.52 ft at the sill against its dead flat's 21.65 (Ind §2.3.2; Indf §3.3, measured
# there), 0.13 ft, taken off the main-breadth line at every port (judgement on measured lines).
LOWER_SILL_INSIDE_BREADTH_FT = 21.65 - 21.52
# At an upper-deck sill the side stands between the two lines: at the midship sill (11.67 ft
# above WL1, 30.47 ft above the rabbet, WL1 18.8 ft above it: Ind §2.3.2, R1) the section gives
# 18.37 ft, 0.30 of the way from the top-timber line (16.96) to the dead flat (21.65); the same
# fraction taken at every port (judgement on measured lines). The quarterdeck's and the
# forecastle's sills, within 2 ft of the top of the side, take the top-timber line (judgement).
UPPER_SILL_FRACTION = (18.37 - 16.96) / (21.65 - 16.96)

# The midship section, ZAZ1407's outermost section (measured, 1407T, ±0.15 ft: Ind §2.3.2):
# (ft above the rabbet, half-breadth moulded); the rabbet 18.8 ft below WL1 at midships (R1).
SECTION = [
    (0.7, 4.0), (1.5, 10.4), (2.35, 12.5), (3.2, 13.9), (4.0, 15.0), (5.7, 16.5), (7.3, 17.7),
    (9.0, 18.8), (10.6, 19.7), (12.3, 20.5), (13.9, 21.0), (15.6, 21.4), (17.3, 21.65),
    (23.0, 21.65), (24.6, 21.4), (26.3, 20.8), (28.0, 19.9), (29.6, 18.75), (31.3, 18.0),
    (34.6, 17.0), (37.1, 16.1),
]  # fmt: skip
WL1_ABOVE_RABBET_FT = 18.8

# ---------------------------------------------------------------------------
# The profile's lines (Indf §3.2, §3.5 item 3)
# ---------------------------------------------------------------------------

# The top of the side, from the taffrail to where the side ends at the beakhead, (ft from AP, ft
# above WL1): measured on 1407F at full resolution, each line tracked along its drawn ink (the
# red alteration lines left out): the taffrail's crown 13 ft abaft AP, 28.0 ft above WL1 (49.3
# above K: Ind's "about 49 ft", tentative, now measured); the roundhouse's rail to its scroll at
# 34.8 ft; the quarterdeck's rail from 35 ft to its breast, its scroll at 72 ft; the waist rail,
# 15.8-16.0 ft (5 ft 4 in above the upper deck); the forecastle's rail from 119.6 ft to the
# beakhead bulkhead, read by columns from 147.5 ft (±0.03 ft) and taken straight across the
# timber heads between 145 and 147.5 ft, where the columns find no line. The bulkhead's edge,
# where her side ends, stands 153.3 ft from AP, upright from 17.8 to 19.0 ft above WL1
# (measured, 1407F at full resolution, row by row); forward of it is the head, not the side
# (Build-Ships.md §5.1: a two-decker's rail ends abaft the stem head, at a beakhead bulkhead;
# Indf §3.5 item 9). Stage A carried the rail on to the knighthead's cap at 160.8 ft
# (`KNIGHTHEAD_FT`); its refinement ended it at the bulkhead, extended from 144.8 ft on its own
# slope to 19.39 ft there, 0.11 ft under the line as read.
RAIL = [
    (-13.0, 28.0), (-10.61, 27.03), (-5.61, 26.43), (-0.61, 25.87), (4.39, 25.33), (9.39, 24.83),
    (14.40, 24.36), (19.40, 23.92), (24.40, 23.51), (29.40, 23.14), (34.40, 22.79),
    (35.0, 21.88), (40.0, 21.37), (44.0, 21.12), (48.01, 20.90), (52.01, 20.70), (56.01, 20.51),
    (60.81, 20.30), (64.0, 19.53), (68.0, 18.79), (70.0, 18.63), (72.0, 17.59), (72.4, 16.0),
    (76.0, 15.97), (90.0, 15.77), (100.0, 15.76), (110.0, 15.88), (119.3, 15.95),
    (119.6, 17.90), (122.0, 18.14), (126.0, 18.26), (130.0, 18.38), (134.0, 18.53),
    (138.0, 18.69), (142.0, 18.88), (144.8, 19.03), (147.5, 19.17), (150.0, 19.30),
    (153.3, 19.50),
]  # fmt: skip
BEAKHEAD_FT = 153.3
# The stem's fore edge, (ft from AP, ft above WL1), low to high: the foremost of the lines
# ZAZ1407 draws along the stem (the dashed bearding line and the rabbet's lines abaft it), where
# the gripe and the knee of the head are fayed to it; separated from the knee's fore edge here
# on 1407F at full resolution (tracked along its ink from the keel, then read row by row, ±0.05
# ft). Its foot is boxed into the keel 1.1 ft above K at 144.5 ft; it meets WL1 at 160.84 ft,
# 2.6 ft abaft the knee's fore edge (163.45), runs up behind the cheeks and the rails of the
# head, and ends at the top of the stem head's fore face, 16.0 ft above WL1 at 162.5 ft; the
# head's top falls aft from there under the bowsprit, parallel to it, drawn dashed behind the
# near knighthead. Stage A's stem ran on up the knee of the head (`KNEE_OF_THE_HEAD`).
STEM = [
    (144.5, -19.25), (145.7, -18.92), (146.9, -18.51), (148.1, -18.01), (149.3, -17.43),
    (150.5, -16.75), (151.7, -15.95), (152.9, -15.02), (154.1, -13.98), (155.3, -12.74),
    (156.68, -11.0), (157.37, -10.0), (157.97, -9.0), (158.50, -8.0), (159.38, -6.0),
    (160.02, -4.0), (160.47, -2.0), (160.84, 0.0), (161.14, 2.0), (161.39, 4.0), (161.61, 6.0),
    (161.82, 8.0), (162.05, 10.5), (162.23, 12.5), (162.36, 14.0), (162.52, 16.0),
]  # fmt: skip
STEM_HEAD_FT = STEM[-1]
# The knee of the head's fore edge, (ft from AP, ft above WL1), low to high, kept here for
# `head_m` at stage B (Build-Ships.md §5.1; Indf §3.5 items 8 and 9) and not written into her
# files before then: the gripe's, the cutwater's and the knee's fore edge, from the band's
# square fore end at about 147.75 ft, where the gripe meets K ahead of the stem's foot, to WL1
# at 163.45 ft as Ind §2.3.6 measures it (1407F, ±0.05-0.15 ft); above it measured on 1407F at
# full resolution by rows to the head's top at 20 ft (174.5 ft from AP). This was stage A's
# `stem_m`.
KNEE_OF_THE_HEAD = [
    (147.75, None), (150.25, -19.7), (151.8, -19.1), (152.75, -18.6), (154.55, -17.1),
    (155.45, -16.1), (156.2, -15.1), (157.4, -13.1), (158.4, -11.1), (159.7, -8.1),
    (160.95, -5.1), (162.3, -2.1), (163.45, 0.0), (164.68, 2.0), (167.56, 5.0), (171.16, 8.0),
    (172.91, 10.0), (173.91, 12.0), (174.31, 14.0), (174.40, 16.0), (174.53, 18.0),
    (174.46, 20.0),
]  # fmt: skip
# The near knighthead: the post ZAZ1407 draws standing up before the bowsprit beside the stem
# head, its after face 160.8 ft from AP and its moulded cap 20.0 ft above WL1 (measured, 1407F
# at full resolution). Stage A read it as the stem head's block and rooted the bowsprit at its
# cap. On 1407F the bowsprit's drawn edges (29 degrees, 2 ft 6 in apart) put its axis about 4
# ft lower at that x, lying on the stem head: at stage B (Indf §3.5 item 9; Ext §6.2 as built)
# the bowsprit is rooted there, on the stem head (`STEM_HEAD_FT`; `head_geometry`), where the
# viewer draws its heel.
KNIGHTHEAD_FT = (160.8, 20.0)
# The post's after face (Ind §2.3.6: 0.08 ft before AP at the heel, 1.24 ft abaft it at WL1,
# raking 3.5 degrees) and above it the counter and the stern to the taffrail, (ft from AP, ft above
# WL1), measured on 1407F at full resolution by rows (the stern's outline, the quarter gallery's
# carvings and the rudder left out; ±0.3 ft).
STERN = [
    (0.08, None), (-1.24, 0.0), (-1.79, 8.0), (-4.14, 10.0), (-6.60, 12.0), (-7.84, 14.0),
    (-8.37, 16.0), (-9.14, 18.0), (-9.52, 20.0), (-10.25, 22.0), (-10.68, 24.0), (-11.0, 26.0),
    (-11.62, 27.0), (-13.0, 28.0),
]  # fmt: skip
# K under the post's heel and at the band's square fore end (Ind §2.3.6).
KEEL_FT = (0.08, 147.75)
# The main wale, (ft from AP, its lower edge and its upper edge ft above WL1): both edges tracked
# on 1407F at full resolution by columns (±0.05 ft), the lower drawn heavy, from where it sweeps
# up into the counter to the stem; 4 ft 3 in broad, its lower edge 10 in below WL1 at 85-90 ft
# (19.9-24.1 ft above K), rising 3 ft 9 in to the stem and 6 ft 0 in aft (measured here). Abaft
# 6 ft its upper edge runs under the quarter gallery's lower finishing, and is held at its
# height there (judgement); forward of 154.5 ft the lower cheek of the head lies along it.
# ZAZ2371 measures it 20.2-24.7 ft above K at midships (Ind §2.3.5, at about 6 px to the foot),
# which stage A carried along parallel to the gun deck's sills (judgement), a nearly flat band
# from 10.8 to 145.3 ft.
MAIN_WALE_FT = [
    (1.0, 5.22, 7.60), (2.0, 4.61, 7.60), (4.0, 3.96, 7.60), (6.0, 3.50, 7.60), (8.0, 3.17, 7.41),
    (15.0, 2.50, 6.75), (20.0, 2.06, 6.30), (30.0, 1.31, 5.53), (40.0, 0.63, 4.88),
    (50.0, 0.11, 4.35), (60.0, -0.32, 3.93), (70.0, -0.60, 3.63), (80.0, -0.76, 3.48),
    (90.0, -0.83, 3.46), (100.0, -0.74, 3.57), (110.0, -0.51, 3.81), (120.0, -0.14, 4.15),
    (130.0, 0.30, 4.60), (140.0, 0.92, 5.16), (145.0, 1.31, 5.51), (150.0, 1.75, 5.97),
    (155.0, 2.27, 6.53), (158.0, 2.64, 6.77), (160.0, 2.90, 7.07),
]  # fmt: skip

# ---------------------------------------------------------------------------
# The hull's shape (stage B: Indf §3.5 item 8; Build-Ships.md §5.0, §5.1, §5.7), drawn only
# ---------------------------------------------------------------------------

# WL1 to WL5's half-breadths by station (Ind §2.3.2, measured), moulded, feet, at stations in
# feet from AP: on 1407T from 5 to 130 ft (±0.15 ft between 20 and 130, ±0.5 at the ends), on
# 1407F from 140 to 159 ft (±0.1 ft); None where the waterline has ended at the rabbet (WL5 at
# 151.8 ft, WL4 155.4, WL3 157.6, WL2 159.6). WL1 is taken at full resolution where
# WL1_HALF_BREADTHS gives the station (the profile's water, so that the two lines give one
# place alike). WL2 to WL5 stand WL2_BELOW_WL1_FT apart below WL1 (Ind §2.3.1; the checker's
# fitted lines on 1407F put them 3.74, 7.49, 11.25 and 15.02 ft below it at midships, within
# 0.06 ft of the spacing). The post (0.6 ft) and 160 ft (0.63) give WL1 alone, a station of one
# point, and are left out.
WATERLINES = {
    5: (7.2, 3.1, 1.5, 1.0, 0.4),
    10: (12.1, 5.6, 2.6, 1.3, 0.6),
    20: (16.6, 13.0, 7.3, 3.5, 1.4),
    30: (18.8, 16.9, 12.6, 7.2, 2.9),
    40: (20.06, 18.9, 16.1, 11.4, 5.4),
    50: (20.8, 20.1, 18.0, 14.5, 9.0),
    60: (21.3, 20.7, 19.1, 16.3, 12.0),
    70: (21.6, 21.1, 19.7, 17.3, 13.8),
    80: (21.7, 21.3, 20.0, 17.8, 14.5),
    90: (21.75, 21.3, 20.0, 17.9, 14.7),
    100: (21.75, 21.3, 20.0, 17.6, 14.2),
    110: (21.75, 21.2, 19.6, 16.8, 12.8),
    120: (21.5, 20.7, 18.7, 15.1, 9.9),
    130: (20.5, 19.2, 16.5, 12.0, 6.2),
    140: (17.68, 15.54, 11.66, 7.17, 2.99),
    142: (16.81, 14.47, 10.46, 6.14, 2.47),
    144: (15.82, 13.22, 9.18, 5.13, 1.99),
    146: (14.62, 11.81, 7.80, 4.17, 1.54),
    148: (13.23, 10.28, 6.47, 3.29, 1.11),
    150: (11.70, 8.60, 5.12, 2.44, 0.72),
    152: (9.96, 6.88, 3.85, 1.63, None),
    154: (7.96, 5.11, 2.7, 0.89, None),
    155: (6.87, 4.24, 2.05, 0.55, None),
    156: (5.70, 3.35, 1.44, None, None),
    157: (4.51, 2.50, 0.92, None, None),
    158: (3.25, 1.63, None, None, None),
    159: (1.96, 0.77, None, None, None),
}
# The main breadth's height by station, (ft from AP, ft above WL1): the upper height of breadth,
# the higher of the two dashed lines ZAZ1407's sheer plan draws below the lower deck's ports,
# tracked on 1407F at full resolution along its ink (its red alteration lines passed over),
# ±0.05 ft, read at MAIN_BREADTH's stations (measured here). 2 ft 8 in above WL1 at midships,
# it sweeps up to 8 ft 4 in at 155 ft, toward the hawse holes, and to 8 ft 1 in at AP, above the
# wing transom (WING_TRANSOM_FT), as Steel's rule lifts the heights of breadth (1805, OCR l.
# 15190-15194). The lower of the two, 4 in above WL1 at midships, is Steel's lower height of
# breadth "a few inches higher" than the load line there; it joins this one forward at the
# hawse holes and aft at the counter. Forward of 155 ft the two run into the hawse holes and
# the stem, and are not read.
HEIGHT_OF_BREADTH = [
    (0.0, 8.12), (10.0, 6.75), (20.0, 5.52), (30.0, 4.57), (40.0, 3.80), (50.0, 3.26),
    (60.0, 2.92), (70.0, 2.72), (80.0, 2.66), (90.0, 2.71), (100.0, 2.75), (110.0, 2.84),
    (120.0, 3.18), (125.0, 3.45), (130.0, 3.84), (135.0, 4.34), (140.0, 5.02), (145.0, 5.86),
    (150.0, 6.96), (155.0, 8.29),
]  # fmt: skip
# The channel wale, the band between the two tiers of ports where the main and fore chain
# plates end: its lower edge (ft from AP, ft above WL1) and its breadth, both tracked on 1407F
# at full resolution along its whole length (measured here): 8.05 ft above WL1 at 90 ft (28.7
# ft above K; ZAZ2371's 28.8, Ind §2.3.5, within 0.1 ft), its upper edge 2.36-2.45 ft above
# it from 10 to 154 ft, the mean taken. ZAZ2371's 1.9 ft broad (28.8-30.7 ft above K) is the
# razee's, the wale cut with her side in the waist (`the_upper_works`). Abaft 10 ft it runs
# into the quarter gallery's lower finishing, and is drawn from there.
CHANNEL_WALE_FT = [
    (10.0, 11.81), (20.0, 10.95), (30.0, 10.20), (40.0, 9.57), (50.0, 9.05), (60.0, 8.63),
    (70.0, 8.31), (80.0, 8.11), (90.0, 8.05), (100.0, 8.09), (110.0, 8.26), (120.0, 8.52),
    (130.0, 8.88), (140.0, 9.35), (150.0, 10.02), (155.0, 10.51), (160.0, 11.06),
]  # fmt: skip
CHANNEL_WALE_BREADTH_FT = 2.4
# The stern (Build-Ships.md §5.1, square), measured on 1407F's body plan, ZAZ1407 at full
# resolution (its heights from K, the band's bottom in the body plan's keel box at 5952 px, WL1
# 21.245 ft above it at AP: Ind §2.3.1; its after body's green WL1 agrees within 0.05 ft): the
# wing transom, the transom's foot, (ft above WL1 at the middle line, at its ends, and its ends'
# half-breadth moulded): 6.74 ft at the middle line and 6.38 at its ends, 12.99 ft out, so
# rounded up 0.36 ft, the middle the higher, as a beam rounds up; and the stern's outline, the
# side counter timber seen from aft, traced from the wing transom's end to the taffrail's side,
# (ft above WL1, half-breadth moulded), ±0.05 ft. The lower counter's and the upper counter's
# touches at the middle line stand 11.39 and 14.09 ft above WL1 on it; Steel's 64 (1805, Folio
# LI, read on the cached leaf, IA n587) puts them 30 ft 6 in and 33 ft 0 in above the rabbet
# (10.9 and 13.4 ft above WL1, the rabbet 19.63 ft below it at AP), the folio's taffrail 50 ft
# 0 in (30.4: hers is 28.0, stage A's stern_m) and its stern 22 ft 0 in broad at the top-timber
# line (hers 19.8-22.1 ft on the outline from 20.6 to 14.6 ft above WL1): a check, Steel's 64
# being of 1369 tons to her 1384. Plainly: stern_m's after face runs straight up the post on
# 1407F to 8.0 ft above WL1 before the counter leaves it, 1 ft 3 in above the wing transom at the
# middle line; the two readings are not reconciled (the line above 6 ft 9 in may be the rudder
# head's), and are open on 1407F.
WING_TRANSOM_FT = (6.74, 6.38, 12.99)
STERN_OUTLINE = [
    (6.6, 13.18), (8.6, 13.15), (10.6, 12.33), (12.6, 11.63), (14.6, 11.07), (16.6, 10.63),
    (18.6, 10.26), (20.6, 9.91), (22.6, 9.60), (24.6, 9.31), (26.6, 9.03),
]  # fmt: skip
# The quarter galleries, two tiers (ft from AP aft and forward, ft above WL1 low and high), each
# at its middle from its rail's lower edge to its top rail and from its after frame to its fore
# frame: the upper deck's three lights and the quarterdeck's three, measured on 1407F at full
# resolution (±0.1 ft), the lower tier's lower finishing and the upper's roof left out.
QUARTER_GALLERIES_FT = [(-6.9, 3.7, 12.7, 17.4), (-8.2, -0.4, 19.9, 24.4)]
# The stern lights, two bands (ft above WL1 low and high, count, half-breadth ft): the
# wardroom's at the upper deck and the captain's at the quarterdeck, behind the balcony, five
# lights each on her own draught as built, ZAZ1953's stern elevation (read; the quarter
# galleries' windows outboard of them in line), the lower band within 10.79 ft of the middle
# line and the upper within 9.60, between the outer pilasters' centres (measured at 4.634 px to
# the foot by its scale strip, ±0.3 ft); their heights the quarter gallery's aftmost lights on
# 1407F, in the same tiers (measured, ±0.1 ft).
STERN_LIGHTS = [(13.7, 16.9, 5, 10.79), (20.9, 23.5, 5, 9.60)]

# ---------------------------------------------------------------------------
# The rig (Indf §4.1-§4.3)
# ---------------------------------------------------------------------------

# The masts at the lower-deck partners (ft from AP), their heel shoulders above K and their
# rakes, measured on ZAZ1280 by the checker (Ind §3.1). Their places in the file: mizen -16.33
# m, main -2.78 m, fore +19.23 m (Indf §2.1).
MASTS = {
    "fore": (143.09, 9.67, 0.3),
    "main": (70.87, 7.15, 1.4),
    "mizzen": (26.42, 10.35, 2.15),
}
# Steel 1794 vol. I p. 49, "64 GUNS. 1369 TONS." (page image IA leaf n66, read twice in Ind §3.1
# and again in Indf §4.1), feet: the lower masts, topmasts and topgallant masts (each with its
# royal pole: the "Royal" rows read 0 0, so the royal sets on the topgallant's pole), and their
# yards; the bowsprit and the jib-boom.
STEEL_64 = {
    "mast": {"main": 101.0, "fore": 89 + 7 / 12, "mizzen": 86.0},
    "topmast": {"main": 58.5, "fore": 53.0, "mizzen": 43.5},
    "topgallant_mast": {"main": 29.25, "fore": 26.5, "mizzen": 21.75},
    "yard": {"main": 90 + 4 / 12, "fore": 79.5, "mizzen": 57.5},  # the mizzen's: the crossjack
    "topsail_yard": {"main": 65 + 4 / 12, "fore": 57.5, "mizzen": 43.25},
    "tg_yard": {"main": 39.0, "fore": 34.5, "mizzen": 29.0},
    "royal_yard": {"main": 32.0, "fore": 28.5, "mizzen": 21.0},
    "mizen_yard": 77.0,
    "bowsprit": 60 + 4 / 12,
    "jib_boom": 43.75,
}
# Steel's diameters at the partners and the slings, inches (p. 49, as above).
STEEL_64_DIAMETER_IN = {"main": 33.5, "fore": 29.75, "mizzen": 19.75, "mizen_yard": 14.0}
# Steel's heads (vol. I, OCR l. 4697-4699, read (OCR)): the main and fore masts' heads 5 in to
# every yard of the mast's length; the mizen mast's and the main and fore topmasts' 4 in; the
# mizen topmast's and every topgallant mast's 3 1/2 in.
HEAD_IN_PER_YARD = {
    "mast": {"main": 5.0, "fore": 5.0, "mizzen": 4.0},
    "topmast": {"main": 4.0, "fore": 4.0, "mizzen": 3.5},
    "topgallant_mast": {"main": 3.5, "fore": 3.5, "mizzen": 3.5},
}
# The topgallant mast's pole-head (Steel 1794 vol. I p. 16, 'Topgallant-masts', OCR l. 2934-2942,
# and p. 42, the fractional table's line, OCR l. 4701-4702; Bel §4.2's "pp. 41-42" and the owner's
# "p. 42" are that table's page, the running heads putting the words on p. 16): topgallant masts
# "have commonly pole heads, either stump, common, or long"; the common and the long are "set up
# from the stop", a long one "two-thirds the length to the stop"; the hounds "three-fifths" of the
# square head's length below the stop. Read as the 74's design reads them (Bel §4.2, judgement
# on those words) and taken for her by the owner (2026-10-29, "Agreed"; Indf §17): the table's
# topgallant length is the mast with a square head of 3 1/2 in to a yard, and the long pole-head
# takes that head's place, set up from the stop, so that the stick rises above the listed
# length and her topgallants and royals hang near Steel's table IV depths between their yards
# (the owner's spars rule kept). Stage A read a common pole of seven-eighteenths within the
# listed length (7/18), on which the two tables disagreed above the topmast caps (Indf §4.3).
LONG_POLE_OF_STOP = 2.0 / 3.0
HOUNDS_OF_STOP = 3.0 / 5.0
# The bowsprit's steeve, about 27 degrees, ±2 (measured on ZAZ1280 and 2371: Ind §3.1). Its
# heel on ZAZ1280 (3840 px, registered on the measured main and fore masts, 20.0 px to the foot)
# just before the fore mast, about 148.3 ft from AP: so 14.2 ft of it lies within the stem head
# (`STEM_HEAD_FT`, 162.5 ft from AP), 16.0 ft along its steeve, and 44.4 ft of its 60 ft 4 in
# stand outboard (measured here, ±1 ft; Luce's third inboard, the frigate's rule, would give
# 40.2). Stage A rooted it at the knighthead's cap (`KNIGHTHEAD_FT`), 46.3 ft outboard.
BOWSPRIT_STEEVE_DEG = 27.0
BOWSPRIT_HEEL_FT = 148.3
# The jib-boom: 7/12 of it outboard (Luce 1866 ch. VII, the frigate's rule; judgement for her).
JIB_BOOM_OUTBOARD = 7.0 / 12.0
# The yards under the bowsprit (Ext §4.1; `spritsail_yards.cut`): Steel's yards (p. 49, the 64,
# read again in Indf §4.6) and Steel's sails (table IV, the 64 column: Ind §5), the sprit course
# 26 cloths at the head and the foot and 7 1/2 yards deep, the sprit topsail 17 and 27 and 9 yards
# deep. The spritsail yard's slings near the cap (Steel 1794 vol. I pp. 196-197; Lavery 1985 I30),
# 0.85 of the bowsprit's outboard part out and 0.8 m under its line, the sprit-topsail yard's
# parral 0.5 m under the jib-boom's line (judgement, the three, as the engine's fixture), and each
# yard braced 30 degrees from square (judgement, as the fixture: Lavery I30's leads stop neither
# sooner).
SPRITSAIL_64 = {"yard_m": 57.5 * FT, "head_cloths": 26.0, "foot_cloths": 26.0, "depth_yd": 7.5}
SPRIT_TOPSAIL_64 = {"yard_m": 34.5 * FT, "head_cloths": 17.0, "foot_cloths": 27.0, "depth_yd": 9.0}
SPRITSAIL_STATION = 0.85
SPRITSAIL_HANG_M = 0.8
SPRIT_TOPSAIL_HANG_M = 0.5
SPRIT_BRACE_LIMIT_DEG = 30
# Their canvas (Steel 1794 vol. I, Sail-making; Ind §5): the first of Steel's two, as her fore
# topsail's and her fore topgallant's, the yards of the same lengths (judgement).
SPRITSAIL_CANVAS = (2, f"{g.STEEL_SM}, 'Spritsail course': No. 2 or 3, the first taken")
SPRIT_TOPSAIL_CANVAS = (6, f"{g.STEEL_SM}, 'Spritsail topsail': No. 6 or 7, the first taken")

# Steel's sail table IV, the 64 column (Steel 1794 vol. I p. *149, page image IA leaf n244, read
# in full by R1 and the checker: Ind §5): cloths at the head and the foot, and the depth in
# yards (the mizen topsail's the mean of its middle, 12, and its clue, 12 3/4). Each cloth 22 1/2
# in in the sail: 24-in canvas less Steel's seam for ships of 50 guns and up (Ind §5, judgement).
STEEL_SAILS_64 = {
    "main.course": (41.5, 44.0, 14.0),
    "fore.course": (36.0, 34.0, 12.0),
    "main.topsail": (27.0, 43.0, 17.5),
    "fore.topsail": (23.0, 37.0, 15.75),
    "mizzen.topsail": (18.5, 27.0, 12.375),
    "main.topgallant": (19.5, 27.5, 9.0),
    "fore.topgallant": (17.0, 24.0, 8.25),
    "mizzen.topgallant": (13.5, 19.5, 6.75),
    "main.royal": (15.0, 20.0, 7.0),
    "fore.royal": (13.0, 17.5, 6.25),
    "mizzen.royal": (10.0, 14.0, 5.0),
}
CLOTH_IN_SAIL_FT = 22.5 / 12.0
# The triangular headsails of the same table: the cloths in the foot and the leech's depth in
# yards (Ind §5): the fore staysail 0 / 19 / 11 1/2, the fore topmast staysail 0 / 18 / 16, the
# jib ("Jib Flying") 0 / 24 / 23.
STEEL_HEADSAILS_64 = {
    "fore.staysail": (19.0, 11.5),
    "fore.topmast_staysail": (18.0, 16.0),
    "jib": (24.0, 23.0),
}
# The staysails between the masts in the same table (Ind §5): its row in words; its figures, the
# cloths at the head and at the foot, the bunt and the after leech in yards (the main staysail a
# triangle, with no head and no bunt); and the area Ind §5 gives it by Steel's own rule for the
# canvas (the cloths of the head and the foot halved, by the bunt and the leech halved: Steel
# 1794 vol. I, the sail-making rules, OCR l. 10873-10883; the four-sided ones an upper bound),
# m2, with the band of Indf §4.3's check, ±10% the triangle and ±25% the four-sided. Steel's 64
# has no mizen topgallant staysail, and she carries none.
STEEL_BETWEEN_64 = {
    "main.staysail": ("0 / 28 cloths, leech 14 yards", (0.0, 28.0, None, 14.0), 102.0, 0.10),
    "main.topmast_staysail": (
        "22 / 24 cloths, bunt 9, after leech 22 1/4 yards",
        (22.0, 24.0, 9.0, 22.25),
        190.0,
        0.25,
    ),
    "middle_staysail": (
        "21 / 21 cloths, bunt 6, after leech 13 1/2 yards",
        (21.0, 21.0, 6.0, 13.5),
        110.0,
        0.25,
    ),
    "main.topgallant_staysail": (
        "18 / 18 cloths, bunt 5, after leech 14 yards",
        (18.0, 18.0, 5.0, 14.0),
        90.0,
        0.25,
    ),
    "mizzen.staysail": (
        "19 1/2 / 21 cloths, bunt 7 1/2, after leech 11 1/2 yards",
        (19.5, 21.0, 7.5, 11.5),
        100.0,
        0.25,
    ),
    "mizzen.topmast_staysail": (
        "16 / 17 cloths, bunt 5, after leech 13 yards",
        (16.0, 17.0, 5.0, 13.0),
        80.0,
        0.25,
    ),
}
# The owner chose (2026-10-29: "Agreed"; Indf §17) the main, middle, mizen and mizen topmast
# staysails cut to these figures (`between_the_masts`): the generator's rules on her spars
# (`g.between_the_masts`) left them outside their bands, the main staysail +26%, the middle -29%,
# the mizen -35% and the mizen topmast +40%. The main topmast and main topgallant staysails,
# within their bands so cut (+18% and -11%), were kept as the rules cut them; since her long
# pole-heads the main topgallant staysail, which those rules made +26%, is cut to the table too.
# The mizen course (Steel's table IV, 64 column; Ind §5): 14 1/2 cloths at the head and 15 1/2
# at the foot, its fore (mast) leech 9 1/4 yards and its after leech 17 1/4.
STEEL_MIZEN_COURSE_64 = (14.5, 15.5, 9.25, 17.25)
# Its fore leech "is attached to the mizen-mast within 6 or 7 feet of the deck" (Steel 1794
# vol. I, 'Mizen-course', OCR l. 11441-11442, read (OCR)): its tack 6 ft 6 in above her
# quarterdeck, the mean. Indf §4.4 judged 3 ft (the truss 11.6 m above her datum); Steel's text
# gives 6 or 7 ft, so 6 ft 6 in was built at stage A, the truss 12.7 m above the datum, and the
# clew check raises it (`mizen_course_cut`).
MIZEN_TACK_ABOVE_DECK_FT = 6.5
# The head room over her roundhouse deck (the clew check: Bel §1.5, §4.5-§4.6, §17.2 item 13; the
# lead's notes of 2026-10-29, item 2): what the mizen course's foot, the 64's driver boom and the
# razee's spanker boom must stand above it by, feet: 6 ft, the 74's (Bel §4.6, judgement: room for
# the deck's people and its carronades' crews to work beneath), going first, to 5 ft, only where
# a check breaks; past that, a report with the figures and no file. On a boom it is Bel §4.6's; on
# a loose foot it is judgement, Bel §1.5 asking a clew only to clear the deck, and the other
# readings are measured in TuningNotes for the lead.
HEAD_ROOM_FT = (6.0, 5.0)
# The mizen yard's lines in Steel's list for a 64 (Steel 1794 vol. II, '64 Gun Ship, 1369 Tons',
# OCR, read here and not on the page image), inches: the derrick (l. 24857, 4 | 36 | Double 14),
# the vang pendants (l. 24862, 4 | 12 | Double 8) and, by its place after the vangs' strapping in
# this list as in the others, the bowlines (l. 24865, garbled: 3 | 24 | Single 10). Indf §4.2's
# check: the rule on her rope gave 4 1/4, 3 3/4 and 3 3/4 (TuningNotes).
STEEL_MIZEN_YARD_LINES_64 = {"derrick": 4.0, "vang": 4.0, "bowline": 3.0}
# Steel's driver boomsail (table IV, the 64 column; Ind §5; Ext §17.2): 22 1/2 cloths at the head
# and 29 at the foot, its fore leech 9 1/2 yards and its after leech 20.
STEEL_DRIVER_64 = (22.5, 29.0, 9.5, 20.0)

# Steel's reef bands for her rate (Ind §5; Steel 1794 vol. I, the sail-making articles, read
# (OCR)): two in each course; three or four in the main topsail (l. 11640), the four taken; three
# in the mizen topsail in ships of 50 guns and up; the fore topsail's three (judgement); one in
# the mizen course a fifth up its mast leech (l. 11448). The frigate-36 reefs her courses once.
REEFS = {"course": 2, "topsail": {"main": 4, "fore": 3, "mizzen": 3}, "topgallant": 0, "royal": 0}

# The brace limits, degrees from square: the frigate-36's (Fincham 1843 art. 102, the long
# ships' upper values, two degrees more a level aloft), judgement for her (Indf §4.2). Checked
# against her lee rigging from the channels measured on 1407F (Indf §3.5 item 7): the lower
# yards, slung 2 ft under the hounds, meet the foremost lee shroud only at 70-74 degrees; the
# foremost lee topmast backstay, set up, would stop the main yard at about 50 and the fore at
# about 47 (measured here). The owner kept the frigate's limits (2026-10-29, Indf §17 item 11:
# "Reasonable"), on the reading that the lee topmast backstays were eased when the yards were
# braced sharp up.
BRACE_PLANS = {
    "fore": [("course", 62), ("topsail", 64), ("topgallant", 66), ("royal", 68)],
    "main": [("course", 64), ("topsail", 66), ("topgallant", 68), ("royal", 70)],
    "mizzen": [("topsail", 62), ("topgallant", 64), ("royal", 66)],
}
CROSSJACK_BRACE_DEG = 60

# The frigate-36's plain sail, m2, against which her rope is scaled (Indf §4.2).
FRIGATE_PLAIN_SAIL_M2 = 1584.0

# Her studding sails, the frigate-36's set (Indf §4.3): Steel's table IV, the 64 column (Ind
# §5), cloths at the head and the foot and the depth in yards; and Steel's booms for a 64 (p. 49;
# Ind §3.1), feet: the lower boom 50 ft 0 in, five-ninths of the main yard, the topmast and
# topgallant booms half the yard each is rigged on (Steel p. 40, read on the page image). Steel's
# table also gives a main lower studding sail, 16 / 16 / 16 1/2 (138 m2), against the one pair
# of lower booms; the frigate-36 carries none, and it is not built (Indf §4.3).
STEEL_STUDDING_64 = {
    ("fore", "lower"): (15.0, 15.0, 13.0, 50.0),
    ("fore", "topmast"): (11.0, 15.0, 17.0, 39.75),
    ("fore", "topgallant"): (8.0, 11.0, 8.5, 28.75),
    ("main", "topmast"): (12.0, 16.0, 18.5, 45.0),
    ("main", "topgallant"): (9.0, 12.0, 9.5, 32.0 + 8.0 / 12.0),
}
# The lower studding sail's boom "is fitted with an iron goose-neck and key, which connects to a
# bolt in the forward part of the fore-channels" (Luce 1884 p. 137, OCR l. 10454-10456, read
# (OCR)): it swings at the fore channel. The 64's fore shrouds' deadeyes about 38 ft above K
# (measured on 1407F at full resolution, the main channel's at 37.0-37.5); the razee's lowered
# channel, 32.0-32.2 ft (measured, ZAZ2371: Ind §2.3.8).
FORE_CHANNEL_K_FT_64 = 38.0
FORE_CHANNEL_K_FT_RAZEE = 32.1

# The storm canvas's heights above the deck she works it from (the frigate-36's, gen_ships.
# frigate(), judgement there): the mizen stay's collar 12 ft up the main mast (Steel 1794 vol. I,
# 'Mizen-stay'), the mizzen storm staysail's head 0.6 of the way up the stay and its clew 7 ft
# above the deck (Steel's mizen staysail "within 6 or 7 feet of the quarter-deck"); the storm
# mizzen's tack 4 ft up its stay, its luff 0.8 of the stay's run to the hounds, its foot "towards
# the taffarel" (Steel, 'Storm mizen') 0.45 of the driver boom. Where her rail over the foot's
# run stands higher than that tack (her roundhouse, on either file), the tack stands at the rail,
# so that the foot does not run through the deck under it (judgement, as the clew check).
MIZEN_STAY_COLLAR_FT = 12.0
STORM_STAYSAIL_HEAD_OF_STAY = 0.6
STORM_STAYSAIL_CLEW_FT = 7.0
STORM_MIZZEN_TACK_FT = 4.0
STORM_MIZZEN_LUFF_OF_RUN = 0.8
STORM_MIZZEN_FOOT_OF_BOOM = 0.45
# The ringtail (the razee's, she having the driver boom): Kipping's brig's, 5 cloths in the head
# and 7 in the foot, its depth the spanker's after leech, its boom the foot and a third (the
# frigate-36's, judgement); the save-alls' head along 0.6 of the lower boom, down to half a
# metre off the water (the frigate-36's, judgement).
RINGTAIL_CLOTHS = (5.0, 7.0)
SAVE_ALL_OF_BOOM = 0.6


# What the cuts compute from the file's own keys, for the generator's report (`her_report`) and
# not the files' notes (the lead's notes of 2026-10-29, item 2), by variant.
REPORT: dict[str, dict] = {}


# ---------------------------------------------------------------------------
# Her particulars: one variant's data, the 64's here and the razee's derived from them
# ---------------------------------------------------------------------------


@dataclass
class Particulars:
    """One variant's figures in the drawings' frame, and the words of her file. `rise_ft` is
    her water's rise against WL1 aft and forward (the 64's none); `datum_deck` the deck she is
    worked from in the waist (`deck_k_ft`), whose midship height is the file's datum unless
    `datum_line` gives another (Indf §2.2): the line, (ft from AP, ft above K), whose midship
    height is the datum when it is not one of her decks there (the razee's old upper deck, D18
    (c)). `rail` and `stern` are (ft from AP,
    ft above WL1), `breadth` (ft from AP, half-breadth at her water, at the top of her side),
    moulded; `mizen` is her after sail, "course" (the 64's) or "spanker" (the razee's). Her
    shape (stage B, drawn only): `channel_wale` (ft from AP, its lower and upper edges ft above
    WL1), `galleries` and `lights` as QUARTER_GALLERIES_FT and STERN_LIGHTS give them, and
    `marks`, each line's rung (Build-Ships.md §5.0 principle 4)."""

    key: str
    file: str
    name: str
    era_notes: str
    header: str
    hull: dict
    hull_notes: dict
    rise_ft: tuple[float, float]
    datum_deck: str
    decks: dict
    ports: dict
    port_size_ft: dict
    port_notes: dict
    rail: list
    stern: list
    breadth: list
    profile_notes: dict
    fore_channel_k_ft: float
    masts: dict
    mizen: str
    channel_wale: list
    galleries: list
    lights: list
    marks: dict
    datum_line: list | None = None

    def water_ft(self, x_ft):
        """Her load water above K at `x_ft` forward of AP, feet."""
        aft, fwd = self.rise_ft
        return wl1_above_k(x_ft) - (aft + (fwd - aft) * x_ft / 160.0)

    def z_m(self, z_k_ft, x_ft):
        """A height above K at `x_ft`, as metres above her water there."""
        return (z_k_ft - self.water_ft(x_ft)) * FT

    @property
    def datum_z(self):
        """The datum, metres above her water: her D18 line at the middle of the load line,
        `datum_line` where she has one, else her `datum_deck`."""
        line = self.datum_line if self.datum_line is not None else self.decks[self.datum_deck]
        return round(self.z_m(interp(line, MIDSHIPS_FT), MIDSHIPS_FT), 2)

    @property
    def frame_z(self):
        """The frame her rig is cut in, metres above her water: the deck she is worked from at
        the middle of the load line (`deck_k_ft`), from which the frigate-36's rules take their
        heights "above the deck" (Indf §2.2). It is her datum where the datum is that deck (the
        64's upper deck); the razee's is her gun deck, 1.39 m, her datum (c) 2.28 m above it, so
        that her rig is cut where D18 (a) cut it and written above the datum (`above_datum`)."""
        return round(self.z_m(self.deck_k_ft(MIDSHIPS_FT), MIDSHIPS_FT), 2)

    def deck_k_ft(self, x_ft):
        """The deck she is worked from at `x_ft`, feet above K: her quarterdeck or forecastle
        over its extent, else the datum's deck (the waist)."""
        for word in ("quarterdeck", "forecastle"):
            pts = self.decks.get(word)
            if pts and pts[0][0] <= x_ft <= pts[-1][0]:
                return interp(pts, x_ft)
        return interp(self.decks[self.datum_deck], x_ft)


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
    """Feet forward of AP as the file's x, metres forward of the middle of the load line."""
    return (x_ft - MIDSHIPS_FT) * FT


def above_datum(p, h_m):
    """A height above her frame (`Particulars.frame_z`), metres, as her file writes it, above her
    datum (D18): unchanged where the two are one (the 64's, so that no byte of hers moves), else
    moved by the frame's height above the datum and kept to the centimetre, so that no height
    above her water moves with the datum (the razee's, D18 (c): her frame 2.28 m below it)."""
    shift = p.frame_z - p.datum_z
    return h_m if shift == 0.0 else round(h_m + shift, 2)


def mast_x_at_datum(p, x, rake_deg):
    """A lower mast's x as her file writes it, at the datum's height (the viewer's and the rake's
    anchor: `deck_height_m`): its place at the frame where the two are one, else raked from there
    to the datum, so that the mast stands where it did (the razee's, D18 (c))."""
    shift = p.datum_z - p.frame_z
    return x if shift == 0.0 else round(x - math.tan(math.radians(rake_deg)) * shift, 2)


def head_ft(length_ft, in_per_yard):
    """A mast's head by Steel's rule, so many inches to every yard of its length, feet."""
    return length_ft / 3.0 * in_per_yard / 12.0


def sixty_four():
    """The 64 as built, 1784 (Indf §2-§4): her hull, decks, ports and masts."""
    hull = {
        "length_waterline_m": 48.8,
        "beam_m": 13.54,
        "draught_m": 6.33,
        "displacement_kg": 2170000.0,
        "gm_m": 1.35,
        "clr_x_m": 4.8,
        "lateral_area_m2": 305.5,
        "hull_speed_kn": 12.8,
        "rudder": {"area_m2": 8.95, "max_angle_deg": 35, "rate_deg_s": 3.0, "span_m": 6.47},
    }
    hull_notes = {
        "length_waterline_m": "160 ft: WL1, ZAZ1407's load line, rabbet to rabbet (measured, "
        "1407F; D29 (b): Ind §2.3.2, §2.4); 164.6 ft (50.2 m) outside the post and the stem.",
        "beam_m": "44 ft 5 in extreme as built (Winfield 1793-1817 p. 100; D34 (a)); 43 ft 6 in "
        "moulded at WL1, about 44 ft 3 in outside the plank (measured, Ind §2.4).",
        "draught_m": "20 ft 9 in mean to K, the band's bottom: 21 ft 3 in at AP, 20 ft 2 in at 160 "
        "ft (measured, 1407F; D29 (b): Ind §2.3.1); 6.15 m to the main keel; Steel's 64 of Folio I "
        "draws 20 ft 8 in abaft and 19 ft 4 in afore (read).",
        "displacement_kg": "2,170 t: judgement within the band integrated on her measured lines, "
        "2,120-2,240 t (Ind §2.3.3), the razee's 1,925 t less by the measured slice of 238-244 "
        "tons of 35 cu ft (Indf §2.1).",
        "gm_m": "4 ft 5 in: judgement within 1.2-1.5 m (Ind §2.3.4), KM measured 7.3 m above K; "
        "no period figure for her KG was found.",
        "clr_x_m": "Tuned against the helm's truths (6 and 17; Indf §2.1, §9, §16 item 3). Her "
        "start, the measured centroid of the plane the file counts (hull and band, no rudder), "
        "0.55 m abaft the middle of the load line (Ind §2.3.6), with the frigate-36's tuned lead "
        "of 9.6% of her load line ahead of it (judgement). Forward of that at stage A, for her "
        "stand-in mizen course, a smaller after sail than the frigate's spanker, and back at stage "
        "B, her rig whole (judgement). Measured, old beside new, in docs/dev/TuningNotes.md, and "
        "held by her tests.",
        "lateral_area_m2": "Below WL1 with the band, the rudder left out, as the frigate's "
        "(measured, 1407F: 3,288-3,290 sq ft; Ind §2.3.6).",
        "hull_speed_kn": "Judgement within D24 (a)'s 12.5-13.0 for the 64 (Indf §2.1); no period "
        "knots for her or her sister were found (Ind §7.2). Tuned only within that band; kept, "
        "no truth asking more of it (the razee faster at every point, D24's 'Plainly': the 64 "
        "is not pinned against the frigate-36).",
        "deck_height_m": "Her upper deck at midships, 10 ft 7 in above WL1 (measured, 1280T: Ind "
        "§2.3.5): the uppermost continuous deck, D18 (a), kept for the 64 (the owner, 2026-10-29: "
        "Indf §2.2, §17 item 1), the datum "
        "of every spar height and every sail's corners.",
        "rudder": "Measured on 1407F (Ind §2.3.6): 95.4-96.9 sq ft below WL1, its sole to the "
        "band's bottom, 21 ft 3 in, the span; 35 degrees and 3 deg/s the frigate-36's "
        "(judgement).",
    }
    lower_ports = [(x, wl1_above_k(x) + s, lower_sill_half_breadth(x)) for x, s in LOWER_SILLS]
    upper_ports = [(x, wl1_above_k(x) + s, upper_sill_half_breadth(x)) for x, s in UPPER_SILLS]
    qd_ports = [
        (x, wl1_above_k(x) + s, interp(TOP_TIMBER, x) + PLANK_FT) for x, s in QUARTERDECK_SILLS
    ]
    decks = dict(DECKS_64)
    aft, breast = ROUNDHOUSE_FT
    decks["roundhouse"] = [
        (x, wl1_above_k(x) + z - ROUNDHOUSE_BELOW_RAIL_FT) for x, z in RAIL if aft <= x <= breast
    ]
    fc_ports = [
        (x, open_deck_sill(x, interp(decks["forecastle"], x)), interp(TOP_TIMBER, x) + PLANK_FT)
        for x in (FORECASTLE_CARRONADE_X_FT, FORECASTLE_PORT_X_FT)
    ]
    rh_ports = [
        (x, open_deck_sill(x, interp(decks["roundhouse"], x)), interp(TOP_TIMBER, x) + PLANK_FT)
        for x in ROUNDHOUSE_PORTS_FT
    ]
    port_notes = {
        "lower": "the gun deck's thirteen a side, every sill measured on ZAZ1407 at full "
        "resolution (Indf §3.5 item 1); the half-breadth at the sill the main-breadth line "
        "measured on the half-breadth plan, less the midship section's 0.13 ft above the dead "
        "flat, with 4 1/2 in of plank (judgement on measured lines)",
        "upper": "the upper deck's thirteen a side, every sill measured on 1407F at full "
        "resolution; the half-breadth 0.30 of the way from the top-timber line to the main "
        "breadth, as the midship section stands at the midship sill, with the plank "
        "(judgement on measured lines)",
        "quarterdeck": "six a side measured on 1407F at full resolution, the after one under "
        "the roundhouse; the half-breadth the top-timber line's with the plank (judgement)",
        "forecastle": "one a side at 140.4 ft (Ind §2.3.7, tentative; none drawn on 1407F at "
        "full resolution, her gun firing over the rail): the sill the deck and 0.41 m, the "
        "half-breadth the top-timber line's (judgement); and one at 127.9 ft for the class's "
        "24-pounder carronade of 1794 (Winfield 1793-1817 p. 99; Indf §5.1, judgement), where "
        "the rail stands 1 ft 2 in above the deck and the gun fires over it, its sill 2 in under "
        "the rail (judgement)",
        "roundhouse": "three a side at 4.5, 14.4 and 24.2 ft from AP for the class's 18-pounder "
        "carronades of 1794 (Winfield 1793-1817 p. 99; Indf §5.1, judgement), firing over the "
        "rail, 1 ft 3 in above the deck: each sill 2 in under the rail, the half-breadth the "
        "top-timber line's (judgement)",
    }
    return Particulars(
        key="sixty-four",
        file="sixty-four.yaml",
        name="Indefatigable",
        era_notes="HMS Indefatigable as built, a 64-gun ship of the Ardent class (Slade's design "
        "of 1762 on the lines of the Fougueux): ordered 1780, launched by Adams at Bucklers Hard "
        "in 1784, never commissioned as a 64 and cut down to a frigate in 1794-95 (Winfield "
        "1793-1817 pp. 99-100). 160 ft 1 1/4 in on the gun deck, 44 ft 5 in extreme, 1384 tons. "
        "Hull measured on her draughts (ZAZ1407, ZAZ1280; Research-Indefatigable-2026-10.md); "
        "spars and sails by Steel 1794 vol. I p. 49 and table IV, the 64's columns; see "
        "tools/ships/indefatigable.py for every figure and judgement.",
        header=(
            "# HMS Indefatigable as built, 1784: a 64-gun ship of the Ardent class (Slade, 1762).\n"
            "# Generated by tools/gen_ships.py (tools/ships/indefatigable.py); edit those and\n"
            "# rerun, do not edit this file. Hull and profile: measured on her draughts\n"
            "# (RMG ZAZ1407, ZAZ1280; docs/design/Research-Indefatigable-2026-10.md).\n"
            "# Spars: Steel 1794 vol. I p. 49, the 64 column, her topgallant masts with Steel's\n"
            "# long pole-heads (pp. 16, 42). Sails: Steel's table IV, the 64 column, the\n"
            "# topgallants and royals cut to the spars (the owner's rule). Her mizen course cut\n"
            "# at the mast, her driver and her yards under the bowsprit: tools/ships/\n"
            "# mizen_yard.py and spritsail_yards.py (docs/design/Design-ShipsEngineExtensions.md\n"
            "# §3, §4, §17).\n"
            "# Units: metres, m2, kg, kN. Comments mark each judgement.\n"
        ),
        hull=hull,
        hull_notes=hull_notes,
        rise_ft=(0.0, 0.0),
        datum_deck="upper",
        decks=decks,
        ports={
            "lower": lower_ports,
            "upper": upper_ports,
            "quarterdeck": qd_ports,
            "forecastle": fc_ports,
            "roundhouse": rh_ports,
        },
        port_size_ft={
            "lower": LOWER_PORT_FT,
            "upper": UPPER_PORT_FT,
            "quarterdeck": QUARTERDECK_PORT_FT,
            "forecastle": QUARTERDECK_PORT_FT,
            "roundhouse": QUARTERDECK_PORT_FT,
        },
        port_notes=port_notes,
        rail=list(RAIL),
        stern=list(STERN),
        breadth=[(x, hb, interp(TOP_TIMBER, x)) for x, hb in WL1_HALF_BREADTHS],
        profile_notes={
            "rail_m": "The top of the side, from the taffrail to where the side ends at the "
            "beakhead bulkhead, 153.3 ft from AP, measured on ZAZ1407 at full resolution (Indf "
            "§3.5 items 3 and 9): the roundhouse's rail to 34.8 ft, the quarterdeck's to its "
            "breast at 72 ft, the waist rail, the forecastle's rail from 119.6 ft, read by "
            "columns forward of the timber heads at 145-147.5 ft and taken straight across them. "
            "Forward of the bulkhead is the head (Build-Ships.md §5.1).",
            "stem_m": "The stem's fore edge, from its foot boxed into the keel 1.1 ft above K to "
            "the top of the stem head's fore face under the bowsprit, 162.5 ft from AP and 16.0 "
            "ft above WL1: measured on ZAZ1407 at full resolution (±0.05 ft), separated from the "
            "knee of the head, which is head_m (Indf §3.5 items 8 and 9).",
            "breadth_m": "By station: the half-breadth at WL1 "
            "(measured, Ind §2.3.2) and at the top of the side, the half-breadth plan's "
            "top-timber line (measured on 1407F at full resolution), each with 4 1/2 in of plank.",
            "stern_m": "The post's after face (Ind §2.3.6), the counter and the stern to the "
            "taffrail, measured on 1407F at full resolution (±0.3 ft; the quarter gallery and the "
            "rudder left out).",
            "wales_m": "The main wale, from 1 ft from AP, where it sweeps up into the counter, to "
            "the stem at 160 ft: both edges tracked on 1407F at full resolution (±0.05 ft), 4 ft "
            "3 in broad, 19.9-24.1 ft above K at 85-90 ft, rising 3 ft 9 in to the stem and 6 ft "
            "0 in aft; abaft 6 ft its upper edge, under the quarter gallery's lower finishing, "
            "held at its height there (judgement). ZAZ2371 measures it 20.2-24.7 ft above K at "
            "midships (Ind §2.3.5, at about 6 px to the foot), which stage A carried parallel to "
            "the gun deck's sills from 10.8 to 145.3 ft (judgement).",
            "decks_m": "Each deck at the middle line (measured, 1280T: Ind §2.3.5), over its "
            "extent; the roundhouse's at the side, 1 ft 3 in under its rail from abaft AP to its "
            "breast at 34.4 ft (measured on ZAZ1280 at 3840 px; judgement that the line is the "
            "deck), for the class's carronades of 1794.",
            "head_m": "The knee of the head's fore edge, the gripe's, the cutwater's and the "
            "knee's, from where it leaves the stem's line at the band's square fore end on K, "
            "147.75 ft from AP and ahead of the stem's foot boxed into the keel, to the head's "
            "top 20 ft above WL1 at 174.5 ft: measured on ZAZ1407 (to WL1, Ind §2.3.6; above it "
            "on 1407F at full resolution by rows), stage A's stem_m.",
            "breadth_line_m": "The main breadth by station, Steel's upper height of breadth at "
            "the main half-breadth, from AP to 155 ft: the half-breadth plan's main-breadth line "
            "(measured on 1407F at full resolution) at the height of the upper of the two dashed "
            "lines of breadth on the sheer plan, 2 ft 8 in above WL1 at midships, swept up to "
            "8 ft 4 in at 155 ft toward the hawse holes and 8 ft 1 in at AP above the wing "
            "transom (tracked on 1407F at full resolution, ±0.05 ft; Steel 1805's rule, OCR l. "
            "15190-15194), with 4 1/2 in of plank.",
            "sections_m": "WL1 to WL5 by station, 5 to 159 ft from AP (measured, Ind §2.3.2: on "
            "1407T to 130 ft, ±0.15 ft, ±0.5 at the ends; on 1407F from 140 ft, ±0.1 ft; WL1 at "
            "full resolution where breadth_m gives it), each waterline 3.77 ft below the last "
            "(Ind §2.3.1), with 4 1/2 in of plank; a waterline ended at the rabbet is left out "
            "at its station.",
            "channel_wales_m": "The channel wale, the band between the tiers of ports where the "
            "chain plates end, from 10 to 160 ft: its lower edge 8.05 ft above WL1 at 90 ft "
            "(28.7 ft above K) and its breadth 2.4 ft, the mean of 2.36-2.45, both tracked on "
            "1407F at full resolution (ZAZ2371's 28.8 ft above K at midships agrees within 0.1 "
            "ft: Ind §2.3.5).",
            "form": "Her form (Build-Ships.md §5.1): no fullness, the ends under the water "
            "drawn through her measured waterlines (sections_m).",
            "form.stern": "Square. The knuckle, the transom's foot where the side closes to it, "
            "is the wing transom at its ends, 6 ft 4 1/2 in above WL1, rounded up 4 in to 6 ft "
            "9 in at the middle line, the middle the higher, as a beam rounds up; the transom's "
            "half-breadths 13 ft 0 in at the knuckle, the wing transom's end, and 9 ft 0 in at "
            "the taffrail's side, 26 ft 11 in above WL1, on the side counter timber's outline "
            "seen from aft, each with the plank: measured on 1407F's body plan, ±0.05 ft. "
            "Plainly: stern_m's after face runs straight up the post on 1407F to 8.0 ft above "
            "WL1 before the counter leaves it, 1 ft 3 in above the wing transom at the middle "
            "line; the two readings are not reconciled (the line above 6 ft 9 in may be the "
            "rudder head's), open on 1407F. Two tiers of "
            "quarter gallery, the upper deck's and the quarterdeck's, each from its rail's lower "
            "edge to its top rail, measured on 1407F at full resolution. Two bands of five "
            "stern lights, read on ZAZ1953's stern elevation, her own as built, the lower within "
            "10 ft 9 in of the middle line and the upper within 9 ft 7 in (measured at 4.63 px "
            "to the foot, ±0.3 ft), at the heights of the quarter gallery's aftmost lights on "
            "1407F, which ZAZ1953 draws in line with them. Steel's 64 (1805 Folio LI, read) as a "
            "check: the lower counter's touch at the middle line 10.9 ft above WL1 against "
            "1407F's 11.4, the upper's 13.4 against 14.1, the taffrail 30.4 against 28.0, the "
            "stern 22 ft broad at the top-timber line against 19.8-22.1 ft on the outline.",
            "form.head": "A figure on the knee of the head: judgement, her type certainly "
            "carrying one (Build-Ships.md §5.0 principle 9, §5.7); ZAZ1407 and ZAZ1953 draw the "
            "knee in outline only, with no figure.",
            "marks": "Each line's rung (Build-Ships.md §5.0 principles 3 and 4): sourced, "
            "measured on her own draughts (ZAZ1407, ZAZ1280, ZAZ1953; ZAZ2371); judged, a "
            "judgement at its weakest point, which the line's note names.",
        },
        fore_channel_k_ft=FORE_CHANNEL_K_FT_64,
        masts={
            name: {
                "x_ft": x,
                "heel_k_ft": heel,
                "rake_deg": rake,
                "length_ft": STEEL_64["mast"][name],
                "cut_ft": 0.0,
            }
            for name, (x, heel, rake) in MASTS.items()
        },
        mizen="course",
        channel_wale=[(x, z, z + CHANNEL_WALE_BREADTH_FT) for x, z in CHANNEL_WALE_FT],
        galleries=list(QUARTER_GALLERIES_FT),
        lights=list(STERN_LIGHTS),
        marks={
            "rail_m": "sourced",
            "breadth_m": "sourced",
            "keel_m": "sourced",
            "stem_m": "sourced",
            "stern_m": "sourced",
            "wales_m": "judged",  # its upper edge abaft 6 ft, under the gallery's finishing
            "section_m": "sourced",
            "decks_m": "judged",  # the roundhouse's line taken for its deck
            "ports_m": "judged",  # the half-breadths at the sills
            "port_size_m": "judged",  # the forecastle's and the roundhouse's
            "head_m": "sourced",
            "breadth_line_m": "sourced",
            "sections_m": "sourced",
            "channel_wales_m": "sourced",
            "form.stern": "sourced",
            "form.stern.knuckle_z_m": "sourced",
            "form.stern.transom_hb_m": "sourced",
            "form.stern.round_up_m": "sourced",
            "form.stern.galleries_m": "sourced",
            "form.stern.lights_m": "sourced",
            "form.head": "judged",
        },
    )


def lower_sill_half_breadth(x_ft):
    """The side's half-breadth at a gun-deck sill, feet outside the plank."""
    return interp(MAIN_BREADTH, x_ft) - LOWER_SILL_INSIDE_BREADTH_FT + PLANK_FT


def upper_sill_half_breadth(x_ft):
    """The side's half-breadth at an upper-deck sill, feet outside the plank."""
    tt, mb = interp(TOP_TIMBER, x_ft), interp(MAIN_BREADTH, x_ft)
    return tt + UPPER_SILL_FRACTION * (mb - tt) + PLANK_FT


def side_half_breadth_64(x_ft, z_ft):
    """The 64's side, moulded, at `x_ft` from AP and `z_ft` above WL1, between her main breadth
    and the top of her side: from the main-breadth line at its height of breadth to the
    top-timber line at her rail, along the midship section's shape between the same two lines
    there (its breadth at the upper height of breadth, its top at the waist rail), the height
    taken as the same share of the way up (judgement on measured lines; at midships it is the
    section as measured: Ind §2.3.2)."""
    z_b, z_t = interp(HEIGHT_OF_BREADTH, x_ft), interp(RAIL, x_ft)
    mb, tt = interp(MAIN_BREADTH, x_ft), interp(TOP_TIMBER, x_ft)
    share = min(max((z_ft - z_b) / (z_t - z_b), 0.0), 1.0)
    section = [(h - WL1_ABOVE_RABBET_FT, hb) for h, hb in SECTION]  # ft above WL1
    mid_b, mid_t = interp(HEIGHT_OF_BREADTH, MIDSHIPS_FT), interp(RAIL, MIDSHIPS_FT)
    flat, top = interp(section, mid_b), interp(section, mid_t)
    tumble = (flat - interp(section, mid_b + share * (mid_t - mid_b))) / (flat - top)
    return mb - tumble * (mb - tt)


def open_deck_sill(x_ft, deck_k_ft):
    """A port's sill on the 64's forecastle or roundhouse, feet above K, where no port is drawn:
    the deck and 0.41 m (Indf §3.3, judgement), or 2 in under the rail where the rail stands
    lower than that, the gun firing over it (judgement)."""
    rail_k = wl1_above_k(x_ft) + interp(RAIL, x_ft)
    return min(deck_k_ft + FORECASTLE_SILL_ABOVE_DECK_M / FT, rail_k - OVER_THE_RAIL_M / FT)


# ---------------------------------------------------------------------------
# The razee (Indf §1.5, §2-§4.5): the dockyard's work on the 64, as data
# ---------------------------------------------------------------------------

# Her load line, ZAZ2371's drawn waterline: 1.45 ft below WL1 aft and 1.47 ft forward, parallel
# to it within the image's resolution, ±0.25 ft (measured, 2371 against 1407F: Ind §2.3.1; D28
# (a)).
RAZEE_RISE_FT = (1.45, 1.47)
# The upper works taken off: the three 64s of 1794, "excepting the portion of bulwark that lay
# abaft the gangway-entrance, ... were cut down level with the upper deck" (James vol. 5 p. 428,
# OCR l. 21885-21887, read (OCR)), and the upper deck in the waist with them, gangways left
# along the sides (ZAZ2375, read). Her quarterdeck the old upper deck to its breast at 74.4 ft
# from AP, her forecastle from 118.5 ft (measured, ZAZ2375: Ind §2.3.5).
RAZEE_QUARTERDECK_BREAST_FT = 74.4
RAZEE_FORECASTLE_FT = 118.5
# Her roundhouse, the bulwark abaft the gangway-entrance that James excepts: the roundhouse of
# ZAZ2371's N.B., "shortened to the Beam abaft the Mizen" at Pellew's desire by the Navy Board's
# warrant of December 1794 (read, tentative: Ind table V10, §2.2), as she was in 1796 (the
# owner's answer, Build-Ships.md §19.1 item 18). Measured on ZAZ2371 at 1280 px (Ind's
# registration: 6.087 px to the foot by its scale strip, AP at the strip's zero by the post's
# heel, K the band's bottom; her line there 19.78 ft above K at AP against Ind's 19.81), where
# it gives them:
# - its deck: the 64's quarterdeck kept over her cabin (`DECKS_64`, measured on 1280T), which
#   ZAZ2371 draws in red, as it draws every deck of hers (her gun deck at midships 23.7 ft above
#   K there, 23.8 on 1280T), from her stern to the 64's roundhouse breast at 34.4 ft, within half
#   a foot of the 64's quarterdeck height abaft 21 ft and in two lines 0.5-1 ft lower forward of
#   it (measured): the proposal's roundhouse of September 1794 before the warrant shortened it
#   (judgement);
# - its aft end where that red line and the top of her side meet the quarter piece, 7.0-7.6 ft
#   abaft AP (measured);
# - its breast at the beam abaft the mizen: ZAZ2375 draws it as the pair of pink beam lines
#   22.1-23.4 ft from AP, 3-4 ft abaft the mizen hole, with the coach's fore bulkhead on its fore
#   side at 23.3 ft (Ind §2.3.5, measured; the beam measured here on 2375 registered on its two
#   bulkheads, 12.8 and 23.3 ft); the N.B.'s beam taken to be that one (judgement);
# - the top of her side over it: at the stern ZAZ2371's ink stands 0.2-0.5 ft above the deck's
#   height (40.0 ft above K 7.0 ft abaft AP: measured); forward of it the drawn top sweeps down
#   fair, without a step, under the red deck from about AP forward, to her quarterdeck rail's
#   height at the mizen (`RAZEE_DRAWN_SIDE_K_FT`, measured), and no rail is drawn over the deck:
#   a roundhouse's open rail (judgement). Her rail is taken 6 in above the deck from the stern
#   to the breast (judgement: a deck stands under its rail, freesail/ship/schema.py), over the
#   drawn top forward of AP, where it steps down to her quarterdeck rail at the warrant's beam,
#   a step no draught draws;
# - her taffrail: the top of her stern's outline, 10.4 ft abaft AP and 21.9 ft above WL1 (43.2
#   above K), which ZAZ2371 draws on the 64's measured stern line within half a foot from the
#   counter up (measured, ±0.2 ft): the 64's stern (`STERN`, 1407F) up to its point 22 ft above
#   WL1, 10 ft 3 in abaft AP. ZAZ2375's "taffrail" 5 ft 6 in abaft AP at the middle line is the
#   stern at her quarterdeck's height, where the 64's line stands 5.7 ft abaft it.
RAZEE_ROUNDHOUSE_FT = (-7.3, 23.3)
RAZEE_ROUNDHOUSE_RAIL_ABOVE_DECK_FT = 0.5
RAZEE_TAFFRAIL_ABOVE_WL1_FT = 22.0
# The top of her side as ZAZ2371 draws it over her quarterdeck, its topmost ink line (ft from AP,
# ft above K; measured there, ±0.2 ft, at five columns each, the guns' circles left out): one
# fair sweep from the stern to the mizen, no rail drawn over the red deck above it.
RAZEE_DRAWN_SIDE_K_FT = [
    (-6.7, 39.9), (-3.0, 39.6), (0.0, 39.2), (4.0, 38.7), (8.6, 38.3), (16.0, 37.6),
    (20.0, 37.3), (23.3, 37.0), (26.5, 36.8), (30.0, 36.5),
]  # fmt: skip
# Her sides (measured, ZAZ2371: Ind §2.3.5): the waist top-side about 30.8 ft above K, 6 in
# below the old upper deck; the quarterdeck rail about 4 ft 6 in above the quarterdeck (not
# re-measured), taken for the forecastle's too (judgement).
RAZEE_WAIST_SIDE_K_FT = 30.8
RAZEE_RAIL_ABOVE_DECK_FT = 4.5
# The breadth at her top-side in the waist, 37 ft 6 in moulded (measured on the midship
# section: Ind §2.3.2), taken along the waist at the same place between the top-timber and the
# main-breadth lines as at the midship section (judgement on measured lines); her quarterdeck
# rail's 34 ft is the top-timber line's.
RAZEE_WAIST_SIDE_FRACTION = (37.5 / 2.0 - 16.96) / (21.65 - 16.96)
# WL2, 3.77 ft below WL1 (measured, 1407T and 1407F: Ind §2.3.1-§2.3.2), its half-breadths at
# WL1_HALF_BREADTHS's stations, moulded (the post's 0.6 at AP taken for it, judgement); her own
# line's taken between WL1's and WL2's by her rise (judgement on measured lines).
WL2_BELOW_WL1_FT = 3.77
WL2_HALF_BREADTHS = [
    (0.0, 0.6), (10.0, 5.6), (20.0, 13.0), (30.0, 16.9), (40.0, 18.9), (50.0, 20.1),
    (60.0, 20.7), (70.0, 21.1), (80.0, 21.3), (90.0, 21.3), (100.0, 21.3), (110.0, 21.2),
    (120.0, 20.7), (130.0, 19.2), (140.0, 15.54), (150.0, 8.60), (155.0, 4.24),
]  # fmt: skip
# Her quarterdeck and forecastle ports (measured, ZAZ2375, ±0.5 ft: Ind §2.3.7), ft from AP:
# six a side on the quarterdeck, the first four the 64's upper-deck ports 1-4 within 0.8 ft;
# three on the forecastle, 6-9 ft before the 64's 11-13. Each 2 ft 9 in-3 ft 3 in wide (the mean
# taken); their depth the 64's upper-deck ports' (judgement).
RAZEE_QUARTERDECK_PORTS_FT = [6.9, 17.5, 28.2, 37.8, 47.4, 57.5]
RAZEE_FORECASTLE_PORTS_FT = [124.4, 134.7, 149.0]
RAZEE_QD_PORT_FT = (3.0, UPPER_PORT_FT[1])
# Her chase port a side for the two long 12s she carried from 1796 as bow chasers (D30 (a)):
# no bow port is measured, so at about +22.9 m (Indf §5.1), 155.1 ft from AP, before the
# catheads (ZAZ2375, from about 151 ft) and 5 ft 8 in abaft what stage A read as the stem head
# (the knighthead's after face, `KNIGHTHEAD_FT`), its sill and half-breadth found as the
# forecastle ports' are (judgement); a chaser's port is a triple of its deck at the chaser's x
# (Build-Ships.md §5.1). It stands 1.8 ft before the side's end at the 64's beakhead bulkhead
# (`BEAKHEAD_FT`), where her rail now ends; a gun's figure, it is not moved for the drawing
# (Build-Ships.md §5.0 principle 8), and its place is open for her stage B.
RAZEE_CHASE_PORT_FT = 155.1
# The lower masts cut at the heel (D19 (a)): each by the height of the deck taken off at that
# mast, so that each head stands as high above the deck worked as the 64's (the kit's account,
# the owner's notes V11; the cut measured on 1280T: Ind §3.3, judgement on measured decks).
RAZEE_CUT_FT = {"fore": 6.25, "main": 6.0 + 7.0 / 12.0, "mizzen": 6.75}
# Her mizen (D20 (a); Indf §4.5): Steel 1794 vol. I p. 40 (the page image, IA leaf n57, read):
# "Driver boom, the same length as the main-topsail-yard", 65 ft 4 in on the 64's; "gaffs 5/8
# of their booms", 40 ft 10 in.
RAZEE_BOOM_FT = STEEL_64["topsail_yard"]["main"]
RAZEE_GAFF_FT = 5.0 / 8.0 * RAZEE_BOOM_FT
# The spanker cut by the frigate-36's rule (gen_ships.frigate(): its head 0.9 of the gaff, its
# foot 0.9 of the boom, the gaff peaked 40 degrees; judgement there): the throat 3 ft below the
# mizen's hounds (the frigate's gaff). The boom's jaws: stage A's 6 ft 6 in above her quarterdeck,
# where the 64's mizen course had its tack (Steel's mizen course "within 6 or 7 feet of the deck"),
# cleared her taffrail as filed before her roundhouse was measured, then ran through her cabin
# under its deck; at stage B they are raised clear of it by the least that clears (the lead's
# notes of 2026-10-29, item 2; `spanker_cut`), the head room `HEAD_ROOM_FT` going first. Indf §4.5's
# hoist of 43.7 ft (about 240 m2) had the jaws about 1 ft above the deck, as the frigate's boom;
# at 6 ft 6 in it was 38.3 ft and 218 m2, which the owner kept (2026-10-29: "meant 218"; Indf §17),
# within 8% of Steel's driver for a 38 (202 m2): that 8% the check the raised cut must hold.
SPANKER_HEAD_OF_GAFF = 0.9
SPANKER_FOOT_OF_BOOM = 0.9
SPANKER_PEAK_DEG = 40.0
SPANKER_THROAT_BELOW_HOUNDS_FT = 3.0
SPANKER_BOOM_ABOVE_DECK_FT = 6.5
STEEL_DRIVER_38_M2 = 202.0
SPANKER_BAND_OF_38 = 0.08
# Her displacement against the 64's (Indf §2.1): the slice between the two lines, 238-244 tons
# of 35 cu ft (measured, 1407F, ±5%: Ind §2.3.3), at 1.016 t a ton.
SLICE_TONS = (238.0, 244.0)
TONNE_OF_TON = 1.016
# Her midship gun-deck sill, 6 ft 5 in above ZAZ2371's line (measured there: Ind §2.3.7), and
# her old upper deck at midships, 12 ft 0 in above it (measured, 2371 and 1280T: Ind §2.3.5):
# the independent measures the derivation is checked against (Indf §1.5), metres.
RAZEE_MIDSHIP_SILL_M = (1.96, 0.03)
RAZEE_OLD_UPPER_DECK_M = (3.66, 0.05)


def razeed(p64):
    """The razee of 1795 derived from the 64 as data (Indf §1.5): the dockyard's work applied by
    named steps, each writing its source into what it changes, and the derivation's checks
    raised before any file is written. Steps 5 and 7 change nothing: her topmasts,
    topgallants, every square yard, the crossjack and the studding-sail booms, and her bowsprit
    and jib-boom, are the 64's (D19 (a); D8 (b) as answered), standing on her new heads and in
    their place in the hull; her guns, people and stores (step 8) are her own (Indf §5-§7)."""
    p = the_rise(p64)
    p = the_upper_works(p)
    p = the_datum(p)
    p = the_heels_cut(p)
    p = the_mizen(p)
    p = her_hull(p)
    check_derivation(p64, p)
    return p


def the_rise(p):
    """Step 1: her water drops 1.45 ft aft and 1.47 ft forward against WL1, so that every height
    above it rises by as much at its station (D28 (a); Ind §2.3.1)."""
    return replace(p, rise_ft=RAZEE_RISE_FT)


def the_upper_works(p):
    """Step 2: the 64's quarterdeck, forecastle and their sides off, and the upper deck in the
    waist: her quarterdeck the old upper deck to its breast, her forecastle from 118.5 ft, her
    gun deck (`upper`) the 64's lower deck, and her short roundhouse over her cabin, the 64's
    quarterdeck kept from her stern to the beam abaft the mizen; her rail, stern, side and
    ports as the cut left them (James vol. 5 p. 428; ZAZ2371, ZAZ2374, ZAZ2375: Ind §2.2,
    §2.3.5, §2.3.7)."""
    old_upper = DECKS_64["upper"]
    qd_end, fc_start = RAZEE_QUARTERDECK_BREAST_FT, RAZEE_FORECASTLE_FT
    quarterdeck = [pt for pt in old_upper if pt[0] < qd_end] + [(qd_end, interp(old_upper, qd_end))]
    forecastle = [(fc_start, interp(old_upper, fc_start))] + [
        pt for pt in old_upper if pt[0] > fc_start
    ]
    # her roundhouse: the 64's quarterdeck from her stern to the beam abaft the mizen
    old_qd = DECKS_64["quarterdeck"]
    rh_aft, rh_breast = RAZEE_ROUNDHOUSE_FT
    roundhouse = (
        [(rh_aft, interp(old_qd, rh_aft))]
        + [pt for pt in old_qd if rh_aft < pt[0] < rh_breast]
        + [(rh_breast, interp(old_qd, rh_breast))]
    )
    decks = {
        "upper": list(DECKS_64["lower"]),
        "quarterdeck": quarterdeck,
        "forecastle": forecastle,
        "roundhouse": roundhouse,
    }

    def above_wl1(x_ft, z_k_ft):
        return round(z_k_ft - wl1_above_k(x_ft), 2)

    # the rail: her taffrail on the 64's stern line, her roundhouse's rail 6 in above its deck
    # to its breast, the quarterdeck's from there to the quarterdeck's breast, the waist
    # top-side, and the forecastle's rail to where her side ends at the 64's beakhead bulkhead,
    # kept with her head and bowsprit
    rail_above = RAZEE_RAIL_ABOVE_DECK_FT
    stern_line = [(z, x) for x, z in STERN if z is not None]
    taff_z = RAZEE_TAFFRAIL_ABOVE_WL1_FT
    taff = round(interp(stern_line, taff_z), 2)
    rail = [(taff, taff_z)]
    rail += [(x, above_wl1(x, z + RAZEE_ROUNDHOUSE_RAIL_ABOVE_DECK_FT)) for x, z in roundhouse]
    step = rh_breast + 0.1
    rail += [(step, above_wl1(step, interp(quarterdeck, step) + rail_above))]
    rail += [(x, above_wl1(x, z + rail_above)) for x, z in quarterdeck if x > step]
    rail += [
        (qd_end + 0.1, above_wl1(qd_end + 0.1, RAZEE_WAIST_SIDE_K_FT)),
        (fc_start - 0.1, above_wl1(fc_start - 0.1, RAZEE_WAIST_SIDE_K_FT)),
    ]
    rail += [(x, above_wl1(x, z + rail_above)) for x, z in forecastle]
    beak = BEAKHEAD_FT  # the 64's beakhead bulkhead, where her forecastle rail met the head
    rail += [(beak, above_wl1(beak, interp(forecastle, beak) + rail_above))]
    # the stern: the 64's post, counter and stern up to her taffrail, as ZAZ2371 draws it
    stern = [pt for pt in STERN if pt[1] is None or pt[1] < taff_z] + [rail[0]]
    # the top of her side: the 64's side at her roundhouse's, quarterdeck's and forecastle's
    # rails' height, the waist's top-side between them
    breadth = []
    for x, hb1 in WL1_HALF_BREADTHS:
        tt = interp(TOP_TIMBER, x)
        top = side_half_breadth_64(x, interp(rail, x))
        if qd_end < x < fc_start:
            top = tt + RAZEE_WAIST_SIDE_FRACTION * (interp(MAIN_BREADTH, x) - tt)
        breadth.append((x, hb1, top))  # her water's half-breadth is `her_hull`'s (step 9)
    # the ports: the 64's gun deck, and her quarterdeck and forecastle's at ZAZ2375's stations,
    # with her chase port before them
    old_sill = [(x, wl1_above_k(x) + s) for x, s in UPPER_SILLS]
    fc_ports = RAZEE_FORECASTLE_PORTS_FT + [RAZEE_CHASE_PORT_FT]
    ports = {
        "upper": list(p.ports["lower"]),
        "quarterdeck": [
            (x, interp(old_sill, x), upper_sill_half_breadth(x)) for x in RAZEE_QUARTERDECK_PORTS_FT
        ],
        "forecastle": [(x, interp(old_sill, x), upper_sill_half_breadth(x)) for x in fc_ports],
    }
    port_notes = {
        "upper": "her gun deck's thirteen a side, the 64's lower-deck ports kept (ZAZ2374 marks "
        "the same thirteen within 0.4 ft: Ind §2.3.7): every sill measured on ZAZ1407 at full "
        "resolution and raised by her rise, the half-breadths the 64's (judgement on measured "
        "lines)",
        "quarterdeck": "six a side at ZAZ2375's centres (measured, ±0.5 ft: Ind §2.3.7), the first "
        "four the 64's upper-deck ports 1-4 within 0.8 ft: the sill the 64's upper-deck sill line "
        "(measured on 1407F) at each port's station, raised by her rise (judgement; not "
        "re-measured on ZAZ2371); 2 ft 9 in-3 ft 3 in wide, the mean, and as deep as the 64's "
        "upper-deck ports (judgement); the half-breadth as at the 64's upper-deck sills "
        "(judgement on measured lines)",
        "forecastle": "three a side at ZAZ2375's centres (measured, ±0.5 ft: Ind §2.3.7): the "
        "sill the 64's upper-deck sill line at each station, held at her foremost upper-deck "
        "port's beyond it (judgement), raised by her rise; the size and the half-breadth as the "
        "quarterdeck's (judgement); and her chase port at 155.1 ft, for the bow chasers she "
        "carried from 1796 (D30 (a); no bow port measured, judgement), found as the others",
    }
    # the channel wale: the 64's, its top cut with her side in the waist to the waist's
    # top-side, as ZAZ2371 measures it (28.8-30.7 ft above K at midships: Ind §2.3.5)
    lower = [(x, z) for x, z, _ in p.channel_wale]
    upper = [(x, z) for x, _, z in p.channel_wale]
    waist = {qd_end, qd_end + 0.1, fc_start - 0.1, fc_start}
    channel_wale = []
    for x in sorted({x for x, _ in lower} | waist):
        top = interp(upper, x)
        if qd_end < x < fc_start:
            top = min(top, RAZEE_WAIST_SIDE_K_FT - wl1_above_k(x))
        channel_wale.append((x, interp(lower, x), top))
    # the stern: the 64's up to her taffrail; one tier of quarter gallery and its band of lights,
    # the 64's lower tier, the upper deck's, which ZAZ2371 draws in its place (tentative): her
    # cabin's, under her roundhouse
    taffrail_above = rail[0][1]
    tier, band = QUARTER_GALLERIES_FT[0], STERN_LIGHTS[0]

    def roundhouse_above_wl1(x_ft):
        return interp(roundhouse, x_ft) - wl1_above_k(x_ft)

    rise_aft = RAZEE_RISE_FT[0] + (RAZEE_RISE_FT[1] - RAZEE_RISE_FT[0]) * taff / 160.0
    taffrail_m = (taffrail_above + rise_aft) * FT
    # her roundhouse's rail over ZAZ2371's drawn top of her side forward of AP, where the drawn
    # top runs under her roundhouse's deck; and the drawn top at the mizen against her
    # quarterdeck rail
    drawn = RAZEE_DRAWN_SIDE_K_FT
    over_drawn = [
        z + RAZEE_ROUNDHOUSE_RAIL_ABOVE_DECK_FT - interp(drawn, x) for x, z in roundhouse if x > 0.0
    ]
    mizen_ft = p.masts["mizzen"]["x_ft"]
    qd_rail_at_mizen = interp(quarterdeck, mizen_ft) + rail_above
    # the 64's stem head above her forecastle deck: her head is not measured on ZAZ2371
    head_x, head_z = STEM_HEAD_FT
    head_above = wl1_above_k(head_x) + head_z - interp(forecastle, head_x)
    REPORT.setdefault("razee", {})["upper_works"] = (
        f"her taffrail {taffrail_m:.2f} m above her water; her quarterdeck rail "
        f"{qd_rail_at_mizen:.1f} ft above K at the mizen; her roundhouse's rail "
        f"{min(over_drawn):.1f}-{max(over_drawn):.1f} ft over ZAZ2371's drawn top forward of AP; "
        f"the stem head {head_above:.1f} ft above her forecastle deck; her transom's half-breadth "
        f"{interp(STERN_OUTLINE, taffrail_above):.2f} ft at her taffrail, moulded; the quarter "
        f"gallery's top {roundhouse_above_wl1(tier[0]) - tier[3]:.1f} ft under her roundhouse's "
        f"deck and {taffrail_above - tier[3]:.1f} ft under her taffrail, its after end "
        f"{tier[0] - taff:.1f} ft forward of her stern's top; the lights' top "
        f"{roundhouse_above_wl1(rh_aft) - band[1]:.1f} ft under the deck at her stern and "
        f"{taffrail_above - band[1]:.1f} ft under her taffrail."
    )
    notes = dict(p.profile_notes)
    notes.update(
        {
            "rail_m": "The top of her side, from her taffrail to where it ends at the 64's "
            "beakhead bulkhead: her taffrail, the top of her stern's outline, on the 64's stern "
            f"line {taffrail_above:g} ft above WL1 and {-taff:g} ft abaft AP (measured on ZAZ2371 "
            "at 10.4 ft and 21.9 ft, ±0.2 ft; the line measured on 1407F); her roundhouse's rail "
            "6 in above its deck from 7.3 ft abaft AP to its breast at the beam abaft the mizen, "
            f"{rh_breast:g} ft from AP (ZAZ2371 draws the top of her side 0.2-0.5 ft above that "
            "deck at the stern, measured; forward of it the drawn top sweeps down fair, without a "
            "step, under the red deck from about AP forward, "
            f"{interp(drawn, 4.0):.1f} ft above K at 4 ft from AP and "
            f"{interp(drawn, rh_breast):.1f} at the breast, to {interp(drawn, mizen_ft):.1f} at "
            "the mizen (measured, ±0.2 ft), "
            "with no rail drawn over the deck: a roundhouse's open rail, carried 6 in above the "
            "deck to the breast, judgement, over "
            "the drawn top forward of AP, since a deck stands under its rail; the step at the "
            "breast follows the warrant's beam, and no draught draws it), stepping down there to "
            "the quarterdeck rail, 4 ft 6 in above the quarterdeck (measured on ZAZ2371, not "
            "re-measured: Ind "
            "§2.3.5), to its breast at 74.4 ft; the waist top-side 30.8 ft above K (measured, "
            "2371); the forecastle's rail from 118.5 ft as the quarterdeck's (judgement), to the "
            "64's bulkhead at 153.3 ft (measured on 1407F), kept with her head and bowsprit and "
            "not measured on ZAZ2371 (judgement; Indf §3.5 items 3 and 9). Was, before her "
            "roundhouse was measured (2026-10-29): the quarterdeck rail aft to a taffrail 5 ft 6 "
            "in abaft AP (ZAZ2375's, the stern at her quarterdeck's height).",
            "stem_m": "The 64's stem's fore edge at her own line, from its foot boxed into the "
            "keel to the top of the stem head's fore face under the bowsprit (measured on 1407F), "
            "kept with her head and not measured on ZAZ2371 (judgement; Indf §3.5 items 3 and 9). "
            "The 64's knee of the head is her head_m.",
            "head_m": "The 64's knee of the head (measured on ZAZ1407) at her own line, kept with "
            "her head and bowsprit and not measured on ZAZ2371 (judgement): its fore edge from "
            "the band's square fore end on K, 147.75 ft from AP, where it leaves the stem's "
            "line, to the head's top.",
            "sections_m": "The 64's WL1 to WL5 by station, 5 to 159 ft from AP (measured, Ind "
            "§2.3.2: on 1407T to 130 ft, ±0.15 ft, ±0.5 at the ends; on 1407F from 140 ft, "
            "±0.1 ft), each 3.77 ft below the last (Ind §2.3.1), at her own line; with 4 1/2 in "
            "of plank.",
            "breadth_line_m": "The 64's main breadth by station, from AP to 155 ft, at her own "
            "line: the half-breadth plan's main-breadth line at the upper height of breadth "
            "drawn on the sheer plan (both measured on 1407F at full resolution), below her cut, "
            "with 4 1/2 in of plank.",
            "channel_wales_m": "The 64's channel wale (measured on 1407F at full resolution) at "
            "her own line, its top cut with her side in the waist to the waist's top-side, 30.8 "
            "ft above K: ZAZ2371 measures it 28.8-30.7 ft above K at midships (Ind §2.3.5), within "
            "0.1 ft of these.",
            "form.stern": "Square: the 64's up to her taffrail (ZAZ2371 draws it kept), the "
            "knuckle at the wing transom's ends, its round-up to the middle line and the "
            "transom's half-breadth there the 64's (measured on 1407F's body plan; the 64's post "
            "on 1407F runs on up to 8.0 ft above WL1, a reading not reconciled with it, open); "
            "at her taffrail, stern_m's top, the outline's half-breadth at that height "
            "(measured on 1407F's "
            "body plan, at her taffrail's height measured on ZAZ2371; judgement that her stern's "
            "face there is the 64's, none of her own draughts drawing it). One tier of quarter "
            "gallery and one band of five lights, the 64's lower tier, the upper deck's, her "
            "cabin's on her quarterdeck under her roundhouse (measured on 1407F; the lights read "
            "on ZAZ1953), which ZAZ2371 draws in its place, one tier of three lights, its sill "
            "about 4 ft 7 in above her aftmost gun-deck port's top as on 1407F and its ends within "
            "half a foot, at about 6 px to the foot: tentative (Build-Ships.md §19.1 item 18). "
            "Both stand under her taffrail and her roundhouse's deck, where her cabin is "
            "(`check_derivation`). Was, before her roundhouse "
            "was measured (2026-10-29): both above her taffrail as filed, the tier's after end "
            "abaft it, and the viewer drew them cut to her side and her transom.",
            "marks": "Each line's rung (Build-Ships.md §5.0 principles 3 and 4): sourced, "
            "measured on her own draughts (the 64's ZAZ1407, ZAZ1280, ZAZ1953; hers ZAZ2371, "
            "ZAZ2375) at her own line; judged, a judgement at its weakest point, which the line's "
            "note names.",
            "breadth_m": "By station: the half-breadth at her line, taken between "
            "WL1's and WL2's by her rise (measured lines, Ind §2.3.2; judgement between them), and "
            "at the top of her side: under the roundhouse's, quarterdeck and forecastle rails, the "
            "64's side at "
            "her rail's height, taken from the main-breadth line at its height of breadth to the "
            "top-timber line at the 64's rail along the midship section's shape between them (her "
            "quarterdeck rail about 34 ft across moulded at midships, the section's there: Ind "
            "§2.3.2), and in the waist her top-side, 37 ft 6 in across at midships, carried along "
            "between the top-timber and main-breadth lines (judgement on measured lines); each "
            "with 4 1/2 in of plank. Stage A took the 64's top-timber line under her rails, the "
            "64's breadth at the 64's own rails 3-10 ft higher.",
            "stern_m": "The 64's post, counter and stern (measured on 1407F: Ind §2.3.6) up to "
            f"her taffrail, {taffrail_above:g} ft above WL1 and {-taff:g} ft abaft AP, where "
            "ZAZ2371 draws her stern's outline on that line within half a foot and ends it "
            "(measured there: 10.4 ft abaft AP, 21.9 ft above WL1, ±0.2 ft). Was: the counter to "
            "the old upper deck's height 5 ft 6 in abaft AP (ZAZ2375's taffrail, the stern at her "
            "quarterdeck's height) and a bulwark above it to her quarterdeck rail (judgement), her "
            "roundhouse not yet in her profile.",
            "wales_m": "The 64's main wale (both edges tracked on 1407F at full resolution; abaft "
            "6 ft from AP its upper edge held, judgement) at her own line, kept below her cut: "
            "19.9-24.1 ft above K at 85-90 ft, where ZAZ2371 measures it 20.2-24.7 ft above K at "
            "midships (Ind §2.3.5, at about 6 px to the foot), 0.3-0.6 ft higher.",
            "decks_m": "Each deck at the middle line over its extent (the 64's, measured on 1280T: "
            "Ind §2.3.5): her gun deck the 64's lower deck; her quarterdeck the 64's upper deck to "
            "its breast at 74.4 ft and her forecastle from 118.5 ft (measured, ZAZ2375), the waist "
            "between them open but for the gangways along the sides; her roundhouse, over her "
            "cabin, the 64's quarterdeck kept from 7.3 ft abaft AP to the beam abaft the mizen, "
            f"{rh_breast:g} ft from AP, to which ZAZ2371's N.B. has it shortened in December 1794 "
            "(read, tentative: Ind table V10) and which ZAZ2375 draws at 22.1-23.4 ft, under the "
            "coach's fore bulkhead (measured; judgement that it is the N.B.'s beam). ZAZ2371 draws "
            "that deck in red, as it draws her decks, from her stern within half a foot of the "
            "64's quarterdeck height abaft 21 ft (measured), and on to the 64's roundhouse breast "
            "at 34.4 ft: the proposal of September 1794, before the warrant (judgement).",
        }
    )
    return replace(
        p,
        decks=decks,
        ports=ports,
        port_size_ft={
            "upper": LOWER_PORT_FT,
            "quarterdeck": RAZEE_QD_PORT_FT,
            "forecastle": RAZEE_QD_PORT_FT,
        },
        port_notes=port_notes,
        rail=rail,
        stern=stern,
        breadth=breadth,
        profile_notes=notes,
        fore_channel_k_ft=FORE_CHANNEL_K_FT_RAZEE,
        channel_wale=channel_wale,
        galleries=[tier],
        lights=[band],
        marks=dict(
            p.marks,
            rail_m="judged",  # her forecastle's rail, her roundhouse's rail over its deck
            breadth_m="judged",  # her water between WL1 and WL2, her waist's top-side
            stem_m="judged",  # her head not measured on ZAZ2371
            stern_m="sourced",  # was judged, her taffrail's height, now measured on ZAZ2371
            decks_m="judged",  # was sourced; her roundhouse's breast, the N.B.'s beam taken
            head_m="judged",  # her head not measured on ZAZ2371
            **{
                "form.stern.transom_hb_m": "judged",  # the 64's outline at her taffrail
                "form.stern.galleries_m": "judged",  # ZAZ2371 at 6 px to the foot
                "form.stern.lights_m": "judged",  # the 64's band, ZAZ2371 drawing no stern
            },
        ),
    )


def the_datum(p):
    """Step 3: D18 (c), the owner's choice (2026-10-29: "I say C, it looks slightly more right to
    me"; Indf §2.2, §17 item 1): her datum is her old upper deck at midships, 12 ft 0 in above
    her line (the 64's upper deck raised by her rise; measured on ZAZ2371 and 1280T: Ind
    §2.3.5), in place of (a), her gun deck at 1.39 m. In the waist that deck is gone but for the
    gangways (ZAZ2375), so it is her `datum_line`, not one of her decks there; the deck she is
    worked from in the waist stays her gun deck (`datum_deck`, which `deck_k_ft` reads), and her
    rig is cut above it as (a) cut it and written above the datum (`Particulars.frame_z`,
    `above_datum`), so that no spar, sail or mast stands elsewhere above her water. Plainly: (c)
    departs from the frigate-36's rule, the uppermost continuous deck (Build-Ships.md §5.5; Indf
    §2.2), which (a) kept."""
    return replace(p, datum_deck="upper", datum_line=list(DECKS_64["upper"]))


def the_heels_cut(p):
    """Step 4: each lower mast cut at the heel by `RAZEE_CUT_FT` (D19 (a); Ind §3.3), its head
    Steel's for the length the table gives, standing so much lower above K."""
    masts = {name: dict(m, cut_ft=RAZEE_CUT_FT[name]) for name, m in p.masts.items()}
    return replace(p, masts=masts)


def the_mizen(p):
    """Step 6: the 64's mizen yard and course give way to a gaff, a driver boom and a spanker
    (D20 (a); Indf §4.5)."""
    return replace(p, mizen="spanker")


def her_hull(p):
    """Step 9: her hull block, her own measured figures and not transforms (Indf §2.1; Ind
    §2.3-§2.4), and the half-breadths at her own water."""
    hull = {
        "length_waterline_m": 48.8,
        "beam_m": 13.54,
        "draught_m": 5.88,
        "displacement_kg": 1925000.0,
        "gm_m": 1.65,
        "clr_x_m": 4.5,
        "lateral_area_m2": 283.4,
        "hull_speed_kn": 14.0,
        "rudder": {"area_m2": 8.45, "max_angle_deg": 35, "rate_deg_s": 3.0, "span_m": 6.04},
    }
    hull_notes = {
        "length_waterline_m": "160 ft: WL1 rabbet to rabbet, as the 64's (D29 (b): Ind §2.3.2, "
        "§2.4); 163.8 ft (49.9 m) outside the post and the stem at her own line (measured, Ind "
        "§2.3.6).",
        "beam_m": "44 ft 5 in extreme as built (Winfield 1793-1817 p. 100; D34 (a)): the cut took "
        "nothing off her breadth.",
        "draught_m": "19 ft 3 in mean to K, the band's bottom, at ZAZ2371's drawn line, 1.45 ft "
        "aft and 1.47 ft forward below WL1 (measured, 2371 against 1407F, ±0.25 ft: Ind §2.3.1; "
        "D28 (a), D29 (b)); 5.71 m to the main keel. Osler's 'nineteen and a half feet abaft' "
        "(p. 111, May 1795) lies within that line's ±0.25 ft.",
        "displacement_kg": "1,925 t: judgement within the band integrated on her measured lines, "
        "1,900-1,955 t (Ind §2.3.3), the 64's 2,170 t less the slice measured between the two "
        "lines, 238-244 tons of 35 cu ft (Indf §2.1).",
        "gm_m": "5 ft 5 in: judgement within 1.5-1.8 m (Ind §2.3.4): KM measured 7.25 m above K, "
        "her KG about 1 ft lower than the 64's for the upper works and the 18- and 9-pounders "
        "taken off; no period figure for either was found.",
        "clr_x_m": "The measured centroid of the plane the file counts (hull and band, no rudder), "
        "0.58-0.64 m abaft the middle of the load line (Ind §2.3.6), with the frigate-36's tuned "
        "lead of 9.6% of her load line ahead of it (Indf §2.1; judgement), tuned against the "
        "helm's truths (6 and 17; Indf §9, §16 item 6). Forward of that at stage B, her spanker "
        "cut smaller on its boom raised clear of her roundhouse having taken her helm away, to "
        "stand it near the frigate-36's (judgement; the truths held at the start). Measured, old "
        "beside new, in docs/dev/TuningNotes.md, and held by her tests.",
        "lateral_area_m2": "Below her line with the band, the rudder left out, as the frigate's "
        "(measured, 1407F at 1.45 ft below WL1: 3,050-3,052 sq ft; Ind §2.3.6).",
        "hull_speed_kn": "D24 (a): the frigate-36's 13.0 carried by the root of the lengths, "
        "sqrt(160/137) = 14.05 (Indf §2.1), tuned only within 13-14.5; no period knots for her "
        "were found (Ind §7). Kept at its start: the band cannot bear out the Virginie chase "
        "close-hauled and running large against the frigate-36 (Indf §9; measured in "
        "docs/dev/TuningNotes.md, reported and not forced). The owner (2026-10-29; Indf §17): "
        "left to the tuning of both ships against the period's accounts, the razee perhaps right "
        "and the frigate-36 too fast, or the razee too slow and the frigate-36 right, neither "
        "presumed the one at fault (truth 7-187's fourth clause). Plainly: the 64 and the razee "
        "have one length, so the gap between their figures is the decision's ranking, not the "
        "waterline's.",
        "deck_height_m": "Her old upper deck at midships, 12 ft 0 in above her line (the 64's "
        "upper deck, measured on 1280T, raised by her rise; 12 ft 0 in, 3.66 m, on ZAZ2371 and "
        "1280T: Ind §2.3.5): D18 (c), the owner's choice "
        "(2026-10-29: 'I say C, it looks slightly more right to me'; Indf §2.2, §17 item 1), in "
        "place of (a), her gun deck at midships, 4 ft 7 in above her line, the uppermost "
        "continuous deck and still the deck she is worked from in the waist, which has gangways "
        "only (ZAZ2375). The datum of every spar height and every sail's corners: her rig is cut "
        "above her gun deck as (a) cut it and written above this datum, none moved above her "
        "water, and each lower mast's x_m its place at this height, raked from its partners. "
        "Plainly: (c) departs from the frigate-36's rule, the uppermost continuous deck "
        "(Build-Ships.md §5.5; Indf §2.2). What it moves in the engine is what reads the datum or "
        "a height written above it: the deck's wind's eye (physics/sails.py, physics/hull.py), "
        "with the readings' datum (api/readings.py); each lower mast's windage, which "
        "physics/sails.py takes from the datum to its head (`_spar_windage_area`, "
        "`_spar_centre_height`); the blanket's reach, three times her tallest lower mast's "
        "written height (physics/sails.py); and the spanker sheet's lead (evolutions/trim.py), "
        "the boom's written height its drop to the horse. The lookout's eye (world/lookout.py), "
        "the datum and her lower mast and topmast together, does not move. Measured in "
        "docs/dev/TuningNotes.md.",
        "rudder": "The 64's (ZAZ2371 shows the same stepped outline), measured on 1407F at her "
        "line (Ind §2.3.6): 90.4-91.8 sq ft below it, span 19 ft 10 in; 35 degrees and 3 deg/s "
        "the frigate-36's (judgement).",
    }
    aft, fwd = p.rise_ft
    breadth = []
    for x, _, top in p.breadth:
        rise = aft + (fwd - aft) * x / 160.0
        hb1, hb2 = interp(WL1_HALF_BREADTHS, x), interp(WL2_HALF_BREADTHS, x)
        breadth.append((x, hb1 + (hb2 - hb1) * rise / WL2_BELOW_WL1_FT, top))
    return replace(
        p,
        key="razee",
        file="razee-44.yaml",
        era_notes="HMS Indefatigable as razeed, 1795: the Ardent-class 64 of 1784 cut down to a "
        "frigate by the Navy Office's draught of September 1794 (ZAZ2371), her quarterdeck, "
        "forecastle and their sides taken off and her lower masts shortened, rated a 44 (Winfield "
        "1793-1817 pp. 99-100; James vol. 1 p. 454, vol. 5 p. 428). Derived from the 64's file as "
        "data: her hull and lines the 64's measured on her draughts (ZAZ1407, ZAZ1280) at her "
        "own line (ZAZ2371), her spars the 64's by Steel 1794 vol. I p. 49 with her lower masts "
        "cut at the heel and a gaff and driver boom by Steel's rule; see "
        "tools/ships/indefatigable.py for every figure and judgement.",
        header=(
            "# HMS Indefatigable as razeed, 1795: the 64 of 1784 cut down to a 44-gun frigate.\n"
            "# Generated by tools/gen_ships.py (tools/ships/indefatigable.py); edit those and\n"
            "# rerun, do not edit this file. Derived from the 64 as data (razeed()): her hull\n"
            "# and profile the 64's measured on her draughts (RMG ZAZ1407, ZAZ1280) at her own\n"
            "# line (ZAZ2371, ZAZ2375; docs/design/Research-Indefatigable-2026-10.md). Spars:\n"
            "# Steel 1794 vol. I p. 49, the 64 column, her lower masts cut at the heel, her\n"
            "# topgallant masts with Steel's long pole-heads (pp. 16, 42); her gaff and driver\n"
            "# boom by Steel's rule (p. 40). Sails: Steel's table IV, the 64 column, the\n"
            "# topgallants and royals cut to the spars (the owner's rule).\n"
            "# Her datum is her old upper deck at midships (D18 (c), the owner's choice), a\n"
            "# departure from the frigate-36's rule, the uppermost continuous deck.\n"
            "# Units: metres, m2, kg, kN. Comments mark each judgement.\n"
        ),
        hull=hull,
        hull_notes=hull_notes,
        breadth=breadth,
    )


def mast_head_k_ft(m):
    """A lower mast's head above K, feet, as `write()` stands it: its heel on its step and its
    length less any cut at the heel (the razee's; Indf §4.1)."""
    return m["heel_k_ft"] + (m["length_ft"] - m["cut_ft"])


def check_derivation(p64, p):
    """The derivation's checks (Indf §1.5), raised before any file is written: her midship sill
    and her old upper deck against ZAZ2371's independent measures, each lower mast's head as
    `write()` stands it lower above K than the 64's by its cut (so no step but the fourth moves
    a heel or a length), and her displacement less by the measured slice; her datum that old
    upper deck (D18 (c)) and her working deck in the waist her gun deck; her roundhouse ending
    abaft her mizen, and her quarter gallery and stern lights under her taffrail and her
    roundhouse's deck, where her cabin is."""
    sill = p.z_m(interp([(x, z) for x, z, _ in p.ports["upper"]], MIDSHIPS_FT), MIDSHIPS_FT)
    want, tol = RAZEE_MIDSHIP_SILL_M
    if abs(sill - want) > tol:
        raise ValueError(
            f"The razee's midship gun-deck sill stands {sill:.3f} m above her water, more than "
            f"{tol} m from ZAZ2371's measured {want} m (Indf §1.5)."
        )
    old_upper = p.z_m(interp(DECKS_64["upper"], MIDSHIPS_FT), MIDSHIPS_FT)
    want, tol = RAZEE_OLD_UPPER_DECK_M
    if abs(old_upper - want) > tol:
        raise ValueError(
            f"The razee's old upper deck stands {old_upper:.3f} m above her water at midships, "
            f"more than {tol} m from the {want} m measured on ZAZ2371 and 1280T (Indf §1.5)."
        )
    gun_deck = p.z_m(interp(p.decks["upper"], MIDSHIPS_FT), MIDSHIPS_FT)
    if p.datum_z != round(old_upper, 2) or p.frame_z != round(gun_deck, 2):
        raise ValueError(
            f"The razee's datum stands {p.datum_z} m and her frame {p.frame_z} m above her water, "
            f"not her old upper deck's {old_upper:.3f} m (D18 (c)) and her gun deck's "
            f"{gun_deck:.3f} m at midships (Indf §2.2)."
        )
    breast, mizen = p.decks["roundhouse"][-1][0], p.masts["mizzen"]["x_ft"]
    if not breast < mizen:
        raise ValueError(
            f"The razee's roundhouse runs to {breast} ft from AP, not abaft her mizen at {mizen} "
            "ft (ZAZ2371's N.B.: 'shortened to the beam abaft the mizen')."
        )
    taff_x, taff_z = p.stern[-1]
    for aft, fore, _low, high in p.galleries:
        deck = min(interp(p.decks["roundhouse"], x) - wl1_above_k(x) for x in (aft, fore))
        if not (high < min(taff_z, deck) and aft > taff_x):
            raise ValueError(
                f"The razee's quarter gallery ({aft}-{fore} ft, top {high} ft above WL1) does not "
                f"stand under her taffrail ({taff_x}, {taff_z}) and her roundhouse's deck."
            )
    for _low, high, _n, _hb in p.lights:
        deck = interp(p.decks["roundhouse"], taff_x) - wl1_above_k(taff_x)
        if not high < min(taff_z, deck):
            raise ValueError(
                f"The razee's stern lights (top {high} ft above WL1) do not stand under her "
                f"taffrail ({taff_z} ft) and her roundhouse's deck ({deck:.2f} ft)."
            )
    for name, m in p.masts.items():
        lower = mast_head_k_ft(p64.masts[name]) - mast_head_k_ft(m)
        if abs(lower - RAZEE_CUT_FT[name]) > 1e-9:
            raise ValueError(
                f"The razee's {name} mast head stands {lower:.3f} ft lower above K than the "
                f"64's, not by its cut of {RAZEE_CUT_FT[name]:.3f} ft (Indf §1.5)."
            )
    slice_tons = (p64.hull["displacement_kg"] - p.hull["displacement_kg"]) / 1000.0 / TONNE_OF_TON
    if not SLICE_TONS[0] <= slice_tons <= SLICE_TONS[1]:
        raise ValueError(
            f"The razee displaces {slice_tons:.1f} tons of 35 cu ft less than the 64, outside the "
            f"slice measured between their lines, {SLICE_TONS[0]:g}-{SLICE_TONS[1]:g} (Indf §1.5)."
        )


# ---------------------------------------------------------------------------
# The file
# ---------------------------------------------------------------------------


class HerBuilder(g.Builder):
    """The generator's Builder, with the figures its shared helpers compute from her own keys
    kept out of her notes (the lead's notes of 2026-10-29, item 2): a spar's rating, which is its
    `rating_kn`; a bowline's size and a staysail's sheet's, which are in their ratings; a
    staysail's area and sides, which are its corners; her hold's tons. What each rule is and what
    it read stays. The eight files keep their notes as they are."""

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
        """`Builder.rate_spars`, its figures left in the file's `rating_kn` alone (`dump` calls
        this last, when every note is written)."""
        super().rate_spars()
        self.notes = {key: self._plain_of_figures(note) for key, note in self.notes.items()}

    def hold(self, capacity_tons, note):
        super().hold(
            capacity_tons, note.replace(f"room for {capacity_tons} tons of cargo", "room for cargo")
        )


def hull_block(p):
    """Her hull dict with its profile as the last key (Build-Ships.md §5.1), and its notes."""
    hull = dict(p.hull)
    hull["deck_height_m"] = p.datum_z
    rudder = hull.pop("rudder")
    hull["rudder"] = rudder
    notes = dict(p.hull_notes)

    def pt(x_ft, z_wl1_ft):
        """A point measured above WL1, as the file's [x, z] above her own water."""
        return [x_m(x_ft), p.z_m(wl1_above_k(x_ft) + z_wl1_ft, x_ft)]

    def k(x_ft):
        return [x_m(x_ft), p.z_m(0.0, x_ft)]

    stem = [pt(x, z) for x, z in STEM]
    stern = [k(x) if z is None else pt(x, z) for x, z in p.stern]
    rail = [pt(x, z) for x, z in p.rail]
    breadth = [[x_m(x), (hb + PLANK_FT) * FT, (top + PLANK_FT) * FT] for x, hb, top in p.breadth]
    wales = [[x_m(x), pt(x, lo)[1], pt(x, hi)[1]] for x, lo, hi in MAIN_WALE_FT]
    rabbet_k = wl1_above_k(MIDSHIPS_FT) - WL1_ABOVE_RABBET_FT
    section = [[p.z_m(rabbet_k + h, MIDSHIPS_FT), (hb + PLANK_FT) * FT] for h, hb in SECTION]
    decks = {word: [[x_m(x), p.z_m(z, x)] for x, z in pts] for word, pts in p.decks.items()}
    ports = {
        word: [[x_m(x), p.z_m(z, x), hb * FT] for x, z, hb in triples]
        for word, triples in p.ports.items()
    }
    sizes = {word: [w * FT, d * FT] for word, (w, d) in p.port_size_ft.items()}
    # her shape (stage B; Indf §3.5 item 8), drawn only: nothing the physics, the guns or the
    # lee ports read is taken from it (Build-Ships.md §5.0 principle 8)
    head = [k(x) if z is None else pt(x, z) for x, z in KNEE_OF_THE_HEAD]
    breadth_line = [
        pt(x, z) + [(interp(MAIN_BREADTH, x) + PLANK_FT) * FT] for x, z in HEIGHT_OF_BREADTH
    ]
    sections = [pt(x, z) + [(hb + PLANK_FT) * FT] for x, z, hb in waterline_points()]
    channel_wales = [[x_m(x), pt(x, lo)[1], pt(x, hi)[1]] for x, lo, hi in p.channel_wale]
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
    notes["profile"] = (
        "Her side, decks and ports (Indf §3; Build-Ships.md §5.1): x forward of the middle of "
        "the load line, z above her load water at each station, metres; every point measured "
        "on her draughts but where its line's note says judgement."
    )
    notes["profile.rail_m"] = p.profile_notes["rail_m"]
    notes["profile.breadth_m"] = p.profile_notes["breadth_m"]
    notes["profile.keel_m"] = (
        "K, the band's bottom, from the post's heel to its square fore end (Ind §2.3.6)."
    )
    notes["profile.stem_m"] = p.profile_notes["stem_m"]
    notes["profile.stern_m"] = p.profile_notes["stern_m"]
    notes["profile.wales_m"] = p.profile_notes["wales_m"]
    notes["profile.section_m"] = (
        "The midship section, ZAZ1407's outermost (measured, 1407T, ±0.15 ft: Ind §2.3.2), with 4 "
        "1/2 in of plank."
    )
    notes["profile.decks_m"] = p.profile_notes["decks_m"]
    for word, text in p.port_notes.items():
        notes[f"profile.ports_m.{word}"] = text[0].upper() + text[1:] + "."
    for key in ("head_m", "breadth_line_m", "sections_m", "channel_wales_m", "form"):
        notes[f"profile.{key}"] = p.profile_notes[key]
    notes["profile.form.stern"] = p.profile_notes["form.stern"]
    notes["profile.form.head"] = p.profile_notes["form.head"]
    notes["profile.marks"] = p.profile_notes["marks"]
    # the stern's features at AP, the knuckle and the transom by the body plan's outline: the
    # knuckle the wing transom's ends, where the side closes to the transom (freesail/ship/
    # form.py's closure), its middle rounded up above them
    middle, knuckle, end_hb = WING_TRANSOM_FT
    taffrail = p.stern[-1][1]
    form = {
        "stern": {
            "type": "square",
            "knuckle_z_m": pt(0.0, knuckle)[1],
            "transom_hb_m": [
                (interp(STERN_OUTLINE, taffrail) + PLANK_FT) * FT,
                (end_hb + PLANK_FT) * FT,
            ],
            "round_up_m": (middle - knuckle) * FT,
            "galleries_m": [
                [x_m(aft), x_m(fore)] + [pt(0.5 * (aft + fore), z)[1] for z in (low, high)]
                for aft, fore, low, high in p.galleries
            ],
            "lights_m": [
                [pt(0.0, low)[1], pt(0.0, high)[1], n, hb * FT] for low, high, n, hb in p.lights
            ],
        },
        "head": "figure",
    }
    # no port triple's half-breadth was measured at its port (Indf §3.3, §3.5 item 8: each is
    # judgement on the measured lines), so every gap is reported and none raises
    drawn = REPORT.setdefault(p.key, {}).setdefault("hull", [])
    drawn.clear()
    g.hull_form(hull, form=form, marks=p.marks, measured=(), report=drawn)
    return hull, notes


def waterline_points():
    """WL1 to WL5 by station as sourced section points, (ft from AP, ft above WL1, half-breadth
    moulded), each station low to high (Ind §2.3.2; `WATERLINES`): WL1 at full resolution where
    `WL1_HALF_BREADTHS` gives the station, a waterline ended at the rabbet left out."""
    wl1 = dict(WL1_HALF_BREADTHS)
    out = []
    for x, row in WATERLINES.items():
        hbs = (wl1.get(x, row[0]), *row[1:])
        points = [(x, -i * WL2_BELOW_WL1_FT, hb) for i, hb in enumerate(hbs) if hb is not None]
        out += sorted(points, key=lambda q: q[1])
    return out


def write(out_dir, p):
    """Build one variant's file in full and dump it to `out_dir`."""
    hull, hull_notes = hull_block(p)
    b = HerBuilder(p.name, "ship", p.era_notes, hull, hull_notes)
    # the frame her rig is cut in: the deck she is worked from at midships, her datum where the
    # two are one (the 64's); every height cut above it is written above her datum (D18;
    # `above_datum`), every mast's place at it (`mast_x_at_datum`)
    frame = p.frame_z
    frame_ft = frame / FT

    # -- the masts' geometry, feet above the frame, keyed as the frigate's (Indf §1.3) --------
    geom, mast_x, rake = {}, {}, {}
    for name, m in p.masts.items():
        L = m["length_ft"] - m["cut_ft"]
        head = head_ft(m["length_ft"], HEAD_IN_PER_YARD["mast"][name])
        # the heel on its step in the hold; a mast cut at the heel (the razee's) stands lower
        # by its cut, its head Steel's for the length the table gives (Indf §4.1)
        above = (mast_head_k_ft(m) - p.water_ft(m["x_ft"])) - frame_ft
        T = STEEL_64["topmast"][name]
        t_head = head_ft(T, HEAD_IN_PER_YARD["topmast"][name])
        t_hoist = T - head  # above the lower cap: the doubling is the lower mast head
        G = STEEL_64["topgallant_mast"][name]
        g_square = head_ft(G, HEAD_IN_PER_YARD["topgallant_mast"][name])
        to_stop = G - g_square  # the listed length less its square head (Bel §4.2)
        pole = LONG_POLE_OF_STOP * to_stop  # the long pole-head, set up from the stop
        g_hoist = to_stop - t_head  # above the topmast cap, to the stop under the pole
        tg_hounds = HOUNDS_OF_STOP * g_square  # the topgallant yard's hoist below the stop
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
            "yard": STEEL_64["yard"][name],
            "topsail_yard": STEEL_64["topsail_yard"][name],
            "tg_yard": STEEL_64["tg_yard"][name],
            "royal_yard": STEEL_64["royal_yard"][name],
            # the frigate's rules (gen_ships.frigate): the lower yards slung 2 ft below the
            # hounds, the topsail yards hoisted to the topmast hounds; the topgallant yards to
            # the topgallant's hounds, under the stop; the royals a foot below the pole's head
            "yard_h": above - head - 2.0,
            "topsail_h": above + t_hoist - t_head,
            "tg_h": above + t_hoist + g_hoist - tg_hounds,
            "royal_h": above + t_hoist + g_hoist + pole - 1.0,
        }
        mast_x[name] = round(x_m(m["x_ft"]), 2)
        rake[name] = m["rake_deg"]

    yard_lengths = {"course": "yard", "topsail": "topsail_yard", "topgallant": "tg_yard"}
    yard_lengths["royal"] = "royal_yard"
    yard_heights = {"course": "yard_h", "topsail": "topsail_h", "topgallant": "tg_h"}
    yard_heights["royal"] = "royal_h"
    level_of_spar = {"course": "lower", "topsail": "topsail", "topgallant": "topgallant"}
    level_of_spar["royal"] = "royal"
    below = {"topgallant": "topsail_h", "royal": "tg_h"}

    # -- the square sails: Steel's below the topmast caps, cut to the spars above them ---------
    def cut(sid, level, gm):
        head_cl, foot_cl, depth_yd = STEEL_SAILS_64[sid]
        head_w, foot_w = head_cl * CLOTH_IN_SAIL_FT, foot_cl * CLOTH_IN_SAIL_FT
        hung = gm[yard_heights[level]]
        if level in below:
            # the owner's rule (Build-Ships.md §19.1 item 5): the spars rule over Steel's sail
            # table above the topmast caps; the sail cut between its yard and the yard below
            depth = hung - gm[below[level]]
        else:
            depth = 3.0 * depth_yd
        area = round((head_w + foot_w) / 2.0 * depth * FT * FT)
        # the centre of the trapezoid, its head on its yard
        drop = depth * (head_w + 2.0 * foot_w) / (3.0 * (head_w + foot_w))
        centre = round(frame + (hung - drop) * FT, 1)
        table = round((head_w + foot_w) / 2.0 * 3.0 * depth_yd * FT * FT)
        return area, centre, head_cl, foot_cl, depth_yd, depth, table

    areas = {}
    for name, levels in BRACE_PLANS.items():
        for level, _ in levels:
            sid = sail_of(name, level)
            areas[sid] = cut(sid, level, geom[name])

    # the after sail, its corners in the drawings' frame so that its area and centre are its
    # cut's: the 64's mizen course (Indf §4.4), its tack on the mast above the quarterdeck; the
    # razee's spanker on her gaff and driver boom (§4.5)
    if p.mizen == "course":
        mizen = mizen_course_cut(p, geom["mizzen"], mast_x["mizzen"], rake["mizzen"], frame)
    else:
        mizen = spanker_cut(p, geom["mizzen"], mast_x["mizzen"], rake["mizzen"], frame)
    # the headsails, each a triangle on its stay (below)
    bow = head_geometry(p, geom, mast_x, rake, frame)
    plain = (
        sum(areas[s][0] for s in areas if not s.endswith(".royal"))
        + sum(h["area"] for sid, h in bow["sails"].items() if sid != "fore.staysail")
        + mizen["area"]
    )
    # her rope: the frigate's scaled by the root of her plain sail over the frigate's, so that a
    # line's rating grows with the sail it works (Indf §4.2; judgement); Steel's rigging table
    # for a 64 (vol. II, '64 Gun Ship', OCR l. 24803-24890) is legible in part: the mizen yard's
    # and the driver's lines are read against it (`mizen_course`, `mizen_driver`), and the rest
    # are the check still to make
    rope_scale = math.sqrt(plain / FRIGATE_PLAIN_SAIL_M2)
    REPORT.setdefault(p.key, {})["rope"] = (plain, rope_scale)

    yards_by_level = {"course": [], "topsail": [], "topgallant": [], "royal": []}
    sails_by_level = {"course": [], "topsail": [], "topgallant": [], "royal": []}
    prov = " Provisional (truth 9), see gen_ships.py."
    for name in ("fore", "main", "mizzen"):
        gm = geom[name]
        m = p.masts[name]
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
        stick = f"{name} lower mast {fmt_ft(gm['length'])} (Steel 1794 vol. I p. 49, the 64)"
        if m["cut_ft"]:
            stick = (
                f"{name} lower mast {fmt_ft(gm['length'])}: the 64's {fmt_ft(m['length_ft'])} "
                f"(Steel 1794 vol. I p. 49) cut {fmt_ft(m['cut_ft'])} at the heel, the height of "
                "the 64's deck above the old upper deck at the mast (D19 (a): the kit's account, "
                "the cut measured on 1280T, Ind §3.3)"
            )
        x_file = mast_x_at_datum(p, x, rake[name])
        placed = (
            ""
            if x_file == x
            else " Its x_m its place at the datum, raked from the partners on her gun deck "
            "(D18 (c)), so that it stands where it did."
        )
        lower = b.spar(
            f"{name}.mast",
            "mast",
            x_m=x_file,
            rake_deg=rake[name],
            height_m=above_datum(p, g.ft(gm["above"])),
            rating_kn=g.design_kn(carried["lower"], g.DESIGN_WIND_KN["lower"]),
            note=f"{stick}, its head {fmt_ft(gm['head'])} by Steel's rule; its heel "
            f"{m['heel_k_ft']:.2f} ft above K and its place at the lower-deck partners "
            f"{m['x_ft']:.2f} ft from AP, raking {rake[name]} deg (measured, ZAZ1280: Ind §3.1)."
            f"{placed}{prov}",
        )
        top = b.spar(
            f"{name}.topmast",
            "topmast",
            steps_on=lower,
            height_m=g.ft(gm["t_hoist"]),
            rating_kn=g.design_kn(carried["topsail"], g.DESIGN_WIND_KN["topsail"]),
            note=f"{name} topmast {fmt_ft(gm['t_len'])} (Steel p. 49), its hoist above the lower "
            f"cap the length less the lower mast head, its head {fmt_ft(gm['t_head'])} by Steel's "
            f"rule.{prov}",
        )
        tg = b.spar(
            f"{name}.topgallant_mast",
            "topgallant_mast",
            steps_on=top,
            height_m=g.ft(gm["g_hoist"]),
            rating_kn=g.design_kn(carried["topgallant"], g.DESIGN_WIND_KN["topgallant"]),
            note=f"{name} topgallant mast {fmt_ft(gm['g_len'])} with its royal pole, one stick "
            "(Steel p. 49: no royal masts in the 64's column): its height the listed length less "
            "its square head of 3 1/2 in to a yard, up to the stop, above the topmast cap; Steel's "
            "long pole-head, two-thirds of the length to the stop, set up from the stop above it "
            "(Steel 1794 vol. I p. 16, OCR l. 2934-2942, and p. 42, OCR l. 4701-4702, read as "
            "Bel "
            "§4.2 reads them, judgement; the owner, "
            "2026-10-29: Indf §17). Stage A read a common pole of seven-eighteenths within the "
            f"listed length.{prov}",
        )
        royal = b.spar(
            f"{name}.royal_mast",
            "royal_mast",
            steps_on=tg,
            height_m=g.ft(gm["r_hoist"]),
            rating_kn=g.design_kn(carried["royal"], g.DESIGN_WIND_KN["royal"]),
            note=f"{name} royal pole, the topgallant mast's own long pole-head (Steel 1794 vol. I "
            "p. 16, OCR l. 2934-2942, and p. 42, OCR l. 4701-4702; Bel §4.2), filed as a royal "
            "mast stepped on it as the frigate-36 files "
            f"hers, so that the royal yard has its own spar (Indf §4.1).{prov}",
        )
        on_spar = {"course": lower, "topsail": top, "topgallant": tg, "royal": royal}
        factor = g.FRIGATE_MAST_ROPE_FACTOR[name] * rope_scale
        for level, limit in BRACE_PLANS[name]:
            yard_id = f"{name}.{level}.yard" if level != "course" else f"{name}.yard"
            sail_id = sail_of(name, level)
            area, centre, head_cl, foot_cl, depth_yd, depth, table = areas[sail_id]
            yard = b.spar(
                yard_id,
                "yard",
                on=on_spar[level],
                length_m=g.ft(gm[yard_lengths[level]]),
                height_m=above_datum(p, g.ft(gm[yard_heights[level]])),
                brace_limit_deg=limit,
                rating_kn=g.design_kn(
                    carried[level_of_spar[level]], g.DESIGN_WIND_KN[level_of_spar[level]]
                ),
                note=f"{name} {level} yard {fmt_ft(gm[yard_lengths[level]])} (Steel p. 49, the "
                f"64); braces {limit} deg from square (the frigate-36's, Fincham 1843 art. 102; "
                "judgement for her, Indf §4.2), kept by the owner with the lee topmast backstays "
                f"eased when braced sharp up (2026-10-29; Indf §17).{prov}",
            )
            reef = REEFS[level] if not isinstance(REEFS[level], dict) else REEFS[level][name]
            canvas = g.FRIGATE_CANVAS[sail_id]
            if level in ("topgallant", "royal"):
                how = (
                    "cut between its yard and the yard below as the spars stand on Steel's long "
                    "pole-heads (Steel 1794 vol. I p. 16, OCR l. 2934-2942, and p. 42, OCR l. "
                    "4701-4702; Bel §4.2; the owner, 2026-10-29: "
                    f"Indf §17), on Steel's cloths ({head_cl:g} at the head, {foot_cl:g} at the "
                    "foot): the spars rule over the sail table (the owner's answer, Build-Ships.md "
                    f"§19.1 item 5), short of table IV's {depth_yd:g} yards deep, {table} m2"
                )
            else:
                how = (
                    f"Steel's table IV, the 64: {head_cl:g} cloths at the head, {foot_cl:g} at "
                    f"the foot, {depth_yd:g} yards deep, 22 1/2 in a cloth in the sail (Ind §5; "
                    f"±10%, judgement); {reef} reef band{'s' if reef != 1 else ''} (Steel)"
                )
            sail = b.sail(
                sail_id,
                "square",
                yard=yard,
                area_m2=area,
                reef_bands=reef,
                # the royals set flying (Steel 1794 vol. I p. 214, ROYALS "Are set flying"),
                # sent down on deck with their yards when taken in
                flying=True if level == "royal" else None,
                x_m=g.raked_x(x, rake[name], centre, deck_m=frame),
                centre_height_m=centre,
                canvas_no=canvas[0],
                cloth_rating_kn=g.cloth(area, canvas[0]),
                note=f"{name} {level}: {how}.{g.canvas_note(canvas)}",
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
            note=f"{shrouds} shrouds a side: "
            + (RAZEE_SHROUD_NOTES if m["cut_ft"] else SHROUD_NOTES)[name]
            + "; the frigate-36's size scaled by her rope (judgement).",
        )
        bs_size = g.quarter((6.0 if name != "mizzen" else 4.5) * rope_scale)
        b.sided(f"{name}.topmast.backstay", "backstay", top, rating=g.rope_kn(bs_size, 2))

    gz = geom["mizzen"]
    lift_size = mizzen_lift_in(rope_scale)
    b.spar(
        "mizzen.crossjack.yard",
        "yard",
        on="mizzen.mast",
        length_m=g.ft(gz["yard"]),
        height_m=above_datum(p, g.ft(gz["yard_h"])),
        brace_limit_deg=CROSSJACK_BRACE_DEG,
        rating_kn=g.design_kn(
            [(areas["mizzen.topsail"][0], areas["mizzen.topsail"][1], "square")],
            g.DESIGN_WIND_KN["lower"],
        ),
        note=f"crossjack yard {fmt_ft(gz['yard'])} (Steel p. 49, the 64); crosses no sail, spreads "
        f"the mizzen topsail's foot; braces {CROSSJACK_BRACE_DEG} deg from square (the "
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
        rating=g.rope_kn(lift_size),
        note="the crossjack's lifts, as a course's (judgement): every yard's "
        "lifts are carried, and drawn (the owner's answer, Build-Ships.md §19.1 item 7).",
    )

    # -- the after sail: the 64's mizen course cut at the mast and her driver in its place (Indf
    # §4.4); the razee's spanker on her gaff and driver boom (§4.5) ------------------------------
    driver_sail = None
    if p.mizen == "course":
        after_sail = mizen_course(b, p, mizen, rope_scale)
        if DRIVER:  # the course filed first, so that the yard's sail stays it (Ext §17.2)
            driver_cut = mizen_driver_cut(p, mizen["cut"], mast_x["mizzen"], rake["mizzen"], frame)
            driver_sail = mizen_driver(b, p, driver_cut)
            REPORT.setdefault(p.key, {})["driver"] = driver_cut
    else:
        after_sail = spanker(b, p, mizen, rope_scale)
    REPORT.setdefault(p.key, {})["after_sail"] = mizen

    # -- the head (Indf §4.6) ------------------------------------------------------------------
    headsails = write_head(b, p, bow, rope_scale)
    sprit_sails = head_yards(b, p, bow, rope_scale)

    # -- the stays the masts stand by (the frigate's, scaled; judgement) ------------------------
    for sid, of, size, text in (
        (
            "fore.stay",
            "fore.mast",
            15.0,
            "to a collar half way out the bowsprit's outboard part (judgement); the fore "
            "staysail and the fore storm staysail set on it",
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

    # -- the staysails between the masts (Indf §4.3): the main topmast and main topgallant
    # staysails by Steel's rules on her geometry, the other four cut to Steel's table IV for a
    # 64 (the owner's choice, 2026-10-29), no mizen topgallant staysail; each note giving the
    # table's figure and how far the cut stands from it, inside Indf §4.3's band ------------------
    between = between_the_masts(b, p, geom, mast_x, rake, frame)
    cut_areas = {s["id"]: s["area_m2"] for s in b.doc["sails"]}
    for sid in between:
        b.notes[sid] += steels_staysail_words(sid, cut_areas[sid], p)

    # -- the studding sails, the storm canvas and the occasional sails (Indf §4.3, §4.7) --------
    stuns = studding_sails(b, p, geom, mast_x, rake, rope_scale)
    storm = storm_canvas(b, p, geom, mast_x, rake, bow, after_sail, rope_scale)
    occasional, save_alls = occasional_sails(b, p, mast_x, mizen, rope_scale)

    # -- groups (the frigate-36's set, with the names the engine reads: Indf §4.7) ---------------
    square = sum(sails_by_level.values(), [])
    b.group("courses", sails_by_level["course"])
    b.group("topsails", sails_by_level["topsail"])
    b.group("topgallants", sails_by_level["topgallant"])
    b.group("royals", list(sails_by_level["royal"]))
    b.group("headsails", headsails)
    b.group("jibs", ["jib"])
    b.group("staysails", headsails[:2] + between)
    # Steel's staysails between the masts as one group, as the frigate-36's (package 57)
    b.group("staysails between the masts", between)
    b.group("studdingsails", stuns)
    b.group("square sails", square)
    b.group("fore-and-aft sails", headsails + between + [after_sail])
    # the light sails, as the frigate-36's: the royals, the light staysails (the main and mizen
    # staysails, of No. 2, are not light canvas) and the studding sails; her one jib, Steel's
    # "Jib Flying", is in plain sail as the frigate's jib is, and not here
    light_staysails = [s for s in between if s not in ("main.staysail", "mizzen.staysail")]
    b.group("light sails", sails_by_level["royal"] + light_staysails + stuns)
    # lying to (package 57): Steel 1794 vol. II, 'Lying-to under the main staysail'
    b.group("lying-to staysails", ["main.staysail"])
    # the polar reads this group alone (world/ships.py): courses, topsails, topgallants, the
    # fore topmast staysail and the jib, and the mizen course or the spanker, as the frigate's
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
    # aliases: what an officer of 1795 would say (Falconer 1780; Lever 1827), the frigate-36's;
    # the first a part has is its name in the log (evolutions/runner.py, part_name)
    if p.mizen == "course":
        # Steel's 'Mizen-course' on the mizen yard (Indf §4.7); "spanker" and "driver" are
        # Steel's own occasional sail (Ext §17.2)
        for word in ("mizzen course", "mizen course", "mizzen", "mizen"):
            b.alias(word, "mizzen.course")
        for word in ("mizzen yard", "mizen yard"):
            b.alias(word, "mizzen.yard")
        if driver_sail:
            for word in ("driver", "spanker", "driver boomsail"):
                b.alias(word, driver_sail)
            for word in ("driver boom", "spanker boom"):
                b.alias(word, "mizzen.boom")
    else:
        b.alias("spanker", "mizzen.spanker")
        b.alias("driver", "mizzen.spanker")
        b.alias("mizzen", "mizzen.spanker")
        b.alias("mizen", "mizzen.spanker")
    b.alias("foresail", "fore.course")
    b.alias("mainsail", "main.course")
    b.alias("fore yard", "fore.yard")
    b.alias("main yard", "main.yard")
    b.alias("crossjack yard", "mizzen.crossjack.yard")
    b.alias("cro'jack yard", "mizzen.crossjack.yard")
    b.alias("crossjack", "mizzen.crossjack.yard")
    if p.mizen == "spanker":
        b.alias("spanker boom", "mizzen.boom")
        b.alias("driver boom", "mizzen.boom")
        b.alias("spanker gaff", "mizzen.gaff")
    if sprit_sails:  # the period's words (Indf §4.6); "spritsail" and its yard are their ids'
        if "sprit_topsail" in sprit_sails:  # the first its name in the log (`part_name`)
            for word in ("sprit topsail", "spritsail topsail"):
                b.alias(word, "sprit_topsail")
            for word in ("sprit topsail yard", "spritsail topsail yard"):
                b.alias(word, "sprit_topsail.yard")
    b.alias("fore staysail", "fore.staysail")
    b.alias("fore topmast staysail", "fore.topmast_staysail")
    b.alias("main topmast staysail", "main.topmast_staysail")
    b.alias("main staysail", "main.staysail")
    b.alias("main topgallant staysail", "main.topgallant_staysail")
    # no mizen topgallant staysail: Steel's 64 column has none, and she carries none (Indf §17)
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
    # groups freesail.ship.parts reads for the muster's sail-room line; none of them is in "all
    # sail" or "light sails", which name the working canvas
    b.group("storm canvas", storm)
    b.group("storm staysails", storm[:2])
    b.group("occasional sails", ([driver_sail] if driver_sail else []) + occasional)
    b.group("save-alls", save_alls)
    b.alias("save-all", "save-alls")
    for (name, level), _ in STEEL_STUDDING_64.items():
        b.group(
            f"{name} {level} studdingsails", [f"{name}.{level}.studdingsail.{s}" for s in g.SIDES]
        )
    # the courses' lines and the topsails' bowlines by their period names, each a group of the
    # two sided lines read as a sided family by its singular (the frigate-36's, WP15 and 3b)
    for name in ("fore", "main"):
        for cls in ("sheet", "tack", "bowline"):
            b.group(f"{name} {cls}s", [f"{name}.course.{cls}.{s}" for s in g.SIDES])
            b.alias(f"{name} {cls}", f"{name} {cls}s")
    for name in ("fore", "main", "mizzen"):
        b.group(f"{name} topsail bowlines", [f"{name}.topsail.bowline.{s}" for s in g.SIDES])
        b.alias(f"{name} top bowline", f"{name} topsail bowlines")

    # -- the ground tackle, the company, the guns and the stores (Indf §5-§7), in the
    # frigate-36's order; her description at far detail (§8) ---------------------------------
    fits = fits_of(p, hull["profile"])
    guns = default_guns(p, fits)
    ground_tackle(b)
    company(b, p, guns)
    armament(b, p, fits)
    quarter_bill(b, p, guns)
    boats_pumps_hold(b)
    b.descriptions([DESCRIPTIONS[p.key]])
    b.dump(os.path.join(out_dir, p.file), p.header)


# The shrouds a side (Indf §4.2): the main channel on ZAZ1407 at full resolution shows ten
# deadeyes before its three backstays' (counted on the crop), the fore the same (judgement);
# the razee's mizen channel seven (measured, ZAZ2371: Ind §2.3.8), the 64's taken the same.
SHROUDS = {"fore": 10, "main": 10, "mizzen": 7}
SHROUD_NOTES = {
    "fore": "the main channel's count on ZAZ1407 (judgement for the fore)",
    "main": "ten deadeyes before the three backstays' in her main channel on ZAZ1407 (measured "
    "on the crop at full resolution)",
    "mizzen": "the razee's mizen channel's seven deadeyes (ZAZ2371: Ind §2.3.8), hers the same "
    "(judgement)",
}
# The razee's, on her lowered channels (measured, ZAZ2371: Ind §2.3.8).
RAZEE_SHROUD_NOTES = {
    "fore": "the main channel's count (judgement for the fore), on her fore channel lowered to "
    "32 ft above K (ZAZ2371: Ind §2.3.8)",
    "main": "ten deadeyes in her main channel from 49.8 to 70.5 ft from AP, lowered about 5 ft to "
    "32 ft above K (measured, ZAZ2371: Ind §2.3.8), the 64's count on ZAZ1407",
    "mizzen": "seven deadeyes in her mizen channel, 37.3 ft above K (measured, ZAZ2371: Ind "
    "§2.3.8)",
}


def sail_of(mast, level):
    """A square sail's id by its mast and level: `main.course`, `fore.topsail`."""
    return f"{mast}.{level}"


def mizzen_lift_in(rope_scale):
    """The lifts of the mizzen's lower yards, inches: a course's lift, the mizzen's share of
    the frigate's rope, scaled with hers (judgement)."""
    rope = g.FRIGATE_ROPE["course"]["lift"] * g.FRIGATE_MAST_ROPE_FACTOR["mizzen"]
    return g.quarter(rope * rope_scale)


def steels_staysail_words(sid, area, p):
    """The words a staysail between the masts adds to its note: Steel's table IV figure for the
    64 and how far her cut of `area` m2 stands from it (Indf §4.3's check), raised before any
    file is written if it falls outside the check's band."""
    row, _figures, steel, band = STEEL_BETWEEN_64[sid]
    gap = area / steel - 1.0
    if abs(gap) > band:
        raise ValueError(
            f"The {p.key}'s {sid} is cut to {area} m2, {gap:+.0%} of Steel's {steel:.0f} for a 64, "
            f"outside Indf §4.3's ±{band:.0%}."
        )
    column = (
        ""
        if p.key == "sixty-four"
        else " Hers is the 64's column, as her design gives her canvas, her spars being the 64's "
        "(Indf §4.2-§4.3)."
    )
    return (
        f" Steel's table IV, the 64 ({row}; Ind §5): about {steel:.0f} m2, the cut within Indf "
        f"§4.3's ±{band:.0%}.{column}"
    )


def staysail(b, p, sid, stay, corners, frame, canvas, rope_in, words):
    """`g.staysail_from_cut` for a staysail whose corners are cut above her frame
    (`Particulars.frame_z`): its corners written above her datum, moved by the frame's height
    above it, so that its corners, centre and area above her water are its cut's (D18 (c), the
    razee's); the generator's own call where the two are one (the 64's)."""
    shift = frame - p.datum_z
    if shift:
        corners = [(x, z + shift) for x, z in corners]
    return g.staysail_from_cut(b, sid, stay, corners, p.datum_z, canvas, rope_in, words)


def between_the_masts(b, p, geom, mast_x, rake, frame):
    """The staysails between the masts (Indf §4.3), modelled on the generator's
    `between_the_masts` for a ship (package 57; Indf §1.3), with the stays the new ones set on.
    The main topmast staysail is its cut by Steel's rules on her spars, within Indf §4.3's band
    of Steel's table IV for a 64; the main, middle, mizen and mizen topmast staysails are cut to
    the table's own figures (`STEEL_BETWEEN_64`), the owner's choice of 2026-10-29 (Indf §17), and
    the main topgallant staysail with them since her long pole-heads; the mizen topgallant
    staysail, which the table's 64 column has not, is not carried, nor the stay the generator's
    rules set it on. Returns the sails, the main
    mast's foremost level first, then the mizen's. Every height here is above her frame
    (`Particulars.frame_z`), each sail written above her datum (`staysail`)."""
    canvas = g.FRIGATE_CANVAS

    def mx(name, z_m):
        return mast_x[name] - math.tan(math.radians(rake[name])) * z_m

    def head(gm, level):
        h = (
            gm["above"]
            + (gm["t_hoist"] if level >= 1 else 0)
            + (gm["g_hoist"] if level >= 2 else 0)
        )
        return g.ft(h)

    def at(name, level):
        z = head(geom[name], level)
        return (mx(name, z), z)

    def before_the_top(name, level=0):
        """Where the generator's rules hang a staysail's peak: before the top of the mast
        `name` (level 0), or before its cross-trees (level 1) (`TOP_REACH_OF_YARD`, judgement
        there)."""
        gm = geom[name]
        yard = gm["yard"] if level == 0 else gm["topsail_yard"]
        return mx(name, head(gm, level)) + g.TOP_REACH_OF_YARD * g.ft(yard)

    def steel(sid):
        """The table's figures for a four-sided staysail, metres: the after leech, the foot (the
        cloths of the head and the foot halved, as Steel's rule for the canvas squares them, 22
        1/2 in a cloth) and the bunt; and the cloths so squared."""
        head_cl, foot_cl, bunt_yd, leech_yd = STEEL_BETWEEN_64[sid][1]
        cloths = 0.5 * (head_cl + foot_cl)
        return g.ft(3.0 * leech_yd), g.ft(cloths * CLOTH_IN_SAIL_FT), g.ft(3.0 * bunt_yd), cloths

    def area_of(sid):
        return next(s["area_m2"] for s in b.doc["sails"] if s["id"] == sid)

    def from_the_table(sid, stay, upper, lower, peak_x, rope_in, where, chosen=None):
        """A four-sided staysail cut to the table's after leech and foot on its stay from
        `upper` to `lower`, its peak at `peak_x` and its bunt as the stay leaves it; its note
        in place of the generator's, `chosen` saying whose choice that was."""
        leech, foot, bunt, cloths = steel(sid)
        corners = g.stay_sail_cut(upper, lower, leech, peak_x=peak_x, foot=foot)
        staysail(b, p, sid, stay, corners, frame, canvas[sid], rope_in, "")
        b.notes[sid] = (
            f"{sid.replace('_', ' ').replace('.', ' ')}, four-sided, square on the foot, cut to "
            f"Steel's table IV, the 64, {chosen or 'as the owner chose (2026-10-29; Indf §17)'}: "
            f"the table's after leech and foot ({cloths:g} cloths of 22 1/2 in, the head's and "
            "the foot's halved, as Steel's rule for the canvas squares them), the bunt as the "
            f"stay leaves it (the table's {bunt:.1f} m); {where}" + g.canvas_note(canvas[sid])
        )
        return sid

    out = []
    # -- between the fore and the main masts ---------------------------------------------------
    gm, gf = geom["main"], geom["fore"]
    main_top = before_the_top("main")
    # the main staysail, a triangle on its own stay: the table's 28 cloths in the foot and 14
    # yards in the leech, square at the clew, its luff up the stay as her headsails' are
    # (judgement on Steel's figures), its tack over the boats on the booms, a fifth of the main
    # mast's height above the deck (the generator's, judgement)
    stay = b.line(
        "main.staysail.stay",
        "stay",
        "main.mast",
        rating=g.rope_kn(9.0),
        note="the main staysail stay, from the main mast head to a luff round the foremast (Steel "
        "1794 vol. I, 'The main-staysail': 'The upper end clinches round the main-mast-head above "
        "the rigging and the lower end sets up with a luff-tackle round the foremast'); 9 in, "
        "judgement.",
    )
    (xu, zu), (xl, zl) = at("main", 0), (mx("fore", 1.0), 1.0)
    tack_z = 0.2 * g.ft(gm["above"])
    tack = (xu + (tack_z - zu) * (xl - xu) / (zl - zu), tack_z)
    _head_cl, foot_cl, _bunt_yd, leech_yd = STEEL_BETWEEN_64["main.staysail"][1]
    corners, _foot, _leech, _fit = triangle_on_stay(
        tack, (xu, zu), foot_cl * CLOTH_IN_SAIL_FT * FT, 3.0 * leech_yd * FT
    )
    sid = "main.staysail"
    staysail(b, p, sid, stay, corners, frame, canvas[sid], 3.5, "")
    b.notes[sid] = (
        "main staysail, a triangle, cut to Steel's table IV, the 64, as the owner chose "
        f"(2026-10-29; Indf §17): {foot_cl:g} cloths of 22 1/2 in in the foot and {leech_yd:g} "
        "yards in the leech, square at the clew, its luff up the stay from its tack, as her "
        "headsails are cut (judgement on Steel's figures); its tack at the stay over the boats on "
        "the booms (a fifth of the main mast's height above the deck, judgement), its peak before "
        "the main top; corners [tack, peak, clew]. 'This sail is seldom used in large vessels' "
        "(Steel), and lying to under it is 'a mean between the two others' (Steel 1794 vol. II, "
        "'Lying-to under the main staysail')." + g.canvas_note(canvas[sid])
    )
    out.append(sid)
    # the main topmast staysail, the generator's rule on her spars: the leech 4 or 5 yards
    # deeper than the main topsail, its foot a cloth or two more than the leech's yards (Steel)
    leech_yd = (gm["topsail_h"] - gm["yard_h"]) / 3.0 + 4.5
    corners = g.stay_sail_cut(
        at("main", 1),
        at("fore", 0),
        g.ft(3.0 * leech_yd),
        peak_x=main_top,
        foot=g.ft((leech_yd + 1.5) * g.CLOTH_FT),
    )
    out.append(
        staysail(
            b,
            p,
            "main.topmast_staysail",
            "main.topmast.stay",
            corners,
            frame,
            canvas["main.topmast_staysail"],
            3.0,
            "the leech 4 or 5 yards deeper than the main topsail, a cloth or two more in the "
            "foot than the leech's yards (Steel; the mean of each taken), the bunt as the stay "
            "leaves it (Steel: two-fifths of the leech), its peak before the main top.",
        )
    )
    # the middle staysail, on its own stay from the main topmast head to the fore topmast under
    # the parral (Steel), a third of the topmast's hoist above the fore cap (the generator's,
    # judgement): the table's figures
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
    # the main topgallant staysail: the table's figures since her long pole-heads (stage B):
    # the generator's rule, the leech 5 1/2 yards deeper than the main topgallant sail, followed
    # that sail's new depth to +26% of the table, outside Indf §4.3's band (-11% on stage A's
    # spars), so it takes the table's as the owner chose for the other four (Indf §17)
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
            chosen="as the owner chose for the other four (2026-10-29; Indf §17), judgement for "
            "this one, the generator's rule on her long pole-heads overrunning the table's band",
        )
    )
    # -- between the main and the mizen masts --------------------------------------------------
    mizen_top = before_the_top("mizzen")
    # the mizen staysail on its stay's span from the mizen mast head to the collar round the
    # main mast (Steel): the collar where the table's bunt falls under its leech and foot
    # (judgement), the peak before the mizen top
    upper = at("mizzen", 0)
    leech, foot, bunt, _cloths = steel("mizzen.staysail")
    fall = (leech - bunt) / foot  # the head's fall, a metre forward
    tan_main = math.tan(math.radians(rake["main"]))
    collar_z = (upper[1] - fall * (mast_x["main"] - upper[0])) / (1.0 - fall * tan_main)
    collar = (mx("main", collar_z), collar_z)
    stay = b.line(
        "mizzen.staysail.stay",
        "stay",
        "mizzen.mast",
        rating=g.rope_kn(6.0),
        note="the mizen staysail stay (Steel 1794 vol. I, 'The mizen-staysail': 'clinches round "
        "the head of the mizen-mast, then reeves through a thimble ... in a collar lashed round "
        "the main-mast, and sets up ... [to] an eye-bolt in the deck abaft the mast. In small "
        "ships, the mizen-staysail bends to the mizen-stay'); 6 in, judgement; the collar where "
        "Steel's table IV bunt falls under its leech and foot (judgement), the staysail on the "
        "span above it.",
    )
    out.append(
        from_the_table(
            "mizzen.staysail",
            stay,
            upper,
            collar,
            mizen_top,
            3.0,
            "its peak before the mizen top (the generator's, judgement). So cut, its foot stands "
            "higher over her quarterdeck than Steel's sail-making has it drop, 'within 6 or 7 "
            "feet' of it (OCR l. 12308-12312): with the leech upright under a peak before the "
            "top, the table's figures and those words cannot both hold on her spars, and the "
            "table is taken (judgement).",
        )
    )
    # the mizen topmast staysail on the mizen topmast stay, to a collar at the main mast's bibs
    # (Steel; the generator's): the table's figures
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


def fmt_ft(v):
    """Feet as the period writes them, feet and inches to the nearest inch."""
    feet = math.floor(v + 1e-9)
    inches = round((v - feet) * 12.0)
    if inches == 12:
        feet, inches = feet + 1, 0
    return f"{feet} ft {inches} in" if inches else f"{feet} ft"


# ---------------------------------------------------------------------------
# The mizen course (Indf §4.4) and the head (§4.6)
# ---------------------------------------------------------------------------


def under_the_run(p, deck, aft_x, fore_x, room):
    """The points of `deck` (a line of (ft from AP, ft above K)) under a run from `aft_x` to
    `fore_x` (metres, the file's x), each (x, z above her water, room), the line's height at
    both ends of the run among them: what a sail's foot or a boom passing over the deck must
    stand above by `room`."""
    if not deck:
        return []
    pts = [(x_m(xf), p.z_m(zk, xf)) for xf, zk in deck]
    lo, hi = pts[0][0], pts[-1][0]
    out = [(x, z, room) for x, z in pts if aft_x <= x <= fore_x]
    for x in (aft_x, fore_x):
        if lo <= x <= hi:
            xf = x / FT + MIDSHIPS_FT
            out.append((x, p.z_m(interp(deck, xf), xf), room))
    return out


def mizen_course_cut(p, gm, mast_x_m, rake_deg, frame):
    """The 64's mizen course cut at the mast (`mizen_yard.course`; Ext §3.4) from Steel's table
    IV: its tack on the mast, its throat a fore leech above at the yard's truss, its head along
    the yard aft and up to the peak, its foot level aft to the clew; (x, z above her water) in
    metres, with its area and centre. Its tack is Steel's, 6 ft 6 in above her quarterdeck,
    unless her roundhouse deck under the foot then stands within the head room of it (the clew
    check: Bel §1.5; the lead's notes of 2026-10-29, item 2): then raised until the foot clears
    it by `HEAD_ROOM_FT`'s first figure, the head room going to its second only where a check
    breaks (the cut's own and the driver's, `mizen_driver_cut`)."""
    x_ft = p.masts["mizzen"]["x_ft"]
    deck = p.z_m(interp(p.decks["quarterdeck"], x_ft), x_ft)
    steel_tack = deck + MIZEN_TACK_ABOVE_DECK_FT * FT
    yard = STEEL_64["mizen_yard"] * FT
    steel = STEEL_MIZEN_COURSE_64

    def cut(tack_z):
        return mizen_yard.course(
            mast_x=mast_x_m,
            rake_deg=rake_deg,
            frame_z=frame,
            tack_z=tack_z,
            steel=steel,
            yard_length_m=yard,
        )

    first = cut(steel_tack)
    tack, _throat, _peak, clew = first["corners"]
    tried = []
    for room_ft in HEAD_ROOM_FT:
        room = room_ft * FT
        under = under_the_run(p, p.decks.get("roundhouse"), clew[0], tack[0], room)
        tack_z = max([steel_tack] + [z + r for _x, z, r in under])
        if tack_z > steel_tack:
            tack_z = math.ceil(tack_z * 100.0 - 1e-9) / 100.0
        try:
            crs = cut(tack_z)
            if DRIVER and MIZEN_COURSE == "gated":
                mizen_driver_cut(p, crs, mast_x_m, rake_deg, frame)
        except ValueError as e:
            tried.append(f"{room_ft:g} ft: {e}")
            continue
        clear = min(tack_z - z for _x, z, _r in under) if under else None
        steel_clear = min(steel_tack - z for _x, z, _r in under) if under else None
        return {
            "corners": crs["corners"],
            "area": round(crs["area"]),
            "x": round(crs["x"], 1),
            "centre": round(crs["centre"], 1),
            "deck": deck,
            "head_m": crs["head"],
            "run": crs["run"],
            "rise": crs["rise"],
            "foot": crs["foot"],
            "cut": crs,
            "steel_tack": steel_tack,
            "head_room_ft": room_ft if tack_z > steel_tack else None,
            "clear": clear,
            "steel_clear": steel_clear,
        }
    raise ValueError(
        "the 64's mizen course cannot be cut clear of her roundhouse deck within the head room "
        "the lead allows (the clew check: Bel §1.5; the lead's notes of 2026-10-29): "
        + "; ".join(tried)
    )


def mizen_driver_cut(p, crs, mast_x_m, rake_deg, frame):
    """Steel's driver on the 64's course `crs` (`mizen_yard.driver`; Ext §17.2), its boom's jaws
    the least that give the boom `HEAD_ROOM_FT`'s first figure of head room over her roundhouse
    deck at the side over its run and keep its after leech within Steel's band (the clew check,
    Bel §1.5, §4.6; the lead's notes of 2026-10-29), the head room going to the second figure
    only where a check breaks; clear over her taffrail. Raises `ValueError` where none holds."""
    boom = RAZEE_BOOM_FT * FT
    mast_at = mizen_yard.mast_line(mast_x_m, rake_deg, frame)
    taff_x, taff_z = p.rail[0]
    taffrail = (x_m(taff_x), p.z_m(wl1_above_k(taff_x) + taff_z, taff_x))
    kw = {
        "mast_x": mast_x_m,
        "rake_deg": rake_deg,
        "frame_z": frame,
        "steel": STEEL_DRIVER_64,
        "course_steel": STEEL_MIZEN_COURSE_64,
    }
    tried = []
    for room_ft in HEAD_ROOM_FT:
        room = room_ft * FT
        fore = mast_at(crs["corners"][0][1])
        under = under_the_run(p, p.decks.get("roundhouse"), fore - boom, fore, room)
        jaws, why = mizen_yard.least_jaws(crs, under=under, **kw)
        jaws = math.ceil(jaws * 100.0 - 1e-9) / 100.0
        try:
            d = mizen_yard.driver(
                crs,
                jaws_z=jaws,
                boom_length_m=boom,
                driver_yard_m=STEEL_64["tg_yard"]["fore"] * FT,
                under=under,
                over=[taffrail],
                **kw,
            )
        except ValueError as e:
            tried.append(f"{room_ft:g} ft: {e}")
            continue
        d["head_room_ft"], d["set_by"], d["under"] = room_ft, why, under
        d["taffrail"] = taffrail
        return d
    raise ValueError(
        "the 64's driver cannot be cut on her course within the head room the lead allows over "
        "her roundhouse (Ext §17.2; the lead's notes of 2026-10-29): " + "; ".join(tried)
    )


def mizen_course(b, p, mz, rope_scale):
    """The 64's mizen course on her mizen yard. Stage B (`MIZEN_COURSE = "gated"`): the lateen
    cut at the mast on the whole yard, a `lateen_yard` slung at its truss with its fore part
    bare, and the lines of Ext §3.4 (`mizen_yard.COURSE_LINES`). Stage A (`"stand-in"`), kept to
    measure the step against: a loose-footed gaff-class sail on the yard's after part, class
    `gaff`, as the owner rules the sail in the physics (Bel §13.5). Returns the course's id."""
    if MIZEN_COURSE not in ("gated", "stand-in"):
        raise ValueError(f"MIZEN_COURSE is {MIZEN_COURSE!r}: 'gated' or 'stand-in' (Indf §0).")
    if DRIVER and MIZEN_COURSE != "gated":
        raise ValueError(
            "DRIVER is True with the stand-in mizen course: the driver is a lateen cut at the "
            "mast on the mizen yard, which must then be a lateen yard (Ext §17.2; "
            "freesail/ship/schema.py)."
        )
    if MIZEN_COURSE == "stand-in":
        return mizen_course_stand_in(b, p, mz, rope_scale)
    datum = p.datum_z
    corners = [[round(x, 2), round(z - datum, 2)] for x, z in mz["corners"]]
    throat = mz["corners"][1]
    canvas = g.FRIGATE_CANVAS["mizzen.spanker"]
    load = [(mz["area"], mz["centre"], "gaff")]
    yard = b.spar(
        "mizzen.yard",
        "lateen_yard",
        on="mizzen.mast",
        length_m=g.ft(STEEL_64["mizen_yard"]),
        height_m=above_datum(p, round(throat[1] - p.frame_z, 2)),
        rating_kn=g.design_kn(load, g.DESIGN_WIND_KN["gaff"]),
        note=f"the mizen yard, Steel's {fmt_ft(STEEL_64['mizen_yard'])} by "
        f"{STEEL_64_DIAMETER_IN['mizen_yard']:g} in (p. 49, the 64), a lateen yard slung at its "
        "truss with its lifts and derrick, its fore part bare (Lavery 1985 I31-I32, the 74's; "
        "Ext §3.4): height_m its truss, the course's throat. Not braced: it has vangs in place "
        "of braces and bowlines at its heel, its sail trimmed by the sheet (Ext §3.3; Falconer "
        "1780, VANGS and BRACE).",
    )
    head_room = mz["head_room_ft"]
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
        note="mizen course, a lateen cut at the mast (D9 (c) as revised, Bel §13.5; Ext §3.4), "
        "the four-sided loose-footed sail the owner rules, on the gaff's curve and trim in the "
        "physics (Ext §3.1): Steel's table IV, the 64 (14 1/2 cloths at the head, 15 1/2 at the "
        "foot, its fore leech 9 1/4 yards and its after leech 17 1/4; Ind §5), 22 1/2 in a "
        "cloth, its luff laced to the mast, its head along the yard to the peak, its foot level "
        "and loose (tools/ships/mizen_yard.py); corners [tack, throat, peak, clew]. "
        + (
            f"Its tack raised on the mast until its foot stands {head_room:g} ft over her "
            "roundhouse deck at the side (the clew check: Bel §1.5; the lead's notes of "
            f"2026-10-29, the head room first, to 5 ft), {head_room:g} ft being the 74's boom's "
            "figure (Bel §4.6) taken for the foot: judgement, Bel §4.5's own course standing "
            "nearer its poop. Plainly: above Steel's 'within 6 or 7 "
            "feet of the deck' (OCR l. 11441-11442), her roundhouse standing over her "
            "quarterdeck at the mizen; stage A cut it 6 ft 6 in above her quarterdeck, and its "
            "foot ended under the roundhouse deck. "
            if head_room is not None
            else "Its tack 6 ft 6 in above her quarterdeck (Steel: 'within 6 or 7 feet of the "
            "deck', OCR l. 11441-11442), its foot clear of her roundhouse deck. "
        )
        + "One reef band a fifth up its mast leech (Steel, OCR l. 11448)."
        + g.canvas_note(canvas),
    )
    # the lines of Ext §3.4: the derrick, the vang pendants and the bowlines at Steel's sizes for
    # a 64 (vol. II, '64 Gun Ship', legible in part: OCR l. 24857-24865), the jeers, whose size
    # is not legible there (l. 24855-24856), at the stand-in's throat halyard's, and the rest at
    # the frigate's spanker's, scaled with her rope (judgement)
    lift = mizzen_lift_in(rope_scale)
    sizes = {
        "yard.jeers": (g.quarter(4.5 * rope_scale), 3),
        "yard.derrick": (STEEL_MIZEN_YARD_LINES_64["derrick"], 4),
        "yard.lift": (lift, 1),
        "yard.vang": (STEEL_MIZEN_YARD_LINES_64["vang"], 1),
        "yard.bowline": (STEEL_MIZEN_YARD_LINES_64["bowline"], 1),
        "course.sheet": (g.quarter(5.0 * rope_scale), 2),
        "course.tack": (g.quarter(3.5 * rope_scale), 1),
    }
    notes = {
        "yard.jeers": "the mizen yard's jeers at its truss (Steel 1794 vol. II p. 37, the 74's "
        "list; Ext §3.4); the 64's own not legible (OCR l. 24855-24856), the stand-in's throat "
        "halyard's size and purchase (judgement).",
        "yard.derrick": "Steel's derrick between the slings and the peak (Steel 1794 vol. II p. "
        "37, the 74's list; vol. I p. 207), a lift of the yard (Ext §3.4): 4 in in double blocks "
        "by the 64's own list (OCR l. 24857).",
        "yard.vang": "the vang pendants, 4 in by the 64's list (Steel 1794 vol. II, OCR l. "
        "24862), one line a side with its falls, which are not legible there.",
        "yard.lift": "the mizen yard's lifts (Lavery 1985 I31-I32), as the "
        "crossjack's (judgement): every yard's lifts are carried (the owner's answer, "
        "Build-Ships.md §19.1 item 7).",
        "yard.bowline": "the bowlines at the yard's heel (Steel 1794 vol. II p. 37, the 74's "
        "list; Lavery 1985 I32), filed as guys of the yard, a bowline being a sail's line in the "
        "engine (Ext §3.4); 3 in by the place of a garbled line in the 64's list (OCR l. 24865, "
        "judgement until it is read on the page image).",
        "course.sheet": "the course's one sheet, to the taffrail (Ext §3.4); the frigate's "
        "spanker sheet's size and purchase (judgement).",
        "course.tack": "the course's tack, forward of the mast (Ext §3.4); the frigate's spanker "
        "outhaul's size (judgement).",
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


def mizen_driver(b, p, d):
    """Steel's driver boomsail of the 64 and its boom (`DRIVER`; Ext §17.2), filed after the
    course so that the yard's sail stays the course (`sail_of`), in the course's place and in
    the sail room; its lines at Steel's sizes, rated by them. Returns the driver's id."""
    datum = p.datum_z
    corners = [[round(x, 2), round(z - datum, 2)] for x, z in d["corners"]]
    area = round(d["area"])
    centre = round(d["centre"], 1)
    jaws = d["boom"]["jaws_z"]
    load = [(area, centre, "gaff")]
    set_by = (
        "and the least that also keeps the driver's after leech within Steel's band, two to "
        "four yards deeper than the course's (Steel 1794 vol. I, DRIVER BOOMSAIL; Ext §17.2), "
        if d["set_by"] == "after leech"
        else ""
    )
    boom = b.spar(
        "mizzen.boom",
        "boom",
        on="mizzen.mast",
        length_m=g.ft(RAZEE_BOOM_FT),
        height_m=above_datum(p, round(jaws - p.frame_z, 2)),
        horse_m=round(0.5 * p.hull["beam_m"], 1),
        rating_kn=g.design_kn(load, g.DESIGN_WIND_KN["gaff"]),
        note=f"driver boom {fmt_ft(RAZEE_BOOM_FT)}, the main topsail yard's length (Steel 1794 "
        "vol. I p. 40: 'Driver boom, the same length as the main-topsail-yard'; Ext §17.2). "
        "Plainly: Steel's p. 49 column gives the 64 '0 0', and the Lancaster's boom of 1797 is "
        "the only 64's on record (Ext §17.1). Level, its jaws on the mast at the least height "
        f"that gives it {d['head_room_ft']:g} ft of head room over her roundhouse deck at the "
        "side (the clew check: Bel §1.5, §4.6; the lead's notes of 2026-10-29, the head room "
        f"first, to 5 ft), {set_by}clear over her taffrail. Ext §17.2's 2.4 m above her "
        "quarterdeck, taken before her roundhouse was measured, laid it level with the "
        "roundhouse deck at the stern. Steel's topping lifts and guy pendants (OCR l. "
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
        note="Steel's driver boomsail (Steel 1794 vol. I, DRIVER BOOMSAIL, OCR l. 13816-13843; "
        "Ext §17; the owner's choice of 2026-10-28), 'occasionally hoisted ... in light fair "
        "winds': a lateen cut at the mast on the mizen yard and its boom, in the sail room, bent "
        "in the mizen course's place by the shift of the one for the other (Ext §17.3: the "
        "period bent it beside the course and brailed the course; one after sail bent is the "
        "game's choice). Steel's table IV, the 64: 22 1/2 cloths at the head and 29 at the foot, "
        "its fore leech 9 1/2 yards and its after leech 20 (Ind §5), 22 1/2 in a cloth; its "
        "throat the course's, its tack at the boom's jaws, its head along the mizen yard's line "
        "and on past the yard's peak on Steel's driver yard (the fore topgallant yard's 34 ft 6 "
        "in, p. 40; not filed, it went aloft with the sail: Ext §17.2), its foot along the boom; "
        f"corners [tack, throat, peak, clew]. Its fore leech short of Steel's, {jaws_by}: Steel's "
        "four figures do not hang together on the course's yard (Ext §17.2). No reef band: Steel "
        "names none." + g.canvas_note(canvas),
    )
    # Steel's lines (vol. I, THE DRIVER or SPANKER SAIL, OCR l. 24523-24545; Ext §17.2) at the
    # sizes Ext §17.2 read in Steel's vol. II list for a 64 (OCR l. 24844-24847, read again here
    # and not on the page image), each rated by its own size as the ringtail's are
    steel_in = {
        "driver.halyard": (3.0, 1, "for Steel's four or five pair of halyards and the throat's"),
        "driver.tack": (3.0, 1, "'set tight with a luff-tackle' to the boom's throat"),
        "driver.sheet": (
            3.0,
            2,
            "rove through the boom's end to the clew, its luff tackle to the taffrail, doing the "
            "outhauler's work; 3 in judgement, the size not legible in the OCR",
        ),
        "driver.downhaul": (2.0, 1, "through a block at the middle of the driver yard"),
    }
    for suffix, cls, _owner, _sided in mizen_yard.DRIVER_LINES:
        size, parts, words = steel_in[suffix]
        b.line(
            f"mizzen.{suffix}",
            cls,
            sail,
            rating=g.rope_kn(size, parts),
            parts=parts if cls == "sheet" else None,
            note=f"the driver's {cls}, {size:g} in (Steel 1794 vol. II, the 64's list, OCR l. "
            f"24844-24847; Ext §17.2): {words}.",
        )
    return sail


def mizen_course_stand_in(b, p, mz, rope_scale):
    """Stage A's mizen course (`MIZEN_COURSE = "stand-in"`): a loose-footed gaff-class sail on
    the yard's after part, class `gaff`, as the owner rules the sail in the physics (Bel §13.5),
    kept to measure stage B's step against. Returns the sail's id."""
    datum = p.datum_z
    corners = [[round(x, 2), round(z - datum, 2)] for x, z in mz["corners"]]
    throat = mz["corners"][1]
    canvas = g.FRIGATE_CANVAS["mizzen.spanker"]
    load = [(mz["area"], mz["centre"], "gaff")]
    yard = b.spar(
        "mizzen.yard",
        "gaff",
        on="mizzen.mast",
        length_m=round(mz["head_m"], 1),
        height_m=above_datum(p, round(throat[1] - p.frame_z, 1)),
        rating_kn=g.design_kn(load, g.DESIGN_WIND_KN["gaff"]),
        note=f"the mizen yard, PROVISIONAL behind the lead's gate (Indf §0): Steel's 77 ft by 14 "
        f"in (p. 49, the 64), slung at its truss with lifts, its fore part bare (Lavery 1985 "
        f"I31-I32, the 74's). Filed at stage A as a gaff, its after part alone: the course's "
        f"head, {mz['head_m']:.1f} m, its truss the throat {throat[1]:.2f} m above her water.",
    )
    sail = b.sail(
        "mizzen.course",
        "gaff",
        mast="mizzen.mast",
        gaff=yard,
        area_m2=mz["area"],
        reef_bands=1,
        x_m=mz["x"],
        centre_height_m=mz["centre"],
        canvas_no=canvas[0],
        cloth_rating_kn=g.cloth(mz["area"], canvas[0]),
        corners_m=corners,
        note="mizen course, PROVISIONAL behind the lead's gate (Indf §0, §4.4): "
        "Steel's table IV, the 64 (14 1/2 cloths at the head, 15 1/2 at the foot, its fore leech "
        "9 1/4 yards and its after leech 17 1/4; Ind §5), its fore leech on the mast from its "
        "tack 6 ft 6 in above the quarterdeck (Steel: 'within 6 or 7 feet of the deck'; Indf "
        "§4.4 judged 3 ft), its head along the yard's after part to the peak, its foot aft, "
        "loose. A four-sided, loose-footed sail like the gaff sail in "
        "the physics (the owner, Bel §13.5), filed as a gaff sail with no boom until the lateen "
        "cut at the mast is built; corners [tack, throat, peak, clew]. One reef band a fifth up "
        "its mast leech (Steel, OCR l. 11448)." + g.canvas_note(canvas),
    )
    # the frigate-36's spanker's lines but the outhaul (it has no boom), scaled with her rope:
    # the throat and peak halyards stand for the yard's jeers (Indf §4.4), the sheet aft
    for lid, cls, of, size, parts in (
        ("mizzen.yard.throat_halyard", "throat_halyard", yard, 4.5, 3),
        ("mizzen.yard.peak_halyard", "peak_halyard", yard, 4.0, 4),
    ):
        b.line(lid, cls, of, rating=g.rope_kn(g.quarter(size * rope_scale), parts))
    b.line(
        "mizzen.course.sheet",
        "sheet",
        sail,
        rating=g.rope_kn(g.quarter(5.0 * rope_scale), 2),
        parts=2,
    )
    b.sided("mizzen.yard.vang", "vang", yard, rating=g.rope_kn(g.quarter(3.5 * rope_scale)))
    lift = mizzen_lift_in(rope_scale)
    b.sided(
        "mizzen.yard.lift",
        "lift",
        yard,
        rating=g.rope_kn(lift),
        note="the mizen yard's lifts (Lavery 1985 I31-I32; Steel's derrick), as the "
        "crossjack's (judgement): every yard's lifts are carried (the owner's answer, "
        "Build-Ships.md §19.1 item 7).",
    )
    return sail


def spanker_cut(p, gm, mast_x_m, rake_deg, frame):
    """The razee's spanker on her gaff and driver boom by the frigate-36's rule (Indf §4.5): its
    tack at the boom's jaws, its throat at the gaff's jaws under the mizen's hounds, its head 0.9
    of the gaff peaked 40 degrees, its foot 0.9 of the boom along it; (x, z above her water) in
    metres, with its area and centre; `gm` and the mast's x above and at her frame
    (`Particulars.frame_z`). The boom lies level, its jaws raised from stage A's 6 ft 6 in above
    her quarterdeck by the least that clears her short roundhouse by the head room (the clew
    check: Bel §1.5, §4.6; the lead's notes of 2026-10-29, item 2) and her taffrail, the spanker
    cut by the rule on them; the head room going first (`HEAD_ROOM_FT`) if the sail would then
    fall outside 8% of Steel's driver for a 38, as the owner settled it (Indf §17)."""
    x_ft = p.masts["mizzen"]["x_ft"]
    deck = p.z_m(p.deck_k_ft(x_ft), x_ft)
    filed = deck + SPANKER_BOOM_ABOVE_DECK_FT * FT
    throat_z = frame + (gm["above"] - gm["head"] - SPANKER_THROAT_BELOW_HOUNDS_FT) * FT
    lean = math.tan(math.radians(rake_deg))

    def on_mast(z):
        return mast_x_m - lean * (z - frame)

    head = SPANKER_HEAD_OF_GAFF * RAZEE_GAFF_FT * FT
    foot = SPANKER_FOOT_OF_BOOM * RAZEE_BOOM_FT * FT
    peak_rad = math.radians(SPANKER_PEAK_DEG)
    throat = (on_mast(throat_z), throat_z)
    peak = (throat[0] - head * math.cos(peak_rad), throat_z + head * math.sin(peak_rad))
    taff_x, taff_z = p.rail[0]
    taffrail = p.z_m(wl1_above_k(taff_x) + taff_z, taff_x)
    boom = RAZEE_BOOM_FT * FT

    def cut(boom_z):
        tack = (on_mast(boom_z), boom_z)
        clew = (tack[0] - foot, boom_z)
        corners = [tack, throat, peak, clew]
        area, cx, cz = g._quad_area_centroid(corners)
        return corners, area, cx, cz, clew

    tried = []
    for room_ft in HEAD_ROOM_FT:
        room = room_ft * FT
        under = under_the_run(
            p, p.decks.get("roundhouse"), on_mast(filed) - boom, on_mast(filed), room
        )
        boom_z = max([filed, taffrail] + [z + r for _x, z, r in under])
        boom_z = math.ceil(boom_z * 100.0 - 1e-9) / 100.0
        corners, area, cx, cz, clew = cut(boom_z)
        if abs(area / STEEL_DRIVER_38_M2 - 1.0) > SPANKER_BAND_OF_38:
            tried.append(f"{room_ft:g} ft: {area:.0f} m2")
            continue
        return {
            "corners": corners,
            "area": round(area),
            "x": round(cx, 1),
            "centre": round(cz, 1),
            "deck": deck,
            "boom_z": boom_z,
            "throat_z": throat_z,
            "leech": peak[1] - boom_z,
            "clew_x": clew[0],
            "filed_z": filed,
            "filed_area": round(cut(filed)[1]),
            "head_room_ft": room_ft,
            "clear": min(boom_z - z for _x, z, _r in under) if under else None,
            "taffrail": taffrail,
            "overhang_ft": (x_m(taff_x) - (on_mast(boom_z) - boom)) / FT,
        }
    raise ValueError(
        "the razee's spanker cannot keep within 8% of Steel's driver for a 38 "
        f"({STEEL_DRIVER_38_M2:g} m2) with its boom clear of her roundhouse by the head room the "
        "lead allows (the lead's notes of 2026-10-29): " + "; ".join(tried)
    )


def spanker(b, p, sp, rope_scale):
    """The razee's gaff, driver boom and spanker (D20 (a); Indf §4.5), with the frigate-36's
    spanker's lines scaled by her rope. Returns the sail's id."""
    datum = p.datum_z
    canvas = g.FRIGATE_CANVAS["mizzen.spanker"]
    load = [(sp["area"], sp["centre"], "gaff")]
    corners = [[round(x, 2), round(z - datum, 2)] for x, z in sp["corners"]]
    gaff = b.spar(
        "mizzen.gaff",
        "gaff",
        on="mizzen.mast",
        length_m=g.ft(RAZEE_GAFF_FT),
        height_m=above_datum(p, round(sp["throat_z"] - p.frame_z, 1)),
        rating_kn=g.design_kn(load, g.DESIGN_WIND_KN["gaff"]),
        note=f"spanker gaff {fmt_ft(RAZEE_GAFF_FT)}, five-eighths of the driver boom (Steel 1794 "
        "vol. I p. 40: 'gaffs 5/8 of their booms'; D20 (a), the 41 ft 10 in of the 44's and 38's "
        "ratio a foot longer); its jaws 3 ft below the mizen's hounds, as the frigate-36's "
        "(judgement). She lost 'her Gaff and Mizen-Top-Mast' on 20 April 1796 (Gazette 13887 p. "
        "388).",
    )
    boom = b.spar(
        "mizzen.boom",
        "boom",
        on="mizzen.mast",
        length_m=g.ft(RAZEE_BOOM_FT),
        height_m=above_datum(p, round(sp["boom_z"] - p.frame_z, 2)),
        horse_m=round(0.5 * p.hull["beam_m"], 1),
        rating_kn=g.design_kn(load, g.DESIGN_WIND_KN["gaff"]),
        note=f"driver boom {fmt_ft(RAZEE_BOOM_FT)}, the main topsail yard's length (Steel 1794 "
        "vol. I p. 40: 'Driver boom, the same length as the main-topsail-yard'; D20 (a)), "
        "overhanging her taffrail, long (Ind §3.3 reckoned it against her taffrail as then "
        "filed; no source objects). Level, its jaws "
        f"raised by the least that gives it {sp['head_room_ft']:g} ft of head room over her short "
        "roundhouse's deck (ZAZ2371, the warrant of December 1794: Ind §2.2; the clew check, Bel "
        "§1.5, §4.6; the lead's notes of 2026-10-29), clear over her taffrail. Plainly: stage A "
        "laid it 6 ft 6 in above her quarterdeck, where the 64's mizen course had its tack "
        "(Steel's 'within 6 or 7 feet of the deck', judgement for the boom), before her roundhouse "
        "was measured, and it ran through the cabin under the deck, so her spanker is cut "
        "smaller on it than the 218 m2 the owner kept (the sail's note). horse_m " + g.HORSE_NOTE,
    )
    sail = b.sail(
        "mizzen.spanker",
        "gaff",
        mast="mizzen.mast",
        gaff=gaff,
        boom=boom,
        area_m2=sp["area"],
        reef_bands=2,
        x_m=sp["x"],
        centre_height_m=sp["centre"],
        canvas_no=canvas[0],
        cloth_rating_kn=g.cloth(sp["area"], canvas[0]),
        corners_m=corners,
        note="spanker (driver) by the frigate-36's rule on her spars (D20 (a); Indf §4.5): its "
        "foot 0.9 of the boom, its head 0.9 of the gaff peaked 40 degrees, its hoist from the "
        "boom's jaws to the gaff's (judgement, ±10%); corners [tack, throat, peak, clew]. Steel's "
        "table IV (read on the page image, Indf §3.5 item 6) gives the 44 a gaff mizen course of "
        "about 88 m2 and a driver of 157, the 38 105 and 202, the 64's driver 198; the "
        "frigate-36's spanker is 167. The owner settled it by this rule at 218 m2, within 8% of "
        "the 38's driver (2026-10-29; Indf §17); with the boom's jaws raised clear of her "
        "roundhouse the same rule cuts it smaller, kept within that 8% (the lead's notes of "
        "2026-10-29). Two reef bands, as the frigate-36's (Steel's mizen course has one)."
        + g.canvas_note(canvas),
    )
    for lid, cls, of, size, parts in (
        ("mizzen.gaff.throat_halyard", "throat_halyard", gaff, 4.5, 3),
        ("mizzen.gaff.peak_halyard", "peak_halyard", gaff, 4.0, 4),
    ):
        b.line(lid, cls, of, rating=g.rope_kn(g.quarter(size * rope_scale), parts))
    b.line(
        "mizzen.spanker.sheet",
        "sheet",
        sail,
        rating=g.rope_kn(g.quarter(5.0 * rope_scale), 2),
        parts=2,
    )
    b.line("mizzen.spanker.outhaul", "outhaul", sail, rating=g.rope_kn(g.quarter(3.5 * rope_scale)))
    b.sided("mizzen.gaff.vang", "vang", gaff, rating=g.rope_kn(g.quarter(3.5 * rope_scale)))
    return sail


def head_geometry(p, geom, mast_x, rake, frame):
    """The bowsprit, the jib-boom and the headsails' triangles, feet and metres above her water.

    The bowsprit's root on the stem head (`STEM_HEAD_FT`), where ZAZ1407 draws it lying (Indf
    §3.5 item 9; stage A rooted it at the near knighthead's cap, `KNIGHTHEAD_FT`, about 4 ft
    higher), steeved 27 degrees, its outboard part measured from its heel; the jib-boom along
    it. The fore stay to a collar half way out the bowsprit's
    outboard part (judgement: where Steel's fore staysail, cut as below, stands clear before
    the fore mast), the fore topmast stay to the bowsprit's end and the jib's stay to the
    jib-boom's (the frigate's leads; judgement). Each headsail a triangle on its stay from its
    tack at the stay's foot: Steel's leech and the cloths of Steel's foot, square to each other
    at the clew ("square on the foot", as Steel cuts the staysails), so that its area is
    Steel's (judgement on Steel's figures)."""
    stem_x, stem_z = STEM_HEAD_FT
    root = (x_m(stem_x), p.z_m(wl1_above_k(stem_x) + stem_z, stem_x))
    inboard = (stem_x - BOWSPRIT_HEEL_FT) / math.cos(math.radians(BOWSPRIT_STEEVE_DEG))
    outboard = STEEL_64["bowsprit"] - inboard
    jib_out = JIB_BOOM_OUTBOARD * STEEL_64["jib_boom"]
    c, s = math.cos(math.radians(BOWSPRIT_STEEVE_DEG)), math.sin(math.radians(BOWSPRIT_STEEVE_DEG))

    def along(d_ft):
        return (root[0] + d_ft * c * FT, root[1] + d_ft * s * FT)

    tip = along(outboard)
    jib_tip = along(outboard + jib_out)
    fore = geom["fore"]

    def at_mast(h_ft):
        z = frame + h_ft * FT
        return (mast_x["fore"] - math.tan(math.radians(rake["fore"])) * (z - frame), z)

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
        foot_cl, leech_yd = STEEL_HEADSAILS_64[sid]
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
        "collar": stays["fore.staysail"][1],
        "sails": sails,
    }


def triangle_on_stay(low, high, foot, leech):
    """A triangular staysail on its stay as her headsails are cut from Steel's table IV (Indf
    §4.3; judgement on Steel's figures): its tack at `low` on the stay, its luff up the stay
    toward `high`, its foot and leech, metres, square to each other at the clew ("square on the
    foot", as Steel cuts the staysails), the clew below and abaft the stay. A sail whose luff is
    longer than its stay is cut to the stay, Steel's proportions kept: the spars rule over the
    sail table (the owner's answer, Build-Ships.md §19.1 item 5); the razee's fore staysail was,
    until her bowsprit was rooted on the stem head. Returns the corners [tack, peak, clew], the
    foot and the leech as cut, and the share of Steel's sides kept."""
    luff = math.hypot(foot, leech)
    run = math.hypot(high[0] - low[0], high[1] - low[1])
    fit = min(1.0, run / luff)
    foot, leech, luff = foot * fit, leech * fit, luff * fit
    ux, uz = (high[0] - low[0]) / run, (high[1] - low[1]) / run
    nx, nz = (-uz, ux) if ux > 0 else (uz, -ux)  # the side below and abaft the stay
    if nz > 0:
        nx, nz = -nx, -nz
    peak = (low[0] + luff * ux, low[1] + luff * uz)
    ca, sa = foot / luff, leech / luff
    clew = (low[0] + foot * (ca * ux + sa * nx), low[1] + foot * (ca * uz + sa * nz))
    return [low, peak, clew], foot, leech, fit


HEAD_CANVAS = {
    "fore.staysail": (
        2,
        f"{g.STEEL_SM}, 'Fore staysail': No. 1 to 3, the middle taken (Ind §5)",
    ),
    "fore.topmast_staysail": g.FRIGATE_CANVAS["fore.topmast_staysail"],
    "jib": g.FRIGATE_CANVAS["jib"],
}


def write_head(b, p, head, rope_scale):
    """The bowsprit, the jib-boom, their stays and the headsails (Indf §4.3, §4.6). Returns the
    headsails' ids, the fore staysail first."""
    datum = p.datum_z
    loads = {sid: (h["area"], h["centre"], "jibheaded") for sid, h in head["sails"].items()}
    bowsprit = b.spar(
        "bowsprit",
        "bowsprit",
        x_m=round(head["root"][0], 2),
        length_m=g.ft(head["outboard"]),
        height_m=above_datum(p, round(head["tip"][1] - p.frame_z, 1)),
        rating_kn=g.design_kn(list(loads.values()), g.DESIGN_WIND_KN["lower"]),
        note=f"bowsprit {fmt_ft(STEEL_64['bowsprit'])} (Steel p. 49, the 64), steeved "
        f"{BOWSPRIT_STEEVE_DEG:g} deg (measured, Ind §3.1), rooted on the stem head, where ZAZ1407 "
        "draws it lying and the viewer draws its heel (Indf §3.5 item 9; Ext §6.2 as built): x_m "
        "its root, length_m its part outboard of the stem head from its heel measured just "
        "before the fore mast on ZAZ1280 (±1 ft; Luce's third inboard would give 40.2 ft), "
        "height_m its end above the datum. Stage A rooted it at the near knighthead's cap (moved "
        "at stage B, the headsails' tacks and the stays' leads with it). "
        + (
            "The spritsail yard slung under it and the sprit-topsail yard under the jib-boom "
            "(D8 (b); Ext §4.1; tools/ships/spritsail_yards.py)."
            if p.key == "sixty-four"
            else "The 64's, in its place in the hull (D8 (b) as answered; Indf §1.5 step 7), with "
            "the spritsail yard slung under it, an occasional sail out of plain sail, and no "
            "sprit-topsail yard (the owner: Indf §4.6, §17 item 5)."
        ),
    )
    jib_boom = b.spar(
        "jib_boom",
        "jib_boom",
        on=bowsprit,
        length_m=g.ft(head["jib_out"]),
        height_m=above_datum(p, round(head["jib_tip"][1] - p.frame_z, 1)),
        rating_kn=g.design_kn([loads["jib"]], g.DESIGN_WIND_KN["jib_boom"]),
        note=f"jib-boom {fmt_ft(STEEL_64['jib_boom'])} (Steel p. 49), 7/12 of it outboard along "
        "the bowsprit's steeve (Luce, the frigate's rule; judgement). No flying jib-boom: Steel's "
        "64 has none, Steel's 'flying jib boom' rule being this boom's (Ind §3.1, judgement).",
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
            "from the fore topmast head to the jib-boom's end: the "
            "jib sets on it (Steel's was set flying on its traveller)",
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
            note=f"the frigate-36's scaled (judgement){'; ' + text if text else ''}.",
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
            corners_m=[[round(x, 2), round(z - datum, 2)] for x, z in h["corners"]],
            note=f"{sid.replace('_', ' ').replace('.', ' ')}, a triangle (Steel's "
            f"table IV, the 64: {h['foot_cl']:g} cloths in the foot, {h['leech_yd']:g} yards in "
            "the leech; Ind §5): its tack at its stay's foot, its luff up the stay, foot and "
            "leech square at the clew (judgement on Steel's figures)"
            + (
                ", cut to her stay, short of Steel's in each side, the spars ruling (the "
                f"owner's answer, Build-Ships.md §19.1 item 5; the table's {h['table']} m2)"
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


def head_yards(b, p, head, rope_scale):
    """The yards under the bowsprit (D8 (b); Indf §4.6; Ext §4.1; `spritsail_yards.cut`), on the
    line her bowsprit and jib-boom have (`head`, from `head_geometry`): the 64's spritsail and
    sprit-topsail yards, Steel's 57 ft 6 in by 12 1/8 in and 34 ft 6 in by 7 in (p. 49), with the
    sprit course (102 m2) and the sprit topsail (103 m2) of table IV; the razee's spritsail yard
    alone, the 64's spar, out of plain sail (the owner's answer, Indf §17 item 5). Their lines
    are `square_sail_lines` at her fore topsail's and fore topgallant's sizes, the yards their
    lengths (judgement: Steel's vol. II list for a 64 is legible in part, and these lines are not
    yet read against it), and the guys of Lavery I28; no halyard to the spritsail yard, which
    hangs in slings (Ext §4.1). Returns the sails' ids, and with `BOWSPRIT_YARDS = False` writes
    nothing."""
    if not BOWSPRIT_YARDS:
        return []
    steel_st = SPRIT_TOPSAIL_64 if p.key == "sixty-four" else None
    cut = spritsail_yards.cut(
        root=head["root"],
        steeve_deg=BOWSPRIT_STEEVE_DEG,
        bowsprit_out_m=head["outboard"] * FT,
        jib_out_m=head["jib_out"] * FT,
        spritsail=SPRITSAIL_64,
        sprit_topsail=steel_st,
        station=SPRITSAIL_STATION,
        hang=SPRITSAIL_HANG_M,
        topsail_hang=SPRIT_TOPSAIL_HANG_M,
    )
    REPORT.setdefault(p.key, {})["sprit"] = cut
    if steel_st:
        upper, lower = cut["sprit_topsail.yard"], cut["spritsail.yard"]
        along = math.hypot(
            round(upper["x"], 2) - round(lower["x"], 2),
            round(upper["z"] - p.frame_z, 2) - round(lower["z"] - p.frame_z, 2),
        )
        REPORT[p.key]["sprit_drawn"] = (
            along,
            *spritsail_yards.drawn_by_slant(
                round(cut["sprit_topsail"]["area"]),
                g.ft(steel_st["yard_m"] / FT),
                g.ft(SPRITSAIL_64["yard_m"] / FT),
                along,
            ),
        )
    braced = (
        f"braces {SPRIT_BRACE_LIMIT_DEG} deg from square, from the yard's arms to the fore top "
        "and the fore stay (Steel 1794 vol. I pp. 196-197; Lavery 1985 I30; judgement, as the "
        "engine's fixture: no lead was measured to stop her sooner); kept out of the file's yard "
        "groups, braced by name, by 'brace sharp up' and 'trim sails' (Ext §4.2 as built)"
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
            height_m=above_datum(p, round(y["z"] - p.frame_z, 2)),
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

    out = [
        write_one(
            "spritsail",
            "spritsail.yard",
            "bowsprit",
            "topsail",
            SPRITSAIL_64,
            SPRITSAIL_CANVAS,
            2,
            False,
            f"spritsail yard {fmt_ft(SPRITSAIL_64['yard_m'] / FT)} by 12 1/8 in (Steel p. 49, the "
            "64), slung under the bowsprit near the cap (Steel 1794 vol. I pp. 196-197: its slings "
            "over the bowsprit, its halyards from the cap; Lavery 1985 I30), "
            f"{SPRITSAIL_STATION:g} of the way out its outboard part and {SPRITSAIL_HANG_M:g} m "
            "under its line (judgement, both); no halyard, it hanging in slings (Ext §4.1)"
            + (
                ""
                if p.key == "sixty-four"
                else ": the owner's answer, the 64's spar, an occasional sail out of plain sail, "
                "and no sprit-topsail yard (Indf §4.6, §17 item 5)"
            )
            + ";",
            "spritsail (the sprit course): Steel's table IV, the 64 (26 cloths, 7 1/2 yards deep; "
            "Ind §5), 22 1/2 in a cloth, hanging from its yard, square, its foot clear of the "
            "water at no heel (tools/ships/spritsail_yards.py). Two diagonal reef bands in Steel, "
            "filed and reefed as a square sail's (Ext §4.1). Out of plain sail, so the polar never "
            "sets it (Ext §4.1). Not modelled: the yard topped by the lee brace, and got fore and "
            "aft in a gale (Ext §4.4).",
        )
    ]
    if steel_st is not None:
        out.append(
            write_one(
                "sprit_topsail",
                "sprit_topsail.yard",
                "jib_boom",
                "topgallant",
                steel_st,
                SPRIT_TOPSAIL_CANVAS,
                0,
                True,
                f"sprit-topsail yard {fmt_ft(steel_st['yard_m'] / FT)} by 7 in (Steel p. 49, the "
                "64), hung under the jib-boom by its parral (Steel p. 197), where its sail's "
                "depth from the spritsail yard is Steel's, near the boom's end (judgement on "
                f"Steel's figures; {SPRIT_TOPSAIL_HANG_M:g} m under its line, judgement); its "
                "halyard stands for the traveller's outhauler (Falconer 1780, SPRITSAIL-TOPSAIL; "
                "Lavery 1985 I29);",
                "sprit topsail: Steel's table IV, the 64 (17 cloths at the head, 27 at the foot, 9 "
                "yards deep; Ind §5), 22 1/2 in a cloth, its head on its yard and its foot spread "
                "on the spritsail yard's arms (Steel, SPRITSAIL TOPSAIL; Falconer 1780), the "
                "sail's plane sloping forward from the one to the other, its centre in that plane "
                "(tools/ships/spritsail_yards.py). No reef band (Lever 1808, OCR l. 7354-7356). "
                "Out of plain sail (Ext §4.1). Not modelled: the yard's run along the jib-boom "
                "(Ext §4.4).",
            )
        )
    return out


# ---------------------------------------------------------------------------
# The studding sails, the storm canvas and the occasional sails (Indf §4.3, §4.7)
# ---------------------------------------------------------------------------


def studding_sails(b, p, geom, mast_x, rake, rope_scale):
    """The studding sails, the frigate-36's set on Steel's figures for a 64: the fore lower and
    the fore and main topmast and topgallant, a pair each, on Steel's booms. Below the topmast
    caps Steel's cloths and depths; the topgallant studding sails as deep as the topgallants
    they spread, cut to the spars by the owner's rule as the topgallants are. Each boom linked
    to its sail's own yard and sitting where it is rigged, as the frigate's: the lower boom at
    the fore channel, the topmast booms on the lower yard, the topgallant booms on the topsail
    yard. Returns the sails' ids."""
    frame = p.frame_z
    fore_x_ft = p.masts["fore"]["x_ft"]
    channel_m = p.z_m(p.fore_channel_k_ft, fore_x_ft) - frame
    out = []
    for (name, level), (head_cl, foot_cl, depth_yd, boom_ft) in STEEL_STUDDING_64.items():
        gm = geom[name]
        parent, hung, boom_h = {
            "lower": (f"{name}.yard", gm["yard_h"], round(channel_m, 1)),
            "topmast": (f"{name}.topsail.yard", gm["topsail_h"], g.ft(gm["yard_h"])),
            "topgallant": (f"{name}.topgallant.yard", gm["tg_h"], g.ft(gm["topsail_h"])),
        }[level]
        head_w, foot_w = head_cl * CLOTH_IN_SAIL_FT, foot_cl * CLOTH_IN_SAIL_FT
        if level == "topgallant":
            depth = gm["tg_h"] - gm["topsail_h"]
            how = (
                "as deep as the topgallant it spreads, cut to the spars as the "
                f"topgallants are (the owner's answer, Build-Ships.md §19.1 item 5); the table's "
                f"{depth_yd:g} yards would give "
                f"{round((head_w + foot_w) / 2.0 * 3.0 * depth_yd * FT * FT)} m2"
            )
        else:
            depth = 3.0 * depth_yd
            how = f"{depth_yd:g} yards deep"
        area = round((head_w + foot_w) / 2.0 * depth * FT * FT)
        drop = depth * (head_w + 2.0 * foot_w) / (3.0 * (head_w + foot_w))
        centre = round(frame + (hung - drop) * FT, 1)
        canvas = g.FRIGATE_CANVAS[f"{level} studding"]
        size = g.quarter({"lower": 3.0, "topmast": 2.5, "topgallant": 2.0}[level] * rope_scale)
        for side in g.SIDES:
            first = side == g.SIDES[0]
            boom = b.spar(
                f"{name}.{level}.studdingsail_boom.{side}",
                "studdingsail_boom",
                on=parent,
                side=side,
                length_m=g.ft(boom_ft),
                height_m=above_datum(p, boom_h),
                rating_kn=g.design_kn([(area, centre, "studding")], g.DESIGN_WIND_KN["studding"]),
                note=(
                    f"{name} {level} studding-sail boom {fmt_ft(boom_ft)} (Steel 1794 vol. I p. "
                    "49, the 64; p. 40: "
                    + (
                        "five-ninths of the main yard), goose-necked at the fore channel (Luce "
                        "1884 p. 137), its height there measured"
                        if level == "lower"
                        else "half the yard it is rigged on)"
                    )
                    + f"; rated for its sail in {g.DESIGN_WIND_KN['studding']:.0f} kn."
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
                x_m=g.raked_x(mast_x[name], rake[name], centre, deck_m=frame),
                centre_height_m=centre,
                canvas_no=canvas[0],
                cloth_rating_kn=g.cloth(area, canvas[0]),
                note=(
                    f"{name} {level} studding sail: Steel's table IV, the 64 (Ind §5), "
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


def storm_canvas(b, p, geom, mast_x, rake, bow, after_sail, rope_scale):
    """The storm canvas, the frigate-36's pattern on her figures (Indf §4.7), every sail in the
    sail room: the fore storm staysail on the fore stay, the mizzen storm staysail on the mizen
    stay, the storm mizzen on its own stay abaft the mizen mast, bent in place of her after sail.
    Each fixed height is taken above the deck she works it from (her quarterdeck), and each sail
    written with its corners. Returns the sails' ids, the storm staysails first."""
    datum, frame = p.datum_z, p.frame_z
    storm = g.FRIGATE_CANVAS["storm"]

    def deck_at(x_m_):
        x_ft = x_m_ / FT + MIDSHIPS_FT
        return p.z_m(p.deck_k_ft(x_ft), x_ft)

    def on_mast(name, z):
        return mast_x[name] - math.tan(math.radians(rake[name])) * (z - frame)

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
            corners_m=[[round(x, 2), round(z - datum, 2)] for x, z in corners],
            note=f"{sid.replace('_', ' ').replace('.', ' ')}, {words}; in the sail room."
            + g.canvas_note(storm, storm=True),
            **kw,
        )

    # the fore storm staysail on the fore stay (Luce 1884 ch. X: "The storm-staysails set on the
    # respective lower-stays"): the frigate's is Kipping's fore staysail, the sail of No. 1 or 2
    # set on the forestay; hers is Steel's fore staysail as her working one is cut (No. 1 to 3),
    # of storm canvas, bent beside it and set in its place
    fss_corners = bow["sails"]["fore.staysail"]["corners"]
    fss = storm_sail(
        "fore.storm_staysail",
        "fore.stay",
        fss_corners,
        "Steel's fore staysail cut as her working one is (table IV, the 64: 19 cloths in the "
        "foot, 11 1/2 yards in the leech; Steel's canvas No. 1 to 3), of storm canvas, on the fore "
        "stay (Luce 1884 ch. X); the frigate-36's is Kipping's fore staysail of No. 1 or 2, the "
        "same sail; corners [tack, peak, clew]",
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
    # the mizzen storm staysail on the mizen stay: its tack at the collar on the main mast, its
    # head 0.6 up the stay towards the mizen's hounds, its clew under the head 7 ft above the
    # quarterdeck (the frigate's; Steel's mizen staysail)
    gz = geom["mizzen"]
    main_deck = deck_at(mast_x["main"])
    collar_z = main_deck + MIZEN_STAY_COLLAR_FT * FT
    collar = (on_mast("main", collar_z), collar_z)
    top_z = frame + (gz["above"] - gz["head"]) * FT
    top = (on_mast("mizzen", top_z), top_z)
    f = STORM_STAYSAIL_HEAD_OF_STAY
    head = (collar[0] + f * (top[0] - collar[0]), collar[1] + f * (top[1] - collar[1]))
    clew = (head[0], deck_at(head[0]) + STORM_STAYSAIL_CLEW_FT * FT)
    mss = storm_sail(
        "mizzen.storm_staysail",
        "mizzen.stay",
        [collar, head, clew],
        "on the mizen stay (Luce 1884 ch. X; the Trenton's allowance has one, Luce p. 171): its "
        "tack at the stay's collar on the main mast, 12 ft above the quarterdeck (Steel, "
        "'Mizen-stay'), its head 0.6 of the way up the stay, its clew under the head 7 ft above "
        "the quarterdeck (Steel's mizen staysail; the frigate-36's, 0.6 judgement); corners "
        "[tack, peak, clew]",
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
    # the storm mizzen: "a triangular sail set abaft the mizzen-mast on a vertical 'stay',
    # hooked under the after trestle-tree, and set up on deck" (Luce 1884 ch. X), "a substitute
    # for the spanker" (ch. XXVII); Steel's 'Storm mizen', bent "to a horse, abaft and parallel
    # to the mizen-mast. The foot is extended towards the taffarel by a sheet"
    size = g.quarter(5.0 * rope_scale)
    b.line(
        "storm_mizzen.stay",
        "stay",
        "mizzen.mast",
        rating=g.rope_kn(size),
        note="the storm mizzen's stay abaft the mizen mast, under its after trestle-tree (Luce "
        "1884 ch. X); the jib stay's, scaled by her rope (judgement).",
    )
    mz_deck = deck_at(mast_x["mizzen"])
    filed_tack = mz_deck + STORM_MIZZEN_TACK_FT * FT
    foot = STORM_MIZZEN_FOOT_OF_BOOM * RAZEE_BOOM_FT * FT
    rail_k = [(xf, wl1_above_k(xf) + zf) for xf, zf in p.rail]
    rail = under_the_run(p, rail_k, on_mast("mizzen", filed_tack) - foot, mast_x["mizzen"], 0.0)
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
        "triangular (Luce 1884 ch. X; Steel 1794 'Storm mizen'): its luff up its stay from a "
        "tack at her rail over the foot's run, which stands above the frigate-36's 4 ft over the "
        "quarterdeck, so that the foot clears her roundhouse deck (judgement, as the clew check: "
        "Bel §1.5), 0.8 of the stay's run to the hounds; its foot towards "
        "the taffrail, 0.45 of the driver boom by Steel's rule (the main topsail yard's length, "
        "p. 40), as the frigate-36's is of her spanker boom "
        f"(judgement); bent in place of the {'mizen course' if p.mizen == 'course' else 'spanker'};"
        " corners [tack, peak, clew]",
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


def occasional_sails(b, p, mast_x, after, rope_scale):
    """The occasional sails, the frigate-36's pattern (Indf §4.7), in the sail room: the ringtail
    on the razee alone, she having the driver boom it runs out on, and a save-all under each fore
    lower studding-sail boom. Returns the occasional sails and the save-alls."""
    out = []
    if p.mizen == "spanker":
        # the ringtail, abaft the spanker (Luce 1884 ch. XXIII: "a ring-tail, which sets abaft the
        # spanker"), on a ringtail boom run out on the driver boom (Kipping 1847, 'Ringtail
        # Sails'; Steel 1794 vol. I, 'Ringtail-boom'), as the frigate-36's
        depth_ft = after["leech"] / FT
        rt_head, foot_ft = (c * CLOTH_IN_SAIL_FT for c in RINGTAIL_CLOTHS)
        area = round((rt_head + foot_ft) / 2.0 * depth_ft * FT * FT)
        boom_ft = foot_ft * 4.0 / 3.0
        centre = round(after["boom_z"] + 0.45 * depth_ft * FT, 1)
        rt_boom = b.spar(
            "ringtail_boom",
            "studdingsail_boom",
            on="mizzen.boom",
            length_m=g.ft(boom_ft),
            height_m=above_datum(p, round(after["boom_z"] - p.frame_z, 2)),
            rating_kn=g.design_kn([(area, centre, "studding")], g.DESIGN_WIND_KN["studding"]),
            note="ringtail boom, run out on the driver boom (Kipping's sliding "
            "gunter-boom; Steel 1794 vol. I, 'Ringtail-boom': 'lashed occasionally to the outer "
            "end of the main-sail-boom'): the ringtail's foot and a third that bears on the boom "
            f"(the frigate-36's, judgement); rated for its sail in "
            f"{g.DESIGN_WIND_KN['studding']:.0f} kn, as a studding sail boom.",
        )
        canvas = g.FRIGATE_CANVAS["ringtail"]
        rt = b.sail(
            "ringtail",
            "studding",
            boom=rt_boom,
            area_m2=area,
            x_m=round(after["clew_x"] - foot_ft / 2.0 * FT, 1),
            centre_height_m=centre,
            canvas_no=canvas[0],
            cloth_rating_kn=g.cloth(area, canvas[0]),
            bent=False,
            note="ringtail (Kipping, Luce 1884): the depth of "
            "the spanker's after leech it borders, 5 cloths in the head and 7 in the foot "
            "(Kipping's brig's, her 22 1/2-in cloth), as the frigate-36's (judgement); a "
            "studding-class sail with no side, lying in the spanker's plane; in the sail room."
            + g.canvas_note(canvas),
        )
        size = g.quarter(2.5 * rope_scale)
        b.line("ringtail.halyard", "halyard", rt, rating=g.rope_kn(size))
        b.line("ringtail.tack", "tack", rt, rating=g.rope_kn(size))
        b.line("ringtail.sheet", "sheet", rt, rating=g.rope_kn(g.quarter(2.0 * rope_scale)))
        out.append(rt)
    # a save-all under each fore lower studding-sail boom (Luce 1884 ch. XXIII, 'Other Sails';
    # Steel 1794 vol. I: "Some ships have a water-sail, similar to a sloop's"): its head along
    # 0.6 of the boom, down to half a metre off the water (the frigate-36's, judgement)
    boom_ft = STEEL_STUDDING_64[("fore", "lower")][3]
    boom_z = p.z_m(p.fore_channel_k_ft, p.masts["fore"]["x_ft"])
    depth = boom_z - 0.5
    area = round(SAVE_ALL_OF_BOOM * boom_ft * FT * depth)
    canvas = g.FRIGATE_CANVAS["save-all"]
    save_alls = []
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
                "save-all under the fore lower studding sail boom (Luce 1884): its head "
                "along 0.6 of the boom, down from the boom at the fore channel to half a metre "
                "off the water (the frigate-36's, judgement); in the "
                "sail room." + g.canvas_note(canvas)
                if side == g.SIDES[0]
                else None
            ),
        )
        size = g.quarter(2.0 * rope_scale)
        b.line(f"{sa}.halyard", "halyard", sa, rating=g.rope_kn(size))
        b.line(f"{sa}.tack", "tack", sa, rating=g.rope_kn(size))
        b.line(f"{sa}.sheet", "sheet", sa, rating=g.rope_kn(g.quarter(1.75 * rope_scale)))
        save_alls.append(sa)
    return out + save_alls, save_alls


# ---------------------------------------------------------------------------
# The guns (Indf §5)
# ---------------------------------------------------------------------------

# Her long guns' lengths (Indf §5.3), each a pattern of `period.ADYE_LONG_GUN_CWT` (Adye 1804
# p. 155, the page image read: Ind §6.4), which gives its weight: the 24-pounder of 9 ft 6 in,
# 49 cwt 2 qr (D31 (a); the pattern a 64's lower deck usually had, memory, unverified: Ind
# §6.4); the 18 of 9 ft 0 in, 40 cwt, and the 9 of 7 ft 6 in, 24 cwt 2 qr, the 74's patterns
# (Bel §13.1 answer 12; Lavery 1985 Table 17 gives the Bellona's 18s 40 cwt in 1761, via Bel
# §13.4), judgement for hers and accepted by the owner (Build-Ships.md §19.1 item 6); the 12 of
# 9 ft 6 in, 34 cwt, the generator's (D31 (a)). Her carronades are Adye's by
# `period.ADYE_CARRONADE_CWT` (p. 72), the longer of Adye's two for the 24 and the 18.
LONG_PATTERNS = {24: (9, 6), 18: (9, 0), 12: (9, 6), 9: (7, 6)}
# Her fits' defaults (Indf §5.1; the fits' names accepted by the lead, 2026-10-28): the 64's as
# built in 1784 (D17 (a)); the razee's as carried in 1796 (the owner, 2026-10-28).
DEFAULT_FIT = {"sixty-four": "ardent class 1784", "razee": "as carried 1796"}
# The Regulations' allowance for exercise (Indf §5.4) counts the upper deck's guns: the 64's
# twenty-six 18-pounders, a third in a ship of two decks; the razee's twenty-six 24-pounders, a
# fourth in a ship of one (the Regulations 1806, the Gunner, Art. XXI, OCR l. 13118-13144).
UPPER_DECK_GUNS = 26
DECKS_OF = {"sixty-four": 2, "razee": 1}
# Her cartridges' powder (Indf §5.4): the engine's shares give every calibre of her fits to the
# ounce of the Regulations' Table No. 29, read on the page image (Ind §6.4), so the shared
# note, which waits on that table, is overridden in her fits until the shared work (SW-1) fills
# the table and its note serves her (Build-Ships.md §10).
CHARGES_NOTE = (
    "A cartridge's powder in pounds, to the ounce: the service charges of cylinder powder for "
    "one shot, the Regulations 1806 (1808 printing), Table No. 29 (the page image read: "
    "Research-Indefatigable-2026-10.md §6.4; the OCR has its title at l.27498-27502 and lost its "
    "figures): the long 24-pounder 8 lb, the 18 6 lb, the 12 4 lb, the 9 3 lb; the 42-pounder "
    "carronade 3 lb 8 oz, the 24 2 lb, the 18 1 lb 8 oz. The engine's shares of the shot, a "
    "third for a long gun and a twelfth for a carronade (freesail/ship/parts.py, charge_lb), "
    "give each of them to the ounce."
)
ARMAMENT_NOTE = (
    "The armament (spec M7 7; package 70; docs/design/Design-Ship-Indefatigable.md §5): the "
    "guns as parts of the graph by their place, in her fits, each on its port of the hull's "
    "profile to the centimetre with its deck named (Build-Ships.md §4.4); their weights by Adye "
    "1804 (pp. 72, 155) and their crews by Falconer 1780 and Douglas 1829 (D31); the magazine's "
    "allowance by kind and calibre. Every figure's source is in tools/ships/indefatigable.py."
)


def piece(kind, pounder):
    """A piece's weight, cwt, and its crew to the pair (Indf §5.3): Adye's weight of her
    pattern; Falconer's men to a long gun "when the ship is well manned, so as to fight both
    sides at once occasionally" (1780, QUARTERS, OCR l. 14315-14340), and Douglas's four to a
    carronade of any nature (1829, art. 136): D31 (c)."""
    if kind == "long":
        weight = period.ADYE_LONG_GUN_CWT[pounder][LONG_PATTERNS[pounder]]
        return weight, period.FALCONER_CREW[pounder]
    return period.ADYE_CARRONADE_CWT[pounder], period.DOUGLAS_CARRONADE_CREW


def ports_from_forward(profile, deck):
    """A deck's ports in the hull's profile as (x, sill) from forward, metres to the centimetre
    as the profile has them, so that a gun on one stands on its triple (Build-Ships.md §4.4)."""
    return [(x, sill) for x, sill, _ in reversed(profile["ports_m"][deck])]


def pairs(ports, deck, first, kind, pounder, note):
    """Broadside pairs on `ports`, numbered on from `first` from forward (Indf §5.2), each gun's
    x and height its port's x and sill, its crew the period's (§5.3); the note on the first."""
    cwt, crew = piece(kind, pounder)
    out = []
    for i, (x, sill) in enumerate(ports):
        made = g.broadside_pair(
            first + i,
            kind,
            pounder,
            cwt,
            x,
            sill,
            note if i == 0 else None,
            deck=deck,
            round_to=0.01,
        )
        for gun, _ in made:
            gun["crew"] = crew  # reassigned, so the key keeps its place (Indf §5.2)
        out += made
    return out


def bow_chasers(port, pounder, note):
    """A pair of long guns as bow chasers in her chase ports, one a side, on the forecastle."""
    cwt, crew = piece("long", pounder)
    made = g.chasers(
        "bow", "long", pounder, cwt, port[0], port[1], note, deck="forecastle", round_to=0.01
    )
    for gun, _ in made:
        gun["crew"] = crew
    return made


def sixty_four_fits(profile):
    """The 64's two fits (Indf §5.1) as (name, source, guns, note): the Ardent class's guns as
    she was built, the default, and the class's from 1794, never hers."""
    lower = ports_from_forward(profile, "lower")
    upper = ports_from_forward(profile, "upper")
    # the quarterdeck's five foremost ports a side; the sixth, under the roundhouse, is drawn
    # and carries no gun of her fit (QUARTERDECK_SILLS)
    quarterdeck = ports_from_forward(profile, "quarterdeck")[:5]
    forecastle = ports_from_forward(profile, "forecastle")  # the 9's port, then the carronade's
    roundhouse = ports_from_forward(profile, "roundhouse")

    def as_built():
        return (
            pairs(
                lower,
                "lower",
                1,
                "long",
                24,
                "The lower deck's twenty-six long 24-pounders, thirteen a side: the 9 ft 6 in gun "
                "of 49 cwt 2 qr (Adye 1804 p. 155; D31 (a)), each on its port, its x and its sill "
                "to the centimetre (Indf §5.2); eleven men to the pair, who fight whichever side "
                "bears (Falconer 1780, QUARTERS; D31 (c)). Numbered from forward and on across her "
                "decks, as the frigate-36 numbers hers; the period numbered each deck from No. 1 "
                "(Bel §7.2).",
            )
            + pairs(
                upper,
                "upper",
                14,
                "long",
                18,
                "The upper deck's twenty-six long 18-pounders: the 9 ft gun of 40 cwt (Adye 1804 "
                "p. 155), the 74's pattern (Bel §13.1 answer 12; judgement for hers); nine men to "
                "the pair (Falconer 1780, QUARTERS).",
            )
            + pairs(
                quarterdeck,
                "quarterdeck",
                27,
                "long",
                9,
                "The quarterdeck's ten long 9-pounders in its five foremost ports a side, the "
                "sixth, under the roundhouse, empty: the 7 ft 6 in gun of 24 cwt 2 qr (Adye 1804 "
                "p. 155; the 74's pattern, judgement for hers); six men to the pair (Falconer "
                "1780).",
            )
            + pairs(
                forecastle[:1],
                "forecastle",
                32,
                "long",
                9,
                "The forecastle's two long 9-pounders, one a side, firing over its rail (no port "
                "is drawn on 1407F: Indf §3.3); six men to the pair (Falconer 1780).",
            )
        )

    source = (
        "RMG ZAZ1407, the gun table (read; written for Stately on the shared sheet); Winfield, "
        "British Warships in the Age of Sail 1793-1817, p. 99, the Ardent class; Adye 1804 pp. "
        "72 and 155, the pieces; Falconer 1780 (QUARTERS) and Douglas 1829 (art. 136), the crews"
    )
    return [
        (
            "ardent class 1784",
            source,
            as_built(),
            "The Ardent class's guns as she was built: 26 x 24-pounders on the lower deck, 26 x "
            "18-pounders on the upper deck, 10 x 9-pounders on the quarterdeck and 2 x 9-pounders "
            "on the forecastle, 64 pieces (ZAZ1407's gun table; Winfield 1793-1817 p. 99; D17 "
            "(a)). The default.",
        ),
        (
            "ardent class 1794",
            source,
            as_built()
            + pairs(
                forecastle[1:],
                "forecastle",
                33,
                "carronade",
                24,
                "The forecastle's two 24-pounder carronades of 1794, one a side (Indf "
                "§5.1, judgement), firing over the rail: 13 cwt, the 3 ft 7 1/2 in carronade (Adye "
                "1804 p. 72); four men to the pair, its captain, two privates and a provider "
                "(Douglas 1829 art. 136).",
            )
            + pairs(
                roundhouse,
                "roundhouse",
                34,
                "carronade",
                18,
                "The roundhouse's six 18-pounder carronades of 1794, three a side "
                "(Indf §5.1; the roundhouse unmeasured but its rail and the line under it, "
                "judgement), firing over the rail: 9 cwt, the 3 ft 3 in carronade (Adye 1804 p. "
                "72); four men to the pair (Douglas 1829 art. 136).",
            ),
            "The class's guns from 1794: those of 1784 with 2 x 24-pounder carronades on the "
            "forecastle and 6 x 18-pounder carronades on the roundhouse, 72 pieces (Winfield "
            "1793-1817 p. 99). Never hers: she was not in commission as a 64 and was cut down from "
            "September 1794 (Ind §4.1, judgement); a fit for a 64 of the class at sea after 1794.",
        ),
    ]


def razee_fits(profile):
    """The razee's two fits (Indf §5.1) as (name, source, guns, note): the establishment as
    razeed in 1795, and the guns she carried from 1796, the default."""
    gun_deck = ports_from_forward(profile, "upper")
    quarterdeck = ports_from_forward(profile, "quarterdeck")
    chase, *forecastle = ports_from_forward(profile, "forecastle")
    twenty_fours = (
        "Her gun deck's twenty-six long 24-pounders, thirteen a side, the 64's lower-deck guns "
        "kept (James vol. 1 p. 454): the 9 ft 6 in gun of 49 cwt 2 qr (Adye 1804 p. 155; D31 (a)), "
        "each on its port, its x and its sill to the centimetre (Indf §5.2); eleven men to the "
        "pair, who fight whichever side bears (Falconer 1780, QUARTERS; D31 (c)). Numbered from "
        "forward and on across her decks, as the frigate-36 numbers hers."
    )
    carronade = (
        "22 cwt 1 qr, the 4 ft 3 1/2 in carronade (Adye 1804 p. 72); four men to the pair, its "
        "captain, two privates and a provider (Douglas 1829 art. 136; D31 (c)), the marines "
        "first at the beat to quarters (crew/quarters.py)"
    )
    as_razeed = (
        pairs(gun_deck, "upper", 1, "long", 24, twenty_fours)
        + pairs(
            quarterdeck[:4],
            "quarterdeck",
            14,
            "long",
            12,
            "The quarterdeck's eight long 12-pounders in its four foremost ports a side: the 9 ft "
            "6 in gun of 34 cwt (Adye 1804 p. 155, the generator's pattern; D31 (a)); seven men to "
            "the pair (Falconer 1780, QUARTERS).",
        )
        + pairs(
            quarterdeck[4:],
            "quarterdeck",
            18,
            "carronade",
            42,
            "The quarterdeck's four 42-pounder carronades in its two aftmost ports a side, by the "
            "cabin and the wheel, where a carronade's short recoil wants the least room "
            f"(judgement, Indf §5.1): {carronade}.",
        )
        + pairs(
            forecastle[:1],
            "forecastle",
            20,
            "carronade",
            42,
            "The forecastle's two 42-pounder carronades in its foremost port a side, by the "
            "catheads and the bitts (judgement, Indf §5.1); four men to the pair.",
        )
        + pairs(
            forecastle[1:],
            "forecastle",
            21,
            "long",
            12,
            "The forecastle's four long 12-pounders in its after two ports a side: seven men to "
            "the pair.",
        )
    )
    as_carried = (
        pairs(gun_deck, "upper", 1, "long", 24, twenty_fours)
        + pairs(
            quarterdeck,
            "quarterdeck",
            14,
            "carronade",
            42,
            "The quarterdeck's twelve 42-pounder carronades, one in each of its six ports a side "
            "(James vol. 1 p. 361: eighteen on the quarterdeck and forecastle together, which "
            f"fill their ports exactly, ZAZ2375): {carronade}.",
        )
        + pairs(
            forecastle,
            "forecastle",
            20,
            "carronade",
            42,
            "The forecastle's six 42-pounder carronades, one in each of its three ports a side; "
            "four men to the pair.",
        )
        + bow_chasers(
            chase,
            12,
            "Her two long 12-pounders as bow chasers, one a side in her chase ports (James vol. 1 "
            "p. 361 puts them on the quarterdeck and forecastle; that they were bow chasers is the "
            "kit's word and the build's judgement, D30 (a)): the 9 ft 6 in gun of 34 cwt (Adye "
            "1804 p. 155, the generator's pattern; the note leans to a short 12 of 7 ft 6 in-8 ft "
            "6 in and 29 1/4-31 1/2 cwt, Ind §6.4); seven men each (Falconer 1780).",
        )
    )
    return [
        (
            "as razeed 1795",
            "Winfield, British Warships in the Age of Sail 1793-1817, p. 99, Indefatigable as a "
            "frigate; RMG ZAZ2371 and ZAZ2398, the armament tables (read); James, Naval History "
            "vol. 1 p. 454; Adye 1804 pp. 72 and 155, the pieces; Falconer 1780 (QUARTERS) and "
            "Douglas 1829 (art. 136), the crews",
            as_razeed,
            "The establishment of 1794 as razeed, registered a 38: 26 x 24-pounders on her gun "
            "deck; on the quarterdeck 8 x 12-pounders and 4 x 42-pounder carronades; on the "
            "forecastle 4 x 12-pounders and 2 x 42-pounder carronades; 44 pieces, which fill the "
            "quarterdeck's six ports and the forecastle's three a side (ZAZ2375, measured). The "
            "split within each deck is judgement. James: none of the three razees went to sea with "
            "the establishment's long guns; 'The Indefatigable mounted but 28' (vol. 1 p. 454).",
        ),
        (
            "as carried 1796",
            "James, Naval History vol. 1 p. 361 (read); Troude vol. 3 p. 31; D30 (a); Adye 1804 "
            "pp. 72 and 155, the pieces; Falconer 1780 (QUARTERS) and Douglas 1829 (art. 136), the "
            "crews",
            as_carried,
            "As she carried them under Pellew at the Virginie, 20-21 April 1796: 26 long "
            "24-pounders on her gun deck, 18 x 42-pounder carronades in the eighteen ports of her "
            "quarterdeck and forecastle, and 2 long 12-pounders, bow chasers by judgement (James "
            "vol. 1 p. 361; Troude vol. 3 p. 31; D30 (a)); 46 pieces. The same in January 1797 "
            "(James vol. 2 pp. 16-17) and in 1805 (vol. 3 p. 313; ADM 1/2408/84, catalogue). James "
            "gives her broadside as 702 lb, counting one 12 (vol. 1 p. 362); the far-detail rule "
            "counts both chasers (combat/far.py; truth 7-188). The "
            "default (the owner, 2026-10-28).",
        ),
    ]


def fits_of(p, profile):
    """Her fits (Indf §5.1) as (name, source, guns, note), in the file's order."""
    return sixty_four_fits(profile) if p.key == "sixty-four" else razee_fits(profile)


def default_guns(p, fits):
    """The default fit's guns, against which her quarter bill and her stores are set."""
    return next(guns for name, _, guns, _ in fits if name == DEFAULT_FIT[p.key])


def armament(b, p, fits):
    """Her fits and their magazines (Indf §5), the charges' notes overridden to cite Table No.
    29 and the 64's exercise note a two-decker's."""
    decks = DECKS_OF[p.key]
    exercise = g.exercise_allowance(UPPER_DECK_GUNS, decks=decks)
    rounds = {"long": g.KINGS_ROUNDS, "carronade": g.KINGS_ROUNDS, "swivel": g.SWIVEL_ROUNDS}
    b.armament(
        ARMAMENT_NOTE,
        DEFAULT_FIT[p.key],
        [
            (name, source, guns, g.fit_magazine(guns, rounds, exercise), note)
            for name, source, guns, note in fits
        ],
    )
    for name, *_ in fits:
        b.armament_notes[("magazine", name, "charges")] = CHARGES_NOTE
        if decks == 2:
            b.armament_notes[("magazine", name, "exercise_charges")] = (
                period.TWO_DECKS_EXERCISE_NOTE
            )


# ---------------------------------------------------------------------------
# The company, the marines and the quarter bill (Indf §6)
# ---------------------------------------------------------------------------

# Her company on the Regulations' table of officers and ratings (1806, 1808 printing, p. 165
# and IA leaves 455-460, the page images read: Ind §4.2): the 64 on the 491 column, the class's
# complement from 1794 (Winfield 1793-1817 p. 99; D17 (a)); the razee on the 44's 294 column
# with 36 seamen over it, 330 (James vol. 1 p. 454: "at first of 310, but afterwards of 330
# men"; D32 (a)). The posts are her wardroom file's (data/people/); the marines the column's
# officers and NCOs and the privates by judgement (no establishment of private marines was
# found: Ind §10.8); the idlers the column's rows by trade, and by judgement a cooper, a cook's
# mate, a gunroom steward and the servants; the seamen shared among the six stations as the
# frigate-36's 182 are (28, 24, 30, 14, 50, 36: judgement), the column's petty officers and its
# boys among them (Indf §6.1-§6.2).
COMPANY = {
    "sixty-four": {
        "complement": 491,
        "column": 64,
        "marines": 84,
        "seamen": {
            "forecastle": 54,
            "fore_top": 46,
            "main_top": 58,
            "mizzen_top": 27,
            "afterguard": 96,
            "waisters": 70,
        },
        "idlers": {
            "carpenter's crew": (
                11,
                "the carpenter's mate and crew of eight, the caulker and the caulker's mate",
            ),
            "sailmaker's crew": (4, "the sailmaker's mate and crew of two, and the ropemaker"),
            "cooper": (1, "a cooper, for the casks (judgement: the column has none)"),
            "armourer": (3, "the armourer and two armourer's mates"),
            "cook": (2, "the ship's cook, and a cook's mate (judgement)"),
            "steward": (
                3,
                "the purser's steward and the steward's mate, and a gunroom steward (judgement)",
            ),
            "servant": (
                12,
                "officers' servants (judgement: the frigate-36's eight, and more for her five "
                "lieutenants and the captain of marines)",
            ),
            "surgeon's mate": (2, "the two assistant surgeons"),
            "clerk": (2, "the captain's clerk and the schoolmaster"),
            "master-at-arms's party": (2, "the two ship's corporals"),
        },
        "marines_note": "the 491 column's captain, two lieutenants, two serjeants, two corporals "
        "and a drummer, 8, and 76 privates (judgement: the Bellona's share in 1761, 97 marines in "
        "her 567, Lavery 1985 p. 17 Table 7, via Bel §13.4; the frigate-36's share would give 74; "
        "the owner's leave of 2026-10-28)",
    },
    "razee": {
        "complement": 330,
        "column": 44,
        "marines": 50,
        "seamen": {
            "forecastle": 37,
            "fore_top": 31,
            "main_top": 39,
            "mizzen_top": 18,
            "afterguard": 66,
            "waisters": 47,
        },
        "idlers": {
            "carpenter's crew": (7, "the carpenter's mate and crew of five, and the caulker"),
            "sailmaker's crew": (3, "the sailmaker's mate and crew of one, and the ropemaker"),
            "cooper": (1, "a cooper, for the casks (judgement: the column has none)"),
            "armourer": (2, "the armourer and an armourer's mate"),
            "cook": (2, "the ship's cook, and a cook's mate (judgement)"),
            "steward": (2, "the purser's steward, and a gunroom steward (judgement)"),
            "servant": (8, "officers' servants, the frigate-36's eight (judgement)"),
            "surgeon's mate": (1, "the assistant surgeon"),
            "clerk": (2, "the captain's clerk and the schoolmaster"),
            "master-at-arms's party": (2, "the two ship's corporals"),
        },
        "marines_note": "the 294 column's two lieutenants, two serjeants, two corporals and a "
        "drummer, 7, and 43 privates, the frigate-36's share of her 264 carried to 330 "
        "(judgement; D32 (a))",
    },
}
# The quarter bill's figures beyond the trimmers (Indf §6.4): the frigate-36's two at the helm
# and no powder beyond the idlers; her small-arms men the frigate-36's share of her seamen, 20 of
# 182; her boarders a quarter of the seamen (`gen_ships.BOARDERS_NOTE`); all judgement as hers.
HELM = 2
SMALL_ARMS_OF_SEAMEN = 20.0 / 182.0
BOARDERS_OF_SEAMEN = 0.25
# The trimmers' shares by station, the frigate-36's 8, 10, 12, 6 and 8 of her 44 (judgement).
TRIMMER_SHARES = {"forecastle": 8, "fore_top": 10, "main_top": 12, "mizzen_top": 6, "afterguard": 8}


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


def at_the_guns(guns, marines):
    """The men one side's guns of a fit take, the chasers included (each chaser its own crew,
    a broadside pair one: `parts.Gun.pair_key`), and how many of them are marines, who take the
    carronades first (crew/quarters.py, the marines at the quarterdeck carronades)."""
    one_side = [gun for gun, _ in guns if gun["place"] != "broadside" or gun["side"] == g.SIDES[0]]
    men = sum(gun["crew"] for gun in one_side)
    carronades = sum(gun["crew"] for gun in one_side if gun["kind"] == "carronade")
    return men, min(carronades, marines)


def quarter_bill(b, p, guns):
    """Her quarter bill set against the default fit (Indf §6.4): the trimmers what her seamen
    leave when one side's guns, the chasers and the wheel are manned, the marines taking the
    carronades first, split by the frigate-36's shares; the bill leaves the marines not at the
    carronades for their division, which the beat to quarters does not (crew/quarters.py; her
    tests hold what it does at muster)."""
    co = COMPANY[p.key]
    seamen = sum(co["seamen"].values())
    men, marines_at = at_the_guns(guns, co["marines"])
    total = seamen - (men - marines_at) - HELM
    trimmers = shares(total, TRIMMER_SHARES)
    fit = DEFAULT_FIT[p.key]
    REPORT.setdefault(p.key, {})["bill"] = (seamen, fit, men, marines_at, total)
    b.quarter_bill(
        g.QUARTER_BILL_NOTE,
        [
            (
                "forecastle",
                trimmers["forecastle"],
                f"The trimmers: what her seamen leave when one side's guns of '{fit}', "
                "the chasers and the wheel are manned, the marines taking the carronades first, "
                "split by the frigate-36's trimmer shares, 8, 10, 12, 6 and 8 of "
                "44 (Indf §6.4; judgement). The bill leaves the marines not wanted at the "
                "carronades for their division, as Falconer quarters them on the poop and "
                "forecastle or gangway (1780, QUARTERS); the beat to quarters (crew/quarters.py) "
                "takes the marines to the long guns before the topmen (Indf §6.4; the station "
                "order is the engine's, open for the lead). Of the "
                "forecastlemen, for the head sails and the fore braces (Luce 1884 ch. XX: the "
                "forecastlemen 'the best older seamen').",
            ),
            ("fore_top", trimmers["fore_top"], "Of the fore topmen, for the fore braces aloft."),
            ("main_top", trimmers["main_top"], "Of the main topmen, the largest top."),
            (
                "mizzen_top",
                trimmers["mizzen_top"],
                "Of the mizzen topmen, for the crossjack braces and the "
                + ("mizen course." if p.mizen == "course" else "spanker."),
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
            "powder": "The powder beyond the idlers: none; her cooks, stewards, servants, clerks, "
            "the cooper, the armourers and the sailmaker's crew pass the cartridges, as the "
            "frigate-36's (judgement after Luce 1884 ch. XX, the powder division).",
            "priority": g.PRIORITY_NOTE,
        },
        small_arms=half_up(seamen * SMALL_ARMS_OF_SEAMEN),
        boarders=half_up(seamen * BOARDERS_OF_SEAMEN),
        small_arms_note="Seamen with the muskets of the stand of arms, the frigate-36's share of "
        "her seamen (20 of 182; judgement). Falconer's men to the small arms by the "
        "Admiralty's order (1780, QUARTERS, OCR l. 14335-14372: a 5th rate 50, a 4th rate of 60 "
        "guns 70, a 3rd rate of 70 guns 80) run close to whole detachments of marines, and stand "
        "for the whole party, marines and seamen (Indf §6.4).",
        boarders_note="The boarders by the bill, a quarter of her seamen told off from "
        "the guns' crews (Luce 1884 ch. XX; judgement, the shared rule), with the marines, who "
        "board with the bayonet.",
        filling=g.filling_party(guns),
    )
    b.crew_notes[("quarter_bill", "filling")] = (
        g.FILLING_NOTE + f" Her {g.filling_party(guns)} are the Regulations' quarter gunners of "
        f"the {period.REGULATIONS_COLUMNS[co['column']]} column (p. 165: Ind §4.2), the period's "
        "figure twice over (Indf §5.4)."
    )


def company(b, p, guns):
    """Her crew section (Indf §6.1-§6.2), the people drawn at muster from her wardroom file
    (§6.3), and the stores beside them: water, provisions and cordage by her complement, a shot
    plug to each of the default fit's `guns` (§7), the spare spars and the sail room by the
    frigate-36's method."""
    co = COMPANY[p.key]
    posts, drawn = g.wardroom(os.path.splitext(p.file)[0])
    idlers = sum(n for n, _ in co["idlers"].values())
    column = period.REGULATIONS_COLUMNS[co["column"]]
    complement = co["complement"]
    # the frigate-36's stores for her 264, carried by the complement (Indf §7; judgement): water
    # 100 tons, cordage 600 fathoms to the nearest fifty
    water = half_up(100.0 * complement / 264.0)
    cordage = 50 * half_up(600.0 * complement / 264.0 / 50.0)
    plugs = len(guns)
    if p.key == "sixty-four":
        whence = (
            "The class's establishment from 1794, 491 (Winfield 1793-1817 p. 99; the Regulations "
            "1806 p. 165, the 64's column; D17 (a)); 500 as built, but a file carries one "
            "complement whatever its fits, and the nine make no difference to her sailing."
        )
    else:
        whence = (
            "330 men and boys, 'at first of 310, but afterwards of 330 men' (James vol. 1 p. 454; "
            "at the Virginie, p. 361), on the 44's column of the Regulations 1806 (p. 165) with 36 "
            "seamen over it (D32 (a))."
        )
    stations_note = (
        "Hands per station, both watches together: her seamen, the complement less the "
        "posts, the marines and the idlers, shared among the six stations as the frigate-36's "
        "182 are (28, 24, 30, 14, 50 and 36: judgement, Indf §6.1-§6.2), the column's petty "
        "officers and its boys among them, the boys in the afterguard as landsmen (spec M3 9 "
        "item 6). Forecastlemen: the head, anchors and headsails; the best older seamen (Luce "
        "1884 ch. XX)."
    )
    entries = [
        (("complement",), complement, whence),
        (("names",), "english", "A King's ship: the english list in data/crew/names.yaml."),
        (("stations", "forecastle"), co["seamen"]["forecastle"], stations_note),
        (("stations", "fore_top"), co["seamen"]["fore_top"], "Fore topmen."),
        (("stations", "main_top"), co["seamen"]["main_top"], "Main topmen, the largest top."),
        (("stations", "mizzen_top"), co["seamen"]["mizzen_top"], "Mizzen topmen."),
        (
            ("stations", "afterguard"),
            co["seamen"]["afterguard"],
            "Afterguard, the boys included (spec M3 9 item 6: boys count as landsmen).",
        ),
        (("stations", "waisters"), co["seamen"]["waisters"], "Waisters."),
        (
            ("stations", "marines"),
            co["marines"],
            f"Marines: {co['marines_note']}; no establishment of private marines by rate was "
            "found (Ind §10.8). They stand watch and work as afterguard, never aloft (Luce 1884 "
            "ch. XX).",
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
            "(judgement, Indf §6.1). Able: 0.30.",
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
                f"{sum(1 for x in posts if x.endswith('lieutenant'))} lieutenants (the "
                f"Regulations 1806 p. 165, the {column} column), then the standing and warrant "
                "officers and the master-at-arms, as the frigate-36's; her wardroom file "
                f"(data/people/{p.file}) gives them. Names are drawn at muster unless a post "
                "gives one."
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
                "Regulations 1806; Ind §4.2) and judgement where it says so; they must sum to "
                "the idlers. "
                if i == 0
                else ""
            )
            + f"{text[0].upper() + text[1:]}: {n}.",
        )
        for i, (trade, (n, text)) in enumerate(co["idlers"].items())
    ]
    entries += [
        (
            ("stores", "water_tons"),
            water,
            "Water: the frigate-36's 100 tons for her 264 carried by the complement, "
            "in iron-hooped casks (Indf §7; judgement), as many weeks at a gallon a man a "
            "day as hers.",
        ),
        (
            ("stores", "provisions_days"),
            120,
            "Provisions: four months at full allowance for the complement, as the frigate-36's "
            "(judgement).",
        ),
        (("stores", "spare_spars"), {}, None),  # the booms, by class: below
        (
            ("stores", "cordage_fathoms"),
            cordage,
            "Spare rope in the boatswain's store: the frigate-36's 600 fathoms carried by the "
            "complement, to fifty fathoms (Indf §7; judgement).",
        ),
        (
            ("stores", "shot_plugs"),
            plugs,
            g.SHOT_PLUGS_NOTE + " One a gun of her default fit (Indf §7).",
        ),
        *g.ration_entries("a King's ship"),
    ]
    b.crew(entries)
    # the named few beyond the posts (package 35), each drawn from a station at muster, the
    # counts above unchanged; the roles and their notes are her wardroom file's (Indf §6.3)
    b.people(
        "The named people beyond the posts (package 35, spec M5 §22): each drawn from a station "
        f"at muster, the counts above unchanged; see data/people/{p.file}.",
        drawn,
    )
    # the booms (package 30b): the frigate-36's, by Luce's stowage (gen_ships.frigate_crew), on
    # her own spars: Steel's 64 has a jib-boom and no flying jib-boom (p. 49)
    b.spare_spars(
        "The booms: the spare spars by class, as the frigate-36's (Luce 1866 ch. XVII, 'Stowing "
        "Booms'; Luce 1884 ch. XI; Steel 1794 vol. I, 'Lashing of Booms'), of her own spars (Indf "
        "§7); see tools/ships/indefatigable.py.",
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
                "The spare jib-boom, amidships (Luce 1866); she has no flying jib-boom (Steel "
                "1794 vol. I p. 49, the 64).",
            ),
        ],
    )
    sail_room(b, p)


def sail_room(b, p):
    """Her sail room by the frigate-36's method (Luce 1884 ch. X p. 171; gen_ships.frigate_crew)
    on her own sails (Indf §7): the second of each working sail of the frigate's list that she
    carries, the heavy-weather foresail and topsails of No. 1, one of each storm sail, and her
    occasional sails."""
    canvas = {s["id"]: s["canvas_no"] for s in b.doc["sails"]}
    after = "mizzen.course" if p.mizen == "course" else "mizzen.spanker"
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
        after,
        "fore.topmast_staysail",
    ]
    heavy = ["fore.course", "fore.topsail", "main.topsail"]
    storm = ["fore.storm_staysail", "mizzen.storm_staysail", "storm_mizzen"]
    occasional = [k for k in ("mizzen.driver", "ringtail") if k in canvas] + [
        f"fore.save_all.{s}" for s in g.SIDES
    ]

    def first(text, i):
        return text if i == 0 else None

    b.sail_room(
        "The sail room (spec 3b §6.3): Luce's allowance for a frigate (1884 ch. X p. 171), as "
        "the frigate-36's, on her own sails (Indf §7), every sail new; see "
        "tools/ships/indefatigable.py.",
        [
            (
                k,
                canvas[k],
                first(
                    "The second of each working sail, of the working number (Luce p. 171); she "
                    "has one jib and no flying jib, and her "
                    + ("mizen course" if p.mizen == "course" else "spanker")
                    + " stands for the frigate's spanker.",
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
            (k, canvas[k], first("The occasional sails, one each (spec 3b §6.4).", i))
            for i, k in enumerate(occasional)
        ],
    )


# ---------------------------------------------------------------------------
# Ground tackle, boats, pumps and hold (Indf §7)
# ---------------------------------------------------------------------------

# Steel's 64 in both files (D33 (a): her burthen stayed 1,384 tons against Steel's 64's 1,369,
# and anchors answer to the hull's mass), from `period.STEEL_ANCHORS`: four bowers of 57 cwt and
# seven 21-in cables, laid three on the best bower and two on the small as on the Channel
# service (Lever 1808 p. 67, as gen_ships cites it), one on the sheet and one on the spare; 120
# fathoms a cable (Falconer 1780, CABLE). The spare anchor is of the kind `sheet`: the schema's
# kinds are four, and the moorings' "two bowers down" counts the bowers (Indf §7).
BOWER_CABLES = {"best_bower": 3, "small_bower": 2, "sheet": 1, "spare_anchor": 1}
# Her burthen and her length on the gun deck as built (Winfield 1793-1817 p. 100: 1,384 3/94
# tons; 160 ft 1 1/4 in), which the hold's and the boats' rules read; the razee's burthen the
# same (D33 (a)).
BURTHEN_TONS = 1384.0
GUN_DECK_FT = 160.0 + 1.25 / 12.0


def ground_tackle(b):
    """Steel's anchors and cables for a 64 (Indf §7), through `Builder.ground_tackle`."""
    steel = period.STEEL_ANCHORS[64]
    if len(BOWER_CABLES) != steel["bowers"] or sum(BOWER_CABLES.values()) != steel["bower_cables"]:
        raise ValueError(
            f"Steel's 64 has {steel['bowers']} bowers and {steel['bower_cables']} bower cables; "
            f"BOWER_CABLES lays {sum(BOWER_CABLES.values())} on {len(BOWER_CABLES)} (Indf §7)."
        )
    bower = round(steel["bower_cwt"] * g.CWT_KG)
    cable = steel["bower_cable_in"]
    stream = steel["stream_cable_in"]
    hawser = g.KEDGE_HAWSER_OF_BOWER * cable
    fathoms = g.CABLE_FATHOMS
    bowers = {
        "best_bower": (
            "bower",
            "the best bower",
            f"The bowers: Steel's four of {steel['bower_cwt']:g} cwt for a 64 (Steel 1794 vol. I, "
            "the anchor table, the page image read: Ind §6.2; D33 (a)); the cables Steel's seven "
            f"of {cable:g} in ('A Cordage Table', read), rated as every rope by Luce 1866 ch. IV, "
            "laid three on the best bower and two on the small, 'three Cables on the best Bower, "
            "two on the small Bower' (Lever 1808 p. 67), 120 fathoms a cable (Falconer 1780, "
            "CABLE).",
        ),
        "small_bower": ("bower", "the small bower", None),
        "sheet": ("sheet", "the sheet anchor", "The sheet anchor, a bower's size, on one cable."),
        "spare_anchor": (
            "sheet",
            "the spare anchor",
            "The spare anchor, Steel's fourth bower, on the seventh cable; of the kind 'sheet', "
            "the schema's kinds being four (Indf §7).",
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
            f"The stream anchor, Steel's {steel['stream_cwt']:g} cwt for a 64, on the stream "
            f"cable of {stream:g} in (Steel 1794 vol. I, the anchor and cordage tables: Ind "
            "§6.2).",
        ),
        (
            "kedge",
            "kedge",
            "the kedge",
            float(round(steel["kedge_cwt"] * g.CWT_KG)),
            fathoms,
            hawser,
            g.rope_kn(hawser),
            "The kedge, Steel's 7 cwt 2 qr for a 64 (as above), on a hawser of half the bower "
            "cable's size, the house rule (gen_ships.KEDGE_HAWSER_OF_BOWER; judgement).",
        ),
    ]
    b.ground_tackle(
        "The ground tackle (package 34, spec M5 §18): Steel's anchors and cables for a 64 (Steel "
        "1794 vol. I; D33 (a); Indf §7), every figure's source in tools/ships/indefatigable.py; "
        "chain cable is later than 1805.",
        anchors,
        chain=False,
    )


def boats_pumps_hold(b):
    """Her boats by Luce's rule on her length, the frigate-36's allowance; her pumps, two chain
    and two hand; her hold by her burthen (Indf §7)."""
    g.hold_for(
        b,
        BURTHEN_TONS,
        True,
        "1,384 tons as built, Winfield 1793-1817 p. 100; a ship of war's hold is her own stores "
        "and ballast: judgement",
    )
    b.pumps(
        g.PUMPS_NOTE + " Hers in the well round the main mast (ZAZ2372, read: Ind §6.5).",
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
            GUN_DECK_FT,
            True,
            [
                (
                    "launch",
                    "launch",
                    "the launch",
                    1.0,
                    "The launch, 2.6 root of her 160 ft (Luce 1866's rule); her own "
                    "boats were not found (Ind §10.11), and Steel's list for a 64, a longboat, a "
                    "pinnace and yawls or cutters (vol. II, read (OCR): Ind §6.1), agrees in kind "
                    "with the frigate-36's allowance, taken (Indf §7). The stream anchor is sent "
                    "in her (Steel 1794 vol. I: 'sent in the long-boat').",
                ),
                (
                    "barge",
                    "barge",
                    "the barge",
                    1.03,
                    "The captain's barge, a little longer than the launch and narrower "
                    "(Falconer, BARGE: 'longer, slighter, and narrower').",
                ),
                ("pinnace", "pinnace", "the pinnace", 0.9, "The pinnace (Falconer, PINNACE)."),
                (
                    "first_cutter",
                    "cutter",
                    "the first cutter",
                    0.9,
                    "The first cutter, 0.9 of the launch (Luce's rule).",
                ),
                (
                    "second_cutter",
                    "cutter",
                    "the second cutter",
                    0.81,
                    "The second cutter, 0.9 of the first.",
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
# Her descriptions (Indf §8; D16 (a))
# ---------------------------------------------------------------------------

DESCRIPTIONS = {
    "sixty-four": (
        "sixty-four",
        "a ship",
        "a sixty-four, a ship of the line of two tiers of ports",
        "The Ardent class's 64 (Winfield 1793-1817 p. 99), a third rate (Falconer 1780, RATES): "
        "what the glass makes out, her two tiers of ports; her rig's word the frigate's, three "
        "masts square-rigged.",
    ),
    "razee": (
        "razee",
        "a ship",
        "a razee, a heavy frigate cut down from a sixty-four, one tier of twenty-four-pounders",
        "Rated a 44 in Steel's List 1799-1802, the Navy List 1815-16 and by James for 1805 "
        "(vol. 3 p. 311): a frigate in every list (Indf §8), her one tier of ports a 64's lower "
        "deck's.",
    ),
}


def her_report() -> str:
    """The generator's report: what her rules compute from the files' own keys, printed as the
    files are written and held by her tests, so that it does not stand in the files' notes to go
    stale (the lead's notes of 2026-10-29, item 2)."""
    out = []
    for key in ("sixty-four", "razee"):
        r = REPORT.get(key, {})
        out += [f"{key}: {line}" for line in r.get("hull", ())]
        if "rope" in r:
            plain, scale = r["rope"]
            out.append(f"{key}: plain sail {plain:.0f} m2, her rope's scale {scale:.3f}.")
        if "bill" in r:
            seamen, fit, men, marines, total = r["bill"]
            out.append(
                f"{key}: the quarter bill on '{fit}': her {seamen} seamen, {men} men at the guns, "
                f"{marines} of them marines, and {HELM} at the wheel leave {total} trimmers."
            )
        if "upper_works" in r:
            out.append(f"{key}: {r['upper_works']}")
    r = REPORT.get("sixty-four", {})
    mz = r.get("after_sail")
    if mz:
        out.append(
            "sixty-four: mizen course: tack "
            f"{mz['corners'][0][1]:.2f} m above her water, "
            f"{(mz['corners'][0][1] - mz['deck']) / FT:.1f} ft above her quarterdeck (Steel's "
            f"{mz['steel_tack']:.2f} m would stand {mz['steel_clear']:.2f} m over her roundhouse "
            f"deck at the side at its worst); the foot {mz['clear']:.2f} m over it now; "
            f"{mz['area']} m2, centre {mz['centre']} m."
        )
    d = r.get("driver")
    if d:
        out.append(
            f"sixty-four: driver: jaws {d['boom']['jaws_z']:.2f} m, set by the "
            f"{d['set_by']}; fore leech {d['fore_leech']:.2f} m, after leech "
            f"{d['after_leech']:.2f} m (Steel's band {d['after_band'][0]:.2f}-"
            f"{d['after_band'][1]:.2f}); {d['area']:.0f} m2 against Steel's "
            f"{d['steel_area']:.1f}; centre {d['centre']:.2f} m; "
            f"{d['beyond_yard']:.2f} m beyond the yard's peak."
        )
    st = r.get("sprit", {})
    if "sprit_topsail" in st:
        s = st["sprit_topsail"]
        along, head, foot = r["sprit_drawn"]
        out.append(
            f"sixty-four: sprit topsail: {s['area']:.0f} m2; the yards {s['gap']:.2f} m apart by "
            f"height, {s['slant']:.2f} m along the slant (Steel's depth), {along:.2f} m as filed; "
            f"drawn along the slant (Ext §6.2 as built): head {head:.2f}, foot {foot:.2f}, the "
            "file's area; risk 9 closed."
        )
    for key in ("sixty-four", "razee"):
        ss = REPORT.get(key, {}).get("sprit", {}).get("spritsail")
        if ss:
            out.append(f"{key}: spritsail: foot {ss['foot_z']:.2f} m above her water.")
    sp = REPORT.get("razee", {}).get("after_sail")
    if sp:
        out.append(
            f"razee: spanker boom: jaws {sp['boom_z']:.2f} m, raised "
            f"{sp['boom_z'] - sp['filed_z']:.2f} m from {sp['filed_z']:.2f} m, "
            f"{sp['head_room_ft']:g} ft over her roundhouse deck ({sp['clear']:.2f} m), "
            f"{sp['boom_z'] - sp['taffrail']:.2f} m over her taffrail, its end "
            f"{sp['overhang_ft']:.1f} ft beyond it; spanker {sp['area']} m2 "
            f"(was {sp['filed_area']}), {sp['area'] / STEEL_DRIVER_38_M2 - 1.0:+.1%} of Steel's "
            "driver for a 38."
        )
    return "\n".join(out)


def build(out_dir: str) -> None:
    """Write her files to `out_dir`: the 64's (`sixty-four.yaml`), then the razee's derived from
    her (`razee-44.yaml`), each through `write()` (Indf §1)."""
    p64 = sixty_four()
    razee = razeed(p64)  # the derivation's checks raised before either file is written
    write(out_dir, p64)
    write(out_dir, razee)
    print(her_report(), file=sys.stderr)
