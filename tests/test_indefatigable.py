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
razee lighter, stiffer and faster than the 64, 7-188 her broadside against the frigate-36's, 7-189
the 64's handling with her mizen yard and spritsails, and the clauses of 7-230 that are hers. Each
is written against the names the Hull keeps (`world.ship`; Design-OneWorld §2.2).

**Stage B (Indf §13 step 7; the lead's notes of 2026-10-29, item 2).** The 64's mizen course is cut
at the mast on her whole yard, her driver is in the sail room and her yards are under the
bowsprit; the razee has her spritsail yard; both have the bowsprit on the stem head, Steel p. 42's
long pole-heads and the clew check's clearances. Each pin that moved stands old beside new where
it is; the whole is "Stage B" below. The stage-A refinement (Indf §3.5 item 9, §17's answers of
2026-10-29) moved the bow's lines and the staysails between the masts, each likewise.

The figures quoted as measured were measured at seed 7 on the owner's machine (Windows 11,
2026-10-28); the bands are the sources' or judgement where they say so.
"""

from __future__ import annotations

import copy
import importlib.util
import math
import random
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

import pytest
import yaml

from freesail import orders, units
from freesail.api.session import make_world
from freesail.core.world import Scenario
from freesail.evolutions import Runner, scripts
from freesail.evolutions import trim as yard_trim
from freesail.orders.resolve import noun_table
from freesail.orders.storm import bowsprit_sail_lines, shorten_sail_lines
from freesail.physics.sails import _square_rigged
from freesail.physics.wind import Wind, WindParams
from freesail.ship import parts
from freesail.ship.loader import load_ship, load_spec, ship_from_dict
from freesail.ship.parts import SailState
from freesail.ship.profile import deck_at, half_breadth_at_sill, interp, ports_of, sill_at
from freesail.ship.stub import OrderError
from freesail.world.ships import _balanced_speed_ms

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
    # her datum, D18 (c), the owner's choice (2026-10-29: Indf §2.2, §17 item 1): her old upper
    # deck at midships, 12 ft 0 in above her line (measured on ZAZ2371 and 1280T: Ind §2.3.5),
    # the 64's upper deck raised by her rise at midships, 1.46 ft: 3.67 m. Was D18 (a), her gun
    # deck there, 4 ft 7 in above her line (the 64's lower deck; 4 ft 5 in-4 ft 8 in on
    # ZAZ2371): 1.39 m
    assert abs(h.deck_height_m - 3.66) <= 0.05
    assert h.deck_height_m == pytest.approx(h64.deck_height_m + 1.46 * FT, abs=0.01)
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
    # the taffrail 13 ft abaft AP and 28 ft above WL1; the rail ends where her side ends, at the
    # beakhead bulkhead 153.3 ft from AP, 19.50 ft above WL1 (measured on 1407F by columns; was
    # 19.39, extended on its own slope from 144.8 ft, and before that the near knighthead's cap,
    # 160.8 ft and 20 ft, which stage A read as the stem head: Indf §3.5 item 9); x forward of
    # the middle of the load line, 80 ft from AP
    assert p.rail_m[0] == pytest.approx(((-13.0 - 80.0) * FT, 28.0 * FT), abs=0.01)
    assert p.rail_m[-1] == pytest.approx(((153.3 - 80.0) * FT, 19.50 * FT), abs=0.01)
    # the stem's fore edge, separated from the knee of the head (measured on 1407F at full
    # resolution, Build-Ships.md §5.1): at WL1 160.84 ft from AP, 2.6 ft abaft the knee's fore
    # edge (163.45, Ind §2.3.6), and up to the stem head and no further, the top of its fore face
    # 162.5 ft from AP and 16.0 ft above WL1 under the bowsprit (was the knee up to its top,
    # 174.5 ft and 20 ft); the rail ends abaft the stem head, as a two-decker's forecastle does
    assert interp([(z, x) for x, z in p.stem_m], 0.0) == pytest.approx(
        (160.84 - 80.0) * FT, abs=0.01
    )
    assert p.stem_m[-1] == pytest.approx(((162.52 - 80.0) * FT, 16.0 * FT), abs=0.01)
    assert max(x for x, _z in p.stem_m) == p.stem_m[-1][0]
    assert p.rail_m[-1][0] < p.stem_m[-1][0] and p.rail_m[-1][1] > p.stem_m[-1][1]
    # its foot boxed into the keel, 1.1 ft above K at 144.5 ft, abaft K's square fore end
    assert p.stem_m[0][0] < p.keel_m[-1][0]
    assert p.stem_m[0][1] - interp(p.keel_m, p.stem_m[0][0]) == pytest.approx(1.06 * FT, abs=0.02)
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
    # the deck she is worked from in the waist is her gun deck, 4 ft 7 in above her line (4 ft
    # 5 in-4 ft 8 in on ZAZ2371), and her datum, D18 (c), her old upper deck at midships, which
    # in the waist is none of her decks (her rise there 0.445 m, RISE_M to the centimetre). Was,
    # under D18 (a): deck_at(p, 0.0) == her datum, her gun deck, 1.39 m
    assert deck_at(p, 0.0) == pytest.approx(interp(decks["upper"], 0.0))
    assert (4.0 + 5.0 / 12.0) * FT <= deck_at(p, 0.0) <= (4.0 + 8.0 / 12.0) * FT
    assert razee.hull.spec.deck_height_m == pytest.approx(old_upper, abs=0.02)
    assert razee.hull.spec.deck_height_m - deck_at(p, 0.0) == pytest.approx(2.28, abs=0.005)
    # six ports a side on her quarterdeck and three on her forecastle (ZAZ2375, measured), and
    # her chase port before them for the 12-pounders of 1796 (D30 (a); judgement)
    assert len(ports_of(p, "quarterdeck")) == 6 and len(ports_of(p, "forecastle")) == 4
    # her taffrail, the top of her stern and of her side, on the 64's stern line 22 ft above
    # WL1 and 10 ft 3 in abaft AP, where ZAZ2371 ends her stern's outline (measured there, 10.4
    # ft and 21.9 ft, ±0.2 ft), 7.15 m above her water. Was 5 ft 6 in abaft AP (ZAZ2375's, the
    # stern at her quarterdeck's height) at her quarterdeck rail's height, 5.26 m: her short
    # roundhouse not yet in her profile (2026-10-29)
    assert p.rail_m[0] == p.stern_m[-1]
    assert p.rail_m[0][0] == pytest.approx((-10.25 - 80.0) * FT, abs=0.01)
    assert p.rail_m[0][1] == pytest.approx(22.0 * FT + RISE_M, abs=0.01)
    # her quarterdeck rail 4 ft 6 in above her quarterdeck (Ind §2.3.5, not re-measured), from
    # her roundhouse's breast to the quarterdeck's
    breast, qd_end = decks["roundhouse"][-1][0], decks["quarterdeck"][-1][0]
    on_qd = [(x, z) for x, z in p.rail_m if breast < x <= qd_end]
    assert len(on_qd) == 2
    for x, z in on_qd:
        assert z - interp(decks["quarterdeck"], x) == pytest.approx(4.5 * FT, abs=0.02), x
    # her waist's top-side, 30.8 ft above K (measured, ZAZ2371), more than a metre under the
    # 64's waist rail at midships (1407F)
    assert interp(p.rail_m, 0.0) < interp(p64.rail_m, 0.0) - 1.0
    # her head the 64's, not measured on ZAZ2371 (judgement): her rail ends at the 64's
    # beakhead bulkhead, her forecastle rail 4 ft 6 in above her forecastle (was carried on to
    # the knighthead's cap: Indf §3.5 item 9), and her stem is the 64's raised by her rise
    assert p.rail_m[-1][0] == p64.rail_m[-1][0]
    assert p.rail_m[-1][1] - interp(decks["forecastle"], p.rail_m[-1][0]) == pytest.approx(
        4.5 * FT, abs=0.02
    )
    assert [x for x, _z in p.stem_m] == [x for x, _z in p64.stem_m]
    for (_x0, z0), (_x1, z1) in zip(p64.stem_m, p.stem_m, strict=True):
        assert abs(z1 - z0 - RISE_M) <= 0.02, (z0, z1)


def test_the_razees_short_roundhouse_stands_over_her_cabin_under_her_taffrail(sixty_four, razee):
    """ZAZ2371's N.B.: her roundhouse "shortened to the Beam abaft the Mizen" by the Navy Board's
    warrant of December 1794 (read, tentative: Ind table V10), as she was in 1796 (Build-Ships.md
    §19.1 item 18; the owner, 2026-10-29). Her roundhouse is the 64's quarterdeck (1280T) kept
    over her cabin at her line, which ZAZ2371 draws in red within half a foot, from 7.3 ft abaft
    AP to the beam abaft the mizen, 23.3 ft from AP (ZAZ2375's beam under the coach's fore
    bulkhead), abaft her mizen; her rail 6 in above it (ZAZ2371's side at the stern; forward of
    it the drawn top sweeps down under the red deck to her quarterdeck rail's height at the
    mizen, with no rail drawn over the deck: judged, a deck standing under its rail, and her
    note says so), stepping down at its breast to her quarterdeck rail; her stern lights and quarter
    gallery, the 64's lower band and tier at her line, under her taffrail and her roundhouse's
    deck, the tier forward of her stern's line. Was: no roundhouse, her taffrail at her
    quarterdeck rail 5 ft 6 in abaft AP, the band and the tier above it (recorded, not moved).
    Her ports, guns and fits are as they were: none on her roundhouse."""
    p64, p = sixty_four.hull.spec.profile, razee.hull.spec.profile
    decks64, decks = dict(p64.decks_m), dict(p.decks_m)
    rh = decks["roundhouse"]
    assert rh[0][0] == pytest.approx(x_of(-7.3), abs=0.01)
    assert rh[-1][0] == pytest.approx(x_of(23.3), abs=0.01)
    assert rh[-1][0] < x_of(MAST_STEPS_FT["mizzen"][0])  # abaft her mizen at its partners
    qd64 = decks64["quarterdeck"]
    for x, z in rh:
        if x >= qd64[0][0]:  # the 64's quarterdeck at her line, over its measured extent
            assert z - interp(qd64, x) == pytest.approx(RISE_M, abs=0.02), x
    assert dict(p.marks)["decks_m"] == "judged"  # the N.B.'s beam taken for ZAZ2375's
    # her rail 6 in above her roundhouse's deck, stepping down at its breast 0.86 m to her
    # quarterdeck rail
    over = [(x, z) for x, z in p.rail_m if rh[0][0] <= x <= rh[-1][0]]
    assert len(over) == len(rh)
    for x, z in over:
        assert z - interp(rh, x) == pytest.approx(0.5 * FT, abs=0.01), x
    after = next(pt for pt in p.rail_m if pt[0] > rh[-1][0])
    assert after[0] - rh[-1][0] < 0.05
    assert over[-1][1] - after[1] == pytest.approx(0.86, abs=0.02)
    # the rail over the roundhouse a judgement over ZAZ2371's drawn top, and her note says so
    assert "the drawn top sweeps down fair, without a step" in text_of(RAZEE)
    # her stern lights and quarter gallery under her taffrail and her roundhouse's deck
    stern = p.form.stern
    taff_x, taff_z = p.stern_m[-1]
    ((x_aft, x_fore, _z_low, z_high),) = stern.galleries_m
    assert z_high < min(taff_z, interp(rh, x_aft), interp(rh, x_fore))
    assert x_aft > interp([(z, x) for x, z in p.stern_m], z_high)
    ((_low, high, _n, _hb),) = stern.lights_m
    assert high < min(taff_z, interp(rh, taff_x))
    # her ports and her guns are as they were: no port and no gun on her roundhouse
    assert "roundhouse" not in dict(p.ports_m)
    for fit in razee.spec.armament.fits.values():
        assert not [g for g in fit.guns if g.deck == "roundhouse"], fit.name


# The razee's spar heights above the datum as filed under D18 (a), 09dde99 (her datum her gun
# deck, 1.39 m), and the lower masts' x_m there, their places at the partners on her gun deck.
# Stage B moved two (old beside new): the bowsprit's end 11.6 -> 10.1, its root on the stem head;
# the boom 4.4 -> 6.46, its jaws raised clear of her roundhouse by the head room, then 5.77 at the
# least that clears her taffrail (the lead's ruling of 2026-10-30).
RAZEE_HEIGHTS_UNDER_A = {
    "main.mast": 23.7,
    "main.yard": 18.8,
    "bowsprit": 10.1,
    "mizzen.boom": 5.77,
}
RAZEE_MASTS_X_UNDER_A = {"fore": 19.23, "main": -2.78, "mizzen": -16.33}


def test_the_razees_datum_is_her_old_upper_deck_and_moves_nothing_above_her_water(razee):
    """D18 (c), the owner's choice (2026-10-29; Indf §2.2): her datum is her old upper deck at
    midships, 3.67 m above her water, 2.28 m above her gun deck, the deck she is worked from in
    the waist and the datum under (a). Her rig is cut above her gun deck as (a) cut it and
    written above the new datum, so that no spar stands elsewhere above her water: each height
    above the datum 2.28 m less than under (a) (the main mast's head 23.7 m, now 21.42), and
    each lower mast's x_m its place at the datum's height, raked from its partners on her gun
    deck (the main -2.78 m, now -2.84). Her lower mast heads stand where Steel's lengths, her
    cuts at the heel and her line put them, as the 64's do. What moves is what reads the datum or
    a height written above it, the deck's wind's eye and the lower masts' windage among them, and
    her note names each. Plainly: (c) departs from the frigate-36's rule, the uppermost continuous
    deck, and her file says so."""
    h = razee.hull.spec
    gun_deck = deck_at(h.profile, 0.0)
    assert gun_deck == pytest.approx(1.39, abs=0.005)
    assert h.deck_height_m - gun_deck == pytest.approx(2.28, abs=0.005)
    for sid, under_a in RAZEE_HEIGHTS_UNDER_A.items():
        assert razee.spars[sid].height_m == pytest.approx(under_a - 2.28, abs=1e-9), sid
        assert above_water(razee, sid) == pytest.approx(under_a + 1.39, abs=1e-9), sid
    for mast, length in STEEL_MASTS_FT.items():
        x, heel = MAST_STEPS_FT[mast]
        water = 21.245 - 1.04 * x / 160.0 - (1.45 + 0.02 * x / 160.0)  # her line above K
        head = (heel + length - CUT_FT[mast] - water) * FT
        assert above_water(razee, f"{mast}.mast") == pytest.approx(head, abs=0.06), mast
        spar = razee.spars[f"{mast}.mast"]
        at_gun_deck = spar.x_m + math.tan(spar.rake) * (h.deck_height_m - gun_deck)
        assert at_gun_deck == pytest.approx(RAZEE_MASTS_X_UNDER_A[mast], abs=0.005), mast
    text = text_of(RAZEE)
    assert "D18 (c), the owner's choice" in text
    assert "departs from the frigate-36's rule, the uppermost continuous deck" in text
    readers = (
        "the deck's wind's eye",
        "each lower mast's windage",
        "the blanket's reach",
        "the spanker sheet's lead",
    )
    for reader in readers:
        assert reader in text, reader


# ---------------------------------------------------------------------------
# Her shape (stage B, the hull's pilot: Indf §3.5 item 8; Build-Ships.md §2.6, §5.1, §5.7)
# ---------------------------------------------------------------------------

# Each line of her profile, each group of her form and each key of her stern, marked by its
# rung (Build-Ships.md §5.0 principle 4): a line measured on her draughts at every point
# sourced, a line with a judgement at its weakest point judged, the figure on her head judged.
SHAPE_MARKS = {
    SIXTY_FOUR: {
        "sourced": (
            "rail_m", "breadth_m", "keel_m", "stem_m", "stern_m", "section_m", "head_m",
            "breadth_line_m", "sections_m", "channel_wales_m", "form.stern",
            "form.stern.knuckle_z_m", "form.stern.transom_hb_m", "form.stern.round_up_m",
            "form.stern.galleries_m", "form.stern.lights_m",
        ),
        "judged": ("wales_m", "decks_m", "ports_m", "port_size_m", "form.head"),
    },
    # her roundhouse in (2026-10-29): stern_m was judged (her taffrail's height), now measured
    # on ZAZ2371; decks_m was sourced, now judged (her roundhouse's breast, the N.B.'s beam
    # taken for ZAZ2375's)
    RAZEE: {
        "sourced": (
            "keel_m", "stern_m", "section_m", "breadth_line_m", "sections_m", "channel_wales_m",
            "form.stern", "form.stern.knuckle_z_m", "form.stern.round_up_m",
        ),
        "judged": (
            "rail_m", "breadth_m", "stem_m", "wales_m", "decks_m", "ports_m", "port_size_m",
            "head_m", "form.stern.transom_hb_m", "form.stern.galleries_m",
            "form.stern.lights_m", "form.head",
        ),
    },
}  # fmt: skip
# WL1 to WL5's half-breadths, moulded, ft, at three of her stations (Ind §2.3.2, measured: 80 ft
# on 1407T, WL1 at full resolution; 140 and 150 ft on 1407F), 3.77 ft apart below WL1 (Ind
# §2.3.1); and the plank outside them, 4 1/2 in (Indf §3.3).
WATERLINES_FT = {
    80: (21.72, 21.3, 20.0, 17.8, 14.5),
    140: (17.68, 15.54, 11.66, 7.17, 2.99),
    150: (11.70, 8.60, 5.12, 2.44, 0.72),
}
WL_SPACING_FT = 3.77
PLANK_FT = 4.5 / 12.0


def x_of(ft_from_ap):
    """Feet forward of AP as her files' x: metres forward of the middle of WL1, 80 ft."""
    return (ft_from_ap - 80.0) * FT


def flat(points):
    """A line of points as one list of numbers, for `pytest.approx`."""
    return [v for point in points for v in point]


def text_of(path):
    """Her file as written, its notes with it."""
    return (ROOT / path).read_text(encoding="utf-8")


@pytest.mark.parametrize("path", [SIXTY_FOUR, RAZEE])
def test_every_line_of_her_shape_carries_its_rung(path):
    """A mark on every line her profile gives, every group of her form and every key of her
    stern, in the profile's order, each its weakest point's word (Build-Ships.md §5.0 principle
    4; §5.6). The rising line and the rabbet are reserved and not written."""
    p = load_spec(path).hull.profile
    lines = [
        key
        for key in (
            "rail_m", "breadth_m", "keel_m", "stem_m", "stern_m", "wales_m", "section_m",
            "decks_m", "ports_m", "port_size_m", "head_m", "breadth_line_m", "sections_m",
            "channel_wales_m", "floor_m", "rabbet_m",
        )
        if getattr(p, key)
    ]  # fmt: skip
    assert "floor_m" not in lines and "rabbet_m" not in lines
    stern = ["knuckle_z_m", "transom_hb_m", "round_up_m", "galleries_m", "lights_m"]
    given = [*lines, "form.stern", *(f"form.stern.{key}" for key in stern), "form.head"]
    marks = dict(p.marks)
    assert list(marks) == given
    assert marks == {key: word for word, keys in SHAPE_MARKS[path].items() for key in keys}


def test_her_waterlines_are_drawn_through_as_measured(sixty_four, razee):
    """`sections_m` is Ind §2.3.2's WL1 to WL5 by station with the plank, 5 to 159 ft from AP,
    each station low to high and a waterline ended at the rabbet left out; the razee's are the
    64's at her own line, each 0.44-0.45 m higher. The drawn side passes through every one of
    them and every point of her main breadth within a millimetre (`form.check`, as at
    generation)."""
    from freesail.ship import form

    p64, p = sixty_four.hull.spec.profile, razee.hull.spec.profile
    by_station = {}
    for x, z, hb in p64.sections_m:
        by_station.setdefault(x, []).append((z, hb))
    assert len(by_station) == 27
    assert min(by_station) == pytest.approx(x_of(5.0), abs=0.01)
    assert max(by_station) == pytest.approx(x_of(159.0), abs=0.01)
    for station, row in WATERLINES_FT.items():
        want = [(-i * WL_SPACING_FT * FT, (hb + PLANK_FT) * FT) for i, hb in enumerate(row)]
        got = by_station[round(x_of(station), 2)]
        assert flat(sorted(got)) == pytest.approx(flat(sorted(want)), abs=0.006), station
    counts = [len(by_station[round(x_of(s), 2)]) for s in (152.0, 155.0, 157.0, 159.0)]
    assert counts == [4, 4, 3, 2]  # WL5 ends at 151.8 ft, WL4 155.4, WL3 157.6, WL2 159.6
    assert [(x, hb) for x, _z, hb in p.sections_m] == [(x, hb) for x, _z, hb in p64.sections_m]
    for (_x, z0, _hb), (_x1, z1, _hb1) in zip(p64.sections_m, p.sections_m, strict=True):
        assert 0.43 <= z1 - z0 <= 0.46, (z0, z1)
    for spec in (sixty_four.hull.spec, razee.hull.spec):
        q = spec.profile
        for x, z, hb in q.sections_m + q.breadth_line_m:
            assert form.half_breadth_at(spec, x, z) == pytest.approx(hb, abs=0.001), (x, z)


def test_her_main_breadth_stands_at_the_drawn_height_of_breadth(sixty_four, razee):
    """`breadth_line_m`, from AP to 155 ft: the half-breadth plan's main-breadth line, 21.74 ft
    moulded at midships, at the upper height of breadth on the sheer plan, 2 ft 8 in above WL1 at
    midships and lifted toward both ends, to 8 ft 4 in at 155 ft and 8 ft 1 in at AP (measured on
    ZAZ1407 at full resolution), as Steel's rule lifts it (1805, OCR l. 15190-15194). The
    razee's is the 64's at her own line."""
    p64, p = sixty_four.hull.spec.profile, razee.hull.spec.profile
    line = p64.breadth_line_m
    assert line[0][0] == pytest.approx(x_of(0.0), abs=0.01)
    assert line[-1][0] == pytest.approx(x_of(155.0), abs=0.01)
    heights = [z for _x, z, _hb in line]
    low = heights.index(min(heights))
    assert line[low][0] == pytest.approx(0.0, abs=0.01)  # lowest at midships, 80 ft from AP
    assert heights[low] == pytest.approx(2.66 * FT, abs=0.01)
    assert all(a > b for a, b in zip(heights[:low], heights[1 : low + 1], strict=True))
    assert all(a < b for a, b in zip(heights[low:-1], heights[low + 1 :], strict=True))
    assert heights[0] == pytest.approx(8.12 * FT, abs=0.01)
    assert heights[-1] == pytest.approx(8.29 * FT, abs=0.01)
    assert max(hb for _x, _z, hb in line) == pytest.approx((21.74 + PLANK_FT) * FT, abs=0.01)
    assert [(x, hb) for x, _z, hb in p.breadth_line_m] == [(x, hb) for x, _z, hb in line]
    for (_x, z0, _hb), (_x1, z1, _hb1) in zip(line, p.breadth_line_m, strict=True):
        assert abs(z1 - z0 - RISE_M) <= 0.02


def test_her_channel_wale_lies_between_her_tiers_of_ports(sixty_four, razee):
    """`channel_wales_m`, measured on 1407F at full resolution from 10 to 160 ft: its lower edge
    8.05 ft above WL1 at 90 ft (28.7 ft above K; ZAZ2371's 28.8, Ind §2.3.5, within 0.1 ft), above
    every port of the lower deck, and 2.4 ft broad, the upper deck's ports cut into its upper
    edge abaft about 40 ft as drawn. The razee's is the 64's at her line, its top cut with her
    side in the waist to her waist's top-side, where ZAZ2371 measures it 28.8-30.7 ft above K at
    midships."""
    p64, p = sixty_four.hull.spec.profile, razee.hull.spec.profile
    wale = p64.channel_wales_m
    assert wale[0][0] == pytest.approx(x_of(10.0), abs=0.01)
    assert wale[-1][0] == pytest.approx(x_of(160.0), abs=0.01)
    mid = min(wale, key=lambda w: abs(w[0] - x_of(90.0)))
    assert mid[1] == pytest.approx(8.05 * FT, abs=0.01)
    for _x, lo, hi in wale:
        assert hi - lo == pytest.approx(2.4 * FT, abs=0.011)
    depth = dict(p64.port_size_m)["lower"][1]
    for x, sill, _hb in ports_of(p64, "lower"):
        assert sill + depth < interp([(w[0], w[1]) for w in wale], x), x
    k_at_midships = -interp(p.keel_m, 0.0)  # her water above K at midships, metres
    # between the breast at 74.4 ft and the forecastle at 118.5 ft, her rail's step a tenth of a
    # foot inside each (`the_upper_works`)
    in_waist = [w for w in p.channel_wales_m if x_of(74.45) < w[0] < x_of(118.45)]
    assert len(in_waist) >= 4
    for x, _lo, hi in in_waist:
        assert hi == pytest.approx(interp(p.rail_m, x), abs=0.011)  # cut to her waist's top-side
    at_mid = min(in_waist, key=lambda w: abs(w[0]))
    assert (at_mid[1] + k_at_midships) / FT == pytest.approx(28.8, abs=0.1)
    assert (at_mid[2] + k_at_midships) / FT == pytest.approx(30.7, abs=0.15)
    by_x = {w[0]: w for w in wale}
    kept = [w for w in p.channel_wales_m if w[0] in by_x and w not in in_waist]
    assert len(kept) >= 10
    for x, lo, hi in kept:
        assert abs(lo - by_x[x][1] - RISE_M) <= 0.02 and abs(hi - by_x[x][2] - RISE_M) <= 0.02


def test_her_head_is_the_knee_measured_on_her_draught(sixty_four, razee):
    """`head_m`, the knee of the head's fore edge: from where it leaves the stem's line at the
    band's square fore end on K, 147.75 ft from AP (keel_m's foremost point, ahead of the stem's
    foot boxed into the keel), through WL1 at 163.45 ft, 2.6 ft before the stem's fore edge, to
    the head's top 20 ft above WL1 at 174.5 ft (measured on ZAZ1407: Ind §2.3.6, and 1407F at
    full resolution); a figure stands on it (judgement). The razee's is the 64's at her own
    line, her head not measured on ZAZ2371."""
    p64, p = sixty_four.hull.spec.profile, razee.hull.spec.profile
    head = p64.head_m
    assert head[0] == pytest.approx(p64.keel_m[-1], abs=0.005)
    assert head[0][0] > p64.stem_m[0][0]
    at_water = interp([(z, x) for x, z in head], 0.0)
    assert at_water == pytest.approx(x_of(163.45), abs=0.01)
    assert at_water - interp([(z, x) for x, z in p64.stem_m], 0.0) == pytest.approx(
        2.61 * FT, abs=0.01
    )
    assert head[-1] == pytest.approx((x_of(174.46), 20.0 * FT), abs=0.01)
    assert all(a[1] < b[1] for a, b in zip(head, head[1:], strict=False))
    assert sixty_four.hull.spec.profile.form.head == razee.hull.spec.profile.form.head == "figure"
    assert [x for x, _z in p.head_m] == [x for x, _z in head]
    for (_x0, z0), (_x1, z1) in zip(head, p.head_m, strict=True):
        assert abs(z1 - z0 - RISE_M) <= 0.02


def test_her_stern_is_square_with_its_galleries_and_lights_as_measured(sixty_four, razee):
    """The 64's stern, square (1407F's body plan and sheer plan, ZAZ1953): the knuckle, where the
    side closes to the transom, at the wing transom's ends, 6 ft 4 1/2 in above WL1 and 13 ft 0 in
    out moulded, rounded up 4 in to 6 ft 9 in at the middle line, the middle the higher; the
    transom's half-breadths 9 ft 0 in at the taffrail on the side counter timber's outline and
    13 ft 0 in at the knuckle, plank on; two tiers of quarter gallery (1407F), the upper deck's
    and the quarterdeck's, forward of her stern; two bands of five stern lights (ZAZ1953), within
    10 ft 9 in and 9 ft 7 in of the middle line, at the quarter gallery's lights' heights and
    within the transom's face. The razee keeps the 64's stern up to her taffrail, and one tier
    and one band, the 64's lower ones at her line (ZAZ2371, tentative), her cabin's under her
    roundhouse; her transom at her taffrail, 22 ft above WL1 (ZAZ2371), is the outline's 9 ft
    8 in there (was 10 ft 10 in at her taffrail as filed before her roundhouse, 15.8 ft)."""
    s64, s = sixty_four.hull.spec.profile.form.stern, razee.hull.spec.profile.form.stern
    assert s64.type == s.type == "square"
    assert s64.knuckle_z_m == pytest.approx(6.38 * FT, abs=0.01)
    assert abs(s.knuckle_z_m - s64.knuckle_z_m - RISE_M) <= 0.02
    # the middle line's 6.74 ft, rounded up above the ends
    assert s64.round_up_m == s.round_up_m == pytest.approx((6.74 - 6.38) * FT, abs=0.01)
    assert s64.transom_hb_m == pytest.approx(
        ((9.03 + PLANK_FT) * FT, (12.99 + PLANK_FT) * FT), abs=0.01
    )
    assert s.transom_hb_m[1] == s64.transom_hb_m[1]
    assert s.transom_hb_m[0] == pytest.approx((9.69 + PLANK_FT) * FT, abs=0.01)  # was 10.81
    lower = (x_of(-6.9), x_of(3.7), 12.7 * FT, 17.4 * FT)
    upper = (x_of(-8.2), x_of(-0.4), 19.9 * FT, 24.4 * FT)
    assert flat(s64.galleries_m) == pytest.approx([*lower, *upper], abs=0.01)
    bands = ((13.7 * FT, 16.9 * FT, 5, 10.79 * FT), (20.9 * FT, 23.5 * FT, 5, 9.60 * FT))
    assert flat(s64.lights_m) == pytest.approx(flat(bands), abs=0.01)
    assert [n for _lo, _hi, n, _hb in s64.lights_m] == [5, 5]
    ((x_aft, x_fore, z_low, z_high),) = s.galleries_m
    assert (x_aft, x_fore) == s64.galleries_m[0][:2]
    assert (z_low - lower[2], z_high - lower[3]) == pytest.approx((RISE_M, RISE_M), abs=0.02)
    ((low, high, n, hb),) = s.lights_m
    assert (n, hb) == s64.lights_m[0][2:]
    assert (low - bands[0][0], high - bands[0][1]) == pytest.approx((RISE_M, RISE_M), abs=0.02)
    for spec in (sixty_four.hull.spec, razee.hull.spec):
        p = spec.profile
        stern = p.form.stern
        taffrail = p.stern_m[-1][1]
        top, foot = stern.transom_hb_m
        assert stern.knuckle_z_m < taffrail
        for z_lo, z_hi, _n, half in stern.lights_m:  # each band within the transom's face
            z = 0.5 * (z_lo + z_hi)
            face = foot + (top - foot) * (z - stern.knuckle_z_m) / (taffrail - stern.knuckle_z_m)
            assert half < face, (z, half, face)
    p64 = sixty_four.hull.spec.profile
    for x_a, _x_f, _z_lo, z_hi in s64.galleries_m:  # each tier forward of the 64's stern
        assert x_a > interp([(z, x) for x, z in p64.stern_m], z_hi)
    # the razee's tier and band under her taffrail and the tier forward of her stern's top, her
    # short roundhouse in her profile (ZAZ2371's note; Build-Ships.md §19.1 item 18; 2026-10-29).
    # Was: both above her taffrail as filed and the tier's after end abaft it, recorded in her
    # stern's note and not moved ("her rail and stern there are open")
    p = razee.hull.spec.profile
    assert z_high < p.stern_m[-1][1] and x_aft > p.stern_m[-1][0]
    assert high < p.stern_m[-1][1]
    assert "her rail and stern there are open" not in text_of(RAZEE)


# The main wale's edges, ft above WL1, at four of her stations (measured on 1407F at full
# resolution by columns, ±0.05 ft): its lowest at 90 ft, sweeping up into the counter aft and
# to the stem forward.
MAIN_WALE_FT = {6.0: (3.50, 7.60), 30.0: (1.31, 5.53), 90.0: (-0.83, 3.46), 150.0: (1.75, 5.97)}


def test_her_main_wale_sweeps_up_to_the_counter_and_the_stem(sixty_four, razee):
    """`wales_m`, both edges tracked on 1407F at full resolution from 1 ft from AP, where it runs
    up into the counter, to the stem at 160 ft: 4 ft 3 in broad, 10 in below WL1 at its lowest at
    85-90 ft (19.9-24.1 ft above K, where ZAZ2371 measures 20.2-24.7 at about 6 px to the foot),
    rising 6 ft aft and 3 ft 9 in forward; abaft 6 ft its upper edge, under the quarter gallery's
    lower finishing, held at its height there (judgement, so the line is judged). The razee's is
    the 64's at her line, point for point (truth 7-186)."""
    p64, p = sixty_four.hull.spec.profile, razee.hull.spec.profile
    wale = p64.wales_m
    assert wale[0][0] == pytest.approx(x_of(1.0), abs=0.01)
    assert wale[-1][0] == pytest.approx(x_of(160.0), abs=0.01)
    for station, (lo, hi) in MAIN_WALE_FT.items():
        got = [w for w in wale if abs(w[0] - x_of(station)) < 0.005]
        assert got and got[0][1:] == pytest.approx([lo * FT, hi * FT], abs=0.01), station
    lows = [lo for _x, lo, _hi in wale]
    deepest = lows.index(min(lows))
    assert wale[deepest][0] == pytest.approx(x_of(90.0), abs=0.01)
    assert all(a > b for a, b in zip(lows[:deepest], lows[1 : deepest + 1], strict=True))
    assert all(a < b for a, b in zip(lows[deepest:-1], lows[deepest + 1 :], strict=True))
    assert lows[0] - lows[deepest] == pytest.approx((5.22 + 0.83) * FT, abs=0.01)
    assert lows[-1] - lows[deepest] == pytest.approx((2.90 + 0.83) * FT, abs=0.01)
    for x, lo, hi in wale:
        if x >= x_of(8.0):
            assert 4.1 * FT <= hi - lo <= 4.35 * FT, x
    assert dict(p64.marks)["wales_m"] == dict(p.marks)["wales_m"] == "judged"
    # it ends inside her stern's and her stem's lines
    assert wale[0][0] > interp([(z, x) for x, z in p64.stern_m], wale[0][2])
    assert wale[-1][0] < interp([(z, x) for x, z in p64.stem_m], wale[-1][1])


def test_the_razees_side_is_the_64s_at_her_rails(sixty_four, razee):
    """Her side below her rails is the 64's cut down (Build-Ships.md §5.0 principles 1 and 10;
    Indf §1.5): at the top of her side under her quarterdeck and forecastle rails, `breadth_m`
    takes the 64's side at her rail's height, between the 64's main-breadth line at its height of
    breadth and its top-timber line at the 64's rail, along the midship section's shape (her
    quarterdeck rail about 34 ft across at midships: Ind §2.3.2), not the top-timber line, the
    64's breadth at the 64's own rails 3-10 ft higher. Her rail's half-breadth so taken stands
    within 0.2 m of the 64's drawn side there (measured: 0.18 m at 10 ft from AP, where the rule
    and the section's shape part most), and the two draw her timbers within 0.25 m of each other
    at the same heights (measured: 0.17 m under her quarterdeck and forecastle, 0.24 m in the
    waist under her top-side, the rule's fit between the breadth and her rail; up to 0.45 m
    before), and alike under the water, within 2 cm."""
    from freesail.ship import form

    s64, s = sixty_four.hull.spec, razee.hull.spec
    p = s.profile
    for x, _hw, hr in p.breadth_m[1:-1]:  # the post and 155 ft, the rule's ends, left out
        rail = interp(p.rail_m, x)
        if rail > 4.0:  # under her quarterdeck and forecastle rails
            assert hr == pytest.approx(form.half_breadth_at(s64, x, rail - RISE_M), abs=0.2), x
        for z in (-1.0, 0.5, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5):
            if z < rail - 0.05:
                here, there = (
                    form.half_breadth_at(s, x, z),
                    form.half_breadth_at(s64, x, z - RISE_M),
                )
                assert here == pytest.approx(there, abs=0.25), (x, z)
                if z <= 0.5:
                    assert here == pytest.approx(there, abs=0.02), (x, z)


def test_her_drawn_hull_stands_within_its_bands_and_moves_nothing():
    """The drawing never changes how she sails or fights (Build-Ships.md §5.0 principle 8): her
    drawn displacement within 2% of the filed (2,158 t against 2,170 and 1,906 against 1,925,
    measured), and every port triple's gap to the drawn side at its sill within 0.40 m (the worst
    the 64's upper deck at +0.39, her waist's tumblehome; the razee's chase port at -0.35,
    measured). None was measured at its port (Indf §3.3), so none raises and none is moved. The
    figures are the generator's report's and these bands', not her notes' (below)."""
    from freesail.ship import form

    for path in (SIXTY_FOUR, RAZEE):
        hull = load_spec(path).hull
        share = form.drawn_displacement_kg(hull) / hull.displacement_kg - 1.0
        assert abs(share) <= 0.02, (path, share)
        gaps = [
            form.half_breadth_at(hull, x, sill) - hb
            for _word, triples in hull.profile.ports_m
            for x, sill, hb in triples
        ]
        assert max(abs(gap) for gap in gaps) <= 0.40, (path, min(gaps), max(gaps))


# What a rule computes from the file's own keys, as her notes once said it and the shared helpers
# still do for the eight: hull_form's drawn figures, a rating, a staysail's area and sides, a
# rope's size and scale, a count of men, a heel, what her tuning measured.
NOT_IN_HER_NOTES = (
    "The hull as drawn",
    "drawn displacement",
    "deep at the greatest section",
    "off the half-breadth by",
    "Measured again",
    "seed 7",
    "men at the guns",
    "trimmers are",
    "tons in iron-hooped",
    "root(",
    "in a side",
    "her 351 seamen",
    "her 238 seamen",
    "default fit, ",
    "714 lb",
    "33-34 ft",
    "one of the eighty-four",
    "one of the fifty",
    "open for B1",
    "as proposed (open: Indf",
    "pp. 41-42",
)
NOT_IN_HER_NOTES_RE = (
    r" -> [0-9.]+ kN",
    r"[0-9] kN(?!/m2)",
    r"staysail [0-9.]+ m2",
    r"rope's [0-9]",
    r"^# [0-9.]+ in[,:]",
    r"lighter rope than the sheet, [0-9.]+ in",
    r"[0-9.]+ deg of (weather|lee) helm",
)


@pytest.mark.parametrize("path", [SIXTY_FOUR, RAZEE])
def test_her_notes_carry_sources_departures_and_judgements_and_no_figure_a_rule_computes(path):
    """The lead's notes of 2026-10-29, item 2: the files' notes carry sources, departures and
    judgements, not figures a rule computes from the file's own keys (an area from a cut, a heel
    from a sill); those live in the generator's report and the tests, where they cannot go stale.
    What each rule read stays in its note: which sails a spar is rated for and in what wind, the
    rope a line is scaled from."""
    said = [line.strip() for line in text_of(path).splitlines() if line.strip().startswith("#")]
    for words in NOT_IN_HER_NOTES:
        assert not [line for line in said if words in line], words
    for pattern in NOT_IN_HER_NOTES_RE:
        hits = [line for line in said if re.search(pattern, line)]
        assert not hits, (pattern, hits[0][:200])
    text = "\n".join(said)
    assert "Rating: fore.course in 55 kn." in text
    assert "Tuned against" in text or "tuned against" in text
    assert "docs/dev/TuningNotes.md" in text
    if path == SIXTY_FOUR:
        # what the file's own cut says sets its driver's jaws, the boom's note and the sail's alike
        assert "the jaws set by the boom's head room (the boom's note)" in text
        assert "and the least that also keeps the driver's after leech" not in text
        # the course's tack is Steel's words read, the lead's ruling of 2026-10-30, not a head room
        assert "Steel's words read, 'within 6 or 7 feet of the deck'" in text
        assert "the deck being the deck the mast stands through there" in text
        assert "and not a head room" in text
        assert "taken for the foot: judgement" not in text
        # the boom's key and why (Ext §17.11)
        assert "Rigged in on the booms while the driver is in the sail room" in text
        # the owner chose four staysails for the table; the fifth is judgement, and says so
        assert (
            "as the owner chose for the other four (2026-10-29; Indf §17), judgement for this one"
            in text
        )
    else:
        # the departure the razee's clr makes from her start, stated
        assert "Forward of that at stage B, her spanker cut smaller" in text
        # her roundhouse's after face, judged for the eye (Indf §17 item 1; Build-Ships.md §5.8)
        assert "Her roundhouse's after face is drawn plain" in text
        assert "ZAZ2371 being a side elevation that cannot show that face" in text
        # the boom at the least that clears her taffrail, and the owner's 218 said plainly
        assert "at literally the least that clears her taffrail" in text
        assert "cannot keep 218" in text


REPORT_PROBE = """
import sys
sys.path.insert(0, "tools")
import gen_ships
sys.modules["gen_ships"] = gen_ships
from ships import indefatigable as her
her.build(sys.argv[1])
"""


def test_the_generators_report_prints_what_her_notes_no_longer_carry(tmp_path):
    """`her_report()`, printed to the standard error as her files are written: the hull as drawn
    (`g.hull_form`'s report, the eight files' notes untouched since none calls it), her rope's
    scale, the quarter bill's arithmetic, the razee's upper works and the cuts of her after sail
    and her yards under the bowsprit. Her files come out as they stand."""
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
    for key, path, filed in (("sixty-four", SIXTY_FOUR, 2170), ("razee", RAZEE, 1925)):
        hull = load_spec(path).hull
        drawn = "the hull as drawn (freesail/ship/form.py):"
        assert f"{key}: {drawn} drawn displacement " in said
        assert f"against the filed {filed} t" in said
        assert said.count(f"{key}: {drawn} the ") == len(hull.profile.ports_m)
        assert f"{key}: plain sail " in said and "her rope's scale 1." in said
        assert (ROOT / path).read_bytes() == (tmp_path / Path(path).name).read_bytes()
    assert (
        "her 351 seamen, 296 men at the guns, 0 of them marines, and 2 at the wheel leave 53"
        in said
    )
    assert (
        "her 238 seamen, 193 men at the guns, 36 of them marines, and 2 at the wheel leave 79"
        in said
    )
    assert "razee: her taffrail 7.15 m above her water" in said
    assert "sixty-four: mizen course: tack 8.73 m above her water, 6.5 ft above" in said
    assert "sixty-four: driver: jaws 9.69 m, set by the clearance" in said
    assert "razee: spanker boom: jaws 7.16 m" in said
    assert "spanker 200 m2 (was 218)" in said
    # the boom's overhang, which left its note; 29.4 ft now, her taffrail where it is filed and
    # the jaws a little forward on the raked mast (29.5 at the jaws of 7.85 m)
    assert "its end 29.4 ft beyond it" in said
    # the sprit topsail as the viewer draws it (`squareCut`), risk 9 closed, not "to come"
    assert "as built): head 9.30, foot 15.75, the file's area; risk 9 closed." in said
    assert "slant remedy" not in said


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
        # the bowsprit 60 ft 4 in, 44.4 ft of it outboard of the stem head from its heel measured
        # on ZAZ1280 (±1 ft; 46.3 ft from the knighthead's cap at stage A); the jib-boom 43 ft 9 in,
        # seven twelfths outboard (the frigate's rule)
        assert abs(units.m_to_feet(sp["bowsprit"].length_m) - 44.4) <= 1.0
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
    # the main truck: Steel's lower mast, topmast and topgallant mast with its long pole-head set
    # up on her measured heel, each doubling a head by Steel's rule, 51.7 m above her water (47.2
    # on stage A's common pole within the listed length)
    truck = sum(s.height_m for s in sixty_four.spar_chain("main.royal_mast"))
    assert truck + sixty_four.hull.spec.deck_height_m == pytest.approx(51.7, abs=0.2)
    # her brace limits are the frigate-36's (Fincham 1843 art. 102; Indf §4.2, judgement): the
    # lee lower shrouds do not stop her lower yards before 70 degrees (measured on 1407F), and the
    # owner keeps them, the lee topmast backstays eased when braced sharp up (2026-10-29: Indf §17)
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
        # Build-Ships.md §19.1 item 5), on Steel p. 42's long pole-heads: each cut between its
        # yard and the yard below, near the table's sail (0.88-0.91 measured; 0.58-0.60 on stage
        # A's common pole within the listed length)
        for sid, row in STEEL_ABOVE_THE_CAPS.items():
            assert 0.85 <= areas[sid] / steel_m2(*row) <= 0.95, sid
        # the main topsail the largest sail, as the frigate-36's
        assert max(areas, key=areas.get) == "main.topsail"
        assert areas["main.course"] > areas["fore.course"] > areas["mizzen.topsail"]
    # the 64's mizen course, cut at the mast on her mizen yard (Indf §4.4; Ext §3.4): Steel's 14
    # 1/2 cloths at the head and 15 1/2 at the foot, its leeches 9 1/4 and 17 1/4 yards
    course = sixty_four.sails["mizzen.course"]
    steel = 15.0 * CLOTH_FT * (9.25 + 17.25) / 2.0 * 3.0 * SQ_FT
    assert abs(course.area_m2 / steel - 1.0) <= 0.10 and course.cls == "lateen"
    assert sixty_four.spars["mizzen.yard"].cls == "lateen_yard"  # gaff at stage A, the stand-in
    # the razee's spanker on her gaff of 40 ft 10 in and driver boom of 65 ft 4 in (Steel p. 40:
    # the boom the main topsail yard's length, the gaff five eighths of it; D20 (a)), by the
    # frigate's rule on her spars within 8% of Steel's driver for a 38, 202 m2 (table IV, read on
    # the page image: Indf §3.5 item 6), as the owner settled it (2026-10-29: Indf §17): 218 m2
    # with the boom through her cabin, 200 with its jaws at the least that clears her taffrail
    # (the clew check, below). (Was ±10% of 202; before that 216-264 m2, Indf §4.5's 240 ±10%.)
    assert razee.spars["mizzen.boom"].length_m == pytest.approx((65.0 + 4.0 / 12.0) * FT, abs=0.06)
    assert razee.spars["mizzen.gaff"].length_m == pytest.approx((40.0 + 10.0 / 12.0) * FT, abs=0.06)
    assert abs(razee.sails["mizzen.spanker"].area_m2 / 202.0 - 1.0) <= 0.08
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
# an upper bound. Steel's 64 has no mizen topgallant staysail, and she carries none.
STEEL_BETWEEN = {
    "main.staysail": (102.0, 0.10),
    "main.topmast_staysail": (190.0, 0.25),
    "middle_staysail": (110.0, 0.25),
    "main.topgallant_staysail": (90.0, 0.25),
    "mizzen.staysail": (100.0, 0.25),
    "mizzen.topmast_staysail": (80.0, 0.25),
}


def test_her_staysails_between_the_masts_stand_within_steels_table_iv(sixty_four, razee):
    """Indf §4.3 and §17 (the owner, 2026-10-29: "Agreed"): every staysail between the masts
    within its band of Steel's table IV for a 64. The main, middle, mizen and mizen topmast
    staysails are cut to the table's own figures, where the generator's rules on her spars left
    them outside (old beside new, the 64's and the razee's alike to a square metre: the main
    staysail 129 m2, +26%, now 102, +0%; the middle 78, -29%, now 110-111, +0-1%; the mizen 65,
    -35%, now 101, +1%; the mizen topmast 112, +40%, now 78, -3%); the main topmast (225, +18%)
    and main topgallant (80, -11%) are kept as those rules cut them; and the mizen topgallant
    staysail (54 m2), which the table's 64 column has not, is gone with its stay, its lines and
    its names, from both files. The razee's canvas is the 64's column, as her design gives it.
    Stage B: the generator's rule followed her long pole-heads' main topgallant to +26% of the
    table (113 m2 on the 64), so it is cut to the table with the other four, 109 m2, +21% (80 at
    stage A, -11%)."""
    for ship in (sixty_four, razee):
        between = ship.groups["staysails between the masts"]
        assert set(between) == set(STEEL_BETWEEN)
        for sid, (steel, band) in STEEL_BETWEEN.items():
            assert abs(ship.sails[sid].area_m2 / steel - 1.0) <= band, (
                sid,
                ship.sails[sid].area_m2,
            )
        assert "mizzen.topgallant_staysail" not in ship.sails
        assert "mizzen.topgallant.stay" not in ship.lines
        assert not [
            ln for ln in ship.lines.values() if ln.id.startswith("mizzen.topgallant_staysail")
        ]
        for name, members in ship.groups.items():
            assert "mizzen.topgallant_staysail" not in members, name
        # the main staysail, a triangle of Steel's 28 cloths and 14 yards square at the clew
        assert ship.sails["main.staysail"].area_m2 == round(
            0.5 * 28.0 * CLOTH_FT * 14.0 * 3.0 * SQ_FT
        )
    # her lying-to staysail is the main staysail, as the frigate-36's (package 57)
    assert sixty_four.groups["lying-to staysails"] == ["main.staysail"]


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
def test_her_quarters_at_the_beat_fill_every_gun_and_leave_the_trimmers_measured(
    path, marines, at_long_guns, trimmers
):
    """Indf §6.4 and §16 item 5: `Quarters.beat` measured at muster on each default fit (the
    generator's report gives the bill's arithmetic). Every gun crew fills; the beat takes the
    marines to the long guns before the topmen (crew/quarters.py; the engine's order, open for the
    lead), so no marines' division forms, as on the frigate-36 (Indf §18 item 13), and the topmen
    the guns leave fall to the trimmers, above the bill's 53 and 79. Measured at seed 7."""
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
    bill = doc_of(path)["crew"]["quarter_bill"]["trimmers"]
    assert sum(bill.values()) == {SIXTY_FOUR: 53, RAZEE: 79}[path]


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
                "driver",
                "spanker",
                "driver boomsail",
                "driver boom",
                "spanker boom",
                "spritsail",
                "sprit topsail",
                "spritsail topsail",
                "spritsail yard",
                "sprit topsail yard",
                "spritsails",
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
                "spritsail",
                "spritsail yard",
                "crossjack",
                "cro'jack yard",
                "fore staysail",
                "middle staysail",
                "mizen topmast staysail",
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
    grammar hands them to the resolver, the article already gone. On her 64 'the spanker' and
    'the driver' are Steel's driver in the sail room (Ext §17.2; stage A's 64 had neither), her
    after sail the mizen course. Neither carries a mizen topgallant staysail (Steel's 64 column
    has none: Indf §17), and its name finds nothing; the razee crosses no sprit-topsail yard (the
    owner: Indf §17 item 5)."""
    table = noun_table(load_ship(path))
    for phrase in phrases:
        assert table.lookup(phrase) is not None, phrase
    for word in ("mizen", "mizzen"):
        assert table.lookup(f"{word} topgallant staysail") is None
    if path == SIXTY_FOUR:
        assert table.lookup("spanker").ids == ["mizzen.driver"]
        assert table.lookup("mizen").ids == ["mizzen.course"]
    else:
        assert table.lookup("sprit topsail") is None


# ---------------------------------------------------------------------------
# Her polars (Indf §9), in tests/test_ships.py's form
# ---------------------------------------------------------------------------


def test_her_polars_are_drawn_from_her_files_and_agree_with_her_sailed_beam_reaches():
    """`polar_of` balances the sails model against the hull's resistance at each angle off the
    wind (tests/test_ships.py:74-93). Her beam reaches in fifteen knots are within half a knot
    of those she sails under plain sail with the yards trimmed, the known truths' polar form
    (`under_plain_sail` at 90 deg): the 64 7.55 kn, the razee 7.86 kn (measured, seed 7; stage A
    7.50 and 7.79). By `polar_of`, old beside new at stage B: the 64's best 4.25, 7.59 and 10.92
    kn in 8, 15 and 25 kn now 4.29, 7.64 and 11.00; the razee's 4.41, 7.93 and 11.54 now 4.46,
    8.02 and 11.64; the frigate-36's 4.62, 8.19 and 11.63; all three closest at 50 deg; the razee
    and the frigate beat at 60, the 64 at 70 (60 at stage A: 3.92 kn at 60 now against 3.98, 5.78
    at 70, a hair's difference in the made good). Indf §9's targets that hold: the razee above
    the 64
    she was cut from, her best in 25 kn at or above the Virginie chase's mean of 11.2 kn
    (Osler p. 125; Gazette 13887 p. 388; D24), and her closest within a step of the
    frigate-36's (the brace limits the frigate's: Indf §4.2). The razee outsailing the
    frigate-36 close-hauled and running large does not hold (truth 7-187's docstring)."""
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
# Her helm as tuned (Indf §9, §16 items 3 and 6): truths 6 and 17 on her files
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "path, after, helm_band",
    [(SIXTY_FOUR, "mizzen course", (0.1, 1.0)), (RAZEE, "spanker", (1.0, 2.5))],
    ids=["sixty-four", "razee"],
)
def test_her_helm_as_tuned_holds_truths_6_and_17(path, after, helm_band):
    """`clr_x_m` tuned with the rig whole (Indf §9's knob; docs/dev/TuningNotes.md, old beside new;
    measured at seed 7 in fifteen knots), in the forms of truths 6 and 17.

    **The 64, +4.8 m** (+5.2 at stage A; +5.0 takes her aback getting under way, 34.7 deg off with
    1.32 kn of sternway, and +4.9 holds, 58.5 deg off): measured again on her course's tack at 8.73
    m and kept. Truth 6's form 0.43 deg on the beam, 2.24 with the headsails in, 0.72 of lee helm
    with the mizen course in (the tack at 9.43 m 0.44, 2.25, 0.71; stage A 0.89, 2.72, 0.43); truth
    17's form no nearer than 61.0 deg off and settled in 424 s (60.5, 428; 65.2, 345); weather helm
    from seven points to eleven, +0.17, +0.43, +0.80 at seven points, the beam and ten points
    (+0.19, +0.44, +0.80; stage A +0.75, +0.89, +1.12).

    **The razee, +4.5 m** (+4.1 from stage A to the first of stage B): her spanker cut smaller on
    its raised boom took her helm away, and +4.5 gives it back. Measured again on the spanker of
    200 m2 and kept: +1.51 on the beam and +2.17 at 60 deg (191 m2 +1.42, +1.72; stage A, 218 m2 at
    +4.1, +1.41, +2.23; 200 m2 at +4.1 +1.17, +1.20), within 0.10 deg of stage A at each of 60 deg,
    seven points, the beam, ten points and 120 deg, though not within the first reading's 0.05 deg
    at seven points, the beam and nine points (+0.09, +0.10, +0.07; +4.4 would give +0.06, +0.02,
    0.00, and less time in stays, which the notes put to the lead); 1.30 to 2.09 deg from six
    points to eleven
    against the frigate-36's 1.45 to 2.19; truth 6's form 1.51, 3.49, 0.86 (1.42, 3.40, 0.88; stage
    A 1.41, 3.48, 1.15); truth 17's 59.6 deg off, 375 s (59.7, 375; stage A 66.1, 389)."""
    from tests.test_known_truths import (
        events,
        headway_kn,
        knots,
        make,
        off_wind,
        reading,
        run,
        under_plain_sail,
    )

    world = under_plain_sail(path, 270.0)
    plain = math.degrees(world.ship.dyn.weather_helm)
    assert helm_band[0] <= plain <= helm_band[1], plain
    world.submit("take in the headsails")
    run(world, 900, trim_every=120)
    without_headsails = math.degrees(world.ship.dyn.weather_helm)
    assert without_headsails > plain + 1.0
    world.submit("set the headsails")
    world.submit(f"take in the {after}")
    run(world, 900, trim_every=120)
    without_after = math.degrees(world.ship.dyn.weather_helm)
    assert without_after < 0.0 and without_after < plain

    for off in (78.75, 112.5):  # seven points and ten: weather helm, the 64's small
        helm = reading(under_plain_sail(path, off))["weather_helm"]
        assert helm_band[0] <= helm <= helm_band[1], (off, helm)
    # six points, her own close-hauled course (for the lead: TuningNotes). The 64's lee helm there
    # is the one to watch: -0.95 deg (the tack at 9.43 m -0.91; stage A -0.05; the razee +2.09; the
    # frigate-36 +1.45)
    six_points = {SIXTY_FOUR: (-1.5, 0.0), RAZEE: (1.0, 2.5)}[path]
    helm = reading(under_plain_sail(path, 67.5))["weather_helm"]
    assert six_points[0] <= helm <= six_points[1], helm

    world = make(path, 293.0, speed_kn=0.0)
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
    assert events(world, "ship.aback") == []
    assert min_off > 45.0 and sternway < 0.5, (min_off, sternway)
    assert settled_at is not None and settled_at <= 600, settled_at
    assert knots(world) > 4.0


def test_the_razee_stays_wears_and_lies_to_in_the_frigates_bands():
    """Truths 10, 11 and 12's bands on the razee as tuned, measured at seed 7: from 290, 292.5 and
    295 degrees she tacks in 435, 427 and 484 s, gaining 85, 78 and 18 m (her spanker at 191 m2:
    405, 400 and 471 s, 84, 77 and 34 m; the frigate-36 343, 447 and 370 s, 51, -37 and 25 m; at
    +4.1 she takes 367, 356 and 416 s); she wears in 494 s (the frigate-36 513 s); hove to she lies
    57.6-63.2 deg off at 1.16 kn at most (the frigate-36 58.4-61.8, 1.38)."""
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

    for heading in (290.0, 292.5, 295.0):
        world = close_hauled_on_starboard(RAZEE, heading=heading)
        y_before = world.ship.dyn.y
        world.submit("tack ship")
        done, seconds = until(world, ("ship.tacked", "ship.missed_stays"), 900)
        assert [e.kind for e in done] == ["ship.tacked"], heading
        assert 285 <= seconds <= 600, (heading, seconds)
        assert world.ship.dyn.y > y_before, heading
    seconds, _lost = wear(close_hauled_on_starboard(RAZEE))
    assert 360 <= seconds <= 720, seconds
    world = hove_to(RAZEE)
    run(world, 300)
    offs, speeds = [], []
    for _ in range(600):
        world.tick()
        offs.append(off_wind(world))
        speeds.append(knots(world))
    assert max(speeds) < 1.6
    assert all(45.0 <= o <= 65.0 for o in offs), (min(offs), max(offs))
    assert events(world, "ship.hove_to") and events(world, "ship.aback") == []


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
    polar form at seed 7: the razee 4.28 deg at 7.86 kn, stage A 4.04 at 7.79; the 64 4.90 deg at
    7.55 kn, stage A 4.6 at 7.50; the frigate-36 5.46 deg at 7.97 kn). Pinned at once.

    **The speed clause, pinned at stage B** (Build-Ships.md §15): her speed greater at every
    angle from her closest to 180 degrees in 15 and 25 kn (`polar_of`: by 0.15-0.38 kn in 15 kn
    and 0.33-0.69 kn in 25 kn; with the spanker at 191 m2 0.13-0.36 and 0.32-0.67; on the 64's
    stand-in 0.16-0.34 and 0.33-0.66).

    **Not pinned: the razee outsailing the frigate-36** (Indf §14 truth 4; D24; the Virginie
    chase). Her best in 25 kn, 11.64 kn, meets the chase's mean of 11.2 and stands 0.01 over the
    frigate-36's; but in 15 kn she is under the frigate-36 close-hauled and running large
    (`polar_of`: 60 deg 4.15 against 4.29, 70 deg 6.00 against 6.14, 120 deg 7.64 against 7.86, 130
    deg 7.26 against 7.40, 140 deg 6.86 against 6.99, 150 deg 6.43 against 6.53; with the spanker
    at 191 m2 4.14, 5.99, 7.63, 7.25, 6.85, 6.43; stage A 4.17, 5.97, 7.60, 7.21, 6.81, 6.39), and
    sailed (60 deg 3.53 against 3.63, 120 deg 7.51 against 7.53; stage A 3.60 and 7.47).
    `hull_speed_kn` at the top of D24's band, 14.5, raises her
    15-kn figures at those angles by 0.03 kn at most (7.67, 7.28, 6.88, 6.45; 60 deg not at all, 70
    deg by 0.01); `clr_x_m` does not reach the polar (+4.1 to +5.1 m measured, no figure moved); the
    brace limits move only with a source. Reported, not forced (Indf §9). The owner (2026-10-29;
    Indf §17) leaves it to the tuning of both ships against the period's accounts, neither presumed
    the one at fault: the razee may be right and the frigate-36 too fast, or the razee too slow
    and the frigate-36 right."""
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
    from freesail.world import ships as S

    p64, p = S.polar_of(SIXTY_FOUR), S.polar_of(RAZEE)
    for wind in (15.0, 25.0):
        for angle in p.angles_deg:
            if angle >= p.closest_deg:
                assert p.speed_kn(angle, wind) > p64.speed_kn(angle, wind), (angle, wind)


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


# ---------------------------------------------------------------------------
# Stage B: her rig (Indf §13 step 7; the lead's notes of 2026-10-29, item 2)
# ---------------------------------------------------------------------------

YD = 3.0 * FT
LEAN_OK_M = 0.1  # a corner on its line within a decimetre (Ext §3.4, §17.2)
HEAD_ROOM_M = 6.0 * FT  # the 74's head room (Bel §4.6), which the 64's driver boom keeps
ROUNDING_M = 0.02  # the files' corners and heights kept to the centimetre
# Steel's table IV, the 64 (Ind §5): the mizen course's and the driver's cloths at the head and
# the foot and fore and after leeches in yards; the sprit course's and sprit topsail's.
COURSE_ROW = (14.5, 15.5, 9.25, 17.25)
DRIVER_ROW = (22.5, 29.0, 9.5, 20.0)
DRIVER_YARD_M = 34.5 * FT  # Steel p. 40, the fore topgallant yard's length (Ext §17.2)


def corners_above_water(ship, sail_id):
    """A sail's `corners_m`, the file's heights above the datum made heights above her water."""
    deck = ship.hull.spec.deck_height_m
    return [(x, z + deck) for x, z in ship.sails[sail_id].corners_m]


def mast_x_at(ship, mast_id, z_above_water):
    """x on a lower mast's raked line at a height above her water (`x_m` is its place at the
    datum: `tools/ships/indefatigable.py`, `mast_x_at_datum`)."""
    spar = ship.spars[mast_id]
    z = z_above_water - ship.hull.spec.deck_height_m
    return spar.x_m - math.tan(spar.rake) * z


def polygon(pts):
    """Area and centroid of a polygon's corners."""
    pts = list(pts)
    a = cx = cz = 0.0
    for (x1, z1), (x2, z2) in zip(pts, pts[1:] + pts[:1], strict=True):
        cross = x1 * z2 - x2 * z1
        a += cross
        cx += (x1 + x2) * cross
        cz += (z1 + z2) * cross
    a *= 0.5
    return abs(a), cx / (6.0 * a), cz / (6.0 * a)


def steel_mean_m2(head, foot, fore_yd, after_yd):
    """Steel's rule for a driver or a mizen (vol. I, OCR l. 10891-10897), square metres."""
    return (head + foot) / 2.0 * CLOTH_FT * (fore_yd + after_yd) / 2.0 * 3.0 * SQ_FT


def roundhouse_of(ship):
    """Her roundhouse deck's line, (x, z above her water): `decks_m`, at the side on the 64."""
    return dict(ship.hull.spec.profile.decks_m)["roundhouse"]


def roundhouse_z(ship, x):
    """Her roundhouse deck at `x`, metres above her water."""
    return interp(roundhouse_of(ship), x)


def doc_of(path):
    return yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))


def lines_of(ship, of):
    return [ln for ln in ship.lines.values() if ln.of == of]


@pytest.mark.parametrize("path", [SIXTY_FOUR, RAZEE])
def test_her_topgallants_and_royals_stand_on_steels_long_pole_heads(path):
    """Steel 1794 vol. I p. 16 (OCR l. 2934-2942) and p. 42 (OCR l. 4701-4702), read as Bel §4.2
    reads them; the owner (2026-10-29, "Agreed": Indf §17). The table's topgallant length is the
    mast with a square head of 3 1/2 in to a yard; the long pole-head takes that head's place,
    two-thirds of the length to the stop,
    set up from the stop. So the topgallant mast's hoist above the topmast cap is the length to
    the stop less the topmast's head, and the pole, filed as a royal mast, stands above it, on
    both her files, the razee's upper masts being the 64's (Indf §4.1-§4.2). The topgallants and
    royals are cut between their yards as the spars so stand, Steel's cloths kept (the owner's
    spars rule). Old beside new, m2 (Steel's table IV in brackets), both files alike: main
    topgallant 66 to 101 (111), fore 52 to 80 (88), mizen 35 to 53 (58); main royal 37 to 56 (64),
    fore 29 to 44 (50), mizen 18 to 28 (31); the 64's plain sail 1,722 to 1,803, the razee's
    1,836 to 1,899 (her spanker at 200 m2), her rope scaled with it; the main truck above the water
    47.2 to 51.7 m on the
    64, 45.7 to 50.2 on the razee. In light airs the gain is small (4 kn on the beam, by
    `_balanced_speed_ms`, the 64 2.14 to 2.16 kn and the razee 2.21 to 2.24: `polar_of`'s docstring
    above gives her polars)."""
    ship = load_ship(path)
    head_in = {"main": 4.0, "fore": 4.0, "mizzen": 3.5}  # the topmast heads, Steel OCR l. 4697-4699
    length_ft = {"main": 29.25, "fore": 26.5, "mizzen": 21.75}  # Steel p. 49, the 64
    topmast_ft = {"main": 58.5, "fore": 53.0, "mizzen": 43.5}
    for mast, g_len in length_ft.items():
        square = g_len / 3.0 * 3.5 / 12.0
        to_stop = g_len - square
        t_head = topmast_ft[mast] / 3.0 * head_in[mast] / 12.0
        hoist = ship.spars[f"{mast}.topgallant_mast"].height_m
        pole = ship.spars[f"{mast}.royal_mast"].height_m
        assert hoist == pytest.approx((to_stop - t_head) * FT, abs=0.06), mast
        assert pole == pytest.approx(2.0 / 3.0 * to_stop * FT, abs=0.06), mast
        # the room the two yards leave a sail, against the table's depth (Bel §4.2's table's form)
        tg = ship.spars[f"{mast}.topgallant.yard"].height_m
        royal = ship.spars[f"{mast}.royal.yard"].height_m
        below = ship.spars[f"{mast}.topsail.yard"].height_m
        assert (tg - below) / (STEEL_ABOVE_THE_CAPS[f"{mast}.topgallant"][2] * YD) > 0.88
        assert (royal - tg) / (STEEL_ABOVE_THE_CAPS[f"{mast}.royal"][2] * YD) > 0.84


@pytest.mark.parametrize("path, steeve_deg", [(SIXTY_FOUR, 0.15), (RAZEE, 0.3)])
def test_her_bowsprit_lies_on_the_stem_head_at_her_steeve(path, steeve_deg):
    """Indf §3.5 item 9, Ext §6.2 as built: ZAZ1407F draws the bowsprit lying on the stem head,
    about 4 ft below the knighthead's cap stage A rooted it at, and at the measured 27 degrees
    (±2; Ind §3.1). Rooted there, old beside new: x_m 24.63 to 25.15 m, the stem head's; outboard
    46.3 to 44.4 ft (14.1 to 13.5 m), the heel measured just before the fore mast; the end's
    height above the 64's datum 9.3 to 7.8 m (its x kept); the jib-boom's end 12.8 to 11.3 m.
    The viewer draws from the stem head to the file's end at the file's length, so the drawn
    steeve is 27.05 deg on the 64 (32.8 before) and 27.2 from the razee's stem head (the viewer
    lowers her heel to her rail's end there, 0.12 m, and draws 27.8: B5's rule, within the
    ±2). The stays' leads follow: the fore stay's collar half way out, the fore topmast stay at
    the bowsprit's end, the jib's at the jib-boom's; the fore staysail's tack 6.08 to 4.73 m above
    the datum and the fore topmast staysail's 9.28 to 7.80, each on the line."""
    ship = load_ship(path)
    h = ship.hull.spec
    stem_x, stem_z = h.profile.stem_m[-1]
    bs, jb = ship.spars["bowsprit"], ship.spars["jib_boom"]
    assert bs.x_m == pytest.approx(stem_x, abs=0.01)
    end_z = h.deck_height_m + bs.height_m
    assert math.degrees(math.asin((end_z - stem_z) / bs.length_m)) == pytest.approx(
        27.0, abs=steeve_deg
    )
    s, c = math.sin(math.radians(27.0)), math.cos(math.radians(27.0))
    assert units.m_to_feet(bs.length_m) == pytest.approx(44.4, abs=1.0)
    end_x = bs.x_m + bs.length_m * c
    jib_z = h.deck_height_m + jb.height_m
    assert (jib_z - end_z) / jb.length_m == pytest.approx(s, abs=0.02)
    # the stays' feet on the line: each headsail's tack, the collar half way out the bowsprit
    tacks = {sid: corners_above_water(ship, sid)[0] for sid in ship.groups["headsails"]}
    assert tacks["fore.topmast_staysail"] == pytest.approx((end_x, end_z), abs=0.1)
    collar = (bs.x_m + 0.5 * bs.length_m * c, stem_z + 0.5 * bs.length_m * s)
    assert tacks["fore.staysail"] == pytest.approx(collar, abs=0.1)
    jib_end = (end_x + jb.length_m * c, end_z + jb.length_m * s)
    assert tacks["jib"] == pytest.approx(jib_end, abs=0.1)


def test_the_64s_mizen_course_is_cut_at_the_mast_on_her_whole_yard(sixty_four):
    """Ext §3.4 on her file (D9 (c); Bel §13.5): the yard a lateen yard, Steel's whole 77 ft 0 in
    by 14 in, slung at its truss with its fore part bare (Ind §3.1's 0.53 of it), not braced; the
    sail a lateen cut at the mast, on the gaff's curve, its tack and throat on the mast's raked
    line, its head along the yard, its foot loose; one reef band; canvas as the stand-in's. Old
    beside new, on the stand-in of stage A: class `gaff` to `lateen`; the yard class `gaff`, 11.1
    m, to `lateen_yard`, 23.5 m; the lateral offset 0.5 x 0.8 sqrt(A) x sin(sheet), 8.16 m of
    arm, in place of the stand-in's whole 11.1-m head (Ext §3.2; Indf §16 item 3), which is what
    moved her balance (`clr_x_m`'s note); the lines the jeers, lifts, derrick, vangs, bowlines,
    sheet and tack of Ext §3.4 for the throat and peak halyards, sheet, vangs and lifts."""
    ship = sixty_four
    yard, course = ship.spars["mizzen.yard"], ship.sails["mizzen.course"]
    assert yard.cls == "lateen_yard" and not yard.is_yard
    assert yard.length_m == pytest.approx(77.0 * FT, abs=0.05)
    assert ship.mast_of(yard).id == "mizzen.mast"
    assert yard.brace_limit == 0.0 or yard.brace_limit is None
    assert course.cls == "lateen" and course.cut_at_mast and course.curve_class == "gaff"
    assert ship.spar_of_role(course, "yard") is yard
    assert ship.spar_of_role(course, "mast") is ship.spars["mizzen.mast"]
    assert ship.spar_of_role(course, "boom") is None and ship.spar_of_role(course, "gaff") is None
    assert ship.sail_of(yard) is course
    tack, throat, peak, clew = corners_above_water(ship, "mizzen.course")
    for corner in (tack, throat):
        assert corner[0] == pytest.approx(mast_x_at(ship, "mizzen.mast", corner[1]), abs=LEAN_OK_M)
    assert yard.height_m + ship.hull.spec.deck_height_m == pytest.approx(throat[1], abs=ROUNDING_M)
    # Steel's cut (Ext §2): the head 27.2 ft aft and 24 ft up, the foot level and 8.86 m
    assert throat[0] - peak[0] == pytest.approx(14.5 * CLOTH_FT * FT, abs=ROUNDING_M)
    assert peak[1] - throat[1] == pytest.approx((17.25 - 9.25) * YD, abs=ROUNDING_M)
    assert throat[1] - tack[1] == pytest.approx(9.25 * YD, abs=ROUNDING_M)
    assert tack[0] - clew[0] == pytest.approx(15.5 * CLOTH_FT * FT, abs=ROUNDING_M)
    assert clew[1] == pytest.approx(tack[1], abs=0.001)
    # the yard's fore part bare, about 0.53 of it (Ind §3.1)
    head = math.dist(throat, peak)
    assert (yard.length_m - head) / yard.length_m == pytest.approx(0.53, abs=0.01)
    # area and centre from the corners, the centre above the water (Ext §3.4)
    area, cx, cz = polygon([tack, throat, peak, clew])
    assert abs(area / steel_mean_m2(*COURSE_ROW) - 1.0) <= 0.10
    assert course.area_m2 == round(area)
    assert course.x_m == pytest.approx(cx, abs=0.06) and course.centre_height_m == pytest.approx(
        cz, abs=0.06
    )
    assert course.reef_bands == 1 and course.canvas_no == 2
    # the lines of Ext §3.4: no brace, no brails; one unsided sheet and one tack
    of_yard = {ln.id: ln.cls for ln in lines_of(ship, "mizzen.yard")}
    assert of_yard == {
        "mizzen.yard.jeers": "halyard",
        "mizzen.yard.derrick": "lift",
        "mizzen.yard.lift.starboard": "lift",
        "mizzen.yard.lift.larboard": "lift",
        "mizzen.yard.vang.starboard": "vang",
        "mizzen.yard.vang.larboard": "vang",
        "mizzen.yard.bowline.starboard": "guy",
        "mizzen.yard.bowline.larboard": "guy",
    }
    of_sail = {ln.id: (ln.cls, ln.side) for ln in lines_of(ship, "mizzen.course")}
    assert of_sail == {"mizzen.course.sheet": ("sheet", None), "mizzen.course.tack": ("tack", None)}
    # Indf §4.2's check on Steel's list for a 64 (vol. II, OCR l. 24857-24865), the sizes taken,
    # old beside new by the rule on her rope: the derrick 4 in in four parts (4 1/4; 111.9 to 99.2
    # kN), the vang pendants 4 in (3 3/4; 21.8 to 24.8 kN), the bowlines 3 in (3 3/4; 21.8 to 13.9)
    assert ship.lines["mizzen.yard.derrick"].rating_kn == pytest.approx(99.2, abs=0.05)
    assert ship.lines["mizzen.yard.vang.starboard"].rating_kn == pytest.approx(24.8, abs=0.05)
    assert ship.lines["mizzen.yard.bowline.starboard"].rating_kn == pytest.approx(13.9, abs=0.05)
    # its groups (Ext §3.4), never "courses": the gale would reduce it twice over
    for group in ("plain sail", "all sail", "fore-and-aft sails"):
        assert "mizzen.course" in ship.groups[group], group
    assert "mizzen.course" not in ship.groups["courses"]
    for group, members in ship.groups.items():
        if "yards" in group:
            assert "mizzen.yard" not in members, group
    # the storm mizzen and the driver each in its place
    assert ship.sails["storm_mizzen"].in_place_of == "mizzen.course"
    assert ship.sails["mizzen.driver"].in_place_of == "mizzen.course"


def test_the_clew_check_her_course_and_booms_clear_her_roundhouse_decks(sixty_four, razee):
    """Bel §1.5, §4.5-§4.6, §17.2 item 13; the lead's notes of 2026-10-29, item 2, and the two
    rulings of 2026-10-30: where a course's clew ends under a roundhouse or poop deck at the side.
    The figures, old beside new.

    **The 64's course, Steel's words read and not a head room.** "Within 6 or 7 feet of the deck"
    (OCR l. 11441-11442), 6 ft 6 in, from the deck the mast stands through there, her roundhouse
    deck. Her tack above her water: stage A's 7.45 m, 6 ft 6 in above her quarterdeck, its foot 0.14
    m under the roundhouse deck at the side; the first of stage B's 9.43 m, raised until the foot
    stood 6 ft over it, the 74's boom's figure, 13.0 ft above her quarterdeck; now 8.73 m, the clew
    1.13 m clear at the side, 1.14 by the file's rounded deck, more than the 74's margin. Her throat
    and truss 15.91, 17.89, now 17.19 m above her water, 2.2 m under the crossjack yard; her centre
    13.6, 15.6, now 14.9 m; the area unchanged.

    **The 64's driver boom** (Ext §17.2, at stage A's course 2.4 m above her quarterdeck, about
    level with the roundhouse deck at the stern, 7.86 m): the least jaws that give 6 ft over that
    deck, 9.69 m, now hold (10.12 m on the course at 9.43 m, where its after leech would have
    been 19.90 m at 9.69, over Steel's 19.43), 1.16 m over her taffrail. No check broken (below).

    **The razee's spanker boom, at literally the least that clears her taffrail.** At stage A's 6
    ft 6 in above her quarterdeck its jaws, 5.82 m, ran through her cabin 0.20 m under her short
    roundhouse's deck and 1.33 m under her taffrail (D18 (c)'s question, Indf §17 item 1). Raised
    by 6 ft of head room over that deck they stood at 7.85 m, 0.70 m over her taffrail, and the
    spanker by the frigate's rule fell from the owner's 218 m2 to 191. Now 7.16 m, up 1.34 m, a
    centimetre over her taffrail as filed and 1.15 m over that deck: a boom her people stoop under.
    The spanker 200 m2, 1% under Steel's driver for a 38 (202 m2), within the owner's 8%; her centre
    13.0, 14.1, now 13.7 m; her ringtail 65, 58, now 60 m2. At 5 ft of head room it would be 195 m2;
    the rule cannot keep 218 with the boom clear of her taffrail."""
    # the 64's course: Steel's 6 ft 6 in from the roundhouse deck at the mast, the foot clear over
    # the whole of its run
    tack, _throat, _peak, clew = corners_above_water(sixty_four, "mizzen.course")
    at_the_mast = sixty_four.spars["mizzen.mast"].x_m
    assert tack[1] == pytest.approx(8.73, abs=0.005)
    assert tack[1] - roundhouse_z(sixty_four, at_the_mast) == pytest.approx(
        6.5 * FT, abs=ROUNDING_M
    )
    for i in range(11):
        x = tack[0] + (clew[0] - tack[0]) * i / 10.0
        assert tack[1] - roundhouse_z(sixty_four, x) >= 1.0, x
    assert tack[1] - roundhouse_z(sixty_four, clew[0]) == pytest.approx(1.14, abs=ROUNDING_M)
    assert tack[1] < above_water(sixty_four, "mizzen.crossjack.yard") - 1.0
    # the 64's driver boom: the least that gives 6 ft over her roundhouse, its end over the taffrail
    taff_x, taff_z = sixty_four.hull.spec.profile.rail_m[0]
    jaws = above_water(sixty_four, "mizzen.boom")
    boom = sixty_four.spars["mizzen.boom"]
    decks = roundhouse_of(sixty_four)
    assert jaws == pytest.approx(9.69, abs=0.005)
    assert min(jaws - z for _x, z in decks) == pytest.approx(HEAD_ROOM_M, abs=ROUNDING_M)
    assert tack[0] - boom.length_m < taff_x and jaws > taff_z
    # the razee's spanker boom: the least that clears her taffrail as filed, and her roundhouse
    jaws = above_water(razee, "mizzen.boom")
    decks = roundhouse_of(razee)
    taff_x, taff_z = razee.hull.spec.profile.rail_m[0]
    assert jaws - taff_z == pytest.approx(0.01, abs=1e-6)
    assert 0.5 < min(jaws - z for _x, z in decks) < HEAD_ROOM_M
    sp_tack, _t, _p, sp_clew = corners_above_water(razee, "mizzen.spanker")
    assert sp_tack[1] == pytest.approx(jaws, abs=ROUNDING_M)
    assert sp_clew[1] == pytest.approx(jaws, abs=ROUNDING_M) and sp_clew[0] < taff_x
    assert razee.sails["mizzen.spanker"].area_m2 == 200
    assert abs(razee.sails["mizzen.spanker"].area_m2 / 202.0 - 1.0) <= 0.08
    assert razee.sails["ringtail"].area_m2 == 60
    assert razee.spars["ringtail_boom"].height_m == razee.spars["mizzen.boom"].height_m
    # her storm mizzen, cut from the quarterdeck, ran its foot through the same deck (the 64's up
    # to 0.91 m under it, the razee's 0.95 m), and now stands at her rail over the foot's run
    # (48 m2 to 43 and 44; centre above water 10.2 to 11.2 m and 8.6 to 9.4 m; old beside new)
    for ship, area in ((sixty_four, 43), (razee, 44)):
        assert ship.sails["storm_mizzen"].area_m2 == area
        st_tack, _peak, st_clew = corners_above_water(ship, "storm_mizzen")
        assert st_clew[1] == pytest.approx(st_tack[1], abs=ROUNDING_M)
        for i in range(11):
            x = st_tack[0] + (st_clew[0] - st_tack[0]) * i / 10.0
            assert st_tack[1] - roundhouse_z(ship, x) > 0.1, x


def test_the_64s_driver_is_steels_in_the_courses_place_and_in_the_sail_room(sixty_four):
    """Ext §17.2 on her file, the generator's assertions read back: class `lateen` cut at the mast,
    on the mizen yard, the mast and its boom; `in_place_of` the course and unbent, in the sail room;
    no reef band; canvas No. 5. Throat the course's; tack on the mast's raked line at the jaws;
    foot along the boom, the clew within it; peak on the yard's line, abaft and above its peak by
    no more than two-thirds of the driver yard. Measured on her roundhouse, against Ext §17.2's
    first cut in brackets and the course at 9.43 m after it: fore leech 7.50 m (6.98, 7.77; Steel's
    8.69), after leech 19.16 m (18.71, 19.42; Steel's band 17.60-19.43), four corners 203 m2 (197,
    207; Steel's rule 198.5, +2%), centre 8.8 m abaft the mast and 16.5 m above the water (8.55,
    14.51, 17.1: her course raised), the peak 6.10 m beyond the yard's (6.09). So the course gives
    way to it for about twice the sail aft. Each figure also holds the 10% and Steel's band, so no
    report past the head room. The boom files `rigged_out: false`, out only while the driver is
    bent (Ext §17.11), and the razee's spanker boom, a gaff sail's, files no such key."""
    ship = sixty_four
    driver, course = ship.sails["mizzen.driver"], ship.sails["mizzen.course"]
    boom = ship.spars["mizzen.boom"]
    assert driver.cls == "lateen" and driver.cut_at_mast and driver.curve_class == "gaff"
    assert driver.state is SailState.UNBENT and course.state is not SailState.UNBENT
    assert driver.in_place_of == "mizzen.course"
    assert ship.spar_of_role(driver, "yard") is ship.spars["mizzen.yard"]
    assert ship.spar_of_role(driver, "mast") is ship.spars["mizzen.mast"]
    assert ship.spar_of_role(driver, "boom") is boom
    assert ship.sail_of("mizzen.yard") is course  # the course filed first (Ext §17.2)
    assert driver.reef_bands == 0 and driver.canvas_no == 5
    assert boom.cls == "boom" and ship.mast_of(boom).id == "mizzen.mast"
    assert boom.length_m == pytest.approx((65.0 + 4.0 / 12.0) * FT, abs=0.06)
    assert boom.rigged_out is False and scripts.driver_boom(ship, driver) is boom
    assert next(s for s in doc_of(SIXTY_FOUR)["spars"] if s["id"] == boom.id)["rigged_out"] is False
    assert "rigged_out" not in next(s for s in doc_of(RAZEE)["spars"] if s["id"] == boom.id)
    d_tack, d_throat, d_peak, d_clew = corners_above_water(ship, "mizzen.driver")
    c_tack, c_throat, c_peak, _c = corners_above_water(ship, "mizzen.course")
    jaws = above_water(ship, "mizzen.boom")
    assert math.dist(d_throat, c_throat) <= LEAN_OK_M
    assert d_tack[1] == pytest.approx(jaws, abs=ROUNDING_M)
    assert d_tack[0] == pytest.approx(mast_x_at(ship, "mizzen.mast", jaws), abs=LEAN_OK_M)
    assert d_clew[1] == pytest.approx(jaws, abs=ROUNDING_M)
    foot = d_tack[0] - d_clew[0]
    assert foot == pytest.approx(29.0 * CLOTH_FT * FT, abs=ROUNDING_M) and foot < boom.length_m
    # the peak on the mizen yard's line, past its peak by no more than 2/3 of the driver yard
    rise, run = c_peak[1] - c_throat[1], c_throat[0] - c_peak[0]
    off = abs((d_peak[0] - c_throat[0]) * rise + (d_peak[1] - c_throat[1]) * run) / math.hypot(
        rise, run
    )
    assert off <= LEAN_OK_M
    assert d_peak[0] < c_peak[0] and d_peak[1] > c_peak[1]
    assert math.dist(d_peak, c_peak) <= 2.0 / 3.0 * DRIVER_YARD_M
    # the area within a tenth of Steel's rule, the after leech within two to four yards deeper
    # than the course's, the centre the corners'
    area, cx, cz = polygon([d_tack, d_throat, d_peak, d_clew])
    assert abs(area / steel_mean_m2(*DRIVER_ROW) - 1.0) <= 0.10
    assert driver.area_m2 == round(area, 0) or abs(driver.area_m2 - area) <= 1.0
    assert (17.25 + 2.0) * YD <= math.dist(d_peak, d_clew) <= (17.25 + 4.0) * YD + 0.01
    assert driver.x_m == pytest.approx(cx, abs=0.06)
    assert driver.centre_height_m == pytest.approx(cz, abs=0.06)
    assert driver.area_m2 > 1.9 * course.area_m2
    # "occasional sails" alone: never plain sail, the courses or all sail (Ext §17.2)
    assert "mizzen.driver" in ship.groups["occasional sails"]
    assert "mizzen.driver" not in ship.groups["storm canvas"]
    for group, members in ship.groups.items():
        if group != "occasional sails":
            assert "mizzen.driver" not in members, group
    # its lines: one each, the sheet unsided and of two parts, rated by Steel's own sizes
    lines = {ln.cls: ln for ln in lines_of(ship, "mizzen.driver")}
    assert set(lines) == {"halyard", "tack", "sheet", "downhaul"}
    assert lines["sheet"].side is None and lines["sheet"].parts == 2
    # the spare in the sail room, of its canvas, with the occasional sails
    room = {s.kind: s.canvas_no for s in parts.sail_room(ship).sails}
    assert room["mizzen.driver"] == 5
    # its boom's horse as the frigate's (HORSE_NOTE), half the beam
    spec = next(s for s in doc_of(SIXTY_FOUR)["spars"] if s["id"] == "mizzen.boom")
    assert spec["horse_m"] == pytest.approx(0.5 * ship.hull.spec.beam_m, abs=0.05)


def test_the_yards_under_her_bowsprit_hang_where_her_spars_put_them(sixty_four, razee):
    """Ext §4.1 and §9.3 on her files: the spritsail yard slung under the bowsprit near the cap,
    no halyard; on the 64 the sprit-topsail yard under the jib-boom near its end, higher, its
    halyard for the traveller's outhauler; on the razee no sprit-topsail yard (the owner: Indf
    §17 item 5). Steel's lengths (p. 49) and sails (table IV: 102 and 103 m2), each foot above
    the water at no heel, their own group and all sail, nothing the engine reads by name.

    **Her bowsprit's and jib-boom's ratings** (`Builder.rate_spars`; the lead's ruling of
    2026-10-30: a spar's rating by the sails through it is a proxy for its scantlings, and the proxy
    may not shrink when a smaller sail is hung on the spar). Old beside new, kN: the 64's bowsprit
    171.0 on its old heel, 100.6 by the sprit sails, now 168.6, the same named rating on the
    headsails' centres as the stem head lowered them; its jib-boom 27.3, 16.1, now 27.0; the razee's
    bowsprit 169.7, 47.2, now 168.5; her jib-boom 27.2, 26.9, no sail's chain through it and
    unmoved. The lugger's flying jib rates her running bowsprit, 21.8 against the 37.4 named: a jib
    and no yard under the spar, left as filed, so that the eight files' bytes hold.

    **Risk 9 (Ext §6.2 as built), closed by the viewer's slant remedy.** The sprit topsail's
    depth lies along the slant between the two yards, and the yards stand so that it is Steel's 9
    yards: 8.22 m of slant as filed, 3.97 m by heights, the sail's plane sloping well forward. The
    drawing's old trapezoid by heights gave 52 m2 against the file's 103 (-49%), and could not hold
    the view test's 5% on her spars: that needed 7.44 m by heights, and the most her line gives, the
    spritsail's foot just clear of the water and the yard at the jib-boom's end, is 7.19 m, at a
    slant of 15 m, near twice Steel's depth. So the yards stayed where the period hangs them, and
    `squareCut` (B5) now takes the gap along the slant: head 9.30 m and foot 15.75 m, the file's
    area."""
    deck = sixty_four.hull.spec.deck_height_m
    bs, jb = sixty_four.spars["bowsprit"], sixty_four.spars["jib_boom"]
    c = math.cos(math.radians(27.0))
    s = math.sin(math.radians(27.0))
    root_z = sixty_four.hull.spec.profile.stem_m[-1][1]
    end_x = bs.x_m + bs.length_m * c

    def bowsprit_z(x):
        return root_z + (x - bs.x_m) * s / c

    yard = sixty_four.spars["spritsail.yard"]
    assert yard.cls == "yard" and yard.parent == "bowsprit"
    assert yard.length_m == pytest.approx(57.5 * FT, abs=0.06)
    assert bs.x_m + 0.7 * bs.length_m * c <= yard.x_m <= end_x  # near the cap
    assert 0.5 <= bowsprit_z(yard.x_m) - (yard.height_m + deck) <= 1.0  # below its line
    assert sixty_four.halyard_of(yard) is None  # it hangs in slings (Ext §4.1)
    top = sixty_four.spars["sprit_topsail.yard"]
    assert top.cls == "yard" and top.parent == "jib_boom"
    assert top.length_m == pytest.approx(34.5 * FT, abs=0.06)
    assert top.height_m > yard.height_m
    assert end_x + 0.5 * jb.length_m * c <= top.x_m <= end_x + jb.length_m * c  # near its end
    jib_z = root_z + (top.x_m - bs.x_m) * s / c
    assert 0.3 <= jib_z - (top.height_m + deck) <= 0.7  # below its line
    assert sixty_four.halyard_of(top) is not None
    slant = math.hypot(top.x_m - yard.x_m, top.height_m - yard.height_m)
    assert slant == pytest.approx(9.0 * YD, abs=0.05)  # Steel's depth
    assert top.height_m - yard.height_m == pytest.approx(3.97, abs=0.05)
    ss, st = sixty_four.sails["spritsail"], sixty_four.sails["sprit_topsail"]
    assert ss.area_m2 == 102 and st.area_m2 == 103
    assert ss.reef_bands == 2 and st.reef_bands == 0
    assert ss.canvas_no == 2 and st.canvas_no == 6
    assert yard.height_m + deck - 7.5 * YD > 2.0  # the spritsail's foot, Steel's depth under it
    assert ss.x_m == pytest.approx(yard.x_m, abs=0.06)
    assert ss.centre_height_m == pytest.approx(yard.height_m + deck - 3.75 * YD, abs=0.06)
    assert yard.x_m < st.x_m < top.x_m
    assert yard.height_m + deck < st.centre_height_m < top.height_m + deck
    for ship, sails in ((sixty_four, ["spritsail", "sprit_topsail"]), (razee, ["spritsail"])):
        assert ship.groups["spritsails"] == sails
        for sid in sails:
            assert sid in ship.groups["all sail"]
            assert ship.under_bowsprit(sid)
            assert ship.under_bowsprit(ship.spar_of_role(sid, "yard"))
            for group in ("plain sail", "courses", "topsails", "headsails", "jibs", "square sails"):
                assert sid not in ship.groups[group], group
        for group in ("yards", "head yards", "lower yards", "topsail yards"):  # Ext §4.2 as built
            assert not {"spritsail.yard", "sprit_topsail.yard"} & set(ship.groups[group]), group
        for jib in ship.groups["jibs"]:
            assert not ship.under_bowsprit(jib)
        # their lines (`square_sail_lines` and the guys, Lavery I28)
        by_class = Counter(ln.cls for ln in lines_of(ship, "spritsail.yard"))
        assert by_class == {"brace": 2, "lift": 2, "guy": 2}
        by_class = Counter(ln.cls for ln in lines_of(ship, "spritsail"))
        assert by_class == {"sheet": 2, "clewline": 2, "buntline": 1, "reef_tackle": 2}
    assert "sprit_topsail.yard" not in razee.spars and "sprit_topsail" not in razee.sails
    # the ratings the rating pass keeps (above), and what it says of them
    for ship, rating in ((sixty_four, 168.6), (razee, 168.5)):
        assert ship.spars["bowsprit"].rating_kn == pytest.approx(rating, abs=0.05)
    assert sixty_four.spars["jib_boom"].rating_kn == pytest.approx(27.0, abs=0.05)
    assert razee.spars["jib_boom"].rating_kn == pytest.approx(26.9, abs=0.05)
    assert "kept over spritsail, sprit_topsail, the smaller load" in text_of(SIXTY_FOUR)
    assert "kept over sprit_topsail, the smaller load" in text_of(SIXTY_FOUR)
    assert "kept over spritsail, the smaller load" in text_of(RAZEE)
    assert load_ship("data/ships/lugger.yaml").spars["bowsprit"].rating_kn == pytest.approx(21.8)
    # the razee's the 64's spar at her own water
    r_deck = razee.hull.spec.deck_height_m
    r_yard = razee.spars["spritsail.yard"]
    assert r_yard.x_m == pytest.approx(yard.x_m, abs=0.01)
    assert r_yard.height_m + r_deck - (yard.height_m + deck) == pytest.approx(RISE_M, abs=0.03)
    assert razee.sails["spritsail"].area_m2 == 102
    assert razee.sails["spritsail"].state is not SailState.UNBENT


def under_plain_sail_ship(path):
    ship = load_ship(path)
    for sid in ship.groups["plain sail"]:
        ship.sails[sid].state = SailState.SET
    return ship


@pytest.mark.parametrize(
    "path, after", [(SIXTY_FOUR, "mizzen.course"), (RAZEE, "mizzen.spanker")], ids=["64", "razee"]
)
def test_her_classing_is_the_frigates_row_counting_the_head_on_the_masts(path, after):
    """The golden table's frigate row (tests/test_rig_classing.py; Ext §10.1), read through the
    engine's own gates on each file, plain sail set, the head field counted on the masts (Ext §4.2
    as built): three masts with yards, four head yards and eight after, the main backed,
    square-rigged, the stagger +2.0 degrees; her driver and her boom sail her after sail, the
    64's course cut at the mast with the driver in the sail room. The yards under the bowsprit are
    in the head list beside those four, each with its own target, never in the after yards; the
    mizen yard in none."""
    ship = under_plain_sail_ship(path)
    masts = [m.id for m in scripts._masts_with_yards(ship)]
    assert masts == ["fore.mast", "main.mast", "mizzen.mast"]
    head, aft = scripts.head_and_after_yards(ship)
    on_masts = [y for y in head if not ship.under_bowsprit(y)]
    assert len(on_masts) == 4 and {ship.mast_of(y).id for y in on_masts} == {"fore.mast"}
    under = {y.id for y in head if ship.under_bowsprit(y)}
    want = {"spritsail.yard", "sprit_topsail.yard"} if path == SIXTY_FOUR else {"spritsail.yard"}
    assert under == want
    assert len(aft) == 8 and not {y.id for y in aft} & under
    assert "mizzen.yard" not in {y.id for y in [*head, *aft]}
    assert ship.mast_of(scripts.yards_to_back(ship)[0]).id == "main.mast"
    assert _square_rigged(ship) is True
    targets = {y.id: y.brace_limit for y in scripts.working_yards(ship)}
    _pairs, diff = yard_trim.stagger(ship, targets)
    assert diff == pytest.approx(2.0, abs=0.05)
    assert [s.id for s in scripts.after_gaff_sails(ship)] == [after]
    assert [s.id for s in scripts.boom_sails(ship)] == [after]
    assert scripts.dipping_lugs(ship) == []


# -- Ext §3, §4 and §17.7 on her file --------------------------------------------------------


LIGHT_AIRS = Wind(WindParams.from_nautical(0.0, 3.0, 0.0, 0.0), random.Random(0))
# shift_sail.yaml's, the boom's two the shift script's own (Ext §17.11: 120 s, judgement)
SHIFT_S = {"take_in": 90, "unbend": 180, "send_up": 150, "bend": 240, "set": 120}
RIG_BOOM_S = 120


def _bare(ship):
    """A bare ship's runner, thirty degrees of apparent wind on the deck, enough to trim to."""
    runner = Runner(ship)
    ship.dyn.apparent_wind_angle = math.radians(-30.0)
    ship.dyn.apparent_wind_speed = 6.0
    return runner


def _run(runner, ship, max_ticks=3000):
    """Tick the runner (no physics) until nothing is in hand: the ticks and the notes."""
    ticks, notes = 0, []
    while runner.in_progress() and ticks < max_ticks:
        runner.step(ship, 1.0, LIGHT_AIRS)
        notes.extend(ship.drain_notes())
        ticks += 1
    assert not runner.in_progress(), f"still at work after {max_ticks} ticks"
    return ticks, notes


def _refusal(ship, text):
    with pytest.raises(OrderError) as e:
        orders.handle(ship, text)
    return str(e.value)


def _in_the_room(ship):
    room = parts.sail_room(ship)
    kinds = ("mizzen.course", "mizzen.driver")
    return [(s.kind, s.canvas_no) for s in room.sails if s.kind in kinds]


def her_doc_with_the_driver_bent():
    """Her file with the driver bent in the course's place, its boom rigged out (Ext §17.11), and
    the course in the sail room."""
    doc = doc_of(SIXTY_FOUR)
    sails = {s["id"]: s for s in doc["sails"]}
    sails["mizzen.course"]["bent"] = False
    del sails["mizzen.driver"]["bent"]
    next(s for s in doc["spars"] if s["id"] == "mizzen.boom")["rigged_out"] = True
    return doc


def _world(tmp_path, bent=False, *also, heading=292.5, knots=15.0):
    """Her file whole in a northerly on the starboard tack, six points off (truth 10's middle
    heading: from 60 degrees off she misses stays, as TuningNotes has it, staying from 61, and from
    60 with the yards under her bowsprit out), under plain sail, settled with the
    yards trimmed (`tests/test_lateen.py`'s way); `bent`, with the driver bent in the course's
    place and set by name; `also`, sails set by name beside it."""
    scenario = Scenario(
        wind_from_deg=0.0,
        wind_speed_kn=knots,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=heading,
        ship_speed_kn=4.0,
    )
    path = SIXTY_FOUR
    if bent:
        path = tmp_path / "sixty-four-driver.yaml"
        path.write_text(yaml.safe_dump(her_doc_with_the_driver_bent()), encoding="utf-8")
        path = str(path)
    world = make_world(7, path, scenario)
    for text in ("set plain sail", "brace sharp up on the starboard tack"):
        world.submit(text)
    if bent:
        world.submit("set the driver")
    for sid in also:
        world.submit(f"set the {sid}")
    for i in range(1200):
        if i >= 400 and i % 120 == 40:
            world.submit("trim sails")
        world.tick()
    return world


def _after(world, start):
    return [e for e in world.log if e.tick > start]


def _until(world, words, ticks):
    """Tick until a line with `words` is logged: its tick."""
    start = world.clock.tick
    for _ in range(ticks):
        world.tick()
        hit = [e for e in _after(world, start) if words in e.text]
        if hit:
            return hit[0].tick
    raise AssertionError(f"no '{words}' in {ticks} ticks: {[e.text for e in _after(world, start)]}")


@pytest.mark.parametrize("drawing", [True, False], ids=["drawing", "furled"])
def test_the_64_shifts_her_mizen_for_the_driver_and_back_each_to_its_end(drawing):
    """Ext §17.3, §17.7 and §17.11 on `sixty-four.yaml`: "shift the mizen for the driver" and back.
    A drawing course is taken in, unbent, sent down while the driver is swayed up, the boom rigged
    out, the driver bent and set: 900 s at the file's times with no company aboard (780 s before
    the boom went out with it, Ext §17.11); a furled one shifted where it hangs in 690 s (570 s),
    the driver left furled. Back, the boom comes in after the unbend. The boom stands out only while
    the driver is bent. The sail room holds the course's canvas, No. 2, in the driver's spare's
    stead, so the count of spares stands; shifted back, the same."""
    ship = load_ship(SIXTY_FOUR)
    runner = _bare(ship)
    course, driver = ship.sails["mizzen.course"], ship.sails["mizzen.driver"]
    boom = ship.spars["mizzen.boom"]
    spares = scripts.spare_sails(ship)
    assert driver.state is SailState.UNBENT and course.state is SailState.FURLED
    assert boom.rigged_out is False
    assert _in_the_room(ship) == [("mizzen.course", 2), ("mizzen.driver", 5)]
    if drawing:
        course.state = SailState.SET
    phases = list(SHIFT_S) if drawing else ["unbend", "send_up", "bend"]
    for text, old, new, old_no, out in (
        ("shift the mizen for the driver", course, driver, 2, True),
        ("shift the driver for the mizen", driver, course, 5, False),
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
        assert (old.id, old_no) in _in_the_room(ship)
        assert scripts.spare_sails(ship) == spares
        assert ship.sails["storm_mizzen"].state is SailState.UNBENT


def test_the_64s_refusals_the_one_place_and_the_reef():
    """Ext §17.3, §17.4 and §17.7 on `sixty-four.yaml`: "bend the driver" with the course bent is
    refused, naming the shift; with the driver bent "bend the storm mizzen" is refused naming it,
    and "shift the driver for the storm mizzen" runs, the two sails rivals for the course's place
    (`_in_each_others_place`); "reef the driver" is refused, Steel naming no band in it; and the
    brace orders refuse the mizen yard in the vangs' words (Ext §3.3)."""
    ship = load_ship(SIXTY_FOUR)
    runner = _bare(ship)
    words = _refusal(ship, "bend the driver")
    assert "is bent in the driver's place" in words and "shift the" in words
    assert _refusal(ship, "brace the mizen yard sharp up") == (
        "The mizzen yard is a lateen yard, not a yard; the lateen sail on it is not braced; it "
        "is trimmed with its sheet and vangs."
    )
    orders.handle(ship, "shift the mizen for the driver")
    _run(runner, ship)
    driver, storm = ship.sails["mizzen.driver"], ship.sails["storm_mizzen"]
    assert scripts._in_each_others_place(driver, storm)
    assert driver.state is not SailState.UNBENT
    words = _refusal(ship, "bend the storm mizzen")
    assert words == (
        "The storm mizzen: The driver is bent in the storm mizzen's place; unbend it first, or "
        "shift the driver for the storm mizzen."
    )
    with pytest.raises(OrderError):
        orders.handle(ship, "reef the driver")
    orders.handle(ship, "shift the driver for the storm mizzen")
    _run(runner, ship)
    assert (driver.state, storm.state) == (SailState.UNBENT, SailState.FURLED)


def test_the_gale_takes_in_her_driver_or_her_course_at_the_third_reef():
    """Ext §3.5 and §17.7 on `sixty-four.yaml`, `shorten sail`'s after sail (`orders.storm`, Luce
    1884 p. 476): with the topsails going to their third reef the driver is taken in, the course
    when it is the one bent; the sail in the sail room no line touches. And the sprit sails first
    of all when set (Ext §4.2 place 8)."""
    for bent, name in ((False, "mizzen course"), (True, "mizzen driver")):
        doc = her_doc_with_the_driver_bent() if bent else doc_of(SIXTY_FOUR)
        ship = ship_from_dict(doc, "sixty-four.yaml")
        for sid in ship.groups["plain sail"]:
            if ship.sails[sid].state is not SailState.UNBENT:
                ship.sails[sid].state = SailState.SET
        if bent:
            ship.sails["mizzen.driver"].state = SailState.SET
        for sid in ("spritsail", "sprit_topsail"):
            ship.sails[sid].state = SailState.SET
        topsails = [s for s in ship.sails.values() if s.id.endswith(".topsail") and s.is_set]
        for sl in topsails:
            sl.reefs = 2
        lines = shorten_sail_lines(ship, 40.0)
        assert f"take in the {name}" in lines, lines
        other = "mizzen driver" if not bent else "mizzen course"
        assert f"take in the {other}" not in lines, lines
        assert bowsprit_sail_lines(ship) == ["take in the sprit topsail", "take in the spritsail"]


@pytest.mark.parametrize("bent", [True, False], ids=["driver", "course"])
def test_truth_7_230_the_64s_clauses_her_after_sail_at_helms_a_lee_and_hove_to(tmp_path, bent):
    """Truth 7-230's clause left for B1 (Ext §17.7), on `sixty-four.yaml`: the driver, bent and
    set, is her after sail on the paths by `drives_aft`: hauled flat aft at helm's a-lee, its words
    naming it and the bowline, and brailed up hove to; the course likewise, the driver then
    untouched in the sail room. Seed 7, fifteen knots, six points off."""
    world = _world(tmp_path, bent)
    after = world.ship.sails["mizzen.driver" if bent else "mizzen.course"]
    assert after.is_set
    name = "driver" if bent else "mizzen course"
    start = world.clock.tick
    world.submit("tack ship")
    _until(world, "Helm's a-lee", 500)
    line = next(e.text for e in _after(world, start) if "Helm's a-lee" in e.text)
    assert f"haul aft the {name} sheet and brace the bowline to leeward" in line, line
    assert after.is_set and math.degrees(abs(after.sheet_angle)) == pytest.approx(18.0, abs=0.01)
    assert world.ship.spars["mizzen.yard"].brace_angle == 0.0
    if not bent:
        assert world.ship.sails["mizzen.driver"].state is SailState.UNBENT
    _until(world, "Tacked", 900)
    start = world.clock.tick
    world.submit("heave to")
    for _ in range(600):
        world.tick()
    texts = [e.text for e in _after(world, start)]
    assert any(e.kind == "ship.hove_to" for e in _after(world, start)), texts
    assert any(f"brailed up the {name}" in t for t in texts), texts
    assert after.state is SailState.IN_THE_GEAR
    if not bent:
        assert world.ship.sails["mizzen.driver"].state is SailState.UNBENT


def test_the_64s_driver_is_brailed_at_up_helm_and_set_after_the_cast(tmp_path):
    """Ext §3.5 and §17.7 on `sixty-four.yaml`, the driver bent: wearing, brailed at "up helm" and
    hauled out by the wind on the new tack (Steel 1794 vol. II pp. 321-322); and it is the sail
    set after the cast getting under way from Falmouth's outer road (the fixture's road, in
    `tests/test_driver.py`; `after_gaff_sails_all`, its `set_lateen`)."""
    world = _world(tmp_path, bent=True)
    after = world.ship.sails["mizzen.driver"]
    start = world.clock.tick
    world.submit("wear ship")
    _until(world, "Up helm", 300)
    assert after.state is SailState.IN_THE_GEAR
    up = next(e.text for e in _after(world, start) if "Up helm" in e.text)
    assert "brail up the driver" in up, up
    _until(world, "Haul out the driver!", 1500)
    assert after.is_set and world.ship.dyn.tack == "larboard"

    scenario = Scenario(
        start_time=datetime(1785, 6, 10, 10, 0),
        wind_from_deg=225.0,
        wind_speed_kn=10.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=225.0,
        ship_speed_kn=0.0,
        position={"lat_deg": 50.133, "lon_deg": -5.035},
        region="channel-west",
    )
    path = tmp_path / "sixty-four-driver.yaml"
    world = make_world(7, str(path), scenario)
    world.run(60)
    assert world.submit("let go the best bower").kind == "order.accepted"
    world.run(900)
    after = world.ship.sails["mizzen.driver"]
    assert after.state is SailState.FURLED
    assert world.submit("get under way").kind == "order.accepted"
    cast = _until(world, "right the helm", 3600)
    line = next(e.text for e in world.log if e.tick == cast and "right the helm" in e.text)
    assert line.endswith("right the helm, brace round the head yards, set the driver."), line
    assert after.is_set and world.ship.sails["mizzen.course"].state is SailState.UNBENT


def test_truth_7_230_the_64s_clauses_her_shift_and_her_polar_with_the_driver():
    """Truth 7-230's clauses left for B1 (Ext §17.7; Steel 1794 vol. I, OCR l. 13819-13821 and
    24536-24538; *Venus*'s shift), on `sixty-four.yaml`.

    1. **The shift at her company**, under plain sail in ten knots 120 degrees off, seed 7: the
       course, drawing, taken in, unbent, sent down while the driver is swayed up, the boom rigged
       out (Ext §17.11), the driver bent and set, in that order; each phase between its file's time
       and a quarter more (measured 102, 205, 171, 137, 273 and 137 s against 90, 180, 150, 120, 240
       and 120; the boom's rigged out by the state of the spar), the whole between fifteen and
       nineteen minutes (1,025 s; old beside new, five phases of 888 s and the band thirteen to
       sixteen). Trimmed, it draws ahead (5.07 kn against 4.93 under the course). Shifted back the
       boom comes in after the unbend, 102, 205, 137, 171, 273 and 137 s, 1,025 s.
    2. **Her polar with the driver**, bent and set in the course's place, above the course's from
       90 to 150 degrees in ten knots, Steel's "light fair winds" (by `_balanced_speed_ms`, kn, the
       course then the driver: 90 deg 5.32, 5.46; 120 deg 5.04, 5.18; 150 deg 4.26, 4.32; and in
       six knots 3.23, 3.32; 3.05, 3.14; 2.56, 2.60). It holds, and is pinned.

    **Measured and not pinned: her tack with the driver bent** (Ext §17.7 as built; Steel's "light
    fair winds", Ext §17.1). "Tacked" from six points off in 15 kn 479 s against 251 s with the
    course, in 10 kn 494 against 279; from 75 deg in 8 kn 506 against 344; she comes through the
    wind in the same time, and the driver's 38-77 kN m of weather helm from 60 to 120 deg in 10 kn
    keeps her from falling off on the new tack. It is the sail of a fair wind, as Steel has it, and
    the sail to shift before working to windward: docs/dev/TuningNotes.md, the table."""
    scenario = Scenario(
        wind_from_deg=0.0,
        wind_speed_kn=10.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=240.0,
        ship_speed_kn=4.0,
    )
    world = make_world(7, SIXTY_FOUR, scenario)
    world.submit("set plain sail")
    for i in range(1200):
        if i >= 400 and i % 120 == 40:
            world.submit("trim sails")
        world.tick()
    ship = world.ship
    course, driver = ship.sails["mizzen.course"], ship.sails["mizzen.driver"]
    boom = ship.spars["mizzen.boom"]
    assert course.is_set and driver.state is SailState.UNBENT and boom.rigged_out is False
    start = world.clock.tick
    assert world.submit("shift the mizen for the driver").kind == "order.accepted"
    ends = {}
    for _ in range(1500):
        world.tick()
        now = world.clock.tick
        room = [kind for kind, _no in _in_the_room(ship)]
        seen = (
            ("take_in", course.state is SailState.IN_THE_GEAR),
            ("unbend", course.state is SailState.UNBENT),
            ("send_up", "mizzen.driver" not in room),
            ("rig_out_boom", boom.rigged_out),
            ("bend", driver.state is not SailState.UNBENT),
            ("set", driver.is_set),
        )
        for phase, done in seen:
            if done and phase not in ends:
                ends[phase] = now
        if driver.is_set:
            break
    began = next(
        e.tick for e in _after(world, start) if e.kind == "evolution.started" and "shift" in e.text
    )
    times = dict(SHIFT_S, rig_out_boom=RIG_BOOM_S)
    in_order = ["take_in", "unbend", "send_up", "rig_out_boom", "bend", "set"]
    assert list(ends) == in_order, ends
    marks = [began, *(ends[phase] for phase in in_order)]
    took = {phase: marks[i + 1] - marks[i] for i, phase in enumerate(in_order)}
    for phase in in_order:
        assert times[phase] <= took[phase] <= 1.25 * times[phase], took
    assert 15 * 60 <= ends["set"] - began <= 19 * 60
    assert course.state is SailState.UNBENT
    assert boom.rigged_out is True

    # and back, the boom's other phase, her way on as she draws under the driver
    start = world.clock.tick
    assert world.submit("shift the driver for the mizen").kind == "order.accepted"
    ends = {}
    for _ in range(1500):
        world.tick()
        now = world.clock.tick
        room = [kind for kind, _no in _in_the_room(ship)]
        seen = (
            ("take_in", driver.state is SailState.IN_THE_GEAR),
            ("unbend", driver.state is SailState.UNBENT),
            ("rig_in_boom", not boom.rigged_out),
            ("send_up", "mizzen.driver" in room),
            ("bend", course.state is not SailState.UNBENT),
            ("set", course.is_set),
        )
        for phase, done in seen:
            if done and phase not in ends:
                ends[phase] = now
        if course.is_set:
            break
    began = next(
        e.tick for e in _after(world, start) if e.kind == "evolution.started" and "shift" in e.text
    )
    times = dict(SHIFT_S, rig_in_boom=RIG_BOOM_S)
    in_order = ["take_in", "unbend", "rig_in_boom", "send_up", "bend", "set"]
    assert list(ends) == in_order, ends
    marks = [began, *(ends[phase] for phase in in_order)]
    took = {phase: marks[i + 1] - marks[i] for i, phase in enumerate(in_order)}
    for phase in in_order:
        assert times[phase] <= took[phase] <= 1.25 * times[phase], took
    assert 15 * 60 <= ends["set"] - began <= 19 * 60
    assert driver.state is SailState.UNBENT and boom.rigged_out is False

    def rigged(doc, driver_set):
        ship = ship_from_dict(doc, "sixty-four.yaml")
        for sid in ship.groups["plain sail"]:
            if sid != "mizzen.course" or not driver_set:
                ship.sails[sid].state = SailState.SET
        if driver_set:
            ship.sails["mizzen.driver"].state = SailState.SET
        return ship

    with_course = rigged(doc_of(SIXTY_FOUR), False)
    with_driver = rigged(her_doc_with_the_driver_bent(), True)
    for angle in (90, 100, 110, 120, 130, 140, 150):
        kn_c = units.ms_to_knots(_balanced_speed_ms(with_course, angle, 10.0))
        kn_d = units.ms_to_knots(_balanced_speed_ms(with_driver, angle, 10.0))
        assert kn_d > kn_c, (angle, kn_c, kn_d)


def test_truth_7_189_the_64_handles_as_a_ship_with_her_mizen_yard_and_her_spritsails(tmp_path):
    """Truth 7-189 (Build-Ships.md §15; Ext §10.3 item 4; D8 (b), D9 (c)), on `sixty-four.yaml` at
    seed 7, fifteen knots, six points off under plain sail. "Mainsail haul" swings the main and
    mizzen yards alone, the yards under the bowsprit going with the head yards at "let go and
    haul"; the mizen yard is never braced; the course is hauled aft at helm's a-lee (above: 7-230's
    clause) and brailed up hove to. Hove to with the spritsail and the sprit topsail set by name
    first, they are clewed up; she lies to within truth 12's band (below 1.6 kn, 45 to 65 degrees
    off, the heading steady within 15; measured 56-63 degrees off and 1.11 kn on the course, no
    aback). Her classing as the frigate's row is the test above."""
    world = _world(tmp_path)
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
    texts = [e.text for e in _after(world, start)]
    assert any(e.kind == "ship.hove_to" for e in _after(world, start)), texts
    assert not [e for e in _after(world, start) if e.kind == "ship.aback"]
    assert "Clewed up the fore topgallant, the spritsail and the sprit topsail." in texts
    for sid in ("spritsail", "sprit_topsail"):
        assert ship.sails[sid].state is SailState.IN_THE_GEAR
    assert ship.sails["mizzen.course"].state is SailState.IN_THE_GEAR
    assert ship.spars["mizzen.yard"].brace_angle == 0.0
    assert max(speeds) < 1.6
    assert all(45.0 <= o <= 65.0 for o in offs), (min(offs), max(offs))
    assert max(offs) - min(offs) <= 30.0


def test_truth_7_189_she_stays_quickly_and_wears_with_her_mizen_brailed():
    """Truth 7-189's clause of her mizen against the Bellona's report, that she stayed and wore
    quickly (Lavery 1985 p. 9; Bel §9; Ext §12 lens 4), judgement for a 64 of her class, on
    `sixty-four.yaml` at seed 7 in fifteen knots. Measured, in truth 10's form, from 290, 292.5 and
    295 degrees: 244, 251 and 266 s, gaining 104, 94 and 67 m (the course's tack at 9.43 m 246, 252
    and 262 s, 105, 95 and 66 m), under Luce's five minutes and well under the frigate-36's 343,
    447 and 370 s (51, -37 and 25 m), which are tacked here, so that the clause says what it claims
    if she is retuned. The band: quicker than the frigate-36's quickest (the report's "quickly",
    which gives no time) and no quicker than four minutes, a round floor of judgement that stands 4
    s under her quickest and has no source (stage A, her stand-in mizen course, 259, 283 and 327
    s). She is under truth 10's 285 s at all three headings, where stage A was at two; that band is
    not asked of her here, for the lead to rule. What sets it (TuningNotes, measured) is her small
    after sail against her lead, not the yards under her bowsprit: she is no quicker through
    the wind than the frigate-36, 124-132 s to "let go and haul" against 108-112, and falls off to
    her course sooner on the new tack. In truth 11's form she wears
    in 497 s (the frigate-36 513 s, within truth 11's six to twelve minutes), the mizen course
    brailed at "up helm" and hauled out by the wind, its yard never braced; so the model gives her
    no more than a quarter of a minute's quickness wearing, and that is reported, not forced.

    **Measured and not pinned: lying to as the Bellona did, under the mainsail and mizen staysail**
    (Lavery 1985, Table 2; Bel §9). With all else in and the helm a-lee she swings 44-70 deg off at
    1.1 kn in 15 kn, 42-78 at 1.8 in 25 kn, as the frigate-36 does (42-76 at 1.5; 41-85 at 1.5): no
    steady lie in the model, where "heave to" gives truth 12's (above)."""
    from tests.test_known_truths import FRIGATE, close_hauled_on_starboard, until

    frigate = []
    for heading in (290.0, 292.5, 295.0):
        world = close_hauled_on_starboard(FRIGATE, heading=heading)
        world.submit("tack ship")
        done, seconds = until(world, ("ship.tacked", "ship.missed_stays"), 900)
        assert [e.kind for e in done] == ["ship.tacked"], heading
        frigate.append(seconds)
    for heading in (290.0, 292.5, 295.0):
        world = close_hauled_on_starboard(SIXTY_FOUR, heading=heading)
        y_before = world.ship.dyn.y
        world.submit("tack ship")
        done, seconds = until(world, ("ship.tacked", "ship.missed_stays"), 900)
        assert [e.kind for e in done] == ["ship.tacked"], heading
        assert 240 <= seconds < min(frigate), (heading, seconds, frigate)
        assert world.ship.dyn.y > y_before, heading
        assert world.ship.spars["mizzen.yard"].brace_angle == 0.0

    world = close_hauled_on_starboard(SIXTY_FOUR)
    course = world.ship.sails["mizzen.course"]
    start = world.clock.tick
    world.submit("wear ship")
    _until(world, "Up helm", 60)
    assert "brail up the mizzen course" in next(
        e.text for e in _after(world, start) if "Up helm" in e.text
    )
    assert course.state is SailState.IN_THE_GEAR
    _until(world, "Haul out the mizzen course!", 700)
    done, _seconds = until(world, ("ship.wore", "evolution.failed"), 400)
    assert [e.kind for e in done] == ["ship.wore"]
    assert 360 <= world.clock.tick - start <= 720, world.clock.tick - start
    assert course.is_set and world.ship.dyn.tack == "larboard"
    assert world.ship.spars["mizzen.yard"].brace_angle == 0.0


@pytest.mark.parametrize("path", [SIXTY_FOUR, RAZEE])
def test_her_long_pole_heads_hold_truth_9(path):
    """Truth 9 on her files, in its own forms, since the long pole-heads moved the spars it carries
    away (`tests/test_known_truths.py` runs it on the frigate-36 and the schooner): in twenty knots
    under plain sail nothing carries away and no line parts; in thirty-five under all sail her
    royals and topgallants go. Measured at seed 7: the 64 loses 6 parts from tick 644, the razee 5
    from tick 632 (TuningNotes)."""
    from tests.test_known_truths import CARRIED_AWAY, events, sail_in_a_wind

    world = sail_in_a_wind(path, 20.0, "set plain sail")
    assert [e for e in world.log if e.kind in CARRIED_AWAY] == []
    assert events(world, "line.parted") == []
    world = sail_in_a_wind(path, 35.0, "make all sail")
    gone = [e for e in world.log if e.kind in CARRIED_AWAY]
    assert gone, "nothing carried away in 35 knots under all sail"
    assert any("royal" in e.subject or "topgallant" in e.subject for e in gone)


def test_the_slant_helper_gives_the_sprit_topsail_the_viewer_draws():
    """`spritsail_yards.drawn_by_slant`, the generator's report's figures, on the file's rounded
    figures: the head and foot `squareCut` draws (tests/test_view_geometry.py pins the drawing
    itself), the head within its yard."""
    sy = _helper("spritsail_yards")
    head, foot = sy.drawn_by_slant(103, 10.5, 17.5, 8.222)
    assert head == pytest.approx(9.30, abs=0.01) and foot == pytest.approx(15.75)
    assert sy.drawn_by_slant(103, 10.5, 17.5, 3.97)[0] == 10.5  # by the heights it filled the yard


# -- the helpers' refusals and the flips (Ext §9.3, §17.2: "a bad file cannot be written") -------


def _helper(name):
    """A pure helper of hers, `tools/ships/<name>.py`, imported by path (Ext §9.3: it imports
    nothing from the generator)."""
    spec = importlib.util.spec_from_file_location(
        f"{name}_under_test", ROOT / "tools" / "ships" / f"{name}.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_her_helpers_refuse_a_cut_that_breaks_its_contract():
    """Each helper raises a sentence where a cut would break Ext §3.4's, §4.1's, §9.3's or §17.2's
    assertions, so that no bad file can be written: the driver's boom under its head room or its
    taffrail; the after leech past Steel's band with the jaws no higher than the head room asks; the
    four corners outside a tenth of Steel's rule, at Steel's own fore leech (Ext §17.2's overshoot)
    and the other way; the head as long as the yard; the spritsail's foot in the water; a jib-boom
    too short for the sprit topsail's depth. Her own cut passes."""
    my, sy = _helper("mizen_yard"), _helper("spritsail_yards")
    mast = {"mast_x": -16.33, "rake_deg": 2.15, "frame_z": 3.22}
    crs = my.course(tack_z=8.73, steel=COURSE_ROW, yard_length_m=77.0 * FT, **mast)
    kw = {
        **mast,
        "steel": DRIVER_ROW,
        "course_steel": COURSE_ROW,
        "boom_length_m": (65.0 + 4.0 / 12.0) * FT,
        "driver_yard_m": DRIVER_YARD_M,
    }
    done = my.driver(crs, jaws_z=9.69, **kw)
    assert done["area"] == pytest.approx(203.0, abs=1.0)
    assert done["boom"]["rigged_out"] is False  # Ext §17.11: what the 64's and the 74's files file
    with pytest.raises(ValueError, match="head room"):
        my.driver(crs, jaws_z=9.69, under=[(-27.62, 7.86, 3.0)], **kw)
    with pytest.raises(ValueError, match="taffrail"):
        my.driver(crs, jaws_z=9.69, over=[(-28.35, 11.0)], **kw)
    with pytest.raises(ValueError, match="after leech"):
        my.driver(crs, jaws_z=9.40, **kw)  # 0.3 m under her jaws: the leech past Steel's top
    with pytest.raises(ValueError, match="outside a tenth"):
        my.driver(crs, jaws_z=17.19 - 9.5 * YD, **kw)  # Steel's own fore leech: 222 m2, +11%
    with pytest.raises(ValueError, match="outside a tenth"):
        my.driver(crs, jaws_z=11.9, **kw)  # the fore leech too short the other way
    with pytest.raises(ValueError, match="fore part bare"):
        my.course(tack_z=8.73, steel=COURSE_ROW, yard_length_m=10.0, **mast)
    head = {"root": (25.15, 4.88), "steeve_deg": 27.0, "bowsprit_out_m": 13.53, "jib_out_m": 7.78}
    ss = {"yard_m": 57.5 * FT, "head_cloths": 26.0, "foot_cloths": 26.0, "depth_yd": 7.5}
    st = {"yard_m": 34.5 * FT, "head_cloths": 17.0, "foot_cloths": 27.0, "depth_yd": 9.0}
    assert sy.cut(**head, spritsail=ss, sprit_topsail=st)["sprit_topsail"][
        "slant"
    ] == pytest.approx(9.0 * YD, abs=0.01)
    with pytest.raises(ValueError, match="foot stands"):
        sy.cut(**head, spritsail=ss, hang=3.5)
    with pytest.raises(ValueError, match="short of the sprit topsail"):
        sy.cut(**{**head, "jib_out_m": 2.0}, spritsail=ss, sprit_topsail=st)


FLIP_PROBE = """
import sys
sys.path.insert(0, "tools")
import gen_ships
sys.modules["gen_ships"] = gen_ships
from ships import indefatigable as her
her.MIZEN_COURSE = sys.argv[2]
her.DRIVER = sys.argv[3] == "driver"
her.BOWSPRIT_YARDS = False
her.build(sys.argv[1])
"""


@pytest.mark.parametrize(
    "course, driver, writes",
    [("stand-in", "driver", False), ("stand-in", "no", True), ("gated", "no", True)],
)
def test_her_flips_stand_each_by_itself(tmp_path, course, driver, writes):
    """Indf §0; Ext §17.2: the module refuses the driver unless the course is cut at the mast, a
    lateen's yard being a `lateen_yard`, and each flip writes a file of its own for the measure
    old beside new: the stand-in's `gaff` yard, or the lateen's with no driver and no boom; neither
    has yards under the bowsprit."""
    done = subprocess.run(
        [sys.executable, "-c", FLIP_PROBE, str(tmp_path), course, driver],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if not writes:
        assert done.returncode != 0 and "DRIVER is True" in done.stderr
        return
    assert done.returncode == 0, done.stderr
    ship = load_ship(str(tmp_path / "sixty-four.yaml"))
    assert ship.spars["mizzen.yard"].cls == ("gaff" if course == "stand-in" else "lateen_yard")
    assert "mizzen.driver" not in ship.sails and "mizzen.boom" not in ship.spars
    assert "spritsail" not in ship.sails and "spritsails" not in ship.groups
