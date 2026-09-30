"""Package 8: the reference ships' particulars stay within their period ranges.

The frigate is the Amazon class of 1795 (Winfield's dimensions) rigged by the
rules of Luce 1866 ch. VII; the schooner a Baltimore-built topsail schooner of
about 1804 after Chapelle; package 32b adds the cutter Sherbourne of 1763 (85
tons, sparred by Fincham 1843 p. 67 and canvassed by Steel 1794) and the brig
Harpy of 1796 (316 tons, Fincham p. 88). The ranges here are wide enough for
tuning within the type and narrow enough that a slip of a decimal, a spar drawn
at the wrong scale or a sail area doubled in a hand edit fails.
`tools/gen_ships.py` is the source of all four files; the last test regenerates
them and compares.
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
CUTTER = ROOT / "data" / "ships" / "cutter.yaml"
BRIG = ROOT / "data" / "ships" / "brig.yaml"


@pytest.fixture(scope="module")
def frigate():
    return load_ship(FRIGATE)


@pytest.fixture(scope="module")
def schooner():
    return load_ship(SCHOONER)


@pytest.fixture(scope="module")
def cutter():
    return load_ship(CUTTER)


@pytest.fixture(scope="module")
def brig():
    return load_ship(BRIG)


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
# the cutter: Sherbourne of 1763, 85 tons, a revenue-cruiser rig (package 32b)
# ---------------------------------------------------------------------------


def test_cutter_hull_is_a_cutter_of_85_tons(cutter):
    """54 ft 6 in on deck and 44 ft 4 in of keel by the burthen rule at 19 ft of beam, 85
    tons; drawing 9 ft 6 in aft, 7 ft 6 in forward (Fincham 1843 p. 67, excess draught
    aft 24 in). Deep and beamy: L/B under 3, displacement 1.1 to 1.4 x the burthen."""
    h = cutter.hull.spec
    assert units.feet_to_m(44.3) < h.length_waterline_m < units.feet_to_m(54.5)
    assert 5.6 <= h.beam_m <= 6.0  # 19 ft extreme
    assert 2.4 <= h.length_waterline_m / h.beam_m <= 2.9
    assert 2.3 <= h.draught_m <= 2.9  # mean of 9 ft 6 in and 7 ft 6 in
    assert 90_000 <= h.displacement_kg <= 125_000  # 1.1 to 1.4 x 85 tons burthen
    assert 0.9 <= h.gm_m <= 1.4  # stiff: a cutter carries a great mainsail
    assert 8.5 <= h.hull_speed_kn <= 10.5
    assert -1.0 <= h.clr_x_m <= 0.5
    assert h.deck_height_m < 1.2


def test_cutter_sail_plan_follows_fincham_and_steel(cutter):
    """Fincham 1843 p. 67 (second revenue cruiser column): main mast hounded 2.6 x the
    beam, boom 0.87 of the length on deck, gaff 0.64 of the boom, bowsprit 0.79 of the
    length outside the stem, square-sail yard 0.84 and topsail yard 0.70 of the length;
    topsail yard 0.70 and topgallant yard 0.44 of the square-sail yard; the 85-ton
    cutter's canvas of his footnote (mainsail 1566, foresail 367, second jib 541 sq ft)
    and Steel 1794 for the rest. One mast, no tops, a running bowsprit."""
    plain = area_of(cutter, "plain sail")
    assert 230 <= plain <= 310
    assert 370 <= area_of(cutter, "all sail") <= 480
    areas = {s.id: s.area_m2 for s in cutter.sails.values()}
    assert areas["main.sail"] > areas["square_sail"] > areas["topsail"] > areas["topgallant"]
    assert areas["jib"] > areas["fore.staysail"]  # a cutter's jib is her larger head sail
    assert 130 <= areas["main.sail"] <= 165  # 1400 to 1750 sq ft about Fincham's 1566
    sp = cutter.spars
    beam = cutter.hull.spec.beam_m
    on_deck = units.feet_to_m(54.5)
    masts = [s for s in sp.values() if s.cls == "mast"]
    assert len(masts) == 1 and masts[0].id == "main.mast"
    assert 2.4 * beam <= sp["main.mast"].height_m <= 3.0 * beam  # hounded 2.6 B plus the head
    assert 0.80 * on_deck <= sp["main.boom"].length_m <= 0.95 * on_deck
    assert 0.58 <= sp["main.gaff"].length_m / sp["main.boom"].length_m <= 0.70
    assert 0.78 * on_deck <= sp["square_sail.yard"].length_m <= 0.90 * on_deck
    sq_yard = sp["square_sail.yard"].length_m
    assert 0.64 * sq_yard <= sp["topsail.yard"].length_m <= 0.76 * sq_yard
    assert 0.38 * sq_yard <= sp["topgallant.yard"].length_m <= 0.50 * sq_yard
    assert 22.0 <= truck_height(cutter, "main.mast") <= 27.0
    bowsprit = sp["bowsprit"]
    assert bowsprit.running and bowsprit.rigged_out
    assert 0.5 * bowsprit.full_length_m <= bowsprit.housed_length_m <= 0.8 * bowsprit.full_length_m
    assert 0.5 * on_deck <= bowsprit.full_length_m <= 0.7 * on_deck  # 0.79 L less the housing
    # the mainsail stands well abaft her one mast; the jib's tack rides the bowsprit end
    assert cutter.sails["main.sail"].x_m < sp["main.mast"].x_m - 4.0
    assert cutter.sails["jib"].x_m > sp["bowsprit"].x_m
    assert cutter.spec.warnings == []


# ---------------------------------------------------------------------------
# the brig: Harpy of 1796, 316 tons, the frigate less a mast (package 32b)
# ---------------------------------------------------------------------------


def test_brig_hull_is_harpy_of_1796(brig):
    """95 ft on the gun deck, 75 ft 1 5/8 in of keel, 28 ft 1 1/2 in of beam, 316 tons;
    drawing about 11 ft 6 in (Fincham 1843 p. 88, the first brig of war of 100 x 30.5 ft
    scaled to her)."""
    h = brig.hull.spec
    assert units.feet_to_m(75.1) < h.length_waterline_m < units.feet_to_m(95.0)
    assert 8.4 <= h.beam_m <= 8.8  # 28 ft 1.5 in extreme
    assert 2.9 <= h.length_waterline_m / h.beam_m <= 3.4
    assert 3.2 <= h.draught_m <= 3.9
    assert 350_000 <= h.displacement_kg <= 450_000  # 1.1 to 1.4 x 316 tons burthen
    assert 0.8 <= h.gm_m <= 1.2
    assert 10.5 <= h.hull_speed_kn <= 12.5
    assert -1.0 <= h.clr_x_m <= 1.5
    assert h.deck_height_m < 2.0


def test_brig_sail_plan_follows_fincham(brig):
    """Fincham 1843 p. 88, the first brig of war: two masts, the main the taller, yards
    alike on both, royals on the topgallant pole, a boom mainsail (Steel 1794 p. 119,
    three reef bands), the frigate's head sails and studding sails scaled to her."""
    plain = area_of(brig, "plain sail")
    assert 680 <= plain <= 850
    assert 1150 <= area_of(brig, "all sail") <= 1400
    areas = {s.id: s.area_m2 for s in brig.sails.values()}
    assert areas["main.spanker"] == max(areas.values())  # the boom mainsail is her great sail
    assert areas["main.topsail"] >= areas["fore.topsail"] > areas["fore.course"]
    assert areas["fore.topgallant"] > areas["fore.royal"]
    sp = brig.spars
    masts = [s.id for s in sp.values() if s.cls == "mast"]
    assert sorted(masts) == ["fore.mast", "main.mast"]
    assert sp["main.mast"].height_m > sp["fore.mast"].height_m
    assert sp["fore.yard"].length_m == sp["main.yard"].length_m
    beam = brig.hull.spec.beam_m
    assert 1.7 * beam <= sp["main.yard"].length_m <= 2.0 * beam
    assert 0.72 <= sp["main.topsail.yard"].length_m / sp["main.yard"].length_m <= 0.82
    assert 29.0 <= truck_height(brig, "main.mast") <= 35.0
    assert 27.0 <= truck_height(brig, "fore.mast") <= 33.0
    assert not sp["bowsprit"].running and "jib_boom" in sp and "flying_jib_boom" in sp
    assert len(brig.groups["studdingsails"]) == 10
    assert len(brig.groups["storm canvas"]) == 3
    assert brig.sails["main.spanker"].x_m < sp["main.mast"].x_m - 5.0
    assert brig.spec.warnings == []


# ---------------------------------------------------------------------------
# all four: the names an officer would use resolve, and the generator is the source
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
        (
            CUTTER,
            [
                "mainsail",
                "main",
                "fore",
                "foresail",
                "crossjack",
                "crossjack yard",
                "gaff topsail",
                "trysail",
                "storm mainsail",
                "head sails",
                "mast",
                "heel rope",
                "topgallant sails",
            ],
        ),
        (
            BRIG,
            [
                "spanker",
                "driver",
                "boom mainsail",
                "trysail",
                "middle staysail",
                "kites",
                "head sails",
                "upper yards",
                "fore yard",
                "main yard",
                "spanker boom",
                "storm staysails",
                "royal masts",
            ],
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
    for committed in (FRIGATE, SCHOONER, CUTTER, BRIG):
        made = out / committed.name
        assert made.exists()
        # Compare as text so that a Windows checkout with CRLF endings
        # (or a generator run there) is not a difference.
        # read both as UTF-8: Windows would otherwise read them in cp1252 (gate 3b, owner)
        assert made.read_text(encoding="utf-8") == committed.read_text(encoding="utf-8"), (
            f"{committed.name} differs from what tools/gen_ships.py writes; "
            "edit the generator and rerun it"
        )


def test_a_ships_path_is_kept_with_forward_slashes_whatever_the_platform(tmp_path):
    """A save or a scenario written on Windows replays on Linux and the other way about:
    the ship's source path is stored with forward slashes, and a path read back with
    backslashes (the owner's saves of gate 4b carried 'data\\\\ships\\\\frigate-36.yaml')
    is accepted (gate 4c, 2026-09-29)."""
    from freesail.ship.loader import load_ship

    ship = load_ship("data\\ships\\frigate-36.yaml")
    assert ship.save_ref() == {"type": "file", "path": "data/ships/frigate-36.yaml"}
    assert load_ship("data/ships/frigate-36.yaml").save_ref() == ship.save_ref()
