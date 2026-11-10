"""The period's tables the new ships share (package 75; docs/design/Build-Ships.md §3.1 item 3;
Design-Ship-Indefatigable.md §5.3, §7 and §12.1 item 4): constants with their sources, importing
nothing and calling nothing, read by a ship's module beside the generator's helpers.

The eight files' own tables stay as they are (`gen_ships.LONG_GUN_CWT`, `CARRONADE_CWT`, and
the crews of `gen_ships.gun_crew`, a judgement reading of Douglas). Adye's 18-pounder carronade
(9 cwt) and 9-pounder (24 1/2) differ from the shared tables' 10 and 26, from memory, which
feed the eight files: so the new ships read this one sourced table and no figure of the eight
moves (Design-Ship-Indefatigable.md §5.3). After stage 0 the builder of each ship's window may
append to it, and changes no figure another ship reads. Since SW-4's words step (2026-11-07) one
figure of the eight reads this table too: the topsail schooner's Musquidobit fit's 18-pounder
carronades, `ADYE_CARRONADE_CWT[18]`, 9 cwt in place of the shared table's 10, no source giving
the 10 (docs/dev/TuningNotes.md, "The words step").

Marks as the research notes give them: read, the page or its image; read (OCR), the OCR text
under docs/references/ only; judgement.
"""

# The weight of iron guns in hundredweight (112 lb) by the weight of their shot and their
# length in feet and inches: Adye, The Bombardier, and Pocket Gunner (1804), p. 155, "Length
# and Weight of English Iron Guns" (the page image, IA leaf n178, read: Research-Indefatigable-
# 2026-10.md §6.4; the 32-pounder read by two readers, Research-74-2026-10.md §4.2; the OCR,
# docs/references/adye/, loses the table's columns). The 24-pounder of 9 ft 6 in is 49 cwt 2 qr,
# of 9 ft 0 in 47 cwt 2 qr; the 9-pounder of 7 ft 6 in 24 cwt 2 qr.
ADYE_LONG_GUN_CWT = {
    32: {(9, 6): 55.0},
    24: {(10, 0): 52.0, (9, 6): 49.5, (9, 0): 47.5},
    18: {(9, 6): 42.0, (9, 0): 40.0},
    12: {(9, 6): 34.0},
    9: {(7, 6): 24.5},
}

# Carronades in hundredweight by the weight of their shot: Adye 1804 p. 72, "Carronades. Their
# Weight and Dimensions" (the page image, IA leaf n95, read: Research-Indefatigable-2026-10.md
# §6.4, Research-74-2026-10.md §4.2). The 42-pounder of 4 ft 3 1/2 in, 22 cwt 1 qr; the
# 32-pounder of 4 ft 0 1/2 in, 17 cwt 0 qr 14 lb; the 24-pounder of 3 ft 7 1/2 in, 13 cwt; the
# 18-pounder of 3 ft 3 in, 9 cwt. Of the two lengths Adye gives the 24 and the 18, the longer
# (Design-Ship-Indefatigable.md §5.3; the shorter, 3 ft 0 in of 11 cwt 2 qr 25 lb and 2 ft 4 in
# of 8 cwt 1 qr 25 lb).
ADYE_CARRONADE_CWT = {42: 22.25, 32: 17.125, 24: 13.0, 18: 9.0}

# The men to a gun by the weight of its shot "when the ship is well manned, so as to fight both
# sides at once occasionally", often with a boy besides to bring the powder: Falconer 1780,
# QUARTERS (OCR docs/references/falconer/, l.14315-14340, read (OCR)). The two-deckers' long
# guns are crewed by it (D31 (c) for the Indefatigable, Design-Ship-Indefatigable.md §5.3; the
# 74 by the owner's answer 12, Research-74-2026-10.md §13.1).
FALCONER_CREW = {42: 15, 32: 13, 24: 11, 18: 9, 12: 7, 9: 6, 6: 5, 4: 4, 3: 3}
# A carronade of any nature with taut breechings: its captain, two privates and a provider
# (Douglas, A Treatise on Naval Gunnery, 2nd ed. 1829, art. 136, p. 163; OCR
# docs/references/douglas/, l.7633-7645, read (OCR)).
DOUGLAS_CARRONADE_CREW = 4

# The 74's patterns, by the owner's answer 12 (Research-74-2026-10.md §13.1, from §4.2's bands):
# the long 32 of 9 ft 6 in and 55 cwt, the long 18 of 9 ft 0 in and 40 cwt, the 9 of 7 ft 6 in
# and 24 1/2 cwt; each a length of ADYE_LONG_GUN_CWT, which gives its weight.
SEVENTY_FOUR_PATTERNS = {32: (9, 6), 18: (9, 0), 9: (7, 6)}

# Ground tackle by the rate's guns: Steel 1794 vol. I, the folding anchor table and "A Cordage
# Table" (the page images, IA leaves n127 and n117, read by two readers: Research-Indefatigable-
# 2026-10.md §6.2). The 64's: four bowers of 57 cwt, a stream of 15 cwt and a kedge of 7 cwt
# 2 qr; seven bower cables of 21 in and the stream's of 11 1/2 in. Which bower is which and how
# the cables are laid on them is the ship's module's (Design-Ship-Indefatigable.md §7); the
# 74's row is her design's to append.
STEEL_ANCHORS = {
    64: {
        "bowers": 4,
        "bower_cwt": 57.0,
        "stream_cwt": 15.0,
        "kedge_cwt": 7.5,
        "bower_cables": 7,
        "bower_cable_in": 21.0,
        "stream_cable_in": 11.5,
    },
}

# The complement each column of the Regulations' table of officers and ratings stands for, by
# the rate's guns: the Regulations 1806, 1808 printing, p. 165 (IA leaf 176, the page images
# read: Research-Indefatigable-2026-10.md §4.2; OCR docs/references/admiralty/, l.10091-10093)
# makes 491 the 64, 343 the 50 and 294 the 44. The razee's company is set on the 44's column
# and the 64's on her own (Design-Ship-Indefatigable.md §6).
REGULATIONS_COLUMNS = {64: 491, 50: 343, 44: 294}

# A two-decker's note above her fit's `exercise_charges` (`gen_ships.exercise_allowance(n,
# decks=2)`), in the form of the one-decker's (`gen_ships.MAGAZINE_NOTES`).
TWO_DECKS_EXERCISE_NOTE = (
    "The Regulations' allowance for exercise a month: a charge and a round shot for a third of "
    "the upper deck guns in a ship of two or three decks, for six months after the guns are "
    "received (the Regulations 1806, 1808 printing, the Gunner, Art. XXI, l.13122-13144: 'one "
    "third of the number of the upper deck guns, in Ships of two or three decks'; the "
    "Captain's chapter, l.8842-8879, gives a third too); the first six months' figure, the "
    "game keeping no commissioning date (judgement)."
)

# -- the Prince de Neufchatel's appends (package 75, B2; Design-Ship-PrinceDeNeufchatel.md §5.3,
# §7). Adye 1804 p. 72 (the page image, IA leaf n95, read for her design): the 12-pounder
# carronade of 2 ft 2 in, bore 4.52 in, 5 cwt 3 qr 10 lb, to the hundredth. Adye p. 155 (the page
# image, IA leaf n178, read for her design): the long 6-pounder of 8 ft 0 in, 22 cwt, and of
# 6 ft 0 in, 16 cwt 2 qr. The shared tables' 6 and 20 cwt (`gen_ships.CARRONADE_CWT`,
# `LONG_GUN_CWT`), from memory, feed the eight files and stay as they are.
ADYE_CARRONADE_CWT[12] = 5.84
ADYE_LONG_GUN_CWT[6] = {(8, 0): 22.0, (6, 0): 16.5}

# Steel 1794 vol. I, the folding anchor table's row for "14 Guns, 300 Tons" (the page image, IA
# leaf n127, read for her design): three bowers of 20 cwt, a stream of 7 cwt and a kedge of 3 cwt
# 2 qr; and "A Cordage Table" (IA leaf n117, read), which has no column for 14 guns: its "Sloops"
# column, five bower cables of 13 1/2 in and a stream cable of 8 in, taken for a vessel of 14 guns
# and about 300 tons (judgement; the "20 guns" column, six cables of 14 1/2 in, the other). Keyed
# by the anchor table's guns, as the 64's row is.
STEEL_ANCHORS[14] = {
    "bowers": 3,
    "bower_cwt": 20.0,
    "stream_cwt": 7.0,
    "kedge_cwt": 3.5,
    "bower_cables": 5,
    "bower_cable_in": 13.5,
    "stream_cable_in": 8.0,
}

# -- the bilander's append (package 75, B4; Design-Ship-Bilander.md §3.6 task 6, §5.3). Adye 1804
# p. 155, "Length and Weight of English Iron Guns" (the page image, IA leaf n178, read for her
# window): the long 3-pounder of 18.6 calibres, 4 ft 6 in, 7 cwt 1 qr; the page's own proportion
# of metal to shot, 270, the check (7 cwt 1 qr of 112 lb over 3 lb). The shared table's 7 cwt
# (`gen_ships.LONG_GUN_CWT[3]`), from memory, feeds the eight files and stays as it is.
ADYE_LONG_GUN_CWT[3] = {(4, 6): 7.25}

# -- the 74's appends (package 75, B7; Design-Ship-Bellerophon.md §5.3, §6.1, §7). Lavery, The
# 74-Gun Ship Bellona (1985), p. 21, Table 17, the types of gun carried at various times (read
# (owner's book)): the long 18-pounder of 9 ft of 1812, 42 cwt, which Adye lacks (Adye's 9-ft gun
# is the 40-cwt one of 1761); the long 12-pounders of 1812, 9 ft and 34 cwt, 7 ft 6 in and 29 cwt;
# and the long 9-pounder of 8 ft 6 in of 1761, 27 1/2 cwt (Table 18 prints 27). Keyed as Adye's
# table, the length in feet and inches. Her design's rule for a weight (§5.3): Adye's where Adye
# gives the pattern, else this table; her 1812 fit's long guns are Lavery's types of 1812, which
# Adye's table of 1804 does not hold (the 18 of 42 cwt the design's own case; Adye's 12-pounders
# of 9 ft and 7 ft 6 in are 32 and 29 1/4 cwt, as package 81 read p. 155 for the viewer).
LAVERY_LONG_GUN_CWT = {
    18: {(9, 0): 42.0},
    12: {(9, 0): 34.0, (7, 6): 29.0},
    9: {(8, 6): 27.5},
}

# Steel 1794 vol. I, the folding anchor table's "Smaller 74 Guns" column and "A Cordage Table"
# (the page images, IA leaves n127 and n117, read: Research-74-2026-10.md §5.7): four bowers of
# 67 cwt, a stream of 16 cwt and a kedge of 8 cwt; seven bower cables of 22 in ("23 or 22" for
# the 74) and a stream cable of 12 1/2 in. Lavery 1985 p. 15, Table 4, a 74 about 1800 (read
# (owner's book)), gives the same anchors, and the cables below.
STEEL_ANCHORS[74] = {
    "bowers": 4,
    "bower_cwt": 67.0,
    "stream_cwt": 16.0,
    "kedge_cwt": 8.0,
    "bower_cables": 7,
    "bower_cable_in": 22.0,
    "stream_cable_in": 12.5,
}
# Lavery 1985 p. 15, Table 4, a 74's cables about 1800 (after NMM SPB 15, by Lavery p. 23): seven
# of 22 in and one of 13 1/2 in, each of 100 fathoms.
LAVERY_74_CABLES = {"bower_cables": 7, "bower_cable_in": 22.0, "stream_cable_in": 13.5}
LAVERY_74_CABLE_FATHOMS = 100.0

# The Regulations' table of officers and ratings (1806, 1808 printing, p. 165 and IA leaves
# 455-460, the page images read row by row: Research-74-2026-10.md §4.3): the 590 column is the
# 74's.
REGULATIONS_COLUMNS[74] = 590
