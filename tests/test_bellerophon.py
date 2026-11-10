"""Package 75, the fourth ship (B7): HMS Bellerophon, the Arrogant-class 74 of 1786.

Her design is docs/design/Design-Ship-Bellerophon.md (Bel-D), from the research note
docs/design/Research-74-2026-10.md (Bel); `tools/ships/bellerophon.py` writes her one file,
`data/ships/seventy-four.yaml` (Bel-D decision 1). These are her tests (Bel-D §14; Build-Ships.md
§14.1), begun at her road's steps 2 and 3 (Bel-D §13) in the band form of
tests/test_ship_particulars.py with the source of each band in a comment: her hull at her own
water, the Channel line; her sills and her measured port triples against the drawn side; the
marks of her shape; her spars against Lavery's Table 10 and her sails against Steel's table IV, the
74 column; her mizen course and her driver; every group the engine reads by name; her polar; the
driver's shift and back; her three fits, their patterns, crews and magazines (her step 4); her
company, her marines, her quarter bill with the marines it keeps and her flag party, against the
590 column and her people file; the beat to quarters at muster on each fit, before her bill by
deck reads the bill's marines; her ground tackle, boats, pumps, hold and stores; her description,
its words and its rank; and the generator's report. Her road's step 5 adds her helm and her
handling as tuned (Bel-D §9), her sailed checks against the Vanguard's log and the Bellona's
reports, truth 7-194, a cruiser and a King's frigate meeting her, her round trip under her rules
captain and her checkpoint at quarters; step 6 her bill by deck (B7.b, Bel-D §6.4, with §12.5's
checks on every armed file) and truths 7-195 and 7-196; step 7 her tack at quarters (B7.c, Bel-D
§6.7), with the 64's and the brig's.

The figures quoted as measured were measured at seed 7 on the owner's machine (Windows 11,
2026-11-10); the bands are the sources' or judgement where they say so.
"""

from __future__ import annotations

import math
import random
import subprocess
import sys
from collections import Counter
from pathlib import Path

import pytest

from freesail import orders, units
from freesail.evolutions import Runner, scripts
from freesail.physics.wind import Wind, WindParams
from freesail.ship import form
from freesail.ship.loader import load_ship, load_spec
from freesail.ship.parts import SailState
from freesail.ship.profile import half_breadth_at_sill, interp, ports_of

ROOT = Path(__file__).resolve().parents[1]
SEVENTY_FOUR = "data/ships/seventy-four.yaml"
SIXTY_FOUR = "data/ships/sixty-four.yaml"
FRIGATE = "data/ships/frigate-36.yaml"
RAZEE = "data/ships/razee-44.yaml"
FT = units.FOOT
SQ_FT = FT * FT
# her water, the Channel line, above WL1 (Bel-D §2.2): the lowest lower-deck sill, L7, 5.44 ft
# above WL1 (measured, two readers: Bel §3.1), stands the Bellona's reported 5 ft 2 in (Lavery 1985
# p. 9, Table 2)
CHANNEL_FT = 5.44 - 62.0 / 12.0
MIDSHIPS_FT = 84.0  # the file's x = 0: half her 168 ft between the perpendiculars


@pytest.fixture(scope="module")
def her():
    return load_ship(SEVENTY_FOUR)


def x_of(ft_from_ap):
    """Feet forward of AP as her file's x: metres forward of the mid-perpendicular."""
    return (ft_from_ap - MIDSHIPS_FT) * FT


def above_wl1_ft(z_m):
    """A height in her file (metres above her water) as feet above WL1, the drawings' frame."""
    return z_m / FT + CHANNEL_FT


def area_of(ship, group):
    return sum(ship.sails[i].area_m2 for i in ship.groups[group])


# ---------------------------------------------------------------------------
# Her hull at the Channel line (Bel-D §2)
# ---------------------------------------------------------------------------


def test_her_hull_is_the_arrogant_class_74_at_her_channel_line(her):
    h = her.hull.spec
    # 168 ft between the perpendiculars (ZAZ1357's table, read; 167.97 measured: Bel §3.2.1)
    assert 167.5 <= units.m_to_feet(h.length_waterline_m) <= 168.5
    # 46 ft 9 in extreme, the Arrogants' contract (ZAZ1357's table and ZAZ1070, read; answer 4)
    assert h.beam_m == pytest.approx((46.0 + 9.0 / 12.0) * FT, abs=0.01)
    # 21 ft 2 1/2 in mean to K at the Channel line: WL1's 20.93 ft (measured) and the line's
    # 0.27 ft (Bel-D §2.2)
    assert units.m_to_feet(h.draught_m) == pytest.approx(20.93 + CHANNEL_FT, abs=0.05)
    # Bel's H1 band, 2,490-2,900 t (Bel-D §1.5's check), at the drawn lines' 2,568-2,638 t at her
    # line (Bel §3.2.5 with the slice to the Channel line: Bel-D §2.1)
    assert 2_568_000 <= h.displacement_kg <= 2_638_000
    # the Bombay Castle's 4 ft 5 7/10 in, a Slade 74 of like size (Steel 1805 p. 141; Bel §3.2.5)
    assert h.gm_m == pytest.approx((4.0 + 5.7 / 12.0) * FT, abs=0.01)
    # 3,503 sq ft below WL1 to K (measured, Bel §3.2.6) and the slice to the line, the rudder out
    assert 3_503 <= h.lateral_area_m2 / SQ_FT <= 3_503 + 0.5 * 168.0 + 10.0
    # her rudder, 104.8 sq ft below WL1 (measured, Bel §3.2.6) and the slice over its breadth
    assert 104.8 <= h.rudder.area_m2 / SQ_FT <= 106.5
    # the datum, D18 (a): her upper deck at the middle, 10.37 ft above her water (measured, the
    # mean of its drawn top and middle lines, 10.77 and 10.52 ft above WL1: Bel §3.3)
    assert h.deck_height_m == pytest.approx((10.645 - CHANNEL_FT) * FT, abs=0.01)


# ---------------------------------------------------------------------------
# Her profile: the sills, the decks and the measured triples (Bel-D §3)
# ---------------------------------------------------------------------------


def sills_ft(profile, word):
    return [above_wl1_ft(z) for _x, z, _hb in ports_of(profile, word)]


def test_her_profile_holds_her_measured_sills_and_decks(her):
    p = her.hull.spec.profile
    # the lower deck's fourteen a side, centres and sills measured on ZAZ1357 (both readers, the
    # checker's boxes: Bel §3.1, §3.3): 6.74 ft above WL1 at the aftmost, 5.44 at the seventh, the
    # lowest, 7.13 forward; Dragon's gun-deck plan (1361F) puts L7-L9 within 0.1 ft
    lower = sills_ft(p, "lower")
    assert len(lower) == 14
    assert min(lower) == pytest.approx(5.44, abs=0.03) == lower[6]
    assert lower[0] == pytest.approx(6.74, abs=0.03)
    assert lower[-1] == pytest.approx(7.13, abs=0.03)
    assert all(a > b for a, b in zip(lower[:6], lower[1:7], strict=True))  # the sheer aft
    assert all(a < b for a, b in zip(lower[7:-1], lower[8:], strict=True))  # and forward
    # the upper deck's fourteen, the red altered places as fitted (Bel §3.3): 13.50 ft aft, 11.95
    # the lowest, at the eighth, 13.67 forward; the quarterdeck's seven, 20.16 to 18.66 ft
    upper, qd = sills_ft(p, "upper"), sills_ft(p, "quarterdeck")
    assert len(upper) == 14 and len(qd) == 7
    assert min(upper) == pytest.approx(11.95, abs=0.03) == upper[7]
    assert upper[0] == pytest.approx(13.50, abs=0.03)
    assert upper[-1] == pytest.approx(13.67, abs=0.03)
    assert qd[0] == pytest.approx(20.16, abs=0.03) and qd[-1] == pytest.approx(18.66, abs=0.03)
    assert all(a > b for a, b in zip(qd, qd[1:], strict=False))  # the quarterdeck falls forward
    # the forecastle's two ports on Dragon's plan (1363F, about 139 and 153 ft) and the carronade's
    # place before the belfry; the poop's three places over its rail (Bel-D §3.3)
    assert len(ports_of(p, "forecastle")) == 3 and len(ports_of(p, "roundhouse")) == 3
    # every sill stands above its deck at its port
    decks = dict(p.decks_m)
    for word, triples in p.ports_m:
        for x, z, _hb in triples:
            assert z > interp(decks[word], x), (word, x)
    # her upper deck at the middle is the datum, the uppermost continuous deck (D18 (a))
    assert interp(decks["upper"], 0.0) == pytest.approx(her.hull.spec.deck_height_m)
    # her lower ports 3 ft 4 3/4 in by 2 ft 8 1/2 in (measured, Bel §3.3)
    size = dict(p.port_size_m)["lower"]
    assert size == pytest.approx(((3.0 + 4.75 / 12.0) * FT, (2.0 + 8.5 / 12.0) * FT), abs=0.01)


def test_her_lowest_sill_stands_the_bellonas_clearance_at_her_measured_breadth(her):
    """Bel-D §1.5's check, raised by her module before her file is written: the lowest lower-deck
    sill 1.57 ± 0.01 m above her water (5 ft 2 in, Lavery 1985 p. 9, Table 2) and the side at it
    within 0.03 m of 7.04 m (the body plan traced at the port's station, task 4)."""
    p = her.hull.spec.profile
    x, z, hb = min(ports_of(p, "lower"), key=lambda t: t[1])
    assert z == pytest.approx(1.57, abs=0.01)
    assert hb == pytest.approx(7.04, abs=0.03)
    assert x == pytest.approx(x_of(76.95), abs=0.01)
    # the side at the midship sill, 7.05 m (measured since the review's re-trace of 2026-11-10,
    # the dead flat on its own line; 7.03 before it)
    assert half_breadth_at_sill(p, "lower", 0.0) == pytest.approx(7.05, abs=0.02)


# Her ports measured on the traced body plan at their own stations (task 4: the sections traced
# at the frame stations from 14.85 to 156.46 ft): every lower and upper port but the aftmost of
# each, whose station lies abaft the traced sections and is carried (judgement).
MEASURED_FROM = {"lower": 1, "upper": 1}


def test_her_measured_port_triples_stand_within_5_cm_of_the_drawn_side():
    """Bel-D §13 step 2: each measured triple within 0.05 m of the side `form.py` draws at its
    sill (the generator asserts it and raises; her drawing's 26). The others are reported and
    never moved to the drawing (Build-Ships.md §5.0 principle 8): the worst the quarterdeck's at
    -0.18 m and the aftmost upper and quarterdeck ports at -0.14, taken toward the stern's outline
    (measured; before the review's mend of 2026-11-10 the poop's aftmost place stood +0.51 m
    inside, its half-breadth carried on past her own stern outline, and this bound was 0.55). Her
    drawn displacement within 2% of the filed (2,556 t against 2,600, measured)."""
    hull = load_spec(SEVENTY_FOUR).hull
    share = form.drawn_displacement_kg(hull) / hull.displacement_kg - 1.0
    assert abs(share) <= 0.02, share
    measured = 0
    gaps = []
    for word, triples in hull.profile.ports_m:
        for i, (x, sill, hb) in enumerate(triples):
            gap = form.half_breadth_at(hull, x, sill) - hb
            gaps.append(gap)
            if word in MEASURED_FROM and i >= MEASURED_FROM[word]:
                assert abs(gap) <= 0.05, (word, i, gap)
                measured += 1
    assert measured == 26
    assert max(abs(gap) for gap in gaps) <= 0.20, (min(gaps), max(gaps))


# The mark on each line of her shape (Build-Ships.md §5.0 principle 4): sourced where the line is
# measured on a held image or read; judged where a rule carries it or a reading is judgement, a
# line taking the word of its weakest point. Old beside new (the review, 2026-11-10): rail_m,
# breadth_line_m and sections_m sourced to judged (the gallery's straight run and the poop's rail
# at its deck; the trace's lowest point; the waterlines carried between Bel's stations), and
# form.fullness written, judged (Bel-D §3.6's table).
SHAPE_MARKS = {
    "sourced": (
        "keel_m", "stern_m", "section_m", "head_m",
        "form.stern", "form.stern.knuckle_z_m", "form.stern.transom_hb_m",
        "form.stern.round_up_m", "form.stern.galleries_m", "form.head",
    ),
    "judged": (
        "rail_m", "breadth_m", "stem_m", "wales_m", "decks_m", "ports_m", "port_size_m",
        "breadth_line_m", "sections_m", "channel_wales_m", "form.fullness", "form.stern.lights_m",
    ),
}  # fmt: skip


def test_every_line_of_her_shape_carries_its_rung():
    p = load_spec(SEVENTY_FOUR).hull.profile
    lines = [
        key
        for key in (
            "rail_m", "breadth_m", "keel_m", "stem_m", "stern_m", "wales_m", "section_m",
            "decks_m", "ports_m", "port_size_m", "head_m", "breadth_line_m", "sections_m",
            "channel_wales_m", "floor_m", "rabbet_m",
        )
        if getattr(p, key)
    ]  # fmt: skip
    assert "floor_m" not in lines and "rabbet_m" not in lines  # reserved, not written
    stern = ["knuckle_z_m", "transom_hb_m", "round_up_m", "galleries_m", "lights_m"]
    given = [
        *lines, "form.fullness", "form.stern", *(f"form.stern.{key}" for key in stern), "form.head"
    ]  # fmt: skip
    marks = dict(p.marks)
    assert list(marks) == given
    assert marks == {key: word for word, keys in SHAPE_MARKS.items() for key in keys}


def test_her_stern_and_head_are_as_measured(her):
    p = her.hull.spec.profile
    # the taffrail's crown 13.05 ft abaft AP and 30.25 ft above WL1 (measured on ZAZ1357, task 1;
    # ZAZ1359's inboard profile draws no crown)
    x, z = p.rail_m[0]
    assert x == pytest.approx(x_of(-13.05), abs=0.01)
    assert above_wl1_ft(z) == pytest.approx(30.25, abs=0.05)
    # the stem proper meets WL1 at 169.02 ft (task 2), its head 170.13 ft and 16.25 ft above
    # WL1 under the bowsprit (ZAZ1359: 170.10 and 16.31); the knee of the head before it
    assert interp([(zz, xx) for xx, zz in p.stem_m], -CHANNEL_FT * FT) == pytest.approx(
        x_of(169.02), abs=0.02
    )
    sx, sz = p.stem_m[-1]
    assert sx == pytest.approx(x_of(170.13), abs=0.02)
    assert above_wl1_ft(sz) == pytest.approx(16.25, abs=0.05)
    assert max(x for x, _z in p.head_m) > sx
    # the counter's knuckle 7.15 ft above WL1 at the middle line (task 1)
    stern = load_spec(SEVENTY_FOUR).hull.profile.form.stern
    assert stern.type == "square"
    assert above_wl1_ft(stern.knuckle_z_m) == pytest.approx(7.15, abs=0.05)


# ---------------------------------------------------------------------------
# Her spars (Lavery 1985 Table 10, her class's list; Steel's column for the rest: Bel-D §4)
# ---------------------------------------------------------------------------

# feet: the yards of each mast, course (the mizzen's the cross-jack), topsail, topgallant, royal;
# Table 10's to the topgallants (the mizen topgallant Steel's 31 ft 6 in), the royals Steel's
TABLE_10_YARDS_FT = {
    "fore": (84.0 + 4.0 / 12.0, 61.5, 40.0, 31.0),
    "main": (96.0 + 8.0 / 12.0, 70.5, 45.0 + 10.0 / 12.0, 35.0),
    "mizzen": (61.5, 46.0 + 1.0 / 12.0, 31.5, 23.0),
}


def test_her_spars_follow_her_class_list(her):
    sp = her.spars
    for mast, lengths in TABLE_10_YARDS_FT.items():
        course = "mizzen.crossjack.yard" if mast == "mizzen" else f"{mast}.yard"
        ids = (course, f"{mast}.topsail.yard", f"{mast}.topgallant.yard", f"{mast}.royal.yard")
        for yard_id, ft in zip(ids, lengths, strict=True):
            assert sp[yard_id].length_m == pytest.approx(ft * FT, abs=0.06), yard_id
    # the mizen yard 86 ft 6 in, the spritsail yard 61 ft 6 in and the sprit topsail yard 40 ft
    # (Table 10: Bel-D §4.3, her class's list before Steel's column)
    assert sp["mizzen.yard"].length_m == pytest.approx(86.5 * FT, abs=0.06)
    assert sp["spritsail.yard"].length_m == pytest.approx(61.5 * FT, abs=0.06)
    assert sp["sprit_topsail.yard"].length_m == pytest.approx(40.0 * FT, abs=0.06)
    # the bowsprit 66 ft, its heel measured at 155.4 ft and its steeve at 31.6 deg on ZAZ1357 and
    # ZAZ1359 (task 7): 48.7 ft outboard of the stem head; the jib-boom 48 ft, seven twelfths out
    assert units.m_to_feet(sp["bowsprit"].length_m) == pytest.approx(48.7, abs=0.3)
    assert sp["jib_boom"].length_m == pytest.approx(48.0 * 7.0 / 12.0 * FT, abs=0.06)
    # the main topmast 64 ft 10 in, its hoist above the cap the length less the lower mast head of
    # five inches to every yard of the 108-ft mast (Steel, OCR l. 4697-4699): 49 ft 10 in
    hoist_ft = 64.0 + 10.0 / 12.0 - 108.0 / 3.0 * 5.0 / 12.0
    assert sp["main.topmast"].height_m == pytest.approx(hoist_ft * FT, abs=0.06)
    # the driver's boom her main topsail yard's 70 ft 6 in (Steel 1794 vol. I p. 40)
    assert sp["mizzen.boom"].length_m == pytest.approx(70.5 * FT, abs=0.06)
    # the main truck on Steel's long pole-heads (Steel p. 42), 56.8 m above her water (measured)
    truck = sum(s.height_m for s in her.spar_chain("main.royal_mast"))
    assert truck + her.hull.spec.deck_height_m == pytest.approx(56.8, abs=0.2)
    # her brace limits are the frigate-36's (Fincham 1843 art. 102), the owner's for the 64
    # (2026-10-29); her lee lower shrouds do not stop her lower yards before 67 degrees (task 10)
    frigate = load_ship(FRIGATE)
    for yard_id in ("fore.yard", "main.yard", "main.topsail.yard", "mizzen.topsail.yard"):
        assert sp[yard_id].brace_limit == frigate.spars[yard_id].brace_limit, yard_id
    assert math.degrees(sp["mizzen.crossjack.yard"].brace_limit) == pytest.approx(60.0)


# ---------------------------------------------------------------------------
# Her sails (Steel's table IV, the 74 column: Bel §5.6; Bel-D §4.4-§4.8)
# ---------------------------------------------------------------------------

CLOTH_FT = 22.5 / 12.0  # 22 1/2 in a cloth in the sail (Ind §5, judgement)
STEEL_SQUARE = {
    "main.course": (46.0, 48.0, 15.75),
    "fore.course": (40.0, 38.0, 13.0),
    "main.topsail": (30.0, 47.0, 19.75),
    "fore.topsail": (26.0, 41.0, 17.5),
    "mizzen.topsail": (20.5, 30.0, 13.875),
}
STEEL_ABOVE_THE_CAPS = {
    "main.topgallant": (21.5, 30.5, 10.0),
    "fore.topgallant": (18.5, 26.5, 8.75),
    "mizzen.topgallant": (15.0, 21.0, 7.25),
    "main.royal": (17.0, 22.0, 7.5),
    "fore.royal": (15.0, 19.0, 6.75),
    "mizzen.royal": (11.0, 15.0, 5.5),
}
# the headsails: cloths in the foot and the leech in yards
STEEL_HEADSAILS = {"fore.staysail": (22.0, 13.0), "fore.topmast_staysail": (21.0, 17.5),
                   "jib": (26.0, 25.0)}  # fmt: skip
# the staysails between the masts by Steel's rule for the canvas, m2, with Bel-D §4.4's band
STEEL_BETWEEN = {
    "main.staysail": (128.0, 0.10),
    "main.topmast_staysail": (228.0, 0.25),
    "middle_staysail": (150.0, 0.25),
    "main.topgallant_staysail": (118.0, 0.25),
    "mizzen.staysail": (126.0, 0.25),
    "mizzen.topmast_staysail": (107.0, 0.25),
}


def steel_m2(head, foot, depth_yd):
    return (head + foot) / 2.0 * CLOTH_FT * depth_yd * 3.0 * SQ_FT


def test_her_sails_follow_steels_table_iv_the_74_column(her):
    areas = {s.id: s.area_m2 for s in her.sails.values()}
    for sid, row in STEEL_SQUARE.items():  # the courses and topsails, ±10%, unscaled (Bel-D §4.4)
        assert abs(areas[sid] / steel_m2(*row) - 1.0) <= 0.10, sid
    for sid, (foot, leech) in STEEL_HEADSAILS.items():  # triangles on their stays, ±10%
        assert abs(areas[sid] / (foot * CLOTH_FT * leech * 3.0 / 2.0 * SQ_FT) - 1.0) <= 0.10, sid
    # above the topmast caps the spars rule over the table (Build-Ships.md §19.1 item 5), on
    # Steel p. 42's long pole-heads: 0.88-0.93 of the table's (measured)
    for sid, row in STEEL_ABOVE_THE_CAPS.items():
        assert 0.85 <= areas[sid] / steel_m2(*row) <= 0.95, sid
    for sid, (m2, band) in STEEL_BETWEEN.items():
        assert abs(areas[sid] / m2 - 1.0) <= band, sid
    assert "mizzen.topgallant_staysail" not in areas  # Steel's 74 has none
    # the main topsail the largest sail, as the frigate-36's and the 64's
    assert max(areas, key=areas.get) == "main.topsail"
    # plain sail 2,225 m2 (measured; Bel-D §4.3's 2,226), above the 64's
    assert 2_150 <= area_of(her, "plain sail") <= 2_300
    assert area_of(her, "plain sail") > area_of(load_ship(SIXTY_FOUR), "plain sail")


def test_her_mizen_course_is_cut_at_the_mast_on_her_mizen_yard(her):
    """Bel-D §4.5 (Ext §3.4): Steel's mizen course, 16 cloths at the head and 17 at the foot, its
    leeches 11 and 21 yards, cut at the mast on her lateen yard; its tack 9 ft above her poop's
    middle line at the mast (task 5: the poop measured running over the mizen to 36.75 ft from AP,
    Lavery I32's deck the poop; the lead's to rule), its foot 2.32 m over that line (measured)."""
    course = her.sails["mizzen.course"]
    steel = 16.5 * CLOTH_FT * (11.0 + 21.0) / 2.0 * 3.0 * SQ_FT
    assert abs(course.area_m2 / steel - 1.0) <= 0.10
    assert course.cls == "lateen" and her.spars["mizzen.yard"].cls == "lateen_yard"
    assert course.state is SailState.FURLED


def test_her_driver_is_steels_in_the_courses_place_and_in_the_sail_room(her):
    """Bel-D §4.6 (Ext §17): Steel's driver boomsail, 25 1/2 cloths at the head and 32 1/2 at the
    foot, its leeches 11 and 24 yards (265.2 m2), on her boom of 70 ft 6 in, its jaws 12.30 m
    above her water at 6 ft of head room over her poop (the lead's answer (13): 6 ft first), set
    by its after leech (measured); unbent, its boom in, the course bent."""
    driver = her.sails["mizzen.driver"]
    steel = 29.0 * CLOTH_FT * (11.0 + 24.0) / 2.0 * 3.0 * SQ_FT
    assert abs(driver.area_m2 / steel - 1.0) <= 0.05
    assert driver.state is SailState.UNBENT
    assert her.spars["mizzen.boom"].rigged_out is False
    assert driver.id in her.groups["occasional sails"]
    # a boom's jaws above the course's tack, so that it swings over the poop's people
    assert her.spars["mizzen.boom"].height_m + her.hull.spec.deck_height_m > 12.2


# ---------------------------------------------------------------------------
# Her groups (Bel-D §4.8)
# ---------------------------------------------------------------------------

# the groups the engine reads by name (`groups.get("...")` and `groups["..."]` in freesail/:
# orders/storm.py, evolutions/scripts.py, world/captains.py, world/ships.py), the vocabulary's
# "make all sail" and "shorten sail", the sail room's and the agents' plans
READ_BY_NAME = (
    "plain sail", "courses", "topsails", "headsails", "jibs", "staysails", "storm canvas",
    "storm staysails", "lying-to staysails", "topgallants", "royals", "occasional sails",
    "all sail",
)  # fmt: skip


def test_every_group_the_engine_reads_by_name_is_hers(her):
    for name in READ_BY_NAME:
        assert her.groups.get(name), name
    # the 64's groups, name for name: a ship of the same rig and the same canvas (Bel-D §4.8)
    assert set(her.groups) == set(load_ship(SIXTY_FOUR).groups)
    assert her.groups["courses"] == ["fore.course", "main.course"]
    assert her.groups["lying-to staysails"] == ["main.staysail"]
    assert her.groups["storm staysails"] == ["fore.storm_staysail", "mizzen.storm_staysail"]
    assert "mizzen.course" in her.groups["plain sail"]
    assert "mizzen.driver" not in her.groups["plain sail"]


# ---------------------------------------------------------------------------
# Her polar (Bel-D §9): measured and recorded, no truth
# ---------------------------------------------------------------------------


def test_her_polar_is_drawn_from_her_file_and_agrees_with_her_sailed_beam_reach():
    """`polar_of` on her file as tuned at her step 5 (Bel-D §9; docs/dev/TuningNotes.md, the knobs
    beside their starts and bounds): 4.50, 7.87 and 11.03 kn her best in 8, 15 and 25 kn, at 90,
    90 and 100 deg; closest at 50 deg; `beat_deg` 70, 70 and 60 in 8, 15 and 25 kn (measured).
    Beside her: the 64's 4.29, 7.64 and 11.00 (beat 70 in 15 kn), the razee's 4.46, 8.02 and 11.64
    and the frigate-36's 4.62, 8.19 and 11.63 (both beat 60). `hull_speed_kn` kept at 12.0 within
    11.5-13.0 (11.5 gives 10.83 in 25 kn, 12.5 11.22, 13.0 11.40); `clr_x_m`, moved for her helm,
    does not reach the polar. Under plain sail with the yards trimmed she sails 7.74 kn at 90 deg in
    15 kn (measured, seed 7; 7.75 at the tuned `clr_x_m`). Bel-D §9's bands: her best in 25 kn
    within 10.5-12, the owner's "about 11" (answer 14; Lavery p. 9, Table 2) and below the
    frigate-36's; 7-8.5 kn at 90 deg in 15 kn (Bel E1); her closest within a step of the frigate's
    while her brace limits are the frigate's. Her beat in 15 kn is 70 by a hair (2.035 kn made good
    at 70 against 2.030 at 60): recorded, not forced. The close-hauled gap against the Bellona's
    reports (9 kn, often 10, close-hauled in a topgallant gale: Lavery p. 9) is the physics' (the
    lead's answer (12)): her 6.64 kn at 60 deg in 25 kn."""
    from freesail.world import ships as S

    p, frigate = S.polar_of(SEVENTY_FOUR), S.polar_of(FRIGATE)
    assert abs(p.speed_kn(90.0, 15.0) - 7.74) <= 0.5
    assert 7.0 <= p.speed_kn(90.0, 15.0) <= 8.5
    best_25 = max(p.speeds_kn[p.winds_kn.index(25.0)])
    assert 10.5 <= best_25 <= 12.0
    assert best_25 < max(frigate.speeds_kn[frigate.winds_kn.index(25.0)])
    assert p.speed_kn(90.0, 8.0) < p.speed_kn(90.0, 15.0) < p.speed_kn(90.0, 25.0)
    assert abs(p.closest_deg - frigate.closest_deg) <= 10.0


# ---------------------------------------------------------------------------
# The driver's shift and back on her file (Bel-D §13 step 3; Ext §17.3, §17.7, §17.11)
# ---------------------------------------------------------------------------

LIGHT_AIRS = Wind(WindParams.from_nautical(0.0, 3.0, 0.0, 0.0), random.Random(0))
# shift_sail.yaml's, the boom's two the shift script's own (Ext §17.11: 120 s, judgement)
SHIFT_S = {"take_in": 90, "unbend": 180, "send_up": 150, "bend": 240, "set": 120}
RIG_BOOM_S = 120


def _run(runner, ship, max_ticks=3000):
    """Tick the runner (no physics) until nothing is in hand: the ticks and the notes."""
    ticks, notes = 0, []
    while runner.in_progress() and ticks < max_ticks:
        runner.step(ship, 1.0, LIGHT_AIRS)
        notes.extend(ship.drain_notes())
        ticks += 1
    assert not runner.in_progress(), f"still at work after {max_ticks} ticks"
    return ticks, notes


@pytest.mark.parametrize("drawing", [True, False], ids=["drawing", "furled"])
def test_she_shifts_her_mizen_for_the_driver_and_back_each_to_its_end(drawing):
    """The order "shift the mizen for the driver" and back on `seventy-four.yaml`, as on the 64's:
    a drawing course taken in, unbent, sent down while the driver is swayed up, the boom rigged
    out, the driver bent and set, 900 s at the file's times with no company aboard; a furled one
    shifted where it hangs in 690 s, the driver left furled. Back, the boom comes in after the
    unbend. The boom stands out only while the driver is bent; the count of spares stands (her
    sail room since her step 4, the driver's spare among its occasional sails)."""
    ship = load_ship(SEVENTY_FOUR)
    runner = Runner(ship)
    ship.dyn.apparent_wind_angle = math.radians(-30.0)
    ship.dyn.apparent_wind_speed = 6.0
    course, driver = ship.sails["mizzen.course"], ship.sails["mizzen.driver"]
    boom = ship.spars["mizzen.boom"]
    spares = scripts.spare_sails(ship)
    assert driver.state is SailState.UNBENT and course.state is SailState.FURLED
    if drawing:
        course.state = SailState.SET
    phases = list(SHIFT_S) if drawing else ["unbend", "send_up", "bend"]
    for text, old, new, out in (
        ("shift the mizen for the driver", course, driver, True),
        ("shift the driver for the mizen", driver, course, False),
    ):
        _kind, _words, data = orders.handle(ship, text)
        assert [(e["evolution"], e["subject"]) for e in data["evolutions"]] == [
            ("shift_sail", old.id)
        ]
        ticks, notes = _run(runner, ship)
        assert ticks == sum(SHIFT_S[p] for p in phases) + RIG_BOOM_S, text
        assert boom.rigged_out is out, text
        assert any(f"Rigged {'out' if out else 'in'} the " in n for n in map(str, notes)), notes
        assert old.state is SailState.UNBENT
        assert new.state is (SailState.SET if drawing else SailState.FURLED)
        assert scripts.spare_sails(ship) == spares
        assert ship.sails["storm_mizzen"].state is SailState.UNBENT


# ---------------------------------------------------------------------------
# Her guns (Bel-D §5)
# ---------------------------------------------------------------------------

FIT_1793, FIT_1795, FIT_1812 = "arrogant class 1793", "arrogant class 1795", "as the bellona 1812"
CWT_KG = 50.80234544  # the hundredweight of 112 lb
# her places from forward, by deck, numbered on across her decks (Bel-D §5.2)
NUMBERS = {
    "lower": range(1, 15),
    "upper": range(15, 29),
    "quarterdeck": range(29, 36),
    "forecastle": range(36, 39),
    "roundhouse": range(39, 42),
}


def _guns(fit):
    return load_spec(SEVENTY_FOUR).armament.fits[fit].guns


def _pieces(fit):
    """(deck, kind, pounder, cwt, crew) -> pieces, a pair's two guns each counted."""
    return Counter((g.deck, g.kind, int(g.pounder), g.weight_cwt, g.crew) for g in _guns(fit))


def test_her_three_fits_hold_their_sources_pieces_and_broadsides():
    """Bel-D §5.1, §5.5: 74, 82 and 78 pieces, the default the owner's 1795-1805 (answer 3); the
    broadside by 70's rule (one side's broadside guns and every chaser, combat/far.py) 781 and 867
    lb, James's (vol. 1, Abstracts No. 1 and 3), and 938 lb on the Bellona's list of 1812 (Lavery
    1985 p. 22, Table 19); none of them a chaser (no chase port is drawn: Bel §3.4)."""
    from freesail.combat.far import far_ship

    arm = load_spec(SEVENTY_FOUR).armament
    assert list(arm.fits) == [FIT_1793, FIT_1795, FIT_1812] and arm.default == FIT_1795
    for fit, pieces, lb in ((FIT_1793, 74, 781.0), (FIT_1795, 82, 867.0), (FIT_1812, 78, 938.0)):
        guns = arm.fits[fit].guns
        assert len(guns) == pieces, fit
        assert all(g.place == "broadside" for g in guns), fit
        assert far_ship(SEVENTY_FOUR, "britain", fit=fit).broadside_lb == lb, fit
    # against the frigate-36's 421 lb as the owner keeps her quarterdeck (Bel-D §5.5)
    frigate = far_ship(FRIGATE, "britain").broadside_lb
    assert round(867.0 / frigate, 2) == 2.06


def test_every_gun_stands_on_its_decks_triple_numbered_on_across_her_decks():
    """Bel-D §5.2: each gun on its port's triple, or its place over the rail, to the centimetre,
    its deck named (Build-Ships.md §4.4); numbered from forward and on across her decks, the lower
    deck first (lower 1-14, upper 15-28, quarterdeck 29-35, the forecastle's ports 36-37 and the
    1795 carronade's place 38, the poop 39-41), a place keeping its number in every fit. The lower
    deck's lowest port, L7 at x -2.15 m, carries her pair No. 8 (7-195's port)."""
    profile = load_spec(SEVENTY_FOUR).hull.profile
    places = {}
    for fit in (FIT_1793, FIT_1795, FIT_1812):
        for g in _guns(fit):
            triples = {(round(t[0], 2), round(t[1], 2)) for t in ports_of(profile, g.deck)}
            assert (g.x_m, g.height_m) in triples, (fit, g.id)
            assert g.number in NUMBERS[g.deck], (fit, g.id)
            assert places.setdefault((g.deck, g.number), g.x_m) == g.x_m, (fit, g.id)
            assert g.id == f"gun.{g.number}.{g.side}"
    for deck, numbers in NUMBERS.items():
        xs = [places[(deck, n)] for n in numbers if (deck, n) in places]
        assert xs == sorted(xs, reverse=True), deck  # from forward
    lowest = min(ports_of(profile, "lower"), key=lambda t: t[1])
    assert lowest[0] == pytest.approx(-2.15, abs=0.005) and places[("lower", 8)] == lowest[0]
    # every place filled in some fit; the 1812 fit leaves the 1795 carronade's place and the poop's
    # aftmost empty
    assert set(places) == {(d, n) for d, ns in NUMBERS.items() for n in ns}
    empty = {(g.deck, g.number) for g in _guns(FIT_1812)} ^ set(places)
    assert empty == {("forecastle", 38), ("roundhouse", 41)}


def test_her_pieces_take_their_patterns_weights_and_the_periods_crews():
    """Bel-D §5.3 (answer 12): a piece takes its pattern's weight, Adye's where Adye gives one
    (1804 pp. 72, 155), else Lavery's Table 17 for its date (1985 p. 21), never the founders'
    scatter; crews by Falconer 1780 (QUARTERS: 13, 9, 7 and 6 to the pair of 32s, 18s, 12s and 9s)
    and Douglas 1829 (art. 136: four to a carronade). One side's guns take 362, 378 and 364 men (Bel
    §4.5's 378 for the default)."""
    long32 = ("lower", "long", 32, 55.0, 13)
    assert _pieces(FIT_1793) == {
        long32: 28,
        ("upper", "long", 18, 40.0, 9): 28,
        ("quarterdeck", "long", 9, 24.5, 6): 14,
        ("forecastle", "long", 9, 27.5, 6): 4,  # the Bellona's 8 ft 6 in nines (Table 18)
    }
    assert _pieces(FIT_1795) == _pieces(FIT_1793) + Counter(
        {
            ("forecastle", "carronade", 32, 17.125, 4): 2,  # 17 cwt 0 qr 14 lb (Adye p. 72)
            ("roundhouse", "carronade", 18, 9.0, 4): 6,
        }
    )
    assert _pieces(FIT_1812) == {
        long32: 28,
        ("upper", "long", 18, 42.0, 9): 28,  # Lavery's type of 1812, which Adye lacks
        ("quarterdeck", "long", 12, 29.0, 7): 6,  # 7 ft 6 in (Table 17, 1812)
        ("quarterdeck", "carronade", 32, 17.125, 4): 8,
        ("forecastle", "carronade", 32, 17.125, 4): 2,
        ("forecastle", "long", 12, 34.0, 7): 2,  # 9 ft (Table 17, 1812)
        ("roundhouse", "carronade", 18, 9.0, 4): 2,
        ("roundhouse", "carronade", 12, 5.84, 4): 2,  # Adye's 2 ft 2 in, 5 cwt 3 qr 10 lb
    }
    for fit, men in ((FIT_1793, 362), (FIT_1795, 378), (FIT_1812, 364)):
        assert sum(g.crew for g in _guns(fit) if g.side == "starboard") == men, fit


def test_her_magazines_take_table_29s_charges_and_a_two_deckers_exercise():
    """Bel-D §5.4: the King's allowance a gun (sixty round, six grape, six chain: judgement, as
    every King's file); the charges Table No. 29's through `charge_lb` with no keyword (SW-1: the
    long 32 10 lb 10 oz, where the share gives 10 lb 11 oz; the 18 6 lb, the 12 4 lb, the 9 3 lb;
    the carronades 2 lb 10 oz, 1 lb 8 oz and 1 lb); exercise 9, a third of her upper deck's 28
    (the Regulations 1806, the Gunner, Art. XXI)."""
    table = {
        ("long", 32): 10.625,
        ("long", 18): 6.0,
        ("long", 12): 4.0,
        ("long", 9): 3.0,
        ("carronade", 32): 2.625,
        ("carronade", 18): 1.5,
        ("carronade", 12): 1.0,
    }
    for fit in load_spec(SEVENTY_FOUR).armament.fits.values():
        assert fit.exercise_charges == 9, fit.name
        for (kind, pounder), lb in fit.charges.items():
            assert lb == table[(kind, int(pounder))], (fit.name, kind, pounder)
        counts = Counter(int(g.pounder) for g in fit.guns)
        for pounder, shot in fit.shot.items():
            n = counts[int(pounder)]
            assert shot == {"round": 60 * n, "grape": 6 * n, "chain": 6 * n}, fit.name


def test_the_viewer_draws_every_gun_of_her_three_fits():
    """Build-Ships.md §6's postscript, the ship builder's checklist (package 81): every gun of
    every fit placed by the viewer's one rule and no port off her drawn side
    (`tools/check_viewer_guns.py`); her poop's places over the rail by the side's own test against
    the deck's port size, the quarterdeck's (judgement, as the 64's)."""
    sys.path.insert(0, str(ROOT / "tools"))
    import check_viewer_guns

    assert check_viewer_guns.check(ROOT / SEVENTY_FOUR).ok


# ---------------------------------------------------------------------------
# Her company, her marines, her quarter bill and her flag (Bel-D §6)
# ---------------------------------------------------------------------------

SEAMEN_STATIONS = ("forecastle", "fore_top", "main_top", "mizzen_top", "afterguard", "waisters")


def test_her_company_holds_the_590_column(her):
    """Bel-D §6.1-§6.2 (answers 10 and 11): 590 on the Regulations' table of 31 December 1806
    (1808 printing p. 165, the 590 column, read row by row: Bel §4.3): sixteen posts, five
    lieutenants among them and the column's second master and chaplain; 111 marines, the
    column's eleven officers and NCOs and 100 privates (Naval Chronicle vol. IX p. 245); 44
    idlers by the column's trades; 419 seamen shared as the frigate-36's 182 are (judgement)."""
    c = her.spec.crew
    assert c.complement == 590 and c.stations["marines"] == 111
    assert len(c.posts) == 16 and sum(1 for p in c.posts if p.post.endswith(" lieutenant")) == 5
    assert {"second master", "chaplain"} <= {p.post for p in c.posts}
    assert c.stations["idlers"] == 44 and sum(c.idlers_by_trade.values()) == 44
    assert c.idlers_by_trade["servant"] == 14  # the boys of the third class (James vol. 1 p. 256)
    assert {k: c.stations[k] for k in SEAMEN_STATIONS} == {
        "forecastle": 65,
        "fore_top": 55,
        "main_top": 69,
        "mizzen_top": 32,
        "afterguard": 115,
        "waisters": 83,
    }
    assert len(c.posts) + c.seamen + c.stations["marines"] + c.stations["idlers"] == 590
    assert c.ratings == {"able": 0.3, "ordinary": 0.4, "landsman": 0.3}
    assert [p.role for p in c.people].count("master's mate") == 3
    assert {"captain of marines", "lieutenant of marines"} <= {p.role for p in c.people}


def test_her_ship_files_posts_and_people_agree_with_her_people_file():
    """tests/test_wardroom.py's check (:42-57) on her file (Bel-D §6.8): the generator draws the
    posts and the drawn roles from `data/people/seventy-four.yaml`, and her flag party from its
    entries marked `flag`, in its order."""
    import yaml

    from freesail.world import people as PE

    wardroom = PE.load_wardroom(SEVENTY_FOUR)
    assert wardroom is not None
    spec = load_spec(ROOT / SEVENTY_FOUR)
    assert [p.post for p in spec.crew.posts] == wardroom.posts
    drawn = [
        (o.role, o.drawn["station"], o.drawn.get("rating"), o.messenger) for o in wardroom.drawn
    ]
    assert [(p.role, p.station, p.rating, p.messenger) for p in spec.crew.people] == drawn
    raw = yaml.safe_load((ROOT / "data" / "people" / "seventy-four.yaml").read_text("utf-8"))
    assert raw["ship"] == SEVENTY_FOUR
    assert [p.post for p in spec.crew.flag] == [e["role"] for e in raw["wardroom"] if e.get("flag")]
    assert wardroom.role_of("captain") == "captain"
    assert wardroom.role_of("officer of the watch") == "first lieutenant"


def test_her_posts_draw_at_muster_the_second_master_and_the_chaplain_as_the_others():
    """Bel-D §6.1: the posts are free words (`PostSpec`), so the 590 column's second master and
    chaplain, which the frigate's file lacks, draw at muster as every post does, each given their
    outline, rank and place by her people file; her flag party is not aboard while no flag flies,
    and her muster is her 590."""
    from tests.test_brains import world_at

    w = world_at(49.5, -5.5, SEVENTY_FOUR)
    people = w.people
    for words, rank, where in (
        ("the second master", "second master", "quarterdeck"),
        ("the chaplain", "chaplain", "gunroom"),
        ("the fifth lieutenant", "lieutenant", "quarterdeck"),
    ):
        p = people.find(words)
        assert p is not None and p.outline is not None, words
        assert (p.rank, p.where) == (rank, where), words
    roles = {p.role for p in people.all}
    assert not roles & {"rear-admiral", "flag lieutenant", "admiral's secretary"}
    assert len(people.all) == 16 + 7  # the posts and the drawn roles
    assert w.ship.extra["crew"].complement == 590


def test_her_quarter_bill_is_set_against_the_default_fit_with_its_marines_kept():
    """Bel-D §6.3: on "arrogant class 1795" her 419 seamen less the long guns' 362 and two at the
    wheel leave 55 trimmers, split by the frigate-36's shares (8, 10, 12, 6, 8 of 44); the marines
    take the carronades' 16, and the bill's `marines` (her stage 0c's key) keeps the other 95 in
    their division; filling 18, the 590 column's quarter gunners (Bel-D §5.4); small arms 46 and
    boarders 105, the frigate-36's share and a quarter of the seamen. The bill's and the crew's
    pickled states carry the stage's keys, hers alone of the files."""
    import pickle

    crew = load_spec(SEVENTY_FOUR).crew
    bill = crew.quarter_bill
    assert bill.trimmers == {
        "forecastle": 10,
        "fore_top": 13,
        "main_top": 15,
        "mizzen_top": 7,
        "afterguard": 10,
    }
    assert (bill.helm, bill.powder, bill.filling) == (2, 0, 18)
    assert bill.priority == "sail before guns"
    assert (bill.small_arms, bill.boarders, bill.marines) == (46, 105, 95)
    assert bill.marines <= crew.stations["marines"]
    assert list(bill.__getstate__())[-1] == "marines"
    assert list(crew.__getstate__())[-1] == "flag"
    assert pickle.loads(pickle.dumps(crew)) == crew


def test_her_flag_party_is_the_rear_admirals_beyond_her_company():
    """Bel-D §17.0, the owner's answer, and the lead's answer (15): the rear-admiral, their flag
    lieutenant and secretary, and their servants, fifteen (James's customary supernumeraries for a
    rear-admiral, vol. 1 p. 156; the make-up judgement), in her crew's `flag:` in the posts' form
    (stage 0c's), counted in no station and not in her 590; their places in her people file the
    quarterdeck and the admiral's cabin."""
    from freesail.world import people as PE

    crew = load_spec(SEVENTY_FOUR).crew
    flag = [p.post for p in crew.flag]
    assert len(flag) == 15
    assert flag[:3] == ["rear-admiral", "flag lieutenant", "admiral's secretary"]
    assert flag[3:] == ["admiral's servant"] * 12
    assert all(p.name is None for p in crew.flag)  # a scenario names them
    assert not set(flag) & {p.post for p in crew.posts}
    assert len(crew.posts) + sum(crew.stations.values()) == crew.complement == 590
    outlines = [o for o in PE.load_wardroom(SEVENTY_FOUR).outlines if o.role in set(flag)]
    assert [o.role for o in outlines] == flag
    assert {o.place for o in outlines} == {"quarterdeck", "cabin"}
    assert all(not o.post and not o.drawn for o in outlines)


# ---------------------------------------------------------------------------
# Her ground tackle, boats, pumps, hold and stores (Bel-D §7)
# ---------------------------------------------------------------------------


def test_her_ground_tackle_is_steels_and_laverys_for_a_74(her):
    """Answer 13: four bowers of 67 cwt, a stream of 16 cwt and a kedge of 8 cwt (Steel 1794 vol.
    I, the 'Smaller 74 Guns' column; Lavery 1985 p. 15, Table 4, about 1800), on seven 22-in
    cables of 100 fathoms laid three, two, one and one (Table 4; Lever 1808 p. 67), the stream's
    13 1/2 in (Table 4; Steel's 12 1/2 in the note) and the kedge's hawser half the bower cable."""
    tackle = her.spec.ground_tackle
    assert not tackle.chain
    anchors = {a.id: a for a in tackle.anchors}
    four = ("best_bower", "small_bower", "sheet", "spare_anchor")
    for aid in four:
        assert anchors[aid].weight_kg == pytest.approx(67 * CWT_KG, abs=1.0), aid
        assert anchors[aid].cable_in == 22.0, aid
    assert [anchors[a].kind for a in four] == ["bower", "bower", "sheet", "sheet"]
    assert [anchors[a].cable_fathoms for a in four] == [300.0, 200.0, 100.0, 100.0]
    assert anchors["stream"].weight_kg == pytest.approx(16 * CWT_KG, abs=1.0)
    assert anchors["stream"].cable_in == 13.5
    assert anchors["kedge"].weight_kg == pytest.approx(8 * CWT_KG, abs=1.0)
    assert anchors["kedge"].cable_in == 11.0
    sixty_four = load_ship(SIXTY_FOUR).spec.ground_tackle.anchors
    assert anchors["best_bower"].cable_kn > max(a.cable_kn for a in sixty_four)


def test_her_boats_pumps_hold_and_stores(her):
    """Bel-D §7: Lavery's six boats of about 1800 (1985 p. 16, Table 5: a launch of 31 ft,
    pinnaces of 32 and 28, cutters of 25, 25 and 18), the larger pinnace filed as the barge whose
    work it does (the owner's "with a barge", answer 13), each line by the generator's factors on
    her length; four chain pumps round the main mast (task 9: Dragon's gun deck, 1361F) and two hand
    pumps; her hold a tenth of her 1,604 tons; her stores the frigate-36's carried to 590 (water
    223 t, cordage 1,350 fathoms), four months' provisions and a shot plug a gun of the default
    fit; her sail room the 64's list on her sails, the driver's spare among its occasional sails."""
    spec = her.spec
    assert [(b.kind, b.length_ft) for b in spec.boats] == [
        ("launch", 31.0),
        ("barge", 32.0),
        ("pinnace", 28.0),
        ("cutter", 25.0),
        ("cutter", 25.0),
        ("cutter", 18.0),
    ]
    assert all(b.crew == b.oars + 1 for b in spec.boats)
    assert [p.kind for p in spec.pumps] == ["chain"] * 4 + ["hand"] * 2
    assert spec.hold.capacity_tons == 160.0
    st = spec.crew.stores
    assert (st.water_tons, st.provisions_days, st.cordage_fathoms, st.shot_plugs) == (
        223.0,
        120.0,
        1350.0,
        82.0,
    )
    assert st.spars == {
        "topmast": 2,
        "topgallant_mast": 2,
        "yard": 2,
        "studdingsail_boom": 4,
        "jib_boom": 1,
    }
    kinds = [s.kind for s in st.sails]
    assert "mizzen.driver" in kinds and "mizzen.course" in kinds and len(kinds) == 20
    assert spec.crew.ration.table == "navy"


# ---------------------------------------------------------------------------
# Her description, its words and its rank (Bel-D §8)
# ---------------------------------------------------------------------------


def test_her_description_names_her_file_and_ranks_her_a_ship_of_the_line():
    """Bel-D §8.1-§8.2: `seventy-four`, "a ship" to the tops and "a seventy-four, a ship of the
    line, fourteen ports a tier" to the glass, her roles a King's ship's and a commodore's and her
    fit her default, filed as every row since SW-4 files both (Bel-D §8.1 had no fit, the default
    serving either way); "a ship of the line" names her and no other file, rank 4;
    "a two-decker" and "a third rate", which name the 64 as well, are not taken (judgement). She
    sails by her first role, a row filed since package 75 (`brains.INTENT_RULED_ROWS`)."""
    from freesail.world import brains
    from freesail.world import captains as C
    from freesail.world import ships as S

    for words in (
        "a seventy-four",
        "seventy-four",
        "a 74",
        "a seventy-four gun ship",
        "a ship of the line",
        "ship of the line",
        "a line-of-battle ship",
        "line-of-battle ship",
        "a line of battle ship",
        "a French ship of the line",
    ):
        assert S.description_key(words) == "seventy-four", words
    for words in ("a two-decker", "a third rate", "a first rate"):
        assert S.description_key(words) is None, words
    d = S.description("seventy-four")
    assert d["file"] == SEVENTY_FOUR and d["rig"] == "a ship"
    assert d["what"] == "a seventy-four, a ship of the line, fourteen ports a tier"
    assert d["roles"] == ["kings-ship", "commodore"] and d["fit"] == "arrogant class 1795"
    own = S.file_descriptions(SEVENTY_FOUR)["seventy-four"]
    assert own["what"] == d["what"] and S._default_fit(SEVENTY_FOUR) == own["fit"]
    assert C.size_of_words(d["what"]) == C.size_rank_of(d["what"]) == 4
    assert C.size_of_file(SEVENTY_FOUR) == C.SIZE_RANK["seventy-four"] == 4
    assert "seventy-four" not in brains.INTENT_RULED_ROWS
    vessel = type("Vessel", (), {"description": "seventy-four", "role": ""})()
    assert brains.role_of_vessel(vessel, None) == "kings-ship"


PERIOD_NAMES = (
    "mizzen course",
    "mizen course",
    "mizzen",
    "mizen",
    "mizen yard",
    "driver",
    "spanker",
    "driver boom",
    "spritsail",
    "sprit topsail",
    "spritsail topsail yard",
    "crossjack",
    "cro'jack yard",
    "foresail",
    "mainsail",
    "fore staysail",
    "middle staysail",
    "mizen staysail",
    "head sails",
    "kites",
    "stuns'ls",
    "lower yards",
    "upper yards",
    "royal masts",
    "storm staysails",
    "storm canvas",
    "occasional sails",
    "save-all",
    "fore sheet",
    "main top bowline",
)


def test_her_period_names_resolve(her):
    """test_period_names_resolve's form (tests/test_ship_particulars.py): object phrases as the
    grammar hands them to the resolver, the article already gone; 'the spanker' and 'the driver'
    her driver in the sail room (Ext §17.2), her after sail the mizen course."""
    from freesail.orders.resolve import noun_table

    table = noun_table(load_ship(SEVENTY_FOUR))
    for phrase in PERIOD_NAMES:
        assert table.lookup(phrase) is not None, phrase
    assert table.lookup("spanker").ids == ["mizzen.driver"]


# ---------------------------------------------------------------------------
# The generator's report (the lead's notes of 2026-10-29, item 2)
# ---------------------------------------------------------------------------

REPORT_PROBE = """
import sys
sys.path.insert(0, "tools")
import gen_ships
sys.modules["gen_ships"] = gen_ships
from ships import bellerophon as her
her.build(sys.argv[1])
"""


def test_the_generators_report_prints_what_her_notes_do_not_carry(tmp_path):
    """`her_report()`, printed to the standard error as her file is written: the hull as drawn,
    the measured triples asserted, her rope's scale, the cuts above the caps, the mizen course
    with the two other readings of its tack, the driver and its jaws, the bowsprit and the yards
    under it, her fits' pieces, broadsides and men, and the quarter bill's arithmetic. Her file
    comes out as it stands."""
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
    drawn = "seventy-four: the hull as drawn (freesail/ship/form.py):"
    assert f"{drawn} drawn displacement " in said and "against the filed 2600 t" in said
    assert said.count(f"{drawn} the ") == len(load_spec(SEVENTY_FOUR).hull.profile.ports_m)
    assert "asserted within 0.05 m of the drawn side: 26 (" in said
    assert "seventy-four: plain sail 2225 m2, her rope's scale 1.185." in said
    assert (
        "seventy-four: mizen course: tack 10.24 m above her water, 9.0 ft above her poop's" in said
    )
    assert said.count("seventy-four: mizen course, the other reading, ") == 2
    assert "seventy-four: driver: jaws 12.30 m, set by the after leech at 6 ft of head room" in said
    assert "seventy-four: bowsprit: 17.3 ft inboard along its steeve, 48.7 ft outboard" in said
    for fit, line in (
        ("arrogant class 1793", "74 pieces, a broadside of 781 lb by 70's rule, 362 men"),
        ("arrogant class 1795", "82 pieces, a broadside of 867 lb by 70's rule, 378 men"),
        ("as the bellona 1812", "78 pieces, a broadside of 938 lb by 70's rule, 364 men"),
    ):
        assert f"seventy-four: fit '{fit}': {line} at one side's guns." in said
    assert (
        "seventy-four: the quarter bill on 'arrogant class 1795': her 419 seamen, 378 men at the "
        "guns, 16 of them marines at the carronades, and 2 at the wheel leave 55 trimmers; the "
        "bill keeps 95 marines in their division." in said
    )
    assert (ROOT / SEVENTY_FOUR).read_bytes() == (tmp_path / "seventy-four.yaml").read_bytes()


# ---------------------------------------------------------------------------
# Her helm and her handling as tuned (Bel-D §9; her road's step 5)
# ---------------------------------------------------------------------------


def _truth_17_form(path, wind_kn):
    """Truth 17's form (tests/test_known_truths.py): from rest at 293 degrees in a northerly,
    plain sail set and braced sharp up; her nearest the wind after six minutes, her sternway,
    the second she settled on her course, and her speed at fifteen minutes."""
    from tests.test_known_truths import events, headway_kn, knots, make, off_wind

    world = make(path, 293.0, knots=wind_kn, speed_kn=0.0)
    world.submit("set plain sail")
    world.submit("brace sharp up on the starboard tack")
    min_off, sternway, settled_at, on_course = 180.0, 0.0, None, 0
    for t in range(1, 901):
        world.tick()
        if t > 360:
            min_off = min(min_off, off_wind(world))
            sternway = max(sternway, -headway_kn(world))
        error = abs(math.degrees(units.wrap_pi(world.ship.dyn.heading - math.radians(293.0))))
        on_course = on_course + 1 if knots(world) > 3.0 and error < 10.0 else 0
        if settled_at is None and on_course >= 60:
            settled_at = t - 60
    return events(world, "ship.aback"), min_off, sternway, settled_at, knots(world)


def test_her_helm_as_tuned_holds_truths_6_and_17():
    """`clr_x_m` tuned with her rig whole, Bel-D §9's second knob, in the 64's forms of truths 6
    and 17 (tests/test_indefatigable.py; docs/dev/TuningNotes.md, old beside new; measured at seed
    7 in fifteen knots). **4.8 m**: her start, 5.5, the 64's stage-A lead over her centroid, took
    her aback getting under way from rest (29.6 deg off, 1.46 kn of sternway, never settled); 4.9
    holds in 15 kn and is aback in 16; 5.0 is aback in 15. At 4.8, truth 6's form: 0.39 deg of
    weather helm on the beam, 2.32 with the headsails in, 0.83 of lee helm with the mizen course
    in (at 5.5: 0.97, 2.88, 0.21 lee); truth 17's form no nearer than 60.7 deg off, settled in 439
    s, and in 16 kn 55.9 deg, 498 s (aback in 17, as the 64 at her 4.8); weather helm from seven
    points to ten, +0.16, +0.39 and +0.79 at seven points, the beam and ten points (the 64's +0.17,
    +0.43 and +0.76); at six points, her own close-hauled course, 0.97 deg of lee helm (the 64's
    0.95), banded as the 64's. The Bellona's "weatherly helm" (Lavery 1985 p. 9, Table 2) is not
    reached close-hauled without her griping aback getting under way: for the owner's eye."""
    from tests.test_known_truths import reading, run, under_plain_sail

    world = under_plain_sail(SEVENTY_FOUR, 270.0)
    plain = math.degrees(world.ship.dyn.weather_helm)
    assert 0.1 <= plain <= 1.0, plain
    world.submit("take in the headsails")
    run(world, 900, trim_every=120)
    without_headsails = math.degrees(world.ship.dyn.weather_helm)
    assert without_headsails > plain + 1.0
    world.submit("set the headsails")
    world.submit("take in the mizzen course")
    run(world, 900, trim_every=120)
    without_after = math.degrees(world.ship.dyn.weather_helm)
    assert without_after < 0.0 and without_after < plain
    for off in (78.75, 112.5):  # seven points and ten: weather helm, small
        helm = reading(under_plain_sail(SEVENTY_FOUR, off))["weather_helm"]
        assert 0.1 <= helm <= 1.0, (off, helm)
    helm = reading(under_plain_sail(SEVENTY_FOUR, 67.5))["weather_helm"]
    assert -1.5 <= helm <= 0.0, helm  # six points: lee helm, as the 64's
    for wind_kn in (15.0, 16.0):
        aback, min_off, sternway, settled_at, kn = _truth_17_form(SEVENTY_FOUR, wind_kn)
        assert aback == [], wind_kn
        assert min_off > 45.0 and sternway < 0.5, (wind_kn, min_off, sternway)
        assert settled_at is not None and settled_at <= 600, (wind_kn, settled_at)
        assert kn > 4.0, wind_kn


def _settled(*also, heading=292.5, knots=15.0, path=SEVENTY_FOUR):
    """Her file whole in a northerly on the starboard tack, six points off (truth 10's middle
    heading), under plain sail, settled with the yards trimmed (the 64's `_world`); `also`, sails
    set by name beside it."""
    from freesail.api.session import make_world
    from freesail.core.world import Scenario

    scenario = Scenario(
        wind_from_deg=0.0,
        wind_speed_kn=knots,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=heading,
        ship_speed_kn=4.0,
    )
    world = make_world(7, path, scenario)
    for text in ("set plain sail", "brace sharp up on the starboard tack"):
        world.submit(text)
    for sid in also:
        world.submit(f"set the {sid}")
    for i in range(1200):
        if i >= 400 and i % 120 == 40:
            world.submit("trim sails")
        world.tick()
    return world


def _until(world, words, ticks):
    """Tick until a line with `words` is logged: its tick."""
    start = world.clock.tick
    for _ in range(ticks):
        world.tick()
        hit = [e for e in world.log if e.tick > start and words in e.text]
        if hit:
            return hit[0].tick
    raise AssertionError(f"no '{words}' in {ticks} ticks")


def test_her_classing_is_the_64s_counting_the_head_on_the_masts():
    """The golden table's frigate row (tests/test_rig_classing.py; Ext §10.1), as the 64's at her
    stage B (Ext §10.3 item 4's form, Bel-D §9): three masts with yards, four head yards on the
    fore mast and eight after, the main backed, square-rigged, the stagger +2.0 degrees; her
    mizen course her after sail and her boom sail, the driver in the sail room; the spritsail and
    sprit-topsail yards in the head list, never in the after yards; the mizen yard in none."""
    from freesail.evolutions import trim as yard_trim
    from freesail.physics.sails import _square_rigged

    ship = load_ship(SEVENTY_FOUR)
    for sid in ship.groups["plain sail"]:
        ship.sails[sid].state = SailState.SET
    assert [m.id for m in scripts._masts_with_yards(ship)] == [
        "fore.mast",
        "main.mast",
        "mizzen.mast",
    ]
    head, aft = scripts.head_and_after_yards(ship)
    on_masts = [y for y in head if not ship.under_bowsprit(y)]
    assert len(on_masts) == 4 and {ship.mast_of(y).id for y in on_masts} == {"fore.mast"}
    under = {y.id for y in head if ship.under_bowsprit(y)}
    assert under == {"spritsail.yard", "sprit_topsail.yard"}
    assert len(aft) == 8 and not {y.id for y in aft} & under
    assert "mizzen.yard" not in {y.id for y in [*head, *aft]}
    assert ship.mast_of(scripts.yards_to_back(ship)[0]).id == "main.mast"
    assert _square_rigged(ship) is True
    targets = {y.id: y.brace_limit for y in scripts.working_yards(ship)}
    _pairs, diff = yard_trim.stagger(ship, targets)
    assert diff == pytest.approx(2.0, abs=0.05)
    assert [s.id for s in scripts.after_gaff_sails(ship)] == ["mizzen.course"]
    assert [s.id for s in scripts.boom_sails(ship)] == ["mizzen.course"]
    assert scripts.dipping_lugs(ship) == []


def test_she_handles_as_a_ship_with_her_mizen_yard_and_her_spritsails():
    """Truth 7-189's form on her file (the 64's; Bel-D §9, her handling; Ext §10.3 item 4), at
    seed 7, fifteen knots, six points off under plain sail. "Mainsail haul" swings the main and
    mizzen yards alone, the yards under the bowsprit going with the head yards at "let go and
    haul"; the mizen yard is never braced; the course is hauled aft at helm's a-lee and brailed
    up hove to. Hove to with the spritsail and the sprit topsail set by name first, they are
    clewed up, and she lies to below 1.6 kn, the heading steady within 15 degrees, 59.1 to 65.0
    degrees off (measured), the swing's peak at +481 s standing 0.02 degrees over truth 12's 65
    before she settles at 63 to 64 (4.7 m and 4.9 m of `clr_x_m` the same within 0.2: no knob of
    the helm's): so the band asked here is 45 to 65.5 (judgement, for the lead), truth 12's own
    band held in its own form below (`test_she_stays_quickly_wears_and_lies_to`)."""
    world = _settled()
    ship = world.ship
    assert ship.sails["mizzen.course"].is_set
    assert world.submit("tack ship").kind == "order.accepted"
    _until(world, "Mainsail haul", 500)
    runner = ship.extra["evolutions"]
    (tack,) = [i.script for i in runner.instances if isinstance(i.script, scripts.TackScript)]
    assert {y.id for y in tack.swing.yards} == {y.id for y in tack.after}
    assert {ship.mast_of(y).id for y in tack.swing.yards} == {"main.mast", "mizzen.mast"}
    assert {"spritsail.yard", "sprit_topsail.yard"} <= {y.id for y in tack.head}
    assert ship.spars["mizzen.yard"].brace_angle == 0.0
    _until(world, "Let go and haul", 700)
    assert {"spritsail.yard", "sprit_topsail.yard"} <= {y.id for y in tack.swing.yards}
    _until(world, "Tacked", 1200)
    assert ship.spars["mizzen.yard"].brace_angle == 0.0
    for text in ("set the spritsail", "set the sprit topsail"):
        world.submit(text)
    for _ in range(600):
        world.tick()
    assert ship.sails["spritsail"].is_set and ship.sails["sprit_topsail"].is_set
    start = world.clock.tick
    world.submit("heave to")
    for _ in range(300):
        world.tick()
    assert units.ms_to_knots(ship.dyn.speed) < 1.6, "not stopped within five minutes"
    offs, speeds = [], []
    for _ in range(600):
        world.tick()
        offs.append(abs(math.degrees(units.wrap_pi(ship.dyn.heading - world.wind.direction_from))))
        speeds.append(units.ms_to_knots(ship.dyn.speed))
    after = [e for e in world.log if e.tick > start]
    assert any(e.kind == "ship.hove_to" for e in after), [e.text for e in after]
    assert not [e for e in after if e.kind == "ship.aback"]
    for sid in ("spritsail", "sprit_topsail"):
        assert ship.sails[sid].state is SailState.IN_THE_GEAR
    assert ship.sails["mizzen.course"].state is SailState.IN_THE_GEAR
    assert ship.spars["mizzen.yard"].brace_angle == 0.0
    assert max(speeds) < 1.6
    assert all(45.0 <= o <= 65.5 for o in offs), (min(offs), max(offs))
    assert max(offs) - min(offs) <= 30.0


def test_she_stays_quickly_wears_and_lies_to():
    """The Bellona "steers very easily, wears very quickly" (1763) and "wears and stays quickly"
    (1783) (Lavery 1985 p. 9, Table 2), on her file as tuned, at seed 7 in fifteen knots, in the
    64's form (truth 7-189's clause, tests/test_indefatigable.py). In truth 10's form, from 290,
    292.5 and 295 degrees she tacks in 237, 243 and 258 s, gaining 105, 95 and 69 m (at her start
    of 5.5 m 290, 299 and 321 s), under Luce's five minutes as the 64's 244, 251 and 266 s are, and
    well under the frigate-36's 343, 447 and 370 s, which are tacked here, so that the clause says
    what it claims if she is retuned. The band: quicker than the frigate-36's quickest (the
    reports' "quickly", which gives no time) and no quicker than three and a half minutes, a round
    floor of judgement 27 s under her quickest, with no source; truth 10's 285 s is not asked of
    her, as of the 64 (the lead's). In truth 11's form she wears in 499 s (the frigate-36 513 s),
    within its six to twelve minutes; hove to in truth 12's form she lies 56.5 to 63.4 deg off at
    1.18 kn at most."""
    from tests.test_known_truths import (
        close_hauled_on_starboard,
        events,
        hove_to,
        knots,
        off_wind,
        run,
        until,
        wear,
    )

    frigate = []
    for heading in (290.0, 292.5, 295.0):
        world = close_hauled_on_starboard(FRIGATE, heading=heading)
        world.submit("tack ship")
        done, seconds = until(world, ("ship.tacked", "ship.missed_stays"), 900)
        assert [e.kind for e in done] == ["ship.tacked"], heading
        frigate.append(seconds)
    for heading in (290.0, 292.5, 295.0):
        world = close_hauled_on_starboard(SEVENTY_FOUR, heading=heading)
        y_before = world.ship.dyn.y
        world.submit("tack ship")
        done, seconds = until(world, ("ship.tacked", "ship.missed_stays"), 900)
        assert [e.kind for e in done] == ["ship.tacked"], heading
        assert 210 <= seconds < min(frigate), (heading, seconds, frigate)
        assert world.ship.dyn.y > y_before, heading
        assert world.ship.spars["mizzen.yard"].brace_angle == 0.0
    seconds, _lost = wear(close_hauled_on_starboard(SEVENTY_FOUR))
    assert 360 <= seconds <= 720, seconds
    world = hove_to(SEVENTY_FOUR)
    run(world, 300)
    offs, speeds = [], []
    for _ in range(600):
        world.tick()
        offs.append(off_wind(world))
        speeds.append(knots(world))
    assert max(speeds) < 1.6
    assert all(45.0 <= o <= 65.0 for o in offs), (min(offs), max(offs))
    assert events(world, "ship.hove_to") and events(world, "ship.aback") == []


def _driver_bent_file(tmp_path):
    """Her file with the driver bent in the course's place, its boom rigged out (Ext §17.11),
    and the course in the sail room (the 64's `her_doc_with_the_driver_bent`)."""
    import yaml

    doc = yaml.safe_load((ROOT / SEVENTY_FOUR).read_text(encoding="utf-8"))
    sails = {s["id"]: s for s in doc["sails"]}
    sails["mizzen.course"]["bent"] = False
    del sails["mizzen.driver"]["bent"]
    next(s for s in doc["spars"] if s["id"] == "mizzen.boom")["rigged_out"] = True
    path = tmp_path / "seventy-four-driver.yaml"
    path.write_text(yaml.safe_dump(doc), encoding="utf-8")
    return str(path)


def test_she_sails_as_the_vanguard_and_the_bellona_were_reported(tmp_path):
    """Bel-D §9's sailed checks, at seed 7 with the yards trimmed, half an hour settled. The
    *Vanguard*, an Arrogant, on 1 August 1798: 5 kn 4 f a point abaft the beam in moderate
    breezes under her courses, topsails and driver (NRS vol. 2 p. 53, page image; Bel S7: 4.75 to
    5.5 kn, ±1 kn); she makes 5.31 kn there in 11 kn of wind (Beaufort 4, judgement; 4.86 in 10 kn,
    6.20 in 13), the driver bent in the course's place and set, 3.8 deg of weather helm (the
    Caledonia's "half a turn a-weather", Bel S14). The Bellona "under reefed topsails 9 kn in smooth
    water, else 7-8" (1763) and "6-7 kn" (1783) (Lavery 1985 p. 9, Table 2; Bel-D §9's 6-9 kn):
    close-hauled, six points off, under her courses, single-reefed topsails and jib, she makes 6.93
    kn in 25 kn of wind (6.17 in 22, 7.66 in 28)."""
    from tests.test_known_truths import make, reading, run

    world = make(_driver_bent_file(tmp_path), 360.0 - 101.25, 11.0, 4.0)
    for text in ("set the courses", "set the topsails", "set the driver",
                 "brace sharp up on the larboard tack"):  # fmt: skip
        world.submit(text)
    run(world, 600)
    run(world, 1200, 120)
    r = reading(world)
    assert world.ship.sails["mizzen.driver"].is_set
    assert abs(r["off"] - 101.25) <= 1.0
    assert 4.75 - 1.0 <= r["speed"] <= 5.5 + 1.0, r
    world = make(SEVENTY_FOUR, 360.0 - 67.5, 25.0, 4.0)
    for text in ("set the courses", "set the topsails", "reef the topsails", "set the jib",
                 "brace sharp up on the starboard tack"):  # fmt: skip
        world.submit(text)
    run(world, 600)
    run(world, 1200, 120)
    r = reading(world)
    assert abs(r["off"] - 67.5) <= 1.0
    assert 6.0 <= r["speed"] <= 9.0, r


# ---------------------------------------------------------------------------
# Truth 7-194: her particulars hold their sources (Bel-D §14.2; her road's step 5)
# ---------------------------------------------------------------------------


def test_truth_7_194_her_particulars_hold_their_sources():
    """**A draft, for Phase 5 to move into `tests/test_known_truths.py`** (Build-Ships.md §15,
    row 7-194; Bel-D §14.2), pinned at her step 5, on `seventy-four.yaml` as it loads. Her beam
    46 ft 9 in (ZAZ1357's table) 14.25 ± 0.05 m; her waterline 168 ft 51.2 ± 0.3 m; her draught to K
    6.46 ± 0.10 m at her water, the Channel line; her displacement within Bel's H1 band, 2,490 to
    2,900 t, and within the measured lines' 2,560 to 2,660 t at her line (Bel-D §2.1, either
    conversion); her GM within 1.2 to 1.5 m. Her lowest lower-deck sill 1.57 ± 0.01 m above her
    water (the Bellona's 5 ft 2 in at Channel draught, Lavery 1985 p. 9, Table 2), the side at it
    6.90 to 7.09 m (6.92 moulded, 7.04 with the plank; 7.04 measured). Her ports a side 14, 14 and
    7, the forecastle's 2 (Bel H3; the forecastle's third place a carronade's over the rail), the
    lower 3 ft 4 3/4 in by 2 ft 8 1/2 in, 1.04 by 0.83 m (Bel-D §3.2's 0.82 a rounding slip). Her
    main mast within 107 ft 4 1/2 in to 108 ft from its heel to its head (Steel's rule; Lavery
    Table 10: 108 ft, its heel 5.11 ft above the keel's top), the mizen yard 86 ft 6 in ± 1%.
    Twenty-eight long 32-pounders of 55 cwt on her lower deck in every fit; 74, 82 and 78 pieces;
    broadsides by 70's rule 781 and 867 lb (James vol. 1, Abstracts No. 1 and 3) and 938 lb. Her
    crews to the pair 13, 9, 7 and 6 for the 32s, 18s, 12s and 9s (Falconer 1780) and 4 to a
    carronade (Douglas 1829 art. 136). Her complement 590 (the 1807 column), five lieutenants, 111
    marines of whom eleven officers and NCOs (the column's: her notes, and her people file's
    captain, lieutenant and serjeant drawn from them); filling 18; exercise 9. Four bowers of 67
    cwt, a stream of 16 and a kedge of 8 on seven 22-in cables (Steel 1794; Lavery p. 15, Table 4);
    six boats (Lavery p. 16, Table 5). "A ship of the line" names her description, rank 4. Pins
    states and bands, no digest."""
    from freesail.combat.far import far_ship
    from freesail.world import captains as C
    from freesail.world import ships as S

    ship = load_ship(SEVENTY_FOUR)
    spec, h = ship.spec, ship.hull.spec
    assert abs(h.beam_m - 14.25) <= 0.05
    assert abs(h.length_waterline_m - 51.2) <= 0.3
    assert abs(h.draught_m - 6.46) <= 0.10
    assert 2_490_000 <= h.displacement_kg <= 2_900_000
    assert 2_560_000 <= h.displacement_kg <= 2_660_000
    assert 1.2 <= h.gm_m <= 1.5
    p = h.profile
    _x, sill, half = min(ports_of(p, "lower"), key=lambda t: t[1])
    assert abs(sill - 1.57) <= 0.01
    assert 6.90 <= half <= 7.09
    counts = {deck: len(ports_of(p, deck)) for deck in ("lower", "upper", "quarterdeck")}
    assert counts == {"lower": 14, "upper": 14, "quarterdeck": 7}
    forecastle = [g for g in spec.armament.fits[FIT_1793].guns if g.deck == "forecastle"]
    assert len({g.number for g in forecastle}) == 2  # the forecastle's two ports a side
    width, depth = dict(p.port_size_m)["lower"]
    assert (round(width, 2), round(depth, 2)) == (1.04, 0.83)
    main = ship.spars["main.mast"]
    x_ft = MIDSHIPS_FT + main.x_m / FT
    heel_ft = -(18.89 + 1.72 * (MIDSHIPS_FT - x_ft) / 168.0) + 5.11  # above WL1 (Bel §5.2)
    head_ft = above_wl1_ft(h.deck_height_m + main.height_m)
    length_ft = (head_ft - heel_ft) / math.cos(main.rake)
    assert 107.0 + 4.5 / 12.0 <= length_ft <= 108.0 + 0.4, length_ft  # heights to the decimetre
    assert abs(ship.spars["mizzen.yard"].length_m / (86.5 * FT) - 1.0) <= 0.01
    arm = spec.armament
    for fit, pieces, lb in ((FIT_1793, 74, 781.0), (FIT_1795, 82, 867.0), (FIT_1812, 78, 938.0)):
        guns = arm.fits[fit].guns
        assert len(guns) == pieces, fit
        lower = [g for g in guns if g.deck == "lower"]
        assert len(lower) == 28 and all(
            (g.kind, g.pounder, g.weight_cwt) == ("long", 32, 55.0) for g in lower
        ), fit
        assert far_ship(SEVENTY_FOUR, "britain", fit=fit).broadside_lb == lb, fit
        crews = {(g.kind, int(g.pounder)): g.crew for g in guns}
        for (kind, pounder), crew in crews.items():
            want = 4 if kind == "carronade" else {32: 13, 18: 9, 12: 7, 9: 6}[pounder]
            assert crew == want, (fit, kind, pounder)
        assert arm.fits[fit].exercise_charges == 9
    crew = spec.crew
    assert crew.complement == 590
    assert sum(1 for q in crew.posts if q.post.endswith(" lieutenant")) == 5
    assert crew.stations["marines"] == 111
    assert {"captain of marines", "lieutenant of marines", "sergeant of marines"} <= {
        q.role for q in crew.people if q.station == "marines"
    }
    assert crew.quarter_bill.filling == 18
    anchors = spec.ground_tackle.anchors
    bowers = [a for a in anchors if abs(a.weight_kg - 67 * CWT_KG) <= 1.0]
    assert len(bowers) == 4 and all(a.cable_in == 22.0 for a in bowers)
    weights = sorted(round(a.weight_kg / CWT_KG) for a in anchors if a not in bowers)
    assert weights == [8, 16]
    assert sum(a.cable_fathoms for a in bowers) / 100.0 == 7.0  # seven cables of 100 fathoms
    assert len(spec.boats) == 6
    assert S.description_key("a ship of the line") == "seventy-four"
    assert C.size_of_file(SEVENTY_FOUR) == 4


# ---------------------------------------------------------------------------
# A frigate meeting her (Bel-D §8.3, §14.1)
# ---------------------------------------------------------------------------


@pytest.fixture
def far_only(monkeypatch):
    """The far brain alone: no crewed promotion within the range (tests/test_brains.py's), so
    that the brain's own judgement is what the test reads."""
    from freesail.world import crews

    monkeypatch.setattr(crews, "CREWED_CAP", 0)


@pytest.mark.parametrize(
    "description, role, keeps_away",
    [("brig-sloop", "cruiser", True), ("frigate", "kings-ship", False)],
    ids=["cruiser", "kings-ship"],
)
def test_a_cruiser_keeps_away_from_her_and_a_kings_frigate_does_not_today(
    far_only, description, role, keeps_away
):
    """Bel-D §8.3 and §14.1: she is hove to off the Lizard (tests/test_brains.py's world, seed 7),
    a French man of war on her own five miles to the north, made out with her colours. A cruiser
    finds her an enemy of a bigger class (`overmatched`: rank 4 against her own) and evades, as
    the cruisers' book has it; a frigate in the King's ship's role does not, and closes her: the
    engine's today, recorded, the rank-4 rule (B7.e, the owner's "Agreed") being her road's step
    7, not built here. **Plainly:** the design's cruiser was a frigate in the cruiser's role, which
    no scenario may give since SW-4 (a frigate's file gives her the King's ship's and the
    commodore's roles alone), so the cruiser is the brig-sloop, the cruisers' own description."""
    from tests.test_brains import world_at

    world = world_at(49.5, -5.5, SEVENTY_FOUR)
    world.submit("set plain sail")
    world.run(900)
    world.submit("heave to")
    world.vessels.serial += 1
    from freesail.world.ships import vessel_from_spec

    v = vessel_from_spec(
        world,
        {
            "description": description,
            "name": "Méduse",
            "nation": "france",
            "position": "49 35 N 5 30 W",
            "goal": "patrolling off the Lizard within 10 miles",
            "intent": "keep the station off the Lizard within 10 miles",
            "colours": "shown",
        },
        world.vessels.serial,
    )
    world.vessels.add(v)
    assert v.brain.role == role
    states = []
    for _ in range(40):
        world.run(60)
        states = [s for _, s in v.brain.history]
        if "evading" in states:
            break
    assert ("evading" in states) is keeps_away, states
    if not keeps_away:
        assert {"investigating a stranger", "engaging", "chasing"} & set(states), states


# ---------------------------------------------------------------------------
# Her round trip under her rules captain, and her checkpoint at quarters (Bel-D §11, §14.1)
# ---------------------------------------------------------------------------

EXERCISING = ROOT / "data" / "scenarios" / "exercising-the-great-guns.yaml"


def test_she_sails_under_her_rules_captain_with_no_fit_named_and_round_trips(tmp_path):
    """Bel-D §11: a scenario of hers, written from its fields by the harbour's maker (the great
    guns' with her file in the frigate's place), reads back to itself and loads with no fit named;
    she sails it at seed 7 under her rules captain as a King's ship with her default fit, "arrogant
    class 1795", the 64 in sight under a rules captain of its own, and no order of hers refused;
    saved at half an hour and loaded from the checkpoint, she carries on as the world that was
    never saved; and a world made with no scenario at all (`make_world(7, her file, Scenario())`)
    takes her default too."""
    import copy

    from freesail.api.session import make_world, ship_factory
    from freesail.core import replay as replay_mod
    from freesail.core.world import Scenario
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
    fields["name"] = "A seventy-four off the Lizard"
    fields.pop("standing_orders")  # her rules captain's book alone
    fields["ship"]["file"] = SEVENTY_FOUR
    assert "fit" not in fields["ship"]
    fields["ships"] = [
        {
            "description": "sixty-four",
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
    assert sf.seed == 7 and sf.ship_file == SEVENTY_FOUR and sf.scenario.fit is None
    world = make_scenario_world(sf)
    begin(world, sf)
    assert world.ship.fit == FIT_1795
    assert world.captain.commands and world.captain.role == "kings-ship"
    stranger = world.vessels.find("Stranger")
    assert stranger.ship_file == SIXTY_FOUR and stranger.brain.role == "kings-ship"
    world.run(1800)
    saved = replay_mod.save_to_file(world, tmp_path / "hers.json")
    world.run(1800)
    assert not [e for e in world.log if e.kind == "order.rejected"]
    assert units.ms_to_knots(world.ship.dyn.speed) > 3.0
    loaded, how = replay_mod.load(saved, ship_factory)
    assert how == "checkpoint" and loaded.ship.fit == FIT_1795
    loaded.run(1800)
    assert loaded.clock.tick == world.clock.tick and loaded.state() == world.state()
    assert make_world(7, SEVENTY_FOUR, Scenario()).ship.fit == FIT_1795


def test_her_checkpoint_at_quarters_is_under_test_checkpoints_bound(tmp_path):
    """Bel-D §14.1: beaten to quarters with her guns cast loose, her company of 590 at their
    stations and her marines in their division, she saves with a checkpoint under
    tests/test_checkpoint.py's bound of 2 MB (the research's scratch 74, 1,220 KB raw: Bel §7.5),
    and loads from it at quarters, her bill as it was."""
    from freesail.api.session import ship_factory
    from freesail.core import replay as replay_mod
    from freesail.crew.quarters import MARINES, quarters_of
    from tests.test_brains import world_at

    world = world_at(49.5, -5.5, SEVENTY_FOUR)
    world.run(10)
    world.submit("beat to quarters")
    world.run(5)
    world.submit("cast loose the guns")
    world.run(200)
    saved = replay_mod.save_to_file(world, tmp_path / "quarters.json")
    cp = replay_mod.checkpoint_path(saved)
    assert cp.exists() and cp.stat().st_size < 2_000_000, cp.stat().st_size
    loaded, how = replay_mod.load(saved, ship_factory)
    assert how == "checkpoint"
    q, q2 = quarters_of(world.ship), quarters_of(loaded.ship)
    assert q2.at_quarters and len(q2.divisions[MARINES]) == len(q.divisions[MARINES]) == 95
    assert {k: gc.deck for k, gc in q2.crews.items()} == {k: gc.deck for k, gc in q.crews.items()}


# ---------------------------------------------------------------------------
# Her bill by deck (B7.b: Bel-D §6.4, §12.5; her road's step 6)
# ---------------------------------------------------------------------------

ARMED = (
    "data/ships/brig.yaml",
    "data/ships/cutter.yaml",
    "data/ships/frigate-36.yaml",
    "data/ships/hermaphrodite-brig.yaml",
    "data/ships/merchant-brig.yaml",
    "data/ships/privateer-schooner.yaml",
    "data/ships/razee-44.yaml",
    SIXTY_FOUR,
)
# Each armed file's beat at muster, its first line, as it was before her bill by deck and as it
# is (measured at seed 7 in tests/test_brains.py's world, the code before B7.b and after, line
# for line and man for man): none of them carries the bill's `marines`, so none keeps a division.
BEAT_LINE = {
    "data/ships/brig.yaml": "ten gun crews manned, the trimmers 42, the helm 2, the powder 13",
    "data/ships/cutter.yaml": "three gun crews manned, the trimmers 9, the helm 1, the powder 4",
    "data/ships/frigate-36.yaml": "21 gun crews manned, the trimmers 44, the helm 2, the powder 22",
    "data/ships/hermaphrodite-brig.yaml": (
        "ten gun crews manned, the trimmers 65, the helm 1, the powder 8"
    ),
    "data/ships/merchant-brig.yaml": (
        "two gun crews manned, the trimmers 2, the helm 1, the powder 1"
    ),
    "data/ships/privateer-schooner.yaml": (
        "seven gun crews manned, the trimmers 11, the helm 1, the powder 3"
    ),
    "data/ships/razee-44.yaml": "24 gun crews manned, the trimmers 93, the helm 2, the powder 22",
    SIXTY_FOUR: "32 gun crews manned, the trimmers 137, the helm 2, the powder 29",
}
# The 64's deck lines, new beside her old beat, which had none (B7.b item 2, keyed on two gun
# decks: the lead's answer (2))
SIXTY_FOURS_DECK_LINES = [
    "The lower deck: 13 gun crews, 143 men.",
    "The upper deck: 13 gun crews, 117 men.",
    "The quarterdeck: five gun crews, 30 men.",
    "The forecastle: one gun crew, 6 men.",
]


def _beaten(path, fit=None, heel_deg=None, engaged=None):
    """Her quarters at muster, seed 7, tests/test_brains.py's world; heeled by hand to shut the
    lee ports by the rule, the battery engaged to a side, where asked."""
    from freesail.combat import action, ports
    from freesail.combat.guns import battery_of
    from freesail.crew.quarters import quarters_of
    from tests.test_brains import world_at

    w = world_at(49.5, -5.5, path, **({"fit": fit} if fit else {}))
    w.run(10)
    said = w.submit("beat to quarters")
    w.run(30)
    if heel_deg is not None:
        b = battery_of(w.ship)
        b.engaged = engaged
        w.ship.dyn.heel = math.radians(heel_deg)
        ports.update(b, action._firer(w, w.ship), w.clock.tick)
    return w, said, quarters_of(w.ship)


@pytest.mark.parametrize(
    "fit, crews, wanted, at_carronades, division, trimmers",
    [
        (FIT_1793, 37, 362, 0, 111, 55),
        (FIT_1795, 41, 378, 16, 95, 55),
        (FIT_1812, 39, 364, 16, 95, 69),
    ],
)
def test_her_beat_to_quarters_keeps_her_marines_in_their_division(
    fit, crews, wanted, at_carronades, division, trimmers
):
    """Bel-D §6.3 and §6.4 item 1, B7.b: the bill's `marines`, 95 (her stage 0c's key), read at
    the beat. Measured at muster on each fit at seed 7 in tests/test_brains.py's world off the
    Lizard, old beside new. Before (her step 4): every crew filled and all 111 marines went to the
    guns (1793: 111 at the long guns; 1795: 103 and 8 at the carronades; 1812: 86 and 25), no
    division formed, and the trimmers stood at 166, 150 and 164. Now the beat keeps the 95 before
    the gun crews draw; the long guns leave the marines out, the carronades take them first; every
    crew fills. On "arrogant class 1795" the trimmers 55 and the helm 2 come first, the long guns'
    362 are exactly the seamen left, the four carronades' 16 the marines beyond the 95: the
    division stands at 95 and the trimmers at the bill's 55, as Bel-D §6.3's arithmetic has it.
    On the 1793 fit, no carronade, the division is the whole 111 and the trimmers 55; on the 1812
    fit the carronades take the 16 and twelve seamen beside them, the trimmers gaining the 14
    seamen the long guns leave, 69."""
    from freesail.crew.model import Station
    from freesail.crew.quarters import MARINES, TRIMMERS

    _w, said, q = _beaten(SEVENTY_FOUR, fit)
    assert len(q.crews) == crews and sum(gc.wanted for gc in q.crews.values()) == wanted
    assert all(len(gc.members) == gc.wanted for gc in q.crews.values())
    at_guns = [
        gc.kind for gc in q.crews.values() for s in gc.members if s.station is Station.MARINES
    ]
    assert (at_guns.count("long"), at_guns.count("carronade")) == (0, at_carronades)
    assert len(q.divisions[MARINES]) == division
    assert all(s.station is Station.MARINES for s in q.divisions[MARINES])
    assert len(q.divisions[TRIMMERS]) == trimmers
    assert f"the marines {division}." in said.text


def test_her_beat_says_her_decks_and_the_64s_with_her():
    """B7.b item 2 (Bel-D §6.4): on a ship whose broadside guns stand on the lower and the upper
    deck, the beat says each deck's crews and men, from below, the poop as "the poop": hers on
    the default fit, and the 64's, old beside new (her old beat had no deck line; her crews and
    divisions man for man as before, the lines alone new: measured)."""
    _w, said, q = _beaten(SEVENTY_FOUR)
    lines = q.describe()
    assert lines[1:6] == [
        "The lower deck: 14 gun crews, 182 men.",
        "The upper deck: 14 gun crews, 126 men.",
        "The quarterdeck: seven gun crews, 42 men.",
        "The forecastle: three gun crews, 16 men.",
        "The poop: three gun crews, 12 men.",
    ]
    assert " ".join(lines[1:6]) in said.text
    assert {gc.deck for gc in q.crews.values()} == set(NUMBERS)
    _w, said, q = _beaten(SIXTY_FOUR)
    assert q.describe()[0] == f"Quarters: {BEAT_LINE[SIXTY_FOUR]}."
    assert q.describe()[1:5] == SIXTY_FOURS_DECK_LINES
    assert said.text == "Beat to quarters! " + " ".join(
        [f"Quarters: {BEAT_LINE[SIXTY_FOUR]}.", *SIXTY_FOURS_DECK_LINES]
    )


@pytest.mark.parametrize("path", [p for p in ARMED if p != SIXTY_FOUR])
def test_nothing_of_a_one_gun_deck_file_moves_at_the_beat(path):
    """§12.5's checks for B7.b on each armed file of one gun deck (the eight that are armed and
    the razee): its beat as it was, line for line (`BEAT_LINE`, measured before B7.b and after:
    every crew's men and every division the same, man for man); no deck line; no crew keeping a
    deck, so that its quarters pickle as before (measured byte for byte); no marines' division,
    since its bill has no `marines`."""
    from freesail.crew.quarters import MARINES

    _w, said, q = _beaten(path)
    assert said.text == f"Beat to quarters! Quarters: {BEAT_LINE[path]}."
    assert q.describe()[0] == f"Quarters: {BEAT_LINE[path]}."
    assert not any(line.startswith("The ") and " deck: " in line for line in q.describe())
    assert all(gc.deck is None and "deck" not in gc.__getstate__() for gc in q.crews.values())
    assert getattr(load_spec(path).crew.quarter_bill, "marines", None) is None
    assert not q.divisions.get(MARINES)


def _old_rob_order(gc, bearing_fwd):
    """The robbing order before B7.b (crew/quarters.py `_rob_order`, as it stood), the reference
    against which a ship with no `lower` deck is held."""
    from freesail.crew.quarters import GUN_PREFIX

    key = gc.key[len(GUN_PREFIX) :]
    if "swivel" in key:
        return (0, 0.0, key)
    if not key.isdigit():
        return (1, 0.0, key)
    return (2, gc.x_m if bearing_fwd in (True, None) else -gc.x_m, key)


@pytest.mark.parametrize("path", [p for p in ARMED if p != SIXTY_FOUR])
def test_robbing_on_a_ship_with_no_lower_deck_is_as_it_was(path):
    """§12.5: robbing by deck (B7.b item 4) is keyed on a `lower` deck; on every armed file
    without one, heeled until ports shut and engaged to the lee side, the crews go in the old
    order from either end, and the line is as it was (the razee's and the frigate-36's measured
    before and after: 'from the bow chasers and the guns, Nos. ...')."""
    from freesail.crew.quarters import _rob_order

    w, _said, q = _beaten(path, heel_deg=25.0, engaged="starboard")
    shut = q._shut_crews()
    assert shut == frozenset()
    for fwd in (True, False, None):
        new = sorted(q.crews.values(), key=lambda gc: _rob_order(gc, fwd, shut))
        old = sorted(q.crews.values(), key=lambda gc: _old_rob_order(gc, fwd))
        assert [gc.key for gc in new] == [gc.key for gc in old], fwd
    _freed, words = q.lend(40, False, True)
    assert " deck" not in words and "ports shut" not in words, words


@pytest.mark.parametrize(
    "path, heel, shut_numbers, words",
    [
        (SEVENTY_FOUR, 12.5, range(3, 13), "from the lower deck, Nos. 7 to 11, their ports shut"),
        (SIXTY_FOUR, 12.5, range(3, 11), "from the lower deck, Nos. 5 to 10, their ports shut"),
    ],
    ids=["seventy-four", "sixty-four"],
)
def test_robbing_by_deck_takes_the_shut_lower_deck_first_and_the_lower_deck_last(
    path, heel, shut_numbers, words
):
    """B7.b item 4 (Bel-D §6.4; the owner's "Agreed", §17.0; the lead's answer (2): the two
    two-deckers alike). Heeled 12.5 deg to starboard by hand, engaged to starboard, the sea shuts
    the lee lower ports amidships; sail work wanting sixty hands, the enemy forward, takes the
    lower-deck crews whose starboard gun is shut, from the after end, and says so; with no side
    engaged it takes no deck's crews for shut, and goes to the other decks' from the end that
    bears least, the lower deck last of all. The 64's line old beside new: 'from the guns, Nos. 12
    to 13 and 24 to 26 and 30 to 31' (her upper works' after guns, as she bore) to 'from the lower
    deck, Nos. 5 to 10, their ports shut' (measured)."""
    from freesail.crew.quarters import LOWER, _rob_order

    w, _said, q = _beaten(path, heel_deg=heel, engaged="starboard")
    shut = q._shut_crews()
    assert {int(k[len("gun:") :]) for k in shut} <= set(shut_numbers) and shut
    assert all(q.crews[k].deck == LOWER for k in shut)
    order = sorted(q.crews.values(), key=lambda gc: _rob_order(gc, True, shut))
    ranks = [(gc.key in shut, gc.deck == LOWER) for gc in order]
    first_other = ranks.index((False, False))
    assert all(r == (True, True) for r in ranks[:first_other])
    open_lower = sum(1 for gc in q.crews.values() if gc.deck == LOWER) - len(shut)
    assert all(r == (False, True) for r in ranks[len(ranks) - open_lower :]), ranks
    assert all(r == (False, False) for r in ranks[first_other : len(ranks) - open_lower]), ranks
    freed, said = q.lend(60, False, True)
    assert said == words and len(freed) >= 60
    for gc in q.crews.values():  # hands back to their guns, as the tick puts them
        for s in gc.members:
            if s.fit and s.at is None:
                s.at = gc.key
    w.ship.extra["battery"].engaged = None
    assert q._shut_crews() == frozenset()
    freed, said = q.lend(60, False, True)
    assert "lower deck" not in said and "ports shut" not in said, said


def test_robbing_past_every_gun_says_the_marines_last_with_one_and():
    """The review's mend (2026-11-10): sail work wanting more hands than every crew holds, the
    line by deck ends with the marines as its last item and one "and" ('..., the lower deck, Nos.
    1 to 3 and 12 to 14, and the marines'), where before it read '..., and the lower deck, ...,
    and the marines' (measured). The 64, whose bill keeps no marines, ends on her lower deck."""
    _w, _said, q = _beaten(SEVENTY_FOUR, heel_deg=12.5, engaged="starboard")
    _freed, said = q.lend(400, False, True)
    assert said == (
        "from the lower deck, Nos. 4 to 11, their ports shut, the poop, Nos. 39 to 41, the upper "
        "deck, Nos. 15 to 28, the quarterdeck, Nos. 29 to 35, the forecastle, Nos. 36 to 38, the "
        "lower deck, Nos. 1 to 3 and 12 to 14, and the marines"
    )


def test_a_crew_pickled_before_the_bill_by_deck_reads_no_deck():
    """§12.5: `GunCrew.deck` a plain class default, so that a crew pickled before it (a kept save,
    a checkpoint at quarters) reads None, and so says no deck line and robs as before; a crew
    keeps its deck in the pickle only where it has one."""
    import pickle

    from freesail.crew.quarters import GunCrew

    old = GunCrew("gun:3", ["gun.3.starboard"], 9, x_m=1.0)
    state = old.__getstate__()
    assert "deck" not in state
    back = GunCrew.__new__(GunCrew)
    back.__dict__.update(state)
    assert back.deck is None
    kept = GunCrew("gun:3", ["gun.3.starboard"], 13, x_m=1.0, deck="lower")
    assert pickle.loads(pickle.dumps(kept)).deck == "lower"


@pytest.mark.parametrize(
    "path, words, deck, side, n",
    [
        (SEVENTY_FOUR, "the starboard lower deck", "lower", "starboard", 14),
        (SEVENTY_FOUR, "the lower-deck guns", "lower", None, 28),
        (SEVENTY_FOUR, "the lower deck to larboard", "lower", "larboard", 14),
        (SEVENTY_FOUR, "the upper deck", "upper", None, 28),
        (SEVENTY_FOUR, "the main deck", "upper", None, 28),
        (SEVENTY_FOUR, "the gun deck", "lower", None, 28),
        (SEVENTY_FOUR, "the quarterdeck guns", "quarterdeck", None, 14),
        (SEVENTY_FOUR, "the forecastle guns", "forecastle", None, 6),
        (SEVENTY_FOUR, "the poop", "roundhouse", None, 6),
        (SEVENTY_FOUR, "the larboard poop carronades", "roundhouse", "larboard", 3),
        (SIXTY_FOUR, "the gun deck", "lower", None, 26),
        (RAZEE, "the gun deck", "upper", None, 26),
        (FRIGATE, "the gun deck", "upper", None, 26),
        (FRIGATE, "the quarterdeck carronades", "quarterdeck", None, 8),
    ],
)
def test_a_deck_named_in_an_order_names_its_broadside_guns(path, words, deck, side, n):
    """B7.b item 5 (Bel-D §6.4; orders/gunnery.py, B7's for the package by the lead's word): a
    deck by its words names that deck's broadside guns, with a side or without (`guns_named`, so
    the director's and the world orders' slots take a deck too): "the main deck" the upper
    (Cumby's "the main and lower decks"), "the gun deck" the lowest deck that carries broadside
    guns, her lower deck and the 64's, the razee's and the frigate-36's upper; the poop's word
    names the `roundhouse`; "carronades" its carronades alone."""
    from freesail.orders.gunnery import guns_named

    ship = load_ship(path)
    ids = guns_named(ship, words)
    assert len(ids) == n, (words, len(ids))
    assert {ship.guns[g].deck for g in ids} == {deck}
    assert all(ship.guns[g].place == "broadside" for g in ids)
    if side:
        assert {ship.guns[g].side for g in ids} == {side}
    if "carronades" in words:
        assert {ship.guns[g].kind for g in ids} == {"carronade"}


@pytest.mark.parametrize(
    "path, words, n",
    [
        (FRIGATE, "No. 3 gun", 2),
        (FRIGATE, "No. 3 starboard gun", 1),
        (FRIGATE, "the bow chaser", 1),
        (FRIGATE, "the quarterdeck", 0),
        (FRIGATE, "the forecastle", 0),
        (FRIGATE, "the lower deck", 0),
        (RAZEE, "the poop", 0),
        (SEVENTY_FOUR, "the quarterdeck", 0),
        (SEVENTY_FOUR, "No. 8 starboard gun", 1),
        ("data/ships/privateer-schooner.yaml", "the long Tom", 1),
        ("data/ships/cutter.yaml", "the upper deck", 6),
    ],
)
def test_the_words_that_named_guns_before_name_the_same_and_a_bare_place_none(path, words, n):
    """§12.5: every phrase `guns_named` answered before answers the same (the tests' own phrases
    and the module's, re-run on every file before B7.b and after: none moved, measured); the
    quarterdeck and the forecastle said bare are places of the ship and name no gun, as before;
    a deck a ship has not names none."""
    from freesail.orders.gunnery import guns_named

    assert len(guns_named(load_ship(path), words)) == n


def test_fire_the_starboard_lower_deck_fires_it_by_name_and_a_ship_without_one_refuses():
    """B7.b item 5 through the order: at quarters, her guns cast loose and a mark engaged to
    starboard, "fire the starboard lower deck" puts her fourteen starboard 32-pounders to fire each
    as soon as it is ready, by name, and the reply says the deck; the frigate-36, which has no
    lower deck, refuses it in words, as before."""
    from freesail.combat.guns import battery_of
    from tests.test_brains import world_at

    for path, kind in ((SEVENTY_FOUR, "guns.fire"), (FRIGATE, "order.rejected")):
        w = world_at(49.5, -5.5, path)
        w.run(10)
        w.submit("beat to quarters")
        w.run(5)
        w.submit("cast loose the guns")
        w.run(200)
        w.submit("engage a mark four cables on the starboard beam")
        said = w.submit("fire the starboard lower deck")
        assert said.kind == kind, said.text
        if path == SEVENTY_FOUR:
            assert said.text == (
                "The starboard lower-deck guns to fire each as soon as it is ready, 14 guns."
            )
            single = battery_of(w.ship).single
            assert len(single) == 14
            assert {(w.ship.guns[g].deck, w.ship.guns[g].side) for g in single} == {
                ("lower", "starboard")
            }
        else:
            assert "names no gun of hers" in said.text


def _cast_loose(path=SEVENTY_FOUR):
    """At quarters, seed 7, tests/test_brains.py's world, her guns cast loose and run out."""
    from tests.test_brains import world_at

    w = world_at(49.5, -5.5, path)
    w.run(10)
    w.submit("beat to quarters")
    w.run(5)
    w.submit("cast loose the guns")
    w.run(200)
    return w


def test_a_deck_fired_by_name_is_refused_in_dumb_show_as_the_broadside_is():
    """The review's mend (2026-11-10) to B7.b item 5: a deck is a broadside of it, so that while
    the battery exercises in dumb show ("no shot leaves the ship") "fire the starboard lower deck"
    is refused as "fire the starboard broadside" is, and no gun fires; a gun by name still goes,
    as the module allows. Before the mend the deck went by the named-gun path and fourteen
    32-pounders fired live (measured)."""
    from freesail.combat.guns import battery_of

    w = _cast_loose()
    assert w.submit("exercise the great guns").kind != "order.rejected"
    broadside = w.submit("fire the starboard broadside")
    assert broadside.kind == "order.rejected" and "dumb show" in broadside.text
    said = w.submit("fire the starboard lower deck")
    assert said.kind == "order.rejected", said.text
    assert said.text == (
        "Order not carried out ('fire the starboard lower deck'): The battery is exercising in "
        "dumb show: no deck is fired at the word; say 'cease exercising' first."
    )
    assert battery_of(w.ship).single == []
    t0 = w.clock.tick
    w.run(300)
    assert not [e for e in w.log if e.tick > t0 and e.text.startswith("Fired")]


def test_a_deck_said_without_a_side_is_the_engaged_sides_and_refused_with_none():
    """The review's mend (2026-11-10): a deck said without a side is the engaged side's, as
    "fire" alone is, and the reply names the side ("fire the gun deck", engaged to starboard:
    her fourteen starboard 32-pounders, where before the mend it promised 28 and the larboard
    guns fired at the mark through her); with no side engaged it is refused in words.
    `guns_named` still names both sides (the director's slots)."""
    from freesail.combat.guns import battery_of
    from freesail.orders.gunnery import guns_named

    w = _cast_loose()
    none = w.submit("fire the lower deck")
    assert none.kind == "order.rejected", none.text
    assert none.text == (
        "Order not carried out ('fire the lower deck'): Fire the lower-deck guns of which side? "
        "No side is engaged: say 'fire the starboard lower-deck guns', or 'engage her to "
        "starboard' first."
    )
    assert battery_of(w.ship).single == []
    w.submit("engage a mark four cables on the starboard beam")
    said = w.submit("fire the gun deck")
    assert said.kind == "guns.fire", said.text
    assert said.text == "The starboard gun-deck guns to fire each as soon as it is ready, 14 guns."
    single = battery_of(w.ship).single
    assert {(w.ship.guns[g].deck, w.ship.guns[g].side) for g in single} == {("lower", "starboard")}
    assert len(single) == 14
    assert len(guns_named(w.ship, "the gun deck")) == 28


def test_a_deck_fired_to_leeward_leaves_out_the_guns_behind_shut_ports_and_says_so():
    """The review's mend (2026-11-10): heeled by hand 12.5 degrees to starboard, engaged to
    starboard, the sea shuts eight of her starboard lower ports (Nos. 4 to 11, truth 7-195's
    rule); "fire the starboard lower deck" puts the six open guns to fire and says the eight
    once, where before the mend the reply counted fourteen and the log said each shut port in a
    line of its own; heeled 20 degrees, all fourteen shut, the order is refused in the
    broadside's words."""
    from freesail.combat import action, ports
    from freesail.combat.guns import battery_of

    w, _said, _q = _beaten(SEVENTY_FOUR, heel_deg=12.5, engaged="starboard")
    b = battery_of(w.ship)
    shut = {g for g in b._shut if w.ship.guns[g].deck == "lower"}
    assert len(shut) == 8
    said = w.submit("fire the starboard lower deck")
    assert said.kind == "guns.fire", said.text
    assert said.text == (
        "The starboard lower-deck guns to fire each as soon as it is ready, six guns; eight are "
        "behind ports the sea has shut."
    )
    assert len(b.single) == 6 and not set(b.single) & shut
    b.single.clear()
    w.ship.dyn.heel = math.radians(20.0)
    ports.update(b, action._firer(w, w.ship), w.clock.tick)
    every = w.submit("fire the starboard lower deck")
    assert every.kind == "order.rejected", every.text
    assert every.text == (
        "Order not carried out ('fire the starboard lower deck'): The starboard lower-deck guns' "
        "ports are shut; the sea is at their sills."
    )
    assert b.single == []


# ---------------------------------------------------------------------------
# Her tack at quarters (B7.c: Bel-D §6.7, §12.5; her road's step 7)
# ---------------------------------------------------------------------------

# At the order to tack in truth 7-136's world (seed 7, 15 kn, close-hauled on the starboard tack
# at 292.5 degrees, 04:22 ship's time: the starboard watch on deck, the idlers below), the guns
# run out: one watch, the tack's party; the hands idle at their quarters; the hands lent under
# `sail before guns` (measured on B7.c). Before it each lent half of every crew (175, 135 and 22
# hands) and the tack wanted every fit hand aboard (574, 477 and 113).
TACK_AT_QUARTERS = {
    SEVENTY_FOUR: (268, 196, 72),
    SIXTY_FOUR: (218, 181, 39),
    "data/ships/brig.yaml": (48, 61, 0),
}


def _close_hauled_at_quarters(path, priority):
    """Truth 7-136's world at quarters, the guns run out under the priority given."""
    from tests.test_known_truths import _guns_ready, close_hauled_on_starboard

    w = close_hauled_on_starboard(path, heading=292.5)
    _guns_ready(w)
    w.run(40)
    w.submit("run out the guns")
    assert w.submit(priority).kind == "guns.priority"
    w.run(120)
    return w


@pytest.mark.parametrize("priority", ["sail before guns", "guns before sail"])
@pytest.mark.parametrize("path", list(TACK_AT_QUARTERS))
def test_a_tack_at_quarters_takes_one_watch_the_guns_giving_only_the_rest(path, priority):
    """Bel-D §6.7, B7.c: an all-hands manoeuvre at quarters is worked first by the hands idle at
    their quarters and takes from the guns, by the robbing order of §6.4 (whole crews from the end
    that bears least, her lower deck last), only what its party wants beyond them; its party the
    hands the same work takes at sea in one watch. Under `guns before sail` nothing is lent and the
    tack goes short of its party, said; where the idle hands are a watch (the brig's 61), nothing
    is lent under either and the tack is not short."""
    watch, idle, lent = TACK_AT_QUARTERS[path]
    w = _close_hauled_at_quarters(path, priority)
    t0 = w.clock.tick
    said = w.submit("tack ship")
    assert said.kind == "order.accepted", said.text
    tack = next(i for i in w.ship.extra["evolutions"].instances if i.evo.id == "tack")
    got = tack.assignment
    assert (got.party, got.wanted) == (watch, watch)
    w.run(1)  # the ship's lines reach the log at the tick
    robbed = [e for e in w.log if e.tick > t0 and e.kind == "quarters.robbed"]
    short = [e for e in w.log if e.tick > t0 and e.kind == "evolution.short_handed"]
    if priority == "sail before guns" and lent:
        assert [e.data["hands"] for e in robbed] == [lent], [e.text for e in robbed]
        assert watch - idle <= lent
        assert "half of each crew" not in robbed[0].text and "lower deck" not in robbed[0].text
        assert (got.got, got.outcome, short) == (watch, "enough", [])
    elif idle >= watch:
        assert (robbed, short, got.got, got.outcome) == ([], [], watch, "enough")
    else:
        assert not robbed
        assert (got.got, got.outcome) == (idle, "short")
        assert [(e.data["hands_got"], e.data["hands_wanted"]) for e in short] == [(idle, watch)]


def test_her_tack_at_quarters_under_sail_before_guns_is_her_cleared_tack():
    """Bel-D §6.7, B7.c, measured in truth 7-136's world: cleared she tacks in 243 s; at quarters
    under `sail before guns`, her party of one watch made up from the guns (72 hands, the poop's,
    the upper deck's and the quarterdeck's after crews), in 243 s too, her crew factor 1.0 through
    the tack. Before B7.c she lent half of every crew (175 hands) and took 386 s, 1.59 times."""
    from tests.test_known_truths import close_hauled_on_starboard, until

    def tacked(w):
        w.submit("tack ship")
        done, seconds = until(w, ("ship.tacked", "ship.missed_stays"), 1200)
        assert done and done[0].kind == "ship.tacked", [e.text for e in done]
        return seconds

    cleared = tacked(close_hauled_on_starboard(SEVENTY_FOUR, heading=292.5))
    at_quarters = tacked(_close_hauled_at_quarters(SEVENTY_FOUR, "sail before guns"))
    assert 210 <= cleared <= 300, cleared
    assert at_quarters <= cleared * 1.05, f"{at_quarters} s against {cleared} s cleared"


# ---------------------------------------------------------------------------
# Truth 7-195: her lower-deck ports shut at the heel the sources give (Bel-D §14.3; step 6)
# ---------------------------------------------------------------------------

# Her lee lower-deck ports shut by the count the rule gives at heels raised from upright, each
# heel 0.3 degree or more from every one of her lower ports' thresholds (Bel-D §14.3's
# knife-edges): §7.1's arithmetic on her file, the side at each sill her drawn half-breadth (task
# 4, re-traced at the review of 2026-11-10), measured: L7 (No. 8) 10.35, L6 (No. 7) 10.42, Nos. 6
# and 9 10.67 and 10.72, Nos. 10 and 5 11.16 and 11.17, Nos. 11 and 4 11.72 and 11.86, Nos. 12 and
# 3 12.89 and 12.94, Nos. 13 and 2 14.58 and 14.64, Nos. 14 and 1 18.90 and 18.98 degrees (before
# the re-trace 10.38, 10.45, 10.68, 10.78, 11.24 and 11.20 for the first six); her upper deck's
# lowest 32.37. Bel-D
# §14.3's counts on the midship figure (none at 10.0, nine at 12.35, eleven at 13.2, thirteen at
# 14.2, all fourteen at 15.2) were before task 4 measured the ends, which shut later: old beside
# new.
LEE_LOWER_SHUT_AT = ((10.0, 0), (12.4, 8), (13.7, 10), (16.0, 12), (19.4, 14))
ROLL_DEG = 4.0  # truth 7-190's roll (`ROLL_SET_DEG`): a ship "rolling", short of heavily


def _in_her_sea():
    """Truth 7-190's world (tests/test_lee_ports.py): her file as the player's ship, her default
    fit, a World that keeps a sea in six knots at seed 7, so that she has her motion; her heel and
    her roll set by the test's hand on the World's own names."""
    from freesail.api.session import make_world
    from freesail.core.world import Scenario

    w = make_world(
        7,
        SEVENTY_FOUR,
        Scenario(
            wind_from_deg=0.0,
            wind_speed_kn=6.0,
            gustiness=0.0,
            variability=0.0,
            ship_heading_deg=90.0,
            ship_speed_kn=0.0,
            sea=True,
        ),
    )
    assert w.motion is not None and w.ship.extra["motion"] is w.motion
    assert w.ship.fit == FIT_1795
    return w


def _ports_at(w, heel_deg, roll_deg, tick):
    """Her ports as the rule reads them at this heel (to starboard) and this roll, both set on
    `ship.dyn.heel` and `world.motion` and read through `action._firer`, at a tick of the test's
    own (the minute's hold counts in ticks): the guns shut."""
    from freesail.combat import action, ports
    from freesail.combat.guns import battery_of

    w.ship.dyn.heel = math.radians(heel_deg)
    w.motion.roll_deg = roll_deg
    battery = battery_of(w.ship)
    ports.update(battery, action._firer(w, w.ship), tick)
    return battery._shut


def _hold_ticks():
    from freesail.combat import ports
    from freesail.core.clock import TICK_SECONDS

    return round(ports.PORT_HOLD_S / TICK_SECONDS)


def test_truth_7_195_her_lowest_lower_deck_port_shuts_at_the_bellonas_heel():
    """**A draft, for Phase 5 to move into `tests/test_known_truths.py` and measure again on the
    merged tree** (Build-Ships.md §15, row 7-195; Bel-D §14.3, in truth 7-190's form): "her lower
    deck's 32-pounders and their ports' sills against the heel" (the brief, item 3). The
    Bellona's lowest gun-deck port 5 ft 2 in above the water at her best Channel draught (Lavery
    1985 p. 9, Table 2), her own lowest sill (L7, the lower deck's pair No. 8 at x -2.15 m, found
    by its triple, the least sill, never by its number) 1.57 m on her drawn side of 7.04 m: by
    `shot.lee_port_shut` it is open at 9.9 degrees of heel alone and shut at 10.9, its threshold
    10.35 (within 10.2-10.7: Bel-D's 10.35 on 7.04, the dead flat re-traced on its own line at the
    review of 2026-11-10, 10.38 on 7.02 before it; 10.58 the source's 5 ft 2 in on the moulded
    22.7 ft, the brief's 10.6; the lead's answer (11)). On her battery, raised from upright: open
    at 9.9, shut at 10.9 with the four ports whose thresholds lie under it; still shut at 9.9 on
    the way down, within the minute's hold and once it has run (the six inches to reopen: below
    9.11); open at 8.6, the minute run. **A roll's amplitude sooner** (the owner's rule, Bel §13.1
    answer 7): with a roll of 4 degrees on her motion it is open at 5.8 degrees of heel and shut at
    6.9. **The
    log:** "The lee lower-deck ports are shut, the sea at their sills." once at the change, her
    guns cast loose. Her weather side open throughout. Measured at seed 7 on the owner's machine,
    2026-11-10.

    **Recorded, not pinned (Bel-D §14.3's condition): in ordinary sailing**, close-hauled six
    points off under plain sail, no book, a steady wind with no gusts: her heel settles at 7.73
    degrees in 22 kn, 9.23 in 24 and 16.55 at its most in 32 (measured); but in 24 kn the setting
    of sail heels her to 10.72 for a moment, the two lowest ports shut and stay shut at the steady
    9.23 (they reopen below 9.11 and 9.18), so "open at 24 kn" does not hold with a degree's
    margin; in 23 kn she peaks at 9.88 and none shuts; in 32 kn twelve of the fourteen are shut.
    In the World's gusts at 24 kn (answer 8's "or in gusts at 24 kn") a lee lower port of hers is
    shut for 31% of the hour, her heel 6.9 to 16.3 degrees (measured again on her re-traced side,
    2026-11-10: one port and 30% before). The period's own cases are swell and rolling, not
    steady heel (the Blenheim, the Monarch, the Droits de l'Homme: Bel §6.1), which the roll's
    clause serves."""
    from freesail.combat import shot

    w = _in_her_sea()
    ship = w.ship
    x, sill, half = min(ports_of(ship.hull.spec.profile, "lower"), key=lambda t: t[1])
    assert x == pytest.approx(-2.15, abs=0.005)
    assert not shot.lee_port_shut(sill, 9.9, half)
    assert shot.lee_port_shut(sill, 10.9, half)
    threshold = math.degrees(math.asin((sill - shot.PORT_SHUT_M) / half))
    assert 10.2 <= threshold <= 10.7, threshold
    (lowest,) = [
        g.id
        for g in ship.guns.values()
        if g.deck == "lower" and g.side == "starboard" and (g.x_m, g.height_m) == (x, sill)
    ]
    for g in ship.guns.values():
        g.cast_loose = True
        g.run_out = True
    ship.drain_notes()
    hold = _hold_ticks()
    assert not _ports_at(w, 0.0, 0.0, 0)
    assert lowest not in _ports_at(w, 9.9, 0.0, 1)
    shut = _ports_at(w, 10.9, 0.0, 2)
    assert lowest in shut and len(shut) == 4
    assert all(ship.guns[g].deck == "lower" and ship.guns[g].side == "starboard" for g in shut)
    lines = [n for n in ship.drain_notes() if len(n) == 5 and n[1] == "guns.ports_shut"]
    assert [n[2] for n in lines] == ["The lee lower-deck ports are shut, the sea at their sills."]
    assert _ports_at(w, 9.9, 0.0, 3) == shut  # down again within the minute
    assert _ports_at(w, 9.9, 0.0, 3 + hold) == shut  # the minute run, the six inches not cleared
    assert not [n for n in ship.drain_notes() if len(n) == 5 and n[1] == "guns.ports_shut"]
    assert not _ports_at(w, 8.6, 0.0, 4 + hold)  # six inches clear and the minute run: open
    # a roll's amplitude sooner, raised from upright
    at = 10 + 3 * hold
    assert not _ports_at(w, 0.0, 0.0, at)
    assert lowest not in _ports_at(w, 5.8, ROLL_DEG, at + 1)
    assert lowest in _ports_at(w, 6.9, ROLL_DEG, at + 2)


def test_truth_7_195_her_lee_lower_deck_guns_shut_by_the_rules_count():
    """Truth 7-195's battery clause (Bel-D §14.3; a draft for Phase 5, as above): her default fit,
    her guns cast loose and run out, heeled to starboard by hand and raised from upright, so that
    the six inches of reopening do not bite; at heels each 0.3 degree or more from every one of
    her lower ports' thresholds (`LEE_LOWER_SHUT_AT`), `Battery._shut` holds her lee lower-deck
    guns in the counts the rule gives: none at 10.0, eight at 12.4, ten at 13.7, twelve at 16.0,
    all fourteen at 19.4. No upper-deck gun is shut below 25 degrees (her lowest upper port's
    threshold 32.37), nor any of the quarterdeck's, the forecastle's or the poop's, and the
    weather side stands open."""
    w = _in_her_sea()
    for g in w.ship.guns.values():
        g.cast_loose = True
        g.run_out = True
    assert not _ports_at(w, 0.0, 0.0, 0)
    for tick, (heel, count) in enumerate(LEE_LOWER_SHUT_AT, start=1):
        shut = _ports_at(w, heel, 0.0, tick)
        lee_lower = [g for g in shut if w.ship.guns[g].deck == "lower"]
        assert len(lee_lower) == count, (heel, len(lee_lower))
        assert all(w.ship.guns[g].side == "starboard" for g in shut), heel
        assert len(shut) == count, heel  # no gun of another deck
    shut = _ports_at(w, 25.0, 0.0, len(LEE_LOWER_SHUT_AT) + 1)
    assert {w.ship.guns[g].deck for g in shut} == {"lower"} and len(shut) == 14


# ---------------------------------------------------------------------------
# Truth 7-196: a 74 crewed holds the floors (Bel-D §14.4; step 6), routed as pace tests
# ---------------------------------------------------------------------------

# Her world off the Lizard (Bel-D §14.4): the frigate about three miles south of the Lizard
# (49.959 N 5.207 W, data/charts/features/channel-west.yaml), and the 74s one to three miles from
# her (settled by measurement: within the crewed range at the end of each timed thousand)
OFF_THE_LIZARD = (49.9, -5.21)
SEVENTY_FOURS_AT = ("49 55.5 N 5 12.0 W", "49 53.5 N 5 14.0 W", "49 52.5 N 5 11.0 W")


@pytest.mark.pace
def test_truth_7_196_a_seventy_four_crewed_holds_the_crewed_floor():
    """**A draft, for Phase 5 to move into `tests/test_known_truths.py`** (Build-Ships.md §15, row
    7-196; Bel-D §14.4): "the pace of a 74 crewed measured against the floors" (the brief, item 3).
    Truth 88's form (tests/test_crews.py), marked `pace` by hand as truths 88 and 7-138 are, so
    that tests/conftest.py routes it to the pace run, alone after the rest. **Its place differs
    from truth 88's:** truth 88's frigate lies at 49 30 N 5 30 W, about thirty miles from the
    Lizard, where 74s keeping a station off the Lizard would sail for it and pass the crewed
    range's demotion within the measure; here the frigate lies about three miles south of it,
    her plain sail set and then hove to (truth 88's "heave to" at the first tick is refused, no
    sail being set: Bel-D §18 item 20), and three 74s of her file are put one to three miles from
    her, keeping the station off the Lizard; a thousand ticks to settle, then the best of three
    timed thousands, at the end of each the crewed ships at `CREWED_CAP` and every 74 within
    `CREWED_NM` of her. At least `CREWED_FLOOR_TICKS_S` (60) a second on the build machine.
    Measured on the owner's machine (seed 7, 2026-11-10): 106 ticks a second, the 74s at 0.25 to
    3.59 miles. **Plainly:** they do not keep their places but engage her: the frigate of this
    world carries no private signal (truth 88's world has no table aboard her), so their challenge
    goes unanswered, and a man of war under their own colours that does not answer is an enemy by
    the King's ship's book (world/signalling.py, package 71's rule), which fires into her; the
    load is three crewed 74s in action, more than on their station."""
    import time

    from freesail.world import crews as K
    from freesail.world.geo import bearing_and_distance
    from tests.test_brains import put, world_at

    w = world_at(*OFF_THE_LIZARD)
    w.submit("set plain sail")
    w.run(900)
    assert w.submit("heave to").kind == "order.accepted"
    goal = "patrolling off the Lizard within 2 miles"
    intent = "keep the station off the Lizard within 2 miles"
    fours = [
        put(w, "seventy-four", "britain", where, goal, intent, name=f"S{i}")
        for i, where in enumerate(SEVENTY_FOURS_AT)
    ]
    assert all(v.ship_file == SEVENTY_FOUR for v in fours)
    w.run(1000)
    best = 0.0
    for _ in range(3):
        t0 = time.perf_counter()
        w.run(1000)
        best = max(best, 1000 / (time.perf_counter() - t0))
        assert len(w.vessels.crewed_ids) == K.CREWED_CAP
        for v in fours:
            nm = bearing_and_distance(w.position, v.position)[1] / units.NAUTICAL_MILE
            assert nm <= K.CREWED_NM, (v.name, nm)
    assert best >= K.CREWED_FLOOR_TICKS_S, f"{best:.0f} ticks a second"


def test_truth_7_196_the_seventy_four_ticks_at_the_build_machines_floor():
    """Truth 7-196's clause alone (Bel-D §14.4; a draft for Phase 5, as above), routed to the pace
    run by its name (tests/conftest.py): truth 51's form with her file in the frigate's place, the
    gate's day from its scenario file (its book and first orders), a thousand ticks to settle and
    the best of three thousands, at least `BUILD_MACHINE_FLOOR` (500) on the build machine. **Pinned
    only if the lead's measurement on the build machine at her merge leaves a tenth's margin (550
    or more); else recorded and reported, and no floor lowered** (the lead's answer (5)). Measured
    on the owner's machine (2026-11-10), four runs: 474, 477, 483 and 490 ticks a second, under the
    floor there (the frigate-36 505 and 631 and the 64 484 and 486 in the same form and runs), so
    this clause fails on that machine as it stands, for the lead's build machine to settle."""
    import time

    from freesail.world.scenarios import begin, load_scenario, make_scenario_world
    from tests.test_known_truths import BUILD_MACHINE_FLOOR, GATE_DAY

    sf = load_scenario(GATE_DAY)
    world = make_scenario_world(sf, ship=SEVENTY_FOUR)
    begin(world, sf)
    assert world.ship.fit == FIT_1795
    world.run(1000)
    best = 0.0
    for _ in range(3):
        t0 = time.perf_counter()
        world.run(1000)
        best = max(best, 1000 / (time.perf_counter() - t0))
    assert best >= BUILD_MACHINE_FLOOR, f"{best:.0f} ticks a second"
