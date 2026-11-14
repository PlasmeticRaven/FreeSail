"""The British coasting bilander of Gwyn's drawing, with her settee main: the *Hopewell* (package
75, the third ship; her builder B4).

Her design is docs/design/Design-Ship-Bilander.md (cited here as Bil-D), from her research note
docs/design/Research-Bilander-2026-10.md (Bil), the engine's design for her settee
(docs/design/Design-ShipsEngineExtensions.md, Ext, §5) and the decisions it names
(docs/design/Decisions-ShipsRound2-2026-10.md). One module writes one file,
`data/ships/bilander.yaml` (Bil-D decision 1): `particulars()` gives her figures in the file's
frame from the data below and raises in words where a check of Bil-D §1.4 fails, `write(out_dir,
p)` builds and dumps her file, and `build(out_dir)` is the generator's hook (`tools/gen_ships.py`,
`SHIP_MODULES`). Her settee is cut by `tools/ships/settee.py` and her spritsail yard by
`tools/ships/spritsail_yards.py`, each pure.

**Built so far (Bil-D §13, steps 1 to 3).** Her hull block and profile with her shape keys
(§2, §3); her masts and yards (§4.1), her square sails and her settee (§4.2, §4.4), the head with
its two headsails and the spritsail yard with its sail (§4.2, §4.3), the main topmast staysail,
the storm canvas, the groups and the aliases (§4.5); her two fits, unarmed by default and the
armed merchant, its guns on her ports and her rail, its magazine and the quarter bill set against
it (§5); her company of eight, drawn from her wardroom file `data/people/bilander.yaml` (§6), her
stores, ground tackle, boat, pumps and hold (§7); her description at far detail (§8), whose
index rows are hers in `freesail/world/ships.py`.

**The frame (Bil-D §1.4).** x in metres forward of the middle of her load waterline, z in metres
above that waterline, her post and her stem at the water at x = -10.76 and +10.76. The figures
come in the sources' own units and are converted once:
- Chapman 1768 Pl. LXII No. 5 (Bil §2.4, measured on IA leaf 0141 at 9.79 px a Swedish foot):
  English feet as Bil gives them beside the Swedish; the bowsprit's in Swedish feet, as measured.
- Gwyn's drawing (RMG PAG3828, held privately; Bil §2.3 and Bil-D §3.2, §4.1): shares of its
  rail length, stem head to taffrail, 785 px, laid on Chapman's rail length (75.6 ft) upward from
  Chapman's waist rail (5.4 ft above the water). **Plainly:** D6 (e) and Bil §2.3 say "above the
  deck"; Gwyn's masts stand on the drawn rail (Bil-D §1.4), so every Gwyn height is laid from it.
- Steel 1805's brig collier of 170 27/94 tons (Tables p. 26 and the folios, the page images read:
  IA leaves n484 and n488 and the cached right leaves of Folios II, VII, XXXII, LI and LV), in
  Steel's feet and inches, scaled by principle 7 (Build-Ships.md §5.0): lengths by her waterline
  over the collier's length between the perpendiculars, 76 ft 11 in (`COLLIER_LENGTH_FT`), the
  sections by her beam over the collier's extreme breadth, 22 ft 11 in.
A lower spar's `height_m` is its head above her datum, her upper deck at side at x 0, 0.92 m
(D18 (a); Bil-D §2.2); an upper mast's its hoist above the cap below; a sail's `corners_m` above
the datum; a sail's `centre_height_m` above the water.

**Her notes (the lead's notes of 2026-10-29, item 2).** The file's notes carry sources,
departures and judgements. A figure a rule computes from the file's own keys (an area from a cut,
a rating, a rope's scale, a drawn displacement, a port's gap) is printed by `her_report()`, the
generator's report, and held by her tests, where it cannot go stale.

The module is imported only by the generator's entry block, after `gen_ships` is made the running
script, and takes every helper as `g.<name>` (Indf §1.2). No function or table of the generator
is changed; every other file stays byte for byte as it is.

Marks as Bil-D's: measured (off a held image, with its error), read (the page or its image),
judgement. The images are not in the repository.
"""

from __future__ import annotations

import math
import os
import re
import sys
from dataclasses import dataclass

import gen_ships as g

from ships import period, settee, spritsail_yards

FT = g.FT
# The Swedish foot (Bil §2.4: Chapman's scale bar, its three rows in the true ratios of the feet).
SW_FOOT = 0.2969


def metres(feet: float) -> float:
    """English feet to metres, to the centimetre."""
    return round(feet * FT, 2) + 0.0


def sw_metres(feet: float) -> float:
    """Swedish feet to metres, to the centimetre."""
    return round(feet * SW_FOOT, 2) + 0.0


# ---------------------------------------------------------------------------
# Chapman 1768 Pl. LXII No. 5, the "Billender", to the plate's own scale (Bil §2.4, measured;
# D7 (a)): English feet as Bil gives them beside the Swedish. **Plainly:** not scaled by D6 (a)'s
# "about 2%" to 130 tons (Bil-D §2.1; the lead's answer, "unscaled, as picked; 'about 130' holds
# 128").
# ---------------------------------------------------------------------------

LWL_FT = 70.6  # sternpost to stem, 72.5 Swedish ft; +-1.5-2 ft where the stem is read
BREADTH_FT = 19.4  # the two breadth marks, 19.9 Swedish ft; +-1.5%; taken as extreme (judgement)
RAIL_LENGTH_FT = 75.6  # taffrail to stem head, 77.6 Swedish ft; +-2%
WAIST_FT = 5.4  # the rail above the waterline, 5.3-5.5 ft (5.4-5.6 Swedish); +-0.5 ft
OVERALL_FT = 83.0  # taffrail to the head, about 85 Swedish ft (the check on Gwyn's head)
# The overhang between the rail and the water (75.6 less 70.6 ft) split two-thirds abaft the post
# and a third before the stem: measured for her at Bil-D §3.6 task 5 on IA leaf 0141, by the eye
# on a ruled strip (the taffrail 3.9 Swedish ft abaft the post at the water, the stem head 2.0 ft
# before the stem) and by the ink's rows (2.9-3.1 and 1.0-1.6 ft); both two-thirds or more aft,
# two-thirds taken. Bil-D's "half each" was judgement until measured.
OVERHANG_AFT_SHARE = 2.0 / 3.0
# The masts at the rail (Bil §2.4: "use the rail positions"): the main 0.41 of the waterline
# forward of the sternpost (29.7 Swedish ft), the fore 0.148 abaft the stem (10.7 ft; Steel's
# 3/20); the main raking aft about 2.8 degrees, the fore nearly plumb.
MAIN_FROM_POST = 0.41
FORE_FROM_STEM = 0.148
RAKE_DEG = {"fore": 0.0, "main": 2.8}
# The square yards at twice their drawn length (Bil §2.4: the plate's yards are drawn braced at 60
# degrees, "Raernes varkeliga langder aro dubbelt storre"; +-0.6 ft at the ends, +-1.5% in scale).
# The dry yard by the Tractat's rule for brigs, the main yard the fore's (Chapman 1781 p. 102,
# read, Bil §2.4): Chapman draws none on No. 5 (Bil-D §4.1).
YARD_FT = {
    "fore.yard": 40.8,
    "fore.topsail.yard": 30.0,
    "fore.topgallant.yard": 20.1,
    "main.crossjack.yard": 40.8,
    "main.topsail.yard": 30.7,
    "main.topgallant.yard": 20.1,
}
# The bowsprit (Bil §2.4, measured in Swedish feet): 28.5 ft outboard at the stem head, steeved
# about 29 degrees; the jib-boom 15.3 ft beyond the cap. Heavier than the Tractat's rule, 1.15
# times the breadth (22.9 ft) outboard (Chapman 1781 pp. 99-100, read).
BOWSPRIT_OUT_SW = 28.5
BOWSPRIT_STEEVE_DEG = 29.0
JIB_BOOM_BEYOND_SW = 15.3
# Chapman's settee, recorded beside hers (Bil §2.4): its yard 12.45 m at 35 degrees, about 92 m2.
CHAPMAN_SETTEE = {"yard_m": 12.45, "deg": 35.4, "area_m2": 92.0}

# ---------------------------------------------------------------------------
# Gwyn's drawing, PAG3828 (Bil §2.3; Bil-D §3.2, §4.1, §4.4): shares of the drawing's rail
# length, 785 px on the 1560-px image, laid on Chapman's rail length upward from Chapman's
# waist rail.
# Measured on the held image at +-10 px a point (+-0.3 m at her scale), re-measured at her road's
# step 1 by two methods (the eye on ruled strips; each yard's and top's ink run through its mast,
# the yard fitted by least squares): docs/dev/TuningNotes.md, "The bilander (package 75, B4)".
# ---------------------------------------------------------------------------

GWYN_RAIL_PX = 785.0
GWYN_RIG = {  # heights above the waist rail as shares of the rail length (Bil-D §4.1)
    "fore": {
        "yard": 0.276,
        "top": 0.329,
        "cap": 0.396,
        "topsail_yard": 0.580,
        "topmast_cap": 0.669,
        "topgallant_yard": 0.750,
        "truck": 0.85,  # Bil
    },
    "main": {
        "yard": 0.293,  # the dry yard
        "top": 0.35,  # Bil
        "cap": 0.425,
        "topsail_yard": 0.633,
        "topmast_cap": 0.721,
        "topgallant_yard": 0.834,
        "truck": 0.95,  # Bil
    },
}
# The settee (Bil §2.3; Bil-D §4.4; D5 (a)): the head 534 px of 785 at 44 degrees to the
# horizontal (Falconer 1780 and Roding I col. 304 about 45, Bil §1.1); the yard 564 px (557
# re-measured; 566 by the ink's fit at her step 1), cut to the head on her file (below); the tack
# 0.30 m above the waist rail under the throat (Gwyn's tack just above the rail, 0.57 of the length
# from the taffrail against Gwyn's 0.58; measured).
GWYN_SETTEE = {"head_px": 534.0, "yard_px": 564.0, "yard_deg": 44.0, "tack_above_waist_m": 0.30}
# The quarterdeck's break 0.325 of the rail length from the taffrail, abaft the main shrouds (Bil
# §2.3; measured), its rail 0.84 m above the waist rail there and 1.65 m at the taffrail; the bow's
# rail 1.00 m above it at the stem head; the head reaching 1.48 m beyond the stem head (Bil-D
# §3.2; measured on the hull crop at +-10 px).
GWYN_BREAK_FROM_TAFFRAIL = 0.325

# ---------------------------------------------------------------------------
# Lloyd's Register (Bil §2.2, read on the row images): the bilanders of 130 tons, Elizabeth
# drawing 12 ft loaded and the Duke of York of Bristol 11 ft; the mean taken, judgement (D7 (a)).
# ---------------------------------------------------------------------------

LLOYDS_DRAUGHT_FT = (12.0, 11.0)

# ---------------------------------------------------------------------------
# Steel 1805's brig collier of 170 27/94 tons, "Bodies of a Brig Collier" (Tables p. 26, IA leaf
# n484, the page image read twice, at full size and again at 1.25x on other crops, every cell the
# same; each row's fairness along the stations the arithmetic check), the stand-in for her body
# under the water and her breadths by station (Bil-D §3.1, §3.4; Build-Ships.md §5.0 principles 5
# and 7). Feet and inches above the base, the upper edge of the rabbet of the keel; "..." Steel's
# own blank. The table prints no rising line and no breadth sweeps; its "cutting down line" (the
# floors' inner line) is kept as read and not drawn. The fore body's stations from the foremost
# perpendicular (FP), the after body's from the after (AP).
# ---------------------------------------------------------------------------

COLLIER_ROWS = (
    "station",
    "lower_breadth",
    "upper_breadth",
    "top_timber",
    "topside",
    "cutting_down",
    "main_half",
    "top_timber_half",
    "diagonal_1",
    "diagonal_2",
    "diagonal_3",
    "diagonal_4",
)
# The table as read, a timber to a line: its name, then the rows above in their order, each cell
# in feet and inches; the fore body's stations from FP, the after body's from AP.
COLLIER_FORE_TABLE = """
⊕ | 30 0 | 9 7 | 12 1¼ | 16 4 | ... | 1 2 | 11 3 | 10 6 | 8 1 | 13 3 | 17 7 | 17 3½
D | 22 5 | 9 10 | 12 1½ | 16 4½ | ... | 1 2 | 11 3 | 10 6 | 7 11½ | 13 0 | 17 5 | 17 2
F | 18 5 | 10 3 | 12 2½ | 16 6 | 17 3 | 1 3 | 11 3 | 10 6 | 7 8½ | 12 8 | 17 0½ | 16 11
H | 14 5 | 10 9¾ | 12 6 | 16 8 | 17 5½ | 1 6 | 11 1¾ | 10 4½ | 7 3 | 11 11 | 16 2½ | 16 4½
K | 10 5 | 11 8 | 13 0 | 16 11 | 17 9 | 2 2 | 10 8 | 10 2 | 6 3½ | 10 9 | 14 10 | 15 3¾
L | 8 5 | 12 2½ | 13 4¼ | 17 1½ | 17 11¼ | 2 11 | 10 2 | 9 11 | 5 6½ | 9 9 | 13 8¾ | 14 4
M | 6 5 | 12 10 | 13 9 | 17 4 | 18 2¼ | 4 4 | 9 5½ | 9 4½ | 4 6 | 8 6 | 12 3½ | 13 0¾
N | 4 5 | 13 9 | 14 3¼ | 17 8 | 18 6 | ... | 8 1 | 8 4½ | 2 6½ | 6 6 | 10 3½ | 11 2
"""
COLLIER_AFT_TABLE = """
4 | 38 11 | 9 8 | 12 2 | 16 5 | ... | 1 2½ | 11 2¾ | 10 5¼ | 7 11½ | 13 0½ | 17 4½ | 17 2
8 | 30 11 | 10 0¾ | 12 4½ | 16 7¾ | 17 5¼ | 1 4 | 11 1 | 10 3½ | 7 7½ | 12 6 | 16 10 | 16 9½
12 | 22 11 | 10 9 | 12 10¼ | 16 11¾ | 17 9 | 1 7 | 10 10½ | 10 0½ | 6 10 | 11 4¼ | 15 7½ | 16 1
14 | 18 11 | 11 2¾ | 13 2½ | 17 3 | 18 0½ | 1 10 | 10 8¼ | 9 10 | 6 3¾ | 10 7 | 14 9 | 15 5¾
16 | 14 11 | 11 9½ | 13 7½ | 17 6½ | 18 4 | 2 3¼ | 10 5½ | 9 7½ | 5 6½ | 9 7 | 13 9 | 14 9½
18 | 10 11 | 12 6½ | 14 1¾ | 17 10¾ | 18 8 | 2 11¾ | 10 2½ | 9 4¼ | 4 7½ | 8 3½ | 12 5 | 13 9½
20 | 6 11 | 13 5¾ | 14 9 | 18 3½ | 19 0¾ | 4 4¼ | 9 10½ | 9 0 | 3 2½ | 6 6½ | 10 8 | 12 7¼
22 | 2 11 | 14 8¼ | 15 6½ | 18 9½ | 19 7¼ | ... | 9 5½ | 8 7 | 1 3 | 3 9½ | 7 11 | 10 5
"""
# "In the fore and after bodies": each diagonal's height up the middle line, and where it ends,
# its distance out on the base or its height up the side line; the side line taken at the main
# half-breadth of dead flat, 11 ft 3 in out (judgement, as the pages note took the sloop's).
COLLIER_DIAGONALS = (
    ("7 4", ("4 5½", "0 0")),
    ("12 3½", ("7 5¾", "0 0")),
    ("17 5¼", ("10 7¾", "0 0")),
    ("19 8¾", ("11 3", "6 0")),
)
# Folio I (IA leaf n488, the "Brig, tons 170" column, read; the rows' words on n487): C, from the
# fore part of the stem at the wing transom's height to the aft part of the post there, 76 ft 3 in
# (merchant ships); D, the keel for the tonnage, 60 ft 8 in; E, FP to dead flat, 30 ft 0 in; F and
# G, the foremost and after timbers 4 ft 5 in and 2 ft 11 in from their perpendiculars (the table's
# N and 22, to the inch); H, the tread of the keel, the post's aft side to the fore-foot, 66 ft
# 3 in; I, the length extreme, 83 ft 0 in; K and L, the breadth 22 ft 6 in moulded and 22 ft 11 in
# extreme; M, the depth in hold, 10 ft 0 in; N, 170 tons; O and P, the load draught 10 ft 9 in
# afore and abaft; R, S, T and V, the main keel sided 9 1/2, 12 and 9 1/2 in, 11 1/2 in deep. A and
# B (the gun deck, the range of the deck) blank.
COLLIER_FOLIO_I = {
    "C": "76 3",
    "D": "60 8",
    "E": "30 0",
    "F": "4 5",
    "G": "2 11",
    "H": "66 3",
    "I": "83 0",
    "K": "22 6",
    "L": "22 11",
    "M": "10 0",
    "O": "10 9",
    "P": "10 9",
    "R": "0 9½",
    "S": "1 0",
    "T": "0 9½",
    "V": "0 11½",
}
# Her length between the perpendiculars: the after body's room, 2 ft from timber to timber (4 to
# 22), counted from dead flat to timber 4, four rooms, as it holds to an inch on Steel's 36 and
# cutter, whose lengths Folio I prints (ships-design/pages-steel-1805-bodies.md §6): 30 ft 0 in +
# 8 ft 0 in + 38 ft 11 in. Folio I's row C (76 ft 3 in, outside the stem and the post at the wing
# transom's height) is shorter, where on the sloop and the cutter it is longer: on 74 ft (row C
# less her stem's 11 in moulding, Folio II, and a post of about a foot), timber 4 would stand 5 ft
# 1 in abaft dead flat, three timbers in five feet. The stations' length taken (Bil-D §3.4: 0.92,
# so nothing is written again); the conflict for the lead (docs/dev/TuningNotes.md).
COLLIER_LENGTH_FT = 30.0 + 8.0 + 38.0 + 11.0 / 12.0
COLLIER_BREADTH_EXTREME_FT = 22.0 + 11.0 / 12.0
# The plank, a side: half the extreme breadth less the moulded (22 ft 11 in less 22 ft 6 in).
COLLIER_PLANK_FT = 2.5 / 12.0
# The load line above the base: level, 10 ft 9 in afore and abaft from the main keel's underside
# (Folio I, O and P), less half the keel's 11 1/2-in depth, the rabbet "mostly in the middle of the
# depth of the keel" in merchant ships (Folio I's note, read; judgement on the half, as the pages
# note took the sloop's): 10 ft 3 1/4 in.
COLLIER_LOAD_ABOVE_BASE = "10 3¼"
COLLIER_DRAUGHT_FT = 10.75
# Folio II (cached right leaf _0491, the brig of 170 tons, read; the sloop's column the check, 13 ft
# 3 in, 1 ft 0 in and 10 in as the pages note read them): the head of the stem's fore part 20 ft
# 1 in above the rabbet; the stem moulded 11 in and sided 10 in at the head. The stem's centre for
# sweeping (rows L and M) blank for her.
COLLIER_STEM = {"head_above_rabbet": "20 1", "moulded": "0 11", "sided": "0 10"}
# Folio VII (_0501): the main wale's lower edge 11 ft 9 in above the rabbet at the stem, 9 ft
# 9 1/2 in at dead flat, 12 ft 6 in at the after timber; 2 ft 0 in broad, three strakes, 5 in
# thick. Folio XXXII (_0551): the upper deck's plank 2 1/2 in; the waist 3 in deep at the lowest
# place; the upper side of the upper deck beam at the middle line 17 ft 2 in above the rabbet
# afore, 16 ft 6 in at midships, 20 ft 9 in abaft; a rise of 1 ft 0 in deep running 37 ft 0 in
# afore AP, its flat 3 in thick. Folio LI (_0589): the lower counter's touch at the middle line
# 16 ft 0 in above the rabbet, the upper counter's 17 ft 2 in, the upper part of the taffrail
# 22 ft 6 in; the stern 15 ft 8 in broad at the top-timber line; abaft AP the lower counter 2 ft
# 4 in, the upper 3 ft 2 in, the counter timber at the taffrail's height 4 ft 10 in. Folio LV
# (_0597): the sheer rail's upper edge 18 ft 11 in above the rabbet afore, 16 ft 7 in midships,
# 19 ft 11 in abaft; the waist rail 1 ft 1 in below it. The checks, recorded beside her own
# lines (each read with the sloop's column, as the pages note gives it, the check on the column).
COLLIER_WALE = {"stem": "11 9", "dead_flat": "9 9½", "after": "12 6", "broad": "2 0"}
COLLIER_DECK_MIDSHIPS = "16 6"
COLLIER_WAIST = "0 3"
COLLIER_TAFFRAIL = "22 6"
COLLIER_STERN_BREADTH = "15 8"
COLLIER_SHEER_RAIL = {"afore": "18 11", "midship": "16 7", "abaft": "19 11"}
# Steel 1805's brigantine of 10 guns, Folio XXXII (_0551, read): the plank to the port sills 1 ft
# 6 in; the ports 1 ft 5 in deep and 2 ft 0 in fore and aft (Bil-D §3.6 task 7: the check on her
# armed fit's ports, which stand cut down from her rail).
BRIGANTINE_PORT = {"sill_above_plank": "1 6", "deep": "1 5", "fore_and_aft": "2 0"}


def collier_table(text: str) -> dict[str, dict[str, float | None]]:
    """A body of the collier's table as read: {timber: {row: feet, None for Steel's blank}}."""
    out = {}
    for line in text.strip().splitlines():
        name, *cells = (c.strip() for c in line.split("|"))
        out[name] = {
            row: None if v == "..." else g.feet_and_inches(v)
            for row, v in zip(COLLIER_ROWS, cells, strict=True)
        }
    return out


COLLIER_FORE = collier_table(COLLIER_FORE_TABLE)
COLLIER_AFT = collier_table(COLLIER_AFT_TABLE)

# ---------------------------------------------------------------------------
# Her own figures: the file's frame
# ---------------------------------------------------------------------------

LWL = LWL_FT * FT
HALF = LWL / 2.0
RAIL_LENGTH = RAIL_LENGTH_FT * FT
WAIST = WAIST_FT * FT
OVERHANG = RAIL_LENGTH - LWL
TAFFRAIL_X = round(-HALF - OVERHANG_AFT_SHARE * OVERHANG, 2) + 0.0
STEM_HEAD_X = round(HALF + (1.0 - OVERHANG_AFT_SHARE) * OVERHANG, 2) + 0.0
# Her datum (D18 (a); Bil-D §2.2): her upper deck at side at x 0, flush from the stem to the
# taffrail under the raised quarterdeck (judgement: Chapman's rail less a merchant's waist).
DATUM = 0.92


def gwyn_z(share: float) -> float:
    """A Gwyn height above her water: Gwyn's share of the rail length laid upward from Chapman's
    waist rail on Chapman's rail length (Bil-D §1.4)."""
    return round(WAIST + share * RAIL_LENGTH, 2) + 0.0


def from_taffrail(share: float) -> float:
    """A Gwyn place fore and aft: Gwyn's share of the rail length forward of the taffrail."""
    return round(TAFFRAIL_X + share * RAIL_LENGTH, 2) + 0.0


def above_datum(z_water: float) -> float:
    """A height above her water as a height above her datum."""
    return round(z_water - DATUM, 2) + 0.0


def _rail_station_x(name: str, z_water: float) -> float:
    """The x of a lower mast's line at a height above her water, from Chapman's station at the
    rail and the rake (Bil-D §2.1)."""
    at_rail = -HALF + MAIN_FROM_POST * LWL if name == "main" else HALF - FORE_FROM_STEM * LWL
    return at_rail - math.tan(math.radians(RAKE_DEG[name])) * (z_water - WAIST)


# Each lower mast's x as filed, at her datum (the engine's mast line runs from x_m at the datum
# by the rake): Chapman's station at the rail carried down by the rake.
MAST_X = {name: round(_rail_station_x(name, DATUM), 2) + 0.0 for name in ("fore", "main")}


def mast_x_at(name: str, z_water: float) -> float:
    """The x of a lower mast's line at a height above her water, as the engine draws it from the
    file: its x_m at the datum carried by its rake."""
    return MAST_X[name] - math.tan(math.radians(RAKE_DEG[name])) * (z_water - DATUM)


# The rig's heights above her water (Bil-D §4.1), by mast; the yards' lengths.
RIG_Z = {mast: {k: gwyn_z(v) for k, v in levels.items()} for mast, levels in GWYN_RIG.items()}
YARD_M = {k: metres(v) for k, v in YARD_FT.items()}

# ---------------------------------------------------------------------------
# The hull block (Bil-D §2.1)
# ---------------------------------------------------------------------------

DRAUGHT_FT = sum(LLOYDS_DRAUGHT_FT) / len(LLOYDS_DRAUGHT_FT)
CB = 0.50  # the brig's block (judgement, D7 (a): "by the brig file's methods")
BRIG_LWL_FT = 88.0  # the brig in the generator: 0.93 of her 95-ft gun deck
BRIG_HULL_SPEED_KN = 11.5
BRIG_CLR_X_M = 0.5
# Her centre of lateral resistance as tuned at her step 4 (Bil-D §9's second knob, the house's way:
# her helm sailed under plain sail in 15 kn at seed 7): from the brig's 0.5 m as a share of her
# waterline, +0.40, to +2.0, the most weather helm, on her step 4's grid of a quarter metre, her
# heave-to keeps her lying to within the heave-to's four to seven points in 8 to 25 kn, the
# polar's winds (judgement on the measures; docs/dev/TuningNotes.md, her section). Her step 4 took
# +2.25 on 10 to 25 kn; her review found her forced round through the wind hove to in 8 kn there
# (and at +2.2), and lying to at +2.0 to +2.15 from 6 to 9 kn. Her drawn lateral plane's centroid
# stands at x -0.23 (recorded).
CLR_X_M = 2.0
FRIGATE_GM_FT = 4.25  # 4 ft 3 in, the frigate's (the brig's method)
FRIGATE_BEAM_FT = 38.3


def hull_figures() -> dict:
    """Her hull block, the house's keys in its order (Bil-D §2.1)."""
    lwl, beam, draught = LWL, BREADTH_FT * FT, DRAUGHT_FT * FT
    return {
        "length_waterline_m": round(lwl, 2),
        "beam_m": round(beam, 2),
        "draught_m": round(draught, 2),
        "displacement_kg": round(lwl * beam * draught * CB * 1025.0, -3),
        "gm_m": round(FRIGATE_GM_FT * BREADTH_FT / FRIGATE_BEAM_FT * FT, 2),
        "clr_x_m": CLR_X_M,
        "lateral_area_m2": round(round(lwl, 2) * round(draught, 2) * 0.85, 1),
        "hull_speed_kn": round(BRIG_HULL_SPEED_KN * math.sqrt(LWL_FT / BRIG_LWL_FT), 1),
        "deck_height_m": DATUM,
        "rudder": {"area_m2": 2.4, "max_angle_deg": 35, "rate_deg_s": 3.5, "span_m": 3.2},
    }


def burthen(length_ft: float) -> float:
    """Tons by the old measure, (L - 3/5 B) x B x B/2 / 94, on her breadth (Bil-D §2.1)."""
    return (length_ft - 0.6 * BREADTH_FT) * BREADTH_FT * BREADTH_FT / 2.0 / 94.0


# D6 (a)'s "about 130", the register's bilanders of 120-140 tons (Bil §2.2): 118 tons on her
# waterline and 128 on her taffrail-to-stem-head length, the rule's length between them.
BURTHEN_BAND = (118.0, 130.0)

HULL_NOTES = {
    "length_waterline_m": "70.6 ft, Chapman 1768 Pl. LXII No. 5 sternpost to stem (72.5 Swedish "
    "ft at the plate's own scale, +-1.5 to 2 ft where the stem is read; Research-Bilander-2026-10"
    ".md §2.4, measured), D7 (a). Plainly: not scaled by D6 (a)'s 'about 2%' to 130 tons, a "
    "factor no source gives and inside the plate's own error (her design's §2.1).",
    "beam_m": "19.4 ft, No. 5's two breadth marks (19.9 Swedish ft, +-1.5%), taken as extreme "
    "(judgement: the marks do not say).",
    "draught_m": "11.5 ft to the keel's lower edge (D29 (b)'s convention): Lloyd's draught loaded "
    "for the two bilanders of 130 tons, 12 ft for Elizabeth and 11 ft for the Duke of York of "
    "Bristol (read on the row images); the mean, judgement. The register's key (1781) does not "
    "say whether the column is the mean or the greatest. Steel 1805's brig collier of 170 tons "
    "draws 10 ft 9 in afore and abaft (Folio I, read), less than the register's bilanders of 130: "
    "the register's column perhaps the greatest draught deep laden (judgement). Chapman draws no "
    "draught.",
    "displacement_kg": "LWL x beam x draught x Cb 0.50 x 1025, the brig file's method (D7 (a)); Cb "
    "the brig's, judgement. The drawn hull's displacement is beside it in the generator's "
    "report, never in its place (Build-Ships.md §5.0 principle 8).",
    "gm_m": "The brig's method: the frigate's 4 ft 3 in scaled by the breadth, 19.4 against 38.3 "
    "ft. Judgement; a deep-laden coaster.",
    "clr_x_m": "Tuned for her helm (her design's §9, the second knob) as the house tunes it, her "
    "helm sailed under plain sail in 15 kn: from the brig's 0.5 m as a share of her waterline "
    "(+0.40, 0.019 L), where she carried 12.2 degrees of lee helm at 60 degrees off the wind and "
    "4.1 abeam, to +2.0, where she carries 4.0 degrees of lee helm at 60 degrees, 2.1 at 67.5 "
    "and 1.1 abeam. The house's little weather helm close-hauled wants about +3.0 (balanced "
    "there), where hove to she comes head to wind and makes sternway; +2.0 is the most, by "
    "quarter metres, her heave-to keeps her lying to within four to seven points in 8 to 25 kn, "
    "the polar's winds (judgement on the measures; at +2.25 she was forced round through the wind "
    "hove to in 8 kn). Her drawn lateral plane's centroid is at x -0.23; the figure is the "
    "engine's balance, not a drawn point.",
    "lateral_area_m2": "LWL x draught x 0.85, the brig's rule.",
    "hull_speed_kn": "D24 (a): the brig's 11.5 kn by the root of the waterlines, 70.6 over 88 ft. "
    "No period speed exists for a bilander (Research-Bilander-2026-10.md §4); within 9.8 to "
    "10.8 kn if her polar wants it (her design's §9, the third knob). Kept at her step 4: her "
    "closest and her beat hold the brig's 50 and 60 degrees across the whole band, so nothing "
    "asks a move.",
    "deck_height_m": "Her upper deck at side at x 0 (D18 (a); Build-Ships.md §5.5), flush from the "
    "stem to the taffrail under the raised quarterdeck: Chapman's rail less a merchant's waist of "
    "about 2 ft 5 in (judgement). Steel 1805's coasting sloop floats with her deck 3 ft 0 1/2 in "
    "above the water at dead flat, the like freeboard. Steel's brig collier, the stand-in for her "
    "body, has her deck nearly at her top-timber line, its waist 3 in deep at the lowest place "
    "(Folio XXXII, read): a collier's flush deck, the check that does not hold (recorded; the "
    "datum stands).",
    "rudder": "The brig's blade by her length and draught (judgement): 2.4 m2, its span 3.2 m; 35 "
    "degrees the period stop.",
}

# ---------------------------------------------------------------------------
# The collier scaled: her stand-in's stations, breadths and sections (Bil-D §3.1, §3.4)
# ---------------------------------------------------------------------------

LENGTH_RATIO = LWL_FT / COLLIER_LENGTH_FT
BEAM_RATIO = BREADTH_FT / COLLIER_BREADTH_EXTREME_FT
LOAD_ABOVE_BASE_FT = g.feet_and_inches(COLLIER_LOAD_ABOVE_BASE)


def collier_timbers() -> list[tuple[str, float, dict]]:
    """The collier's timbers aft to forward: (name, x forward of its mid-perpendiculars in its
    own feet, the row's cells in feet)."""
    half = COLLIER_LENGTH_FT / 2.0
    out = [(name, row["station"] - half, row) for name, row in COLLIER_AFT.items()]
    out += [(name, half - row["station"], row) for name, row in COLLIER_FORE.items()]
    return sorted(out, key=lambda t: t[1])


def collier_rows() -> dict:
    """The collier's table as `g.from_steel_table` takes it, the plank put on every half-breadth
    and every diagonal's length (2 1/2 in a side, Folio I's extreme less its moulded breadth), so
    that the stand-in is drawn to the outside of the plank as her beam is (judgement)."""
    plank = COLLIER_PLANK_FT
    timbers = []
    for name, x_ft, row in collier_timbers():
        reaches = [
            None if row[f"diagonal_{i}"] is None else row[f"diagonal_{i}"] + plank
            for i in range(1, 5)
        ]
        timbers.append(
            [
                name,
                x_ft * FT,
                row["lower_breadth"],
                row["upper_breadth"],
                row["main_half"] + plank,
                reaches,
            ]
        )
    half_m = COLLIER_LENGTH_FT * FT / 2.0
    return {
        "water": [[-half_m, COLLIER_LOAD_ABOVE_BASE], [half_m, COLLIER_LOAD_ABOVE_BASE]],
        "diagonals": [[h, [out, up]] for h, (out, up) in COLLIER_DIAGONALS],
        "timbers": timbers,
    }


def diagonal_point(i: int, length_ft: float) -> tuple[float, float]:
    """A point `length_ft` down the collier's `i`th diagonal (1 the first), as (half-breadth,
    height above the base), feet, as `g.from_steel_table` lays it."""
    h, (out, up) = COLLIER_DIAGONALS[i - 1]
    h = g.feet_and_inches(h)
    vy, vz = g.feet_and_inches(out), g.feet_and_inches(up) - h
    n = math.hypot(vy, vz)
    return length_ft * vy / n, h + length_ft * vz / n


def collier_section_ft(row: dict) -> list[tuple[float, float]]:
    """A timber's section in the collier's feet, (height above the base, half-breadth) low to
    high, the plank on: its diagonals' points, its lower and upper heights of breadth at the main
    half-breadth, and the top-timber line at its half-breadth."""
    plank = COLLIER_PLANK_FT
    pts = []
    for i in range(1, 5):
        d = row[f"diagonal_{i}"]
        if d is not None:
            y, z = diagonal_point(i, d + plank)
            pts.append((z, y))
    main = row["main_half"] + plank
    pts += [(row["lower_breadth"], main), (row["upper_breadth"], main)]
    pts.append((row["top_timber"], row["top_timber_half"] + plank))
    out: list[tuple[float, float]] = []
    for z, y in sorted(pts):
        if out and z <= out[-1][0] + 1e-9:
            continue
        out.append((z, y))
    return out


def collier_half_breadth(x: float, z: float) -> float:
    """The collier's half-breadth, scaled, at her x and her height above the water: each timber's
    section at that height (its points joined straight, judgement: the table prints no breadth
    sweep, so the diagonals' points are joined straight as the pages note joined the sloop's),
    straight between the two timbers about the x (judgement)."""
    from freesail.ship.profile import interp

    z_ft = LOAD_ABOVE_BASE_FT + z / FT / BEAM_RATIO
    line = [
        (x_ft * FT * LENGTH_RATIO, interp(collier_section_ft(row), z_ft))
        for _name, x_ft, row in collier_timbers()
    ]
    return interp(line, x) * FT * BEAM_RATIO


def collier_breadth() -> list[list[float]]:
    """`breadth_m` from the collier, scaled: at each timber her half-breadth at the water and at
    the top-timber line, x by the length ratio, the half-breadths by the beam ratio."""
    from freesail.ship.profile import interp

    out = []
    for _name, x_ft, row in collier_timbers():
        sec = collier_section_ft(row)
        out.append(
            [
                x_ft * FT * LENGTH_RATIO,
                interp(sec, LOAD_ABOVE_BASE_FT) * FT * BEAM_RATIO,
                sec[-1][1] * FT * BEAM_RATIO,
            ]
        )
    return out


def dead_flat_section() -> list[list[float]]:
    """`section_m`: the collier's dead flat scaled, [z above her water, half-breadth] low to high:
    the keel's edge at the rabbet, its half-siding the main keel's (Folio I, S); the diagonals'
    points and the heights of breadth; the top-timber line's half-breadth carried up to Chapman's
    rail, her side above the water her own source's (principle 7)."""
    sec = collier_section_ft(COLLIER_FORE["⊕"])
    keel_half = g.feet_and_inches(COLLIER_FOLIO_I["S"]) / 2.0
    pts = [(0.0, keel_half), *sec[:-1]]
    out = [[(z - LOAD_ABOVE_BASE_FT) * FT * BEAM_RATIO, y * FT * BEAM_RATIO] for z, y in pts]
    out.append([WAIST, sec[-1][1] * FT * BEAM_RATIO])
    return out


def rabbet_line() -> list[list[float]]:
    """`rabbet_m`, kept and not drawn (Build-Ships.md §5.0 principle 11): the keel's rabbet at the
    collier's base, the tables' "upper edge of rabbet" (its load line 10 ft 3 1/4 in above it),
    scaled, from the post to the fore-foot along `keel_m`; its half-sidings the main keel's,
    Folio I's R, S and T (afore, midships, abaft: 9 1/2, 12 and 9 1/2 in) at her beam ratio, at
    the fore-foot, the dead flat and the post."""
    z = round(-LOAD_ABOVE_BASE_FT * FT * BEAM_RATIO, 2) + 0.0
    forefoot = POST[0][0] + metres(g.feet_and_inches(COLLIER_FOLIO_I["H"])) * LENGTH_RATIO
    from_middle_ft = COLLIER_LENGTH_FT / 2.0 - g.feet_and_inches(COLLIER_FOLIO_I["E"])
    dead_flat = from_middle_ft * FT * LENGTH_RATIO
    out = []
    for x, row in ((POST[0][0], "T"), (dead_flat, "S"), (forefoot, "R")):
        half = g.feet_and_inches(COLLIER_FOLIO_I[row]) / 2.0 * FT * BEAM_RATIO
        out.append([round(x, 2) + 0.0, z, round(half, 2) + 0.0])
    return out


def collier_drawn_depth() -> float:
    """The collier's depth to its keel's underside at her scale: its 10 ft 9 in by the beam ratio
    (principle 7), drawn, and recorded beside her draught, never moved (Bil-D §3.4)."""
    return round(COLLIER_DRAUGHT_FT * FT * BEAM_RATIO, 2) + 0.0


def collier_checks() -> dict:
    """The collier's folios at her scale above her water (Bil-D §3.4, §3.6 task 1), each for the
    report beside her own line, never in it."""

    def up(feet):
        return (feet - LOAD_ABOVE_BASE_FT) * FT * BEAM_RATIO

    def read(v):
        return up(g.feet_and_inches(v))

    broad = g.feet_and_inches(COLLIER_WALE["broad"]) * FT * BEAM_RATIO
    wale = read(COLLIER_WALE["dead_flat"])
    top_timber = COLLIER_FORE["⊕"]["top_timber"]
    return {
        "the top-timber line at dead flat": up(top_timber),
        "the deck at side at dead flat (the top-timber line less the waist)": up(
            top_timber - g.feet_and_inches(COLLIER_WAIST)
        ),
        "the sheer rail afore, midship and abaft": tuple(
            read(v) for v in COLLIER_SHEER_RAIL.values()
        ),
        "the main wale at dead flat, its lower and upper edges": (wale, wale + broad),
        "the upper part of the taffrail": read(COLLIER_TAFFRAIL),
        "the stern's half-breadth at the top-timber line": (
            g.feet_and_inches(COLLIER_STERN_BREADTH) / 2.0 * FT * BEAM_RATIO
        ),
    }


# ---------------------------------------------------------------------------
# Her lines (Bil-D §3.2): Gwyn's sheer on Chapman's waist; the collier's body under the water
# ---------------------------------------------------------------------------

# Gwyn's sheer, heights above the waist rail (Bil-D §3.2, measured on the hull crop at +-10 px):
# the quarterdeck's light rail 1.65 m up at the taffrail, 1.30 m at 0.153 of the length from it
# and 0.84 m at its break, 0.325 of the length from the taffrail, abaft the main shrouds (Bil
# §2.3); the waist rail 0.10 m up just forward of the break, Chapman's at x 0.12, 0.07 m up at x
# 4.0, 0.25 m at the fore mast and 0.65 m at x 10.0; the bow's rail 1.00 m up at the stem head.
QD_RAIL = ((0.0, 1.65), (0.153, 1.30), (GWYN_BREAK_FROM_TAFFRAIL, 0.84))
BREAK_STEP_M = 0.10  # the break's step fore and aft (judgement, drawn)
WAIST_RAIL = ((0.12, 0.0), (4.00, 0.07), (None, 0.25), (10.00, 0.65))  # None: the fore mast
BOW_RISE_M = 1.00
WAIST_AT_BREAK_M = 0.10
# The post raking about 7 degrees to the water (judgement; the collier's post is on Folio IV, not
# fetched): its heel at x -10.40, -10.62 at 1.30 m below the water. The counter from the post at
# the water to the taffrail, rounded (Gwyn's stern view, at the measured overhang): shares of the
# overhang abaft the post at 1.20 and 2.20 m above the water (Bil-D §3.2's points, carried to the
# measured overhang).
POST = ((-10.40, None), (-10.62, -1.30))
COUNTER = ((0.513, 1.20), (0.842, 2.20))
# The stem above the water: raking forward from the water to the stem head, a share of the
# measured overhang at 1.40 m (Bil-D §3.2's bluff merchant's stem, carried to the overhang).
STEM_ABOVE = (0.513, 1.40)
# The keel: level at the collier's depth scaled, from the post's heel forward by the collier's
# tread of the keel (Folio I, H: 66 ft 3 in, the post's aft side to the fore-foot), scaled by the
# length ratio; the fore-foot rounded up to the stem at the water as a quarter ellipse (judgement:
# the collier's stem is not printed for her, Folio II's rows L and M being blank).
FOREFOOT_STEPS_DEG = (30.0, 60.0)
# Gwyn's wale, hung from Chapman's waist rail (Bil-D §3.2) and so measured from the drawing's own
# waist rail at the same x: its top 33 px below the rail's top and 25 px broad, in the waist,
# carried along the sheer by Bil-D §3.2's points. Re-measured at her review (2026-11-08) by two
# methods: the ink's luminance down thirteen clean columns (x 730-940; the rail's top at y 963-973,
# the wale's top 32 or 33 px under it at every column but one, 29; the median 33), and the eye on
# a ruled crop at midships (31-34 px). Her step 1 had laid 39 px from y 961, the masts' feet and
# the datum of her rig's heights, where the rail the wale hangs from is drawn at y 968-969 between
# the masts: two reference lines mixed. Bil-D's first reading, 26 and 20 px, lies within its
# +-10 px of this. At Chapman's scale the band's lower edge stands 0.06 m under her water at
# midships, where Gwyn draws about 5 px of side under it before the sea: the drawing's vertical
# scale is not its horizontal (Bil-D §18 item 8). The collier's main wale, Folio VII at her
# scale, -0.12 to 0.39 m at dead flat, lies lower still (the generator's report).
WALE_TOP_BELOW_WAIST_PX = 33.0
WALE_BROAD_PX = 25.0
WALE_RISE = ((-10.00, 0.31), (-4.00, 0.06), (0.12, 0.0), (4.00, 0.07), (10.00, 0.65))
# Her decks at side (Bil-D §3.2, judgement): the upper deck the waist rail less 0.73 m along the
# sheer, its after end 0.01 m inside the counter's line at its height, as Bil-D's (-11.20, 1.45)
# stood against its counter at -11.21 (her review: laid 0.32 m inside the taffrail, the end had
# moved 0.26 m aft with the taffrail where the counter at that height moved 0.13 m, and stood
# 0.10 m outside the drawn hull), and 0.32 m inside the stem head forward; the quarterdeck at
# Gwyn's planksheer, raised about 1.25 m above the upper deck at its break.
UPPER_DECK = ((None, 1.45), (-4.00, 1.00), (0.12, 0.92), (4.00, 0.99), (None, 1.17), (-0.32, 1.85))
DECK_INSIDE_COUNTER_M = 0.01
QUARTERDECK = ((0.32, 2.80), (None, 2.25))
# The armed fit's ports (Bil-D §3.2, §5.2; the owner's answer: "cutouts in the gunwale"): two a
# side in the waist at x 1.0 and 4.0 (judgement), sills the deck + 16 in (after the Raven's,
# Steel 1805 p. lix; judgement), 0.50 m by 0.30 m cut down from the rail (judgement; Steel's
# brigantine of 10 guns cuts 2 ft by 1 ft 5 in, 1 ft 6 in above the plank: Folio XXXII, read,
# the check, which her rail cannot hold).
PORTS_X = (1.00, 4.00)
SILL_ABOVE_DECK_M = 16.0 * 0.0254
PORT_SIZE = (0.50, 0.30)
# The head (Bil-D §3.2): Gwyn's knee and figure from the stem 0.50 m above the water, reaching
# 0.88 m beyond the stem head at 1.80 m and 1.48 m beyond it at 2.70 m (measured).
HEAD = ((None, 0.50), (0.88, 1.80), (1.48, 2.70))
# Gwyn's separate stern view (Bil §2.3, read; Bil-D §3.2, measured on the stern view at +-5 px,
# scaled to her taffrail's 3.30 m): rounded, three oval lights on a blue ground in one band.
LIGHTS = (1.75, 2.75, 3, 1.10)
# Her round counter's half-breadths (the lead's ruling (11) of 2026-11-09:
# `form.stern.counter_hb_m`, freesail/ship/form.py): Gwyn's stern view gives her rail 1.55 m off
# the middle line at the taffrail and 2.02 m at the wale (her step 1 and her review, measured at
# her scale; Bil-D's 2.05), the collier's stern 2.02 m a side at the top-timber line (Folio LI)
# the check. Filed at the taffrail's height and at the wale's middle at its after end (judgement
# on the height: the band's 0.25 to 0.99 m at x -10.0); the counter's foot the water, where the
# post meets it.
COUNTER_AT_WALE_M = 2.02
COUNTER_AT_TAFFRAIL_M = 1.55

MARKS = {
    "rail_m": "stand-in",  # Gwyn's sheer at Chapman's scale; the overhang measured
    "breadth_m": "stand-in",  # the collier, scaled
    "keel_m": "judged",  # the post's heel; its depth the collier's, its fore-foot its tread
    "stem_m": "judged",  # the fore-foot's curve; above the water the measured rake
    "stern_m": "judged",  # the post's rake and the counter
    "wales_m": "stand-in",  # Gwyn at Chapman's scale
    "section_m": "stand-in",  # the collier's dead flat, Chapman's rail
    "decks_m": "judged",
    "ports_m": "judged",
    "port_size_m": "judged",
    "head_m": "stand-in",  # Gwyn at Chapman's scale
    "rabbet_m": "judged",  # the rabbet's place in the keel's depth
    "breadth_line_m": "stand-in",
    "sections_m": "stand-in",
    "form.fullness": "judged",
    "form.stern": "sourced",
    "form.stern.counter_hb_m": "stand-in",
    "form.stern.lights_m": "stand-in",
    "form.head": "sourced",
}

PROFILE_NOTES = {
    "profile": "Her lines (Build-Ships.md §5.0-§5.3; her design's §3): above the water Chapman "
    "1768 Pl. LXII No. 5 at the plate's own scale (her side, her length, her masts) with Gwyn's "
    "sheer, raised quarterdeck, wale, head and stern on it (RMG PAG3828, measured and laid on "
    "Chapman's rail length); under the water Steel 1805's brig collier of 170 27/94 tons (Tables "
    "p. 26, the page image read), her type's nearest table, no lines of any bilander existing: "
    "lengths by her waterline over the collier's 76 ft 11 in between the perpendiculars, the "
    "sections by her beam over its 22 ft 11 in extreme breadth, so that its floor, tumblehome and "
    "flare keep their angles (principle 7). The drawn depth and displacement are recorded beside "
    "her draught and displacement in the generator's report, never moved (principle 8).",
    "profile.rail_m": "The top of the side, taffrail to stem head. The waist Chapman's, 5.4 ft "
    "above the water (5.3 to 5.5 ft, measured); above it Gwyn's rise at Chapman's scale: the "
    "quarterdeck's light rail on stanchions from its break, 0.325 of the length from the "
    "taffrail, up to the taffrail, and the bow's rise to the stem head (measured on the hull "
    "crop). The taffrail and the stem head stand beyond the water's ends by Chapman's overhang, "
    "75.6 less 70.6 ft, two-thirds abaft the post and a third before the stem (measured on the "
    "plate by two methods). Chapman's own sheer, read roughly, rises 2.7 ft forward and 3.6 ft "
    "aft (the check). Stand-in: Gwyn's metres rest on Chapman's scale.",
    "profile.breadth_m": "The collier's half-breadths at its load line and at its top-timber line "
    "by timber, the plank on (2 1/2 in a side, Folio I's extreme less its moulded breadth), "
    "scaled; the half-breadth at the water straight between the table's points that bracket it, "
    "the table printing no breadth sweep (judgement, as the pages note took the sloop's). Its "
    "load line 10 ft 3 1/4 in above the base: 10 ft 9 in afore and abaft from the keel's "
    "underside (Folio I), less half the keel's depth (judgement on the rabbet). Abaft the "
    "aftermost timber the side closes along the post and the counter to the middle line, the "
    "round stern's closure, held out over the counter to its half-breadths: Gwyn's stern view "
    "gives her rail 1.55 m off the middle line at the taffrail and 2.02 m at the wale, her "
    "lights spread +-1.22 m (measured at her scale), and the collier's stern is 15 ft 8 in "
    "broad (Folio LI). No station abaft the post can be filed here, a half-breadth of nothing at "
    "the water being refused: the counter's are filed in form.stern.counter_hb_m and drawn by "
    "it (the generator's report).",
    "profile.keel_m": "Level at the collier's depth to its keel's underside, scaled; from the "
    "post's heel (judged) forward by the collier's tread of the keel, Folio I's 66 ft 3 in, "
    "scaled. Her file's draught, 11.5 ft, is deeper, recorded and never moved (principle 7). "
    "Judged: the post's heel.",
    "profile.stem_m": "The stem's fore edge: from the fore-foot, a quarter ellipse up to the water "
    "(judgement: Folio II prints no centre for the collier's stem), then raking forward to the "
    "stem head by the measured overhang, a bluff merchant's stem (judgement on its curve). Its "
    "top is the stem head, the bowsprit's root.",
    "profile.stern_m": "The post raking about 7 degrees to the water (judgement: the collier's "
    "post is on Folio IV, not fetched), then the round counter to the taffrail at the measured "
    "overhang (Gwyn's stern view; judgement on its curve).",
    "profile.wales_m": "Gwyn's dark band at Chapman's scale, hung from Chapman's waist rail: its "
    "top 33 px below the drawing's own waist rail at the same x and 25 px broad in the waist "
    "(measured by two methods), carried along the sheer (judgement). Its lower edge stands at "
    "her water at midships, where Gwyn draws a strip of side under it before the sea: the "
    "drawing's vertical scale is not its horizontal. The collier's main wale, Folio VII, lower "
    "still at her scale, is the check (the generator's report).",
    "profile.section_m": "The collier's dead flat, scaled, the plank on: the keel's edge at the "
    "rabbet, its half-siding the collier's keel's (Folio I, S); its diagonals' points and its "
    "heights of breadth; its top-timber half-breadth carried up to Chapman's rail, her side above "
    "the water her own source's (principle 7).",
    "profile.decks_m": "Her upper deck at side the waist rail less 0.73 m along the sheer, flush "
    "from the counter, its after end just inside the counter's line, to the stem head; the "
    "quarterdeck at Gwyn's planksheer, raised about 1.25 m above it at its break (judgement "
    "both). The collier's deck stands nearly at its top-timber line, its waist 3 in deep (Folio "
    "XXXII): no check on a vessel with a raised quarterdeck.",
    "profile.ports_m": "The armed fit's ports, two a side in the waist (her design's §5.2; the "
    "owner's 'cutouts in the gunwale'): invented for the fit, Gwyn drawing her unpierced. Sills "
    "the deck + 16 in (judgement, after the Raven's, Steel 1805 p. lix); each half-breadth the "
    "collier's at the sill at that x, scaled, never the drawing's (principle 8).",
    "profile.port_size_m": "0.50 m by 0.30 m, cut down from the rail, which it does not reach "
    "(judgement). Steel 1805's brigantine of 10 guns cuts 2 ft by 1 ft 5 in, 1 ft 6 in above the "
    "plank (Folio XXXII, read): the check, whose depth her rail cannot hold.",
    "profile.head_m": "Gwyn's knee and figure, from the stem 0.50 m above the water to 1.48 m "
    "beyond the stem head (measured). Chapman's 'overall to the head', 83 ft, would put it about "
    "2.3 m beyond: the check, recorded.",
    "profile.rabbet_m": "Kept and not drawn (principle 11): the keel's rabbet at the collier's "
    "base, the tables' upper edge of the rabbet, scaled, along the keel from the post to the "
    "fore-foot; its half-sidings the main keel's, sided 9 1/2, 12 and 9 1/2 in afore, midships "
    "and abaft (Folio I, read), at her beam ratio. Judged: the rabbet's place in the keel's depth, "
    "half of it in merchant ships by Folio I's note.",
    "profile.breadth_line_m": "The collier's upper height of breadth at its main half-breadth by "
    "timber, the plank on, through g.from_steel_table (Build-Ships.md §5.3), scaled.",
    "profile.sections_m": "The collier's diagonals and its lower height of breadth by timber, the "
    "plank on, through g.from_steel_table, scaled. The table prints no rising line, so no "
    "floor_m is written (principle 11 keeps what is found; nothing is).",
    "profile.form": "No fullness beyond the default rule: the collier's sections draw the ends "
    "(principle 5).",
    "profile.form.stern": "Round, closed to the middle line (Gwyn's separate stern view, read): "
    "three oval lights in one band on a blue ground, a red band below, the rudder; the band's "
    "heights and spread measured on the stern view, scaled to her taffrail. Her round counter "
    "1.55 m a side at the taffrail and 2.02 m at the wale (measured on the stern view at her "
    "scale), filed at the taffrail's height and the wale's middle at its after end (judgement) "
    "in counter_hb_m, the counter's foot the water; the round's depth is the drawing's rule "
    "(freesail/ship/form.py). Her carving and "
    "paint in words: the blue stern and red band; an oval carved badge on each quarter in "
    "scrollwork (read on the hull crop); the red ensign on a staff at the taffrail.",
    "profile.form.head": "A figure with head rails (Gwyn, read).",
    "profile.marks": "Each line's rung (Build-Ships.md §5.0 principles 3 and 4): sourced, her own "
    "drawing; stand-in, S†, her type's plate or table at her scale; judged, a judgement at its "
    "weakest point, which its note names.",
}


def break_x() -> float:
    """The quarterdeck's break, Gwyn's share of the rail length forward of the taffrail."""
    return from_taffrail(GWYN_BREAK_FROM_TAFFRAIL)


def rail_line() -> list[list[float]]:
    """`rail_m`: the quarterdeck's rail from the taffrail to its break, the step down to the waist
    rail, and the waist rail on to the stem head (Bil-D §3.2)."""
    out = [[from_taffrail(share), WAIST + up] for share, up in QD_RAIL]
    out.append([break_x() + BREAK_STEP_M, WAIST + WAIST_AT_BREAK_M])
    for x, up in WAIST_RAIL:
        out.append([MAST_X["fore"] if x is None else x, WAIST + up])
    out.append([STEM_HEAD_X, WAIST + BOW_RISE_M])
    return out


def stem_line(depth: float) -> list[list[float]]:
    """`stem_m`, low to high: the fore-foot by the collier's tread, its quarter ellipse up to the
    water, the stem above it raking to the stem head."""
    forefoot = POST[0][0] + metres(g.feet_and_inches(COLLIER_FOLIO_I["H"])) * LENGTH_RATIO
    run = HALF - forefoot
    out = [[forefoot, -depth]]
    for deg in FOREFOOT_STEPS_DEG:
        t = math.radians(deg)
        out.append([forefoot + run * math.sin(t), -depth * math.cos(t)])
    fore_overhang = STEM_HEAD_X - HALF
    share, z = STEM_ABOVE
    out += [[HALF, 0.0], [HALF + share * fore_overhang, z], [STEM_HEAD_X, WAIST + BOW_RISE_M]]
    return out


def stern_line(depth: float) -> list[list[float]]:
    """`stern_m`, low to high: the post from its heel to the water, the counter to the taffrail."""
    aft_overhang = -HALF - TAFFRAIL_X
    out = [[POST[0][0], -depth], list(POST[1]), [-HALF, 0.0]]
    out += [[-HALF - share * aft_overhang, z] for share, z in COUNTER]
    out.append([TAFFRAIL_X, WAIST + QD_RAIL[0][1]])
    return out


def counter_points() -> list[list[float]]:
    """`form.stern.counter_hb_m`: her round counter's half-breadths by height, low to high, at the
    wale's middle at its after end and at the taffrail (`COUNTER_AT_WALE_M`,
    `COUNTER_AT_TAFFRAIL_M`)."""
    _x, low, high = wales_line()[0]
    taffrail = stern_line(collier_drawn_depth())[-1][1]
    return [
        [round((low + high) / 2.0, 2) + 0.0, COUNTER_AT_WALE_M],
        [taffrail, COUNTER_AT_TAFFRAIL_M],
    ]


def wales_line() -> list[list[float]]:
    """`wales_m`: Gwyn's band at Chapman's scale, carried along the sheer."""
    top = WAIST - WALE_TOP_BELOW_WAIST_PX / GWYN_RAIL_PX * RAIL_LENGTH
    broad = WALE_BROAD_PX / GWYN_RAIL_PX * RAIL_LENGTH
    return [[x, top + rise - broad, top + rise] for x, rise in WALE_RISE]


def decks() -> dict[str, list[list[float]]]:
    """`decks_m`: the upper deck and the quarterdeck at side (judgement)."""

    def x_of(v, end):
        if v is None:
            return MAST_X["fore"] if end == "fore" else break_x()
        return v

    upper = []
    for i, (x, z) in enumerate(UPPER_DECK):
        if i == 0:
            x = round(stern_x_at(z) + DECK_INSIDE_COUNTER_M, 2) + 0.0
        elif i == len(UPPER_DECK) - 1:
            x = STEM_HEAD_X + x
        upper.append([x_of(x, "fore"), z])
    qd = [[TAFFRAIL_X + QUARTERDECK[0][0], QUARTERDECK[0][1]], [break_x(), QUARTERDECK[1][1]]]
    return {"upper": upper, "quarterdeck": qd}


def stern_x_at(z: float) -> float:
    """The stern's line at height z: the post, the counter and the taffrail (`stern_m`)."""
    from freesail.ship.profile import interp

    return interp([(pz, px) for px, pz in stern_line(collier_drawn_depth())], z)


def deck_at(x: float) -> float:
    """Her upper deck at side at x."""
    from freesail.ship.profile import interp

    return interp(decks()["upper"], x)


def ports() -> list[list[float]]:
    """`ports_m["upper"]`: each [x, sill, half-breadth at the sill], the half-breadth the
    collier's, scaled (never the drawing's)."""
    out = []
    for x in PORTS_X:
        sill = round(deck_at(x) + SILL_ABOVE_DECK_M, 2)
        out.append([x, sill, collier_half_breadth(x, sill)])
    return out


def head_line(stem: list[list[float]]) -> list[list[float]]:
    """`head_m`: the knee from the stem's fore edge at its height to the figure."""
    above = [p for p in stem if p[1] >= 0.0]
    out = []
    for reach, z in HEAD:
        if reach is None:
            from freesail.ship.profile import interp

            x = interp([[pz, px] for px, pz in above], z)
        else:
            x = STEM_HEAD_X + reach
        out.append([x, z])
    return out


@dataclass(frozen=True)
class Particulars:
    """Her figures in the file's frame, metres: the hull block and its notes, and the profile's
    lines ([x, z] above her water, a port [x, sill, half-breadth], the breadth [x, at her water,
    at the rail]) as `g.hull_profile` takes them."""

    hull: dict
    hull_notes: dict
    lines: dict


def check_burthen() -> None:
    """Her burthen by the old measure on her waterline and on her taffrail-to-stem-head length,
    each within D6 (a)'s band (Bil-D §1.4), raised in words."""
    for words, length in (
        ("the waterline", LWL_FT),
        ("the length taffrail to stem head", RAIL_LENGTH_FT),
    ):
        tons = burthen(length)
        if not BURTHEN_BAND[0] - 0.5 <= tons <= BURTHEN_BAND[1]:
            raise ValueError(
                f"her burthen on {words}, {length} ft, is {tons:.1f} tons by the old measure; "
                f"between {BURTHEN_BAND[0]:g} and {BURTHEN_BAND[1]:g} is wanted (D6 (a))."
            )


def particulars() -> Particulars:
    """Her figures in the file's frame, and the checks of Bil-D §1.4 that need no rig raised in
    words (never an `assert`, which `python -O` strips) before the file is written."""
    check_burthen()
    depth = collier_drawn_depth()
    stem = stem_line(depth)
    parts, _marks = g.from_steel_table(
        collier_rows(), length_ratio=LENGTH_RATIO, beam_ratio=BEAM_RATIO
    )
    lines = {
        "rail": rail_line(),
        "breadth": collier_breadth(),
        "keel": [[POST[0][0], -depth], [stem[0][0], -depth]],
        "stem": stem,
        "stern": stern_line(depth),
        "wales": wales_line(),
        "section": dead_flat_section(),
        "decks": decks(),
        "ports": {"upper": ports()},
        "port_size": {"upper": list(PORT_SIZE)},
        "head": head_line(stem),
        "breadth_line": parts["breadth_line"],
        "sections": parts["sections"],
        "rabbet": rabbet_line(),
    }
    return Particulars(hull=hull_figures(), hull_notes=dict(HULL_NOTES), lines=lines)


def profile_into(p: Particulars, report: list) -> None:
    """Her profile and shape keys added to `p.hull` through `g.hull_profile` and `g.hull_form`,
    their notes to `p.hull_notes`; the drawn hull and each port triple's gap to the drawn side
    reported (her triples' half-breadths are the collier's, not measured at a port: Bil-D §3.5)."""
    ln = dict(p.lines)
    rail, breadth = ln.pop("rail"), ln.pop("breadth")
    p.hull["profile"] = g.hull_profile(rail, breadth, **ln)
    form = {
        "fullness": [1.0, 1.0],
        "stern": {"type": "round", "counter_hb_m": counter_points(), "lights_m": [list(LIGHTS)]},
        "head": "figure",
    }
    REPORT["gaps"] = g.hull_form(p.hull, form=form, marks=MARKS, measured=(), report=report)
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
# The rig (Bil-D §4)
# ---------------------------------------------------------------------------

# The brig's (`brig()` in the generator) sail rules, carried to her spars: a course 0.42 of its
# yard deep, its head and foot 0.9 of the yard; a topsail's head 0.82 and a topgallant's 0.89 of
# its yard, each foot 0.9 of the yard below; the course's centre 0.45 of its depth under its yard,
# the others' half-way between the yards; reefs a course one and a topsail three.
COURSE_DEPTH_OF_YARD = 0.42
HEAD_OF_YARD = {"course": 0.9, "topsail": 0.82, "topgallant": 0.89}
FOOT_OF_YARD_BELOW = 0.9
REEFS = {"course": 1, "topsail": 3, "topgallant": 0}
# Brace limits, degrees from square: the brig's, level for level (brig.yaml, read; Bil-D §4.1):
# the fore 60, 62 and 64; the dry yard 62 and the main topsail and topgallant yards 64 and 66.
BRACE_LIMIT_DEG = {
    "fore.yard": 60,
    "fore.topsail.yard": 62,
    "fore.topgallant.yard": 64,
    "main.crossjack.yard": 62,
    "main.topsail.yard": 64,
    "main.topgallant.yard": 66,
}
# The brig's plain sail (brig.yaml's "plain sail", read: 766 m2), whose rope hers is scaled from
# by the root of her own over it (Bil-D §4.1; judgement, Indf §4.2's method).
BRIG_PLAIN_M2 = 766.0
# The brig's shrouds and stays (brig() in the generator): five shrouds of 7.5 in a side at each
# mast and two topmast backstays of 5 in (Gwyn draws about six deadeyes at each channel, Bil
# §2.3), the stays' sizes, all scaled by her rope's scale.
SHROUDS_IN, SHROUDS = 7.5, 5
BACKSTAY_IN, BACKSTAYS = 5.0, 2
STAY_IN = {
    "fore.stay": 11.0,
    "fore.topmast.stay": 6.0,
    "jib.stay": 4.0,
    "main.stay": 12.0,
    "main.topmast.stay": 6.0,
    "main.topgallant.stay": 3.5,
    "bobstay": 9.0,
    "martingale": 4.0,
}
# The settee's lines on the brig's sizes for the like lines (Bil-D §4.4; the fixture's, Ext §5.1):
# the jeers the brig's throat halyard (3 1/2 in, three parts), the derrick her peak halyard (3 in,
# four), the vangs her gaff's vangs (3 in), the ourses her main course's bowlines, the tacks and
# the clewlines and the buntline her main course's, the one sheet her spanker's (4 in, two parts).
SETTEE_ROPE = {
    "halyard": (3.5, 3),
    "lift": (3.0, 4),
    "vang": (3.0, 1),
    "guy": (None, 1),
    "tack": (None, 1),
    "sheet": (4.0, 2),
    "clewline": (None, 1),
    "buntline": (None, 1),
}
SETTEE_COURSE_ROPE = {
    "guy": "bowline",
    "tack": "tack",
    "clewline": "clewline",
    "buntline": "buntline",
}
# The settee's cut (D5 (a); Bil-D §4.4): the head Gwyn's, laid on Chapman's rail length; the tack
# 0.30 m above the waist rail. The yard cut to the head: the drawing draws a settee's yard as its
# head (B5.4's finding, Ext §6.3 as built), and her design's §4.4 cuts it so then, recorded.
SETTEE_HEAD_M = round(GWYN_SETTEE["head_px"] / GWYN_RAIL_PX * RAIL_LENGTH, 2)
SETTEE_TACK_Z = round(WAIST + GWYN_SETTEE["tack_above_waist_m"], 2)
SETTEE_CANVAS = g.BRIG_CANVAS["main.spanker"]  # the brig's mainsail's number, Steel p. 119
# The headsails (Bil-D §4.2; Gwyn, read: the fore topmast staysail and the jib on the jib-boom):
# each a triangle on its stay by `g.stay_sail_cut`, its tack at the stay's lower end, its peak as
# far up the stay's rise as Gwyn draws it (the jib's head 0.674 of the rise from the jib-boom's end
# to the fore topmast head, the staysail's 0.516 from the bowsprit's; measured at her step 1 on
# the held image, judgement on the reading), the leech upright under the peak to the tack's
# height. Both stays from the fore topmast's cap (the brig's are of the fore topmast).
HEADSAIL_PEAK_SHARE = {"fore.topmast_staysail": 0.516, "jib": 0.674}
HEADSAIL_ROPE_IN = {"fore.topmast_staysail": 3.0, "jib": 3.0}
# The spritsail (Bil-D §4.3; D8 (b)): its yard the fore topsail yard's length (Steel 1794 vol. I
# p. 40: "cross-jack and spritsail yards as the fore topsail yard"), slung 0.85 of the way out the
# bowsprit's outboard part and 0.8 m under its line (judgement, the 64's); its sail 14 cloths at the
# head and the foot, the 64's share of its yard (26 cloths on 57 ft 6 in, Steel's table IV), and
# deep to within a metre of the water in Steel's half yards (judgement).
SPRITSAIL_CLOTHS = 14.0
SPRITSAIL_STATION = 0.85
SPRITSAIL_HANG_M = 0.8
SPRITSAIL_FOOT_ABOVE_WATER_M = 1.0
SPRIT_BRACE_LIMIT_DEG = 30
SPRITSAIL_REEFS = 2  # Steel's two diagonal reef bands for a spritsail (the 64's)
SPRITSAIL_CANVAS = (2, f"{g.STEEL_SM}, 'Spritsail course': No. 2 or 3, the first taken")
# The main topmast staysail (Bil-D §4.5): Steel's rule as the brig's (`between_the_masts`), its
# leech 4 or 5 yards deeper than the main topsail and its foot a cloth or two more than the
# leech's yards, its peak before the main top; its leech cut short so that its foot stands a foot
# clear of the settee's yard where they cross (judgement), its foot to the fore mast.
MTSS_CLEAR_M = 0.30
MTSS_ROPE_IN = 2.5


def square_cuts() -> dict[str, tuple[int, float, float]]:
    """Her square sails by the brig's rules on her yards: each sail's (area m2, centre above her
    water, depth m)."""
    out = {}
    for name in ("fore", "main"):
        z = RIG_Z[name]
        lower = "fore.yard" if name == "fore" else "main.crossjack.yard"
        topsail, tg = f"{name}.topsail.yard", f"{name}.topgallant.yard"
        if name == "fore":
            depth = COURSE_DEPTH_OF_YARD * YARD_M[lower]
            width = HEAD_OF_YARD["course"] * YARD_M[lower]
            out["fore.course"] = (round(width * depth), round(z["yard"] - 0.45 * depth, 1), depth)
        for sail, yard, below, top_z, low_z in (
            (f"{name}.topsail", topsail, lower, z["topsail_yard"], z["yard"]),
            (f"{name}.topgallant", tg, topsail, z["topgallant_yard"], z["topsail_yard"]),
        ):
            level = sail.split(".")[1]
            depth = top_z - low_z
            head = HEAD_OF_YARD[level] * YARD_M[yard]
            foot = FOOT_OF_YARD_BELOW * YARD_M[below]
            out[sail] = (round(0.5 * (head + foot) * depth), round(low_z + 0.5 * depth, 1), depth)
    return out


def settee_cut() -> dict:
    """Her settee by D5 (a) through `settee.cut`, on the main mast's line as filed."""
    return settee.cut(
        head_m=SETTEE_HEAD_M,
        yard_deg=GWYN_SETTEE["yard_deg"],
        tack_z=SETTEE_TACK_Z,
        mast_x_at=lambda z: mast_x_at("main", z),
    )


def written_corners(corners) -> list[list[float]]:
    """A sail's corners (x, z above her water) as filed: x and the height above the datum, each to
    the centimetre."""
    return [[round(x, 2) + 0.0, above_datum(z)] for x, z in corners]


def as_water(corners) -> list[tuple[float, float]]:
    """Filed corners back above her water."""
    return [(x, z + DATUM) for x, z in corners]


def head_geometry() -> dict:
    """The bowsprit and the jib-boom on Chapman's figures (Bil-D §4.2): the root at the stem head,
    the bowsprit's end (its cap) and the jib-boom's end, (x, z above her water)."""
    root = (STEM_HEAD_X, round(WAIST + BOW_RISE_M, 2))
    c, s = math.cos(math.radians(BOWSPRIT_STEEVE_DEG)), math.sin(math.radians(BOWSPRIT_STEEVE_DEG))
    out_m, jib_m = sw_metres(BOWSPRIT_OUT_SW), sw_metres(JIB_BOOM_BEYOND_SW)
    end = (root[0] + out_m * c, root[1] + out_m * s)
    jend = (end[0] + jib_m * c, end[1] + jib_m * s)
    return {"root": root, "end": end, "jib_end": jend, "out_m": out_m, "jib_m": jib_m}


def headsail_corners(head: dict) -> dict[str, list[tuple[float, float]]]:
    """Each headsail's corners [tack, peak, clew] above her water (`HEADSAIL_PEAK_SHARE`)."""
    upper = (MAST_X["fore"], RIG_Z["fore"]["topmast_cap"])
    out = {}
    for sid, lower in (("fore.topmast_staysail", head["end"]), ("jib", head["jib_end"])):
        peak_z = lower[1] + HEADSAIL_PEAK_SHARE[sid] * (upper[1] - lower[1])
        out[sid] = g.stay_sail_cut(upper, lower, peak_z - lower[1], peak_z=peak_z)
    return out


def spritsail_cut(head: dict) -> dict:
    """The spritsail yard and its sail through `spritsail_yards.cut` (Ext §4.1; D8 (b))."""
    s = math.sin(math.radians(BOWSPRIT_STEEVE_DEG))
    sling_z = head["root"][1] + SPRITSAIL_STATION * head["out_m"] * s - SPRITSAIL_HANG_M
    half_yards = math.floor(2.0 * (sling_z - SPRITSAIL_FOOT_ABOVE_WATER_M) / spritsail_yards.YARD_M)
    row = {
        "yard_m": YARD_M["fore.topsail.yard"],
        "head_cloths": SPRITSAIL_CLOTHS,
        "foot_cloths": SPRITSAIL_CLOTHS,
        "depth_yd": half_yards / 2.0,
    }
    cut = spritsail_yards.cut(
        root=head["root"],
        steeve_deg=BOWSPRIT_STEEVE_DEG,
        bowsprit_out_m=head["out_m"],
        jib_out_m=head["jib_m"],
        spritsail=row,
        station=SPRITSAIL_STATION,
        hang=SPRITSAIL_HANG_M,
    )
    cut["row"] = row
    return cut


def settee_yard_z(cut: dict, x: float) -> float:
    """The height of the settee's yard above her water at x, along its head (its yard cut to it)."""
    _tack, throat, peak, _clew = cut["corners"]
    return throat[1] + (x - throat[0]) * (peak[1] - throat[1]) / (peak[0] - throat[0])


def main_topmast_staysail_corners(cut: dict) -> tuple[list[tuple[float, float]], dict]:
    """The main topmast staysail's corners [tack, nock, peak, clew] above her water, and its
    figures beside Steel's (Bil-D §4.5): its stay from the main topmast's cap to the fore lower
    cap, its peak on the stay before the main top (`g.TOP_REACH_OF_YARD` of the dry yard before the
    mast at the lower cap's height, as the brig's), Steel's leech cut short so that its foot
    stands `MTSS_CLEAR_M` above the settee's yard under the clew, Steel's foot to the fore mast."""
    upper = (mast_x_at("main", RIG_Z["main"]["topmast_cap"]), RIG_Z["main"]["topmast_cap"])
    lower = (MAST_X["fore"], RIG_Z["fore"]["cap"])
    top_x = (
        mast_x_at("main", RIG_Z["main"]["cap"])
        + g.TOP_REACH_OF_YARD * YARD_M["main.crossjack.yard"]
    )
    peak = (top_x, g.stay_point(upper, lower, top_x))
    topsail_yd = (RIG_Z["main"]["topsail_yard"] - RIG_Z["main"]["yard"]) / spritsail_yards.YARD_M
    steel_leech = (topsail_yd + 4.5) * spritsail_yards.YARD_M
    steel_foot = (topsail_yd + 4.5 + 1.5) * g.CLOTH_FT * FT
    clew_z = max(peak[1] - steel_leech, settee_yard_z(cut, top_x) + MTSS_CLEAR_M)
    fore_x = min(top_x + steel_foot, lower[0])
    nock = (fore_x, g.stay_point(upper, lower, fore_x))
    corners = [(fore_x, clew_z), nock, peak, (top_x, clew_z)]
    figures = {
        "steel_leech": steel_leech,
        "leech": peak[1] - clew_z,
        "steel_foot": steel_foot,
        "foot": fore_x - top_x,
        "clear": clew_z - settee_yard_z(cut, top_x),
    }
    return corners, figures


def check_rig(cuts: dict, cut: dict, mtss: tuple) -> list[str]:
    """Bil-D §1.4's checks on the rig, raised in words: the fore course's foot clear of the rail at
    the fore mast; the main topmast staysail's foot clear of the settee's yard. Returns the
    figures as sentences for the report."""
    from freesail.ship.profile import interp

    rail = interp(rail_line(), MAST_X["fore"])
    foot = RIG_Z["fore"]["yard"] - cuts["fore.course"][2]
    if foot <= rail:
        raise ValueError(
            f"the fore course's foot stands {foot:.2f} m above the water at the fore mast, the "
            f"rail {rail:.2f} m: its foot clears the rail (her design's §4.2)."
        )
    corners, fig = mtss
    if fig["clear"] < MTSS_CLEAR_M - 0.01:
        raise ValueError(
            f"the main topmast staysail's foot stands {fig['clear']:.2f} m above the settee's yard "
            f"under its clew; {MTSS_CLEAR_M:g} m is wanted (her design's §4.5)."
        )
    return [
        f"the fore course's foot {foot:.2f} m above the water, {foot - rail:.2f} m clear of the "
        "rail at the fore mast.",
        f"the main topmast staysail: leech {fig['leech']:.2f} m against Steel's "
        f"{fig['steel_leech']:.2f} m, cut so that its foot stands {fig['clear']:.2f} m above the "
        f"settee's yard; foot {fig['foot']:.2f} m against Steel's {fig['steel_foot']:.2f} m, to "
        "the fore mast.",
    ]


def rope_scale(plain_m2: float) -> float:
    """Her rope's scale on the brig's: the root of her plain sail over the brig's (Bil-D §4.1)."""
    return math.sqrt(plain_m2 / BRIG_PLAIN_M2)


def sizes_for(level: str, mast: str, scale: float) -> dict[str, float]:
    """A level's rope sizes, the frigate's establishment by the brig's mast factor and scale, by
    hers (as the brig's are the frigate's by hers)."""
    factor = g.BRIG_MAST_ROPE_FACTOR[mast] * g.BRIG_ROPE_SCALE * scale
    return {cls: g.quarter(c * factor) for cls, c in g.FRIGATE_ROPE[level].items()}


PROV = " Provisional (truth 9), see gen_ships.py."

# Her era note's first clause, before its colon, is the class her readings serve
# (`api.readings.ship_class_words`, in-world: tests/test_in_world.py).
ERA_NOTES = (
    "A British coasting bilander under a settee main: two masts, a ship's square fore and a main "
    "with the long lateen-cut settee under its topsail and a dry yard, a raised quarterdeck and a "
    "round windowed stern; an old survivor of a rig rare by 1769 (Falconer 1780, BILANDER) and "
    "'seldom used but by the Dutch' by 1794 (Steel 1794 vol. I p. 220), the last British bilander "
    "in the register in 1789 (Lloyd's Register). Her hull Chapman's bilander of 1768 at the "
    "plate's own scale, 70.6 by 19.4 ft (Architectura Navalis Mercatoria Pl. LXII No. 5), drawn "
    "as Edward Gwyn's British bilander of about 1780 (RMG PAG3828) on Steel 1805's brig collier's "
    "body; 118 tons burthen on her waterline and 128 on her length taffrail to stem head by the "
    "old measure; rigged to Gwyn's heights with Chapman's yards. Unarmed by default, a trader of "
    "eight hands, with the armed merchant's four 3-pounders and four swivels for the editor "
    "(Lloyd's 1779 and 1782: the Elizabeth's guns). Not the Hopewell of Poole, a bilander of 150 "
    "tons built in 1749 and lengthened in 1756 (Lloyd's 1776, 1779), whose name she bears by the "
    "owner's answer of 2026-10-29. Undated. See tools/ships/bilander.py for every figure's source."
)

HEADER = (
    "# The bilander Hopewell: a British coasting bilander under a settee main, Chapman's\n"
    "# bilander of 1768 (Pl. LXII No. 5) at the plate's own scale drawn as Gwyn's British\n"
    "# bilander of about 1780 (RMG PAG3828, measured on the museum's image and never copied) on\n"
    "# Steel 1805's brig collier's body. Generated by tools/gen_ships.py\n"
    "# (tools/ships/bilander.py, her settee by tools/ships/settee.py); edit those and rerun, do\n"
    "# not edit this file. Her design: docs/design/Design-Ship-Bilander.md. Rope: the brig's\n"
    "# scaled to her sail (judgement). Spar ratings are provisional, set for truth 9 with the M1\n"
    "# sail curves; see the script. Canvas: Steel 1794 vol. I; cloth ratings from the number by\n"
    "# Luce App. E. Units: metres, m2, kg, kN. Comments mark judgements.\n"
)

# What her rules compute from her own keys, for `her_report()`.
REPORT: dict = {}


def write(out_dir: str, p: Particulars) -> None:
    """Build her file and dump it to `out_dir`: the hull, the masts and yards, the square sails,
    the settee, the head and the spritsail, the main topmast staysail and the storm canvas, the
    groups and the aliases (Bil-D §1.4's order); then her guns, company and stores in the house's
    order of the files (the ground tackle, the crew, the armament and its bill, the hold, the
    pumps and the boat, as the merchant brig's and the Neufchatel's), and her description."""
    report: list[str] = []
    profile_into(p, report)
    REPORT["hull"] = report
    b = HerBuilder("Hopewell", "bilander", ERA_NOTES, p.hull, p.hull_notes)
    dw = g.DESIGN_WIND_KN

    cuts = square_cuts()
    cut = settee_cut()
    head = head_geometry()
    heads = headsail_corners(head)
    sprit = spritsail_cut(head)
    mtss = main_topmast_staysail_corners(cut)
    REPORT["rig"] = check_rig(cuts, cut, mtss)

    # her rope's scale (Bil-D §4.1): her plain sail over the brig's, its area from the cuts
    head_areas = {sid: round(settee.area_centroid(c)[0]) for sid, c in heads.items()}
    plain = (
        sum(cuts[s][0] for s in cuts)
        + round(settee.area_centroid(as_water(written_corners(cut["corners"])))[0])
        + sum(head_areas.values())
    )
    scale = rope_scale(plain)
    REPORT["rope"] = (plain, scale)

    yards = masts_and_yards(b, cuts, cut, head_areas, heads, scale, dw)
    squares = square_sails(b, cuts, scale)
    the_settee(b, cut, scale)
    headsails, spritsail = the_head(b, head, heads, sprit, scale, dw)
    between, storm = staysail_and_storm(b, mtss, scale)
    groups_and_aliases(b, yards, squares, headsails, spritsail, between, storm)
    REPORT["plain"] = sum(
        next(s["area_m2"] for s in b.doc["sails"] if s["id"] == sid)
        for sid in b.doc["groups"]["plain sail"]
    )

    # -- her guns, her company and her stores (Bil-D §5-§7), in the house's order of the files;
    # her description at far detail (§8) ---------------------------------------------------------
    guns = her_guns(p.hull["profile"])
    ground_tackle(b)
    company(b)
    armament(b, guns)
    quarter_bill(b, guns)
    hold_pumps_boat(b)
    b.descriptions([DESCRIPTION])
    b.dump(os.path.join(out_dir, "bilander.yaml"), HEADER)


def loads_of(cuts: dict, cut: dict) -> dict[str, tuple[int, float, str]]:
    """Each working sail's (area, centre above her water, curve class) for the spars' ratings."""
    loads = {sid: (a, c, "square") for sid, (a, c, _d) in cuts.items()}
    area, _cx, cz = settee.area_centroid(as_water(written_corners(cut["corners"])))
    loads["main.settee"] = (round(area), round(cz, 1), "lug")
    return loads


MAST_WORDS = {
    "fore": "the fore 0.148 of the waterline abaft the stem at the rail (10.7 Swedish ft; Steel's "
    "3/20), nearly plumb",
    "main": "the main 0.41 of the waterline forward of the sternpost at the rail (29.7 Swedish "
    "ft), raking aft about 2.8 degrees; x_m its line at the datum",
}
LEVEL_OF_SPAR = {"yard": "lower", "topsail": "topsail", "topgallant": "topgallant"}


def masts_and_yards(b, cuts, cut, head_areas, heads, scale, dw):
    """Her masts and yards (Bil-D §4.1): the lower masts at Chapman's stations to Gwyn's caps,
    the topmasts and the topgallant masts with their poles to Gwyn's trucks; the yards at Gwyn's
    heights and Chapman's lengths, the main's lower yard a dry yard; the settee's yard. Returns
    the yards by mast, lowest first."""
    loads = loads_of(cuts, cut)
    yards = {"fore": [], "main": []}
    for name in ("fore", "main"):
        z = RIG_Z[name]
        sails = (
            ["fore.course", "fore.topsail", "fore.topgallant"]
            if name == "fore"
            else ["main.topsail", "main.topgallant", "main.settee"]
        )
        carried = {
            "lower": [loads[s] for s in sails],
            "topsail": [loads[s] for s in sails if "top" in s],
            "topgallant": [loads[s] for s in sails if "topgallant" in s],
        }
        lower = b.spar(
            f"{name}.mast",
            "mast",
            x_m=MAST_X[name],
            rake_deg=RAKE_DEG[name] or None,
            height_m=above_datum(z["cap"]),
            heave_to_aback=True if name == "main" else None,
            rating_kn=g.design_kn(carried["lower"], dw["lower"]),
            note=f"{name} lower mast: {MAST_WORDS[name]} (Chapman 1768 Pl. LXII No. 5, measured: "
            "Research-Bilander-2026-10.md §2.4); its cap at Gwyn's height, laid from the waist "
            "rail on Chapman's rail length (her design's §4.1; Gwyn's masts stand on the drawn "
            "rail, so D6 (e)'s 'above the deck' is read from it), its top at Gwyn's top."
            + (
                " heave_to_aback: her main laid aback to heave to (D4 (a); Ext §5.7), the main "
                "topsail on its dry yard to the mast."
                if name == "main"
                else ""
            )
            + PROV,
        )
        top = b.spar(
            f"{name}.topmast",
            "topmast",
            steps_on=lower,
            height_m=round(z["topmast_cap"] - z["cap"], 2),
            rating_kn=g.design_kn(carried["topsail"], dw["topsail"]),
            note=f"{name} topmast: from the lower cap to its own at Gwyn's height (her design's "
            f"§4.1).{PROV}",
        )
        b.spar(
            f"{name}.topgallant_mast",
            "topgallant_mast",
            steps_on=top,
            height_m=round(z["truck"] - z["topmast_cap"], 2),
            rating_kn=g.design_kn(carried["topgallant"], dw["topgallant"]),
            note=f"{name} topgallant mast with its pole, from the topmast cap to Gwyn's truck; no "
            f"royal mast and no royal (D40 (a): no drawing of her type has one).{PROV}",
        )
        on = {"yard": lower, "topsail": top, "topgallant": f"{name}.topgallant_mast"}
        for level, key, yard_id in (
            ("yard", "yard", "fore.yard" if name == "fore" else "main.crossjack.yard"),
            ("topsail", "topsail_yard", f"{name}.topsail.yard"),
            ("topgallant", "topgallant_yard", f"{name}.topgallant.yard"),
        ):
            words = YARD_WORDS[yard_id]
            # the dry yard carries no sail's chain: it is rated for the main topsail whose foot it
            # spreads, as the frigate's crossjack is for her mizen topsail
            load = (
                [loads["main.topsail"]]
                if yard_id == "main.crossjack.yard"
                else carried[LEVEL_OF_SPAR[level]]
            )
            yard = b.spar(
                yard_id,
                "yard",
                on=on[level],
                length_m=YARD_M[yard_id],
                height_m=above_datum(z[key]),
                brace_limit_deg=BRACE_LIMIT_DEG[yard_id],
                rating_kn=g.design_kn(load, dw[LEVEL_OF_SPAR[level]]),
                note=f"{words}; at Gwyn's height (her design's §4.1); braces "
                f"{BRACE_LIMIT_DEG[yard_id]} deg from square, the brig's level for level "
                f"(brig.yaml; judgement, no source giving hers).{PROV}",
            )
            yards[name].append(yard)
        b.sided(
            f"{name}.shrouds",
            "shroud",
            lower,
            rating=g.rope_kn(g.quarter(SHROUDS_IN * scale), SHROUDS),
            note="the brig's five shrouds of 7.5 in a side, her rope's scale (judgement); Gwyn "
            "draws about six deadeyes at each channel, the shrouds and a backstay (Research-"
            "Bilander-2026-10.md §2.3).",
        )
        b.sided(
            f"{name}.topmast.backstay",
            "backstay",
            top,
            rating=g.rope_kn(g.quarter(BACKSTAY_IN * scale), BACKSTAYS),
        )
    # the settee's yard (Bil-D §4.4; Ext §5.1): slung on the main mast a third of the way along
    # its head, its height_m the sling's above the datum, cut to the head
    sling = cut["sling"]
    b.spar(
        "main.lug_yard",
        "lug_yard",
        on="main.mast",
        length_m=round(cut["yard_m"], 2),
        height_m=above_datum(sling[1]),
        rating_kn=g.design_kn([loads["main.settee"]], dw["lower"]),
        note="the settee's yard, the bilander's main yard (Falconer 1780, YARD; Research-Bilander-"
        "2026-10.md §1.1), slung on the main mast a third of the way along the head from the "
        "throat (D5 (a)), height_m the sling. Its length the head's: Gwyn draws the yard 564 px "
        "against the head's 534 (about 0.9 m longer), and the drawing draws a settee's yard as its "
        "head, so it is cut to the head here (her design's §4.4, B5.4's finding); Chapman's settee "
        "yard is 12.45 m at 35 degrees (recorded). Not braced (Ext E3): its trim is its sheet's "
        "and its vangs'.",
    )
    return yards


YARD_WORDS = {
    "fore.yard": "fore yard 40.8 ft, Chapman's at twice its drawn length (Research-Bilander-"
    "2026-10.md §2.4, measured: 0.578 of the waterline; 2.1 of her breadth)",
    "fore.topsail.yard": "fore topsail yard 30.0 ft, Chapman's (measured)",
    "fore.topgallant.yard": "fore topgallant yard 20.1 ft, Chapman's (measured)",
    "main.crossjack.yard": "the dry yard, 40.8 ft: a yard under the main top with no sail, filed "
    "as the frigate's crossjack, spreading the main topsail's foot (Gwyn, read; Lescallier Pl. "
    "XVII fig. 7 and Pl. XXII fig. 8; Steel 1794 vol. I, BRIG: a crossjack yard and no main yard), "
    "its length the fore yard's by Chapman's rule for brigs (Chapman 1781 p. 102, read: a brig's "
    "main yard the fore's), Chapman drawing none on that bilander. The check, by judgement: the "
    "64's crossjack to her mizen topsail yard (Steel 1794 p. 49) carried to her main topsail yard "
    "gives 40.8 ft too; Steel p. 40's ship's rule, the crossjack as the fore topsail yard, would "
    "give 30.0 ft, shorter than the main topsail yard it spreads, and is not taken",
    "main.topsail.yard": "main topsail yard 30.7 ft, Chapman's (measured), its sail sheeted to the "
    "dry yard's arms (Gwyn; Lescallier)",
    "main.topgallant.yard": "main topgallant yard 20.1 ft, Chapman's (measured)",
}

SQUARE_WORDS = {
    "course": "the brig's rule on her yard: 0.42 of the yard deep, its head and foot 0.9 of it",
    "topsail": "the brig's rule between her yards: the head 0.82 of its yard, the foot 0.9 of the "
    "yard below, as deep as the hoist between them",
    "topgallant": "the brig's rule between her yards: the head 0.89 of its yard, the foot 0.9 of "
    "the yard below, as deep as the hoist between them",
}


def square_sails(b, cuts, scale):
    """Her five square sails (Bil-D §4.2): cut between her yards as they stand by the brig's
    rules; canvas by the brig's table; reefs as the brig's; lines by `g.square_sail_lines` on the
    brig's sizes by her rope's scale. Returns them by level."""
    out = {"course": [], "topsail": [], "topgallant": []}
    yard_of = {
        "fore.course": "fore.yard",
        "fore.topsail": "fore.topsail.yard",
        "fore.topgallant": "fore.topgallant.yard",
        "main.topsail": "main.topsail.yard",
        "main.topgallant": "main.topgallant.yard",
    }
    for sid, yard in yard_of.items():
        name, level = sid.split(".")
        area, centre, _depth = cuts[sid]
        canvas = g.BRIG_CANVAS[sid]
        reef = REEFS[level]
        sheeted = (
            " Sheeted to the dry yard's arms (Gwyn; Lescallier Pl. XVII fig. 7 and Pl. XXII fig. "
            "8): plainly, wider at the foot than Chapman's drawn sail, whose clews come to the top "
            "34 ft apart; D40 (a) takes Gwyn's."
            if sid == "main.topsail"
            else ""
        )
        sail = b.sail(
            sid,
            "square",
            yard=yard,
            area_m2=area,
            reef_bands=reef,
            x_m=g.raked_x(MAST_X[name], RAKE_DEG[name], centre, DATUM),
            centre_height_m=centre,
            canvas_no=canvas[0],
            cloth_rating_kn=g.cloth(area, canvas[0]),
            note=f"{name} {level}: {SQUARE_WORDS[level]} (brig() in the generator; Steel 1794: a "
            f"brig's sails 'similar to those on the main and fore masts of a ship').{sheeted}"
            + g.canvas_note(canvas),
        )
        g.square_sail_lines(
            b,
            sail,
            yard,
            sizes_for(level, name, scale),
            hoisting=(level != "course"),
            course=(level == "course"),
            reef=(reef > 0),
            bowline=(level == "topsail"),
        )
        out[level].append(sail)
    # the dry yard's braces and lifts (Lescallier Pl. XVII fig. 7: its lifts from the cap), the
    # main course's sizes; no halyard, it is slung
    sizes = sizes_for("course", "main", scale)
    b.sided(
        "main.crossjack.yard.brace",
        "brace",
        "main.crossjack.yard",
        rating=g.rope_kn(sizes["brace"]),
    )
    b.sided(
        "main.crossjack.yard.lift", "lift", "main.crossjack.yard", rating=g.rope_kn(sizes["lift"])
    )
    return out


def the_settee(b, cut, scale):
    """Her settee (Bil-D §4.4; Ext §5.1; D5 (a)): its corners from `settee.cut`, filed above the
    datum; its lines from `settee.lines`, rated on the brig's sizes for the like lines by her
    rope's scale; `settee.check` on the corners as filed and the lines as written."""
    corners = written_corners(cut["corners"])
    area, cx, cz = settee.area_centroid(as_water(corners))
    s = b.sail(
        "main.settee",
        "lug",
        yard="main.lug_yard",
        mast="main.mast",
        dipping=True,
        settee=True,
        corners_m=corners,
        area_m2=round(area),
        reef_bands=1,
        x_m=round(cx, 1),
        centre_height_m=round(cz, 1),
        canvas_no=SETTEE_CANVAS[0],
        cloth_rating_kn=g.cloth(round(area), SETTEE_CANVAS[0]),
        note="the settee, her main (Falconer 1780, BILANDER: 'the main-sail ... bent to a yard "
        "hanging fore and aft'; Research-Bilander-2026-10.md §1), cut to D5 (a) by "
        "tools/ships/settee.py: its head Gwyn's, 534 px of Gwyn's 785, at 44 degrees to the "
        "horizontal; the leech and the foot each 0.72 of the head and the luff 0.16 of the leech "
        "(Gwyn's ratios); slung a third of the way along the head from the throat on the main "
        "mast's raked line (D5 (a): a lateen yard's third, Lescallier pp. 377-380, Steel 1794 vol. "
        "I p. 237; plainly, against Gwyn's 0.395); the tack 0.30 m above the waist rail under the "
        "throat (Gwyn, measured); the clew where the foot from the tack meets the leech from the "
        "peak. Corners [tack, throat, peak, clew] above the datum. Gwyn draws the yard crossing "
        "the mast higher than the third puts it (recorded in docs/dev/TuningNotes.md, the cut "
        "standing on D5 (a) and Gwyn's tack). Chapman's settee is about 92 m2 on a 12.45-m yard at "
        "35 degrees (recorded, not tuned). One reef band a fifth of the leech up, parallel to the "
        "foot (D42 (a)). A dipping lug that is a settee (Ext §5.1): handled by its own evolutions "
        "(B3.3), never a lugger's lug; in 'courses', 'plain sail' and 'all sail', never 'gaff "
        "sails'." + g.canvas_note(SETTEE_CANVAS),
    )
    written = settee.lines("main.lug_yard", s)
    course = sizes_for("course", "main", scale)
    for lid, cls, of, side in written:
        size, parts = SETTEE_ROPE[cls]
        if size is None:
            size = course[SETTEE_COURSE_ROPE[cls]]
        else:
            size = g.quarter(size * scale)
        rating = g.rope_kn(size, parts)
        if side is None:
            b.line(
                lid,
                cls,
                of,
                rating=rating,
                parts=parts if cls == "sheet" else None,
                note=SETTEE_LINE_NOTES.get(cls),
            )
        else:
            b.line(
                lid,
                cls,
                of,
                side=side,
                rating=rating,
                note=SETTEE_LINE_NOTES.get(cls) if side == settee.SIDES[0] else None,
            )
    settee.check(
        {**cut, "corners": as_water(corners)},
        written,
        mast_x_at=lambda z: mast_x_at("main", z),
        taffrail_x=TAFFRAIL_X,
        sail_id=s,
    )
    REPORT["settee"] = {
        "area": area,
        "centre": (cx, cz),
        "sling": cut["sling"],
        "corners": as_water(corners),
        "yard_m": cut["yard_m"],
    }
    return s


SETTEE_LINE_NOTES = {
    "halyard": "the jeers (Lescallier's drisse, p): a double block on the yard and one at the "
    "masthead (Steel 1794 vol. I p. 207); the brig's throat halyard's size, three parts, by her "
    "rope's scale (judgement).",
    "lift": "the derrick (Lescallier's martinet, o), the peak's lift, from the masthead to the "
    "yard between the slings and the peak (Steel p. 207); the brig's peak halyard's size, four "
    "parts.",
    "vang": "the peak brace (Lescallier's bras, t), the English vangs, a side, to the quarter "
    "(Steel p. 208; Falconer, VANGS); the brig's gaff vangs' size.",
    "guy": "the ourses (Lescallier's q), the English bowlines at the yard's heel, a side, which "
    "'doth serve for a brace to that yard' (Mainwaring; Steel p. 208); the brig's main course's "
    "bowlines' size.",
    "tack": "the tacks (Lescallier's amures, r), a side, the weather one hauled down; the brig's "
    "main course's tacks' size.",
    "sheet": "the one sheet (Lescallier's ecoute, s), made fast at the taffrail (Lescallier p. "
    "390; Ext §5.1: one, unsided); the brig's spanker sheet's size, two parts.",
    "clewline": "the clewlines and the buntline, 'comme pour les voiles quarrees' (Lescallier p. "
    "390, pp. 221-228); the brig's main course's sizes.",
}


HEAD_WORDS = {
    "fore.topmast_staysail": "the fore topmast staysail (Gwyn, read), a triangle on the fore "
    "topmast stay from the bowsprit's cap, its head 0.516 of the stay's rise up it as Gwyn draws "
    "it (measured), the leech upright under the head to the tack's height (g.stay_sail_cut; "
    "judgement on the cut); corners [tack, peak, clew] above the datum.",
    "jib": "the jib on the jib-boom (Gwyn, read), a triangle on the jib stay from the jib-boom's "
    "end, its head 0.674 of the stay's rise up it as Gwyn draws it (measured), the leech upright "
    "under the head to the tack's height (g.stay_sail_cut; judgement on the cut); corners [tack, "
    "peak, clew] above the datum. No flying jib and no fore staysail: Gwyn draws neither.",
}


def staysail(b, sid, stay, corners, canvas, rope_in, words, bent=None, scale=1.0):
    """A staysail or a headsail of these corners (x, z above her water) on its stay: its area and
    centre from its corners, filed with them above the datum; its halyard, sheets and downhaul on
    the brig's size by her rope's scale, raised to bear its cloth as `g.staysail_from_cut` raises
    it (judgement)."""
    area_m2, cx, cz = settee.area_centroid(corners)
    area = round(area_m2)
    storm = canvas is g.BRIG_CANVAS["storm"]
    cloth = g.storm_cloth(area) if storm else g.cloth(area, canvas[0])
    s = b.sail(
        sid,
        "jibheaded",
        stay=stay,
        area_m2=area,
        x_m=round(cx, 1),
        centre_height_m=round(cz, 1),
        canvas_no=canvas[0],
        cloth_rating_kn=cloth,
        bent=bent,
        corners_m=written_corners(corners),
        note=words + g.canvas_note(canvas, storm=storm),
    )
    size = g.quarter(rope_in * scale)
    bear = math.ceil(4.0 * math.sqrt(0.5 * cloth / g.ROPE_KN_PER_SQ_IN)) / 4.0
    size = max(size, bear)
    b.line(f"{sid}.halyard", "halyard", s, rating=g.rope_kn(size, 2))
    b.sided(
        f"{sid}.sheet",
        "sheet",
        s,
        rating=g.rope_kn(size),
        note="to bear its sail: its working load half the cloth's rating (judgement).",
    )
    b.line(f"{sid}.downhaul", "downhaul", s, rating=g.rope_kn(g.quarter(size * 0.8)))
    return s


def the_head(b, head, heads, sprit, scale, dw):
    """The head (Bil-D §4.2, §4.3): the bowsprit and the jib-boom on Chapman's figures, the stays,
    the fore topmast staysail and the jib, and the spritsail yard with its sail bent. Returns the
    headsails and the spritsail."""
    head_loads = []
    for corners in heads.values():
        a, _cx, cz = settee.area_centroid(corners)
        head_loads.append((round(a), round(cz, 1), "jibheaded"))
    root, end, jend = head["root"], head["end"], head["jib_end"]
    bowsprit = b.spar(
        "bowsprit",
        "bowsprit",
        x_m=root[0],
        length_m=head["out_m"],
        height_m=above_datum(end[1]),
        rating_kn=g.design_kn(head_loads, dw["lower"]),
        note=f"bowsprit 28.5 Swedish ft outboard at the stem head, steeved about "
        f"{BOWSPRIT_STEEVE_DEG:g} degrees (Chapman's No. 5, measured: Research-Bilander-2026-10.md "
        "§2.4), heavier than the Tractat's rule (1.15 of the breadth outboard, 22.9 Swedish ft; "
        "Chapman 1781 pp. 99-100, read): x_m its root at the stem head, where the viewer draws "
        "its heel, length_m its part outboard, height_m its end above the datum. Its heel inboard "
        "not read. The spritsail yard slung under it (D8 (b); Ext §4.1; "
        "tools/ships/spritsail_yards.py).",
    )
    jib_boom = b.spar(
        "jib_boom",
        "jib_boom",
        on=bowsprit,
        length_m=head["jib_m"],
        height_m=above_datum(jend[1]),
        rating_kn=g.design_kn([head_loads[1]], dw["jib_boom"]),
        note="jib-boom 15.3 Swedish ft beyond the bowsprit's cap along its steeve (Chapman's, "
        f"measured), its end above the datum. No flying jib-boom: Gwyn draws none.{PROV}",
    )
    for lid, of in (
        ("fore.stay", "fore.mast"),
        ("fore.topmast.stay", "fore.topmast"),
        ("jib.stay", "fore.topmast"),
        ("main.stay", "main.mast"),
        ("main.topmast.stay", "main.topmast"),
        ("main.topgallant.stay", "main.topgallant_mast"),
        ("bobstay", bowsprit),
        ("martingale", jib_boom),
    ):
        b.line(
            lid,
            "stay",
            of,
            rating=g.rope_kn(g.quarter(STAY_IN[lid] * scale)),
            note=STAY_NOTES.get(lid),
        )
    headsails = [
        staysail(
            b,
            sid,
            "fore.topmast.stay" if sid == "fore.topmast_staysail" else "jib.stay",
            corners,
            g.BRIG_CANVAS[sid],
            HEADSAIL_ROPE_IN[sid],
            HEAD_WORDS[sid],
            scale=scale,
        )
        for sid, corners in heads.items()
    ]
    # the spritsail yard and its sail (D8 (b); Bil-D §4.3; Ext §4.1)
    y, sl = sprit["spritsail.yard"], sprit["spritsail"]
    area = round(sl["area"])
    centre = round(sl["centre"], 1)
    yard = b.spar(
        "spritsail.yard",
        "yard",
        on=bowsprit,
        x_m=round(y["x"], 2),
        length_m=YARD_M["fore.topsail.yard"],
        height_m=above_datum(y["z"]),
        brace_limit_deg=SPRIT_BRACE_LIMIT_DEG,
        rating_kn=g.design_kn([(area, centre, "square")], dw["topsail"]),
        note="spritsail yard 30.0 ft, the fore topsail yard's, by Steel 1794 vol. I p. 40's rule "
        "for the Navy, 'cross-jack and spritsail yards as the fore topsail yard' (read on the page "
        "image; Steel's 64 has the two alike at 57 ft 6 in, p. 49): a King's rule carried to a "
        "trader (judgement). Slung under the bowsprit near the cap (Steel 1794 vol. I pp. "
        f"196-197), {SPRITSAIL_STATION:g} of the way out its outboard part and "
        f"{SPRITSAIL_HANG_M:g} m under its line (judgement, the 64's); x_m and height_m its "
        f"slings; no halyard, it hanging in slings (Ext §4.1); braces {SPRIT_BRACE_LIMIT_DEG} deg "
        "from square (judgement, the 64's); kept out of the file's yard groups, braced by name. "
        "Evidence for the yard: Steel 1794's Plate 1, the bilander, and Lescallier's belandre, "
        "Pl. XXII fig. 8 (read); none in Gwyn. No sprit-topsail yard: no drawing of her type "
        "shows one.",
    )
    row = sprit["row"]
    sail = b.sail(
        "spritsail",
        "square",
        yard=yard,
        area_m2=area,
        reef_bands=SPRITSAIL_REEFS,
        x_m=round(sl["x"], 1),
        centre_height_m=centre,
        canvas_no=SPRITSAIL_CANVAS[0],
        cloth_rating_kn=g.cloth(area, SPRITSAIL_CANVAS[0]),
        note=f"spritsail: {row['head_cloths']:g} cloths at the head and the foot, the 64's share "
        "of its yard (26 cloths on 57 ft 6 in, Steel's table IV), and deep to within a metre of "
        "the water in Steel's half yards (judgement), 22 1/2 in a cloth, hanging square from its "
        "yard (tools/ships/spritsail_yards.py, which checks its foot above the water at no heel). "
        "Two diagonal reef bands, Steel's for a spritsail. Bent (the owner's answer for the razee, "
        "'an occasional sail kept out of plain sail', read in the period's sense, set now and then "
        "in light fair winds: her design's §4.3): in 'spritsails' and 'all sail', never in 'plain "
        "sail', 'courses', 'headsails' or the sail room's 'occasional sails', so the polar never "
        "sets it; hove to it is clewed up and 'shorten sail' takes it in first (Ext §4.2)."
        + g.canvas_note(SPRITSAIL_CANVAS),
    )
    sizes = sizes_for("topsail", "fore", scale)
    g.square_sail_lines(b, sail, yard, sizes, hoisting=False, reef=SPRITSAIL_REEFS > 0)
    b.sided(
        f"{yard}.guy",
        "guy",
        yard,
        rating=g.rope_kn(sizes["brace"]),
        note="the spritsail yard's guys (Lavery 1985 I28, as the 64's), the braces' size "
        "(judgement).",
    )
    REPORT["sprit"] = sprit
    return headsails, sail


STAY_NOTES = {
    "fore.stay": "the brig's sizes for her stays by her rope's scale (judgement); the fore storm "
    "staysail sets on it.",
    "jib.stay": "from the fore topmast head to the jib-boom's end: the jib sets on it.",
    "main.stay": "from the main mast head to the fore mast; the main storm staysail sets on it.",
    "main.topmast.stay": "from the main topmast head to the fore mast head: the main topmast "
    "staysail sets on it.",
}


def staysail_and_storm(b, mtss, scale):
    """The main topmast staysail, the one staysail between the masts and her lying-to staysail,
    bent and out of plain sail; the fore and main storm staysails in the sail room, the brig's
    pattern (Bil-D §4.5). Returns them."""
    corners, _fig = mtss
    between = staysail(
        b,
        "main.topmast_staysail",
        "main.topmast.stay",
        corners,
        g.BRIG_CANVAS["main.topmast_staysail"],
        MTSS_ROPE_IN,
        "the main topmast staysail, the one staysail she sets between the masts: Lescallier pp. "
        "402-403 give the brigantin, of which the bilander is a variant, 'staysails and jibs' "
        "(Research-Bilander-2026-10.md §2.1, read (OCR)); which staysail is judgement, Gwyn "
        "drawing none there. Cut by Steel's rule as the brig's (the leech 4 or 5 yards deeper "
        "than the main topsail, the foot a cloth or two more than the leech's yards, the peak "
        "before the main top), its leech cut short so that its foot stands a foot clear of the "
        "settee's yard where they cross, its foot to the fore mast (judgement). No main staysail: "
        "its foot would lie across the settee's fore part (judgement). Bent, out of plain sail as "
        "the brig's is, and her lying-to staysail; corners [tack, nock, peak, clew] above the "
        "datum.",
        scale=scale,
    )
    storm_canvas = g.BRIG_CANVAS["storm"]
    fore_yard_ft = YARD_FT["fore.yard"]
    fss_foot = 0.9 * fore_yard_ft / 2.0 + 4.0
    fss_leech = 0.42 * fore_yard_ft
    fss_area = round(0.5 * fss_foot * fss_leech * FT * FT)
    fss = b.sail(
        "fore.storm_staysail",
        "jibheaded",
        stay="fore.stay",
        area_m2=fss_area,
        x_m=round(MAST_X["fore"] + 1.0 + fss_foot * FT / 3.0, 1),
        centre_height_m=round(DATUM + 1.5 + fss_leech * FT / 3.0, 1),
        canvas_no=storm_canvas[0],
        cloth_rating_kn=g.storm_cloth(fss_area),
        bent=False,
        note="fore storm staysail on the fore stay (Luce 1884 ch. X), cut as the brig's: "
        "Kipping's fore staysail, its foot half the course's head and 4 ft, its leech the "
        "course's depth, on her fore yard; in the sail room." + g.canvas_note(storm_canvas, True),
    )
    s3 = g.quarter(3.0 * scale)
    b.line("fore.storm_staysail.halyard", "halyard", fss, rating=g.rope_kn(s3, 2))
    b.sided("fore.storm_staysail.sheet", "sheet", fss, rating=g.rope_kn(s3, 3))
    b.line(
        "fore.storm_staysail.downhaul", "downhaul", fss, rating=g.rope_kn(g.quarter(2.5 * scale))
    )
    run_ft = (MAST_X["fore"] - MAST_X["main"]) / FT
    rise_ft = (RIG_Z["main"]["top"] - DATUM) / FT - 12.0
    head_x, head_z = -0.6 * run_ft, 12.0 + 0.6 * rise_ft
    mss_area = round(0.5 * abs(head_x * (7.0 - 12.0) - (head_z - 12.0) * head_x) * FT * FT)
    mss = b.sail(
        "main.storm_staysail",
        "jibheaded",
        stay="main.stay",
        area_m2=mss_area,
        x_m=round(MAST_X["fore"] + (2.0 * head_x / 3.0) * FT, 1),
        centre_height_m=round(DATUM + (12.0 + head_z + 7.0) / 3.0 * FT, 1),
        canvas_no=storm_canvas[0],
        cloth_rating_kn=g.storm_cloth(mss_area),
        bent=False,
        note="main storm staysail on the main stay, the brig's (Luce 1884 ch. X: 'the "
        "storm-staysails set on the respective lower-stays'): its tack at the fore mast collar "
        "12 ft up, its head 0.6 up the stay, its clew 7 ft above the deck (judgement, the "
        "brig's); in the sail room. It stands in the settee's place in a gale, the settee taken in "
        "with the topsails' third reef (Ext §5.8; her design's §4.5, to be checked on her file)."
        + g.canvas_note(storm_canvas, True),
    )
    b.line("main.storm_staysail.halyard", "halyard", mss, rating=g.rope_kn(s3, 2))
    b.sided("main.storm_staysail.sheet", "sheet", mss, rating=g.rope_kn(s3, 3))
    b.line(
        "main.storm_staysail.downhaul", "downhaul", mss, rating=g.rope_kn(g.quarter(2.5 * scale))
    )
    return [between], [fss, mss]


def groups_and_aliases(b, yards, squares, headsails, spritsail, between, storm):
    """Her groups with the names the engine reads, and her aliases in the period's words, the
    brig's where they fit (Bil-D §4.4, §4.5)."""
    settee_id = "main.settee"
    courses = [*squares["course"], settee_id]
    b.group("courses", courses)
    b.group("topsails", squares["topsail"])
    b.group("topgallants", squares["topgallant"])
    b.group("headsails", headsails)
    b.group("jibs", headsails[1:])
    b.group("staysails", headsails[:1] + between)
    b.group("staysails between the masts", between)
    b.group("square sails", squares["course"] + squares["topsail"] + squares["topgallant"])
    b.group("fore-and-aft sails", [*headsails, *between, settee_id])
    b.group("lying-to staysails", between)
    b.group("spritsails", [spritsail])
    plain = courses + squares["topsail"] + squares["topgallant"] + headsails
    b.group("plain sail", plain)
    b.group("all sail", [*plain, *between, spritsail])
    by_level = [y for i in range(3) for y in (yards["fore"][i], yards["main"][i])]
    for name in ("fore", "main"):
        b.group(f"{name} yards", yards[name])
    b.group("yards", by_level)
    b.group("lower yards", [yards["fore"][0], yards["main"][0]])
    b.group("topsail yards", [yards["fore"][1], yards["main"][1]])
    b.group("topgallant yards", [yards["fore"][2], yards["main"][2]])
    b.group("head yards", yards["fore"])
    b.group("after yards", yards["main"])
    b.group("lower masts", ["fore.mast", "main.mast"])
    b.group("topmasts", ["fore.topmast", "main.topmast"])
    b.group("topgallant masts", ["fore.topgallant_mast", "main.topgallant_mast"])
    b.group("storm canvas", storm)
    b.group("storm staysails", storm)
    for cls in ("sheet", "tack", "bowline"):
        b.group(f"fore {cls}s", [f"fore.course.{cls}.{s}" for s in g.SIDES])
        b.alias(f"fore {cls}", f"fore {cls}s")
    b.group("fore topsail bowlines", [f"fore.topsail.bowline.{s}" for s in g.SIDES])
    b.alias("fore top bowline", "fore topsail bowlines")
    b.group("main topsail bowlines", [f"main.topsail.bowline.{s}" for s in g.SIDES])
    b.alias("main top bowline", "main topsail bowlines")
    b.group("main tacks", [f"{settee_id}.tack.{s}" for s in g.SIDES])
    b.alias("main tack", "main tacks")
    b.alias("main sheet", f"{settee_id}.sheet")
    # the settee, her mainsail (Bil-D §4.4): "the bilander's main yard" (Falconer 1780, YARD)
    for word in ("mainsail", "main sail", "the mainsail", "settee", "the settee"):
        b.alias(word, settee_id)
    for word in ("main yard", "settee yard", "lateen yard"):
        b.alias(word, "main.lug_yard")
    for word in ("crossjack", "crossjack yard", "cross-jack yard", "dry yard"):
        b.alias(word, "main.crossjack.yard")
    b.alias("foresail", "fore.course")
    b.alias("fore yard", "fore.yard")
    b.alias("fore topmast staysail", "fore.topmast_staysail")
    b.alias("main topmast staysail", "main.topmast_staysail")
    b.alias("the spritsail yard", "spritsail.yard")
    b.alias("head sails", "headsails")
    b.alias("topgallant sails", "topgallants")
    b.alias("upper yards", "topgallant yards")


# ---------------------------------------------------------------------------
# Her guns, her company and her stores (Bil-D §5-§8; her road's step 3)
# ---------------------------------------------------------------------------

# Her fits (Bil-D §5.1; the brief, item 3; D41 (a)): unarmed by default, a coasting trader in
# peace as Gwyn draws her, and one fit the scenario may name, "armed merchant".
ARMED_FIT = "armed merchant"
# Its pieces (Bil-D §5.3): Adye 1804's long 3-pounder of 4 ft 6 in (p. 155), the one length
# Adye gives (`period.ADYE_LONG_GUN_CWT[3]`); three men a gun (Falconer 1780, QUARTERS; D31 (c)).
LONG_3_PATTERN = (4, 6)
# The swivels on Gwyn's open quarterdeck rail, from forward (Bil-D §5.2, judgement), four by one
# call of the generator's helper so that their ids run swivel.1 and swivel.2 once.
SWIVELS_X = (-5.50, -9.00)
SWIVEL_COUNT = 4

GUNS_NOTE = (
    "The armament (spec M7 7; package 70's shape; docs/design/Design-Ship-Bilander.md §5): "
    "unarmed by default, a coasting trader in peace as Gwyn draws her (the brief, item 3), with "
    "one fit the scenario may name (ship: {fit: armed merchant}): Elizabeth's four 3-pounders of "
    "the register and four swivels. Each 3-pounder on its port of the hull's profile to the "
    "centimetre with its deck named, each swivel at the quarterdeck rail's height at its own x "
    "(Build-Ships.md §5.3 and §6's checklist); the piece Adye 1804's (p. 155) and the crews "
    "Falconer 1780's (D31 (c)); the magazine a trader's. Every figure's source is in "
    "tools/ships/bilander.py."
)
FIT_SOURCE = (
    "Lloyd's Register 1779 and 1782, the bilander Elizabeth of 130 tons, '4-3 P.' (the row images "
    "read: Research-Bilander-2026-10.md §3); Adye 1804 p. 155, the piece; Falconer 1780 "
    "(QUARTERS), the crews; the swivels and every place judgement"
)
FIT_NOTE = (
    "The armed merchant (D41 (a)): four long 3-pounders, two a side in the waist, Elizabeth's four "
    "3-pounders of the common construction (Lloyd's 1779 and 1782), and four half-pounder swivels "
    "on the quarterdeck rail, two a side (judgement: no British source counts a bilander's "
    "swivels; four is the privateer schooner's). The register's other bilanders give the degrees "
    "an editor may reason within: Kerrison's six 4-pounders (140 tons, 1781-1783) and Essex's two "
    "2-pounders (160 tons, 1781); neither is a fit. Her ports are cut for the fit in the waist "
    "bulwark (the owner's 'cutouts in the gunwale', 2026-10-29), Gwyn drawing her unpierced. Her "
    "eight cannot man a side's guns, the helm and the sails together: at the beat the bill's "
    "trimmers and helmsman are told off first and the guns take what is left (her design's §5.4; "
    "the beat measured in docs/dev/TuningNotes.md)."
)
THREES_NOTE = (
    "Four long 3-pounders, two a side at her two ports a side in the waist, Nos. 1 and 2 from "
    "forward (the places judgement: between the fore chains and the main mast, Bil-D §5.2), each "
    "on its port's triple, its x and its sill to the centimetre: Adye 1804's 3-pounder of 4 ft "
    "6 in, 7 cwt 1 qr (p. 155, the page image read), the one length Adye gives; three men to the "
    "pair of a number (Falconer 1780, QUARTERS; D31 (c)), who fight whichever gun bears."
)
SWIVELS_NOTE = (
    "Four half-pounder swivels, two a side on the quarterdeck's open rail (Gwyn draws it on "
    "stanchions, Bil-D §3.2; the places judgement), each at the rail's height at its own x, as the "
    "house sets a swivel (Build-Ships.md §5.3); on its yoke, no port; its half hundredweight the "
    "house's (judgement); one man each, from whoever is spare."
)
# Her cartridges' powder (Bil-D §5.3): the Regulations' Table No. 29 through `charge_lb` and the
# shared note since the shared work SW-1 filled the table (Build-Ships.md §10): the long
# 3-pounder's 1 lb, as the share gave it, and the half-pounder swivel's 2 oz, where the engine's
# half gave 4 oz. Her own note, which said so until then, is gone.


def her_guns(profile: dict) -> list:
    """The armed fit's guns (Bil-D §5.2-§5.3), as (mapping, note) entries: the 3-pounders by
    `g.broadside_pair` on her upper deck's port triples, numbered from forward, each crew
    Falconer's (assigning an existing key keeps the key order, Indf §5.2); the swivels by one
    call of `g.swivels` on the quarterdeck, each then set to the rail's height at its own x
    (`rail_at`'s rule, `freesail/ship/profile.py`). Checked before the file is written."""
    from freesail.ship.profile import interp

    cwt = period.ADYE_LONG_GUN_CWT[3][LONG_3_PATTERN]
    from_forward = sorted(profile["ports_m"]["upper"], key=lambda t: -t[0])
    guns = []
    for number, (x, sill, _hb) in enumerate(from_forward, start=1):
        made = g.broadside_pair(
            number,
            "long",
            3,
            cwt,
            x,
            sill,
            THREES_NOTE if number == 1 else None,
            deck="upper",
            round_to=0.01,
        )
        for gun, _ in made:
            gun["crew"] = period.FALCONER_CREW[3]
        guns += made
    made = g.swivels(
        SWIVEL_COUNT, list(SWIVELS_X), 0.0, SWIVELS_NOTE, deck="quarterdeck", round_to=0.01
    )
    for gun, _ in made:
        gun["height_m"] = round(interp(profile["rail_m"], gun["x_m"]), 2) + 0.0
    guns += made
    check_guns(guns, profile)
    return guns


def check_guns(guns: list, profile: dict) -> None:
    """Every port gun of the fit on a port triple of its deck within 0.01 m by its x and its
    height, no two of a side on one (Bil-D §1.4; Build-Ships.md §6's checklist, item 2), and each
    swivel at the rail's height at its x within 0.01 m, on the quarterdeck's extent; raised in
    words."""
    from freesail.ship.profile import interp

    taken = set()
    for gun, _ in guns:
        if gun["place"] == "rail":
            rail = interp(profile["rail_m"], gun["x_m"])
            deck = profile["decks_m"][gun["deck"]]
            if abs(gun["height_m"] - rail) > 0.01 or not deck[0][0] <= gun["x_m"] <= deck[-1][0]:
                raise ValueError(
                    f"bilander: {gun['id']} stands at x {gun['x_m']:g} m, {gun['height_m']:g} m "
                    f"above her water, not on the {gun['deck']}'s rail ({rail:.2f} m there)."
                )
            continue
        on = [
            i
            for i, (x, sill, _hb) in enumerate(profile["ports_m"][gun["deck"]])
            if abs(gun["x_m"] - x) <= 0.01 and abs(gun["height_m"] - sill) <= 0.01
        ]
        if not on:
            raise ValueError(
                f"bilander: {gun['id']} stands at x {gun['x_m']:g} m, {gun['height_m']:g} m above "
                f"her water, on no port triple of her {gun['deck']} deck within 0.01 m."
            )
        if (gun["side"], on[0]) in taken:
            raise ValueError(f"bilander: {gun['id']} stands in a port another gun has.")
        taken.add((gun["side"], on[0]))


def armament(b, guns) -> None:
    """Her fits (Bil-D §5.1, §5.3): `unarmed` the default and the armed merchant, its magazine
    the merchant brig's (`g.MERCHANT_ROUNDS`, 20 round and 4 grape a gun; `g.SWIVEL_ROUNDS`, 40
    a swivel; judgement), no charges for exercise (a King's fit's only), the charges Table No.
    29's under the shared note (SW-1)."""
    magazine = g.fit_magazine(guns, {"long": g.MERCHANT_ROUNDS, "swivel": g.SWIVEL_ROUNDS})
    b.armament(GUNS_NOTE, g.UNARMED, [(ARMED_FIT, FIT_SOURCE, guns, magazine, FIT_NOTE)])


# Her company, eight (D43; Bil-D §6.1): the posts her wardroom file's, the master and the mate
# (data/people/bilander.yaml); two in each top, the main top's for the settee's loosing and
# furling aloft (Ext §5.1 and its risk 10), the fore's alike (judgement); the boy in the
# afterguard, the messenger, drawn by name; the cook. No forecastle station: the head sheets and
# the anchors fall to the fore topmen by the hands' ranking (crew/hands.py), a company of eight
# having no hand to spare for one.
COMPLEMENT = 8
STATIONS = {"fore_top": 2, "main_top": 2, "afterguard": 1, "idlers": 1}
# Her shares (the lead's ruling (8) of 2026-11-09, package 75; judgement): able seamen and a boy,
# no ordinary seaman, so that her five muster four able topmen and a landsman boy, as the
# merchant brig's boy is rated (data/people/merchant-brig.yaml); the merchant brig's own shares,
# 0.70, 0.20 and 0.10, mustered the boy an able seaman (B4).
RATINGS = {"able": 0.80, "ordinary": 0.0, "landsman": 0.20}
# Her stores (Bil-D §7; judgement): water for eight at a gallon a man a day for two months is
# about two tons (252 gallons to the ton, data/crew/ration.yaml), and some over; provisions for
# two months, a coaster's passage and its delays; the spare rope; a small trader's shot plugs,
# the smack's.
WATER_TONS = 3
PROVISIONS_DAYS = 60
CORDAGE_FATHOMS = 80
SHOT_PLUGS = 2
# The quarter bill beyond the gun crews (Bil-D §5.4; judgement): the merchant brig's trimmers, a
# topman of each top; one at the helm; no hand at the powder beyond the cook; the merchant
# brig's small arms, two, and a trader's boarders, three of her eight.
TRIMMERS = {"fore_top": 1, "main_top": 1}
HELM = 1
POWDER = 0
SMALL_ARMS = 2
BOARDERS = 3


def company(b) -> None:
    """Her crew section (Bil-D §6.1), the people drawn at muster from her wardroom file (§6.2),
    and her stores beside them (§7): water, provisions, cordage, shot plugs, the ration, a spare
    topsail yard, and her sail room. Her complement checked against her posts and stations."""
    posts, drawn = g.wardroom("bilander")
    on_stations = sum(STATIONS.values())
    if len(posts) + on_stations != COMPLEMENT:
        raise ValueError(
            f"bilander: her {len(posts)} posts and {on_stations} hands on station make "
            f"{len(posts) + on_stations}, not her {COMPLEMENT}."
        )
    entries = [
        (
            ("complement",),
            COMPLEMENT,
            "Eight (D43): a coasting trader of about 130 tons, the master, the mate, four seamen, "
            "a boy and a cook (judgement). No source gives a bilander's company (Research-"
            "Bilander-2026-10.md §2.8): the Nancy of Boston, 170 tons and catalogued 'brigantine "
            "or bilander', had ten in 1779 (TNA HCA 32/405/21, the catalogue); the merchant "
            "brig's five men to a hundred tons gives six or seven, and a settee dipped by hand "
            "at every tack wants the upper figure.",
        ),
        (
            ("names",),
            "english",
            "A British coaster's people: the english list in data/crew/names.yaml, as the smack's.",
        ),
        (
            ("stations", "fore_top"),
            STATIONS["fore_top"],
            "Hands per station, both watches together (Bil-D §6.1; judgement). No forecastle "
            "station: the head sheets and the anchors fall to the fore topmen by the hands' "
            "ranking, a company of eight having no hand to spare for one. Fore topmen: 2, the "
            "main top's alike.",
        ),
        (
            ("stations", "main_top"),
            STATIONS["main_top"],
            "Main topmen: 2, for the settee's loosing and furling aloft and her main topsail and "
            "topgallant (Ext §5.1 and its risk 10: two in the main top at the least).",
        ),
        (
            ("stations", "afterguard"),
            STATIONS["afterguard"],
            "Afterguard: the boy, 1, the messenger (the smack's and the merchant brig's).",
        ),
        (("stations", "idlers"), STATIONS["idlers"], "Idlers: the cook."),
        (
            ("ratings", "able"),
            RATINGS["able"],
            "Share of the seamen by rating (judgement; the lead's ruling of 2026-11-09): a "
            "coaster's able seamen and a boy, four able topmen and a landsman boy, as the "
            "merchant brig's boy is rated; her shares (0.70, 0.20, 0.10) mustered the boy an "
            "able seaman. Able: 0.80.",
        ),
        (("ratings", "ordinary"), RATINGS["ordinary"], "Ordinary: none."),
        (("ratings", "landsman"), RATINGS["landsman"], "Landsmen: 0.20, the boy."),
    ]
    entries += [
        (
            ("posts", post),
            None,
            (
                "Station holders by post (spec M3 2.3): the master who commands her and the mate, "
                "as the smack's (data/people/bilander.yaml); names are drawn at muster."
            )
            if i == 0
            else None,
        )
        for i, post in enumerate(posts)
    ]
    entries += [
        (("idlers_by_trade", "cook"), 1, "How the idlers are made up: the cook, 1."),
        (
            ("stores", "water_tons"),
            WATER_TONS,
            "Water for two months: eight men at a gallon a day is about 2 tons, and some over "
            "(judgement).",
        ),
        (
            ("stores", "provisions_days"),
            PROVISIONS_DAYS,
            "Provisions: two months, a coaster's passage and its delays (judgement).",
        ),
        (("stores", "spare_spars"), {}, None),  # the booms, by class: below
        (
            ("stores", "cordage_fathoms"),
            CORDAGE_FATHOMS,
            "Spare rope (judgement).",
        ),
        (
            ("stores", "shot_plugs"),
            SHOT_PLUGS,
            g.SHOT_PLUGS_NOTE + " A small trader's 2, the smack's.",
        ),
        *g.ration_entries(
            "a coaster's articles promised the like, as the merchant brig's (judgement: no scale "
            "of the period's merchant service is in the references)"
        ),
    ]
    b.crew(entries)
    b.people(
        "The named people beyond the posts (package 35, spec M5 §22): the boy as the messenger; "
        "see data/people/bilander.yaml.",
        drawn,
    )
    b.spare_spars(
        "The booms: a trader's spare (Bil-D §7; judgement after Luce 1866 ch. XVII, scaled down); "
        "see tools/ships/bilander.py.",
        [("yard", 1, "A spare topsail yard, to answer either mast (judgement, after Luce 1866).")],
    )
    canvas = {s["id"]: s["canvas_no"] for s in b.doc["sails"]}
    b.sail_room(
        "The sail room (spec 3b §6.3): a trader's second suit of the sails she wears out (Bil-D "
        "§7); see tools/ships/bilander.py.",
        [
            (
                "fore.topsail",
                canvas["fore.topsail"],
                "A second fore topsail and jib (judgement, as the merchant brig's).",
            ),
            ("jib", canvas["jib"], None),
            (
                "fore.storm_staysail",
                canvas["fore.storm_staysail"],
                "Storm canvas, one of each (spec 3b §6.4).",
            ),
            ("main.storm_staysail", canvas["main.storm_staysail"], None),
        ],
    )


def at_the_guns(guns) -> int:
    """The men a fit wants at the beat: one crew to a broadside pair, and one to each gun not on
    the broadside, a swivel its own (`parts.Gun.pair_key`)."""
    one_side = [gun for gun, _ in guns if gun["place"] != "broadside" or gun["side"] == g.SIDES[0]]
    return sum(gun["crew"] for gun in one_side)


def quarter_bill(b, guns) -> None:
    """Her quarter bill set against the armed fit (Bil-D §5.4), as Build-Ships.md §9.1 sets an
    unarmed default's: the merchant brig's trimmers, one at the helm, the powder the cook's, the
    filling party, sail before guns, two small-arms men and three boarders; the arithmetic in the
    generator's report."""
    REPORT["bill"] = (sum(STATIONS.values()), at_the_guns(guns))
    b.quarter_bill(
        g.QUARTER_BILL_NOTE,
        [
            (
                "fore_top",
                TRIMMERS["fore_top"],
                "The trimmers: a topman of each top for the braces and the sheets, the merchant "
                "brig's (judgement); the settee's sheet is her trim aft.",
            ),
            ("main_top", TRIMMERS["main_top"], None),
        ],
        HELM,
        POWDER,
        "sail before guns",
        {
            "helm": "One man at the helm, as the merchant brig's (judgement).",
            "powder": "The powder beyond the idlers: none; the cook passes it (judgement: eight "
            "hands, the boy among them, and six wanted at one side's 3-pounders).",
            "priority": "A merchantman's weapon is her heels: the sails before the guns "
            "(judgement), the merchant brig's.",
        },
        small_arms=SMALL_ARMS,
        boarders=BOARDERS,
        small_arms_note="Two men with the master's muskets from the cabin (judgement: a trader's "
        "chest of arms), the merchant brig's.",
        boarders_note="Three of her hands: a trader does not board (judgement, the merchant "
        "brig's share of her company).",
        filling=g.filling_party(guns),
    )
    b.crew_notes[("quarter_bill", "filling")] = (
        g.FILLING_NOTE + " Her four 3-pounders give one (Bil-D §5.3)."
    )


# Her burthen for the house's rules of tackle, hold and boat (Bil-D §7): the old measure on her
# length taffrail to stem head, 128 tons, D6 (a)'s "about 130"; her boat on that length.
BURTHEN_TONS = float(round(burthen(RAIL_LENGTH_FT)))
# The period's check on her anchors (Bil-D §7): the smallest rows of Steel 1794 vol. I's anchor
# table, the Navy's (the page image, IA leaf n127, read for her design): the brigs of 200 tons,
# three anchors of 12 cwt, and the cutter, three of 10 cwt.
STEEL_SMALLEST_ANCHORS = {"brigs of 200 tons": ("three", 12.0), "the cutter": ("three", 10.0)}
STEEL_BRIG_TONS = 200.0


def ground_tackle(b) -> None:
    """Her ground tackle by the house's rule on her burthen, beam and draught, the merchant
    brig's (`g.ground_tackle_for`); Steel's Navy table the check, in the note and the report
    (Bil-D §7)."""
    g.ground_tackle_for(b, BURTHEN_TONS, BREADTH_FT, DRAUGHT_FT)
    brig_n, brig_cwt = STEEL_SMALLEST_ANCHORS["brigs of 200 tons"]
    cutter_n, cutter_cwt = STEEL_SMALLEST_ANCHORS["the cutter"]
    b.tackle_notes[("anchors", "best_bower")] += (
        " The period's check: Steel 1794 vol. I's anchor table is the Navy's and ends at the "
        f"brigs of 200 tons, {brig_n} anchors of {brig_cwt:g} cwt, and the cutter, {cutter_n} of "
        f"{cutter_cwt:g} cwt (the page image, IA leaf n127, read for her design), a King's "
        "allowance heavier than a merchant's: the house's rule, later than her years, is kept for "
        "the two traders alike (judgement; Bil-D §7). Two bowers and a kedge, no sheet or stream "
        "under 200 tons (Lever 1808 p. 67). Gwyn's catted anchor, if it is one, a bower."
    )
    REPORT["anchors"] = brig_cwt / STEEL_BRIG_TONS * BURTHEN_TONS


def hold_pumps_boat(b) -> None:
    """Her hold a trader's half of her burthen; two hand pumps; her one boat, the long-boat, by
    Luce's rule on her length at the small vessel's factor (Bil-D §7), the merchant brig's rules
    and order."""
    g.hold_for(
        b,
        BURTHEN_TONS,
        False,
        "a coasting trader's hold, her trade: judgement, the merchant brig's share",
    )
    b.pumps(
        g.PUMPS_NOTE + " Two hand pumps, as the merchant brig's (judgement).",
        g.pump_entries(0, 2, ["the starboard pump", "the larboard pump"]),
    )
    b.boats(
        g.BOATS_NOTE,
        g.boat_entries(
            RAIL_LENGTH_FT,
            False,
            [
                (
                    "long_boat",
                    "launch",
                    "the long-boat",
                    1.0,
                    "The long-boat, a merchantman's one boat, stowed amidships, by Luce's rule on "
                    "her 75.6 ft taffrail to stem head at the small vessel's factor, as the "
                    "merchant brig's. Gwyn draws no boat (Research-Bilander-2026-10.md §2.7), "
                    "which is no evidence either way; one boat is judgement.",
                ),
            ],
        ),
    )


# Her far description (D16 (a); Bil-D §8), in her own file by SW-4's form (Build-Ships.md §8.1,
# §8.2): the tops make out a bilander, the glass a merchantman; her fit her file's default,
# `unarmed`, so that a far ship of hers carries nothing new (Build-Ships.md §8.1: a far vessel
# takes her description's fit only where it is not her file's default); a merchant's role.
DESCRIPTION = (
    "bilander",
    "a bilander",
    "a bilander, a merchantman under a settee main, deep laden",
    "The tops make her out a bilander: her settee's yard, peaked high over her stern and the "
    "longest spar she carries, is the rig's mark, as a lugger's lugs are, and the period named "
    "the rig on sight (Falconer 1780, BILANDER; Steel 1794 vol. I p. 220; Röding vol. I col. 304: "
    "it differs from the brig and the snow by its great sail); judgement on the words (D16 (a)). "
    "'Deep laden' is the merchantman's look, judgement, as the merchant brig's. Unarmed, her "
    "file's default; a merchant's role (Build-Ships.md §8.2).",
    g.UNARMED,
    ["merchant"],
)


# ---------------------------------------------------------------------------
# The generator's report and the hook
# ---------------------------------------------------------------------------


def source_checks() -> list[str]:
    """The sources' checks beside her own figures, as sentences for the report (Bil-D §2.1, §3.2,
    §4.4, §3.6 task 7): her burthen by the old measure; Chapman's length overall against Gwyn's
    head; the collier's stem head against hers; Chapman's settee against hers; Steel's
    brigantine's port on her waist."""
    from freesail.ship.profile import interp

    out = [
        f"her burthen by the old measure {burthen(LWL_FT):.1f} tons on her waterline and "
        f"{burthen(RAIL_LENGTH_FT):.1f} on her length taffrail to stem head."
    ]
    overall = TAFFRAIL_X + OVERALL_FT * FT - STEM_HEAD_X
    reach = HEAD[-1][0]
    out.append(
        f"Chapman's length overall, {OVERALL_FT:g} ft, puts the head {overall:.2f} m beyond the "
        f"stem head, against Gwyn's {reach:.2f}."
    )
    stem = (g.feet_and_inches(COLLIER_STEM["head_above_rabbet"]) - LOAD_ABOVE_BASE_FT) * FT
    out.append(
        f"the collier's stem head at her scale {stem * BEAM_RATIO:.2f} m above her water, against "
        f"her stem head's {WAIST + BOW_RISE_M:.2f}."
    )
    out.append(
        f"Chapman's settee about {CHAPMAN_SETTEE['area_m2']:g} m2 on a "
        f"{CHAPMAN_SETTEE['yard_m']:g}-m yard at {CHAPMAN_SETTEE['deg']:g} degrees, recorded "
        "beside hers."
    )
    sill = g.feet_and_inches(BRIGANTINE_PORT["sill_above_plank"]) * FT
    deep = g.feet_and_inches(BRIGANTINE_PORT["deep"]) * FT
    over = [interp(decks()["upper"], x) + sill + deep - interp(rail_line(), x) for x in PORTS_X]
    out.append(
        "Steel 1805's brigantine's port on her waist (its sill 1 ft 6 in above the deck, 1 ft 5 in "
        f"deep): its top {', '.join(f'{v:+.2f}' for v in over)} m against her rail at x "
        f"{', '.join(f'{x:g}' for x in PORTS_X)}."
    )
    return out


def her_report() -> str:
    """The generator's report: what her rules compute from her file's own keys, printed as her
    file is written and held by her tests (the lead's notes of 2026-10-29, item 2)."""
    out = [f"bilander: {line}" for line in source_checks()]
    out += [f"bilander: {line}" for line in REPORT.get("hull", [])]
    depth = collier_drawn_depth()
    out.append(
        f"bilander: the collier drawn {depth:.2f} m deep to its keel's underside against her "
        f"draught of {hull_figures()['draught_m']:.2f} m, recorded and never moved; its length "
        f"ratio {LENGTH_RATIO:.4f} and beam ratio {BEAM_RATIO:.4f}."
    )
    out.append(
        f"bilander: clr_x_m {CLR_X_M:+.2f} as tuned for her helm, against her start, the brig's "
        f"{BRIG_CLR_X_M:g} m as a share of her waterline, "
        f"{BRIG_CLR_X_M * LWL_FT / BRIG_LWL_FT:+.2f}."
    )
    for words, v in collier_checks().items():
        figure = ", ".join(f"{x:.2f}" for x in v) if isinstance(v, tuple) else f"{v:.2f}"
        out.append(f"bilander: the collier at her scale, {words}: {figure} m.")
    if "stern" in REPORT:
        (d1, hb1), (d2, hb2) = REPORT["stern"]
        out.append(
            f"bilander: her round stern drawn to its counter's half-breadths (counter_hb_m): at "
            f"the lights' middle height, {(LIGHTS[0] + LIGHTS[1]) / 2.0:.2f} m, {hb1:.2f} m off "
            f"the middle line {d1:.1f} m inside the taffrail and {hb2:.2f} m {d2:.1f} m inside, "
            f"against Gwyn's stern view's {COUNTER_AT_TAFFRAIL_M:.2f} m at the taffrail and "
            f"{COUNTER_AT_WALE_M:.2f} m at the wale."
        )
    out += [f"bilander: {line}" for line in REPORT.get("rig", [])]
    if "settee" in REPORT:
        st = REPORT["settee"]
        (tx, tz), (hx, hz), (px, pz), (cx_, cz_) = st["corners"]
        out.append(
            f"bilander: the settee {st['area']:.1f} m2, its centre x {st['centre'][0]:.2f}, "
            f"{st['centre'][1]:.2f} m above the water; tack ({tx:.2f}, {tz:.2f}), throat "
            f"({hx:.2f}, {hz:.2f}), peak ({px:.2f}, {pz:.2f}), clew ({cx_:.2f}, {cz_:.2f}) above "
            f"the water; slung at ({st['sling'][0]:.2f}, {st['sling'][1]:.2f}); its yard "
            f"{st['yard_m']:.2f} m; "
            f"the peak {px - TAFFRAIL_X:.2f} m and the clew {cx_ - TAFFRAIL_X:.2f} m inside the "
            "taffrail."
        )
    if "sprit" in REPORT:
        ss = REPORT["sprit"]["spritsail"]
        out.append(
            f"bilander: the spritsail {ss['area']:.1f} m2, {REPORT['sprit']['row']['depth_yd']:g} "
            f"yards deep, its foot {ss['foot_z']:.2f} m above her water."
        )
    if "rope" in REPORT:
        plain, scale = REPORT["rope"]
        out.append(
            f"bilander: her rope's scale on the brig's, the root of {plain} m2 over "
            f"{BRIG_PLAIN_M2:g}: {scale:.3f}."
        )
    if "plain" in REPORT:
        out.append(f"bilander: plain sail {REPORT['plain']} m2.")
    if "bill" in REPORT:
        hands, men = REPORT["bill"]
        out.append(
            f"bilander: the quarter bill on '{ARMED_FIT}': of her {hands} hands off the "
            f"quarterdeck the bill tells off {sum(TRIMMERS.values())} trimmers and {HELM} at the "
            f"helm first, and her guns want {men} (a crew of {period.FALCONER_CREW[3]} to each "
            "3-pounder pair, a man to each swivel)."
        )
    if "anchors" in REPORT:
        cwt = STEEL_SMALLEST_ANCHORS["brigs of 200 tons"][1]
        out.append(
            f"bilander: Steel 1794's brigs of 200 tons, {cwt:g} cwt to an anchor, give "
            f"{REPORT['anchors']:.1f} cwt on her {BURTHEN_TONS:g} tons, against the house's "
            f"{g.BOWER_CWT_PER_100_TONS * BURTHEN_TONS / 100.0:.1f}."
        )
    return "\n".join(out)


def drawn_stern(path: str) -> list[tuple[float, float]]:
    """Her drawn stern's half-breadth at the lights' middle height, 0.4 and 0.8 m inside the
    taffrail, read off the file as written (`freesail.ship.form`): for the report beside Gwyn's
    stern view and the collier's, her round counter drawn by `counter_hb_m`."""
    from freesail.ship import form
    from freesail.ship.loader import load_spec

    hull = load_spec(path).hull
    z = (LIGHTS[0] + LIGHTS[1]) / 2.0
    return [(d, form.half_breadth_at(hull, TAFFRAIL_X + d, z)) for d in (0.4, 0.8)]


def build(out_dir: str) -> None:
    """Write her file to `out_dir`, `bilander.yaml`, through `write()`; the checks of Bil-D §1.4
    raised before it is written."""
    REPORT.clear()
    write(out_dir, particulars())
    REPORT["stern"] = drawn_stern(os.path.join(out_dir, "bilander.yaml"))
    print(her_report(), file=sys.stderr)
