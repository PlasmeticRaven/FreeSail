"""The *Purísima Concepción* class three-decker of the Spanish navy, as rebuilt at Cádiz (1786 to
1793), in her fits of 1797 and 1809 (package 90, the fifth hull; her builder).

Her design is docs/design/Design-Ship-PurisimaConcepcion.md (cited here as Con-D), from her
research note docs/design/Research-PurisimaConcepcion-2026-11.md (Res), her measuring note
docs/design/ships-design/pages-concepcion.md (Pages, its head the owner's choice of her source and
the lead's rulings of 2026-11-20, nudges 30 and 33), Winfield's facts by page in the lead's words
(docs/design/VesselReferences-2026-11-Spanish.md, VR-Sp: §4 her entry, §7 the units, §15 her
company, §16 her guns by deck) and the engine's note on three gun decks
(docs/design/Design-Package90-Engine.md §6). One module writes one file,
`data/ships/three-decker.yaml` (Con-D decision 1; the lead's ruling 5 of 2026-11-18):
`write(out_dir)` builds and dumps it and `build(out_dir)` is the generator's hook
(`tools/gen_ships.py`, `SHIP_MODULES`).

**What she is made of.** Her hull is her own plan as built, PB-039 (Biblioteca Virtual de Defensa,
record 1026905; the Archivo Histórico de la Armada), rung S, unscaled: the owner's "Use PB-039
(Recommended)" of 2026-11-20 and the lead's rulings 1 to 5 of that day. Her sister's sheets at
Greenwich (RMG ZAZ0100 to ZAZ0103, read at 1,280 px and cited by number) are the comparison; they
place her sixteenth lower pair aftmost and her quarterdeck's and poop's ports. Her rig is the 74's
machinery (`tools/ships/bellerophon.py`), its rules copied here and not imported, since an import
would tie her bytes to another ship's module (Con-D §1.1): every length of the 74's rig x 1.15 by
Steel's rule for her main mast (Con-D §4.1), every sail's cloths and depth x 1.15, its area so
x 1.32 (Con-D §4.2, JUDGEMENT), on her own masts' places and her own decks; her mizen course cut
at the mast on its lateen yard (`tools/ships/mizen_yard.py`) and her yards under the bowsprit
(`tools/ships/spritsail_yards.py`); no driver (Con-D decision 12). Her guns are her own record's
by deck for both fits (Winfield pp. 406-410: VR-Sp §4, §16), their pounds as her navy named them
(the owner's Dec 9), the obús carried as a carronade of its calibre (Dec, Part E); her company the
1788 regulation's for her default fit, the file's, and the 1803 regulation's recorded in the 1809
fit's note (VR-Sp §15; the lead's ruling (5) of 2026-11-07: a company belongs to a file).

**The frame.** Her lines below are her measuring note's, in its frame: metres, x forward of the
middle of her load line between the post's after face and the stem's fore face, z above L0, the
straight fit of her drawn top waterline (Pages, "Units and datums"). Her water is the line as
traced (the lead's ruling 1): on L0 forward of about x -5 m and under it aft, 8.02 m to K at the
post's after face, 7.94 m at the middle and 7.65 m at the stem's fore face (Pages §12.1). Every
height is converted once to the file's frame, above her water at its own station (`fz`), as the
engine reads a height (Pages §12.1, its last paragraph: JUDGEMENT on what ruling 2 asks, the lead's
to confirm). The rig's rules are Steel's, in feet: they run in feet forward of her post's after
face on her line and feet above her water (`x_m`, `z_m`), as the 74's run in her drawings' feet. A
spar's `height_m` and a sail's `corners_m` are written above her datum, her upper deck at the
middle, 5.99 m (`deck_height_m`, ruled by the lead's nudge 33); a sail's centre above the water.

**Her notes.** The file's notes carry sources, departures and judgements; a figure a rule computes
from the file's own keys is printed by `her_report()`, the generator's report, and held by her
tests (the lead's notes of 2026-10-29, item 2). `HerBuilder` keeps the shared helpers' such
figures out of her notes, as the 74's does.

The module is imported only by the generator's entry block, after `gen_ships` is made the running
script, and takes every helper as `g.<name>`. No function or table of the generator is changed;
every other file stays byte for byte as it is.

Marks: measured (off her plan, Pages, with its uncertainty), read (the sheet or the page), via
Winfield (VR-Sp), rule, JUDGEMENT.
"""

from __future__ import annotations

import math
import os
import re
import sys

import gen_ships as g

from ships import mizen_yard, period, spritsail_yards

FT = g.FT

# Her flips, the 74's: the mizen course cut at the mast on her lateen yard (B3.1) and the yards
# under the bowsprit (B3.2), each built before her window. No driver (Con-D decision 12): the 74's
# is Steel's British boomsail, the owner's choice for the British 74 (Bel-D §4.6), and nothing
# gives it to a Spanish ship.
MIZEN_COURSE = "gated"
BOWSPRIT_YARDS = True

# The 74's rig scaled to hers (Con-D §4.1, §4.2): her main lower mast by Steel's rule, half the
# lower deck and the extreme breadth (Steel 1794 vol. I p. 39, read (OCR)), on James's *San Josef*,
# 194 ft 3 in and 54 ft 3 in (vol. 2 p. 59, read (OCR)), is 124 ft 3 in, against the 74's 108 ft
# (Lavery 1985 p. 19, Table 10): 1.150. Every length of the 74's rig is so scaled, and every sail's
# cloths and depth with it, its area by 1.32 (JUDGEMENT), until a Spanish rule or PB-078 (a 112's
# canvas, Romero Landa 1791) is read. On her own length, PB-039's 61.26 m on her lower deck, and
# James's breadth, Steel's rule would give 127 ft 7 in (computed): recorded; the ruled 1.15 filed.
RIG_SCALE = 1.15

# ---------------------------------------------------------------------------
# Her frame: K, the line as traced, and the file's heights (Pages §4.2, §6, §12.1)
# ---------------------------------------------------------------------------

# The post's after face and the stem's fore face on her line (Pages §5.1: x 3,131 to 11,870 px at
# 39.75 px a pie, 219.8 pies, 61.26 m; the lead's ruling 3).
POST_X = -30.63
STEM_X = 30.63
# K, the lowest keel line (a false keel's lower edge: judgement, as the drawn hulls file theirs,
# D29 (b)), straight, in the note's frame: 8.17 m under L0 at the post's after face, 7.73 under it
# at the knee's foot (Pages §4.2, §6; +-0.03 m).
K_LINE = [(-30.63, -8.17), (23.66, -7.73)]
# The rabbet line, straight, the body plan's base (Pages §4.2).
RABBET = [(-30.63, -7.36), (30.63, -6.83)]
# Her load line as traced, metres above K (the lead's ruling 1; Pages §12.1): 8.02 at the post's
# after face, 7.98 at x -5 m, where it leaves L0's straight fit going aft, 7.94 at the middle and
# 7.65 at the stem's fore face. The straight fit's 8.17, 7.92 and 7.67 are beside it, with the
# doubt about the photograph: the other waterlines leave their straight fits aft unevenly, so the
# sheet or its photograph may bend the line there (Pages §12.1).
TRACED_TO_K = [(-30.63, 8.02), (-5.0, 7.98), (0.0, 7.94), (30.63, 7.65)]


def interp(points, x):
    """The value at `x` of a line of (x, value) points, straight between them and held at the
    first and the last beyond them."""
    if x <= points[0][0]:
        return points[0][1]
    for (x0, v0), (x1, v1) in zip(points, points[1:], strict=False):
        if x <= x1:
            return v0 + (v1 - v0) * (x - x0) / (x1 - x0)
    return points[-1][1]


def straight(points, x):
    """The value at `x` on the straight line through a line's two points, carried beyond them."""
    (x0, v0), (x1, v1) = points
    return v0 + (v1 - v0) * (x - x0) / (x1 - x0)


def water(x):
    """Her water, the line as traced, at `x`: metres above L0 (Pages §12.1), held at the post's
    after face and the stem's fore face beyond them."""
    xc = min(max(x, POST_X), STEM_X)
    return interp(TRACED_TO_K, xc) + straight(K_LINE, xc)


def fz(x, z):
    """A height of the note's frame, metres above L0 at `x`, as the file's: above her water."""
    return z - water(x)


def fp(x, z):
    """A point of the note's frame as the file's [x, z]."""
    return [x, fz(x, z)]


# The rig's frame (Steel's rules in feet): feet forward of her post's after face on her line, and
# feet above her water at their own station.
MIDSHIPS_FT = -POST_X / FT
CHANNEL_FT = 0.0


def x_m(x_ft):
    """Feet forward of her post's after face as the file's x, metres forward of the middle."""
    return POST_X + x_ft * FT


def ft_x(x):
    """The file's x as feet forward of her post's after face."""
    return (x - POST_X) / FT


def z_m(z_ft):
    """Feet above her water as the file's z, metres."""
    return z_ft * FT


def keel_top_ft(x_ft):
    """The keel's top at `x_ft`, feet above her water (below it): the rabbet line, the body plan's
    base (Pages §4.2; judgement on the rabbet as the keel's top, as the 74's base)."""
    x = x_m(x_ft)
    return fz(x, straight(RABBET, x)) / FT


# ---------------------------------------------------------------------------
# The decks (Pages §5.3; the lead's ruling 5 and nudge 33)
# ---------------------------------------------------------------------------

# Each deck at the middle line, the upper of the pair of red lines PB-039 draws for it, z above L0
# (Pages §5.3: measured, +-0.02 m; the upper line read as the plank's upper side, the second as the
# beam's, judgement), at the sheer's stations; the decks' ends forward of +19 and aft of -27 not
# traced. Accepted as measured (ruling 5).
DECK_LINES = {
    "poop": [(-27.34, 10.50), (-22.78, 10.33)],
    "quarterdeck": [(-27.34, 8.55), (-22.78, 8.37), (-17.53, 8.11)],
    "upper": [
        (-27.34, 6.41), (-22.78, 6.26), (-17.53, 6.15), (-12.27, 6.08), (-7.01, 6.09),
        (-1.41, 6.08), (2.10, 6.05), (7.71, 6.04), (18.92, 6.02),
    ],
    "middle": [
        (-27.34, 4.28), (-22.78, 4.12), (-17.53, 4.00), (-12.27, 3.92), (-7.01, 3.92),
        (-1.41, 3.90), (2.10, 3.90), (7.71, 3.87), (13.31, 3.92), (18.92, 3.98),
        (23.83, 4.15), (26.63, 4.25),
    ],
    "lower": [
        (-27.34, 1.86), (-22.78, 1.72), (-17.53, 1.58), (-12.27, 1.52), (-7.01, 1.54),
        (-1.41, 1.52), (2.10, 1.53), (7.71, 1.52), (13.31, 1.56), (18.92, 1.74),
        (23.83, 1.87), (26.63, 1.85),
    ],
}  # fmt: skip
# The waist's gangway and the forecastle, one red line forward from the quarterdeck's after part
# (Pages §5.3, measured), the gangways at the side over the waist and the forecastle's deck
# forward.
GANGWAY_AND_FORECASTLE = [
    (-7.01, 7.65), (-1.41, 7.63), (2.10, 7.62), (7.71, 7.66), (13.31, 7.75), (18.92, 7.91),
    (23.83, 8.10), (26.63, 8.45),
]  # fmt: skip
# The orlop's red line (Pages §5.3): no deck word of the file (`schema.DECK_WORDS`); in her note.
ORLOP_MID_M = -0.90
# The 74's method for a deck's surface (the lead's ruling 4 and nudge 33): the mean of the pair of
# red lines her sheet draws for it, where Pages took the upper. Her pair stands 15 to 16 px apart,
# 0.105 to 0.112 m (Pages §5.3, measured): half of 0.11 m taken, so that every deck of hers stands
# 0.055 m under the upper line (Pages §5.3: "every deck of hers lower by the same 0.05 to 0.06 m").
DECK_PAIR_HALF_M = 0.055
# Her datum, ruled: her upper deck at the middle by the 74's method above her line as traced, 5.99
# m (the lead's nudge 33, 2026-11-20; 6.06 m by Pages' upper line beside it, 5.98 to 6.00 by the
# 74's method: Pages §5.3). `check_hull` holds the deck below to it within a centimetre.
DATUM = 5.99

# The decks' extents beyond what PB-039's red lines give (JUDGEMENT, each): the poop's breast at x
# -20.5, forward of the foremost of the three small ports ZAZ0100 draws on her sister's poop (x
# -21.4: Pages §11.3) and short of -17.53, where PB-039 draws no poop; the quarterdeck carried
# forward to its breast at -6.5, over the foremost of the six ports a side ZAZ0100 draws on it (x
# -7.3), on the gangway line's height there; the forecastle from its breast at +13.0, about a fifth
# of her length forward of the middle as the 74's (121 ft from AP, Bel-D §3.2), to the beakhead
# bulkhead at +27.9, the 74's 7.4 ft abaft the stem at her water scaled by the lengths; the upper
# deck carried forward of +18.92 to +26.63 by the middle deck's rise there; the poop's and the
# quarterdeck's after ends at the stern's after edge, each on its own slope.
POOP_BREAST_X = -20.5
QUARTERDECK_BREAST_X = -6.5
FORECASTLE_BREAST_X = 13.0
BEAKHEAD_X = 27.9


def _sloped(points, x):
    """A line's height at `x` beyond its points, carried on the slope of its two nearest."""
    (x0, v0), (x1, v1) = (points[0], points[1]) if x < points[0][0] else (points[-2], points[-1])
    return v0 + (v1 - v0) * (x - x0) / (x1 - x0)


def deck_extents():
    """Each deck's upper red line over its extent, (x, z above L0), PB-039's points and the
    extents above (JUDGEMENT where they say so)."""
    poop = list(DECK_LINES["poop"])
    qd = list(DECK_LINES["quarterdeck"])
    stern_poop = stern_x_at(_sloped(poop, -32.8))
    poop = [(round(stern_poop, 2), round(_sloped(poop, stern_poop), 2)), *poop]
    poop.append((POOP_BREAST_X, round(_sloped(DECK_LINES["poop"], POOP_BREAST_X), 2)))
    stern_qd = stern_x_at(_sloped(qd, -32.3))
    qd = [(round(stern_qd, 2), round(_sloped(qd, stern_qd), 2)), *qd]
    qd.append(GANGWAY_AND_FORECASTLE[0])
    qd.append(
        (QUARTERDECK_BREAST_X, round(interp(GANGWAY_AND_FORECASTLE, QUARTERDECK_BREAST_X), 2))
    )
    fc = [(FORECASTLE_BREAST_X, round(interp(GANGWAY_AND_FORECASTLE, FORECASTLE_BREAST_X), 2))]
    fc += [p for p in GANGWAY_AND_FORECASTLE if p[0] > FORECASTLE_BREAST_X]
    fc.append((BEAKHEAD_X, round(_sloped(GANGWAY_AND_FORECASTLE, BEAKHEAD_X), 2)))
    upper = list(DECK_LINES["upper"])
    rise = interp(DECK_LINES["middle"], 26.63) - interp(DECK_LINES["middle"], 18.92)
    rise_23 = interp(DECK_LINES["middle"], 23.83) - interp(DECK_LINES["middle"], 18.92)
    upper += [(23.83, round(upper[-1][1] + rise_23, 2)), (26.63, round(upper[-1][1] + rise, 2))]
    return {
        "lower": list(DECK_LINES["lower"]),
        "middle": list(DECK_LINES["middle"]),
        "upper": upper,
        "quarterdeck": qd,
        "forecastle": fc,
        "roundhouse": poop,
    }


def deck_m(word, x):
    """A deck's surface at `x` by the 74's method, the file's z (above her water there)."""
    return fz(x, interp(DECKS[word], x) - DECK_PAIR_HALF_M)


# ---------------------------------------------------------------------------
# The ports and their sills (Pages §5.2, §11.3; ruling 5)
# ---------------------------------------------------------------------------

# One side's ports, [x, sill z above L0, half-breadth at the sill], from aft (Pages §5.2: measured
# on PB-039 by their heavy edges; x +-0.02 m, sills +-0.02, half-breadths +-0.05, +-0.15 at the
# end ports; the half-breadths the body plan's at the sill's height, read as moulded: JUDGEMENT,
# Pages §4.5). Accepted as measured (ruling 5).
LOWER_PORTS = [
    (-24.66, 2.30, 6.80), (-21.12, 2.16, 7.18), (-17.57, 2.07, 7.44), (-14.02, 2.00, 7.63),
    (-10.47, 1.95, 7.79), (-6.91, 1.93, 7.93), (-3.39, 1.93, 8.04), (0.18, 1.91, 8.07),
    (3.78, 1.89, 7.99), (7.32, 1.90, 7.97), (10.89, 1.97, 7.90), (14.46, 2.05, 7.79),
    (18.02, 2.17, 7.64), (21.60, 2.30, 7.24), (25.18, 2.48, 6.11),
]  # fmt: skip
MIDDLE_PORTS = [
    (-26.46, 4.72, 6.15), (-22.89, 4.59, 6.46), (-19.36, 4.48, 6.69), (-15.80, 4.39, 6.83),
    (-12.25, 4.32, 6.95), (-8.67, 4.30, 7.04), (-5.15, 4.31, 7.10), (-1.60, 4.30, 7.16),
    (1.98, 4.29, 7.12), (5.52, 4.29, 7.01), (9.09, 4.33, 7.00), (12.68, 4.38, 6.97),
    (16.18, 4.47, 6.86), (19.82, 4.59, 6.68), (23.36, 4.75, 6.08), (26.97, 4.93, 4.67),
]  # fmt: skip
UPPER_PORTS = [
    (-28.27, 6.70, 5.36), (-24.68, 6.57, 5.72), (-21.14, 6.47, 5.95), (-17.58, 6.39, 6.13),
    (-14.02, 6.33, 6.27), (-10.48, 6.31, 6.37), (-6.92, 6.30, 6.45), (-3.40, 6.29, 6.54),
    (0.21, 6.30, 6.57), (3.79, 6.29, 6.32), (7.35, 6.29, 6.27), (10.89, 6.36, 6.26),
    (14.47, 6.43, 6.23), (18.02, 6.52, 6.19), (21.61, 6.65, 5.88), (25.18, 6.81, 5.31),
]  # fmt: skip
# The sixteenth lower pair, cut at Cádiz in 1791 and unarmed in Spanish service (VR-Sp §4): the
# aftmost, under the upper tier's aftmost port at x -28.27, as ZAZ0100 draws every lower port under
# an upper one (Pages §11.3, read; ruling 5). PB-039 does not draw it, so its sill is the lower
# tier's sheer carried aft from its two aftmost ports (JUDGEMENT), and its half-breadth her drawn
# side's at its sill (the Diana's bow port's road, the lead's nudge 59), the port shaping no line of
# hers; its first figure, about 4.8 m between the water's there and the upper port's over it
# (JUDGEMENT), only seeds the drawing.
SIXTEENTH_LOWER = (-28.27, 2.44, 4.80)
# The quarterdeck: six ports a side at ZAZ0100's places, x -18.8 to -7.3, 2.30 m apart (Pages
# §11.3: read at 1,280 px on her sister's sheet, about +-0.1 m); the poop's three small ports at
# x -25.4, -23.4 and -21.4 (the same), taken as gun places over the rail, their sills not read; the
# forecastle's places not made out on any sheet (Pages §11.3), three a side taken over the upper
# tier's three foremost ports (JUDGEMENT), for the fits' six and four forecastle guns.
QUARTERDECK_PORTS_X = (-18.8, -16.5, -14.2, -11.9, -9.6, -7.3)
POOP_PLACES_X = (-25.4, -23.4, -21.4)
FORECASTLE_PORTS_X = (18.02, 21.61, 25.18)
# The upper works' sills, the deck and 1 ft (the 74's forecastle's and quarterdeck's, 1.0 to 1.1
# ft over their deck: Bel §3.3; JUDGEMENT for hers); a place over the rail 2 in under it (the 64's
# and the 74's convention).
SILL_ABOVE_DECK_M = 1.0 * FT
OVER_THE_RAIL_M = 0.05
# The side above her upper tier tumbles home as her midship section does from 4 to 7 m above L0,
# 7.31 to 6.43 m (Pages §6, measured): 0.29 m of half-breadth to the metre, carried up to the
# upper works' sills and the top of the side from the upper tier's half-breadth at each station
# (JUDGEMENT, the side above the upper tier not traced: Pages §6).
TUMBLEHOME_PER_M = 0.29
# The ports' sizes, width by depth (Pages §5.2: measured, +-1 cm; ruling 5): the lower 1.01 x 0.93
# m, the middle 0.91 x 0.76, the upper 0.80 x 0.67; the upper works' not measured, the 74's
# quarterdeck's 2 ft 7 in by 2 ft 4 in (Con-D §3.4, JUDGEMENT).
PORT_SIZE_M = {
    "lower": (1.01, 0.93),
    "middle": (0.91, 0.76),
    "upper": (0.80, 0.67),
    "quarterdeck": (0.79, 0.71),
    "forecastle": (0.79, 0.71),
    "roundhouse": (0.79, 0.71),
}
# The lee port (Con-D §10; Pages §5.2): the midship lower port, No. 8 from forward at x +0.18,
# dipping at 13.3 deg on L0 (the sill's z over its half-breadth); on her line as traced, which
# stands 0.02 m over L0 there, 13.2 (computed: `check_hull`).
MIDSHIP_LOWER_X = 0.18

# ---------------------------------------------------------------------------
# Her lines (Pages §5, §6; ruling 5)
# ---------------------------------------------------------------------------

# The half-breadth at L0 at the body plan's stations, aft 9 to fore 7 (Pages §6: measured, read as
# moulded, as drawn: JUDGEMENT, Pages §4.5); her plank (3 to 4 pulgadas, JUDGEMENT) is in her mass
# and not on her lines, as the *Diana*'s.
BREADTH_AT_L0 = [
    (-28.63, 2.75), (-26.43, 5.57), (-23.29, 6.83), (-19.84, 7.33), (-16.33, 7.65), (-12.84, 7.84),
    (-9.38, 7.99), (-6.00, 8.11), (-2.49, 8.17), (0.99, 8.17), (4.48, 8.06), (8.00, 8.06),
    (11.46, 8.00), (14.97, 7.90), (18.50, 7.72), (21.96, 7.22), (25.49, 5.81), (27.24, 4.47),
]  # fmt: skip
# The midship section "m" aft, at x +0.99, (z above L0, half-breadth), moulded (Pages §6: measured;
# its area to L0 99.2 m2, its greatest half-breadth 8.18 m at z +0.54, the floor nearly flat for 4
# m out from the keel, the turn of the bilge sharp).
MIDSHIP_X = 0.99
SECTION = [
    (-7.00, 0.59), (-6.90, 1.52), (-6.75, 4.10), (-6.50, 4.96), (-6.00, 5.89), (-5.50, 6.42),
    (-5.00, 6.77), (-4.00, 7.31), (-3.00, 7.71), (-2.00, 7.98), (-1.00, 8.13), (0.00, 8.17),
    (1.00, 8.18), (2.00, 8.05), (3.00, 7.74), (4.00, 7.31), (5.00, 6.93), (6.00, 6.63),
    (7.00, 6.43),
]  # fmt: skip
# The stem's fore face from the forefoot (the keel's lower edge there) to her line (Pages §5.1, §6:
# measured), plumb from the line to the lower deck (Pages §5.1: the length at the lower deck's
# height ends at the same x); behind the head to the stem head, not measured, on the 74's rake
# there (1.1 ft over the 16.25 ft from WL1 to her stem head: ZAZ1357, task 2), to a head 1.23 m
# over her upper deck carried to the stem, the 74's 3.5 ft x 1.15 (JUDGEMENT).
STEM = [
    (23.64, -7.45), (25.81, -7.00), (28.76, -5.00), (30.03, -3.00), (30.38, -2.00),
    (30.58, -1.00), (30.63, 0.00), (30.63, 1.50),
]  # fmt: skip
STEM_RAKE = 1.11 / 16.25
STEM_HEAD_ABOVE_UPPER_M = 3.5 * RIG_SCALE * FT
# The knee of the head's fore edge from K (Pages §5.1, §6: measured) to her line, and above it to
# the head's top under the figure the 74's knee (ZAZ1357, task 2: Bel-D §3.2) by its offsets from
# its own knee at WL1, x by her length over the 74's and z so that its top stands over her rail's
# fore end as the 74's stands 0.7 ft over hers (JUDGEMENT: PB-039's head above her line not
# measured, Pages §5.1 "and on to the beakhead and figure (read)").
HEAD = [
    (23.66, -7.73), (26.49, -7.00), (28.12, -6.00), (29.15, -5.00), (29.87, -4.00),
    (30.43, -3.00), (30.86, -2.00), (31.21, -1.00), (31.54, 0.00),
]  # fmt: skip
# The 74's knee above WL1, (ft above WL1, ft forward of its knee at WL1, 172.51 ft from AP):
# ZAZ1357 traced (Bel-D §3.2, `bellerophon.HEAD_FT`); its top 22.0 ft above WL1, the 74's rail's
# fore end 21.30 (her `RAIL_FT`).
SEVENTY_FOURS_KNEE_FT = [
    (2.0, 1.23), (4.0, 2.63), (6.0, 4.31), (8.0, 6.31), (10.0, 8.31), (12.0, 9.94),
    (14.0, 10.75), (16.0, 11.00), (18.0, 10.77), (20.0, 10.55), (22.0, 10.02),
]  # fmt: skip
SEVENTY_FOURS_KNEE_TOP_OVER_RAIL_FT = 22.0 - 21.30
SEVENTY_FOURS_LENGTH_M = 51.2
# The post's after face, raked 1.5 deg to the keel's square (Pages §5.1, measured), from K to the
# counter's knuckle, the wing transom: not read on PB-039 (its stern board is ZAZ0101's, not read:
# Pages §5.5), taken 0.82 m over her lower deck at the stern, the 74's 2.3 ft over hers x 1.15
# (ZAZ1357: Bel-D §3.2; JUDGEMENT); the stern's after edge from there to the taffrail's top, 11.84
# m at x -33.23 (Pages §5.5, measured), straight (JUDGEMENT: raked aft from the counter to the
# taffrail, read).
POST_RAKE_DEG = 1.5
KNUCKLE_ABOVE_LOWER_DECK_M = 2.3 * RIG_SCALE * FT
TAFFRAIL = (-33.23, 11.84)
# The transom's half-breadths at the taffrail's side and at the knuckle, the 74's share of her
# half-beam (ZAZ1357's body plan: 9.9 ft and 15.0 ft with the plank against her 23 ft 4 1/2 in,
# 0.44 and 0.66: Bel-D §3.2) on hers (JUDGEMENT: her stern not read); its round-up the 74's 0.28 ft
# x 1.15 (JUDGEMENT).
TRANSOM_HB_SHARE = (0.44, 0.66)
ROUND_UP_M = 0.28 * RIG_SCALE * FT
# Her quarter galleries and the stern's lights (Pages §5.5: measured on the quarter, +-0.05 m by
# eye; accepted, ruling 5): two closed galleries and a third tier of lights over them, the lights
# at z 4.80 to 5.92, 7.39 to 7.95 and 9.39 to 9.92 above L0, the lowest gallery from x -32.1 to
# -28.2; the upper two's spans taken as the lowest's (JUDGEMENT). Each band of the stern's lights
# at a gallery's tier, eight lights (the 74's count, Lavery 1985 D1) spread over 0.8 of the
# transom's half-breadth at the band (JUDGEMENT: her stern board, ZAZ0101's, not read).
GALLERIES = [(-32.1, -28.2, 4.80, 5.92), (-32.1, -28.2, 7.39, 7.95), (-32.1, -28.2, 9.39, 9.92)]
LIGHTS_A_BAND = 8
LIGHTS_SPREAD = 0.8
# The main wale amidships (Pages §5.4: measured at x +1.4, +-0.02 m), its lower edge 0.17 m and
# its upper edge 1.09 m above L0, carried along the length parallel to the lower tier's sills (the
# 74's rule: JUDGEMENT, not traced along the length). The channel wales, between her middle and
# upper tiers, where a three-decker's channel wales stand (Steel), set in the gap at the middle as
# the 74's stands in hers (Bel §3.3: 0.44 ft over the lower port tops, 0.75 ft under the upper
# sills of 3.79 ft, 0.12 and 0.20 of it) and carried parallel to the upper sills (JUDGEMENT); the
# middle wales between her lower and middle tiers have no key, and stand in her note.
MAIN_WALE_AT = (1.40, 0.17, 1.09)
CHANNEL_WALE_SHARE = (0.12, 0.20)
WALE_XS = [float(x) for x in range(-27, 28, 3)]
# The bulwark over her upper works (JUDGEMENT): the top of the side 1.0 m over the poop, the
# quarterdeck, the gangways and the forecastle, the 74's quarterdeck rail's 3.35 ft over its deck
# (ZAZ1357 at 60 ft from AP: Bel §3.3); the taffrail's top measured.
BULWARK_M = 1.0

# ---------------------------------------------------------------------------
# The rig (Con-D §4; the 74's, Bel-D §4.1-§4.3, x 1.15)
# ---------------------------------------------------------------------------

# Her masts' places, PB-039's stumps above the rail (Pages §5.7: measured, +-0.05 m; ruling 5),
# upright within the reading (ZAZ0101's stumps and the partners on ZAZ0102's middle deck at the
# same spacing: Pages §11.5); their heels above the keel's top the 74's x 1.15 (ZAZ1359: Bel §5.2;
# JUDGEMENT). Each lower mast is stepped on the keel and stands through three decks.
MASTS = {
    "fore": (ft_x(23.37), 5.9 * RIG_SCALE, 0.0),
    "main": (ft_x(-3.47), 5.11 * RIG_SCALE, 0.0),
    "mizzen": (ft_x(-18.94), 7.85 * RIG_SCALE, 0.0),
}
# The 74's masts and yards (Dragon's: Lavery 1985 p. 19, Table 10, read (owner's book); where it
# lacks a spar, Steel 1794 vol. I p. 49's 74 column: Bel-D §4.1), feet, each x 1.15 below.
SEVENTY_FOURS_SPARS_FT = {
    "mast": {"main": 108.0, "fore": 95.0 + 8.0 / 12.0, "mizzen": 93.5},
    "topmast": {"main": 64.0 + 10.0 / 12.0, "fore": 57.75, "mizzen": 47.0 + 8.0 / 12.0},
    "topgallant_mast": {"main": 33.0, "fore": 28.0 + 10.0 / 12.0, "mizzen": 24.5 * 0.973},
    "yard": {"main": 96.0 + 8.0 / 12.0, "fore": 84.0 + 4.0 / 12.0, "mizzen": 61.5},
    "topsail_yard": {"main": 70.5, "fore": 61.5, "mizzen": 46.0 + 1.0 / 12.0},
    "tg_yard": {"main": 45.0 + 10.0 / 12.0, "fore": 40.0, "mizzen": 31.5},
    "royal_yard": {"main": 35.0, "fore": 31.0, "mizzen": 23.0},
    "mizen_yard": 86.5,
    "bowsprit": 66.0,
    "jib_boom": 48.0,
}


def _scaled(v):
    if isinstance(v, dict):
        return {k: _scaled(x) for k, x in v.items()}
    return v * RIG_SCALE


SPARS_FT = _scaled(SEVENTY_FOURS_SPARS_FT)
# Steel's heads (vol. I, OCR l. 4697-4699, read (OCR); p. 42): 5 in to every yard of the main and
# fore masts, 4 in the mizen mast's and the main and fore topmasts', 3 1/2 in the rest.
HEAD_IN_PER_YARD = {
    "mast": {"main": 5.0, "fore": 5.0, "mizzen": 4.0},
    "topmast": {"main": 4.0, "fore": 4.0, "mizzen": 3.5},
    "topgallant_mast": {"main": 3.5, "fore": 3.5, "mizzen": 3.5},
}
# Steel's long pole-head (Steel 1794 vol. I p. 16 and p. 42; the 74's, Bel-D §4.2).
LONG_POLE_OF_STOP = 2.0 / 3.0
HOUNDS_OF_STOP = 3.0 / 5.0
# The bowsprit: steeved as the 74's, 31.6 deg (ZAZ1357, task 7), rooted on her stem head, its heel
# the 74's 14.73 ft abaft her stem head x 1.15 (JUDGEMENT: PB-039's bowsprit not measured, Pages
# §5); the jib-boom 7/12 outboard (Luce 1866 ch. VII, the frigate's rule; the 74's).
BOWSPRIT_STEEVE_DEG = 31.6
BOWSPRIT_HEEL_ABAFT_HEAD_FT = 14.73 * RIG_SCALE
JIB_BOOM_OUTBOARD = 7.0 / 12.0
# The yards under the bowsprit, the 74's (Lavery 1985 Table 10, 61 ft 6 in and 40 ft 0 in; Steel's
# table IV, the 74: 29 cloths 8 yards deep, 18 1/2 and 29 1/2 cloths 10 yards deep), x 1.15.
SPRITSAIL = {
    "yard_m": 61.5 * RIG_SCALE * FT,
    "head_cloths": 29.0 * RIG_SCALE,
    "foot_cloths": 29.0 * RIG_SCALE,
    "depth_yd": 8.0 * RIG_SCALE,
}
SPRIT_TOPSAIL = {
    "yard_m": 40.0 * RIG_SCALE * FT,
    "head_cloths": 18.5 * RIG_SCALE,
    "foot_cloths": 29.5 * RIG_SCALE,
    "depth_yd": 10.0 * RIG_SCALE,
}
SPRITSAIL_STATION = 0.85
SPRITSAIL_HANG_M = 0.8 * RIG_SCALE
SPRIT_TOPSAIL_HANG_M = 0.5 * RIG_SCALE
SPRIT_BRACE_LIMIT_DEG = 30
SPRITSAIL_CANVAS = (2, f"{g.STEEL_SM}, 'Spritsail course': No. 2 or 3, the first taken")
SPRIT_TOPSAIL_CANVAS = (6, f"{g.STEEL_SM}, 'Spritsail topsail': No. 6 or 7, the first taken")
# Steel's sail table IV, the 74 column (Steel 1794 vol. I p. *149: Bel §5.6), cloths at the head
# and the foot and the depth in yards, each x 1.15 (Con-D §4.2, JUDGEMENT); 22 1/2 in a cloth.
SEVENTY_FOURS_SAILS = {
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
STEEL_SAILS = {k: tuple(v * RIG_SCALE for v in row) for k, row in SEVENTY_FOURS_SAILS.items()}
CLOTH_IN_SAIL_FT = 22.5 / 12.0
# The headsails of the same column, the cloths in the foot and the leech in yards, x 1.15.
STEEL_HEADSAILS = {
    k: (foot * RIG_SCALE, leech * RIG_SCALE)
    for k, (foot, leech) in {
        "fore.staysail": (22.0, 13.0),
        "fore.topmast_staysail": (21.0, 17.5),
        "jib": (26.0, 25.0),
    }.items()
}
# The staysails between the masts in the same column: its row in words, its figures (the cloths at
# the head and the foot, the bunt and the after leech in yards) x 1.15, and Steel's area by Steel's
# rule for the canvas x 1.32, with the 74's band (Bel-D §4.4).
AREA_SCALE = RIG_SCALE * RIG_SCALE
STEEL_BETWEEN = {
    sid: (words, tuple(None if v is None else v * RIG_SCALE for v in figures), area * AREA_SCALE,
          band)
    for sid, (words, figures, area, band) in {
        "main.staysail": ("0 / 31 cloths, leech 15 3/4 yards", (0.0, 31.0, None, 15.75), 128.0,
                          0.10),
        "main.topmast_staysail": ("25 / 27 cloths, bunt 9 1/2, after leech 24 yards",
                                  (25.0, 27.0, 9.5, 24.0), 228.0, 0.25),
        "middle_staysail": ("24 / 24 cloths, bunt 7 1/2, after leech 16 1/2 yards",
                            (24.0, 24.0, 7.5, 16.5), 150.0, 0.25),
        "main.topgallant_staysail": ("21 / 21 cloths, bunt 6, after leech 15 1/2 yards",
                                     (21.0, 21.0, 6.0, 15.5), 118.0, 0.25),
        "mizzen.staysail": ("20 1/2 / 22 1/2 cloths, bunt 9, after leech 13 1/2 yards",
                            (20.5, 22.5, 9.0, 13.5), 126.0, 0.25),
        "mizzen.topmast_staysail": ("19 / 20 cloths, bunt 6 1/2, after leech 14 1/2 yards",
                                    (19.0, 20.0, 6.5, 14.5), 107.0, 0.25),
    }.items()
}  # fmt: skip
# The mizen course (the same column: 16 cloths at the head, 17 at the foot, its fore leech 11
# yards and its after leech 21), x 1.15; its tack the 74's 9 ft over the deck the mast stands
# through x 1.15 (Bel-D §4.5; JUDGEMENT): hers is her quarterdeck, the poop ending abaft her mizen.
STEEL_MIZEN_COURSE = tuple(v * RIG_SCALE for v in (16.0, 17.0, 11.0, 21.0))
MIZEN_TACK_ABOVE_DECK_FT = 9.0 * RIG_SCALE
# Steel's driver boom, the main topsail yard's length (Steel 1794 vol. I p. 40): she carries none,
# and the storm mizzen's foot is set by it as the 74's is (JUDGEMENT).
DRIVER_BOOM_FT = SPARS_FT["topsail_yard"]["main"]
# Steel's reef bands for the 74's rate (Bel §5.6), hers the same.
REEFS = {"course": 2, "topsail": {"main": 4, "fore": 3, "mizzen": 3}, "topgallant": 0, "royal": 0}
# The brace limits, the 74's (the frigate-36's, Fincham 1843 art. 102: Bel-D §4.3), no source for
# a first rate's being read (Con-D §4.3).
BRACE_PLANS = {
    "fore": [("course", 62), ("topsail", 64), ("topgallant", 66), ("royal", 68)],
    "main": [("course", 64), ("topsail", 66), ("topgallant", 68), ("royal", 70)],
    "mizzen": [("topsail", 62), ("topgallant", 64), ("royal", 66)],
}
CROSSJACK_BRACE_DEG = 60
# Her fore channel over her upper tier (PB-039 draws her channels above it, their chain plates down
# across it: Con-D §13, read), its height above her water the 74's 2.6 ft over its upper port tops
# x 1.15 over hers at the fore mast (Bel §3.3; JUDGEMENT): for the fore lower studding-sail boom and
# the save-all, as the 74's.
FORE_CHANNEL_OVER_PORT_TOPS_FT = 2.6 * RIG_SCALE
# The shrouds a side, the 74's (the 64's count: Bel-D §4.3; JUDGEMENT for hers).
SHROUDS = {"fore": 10, "main": 10, "mizzen": 7}
# The frigate-36's plain sail, m2, against which her rope is scaled (the 74's rule, Bel-D §4.3).
FRIGATE_PLAIN_SAIL_M2 = 1584.0
# Her studding sails, the 74's set (Steel's table IV, the 74: cloths at the head and the foot and
# the depth in yards, x 1.15) on booms by Steel's p. 40 rules on her own yards: the lower boom
# five-ninths of the main yard, the topmast booms half the lower yards, the topgallant booms half
# the topsail yards.
_S = SPARS_FT
STUDDING = {
    ("fore", "lower"): (18.0 * RIG_SCALE, 18.0 * RIG_SCALE, 15.0 * RIG_SCALE,
                        5.0 / 9.0 * _S["yard"]["main"]),
    ("fore", "topmast"): (14.0 * RIG_SCALE, 18.0 * RIG_SCALE, 18.5 * RIG_SCALE,
                          0.5 * _S["yard"]["fore"]),
    ("fore", "topgallant"): (10.0 * RIG_SCALE, 14.0 * RIG_SCALE, 9.25 * RIG_SCALE,
                             0.5 * _S["topsail_yard"]["fore"]),
    ("main", "topmast"): (15.0 * RIG_SCALE, 19.0 * RIG_SCALE, 23.75 * RIG_SCALE,
                          0.5 * _S["yard"]["main"]),
    ("main", "topgallant"): (11.0 * RIG_SCALE, 15.0 * RIG_SCALE, 10.25 * RIG_SCALE,
                             0.5 * _S["topsail_yard"]["main"]),
}  # fmt: skip
# The storm canvas's heights above the deck she works it from (the 74's, x 1.15: JUDGEMENT).
MIZEN_STAY_COLLAR_FT = 12.0 * RIG_SCALE
STORM_STAYSAIL_HEAD_OF_STAY = 0.6
STORM_STAYSAIL_CLEW_FT = 7.0 * RIG_SCALE
STORM_MIZZEN_TACK_FT = 4.0 * RIG_SCALE
STORM_MIZZEN_LUFF_OF_RUN = 0.8
STORM_MIZZEN_FOOT_OF_BOOM = 0.45
SAVE_ALL_OF_BOOM = 0.6
# The 64's rope scale (the 74's reference for the mizen yard's lines read from the 64's list).
RUN_64_ROPE_SCALE = 1.08

# What the cuts compute from the file's own keys, for the generator's report (`her_report`).
REPORT: dict = {}

# ---------------------------------------------------------------------------
# Her hull's figures (Con-D §2; the lead's rulings 1 to 5 and nudge 33)
# ---------------------------------------------------------------------------

HULL = {
    "length_waterline_m": 61.26,
    "beam_m": 16.54,
    "draught_m": 7.94,
    "displacement_kg": 4440000.0,
    "gm_m": 1.5,
    "clr_x_m": 6.3,
    "lateral_area_m2": 473.5,
    "hull_speed_kn": 13.1,
    "rudder": {"area_m2": 13.3, "max_angle_deg": 25, "rate_deg_s": 3.0, "span_m": 8.29},
}
# The drawn displacement, tonnes, by her line (Pages §4.3, §12.1: computed, +-2%), and the ruled
# range (the lead's ruling 2), against which `check_hull` holds her file's mass.
DRAWN_T = {
    "straight fit, with the keel": 4349.0,
    "straight fit, 3 to 4 pulgadas": (4443.0, 4473.0),
    "as traced, with the keel": 4327.0,
    "as traced, 3 to 4 pulgadas": (4421.0, 4452.0),
}
RULED_T = (4421.0, 4473.0)
WINFIELD_T = 5167.0
HULL_NOTES = {
    "length_waterline_m": "61.26 m, PB-039's from the post's after face to the stem's fore face on "
    "her line, 219.8 pies (Pages §5.1, measured; the lead's ruling 3); 220.0 pies outside them at "
    "the lower deck and 215.5 between the rabbets there. Winfield's rebuilt eslora, 220 pies 6 "
    "pulgadas, 61.30 m as printed (p. 407: VR-Sp §4), beside it; whether the eslora is taken "
    "between the rabbets or outside stays open. Plainly: D29 (b) files the drawn hulls' length "
    "rabbet to rabbet at the load line; hers, as the Diana's, is post to stem by the ruling.",
    "beam_m": "16.54 m, James's extreme breadth of her sister the San Josef, 54 ft 3 in (vol. 2 "
    "p. 59, read (OCR); Con-D §2), the file's beam being the extreme, as the 74's; PB-039's "
    "moulded breadth at her line 16.34 m amidships (Pages §6), the as-built manga 58 pies 0 "
    "(16.16 m) and the rebuilt 16.25 m (VR-Sp §4) beside it, the book's manga read as inside the "
    "plank (JUDGEMENT).",
    "draught_m": "7.94 m to K at the middle of her load line as traced on PB-039 (the lead's "
    "ruling 1; Pages §12.1, measured): 8.02 m at the post's after face and 7.65 m at the stem's "
    "fore face, a drag of 0.37 m; the straight fit's 7.92 m (8.17 and 7.67, a drag of 0.50) beside "
    "it, with the doubt about the photograph (the other waterlines leave their straight fits aft "
    "unevenly). The middle of a bent line taken, not the mean of its ends, 7.84 m (JUDGEMENT, for "
    "the lead: Con-D §18 item 8). K the false keel's lower edge (judgement), as the drawn hulls "
    "file theirs.",
    "displacement_kg": "Her body as drawn on PB-039, outside the plank, at her line as drawn: "
    "about 4,440 t, the range 4,421 to 4,473 t (the line as traced and the straight fit, each "
    "outside 3 to 4 pulgadas of plank), the plank's thickness JUDGEMENT, no scantling source being "
    "read (the lead's ruling 2; Pages §4.3, §12.1: computed, +-2%); 4,327 t with the keel and no "
    "plank to the line as traced. Winfield's 5,167 t (p. 407: VR-Sp §4) beside it: read as "
    "toneladas of 2,000 libras (921.6 kg, the Diana's table's unit) about 4,762 t, most likely "
    "reckoned level near her after draught (JUDGEMENT; the book's own mark on the figure would "
    "settle it: Pages §12.5); as metric tonnes it would need a line 0.8 to 0.9 m above her drawn "
    "one, in the main wale's band, drawn nowhere on the sheet.",
    "gm_m": "JUDGEMENT: the 74's 1.36 m (the Bombay Castle's, Steel 1805 p. 141) raised for a "
    "broad ship (James vol. 1 pp. 29-30: Spain built her ships broader than any other nation's, "
    "for safety), to be tuned against the 74's heel (Con-D §2).",
    "clr_x_m": "6.3 m, a tuned figure and not her plan's (the lead's nudge 97): tuned with her rig "
    "whole against her helm and her tack (Con-D §9), in the 74's forms of truths 6 and 17. At her "
    "design's start, 5.7 m, the 74's lead over her length, her helm stood under the 74's: 0.13 "
    "deg of weather helm on the beam against the 74's 0.39, 1.46 of lee helm six points off "
    "against 0.97, and at 35 deg of rudder she stayed quicker than the 74. 6.3 m is the most "
    "weather helm that holds truth 17's form getting under way by a margin, as the 74's 4.8 was "
    "chosen; at 7.0 and over she is taken aback from rest. Her helm at 6.3: 0.53 deg of weather "
    "helm on the beam (the 74's 0.39), 0.70 of lee helm six points off (0.97). Measured, old "
    "beside new, in docs/dev/TuningNotes.md, 'Package 90, the Purísima Concepción'.",
    "lateral_area_m2": "About 473.5 m2 to K and the knee's fore edge, the rudder left out, by the "
    "drawn hulls' method, D29 (b), reckoned to her line as traced (the lead's rulings 2 and 5; "
    "Pages §5.6, §12.1: 475.2 m2 to the straight fit, measured, less the strip between the two "
    "lines aft, about 1.7 m2, computed); 455.3 m2 to the keel's lower edge and the stem's fore "
    "face, 488.5 m2 with the rudder.",
    "hull_speed_kn": "JUDGEMENT: the 74's 12.0 by the square root of the lengths, 13.1 on 61.26 m "
    "(Con-D §2), within the band her polar is held to (Con-D §9).",
    "deck_height_m": "5.99 m, ruled (the lead's nudge 33): her upper deck at the middle by the "
    "74's method, the mean of the pair of red lines PB-039 draws for it, above her line as traced "
    "(Pages §5.3); 6.06 m by her note's upper line beside it. The same deck as the 74's 3.16 m and "
    "the 64's 3.22 m by its place, the highest continuous deck, at the waist: the datum of every "
    "spar height and every sail's corners.",
    "rudder": "PB-039's rudder, its area and span accepted as measured (the lead's ruling 5; "
    "Pages §5.6, +-5%): 13.3 m2 below her line, a span of 8.29 m to its sole on K, 1.03 m broad "
    "at the line and 1.88 m at the heel; 3 deg/s the 74's (judgement). Its greatest angle, 25 "
    "deg, is a tuned figure and not her plan's (the lead's nudge 97): at the 74's 35 she stayed "
    "from truth 10's three headings in 210 to 223 s, quicker than the 74's 237 to 258, against "
    "her brief's 'no quicker than the 74's' (Con-D §9); at 25 she stays in 258 to 293, each "
    "slower than the 74's; at 22 she misses stays from 295 deg, and at 23 in 12 kn. Plainly: her "
    "tack is quicker than Luce's five to ten minutes, the engine's tack not slowing with a ship's "
    "size (Con-D §19; the carried fault 30), and is accepted as she is (the lead's nudge 97).",
}

# ---------------------------------------------------------------------------
# The ports' half-breadths, the side above the upper tier, the rail
# ---------------------------------------------------------------------------


def stern_x_at(z):
    """The stern's after edge at `z` above L0: the post's after face, raked, to the knuckle, then
    straight to the taffrail's top (JUDGEMENT above the knuckle)."""
    knuckle = knuckle_note()
    if z <= knuckle:
        return POST_X - math.tan(math.radians(POST_RAKE_DEG)) * z
    x0 = POST_X - math.tan(math.radians(POST_RAKE_DEG)) * knuckle
    return x0 + (TAFFRAIL[0] - x0) * (z - knuckle) / (TAFFRAIL[1] - knuckle)


def knuckle_note():
    """The counter's knuckle, z above L0: her lower deck at the stern and the 74's height over it
    (JUDGEMENT)."""
    return round(DECK_LINES["lower"][0][1] + KNUCKLE_ABOVE_LOWER_DECK_M, 2)


def upper_tier_at(x):
    """The upper tier's sill and half-breadth at `x`, straight between its ports."""
    pts = sorted(UPPER_PORTS)
    return interp([(px, s) for px, s, _hb in pts], x), interp([(px, h) for px, _s, h in pts], x)


def side_hb(x, z):
    """The side's half-breadth at `x` and `z` above L0 over her upper tier: the upper tier's,
    tumbled home (JUDGEMENT)."""
    sill, hb = upper_tier_at(x)
    return hb - TUMBLEHOME_PER_M * (z - sill)


def rail_note():
    """The top of the side, taffrail to the beakhead bulkhead, (x, z above L0): the taffrail's top
    (measured), the bulwark over the poop, the quarterdeck, the gangways and the forecastle
    (JUDGEMENT)."""
    poop = DECKS["roundhouse"]
    qd = DECKS["quarterdeck"]
    fc = DECKS["forecastle"]
    out = [TAFFRAIL]
    out += [(x, round(z + BULWARK_M, 2)) for x, z in poop]
    breast = round(POOP_BREAST_X + 0.1, 2)
    out.append((breast, round(interp(qd, breast) + BULWARK_M, 2)))
    out += [(x, round(z + BULWARK_M, 2)) for x, z in qd if x > breast]
    out += [
        (x, round(z + BULWARK_M, 2))
        for x, z in GANGWAY_AND_FORECASTLE
        if QUARTERDECK_BREAST_X < x < FORECASTLE_BREAST_X
    ]
    out += [(x, round(z + BULWARK_M, 2)) for x, z in fc]
    return out


def port_triples(drawn=None):
    """Her ports by deck, (x, sill z above L0, half-breadth), and the triples measured: the three
    gun decks' on PB-039 (Pages §5.2) but the sixteenth lower port; the upper works' places
    (ZAZ0100's, Pages §11.3) and their sills, and the sixteenth lower port's, JUDGEMENT, each such
    triple's half-breadth her drawn side's at its sill where `drawn` gives it ({(deck, x): hb}),
    else its first figure, which only seeds the drawing."""
    drawn = drawn or {}
    out = {
        "lower": sorted([*LOWER_PORTS, SIXTEENTH_LOWER]),
        "middle": list(MIDDLE_PORTS),
        "upper": list(UPPER_PORTS),
    }
    measured = [(w, x) for w, ports in out.items() for x, _s, _h in ports]
    measured.remove(("lower", SIXTEENTH_LOWER[0]))
    for word, xs in (("quarterdeck", QUARTERDECK_PORTS_X), ("forecastle", FORECASTLE_PORTS_X)):
        rows = []
        for x in xs:
            sill = interp(DECKS[word], x) - DECK_PAIR_HALF_M + SILL_ABOVE_DECK_M
            rows.append((x, round(sill, 2), round(side_hb(x, sill), 2)))
        out[word] = rows
    rail = rail_note()
    rows = []
    for x in POOP_PLACES_X:
        sill = interp(rail, x) - OVER_THE_RAIL_M
        rows.append((x, round(sill, 2), round(side_hb(x, sill), 2)))
    out["roundhouse"] = rows
    for word, rows in out.items():
        out[word] = [(x, s, drawn.get((word, x), hb)) for x, s, hb in rows]
    return out, measured


PORT_NOTES = {
    "lower": "Her lower deck's fifteen a side as built and rebuilt, 12.78 pies (3.56 m) apart, "
    "measured on PB-039 (Pages §5.2: x and sills +-0.02 m, the half-breadths the body plan's at "
    "the sill, +-0.05 m, +-0.15 at the end ports, read as moulded, JUDGEMENT); accepted as "
    "measured (the lead's ruling 5). And the sixteenth pair cut at Cádiz in 1791, unarmed in "
    "Spanish service (VR-Sp §4), the aftmost, under the upper tier's aftmost port, as ZAZ0100 "
    "draws every lower port under an upper one (Pages §11.3, read): its sill the tier's sheer "
    "carried aft (JUDGEMENT) and its half-breadth her drawn side's at it (the Diana's bow port's "
    "road, the lead's nudge 59), PB-039 not drawing it",
    "middle": "Her middle deck's sixteen a side, staggered between the lower and the upper, "
    "measured on PB-039 as the lower's (Pages §5.2); accepted as measured (ruling 5)",
    "upper": "Her upper deck's sixteen a side, over the lower ports and one more aft, measured on "
    "PB-039 as the lower's (Pages §5.2); accepted as measured (ruling 5)",
    "quarterdeck": "Six a side at the places ZAZ0100 draws on her sister's quarterdeck, x -18.8 "
    "to -7.3, 2.30 m apart (Pages §11.3: read at 1,280 px, about +-0.1 m); their sills the deck "
    "and 1 ft, the 74's (JUDGEMENT), and their half-breadths her drawn side's at the sill (the "
    "Diana's road): her upper works were not measured",
    "forecastle": "Three a side, for her fits' six and four forecastle guns, taken over the upper "
    "tier's three foremost ports, no sheet's forecastle ports having been made out (Pages §11.3; "
    "JUDGEMENT); their sills as the quarterdeck's, their half-breadths her drawn side's",
    "roundhouse": "The 1809 fit's three obús places a side on the poop at the three small ports "
    "ZAZ0100 draws there, x -25.4, -23.4 and -21.4 (Pages §11.3, read at 1,280 px), as gun places "
    "over the rail, 2 in under it, their sills not being read (the 74's convention; JUDGEMENT); "
    "their half-breadths her drawn side's",
}

# ---------------------------------------------------------------------------
# The file's hull block
# ---------------------------------------------------------------------------


class HerBuilder(g.Builder):
    """The generator's Builder, with the figures its shared helpers compute from her own keys
    kept out of her notes (the lead's notes of 2026-10-29, item 2): a spar's rating, a bowline's
    size and a staysail's sheet's, a staysail's area and sides; the 74's, word for word."""

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


def breadth_rows():
    """`breadth_m`'s rows, [x, half-breadth at her water, at the rail]: the body plan's half-breadth
    at L0 (measured), and at the top of the side the upper tier's tumbled home (JUDGEMENT)."""
    rail = rail_note()
    return [[x, hb, side_hb(x, interp(rail, x))] for x, hb in BREADTH_AT_L0]


def section_rows():
    """`sections_m`'s sourced points, station by station, (x, z, half-breadth) in the file's frame:
    at each lower port its sill and the upper port's over it (within 0.03 m in x); at each middle
    port its sill, with the lower and the upper tiers' sills and half-breadths at its x, straight
    between their ports either side (computed), or the water's where it lies beyond them; and the
    upper tier's aftmost with the water's under it. Each measured port's own triple a point, so
    that her drawn side stands on every measured port (Build-Ships.md §5.0 principle 8: the side
    drawn to the ports, never a port to the side)."""
    uppers = {round(x, 2): (s, h) for x, s, h in UPPER_PORTS}
    lowers = sorted(LOWER_PORTS)
    out = []
    for x, s, h in lowers:
        near = min(uppers, key=lambda u: abs(u - x))
        su, hu = uppers[near]
        out.append((x, [(fz(x, s), h), (fz(x, su), hu)]))
    x, su, hu = min(UPPER_PORTS)
    out.append((x, [(0.0, interp(BREADTH_AT_L0, x)), (fz(x, su), hu)]))
    for x, s, h in MIDDLE_PORTS:
        pts = [(fz(x, s), h)]
        for tier in (lowers, sorted(UPPER_PORTS)):
            if tier[0][0] <= x <= tier[-1][0]:
                ts = interp([(px, ps) for px, ps, _ph in tier], x)
                th = interp([(px, ph) for px, _ps, ph in tier], x)
                pts.append((fz(x, ts), th))
        if len(pts) < 2:
            pts.append((0.0, interp(BREADTH_AT_L0, x)))
        out.append((x, sorted(pts)))
    rows = []
    for x, pts in sorted(out):
        rows += [[x, z, hb] for z, hb in pts]
    return rows


def wale_rows(band, ports, at):
    """A band (z above L0, low and high) at `at` carried along the length parallel to a tier's sills
    (`ports`, (x, sill, hb)), at `WALE_XS`, in the file's frame (JUDGEMENT)."""
    sills = sorted((x, s) for x, s, _h in ports)
    s0 = interp(sills, at)
    lo0, hi0 = band
    out = []
    for x in WALE_XS:
        d = interp(sills, x) - s0
        out.append([x, fz(x, lo0 + d), fz(x, hi0 + d)])
    return out


def channel_wale_band():
    """The channel wale's band at the middle, between the middle tier's port tops and the upper
    tier's sills, set in the gap as the 74's is (JUDGEMENT)."""
    middle = sorted((x, s) for x, s, _h in MIDDLE_PORTS)
    top = interp(middle, 0.0) + PORT_SIZE_M["middle"][1]
    sill, _hb = upper_tier_at(0.0)
    gap = sill - top
    return top + CHANNEL_WALE_SHARE[0] * gap, sill - CHANNEL_WALE_SHARE[1] * gap


def stem_points():
    """Her stem's fore face, low to high, in the file's frame: PB-039's to the lower deck, then on
    the 74's rake to her stem head (JUDGEMENT above the lower deck)."""
    head = stem_head_note()
    return [fp(x, z) for x, z in STEM] + [fp(*head)]


def stem_head_note():
    """Her stem head, (x, z above L0): her upper deck carried to the stem and the 74's height over
    it, on the 74's rake from the lower deck (JUDGEMENT)."""
    up = DECKS["upper"]
    z = _sloped(up, STEM_X) + STEM_HEAD_ABOVE_UPPER_M
    x = STEM[-1][0] + STEM_RAKE * (z - STEM[-1][1])
    return (round(x, 2), round(z, 2))


def head_points():
    """The knee of the head, low to high, in the file's frame: PB-039's to her line, the 74's knee
    above it (JUDGEMENT)."""
    rail_end = rail_note()[-1][1]
    top = rail_end + SEVENTY_FOURS_KNEE_TOP_OVER_RAIL_FT * FT * RIG_SCALE
    z_scale = top / (SEVENTY_FOURS_KNEE_FT[-1][0] * FT)
    x_scale = HULL["length_waterline_m"] / SEVENTY_FOURS_LENGTH_M
    x0 = HEAD[-1][0]
    above = [(x0 + dx * FT * x_scale, z * FT * z_scale) for z, dx in SEVENTY_FOURS_KNEE_FT]
    return [fp(x, z) for x, z in HEAD] + [fp(round(x, 2), round(z, 2)) for x, z in above]


def stern_points():
    """The post's after face from K, the knuckle, and the taffrail's top, in the file's frame."""
    k_x = POST_X - math.tan(math.radians(POST_RAKE_DEG)) * K_LINE[0][1]
    knuckle = knuckle_note()
    return [
        fp(round(k_x, 2), straight(K_LINE, k_x)),
        fp(POST_X, 0.0),
        fp(round(stern_x_at(knuckle), 2), knuckle),
        fp(*TAFFRAIL),
    ]


def transom_hb_at(z_file):
    """The transom's half-breadth at a height of the file's frame, straight between the knuckle
    and the taffrail's side (JUDGEMENT)."""
    half = 0.5 * HULL["beam_m"]
    lo = (fz(stern_x_at(knuckle_note()), knuckle_note()), TRANSOM_HB_SHARE[1] * half)
    hi = (fz(TAFFRAIL[0], TAFFRAIL[1]), TRANSOM_HB_SHARE[0] * half)
    return interp([lo, hi], z_file)


def check_hull(hull, triples):
    """Con-D §2's and §10's figures held before any file is written: her draught to K at the middle
    of her line as traced 7.94 m; her datum her upper deck there by the 74's method within a
    centimetre; her midship lower port dipping at 13.0 to 13.5 deg; her mass inside the ruled
    range, 4,421 to 4,473 t."""
    draught = water(0.0) - straight(K_LINE, 0.0)
    if abs(draught - hull["draught_m"]) > 0.005:
        raise ValueError(
            f"her line as traced stands {draught:.3f} m over K at the middle, not her "
            f"draught's {hull['draught_m']} (the lead's ruling 1)."
        )
    deck = deck_m("upper", 0.0)
    if abs(deck - DATUM) > 0.01:
        raise ValueError(
            f"her upper deck stands {deck:.3f} m above her water at the middle, not within a "
            f"centimetre of the ruled {DATUM} (nudge 33)."
        )
    x, sill, hb = next(t for t in triples["lower"] if t[0] == MIDSHIP_LOWER_X)
    dip = math.degrees(math.atan2(fz(x, sill), hb))
    if not 13.0 <= dip <= 13.5:
        raise ValueError(f"her midship lower port dips at {dip:.2f} deg, not 13.0 to 13.5.")
    t = hull["displacement_kg"] / 1000.0
    if not RULED_T[0] <= t <= RULED_T[1]:
        raise ValueError(f"her displacement, {t:.0f} t, is outside the ruled 4,421 to 4,473 t.")
    REPORT["dip"] = dip
    REPORT["deck"] = deck
    REPORT["draught"] = draught


def hull_block():
    """Her hull dict with its profile as the last key (Build-Ships.md §5.1), and its notes: drawn
    once with her judged triples' first figures, then again with each one's half-breadth her drawn
    side's at its sill, no judged port shaping a line of hers (`port_triples`)."""
    _hull_block({})
    triples, measured = REPORT["triples"], set(REPORT["measured"])
    drawn = {
        (word, x): round(hb + REPORT["gaps"][(word, x)], 2)
        for word, rows in triples.items()
        for x, _s, hb in rows
        if (word, x) not in measured
    }
    REPORT["drawn_hb"] = drawn
    return _hull_block(drawn)


def _hull_block(judged_hb):
    """Her hull and its notes, her judged triples' half-breadths `judged_hb` ({(deck, x): hb})."""
    hull = dict(HULL)
    hull["deck_height_m"] = DATUM
    rudder = hull.pop("rudder")
    hull["rudder"] = rudder
    notes = dict(HULL_NOTES)
    triples, measured = port_triples(judged_hb)
    rail = [fp(x, z) for x, z in rail_note()]
    breadth = [[x, hw, hr] for x, hw, hr in breadth_rows()]
    # K straight in the note's frame, filed at her line's knots too: above a bent water it bends
    keel_xs = sorted(
        {K_LINE[0][0], *(x for x, _k in TRACED_TO_K if x < K_LINE[1][0]), K_LINE[1][0]}
    )
    keel = [fp(x, straight(K_LINE, x)) for x in keel_xs]
    lower_sills = triples["lower"]
    wales = wale_rows(MAIN_WALE_AT[1:], LOWER_PORTS, MAIN_WALE_AT[0])
    channel = wale_rows(channel_wale_band(), UPPER_PORTS, 0.0)
    section = [[fz(MIDSHIP_X, z), hb] for z, hb in SECTION]
    decks = {word: [fp(x, z - DECK_PAIR_HALF_M) for x, z in pts] for word, pts in DECKS.items()}
    ports = {word: [fp(x, s) + [hb] for x, s, hb in t] for word, t in triples.items()}
    sizes = {word: list(PORT_SIZE_M[word]) for word in ports}
    hull["profile"] = g.hull_profile(
        rail,
        breadth,
        keel=keel,
        stem=stem_points(),
        stern=stern_points(),
        wales=wales,
        section=section,
        decks=decks,
        ports=ports,
        port_size=sizes,
        head=head_points(),
        sections=section_rows(),
        channel_wales=channel,
    )
    notes.update(PROFILE_NOTES)
    for word, text in PORT_NOTES.items():
        notes[f"profile.ports_m.{word}"] = text + "."
    knuckle = fz(stern_x_at(knuckle_note()), knuckle_note())
    form = {
        "fullness": [1.0, 1.0],
        "stern": {
            "type": "square",
            "knuckle_z_m": knuckle,
            "transom_hb_m": [
                TRANSOM_HB_SHARE[0] * 0.5 * HULL["beam_m"],
                TRANSOM_HB_SHARE[1] * 0.5 * HULL["beam_m"],
            ],
            "round_up_m": ROUND_UP_M,
            "galleries_m": [
                [aft, fore, fz(aft, low), fz(aft, high)] for aft, fore, low, high in GALLERIES
            ],
            "lights_m": [
                [
                    fz(aft, low),
                    fz(aft, high),
                    LIGHTS_A_BAND,
                    LIGHTS_SPREAD * transom_hb_at(fz(aft, 0.5 * (low + high))),
                ]
                for aft, _fore, low, high in GALLERIES
            ],
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
    REPORT["lower_sills"] = lower_sills
    check_hull(hull, triples)
    return hull, notes


# Each line's rung (Build-Ships.md §5.0 principles 3 and 4), its weakest point named.
MARKS = {
    "rail_m": "judged",  # her upper works' bulwark over their decks
    "breadth_m": "judged",  # the half-breadths at the rail; the water's L0's aft of x -8
    "keel_m": "sourced",
    "stem_m": "judged",  # behind the head, from the lower deck to the stem head
    "stern_m": "judged",  # the knuckle and the stern's after edge to the taffrail
    "wales_m": "judged",  # along the length
    "section_m": "sourced",
    "decks_m": "judged",  # the upper works' extents
    "ports_m": "judged",  # the upper works' places, and the sixteenth lower port
    "port_size_m": "judged",  # the upper works'
    "head_m": "judged",  # above her line
    "sections_m": "judged",  # the water's points beyond the tiers, L0's half-breadths
    "channel_wales_m": "judged",  # its band and its run
    "form.fullness": "judged",
    "form.stern": "judged",
    "form.stern.knuckle_z_m": "judged",
    "form.stern.transom_hb_m": "judged",
    "form.stern.round_up_m": "judged",
    "form.stern.galleries_m": "judged",  # the upper two tiers' spans
    "form.stern.lights_m": "judged",  # the count and the spread
    "form.head": "sourced",
}

PROFILE_NOTES = {
    "profile": "Her side, decks and ports (Con-D §3; Build-Ships.md §5.1): x forward of the middle "
    "of her line between the post's after face and the stem's fore face, z above her water, the "
    "line as traced (the lead's ruling 1), at each point's own station, metres; PB-039's lines as "
    "drawn, measured at the library's full size (Pages: 39.75 px a pie, 0.70 cm a pixel), but "
    "where a line's note says judgement.",
    "profile.rail_m": "The top of the side from the taffrail's top, 11.84 m over L0 at x -33.23 "
    "(Pages §5.5, measured), over the poop, the quarterdeck, the gangways and the forecastle to "
    "the beakhead bulkhead: 1.0 m over each deck's line (JUDGEMENT, the 74's quarterdeck rail over "
    "its deck), her upper works not being measured on PB-039.",
    "profile.breadth_m": "By station, aft 9 to fore 7: the half-breadth at her line, PB-039's body "
    "plan at L0 (Pages §6, measured, as drawn: JUDGEMENT on moulded or outside the plank, Pages "
    "§4.5); aft of about x -8 m her water lies up to 0.14 m under L0 and the after sections were "
    "not read again at that height (Pages §12.1: to do), so the water's half-breadth there is L0's "
    "(JUDGEMENT). At the top of the side the upper tier's half-breadth tumbled home as her midship "
    "section (JUDGEMENT).",
    "profile.keel_m": "K, the lowest keel line (a false keel's lower edge, judgement), from the "
    "post's after face to the knee's foot (Pages §4.2, §6, measured), straight in her plan's frame "
    "and filed at her line's knots (x -5 and 0) as well, so that it stands her draught under her "
    "water at each.",
    "profile.stem_m": "The stem's fore face from the forefoot through her line, plumb to the lower "
    "deck (Pages §5.1, §6, measured), then on the 74's rake to her stem head, 1.23 m over her "
    "upper deck carried to the stem (the 74's 3.5 ft x 1.15: JUDGEMENT, not measured).",
    "profile.stern_m": "The post's after face raked 1.5 deg (Pages §5.1, measured) from K to the "
    "counter's knuckle, taken 0.82 m over her lower deck at the stern (the 74's 2.3 ft x 1.15: "
    "JUDGEMENT), and the stern's after edge straight from there to the taffrail's top (measured, "
    "Pages §5.5; straight between, JUDGEMENT).",
    "profile.wales_m": "The main wale: amidships from 0.17 to 1.09 m over L0 (Pages §5.4, "
    "measured at x +1.4), carried along the length parallel to the lower tier's sills (JUDGEMENT, "
    "the 74's rule: not traced along the length). The middle wales between her lower and middle "
    "tiers have no key of the file.",
    "profile.section_m": "The midship section, station m aft at x +0.99, from the keel to 7 m "
    "over L0, as drawn (Pages §6, measured; moulded, JUDGEMENT): the floor nearly flat for 4 m "
    "out, the turn of the bilge sharp, the greatest half-breadth 8.18 m at 0.54 m over L0.",
    "profile.decks_m": "Each deck at the middle line by the 74's method, the mean of the pair of "
    "red lines PB-039 draws for it, 0.055 m under the upper line Pages reads (Pages §5.3, "
    "measured; the lead's ruling 4 and nudge 33), over PB-039's stations; carried beyond them "
    "(JUDGEMENT): the upper deck forward of +18.92 by the middle deck's rise, the poop to its "
    "breast at -20.5, the quarterdeck to its breast at -6.5 on the gangway line, the forecastle "
    "from +13.0 to the beakhead bulkhead at +27.9, each end on its slope. The orlop's red line, "
    "0.90 m under L0 at the middle, has no deck word of the file.",
    "profile.port_size_m": "Width by depth: the lower 1.01 x 0.93 m, the middle 0.91 x 0.76, the "
    "upper 0.80 x 0.67 (Pages §5.2, measured, +-1 cm; ruling 5); the quarterdeck's, the "
    "forecastle's and the poop's the 74's quarterdeck's, 2 ft 7 in by 2 ft 4 in (Con-D §3.4, "
    "JUDGEMENT), the poop's places being over the rail.",
    "profile.head_m": "The knee of the head's fore edge from K to her line, 31.54 m forward at L0 "
    "(Pages §5.1, §6, measured); above it the 74's knee (ZAZ1357, Bel-D §3.2) scaled by the "
    "lengths and by the height of her rail's fore end, its top over it (JUDGEMENT: PB-039's head "
    "and figure read, not measured).",
    "profile.sections_m": "Her ports' own triples as sourced points of her side: at each lower "
    "port its sill and the upper port's over it, at each middle port its sill (Pages §5.2, "
    "measured), with the lower and upper tiers' points at its x straight between their ports "
    "(computed), or the water's beyond them, and the upper tier's aftmost with the water's under "
    "it; so that the drawn side stands on every measured port (Build-Ships.md §5.0 principle 8). "
    "Judged at its weakest: the water's half-breadths there L0's (as breadth_m's).",
    "profile.channel_wales_m": "The channel wales between her middle and upper tiers, set in the "
    "gap at the middle as the 74's channel wale stands in hers (Bel §3.3) and carried parallel to "
    "the upper sills (JUDGEMENT: not measured).",
    "profile.form.fullness": "The default rule, [1, 1] (JUDGEMENT).",
    "profile.form.stern": "Square. Two closed quarter galleries and a third tier of lights over "
    "them on PB-039's quarter (Pages §5.5: the lights at 4.80-5.92, 7.39-7.95 and 9.39-9.92 m "
    "over L0, the lowest gallery from x -32.1 to -28.2: measured, accepted, ruling 5), the upper "
    "two's spans the lowest's (JUDGEMENT). Her stern board (ZAZ0101's) not read, so the knuckle, "
    "the transom's half-breadths (the 74's share of her half-beam), its round-up (the 74's x "
    "1.15) and the lights' count (eight a band, the 74's) and spread are JUDGEMENT.",
    "profile.form.head": "A beakhead with its rails and a figure (PB-039, read: Res §2.4); carving "
    "and paint stay in words.",
    "profile.marks": "Each line's rung (Build-Ships.md §5.0 principles 3 and 4): sourced, measured "
    "on her own plan, PB-039 (rung S, her own lines: the owner's choice of 2026-11-20); judged, a "
    "judgement at its weakest point, which the line's note names.",
}

# The decks over their extents (set at import from PB-039's red lines and the judged extents).
DECKS = {}
DECKS.update(deck_extents())


# ---------------------------------------------------------------------------
# Her decks and rail in the rig's frame (feet forward of her post, feet above her water)
# ---------------------------------------------------------------------------


def deck_ft(word, x_ft):
    """A deck's surface at `x_ft`, feet above her water."""
    return deck_m(word, x_m(x_ft)) / FT


def poop_middle_ft(x_ft):
    """Her poop at the middle line at `x_ft`, feet above her water."""
    return deck_ft("roundhouse", x_ft)


def _in(word, x):
    pts = DECKS[word]
    return pts[0][0] <= x <= pts[-1][0]


def deck_worked_ft(x_ft):
    """The deck she is worked from at `x_ft`, feet above her water: the poop over its extent, else
    the quarterdeck's or the forecastle's over theirs, else the upper deck (the waist)."""
    x = x_m(x_ft)
    for word in ("roundhouse", "quarterdeck", "forecastle"):
        if _in(word, x):
            return deck_ft(word, x_ft)
    return deck_ft("upper", x_ft)


POOP_MIDDLE_LINE_FT = [(ft_x(x), deck_m("roundhouse", x) / FT) for x, _z in DECKS["roundhouse"]]
QUARTERDECK_LINE_FT = [(ft_x(x), deck_m("quarterdeck", x) / FT) for x, _z in DECKS["quarterdeck"]]
RAIL_FT = [(ft_x(x), fz(x, z) / FT) for x, z in rail_note()]
_HEAD = stem_head_note()
STEM_HEAD_FT = (ft_x(_HEAD[0]), fz(*_HEAD) / FT)
BOWSPRIT_HEEL_FT = STEM_HEAD_FT[0] - BOWSPRIT_HEEL_ABAFT_HEAD_FT


def fore_channel_ft():
    """Her fore channel's height, feet above her water: the upper tier's port tops at the fore mast
    and the 74's 2.6 ft over them x 1.15 (JUDGEMENT)."""
    x = x_m(MASTS["fore"][0])
    sill, _hb = upper_tier_at(x)
    top = fz(x, sill + PORT_SIZE_M["upper"][1])
    return top / FT + FORE_CHANNEL_OVER_PORT_TOPS_FT


# ---------------------------------------------------------------------------
# The rig's geometry (the 74's rules: Bel-D §4.1, §4.2)
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
    """Each mast's geometry in feet above her datum, keyed as the 74's: the lower masthead
    (`above`) from the heel on its step and its length; the yards' heights by the frigate's rules
    (the lower yards 2 ft under the hounds, the topsail yards at the topmast's hounds, the
    topgallants under the stop, the royals a foot under the long pole's head), the 74's."""
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
    frigate's rope, scaled with hers (judgement, the 74's)."""
    rope = g.FRIGATE_ROPE["course"]["lift"] * g.FRIGATE_MAST_ROPE_FACTOR["mizzen"]
    return g.quarter(rope * rope_scale)


def under_the_run(line, aft_x, fore_x, room):
    """The points of `line` (a deck, (ft forward of her post, ft above her water)) under a run from
    `aft_x` to `fore_x` (metres, the file's x), each (x, z above her water, room), the line's
    height at both ends of the run among them (the 74's)."""
    pts = [(x_m(xf), z_m(z)) for xf, z in line]
    lo, hi = pts[0][0], pts[-1][0]
    out = [(x, z, room) for x, z in pts if aft_x <= x <= fore_x]
    for x in (aft_x, fore_x):
        if lo <= x <= hi:
            out.append((x, z_m(interp(line, ft_x(x))), room))
    return out


# ---------------------------------------------------------------------------
# The mizen course (Con-D §4.2; the 74's, Bel-D §4.5)
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
    """What the course's level foot stands over her poop's and her quarterdeck's middle lines, at
    the least, over its run."""
    tack, _throat, _peak, clew = crs["corners"]
    under = under_the_run(POOP_MIDDLE_LINE_FT, clew[0], tack[0], 0.0)
    under += under_the_run(QUARTERDECK_LINE_FT, clew[0], tack[0], 0.0)
    return min(tack[1] - z for _x, z, _r in under)


def mizen_course_cut(mast_x_m, rake_deg):
    """Her mizen course cut at the mast (`mizen_yard.course`; Ext §3.4) from Steel's table IV, the
    74 x 1.15: its tack `MIZEN_TACK_ABOVE_DECK_FT` above the deck her mizen stands through, her
    quarterdeck (her poop ends abaft it), to the centimetre above; (x, z above her water) in
    metres, with its area and centre. Raises `ValueError` where the foot would not then clear her
    poop and her quarterdeck (the 74's clew check). Steel's words (6 ft 6 in above the deck the
    mast stands through) and the 74's 9 ft unscaled are cut beside it for the report."""
    x_ft = MASTS["mizzen"][0]
    deck = z_m(deck_ft("quarterdeck", x_ft))
    tack_z = math.ceil((deck + MIZEN_TACK_ABOVE_DECK_FT * FT) * 100.0 - 1e-9) / 100.0
    crs = course_on(tack_z, mast_x_m, rake_deg)
    clear = foot_clear(crs)
    if clear <= 0.0:
        raise ValueError(
            f"her mizen course's foot stands {clear:.2f} m over her poop's middle line: its clew "
            "must clear it (the 74's clew check, Bel-D §1.5)."
        )
    others = {}
    for words, z in (
        ("9 ft above the quarterdeck (the 74's, unscaled)", deck + 9.0 * FT),
        (
            "6 ft 6 in above the quarterdeck (Steel's words from the deck the mast stands through)",
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
        "cut": crs,
        "clear": clear,
        "others": others,
    }


def mizen_course(b, mz, rope_scale):
    """Her mizen course on her mizen yard (Con-D §4.2; Ext §3.4): the lateen cut at the mast on the
    whole yard, a `lateen_yard` slung at its truss with its fore part bare, and the lines of Ext
    §3.4 (`mizen_yard.COURSE_LINES`), the 74's. Returns the course's id."""
    if MIZEN_COURSE != "gated":
        raise ValueError(f"MIZEN_COURSE is {MIZEN_COURSE!r}: she has only 'gated'.")
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
        note=f"the mizen yard, {fmt_ft(SPARS_FT['mizen_yard'])}, the 74's 86 ft 6 in (Dragon's: "
        "Lavery 1985 p. 19, Table 10) x 1.15 (Con-D §4.2, JUDGEMENT), a lateen yard slung at its "
        "truss with its lifts and derrick, its fore part bare (Ext §3.4): height_m its truss, the "
        "course's throat. Not braced: vangs in place of braces and bowlines at its heel, its sail "
        "trimmed by the sheet (Ext §3.3). Plainly: whether a Spanish three-decker carried a "
        "lateen yard or a gaff in 1797 and 1809 was not found (Con-D §4.2).",
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
        note="mizen course, a lateen cut at the mast (Ext §3.4), the 74's four-sided loose-footed "
        "sail on the gaff's curve and trim in the physics (Ext §3.1): Steel's table IV, the 74 (16 "
        "cloths at the head, 17 at the foot, its fore leech 11 yards and its after leech 21), each "
        "x 1.15 (Con-D §4.2, JUDGEMENT), 22 1/2 in a cloth, its luff laced to the mast, its head "
        "along the yard to the peak, its foot level and loose (tools/ships/mizen_yard.py); corners "
        "[tack, throat, peak, clew]. Its tack the 74's 9 ft x 1.15 above her quarterdeck at the "
        "mast, the deck her mizen stands through, her poop ending abaft it (JUDGEMENT; the 74's "
        "rule, Bel-D §4.5). One reef band a fifth up its mast leech (Steel)."
        + g.canvas_note(canvas),
    )
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
        "yard.jeers": "the mizen yard's jeers at its truss (Ext §3.4); the 74's, the frigate's "
        "spanker throat halyard's size and purchase scaled by her rope (judgement).",
        "yard.derrick": "the derrick between the slings and the peak (Ext §3.4), the 74's 64's 4 "
        "in in double blocks scaled by her rope against the 64's (judgement).",
        "yard.vang": "the vang pendants, the 64's 4 in scaled by her rope against the 64's "
        "(judgement, the 74's), one line a side with its falls.",
        "yard.lift": "the mizen yard's lifts, as the crossjack's (judgement, the 74's): every "
        "yard's lifts are carried (the owner's answer, Build-Ships.md §19.1 item 7).",
        "yard.bowline": "the bowlines at the yard's heel, filed as guys of the yard, a bowline "
        "being a sail's line in the engine (Ext §3.4); the 64's 3 in scaled by her rope against "
        "the 64's (judgement, the 74's).",
        "course.sheet": "the course's one sheet, to the taffrail (Ext §3.4); the frigate's spanker "
        "sheet's size and purchase scaled by her rope (judgement, the 74's).",
        "course.tack": "the course's tack, forward of the mast (Ext §3.4); the frigate's spanker "
        "outhaul's size scaled by her rope (judgement, the 74's).",
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


# ---------------------------------------------------------------------------
# The head (the 74's, Bel-D §4.7)
# ---------------------------------------------------------------------------


def triangle_on_stay(low, high, foot, leech):
    """A triangular staysail on its stay as the 74's headsails are cut from Steel's table IV: its
    tack at `low` on the stay, its luff up the stay toward `high`, its foot and leech, metres,
    square to each other at the clew, the clew below and abaft the stay; cut to the stay where its
    luff is longer, Steel's proportions kept (the spars rule: Build-Ships.md §19.1 item 5). Returns
    the corners [tack, peak, clew], the foot and the leech as cut, and the share of Steel's sides
    kept."""
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
    """The bowsprit, the jib-boom and the headsails' triangles, metres above her water, the 74's
    rules: the bowsprit's root on her stem head, steeved `BOWSPRIT_STEEVE_DEG`, its outboard part
    its length less its part inboard of the stem head from its heel; the jib-boom along it; the
    fore stay to a collar half way out the bowsprit's outboard part, the fore topmast stay to its
    end and the jib's stay to the jib-boom's; each headsail a triangle on its stay."""
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
    """The bowsprit, the jib-boom, their stays and the headsails (the 74's). Returns the
    headsails' ids, the fore staysail first."""
    loads = {sid: (h["area"], h["centre"], "jibheaded") for sid, h in head["sails"].items()}
    bowsprit = b.spar(
        "bowsprit",
        "bowsprit",
        x_m=round(head["root"][0], 2),
        length_m=g.ft(head["outboard"]),
        height_m=round(head["tip"][1] - DATUM, 1),
        rating_kn=g.design_kn(list(loads.values()), g.DESIGN_WIND_KN["lower"]),
        note=f"bowsprit {fmt_ft(SPARS_FT['bowsprit'])}, the 74's 66 ft (Dragon's: Lavery 1985 p. "
        "19, Table 10) x 1.15 (Con-D §4.2, JUDGEMENT), steeved as the 74's, "
        f"{BOWSPRIT_STEEVE_DEG:g} deg (ZAZ1357, task 7: JUDGEMENT for hers, PB-039's bowsprit "
        "not being measured), rooted on her stem head: x_m its root, length_m its part outboard of "
        "the stem head from its heel, the 74's 14 ft 9 in abaft her stem head x 1.15 (JUDGEMENT), "
        "height_m its end above the datum. The spritsail yard slung under it and the sprit-topsail "
        "yard under the jib-boom (D8 (b); Ext §4.1; tools/ships/spritsail_yards.py).",
    )
    jib_boom = b.spar(
        "jib_boom",
        "jib_boom",
        on=bowsprit,
        length_m=g.ft(head["jib_out"]),
        height_m=round(head["jib_tip"][1] - DATUM, 1),
        rating_kn=g.design_kn([loads["jib"]], g.DESIGN_WIND_KN["jib_boom"]),
        note=f"jib-boom {fmt_ft(SPARS_FT['jib_boom'])}, the 74's 48 ft x 1.15 (JUDGEMENT), 7/12 "
        "of it outboard along the bowsprit's steeve (Luce, the frigate's rule; the 74's).",
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
            "from the fore topmast head to the jib-boom's end: the jib sets on it",
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
            "74, its cloths in the foot and yards in the leech x 1.15: Con-D §4.2, JUDGEMENT): its "
            "tack at its stay's foot, its luff up the stay, foot and leech square at the clew "
            "(judgement on Steel's figures, the 74's)"
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
    """The yards under the bowsprit (D8 (b); Ext §4.1; `spritsail_yards.cut`), the 74's x 1.15, on
    the line her bowsprit and jib-boom have; their lines `square_sail_lines` at her fore topsail's
    and fore topgallant's sizes, and the guys; no halyard to the spritsail yard, which hangs in
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
        "the fore stay (Steel 1794 vol. I pp. 196-197; the 74's); kept out of the file's yard "
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
            note=f"the {yard_id.split('.')[0].replace('_', ' ')} yard's guys (Lavery 1985 I28, the "
            "74's), the braces' size (judgement).",
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
            f"spritsail yard {fmt_ft(SPRITSAIL['yard_m'] / FT)}, the 74's 61 ft 6 in (Lavery 1985 "
            "Table 10) x 1.15 (JUDGEMENT), slung under the bowsprit near the cap (Steel 1794 vol. "
            f"I pp. 196-197), {SPRITSAIL_STATION:g} of the way out its outboard part and "
            f"{SPRITSAIL_HANG_M:g} m under its line (the 74's, x 1.15: judgement); no halyard, it "
            "hanging in slings (Ext §4.1);",
            "spritsail (the sprit course): Steel's table IV, the 74 (29 cloths, 8 yards deep), x "
            "1.15 (Con-D §4.2, JUDGEMENT), 22 1/2 in a cloth, hanging from its yard, square, its "
            "foot clear of the water at no heel (tools/ships/spritsail_yards.py). Two diagonal "
            "reef bands in Steel, filed and reefed as a square sail's (Ext §4.1). Out of plain "
            "sail, so the polar never sets it (Ext §4.1).",
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
            f"sprit-topsail yard {fmt_ft(SPRIT_TOPSAIL['yard_m'] / FT)}, the 74's 40 ft 0 in "
            "(Lavery 1985 Table 10) x 1.15 (JUDGEMENT), hung under the jib-boom by its parral "
            "(Steel p. 197), where its sail's depth from the spritsail yard is Steel's (the 74's "
            f"rule); {SPRIT_TOPSAIL_HANG_M:g} m under its line (judgement); its halyard stands for "
            "the traveller's outhauler (Falconer 1780, SPRITSAIL-TOPSAIL);",
            "sprit topsail: Steel's table IV, the 74 (18 1/2 cloths at the head, 29 1/2 at the "
            "foot, 10 yards deep), x 1.15 (Con-D §4.2, JUDGEMENT), 22 1/2 in a cloth, its head on "
            "its yard and its foot spread on the spritsail yard's arms (Steel, SPRITSAIL TOPSAIL; "
            "tools/ships/spritsail_yards.py). No reef band (Lever 1808). Out of plain sail (Ext "
            "§4.1).",
        ),
    ]


# ---------------------------------------------------------------------------
# The staysails between the masts (the 74's, Bel-D §4.4)
# ---------------------------------------------------------------------------


def steels_staysail_words(sid, area):
    """The words a staysail between the masts adds to its note: Steel's table IV figure for the 74
    x 1.32 and the band the 74's design holds it in, raised before any file is written if the cut
    falls outside it."""
    row, _figures, steel, band = STEEL_BETWEEN[sid]
    gap = area / steel - 1.0
    if abs(gap) > band:
        raise ValueError(
            f"her {sid} is cut to {area} m2, {gap:+.0%} of Steel's {steel:.0f} for a 74 x 1.32, "
            f"outside the 74's ±{band:.0%} (Bel-D §4.4)."
        )
    return (
        f" Steel's table IV, the 74 ({row}), x 1.15 a side: about {steel:.0f} m2, the cut within "
        f"the 74's ±{band:.0%} (Bel-D §4.4)."
    )


def between_the_masts(b, geom, mast_x, rake):
    """The staysails between the masts, the 74's pattern on her figures: the main staysail a
    triangle on its own stay; the main topmast staysail by Steel's rules on her spars; the
    middle, the main topgallant, the mizen and the mizen topmast staysails cut to Steel's table
    IV x 1.15; no mizen topgallant staysail. Every height above her datum. Returns the sails, the
    main mast's first."""
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
            "Steel's table IV, the 74, x 1.15 (Con-D §4.2, JUDGEMENT), as the owner chose for the "
            f"64 (2026-10-29): the table's after leech and foot ({cloths:g} cloths of 22 1/2 in, "
            "the head's and the foot's halved, as Steel's rule for the canvas squares them), the "
            f"bunt as the stay leaves it (the table's {bunt:.1f} m); {where}"
            + g.canvas_note(canvas[sid])
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
        "1794 vol. I, 'The main-staysail'); 9 in, judgement (the 74's).",
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
        "main staysail, a triangle, cut to Steel's table IV, the 74, x 1.15 (Con-D §4.2, "
        f"JUDGEMENT): {foot_cl:g} cloths of 22 1/2 in in the foot and {leech_yd:g} yards in the "
        "leech, square at the clew, its luff up the stay from its tack, as her headsails are cut "
        "(judgement on Steel's figures, the 74's); its tack at the stay a fifth of the main mast's "
        "height above the deck (judgement, the 74's), its peak before the main top; corners [tack, "
        "peak, clew]. 'This sail is seldom used in large vessels' (Steel)."
        + g.canvas_note(canvas[sid])
    )
    out.append(sid)
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
        "topmast's hoist above the fore cap (judgement, the 74's); size judgement.",
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
        "(judgement, the 74's), the staysail on the span above it.",
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
# The studding sails, the storm canvas and the occasional sails (the 74's, Bel-D §4.4, §4.8)
# ---------------------------------------------------------------------------


def studding_sails(b, geom, mast_x, rake, rope_scale):
    """The studding sails, the 74's set on Steel's figures for a 74 x 1.15: the fore lower and the
    fore and main topmast and topgallant, a pair each, on booms by Steel's p. 40 rules on her
    yards; the topgallant studding sails as deep as the topgallants they spread. The lower boom at
    her fore channel, the topmast booms on the lower yard, the topgallant booms on the topsail
    yard. Returns the sails' ids."""
    channel_m = round(z_m(fore_channel_ft()) - DATUM, 1)
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
            "lower": "five-ninths of the main yard), goose-necked at her fore channel (Luce 1884 "
            "p. 137), over her upper tier (JUDGEMENT on its height)",
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
                    f"{name} {level} studding sail: Steel's table IV, the 74, x 1.15 (Con-D §4.2, "
                    f"JUDGEMENT), {head_cl:g} cloths at the head and {foot_cl:g} at the foot, "
                    f"{how}; its head on its yard at the yardarm of the sail it spreads."
                    + g.canvas_note(canvas)
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
    """The storm canvas, the 74's pattern on her figures, every sail in the sail room: the fore
    storm staysail on the fore stay, the mizzen storm staysail on the mizen stay, the storm mizzen
    on its own stay abaft the mizen mast, bent in place of the mizen course. Each fixed height
    taken above the deck she works it from (`deck_worked_ft`). Returns the sails' ids, the storm
    staysails first."""
    storm = g.FRIGATE_CANVAS["storm"]

    def deck_at(x):
        return z_m(deck_worked_ft(ft_x(x)))

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
        "Steel's fore staysail cut as her working one is (table IV, the 74, x 1.15), of storm "
        "canvas, on the fore stay (Luce 1884 ch. X: 'The storm-staysails set on the respective "
        "lower-stays'); corners [tack, peak, clew]",
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
        "on the mizen stay (Luce 1884 ch. X): its tack at the stay's collar on the main mast, the "
        "74's 12 ft x 1.15 above the deck (Steel, 'Mizen-stay'), its head 0.6 of the way up the "
        "stay, its clew under the head the 74's 7 ft x 1.15 above the deck she works it from there "
        "(the 74's and the frigate-36's, judgement); corners [tack, peak, clew]",
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
        "1884 ch. X); the jib stay's, scaled by her rope (judgement, the 74's).",
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
        "the 74's 4 ft x 1.15 above the deck at the mast, or at her rail over the foot's run "
        "where that stands higher (judgement, the 74's), 0.8 of the stay's run to the hounds; its "
        "foot towards the taffrail, 0.45 of Steel's driver boom, the main topsail yard's length "
        "(p. 40), which she does not carry (the 74's rule kept, judgement); bent in place of the "
        "mizen course; corners [tack, peak, clew]",
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
    """A save-all under each fore lower studding-sail boom, the 74's pattern (Luce 1884 ch. XXIII;
    Steel 1794 vol. I: 'Some ships have a water-sail'): its head along 0.6 of the boom, down from
    the boom at her fore channel to half a metre off the water (judgement); in the sail room. No
    ringtail: no source gives a first rate's (judgement, the 74's)."""
    boom_ft = STUDDING[("fore", "lower")][3]
    depth = z_m(fore_channel_ft()) - 0.5
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
                "of the boom, down from the boom at her fore channel to half a metre off the water "
                "(the 74's and the frigate-36's, judgement); in the sail room."
                + g.canvas_note(canvas)
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
# The guns (Con-D §5; package 81's checklist, Build-Ships.md §6's postscript)
# ---------------------------------------------------------------------------

# Her two fits (Con-D decision 7), in the file's order, and the default (the owner's Dec 8).
FIT_1797 = "concepcion 1797"
FIT_1809 = "concepcion 1809"
DEFAULT_FIT = FIT_1797
# Her guns numbered by deck from forward, each deck from No. 1, as the 74's (B7.d; Con-D decision
# 6): the lower deck Nos. 1 to 15 armed and No. 16 the empty sixteenth pair aftmost, the middle and
# the upper 1 to 16, the quarterdeck 1 to 6, the forecastle 1 to 3, the poop 1 to 3; a place keeps
# its number in both fits, and a fit that leaves a place empty leaves a gap.
GUN_DECKS = ("lower", "middle", "upper", "quarterdeck", "forecastle", "roundhouse")
NUMBERING = "by deck"
# Each fit's pieces and its broadside in libras by 70's rule (one side's broadside guns), her guns'
# pounds being as her navy named them (Winfield p. 407: VR-Sp §4), with the book's pair beside.
FIT_FIGURES = {FIT_1797: (112, 1188), FIT_1809: (116, 1508)}
WINFIELD_PAIRS = {FIT_1797: "1,188 libras (1,282 lb)", FIT_1809: "1,508 libras (1,627 lb)"}
# The Regulations' allowance for exercise: a third of the upper deck's guns in a ship of two or
# three decks (the Regulations 1806, the Gunner, Art. XXI; Eng §6.2), her third battery's 32.
UPPER_DECK_GUNS = 32
# The book's libra in English pounds (0.4608 kg: Winfield et al. 2023, pp. 41-46, VR-Sp §7).
LIBRA_LB = 0.4608 / 0.45359237
# The guns' weights, cwt: no Spanish weight by calibre is in the passages read (Con-D §5.3), so
# each is an English pattern's of nearest weight, interim (JUDGEMENT): the long 24, 18 and 12
# Adye's of 9 ft 6 in and the long 8 Adye's 9 of 7 ft 6 in (Adye 1804 p. 155: `period`), the long
# 36 the English 32's 55 cwt scaled by the shot, 36 libras over 32 lb (36.57 / 32), the 48-pounder
# obús the English 42-pounder carronade's and the 24-pounder obús the 24-pounder carronade's (Adye
# 1804 p. 72: `period`), until the period's Spanish artillery treatises give them.
CWT = {
    ("long", 36): round(period.ADYE_LONG_GUN_CWT[32][(9, 6)] * 36.0 * LIBRA_LB / 32.0, 1),
    ("long", 24): period.ADYE_LONG_GUN_CWT[24][(9, 6)],
    ("long", 18): period.ADYE_LONG_GUN_CWT[18][(9, 6)],
    ("long", 12): period.ADYE_LONG_GUN_CWT[12][(9, 6)],
    ("long", 8): period.ADYE_LONG_GUN_CWT[9][(7, 6)],
    ("carronade", 48): period.ADYE_CARRONADE_CWT[42],
    ("carronade", 24): period.ADYE_CARRONADE_CWT[24],
}
# The men to a pair (Con-D §5.3): Falconer's for the long guns "when the ship is well manned"
# (1780, QUARTERS: `period.FALCONER_CREW`), the 36 fourteen between Falconer's thirteen for a 32
# and fifteen for a 42 and the 8 Falconer's 9's six (judgement); an obús Douglas's four for a
# carronade (1829, art. 136).
CREW = {
    ("long", 36): 14,
    ("long", 24): period.FALCONER_CREW[24],
    ("long", 18): period.FALCONER_CREW[18],
    ("long", 12): period.FALCONER_CREW[12],
    ("long", 8): period.FALCONER_CREW[9],
    ("carronade", 48): period.DOUGLAS_CARRONADE_CREW,
    ("carronade", 24): period.DOUGLAS_CARRONADE_CREW,
}
POUNDS_WORDS = (
    "filed as her navy named it (the owner's Dec 9: Plan-Package90.md §0), a Spanish gun's "
    "libras about 1.6 per cent over English pounds at the book's libra of 0.4608 kg (Winfield et "
    "al. 2023, pp. 41-46: VR-Sp §7), so the game's range and weight of broadside read it a "
    "little light"
)
OBUS_WORDS = (
    "carried as a carronade of its calibre (Plan-Package90.md §4 row 10; Con-D §5.4): plainly, a "
    "howitzer threw a shell as well as a shot, and the engine has no shell, so it fires round and "
    "grape as a carronade does; the obús as a kind of its own is a later gunnery package's"
)
ARMAMENT_NOTE = (
    "The armament (spec M7 7; package 70; docs/design/Design-Ship-PurisimaConcepcion.md §5): the "
    "guns as parts of the graph by their place, in her two fits, each on its port of the hull's "
    "profile or its place over the rail to the centimetre, its deck named (Build-Ships.md §4.4); "
    "her guns by deck her own record's (Winfield et al. 2023, pp. 406-410), their pounds as her "
    "navy named them (the owner's Dec 9), the obús carried as a carronade of its calibre; their "
    "weights the English patterns of nearest weight (Adye 1804 pp. 72, 155: interim, JUDGEMENT, no "
    "Spanish weight by calibre being read); their crews by Falconer 1780 and Douglas 1829; the "
    "magazine's allowance by kind and calibre, a foreign gun's charge its kind's share. Numbered "
    "by deck, each deck's pairs from No. 1 forward, a pair keeping one number, so her gun is said "
    "with its deck; the `numbering` below says so (B7.d). Every figure's source is in "
    "tools/ships/concepcion.py."
)


def places_of(profile):
    """Each deck's places from forward as (number, x, sill), metres as the profile has them, so
    that a gun on one stands on its triple (Build-Ships.md §4.4), numbered by deck from No. 1."""
    out = {}
    for deck in GUN_DECKS:
        ports = sorted(profile["ports_m"][deck], key=lambda t: -t[0])
        out[deck] = [(1 + i, x, sill) for i, (x, sill, _hb) in enumerate(ports)]
    return out


def by_deck_id(gun):
    """A gun's id with its deck (B7.d): `gun.lower.3.starboard`."""
    return f"gun.{gun['deck']}.{gun['number']}.{gun['side']}"


def pairs(places, deck, kind, pounder, note):
    """Broadside pairs at `places`, each gun on its triple to the centimetre with its deck named,
    its weight and crew by her rules; the note on the first. Each id re-keyed by its deck after the
    call (`by_deck_id`)."""
    cwt = CWT[(kind, pounder)]
    out = []
    for i, (number, x, sill) in enumerate(places):
        made = g.broadside_pair(
            number, kind, pounder, cwt, x, sill, note if i == 0 else None, deck=deck, round_to=0.01
        )
        for gun, _ in made:
            gun["id"] = by_deck_id(gun)  # reassigned, so that the key keeps its place
            gun["crew"] = CREW[(kind, pounder)]
        out += made
    return out


def numbered(places, *numbers):
    """The places of a deck with these numbers, in the deck's order."""
    return [p for p in places if p[0] in numbers]


def her_fits(profile):
    """Her two fits (Con-D §5.1-§5.3) as (name, source, guns, note), in the file's order."""
    p = places_of(profile)
    lower = pairs(
        numbered(p["lower"], *range(1, 16)),
        "lower",
        "long",
        36,
        "The lower deck's thirty long 36-pounders, fifteen a side at Nos. 1 to 15 from forward, "
        "PB-039's ports; No. 16, the sixteenth pair aftmost cut at Cádiz in 1791, empty, unarmed "
        "in Spanish service (VR-Sp §4). A 36-pounder of the Spanish navy, 36 libras, "
        f"{POUNDS_WORDS}; its weight the English 32's 55 cwt scaled by the shot (interim, "
        "JUDGEMENT: Con-D §5.3); fourteen men to the pair, between Falconer's thirteen for a 32 "
        "and fifteen for a 42 (judgement), who fight whichever side bears. Numbered by deck from "
        "forward, each deck from No. 1 (B7.d).",
    )
    middle = pairs(
        p["middle"],
        "middle",
        "long",
        24,
        "The middle deck's thirty-two long 24-pounders, sixteen a side: a Spanish 24 of 24 libras, "
        "filed as her navy named it; its weight Adye's 24-pounder of 9 ft 6 in, 49 cwt 2 qr (Adye "
        "1804 p. 155; interim, JUDGEMENT on the pattern); eleven men to the pair (Falconer 1780, "
        "QUARTERS). Plainly: James gives the San Josef 18-pounders on her second deck at her "
        "capture (vol. 2 p. 51); Winfield's 24s are taken, the book's broadside the check.",
    )
    upper_12 = pairs(
        p["upper"],
        "upper",
        "long",
        12,
        "The upper deck's thirty-two long 12-pounders, sixteen a side, the 18s replaced by 12s at "
        "the rebuild (VR-Sp §4): a Spanish 12 of 12 libras, filed as her navy named it; Adye's "
        "12-pounder of 9 ft 6 in, 34 cwt (interim, JUDGEMENT); seven men to the pair (Falconer).",
    )
    qd_8 = pairs(
        p["quarterdeck"],
        "quarterdeck",
        "long",
        8,
        "The quarterdeck's twelve long 8-pounders, six a side at ZAZ0100's places, added at the "
        "rebuild (VR-Sp §4): a Spanish 8 of 8 libras, filed as her navy named it; Adye's 9-pounder "
        "of 7 ft 6 in, 24 cwt 2 qr, the nearest pattern (interim, JUDGEMENT); six men to the pair, "
        "Falconer's for a 9 (judgement).",
    )
    fc_8 = pairs(
        p["forecastle"],
        "forecastle",
        "long",
        8,
        "The forecastle's six long 8-pounders, three a side (the places JUDGEMENT: no sheet's "
        "forecastle ports were made out, Pages §11.3); the quarterdeck's pattern and crew.",
    )
    of_1797 = lower + middle + upper_12 + qd_8 + fc_8
    lower_9 = pairs(
        numbered(p["lower"], *range(1, 16)),
        "lower",
        "long",
        36,
        "The lower deck's thirty long 36-pounders, as in the 1797 fit, No. 16 empty.",
    )
    middle_9 = pairs(p["middle"], "middle", "long", 24, "The middle deck's 24s, as in 1797.")
    upper_18 = pairs(
        p["upper"],
        "upper",
        "long",
        18,
        "The upper deck's thirty-two long 18-pounders, the 12s replaced at Ferrol in 1803 (VR-Sp "
        "§4; the ordinance of 1803's own note: 'Concepción carried 18-pounders in her third "
        "battery', VR-Sp §16): a Spanish 18 of 18 libras, filed as her navy named it; Adye's "
        "18-pounder of 9 ft 6 in, 42 cwt (interim, JUDGEMENT); nine men to the pair (Falconer).",
    )
    qd_long = pairs(
        numbered(p["quarterdeck"], 1, 2),
        "quarterdeck",
        "long",
        8,
        "The quarterdeck's four long 8-pounders at its two foremost ports a side, in the wake of "
        "the main shrouds (the 74's 1812 rule, long guns at the shrouds: Bel-D §5.1; the places "
        "JUDGEMENT); No. 3 left empty, the fit carrying ten pieces on the twelve ports.",
    )
    qd_obus = pairs(
        numbered(p["quarterdeck"], 4, 5, 6),
        "quarterdeck",
        "carronade",
        48,
        "The quarterdeck's six 48-pounder obuses, three a side at its three after ports (the "
        "places JUDGEMENT: the obuses on the ports nearest the ends, Con-D §3.3): a 48-pounder "
        f"obús of the Spanish navy, {OBUS_WORDS}; its weight the English 42-pounder carronade's, "
        "22 cwt 1 qr (Adye 1804 p. 72; interim, JUDGEMENT); four men to the pair (Douglas 1829 "
        "art. 136), the soldiers first at the beat (crew/quarters.py).",
    )
    fc_obus = pairs(
        numbered(p["forecastle"], 1),
        "forecastle",
        "carronade",
        48,
        "The forecastle's two 48-pounder obuses at its foremost ports, forward of the fore "
        "shrouds (the places JUDGEMENT), as the quarterdeck's.",
    )
    fc_long = pairs(
        numbered(p["forecastle"], 2, 3),
        "forecastle",
        "long",
        8,
        "The forecastle's four long 8-pounders at its after ports, in the wake of the fore shrouds "
        "(JUDGEMENT), as the quarterdeck's.",
    )
    poop_obus = pairs(
        p["roundhouse"],
        "roundhouse",
        "carronade",
        24,
        "The poop's six 24-pounder obuses, three a side over its rail (VR-Sp §4, the 1803 "
        f"alteration; the places ZAZ0100's three small poop ports, JUDGEMENT): {OBUS_WORDS}; "
        "Adye's 24-pounder carronade, 13 cwt (interim, JUDGEMENT); four men to the pair (Douglas).",
    )
    of_1809 = lower_9 + middle_9 + upper_18 + qd_long + qd_obus + fc_obus + fc_long + poop_obus
    source = (
        "Winfield et al. 2023, Spanish Warships in the Age of Sail 1700-1860, pp. 406-410 (via the "
        "lead: VesselReferences-2026-11-Spanish.md §4, §16); Adye 1804 pp. 72 and 155, the English "
        "patterns of nearest weight (interim); Falconer 1780 (QUARTERS) and Douglas 1829 (art. "
        "136), the crews"
    )

    def own(guns):
        """A fit's guns its own mappings, that no two fits share one (the dump would alias it)."""
        return [(dict(gun), note) for gun, note in guns]

    return [
        (
            FIT_1797,
            source,
            own(of_1797),
            "Her establishment of 112 after the rebuild at Cádiz (1786 to 1793), the class's from "
            "1793 to 1803 and St Vincent's: 30 x 36-pounders on the lower deck, 32 x 24 on the "
            "middle, 32 x 12 on the upper, 12 x 8 on the quarterdeck and 6 x 8 on the forecastle, "
            f"112 pieces, a broadside of {WINFIELD_PAIRS[FIT_1797]} as the book gives the pair "
            "(Winfield p. 407: VR-Sp §4); the game sums her pounds as her navy named them, so her "
            "broadside reads about 1.6 per cent light in English pounds. The default (the owner's "
            "Dec 8): her company the file's, the 1788 regulation's 877, of whom 225 soldiers "
            "(VR-Sp §15).",
        ),
        (
            FIT_1809,
            source,
            own(of_1809),
            "As altered at Ferrol in 1803 and recommissioned to Cádiz in September 1809, to her "
            "loss in March 1810: 30 x 36, 32 x 24 and 32 x 18 on her three gun decks, 4 x 8 and 6 "
            "x 48-pounder obuses on the quarterdeck, 4 x 8 and 2 x 48-pounder obuses on the "
            "forecastle and 6 x 24-pounder obuses on the poop, 116 pieces, a broadside of "
            f"{WINFIELD_PAIRS[FIT_1809]} (Winfield p. 407: VR-Sp §4). The ordinance of 1803's "
            "three-decker of 112 carries two more 48-pounder obuses on the quarterdeck, 118 "
            "pieces, the poop's six outside the nominal count (VR-Sp §16): noted, not a fit. "
            "Plainly, her company: the Regulation of 16 October 1803 gives a 112 1,015, of whom "
            "275 soldiers, 200 infantry and 75 infantry-artillery (VR-Sp §15); a company belongs "
            "to a file (the lead's ruling (5) of 2026-11-07), so this fit sails with the file's "
            "877 of the 1788 regulation, the 1803 figure a departure recorded here (Con-D §6.1).",
        ),
    ]


def broadside_lb(guns):
    """A fit's broadside by 70's rule (combat/far.py): one side's broadside guns and every chaser,
    in her guns' own pounds (libras)."""
    one_side = [gun for gun, _ in guns if gun["place"] != "broadside" or gun["side"] == g.SIDES[0]]
    return sum(gun["pounder"] for gun in one_side)


def check_fits(fits, profile):
    """Con-D §5's checks on her guns, raised before her file is written: every gun of every fit on
    a triple of its deck to the centimetre, its deck named, its id its deck's, number's and side's
    (B7.d); the pieces of each fit 112 and 116, their broadsides 1,188 and 1,508 libras."""
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
                f"her fit '{name}' mounts {pieces} pieces with a broadside of {lb} libras, not "
                f"{FIT_FIGURES[name][0]} and {FIT_FIGURES[name][1]} (Winfield p. 407)."
            )


def default_guns(fits):
    """The default fit's guns, against which her quarter bill and her stores are set."""
    return next(guns for name, _, guns, _ in fits if name == DEFAULT_FIT)


def armament(b, fits):
    """Her fits and their magazines: `fit_magazine` with the King's allowance (judgement, as every
    King's file), a foreign gun's charge its kind's share (`charge_lb`), the exercise a
    three-decker's, a third of her upper deck's guns (Eng §6.2). Her guns numbered by deck (B7.d):
    the armament's `numbering` set after the call, as the 74's."""
    exercise = g.exercise_allowance(UPPER_DECK_GUNS, decks=3)
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
# The company, her soldiers and the quarter bill (Con-D §6)
# ---------------------------------------------------------------------------

# Her company by the 1788 regulation, a navío of 112 (Winfield et al. 2023, p. 1446 and the two
# pages following: VR-Sp §15): 19 commissioned officers, 10 major officers, 23 sea officers, 168
# infantry, 57 infantry-artillery, 130 artillery, 200 seamen, 230 landsmen and 40 boys, 877 in all
# (the book's Total, 848, leaves out the commissioned and the major officers). Her own 839 (pp.
# 406-410, unbroken: VR-Sp §4) is in her note. The split onto the game's stations is JUDGEMENT
# (Con-D §6.1), the 74's form, the regulation's kinds its check: her posts the commissioned
# officers and the chiefs of the major and sea officers; her soldiers, the infantry and the
# infantry-artillery, the `marines` station; her idlers the rest of the major and sea officers'
# trades and the officers' servants; her seamen the artillery, the seamen, the landsmen, the boys
# and the alféreces, in the six stations as the frigate-36's 182 are.
COMPLEMENT = 877
REGULATION_1788 = {
    "commissioned": 19,
    "major": 10,
    "sea": 23,
    "infantry": 168,
    "infantry-artillery": 57,
    "artillery": 130,
    "seamen": 200,
    "landsmen": 230,
    "boys": 40,
}
REGULATION_1803 = {"all": 1015, "infantry": 200, "infantry-artillery": 75}
HER_OWN_MEN = 839
POSTS = 21
SOLDIERS = REGULATION_1788["infantry"] + REGULATION_1788["infantry-artillery"]
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
        15,
        "the carpenters and caulkers of her sea officers and their crew, the 74's eleven scaled "
        "to a first rate (judgement)",
    ),
    "sailmaker's crew": (5, "the sailmaker's mates and crew (judgement)"),
    "cooper": (2, "two coopers, for the casks (judgement)"),
    "armourer": (4, "the armourers of her sea officers (the regulation's kind; judgement)"),
    "cook": (3, "the cooks of her sea officers (the regulation's kind; judgement)"),
    "steward": (4, "the purser's people (judgement)"),
    "servant": (19, "the officers' servants, of her forty boys (judgement)"),
    "surgeon's mate": (3, "the surgeons of her major officers beyond the surgeon (judgement)"),
    "clerk": (3, "the captain's and the purser's clerks (judgement)"),
    "master-at-arms's party": (2, "two corporals (judgement)"),
}
SOLDIERS_NOTE = (
    "her soldiers, the 1788 regulation's 168 infantry and 57 infantry-artillery (Winfield et al. "
    "2023, p. 1446: VR-Sp §15), in the marines' station, whose kit is the nation's: in the game "
    "they serve the carronades and no long gun, which her bill keeps (crew/quarters.py), and stand "
    "watch and work as afterguard, never aloft. The 1803 regulation's 275 (200 and 75) are in the "
    "1809 fit's note, a departure"
)
# Her ratings by the regulation's kinds (JUDGEMENT on the kinds, Con-D §6.1): her seamen, 200 of
# the 600 of the artillery, seamen, landsmen and boys, as able; the artillery, the artilleros de
# mar, 130, as ordinary; the landsmen and the boys, 270, as landsmen.
RATINGS = {"able": 0.33, "ordinary": 0.22, "landsman": 0.45}
# The quarter bill beyond the trimmers (Con-D §6.3): four at the helm, two wheels' men on a first
# rate (JUDGEMENT); no powder beyond the idlers (the 74's); her small-arms men the frigate-36's
# share of her seamen and her boarders a quarter of them (the 74's rules); her filling party one
# to every four cannon of her default fit (Falconer 1780, QUARTER-GUNNER: `gen_ships`).
HELM = 4
SMALL_ARMS_OF_SEAMEN = 20.0 / 182.0
BOARDERS_OF_SEAMEN = 0.25
# The trimmers' shares by station, the frigate-36's 8, 10, 12, 6 and 8 (the 74's; judgement).
TRIMMER_SHARES = {"forecastle": 8, "fore_top": 10, "main_top": 12, "mizzen_top": 6, "afterguard": 8}
# The 74's trimmers, 55 of her 419 seamen (her bill as filed), the share against which hers are
# measured for the lead (her report): the 74's rule leaves her what her long guns do not take.
SEVENTY_FOURS_TRIMMERS = (55, 419)
# Her stores beside the company (Con-D §7; the 74's method, judgement): the frigate-36's 100 tons of
# water for her 264 and her 600 fathoms of spare rope, carried by the complement; four months'
# provisions (the 74's days).
FRIGATE_COMPLEMENT = 264.0
PROVISIONS_DAYS = 120
# The relieving tackles' hands at her tiller where the wheel is shot away (package 116): the lead's
# ruling 8 of 2026-11-18 (Plan-Package90.md §13.1) asks her builder to propose the number with her
# file. Eight is proposed, a first rate's heavier tiller against the frigate's six (Con-D §7,
# JUDGEMENT); a ship file's `timing:` carries an evolution's timing keys and not its crew, so the
# number is in her report for the lead and the tackles are measured with the evolution's six.
TACKLES_HANDS_PROPOSED = 8


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
    """Her seamen by station: the complement less the posts, the soldiers and the idlers, shared
    by the frigate-36's stations."""
    idlers = sum(n for n, _ in IDLERS.values())
    return shares(COMPLEMENT - POSTS - SOLDIERS - idlers, FRIGATE_SEAMEN)


def at_the_guns(guns, marines):
    """The men one side's guns of a fit take, and how many of them are soldiers, who take the
    carronades first (crew/quarters.py)."""
    one_side = [gun for gun, _ in guns if gun["place"] != "broadside" or gun["side"] == g.SIDES[0]]
    men = sum(gun["crew"] for gun in one_side)
    carronades = sum(gun["crew"] for gun in one_side if gun["kind"] == "carronade")
    return men, min(carronades, marines)


def company(b, guns):
    """Her crew section (Con-D §6.1-§6.2), the posts and the people drawn at muster from her people
    file (§6.6), and the stores beside them: water, provisions and cordage by her complement, a shot
    plug to each of the default fit's `guns` (§7), the spare spars and the sail room by the 74's
    method."""
    posts, drawn = g.wardroom("three-decker")
    if len(posts) != POSTS:
        raise ValueError(f"her people file gives {len(posts)} posts, not her {POSTS} (Con-D §6.1).")
    seamen = seamen_by_station()
    idlers = sum(n for n, _ in IDLERS.values())
    water = half_up(100.0 * COMPLEMENT / FRIGATE_COMPLEMENT)
    cordage = 50 * half_up(600.0 * COMPLEMENT / FRIGATE_COMPLEMENT / 50.0)
    stations_note = (
        "Hands per station, both watches together: her seamen, the complement less the posts, the "
        "soldiers and the idlers, shared among the six stations as the frigate-36's 182 are (28, "
        "24, 30, 14, 50 and 36: judgement, the 74's), the regulation's artillery, seamen, "
        "landsmen and boys and her alféreces among them, the boys in the afterguard as landsmen "
        "(spec M3 9 item 6). Forecastlemen: the head, anchors and headsails."
    )
    entries = [
        (
            ("complement",),
            COMPLEMENT,
            "A navío of 112's company by the regulation of 1 January 1788, 877 men and boys: 19 "
            "commissioned officers, 10 major officers, 23 sea officers, 168 infantry, 57 "
            "infantry-artillery, 130 artillery, 200 seamen, 230 landsmen and 40 boys (Winfield et "
            "al. 2023, p. 1446 and the two pages following: VR-Sp §15; the book's Total, 848, "
            "leaves out the commissioned and the major officers), the 1797 fit's, the file's. Her "
            f"own {HER_OWN_MEN} (pp. 406-410, unbroken: VR-Sp §4) beside it, four per cent under. "
            "The war increase, a man for each gun of her main batteries, half infantry and half "
            "landsmen, is not filed (907 or 971 by the reading of 'battery': VR-Sp §15; the "
            "lead's). The 1809 fit's 1,015 by the regulation of 1803 is in its note.",
        ),
        (
            ("names",),
            "spanish",
            "A ship of the Spanish navy: the spanish list in data/crew/names.yaml (package 90, "
            "N1).",
        ),
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
        (("stations", "marines"), SOLDIERS, f"Soldiers: {SOLDIERS_NOTE}."),
        (
            ("stations", "idlers"),
            idlers,
            "Idlers: the trades below (Luce 1884 ch. XX: they stand no night watches).",
        ),
        (
            ("ratings", "able"),
            RATINGS["able"],
            "Share of the seamen (not soldiers, idlers or officers) by rating, by the regulation's "
            "kinds (JUDGEMENT, Con-D §6.1): her 200 seamen of its 600 artillery, seamen, landsmen "
            f"and boys able, {RATINGS['able']:.2f}.",
        ),
        (
            ("ratings", "ordinary"),
            RATINGS["ordinary"],
            f"Ordinary: the 130 artillery, artilleros de mar, {RATINGS['ordinary']:.2f}.",
        ),
        (
            ("ratings", "landsman"),
            RATINGS["landsman"],
            f"Landsmen: the 230 landsmen and the 40 boys, {RATINGS['landsman']:.2f}.",
        ),
    ]
    entries += [
        (
            ("posts", post),
            None,
            (
                "Station holders by post (spec M3 2.3), in the game's English, as for every ship: "
                "of the regulation's commissioned officers her brigadier commanding, the captain; "
                "the capitán de navío, her second; the capitán de fragata, the first lieutenant; "
                "and the four tenientes de navío and four tenientes de fragata, the second to the "
                "ninth lieutenants, the eight alféreces in her stations; the chiefs of her major "
                "and sea officers, the first and second pilots as the master and the second "
                "master, the boatswain, the gunner, the carpenter, the purser, the surgeon and the "
                "chaplain; and the sailmaker and the master-at-arms, posts in the 74's file "
                "(JUDGEMENT, Con-D §6.1). Her people file (data/people/three-decker.yaml) gives "
                "them. Names are drawn at muster unless a post gives one."
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
                "How the idlers are made up (JUDGEMENT, Con-D §6.1), the rest of the regulation's "
                "sea and major officers' trades and her officers' servants; they must sum to the "
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
            "Water: the frigate-36's 100 tons for her 264 carried by the complement (Con-D §7; "
            "judgement, the 74's method), as many weeks at a gallon a man a day as hers.",
        ),
        (
            ("stores", "provisions_days"),
            PROVISIONS_DAYS,
            "Provisions: four months at full allowance for the complement, the 74's (judgement).",
        ),
        (("stores", "spare_spars"), {}, None),
        (
            ("stores", "cordage_fathoms"),
            cordage,
            "Spare rope in the boatswain's store: the frigate-36's 600 fathoms carried by the "
            "complement, to fifty fathoms (Con-D §7; judgement, the 74's).",
        ),
        (
            ("stores", "shot_plugs"),
            len(guns),
            g.SHOT_PLUGS_NOTE + " One a gun of her default fit (Con-D §7).",
        ),
        *g.ration_entries("a King's ship"),
    ]
    b.crew(entries)
    b.people(
        "The named people beyond the posts (package 35, spec M5 §22): each drawn from a station "
        "at muster, the counts above unchanged; see data/people/three-decker.yaml.",
        drawn,
    )
    b.spare_spars(
        "The booms: the spare spars by class, the 74's (Luce 1866 ch. XVII, 'Stowing Booms'; Luce "
        "1884 ch. XI; Steel 1794 vol. I, 'Lashing of Booms'), of her own spars (Con-D §7); see "
        "tools/ships/concepcion.py.",
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
        ],
    )
    sail_room(b)


def sail_room(b):
    """Her sail room by the frigate-36's method (Luce 1884 ch. X p. 171), the 74's, on her own
    sails (Con-D §7): the second of each working sail she carries, the heavy-weather foresail and
    topsails of No. 1, one of each storm sail, and her save-alls."""
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
    occasional = [f"fore.save_all.{s}" for s in g.SIDES]

    def first(text, i):
        return text if i == 0 else None

    b.sail_room(
        "The sail room (spec 3b §6.3): Luce's allowance for a frigate (1884 ch. X p. 171), as the "
        "74's, on her own sails (Con-D §7), every sail new; see tools/ships/concepcion.py.",
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
                first("The occasional sails, one each (spec 3b §6.4): the save-alls.", i),
            )
            for i, k in enumerate(occasional)
        ],
    )


def quarter_bill(b, guns):
    """Her quarter bill set against the default fit (Con-D §6.3), by the 74's rule: the trimmers
    what her seamen leave when one side's long guns and the wheel are manned, the soldiers taking
    the carronades, split by the frigate-36's shares; the bill's `marines` the soldiers kept in
    their division, the rest of them, written after the generator's call, which takes no such key
    (the 74's)."""
    seamen = sum(seamen_by_station().values())
    men, marines_at = at_the_guns(guns, SOLDIERS)
    total = seamen - (men - marines_at) - HELM
    if total < len(TRIMMER_SHARES):
        raise ValueError(
            f"her {seamen} seamen leave {total} trimmers when one side's long guns of "
            f"'{DEFAULT_FIT}' ({men - marines_at} men) and the wheel are manned (Con-D §6.1)."
        )
    trimmers = shares(total, TRIMMER_SHARES)
    kept = SOLDIERS - marines_at
    REPORT["bill"] = (seamen, men, marines_at, total, kept)
    b.quarter_bill(
        g.QUARTER_BILL_NOTE,
        [
            (
                "forecastle",
                trimmers["forecastle"],
                f"The trimmers: what her seamen leave when one side's guns of '{DEFAULT_FIT}' and "
                "the wheel are manned, the soldiers serving no long gun, split by the frigate-36's "
                "trimmer shares, 8, 10, 12, 6 and 8 of 44 (the 74's rule; judgement). Of the "
                "forecastlemen, for the head sails and the fore braces.",
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
            "helm": "Four at the wheel, two wheels' men on a first rate (Con-D §6.3, JUDGEMENT).",
            "powder": "The powder beyond the idlers: none, as the 74's; her boys among the "
            "idlers, her cooks, stewards, clerks, the coopers, the armourers and the sailmaker's "
            "crew pass the cartridges (Falconer 1780, QUARTERS; judgement).",
            "priority": g.PRIORITY_NOTE,
        },
        small_arms=half_up(seamen * SMALL_ARMS_OF_SEAMEN),
        boarders=half_up(seamen * BOARDERS_OF_SEAMEN),
        small_arms_note="Seamen with the muskets of the stand of arms, the frigate-36's share of "
        "her seamen (20 of 182; judgement, the 74's); her soldiers are the musketry's body.",
        boarders_note="The boarders by the bill, a quarter of her seamen told off from the guns' "
        "crews (Luce 1884 ch. XX; judgement, the shared rule), with the soldiers.",
        filling=g.filling_party(guns),
    )
    b.crew_notes[("quarter_bill", "filling")] = (
        g.FILLING_NOTE + " Hers one to every four cannon of her default fit (Falconer 1780, "
        "QUARTER-GUNNER; judgement for her)."
    )
    b.doc["crew"]["quarter_bill"]["marines"] = kept
    b.crew_notes[("quarter_bill", "marines")] = (
        "The soldiers the bill keeps in their division at the beat: her soldiers but those at the "
        "default fit's carronades, on the poop and the gangways with their muskets (the 74's form, "
        "Falconer 1780, QUARTERS; Con-D §6.3). Read by the bill by deck (B7.b): her long guns take "
        "no soldier. Plainly: Spanish practice put soldiers at the guns, the infantry-artillery "
        "the artillery's own (Con-D §6.1); the engine's rule keeps them from the long guns, and "
        "her report measures what that leaves for the lead."
    )


def fit_bills(b, fits):
    """Each fit beside the default's its own bill where its guns want one (`schema.FIT_OWN_BILL`;
    the 64's and the razee's road, package 75, B1 and Phase 5): its `marines`, her soldiers less
    those at the fit's carronades, her obuses, who take them first (Con-D §6.3: in 1809 the obuses
    take 28 of them); and its `trimmers`, what her seamen leave when one side's long guns of the
    fit and the wheel are manned, split by the frigate-36's shares, so that every crew of the fit
    is manned at the beat. JUDGEMENT each, the bill's rule on the fit's guns, said in its note; the
    file bears one company whatever her fit, the 1788 regulation's."""
    seamen = sum(seamen_by_station().values())
    bill = b.doc["crew"]["quarter_bill"]
    kept = bill["marines"]
    bill_trimmers = sum(bill["trimmers"].values())
    for name, _, guns, _ in fits:
        if name == DEFAULT_FIT:
            continue
        men, marines_at = at_the_guns(guns, SOLDIERS)
        own = {}
        n = SOLDIERS - marines_at
        if n != kept:
            own["marines"] = n
            REPORT.setdefault("fit_bills", []).append(("marines", name, men, marines_at, n))
            b.armament_notes[("fit", name, "marines")] = (
                "The soldiers the bill keeps in their division at the beat when she carries this "
                f"fit (the 64's road, package 75, B1): her {SOLDIERS} but the {marines_at} at this "
                "fit's obuses, carried as carronades, who take them first, the long guns taking "
                f"none (the bill's rule, B7.b); the bill's {kept} (above) is the default fit's. "
                "JUDGEMENT: the bill's rule on this fit's guns, the file bearing one company, the "
                "1788 regulation's."
            )
        total = seamen - (men - marines_at) - HELM
        if total != bill_trimmers:
            if total < len(TRIMMER_SHARES):
                raise ValueError(
                    f"her {seamen} seamen leave {total} trimmers on '{name}' (Con-D §6.1)."
                )
            own["trimmers"] = shares(total, TRIMMER_SHARES)
            REPORT.setdefault("fit_bills", []).append(("trimmers", name, men, marines_at, total))
            b.armament_notes[("fit", name, "trimmers")] = (
                "The trimmers the bill tells off by station at the beat when she carries this fit "
                "(the razee's road, package 75, Phase 5): what her seamen leave when one side's "
                "long guns of this fit and the wheel are manned, the soldiers taking the obuses "
                "first, split by the frigate-36's shares as the bill's are, so that every crew of "
                "this fit is manned at the beat; the bill's (above) are the default fit's, whose "
                f"guns want {'fewer' if total > bill_trimmers else 'more'} seamen. JUDGEMENT: the "
                "bill's rule on this fit's guns, the file bearing one company."
            )
        if not own:
            continue
        fit = b.doc["armament"]["fits"][name]
        items = list(fit.items())
        fit.clear()
        for k, v in items:
            fit[k] = v
            if k == "source":
                fit.update(own)


def check_company(b):
    """Con-D §6.1's checks on her company, raised before her file is written: the company's sum
    877, the regulation's kinds summing to it, her soldiers 225, the idlers by trade summing to the
    idlers, and the bill's `marines` no more than her soldiers."""
    crew = b.doc["crew"]
    st = crew["stations"]
    total = len(crew["posts"]) + sum(st.values())
    if total != COMPLEMENT or crew["complement"] != COMPLEMENT:
        raise ValueError(f"her company sums to {total}, not {COMPLEMENT} (Con-D §6.1).")
    if sum(REGULATION_1788.values()) != COMPLEMENT:
        raise ValueError("the 1788 regulation's kinds do not sum to her 877 (VR-Sp §15).")
    if st["marines"] != SOLDIERS:
        raise ValueError(f"her soldiers are {st['marines']}, not {SOLDIERS} (VR-Sp §15).")
    if sum(crew["idlers_by_trade"].values()) != st["idlers"]:
        raise ValueError("her idlers by trade do not sum to her idlers (Con-D §6.1).")
    if not 0 <= crew["quarter_bill"]["marines"] <= st["marines"]:
        raise ValueError("her bill keeps more soldiers than she bears (Con-D §6.3).")


# ---------------------------------------------------------------------------
# Ground tackle, boats, pumps and hold (Con-D §7)
# ---------------------------------------------------------------------------

# The ground tackle (Con-D §7), through `Builder.ground_tackle` directly: the 74's (Steel's
# "Smaller 74 Guns" and Lavery's Table 4: `period.STEEL_ANCHORS[74]`, `LAVERY_74_CABLES`) scaled to
# a first rate, every anchor by the rig's area, x 1.32, and the bower cable Steel's largest, 24
# in (Steel 1794 vol. I, "The Weight of Cables, Hawsers, &c.", OCR l. 7944-7950, read (OCR): the
# table's first row), the stream cable x 1.15 (JUDGEMENT, each: Steel's 100-gun row of the anchor
# table is garbled in the OCR, l. 5180 onward, and is to be read on the page image).
BOWER_CABLES = {"best_bower": 3, "small_bower": 2, "sheet": 1, "spare_anchor": 1}
ANCHOR_SCALE = AREA_SCALE
BOWER_CABLE_IN = 24.0
# Her burthen for the hold's rule: her sister the San Josef's 2,457 tons bm (James vol. 2 p. 59,
# read (OCR): Res §2.2), her own arqueo 2,771 tons as rebuilt (VR-Sp §4) being a Spanish capacity
# (JUDGEMENT).
BURTHEN_TONS = 2457.0
# Her boats, the 74's six (Lavery 1985 p. 16, Table 5) and a second launch (Con-D §7, JUDGEMENT).
BOATS = [
    (
        "launch",
        "launch",
        "the launch",
        31.0,
        "The launch of 31 ft, the 74's (Lavery 1985 p. 16, Table 5); her breadth a quarter of her "
        "length, her oars a thwart to three feet and her tons by the generator's rule for a boat "
        "herself (judgement).",
    ),
    (
        "second_launch",
        "launch",
        "the second launch",
        31.0,
        "A second launch of the same, a first rate's (Con-D §7, JUDGEMENT).",
    ),
    ("barge", "barge", "the barge", 32.0, "The barge of 32 ft, the 74's (judgement for hers)."),
    ("pinnace", "pinnace", "the pinnace", 28.0, "The pinnace of 28 ft, the 74's."),
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
# Her pumps: the 74's four chain pumps in the well round the main mast and two hand pumps (Con-D
# §7, JUDGEMENT).
PUMP_NAMES = [
    "the starboard after chain pump",
    "the larboard after chain pump",
    "the starboard fore chain pump",
    "the larboard fore chain pump",
    "the starboard hand pump",
    "the larboard hand pump",
]


def ground_tackle(b):
    """Her anchors and cables (Con-D §7), through `Builder.ground_tackle`."""
    steel = period.STEEL_ANCHORS[74]
    cables = period.LAVERY_74_CABLES
    if len(BOWER_CABLES) != steel["bowers"] or sum(BOWER_CABLES.values()) != steel["bower_cables"]:
        raise ValueError("her bowers and cables are not the 74's four and seven (Con-D §7).")
    bower_cwt = round(steel["bower_cwt"] * ANCHOR_SCALE)
    stream_cwt = round(steel["stream_cwt"] * ANCHOR_SCALE)
    kedge_cwt = round(steel["kedge_cwt"] * ANCHOR_SCALE, 1)
    bower = round(bower_cwt * g.CWT_KG)
    cable = BOWER_CABLE_IN
    stream = g.quarter(cables["stream_cable_in"] * RIG_SCALE)
    hawser = g.KEDGE_HAWSER_OF_BOWER * cable
    fathoms = period.LAVERY_74_CABLE_FATHOMS
    REPORT["anchors"] = (bower_cwt, stream_cwt, kedge_cwt, cable, stream)
    bowers = {
        "best_bower": (
            "bower",
            "the best bower",
            f"The bowers: four of {bower_cwt:g} cwt, the 74's 67 (Steel's 'Smaller 74 Guns' and "
            "Lavery 1985 p. 15, Table 4) scaled by her rig's area, x 1.32 (JUDGEMENT: Steel's "
            "100-gun row is garbled in the OCR); seven cables of 24 in, the largest of Steel's "
            "table of the weight of cables (Steel 1794 vol. I, OCR l. 7944-7950; JUDGEMENT), and "
            "100 fathoms, laid three on the best bower and two on the small, 'three Cables on the "
            "best Bower, two on the small Bower' (Lever 1808 p. 67).",
        ),
        "small_bower": ("bower", "the small bower", None),
        "sheet": ("sheet", "the sheet anchor", "The sheet anchor, a bower's size, on one cable."),
        "spare_anchor": (
            "sheet",
            "the spare anchor",
            "The spare anchor, the fourth bower, on the seventh cable; of the kind 'sheet', the "
            "schema's kinds being four, as the 74's.",
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
            float(round(stream_cwt * g.CWT_KG)),
            fathoms,
            stream,
            g.rope_kn(stream),
            f"The stream anchor of {stream_cwt:g} cwt, the 74's 16 x 1.32, on a stream cable of "
            f"{stream:g} in, the 74's 13 1/2 x 1.15 (JUDGEMENT), and 100 fathoms.",
        ),
        (
            "kedge",
            "kedge",
            "the kedge",
            float(round(kedge_cwt * g.CWT_KG)),
            fathoms,
            hawser,
            g.rope_kn(hawser),
            f"The kedge of {kedge_cwt:g} cwt, the 74's 8 x 1.32 (JUDGEMENT), on a hawser of half "
            "the bower cable's size, the house rule (gen_ships.KEDGE_HAWSER_OF_BOWER; judgement), "
            "of her cables' length (judgement).",
        ),
    ]
    b.ground_tackle(
        "The ground tackle (package 34, spec M5 §18): four bowers, a stream and a kedge, the 74's "
        "scaled to a first rate (Con-D §7, JUDGEMENT), every figure's source in "
        "tools/ships/concepcion.py; chain cable is later than 1805.",
        anchors,
        chain=False,
    )


def boat_line(bid, kind, name, length_ft, text):
    """A boat's line from her length by the generator's own factors (the 74's)."""
    breadth = length_ft * g.BOAT_BREADTH_OF_LENGTH
    oars = max(2, int(length_ft / g.BOAT_FEET_PER_OAR) // 2 * 2)
    weight_lb = (
        breadth * breadth * length_ft * g.BOAT_WEIGHT_FACTORS.get(kind, g.BOAT_WEIGHT_DEFAULT)
    )
    tons = round(max(0.1, weight_lb / g.LB_PER_TON), 1)
    return (bid, kind, name, float(length_ft), oars, oars + 1, tons, text)


def boats_pumps_hold(b):
    """Her hold by her burthen, her pumps, four chain and two hand, and her seven boats (Con-D
    §7)."""
    g.hold_for(
        b,
        BURTHEN_TONS,
        True,
        "2,457 tons, her sister the San Josef's burthen (James vol. 2 p. 59, read (OCR)); a ship "
        "of war's hold is her own stores and ballast: judgement",
    )
    b.pumps(
        g.PUMPS_NOTE + " Hers the 74's four chain pumps in the well round the main mast and two "
        "hand pumps (Con-D §7, JUDGEMENT).",
        g.pump_entries(4, 2, PUMP_NAMES),
    )
    b.boats(
        "The boats (package 35, spec M5 §23): the 74's six of about 1800 (Lavery 1985 p. 16, "
        "Table 5) and a second launch (Con-D §7, JUDGEMENT); their breadth, oars and tons by the "
        "generator's factors on those lengths; see tools/ships/concepcion.py.",
        [boat_line(*entry) for entry in BOATS],
    )


# ---------------------------------------------------------------------------
# Her description (Con-D §8.1; SW-4's form)
# ---------------------------------------------------------------------------

DESCRIPTION = (
    "three-decker",
    "a three-decker",
    "a three-decker, sixteen ports a tier",
    "A ship of three gun decks: the tops make out a three-decker at her rig's distance, her size "
    "and her three tiers being what the logs of the period record at first sight of a fleet "
    "('another First-rate', Nelson's narrative, Nicolas vol. 2 p. 341; the lead's ruling 17 of "
    "2026-11-12 for a ship of the line; JUDGEMENT on the distance, as the 74's); the glass her "
    "three tiers of sixteen ports a side as rebuilt (VR-Sp §4). Not 'a first rate' in what is made "
    "out: a rate is a navy's book, not a sight (judgement); 'a first rate' names her description "
    "in a scenario's words. Her default fit serves a far ship of her; her roles a King's ship's "
    "and, where she leads a squadron, a commodore's, a flagship through most of her service "
    "(VR-Sp §4; Con-D §12).",
    DEFAULT_FIT,
    ["kings-ship", "commodore"],
)


# ---------------------------------------------------------------------------
# The file
# ---------------------------------------------------------------------------

ERA_NOTES = (
    "Purísima Concepción, a three-decker of 112 guns of the Spanish navy, the first rate of her "
    "class as rebuilt: built at Ferrol to Romero Landa's 'sistema francés', launched 24 December "
    "1779 (94 guns), rebuilt at Cádiz 1786 to 1793 as a 112 "
    "(the sixteenth lower pair cut in 1791), at Toulon in 1793 and Cape St Vincent in 1797, "
    "altered to 116 at Ferrol in 1803, driven ashore in Cádiz Bay on 7 March 1810 and burnt "
    "(Winfield et al. 2023, pp. 406-410: VR-Sp §4). Hull: her own plan as built, PB-039 "
    "(Biblioteca Virtual de Defensa, record 1026905), measured (pages-concepcion.md); rig: the "
    "74's x 1.15 by Steel's rule; guns and company: Winfield and the regulations of 1788 and 1803; "
    "see tools/ships/concepcion.py for every figure and judgement."
)
HEADER = (
    "# The Purísima Concepción, three-decker of the Spanish navy, as rebuilt (1786-1793).\n"
    "# Generated by tools/gen_ships.py (tools/ships/concepcion.py); edit those and\n"
    "# rerun, do not edit this file. Hull and profile: measured on her own plan as\n"
    "# built, PB-039 (Biblioteca Virtual de Defensa, record 1026905;\n"
    "# docs/design/ships-design/pages-concepcion.md), her water the line as traced on it.\n"
    "# Spars and sails: the 74's (tools/ships/bellerophon.py) x 1.15 by Steel's rule for\n"
    "# her main mast, her mizen course cut at the mast and her yards under the bowsprit\n"
    "# (tools/ships/mizen_yard.py and spritsail_yards.py). Guns by deck: Winfield et al.\n"
    "# 2023, pp. 406-410; company: the regulation of 1788.\n"
    "# Units: metres, m2, kg, kN. Comments mark each judgement.\n"
)


def write(out_dir):
    """Build her file in full and dump it to `out_dir`."""
    hull, hull_notes = hull_block()
    b = HerBuilder("Purísima Concepción", "ship", ERA_NOTES, hull, hull_notes)
    geom, mast_x, rake = mast_geometry()

    yard_lengths = {"course": "yard", "topsail": "topsail_yard", "topgallant": "tg_yard"}
    yard_lengths["royal"] = "royal_yard"
    yard_heights = {"course": "yard_h", "topsail": "topsail_h", "topgallant": "tg_h"}
    yard_heights["royal"] = "royal_h"
    level_of_spar = {"course": "lower", "topsail": "topsail", "topgallant": "topgallant"}
    level_of_spar["royal"] = "royal"
    below = {"topgallant": "topsail_h", "royal": "tg_h"}

    # -- the square sails: Steel's x 1.15 below the topmast caps, cut to the spars above them ----
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

    mizen = mizen_course_cut(mast_x["mizzen"], rake["mizzen"])
    bow = head_geometry(geom, mast_x, rake)
    plain = (
        sum(areas[s][0] for s in areas if not s.endswith(".royal"))
        + sum(h["area"] for sid, h in bow["sails"].items() if sid != "fore.staysail")
        + mizen["area"]
    )
    # her rope: the frigate's scaled by the root of her plain sail over the frigate's (the 74's)
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
            "by Steel's rule, half the lower deck and the extreme breadth (Steel 1794 vol. I p. "
            "39) on her sister's, the 74's 108 ft x 1.15 (Con-D §4.1)"
            if name == "main"
            else "the 74's (Dragon's: Lavery 1985 p. 19, Table 10) x 1.15 (Con-D §4.1, JUDGEMENT)"
        )
        lower = b.spar(
            f"{name}.mast",
            "mast",
            x_m=x,
            rake_deg=rake[name],
            height_m=g.ft(gm["above"]),
            rating_kn=g.design_kn(carried["lower"], g.DESIGN_WIND_KN["lower"]),
            note=f"{name} lower mast {fmt_ft(gm['length'])} ({source}), its head "
            f"{fmt_ft(gm['head'])} by Steel's rule; stepped on the keel, its heel {heel:.2f} ft "
            "above the keel's top, the 74's x 1.15 (JUDGEMENT), standing through three decks; its "
            "place PB-039's stump above the rail, upright within the reading (Pages §5.7, §11.5; "
            f"ruling 5).{prov}",
        )
        top = b.spar(
            f"{name}.topmast",
            "topmast",
            steps_on=lower,
            height_m=g.ft(gm["t_hoist"]),
            rating_kn=g.design_kn(carried["topsail"], g.DESIGN_WIND_KN["topsail"]),
            note=f"{name} topmast {fmt_ft(gm['t_len'])}, the 74's x 1.15 (JUDGEMENT), its hoist "
            "above the lower cap the length less the lower mast head, its head "
            f"{fmt_ft(gm['t_head'])} by Steel's rule.{prov}",
        )
        tg = b.spar(
            f"{name}.topgallant_mast",
            "topgallant_mast",
            steps_on=top,
            height_m=g.ft(gm["g_hoist"]),
            rating_kn=g.design_kn(carried["topgallant"], g.DESIGN_WIND_KN["topgallant"]),
            note=f"{name} topgallant mast {fmt_ft(gm['g_len'])}, the 74's x 1.15 (JUDGEMENT), with "
            "its royal pole, one stick: its height the length less its square head of 3 1/2 in to "
            "a yard, up to the stop, above the topmast cap; Steel's long pole-head, two-thirds of "
            "the length to the stop, set up from the stop above it (Steel 1794 vol. I p. 16 and p. "
            f"42; the 74's).{prov}",
        )
        royal = b.spar(
            f"{name}.royal_mast",
            "royal_mast",
            steps_on=tg,
            height_m=g.ft(gm["r_hoist"]),
            rating_kn=g.design_kn(carried["royal"], g.DESIGN_WIND_KN["royal"]),
            note=f"{name} royal pole, the topgallant mast's own long pole-head (Steel 1794 vol. I "
            "p. 16 and p. 42), filed as a royal mast stepped on it as the 74's, so that the royal "
            f"yard has its own spar.{prov}",
        )
        on_spar = {"course": lower, "topsail": top, "topgallant": tg, "royal": royal}
        factor = g.FRIGATE_MAST_ROPE_FACTOR[name] * rope_scale
        for level, limit in BRACE_PLANS[name]:
            yard_id = f"{name}.{level}.yard" if level != "course" else f"{name}.yard"
            sail_id = sail_of(name, level)
            area, centre, head_cl, foot_cl, depth_yd, _depth, table = areas[sail_id]
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
                note=f"{name} {level} yard {fmt_ft(gm[yard_lengths[level]])}, the 74's x 1.15 "
                f"(JUDGEMENT); braces {limit} deg from square (the 74's, the frigate-36's: Fincham "
                f"1843 art. 102).{prov}",
            )
            reef = REEFS[level] if not isinstance(REEFS[level], dict) else REEFS[level][name]
            canvas = g.FRIGATE_CANVAS[sail_id]
            if level in ("topgallant", "royal"):
                how = (
                    "cut between its yard and the yard below as the spars stand on Steel's long "
                    f"pole-heads, on Steel's cloths x 1.15 ({head_cl:g} at the head, {foot_cl:g} "
                    "at the foot): the spars rule over the sail table (the owner's answer, "
                    f"Build-Ships.md §19.1 item 5), short of table IV's {depth_yd:g} yards deep"
                )
            else:
                how = (
                    f"Steel's table IV, the 74, x 1.15 (Con-D §4.2, JUDGEMENT): {head_cl:g} cloths "
                    f"at the head, {foot_cl:g} at the foot, {depth_yd:g} yards deep, 22 1/2 in a "
                    f"cloth in the sail; {reef} reef band{'s' if reef != 1 else ''} (Steel)"
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
            note=f"{shrouds} shrouds a side, the 74's count (judgement: her channels' deadeyes not "
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
        note=f"crossjack yard {fmt_ft(gz['yard'])}, the 74's x 1.15 (JUDGEMENT); crosses no sail, "
        f"spreads the mizzen topsail's foot; braces {CROSSJACK_BRACE_DEG} deg from square (the "
        "74's; judgement).",
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

    after_sail = mizen_course(b, mizen, rope_scale)
    REPORT["after_sail"] = mizen

    headsails = write_head(b, bow, rope_scale)
    sprit_sails = head_yards(b, bow, rope_scale)
    REPORT["head"] = bow

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
            "from the mizen mast head to a collar on the main mast above the deck (Steel 1794 vol. "
            "I, 'Mizen-stay'); the mizzen storm staysail sets on it",
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

    between = between_the_masts(b, geom, mast_x, rake)
    cut_areas = {s["id"]: s["area_m2"] for s in b.doc["sails"]}
    for sid in between:
        b.notes[sid] += steels_staysail_words(sid, cut_areas[sid])

    stuns = studding_sails(b, geom, mast_x, rake, rope_scale)
    storm = storm_canvas(b, geom, mast_x, rake, bow, after_sail, rope_scale)
    saves = save_alls(b, mast_x, rope_scale)

    # -- groups, the 74's set with the names the engine reads ------------------------------------
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
    b.group(
        "plain sail",
        sails_by_level["course"]
        + sails_by_level["topsail"]
        + sails_by_level["topgallant"]
        + headsails[1:]
        + [after_sail],
    )
    b.group("all sail", square + headsails + between + [after_sail] + stuns + sprit_sails)
    if sprit_sails:
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
    for word in ("mizzen course", "mizen course", "mizzen", "mizen"):
        b.alias(word, "mizzen.course")
    for word in ("mizzen yard", "mizen yard"):
        b.alias(word, "mizzen.yard")
    b.alias("foresail", "fore.course")
    b.alias("mainsail", "main.course")
    b.alias("fore yard", "fore.yard")
    b.alias("main yard", "main.yard")
    b.alias("crossjack yard", "mizzen.crossjack.yard")
    b.alias("cro'jack yard", "mizzen.crossjack.yard")
    b.alias("crossjack", "mizzen.crossjack.yard")
    if sprit_sails:
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
    b.group("storm canvas", storm)
    b.group("storm staysails", storm[:2])
    b.group("occasional sails", saves)
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

    # -- the ground tackle, the company, the guns and the stores (Con-D §5-§7); her description
    fits = her_fits(hull["profile"])
    check_fits(fits, hull["profile"])
    guns = default_guns(fits)
    ground_tackle(b)
    company(b, guns)
    armament(b, fits)
    quarter_bill(b, guns)
    fit_bills(b, fits)
    check_company(b)
    boats_pumps_hold(b)
    b.descriptions([DESCRIPTION])
    b.dump(os.path.join(out_dir, "three-decker.yaml"), HEADER)


def her_report() -> str:
    """The generator's report: what her rules compute from the file's own keys, printed as the file
    is written and held by her tests, so that it does not stand in the file's notes to go stale."""
    out = [f"three-decker: {line}" for line in REPORT.get("hull", ())]
    measured = REPORT.get("measured", [])
    out.append(
        "three-decker: port triples measured on PB-039, asserted within 0.05 m of the drawn side: "
        f"{len(measured)}."
    )
    if "dip" in REPORT:
        out.append(
            f"three-decker: her draught to K at the middle of her line as traced "
            f"{REPORT['draught']:.3f} m; her upper deck there {REPORT['deck']:.3f} m above her "
            f"water by the 74's method; her midship lower port dips at {REPORT['dip']:.2f} deg."
        )
    if "rope" in REPORT:
        plain, scale = REPORT["rope"]
        out.append(f"three-decker: plain sail {plain:.0f} m2, her rope's scale {scale:.3f}.")
    for sid, (area, centre, _h, _f, _d, depth, table) in REPORT.get("square", {}).items():
        if sid.endswith((".topgallant", ".royal")):
            out.append(
                f"three-decker: {sid}: {area} m2 cut to the spars, {depth / 3.0:.2f} yards deep "
                f"against table IV's x 1.15 ({table} m2), {area / table:.0%} of it; centre "
                f"{centre} m."
            )
    mz = REPORT.get("after_sail")
    if mz:
        out.append(
            f"three-decker: mizen course: tack {mz['corners'][0][1]:.2f} m above her water, "
            f"{(mz['corners'][0][1] - mz['deck']) / FT:.1f} ft above her quarterdeck at the mast; "
            f"its foot {mz['clear']:.2f} m over her poop and quarterdeck, at the least; "
            f"{mz['area']} m2, centre {mz['centre']} m; throat {mz['corners'][1][1]:.2f} m."
        )
        for words, o in mz["others"].items():
            out.append(
                f"three-decker: mizen course, the other reading, {words}: tack {o['tack']:.2f} m, "
                f"its foot {o['clear']:.2f} m over the poop, {o['area']:.0f} m2, centre "
                f"{o['centre']:.2f} m."
            )
    hd = REPORT.get("head")
    if hd:
        out.append(
            f"three-decker: bowsprit: {hd['inboard']:.1f} ft inboard along its steeve, "
            f"{hd['outboard']:.1f} ft outboard; its end {hd['tip'][1]:.2f} m above her water."
        )
        for sid, h in hd["sails"].items():
            out.append(f"three-decker: {sid}: {h['area']} m2, {h['fit']:.0%} of Steel's sides.")
    st = REPORT.get("sprit", {})
    if "sprit_topsail" in st:
        s = st["sprit_topsail"]
        along, head, foot = REPORT["sprit_drawn"]
        out.append(
            f"three-decker: sprit topsail: {s['area']:.0f} m2; the yards {s['gap']:.2f} m apart by "
            f"height, {s['slant']:.2f} m along the slant, {along:.2f} m as filed; drawn head "
            f"{head:.2f}, foot {foot:.2f}."
        )
        out.append(
            f"three-decker: spritsail: foot {st['spritsail']['foot_z']:.2f} m above her water."
        )
    for name, (pieces, lb, men) in REPORT.get("fits", {}).items():
        out.append(
            f"three-decker: fit '{name}': {pieces} pieces, a broadside of {lb} libras by 70's "
            f"rule, {men} men at one side's guns."
        )
    if "bill" in REPORT:
        seamen, men, marines_at, total, kept = REPORT["bill"]
        share = SEVENTY_FOURS_TRIMMERS[0] / SEVENTY_FOURS_TRIMMERS[1]
        out.append(
            f"three-decker: the quarter bill on '{DEFAULT_FIT}': her {seamen} seamen, {men} men at "
            f"the guns, {marines_at} of them soldiers at the carronades, and {HELM} at the wheel "
            f"leave {total} trimmers (the 74's share of her seamen would be "
            f"{half_up(seamen * share)}); the bill keeps {kept} soldiers in their division."
        )
    for what, name, men, marines_at, n in REPORT.get("fit_bills", ()):
        out.append(
            f"three-decker: fit '{name}': {men} men at one side's guns, {marines_at} of them "
            f"soldiers at the obuses; its own {what}, {n}."
        )
    if "anchors" in REPORT:
        bower, stream, kedge, cable, scable = REPORT["anchors"]
        out.append(
            f"three-decker: anchors: bowers {bower:g} cwt, stream {stream:g}, kedge {kedge:g}; "
            f"bower cables {cable:g} in, stream {scable:g} in."
        )
    return "\n".join(out)


def build(out_dir: str) -> None:
    """Write her file to `out_dir`, `three-decker.yaml`, through `write()`; her design's checks
    raised before it is written."""
    REPORT.clear()
    write(out_dir)
    print(her_report(), file=sys.stderr)
