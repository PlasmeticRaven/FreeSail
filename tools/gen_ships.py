"""Generate the two draft reference ship files.

Run from the repository root:  python tools/gen_ships.py

The YAML files under data/ships/ are the source of truth once written and may
be edited by hand (package 8 verifies their particulars against the references
in docs/references/). This script exists to save typing when a rig is first
laid out, and as a starting point for new rigs: copy the frigate() or
schooner() function, change the spars, sails and lines, and run it. Re-running
it overwrites the two draft files, so hand edits made since (brace limits,
clr_x_m) must be folded back in here first or they will be lost.

Hand edits since generation, folded in below: brace limits 55 to 62 degrees
from square (Luce: about 28 degrees of yard to keel when sharp up); frigate
clr_x_m +2.5 m.
"""

from __future__ import annotations

import sys

import yaml

SIDES = ("starboard", "larboard")


class Builder:
    def __init__(self, name, rig, era_notes, hull):
        self.doc = {
            "ship": {"name": name, "rig": rig, "era_notes": era_notes},
            "hull": hull,
            "spars": [],
            "sails": [],
            "lines": [],
            "groups": {},
            "aliases": {},
        }

    def spar(self, id, cls, **kw):
        d = {"id": id, "class": cls}
        d.update({k: v for k, v in kw.items() if v is not None})
        self.doc["spars"].append(d)
        return id

    def sail(self, id, cls, **kw):
        d = {"id": id, "class": cls}
        d.update({k: v for k, v in kw.items() if v is not None})
        self.doc["sails"].append(d)
        return id

    def line(self, id, cls, of, side=None, rating=None):
        d = {"id": id, "class": cls, "of": of}
        if side:
            d["side"] = side
        if rating:
            d["rating_kn"] = rating
        self.doc["lines"].append(d)
        return id

    def sided(self, base, cls, of, rating=None):
        for s in SIDES:
            self.line(f"{base}.{s}", cls, of, side=s, rating=rating)

    def group(self, name, members):
        self.doc["groups"][name] = members

    def alias(self, name, target):
        self.doc["aliases"][name] = target

    def dump(self, path, header):
        text = yaml.safe_dump(self.doc, sort_keys=False, allow_unicode=True, width=100)
        with open(path, "w") as f:
            f.write(header + text)


def square_sail_lines(b, sail, yard, hoisting, course=False, reef=False):
    """The essential running rigging of a square sail and its yard."""
    if hoisting:
        b.line(f"{yard}.halyard", "halyard", yard)
    b.sided(f"{yard}.brace", "brace", yard)
    b.sided(f"{yard}.lift", "lift", yard)
    b.sided(f"{sail}.sheet", "sheet", sail)
    b.sided(f"{sail}.clewline", "clewline", sail)
    b.line(f"{sail}.buntline", "buntline", sail)
    if course:
        b.sided(f"{sail}.tack", "tack", sail)
        b.sided(f"{sail}.bowline", "bowline", sail)
    if reef:
        b.sided(f"{sail}.reef_tackle", "reef_tackle", sail)


def frigate():
    b = Builder(
        "Amazon",
        "ship",
        "Draft particulars for a 36-gun 18-pounder frigate of the 1790s. "
        "Dimensions and sail areas are approximate and to be checked (WP8).",
        {
            "length_waterline_m": 43.5,
            "beam_m": 11.9,
            "draught_m": 4.9,
            "displacement_kg": 1400000,
            "gm_m": 1.3,
            "clr_x_m": 2.5,
            "lateral_area_m2": 170,
            "deck_height_m": 2.0,
            "rudder": {"area_m2": 7.5, "max_angle_deg": 35, "rate_deg_s": 3.0},
        },
    )
    # masts: (name, x, lower height, topmast, topgallant, royal)
    masts = {
        "fore": (14.0, 22.0, 14.0, 8.0, 5.0),
        "main": (-2.0, 25.0, 15.5, 9.0, 5.5),
        "mizzen": (-16.0, 19.0, 12.0, 7.0, 4.0),
    }
    # square sails per mast: (level, yard len, area, brace limit)
    plans = {
        "fore": [
            ("course", 22.0, 290, 55),
            ("topsail", 17.0, 330, 58),
            ("topgallant", 12.0, 140, 60),
            ("royal", 8.0, 70, 62),
        ],
        "main": [
            ("course", 25.0, 370, 55),
            ("topsail", 19.0, 420, 58),
            ("topgallant", 13.0, 170, 60),
            ("royal", 9.0, 85, 62),
        ],
        "mizzen": [("topsail", 13.0, 200, 58), ("topgallant", 9.0, 90, 60), ("royal", 6.0, 45, 62)],
    }
    yards_by_level = {"course": [], "topsail": [], "topgallant": [], "royal": []}
    sails_by_level = {"course": [], "topsail": [], "topgallant": [], "royal": []}
    for m, (x, h_lower, h_top, h_tg, h_royal) in masts.items():
        lower = b.spar(f"{m}.mast", "mast", x_m=x, height_m=h_lower, rating_kn=500)
        top = b.spar(f"{m}.topmast", "topmast", steps_on=lower, height_m=h_top, rating_kn=150)
        tg = b.spar(
            f"{m}.topgallant_mast", "topgallant_mast", steps_on=top, height_m=h_tg, rating_kn=55
        )
        royal = b.spar(f"{m}.royal_mast", "royal_mast", steps_on=tg, height_m=h_royal, rating_kn=22)
        heights = {
            "course": (lower, h_lower * 0.85, h_lower * 0.45),
            "topsail": (top, h_lower + h_top * 0.9, h_lower + h_top * 0.45),
            "topgallant": (tg, h_lower + h_top + h_tg * 0.9, h_lower + h_top + h_tg * 0.45),
            "royal": (
                royal,
                h_lower + h_top + h_tg + h_royal * 0.9,
                h_lower + h_top + h_tg + h_royal * 0.4,
            ),
        }
        for level, ylen, area, limit in plans[m]:
            on, yard_h, sail_h = heights[level]
            yard_id = f"{m}.{level}.yard" if level != "course" else f"{m}.yard"
            if m == "mizzen" and level == "course":
                continue
            yard = b.spar(
                yard_id,
                "yard",
                on=on,
                length_m=ylen,
                height_m=round(yard_h, 1),
                brace_limit_deg=limit,
                rating_kn={"course": 120, "topsail": 90, "topgallant": 40, "royal": 18}[level],
            )
            sail_id = f"{m}.{level}" if level != "course" else f"{m}.course"
            reef = {"course": 1, "topsail": 3, "topgallant": 0, "royal": 0}[level]
            sail = b.sail(
                sail_id,
                "square",
                yard=yard,
                area_m2=area,
                reef_bands=reef,
                x_m=x,
                centre_height_m=round(sail_h + 2.0, 1),
            )
            square_sail_lines(
                b,
                sail,
                yard,
                hoisting=(level != "course"),
                course=(level == "course"),
                reef=(reef > 0),
            )
            yards_by_level[level].append(yard)
            sails_by_level[level].append(sail)
        b.sided(f"{m}.shrouds", "shroud", lower, rating=300)
        b.sided(f"{m}.topmast.backstay", "backstay", top, rating=150)
    # crossjack yard on the mizzen (no sail), for the mizzen topsail braces' sake
    b.spar(
        "mizzen.crossjack.yard",
        "yard",
        on="mizzen.mast",
        length_m=18.0,
        height_m=16.0,
        brace_limit_deg=55,
        rating_kn=80,
    )
    b.sided("mizzen.crossjack.yard.brace", "brace", "mizzen.crossjack.yard")
    # spanker
    gaff = b.spar(
        "mizzen.gaff", "gaff", on="mizzen.mast", length_m=11.0, height_m=15.0, rating_kn=60
    )
    boom = b.spar(
        "mizzen.boom", "boom", on="mizzen.mast", length_m=17.0, height_m=2.5, rating_kn=80
    )
    spanker = b.sail(
        "mizzen.spanker",
        "gaff",
        mast="mizzen.mast",
        gaff=gaff,
        boom=boom,
        area_m2=180,
        reef_bands=2,
        x_m=-20.0,
        centre_height_m=9.0,
    )
    b.line("mizzen.gaff.throat_halyard", "throat_halyard", gaff)
    b.line("mizzen.gaff.peak_halyard", "peak_halyard", gaff)
    b.line("mizzen.spanker.sheet", "sheet", spanker)
    b.line("mizzen.spanker.outhaul", "outhaul", spanker)
    b.sided("mizzen.gaff.vang", "vang", gaff)
    # head: bowsprit, jib-boom, flying jib-boom, stays and headsails
    bowsprit = b.spar("bowsprit", "bowsprit", x_m=22.0, length_m=16.0, height_m=6.0, rating_kn=300)
    jib_boom = b.spar(
        "jib_boom", "jib_boom", on=bowsprit, length_m=11.0, height_m=8.0, rating_kn=70
    )
    b.spar(
        "flying_jib_boom", "flying_jib_boom", on=jib_boom, length_m=7.0, height_m=9.0, rating_kn=30
    )
    b.line("fore.stay", "stay", "fore.mast", rating=250)
    b.line("fore.topmast.stay", "stay", "fore.topmast", rating=120)
    b.line("jib.stay", "stay", "fore.topgallant_mast", rating=60)
    b.line("flying_jib.stay", "stay", "fore.royal_mast", rating=30)
    b.line("main.stay", "stay", "main.mast", rating=300)
    b.line("main.topmast.stay", "stay", "main.topmast", rating=150)
    b.line("bobstay", "stay", bowsprit, rating=250)
    b.line("martingale", "stay", jib_boom, rating=80)
    headsails = []
    for sid, stay, area, x, h in (
        ("fore.topmast_staysail", "fore.topmast.stay", 70, 20.0, 12.0),
        ("jib", "jib.stay", 110, 27.0, 14.0),
        ("flying_jib", "flying_jib.stay", 60, 33.0, 17.0),
    ):
        s = b.sail(sid, "jibheaded", stay=stay, area_m2=area, x_m=x, centre_height_m=h)
        b.line(f"{sid}.halyard", "halyard", s)
        b.sided(f"{sid}.sheet", "sheet", s)
        b.line(f"{sid}.downhaul", "downhaul", s)
        headsails.append(s)
    mts = b.sail(
        "main.topmast_staysail",
        "jibheaded",
        stay="main.topmast.stay",
        area_m2=90,
        x_m=6.0,
        centre_height_m=20.0,
    )
    b.line("main.topmast_staysail.halyard", "halyard", mts)
    b.sided("main.topmast_staysail.sheet", "sheet", mts)
    b.line("main.topmast_staysail.downhaul", "downhaul", mts)
    # studding sails on fore and main: lower (fore only), topmast, topgallant
    stuns = []
    for m in ("fore", "main"):
        x = masts[m][0]
        for level, parent_yard, area, h in (
            ("lower", f"{m}.yard", 90, 9.0),
            ("topmast", f"{m}.topsail.yard", 85, 21.0),
            ("topgallant", f"{m}.topgallant.yard", 40, 31.0),
        ):
            if m == "main" and level == "lower":
                continue
            for side in SIDES:
                boom_id = b.spar(
                    f"{m}.{level}.studdingsail_boom.{side}",
                    "studdingsail_boom",
                    on=parent_yard,
                    side=side,
                    length_m={"lower": 12.0, "topmast": 9.0, "topgallant": 6.0}[level],
                    height_m=h - 3.0,
                    rating_kn=18,
                )
                sid = b.sail(
                    f"{m}.{level}.studdingsail.{side}",
                    "studding",
                    boom=boom_id,
                    yard=parent_yard,
                    side=side,
                    area_m2=area,
                    x_m=x,
                    centre_height_m=h,
                )
                b.line(f"{sid}.halyard", "halyard", sid)
                b.line(f"{sid}.tack", "tack", sid)
                b.line(f"{sid}.sheet", "sheet", sid)
                b.line(f"{sid}.downhaul", "downhaul", sid)
                stuns.append(sid)
    # groups
    b.group("courses", sails_by_level["course"])
    b.group("topsails", sails_by_level["topsail"])
    b.group("topgallants", sails_by_level["topgallant"])
    b.group("royals", sails_by_level["royal"])
    b.group("headsails", headsails)
    b.group("staysails", headsails[:1] + [mts])
    b.group("studdingsails", stuns)
    b.group("square sails", sum(sails_by_level.values(), []))
    b.group("fore-and-aft sails", headsails + [mts, spanker])
    b.group(
        "plain sail",
        sails_by_level["course"]
        + sails_by_level["topsail"]
        + sails_by_level["topgallant"]
        + headsails[:2]
        + [spanker],
    )
    b.group("all sail", sum(sails_by_level.values(), []) + headsails + [mts, spanker] + stuns)
    for m in masts:
        b.group(
            f"{m} yards",
            [y for lvl in yards_by_level for y in yards_by_level[lvl] if y.startswith(m + ".")]
            + (["mizzen.crossjack.yard"] if m == "mizzen" else []),
        )
    b.group(
        "yards",
        [y for lvl in yards_by_level for y in yards_by_level[lvl]] + ["mizzen.crossjack.yard"],
    )
    b.group(
        "head yards",
        [
            y
            for y in yards_by_level["course"]
            + yards_by_level["topsail"]
            + yards_by_level["topgallant"]
            + yards_by_level["royal"]
            if y.startswith("fore.")
        ],
    )
    b.group(
        "after yards",
        [y for lvl in yards_by_level for y in yards_by_level[lvl] if not y.startswith("fore.")]
        + ["mizzen.crossjack.yard"],
    )
    b.group(
        "topgallant masts",
        ["fore.topgallant_mast", "main.topgallant_mast", "mizzen.topgallant_mast"],
    )
    # aliases
    b.alias("spanker", "mizzen.spanker")
    b.alias("driver", "mizzen.spanker")
    b.alias("mizzen", "mizzen.spanker")
    b.alias("foresail", "fore.course")
    b.alias("mainsail", "main.course")
    b.alias("fore yard", "fore.yard")
    b.alias("main yard", "main.yard")
    b.alias("crossjack yard", "mizzen.crossjack.yard")
    b.alias("cro'jack yard", "mizzen.crossjack.yard")
    b.alias("fore topmast staysail", "fore.topmast_staysail")
    b.alias("main topmast staysail", "main.topmast_staysail")
    b.alias("stuns'ls", "studdingsails")
    b.alias("studding sails", "studdingsails")
    b.alias("kites", "studdingsails")
    for m in ("fore", "main"):
        for level in ("lower", "topmast", "topgallant"):
            if m == "main" and level == "lower":
                continue
            b.group(f"{m} {level} studdingsails", [f"{m}.{level}.studdingsail.{s}" for s in SIDES])
    b.dump(
        "data/ships/frigate-36.yaml",
        "# Draft reference ship: a 36-gun frigate, ship-rigged. Generated for M1; WP8 verifies\n"
        "# particulars against the references in docs/references/. Units: metres, m2, kg, kN.\n",
    )


def schooner():
    b = Builder(
        "Speedwell",
        "topsail-schooner",
        "Draft particulars for a Baltimore-built topsail schooner of about 1804. "
        "Dimensions and sail areas are approximate and to be checked (WP8).",
        {
            "length_waterline_m": 27.5,
            "beam_m": 7.3,
            "draught_m": 3.2,
            "displacement_kg": 190000,
            "gm_m": 1.0,
            "clr_x_m": -0.4,
            "lateral_area_m2": 75,
            "hull_speed_kn": 10.5,
            "deck_height_m": 1.2,
            "rudder": {"area_m2": 2.2, "max_angle_deg": 35, "rate_deg_s": 4.0},
        },
    )
    fore = b.spar("fore.mast", "mast", x_m=7.5, height_m=17.0, rating_kn=220)
    fore_top = b.spar("fore.topmast", "topmast", steps_on=fore, height_m=9.0, rating_kn=60)
    fore_tg = b.spar(
        "fore.topgallant_mast", "topgallant_mast", steps_on=fore_top, height_m=5.0, rating_kn=25
    )
    main = b.spar("main.mast", "mast", x_m=-3.0, height_m=19.0, rating_kn=240)
    main_top = b.spar("main.topmast", "topmast", steps_on=main, height_m=10.0, rating_kn=60)
    # square sails on the fore
    ty = b.spar(
        "fore.topsail.yard",
        "yard",
        on=fore_top,
        length_m=11.0,
        height_m=19.5,
        brace_limit_deg=58,
        rating_kn=45,
    )
    ts = b.sail(
        "fore.topsail", "square", yard=ty, area_m2=62, reef_bands=2, x_m=7.5, centre_height_m=16.0
    )
    square_sail_lines(b, ts, ty, hoisting=True, reef=True)
    tgy = b.spar(
        "fore.topgallant.yard",
        "yard",
        on=fore_tg,
        length_m=8.0,
        height_m=24.5,
        brace_limit_deg=60,
        rating_kn=22,
    )
    tgs = b.sail("fore.topgallant", "square", yard=tgy, area_m2=32, x_m=7.5, centre_height_m=23.0)
    square_sail_lines(b, tgs, tgy, hoisting=True)
    # gaff sails
    fgaff = b.spar("fore.gaff", "gaff", on=fore, length_m=7.0, height_m=15.0, rating_kn=45)
    foresail = b.sail(
        "fore.sail",
        "gaff",
        mast=fore,
        gaff=fgaff,
        area_m2=95,
        reef_bands=2,
        x_m=3.5,
        centre_height_m=8.0,
    )
    b.line("fore.gaff.throat_halyard", "throat_halyard", fgaff)
    b.line("fore.gaff.peak_halyard", "peak_halyard", fgaff)
    b.sided("fore.sail.sheet", "sheet", foresail)  # loose-footed, overlapping
    b.line("fore.sail.tack", "tack", foresail)
    mgaff = b.spar("main.gaff", "gaff", on=main, length_m=9.0, height_m=17.0, rating_kn=50)
    mboom = b.spar("main.boom", "boom", on=main, length_m=13.0, height_m=2.0, rating_kn=60)
    mainsail = b.sail(
        "main.sail",
        "gaff",
        mast=main,
        gaff=mgaff,
        boom=mboom,
        area_m2=150,
        reef_bands=3,
        x_m=-8.0,
        centre_height_m=9.0,
    )
    b.line("main.gaff.throat_halyard", "throat_halyard", mgaff)
    b.line("main.gaff.peak_halyard", "peak_halyard", mgaff)
    b.line("main.sail.sheet", "sheet", mainsail)
    b.line("main.sail.outhaul", "outhaul", mainsail)
    b.sided("main.gaff.vang", "vang", mgaff)
    gt = b.sail(
        "main.gaff_topsail", "jibheaded", mast=main_top, area_m2=35, x_m=-6.0, centre_height_m=22.0
    )
    b.line("main.gaff_topsail.halyard", "halyard", gt)
    b.line("main.gaff_topsail.sheet", "sheet", gt)
    b.line("main.gaff_topsail.tack", "tack", gt)
    # head
    bowsprit = b.spar("bowsprit", "bowsprit", x_m=14.0, length_m=9.0, height_m=3.0, rating_kn=150)
    jib_boom = b.spar("jib_boom", "jib_boom", on=bowsprit, length_m=6.0, height_m=4.0, rating_kn=40)
    b.line("fore.stay", "stay", fore, rating=150)
    b.line("fore.topmast.stay", "stay", fore_top, rating=70)
    b.line("jib.stay", "stay", fore_top, rating=60)
    b.line("flying_jib.stay", "stay", fore_tg, rating=25)
    b.line("main.topmast.stay", "stay", main_top, rating=70)
    b.line("bobstay", "stay", bowsprit, rating=120)
    b.line("martingale", "stay", jib_boom, rating=40)
    b.sided("fore.shrouds", "shroud", fore, rating=150)
    b.sided("main.shrouds", "shroud", main, rating=150)
    b.sided("fore.topmast.backstay", "backstay", fore_top, rating=60)
    b.sided("main.topmast.backstay", "backstay", main_top, rating=60)
    heads = []
    for sid, stay, area, x, h in (
        ("fore.staysail", "fore.stay", 40, 12.0, 6.5),
        ("jib", "jib.stay", 55, 17.0, 8.0),
        ("flying_jib", "flying_jib.stay", 30, 21.0, 10.0),
    ):
        s = b.sail(sid, "jibheaded", stay=stay, area_m2=area, x_m=x, centre_height_m=h)
        b.line(f"{sid}.halyard", "halyard", s)
        b.sided(f"{sid}.sheet", "sheet", s)
        b.line(f"{sid}.downhaul", "downhaul", s)
        heads.append(s)
    # a fore topmast studding sail each side, for the stuns'l evolutions on this rig
    stuns = []
    for side in SIDES:
        boom = b.spar(
            f"fore.topmast.studdingsail_boom.{side}",
            "studdingsail_boom",
            on=ty,
            side=side,
            length_m=6.0,
            height_m=16.0,
            rating_kn=12,
        )
        s = b.sail(
            f"fore.topmast.studdingsail.{side}",
            "studding",
            boom=boom,
            yard=ty,
            side=side,
            area_m2=28,
            x_m=7.5,
            centre_height_m=17.0,
        )
        for cls in ("halyard", "tack", "sheet", "downhaul"):
            b.line(f"{s}.{cls}", cls, s)
        stuns.append(s)
    b.group("topsails", [ts])
    b.group("topgallants", [tgs])
    b.group("square sails", [ts, tgs])
    b.group("headsails", heads)
    b.group("fore-and-aft sails", heads + [foresail, mainsail, gt])
    b.group("studdingsails", stuns)
    b.group("fore topmast studdingsails", stuns)
    b.group("plain sail", [foresail, mainsail, ts, tgs, heads[0], heads[1]])
    b.group("all sail", [foresail, mainsail, gt, ts, tgs] + heads + stuns)
    b.group("yards", [ty, tgy])
    b.group("fore yards", [ty, tgy])
    b.alias("foresail", "fore.sail")
    b.alias("the fore", "fore.sail")
    b.alias("mainsail", "main.sail")
    b.alias("the main", "main.sail")
    b.alias("gaff topsail", "main.gaff_topsail")
    b.alias("main gaff topsail", "main.gaff_topsail")
    b.alias("fore staysail", "fore.staysail")
    b.alias("stuns'ls", "studdingsails")
    b.alias("studding sails", "studdingsails")
    b.dump(
        "data/ships/topsail-schooner.yaml",
        "# Draft reference ship: a Baltimore topsail schooner. Generated for M1; WP8 verifies\n"
        "# particulars against the references in docs/references/. Units: metres, m2, kg, kN.\n",
    )


if __name__ == "__main__":
    import os

    os.makedirs("data/ships", exist_ok=True)
    frigate()
    schooner()
    print("written", file=sys.stderr)
