"""Package 8: the reference ships' particulars stay within their period ranges.

The frigate is the Amazon class of 1795 (Winfield's dimensions) rigged by the
rules of Luce 1866 ch. VII; the schooner a Baltimore-built topsail schooner of
about 1804 after Chapelle. The ranges here are wide enough for tuning within
the type and narrow enough that a slip of a decimal, a spar drawn at the wrong
scale or a sail area doubled in a hand edit fails. `tools/gen_ships.py` is the
source of both files; the last test regenerates them and compares.
"""

from __future__ import annotations

import math
import subprocess
import sys
from pathlib import Path

import pytest

from freesail import units
from freesail.orders.resolve import noun_table
from freesail.ship.loader import load_ship

ROOT = Path(__file__).resolve().parents[1]
FRIGATE = ROOT / "data" / "ships" / "frigate-36.yaml"
SCHOONER = ROOT / "data" / "ships" / "topsail-schooner.yaml"


@pytest.fixture(scope="module")
def frigate():
    return load_ship(FRIGATE)


@pytest.fixture(scope="module")
def schooner():
    return load_ship(SCHOONER)


def area_of(ship, group):
    return sum(ship.sails[i].area_m2 for i in ship.groups[group])


def truck_height(ship, mast):
    """Height above the deck of the top of the mast's uppermost stick."""
    masts = {"mast", "topmast", "topgallant_mast", "royal_mast"}
    top = mast
    while True:
        above = [s for s in ship.spars.values() if s.parent == top and s.cls in masts]
        if not above:
            break
        top = above[0].id
    return sum(s.height_m for s in ship.spar_chain(top))  # the chain includes the top itself


# ---------------------------------------------------------------------------
# the frigate: a 36-gun 18-pounder of the 1790s
# ---------------------------------------------------------------------------


def test_frigate_hull_is_an_amazon_class_frigate(frigate):
    h = frigate.hull.spec
    # gundeck 143 ft, keel 119 ft 6 in: the load line lies between them
    assert units.m_to_feet(36.4) < units.m_to_feet(h.length_waterline_m) < 143.0
    assert 11.4 <= h.beam_m <= 12.0  # 38 ft 4 in extreme breadth
    assert 4.2 <= h.draught_m <= 5.2  # 14 to 17 ft mean, stored for sea
    # displacement of a 930-ton-burthen frigate: 1.2 to 1.5 times the burthen
    assert 1_100_000 <= h.displacement_kg <= 1_450_000
    assert 1.0 <= h.gm_m <= 1.6  # 3 ft 3 in to 5 ft 3 in
    assert 12.0 <= h.hull_speed_kn <= 14.0  # the type's best of 12 to 13 knots
    assert 0.0 <= h.clr_x_m <= 4.0  # a little forward of midships, never abaft
    assert 1.4 <= h.deck_height_m <= 2.4


def test_frigate_plain_sail_area_is_in_period(frigate):
    plain = area_of(frigate, "plain sail")
    # about 17,000 sq ft; a 36 carried 14,000 to 20,000 sq ft of plain sail
    assert 1_300 <= plain <= 1_860
    all_sail = area_of(frigate, "all sail")
    assert 2_000 <= all_sail <= 3_000
    # the main topsail is the largest sail, then the main course
    areas = {s.id: s.area_m2 for s in frigate.sails.values()}
    assert max(areas, key=areas.get) == "main.topsail"
    assert areas["main.course"] > areas["fore.course"] > areas["mizzen.topsail"]
    assert areas["main.topsail"] > areas["fore.topsail"] > areas["mizzen.topsail"]


def test_frigate_spars_follow_the_masting_rules(frigate):
    sp = frigate.spars
    lwl_ft = units.m_to_feet(frigate.hull.spec.length_waterline_m)
    beam_ft = units.m_to_feet(frigate.hull.spec.beam_m)
    main_len_ft = (lwl_ft + beam_ft) / 2.0  # Luce: heel to head
    # the main lower mast stands about 74 ft above the deck (88 ft less the step)
    assert 20.0 <= sp["main.mast"].height_m <= 24.0
    # fore 9/10 of the main, mizzen shorter still
    assert sp["fore.mast"].height_m < sp["main.mast"].height_m
    assert sp["mizzen.mast"].height_m < sp["fore.mast"].height_m
    # main yard 10/11 of the main mast (Luce) or 0.575 of the gundeck (Falconer): 78 to 84 ft
    assert 23.5 <= sp["main.yard"].length_m <= 25.7
    assert sp["main.yard"].length_m == pytest.approx(
        units.feet_to_m(main_len_ft * 10.0 / 11.0), abs=0.6
    )
    # topsail yard three quarters of the lower, topgallant 9/14 of that
    assert 0.7 <= sp["main.topsail.yard"].length_m / sp["main.yard"].length_m <= 0.8
    assert 0.6 <= sp["main.topgallant.yard"].length_m / sp["main.topsail.yard"].length_m <= 0.7
    # the main truck 40 to 48 m above the deck (the ship is 43.6 m on the gundeck)
    assert 40.0 <= truck_height(frigate, "main.mast") <= 48.0
    assert truck_height(frigate, "fore.mast") < truck_height(frigate, "main.mast")
    assert truck_height(frigate, "mizzen.mast") < truck_height(frigate, "fore.mast")
    # yards hang below the head of the mast they are on, in order aloft
    for m in ("fore", "main"):
        assert sp[f"{m}.yard"].height_m < sp[f"{m}.topsail.yard"].height_m
        assert sp[f"{m}.topsail.yard"].height_m < sp[f"{m}.topgallant.yard"].height_m
        assert sp[f"{m}.topgallant.yard"].height_m < sp[f"{m}.royal.yard"].height_m
        assert sp[f"{m}.royal.yard"].height_m < truck_height(frigate, f"{m}.mast")
    # bowsprit 5/8 of the main mast, a third inboard: 35 to 40 ft outboard
    assert 10.0 <= sp["bowsprit"].length_m <= 12.5
    # brace limits kept from integration: 28 to 35 degrees of yard to keel sharp up
    for s in sp.values():
        if s.is_yard:
            # Fincham 1843 art. 102: the long ships' lower yards 61 to 67 from square, two
            # degrees a level aloft (spec 3b §2.1); the crossjack 60
            assert 58.0 <= math.degrees(s.brace_limit) <= 70.0


def test_frigate_sail_centres_rise_with_their_yards(frigate):
    for m in ("fore", "main", "mizzen"):
        levels = ["topsail", "topgallant", "royal"]
        if m != "mizzen":
            levels.insert(0, "course")
        zs = [frigate.sails[f"{m}.{lvl}"].centre_height_m for lvl in levels]
        assert zs == sorted(zs)
        for lvl, z in zip(levels, zs, strict=True):
            yard = frigate.yard_of(f"{m}.{lvl}")
            assert z < yard.height_m + frigate.hull.spec.deck_height_m
    # the plain-sail centre of effort is a little forward of the centre of lateral
    # resistance, within the ship's beam of it; further would gripe or fall off
    plain = frigate.groups["plain sail"]
    area = area_of(frigate, "plain sail")
    ce_x = sum(frigate.sails[i].area_m2 * frigate.sails[i].x_m for i in plain) / area
    assert abs(ce_x - frigate.hull.spec.clr_x_m) < frigate.hull.spec.beam_m


def test_frigate_ratings_are_ordered_aloft(frigate):
    """Lighter gear aloft is weaker: royal < topgallant < topsail < lower, each mast."""
    sp = frigate.spars
    for m in ("fore", "main", "mizzen"):
        masts = [f"{m}.royal_mast", f"{m}.topgallant_mast", f"{m}.topmast", f"{m}.mast"]
        ratings = [sp[i].rating_kn for i in masts]
        assert ratings == sorted(ratings), m
        yards = [f"{m}.royal.yard", f"{m}.topgallant.yard", f"{m}.topsail.yard"]
        if m != "mizzen":
            yards.append(f"{m}.yard")
        ratings = [sp[i].rating_kn for i in yards]
        assert ratings == sorted(ratings), m
    # lines follow the rope: a main topsail sheet (5.5 in) is stouter than a royal sheet
    ln = frigate.lines
    assert (
        ln["main.topsail.sheet.starboard"].rating_kn
        > ln["main.topgallant.sheet.starboard"].rating_kn
    )
    assert (
        ln["main.topgallant.sheet.starboard"].rating_kn > ln["main.royal.sheet.starboard"].rating_kn
    )
    assert ln["main.stay"].rating_kn > ln["main.topmast.stay"].rating_kn > ln["jib.stay"].rating_kn
    # the file states every rating: no defaults were filled in
    assert frigate.spec.warnings == []
    # light canvas aloft blows out before the courses and topsails would
    sails = frigate.sails
    assert sails["main.royal"].cloth_rating_kn / sails["main.royal"].area_m2 < (
        sails["main.topsail"].cloth_rating_kn / sails["main.topsail"].area_m2
    )


def test_frigate_head_stays_lead_from_the_right_mastheads(frigate):
    assert frigate.lines["fore.topmast.stay"].of == "fore.topmast"
    assert frigate.lines["jib.stay"].of == "fore.topmast"
    assert frigate.lines["flying_jib.stay"].of == "fore.topgallant_mast"
    assert [s.id for s in frigate.spar_chain("jib")] == ["fore.topmast", "fore.mast"]


# ---------------------------------------------------------------------------
# the schooner: a Baltimore-built topsail schooner of about 1804
# ---------------------------------------------------------------------------


def test_schooner_hull_is_lynx_of_1812(schooner):
    """Kemp's Lynx (H.M. schooner Musquidobit), Chapelle 1930 pp. 82-83: 94 ft 7 in on
    deck, 73 ft 1 in keel, 24 ft 0 in beam, 10 ft 3 in depth, 223 91/94 tons."""
    h = schooner.hull.spec
    # the load line lies between the keel and the deck of a hull with raking ends
    assert units.feet_to_m(73.1) < h.length_waterline_m < units.feet_to_m(94.6)
    assert 7.1 <= h.beam_m <= 7.5  # 24 ft 0 in extreme
    assert 3.3 <= h.length_waterline_m / h.beam_m <= 3.9  # Lynx and Grecian are 3.95 on deck
    assert 2.9 <= h.draught_m <= 3.8  # Marestier's 0.35 / 0.56 of the beam: 8 ft 5 in / 13 ft 4 in
    assert 170_000 <= h.displacement_kg <= 250_000  # 0.85 to 1.1 x 224 tons burthen
    assert 0.8 <= h.gm_m <= 1.3
    assert 10.5 <= h.hull_speed_kn <= 12.5
    assert -1.5 <= h.clr_x_m <= 1.0
    assert h.deck_height_m < 1.3  # a low-sided vessel: port sills 3 ft 5 in above water


def test_schooner_sail_plan_follows_fincham(schooner):
    """Fincham's rules for two-masted schooners as Chapelle gives them (pp. 160-161), at
    the upper end of each range for an American vessel. Ranges widened from the first
    draft (plain sail 420-650 m2) because Chapelle's Spider carried 6,499 sq ft on an
    80 ft deck and a Baltimore-built 75-footer 8,854 (p. 167): 95 ft of Lynx wants
    6,500 to 8,000 sq ft of plain sail."""
    plain = area_of(schooner, "plain sail")
    assert 600 <= plain <= 750
    assert 700 <= area_of(schooner, "all sail") <= 900  # the Prides carry 840 to 870
    areas = {s.id: s.area_m2 for s in schooner.sails.values()}
    assert (
        areas["main.sail"] > areas["fore.sail"] > areas["fore.topsail"] > areas["fore.topgallant"]
    )
    sp = schooner.spars
    beam = schooner.hull.spec.beam_m
    lwl = schooner.hull.spec.length_waterline_m
    assert sp["main.mast"].height_m > sp["fore.mast"].height_m  # the main is the taller stick
    # mainmast heel to hounds 2.6 to 2.8 x the beam, less the 11 ft to the deck, plus head
    assert 2.4 * beam <= sp["main.mast"].height_m + units.feet_to_m(11.0) <= 3.3 * beam
    assert 17.5 <= sp["fore.mast"].height_m <= 20.5
    assert 0.62 * lwl <= sp["main.boom"].length_m <= 0.74 * lwl  # 0.66 to 0.7 x LWL
    assert 0.44 <= sp["main.gaff"].length_m / sp["main.boom"].length_m <= 0.53
    assert 0.32 * lwl <= sp["fore.topsail.yard"].length_m <= 0.44 * lwl  # 0.7-0.75 x fore yard
    assert 27.0 <= truck_height(schooner, "main.mast") <= 33.0
    assert 26.0 <= truck_height(schooner, "fore.mast") <= 32.0
    # the sails sit abaft their raked masts, the mainsail well abaft its
    assert schooner.sails["main.sail"].x_m < sp["main.mast"].x_m - 5.0
    assert schooner.sails["fore.topsail"].x_m < sp["fore.mast"].x_m
    assert schooner.spec.warnings == []


# ---------------------------------------------------------------------------
# both: the names an officer would use resolve, and the generator is the source
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "path, phrases",
    [
        (
            FRIGATE,
            [
                "spanker",
                "driver",
                "cro'jack yard",
                "crossjack",
                "spanker boom",
                "driver boom",
                "kites",
                "head sails",
                "jibs",
                "topsail yards",
                "topgallant yards",
                "royal yards",
                "lower yards",
                "upper yards",
                "topmasts",
                "royal masts",
                "light sails",
                "middle staysail",
                "topgallant sails",
                "fore topmast stays'l",
            ],
        ),
        (
            SCHOONER,
            ["fore", "main", "gaff topsail", "gaff sails", "jibs", "kites", "light sails"],
        ),
    ],
)
def test_period_names_resolve(path, phrases):
    """Object phrases as the grammar hands them to the resolver: the article already gone."""
    ship = load_ship(path)
    table = noun_table(ship)
    for phrase in phrases:
        assert table.lookup(phrase) is not None, phrase


def test_generator_reproduces_the_committed_files(tmp_path):
    out = tmp_path / "ships"
    subprocess.run(
        [sys.executable, str(ROOT / "tools" / "gen_ships.py"), str(out)],
        check=True,
        cwd=ROOT,
        capture_output=True,
    )
    for committed in (FRIGATE, SCHOONER):
        made = out / committed.name
        assert made.exists()
        # Compare as text so that a Windows checkout with CRLF endings
        # (or a generator run there) is not a difference.
        assert made.read_text() == committed.read_text(), (
            f"{committed.name} differs from what tools/gen_ships.py writes; "
            "edit the generator and rerun it"
        )
