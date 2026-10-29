"""Package 75, the first ship (B1): HMS Indefatigable, the 64 of 1784 and the razee of 1795.

Her design is docs/design/Design-Ship-Indefatigable.md (Indf), from the research note
docs/design/Research-Indefatigable-2026-10.md (Ind); `tools/ships/indefatigable.py` writes both
files, `data/ships/sixty-four.yaml` and `data/ships/razee-44.yaml`, the razee derived from the 64
as data (Indf §1.5). These are her tests (Indf §14; Build-Ships.md §14.1), in the band form of
tests/test_ship_particulars.py with the source of each band in a comment: her two hulls, profiles
and sills against the measured lines; her spars against Steel 1794 vol. I p. 49 and her sails
against Steel's table IV; her guns, fits, crews, exercise and filling against Winfield, James, Adye,
Falconer and the Regulations; her company, posts and marines against the Regulations' columns and
her wardroom files; her ground tackle against Steel's 64; her descriptions and size ranks; her
names; her polars in tests/test_ships.py's form; and her round trip under the rules captains at
seed 7 with no fit named (Indf §11.2).

Her truths are drafted here under their numbers (Build-Ships.md §15), to be moved into
tests/test_known_truths.py in Phase 5 and measured again there: 7-186 her particulars, 7-187 the
razee lighter, stiffer and faster than the 64, 7-188 her broadside against the frigate-36's. Each
is written against the names the Hull keeps (`world.ship`; Design-OneWorld §2.2). Truth 7-189,
the 64's handling with her mizen yard and spritsails, is stage B's.

**Stage A.** The 64 sails on her stand-in mizen course with no yards under the bowsprit (Indf
§0): her rig's figures here are pinned on the stand-in, and measured again, old beside new, when
stage B flips `MIZEN_COURSE`, `BOWSPRIT_YARDS` and the driver. The razee is final.

The figures quoted as measured were measured at seed 7 on the owner's machine (Windows 11,
2026-10-28); the bands are the sources' or judgement where they say so.
"""

from __future__ import annotations

import copy
import math
from collections import Counter
from pathlib import Path

import pytest
import yaml

from freesail import units
from freesail.orders.resolve import noun_table
from freesail.ship.loader import load_ship, load_spec
from freesail.ship.profile import deck_at, half_breadth_at_sill, interp, ports_of, sill_at

ROOT = Path(__file__).resolve().parents[1]
SIXTY_FOUR = "data/ships/sixty-four.yaml"
RAZEE = "data/ships/razee-44.yaml"
FRIGATE = "data/ships/frigate-36.yaml"
FT = units.FOOT
SQ_FT = FT * FT
CWT_KG = 50.80234544  # the hundredweight of 112 lb

# Her load line against the 64's: ZAZ2371's drawn line 1.45 ft below WL1 aft and 1.47 ft forward
# (measured, 2371 against 1407F, ±0.25 ft: Ind §2.3.1; D28 (a)), 0.44 m to the centimetre.
RISE_M = 0.44
# The lower masts cut at the heel (D19 (a)): the fore 6 ft 3 in, the main 6 ft 7 in, the mizzen
# 6 ft 9 in, the height of the deck taken off at each (measured on 1280T: Ind §3.3).
CUT_FT = {"fore": 6.25, "main": 6.0 + 7.0 / 12.0, "mizzen": 6.75}


@pytest.fixture(scope="module")
def sixty_four():
    return load_ship(SIXTY_FOUR)


@pytest.fixture(scope="module")
def razee():
    return load_ship(RAZEE)


def area_of(ship, group):
    return sum(ship.sails[i].area_m2 for i in ship.groups[group])


def above_water(ship, spar_id):
    """A spar's height above her water: the file's height above the datum and the datum."""
    return ship.spars[spar_id].height_m + ship.hull.spec.deck_height_m


def guns_by(fit):
    """A fit's guns counted by (kind, pounder, deck)."""
    return Counter((g.kind, int(g.pounder), g.deck) for g in fit.guns)


# ---------------------------------------------------------------------------
# Her hulls (Indf §2.1)
# ---------------------------------------------------------------------------


def test_the_64s_hull_is_the_ardent_class_64_as_drawn(sixty_four):
    h = sixty_four.hull.spec
    # 160 ft on WL1 rabbet to rabbet (measured, ZAZ1407: Ind §2.3.2; D29 (b)); 160 ft 1 1/4 in on
    # the gun deck (Winfield 1793-1817 p. 100)
    assert 159.0 <= units.m_to_feet(h.length_waterline_m) <= 161.0
    assert 13.4 <= h.beam_m <= 13.6  # 44 ft 5 in extreme as built (Winfield p. 100; D34 (a))
    # 20 ft 9 in mean to K at WL1 (measured, 1407F: Ind §2.3.1); Steel's 64 of Folio I draws
    # 20 ft 8 in abaft and 19 ft 4 in afore
    assert 6.2 <= h.draught_m <= 6.45
    # the band integrated on her measured lines, 2,120-2,240 t (Ind §2.3.3)
    assert 2_120_000 <= h.displacement_kg <= 2_240_000
    assert 1.2 <= h.gm_m <= 1.5  # Ind §2.3.4: KM measured 7.3 m above K, her KG judgement
    assert 12.5 <= h.hull_speed_kn <= 13.0  # D24 (a): the 64 below the razee, judgement
    # before the centroid of her plane (0.55 m abaft the middle: Ind §2.3.6), within an eighth
    # of her load line ahead of the middle (judgement; tuned against truths 6 and 17)
    assert 0.0 <= h.clr_x_m <= h.length_waterline_m / 8.0
    # the plane below WL1 with the band, the rudder left out: 3,288-3,290 sq ft (measured, 1407F)
    assert 3_280 <= h.lateral_area_m2 / SQ_FT <= 3_300
    # the datum, D18 (a): her upper deck at midships, 10 ft 7 in above WL1 (measured, 1280T)
    assert h.deck_height_m == pytest.approx((10.0 + 7.0 / 12.0) * FT, abs=0.02)
    # her rudder, 95.4-96.9 sq ft below WL1 (measured, 1407F: Ind §2.3.6)
    assert 95.0 <= h.rudder.area_m2 / SQ_FT <= 97.0


def test_the_razees_hull_is_the_64s_at_her_own_line(sixty_four, razee):
    h, h64 = razee.hull.spec, sixty_four.hull.spec
    # the cut took nothing off her length or her breadth (D29 (b), D34 (a))
    assert h.length_waterline_m == h64.length_waterline_m and h.beam_m == h64.beam_m
    # 19 ft 3 in mean to K at ZAZ2371's line (measured: Ind §2.3.1); Osler's "nineteen and a
    # half feet abaft" (p. 111, May 1795) within that line's ±0.25 ft
    assert 5.75 <= h.draught_m <= 6.0
    assert 1_900_000 <= h.displacement_kg <= 1_955_000  # Ind §2.3.3's band at her line
    assert 1.5 <= h.gm_m <= 1.8  # Ind §2.3.4: her KG about a foot lower, judgement
    # D24 (a): the frigate-36's 13.0 carried by the root of the lengths, tuned within 13-14.5,
    # and above the 64's (the decision's ranking, the two hulls one length)
    assert 13.0 <= h.hull_speed_kn <= 14.5 and h.hull_speed_kn > h64.hull_speed_kn
    assert 0.0 <= h.clr_x_m <= h.length_waterline_m / 8.0  # as the 64's (judgement; tuned)
    # her plane at her line, 3,050-3,052 sq ft (measured, 1407F 1.45 ft below WL1)
    assert 3_040 <= h.lateral_area_m2 / SQ_FT <= 3_060
    # her datum, D18 (a): her gun deck at midships, 4 ft 7 in above her line (the 64's lower
    # deck, measured on 1280T; 4 ft 5 in-4 ft 8 in on ZAZ2371: Ind §2.3.5)
    assert (4.0 + 5.0 / 12.0) * FT <= h.deck_height_m <= (4.0 + 8.0 / 12.0) * FT
    assert 90.0 <= h.rudder.area_m2 / SQ_FT <= 92.0  # 90.4-91.8 sq ft below her line


# ---------------------------------------------------------------------------
# Her profiles and sills (Indf §3; the measuring of §3.5)
# ---------------------------------------------------------------------------


def test_the_64s_profile_holds_her_measured_sills_rail_and_decks(sixty_four):
    p = sixty_four.hull.spec.profile
    # her gun deck: thirteen ports a side, every sill measured on ZAZ1407 at full resolution
    # (Indf §3.5 item 1), 6.09 ft above WL1 at the aftmost, 5.02 at the seventh, 6.03 forward
    lower = ports_of(p, "lower")
    assert len(lower) == 13
    sills = [z for _x, z, _hb in lower]
    assert min(sills) == pytest.approx(5.02 * FT, abs=0.01) == sills[6]
    assert sills[0] == pytest.approx(6.09 * FT, abs=0.01)
    assert sills[-1] == pytest.approx(6.03 * FT, abs=0.01)
    assert all(a > b for a, b in zip(sills[:6], sills[1:7], strict=True))  # the sheer aft
    assert all(a < b for a, b in zip(sills[6:-1], sills[7:], strict=True))  # and forward
    # the side at the midship sill: 21.52 ft moulded and the plank, 6.67 m (Indf §3.3), on the
    # half-breadth plan's measured main-breadth line (judgement on measured lines)
    assert 6.6 <= half_breadth_at_sill(p, "lower", 0.0) <= 6.75
    # the upper deck's thirteen, 11.67-12.96 ft above WL1, and the quarterdeck's six,
    # 18.11-19.14 ft (measured on 1407F at full resolution)
    upper, qd = ports_of(p, "upper"), ports_of(p, "quarterdeck")
    assert len(upper) == 13 and len(qd) == 6
    assert min(z for _x, z, _hb in upper) == pytest.approx(11.67 * FT, abs=0.03)
    assert max(z for _x, z, _hb in upper) == pytest.approx(12.96 * FT, abs=0.03)
    assert min(z for _x, z, _hb in qd) == pytest.approx(18.11 * FT, abs=0.03)
    assert max(z for _x, z, _hb in qd) == pytest.approx(19.14 * FT, abs=0.03)
    # her gun-deck ports 3 ft 3 in by 2 ft 8 in (measured: 3.27 by 2.66 ft the mean)
    size = dict(p.port_size_m)["lower"]
    assert size == pytest.approx((3.27 * FT, 2.66 * FT), abs=0.01)
    # the taffrail 13 ft abaft AP and 28 ft above WL1, the stem head 160.8 ft from AP and 20 ft
    # above it (measured on 1407F); x forward of the middle of the load line, 80 ft from AP
    assert p.rail_m[0] == pytest.approx(((-13.0 - 80.0) * FT, 28.0 * FT), abs=0.01)
    assert p.rail_m[-1] == pytest.approx(((160.8 - 80.0) * FT, 20.0 * FT), abs=0.01)
    # her upper deck at midships is the datum, the uppermost continuous deck (D18 (a))
    decks = dict(p.decks_m)
    assert interp(decks["upper"], 0.0) == pytest.approx(sixty_four.hull.spec.deck_height_m)
    # every sill stands above its deck at its port
    for word, triples in p.ports_m:
        for x, z, _hb in triples:
            assert z > interp(decks[word], x), (word, x)


def test_the_razees_profile_is_the_64s_cut_down_at_her_own_line(sixty_four, razee):
    p64, p = sixty_four.hull.spec.profile, razee.hull.spec.profile
    # her gun deck is the 64's lower deck and its ports the 64's, raised by her rise
    gun_deck = ports_of(p, "upper")
    assert [(x, hb) for x, _z, hb in gun_deck] == [(x, hb) for x, _z, hb in ports_of(p64, "lower")]
    # her midship sill against ZAZ2371's own measure, 6 ft 5 in above its line, 1.96 ±0.03 m
    # (Ind §2.3.7): the derivation's independent check (Indf §1.5)
    assert abs(sill_at(p, "upper", 0.0) - 1.96) <= 0.03
    # her old upper deck at midships, 12 ft 0 in above her line (measured, 2371 and 1280T)
    old_upper = interp(dict(p64.decks_m)["upper"], 0.0) + RISE_M
    assert abs(old_upper - 3.66) <= 0.05
    decks = dict(p.decks_m)
    # her quarterdeck the old upper deck to its breast at 74.4 ft from AP, her forecastle from
    # 118.5 ft (measured, ZAZ2375: Ind §2.3.5); the waist between them open but for gangways
    assert decks["quarterdeck"][-1][0] == pytest.approx((74.4 - 80.0) * FT, abs=0.01)
    assert decks["forecastle"][0][0] == pytest.approx((118.5 - 80.0) * FT, abs=0.01)
    assert deck_at(p, 0.0) == pytest.approx(razee.hull.spec.deck_height_m, abs=0.01)
    # six ports a side on her quarterdeck and three on her forecastle (ZAZ2375, measured), and
    # her chase port before them for the 12-pounders of 1796 (D30 (a); judgement)
    assert len(ports_of(p, "quarterdeck")) == 6 and len(ports_of(p, "forecastle")) == 4
    # her taffrail 5 ft 6 in abaft AP (measured, ZAZ2375), her quarterdeck rail 4 ft 6 in above
    # her quarterdeck (Ind §2.3.5, not re-measured)
    assert p.rail_m[0][0] == pytest.approx((-5.5 - 80.0) * FT, abs=0.01)
    assert p.rail_m[0][1] - interp(decks["quarterdeck"], p.rail_m[0][0]) == pytest.approx(
        4.5 * FT, abs=0.02
    )
    # her waist's top-side, 30.8 ft above K (measured, ZAZ2371), more than a metre under the
    # 64's waist rail at midships (1407F)
    assert interp(p.rail_m, 0.0) < interp(p64.rail_m, 0.0) - 1.0


# ---------------------------------------------------------------------------
# Her spars (Steel 1794 vol. I p. 49, the 64 column; Indf §4.1-§4.2)
# ---------------------------------------------------------------------------

# Steel 1794 vol. I p. 49, "64 GUNS. 1369 TONS." (the page image read: Ind §3.1, Indf §4.1),
# feet: the yards of each mast, course (the mizzen's the crossjack), topsail, topgallant, royal.
STEEL_YARDS_FT = {
    "fore": (79.5, 57.5, 34.5, 28.5),
    "main": (90.0 + 4.0 / 12.0, 65.0 + 4.0 / 12.0, 39.0, 32.0),
    "mizzen": (57.5, 43.25, 29.0, 21.0),
}
# The lower masts (the same page), feet, and where they stand: at the lower-deck partners, ft
# from AP, their heels above K (measured on ZAZ1280: Ind §3.1). WL1 21.245 ft above K at AP, the
# keel dragging 1.04 ft over 160 ft (measured, 1407F: Ind §2.3.1).
STEEL_MASTS_FT = {"fore": 89.0 + 7.0 / 12.0, "main": 101.0, "mizzen": 86.0}
MAST_STEPS_FT = {"fore": (143.09, 9.67), "main": (70.87, 7.15), "mizzen": (26.42, 10.35)}


def test_her_spars_follow_steels_table_for_a_64(sixty_four, razee):
    for ship in (sixty_four, razee):
        sp = ship.spars
        for mast, lengths in STEEL_YARDS_FT.items():
            course = "mizzen.crossjack.yard" if mast == "mizzen" else f"{mast}.yard"
            ids = (course, f"{mast}.topsail.yard", f"{mast}.topgallant.yard", f"{mast}.royal.yard")
            for yard_id, ft in zip(ids, lengths, strict=True):
                # to the decimetre the file keeps
                assert sp[yard_id].length_m == pytest.approx(ft * FT, abs=0.06), yard_id
        # the bowsprit 60 ft 4 in, 46.3 ft of it outboard from its heel measured on ZAZ1280
        # (±1 ft); the jib-boom 43 ft 9 in, seven twelfths outboard (the frigate's rule)
        assert abs(units.m_to_feet(sp["bowsprit"].length_m) - 46.3) <= 1.0
        assert sp["jib_boom"].length_m == pytest.approx(43.75 * 7.0 / 12.0 * FT, abs=0.06)
        # the main topmast 58 ft 6 in, its hoist above the cap the length less the lower mast
        # head of five inches to every yard of the mast (Steel, OCR l. 4697-4699): 44 ft 6 in
        hoist_ft = 58.5 - 101.0 / 3.0 * 5.0 / 12.0
        assert sp["main.topmast"].height_m == pytest.approx(hoist_ft * FT, abs=0.06)
        # the main topsail yard 0.72 of the main yard by Steel's lengths
        assert 0.70 <= sp["main.topsail.yard"].length_m / sp["main.yard"].length_m <= 0.74
    # the 64's lower mast heads stand where Steel's lengths set up on the measured heels put
    # them: the head above WL1 the heel and the length less WL1 above K at the mast
    for mast, length in STEEL_MASTS_FT.items():
        x, heel = MAST_STEPS_FT[mast]
        head = (heel + length - (21.245 - 1.04 * x / 160.0)) * FT
        assert above_water(sixty_four, f"{mast}.mast") == pytest.approx(head, abs=0.06), mast
    # the main truck: Steel's lower mast, topmast and topgallant mast with its pole set up on
    # her measured heel, each doubling a head by Steel's rule, 47.1 m above her water
    truck = sum(s.height_m for s in sixty_four.spar_chain("main.royal_mast"))
    assert truck + sixty_four.hull.spec.deck_height_m == pytest.approx(47.1, abs=0.2)
    # her brace limits are the frigate-36's (Fincham 1843 art. 102; Indf §4.2, judgement): the
    # lee lower shrouds do not stop her lower yards before 70 degrees (measured on 1407F)
    frigate = load_ship(FRIGATE)
    for yard_id in ("fore.yard", "main.yard", "main.topsail.yard", "mizzen.topsail.yard"):
        assert sixty_four.spars[yard_id].brace_limit == frigate.spars[yard_id].brace_limit


# ---------------------------------------------------------------------------
# Her sails (Steel's table IV, the 64 column; Indf §4.3-§4.5)
# ---------------------------------------------------------------------------

# Steel's table IV, the 64 column (Steel 1794 vol. I p. *149, the page image read: Ind §5):
# cloths at the head and the foot and the depth in yards; 22 1/2 in a cloth in the sail.
CLOTH_FT = 22.5 / 12.0
STEEL_SQUARE = {
    "main.course": (41.5, 44.0, 14.0),
    "fore.course": (36.0, 34.0, 12.0),
    "main.topsail": (27.0, 43.0, 17.5),
    "fore.topsail": (23.0, 37.0, 15.75),
    "mizzen.topsail": (18.5, 27.0, 12.375),
}
STEEL_ABOVE_THE_CAPS = {
    "main.topgallant": (19.5, 27.5, 9.0),
    "fore.topgallant": (17.0, 24.0, 8.25),
    "mizzen.topgallant": (13.5, 19.5, 6.75),
    "main.royal": (15.0, 20.0, 7.0),
    "fore.royal": (13.0, 17.5, 6.25),
    "mizzen.royal": (10.0, 14.0, 5.0),
}
# The headsails: cloths in the foot and the leech in yards.
STEEL_HEADSAILS = {
    "fore.staysail": (19.0, 11.5),
    "fore.topmast_staysail": (18.0, 16.0),
    "jib": (24.0, 23.0),
}


def steel_m2(head, foot, depth_yd):
    return (head + foot) / 2.0 * CLOTH_FT * depth_yd * 3.0 * SQ_FT


def test_her_sails_follow_steels_table_iv(sixty_four, razee):
    for ship in (sixty_four, razee):
        areas = {s.id: s.area_m2 for s in ship.sails.values()}
        for sid, row in STEEL_SQUARE.items():  # the courses and topsails, ±10% (Indf §14)
            assert abs(areas[sid] / steel_m2(*row) - 1.0) <= 0.10, sid
        for sid, (foot, leech) in STEEL_HEADSAILS.items():  # triangles on their stays
            assert abs(areas[sid] / (foot * CLOTH_FT * leech * 3.0 / 2.0 * SQ_FT) - 1.0) <= 0.10
        # above the topmast caps the spars rule over the table (the owner's answer,
        # Build-Ships.md §19.1 item 5): each cut between its yard and the yard below, half to
        # three quarters of the table's sail (0.58-0.60 measured)
        for sid, row in STEEL_ABOVE_THE_CAPS.items():
            assert 0.5 <= areas[sid] / steel_m2(*row) <= 0.75, sid
        # the main topsail the largest sail, as the frigate-36's
        assert max(areas, key=areas.get) == "main.topsail"
        assert areas["main.course"] > areas["fore.course"] > areas["mizzen.topsail"]
    # the 64's mizen course, the stand-in on her mizen yard's after part (Indf §4.4): Steel's
    # 14 1/2 cloths at the head and 15 1/2 at the foot, its leeches 9 1/4 and 17 1/4 yards
    course = sixty_four.sails["mizzen.course"]
    steel = 15.0 * CLOTH_FT * (9.25 + 17.25) / 2.0 * 3.0 * SQ_FT
    assert abs(course.area_m2 / steel - 1.0) <= 0.10 and course.cls == "gaff"
    assert sixty_four.spars["mizzen.yard"].cls == "gaff"  # stage A; the gated class at stage B
    # the razee's spanker on her gaff of 40 ft 10 in and driver boom of 65 ft 4 in (Steel p. 40:
    # the boom the main topsail yard's length, the gaff five eighths of it; D20 (a)), about
    # 240 m2 by the frigate's rule (Indf §4.5, ±10%)
    assert razee.spars["mizzen.boom"].length_m == pytest.approx((65.0 + 4.0 / 12.0) * FT, abs=0.06)
    assert razee.spars["mizzen.gaff"].length_m == pytest.approx((40.0 + 10.0 / 12.0) * FT, abs=0.06)
    assert 216.0 <= razee.sails["mizzen.spanker"].area_m2 <= 264.0
    # plain sail: the 64's above the frigate-36's 1,584 m2 (a ship of 1,369 tons to her 930),
    # the razee's above the 64's by her spanker for the mizen course
    frigate = load_ship(FRIGATE)
    assert (
        area_of(frigate, "plain sail")
        < area_of(sixty_four, "plain sail")
        < area_of(razee, "plain sail")
    )
    assert 1_600 <= area_of(sixty_four, "plain sail") <= 1_900


# Her staysails between the masts in Steel's table IV, the 64 column (Ind §5), m2, and the band of
# Indf §4.3's check: ±10% the main staysail, a triangle; ±25% the four-sided ones, their areas
# an upper bound. Steel's 64 has no mizen topgallant staysail.
STEEL_BETWEEN = {
    "main.staysail": (102.0, 0.10),
    "main.topmast_staysail": (190.0, 0.25),
    "middle_staysail": (110.0, 0.25),
    "main.topgallant_staysail": (90.0, 0.25),
    "mizzen.staysail": (100.0, 0.25),
    "mizzen.topmast_staysail": (80.0, 0.25),
}


def test_her_staysails_between_the_masts_stand_against_steels_table_iv_as_recorded(
    sixty_four, razee
):
    """Indf §4.3: the helper's staysails between the masts (`between_the_masts`, the frigate's
    rules on her spars) checked against Steel's table IV. Four of the six fall outside the
    check's bands, measured: the main staysail +26% (the razee's +27%), the middle -29%, the
    mizzen -35% (-34%) and the mizzen topmast +40%; the main topmast +18% (+19%) and the main
    topgallant -11% lie within. They are kept as cut, each note saying so, open for the owner
    or the lead; this pins that state, so that a recut or a drift is seen."""
    for ship in (sixty_four, razee):
        between = ship.groups["staysails between the masts"]
        assert set(between) == set(STEEL_BETWEEN) | {"mizzen.topgallant_staysail"}
        outside = {
            sid
            for sid, (steel, band) in STEEL_BETWEEN.items()
            if abs(ship.sails[sid].area_m2 / steel - 1.0) > band
        }
        assert outside == {
            "main.staysail",
            "middle_staysail",
            "mizzen.staysail",
            "mizzen.topmast_staysail",
        }


# ---------------------------------------------------------------------------
# Her guns (Indf §5)
# ---------------------------------------------------------------------------

# Adye 1804 pp. 72 and 155 (D31 (a); Indf §5.3): the pieces' weights, cwt, by (kind, pounder);
# the 18-pounder at 40 cwt the 74's reading (the owner's answer). Their crews: Falconer 1780,
# QUARTERS (11, 9, 7, 6) and Douglas 1829 art. 136 (4 to any carronade) (D31 (c)).
ADYE_CWT = {
    ("long", 24): 49.5,
    ("long", 18): 40.0,
    ("long", 12): 34.0,
    ("long", 9): 24.5,
    ("carronade", 42): 22.25,
    ("carronade", 24): 13.0,
    ("carronade", 18): 9.0,
}
CREWS = {("long", 24): 11, ("long", 18): 9, ("long", 12): 7, ("long", 9): 6}


def test_her_fits_guns_and_crews_are_the_periods(sixty_four, razee):
    arm64, arm = sixty_four.spec.armament, razee.spec.armament
    # the 64's establishment as built (Winfield 1793-1817 p. 99): 26 x 24 on the gun deck,
    # 26 x 18 on the upper deck, 10 x 9 on the quarterdeck and 2 on the forecastle, 64 pieces;
    # and the class's of 1794, two 24-pounder and six 18-pounder carronades added (the same)
    assert arm64.default == "ardent class 1784"
    assert guns_by(arm64.fits["ardent class 1784"]) == {
        ("long", 24, "lower"): 26,
        ("long", 18, "upper"): 26,
        ("long", 9, "quarterdeck"): 10,
        ("long", 9, "forecastle"): 2,
    }
    assert guns_by(arm64.fits["ardent class 1794"]) == {
        **guns_by(arm64.fits["ardent class 1784"]),
        ("carronade", 24, "forecastle"): 2,
        ("carronade", 18, "roundhouse"): 6,
    }
    # the razee as razeed (Winfield p. 99), 44 pieces, and as carried from 1796, her default
    # (the owner's answer): 26 x 24, 18 x 42-pounder carronades and two long 12s as bow
    # chasers (James vol. 1 p. 361)
    assert arm.default == "as carried 1796"
    assert guns_by(arm.fits["as razeed 1795"]) == {
        ("long", 24, "upper"): 26,
        ("long", 12, "quarterdeck"): 8,
        ("carronade", 42, "quarterdeck"): 4,
        ("long", 12, "forecastle"): 4,
        ("carronade", 42, "forecastle"): 2,
    }
    carried = arm.fits["as carried 1796"]
    assert guns_by(carried) == {
        ("long", 24, "upper"): 26,
        ("carronade", 42, "quarterdeck"): 12,
        ("carronade", 42, "forecastle"): 6,
        ("long", 12, "forecastle"): 2,
    }
    assert sorted(g.place for g in carried.guns if g.pounder == 12) == ["bow", "bow"]
    for ship in (sixty_four, razee):
        profile = ship.hull.spec.profile
        for fit in ship.spec.armament.fits.values():
            numbers = [(g.number, g.side) for g in fit.guns if g.place == "broadside"]
            assert len(numbers) == len(set(numbers)), fit.name
            for g in fit.guns:
                key = (g.kind, int(g.pounder))
                assert g.weight_cwt == ADYE_CWT[key], (fit.name, g.id)
                assert g.crew == CREWS.get(key, 4), (fit.name, g.id)
                # every gun on a port of its own deck, to the centimetre (Build-Ships.md §4.4)
                assert any(
                    abs(g.x_m - x) <= 0.01 and abs(g.height_m - z) <= 0.01
                    for x, z, _hb in ports_of(profile, g.deck)
                ), (fit.name, g.id)
            # numbered from forward on each deck, and on across her decks (Indf §5.2)
            side = sorted(
                (g for g in fit.guns if g.place == "broadside" and g.side == "starboard"),
                key=lambda g: g.number,
            )
            for deck in {g.deck for g in side}:
                xs = [g.x_m for g in side if g.deck == deck]
                assert xs == sorted(xs, reverse=True), (fit.name, deck)
    # the exercise allowance, the Regulations 1806, the Gunner, Art. XXI (OCR l. 13118-13144:
    # Indf §5.4): a third of the upper deck's guns in a ship of two decks, the 64's 26; a
    # fourth in a ship of one, the razee's 26
    assert {f.exercise_charges for f in arm64.fits.values()} == {8}
    assert {f.exercise_charges for f in arm.fits.values()} == {6}
    # the filling room: the Regulations' quarter gunners of the 491 and 294 columns (p. 165)
    assert sixty_four.spec.crew.quarter_bill.filling == 16
    assert razee.spec.crew.quarter_bill.filling == 11
    # the charges by Table No. 29 as read (Indf §5.4): 24-pdr 8 lb, 18-pdr 6, 12-pdr 4, 9-pdr 3;
    # the 42-pdr carronade 3 1/2, the 24-pdr 2, the 18-pdr 1 1/2
    table = {("long", 24): 8.0, ("long", 18): 6.0, ("long", 12): 4.0, ("long", 9): 3.0}
    table.update({("carronade", 42): 3.5, ("carronade", 24): 2.0, ("carronade", 18): 1.5})
    for ship in (sixty_four, razee):
        for fit in ship.spec.armament.fits.values():
            for (kind, pounder), lb in (fit.charges or {}).items():
                assert lb == table[(kind, int(pounder))], (fit.name, kind, pounder)
            # sixty round, six grape and six chain a gun (the generator's `KINGS_ROUNDS`,
            # judgement after Lavery on the Ordnance's allowance of the 1790s)
            counts = Counter(int(g.pounder) for g in fit.guns)
            for pounder, shot in fit.shot.items():
                n = counts[int(pounder)]
                assert shot == {"round": 60 * n, "grape": 6 * n, "chain": 6 * n}, fit.name


# ---------------------------------------------------------------------------
# Her company, her wardroom, her ground tackle (Indf §6-§7)
# ---------------------------------------------------------------------------


def test_her_companies_hold_the_regulations_columns(sixty_four, razee):
    c64, c = sixty_four.spec.crew, razee.spec.crew
    # the 64: 491, the Regulations' column for a 64 (1806, p. 165; Winfield 1793-1817 p. 99 from
    # 1794); its five lieutenants and three master's mates; 84 marines, the column's captain,
    # two lieutenants, two serjeants, two corporals and a drummer with 76 privates (the
    # Bellona's share in 1761, Lavery 1985 p. 17; judgement the owner accepted)
    assert c64.complement == 491 and c64.stations["marines"] == 84
    assert sum(1 for p in c64.posts if p.post.endswith(" lieutenant")) == 5
    assert [p.role for p in c64.people].count("master's mate") == 3
    assert {"captain of marines", "lieutenant of marines"} <= {p.role for p in c64.people}
    # the razee: 330, "at first of 310, but afterwards of 330 men" (James vol. 1 p. 454), on the
    # 44's column (294) with 36 seamen over it (D32 (a)): three lieutenants, two master's mates,
    # 50 marines, the column's seven and 43 privates (judgement)
    assert c.complement == 330 and c.stations["marines"] == 50
    assert sum(1 for p in c.posts if p.post.endswith(" lieutenant")) == 3
    assert [p.role for p in c.people].count("master's mate") == 2
    for crew in (c64, c):
        # every man somewhere: the posts, the seamen's stations, the marines and the idlers
        marines, idlers = crew.stations["marines"], crew.stations["idlers"]
        assert len(crew.posts) + crew.seamen + marines + idlers == crew.complement
        assert sum(crew.idlers_by_trade.values()) == idlers
        assert crew.quarter_bill.helm == 2 and crew.ration.table == "navy"
    # the 64's company larger than the razee's at every station
    for station in ("forecastle", "fore_top", "main_top", "mizzen_top", "afterguard", "waisters"):
        assert c64.stations[station] > c.stations[station], station


@pytest.mark.parametrize(
    "path, marines, at_long_guns, trimmers",
    [(SIXTY_FOUR, 84, 84, 137), (RAZEE, 50, 18, 93)],
)
def test_her_quarters_at_the_beat_are_as_her_bills_note_records(
    path, marines, at_long_guns, trimmers
):
    """Indf §6.4 and §16 item 5: `Quarters.beat` measured at muster on each default fit, as the
    quarter bill's trimmers' note records it. Every gun crew fills; the beat takes the marines to
    the long guns before the topmen (crew/quarters.py; the engine's order, open for the lead), so
    no marines' division forms, as on the frigate-36 (Indf §18 item 13), and the topmen the guns
    leave fall to the trimmers, above the bill's 53 and 79. Measured at seed 7."""
    from freesail.crew.model import Station
    from freesail.crew.quarters import MARINES, TRIMMERS, quarters_of
    from tests.test_brains import world_at

    w = world_at(49.5, -5.5, path)
    w.run(10)
    w.submit("beat to quarters")
    w.run(30)
    q = quarters_of(w.ship)
    assert all(len(gc.members) == gc.wanted for gc in q.crews.values())
    at_guns = [
        gc.kind for gc in q.crews.values() for s in gc.members if s.station is Station.MARINES
    ]
    assert (len(at_guns), at_guns.count("long")) == (marines, at_long_guns)
    assert not q.divisions.get(MARINES)
    assert len(q.divisions[TRIMMERS]) == trimmers


@pytest.mark.parametrize("path", [SIXTY_FOUR, RAZEE])
def test_her_ship_files_posts_and_people_agree_with_her_wardroom_files(path):
    """tests/test_wardroom.py's check (:42-57) on her two files: the generator draws the posts
    and the drawn roles from `data/people/<ship>.yaml` (spec M6 §2)."""
    from freesail.world import people as PE

    stem = Path(path).stem
    wardroom = PE.load_wardroom(path)
    assert wardroom is not None, stem
    spec = load_spec(ROOT / path)
    assert [p.post for p in spec.crew.posts] == wardroom.posts, stem
    drawn = [
        (o.role, o.drawn["station"], o.drawn.get("rating"), o.messenger) for o in wardroom.drawn
    ]
    assert [(p.role, p.station, p.rating, p.messenger) for p in spec.crew.people] == drawn
    raw = yaml.safe_load((ROOT / "data" / "people" / f"{stem}.yaml").read_text("utf-8"))
    assert raw["ship"] == path
    assert wardroom.role_of("captain") and wardroom.role_of("officer of the watch")


def test_her_ground_tackle_is_steels_for_a_64(sixty_four, razee):
    frigate = load_ship(FRIGATE).spec.ground_tackle.anchors
    for ship in (sixty_four, razee):
        tackle = ship.spec.ground_tackle
        assert not tackle.chain  # hemp in her years
        anchors = {a.id: a for a in tackle.anchors}
        # four bowers of 57 cwt, seven cables of 21 in laid three, two, one and one (Steel 1794
        # vol. I, the anchor table and 'A Cordage Table': Ind §6.2; Lever 1808 p. 67; D33 (a))
        four = ("best_bower", "small_bower", "sheet", "spare_anchor")
        for aid in four:
            assert anchors[aid].weight_kg == pytest.approx(57 * CWT_KG, abs=1.0), aid
            assert anchors[aid].cable_in == 21.0, aid
        assert [anchors[a].cable_fathoms for a in four] == [360.0, 240.0, 120.0, 120.0]
        # the stream anchor of 15 cwt on 11 1/2 in, the kedge of 7 cwt 2 qr (the same tables)
        assert anchors["stream"].weight_kg == pytest.approx(15 * CWT_KG, abs=1.0)
        assert anchors["stream"].cable_in == 11.5
        assert anchors["kedge"].weight_kg == pytest.approx(7.5 * CWT_KG, abs=1.0)
        # her bower cable stronger than any of the frigate-36's (19 in, judgement there)
        assert anchors["best_bower"].cable_kn > max(a.cable_kn for a in frigate)


# ---------------------------------------------------------------------------
# Her descriptions and names (Indf §8)
# ---------------------------------------------------------------------------


def test_her_descriptions_name_her_files_and_rank_the_razee_a_frigate():
    from freesail.world import brains
    from freesail.world import captains as C
    from freesail.world import ships as S

    for words, key in (
        ("a sixty-four", "sixty-four"),
        ("a 64", "sixty-four"),
        ("a sixty-four gun ship", "sixty-four"),
        ("a razee", "razee"),
        ("a razee frigate", "razee"),
        ("a cut-down sixty-four", "razee"),
        ("a French razee", "razee"),
    ):
        assert S.description_key(words) == key, words
    # "a ship of the line" is the 74's words, not hers (Indf §8; tests/test_ships.py:99)
    assert S.description_key("a ship of the line") is None
    for key, path, rank in (("sixty-four", SIXTY_FOUR, 4), ("razee", RAZEE, 3)):
        d = S.description(key)
        assert d["file"] == path and d["rig"] == "a ship"  # three masts square-rigged
        assert S.file_descriptions(path)[key]["what"] == d["what"]
        # D16 (a): the razee a frigate (rank 3) by her own words, "cut down from a sixty-four"
        # in them; the 64 rank 4 (`_SIZE_WORDS`, the razee's first)
        assert C.size_of_words(d["what"]) == rank and C.size_rank_of(d["what"]) == rank
        assert C.size_of_file(path) == C.SIZE_RANK[key] == rank
        vessel = type("Vessel", (), {"description": key, "role": ""})()
        assert brains.role_of_vessel(vessel, None) == "kings-ship"  # a King's ship, as the frigate


@pytest.mark.parametrize(
    "path, phrases",
    [
        (
            SIXTY_FOUR,
            [
                "mizzen course",
                "mizen course",
                "mizzen",
                "mizen",
                "mizzen yard",
                "mizen yard",
                "crossjack",
                "cro'jack yard",
                "foresail",
                "mainsail",
                "fore staysail",
                "fore topmast stays'l",
                "middle staysail",
                "mizen staysail",
                "head sails",
                "jibs",
                "kites",
                "stuns'ls",
                "lower yards",
                "upper yards",
                "royal masts",
                "topgallant sails",
                "light sails",
                "storm mizen",
                "storm staysails",
                "save-all",
                "fore sheet",
                "main top bowline",
            ],
        ),
        (
            RAZEE,
            [
                "spanker",
                "driver",
                "mizzen",
                "mizen",
                "spanker boom",
                "driver boom",
                "spanker gaff",
                "ringtail",
                "crossjack",
                "cro'jack yard",
                "fore staysail",
                "middle staysail",
                "mizen topgallant staysail",
                "head sails",
                "kites",
                "upper yards",
                "royal masts",
                "storm mizzen",
                "storm canvas",
                "occasional sails",
                "save-alls",
                "main tack",
                "mizzen top bowline",
            ],
        ),
    ],
)
def test_her_period_names_resolve(path, phrases):
    """test_period_names_resolve's form (tests/test_ship_particulars.py): object phrases as the
    grammar hands them to the resolver, the article already gone. Her 64 has no spanker (Indf
    §4.7): her after sail is the mizen course, and 'the spanker' finds nothing on her."""
    table = noun_table(load_ship(path))
    for phrase in phrases:
        assert table.lookup(phrase) is not None, phrase
    if path == SIXTY_FOUR:
        assert table.lookup("spanker") is None and table.lookup("driver") is None


# ---------------------------------------------------------------------------
# Her polars (Indf §9), in tests/test_ships.py's form
# ---------------------------------------------------------------------------


def test_her_polars_are_drawn_from_her_files_and_agree_with_her_sailed_beam_reaches():
    """`polar_of` balances the sails model against the hull's resistance at each angle off the
    wind (tests/test_ships.py:74-93). Her beam reaches in fifteen knots are within half a knot
    of those she sails under plain sail with the yards trimmed, the known truths' polar form
    (`under_plain_sail` at 90 deg): the 64 7.50 kn, the razee 7.78 kn (measured, seed 7). By
    `polar_of`: the 64's best 4.25, 7.59 and 10.92 kn in 8, 15 and 25 kn, the razee's 4.41, 7.93
    and 11.54, the frigate-36's 4.62, 8.19 and 11.63; all three closest at 50 deg and beating
    at 60. Indf §9's targets that hold: the razee above the 64 she was cut from, her best in 25
    kn at or above the Virginie chase's mean of 11.2 kn (Osler p. 125; Gazette 13887 p. 388;
    D24), and her closest within a step of the frigate-36's (the brace limits the frigate's:
    Indf §4.2). The razee outsailing the frigate-36 close-hauled and running large does not
    hold (truth 7-187's docstring)."""
    from freesail.world import ships as S

    frigate = S.polar_of(FRIGATE)
    measured = {SIXTY_FOUR: 7.5, RAZEE: 7.8}
    for path, kn in measured.items():
        p = S.polar_of(path)
        assert abs(p.speed_kn(90.0, 15.0) - kn) <= 0.5, (path, p.speed_kn(90.0, 15.0))
        assert p.speed_kn(90.0, 8.0) < p.speed_kn(90.0, 15.0) < p.speed_kn(90.0, 25.0)
        assert p.speed_kn(20.0, 15.0) == 0.0  # nothing closer than the grid's first angle
        assert abs(p.closest_deg - frigate.closest_deg) <= 10.0
    razee, sixty_four = S.polar_of(RAZEE), S.polar_of(SIXTY_FOUR)
    assert razee.speed_kn(90.0, 15.0) > sixty_four.speed_kn(90.0, 15.0)
    assert max(razee.speeds_kn[razee.winds_kn.index(25.0)]) >= 11.2


# ---------------------------------------------------------------------------
# Her round trip under the rules captains at seed 7, no fit named (Indf §11.2, §14 item 5)
# ---------------------------------------------------------------------------

EXERCISING = ROOT / "data" / "scenarios" / "exercising-the-great-guns.yaml"
FILE_OF = {"sixty-four": SIXTY_FOUR, "razee": RAZEE}


@pytest.mark.parametrize("path, other", [(RAZEE, "sixty-four"), (SIXTY_FOUR, "razee")])
def test_her_scenario_round_trips_and_she_sails_it_under_the_rules_captain_with_no_fit_named(
    path, other, tmp_path
):
    """What is common to every option of D25 (Indf §11.2), built now with no scenario file: a
    scenario of hers, written from its fields by the harbour's maker (`write_scenario`; the
    great guns' scenario with her file in the frigate's place), reads back to itself and loads
    with no fit named; she sails it at seed 7 under her rules captain with her default fit ("as
    carried 1796", the owner's answer; "ardent class 1784"), the other of her two files in
    sight under a rules captain of its own as a King's ship, and no order of hers refused;
    saved at half an hour and loaded from the checkpoint, she carries on as the world that was
    never saved. The 64 sails the razee's scenario by the command line (D48 (a)), no fit being
    named. Measured: an hour in, the razee 5.7 kn and the 64 5.0 kn under plain sail, each
    captain investigating the stranger."""
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
    fields["name"] = f"The {other}'s sister off the Lizard"
    fields.pop("standing_orders")  # her rules captain's book alone
    fields["ship"]["file"] = path
    assert "fit" not in fields["ship"]
    fields["ships"] = [
        {
            "description": other,
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
    assert sf.seed == 7 and sf.ship_file == path and sf.scenario.fit is None
    world = make_scenario_world(sf)
    begin(world, sf)
    default = load_spec(path).armament.default
    assert world.ship.fit == default
    assert world.captain.commands and world.captain.role == "kings-ship"
    stranger = world.vessels.find("Stranger")
    assert stranger.ship_file == FILE_OF[other] and stranger.brain.role == "kings-ship"
    world.run(1800)
    saved = replay_mod.save_to_file(world, tmp_path / "hers.json")
    world.run(1800)
    assert not [e for e in world.log if e.kind == "order.rejected"]
    assert units.ms_to_knots(world.ship.dyn.speed) > 3.0
    loaded, how = replay_mod.load(saved, ship_factory)
    assert how == "checkpoint" and loaded.ship.fit == default
    loaded.run(1800)
    assert loaded.clock.tick == world.clock.tick and loaded.state() == world.state()
    if path == RAZEE:
        by_hand = make_scenario_world(sf, ship=SIXTY_FOUR)
        begin(by_hand, sf)
        by_hand.run(600)
        assert by_hand.ship.fit == "ardent class 1784"
        assert not [e for e in by_hand.log if e.kind == "order.rejected"]


# ---------------------------------------------------------------------------
# Her truths, 7-186 to 7-188 (Build-Ships.md §15; Indf §14)
# ---------------------------------------------------------------------------


def test_truth_7_186_her_particulars_hold_their_sources_and_the_razee_is_the_64_cut_down():
    """Indf §14 truth 1, the brief's item 6. Both files load. Beam 13.5 ± 0.1 m (44 ft 5 in,
    Winfield 1793-1817 p. 100), load line 48.8 ± 0.3 m (160 ft on WL1, measured), draughts
    6.33 and 5.88 ± 0.1 m (measured on ZAZ1407 and ZAZ2371). The razee's profile below the old
    upper deck is the 64's raised by her rise, 0.44 ± 0.02 m, point by point: her keel, stem
    and counter, her wales, her midship section, her gun deck (the 64's lower deck) and its
    thirteen ports, her quarterdeck (the old upper deck); 0.44-0.45 by the files. The lowest
    gun-deck sills 1.53 and 1.98 ± 0.03 m (5.02 ft above WL1 on ZAZ1407; ZAZ2371's 1.96). Each
    lower mast's head lower by its cut (6 ft 3 in, 6 ft 7 in, 6 ft 9 in: Ind §3.3) less the
    rise, ± 0.1 m for the heights kept to the decimetre (1.43, 1.53 and 1.63 m by the files).
    26 long 24-pounders in every fit of both files. Complements 491 and 330, marines 84 and 50
    (the Regulations' columns; James vol. 1 p. 454). Four bowers of 57 cwt in both (Steel's
    64). Pinned at once: nothing here moves at stage B."""
    s64, s = load_ship(SIXTY_FOUR), load_ship(RAZEE)
    h64, h = s64.hull.spec, s.hull.spec
    for hull in (h64, h):
        assert abs(hull.beam_m - 13.5) <= 0.1
        assert abs(hull.length_waterline_m - 48.8) <= 0.3
    assert abs(h64.draught_m - 6.33) <= 0.1 and abs(h.draught_m - 5.88) <= 0.1
    p64, p = h64.profile, h.profile
    old_upper = dict(p64.decks_m)["upper"]

    def raised(old, new):
        assert abs(new - old - RISE_M) <= 0.02, (old, new)

    def below_old_upper(x, z):
        return z < interp(old_upper, x)

    for (x0, z0), (x1, z1) in zip(p64.keel_m, p.keel_m, strict=True):
        assert x0 == x1
        raised(z0, z1)
    compared = 0
    for line64, line in ((p64.stem_m, p.stem_m), (p64.stern_m, p.stern_m)):
        for (x0, z0), (x1, z1) in zip(line64, line, strict=False):
            if x0 == x1 and below_old_upper(x0, z0):
                raised(z0, z1)
                compared += 1
    assert compared >= 15  # the stem to the old upper deck and the counter
    for w64, w in zip(p64.wales_m, p.wales_m, strict=True):
        assert w64[0] == w[0]
        raised(w64[1], w[1])
        raised(w64[2], w[2])
    for (z0, hb0), (z1, hb1) in zip(p64.section_m, p.section_m, strict=True):
        assert hb0 == hb1
        if z0 < interp(old_upper, 0.0):
            raised(z0, z1)
    lower64, gun_deck = dict(p64.decks_m)["lower"], dict(p.decks_m)["upper"]
    for (x0, z0), (x1, z1) in zip(lower64, gun_deck, strict=True):
        assert x0 == x1
        raised(z0, z1)
    for x, z in dict(p.decks_m)["quarterdeck"]:
        raised(interp(old_upper, x), z)
    for (x0, z0, hb0), (x1, z1, hb1) in zip(
        ports_of(p64, "lower"), ports_of(p, "upper"), strict=True
    ):
        assert (x0, hb0) == (x1, hb1)
        raised(z0, z1)
    assert abs(min(z for _x, z, _hb in ports_of(p64, "lower")) - 1.53) <= 0.03
    assert abs(min(z for _x, z, _hb in ports_of(p, "upper")) - 1.98) <= 0.03
    for mast, cut_ft in CUT_FT.items():
        lower = above_water(s64, f"{mast}.mast") - above_water(s, f"{mast}.mast")
        assert abs(lower - (cut_ft * FT - RISE_M)) <= 0.1, (mast, lower)
    for ship in (s64, s):
        for fit in ship.spec.armament.fits.values():
            long_24s = [g for g in fit.guns if g.kind == "long" and g.pounder == 24]
            assert len(long_24s) == 26, fit.name
        anchors = ship.spec.ground_tackle.anchors
        bowers = [a for a in anchors if abs(a.weight_kg - 57 * CWT_KG) <= 1.0]
        assert len(bowers) == 4 and {a.kind for a in bowers} <= {"bower", "sheet"}
    assert (s64.spec.crew.complement, s.spec.crew.complement) == (491, 330)
    assert (s64.spec.crew.stations["marines"], s.spec.crew.stations["marines"]) == (84, 50)


def test_truth_7_187_the_razee_is_lighter_stiffer_and_faster_than_the_64_she_was_cut_from():
    """The plan's (Phase 5); Indf §14 truth 2. The razee displaces less than the 64 by the
    slice measured between their lines, 238-244 tons of 35 cu ft (Ind §2.3.3; 241.1 by the
    files); she draws 0.44 ± 0.03 m less (0.45); her righting moment at 10 degrees of heel is
    greater by at least 4% (1,925 t at 1.65 m against 2,170 t at 1.35 m: 8.4% by the files);
    and under plain sail on a beam reach in fifteen knots she heels less (the known truths'
    polar form at seed 7: the razee 4.1 deg at 7.78 kn, the 64 4.6 deg at 7.50 kn; the
    frigate-36 5.5 deg at 7.97 kn). Pinned at once.

    **The speed clause waits on stage B** (Build-Ships.md §15): her speed greater at every
    angle from her closest to 180 degrees in 15 and 25 kn. Measured now on the 64's stand-in
    mizen course it holds (`polar_of`: the razee faster at every angle from 50 to 180 degrees,
    by 0.16-0.34 kn in 15 kn and 0.30-0.65 kn in 25 kn); but the 64's after sail changes when
    her mizen course goes to its yard (Indf §0, §16 item 3), so the clause is pinned then, old
    beside new, and on the stand-in, said so, if the gate slips past the package's merge.

    **Not pinned: the razee outsailing the frigate-36** (Indf §14 truth 4; D24; the Virginie
    chase). Her best in 25 kn, 11.54 kn, meets the chase's mean of 11.2; but in 15 kn she is
    under the frigate-36 close-hauled and running large (`polar_of`: 60 deg 4.15 against 4.29,
    70 deg 5.96 against 6.14, 120 deg 7.60 against 7.86, 130 deg 7.21 against 7.40, 140 deg 6.82
    against 6.99, 150 deg 6.39 against 6.53), and sailed (60 deg 3.58 against 3.63, 120 deg 7.37
    against 7.53). `hull_speed_kn` at the top of D24's band, 14.5, raises her 15-kn figures by
    0.04 kn at most; `clr_x_m` does not reach the polar; the brace limits move only with a
    source. Reported, not forced (Indf §9)."""
    from tests.test_known_truths import under_plain_sail

    s64, s = load_spec(SIXTY_FOUR), load_spec(RAZEE)
    slice_tons = (s64.hull.displacement_kg - s.hull.displacement_kg) / units.LONG_TON
    assert 238.0 <= slice_tons <= 244.0, f"{slice_tons:.1f} tons"
    assert abs(s64.hull.draught_m - s.hull.draught_m - 0.44) <= 0.03

    def righting(world):
        hull = world.ship.hull
        return hull.spec.displacement_kg * units.G * hull.gm_m * math.sin(math.radians(10.0))

    w64 = under_plain_sail(SIXTY_FOUR, 90.0)
    w = under_plain_sail(RAZEE, 90.0)
    assert righting(w) >= 1.04 * righting(w64)
    heel64, heel = abs(math.degrees(w64.ship.dyn.heel)), abs(math.degrees(w.ship.dyn.heel))
    assert 2.0 <= heel < heel64 <= 8.0, (heel, heel64)
    for world in (w64, w):  # both on the beam reach with way on
        assert units.ms_to_knots(world.ship.dyn.speed) > 6.5


def _interval(path: str, hurt_share: float) -> float:
    """Truth 7-135's measure on her file (`_frigate_interval`, tests/test_known_truths.py): the
    mean seconds between a starboard long 24-pounder's discharges over twenty minutes of the
    battery's own cycle at a mark abeam, the company full or a share of each gun crew struck
    down at their guns after the beat."""
    from freesail.combat.action import _firer
    from freesail.combat.guns import FireMode, Target, battery_of
    from freesail.crew.quarters import quarters_of
    from tests.test_brains import world_at
    from tests.test_known_truths import _guns_ready

    w = world_at(49.5, -5.5, path)
    w.run(60)
    _guns_ready(w)
    w.run(40)
    ship = w.ship
    q = quarters_of(ship)
    if hurt_share:
        for gc in q.crews.values():
            n = int(round(len(gc.members) * hurt_share))
            for s in gc.members[:n]:
                s.fit = False
                s.hurt = "wounded"
                s.at = None
    b = battery_of(ship)
    b.engaged = "starboard"
    b.mode = FireMode.AS_THEY_BEAR
    b.target = "mark"
    b.target_words = "a brig"
    mark = Target(
        id="mark",
        words="a brig",
        bearing_rad=units.wrap_2pi(float(ship.heading) + math.pi / 2.0),
        range_m=200.0,
        heading_rad=float(ship.heading),
        length_m=30.0,
        heel_deg=0.0,
        nation="france",
        body=None,
        world=None,
    )
    rng = w.rng.stream("truth-7-188")
    firings: dict[str, list[int]] = {}
    for tick in range(20 * 60):
        before = {g.id: g.fired for g in ship.guns.values()}
        b.tick(1.0, q, _firer(w, ship), mark, rng, tick, lambda *a, **k: [])
        for g in ship.guns.values():
            if g.fired > before[g.id]:
                firings.setdefault(g.id, []).append(tick)
    gaps = []
    for gid, ticks in firings.items():
        g = ship.guns[gid]
        if g.kind == "long" and g.pounder == 24 and g.side == "starboard" and len(ticks) > 2:
            gaps += [t2 - t1 for t1, t2 in zip(ticks[1:], ticks[2:], strict=False)]
    assert gaps, "no 24-pounder fired twice"
    return sum(gaps) / len(gaps)


def test_truth_7_188_her_broadside_against_the_frigate_36s_by_70s_rule():
    """The brief's item 6; Indf §14 truth 3. By 70's rule (`far_ship`: one side's broadside
    guns and every chaser, `combat/far.py`), the razee's broadside weighs 510 lb as razeed in
    1795 and 714 lb as carried from 1796, against the frigate-36's 421: ratios 1.21 and 1.70
    ± 0.05 (counts; James's 702 for 1796 counts one 12-pounder, Indf §18 item 2). The 64's,
    600 lb as built (1.43), is pinned beside them. The bands hold the frigate-36's quarterdeck
    as the owner keeps it, and the 416 lb it would weigh corrected (Indf §16 item 14). Her rate,
    in truth 7-135's form on her own files at seed 7: the mean interval of a starboard long
    24-pounder over twenty minutes at a mark abeam, within the frigate's bands, 90-125 s with
    the full company and 140-210 s with a quarter of each crew struck down. Measured: the razee
    as carried 1796 108 s and 195 s, the 64 as built 103 s and 185 s; three of a 24-pounder's
    eleven (Falconer) struck down."""
    from freesail.combat.far import far_ship

    frigate = far_ship(FRIGATE, "britain").broadside_lb
    # her 421 lb as the owner keeps her quarterdeck, or the 416 it would weigh corrected
    assert 416.0 <= frigate <= 421.0
    razeed = far_ship(RAZEE, "britain", fit="as razeed 1795").broadside_lb
    carried = far_ship(RAZEE, "britain").broadside_lb
    assert (razeed, carried) == (510.0, 714.0)
    assert abs(razeed / frigate - 1.21) <= 0.05 and abs(carried / frigate - 1.70) <= 0.05
    assert far_ship(SIXTY_FOUR, "britain").broadside_lb == 600.0
    for path in (RAZEE, SIXTY_FOUR):
        full = _interval(path, 0.0)
        assert 90.0 <= full <= 125.0, f"{path}: {full:.0f} s"
        short = _interval(path, 0.25)
        assert 140.0 <= short <= 210.0, f"{path}: {short:.0f} s"
        assert short >= full * 1.3
