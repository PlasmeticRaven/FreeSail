"""Package 75, the second ship (B2): the Prince de Neufchatel, the American privateer
hermaphrodite brig of 1812-1814.

Her design is docs/design/Design-Ship-PrinceDeNeufchatel.md (Neuf-D), from the research note
docs/design/Research-PrinceDeNeufchatel-2026-10.md (Neuf); `tools/ships/neufchatel.py` writes
her file, `data/ships/hermaphrodite-brig.yaml`. These are her tests (Neuf-D §14; Build-Ships.md
§14.1), in the band form of tests/test_ship_particulars.py with the source of each band in a
comment. Begun with her road's steps 1 to 3 (Neuf-D §13): her hull block against ZAZ6177 and
Winfield; her profile's points, sills and half-breadths against Neuf-D §3.2-§3.3, eleven port
triples a side, her stern raked and her head a knee, a mark on every shape line; her spars
against ZAZ6179 and Fincham where taken; her sails against ZAZ6179's areas; her main topgallant
on its two light yards a schooner's mast's (the lead's ruling of 2026-11-06 on Neuf-D §12.2a,
no key) and her golden row through the golden table's gates; every group the engine reads by
name, and the main topgallant within reach of "make all sail" and "shorten sail"; her sources'
words for her sails; the generator's report and her file as committed. Her road's steps 4 and 6:
her fit, guns, crews and magazine against Winfield, Adye, Douglas and Falconer, and the builder's
checklist for the viewer (Build-Ships.md §6's postscript); her broadside by 70's rule; her
company, posts, marines and people file against Niles and Cobb; the beat to quarters on her fit,
measured; her ground tackle against Steel's row, her boats, pumps, hold and stores; her
description in her file and through the index; her round trip at seed 7 with no fit named; her
line of the lee ports' truth (7-190), measured; and truth 7-192 with its index clause. Her road's
step 5 (Neuf-D §9, §12.2 item 8, §14): her polar in tests/test_ships.py's form and truth 7-193, her
best point; her helm as tuned (`clr_x_m`, truth 6's form); her light main yards' short swing at
"Main-topsail haul."; her tack, wear and heave-to beside trial A's, her main topgallant set hove
to; getting under way; "shorten sail" taking in her main topgallant; her gale's course reefs; and
truth 9's two forms on her file.

The figures quoted as measured were measured on the owner's machine (Windows 11, 2026-11-07);
the bands are the sources' or judgement where they say so.
"""

from __future__ import annotations

import copy
import math
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

from freesail import units
from freesail.api import viewer_guns
from freesail.api.readings import ship_class_words
from freesail.combat.far import far_ship
from freesail.evolutions import scripts
from freesail.evolutions import trim as yard_trim
from freesail.orders.resolve import noun_table
from freesail.orders.vocabulary import load_vocabulary
from freesail.physics.sails import _square_rigged
from freesail.ship.loader import load_ship, load_spec
from freesail.ship.parts import SailState
from freesail.ship.profile import ports_of
from freesail.world import brains
from freesail.world import captains as C
from freesail.world import ships as S
from freesail.world.ships import polar_of

ROOT = Path(__file__).resolve().parents[1]
HER = "data/ships/hermaphrodite-brig.yaml"
FT = units.FOOT
SQ_FT = FT * FT
CWT_KG = 50.80234544  # the hundredweight of 112 lb
# her datum, her flush deck at side at mid-length, 3.8 ft above her line (Neuf §2.7)
DATUM_M = 1.16


@pytest.fixture(scope="module")
def her():
    return load_ship(HER)


def above_water(ship, spar_id):
    """A spar's height above her water: the file's height above the datum and the datum."""
    return ship.spars[spar_id].height_m + ship.hull.spec.deck_height_m


def text_of(path):
    return (ROOT / path).read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Her hull (Neuf-D §2.1)
# ---------------------------------------------------------------------------


def test_her_hull_holds_her_lines_and_winfield(her):
    hull = her.hull.spec
    assert her.spec.rig == "hermaphrodite brig"
    # 107.3 ft between the rabbets at her sailing-trim line (ZAZ6177, measured +-0.5 ft: Neuf §2.4)
    assert hull.length_waterline_m == pytest.approx(107.3 * FT, abs=0.2)
    # 25 ft 8 in extreme (Winfield 1793-1817 pp. 335-336)
    assert hull.beam_m == pytest.approx((25.0 + 8.0 / 12.0) * FT, abs=0.05)
    # 10 ft 4 1/2 in mean to the false keel at the sailing-trim line (ZAZ6177, measured +-0.25 ft)
    assert hull.draught_m == pytest.approx(10.36 * FT, abs=0.08)
    # 288 t at her sailing trim (measured, +-10 t: Neuf §2.5)
    assert hull.displacement_kg == pytest.approx(288000.0, abs=10000.0)
    # 1,100 sq ft to the false keel's bottom (measured, +-5%: Neuf §2.6)
    assert hull.lateral_area_m2 == pytest.approx(102.0, abs=5.0)
    # GM within D23 (a)'s 2.0-2.2 (judgement); hull speed within Neuf-D §9's 12.5-13.9 (judgement)
    assert 2.0 <= hull.gm_m <= 2.2
    assert 12.5 <= hull.hull_speed_kn <= 13.9
    # her flush deck at side at mid-length, 3.8 ft above her line (measured +-0.3 ft: Neuf §2.7)
    assert hull.deck_height_m == pytest.approx(3.8 * FT, abs=0.09)
    # the rudder's blade below her line, 28.1 sq ft on a span of 11.7 ft (measured: Neuf §2.6)
    assert hull.rudder.area_m2 == pytest.approx(28.1 * SQ_FT, abs=0.3)
    assert hull.rudder.span_m == pytest.approx(11.7 * FT, abs=0.1)


def test_winfields_tonnage_holds_by_the_navys_rule():
    """Neuf-D §1.5: the Navy's rule on Winfield's keel for tonnage and extreme breadth (93 ft
    8 1/4 in and 25 ft 8 in) within a ton of his 328 22/94 (pp. 335-336)."""
    keel, beam = 93.0 + 8.25 / 12.0, 25.0 + 8.0 / 12.0
    assert keel * beam * beam / 2.0 / 94.0 == pytest.approx(328.0 + 22.0 / 94.0, abs=1.0)


# ---------------------------------------------------------------------------
# Her profile and shape (Neuf-D §3)
# ---------------------------------------------------------------------------

# Neuf-D §3.2's rail, file frame (measured on ZAZ6177, +-0.3 ft; the taffrail first)
RAIL_M = [
    (-17.96, 2.88),
    (-16.41, 2.56),
    (-12.97, 2.49),
    (-10.81, 2.42),
    (-8.64, 2.40),
    (-6.48, 2.29),
    (-3.46, 2.29),
    (-0.69, 2.36),
    (2.61, 2.37),
    (6.05, 2.34),
    (8.21, 2.40),
    (10.84, 2.57),
    (12.97, 2.72),
    (14.92, 2.77),
    (16.05, 2.78),
]
# Neuf-D §3.3's eleven ports, from forward: x (m), sill (ft, measured +-0.3 ft), half-breadth (m,
# the top breadth at the station with 2 in of plank: judgement until task 3)
PORTS = [
    (14.39, 6.68, 2.03),
    (11.58, 5.97, 3.07),
    (8.72, 5.20, 3.64),
    (6.00, 5.20, 3.81),
    (3.05, 5.06, 3.87),
    (0.12, 4.92, 3.83),
    (-2.74, 4.94, 3.69),
    (-5.64, 4.94, 3.53),
    (-8.56, 5.09, 3.35),
    (-11.37, 5.39, 3.02),
    (-14.23, 5.84, 2.72),
]


def test_her_profile_is_her_measured_lines(her):
    profile = her.hull.spec.profile
    assert [tuple(p) for p in profile.rail_m] == RAIL_M
    triples = dict(profile.ports_m)["upper"]
    assert len(triples) == 11
    xs = [t[0] for t in triples]
    assert xs == sorted(xs)
    for (x, sill, hb), (px, psill, phb) in zip(sorted(PORTS), triples, strict=True):
        assert px == pytest.approx(x, abs=0.005)
        assert psill == pytest.approx(sill * FT, abs=0.006)
        assert phb == pytest.approx(hb, abs=0.005)
    # her lowest sill, amidships, 4 ft 11 in (1.50 m): measured for the design and confirmed by
    # task 1's checker on both sheets of her lines within 0.05 ft, so the band tightened to
    # +-0.03 m (Neuf-D §14, 7-192's clause)
    assert min(t[1] for t in triples) == pytest.approx(1.50, abs=0.03)
    # the port's size, the eleven's mean (measured: 2 ft 8 in by 2.48 ft)
    assert list(dict(profile.port_size_m)["upper"]) == pytest.approx([0.81, 0.76], abs=0.005)
    # every point below her rail: her deck and her sills
    for deck, line in profile.decks_m:
        assert deck == "upper"
        assert len(line) == 13


def test_her_stern_is_raked_and_her_head_a_knee(her):
    """Neuf-D §3.5: a flat transom raking from its foot, 4.65 ft above her water just abaft the
    post's head, to the taffrail, 9.46 ft above her water and 5.26 ft abaft the after rabbet, with
    no counter (measured on ZAZ6177; re-traced by task 1's checker within 0.2 ft at both ends on
    ZAZ6177 and ZAZ6178); 16.1 ft across its top corners and 16.6 ft at its knuckle, so that it
    tumbles home above the knuckle as every transom does; her head a knee, its terminal unread.
    The knuckle's breadth is the re-reading at the knuckle's height, taken by the lead's ruling of
    2026-11-07 (package 75, B2b): the sides near plumb, 16.6-16.8 ft across from 4.0 to 7.0 ft above
    her water. Old beside new: 15.8 ft, read at 3.2-3.9 ft below the knuckle, `transom_hb_m`
    [2.46, 2.41] to [2.46, 2.53]."""
    profile = her.hull.spec.profile
    form = profile.form
    assert form.stern.type == "raked"
    assert form.head == "knee"
    assert form.stern.knuckle_z_m == pytest.approx(4.65 * FT, abs=0.02)
    assert list(form.stern.transom_hb_m) == pytest.approx(
        [16.1 * FT / 2.0, 16.6 * FT / 2.0], abs=0.02
    )
    assert form.stern.transom_hb_m[0] < form.stern.transom_hb_m[1]  # tumbling home
    taffrail = profile.stern_m[-1]
    assert taffrail[1] == pytest.approx(9.46 * FT, abs=0.02)
    rake = math.degrees(
        math.atan2(profile.stern_m[-2][0] - taffrail[0], taffrail[1] - profile.stern_m[-2][1])
    )
    assert 28.0 <= rake <= 35.0  # 31 deg (the design's chord); 33-34 by the checker's re-trace


SHAPE_LINES = (
    "rail_m",
    "breadth_m",
    "keel_m",
    "stem_m",
    "stern_m",
    "section_m",
    "decks_m",
    "ports_m",
    "port_size_m",
    "head_m",
    "sections_m",
    "rabbet_m",
)


def test_every_line_of_her_shape_carries_its_rung():
    """Build-Ships.md §5.0 principle 4: each line her profile gives has its word, the word of its
    weakest point (Neuf-D §3.5's table): the keel and the stem judged at the gripe's foot, the
    ports and the breadth at the top breadth taken for their half-breadths; each key of her stern
    but its type marked too (tests/test_profiles.py's check, which her file first met at step
    4)."""
    profile = yaml.safe_load(text_of(HER))["hull"]["profile"]
    marks = profile["marks"]
    for line in SHAPE_LINES:
        assert line in profile and line in marks, line
    for key in profile["form"]["stern"]:
        if key != "type":
            assert marks[f"form.stern.{key}"] == "sourced", key
    assert {k for k, v in marks.items() if v == "judged"} == {
        "breadth_m",
        "keel_m",
        "stem_m",
        "ports_m",
        "form.fullness",
        "form.head",
    }
    assert marks["form.stern"] == "sourced"
    assert set(marks.values()) <= {"sourced", "judged"}


# ---------------------------------------------------------------------------
# Her spars (ZAZ6179, measured, the yards doubled; Fincham 1843 p. 78 where taken: Neuf-D §4.1-§4.2)
# ---------------------------------------------------------------------------

# above her water, ft (ZAZ6179, measured: Neuf §3.3), the band the sheet's reading (yards +-1.5
# ft doubled in length, every height +-0.5 ft; masts +-1 ft)
YARDS_FT = {
    "fore.yard": (65.0, 47.2),
    "fore.topsail.yard": (46.8, 78.5),
    "fore.topgallant.yard": (26.0, 97.7),
    "fore.royal.yard": (24.5, 108.1),
    "main.topsail.yard": (34.7, 95.7),
    "main.topgallant.yard": (24.3, 107.5),
}
# Fincham 1843 p. 78's first example, ft (read), within 2 ft of hers where both exist (Neuf-D §1.5)
FINCHAM_YARDS_FT = {
    "fore.yard": 63.25,
    "fore.topsail.yard": 46.52,
    "fore.topgallant.yard": 26.67,
    "main.topsail.yard": 36.3,
    "main.topgallant.yard": 23.22,
}


def test_her_masts_stand_as_her_sheets_draw_them(her):
    spars = {s.id: s for s in load_spec(HER).spars}
    fore, main = spars["fore.mast"], spars["main.mast"]
    # 43.7 ft apart at the deck (Neuf §2.7: 43.6-43.9; ZAZ6179 43.9), independent of the join
    assert (fore.x_m - main.x_m) == pytest.approx(13.3, abs=0.3)
    # raking 12.4 and 10.3 deg with her water level (ZAZ6179, measured +-0.7 deg)
    assert main.rake_deg == pytest.approx(12.4, abs=0.7)
    assert fore.rake_deg == pytest.approx(10.3, abs=0.7)
    # the lower caps 61.3 ft (by length and rake) and 79.6 ft (read) above her water
    assert above_water(her, "fore.mast") == pytest.approx(61.3 * FT, abs=1.0 * FT)
    assert above_water(her, "main.mast") == pytest.approx(79.6 * FT, abs=1.0 * FT)
    # the trucks 110.4 and 110.1 ft above her water (measured, +-1 ft)
    for top, truck in (
        (["fore.mast", "fore.topmast", "fore.topgallant_mast", "fore.royal_mast"], 110.4),
        (["main.mast", "main.topmast", "main.topgallant_mast"], 110.1),
    ):
        stacked = DATUM_M + sum(her.spars[s].height_m for s in top)
        assert stacked == pytest.approx(truck * FT, abs=1.0 * FT)
    # the main a schooner's pole mast: crosstrees and no top, its topmast and pole one stick
    assert her.spars["main.topgallant_mast"].parent == "main.topmast"
    assert "fore.royal_mast" in her.spars and "main.royal_mast" not in her.spars


def test_her_yards_gaffs_and_boom_are_her_sail_plans(her):
    for yid, (length_ft, h_ft) in YARDS_FT.items():
        y = her.spars[yid]
        assert y.length_m == pytest.approx(length_ft * FT, abs=1.5 * FT), yid
        assert above_water(her, yid) == pytest.approx(h_ft * FT, abs=0.5 * FT), yid
        if yid in FINCHAM_YARDS_FT:
            assert abs(y.length_m / FT - FINCHAM_YARDS_FT[yid]) <= 2.0, yid
    # the gaffs 32.9 and 37.3 ft, their jaws 46.9 and 64.4 ft above her water; the boom 64.2 ft,
    # 10.4 ft above her water at the mast (ZAZ6179, measured +-0.7 ft); the boom 19.6 +-0.3 m and
    # the fore yard 19.8 +-0.5 m (7-192's clauses, Neuf-D §14)
    for gid, length_ft, jaws_ft in (("fore.gaff", 32.9, 46.9), ("main.gaff", 37.3, 64.4)):
        assert her.spars[gid].length_m == pytest.approx(length_ft * FT, abs=0.7 * FT)
        assert above_water(her, gid) == pytest.approx(jaws_ft * FT, abs=0.7 * FT)
    assert her.spars["main.boom"].length_m == pytest.approx(19.6, abs=0.3)
    assert above_water(her, "main.boom") == pytest.approx(10.4 * FT, abs=0.7 * FT)
    assert her.spars["fore.yard"].length_m == pytest.approx(19.8, abs=0.5)
    # the head (Neuf §1.2): the bowsprit 22.4 ft outboard of the stem; the jibboom's and the
    # flying jibboom's ends 22.8 and 25.5 ft above her water (ZAZ6179, measured by the checker)
    assert her.spars["bowsprit"].length_m == pytest.approx(22.4 * FT, abs=1.0 * FT)
    assert above_water(her, "jib_boom") == pytest.approx(22.8 * FT, abs=0.5 * FT)
    assert above_water(her, "flying_jib_boom") == pytest.approx(25.5 * FT, abs=0.5 * FT)
    # every spar rated by the pass from what the engine's graph hangs on it
    for sid, spar in her.spars.items():
        assert spar.rating_kn > 0.0, sid


# ---------------------------------------------------------------------------
# Her sails (ZAZ6179, measured from the corners, +-10-15%: Neuf §3.3; Neuf-D §4.3-§4.7)
# ---------------------------------------------------------------------------

# sq ft as drawn (Neuf §3.3; the flying jib, the main staysail and the main topmast staysail on
# its upper foot read by task 5's checker, the tuning notes)
SAILS_SQFT = {
    "main.sail": 2780,
    "fore.course": 2000,
    "fore.topsail": 1700,
    "fore.sail": 1660,
    "fore.topgallant": 580,
    "main.staysail": 530,
    "main.gaff_topsail": 470,
    "main.topgallant": 300,
    "fore.royal": 250,
    "fore.lower.studdingsail.starboard": 665,
    "flying_jib": 447,
    "main.topmast_staysail": 398,
}


def test_her_sails_are_cut_within_fifteen_percent_of_her_sail_plan(her):
    for sid, sqft in SAILS_SQFT.items():
        assert her.sails[sid].area_m2 == pytest.approx(sqft * SQ_FT, rel=0.15), sid
    # the fore gaff sail: loose-footed, its clew 2.7-2.9 ft abaft the mainmast's line at 12.6 ft
    # above her water (Neuf §1.2, measured; Neuf-D §14: 0.8-0.9 m, +-0.3)
    fg = her.sails["fore.sail"]
    assert "boom" not in fg.roles
    tack, throat, peak, clew = fg.corners_m
    main = {s.id: s for s in load_spec(HER).spars}["main.mast"]
    clew_z = clew[1] + DATUM_M
    mast_x = main.x_m - math.tan(math.radians(main.rake_deg)) * (clew_z - DATUM_M)
    assert mast_x - clew[0] == pytest.approx(0.85, abs=0.3)
    assert clew_z == pytest.approx(12.6 * FT, abs=0.05)
    # its jaws just below the fore yard, its peak 61.7 ft above her water (measured)
    assert peak[1] + DATUM_M == pytest.approx(61.7 * FT, abs=0.7 * FT)
    # the mainsail's corners its spars': luff 55 and leech 65 ft (Neuf §3.3, re-measured)
    t, th, pk, cl = her.sails["main.sail"].corners_m
    assert math.dist(t, th) == pytest.approx(55.0 * FT, abs=1.0 * FT)
    assert math.dist(pk, cl) == pytest.approx(65.0 * FT, abs=1.0 * FT)


def test_her_plain_sail_is_the_brigs_and_the_schooners_together(her):
    """Neuf-D decision 14 (the owner, 2026-10-29: "Reasonable to start"): the fore course,
    topsail and topgallant, the fore gaff sail, the mainsail, the fore staysail and the jib; the
    main topgallant, the main staysail and the gaff topsail never in it."""
    plain = her.groups["plain sail"]
    assert plain == [
        "fore.course",
        "fore.topsail",
        "fore.topgallant",
        "fore.sail",
        "main.sail",
        "fore.staysail",
        "jib",
    ]
    for sid in ("main.topgallant", "main.staysail", "main.gaff_topsail", "fore.royal"):
        assert sid not in plain
    # the reefs (Neuf-D §4.3; Cobb p. 95)
    reefs = {sid: her.sails[sid].reef_bands for sid in her.sails}
    assert reefs["fore.course"] == 2 and reefs["fore.sail"] == 2
    assert reefs["fore.topsail"] == 3 and reefs["main.sail"] == 3
    assert reefs["jib"] == 0 and reefs["main.topgallant"] == 0
    assert her.sails["fore.royal"].flying


def test_her_light_sails_and_storm_canvas_are_the_owners_choice(her):
    """D35 (b) limited (Neuf-D §4.7): the fore's lower, topmast and topgallant studding sails a
    pair each, none on the main; the main topmast staysail on its upper foot; no ringtail, no water
    sail, no middle or main topgallant staysail; the storm canvas in the sail room (§4.8)."""
    stuns = her.groups["studdingsails"]
    assert sorted(stuns) == sorted(
        f"fore.{level}.studdingsail.{side}"
        for level in ("lower", "topmast", "topgallant")
        for side in ("starboard", "larboard")
    )
    for sid in ("ringtail", "water_sail", "middle_staysail", "main.topgallant_staysail"):
        assert sid not in her.sails
    mts = her.sails["main.topmast_staysail"]
    assert min(z for _x, z in mts.corners_m) + DATUM_M == pytest.approx(72.9 * FT, abs=0.05)
    for sid in her.groups["storm canvas"]:
        assert her.sails[sid].state is SailState.UNBENT, sid
    assert her.groups["storm staysails"] == ["fore.storm_staysail"]
    assert her.sails["storm_trysail"].in_place_of == "main.sail"
    assert her.sails["storm_jib"].in_place_of == "jib"


def test_every_sail_has_its_chain_and_every_square_its_braces_and_sheets(her):
    """tests/test_ship_loader.py's checks on the reference ships, on hers."""
    for sail in her.sails.values():
        chain = her.spar_chain(sail)
        assert chain and chain[-1].parent is None, sail.id
        if sail.cls == "square":
            assert len(her.braces_of(her.yard_of(sail))) == 2, sail.id
            assert len(her.sheets_of(sail)) == 2, sail.id
        if sail.cls == "studding":
            assert sail.side in ("starboard", "larboard")
            assert her.spar_of_role(sail, "boom").side == sail.side
    # the main's lower light yard carries no sail and has its braces and lifts a yard's
    lower = her.spars["main.topsail.yard"]
    assert not [s for s in her.sails.values() if s.roles.get("yard") == lower.id]
    assert len(her.braces_of(lower)) == 2


# ---------------------------------------------------------------------------
# Her main topgallant and her classing (Neuf-D §4.5, §12.2; the lead's ruling of 2026-11-06)
# ---------------------------------------------------------------------------


def test_her_main_topgallant_stands_on_a_schooners_mast(her):
    """Two light yards on the main topmast and its pole, the square sail between them, no key:
    the engine's rule reads the two yards and the sail as a schooner's mast's, and nothing on
    the fore (B3.4; Neuf-D §12.2a)."""
    named = [pid for pid in her.parts if her.on_schooner_mast(pid)]
    assert named == ["main.topsail.yard", "main.topgallant.yard", "main.topgallant"]
    assert her.spars["main.topsail.yard"].parent == "main.topmast"
    assert her.spars["main.topgallant.yard"].parent == "main.topgallant_mast"
    assert her.sails["main.topgallant"].roles["yard"] == "main.topgallant.yard"
    assert "schooner_mast" not in text_of(HER)


def test_her_classing_is_a_fore_and_after_with_four_fore_yards(her):
    """Her golden row (Neuf-D §12.2, as B3.4 built the rule), read through the golden table's
    gates (tests/test_rig_classing.py) with her plain sail set: the fore her one mast with yards;
    her head yards the four fore yards, her after yards the main's two light yards; the fore laid
    aback to heave to; not square-rigged; no driver; her mainsail the boom sail she gets under way
    under (Cobb p. 38: "her mainmast was rigged as a schooner")."""
    for sid in her.groups["plain sail"]:
        her.sails[sid].state = SailState.SET
    fore = ["fore.yard", "fore.topsail.yard", "fore.topgallant.yard", "fore.royal.yard"]
    assert [m.id for m in scripts._masts_with_yards(her)] == ["fore.mast"]
    head, after = scripts.head_and_after_yards(her)
    assert [y.id for y in head] == fore
    assert [y.id for y in after] == ["main.topsail.yard", "main.topgallant.yard"]
    back = scripts.yards_to_back(her)
    assert [y.id for y in back] == fore
    assert her.mast_of(back[0]).id == "fore.mast"
    assert [y.id for y in scripts.yards_to_back_set(her)] == fore
    assert _square_rigged(her) is False
    assert scripts.after_gaff_sails(her) == []
    assert [s.id for s in scripts._boom_mainsails(her)] == ["main.sail", "storm_trysail"]
    assert [s.id for s in scripts.boom_sails(her)] == ["main.sail"]
    assert scripts.dipping_lugs(her) == []
    targets = {y.id: y.brace_limit for y in scripts.working_yards(her)}
    assert sorted(targets) == sorted(fore + ["main.topsail.yard", "main.topgallant.yard"])
    _, stagger = yard_trim.stagger(her, targets)
    assert stagger == pytest.approx(-2.0, abs=0.05)


# ---------------------------------------------------------------------------
# Her groups and words (Neuf-D §4.8)
# ---------------------------------------------------------------------------

# the groups the engine reads by name (a grep of freesail/ for `groups.get("...")` and
# `groups["..."]`: orders/storm.py, evolutions/scripts.py, world/captains.py, world/ships.py)
READ_BY_NAME = (
    "plain sail",
    "courses",
    "topsails",
    "headsails",
    "jibs",
    "gaff sails",
    "staysails",
    "storm canvas",
    "storm staysails",
    "lying-to staysails",
)


def test_every_group_the_engine_reads_by_name_is_hers(her):
    for name in READ_BY_NAME:
        assert her.groups.get(name), name
    assert her.groups["courses"] == ["fore.course"]
    assert her.groups["gaff sails"] == ["fore.sail", "main.sail"]
    assert her.groups["lying-to staysails"] == ["main.staysail"]
    assert her.groups["after yards"] == ["main.topsail.yard", "main.topgallant.yard"]


def test_make_all_sail_and_shorten_sail_reach_her_main_topgallant(her):
    """B3.4's finding (the lead's notes of 2026-11-06): "shorten sail" never took in her main
    topgallant, her design's groups keeping it out of every group the list reaches. It is in her
    "royals" with the fore royal, which "make all sail" sets and "shorten sail" takes in, and in
    no group plain sail, the topgallants, the topsails or the courses name."""
    vocab = load_vocabulary()
    table = noun_table(her)
    for verb, phrase in (
        ("make all sail", "set the royals"),
        ("shorten sail", "take in the royals"),
    ):
        assert phrase in vocab.group_evolutions[verb]
    assert table.lookup("royals").ids == ["fore.royal", "main.topgallant"]
    for group in ("plain sail", "topgallants", "topsails", "courses"):
        assert "main.topgallant" not in her.groups[group], group


# her sources' words (Neuf-D §4.8): Cobb 1841's "foresail" the course (pp. 105-107), his
# "fore-and-aft foresail" the gaff sail (pp. 33-34, 79), his "fore-and-aft mainsail" (p. 95)
WORDS = {
    "foresail": ["fore.course"],
    "fore course": ["fore.course"],
    "fore-and-aft foresail": ["fore.sail"],
    "fore gaff sail": ["fore.sail"],
    "gaff foresail": ["fore.sail"],
    "mainsail": ["main.sail"],
    "fore-and-aft mainsail": ["main.sail"],
    "gaff topsail": ["main.gaff_topsail"],
    "main topgallant": ["main.topgallant"],
    "main topgallant sail": ["main.topgallant"],
    "main staysail": ["main.staysail"],
    "main topmast staysail": ["main.topmast_staysail"],
}


def test_her_sources_words_name_her_sails(her):
    table = noun_table(her)
    for phrase, ids in WORDS.items():
        noun = table.lookup(phrase)
        assert noun is not None and list(noun.ids) == ids, phrase


# ---------------------------------------------------------------------------
# The generator: her file as committed, and its report (Neuf-D §1.5, §3.5)
# ---------------------------------------------------------------------------

REPORT_PROBE = """
import sys
sys.path.insert(0, "tools")
import gen_ships
sys.modules["gen_ships"] = gen_ships
from ships import neufchatel as her
her.build(sys.argv[1])
"""


def test_the_generator_writes_her_file_as_committed_and_reports_its_checks(tmp_path):
    """`build()` raises the checks of Neuf-D §1.5 before her file is written and prints the
    generator's report: the tonnage, the masts' spacing and trucks, each sail as cut against her
    sail plan, the hull as drawn and every port triple's gap to the drawn side (none of the
    triples measured at its sill: each gap reported, none raised). Her file comes out as it
    stands."""
    done = subprocess.run(
        [sys.executable, "-c", REPORT_PROBE, str(tmp_path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert done.returncode == 0, done.stderr
    said = done.stderr
    assert (ROOT / HER).read_bytes() == (tmp_path / Path(HER).name).read_bytes()
    assert "hermaphrodite-brig: the Navy's rule on Winfield's keel and breadth gives 328." in said
    assert "hermaphrodite-brig: her masts 43.70 ft apart at the deck" in said
    assert "hermaphrodite-brig: her sails as cut: main.sail" in said
    drawn = "hermaphrodite-brig: the hull as drawn (freesail/ship/form.py):"
    assert f"{drawn} drawn displacement " in said and "against the filed 288 t" in said
    gaps = re.search(rf"{re.escape(drawn)} the upper deck's ports: [^\n]* by ([^m]*) m", said)
    assert gaps and len(gaps.group(1).split(",")) == 11
    assert "reported and never moved to the drawing" in said
    # her road's step 4: the quarter bill's arithmetic and the house's anchor rule set aside;
    # plain sail 1006 m2 to 959 with her fore staysail corrected from the working 93 m2 to the
    # triangle that fits forward of the fore mast, 46 (the lead's ruling of 2026-11-07, B2b), the
    # arithmetic 35.5 to 33.8 trimmers and the bill's 35 kept as written (for the lead); 34 by the
    # rule since the lead's ruling (6) of 2026-11-09 (old: "(35 written)")
    assert (
        "the quarter bill on 'as taken 1814': her plain sail 959 m2 against the brig-sloop's 766 "
        "carries the brig's 27 trimmers to 33.8 (34 written); of her 94 seamen, the beat takes 42 "
        "to her guns" in said
    )
    assert "hermaphrodite-brig: her rope's scales, fore 1.194, head 1.314, fore gaff" in said
    assert "bowers of 16.4 cwt by five to the hundred tons (32.6 by the beam rule)" in said
    assert "against Steel's 20 cwt and 13.5 in." in said


def test_her_notes_carry_no_figure_a_rule_computes():
    """The lead's notes of 2026-10-29, item 2: no rating's figure, no bowline's size, in her
    notes; what each rule read stays."""
    said = [line.strip() for line in text_of(HER).splitlines() if line.strip().startswith("#")]
    assert not [line for line in said if re.search(r" -> [0-9.]+ kN", line)]
    assert not [line for line in said if re.search(r"than the sheet, [0-9.]+ in", line)]
    assert [line for line in said if "Rating: fore.course" in line]


def test_her_class_is_served_in_the_periods_words():
    """Her era note's first clause is the class her readings serve (`ship_class_words`), in-world
    (package 85's rule): her type and her year, no capture she has not yet suffered and no build
    reference."""
    spec = load_spec(HER)
    said = ship_class_words(spec, spec.name)
    assert said == "a Baltimore privateer hermaphrodite brig of 1812, built at New York"
    for words in ("tools/", "ZAZ", "taken", "1815", "Neuf"):
        assert words not in said


def test_her_file_loads_rates_and_polars(her):
    """Her road's step 2 (Neuf-D §13): her file loads with no default rating, every spar and
    line rated, and draws a polar; its figures are pinned at step 5 (Neuf-D §9: her polar's test
    and 7-193, below)."""
    spec = load_spec(HER)
    assert spec.warnings == []
    assert all(ln.rating_kn > 0.0 for ln in her.lines.values())
    polar = polar_of(HER)
    assert all(v >= 0.0 for row in polar.speeds_kn for v in row)
    assert polar.closest_deg <= 90.0


# ---------------------------------------------------------------------------
# Her guns (Neuf-D §5; her road's step 4)
# ---------------------------------------------------------------------------

FIT = "as taken 1814"
# Adye 1804 (the page images read for her design): the 12-pounder carronade of 2 ft 2 in, 5 cwt
# 3 qr 10 lb (p. 72); the long 6-pounder of 8 ft 0 in, 22 cwt (p. 155)
ADYE_CWT = {("carronade", 12): 5.0 + 3.0 / 4.0 + 10.0 / 112.0, ("long", 6): 22.0}
# Douglas 1829 art. 136, four to a carronade; Falconer 1780, QUARTERS, five to a long 6
CREWS = {("carronade", 12): 4, ("long", 6): 5}


def guns_by(fit):
    """A fit's guns counted by (kind, pounder, place, deck)."""
    return Counter((g.kind, int(g.pounder), g.place, g.deck) for g in fit.guns)


def test_her_fit_guns_and_crews_are_the_periods():
    """Neuf-D §5.1-§5.4: her one fit, the Admiralty's record (Winfield 1793-1817 pp. 335-336): 16
    x 12-pounder carronades and 2 long 6-pounders, 18 pieces, no pivot; the carronades eight a side
    in the second to the ninth ports from forward, numbered from forward, the 6s bow chasers in the
    foremost, the two aftmost ports empty (judgement); Adye's weights, Douglas's and Falconer's
    crews; the privateer schooner's allowance, 40 round, 6 grape and 4 chain a gun, and no charges
    for exercise; the charges Table No. 29's, a 12-pounder carronade's 1 lb and a long 6's 2 lb;
    the filling party one to every four cannon (Falconer 1780, QUARTER-GUNNER)."""
    spec = load_spec(HER)
    arm = spec.armament
    assert arm.default == FIT and list(arm.fits) == [FIT]
    fit = arm.fits[FIT]
    assert guns_by(fit) == {
        ("carronade", 12, "broadside", "upper"): 16,
        ("long", 6, "bow", "upper"): 2,
    }
    triples = ports_of(spec.hull.profile, "upper")
    from_forward = sorted(triples, key=lambda t: -t[0])
    for g in fit.guns:
        key = (g.kind, int(g.pounder))
        assert g.weight_cwt == pytest.approx(ADYE_CWT[key], abs=0.005), g.id
        assert g.crew == CREWS[key], g.id
        port = [i for i, (x, _z, _hb) in enumerate(from_forward) if abs(g.x_m - x) <= 0.01]
        assert len(port) == 1 and abs(g.height_m - from_forward[port[0]][1]) <= 0.01, g.id
        if g.place == "bow":
            assert port == [0], g.id  # the foremost port a side
        else:
            assert port == [g.number], g.id  # No. 1 in the second port from forward
    side = sorted(
        (g for g in fit.guns if g.side == "starboard" and g.place == "broadside"),
        key=lambda g: g.number,
    )
    assert [g.x_m for g in side] == sorted((g.x_m for g in side), reverse=True)
    manned = {round(g.x_m, 2) for g in fit.guns}
    assert [t[0] for t in triples if round(t[0], 2) not in manned] == [-14.23, -11.37]
    assert fit.exercise_charges == 0
    assert fit.charges == {("carronade", 12.0): 1.0, ("long", 6.0): 2.0}
    assert fit.shot == {
        12.0: {"round": 40 * 16, "grape": 6 * 16, "chain": 4 * 16},
        6.0: {"round": 40 * 2, "grape": 6 * 2, "chain": 4 * 2},
    }
    assert fit.cartridges == {("carronade", 12.0): 55 * 16, ("long", 6.0): 55 * 2}
    assert spec.crew.quarter_bill.filling == 4


def test_the_builders_checklist_draws_every_gun_of_hers():
    """Build-Ships.md §6's postscript (package 81): every gun on its deck's triple at its own x
    within 0.01 m, the sill her sheet's (above) and the half-breadth her side's; `port_size_m` for
    her one deck with ports; every gun's weight within a tenth of the pattern the viewer draws it
    by; the checker clean. Her chase port's top stands 0.04 m above her traced rail, noted by the
    checker and not refused (Neuf-D §3.2: the end ports are shallower than the deck's one size)."""
    sys.path.insert(0, str(ROOT / "tools"))
    import check_viewer_guns

    spec = load_spec(HER)
    assert dict(spec.hull.profile.port_size_m)["upper"]
    for g in spec.armament.fits[FIT].guns:
        assert viewer_guns.figure(g.kind, g.pounder, g.weight_cwt).weight_off <= 0.01, g.id
    rep = check_viewer_guns.check(ROOT / HER)
    assert rep.ok, rep.lines
    assert not [line for line in rep.lines if line.strip().startswith("weight ")]
    assert "  fit 'as taken 1814': 18 guns: 18 port" in rep.lines
    assert "    empty ports a side: upper 2" in rep.lines
    notes = [line for line in rep.lines if line.strip().startswith("note ")]
    assert notes == [
        f"    note chaser.bow.{side}: its port cut to the rail (0.04 m)"
        for side in ("starboard", "larboard")
    ]


def test_her_broadside_by_70s_rule_is_a_hundred_and_eight_pounds():
    """Neuf-D §5.5: `far_ship` counts one side's broadside guns and every gun not on the
    broadside (combat/far.py): eight 12-pounder carronades and her two long 6s, 108 lb, where the
    brig-sloop fires 268 lb and the frigate-36 421 lb by the same rule (Indf §5.5)."""
    assert far_ship(HER, "united-states").broadside_lb == 108.0
    assert far_ship("data/ships/brig.yaml", "britain").broadside_lb == 268.0
    assert far_ship("data/ships/frigate-36.yaml", "britain").broadside_lb == 421.0


# ---------------------------------------------------------------------------
# Her company, her wardroom, her quarters (Neuf-D §6)
# ---------------------------------------------------------------------------


def test_her_company_holds_niles_and_cobb():
    """Neuf-D §6.1-§6.2, §6.4-§6.5: 130 (Niles vol. VII p. 284); twelve posts, a captain and five
    lieutenants among them (Cobb 1841 p. 40) and the surgeon (pp. 75-76); sixteen marines
    (judgement on Cobb p. 73); eight idlers; 94 seamen, no main top (her main a schooner's, p.
    91); more landsmen than the privateer schooner's (p. 39); the american list; the nine
    prize-masters one drawn by name, with a quartermaster and the boy who carries the word; the
    quarter bill's judgement figures."""
    crew = load_spec(HER).crew
    assert crew.complement == 130 and crew.names == "american"
    posts = [p.post for p in crew.posts]
    assert posts == [
        "captain",
        "first lieutenant",
        "second lieutenant",
        "third lieutenant",
        "fourth lieutenant",
        "fifth lieutenant",
        "master",
        "surgeon",
        "boatswain",
        "gunner",
        "carpenter",
        "sailmaker",
    ]
    assert sum(1 for p in posts if p.endswith(" lieutenant")) == 5
    st = crew.stations
    assert (st["marines"], st["idlers"], crew.seamen) == (16, 8, 94)
    assert (st["forecastle"], st["fore_top"], st["afterguard"], st["waisters"]) == (20, 24, 30, 20)
    assert st["main_top"] == st["mizzen_top"] == 0
    assert len(crew.posts) + crew.seamen + st["marines"] + st["idlers"] == crew.complement
    assert sum(crew.idlers_by_trade.values()) == st["idlers"]
    assert crew.ratings == {"able": 0.35, "ordinary": 0.35, "landsman": 0.30}
    privateer = load_spec("data/ships/privateer-schooner.yaml").crew.ratings
    assert crew.ratings["landsman"] > privateer["landsman"]
    assert [(p.role, p.station, p.rating, p.messenger) for p in crew.people] == [
        ("prize-master", "afterguard", "able", False),
        ("quartermaster", "afterguard", "able", False),
        ("boy", "afterguard", "landsman", True),
    ]
    bill = crew.quarter_bill
    # 34 by the rule (the lead's ruling (6) of 2026-11-09): the brig's 27 by her plain sail, 33.8,
    # rounded, split by largest remainder on Neuf-D's 9, 11 and 15 (old: 35, the afterguard's 15)
    assert bill.trimmers == {"forecastle": 9, "fore_top": 11, "afterguard": 14}
    assert (bill.helm, bill.powder, bill.priority) == (1, 2, "sail before guns")
    assert (bill.small_arms, bill.boarders) == (26, 85)


def test_her_ship_files_posts_and_people_agree_with_her_wardroom_file():
    """tests/test_wardroom.py's check (:42-57) on her file (Neuf-D §6.3): the generator draws the
    posts and the drawn roles from `data/people/hermaphrodite-brig.yaml` (spec M6 §2). Her
    outlines name no one and say no source's page, no judgement and no 'he' in the words served."""
    from freesail.world import people as PE

    wardroom = PE.load_wardroom(HER)
    assert wardroom is not None
    spec = load_spec(ROOT / HER)
    assert [p.post for p in spec.crew.posts] == wardroom.posts
    drawn = [
        (o.role, o.drawn["station"], o.drawn.get("rating"), o.messenger) for o in wardroom.drawn
    ]
    assert [(p.role, p.station, p.rating, p.messenger) for p in spec.crew.people] == drawn
    raw = yaml.safe_load((ROOT / "data" / "people" / "hermaphrodite-brig.yaml").read_text("utf-8"))
    assert raw["ship"] == HER
    assert wardroom.role_of("captain") == "captain"
    assert wardroom.role_of("officer of the watch") == "first lieutenant"
    assert wardroom.role_of("master") == "master"
    for entry in raw["wardroom"]:
        for key in ("traits", "history", "brief"):
            words = " ".join(entry[key]) if key == "traits" else entry[key]
            forbidden = r"Cobb|Neuf|p\. \d|judgement|\bhis\b|\bhe\b|\bhim\b"
            assert words and not re.search(forbidden, words), (entry["role"], key)


def test_her_quarters_at_the_beat_fill_every_gun_and_leave_the_trimmers_measured():
    """Neuf-D §6.4: `Quarters.beat` measured at muster on her fit at seed 7 (crew/quarters.py).
    Every gun crew fills: ten crews, a crew to each carronade pair and to each chaser, 42 men. The
    beat takes the marines to the carronades first (`_preferred_stations`, the engine's order for
    every ship bearing marines), so her sixteen stand at the carronades with sixteen of the
    afterguard, and no marines' division forms, as on the frigate-36 and the razee (Indf §18 item
    13): the design's 'the marines stand apart from the guns' is not what the engine does, and is
    reported. Her forecastlemen man the two long 6s; the trimmers are the bill's 34 and every
    seaman the guns leave, 65; the tiller one; the powder her two waisters and six idlers; the
    carpenter's crew at the wings. Old, with the bill's 35 (before the lead's ruling (6) of
    2026-11-09, 34 by the rule): fifteen of the afterguard and a waister at the carronades, the
    trimmers 65 the same, the afterguard's one more of them and the waisters' one fewer."""
    from freesail.crew.model import Station
    from freesail.crew.quarters import CARPENTER, HELM, MARINES, POWDER, TRIMMERS, quarters_of
    from tests.test_brains import world_at

    w = world_at(49.5, -5.5, HER)
    w.run(10)
    w.submit("beat to quarters")
    w.run(30)
    q = quarters_of(w.ship)
    assert all(len(gc.members) == gc.wanted for gc in q.crews.values())
    assert (len(q.crews), sum(gc.wanted for gc in q.crews.values())) == (10, 42)
    at_guns = Counter((gc.kind, s.station) for gc in q.crews.values() for s in gc.members)
    assert at_guns == {
        ("carronade", Station.MARINES): 16,
        ("carronade", Station.AFTERGUARD): 16,
        ("long", Station.FORECASTLE): 10,
    }
    assert not q.divisions.get(MARINES)
    sizes = {d: len(q.divisions[d]) for d in (TRIMMERS, HELM, POWDER, CARPENTER)}
    assert sizes == {TRIMMERS: 65, HELM: 1, POWDER: 8, CARPENTER: 2}
    assert not [e for e in w.log if e.kind == "order.rejected"]


# ---------------------------------------------------------------------------
# Her ground tackle, boats, pumps, hold and stores (Neuf-D §7)
# ---------------------------------------------------------------------------


def test_her_ground_tackle_is_steels_row_for_fourteen_guns_and_three_hundred_tons():
    """Steel 1794 vol. I, the anchor table's '14 Guns, 300 Tons' (three bowers of 20 cwt, a stream
    of 7 cwt and a kedge of 3 cwt 2 qr) and the cordage table's 'Sloops' column (five cables of 13
    1/2 in and a stream cable of 8 in), the page images read for her design (Neuf-D §7); the
    cables laid two, two and one (judgement); hemp in her years."""
    tackle = load_spec(HER).ground_tackle
    assert not tackle.chain
    anchors = {a.id: a for a in tackle.anchors}
    assert list(anchors) == ["best_bower", "small_bower", "sheet", "stream", "kedge"]
    bowers = ("best_bower", "small_bower", "sheet")
    for aid in bowers:
        assert anchors[aid].weight_kg == pytest.approx(20 * CWT_KG, abs=1.0), aid
        assert anchors[aid].cable_in == 13.5, aid
    assert [anchors[a].cable_fathoms for a in bowers] == [240.0, 240.0, 120.0]
    assert anchors["stream"].weight_kg == pytest.approx(7 * CWT_KG, abs=1.0)
    assert anchors["stream"].cable_in == 8.0
    assert anchors["kedge"].weight_kg == pytest.approx(3.5 * CWT_KG, abs=1.0)
    assert anchors["kedge"].cable_in == 6.75  # half the bower cable, the house's rule


def test_her_boats_pumps_hold_and_stores():
    """Neuf-D §7: her long boat amidships (Cobb 1841 p. 73) and a yawl (judgement) by Luce's rule
    on her 110 ft 8 in on deck, as the privateer schooner's; two hand pumps (Cobb p. 55, 'the
    pumps'; the kind judgement); her hold a trader's share of her 328 tons, 164 tons (Cobb p. 40:
    cleared for prize goods); water for two months at a gallon a man a day and provisions for
    three (judgement); a shot plug a gun; the brig-sloop's spare spars and rope; her sail room by
    the topsail schooner's method; the Navy's ration."""
    spec = load_spec(HER)
    assert spec.hold.capacity_tons == 164.0
    assert [(p.kind, p.hands) for p in spec.pumps] == [("hand", 2), ("hand", 2)]
    assert [(b.id, b.kind, b.length_ft) for b in spec.boats] == [
        ("long_boat", "long-boat", 22.0),
        ("yawl", "yawl", 18.0),
    ]
    stores = spec.crew.stores
    assert (stores.water_tons, stores.provisions_days) == (35.0, 90.0)
    # 130 men a gallon a day for sixty days, at ten pounds a gallon, in tons of 2,240 lb
    assert stores.water_tons == pytest.approx(130 * 60 * 10.0 / 2240.0, abs=0.5)
    assert stores.shot_plugs == 18.0 and stores.cordage_fathoms == 300.0
    assert stores.spars == {
        "topmast": 1,
        "topgallant_mast": 1,
        "yard": 1,
        "studdingsail_boom": 2,
        "jib_boom": 1,
    }
    assert [s.kind for s in stores.sails] == [
        "fore.sail",
        "fore.topsail",
        "jib",
        "fore.storm_staysail",
        "storm_trysail",
        "storm_jib",
    ]
    assert spec.crew.ration.table == "navy"


# ---------------------------------------------------------------------------
# Her description at far detail (Neuf-D §8; her road's steps 4 and 6)
# ---------------------------------------------------------------------------

WHAT = (
    "a hermaphrodite brig, a brig's foremast and a schooner's main, long and low, pierced for "
    "eleven guns a side"
)


def test_her_description_in_her_file_is_a_brig_at_four_miles_and_a_privateer():
    """Neuf-D §8, by SW-4's form (Build-Ships.md §8.1, §8.2): her file's description, rig 'a brig'
    (D15 (a): the tops make out a brig), her words, the role `privateer` (a role of
    `captains.ROLES` with its book), and her one fit, her file's default, so that a far ship of
    hers carries nothing new (the design's 'no fit' was written before SW-4's form, by which every
    row's file gives both). Rank 2 by her words before the first comma; none of them a man of
    war's."""
    own = S.file_descriptions(HER)
    assert list(own) == ["hermaphrodite brig"]
    d = own["hermaphrodite brig"]
    assert (d["rig"], d["what"], d["roles"], d["fit"]) == ("a brig", WHAT, ["privateer"], FIT)
    assert S._default_fit(HER) == FIT
    assert "privateer" in C.ROLES and C.load_doctrine("privateer").role == "privateer"
    assert C.SIZE_RANK["hermaphrodite brig"] == 2
    assert C.size_of_words(WHAT) == 2 and C.size_rank_of(WHAT) == 2
    assert not [w for w in C.MAN_OF_WAR_WORDS if w in WHAT]


@pytest.mark.parametrize(
    "words",
    [
        "hermaphrodite brig",
        "a hermaphrodite brig",
        "an hermaphrodite brig",
        "a privateer brig",
        "privateer brig",
        "the privateer brig",
        "an American hermaphrodite brig",
        "a French privateer brig",
    ],
)
def test_her_words_name_her_through_the_index(words):
    """Neuf-D §8, §14 (her road's step 6): her four phrases, Cobb's 'hermaphrodite brig' (1841 p.
    23) with either article and her log's 'privateer brig' (Stevens 1915 p. 26), give her key, and
    so do they qualified (their tail). 'A hermaphrodite brig' and 'an hermaphrodite brig' resolve
    by the index's own key since SW-4's reviews (`description_key` tries the whole words after the
    article first); their rows are kept as the lead accepted them (Neuf-D §17, lead item 9)."""
    assert S.description_key(words) == "hermaphrodite brig"


def test_a_brig_stays_the_merchant_brigs_and_her_index_row_is_her_files():
    """Neuf-D §8, §14, §18 item 7: 'a brig' and 'brig' still give the merchant brig; her index row
    names her file, whose words it serves with her fit and roles; her file's class is rank 2 (the
    player's shadow); a far ship of hers takes the role `privateer` and carries her default fit
    unwritten, and a role her file does not give is refused in words."""
    for words in ("a brig", "brig", "the brig"):
        assert S.description_key(words) == "merchant brig", words
    assert S.description("hermaphrodite brig") == {
        "file": HER,
        "rig": "a brig",
        "what": WHAT,
        "fit": FIT,
        "roles": ["privateer"],
    }
    assert S.DESCRIPTIONS["hermaphrodite brig"]["what"] == WHAT
    assert C.size_of_file(HER) == 2
    from tests.test_profile import _sea

    world = _sea()
    spec = {
        "description": "a privateer brig",
        "name": "Prince de Neufchatel",
        "nation": "united-states",
        "position": "49 30 N 5 30 W",
        "goal": "bound for Brest",
        "role": "privateer",
    }
    v = S.vessel_from_spec(world, dict(spec), 1)
    assert (v.description, v.ship_file, v.role, v.fit) == (
        "hermaphrodite brig",
        HER,
        "privateer",
        "",
    )
    assert brains.role_of_vessel(v, None) == "privateer"
    # with no role given, her file's first role (B2b, the lead's ruling of 2026-11-07: old, the
    # merchant's on a passage by the intent rules, which her row no longer keeps)
    assert brains.role_of_vessel(SimpleNamespace(description=v.description, role=""), None) == (
        "privateer"
    )
    with pytest.raises(ValueError, match="'kings-ship' is no role a hermaphrodite brig takes"):
        S.vessel_from_spec(world, dict(spec, role="kings-ship"), 2)


# Every row's role by `brains.role_of_vessel` with no role given, by the intent's kind: none,
# a passage, home, a station, a station cruising for prizes, a ground, a letter and a convoy
# (measured at B2's tree, 52fad521; package 75, B2b). Hers alone moved: by the intent rules
# merchant, merchant, merchant, kings-ship, privateer, fisherman, packet, commodore, where her
# file's first role is a privateer's now wherever the intent's kind names none. The bilander's row
# (package 75, B4), filed since 75 with `roles: [merchant]` (Bil-D §8), sails by its first role,
# a merchant wherever the intent's kind names none (measured at her landing, the same arithmetic).
INTENT_KINDS = (
    ("", False, False),
    ("passage", False, False),
    ("home", False, False),
    ("station", False, False),
    ("station", True, False),
    ("fish", False, False),
    ("letter", False, False),
    ("passage", False, True),
)
_TAIL = ["privateer", "fisherman", "packet", "commodore"]
ROLE_BY_INTENT = {
    "frigate": ["kings-ship"] * 4 + _TAIL,
    "schooner": ["merchant"] * 3 + ["kings-ship"] + _TAIL,
    "privateer schooner": ["merchant"] * 3 + ["kings-ship"] + _TAIL,
    "cutter": ["merchant"] * 3 + ["cruiser"] + _TAIL,
    "revenue cutter": ["revenue"] * 4 + _TAIL,
    "hired armed cutter": ["cruiser"] * 4 + _TAIL,
    "coasting cutter": ["merchant"] * 4 + _TAIL,
    "brig-sloop": ["cruiser"] * 4 + _TAIL,
    "merchant brig": ["merchant"] * 3 + ["kings-ship"] + _TAIL,
    "lugger": ["merchant"] * 3 + ["kings-ship"] + _TAIL,
    "privateer lugger": ["privateer"] * 4 + _TAIL,
    "smack": ["merchant"] * 3 + ["kings-ship"] + _TAIL,
    "sixty-four": ["kings-ship"] * 4 + _TAIL,
    "razee": ["kings-ship"] * 4 + _TAIL,
    "hermaphrodite brig": ["privateer"] * 4 + _TAIL,
    "bilander": ["merchant"] * 4 + _TAIL,
}


def test_her_row_sails_by_her_first_role_and_no_other_row_moves():
    """The lead's ruling (3)(b) of 2026-11-07 (package 75, B2b), the smallest road: her row files
    `roles: [privateer]` in her file as SW-4's sub-type rows do, and `brains.sub_type_role` reads
    the first role of any description that files them but the rows sailed before package 75,
    which keep the intent's rules (`brains.INTENT_RULED_ROWS`): so hers, the first whole file to,
    is a privateer wherever the intent's kind names no role, and every other row's role is as
    before at every intent's kind (`ROLE_BY_INTENT`, measured before the step). A crewed World's
    captain takes his own file's first row's by the same rule (`brains.own_sub_type_role`), hers
    alone of the files until the bilander's landing (package 75, B4), whose row, filed since 75
    with its roles, sails by its first role as hers does: a merchant."""
    for key, roles in ROLE_BY_INTENT.items():
        got = []
        for kind, prizes, convoy in INTENT_KINDS:
            intent = SimpleNamespace(kind=kind, prizes=prizes, convoy=convoy) if kind else None
            got.append(brains.role_of_vessel(SimpleNamespace(description=key, role=""), intent))
        assert got == roles, key
    assert set(ROLE_BY_INTENT) == set(S.DESCRIPTIONS)
    assert set(brains.SUB_TYPE_ROWS).isdisjoint(brains.INTENT_RULED_ROWS)
    own = {}
    for path in sorted((ROOT / "data" / "ships").glob("*.yaml")):
        world = SimpleNamespace(ship=SimpleNamespace(spec=SimpleNamespace(source=str(path))))
        own[path.name] = brains.own_sub_type_role(world)
    assert {k: v for k, v in own.items() if v} == {
        "bilander.yaml": "merchant",
        "hermaphrodite-brig.yaml": "privateer",
    }


def _her_world(intent="", papers=None):
    """Her crewed World under American colours off the Lizard (tests/test_brains.py's world)."""
    from datetime import datetime

    from freesail.api.session import make_world
    from freesail.core.world import Scenario

    sc = Scenario(
        start_time=datetime(1805, 6, 12, 10, 0),
        wind_from_deg=270.0,
        wind_speed_kn=14.0,
        gustiness=0.0,
        variability=0.0,
        position={"lat_deg": 49.5, "lon_deg": -5.5},
        region="channel-west",
        ports=["falmouth", "plymouth", "brest"],
        nation="united-states",
        intent=intent,
        papers=dict(papers or {}),
    )
    return make_world(7, HER, sc)


@pytest.mark.parametrize(
    "intent",
    [
        "",
        "bound for Plymouth",
        "keep the station off the Lizard within 10 miles",
        "cruise for prizes off the Lizard within 10 miles",
    ],
    ids=["no intent", "a passage", "a station", "cruising for prizes"],
)
def test_she_is_a_privateer_wherever_no_scenario_or_intent_names_a_role(intent):
    """The lead's ruling (3)(b) of 2026-11-07 (package 75, B2b): her own captain, crewed under
    American colours at seed 7, sails, signals and reads as a privateer wherever no scenario or
    intent names a role, as the privateer schooner does cruising for prizes: the privateer's book,
    the privateer's service, no private table (none unless the scenario's papers give her one,
    package 76's rule), and "a privateer of the United States" in her reading. Old, her wardroom's
    captain read as a King's commission (`captains._is_kings_ship`, left as it is): with no intent
    no role, the King's service, no private table and "a ship of the the United States navy"; on a
    passage and on a station the King's ship's book, the King's service, the private table of the
    United States and the same words. Cruising for prizes she was a privateer before as now."""
    from freesail.api import readings as R
    from freesail.world import service, signals

    w = _her_world(intent)
    c = w.captain
    assert (c.role, c.sub_type_role) == ("privateer", "privateer")
    assert (c.doctrine.role if intent else c.doctrine) == ("privateer" if intent else None)
    assert service.service_of(w) == "privateer" and signals.table_of(w) is None
    assert R.ship_words(w).startswith(
        "The ship: Prince de Neufchatel, a Baltimore privateer hermaphrodite brig of 1812, built "
        "at New York; a privateer of the United States."
    )
    papered = _her_world(intent, papers={"private_signals": True})
    assert signals.table_of(papered) is not None and papered.captain.role == "privateer"


def test_a_far_ship_of_hers_answers_a_hail_as_a_privateer():
    """Her far ship with no role given, on a passage and on a station (package 75, B2b): her
    brain's role the privateer's, she answers a hail by the privateer's table (data/captains/
    hail.yaml) and carries no private table. Old: on a passage the merchant's book and answer,
    on a station the King's ship's ("the United States brig ...") with the private table of the
    United States, her intent ruling her as the row's."""
    from freesail.world import hail, signals
    from tests.test_brains import put, world_at

    w = world_at(49.5, -5.5)
    goals = (
        ("bound for Brest", "bound for Brest"),
        ("patrolling off Ushant within 15 miles", "keep the station off Ushant within 15 miles"),
    )
    for n, (goal, intent) in enumerate(goals):
        at = "49 30.4 N 5 30 W"
        v = put(w, "hermaphrodite brig", "united-states", at, goal, intent=intent, name=f"N{n}")
        assert v.brain.role == "privateer"
        answer = hail.answer_by_table(w, v, "What ship is that?")
        assert answer.startswith(f"The privateer N{n} of "), answer
        assert signals.vessel_table(w, v) is None


# ---------------------------------------------------------------------------
# Her round trip under the rules captains at seed 7, no fit named (Neuf-D §11.3)
# ---------------------------------------------------------------------------

EXERCISING = ROOT / "data" / "scenarios" / "exercising-the-great-guns.yaml"


def test_her_scenario_round_trips_and_she_sails_it_under_the_rules_captain_with_no_fit_named(
    tmp_path,
):
    """What is common to any scenario of hers (Neuf-D §11.3), built with no scenario file of hers
    (B6 out to a supplemental package): a scenario written from its fields by the harbour's maker
    (the great guns' with her file in the frigate's place, under American colours and cruising for
    prizes off the Lizard) reads back to itself and loads with no fit named; she sails it at seed 7
    under her rules captain by the privateer's book with her default fit, a British brig-sloop in
    sight under a cruiser's, and no order of hers refused; saved at half an hour and loaded from
    the checkpoint, she carries on as the world that was never saved. Measured: an hour in, 6.22
    kn in ten knots of wind, her captain a privateer investigating the stranger, as before, at
    `clr_x_m` -0.6 (the owner's ruling for the lead of 2026-11-08, B2c; old beside new: 6.19 at
    +0.1 before it; 6.02 kn with her fore staysail the working 93 m2, before package 75's B2b
    corrected it to the triangle that fits forward of the fore mast, 46; before the jib's mend of
    the reviews of 2026-11-07, 6.11 at her start's `clr_x_m` +0.3 and 5.95 at step 5's +2.0). The
    hour is all it asks: run on, she stands on to the north while she investigates and takes the
    ground at 4,266 s in a fathom and a half (4,251 s at +0.1; with the 93 m2, on the Stags at
    3,911 s, the lookout's warning at 3,300 s not acted on), since the captain's danger-ahead
    states leave out "investigating a stranger" (world/captains.py; the rules captain's, for the
    lead's list, not mended: the lead's ruling (3)(c) of 2026-11-07)."""
    from freesail.api.session import ship_factory
    from freesail.core import replay as replay_mod
    from freesail.world.scenarios import (
        begin,
        load_scenario,
        make_scenario_world,
        read_scenario_text,
        scenario_text,
        write_scenario,
    )

    _text, fields = read_scenario_text(EXERCISING)
    fields = copy.deepcopy(fields)
    fields["name"] = "A privateer off the Lizard"
    fields.pop("standing_orders")  # her rules captain's book alone
    fields["nation"] = "united-states"
    fields["intent"] = "cruise for prizes off the Lizard within 10 miles"
    fields["ship"]["file"] = HER
    assert "fit" not in fields["ship"]
    fields["ships"] = [
        {
            "description": "brig-sloop",
            "name": "Stranger",
            "nation": "britain",
            "position": "49 45 N 5 20 W",
            "goal": "bound for Plymouth",
            "intent": "bound for Plymouth",
        }
    ]
    written = write_scenario(fields, tmp_path / "hers.yaml")
    new = written.read_text(encoding="utf-8")
    again_text, again = read_scenario_text(written)
    assert scenario_text(again, again_text) == new
    sf = load_scenario(written)
    assert sf.seed == 7 and sf.ship_file == HER and sf.scenario.fit is None
    world = make_scenario_world(sf)
    begin(world, sf)
    assert world.ship.fit == FIT
    assert world.captain.commands and world.captain.role == "privateer"
    stranger = world.vessels.find("Stranger")
    assert stranger.ship_file == "data/ships/brig.yaml" and stranger.brain.role == "cruiser"
    world.run(1800)
    saved = replay_mod.save_to_file(world, tmp_path / "hers.json")
    world.run(1800)
    assert not [e for e in world.log if e.kind == "order.rejected"]
    assert units.ms_to_knots(world.ship.dyn.speed) == pytest.approx(6.22, abs=0.5)
    loaded, how = replay_mod.load(saved, ship_factory)
    assert how == "checkpoint" and loaded.ship.fit == FIT
    loaded.run(1800)
    assert loaded.clock.tick == world.clock.tick and loaded.state() == world.state()


# ---------------------------------------------------------------------------
# Her line of the lee ports' truth, 7-190 (Neuf-D §3.4, §10; Build-Ships.md §7)
# ---------------------------------------------------------------------------


def test_her_lowest_lee_port_shuts_at_eighteen_degrees_and_a_roll_sooner():
    """Her line of 7-190, measured by its draft's own form (tests/test_lee_ports.py; §7.1's rule as
    built, the minute's hold included), for its table (`LOWEST_LEE_PORT`) to take with her file:
    her fit in a World that keeps a sea, her heel to starboard and her roll set by hand on the
    World's own names. Her lowest port with a gun in it, No. 5 amidships (1.50 m, half-breadth 3.83
    m at its sill), shuts at 18.18 degrees of heel alone (Neuf-D §3.4's 18.2); open half a degree
    below, shut a degree above with three of her lee ports (Nos. 4, 5 and 6), and a roll of 4
    degrees on her motion the same four degrees sooner by the same count; her weather side open;
    upright again, every port open once the minute's hold has run."""
    from tests import test_lee_ports as L

    w = L._in_a_sea(HER)
    assert w.ship.fit == FIT
    gid, heel = L._lowest_lee(w, "upper")
    assert gid == "gun.5.starboard" and heel == pytest.approx(18.18, abs=0.05)
    assert L._open_then_shut(w, "upper", 18.18, 0.0, 0) == (0, 3)
    assert L._open_then_shut(w, "upper", 18.18, L.ROLL_SET_DEG, 4 * L.HOLD) == (0, 3)


# ---------------------------------------------------------------------------
# Her polar (Neuf-D §9; her road's step 5), in tests/test_ships.py's form
# ---------------------------------------------------------------------------

FRIGATE = "data/ships/frigate-36.yaml"
BRIG = "data/ships/brig.yaml"
SCHOONER = "data/ships/topsail-schooner.yaml"


def test_her_polar_is_drawn_from_her_file_and_agrees_with_her_sailed_beam_reach():
    """`polar_of` balances the sails model against her hull's resistance at each angle off the
    wind (tests/test_ships.py:74-93's form, her own figures). Her beam reach in fifteen knots is
    within half a knot of the one she sails under plain sail with the yards trimmed (the known
    truths' `under_plain_sail` at 90 degrees: 8.29 kn, heeling 5.4 degrees; the polar 8.53), and
    her polar's beam reaches in 8, 15 and 25 kn are her measured 4.85, 8.53 and 12.07 kn (+-0.5).
    Old beside new: 4.95, 8.68 and 12.22 (sailed 8.43 kn, heeling 5.5) before her fore staysail
    was corrected from the working 93 m2 to the triangle that fits forward of the fore mast, 46
    (the lead's ruling of 2026-11-07, B2b); 4.99, 8.73 and 12.27 before the reviews of 2026-11-07
    moved her jib's centre aft to its triangle's. Her start figures stand (Neuf-D §9's knobs;
    docs/dev/TuningNotes.md):
    `hull_speed_kn` 12.9 kept, her best in 25 kn inside her accounts' band at every hull speed of
    12.5-13.9 (12.09 to 12.67 kn, measured before the jib's mend); `gm_m` 2.1 kept (no account
    gives her heel); `clr_x_m`, tuned for her helm (+0.3 to -0.6), is not read by the polar (at
    B2c's re-tune, +0.1 to -0.6, every cell of her polar the same to the last bit; her sailed
    beam reach 8.29 kn as before).
    Beside her, by the same arithmetic: the frigate-36 4.62, 8.19 and 11.63 kn at her best (90, 90
    and 100 degrees), the brig-sloop 4.57, 7.92 and 10.97 (100 degrees), the topsail schooner
    4.59, 7.92 and 10.95 (100, 90, 90). Her closest angle, 40 degrees, the schooners', inside the
    frigate's and the brig's 50 (truth 2's order); she beats at 60 in every wind, the schooners at
    50 in 25 kn."""
    from tests.test_known_truths import knots, under_plain_sail

    p = polar_of(HER)
    measured = {8.0: 4.85, 15.0: 8.53, 25.0: 12.07}
    for wind, kn in measured.items():
        assert abs(p.speed_kn(90.0, wind) - kn) <= 0.5, (wind, p.speed_kn(90.0, wind))
    assert p.speed_kn(90.0, 8.0) < p.speed_kn(90.0, 15.0) < p.speed_kn(90.0, 25.0)
    assert p.speed_kn(20.0, 15.0) == 0.0  # nothing closer than the grid's first angle
    assert p.closest_deg == polar_of(SCHOONER).closest_deg < polar_of(BRIG).closest_deg
    assert p.beat_deg(15.0) == p.beat_deg(25.0) == 60.0
    sailed = knots(under_plain_sail(HER, 270.0))
    assert abs(p.speed_kn(90.0, 15.0) - sailed) <= 0.5, sailed


def test_truth_7_193_her_polars_best_point_from_her_accounts():
    """Neuf-D §14 truth 2 (Build-Ships.md §15), a draft for Phase 5 to move into
    tests/test_known_truths.py. Her best speed in 25 kn of wind under plain sail (`polar_of`)
    within her accounts' band, 11.5 to 13.0 kn: Cobb 1841's 12.5 knots twice, running (p. 54,
    out of Boston with the yards squared, the unit loose; p. 138, the gale chase), the band
    judgement (Neuf-D §9), held wherever the engine puts it (the owner, 2026-10-29: "don't worry
    about tuning for best speed running"; the lead's answer 5 at Neuf-D §17). Her pointing: her
    `closest_deg` no wider than the frigate-36's, and her speed at 60 and 70 degrees off in 15
    and 25 kn above the frigate-36's ("we could haul closer upon the wind than the enemy", Cobb
    p. 96, her strongest evidence), pinned because her file bears it out.

    Measured on the owner's machine, 2026-11-08, her start figures standing (`hull_speed_kn`
    12.9) and her fore staysail the triangle that fits forward of the fore mast, 46 m2 (the lead's
    ruling of 2026-11-07, B2b: the design's working 93 m2 a derivation of its own): her best in 25
    kn 12.07 kn, inside the band as before (old beside new: 12.22 with the 93 m2, 12.27 before the
    jib's mend of the reviews of 2026-11-07). **Reported, not pinned:** the best point's angle, 90
    degrees (12.06 kn at 100; 12.22 and 12.20 before), where her accounts were running; at 150
    degrees 9.92 kn and dead before it 9.35 (10.00 and 9.42 before; the frigate-36 10.01 and
    9.23); sailed with her studding sails set, 11.12 and 10.37 kn (11.17 and 10.36 before) against
    the frigate-36's 11.70 and 10.76, so that the frigate gains on her running as the frigates did
    (Cobb p. 97). Her closest 40 degrees against the frigate's 50; at 60 and 70 degrees 6.30 and
    7.14 kn in 15 kn against the frigate's 4.29 and 6.14, and 9.54 and 10.60 in 25 kn against 7.03
    and 9.62 (6.53, 7.34, 9.81 and 10.80 before), the slimmest margin 0.98 kn at 70 degrees in 25
    kn (1.18 before; Neuf-D §9's 0.8 on its stand-in). Arithmetic on the files ("the same on every
    machine", world/ships.py)."""
    hers, frigate = polar_of(HER), polar_of(FRIGATE)
    best = max(hers.speeds_kn[hers.winds_kn.index(25.0)])
    assert 11.5 <= best <= 13.0, best
    assert hers.closest_deg <= frigate.closest_deg
    for wind in (15.0, 25.0):
        for off in (60.0, 70.0):
            assert hers.speed_kn(off, wind) > frigate.speed_kn(off, wind), (off, wind)


# ---------------------------------------------------------------------------
# Her helm as tuned, and her handling (Neuf-D §9, §12.2 item 8; her road's step 5)
# ---------------------------------------------------------------------------


def test_her_helm_as_tuned_is_balanced_close_hauled():
    """Step 5's close-hauled band (Neuf-D §9's knob, `clr_x_m`, tuned with her rig whole in the
    topsail schooner's way: "at +0.5 m she is balanced close-hauled in 15 kn";
    docs/dev/TuningNotes.md, old beside new), measured at seed 7 in fifteen knots under plain
    sail, the yards and sheets trimmed, 60 degrees off (her `beat_deg`; the topsail schooner's
    -0.04): **-1.0 to +1.7 degrees** of weather helm, step 5's -1.0 to +1.5 widened by 0.2
    degrees by the owner's ruling for the lead of 2026-11-08 ("Re-tune, widen bands 0.2
    degrees"; package 75, B2c). The reason: her fore staysail corrected to the 46 m2 that fits
    forward of her fore mast (the lead's ruling of 2026-11-07, B2b) gives her the weather helm
    close-hauled, and her helm falls from close-hauled to the beam where the schooner's rises, so
    that no single lead holds both of step 5's bands (swept at B2b: -0.3 m gives +2.66
    close-hauled and +0.92 abeam, -0.6 +1.65 and +0.39, -0.9 +0.60 and -0.17, -1.2 -0.50 and
    -0.75). At **-0.6 m** she carries +1.65 degrees close-hauled, +2.25 at six points and +1.30
    at seven; +2.44 at 60 degrees in 25 kn. Old beside new: at +0.1 (B2b's) +3.95, +4.30
    and +2.81, +5.09 in 25 kn, this test then a strict known failure (from the review of
    2026-11-08 to B2c, its band moved to her measure, +2.5 to +5.0, at B2b's build); with the
    working 93 m2 at +0.1, +1.11, +2.11 and +1.49, +1.75 in 25 kn, inside step 5's band. Before
    the reviews of 2026-11-07 moved her jib's centre aft to its triangle's (from above its stay),
    she was tuned to +2.0 against the lee helm the misplaced jib gave her."""
    from tests.test_known_truths import reading, under_plain_sail

    close_hauled = reading(under_plain_sail(HER, 300.0))["weather_helm"]
    assert -1.0 <= close_hauled <= 1.7, close_hauled


def test_her_helm_as_tuned_abeam_and_at_ten_points():
    """Step 5's band abeam and at ten points, **+0.3 to +4.0 degrees** of weather helm (+0.5 to
    +4.0, its lower bound widened by 0.2 degrees by the owner's ruling for the lead of 2026-11-08;
    package 75, B2c, the test above), measured as the close-hauled band at seed 7 in fifteen
    knots under plain sail, the yards and sheets trimmed, with `clr_x_m` as tuned, **-0.6 m**:
    +0.39 abeam (the frigate-36 +1.99, the brig-sloop +1.57, the topsail schooner +4.30) and +1.39
    at ten points, +3.06 at twelve; +0.07 abeam in 25 kn. Old beside new: at +0.1 (B2b's)
    +1.61, +2.10 and +3.16, +1.60 in 25 kn; with the working 93 m2 at +0.1, +0.78, +1.84 and
    +3.20, +0.73 in 25 kn. Split from the close-hauled band at the review of 2026-11-08, while
    that one was a recorded departure."""
    from tests.test_known_truths import reading, under_plain_sail

    for off in (90.0, 112.5):
        helm = reading(under_plain_sail(HER, 360.0 - off))["weather_helm"]
        assert 0.3 <= helm <= 4.0, (off, helm)
    assert load_spec(HER).hull.clr_x_m == -0.6


def test_truth_6_her_headsails_and_her_mainsail_set_her_helm():
    """Truth 6's form on her file as tuned (tests/test_known_truths.py), abeam in 15 kn, seed 7:
    +0.39 degrees of weather helm under plain sail, +4.23 with the headsails in, -13.02 (lee
    helm) with the headsails set and the mainsail, her driving sail, in, at `clr_x_m` -0.6 (the
    owner's ruling for the lead of 2026-11-08, B2c; at +0.1 before it: +1.61, +5.29, -11.24; with
    the working 93 m2 fore staysail before B2b: +0.78, +5.13, -11.73; at the start's `clr_x_m`
    +0.3 then: +1.13, +5.39, -11.24)."""
    from tests.test_known_truths import run, under_plain_sail

    world = under_plain_sail(HER, 270.0)
    plain = math.degrees(world.ship.dyn.weather_helm)
    world.submit("take in the headsails")
    run(world, 900, trim_every=120)
    without_headsails = math.degrees(world.ship.dyn.weather_helm)
    assert without_headsails > plain + 1.0
    world.submit("set the headsails")
    world.submit("take in the mainsail")
    run(world, 900, trim_every=120)
    without_mainsail = math.degrees(world.ship.dyn.weather_helm)
    assert without_mainsail < 0.0 and without_mainsail < plain


def test_her_light_main_yards_swing_short_at_main_topsail_haul():
    """The lead's rulings 1 and 2 of 2026-11-06 (Luce 1884 p. 417), built at B3.4, on her file:
    her main crossing no course, her two light main yards, every after yard of hers on a
    schooner's mast, are hauled by "Main-topsail haul." in the short after swing,
    `light_after_swing_s`'s 20 s and not `brace_s`'s 45, as the fixture with her main topgallant
    (tests/test_schooner_mast.py). The word kept for her by the lead's ruling (2)(c) of
    2026-11-07: the order names the haul of the after yards and not the sail, and no source
    gives a schooner's own word (her design's §12.2). Her fore course set, its tack is kept fast
    at the haul and risen apart at "let go and haul" (the ruling's (2)(a), B3.4b; Luce 1884 pp.
    421, 428, 446; the next test). Old beside new: "Rise tacks and sheets. Main-topsail haul"
    from her file's first tree to B3.4b."""
    from freesail.evolutions import EVOLUTIONS

    ship = load_ship(HER)
    for sid in ship.groups["plain sail"]:
        ship.sails[sid].state = SailState.SET
    tack = scripts.TackScript(ship, {}, EVOLUTIONS["tack"].timing)
    assert [y.id for y in tack.after] == ["main.topsail.yard", "main.topgallant.yard"]
    assert tack._after_swing_s() == 20.0
    assert tack._haul_words() == "Main-topsail haul"
    assert tack._courses_drawing() == (True, False)


def test_she_stays_quickly_her_light_main_yards_hauled_short():
    """Truth 10's form on her file as tuned, measured at seed 7 in 15 kn, beside trial A's on this
    tree (the topsail schooner with a fore course, settled 2,400 s: tacked in 149 s; Eng §3.3)
    and the main topgallant's fixture (172 s with it set, 164 s furled; B3.4, ruling 1). From
    292.5 degrees she tacks in 189 s (from 290 and 295: 192 and 193 s), gaining 114 m to
    windward: "Main-topsail haul." at 53 s, hanging in stays at 63 s, and "Rise fore tack and
    sheet. Let go and haul." at 77 s, her light main yards swung in 24 s (the short swing's 20 by
    the weather and the hands), and no "Mainsail haul"; at `clr_x_m` -0.6, the owner's ruling for
    the lead of 2026-11-08 (B2c). Old beside new: at +0.1 before it, 261 s (269 and 268), gaining
    144 m, the words at 50 and 75 s, hanging in stays at 62 s; with her fore staysail the working
    93 m2 before it was corrected to the triangle that fits forward of the fore mast, 46 (the
    lead's ruling of 2026-11-07, B2b), 182 s (184 and 181), gaining 118 m, the words at 49 and 74
    s, never in stays. At the start's `clr_x_m` +0.3 she tacked then in 198 s (229 and 224),
    gaining 129 m (docs/dev/TuningNotes.md). Old beside new, words only, every tick the same:
    "Rise tacks and sheets. Main-topsail haul." and "Let go and haul." until B3.4b, where her
    fore tack is kept fast at the haul and risen apart before her head yards are hauled (the
    lead's ruling (2)(a) of 2026-11-07; Luce 1884 pp. 421, 428, 446)."""
    from tests.test_known_truths import close_hauled_on_starboard, until

    world = close_hauled_on_starboard(HER)
    y_before, start = world.ship.dyn.y, world.clock.tick
    world.submit("tack ship")
    done, seconds = until(world, ("ship.tacked", "ship.missed_stays"), 900)
    assert [e.kind for e in done] == ["ship.tacked"]
    assert 120 <= seconds <= 300, seconds
    assert world.ship.dyn.tack == "larboard" and world.ship.dyn.y > y_before
    haul = "Main-topsail haul."
    let_go = "Rise fore tack and sheet. Let go and haul."
    said = {}
    for e in world.log:
        for key in (haul, let_go, "Mainsail haul", "Rise tacks and sheets"):
            hit = e.text.startswith(key) if key in (haul, let_go) else key in e.text
            if e.tick >= start and hit:
                said.setdefault(key, e.tick - start)
    assert set(said) == {haul, let_go}  # no "Mainsail haul" (ruling 2), the fore tack apart
    assert 20 <= said[let_go] - said[haul] <= 35


def test_she_wears_and_lies_to_as_a_fore_and_after_with_a_square_fore():
    """Truths 11 and 12's forms on her file as tuned, measured at seed 7 in 15 kn, beside trial
    A's (wore in 449 s; hove to 50.2 degrees off at 2.65 kn; Eng §3.3). She wears in 452 s
    keeping her mainsail ("Up helm; brace in the after yards"), 249 m to leeward. Hove to the
    fore-and-after's way (the mainsail sheet flat aft, the fore staysail to windward, the fore
    topsail aback, the helm a-lee) she lies 51.3 degrees off forereaching 3.12 kn, inside truth
    12's band of angle (45-65) and above its 1.6 kn, as trial A is. With her main topgallant set
    abaft the backed fore (the heave-to clews up the light sails forward of the backed yards only:
    Neuf-D §12.2 item 8's second finding) she lies 51.3 degrees off at 3.09 kn, the sail still set,
    within truth 12's band. At `clr_x_m` -0.6, the owner's ruling for the lead of 2026-11-08
    (B2c); old beside new: at +0.1 before it, 521 s and 241 m, 49.1 degrees at 2.59 kn, 49.0 at
    2.56 with the main topgallant set; her fore staysail the working 93 m2 before it was
    corrected to the triangle that fits forward of the fore mast, 46 (the lead's ruling of
    2026-11-07, B2b): 461 s and 255 m; 51.1 degrees at 3.01 kn, 51.0 at 2.98 with the main
    topgallant set; at the start's `clr_x_m` +0.3 then: 467 s, 50.4 degrees at 2.86 kn."""
    from tests.test_known_truths import (
        close_hauled_on_starboard,
        events,
        knots,
        off_wind,
        run,
        wear,
    )

    world = close_hauled_on_starboard(HER)
    seconds, _lost = wear(world)
    assert 360 <= seconds <= 600, seconds
    assert world.ship.dyn.tack == "larboard" and world.ship.sails["main.sail"].is_set
    assert not [e for e in world.log if "brail up the mainsail" in e.text.lower()]
    for topgallant in (False, True):
        world = close_hauled_on_starboard(HER, speed_kn=5.0)
        if topgallant:
            world.submit("set the main topgallant")
            run(world, 600, trim_every=120)
            assert world.ship.sails["main.topgallant"].is_set
        start = world.clock.tick
        world.submit("heave to")
        run(world, 300)
        offs, speeds = [], []
        for _ in range(600):
            world.tick()
            offs.append(off_wind(world))
            speeds.append(knots(world))
        assert all(45.0 <= o <= 65.0 for o in offs), (topgallant, min(offs), max(offs))
        assert max(speeds) < 3.5, (topgallant, max(speeds))
        assert events(world, "ship.hove_to") and events(world, "ship.aback", after=start) == []
        assert world.ship.sails["main.topgallant"].is_set is topgallant


def test_she_gets_under_way_from_her_anchor_as_a_schooner():
    """Getting under way (B3.4's measure, trial A's form: anchored off Falmouth in 15 kn, the wind
    north, her head south-west, "get under way" after a quarter of an hour at her best bower):
    she casts on the starboard tack under her fore topsail, her mainsail and her jib, the topsail
    yard abox, as the rule has a fore-and-after with yards on her fore cast, and is under way in
    1,465 s (trial A 1,475 s), 5.8 kn full and by (at `clr_x_m` -0.6, B2c; 1,466 s and 5.8 kn
    at +0.1 before it)."""
    from datetime import datetime

    from freesail.api.session import make_world
    from freesail.core.world import Scenario
    from tests.test_known_truths import knots, until

    scenario = Scenario(
        wind_from_deg=0.0,
        wind_speed_kn=15.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=225.0,
        ship_speed_kn=0.0,
        start_time=datetime(1805, 6, 10, 10, 0),
        position={"lat_deg": 50.133, "lon_deg": -5.035},
        region="channel-west",
    )
    world = make_world(7, HER, scenario)
    world.run(60)
    world.submit("let go the best bower")
    world.run(900)
    start = world.clock.tick
    world.submit("get under way")
    done, seconds = until(world, ("ship.under_way", "evolution.failed"), 2400)
    assert [e.kind for e in done] == ["ship.under_way"]
    assert 1200 <= seconds <= 1800, seconds
    assert "on the starboard tack, under the topsail and the mainsail and the jib" in done[0].text
    said = " ".join(e.text for e in world.log if e.tick > start)
    assert "The topsail yard abox." in said and "spanker" not in said
    assert knots(world) > 4.0


def test_shorten_sail_takes_in_her_main_topgallant():
    """B3.4's finding mended in her file (her main topgallant in "royals"), sailed: under plain
    sail with her main topgallant set, in 15 kn abeam, "shorten sail" takes it in with the fore
    topgallant ("Took in the main topgallant; hanging in the gear"), where her design's groups
    kept it out of every group the list reaches."""
    from tests.test_known_truths import run, under_plain_sail

    world = under_plain_sail(HER, 270.0)
    world.submit("set the main topgallant")
    run(world, 600, trim_every=120)
    topgallant = world.ship.sails["main.topgallant"]
    assert topgallant.is_set
    start = world.clock.tick
    world.submit("shorten sail")
    run(world, 600)
    assert not topgallant.is_set
    taken_in = [e.text for e in world.log if e.tick > start and e.kind == "sail.taken_in"]
    assert any("main topgallant" in t for t in taken_in), taken_in


def test_her_gale_reefs_her_fore_course_twice_and_keeps_her_mainsail():
    """Her gale against her accounts: on 28 December 1814 she lay under "a closely reefed
    mainsail and a double-reefed foresail" (Cobb 1841 p. 95), Cobb's foresail her course (pp.
    105-107). By the lead's ruling 4 (`orders.storm._after_sail_lines`; Luce 1884 p. 476) a
    fore-and-after with topsails reefs her course once as the topsails take their second reef and
    once more at the third, her two reef bands then taken, and takes in nothing after: her
    mainsail, her driving sail, is kept whole, no line of "shorten sail" reefing a fore-and-
    after's gaff mainsail (the closely reefed mainsail not built, the lead's). Her fore gaff sail,
    a boomless gaff sail on the mast that crosses her course, is not taken in by the gale's
    reduction but when she lies a-try, as Cobb has it (1841 p. 79): the owner's ruling for the
    lead of 2026-11-08 ("At lie a-try"; package 75, B2c). At B2b (the lead's ruling (3)(e) of
    2026-11-07) it was taken in with the topsails' second reef ("take in the fore sail" beside
    the course's line from her topsails' first reef on), and once the jib was in she griped up to
    37-38 degrees off at about 2 kn with the helm hard over until she lay a-try. Sailed in the
    gale of B3.4's reviews (15 kn rising to 44, "shorten sail" at six winds, "lie a-try" at 7,200
    s; measured, docs/dev/TuningNotes.md, B2c), at `clr_x_m` -0.6: the course reefed at 4,625 s
    and again at 5,600 s, the fore topsail close-reefed, the jib in at 30 kn (5,364 s), after it a
    luff of three minutes to 47 degrees off and then 65-69 degrees off at 10-11 kn with the helm
    19-24 degrees over until lie a-try, the fore storm
    staysail set at 34 kn (6,780 s); lying a-try at 7,677 s under the fore topsail, the mainsail
    and the staysails, the course and the fore gaff sail taken in by "lie a-try", and at 8,400 s
    38.9 degrees off at 3.26 kn under the fore topsail, the mainsail and the storm staysail. Old
    beside new: at B2b, the fore gaff sail in at 4,487 s, the course reefed at 4,622 and 5,581 s,
    lying a-try at 7,664 s, and at 8,400 s 36.1 degrees off at 5.29 kn; before B2b, with her fore
    staysail the working 93 m2, the course reefed at 4,628 and 5,616 s, the fore storm staysail
    set at 34 kn, lying a-try at 7,674 s, and at 8,400 s 39.7 degrees off at 2.45 kn under the
    fore topsail, the storm staysail, the fore gaff sail and the mainsail whole."""
    from freesail.orders.storm import _after_sail_lines

    ship = load_ship(HER)
    for sid in ship.groups["plain sail"]:
        ship.sails[sid].state = SailState.SET
    course, topsail = ship.sails["fore.course"], ship.sails["fore.topsail"]
    assert (course.reef_bands, topsail.reef_bands) == (2, 3)
    assert not _square_rigged(ship)
    assert _after_sail_lines(ship) == []
    topsail.reefs = 1
    assert _after_sail_lines(ship) == ["reef the fore course, one reef"]
    course.reefs, topsail.reefs = 1, 2
    assert _after_sail_lines(ship) == ["reef the fore course, one reef"]
    course.reefs = 2
    assert _after_sail_lines(ship) == []
    assert ship.sails["fore.sail"].is_set  # handed at lie a-try, not by the gale's reduction
    assert ship.sails["main.sail"].is_set and ship.sails["main.sail"].reefs == 0


def test_only_she_has_a_boomless_gaff_sail_beside_a_course():
    """The guard of the lead's ruling (3)(e) of 2026-11-07 (package 75, B2b): lie a-try's handing of
    a boomless gaff sail on a mast that crosses a course (`scripts.gaff_sails_beside_a_course`)
    is hers alone of the files, her fore gaff sail abaft her fore course (the gale's take-in of it
    at the topsails' second reef, B2b's, moved to lie a-try by the owner's ruling for the lead of
    2026-11-08, B2c). The schooners' fore gaff sails are boomless too, but their fore masts cross
    no course; every other gaff sail is on its boom."""
    found = {}
    for path in sorted((ROOT / "data" / "ships").glob("*.yaml")):
        ship = load_ship(path)
        found[path.name] = [sl.id for sl in scripts.gaff_sails_beside_a_course(ship)]
    assert {k: v for k, v in found.items() if v} == {"hermaphrodite-brig.yaml": ["fore.sail"]}
    for name in ("topsail-schooner.yaml", "privateer-schooner.yaml"):
        fg = load_ship(ROOT / "data" / "ships" / name).sails["fore.sail"]
        assert fg.cls == "gaff" and "boom" not in fg.roles  # boomless, but no course beside it


def test_she_lies_a_try_under_her_mainsail_her_fore_gaff_sail_taken_in():
    """Lie a-try on her (the lead's ruling (3)(e) of 2026-11-07, package 75's B2b): her fore gaff
    sail handed with the square sails, she lies to under the fore topsail, her mainsail and her
    staysails, and the line names her two gaff sails: "Lying a-try under the fore topsail, the
    mainsail and the staysails, the fore-and-aft foresail taken in, helm a-lee." Old: "Lying
    a-try under the fore topsail and the staysails, helm a-lee.", whatever was set, her two gaff
    sails standing whole beside it. Every other file's line is as it was ("the main topsail and
    the staysails" on the frigate, truth 28's). Since the owner's ruling for the lead of
    2026-11-08 ("At lie a-try"; B2c) this is where her fore gaff sail is taken in, as Cobb has
    it (1841 p. 79), and not at the topsails' second reef; the handing and the line as built at
    B2b."""
    from tests.test_known_truths import run, under_plain_sail

    world = under_plain_sail(HER, 300.0)
    start = world.clock.tick
    world.submit("lie a-try")
    run(world, 600)
    lying = [e.text for e in world.log if e.tick > start and e.kind == "ship.hove_to"]
    assert lying == [
        "Lying a-try under the fore topsail, the mainsail and the staysails, the fore-and-aft "
        "foresail taken in, helm a-lee."
    ]
    sails = world.ship.sails
    assert not sails["fore.sail"].is_set and sails["main.sail"].is_set
    assert sails["fore.topsail"].is_set and not sails["fore.course"].is_set


def test_truth_9_she_carries_plain_sail_in_twenty_knots_and_her_light_sails_go_in_thirty_five():
    """Truth 9's two forms on her file (tests/test_known_truths.py, `sail_in_a_wind`: the wind on
    the larboard beam twenty minutes), Neuf-D §16 risk 2 (the most canvas for her weight in the
    game, her lines scaled per mast): under plain sail in 20 kn nothing carries away and no line
    parts, her worst strain her fore topgallant yard's 0.54 of its rating (0.88 in 25 kn, the
    frigate-36's main topgallant yard 1.05); under all sail in 35 kn her light sails and yards go,
    each said urgently: the fore royal mast and the main topmast carried away (measured, seed 7,
    at `clr_x_m` -0.6, the owner's ruling for the lead of 2026-11-08, B2c; at +0.1 before it the
    main topmast and the fore royal yard, the strains the same). Old beside new, her fore
    staysail the working 93 m2 before package 75's B2b corrected it to the triangle that fits
    forward of the fore mast, 46, and her head's rope scaled down with it (1.455 to 1.314): 0.53
    and 0.87; the fore royal mast, the main topgallant mast, the main topmast and the fore
    topgallant yard carried away."""
    from tests.test_known_truths import CARRIED_AWAY, events, sail_in_a_wind

    world = sail_in_a_wind(HER, 20.0, "set plain sail")
    assert [e for e in world.log if e.kind in CARRIED_AWAY] == []
    assert events(world, "line.parted") == []
    world = sail_in_a_wind(HER, 35.0, "make all sail")
    gone = [e for e in world.log if e.kind in CARRIED_AWAY]
    assert gone and all(e.severity.value == "urgent" for e in gone)
    assert any("royal" in e.subject or "topgallant" in e.subject for e in gone)


# ---------------------------------------------------------------------------
# Truth 7-192 (Build-Ships.md §15; Neuf-D §14 truth 1), drafted here for Phase 5
# ---------------------------------------------------------------------------


def test_truth_7_192_the_prince_de_neufchatels_particulars_hold_their_sources():
    """Neuf-D §14 truth 1, a draft for Phase 5 to move into tests/test_known_truths.py. Her file
    loads, `ship.rig` 'hermaphrodite brig'; LWL 32.7 +-0.2 m (107.3 ft between the rabbets,
    ZAZ6177), beam 7.82 +-0.05 m (25 ft 8 in, Winfield 1793-1817 pp. 335-336), draught 3.16 +-0.08
    m (10.36 ft mean to the false keel), 288 +-10 t, lateral area 102 +-5 m2. Her masts 13.3 +-0.3 m
    apart at the deck (43.7 ft, Neuf §2.7), raking 12.4 and 10.3 +-0.7 degrees; four square yards
    on the fore and a boomless gaff sail; a gaff mainsail on a boom of 19.6 +-0.3 m (64.2 ft); the
    fore yard 19.8 +-0.5 m (65 ft). Eleven port triples a side; every gun on one within 0.01 m; her
    lowest sill 1.50 +-0.03 m (4 ft 11 in, task 1's checker confirming it). Her default fit 16 x
    12-pounder carronades and 2 long 6-pounders, 18 pieces, 108 lb by 70's rule; her complement
    130 with a captain and five lieutenants among her posts (Cobb 1841 p. 40); the names
    `american`. Her rig read as Cobb's (p. 38): one mast with yards, not square-rigged, her main a
    schooner's. Her description in her file: 'hermaphrodite brig', 'a brig' at a distance, the
    role `privateer`, her default fit; size rank 2. The index clause (her road's step 6):
    `description('hermaphrodite brig')` gives her file and those words, and 'a hermaphrodite brig'
    names her. Arithmetic on her file alone (`load_spec`, `file_descriptions`, `description`,
    `far_ship`), the same on every machine; none of it moved with her road's step 5, whose knobs
    were her hull speed (12.9 kept), her clr (+0.3 to +0.1, for her helm) and her GM (2.1 kept,
    within 2.0-2.2)."""
    ship = load_ship(HER)
    spec = ship.spec
    hull = spec.hull
    assert spec.rig == "hermaphrodite brig"
    assert abs(hull.length_waterline_m - 32.7) <= 0.2
    assert abs(hull.beam_m - 7.82) <= 0.05
    assert abs(hull.draught_m - 3.16) <= 0.08
    assert abs(hull.displacement_kg - 288000.0) <= 10000.0
    assert abs(hull.lateral_area_m2 - 102.0) <= 5.0
    spars = {s.id: s for s in spec.spars}
    fore, main = spars["fore.mast"], spars["main.mast"]
    assert abs((fore.x_m - main.x_m) - 13.3) <= 0.3
    assert abs(main.rake_deg - 12.4) <= 0.7 and abs(fore.rake_deg - 10.3) <= 0.7
    fore_yards = [y.id for y in scripts.working_yards(ship) if ship.mast_of(y).id == "fore.mast"]
    assert len(fore_yards) == 4
    fg = ship.sails["fore.sail"]
    assert fg.cls == "gaff" and "boom" not in fg.roles
    ms = ship.sails["main.sail"]
    assert ms.cls == "gaff" and ms.roles["boom"] == "main.boom"
    assert abs(ship.spars["main.boom"].length_m - 19.6) <= 0.3
    assert abs(ship.spars["fore.yard"].length_m - 19.8) <= 0.5
    triples = ports_of(hull.profile, "upper")
    assert len(triples) == 11
    fit = spec.armament.fits[spec.armament.default]
    for g in fit.guns:
        assert any(
            abs(g.x_m - x) <= 0.01 and abs(g.height_m - z) <= 0.01 for x, z, _hb in triples
        ), g.id
    assert abs(min(z for _x, z, _hb in triples) - 1.50) <= 0.03
    assert spec.armament.default == FIT
    assert guns_by(fit) == {
        ("carronade", 12, "broadside", "upper"): 16,
        ("long", 6, "bow", "upper"): 2,
    }
    assert far_ship(HER, "united-states").broadside_lb == 108.0
    crew = spec.crew
    assert crew.complement == 130 and crew.names == "american"
    posts = [p.post for p in crew.posts]
    assert "captain" in posts and sum(1 for p in posts if p.endswith(" lieutenant")) == 5
    assert [m.id for m in scripts._masts_with_yards(ship)] == ["fore.mast"]
    assert _square_rigged(ship) is False
    assert [pid for pid in ship.parts if ship.on_schooner_mast(pid)] == [
        "main.topsail.yard",
        "main.topgallant.yard",
        "main.topgallant",
    ]
    own = S.file_descriptions(HER)["hermaphrodite brig"]
    assert (own["rig"], own["roles"], own["fit"]) == ("a brig", ["privateer"], FIT)
    assert C.SIZE_RANK["hermaphrodite brig"] == 2
    # the index clause (her road's step 6)
    d = S.description("hermaphrodite brig")
    assert (d["file"], d["rig"], d["what"]) == (HER, "a brig", own["what"])
    assert S.description_key("a hermaphrodite brig") == "hermaphrodite brig"
