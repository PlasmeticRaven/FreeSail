"""Generate the four reference ship files from documented particulars and period rules.

Run from the repository root:  python tools/gen_ships.py [output directory]

This script is the source of `data/ships/frigate-36.yaml`,
`data/ships/topsail-schooner.yaml`, `data/ships/cutter.yaml` and
`data/ships/brig.yaml`. Do not hand-edit those files: change the numbers or
rules here and regenerate, so that the files, the rules that produced them and
the citations stay together (`git diff` must be empty after a run). Every
number that is a judgement rather than a citation is marked "judgement" in the
comment the script writes next to it.

How the numbers are made
------------------------

Hull particulars are taken from published dimensions (the frigate: the
Amazon class of 1795; the schooner: Kemp's Lynx of 1812, from the Admiralty
draught Chapelle reproduces in The Baltimore Clipper, 1930; the cutter:
Sherbourne of 1763, 85 tons, 54 ft 6 in by 19 ft; the brig: Harpy of 1796,
316 tons, 95 ft on the gun deck, 75 ft 1 5/8 in of keel, 28 ft 1 1/2 in of
beam, 12 ft 0 1/2 in of hold, both from the printed dimensions noted in
docs/design/VesselCandidates.md) and converted: gundeck and keel length to a
load waterline, burthen to a displacement, the "depth in hold" to a draught.
The schooner's rig, whose spar dimensions Chapelle could not find, is
reconstructed as he prescribes: by Fincham's masting rules, checked against
the spar tables he prints (Sea Lark 1812, Spider 1835) and Marestier's
measured schooners of 1820. The cutter's rig (package 32b) is Fincham 1843
p. 67, the second revenue cruiser's column of his cutter table (main mast
hounded 2.6 x the beam, boom 0.87 of the length, gaff 0.64 of the boom,
bowsprit 0.79 of the length, square-sail yard 0.84, the topsail and
topgallant yards 0.70 and 0.44 of it) with arts. 86 and 87 (pp. 35 to 36) for
the mast's place and the sails' proportions and his footnote on the 85-ton
cutter's canvas (mainsail 1566, foresail 367, second jib 541 sq ft); her sails
are cut by Steel 1794 (the cutter's mainsail p. 120, the sloop's square sail,
topsail and topgallant pp. 124 to 126, the smack's foresail and jib, the storm
jib p. 190), and her bowsprit runs in and out (a `running` bowsprit with a
`housed_length_m`, the one addition the two ships needed of the file format).
The brig's rig is Fincham 1843 p. 88, the first brig of war (100 x 30.5 ft)
scaled to Harpy, with pp. 82 to 83 for the placing of her masts and Steel's
brig's mainsail (p. 119, No. 5 or 6 canvas, three reef bands) for the boom
mainsail; her head sails, staysails, studding sails and storm canvas follow
the frigate's rules at her size.

Spar lengths follow the proportional rules that the period's own masting
texts give. The chain of rules used for the frigate is Luce 1866, ch. VII
"The Mast" (mast-making; yards and booms), cross-checked against Falconer
1780, art. YARD (the table of yard lengths by class of ship: for "all the
rest" below 44 guns, main yard = 0.575 x gun-deck length). Luce's rules:

    main mast (heel to truck) = (LWL + extreme breadth) / 2
    head of a lower mast      = 1/6 of its length
    fore mast                 = 9/10 of the main, in all its proportions
    mizzen mast               = 13/15 of the main in length
    main topmast              = 3/5 of the main mast; head 1/6 of itself
    topgallant masts          = 1/2 of their topmasts
    royal masts               = 2/3 of the topgallant masts
    bowsprit                  = 5/8 of the main mast, one third inboard
    jib-boom                  = 6/7 of the bowsprit, 7/12 of it outboard
    main yard                 = 10/11 of the main mast
    main topsail yard         = 3/4 of the main yard
    main topgallant yard      = 9/14 of the topsail yard
    yards of the fore         = 9/10 of the main's; of the mizzen 5/7
    spanker boom              = 1/2 of the main mast; gaff 4/5 of the boom
    studding-sail booms       = 1/2 of the yard they are rigged on

Sail areas follow from the spars: a square sail is a trapezoid between its
own yard (head) and the yardarms of the yard below (foot), as deep as the
hoist between them (Lever 1827, "Sails": cloths gored from the clews to the
head; Falconer, art. SAIL: the clews of a topsail are drawn out to the
extremities of the lower yard by the topsail sheets). Fore-and-aft sails
are drawn between their spars.

Line ratings come from rope. Luce 1866 ch. IV "Rope" (and 1884 ch. IV):
the breaking strain of tarred hemp Government rope is 1044.9 lb times the
square of the circumference in inches, and "no cordage should be subjected
to a strain above one-third of its estimated strength". So a line's
rating_kn, the load at which the strain rule (spec 7.5) begins to tell, is
one third of the breaking strain of a rope of the size that line was made
of. A purchase multiplies the fall's rating by its parts. The engine then
parts a line when the load passes 1.5 x rating: half the breaking strain of
the new rope, which is what a season's chafe, a splice or a knot leaves.
Rope sizes for lower rigging follow Luce 1866 ch. VIII ("first rates, fore
and main 10 1/2 inch; the size diminishes one inch for each succeeding
class of vessel"; a frigate's forestay collar is "eight-inch for a
frigate", ch. X). Running-rigging sizes are the customary proportions of an
18-pounder frigate's establishment; the OCR references do not reproduce
Steel's 1794 tables, so they are judgements against the owner may check.

Spar ratings cannot come from a rope table. They are set by the rule that
a spar is expected to stand with all the sail it carries (studding sails
excepted) set in the strongest wind in which period practice would still
have that sail on her: royals to 20 knots, topgallants to 25, topsails and
topmasts to 40 (a whole gale, reefed), lower masts and yards to 55. The
rating is the sustained load the engine puts on the spar in that wind,
computed here as the static force at the class's peak coefficient times
SUSTAINED_FRACTION, which was measured with tools/measure_loads.py (heel,
the ship's own way and an imperfect trim leave the sustained load at about
that fraction of the static peak). Those winds were chosen to give truth 9
(spec 7.6: royals and topgallants carried away in 35 knots on a reach under
all sail, nothing in 20 knots under plain sail) with the current sail
curves; they are provisional until package 10 retunes the curves, and the
comment on each spar says so.

Brace limits are kept from integration: Luce 1866 ch. XXIV, "Trimming
yards", d'Ulloa found the yard should make 28 degrees with the keel when
sharp up, Fincham 19; the limits here are 55 to 62 degrees from square
(35 to 28 of yard to keel), the upper yards a little sharper.
"""

from __future__ import annotations

import copy
import importlib
import math
import os
import re
import sys

import yaml

# The rating pass loads the doc through the engine's own loader; run as a script from a
# checkout that is not installed, the repository root must be importable.
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

SIDES = ("starboard", "larboard")
FT = 0.3048

# Luce 1866 ch. IV: breaking strain of tarred hemp = 1044.9 lb x circumference^2 (inches);
# working load one third of that. In kN per square inch of circumference:
ROPE_KN_PER_SQ_IN = round(1044.9 * 4.44822 / 1000.0 / 3.0, 4)  # 1.5493

# The engine's force coefficient at the peak of each class's curve (data/sail_classes.yaml,
# |(C_L, C_D)| at the best angle). Package 10: if the curves change, change these and rerun.
PEAK_COEFF = {"square": 1.23, "studding": 1.25, "gaff": 1.29, "jibheaded": 1.32, "lug": 1.29}
# Package 75 (docs/design/Design-ShipsEngineExtensions.md §3.1): the lateen row's 1.15 and 0.48
# at its best angle, 35 degrees, give 1.246 by the same rule. No file of the eight carries a
# lateen sail; without the entry the rating pass would fail on the first that does.
PEAK_COEFF["lateen"] = 1.25

# Sustained load / static peak-coefficient load, measured with tools/measure_loads.py on the
# frigate on a beam reach with the yards trimmed to the wind: 0.9 at 35 knots under all
# sail, 0.7 at 20 knots under plain sail (heel takes area away, the ship's own way adds
# apparent wind, the trim is a little off the peak). Re-measured by package 10 with its
# curves (run the tool with PYTHONPATH=.): at 20 knots under plain sail the topgallant
# yards sit at 0.72 of rating on the frigate and 0.70 on the schooner; at 35 knots under
# all sail the royals and topgallants go within twelve minutes (truth 9).
SUSTAINED_FRACTION = 0.85

# Wind (knots, true, at 10 m) in which a spar is expected to stand with all its sail set.
# Chosen for truth 9 with the current curves; provisional until package 10 (see docstring).
DESIGN_WIND_KN = {
    "lower": 55.0,  # lower masts and yards, bowsprit: a storm, and they carry courses reefed
    "topsail": 40.0,  # topmasts and topsail yards: a whole gale under close-reefed topsails
    "topgallant": 25.0,  # topgallant masts and yards: a strong breeze is their limit
    "royal": 20.0,  # royal masts and yards: royals come in when it freshens
    "jib_boom": 30.0,  # the jib is a stout sail, the boom less so
    "flying_jib_boom": 22.0,  # a light spar for a light sail
    "gaff": 45.0,  # spanker gaff and boom: the spanker is carried reefed in a gale
    "studding": 18.0,  # studding-sail booms: light spars, fair-weather sails
}

# Canvas (milestone 3b, package 22; spec 3b §6.1, docs/references/RigGeometryNotes.md §4).
# Every sail is given the number of the canvas it is made of, 1 the heaviest ("The strongest
# Canvas is called No. 1, and it decreases gradually to No. 8": Lever 1808, 1827 printing,
# 'Sails'), and its cloth rating follows from the number: freesail.ship.parts.cloth_rating_for,
# which is
# CLOTH_KN_PER_M2_NO2 (0.9 kN/m2, milestone 2's rating for courses and topsails, all of No. 2)
# times the canvas's crosswise strength relative to No. 2 (Luce 1884 App. E pp. 610-611,
# docs/references/Tables.md §2) times the area. So every No. 2 sail keeps its milestone 2
# rating exactly, and the rest follow Luce's strengths. Milestone 2 rated the canvas by level
# instead (kN/m2: courses and topsails 0.9, topgallants 0.30, royals 0.25, studding sails 0.20,
# jib-headed sails 0.50, gaff sails 0.70); the numbers below replace that table.
#
# The numbers are period practice for the ship of 1795 first: Steel 1794 vol. I, 'The Practice
# of Sail-making', gives the navy's number for each sail (its article named in each comment),
# with Kipping 1847 for the frigate's studding sails and jibs; Luce 1884 ch. X p. 171
# (Tables.md §1, the Trenton's allowance) is the rule where Steel's range contains his number,
# and is named where it differs. The research notes' rule (spec 3b §6.1: topgallants 4 and 6,
# royals 8 and 9, jib 2, flying jib 5, lower studding sails 5) was drawn from Luce because
# Steel's topsail and topgallant articles were not found in the OCR at the time; they are
# there (Steel's 'Main-topsail', 'Main-topgallant-sail' and the rest), and for a frigate of
# 1795 they win. The schooner takes the same number as the frigate's sail at the same height,
# or Steel's for a sloop or cutter where he gives her kind of sail.
STEEL_SM = "Steel 1794 vol. I, Sail-making"
KIPPING_SM = "Kipping 1847 (1898 printing), Sails and Sailmaking"
LUCE_171 = "Luce 1884 ch. X p. 171 (Tables.md §1)"
FRIGATE_CANVAS: dict[str, tuple[int, str]] = {
    "fore.course": (
        2,
        f"{STEEL_SM}, 'Fore-course': No. 1 or 2; {LUCE_171}: the working foresail of No. 2, "
        "the heavy one of No. 1 (in the sail room)",
    ),
    "main.course": (2, f"{STEEL_SM}, 'Main-course': No. 1 or 2; {LUCE_171}: No. 2"),
    "fore.topsail": (
        2,
        f"{STEEL_SM}, 'Fore-topsail': No. 2 or 3; {LUCE_171}: the working topsail of No. 2, "
        "the heavy one of No. 1 (in the sail room)",
    ),
    "main.topsail": (
        2,
        f"{STEEL_SM}, 'Main-topsail': No. 2 or 3; {LUCE_171}: the working topsail of No. 2, "
        "the heavy one of No. 1 (in the sail room)",
    ),
    "mizzen.topsail": (
        4,
        f"{STEEL_SM}, 'Mizen-topsail': No. 4, 5 or 6, the heaviest taken; {LUCE_171} gives "
        "No. 3 for the Trenton's",
    ),
    "fore.topgallant": (
        6,
        f"{STEEL_SM}, 'Fore-topgallant-sail': No. 6 or 7; {KIPPING_SM}: 'In the royal navy the "
        f"topgallant-sails are made of No. 6'; {LUCE_171} gives No. 4 for the Trenton's",
    ),
    "main.topgallant": (
        6,
        f"{STEEL_SM}, 'Main-topgallant-sail': No. 6 or 7; {KIPPING_SM}: No. 6 in the royal "
        f"navy; {LUCE_171} gives No. 4",
    ),
    "mizzen.topgallant": (
        7,
        f"{STEEL_SM}, 'Mizen-topgallant-sail': No. 7 or 8; {LUCE_171} gives No. 6",
    ),
    "fore.royal": (8, f"{STEEL_SM}, 'Fore-royal-sail': No. 8; {LUCE_171}: No. 8"),
    "main.royal": (8, f"{STEEL_SM}, 'Main-royal-sail': No. 8; {LUCE_171}: No. 8"),
    "mizzen.royal": (
        8,
        f"{STEEL_SM}, 'Mizen-royal-sail': No. 8, the lightest of his numbers (Lever 1808, 'Sails': "
        f"'decreases gradually to No. 8'); {LUCE_171} gives No. 9",
    ),
    "mizzen.spanker": (
        2,
        f"{STEEL_SM}, 'Mizen-course' (the gaff mizzen of 1794): No. 2 or 3; {LUCE_171}: the "
        "spanker of No. 2",
    ),
    "fore.topmast_staysail": (
        6,
        f"{STEEL_SM}, 'Fore topmast staysail': No. 5, 6 or 7 (the OCR reads '6, 6, or 7'); "
        f"{KIPPING_SM}: 'in the royal navy it is made of No. 6'",
    ),
    "jib": (
        6,
        f"{STEEL_SM}, 'Jib' ('the foremost sail of a ship'): No. 6 or 7; {KIPPING_SM}, 'Outer "
        "jib', on the stay from the jib-boom end to the fore topmast, as this one: No. 6. "
        f"{LUCE_171} gives No. 2, the jib of 1884 being the working headsail",
    ),
    "flying_jib": (
        7,
        f"judgement: Steel's jib range (No. 6 or 7) at its lighter end, the flying jib setting "
        f"outside and above the jib; {LUCE_171} makes his three numbers lighter than the jib",
    ),
    "main.topmast_staysail": (
        5,
        f"{STEEL_SM}, 'Main topmast staysail': No. 5 or 6; {KIPPING_SM}: No. 6 in the royal navy",
    ),
    # package 57: the staysails between the masts from Steel's articles (the OCR's lines
    # 12222 to 12820; 'Mizen staysail', 'Middle staysail' and the rest)
    "main.staysail": (
        2,
        f"{STEEL_SM}, 'Main staysail': 'made of canvas No. 1 to 3', the middle taken",
    ),
    "middle_staysail": (6, f"{STEEL_SM}, 'Middle staysail': 'No. 6, or 7', the heavier"),
    "main.topgallant_staysail": (7, f"{STEEL_SM}, 'Main topgallant staysail': 'canvas No. 7'"),
    "mizzen.staysail": (2, f"{STEEL_SM}, 'Mizen staysail': 'No. 2 or 3', the heavier"),
    "mizzen.topmast_staysail": (
        7,
        "Steel 1794's navy number as docs/references/RigGeometryNotes.md reads it (No. 7); his "
        "article is not in the OCR",
    ),
    "mizzen.topgallant_staysail": (
        8,
        f"judgement: {STEEL_SM}, 'Royal staysails': 'canvas No. 8 ... the same as a "
        "topgallant-staysail', the lightest of his numbers for the lightest of the staysails",
    ),
    "lower studding": (
        6,
        f"{KIPPING_SM}, 'On Studding-sails': 'Under frigates of the second class to frigates "
        "of the sixth class inclusive, the lower and top studding-sails are made of No. 6'; "
        f"{STEEL_SM}, 'Lower Fore Studdingsails': No. 6 or 7",
    ),
    "topmast studding": (
        6,
        f"{KIPPING_SM}: frigates' top studding-sails No. 6; {STEEL_SM}, 'Fore Topmast "
        "Studdingsails': No. 6 or 7",
    ),
    "topgallant studding": (
        7,
        f"{KIPPING_SM}: frigates' topgallant studding-sails 'No. 7 or No. 8'; {STEEL_SM}: "
        "No. 7 or 8",
    ),
    "storm": (
        1,
        f"{LUCE_171}: every storm sail of No. 1; Luce 1884 ch. X, 'Storm-Sails are made of the "
        "strongest canvas'",
    ),
    "ringtail": (
        5,
        f"{KIPPING_SM}, 'Ringtail Sails' (a brig's): No. 5 or 6; {STEEL_SM}, 'Sloop's ringtail "
        "sail': No. 5 or 8",
    ),
    "save-all": (
        7,
        f"judgement: no source gives a ship's save-all; {STEEL_SM}, 'Sloop's water-sail', "
        "No. 7, 'Some ships have a water-sail, similar to a sloop's'",
    ),
}
SCHOONER_CANVAS: dict[str, tuple[int, str]] = {
    "fore.topsail": (
        2,
        f"as the frigate's topsails ({STEEL_SM}, 'Fore-topsail': No. 2 or 3; {LUCE_171}: "
        "No. 2); Steel's 'Sloop's topsail', No. 6 or 7, is a cutter's light flying topsail, "
        "not the schooner's reefing topsail (judgement)",
    ),
    "fore.topgallant": (
        6,
        f"as the frigate's topgallants ({STEEL_SM}: No. 6 or 7); Steel's 'Sloop's "
        "topgallant-sail' is No. 8",
    ),
    "fore.sail": (
        2,
        f"{STEEL_SM}, 'Cutter's mainsail' and the sloop's mainsail: No. 1 or 2; the lower "
        "sails of the frigate are No. 2",
    ),
    "main.sail": (2, f"{STEEL_SM}, 'Cutter's mainsail' and the sloop's mainsail: No. 1 or 2"),
    "main.gaff_topsail": (8, f"{STEEL_SM}, 'Sloop's gaff topsail': No. 8"),
    "fore.staysail": (
        2,
        f"{STEEL_SM}, 'Smack's foresail': No. 1 or 2; 'Fore staysail' (a ship's, on the fore "
        "stay): No. 1 to 3",
    ),
    "jib": (2, f"{STEEL_SM}, 'Smack's jib': No. 1 or 2; the sloop's first jib No. 2 to 6"),
    "flying_jib": (6, f"{STEEL_SM}, 'Sloop's flying jib': No. 6"),
    "topmast studding": (6, "as the frigate's topmast studding sails (Kipping, Steel: No. 6)"),
    "storm trysail": (
        1,
        f"{STEEL_SM}, 'Sloop's trysail, or storm mainsail': No. 1 or 2; {LUCE_171}: storm "
        "sails of No. 1",
    ),
    "storm jib": (
        1,
        f"{STEEL_SM}, the sloop's jibs (p. 190): 'No. 1 or 2 ... two-thirds of the size of the "
        "first jib, and is used in stormy weather, in lieu of a larger one'",
    ),
    "ringtail": (
        5,
        f"{STEEL_SM}, 'Sloop's ringtail sail': No. 5 or 8; {KIPPING_SM}, a brig's: No. 5 or 6",
    ),
    "water sail": (7, f"{STEEL_SM}, 'Sloop's water-sail': No. 7"),
}


def cloth(area_m2: float, canvas_no: int) -> float:
    """The cloth rating, kN, of a sail of this area and canvas (freesail.ship.parts)."""
    from freesail.ship.parts import cloth_rating_for

    return cloth_rating_for(area_m2, canvas_no)


def storm_cloth(area_m2: float) -> float:
    """A storm sail's cloth rating, kN (package 45): rated for the wind it is cut for,
    seventy knots apparent, and not by the square metre as the working canvas is
    (freesail.ship.parts.storm_cloth_rating_for, with the reasoning)."""
    from freesail.ship.parts import storm_cloth_rating_for

    return storm_cloth_rating_for(area_m2)


def canvas_note(canvas: tuple[int, str], storm: bool = False) -> str:
    """The comment text for a sail's canvas: its number, the source, and the rating rule;
    for storm canvas (package 45) the rating for the wind it is cut for."""
    from freesail.ship.parts import (
        CLOTH_KN_PER_M2_NO2,
        STORM_CANVAS_APPARENT_KN,
        STORM_CANVAS_RATIO,
        canvas_strength,
        storm_cloth_rating_for,
    )

    no, source = canvas
    per = CLOTH_KN_PER_M2_NO2 * canvas_strength(no)
    if storm:
        return (
            f" Canvas No. {no} ({source}); rated for the wind it is cut for (package 45): "
            f"{storm_cloth_rating_for(1.0):.2f} kN/m2, the model's force on a jib-headed sail "
            f"at {STORM_CANVAS_APPARENT_KN:.0f} knots apparent over a strain of "
            f"{STORM_CANVAS_RATIO}, where the cloth's own rating of {per:.3f} kN/m2 "
            "({canvas_strength:.2f} of No. 2 by Luce App. E) blew it out at sixty."
        ).replace("{canvas_strength:.2f}", f"{canvas_strength(no):.2f}")
    return (
        f" Canvas No. {no} ({source}); cloth {per:.3f} kN/m2, {canvas_strength(no):.2f} of "
        "No. 2 by Luce App. E."
    )


RHO_AIR = 1.225
KNOT = 0.514444


def ft(x: float) -> float:
    """Feet to metres, one decimal."""
    return round(x * FT, 1)


# Package 32e: the horse a boom's sheet travels on, written on every gaff sail's boom.
HORSE_NOTE = (
    "is the horse across the stern for the sheet to travel on (Steel 1794 vol. I, p. 167, "
    "HORSE: 'a thick iron rod, fastened at the ends to the inside of the stern of vessels "
    "that carry a fore and aft mainsail, for the main sheet to travel on'), half the beam "
    "(judgement: the inside breadth of the stern); the sheet's geometry reads it "
    "(evolutions/trim.py)."
)


def rope_kn(circ_in: float, parts: int = 1) -> float:
    """Working rating of a tarred hemp rope of this circumference, rove with this many parts."""
    return round(parts * ROPE_KN_PER_SQ_IN * circ_in * circ_in, 1)


class DesignLoad(float):
    """A spar rating still to be computed: carries the design wind until the rating pass.

    `design_kn` returns one of these from the sails the caller names; `Builder.rate_spars`
    then recomputes it from every sail the engine's own graph hangs on the spar (studding
    sails excepted) and replaces it with a plain float before the file is written.
    """

    wind_kn: float

    def __new__(cls, value: float, wind_kn: float):
        obj = super().__new__(cls, value)
        obj.wind_kn = wind_kn
        return obj

    def __reduce__(self):
        return (DesignLoad, (float(self), self.wind_kn))


def static_kn(sails: list[tuple[float, float, str]], wind_kn: float) -> float:
    """Static peak-coefficient force, kN, of (area_m2, centre_height_m, class) sails."""
    v10 = wind_kn * KNOT
    force = 0.0
    for area, height, cls in sails:
        v = v10 * (max(height, 1.0) / 10.0) ** 0.11  # the shear the engine uses (spec 7.1)
        force += 0.5 * RHO_AIR * v * v * area * PEAK_COEFF[cls]
    return force / 1000.0


def design_kn(sails: list[tuple[float, float, str]], wind_kn: float) -> DesignLoad:
    """Sustained load, kN, of these sails in this wind; finalised by the rating pass."""
    return DesignLoad(round(static_kn(sails, wind_kn) * SUSTAINED_FRACTION, 1), wind_kn)


# ---------------------------------------------------------------------------
# The ground tackle (package 34, spec M5 §18; decision 30): one rule for every ship
# ---------------------------------------------------------------------------

CWT_KG = 50.8023  # the hundredweight of 112 lb
# "The old rule for determining the weight of anchors for any vessel was as follows: For
# the bowers, two thirds the draught of water when loaded and the greatest breadth of beam,
# allowing one cwt. for each foot of the same. Or the simple rule of five cwt. for every
# hundred tons burden may be adopted" (Luce 1866, ch. XIV Ground Tackle, 'Rules for
# finding weight of anchors and kedges'). The tonnage rule is the one used, since it
# serves a cutter of 85 tons as it serves a frigate of 933 (the beam rule gives the
# frigate 48 cwt against the tonnage rule's 47, and would give the cutter 15 against 4);
# the beam rule is written as the check in the frigate's comment. Steel 1794's table of
# anchors by rate ('The most approved dimensions and weight of anchors', vol. I) is
# illegible in the OCR; the figure recalled for a 36-gun frigate's bowers (about 42 cwt)
# is UNVERIFIED and noted in docs/dev/TuningNotes.md.
BOWER_CWT_PER_100_TONS = 5.0
# The stream "about one fourth the weight of the bower" and a single kedge "one eighth"
# (Luce 1866, ch. XIV, the Book of Allowances of 1865 quoted, items 3 and 4).
STREAM_OF_BOWER = 0.25
KEDGE_OF_BOWER = 0.125
# "All cables ought to be one hundred and twenty fathoms in length" (Falconer 1780, CABLE),
# and "it is necessary to splice at least two cables together, in order to double the
# length when a ship is obliged to anchor in deep water" (the same); on the Channel service
# "three Cables on the best Bower, two on the small Bower" (Lever 1808, 'Anchors', p. 67).
# The best bower here has two spliced, the rest one each (judgement between the two).
CABLE_FATHOMS = 120.0
BEST_BOWER_CABLES = 2
# The cable's size: half an inch of circumference to every foot of the ship's beam, the
# rule of thumb (JUDGEMENT, UNVERIFIED: not found in the texts in hand; Steel's table
# 'The number of cables, and their sizes, allowed in the Navy, to ships of each rate',
# vol. I, is garbled in the OCR, and the 17 inches recalled for a 36-gun frigate's bower
# cable against this rule's 19 is noted in the tuning notes). The stream's cable two
# thirds of the bower's and the kedge's hawser half (judgement; Luce 1866 ch. XIV:
# "not counting stream-cables, the largest hawsers ... are eleven inches").
CABLE_IN_PER_FOOT_OF_BEAM = 0.5
STREAM_CABLE_OF_BOWER = 2.0 / 3.0
KEDGE_HAWSER_OF_BOWER = 0.5
# Two bowers and a sheet anchor, a stream and a kedge for a ship; a small vessel under
# two hundred tons two bowers and a kedge: "Two bower anchors, and in vessels of two
# hundred tons and upwards, a spare or waist anchor" (Lever 1808, 'Anchors', p. 67, the
# coasters), the stream with the spare (judgement).
SHEET_AND_STREAM_FROM_TONS = 200.0


def ground_tackle_for(b, burthen, beam_ft, draught_ft):
    """The anchors and cables of a ship by her size: the one rule for the four files."""
    bower_cwt = round(BOWER_CWT_PER_100_TONS * burthen / 100.0, 1)
    beam_rule_cwt = round(2.0 / 3.0 * draught_ft + beam_ft, 1)
    circ = round(CABLE_IN_PER_FOOT_OF_BEAM * beam_ft * 2.0) / 2.0  # to the half inch
    stream_circ = round(STREAM_CABLE_OF_BOWER * circ * 2.0) / 2.0
    kedge_circ = round(KEDGE_HAWSER_OF_BOWER * circ * 2.0) / 2.0
    kg = round(bower_cwt * CWT_KG, -1)
    anchors = [
        (
            "best_bower",
            "bower",
            "the best bower",
            kg,
            CABLE_FATHOMS * BEST_BOWER_CABLES,
            circ,
            rope_kn(circ),
            f"The bowers: {bower_cwt:g} cwt by the rule of five cwt to the hundred tons "
            f"({burthen:g} tons burthen; the beam rule, two thirds the draught and the beam in "
            f"cwt, gives {beam_rule_cwt:g}), Luce 1866 ch. XIV. The cable {circ:g} inches, "
            f"half an inch to the foot of beam (judgement, unverified), rated as every rope "
            f"by Luce ch. IV; two cables of 120 fathoms spliced on the best bower (Falconer "
            f"1780, CABLE; Lever 1808 p. 67).",
        ),
        ("small_bower", "bower", "the small bower", kg, CABLE_FATHOMS, circ, rope_kn(circ), None),
    ]
    if burthen >= SHEET_AND_STREAM_FROM_TONS:
        anchors.append(
            (
                "sheet",
                "sheet",
                "the sheet anchor",
                kg,
                CABLE_FATHOMS,
                circ,
                rope_kn(circ),
                "The sheet anchor, the bowers' size and cable (Lever 1808 p. 67).",
            )
        )
        anchors.append(
            (
                "stream",
                "stream",
                "the stream anchor",
                round(kg * STREAM_OF_BOWER, -1),
                CABLE_FATHOMS,
                stream_circ,
                rope_kn(stream_circ),
                "The stream anchor, a quarter of the bower (Luce 1866 ch. XIV, the Book of "
                "Allowances), its cable two thirds of the bower's (judgement).",
            )
        )
    anchors.append(
        (
            "kedge",
            "kedge",
            "the kedge",
            round(kg * KEDGE_OF_BOWER, -1),
            CABLE_FATHOMS,
            kedge_circ,
            rope_kn(kedge_circ),
            "The kedge, an eighth of the bower (Luce 1866 ch. XIV), on a hawser of half the "
            "cable's size (judgement).",
        )
    )
    b.ground_tackle(
        "The ground tackle (package 34, spec M5 §18): the anchors by the ship's size and the "
        "hemp cables by the fathom, every figure's rule in tools/gen_ships.py; chain cable "
        "is later than 1805 and the file says so.",
        anchors,
        chain=False,
    )


def quarter(x: float) -> float:
    """Round a rope size to the nearest quarter inch."""
    return round(x * 4.0) / 4.0


# ---------------------------------------------------------------------------
# The hull's profile (package 75; docs/design/Build-Ships.md §5.1, §5.3): the side, the decks
# and the ports in the fore-and-aft plane, x forward of midships and z above the file's
# waterline, in metres. A ship's function or module gives it as the last key of her hull dict,
# with a note for each line in her `hull_notes`, keyed "profile.<key>" (and
# "profile.<key>.<deck>" for one deck's line); `Builder.dump` writes each line on one line.
# ---------------------------------------------------------------------------


def hull_profile(rail, breadth, **parts):
    """The hull's `profile:` mapping from its lines: `rail`, [[x, z], ...] from the taffrail
    to the stem head, and `breadth`, [[x, hb_water, hb_rail], ...], with those of the other
    parts the sources give, named as the schema's keys without their `_m` (`keel`, `stem`,
    `stern`, `wales`, `section`; by deck word, `decks`, `ports` and `port_size`; and stage 0H's
    shape points, `head`, `breadth_line`, `sections`, `channel_wales`, `floor` and `rabbet`),
    each in its key's form. The keys in the schema's order (`schema.PROFILE_KEYS`), every figure
    in metres to the centimetre. The form and the marks are not parts: `hull_form` adds them.
    Whatever the load would refuse (Build-Ships.md §5.2) raises ValueError here with the
    schema's own sentence, its check (`schema._parse_profile`) run on the mapping as it will be
    written, so that a ship's module fails at generation and not at the load."""
    from freesail.ship.schema import PROFILE_KEYS, ShipFileError, _parse_profile

    given = {"rail_m": rail, "breadth_m": breadth}
    # every line of points in `_m`, the shape's six among them; `form` and `marks` are not
    others = [key for key in PROFILE_KEYS if key.endswith("_m") and key not in given]
    for word, line in parts.items():
        if f"{word}_m" not in others:
            words = ", ".join(key.removesuffix("_m") for key in others)
            later = (
                "; the form and the marks are hull_form's (Build-Ships.md §5.3)"
                if word in ("form", "marks")
                else ""
            )
            raise ValueError(
                f"hull_profile takes no part '{word}'; beside the rail and the breadth its parts "
                f"are {words}{later}."
            )
        if line is not None:
            given[f"{word}_m"] = line
    profile = {key: _centimetres(given[key]) for key in PROFILE_KEYS if key in given}
    try:
        _parse_profile(profile, "hull_profile")
    except ShipFileError as e:
        raise ValueError(str(e)) from e
    return profile


def _centimetres(v):
    """A profile's figures to the centimetre, its points as lists (yaml's safe dump writes no
    tuple); anything that is not a number is left for the schema to refuse in words."""
    if isinstance(v, dict):
        return {str(k): _centimetres(x) for k, x in v.items()}
    if isinstance(v, list | tuple):
        return [_centimetres(x) for x in v]
    if isinstance(v, int | float) and not isinstance(v, bool):
        return round(float(v), 2) + 0.0  # + 0.0: never a "-0.0" in a file
    return v


def _flow_profile(block):
    """The hull's `  profile:` block as yaml writes it, with each list in it on one flow line,
    as `Builder.dump` sets a sail's corners: a line of points `rail_m: [[x, z], ...]`, a
    deck's under its word, and a port's size `[width, depth]`; and from stage 0H, `sections_m`
    one station to a line, each under the first, and in the form's blocks its lists the same
    (`fullness`, `transom_hb_m`, a tier of galleries, a band of lights)."""

    def points(mo):
        indent, key, body = mo.groups()
        pts = re.findall(rf"^{indent}- - (\S+)\n((?:{indent}  - \S+\n)+)", body, flags=re.M)
        each = [
            "[" + ", ".join([first, *re.findall(r"- (\S+)\n", rest)]) + "]" for first, rest in pts
        ]
        if key != "sections_m":
            return f"{indent}{key}: [{', '.join(each)}]\n"
        stations = []  # the points of each x in turn, as written
        for (first, _rest), point in zip(pts, each, strict=True):
            if stations and stations[-1][0] == first:
                stations[-1][1].append(point)
            else:
                stations.append((first, [point]))
        under = ",\n" + " " * len(f"{indent}{key}: [")
        return f"{indent}{key}: [" + under.join(", ".join(s) for _x, s in stations) + "]\n"

    def numbers(mo):
        indent, key, body = mo.groups()
        return f"{indent}{key}: [" + ", ".join(re.findall(r"- (\S+)\n", body)) + "]\n"

    block = re.sub(r"^( +)(\w+):\n((?:\1- - \S+\n(?:\1  - \S+\n)+)+)", points, block, flags=re.M)
    return re.sub(r"^( +)(\w+):\n((?:\1- \S+\n)+)", numbers, block, flags=re.M)


# ---------------------------------------------------------------------------
# The hull's shape (package 75, SW-2b.1; docs/design/Build-Ships.md §5.0, §5.1, §5.3): the
# helpers through which every ship's builder writes stage 0H's shape keys. `hull_profile` takes
# their six lines of points as parts; `hull_form` adds the form and the marks, and checks the
# hull as `freesail/ship/form.py` draws it against the file; `midship_section` makes a section
# by Steel's sweeps for a hull with no measured one; `from_steel_table` makes a stand-in's main
# breadth and section points from one of Steel's bodies tables. The shape is drawn only: nothing
# the physics, the guns or the lee ports read is taken from it, and no port triple is ever
# written from the drawing (§5.0 principle 8).
# ---------------------------------------------------------------------------

# The keel's half-siding where a made section is given none: the main keel's siding at midships
# as a share of the moulded breadth, Steel 1805 Folio I, rows K and S (read:
# ships-design/pages-steel-1805-bodies.md §4): 1 ft 4 in of 37 ft 6 in in the frigate of 36,
# 1 ft 1 in of 29 ft 3 in in the cutter, 0.036 and 0.037; the coasting sloop's 10 in of 16 ft
# 4 in, 0.051, is a merchant's keel (judgement: the ships of war's share).
KEEL_SIDING_OF_BREADTH = 0.036
# A made section's arcs are set down in steps of no more than this (judgement: a section in a
# file is a few points to the centimetre, as a draught's are read off it).
SWEEP_STEP_DEG = 15.0


def hull_form(hull, *, form, marks, measured=(), report=None):
    """The hull's form and its marks added to its profile (Build-Ships.md §5.1, §5.3: stage
    0H's `form` and `marks`), and the hull as drawn checked against the file. `hull` is the
    ship's hull mapping, her profile in it from `hull_profile` and her displacement and draught
    beside it. `form` is {fullness, stern, head} in §5.1's form and `marks` each line's one word,
    {line: word} (§5.0 principle 4); either None or empty gives none. The form is written in the
    schema's order, its metres to the centimetre and its fullness to two places, a band's count
    of lights whole and its words as given (not through `_centimetres`, which would make a count
    a float); the marks in the profile's order.

    Whatever the load would refuse raises ValueError with the schema's own sentence, and then
    `freesail.ship.form.check` draws the hull, raising where the drawing fails. `measured` names
    the triples the ship's sources measured, each a deck word (all its ports) or (deck word, x):
    a gap over `form.PORT_GAP_M` raises for one of them and is reported for every other. No
    triple is ever written from the drawing (§5.0 principles 7 and 8).

    Nothing it computes goes into a note: a ship's notes carry sources, departures and
    judgements, and a figure a rule computes from the file's own keys belongs in the generator's
    report and the tests, where it cannot go stale (the lead's notes of 2026-10-29, item 2).
    `report`, a list if given, gets those as sentences for the generator to print: the drawn
    displacement beside the filed one, the drawn depth beside the draught, and each port triple's
    gap to the drawn side at its sill, deck by deck.

    Returns each triple's gap in metres, the drawn side less the triple's half-breadth, keyed
    (deck word, x)."""
    from freesail.ship import form as drawn
    from freesail.ship.schema import ShipFileError, _parse_hull

    profile = hull.get("profile") if isinstance(hull, dict) else None
    if not isinstance(profile, dict):
        raise ValueError("hull_form: the hull has no profile; hull_profile makes it first.")
    if "form" in profile or "marks" in profile:
        raise ValueError(
            "hull_form: the profile has its form or its marks already; hull_form adds them once."
        )
    shaped = dict(profile)
    if form:
        shaped["form"] = _form_figures(form)
    if marks:
        shaped["marks"] = _marks_in_order(marks)
    try:
        spec = _parse_hull({**hull, "profile": shaped}, "hull_form")
    except ShipFileError as e:
        raise ValueError(str(e)) from e
    try:
        lines = drawn.check(spec)
    except ValueError as e:
        raise ValueError(f"hull_form: {e}") from e

    ports = dict(spec.profile.ports_m)
    named = set()
    for entry in measured:
        if isinstance(entry, str):
            if entry not in ports:
                raise ValueError(
                    f"hull_form: measured names the {entry} deck's ports, and the profile gives "
                    f"that deck none; its port decks are {', '.join(ports) or 'none'}."
                )
            named |= {(entry, x) for x, _sill, _hb in ports[entry]}
            continue
        word, x = entry
        at = [t[0] for t in ports.get(word, ()) if abs(t[0] - x) < 0.005]
        if not at:
            raise ValueError(
                f"hull_form: measured names the {word} port at x {x:g}, and the profile gives "
                "no port there; name a triple by its deck and its x to the centimetre."
            )
        named.add((word, at[0]))
    gaps = {}
    for word, triples in spec.profile.ports_m:
        for x, sill, hb in triples:
            gaps[(word, x)] = drawn.half_breadth_at(spec, x, sill) - hb
    wrong = [(k, g) for k, g in gaps.items() if k in named and abs(g) > drawn.PORT_GAP_M]
    if wrong:
        each = "; ".join(f"the {w} port at x {x:g}, {g:+.2f} m" for (w, x), g in wrong)
        raise ValueError(
            f"hull_form: the drawn side misses a measured port triple by more than "
            f"{drawn.PORT_GAP_M:g} m at its sill: {each}. A port is never moved to the drawing "
            "(Build-Ships.md §5.0 principle 8): mend the shape's lines, or measure the port again."
        )

    hull["profile"] = shaped
    if report is None:
        return gaps
    said = "the hull as drawn (freesail/ship/form.py):"
    report.append(f"{said} {_line_of(lines, 'drawn displacement ')}.")
    report.append(f"{said} {_line_of(lines, ' deep at the greatest section')}.")
    for word, triples in spec.profile.ports_m:
        off = [x for x, _sill, _hb in triples if abs(gaps[(word, x)]) > drawn.PORT_GAP_M]
        figures = ", ".join(f"{round(gaps[(word, x)], 2) + 0.0:+.2f}" for x, _s, _h in triples)
        text = (
            f"{said} the {word} deck's ports: the side at each sill, aft to forward, off the "
            f"half-breadth by {figures} m"
        )
        if off:
            text += (
                f"; more than {drawn.PORT_GAP_M:g} m at x {', '.join(f'{x:g}' for x in off)}, "
                "reported and never moved to the drawing"
            )
        mine = sum(1 for x, _s, _h in triples if (word, x) in named)
        if mine:
            text += f"; the {mine} measured each within {drawn.PORT_GAP_M:g} m"
        report.append(text + ".")
    return gaps


def _form_figures(form):
    """The profile's `form` as `hull_form` writes it: its keys in the schema's order and the
    stern's likewise (any other after them, for the schema to refuse in words); a key given
    None left out; its metres to the centimetre, the fullness to two places, a band's count of
    lights whole, its words as given."""
    from freesail.ship.schema import FORM_KEYS, STERN_KEYS

    if not isinstance(form, dict):
        return form
    out = {}
    for key in _schema_order(form, FORM_KEYS):
        v = form[key]
        if v is None:
            continue
        if key == "stern" and isinstance(v, dict):
            kept = [k for k in _schema_order(v, STERN_KEYS) if v[k] is not None]
            v = {k: _stern_figure(k, v[k]) for k in kept}
        elif key == "fullness":
            v = _centimetres(v)
        out[key] = v
    return out


def _stern_figure(key, v):
    """One of the stern's keys as written: its type a word, a band of lights [z_low, z_high,
    n, hb] with its count whole, every other figure metres to the centimetre."""
    if key == "type":
        return v
    if key == "lights_m" and isinstance(v, list | tuple):
        return [
            [*_centimetres(band[:2]), _whole(band[2]), _centimetres(band[3])]
            if isinstance(band, list | tuple) and len(band) == 4
            else _centimetres(band)
            for band in v
        ]
    return _centimetres(v)


def _whole(n):
    """A count as a whole number where it is one (a float of a whole number to an int);
    anything else left for the schema to refuse in words."""
    if isinstance(n, float) and n.is_integer():
        return int(n)
    return n


def _schema_order(given, keys):
    """A mapping's keys in the schema's order, and any the schema does not know after them."""
    return [k for k in keys if k in given] + [k for k in given if k not in keys]


def _marks_in_order(marks):
    """Each line's word in the profile's order: its lines, then the form's groups, each group's
    stern keys after it; any other after them, for the schema to refuse in words."""
    from freesail.ship.schema import FORM_KEYS, PROFILE_KEYS, STERN_KEYS

    order = [k for k in PROFILE_KEYS if k not in ("form", "marks")]
    for group in FORM_KEYS:
        order.append(f"form.{group}")
        if group == "stern":
            order += [f"form.stern.{k}" for k in STERN_KEYS]
    if not isinstance(marks, dict):
        return marks
    named = {str(k): w for k, w in marks.items()}
    return {k: named[k] for k in _schema_order(named, order)}


def _line_of(lines, words):
    """The one of `form.check`'s lines that says `words`."""
    return next(line for line in lines if words in line)


def midship_section(
    *,
    half_breadth,
    breadth_z,
    depth,
    deadrise_deg,
    bilge_m,
    tumblehome_m,
    rail_z,
    half_siding=None,
):
    """A midship section, [[z, half_breadth], ...] low to high, metres to the centimetre, z above
    the water, by Steel's sweeps simplified (Steel 1805, OCR l. 2862-2883, "FRAMES", and
    11753-11785, "SWEEPS"), for a hull with no measured one (Build-Ships.md §5.1, §5.3; its line
    is marked `judged`):
    - the floor, straight from the keel's edge, `half_siding` out and `depth` below the water,
      rising at `deadrise_deg` (Steel: "a straight line ... drawn from the upper edge of the keel
      to touch the back of the floor sweep");
    - the bilge, one arc of radius `bilge_m` tangent to the floor and to the side (Steel's
      floor sweep, reconciling sweep and lower breadth sweep taken as one);
    - the side, upright to the main breadth, `half_breadth` at `breadth_z` (Steel's lower and
      upper heights of breadth taken as one);
    - the topside, Steel's upper breadth sweep and top-timber hollow taken as two equal arcs,
      the one turned against the other, from the breadth to the rail, `tumblehome_m` inside it (less
      than nothing, a flare) at `rail_z`, upright at both.
    `half_siding`, the keel's, is by default Steel's share of the breadth
    (`KEEL_SIDING_OF_BREADTH`). Figures that make no section raise ValueError in words: a bilge
    too great for the floor and the side to hold, a floor reaching the side above the breadth, a
    rail at or below it, a topside leaning in or out as far as it rises."""
    figures = {
        "half_breadth": half_breadth,
        "breadth_z": breadth_z,
        "depth": depth,
        "deadrise_deg": deadrise_deg,
        "bilge_m": bilge_m,
        "tumblehome_m": tumblehome_m,
        "rail_z": rail_z,
    }
    if half_siding is not None:
        figures["half_siding"] = half_siding
    for name, v in figures.items():
        if isinstance(v, bool) or not isinstance(v, int | float) or not math.isfinite(v):
            raise ValueError(f"midship_section: {name} is {v!r}, which is not a number.")
    big_y, z_b, z_r, r, t = half_breadth, breadth_z, rail_z, bilge_m, tumblehome_m
    z_k = -depth
    y_k = KEEL_SIDING_OF_BREADTH * big_y if half_siding is None else half_siding
    if not depth > 0.0:
        raise ValueError(
            f"midship_section: the keel's edge is {depth:g} m down; the depth below the water is "
            "more than nothing."
        )
    if not 0.0 < y_k < big_y:
        raise ValueError(
            f"midship_section: the keel's half-siding is {y_k:g} m against a main half-breadth of "
            f"{big_y:g} m; it is more than nothing and less than the half-breadth."
        )
    if not z_k < z_b < z_r:
        raise ValueError(
            f"midship_section: the keel's edge at z {z_k:g}, the main breadth at {z_b:g} and the "
            f"rail at {z_r:g} m; each stands above the last."
        )
    if not 0.0 <= deadrise_deg < 90.0:
        raise ValueError(
            f"midship_section: a deadrise of {deadrise_deg:g} degrees; the floor rises from the "
            "keel at nothing or more, and less than upright."
        )
    if not r >= 0.0:
        raise ValueError(
            f"midship_section: a bilge of radius {r:g} m; a radius is not less than nothing."
        )
    if not t < big_y:
        raise ValueError(
            f"midship_section: a tumblehome of {t:g} m leaves the rail no half-breadth inside the "
            f"main half-breadth of {big_y:g} m."
        )
    if not abs(t) < z_r - z_b:
        raise ValueError(
            f"midship_section: a tumblehome of {t:g} m on a topside {z_r - z_b:.2f} m high; the "
            "side leans in or out less than it rises."
        )
    a = math.radians(deadrise_deg)
    sa, ca = math.sin(a), math.cos(a)
    corner = z_k + (big_y - y_k) * sa / ca  # where the floor alone meets the side
    if corner > z_b:
        raise ValueError(
            f"midship_section: the floor, rising at {deadrise_deg:g} degrees from the keel's edge, "
            f"meets the side at z {corner:.2f}, above the main breadth at {z_b:g} m; a smaller "
            "deadrise or a higher breadth is wanted."
        )
    # the bilge's centre stands no higher than the breadth, and its foot on the floor no nearer
    # the middle line than the keel's edge
    fits = min(((z_b - z_k) * ca - (big_y - y_k) * sa), big_y - y_k) / (1.0 - sa)
    if r > fits + 1e-9:
        raise ValueError(
            f"midship_section: a bilge of radius {r:g} m does not fit between the floor and the "
            f"side below the main breadth; with these figures it is at most {fits:.2f} m."
        )
    z_c = z_k + (r + (big_y - r - y_k) * sa) / ca
    pts = [(z_k, y_k)]
    turn = a - 0.5 * math.pi  # the floor's tangent point, seen from the bilge's centre
    steps = max(1, math.ceil((90.0 - deadrise_deg) / SWEEP_STEP_DEG))
    for i in range(steps + 1):
        th = turn * (1.0 - i / steps)
        pts.append((z_c + r * math.sin(th), big_y - r + r * math.cos(th)))
    if z_b > z_c:
        pts.append((z_b, big_y))
    h = z_r - z_b
    if t == 0.0:
        pts.append((z_r, big_y))
    else:
        s = 1.0 if t > 0.0 else -1.0
        sweep = (t * t + h * h) / (4.0 * abs(t))  # each arc's radius, the two meeting halfway
        phi = math.asin(min(1.0, 0.5 * h / sweep))
        n = max(1, math.ceil(math.degrees(phi) / SWEEP_STEP_DEG))
        for i in range(1, n + 1):  # the upper breadth sweep, from the breadth to halfway
            p = phi * i / n
            pts.append((z_b + sweep * math.sin(p), big_y - s * sweep * (1.0 - math.cos(p))))
        for i in range(n - 1, -1, -1):  # the hollow, from halfway to the rail
            p = phi * i / n
            pts.append((z_r - sweep * math.sin(p), big_y - t + s * sweep * (1.0 - math.cos(p))))
    out = []
    for z, hb in pts:
        point = [round(z, 2) + 0.0, round(hb, 2) + 0.0]
        if out and point[0] <= out[-1][0]:
            if len(out) == 1 and point[0] == out[0][0] and point[1] > out[0][1]:
                out.append(point)  # a flat floor: the keel's edge, then the bilge's foot
            elif point[0] == out[-1][0]:
                out[-1] = point  # a centimetre apart: the later stands, the rail last of all
            continue
        out.append(point)
    return out


def feet_and_inches(v):
    """Feet and inches as Steel's tables print them ('18 10', '17 4¼', '0 8'), or a number of
    feet as it is, in feet."""
    if isinstance(v, int | float) and not isinstance(v, bool):
        return float(v)
    try:
        feet, inches = str(v).replace("¼", ".25").replace("½", ".5").replace("¾", ".75").split()
        return float(feet) + float(inches) / 12.0
    except ValueError:
        raise ValueError(f"'{v}' is not feet and inches as Steel prints them ('18 10½').") from None


def from_steel_table(rows, *, length_ratio, beam_ratio):
    """One of Steel's bodies tables (1805; ships-design/pages-steel-1805-bodies.md §3: the
    frigate of 36 guns, the cutter of 273 tons, the coasting sloop of 60 tons) as a stand-in's
    main breadth and section points (Build-Ships.md §5.0 principles 5 and 7, §5.3). Returns the
    parts for `hull_profile`, {`breadth_line`, `sections`}, and their marks for `hull_form`,
    each `stand-in` (S†).

    `rows` is the table as read, every height above Steel's base (the rabbet) and every breadth
    in Steel's feet and inches ('18 10½') or in feet:
    - `water`: the load line above the base, [[x, height], ...] aft to forward (§5.1), straight
      between its points and held beyond them;
    - `diagonals`: each [its height up the middle line, [its end's half-breadth, its end's
      height]], the 1st first (§3, "the diagonals");
    - `timbers`: aft to forward, each [its name, x, the lower height of breadth (None where the
      table prints one height), the upper, the main half-breadth, [its length down each
      diagonal, None where Steel leaves it blank]], x forward of the table's mid-perpendiculars
      in metres (§5.2).

    At each timber the main breadth is the upper height of breadth at the main half-breadth;
    the section's points are each diagonal's and the lower height of breadth's, moulded as
    Steel's are. The top-timber line is the file's rail, from her own source, not the
    stand-in's (§5.0 principle 7). Scaled by principle 7: x by `length_ratio`, the waterlines'
    lengths hers over the table's; the heights above the water and the half-breadths by
    `beam_ratio`, the beams', so that the stand-in's floor, tumblehome and flare keep their
    angles. Every figure to the centimetre; a point of a timber within a centimetre of the one
    below it, so rounded, is left out."""
    from freesail.ship.profile import interp

    for name, ratio in (("length_ratio", length_ratio), ("beam_ratio", beam_ratio)):
        if isinstance(ratio, bool) or not isinstance(ratio, int | float) or not ratio > 0.0:
            raise ValueError(
                f"from_steel_table: {name} is {ratio!r}; a ratio is more than nothing."
            )

    def feet(v, where):
        """A figure of the table in feet, refused with its place in the table named."""
        try:
            return feet_and_inches(v)
        except ValueError as e:
            raise ValueError(f"from_steel_table: {where}, {e}") from None

    water = sorted((float(x), feet(h, "the load line")) for x, h in rows["water"])
    diagonals = []
    for i, (height, (out, up)) in enumerate(rows["diagonals"], start=1):
        h = feet(height, f"diagonal {i}")
        vy, vz = feet(out, f"diagonal {i}"), feet(up, f"diagonal {i}") - h
        n = math.hypot(vy, vz)
        diagonals.append((h, vy / n, vz / n))
    breadth_line, sections = [], []
    last = None
    for name, x, lower, upper, main, reaches in rows["timbers"]:
        where = f"timber {name}"
        if last is not None and not x > last[1]:
            raise ValueError(
                f"from_steel_table: timber {name} at x {x:g} is not forward of timber {last[0]} "
                f"(x {last[1]:g}); the timbers run aft to forward."
            )
        if len(reaches) != len(diagonals):
            raise ValueError(
                f"from_steel_table: timber {name} gives {len(reaches)} diagonals and the table "
                f"{len(diagonals)}; give None where Steel leaves one blank."
            )
        last = (name, x)
        load = interp(water, x)
        main_ft = feet(main, where)

        def at(z_ft, hb_ft, x=x, load=load):
            """A point of this timber above Steel's base, as the file's [x, z, hb], scaled."""
            return [
                _centimetres(x * length_ratio),
                _centimetres((z_ft - load) * FT * beam_ratio),
                _centimetres(hb_ft * FT * beam_ratio),
            ]

        breadth_line.append(at(feet(upper, where), main_ft))
        points = [
            at(h + feet(d, where) * uz, feet(d, where) * uy)
            for (h, uy, uz), d in zip(diagonals, reaches, strict=True)
            if d is not None
        ]
        if lower is not None:
            points.append(at(feet(lower, where), main_ft))
        for point in sorted(points, key=lambda p: p[1]):
            if sections and sections[-1][0] == point[0] and point[1] <= sections[-1][1]:
                continue
            sections.append(point)
    parts = {"breadth_line": breadth_line, "sections": sections}
    return parts, {"breadth_line_m": "stand-in", "sections_m": "stand-in"}


class Builder:
    def __init__(self, name, rig, era_notes, hull, hull_notes=None):
        self.doc = {
            "ship": {"name": name, "rig": rig, "era_notes": era_notes},
            "hull": hull,
            "spars": [],
            "sails": [],
            "lines": [],
            "groups": {},
            "aliases": {},
        }
        self.notes: dict[str, str] = {}
        self.hull_notes: dict[str, str] = dict(hull_notes or {})
        self.crew_notes: dict[tuple[str, ...], str] = {}
        self.tackle_notes: dict[tuple[str, ...], str] = {}
        self.hold_note: str = ""
        self.boat_notes: dict[tuple[str, ...], str] = {}
        self.oars_note: str = ""

    def spar(self, id, cls, note=None, **kw):
        d = {"id": id, "class": cls}
        d.update({k: v for k, v in kw.items() if v is not None})
        if cls == "studdingsail_boom":
            # Milestone 3b (spec 3b §7): every studding sail boom, the ringtail's among them,
            # starts the voyage rigged in, as at sea; it is rigged out to set its sail (Luce
            # 1884 ch. XXIII, 'The Topmast Studding-sail': "Set taut! Rig out! Hoist away!";
            # RigGeometryNotes §5). A gaff sail's boom is not rigged in and carries no state.
            d["rigged_out"] = False
        self.doc["spars"].append(d)
        if note:
            self.notes[id] = note
        return id

    def sail(self, id, cls, note=None, **kw):
        d = {"id": id, "class": cls}
        d.update({k: v for k, v in kw.items() if v is not None})
        self.doc["sails"].append(d)
        if note:
            self.notes[id] = note
        return id

    def line(self, id, cls, of, side=None, rating=None, note=None, parts=None):
        d = {"id": id, "class": cls, "of": of}
        if side:
            d["side"] = side
        if rating:
            d["rating_kn"] = rating
        if parts is not None and parts > 1:
            # a sheet's purchase (package 32e): its fall's scope in fathoms reads it
            d["parts"] = int(parts)
        self.doc["lines"].append(d)
        if note:
            self.notes[id] = note
        return id

    def sided(self, base, cls, of, rating=None, note=None):
        for s in SIDES:
            self.line(
                f"{base}.{s}", cls, of, side=s, rating=rating, note=note if s == SIDES[0] else None
            )

    def group(self, name, members):
        self.doc["groups"][name] = members

    def alias(self, name, target):
        self.doc["aliases"][name] = target

    def crew(self, entries):
        """The `crew:` section (spec M3 §2.3) from (path, value, note) entries.

        A path is ("complement",), ("stations", "forecastle"), ("posts", "captain") and so
        on; the note is written above the value's line in the file, like the hull's.
        """
        crew: dict = {}
        for path, value, note in entries:
            if path[0] == "posts":
                crew.setdefault("posts", []).append({"post": path[1]})
            elif len(path) == 1:
                crew[path[0]] = value
            else:
                crew.setdefault(path[0], {})[path[1]] = value
            if note:
                self.crew_notes[tuple(path)] = note
        self.doc["crew"] = crew

    def sail_room(self, note, entries):
        """The stores' `sails:` list (spec 3b §6.3) from (kind, canvas_no, note) entries: each
        a sail in the sail room at condition 100, the note written above its line."""
        stores = self.doc["crew"].setdefault("stores", {})
        stores["sails"] = [{"kind": k, "canvas_no": no, "condition": 100} for k, no, _ in entries]
        self.crew_notes[("stores", "sails")] = note
        for kind, _, text in entries:
            self.crew_notes[("sails", kind)] = text

    def spare_spars(self, note, entries):
        """The stores' `spare_spars` by class (package 30b) from (class, count, note) entries:
        the booms, each class's note written above its line and `note` above the store's."""
        stores = self.doc["crew"].setdefault("stores", {})
        stores["spare_spars"] = {cls: n for cls, n, _ in entries}
        self.crew_notes[("stores", "spare_spars")] = note
        for cls, _, text in entries:
            if text:
                self.crew_notes[("spare_spars", cls)] = text

    def ground_tackle(self, note, anchors, chain=False):
        """The `ground_tackle:` section (package 34, spec M5 §18) from (id, kind, name,
        weight_kg, cable_fathoms, cable_in, cable_kn, note) entries, the note above each
        anchor's line and `note` above the section."""
        self.doc["ground_tackle"] = {
            "chain": chain,
            "anchors": [
                {
                    "id": aid,
                    "kind": kind,
                    "name": name,
                    "weight_kg": weight,
                    "cable_fathoms": fathoms,
                    "cable_in": circ,
                    "cable_kn": kn,
                }
                for aid, kind, name, weight, fathoms, circ, kn, _ in anchors
            ],
        }
        self.tackle_notes = {("section",): note}
        for aid, _, _, _, _, _, _, text in anchors:
            if text:
                self.tackle_notes[("anchors", aid)] = text

    def hold(self, capacity_tons, note):
        """The `hold:` section (package 35, spec M5 §23): the room for a cargo in tons,
        the note above the section."""
        self.doc["hold"] = {"capacity_tons": capacity_tons}
        self.hold_note = note

    def boats(self, note, entries):
        """The `boats:` list (package 35, spec M5 §23) from (id, kind, name, length_ft,
        oars, crew, tons, note[, file]) entries, the note above each boat's line and `note`
        above the section; `file` (package 82, item 4), the boat's own ship file by which
        she is manned as a hull, written as the last key of her mapping where an entry
        gives one."""
        self.doc["boats"] = []
        self.boat_notes = {("section",): note}
        for entry in entries:
            bid, kind, name, length, oars, crew, tons, text = entry[:8]
            boat = {
                "id": bid,
                "kind": kind,
                "name": name,
                "length_ft": length,
                "oars": oars,
                "crew": crew,
                "tons": tons,
            }
            if len(entry) > 8 and entry[8]:
                boat["file"] = entry[8]
            self.doc["boats"].append(boat)
            if text:
                self.boat_notes[("boats", bid)] = text

    def oars(self, note, number, thrust_n, power_w, tiring_h):
        """The `oars:` section (package 82, item 4; the design's §5.2): a boat's oars and
        the three figures of the oar force, `note` above the section."""
        self.doc["oars"] = {
            "number": number,
            "thrust_n": thrust_n,
            "power_w": power_w,
            "tiring_h": tiring_h,
        }
        self.oars_note = note

    def pumps(self, note, entries):
        """The `pumps:` list (package 73, spec M7 §13) from (id, kind, name, tons_per_hour,
        hands, note) entries, the note above each pump's line and `note` above the section."""
        self.doc["pumps"] = [
            {"id": pid, "kind": kind, "name": name, "tons_per_hour": tph, "hands": hands}
            for pid, kind, name, tph, hands, _ in entries
        ]
        self.pump_notes = {("section",): note}
        for pid, _, _, _, _, text in entries:
            if text:
                self.pump_notes[("pumps", pid)] = text

    def gear(self, note, entries):
        """The `gear:` list (package 56, spec M7b §21a) from (id, kind, name, sizes, note)
        entries, `sizes` a mapping of the period's figures (beam_ft, length_fathoms, nets,
        hooks); the note above each piece's line and `note` above the section."""
        self.doc["gear"] = [
            {"id": gid, "kind": kind, "name": name, **sizes}
            for gid, kind, name, sizes, _ in entries
        ]
        self.gear_notes = {("section",): note}
        for gid, _, _, _, text in entries:
            if text:
                self.gear_notes[("gear", gid)] = text

    def people(self, note, entries):
        """The crew's `people:` list (package 35, spec M5 §22) from (role, station,
        rating, messenger, note) entries: the named roles beyond the posts, each drawn
        from its station at muster; the note above each role's line and `note` above the
        list."""
        crew = self.doc["crew"]
        crew["people"] = [
            {
                "role": role,
                "station": station,
                **({"rating": rating} if rating else {}),
                **({"messenger": True} if messenger else {}),
            }
            for role, station, rating, messenger, _ in entries
        ]
        self.crew_notes[("people",)] = note
        for role, _, _, _, text in entries:
            if text:
                self.crew_notes[("people", role)] = text

    def armament(self, note, default, fits):
        """The `armament:` section (spec M7 §7; package 70) from fits, each
        (name, source, guns, magazine, note): `guns` a list of (mapping, note) in the
        file's order, `magazine` the fit's magazine in the file's order (`fit_magazine`:
        the filled cartridges and their charges by kind and calibre, the powder barrels,
        a King's fit's charges for exercise, the shot by calibre and kind; practice and
        resupply, between packages 72 and 73); the note above the section, each fit's
        above its name, a gun's above its line, `MAGAZINE_NOTES` above the magazine's
        keys."""
        self.doc["armament"] = {
            "default": default,
            "fits": {
                name: {"source": source, "guns": [g for g, _ in guns], **magazine}
                for name, source, guns, magazine, _ in fits
            },
        }
        self.armament_notes = {("section",): note}
        for name, _, guns, magazine, text in fits:
            if text:
                self.armament_notes[("fit", name)] = text
            for g, gnote in guns:
                if gnote:
                    self.armament_notes[("gun", name, g["id"])] = gnote
            for key in magazine:
                if key in MAGAZINE_NOTES:
                    self.armament_notes[("magazine", name, key)] = MAGAZINE_NOTES[key]

    def quarter_bill(
        self,
        note,
        trimmers,
        helm,
        powder,
        priority,
        notes,
        small_arms=0,
        boarders=0,
        small_arms_note="",
        boarders_note="",
        filling=None,
    ):
        """The crew's `quarter_bill:` block (spec M7 §8a; package 70): the trimmers by
        station as (station, n, note) entries, the hands at the helm, the powder beyond the
        idlers, the men who fill cartridges when given (`filling_party`; the owner's practice
        and resupply, folded in by package 86, after the powder with `FILLING_NOTE`), and the
        fighting book's priority; `notes` the words above helm, powder and priority. Package
        73 (spec M7 §11): the small-arms men and the boarders told off from the guns' crews,
        each with its note."""
        crew = self.doc["crew"]
        crew["quarter_bill"] = {
            "trimmers": {st: n for st, n, _ in trimmers},
            "helm": helm,
            "powder": powder,
            **({"filling": filling} if filling is not None else {}),
            "priority": priority,
            "small_arms": small_arms,
            "boarders": boarders,
        }
        self.crew_notes[("quarter_bill",)] = note
        for st, _, text in trimmers:
            if text:
                self.crew_notes[("trimmers", st)] = text
        if filling is not None:
            self.crew_notes[("quarter_bill", "filling")] = FILLING_NOTE
        for key, text in notes.items():
            self.crew_notes[("quarter_bill", key)] = text
        self.crew_notes[("quarter_bill", "small_arms")] = small_arms_note or SMALL_ARMS_NOTE
        self.crew_notes[("quarter_bill", "boarders")] = boarders_note or BOARDERS_NOTE

    def rate_spars(self):
        """Second pass: rate every spar from what the engine's graph hangs on it.

        The doc is loaded through the real loader; each spar with a DesignLoad rating is
        then rated for every sail whose spar chain passes through it (studding sails
        excepted: they are fair-weather sails, and their booms carry them alone) at its
        design wind, and its comment gains the list.
        """
        from freesail.ship.loader import ship_from_dict

        probe = copy.deepcopy(self.doc)
        for spar in probe["spars"]:
            if isinstance(spar.get("rating_kn"), DesignLoad):
                spar["rating_kn"] = float(spar["rating_kn"])
        from freesail.ship.parts import SailState

        ship = ship_from_dict(probe, "rating pass")
        carried: dict[str, list[tuple[str, float, float, str]]] = {s: [] for s in ship.spars}
        # Milestone 3b: a sail that starts in the sail room (storm canvas, the occasional
        # sails) is set in place of or beyond the working canvas the spars are rated for, and
        # loads nothing here, except the boom made for it alone (a ringtail boom), which is
        # rated for its sail as a studding sail boom is.
        booms_in_use = {
            b.id
            for s in ship.sails.values()
            if s.state is not SailState.UNBENT and (b := ship.spar_of_role(s, "boom")) is not None
        }
        for sail in ship.sails.values():
            # rated at the peak of its `curve_class`'s curve (package 75: the gaff's for a
            # lateen cut at the mast, as the physics will take it from the engine's lateen step;
            # else its own class)
            entry = (sail.id, sail.area_m2, sail.centre_height_m, sail.curve_class)
            boom = ship.spar_of_role(sail, "boom") if sail.cls == "studding" else None
            if sail.state is SailState.UNBENT:
                own = boom is not None and boom.cls == "studdingsail_boom"
                if own and boom.id not in booms_in_use:
                    carried[boom.id].append(entry)
                continue
            chain = ship.spar_chain(sail)
            for spar in chain:
                carried[spar.id].append(entry)
            if boom is not None and boom not in chain:
                carried[boom.id].append(entry)
        for spar in self.doc["spars"]:
            rating = spar.get("rating_kn")
            if not isinstance(rating, DesignLoad):
                continue
            sails = carried[spar["id"]]
            cls = ship.spars[spar["id"]].cls
            if cls != "studdingsail_boom":
                sails = [s for s in sails if s[3] != "studding"]
            if sails:
                loads = [(a, h, c) for _, a, h, c in sails]
                value = round(static_kn(loads, rating.wind_kn) * SUSTAINED_FRACTION, 1)
                spar["rating_kn"] = max(value, 1.0)
                names = ", ".join(s[0] for s in sails)
                how = f"Rating: {names} in {rating.wind_kn:.0f} kn -> {spar['rating_kn']:g} kN."
                # a spar's rating by the sails whose chains pass through it is a proxy for its
                # scantlings, and the proxy may not shrink when a smaller sail is hung on the
                # spar: a bowsprit or a jib-boom with yards crossed under it keeps the larger of
                # its named rating, from the headsails that load the stays' masts instead, and
                # the sails' (package 75, the lead's ruling of 2026-10-30, on the yards under the
                # 64's and the razee's bowsprit). No yard is crossed under those spars on the
                # eight files. Three of them chain a jib through a running bowsprit, and a jib is
                # no such sail: on the cutter and the smack the sails named are that jib, so
                # nothing shrinks; the lugger's flying jib keeps its 21.8 kN against the 37.4 named.
                if (
                    cls in ("bowsprit", "jib_boom")
                    and float(rating) > spar["rating_kn"]
                    and all(ship.under_bowsprit(s[0]) for s in sails)
                ):
                    spar["rating_kn"] = float(rating)
                    how = (
                        f"Rating: the sails named in the script in {rating.wind_kn:.0f} kn -> "
                        f"{spar['rating_kn']:g} kN, kept over {names}, the smaller load."
                    )
            else:
                # the engine hangs no sail's chain on this spar (a bare yard, a boom, the
                # bowsprit and jib-booms, whose headsails load the stays' masts instead):
                # keep the rating from the sails the script named for it
                spar["rating_kn"] = float(rating)
                how = (
                    f"Rating: the sails named in the script in {rating.wind_kn:.0f} kn -> "
                    f"{spar['rating_kn']:g} kN (the engine's graph loads nothing on it)."
                )
            self.notes[spar["id"]] = (self.notes.get(spar["id"], "").rstrip() + " " + how).strip()

    def whole_ship_groups(self):
        """The groups every ship has by the parts she has (package 33c; playtest 13's brig,
        `rig out the topmast stuns'ls` and `square the sails` refused): the studding sails
        of one level on every mast together ("the topmast studdingsails", the fore's and the
        main's), where she has any; and "the sails" for her working canvas, the "all sail"
        group (the storm canvas and the occasional sails are not in it, as they are not set
        with the rest). A group or an alias the ship's builder gave is kept."""
        sail_ids = [s["id"] for s in self.doc["sails"]]
        groups, aliases = self.doc["groups"], self.doc["aliases"]
        for level in ("lower", "topmast", "topgallant"):
            members = [i for i in sail_ids if f".{level}.studdingsail." in f".{i}"]
            name = f"{level} studdingsails"
            if members and name not in groups and name not in aliases:
                self.group(name, members)
        if "all sail" in groups and "sails" not in groups and "sails" not in aliases:
            self.alias("sails", "all sail")

    def descriptions(self, entries):
        """The vessel's descriptions at far detail (spec M5 §25; package 36): one file,
        two descriptions where the type served two trades (the brig-sloop of the Navy and
        the merchant brig). Each {key: {rig, what, note}}: her rig's word as the tops make
        it out at four miles, what she is when made out, and the source. Read by
        `freesail.world.ships` for the other sail; the engine's physics reads none of it."""
        self.doc["ship"]["descriptions"] = {
            key: {"rig": rig, "what": what, "note": note} for key, rig, what, note in entries
        }

    def dump(self, path, header):
        self.whole_ship_groups()
        self.rate_spars()
        text = yaml.safe_dump(self.doc, sort_keys=False, allow_unicode=True, width=100)
        # a sail's corners (package 57) on one line, as pairs: `corners_m: [[x, z], ...]`
        text = re.sub(
            r"^(  corners_m:)\n((?:  - - \S+\n    - \S+\n)+)",
            lambda mo: (
                mo.group(1)
                + " ["
                + ", ".join(
                    f"[{a}, {c}]" for a, c in re.findall(r"  - - (\S+)\n    - (\S+)\n", mo.group(2))
                )
                + "]\n"
            ),
            text,
            flags=re.M,
        )
        # the hull's profile (package 75) likewise, each of its lists on one line and
        # `sections_m` one station to a line, the form's mappings left as blocks; only inside
        # `  profile:`, so that no other list in a file moves
        text = re.sub(
            r"^  profile:\n(?:    .*\n)+", lambda mo: _flow_profile(mo.group(0)), text, flags=re.M
        )
        out = []
        in_hull = False
        hull_key = ""
        profile_key = ""
        in_crew = False
        crew_key = ""
        store_key = ""
        in_tackle = False
        in_boats = False
        in_gear = False
        in_pumps = False
        in_armament = False
        fit_name = ""
        gear_notes = getattr(self, "gear_notes", {})
        pump_notes = getattr(self, "pump_notes", {})
        armament_notes = getattr(self, "armament_notes", {})
        for line in text.splitlines():
            if line.startswith("hull:"):
                in_hull = True
            elif in_hull and not line.startswith("  "):
                in_hull = False
            if line.startswith("crew:"):
                in_crew = True
            elif in_crew and not line.startswith("  "):
                in_crew = False
            # the armament (package 70), noted as the ground tackle is: the section, each
            # fit above its name, a gun above its line
            if line.startswith("armament:"):
                in_armament = True
                note = armament_notes.get(("section",))
                if note:
                    out.append("# " + note)
            elif in_armament and not line.startswith("  "):
                in_armament = False
            if in_armament:
                note = None
                if m := re.match(r"^    ([^ :][^:]*):$", line):
                    fit_name = m.group(1).strip("'\"")
                    note = armament_notes.get(("fit", fit_name))
                elif m := re.match(r"^      - id: (\S+)$", line):
                    note = armament_notes.get(("gun", fit_name, m.group(1)))
                elif m := re.match(
                    r"^      (cartridges|charges|powder_barrels|exercise_charges):", line
                ):
                    # the magazine's keys (practice and resupply, between packages 72 and 73)
                    note = armament_notes.get(("magazine", fit_name, m.group(1)))
                if note:
                    out.append(" " * (len(line) - len(line.lstrip())) + "# " + note)
            if line.startswith("ground_tackle:"):
                in_tackle = True
                note = self.tackle_notes.get(("section",))
                if note:
                    out.append("# " + note)
            elif in_tackle and not line.startswith("  "):
                in_tackle = False
            if in_tackle and (m := re.match(r"^  - id: (\S+)$", line)):
                note = self.tackle_notes.get(("anchors", m.group(1)))
                if note:
                    out.append("  # " + note)
            # the hold and the boats (package 35), noted as the ground tackle is
            if line.startswith("hold:") and self.hold_note:
                out.append("# " + self.hold_note)
            if line.startswith("oars:") and self.oars_note:
                out.append("# " + self.oars_note)
            if line.startswith("boats:"):
                in_boats = True
                note = self.boat_notes.get(("section",))
                if note:
                    out.append("# " + note)
            elif in_boats and not line.startswith("  ") and not line.startswith("- "):
                in_boats = False
            if in_boats and (m := re.match(r"^- id: (\S+)$", line)):
                note = self.boat_notes.get(("boats", m.group(1)))
                if note:
                    out.append("# " + note)
            # the fishing gear (package 56), noted as the boats are
            if line.startswith("gear:"):
                in_boats = False
                in_gear = True
                note = gear_notes.get(("section",))
                if note:
                    out.append("# " + note)
            elif in_gear and not line.startswith("  ") and not line.startswith("- "):
                in_gear = False
            if in_gear and (m := re.match(r"^- id: (\S+)$", line)):
                note = gear_notes.get(("gear", m.group(1)))
                if note:
                    out.append("# " + note)
            # the pumps (package 73), noted as the boats are
            if line.startswith("pumps:"):
                in_boats = False
                in_gear = False
                in_pumps = True
                note = pump_notes.get(("section",))
                if note:
                    out.append("# " + note)
            elif in_pumps and not line.startswith("  ") and not line.startswith("- "):
                in_pumps = False
            if in_pumps and (m := re.match(r"^- id: (\S+)$", line)):
                note = pump_notes.get(("pumps", m.group(1)))
                if note:
                    out.append("# " + note)
            if in_crew:
                note = None
                if m := re.match(r"^    - kind: (\S+)$", line):
                    note = self.crew_notes.get(("sails", m.group(1)))
                elif m := re.match(r"^  - post: (.+)$", line):
                    note = self.crew_notes.get(("posts", m.group(1)))
                elif m := re.match(r"^  - role: (.+)$", line):
                    note = self.crew_notes.get(("people", m.group(1).strip("'\"")))
                elif m := re.match(r"^  (\w+):", line):
                    crew_key = m.group(1)
                    note = self.crew_notes.get((crew_key,))
                elif store_key == "spare_spars" and (m := re.match(r"^      (\w+): \d+$", line)):
                    note = self.crew_notes.get(("spare_spars", m.group(1)))
                elif store_key == "trimmers" and (m := re.match(r"^      (\w+): \d+$", line)):
                    note = self.crew_notes.get(("trimmers", m.group(1)))  # package 70
                elif m := re.match(r"^    (\w[^:]*):", line):
                    store_key = m.group(1)
                    note = self.crew_notes.get((crew_key, m.group(1)))
                if note:
                    out.append(" " * (len(line) - len(line.lstrip())) + "# " + note)
            m = re.match(r"^- id: (\S+)$", line)
            if m and m.group(1) in self.notes and not in_boats and not in_gear and not in_pumps:
                out.append("# " + self.notes[m.group(1)])
            m = re.match(r"^  (\w+):", line) if in_hull else None
            if m and m.group(1) in self.hull_notes:
                out.append("  # " + self.hull_notes[m.group(1)])
            if m:
                hull_key = m.group(1)
            # the hull's profile (package 75): its lines noted by their dotted keys,
            # "profile.<key>" above a line and "profile.<key>.<deck>" above a deck's; only
            # those, the profile's keys being four and six spaces in and the hull's own two
            elif in_hull and hull_key == "profile" and (m := re.match(r"^( {4}| {6})(\w+):", line)):
                if len(m.group(1)) == 4:
                    profile_key = m.group(2)
                    note = self.hull_notes.get(f"profile.{profile_key}")
                else:
                    note = self.hull_notes.get(f"profile.{profile_key}.{m.group(2)}")
                if note:
                    out.append(m.group(1) + "# " + note)
            out.append(line)
        # LF and UTF-8 on every platform (the comments carry the section sign and the degree)
        with open(path, "w", newline="\n", encoding="utf-8") as f:
            f.write(header + "\n".join(out) + "\n")


# -- the staysails between the masts (package 57) ---------------------------------------
# Steel 1794 vol. I, 'The Practice of Sail-making' (the OCR's lines 12222 to 12820), for the
# navy: the main staysail "is triangular, square on the foot ... extended upon the
# main-staysail-stay, between the main and fore masts, so that the foot will clear the boat
# upon the booms"; the mizen staysail "is quadrilateral, square on the foot ... it has a
# bunt two-fifths of the depth of the leech in the navy ... The foot drops within 6 or 7
# feet of the quarter-deck"; the main topmast staysail "is quadrilateral, cut square on the
# foot ... The leech is 4 or 5 yards deeper than the [main topsail], and there are one or
# two cloths more in the foot than the leech is yards in depth ... The bunt is two-fifths
# of the depth of the leech"; the middle staysail "is quadrilateral ... It has a square
# bunt five-twelfths of the depth of the leech ... The leech is from 4 to 7 yards deeper
# than the [main topgallant sail], and there are from 6 to 8 cloths more in the foot than
# the leech is yards in depth. Sloops and brigs in the navy have only from one to three";
# the main topgallant staysail "is quadrilateral ... It has a [bunt] from one-third to
# three-sevenths of the depth of the leech ... The leech is nearly of the same depth as
# the leech of the middle-staysail ... from 3 to 6 cloths more in the foot than the leech
# is yards in depth". His rule for the canvas (p. 96) groups the "Mizen staysails,
# main-topmast-staysails, middle staysails, and main-topgallant-staysails" as the
# four-sided ones and the "Main staysails, fore staysails, jibs" as the triangles. Each is
# cut here as he cuts it: the head along its stay, the leech and the bunt square to the
# foot (upright), the leech's depth and the foot's cloths by his rule where he gives them.
CLOTH_FT = 2.0  # a cloth of the navy's canvas, 24 inches (Steel's cloths; Lever 1808)
# The leech of a staysail hoisted to a mast head hangs clear before the top (or the
# cross-trees) under that head: a tenth of the lower yard of its mast before the mast for
# a top, a tenth of the topsail yard for the cross-trees (judgement: the top's half-breadth
# fore and aft; Steel's peak is at the head, its leech before the top's rim).
TOP_REACH_OF_YARD = 0.1


def stay_sail_cut(upper, lower, leech, *, peak_x=None, peak_z=None, foot=None, bunt=None):
    """A staysail cut on its stay, square on the foot (package 57): `upper` and `lower` the
    stay's ends (x forward of midships, height above the deck, metres), the peak on the
    stay at `peak_x` (or at the height `peak_z`), the leech `leech` metres upright under
    it to the clew, and the foot forward from the clew to the tack: `foot` metres long (the
    nock on the stay over the tack), or as long as a bunt of `bunt` of the leech makes it;
    with neither, a triangle whose tack is on the stay. The corners: [tack, nock, peak,
    clew], or [tack, peak, clew]."""
    (xu, zu), (xl, zl) = upper, lower
    slope = (zl - zu) / (xl - xu)

    def z_at(x):
        return zu + (x - xu) * slope

    def x_at(z):
        return xu + (z - zu) / slope

    if peak_z is not None:
        peak = (x_at(peak_z), peak_z)
    else:
        peak = (peak_x, z_at(peak_x))
    clew = (peak[0], peak[1] - leech)
    if foot is None and bunt is None:
        return [(x_at(clew[1]), clew[1]), peak, clew]
    if foot is not None:
        nock = (peak[0] + foot, z_at(peak[0] + foot))
    else:
        nz = peak[1] - (1.0 - bunt) * leech
        nock = (x_at(nz), nz)
    return [(nock[0], clew[1]), nock, peak, clew]


def stay_point(upper, lower, x):
    """The height of a stay at `x` (metres; its ends as `stay_sail_cut` takes them)."""
    (xu, zu), (xl, zl) = upper, lower
    return zu + (x - xu) * (zl - zu) / (xl - xu)


def staysail_from_cut(b, sid, stay, corners, deck_height, canvas, rope_in, words):
    """The staysail of these corners on its stay, its area and centre from them, its
    halyard, sheets and downhaul (sizes judgement, as the frigate's head sails')."""
    area_m2, cx, cz = _quad_area_centroid(corners)
    area = round(area_m2)
    shape = "a triangle" if len(corners) == 3 else "four-sided"
    if len(corners) == 4:
        tack, nock, peak, clew = corners
        cut = (
            f"leech {peak[1] - clew[1]:.1f} m, bunt {nock[1] - tack[1]:.1f} m "
            f"({(nock[1] - tack[1]) / (peak[1] - clew[1]):.2f} of the leech), foot "
            f"{nock[0] - clew[0]:.1f} m ({(nock[0] - clew[0]) / FT / CLOTH_FT:.0f} cloths)"
        )
    else:
        tack, peak, clew = corners
        cut = f"leech {peak[1] - clew[1]:.1f} m, foot {tack[0] - clew[0]:.1f} m"
    s = b.sail(
        sid,
        "jibheaded",
        stay=stay,
        area_m2=area,
        x_m=round(cx, 1),
        centre_height_m=round(deck_height + cz, 1),
        canvas_no=canvas[0],
        cloth_rating_kn=cloth(area, canvas[0]),
        corners_m=[[round(x, 2), round(z, 2)] for x, z in corners],
        note=f"{sid.replace('_', ' ').replace('.', ' ')} {area} m2, {shape}, square on the "
        f"foot (Steel 1794 vol. I, Sail-making): {cut}; {words}" + canvas_note(canvas),
    )
    # the sheet bears its sail: a rope whose working load is half the cloth's rating, so
    # that the cloth strains before the sheet parts (judgement; the strain rule parts a
    # line at 1.5 of its rating and a sail takes 0.6 of its pull on its sheet), the given
    # size the least
    rope_in = max(
        rope_in, math.ceil(4.0 * math.sqrt(0.5 * cloth(area, canvas[0]) / ROPE_KN_PER_SQ_IN)) / 4.0
    )
    b.line(f"{sid}.halyard", "halyard", s, rating=rope_kn(rope_in, 2))
    b.sided(
        f"{sid}.sheet",
        "sheet",
        s,
        rating=rope_kn(rope_in),
        note=f"{rope_in} in, to bear its sail: its working load half the cloth's rating "
        "(judgement).",
    )
    b.line(f"{sid}.downhaul", "downhaul", s, rating=rope_kn(quarter(rope_in * 0.8)))
    return s


def between_the_masts(b, *, geom, mast_x, rake_deg, deck_height, ahead, after, canvas, brig):
    """The staysails between the mast `ahead` and the mast `after` of a ship or a brig by
    Steel's rules (package 57; see above): the main (or the mizen) staysail, the topmast
    staysail, the middle staysail (on the main only) and the topgallant staysail, with the
    stays the new ones set on. Returns the sails, foremost level first."""
    ga, gf = geom[after], geom[ahead]

    def mx(name, z_m):
        return mast_x[name] - math.tan(math.radians(rake_deg[name])) * z_m

    def head(g, level):
        h = g["above"] + (g["t_hoist"] if level >= 1 else 0) + (g["g_hoist"] if level >= 2 else 0)
        return ft(h)

    def at(name, level):
        z = head(geom[name], level)
        return (mx(name, z), z)

    top_z = ft(ga["above"])  # the after mast's top, at its lower mast head
    top_x = mx(after, top_z) + TOP_REACH_OF_YARD * ft(ga["yard"])
    xtree_x = mx(after, head(ga, 1)) + TOP_REACH_OF_YARD * ft(ga["topsail_yard"])
    topsail_yd = (ga["topsail_h"] - ga["yard_h"]) / 3.0
    tg_yd = (ga["tg_h"] - ga["topsail_h"]) / 3.0
    yards_of_main = 1.0 if after == "main" else 5.0 / 7.0  # judgement: the mizen's 5/7
    out = []
    if after == "main":
        # the main staysail: a triangle on the main staysail stay (a brig's on her main stay,
        # "in small ships" as Steel has the mizen staysail on the mizen stay), its foot clear
        # of the boats on the booms, a fifth of the main mast's height above the deck
        # (judgement), its peak before the top
        if brig:
            stay = "main.stay"
        else:
            stay = b.line(
                "main.staysail.stay",
                "stay",
                "main.mast",
                rating=rope_kn(9.0),
                note="the main staysail stay, from the main mast head to a luff round the "
                "foremast (Steel 1794 vol. I, 'The main-staysail': 'The upper end clinches round "
                "the main-mast-head above the rigging and the lower end sets up with a "
                "luff-tackle round the foremast'); 9 in, judgement.",
            )
        foot_z = 0.2 * ft(ga["above"])
        ends = (at("main", 0), (mx(ahead, 1.0), 1.0))
        peak_z = stay_point(*ends, top_x)
        corners = stay_sail_cut(*ends, peak_z - foot_z, peak_x=top_x)
        out.append(
            staysail_from_cut(
                b,
                "main.staysail",
                stay,
                corners,
                deck_height,
                canvas["main.staysail"],
                3.5 if not brig else 3.0,
                "its tack at the stay over the boats on the booms (a fifth of the main mast's "
                "height above the deck, judgement), its peak before the main top. 'This sail is "
                "seldom used in large vessels' (Steel), and lying to under it is 'a mean between "
                "the two others' (Steel 1794 vol. II, 'Lying-to under the main staysail').",
            )
        )
    else:
        # the mizen staysail: four-sided, a bunt of two-fifths of the leech, on its own stay
        # in a ship from the mizen mast head to the deck abaft the main mast (Steel), its foot
        # within 6 or 7 feet of the quarter-deck, its peak before the mizen top
        stay = b.line(
            "mizzen.staysail.stay",
            "stay",
            "mizzen.mast",
            rating=rope_kn(6.0),
            note="the mizen staysail stay (Steel 1794 vol. I, 'The mizen-staysail': 'clinches "
            "round the head of the mizen-mast, then reeves through a thimble ... in a collar "
            "lashed round the main-mast, and sets up ... [to] an eye-bolt in the deck abaft the "
            "mast. In small ships, the mizen-staysail bends to the mizen-stay'); 6 in, "
            "judgement.",
        )
        ends = (at("mizzen", 0), (mx(ahead, 0.0) - 1.0, 0.0))
        leech = stay_point(*ends, top_x) - ft(6.5)
        corners = stay_sail_cut(*ends, leech, peak_x=top_x, bunt=0.4)
        out.append(
            staysail_from_cut(
                b,
                "mizzen.staysail",
                stay,
                corners,
                deck_height,
                canvas["mizzen.staysail"],
                3.0,
                "the bunt two-fifths of the leech and the foot 6 ft 6 in above the deck "
                "(Steel's 'within 6 or 7 feet of the quarter-deck'), its peak before the mizen "
                "top.",
            )
        )
    # the topmast staysail: the main's leech 4 or 5 yards (4.5) deeper than the main topsail,
    # its foot a cloth or two (1.5) more than the leech's yards (Steel); the mizen's the
    # main's rule on its own topsail and five-sevenths of it (judgement: Steel's mizen
    # topmast staysail is not in the OCR; Luce's mizen yards are 5/7 of the main's)
    if after == "main":
        mts_stay = "main.topmast.stay"
        mts_lower = at(ahead, 0)
        leech_yd = topsail_yd + 4.5
        foot_ft = (leech_yd + 1.5) * CLOTH_FT
    else:
        mts_stay = b.line(
            "mizzen.topmast.stay",
            "stay",
            "mizzen.topmast",
            rating=rope_kn(4.5),
            note="the mizen topmast stay, to a collar at the fore part of the main mast 'close "
            "up to the bibs' (Steel 1794 vol. I, 'The mizen topmast-stay'); 4.5 in, judgement; "
            "the mizen topmast staysail sets on it.",
        )
        mts_lower = (mx(ahead, ft(gf["above"] - gf["head"])), ft(gf["above"] - gf["head"]))
        main_topsail_yd = (gf["topsail_h"] - gf["yard_h"]) / 3.0
        leech_yd = (main_topsail_yd + 4.5) * yards_of_main
        foot_ft = (main_topsail_yd + 4.5 + 1.5) * CLOTH_FT * yards_of_main
    corners = stay_sail_cut(
        at(after, 1), mts_lower, ft(3.0 * leech_yd), peak_x=top_x, foot=ft(foot_ft)
    )
    words = (
        "the leech 4 or 5 yards deeper than the main topsail, a cloth or two more in the foot "
        "than the leech's yards (Steel; the mean of each taken), the bunt as the stay leaves it "
        "(Steel: two-fifths of the leech), its peak before the main top."
        if after == "main"
        else "the main topmast staysail's rule on the main's topsail and five-sevenths of it "
        "(judgement: Steel's article is not in the OCR), the bunt as the stay leaves it, its "
        "peak before the mizen top."
    )
    sid = f"{after}.topmast_staysail"
    out.append(
        staysail_from_cut(
            b, sid, mts_stay, corners, deck_height, canvas[sid], 3.0 if not brig else 2.5, words
        )
    )
    if after == "main":
        # the middle staysail, on its own stay from the main topmast head to the fore topmast
        # under the parral ('a strap or grommet made fast round the fore-topmast, under the
        # parral', Steel 1794 vol. I, 'The middle-staysail'): a third of the topmast's hoist
        # above the fore cap (judgement)
        mid_stay = b.line(
            "middle_staysail.stay",
            "stay",
            "main.topmast",
            rating=rope_kn(4.0 if not brig else 3.0),
            note="the middle staysail stay, from the main topmast head to a grommet round the "
            "fore topmast under the parral (Steel 1794 vol. I, 'The middle-staysail'), a third "
            "of the topmast's hoist above the fore cap (judgement); size judgement.",
        )
        low_z = ft(gf["above"] + 0.35 * gf["t_hoist"])
        mid_leech_yd = tg_yd + 5.5
        mid_cloths = mid_leech_yd + (2.0 if brig else 7.0)
        corners = stay_sail_cut(
            at("main", 1),
            (mx(ahead, low_z), low_z),
            ft(3.0 * mid_leech_yd),
            peak_x=top_x,
            foot=ft(mid_cloths * CLOTH_FT),
        )
        out.append(
            staysail_from_cut(
                b,
                "middle_staysail",
                mid_stay,
                corners,
                deck_height,
                canvas["middle_staysail"],
                2.5 if not brig else 2.0,
                "the leech 4 to 7 yards (5.5) deeper than the main topgallant sail, "
                + (
                    "two cloths more in the foot than the leech's yards ('Sloops and brigs in "
                    "the navy have only from one to three')"
                    if brig
                    else "7 cloths more in the foot than the leech's yards (6 to 8)"
                )
                + " (Steel), the bunt as the stay leaves it (Steel: five-twelfths of the "
                "leech), its peak before the main top.",
            )
        )
    else:
        mid_leech_yd = (
            gf["tg_h"] - gf["topsail_h"]
        ) / 3.0 + 5.5  # the main's middle staysail's leech
    # the topgallant staysail: the main's leech nearly the middle staysail's, 3 to 6 cloths
    # (4.5) more in the foot (Steel); the mizen's five-sevenths of it (judgement), on the
    # mizen topgallant stay that 'trices up to the main-topmast-head' (Steel)
    if after == "main":
        tg_stay = "main.topgallant.stay"
        if not brig:
            tg_stay = b.line(
                "main.topgallant.stay",
                "stay",
                "main.topgallant_mast",
                rating=rope_kn(3.5),
                note="the main topgallant stay, through a block at the fore topmast head and "
                "down to the fore top (Steel 1794 vol. I, 'The main-topgallant-stay'); 3.5 in, "
                "judgement; the main topgallant staysail sets on it.",
            )
    else:
        tg_stay = b.line(
            "mizzen.topgallant.stay",
            "stay",
            "mizzen.topgallant_mast",
            rating=rope_kn(3.0),
            note="the mizen topgallant stay, which 'trices up to the main-topmast-head' (Steel "
            "1794 vol. I); 3 in, judgement; the mizen topgallant staysail sets on it.",
        )
    tg_leech_yd = mid_leech_yd * yards_of_main
    tg_foot_ft = (mid_leech_yd + 4.5) * CLOTH_FT * yards_of_main
    corners = stay_sail_cut(
        at(after, 2), at(ahead, 1), ft(3.0 * tg_leech_yd), peak_x=xtree_x, foot=ft(tg_foot_ft)
    )
    sid = f"{after}.topgallant_staysail"
    out.append(
        staysail_from_cut(
            b,
            sid,
            tg_stay,
            corners,
            deck_height,
            canvas[sid],
            2.0,
            (
                "the leech nearly the middle staysail's, 4 or 5 cloths more in the foot than "
                "the leech's yards (Steel: 3 to 6), the bunt as the stay leaves it (Steel: a "
                "third to three-sevenths of the leech), its peak before the topmast cross-trees."
                if after == "main"
                else "the main topgallant staysail's rule and five-sevenths of it (judgement; "
                "Steel's 'Royal staysails ... the same as a topgallant-staysail'), its peak "
                "before the mizen topmast cross-trees."
            ),
        )
    )
    return out


def square_sail_lines(b, sail, yard, sizes, hoisting, course=False, reef=False, bowline=False):
    """The essential running rigging of a square sail and its yard, rated from rope sizes.

    `sizes` maps a line class to a rope circumference in inches (halyard: the tye).
    Courses and topsails (`course`, `bowline`) carry a bowline a side, its bridles
    taken as one part (spec 3b §4).
    """
    r = {cls: rope_kn(c) for cls, c in sizes.items()}
    if hoisting:
        b.line(f"{yard}.halyard", "halyard", yard, rating=r["halyard"])
    b.sided(f"{yard}.brace", "brace", yard, rating=r["brace"])
    b.sided(f"{yard}.lift", "lift", yard, rating=r["lift"])
    b.sided(f"{sail}.sheet", "sheet", sail, rating=r["sheet"])
    b.sided(f"{sail}.clewline", "clewline", sail, rating=r["clewline"])
    b.line(f"{sail}.buntline", "buntline", sail, rating=r["buntline"])
    if course:
        b.sided(f"{sail}.tack", "tack", sail, rating=r["tack"])
    if course or bowline:
        b.sided(
            f"{sail}.bowline",
            "bowline",
            sail,
            rating=r["bowline"],
            note=f"{sail} bowline, one a side with its bridles: hauls the weather leech "
            "forward on a wind (Luce 1884 ch. IX, 'Bowlines'; ch. X, 'two bowline-cringles "
            "and one bridle on each leech'; Kipping, Sails and Sailmaking, the 1847 text); a "
            f"lighter rope than the sheet, {sizes['bowline']} in (judgement), rated by Luce "
            "1866 ch. IV.",
        )
    if reef:
        b.sided(f"{sail}.reef_tackle", "reef_tackle", sail, rating=r["reef_tackle"])


# ---------------------------------------------------------------------------
# The frigate: Amazon class, 1795
# ---------------------------------------------------------------------------

# Rope sizes (inches circumference) for the main's gear by level. Fore gear is 0.92 of the
# main's and mizzen gear 0.8, rounded to the quarter inch (judgement: the customary
# proportions of an 18-pounder frigate's establishment; not in the OCR references).
FRIGATE_ROPE = {
    "course": {
        "sheet": 7.0,
        "tack": 8.0,
        "brace": 5.0,
        "lift": 5.0,
        "clewline": 4.0,
        "buntline": 3.0,
        "bowline": 4.0,
        "reef_tackle": 4.0,
    },
    "topsail": {
        "halyard": 6.0,  # the tye; the halyard fall is a purchase on it
        "sheet": 5.5,
        "brace": 4.0,
        "lift": 3.5,
        "clewline": 3.5,
        "buntline": 2.5,
        "reef_tackle": 3.5,
        # the topsail bowline: the clewline's size, as the course's bowline is its
        # clewline's (judgement; spec 3b §4, "a topsail sheet's lighter rope")
        "bowline": 3.5,
    },
    "topgallant": {
        "halyard": 3.0,
        "sheet": 3.0,
        "brace": 2.5,
        "lift": 2.5,
        "clewline": 2.5,
        "buntline": 2.0,
    },
    "royal": {
        "halyard": 2.0,
        "sheet": 2.0,
        "brace": 1.75,
        "lift": 1.75,
        "clewline": 1.75,
        "buntline": 1.5,
    },
}
FRIGATE_MAST_ROPE_FACTOR = {"fore": 0.92, "main": 1.0, "mizzen": 0.8}


def frigate(out_dir="data/ships"):
    # -- hull: Amazon class 36-gun 18-pounder frigate, Sir William Rule, launched 1795 ------
    # Dimensions as published (Winfield, British Warships in the Age of Sail 1793-1817, via
    # the class's Wikipedia entries): gundeck 143 ft 2.5 in, keel 119 ft 5.5 in, extreme
    # breadth 38 ft 4 in, depth in hold 13 ft 6 in, 933 67/94 tons burthen; draught unladen
    # 10 ft 3 in forward, 15 ft 3 in aft.
    gundeck_ft = 143.2
    beam_ft = 38.33
    lwl_ft = round(0.957 * gundeck_ft)  # judgement: the load line is 0.96 of the gundeck, 137 ft
    draught_ft = 15.0  # judgement: mean of 13 ft forward and 17 ft aft, stored for sea
    lwl = ft(lwl_ft)
    beam = ft(beam_ft)
    draught = ft(draught_ft)
    # Displacement: LWL x beam x draught x block coefficient 0.55 (a frigate's body is fuller
    # than her sharp ends suggest) x 1025 kg/m3 = about 1,270 t, 1.36 x the burthen, which is
    # the usual ratio for a frigate of the period.
    displacement = round(lwl * beam * draught * 0.55 * 1025.0, -4)
    deck_height = 1.8  # the upper (gun) deck at midships: port sills about 8 ft above water

    b = Builder(
        "Amazon",
        "ship",
        "A 36-gun 18-pounder frigate of the Amazon class (Sir William Rule, launched 1795): "
        "gundeck 143 ft 2.5 in, keel 119 ft 5.5 in, beam 38 ft 4 in, 933 tons burthen. "
        "Spars by the rules of Luce 1866 ch. VII checked against Falconer 1780; "
        "rope by Luce ch. IV; see tools/gen_ships.py for every rule and judgement.",
        {
            "length_waterline_m": lwl,
            "beam_m": beam,
            "draught_m": draught,
            "displacement_kg": displacement,
            "gm_m": 1.3,
            "clr_x_m": 3.0,
            "lateral_area_m2": round(lwl * draught * 0.85, -1),
            "hull_speed_kn": 13.0,
            "deck_height_m": deck_height,
            "rudder": {"area_m2": 6.0, "max_angle_deg": 35, "rate_deg_s": 3.0, "span_m": 4.6},
        },
        {
            "length_waterline_m": f"{lwl_ft:.0f} ft: judgement, 0.96 of the 143 ft gundeck "
            "(keel 119 ft 6 in). Amazon class 1795, Winfield.",
            "beam_m": "38 ft 4 in extreme breadth (Winfield).",
            "draught_m": f"{draught_ft:.0f} ft mean, judgement: 13 ft forward, 17 ft aft stored "
            "for sea (unladen 10 ft 3 in / 15 ft 3 in, Winfield).",
            "displacement_kg": "LWL x beam x draught x Cb 0.55 x 1025: about 1,270 t, 1.36 x "
            "the 933 tons burthen (judgement: the usual ratio for the type).",
            "gm_m": "4 ft 3 in: judgement, typical of an 18-pounder frigate (3.5 to 5 ft).",
            "clr_x_m": "Geometric centre of the lateral plane about 1.0 m abaft midships "
            "(drag of the keel, deadwood aft); the centre of pressure with way on lies a "
            "lead of about 10 per cent of LWL ahead of it (judgement): +3.0 m. Package 8 "
            "set +3.5; package 10 moved it 0.5 m aft after the raked masts carried the "
            "sail centres aft (docs/dev/TuningNotes.md): with the tuned curves she then "
            "carries about 1 deg of weather helm close-hauled and 2 on a beam reach in "
            "15 kn (truth 6), and gets under way from rest without rounding up into "
            "the wind (truth 17); at +3.5 she rounded up to 33 deg off with sternway.",
            "lateral_area_m2": "LWL x draught x 0.85 for the fullness of the profile.",
            "hull_speed_kn": "The best speed of 18-pounder frigates in sailing-quality "
            "reports is 12 to 13 knots (Winfield); the derived 1.34 sqrt(LWL ft) = 15.7 is "
            "a modern yacht's figure. Package 10 may tune within 12.5 to 13.5.",
            "deck_height_m": "Upper (gun) deck at midships, about 6 ft above the load line.",
            "rudder": "Blade about 15 ft by 4 ft 3 in (span_m its depth, 15 ft: with the area "
            "it gives the blade's aspect ratio and so its lift slope, physics/hull.py, package "
            "32e); 35 degrees is the period stop.",
        },
    )

    # -- spars in feet by Luce 1866 ch. VII (see the module docstring) --------------------
    main_len = (lwl_ft + beam_ft) / 2.0  # 87.7 ft heel to head
    step_to_deck = 14.0  # depth in hold 13.5 ft plus the step on the keelson
    mast_ratio = {"fore": 0.9, "main": 1.0, "mizzen": 13.0 / 15.0}
    yard_ratio = {"fore": 0.9, "main": 1.0, "mizzen": 5.0 / 7.0}
    # positions: fore mast about 1/8 of the gundeck abaft the stem, main a little abaft
    # midships, mizzen about 1/6 before the taffrail (the draught of the class)
    mast_x = {"fore": 14.0, "main": -2.0, "mizzen": -16.0}

    geom = {}
    for name in ("fore", "main", "mizzen"):
        L = main_len * mast_ratio[name]
        if name == "mizzen":
            # steps a deck higher than the others; judgement: apply 13/15 to the height
            # above deck rather than to the whole stick
            above = (main_len - step_to_deck) * mast_ratio[name]
        else:
            above = L - step_to_deck
        head = L / 6.0
        T = 0.6 * main_len * (1.0 if name == "main" else (0.9 if name == "fore" else 5.0 / 7.0))
        t_head = T / 6.0
        t_hoist = T - head  # above the lower cap: the doubling is the lower mast head
        G = T / 2.0
        g_head = G / 6.0
        g_hoist = G - t_head
        R = 2.0 * G / 3.0
        r_hoist = R - g_head
        yard = (10.0 / 11.0) * main_len * yard_ratio[name]
        topsail_yard = 0.75 * (10.0 / 11.0) * main_len * yard_ratio[name]
        tg_yard = (9.0 / 14.0) * topsail_yard
        royal_yard = (2.0 / 3.0) * tg_yard  # judgement: British 1790s royals, not Luce's 9/20
        yard_h = above - head - 2.0  # slung a little below the hounds
        topsail_h = above + t_hoist - t_head  # hoisted to the topmast hounds
        tg_h = above + t_hoist + g_hoist - g_head
        royal_h = above + t_hoist + g_hoist + r_hoist - 1.0
        geom[name] = {
            "above": above,
            "head": head,
            "t_len": T,
            "t_hoist": t_hoist,
            "g_hoist": g_hoist,
            "r_hoist": r_hoist,
            "yard": yard,
            "topsail_yard": topsail_yard,
            "tg_yard": tg_yard,
            "royal_yard": royal_yard,
            "yard_h": yard_h,
            "topsail_h": topsail_h,
            "tg_h": tg_h,
            "royal_h": royal_h,
        }

    # sail areas (m2) and centres (m above water) from the spar geometry
    def trapezoid(head_ft, foot_ft, depth_ft):
        return round((head_ft + foot_ft) / 2.0 * depth_ft * FT * FT)

    areas = {}
    for name, g in geom.items():
        levels = {}
        if name != "mizzen":
            depth = 0.42 * g["yard"]  # judgement: the drop of a course is 0.42 of its yard
            levels["course"] = (
                trapezoid(0.9 * g["yard"], 0.9 * g["yard"], depth),
                round(deck_height + (g["yard_h"] - 0.45 * depth) * FT, 1),
            )
        depth = g["topsail_h"] - g["yard_h"]
        levels["topsail"] = (
            trapezoid(0.82 * g["topsail_yard"], 0.9 * g["yard"], depth),
            round(deck_height + (g["yard_h"] + 0.5 * depth) * FT, 1),
        )
        depth = g["tg_h"] - g["topsail_h"]
        levels["topgallant"] = (
            trapezoid(0.89 * g["tg_yard"], 0.9 * g["topsail_yard"], depth),
            round(deck_height + (g["topsail_h"] + 0.5 * depth) * FT, 1),
        )
        depth = g["royal_h"] - g["tg_h"]
        levels["royal"] = (
            trapezoid(0.89 * g["royal_yard"], 0.9 * g["tg_yard"], depth),
            round(deck_height + (g["tg_h"] + 0.5 * depth) * FT, 1),
        )
        areas[name] = levels

    # studding sails: width 0.4 of the yard they hang from, as deep as the sail beside them
    stuns_area = {}
    for name in ("fore", "main"):
        g = geom[name]
        stuns_area[name] = {
            "lower": round(0.4 * g["yard"] * 0.9 * 0.42 * g["yard"] * FT * FT),
            "topmast": round(0.4 * g["topsail_yard"] * (g["topsail_h"] - g["yard_h"]) * FT * FT),
            "topgallant": round(0.4 * g["tg_yard"] * (g["tg_h"] - g["topsail_h"]) * FT * FT),
        }

    # Brace limits, degrees from square (spec 3b §2.1). Fincham 1843 art. 102: Hardy's
    # squadron of 1827 measured the long, fine 28-gun ships "bracing their main-yard from
    # 23 deg to 29 deg, and their fore-yards from 26 deg to 30 deg" from the keel (61 to
    # 67 and 60 to 64 from square); they "seldom" lay within six points. A long frigate
    # of 1795, coppered and well found, takes the long ships' upper values for her lower
    # yards: main 64, fore 62, the crossjack 60 (its shrouds, on the mizzen, stand
    # closer). Each yard above its lower yard braces two degrees more, the shrouds
    # converging aloft (judgement, as before).
    plans = {
        "fore": [("course", 62), ("topsail", 64), ("topgallant", 66), ("royal", 68)],
        "main": [("course", 64), ("topsail", 66), ("topgallant", 68), ("royal", 70)],
        "mizzen": [("topsail", 62), ("topgallant", 64), ("royal", 66)],
    }
    yards_by_level = {"course": [], "topsail": [], "topgallant": [], "royal": []}
    sails_by_level = {"course": [], "topsail": [], "topgallant": [], "royal": []}
    yard_lengths = {
        "course": "yard",
        "topsail": "topsail_yard",
        "topgallant": "tg_yard",
        "royal": "royal_yard",
    }
    yard_heights = {
        "course": "yard_h",
        "topsail": "topsail_h",
        "topgallant": "tg_h",
        "royal": "royal_h",
    }
    level_of_spar = {
        "course": "lower",
        "topsail": "topsail",
        "topgallant": "topgallant",
        "royal": "royal",
    }

    mast_rule = {
        "main": "Luce: (LWL + breadth)/2",
        "fore": "Luce: 9/10 of the main",
        "mizzen": "Luce: 13/15 of the main",
    }
    for name in ("fore", "main", "mizzen"):
        g = geom[name]
        x = mast_x[name]
        lv = areas[name]
        # what each mast carries, for the spar ratings (no studding sails)
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
            # the lower mast also carries the spanker (set below)
            carried["lower"].append((SPANKER_AREA, SPANKER_CENTRE, "gaff"))
        prov = " Provisional (truth 9), see gen_ships.py."
        lower = b.spar(
            f"{name}.mast",
            "mast",
            x_m=x,
            rake_deg=FRIGATE_RAKE_DEG[name],
            height_m=ft(g["above"]),
            rating_kn=design_kn(carried["lower"], DESIGN_WIND_KN["lower"]),
            note=f"{name} lower mast: {main_len * mast_ratio[name]:.0f} ft heel to head "
            f"({mast_rule[name]}), "
            f"{g['above']:.0f} ft above the deck.{prov}",
        )
        top = b.spar(
            f"{name}.topmast",
            "topmast",
            steps_on=lower,
            height_m=ft(g["t_hoist"]),
            rating_kn=design_kn(carried["topsail"], DESIGN_WIND_KN["topsail"]),
            note=f"{name} topmast: {g['t_len']:.0f} ft "
            f"(Luce: 3/5 of the main mast), {g['t_hoist']:.0f} ft of it above the lower "
            f"cap.{prov}",
        )
        tg = b.spar(
            f"{name}.topgallant_mast",
            "topgallant_mast",
            steps_on=top,
            height_m=ft(g["g_hoist"]),
            rating_kn=design_kn(carried["topgallant"], DESIGN_WIND_KN["topgallant"]),
            note=f"{name} topgallant mast: half the topmast (Luce), {g['g_hoist']:.0f} ft above "
            f"the topmast cap.{prov}",
        )
        royal = b.spar(
            f"{name}.royal_mast",
            "royal_mast",
            steps_on=tg,
            height_m=ft(g["r_hoist"]),
            rating_kn=design_kn(carried["royal"], DESIGN_WIND_KN["royal"]),
            note=f"{name} royal mast: 2/3 of the topgallant mast (Luce), {g['r_hoist']:.0f} ft "
            f"above its head.{prov}",
        )
        on_spar = {"course": lower, "topsail": top, "topgallant": tg, "royal": royal}
        for level, limit in plans[name]:
            yard_id = f"{name}.{level}.yard" if level != "course" else f"{name}.yard"
            sail_id = f"{name}.{level}" if level != "course" else f"{name}.course"
            area, centre = lv[level]
            rule = {
                "course": "10/11 of the mast (Luce; Falconer: 0.575 of the gundeck)",
                "topsail": "3/4 of the lower yard (Luce)",
                "topgallant": "9/14 of the topsail yard (Luce)",
                "royal": "2/3 of the topgallant yard (judgement; Luce's 9/20 is the later "
                "small royal)",
            }[level]
            yard = b.spar(
                yard_id,
                "yard",
                on=on_spar[level],
                length_m=ft(g[yard_lengths[level]]),
                height_m=ft(g[yard_heights[level]]),
                brace_limit_deg=limit,
                rating_kn=design_kn(
                    carried[level_of_spar[level]], DESIGN_WIND_KN[level_of_spar[level]]
                ),
                note=f"{name} {level} yard {g[yard_lengths[level]]:.0f} ft, {rule}; braces "
                f"{limit} deg from square (Fincham 1843 art. 102, the long ships' upper "
                f"value{'' if level == 'course' else ', two degrees a level aloft'}).{prov}",
            )
            reef = {"course": 1, "topsail": 3, "topgallant": 0, "royal": 0}[level]
            canvas = FRIGATE_CANVAS[sail_id]
            sail = b.sail(
                sail_id,
                "square",
                yard=yard,
                area_m2=area,
                reef_bands=reef,
                # package 57: the royals set flying (Steel 1794 vol. I p. 214, ROYALS "Are set
                # flying"), sent down on deck with their yards when taken in
                flying=True if level == "royal" else None,
                x_m=raked_x(x, FRIGATE_RAKE_DEG[name], centre),
                centre_height_m=centre,
                canvas_no=canvas[0],
                cloth_rating_kn=cloth(area, canvas[0]),
                note=f"{name} {level}: {area} m2 between its yard and the yardarms below "
                f"(head {0.9 if level == 'course' else (0.82 if level == 'topsail' else 0.89):.2f} "
                f"of the yard).{canvas_note(canvas)}",
            )
            factor = FRIGATE_MAST_ROPE_FACTOR[name]
            sizes = {cls: quarter(c * factor) for cls, c in FRIGATE_ROPE[level].items()}
            square_sail_lines(
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
        shroud_size, shroud_count = (9.5, 9) if name != "mizzen" else (6.5, 6)
        b.sided(
            f"{name}.shrouds",
            "shroud",
            lower,
            rating=rope_kn(shroud_size, shroud_count),
            note=f"{shroud_count} shrouds of {shroud_size} in a side (Luce 1866 ch. VIII: "
            "first rates 10 1/2 in, one inch less per class).",
        )
        bs_size = 6.0 if name != "mizzen" else 4.5
        b.sided(f"{name}.topmast.backstay", "backstay", top, rating=rope_kn(bs_size, 2))

    g = geom["mizzen"]
    b.spar(
        "mizzen.crossjack.yard",
        "yard",
        on="mizzen.mast",
        length_m=ft(g["yard"]),
        height_m=ft(g["yard_h"]),
        brace_limit_deg=60,
        rating_kn=design_kn(
            [(areas["mizzen"]["topsail"][0], areas["mizzen"]["topsail"][1], "square")],
            DESIGN_WIND_KN["lower"],
        ),
        note=f"crossjack yard {g['yard']:.0f} ft, 5/7 of the main yard (Luce; Falconer: equal "
        "to the fore topsail yard); crosses no sail, spreads the mizzen topsail's foot; "
        "braces 60 deg from square (Fincham 1843 art. 102: the long ships' lower yards 61 to "
        "67 from square; the mizzen's shrouds stand closer, judgement, spec 3b §2.1).",
    )
    b.sided(
        "mizzen.crossjack.yard.brace",
        "brace",
        "mizzen.crossjack.yard",
        rating=rope_kn(quarter(5.0 * FRIGATE_MAST_ROPE_FACTOR["mizzen"])),
    )
    # spanker: boom 1/2 the main mast, gaff 4/5 of the boom (Luce)
    boom_ft = 0.5 * main_len
    gaff_ft = 0.8 * boom_ft
    gaff = b.spar(
        "mizzen.gaff",
        "gaff",
        on="mizzen.mast",
        length_m=ft(gaff_ft),
        height_m=ft(g["above"] - g["head"] - 3.0),
        rating_kn=design_kn([(SPANKER_AREA, SPANKER_CENTRE, "gaff")], DESIGN_WIND_KN["gaff"]),
        note=f"spanker gaff {gaff_ft:.0f} ft, 4/5 of the boom (Luce).",
    )
    boom = b.spar(
        "mizzen.boom",
        "boom",
        on="mizzen.mast",
        length_m=ft(boom_ft),
        height_m=2.4,
        horse_m=round(0.5 * beam, 1),
        rating_kn=design_kn([(SPANKER_AREA, SPANKER_CENTRE, "gaff")], DESIGN_WIND_KN["gaff"]),
        note=f"spanker boom {boom_ft:.0f} ft, half the main mast (Luce); horse_m " + HORSE_NOTE,
    )
    spanker = b.sail(
        "mizzen.spanker",
        "gaff",
        mast="mizzen.mast",
        gaff=gaff,
        boom=boom,
        area_m2=SPANKER_AREA,
        reef_bands=2,
        x_m=raked_x(-21.0, FRIGATE_RAKE_DEG["mizzen"], SPANKER_CENTRE),
        centre_height_m=SPANKER_CENTRE,
        canvas_no=FRIGATE_CANVAS["mizzen.spanker"][0],
        cloth_rating_kn=cloth(SPANKER_AREA, FRIGATE_CANVAS["mizzen.spanker"][0]),
        note=f"spanker (driver) {SPANKER_AREA} m2: foot 0.9 of the boom, head 0.9 of the gaff, "
        "hoist from boom to jaws, gaff peaked 40 degrees; centre 0.4 of the boom abaft the mast."
        + canvas_note(FRIGATE_CANVAS["mizzen.spanker"]),
    )
    b.line("mizzen.gaff.throat_halyard", "throat_halyard", gaff, rating=rope_kn(4.5, 3))
    b.line("mizzen.gaff.peak_halyard", "peak_halyard", gaff, rating=rope_kn(4.0, 4))
    b.line("mizzen.spanker.sheet", "sheet", spanker, rating=rope_kn(5.0, 2), parts=2)
    b.line("mizzen.spanker.outhaul", "outhaul", spanker, rating=rope_kn(3.5))
    b.sided("mizzen.gaff.vang", "vang", gaff, rating=rope_kn(3.5))

    # head: bowsprit 5/8 of the main mast, one third inboard; jib-boom 6/7 of the bowsprit,
    # 7/12 of it outboard (Luce); flying jib-boom 2/3 of the jib-boom's outboard part
    # (judgement). length_m is the outboard part.
    bowsprit_ft = 5.0 / 8.0 * main_len
    bowsprit_out = bowsprit_ft * 2.0 / 3.0
    jib_boom_ft = 6.0 / 7.0 * bowsprit_ft
    jib_boom_out = jib_boom_ft * 7.0 / 12.0
    flying_out = 2.0 / 3.0 * jib_boom_out
    heads = [
        ("fore.topmast_staysail", "fore.topmast.stay", 75, 24.0, 10.0),
        ("jib", "jib.stay", 130, 31.0, 12.0),
        ("flying_jib", "flying_jib.stay", 70, 37.0, 14.0),
    ]
    head_loads = {sid: (area, h, "jibheaded") for sid, _, area, _, h in heads}
    bowsprit = b.spar(
        "bowsprit",
        "bowsprit",
        x_m=21.0,
        length_m=ft(bowsprit_out),
        height_m=6.0,
        rating_kn=design_kn(list(head_loads.values()), DESIGN_WIND_KN["lower"]),
        note=f"bowsprit {bowsprit_ft:.0f} ft, 5/8 of the main mast, {bowsprit_out:.0f} ft "
        "outboard (Luce).",
    )
    jib_boom = b.spar(
        "jib_boom",
        "jib_boom",
        on=bowsprit,
        length_m=ft(jib_boom_out),
        height_m=8.0,
        rating_kn=design_kn(
            [head_loads["jib"], head_loads["flying_jib"]], DESIGN_WIND_KN["jib_boom"]
        ),
        note=f"jib-boom {jib_boom_ft:.0f} ft, 6/7 of the bowsprit, {jib_boom_out:.0f} ft outboard "
        f"(Luce).{prov}",
    )
    b.spar(
        "flying_jib_boom",
        "flying_jib_boom",
        on=jib_boom,
        length_m=ft(flying_out),
        height_m=9.0,
        rating_kn=design_kn([head_loads["flying_jib"]], DESIGN_WIND_KN["flying_jib_boom"]),
        note=f"flying jib-boom {flying_out:.0f} ft outboard (judgement).{prov}",
    )
    b.line(
        "fore.stay",
        "stay",
        "fore.mast",
        rating=rope_kn(15.0),
        note="15 in (judgement; Luce: an 8 in collar 'for a frigate').",
    )
    b.line(
        "fore.topmast.stay",
        "stay",
        "fore.topmast",
        rating=rope_kn(7.5),
        note="7.5 in; carries the fore topmast staysail.",
    )
    b.line(
        "jib.stay",
        "stay",
        "fore.topmast",
        rating=rope_kn(5.0),
        note="5 in, from the fore topmast head to the jib-boom end: the jib sets on it.",
    )
    b.line(
        "flying_jib.stay",
        "stay",
        "fore.topgallant_mast",
        rating=rope_kn(3.5),
        note="3.5 in, from the fore topgallant mast head to the flying jib-boom end.",
    )
    b.line("main.stay", "stay", "main.mast", rating=rope_kn(16.0), note="16 in (judgement).")
    b.line("main.topmast.stay", "stay", "main.topmast", rating=rope_kn(7.5))
    b.line("bobstay", "stay", bowsprit, rating=rope_kn(12.0))
    b.line("martingale", "stay", jib_boom, rating=rope_kn(5.0))
    headsails = []
    for sid, stay, area, x, h in heads:
        s = b.sail(
            sid,
            "jibheaded",
            stay=stay,
            area_m2=area,
            x_m=x,
            centre_height_m=h,
            canvas_no=FRIGATE_CANVAS[sid][0],
            cloth_rating_kn=cloth(area, FRIGATE_CANVAS[sid][0]),
            note=f"{sid.replace('_', ' ').replace('.', ' ')} {area} m2 (judgement from the "
            "stay's run: luff along the stay, foot to the boom end)."
            + canvas_note(FRIGATE_CANVAS[sid]),
        )
        size = {"fore.topmast_staysail": 3.5, "jib": 3.5, "flying_jib": 2.5}[sid]
        b.line(f"{sid}.halyard", "halyard", s, rating=rope_kn(size, 2))
        b.sided(f"{sid}.sheet", "sheet", s, rating=rope_kn(size))
        b.line(f"{sid}.downhaul", "downhaul", s, rating=rope_kn(quarter(size * 0.8)))
        headsails.append(s)
    # package 57 (gate 6c's finding; the owner's word of 2026-10-17): the staysails between
    # the masts by Steel's list for a ship, the main topmast staysail among them (80 m2 of
    # judgement before), each cut as Steel cuts it (`between_the_masts`)
    staysail_kw = dict(
        geom=geom,
        mast_x=mast_x,
        rake_deg=FRIGATE_RAKE_DEG,
        deck_height=deck_height,
        canvas=FRIGATE_CANVAS,
        brig=False,
    )
    between = between_the_masts(b, ahead="fore", after="main", **staysail_kw)
    between += between_the_masts(b, ahead="main", after="mizzen", **staysail_kw)

    # studding sails on fore and main: lower (fore only), topmast, topgallant. The boom is
    # linked to the sail's own yard (so both go with it) and sits where it is rigged: the
    # swinging boom at the rail, the topmast booms on the lower yard, the topgallant booms
    # on the topsail yard.
    stuns = []
    for name in ("fore", "main"):
        x = mast_x[name]
        g = geom[name]
        for level, parent_yard, boom_len, boom_h, centre in (
            (
                "lower",
                f"{name}.yard",
                0.5 * g["yard"],
                1.0,
                areas[name]["course"][1] if name == "fore" else 0.0,
            ),
            (
                "topmast",
                f"{name}.topsail.yard",
                0.5 * g["topsail_yard"],
                ft(g["yard_h"]),
                areas[name]["topsail"][1],
            ),
            (
                "topgallant",
                f"{name}.topgallant.yard",
                0.5 * g["tg_yard"],
                ft(g["topsail_h"]),
                areas[name]["topgallant"][1],
            ),
        ):
            if name == "main" and level == "lower":
                continue
            area = stuns_area[name][level]
            stuns_canvas = FRIGATE_CANVAS[f"{level} studding"]
            for side in SIDES:
                boom_id = b.spar(
                    f"{name}.{level}.studdingsail_boom.{side}",
                    "studdingsail_boom",
                    on=parent_yard,
                    side=side,
                    length_m=ft(boom_len),
                    height_m=boom_h,
                    rating_kn=design_kn([(area, centre, "studding")], DESIGN_WIND_KN["studding"]),
                    note=(
                        f"{name} {level} studding-sail boom {boom_len:.0f} ft, half the yard it is "
                        f"rigged on (Luce); rated for its sail in "
                        f"{DESIGN_WIND_KN['studding']:.0f} kn.{prov}"
                        if side == SIDES[0]
                        else None
                    ),
                )
                sid = b.sail(
                    f"{name}.{level}.studdingsail.{side}",
                    "studding",
                    boom=boom_id,
                    yard=parent_yard,
                    side=side,
                    area_m2=area,
                    x_m=raked_x(x, FRIGATE_RAKE_DEG[name], centre),
                    centre_height_m=centre,
                    canvas_no=stuns_canvas[0],
                    cloth_rating_kn=cloth(area, stuns_canvas[0]),
                    note=(
                        f"{name} {level} studding sail {area} m2: 0.4 of the yard wide, as deep as "
                        "the sail beside it (judgement)." + canvas_note(stuns_canvas)
                        if side == SIDES[0]
                        else None
                    ),
                )
                size = {"lower": 3.0, "topmast": 2.5, "topgallant": 2.0}[level]
                b.line(f"{sid}.halyard", "halyard", sid, rating=rope_kn(size))
                b.line(f"{sid}.tack", "tack", sid, rating=rope_kn(size))
                b.line(f"{sid}.sheet", "sheet", sid, rating=rope_kn(quarter(size * 0.8)))
                b.line(f"{sid}.downhaul", "downhaul", sid, rating=rope_kn(quarter(size * 0.7)))
                stuns.append(sid)

    # -- storm canvas and the occasional sails (milestone 3b, package 22; spec 3b §6.4) ------
    # Every one starts the voyage in the sail room (`bent: false`): storm canvas is bent before
    # a blow ("Storm-Sails are made of the strongest canvas, and are used ... only in the
    # heaviest weather", Luce 1884 ch. X), the occasional sails when light fair winds call for
    # them. Unbent, they carry no load and catch no wind, and the rating pass leaves them out:
    # the spars are rated for the working canvas they were rated for before.
    storm_canvas = FRIGATE_CANVAS["storm"]
    b.line(
        "mizzen.stay",
        "stay",
        "mizzen.mast",
        rating=rope_kn(10.0),
        note="mizzen stay, from the mizzen mast head to a collar on the main mast twelve feet "
        "above the deck (Steel 1794 vol. I, 'Mizen-stay'); the mizzen storm staysail sets on it. "
        "10 in: judgement, the frigate's lower stays being 1.6 to 1.7 times their shrouds (fore "
        "15 in and main 16 in to 9.5 in) and the mizzen shrouds 6.5 in.",
    )
    # the fore storm staysail on the fore stay (Luce 1884 ch. X: "The storm-staysails set on
    # the respective lower-stays"), cut as Kipping's fore staysail, the sail of No. 1 or 2 set
    # on the forestay: a right-angled triangle whose foot has half the cloths in the head of
    # the fore course and two more, and whose leech is the depth of the fore course
    g = geom["fore"]
    fss_foot = 0.9 * g["yard"] / 2.0 + 4.0  # (head cloths / 2 + 2) cloths of 2 ft
    fss_leech = 0.42 * g["yard"]
    fss_area = round(0.5 * fss_foot * fss_leech * FT * FT)
    fss_clew_x = mast_x["fore"] + 1.0  # the clew just before the fore mast (judgement)
    fss_centre = round(deck_height + (1.5 + fss_leech * FT / 3.0), 1)
    fss = b.sail(
        "fore.storm_staysail",
        "jibheaded",
        stay="fore.stay",
        area_m2=fss_area,
        x_m=round(fss_clew_x + fss_foot * FT / 3.0, 1),
        centre_height_m=fss_centre,
        canvas_no=storm_canvas[0],
        cloth_rating_kn=storm_cloth(fss_area),
        bent=False,
        note=f"fore storm staysail {fss_area} m2 on the fore stay (Luce 1884 ch. X): Kipping's "
        f"fore staysail, a right-angled triangle, foot {fss_foot:.0f} ft (half the fore course's "
        f"head cloths and two), leech {fss_leech:.0f} ft (the course's depth); the clew just "
        "before the fore mast and the foot 5 ft above the deck (judgement); in the sail room."
        + canvas_note(storm_canvas, storm=True),
    )
    # storm staysail halliards "sometimes a luff, and sometimes a gun-tackle purchase"; the
    # sheets "temporary purchases, ... stout luffs hooked ... to the clew-cringles, and
    # brought well aft" (Luce 1884 ch. IX); sizes judgement, as the fore topmast staysail's
    b.line("fore.storm_staysail.halyard", "halyard", fss, rating=rope_kn(3.5, 2))
    b.sided("fore.storm_staysail.sheet", "sheet", fss, rating=rope_kn(3.5, 3))
    b.line("fore.storm_staysail.downhaul", "downhaul", fss, rating=rope_kn(2.75))
    # the mizzen storm staysail on the mizzen stay: its tack at the main mast collar, its head
    # 0.6 of the way up the stay, its clew under the head seven feet above the deck ("the foot
    # drops within 6 or 7 feet of the quarter-deck", Steel 1794 vol. I, 'Mizen staysail');
    # 0.6: judgement for a storm sail smaller than the working mizzen staysail
    gm = geom["mizzen"]
    run_ft = (mast_x["main"] - mast_x["mizzen"]) / FT
    rise_ft = gm["above"] - gm["head"] - 12.0
    head_x, head_z = -0.6 * run_ft, 12.0 + 0.6 * rise_ft
    mss_area = round(0.5 * abs(head_x * (7.0 - 12.0) - (head_z - 12.0) * head_x) * FT * FT)
    mss = b.sail(
        "mizzen.storm_staysail",
        "jibheaded",
        stay="mizzen.stay",
        area_m2=mss_area,
        x_m=round(mast_x["main"] + (2.0 * head_x / 3.0) * FT, 1),
        centre_height_m=round(deck_height + (12.0 + head_z + 7.0) / 3.0 * FT, 1),
        canvas_no=storm_canvas[0],
        cloth_rating_kn=storm_cloth(mss_area),
        bent=False,
        note=f"mizzen storm staysail {mss_area} m2 on the mizzen stay (Luce 1884 ch. X; the "
        "Trenton's allowance has one, Luce p. 171): tack at the main mast collar, head 0.6 up "
        "the stay, clew 7 ft above the deck (Steel's mizzen staysail; 0.6 judgement); in the "
        "sail room." + canvas_note(storm_canvas, storm=True),
    )
    b.line("mizzen.storm_staysail.halyard", "halyard", mss, rating=rope_kn(3.0, 2))
    b.sided("mizzen.storm_staysail.sheet", "sheet", mss, rating=rope_kn(3.0, 3))
    b.line("mizzen.storm_staysail.downhaul", "downhaul", mss, rating=rope_kn(2.5))
    # the storm mizzen: "a triangular sail set abaft the mizzen-mast on a vertical 'stay',
    # hooked under the after trestle-tree, and set up on deck" (Luce 1884 ch. X), "a
    # substitute for the spanker" (ch. XXVII); Steel 1794 vol. I, 'Storm mizen': triangular,
    # bent "to a horse, abaft and parallel to the mizen-mast. The foot is extended towards the
    # taffarel by a sheet". Spec 3b §6.4 drew it as a gaff sail; the sources that name it make
    # it jib-headed, so it is one here, and it is bent in place of the spanker.
    b.line(
        "storm_mizzen.stay",
        "stay",
        "mizzen.mast",
        rating=rope_kn(5.0),
        note="the storm mizzen's vertical stay under the mizzen's after trestle-tree (Luce 1884 "
        "ch. X); 5 in: judgement, as the jib stay.",
    )
    sm_luff = 0.8 * (gm["above"] - gm["head"] - 4.0)  # judgement: 0.8 of the stay's run
    sm_foot = 0.45 * boom_ft  # judgement: "towards the taffarel", 0.45 of the spanker boom
    sm_area = round(0.5 * sm_luff * sm_foot * FT * FT)
    sm = b.sail(
        "storm_mizzen",
        "jibheaded",
        stay="storm_mizzen.stay",
        area_m2=sm_area,
        x_m=round(mast_x["mizzen"] - sm_foot / 3.0 * FT, 1),
        centre_height_m=round(deck_height + (4.0 + sm_luff / 3.0) * FT, 1),
        canvas_no=storm_canvas[0],
        cloth_rating_kn=storm_cloth(sm_area),
        bent=False,
        in_place_of="mizzen.spanker",
        note=f"storm mizzen {sm_area} m2, triangular (Luce 1884 ch. X; Steel 1794 'Storm "
        f"mizen'): luff {sm_luff:.0f} ft on its vertical stay (0.8 of the mast head's height "
        f"above the tack, judgement), foot {sm_foot:.0f} ft towards the taffrail (judgement); "
        "bent in place of the spanker; in the sail room." + canvas_note(storm_canvas, storm=True),
    )
    b.line("storm_mizzen.halyard", "halyard", sm, rating=rope_kn(3.0, 2))
    b.line("storm_mizzen.sheet", "sheet", sm, rating=rope_kn(3.5, 3), parts=3)
    b.line("storm_mizzen.downhaul", "downhaul", sm, rating=rope_kn(2.5))
    storm = [fss, mss, sm]

    # the ringtail, abaft the spanker (Luce 1884 ch. XXIII, 'Other Sails': "a ring-tail, which
    # sets abaft the spanker"): the kind that "sets like a topmast studding sail, outside of the
    # after-leech of the main-trysail; it has a sliding gunter-boom, called the ringtail boom,
    # which runs out on the main-trysail boom" (Kipping 1847, 'Ringtail Sails', a brig's). Its
    # head on a short yard hoisted to the gaff end, its foot hauled out on the ringtail boom
    # run out on the driver boom. Depth: the spanker's after leech (hoist and the gaff's rise
    # at its 40 degree peak); breadth: Kipping's brig's, 5 cloths in the head and 7 in the
    # foot. Falconer's little-mast ringtail on the stern (1780) is for a driver without a boom
    # and is not built.
    rt_depth = 41.0 + 0.9 * gaff_ft * math.sin(math.radians(40.0))
    rt_head, rt_foot = 10.0, 14.0  # 5 and 7 cloths of 2 ft
    rt_area = round((rt_head + rt_foot) / 2.0 * rt_depth * FT * FT)
    rt_boom_ft = rt_foot * 4.0 / 3.0  # judgement: the foot and a third bearing on the boom
    rt_centre = round(deck_height + 2.4 + 0.45 * rt_depth * FT, 1)
    rt_boom = b.spar(
        "ringtail_boom",
        "studdingsail_boom",
        on="mizzen.boom",
        length_m=ft(rt_boom_ft),
        height_m=2.4,
        rating_kn=design_kn([(rt_area, rt_centre, "studding")], DESIGN_WIND_KN["studding"]),
        note=f"ringtail boom {rt_boom_ft:.0f} ft, run out on the driver boom (Kipping's sliding "
        "gunter-boom; Steel 1794 vol. I, 'Ringtail-boom': 'lashed occasionally to the outer end "
        "of the main-sail-boom'): the ringtail's foot and a third that bears on the boom "
        f"(judgement); rated for its sail in {DESIGN_WIND_KN['studding']:.0f} kn, as a "
        f"studding sail boom.{prov}",
    )
    rt_canvas = FRIGATE_CANVAS["ringtail"]
    rt = b.sail(
        "ringtail",
        "studding",
        boom=rt_boom,
        area_m2=rt_area,
        x_m=round(
            raked_x(-16.0, FRIGATE_RAKE_DEG["mizzen"], rt_centre)
            - (0.9 * boom_ft + rt_foot / 2.0) * FT,
            1,
        ),
        centre_height_m=rt_centre,
        canvas_no=rt_canvas[0],
        cloth_rating_kn=cloth(rt_area, rt_canvas[0]),
        bent=False,
        note=f"ringtail {rt_area} m2 (Kipping, Luce 1884): {rt_depth:.0f} ft deep, the depth "
        "of the spanker's after leech it borders (as Falconer's schooner's), 5 cloths in the "
        "head and 7 in the foot (Kipping's brig's); a studding-class sail with no side, "
        "lying in the spanker's plane; in the sail room." + canvas_note(rt_canvas),
    )
    # halyard to the gaff end, tack (the outhaul on the ringtail boom) and sheet; sizes as the
    # topmast studding sails' (judgement)
    b.line("ringtail.halyard", "halyard", rt, rating=rope_kn(2.5))
    b.line("ringtail.tack", "tack", rt, rating=rope_kn(2.5))
    b.line("ringtail.sheet", "sheet", rt, rating=rope_kn(2.0))
    occasional = [rt]
    # a save-all under each lower studding sail boom (Luce 1884 ch. XXIII, 'Other Sails': "a
    # save-all, under the lower studding-sail boom ... never met with in the service now",
    # that is, carried earlier): a water sail for a ship ("Some ships have a water-sail,
    # similar to a sloop's", Steel 1794 vol. I). Judgement for its size, there being no
    # source: its head along 0.6 of the boom, as deep as the boom is high above the water less
    # half a metre.
    lower_boom_ft = 0.5 * geom["fore"]["yard"]
    sa_depth = deck_height + 1.0 - 0.5  # the swinging boom 1 m above the deck (above)
    sa_area = round(0.6 * lower_boom_ft * FT * sa_depth)
    sa_centre = round(0.5 + sa_depth / 2.0, 1)
    sa_canvas = FRIGATE_CANVAS["save-all"]
    save_alls = []
    for side in SIDES:
        sa = b.sail(
            f"fore.save_all.{side}",
            "studding",
            boom=f"fore.lower.studdingsail_boom.{side}",
            yard="fore.yard",
            side=side,
            area_m2=sa_area,
            x_m=round(mast_x["fore"], 1),
            centre_height_m=sa_centre,
            canvas_no=sa_canvas[0],
            cloth_rating_kn=cloth(sa_area, sa_canvas[0]),
            bent=False,
            note=(
                f"save-all {sa_area} m2 under the fore lower studding sail boom (Luce 1884): "
                "head along 0.6 of the boom, down to half a metre off the water (judgement); "
                "in the sail room." + canvas_note(sa_canvas)
                if side == SIDES[0]
                else None
            ),
        )
        # sizes as the topgallant studding sails' (judgement: the save-all is the lighter sail)
        b.line(f"{sa}.halyard", "halyard", sa, rating=rope_kn(2.0))
        b.line(f"{sa}.tack", "tack", sa, rating=rope_kn(2.0))
        b.line(f"{sa}.sheet", "sheet", sa, rating=rope_kn(1.75))
        save_alls.append(sa)
    occasional += save_alls

    # groups
    b.group("courses", sails_by_level["course"])
    b.group("topsails", sails_by_level["topsail"])
    b.group("topgallants", sails_by_level["topgallant"])
    b.group("royals", sails_by_level["royal"])
    b.group("headsails", headsails)
    b.group("jibs", headsails[1:])
    b.group("staysails", headsails[:1] + between)
    # Steel's staysails between the masts as one group, so the sail line and an order can
    # name them where the fore topmast staysail is set with plain sail (package 57)
    b.group("staysails between the masts", between)
    b.group("studdingsails", stuns)
    b.group("square sails", sum(sails_by_level.values(), []))
    b.group("fore-and-aft sails", headsails + between + [spanker])
    # the light staysails: the middle staysail and the topgallant staysails, of No. 6 to 8,
    # with the main topmast staysail as before; the main and mizen staysails, of No. 2, are
    # not light canvas (package 57)
    light_staysails = [s for s in between if s not in ("main.staysail", "mizzen.staysail")]
    b.group("light sails", sails_by_level["royal"] + [headsails[2]] + light_staysails + stuns)
    # lying to (package 57): Steel 1794 vol. II, 'Lying-to under the main staysail' and 'the
    # preferable way is under the fore staysail, the main staysail, and mizen staysail'; the
    # fore and mizen storm staysails stand for his fore and mizen in a gale, as M6 left them
    b.group("lying-to staysails", ["main.staysail"])
    b.group(
        "plain sail",
        sails_by_level["course"]
        + sails_by_level["topsail"]
        + sails_by_level["topgallant"]
        + headsails[:2]
        + [spanker],
    )
    b.group("all sail", sum(sails_by_level.values(), []) + headsails + between + [spanker] + stuns)
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
    # aliases: what an officer of 1795 would say (Falconer 1780; Lever 1827)
    b.alias("spanker", "mizzen.spanker")
    b.alias("driver", "mizzen.spanker")
    b.alias("mizzen", "mizzen.spanker")
    b.alias("foresail", "fore.course")
    b.alias("mainsail", "main.course")
    b.alias("fore yard", "fore.yard")
    b.alias("main yard", "main.yard")
    b.alias("crossjack yard", "mizzen.crossjack.yard")
    b.alias("cro'jack yard", "mizzen.crossjack.yard")
    b.alias("crossjack", "mizzen.crossjack.yard")
    b.alias("spanker boom", "mizzen.boom")
    b.alias("driver boom", "mizzen.boom")
    b.alias("spanker gaff", "mizzen.gaff")
    b.alias("fore topmast staysail", "fore.topmast_staysail")
    b.alias("main topmast staysail", "main.topmast_staysail")
    # package 57: the middle staysail (`middle_staysail`) is its own sail now (Steel), not
    # another name for the main topmast staysail
    b.alias("main staysail", "main.staysail")
    b.alias("main topgallant staysail", "main.topgallant_staysail")
    for word in ("mizzen", "mizen"):
        b.alias(f"{word} staysail", "mizzen.staysail")
        b.alias(f"{word} topmast staysail", "mizzen.topmast_staysail")
        b.alias(f"{word} topgallant staysail", "mizzen.topgallant_staysail")
    b.alias("stuns'ls", "studdingsails")
    b.alias("studding sails", "studdingsails")
    b.alias("kites", "studdingsails")
    b.alias("head sails", "headsails")
    b.alias("topgallant sails", "topgallants")
    b.alias("upper yards", "topgallant yards")
    # milestone 3b: the sail room's own canvas (spec 3b §6.4). "storm canvas" and "occasional
    # sails" are the groups freesail.ship.parts reads for the muster's sail-room line; none of
    # these sails is in "all sail" or "light sails", which name the working canvas.
    b.group("storm canvas", storm)
    b.group("storm staysails", storm[:2])
    b.group("occasional sails", occasional)
    b.group("save-alls", save_alls)
    # the ids read as a sailor says them (storm mizzen, ringtail); the save-alls by their
    # side, "the starboard save-all", as a sided family like the courses' sheets
    b.alias("save-all", "save-alls")
    for name in ("fore", "main"):
        for level in ("lower", "topmast", "topgallant"):
            if name == "main" and level == "lower":
                continue
            b.group(
                f"{name} {level} studdingsails", [f"{name}.{level}.studdingsail.{s}" for s in SIDES]
            )
    # WP15: the courses' lines by their period names (Falconer: main-sheet,
    # main-tack, main-bowline; fore-sheet, fore-tack, fore-bowline). Each is
    # a group of the two sided lines, and the singular alias to it is read
    # by the orders parser as a sided family ("haul the weather main sheet").
    for name in ("fore", "main"):
        for cls in ("sheet", "tack", "bowline"):
            b.group(f"{name} {cls}s", [f"{name}.course.{cls}.{s}" for s in SIDES])
            b.alias(f"{name} {cls}", f"{name} {cls}s")
    # milestone 3b: the topsails' bowlines, and Luce's name for them (1884 ch. IX,
    # 'Top-Bowlines'), read as sided families like the courses' above
    for name in ("fore", "main", "mizzen"):
        b.group(f"{name} topsail bowlines", [f"{name}.topsail.bowline.{s}" for s in SIDES])
        b.alias(f"{name} top bowline", f"{name} topsail bowlines")
    ground_tackle_for(b, 933.0, beam_ft, draught_ft)
    frigate_crew(b)
    frigate_armament(b, deck_height)
    hold_for(b, 933.0, True, "a ship of war's hold is her own stores and ballast: judgement")
    b.pumps(
        PUMPS_NOTE,
        pump_entries(
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
        BOATS_NOTE,
        boat_entries(
            gundeck_ft,
            True,
            [
                (
                    "launch",
                    "launch",
                    "the launch",
                    1.0,
                    "The launch, 2.6 root(143 ft) = 31 ft; the stream anchor is sent in her "
                    "(Steel 1794 vol. I: 'sent in the long-boat'), and the water comes off in "
                    "her in gang casks (Luce 1866, 'Boats').",
                    "data/ships/boat-launch-31.yaml",
                ),
                (
                    "barge",
                    "barge",
                    "the barge",
                    1.03,
                    "The captain's barge, a little longer than the launch and narrower "
                    "(Falconer, BARGE: 'longer, slighter, and narrower').",
                ),
                (
                    "pinnace",
                    "pinnace",
                    "the pinnace",
                    0.9,
                    "The pinnace, eight oars (Falconer, PINNACE).",
                ),
                (
                    "first_cutter",
                    "cutter",
                    "the first cutter",
                    0.9,
                    "The first cutter, 0.9 of the launch (Luce's rule).",
                    "data/ships/boat-cutter-28.yaml",
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
                    JOLLY_BOAT_OF_LAUNCH,
                    "The jolly boat, the small boat at the stern davits (judgement in the size).",
                ),
            ],
        ),
    )
    b.dump(
        os.path.join(out_dir, "frigate-36.yaml"),
        "# Reference ship: Amazon, a 36-gun 18-pounder frigate of the Amazon class (Rule, 1795).\n"
        "# Generated by tools/gen_ships.py; edit that script and rerun, do not edit this file.\n"
        "# Hull: Winfield's published dimensions of the class. Spars: Luce 1866 ch. VII rules,\n"
        "# checked against Falconer 1780 art. YARD. Rope: Luce 1866 ch. IV (breaking strain of\n"
        "# tarred hemp, one third for the working load) and ch. VIII (sizes by class). Brace\n"
        "# limits: Luce 1866 ch. XXIV (d'Ulloa, Fincham). Spar ratings are provisional, set for\n"
        "# truth 9 with the M1 sail curves; see the script's docstring. Canvas: Steel 1794 vol. I\n"
        "# with Kipping and Luce 1884 p. 171; cloth ratings from the number by Luce App. E.\n"
        "# Units: metres, m2, kg, kN. Comments mark each judgement.\n",
    )


# spanker geometry, shared by the mast rating and the sail (feet: boom 44, gaff 35, hoist 41)
# Mast rake, degrees aft of the vertical, as the file's rake_deg. A judgement for a
# 1790s frigate: the fore nearly upright, the main a little more, the mizzen most
# (Lever 1808 "Masts"; Steel's establishments give the rake in inches per foot, not
# in the references). Sail centres are carried aft with the mast as they rise.
FRIGATE_RAKE_DEG = {"fore": 1.5, "main": 2.5, "mizzen": 4.5}
FRIGATE_DECK_M = 1.8  # deck_height_m of the frigate's hull block, for the rake offset


def raked_x(mast_x_m, rake_deg, centre_height_m, deck_m=FRIGATE_DECK_M):
    """x of a sail centre hung on a raked mast: carried aft by tan(rake) per metre of hoist."""
    return round(
        mast_x_m - math.tan(math.radians(rake_deg)) * max(centre_height_m - deck_m, 0.0), 1
    )


SPANKER_AREA = 167
SPANKER_CENTRE = 9.8


# ---------------------------------------------------------------------------
# The schooner: a Baltimore-built topsail schooner of about 1804
# ---------------------------------------------------------------------------


def schooner(out_dir="data/ships", armed=False):
    """The topsail schooner Speedwell (`topsail-schooner.yaml`), or with `armed` the
    letter of marque of her draught (`privateer-schooner.yaml`, PROVISIONAL ahead of
    package 75): the same hull, rig and company, with a fit of guns and a quarter bill."""
    # Design winds: as the frigate's, plus the gaff-topsail pole at 22 (that sail comes in
    # early)
    dw = dict(DESIGN_WIND_KN, gaff_topsail=22.0)
    # -- hull: Kemp's Lynx of 1812 (Chapelle, The Baltimore Clipper, 1930) ------------------
    # Chapelle pp. 82-83 and fig. 17, the Admiralty draught of H.M. schooner Musquidobit,
    # late the Baltimore privateer Lynx (Thomas Kemp, Fell's Point, 1812), taken off at
    # Portsmouth 10 May 1816: length on deck 94 ft 7 in; keel for tonnage 73 ft 1 1/4 in;
    # breadth extreme 24 ft 0 in, moulded 23 ft 8 in; depth of hold 10 ft 3 in; 223 91/94
    # tons; deadrise about 30 degrees, a great deal of drag to the keel, very raking stem
    # and sternpost, both masts raking alike, seven ports a side. "The only thing lacking
    # ... is the spar dimensions, which unfortunately are not to be found" (p. 82), so the
    # rig is reconstructed the way Chapelle does it for Grecian (p. 94): by Fincham's
    # masting rules as he gives them (pp. 159-162), checked against the spar tables he
    # prints (Sea Lark, an American schooner of 1812, pp. 41-42; H.M. schooner Spider,
    # pp. 165-167) and Marestier's measured Baltimore schooners of 1820 (pp. 113-115:
    # mainmast 3.08 to 3.23 x the beam). Speedwell is built to Lynx's draught; the file
    # keeps her name and her date of about 1804, the yard and the type being the same.
    lod_ft = 94.6
    keel_ft = 73.1
    beam_ft = 24.0
    depth_ft = 10.25
    lwl_ft = 85.0  # judgement: between the 73 ft keel and the 94.6 ft deck, with those ends
    # Draught: Marestier's Mammoth (p. 113) drew 0.35 of her beam forward and 0.56 aft; on
    # 24 ft of beam that is 8 ft 5 in and 13 ft 4 in, mean 10 ft 11 in.
    draught_ft = round((0.348 + 0.557) / 2.0 * beam_ft, 1)
    lwl, beam, draught = ft(lwl_ft), ft(beam_ft), ft(draught_ft)
    # Displacement: Cb 0.33 on LWL x beam x mean draught (30 degrees of deadrise, slack
    # bilges). Spider, 183 tons burthen and "not at all extreme", weighed 204 tons 3 cwt
    # fully equipped (p. 166); a sharper hull of 224 tons burthen comes to about 210 t.
    displacement = round(lwl * beam * draught * 0.33 * 1025.0, -3)
    deck_height = 0.9  # Spider's port sills 3 ft 5 in above water, sills 10 in above deck
    rake = 0.2  # both masts rake alike (p. 82); Fincham: main 1 in 6 to 1 in 4 (p. 160)

    b = Builder(
        "Speedwell",
        "topsail-schooner",
        "A Baltimore-built topsail schooner of about 1804, built to the draught of Kemp's "
        "Lynx of 1812 (Chapelle 1930, pp. 82-83): 94 ft 7 in on deck, 24 ft beam, 224 tons, "
        "masts raking 1 in 5, a fore topsail and topgallant over a loose-footed foresail. "
        "Rig by Fincham's rules as Chapelle gives them (pp. 159-162) checked against his "
        "spar tables; rope by Luce ch. IV; see tools/gen_ships.py for every rule.",
        {
            "length_waterline_m": lwl,
            "beam_m": beam,
            "draught_m": draught,
            "displacement_kg": displacement,
            "gm_m": 1.0,
            "clr_x_m": 0.5,
            "lateral_area_m2": round(lwl * draught * 0.78, -1),
            "hull_speed_kn": 11.5,
            "deck_height_m": deck_height,
            "rudder": {"area_m2": 2.0, "max_angle_deg": 35, "rate_deg_s": 4.0, "span_m": 3.4},
        },
        {
            "length_waterline_m": f"{lwl_ft:.0f} ft: judgement between Lynx's {keel_ft:.0f} ft "
            f"keel and {lod_ft:.1f} ft deck (Chapelle p. 82), her stem and post raking hard.",
            "beam_m": "24 ft 0 in extreme, 23 ft 8 in moulded (Chapelle p. 82).",
            "draught_m": f"{draught_ft:.1f} ft mean: Marestier's draughts of 0.35 and 0.56 of "
            "the beam forward and aft (Chapelle p. 113) on Lynx's beam.",
            "displacement_kg": "LWL x beam x draught x Cb 0.33 x 1025, about 210 t; Spider "
            f"(183 tons burthen) weighed 204 t equipped (p. 166); depth of hold {depth_ft} ft.",
            "gm_m": "3 ft 3 in: judgement; tender (Chapelle p. 104: schooners capsized when "
            "overpressed with sail), heavily ballasted.",
            "clr_x_m": "Rankine (Chapelle p. 159): the middle of the sail base lies 0.05 to "
            "0.0625 of the base (1.6 to 1.7 x LWL) ahead of the centre of lateral area, so "
            "the geometric centre is about 1.4 m abaft this plan's centre of effort (+1.0 m "
            "under plain sail). The engine wants its centre of pressure further forward, as "
            "on the frigate: at +0.5 m she is balanced close-hauled in 15 kn and carries 5 "
            "deg of weather helm on a beam reach; at -0.4 m (the M1 value) she carried 4 deg "
            "of lee helm close-hauled. Judgement; package 10 checks truths 2 and 6.",
            "lateral_area_m2": "LWL x draught x 0.78 for a profile that is deep aft only.",
            "hull_speed_kn": "The type's recorded best is 11 to 12 knots; the derived "
            "1.34 sqrt(LWL ft) = 12.4 is too generous. Package 10 may tune within 11 to 12.",
            "deck_height_m": "Port sills 3 ft 5 in above the water and 10 in above the deck "
            "(Spider's specification, Chapelle pp. 166-167): a low-sided vessel.",
            "rudder": "A deep narrow blade, about 11 ft by 2 ft (span_m its depth, 11 ft; "
            "package 32e).",
        },
    )

    # -- spars in feet by Fincham's rules for two-masted schooners (Chapelle pp. 160-161),
    # taken at the upper end of each range because "the resultant rig is perhaps a little
    # small for American vessels" (p. 159); the American checks are noted beside each.
    main_hounded = 2.8 * beam_ft  # mainmast heel to hounds = 2.6 to 2.8 x extreme breadth
    topmast_hounded = 1.0 * beam_ft  # topmasts hounded = 0.83 to 1.0 x breadth
    pole = 0.5 * topmast_hounded  # pole heads of topmasts = 0.5 x hounded length
    main_head = 0.35 * topmast_hounded  # heads of lower masts = 0.3 to 0.4 x topmasts
    main_total = main_hounded + main_head  # 75.6 ft: Marestier 3.08 to 3.23 x beam = 74-78
    step_to_deck = depth_ft + 0.75  # steps on the keelson
    main_above = main_total - step_to_deck
    fore_hounded = 0.95 * main_hounded  # foremast = 0.9 to 0.97 x mainmast
    fore_head = main_head
    fore_total = fore_hounded + fore_head
    fore_above = fore_total - step_to_deck
    # the fore topmast heels at the trestletrees, so its hounds stand this much above the
    # lower cap; the topgallant sets on its pole (the fore.topgallant_mast part)
    fore_top = topmast_hounded + pole
    fore_top_hoist = topmast_hounded - fore_head
    fore_tg = pole
    fore_tg_hoist = pole
    main_top = topmast_hounded + pole  # a pole topmast for the gaff topsail
    main_top_hoist = main_top - main_head
    fore_yard = 0.57 * lwl_ft  # fore yard = 0.48 to 0.57 x LWL (Sea Lark carried 0.69)
    topsail_yard = 0.75 * fore_yard  # fore-topsail yard = 0.7 to 0.75 x fore yard
    tg_yard = 0.48 * fore_yard  # fore-topgallant yard = 0.42 to 0.48 x fore yard
    # (the fore yard is a bare spread yard for the topsail's foot; it is not a part here)
    main_boom = 0.70 * lwl_ft  # main boom = 0.66 to 0.7 x LWL (Sea Lark 0.71)
    main_gaff = 0.48 * main_boom  # main gaff = 0.44 to 0.53 x boom (Sea Lark 28 ft)
    fore_gaff = 0.85 * main_gaff  # fore gaff = 0.73 to 1.0 x main gaff (Sea Lark 24 ft)
    # head: bowsprit outboard 0.12 x LWL, jib-boom 0.4 x LWL, the tack of the jib 0.41 to
    # 0.46 x LWL before the stem; a little more bowsprit for the low American steeve
    bowsprit_out = 0.14 * lwl_ft
    jib_boom_out = 0.28 * lwl_ft
    fore_yard_h = fore_above - fore_head - 2.0
    topsail_h = fore_above + fore_top_hoist - 1.0
    tg_h = fore_above + fore_top_hoist + pole - 1.5
    # stations: foremast 0.28 to 0.34 x LWL before the middle, mainmast 0.05 to 0.11 abaft
    fore_x = round(0.30 * lwl * 1.0, 1)
    main_x = -round(0.10 * lwl, 1)

    def raked(mast_x_m, z_above_deck_ft):
        """x of a point on a raked mast, metres: the rake carries it aft as it rises."""
        return mast_x_m - rake * z_above_deck_ft * FT

    def trapezoid(head_ft, foot_ft, depth_ft):
        return round((head_ft + foot_ft) / 2.0 * depth_ft * FT * FT)

    ts_depth = topsail_h - fore_yard_h  # "depth of fore-topsail = extreme beam, nearly"
    ts_area = trapezoid(0.82 * topsail_yard, 0.9 * fore_yard, ts_depth)
    ts_z = fore_yard_h + 0.5 * ts_depth
    ts_centre = round(deck_height + ts_z * FT, 1)
    tg_depth = tg_h - topsail_h
    tg_area = trapezoid(0.89 * tg_yard, 0.9 * topsail_yard, tg_depth)
    tg_z = topsail_h + 0.5 * tg_depth
    tg_centre = round(deck_height + tg_z * FT, 1)
    # gaff sails (Fincham, p. 160): foot of the mainsail from clew to mast (0.92 of the
    # boom), head 0.5 to 0.6 of the foot; the nock 0.045 of the hounded length below the
    # hounds; gaffs inclined 25 to 30 degrees; foot of the foresail 0.7 to 0.85 of the
    # mainsail's, its head 0.75 to 1.0 of the mainsail's
    gaff_rise = 0.51  # tan 27 degrees
    main_foot = 0.92 * main_boom
    main_head_ft = 0.92 * main_gaff
    main_nock = main_above - main_head - 0.045 * main_hounded
    main_hoist = main_nock - 5.0
    main_area = round(
        (
            (main_foot + main_head_ft) / 2.0 * main_hoist
            + 0.5 * main_head_ft * gaff_rise * main_head_ft
        )
        * FT
        * FT
    )
    main_z = 5.0 + 0.45 * main_hoist
    main_centre = round(deck_height + main_z * FT, 1)
    fore_foot = 0.8 * main_foot  # loose-footed, sheeting abaft the main mast
    fore_head_ft = 0.92 * fore_gaff
    fore_nock = fore_above - fore_head - 0.045 * fore_hounded
    fore_hoist = fore_nock - 6.0
    fore_area = round(
        (
            (fore_foot + fore_head_ft) / 2.0 * fore_hoist
            + 0.5 * fore_head_ft * gaff_rise * fore_head_ft
        )
        * FT
        * FT
    )
    fore_z = 6.0 + 0.45 * fore_hoist
    fore_centre = round(deck_height + fore_z * FT, 1)
    # gaff topsail: luff up the pole topmast, foot along the gaff (Spider's, p. 167, was
    # 498 sq ft on a 27 ft gaff)
    gt_area = round(0.6 * main_head_ft * main_top_hoist * FT * FT)
    gt_z = main_above + 0.4 * main_top_hoist
    gt_centre = round(deck_height + gt_z * FT, 1)
    # headsails (Fincham: foot of the jib 0.32 to 0.35 x LWL; Spider's staysail was the
    # larger sail of the two, 690 to 592 sq ft): a triangle with a little round
    stem_x = lwl / 2.0
    jib_tack_x = stem_x + ft(bowsprit_out) + ft(jib_boom_out)
    jib_foot = 0.35 * lwl_ft
    jib_area = round(0.5 * jib_foot * (fore_above - fore_head - 8.0) * 1.15 * FT * FT)
    stay_foot = 0.4 * lwl_ft
    stay_area = round(0.5 * stay_foot * (fore_above - fore_head - 8.0) * 1.1 * FT * FT)
    flying_area = round(0.5 * jib_area)
    stuns_area = round(0.4 * topsail_yard * ts_depth * FT * FT)
    prov = " Provisional (truth 9), see gen_ships.py."

    fore = b.spar(
        "fore.mast",
        "mast",
        x_m=fore_x,
        rake_deg=round(math.degrees(math.atan(rake)), 1),
        height_m=ft(fore_above),
        rating_kn=design_kn(
            [
                (fore_area, fore_centre, "gaff"),
                (ts_area, ts_centre, "square"),
                (tg_area, tg_centre, "square"),
            ],
            dw["lower"],
        ),
        note=f"fore mast {fore_total:.0f} ft heel to head (Fincham: 0.95 of the main), "
        f"{fore_above:.0f} ft above the deck, raking 1 in 5 like the main (Chapelle p. 82); "
        f"stationed 0.30 of LWL before the middle (Fincham).{prov}",
    )
    fore_topmast = b.spar(
        "fore.topmast",
        "topmast",
        steps_on=fore,
        height_m=ft(fore_top_hoist),
        rating_kn=design_kn(
            [(ts_area, ts_centre, "square"), (tg_area, tg_centre, "square")],
            dw["topsail"],
        ),
        note=f"fore topmast {fore_top:.0f} ft with its pole (Fincham: hounded the beam, "
        f"pole half of that), hounds {fore_top_hoist:.0f} ft above the lower cap.{prov}",
    )
    fore_tgm = b.spar(
        "fore.topgallant_mast",
        "topgallant_mast",
        steps_on=fore_topmast,
        height_m=ft(fore_tg_hoist),
        rating_kn=design_kn([(tg_area, tg_centre, "square")], dw["topgallant"]),
        note=f"fore topgallant 'mast': the {fore_tg:.0f} ft pole of the topmast, on which the "
        f"topgallant sets (Fincham).{prov}",
    )
    main = b.spar(
        "main.mast",
        "mast",
        x_m=main_x,
        rake_deg=round(math.degrees(math.atan(rake)), 1),
        height_m=ft(main_above),
        rating_kn=design_kn(
            [(main_area, main_centre, "gaff"), (gt_area, gt_centre, "jibheaded")],
            dw["lower"],
        ),
        note=f"main mast {main_total:.0f} ft heel to head: hounded 2.8 x the beam plus a head "
        "0.35 of the topmast (Fincham, Chapelle p. 161; Marestier's schooners 3.08 to 3.23 x "
        f"the beam, p. 114), {main_above:.0f} ft above the deck, raking 1 in 5; stationed "
        f"0.10 of LWL abaft the middle.{prov}",
    )
    main_topmast = b.spar(
        "main.topmast",
        "topmast",
        steps_on=main,
        height_m=ft(main_top_hoist),
        rating_kn=design_kn([(gt_area, gt_centre, "jibheaded")], dw["gaff_topsail"]),
        note=f"main topmast {main_top:.0f} ft, hounded the beam with a pole half as long "
        f"(Fincham), a pole for the gaff topsail, which comes in early.{prov}",
    )
    ty = b.spar(
        "fore.topsail.yard",
        "yard",
        on=fore_topmast,
        length_m=ft(topsail_yard),
        height_m=ft(topsail_h),
        brace_limit_deg=58,
        rating_kn=design_kn(
            [(ts_area, ts_centre, "square"), (tg_area, tg_centre, "square")],
            dw["topsail"],
        ),
        note=f"fore topsail yard {topsail_yard:.0f} ft, 0.75 of a {fore_yard:.0f} ft fore yard "
        "that is 0.57 of LWL (Fincham; Sea Lark's fore yard was 0.69, Chapelle p. 42); braces "
        "58 deg from square as before (Chapelle is silent on bracing; Fincham 1843 art. 102's "
        f"figures are for ships' lower yards; judgement, spec 3b §2.1).{prov}",
    )
    ts = b.sail(
        "fore.topsail",
        "square",
        yard=ty,
        area_m2=ts_area,
        reef_bands=2,
        x_m=round(raked(fore_x, ts_z), 1),
        centre_height_m=ts_centre,
        canvas_no=SCHOONER_CANVAS["fore.topsail"][0],
        cloth_rating_kn=cloth(ts_area, SCHOONER_CANVAS["fore.topsail"][0]),
        note=f"fore topsail {ts_area} m2 between its yard and the fore yardarms, "
        f"{ts_depth:.0f} ft deep ('the extreme beam, nearly', Fincham); x carried aft by the rake."
        + canvas_note(SCHOONER_CANVAS["fore.topsail"]),
    )
    square_sail_lines(
        b,
        ts,
        ty,
        {
            "halyard": 3.5,
            "sheet": 3.0,
            "brace": 2.5,
            "lift": 2.5,
            "clewline": 2.5,
            "buntline": 2.0,
            "reef_tackle": 2.5,
            "bowline": 2.5,  # the clewline's size (judgement; spec 3b §4)
        },
        hoisting=True,
        reef=True,
        bowline=True,
    )
    tgy = b.spar(
        "fore.topgallant.yard",
        "yard",
        on=fore_tgm,
        length_m=ft(tg_yard),
        height_m=ft(tg_h),
        brace_limit_deg=60,
        rating_kn=design_kn([(tg_area, tg_centre, "square")], dw["topgallant"]),
        note=f"fore topgallant yard {tg_yard:.0f} ft, 0.48 of the fore yard (Fincham); braces "
        f"60 deg from square, two more than the topsail yard (judgement, as before).{prov}",
    )
    tgs = b.sail(
        "fore.topgallant",
        "square",
        yard=tgy,
        area_m2=tg_area,
        x_m=round(raked(fore_x, tg_z), 1),
        centre_height_m=tg_centre,
        canvas_no=SCHOONER_CANVAS["fore.topgallant"][0],
        cloth_rating_kn=cloth(tg_area, SCHOONER_CANVAS["fore.topgallant"][0]),
        note=f"fore topgallant {tg_area} m2; light canvas."
        + canvas_note(SCHOONER_CANVAS["fore.topgallant"]),
    )
    square_sail_lines(
        b,
        tgs,
        tgy,
        {
            "halyard": 2.0,
            "sheet": 2.0,
            "brace": 1.75,
            "lift": 1.75,
            "clewline": 1.75,
            "buntline": 1.5,
        },
        hoisting=True,
    )
    # gaff sails
    fgaff = b.spar(
        "fore.gaff",
        "gaff",
        on=fore,
        length_m=ft(fore_gaff),
        height_m=ft(fore_nock),
        rating_kn=design_kn([(fore_area, fore_centre, "gaff")], dw["gaff"]),
        note=f"fore gaff {fore_gaff:.0f} ft, 0.85 of the main gaff (Fincham; Sea Lark's 24 ft, "
        "Chapelle p. 42); the foresail is loose-footed and overlaps the main (Luce 1884 "
        "ch. XXXIV: a boom foresail sets worse on a wind).",
    )
    foresail = b.sail(
        "fore.sail",
        "gaff",
        mast=fore,
        gaff=fgaff,
        area_m2=fore_area,
        reef_bands=2,
        x_m=round(raked(fore_x, fore_z) - 0.4 * fore_foot * FT, 1),
        centre_height_m=fore_centre,
        canvas_no=SCHOONER_CANVAS["fore.sail"][0],
        cloth_rating_kn=cloth(fore_area, SCHOONER_CANVAS["fore.sail"][0]),
        note=f"foresail {fore_area} m2: foot {fore_foot:.0f} ft (0.8 of the mainsail's, "
        f"Fincham) sheeting abaft the main mast, head on the gaff, hoist {fore_hoist:.0f} ft, "
        "gaff peaked 27 degrees; centre 0.4 of the foot abaft the raked mast."
        + canvas_note(SCHOONER_CANVAS["fore.sail"]),
    )
    b.line("fore.gaff.throat_halyard", "throat_halyard", fgaff, rating=rope_kn(3.0, 4))
    b.line("fore.gaff.peak_halyard", "peak_halyard", fgaff, rating=rope_kn(3.0, 4))
    b.sided("fore.sail.sheet", "sheet", foresail, rating=rope_kn(3.5))
    b.line("fore.sail.tack", "tack", foresail, rating=rope_kn(3.5))
    mgaff = b.spar(
        "main.gaff",
        "gaff",
        on=main,
        length_m=ft(main_gaff),
        height_m=ft(main_nock),
        rating_kn=design_kn([(main_area, main_centre, "gaff")], dw["gaff"]),
        note=f"main gaff {main_gaff:.0f} ft, 0.48 of the boom (Fincham; Sea Lark's 28 ft), "
        "its nock 0.045 of the hounded mast below the hounds.",
    )
    mboom = b.spar(
        "main.boom",
        "boom",
        on=main,
        length_m=ft(main_boom),
        height_m=1.5,
        horse_m=round(0.5 * beam, 1),
        rating_kn=design_kn([(main_area, main_centre, "gaff")], dw["gaff"]),
        note=f"main boom {main_boom:.0f} ft, 0.70 of LWL (Fincham; Sea Lark's 0.71, Chapelle "
        "p. 42), well over the taffrail; horse_m " + HORSE_NOTE,
    )
    mainsail = b.sail(
        "main.sail",
        "gaff",
        mast=main,
        gaff=mgaff,
        boom=mboom,
        area_m2=main_area,
        reef_bands=3,
        x_m=round(raked(main_x, main_z) - 0.4 * main_foot * FT, 1),
        centre_height_m=main_centre,
        canvas_no=SCHOONER_CANVAS["main.sail"][0],
        cloth_rating_kn=cloth(main_area, SCHOONER_CANVAS["main.sail"][0]),
        note=f"mainsail {main_area} m2: foot {main_foot:.0f} ft from clew to mast, head 0.92 of "
        f"the gaff, hoist {main_hoist:.0f} ft to a nock {main_nock:.0f} ft above the deck "
        "(Fincham: 2 to 2.4 x the beam above water), gaff peaked 27 degrees; Spider's, on a "
        "23 ft beam, was 1982 sq ft (Chapelle p. 167)." + canvas_note(SCHOONER_CANVAS["main.sail"]),
    )
    b.line("main.gaff.throat_halyard", "throat_halyard", mgaff, rating=rope_kn(3.5, 4))
    b.line("main.gaff.peak_halyard", "peak_halyard", mgaff, rating=rope_kn(3.0, 5))
    b.line(
        "main.sail.sheet",
        "sheet",
        mainsail,
        rating=rope_kn(4.0, 3),
        parts=3,
        note="4 in, a threefold purchase.",
    )
    b.line("main.sail.outhaul", "outhaul", mainsail, rating=rope_kn(2.5))
    b.sided("main.gaff.vang", "vang", mgaff, rating=rope_kn(2.5))
    gt = b.sail(
        "main.gaff_topsail",
        "jibheaded",
        mast=main_topmast,
        area_m2=gt_area,
        x_m=round(raked(main_x, gt_z) - 0.3 * main_head_ft * FT, 1),
        centre_height_m=gt_centre,
        canvas_no=SCHOONER_CANVAS["main.gaff_topsail"][0],
        cloth_rating_kn=cloth(gt_area, SCHOONER_CANVAS["main.gaff_topsail"][0]),
        note=f"main gaff topsail {gt_area} m2, luff on the topmast, foot along the gaff "
        "(Luce 1884 ch. XXXIV)." + canvas_note(SCHOONER_CANVAS["main.gaff_topsail"]),
    )
    b.line("main.gaff_topsail.halyard", "halyard", gt, rating=rope_kn(2.5))
    b.line("main.gaff_topsail.sheet", "sheet", gt, rating=rope_kn(2.5))
    b.line("main.gaff_topsail.tack", "tack", gt, rating=rope_kn(2.5))
    # head
    # the staysail tacks at the stem head, the jib and the jib topsail (flying jib) at the
    # jib-boom end (Fincham: tack of the jib 0.41 to 0.46 x LWL before the stem)
    heads = [
        ("fore.staysail", "fore.stay", stay_area, round(stem_x - 0.35 * stay_foot * FT, 1), 6.0),
        ("jib", "jib.stay", jib_area, round(jib_tack_x - 0.35 * jib_foot * FT, 1), 7.5),
        (
            "flying_jib",
            "flying_jib.stay",
            flying_area,
            round(jib_tack_x - 0.25 * jib_foot * FT, 1),
            10.0,
        ),
    ]
    head_loads = {sid: (area, h, "jibheaded") for sid, _, area, _, h in heads}
    bowsprit = b.spar(
        "bowsprit",
        "bowsprit",
        x_m=round(stem_x, 1),
        length_m=ft(bowsprit_out),
        height_m=3.0,
        rating_kn=design_kn(list(head_loads.values()), dw["lower"]),
        note=f"bowsprit {bowsprit_out:.0f} ft outboard, 0.14 of LWL (Fincham gives 0.12 for the "
        "Royal Navy's; Grecian's 'was probably rather short', Chapelle p. 93), steeved low.",
    )
    jib_boom = b.spar(
        "jib_boom",
        "jib_boom",
        on=bowsprit,
        length_m=ft(jib_boom_out),
        height_m=4.0,
        rating_kn=design_kn([head_loads["flying_jib"]], dw["jib_boom"]),
        note=f"jib-boom {jib_boom_out:.0f} ft outboard: the jib tacks "
        f"{bowsprit_out + jib_boom_out:.0f} ft before the stem, 0.42 of LWL (Fincham 0.41 to "
        f"0.46).{prov}",
    )
    b.line(
        "fore.stay",
        "stay",
        fore,
        rating=rope_kn(8.0),
        note="8 in, to the stem head; the fore staysail sets on it.",
    )
    b.line(
        "fore.topmast.stay",
        "stay",
        fore_topmast,
        rating=rope_kn(4.5),
        note="4.5 in, fore topmast head to the jib-boom end.",
    )
    b.line(
        "jib.stay",
        "stay",
        fore,
        rating=rope_kn(5.0),
        note="5 in, fore mast head to the bowsprit cap: the jib sets on it (Luce 1884 ch. XXXIV, "
        "'the jib of a schooner is that sail whose tack is nearest the bowsprit cap').",
    )
    b.line(
        "flying_jib.stay",
        "stay",
        fore_topmast,
        rating=rope_kn(3.0),
        note="3 in, fore topmast head to the jib-boom end, for the flying jib.",
    )
    b.line("main.topmast.stay", "stay", main_topmast, rating=rope_kn(4.0))
    b.line("bobstay", "stay", bowsprit, rating=rope_kn(7.0))
    b.line("martingale", "stay", jib_boom, rating=rope_kn(3.5))
    b.sided(
        "fore.shrouds", "shroud", fore, rating=rope_kn(6.5, 4), note="4 shrouds of 6.5 in a side."
    )
    b.sided("main.shrouds", "shroud", main, rating=rope_kn(6.5, 4))
    b.sided("fore.topmast.backstay", "backstay", fore_topmast, rating=rope_kn(3.5, 2))
    b.sided("main.topmast.backstay", "backstay", main_topmast, rating=rope_kn(3.5, 2))
    head_sails = []
    for sid, stay, area, x, h in heads:
        s = b.sail(
            sid,
            "jibheaded",
            stay=stay,
            area_m2=area,
            x_m=x,
            centre_height_m=h,
            canvas_no=SCHOONER_CANVAS[sid][0],
            cloth_rating_kn=cloth(area, SCHOONER_CANVAS[sid][0]),
            note=f"{sid.replace('_', ' ').replace('.', ' ')} {area} m2 (judgement from the "
            "stay's run)." + canvas_note(SCHOONER_CANVAS[sid]),
        )
        size = {"fore.staysail": 2.5, "jib": 3.0, "flying_jib": 2.0}[sid]
        b.line(f"{sid}.halyard", "halyard", s, rating=rope_kn(size, 2))
        b.sided(f"{sid}.sheet", "sheet", s, rating=rope_kn(size))
        b.line(f"{sid}.downhaul", "downhaul", s, rating=rope_kn(quarter(size * 0.8)))
        head_sails.append(s)
    # a fore topmast studding sail each side; the boom rigs on the fore yard, a bare spread
    # yard the type crossed for the topsail sheets, which the file does not model (the M1
    # contract counts two yards on her), so the boom hangs from the topsail yard at the
    # fore yard's height
    stuns = []
    for side in SIDES:
        boom = b.spar(
            f"fore.topmast.studdingsail_boom.{side}",
            "studdingsail_boom",
            on=ty,
            side=side,
            length_m=ft(0.5 * topsail_yard),
            height_m=ft(fore_yard_h),
            rating_kn=design_kn([(stuns_area, ts_centre, "studding")], dw["studding"]),
            note=(
                "fore topmast studding-sail boom, half the topsail yard, at the fore yard's "
                f"height; rated for its sail in {dw['studding']:.0f} kn.{prov}"
                if side == SIDES[0]
                else None
            ),
        )
        s = b.sail(
            f"fore.topmast.studdingsail.{side}",
            "studding",
            boom=boom,
            yard=ty,
            side=side,
            area_m2=stuns_area,
            x_m=fore_x,
            centre_height_m=ts_centre,
            canvas_no=SCHOONER_CANVAS["topmast studding"][0],
            cloth_rating_kn=cloth(stuns_area, SCHOONER_CANVAS["topmast studding"][0]),
            note=(
                f"fore topmast studding sail {stuns_area} m2 (judgement)."
                + canvas_note(SCHOONER_CANVAS["topmast studding"])
                if side == SIDES[0]
                else None
            ),
        )
        for cls, size in (("halyard", 2.0), ("tack", 2.0), ("sheet", 1.75), ("downhaul", 1.5)):
            b.line(f"{s}.{cls}", cls, s, rating=rope_kn(size))
        stuns.append(s)

    # -- storm canvas and the occasional sails (milestone 3b, package 22; spec 3b §6.4) ------
    # As in the frigate, each starts in the sail room (`bent: false`), carries no load and
    # catches no wind until bent, and is left out of the rating pass. The storm canvas is the
    # owner's judgement (spec 3b §6.4) given its shape by Steel's sloops and cutters.
    #
    # The storm trysail: Steel 1794 vol. I, 'Sloop's trysail, or storm mainsail': "occasionally
    # used for the mainsail in stormy weather. The fore-leech is from three-fourths of the
    # depth to the same depth as the mainsail, and the after-leech is one-eighth deeper ...
    # The head has two-fifths of the number of cloths that are in the head of the mainsail,
    # and the [foot] is three times the breadth of the head. ... the head is bent to a gaff,
    # and the foot is extended by the boom"; "three or four reef-bands". Bent to the main gaff
    # and boom in place of the mainsail. (Luce 1884 ch. XXXIV makes a schooner's storm trysail
    # "similar in shape to the storm mizzen", triangular; Steel's is of the schooner's time.)
    storm_canvas = SCHOONER_CANVAS["storm trysail"]
    st_head = 0.4 * main_head_ft
    st_foot = 3.0 * st_head
    st_luff = 0.85 * main_hoist  # judgement: between Steel's three-fourths and the whole
    st_leech = st_luff * 9.0 / 8.0
    st_area = round((st_head + st_foot) / 2.0 * (st_luff + st_leech) / 2.0 * FT * FT)
    st_z = 5.0 + 0.45 * st_luff
    st = b.sail(
        "storm_trysail",
        "gaff",
        mast=main,
        gaff=mgaff,
        boom=mboom,
        area_m2=st_area,
        reef_bands=3,
        x_m=round(raked(main_x, st_z) - 0.4 * st_foot * FT, 1),
        centre_height_m=round(deck_height + st_z * FT, 1),
        canvas_no=storm_canvas[0],
        cloth_rating_kn=storm_cloth(st_area),
        bent=False,
        in_place_of="main.sail",
        note=f"storm trysail {st_area} m2 (Steel's sloop's storm mainsail): head {st_head:.0f} ft "
        f"(two-fifths of the mainsail's), foot {st_foot:.0f} ft (three times the head), luff "
        f"{st_luff:.0f} ft (0.85 of the mainsail's, judgement within Steel's three-fourths to "
        "the whole), after leech an eighth deeper; three reef bands (Steel: three or four); "
        "bent to the main gaff and boom in place of the mainsail; in the sail room."
        + canvas_note(storm_canvas, storm=True),
    )
    b.line("storm_trysail.sheet", "sheet", st, rating=rope_kn(4.0, 3), parts=3)
    b.line("storm_trysail.outhaul", "outhaul", st, rating=rope_kn(2.5))
    # the storm jib: Steel 1794 vol. I, the sloop's jibs: "two-thirds of the size of the first
    # jib, and is used in stormy weather, in lieu of a larger one"; hanked to the jib stay in
    # place of the jib, its centre as much lower as its size is smaller (judgement)
    jib_x, jib_h = heads[1][3], heads[1][4]
    sj_area = round(2.0 / 3.0 * jib_area)
    sj_canvas = SCHOONER_CANVAS["storm jib"]
    sj = b.sail(
        "storm_jib",
        "jibheaded",
        stay="jib.stay",
        area_m2=sj_area,
        x_m=jib_x,
        centre_height_m=round(jib_h * math.sqrt(2.0 / 3.0), 1),
        canvas_no=sj_canvas[0],
        cloth_rating_kn=storm_cloth(sj_area),
        bent=False,
        in_place_of="jib",
        note=f"storm jib {sj_area} m2, two-thirds of the jib (Steel 1794); hanked to the jib stay "
        "in place of the jib; in the sail room." + canvas_note(sj_canvas, storm=True),
    )
    b.line("storm_jib.halyard", "halyard", sj, rating=rope_kn(3.0, 2))
    b.sided("storm_jib.sheet", "sheet", sj, rating=rope_kn(3.0))
    b.line("storm_jib.downhaul", "downhaul", sj, rating=rope_kn(2.5))
    storm = [st, sj]

    # the ringtail on the main boom: "as in all sloops, brigs, and schooners ... of the same
    # depth with that part of the main-sail upon which it borders" (Falconer 1780,
    # RING-TAIL); Steel 1794 vol. I, 'Sloop's ringtail sail': "occasionally hoisted abaft the
    # after-leech of the main sail ... The head is bent to a small yard at the outer end of the
    # gaff; and the foot is spread on the boom, which is prolonged by [the ringtail boom]
    # lashed to the outer end"; Kipping 1847, 'Ringtail Sails': a sliding gunter ringtail boom
    # run out on the main boom, 4 or 5 cloths in the head and 6 or 7 in the foot
    rt_depth = main_hoist + main_head_ft * gaff_rise  # the mainsail's after leech
    rt_head, rt_foot = 10.0, 14.0  # 5 and 7 cloths of 2 ft (Kipping's broader)
    rt_area = round((rt_head + rt_foot) / 2.0 * rt_depth * FT * FT)
    rt_z = 1.5 / FT + 0.45 * rt_depth
    rt_centre = round(deck_height + rt_z * FT, 1)
    rt_boom_ft = rt_foot * 4.0 / 3.0  # judgement: the foot and a third bearing on the boom
    rt_boom = b.spar(
        "ringtail_boom",
        "studdingsail_boom",
        on=mboom,
        length_m=ft(rt_boom_ft),
        height_m=1.5,
        rating_kn=design_kn([(rt_area, rt_centre, "studding")], dw["studding"]),
        note=f"ringtail boom {rt_boom_ft:.0f} ft, run out on the main boom (Kipping; Steel: "
        "'lashed occasionally to the outer end of the main-sail-boom'): the ringtail's foot and "
        "a third that bears on the boom (judgement); rated for its sail in "
        f"{dw['studding']:.0f} kn, as a studding sail boom.{prov}",
    )
    rt_canvas = SCHOONER_CANVAS["ringtail"]
    rt = b.sail(
        "ringtail",
        "studding",
        boom=rt_boom,
        area_m2=rt_area,
        x_m=round(raked(main_x, rt_z) - (main_foot + rt_foot / 2.0) * FT, 1),
        centre_height_m=rt_centre,
        canvas_no=rt_canvas[0],
        cloth_rating_kn=cloth(rt_area, rt_canvas[0]),
        bent=False,
        note=f"ringtail {rt_area} m2: {rt_depth:.0f} ft deep, the mainsail's after leech "
        "(Falconer), 5 cloths in the head and 7 in the foot (Kipping); a studding-class sail "
        "with no side, lying in the mainsail's plane; in the sail room." + canvas_note(rt_canvas),
    )
    b.line("ringtail.halyard", "halyard", rt, rating=rope_kn(2.0))
    b.line("ringtail.tack", "tack", rt, rating=rope_kn(2.0))
    b.line("ringtail.sheet", "sheet", rt, rating=rope_kn(1.75))
    # the water sail under the main boom: Steel 1794 vol. I, 'Sloop's water-sail': "cut square
    # on the head ... occasionally spread under the boom of the main-sail in fair winds ... The
    # depth of this sail is from one-half to three-fourths of the length of the boom, and it is
    # 4 or 5 cloths wide". A boom at head height cannot have half its length of sail hanging
    # under it, so the OCR's "depth" is read as the head's run along the boom, 0.6 of it, and
    # the sail as deep as the boom stands above the water less half a metre (judgement).
    ws_depth = deck_height + 1.5 - 0.5
    ws_area = round(0.6 * main_boom * FT * ws_depth)
    ws_canvas = SCHOONER_CANVAS["water sail"]
    ws = b.sail(
        "water_sail",
        "studding",
        boom=mboom,
        area_m2=ws_area,
        x_m=round(main_x - 0.5 * main_boom * FT, 1),
        centre_height_m=round(0.5 + ws_depth / 2.0, 1),
        canvas_no=ws_canvas[0],
        cloth_rating_kn=cloth(ws_area, ws_canvas[0]),
        bent=False,
        note=f"water sail {ws_area} m2 under the main boom (Steel's sloop's): head along 0.6 of "
        "the boom, down to half a metre off the water (judgement, see the script); a "
        "studding-class sail laced under the boom, with no side; in the sail room."
        + canvas_note(ws_canvas),
    )
    # sizes judgement: Steel gives the water sail's bolt-rope 1.5 in
    b.line("water_sail.halyard", "halyard", ws, rating=rope_kn(1.75))
    b.line("water_sail.tack", "tack", ws, rating=rope_kn(1.75))
    b.line("water_sail.sheet", "sheet", ws, rating=rope_kn(1.5))
    occasional = [rt, ws]

    b.group("topsails", [ts])
    b.group("topgallants", [tgs])
    b.group("square sails", [ts, tgs])
    b.group("headsails", head_sails)
    b.group("jibs", head_sails[1:])
    b.group("gaff sails", [foresail, mainsail])
    b.group("fore-and-aft sails", head_sails + [foresail, mainsail, gt])
    b.group("studdingsails", stuns)
    b.group("fore topmast studdingsails", stuns)
    b.group("light sails", [gt, tgs, head_sails[2]] + stuns)
    b.group("plain sail", [foresail, mainsail, ts, tgs, head_sails[0], head_sails[1]])
    b.group("all sail", [foresail, mainsail, gt, ts, tgs] + head_sails + stuns)
    b.group("yards", [ty, tgy])
    b.group("fore yards", [ty, tgy])
    b.group("topsail yards", [ty])
    b.group("topgallant yards", [tgy])
    b.alias("foresail", "fore.sail")
    b.alias("the fore", "fore.sail")
    b.alias("mainsail", "main.sail")
    b.alias("the main", "main.sail")
    b.alias("gaff topsail", "main.gaff_topsail")
    b.alias("main gaff topsail", "main.gaff_topsail")
    b.alias("fore staysail", "fore.staysail")
    b.alias("stuns'ls", "studdingsails")
    b.alias("studding sails", "studdingsails")
    b.alias("kites", "studdingsails")
    b.alias("head sails", "headsails")
    b.alias("topgallant sails", "topgallants")
    # milestone 3b: the sail room's own canvas (spec 3b §6.4), as in the frigate
    b.group("storm canvas", storm)
    b.group("occasional sails", occasional)
    # the ids read as a sailor says them: storm trysail, storm jib, ringtail, water sail
    # milestone 3b: her one square sail's bowlines; with no course on the fore, "the fore
    # bowline" is the fore topsail's, and Luce's "top-bowline" (1884 ch. IX) likewise
    b.group("fore bowlines", ["fore.topsail.bowline.starboard", "fore.topsail.bowline.larboard"])
    b.alias("fore bowline", "fore bowlines")
    b.alias("fore top bowline", "fore bowlines")
    ground_tackle_for(b, 224.0, beam_ft, draught_ft)
    schooner_crew(b)
    if armed:
        schooner_armament(b)
    hold_for(b, 224.0, False, "a sharp Baltimore hull stows about half her tonnage: judgement")
    b.pumps(PUMPS_NOTE, pump_entries(0, 2, ["the starboard pump", "the larboard pump"]))
    b.boats(
        BOATS_NOTE,
        boat_entries(
            lod_ft,
            False,
            [
                (
                    "long_boat",
                    "long-boat",
                    "the long-boat",
                    1.0,
                    "The long-boat, a fifth under Luce's rule for a ship of war (judgement for "
                    "a privateer).",
                ),
                ("yawl", "yawl", "the yawl", 0.8, "The yawl, four oars (Falconer, YAWL)."),
            ],
        ),
    )
    if armed:
        privateer_schooner(b, out_dir)
        return
    b.dump(
        os.path.join(out_dir, "topsail-schooner.yaml"),
        "# Reference ship: Speedwell, a Baltimore-built topsail schooner of about 1804, to the\n"
        "# draught of Kemp's Lynx of 1812 (H.M. schooner Musquidobit; Chapelle, The Baltimore\n"
        "# Clipper, 1930, pp. 82-83, fig. 17). Generated by tools/gen_ships.py; edit that script\n"
        "# and rerun, do not edit this file. Rig: Fincham's masting rules as Chapelle gives them\n"
        "# (pp. 159-162), checked against his spar tables (Sea Lark pp. 41-42, Spider pp.\n"
        "# 165-167) and Marestier's schooners (pp. 113-115). Rope: Luce 1866 ch. IV. Rig details:\n"
        "# Luce 1884 ch. XXXIV. Spar ratings are provisional, set for truth 9 with the M1 sail\n"
        "# curves; see the script. Canvas: Steel 1794 vol. I (sloops and cutters); cloth ratings\n"
        "# from the number by Luce App. E. Units: metres, m2, kg, kN. Comments mark judgements.\n",
    )


# ---------------------------------------------------------------------------
# The hold and the boats (package 35, spec M5 §22, §23): one rule for every ship
# ---------------------------------------------------------------------------

# The room for a cargo, as a part of the burthen (Falconer 1780, HOLD: "the ballast,
# provisions, and stores of a ship of war, and the principal part of the cargo in a
# merchantman"). A ship of war's hold is full of her own water, provisions, cable tiers
# and ballast, and what is left stows a prize's goods or stores taken in: judgement, a
# tenth of the burthen. A trader stows about half her tonnage of measurement in a sharp
# hull (Chapelle 1930 remarks the Baltimore type's small capacity; the fraction is
# judgement) and a revenue cutter, deep and full, the same half less her own stores.
HOLD_OF_BURTHEN_SHIP_OF_WAR = 0.1
HOLD_OF_BURTHEN_TRADER = 0.5
# The boats, by Luce 1866's rules of size ('Boats', 'Rules for Size of Boats for
# Ships-of-War': "For the length of first launch, multiply the square root of the length
# of the ship by 2.6; breadth, 1/4 of the length. First and second cutters of ships of the
# line, and first cutters of sloops to be .9 of launch. Third and fourth cutters ... and
# second cutters of sloops to be .9 of first cutter. Quarter, waist or stern boats to be of
# the same dimensions as the ... second cutter of sloops, but lighter built"), and the
# boats a ship carried from Steel 1794 vol. II (the chapters 'ships' long-boats or
# launches', 'ships' pinnaces and rowing barges', 'ships' cutters or yawls') and Falconer
# 1780, BOAT ("the long-boat ... the barges are next in order ... pinnaces ... cutters ...
# yawls"), PINNACE ("usually rowed with eight oars") and YAWL ("rowed by four or six
# oars"). The allowance by the ship's size is judgement on those texts: a frigate a
# launch, a barge, a pinnace, two cutters and a jolly boat; a brig a launch, a cutter and
# a jolly boat; a schooner a long-boat and a yawl; a cutter a boat and a punt. A merchant
# or revenue vessel's boats are smaller than Luce's rule for a ship of war gives, by a
# fifth (judgement). The oars by the length, a thwart to every three feet (judgement on
# Falconer's eight and six); the crew the oars and a coxswain; the tons a boat carries by
# Luce's weight rule for the boat herself (the breadth squared times the length, in
# pounds, times 2.5 for a launch, 1.9 a first cutter, 1.4 a second, 1.0 a quarter boat),
# a boat carrying about her own weight (judgement).
LAUNCH_LENGTH_FACTOR = 2.6
BOAT_BREADTH_OF_LENGTH = 0.25
CUTTER_OF_LAUNCH = 0.9
JOLLY_BOAT_OF_LAUNCH = 0.65  # judgement: a jolly boat of 18 to 20 feet to a 30-foot launch
SMALL_VESSEL_BOAT_FACTOR = 0.8
BOAT_FEET_PER_OAR = 3.0
BOAT_WEIGHT_FACTORS = {"launch": 2.5, "long-boat": 2.5, "barge": 1.9, "pinnace": 1.9, "cutter": 1.4}
BOAT_WEIGHT_DEFAULT = 1.0
LB_PER_TON = 2240.0


def hold_for(b, burthen, ship_of_war, note):
    fraction = HOLD_OF_BURTHEN_SHIP_OF_WAR if ship_of_war else HOLD_OF_BURTHEN_TRADER
    tons = round(burthen * fraction)
    b.hold(
        tons,
        f"The hold (package 35, spec M5 §23): room for {tons} tons of cargo beyond her own "
        f"stores, {fraction:g} of the {burthen:g} tons burthen ({note}; Falconer 1780, HOLD); "
        "see tools/gen_ships.py.",
    )


def boat_entries(length_ft, ship_of_war, allowance):
    """The boats' lines from Luce's rule: `allowance` is a list of (id, kind, name, of_launch)."""
    launch = LAUNCH_LENGTH_FACTOR * math.sqrt(length_ft)
    if not ship_of_war:
        launch *= SMALL_VESSEL_BOAT_FACTOR
    out = []
    for entry in allowance:
        bid, kind, name, of_launch, text = entry[:5]
        file = entry[5] if len(entry) > 5 else None  # package 82: her own file, where she has one
        length = round(launch * of_launch)
        breadth = length * BOAT_BREADTH_OF_LENGTH
        oars = max(2, int(length / BOAT_FEET_PER_OAR) // 2 * 2)
        weight_lb = breadth * breadth * length * BOAT_WEIGHT_FACTORS.get(kind, BOAT_WEIGHT_DEFAULT)
        tons = round(max(0.1, weight_lb / LB_PER_TON), 1)
        row = (bid, kind, name, float(length), oars, oars + 1, tons, text)
        out.append(row + (file,) if file else row)
    return out


# The pumps (package 73, spec M7 §13; docs/design/Design-WaterAndHealth.md). The chain pump
# of Cole and Bentinck, in the King's ships from the 1770s and standard by 1805: in the
# Seaford's trial "the chain pump, wrought by four men, discharged a ton of water in 43
# seconds and a half" (Falconer 1780, PUMP, the article's close), which is 83 tons an hour
# at four men fresh, taken as 80; the common pump, the brake or elm-tree pump, two men at
# the brake, a fraction of it (judgement from its bore: a seven-inch bore, a twelve-inch
# stroke, thirty strokes a minute is some 13 tons an hour; 15 taken). The King's ships
# carried two chain pumps at the main mast and two elm-tree pumps (Lavery, Arming and
# Fitting, the pumps; from memory); a brig-sloop one chain pump and two hand pumps
# (judgement); the small vessels hand pumps alone (Steel 1794 on the pumps of small craft;
# judgement for the count). The rates are the pump's with its hands fresh; the men's
# numbers, their rating and their fatigue, and the roll, make the lift the keeper gives
# (`freesail/world/water.py`).
CHAIN_PUMP_T_PER_H = 80.0
CHAIN_PUMP_HANDS = 4
HAND_PUMP_T_PER_H = 15.0
HAND_PUMP_HANDS = 2
# package 73 (spec M7 §11): the quarter bill's small-arms men and boarders
SMALL_ARMS_NOTE = (
    "The small-arms men beyond the marines: seamen with the muskets of the stand of arms, "
    "firing at will within musket shot when the arms are served out (Luce 1884 ch. XX: the "
    "station bill's small-arms men; the count judgement against the company)."
)
BOARDERS_NOTE = (
    "The boarders told off from the guns' crews (Luce 1884 ch. XX: 'boarders and sail "
    "trimmers are told off from the guns' crews'; the first and second boarders of the "
    "station bill), beside the marines who board with the bayonet; the count judgement at "
    "about a quarter of the seamen."
)
PUMPS_NOTE = (
    "The pumps (package 73, spec M7 §13): the chain pump of Cole and Bentinck, a ton in 43 "
    "seconds and a half with four men (Falconer 1780, PUMP), and the common brake pump with "
    "two; the counts by the ship's class (Lavery, Arming and Fitting; Steel 1794); see "
    "tools/gen_ships.py."
)
SHOT_PLUGS_NOTE = (
    "The carpenter's shot plugs (package 73, spec M7 §14): tapered plugs of soft wood with "
    "oakum and tallow, kept ready in action (the Regulations and Instructions 1806, the "
    "Carpenter; Falconer 1780, PLUG: 'shot-plugs ... to stop holes made by cannon shot'); "
    "the count by her class, judgement."
)


def pump_entries(chain, hand, names):
    """The pumps' lines: so many chain pumps and so many hand pumps, the names from
    `names` in order."""
    out = []
    i = 0
    for n in range(chain):
        out.append(
            (
                f"pump.chain.{n + 1}",
                "chain",
                names[i],
                CHAIN_PUMP_T_PER_H,
                CHAIN_PUMP_HANDS,
                "A chain pump at the main mast (Falconer 1780, PUMP): four men, 80 tons an "
                "hour fresh."
                if n == 0
                else None,
            )
        )
        i += 1
    for n in range(hand):
        out.append(
            (
                f"pump.hand.{n + 1}",
                "hand",
                names[i],
                HAND_PUMP_T_PER_H,
                HAND_PUMP_HANDS,
                "A brake pump (the common or elm-tree pump): two men, 15 tons an hour fresh "
                "(judgement)."
                if n == 0
                else None,
            )
        )
        i += 1
    return out


BOATS_NOTE = (
    "The boats (package 35, spec M5 §23): their lengths by Luce 1866's rule ('Boats', 'Rules "
    "for Size of Boats for Ships-of-War': the launch 2.6 times the square root of the ship's "
    "length, the cutters 0.9 of it), the allowance after Steel 1794 vol. II and Falconer 1780 "
    "(BOAT, PINNACE, YAWL), the oars a thwart to three feet, the tons by Luce's weight rule "
    "for the boat herself; see tools/gen_ships.py."
)


# ---------------------------------------------------------------------------
# The ship's company (spec M3 §2.3)
# ---------------------------------------------------------------------------
#
# Stations follow Luce 1884 ch. XX (Watch, Quarter and Station Bills): forecastlemen are
# "able seamen ... together with a few ordinary seamen"; the tops "seamen, ordinary seamen,
# active, able-bodied men"; the afterguard "comparatively few seamen ... the balance being
# landsmen"; the marines "divided between the two watches, and their work on deck is
# generally the same as that of the afterguard"; idlers "stand no night watches". The
# standing officers are Falconer's (1780, ORDINARY: "the gunner, boatswain, carpenter,
# deputy-purser and cook"; CARPENTER). The stations and the posts together make the
# complement; the loader checks it.

# The wardroom files (spec M6 §2; package 40): `data/people/<ship>.yaml` is the source of
# each ship's station holders, with their ranks, places and outlines. The posts of the
# muster and the people drawn from a station at muster are read from it here, so that the
# ship file's `crew.posts` and `crew.people` and the people the game names agree
# (tests/test_people.py proves it against the files as written).
PEOPLE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "people"
)


def wardroom(stem):
    """The posts (in the file's order) and the people drawn at muster of a ship's wardroom
    file, the latter as (role, station, rating, messenger, note) entries for `Builder.people`."""
    with open(os.path.join(PEOPLE_DIR, stem + ".yaml"), encoding="utf-8") as f:
        doc = yaml.safe_load(f) or {}
    entries = doc.get("wardroom") or []
    posts = tuple(str(e["role"]) for e in entries if e.get("post"))
    drawn = [
        (
            str(e["role"]),
            str(e["drawn"]["station"]),
            str(e["drawn"]["rating"]) if e["drawn"].get("rating") else None,
            bool(e.get("messenger")),
            " ".join(str(e.get("note") or "").split()) or None,
        )
        for e in entries
        if e.get("drawn")
    ]
    return posts, drawn


FRIGATE_POSTS, FRIGATE_DRAWN = wardroom("frigate-36")
SCHOONER_POSTS, SCHOONER_DRAWN = wardroom("topsail-schooner")
CUTTER_POSTS, CUTTER_DRAWN = wardroom("cutter")
BRIG_POSTS, BRIG_DRAWN = wardroom("brig")
MERCHANT_BRIG_POSTS, MERCHANT_BRIG_DRAWN = wardroom("merchant-brig")


def ration_entries(whose):
    """The crew's `ration:` block (package 54, spec M7b §19): the table of
    data/crew/ration.yaml the ship is served from and the water a man a day. `whose` says
    why the Navy's table serves her, after its source."""
    return [
        (
            ("ration", "table"),
            "navy",
            "The ration (package 54, spec M7b 19): the Navy's table, the Regulations of 1806 "
            f"(Sect. IX, Chap. I, Art. I), as data/crew/ration.yaml gives it; {whose}.",
        ),
        (
            ("ration", "water_gallons"),
            1,
            "Water drawn a man a day for his drink, his grog and the coppers: a gallon, the "
            "figure her water above is reckoned at (judgement).",
        ),
    ]


# ---------------------------------------------------------------------------
# The armament and the quarter bill (spec M7 §7, §8a; package 70)
# ---------------------------------------------------------------------------
#
# A gun is a part of the graph by its position (freesail/ship/parts.py `Gun`), carried in a
# **fit** the scenario chooses between (`ship: {fit: ...}`), each fit with its magazine. The
# figures below are remembered from Lavery, *The Arming and Fitting of English Ships of War
# 1600-1815* (the Establishments' guns, the carronade's adoption from 1779 and its
# establishment of 1794 to 1795, the allowance of powder and shot), Winfield, *British
# Warships in the Age of Sail 1793-1817* (each class's armament), Douglas, *A Treatise on
# Naval Gunnery* (1820: the exercise, the crews, the ranges), and Falconer 1780 (CANNON,
# SWIVEL); none of these is in docs/references/ as a page, so every figure is FROM MEMORY
# and marked UNVERIFIED where the text says so, as data/nations.yaml marks its dates. A
# figure the sources do not give is a judgement and says so.

# The guns' weights, in hundredweight (112 lb), by kind and the weight of their shot
# (UNVERIFIED, from memory): the long guns of Blomefield's pattern as the 1790s cast them
# (the 18-pounder of 9 ft, 42 cwt; the 12-pounder of 9 ft, 34; the 9-pounder of 7 ft 6 in,
# 26; the 6-pounder of 7 ft, 20; the 4-pounder of 6 ft, 12 1/2; the 3-pounder of 4 ft 6 in,
# 7), the Carron Company's carronades (the 32-pounder, 17 cwt; the 24-pounder, 13; the
# 18-pounder, 10; the 12-pounder, 6), and the half-pounder swivel on its yoke (about half a
# hundredweight: judgement).
LONG_GUN_CWT = {18: 42.0, 12: 34.0, 9: 26.0, 6: 20.0, 4: 12.5, 3: 7.0}
CARRONADE_CWT = {32: 17.0, 24: 13.0, 18: 10.0, 12: 6.0}
SWIVEL_CWT = 0.5

# The crew of a gun by the quarter bill, for the pair of one number (the starboard and the
# larboard gun of a number share a crew, which fights whichever side is engaged and is
# divided when both are: Lavery, the quarter bill; the Regulations, the men quartered at the
# guns): a man to about five hundredweight of a long gun and two for the captain and the
# sponger (Douglas 1820, the exercise: an 18-pounder's crew of eight to ten with the boy;
# the rule a judgement reading of his crews), a carronade's lighter (three and a man to
# every eight hundredweight: a 32-pounder carronade worked by five, a 12-pounder by four;
# judgement after Lavery), a swivel one man, who comes from whoever is spare.


def gun_crew(kind, cwt):
    if kind == "long":
        return 2 + int(round(cwt / 5.0))
    if kind == "carronade":
        return 3 + int(round(cwt / 8.0))
    return 1


# The allowance of shot a gun, by the ship's service: a King's ship's sixty round, with
# grape and double-headed (chain) shot a tenth of it between them (Lavery on the Ordnance's
# allowance of the 1790s, about sixty to seventy rounds a gun for a cruise; the shares
# judgement); a hired cutter's forty (her magazine smaller; judgement); a merchantman's
# twenty round and a little grape for her own defence (judgement); a swivel's forty
# half-pound balls. Cartridges one a round and a tenth over for the blank charges (the
# signal gun, the gun to leeward; judgement).
KINGS_ROUNDS = {"round": 60, "grape": 6, "chain": 6}
HIRED_ROUNDS = {"round": 40, "grape": 6, "chain": 4}
MERCHANT_ROUNDS = {"round": 20, "grape": 4}
SWIVEL_ROUNDS = {"round": 40}
BLANK_SHARE = 0.1

# The port sill above the deck, for a gun's muzzle height above the water upright: about two
# feet on a gun deck (Lavery, the ports; judgement for the figure), the rail's height for a
# swivel the same.
PORT_SILL_M = 0.6


def fit_magazine(guns, rounds_by_kind, exercise_charges=0):
    """A fit's magazine for its guns, each gun with the allowance of its kind
    (`rounds_by_kind`: {"long"|"carronade"|"swivel": {kind: n}}), as a mapping in the
    file's order (practice and resupply, between packages 72 and 73; the build design's
    §1.2): `cartridges`, filled, by the gun's kind and calibre, a round each and a tenth
    over (`BLANK_SHARE`); `charges`, a cartridge's powder by kind and calibre
    (`freesail.ship.parts.charge_lb`, the shares UNVERIFIED until package 75 reads the
    Regulations' Table No. 29); `powder_barrels`, the powder below in barrels of a hundred
    pounds, `RESERVE_SHARE` of the filled powder rounded up; `exercise_charges`, a King's
    fit's allowance for exercise a month (`exercise_allowance`), written only when above
    nought; and `shot` by calibre and kind."""
    from freesail.ship.parts import BARREL_LB, RESERVE_SHARE, charge_lb

    cartridges: dict = {}
    charges: dict = {}
    shot: dict = {}
    for g, _ in guns:
        p, kind = g["pounder"], g["kind"]
        allowance = rounds_by_kind[kind]
        total = sum(allowance.values())
        filled = cartridges.setdefault(kind, {})
        filled[p] = filled.get(p, 0) + int(round(total * (1.0 + BLANK_SHARE)))
        charges.setdefault(kind, {})[p] = charge_lb(kind, p)
        by = shot.setdefault(p, {})
        for k, n in allowance.items():
            by[k] = by.get(k, 0) + n
    filled_lb = sum(n * charges[k][p] for k, ps in cartridges.items() for p, n in ps.items())
    out = {
        "cartridges": cartridges,
        "charges": charges,
        "powder_barrels": math.ceil(RESERVE_SHARE * filled_lb / BARREL_LB),
    }
    if exercise_charges > 0:
        out["exercise_charges"] = exercise_charges
    out["shot"] = shot
    return out


def exercise_allowance(upper_deck_guns, decks=1):
    """The Regulations' allowance for exercise: a charge of powder and a round shot a month
    for a fourth of the upper deck guns in a ship of one deck, a third in ships of two or
    three decks (package 75: `decks`, a two-decker's), the figure for the first six months
    after the guns are received (the Regulations 1806, 1808 printing, the Gunner, Art. XXI,
    OCR l.13122-13144; the game keeps no commissioning date, so the first six months'
    figure: judgement). A King's fit only. A two-decker's note is
    `tools/ships/period.py`'s `TWO_DECKS_EXERCISE_NOTE`."""
    if decks not in (1, 2, 3):
        raise ValueError(f"the Regulations allow for ships of one, two or three decks, not {decks}")
    return upper_deck_guns // (4 if decks == 1 else 3)


def filling_party(guns):
    """The quarter bill's men filling cartridges: one to every four cannon, the swivels
    not cannon (Falconer 1780, QUARTER-GUNNER, l.14283-14289: 'one quarter-gunner being
    allowed to every four cannon'), and one at the least."""
    return max(1, sum(1 for g, _ in guns if g["kind"] != "swivel") // 4)


# The notes above a fit's magazine keys (practice and resupply, between packages 72 and 73;
# docs/design/Build-PracticeAndResupply.md §1.2, §2).
MAGAZINE_NOTES = {
    "cartridges": (
        "The cartridges filled at the fitting out, by the gun's kind and calibre: a round a "
        "gun of the allowance below and a tenth over for the blank charges (judgement); the "
        "gunner fills more from the powder below as they are fired (combat/filling.py)."
    ),
    "charges": (
        "A cartridge's powder in pounds, to the ounce: a long gun a third of its shot's "
        "weight (Falconer 1780, CANNON, quoting Robins, l.4826-4831: a third 'or even less' "
        "would be an advantage; the service charge of 1805 a third from memory, "
        "UNVERIFIED), a carronade a twelfth (from memory, UNVERIFIED), a swivel a half "
        "(Falconer's smaller pieces, l.4827: judgement). Package 75 replaces them from the "
        "Regulations' Table No. 29 (OCR l.27498-27502), whose figures the OCR lost."
    ),
    "powder_barrels": (
        "The powder below in barrels of a hundred pounds (Falconer 1780, the French "
        "glossary, 'Baril de poudre', l.22563-22564; the English barrel's weight "
        "UNVERIFIED), half the filled powder rounded up to the barrel (judgement: the "
        "period kept most of its powder in the barrels)."
    ),
    "exercise_charges": (
        "The Regulations' allowance for exercise a month: a charge and a round shot for a "
        "fourth of the upper deck guns in a ship of one deck, for six months after the guns "
        "are received (the Regulations 1806, 1808 printing, the Gunner, Art. XXI, "
        "l.13122-13144; the Captain's chapter, l.8842-8879, gives a third); the first six "
        "months' figure, the game keeping no commissioning date (judgement)."
    ),
}
FILLING_NOTE = (
    "The quarter gunners and the gunner's crew in the filling room, one to every four cannon "
    "(Falconer 1780, QUARTER-GUNNER, l.14283-14289); the swivels are not cannon (practice "
    "and resupply, between packages 72 and 73)."
)


# Package 75 (docs/design/Build-Ships.md §3.1 item 7, §5.3): each gun helper below takes the
# deck its guns stand on, `deck`, one of `schema.DECK_WORDS`, written last in each gun's
# mapping and left out when None, as every gun of the eight files is; and `round_to`, the step
# its x_m and height_m are rounded to: the tenth of a metre the eight files have, or the
# centimetre of a port's own x and sill from a hull's profile. Rounded as round(v, 1) or
# round(v, 2), never as round(v / step) * step, whose floats (2.4 as 2.4000000000000004) would
# move the files' bytes.
GUN_ROUNDING_PLACES = {0.1: 1, 0.01: 2}


def _gun_places(round_to):
    """The decimal places of a gun helper's `round_to`."""
    if round_to not in GUN_ROUNDING_PLACES:
        raise ValueError(f"a gun's x_m and height_m round to 0.1 or 0.01 m, not {round_to!r}")
    return GUN_ROUNDING_PLACES[round_to]


def _on_deck(g, deck):
    """The gun's mapping with its deck written last, where the caller gives one."""
    if deck is not None:
        g["deck"] = deck
    return g


def broadside_pair(number, kind, pounder, cwt, x_m, height_m, note=None, deck=None, round_to=0.1):
    """The two guns of one number, starboard then larboard, as (mapping, note) entries;
    the note on the starboard gun alone."""
    places = _gun_places(round_to)
    out = []
    for i, side in enumerate(SIDES):
        g = {
            "id": f"gun.{number}.{side}",
            "kind": kind,
            "pounder": pounder,
            "place": "broadside",
            "number": number,
            "side": side,
            "x_m": round(x_m, places),
            "height_m": round(height_m, places),
            "crew": gun_crew(kind, cwt),
            "weight_cwt": cwt,
        }
        out.append((_on_deck(g, deck), note if i == 0 else None))
    return out


def chasers(place, kind, pounder, cwt, x_m, height_m, note=None, deck=None, round_to=0.1):
    """A pair of chase guns at the bow or the stern, one a side."""
    places = _gun_places(round_to)
    out = []
    for i, side in enumerate(SIDES):
        g = {
            "id": f"chaser.{place}.{side}",
            "kind": kind,
            "pounder": pounder,
            "place": place,
            "side": side,
            "x_m": round(x_m, places),
            "height_m": round(height_m, places),
            "crew": gun_crew(kind, cwt),
            "weight_cwt": cwt,
        }
        out.append((_on_deck(g, deck), note if i == 0 else None))
    return out


def pivot_gun(kind, pounder, cwt, x_m, height_m, arc_deg, note=None, deck=None, round_to=0.1):
    """A gun on a pivot amidships (PROVISIONAL, the owner's ask of 2026-10-25): no side, it
    trains to either (`combat/guns.py`) through its own arc, (from, to) degrees off the bow
    over either side (package 86: per gun, each pivot's from its own ship's rig); its own
    crew by the gun's rule."""
    places = _gun_places(round_to)
    g = {
        "id": "pivot",
        "kind": kind,
        "pounder": pounder,
        "place": "pivot",
        "arc_deg": [float(arc_deg[0]), float(arc_deg[1])],
        "x_m": round(x_m, places),
        "height_m": round(height_m, places),
        "crew": gun_crew(kind, cwt),
        "weight_cwt": cwt,
    }
    return [(_on_deck(g, deck), note)]


def swivels(count, xs_m, height_m, note=None, deck=None, round_to=0.1):
    """So many half-pounder swivels on the rail, numbered a side from forward."""
    places = _gun_places(round_to)
    out = []
    n = 0
    for x in xs_m:
        for side in SIDES:
            n += 1
            if n > count:
                break
            g = {
                "id": f"swivel.{(n + 1) // 2}.{side}",
                "kind": "swivel",
                "pounder": 0.5,
                "place": "rail",
                "number": (n + 1) // 2,
                "side": side,
                "x_m": round(x, places),
                "height_m": round(height_m, places),
                "crew": 1,
                "weight_cwt": SWIVEL_CWT,
            }
            out.append((_on_deck(g, deck), note if n == 1 else None))
    return out


def spaced(fore_m, aft_m, n):
    """n positions from `fore_m` to `aft_m` along the hull, forward positive."""
    if n == 1:
        return [(fore_m + aft_m) / 2.0]
    step = (fore_m - aft_m) / (n - 1)
    return [fore_m - i * step for i in range(n)]


QUARTER_BILL_NOTE = (
    "The quarter bill beyond the gun crews (spec M7 8a; package 70; docs/design/"
    "Design-WorkInAction.md): at quarters every man has a station by it, the gun crews the "
    "fit's (each gun's crew above), the sail trimmers here by station (the men who leave the "
    "guns for a brace or a sail: Luce 1884 ch. XX, 'Watch, Quarter and Station Bills'), the "
    "hands at the helm, the powder beyond the idlers, and the fighting book's priority when "
    "sail work wants more hands than the trimmers give; the marines, the carpenter's crew "
    "and the surgeon's mates have their stations by their trades. The counts are judgement "
    "against the stations above."
)
PRIORITY_NOTE = (
    "The fighting book's priority when sail work wants more hands than the trimmers give "
    "(spec M7 8a): 'sail before guns' robs the guns (the disengaged battery first) and the "
    "log says from where; 'guns before sail' makes the sail work wait short-handed. The "
    "player's book and the doctrine may say otherwise."
)


def frigate_armament(b, deck_height):
    """The Amazon class's armament of 1795 as this fit has it, from memory: on the upper deck
    twenty-six 18-pounders; on the quarterdeck eight 32-pounder carronades and two
    9-pounders; on the forecastle two 9-pounders and two 32-pounder carronades; one fit.
    INCORRECT on the quarterdeck, pending correction. Winfield 1793-1817 p. 143 (the owner's
    copy, read 2026-10-25) gives the class's establishment of 16.3.1795 as 26 x 18-pounders;
    QD 8 x 9-pounders + 6 x 32-pounder carronades; Fc 2 x 9-pounders + 2 x 32-pounder
    carronades: 44 pieces where this fit has 40. The upper deck and the forecastle agree.
    Kept as it is by the owner's ruling of 2026-10-25 while the new ships are built
    (docs/dev/TuningNotes.md, "Open, for the lead: the frigate's quarterdeck"). The ports
    along the gun deck spaced about nine feet (Lavery, the ports of an 18-pounder frigate;
    judgement for the figure), the sills about two feet above the deck; the quarterdeck and
    forecastle a deck higher (about seven feet, judgement). The forecastle 9-pounders are
    the bow chasers; the quarterdeck pair a broadside pair."""
    gun_deck = deck_height + PORT_SILL_M
    upper = deck_height + 2.1 + PORT_SILL_M
    guns = []
    xs = spaced(16.5, -16.5, 13)
    for i, x in enumerate(xs, start=1):
        guns += broadside_pair(
            i,
            "long",
            18,
            LONG_GUN_CWT[18],
            x,
            gun_deck,
            (
                "The upper deck's twenty-six long 18-pounders, thirteen a side (Winfield, the "
                "Amazon class's establishment; UNVERIFIED from memory): the 9 ft gun of 42 cwt "
                "(Blomefield's pattern, from memory), the ports about nine feet apart from 54 ft "
                "before midships to 54 ft abaft (judgement), the muzzle about eight feet above "
                "the water upright; a crew of ten to the pair, who fight whichever gun bears "
                "(Douglas 1820, the exercise; the rule in tools/gen_ships.py gun_crew)."
                if i == 1
                else None
            ),
        )
    for j, x in enumerate(spaced(-7.0, -17.5, 4), start=14):
        guns += broadside_pair(
            j,
            "carronade",
            32,
            CARRONADE_CWT[32],
            x,
            upper,
            (
                "The quarterdeck's eight 32-pounder carronades, four a side (from memory; "
                "INCORRECT, pending correction: Winfield 1793-1817 p. 143 gives six, with eight "
                "long 9-pounders; the carronade establishment of 1794 to 1795, Lavery): 17 cwt "
                "each (the Carron Company's, from memory), on the quarterdeck a deck above the "
                "guns; five men to the pair, the marines among them."
                if j == 14
                else None
            ),
        )
    guns += broadside_pair(
        18,
        "carronade",
        32,
        CARRONADE_CWT[32],
        14.0,
        upper,
        "The forecastle's two 32-pounder carronades, one a side (Winfield 1793-1817 p. 143).",
    )
    guns += broadside_pair(
        19,
        "long",
        9,
        LONG_GUN_CWT[9],
        -4.5,
        upper,
        "The quarterdeck's two long 9-pounders, one a side, the foremost quarterdeck ports "
        "(from memory; INCORRECT, pending correction: Winfield 1793-1817 p. 143 gives eight): "
        "the 7 ft 6 in gun of 26 cwt (from memory); seven to the pair.",
    )
    guns += chasers(
        "bow",
        "long",
        9,
        LONG_GUN_CWT[9],
        17.5,
        upper,
        "The forecastle's two long 9-pounders as the bow chasers (Winfield gives the "
        "forecastle its pair; that they served as chase guns is the frigate's practice, "
        "judgement): 26 cwt, seven men each.",
    )
    # a King's fit: the allowance for exercise as a ship of one deck, a fourth of the upper
    # deck's twenty-six 18-pounders, the quarterdeck's and the forecastle's guns not counted
    # (judgement on the Article's "upper deck guns"; practice and resupply)
    magazine = fit_magazine(
        guns,
        {"long": KINGS_ROUNDS, "carronade": KINGS_ROUNDS, "swivel": SWIVEL_ROUNDS},
        exercise_allowance(26),
    )
    b.armament(
        "The armament (spec M7 7; package 70): the guns as parts of the graph by their place, "
        "in the one fit the class carried in 1805; each with its crew by the quarter bill and "
        "the magazine's allowance by kind and calibre. Every figure's source is in "
        "tools/gen_ships.py; "
        "the weights are from memory and UNVERIFIED against a printed page, and the "
        "quarterdeck's guns are INCORRECT against Winfield 1793-1817 p. 143 (eight 9-pounders "
        "and six carronades, not two and eight), kept by the owner's ruling pending correction.",
        "amazon class 1795",
        [
            (
                "amazon class 1795",
                "Winfield, British Warships in the Age of Sail 1793-1817, p. 143, the Amazon "
                "class (this fit's quarterdeck is from memory and INCORRECT against it, pending "
                "correction); Lavery, Arming and Fitting, the carronade establishment of 1794-5 "
                "and the Ordnance's allowance; Douglas 1820, the crews",
                guns,
                magazine,
                "The class's armament of 1795 as this fit has it: 26 x 18-pounders, 10 x "
                "32-pounder carronades, 4 x 9-pounders. INCORRECT on the quarterdeck, pending "
                "correction (the owner, 2026-10-25): Winfield 1793-1817 p. 143 gives it 8 x "
                "9-pounders and 6 x 32-pounder carronades, 44 pieces in all.",
            )
        ],
    )
    b.quarter_bill(
        QUARTER_BILL_NOTE,
        [
            (
                "forecastle",
                8,
                "The trimmers: of the forecastlemen, for the head sails and the fore braces "
                "(Luce 1884 ch. XX: the forecastlemen 'the best older seamen'); the five "
                "counts make the 44 hands the 264 leave when every gun of a side, the chasers "
                "and the wheel are manned (judgement).",
            ),
            ("fore_top", 10, "Of the fore topmen, for the fore braces and the topsails aloft."),
            ("main_top", 12, "Of the main topmen, the largest top, for the main braces."),
            ("mizzen_top", 6, "Of the mizzen topmen, for the crossjack braces and the spanker."),
            (
                "afterguard",
                8,
                "Of the afterguard, at the main sheet and the after braces; the rest of the "
                "afterguard to the quarterdeck carronades.",
            ),
        ],
        2,
        0,
        "sail before guns",
        {
            "helm": "Two quartermasters at the wheel (Luce 1884 ch. XX, the quartermasters).",
            "powder": (
                "The powder beyond the idlers: none; a frigate's cooks, stewards, servants, "
                "the clerk, the cooper, the armourer and the sailmaker's crew pass the "
                "cartridges (judgement after Luce 1884 ch. XX, the powder division)."
            ),
            "priority": PRIORITY_NOTE,
        },
        small_arms=20,
        boarders=60,
        small_arms_note=(
            "Twenty topmen and forecastlemen with the muskets of the stand of arms (judgement "
            "for a 36-gun frigate of 264)."
        ),
        boarders_note=(
            "Sixty boarders by the bill: the first and second boarders told off from the guns' "
            "crews, with the forty marines (judgement: a frigate's boarding party of a hundred)."
        ),
        filling=filling_party(guns),
    )


def cutter_armament(b, deck_height):
    """The cutter's two fits (the owner, 2026-10-23): the Admiralty's 12-pounder carronades
    that its cutters carried from the 1790s, the default of 1805 (Winfield, the hired and
    the Admiralty's cutters of 1793-1817: ten 12-pounder carronades in a cutter of 150 to
    200 tons, six to eight in the smaller; six for 85 tons, judgement; UNVERIFIED from
    memory), and the long 3-pounders with eight swivels her file names in words, the
    revenue and the hired cutters' fit of the 1760s on (Sherbourne's as built, the kit's
    manual; the swivels Falconer 1780, SWIVEL)."""
    deck = deck_height + PORT_SILL_M
    rail = deck_height + 0.8  # the rail about two feet eight above the deck (judgement)
    xs = spaced(2.5, -3.5, 3)
    carronades = []
    for i, x in enumerate(xs, start=1):
        carronades += broadside_pair(
            i,
            "carronade",
            12,
            CARRONADE_CWT[12],
            x,
            deck,
            (
                "Six 12-pounder carronades, three a side, abaft the mast where a cutter's "
                "ports lie (judgement): the Carron Company's 12-pounder of about 6 cwt (from "
                "memory), four men to the pair."
                if i == 1
                else None
            ),
        )
    long_guns = []
    for i, x in enumerate(xs, start=1):
        long_guns += broadside_pair(
            i,
            "long",
            3,
            LONG_GUN_CWT[3],
            x,
            deck,
            (
                "Six long 3-pounders, three a side (the kit's manual: Sherbourne's six "
                "3-pounders): the 4 ft 6 in gun of 7 cwt (from memory), three men to the pair."
                if i == 1
                else None
            ),
        )
    long_guns += swivels(
        8,
        [5.0, 1.0, -2.0, -5.0],
        rail,
        "Eight half-pounder swivels on the rail, four a side (the kit's manual; Falconer "
        "1780, SWIVEL: 'a small piece of artillery ... fixed on a socket'), a man each when "
        "a man is spare.",
    )
    # the Admiralty's carronades a King's fit, with the allowance for exercise (practice and
    # resupply); the revenue's and the hired cutters' long guns none
    carr_magazine = fit_magazine(
        carronades, {"carronade": HIRED_ROUNDS}, exercise_allowance(len(carronades))
    )
    long_magazine = fit_magazine(long_guns, {"long": HIRED_ROUNDS, "swivel": SWIVEL_ROUNDS})
    b.armament(
        "The armament (spec M7 7; package 70): two fits the scenario chooses between (ship: "
        "{fit: ...}; the owner, 2026-10-23): the 12-pounder carronades the Admiralty gave its "
        "cutters from the 1790s, the default of 1805, and the long 3-pounders with eight "
        "swivels of the revenue and hired cutters. Every figure's source is in "
        "tools/gen_ships.py; the weights are from memory and UNVERIFIED against a page.",
        "carronades",
        [
            (
                "carronades",
                "Winfield, British Warships in the Age of Sail 1793-1817, the Admiralty's and "
                "the hired armed cutters (UNVERIFIED from memory; the count for 85 tons "
                "judgement); Lavery, Arming and Fitting, the carronade",
                carronades,
                carr_magazine,
                "The Admiralty's fit of 1805: six 12-pounder carronades.",
            ),
            (
                "long guns",
                "The kit's manual (Sherbourne as built, 1763: six 3-pounders and eight "
                "swivels); Falconer 1780, SWIVEL; the weights from memory",
                long_guns,
                long_magazine,
                "The revenue and hired cutters' fit: six long 3-pounders and eight swivels.",
            ),
        ],
    )
    b.quarter_bill(
        QUARTER_BILL_NOTE,
        [
            (
                "forecastle",
                4,
                "The trimmers: four of the forecastlemen for the head sails and the running "
                "bowsprit (judgement).",
            ),
            ("afterguard", 4, "Four of the afterguard at the main sheet and the boom."),
        ],
        1,
        2,
        "sail before guns",
        {
            "helm": "One man at the tiller (a cutter steers with a tiller; judgement).",
            "powder": "Two of the waisters to pass the cartridges (judgement).",
            "priority": PRIORITY_NOTE,
        },
        small_arms=6,
        boarders=20,
        small_arms_note=(
            "Six of the cutter's best shots with the stand of arms' muskets (judgement); she "
            "bears no marines."
        ),
        boarders_note=(
            "Twenty of the cutter's seamen with cutlass and pistol (judgement: a cutter's "
            "company boards almost whole)."
        ),
        filling=filling_party(carronades),
    )


def privateer_schooner(b, out_dir):
    """The letter of marque of Speedwell's draught (PROVISIONAL; the owner's ask of
    2026-10-25, ahead of package 75): the hull, the rig, the company and the boats are the
    topsail schooner's, built above, with her guns and her quarter bill
    (`schooner_armament`); a file of her own so that every scenario and trial sailing the
    unarmed Speedwell is untouched."""
    b.doc["ship"]["era_notes"] = (
        "A Baltimore privateer schooner of about 1804 (PROVISIONAL, ahead of package 75): "
        "Speedwell's draught, Kemp's Lynx of 1812 (Chapelle 1930, pp. 82-83), her hull, rig "
        "and company of forty the topsail schooner's, armed with a long 12-pounder on a pivot "
        "amidships and four carronades (the default fit), or a letter of marque's six long "
        "6-pounders; see tools/gen_ships.py for every rule."
    )
    b.descriptions(
        [
            (
                "privateer schooner",
                "a schooner",
                "a topsail schooner, pierced for guns",
                "PROVISIONAL. A Baltimore schooner armed as a letter of marque; her ports are "
                "what the glass makes out, not her commission (judgement).",
            ),
        ]
    )
    b.dump(
        os.path.join(out_dir, "privateer-schooner.yaml"),
        "# PROVISIONAL (the owner's ask of 2026-10-25, ahead of package 75): a letter of marque\n"
        "# of Speedwell's draught, Kemp's Lynx of 1812 (Chapelle, The Baltimore Clipper, 1930,\n"
        "# pp. 82-83), the hull, rig and company the topsail schooner's (topsail-schooner.yaml\n"
        "# and its sources), with two fits (a long 12-pounder on a pivot and four carronades,\n"
        "# the default; a letter of marque's six long 6-pounders) and a quarter bill.\n"
        "# Generated by tools/gen_ships.py; edit that script and rerun, do not edit this file.\n"
        "# Units: metres, m2, kg, kN. Comments mark judgements.\n",
    )


def schooner_armament(b):
    """PROVISIONAL (the owner's ask of 2026-10-25, ahead of package 75): the topsail
    schooner's first fit, to test the armament's extensibility to a new hull through the
    generator alone. A letter of marque's armament of about 1805: six long 6-pounders, three
    a side, in the 2nd, 4th and 6th of Lynx's seven ports a side (Chapelle 1930, p. 82: seven
    ports a side on the Admiralty's draught), and four half-pounder swivels on the rail. A
    Baltimore letter of marque of Lynx's size shipped six or eight guns and about forty men,
    a privateer twice the guns and three times the men (from memory, UNVERIFIED; the count
    a judgement for the file's complement of forty). The pivot gun ('long Tom') the type is
    known for is the default fit built below it (`pivot_gun`, the place `pivot` of
    `GUN_PLACES`, the owner's loadout of 2026-10-25), with four carronades and the swivels;
    this six-gun fit is the letter of marque's. Package 75 replaces both fits from the
    type's own records (spec M7 §7, §27)."""
    # The port sills 3 ft 5 in above the water (Spider's specification, Chapelle pp.
    # 166-167), the source's own figure rather than the deck's: a low-sided vessel whose lee
    # ports shut at about 12 degrees of heel (shot.lee_port_shut's foot above the water).
    sill = ft(3.0 + 5.0 / 12.0)
    rail = 0.9 + 0.8  # the rail about two feet eight above the deck (judgement, as the cutter's)
    guns = []
    for i, x in enumerate(spaced(8.4, -8.4, 3), start=1):
        guns += broadside_pair(
            i,
            "long",
            6,
            LONG_GUN_CWT[6],
            x,
            sill,
            (
                "PROVISIONAL (ahead of package 75). Six long 6-pounders, three a side, in the "
                "2nd, 4th and 6th of the seven ports (Chapelle p. 82; the count a judgement): "
                "the 7 ft gun of 20 cwt (from memory), six men to the pair."
                if i == 1
                else None
            ),
        )
    guns += swivels(
        4,
        [10.0, -10.0],
        rail,
        "PROVISIONAL. Four half-pounder swivels on the rail, two a side at the bow and the "
        "quarter (judgement; Falconer 1780, SWIVEL), a man each when a man is spare.",
    )
    magazine = fit_magazine(guns, {"long": HIRED_ROUNDS, "swivel": SWIVEL_ROUNDS})
    # The long Tom (the owner's loadout, 2026-10-25): one long 12-pounder on a pivot
    # amidships between the masts (the fore at +7.8 m, the main at -2.6 m), firing over the
    # rail on either side, and four 12-pounder carronades, two a side, in the ports forward
    # of the fore mast and abaft the main, clear of the pivot's sweep; the swivels as above.
    # The Baltimore privateers of 1812 carried a long 12, 18 or 24 on the pivot and a few
    # carronades or long guns on the broadside (Chapelle 1930, from memory, UNVERIFIED; the
    # long 12 a judgement for a hull of 224 tons).
    tom = pivot_gun(
        "long",
        12,
        LONG_GUN_CWT[12],
        2.6,
        rail,
        (60.0, 140.0),
        "PROVISIONAL (the owner's loadout, 2026-10-25). The long Tom: a long 12-pounder of "
        "34 cwt (from memory) on a pivot amidships between the masts, firing over the rail to "
        "either side; nine men by the gun's rule. Its arc from 60 to 140 degrees off the bow "
        "(the owner's ruling of the day, from her rig: the fore topmast backstays at about 55 "
        "to 60 degrees from the pivot, the main shrouds at about 140 to 150; "
        "docs/design/Proposal-PivotGun.md §3).",
    )
    for i, x in enumerate((10.5, -7.5), start=1):
        tom += broadside_pair(
            i,
            "carronade",
            12,
            CARRONADE_CWT[12],
            x,
            sill,
            (
                "PROVISIONAL. Four 12-pounder carronades, two a side, forward of the fore mast "
                "and abaft the main, clear of the pivot's sweep (judgement): the Carron "
                "Company's 12-pounder of about 6 cwt (from memory), four men to the pair."
                if i == 1
                else None
            ),
        )
    tom += swivels(4, [10.0, -10.0], rail, None)
    tom_magazine = fit_magazine(
        tom, {"long": HIRED_ROUNDS, "carronade": HIRED_ROUNDS, "swivel": SWIVEL_ROUNDS}
    )
    b.armament(
        "The armament (spec M7 7; package 70's shape): PROVISIONAL, the owner's ask of "
        "2026-10-25 ahead of package 75, which gives the schooner her fits from the type's own "
        "records. Two fits the scenario chooses between (ship: {fit: ...}): the long Tom on "
        "its pivot with four carronades, the default, and a letter of marque's six long "
        "6-pounders. Every figure's source is in tools/gen_ships.py; the weights are from "
        "memory and UNVERIFIED against a page.",
        "long tom",
        [
            (
                "long tom",
                "Chapelle, The Baltimore Clipper, 1930 (the pivot gun of the Baltimore "
                "privateers, from memory, UNVERIFIED); the owner's loadout of 2026-10-25; the "
                "weights from memory",
                tom,
                tom_magazine,
                "PROVISIONAL. A privateer's fit: a long 12-pounder on the pivot, four "
                "12-pounder carronades and four swivels.",
            ),
            (
                "letter of marque",
                "Chapelle, The Baltimore Clipper, 1930, p. 82 (Lynx's seven ports a side) and "
                "pp. 166-167 (Spider's port sills); the count of guns a judgement for a letter "
                "of marque of forty men (UNVERIFIED from memory); the weights from memory",
                guns,
                magazine,
                "PROVISIONAL. A letter of marque's fit: six long 6-pounders and four swivels.",
            ),
        ],
    )
    b.quarter_bill(
        QUARTER_BILL_NOTE,
        [
            (
                "forecastle",
                4,
                "PROVISIONAL. The trimmers: four of the forecastlemen for the head sails "
                "(judgement).",
            ),
            ("fore_top", 3, "Three of the fore topmen for the fore braces and the topsail."),
            ("afterguard", 4, "Four of the afterguard at the main sheet and the gaffs."),
        ],
        1,
        2,
        "sail before guns",
        {
            "helm": "One man at the tiller (a Baltimore schooner steered with a tiller; "
            "judgement).",
            "powder": "Two of the waisters to pass the cartridges (judgement).",
            "priority": PRIORITY_NOTE,
        },
        small_arms=8,
        boarders=26,
        small_arms_note=(
            "Eight of her people with the stand of arms' muskets (PROVISIONAL, for package 75: "
            "judgement after the King's cutter's six of thirty); she bears no marines."
        ),
        boarders_note=(
            "Twenty-six boarders of her forty with cutlass and pistol (PROVISIONAL, for package "
            "75: judgement after the King's cutter's twenty of thirty; a privateer's company "
            "boards almost whole)."
        ),
        filling=filling_party(tom),
    )


def brig_armament(b, deck_height):
    """H.M. brig-sloop Harpy's: sixteen 32-pounder carronades and two long 6-pounder chase
    guns (the kit's manual; Winfield's Diligence class, UNVERIFIED from memory), one fit; the
    carronades eight a side along the flush deck, the 6-pounders at the bow ports."""
    deck = deck_height + PORT_SILL_M
    guns = []
    for i, x in enumerate(spaced(9.1, -9.1, 8), start=1):
        guns += broadside_pair(
            i,
            "carronade",
            32,
            CARRONADE_CWT[32],
            x,
            deck,
            (
                "Sixteen 32-pounder carronades, eight a side (the kit's manual; Winfield, the "
                "Diligence class, UNVERIFIED from memory): 17 cwt each (from memory), the "
                "ports about eight feet and a half apart (judgement), five men to the pair."
                if i == 1
                else None
            ),
        )
    guns += chasers(
        "bow",
        "long",
        6,
        LONG_GUN_CWT[6],
        12.0,
        deck,
        "Two long 6-pounders at the bow ports as the chase guns (the kit's manual): the 7 ft "
        "gun of 20 cwt (from memory), six men each.",
    )
    # a King's fit: the allowance for exercise a fourth of her guns, all on the flush deck
    # (practice and resupply)
    magazine = fit_magazine(
        guns, {"long": KINGS_ROUNDS, "carronade": KINGS_ROUNDS}, exercise_allowance(len(guns))
    )
    b.armament(
        "The armament (spec M7 7; package 70): the guns as parts of the graph by their place, "
        "the class's one fit; each with its crew by the quarter bill and the magazine's "
        "allowance by kind and calibre. Every figure's source is in tools/gen_ships.py; the "
        "weights and "
        "the establishment are from memory and UNVERIFIED against a printed page.",
        "diligence class 1796",
        [
            (
                "diligence class 1796",
                "The kit's manual (docs/design/VesselCandidates.md); Winfield, British Warships "
                "in the Age of Sail 1793-1817, the Diligence class (UNVERIFIED from memory); "
                "Lavery, Arming and Fitting; Douglas 1820, the crews",
                guns,
                magazine,
                "The class's armament: 16 x 32-pounder carronades, 2 x 6-pounder chase guns.",
            )
        ],
    )
    b.quarter_bill(
        QUARTER_BILL_NOTE,
        [
            ("forecastle", 6, "The trimmers: six of the forecastlemen for the head sails."),
            ("fore_top", 6, "Six of the fore topmen for the fore braces."),
            ("main_top", 7, "Seven of the main topmen for the main braces."),
            ("afterguard", 8, "Eight of the afterguard at the main sheet and the after braces."),
        ],
        2,
        0,
        "sail before guns",
        {
            "helm": "Two quartermasters at the wheel (Luce 1884 ch. XX).",
            "powder": (
                "The powder beyond the idlers: none; the cooks, stewards and servants pass the "
                "cartridges (judgement)."
            ),
            "priority": PRIORITY_NOTE,
        },
        small_arms=8,
        boarders=30,
        small_arms_note="Eight of the brig's seamen with the stand of arms' muskets (judgement).",
        boarders_note="Thirty boarders from the guns' crews with the twenty marines (judgement).",
        filling=filling_party(guns),
    )


def merchant_brig_armament(b):
    """The merchant brig's few guns (spec M7 §7: 'the merchant brig's few'): four long
    6-pounders, two a side, for her own defence against a privateer's boats (the period's
    merchantmen of three hundred tons carried a few 4- or 6-pounders or none; judgement),
    with a merchant's scant magazine; her hull and deck the Harpy's."""
    deck = 1.5 + PORT_SILL_M
    guns = []
    for i, x in enumerate((4.0, -4.0), start=1):
        guns += broadside_pair(
            i,
            "long",
            6,
            LONG_GUN_CWT[6],
            x,
            deck,
            (
                "Four long 6-pounders, two a side (judgement: a merchant brig's defence against "
                "a privateer's boats), the 7 ft gun of 20 cwt (from memory); the merchant's "
                "bill gives four men to the pair where the King's would give six, so her guns "
                "are served short and slow (spec M7 8)."
                if i == 1
                else None
            ),
        )
    for g, _ in guns:
        g["crew"] = 4  # the merchant's own quarter bill, short of Douglas's figure (judgement)
    magazine = fit_magazine(guns, {"long": MERCHANT_ROUNDS})
    b.armament(
        "The armament (spec M7 7; package 70): the merchant brig's few guns, one fit, her "
        "magazine a trader's (twenty round and a little grape a gun: judgement). Every "
        "figure's source is in tools/gen_ships.py; the weights are from memory.",
        "merchant",
        [
            (
                "merchant",
                "Judgement on the period's trade (a brig of three hundred tons carried a few "
                "4- or 6-pounders for her own defence, or none); the gun's weight from memory",
                guns,
                magazine,
                "A trader's fit: four 6-pounders, two a side.",
            )
        ],
    )
    b.quarter_bill(
        QUARTER_BILL_NOTE,
        [
            ("fore_top", 1, "The trimmers: a topman of each top for the braces (judgement)."),
            ("main_top", 1, None),
        ],
        1,
        0,
        "sail before guns",
        {
            "helm": "One man at the wheel (judgement).",
            "powder": "The powder beyond the idlers: none; the cook and the boy (judgement).",
            "priority": (
                "A merchantman's weapon is her heels: the sails before the guns (judgement)."
            ),
        },
        small_arms=2,
        boarders=6,
        small_arms_note=(
            "Two men with the master's muskets from the cabin (judgement: a merchant brig's "
            "chest of arms)."
        ),
        boarders_note="Six of the merchant brig's hands: a trader does not board (judgement).",
        filling=filling_party(guns),
    )


def frigate_crew(b):
    posts_note = (
        "Station holders by post (spec M3 2.3): the commissioned officers, then the standing "
        "and warrant officers (Falconer, ORDINARY and CARPENTER). Names are drawn at muster "
        "unless a post gives one."
    )
    b.crew(
        [
            (("complement",), 264, "Winfield: the Amazon class establishment, 264 men."),
            (("names",), "english", "A King's ship: the english list in data/crew/names.yaml."),
            (
                ("stations", "forecastle"),
                28,
                "Hands per station, both watches together. Forecastlemen: the head, anchors "
                "and headsails; the best older seamen (Luce 1884 ch. XX). 28: judgement "
                "(spec M3 2.3).",
            ),
            (
                ("stations", "fore_top"),
                24,
                "Fore topmen: judgement (spec M3 2.3); Luce: the smartest of the young seamen.",
            ),
            (
                ("stations", "main_top"),
                30,
                "Main topmen: judgement (spec M3 2.3), the largest top.",
            ),
            (("stations", "mizzen_top"), 14, "Mizzen topmen: judgement (spec M3 2.3)."),
            (
                ("stations", "afterguard"),
                50,
                "Afterguard, the boys included (spec M3 9 item 6: boys count as landsmen): "
                "judgement (spec M3 2.3).",
            ),
            (
                ("stations", "waisters"),
                36,
                "Waisters: judgement. The spec's 48 less the twelve posts, so that stations and "
                "posts make the 264 of the establishment (the spec's figures made 276); the "
                "waist is the station whose numbers no yard or gear fixes.",
            ),
            (
                ("stations", "marines"),
                40,
                "Marines: judgement (spec M3 2.3), a sergeant's party for a frigate; they "
                "stand watch and work as afterguard, never aloft (Luce 1884 ch. XX).",
            ),
            (
                ("stations", "idlers"),
                30,
                "Idlers: the trades below (Luce 1884 ch. XX: they stand no night watches).",
            ),
            (
                ("ratings", "able"),
                0.30,
                "Share of the seamen (not marines, idlers or officers) by rating: judgement "
                "(spec M3 2.3), a wartime frigate's books (Falconer, ORDINARY: able and "
                "ordinary as rated on the navy books). Able: 0.30.",
            ),
            (("ratings", "ordinary"), 0.40, "Ordinary: 0.40, judgement."),
            (("ratings", "landsman"), 0.30, "Landsmen: 0.30, judgement."),
        ]
        + [
            (("posts", post), None, posts_note if i == 0 else None)
            for i, post in enumerate(FRIGATE_POSTS)
        ]
        + [
            (
                ("idlers_by_trade", "carpenter's crew"),
                6,
                "How the idlers are made up; they must sum to the idlers. Judgement for a "
                "frigate of 264 (spec M3 2.3). The carpenter's mates and crew: 6.",
            ),
            (("idlers_by_trade", "sailmaker's crew"), 3, "The sailmaker's mate and crew: 3."),
            (("idlers_by_trade", "cooper"), 1, "The cooper, for the casks: 1."),
            (("idlers_by_trade", "armourer"), 1, "The armourer, at the forge: 1."),
            (("idlers_by_trade", "cook"), 2, "The ship's cook and his mate: 2."),
            (("idlers_by_trade", "steward"), 3, "Purser's, captain's and gunroom stewards: 3."),
            (("idlers_by_trade", "servant"), 8, "Officers' servants: 8."),
            (("idlers_by_trade", "surgeon's mate"), 2, "The surgeon's mates: 2."),
            (("idlers_by_trade", "clerk"), 1, "The captain's clerk: 1."),
            (("idlers_by_trade", "master-at-arms's party"), 3, "The ship's corporals: 3."),
            (
                ("stores", "water_tons"),
                100,
                "Numbers only in milestone 3 (spec M3 10 says which milestone consumes each). "
                "Water: 100 tons in iron-hooped casks (spec M3 2.3 after Winfield, about four "
                "months at the frigates' allowance; at a gallon a man a day it is some twelve "
                "weeks for 264).",
            ),
            (
                ("stores", "provisions_days"),
                120,
                "Provisions: four months at full allowance for the complement (judgement).",
            ),
            (("stores", "spare_spars"), {}, None),  # the booms, by class: below
            (
                ("stores", "cordage_fathoms"),
                600,
                "Spare rope in the boatswain's store (judgement).",
            ),
            (
                ("stores", "shot_plugs"),
                40,
                SHOT_PLUGS_NOTE + " A frigate's 40.",
            ),
            *ration_entries("a King's ship"),
        ]
    )
    # The people (package 35, spec M5 §22): the named few beyond the posts. The master's
    # mates and the midshipmen "assist him in making any other observations or calculations"
    # (the Regulations of 1806, the Master, art. XXVIII, p. 192 of the 1808 printing); a
    # midshipman carries the captain's word about the ship (the messenger of
    # InwardAndOutward.md). Each is drawn from his station at muster, keeping the counts
    # of spec M3 §2.3 as they are: a master's mate an able seaman of the forecastle, a
    # midshipman one of the boys of the afterguard (spec M3 §9 item 6: the boys count as
    # landsmen). The roles and their notes are the wardroom file's (package 40).
    b.people(
        "The named people beyond the posts (package 35, spec M5 §22): each drawn from his "
        "station at muster, the counts above unchanged; see tools/gen_ships.py.",
        FRIGATE_DRAWN,
    )
    # The booms (package 30b): the spare spars Luce stows between the fore and main masts
    # (1866, ch. XVII Spare Spars, 'Stowing Booms between the fore and mainmast', 'In two
    # Piles'): to starboard the main topmast, a stump main topgallant mast, mast-fishes, a
    # half-yard and the main topmast studding-sail booms; to port the fore topmast, a stump
    # fore topgallant mast, a mast-fish, a half-yard, the fore topmast studding-sail booms and
    # the flying jib-boom; the spare main and fore topsail yards in the chains or cranes on
    # the quarters and the spare jib-boom amidships. Luce 1884 (ch. XI Purchasing Weights,
    # 'Stowing Booms') stows the same: "spare spars for the main and mizzen" to starboard,
    # "for the fore, and spare head-booms" to port, "spare topsail-yards in lumber-irons, or
    # cranes on the quarters". The mast-fishes and half-yards are fishes and makings, not
    # spars that replace one, and are left out; so is every spar Luce does not stow (a royal
    # mast, a lower mast, a lower yard, the bowsprit): "Top-gallant and royal-yards and
    # studding-sail booms are easily replaced" (1866), from spars the ship has not got here.
    b.spare_spars(
        "The booms: the spare spars by class (Luce 1866 ch. XVII, 'Stowing Booms'; Luce 1884 "
        "ch. XI, 'Stowing Booms'; Steel 1794 vol. I, 'Lashing of Booms': \"the spare topmasts, "
        'yards, &c. stowed on the boat skids"); see tools/gen_ships.py.',
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
            ("flying_jib_boom", 1, "The flying jib-boom, in the port pile (Luce 1866)."),
        ],
    )
    # The sail room (spec 3b §6.3), from Luce's allowance for a frigate (1884 ch. X p. 171,
    # Tables.md §1): two of each working sail, the second in the sail room; of the two
    # foresails and the two fore and main topsails "one fore-sail, one fore and one main-
    # topsail to be of No. 1 canvas", the heavy-weather sails, which are the second of their
    # kind here (spec 3b §6.3 reads "a second ... plus" them, three of each; the table allows
    # two, and Tables.md reads it so); one of each storm sail. The occasional sails, which the
    # allowance of 1884 no longer carried, one each (spec 3b §6.4). The main topmast staysail
    # and the studding sails are not in the allowance and have no second (judgement: one set
    # of studding sails, made up in the tops).
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
        "flying_jib",
        "mizzen.spanker",
        "fore.topmast_staysail",
    ]
    heavy = ["fore.course", "fore.topsail", "main.topsail"]
    storm = ["fore.storm_staysail", "mizzen.storm_staysail", "storm_mizzen"]
    occasional = [("ringtail", "ringtail")] + [(f"fore.save_all.{s}", "save-all") for s in SIDES]

    def first(notes, i):
        return notes if i == 0 else None

    b.sail_room(
        "The sail room (spec 3b §6.3): Luce's allowance for a frigate (1884 ch. X p. 171), "
        "every sail new; see tools/gen_ships.py.",
        [
            (
                k,
                FRIGATE_CANVAS[k][0],
                first("The second of each working sail, of the working number (Luce p. 171).", i),
            )
            for i, k in enumerate(working)
        ]
        + [
            (
                k,
                1,
                first(
                    "The heavy-weather foresail and fore and main topsails, of No. 1 "
                    "(Luce p. 171, the table's note).",
                    i,
                ),
            )
            for i, k in enumerate(heavy)
        ]
        + [
            (k, FRIGATE_CANVAS["storm"][0], first("Storm canvas, one of each (Luce p. 171).", i))
            for i, k in enumerate(storm)
        ]
        + [
            (k, FRIGATE_CANVAS[c][0], first("The occasional sails, one each (spec 3b §6.4).", i))
            for i, (k, c) in enumerate(occasional)
        ],
    )


def schooner_crew(b):
    b.crew(
        [
            (
                ("complement",),
                40,
                "A privateer's complement of about forty (Chapelle, The Baltimore Clipper; "
                "judgement, spec M3 2.3).",
            ),
            (
                ("names",),
                "american",
                "A Baltimore crew: the american list in data/crew/names.yaml.",
            ),
            (
                ("stations", "forecastle"),
                10,
                "Hands per station, both watches together; a schooner has no main or mizzen top "
                "and carries no marines. Forecastlemen: 10, judgement (spec M3 2.3).",
            ),
            (
                ("stations", "fore_top"),
                6,
                "Fore topmen, for the topsail and topgallant: 6, judgement (spec M3 2.3).",
            ),
            (
                ("stations", "afterguard"),
                11,
                "Afterguard, at the main sheet and the gaff sails: 11, judgement (spec M3 2.3).",
            ),
            (("stations", "waisters"), 6, "Waisters: 6, judgement (spec M3 2.3)."),
            (("stations", "idlers"), 4, "Idlers: the trades below (spec M3 2.3)."),
            (
                ("ratings", "able"),
                0.45,
                "Share of the seamen by rating: judgement. A privateer shipped prime seamen "
                "where she could, and more able hands than a King's ship. Able: 0.45.",
            ),
            (("ratings", "ordinary"), 0.40, "Ordinary: 0.40, judgement."),
            (("ratings", "landsman"), 0.15, "Landsmen: 0.15, judgement."),
        ]
        + [
            (
                ("posts", post),
                None,
                "Station holders by post (spec M3 2.3); names are drawn at muster."
                if i == 0
                else None,
            )
            for i, post in enumerate(SCHOONER_POSTS)
        ]
        + [
            (
                ("idlers_by_trade", "cook"),
                1,
                "How the idlers are made up (spec M3 2.3). The cook: 1, judgement.",
            ),
            (("idlers_by_trade", "steward"), 1, "A steward: 1, judgement."),
            (("idlers_by_trade", "carpenter's crew"), 1, "A carpenter: 1, judgement."),
            (("idlers_by_trade", "sailmaker's crew"), 1, "A sailmaker: 1, judgement."),
            (
                ("stores", "water_tons"),
                8,
                "Stores for a short cruise (spec M3 2.3). Water for six weeks: 40 men at a "
                "gallon a day is about 7.5 tons (judgement).",
            ),
            (("stores", "provisions_days"), 60, "Provisions: two months (judgement)."),
            (("stores", "spare_spars"), {}, None),  # the booms, by class: below
            (("stores", "cordage_fathoms"), 150, "Spare rope (judgement)."),
            (
                ("stores", "shot_plugs"),
                8,
                SHOT_PLUGS_NOTE + " A schooner's 8.",
            ),
            *ration_entries("a private ship of war's articles promised the like (judgement)"),
        ]
    )
    # The people (package 35, spec M5 §22): the master and a mate are posts already; a boy
    # of the afterguard carries the word (judgement: a privateer rated no midshipmen). The
    # roles and their notes are the wardroom file's (package 40).
    b.people(
        "The named people beyond the posts (package 35, spec M5 §22); see tools/gen_ships.py.",
        SCHOONER_DRAWN,
    )
    # The booms (package 30b): a privateer on a short cruise carried fewer spares than
    # Luce's frigate (1866, ch. XVII 'Stowing Booms', which the frigate's follow), and no
    # source lists a schooner's. Judgement from Luce's list scaled to her rig: one topmast,
    # which the upper spars of a two-masted vessel were made alike for, "in order that the
    # spare spars and sails may answer to replace those of either mast" (Chapelle 1930,
    # 'Masting Rules and Sail Plans', of the brig, after Fincham); a spare topsail yard, as
    # Luce's frigate carries hers ("a vessel may be saved from a lee-shore, by having a
    # topsail or lower yard to supply readily the place of one sprung", 1866); and one pair
    # of topmast studding-sail booms, as each of Luce's piles carries.
    b.spare_spars(
        "The booms: the spare spars by class (judgement after Luce 1866 ch. XVII, 'Stowing "
        "Booms', and Chapelle 1930, 'Masting Rules and Sail Plans'); see tools/gen_ships.py.",
        [
            ("topmast", 1, "One topmast, to answer either mast (judgement, after Chapelle)."),
            ("yard", 1, "A spare topsail yard (judgement, after Luce 1866)."),
            (
                "studdingsail_boom",
                2,
                "A pair of topmast studding-sail booms (judgement, after Luce 1866).",
            ),
        ],
    )
    # The sail room (spec 3b §6.3): a second foresail, fore topsail and jib, the sails a
    # privateer on a short cruise could least do without (spec 3b §6.3, judgement), with her
    # storm canvas and occasional sails, one each (spec 3b §6.4).
    b.sail_room(
        "The sail room (spec 3b §6.3), every sail new; see tools/gen_ships.py.",
        [
            (
                "fore.sail",
                SCHOONER_CANVAS["fore.sail"][0],
                "A second foresail, fore topsail and jib (spec 3b §6.3, judgement).",
            ),
            ("fore.topsail", SCHOONER_CANVAS["fore.topsail"][0], None),
            ("jib", SCHOONER_CANVAS["jib"][0], None),
            (
                "storm_trysail",
                SCHOONER_CANVAS["storm trysail"][0],
                "Storm canvas, one of each (spec 3b §6.4, judgement).",
            ),
            ("storm_jib", SCHOONER_CANVAS["storm jib"][0], None),
            (
                "ringtail",
                SCHOONER_CANVAS["ringtail"][0],
                "The occasional sails, one each (spec 3b §6.4).",
            ),
            ("water_sail", SCHOONER_CANVAS["water sail"][0], None),
        ],
    )


# ---------------------------------------------------------------------------
# The cutter: H.M. armed cutter Sherbourne, 1763 (package 32b; spec M5 §23)
# ---------------------------------------------------------------------------
#
# Sources. The hull from the kit's manual as the owner noted it (VesselCandidates.md;
# Winfield's 1714 to 1792 volume and the RMG draught were not reachable): 85 tons burthen,
# 54 ft 6 in, 19 ft beam, complement 30, six 3-pounders and eight swivels. The 54 ft 6 in
# is on deck, which the burthen settles: by the Navy's rule (keel x breadth x half-breadth
# / 94) a keel of 54 ft 6 in on 19 ft would make 105 tons; 85 tons want a keel for tonnage
# of 44 ft 3 in, a fifth less, which is the difference between the deck and the keel of a
# cutter with a plumb stem and a raking post.
#
# The spars by Fincham 1843, 'On Masting Cutters and Schooners', 'Proportions for the
# Masts, Booms, &c. of Cutters' (the OCR's p. 67: a table of proportions in terms of the
# breadth and the length on deck for three yachts and two revenue cruisers; the second
# revenue cruiser, 55.8 ft by 18.5 ft, is Sherbourne's size, and her column is taken, the
# first's, 63.7 ft by 22.1 ft, as the check). His footnote to the table (p. 67) works the
# sails of "a cutter of 85 tons": mainsail 1566 sq ft, foresail 367, second jib 541,
# 2474 sq ft in all, their centres 29.4, 20.0 and 19.5 ft above the water and 14.8 ft
# abaft, 13.7 and 32.8 ft before the middle; it is a yacht's masting (the nock 2.4 to
# 2.6 breadths up), so the file's sails are drawn from the revenue cruiser's spars by his
# rules and the footnote is the check. The rules for the sails are his arts. 86 and 87
# (pp. 35 to 36): the mainsail's nock 2.1 to 2.2 breadths above the water in revenue
# cruisers, the leech 1.4 to 1.6 of the luff, the head 0.6 to 0.66 of the foot (0.74 in
# some revenue cruisers), the gaff peaked 25 to 30 degrees; the foresail's foot 0.9 of the
# distance from the stay to the mast, its luff 0.8 to 0.87 of the stay and its leech 0.8 of
# the luff; the jib's tack 0.55 to 0.6 of the water-line before the stem, its foot the
# distance from the tack to the stem, its luff 0.8 to 0.85 of the stay; the bowsprit 8 to
# 9 in beyond the jib's tack, plus what is housed. Steel 1794 vol. I: the cutter's masts
# in one stick or with a fidded topmast ("cutters and other small vessels have their
# lower-masts and top-masts all in one ... sometimes they have a common head, like other
# lower-masts, with cross-trees, cap, and top-mast", 'Top-masts', OCR line 2905; "Cutter's
# masts are oftentimes left eight-square four or five feet above the deck", line 3699),
# the rake of cutters' masts "one inch and a half to [a] yard" and "their bowsprits lie
# nearly in an horizontal direction" (line 1909), the HEEL-ROPE "to haul out the bowsprits
# of cutters" (line 20214); his sail-making chapter for each sail (cited at each). The
# heel-rope and the traveller are the running bowsprit's gear; Falconer 1780, CUTTER: "a
# small vessel commonly navigated in the channel of England; it is furnished with one
# mast, and rigged as a sloop ... Many of these vessels are used on an illicit trade, and
# others employed by the government to seize them".

CUTTER_CANVAS: dict[str, tuple[int, str]] = {
    "main.sail": (2, f"{STEEL_SM} p. 120, 'Cutter's mainsail': No. 1 or 2"),
    "square_sail": (
        6,
        f"{STEEL_SM} p. 124, 'Sloop's square-sail, or cross-jack': No. 6 or 7; the heavier taken",
    ),
    "topsail": (
        6,
        f"{STEEL_SM} p. 125, 'Sloop's topsail': No. 6 or 7, the cutter's light flying topsail "
        "that the schooner's file set aside as not hers; it is this one's",
    ),
    "topgallant": (8, f"{STEEL_SM} p. 126, 'Sloop's topgallant-sail': No. 8"),
    "main.gaff_topsail": (8, f"{STEEL_SM} p. 126, 'Sloop's gaff topsail': No. 8"),
    "fore.staysail": (2, f"{STEEL_SM}, 'Smack's foresail' (OCR line 15622): No. 1 or 2"),
    "jib": (2, f"{STEEL_SM}, 'Smack's jib' (OCR line 15709): No. 1 or 2"),
    "storm trysail": (1, f"{STEEL_SM}, 'Cutter's trysail' (OCR line 14359): No. 1 or 2"),
    "storm jib": (
        1,
        f"{STEEL_SM}, the sloop's jibs (p. 190): 'No. 1 or 2 ... two-thirds of the size of the "
        "first jib, and is used in stormy weather, in lieu of a larger one'",
    ),
}

# The cutter's rope sizes, inches of circumference (judgement: Steel's rigging table for a
# cutter of 200 tons is in his second volume, not in the OCR references; these are the
# schooner's sizes for the same gear, a little lighter on a hull of 85 tons, and rated by
# Luce 1866 ch. IV as every line is).
CUTTER_ROPE = {
    "square_sail": {
        "halyard": 3.5,  # the tye of a yard hoisted from the deck
        "sheet": 3.0,
        "brace": 2.0,
        "lift": 2.0,
        "clewline": 2.0,
        "buntline": 1.5,
        "bowline": 2.0,
        "reef_tackle": 2.0,
    },
    "topsail": {
        "halyard": 2.5,
        "sheet": 2.5,
        "brace": 1.75,
        "lift": 1.75,
        "clewline": 1.75,
        "buntline": 1.5,
        "bowline": 1.75,
        "reef_tackle": 1.75,
    },
    "topgallant": {
        "halyard": 1.75,
        "sheet": 1.75,
        "brace": 1.5,
        "lift": 1.5,
        "clewline": 1.5,
        "buntline": 1.25,
    },
}


def cutter(out_dir="data/ships"):
    # Design winds: the frigate's, with the gaff topsail's 22 knots (as the schooner's) for
    # the square sail and the topgallant as well: a cutter's square sail is a fair-wind sail
    # set flying from the deck, and her topgallant is the lightest sail she has; both come
    # in as early as the gaff topsail (the rule the package brief asks for; judgement).
    dw = dict(DESIGN_WIND_KN, gaff_topsail=22.0, square_sail=22.0, topgallant=22.0)
    # -- hull ---------------------------------------------------------------------------
    lod_ft = 54.5  # on deck (the manual; the burthen settles it, see the section comment)
    beam_ft = 19.0
    burthen = 85.0
    keel_ft = burthen * 94.0 / (beam_ft * beam_ft / 2.0)  # 44.3 ft for tonnage, by the rule
    lwl_ft = 50.0  # judgement: a plumb stem, a raking post; nearer the deck than the keel
    # Draught: the brief's rule for the type, half her breadth aft (a cutter drew deep
    # aft, for grip on a wind), less Fincham's excess of draught aft for the second
    # revenue cruiser, 24 in (p. 67, the table's last row), forward; the mean is stored.
    draught_aft_ft = 0.5 * beam_ft
    draught_fwd_ft = draught_aft_ft - 2.0
    draught_ft = (draught_aft_ft + draught_fwd_ft) / 2.0
    lwl, beam, draught = ft(lwl_ft), ft(beam_ft), ft(draught_ft)
    # Displacement: Cb 0.45 (judgement) on LWL x beam x mean draught: fuller than the
    # schooner's 0.33 (her 30 degrees of deadrise) for the deep, full-bodied revenue
    # cutter of the draughts, slacker than the frigate's 0.55; about 105 t, 1.24 x the 85
    # tons burthen. Fincham's check: the area of sail is 3.5 x the area of the load water
    # section for the second revenue cruiser (p. 67); at a waterplane coefficient of
    # 0.75 that section is 712 sq ft and the sail 2,490, which is his 85-ton cutter's
    # 2,474 sq ft of mainsail, foresail and jib.
    displacement = round(lwl * beam * draught * 0.45 * 1025.0, -3)
    deck_height = 0.9  # judgement: a low-sided vessel, the deck about 3 ft above the water
    deck_above_lwl_ft = deck_height / FT
    # Rake: Fincham's second revenue cruiser, 13 in in 12 ft (p. 67); Steel gives cutters
    # 1.5 in to the yard, less, and is the check.
    rake_deg = round(math.degrees(math.atan(13.0 / 144.0)), 1)

    b = Builder(
        "Sherbourne",
        "cutter",
        "H.M. armed cutter Sherbourne (Slade's design, built at Woolwich, launched 1763): "
        "85 tons burthen, 54 ft 6 in on deck, 19 ft beam; the Channel's revenue cutter, of "
        "the type the pilot cutters and the hired armed cutters of the war shared; six "
        "3-pounders and eight swivels (her two fits, the Admiralty's 12-pounder carronades of "
        "1805 the default: armament below, package 70). Hull from the "
        "kit's manual (Winfield and the Greenwich draught not reached); spars by Fincham "
        "1843's table of proportions for revenue cruisers (p. 67) and his rules for cutters' "
        "sails (arts. 86, 87); sails by Steel 1794; see tools/gen_ships.py for every rule.",
        {
            "length_waterline_m": lwl,
            "beam_m": beam,
            "draught_m": draught,
            "displacement_kg": displacement,
            "gm_m": 1.1,
            "clr_x_m": -0.4,
            "lateral_area_m2": round(lwl * draught * 0.85),
            "hull_speed_kn": 9.5,
            "deck_height_m": deck_height,
            "rudder": {"area_m2": 1.2, "max_angle_deg": 35, "rate_deg_s": 5.0, "span_m": 2.7},
        },
        {
            "length_waterline_m": f"{lwl_ft:.0f} ft: judgement between the {keel_ft:.0f} ft "
            f"keel for tonnage (85 tons on 19 ft by the Navy's rule) and the {lod_ft} ft "
            "on deck (the kit's manual), a plumb stem and a raking post.",
            "beam_m": "19 ft 0 in (the kit's manual; Winfield not reached).",
            "draught_m": f"{draught_ft:.1f} ft mean: {draught_aft_ft:.1f} ft aft, half her "
            f"breadth (the type's rule, judgement), {draught_fwd_ft:.1f} ft forward "
            "(Fincham 1843 p. 67: a revenue cruiser's excess of draught aft, 24 in).",
            "displacement_kg": "LWL x beam x draught x Cb 0.45 x 1025, about 105 t, 1.24 x "
            "the 85 tons burthen (Cb judgement: fuller than the schooner's 0.33, slacker "
            "than the frigate's 0.55, for a deep full-bodied revenue cutter).",
            "gm_m": "3 ft 7 in: judgement; a cutter was stiff and carried a great press of "
            "sail (the type's reputation), heavily ballasted; more than the schooner's "
            "3 ft 3 in on a narrower beam.",
            "clr_x_m": "Judgement, set as the schooner's was: the centre of pressure a "
            "little before the middle so that she is balanced close-hauled in 15 kn and "
            "carries a few degrees of weather helm on a beam reach (measured; see "
            "docs/dev/TuningNotes.md, package 32b). Fincham p. 67 puts a revenue "
            "cruiser's centre of effort 0.017 of the water-line abaft the middle.",
            "lateral_area_m2": "LWL x draught x 0.85 for a deep full profile.",
            "hull_speed_kn": f"1.34 sqrt({lwl_ft:.0f} ft) = 9.5 knots, kept: the type's "
            "records of 10 to 11 knots are the big cutters' of 150 to 200 tons (judgement).",
            "deck_height_m": "The deck about 3 ft above the water (judgement: a low-sided "
            "vessel, as the schooner).",
            "rudder": "A deep narrow blade, about 9 ft by 1 ft 6 in (judgement; span_m its "
            "depth, 9 ft; package 32e).",
        },
    )

    # -- spars in feet by Fincham's table (p. 67), the second revenue cruiser's column ---
    main_hounded = 2.6 * beam_ft  # main-mast hounded = 2.6 x breadth extreme
    main_head = 0.23 * main_hounded  # main-mast headed = 0.23 x hounded length
    main_total = main_hounded + main_head
    below_lwl = 0.269 * beam_ft  # main-mast below the load-water-line = 0.269 x breadth
    step_to_deck = below_lwl + deck_above_lwl_ft
    main_above = main_total - step_to_deck
    hounds_above = main_above - main_head
    topmast_hounded = 0.60 * main_hounded  # main-top-mast hounded = 0.60 x main hounded
    topmast_pole = 0.28 * topmast_hounded  # head or pole = 0.28 x hounded length
    topmast_hoist = topmast_hounded - main_head  # the doubling is the lower mast head
    boom_ft = 0.87 * lod_ft  # main-boom = 0.87 x length on deck
    gaff_ft = 0.64 * boom_ft  # main-gaff = 0.64 x main-boom
    bowsprit_ft = 0.79 * lod_ft  # bowsprit = 0.79 x length on deck, the whole stick
    bowsprit_housed = 0.60 * beam_ft  # housed from the fore part of the stem = 0.60 x breadth
    bowsprit_out = bowsprit_ft - bowsprit_housed
    # Reefed: a running bowsprit had two or three fid-holes at its heel, its "reefs"; the
    # file takes one reef, a third of the outboard length brought in (judgement: no source
    # in the references gives the reef's depth).
    bowsprit_reefed = bowsprit_out * 2.0 / 3.0
    sq_yard = 0.84 * lod_ft  # square-sail yard = 0.84 x length on deck
    ts_yard = 0.70 * sq_yard  # top-sail yard = 0.70 x square-sail yard
    tg_yard = 0.44 * sq_yard  # top-gallant yard = 0.44 x square-sail yard
    mast_x_ft = 0.101 * lwl_ft  # main-mast before the middle = 0.101 x water-line
    mast_x = round(mast_x_ft * FT, 1)
    stem_x_ft = lwl_ft / 2.0 + 1.0  # the stem head a foot before the water-line's stem
    stem_x = round(stem_x_ft * FT, 1)
    rake = math.tan(math.radians(rake_deg))

    def raked(z_above_deck_ft):
        """x, ft, of a point on the raked mast."""
        return mast_x_ft - rake * z_above_deck_ft

    def m(x_ft):
        return round(x_ft * FT, 1)

    # heights above the deck, ft: the square-sail yard in the doubling just under the cap,
    # above the gaff's peak ("the height of the square-sail-yards will be their diameter
    # above the upper part of the gaff", Fincham art. 89); the topsail yard under the
    # topmast hounds; the topgallant yard near the pole's head
    nock = hounds_above - 0.045 * main_hounded  # the nock below the hounds, as the schooner's
    boom_h = 5.0  # judgement: the boom's jaws 5 ft above the deck, over the counter
    gaff_rise = math.tan(math.radians(27.0))  # Fincham art. 86: gaffs at 25 to 30 degrees
    sq_yard_h = main_above - 0.5
    ts_yard_h = main_above + topmast_hoist - 1.0
    tg_yard_h = main_above + topmast_hoist + topmast_pole - 0.5

    def trapezoid(head_ft, foot_ft, depth_ft):
        return round((head_ft + foot_ft) / 2.0 * depth_ft * FT * FT)

    # the mainsail (Fincham arts. 86, 87; Steel's cutter's mainsail)
    main_foot = 0.92 * boom_ft
    main_head_ft = 0.92 * gaff_ft
    main_hoist = nock - boom_h
    main_area = round(
        (
            (main_foot + main_head_ft) / 2.0 * main_hoist
            + 0.5 * main_head_ft * gaff_rise * main_head_ft
        )
        * FT
        * FT
    )
    main_z = boom_h + 0.45 * main_hoist
    main_centre = round(deck_height + main_z * FT, 1)
    peak_h = nock + main_head_ft * gaff_rise
    # the square sail: as broad as its yard, square in the head and leeches, four-fifths of
    # the mainsail's fore-leech deep (Steel, 'Sloop's square-sail')
    sq_depth = 0.8 * main_hoist
    sq_area = round(0.9 * sq_yard * sq_depth * FT * FT)
    sq_z = sq_yard_h - 0.45 * sq_depth
    sq_centre = round(deck_height + sq_z * FT, 1)
    # the topsail between its yard and the square-sail yardarms; the topgallant above it
    ts_depth = ts_yard_h - sq_yard_h
    ts_area = trapezoid(0.82 * ts_yard, 0.9 * sq_yard, ts_depth)
    ts_z = sq_yard_h + 0.5 * ts_depth
    ts_centre = round(deck_height + ts_z * FT, 1)
    tg_depth = tg_yard_h - ts_yard_h
    tg_area = trapezoid(0.89 * tg_yard, 0.9 * ts_yard, tg_depth)
    tg_z = ts_yard_h + 0.5 * tg_depth
    tg_centre = round(deck_height + tg_z * FT, 1)
    # the gaff topsail: luff up the pole above the gaff's peak, foot along the gaff
    topmast_head = main_above + topmast_hoist + topmast_pole
    gt_area = round(0.5 * main_head_ft * (topmast_head - peak_h) * FT * FT)
    gt_z = main_above + 0.4 * (topmast_hoist + topmast_pole)
    gt_centre = round(deck_height + gt_z * FT, 1)
    # the foresail: a staysail on the forestay from the hounds to the stem head (Fincham
    # art. 87: foot 0.9 of the distance from the stay to the mast, luff 0.85 of the stay,
    # leech 0.8 of the luff); its corners give its area (Heron) and its centre (centroid)
    fs_tack = (stem_x_ft, 1.0)
    fs_head_full = (raked(hounds_above), hounds_above)
    stay_len = math.hypot(fs_head_full[0] - fs_tack[0], fs_head_full[1] - fs_tack[1])
    fs_luff = 0.85 * stay_len
    fs_foot = 0.9 * (stem_x_ft - mast_x_ft)
    fs_leech = 0.8 * fs_luff
    s = (fs_luff + fs_foot + fs_leech) / 2.0
    fs_area = round(math.sqrt(s * (s - fs_luff) * (s - fs_foot) * (s - fs_leech)) * FT * FT)
    fs_head = (
        fs_tack[0] + (fs_head_full[0] - fs_tack[0]) * fs_luff / stay_len,
        fs_tack[1] + (fs_head_full[1] - fs_tack[1]) * fs_luff / stay_len,
    )
    fs_clew = (stem_x_ft - fs_foot, 3.0)
    fs_x = (fs_tack[0] + fs_head[0] + fs_clew[0]) / 3.0
    fs_z = (fs_tack[1] + fs_head[1] + fs_clew[1]) / 3.0
    # the jib: tack 9 in short of the bowsprit end (Fincham art. 87), foot the distance
    # from the tack to the stem, luff 0.8 of the line from the lower mast head (the jib
    # halyard block, at the cap) to the tack; the clew at the stem head. Fincham's 85-ton
    # cutter's second jib is 541 sq ft with its centre 32.8 ft before the middle and 19.5 ft
    # up (p. 67): the check on the figures below.
    jib_tack = (stem_x_ft + bowsprit_out - 0.75, 2.0)
    jib_halyard = (raked(main_above), main_above)
    jib_stay_len = math.hypot(jib_halyard[0] - jib_tack[0], jib_halyard[1] - jib_tack[1])
    jib_luff = 0.8 * jib_stay_len
    jib_head = (
        jib_tack[0] + (jib_halyard[0] - jib_tack[0]) * jib_luff / jib_stay_len,
        jib_tack[1] + (jib_halyard[1] - jib_tack[1]) * jib_luff / jib_stay_len,
    )
    jib_clew = (stem_x_ft, 4.0)
    jib_area = round(
        0.5
        * abs(
            (jib_head[0] - jib_tack[0]) * (jib_clew[1] - jib_tack[1])
            - (jib_head[1] - jib_tack[1]) * (jib_clew[0] - jib_tack[0])
        )
        * FT
        * FT
    )
    jib_x = (jib_tack[0] + jib_head[0] + jib_clew[0]) / 3.0
    jib_z = (jib_tack[1] + jib_head[1] + jib_clew[1]) / 3.0
    prov = " Provisional (truth 9), see gen_ships.py."

    mast = b.spar(
        "main.mast",
        "mast",
        x_m=mast_x,
        rake_deg=rake_deg,
        height_m=ft(main_above),
        rating_kn=design_kn(
            [
                (main_area, main_centre, "gaff"),
                (sq_area, sq_centre, "square"),
                (ts_area, ts_centre, "square"),
                (tg_area, tg_centre, "square"),
                (gt_area, gt_centre, "jibheaded"),
                (fs_area, round(deck_height + fs_z * FT, 1), "jibheaded"),
            ],
            dw["lower"],
        ),
        note=f"the mast (Steel calls a cutter's her main mast): {main_total:.0f} ft heel to "
        f"head, hounded {main_hounded:.0f} ft (Fincham 1843 p. 67, the second revenue "
        f"cruiser: 2.6 x the breadth) with a head 0.23 of that, {main_above:.0f} ft above "
        f"the deck; stepped 0.269 x the breadth below the water-line (Fincham); raking "
        f"{rake_deg} deg, 13 in in 12 ft (Fincham; Steel: 1.5 in to the yard); stationed "
        f"0.101 of the water-line before the middle (Fincham).{prov}",
    )
    topmast = b.spar(
        "main.topmast",
        "topmast",
        steps_on=mast,
        height_m=ft(topmast_hoist),
        rating_kn=design_kn(
            [(ts_area, ts_centre, "square"), (tg_area, tg_centre, "square")], dw["topsail"]
        ),
        note=f"topmast {topmast_hounded + topmast_pole:.0f} ft with its pole: hounded 0.60 of "
        f"the lower mast's hounded length, the pole 0.28 of that (Fincham p. 67); fidded "
        f"above the lower mast head with cross-trees and a cap (Steel 1794: 'sometimes they "
        f"have a common head, like other lower-masts, with cross-trees, cap, and top-mast'), "
        f"hounds {topmast_hoist:.0f} ft above the cap, so that it strikes as a ship's "
        f"topmast does.{prov}",
    )
    pole = b.spar(
        "main.topgallant_mast",
        "topgallant_mast",
        steps_on=topmast,
        height_m=ft(topmast_pole),
        rating_kn=design_kn([(tg_area, tg_centre, "square")], dw["topgallant"]),
        note=f"topgallant 'mast': the {topmast_pole:.0f} ft pole of the topmast, on which the "
        f"topgallant sets (Fincham; as the schooner's), sent down with the topgallant yard "
        f"in a blow.{prov}",
    )
    gaff = b.spar(
        "main.gaff",
        "gaff",
        on=mast,
        length_m=ft(gaff_ft),
        height_m=ft(nock),
        rating_kn=design_kn([(main_area, main_centre, "gaff")], dw["gaff"]),
        note=f"gaff {gaff_ft:.0f} ft, 0.64 of the boom (Fincham p. 67); its jaws at the nock, "
        f"{nock:.0f} ft above the deck, 0.045 of the hounded mast below the hounds (as the "
        "schooner's, after Fincham art. 89).",
    )
    boom = b.spar(
        "main.boom",
        "boom",
        on=mast,
        length_m=ft(boom_ft),
        height_m=ft(boom_h),
        horse_m=round(0.5 * beam, 1),
        rating_kn=design_kn([(main_area, main_centre, "gaff")], dw["gaff"]),
        note=f"boom {boom_ft:.0f} ft, 0.87 of the length on deck (Fincham p. 67), far over "
        f"the counter: the clew of a cutter's mainsail lies 0.2 to 0.3 of the water-line "
        f"abaft the post (Fincham art. 86); {boom_h:.0f} ft above the deck (judgement); "
        "horse_m " + HORSE_NOTE,
    )
    sqy = b.spar(
        "square_sail.yard",
        "yard",
        on=mast,
        length_m=ft(sq_yard),
        height_m=ft(sq_yard_h),
        brace_limit_deg=58,
        rating_kn=design_kn([(sq_area, sq_centre, "square")], dw["square_sail"]),
        note=f"square-sail yard {sq_yard:.0f} ft, 0.84 of the length on deck (Fincham p. 67; "
        "Steel's 'cross-jack' yard of a one-masted vessel), hoisted from the deck by its "
        "halyard to the doubling under the cap, above the gaff's peak (Fincham art. 89). "
        "The type set this sail flying, the yard sent up with it and struck when it came "
        "in; the file crosses it, as a yard the engine can hoist and brace, since a yard "
        "sent up and down with its sail is not a thing the runner has (the schooner's own "
        "bare fore yard, spec M0 to M2 §12 item 7, is the same question left open). Braces "
        "58 deg from square, as the schooner's topsail yard: a long yard, 2.4 breadths, "
        f"against a cutter's few shrouds (judgement, spec 3b §2.1).{prov}",
    )
    sq = b.sail(
        "square_sail",
        "square",
        yard=sqy,
        area_m2=sq_area,
        reef_bands=2,
        x_m=m(raked(sq_z)),
        centre_height_m=sq_centre,
        canvas_no=CUTTER_CANVAS["square_sail"][0],
        cloth_rating_kn=cloth(sq_area, CUTTER_CANVAS["square_sail"][0]),
        note=f"square sail {sq_area} m2 (Steel 1794 p. 124, 'Sloop's square-sail, or "
        f"cross-jack': square in the head and leeches, {sq_depth:.0f} ft deep, four-fifths "
        "of the mainsail's fore-leech; two reef-bands). A fair-wind sail, in the light "
        "sails, not the plain sail." + canvas_note(CUTTER_CANVAS["square_sail"]),
    )
    square_sail_lines(
        b, sq, sqy, CUTTER_ROPE["square_sail"], hoisting=True, reef=True, bowline=True
    )
    tsy = b.spar(
        "topsail.yard",
        "yard",
        on=topmast,
        length_m=ft(ts_yard),
        height_m=ft(ts_yard_h),
        brace_limit_deg=64,
        rating_kn=design_kn(
            [(ts_area, ts_centre, "square"), (tg_area, tg_centre, "square")], dw["topsail"]
        ),
        note=f"topsail yard {ts_yard:.0f} ft, 0.70 of the square-sail yard (Fincham p. 67), "
        "hoisted to the topmast hounds; braces 64 deg from square, as a frigate's topsail "
        "yards (a yard of 1.7 breadths on a narrow topmast rigging; Fincham 1843 art. 102's "
        "two degrees a level aloft would give 60 over the lower yard: judgement, spec 3b "
        f"§2.1).{prov}",
    )
    ts = b.sail(
        "topsail",
        "square",
        yard=tsy,
        area_m2=ts_area,
        reef_bands=1,
        x_m=m(raked(ts_z)),
        centre_height_m=ts_centre,
        canvas_no=CUTTER_CANVAS["topsail"][0],
        cloth_rating_kn=cloth(ts_area, CUTTER_CANVAS["topsail"][0]),
        note=f"topsail {ts_area} m2 between its yard and the square-sail yardarms, "
        f"{ts_depth:.0f} ft deep (Steel 1794 p. 125, 'Sloop's topsail': the depth in the "
        "middle two-thirds of the cross-jack's; one reef-band); x carried aft by the rake."
        + canvas_note(CUTTER_CANVAS["topsail"]),
    )
    square_sail_lines(b, ts, tsy, CUTTER_ROPE["topsail"], hoisting=True, reef=True, bowline=True)
    tgy = b.spar(
        "topgallant.yard",
        "yard",
        on=pole,
        length_m=ft(tg_yard),
        height_m=ft(tg_yard_h),
        brace_limit_deg=66,
        rating_kn=design_kn([(tg_area, tg_centre, "square")], dw["topgallant"]),
        note=f"topgallant yard {tg_yard:.0f} ft, 0.44 of the square-sail yard (Fincham p. 67), "
        "on the pole; braces 66 deg from square, two more than the topsail yard "
        f"(judgement).{prov}",
    )
    tgs = b.sail(
        "topgallant",
        "square",
        yard=tgy,
        area_m2=tg_area,
        x_m=m(raked(tg_z)),
        centre_height_m=tg_centre,
        canvas_no=CUTTER_CANVAS["topgallant"][0],
        cloth_rating_kn=cloth(tg_area, CUTTER_CANVAS["topgallant"][0]),
        note=f"topgallant {tg_area} m2, {tg_depth:.0f} ft deep (Steel 1794 p. 126, 'Sloop's "
        "topgallant-sail': 'from 3 to 5 yards deep'); the lightest sail she has."
        + canvas_note(CUTTER_CANVAS["topgallant"]),
    )
    square_sail_lines(b, tgs, tgy, CUTTER_ROPE["topgallant"], hoisting=True)
    mainsail = b.sail(
        "main.sail",
        "gaff",
        mast=mast,
        gaff=gaff,
        boom=boom,
        area_m2=main_area,
        reef_bands=4,
        x_m=m(raked(main_z) - 0.4 * main_foot),
        centre_height_m=main_centre,
        canvas_no=CUTTER_CANVAS["main.sail"][0],
        cloth_rating_kn=cloth(main_area, CUTTER_CANVAS["main.sail"][0]),
        note=f"mainsail {main_area} m2: foot {main_foot:.0f} ft from clew to mast (0.92 of the "
        f"boom), head {main_head_ft:.0f} ft (0.92 of the gaff, 0.64 of the foot: Fincham art. "
        f"86 gives 0.6 to 0.66, 0.74 in some revenue cruisers), hoist {main_hoist:.0f} ft to "
        f"the nock {nock:.0f} ft above the deck ({(nock + deck_above_lwl_ft) / beam_ft:.2f} "
        "breadths above the water: Fincham art. 86, 2.1 to 2.2 in revenue cruisers), gaff "
        "peaked 27 degrees; four reef-bands (Steel 1794 p. 120, 'Cutter's mainsail'); centre "
        "0.4 of the foot abaft the raked mast. Fincham's 85-ton cutter's mainsail (p. 67) was "
        "1566 sq ft on a yacht's taller mast." + canvas_note(CUTTER_CANVAS["main.sail"]),
    )
    b.line("main.gaff.throat_halyard", "throat_halyard", gaff, rating=rope_kn(3.0, 3))
    b.line("main.gaff.peak_halyard", "peak_halyard", gaff, rating=rope_kn(2.5, 4))
    b.line(
        "main.sail.sheet",
        "sheet",
        mainsail,
        rating=rope_kn(3.5, 3),
        parts=3,
        note="3.5 in, a threefold purchase on the boom (judgement, as the schooner's main sheet).",
    )
    b.line("main.sail.outhaul", "outhaul", mainsail, rating=rope_kn(2.0))
    b.sided("main.gaff.vang", "vang", gaff, rating=rope_kn(2.0))
    gt = b.sail(
        "main.gaff_topsail",
        "jibheaded",
        mast=topmast,
        area_m2=gt_area,
        x_m=m(raked(gt_z) - 0.3 * main_head_ft),
        centre_height_m=gt_centre,
        canvas_no=CUTTER_CANVAS["main.gaff_topsail"][0],
        cloth_rating_kn=cloth(gt_area, CUTTER_CANVAS["main.gaff_topsail"][0]),
        note=f"gaff topsail {gt_area} m2: luff {topmast_head - peak_h:.0f} ft up the pole "
        "above the gaff's peak, foot along the gaff (Steel 1794 p. 126, 'Sloop's gaff "
        "topsail'; Fincham p. 67 gives the type a gaff-topsail yard)."
        + canvas_note(CUTTER_CANVAS["main.gaff_topsail"]),
    )
    b.line("main.gaff_topsail.halyard", "halyard", gt, rating=rope_kn(2.0))
    b.line("main.gaff_topsail.sheet", "sheet", gt, rating=rope_kn(2.0))
    b.line("main.gaff_topsail.tack", "tack", gt, rating=rope_kn(2.0))
    # -- the head: the running bowsprit, the forestay and the jib ------------------------
    bowsprit = b.spar(
        "bowsprit",
        "bowsprit",
        x_m=stem_x,
        length_m=ft(bowsprit_out),
        height_m=1.2,
        running=True,
        housed_length_m=ft(bowsprit_reefed),
        rigged_out=True,
        rating_kn=design_kn(
            [(jib_area, round(deck_height + jib_z * FT, 1), "jibheaded")], dw["lower"]
        ),
        note=f"the running bowsprit: {bowsprit_ft:.0f} ft in all, 0.79 of the length on deck "
        f"(Fincham p. 67), {bowsprit_housed:.0f} ft of it housed (0.60 x the breadth, "
        f"Fincham) and {bowsprit_out:.0f} ft outboard rigged out, nearly horizontal (Steel "
        "1794: cutters' bowsprits 'lie nearly in an horizontal direction'). It runs in and "
        "out on the deck through the gammoning iron by its heel-rope (Steel 1794, HEEL-ROPE: "
        "'to haul out the bowsprits of cutters') and is fidded at its reefs: `running`, and "
        f"`housed_length_m` is its outboard length reefed, {bowsprit_reefed:.0f} ft, a third "
        "in (judgement; the type had two or three reefs); `rigged_out` true is the full "
        "length, the jib's tack at its end. reef_bowsprit.yaml and rig_out_bowsprit.yaml "
        "move it; the jib, whose tack rides the traveller at the end, must be down first "
        f"(spec M5 §23; package 32b).{prov}",
    )
    b.line(
        "bowsprit.heel_rope",
        "outhaul",
        bowsprit,
        rating=rope_kn(3.5, 2),
        note="the heel-rope, the tackle that runs the bowsprit out and in (Steel 1794, "
        "HEEL-ROPE); 3.5 in, two parts (judgement).",
    )
    b.line(
        "fore.stay",
        "stay",
        mast,
        rating=rope_kn(7.0),
        note="the forestay, from the hounds to the stem head; the foresail sets on it with "
        "hanks (Steel 1794, 'Smack's foresail'). 7 in (judgement).",
    )
    b.line(
        "jib.stay",
        "stay",
        topmast,
        rating=rope_kn(4.0),
        note="the topmast stay, from the topmast hounds to the bowsprit end. The jib sets "
        "flying, hoisted by its halyard from the lower mast head with its tack on the "
        "traveller at the bowsprit end (Steel 1794, 'Smack's jib': 'hoists by haliards, "
        "without a stay'); the file names this stay as the line the jib's luff lies along, "
        "as the schooner's flying jib has one, so that the engine and the viewer find its "
        "luff. 4 in (judgement).",
    )
    b.sided(
        "main.shrouds",
        "shroud",
        mast,
        rating=rope_kn(6.0, 4),
        note="4 shrouds of 6 in a side (judgement; Steel's cutter of 200 tons is in his "
        "second volume).",
    )
    b.sided(
        "main.topmast.backstay",
        "backstay",
        topmast,
        rating=rope_kn(3.5, 2),
        note="the runners, a pair (Steel 1794: a cutter's topmast 'two pair of topmast shrouds "
        "and one pair of backstays'); 3.5 in, two parts (judgement).",
    )
    b.line("bobstay", "stay", bowsprit, rating=rope_kn(6.0))
    foresail = b.sail(
        "fore.staysail",
        "jibheaded",
        stay="fore.stay",
        area_m2=fs_area,
        x_m=m(fs_x),
        centre_height_m=round(deck_height + fs_z * FT, 1),
        canvas_no=CUTTER_CANVAS["fore.staysail"][0],
        cloth_rating_kn=cloth(fs_area, CUTTER_CANVAS["fore.staysail"][0]),
        note=f"the foresail, a staysail on the forestay, {fs_area} m2: foot {fs_foot:.0f} ft "
        f"(0.9 of the stay's distance from the mast), luff {fs_luff:.0f} ft (0.85 of the "
        f"{stay_len:.0f} ft stay), leech {fs_leech:.0f} ft (0.8 of the luff): Fincham art. "
        "87; the centre its corners' centroid. Fincham's 85-ton cutter's was 367 sq ft. No "
        "reef bands: Steel's smack's foresail has two 'sometimes', 'but a bonnet is more "
        "frequently used', and the catalogue reefs no jib-headed sail."
        + canvas_note(CUTTER_CANVAS["fore.staysail"]),
    )
    b.line("fore.staysail.halyard", "halyard", foresail, rating=rope_kn(2.5, 2))
    b.sided("fore.staysail.sheet", "sheet", foresail, rating=rope_kn(2.5))
    b.line("fore.staysail.downhaul", "downhaul", foresail, rating=rope_kn(2.0))
    jib = b.sail(
        "jib",
        "jibheaded",
        stay="jib.stay",
        halyard_spar=bowsprit,
        area_m2=jib_area,
        x_m=m(jib_x),
        centre_height_m=round(deck_height + jib_z * FT, 1),
        canvas_no=CUTTER_CANVAS["jib"][0],
        cloth_rating_kn=cloth(jib_area, CUTTER_CANVAS["jib"][0]),
        note=f"the jib, {jib_area} m2 (Fincham art. 87): tack 9 in short of the bowsprit end, "
        f"{jib_tack[0] - stem_x_ft:.0f} ft before the stem "
        f"({(jib_tack[0] - lwl_ft / 2.0) / lwl_ft:.2f} of the water-line; Fincham 0.55 to "
        f"0.6), foot the {jib_tack[0] - stem_x_ft:.0f} ft "
        f"to the stem, luff {jib_luff:.0f} ft (0.8 of the {jib_stay_len:.0f} ft from the "
        "lower mast head to the tack), clew at the stem head; centre the corners' centroid, "
        f"{jib_x - lwl_ft / 2.0:.0f} ft before the middle and {jib_z + deck_above_lwl_ft:.0f} "
        "ft above the water (Fincham's 85-ton cutter's second jib: 541 sq ft, 32.8 ft before "
        "and 19.5 ft up). `halyard_spar` names the bowsprit its tack runs out on: it cannot "
        "be set with the bowsprit reefed (set_jibheaded.yaml), and reefing or rigging out "
        "the bowsprit wants it down (package 32b). No reef bands: the type shifted jibs "
        "rather than reefed them, which the storm jib does here."
        + canvas_note(CUTTER_CANVAS["jib"]),
    )
    b.line("jib.halyard", "halyard", jib, rating=rope_kn(3.0, 2))
    b.sided("jib.sheet", "sheet", jib, rating=rope_kn(3.0))
    b.line("jib.downhaul", "downhaul", jib, rating=rope_kn(2.5))
    b.line(
        "jib.outhaul",
        "outhaul",
        jib,
        rating=rope_kn(2.5),
        note="hauls the traveller, with the jib's tack, out to the bowsprit end (Lever 1808, "
        "'The Jib': the traveller on the boom; judgement for the size).",
    )
    head_sails = [foresail, jib]

    # -- storm canvas (spec 3b §6.4; package 32b) ---------------------------------------
    # The storm trysail: Steel 1794 vol. I, 'Cutter's trysail' (OCR line 14359): "occasionally
    # used, instead of the main-sail, in stormy weather ... In the head of the trysail there
    # are two-fifths of the number of cloths that are in the head of the main-sail: the
    # fore-leech is about three-fourths of the depth of the fore-leech of the main-sail, and
    # the after-leech is one-sixth deeper than the fore-leech ... three reef-bands"; the foot
    # three-fourths of the mainsail's (judgement: Steel gores it "from the tack, leaving two
    # or three square cloths at the clue" and gives no length). Bent to the gaff and boom in
    # place of the mainsail.
    storm_canvas = CUTTER_CANVAS["storm trysail"]
    st_head = 0.4 * main_head_ft
    st_luff = 0.75 * main_hoist
    st_leech = st_luff * 7.0 / 6.0
    st_foot = 0.75 * main_foot
    st_area = round((st_head + st_foot) / 2.0 * (st_luff + st_leech) / 2.0 * FT * FT)
    st_z = boom_h + 0.45 * st_luff
    st = b.sail(
        "storm_trysail",
        "gaff",
        mast=mast,
        gaff=gaff,
        boom=boom,
        area_m2=st_area,
        reef_bands=3,
        x_m=m(raked(st_z) - 0.4 * st_foot),
        centre_height_m=round(deck_height + st_z * FT, 1),
        canvas_no=storm_canvas[0],
        cloth_rating_kn=storm_cloth(st_area),
        bent=False,
        in_place_of="main.sail",
        note=f"storm trysail {st_area} m2 (Steel 1794, 'Cutter's trysail'): head {st_head:.0f} "
        f"ft (two-fifths of the mainsail's), fore-leech {st_luff:.0f} ft (three-fourths of the "
        f"mainsail's), after-leech a sixth deeper, foot {st_foot:.0f} ft (three-fourths of "
        "the mainsail's, judgement); three reef-bands; bent to the gaff and boom in place of "
        "the mainsail; in the sail room." + canvas_note(storm_canvas, storm=True),
    )
    b.line("storm_trysail.sheet", "sheet", st, rating=rope_kn(3.5, 3), parts=3)
    b.line("storm_trysail.outhaul", "outhaul", st, rating=rope_kn(2.0))
    # the storm jib: Steel's sloop's storm jib, two-thirds of the first jib (p. 190); its
    # tack on the traveller run in to the reefed bowsprit's end, so it sets whether the
    # bowsprit is reefed or out, and the file gives it no `halyard_spar`
    sj_area = round(2.0 / 3.0 * jib_area)
    sj_tack_x = stem_x_ft + bowsprit_reefed - 0.75
    sj_x = (sj_tack_x + jib_head[0] + jib_clew[0]) / 3.0
    sj_canvas = CUTTER_CANVAS["storm jib"]
    sj = b.sail(
        "storm_jib",
        "jibheaded",
        stay="jib.stay",
        area_m2=sj_area,
        x_m=m(sj_x),
        centre_height_m=round((deck_height + jib_z * FT) * math.sqrt(2.0 / 3.0), 1),
        canvas_no=sj_canvas[0],
        cloth_rating_kn=storm_cloth(sj_area),
        bent=False,
        in_place_of="jib",
        note=f"storm jib {sj_area} m2, two-thirds of the jib (Steel 1794 p. 190, the sloop's "
        f"jibs); its tack on the traveller at the reefed bowsprit's end, {bowsprit_reefed:.0f} "
        "ft before the stem, its centre lower as its size is smaller (judgement); set in place "
        "of the jib, with the bowsprit reefed or not; in the sail room."
        + canvas_note(sj_canvas, storm=True),
    )
    b.line("storm_jib.halyard", "halyard", sj, rating=rope_kn(3.0, 2))
    b.sided("storm_jib.sheet", "sheet", sj, rating=rope_kn(3.0))
    b.line("storm_jib.downhaul", "downhaul", sj, rating=rope_kn(2.5))
    storm = [st, sj]

    # groups: the plain sail of a cutter is her mainsail, foresail, jib and topsail (spec M5
    # §23); the square sail, the topgallant and the gaff topsail are her light canvas
    b.group("courses", [sq])
    b.group("topsails", [ts])
    b.group("topgallants", [tgs])
    b.group("square sails", [sq, ts, tgs])
    b.group("headsails", head_sails)
    b.group("jibs", [jib])
    b.group("staysails", [foresail])
    b.group("gaff sails", [mainsail])
    b.group("fore-and-aft sails", head_sails + [mainsail, gt])
    b.group("light sails", [gt, tgs, sq])
    b.group("plain sail", [mainsail, foresail, jib, ts])
    b.group("all sail", [mainsail, gt, sq, ts, tgs, foresail, jib])
    b.group("yards", [sqy, tsy, tgy])
    b.group("main yards", [sqy, tsy, tgy])
    b.group("lower yards", [sqy])
    b.group("topsail yards", [tsy])
    b.group("topgallant yards", [tgy])
    b.group("lower masts", [mast])
    b.group("topmasts", [topmast])
    b.group("topgallant masts", [pole])
    b.group("storm canvas", storm)
    # the square sail's bowlines and the topsail's, as the schooner's fore bowlines
    b.group("square sail bowlines", [f"square_sail.bowline.{s}" for s in SIDES])
    b.group("topsail bowlines", [f"topsail.bowline.{s}" for s in SIDES])
    b.alias("square sail bowline", "square sail bowlines")
    b.alias("topsail bowline", "topsail bowlines")
    b.alias("top bowline", "topsail bowlines")
    # aliases: what a cutter's master says (Steel 1794; Fincham 1843; Falconer 1780)
    b.alias("mainsail", "main.sail")
    b.alias("the main", "main.sail")
    b.alias("foresail", "fore.staysail")
    b.alias("the fore", "fore.staysail")
    # Steel's names, with the article so that the log keeps the id's words (an alias
    # beginning "the" is read but not written): the crossjack is the square sail
    b.alias("the crossjack", "square_sail")
    b.alias("the crossjack yard", "square_sail.yard")
    b.alias("the main topsail", "topsail")
    b.alias("the main topgallant", "topgallant")
    b.alias("gaff topsail", "main.gaff_topsail")
    b.alias("trysail", "storm_trysail")
    b.alias("storm mainsail", "storm_trysail")
    b.alias("head sails", "headsails")
    b.alias("topgallant sails", "topgallants")
    b.alias("the mast", "main.mast")
    b.alias("main mast", "main.mast")
    ground_tackle_for(b, burthen, beam_ft, draught_ft)
    cutter_crew(b)
    cutter_armament(b, deck_height)
    hold_for(b, burthen, False, "a revenue cutter's hold less her own stores: judgement")
    b.pumps(PUMPS_NOTE, pump_entries(0, 2, ["the starboard pump", "the larboard pump"]))
    b.boats(
        BOATS_NOTE,
        boat_entries(
            lod_ft,
            False,
            [
                (
                    "boat",
                    "yawl",
                    "the boat",
                    1.0,
                    "The cutter's boat, a yawl of four oars (Falconer, YAWL), on the deck "
                    "amidships.",
                    "data/ships/boat-yawl-16.yaml",
                ),
                (
                    "punt",
                    "punt",
                    "the punt",
                    0.75,
                    "A punt for the pilot and the shore (judgement).",
                ),
            ],
        ),
    )
    b.dump(
        os.path.join(out_dir, "cutter.yaml"),
        "# The cutter: Sherbourne, H.M. armed cutter of 1763 (Slade; Woolwich), the Channel's\n"
        "# revenue cutter, 85 tons, 54 ft 6 in on deck by 19 ft (the kit's manual as the owner\n"
        "# noted it; docs/design/VesselCandidates.md). Generated by tools/gen_ships.py; edit\n"
        "# that script and rerun, do not edit this file. Spars: Fincham 1843, 'Proportions for\n"
        "# the Masts, Booms, &c. of Cutters' (p. 67, the second revenue cruiser) and his rules\n"
        "# for cutters' sails (arts. 86, 87, pp. 35 to 36); sails: Steel 1794 vol. I, the sloop's\n"
        "# and cutter's sails of his sail-making chapter; rope: Luce 1866 ch. IV; the running\n"
        "# bowsprit: Steel 1794 (HEEL-ROPE) and Lever 1808 (the traveller). Spar ratings are\n"
        "# provisional, set for truth 9 with the M1 sail curves; see the script. Cloth ratings\n"
        "# from the canvas number by Luce App. E. Units: metres, m2, kg, kN. Comments mark\n"
        "# judgements. Package 32b (spec M5 §23): no engine change but the running bowsprit.\n",
    )


def cutter_crew(b):
    b.crew(
        [
            (
                ("complement",),
                30,
                "Thirty: the kit's manual's complement for Sherbourne (Winfield not reached).",
            ),
            (("names",), "english", "A revenue crew: the english list in data/crew/names.yaml."),
            (
                ("stations", "forecastle"),
                8,
                "Hands per station, both watches together; a cutter has no tops and no "
                "marines, and her hands work aloft from the deck stations (spec M3 2.3). "
                "Forecastlemen, for the head sails and the bowsprit: 8, judgement.",
            ),
            (
                ("stations", "afterguard"),
                10,
                "Afterguard, at the main sheet and the boom: 10, judgement.",
            ),
            (("stations", "waisters"), 6, "Waisters: 6, judgement."),
            (("stations", "idlers"), 3, "Idlers: the trades below (spec M3 2.3)."),
            (
                ("ratings", "able"),
                0.6,
                "Share of the seamen by rating: judgement. A revenue cutter's crew were "
                "Channel seamen, mostly able. Able: 0.60.",
            ),
            (("ratings", "ordinary"), 0.3, "Ordinary: 0.30, judgement."),
            (("ratings", "landsman"), 0.1, "Landsmen: 0.10, judgement."),
        ]
        + [
            (
                ("posts", post),
                None,
                "Station holders by post (spec M3 2.3): a revenue cutter's master (her "
                "commander), his mate and the boatswain; names are drawn at muster."
                if i == 0
                else None,
            )
            for i, post in enumerate(CUTTER_POSTS)
        ]
        + [
            (
                ("idlers_by_trade", "cook"),
                1,
                "How the idlers are made up (spec M3 2.3). The cook: 1, judgement.",
            ),
            (("idlers_by_trade", "steward"), 1, "A steward: 1, judgement."),
            (("idlers_by_trade", "carpenter's crew"), 1, "A carpenter: 1, judgement."),
            (
                ("stores", "water_tons"),
                4,
                "Stores for a cruise of the Channel (spec M3 2.3). Water for a month: 30 "
                "men at a gallon a day is about 4 tons (judgement).",
            ),
            (("stores", "provisions_days"), 30, "Provisions: a month (judgement)."),
            (("stores", "spare_spars"), {}, None),  # the booms, by class: below
            (("stores", "cordage_fathoms"), 80, "Spare rope (judgement)."),
            (
                ("stores", "shot_plugs"),
                8,
                SHOT_PLUGS_NOTE + " A cutter's 8.",
            ),
            *ration_entries("a revenue cruiser victualled as the King's ships (judgement)"),
        ]
    )
    # The people (package 35, spec M5 §22): a boy of the afterguard carries the word
    # (judgement: a revenue cutter's company had no midshipman). The roles and their notes
    # are the wardroom file's (package 40).
    b.people(
        "The named people beyond the posts (package 35, spec M5 §22); see tools/gen_ships.py.",
        CUTTER_DRAWN,
    )
    # The booms (package 30b): a spare topmast and a spare topsail yard, the two spars a
    # cutter could shift at sea (judgement after Luce 1866 ch. XVII, 'Stowing Booms', as
    # the schooner's); the bowsprit and the boom are the dockyard's.
    b.spare_spars(
        "The booms: the spare spars by class (judgement after Luce 1866 ch. XVII, 'Stowing "
        "Booms'); see tools/gen_ships.py.",
        [
            ("topmast", 1, "A spare topmast (judgement, after Luce 1866)."),
            ("yard", 1, "A spare topsail yard (judgement, after Luce 1866)."),
        ],
    )
    # The sail room (spec 3b §6.3): a spare jib and mainsail, the sails a cutter could
    # least do without (spec M5 §23; judgement), with her storm canvas, one each.
    b.sail_room(
        "The sail room (spec 3b §6.3), every sail new; see tools/gen_ships.py.",
        [
            (
                "jib",
                CUTTER_CANVAS["jib"][0],
                "A spare jib and mainsail (spec M5 §23, judgement).",
            ),
            ("main.sail", CUTTER_CANVAS["main.sail"][0], None),
            (
                "storm_trysail",
                CUTTER_CANVAS["storm trysail"][0],
                "Storm canvas, one of each (spec 3b §6.4, judgement).",
            ),
            ("storm_jib", CUTTER_CANVAS["storm jib"][0], None),
        ],
    )


# ---------------------------------------------------------------------------
# The brig: H.M. brig-sloop Harpy, 1796, Diligence class (package 32b; spec M5 §25)
# ---------------------------------------------------------------------------
#
# Sources. The hull from the kit's manual as the owner noted it (VesselCandidates.md;
# Winfield's 1793 to 1817 volume and the RMG draught were not reachable): 316 tons
# burthen, 95 ft 0 in on the gun deck, 75 ft 1 5/8 in on the keel, 28 ft 1 1/2 in extreme
# breadth, 12 ft 0 1/2 in depth in hold, complement 121, sixteen 32-pounder carronades and
# two 6-pounder chase guns. The keel, breadth and burthen agree by the Navy's rule
# (75.14 x 28.125 x 14.06 / 94 = 316.1), which is the check the manual's figures pass.
#
# The spars by Fincham 1843, 'On Masting Brigs', pp. 82 to 83 (the general observations:
# the brigs of war derived from the cutter, their masts further aft than a ship's, "the
# main-mast is, in general, [.147] abaft, and the fore-mast .331 before the middle of the
# water-line", the centre of effort of the 18-gun brigs .026 of the water-line before the
# middle) and the table on p. 88, 'Tables showing the Proportions for the lengths of
# Masts, Yards, &c., with the position of the Masts and Sails, as given to Brigs': four
# columns, two brigs of war (100 ft on deck by 30.5 ft, the 18-gun brig's size; 90 ft by
# 24.5 ft), a yacht and a Swedish brig. The first brig of war's column is taken, the
# nearest in form to a brig-sloop of 95 ft, and the second is the check. Steel 1794 vol. I
# on brigs (OCR line 1902): "the main-mast placed about two-thirds of their whole length
# abaft the head of the stem, and the foremast three twentieths ... The main-mast inclines
# aft at the head ... three quarters of an inch in every yard of its length; the foremast a
# full eighth part of an inch", the check on Fincham's positions; his mast table for a brig
# of 200 tons (line 5358) lists a topgallant-royal mast, so the royals are hers by her
# date; his sail-making chapter: "The sails of a brig with 2 masts are also similar to
# those on the main and fore masts of a ship, excepting the main sail, which is set in the
# plane of her keel, and is extended by a gaff at the head and a boom at the foot" (line
# 9825), and 'A brig's mainsail' (p. 119). Luce 1866 ch. VII's proportions, the frigate's
# rules, are the check on Fincham's brig (a main mast of (LWL + breadth)/2 = 58 ft against
# Fincham's 65; topmast 3/5 of the main; yards as the frigate's).

BRIG_CANVAS: dict[str, tuple[int, str]] = {
    k: FRIGATE_CANVAS[k]
    for k in (
        "fore.course",
        "main.course",
        "fore.topsail",
        "main.topsail",
        "fore.topgallant",
        "main.topgallant",
        "fore.royal",
        "main.royal",
        "fore.topmast_staysail",
        "jib",
        "flying_jib",
        "main.topmast_staysail",
        # package 57: Steel's own numbers for the brig's staysails, which were judgement
        # before (No. 5 for the main staysail, No. 7 for the main topgallant)
        "main.staysail",
        "middle_staysail",
        "main.topgallant_staysail",
        "lower studding",
        "topmast studding",
        "topgallant studding",
        "storm",
    )
}
BRIG_CANVAS.update(
    {
        "main.spanker": (
            5,
            f"{STEEL_SM} p. 119, 'A brig's mainsail' (the boom mainsail on the gaff and boom): "
            "'made of canvas No. 5 or 6', the heavier taken; a brig's is lighter than a "
            f"ship's spanker of No. 2 ({LUCE_171})",
        ),
    }
)

# Rope sizes for a brig of 316 tons: the frigate's establishment (judgement, as the
# frigate's own) scaled by 0.8, the fore gear 0.92 of the main's (judgement).
BRIG_ROPE_SCALE = 0.8
BRIG_MAST_ROPE_FACTOR = {"fore": 0.92, "main": 1.0}


def brig(out_dir="data/ships", merchant=False):
    """The brig: H.M. brig-sloop Harpy (`brig.yaml`), or with `merchant` the trade's brig of
    her lines and rig (`merchant-brig.yaml`, package 68): the same hull and spars, a
    master's and mates' company, a merchant's stores, the trader's hold and boats."""
    dw = DESIGN_WIND_KN
    # -- hull ---------------------------------------------------------------------------
    gundeck_ft = 95.0
    keel_ft = 75.135
    beam_ft = 28.125
    burthen = keel_ft * beam_ft * beam_ft / 2.0 / 94.0  # 316.1 tons by the Navy's rule
    lwl_ft = round(0.93 * gundeck_ft)  # judgement: 0.93 of the deck, 88 ft (keel 75 ft)
    # Draught: the 12 ft 0.5 in depth of hold to a draught, as the frigate's: 10.5 ft
    # forward and 12.5 ft aft stored for sea (judgement; a brig-sloop of the class drew
    # about 11 to 13 ft aft)
    draught_ft = 11.5
    lwl, beam, draught = ft(lwl_ft), ft(beam_ft), ft(draught_ft)
    # Displacement: Cb 0.50 (judgement: a sloop's block, fuller aft than a frigate's 0.55
    # is fine, shallower): about 410 t, 1.3 x the burthen
    displacement = round(lwl * beam * draught * 0.50 * 1025.0, -3)
    deck_height = 1.5  # a flush-decked brig-sloop's deck about 5 ft above the load line
    deck_above_lwl_ft = deck_height / FT
    mast_x_ft = {"fore": 0.331 * lwl_ft, "main": -0.147 * lwl_ft}  # Fincham p. 88
    mast_x = {k: round(v * FT, 1) for k, v in mast_x_ft.items()}
    rake_deg = {  # Fincham p. 88: main 10 in, fore 3 in, in 12 ft
        "main": round(math.degrees(math.atan(10.0 / 144.0)), 1),
        "fore": round(math.degrees(math.atan(3.0 / 144.0)), 1),
    }

    b = Builder(
        "Harpy",
        "brig",
        "H.M. brig-sloop Harpy of the Diligence class (launched 1796, sold 1817): 316 tons "
        "burthen, 95 ft on the gun deck, 75 ft 1 5/8 in on the keel, 28 ft 1 1/2 in beam, "
        "12 ft 0 1/2 in in the hold; sixteen 32-pounder carronades and two 6-pounder chase "
        "guns (the armament below, package 70). The Navy's brig; the merchant brig is "
        "her second description at far detail (package 36). Hull from the kit's manual "
        "(Winfield and the Greenwich draught not reached); spars by Fincham 1843's table of "
        "proportions for brigs of war (p. 88) checked against Luce 1866 ch. VII; sails by "
        "Steel 1794; see tools/gen_ships.py for every rule.",
        {
            "length_waterline_m": lwl,
            "beam_m": beam,
            "draught_m": draught,
            "displacement_kg": displacement,
            "gm_m": 0.95,
            "clr_x_m": 0.5,
            "lateral_area_m2": round(lwl * draught * 0.85, -1),
            "hull_speed_kn": 11.5,
            "deck_height_m": deck_height,
            "rudder": {"area_m2": 3.0, "max_angle_deg": 35, "rate_deg_s": 3.5, "span_m": 3.7},
        },
        {
            "length_waterline_m": f"{lwl_ft:.0f} ft: judgement, 0.93 of the 95 ft gun deck "
            f"(keel 75 ft 1 5/8 in), a brig-sloop's ends raking more than a frigate's.",
            "beam_m": "28 ft 1 1/2 in extreme breadth (the kit's manual; Winfield not reached).",
            "draught_m": f"{draught_ft:.1f} ft mean, judgement: 10.5 ft forward, 12.5 ft aft "
            "stored for sea, from the 12 ft depth in hold as the frigate's is derived.",
            "displacement_kg": "LWL x beam x draught x Cb 0.50 x 1025: about 410 t, 1.3 x "
            f"the {burthen:.0f} tons burthen (Cb judgement: a sloop's block).",
            "gm_m": "3 ft 1 in: judgement, the frigate's 4 ft 3 in scaled by the breadth "
            "(28.1 to 38.3 ft); a brig-sloop was tenderer than a frigate.",
            "clr_x_m": "Judgement, set as the schooner's and the frigate's were: the centre "
            "of pressure before the middle so that she carries a little weather helm "
            "close-hauled and a few degrees on a beam reach in 15 kn (measured; "
            "docs/dev/TuningNotes.md, package 32b). Fincham p. 83 puts a brig of war's "
            "centre of effort 0.026 of the water-line before the middle, with the masts "
            "further aft than a ship's.",
            "lateral_area_m2": "LWL x draught x 0.85 for the fullness of the profile.",
            "hull_speed_kn": "The brig-sloops' recorded best is 10 to 11 knots (judgement, "
            f"between the schooner's 11.5 and the frigate's 13); 1.34 sqrt({lwl_ft:.0f} ft) "
            "= 12.6 is a modern yacht's figure.",
            "deck_height_m": "A flush deck about 5 ft above the load line (judgement).",
            "rudder": "Blade about 12 ft by 3 ft (span_m its depth, 12 ft; package 32e); 35 "
            "degrees is the period stop (judgement).",
        },
    )

    # -- spars in feet by Fincham's table (p. 88), the first brig of war's column ---------
    main_hounded = 1.93 * beam_ft  # main-mast hounded = 1.93 x breadth
    main_head = 0.1933 * main_hounded  # headed = 0.1933 x hounded length
    fore_hounded = 0.87 * main_hounded  # fore-mast hounded = 0.87 x main-mast hounded
    fore_head = 0.1933 * fore_hounded
    main_top_hounded = 1.13 * beam_ft  # main-top-mast hounded = 1.13 x breadth
    main_top_head = 0.1585 * main_top_hounded
    fore_top_hounded = 0.945 * main_top_hounded  # fore-top-mast hounded = 0.945 x main's
    fore_top_head = 0.1585 * fore_top_hounded
    tg_hounded = 0.765 * beam_ft  # top-gallant-mast hounded = 0.765 x breadth, fore as main
    tg_pole = 0.75 * tg_hounded  # pole = 0.75 x hounded length: the royal mast
    below_lwl = {"main": 0.245 * beam_ft, "fore": 0.2 * beam_ft}  # Fincham p. 88
    bowsprit_ft = 0.886 * fore_hounded  # bowsprit = 0.886 x fore-mast hounded, the whole
    bowsprit_housed = 0.5 * beam_ft  # housed from the fore part of the stem = 0.5 x breadth
    bowsprit_out = bowsprit_ft - bowsprit_housed
    jib_boom_ft = 0.62 * bowsprit_ft  # jib-boom = 0.62 x bowsprit
    jib_boom_out = jib_boom_ft * 7.0 / 12.0  # 7/12 of it outboard (Luce, as the frigate's)
    flying_ft = 1.22 * jib_boom_ft  # flying jib-boom = 1.22 x jib-boom, lying along it
    flying_out = 0.5 * flying_ft  # half of it beyond the jib-boom end (judgement)
    main_yard = 0.546 * gundeck_ft  # main-yard = 0.546 x length; fore-yard = main-yard
    topsail_yard = 0.769 * main_yard  # top-sail-yards = 0.769 x main-yard, fore as main
    tg_yard = 0.492 * main_yard  # top-gallant-yards = 0.492 x main-yard
    royal_yard = 0.712 * tg_yard  # royal-yards = 0.712 x top-gallant-yard
    boom_ft = 0.58 * gundeck_ft  # main-boom = 0.58 x length
    gaff_ft = 0.586 * boom_ft  # main-gaff = 0.586 x main-boom
    swing_boom = 0.6 * main_yard  # swing-booms (the lower studding sail booms) = 0.6 x lower yards

    geom = {}
    for name in ("fore", "main"):
        hounded = main_hounded if name == "main" else fore_hounded
        head = main_head if name == "main" else fore_head
        step_to_deck = below_lwl[name] + deck_above_lwl_ft
        above = hounded + head - step_to_deck
        t_hounded = main_top_hounded if name == "main" else fore_top_hounded
        t_head = main_top_head if name == "main" else fore_top_head
        t_hoist = t_hounded - head  # the doubling is the lower mast head
        g_hoist = tg_hounded - t_head
        r_hoist = tg_pole - 1.0  # the royal yard hoists to a foot below the pole's head
        geom[name] = {
            "hounded": hounded,
            "head": head,
            "above": above,
            "hounds": above - head,
            "t_len": t_hounded + t_head,
            "t_hoist": t_hoist,
            "g_hoist": g_hoist,
            "r_hoist": r_hoist,
            "yard": main_yard,
            "topsail_yard": topsail_yard,
            "tg_yard": tg_yard,
            "royal_yard": royal_yard,
            "yard_h": above - head - 2.0,
            "topsail_h": above + t_hoist - 1.0,
            "tg_h": above + t_hoist + g_hoist - 1.0,
            "royal_h": above + t_hoist + g_hoist + r_hoist - 0.5,
        }

    def trapezoid(head_ft, foot_ft, depth_ft):
        return round((head_ft + foot_ft) / 2.0 * depth_ft * FT * FT)

    # sail areas (m2) and centres (m above water) from the spars, as the frigate's
    areas = {}
    for name, g in geom.items():
        levels = {}
        depth = 0.42 * g["yard"]  # the drop of a course is 0.42 of its yard (as the frigate's)
        levels["course"] = (
            trapezoid(0.9 * g["yard"], 0.9 * g["yard"], depth),
            round(deck_height + (g["yard_h"] - 0.45 * depth) * FT, 1),
        )
        depth = g["topsail_h"] - g["yard_h"]
        levels["topsail"] = (
            trapezoid(0.82 * g["topsail_yard"], 0.9 * g["yard"], depth),
            round(deck_height + (g["yard_h"] + 0.5 * depth) * FT, 1),
        )
        depth = g["tg_h"] - g["topsail_h"]
        levels["topgallant"] = (
            trapezoid(0.89 * g["tg_yard"], 0.9 * g["topsail_yard"], depth),
            round(deck_height + (g["topsail_h"] + 0.5 * depth) * FT, 1),
        )
        depth = g["royal_h"] - g["tg_h"]
        levels["royal"] = (
            trapezoid(0.89 * g["royal_yard"], 0.9 * g["tg_yard"], depth),
            round(deck_height + (g["tg_h"] + 0.5 * depth) * FT, 1),
        )
        areas[name] = levels

    # the spanker (Steel's brig's mainsail): its fore-leech nearly the main mast from the
    # hounds to the boom, the after-leech a third deeper, the head to within 9 in of the
    # gaff's cleats, the foot to within 18 in of the boom's sheave (Steel 1794 p. 119)
    gm = geom["main"]
    boom_h = 6.0  # judgement: the boom's jaws 6 ft above the deck, over the taffrail
    sp_hoist = gm["hounds"] - boom_h
    sp_head = gaff_ft - 0.75
    sp_foot = boom_ft - 1.5
    sp_rise = sp_hoist / 3.0  # the after-leech a third deeper: the gaff's peak that much up
    sp_area = round(((sp_foot + sp_head) / 2.0 * sp_hoist + 0.5 * sp_head * sp_rise) * FT * FT)
    sp_z = boom_h + 0.45 * sp_hoist
    sp_centre = round(deck_height + sp_z * FT, 1)

    stuns_area = {}
    for name in ("fore", "main"):
        g = geom[name]
        stuns_area[name] = {
            "lower": round(0.4 * g["yard"] * 0.9 * 0.42 * g["yard"] * FT * FT),
            "topmast": round(0.4 * g["topsail_yard"] * (g["topsail_h"] - g["yard_h"]) * FT * FT),
            "topgallant": round(0.4 * g["tg_yard"] * (g["tg_h"] - g["topsail_h"]) * FT * FT),
        }

    # Brace limits, degrees from square (spec 3b §2.1): as the frigate's, from Fincham 1843
    # art. 102 (the long ships' lower yards 61 to 67 from square), less two for a short
    # ship whose lower yards are long for her breadth (a brig's main yard 1.85 breadths,
    # a frigate's 2.1; judgement): main 62, fore 60, two degrees a level aloft.
    plans = {
        "fore": [("course", 60), ("topsail", 62), ("topgallant", 64), ("royal", 66)],
        "main": [("course", 62), ("topsail", 64), ("topgallant", 66), ("royal", 68)],
    }
    yards_by_level = {"course": [], "topsail": [], "topgallant": [], "royal": []}
    sails_by_level = {"course": [], "topsail": [], "topgallant": [], "royal": []}
    yard_lengths = {
        "course": "yard",
        "topsail": "topsail_yard",
        "topgallant": "tg_yard",
        "royal": "royal_yard",
    }
    yard_heights = {
        "course": "yard_h",
        "topsail": "topsail_h",
        "topgallant": "tg_h",
        "royal": "royal_h",
    }
    level_of_spar = {
        "course": "lower",
        "topsail": "topsail",
        "topgallant": "topgallant",
        "royal": "royal",
    }
    mast_rule = {
        "main": "Fincham p. 88: hounded 1.93 x the breadth, the head 0.1933 of that",
        "fore": "Fincham p. 88: hounded 0.87 of the main's, the head 0.1933 of that",
    }
    prov = " Provisional (truth 9), see gen_ships.py."
    for name in ("fore", "main"):
        g = geom[name]
        x = mast_x[name]
        lv = areas[name]
        carried = {
            level: [(lv[lev][0], lv[lev][1], "square") for lev in lv if lev in above_levels]
            for level, above_levels in (
                ("lower", ("course", "topsail", "topgallant", "royal")),
                ("topsail", ("topsail", "topgallant", "royal")),
                ("topgallant", ("topgallant", "royal")),
                ("royal", ("royal",)),
            )
        }
        if name == "main":
            carried["lower"].append((sp_area, sp_centre, "gaff"))
        lower = b.spar(
            f"{name}.mast",
            "mast",
            x_m=x,
            rake_deg=rake_deg[name],
            height_m=ft(g["above"]),
            rating_kn=design_kn(carried["lower"], dw["lower"]),
            note=f"{name} lower mast: {g['hounded'] + g['head']:.0f} ft heel to head "
            f"({mast_rule[name]}), {g['above']:.0f} ft above the deck, stepped "
            f"{below_lwl[name]:.1f} ft below the water-line (Fincham); raking "
            f"{rake_deg[name]} deg (Fincham p. 88: {'10' if name == 'main' else '3'} in in "
            f"12 ft); stationed {abs(mast_x_ft[name]) / lwl_ft:.3f} of the water-line "
            f"{'abaft' if name == 'main' else 'before'} the middle (Fincham pp. 83, 88; Steel "
            "1794: the main two-thirds of the length abaft the stem, the fore three "
            f"twentieths).{prov}",
        )
        top = b.spar(
            f"{name}.topmast",
            "topmast",
            steps_on=lower,
            height_m=ft(g["t_hoist"]),
            rating_kn=design_kn(carried["topsail"], dw["topsail"]),
            note=f"{name} topmast: {g['t_len']:.0f} ft (Fincham p. 88: the main's hounded "
            "1.13 x the breadth, the fore's 0.945 of the main's, the head 0.1585 of the "
            f"hounded length), {g['t_hoist']:.0f} ft of it above the lower cap.{prov}",
        )
        tg = b.spar(
            f"{name}.topgallant_mast",
            "topgallant_mast",
            steps_on=top,
            height_m=ft(g["g_hoist"]),
            rating_kn=design_kn(carried["topgallant"], dw["topgallant"]),
            note=f"{name} topgallant mast: hounded {tg_hounded:.0f} ft, 0.765 x the breadth "
            f"(Fincham p. 88), {g['g_hoist']:.0f} ft above the topmast cap.{prov}",
        )
        royal = b.spar(
            f"{name}.royal_mast",
            "royal_mast",
            steps_on=tg,
            height_m=ft(g["r_hoist"]),
            rating_kn=design_kn(carried["royal"], dw["royal"]),
            note=f"{name} royal mast: the topgallant mast's pole, {tg_pole:.0f} ft, 0.75 of "
            "its hounded length (Fincham p. 88), on which the royal sets; Steel 1794's brig of "
            "200 tons carries a topgallant-royal mast, so the royals are hers by her date "
            f"(spec M5 §25).{prov}",
        )
        on_spar = {"course": lower, "topsail": top, "topgallant": tg, "royal": royal}
        for level, limit in plans[name]:
            yard_id = f"{name}.{level}.yard" if level != "course" else f"{name}.yard"
            sail_id = f"{name}.{level}" if level != "course" else f"{name}.course"
            area, centre = lv[level]
            rule = {
                "course": "0.546 of the length on deck, the fore yard as the main (Fincham p. "
                "88; Luce's 10/11 of a (LWL + breadth)/2 main mast gives 53 ft)",
                "topsail": "0.769 of the lower yard (Fincham p. 88; Luce 3/4)",
                "topgallant": "0.492 of the lower yard (Fincham p. 88; Luce 9/14 of the "
                "topsail yard gives 26 ft)",
                "royal": "0.712 of the topgallant yard (Fincham p. 88)",
            }[level]
            yard = b.spar(
                yard_id,
                "yard",
                on=on_spar[level],
                length_m=ft(g[yard_lengths[level]]),
                height_m=ft(g[yard_heights[level]]),
                brace_limit_deg=limit,
                rating_kn=design_kn(carried[level_of_spar[level]], dw[level_of_spar[level]]),
                note=f"{name} {level} yard {g[yard_lengths[level]]:.0f} ft, {rule}; braces "
                f"{limit} deg from square (Fincham 1843 art. 102 less two for a short ship, "
                f"judgement{'' if level == 'course' else ', two degrees a level aloft'}).{prov}",
            )
            reef = {"course": 1, "topsail": 3, "topgallant": 0, "royal": 0}[level]
            canvas = BRIG_CANVAS[sail_id]
            sail = b.sail(
                sail_id,
                "square",
                yard=yard,
                area_m2=area,
                reef_bands=reef,
                flying=True if level == "royal" else None,  # package 57, as the frigate's
                x_m=raked_x(x, rake_deg[name], centre, deck_height),
                centre_height_m=centre,
                canvas_no=canvas[0],
                cloth_rating_kn=cloth(area, canvas[0]),
                note=f"{name} {level}: {area} m2 between its yard and the yardarms below "
                f"(head {0.9 if level == 'course' else (0.82 if level == 'topsail' else 0.89):.2f} "
                "of the yard), as the frigate's; Steel 1794: a brig's sails 'similar to those "
                "on the main and fore masts of a ship'." + canvas_note(canvas),
            )
            factor = BRIG_MAST_ROPE_FACTOR[name] * BRIG_ROPE_SCALE
            sizes = {cls: quarter(c * factor) for cls, c in FRIGATE_ROPE[level].items()}
            square_sail_lines(
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
        b.sided(
            f"{name}.shrouds",
            "shroud",
            lower,
            rating=rope_kn(7.5, 5),
            note="5 shrouds of 7.5 in a side (Luce 1866 ch. VIII: first rates 10 1/2 in, one "
            "inch less per class; judgement for a sloop; Kipping 1854: 'brigs have four pair "
            "of shrouds forward').",
        )
        b.sided(f"{name}.topmast.backstay", "backstay", top, rating=rope_kn(5.0, 2))

    # the spanker on the main: Steel's brig's mainsail, on the gaff and boom
    g = geom["main"]
    gaff = b.spar(
        "main.gaff",
        "gaff",
        on="main.mast",
        length_m=ft(gaff_ft),
        height_m=ft(g["hounds"] - 1.0),
        rating_kn=design_kn([(sp_area, sp_centre, "gaff")], dw["gaff"]),
        note=f"main gaff {gaff_ft:.0f} ft, 0.586 of the boom (Fincham p. 88); its jaws under "
        "the hounds (Steel 1794 p. 119: the fore-leech 'nearly the length of the main-mast "
        "from the under part of the hounds to the boom').",
    )
    boom = b.spar(
        "main.boom",
        "boom",
        on="main.mast",
        length_m=ft(boom_ft),
        height_m=ft(boom_h),
        horse_m=round(0.5 * beam, 1),
        rating_kn=design_kn([(sp_area, sp_centre, "gaff")], dw["gaff"]),
        note=f"main boom {boom_ft:.0f} ft, 0.58 of the length on deck (Fincham p. 88; Luce's "
        f"half the main mast gives 32 ft, a ship's spanker boom), {boom_h:.0f} ft above the "
        "deck (judgement); horse_m " + HORSE_NOTE,
    )
    spanker = b.sail(
        "main.spanker",
        "gaff",
        mast="main.mast",
        gaff=gaff,
        boom=boom,
        area_m2=sp_area,
        reef_bands=3,
        x_m=round(
            raked_x(mast_x["main"], rake_deg["main"], sp_centre, deck_height) - 0.4 * sp_foot * FT,
            1,
        ),
        centre_height_m=sp_centre,
        canvas_no=BRIG_CANVAS["main.spanker"][0],
        cloth_rating_kn=cloth(sp_area, BRIG_CANVAS["main.spanker"][0]),
        note=f"the spanker, a brig's boom mainsail, {sp_area} m2 (Steel 1794 p. 119, 'A "
        f"brig's mainsail'): fore-leech {sp_hoist:.0f} ft, the main mast from the hounds to "
        f"the boom, after-leech a third deeper, head {sp_head:.0f} ft to within 9 in of the "
        f"gaff's cleats, foot {sp_foot:.0f} ft to within 18 in of the boom's sheave; three "
        "reef-bands (Steel); centre 0.4 of the foot abaft the raked mast."
        + canvas_note(BRIG_CANVAS["main.spanker"]),
    )
    b.line("main.gaff.throat_halyard", "throat_halyard", gaff, rating=rope_kn(3.5, 3))
    b.line("main.gaff.peak_halyard", "peak_halyard", gaff, rating=rope_kn(3.0, 4))
    b.line("main.spanker.sheet", "sheet", spanker, rating=rope_kn(4.0, 2), parts=2)
    b.line("main.spanker.outhaul", "outhaul", spanker, rating=rope_kn(3.0))
    b.sided("main.gaff.vang", "vang", gaff, rating=rope_kn(3.0))

    # the head: bowsprit, jib-boom and flying jib-boom; the head sails' areas are
    # judgements from the stays' runs, as the frigate's, at a brig-sloop's size
    stem_x = round(lwl / 2.0, 1)
    heads = [
        ("fore.topmast_staysail", "fore.topmast.stay", 33, round(stem_x - 1.5, 1), 7.5),
        ("jib", "jib.stay", 57, round(stem_x + 4.0, 1), 9.0),
        ("flying_jib", "flying_jib.stay", 31, round(stem_x + 9.0, 1), 10.5),
    ]
    head_loads = {sid: (area, h, "jibheaded") for sid, _, area, _, h in heads}
    bowsprit = b.spar(
        "bowsprit",
        "bowsprit",
        x_m=stem_x,
        length_m=ft(bowsprit_out),
        height_m=4.5,
        rating_kn=design_kn(list(head_loads.values()), dw["lower"]),
        note=f"bowsprit {bowsprit_ft:.0f} ft, 0.886 of the fore mast's hounded length, "
        f"{bowsprit_housed:.0f} ft of it housed (0.5 x the breadth) and {bowsprit_out:.0f} "
        "ft outboard, steeved 51 in in 12 ft (Fincham p. 88).",
    )
    jib_boom = b.spar(
        "jib_boom",
        "jib_boom",
        on=bowsprit,
        length_m=ft(jib_boom_out),
        height_m=6.0,
        rating_kn=design_kn([head_loads["jib"], head_loads["flying_jib"]], dw["jib_boom"]),
        note=f"jib-boom {jib_boom_ft:.0f} ft, 0.62 of the bowsprit (Fincham p. 88), "
        f"{jib_boom_out:.0f} ft of it outboard (7/12, Luce, as the frigate's).{prov}",
    )
    b.spar(
        "flying_jib_boom",
        "flying_jib_boom",
        on=jib_boom,
        length_m=ft(flying_out),
        height_m=7.0,
        rating_kn=design_kn([head_loads["flying_jib"]], dw["flying_jib_boom"]),
        note=f"flying jib-boom {flying_ft:.0f} ft, 1.22 of the jib-boom, lying along it "
        f"(Fincham p. 88), half of it beyond the jib-boom end (judgement).{prov}",
    )
    b.line(
        "fore.stay",
        "stay",
        "fore.mast",
        rating=rope_kn(11.0),
        note="11 in (judgement: the frigate's 15 in scaled); the fore storm staysail sets on it.",
    )
    b.line("fore.topmast.stay", "stay", "fore.topmast", rating=rope_kn(6.0))
    b.line(
        "jib.stay",
        "stay",
        "fore.topmast",
        rating=rope_kn(4.0),
        note="4 in, from the fore topmast head to the jib-boom end: the jib sets on it.",
    )
    b.line(
        "flying_jib.stay",
        "stay",
        "fore.topgallant_mast",
        rating=rope_kn(3.0),
        note="3 in, from the fore topgallant mast head to the flying jib-boom end.",
    )
    b.line(
        "main.stay",
        "stay",
        "main.mast",
        rating=rope_kn(12.0),
        note="12 in (judgement), from the main mast head to a collar on the fore mast (Steel "
        "1794, 'The main-staysail': the stay 'clinches round the main-mast-head above the "
        "rigging and the lower end sets up with a luff-tackle round the foremast'); the main "
        "staysail and the main storm staysail set on it.",
    )
    b.line("main.topmast.stay", "stay", "main.topmast", rating=rope_kn(6.0))
    b.line(
        "main.topgallant.stay",
        "stay",
        "main.topgallant_mast",
        rating=rope_kn(3.5),
        note="3.5 in, to the fore topmast head (Steel 1794: 'the main-topgallant-stay reeves "
        "through a block fastened to the fore-topmast-head'); the main topgallant staysail "
        "sets on it.",
    )
    b.line("bobstay", "stay", bowsprit, rating=rope_kn(9.0))
    b.line("martingale", "stay", jib_boom, rating=rope_kn(4.0))
    headsails = []
    for sid, stay, area, x, h in heads:
        s = b.sail(
            sid,
            "jibheaded",
            stay=stay,
            area_m2=area,
            x_m=x,
            centre_height_m=h,
            canvas_no=BRIG_CANVAS[sid][0],
            cloth_rating_kn=cloth(area, BRIG_CANVAS[sid][0]),
            note=f"{sid.replace('_', ' ').replace('.', ' ')} {area} m2 (judgement from the "
            "stay's run: the frigate's head sails scaled by the square of the length, 95 to "
            "143 ft)." + canvas_note(BRIG_CANVAS[sid]),
        )
        size = {"fore.topmast_staysail": 3.0, "jib": 3.0, "flying_jib": 2.0}[sid]
        b.line(f"{sid}.halyard", "halyard", s, rating=rope_kn(size, 2))
        b.sided(f"{sid}.sheet", "sheet", s, rating=rope_kn(size))
        b.line(f"{sid}.downhaul", "downhaul", s, rating=rope_kn(quarter(size * 0.8)))
        headsails.append(s)
    # the staysails between the masts (package 57): Steel's for a brig, whose sails are
    # "similar to those on the main and fore masts of a ship" and whose main staysail is
    # "commonly [bent] in brigs": the main, main topmast, middle and main topgallant
    # staysails, the middle new ("Sloops and brigs in the navy have only from one to three
    # [cloths] more"), each cut by Steel's rule as the frigate's (`between_the_masts`); they
    # were triangles of judgement from the stays' runs before
    between = between_the_masts(
        b,
        geom=geom,
        mast_x=mast_x,
        rake_deg=rake_deg,
        deck_height=deck_height,
        ahead="fore",
        after="main",
        canvas=BRIG_CANVAS,
        brig=True,
    )

    # studding sails on fore and main by the frigate's rule: lower (fore only), topmast and
    # topgallant, the booms on the yards; the swinging boom 0.6 of the lower yard (Fincham)
    stuns = []
    for name in ("fore", "main"):
        x = mast_x[name]
        g = geom[name]
        for level, parent_yard, boom_len, boom_h_, centre in (
            ("lower", f"{name}.yard", swing_boom, 1.0, areas[name]["course"][1]),
            (
                "topmast",
                f"{name}.topsail.yard",
                0.5 * g["topsail_yard"],
                ft(g["yard_h"]),
                areas[name]["topsail"][1],
            ),
            (
                "topgallant",
                f"{name}.topgallant.yard",
                0.5 * g["tg_yard"],
                ft(g["topsail_h"]),
                areas[name]["topgallant"][1],
            ),
        ):
            if name == "main" and level == "lower":
                continue
            area = stuns_area[name][level]
            stuns_canvas = BRIG_CANVAS[f"{level} studding"]
            for side in SIDES:
                boom_id = b.spar(
                    f"{name}.{level}.studdingsail_boom.{side}",
                    "studdingsail_boom",
                    on=parent_yard,
                    side=side,
                    length_m=ft(boom_len),
                    height_m=boom_h_,
                    rating_kn=design_kn([(area, centre, "studding")], dw["studding"]),
                    note=(
                        f"{name} {level} studding-sail boom {boom_len:.0f} ft, "
                        + (
                            "0.6 of the lower yard (Fincham p. 88, swing-booms)"
                            if level == "lower"
                            else "half the yard it is rigged on (Luce)"
                        )
                        + f"; rated for its sail in {dw['studding']:.0f} kn.{prov}"
                        if side == SIDES[0]
                        else None
                    ),
                )
                sid = b.sail(
                    f"{name}.{level}.studdingsail.{side}",
                    "studding",
                    boom=boom_id,
                    yard=parent_yard,
                    side=side,
                    area_m2=area,
                    x_m=raked_x(x, rake_deg[name], centre, deck_height),
                    centre_height_m=centre,
                    canvas_no=stuns_canvas[0],
                    cloth_rating_kn=cloth(area, stuns_canvas[0]),
                    note=(
                        f"{name} {level} studding sail {area} m2: 0.4 of the yard wide, as deep "
                        "as the sail beside it (judgement, as the frigate's)."
                        + canvas_note(stuns_canvas)
                        if side == SIDES[0]
                        else None
                    ),
                )
                size = {"lower": 2.5, "topmast": 2.0, "topgallant": 1.75}[level]
                b.line(f"{sid}.halyard", "halyard", sid, rating=rope_kn(size))
                b.line(f"{sid}.tack", "tack", sid, rating=rope_kn(size))
                b.line(f"{sid}.sheet", "sheet", sid, rating=rope_kn(quarter(size * 0.8)))
                b.line(f"{sid}.downhaul", "downhaul", sid, rating=rope_kn(quarter(size * 0.7)))
                stuns.append(sid)

    # -- storm canvas (spec 3b §6.4; spec M5 §25): a storm fore staysail, a main storm
    # staysail and a storm trysail, each in the sail room --------------------------------
    storm_canvas = BRIG_CANVAS["storm"]
    gf = geom["fore"]
    fss_foot = 0.9 * gf["yard"] / 2.0 + 4.0
    fss_leech = 0.42 * gf["yard"]
    fss_area = round(0.5 * fss_foot * fss_leech * FT * FT)
    fss_clew_x = mast_x["fore"] + 1.0
    fss = b.sail(
        "fore.storm_staysail",
        "jibheaded",
        stay="fore.stay",
        area_m2=fss_area,
        x_m=round(fss_clew_x + fss_foot * FT / 3.0, 1),
        centre_height_m=round(deck_height + (1.5 + fss_leech * FT / 3.0), 1),
        canvas_no=storm_canvas[0],
        cloth_rating_kn=storm_cloth(fss_area),
        bent=False,
        note=f"fore storm staysail {fss_area} m2 on the fore stay (Luce 1884 ch. X), cut as "
        f"the frigate's: Kipping's fore staysail, foot {fss_foot:.0f} ft, leech "
        f"{fss_leech:.0f} ft (the course's depth); in the sail room."
        + canvas_note(storm_canvas, storm=True),
    )
    b.line("fore.storm_staysail.halyard", "halyard", fss, rating=rope_kn(3.0, 2))
    b.sided("fore.storm_staysail.sheet", "sheet", fss, rating=rope_kn(3.0, 3))
    b.line("fore.storm_staysail.downhaul", "downhaul", fss, rating=rope_kn(2.5))
    # the main storm staysail on the main stay, as the frigate's mizzen storm staysail is on
    # the mizzen stay: tack at the fore mast collar 12 ft up, head 0.6 up the stay, clew
    # 7 ft above the deck (Steel's mizzen staysail; 0.6 judgement)
    run_ft = (mast_x["fore"] - mast_x["main"]) / FT
    rise_ft = gm["hounds"] - 12.0
    head_x, head_z = -0.6 * run_ft, 12.0 + 0.6 * rise_ft
    mss_area = round(0.5 * abs(head_x * (7.0 - 12.0) - (head_z - 12.0) * head_x) * FT * FT)
    mss = b.sail(
        "main.storm_staysail",
        "jibheaded",
        stay="main.stay",
        area_m2=mss_area,
        x_m=round(mast_x["fore"] + (2.0 * head_x / 3.0) * FT, 1),
        centre_height_m=round(deck_height + (12.0 + head_z + 7.0) / 3.0 * FT, 1),
        canvas_no=storm_canvas[0],
        cloth_rating_kn=storm_cloth(mss_area),
        bent=False,
        note=f"main storm staysail {mss_area} m2 on the main stay (Luce 1884 ch. X: 'the "
        "storm-staysails set on the respective lower-stays'): tack at the fore mast collar, "
        "head 0.6 up the stay, clew 7 ft above the deck (as the frigate's mizzen storm "
        "staysail; 0.6 judgement); in the sail room." + canvas_note(storm_canvas, storm=True),
    )
    b.line("main.storm_staysail.halyard", "halyard", mss, rating=rope_kn(3.0, 2))
    b.sided("main.storm_staysail.sheet", "sheet", mss, rating=rope_kn(3.0, 3))
    b.line("main.storm_staysail.downhaul", "downhaul", mss, rating=rope_kn(2.5))
    # the storm trysail on the main gaff and boom in place of the spanker: Steel's sloop's
    # storm mainsail rule, as the schooner's storm trysail (head two-fifths of the sail's,
    # foot three times the head, luff 0.85 of the hoist, after-leech an eighth deeper,
    # three reef-bands); Luce 1884 ch. XXIX: lying to under "probably single reefed trysail"
    st_head = 0.4 * sp_head
    st_foot = 3.0 * st_head
    st_luff = 0.85 * sp_hoist
    st_leech = st_luff * 9.0 / 8.0
    st_area = round((st_head + st_foot) / 2.0 * (st_luff + st_leech) / 2.0 * FT * FT)
    st_z = boom_h + 0.45 * st_luff
    st = b.sail(
        "storm_trysail",
        "gaff",
        mast="main.mast",
        gaff=gaff,
        boom=boom,
        area_m2=st_area,
        reef_bands=3,
        x_m=round(
            raked_x(mast_x["main"], rake_deg["main"], deck_height + st_z * FT, deck_height)
            - 0.4 * st_foot * FT,
            1,
        ),
        centre_height_m=round(deck_height + st_z * FT, 1),
        canvas_no=storm_canvas[0],
        cloth_rating_kn=storm_cloth(st_area),
        bent=False,
        in_place_of="main.spanker",
        note=f"storm trysail {st_area} m2 on the main gaff and boom (Steel 1794, 'Sloop's "
        f"trysail, or storm mainsail', as the schooner's): head {st_head:.0f} ft (two-fifths "
        f"of the spanker's), foot {st_foot:.0f} ft (three times the head), luff "
        f"{st_luff:.0f} ft (0.85 of the spanker's hoist, judgement), after-leech an eighth "
        "deeper; three reef-bands; bent in place of the spanker; in the sail room."
        + canvas_note(storm_canvas, storm=True),
    )
    b.line("storm_trysail.sheet", "sheet", st, rating=rope_kn(4.0, 2), parts=2)
    b.line("storm_trysail.outhaul", "outhaul", st, rating=rope_kn(3.0))
    storm = [fss, mss, st]

    # groups, as the frigate's less a mast
    b.group("courses", sails_by_level["course"])
    b.group("topsails", sails_by_level["topsail"])
    b.group("topgallants", sails_by_level["topgallant"])
    b.group("royals", sails_by_level["royal"])
    b.group("headsails", headsails)
    b.group("jibs", headsails[1:])
    b.group("staysails", headsails[:1] + between)
    b.group("staysails between the masts", between)  # package 57, as the frigate's
    b.group("studdingsails", stuns)
    b.group("square sails", sum(sails_by_level.values(), []))
    b.group("fore-and-aft sails", headsails + between + [spanker])
    b.group("light sails", sails_by_level["royal"] + [headsails[2]] + between[2:] + stuns)
    b.group("lying-to staysails", ["main.staysail"])  # package 57, as the frigate's
    b.group(
        "plain sail",
        sails_by_level["course"]
        + sails_by_level["topsail"]
        + sails_by_level["topgallant"]
        + headsails[:2]
        + [spanker],
    )
    b.group(
        "all sail",
        sum(sails_by_level.values(), []) + headsails + between + [spanker] + stuns,
    )
    for name in ("fore", "main"):
        b.group(
            f"{name} yards",
            [y for lvl in yards_by_level for y in yards_by_level[lvl] if y.startswith(name + ".")],
        )
    b.group("yards", [y for lvl in yards_by_level for y in yards_by_level[lvl]])
    b.group("lower yards", yards_by_level["course"])
    b.group("topsail yards", yards_by_level["topsail"])
    b.group("topgallant yards", yards_by_level["topgallant"])
    b.group("royal yards", yards_by_level["royal"])
    b.group(
        "head yards",
        [y for lvl in yards_by_level for y in yards_by_level[lvl] if y.startswith("fore.")],
    )
    b.group(
        "after yards",
        [y for lvl in yards_by_level for y in yards_by_level[lvl] if y.startswith("main.")],
    )
    b.group("lower masts", ["fore.mast", "main.mast"])
    b.group("topmasts", ["fore.topmast", "main.topmast"])
    b.group("topgallant masts", ["fore.topgallant_mast", "main.topgallant_mast"])
    b.group("royal masts", ["fore.royal_mast", "main.royal_mast"])
    b.alias("spanker", "main.spanker")
    b.alias("driver", "main.spanker")
    b.alias("boom mainsail", "main.spanker")
    b.alias("trysail", "main.spanker")
    b.alias("foresail", "fore.course")
    b.alias("mainsail", "main.course")
    b.alias("fore yard", "fore.yard")
    b.alias("main yard", "main.yard")
    b.alias("spanker boom", "main.boom")
    b.alias("driver boom", "main.boom")
    b.alias("spanker gaff", "main.gaff")
    b.alias("fore topmast staysail", "fore.topmast_staysail")
    b.alias("main staysail", "main.staysail")
    b.alias("main topmast staysail", "main.topmast_staysail")
    b.alias("main topgallant staysail", "main.topgallant_staysail")
    b.alias("stuns'ls", "studdingsails")
    b.alias("studding sails", "studdingsails")
    b.alias("kites", "studdingsails")
    b.alias("head sails", "headsails")
    b.alias("topgallant sails", "topgallants")
    b.alias("upper yards", "topgallant yards")
    b.group("storm canvas", storm)
    b.group("storm staysails", storm[:2])
    for name in ("fore", "main"):
        for level in ("lower", "topmast", "topgallant"):
            if name == "main" and level == "lower":
                continue
            b.group(
                f"{name} {level} studdingsails", [f"{name}.{level}.studdingsail.{s}" for s in SIDES]
            )
    for name in ("fore", "main"):
        for cls in ("sheet", "tack", "bowline"):
            b.group(f"{name} {cls}s", [f"{name}.course.{cls}.{s}" for s in SIDES])
            b.alias(f"{name} {cls}", f"{name} {cls}s")
        b.group(f"{name} topsail bowlines", [f"{name}.topsail.bowline.{s}" for s in SIDES])
        b.alias(f"{name} top bowline", f"{name} topsail bowlines")
    ground_tackle_for(b, burthen, beam_ft, draught_ft)
    if merchant:
        merchant_brig(b, out_dir, burthen, gundeck_ft)
        return
    brig_crew(b)
    brig_armament(b, deck_height)
    hold_for(b, burthen, True, "a brig-sloop's hold is her own stores: judgement")
    b.pumps(
        PUMPS_NOTE,
        pump_entries(1, 2, ["the chain pump", "the starboard hand pump", "the larboard hand pump"]),
    )
    b.boats(
        BOATS_NOTE,
        boat_entries(
            gundeck_ft,
            True,
            [
                (
                    "launch",
                    "launch",
                    "the launch",
                    1.0,
                    "The launch, 2.6 root(95 ft) = 25 ft (Luce's rule).",
                    "data/ships/boat-launch-25.yaml",
                ),
                (
                    "cutter",
                    "cutter",
                    "the cutter",
                    0.9,
                    "The cutter, 0.9 of the launch, a sloop's first cutter (Luce's rule).",
                    "data/ships/boat-cutter-23.yaml",
                ),
                (
                    "jolly_boat",
                    "jolly boat",
                    "the jolly boat",
                    JOLLY_BOAT_OF_LAUNCH,
                    "The jolly boat at the stern (judgement in the size).",
                    "data/ships/boat-yawl-16.yaml",
                ),
            ],
        ),
    )
    # Her two descriptions at far detail (spec M5 §25, package 36; the owner, 2026-09-29:
    # the brig-sloop is the Navy's brig and the merchant brig the trade's, one file): what
    # the tops make out at four miles is the rig, two square-rigged masts (Falconer 1780,
    # BRIG: "a merchant-ship with two masts"; Steel 1794 vol. I: the brig's sails as a
    # ship's fore and main), and what she is when made out within a mile and a half.
    b.descriptions(
        [
            (
                "brig-sloop",
                "a brig",
                "a brig-sloop of war, sixteen ports a side",
                "Harpy herself: sixteen 32-pounder carronades (the kit's manual; "
                "docs/design/VesselCandidates.md); the ports are what the glass counts.",
            ),
            (
                "merchant brig",
                "a brig",
                "a merchant brig, deep laden",
                "The trade's brig of the same rig and size, her ports painted and no guns "
                "run out (Falconer 1780, BRIG); 'deep laden' is the merchantman's look, "
                "judgement.",
            ),
        ]
    )
    b.dump(
        os.path.join(out_dir, "brig.yaml"),
        "# The brig: Harpy, H.M. brig-sloop of the Diligence class (launched 1796, sold 1817),\n"
        "# 316 tons, 95 ft on the gun deck by 28 ft 1 1/2 in (the kit's manual as the owner\n"
        "# noted it; docs/design/VesselCandidates.md). Generated by tools/gen_ships.py; edit\n"
        "# that script and rerun, do not edit this file. Spars: Fincham 1843, 'On Masting\n"
        "# Brigs' (pp. 82 to 83) and the table of proportions for brigs of war (p. 88), checked\n"
        "# against Luce 1866 ch. VII and Steel 1794; sails: Steel 1794 vol. I ('A brig's\n"
        "# mainsail', p. 119; a brig's sails as a ship's fore and main); rope: Luce 1866 ch. IV.\n"
        "# Spar ratings are provisional, set for truth 9 with the M1 sail curves; see the\n"
        "# script. Canvas: Steel 1794 with Kipping and Luce 1884 p. 171; cloth ratings from the\n"
        "# number by Luce App. E. Units: metres, m2, kg, kN. Comments mark judgements. Package\n"
        "# 32b (spec M5 §25): no engine change.\n",
    )


def merchant_brig(b, out_dir, burthen, gundeck_ft):
    """The merchant brig's own (package 68; the cold review of 2026-10-22, R-63: "A merchant
    brig, free" sailed H.M. brig-sloop Harpy's file, a commander and a surgeon, twenty
    marines, the Navy's books and a 32-ton hold under the American colours, and the director
    called her a king's ship): her name and words, her company, her stores, the trader's
    hold and boats; the hull, the spars, the sails and the ground tackle are the Harpy's,
    built above."""
    b.doc["ship"]["name"] = "Industry"
    b.doc["ship"]["era_notes"] = (
        "The merchant brig Industry (package 68): the trade's brig of the Harpy's lines and "
        "rig, about 316 tons burthen, her ports painted and four 6-pounders for her own defence "
        "(package 70); a master's and mates' "
        "company of sixteen and no marines, a merchant's stores and the trader's hold and "
        "boats. The hull and the rig are the brig-sloop's (Falconer 1780, BRIG: 'a merchant-"
        "ship with two masts'; the trade's brig of the period of the same size, judgement), "
        "every rule as the Harpy's; see tools/gen_ships.py."
    )
    merchant_brig_crew(b)
    merchant_brig_armament(b)
    hold_for(b, burthen, False, "a merchant brig's hold, her trade: judgement")
    b.pumps(PUMPS_NOTE, pump_entries(0, 2, ["the starboard pump", "the larboard pump"]))
    b.boats(
        BOATS_NOTE,
        boat_entries(
            gundeck_ft,
            False,
            [
                (
                    "long_boat",
                    "launch",
                    "the long-boat",
                    1.0,
                    "The long-boat, a merchantman's one great boat, stowed amidships (Luce's "
                    "rule on a small vessel's scale).",
                ),
                (
                    "jolly_boat",
                    "jolly boat",
                    "the jolly boat",
                    JOLLY_BOAT_OF_LAUNCH,
                    "The jolly boat at the stern (judgement in the size).",
                    "data/ships/boat-yawl-16.yaml",
                ),
            ],
        ),
    )
    b.descriptions(
        [
            (
                "merchant brig",
                "a brig",
                "a merchant brig, deep laden",
                "The trade's brig, her ports painted and no guns run out (Falconer 1780, "
                "BRIG); 'deep laden' is the merchantman's look, judgement.",
            ),
        ]
    )
    b.dump(
        os.path.join(out_dir, "merchant-brig.yaml"),
        "# The merchant brig: Industry, the trade's brig of the Harpy's lines and rig (package\n"
        "# 68; the cold review of 2026-10-22, R-63): about 316 tons, 95 ft by 28 ft 1 1/2 in,\n"
        "# the hull, the spars, the sails and the ground tackle the brig-sloop's (brig.yaml and\n"
        "# its sources), the company a master's and mates' of sixteen, no marines, a merchant's\n"
        "# stores and the trader's hold and boats. Generated by tools/gen_ships.py; edit that\n"
        "# script and rerun, do not edit this file. Units: metres, m2, kg, kN. Comments mark\n"
        "# judgements.\n",
    )


def merchant_brig_crew(b):
    """The merchant brig's company (package 68): sixteen, a master's and mates' (the posts
    of data/people/merchant-brig.yaml), no marines and no idlers but the cook; the stores of
    a trader's voyage; the ration the Navy's table, which her articles promised the like of
    (judgement: the period's merchant service had no scale of its own in the references)."""
    b.crew(
        [
            (
                ("complement",),
                16,
                "A merchant brig of about 300 tons: a master, two mates, a boatswain and a "
                "carpenter, a cook, nine seamen and a boy (judgement on the period's trade, "
                "about five men to a hundred tons).",
            ),
            (
                ("names",),
                "american",
                "The scenario's brig wears the American colours: the american list in "
                "data/crew/names.yaml.",
            ),
            (
                ("stations", "forecastle"),
                3,
                "Hands per station, both watches together; a merchant brig has no marines and "
                "works aloft from the deck stations. Forecastlemen: 3, judgement.",
            ),
            (("stations", "fore_top"), 3, "Fore topmen: 3, judgement."),
            (("stations", "main_top"), 3, "Main topmen: 3, judgement."),
            (("stations", "afterguard"), 1, "Afterguard: the boy, 1, judgement."),
            (("stations", "idlers"), 1, "Idlers: the cook."),
            (
                ("ratings", "able"),
                0.70,
                "Share of the seamen by rating: judgement. A merchantman shipped able seamen "
                "and few others. Able: 0.70.",
            ),
            (("ratings", "ordinary"), 0.20, "Ordinary: 0.20, judgement."),
            (("ratings", "landsman"), 0.10, "Landsmen: 0.10, judgement."),
        ]
        + [
            (
                ("posts", post),
                None,
                "Station holders by post (spec M3 2.3): the master, the mates, the boatswain "
                "and the carpenter (data/people/merchant-brig.yaml); names are drawn at muster."
                if i == 0
                else None,
            )
            for i, post in enumerate(MERCHANT_BRIG_POSTS)
        ]
        + [
            (("idlers_by_trade", "cook"), 1, "How the idlers are made up: the cook, 1."),
            (
                ("stores", "water_tons"),
                6,
                "Water for two months: 16 men at a gallon a day is about 4 tons, and some over "
                "(judgement).",
            ),
            (("stores", "provisions_days"), 90, "Provisions: three months (judgement)."),
            (("stores", "spare_spars"), {}, None),  # the booms, by class: below
            (("stores", "cordage_fathoms"), 150, "Spare rope (judgement)."),
            (
                ("stores", "shot_plugs"),
                4,
                SHOT_PLUGS_NOTE + " A merchantman's 4.",
            ),
            *ration_entries(
                "a merchant's articles promised the like (judgement: no scale of the period's "
                "merchant service is in the references)"
            ),
        ]
    )
    b.people(
        "The named people beyond the posts (package 35, spec M5 §22): a boy as the "
        "messenger; see tools/gen_ships.py.",
        MERCHANT_BRIG_DRAWN,
    )
    b.spare_spars(
        "The booms: a trader's spares (judgement after Luce 1866 ch. XVII, scaled down); see "
        "tools/gen_ships.py.",
        [
            ("topmast", 1, "One topmast, to answer either mast (judgement, after Chapelle)."),
            ("yard", 1, "A spare topsail yard (judgement, after Luce 1866)."),
        ],
    )
    b.sail_room(
        "The sail room (spec 3b §6.3): a trader's second suit of the sails she wears out; see "
        "tools/gen_ships.py.",
        [
            (
                "fore.topsail",
                BRIG_CANVAS["fore.topsail"][0],
                "A second fore and main topsail and jib (judgement).",
            ),
            ("main.topsail", BRIG_CANVAS["main.topsail"][0], None),
            ("jib", BRIG_CANVAS["jib"][0], None),
            (
                "fore.storm_staysail",
                BRIG_CANVAS["storm"][0],
                "Storm canvas, one of each (spec 3b §6.4).",
            ),
            ("main.storm_staysail", BRIG_CANVAS["storm"][0], None),
        ],
    )


def brig_crew(b):
    posts_note = (
        "Station holders by post (spec M3 2.3): a brig-sloop's, the commander and his "
        "lieutenant, then the master and the standing and warrant officers (Falconer, "
        "ORDINARY and CARPENTER). Names are drawn at muster unless a post gives one."
    )
    b.crew(
        [
            (
                ("complement",),
                121,
                "The kit's manual: the Diligence class establishment, 121 (Winfield not reached).",
            ),
            (("names",), "english", "A King's ship: the english list in data/crew/names.yaml."),
            (
                ("stations", "forecastle"),
                14,
                "Hands per station, both watches together, the frigate's stations in small "
                "(spec M3 2.3; Luce 1884 ch. XX). Forecastlemen: 14, judgement.",
            ),
            (("stations", "fore_top"), 12, "Fore topmen: 12, judgement."),
            (("stations", "main_top"), 14, "Main topmen: 14, judgement, the larger top."),
            (("stations", "afterguard"), 22, "Afterguard, the boys included: 22, judgement."),
            (
                ("stations", "waisters"),
                14,
                "Waisters: 14, judgement; the station whose numbers make up the establishment.",
            ),
            (
                ("stations", "marines"),
                20,
                "Marines: 20, judgement, a sergeant's party for a sloop (a brig-sloop of the "
                "class carried about twenty); they work as afterguard, never aloft.",
            ),
            (("stations", "idlers"), 17, "Idlers: the trades below."),
            (
                ("ratings", "able"),
                0.30,
                "Share of the seamen by rating: judgement, a King's ship's books as the "
                "frigate's. Able: 0.30.",
            ),
            (("ratings", "ordinary"), 0.40, "Ordinary: 0.40, judgement."),
            (("ratings", "landsman"), 0.30, "Landsmen: 0.30, judgement."),
        ]
        + [
            (("posts", post), None, posts_note if i == 0 else None)
            for i, post in enumerate(BRIG_POSTS)
        ]
        + [
            (
                ("idlers_by_trade", "carpenter's crew"),
                3,
                "How the idlers are made up; they must sum to the idlers. Judgement for a "
                "brig-sloop of 121. The carpenter's mate and crew: 3.",
            ),
            (("idlers_by_trade", "sailmaker's crew"), 1, "A sailmaker: 1."),
            (("idlers_by_trade", "cooper"), 1, "The cooper: 1."),
            (("idlers_by_trade", "cook"), 2, "The cook and his mate: 2."),
            (("idlers_by_trade", "steward"), 2, "The purser's and the commander's stewards: 2."),
            (("idlers_by_trade", "servant"), 5, "Officers' servants: 5."),
            (("idlers_by_trade", "surgeon's mate"), 1, "The surgeon's mate: 1."),
            (("idlers_by_trade", "clerk"), 1, "The commander's clerk: 1."),
            (("idlers_by_trade", "master-at-arms's party"), 1, "A ship's corporal: 1."),
            (
                ("stores", "water_tons"),
                45,
                "Water: 45 tons, the frigate's four months' allowance scaled to 121 men "
                "(judgement).",
            ),
            (
                ("stores", "provisions_days"),
                120,
                "Provisions: four months at full allowance (judgement, as the frigate's).",
            ),
            (("stores", "spare_spars"), {}, None),  # the booms, by class: below
            (
                ("stores", "cordage_fathoms"),
                300,
                "Spare rope in the boatswain's store (judgement).",
            ),
            (
                ("stores", "shot_plugs"),
                20,
                SHOT_PLUGS_NOTE + " A brig-sloop's 20.",
            ),
            *ration_entries("a King's ship"),
        ]
    )
    # The people (package 35, spec M5 §22): a master's mate and a midshipman as the
    # messenger, as the frigate's in small (the Regulations of 1806, the Master, art.
    # XXVIII). The roles and their notes are the wardroom file's (package 40).
    b.people(
        "The named people beyond the posts (package 35, spec M5 §22): each drawn from his "
        "station at muster, the counts above unchanged; see tools/gen_ships.py.",
        BRIG_DRAWN,
    )
    # The booms (package 30b): the frigate's list (Luce 1866 ch. XVII, 'Stowing Booms')
    # scaled to a brig-sloop: one topmast, made alike for either mast "in order that the
    # spare spars and sails may answer to replace those of either mast" (Chapelle 1930,
    # 'Masting Rules and Sail Plans', of the brig, after Fincham), one topgallant mast, one
    # topsail yard, a pair of topmast studding-sail booms and the spare jib-boom.
    b.spare_spars(
        "The booms: the spare spars by class (Luce 1866 ch. XVII, 'Stowing Booms', scaled to "
        "a brig-sloop; Chapelle 1930 on the brig's upper spars made alike); see "
        "tools/gen_ships.py.",
        [
            ("topmast", 1, "One topmast, to answer either mast (Chapelle, after Fincham)."),
            ("topgallant_mast", 1, "A stump topgallant mast (judgement, after Luce 1866)."),
            ("yard", 1, "A spare topsail yard (judgement, after Luce 1866)."),
            (
                "studdingsail_boom",
                2,
                "A pair of topmast studding-sail booms (judgement, after Luce).",
            ),
            ("jib_boom", 1, "The spare jib-boom (Luce 1866)."),
        ],
    )
    # The sail room (spec 3b §6.3) by the schooner's rule: a second of each sail she could
    # least do without (judgement: the two topsails, the fore course, the jib and the fore
    # topmast staysail, the sails a sloop wore out), and one of each storm sail.
    b.sail_room(
        "The sail room (spec 3b §6.3), every sail new; see tools/gen_ships.py.",
        [
            (
                "fore.topsail",
                BRIG_CANVAS["fore.topsail"][0],
                "A second fore and main topsail, fore course, jib and fore topmast staysail "
                "(spec 3b §6.3, judgement).",
            ),
            ("main.topsail", BRIG_CANVAS["main.topsail"][0], None),
            ("fore.course", BRIG_CANVAS["fore.course"][0], None),
            ("jib", BRIG_CANVAS["jib"][0], None),
            ("fore.topmast_staysail", BRIG_CANVAS["fore.topmast_staysail"][0], None),
            (
                "fore.storm_staysail",
                BRIG_CANVAS["storm"][0],
                "Storm canvas, one of each (spec 3b §6.4).",
            ),
            ("main.storm_staysail", BRIG_CANVAS["storm"][0], None),
            ("storm_trysail", BRIG_CANVAS["storm"][0], None),
        ],
    )


# ---------------------------------------------------------------------------
# The lugger: the chasse-marée on the Éclair of 1795 (package 43b; spec M6 §19; decision 42)
# ---------------------------------------------------------------------------
#
# Sources (docs/design/VesselReferences-2026-10.md § 1, decision 42). The hull is L'Éclair,
# a French gun-lugger taken by Strachan's squadron and "taken off afloat" at Portsmouth on
# 2 July 1795 (RMG ZAZ6306, read from the plan): 59 ft 3 in on the range of the deck, 45 ft
# 11 in keel for tonnage, 20 ft 4 in breadth extreme, 7 ft 0 in depth in hold, 101 tons
# (the Navy's rule on 45 ft 11 in by 20 ft 4 in gives 100 92/94), three guns. The rig is
# Forfait's Table VII, *Lougres ou woguers*, the 60-pied column (1788 p. 75): the masts in
# terms of the breadth, the yards in terms of the length; main mast 3.455 B, fore 2.759 B,
# mizen (tapecul) 1.888 B, topmasts 1.091 B, bowsprit 2.649 B; main yard 0.573 L, fore
# 0.454 L, main topsail yard 0.424 L, fore 0.393 L, mizen yard and outrigger 0.364 L; the
# main mast 0.040 L abaft the middle, the fore 0.364 L before it, the mizen "le plus près
# qu'on peut du couronnement"; rakes 1 in, 4 lignes and 2 in per foot; the sail area 4.037
# L x B, its centre 0.024 L abaft the middle and 1.576 B high. The references note warns
# that her breadth is 0.343 of her length, beamier than Forfait's luggers, so that masts on
# her breadth come tall, and asks the area and the centre checked: the masts are set on her
# breadth here, since the area then keeps Forfait's own coefficient on her own L x B (the
# yards on her length, the masts' height on her breadth: area goes as L x B either way),
# and the check is printed in the file's comments (the masts on the length instead would
# give 0.75 of it, a lugger under-canvassed by her own author's rule). Heels below the
# load line by Fincham's chasse-marée (1843 p. 61: main 0.26 B, fore 0.17 B, mizen 0.08 B
# for the lugger). The lugs are dipping lugs, slung at a third of the yard (Forfait pp. 5
# to 6; Lescallier 1791 pp. 391 to 392; Steel 1794 vol. I, LUGGER), the yard peaked at
# 60 to 70 degrees to the mast and hoisted to a foot below the sheave (Forfait p. 53); the
# lug topsails have braces, lifts and bowlines and are trimmed as square topsails (Forfait
# p. 53: "les huniers seuls"); the mizen a lug sheeted to its outrigger and not dipped
# (Holdsworth 1874 p. 104's "working mizen"; judgement); the bowsprit runs on a chevalet
# (Forfait p. 53), the cutter's running bowsprit; the storm suit is the taille-vent, a lug
# of about half the mainsail's area tacked at the foot of the mast (Forfait p. 52;
# Lescallier pp. 408 to 409; Willaumez 1831, TAILLE-VENT), its yard 0.7 of the main yard
# (Fincham's chasse-marée's second suit).

LUGGER_CANVAS: dict[str, tuple[int, str]] = {
    "lug": (
        2,
        "judgement: no period number for a lug found; the cutter's mainsail's, Steel 1794 p. "
        "120, No. 1 or 2, for the sail that drives her",
    ),
    "mizen": (3, "judgement: a lighter lug than the fore and main"),
    "topsail": (
        6,
        f"{STEEL_SM} p. 125, 'Sloop's topsail': No. 6 or 7, the lugger's topsails as light",
    ),
    "jib": (2, f"{STEEL_SM}, 'Smack's jib' (OCR line 15709): No. 1 or 2"),
    "flying jib": (6, "judgement: a light outer jib"),
    "taille-vent": (1, "judgement: the storm lug, of the heaviest"),
    "storm jib": (
        1,
        f"{STEEL_SM}, the sloop's jibs (p. 190): 'No. 1 or 2 ... used in stormy weather'",
    ),
}

LUGGER_TOPSAIL_ROPE = {
    "halyard": 2.5,
    "sheet": 2.5,
    "brace": 1.75,
    "lift": 1.75,
}
LUGGER_POSTS, LUGGER_DRAWN = wardroom("lugger")


def _quad_area_centroid(pts):
    """The area and the centroid of a four-cornered sail by its corners (x, z), feet."""
    a = cx = cz = 0.0
    n = len(pts)
    for i in range(n):
        x1, z1 = pts[i]
        x2, z2 = pts[(i + 1) % n]
        cross = x1 * z2 - x2 * z1
        a += cross
        cx += (x1 + x2) * cross
        cz += (z1 + z2) * cross
    a *= 0.5
    return abs(a), cx / (6.0 * a), cz / (6.0 * a)


def lugger(out_dir="data/ships"):
    dw = dict(DESIGN_WIND_KN, lug=45.0)  # a lug is carried reefed in a gale, as a gaff sail
    # -- hull ---------------------------------------------------------------------------
    lod_ft = 59.25  # the range of the deck (RMG ZAZ6306)
    keel_ft = 45.0 + 11.0 / 12.0
    beam_ft = 20.0 + 4.0 / 12.0
    burthen = 101.0
    lwl_ft = 55.0  # judgement: between the keel and the deck, a raking stem and post
    # draught: deep aft for grip (Willaumez 1831, CHASSE-MARÉE: the main mast "très incliné
    # sur l'arrière" over a hull drawing most aft); judgement, 8 ft 6 in aft and 5 ft 6 in
    # forward, the mean a foot over her depth in hold (7 ft 0 in), the keel and floors
    draught_aft_ft = 8.5
    draught_fwd_ft = 5.5
    draught_ft = (draught_aft_ft + draught_fwd_ft) / 2.0
    lwl, beam, draught = ft(lwl_ft), ft(beam_ft), ft(draught_ft)
    displacement = round(lwl * beam * draught * 0.45 * 1025.0, -3)
    deck_height = 1.0  # judgement: about 3 ft 3 in of side above the water
    deck_above_lwl_ft = deck_height / FT
    L, B = lod_ft, beam_ft

    b = Builder(
        "Éclair",
        "lugger",
        "L'Éclair, a French gun-lugger of the war taken in 1795 and taken off afloat at "
        "Portsmouth (RMG ZAZ6306): 101 tons burthen, 59 ft 3 in on the range of the deck, 45 "
        "ft 11 in keel for tonnage, 20 ft 4 in breadth, 7 ft depth in hold, three guns (guns "
        "are not parts until milestone 7); a chasse-marée of three masts with dipping lugs, "
        "lug topsails, a lug mizen to an outrigger and jibs on a running bowsprit, by "
        "Forfait 1788's Table VII (the 60-pied lougre), with the taille-vent for a blow; "
        "see tools/gen_ships.py for every rule.",
        {
            "length_waterline_m": lwl,
            "beam_m": beam,
            "draught_m": draught,
            "displacement_kg": displacement,
            "gm_m": 1.2,
            "clr_x_m": -1.6,
            "lateral_area_m2": round(lwl * draught * 0.85),
            "hull_speed_kn": round(1.34 * math.sqrt(lwl_ft), 1),
            "deck_height_m": deck_height,
            "rudder": {"area_m2": 1.4, "max_angle_deg": 35, "rate_deg_s": 5.0, "span_m": 2.5},
        },
        {
            "length_waterline_m": f"{lwl_ft:.0f} ft: judgement between the {keel_ft:.1f} ft keel "
            f"for tonnage and the {lod_ft} ft on the range of the deck (RMG ZAZ6306).",
            "beam_m": "20 ft 4 in extreme (RMG ZAZ6306; the inch figure may carry a half).",
            "draught_m": f"{draught_ft:.1f} ft mean: {draught_aft_ft} ft aft, {draught_fwd_ft} ft "
            "forward (judgement: a chasse-marée drew most aft; her depth in hold 7 ft 0 in, the "
            "plan).",
            "displacement_kg": "LWL x beam x draught x Cb 0.45 x 1025, about her 101 tons "
            "burthen (Cb judgement, the cutter's: a beamy hull, fine at the ends for speed: "
            "luggers were built 'pour la marche', Lescallier 1791 p. 408).",
            "gm_m": "3 ft 11 in: judgement; a beamy hull that carried a great press of sail high "
            "when others reefed (Forfait 1788 p. 53), stiffer than the cutter.",
            "clr_x_m": "5 ft 3 in abaft the middle: judgement, measured (docs/dev/TuningNotes.md, "
            "package 43b). At 2 ft abaft, near Forfait's centre of effort (0.024 L abaft, Table "
            "VII), the great lugs to leeward griped her up into the wind as she gathered way "
            "with the rudder hard over; here she carries four degrees of weather helm at seven "
            "points and is nearly balanced close-hauled.",
            "lateral_area_m2": "LWL x draught x 0.85 (the cutter's rule).",
            "hull_speed_kn": f"1.34 sqrt({lwl_ft:.0f} ft).",
            "deck_height_m": "The deck about 3 ft 3 in above the water (judgement).",
            "rudder": "A blade about 8 ft deep (judgement).",
        },
    )

    def m(x_ft):
        return round(x_ft * FT, 1)

    peak = math.radians(25.0)  # the yard at 65 degrees to the mast (Forfait p. 53: 60 to 70)
    prov = " Provisional (truth 9), see gen_ships.py."
    masts = {
        # name: (Forfait's factor of B, place in ft before the middle, rake in/ft, heel/B)
        "fore": (2.759, 0.364 * L, 4.0 / 12.0, 0.17),
        "main": (3.455, -0.040 * L, 1.0, 0.26),
        "mizen": (1.888, -(L / 2.0 - 1.0), 2.0, 0.08),
    }
    yards = {"fore": 0.454 * L, "main": 0.573 * L, "mizen": 0.364 * L}
    topsail_yards = {"fore": 0.393 * L, "main": 0.424 * L}
    topmast_ft = 1.091 * B
    stem_x_ft = lwl_ft / 2.0 + 1.0
    built = {}
    lug_areas = {}
    lug_cut = {}  # package 57: each lug's corners in feet, its mast at the sling, the sling
    lines_canvas = {
        "fore": LUGGER_CANVAS["lug"],
        "main": LUGGER_CANVAS["lug"],
        "mizen": LUGGER_CANVAS["mizen"],
    }
    lug_rope = {"fore": 3.0, "main": 3.5, "mizen": 2.5}
    for name, (factor, x_ft, rake_in, heel_b) in masts.items():
        total = factor * B
        heel = heel_b * B
        above = total - heel - deck_above_lwl_ft
        rake_deg = round(math.degrees(math.atan(rake_in / 12.0)), 1)
        rake = math.tan(math.radians(rake_deg))
        yard_ft = yards[name]
        sling_h = above - 1.0  # hoisted to a foot below the sheave (Forfait p. 53)
        mast_at_sling = x_ft - rake * sling_h
        throat = (
            mast_at_sling + yard_ft / 3.0 * math.cos(peak),
            sling_h - yard_ft / 3.0 * math.sin(peak),
        )
        peak_pt = (
            mast_at_sling - 2.0 * yard_ft / 3.0 * math.cos(peak),
            sling_h + 2.0 * yard_ft / 3.0 * math.sin(peak),
        )
        if name == "mizen":
            # a standing lug: its tack at the mast, its clew to the outrigger's end over the
            # stern (0.364 L, two thirds of it outboard: judgement)
            tack = (x_ft + 1.0, 3.0)
            clew = (x_ft - 2.0 / 3.0 * 0.364 * L, 4.0)
        elif name == "fore":
            # the fore lug's tack at the stem head (Willaumez: the fore mast two or three feet
            # abaft the stem head; Holdsworth p. 104: the tack to a bumkin outside the stem),
            # its foot 0.9 of its yard (judgement, the narrower foot of a sail tacked forward)
            tack = (stem_x_ft, 3.0)
            clew = (tack[0] - 0.9 * yard_ft, 3.0)
        else:
            # the main lug's tack on the deck under its throat, before the mast; the foot as
            # long as the yard (judgement)
            tack = (throat[0], 3.0)
            clew = (tack[0] - 1.0 * yard_ft, 3.0)
        area_ft2, cx, cz = _quad_area_centroid([tack, throat, peak_pt, clew])
        area = round(area_ft2 * FT * FT)
        centre_h = round(deck_height + cz * FT, 1)
        lug_areas[name] = (area, cx, cz)
        lug_cut[name] = (tack, throat, peak_pt, clew, mast_at_sling, sling_h)
        mast = b.spar(
            f"{name}.mast",
            "mast",
            x_m=m(x_ft),
            rake_deg=rake_deg,
            height_m=ft(above),
            rating_kn=design_kn([(area, centre_h, "lug")], dw["lower"]),
            note=f"the {name} mast {total:.0f} ft heel to head, {factor} of the breadth "
            f"(Forfait 1788 Table VII p. 75, the 60-pied lougre), {above:.0f} ft above the deck; "
            f"the heel {heel:.1f} ft below the water-line ({heel_b} B, Fincham 1843 p. 61); "
            f"stationed {abs(x_ft):.1f} ft {'before' if x_ft > 0 else 'abaft'} the middle "
            f"(Forfait); raking {rake_deg} deg ({rake_in:.2g} in to the foot, Forfait). A few "
            "shrouds a side with runners (BASTAQUE, Willaumez 1831), the lee ones slacked to "
            f"trim the lug (Forfait p. 53).{prov}",
        )
        yard = b.spar(
            f"{name}.lug_yard",
            "lug_yard",
            on=mast,
            length_m=ft(yard_ft),
            height_m=ft(sling_h),
            rating_kn=design_kn([(area, centre_h, "lug")], dw["lug"]),
            note=f"the {name} lug's yard {yard_ft:.1f} ft ({yards[name] / L:.3f} of the length, "
            "Forfait Table VII), slung at a third of its length and peaked at 65 degrees to the "
            "mast (Forfait p. 53: 60 to 70), hoisted to a foot below the sheave; no braces and no "
            f"lifts ('les ralingues en font l'office', Forfait p. 53).{prov}",
        )
        dipping = name != "mizen"
        canvas = lines_canvas[name]
        sail = b.sail(
            f"{name}.lug",
            "lug",
            yard=yard,
            mast=mast,
            area_m2=area,
            reef_bands=2 if dipping else 1,
            x_m=m(cx),
            centre_height_m=centre_h,
            canvas_no=canvas[0],
            cloth_rating_kn=cloth(area, canvas[0]),
            dipping=dipping or None,
            # package 57: the cut as the generator works it, for the drawing: the yard slung a
            # third from its fore end, two thirds of the sail abaft the mast
            corners_m=[[m(px), m(pz)] for px, pz in (tack, throat, peak_pt, clew)],
            note=(
                f"the {name} lug, {area} m2, a dipping lug: two thirds of its cloth to leeward "
                "of the mast and its tack shifted in going about (Forfait pp. 5 to 6; Lescallier "
                "pp. 391 to 392; Steel 1794, LUGGER); its corners the tack, the yard's two ends "
                "and the clew, the foot as long as the yard (judgement); two reef-bands "
                "(judgement; Fincham p. 59: luggers carried 'two sets of sails, large and "
                "small')."
                if dipping
                else f"the mizen lug (tapecul), {area} m2: a standing lug, tacked at the mast and "
                "sheeted to its outrigger over the stern, not dipped in going about (Holdsworth "
                "1874 p. 104: the Yarmouth luggers' 'working mizen'; judgement); one reef-band."
            )
            + canvas_note(canvas),
        )
        b.line(
            f"{name}.lug_yard.halyard",
            "halyard",
            yard,
            rating=rope_kn(lug_rope[name], 2),
            note=f"the {name} lug's halyard, {lug_rope[name]} in, two parts (judgement): 'a "
            "halyard to each sail' (Forfait p. 53)."
            if name == "fore"
            else None,
        )
        b.line(f"{name}.lug.tack", "tack", sail, rating=rope_kn(lug_rope[name]))
        b.line(
            f"{name}.lug.sheet",
            "sheet",
            sail,
            rating=rope_kn(lug_rope[name] - 0.5, 2),
            parts=2,
            note="the sheet to the lee clew, shifted with the tack in going about (Steel 1794, "
            "LUGGER); two parts (judgement)."
            if name == "main"
            else (
                "the mizen's sheet, rove through the outrigger's end ('bout-dehors de tapecul', "
                "0.364 L, Forfait Table VII); two parts (judgement)."
                if name == "mizen"
                else None
            ),
        )
        b.sided(
            f"{name}.shrouds", "shroud", mast, rating=rope_kn(5.0 if name != "mizen" else 3.5, 2)
        )
        b.line(f"{name}.stay", "stay", mast, rating=rope_kn(5.0 if name != "mizen" else 3.5))
        built[name] = (mast, yard, sail, above, x_ft, rake, centre_h)

    # the lug topsails on the fore and main topmasts, fidded abaft the lower mast heads in
    # iron rings (Steel 1794, LUGGER; Lescallier 1791 p. 408: each mast with "un mât de hune
    # ... à l'arrière ... dans un cercle de fer", and lug topsails). Package 57 (the owner's
    # notes 1 to 4 of the Éclair's first cruise): they are lugs, not square topsails: a yard
    # slung a third from its fore end on the topmast, peaked as the lower lug's, the clew
    # sheeted to the lower lug's peak and the tack to the lower mast head, so that the sail
    # lies as the lower lug lies, on its side of the mast, and is trimmed with it by the
    # lower lug's sheet. Forfait's braces and lifts (p. 53: "les huniers seuls ont des bras,
    # des balancines & des boulines") are kept for the setting and the picture, not for a
    # square trim; his bowlines are left out, the tack doing a lug's bowline's office
    # (judgement). Set flying (the owner's note of 2026-10-17): swayed up from the deck with
    # the sail bent and sent down whole, never reefed aloft; in a breeze the topmast itself
    # is struck.
    topsails = []
    topsail_yards_built = []
    topmasts = []
    for name in ("fore", "main"):
        mast, yard, sail, above, x_ft, rake, _ch = built[name]
        tack_lo, _throat_lo, peak_lo, _clew_lo, mast_at_sling_lo, sling_lo = lug_cut[name]
        hoist = 0.75 * topmast_ft  # the quarter of it in the doubling (judgement)
        tm = b.spar(
            f"{name}.topmast",
            "topmast",
            steps_on=mast,
            height_m=ft(hoist),
            rating_kn=None,
            note=f"the {name} topmast {topmast_ft:.0f} ft, 1.091 of the breadth (Forfait Table "
            f"VII), fidded abaft the mast head in an iron ring (Steel 1794, LUGGER; Lescallier "
            f"1791 p. 408), {hoist:.0f} ft above the cap (judgement: a quarter of it in the "
            "doubling); struck and housed in a breeze, the topsail being sent down.",
        )
        ty_len = topsail_yards[name]
        ty_h = above + hoist - 1.0
        sling = (x_ft - rake * ty_h, ty_h)
        ts_throat = (
            sling[0] + ty_len / 3.0 * math.cos(peak),
            sling[1] - ty_len / 3.0 * math.sin(peak),
        )
        ts_peak = (
            sling[0] - 2.0 * ty_len / 3.0 * math.cos(peak),
            sling[1] + 2.0 * ty_len / 3.0 * math.sin(peak),
        )
        ts_tack = (mast_at_sling_lo, sling_lo)  # at the lower mast head, by the slings
        ts_clew = peak_lo  # sheeted to the lower lug's peak
        ts_area_ft2, ts_cx, ts_cz = _quad_area_centroid([ts_tack, ts_throat, ts_peak, ts_clew])
        ts_area = round(ts_area_ft2 * FT * FT)
        ts_centre = round(deck_height + ts_cz * FT, 1)
        b.doc["spars"][-1]["rating_kn"] = design_kn([(ts_area, ts_centre, "lug")], dw["topsail"])
        ty = b.spar(
            f"{name}.topsail.lug_yard",
            "lug_yard",
            on=tm,
            length_m=ft(ty_len),
            height_m=ft(ty_h),
            rating_kn=design_kn([(ts_area, ts_centre, "lug")], dw["topsail"]),
            note=f"the {name} topsail's yard {ty_len:.1f} ft ({ty_len / L:.3f} of the length, "
            "Forfait Table VII), a lug yard slung a third from its fore end and peaked as the "
            "lower lug's (Steel 1794, LUGGER: 'one on each lower-mast and topmast'); its braces "
            "and lifts are Forfait's (p. 53) for the setting and the picture: the sail is "
            f"trimmed by the lower lug's sheet, not braced.{prov}",
        )
        ts = b.sail(
            f"{name}.topsail",
            "lug",
            yard=ty,
            mast=tm,
            area_m2=ts_area,
            flying=True,
            sheeted_to=sail,
            x_m=m(ts_cx),
            centre_height_m=ts_centre,
            canvas_no=LUGGER_CANVAS["topsail"][0],
            cloth_rating_kn=cloth(ts_area, LUGGER_CANVAS["topsail"][0]),
            corners_m=[[m(px), m(pz)] for px, pz in (ts_tack, ts_throat, ts_peak, ts_clew)],
            note=f"the {name} lug topsail {ts_area} m2 (Lescallier 1791 p. 408: 'des huniers à "
            "bourcet'; the owner's notes of 2026-10-17): its corners the tack at the lower mast "
            "head, its yard's two ends, and the clew at the lower lug's peak, to which it is "
            "sheeted, so that it lies on the lower lug's side of the mast and at its angle; set "
            "flying, sent down whole, no reef-band." + canvas_note(LUGGER_CANVAS["topsail"]),
        )
        r = LUGGER_TOPSAIL_ROPE
        b.line(f"{ts}.halyard", "halyard", ty, rating=rope_kn(r["halyard"], 2))
        b.line(
            f"{ts}.sheet",
            "sheet",
            ts,
            rating=rope_kn(r["sheet"]),
            note="the lug topsail's sheet, to the lower lug's peak (package 57); one part."
            if name == "fore"
            else None,
        )
        b.line(f"{ts}.tack", "tack", ts, rating=rope_kn(r["sheet"]))
        b.sided(f"{ts}.brace", "brace", ty, rating=rope_kn(r["brace"]))
        b.sided(f"{ts}.lift", "lift", ty, rating=rope_kn(r["lift"]))
        topsails.append(ts)
        topsail_yards_built.append(ty)
        topmasts.append(tm)

    # -- the head: the running bowsprit and two jibs ---------------------------------------
    fore_mast, _fy, fore_lug, fore_above, fore_x, fore_rake, _fc = built["fore"]
    bowsprit_ft = 2.649 * B
    bowsprit_out = 0.55 * bowsprit_ft  # judgement: the rest inboard on the chevalet
    bowsprit_reefed = bowsprit_out * 2.0 / 3.0
    stem_x = round(stem_x_ft * FT, 1)

    def jib_sail(sid, tack_x, head_h, clew, sheet_in, canvas, stay, halyard_spar, words):
        tack = (tack_x, 3.0)
        head = (fore_x - fore_rake * head_h, head_h)
        luff = math.hypot(head[0] - tack[0], head[1] - tack[1])
        luff_used = 0.85 * luff
        head = (
            tack[0] + (head[0] - tack[0]) * 0.85,
            tack[1] + (head[1] - tack[1]) * 0.85,
        )
        area_ft2 = 0.5 * abs(
            (head[0] - tack[0]) * (clew[1] - tack[1]) - (head[1] - tack[1]) * (clew[0] - tack[0])
        )
        area = round(area_ft2 * FT * FT)
        x = (tack[0] + head[0] + clew[0]) / 3.0
        z = (tack[1] + head[1] + clew[1]) / 3.0
        sail = b.sail(
            sid,
            "jibheaded",
            stay=stay,
            halyard_spar=halyard_spar,
            area_m2=area,
            x_m=m(x),
            centre_height_m=round(deck_height + z * FT, 1),
            canvas_no=canvas[0],
            cloth_rating_kn=cloth(area, canvas[0]),
            note=f"{words} {area} m2: luff {luff_used:.0f} ft, 0.85 of the line from its halyard "
            "to "
            "its tack (Fincham art. 87's rule for a cutter's jib, judgement for a lugger's)."
            + canvas_note(canvas),
        )
        b.line(f"{sid}.halyard", "halyard", sail, rating=rope_kn(sheet_in, 2))
        b.sided(f"{sid}.sheet", "sheet", sail, rating=rope_kn(sheet_in))
        b.line(f"{sid}.downhaul", "downhaul", sail, rating=rope_kn(sheet_in - 0.5))
        return sail, area, x, z

    bowsprit = b.spar(
        "bowsprit",
        "bowsprit",
        x_m=stem_x,
        length_m=ft(bowsprit_out),
        height_m=1.5,
        running=True,
        housed_length_m=ft(bowsprit_reefed),
        rigged_out=True,
        rating_kn=None,
        note=f"the running bowsprit, {bowsprit_ft:.0f} ft in all, 2.649 of the breadth (Forfait "
        f"Table VII), long and little steeved (1 3/4 in to the foot, Forfait; Lescallier p. 408); "
        f"{bowsprit_out:.0f} ft outboard rigged out (0.55 of it, judgement), running in and out "
        "on a chevalet and an iron collar at the stem so that the jibs' effect is set 'plus ou "
        f"moins' (Forfait p. 53); reefed, {bowsprit_reefed:.0f} ft outboard (a third in, the "
        f"cutter's rule).{prov}",
    )
    b.line(
        "bowsprit.heel_rope",
        "outhaul",
        bowsprit,
        rating=rope_kn(3.5, 2),
        note="the heel-rope that runs the bowsprit out and in (the cutter's; judgement).",
    )
    b.line("bobstay", "stay", bowsprit, rating=rope_kn(5.0))
    b.line(
        "jib.stay",
        "stay",
        fore_mast,
        rating=rope_kn(3.5),
        note="the jib's luff line from the fore mast head; the jibs set flying on travellers.",
    )
    b.line("flying_jib.stay", "stay", topmasts[0], rating=rope_kn(2.5))
    jib, jib_area, jib_x, jib_z = jib_sail(
        "jib",
        stem_x_ft + bowsprit_reefed - 0.75,
        fore_above - 2.0,
        (stem_x_ft, 4.0),
        3.0,
        LUGGER_CANVAS["jib"],
        "jib.stay",
        None,
        "the jib (the inner), its tack at the reefed bowsprit's end, set whether the bowsprit "
        "is reefed or rigged out;",
    )
    fjib, fjib_area, fjib_x, fjib_z = jib_sail(
        "flying_jib",
        stem_x_ft + bowsprit_out - 0.75,
        fore_above + 0.75 * topmast_ft - 1.0,
        (stem_x_ft + 0.5 * bowsprit_reefed, 6.0),
        2.5,
        LUGGER_CANVAS["flying jib"],
        "flying_jib.stay",
        bowsprit,
        "the flying jib (the outer), its tack on the traveller at the bowsprit end, which wants "
        "the bowsprit rigged out (halyard_spar), from the fore topmast head ('un beaupré surmonté "
        "de deux ou plusieurs focs', Forfait p. 53);",
    )
    b.doc["spars"][[s["id"] for s in b.doc["spars"]].index("bowsprit")]["rating_kn"] = design_kn(
        [
            (jib_area, round(deck_height + jib_z * FT, 1), "jibheaded"),
            (fjib_area, round(deck_height + fjib_z * FT, 1), "jibheaded"),
        ],
        dw["lower"],
    )
    b.line("jib.outhaul", "outhaul", jib, rating=rope_kn(2.5))
    b.line("flying_jib.outhaul", "outhaul", fjib, rating=rope_kn(2.0))

    # -- storm canvas: the taille-vent and a storm jib -------------------------------------
    main_mast, main_yard, main_lug, main_above, main_x, main_rake, main_centre = built["main"]
    main_area, main_cx, main_cz = lug_areas["main"]
    tv_area = round(0.5 * main_area)
    tv_cz = 0.8 * main_cz  # a smaller yard hoisted lower (judgement)
    canvas = LUGGER_CANVAS["taille-vent"]
    tv = b.sail(
        "taille_vent",
        "lug",
        yard=main_yard,
        mast=main_mast,
        area_m2=tv_area,
        reef_bands=1,
        x_m=m(main_x - main_rake * tv_cz + 0.1 * yards["main"]),
        centre_height_m=round(deck_height + tv_cz * FT, 1),
        canvas_no=canvas[0],
        cloth_rating_kn=storm_cloth(tv_area),
        bent=False,
        in_place_of="main.lug",
        note=f"the taille-vent {tv_area} m2, about half the main lug (Forfait p. 52; Willaumez "
        "1831, TAILLE-VENT), its yard 0.7 of the main yard (Fincham 1843 p. 61, the chasse-marée's "
        "second suit; the file bends it to the main lug's yard), tacked at the foot of the mast "
        "and not to the side, so that it needs no shifting and is safe aback ('quand le Bâtiment "
        "vient vent devant, la plus grande portion de la voile se range dans la direction du "
        "vent', Forfait p. 52): a standing lug; set in place of the main lug in blowing weather; "
        "in the sail room." + canvas_note(canvas, storm=True),
    )
    b.line("taille_vent.tack", "tack", tv, rating=rope_kn(3.0))
    b.line("taille_vent.sheet", "sheet", tv, rating=rope_kn(3.0, 2), parts=2)
    sj_area = round(2.0 / 3.0 * jib_area)
    sj_canvas = LUGGER_CANVAS["storm jib"]
    sj = b.sail(
        "storm_jib",
        "jibheaded",
        stay="jib.stay",
        area_m2=sj_area,
        x_m=m(jib_x - 2.0),
        centre_height_m=round((deck_height + jib_z * FT) * math.sqrt(2.0 / 3.0), 1),
        canvas_no=sj_canvas[0],
        cloth_rating_kn=storm_cloth(sj_area),
        bent=False,
        in_place_of="jib",
        note=f"storm jib {sj_area} m2, two-thirds of the jib (Steel 1794 p. 190, the sloop's), "
        "its tack at the reefed bowsprit's end; in the sail room."
        + canvas_note(sj_canvas, storm=True),
    )
    b.line("storm_jib.halyard", "halyard", sj, rating=rope_kn(3.0, 2))
    b.sided("storm_jib.sheet", "sheet", sj, rating=rope_kn(3.0))
    b.line("storm_jib.downhaul", "downhaul", sj, rating=rope_kn(2.5))

    lugs = [built[n][2] for n in ("fore", "main", "mizen")]
    head_sails = [jib, fjib]
    # Forfait's check on the whole (Table VII, the 60-pied column): the sail area 4.037 L x B,
    # its centre of effort 0.024 L abaft the middle and 1.576 B above the water
    working = [(lug_areas[n][0], lug_areas[n][1]) for n in ("fore", "main", "mizen")]
    sails_doc = {sd["id"]: sd for sd in b.doc["sails"]}
    for sid in [s for s in topsails] + head_sails:
        sd = sails_doc[sid]
        working.append((sd["area_m2"], sd["x_m"] / FT))
    total_m2 = sum(a for a, _ in working)
    ce_ft = sum(a * x for a, x in working) / total_m2
    forfait_m2 = 4.037 * L * B * FT * FT
    b.notes["fore.mast"] = (
        b.notes["fore.mast"]
        + f" Forfait's check (Table VII, 60 pieds): the working canvas {total_m2:.0f} m2 against "
        f"4.037 L x B = {forfait_m2:.0f} m2 on her length and breadth; its centre "
        f"{abs(ce_ft) / L:.3f} L {'abaft' if ce_ft < 0 else 'before'} the middle against his "
        "0.024 L abaft."
    )

    b.group("lugs", lugs)
    b.group("dipping lugs", lugs[:2])
    b.group("topsails", topsails)
    # package 57: the lug topsails are lugs, set flying; she has no square sail and no yard
    # that is braced
    b.group("lug topsails", topsails)
    b.group("flying sails", topsails)
    b.group("headsails", head_sails)
    b.group("jibs", head_sails)
    b.group("fore-and-aft sails", head_sails + lugs + topsails)
    b.group("light sails", [fjib])
    b.group("plain sail", lugs + topsails + [jib])
    b.group("all sail", lugs + topsails + head_sails)
    b.group("topsail yards", topsail_yards_built)
    b.group("lower masts", [built[n][0] for n in ("fore", "main", "mizen")])
    b.group("topmasts", topmasts)
    b.group("storm canvas", [tv, sj])
    b.alias("the fore lug", "fore.lug")
    b.alias("foresail", "fore.lug")
    b.alias("the foresail", "fore.lug")
    b.alias("mainsail", "main.lug")
    b.alias("the mainsail", "main.lug")
    b.alias("the main", "main.lug")
    b.alias("mizen", "mizen.lug")
    b.alias("the mizen", "mizen.lug")
    b.alias("tapecul", "mizen.lug")
    b.alias("taille-vent", "taille_vent")
    b.alias("storm lug", "taille_vent")
    b.alias("head sails", "headsails")
    b.descriptions(
        [
            (
                "lugger",
                "a lugger",
                "a chasse-marée, three-masted under lugs",
                "L'Éclair's hull (RMG ZAZ6306) as the Breton and Norman coaster, fisherman or "
                "privateer of the war (Forfait 1788 pp. 52 to 55; spec M6 §19; judgement on the "
                "words).",
            )
        ]
    )
    ground_tackle_for(b, burthen, beam_ft, draught_ft)
    lugger_crew(b)
    hold_for(b, burthen, False, "a chasse-marée, a coaster deep in the hold: judgement")
    b.pumps(PUMPS_NOTE, pump_entries(0, 1, ["the pump"]))
    b.boats(
        BOATS_NOTE,
        boat_entries(
            lod_ft,
            False,
            [
                (
                    "boat",
                    "yawl",
                    "the boat",
                    1.0,
                    "The lugger's boat, a yawl (judgement).",
                    "data/ships/boat-yawl-16.yaml",
                ),
            ],
        ),
    )
    b.gear(
        GEAR_NOTE,
        [
            (
                "drift_nets",
                "drift nets",
                "the drift nets",
                {"nets": 60, "length_fathoms": 1000},
                "A fleet of drift nets for the pilchard, the mackerel, the herring and the "
                "sardine, shot at sunset over the quarter before the wind and ridden to by "
                "night (Holdsworth 1874 pp. 98 to 99, 106 to 111: a herring fleet a mile and a "
                "quarter, the pilchard nets of Cornwall 'about the size of those for herrings, "
                "but with a smaller mesh'); sixty nets and a thousand fathoms for her size, "
                "judgement.",
            ),
            (
                "lines",
                "lines",
                "the lines",
                {"length_fathoms": 3600, "hooks": 2340},
                "Longlines for the cod, the ling and the conger, shot under easy sail across "
                "the tide and hauled by short tacks (Holdsworth 1874 pp. 137 to 139: 180 lines "
                "of 40 fathoms and 4,680 hooks for a smack of 68 tons); half of it for a "
                "coaster's hands, judgement.",
            ),
        ],
    )
    b.dump(
        os.path.join(out_dir, "lugger.yaml"),
        "# The lugger: L'Éclair, a French gun-lugger taken in 1795 (RMG ZAZ6306), 101 tons, 59 ft\n"
        "# 3 in on deck by 20 ft 4 in, as the chasse-marée of the war (docs/design/\n"
        "# VesselReferences-2026-10.md § 1, decision 42). Generated by tools/gen_ships.py;\n"
        "# edit that script and rerun, do not edit this file. Spars: Forfait 1788, Table VII\n"
        "# (p. 75, the 60-pied lougre), the masts on her breadth and the yards on her length;\n"
        "# heels: Fincham 1843 p. 61; the\n"
        "# lug and its dip: Forfait pp. 5 to 6 and 52 to 55, Lescallier 1791 pp. 391 to 392 and\n"
        "# 408 to 409, Steel 1794 vol. I, LUGGER. Units: metres, m2, kg, kN. Comments mark\n"
        "# judgements. Package 43b (spec M6 §19; the proposal's §4.4): the lug and its dip are\n"
        "# the engine's additions, as the running bowsprit was the cutter's.\n",
    )


# The fishing gear (package 56, spec M7b §21a): what each fishing hull carries, and no
# other; the gear's evolutions are data/evolutions/shoot_*.yaml and haul_*.yaml, its
# fishing freesail/world/fishing.py with the grounds of data/fishing/.
GEAR_NOTE = (
    "The fishing gear (package 56, spec M7b §21a): what she carries and no other, each with "
    "its source; the evolutions that work it are data/evolutions/shoot_*.yaml and "
    "haul_*.yaml, its fishing the grounds' of data/fishing/; see tools/gen_ships.py."
)


def lugger_crew(b):
    b.crew(
        [
            (
                ("complement",),
                30,
                "Thirty: judgement. Forfait 1788 p. 54: the war lugger 'exige un équipage "
                "d'élite & "
                "fort nombreux'; no figure for her complement was found (the references note).",
            ),
            (
                ("names",),
                "french",
                "A Breton and Norman crew: the french list in data/crew/names.yaml.",
            ),
            (
                ("stations", "forecastle"),
                10,
                "Hands per station, both watches together; no tops: the fore lug, the jibs and "
                "the bowsprit, 10, judgement.",
            ),
            (
                ("stations", "afterguard"),
                10,
                "Afterguard, at the main and mizen lugs: 10, judgement.",
            ),
            (("stations", "waisters"), 5, "Waisters: 5, judgement."),
            (("stations", "idlers"), 2, "Idlers: the cook and a carpenter (spec M3 2.3)."),
            (
                ("ratings", "able"),
                0.7,
                "Share of the seamen by rating: 'un équipage d'élite' (Forfait p. 54). Able: 0.70.",
            ),
            (("ratings", "ordinary"), 0.25, "Ordinary: 0.25, judgement."),
            (("ratings", "landsman"), 0.05, "Landsmen: 0.05, judgement."),
        ]
        + [
            (
                ("posts", post),
                None,
                "Station holders by post (spec M3 2.3): the master who commands her, his mate "
                "and the boatswain; names are drawn at muster."
                if i == 0
                else None,
            )
            for i, post in enumerate(LUGGER_POSTS)
        ]
        + [
            (("idlers_by_trade", "cook"), 1, "The cook: 1, judgement."),
            (("idlers_by_trade", "carpenter's crew"), 1, "A carpenter: 1, judgement."),
            (
                ("stores", "water_tons"),
                4,
                "Stores for a month (judgement): 30 men at a gallon a day is about 4 tons.",
            ),
            (("stores", "provisions_days"), 30, "Provisions: a month (judgement)."),
            (("stores", "spare_spars"), {}, None),
            (("stores", "cordage_fathoms"), 80, "Spare rope (judgement)."),
            (
                ("stores", "shot_plugs"),
                4,
                SHOT_PLUGS_NOTE + " A lugger's 4.",
            ),
            *ration_entries(
                "the measure for a French vessel too, whose own ration the references do not "
                "give (judgement)"
            ),
        ]
    )
    b.people(
        "The named people beyond the posts (package 43b): a boy as the messenger; see "
        "tools/gen_ships.py.",
        LUGGER_DRAWN,
    )
    b.spare_spars(
        "The booms: a spare lug yard and a spare topmast (judgement: the lugger's masting 'est "
        "sujette à des accidens fréquens', Forfait p. 54).",
        [
            ("lug_yard", 1, "A spare lug yard (judgement)."),
            ("topmast", 1, "A spare topmast (judgement)."),
        ],
    )
    b.sail_room(
        "The sail room (spec 3b §6.3), every sail new; see tools/gen_ships.py.",
        [
            ("main.lug", LUGGER_CANVAS["lug"][0], "A spare main lug and jib (judgement)."),
            ("jib", LUGGER_CANVAS["jib"][0], None),
            (
                "taille_vent",
                LUGGER_CANVAS["taille-vent"][0],
                "The taille-vent for a blow and a storm jib (Forfait p. 52).",
            ),
            ("storm_jib", LUGGER_CANVAS["storm jib"][0], None),
        ],
    )


# ---------------------------------------------------------------------------
# The smack: the Culloden smack of 1746 (package 43b; spec M6 §19; decision 42)
# ---------------------------------------------------------------------------
#
# Sources (docs/design/VesselReferences-2026-10.md § 2, the owner's choice of 2026-10-10,
# decision 42). The hull is the Navy's smack Culloden, stationed in Scotland, built at
# Plymouth in 1746 by B. Slade: gun deck 43 ft, keel 34 ft 0 in, breadth 14 ft 0 in, depth
# 5 ft 6 in, 35 tons, 8 men, 2 guns (Charnock 1802 vol. III p. 274, Hoys and Transports,
# read from the page image). The Navy's rule passes: 34 x 14 x 7 / 94 = 35.4 tons. The
# check on her shape is Chapman's English smack for flatfish (1768, plate LIX No. 3: 38.2
# ft between perpendiculars, 13.3 ft moulded, 6.3 ft draught). The spars are Steel's
# "Proportions of masts, yards, &c. for sloops, smacks, and hoys" (1794 vol. I p. 41, read
# from the page image): the mast and topmast in one, 3 3/4 the breadth; to the hounds 3/4
# of the whole; the boom 2/3 of the mast, the gaff 3/5 of the boom; the cross-jack (square
# sail) yard 3/5 of the mast, the topsail yard 4/5 of the cross-jack yard; the bowsprit 5/9
# of the mast (the fraction's small type uncertain). The bowsprit runs in a ring of iron
# and comes inboard (Lescallier 1791 p. 420: "leur bout de beaupré est mobile dans un
# cercle de fer qui le contient, & peut se rentrer très-facilement en-dedans du
# Bâtiment"), the cutter's running bowsprit; her foresail carries a bonnet more often than
# reef bands (Steel, 'Smack's foresail'). The rules for the sails' shapes are the
# cutter's, Fincham's arts. 86 and 87, for want of a smack's own (Lescallier: "le
# Gréement est semblable à celui des Sloops"). The well is Holdsworth's (1874 pp. 139 to
# 140): two water-tight bulkheads across the vessel amidships, holes bored in her bottom,
# the well-deck holding the water's level; its size is judgement. Her trade (Holdsworth
# pp. 137 to 141, 231 to 232): a Harwich welled cod smack of the North Sea working
# longlines on the Dogger, or a trawler; in the game, the fisherman of the Channel's
# grounds at far detail and a small handy vessel in the regatta (spec M6 §19, §21).

SMACK_CANVAS: dict[str, tuple[int, str]] = {
    "main.sail": (
        2,
        f"{STEEL_SM} p. 120, 'Cutter's mainsail' (a smack is rigged as a sloop): No. 1 or 2",
    ),
    "fore.staysail": (2, f"{STEEL_SM}, 'Smack's foresail' (OCR line 15622): No. 1 or 2"),
    "jib": (2, f"{STEEL_SM}, 'Smack's jib' (OCR line 15709): No. 1 or 2"),
    "square_sail": (
        6,
        f"{STEEL_SM} p. 124, 'Sloop's square-sail, or cross-jack': No. 6 or 7; the heavier taken",
    ),
    "topsail": (6, f"{STEEL_SM} p. 125, 'Sloop's topsail': No. 6 or 7"),
    "storm trysail": (1, f"{STEEL_SM}, 'Cutter's trysail' (OCR line 14359): No. 1 or 2"),
    "storm jib": (
        1,
        f"{STEEL_SM}, the sloop's jibs (p. 190): 'No. 1 or 2 ... two-thirds of the size of the "
        "first jib, and is used in stormy weather, in lieu of a larger one'",
    ),
}

# Rope sizes: the cutter's square sail's and topsail's (judgement: a smack of 35 tons, a
# third of the cutter's, her gear a size lighter), rated by Luce 1866 ch. IV.
SMACK_ROPE = {
    "square_sail": {
        "halyard": 2.5,
        "sheet": 2.25,
        "brace": 1.5,
        "lift": 1.5,
        "clewline": 1.5,
        "buntline": 1.25,
        "bowline": 1.5,
        "reef_tackle": 1.5,
    },
    "topsail": {
        "halyard": 2.0,
        "sheet": 2.0,
        "brace": 1.25,
        "lift": 1.25,
        "clewline": 1.25,
        "buntline": 1.0,
        "bowline": 1.25,
        "reef_tackle": 1.25,
    },
}
SMACK_POSTS, SMACK_DRAWN = wardroom("smack")


def smack(out_dir="data/ships"):
    dw = dict(DESIGN_WIND_KN, square_sail=22.0)  # the square sail a fair-wind sail, as the cutter's
    # -- hull ---------------------------------------------------------------------------
    lod_ft = 43.0  # the gun deck (Charnock)
    keel_ft = 34.0
    beam_ft = 14.0
    burthen = 35.0
    lwl_ft = 40.0  # judgement between the keel and the deck: a plumb stem, a raking post
    # draught: the cutter's rule for the type, half her breadth aft, and a foot and a half
    # less forward; the mean 6 ft 3 in, Chapman's English smack's 6.3 ft the check
    draught_aft_ft = 0.5 * beam_ft
    draught_fwd_ft = draught_aft_ft - 1.5
    draught_ft = (draught_aft_ft + draught_fwd_ft) / 2.0
    lwl, beam, draught = ft(lwl_ft), ft(beam_ft), ft(draught_ft)
    # Displacement: Cb 0.45, the cutter's (Holdsworth p. 66: the old smacks "were built
    # with the principal object of living through anything"); the well's water is counted
    # in it, since it moves with her though it buoys her not (judgement on Holdsworth's well).
    displacement = round(lwl * beam * draught * 0.45 * 1025.0, -2)
    deck_height = 0.75  # judgement: low-sided, about 2 ft 6 in above the water
    deck_above_lwl_ft = deck_height / FT
    rake_deg = round(math.degrees(math.atan(1.5 / 36.0)), 1)  # Steel: cutters 1.5 in to the yard

    b = Builder(
        "Culloden",
        "smack",
        "The Navy's smack Culloden (built at Plymouth by B. Slade, 1746, stationed in "
        "Scotland): 35 tons burthen, 43 ft on the gun deck, 34 ft keel, 14 ft breadth, 5 ft "
        "6 in depth, 8 men and 2 guns (Charnock 1802 vol. III p. 274); cutter-rigged with "
        "a running bowsprit (Lescallier 1791 p. 420) by Steel's proportions for sloops, smacks "
        "and hoys (1794 vol. I p. 41), with a well amidships (Holdsworth 1874 pp. 139 to 140; "
        "Steel 1805, WELL). The fisherman of the Channel's grounds and the small handy vessel "
        "of the regatta (spec M6 §19); see tools/gen_ships.py for every rule.",
        {
            "length_waterline_m": lwl,
            "beam_m": beam,
            "draught_m": draught,
            "displacement_kg": displacement,
            "gm_m": 0.9,
            "clr_x_m": -0.3,
            "lateral_area_m2": round(lwl * draught * 0.85),
            "hull_speed_kn": round(1.34 * math.sqrt(lwl_ft), 1),
            "deck_height_m": deck_height,
            "rudder": {"area_m2": 0.7, "max_angle_deg": 35, "rate_deg_s": 6.0, "span_m": 2.0},
        },
        {
            "length_waterline_m": f"{lwl_ft:.0f} ft: judgement between the {keel_ft:.0f} ft keel "
            f"and the {lod_ft:.0f} ft gun deck (Charnock vol. III p. 274), a plumb stem and a "
            "raking post.",
            "beam_m": "14 ft 0 in (Charnock vol. III p. 274).",
            "draught_m": f"{draught_ft:.2f} ft mean: {draught_aft_ft:.1f} ft aft, half her breadth "
            f"(the cutter's rule for the type, judgement), {draught_fwd_ft:.1f} ft forward; "
            "Chapman's English smack (1768, plate LIX No. 3) draws 6.3 ft. Her depth in hold, 5 "
            "ft 6 in (Charnock), is the check that she is not deeper.",
            "displacement_kg": "LWL x beam x draught x Cb 0.45 x 1025, about 1.3 x the 35 tons "
            "burthen: the cutter's block (judgement; Holdsworth p. 66, the old smacks 'built with "
            "the principal object of living through anything'). The well's water counts in it: it "
            "moves with her though it buoys her not (hold.well_m3; judgement on Holdsworth).",
            "gm_m": "3 ft: judgement; a smack was stiff and heavily ballasted, a little less "
            "than the cutter's 3 ft 7 in on her narrower beam.",
            "clr_x_m": "Judgement, as the cutter's: the centre of pressure a little before the "
            "middle so that she is nearly balanced close-hauled and carries a little weather helm "
            "on a beam reach (measured; docs/dev/TuningNotes.md, package 43b).",
            "lateral_area_m2": "LWL x draught x 0.85 for a deep full profile (the cutter's rule).",
            "hull_speed_kn": f"1.34 sqrt({lwl_ft:.0f} ft).",
            "deck_height_m": "The deck about 2 ft 6 in above the water (judgement).",
            "rudder": "A blade about 6 ft 6 in deep by 1 ft 2 in (judgement, the cutter's in "
            "small).",
        },
    )

    # -- spars by Steel's proportions for sloops, smacks and hoys (1794 vol. I p. 41) ------
    mast_total = 3.75 * beam_ft  # mast and topmast in one, 3 3/4 the breadth
    hounds_from_heel = 0.75 * mast_total  # to the hounds 3/4 of the whole
    below_lwl = 0.269 * beam_ft  # the cutter's heel below the water-line (Fincham p. 67)
    step_to_deck = below_lwl + deck_above_lwl_ft
    mast_above = mast_total - step_to_deck
    hounds_above = hounds_from_heel - step_to_deck
    boom_ft = 2.0 / 3.0 * mast_total
    gaff_ft = 3.0 / 5.0 * boom_ft
    sq_yard = 3.0 / 5.0 * mast_total  # the cross-jack yard
    ts_yard = 4.0 / 5.0 * sq_yard
    bowsprit_ft = 5.0 / 9.0 * mast_total
    bowsprit_housed = 0.60 * beam_ft  # inboard, the cutter's rule (Fincham)
    bowsprit_out = bowsprit_ft - bowsprit_housed
    bowsprit_reefed = bowsprit_out * 2.0 / 3.0
    # the mast stepped well forward for a large mainsail (Holdsworth pp. 70 to 71, of the
    # trawl smacks), 0.15 of the water-line before the middle (judgement; the cutter's 0.101)
    mast_x_ft = 0.15 * lwl_ft
    mast_x = round(mast_x_ft * FT, 1)
    stem_x_ft = lwl_ft / 2.0 + 1.0
    stem_x = round(stem_x_ft * FT, 1)
    rake = math.tan(math.radians(rake_deg))

    def raked(z_above_deck_ft):
        return mast_x_ft - rake * z_above_deck_ft

    def m(x_ft):
        return round(x_ft * FT, 1)

    nock = hounds_above - 0.045 * hounds_from_heel
    boom_h = 4.0  # judgement: the boom's jaws 4 ft above the deck
    gaff_rise = math.tan(math.radians(27.0))
    sq_yard_h = hounds_above  # the square sail's yard hoisted to the hounds
    ts_yard_h = mast_above - 1.5  # the topsail's under the masthead

    def trapezoid(head_ft, foot_ft, depth_ft):
        return round((head_ft + foot_ft) / 2.0 * depth_ft * FT * FT)

    main_foot = 0.92 * boom_ft
    main_head_ft = 0.92 * gaff_ft
    main_hoist = nock - boom_h
    main_area = round(
        (
            (main_foot + main_head_ft) / 2.0 * main_hoist
            + 0.5 * main_head_ft * gaff_rise * main_head_ft
        )
        * FT
        * FT
    )
    main_z = boom_h + 0.45 * main_hoist
    main_centre = round(deck_height + main_z * FT, 1)
    sq_depth = 0.8 * main_hoist
    sq_area = round(0.9 * sq_yard * sq_depth * FT * FT)
    sq_z = sq_yard_h - 0.45 * sq_depth
    sq_centre = round(deck_height + sq_z * FT, 1)
    ts_depth = ts_yard_h - sq_yard_h
    ts_area = trapezoid(0.82 * ts_yard, 0.9 * sq_yard, ts_depth)
    ts_z = sq_yard_h + 0.5 * ts_depth
    ts_centre = round(deck_height + ts_z * FT, 1)
    # the foresail on the forestay from the hounds to the stem head (Fincham art. 87)
    fs_tack = (stem_x_ft, 1.0)
    fs_head_full = (raked(hounds_above), hounds_above)
    stay_len = math.hypot(fs_head_full[0] - fs_tack[0], fs_head_full[1] - fs_tack[1])
    fs_luff = 0.85 * stay_len
    fs_foot = 0.9 * (stem_x_ft - mast_x_ft)
    fs_leech = 0.8 * fs_luff
    s = (fs_luff + fs_foot + fs_leech) / 2.0
    fs_area = round(math.sqrt(s * (s - fs_luff) * (s - fs_foot) * (s - fs_leech)) * FT * FT)
    fs_head = (
        fs_tack[0] + (fs_head_full[0] - fs_tack[0]) * fs_luff / stay_len,
        fs_tack[1] + (fs_head_full[1] - fs_tack[1]) * fs_luff / stay_len,
    )
    fs_clew = (stem_x_ft - fs_foot, 3.0)
    fs_x = (fs_tack[0] + fs_head[0] + fs_clew[0]) / 3.0
    fs_z = (fs_tack[1] + fs_head[1] + fs_clew[1]) / 3.0
    # the jib: tack 9 in short of the bowsprit end, luff 0.8 of the line from the mast's
    # head above the hounds to the tack (Fincham art. 87), clew at the stem head
    jib_tack = (stem_x_ft + bowsprit_out - 0.75, 2.0)
    jib_halyard_h = hounds_above + 0.5 * (mast_above - hounds_above)
    jib_halyard = (raked(jib_halyard_h), jib_halyard_h)
    jib_stay_len = math.hypot(jib_halyard[0] - jib_tack[0], jib_halyard[1] - jib_tack[1])
    jib_luff = 0.8 * jib_stay_len
    jib_head = (
        jib_tack[0] + (jib_halyard[0] - jib_tack[0]) * jib_luff / jib_stay_len,
        jib_tack[1] + (jib_halyard[1] - jib_tack[1]) * jib_luff / jib_stay_len,
    )
    jib_clew = (stem_x_ft, 3.5)
    jib_area = round(
        0.5
        * abs(
            (jib_head[0] - jib_tack[0]) * (jib_clew[1] - jib_tack[1])
            - (jib_head[1] - jib_tack[1]) * (jib_clew[0] - jib_tack[0])
        )
        * FT
        * FT
    )
    jib_x = (jib_tack[0] + jib_head[0] + jib_clew[0]) / 3.0
    jib_z = (jib_tack[1] + jib_head[1] + jib_clew[1]) / 3.0
    prov = " Provisional (truth 9), see gen_ships.py."

    mast = b.spar(
        "main.mast",
        "mast",
        x_m=mast_x,
        rake_deg=rake_deg,
        height_m=ft(mast_above),
        rating_kn=design_kn(
            [
                (main_area, main_centre, "gaff"),
                (sq_area, sq_centre, "square"),
                (ts_area, ts_centre, "square"),
                (fs_area, round(deck_height + fs_z * FT, 1), "jibheaded"),
                (jib_area, round(deck_height + jib_z * FT, 1), "jibheaded"),
            ],
            dw["lower"],
        ),
        note=f"the mast and topmast in one stick, {mast_total:.1f} ft heel to head, 3 3/4 the "
        f"breadth (Steel 1794 vol. I p. 41, sloops, smacks and hoys), {mast_above:.0f} ft above "
        f"the deck; the hounds 3/4 of the whole from the heel ({hounds_above:.0f} ft above the "
        f"deck); stepped {below_lwl:.1f} ft below the water-line (Fincham's cutter, 0.269 of "
        f"the breadth); raking {rake_deg} deg (Steel: cutters 1.5 in to the yard); stationed "
        f"0.15 of the water-line before the middle, well forward for a large mainsail "
        f"(Holdsworth 1874 pp. 70 to 71; judgement on the figure). No topmast to strike: the "
        f"topsail yard crosses the mast's own head.{prov}",
    )
    gaff = b.spar(
        "main.gaff",
        "gaff",
        on=mast,
        length_m=ft(gaff_ft),
        height_m=ft(nock),
        rating_kn=design_kn([(main_area, main_centre, "gaff")], dw["gaff"]),
        note=f"gaff {gaff_ft:.0f} ft, 3/5 of the boom (Steel p. 41); its jaws at the nock, "
        f"{nock:.0f} ft above the deck (the cutter's rule after Fincham art. 89).",
    )
    boom = b.spar(
        "main.boom",
        "boom",
        on=mast,
        length_m=ft(boom_ft),
        height_m=ft(boom_h),
        horse_m=round(0.5 * beam, 1),
        rating_kn=design_kn([(main_area, main_centre, "gaff")], dw["gaff"]),
        note=f"boom {boom_ft:.0f} ft, 2/3 of the mast (Steel p. 41), over the counter; "
        f"{boom_h:.0f} ft above the deck (judgement); horse_m " + HORSE_NOTE,
    )
    sqy = b.spar(
        "square_sail.yard",
        "yard",
        on=mast,
        length_m=ft(sq_yard),
        height_m=ft(sq_yard_h),
        brace_limit_deg=58,
        rating_kn=design_kn([(sq_area, sq_centre, "square")], dw["square_sail"]),
        note=f"the cross-jack yard {sq_yard:.1f} ft, 3/5 of the mast (Steel p. 41), the square "
        "sail's, hoisted to the hounds; braces 58 deg from square, as the cutter's (judgement). "
        "Willaumez 1831, SMACK: a square sail hoisted and lowered with its yard." + prov,
    )
    sq = b.sail(
        "square_sail",
        "square",
        yard=sqy,
        area_m2=sq_area,
        reef_bands=1,
        x_m=m(raked(sq_z)),
        centre_height_m=sq_centre,
        canvas_no=SMACK_CANVAS["square_sail"][0],
        cloth_rating_kn=cloth(sq_area, SMACK_CANVAS["square_sail"][0]),
        note=f"square sail {sq_area} m2 (Steel 1794 p. 124, 'Sloop's square-sail, or "
        f"cross-jack': {sq_depth:.0f} ft deep, four-fifths of the mainsail's fore-leech; one "
        "reef-band, judgement); a fair-wind sail, in the light sails."
        + canvas_note(SMACK_CANVAS["square_sail"]),
    )
    square_sail_lines(b, sq, sqy, SMACK_ROPE["square_sail"], hoisting=True, reef=True, bowline=True)
    tsy = b.spar(
        "topsail.yard",
        "yard",
        on=mast,
        length_m=ft(ts_yard),
        height_m=ft(ts_yard_h),
        brace_limit_deg=64,
        rating_kn=design_kn([(ts_area, ts_centre, "square")], dw["topsail"]),
        note=f"topsail yard {ts_yard:.1f} ft, 4/5 of the cross-jack yard (Steel p. 41), on the "
        "mast's head above the hounds; braces 64 deg from square, as the cutter's (judgement)."
        + prov,
    )
    ts = b.sail(
        "topsail",
        "square",
        yard=tsy,
        area_m2=ts_area,
        x_m=m(raked(ts_z)),
        centre_height_m=ts_centre,
        canvas_no=SMACK_CANVAS["topsail"][0],
        cloth_rating_kn=cloth(ts_area, SMACK_CANVAS["topsail"][0]),
        note=f"topsail {ts_area} m2, {ts_depth:.0f} ft deep between its yard and the square "
        "sail's (Steel 1794 p. 125; Willaumez 1831, SMACK: her topsail, when she carries one, "
        "hollow in the foot and sheeted to the deck); light canvas."
        + canvas_note(SMACK_CANVAS["topsail"]),
    )
    square_sail_lines(b, ts, tsy, SMACK_ROPE["topsail"], hoisting=True)
    mainsail = b.sail(
        "main.sail",
        "gaff",
        mast=mast,
        gaff=gaff,
        boom=boom,
        area_m2=main_area,
        reef_bands=3,
        x_m=m(raked(main_z) - 0.4 * main_foot),
        centre_height_m=main_centre,
        canvas_no=SMACK_CANVAS["main.sail"][0],
        cloth_rating_kn=cloth(main_area, SMACK_CANVAS["main.sail"][0]),
        note=f"mainsail {main_area} m2: foot {main_foot:.0f} ft (0.92 of the boom), head "
        f"{main_head_ft:.0f} ft (0.92 of the gaff), hoist {main_hoist:.0f} ft to the nock, the "
        "gaff peaked 27 degrees (the cutter's rules, Fincham arts. 86 and 87); three reef-bands "
        "(judgement; the cutter's four on a larger sail)." + canvas_note(SMACK_CANVAS["main.sail"]),
    )
    b.line("main.gaff.throat_halyard", "throat_halyard", gaff, rating=rope_kn(2.5, 3))
    b.line("main.gaff.peak_halyard", "peak_halyard", gaff, rating=rope_kn(2.0, 4))
    b.line(
        "main.sail.sheet",
        "sheet",
        mainsail,
        rating=rope_kn(2.75, 3),
        parts=3,
        note="2.75 in, a threefold purchase on the boom (judgement, the cutter's in small).",
    )
    b.line("main.sail.outhaul", "outhaul", mainsail, rating=rope_kn(1.75))
    b.sided("main.gaff.vang", "vang", gaff, rating=rope_kn(1.5))
    # -- the head: the running bowsprit, the forestay, the foresail and the jib ----------
    bowsprit = b.spar(
        "bowsprit",
        "bowsprit",
        x_m=stem_x,
        length_m=ft(bowsprit_out),
        height_m=1.0,
        running=True,
        housed_length_m=ft(bowsprit_reefed),
        rigged_out=True,
        rating_kn=design_kn(
            [(jib_area, round(deck_height + jib_z * FT, 1), "jibheaded")], dw["lower"]
        ),
        note=f"the running bowsprit: {bowsprit_ft:.0f} ft in all, 5/9 of the mast (Steel p. 41, "
        f"the fraction uncertain in the small type), {bowsprit_housed:.0f} ft of it inboard "
        f"(the cutter's 0.60 of the breadth) and {bowsprit_out:.0f} ft outboard rigged out; it "
        "runs in a ring of iron and comes inboard (Lescallier 1791 p. 420), as the cutter's "
        f"does; reefed, {bowsprit_reefed:.0f} ft outboard (a third in, the cutter's)."
        f"{prov}",
    )
    b.line(
        "bowsprit.heel_rope",
        "outhaul",
        bowsprit,
        rating=rope_kn(2.5, 2),
        note="the heel-rope that runs the bowsprit out and in (Steel 1794, HEEL-ROPE); 2.5 in, "
        "two parts (judgement).",
    )
    b.line(
        "fore.stay",
        "stay",
        mast,
        rating=rope_kn(5.0),
        note="the forestay, from the hounds to the stem head; the foresail sets on it with "
        "hanks (Steel 1794, 'Smack's foresail'). 5 in (judgement).",
    )
    b.line(
        "jib.stay",
        "stay",
        mast,
        rating=rope_kn(3.0),
        note="the jib's luff line from the mast's head to the bowsprit end: the jib sets flying "
        "on the traveller (Steel 1794, 'Smack's jib': 'hoists by haliards, without a stay'), "
        "named so that the engine and the viewer find its luff, as the cutter's. 3 in "
        "(judgement).",
    )
    b.sided(
        "main.shrouds",
        "shroud",
        mast,
        rating=rope_kn(4.5, 3),
        note="3 shrouds of 4.5 in a side (judgement).",
    )
    b.sided(
        "main.runner",
        "backstay",
        mast,
        rating=rope_kn(3.0, 2),
        note="the runners, a pair (judgement, the cutter's backstays in small).",
    )
    b.line("bobstay", "stay", bowsprit, rating=rope_kn(4.5))
    foresail = b.sail(
        "fore.staysail",
        "jibheaded",
        stay="fore.stay",
        area_m2=fs_area,
        x_m=m(fs_x),
        centre_height_m=round(deck_height + fs_z * FT, 1),
        canvas_no=SMACK_CANVAS["fore.staysail"][0],
        cloth_rating_kn=cloth(fs_area, SMACK_CANVAS["fore.staysail"][0]),
        note=f"the foresail on the forestay, {fs_area} m2 (Fincham art. 87's rules, the cutter's: "
        f"foot {fs_foot:.0f} ft, luff {fs_luff:.0f} ft, leech {fs_leech:.0f} ft). Steel's smack's "
        "foresail has two reef bands 'sometimes, but a bonnet is more frequently used'; the "
        "catalogue reefs no jib-headed sail and has no bonnet yet."
        + canvas_note(SMACK_CANVAS["fore.staysail"]),
    )
    b.line("fore.staysail.halyard", "halyard", foresail, rating=rope_kn(2.0, 2))
    b.sided("fore.staysail.sheet", "sheet", foresail, rating=rope_kn(2.0))
    b.line("fore.staysail.downhaul", "downhaul", foresail, rating=rope_kn(1.5))
    jib = b.sail(
        "jib",
        "jibheaded",
        stay="jib.stay",
        halyard_spar=bowsprit,
        area_m2=jib_area,
        x_m=m(jib_x),
        centre_height_m=round(deck_height + jib_z * FT, 1),
        canvas_no=SMACK_CANVAS["jib"][0],
        cloth_rating_kn=cloth(jib_area, SMACK_CANVAS["jib"][0]),
        note=f"the jib, {jib_area} m2 (Fincham art. 87's rules, the cutter's): tack 9 in short of "
        f"the bowsprit end, {jib_tack[0] - stem_x_ft:.0f} ft before the stem, luff "
        f"{jib_luff:.0f} ft, clew at the stem head; it wants the bowsprit rigged out "
        "(halyard_spar), as the cutter's." + canvas_note(SMACK_CANVAS["jib"]),
    )
    b.line("jib.halyard", "halyard", jib, rating=rope_kn(2.5, 2))
    b.sided("jib.sheet", "sheet", jib, rating=rope_kn(2.25))
    b.line("jib.downhaul", "downhaul", jib, rating=rope_kn(1.75))
    b.line(
        "jib.outhaul",
        "outhaul",
        jib,
        rating=rope_kn(1.75),
        note="the traveller's outhaul (Lever 1808, 'The Jib'; judgement for the size).",
    )
    head_sails = [foresail, jib]
    # -- storm canvas: the cutter's rules ------------------------------------------------
    storm_canvas = SMACK_CANVAS["storm trysail"]
    st_head = 0.4 * main_head_ft
    st_luff = 0.75 * main_hoist
    st_leech = st_luff * 7.0 / 6.0
    st_foot = 0.75 * main_foot
    st_area = round((st_head + st_foot) / 2.0 * (st_luff + st_leech) / 2.0 * FT * FT)
    st_z = boom_h + 0.45 * st_luff
    st = b.sail(
        "storm_trysail",
        "gaff",
        mast=mast,
        gaff=gaff,
        boom=boom,
        area_m2=st_area,
        reef_bands=2,
        x_m=m(raked(st_z) - 0.4 * st_foot),
        centre_height_m=round(deck_height + st_z * FT, 1),
        canvas_no=storm_canvas[0],
        cloth_rating_kn=storm_cloth(st_area),
        bent=False,
        in_place_of="main.sail",
        note=f"storm trysail {st_area} m2 by the cutter's rules (Steel 1794, 'Cutter's "
        "trysail'), bent in place of the mainsail; in the sail room."
        + canvas_note(storm_canvas, storm=True),
    )
    b.line("storm_trysail.sheet", "sheet", st, rating=rope_kn(2.75, 3), parts=3)
    b.line("storm_trysail.outhaul", "outhaul", st, rating=rope_kn(1.75))
    sj_area = round(2.0 / 3.0 * jib_area)
    sj_tack_x = stem_x_ft + bowsprit_reefed - 0.75
    sj_x = (sj_tack_x + jib_head[0] + jib_clew[0]) / 3.0
    sj_canvas = SMACK_CANVAS["storm jib"]
    sj = b.sail(
        "storm_jib",
        "jibheaded",
        stay="jib.stay",
        area_m2=sj_area,
        x_m=m(sj_x),
        centre_height_m=round((deck_height + jib_z * FT) * math.sqrt(2.0 / 3.0), 1),
        canvas_no=sj_canvas[0],
        cloth_rating_kn=storm_cloth(sj_area),
        bent=False,
        in_place_of="jib",
        note=f"storm jib {sj_area} m2, two-thirds of the jib (Steel 1794 p. 190), its tack at the "
        "reefed bowsprit's end; in the sail room." + canvas_note(sj_canvas, storm=True),
    )
    b.line("storm_jib.halyard", "halyard", sj, rating=rope_kn(2.25, 2))
    b.sided("storm_jib.sheet", "sheet", sj, rating=rope_kn(2.25))
    b.line("storm_jib.downhaul", "downhaul", sj, rating=rope_kn(1.75))
    storm = [st, sj]

    # groups: the smack's working sail is her mainsail, foresail and jib (Holdsworth pp. 70
    # to 71 and 137 to 139: under easy sail to shoot the lines, the foresail lowered to haul
    # them); the square sail and the topsail are her light canvas, for a fair wind
    b.group("courses", [sq])
    b.group("topsails", [ts])
    b.group("square sails", [sq, ts])
    b.group("headsails", head_sails)
    b.group("jibs", [jib])
    b.group("staysails", [foresail])
    b.group("gaff sails", [mainsail])
    b.group("fore-and-aft sails", head_sails + [mainsail])
    b.group("light sails", [sq, ts])
    b.group("plain sail", [mainsail, foresail, jib])
    b.group("all sail", [mainsail, sq, ts, foresail, jib])
    b.group("yards", [sqy, tsy])
    b.group("main yards", [sqy, tsy])
    b.group("lower yards", [sqy])
    b.group("topsail yards", [tsy])
    b.group("lower masts", [mast])
    b.group("storm canvas", storm)
    b.group("square sail bowlines", [f"square_sail.bowline.{s}" for s in SIDES])
    b.alias("square sail bowline", "square sail bowlines")
    b.alias("mainsail", "main.sail")
    b.alias("the main", "main.sail")
    b.alias("foresail", "fore.staysail")
    b.alias("the fore", "fore.staysail")
    b.alias("the crossjack", "square_sail")
    b.alias("the crossjack yard", "square_sail.yard")
    b.alias("trysail", "storm_trysail")
    b.alias("storm mainsail", "storm_trysail")
    b.alias("head sails", "headsails")
    b.alias("the mast", "main.mast")
    b.alias("main mast", "main.mast")
    b.descriptions(
        [
            (
                "smack",
                "a smack",
                "a fishing smack, her well amidships",
                "The Culloden smack's hull (Charnock vol. III p. 274) as the fisherman of the "
                "Channel's grounds (spec M6 §19; judgement on the words).",
            )
        ]
    )
    ground_tackle_for(b, burthen, beam_ft, draught_ft)
    smack_crew(b)
    hold_for(b, burthen, False, "a fishing smack's hold forward and aft of her well: judgement")
    well_m3 = round(10.0 * 8.0 * 4.0 * FT**3, 1)  # judgement: 10 ft by 8 by 4 below the water
    b.doc["hold"]["well_m3"] = well_m3
    b.hold_note += (
        f" The well, {well_m3} m3 (10 ft by 8 by 4 ft below the water-line, judgement), the "
        "water-tight compartment amidships open to the sea through holes in her bottom "
        "(Holdsworth 1874 pp. 139 to 140; Steel 1805, WELL), where the live cod are kept."
    )
    b.pumps(PUMPS_NOTE, pump_entries(0, 1, ["the pump"]))
    b.boats(
        BOATS_NOTE,
        boat_entries(
            lod_ft,
            False,
            [
                (
                    "boat",
                    "yawl",
                    "the boat",
                    0.8,
                    "The smack's boat, for the lines and the shore (Holdsworth pp. 137 to 139; "
                    "judgement on the size).",
                )
            ],
        ),
    )
    b.gear(
        GEAR_NOTE,
        [
            (
                "trawl",
                "trawl",
                "the trawl",
                {"beam_ft": 36.0, "length_fathoms": 120},
                "A beam trawl of 36 ft, the smallest of the deep-sea trawls and the Yarmouth "
                "men's (Holdsworth 1874 pp. 47, 59), towed with the tide under easy sail at half "
                "a knot to a knot and a half faster than the stream, five or six hours a haul, "
                "and hove up by the winch in three quarters of an hour (pp. 70 to 71, 77 to "
                "79); the warp 120 fathoms, judgement.",
            ),
            (
                "lines",
                "lines",
                "the lines",
                {"length_fathoms": 3600, "hooks": 2340},
                "Longlines, 90 lines of 40 fathoms and 2,340 hooks baited with whelks: half of "
                "the 68-ton cod smack's string (Holdsworth 1874 pp. 137 to 139), judgement on "
                "her size; the cod put alive into the well.",
            ),
            (
                "seine",
                "seine",
                "the seine",
                {"length_fathoms": 80},
                "A tuck-sean of 80 fathoms, eight deep at the sleeves and ten at the bunt, shot "
                "round a shoal from the boat in a bay by day and tucked into the boat at once "
                "(Holdsworth 1874 p. 158: 'where only one net is used for the whole process ... "
                "the net is called ... either a stop-sean or a tuck-sean'). The pilchard seans "
                "of St Ives and the south coast were the seine companies' with their own boats "
                "(pp. 188 to 195); a smack's own small sean worked by her boat is judgement, "
                "for the spec's truth 105.",
            ),
        ],
    )
    b.dump(
        os.path.join(out_dir, "smack.yaml"),
        "# The smack: Culloden, the Navy's smack of 1746 (B. Slade, Plymouth), 35 tons, 43 ft on\n"
        "# the gun deck by 14 ft (Charnock 1802 vol. III p. 274; docs/design/VesselReferences-\n"
        "# 2026-10.md § 2, decision 42). Generated by tools/gen_ships.py; edit that script and\n"
        "# rerun, do not edit this file. Spars: Steel 1794 vol. I p. 41, 'Proportions of masts,\n"
        "# yards, &c. for sloops, smacks, and hoys'; the sails' shapes the cutter's (Fincham 1843\n"
        "# arts. 86, 87); canvas: Steel's smack's and sloop's sails; the running bowsprit:\n"
        "# Lescallier 1791 p. 420; the well: Holdsworth 1874 pp. 139 to 140. Units: metres, m2,\n"
        "# kg, kN. Comments mark judgements. Package 43b (spec M6 §19): no engine change but the\n"
        "# hold's well.\n",
    )


def smack_crew(b):
    b.crew(
        [
            (
                ("complement",),
                8,
                "Eight: the Culloden's men (Charnock vol. III p. 274); Holdsworth's cod smacks of "
                "twice her tonnage carried nine to eleven (p. 141).",
            ),
            (("names",), "english", "A smack's crew: the english list in data/crew/names.yaml."),
            (
                ("stations", "forecastle"),
                3,
                "Hands per station, both watches together; a smack has no tops: three for the "
                "head sails, the bowsprit and the lines, judgement.",
            ),
            (("stations", "afterguard"), 2, "Afterguard, at the main sheet: 2, judgement."),
            (("stations", "idlers"), 1, "The cook (spec M3 2.3)."),
            (
                ("ratings", "able"),
                0.8,
                "Share of the seamen by rating: fishermen bred to it (judgement). Able: 0.80.",
            ),
            (("ratings", "ordinary"), 0.2, "Ordinary: 0.20, the apprentices (Holdsworth p. 141)."),
            (("ratings", "landsman"), 0.0, "No landsmen."),
        ]
        + [
            (
                ("posts", post),
                None,
                "Station holders by post (spec M3 2.3): the master who commands her and his "
                "mate; names are drawn at muster."
                if i == 0
                else None,
            )
            for i, post in enumerate(SMACK_POSTS)
        ]
        + [
            (("idlers_by_trade", "cook"), 1, "The cook: 1, judgement."),
            (
                ("stores", "water_tons"),
                1,
                "Stores for a fortnight on the grounds (judgement): water for eight men, a ton.",
            ),
            (("stores", "provisions_days"), 14, "Provisions: a fortnight (judgement)."),
            (("stores", "spare_spars"), {}, None),
            (("stores", "cordage_fathoms"), 40, "Spare rope (judgement)."),
            (
                ("stores", "shot_plugs"),
                2,
                SHOT_PLUGS_NOTE + " A smack's 2.",
            ),
            *ration_entries("the measure for a smack's men, found by her owner (judgement)"),
        ]
    )
    b.people(
        "The named people beyond the posts (package 43b): the boy as the messenger; see "
        "tools/gen_ships.py.",
        SMACK_DRAWN,
    )
    b.spare_spars(
        "The booms: a spare topsail yard (judgement).",
        [("yard", 1, "A spare topsail yard (judgement).")],
    )
    b.sail_room(
        "The sail room (spec 3b §6.3), every sail new; see tools/gen_ships.py.",
        [
            ("jib", SMACK_CANVAS["jib"][0], "A spare jib (judgement)."),
            (
                "storm_trysail",
                SMACK_CANVAS["storm trysail"][0],
                "Storm canvas, one of each (spec 3b §6.4, judgement).",
            ),
            ("storm_jib", SMACK_CANVAS["storm jib"][0], None),
        ],
    )


# ---------------------------------------------------------------------------------------
# The boats as ships (package 82, item 4; docs/design/Design-BoatAndPersonAboard.md §5.1):
# five patterns of boat the game sends away as a vessel, each a file of her own by which she
# is manned as a hull of the world, the ships' `boats:` lists pointing at them with `file:`.
# The ladder is honest: no boat's lines are on file and no period plan of a boat is read;
# Luce's rule of breadth is a named period rule and the rest is judgement that names what it
# differs from, each line marked so in its note. Steel 1805's Folio LVII ("Dimensions and
# scantlings of boats", IA leaves 599 to 602; the OCR at l. 43444 is garbled) is the better
# source and is named in every file as "to read": read, its figures replace the judgement in
# the file and the drawing, never the game's behaviour (the ships session's principle 12),
# since nothing the oars or the sail read is taken from the shape.
# ---------------------------------------------------------------------------------------

# The oar force's three figures (the design's §5.2; `freesail/physics/oars.py`), the same in
# every boat's file: a man's pull on the blade at no way, his power at the oar over hours,
# and the hours at the oars that halve his strength. Judgement, fitted to the brief's words
# (three to four knots light under four oars, a knot and a half towing, the men tiring by
# the hour); the period's books give no figure for a man's power at an oar (Falconer 1780,
# OAR; Steel 1805 p. 181).
OAR_THRUST_N = 50.0
OAR_POWER_W = 60.0
OAR_TIRING_H = 4.0
OARS_NOTE = (
    "The oars (package 82; the design's §5.2): the thrust of one oar is min(thrust_n, "
    "power_w / way) x the stroke x the men's tiring, 1 / (1 + hours / tiring_h); thrust_n a "
    "man's pull on the blade at no way, power_w his power at the oar over hours, tiring_h the "
    "hours that halve his strength. Judgement, fitted to the brief's words (three to four knots "
    "light under four oars, a knot and a half towing, the men tiring by the hour); the oar a "
    "lever of the second class striking the water (Falconer 1780, OAR), which gives no figure. "
    "Read by freesail/physics/oars.py and by nothing else."
)
BOAT_FILE_NOTE = (
    "To read: Steel 1805, Folio LVII, 'Dimensions and scantlings of boats' (IA leaves 599 to "
    "602), which gives the pattern's dimensions by length; read, its figures replace the "
    "judgement here, and never the game's behaviour."
)
# The patterns: (file stem, the kind, the words, the length in feet, the depth in feet, the
# draught laden in feet, the displacement laden in kg, the oars, the mast above the gunwale in
# feet, the lug in square feet, which boats of the eight she is the class of, her sources).
BOAT_PATTERNS = (
    (
        "boat-yawl-16",
        "yawl",
        "a 16-ft four-oared boat with a standing lug stepped at will",
        16.0,
        1.75,
        1.17,
        1000.0,
        4,
        12.0,
        60.0,
        "the lugger's boat (16 ft), the brig's jolly boat (16 ft) and the cutter's boat (15 ft: "
        "the difference of a foot is recorded in the cutter's note and never moved)",
        "Falconer 1780, YAWL ('a wherry or small ship's boat, usually rowed by four or six "
        "oars'); Steel 1805 p. 181 (OCR l. 11336 to 11380: the yawl 'less than the pinnace', "
        "the boats 'constructed for rowing or sailing'); Steel 1794 vol. II, the boats' stores "
        "table (the YAWL or CUTTER column: masts, sails and halyards allowed, OCR l. 20713, "
        "21856, 22936); Luce 1866, 'Boats'.",
    ),
    (
        "boat-cutter-28",
        "cutter",
        "the frigate's first cutter, an eight-oared boat with a lug",
        28.0,
        2.75,
        1.5,
        2900.0,
        8,
        17.0,
        160.0,
        "the frigate's first cutter (28 ft); her second cutter (25 ft) is the same pattern "
        "smaller and is recorded so, no file",
        "Steel 1805 p. 181 ('ships' cutters ... shorter, broader, and deeper, in proportion ... "
        "clincher built, and constructed for sailing or rowing'); Luce 1866 'Boats' (the first "
        "cutter 0.9 of the launch); the frigate's file (Luce's rule, 0.9 x 31).",
    ),
    (
        "boat-launch-31",
        "launch",
        "the frigate's launch, a ten-oared boat with a lug, fit to weigh an anchor",
        31.0,
        3.25,
        1.83,
        4500.0,
        10,
        19.0,
        250.0,
        "the frigate's launch (31 ft)",
        "Steel 1805 p. 181 ('the launch ... longer, more flat in its bottom, and lower ... "
        "better calculated for rowing and approaching a flat shore'; 'fit to weigh an "
        "anchor'); Steel 1794 vol. I ('sent in the long-boat', the stream anchor, OCR l. "
        "5739); Luce 1866 'Boats' (2.6 root(L)); the water she brings off in gang casks is her "
        "load (Luce's weight rule for the launch herself, 2.5 lb x B^2 x L, gives about 2.1 "
        "tons).",
    ),
    (
        "boat-launch-25",
        "launch",
        "the brig's launch, an eight-oared boat with a lug",
        25.0,
        2.75,
        1.5,
        2700.0,
        8,
        16.0,
        160.0,
        "the brig's launch (25 ft); the merchant brig's long-boat (20 ft) and the schooners' "
        "long-boats (20 ft) are the pattern smaller and recorded so, no file",
        "as the frigate's launch; the brig's file (Luce's rule, 2.6 root(95)).",
    ),
    (
        "boat-cutter-23",
        "cutter",
        "the brig's cutter, a six-oared boat with a lug",
        23.0,
        2.33,
        1.25,
        1900.0,
        6,
        14.0,
        110.0,
        "the brig's cutter (23 ft)",
        "as the frigate's cutter; the brig's file.",
    ),
)
BOAT_CANVAS = (
    8,
    "No. 8 canvas, the lightest Steel's sail-maker uses for small boats' sails "
    "(judgement after Steel 1794 vol. I, the canvas numbers)",
)


def boat(out_dir, pattern):
    """One boat's file from a `BOAT_PATTERNS` row: her hull from the length by Luce's rule of
    breadth (a quarter of the length) and the judged depth, draught and displacement; one
    mast stepped at will with a standing lug and its halyard, tack and sheet; her oars (the
    `oars:` section); a coxswain and the oarsmen; a grapnel, filed as the smallest anchor the
    schema knows; no guns, no hold, no boats."""
    stem, kind, words, L_ft, depth_ft, draught_ft, disp, oars, mast_ft, lug_ft2, of_the, src = (
        pattern
    )
    B_ft = L_ft * BOAT_BREADTH_OF_LENGTH
    lwl, beam, draught = ft(L_ft), ft(B_ft), ft(draught_ft)
    gunwale_m = round((depth_ft - draught_ft) * FT, 2)
    hull_speed = round(1.34 * math.sqrt(L_ft), 1)
    b = Builder(
        "the boat",
        "boat",
        f"{words[:1].upper()}{words[1:]}: the pattern of {of_the}. A boat of the ships' files "
        "(package 82; docs/design/Design-BoatAndPersonAboard.md §5), manned as a hull of the "
        "world when she is commanded and the script's boat on her errands otherwise; her name "
        f"is her ship's ('the Raven's boat') when she is manned. Sources: {src} "
        f"{BOAT_FILE_NOTE} Built by tools/gen_ships.py; edit the script and rerun.",
        {
            "length_waterline_m": lwl,
            "beam_m": beam,
            "draught_m": draught,
            "displacement_kg": disp,
            "gm_m": 0.5,
            "clr_x_m": 0.0,
            "lateral_area_m2": round(lwl * draught * 0.85, 2),
            "hull_speed_kn": hull_speed,
            "deck_height_m": gunwale_m,
            "rudder": {
                "area_m2": round(0.016 * L_ft, 2),
                "max_angle_deg": 35,
                "rate_deg_s": 20.0,
                "span_m": round(depth_ft * FT, 2),
            },
        },
        {
            "length_waterline_m": f"{L_ft:.0f} ft, the boat's length (the pattern's; judgement "
            "from the ships' boats lists, which Luce's rule sizes).",
            "beam_m": f"{B_ft:.2f} ft, a quarter of the length (Luce 1866, 'Boats': a named "
            "period rule).",
            "draught_m": f"{draught_ft:.2f} ft laden (judgement: to read, Steel 1805 Folio LVII).",
            "displacement_kg": f"{disp:,.0f} kg laden: the boat herself by Luce's weight rule "
            "and her men and their gear the rest (judgement).",
            "gm_m": "0.5 m, a boat's (judgement: an open boat is tender under sail and stiff "
            "with her men sat low).",
            "clr_x_m": "Amidships (judgement).",
            "lateral_area_m2": "LWL x draught x 0.85, the small vessels' rule.",
            "hull_speed_kn": f"1.34 sqrt({L_ft:.0f} ft).",
            "deck_height_m": f"The gunwale {depth_ft - draught_ft:.2f} ft above the water laden "
            f"(a depth of {depth_ft:.2f} ft less the draught; judgement); a man standing in her "
            "looks from 1.7 m over it (freesail/world/lookout.py).",
            "rudder": f"A yoke's rudder hung on the transom, {0.016 * L_ft:.2f} m2 (a boat's "
            "rudder is large for her size, about a sixtieth of a square metre to the foot of "
            "her length: judgement after the yawl's and the launch's blades), as deep as her "
            "depth, put over quickly by the coxswain's yoke lines (judgement).",
        },
    )
    # -- the rig: one mast stepped at will, a standing lug ------------------------------
    yard_ft = round(0.9 * mast_ft, 1)
    lug_m2 = round(lug_ft2 * FT * FT, 1)
    mast_x = round(0.25 * lwl, 1)  # a quarter of the length before the middle (judgement)
    sling_ft = mast_ft - 0.8
    tack = (mast_x / FT + 0.5, 1.5)
    throat = (mast_x / FT + yard_ft / 3.0 * 0.5, sling_ft - yard_ft / 3.0 * 0.85)
    peak = (mast_x / FT - 2.0 * yard_ft / 3.0 * 0.5, sling_ft + 2.0 * yard_ft / 3.0 * 0.85)
    clew = (mast_x / FT - 0.9 * yard_ft, 2.0)
    _area, cx, cz = _quad_area_centroid([tack, throat, peak, clew])
    centre_h = round(gunwale_m + cz * FT, 1)
    dw = 25.0  # the wind the rig is rated to carry its whole lug in (judgement: a boat reefs early)
    mast = b.spar(
        "mast",
        "mast",
        x_m=mast_x,
        height_m=ft(mast_ft),
        rating_kn=design_kn([(lug_m2, centre_h, "lug")], dw),
        note=f"one mast of {mast_ft:.0f} ft above the gunwale, stepped at will in a thwart's "
        "clamp and unstepped to pull (Steel 1794 vol. II, the boats' stores table: masts, sails "
        "and halyards allowed to the yawl and the cutter), unstayed; judgement on the length "
        f"(about 0.6 of the boat's). {BOAT_FILE_NOTE}",
    )
    yard = b.spar(
        "lug_yard",
        "lug_yard",
        on=mast,
        length_m=ft(yard_ft),
        height_m=ft(sling_ft),
        rating_kn=design_kn([(lug_m2, centre_h, "lug")], dw),
        note=f"the lug's yard {yard_ft:.0f} ft, 0.9 of the mast, slung at a third and peaked "
        "(judgement after the luggers' practice, Forfait 1788 p. 53).",
    )
    sail = b.sail(
        "lug",
        "lug",
        yard=yard,
        mast=mast,
        area_m2=lug_m2,
        reef_bands=1,
        x_m=round(cx * FT, 1),
        centre_height_m=centre_h,
        canvas_no=BOAT_CANVAS[0],
        cloth_rating_kn=cloth(lug_m2, BOAT_CANVAS[0]),
        corners_m=[[round(px * FT, 1), round(pz * FT, 1)] for px, pz in (tack, throat, peak, clew)],
        note=f"a standing lug of {lug_ft2:.0f} sq ft ({lug_m2} m2), tacked at the mast and "
        "not dipped, one reef-band (judgement after the yawl's and cutter's columns of Steel "
        f"1794's boats' stores); {BOAT_CANVAS[1]}.",
    )
    b.line(
        "lug_yard.halyard",
        "halyard",
        yard,
        rating=rope_kn(1.5),
        note="the halyard, 1.5 in (judgement).",
    )
    b.line("lug.tack", "tack", sail, rating=rope_kn(1.25))
    b.line(
        "lug.sheet",
        "sheet",
        sail,
        rating=rope_kn(1.25),
        note="the sheet, 1.25 in, in hand (judgement).",
    )
    # -- the oars ------------------------------------------------------------------------
    b.oars(OARS_NOTE, oars, OAR_THRUST_N, OAR_POWER_W, OAR_TIRING_H)
    # -- her people: the coxswain and the oarsmen -----------------------------------------
    b.crew(
        [
            (
                ("complement",),
                oars + 1,
                f"A coxswain and {oars} oarsmen, one to an oar (the ships' boats lists: a crew "
                "of the oars and one).",
            ),
            (("names",), "english", "Her men are her ship's: the english list."),
            (
                ("stations", "waisters"),
                oars,
                "The oarsmen, filed at the waist's station, the nearest word the schema has for "
                "men on the thwarts (judgement).",
            ),
            (("ratings", "able"), 1.0, "A boat's crew are picked men: all able (judgement)."),
            (("posts", "coxswain"), None, "The coxswain who steers her and commands her crew."),
            (("stores", "water_tons"), 0.05, "A breaker of water (judgement)."),
            (("stores", "provisions_days"), 1, "A day's bread (judgement)."),
        ]
    )
    # -- a grapnel ----------------------------------------------------------------------
    b.ground_tackle(
        "A grapnel on a line (judgement): the one anchor a boat carries, filed as a kedge, the "
        "smallest anchor the schema knows.",
        [
            (
                "grapnel",
                "kedge",
                "the grapnel",
                round(1.0 * L_ft, 0),
                20.0,
                1.5,
                rope_kn(1.5),
                f"A grapnel of about {L_ft:.0f} lb on 20 fathoms of 1.5-in line (judgement).",
            )
        ],
    )
    b.dump(
        os.path.join(out_dir, f"{stem}.yaml"),
        f"# {words[:1].upper()}{words[1:]} (package 82, item 4): the pattern of {of_the}.\n"
        "# Generated by tools/gen_ships.py; edit that script and rerun, do not edit this file.\n"
        "# Breadth by Luce 1866's rule, a quarter of the length; the rest judgement that names\n"
        "# what it differs from, each line marked in its note; to read, Steel 1805 Folio LVII.\n"
        "# Units: metres, m2, kg, kN. Comments mark judgements. The oars' three figures and\n"
        "# the oar force: docs/design/Design-BoatAndPersonAboard.md §5.2.\n",
    )


def boat_yawl_16(out_dir="data/ships"):
    boat(out_dir, BOAT_PATTERNS[0])


def boat_cutter_28(out_dir="data/ships"):
    boat(out_dir, BOAT_PATTERNS[1])


def boat_launch_31(out_dir="data/ships"):
    boat(out_dir, BOAT_PATTERNS[2])


def boat_launch_25(out_dir="data/ships"):
    boat(out_dir, BOAT_PATTERNS[3])


def boat_cutter_23(out_dir="data/ships"):
    boat(out_dir, BOAT_PATTERNS[4])


# Package 75 (docs/design/Build-Ships.md §3.1 items 1 and 2; Design-Ship-Indefatigable.md
# §1.2): the new ships are built by their own modules under tools/ships/, run after the eight
# above in the order they are built (the lead's ruling of 2026-10-28, in
# docs/dev/M7-WorkPackages.md): the Indefatigable, the Prince de Neufchatel, the bilander, the
# 74. Each is named here from stage 0, a stub writing nothing until its builder fills it, so
# that no ship's builder edits this script. A module begins `import gen_ships as g` and takes
# every helper as `g.<name>`; it is imported only below, after `gen_ships` is made this running
# script, so that its Builders, DesignLoads and helpers are these, one copy (a Builder of one
# copy with a DesignLoad of another fails at `dump`: measured, Design-Ship-Indefatigable.md
# §1.2).
SHIP_MODULES = ("indefatigable", "neufchatel", "bilander", "bellerophon")


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "data/ships"
    os.makedirs(out, exist_ok=True)
    frigate(out)
    schooner(out)
    schooner(out, armed=True)
    cutter(out)
    brig(out)
    brig(out, merchant=True)
    lugger(out)
    smack(out)
    # the boats (package 82, item 4), after the eight whose lists point at them
    boat_yawl_16(out)
    boat_cutter_28(out)
    boat_launch_31(out)
    boat_launch_25(out)
    boat_cutter_23(out)
    # the per-ship modules, each `build(out_dir)`: `ships` is tools/ships/, this script's own
    # directory being on the path when it runs (the repository root, put before it, has none)
    sys.modules.setdefault("gen_ships", sys.modules[__name__])
    for name in SHIP_MODULES:
        importlib.import_module(f"ships.{name}").build(out)
    print(f"written to {out}", file=sys.stderr)
