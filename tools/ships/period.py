"""The period's tables the new ships share (package 75; docs/design/Build-Ships.md §3.1 item 3;
Design-Ship-Indefatigable.md §5.3, §7 and §12.1 item 4): constants with their sources, importing
nothing and calling nothing, read by a ship's module beside the generator's helpers.

The eight files' own tables stay as they are (`gen_ships.LONG_GUN_CWT`, `CARRONADE_CWT`, and
the crews of `gen_ships.gun_crew`, a judgement reading of Douglas). Adye's 18-pounder carronade
(9 cwt) and 9-pounder (24 1/2) differ from the shared tables' 10 and 26, from memory, which
feed the eight files: so the new ships read this one sourced table and no figure of the eight
moves (Design-Ship-Indefatigable.md §5.3). After stage 0 the builder of each ship's window may
append to it, and changes no figure another ship reads.

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
