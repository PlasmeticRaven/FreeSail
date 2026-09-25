"""Generate the two reference ship files from documented particulars and period rules.

Run from the repository root:  python tools/gen_ships.py [output directory]

This script is the source of `data/ships/frigate-36.yaml` and
`data/ships/topsail-schooner.yaml`. Do not hand-edit those files: change the
numbers or rules here and regenerate, so that the files, the rules that
produced them and the citations stay together (`git diff` must be empty after
a run). Every number that is a judgement rather than a citation is marked
"judgement" in the comment the script writes next to it.

How the numbers are made
------------------------

Hull particulars are taken from published dimensions (the frigate: the
Amazon class of 1795; the schooner: Kemp's Lynx of 1812, from the Admiralty
draught Chapelle reproduces in The Baltimore Clipper, 1930) and converted:
gundeck and keel length to a load waterline, burthen to a displacement, the
"depth in hold" to a draught. The schooner's rig, whose spar dimensions
Chapelle could not find, is reconstructed as he prescribes: by Fincham's
masting rules, checked against the spar tables he prints (Sea Lark 1812,
Spider 1835) and Marestier's measured schooners of 1820.

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
have that sail on her: royals to 20 knots, topgallants to 22, topsails and
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
import os
import re
import sys

import yaml

SIDES = ("starboard", "larboard")
FT = 0.3048

# Luce 1866 ch. IV: breaking strain of tarred hemp = 1044.9 lb x circumference^2 (inches);
# working load one third of that. In kN per square inch of circumference:
ROPE_KN_PER_SQ_IN = round(1044.9 * 4.44822 / 1000.0 / 3.0, 4)  # 1.5493

# The engine's force coefficient at the peak of each class's curve (data/sail_classes.yaml,
# |(C_L, C_D)| at the best angle). Package 10: if the curves change, change these and rerun.
PEAK_COEFF = {"square": 1.45, "studding": 1.17, "gaff": 1.62, "jibheaded": 1.61}

# Sustained load / static peak-coefficient load, measured with tools/measure_loads.py on the
# frigate on a beam reach with the yards trimmed to the wind: 0.9 at 35 knots under all
# sail, 0.7 at 20 knots under plain sail (heel takes area away, the ship's own way adds
# apparent wind, the trim is a little off the peak).
SUSTAINED_FRACTION = 0.85

# Wind (knots, true, at 10 m) in which a spar is expected to stand with all its sail set.
# Chosen for truth 9 with the current curves; provisional until package 10 (see docstring).
DESIGN_WIND_KN = {
    "lower": 55.0,  # lower masts and yards, bowsprit: a storm, and they carry courses reefed
    "topsail": 40.0,  # topmasts and topsail yards: a whole gale under close-reefed topsails
    "topgallant": 22.0,  # topgallant masts and yards: a strong breeze is their limit
    "royal": 20.0,  # royal masts and yards: royals come in when it freshens
    "jib_boom": 30.0,  # the jib is a stout sail, the boom less so
    "flying_jib_boom": 22.0,  # a light spar for a light sail
    "gaff": 45.0,  # spanker gaff and boom: the spanker is carried reefed in a gale
    "studding": 18.0,  # studding-sail booms: light spars, fair-weather sails
}

# Cloth rating as a fraction of area (kN per m2). The engine blows a sail out at 1.8 x this.
# Courses and topsails are of Nos. 1 to 3 canvas, the light sails of Nos. 6 to 8 (Luce 1884
# ch. XI, table of sails for the "Trenton" class; Lever 1827 "Sails": No. 1 the strongest,
# decreasing to No. 8). The default in the engine is 0.9, under which nothing ever blows
# out; the light-canvas fractions are set so that royals and topgallants go in a gale.
CLOTH_KN_PER_M2 = {
    "course": 0.9,
    "topsail": 0.9,
    "topgallant": 0.30,
    "royal": 0.25,
    "studding": 0.20,
    "jibheaded": 0.50,
    "gaff": 0.70,
}

RHO_AIR = 1.225
KNOT = 0.514444


def ft(x: float) -> float:
    """Feet to metres, one decimal."""
    return round(x * FT, 1)


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


def quarter(x: float) -> float:
    """Round a rope size to the nearest quarter inch."""
    return round(x * 4.0) / 4.0


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

    def spar(self, id, cls, note=None, **kw):
        d = {"id": id, "class": cls}
        d.update({k: v for k, v in kw.items() if v is not None})
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

    def line(self, id, cls, of, side=None, rating=None, note=None):
        d = {"id": id, "class": cls, "of": of}
        if side:
            d["side"] = side
        if rating:
            d["rating_kn"] = rating
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
        ship = ship_from_dict(probe, "rating pass")
        carried: dict[str, list[tuple[str, float, float, str]]] = {s: [] for s in ship.spars}
        for sail in ship.sails.values():
            for spar in ship.spar_chain(sail):
                carried[spar.id].append((sail.id, sail.area_m2, sail.centre_height_m, sail.cls))
            if sail.cls == "studding":
                boom = ship.spar_of_role(sail, "boom")
                if boom is not None:
                    carried[boom.id].append((sail.id, sail.area_m2, sail.centre_height_m, sail.cls))
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

    def dump(self, path, header):
        self.rate_spars()
        text = yaml.safe_dump(self.doc, sort_keys=False, allow_unicode=True, width=100)
        out = []
        in_hull = False
        for line in text.splitlines():
            if line.startswith("hull:"):
                in_hull = True
            elif in_hull and not line.startswith("  "):
                in_hull = False
            m = re.match(r"^- id: (\S+)$", line)
            if m and m.group(1) in self.notes:
                out.append("# " + self.notes[m.group(1)])
            m = re.match(r"^  (\w+):", line) if in_hull else None
            if m and m.group(1) in self.hull_notes:
                out.append("  # " + self.hull_notes[m.group(1)])
            out.append(line)
        with open(path, "w") as f:
            f.write(header + "\n".join(out) + "\n")


def square_sail_lines(b, sail, yard, sizes, hoisting, course=False, reef=False):
    """The essential running rigging of a square sail and its yard, rated from rope sizes.

    `sizes` maps a line class to a rope circumference in inches (halyard: the tye).
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
        b.sided(f"{sail}.bowline", "bowline", sail, rating=r["bowline"])
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
            "clr_x_m": 3.5,
            "lateral_area_m2": round(lwl * draught * 0.85, -1),
            "hull_speed_kn": 13.0,
            "deck_height_m": deck_height,
            "rudder": {"area_m2": 6.0, "max_angle_deg": 35, "rate_deg_s": 3.0},
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
            "lead of about 11 per cent of LWL ahead of it (judgement): +3.5 m. With this "
            "sail plan (centre of effort +3.0 m under plain sail) she carries 0.2 deg of "
            "weather helm close-hauled and 0.7 reaching in 15 kn; at the +2.5 m of M1 "
            "integration she carries 1.3 deg of lee helm. Package 10 checks truths 6 and 12.",
            "lateral_area_m2": "LWL x draught x 0.85 for the fullness of the profile.",
            "hull_speed_kn": "The best speed of 18-pounder frigates in sailing-quality "
            "reports is 12 to 13 knots (Winfield); the derived 1.34 sqrt(LWL ft) = 15.7 is "
            "a modern yacht's figure. Package 10 may tune within 12.5 to 13.5.",
            "deck_height_m": "Upper (gun) deck at midships, about 6 ft above the load line.",
            "rudder": "Blade about 15 ft by 4 ft 3 in; 35 degrees is the period stop.",
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

    plans = {
        "fore": [("course", 55), ("topsail", 58), ("topgallant", 60), ("royal", 62)],
        "main": [("course", 55), ("topsail", 58), ("topgallant", 60), ("royal", 62)],
        "mizzen": [("topsail", 58), ("topgallant", 60), ("royal", 62)],
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
                note=f"{name} {level} yard {g[yard_lengths[level]]:.0f} ft, {rule}.{prov}",
            )
            reef = {"course": 1, "topsail": 3, "topgallant": 0, "royal": 0}[level]
            sail = b.sail(
                sail_id,
                "square",
                yard=yard,
                area_m2=area,
                reef_bands=reef,
                x_m=x,
                centre_height_m=centre,
                cloth_rating_kn=round(CLOTH_KN_PER_M2[level] * area, 1),
                note=f"{name} {level}: {area} m2 between its yard and the yardarms below "
                f"(head {0.9 if level == 'course' else (0.82 if level == 'topsail' else 0.89):.2f} "
                f"of the yard); cloth {CLOTH_KN_PER_M2[level]:.2f} kN/m2.",
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
        brace_limit_deg=55,
        rating_kn=design_kn(
            [(areas["mizzen"]["topsail"][0], areas["mizzen"]["topsail"][1], "square")],
            DESIGN_WIND_KN["lower"],
        ),
        note=f"crossjack yard {g['yard']:.0f} ft, 5/7 of the main yard (Luce; Falconer: equal "
        "to the fore topsail yard); crosses no sail, spreads the mizzen topsail's foot.",
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
        rating_kn=design_kn([(SPANKER_AREA, SPANKER_CENTRE, "gaff")], DESIGN_WIND_KN["gaff"]),
        note=f"spanker boom {boom_ft:.0f} ft, half the main mast (Luce).",
    )
    spanker = b.sail(
        "mizzen.spanker",
        "gaff",
        mast="mizzen.mast",
        gaff=gaff,
        boom=boom,
        area_m2=SPANKER_AREA,
        reef_bands=2,
        x_m=-21.0,
        centre_height_m=SPANKER_CENTRE,
        cloth_rating_kn=round(CLOTH_KN_PER_M2["gaff"] * SPANKER_AREA, 1),
        note=f"spanker (driver) {SPANKER_AREA} m2: foot 0.9 of the boom, head 0.9 of the gaff, "
        "hoist from boom to jaws, gaff peaked 40 degrees; centre 0.4 of the boom abaft the mast.",
    )
    b.line("mizzen.gaff.throat_halyard", "throat_halyard", gaff, rating=rope_kn(4.5, 3))
    b.line("mizzen.gaff.peak_halyard", "peak_halyard", gaff, rating=rope_kn(4.0, 4))
    b.line("mizzen.spanker.sheet", "sheet", spanker, rating=rope_kn(5.0, 2))
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
            cloth_rating_kn=round(CLOTH_KN_PER_M2["jibheaded"] * area, 1),
            note=f"{sid.replace('_', ' ').replace('.', ' ')} {area} m2 (judgement from the "
            "stay's run: luff along the stay, foot to the boom end).",
        )
        size = {"fore.topmast_staysail": 3.5, "jib": 3.5, "flying_jib": 2.5}[sid]
        b.line(f"{sid}.halyard", "halyard", s, rating=rope_kn(size, 2))
        b.sided(f"{sid}.sheet", "sheet", s, rating=rope_kn(size))
        b.line(f"{sid}.downhaul", "downhaul", s, rating=rope_kn(quarter(size * 0.8)))
        headsails.append(s)
    mts = b.sail(
        "main.topmast_staysail",
        "jibheaded",
        stay="main.topmast.stay",
        area_m2=80,
        x_m=6.0,
        centre_height_m=18.0,
        cloth_rating_kn=round(CLOTH_KN_PER_M2["jibheaded"] * 80, 1),
        note="main topmast staysail 80 m2 (judgement).",
    )
    b.line("main.topmast_staysail.halyard", "halyard", mts, rating=rope_kn(3.0, 2))
    b.sided("main.topmast_staysail.sheet", "sheet", mts, rating=rope_kn(3.0))
    b.line("main.topmast_staysail.downhaul", "downhaul", mts, rating=rope_kn(2.5))

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
                    x_m=x,
                    centre_height_m=centre,
                    cloth_rating_kn=round(CLOTH_KN_PER_M2["studding"] * area, 1),
                    note=(
                        f"{name} {level} studding sail {area} m2: 0.4 of the yard wide, as deep as "
                        "the sail beside it (judgement)."
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

    # groups
    b.group("courses", sails_by_level["course"])
    b.group("topsails", sails_by_level["topsail"])
    b.group("topgallants", sails_by_level["topgallant"])
    b.group("royals", sails_by_level["royal"])
    b.group("headsails", headsails)
    b.group("jibs", headsails[1:])
    b.group("staysails", headsails[:1] + [mts])
    b.group("studdingsails", stuns)
    b.group("square sails", sum(sails_by_level.values(), []))
    b.group("fore-and-aft sails", headsails + [mts, spanker])
    b.group("light sails", sails_by_level["royal"] + [headsails[2], mts] + stuns)
    b.group(
        "plain sail",
        sails_by_level["course"]
        + sails_by_level["topsail"]
        + sails_by_level["topgallant"]
        + headsails[:2]
        + [spanker],
    )
    b.group("all sail", sum(sails_by_level.values(), []) + headsails + [mts, spanker] + stuns)
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
    b.alias("middle staysail", "main.topmast_staysail")
    b.alias("stuns'ls", "studdingsails")
    b.alias("studding sails", "studdingsails")
    b.alias("kites", "studdingsails")
    b.alias("head sails", "headsails")
    b.alias("topgallant sails", "topgallants")
    b.alias("upper yards", "topgallant yards")
    for name in ("fore", "main"):
        for level in ("lower", "topmast", "topgallant"):
            if name == "main" and level == "lower":
                continue
            b.group(
                f"{name} {level} studdingsails", [f"{name}.{level}.studdingsail.{s}" for s in SIDES]
            )
    b.dump(
        os.path.join(out_dir, "frigate-36.yaml"),
        "# Reference ship: Amazon, a 36-gun 18-pounder frigate of the Amazon class (Rule, 1795).\n"
        "# Generated by tools/gen_ships.py; edit that script and rerun, do not edit this file.\n"
        "# Hull: Winfield's published dimensions of the class. Spars: Luce 1866 ch. VII rules,\n"
        "# checked against Falconer 1780 art. YARD. Rope: Luce 1866 ch. IV (breaking strain of\n"
        "# tarred hemp, one third for the working load) and ch. VIII (sizes by class). Brace\n"
        "# limits: Luce 1866 ch. XXIV (d'Ulloa, Fincham). Spar ratings and cloth ratings are\n"
        "# provisional, set for truth 9 with the M1 sail curves; see the script's docstring.\n"
        "# Units: metres, m2, kg, kN. Comments mark each judgement.\n",
    )


# spanker geometry, shared by the mast rating and the sail (feet: boom 44, gaff 35, hoist 41)
SPANKER_AREA = 167
SPANKER_CENTRE = 9.8


# ---------------------------------------------------------------------------
# The schooner: a Baltimore-built topsail schooner of about 1804
# ---------------------------------------------------------------------------


def schooner(out_dir="data/ships"):
    # Design winds: as the frigate's, except that her topgallant gear is rated for 25 knots
    # (she heels and flies so in the untuned physics that 22 left it strained under plain
    # sail in 20) and the gaff-topsail pole for 22 (that sail comes in early).
    dw = dict(DESIGN_WIND_KN, topgallant=25.0, gaff_topsail=22.0)
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
            "clr_x_m": -0.4,
            "lateral_area_m2": round(lwl * draught * 0.78, -1),
            "hull_speed_kn": 11.5,
            "deck_height_m": deck_height,
            "rudder": {"area_m2": 2.0, "max_angle_deg": 35, "rate_deg_s": 4.0},
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
            "0.0625 of the base ahead of the centre of lateral area. Kept at -0.4 m: the "
            "helm the engine gives with this plan is checked in tools/gen_ships.py's report.",
            "lateral_area_m2": "LWL x draught x 0.78 for a profile that is deep aft only.",
            "hull_speed_kn": "The type's recorded best is 11 to 12 knots; the derived "
            "1.34 sqrt(LWL ft) = 12.4 is too generous. Package 10 may tune within 11 to 12.",
            "deck_height_m": "Port sills 3 ft 5 in above the water and 10 in above the deck "
            "(Spider's specification, Chapelle pp. 166-167): a low-sided vessel.",
            "rudder": "A deep narrow blade, about 11 ft by 2 ft.",
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
        "that is 0.57 of LWL (Fincham; Sea Lark's fore yard was 0.69, Chapelle p. 42).{prov}",
    )
    ts = b.sail(
        "fore.topsail",
        "square",
        yard=ty,
        area_m2=ts_area,
        reef_bands=2,
        x_m=round(raked(fore_x, ts_z), 1),
        centre_height_m=ts_centre,
        cloth_rating_kn=round(CLOTH_KN_PER_M2["topsail"] * ts_area, 1),
        note=f"fore topsail {ts_area} m2 between its yard and the fore yardarms, "
        f"{ts_depth:.0f} ft deep ('the extreme beam, nearly', Fincham); x carried aft by the rake.",
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
        },
        hoisting=True,
        reef=True,
    )
    tgy = b.spar(
        "fore.topgallant.yard",
        "yard",
        on=fore_tgm,
        length_m=ft(tg_yard),
        height_m=ft(tg_h),
        brace_limit_deg=60,
        rating_kn=design_kn([(tg_area, tg_centre, "square")], dw["topgallant"]),
        note=f"fore topgallant yard {tg_yard:.0f} ft, 0.48 of the fore yard (Fincham).{prov}",
    )
    tgs = b.sail(
        "fore.topgallant",
        "square",
        yard=tgy,
        area_m2=tg_area,
        x_m=round(raked(fore_x, tg_z), 1),
        centre_height_m=tg_centre,
        cloth_rating_kn=round(CLOTH_KN_PER_M2["topgallant"] * tg_area, 1),
        note=f"fore topgallant {tg_area} m2; light canvas.",
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
        cloth_rating_kn=round(CLOTH_KN_PER_M2["gaff"] * fore_area, 1),
        note=f"foresail {fore_area} m2: foot {fore_foot:.0f} ft (0.8 of the mainsail's, "
        f"Fincham) sheeting abaft the main mast, head on the gaff, hoist {fore_hoist:.0f} ft, "
        "gaff peaked 27 degrees; centre 0.4 of the foot abaft the raked mast.",
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
        rating_kn=design_kn([(main_area, main_centre, "gaff")], dw["gaff"]),
        note=f"main boom {main_boom:.0f} ft, 0.70 of LWL (Fincham; Sea Lark's 0.71, Chapelle "
        "p. 42), well over the taffrail.",
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
        cloth_rating_kn=round(CLOTH_KN_PER_M2["gaff"] * main_area, 1),
        note=f"mainsail {main_area} m2: foot {main_foot:.0f} ft from clew to mast, head 0.92 of "
        f"the gaff, hoist {main_hoist:.0f} ft to a nock {main_nock:.0f} ft above the deck "
        "(Fincham: 2 to 2.4 x the beam above water), gaff peaked 27 degrees; Spider's, on a "
        "23 ft beam, was 1982 sq ft (Chapelle p. 167).",
    )
    b.line("main.gaff.throat_halyard", "throat_halyard", mgaff, rating=rope_kn(3.5, 4))
    b.line("main.gaff.peak_halyard", "peak_halyard", mgaff, rating=rope_kn(3.0, 5))
    b.line(
        "main.sail.sheet",
        "sheet",
        mainsail,
        rating=rope_kn(4.0, 3),
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
        cloth_rating_kn=round(CLOTH_KN_PER_M2["jibheaded"] * gt_area, 1),
        note=f"main gaff topsail {gt_area} m2, luff on the topmast, foot along the gaff "
        "(Luce 1884 ch. XXXIV).",
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
            cloth_rating_kn=round(CLOTH_KN_PER_M2["jibheaded"] * area, 1),
            note=f"{sid.replace('_', ' ').replace('.', ' ')} {area} m2 (judgement from the "
            "stay's run).",
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
            cloth_rating_kn=round(CLOTH_KN_PER_M2["studding"] * stuns_area, 1),
            note=(
                f"fore topmast studding sail {stuns_area} m2 (judgement)."
                if side == SIDES[0]
                else None
            ),
        )
        for cls, size in (("halyard", 2.0), ("tack", 2.0), ("sheet", 1.75), ("downhaul", 1.5)):
            b.line(f"{s}.{cls}", cls, s, rating=rope_kn(size))
        stuns.append(s)
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
    b.dump(
        os.path.join(out_dir, "topsail-schooner.yaml"),
        "# Reference ship: Speedwell, a Baltimore-built topsail schooner of about 1804, to the\n"
        "# draught of Kemp's Lynx of 1812 (H.M. schooner Musquidobit; Chapelle, The Baltimore\n"
        "# Clipper, 1930, pp. 82-83, fig. 17). Generated by tools/gen_ships.py; edit that script\n"
        "# and rerun, do not edit this file. Rig: Fincham's masting rules as Chapelle gives them\n"
        "# (pp. 159-162), checked against his spar tables (Sea Lark pp. 41-42, Spider pp.\n"
        "# 165-167) and Marestier's schooners (pp. 113-115). Rope: Luce 1866 ch. IV. Rig details:\n"
        "# Luce 1884 ch. XXXIV. Spar and cloth ratings are provisional, set for truth 9 with the\n"
        "# M1 sail curves; see the script. Units: metres, m2, kg, kN. Comments mark judgements.\n",
    )


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "data/ships"
    os.makedirs(out, exist_ok=True)
    frigate(out)
    schooner(out)
    print(f"written to {out}", file=sys.stderr)
