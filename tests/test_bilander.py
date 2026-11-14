"""Package 75, the third ship (B4): the bilander Hopewell, a British coasting bilander under a
settee main.

Her design is docs/design/Design-Ship-Bilander.md (Bil-D), from the research note
docs/design/Research-Bilander-2026-10.md (Bil) and the engine's design for her settee
(docs/design/Design-ShipsEngineExtensions.md, Ext, §5); `tools/ships/bilander.py` writes her file,
`data/ships/bilander.yaml`, and `tools/ships/settee.py` cuts her settee. These are her tests
(Bil-D §14; Build-Ships.md §14.1), in the band form of tests/test_ship_particulars.py with the
source of each band in a comment. Begun with her road's steps 1 and 2 (Bil-D §13): her hull block
against Chapman and Lloyd's and her burthen by the old measure; her profile against Chapman, Gwyn
and Steel 1805's brig collier, her stand-in under the water, and a mark on every shape line; her
masts and yards against Gwyn's shares and Chapman's yards; her settee's cut and contract, and
`settee.py`'s checks each raised in words; her spritsail and main topmast staysail bent and out of
plain sail; the generator's report and her file as committed; her file loading, rated, and her
polar beside the brig's, with rule 1's clause of truth 7-197 drafted on it. Her road's step 3
(Bil-D §5-§8): her two fits, unarmed by default and the armed merchant, its guns against Lloyd's,
Adye and Falconer, each on its port or on her rail, and the builder's checklist for the viewer
(Build-Ships.md §6's postscript); her broadside by 70's rule; her armed fit's lowest lee port by
7-190's form; her company of eight and her wardroom file; the beat to quarters on the armed fit,
measured; her ground tackle, boat, pumps, hold, stores and ration; her description in her file
and through the index, and her role by every intent. Her road's step 4 (Bil-D §9, §14): her polar
recorded beside the brig-sloop's and the merchant brig's, §9's knobs each beside its start and its
bound (`clr_x_m` tuned for her helm, the rest kept), her helm and truth 6's form, and truth 7-197
whole. Her road's step 5, on the engine's settee (B3.3; Bil-D §12.2, §14; Ext §5): her heave-to
both ways, her sheet's block against her taffrail, rule 5's measure on her file, her settee
requests at eight by watch, truths 7-198 and 7-199 on her file, and her first hour at seed 7 with
no fit named; each judged by her heading and tack a set time after, never by "Tacked" (D13 (a)).
And B3.3b's guard on her file: forced round hove to, her settee dipped first at "fill away".
The untried manoeuvres, run once on her file, are recorded in docs/dev/TuningNotes.md.

The figures quoted as measured were measured on the owner's machine (Windows 11, 2026-11-08);
the bands are the sources' or judgement where they say so.
"""

from __future__ import annotations

import importlib.util
import json
import math
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

import pytest
import yaml

from freesail import units
from freesail.api.readings import ship_class_words
from freesail.ship import form as drawn
from freesail.ship.loader import load_ship, load_spec
from freesail.ship.parts import SailState
from freesail.world.ships import polar_of

ROOT = Path(__file__).resolve().parents[1]
HER = "data/ships/bilander.yaml"
BRIG = "data/ships/brig.yaml"
FT = units.FOOT
SW_FT = 0.2969  # the Swedish foot (Bil §2.4)
# her datum, her upper deck at side at x 0 (Bil-D §2.2, judgement)
DATUM_M = 0.92
# Chapman's No. 5 (Bil §2.4, measured): the rail 5.3-5.5 ft above the water, 75.6 ft taffrail to
# stem head; Gwyn's heights laid on them as shares of the rail length (Bil-D §1.4)
WAIST_M = 5.4 * FT
RAIL_LENGTH_M = 75.6 * FT


@pytest.fixture(scope="module")
def her():
    return load_ship(HER)


@pytest.fixture(scope="module")
def spec():
    """Her file's spec, its spars, sails and lines by id."""
    s = load_spec(HER)
    return (
        s,
        {x.id: x for x in s.spars},
        {x.id: x for x in s.sails},
        list(s.lines),
    )


@pytest.fixture(scope="module")
def doc():
    return yaml.safe_load((ROOT / HER).read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def settee():
    """`tools/ships/settee.py`, pure, imported as a module (it imports nothing of the generator)."""
    spec = importlib.util.spec_from_file_location(
        "settee_under_test", ROOT / "tools" / "ships" / "settee.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


MODULE_PROBE = """
import json, sys
sys.path.insert(0, "tools")
import gen_ships
sys.modules["gen_ships"] = gen_ships
from ships import bilander as her
print(json.dumps({
    "fore": her.COLLIER_FORE, "aft": her.COLLIER_AFT, "folio": her.COLLIER_FOLIO_I,
    "length_ft": her.COLLIER_LENGTH_FT, "length_ratio": her.LENGTH_RATIO,
    "beam_ratio": her.BEAM_RATIO, "taffrail": her.TAFFRAIL_X, "stem_head": her.STEM_HEAD_X,
    "mast_x": her.MAST_X, "rig": her.RIG_Z, "depth": her.collier_drawn_depth(),
}, ensure_ascii=True))
"""


@pytest.fixture(scope="module")
def module():
    """The module's figures, read through the generator as its hook runs it (a subprocess, so
    that this process keeps no second copy of the generator)."""
    done = subprocess.run(
        [sys.executable, "-c", MODULE_PROBE],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert done.returncode == 0, done.stderr
    return json.loads(done.stdout)


def above_water(spars, spar_id):
    """A spar's height above her water: the file's height above the datum and the datum."""
    return spars[spar_id].height_m + DATUM_M


# ---------------------------------------------------------------------------
# Her hull (Bil-D §2.1)
# ---------------------------------------------------------------------------


def test_her_hull_holds_chapman_and_lloyds(her):
    hull = her.hull.spec
    assert her.spec.rig == "bilander"
    assert her.spec.name == "Hopewell"  # the owner's answer, "Hopewell is fine" (Bil-D §17)
    # Chapman 1768 Pl. LXII No. 5, 72.5 Swedish ft sternpost to stem, +-1.5-2 ft (Bil §2.4)
    assert hull.length_waterline_m == pytest.approx(21.5, abs=0.5)
    # 19.9 Swedish ft between the breadth marks, +-1.5% (Bil §2.4)
    assert hull.beam_m == pytest.approx(5.91, abs=0.1)
    # Lloyd's bilanders of 130 tons, 11 and 12 ft loaded (Bil §2.2, read): their mean +-0.5 ft
    assert hull.draught_m == pytest.approx(3.51, abs=0.16)
    # the brig's method, LWL x B x T x 0.50 x 1025 (D7 (a), judgement)
    assert hull.displacement_kg == pytest.approx(229000.0, abs=1000.0)
    # the brig's 11.5 kn by the root of the waterlines, within her design's knob (9.8-10.8 kn)
    assert 9.8 <= hull.hull_speed_kn <= 10.8
    assert hull.deck_height_m == pytest.approx(DATUM_M)


def test_her_burthen_by_the_old_measure_is_about_130_tons():
    """(L - 3/5 B) x B x B/2 / 94 on her breadth gives 118 tons on her waterline and 128 on her
    length taffrail to stem head (Bil §2.4; Bil-D §2.1): D6 (a)'s "about 130", the register's
    bilanders of 120-140 tons (Bil §2.2)."""
    b = 19.4
    for length, tons in ((70.6, 118.0), (75.6, 128.0)):
        assert (length - 0.6 * b) * b * b / 2.0 / 94.0 == pytest.approx(tons, abs=0.5)


# ---------------------------------------------------------------------------
# Her profile and shape (Bil-D §3)
# ---------------------------------------------------------------------------

SHAPE_LINES = (
    "rail_m",
    "breadth_m",
    "keel_m",
    "stem_m",
    "stern_m",
    "wales_m",
    "section_m",
    "decks_m",
    "ports_m",
    "port_size_m",
    "head_m",
    "breadth_line_m",
    "sections_m",
    "rabbet_m",
)


def test_every_line_of_her_shape_carries_its_rung(doc):
    """Build-Ships.md §5.0 principle 4 and Bil-D §3.2's marks after step 1: Gwyn's lines and the
    collier's stand-in (S†); the keel, the stem and the stern judged at their weakest points (the
    post's heel and rake, the fore-foot's curve); her decks and ports judged; her stern's type and
    her head's word sourced (Gwyn, needing no scale), its lights stand-in. No floor_m: the collier's
    table prints no rising line. Her rabbet kept and not drawn (principle 11; her review,
    2026-11-08: Folio I's sidings read at her step 1 and kept): at the collier's base scaled,
    -2.65 m, from the post to the fore-foot, its half-sidings Folio I's R, S and T (9 1/2, 12 and
    9 1/2 in) at her beam ratio, judged at the rabbet's place in the keel's depth."""
    profile = doc["hull"]["profile"]
    marks = profile["marks"]
    for line in SHAPE_LINES:
        assert line in profile and line in marks, line
    assert "floor_m" not in profile
    assert profile["rabbet_m"] == [[-10.4, -2.65, 0.1], [2.37, -2.65, 0.13], [8.13, -2.65, 0.1]]
    assert profile["rabbet_m"][-1][0] == profile["keel_m"][-1][0]
    assert {k for k, v in marks.items() if v == "judged"} == {
        "keel_m",
        "rabbet_m",
        "stem_m",
        "stern_m",
        "decks_m",
        "ports_m",
        "port_size_m",
        "form.fullness",
    }
    assert {k for k, v in marks.items() if v == "sourced"} == {"form.stern", "form.head"}
    assert marks["form.stern.lights_m"] == "stand-in"


def test_her_side_is_chapmans_and_her_rail_ends_lie_by_his_overhang(doc, module):
    """Her waist rail Chapman's, 5.3-5.5 ft above the water (Bil §2.4); the taffrail and the stem
    head Chapman's rail length apart (75.6 ft, +-2%), the overhang two-thirds abaft the post and a
    third before the stem (her step 1, measured on IA leaf 0141 by two methods)."""
    rail = doc["hull"]["profile"]["rail_m"]
    xs = [p[0] for p in rail]
    waist = min(z for _x, z in rail)
    assert 5.3 * FT - 0.01 <= waist <= 5.5 * FT + 0.01
    assert xs[-1] - xs[0] == pytest.approx(RAIL_LENGTH_M, rel=0.02)
    half = 0.5 * 70.6 * FT
    aft, fore = -half - xs[0], xs[-1] - half
    assert aft / (aft + fore) == pytest.approx(2.0 / 3.0, abs=0.02)
    assert (module["taffrail"], module["stem_head"]) == (xs[0], xs[-1])
    # Gwyn's quarterdeck rail 0.84 m above the waist rail at its break and 1.65 m at the taffrail,
    # the bow's 1.00 m at the stem head (Bil-D §3.2, measured; +-10 px, about 0.3 m)
    assert rail[0][1] - WAIST_M == pytest.approx(1.65, abs=0.02)
    assert rail[2][1] - WAIST_M == pytest.approx(0.84, abs=0.02)
    assert rail[-1][1] - WAIST_M == pytest.approx(1.00, abs=0.02)


def test_her_body_under_the_water_is_the_brig_colliers_scaled(doc, module):
    """Bil-D §3.1, §3.4: Steel 1805's brig collier of 170 27/94 tons (Tables p. 26, read), lengths
    by her waterline over its 76 ft 11 in between the perpendiculars (0.918), the sections by her
    beam over its 22 ft 11 in extreme breadth (0.847). Its dead flat's main half-breadth with the
    plank, 11 ft 5 1/2 in, is her half-beam; its drawn depth, 10 ft 9 in scaled, is recorded beside
    her draught (2.77 m against 3.51), never moved; her drawn displacement within the principles'
    15% of her filed one (Build-Ships.md §5.0 principle 8)."""
    assert module["length_ratio"] == pytest.approx(70.6 / (76.0 + 11.0 / 12.0))
    assert module["beam_ratio"] == pytest.approx(19.4 / (22.0 + 11.0 / 12.0))
    assert module["depth"] == pytest.approx(2.77, abs=0.005)
    profile = doc["hull"]["profile"]
    widest = max(hb for _x, hb, _r in profile["breadth_m"])
    assert widest == pytest.approx(19.4 * FT / 2.0, abs=0.01)
    assert profile["keel_m"][0][1] == pytest.approx(-module["depth"])
    spec = load_spec(HER).hull
    assert drawn.drawn_displacement_kg(spec) == pytest.approx(spec.displacement_kg, rel=0.15)
    # the collier's stations hers: sixteen timbers, x by the length ratio
    assert len(profile["breadth_m"]) == 16
    assert len({p[0] for p in profile["sections_m"]}) == 16


def test_steels_collier_as_read_holds_its_own_folio(module):
    """The transcription's arithmetic checks (Bil-D §3.6 task 1; docs/dev/TuningNotes.md): the
    table's dead flat and its foremost and after timbers are Folio I's E, F and G to the inch; its
    after body's room is 2 ft from timber 4 to 22; dead flat's main half-breadth doubled is Folio
    I's moulded breadth, 22 ft 6 in; her length between the perpendiculars 76 ft 11 in, the room
    counted from dead flat as it holds on Steel's 36 and cutter."""
    fore, aft, folio = module["fore"], module["aft"], module["folio"]

    def ft(v):
        feet, inches = v.replace("½", ".5").split()
        return float(feet) + float(inches) / 12.0

    dead_flat = "⊕"
    assert fore[dead_flat]["station"] == pytest.approx(ft(folio["E"]))
    assert fore["N"]["station"] == pytest.approx(ft(folio["F"]))
    assert aft["22"]["station"] == pytest.approx(ft(folio["G"]))
    stations = [aft[t]["station"] for t in ("4", "8", "12", "14", "16", "18", "20", "22")]
    numbers = [4, 8, 12, 14, 16, 18, 20, 22]
    pairs = list(zip(stations, numbers, strict=True))
    for (s0, n0), (s1, n1) in zip(pairs, pairs[1:], strict=False):
        assert s0 - s1 == pytest.approx(2.0 * (n1 - n0))
    assert 2.0 * fore[dead_flat]["main_half"] == pytest.approx(ft(folio["K"]))
    assert module["length_ft"] == pytest.approx(30.0 + 8.0 + 38.0 + 11.0 / 12.0)
    # each row fair: the upper height of breadth rises toward both ends from dead flat
    for body in (fore, aft):
        rows = sorted(body.values(), key=lambda r: r["station"])
        ups = [r["upper_breadth"] for r in rows]
        assert ups == sorted(ups, reverse=True)


def test_her_stern_is_round_with_three_lights_and_her_head_a_figure(doc):
    """Gwyn's separate stern view: rounded, three oval lights in one band (Bil §2.3, read); a
    figure with head rails (read). A round stern takes no transom (Build-Ships.md §5.1)."""
    form = doc["hull"]["profile"]["form"]
    assert form["stern"]["type"] == "round"
    assert "transom_hb_m" not in form["stern"]
    assert form["stern"]["lights_m"] == [[1.75, 2.75, 3, 1.1]]
    assert form["head"] == "figure"
    head = doc["hull"]["profile"]["head_m"]
    stem_head = doc["hull"]["profile"]["stem_m"][-1][0]
    # the figure 1.48 m beyond the stem head (Gwyn, measured); Chapman's overall 83 ft the check
    assert head[-1][0] - stem_head == pytest.approx(1.48, abs=0.01)


def test_her_ports_are_cut_down_from_the_rail_and_their_half_breadths_are_the_colliers(doc):
    """Bil-D §3.2, §5.2: the armed fit's two ports a side in the waist at x 1.0 and 4.0, sills the
    deck + 16 in, 0.50 by 0.30 m, their tops under the rail (the owner's "cutouts in the gunwale");
    each half-breadth the collier's at the sill, within 0.05 m of the drawn side (none measured at
    a port: each gap reported)."""
    profile = doc["hull"]["profile"]
    ports = profile["ports_m"]["upper"]
    assert [p[0] for p in ports] == [1.0, 4.0]
    width, depth = profile["port_size_m"]["upper"]
    assert (width, depth) == (0.5, 0.3)
    from freesail.ship.profile import interp

    for x, sill, _hb in ports:
        assert sill == pytest.approx(interp(profile["decks_m"]["upper"], x) + 16 * 0.0254, abs=0.01)
        assert sill + depth < interp(profile["rail_m"], x)
    spec = load_spec(HER).hull
    for x, sill, hb in ports:
        assert drawn.half_breadth_at(spec, x, sill) == pytest.approx(hb, abs=drawn.PORT_GAP_M)


# ---------------------------------------------------------------------------
# Her masts and yards (Bil-D §4.1)
# ---------------------------------------------------------------------------

# Gwyn's heights above the waist rail as shares of the rail length (Bil §2.3; Bil-D §4.1, measured
# and re-measured at her step 1 by two methods, within +-10 px of each other)
GWYN_SHARES = {
    "fore.yard": 0.276,
    "fore.topsail.yard": 0.580,
    "fore.topgallant.yard": 0.750,
    "main.crossjack.yard": 0.293,
    "main.topsail.yard": 0.633,
    "main.topgallant.yard": 0.834,
}
# Chapman's yards at twice their drawn length, ft (Bil §2.4, measured, +-1.5%); the dry yard by
# Chapman's rule for brigs, the fore yard's (Chapman 1781 p. 102, read)
CHAPMAN_YARDS_FT = {
    "fore.yard": 40.8,
    "fore.topsail.yard": 30.0,
    "fore.topgallant.yard": 20.1,
    "main.crossjack.yard": 40.8,
    "main.topsail.yard": 30.7,
    "main.topgallant.yard": 20.1,
}


def gwyn_share(z_water):
    return (z_water - WAIST_M) / RAIL_LENGTH_M


def test_her_masts_stand_at_chapmans_stations(spec):
    """Bil §2.4 (measured): the main 0.41 of the waterline forward of the sternpost at the rail,
    raking aft about 2.8 degrees; the fore 0.148 abaft the stem, plumb; 9.51 m apart at the rail
    (Chapman 31.1 ft, measured)."""
    ship, spars, _sails, _lines = spec
    lwl = ship.hull.length_waterline_m
    main, fore = spars["main.mast"], spars["fore.mast"]
    rake = math.tan(math.radians(main.rake_deg))
    main_at_rail = main.x_m - rake * (WAIST_M - DATUM_M)
    assert main_at_rail == pytest.approx(-lwl / 2.0 + 0.41 * lwl, abs=0.01)
    assert fore.x_m == pytest.approx(lwl / 2.0 - 0.148 * lwl, abs=0.01)
    assert main.rake_deg == pytest.approx(2.8)
    assert fore.rake_deg is None
    assert fore.x_m - main_at_rail == pytest.approx(31.1 * FT, abs=0.1)
    # her main laid aback to heave to, and no other (D4 (a); Ext §5.7)
    assert [s.id for s in ship.spars if s.heave_to_aback] == ["main.mast"]


def test_her_rig_holds_gwyns_heights_and_chapmans_yards(spec):
    """Bil-D §4.1 and truth 7-197's rig clause: the main top 0.35, the main truck 0.95 and the fore
    truck 0.85 of the rail length above the waist rail (Gwyn, Bil §2.3: +-0.02, +-0.03); each yard
    at Gwyn's height (+-2% of the share) and Chapman's length (+-0.2 m); a dry yard on the main
    and no royal (D40 (a))."""
    _ship, spars, sails, _lines = spec
    for yard, share in GWYN_SHARES.items():
        assert gwyn_share(above_water(spars, yard)) == pytest.approx(share, abs=0.02 * share), yard
        assert spars[yard].length_m == pytest.approx(CHAPMAN_YARDS_FT[yard] * FT, abs=0.2)
    main_truck = above_water(spars, "main.mast") + spars["main.topmast"].height_m
    main_truck += spars["main.topgallant_mast"].height_m
    fore_truck = above_water(spars, "fore.mast") + spars["fore.topmast"].height_m
    fore_truck += spars["fore.topgallant_mast"].height_m
    assert gwyn_share(main_truck) == pytest.approx(0.95, abs=0.03)
    assert gwyn_share(fore_truck) == pytest.approx(0.85, abs=0.03)
    assert not [s for s in spars if "royal" in s]
    assert "main.yard" not in spars and "main.crossjack.yard" in spars
    assert not [s for s in sails.values() if s.roles.get("yard") == "main.crossjack.yard"]
    # the brig's brace limits, level for level (brig.yaml; Bil-D §4.1, judgement)
    assert {y: spars[y].brace_limit_deg for y in GWYN_SHARES} == {
        "fore.yard": 60,
        "fore.topsail.yard": 62,
        "fore.topgallant.yard": 64,
        "main.crossjack.yard": 62,
        "main.topsail.yard": 64,
        "main.topgallant.yard": 66,
    }


# ---------------------------------------------------------------------------
# Her settee (Bil-D §4.4; Ext §5.1; D5 (a))
# ---------------------------------------------------------------------------


def settee_corners(sails):
    return [(x, z + DATUM_M) for x, z in sails["main.settee"].corners_m]


def test_her_settee_holds_d5a_and_gwyn(spec):
    """Truth 7-197's settee clause (Bil-D §14): luff over leech 0.16 +-0.02 and leech and foot over
    head 0.72 +-0.02 (D5 (a), Gwyn's ratios); the head at 44 +-1 degrees and 0.68 of the rail
    length (Gwyn's 534 px of 785); slung a third of the way along the head from the throat on the
    main mast's raked line within 0.1 m (Ext §5.1); the peak inside the taffrail by 0.07-0.11 of
    the rail length (Gwyn 0.09 +-0.02, Bil §2.3); `settee` and `dipping` true, one unsided sheet;
    its yard cut to its head (her design's §4.4, B5.4's finding: the drawing draws a settee's yard
    as its head)."""
    ship, spars, sails, lines = spec
    sail = sails["main.settee"]
    assert sail.settee and sail.dipping and sail.cls == "lug"
    assert sail.roles == {"yard": "main.lug_yard", "mast": "main.mast"}
    tack, throat, peak, clew = settee_corners(sails)
    head, leech = math.dist(throat, peak), math.dist(peak, clew)
    foot, luff = math.dist(tack, clew), math.dist(tack, throat)
    assert luff / leech == pytest.approx(0.16, abs=0.02)
    assert leech / head == pytest.approx(0.72, abs=0.02)
    assert foot / head == pytest.approx(0.72, abs=0.02)
    rise = math.degrees(math.atan2(peak[1] - throat[1], throat[0] - peak[0]))
    assert rise == pytest.approx(44.0, abs=1.0)
    assert head / RAIL_LENGTH_M == pytest.approx(534.0 / 785.0, abs=0.005)
    yard = spars["main.lug_yard"]
    assert yard.length_m == pytest.approx(head, abs=0.02)
    sx = throat[0] + (peak[0] - throat[0]) / 3.0
    sz = throat[1] + (peak[1] - throat[1]) / 3.0
    main = spars["main.mast"]
    on_line = main.x_m - math.tan(math.radians(main.rake_deg)) * (sz - DATUM_M)
    assert abs(sx - on_line) <= 0.1
    assert yard.height_m + DATUM_M == pytest.approx(sz, abs=0.02)
    taffrail = ship.hull.profile.rail_m[0][0]
    assert 0.07 <= (peak[0] - taffrail) / RAIL_LENGTH_M <= 0.11
    assert clew[0] > taffrail
    # the tack 0.30 m above the waist rail, under the throat (Gwyn, measured)
    assert tack[1] - WAIST_M == pytest.approx(0.30, abs=0.01)
    assert tack[0] == pytest.approx(throat[0])
    sheets = [ln for ln in lines if ln.cls == "sheet" and ln.of == "main.settee"]
    assert len(sheets) == 1 and sheets[0].side is None
    # about 73 m2 by its corners (Bil-D §4.4), against Chapman's about 92 (recorded)
    assert sail.area_m2 == 73


def test_her_settee_lines_are_lescalliers(spec):
    """Lescallier p. 390 (Bil §1.2; Ext §5.1): the jeers a halyard and the derrick a lift of the
    yard, the vangs and the ourses a side, the tacks a side, one sheet, two clewlines and a
    buntline; the yard never braced (Ext E3)."""
    _ship, spars, _sails, lines = spec

    def of(owner):
        return sorted((ln.cls, ln.side or "") for ln in lines if ln.of == owner)

    sides = ("starboard", "larboard")
    assert of("main.lug_yard") == sorted(
        [("halyard", ""), ("lift", "")] + [(c, s) for c in ("vang", "guy") for s in sides]
    )
    assert of("main.settee") == sorted(
        [("sheet", ""), ("buntline", "")] + [(c, s) for c in ("tack", "clewline") for s in sides]
    )
    assert spars["main.lug_yard"].brace_limit_deg is None


def test_settee_cut_gives_her_figures_and_its_checks_raise_in_words(settee):
    """`settee.py`'s checks (Ext §9.3; Bil-D §4.4), each a ValueError with a sentence: the sling
    off the mast's line; the peak or the clew abaft the taffrail; two sheets, or a sided one; a
    corner off D5 (a)'s ratios. Her own cut passes them."""

    def mast(z):
        return -1.9 - math.tan(math.radians(2.8)) * (z - DATUM_M)

    cut = settee.cut(head_m=15.68, yard_deg=44.0, tack_z=1.95, mast_x_at=mast)
    lines = settee.lines("main.lug_yard", "main.settee")
    settee.check(cut, lines, mast_x_at=mast, taffrail_x=-11.78, sail_id="main.settee")
    assert cut["yard_m"] == cut["head"]
    assert cut["area"] == pytest.approx(73.4, abs=0.1)
    with pytest.raises(ValueError, match="off the mast's raked line"):
        settee.check(
            cut, lines, mast_x_at=lambda z: mast(z) + 0.2, taffrail_x=-11.78, sail_id="main.settee"
        )
    with pytest.raises(ValueError, match="abaft the taffrail"):
        settee.check(cut, lines, mast_x_at=mast, taffrail_x=-9.0, sail_id="main.settee")
    sided = [ln for ln in lines if ln[1] != "sheet"]
    sided += [("main.settee.sheet.starboard", "sheet", "main.settee", "starboard")]
    with pytest.raises(ValueError, match="one unsided sheet"):
        settee.check(cut, sided, mast_x_at=mast, taffrail_x=-11.78, sail_id="main.settee")
    two = [*lines, ("main.settee.sheet2", "sheet", "main.settee", None)]
    with pytest.raises(ValueError, match="one unsided sheet"):
        settee.check(cut, two, mast_x_at=mast, taffrail_x=-11.78, sail_id="main.settee")
    tack, throat, peak, clew = cut["corners"]
    short = {**cut, "corners": [(tack[0], tack[1] + 0.5), throat, peak, clew]}
    with pytest.raises(ValueError, match="D5 \\(a\\)"):
        settee.check(short, lines, mast_x_at=mast, taffrail_x=-11.78, sail_id="main.settee")
    with pytest.raises(ValueError, match="more than nothing"):
        settee.cut(head_m=0.0, yard_deg=44.0, tack_z=1.95, mast_x_at=mast)


# ---------------------------------------------------------------------------
# Her head, her spritsail and her staysails (Bil-D §4.2, §4.3, §4.5)
# ---------------------------------------------------------------------------


def test_her_spritsail_and_main_topmast_staysail_are_bent_and_out_of_plain_sail(her):
    """Bil-D §4.3, §4.5: the spritsail bent, in "spritsails" and "all sail" and never in "plain
    sail", "courses", "headsails", "jibs" or the sail room's "occasional sails"; the main topmast
    staysail bent, out of plain sail, the one staysail between the masts and the one lying-to
    staysail; the storm staysails in the sail room."""
    groups = her.spec.groups
    for sid in ("spritsail", "main.topmast_staysail"):
        assert her.sails[sid].state is not SailState.UNBENT, sid
        assert sid in groups["all sail"] and sid not in groups["plain sail"], sid
        assert sid not in groups.get("occasional sails", []), sid
    assert groups["spritsails"] == ["spritsail"]
    for name in ("courses", "headsails", "jibs"):
        assert "spritsail" not in groups[name]
    assert groups["lying-to staysails"] == ["main.topmast_staysail"]
    assert groups["staysails between the masts"] == ["main.topmast_staysail"]
    assert "main.staysail" not in her.sails
    for sid in groups["storm canvas"]:
        assert her.sails[sid].state is SailState.UNBENT, sid


def test_her_groups_name_her_settee_her_mainsail_and_a_course(her):
    """Ext §5.1, E15: the settee in "courses", "plain sail" and "all sail", never "gaff sails";
    named her mainsail; her plain sail Gwyn's set (Bil §2.3), the fore's three square sails, the
    main topsail and topgallant, the settee, the jib and the fore topmast staysail."""
    groups, aliases = her.spec.groups, her.spec.aliases
    assert groups["courses"] == ["fore.course", "main.settee"]
    assert "main.settee" in groups["plain sail"] and "main.settee" in groups["all sail"]
    assert "gaff sails" not in groups
    for word in ("mainsail", "main sail", "settee"):
        assert aliases[word] == "main.settee"
    assert aliases["main yard"] == "main.lug_yard"
    assert aliases["dry yard"] == aliases["crossjack"] == "main.crossjack.yard"
    assert sorted(groups["plain sail"]) == sorted(
        [
            "fore.course",
            "fore.topsail",
            "fore.topgallant",
            "main.topsail",
            "main.topgallant",
            "main.settee",
            "fore.topmast_staysail",
            "jib",
        ]
    )
    assert groups["after yards"] == [
        "main.crossjack.yard",
        "main.topsail.yard",
        "main.topgallant.yard",
    ]
    for name, members in groups.items():
        if "yard" in name:
            assert "main.lug_yard" not in members and "spritsail.yard" not in members, name


def test_the_main_topmast_staysails_foot_clears_the_settees_yard(spec):
    """Bil-D §1.4's check: the main topmast staysail's foot stands a foot (0.30 m, judgement) above
    the settee's yard where they cross, its leech cut from Steel's rule for it."""
    _ship, spars, sails, _lines = spec
    tack, _nock, _peak, clew = [
        (x, z + DATUM_M) for x, z in sails["main.topmast_staysail"].corners_m
    ]
    _t, throat, s_peak, _c = settee_corners(sails)
    yard_z = throat[1] + (clew[0] - throat[0]) * (s_peak[1] - throat[1]) / (s_peak[0] - throat[0])
    assert clew[1] - yard_z == pytest.approx(0.30, abs=0.02)
    assert tack[0] == pytest.approx(spars["fore.mast"].x_m)


def test_her_spritsails_foot_clears_the_water_and_its_yard_is_the_fore_topsail_yards(spec):
    """Bil-D §4.3: the spritsail yard the fore topsail yard's length (Steel 1794 vol. I p. 40);
    its sail's foot above the water at no heel (`spritsail_yards.cut` checks it), a metre or more
    by its cut (judgement)."""
    _ship, spars, sails, _lines = spec
    yard = spars["spritsail.yard"]
    assert yard.length_m == spars["fore.topsail.yard"].length_m
    depth = 2.0 * (yard.height_m + DATUM_M - sails["spritsail"].centre_height_m)
    assert yard.height_m + DATUM_M - depth >= 1.0


# ---------------------------------------------------------------------------
# The generator, her notes, her class's words
# ---------------------------------------------------------------------------

REPORT_PROBE = """
import sys
sys.path.insert(0, "tools")
import gen_ships
sys.modules["gen_ships"] = gen_ships
from ships import bilander as her
her.build(sys.argv[1])
"""


def test_the_generator_writes_her_file_as_committed_and_reports_its_checks(tmp_path):
    """`build()` raises the checks of Bil-D §1.4 before her file is written and prints the
    generator's report: the hull as drawn (drawn displacement 215 t against the filed 229, -6%;
    drawn 2.65 m deep at the greatest section against her draught of 3.51 m), each port triple's
    gap to the drawn side (+0.01 and +0.02 m, none measured at its port), the collier's figures at
    her scale beside hers, the fore course's foot clear of the rail, the main topmast staysail cut
    to clear the settee's yard, the settee's corners and the spritsail's foot; and since her step
    3, the quarter bill's arithmetic on the armed fit and Steel's Navy anchors on her tonnage beside
    the house's rule; since her step 4, her `clr_x_m` as tuned beside its start (+2.25 at her step
    4, +2.0 since her review); since her review, her round stern as drawn beside Gwyn's stern view,
    at the lights' middle height: since her counter is drawn to its filed half-breadths (the lead's
    ruling (11) of 2026-11-09, `form.stern.counter_hb_m`), 0.99 m off the middle line 0.4 m inside
    the taffrail and 1.84 m 0.8 m inside, against Gwyn's 1.55 m at the taffrail and 2.02 m at the
    wale (old: 0.35 and 0.91 m, the round stern closed straight to the middle line, recorded and
    not drawn). Her file comes out as it stands."""
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
    drawn_ = "bilander: the hull as drawn (freesail/ship/form.py):"
    assert f"{drawn_} drawn displacement 215 t against the filed 229 t (-6%)." in said
    assert (
        "the upper deck's ports: the side at each sill, aft to forward, off the half-breadth"
        in (said)
    )
    assert "bilander: the collier drawn 2.77 m deep to its keel's underside" in said
    assert (
        "bilander: the fore course's foot 2.79 m above the water, 0.89 m clear of the rail" in said
    )
    assert "cut so that its foot stands 0.30 m above the settee's yard" in said
    assert "bilander: the settee 73.4 m2" in said
    assert "bilander: plain sail 372 m2." in said
    assert "118.0 tons on her waterline and 128.0 on her length taffrail to stem head" in said
    assert "the collier's stem head at her scale 2.53 m above her water" in said
    assert (
        "bilander: the quarter bill on 'armed merchant': of her 6 hands off the quarterdeck the "
        "bill tells off 2 trimmers and 1 at the helm first, and her guns want 10" in said
    )
    assert "give 7.7 cwt on her 128 tons, against the house's 6.4." in said
    assert (
        "bilander: clr_x_m +2.00 as tuned for her helm, against her start, the brig's 0.5 m as a "
        "share of her waterline, +0.40." in said
    )
    assert (
        "bilander: her round stern drawn to its counter's half-breadths (counter_hb_m): at the "
        "lights' middle height, 2.25 m, 0.99 m off the middle line 0.4 m inside the taffrail and "
        "1.84 m 0.8 m inside, against Gwyn's stern view's 1.55 m at the taffrail and 2.02 m at the "
        "wale." in said
    )


def test_her_notes_carry_no_figure_a_rule_computes():
    """The lead's notes of 2026-10-29, item 2: no rating's figure, no bowline's size, in her
    notes; what each rule read stays."""
    said = [
        line.strip()
        for line in (ROOT / HER).read_text(encoding="utf-8").splitlines()
        if line.strip().startswith("#")
    ]
    assert not [line for line in said if re.search(r" -> [0-9.]+ kN", line)]
    assert not [line for line in said if re.search(r"than the sheet, [0-9.]+ in", line)]
    assert [line for line in said if "Rating: fore.course" in line]


def test_her_class_is_served_in_the_periods_words():
    """Her era note's first clause is the class her readings serve (`ship_class_words`), in-world
    (package 85's rule): her type and her rig, no build reference."""
    spec = load_spec(HER)
    said = ship_class_words(spec, spec.name)
    assert said == "a British coasting bilander under a settee main"
    for words in ("tools/", "PAG", "Chapman", "Bil-D", "Hopewell"):
        assert words not in said


# ---------------------------------------------------------------------------
# Her file loads, rates and polars (her road's step 2); rule 1 (Bil-D §9; truth 7-197's clause)
# ---------------------------------------------------------------------------


def test_her_file_loads_rates_and_polars(her):
    """Her road's step 2 (Bil-D §13): her file loads with no warning, every spar and line rated,
    and draws a polar."""
    spec = load_spec(HER)
    assert spec.warnings == []
    assert all(ln.rating_kn > 0.0 for ln in her.lines.values())
    assert all(sp.rating_kn > 0.0 for sp in spec.spars)
    polar = polar_of(HER)
    assert all(v >= 0.0 for row in polar.speeds_kn for v in row)


def test_her_polar_agrees_with_her_sailed_beam_reach_and_her_helm_is_as_tuned():
    """`polar_of` (tests/test_ships.py:74-93's form, her own figures): her beam reaches in 8, 15
    and 25 kn are her measured 3.76, 6.62 and 9.31 kn (+-0.5), and in 15 kn within half a knot of
    the one she sails under plain sail with the yards trimmed (the known truths' `settle`, at 90
    degrees: 6.52 kn, heeling 6.9 degrees; 6.51 at her step 3, 6.49 at her step 2 before she had
    a company). Her eight set plain sail in it, all hands called: the watch of three alone takes
    the sails in turn, and the harness's 400 s (`under_plain_sail`) sets her courses and fore
    topsail only, so she is given 1,800 s, plain sail being set by about 1,700 s (measured at her
    step 3; recorded, not tuned: Bil-D §16 risk 7). She is slower than the brig (7.83 kn on the
    polar in 15 kn), a deep-laden hull under Gwyn's short rig, 372 m2 of plain sail on 229 t
    against the brig's 766 on 413 (Bil-D §9: recorded, not tuned up; no source gives a bilander's
    speed).

    **Her helm as tuned** (Bil-D §9's second knob, `clr_x_m`; her step 4, the house's way, weather
    helm positive): +0.40 (the brig's 0.5 m as a share of her waterline) gave 4.06 degrees of lee
    helm abeam and 12.24 at 60 degrees off the wind; +2.0, as built since her review (2026-11-08),
    gives 1.09 of lee helm abeam (4.00 at 60 degrees, 2.05 at 67.5), the most weather helm, by
    quarter metres, her heave-to allows in 8 to 25 kn (below; at +3.0, balanced close-hauled, she
    comes head to wind hove to and makes sternway). Her step 4 took +2.25 (0.69 abeam, 2.86 at 60,
    1.32 at 67.5) on 10 to 25 kn, where hove to in 8 kn she was forced round through the wind (her
    review). Truth 6's form holds: the headsails taken in, her helm goes to weather (+0.36; +0.74
    at +2.25); the settee taken in, to lee (-3.28; -2.83 at +2.25): her headsails give lee helm and
    her after sail weather helm. Sailed abeam, 6.52 kn at both figures. Since her boy is a landsman
    (the lead's ruling (8) of 2026-11-09), sailed in this harness she makes 6.20 kn abeam, within
    half a knot of her polar's 6.62, and her helm under plain sail at its end is 0.02 of lee helm
    (old: 1.09), the headsails taken in +0.44 (old +0.36), the settee taken in -3.29 (old -3.28):
    her company's work at the trims changed, measured and not tuned, her polar the same."""
    from tests.test_known_truths import knots, make, run, settle, tack_for

    p = polar_of(HER)
    measured = {8.0: 3.76, 15.0: 6.62, 25.0: 9.31}
    for wind, kn in measured.items():
        assert abs(p.speed_kn(90.0, wind) - kn) <= 0.5, (wind, p.speed_kn(90.0, wind))
    assert p.speed_kn(90.0, 8.0) < p.speed_kn(90.0, 15.0) < p.speed_kn(90.0, 25.0)
    assert p.speed_kn(90.0, 15.0) < polar_of(BRIG).speed_kn(90.0, 15.0)
    assert load_spec(HER).hull.clr_x_m == 2.0
    w = make(HER, 270.0)
    orders = ["call all hands", "set plain sail", f"brace sharp up on the {tack_for(270.0)} tack"]
    settle(w, orders, sail_wait=1800)
    plain = ["fore.course", "fore.topsail", "fore.topgallant", "main.topsail", "main.topgallant"]
    plain += ["main.settee", "fore.topmast_staysail", "jib"]
    assert all(w.ship.sails[s].state is SailState.SET for s in plain)
    sailed = knots(w)
    assert abs(p.speed_kn(90.0, 15.0) - sailed) <= 0.5, sailed

    def helm():
        return math.degrees(w.ship.dyn.weather_helm)

    plain_helm = helm()
    assert plain_helm == pytest.approx(-0.02, abs=0.3)
    w.submit("take in the headsails")
    run(w, 900, trim_every=120)
    no_headsails = helm()
    w.submit("set the headsails")
    w.submit("take in the mainsail")
    run(w, 900, trim_every=120)
    no_settee = helm()
    assert w.ship.sails["main.settee"].state is SailState.IN_THE_GEAR
    assert no_headsails > plain_helm > no_settee, (no_headsails, plain_helm, no_settee)
    assert no_headsails == pytest.approx(0.44, abs=0.3)
    assert no_settee == pytest.approx(-3.29, abs=0.3)


def test_her_polar_as_measured_and_tuned_beside_the_brig_sloops_and_the_merchant_brigs(tmp_path):
    """Her road's step 4 (Bil-D §9): her polar on her file (`polar_of`, plain sail, the same on
    every machine), recorded beside the brig-sloop's and the merchant brig's, which are one polar
    to the hundredth (the merchant brig sails the brig-sloop's hull, spars and sails: her file's
    head note). Measured (2026-11-08): closest 50; beating at 60 in 8, 15 and 25 kn; her best 3.79,
    6.66 and 9.38 kn at 100 degrees against their 4.57, 7.92 and 10.97; in 15 kn at 60 degrees 3.62
    kn against 4.26, abeam 6.62 against 7.83; her way to windward in 15 kn 1.81 kn at 60 against
    1.75 at 70, the beat's margin 0.06 kn (her design's probe 0.05-0.12 by the headsails' cut). No
    speed is sourced for her (Research-Bilander-2026-10.md §4): recorded, the bands the measure's,
    judgement. The knobs in §9's order, each beside its start and its bound: the headsails' cut
    kept (43 m2, Gwyn's heads on her own stays by `stay_sail_cut`'s rule; no source cuts them
    otherwise); `clr_x_m` tuned for her helm, which the polar does not read (her sailed beam reach,
    above, and her heave-to, below); and `hull_speed_kn` kept at its start, 10.3, rule 1 holding
    across its whole band of 9.8 to 10.8 (the beat's margin 0.069, 0.062 and 0.064 kn), so nothing
    asks a move."""
    from freesail.world.ships import POLAR_WINDS_KN

    brig, merchant, p = polar_of(BRIG), polar_of("data/ships/merchant-brig.yaml"), polar_of(HER)
    assert merchant.speeds_kn == brig.speeds_kn and merchant.closest_deg == brig.closest_deg
    assert (p.closest_deg, [p.beat_deg(w) for w in POLAR_WINDS_KN]) == (50.0, [60.0, 60.0, 60.0])
    for wind, best, brig_best in ((8.0, 3.79, 4.57), (15.0, 6.66, 7.92), (25.0, 9.38, 10.97)):
        assert max(p.angles_deg, key=lambda a, w=wind: p.speed_kn(a, w)) == 100
        assert p.speed_kn(100.0, wind) == pytest.approx(best, abs=0.05), wind
        assert brig.speed_kn(100.0, wind) == pytest.approx(brig_best, abs=0.01), wind
    assert p.speed_kn(60.0, 15.0) == pytest.approx(3.62, abs=0.05)
    assert brig.speed_kn(60.0, 15.0) == pytest.approx(4.26, abs=0.01)

    def made_good(polar, angle, wind=15.0):
        return polar.speed_kn(angle, wind) * math.cos(math.radians(angle))

    assert made_good(p, 60.0) - made_good(p, 70.0) == pytest.approx(0.06, abs=0.02)
    assert load_spec(HER).hull.hull_speed_kn == 10.3
    doc = yaml.safe_load((ROOT / HER).read_text(encoding="utf-8"))
    for knots in (9.8, 10.8):  # her design's band for the third knob (judgement about D24 (a))
        doc["hull"]["hull_speed_kn"] = knots
        path = tmp_path / f"hull-speed-{knots}" / "bilander.yaml"
        path.parent.mkdir()
        path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
        q = polar_of(str(path))
        assert q.closest_deg <= 50.0 and q.beat_deg(15.0) <= 60.0, knots
        assert made_good(q, 60.0) > made_good(q, 70.0), knots


def test_truth_7_197_her_particulars_hold_their_sources_and_she_lies_as_close_as_a_brig(module):
    """Truth 7-197 (B4; Bil-D §14; Build-Ships.md §15), whole, drafted here for Phase 5: her
    particulars hold their sources, and by the wind she lies as close as a brig. Measured on her
    file at her step 4 (the owner's machine, 2026-11-08), each band its source's:
    - her hull: LWL 21.52 m against Chapman's 70.6 ft, +-1.5-2 ft (21.5 +- 0.5); beam 5.91 m
      against Chapman's 19.4 ft, +-1.5% (+- 0.1); draught 3.51 m against Lloyd's 11 and 12 ft
      (+- 0.16); burthen by the old measure 118 and 128 tons, D6 (a)'s "about 130" (118-130);
      her waist rail 1.65 m above the water against Chapman's 5.3-5.5 ft (+- 0.05);
    - her settee to D5 (a): luff over leech 0.16, leech and foot over head 0.72 (+- 0.02, Gwyn's
      ratios); the head at 44 degrees (+- 1) and 0.68 of the rail length (Gwyn's 534 px of 785),
      its yard cut to it (B5.4's finding: the drawing draws a settee's yard as its head; her
      design's §14 had the yard 0.72 of the rail length, Gwyn's 564 px, before her step 2 cut it,
      old beside new: 16.59 to 15.68 m); slung a third along throat to peak on the main mast's
      raked line (within 0.1 m); the peak 0.088 of the rail length inside the taffrail (0.07-0.11,
      Gwyn's 0.09 +- 0.02); `settee` and `dipping` true; one unsided sheet;
    - her rig to Gwyn's shares above the waist rail: the main top 0.35 (+- 0.02), the main truck
      0.95 and the fore truck 0.85 (+- 0.03); Chapman's yards: the fore yard 12.44 m, the topsail
      yards 9.14 and 9.36 m (+- 0.2); a dry yard on the main and no royal (D40 (a));
    - her company of eight, two in the main top (D43; Ext §5.1); `heave_to_aback` on the main mast
      and no other (D4 (a));
    - her fits: unarmed by default (the brief, item 3), the armed merchant four long 3-pounders and
      four half-pounder swivels (Lloyd's Elizabeth, "4-3 P."; D41 (a));
    - her description at rank 1, "merchant" in what she is made out to be (D16 (a));
    - **rule 1** (D46 rule 1; Ext §5.9; Steel 1794 vol. I p. 237, Lescallier p. 380: lateen craft
      lie a point nearer the wind than square-riggers, five points against six; with a square fore
      she does not gain the whole point, Research-Bilander-2026-10.md §4, judgement): her
      `closest_deg` and `beat_deg(15)` no wider than the brig's 50 and 60 degrees at this head.
      Measured: 50 and 60, the beat by 0.06 kn of way to windward over 70 degrees. To be measured
      again on D44 (c)'s settee row had rule 5 taken it (Bil-D §14): on her file it did not (her
      step 5, `test_rule_5_on_her_file_holds_held_aback_near_its_trim_and_never_in_stays`), so the
      clause stands as measured here."""
    ship = load_ship(HER)
    spec = load_spec(HER)
    hull = spec.hull
    assert abs(hull.length_waterline_m - 21.5) <= 0.5 and abs(hull.beam_m - 5.91) <= 0.1
    assert abs(hull.draught_m - 3.51) <= 0.16
    b = 19.4
    for length in (70.6, 75.6):  # her waterline and her taffrail to stem head, ft
        assert 118.0 - 0.5 <= (length - 0.6 * b) * b * b / 2.0 / 94.0 <= 130.0
    waist = min(z for _x, z in hull.profile.rail_m)
    assert abs(waist - 1.65) <= 0.05
    spars, sails = {x.id: x for x in spec.spars}, {x.id: x for x in spec.sails}
    settee = sails["main.settee"]
    tack, throat, peak, clew = settee_corners(sails)
    head, leech = math.dist(throat, peak), math.dist(peak, clew)
    assert abs(math.dist(tack, throat) / leech - 0.16) <= 0.02
    assert abs(leech / head - 0.72) <= 0.02 and abs(math.dist(tack, clew) / head - 0.72) <= 0.02
    assert abs(math.degrees(math.atan2(peak[1] - throat[1], throat[0] - peak[0])) - 44.0) <= 1.0
    yard = spars["main.lug_yard"]
    assert abs(yard.length_m / RAIL_LENGTH_M - 534.0 / 785.0) <= 0.02
    assert abs(yard.length_m - head) <= 0.02
    sx, sz = throat[0] + (peak[0] - throat[0]) / 3.0, throat[1] + (peak[1] - throat[1]) / 3.0
    main = spars["main.mast"]
    assert abs(sx - (main.x_m - math.tan(math.radians(main.rake_deg)) * (sz - DATUM_M))) <= 0.1
    taffrail = hull.profile.rail_m[0][0]
    assert 0.07 <= (peak[0] - taffrail) / RAIL_LENGTH_M <= 0.11
    assert settee.settee and settee.dipping
    sheets = [ln for ln in spec.lines if ln.cls == "sheet" and ln.of == "main.settee"]
    assert len(sheets) == 1 and sheets[0].side is None
    assert abs(gwyn_share(module["rig"]["main"]["top"]) - 0.35) <= 0.02
    truck = {
        m: above_water(spars, f"{m}.mast")
        + spars[f"{m}.topmast"].height_m
        + spars[f"{m}.topgallant_mast"].height_m
        for m in ("fore", "main")
    }
    assert abs(gwyn_share(truck["main"]) - 0.95) <= 0.03
    assert abs(gwyn_share(truck["fore"]) - 0.85) <= 0.03
    for yid, metres in (
        ("fore.yard", 12.44),
        ("fore.topsail.yard", 9.14),
        ("main.topsail.yard", 9.36),
    ):
        assert abs(spars[yid].length_m - metres) <= 0.2, yid
    assert "main.crossjack.yard" in spars and not [s for s in spars if "royal" in s]
    assert spec.crew.complement == 8 and spec.crew.stations["main_top"] == 2
    assert [s.id for s in ship.spars.values() if s.heave_to_aback] == ["main.mast"]
    arm = spec.armament
    assert arm.default == "unarmed" and arm.fit(None) is None
    assert Counter((g.kind, g.pounder) for g in arm.fits[ARMED].guns) == {
        ("long", 3.0): 4,
        ("swivel", 0.5): 4,
    }
    from freesail.world import captains as C
    from freesail.world import ships as S

    d = S.description("bilander")
    assert C.size_of_file(HER) == 1 and C.size_rank_of(d["what"]) == 1
    assert "merchant" in d["what"]
    brig, p = polar_of(BRIG), polar_of(HER)
    assert (brig.closest_deg, brig.beat_deg(15.0)) == (50.0, 60.0)
    assert p.closest_deg <= brig.closest_deg and p.beat_deg(15.0) <= brig.beat_deg(15.0)


# ---------------------------------------------------------------------------
# Her guns (Bil-D §5; her road's step 3)
# ---------------------------------------------------------------------------

ARMED = "armed merchant"
# Adye 1804 p. 155 (the page image read): the long 3-pounder of 4 ft 6 in, 7 cwt 1 qr; the swivel's
# half hundredweight the house's (judgement)
ADYE_3_CWT = 7.25
CWT_KG = 50.80234544  # the hundredweight of 112 lb


def test_her_fits_are_unarmed_by_default_and_the_armed_merchant_is_elizabeths_guns():
    """Bil-D §5.1-§5.3: unarmed by default (the brief, item 3), so no battery is made; one fit, the
    armed merchant: Elizabeth's four 3-pounders (Lloyd's 1779 and 1782, '4-3 P.'), two a side in
    the waist at her two ports a side, numbered from forward, each on its triple to the centimetre,
    Adye's 7 cwt 1 qr and Falconer's three men; and four half-pounder swivels on the quarterdeck
    rail, two a side, each at the rail's height at its own x (`rail_at`'s rule), one man each
    (judgement). The merchant brig's magazine (20 round and 4 grape a gun, 40 a swivel), no charges
    for exercise; the charges Table No. 29's since SW-1, the long 3-pounder's 1 lb and the
    swivel's 2 oz (the engine's half, 4 oz, before it); one man filling (Falconer 1780,
    QUARTER-GUNNER)."""
    from freesail.ship.profile import ports_of, rail_at

    spec = load_spec(HER)
    arm = spec.armament
    assert arm.default == "unarmed" and list(arm.fits) == [ARMED]
    assert arm.fit(None) is None and load_ship(HER).guns == {}
    fit = arm.fits[ARMED]
    assert Counter((g.kind, g.pounder, g.place, g.deck) for g in fit.guns) == {
        ("long", 3.0, "broadside", "upper"): 4,
        ("swivel", 0.5, "rail", "quarterdeck"): 4,
    }
    profile = spec.hull.profile
    from_forward = sorted(ports_of(profile, "upper"), key=lambda t: -t[0])
    for g in fit.guns:
        if g.kind == "long":
            assert (g.weight_cwt, g.crew) == (ADYE_3_CWT, 3), g.id
            x, sill, _hb = from_forward[g.number - 1]
            assert abs(g.x_m - x) <= 0.01 and abs(g.height_m - sill) <= 0.01, g.id
        else:
            assert (g.weight_cwt, g.crew) == (0.5, 1), g.id
            assert g.height_m == pytest.approx(rail_at(profile, g.x_m), abs=0.005), g.id
    # the swivels at x -5.50 and -9.00 (Bil-D §5.2), on her rail as it rises aft: 2.63 and 3.02 m
    # (her design's 2.66 and 3.05 on its own rail, before her step 1 moved the taffrail aft)
    assert sorted({(g.x_m, g.height_m) for g in fit.guns if g.kind == "swivel"}) == [
        (-9.0, 3.02),
        (-5.5, 2.63),
    ]
    assert [g.id for g in fit.guns if g.side == "starboard"] == [
        "gun.1.starboard",
        "gun.2.starboard",
        "swivel.1.starboard",
        "swivel.2.starboard",
    ]
    assert fit.exercise_charges == 0
    assert fit.cartridges == {("long", 3.0): 26 * 4, ("swivel", 0.5): 44 * 4}
    # package 75, SW-1 (Build-Ships.md §10), old beside new: the swivel's Table No. 29's 2 oz
    # (was {("long", 3.0): 1.0, ("swivel", 0.5): 0.25}); her barrel the same, 126 lb filled
    # where it was 148
    assert fit.charges == {("long", 3.0): 1.0, ("swivel", 0.5): 0.125}
    assert fit.shot == {3.0: {"round": 80, "grape": 16}, 0.5: {"round": 160}}
    assert fit.powder_barrels == 1
    assert spec.crew.quarter_bill.filling == 1


def test_the_builders_checklist_draws_every_gun_of_hers():
    """Build-Ships.md §6's postscript (package 81): every port gun on its deck's triple at its own x
    within 0.01 m (above), `port_size_m` for her one deck with ports, every gun's weight within a
    tenth of the pattern the viewer draws it by (the 3-pounder's own, 4 ft 6 in), and the checker
    clean: her four 3-pounders in their ports, her four swivels on the rail, no port empty, no
    note."""
    sys.path.insert(0, str(ROOT / "tools"))
    import check_viewer_guns

    from freesail.api import viewer_guns

    spec = load_spec(HER)
    assert dict(spec.hull.profile.port_size_m)["upper"] == (0.5, 0.3)
    for g in spec.armament.fits[ARMED].guns:
        assert viewer_guns.figure(g.kind, g.pounder, g.weight_cwt).weight_off <= 0.01, g.id
    rep = check_viewer_guns.check(ROOT / HER)
    assert rep.ok, rep.lines
    assert rep.lines == [
        "bilander.yaml: the contract given",
        "  fit 'armed merchant': 8 guns: 4 port, 4 rail",
    ]


def test_her_broadside_by_70s_rule_is_eight_pounds():
    """`far_ship` counts one side's broadside guns and every gun not on the broadside
    (combat/far.py): her two 3-pounders a side and all four swivels, 8 lb, where her design
    reckoned 7 (6 lb a side and two swivels' 1 lb; the rule counts both sides' rail guns, as
    Build-Ships.md §9.1's review found for the lugger); unarmed, none."""
    from freesail.combat.far import far_ship

    assert far_ship(HER, "britain").broadside_lb == 0.0
    assert far_ship(HER, "britain", ARMED).broadside_lb == 8.0


def test_her_armed_fits_lowest_lee_port_shuts_at_twenty_two_degrees():
    """Her armed fit's line by 7-190's form (tests/test_lee_ports.py; Build-Ships.md §7.1's rule
    as built, the minute's hold included), for the record: unarmed by default, she has no line in
    7-190 (Bil-D §10). In a World that keeps a sea, her heel to starboard and her roll set by hand:
    her lowest lee port, No. 2 abaft (1.34 m, half-breadth 2.80 m at its sill), shuts at 21.70
    degrees of heel alone (her design's 20.8 on a half-breadth of 2.92, before the collier's
    sections gave her side); open half a degree below, shut a degree above, and a roll of 4 degrees
    on her motion the same four degrees sooner; her weather side open; upright again, open once the
    minute's hold has run. No. 1 forward (1.40 m, 2.79 m) shuts at 23.11 degrees."""
    from tests import test_lee_ports as L

    w = L._in_a_sea(HER, ARMED)
    assert w.ship.fit == ARMED
    gid, heel = L._lowest_lee(w, "upper")
    assert gid == "gun.2.starboard" and heel == pytest.approx(21.70, abs=0.05)
    assert L._open_then_shut(w, "upper", 21.70, 0.0, 0) == (0, 1)
    assert L._open_then_shut(w, "upper", 21.70, L.ROLL_SET_DEG, 4 * L.HOLD) == (0, 1)
    assert L.shut_heel(1.40, 2.79) == pytest.approx(23.11, abs=0.01)


# ---------------------------------------------------------------------------
# Her company, her wardroom, her quarters (Bil-D §5.4, §6)
# ---------------------------------------------------------------------------


def test_her_company_is_eight_with_two_in_the_main_top():
    """Bil-D §6.1 (D43): eight, the master and the mate (the smack's posts), two in each top (the
    main top's for the settee aloft: Ext §5.1 and its risk 10), the boy in the afterguard as the
    messenger, the cook; no forecastle station; her shares by rating 0.80 able and 0.20 landsmen,
    the boy drawn a landsman (the lead's ruling (8) of 2026-11-09; old: the merchant brig's shares,
    0.70, 0.20 and 0.10, the boy drawn an ordinary seaman); the english list. The quarter bill
    (§5.4): a topman of each top trimming, one at the helm, the powder the cook's, sail before
    guns, two small-arms men and three boarders (judgement)."""
    crew = load_spec(HER).crew
    assert (crew.complement, crew.names, crew.seamen) == (8, "english", 5)
    assert [p.post for p in crew.posts] == ["master", "mate"]
    st = {k: v for k, v in crew.stations.items() if v}
    assert st == {"fore_top": 2, "main_top": 2, "afterguard": 1, "idlers": 1}
    assert crew.stations["forecastle"] == 0
    assert len(crew.posts) + sum(st.values()) == crew.complement
    assert crew.idlers_by_trade == {"cook": 1}
    assert crew.ratings == {"able": 0.80, "ordinary": 0.0, "landsman": 0.20}
    assert [(p.role, p.station, p.rating, p.messenger) for p in crew.people] == [
        ("boy", "afterguard", "landsman", True)
    ]
    bill = crew.quarter_bill
    assert bill.trimmers == {"fore_top": 1, "main_top": 1}
    assert (bill.helm, bill.powder, bill.priority) == (1, 0, "sail before guns")
    assert (bill.small_arms, bill.boarders, bill.filling) == (2, 3, 1)


def test_her_ship_files_posts_and_people_agree_with_her_wardroom_file():
    """tests/test_wardroom.py's check (:42-57) on her file (Bil-D §6.2): the generator draws the
    posts and the drawn roles from `data/people/bilander.yaml` (spec M6 §2); the harness's stations
    the smack's, the captain the master and the officer of the watch and the master's station the
    mate. Her outlines are bred in the Poole and Newfoundland trade, name no one and say no
    source's page, no judgement and no 'he' in the words served."""
    from freesail.world import people as PE

    wardroom = PE.load_wardroom(HER)
    assert wardroom is not None
    spec = load_spec(ROOT / HER)
    assert [p.post for p in spec.crew.posts] == wardroom.posts == ["master", "mate"]
    drawn = [
        (o.role, o.drawn["station"], o.drawn.get("rating"), o.messenger) for o in wardroom.drawn
    ]
    assert [(p.role, p.station, p.rating, p.messenger) for p in spec.crew.people] == drawn
    raw = yaml.safe_load((ROOT / "data" / "people" / "bilander.yaml").read_text("utf-8"))
    assert raw["ship"] == HER
    assert wardroom.role_of("captain") == "master"
    assert wardroom.role_of("officer of the watch") == "mate"
    assert wardroom.role_of("master") == "mate"
    forbidden = r"Lloyd|Bil|p\. \d|judgement|\bhis\b|\bhe\b|\bhim\b|Hopewell"
    for entry in raw["wardroom"]:
        for key in ("traits", "history", "brief"):
            words = " ".join(entry[key]) if key == "traits" else entry[key]
            assert words and not re.search(forbidden, words), (entry["role"], key)


def _her_world(fit=None):
    """Her World off the Lizard under British colours at seed 7 (tests/test_brains.py's world),
    her default fit or the one named."""
    from tests.test_brains import world_at

    return world_at(49.5, -5.5, HER, **({"fit": fit} if fit else {}))


def test_her_muster_at_seed_7_puts_four_topmen_aloft_and_the_boy_aft():
    """Her muster at seed 7 (crew/muster.py): the master and the mate on the quarterdeck; her five
    seamen by the shares (four able, one landsman: the lead's ruling (8) of 2026-11-09), the tops
    filled first (`FILL_ORDER`), four able topmen aloft; the afterguard's one hand the landsman,
    and the boy drawn from it (world/people.py), as the merchant brig's boy is rated; the cook.
    Old: by the merchant brig's shares (four able, one ordinary) three able and the ordinary aloft
    and the afterguard's hand able, the boy, drawn wanting `ordinary` and finding none there,
    mustered an able seaman (B4, for the lead)."""
    w = _her_world()
    by = [(s.station.value, s.rating.value) for s in w.ship.extra["crew"].sailors]
    assert by == [
        ("quarterdeck", "officer"),
        ("quarterdeck", "officer"),
        ("fore_top", "able"),
        ("fore_top", "able"),
        ("main_top", "able"),
        ("main_top", "able"),
        ("afterguard", "landsman"),
        ("idlers", "idler"),
    ]
    boy = w.people.find("the boy")
    assert boy is not None and boy.messenger
    assert boy.sailor_id == next(
        s.id for s in w.ship.extra["crew"].sailors if s.station.value == "afterguard"
    )
    assert [p.role for p in w.people.all] == ["master", "mate", "boy"]


@pytest.mark.parametrize("fit", [None, ARMED], ids=["unarmed", "armed merchant"])
def test_her_quarters_at_the_beat_man_one_gun_short_on_the_armed_fit(fit):
    """Bil-D §5.4: `Quarters.beat` measured at muster at seed 7 (crew/quarters.py), off the
    Lizard. Her six hands off the quarterdeck: the bill's two trimmers (a topman of each top) and
    the helm are told off first, the cook to the powder. The helm takes an able man first, and
    since her boy is a landsman (the lead's ruling (8) of 2026-11-09) it is a fore topman, the
    afterguard's hand, the boy, going to the trimmers unarmed and to No. 1 armed (old: the boy at
    the helm, the afterguard's hand able). On the armed fit her guns want ten, a crew of three to
    each 3-pounder pair and a man to each swivel: No. 1 forward takes the boy and the main topman
    left, one short (old: the two topmen left), and No. 2 and the swivels stand unmanned, as the
    log says; her design's 'one gun or none', recorded as the period's numbers give it and not
    forced. Unarmed, no gun crew forms and the three topmen and the boy are the trimmers (old: the
    four topmen). The log's lines are the same."""
    from freesail.crew.quarters import HELM, POWDER, TRIMMERS, quarters_of

    w = _her_world(fit)
    w.run(10)
    w.submit("beat to quarters")
    w.run(30)
    q = quarters_of(w.ship)
    manned = {k: [s.station.value for s in gc.members] for k, gc in q.crews.items()}
    sizes = {d: [s.station.value for s in q.divisions[d]] for d in (TRIMMERS, HELM, POWDER)}
    said = [e.text for e in w.log if e.kind == "crew.quarters"]
    if fit is None:
        assert manned == {}
        assert sizes == {
            TRIMMERS: ["fore_top", "main_top", "main_top", "afterguard"],
            HELM: ["fore_top"],
            POWDER: ["idlers"],
        }
        assert said == [
            "Beat to quarters! Quarters: no gun crews manned, the trimmers 4, the helm 1, the "
            "powder 1."
        ]
    else:
        assert {k: gc.wanted for k, gc in q.crews.items()} == {
            "gun:1": 3,
            "gun:2": 3,
            "gun:swivel.1.larboard": 1,
            "gun:swivel.1.starboard": 1,
            "gun:swivel.2.larboard": 1,
            "gun:swivel.2.starboard": 1,
        }
        assert {k: v for k, v in manned.items() if v} == {"gun:1": ["afterguard", "main_top"]}
        assert sizes == {
            TRIMMERS: ["fore_top", "main_top"],
            HELM: ["fore_top"],
            POWDER: ["idlers"],
        }
        # package 115 D1 (re-pinned by the lead's word): the beat says the guns are secured;
        # old, the line ended at "stand unmanned."
        assert said == [
            "Beat to quarters! Quarters: one gun crew manned, the trimmers 2, the helm 1, the "
            "powder 1. Not hands enough for every gun: the swivels and No. 2 gun stand unmanned. "
            "The guns are secured: 'cast loose the guns' to serve them."
        ]
    assert not [e for e in w.log if e.kind == "order.rejected"]


# ---------------------------------------------------------------------------
# Her ground tackle, boat, pumps, hold and stores (Bil-D §7)
# ---------------------------------------------------------------------------


def test_her_ground_tackle_is_the_house_rule_two_bowers_and_a_kedge():
    """Bil-D §7: the merchant brig's rule (`gen_ships.ground_tackle_for`) on her 128 tons, 19.4 ft
    and 11.5 ft: two bowers of 6.4 cwt by Luce 1866's five to the hundred tons (to ten kilograms),
    9 1/2-in hemp cables, the best bower's two spliced, and a kedge of an eighth on a hawser of
    half; no sheet or stream under 200 tons (Lever 1808 p. 67). Steel 1794's Navy table, whose
    smallest rows (the brigs of 200 tons, three of 12 cwt) would give her 7.7 cwt, is the check in
    her note and the generator's report."""
    tackle = load_spec(HER).ground_tackle
    assert not tackle.chain
    anchors = {a.id: a for a in tackle.anchors}
    assert list(anchors) == ["best_bower", "small_bower", "kedge"]
    for aid in ("best_bower", "small_bower"):
        assert anchors[aid].weight_kg == pytest.approx(6.4 * CWT_KG, abs=5.0), aid
        assert (anchors[aid].kind, anchors[aid].cable_in) == ("bower", 9.5), aid
    assert [anchors[a].cable_fathoms for a in anchors] == [240.0, 120.0, 120.0]
    assert anchors["kedge"].weight_kg == 40.0 and anchors["kedge"].cable_in == 5.0
    text = (ROOT / HER).read_text(encoding="utf-8")
    assert "the brigs of 200 tons, three anchors of 12 cwt, and the cutter, three of 10 cwt" in text


def test_her_boat_pumps_hold_and_stores():
    """Bil-D §7: one boat, the long-boat amidships, 18 ft by Luce's rule on her 75.6 ft at the small
    vessel's factor (Gwyn draws none: judgement); two hand pumps, the merchant brig's; her hold a
    trader's half of her 128 tons; water for two months at a gallon a man a day and some over,
    provisions for two months, 80 fathoms of spare rope, two shot plugs, a spare topsail yard, a
    second fore topsail and jib and the storm staysails in the sail room (judgement); the Navy's
    ration, which every file names (tests/test_stores.py)."""
    spec = load_spec(HER)
    assert [(b.id, b.kind, b.name, b.length_ft, b.oars) for b in spec.boats] == [
        ("long_boat", "launch", "the long-boat", 18.0, 6)
    ]
    assert [(p.kind, p.hands) for p in spec.pumps] == [("hand", 2), ("hand", 2)]
    assert spec.hold.capacity_tons == 64.0
    stores = spec.crew.stores
    assert (stores.water_tons, stores.provisions_days) == (3.0, 60.0)
    # eight men a gallon a day for sixty days, at 252 gallons to the ton (data/crew/ration.yaml)
    assert 8 * 60 / 252.0 < stores.water_tons < 2 * 8 * 60 / 252.0
    assert (stores.cordage_fathoms, stores.shot_plugs, stores.spars) == (80.0, 2.0, {"yard": 1})
    assert [s.kind for s in stores.sails] == [
        "fore.topsail",
        "jib",
        "fore.storm_staysail",
        "main.storm_staysail",
    ]
    raw = yaml.safe_load((ROOT / HER).read_text(encoding="utf-8"))["crew"]["ration"]
    assert raw == {"table": "navy", "water_gallons": 1}


# ---------------------------------------------------------------------------
# Her description at far detail (Bil-D §8; D16 (a))
# ---------------------------------------------------------------------------

WHAT = "a bilander, a merchantman under a settee main, deep laden"


def test_her_description_in_her_file_is_a_bilander_at_four_miles_and_a_merchant():
    """Bil-D §8, by SW-4's form (Build-Ships.md §8.1, §8.2): her file's one description, rig 'a
    bilander' (the tops make out her settee's yard; the period named the rig on sight), her words,
    the role `merchant`, and her fit `unarmed`, her file's default, so that a far ship of hers
    carries nothing new (her design's 'no fit word' was written before SW-4's form, by which every
    row's file gives both, as the topsail schooner's does). Rank 1 by her words, a cutter's; none
    of them a man of war's; 'merchant' in what she is made out to be, so that a cruiser takes her
    for a weaker mark (`captains._weaker`)."""
    from freesail.world import brains
    from freesail.world import captains as C
    from freesail.world import ships as S

    own = S.file_descriptions(HER)
    assert list(own) == ["bilander"]
    d = own["bilander"]
    assert (d["rig"], d["what"], d["roles"], d["fit"]) == (
        "a bilander",
        WHAT,
        ["merchant"],
        "unarmed",
    )
    assert S._default_fit(HER) == "unarmed"
    assert C.SIZE_RANK["bilander"] == 1 and C.size_of_file(HER) == 1
    assert C.size_of_words(WHAT) == 1 and C.size_rank_of(WHAT) == 1
    assert "merchant" in WHAT and not [w for w in C.MAN_OF_WAR_WORDS if w in WHAT]
    assert brains.description_role("bilander") == "merchant"


@pytest.mark.parametrize(
    "words",
    [
        "bilander",
        "a bilander",
        "the bilander",
        "a billander",
        "billander",
        "an armed bilander",
        "a merchant bilander",
        "a British bilander",
    ],
)
def test_her_words_name_her_through_the_index(words):
    """Bil-D §8: her rig's word with either article and Lloyd's key's spelling, 'Billander' (the
    keys of 1781 to 1789), give her key; qualified, they give it by the tail rule
    (`description_key`)."""
    from freesail.world import ships as S

    assert S.description_key(words) == "bilander"


def test_her_index_row_is_her_files_and_a_far_ship_of_hers_sails_unarmed_as_a_merchant():
    """Bil-D §8: her index row names her file, whose words it serves with her fit and role; a far
    ship of 'a bilander' carries her default unwritten and takes the merchant's role where none is
    given; a fit and a role her file gives are kept; a role it does not give is refused in words."""
    from freesail.world import brains
    from freesail.world import ships as S
    from tests.test_profile import _sea

    assert S.description("bilander") == {
        "file": HER,
        "rig": "a bilander",
        "what": WHAT,
        "fit": "unarmed",
        "roles": ["merchant"],
    }
    world = _sea()
    spec = {
        "description": "a bilander",
        "name": "Hopewell",
        "nation": "britain",
        "position": "49 30 N 5 30 W",
        "goal": "bound for Plymouth",
    }
    v = S.vessel_from_spec(world, dict(spec), 1)
    assert (v.description, v.ship_file, v.role, v.fit) == ("bilander", HER, "", "")
    assert brains.role_of_vessel(v, None) == "merchant"
    armed = S.vessel_from_spec(world, dict(spec, role="merchant", fit=ARMED), 2)
    assert (armed.role, armed.fit) == ("merchant", ARMED)
    with pytest.raises(
        ValueError, match="'kings-ship' is no role a bilander takes; her file gives"
    ):
        S.vessel_from_spec(world, dict(spec, role="kings-ship"), 3)


def test_her_row_sails_by_her_first_role_wherever_the_intent_names_none():
    """`brains.sub_type_role` reads the first role of every row filed since package 75 (B2b, the
    lead's ruling of 2026-11-07; `INTENT_RULED_ROWS` holds the eight older rows): hers is the
    merchant's with no intent, on a passage, homeward and on a station, and the intent's own where
    it names one (prizes the privateer's, a ground the fisherman's, a letter the packet's, a convoy
    the commodore's). Her own World's captain takes the same by her file's first row
    (`brains.own_sub_type_role`)."""
    from types import SimpleNamespace

    from freesail.world import brains

    kinds = (
        ("", False, False),
        ("passage", False, False),
        ("home", False, False),
        ("station", False, False),
        ("station", True, False),
        ("fish", False, False),
        ("letter", False, False),
        ("passage", False, True),
    )
    got = []
    for kind, prizes, convoy in kinds:
        intent = SimpleNamespace(kind=kind, prizes=prizes, convoy=convoy) if kind else None
        got.append(brains.role_of_vessel(SimpleNamespace(description="bilander", role=""), intent))
    assert got == ["merchant"] * 4 + ["privateer", "fisherman", "packet", "commodore"]
    assert "bilander" not in brains.INTENT_RULED_ROWS
    world = SimpleNamespace(ship=SimpleNamespace(spec=SimpleNamespace(source=str(ROOT / HER))))
    assert brains.own_sub_type_role(world) == "merchant"


# ---------------------------------------------------------------------------
# Her handling on the engine's settee (her road's step 5; Bil-D §12.2, §14; Ext §5; B3.3)
# ---------------------------------------------------------------------------

SETTEE = "main.settee"
FOUR_POINTS, SEVEN_POINTS = 45.0, 78.75  # the heave-to's band (data/evolutions/heave_to.yaml)
LUG_FLOOR_DEG = 8.0


def _her_settle(knots=15.0, **scenario):
    """B3.4's settle on her file, as tests/test_settee.py settles the fixture (docs/dev/
    TuningNotes.md, "The schooner's mast"): seed 7, the wind from the north, no gusts, her head
    292.5 degrees (67.5 off on the starboard tack) at 5 kn; plain sail set and braced sharp up,
    settled 2,400 s, trimmed every two minutes after 300 s. Two changes for her company of eight,
    each judgement (her step 5): all hands called first and kept up (a watch of two or three sets
    her plain sail one sail at a time: all hands set it by about 1,650 s in 15 kn and 1,800 in 20),
    and the trim ordered only while her hands are free, the settle ending once their work in hand
    is done (trimmed every two minutes regardless, her eight fall behind, the trims queue, and a
    heave-to ordered after them waits on them: measured at her step 5)."""
    from freesail.api.session import make_world
    from freesail.core.world import Scenario

    sc = Scenario(
        wind_from_deg=0.0,
        wind_speed_kn=knots,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=292.5,
        ship_speed_kn=5.0,
        **scenario,
    )
    world = make_world(7, HER, sc)
    for order in ("call all hands", "set plain sail", "brace sharp up on the starboard tack"):
        world.submit(order)
    runner = world.ship.extra["evolutions"]
    for i in range(2400):
        if i % 120 == 0 and i > 300 and not runner.in_progress():
            world.submit("trim sails")
        world.tick()
    for _ in range(600):
        if not runner.in_progress():
            break
        world.tick()
    assert not runner.in_progress()
    assert all(world.ship.sails[s].is_set for s in world.ship.groups["plain sail"])
    assert world.ship.dyn.tack == "starboard"
    return world


def _rel_deg(world) -> float:
    return math.degrees(units.relative_bearing(world.ship.dyn.heading, world.wind.direction_from))


def _after(world, start: int) -> list:
    return [e for e in world.log if e.tick > start]


def _first_tick(world, start: int, words: str) -> int | None:
    hit = [e.tick for e in _after(world, start) if words in e.text]
    return hit[0] - start if hit else None


# Her lie hove to, measured on her file at seed 7 from her settle at her `clr_x_m` +2.0 (her
# review, 2026-11-08): the degrees off the wind at +150 s and +300 s, the least and the most from
# +300 s to +900 s, her mean headway there (kn); and her helm close-hauled before the order
# (weather helm positive). At +2.25 (her step 5): 15 kn kept 59.9, 63.9, 63.9-64.2, 0.72; 20 kn
# kept 61.6, 64.0, 63.9-64.0, 0.92; 15 kn clewed up 65.0, 68.7, 67.8-68.6, 1.08; 20 kn clewed up
# 72.7, 66.6, 66.6-66.7, 1.35; her helm -1.27 and +3.30; in 8 kn kept, forced round through the
# wind at +307 s.
HOVE_TO = {
    (8.0, True): (45.8, 70.0, 64.8, 70.0, 0.54),
    (15.0, True): (61.7, 65.2, 65.1, 65.4, 0.95),
    (20.0, True): (65.3, 62.7, 62.7, 63.6, 1.14),
    (15.0, False): (67.0, 68.1, 68.0, 69.0, 1.16),
    (20.0, False): (73.1, 67.3, 67.3, 69.3, 1.23),
}
# Her helm at the settle's end, measured again with her boy a landsman (the lead's ruling (8) of
# 2026-11-09): her company's work at the settle's trims changed, the settle ends at another
# moment of her trim (in 15 kn at 2,667 s, old 2,580; in 20 kn at 2,432, old 2,536), and the
# figure moves (old: -2.02, -2.02 and +0.25), her lie hove to within its old figures' bounds
CLOSE_HAULED_HELM = {8.0: -1.14, 15.0: 0.43, 20.0: -4.91}


@pytest.mark.parametrize(
    "knots, kept",
    [(8.0, True), (15.0, True), (15.0, False), (20.0, True), (20.0, False)],
    ids=["8.0-kept", "15.0-kept", "15.0-clewed up", "20.0-kept", "20.0-clewed up"],
)
def test_hove_to_her_main_topsail_goes_to_the_mast_and_she_lies_to_both_ways(
    monkeypatch, knots, kept
):
    """Ext §5.7 and her design's §12.2 item 5 and §14 (a test, not a truth: no source says how a
    bilander lay to, Research-Bilander-2026-10.md §4), on B3.3's settee: her main topsail to the
    mast by her file's `heave_to_aback` (D4 (a)), her courses hauled up, and her settee by the
    engine's driver rule, as the lead ruled on Ext §14 item 3: kept, its sheet eased
    (`HOVE_TO_DRIVER_APPARENT`), her backed yards being on her aftermost mast with yards; and,
    the other way measured against it (`SETTEE_KEPT_HOVE_TO` false), clewed up aloft, D4 (a)'s
    words, its yard standing. Her lie at seed 7 from her settle at her `clr_x_m` as tuned, +2.0,
    measured (her review, 2026-11-08), at +150 s, +300 s and from +300 s to +900 s, her mean
    headway there:
    - kept: 8 kn 45.8, 70.0, 64.8-70.0 degrees off, 0.54 kn ahead; 15 kn 61.7, 65.2, 65.1-65.4,
      0.95 kn; 20 kn 65.3, 62.7, 62.7-63.6, 1.14 kn (the fixture 63.5 degrees, the brig 63-64);
    - clewed up: 15 kn 67.0, 68.1, 68.0-69.0, 1.16 kn; 20 kn 73.1, 67.3, 67.3-69.3, 1.23 kn.
    Both inside the heave-to's four to seven points on her file, where on the fixture (and on her
    file at her start, +0.40) clewed up she fell off past seven points: so the figures do not say
    otherwise and the driver rule stands, B3.3's way pinned. Kept, she lies to in 8 kn too, the
    lightest of the polar's winds: at +2.25 (her step 5's figure) she was forced round through the
    wind there at +307 s, and at +2.2 at +360 s (her review); clewed up in 8 kn she lies past
    seven points at +2.0 (72.3-87.0), the other way, recorded and not pinned. At +0.40 she lay
    kept 64.2 degrees off at 1.93 kn and clewed up fell off to a run by +900 s; at +3.0 kept she
    came head to wind by +150 s and made sternway (her tuning notes). Her helm close-hauled
    before the order, 67.5 degrees off: 2.02 degrees of lee helm in 8 kn and in 15, 0.25 of
    weather helm in 20 (at +2.25, 1.27 of lee helm in 15 and 3.30 of weather helm in 20); since her
    boy is a landsman (the lead's ruling (8) of 2026-11-09), 1.14 of lee helm in 8 kn, 0.43 of
    weather helm in 15 and 4.91 of lee helm in 20, her settle ending at another moment of her trim
    (`CLOSE_HAULED_HELM`), and her lie hove to within two degrees of the figures above (8 kn kept
    47.5, 69.5, 64.7-69.5 at 0.54 kn; 15 kn kept 61.4, 65.2, 65.1-65.4; clewed up 66.9, 67.9,
    67.9-68.9; 20 kn kept 65.3, 62.6, 62.6-63.6; clewed up 73.5, 67.2, 67.2-69.3; each headway
    the same to the hundredth)."""
    from freesail.evolutions import scripts

    monkeypatch.setattr(scripts, "SETTEE_KEPT_HOVE_TO", kept)
    world = _her_settle(knots)
    settee = world.ship.sails[SETTEE]
    assert math.degrees(world.ship.dyn.weather_helm) == pytest.approx(
        CLOSE_HAULED_HELM[knots], abs=0.5
    )
    start = world.clock.tick
    world.submit("heave to")
    at, offs, ahead = {}, [], []
    for i in range(1, 901):
        world.tick()
        off = abs(_rel_deg(world))
        if i in (150, 300):
            at[i] = off
        if i > 300:
            offs.append(off)
            ahead.append(units.ms_to_knots(world.ship.dyn.u))
    texts = [e.text for e in _after(world, start)]
    words = "eased off the mainsail sheet" if kept else "clewed up the mainsail"
    assert f"Hauled up the courses; {words}." in texts, texts
    # in 20 kn her settle now ends with her yards braced sharp up to their limits, its last trim
    # not yet ordered (her boy a landsman, the lead's ruling (8) of 2026-11-09), so that none is
    # braced up at the heave-to (old: "braced up the other yards" at every wind)
    braced = "" if knots == 20.0 else " braced up the other yards;"
    assert (
        f"Braced the main topsail aback;{braced} hauled aft the head sheets; helm a-lee." in texts
    )
    assert any(
        t.startswith("Hove to on the starboard tack, main topsail to the mast") for t in texts
    )
    assert not settee.yard_lowered
    if kept:
        assert settee.is_set
    else:
        assert settee.state is SailState.IN_THE_GEAR
    at_150, at_300, least, most, headway = HOVE_TO[(knots, kept)]
    assert abs(at[150] - at_150) <= 3.0 and abs(at[300] - at_300) <= 3.0, at
    assert FOUR_POINTS <= min(offs) and max(offs) <= SEVEN_POINTS
    assert abs(min(offs) - least) <= 1.0 and abs(max(offs) - most) <= 1.0, (min(offs), max(offs))
    assert sum(ahead) / len(ahead) == pytest.approx(headway, abs=0.15)


def test_forced_round_hove_to_her_kept_settee_is_dipped_first_and_she_fills_away():
    """Her review's finding 1 (docs/dev/TuningNotes.md, "Her review's mends"), built by B3.3b, the
    follow-up B3 step keyed on `settee` alone that her design's §17 lead item 8 provides for (the
    lead's answer (8)): hove to with her settee kept, its yard on the larboard side, the starboard
    tack's lee, a shift of eight points forces her round onto the larboard tack, and the yard is on
    her weather side, against its mast. "Fill away" dips it first, as she lies (Ext §5.7's as-built
    note): lowered at the order, hoisted on the starboard side when its time is done, its sheet
    drawn for the wind she will have full and by, and then she is let fall off and filled away,
    each said. Seed 7, 15 kn, from her settle, hove to at +108 s (old +106) and the shift 60 s
    after: forced round 20 s after the shift, the order 40 s after that; the dip's words at +1 s,
    she lying 65-85 degrees off while its yard is on deck (as she lies with it clewed up, D4 (a));
    hoisted and "Hauled aft the head sheets" at +177 s, "Filled away on the larboard tack" at +244
    s; at +300 s it draws clear of its mast as at her settle (61.8 m2), at 4.04 kn. Old, before her
    boy was a landsman (the lead's ruling (8) of 2026-11-09; the dip is all hands' work, the boy
    among them): hoisted at +158 s, filled away at +218 s, at 4.15 kn. Before B3.3b she
    was filled away at +59 s with it drawing against its mast to the end, two-thirds of that
    (41.3 m2), at 3.13 kn, and no line said so; at her step 5's +2.25 in 8 kn she was forced round
    of herself and filled away so (41.4 m2, 2.23 kn, her review). Dipped as she fell off instead
    (B3.3b's first build, not committed), the settee down while she had a knot of way, she came
    head to the wind once it was hoisted and was taken aback at +254 s, going astern."""
    from freesail.evolutions import trim as yard_trim
    from freesail.physics import sails as P

    world = _her_settle(15.0)
    settee = world.ship.sails[SETTEE]
    whole = settee.area_effective_m2  # clear of its mast, at her settle
    world.submit("heave to")
    for _ in range(600):
        world.tick()
        if "hove_to" in world.ship.extra:
            break
    world.run(60)
    assert world.ship.extra["hove_to"]["sign"] == 1.0
    assert settee.is_set and settee.lug_side == "larboard"
    start = world.clock.tick
    wind = world.wind  # the wind shifted at a stroke, as tests/test_lying_to.py forces her round
    wind.follow(units.wrap_2pi(wind.base_direction - 8.0 * units.POINT), wind.base_speed)
    world.scenario.wind_from_deg = math.degrees(wind.base_direction)
    world.run(60)
    (forced,) = [e for e in _after(world, start) if e.kind == "ship.forced_round"]
    assert "lies on the larboard tack" in forced.text
    lies = yard_trim.read_sheet(world.ship, settee).side
    assert settee.lug_side == "larboard" and lies == 1 and P.against_the_mast(settee, lies)
    start = world.clock.tick
    assert world.submit("fill away").kind == "order.accepted"
    world.run(300)
    dip = (
        "Dip the mainsail: lower the yard, pass it round abaft the mast and shift the tack to the "
        "weather bow."
    )
    hoisted = "Dipped the mainsail; hoisted on the starboard side, to leeward of the mast."
    hauled = "Hauled aft the head sheets; kept the helm a-lee to let her fall off."
    assert _first_tick(world, start, dip) == 1
    up = _first_tick(world, start, hoisted)
    assert up is not None and abs(up - 177) <= 10, [e.text for e in _after(world, start)]
    assert _first_tick(world, start, hauled) == up  # then she is let fall off
    filled = [e for e in _after(world, start) if e.kind == "ship.filled_away"]
    assert len(filled) == 1 and filled[0].text.startswith("Filled away on the larboard tack")
    assert up < filled[0].tick - start <= up + 90
    assert not [e for e in _after(world, start) if e.kind in ("ship.aback", "ship.filled")]
    lies = yard_trim.read_sheet(world.ship, settee).side
    assert settee.is_set and settee.lug_side == "starboard" and not settee.yard_lowered
    assert lies == 1 and not P.against_the_mast(settee, lies)
    assert world.ship.dyn.tack == "larboard" and "hove_to" not in world.ship.extra
    assert settee.area_effective_m2 == pytest.approx(whole, rel=0.01)
    assert abs(_rel_deg(world)) == pytest.approx(67.5, abs=5.0)  # full and by on the larboard tack


def test_forced_round_in_her_larboard_watch_by_night_the_settee_is_to_be_dipped_with_hands():
    """The review of the lead's ruling (3)(i) of 2026-11-10, on her file as her watch plays it: from
    her settle at 00:00 (all hands kept up), hove to, the hands piped down at 00:46, the larboard
    watch's two on deck, 60 s, and the shift of eight points. Forced round at +20 s; hove to no
    longer at +155 s, her after yards full, and the settee lies against its mast. The watch's dip
    wants six and begins with three (`hands.SHORT_HANDED_SHARE`): with two it waits for hands, and
    the line says the mainsail is to be dipped, the runner's "Not hands enough on deck" after it,
    no word that the watch dips it. When there are hands it begins: all hands called at +160 s,
    begun at +161 s with the four on deck, dipped at +555 s, on her lee, drawing whole. Before
    (caf1d329), the line said "The watch dips the mainsail, lying against its mast." on the tick
    the dip was found to wait for hands. Left to the watch (hove to 600 s, as the tuning notes
    measure it), the dip waits to the watch's end: at +1,800 s the settee lies against its mast, at
    41.2 m2 and 2.54 kn, as it lay before the ruling; begun as the starboard watch relieves the
    deck at 04:00 and dipped 680 s after (docs/dev/TuningNotes.md, "The review's mends of the two
    builds")."""
    from datetime import datetime

    from freesail.evolutions import trim as yard_trim
    from freesail.physics import sails as P

    world = _her_settle(15.0, start_time=datetime(1805, 6, 1, 0, 0))
    runner = world.ship.extra["evolutions"]
    settee = world.ship.sails[SETTEE]
    whole = settee.area_effective_m2  # clear of its mast, at her settle
    world.submit("heave to")
    for _ in range(600):
        world.tick()
        if "hove_to" in world.ship.extra:
            break
    for _ in range(600):
        if not runner.in_progress():
            break
        world.tick()
    assert world.submit("pipe down").kind == "crew.piped_down"
    world.run(60)
    assert world.ship.extra["hove_to"]["sign"] == 1.0 and settee.lug_side == "larboard"
    start = world.clock.tick
    wind = world.wind
    wind.follow(units.wrap_2pi(wind.base_direction - 8.0 * units.POINT), wind.base_speed)
    world.scenario.wind_from_deg = math.degrees(wind.base_direction)
    for _ in range(600):
        world.tick()
        if "hove_to" not in world.ship.extra:
            break
    (filled,) = [e for e in _after(world, start) if e.kind == "ship.filled"]
    at = filled.tick - start
    assert abs(at - 155) <= 15 and filled.severity.value == "urgent"
    assert filled.text.endswith(
        "hove to no longer. The helm keeps her full and by. "
        "The mainsail, lying against its mast, is to be dipped."
    ), filled.text
    assert "The watch dips" not in filled.text and "settees_dipped" not in filled.data
    assert filled.data["settees_to_be_dipped"] == [SETTEE]
    waiting = [e for e in _after(world, start) if e.kind == "evolution.waiting"]
    assert [(e.tick - start, e.text) for e in waiting] == [
        (at, "Not hands enough on deck to dip the mainsail; there are but two to spare.")
    ]
    said = [e.kind for e in _after(world, start)]
    assert said.index("evolution.waiting") > said.index("ship.filled")  # after the line
    (dip,) = [i for i in runner.instances if i.evo.id == "dip_settee"]
    assert dip.waiting and dip.waiting_for == "hands"
    world.run(160 - (world.clock.tick - start))
    assert dip.waiting and settee.lug_side == "larboard" and not settee.yard_lowered
    assert world.submit("call all hands").kind == "crew.order"
    for _ in range(900):
        world.tick()
        if not runner.in_progress():
            break
    begun = _first_tick(world, start, "Dip the mainsail! Hands to the jeers and the tack.")
    up = _first_tick(world, start, "Dipped the mainsail; it stands to leeward of the mast.")
    assert begun == 161 and up is not None and abs(up - 555) <= 20
    lies = yard_trim.read_sheet(world.ship, settee).side
    assert settee.is_set and settee.lug_side == "starboard" and not settee.yard_lowered
    assert lies == 1 and not P.against_the_mast(settee, lies)
    assert settee.area_effective_m2 == pytest.approx(whole, rel=0.01)
    assert not [e for e in _after(world, start) if e.kind == "evolution.failed"]


@pytest.mark.parametrize(
    "hour, watch, wore_s, taken_in_s",
    [(0, "larboard", 558, None), (4, "starboard", 501, 643)],
)
def test_a_wear_ordered_after_an_order_of_her_settee_begins_at_once_and_keeps_the_order(
    hour, watch, wore_s, taken_in_s
):
    """The review of the lead's ruling (3)(iii) of 2026-11-10: the wear holds her settee from the
    order, and an order of the settee's given first does not keep it waiting on the settee alone
    (`Runner._settees_only`): the wear begins at the order, as a manoeuvre that belays the step-list
    work in hand does (decision 25), and the settee's order is not begun while she wears. From her
    settle (all hands kept up), the hands piped down, 30 s, "take in the mainsail", and 29 s later
    "wear ship"; seed 7, 15 kn.
    - Her larboard watch by night (00:45, two on deck): the take in waits for hands; the wear
      calls all hands at the order and wears her at +558 s; the take in waits for the wear, and
      after it for hands again (the watch of two), kept: all hands called, it is begun at once.
      Before (caf1d329) the wear waited behind the take in, itself waiting for hands, and nothing
      more was said to +1,200 s, she on the starboard tack still; before the ruling (8bceb1cb) it
      wore her at +558 s and the take in was lost at +30 s ("The mainsail is in the gear; there is
      nothing to take in.", the wear lowering it), the settee hoisted again on the new lee.
    - Her starboard watch (04:45, three on deck): the take in is begun short-handed, and the wear
      belays it at the order ("Belayed taking in the mainsail: stations for wearing ship."), wears
      her at +501 s, and the take in is taken up again after: "Took in the mainsail" at +643 s, as
      before the ruling. Before (caf1d329) the wear waited for the take in to +169 s and wore her
      at +637 s."""
    from datetime import datetime

    world = _her_settle(15.0, start_time=datetime(1805, 6, 1, hour, 0))
    assert world.submit("pipe down").kind == "crew.piped_down"
    world.run(30)
    runner = world.ship.extra["evolutions"]
    settee = world.ship.sails[SETTEE]
    start = world.clock.tick
    assert world.submit("take in the mainsail").kind == "order.accepted"
    world.run(29)
    (take_in,) = [i for i in runner.instances if i.evo.id == "take_in_settee"]
    assert take_in.waiting == (watch == "larboard") and not take_in.paused
    assert world.submit("wear ship").kind == "order.accepted"
    (wear,) = [i for i in runner.instances if i.evo.id == "wear"]
    assert not wear.waiting and SETTEE in wear.holds and SETTEE in take_in.holds
    if watch == "larboard":
        assert take_in.waiting and take_in.waiting_for == "hands"
    else:
        assert take_in.paused  # belayed by the wear
    for _ in range(900):
        world.tick()
        if any(e.kind == "ship.wore" for e in _after(world, start)):
            break
    after = _after(world, start)
    assert _first_tick(world, start, "All hands! (to wear ship)") == 30
    (wore,) = [e.tick - start for e in after if e.kind == "ship.wore"]
    assert abs(wore - wore_s) <= 15 and world.ship.dyn.tack == "larboard"
    assert not [e for e in after if e.kind in ("sail.taken_in", "evolution.done_already")]
    belayed = [e.text for e in after if e.kind == "evolution.belayed"]
    if watch == "larboard":
        assert belayed == []
        world.run(5)
        assert take_in in runner.instances and take_in.waiting_for == "hands"  # kept, not lost
        assert settee.is_set and settee.lug_side == "starboard"  # hoisted on the new lee
        assert world.submit("call all hands").kind == "crew.order"
        mark = world.clock.tick - start
        for _ in range(300):
            world.tick()
            if not runner.in_progress():
                break
        taken = _first_tick(world, start, "Took in the mainsail")
        assert taken is not None and mark < taken <= mark + 150
    else:
        assert belayed == ["Belayed taking in the mainsail: stations for wearing ship."]
        for _ in range(300):
            world.tick()
            if not runner.in_progress():
                break
        taken = _first_tick(world, start, "Took in the mainsail")
        assert taken is not None and abs(taken - taken_in_s) <= 15
    assert settee.state is SailState.IN_THE_GEAR and not runner.in_progress()


def test_its_sheet_leads_a_fathom_abaft_its_clew_and_within_a_fathom_of_her_taffrail():
    """Ext §5.9 with the lead's ruling on her design's §17 lead item 4 (the block a fathom abaft the
    clew and abreast of it, the trim reading no part of the profile), and her design's §12.2 item
    6, B4's check: her settee's foot by its corners, tack to clew, is 11.29 m, where the loose-
    footed proxy (0.8 of the root of 73 m2) gives 6.84; the block a fathom abaft the clew at the
    lug's floor (8 degrees) stands at x -11.47, 0.31 m inside her taffrail (x -11.78): within the
    fathom. The proxy's would have stood at x -7.06, 4.72 m inside it (her design's 4.45 m and, for
    this block, 0.03 m, measured on its taffrail at x -11.52 before her step 1 moved the taffrail
    aft; old beside new). Her clew 2.12 m inside the taffrail (her design's 1.86). For the record
    (§12.2): the physics' lateral offset takes half the proxy's foot, 3.42 m, where her cut's half
    foot is 5.64 m (39% less); unchanged under the gate."""
    from freesail.evolutions import trim as yard_trim

    ship = load_ship(HER)
    settee = ship.sails[SETTEE]
    (tx, tz), _throat, _peak, (cx, cz) = settee.corners_m
    geo = yard_trim.sheet_geometry(ship, settee)
    assert not geo.boomed and geo.arm_m == pytest.approx(math.hypot(cx - tx, cz - tz))
    assert geo.arm_m == pytest.approx(11.29, abs=0.01)
    assert 0.8 * math.sqrt(settee.area_m2) == pytest.approx(6.84, abs=0.01)
    assert math.degrees(geo.floor) == pytest.approx(LUG_FLOOR_DEG)
    assert geo.lead_aft_m == yard_trim.FATHOM_M
    block_x = tx + geo._block(geo.floor)[0]
    taffrail = min(x for x, _z in ship.hull.spec.profile.rail_m)
    assert block_x == pytest.approx(-11.47, abs=0.01) and taffrail == -11.78
    assert 0.0 < block_x - taffrail <= yard_trim.FATHOM_M
    assert block_x - taffrail == pytest.approx(0.31, abs=0.01)
    assert cx - taffrail == pytest.approx(2.12, abs=0.01)


def _held_aback(incidence: float, against: bool) -> tuple[float, float]:
    """Her settee alone, at rest in 15 kn, held on its weather side at the lug's floor by its sheet
    (`set_sheet_angle(..., "weather")`), its yard on that side (clear of the mast) or the other
    (against it), the wind `incidence` degrees on its back face: the sail's force and the main
    mast's load, kN a square metre of its file area (B3.3's measure, Ext §5.10)."""
    import random

    from freesail.evolutions import trim as yard_trim
    from freesail.physics import sails as P
    from freesail.physics.wind import Wind, WindParams

    ship = load_ship(HER)
    for sl in ship.sails.values():
        sl.state = SailState.FURLED
    wind = Wind(
        WindParams.from_nautical((incidence - LUG_FLOOR_DEG) % 360.0, 15.0, 0.0, 0.0),
        random.Random(0),
    )
    s = ship.sails[SETTEE]
    s.state = SailState.SET
    P.compute_sail_forces(ship, wind)  # the deck's reading, for the sheet's sides
    yard_trim.set_sheet_angle(ship, s, math.radians(LUG_FLOOR_DEG), "weather")
    s.lug_side = "larboard" if against else "starboard"
    P.compute_sail_forces(ship, wind)
    assert s.backed and yard_trim.read_sheet(ship, s).held_to_windward
    return s.force_kn / s.area_m2, ship.spars["main.mast"].load_kn / s.area_m2


def _topsail_aback(incidence: float) -> tuple[float, float]:
    """Her main topsail alone on its square yard, the wind `incidence` degrees on its back face."""
    import random

    from freesail.physics import sails as P
    from freesail.physics.wind import Wind, WindParams

    ship = load_ship(HER)
    for sl in ship.sails.values():
        sl.state = SailState.FURLED
    wind = Wind(WindParams.from_nautical(90.0 - incidence, 15.0, 0.0, 0.0), random.Random(0))
    t = ship.sails["main.topsail"]
    t.state = SailState.SET
    ship.spars["main.topsail.yard"].brace_angle = 0.0
    P.compute_sail_forces(ship, wind)
    assert t.backed
    return t.force_kn / t.area_m2, ship.spars["main.mast"].load_kn / t.area_m2


def test_rule_5_on_her_file_holds_held_aback_near_its_trim_and_never_in_stays():
    """Rule 5 (D46; Fincham 1843 p. 59: aback, the settee presses the mast harder than a square
    sail does), Ext §5.10's measure on her file (B4's, the lead's ruling on her design's §17 lead
    item 8): the main mast's load a square metre of her settee held aback, against her main
    topsail's, at rest in 15 kn. Measured (2026-11-08), settee against topsail, kN a square metre:
    held aback near its trim, clear of the mast, 3.32 at 20 degrees on the back face, 1.92 at 25,
    1.28 at 30 and 1.03 at 35; against it, 2.22 at 20 and 1.28 at 25; laid flat aback it presses
    less, clear 0.86 at 40 and 0.82 at 45 and 60 (the engine's coefficients Ext §5.10's columns to
    the third place, as on the fixture). In her own tack at seed 7 in 15 and 20 kn her settee is
    never aback (truth 7-198, below: its single sheet lies it to leeward of the wind), her main
    topsail 39 and 36 ticks; in a shift of one and of two points close-hauled neither is aback
    (the settee's chord 27 degrees, the topsail's 29; her tuning notes). So on her file as on the
    fixture the case that holds is the settee held aback near its trim, which neither case the
    design named puts it in: pinned so and named, by the lead's ruling on Ext §14 item 4 (the case
    that holds pinned and named). D44 (c)'s `settee` row, accepted in advance only if neither
    holds, is not taken (her step 5; for the lead, as B3.3 left it: whether the static case
    counts). The main mast's load a square metre is the sail's own in every case."""
    for incidence, clear, against in ((20.0, 3.32, 2.22), (25.0, 1.92, 1.28), (30.0, 1.28, None)):
        top, top_mast = _topsail_aback(incidence)
        held, mast = _held_aback(incidence, against=False)
        assert mast == pytest.approx(held) and top_mast == pytest.approx(top)
        assert held / top == pytest.approx(clear, abs=0.03), incidence
        assert held > top, incidence
        if against is not None:
            on_mast, _ = _held_aback(incidence, against=True)
            assert on_mast / top == pytest.approx(against, abs=0.03), incidence
            assert on_mast > top, incidence
    for incidence in (40.0, 45.0, 60.0):  # laid flat aback: less than the topsail, clear or not
        top, _ = _topsail_aback(incidence)
        assert _held_aback(incidence, against=False)[0] < top, incidence
        assert _held_aback(incidence, against=True)[0] < top, incidence


# Her settee requests by watch (Ext §5.3; her design's §14 and §16 risk 7): each of the four
# settee evolutions' crew request against the hands on deck of her company as mustered at seed 7:
# the outcome, the hands wanted (after the company's clamp) and the hands got
REQUESTS = {
    ("starboard", False): [("short", 5, 3), ("short", 6, 3), ("short", 5, 3), ("short", 6, 3)],
    ("starboard", True): [("short", 5, 3), ("short", 6, 4), ("short", 5, 3), ("short", 6, 4)],
    ("larboard", False): [
        ("too few", 5, 0),
        ("too few", 6, 0),
        ("too few", 5, 0),
        ("too few", 6, 0),
    ],
    ("larboard", True): [("too few", 5, 0), ("short", 6, 3), ("too few", 5, 0), ("short", 6, 3)],
}


def test_her_settee_requests_at_eight_begin_with_the_starboard_watch_and_wait_with_the_larboard():
    """Her design's §14 ("every settee request begins at her company of eight") and §16 risk 7,
    measured (Ext §5.3: six hands each, begun short-handed with half, `hands.SHORT_HANDED_SHARE`;
    the set and the furl aloft, which only hands who go aloft may take). Her eight are the master
    and the mate (never hands), her five seamen and the cook (an idler, on deck by day only, never
    aloft); mustered at seed 7 her starboard watch is a fore topman, a main topman and the
    afterguard's hand (the boy's sailor), three, and her larboard watch a fore topman and a main
    topman, two (the afterguard's one hand falls to the starboard). So:
    - the starboard watch begins every request short-handed with three, by night and by day (four
      for the take in and the dip by day, the cook with them); sailed from her settle with that
      watch alone (all hands piped down) at 04:00, clewed up in 169 s, set from the gear in 183 s,
      furled from set in 490 s and set from furled in 316 s, its third hand the boy, a landsman
      since the lead's ruling (8) of 2026-11-09 (old, an able seaman: 118, 128, 343 and 221 s);
    - the larboard watch's two begin none by night: "Not hands enough on deck"; by day, the cook
      up, the take in and the dip begin with three (clewed up in 184 s, set from the gear in 199 s
      sailed, its two topmen both able since the ruling; old, an able and an ordinary: 197 and
      213 s), and the furl and the loosing aloft wait for all hands ("there are but two to
      spare").
    The ruling's (9), the boy's hand to the larboard watch, is not built: it makes the watches two
    and three, not three and three, and measured in scratch the larboard then begins every request
    and the starboard none by night (docs/dev/TuningNotes.md, for the lead).
    Her design's claim ("a company of eight meets with a watch on deck of four", Ext §5.3) does
    not hold for her watches of three and two: recorded as measured and nothing tuned to make her
    quicker (§16 risk 7); for the lead. Her main-top pair is there for the loosing and the furling
    aloft (Ext §5.1): each watch's main topman is the first taken aloft."""
    from freesail.crew import hands
    from freesail.crew.model import Station, Watch
    from freesail.evolutions import EVOLUTIONS

    w = _her_world()
    crew = w.ship.extra["crew"]
    by_watch = Counter(s.watch.value for s in crew.sailors if s.station is not Station.QUARTERDECK)
    assert by_watch == {"starboard": 3, "larboard": 2, "none": 1}  # the cook keeps no watch
    for (watch, day), want in REQUESTS.items():
        deck = [
            s
            for s in crew.sailors
            if s.station is not Station.QUARTERDECK
            and s.fit
            and (s.watch is Watch(watch) or (day and s.station is Station.IDLERS))
        ]
        got = []
        for eid in ("set_settee", "take_in_settee", "furl_settee", "dip_settee"):
            evo = EVOLUTIONS[eid]
            request = hands.CrewRequest.from_mapping(evo.crew)
            aloft = any(step.aloft for step in evo.steps)
            for s in crew.sailors:
                s.at = None
            done = hands.request(crew, deck, eid, request, "main", aloft=aloft)
            got.append((done.outcome, done.wanted, done.got))
            if done.got and aloft:
                assert done.hands[0].station is Station.MAIN_TOP, (watch, eid)
        assert got == want, (watch, day, got)


@pytest.mark.parametrize(
    "knots, haul_s, lowered_s, factor",
    [(15.0, 90, 149, 1.342), (20.0, 93, 159, 1.517)],
)
def test_truth_7_198_her_settee_in_stays_is_kept_drawing_its_ourse_to_leeward_and_dipped_last(
    knots, haul_s, lowered_s, factor
):
    """Truth 7-198 (B4, on B3.3; Bil-D §14; Ext §10.3 item 1; D46 rules 2 and 3, D3 (b)), drafted
    on the fixture by B3.3 (tests/test_settee.py) and measured again here on her file, for Phase 5:
    in stays her settee is kept drawing as a ship's mizen is, its ourse braced to leeward as the
    helm goes down, and its yard is changed last, after the head yards are swung. Each rule is
    carried over by judgement from a ship's mizen (Bourdé 1765 p. 87; Steel 1794 vol. II p. 316;
    Boteler p. 163) to her settee, which Röding (1794 vol. II col. 581) has lowered and shifted
    round in going about (D1 (a)); rule 2 is pinned on her own dip, the yard lowered and passed
    round and by how many hands (D46 (d)), not against a brig.

    Her file at seed 7 from her settle (close-hauled on the starboard tack, 67.5 degrees off),
    15 and 20 kn, measured on the owner's machine at her `clr_x_m` +2.0 (her review, 2026-11-08;
    at her step 5's +2.25 each tick within a second of these): at helm's a-lee + 1 tick the
    settee set at its floor, 8 degrees, the words "haul aft the mainsail sheet and brace the ourse
    to leeward"; her after yards hauled by "Main-topsail haul." at 32 s and 28 s (the lead's
    ruling (2)(d) of 2026-11-07, as on the fixture), her fore tack risen apart, "Rise fore tack
    and sheet. Let go and haul. ..." at 90 s and 93 s (89 and 93 at +2.25; the fixture's 97 and
    96); the head yards' swing ended and the yard lowered at 149 s and 159 s ("Dip the mainsail:
    lower the yard, pass it round abaft the mast ..."; 148 and 160 at +2.25; the fixture's 155
    and 161); down in one spell of 161 and 182 ticks (`SETTEE_DIP_S` 120 by her factor of 1.342
    and 1.517; the fixture's 1.33 and 1.51), its side larboard to starboard; hoisted and
    "Tacked" at 310 s and 341 s (309 and 342 at +2.25; the fixture's 318 and 342), the report's
    tick recorded and not pinned, only its order after the hoist (D13 (a); her review); at +400 s
    on the larboard tack 67.4 and 66.5 degrees off. **Rule 2's hands:** six at
    her dip, the tack's all hands (her two fore topmen, her two main topmen, the afterguard's hand
    and the cook), the master and the mate on the quarterdeck. **Rule 5 in stays:** her settee is
    never aback from helm's a-lee to "Tacked", where her main topsail is (the static case,
    `test_rule_5_...`). Judged by her heading and tack at a set time, never by the "Tacked" line
    (D13 (a))."""
    from freesail.evolutions import scripts

    world = _her_settle(knots)
    settee = world.ship.sails[SETTEE]
    start = world.clock.tick
    world.submit("tack ship")
    world.tick()
    assert settee.is_set
    assert math.degrees(abs(settee.sheet_angle)) == pytest.approx(LUG_FLOOR_DEG, abs=1.0)
    line = next(e.text for e in _after(world, start) if "Helm's a-lee" in e.text)
    assert "haul aft the mainsail sheet and brace the ourse to leeward" in line, line
    runner = world.ship.extra["evolutions"]
    sides, lowered, backed, at_dip = [], [], 0, set()
    for i in range(2, 601):
        world.tick()
        if settee.yard_lowered:
            lowered.append(i)
            (tack,) = [x for x in runner.instances if isinstance(x.script, scripts.TackScript)]
            at_dip.add(tuple(sorted(h.station.value for h in tack.assignment.hands)))
        if settee.is_set and settee.backed:
            backed += 1
        sides.append(settee.lug_side)
        if i == 400:
            at_400 = (world.ship.dyn.tack, abs(_rel_deg(world)))
    texts = [e.text for e in _after(world, start)]
    assert "Main-topsail haul." in texts
    assert any(t.startswith("Rise fore tack and sheet. Let go and haul.") for t in texts)
    haul = _first_tick(world, start, "Let go and haul")
    swung = _first_tick(world, start, "Dip the mainsail: lower the yard")
    tacked = _first_tick(world, start, "Tacked")
    hoisted = _first_tick(world, start, "Dipped the mainsail; hoisted on the starboard side")
    assert _first_tick(world, start, "Main-topsail haul.") < haul
    assert abs(haul - haul_s) <= 5 and haul < swung
    assert lowered[0] >= swung and abs(lowered[0] - lowered_s) <= 10
    down = len(lowered)
    assert lowered == list(range(lowered[0], lowered[0] + down))  # one spell, not two
    assert abs(down - scripts.SETTEE_DIP_S * factor) <= 10
    assert sides[0] == "larboard" and sides[-1] == "starboard"
    assert hoisted is not None and tacked is not None and tacked >= hoisted  # the order alone
    assert at_dip == {
        ("afterguard", "fore_top", "fore_top", "idlers", "main_top", "main_top")
    }  # rule 2: six of her eight, the posts on the quarterdeck
    assert backed == 0  # rule 5: never aback in her tack
    assert at_400[0] == "larboard" and abs(at_400[1] - 67.5) <= 5.0


@pytest.mark.parametrize("knots, crossed_s, hoisted_s", [(15.0, 58, 153), (20.0, 48, 168)])
def test_truth_7_199_in_wearing_her_settee_is_lowered_as_she_bears_up_and_hoisted_past_the_wind(
    knots, crossed_s, hoisted_s
):
    """Truth 7-199 (B4, on B3.3; Bil-D §14; Ext §10.3 item 2; D46 (d) rule 4 as reworded), drafted
    on the fixture by B3.3 and measured again here on her file, for Phase 5: in wearing her settee
    is lowered as she bears up and hoisted again on the new lee once her stern is past the wind.
    Steel's order for a ship's mizen (1794 vol. II pp. 321-322: hauled up as she bears up, hauled
    out "as soon as the stern has passed the wind"), carried over by judgement to the dip D1 (a)
    gives the settee; the truth pins the order of events, not a clewing up.

    Her file at seed 7 from her settle, 15 and 20 kn, measured at her `clr_x_m` +2.0 (her review,
    2026-11-08): lowered at "up helm" + 1 tick ("Up helm; lower the mainsail; brace in the after
    yards"); the wind across her stern to the larboard quarter at 58 s and 48 s (57 and 48 at her
    step 5's +2.25; the fixture's 66 and 55); hoisted at 153 s and 168 s (the fixture's 152 and
    168), the wind then 120.5 and 121.7 degrees on her larboard side (121.4 and 120.4 at +2.25)
    ("Hoisted the mainsail on the starboard side, to leeward of the mast; the wind is past the
    stern."); "Wore" at 472 s and 517 s (472 and 516 at +2.25; the fixture's 478 and 520), the
    report's tick recorded and not pinned, only its order after the hoist (her review); at +600 s
    on the larboard tack 67.5 and 67.4 degrees off. Judged by her heading and tack at a set time
    (D13 (a))."""
    world = _her_settle(knots)
    settee = world.ship.sails[SETTEE]
    start = world.clock.tick
    world.submit("wear ship")
    lowered, crossed, hoist = [], None, None
    for i in range(1, 601):
        world.tick()
        rel = _rel_deg(world)
        if settee.yard_lowered:
            lowered.append(i)
        if crossed is None and rel < 0 and abs(rel) > 90:
            crossed = i
        if hoist is None and lowered and not settee.yard_lowered:
            hoist = (i, rel)
        if i == 600:
            at_600 = (world.ship.dyn.tack, abs(rel))
    up = next(e.text for e in _after(world, start) if "Up helm" in e.text)
    assert "Up helm; lower the mainsail; brace in the after yards" in up, up
    assert lowered and lowered[0] <= 5
    assert abs(crossed - crossed_s) <= 10 and abs(hoist[0] - hoisted_s) <= 10
    assert hoist[0] > crossed and hoist[1] < 0.0  # the wind on the new side of the stern
    texts = [e.text for e in _after(world, start)]
    assert (
        "Hoisted the mainsail on the starboard side, to leeward of the mast; the wind is past the "
        "stern." in texts
    )
    wore = _first_tick(world, start, "Wore")
    assert wore is not None and wore > hoist[0]  # the order alone (D13 (a))
    assert settee.is_set and settee.lug_side == "starboard"
    assert at_600[0] == "larboard" and abs(at_600[1] - 67.5) <= 5.0


def test_her_first_hour_at_seed_7_under_her_rules_captain_with_no_fit_named(tmp_path):
    """Her design's §11 and §14 (after B3.3, since before it she got under way as a lugger): what is
    common to any scenario of hers, built with no scenario file of hers (B6's, out to a
    supplemental package). With no fit named she is unarmed, her default (`make_world(7, her file,
    Scenario())`: no gun, no fit, and an hour with nothing refused). A scenario written from its
    fields by the harbour's maker (the great guns' with her file in the frigate's place, British,
    bound for Plymouth, her road home, a British merchant brig in sight bound for Falmouth) reads
    back to itself and loads with no fit named; she sails it at seed 7 under her rules captain by
    the merchant's book, the stranger under a merchant's, and no order of hers refused; saved at
    half an hour and loaded from the checkpoint, she carries on as the world that was never saved.
    Measured (2026-11-08): on passage, shaping a course for Plymouth; her eight set her plain sail
    by her watch one sail at a time, the last at about 2,700 s; an hour in, 4.38 kn in the
    westerly of ten knots, heading 60 degrees."""
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

    bare = make_world(7, HER, Scenario())
    bare.run(3600)
    assert bare.ship.fit == "" and bare.ship.guns == {}
    assert not [e for e in bare.log if e.kind == "order.rejected"]
    _text, fields = read_scenario_text(
        ROOT / "data" / "scenarios" / "exercising-the-great-guns.yaml"
    )
    fields = copy.deepcopy(fields)
    fields["name"] = "A bilander bound for Plymouth"
    fields.pop("standing_orders")  # her rules captain's book alone
    fields["ship"]["file"] = HER
    fields["intent"] = "bound for Plymouth"
    assert "fit" not in fields["ship"]
    fields["ships"] = [
        {
            "description": "merchant brig",
            "name": "Stranger",
            "nation": "britain",
            "position": "49 45 N 5 20 W",
            "goal": "bound for Falmouth",
            "intent": "bound for Falmouth",
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
    assert world.ship.fit == "" and world.ship.guns == {}
    assert world.captain.commands and world.captain.role == "merchant"
    stranger = world.vessels.find("Stranger")
    assert stranger.ship_file == "data/ships/merchant-brig.yaml"
    assert stranger.brain.role == "merchant"
    world.run(1800)
    saved = replay_mod.save_to_file(world, tmp_path / "hers.json")
    world.run(1800)
    assert not [e for e in world.log if e.kind == "order.rejected"]
    assert all(world.ship.sails[s].is_set for s in world.ship.groups["plain sail"])
    assert units.ms_to_knots(world.ship.dyn.speed) == pytest.approx(4.38, abs=0.3)
    loaded, how = replay_mod.load(saved, ship_factory)
    assert how == "checkpoint" and loaded.ship.fit == ""
    loaded.run(1800)
    assert loaded.clock.tick == world.clock.tick and loaded.state() == world.state()
