"""Package 90, the tartane: the whole lateen's shared cut, `tools/ships/lateen.py`
(docs/design/Plan-Package90.md §7.1, §7.2: the tartane's builder fills it and merges it alone,
before the polacre's and the xebec's rigs are written).

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
from pathlib import Path

import pytest

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
