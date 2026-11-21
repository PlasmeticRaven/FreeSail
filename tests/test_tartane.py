"""Package 90, the tartane: the whole lateen's shared cut, `tools/ships/lateen.py`, and her two
files, `data/ships/tartane.yaml` (the trader) and `data/ships/coastguard-tartane.yaml` (the
guarda-costa of the same hull), written by `tools/ships/tartane.py` (docs/design/
Design-Ship-Tartane.md, Tar-D; her measuring, docs/design/ships-design/pages-tartane.md, Pages;
docs/design/Plan-Package90.md §7.1, §7.2, §8.1: the tartane's builder fills `lateen.py` and merges
it alone, before the polacre's and the xebec's rigs are written).

Her truths, 7-681 to 7-689 (Tar-D §13's T-1 to T-9), are drafted here under their numbers where
they hold on the tree as it stands, each a state: 7-681 (T-1) and 7-688 (T-8); and 7-695, from the
spare, her watch by night (the lead's nudge 38, question 4). The others wait on
the engine's steps not yet merged and stay drafted in her design's §13: 7-682 (T-2, a point nearer
the wind than a square-rigger: A8 tunes the lateen row, and A1a gives her lateen its bad hand;
measured today she lies 60 degrees off making 1.91 kn to windward where the merchant brig holds
63.75 making 1.89, a third of a point), 7-683 (T-3, her tack and wear with her yards shifted or
left: A1a to A1c, re-measured after A1d), 7-684 (T-4, the bad hand and `shift the mainsail`:
A1a), 7-685 (T-5, hove to with her topsail a topsail: A5 and A6), 7-686 (T-6, the gale: A8, with
A1a's lateen evolutions), 7-687 (T-7, her great sail's all-hands call: A1a) and 7-689 (T-9, taken
aback: A1d, with A1c's wear over 22 knots).

`lateen.py` is pure: it imports nothing of the generator or the game, has no `build` and is
named by no `SHIP_MODULES` row. Its cut is a whole lateen's (docs/design/Design-Ship-Tartane.md
§4.1, Design-Ship-Polacre.md §4.3, Design-Ship-Xebec.md §4.2): the yard slung a third of its
length from the car on the mast's raked line, the head the yard less its ends (Forfait 1788 p.
121), three-cornered (Lescallier p. 378) and written with four corners `[tack, throat, peak,
clew]` for the drawing, the tack a short luff under the throat; Lescallier p. 379's lines; and its
checks each raised in words.
"""

from __future__ import annotations

import ast
import importlib.util
import math
import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from freesail.ship.loader import load_ship, load_spec
from freesail.ship.parts import SailState
from freesail.world import captains
from freesail.world import ships as S
from freesail.world.ships import polar_of

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def lateen():
    """`tools/ships/lateen.py`, imported as a module on its own (it imports nothing of the
    generator)."""
    spec = importlib.util.spec_from_file_location(
        "lateen_under_test", ROOT / "tools" / "ships" / "lateen.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _mast(rake_deg=0.0, x=4.0, deck=1.0):
    """A mast's raked line: x at a height above the water, `rake_deg` positive aft."""
    return lambda z: x - math.tan(math.radians(rake_deg)) * (z - deck)


# A round lateen for the cut's own tests: a 24-m yard at 50 degrees slung 9 m above the water on a
# mast standing upright at x 4, a third of a metre at the car and half a metre at the penne.
YARD = {"yard_m": 24.0, "car_end_m": 0.3, "penne_end_m": 0.5, "yard_deg": 50.0, "sling_z": 9.0}


def test_the_lateens_cut_is_pure_imports_nothing_of_the_game_and_has_no_build():
    tree = ast.parse((ROOT / "tools" / "ships" / "lateen.py").read_text(encoding="utf-8"))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported |= {a.name.split(".")[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom):
            imported.add((node.module or "").split(".")[0])
    assert imported == {"__future__", "math"}
    names = {n.name for n in tree.body if isinstance(n, ast.FunctionDef)}
    assert names == {"area_centroid", "meet", "_positive", "cut", "lines", "check"}
    assert "build" not in names
    assert "whole lateen's cut" in ast.get_docstring(tree)


def test_the_yard_is_slung_a_third_from_the_car_on_the_masts_raked_line(lateen):
    for rake in (-3.0, 0.0, 10.0):
        mast = _mast(rake)
        c = lateen.cut(**YARD, mast_x_at=mast, luff_m=0.3, leech_m=18.0, foot_m=14.0)
        car, penne, sling = c["car"], c["penne"], c["sling"]
        assert math.dist(car, penne) == pytest.approx(24.0)
        assert math.dist(car, sling) == pytest.approx(8.0)  # a third of 24 m
        assert sling == pytest.approx((mast(9.0), 9.0))
        # the penne aft and up at the yard's angle
        assert math.degrees(math.atan2(penne[1] - car[1], car[0] - penne[0])) == pytest.approx(50)


def test_the_head_is_the_yard_less_its_ends_and_the_tack_a_luff_under_the_throat(lateen):
    c = lateen.cut(**YARD, mast_x_at=_mast(), luff_m=0.3, leech_m=18.0, foot_m=14.0)
    tack, throat, peak, clew = c["corners"]
    assert c["head"] == pytest.approx(23.2)
    assert math.dist(throat, peak) == pytest.approx(23.2)
    assert math.dist(c["car"], throat) == pytest.approx(0.3)
    assert math.dist(c["penne"], peak) == pytest.approx(0.5)
    assert tack == pytest.approx((throat[0], throat[1] - 0.3))
    assert c["luff"] == 0.3


def test_the_clew_is_where_the_leech_and_the_foot_meet_the_lower_or_the_point_given(lateen):
    c = lateen.cut(**YARD, mast_x_at=_mast(), luff_m=0.3, leech_m=18.0, foot_m=14.0)
    tack, _, peak, clew = c["corners"]
    assert math.dist(peak, clew) == pytest.approx(18.0)
    assert math.dist(tack, clew) == pytest.approx(14.0)
    other = max(lateen.meet(tack, 14.0, peak, 18.0), key=lambda p: p[1])
    assert clew[1] < other[1]  # the lower of the two
    assert (c["leech"], c["foot"]) == pytest.approx((18.0, 14.0))
    given = lateen.cut(**YARD, mast_x_at=_mast(), luff_m=0.3, clew=(-4.0, 1.5))
    assert given["corners"][3] == (-4.0, 1.5)
    assert given["leech"] == pytest.approx(math.dist(given["corners"][2], (-4.0, 1.5)))


def test_the_area_and_the_centre_are_the_corners_by_the_shoelace(lateen):
    c = lateen.cut(**YARD, mast_x_at=_mast(), luff_m=0.3, clew=(-4.0, 1.5))
    tack, throat, peak, clew = c["corners"]

    # a quadrilateral, split on the tack-peak diagonal
    def tri(a, b, d):
        return abs((b[0] - a[0]) * (d[1] - a[1]) - (d[0] - a[0]) * (b[1] - a[1])) / 2

    assert c["area"] == pytest.approx(tri(tack, throat, peak) + tri(tack, peak, clew))
    assert lateen.area_centroid([(0, 0), (4, 0), (4, 3), (0, 3)]) == pytest.approx((12, 2, 1.5))


def test_lescalliers_lines_of_a_whole_lateen(lateen):
    assert lateen.lines("main.lateen_yard", "main.lateen") == [
        ("main.lateen_yard.jeers", "halyard", "main.lateen_yard", None),
        ("main.lateen_yard.ourse.starboard", "guy", "main.lateen_yard", "starboard"),
        ("main.lateen_yard.ourse.larboard", "guy", "main.lateen_yard", "larboard"),
        ("main.lateen_yard.oste.starboard", "vang", "main.lateen_yard", "starboard"),
        ("main.lateen_yard.oste.larboard", "vang", "main.lateen_yard", "larboard"),
        ("main.lateen_yard.van.starboard", "vang", "main.lateen_yard", "starboard"),
        ("main.lateen_yard.van.larboard", "vang", "main.lateen_yard", "larboard"),
        ("main.lateen.sheet", "sheet", "main.lateen", None),
        ("main.lateen.tack", "tack", "main.lateen", None),
    ]


def test_the_cuts_refusals_are_said_in_words(lateen):
    mast = _mast()
    base = dict(YARD, mast_x_at=mast, luff_m=0.3, leech_m=18.0, foot_m=14.0)
    cases = [
        (dict(yard_deg=0.0), "rises aft at more than nothing and less than upright"),
        (dict(yard_deg=90.0), "rises aft at more than nothing and less than upright"),
        (dict(luff_m=0.0), "the lateen's luff is 0.0; it is more than nothing."),
        (dict(yard_m=-1.0), "the lateen's yard is -1.0; it is more than nothing."),
        (dict(car_end_m=-0.1), "the lateen yard's end at the car is -0.1; it is nothing or more."),
        (dict(car_end_m=9.0), "reach past its sling"),
        (dict(leech_m=1.0, foot_m=1.0), "cannot meet"),
        (dict(clew=(0.0, 1.0)), "the lateen's clew is given twice"),
        (dict(leech_m=None), "the lateen's clew is not given"),
    ]
    for change, words in cases:
        with pytest.raises(ValueError, match=re.escape(words)):
            lateen.cut(**{**base, **change})


def test_the_checks_hold_a_true_cut_and_raise_each_fault_in_words(lateen):
    mast = _mast()
    c = lateen.cut(**YARD, mast_x_at=mast, luff_m=0.3, leech_m=18.0, foot_m=14.0)
    written = lateen.lines("main.lateen_yard", "main.lateen")
    kw = dict(mast_x_at=mast, aft_x=-12.0, sail_id="main.lateen", yard_m=24.0, ends=(0.3, 0.5))
    lateen.check(c, written, **kw)
    lateen.check(c, written, **kw, deck_at=lambda x: 1.0)
    # the sling off the mast's raked line
    with pytest.raises(ValueError, match="slung \\+0.50 m off the mast's raked line"):
        lateen.check(c, written, **{**kw, "mast_x_at": _mast(x=3.5)})
    # the head not the yard less its ends
    with pytest.raises(ValueError, match="the head is the yard less its ends"):
        lateen.check(c, written, **{**kw, "yard_m": 25.0})
    # the peak abaft the farthest its sheet leads
    with pytest.raises(ValueError, match="the lateen's peak stands at x"):
        lateen.check(c, written, **{**kw, "aft_x": 0.0})
    # a corner under the deck
    with pytest.raises(ValueError, match="under her deck there"):
        lateen.check(c, written, **kw, deck_at=lambda x: 5.0)
    # a luff of nothing
    flat = dict(c, corners=[c["corners"][1], *c["corners"][1:]])
    with pytest.raises(ValueError, match="the lateen's tack stands on its throat"):
        lateen.check(flat, written, **kw)
    # a sheet sided, two sheets, no tack
    sided = [ln for ln in written if ln[1] != "sheet"] + [
        ("main.lateen.sheet.starboard", "sheet", "main.lateen", "starboard")
    ]
    with pytest.raises(ValueError, match="the lateen has 1 sheets, sided \\['starboard'\\]"):
        lateen.check(c, sided, **kw)
    two = [*written, ("main.lateen.sheet2", "sheet", "main.lateen", None)]
    with pytest.raises(ValueError, match="the lateen has 2 sheets"):
        lateen.check(c, two, **kw)
    tackless = [ln for ln in written if ln[1] != "tack"]
    with pytest.raises(ValueError, match="the lateen has 0 tacks"):
        lateen.check(c, tackless, **kw)


# ---------------------------------------------------------------------------
# Her two files: the generator's report, the hull, the rig, her company, her guns, her rows
# ---------------------------------------------------------------------------

HER = "data/ships/tartane.yaml"
GUARD = "data/ships/coastguard-tartane.yaml"
PIED = 0.3248


@pytest.fixture(scope="module")
def built(tmp_path_factory):
    """Her module run as the generator runs it (`gen_ships` the running script), into a scratch
    folder: her files and her report."""
    out = tmp_path_factory.mktemp("tartane")
    probe = (
        "import sys\n"
        "sys.path.insert(0, 'tools')\n"
        "import gen_ships\n"
        "from ships import tartane\n"
        "tartane.build(sys.argv[1])\n"
    )
    run = subprocess.run(
        [sys.executable, "-c", probe, str(out)],
        check=True,
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    return out, run.stderr


def _report(stderr, words):
    return [line for line in stderr.splitlines() if words in line]


def test_her_module_writes_her_two_files_byte_for_byte_as_committed(built):
    out, _ = built
    assert sorted(p.name for p in out.iterdir()) == ["coastguard-tartane.yaml", "tartane.yaml"]
    for name in ("tartane.yaml", "coastguard-tartane.yaml"):
        assert (out / name).read_bytes() == (ROOT / "data" / "ships" / name).read_bytes(), name


@pytest.mark.parametrize("path", [HER, GUARD])
def test_her_files_load_with_no_warning_every_part_rated(path):
    spec = load_spec(path)
    assert spec.warnings == []
    ship = load_ship(path)
    assert all(sp.rating_kn > 0.0 for sp in spec.spars)
    assert all(ln.rating_kn > 0.0 for ln in ship.lines.values())
    p = polar_of(path)
    assert all(v >= 0.0 for row in p.speeds_kn for v in row)


@pytest.mark.parametrize("path", [HER, GUARD])
def test_her_hull_is_her_drawn_body_on_h_outside_the_plank(path, built):
    """Tar-D §2 with the lead's rulings of 2026-11-20 (nudges 29 and 30): every figure on H, the
    line the sheet marks; her displacement the body as drawn outside the plank, Chapman's body to
    H with its keel (135.2 t moulded: Pages §4.3) and a plank of 2½ pouces (JUDGEMENT), the range
    2 to 3 pouces in her report."""
    hull = load_spec(path).hull
    assert (hull.length_waterline_m, hull.draught_m, hull.lateral_area_m2) == (18.47, 2.38, 40.9)
    assert (hull.hull_speed_kn, hull.deck_height_m, hull.gm_m) == (10.4, 0.54, 0.8)
    assert hull.beam_m == round(20 * PIED + PIED / 3, 2) == 6.6
    assert hull.displacement_kg == 142200.0
    _, stderr = built
    stem = Path(path).stem
    line = _report(stderr, f"{stem}: her body drawn to H")[0]
    assert "135.2 t moulded" in line and "142.2 t outside the plank, filed" in line
    assert "140.8 to 143.6 t on 2 to 3 pouces" in line
    drawn = _report(stderr, f"{stem}: the hull as drawn (freesail/ship/form.py): drawn displ")[0]
    assert "drawn displacement 143 t against the filed 142 t (+1%)" in drawn


def test_her_profile_is_chapmans_plate_at_her_scale_with_the_plank():
    """Tar-D §3 (Pages §6): every line of the plate at her scale on H, rung S† (stand-in), each
    half-breadth the plate's moulded one and the plank; the war tartane's four ports a side only
    in the coastguard's file, the trader no war tartane."""
    plank = 2.5 / 12 * PIED
    for path in (HER, GUARD):
        prof = load_spec(path).hull.profile
        assert prof.rail_m[0] == (-9.72, 3.3) and prof.rail_m[-1] == (10.38, 3.67)
        assert prof.keel_m == ((-8.91, -2.43), (0.0, -2.38), (6.71, -2.32))
        assert prof.stem_m[-1] == (10.58, 4.74) and prof.stern_m[3] == (-9.23, 0.0)
        midship = [t for t in prof.breadth_m if t[0] == -0.23][0]
        assert midship[1] == pytest.approx(3.27 + plank, abs=0.006)
        marks = dict(prof.marks)
        assert marks["rail_m"] == marks["breadth_m"] == "stand-in"
        assert prof.form.stern.type == "round" and prof.form.head == "knee"
    assert load_spec(HER).hull.profile.ports_m == ()
    ports = dict(load_spec(GUARD).hull.profile.ports_m)["upper"]
    assert [(x, s) for x, s, _ in ports] == [
        (-4.66, 1.37),
        (-1.94, 1.11),
        (3.21, 1.18),
        (5.93, 1.57),
    ]
    assert dict(load_spec(GUARD).hull.profile.port_size_m)["upper"] == (0.52, 0.54)


def test_her_masts_and_yards_hold_forfaits_table_ii():
    """Truth 7-681's figures (T-1): her masts, yards and places within rounding of Forfait 1788
    Table II's Humble (read on the page image: Tar §2.1), the pied du roi 0.3248 m; the topgallant
    the Humble carries left out (Tar-D §4.1)."""
    spars = {s.id: s for s in load_spec(HER).spars}
    assert spars["main.lateen_yard"].length_m == round(75 * PIED, 2)
    assert spars["main.topsail.yard"].length_m == round(32 * PIED, 2)
    assert spars["main.treou.yard"].length_m == round(41 * PIED, 2)
    assert spars["mizzen.lateen_yard"].length_m == round(47 * PIED, 2)
    assert spars["bowsprit"].length_m == round(10.5 * PIED, 2)
    assert "main.topgallant.yard" not in spars and "main.topmast" not in spars


def test_her_main_stands_upright_by_the_owners_rule_one_figure():
    """Her main's rake, one figure in her module (the owner's rule of 2026-11-20: the better
    sailing of upright and slightly forward, measured: docs/dev/TuningNotes.md, the tartane's
    section): upright, as Chapman's Pl. LXII No. 16 draws a tartane's main; her mizen raked aft
    10 degrees (JUDGEMENT on Forfait p. 128)."""
    spars = {s.id: s for s in load_spec(HER).spars}
    assert spars["main.mast"].rake_deg is None
    assert spars["mizzen.mast"].rake_deg == 10.0
    assert spars["main.mast"].x_m == 3.87  # Forfait's 10 pieds 5 pouces before the middle


def test_her_great_lateen_is_cut_by_forfaits_rule_and_her_sail_is_his(built):
    """Tar-D §4.1, §4.5 (Forfait p. 121): the great lateen's head the yard less its ends, its yard
    slung a third from the car on the main's raked line at its hounds and peaked so that the car
    is tacked at the stem, its clew on the deck at the mast's foot (her design's reading, R); the
    mizen lateen 'semblable' (Forfait pp. 124-125), its clew at its own mast's foot, its peak inside
    the outrigger's end; her plain sail checked against the Humble's 2,237½ square pieds less his
    topgallant's 20 m² (JUDGEMENT), within ±15%: 216.1 m², +0.0%."""
    spec = load_spec(HER)
    sails = {s.id: s for s in spec.sails}
    great = sails["main.lateen"]
    assert great.cls == "lateen" and not great.cut_at_mast and not great.dipping
    tack, throat, peak, clew = great.corners_m
    assert math.dist(throat, peak) == pytest.approx((75 - 2.25) * PIED, abs=0.02)
    assert clew == (3.87, 0.31)  # the deck at the main's foot, above the datum
    assert tack[0] == throat[0] and throat[1] - tack[1] == pytest.approx(0.3)
    _, stderr = built
    assert _report(stderr, "tartane: the great yard peaked 34.4 degrees to tack its car")
    assert _report(stderr, "tartane: her plain sail 216.1 m² against Forfait's 236.0 m²")
    plain = sum(sails[s].area_m2 for s in load_ship(HER).groups["plain sail"])
    assert plain == 216
    assert (sails["main.lateen"].area_m2, sails["mizzen.lateen"].area_m2) == (79, 26)
    assert (sails["main.topsail"].area_m2, sails["jib"].area_m2) == (77, 34)


def test_her_groups_are_her_designs_and_name_no_courses():
    """Tar-D §4.4: plain sail the two lateens, the topsail and the jib; all sail those and the
    tréou; no "courses" (her lateen is no course). Her design's "lateens" group waits on A1b,
    which builds the orders that name it and adds the family to the standing book's (truth
    7-625)."""
    ship = load_ship(HER)
    g = ship.groups
    assert set(g["plain sail"]) == {"main.lateen", "main.topsail", "mizzen.lateen", "jib"}
    assert set(g["all sail"]) == set(g["plain sail"]) | {"main.treou"}
    assert "courses" not in g and "lateens" not in g
    assert ship.aliases["mainsail"] == "main.lateen" and ship.aliases["mizen"] == "mizzen.lateen"
    sails = {s.id: s for s in load_spec(HER).sails}
    assert sails["main.treou"].flying and sails["main.treou"].cls == "square"
    assert not sails["main.bouffette"].bent and sails["main.bouffette"].in_place_of == "main.lateen"


def test_her_companies_ten_and_thirty_four_the_trader_french_the_guarda_costa_spanish():
    """Tar-D §6: the trader's ten, the master and the mate each heading a watch (ruling 11), six
    able seamen, the boy and the cook; the guarda-costa's thirty-four. The trader's names are
    from the french list (her design's §6.4, the lead's nudge 38), which reads her as France's,
    and the guarda-costa's from the spanish (package 90's N1), which reads her as Spain's. Old
    (71dd278): both spanish."""
    trader, guard = load_spec(HER).crew, load_spec(GUARD).crew
    assert (trader.complement, guard.complement) == (10, 34)
    assert (trader.names, guard.names) == ("french", "spanish")
    assert [p.post for p in trader.posts] == [p.post for p in guard.posts] == ["master", "mate"]
    trader_stations = sum(trader.stations.values())
    guard_stations = sum(guard.stations.values())
    assert (trader_stations, guard_stations) == (8, 32)


def test_her_trader_is_watched_three_able_seamen_a_side_the_boy_to_the_starboard():
    """The lead's nudge 41, point 3: her complement's words say what her bill draws, for a player
    reads the muster. Her design's §6.1 has six able seamen, three a watch, in watches of three
    seamen, four with the boy. Her stations four and three: the muster watches the forecastle's
    four two a side and the afterguard's two able seamen one a side, its odd hand, the boy, to the
    starboard (freesail/crew/muster.py, rule 3); and her file's words say so. Old (8998c08): the
    forecastle three and the afterguard four, watched four able seamen to the starboard and two
    with the boy to the larboard, under words of "two watches of three"."""
    import random

    from freesail.crew.model import Rating, Watch
    from freesail.crew.muster import muster

    spec = load_spec(HER).crew
    stations = {st: n for st, n in spec.stations.items() if n}
    assert stations == {"forecastle": 4, "afterguard": 3, "idlers": 1}
    crew = muster(spec, random.Random(7))
    able = [
        len([s for s in crew.sailors if s.watch is watch and s.rating is Rating.ABLE])
        for watch in (Watch.STARBOARD, Watch.LARBOARD)
    ]
    assert able == [3, 3]
    boys = [(s.station.value, s.watch) for s in crew.sailors if s.rating is Rating.ORDINARY]
    assert boys == [("afterguard", Watch.STARBOARD)]
    words = (ROOT / HER).read_text(encoding="utf-8")
    assert "six able seamen in two watches of three, a boy in the starboard watch, and a" in words


@pytest.mark.parametrize(
    ("path", "nation", "names"), [(HER, "france", "french"), (GUARD, "spain", "spanish")]
)
def test_each_of_her_files_reads_as_its_lists_nation_with_no_nation_given(path, nation, names):
    """The lead's nudge 38, question 6, by truth 7-680's measure: her scenario giving no nation,
    the trader reads as France's and her people carry French names, and the guarda-costa as
    Spain's with Spanish names. A Frenchman's people do not read as Spain's. Each given name as
    the muster writes it (`muster.abbreviate`, a muster book's short forms, which turn the french
    list's Charles into "Chas."). Old (71dd278): the trader read as Spain's, her people Spanish."""
    from freesail.api.session import make_world
    from freesail.core.world import Scenario
    from freesail.crew.muster import abbreviate

    lists = yaml.safe_load((ROOT / "data" / "crew" / "names.yaml").read_text(encoding="utf-8"))
    given_written = {abbreviate(g) for g in lists[names]["given"]}
    world = make_world(7, path, Scenario())
    assert world.scenario.nation is None
    assert world.dealings.ship_nation == nation
    for sailor in world.ship.extra["crew"].sailors:
        given, surname = sailor.name.split(" ", 1)
        assert given in given_written and surname in lists[names]["surnames"], sailor.name


def test_the_guarda_costas_guns_are_chapmans_in_the_war_tartanes_ports():
    """Tar-D §7 (package 81's checklist): eight long 4-pounders, one in each of the war tartane's
    four ports a side, each at its port's sill, and four swivels on the rail aft; drawn by the
    viewer's one rule (`tools/check_viewer_guns.py` clean); the trader unarmed, no armament."""
    from freesail.api import viewer_guns  # noqa: F401  (the check's own rule)

    assert load_spec(HER).armament is None
    arm = load_spec(GUARD).armament
    assert arm.default == "long guns"
    guns = arm.fits["long guns"].guns
    longs = [g for g in guns if g.kind == "long"]
    assert len(longs) == 8 and {g.pounder for g in longs} == {4.0}
    ports = {x: sill for x, sill, _ in dict(load_spec(GUARD).hull.profile.ports_m)["upper"]}
    assert all(ports[g.x_m] == g.height_m for g in longs)
    assert len([g for g in guns if g.kind == "swivel"]) == 4
    run = subprocess.run(
        [sys.executable, "tools/check_viewer_guns.py", HER, GUARD],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert run.returncode == 0 and run.stdout.strip().endswith("clean"), run.stdout


def test_her_descriptions_rows_and_words_rank_her_the_cutters_class():
    """Tar-D §8, §9: 'a tartane' at four miles; the trader 'a tartane, a coaster under her great
    lateen, deep laden', a merchant, unarmed; the guarda-costa 'a King's tartane, armed, a
    guarda-costa', the revenue role, her long guns; each ranked the cutter's class by every
    reading; her words, Falconer's and Steel's 'tartan', the Spanish 'tartana' and James's
    'garda-costa'."""
    for key, path, fit, roles in (
        ("tartane", HER, "unarmed", ["merchant"]),
        ("guarda-costa tartane", GUARD, "long guns", ["revenue"]),
    ):
        d = S.description(key)
        assert (d["file"], d["rig"], d["fit"], d["roles"]) == (path, "a tartane", fit, roles)
        readings = [
            captains.SIZE_RANK.get(key),
            captains.size_rank_of(key),
            captains.size_of_words(d["rig"]),
            captains.size_of_words(d["what"]),
            captains.size_rank_of(d["what"]),
            captains.size_of_file(d["file"]),
        ]
        assert readings == [1] * 6, key
    assert "King's" in S.description("guarda-costa tartane")["what"]
    for words, key in (
        ("a tartan", "tartane"),
        ("tartana", "tartane"),
        ("a garda-costa", "guarda-costa tartane"),
    ):
        assert S.description_key(words) == key


# ---------------------------------------------------------------------------
# Her truths that hold on the tree as it stands: 7-681 (T-1), 7-688 (T-8) and 7-695
# ---------------------------------------------------------------------------


def test_truth_7_681_her_particulars_hold_their_sources():
    """T-1 (Tar-D §13): her particulars hold their sources. Her length and breadth Forfait's
    Humble (62¾ by 20⅓ pieds; Table II, read on the page image), her masts and yards his within
    rounding, their places his from the middle of her perpendiculars (x +0.49 in her frame: Pages
    §6.4); her lines Chapman's Pl. LVII No. 16 at her scale, lengths by 1.100 and sections by 1.268
    (Pages §3.4): her waterline 18.47 m and her draught 2.38 m on H, her drawn displacement within
    Pages §4.3's ±6% of the filed."""
    spec = load_spec(HER)
    spars = {s.id: s for s in spec.spars}
    assert round(62.75 * PIED, 2) == 20.38 and spec.hull.beam_m == round((20 + 1 / 3) * PIED, 2)
    for sid, pieds in (
        ("main.lateen_yard", 75),
        ("main.topsail.yard", 32),
        ("mizzen.lateen_yard", 47),
        ("bowsprit", 10.5),
    ):
        assert spars[sid].length_m == pytest.approx(pieds * PIED, abs=0.005), sid
    assert spars["main.mast"].x_m == pytest.approx(0.49 + (10 + 5 / 12) * PIED, abs=0.01)
    assert spars["mizzen.mast"].x_m == pytest.approx(
        0.49 - (15 + 2 / 12) * PIED - math.tan(math.radians(10.0)) * (0.54 - 0.93), abs=0.01
    )
    # the main: 59 pieds heel to head, its heel on a keelson over the keel's upper edge
    main_head = -2.12 + 0.25 + 59 * PIED  # above the water, upright
    assert spars["main.mast"].height_m == pytest.approx(main_head - 0.54, abs=0.01)
    assert spec.hull.length_waterline_m == pytest.approx(56.55 * 0.2969 * 1.1003, abs=0.01)
    assert spec.hull.draught_m == pytest.approx(6.317 * 0.2969 * 1.2682, abs=0.01)
    drawn = 135.2 / 0.94, 135.2 / 1.06
    assert drawn[1] * 1000 < spec.hull.displacement_kg < drawn[0] * 1000 * 1.06


def test_truth_7_688_before_the_wind_the_treou_set_adds_way_the_great_lateen_taken_in_for_it():
    """T-8 (Tar-D §13; Lescallier p. 401: the tréou set with the wind aft; Falconer 1780, TREOU):
    running dead before 15 knots of wind, her great lateen taken in and her tréou set flying on
    its yard, she runs faster than under plain sail. Measured on the tree as it stands (seed 7):
    4.69 kn under plain sail; 4.35 with the great lateen taken in; 4.86 with the tréou set."""
    from tests.test_known_truths import knots, make, run, settle

    w = make(HER, 180.0, 15.0, 4.0)
    settle(w, ["call all hands", "set plain sail", "square the yards"], sail_wait=1800, ticks=1200)
    plain = knots(w)
    assert w.ship.sails["main.treou"].state is SailState.FURLED
    w.submit("take in the mainsail")
    run(w, 600, trim_every=120)
    lateen_in = knots(w)
    assert w.ship.sails["main.lateen"].state is SailState.IN_THE_GEAR
    w.submit("set the treou")
    run(w, 900, trim_every=120)
    assert w.ship.sails["main.treou"].state is SailState.SET
    assert knots(w) > plain > lateen_in


LIE_TO = 'standing order "lie to": when the true wind exceeds 10 knots then heave to'
FILL = 'standing order "fill": when the true wind is below 8 knots then fill away'


def test_truth_7_695_by_night_her_watch_heaves_to_and_fills_away_all_hands_called_if_too_few():
    """The lead's nudge 38, question 4: her watch by night, measured now that package 119 is
    merged, as truth 7-704 is the merchant brig's. The number is 7-695, from the spare: 7-681 to
    7-689 are T-1 to T-9's, each written or waiting. The trader off the Lizard by night
    (tests/test_hands.py's trader at seed 7, 02:00). Her ten: the master and the mate head the
    larboard and the starboard watch; six able seamen and the boy are in the watches; the cook is
    an idler. With her stations four and three (the lead's nudge 41, point 3), the bill draws three
    able seamen and the boy to the starboard, and three able seamen to the larboard: her design's
    §6.1, watches of three seamen, four with the boy. (Filed three and four before, it drew four
    able seamen to the starboard, and two and the boy to the larboard: the same counts.)

    Heaving to and filling away want twelve by their files; the company's clamp gives her eight,
    and as manoeuvres they take no post. Each calls all hands where the watch on deck is under
    half of that (`too_few: all hands`, package 119):
    - the larboard's three are too few. By the player's order and by a standing order (to lie
      to over ten knots; to fill away under eight, the wind falling to six), all hands are called
      once for each. She is hove to (in 76 s, before the watch below is up, so "All hands on
      deck." is not said) and filled away (in 181 s, the watch below up at 90 s), and the hands
      are piped down with the larboard watch on deck;
    - the starboard's four are half of eight, not too few. The watch begins each itself, short,
      four of eight, and nobody is called or piped down.
    Nothing waits and nothing fails on either watch.

    Her file gives no `hands:` of her own. The bilander's six (0dbd4fc, taken out at b4e814c),
    measured on this tree, make either watch begin both short and call no one: they are not put
    back. Recorded, not asserted: filled away, she lies 20 to 45 degrees off the wind at about a
    knot, her topsail left in the gear, since her heave-to hauls it up as a course and filling
    away does not set it again (A5: her topsail a topsail). Set again, it steadies her on her
    course at 3.8 kn."""
    from freesail import units
    from freesail.crew.bill import Watch
    from tests.test_hands import asked, trader_at

    assert not (load_spec(HER).hands or {})
    for watch, on_deck in ((Watch.STARBOARD, 4), (Watch.LARBOARD, 3)):
        too_few = watch is Watch.LARBOARD
        for eid in ("heave_to", "fill_away"):
            w, crew, runner = trader_at(HER, 2, watch)
            assert len([s for s in crew.sailors if s.watch is watch]) == on_deck
            if eid == "fill_away":
                w.ship.extra["hove_to"] = {"tack": "starboard", "backed": ["main"]}
            inst = asked(w, eid, None)
            assert runner._take_hands(w.ship, inst, crew), (watch, eid, inst.wait_line)
            assert inst.wait_line == "" and inst.all_hands is too_few, (watch, eid)
            if not too_few:
                got = inst.assignment
                assert (got.got, got.wanted, got.outcome) == (4, 8, "short"), (watch, eid)
        # the two roads, in the world: the player's orders and standing orders
        for given in ("heave to", LIE_TO):
            road = (watch, given)
            w, crew, _runner = trader_at(HER, 2, watch)
            for sid in w.ship.groups["plain sail"]:
                w.ship.sails[sid].state = SailState.SET
            w.ship.dyn.heading = units.deg_to_rad(215.0)
            w.ship.dyn.speed = units.knots_to_ms(5.0)
            w.submit("steer 215")
            w.run(400)
            t0 = w.clock.tick
            w.submit(given)
            w.run(600)
            ev = [e for e in w.log if e.tick >= t0]
            if given != "heave to":
                assert [e.text for e in ev if e.text.startswith("By standing order")] == [
                    "By standing order 'lie to': heaving to."
                ], road
            called = [e.text for e in ev if e.kind == "crew.all_hands"]
            assert called == (["All hands! (to heave to)"] if too_few else []), road
            assert not [e for e in ev if e.kind == "crew.all_hands_up"], road
            assert not [e for e in ev if e.kind in ("evolution.waiting", "evolution.failed")]
            hove = [e.tick for e in ev if e.kind == "ship.hove_to"]
            piped = [e for e in ev if e.kind == "crew.piped_down"]
            assert len(hove) == 1 and "hove_to" in w.ship.extra, road
            if too_few:
                assert [e.text for e in piped] == [
                    f"Piped down; the {watch.value} watch has the deck."
                ], road
                assert piped[0].tick >= hove[0], road
            else:
                assert not piped, road
            assert crew.watch_on_deck is watch and not crew.all_hands_called, road
            # and filled away again
            t1 = w.clock.tick
            if given == "heave to":
                w.submit("fill away")
            else:
                w.submit(FILL)
                w.wind.speed = w.wind.base_speed = units.knots_to_ms(6.0)  # the wind falls
            w.run(900)
            ev = [e for e in w.log if e.tick >= t1]
            if given != "heave to":
                assert [e.text for e in ev if e.text.startswith("By standing order")] == [
                    "By standing order 'fill': filling away."
                ], road
            called = [e.text for e in ev if e.kind == "crew.all_hands"]
            assert called == (["All hands! (to fill away)"] if too_few else []), road
            up = [e.kind for e in ev if e.kind == "crew.all_hands_up"]
            assert up == (["crew.all_hands_up"] if too_few else []), road
            assert not [e for e in ev if e.kind in ("evolution.waiting", "evolution.failed")]
            filled = [e.tick for e in ev if e.kind == "ship.filled_away"]
            piped = [e for e in ev if e.kind == "crew.piped_down"]
            assert len(filled) == 1 and "hove_to" not in w.ship.extra, road
            if too_few:
                assert [e.text for e in piped] == [
                    f"Piped down; the {watch.value} watch has the deck."
                ], road
                assert piped[0].tick >= filled[0], road
            else:
                assert not piped, road
            assert crew.watch_on_deck is watch and not crew.all_hands_called, road
