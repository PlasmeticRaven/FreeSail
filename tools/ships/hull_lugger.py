"""The lugger's hull as drawn: L'Éclair of 1795 (package 75, SW-2 with SW-2b.2; Build-Ships.md §5).

Her measured points, and her profile and form through `g.hull_profile` and `g.hull_form`, as the
64's and the razee's are built (`tools/ships/indefatigable.py`). `lugger()` in `tools/gen_ships.py`
calls `shape` once, the last thing it adds to her hull. The figures and every reading behind them
are `docs/design/ships-design/pages-zaz6306.md` (the note), whose §6 gives these lists in this
order, and `tests/test_hull_lugger.py` holds the file, this module and the note to each other. No
image is in the repository: Greenwich's sheets are read and cited, never copied.

**The rungs (Build-Ships.md §5.0).** S above the water: ZAZ6306, the gun lugger taken off afloat at
Portsmouth in 1795 (her stepped rail, her plan's outline, the post and the stem, the deck at side,
what that line is T, the band's heights; the round stern and no head). S† under it: Le Coureur on
ZAZ6170, her type (judgement), twenty years older (principle 7: lengths by 0.868, sections by
0.9135, her own 2 in of plank). T where neither reaches: the ends of the keel and the water, that
the band is her wale, and the side between the water and her main breadth, where her type's curve
is moved to meet her own plan. Each line below takes the word of its weakest point (`MARKS`).

**Drawn only (principle 8).** Nothing here moves a figure the physics or the gunnery reads. Her
draught, waterline, displacement and deck height stand as filed, and the green line is recorded
beside them. **As the lead ruled on 2026-10-31** (the note's §13.4): the sections by principle 7's
one factor, 2.53 m deep amidships; and her line at her sheet's length, not the file's, a departure
from principle 7's last sentence, whose words would make the length factor 0.793. The hold's floor
line is a depth of hold and no draught, and is not the measure.

**No port.** Her sheet draws none and no gun is in her file: her three guns are taken to fire over
the rail (the note's §6.4), which §5.1 gives no triple. `ports_m` and `port_size_m` are therefore
not given, as built by the lead's ruling; the triples a port would take are in the note and reported
by her test.
"""

from __future__ import annotations

import sys

import gen_ships as g

# -- her own sheet, ZAZ6306 (S; the note's §5, §6.1): x forward of the middle of its two
# perpendiculars, z above its green line, which is taken as the file's waterline; metres -----------

# The top of her side, taffrail to stem head, with its two steps (each given 0.01 m apart, the
# schema wanting x rising).
RAIL = [
    [-9.45, 2.84], [-9.03, 2.74], [-8.27, 2.60], [-7.51, 2.48], [-6.74, 2.39], [-5.98, 2.31],
    [-5.22, 2.24], [-4.44, 2.18], [-4.43, 1.62], [-3.70, 1.59], [-2.93, 1.55], [-2.17, 1.52],
    [-1.41, 1.50], [-0.65, 1.49], [0.00, 1.50], [0.88, 1.52], [1.64, 1.53], [2.40, 1.57],
    [3.16, 1.61], [3.92, 1.66], [4.09, 1.69], [4.10, 1.94], [4.69, 1.98], [5.45, 2.05],
    [6.21, 2.14], [6.97, 2.25], [7.73, 2.39], [8.50, 2.60], [9.03, 2.83],
]  # fmt: skip

# [x, hb_water, hb_rail]: the third the plan's outline (S); the second the stand-in's at the water
# (S†) from -8.69 to +8.85, the rest closing the line to her post and stem (T).
BREADTH = [
    [-9.02, 0.12, 0.27], [-8.95, 0.22, 0.54], [-8.84, 0.39, 0.81], [-8.69, 0.58, 1.09],
    [-8.43, 0.89, 1.36], [-8.24, 1.12, 1.63], [-7.51, 1.69, 2.21], [-6.74, 2.04, 2.55],
    [-5.98, 2.30, 2.73], [-5.22, 2.50, 2.83], [-4.46, 2.65, 2.89], [-2.93, 2.88, 2.96],
    [-1.41, 3.00, 2.98], [0.00, 3.06, 2.98], [1.64, 2.99, 2.97], [3.16, 2.83, 2.98],
    [4.69, 2.51, 2.97], [5.45, 2.21, 2.90], [6.21, 1.88, 2.77], [6.97, 1.36, 2.49],
    [7.73, 0.84, 2.07], [8.26, 0.49, 1.63], [8.50, 0.37, 1.36], [8.69, 0.27, 1.09],
    [8.85, 0.19, 0.81], [8.97, 0.15, 0.54], [8.99, 0.14, 0.27],
]  # fmt: skip

# The deck at side, line D2, over the length it can be traced.
DECKS = {
    "upper": [
        [-8.27, 1.17], [-7.51, 1.12], [-6.74, 1.07], [-5.98, 0.99], [-5.22, 0.94], [-4.46, 0.89],
        [-3.70, 0.83], [-2.93, 0.79], [-2.17, 0.78], [-1.41, 0.76], [-0.65, 0.75], [0.00, 0.74],
        [0.88, 0.75], [1.64, 0.76], [2.40, 0.78], [3.16, 0.81], [3.92, 0.84], [4.69, 0.89],
        [5.45, 0.97], [6.21, 1.08], [6.97, 1.14], [7.73, 1.21], [8.50, 1.28],
    ]
}  # fmt: skip

# The stem's fore edge, low to high: the foot (T), the dashed forefoot (tentative), above the water
# measured, and last the head at the perpendicular.
STEM = [
    [6.86, -2.18], [8.06, -1.79], [8.37, -1.69], [8.64, -1.52], [8.83, -1.32], [9.01, -1.10],
    [9.14, -0.83], [9.30, 0.00], [9.34, 0.42], [9.37, 1.07], [9.37, 1.83], [9.36, 2.42],
    [9.34, 2.91], [9.04, 2.92],
]  # fmt: skip

# The post's after edge, low to high: the heel (T), at the strip (dashed), at the water, the
# taffrail. No counter: the post rises straight to the taffrail.
STERN = [[-8.49, -2.98], [-8.66, -2.11], [-9.03, 0.00], [-9.45, 2.84]]

# The band between her lines B and C, the post's fore edge to where C fades: [x, z_lower, z_upper].
WALES = [
    [-9.14, 1.88, 2.07], [-8.27, 1.63, 1.87], [-5.98, 1.34, 1.58], [-2.93, 1.12, 1.36],
    [0.00, 1.07, 1.32], [3.16, 1.20, 1.43], [6.21, 1.47, 1.70], [7.73, 1.72, 1.95],
    [8.01, 1.75, 1.99],
]  # fmt: skip

# -- under the water, Le Coureur on ZAZ6170 at the factors (S†; the note's §6.2, §11, §13) ------

# The midship section, [z, hb], plank on: below 0.30 m Le Coureur's station 6; then her own rail.
SECTION = [
    [-2.53, 0.10], [-2.22, 0.15], [-2.00, 0.50], [-1.80, 0.95], [-1.60, 1.44], [-1.40, 1.88],
    [-1.20, 2.23], [-1.00, 2.49], [-0.80, 2.69], [-0.60, 2.83], [-0.40, 2.94], [-0.20, 3.02],
    [0.00, 3.07], [0.20, 3.10], [0.30, 3.10], [1.50, 2.98],
]  # fmt: skip

# The keel's lower edge, the post's heel to the forefoot: the two ends T.
KEEL = [
    [-8.49, -2.98], [-4.24, -2.77], [0.27, -2.53], [2.64, -2.40], [4.52, -2.30], [6.11, -2.22],
    [6.86, -2.18],
]  # fmt: skip

# [x, z, half-siding]: not drawn.
RABBET = [
    [-8.69, 0.00, 0.10], [-8.19, -2.10, 0.10], [-8.02, -2.67, 0.10], [-6.62, -2.59, 0.10],
    [-5.57, -2.53, 0.10], [-4.24, -2.46, 0.10], [-2.36, -2.36, 0.10], [0.27, -2.22, 0.10],
    [2.64, -2.10, 0.10], [4.52, -2.00, 0.10], [6.11, -1.91, 0.10], [7.43, -1.84, 0.10],
    [8.03, -1.60, 0.10], [8.36, -1.34, 0.10], [8.54, -1.09, 0.10], [8.66, -0.84, 0.10],
    [8.75, -0.59, 0.10], [8.84, -0.34, 0.10], [8.91, 0.00, 0.10],
]  # fmt: skip

# The main breadth, [x, z, hb]: its height Le Coureur's at the factors (S†); its half-breadth her
# own plan's outline with a tumblehome fading from 0.114 m amidships (T).
BREADTH_LINE = [
    [-8.23, 0.96, 1.70], [-7.43, 1.01, 2.33], [-6.62, 0.91, 2.68], [-5.57, 0.74, 2.89],
    [-4.24, 0.74, 3.01], [-2.36, 0.50, 3.08], [0.27, 0.40, 3.09], [2.64, 0.62, 3.09],
    [4.52, 0.77, 3.08], [6.11, 1.29, 2.89], [7.43, 1.50, 2.32], [8.25, 1.77, 1.70],
]  # fmt: skip

# By Le Coureur's numbered stations, aft to forward: her x, then [z, hb] low to high, read from
# ZAZ6170's body plan at the heights given. Up to z = 0 each is at the factors with her plank on
# (S†). Above it (T; the note's §6.2) the same curve at the factors, moved straight in height by
# what her main breadth has over or under Le Coureur's there, and never past it: so the side rounds
# as her type's does, and does not run straight from the water to a corner at the main breadth.
STATIONS = {
    "12": (-8.23, [[-0.60, 0.18], [-0.40, 0.38], [-0.20, 0.73], [0.00, 1.13],
                   [0.20, 1.41], [0.40, 1.59], [0.60, 1.68], [0.80, 1.70]]),
    "11": (-7.43, [[-1.25, 0.19], [-1.00, 0.28], [-0.80, 0.34], [-0.60, 0.56], [-0.40, 0.92],
                   [-0.20, 1.40], [0.00, 1.75],
                   [0.20, 1.96], [0.40, 2.11], [0.60, 2.22], [0.80, 2.29]]),
    "10": (-6.62, [[-1.50, 0.28], [-1.25, 0.39], [-1.00, 0.51], [-0.80, 0.75], [-0.60, 1.11],
                   [-0.40, 1.54], [-0.20, 1.88], [0.00, 2.09],
                   [0.20, 2.28], [0.40, 2.44], [0.60, 2.55], [0.80, 2.64]]),
    "9": (-5.57, [[-2.25, 0.15], [-2.00, 0.26], [-1.75, 0.35], [-1.50, 0.50], [-1.25, 0.70],
                  [-1.00, 1.04], [-0.80, 1.41], [-0.60, 1.80], [-0.40, 2.09], [-0.20, 2.29],
                  [0.00, 2.42],
                  [0.20, 2.58], [0.40, 2.71], [0.60, 2.82]]),
    "8": (-4.24, [[-2.00, 0.35], [-1.75, 0.55], [-1.50, 0.85], [-1.25, 1.24], [-1.00, 1.73],
                  [-0.80, 2.05], [-0.60, 2.31], [-0.40, 2.50], [-0.20, 2.62], [0.00, 2.70],
                  [0.20, 2.81], [0.40, 2.89], [0.60, 2.96]]),
    "7": (-2.36, [[-2.00, 0.48], [-1.75, 0.86], [-1.50, 1.40], [-1.25, 1.89], [-1.00, 2.29],
                  [-0.80, 2.52], [-0.60, 2.71], [-0.40, 2.81], [-0.20, 2.90], [0.00, 2.96],
                  [0.20, 3.01], [0.40, 3.06]]),
    "6": (0.27, [[-2.00, 0.50], [-1.75, 1.07], [-1.50, 1.67], [-1.25, 2.15], [-1.00, 2.49],
                 [-0.80, 2.69], [-0.60, 2.83], [-0.40, 2.94], [-0.20, 3.02], [0.00, 3.07],
                 [0.20, 3.09]]),
    "5": (2.64, [[-1.75, 0.68], [-1.50, 1.20], [-1.25, 1.72], [-1.00, 2.14], [-0.80, 2.40],
                 [-0.60, 2.59], [-0.40, 2.74], [-0.20, 2.84], [0.00, 2.93],
                 [0.20, 3.00], [0.40, 3.05]]),
    "4": (4.52, [[-1.50, 0.65], [-1.25, 1.04], [-1.00, 1.48], [-0.80, 1.81], [-0.60, 2.07],
                 [-0.40, 2.29], [-0.20, 2.45], [0.00, 2.57],
                 [0.20, 2.74], [0.40, 2.87], [0.60, 2.99]]),
    "3": (6.11, [[-1.50, 0.32], [-1.25, 0.53], [-1.00, 0.79], [-0.80, 1.02], [-0.60, 1.27],
                 [-0.40, 1.53], [-0.20, 1.76], [0.00, 1.95],
                 [0.20, 2.17], [0.40, 2.36], [0.60, 2.52], [0.80, 2.65], [1.00, 2.75]]),
    "2": (7.43, [[-1.50, 0.18], [-1.25, 0.27], [-1.00, 0.37], [-0.80, 0.48], [-0.60, 0.59],
                 [-0.40, 0.74], [-0.20, 0.88], [0.00, 1.04],
                 [0.20, 1.29], [0.40, 1.52], [0.60, 1.73], [0.80, 1.92], [1.00, 2.06],
                 [1.25, 2.21]]),
    "1": (8.25, [[-1.00, 0.17], [-0.80, 0.23], [-0.60, 0.28], [-0.40, 0.35], [-0.20, 0.41],
                 [0.00, 0.50],
                 [0.20, 0.64], [0.40, 0.79], [0.60, 0.95], [0.80, 1.10], [1.00, 1.26],
                 [1.25, 1.44], [1.50, 1.58]]),
}  # fmt: skip

# -- the form and the rungs -------------------------------------------------------------------

# Round at the rail, no counter and no head (S): no transom, galleries or lights are on her sheet,
# and none is invented (principle 9).
FORM = {"stern": {"type": "round"}, "head": "none"}

# Each line by its weakest point (principle 4; the note's §6.5).
MARKS = {
    "rail_m": "sourced",
    "breadth_m": "judged",  # its water's two ends only; between them the stand-in's, its rail hers
    "keel_m": "judged",  # its two ends; between them the stand-in's
    "stem_m": "judged",  # its foot only; above it her own
    "stern_m": "judged",  # its heel only; above it her own
    "wales_m": "judged",  # its heights hers (S); that it is her wale, T
    "section_m": "stand-in",
    "decks_m": "judged",  # its heights hers (S); what the line is, T
    "breadth_line_m": "judged",
    "sections_m": "judged",  # above the water only; up to it the stand-in's
    "rabbet_m": "stand-in",
    "form.stern": "sourced",
    "form.head": "sourced",
}

# The file's notes: sources, departures and judgements, no figure a rule computes from her keys
# (the lead's notes of 2026-10-29, item 2; those are the report's).
NOTES = {
    "profile": (
        "Her lines (Build-Ships.md §5; docs/design/ships-design/pages-zaz6306.md, the note): x "
        "forward of the middle of ZAZ6306's two perpendiculars, z above its green line, taken as "
        "the file's waterline and recorded beside it, not moved; metres, plank on. Above the "
        "water her own sheet (S), but for the curve of the side up to her main breadth (T, the "
        "note's §6.2); under it Le Coureur on ZAZ6170, her type (judgement; S†, the note's §13), "
        "lengths by 0.868, sections by 0.9135, her own 2 in of plank. A departure "
        "from §5.0 principle 7's last sentence: her line is drawn at her sheet's length, not the "
        "file's, so that her own rail, plan and stem stand (the note's §13.4). No port: her sheet "
        "draws none, and her three guns are taken to fire over the rail (judgement, the note's "
        "§6.4)."
    ),
    "profile.rail_m": (
        "The top of her side from the taffrail to the stem head, with its two steps at 15.07 and "
        "43.04 ft from the after perpendicular (measured on ZAZ6306, ±0.05 ft: the note's §5.2; "
        "each step given 0.01 m apart)."
    ),
    "profile.breadth_m": (
        "By station. At the rail, the outline of ZAZ6306's plan (measured, ±0.03 ft, the note's "
        "§5.2; judgement that it is the side at the deck). At the water, Le Coureur's at the "
        "factors (S†, the note's §11.4), the three figures aft of x -8.75 and the two at +8.97 and "
        "+8.99 closing the line to her post and stem (T: Le Coureur's water ends square on her "
        "tuck, and she is round). Her plan is fuller than Le Coureur's at both ends, so her side "
        "flares from the water to the rail there, which no sheet of her confirms (the note's "
        "§13.3)."
    ),
    "profile.keel_m": (
        "The keel's lower edge, the post's heel to the forefoot: Le Coureur's at the factors (S†, "
        "ZAZ6170's body plan, the note's §11.6), its two ends where her own dashed post and "
        "forefoot, carried on, meet it (T). Her body is not turned from Le Coureur's drag to the "
        "green line's (judgement, the note's §6.2). Her file's draught stands; to read: the "
        "scantling document held with ZAZ6306, not scanned (the note's §8)."
    ),
    "profile.stem_m": (
        "The stem's fore edge, low to high: its foot her dashed forefoot carried on to the "
        "stand-in's keel (T); the dashed forefoot (measured on ZAZ6306, tentative); above the "
        "water measured, tentative above 7.9 ft on a faint line; its head at the perpendicular "
        "(the note's §5.3, §6.1)."
    ),
    "profile.stern_m": (
        "The post's after edge, low to high: its heel carried on to the stand-in's keel (T); at "
        "the sheet's scale strip, dashed; at the water; the taffrail (measured on ZAZ6306, the "
        "note's §4, §5.3). No counter."
    ),
    "profile.wales_m": (
        "The band between her lines B and C, the only band on her side, above her deck (its "
        "heights measured on ZAZ6306, ±0.1 ft, the note's §5.1). That it stands for the main wale "
        "is judgement (T). Her sheet is an inboard profile and blank below the deck, which does "
        "not show she had no wale there; none is given her, Le Coureur's at the factors standing "
        "across her deck at side (the note's §6.1)."
    ),
    "profile.section_m": (
        "The midship section: below 0.30 m Le Coureur's station 6 at the factors, the mean of its "
        "two halves on ZAZ6170's body plan (S†, the note's §11.4), so Chapelle 1930's 'great "
        "deadrise' (OCR l. 508) is measured on her type; above it her own rail (S, the note's "
        "§5.2)."
    ),
    "profile.decks_m": (
        "The deck at side: line D2 of ZAZ6306 (measured, ±0.1 ft, the note's §5.1), over the "
        "length it can be traced; judgement that it is the deck at side or the plank's underside, "
        "within an inch either way. The file's deck height stands, recorded beside it (the note's "
        "§7)."
    ),
    "profile.breadth_line_m": (
        "The main breadth by station: its height Le Coureur's at the factors (S†, the note's "
        "§11.4); its half-breadth her own plan's outline with a tumblehome fading from the "
        "difference between the caption's 20 ft 4 in and the plan's 19 ft 7 in (judgement, the "
        "note's §6.3)."
    ),
    "profile.sections_m": (
        "Le Coureur's numbered stations 12 to 1, read from ZAZ6170's body plan (measured, the "
        "note's §11.4) at the factors with her plank on: her type's body, not hers, no sheet of "
        "her having a body plan (S†). Above the water the same curves moved to meet her own main "
        "breadth, her plan being fuller at the ends and narrower at station 12 (T, the note's "
        "§6.2). Chapelle 1930 p. 7 and ZAZ4734 are its checks (the note's §11.9, §13.2); stations "
        "12 and 1 the least sure."
    ),
    "profile.rabbet_m": (
        "Not drawn. Its two after points her post's dashed fore edge (tentative); the rest Le "
        "Coureur's on ZAZ6170 at the factors, the half-siding hers at the factor (S†, the note's "
        "§6.2)."
    ),
    "profile.form": (
        "As ZAZ6306 draws her (the note's §5.2, §5.3, §6.3): round at the rail with no counter, "
        "transom, galleries or lights, and a plain stem head with no knee. Le Coureur's square "
        "tuck is not hers."
    ),
    "profile.marks": (
        "Each line by its weakest point (Build-Ships.md §5.0 principle 4); where along the hull "
        "each stands is in its note."
    ),
}


def sections() -> list[list[float]]:
    """`STATIONS` as `sections_m`'s points, [x, z, hb], aft to forward."""
    return [[x, z, hb] for x, points in STATIONS.values() for z, hb in points]


def shape(hull: dict, notes: dict) -> None:
    """Her profile, form and marks added to her hull mapping, and each line's note to her notes.
    What the form computes from her keys goes to the generator's report on stderr, not the notes."""
    hull["profile"] = g.hull_profile(
        RAIL,
        BREADTH,
        keel=KEEL,
        stem=STEM,
        stern=STERN,
        wales=WALES,
        section=SECTION,
        decks=DECKS,
        breadth_line=BREADTH_LINE,
        sections=sections(),
        rabbet=RABBET,
    )
    notes.update(NOTES)
    report: list[str] = []
    g.hull_form(hull, form=FORM, marks=MARKS, measured=(), report=report)
    for line in report:
        print(f"lugger: {line}", file=sys.stderr)
