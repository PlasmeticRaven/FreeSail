"""Package 75, SW-2b.1: the generator's helpers for the hull's shape (docs/design/Build-Ships.md
§5.0, §5.1, §5.3, §5.6).

Stage 0H put the shape keys in the ship file's form, and `freesail/ship/form.py` draws the hull
from them. These are the helpers through which every ship's builder writes them, and no ship
file changes with them (the two-way byte test, `tests/test_ship_particulars.py`):
- `g.hull_profile` takes the six lines of points as parts, and refuses the form and the marks,
  which are `g.hull_form`'s;
- `g.hull_form` adds the form and the marks as given, metres to the centimetre and a band's
  count of lights whole, and refuses in the schema's words what the load would refuse. It
  writes no computed figure into a ship's notes (the lead's notes of 2026-10-29, item 2): it
  gives the generator's report the drawn displacement and depth beside the filed ones and each
  port triple's gap to the drawn side at its sill: a gap over 0.05 m raises for a triple the ship
  measured and is reported for any other, and no triple is ever moved (§5.0 principle 8);
- `g.midship_section` makes a section by Steel's sweeps, simplified, through its inputs;
- `g.from_steel_table` turns one of Steel's bodies tables into a stand-in's main breadth and
  section points, scaled by §5.0 principle 7; on Steel's 36 it gives the pages note's figures;
- `Builder.dump` writes the form's mappings as blocks and `sections_m` one station to a line.

Every hull in those tests is built in the test; a ship file is written only into `tmp_path`.

From SW-2 and SW-2b.2 (§5.6, §15), at the end, the ship files themselves: every file's rail above
its decks and sills and a mark on every shape line; each port triple's gap to the drawn side at its
sill and the drawn displacement and depth beside the filed ones, reported; the pair check, with
`SAME_HULL_BY_INTENT`; and truth 7-185, drafted here as §15 has it, its bands old beside new.
"""

from __future__ import annotations

import copy
import functools
import importlib.util
import inspect
import itertools
import math
import subprocess
import sys
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest
import yaml

from freesail.combat.ports import PORT_PLACES
from freesail.ship import form as drawn
from freesail.ship.loader import load_ship, load_spec, spec_from_dict
from freesail.ship.profile import interp, ports_of, rail_at
from freesail.ship.schema import PROFILE_KEYS, HullForm, HullStern

ROOT = Path(__file__).resolve().parents[1]
FT = 0.3048


@pytest.fixture(scope="module")
def gen():
    """The generator as a module, not run: its helpers as a ship's module takes them."""
    spec = importlib.util.spec_from_file_location(
        "gen_ships_under_test", ROOT / "tools" / "gen_ships.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# A frigate's hull, hand-built (round figures, each line easy to reckon, not a ship's): her lines
# as `hull_profile`'s parts, every shape line among them, and one side's ports on the upper deck.
RAIL = [[-21.0, 5.0], [0.0, 4.0], [21.0, 5.0]]
BREADTH = [[-18.0, 3.0, 3.4], [0.0, 5.0, 4.6], [18.0, 2.0, 3.0]]
PARTS = {
    "keel": [[-19.0, -4.5], [17.0, -4.4]],
    "stem": [[17.0, -4.4], [20.0, -1.0], [20.5, 0.0], [21.0, 5.0]],
    "stern": [[-19.0, -4.5], [-19.5, 0.0], [-20.5, 3.0], [-21.0, 5.0]],
    "wales": [[-18.0, 0.8, 1.4], [0.0, 0.5, 1.1], [18.0, 0.9, 1.5]],
    "section": [[-4.2, 0.2], [-3.0, 2.8], [-1.5, 4.3], [0.0, 4.9], [1.0, 5.1], [4.0, 4.6]],
    "decks": {"upper": [[-18.0, 1.8], [0.0, 1.5], [18.0, 1.9]]},
    "ports": {"upper": [[-8.0, 2.2, 4.5], [0.0, 2.1, 4.9], [8.0, 2.3, 4.0]]},
    "port_size": {"upper": [0.8, 0.7]},
    "head": [[20.6, 0.5], [22.0, 3.0], [22.4, 4.6]],
    "breadth_line": [[-12.0, 1.4, 4.4], [0.0, 1.0, 5.1], [12.0, 1.6, 4.1]],
    "sections": [
        [-9.0, -2.0, 3.0],
        [-9.0, -1.0, 3.8],
        [9.0, -1.0, 3.2],
        [9.0, 0.0, 3.9],
        [9.0, 0.8, 4.2],
    ],
    "channel_wales": [[-10.0, 2.6, 3.0], [10.0, 2.7, 3.1]],
    "floor": [[-10.0, -3.6, 1.2], [0.0, -3.8, 2.0], [10.0, -3.4, 1.0]],
    "rabbet": [[-18.0, -4.2, 0.2], [16.0, -4.1, 0.2]],
}
SHAPE_PARTS = ("head", "breadth_line", "sections", "channel_wales", "floor", "rabbet")
# Her form as a builder gives it, a figure past the centimetre and a count as a float among it,
# and her marks out of the profile's order.
FORM = {
    "head": "figure",
    "stern": {
        "lights_m": [[3.6, 4.4, 6.0, 2.4]],
        "type": "square",
        "transom_hb_m": [3.0, 2.6],
        "knuckle_z_m": 3.004,
        "round_up_m": 0.3,
        "galleries_m": [[-20.5, -17.0, 3.4, 4.6]],
    },
    "fullness": [1.0, 1.2],
}
MARKS = {
    "form.head": "judged",
    "sections_m": "sourced",
    "form.stern.galleries_m": "judged",
    "rail_m": "sourced",
    "form.stern": "stand-in",
    "breadth_line_m": "rule",
    "section_m": "stand-in",
}
WRITTEN_FORM = {
    "fullness": [1.0, 1.2],
    "stern": {
        "type": "square",
        "knuckle_z_m": 3.0,
        "transom_hb_m": [3.0, 2.6],
        "round_up_m": 0.3,
        "galleries_m": [[-20.5, -17.0, 3.4, 4.6]],
        "lights_m": [[3.6, 4.4, 6, 2.4]],
    },
    "head": "figure",
}
WRITTEN_MARKS = {
    "rail_m": "sourced",
    "section_m": "stand-in",
    "breadth_line_m": "rule",
    "sections_m": "sourced",
    "form.stern": "stand-in",
    "form.stern.galleries_m": "judged",
    "form.head": "judged",
}
NOTES = {"displacement_kg": "The filed displacement.", "draught_m": "The filed draught."}
SAID = "the hull as drawn (freesail/ship/form.py): "


def _hull(gen, **changes) -> dict:
    """Her hull mapping, its profile made by `hull_profile`, a part changed or left out (None)."""
    parts = {**copy.deepcopy(PARTS), **changes}
    return {
        "length_waterline_m": 40.0,
        "beam_m": 10.0,
        "draught_m": 4.5,
        "displacement_kg": 900000.0,
        "gm_m": 1.2,
        "deck_height_m": 1.5,
        "profile": gen.hull_profile(RAIL, BREADTH, **parts),
    }


def _doc(hull: dict) -> dict:
    """A small ship of one mast on the hull given."""
    return {
        "ship": {"name": "Test", "rig": "ship"},
        "hull": copy.deepcopy(hull),
        "spars": [{"id": "main", "class": "mast", "x_m": 0.0, "height_m": 20.0, "rating_kn": 400}],
    }


def _spec(hull: dict):
    return spec_from_dict(_doc(hull), "p.yaml").hull


def _formed(gen, measured=(), **changes) -> tuple[dict, list, dict]:
    """Her hull with the form and the marks added, the generator's report `hull_form` gives and
    the gaps it returns."""
    hull, report = _hull(gen, **changes), []
    gaps = gen.hull_form(hull, form=FORM, marks=MARKS, measured=measured, report=report)
    return hull, report, gaps


def _on_the_side(gen, off: dict | None = None) -> dict:
    """The ports with each half-breadth the drawn side's at its sill to the centimetre, but the
    ones given in `off`, {x: metres}, moved out by so much."""
    hull, _report, gaps = _formed(gen)
    off = off or {}
    return {
        "upper": [
            [x, sill, round(hb + gaps[("upper", x)], 2) + off.get(x, 0.0)]
            for x, sill, hb in hull["profile"]["ports_m"]["upper"]
        ]
    }


# -- hull_profile takes the six lines of points ----------------------------------------------


def test_hull_profile_takes_the_six_shape_lines_and_not_the_form_or_the_marks(gen):
    p = gen.hull_profile(
        RAIL,
        BREADTH,
        head=[[20.6, 0.504], [22.0, 3.0]],
        sections=PARTS["sections"],
        breadth_line=PARTS["breadth_line"],
        rabbet=PARTS["rabbet"],
        floor=PARTS["floor"],
        channel_wales=PARTS["channel_wales"],
    )
    assert list(p) == ["rail_m", "breadth_m", *(f"{w}_m" for w in SHAPE_PARTS)]
    assert p["head_m"] == [[20.6, 0.5], [22.0, 3.0]]  # to the centimetre
    for word in ("form", "marks"):
        with pytest.raises(ValueError) as e:
            gen.hull_profile(RAIL, BREADTH, **{word: {}})
        said = str(e.value)
        assert said.startswith(f"hull_profile takes no part '{word}'; beside the rail and the")
        assert said.endswith(
            "rabbet; the form and the marks are hull_form's (Build-Ships.md §5.3)."
        )
        assert "form," not in said and "marks," not in said
    with pytest.raises(ValueError, match="sections_m gives one point at x 9"):
        gen.hull_profile(RAIL, BREADTH, sections=[[9.0, 0.0, 3.9]])


# -- hull_form writes what it is given, and refuses what the schema refuses -----------------


def test_hull_form_writes_the_form_and_the_marks_as_given(gen):
    hull, _report, _gaps = _formed(gen)
    before = _hull(gen)["profile"]
    p = hull["profile"]
    assert list(p) == list(PROFILE_KEYS)  # every key, the form and the marks last
    assert {k: v for k, v in p.items() if k not in ("form", "marks")} == before
    assert p["form"] == WRITTEN_FORM and list(p["form"]["stern"]) == list(WRITTEN_FORM["stern"])
    assert type(p["form"]["stern"]["lights_m"][0][2]) is int  # a count, whole
    assert p["marks"] == WRITTEN_MARKS and list(p["marks"]) == list(WRITTEN_MARKS)
    loaded = _spec(hull).profile
    assert loaded.form == HullForm(
        fullness=(1.0, 1.2),
        stern=HullStern(
            type="square",
            knuckle_z_m=3.0,
            transom_hb_m=(3.0, 2.6),
            round_up_m=0.3,
            galleries_m=((-20.5, -17.0, 3.4, 4.6),),
            lights_m=((3.6, 4.4, 6, 2.4),),
        ),
        head="figure",
    )
    assert loaded.marks == tuple(WRITTEN_MARKS.items())
    # a form or marks left out, or given None, writes none
    hull = _hull(gen)
    gen.hull_form(hull, form={"head": "knee", "fullness": None}, marks=None)
    assert hull["profile"]["form"] == {"head": "knee"} and "marks" not in hull["profile"]


SQUARE = FORM["stern"]
REFUSALS = [
    ("a key the form does not take", {"tail": 1}, None, "form has 'tail', which it does not"),
    ("a stern of another type", {"stern": {**SQUARE, "type": "flat"}}, None, "square, raked or"),
    (
        "a transom on a round stern",
        {"stern": {"type": "round", "transom_hb_m": [1.0, 1.0]}},
        None,
        "a round stern has no transom",
    ),
    (
        "a square stern with no transom",
        {"stern": {"type": "square"}},
        None,
        "is square and gives no transom_hb_m",
    ),
    (
        "the knuckle at the taffrail",
        {"stern": {**SQUARE, "knuckle_z_m": 5.0}},
        None,
        "at or above the taffrail",
    ),
    (
        "a band of half a light",
        {"stern": {**SQUARE, "lights_m": [[3.6, 4.4, 2.5, 2.4]]}},
        None,
        "a whole number of lights",
    ),
    ("a fullness of nothing", {"fullness": [0.0, 1.0]}, None, "a fullness is more than nothing"),
    ("a head of another word", {"head": "lion"}, None, "what stands on the head is none,"),
    ("a word of no rung", None, {"keel_m": "measured"}, "is marked sourced, stand-in, rule or"),
    (
        "a mark of what the profile does not give",
        {"stern": {"type": "round"}},
        {"form.stern.lights_m": "judged"},
        "'form.stern.lights_m', which is not a line",
    ),
]


@pytest.mark.parametrize("words, form, marks, match", REFUSALS, ids=[r[0] for r in REFUSALS])
def test_hull_form_refuses_in_the_schemas_words_and_leaves_the_hull_as_it_was(
    gen, words, form, marks, match
):
    hull, report = _hull(gen), []
    before = copy.deepcopy(hull)
    with pytest.raises(ValueError, match=match) as e:
        gen.hull_form(hull, form=form, marks=marks, report=report)
    assert str(e.value).startswith("hull_form: the profile's ")
    assert hull == before and report == []


def test_hull_form_wants_a_profile_and_adds_the_form_once(gen):
    with pytest.raises(ValueError, match="hull_form: the hull has no profile; hull_profile makes"):
        gen.hull_form({"length_waterline_m": 40.0}, form=FORM, marks=None)
    hull, _report, _gaps = _formed(gen)
    with pytest.raises(ValueError, match="has its form or its marks already; hull_form adds them"):
        gen.hull_form(hull, form=None, marks={"rail_m": "sourced"})


def test_a_drawing_that_misses_a_given_point_is_refused(gen):
    """`form.check`'s own refusal, a main breadth above the rail, raised from `hull_form`."""
    hull = _hull(gen, breadth_line=[[-12.0, 1.4, 4.4], [0.0, 4.5, 5.1], [12.0, 1.6, 4.1]])
    with pytest.raises(ValueError, match="^hull_form: the drawn side misses breadth_line_m's poi"):
        gen.hull_form(hull, form=None, marks=None)
    assert "form" not in hull["profile"]


# -- the report: the drawn hull beside the file's figures, in no note; the gap rule ----------


def test_hull_form_reports_the_drawn_hull_beside_the_files_figures_and_writes_no_note(gen):
    """The lead's notes of 2026-10-29, item 2: a ship's notes carry sources, departures and
    judgements, and a figure a rule computes from the file's own keys belongs in the generator's
    report and the tests. So `hull_form` takes no notes. It gives its report the drawn displacement
    beside the filed one and the drawn depth beside the draught, as `form.check` gives them; each
    port's gap to the drawn side at its sill, the drawn half-breadth less the triple's, aft to
    forward, those over 0.05 m named; the triples themselves as they were."""
    assert "notes" not in inspect.signature(gen.hull_form).parameters
    hull, report, gaps = _formed(gen)
    spec = _spec(hull)
    lines = drawn.check(spec)
    assert report[0] == f"{SAID}{lines[0]}."
    assert report[1] == f"{SAID}{lines[1]}."
    assert lines[0].startswith("drawn displacement") and "the file's draught of 4.5 m" in lines[1]
    triples = PARTS["ports"]["upper"]
    assert hull["profile"]["ports_m"]["upper"] == triples  # never moved
    expected = {("upper", x): drawn.half_breadth_at(spec, x, sill) - hb for x, sill, hb in triples}
    assert gaps == expected
    figures = ", ".join(f"{round(g, 2) + 0.0:+.2f}" for g in expected.values())
    line = report[2]
    assert line.startswith(f"{SAID}the upper deck's ports: the side at each sill, aft to forward")
    assert f"off the half-breadth by {figures} m" in line
    over = [f"{x:g}" for (_w, x), g in expected.items() if abs(g) > 0.05]
    assert over  # the hand-built ports stand off her drawn side
    assert f"; more than 0.05 m at x {', '.join(over)}, reported" in line
    assert "measured" not in line
    # with no report asked for it does the same work and says nothing
    quiet = _hull(gen)
    assert gen.hull_form(quiet, form=FORM, marks=MARKS) == gaps
    assert quiet == hull


def test_a_measured_triple_off_the_drawn_side_raises_and_any_other_is_reported(gen):
    """§5.3: a gap over 0.05 m raises for a triple named in `measured`, by its deck or by its
    deck and x, and is reported for every other; within it a measured triple passes. No triple
    is ever moved to the drawing, and `measured` names only triples the profile gives."""
    on = _on_the_side(gen)
    hull, report, gaps = _formed(gen, measured=("upper",), ports=on)
    assert all(abs(g) <= 0.005 for g in gaps.values())
    assert "; the 3 measured each within 0.05 m." in report[2]
    off = _on_the_side(gen, {8.0: 0.2})
    for measured in (("upper",), [("upper", 8.0)], [("upper", 8.004)]):
        with pytest.raises(ValueError) as e:
            _formed(gen, measured=measured, ports=off)
        assert str(e.value).startswith(
            "hull_form: the drawn side misses a measured port triple by more than 0.05 m at its "
            "sill: the upper port at x 8, -0.20 m."
        )
    hull, report, gaps = _formed(gen, measured=[("upper", 0.0), ("upper", -8.0)], ports=off)
    assert gaps[("upper", 8.0)] == pytest.approx(-0.2, abs=0.006)
    assert hull["profile"]["ports_m"]["upper"] == off["upper"]  # never moved
    assert "; more than 0.05 m at x 8, reported and never moved to the drawing" in report[2]
    assert report[2].endswith("; the 2 measured each within 0.05 m.")
    with pytest.raises(ValueError, match="names the quarterdeck deck's ports, and the profile"):
        _formed(gen, measured=("quarterdeck",))
    with pytest.raises(ValueError, match="names the upper port at x 4, and the profile gives no"):
        _formed(gen, measured=[("upper", 4.0)])


# -- midship_section: Steel's sweeps, simplified ---------------------------------------------

# A frigate's midship section by the sweeps: Steel's 36 at dead flat, moulded (the pages note,
# ships-design/pages-steel-1805-bodies.md §3.1, §5.1): the main half-breadth 18 ft 10 in at the
# upper height of breadth, 18 ft 11 in above the base, the load line 16 ft 3 1/2 in above it and
# the top-timber line 27 ft 0 in at 16 ft 9 in; the keel's half-siding Steel's share of the
# breadth, the helper's default (0.21 m against Folio I's 8 in, 0.20 m); the deadrise and the
# bilge the hull design's fit of a floor and one arc to her diagonals at dead flat (11 degrees,
# 16 ft 9 in: measured in the session's scratch, judgement).
LOAD_36_FT = 16 + 3.5 / 12
SWEPT = {
    "half_breadth": (18 + 10 / 12) * FT,
    "breadth_z": (18 + 11 / 12 - LOAD_36_FT) * FT,
    "depth": LOAD_36_FT * FT,
    "deadrise_deg": 11.0,
    "bilge_m": 5.1,
    "tumblehome_m": (2 + 1 / 12) * FT,
    "rail_z": (27.0 - LOAD_36_FT) * FT,
}
# Her midship section at dead flat as the note gives it (§5.4: z above the load line, the
# half-breadth with 4 in of plank but at the first point, the keel's rabbet), and the plank, 4 in;
# its points from the table are the 2nd to the 7th, the five diagonals and the lower height of
# breadth (the 8th is the upper, the main breadth, and the last the top timber, the rail).
STEEL_36_SECTION = [(-4.96, 0.20), (-4.62, 2.02), (-4.17, 3.25), (-3.58, 4.02), (-2.85, 4.65),
                    (-2.05, 5.17), (0.29, 5.84), (0.80, 5.84), (3.27, 5.21)]  # fmt: skip
PLANK_36_M = 4.0 / 12.0 * FT


def test_midship_section_runs_through_its_inputs(gen):
    """The keel's edge, the floor at its deadrise, the bilge on its radius tangent to the floor
    and to the side, the side upright to the main breadth, the topside two equal arcs to the rail
    `tumblehome_m` inside it and upright there; z rising, to the centimetre."""
    sec = gen.midship_section(**SWEPT)
    zs = [z for z, _hb in sec]
    assert zs == sorted(set(zs))
    assert all(round(v, 2) == v for pt in sec for v in pt)
    y, z_b, r = SWEPT["half_breadth"], SWEPT["breadth_z"], SWEPT["bilge_m"]
    y_k = 0.036 * y  # Steel's share of the breadth (Folio I)
    assert sec[0] == [round(-SWEPT["depth"], 2), round(y_k, 2)]
    assert sec[-1] == [round(SWEPT["rail_z"], 2), round(y - SWEPT["tumblehome_m"], 2)]
    assert max(hb for _z, hb in sec) == round(y, 2)
    a = math.radians(11.0)
    z_c = -SWEPT["depth"] + (r + (y - r - y_k) * math.sin(a)) / math.cos(a)
    floor_foot = (z_c - r * math.cos(a), y - r + r * math.sin(a))
    assert sec[1] == pytest.approx(list(floor_foot), abs=0.006)
    assert math.degrees(math.atan2(sec[1][0] - sec[0][0], sec[1][1] - sec[0][1])) == (
        pytest.approx(11.0, abs=0.5)
    )
    bilge = [(z, hb) for z, hb in sec[1:] if z <= z_c + 0.005]
    assert len(bilge) >= 6  # the arc in steps of 15 degrees or less
    for z, hb in bilge:
        assert math.hypot(z - z_c, hb - (y - r)) == pytest.approx(r, abs=0.01)
    assert [round(z_c, 2), round(y, 2)] in sec and [round(z_b, 2), round(y, 2)] in sec
    top = [(z, hb) for z, hb in sec if z > z_b + 0.005]
    assert all(b[1] <= a_[1] for a_, b in zip(top, top[1:], strict=False))  # tumbling home
    halfway = [z for z, hb in top if hb == pytest.approx(y - 0.5 * SWEPT["tumblehome_m"], abs=0.01)]
    assert halfway == [pytest.approx(0.5 * (z_b + SWEPT["rail_z"]), abs=0.01)]
    # against Steel's own section at dead flat (§5.4, the plank off), at Steel's five diagonals
    # and two heights of breadth: within 0.15 m (measured: 0.14 m at the 2nd diagonal, the one
    # arc fuller there than Steel's three sweeps, and 0.08 m at the 4th and the 5th)
    for z, hb in STEEL_36_SECTION[1:8]:
        assert interp(sec, z) == pytest.approx(hb - PLANK_36_M, abs=0.15), z


def test_midship_section_flares_stands_upright_and_takes_a_keel(gen):
    shape = {**SWEPT, "tumblehome_m": -0.3}
    sec = gen.midship_section(**shape, half_siding=0.25)
    assert sec[0][1] == 0.25 and sec[-1][1] == round(SWEPT["half_breadth"] + 0.3, 2)
    assert max(hb for _z, hb in sec) == sec[-1][1]  # the rail the widest
    upright = gen.midship_section(**{**SWEPT, "tumblehome_m": 0.0})
    assert upright[-2:] == [
        [round(SWEPT["breadth_z"], 2), round(SWEPT["half_breadth"], 2)],
        [round(SWEPT["rail_z"], 2), round(SWEPT["half_breadth"], 2)],
    ]
    flat = gen.midship_section(**{**SWEPT, "deadrise_deg": 0.0, "bilge_m": 2.0})
    assert flat[0][0] == flat[1][0] and flat[1][1] == round(SWEPT["half_breadth"] - 2.0, 2)


SECTION_REFUSALS = [
    ("a floor too steep", {"deadrise_deg": 70.0}, "meets the side at z .*, above the main"),
    ("a bilge too great", {"bilge_m": 9.0}, "a bilge of radius 9 m does not fit .* at most"),
    ("a rail under the breadth", {"rail_z": 0.5}, "each stands above the last"),
    ("no depth", {"depth": 0.0}, "the depth below the water is more than nothing"),
    ("a deadrise upright", {"deadrise_deg": 90.0}, "less than upright"),
    ("a bilge less than nothing", {"bilge_m": -1.0}, "a radius is not less than nothing"),
    ("a rail of no breadth", {"tumblehome_m": 6.0}, "leaves the rail no half-breadth"),
    ("a side leaning more than it rises", {"tumblehome_m": -2.5}, "less than it rises"),
    ("a keel wider than she is", {"half_siding": 6.0}, "less than the half-breadth"),
    ("a figure not a number", {"bilge_m": "5"}, "bilge_m is '5', which is not a number"),
]


@pytest.mark.parametrize(
    "words, change, match", SECTION_REFUSALS, ids=[r[0] for r in SECTION_REFUSALS]
)
def test_midship_section_refuses_figures_that_make_no_section(gen, words, change, match):
    with pytest.raises(ValueError, match=f"^midship_section: .*{match}"):
        gen.midship_section(**{**SWEPT, **change})


def test_a_made_section_is_drawn_through_and_marked_judged(gen):
    """A made section in a profile, marked `judged` (§5.1): the schema takes it and the form draws
    the hull through it, as through a measured one."""
    sec = gen.midship_section(
        half_breadth=5.0, breadth_z=0.8, depth=4.2, deadrise_deg=14.0, bilge_m=2.2,
        tumblehome_m=0.4, rail_z=4.0,
    )  # fmt: skip
    hull = _hull(gen, section=sec, sections=None, breadth_line=None)
    gen.hull_form(hull, form=None, marks={"section_m": "judged"})
    spec = _spec(hull)
    assert spec.profile.section_m == tuple(tuple(pt) for pt in sec)
    assert drawn.check(spec)


# -- from_steel_table: a stand-in from Steel's bodies ----------------------------------------

# Steel's 36, "the frigate of 36 guns and 877 tons", as the pages note reads her
# (docs/design/ships-design/pages-steel-1805-bodies.md): the load line above the base, 16 ft
# 10 in at AP (x -20.88) and 15 ft 10 in at FP (x +20.88), straight (§5.1); the diagonals'
# heights up the middle line and their ends, the 1st to the 3d on the base and the 4th to the
# 6th on the side line 18 ft 10 in out (§3.1); and by timber aft to forward, x (§5.2), the lower
# and upper heights of breadth, the main half-breadth and the 1st to 6th diagonals (§3.1, as read
# on the page image; None, Steel's blank). Timber 29's heights of breadth are as printed (the
# note's probable misprint, the lower above the upper).
STEEL_36 = {
    "water": [[-20.88, "16 10"], [20.88, "15 10"]],
    "diagonals": [
        ["8 0", ["7 4", "0 0"]],
        ["12 0", ["13 2", "0 0"]],
        ["15 8", ["18 1", "0 0"]],
        ["19 2½", ["18 10", "3 8½"]],
        ["22 2", ["18 10", "7 10½"]],
        ["28 0", ["18 10", "11 8"]],
    ],
    "timbers": [
        ["30", -20.02, "22 11", "23 1½", "13 7", ["0 8", "1 2", "2 3", "4 6", "7 4½", "13 5½"]],
        ["29", -19.28, "22 9", "22 6", "14 0", ["1 1½", "2 0", "3 8", "6 3½", "9 2½", "14 9½"]],
        ["27", -17.81, "21 8½", "22 1", "15 0",
         ["1 11½", "3 6½", "5 9½", "8 9½", "11 8", "16 7¼"]],
        ["25", -16.33, "20 11½", "21 6", "15 9", ["2 10", "5 0", "7 7½", "10 8", "13 5½", "18 0"]],
        ["23", -14.86, "20 4", "20 11", "16 5", ["3 9", "6 4", "9 2", "12 3", "14 11", "19 2"]],
        ["19", -11.91, "19 3", "20 1½", "17 5",
         ["5 6½", "8 9½", "11 10½", "14 9½", "17 2½", None]],
        ["15", -8.97, "18 5", "19 5½", "18 1½", ["7 1", "10 10", "13 10½", "16 8", "18 9", None]],
        ["11", -6.02, "17 9½", "19 1", "18 6½", ["8 3", "12 5", "15 5½", "18 8", "19 11", None]],
        ["7", -3.07, "17 5½", "18 10½", "18 9",
         ["8 10", "13 4", "16 4¼", "18 10¾", "20 8", None]],
        ["⊕", 2.11, "17 3", "18 11", "18 10", ["9 4", "13 11½", "17 0", "19 4", "20 10½", None]],
        ["C", 5.77, "17 4¼", "18 11½", "18 10", ["9 3", "13 9", "16 10", "19 1½", "20 9", None]],
        ["G", 8.71, "17 9¼", "19 1", "18 10", ["8 10", "13 1", "16 2¼", "18 8", "20 5", None]],
        ["L", 11.66, "18 6½", "19 6½", "18 5½",
         ["7 11¼", "11 10½", "14 11½", "17 7½", "19 6", None]],
        ["P", 14.61, "19 11", "20 7½", "17 1½",
         ["6 6½", "9 10½", "12 10¾", "15 7½", "17 7½", None]],
        ["T", 17.54, "22 1½", "22 6", "13 9", ["4 2", "6 9½", "9 4½", "11 9½", "13 8½", None]],
        ["W", 19.01, "23 8", "23 11¼", "10 7½", ["2 1", "4 4½", "6 6½", "8 8", "10 4", None]],
        ["X", 19.75, "24 7", "24 9½", "8 3", ["0 8", "2 8½", "4 7", "6 5½", "7 11", None]],
    ],
}  # fmt: skip


def _fi(s: str) -> float:
    """Feet and inches as Steel prints them, in feet (the test's own reading)."""
    s = s.replace("¼", ".25").replace("½", ".5").replace("¾", ".75")
    feet, inches = s.split()
    return float(feet) + float(inches) / 12.0


def _load_36(x: float) -> float:
    return _fi("16 10") + (x + 20.88) / 41.76 * (_fi("15 10") - _fi("16 10"))


def test_from_steel_table_gives_the_notes_figures_for_steels_36(gen):
    """At each timber the main breadth is the upper height of breadth above the load line at the
    main half-breadth; at dead flat the section's points are the note's midship section (§5.4),
    moulded; every diagonal Steel prints and every lower height of breadth gives one point, low
    to high; both lines marked `stand-in`."""
    parts, marks = gen.from_steel_table(STEEL_36, length_ratio=1.0, beam_ratio=1.0)
    assert marks == {"breadth_line_m": "stand-in", "sections_m": "stand-in"}
    assert list(parts) == ["breadth_line", "sections"]
    timbers = STEEL_36["timbers"]
    assert parts["breadth_line"] == [
        [x, pytest.approx((_fi(upper) - _load_36(x)) * FT, abs=0.005),
         pytest.approx(_fi(main) * FT, abs=0.005)]
        for _t, x, _lower, upper, main, _d in timbers
    ]  # fmt: skip
    by_x: dict[float, list[tuple[float, float]]] = {}
    for x, z, hb in parts["sections"]:
        by_x.setdefault(x, []).append((z, hb))
    assert list(by_x) == [t[1] for t in timbers]
    for _t, x, _lower, _upper, _main, diagonals in timbers:
        points = by_x[x]
        assert len(points) == sum(d is not None for d in diagonals) + 1
        assert [z for z, _hb in points] == sorted(z for z, _hb in points)
    dead_flat = [(z, hb - PLANK_36_M) for z, hb in STEEL_36_SECTION[1:7]]
    assert by_x[2.11] == [pytest.approx(pt, abs=0.011) for pt in dead_flat]  # both rounded
    assert parts["breadth_line"][9] == pytest.approx([2.11, 0.80, 5.84 - PLANK_36_M], abs=0.006)
    # timber 29's misprint as printed: the lower height of breadth above the upper, one breadth
    assert (pytest.approx(1.82, abs=0.005), 4.27) in by_x[-19.28]
    assert parts["breadth_line"][1][1:] == [pytest.approx(1.74, abs=0.005), 4.27]


def test_from_steel_table_scales_lengths_by_the_waterlines_and_sections_by_the_beams(gen):
    """§5.0 principle 7: x by the waterlines' ratio; the heights above the water and the
    half-breadths by the beams', one factor, so that the floor's and the tumblehome's angles
    are kept; the depth so drawn the table's by the beams'."""
    plain, _marks = gen.from_steel_table(STEEL_36, length_ratio=1.0, beam_ratio=1.0)
    scaled, _marks = gen.from_steel_table(STEEL_36, length_ratio=0.9, beam_ratio=1.08)
    for key in ("breadth_line", "sections"):
        assert len(scaled[key]) == len(plain[key])
        for (x, z, hb), (sx, sz, shb) in zip(plain[key], scaled[key], strict=True):
            assert sx == pytest.approx(x * 0.9, abs=0.0051)
            assert sz == pytest.approx(z * 1.08, abs=0.011)
            assert shb == pytest.approx(hb * 1.08, abs=0.011)
    with pytest.raises(ValueError, match="beam_ratio is 0; a ratio is more than nothing"):
        gen.from_steel_table(STEEL_36, length_ratio=1.0, beam_ratio=0)
    # an angle in a section is kept: the 1st diagonal's points of dead flat and of timber 30
    for x in (2.11, -20.02):
        a, b = [pt for pt in plain["sections"] if pt[0] == x][:2]
        c, d = [pt for pt in scaled["sections"] if pt[0] == pytest.approx(x * 0.9, abs=0.006)][:2]
        assert math.atan2(b[1] - a[1], b[2] - a[2]) == pytest.approx(
            math.atan2(d[1] - c[1], d[2] - c[2]), abs=0.02
        )


def test_from_steel_tables_parts_draw_a_stand_in(gen):
    """The parts as `hull_profile` takes them and the marks as `hull_form` does: on Steel's 36's
    own plan (§5.2's water and rail, moulded) her table's points are drawn through, as sourced
    points are (§5.0 principle 5). Her displacement is the test's (judgement): the drawn one is
    recorded beside it, not asserted."""
    parts, marks = gen.from_steel_table(STEEL_36, length_ratio=1.0, beam_ratio=1.0)
    plan = [  # §5.2: x, the rail's height, the half-breadths at the water and at the rail
        (-20.02, 4.27, 1.31, 3.72), (-19.28, 4.20, 2.37, 3.84), (-17.81, 4.09, 3.72, 4.05),
        (-16.33, 3.96, 4.35, 4.24), (-14.86, 3.85, 4.72, 4.42), (-11.91, 3.67, 5.19, 4.70),
        (-8.97, 3.52, 5.47, 4.90), (-6.02, 3.41, 5.63, 5.04), (-3.07, 3.33, 5.70, 5.09),
        (2.11, 3.27, 5.73, 5.11), (5.77, 3.29, 5.73, 5.11), (8.71, 3.33, 5.71, 5.11),
        (11.66, 3.43, 5.55, 5.03), (14.61, 3.54, 5.03, 4.81), (17.54, 3.70, 3.73, 4.14),
        (19.01, 3.81, 2.52, 3.38), (19.75, 3.89, 1.65, 2.77),
    ]  # fmt: skip
    hull = {
        "length_waterline_m": 41.76,
        "beam_m": 11.68,
        "draught_m": 5.44,
        "displacement_kg": 1_300_000.0,
        "gm_m": 1.3,
        "profile": gen.hull_profile(
            [[x, rail] for x, rail, _hw, _hr in plan],
            [[x, hw, hr] for x, _rail, hw, hr in plan],
            keel=[[-20.88, -5.59], [20.88, -5.28]],  # Folio I's draughts (§5.3)
            section=[STEEL_36_SECTION[0]]
            + [[z, hb - PLANK_36_M] for z, hb in STEEL_36_SECTION[1:]],
            **parts,
        ),
    }
    report = []
    gen.hull_form(hull, form=None, marks={"breadth_m": "stand-in", **marks}, report=report)
    spec = _spec(hull)
    for x, z, hb in spec.profile.sections_m + spec.profile.breadth_line_m:
        assert drawn.half_breadth_at(spec, x, z) == pytest.approx(hb, abs=0.001), (x, z)
    assert "against the file's draught of 5.44 m" in report[1]


FROM_TABLE_REFUSALS = [
    (
        "timbers out of order",
        lambda t: t["timbers"].insert(0, t["timbers"].pop(3)),
        r"timber 30 at x -20.02 is not forward of timber 25 \(x -16.33\); the timbers run aft",
    ),
    (
        "a diagonal missing",
        lambda t: t["timbers"][0][5].pop(),
        "timber 30 gives 5 diagonals and the table 6; give None where Steel leaves one blank",
    ),
    (
        "a figure not Steel's",
        lambda t: t["timbers"][0].__setitem__(4, "13 ft 7"),
        "timber 30, '13 ft 7' is not feet and inches as Steel prints them",
    ),
]


@pytest.mark.parametrize(
    "words, change, match", FROM_TABLE_REFUSALS, ids=[r[0] for r in FROM_TABLE_REFUSALS]
)
def test_from_steel_table_refuses_a_table_it_cannot_read(gen, words, change, match):
    table = copy.deepcopy(STEEL_36)
    change(table)
    with pytest.raises(ValueError, match=f"^from_steel_table: {match}"):
        gen.from_steel_table(table, length_ratio=1.0, beam_ratio=1.0)


# -- the dump --------------------------------------------------------------------------------


def test_the_dump_writes_the_form_as_blocks_and_the_sections_a_station_a_line(gen, tmp_path):
    hull, _report, _gaps = _formed(gen)
    notes = dict(NOTES)
    notes.update(
        {
            "profile.sections_m": "The sections, measured.",
            "profile.form": "The form.",
            "profile.form.stern": "The stern, a stand-in.",
            "profile.marks": "The rungs.",
        }
    )
    b = gen.Builder("Test", "ship", "A test.", hull, hull_notes=notes)
    b.spar("main", "mast", x_m=0.0, height_m=20.0, rating_kn=400.0)
    path = tmp_path / "test.yaml"
    b.dump(str(path), "# A test.\n")
    text = path.read_text(encoding="utf-8")
    assert (
        "    # The sections, measured.\n"
        "    sections_m: [[-9.0, -2.0, 3.0], [-9.0, -1.0, 3.8],\n"
        "                 [9.0, -1.0, 3.2], [9.0, 0.0, 3.9], [9.0, 0.8, 4.2]]\n"
        "    channel_wales_m: [[-10.0, 2.6, 3.0], [10.0, 2.7, 3.1]]\n"
    ) in text
    assert (
        "    # The form.\n"
        "    form:\n"
        "      fullness: [1.0, 1.2]\n"
        "      # The stern, a stand-in.\n"
        "      stern:\n"
        "        type: square\n"
        "        knuckle_z_m: 3.0\n"
        "        transom_hb_m: [3.0, 2.6]\n"
        "        round_up_m: 0.3\n"
        "        galleries_m: [[-20.5, -17.0, 3.4, 4.6]]\n"
        "        lights_m: [[3.6, 4.4, 6, 2.4]]\n"
        "      head: figure\n"
        "    # The rungs.\n"
        "    marks:\n"
        "      rail_m: sourced\n"
        "      section_m: stand-in\n"
        "      breadth_line_m: rule\n"
        "      sections_m: sourced\n"
        "      form.stern: stand-in\n"
        "      form.stern.galleries_m: judged\n"
        "      form.head: judged\n"
        "spars:\n"
    ) in text
    assert "  # The filed displacement.\n" in text and "The hull as drawn" not in text
    assert yaml.safe_load(text)["hull"]["profile"] == hull["profile"]
    assert load_ship(path).spec.hull.profile == _spec(hull).profile


# -- SW-2 with SW-2b.2: the ship files' own lines (§5.6) -----------------------------------------

SHIP_FILES = sorted((ROOT / "data" / "ships").glob("*.yaml"))
SHIP_NAMES = [path.stem for path in SHIP_FILES]
# The eight files of the packages before 75, whose lines the hull step drew.
THE_EIGHT = (
    "brig",
    "cutter",
    "frigate-36",
    "lugger",
    "merchant-brig",
    "privateer-schooner",
    "smack",
    "topsail-schooner",
)


@functools.cache
def _ship_spec(name: str):
    return load_spec(ROOT / "data" / "ships" / f"{name}.yaml")


def test_every_file_carries_a_profile_whose_rail_stands_above_its_decks_and_sills():
    for name in SHIP_NAMES:
        p = _ship_spec(name).hull.profile
        assert p is not None, name
        for word, points in p.decks_m:
            for x, z in points:
                # abaft or forward of the rail's points the side closes to the stern or the stem
                if p.rail_m[0][0] <= x <= p.rail_m[-1][0]:
                    assert z <= rail_at(p, x), (name, word, x)
        for word, triples in p.ports_m:
            for x, sill, _hb in triples:
                assert interp(dict(p.decks_m)[word], x) <= sill < rail_at(p, x), (name, word, x)


def test_a_mark_on_every_shape_line_of_every_file():
    """§5.0 principle 4: each line a file gives, each group of its form and each key of its stern
    but the stern's type says in one word where it came from."""
    for name, path in zip(SHIP_NAMES, SHIP_FILES, strict=True):
        p = yaml.safe_load(path.read_text(encoding="utf-8"))["hull"]["profile"]
        form = p["form"]
        lines = [k for k in p if k not in ("form", "marks")]
        groups = [f"form.{k}" for k in form]
        stern = [f"form.stern.{k}" for k in form.get("stern", {}) if k != "type"]
        marks = p["marks"]
        assert [k for k in lines + groups + stern if k not in marks] == [], name
        assert set(marks.values()) <= {"sourced", "stand-in", "rule", "judged"}, name


# The triples each file's sources measured, as her module's `measured` names them to `g.hull_form`
# (deck, x's): the other triples stand at the guns' own x and are reported.
MEASURED_TRIPLES = {
    "cutter": ("upper", (-4.75, -2.35, 0.02, 3.58)),  # the sheet's four ports
    "privateer-schooner": ("upper", (-10.86, -2.08, 4.81)),  # the plate's three with no gun in them
    "topsail-schooner": ("upper", (-10.86, -2.08, 4.81)),
}


def test_each_port_triples_gap_to_the_drawn_side_is_reported_and_a_measured_one_held(capsys):
    """§5.6, §5.3: the drawn side's half-breadth at each sill less the triple's, reported for the
    eight and asserted within `form.PORT_GAP_M` for a measured triple; no triple is ever moved to
    the drawing (§5.0 principle 8). The lugger and the smack have none, their sheets drawing no
    port and their guns none (§5.4, §5.7)."""
    gaps = {}
    for name in THE_EIGHT:
        hull = _ship_spec(name).hull
        gaps[name] = {
            (word, x): drawn.half_breadth_at(hull, x, sill) - hb
            for word, triples in hull.profile.ports_m
            for x, sill, hb in triples
        }
    with capsys.disabled():
        print("\nthe port triples' gaps to the drawn side, m, deck by deck, aft to forward:")
        for name, by_port in gaps.items():
            print(f"  {name}: " + (", ".join(f"{g:+.2f}" for g in by_port.values()) or "no port"))
    assert not gaps["lugger"] and not gaps["smack"]
    assert all(gaps[name] for name in THE_EIGHT if name not in ("lugger", "smack"))
    for name, (deck, xs) in MEASURED_TRIPLES.items():
        held = [g for (w, x), g in gaps[name].items() if w == deck and x in xs]
        assert len(held) == len(xs) and max(abs(g) for g in held) <= drawn.PORT_GAP_M, name


def test_the_drawn_displacement_and_depth_stand_beside_the_filed_ones(capsys):
    """§5.6, §5.0 principle 8: reported and never moved. A drawn displacement more than 15% off the
    filed one says so: the two brigs' at -27% and the smack's at -18%, which the lead's note of
    2026-10-31 has reported past the line."""
    past = set()
    with capsys.disabled():
        print("\nthe hulls as drawn, beside the files:")
        for name in SHIP_NAMES:
            hull = _ship_spec(name).hull
            displacement, depth = drawn.check(hull)[:2]
            print(f"  {name}: {displacement}; {depth}")
            assert f"against the filed {hull.displacement_kg / 1000.0:.0f} t" in displacement
            assert f"against the file's draught of {hull.draught_m:g} m" in depth
            if "more than 15% off: recorded, not moved" in displacement:
                past.add(name)
    assert past == {"brig", "merchant-brig", "smack"}


# -- the pair check (§5.6) -----------------------------------------------------------------------

# Two files may draw alike only as one class in two roles, with the owner's reason (§5.0 principle
# 10; the owner, 2026-10-28). The pair check fails any other pair.
SAME_HULL_BY_INTENT = {
    frozenset(("brig", "merchant-brig")): (
        "Keep her like the brig, for the purposes of hulls that currently are shared between navy "
        "and merchant roles, we shall consider them one class in two purposes, so the hull may "
        "stay the same between the roles for current examples."
    ),
    frozenset(("topsail-schooner", "privateer-schooner")): (
        "Alike for now, same reasoning as the brig, they are one class in two roles, so they would "
        "look alike except for where they specifically differ in details."
    ),
}
PAIR_BOX_PX = 100.0
# Judgement, re-set after the owner's first sheet, old beside new (§5.6).
PAIR_APART_PX = 4.0


def _ring(outline) -> np.ndarray:
    """An outline as a closed ring of points, `form.outline` having normalised it."""
    return np.array([*outline, outline[0]], dtype=float)


def _thin(ring: np.ndarray) -> np.ndarray:
    """The ring in pixels with a point dropped where it stands within half a pixel of the last kept,
    the end kept: an end-on outline runs to hundreds of points a few hundredths apart, and half a
    pixel is nothing beside `PAIR_APART_PX` (measured: every pair's figure as at a tenth of one,
    within 0.01 px, in little more than half the time)."""
    kept = [ring[0]]
    for point in ring[1:-1]:
        if np.hypot(*(point - kept[-1])) >= 0.5:
            kept.append(point)
    kept.append(ring[-1])
    return np.array(kept)


def _dense(ring: np.ndarray) -> np.ndarray:
    """The ring's points, and more along each edge so that none is over a pixel from the next."""
    out = [ring[:1]]
    for a, b in zip(ring[:-1], ring[1:], strict=True):
        steps = max(1, math.ceil(float(np.hypot(*(b - a)))))
        out.append(a + (b - a) * (np.arange(1, steps + 1) / steps)[:, None])
    return np.vstack(out)


def _farthest_from(points: np.ndarray, ring: np.ndarray) -> float:
    """The farthest any of the points stands from the nearest edge of the ring."""
    a, edge = ring[:-1], ring[1:] - ring[:-1]
    lengths = np.maximum((edge * edge).sum(axis=1), 1e-12)
    from_a = points[:, None, :] - a[None, :, :]
    along = np.clip((from_a * edge[None, :, :]).sum(axis=2) / lengths[None, :], 0.0, 1.0)
    off = from_a - along[:, :, None] * edge[None, :, :]
    return float(np.hypot(off[:, :, 0], off[:, :, 1]).min(axis=1).max())


def _px_apart(one, other) -> float:
    """The Hausdorff distance between two outlines, in pixels, the pair drawn in one 100-px box:
    their joint extent filling it each way."""
    a, b = _ring(one), _ring(other)
    low = np.minimum(a.min(axis=0), b.min(axis=0))
    high = np.maximum(a.max(axis=0), b.max(axis=0))
    scale = PAIR_BOX_PX / np.maximum(high - low, 1e-12)
    a, b = _thin((a - low) * scale), _thin((b - low) * scale)
    return max(_farthest_from(_dense(a), b), _farthest_from(_dense(b), a))


def _own(hull, view: str) -> np.ndarray:
    """The hull's outline in one view on her own drawn figures, as §5.6 words it ("normalised to one
    length, beam, freeboard and draught"): `form.outline` divides by her filed length, beam and
    draught, and an S hull is drawn at her sheet's, not those (§5.0 principles 5 and 8). So the
    along by her drawn water line, its middle at nought; the across by her widest half-breadth; the
    depth by her deepest point. The freeboard is `form.outline`'s, her own drawn top already."""
    stations = drawn.stations(hull)
    ends = [
        float(np.interp(0.0, [p[1] for p in s], [p[0] for p in s]))
        for s in (stations[0], stations[-1])
    ]
    widest = max(p[2] for s in stations for p in s)
    deepest = -min(p[1] for s in stations for p in s)
    ring = np.array(drawn.outline(hull, view), dtype=float)
    if view == "abeam":
        across = (ring[:, 0] * hull.length_waterline_m - 0.5 * sum(ends)) / (ends[1] - ends[0])
    else:
        across = ring[:, 0] * 0.5 * hull.beam_m / widest
    up = np.where(ring[:, 1] < 0.0, ring[:, 1] * hull.draught_m / deepest, ring[:, 1])
    return np.column_stack([across, up])


def _rings(hull) -> list[np.ndarray]:
    return [_own(hull, view) for view in drawn.VIEWS]


def _apart(rings_one, rings_other) -> list[float]:
    return [_px_apart(a, b) for a, b in zip(rings_one, rings_other, strict=True)]


def _views_apart(one, other) -> list[float]:
    return _apart(_rings(one), _rings(other))


def test_the_pair_check_reads_a_hull_by_its_lines_and_not_its_size():
    """One shape at two sizes stands nothing apart, every view being normalised to one length,
    beam, freeboard and draught on her own drawn figures (`_own`), and so does one drawing under
    another file's filed figures, which is §5.0 principle 10's silent sharing; another stem and a
    fuller section do not."""
    lines = {
        "rail_m": RAIL,
        "breadth_m": BREADTH,
        **{f"{k}_m": PARTS[k] for k in ("keel", "stem", "stern", "section")},
    }
    figures = {
        "length_waterline_m": 40.0,
        "beam_m": 10.0,
        "draught_m": 4.5,
        "displacement_kg": 900000.0,
        "gm_m": 1.2,
    }

    def spec(profile, **hull):
        return _spec({**figures, **hull, "profile": profile})

    def scaled(k_x, k_y, k_up, k_down):
        def up(z):
            return z * (k_up if z >= 0.0 else k_down)

        return {
            "rail_m": [[x * k_x, up(z)] for x, z in lines["rail_m"]],
            "breadth_m": [[x * k_x, w * k_y, r * k_y] for x, w, r in lines["breadth_m"]],
            "keel_m": [[x * k_x, up(z)] for x, z in lines["keel_m"]],
            "stem_m": [[x * k_x, up(z)] for x, z in lines["stem_m"]],
            "stern_m": [[x * k_x, up(z)] for x, z in lines["stern_m"]],
            "section_m": [[up(z), hb * k_y] for z, hb in lines["section_m"]],
        }

    plain = spec(lines)
    larger = spec(
        scaled(1.5, 1.2, 1.25, 0.8),
        length_waterline_m=60.0,
        beam_m=12.0,
        draught_m=3.6,
    )
    assert max(_views_apart(plain, larger)) < 0.01
    assert max(_views_apart(plain, plain)) < 1e-9
    # the same lines, not scaled, under another file's figures (the stations' grid moving with her
    # filed length, under a pixel): on the filed figures this stood far apart and passed
    filed_otherwise = spec(lines, length_waterline_m=31.0, beam_m=7.5, draught_m=3.0)
    assert max(_views_apart(plain, filed_otherwise)) < PAIR_APART_PX / 2.0
    raked = copy.deepcopy(lines)
    raked["stem_m"] = [[17.0, -4.4], [18.0, -1.0], [18.5, 0.0], [24.0, 5.0]]
    assert _views_apart(plain, spec(raked))[0] >= PAIR_APART_PX
    fuller = copy.deepcopy(lines)
    fuller["section_m"] = [
        [-4.2, 3.0],
        [-3.0, 4.6],
        [-1.5, 4.9],
        [0.0, 5.0],
        [1.0, 5.1],
        [4.0, 4.6],
    ]
    assert max(_views_apart(plain, spec(fuller))) >= PAIR_APART_PX


def test_the_pair_check_fails_one_drawing_under_two_files_figures():
    """§5.0 principle 10: the cutter's profile given point for point to the smack, her filed figures
    kept, is one drawing, and the check must see it. On the filed figures (`form.outline` alone) it
    stood 14.84, 12.93 and 14.69 px apart and passed (the landing's review, by this mutation)."""
    cutter = _ship_spec("cutter").hull
    copied = replace(_ship_spec("smack").hull, profile=cutter.profile)
    assert max(_views_apart(cutter, copied)) < PAIR_APART_PX / 2.0


def test_the_pair_check_every_two_files_differ_or_stand_as_one_class_in_two_roles(capsys):
    """§5.6, §5.0 principles 1 and 10: every two files' outlines abeam, ahead and astern, in one
    100-px box, differ by `PAIR_APART_PX` or more in at least one view, or the pair stands in
    `SAME_HULL_BY_INTENT` with the owner's reason. Before the hull step every pair was 0 px
    apart; at its landing the closest pair outside the list, the cutter and the smack, stands 5.5,
    4.5 and 6.0 px apart (8.4, 4.4 and 6.2 by the filed figures, as first measured)."""
    rings = {name: _rings(_ship_spec(name).hull) for name in SHIP_NAMES}
    apart = {
        frozenset(pair): _apart(rings[pair[0]], rings[pair[1]])
        for pair in itertools.combinations(SHIP_NAMES, 2)
    }
    with capsys.disabled():
        print("\nthe pair check, px apart abeam, ahead and astern, the closest pairs:")
        for pair, px in sorted(apart.items(), key=lambda item: max(item[1]))[:6]:
            print(f"  {' and '.join(sorted(pair))}: " + ", ".join(f"{v:.1f}" for v in px))
    alike = {pair for pair, px in apart.items() if max(px) < PAIR_APART_PX}
    assert alike <= set(SAME_HULL_BY_INTENT), sorted(map(sorted, alike - set(SAME_HULL_BY_INTENT)))
    for pair, reason in SAME_HULL_BY_INTENT.items():
        assert pair <= set(SHIP_NAMES), pair
        assert "one class" in reason, pair


# -- truth 7-185 (§15), drafted here for Phase 5 to move ------------------------------------------

FT = 0.3048
# Each file's lowest sill in its source's band, metres (§5.4, §15; §5.0 principles 5 and 12: her own
# sheet decides over a rule). The lugger and the smack have no port, so no sill (§5.4, §5.7).
LOWEST_SILL_BANDS = {
    # The class's draughts, ZAZ2587 and five sheets more: port 7, 7.19 ft above WL1, ±0.05 ft, and
    # ±0.15 ft for WL1 (pages-zaz2587.md §7.1). Steel's 36's 2.34 m (Folio I), §5.4's first figure,
    # stands above it, recorded beside it and not ruled on (the lead's note of 2026-10-31, point 6).
    "frigate-36": ((7.19 - 0.20) * FT, (7.19 + 0.20) * FT),
    # OLD BESIDE NEW, the one pin this step moves (the lead's note of 2026-10-31, point 4). Old:
    # Steel 1805 p. 124's four to five feet for "sloops, cutters, &c." (OCR l. 8268-8271), 1.22-1.52
    # m, rung R, §5.4 as first written. New: 5 ft 2 in ±0.05 ft above WL1, port 5 of ZAZ4491, rung
    # S, 1.555 to 1.585 m (pages-zaz4491.md §5.7, §7), her sill 0.05 m over the old band.
    "brig": ((5.15 - 0.05) * FT, (5.15 + 0.05) * FT),
    "merchant-brig": ((5.15 - 0.05) * FT, (5.15 + 0.05) * FT),
    # Her own draught, as built: 1 ft 3 in over the deck (ZAZ6381's note), 3.32 ft above the line at
    # the sheet's port 2 on CHN0224, ±0.09 ft (pages-zaz6381.md §5.8). Steel's 1.22-1.52 m, §5.4's
    # first figure, stands above it, flagged for the owner when L2 comes (the same note, point 7).
    "cutter": ((3.32 - 0.09) * FT, (3.32 + 0.09) * FT),
    # The plate's own lowest, port 3, 3 ft 1 in, measured 3.11 ft ±0.05 (the lead's note, point 3;
    # pages-chapelle-fig17.md §5.4, §6.2), Steel's schooner's figure; Spider's 3 ft 5 in of 1835,
    # §5.4's first figure, recorded beside it.
    "privateer-schooner": ((3.11 - 0.05) * FT, (3.11 + 0.05) * FT),
    "topsail-schooner": ((3.11 - 0.05) * FT, (3.11 + 0.05) * FT),
    # ZAZ1407's 5.02 ft above WL1 and the razee by her rise (truth 7-186).
    "sixty-four": (1.53 - 0.03, 1.53 + 0.03),
    "razee-44": (1.98 - 0.03, 1.98 + 0.03),
}


def test_truth_7_185_the_generator_writes_every_file_and_every_port_gun_stands_on_its_port(
    tmp_path,
):
    """The brief's item 6, §15, on no world and no seed: the generator run into a scratch directory
    (the owner's machine, 2026-10-31). The generated set equals the committed set and each file is
    equal, compared as text. Every port gun of every fit of every file names its deck and stands on
    a triple of that deck within 0.01 m, its (x_m, height_m) to the triple's x and sill. Each file's
    lowest sill in its source's band (`LOWEST_SILL_BANDS`, the brig's old beside new): measured
    2.19, 1.57, 1.57, 1.00, 0.95, 0.95, 1.53 and 1.98 m. A new ship's sill is her own truth's until
    Phase 5 re-runs this with every file (§15)."""
    out = tmp_path / "ships"
    subprocess.run(
        [sys.executable, str(ROOT / "tools" / "gen_ships.py"), str(out)],
        check=True,
        cwd=ROOT,
        capture_output=True,
    )
    assert sorted(p.name for p in out.iterdir()) == sorted(p.name for p in SHIP_FILES)
    for path in SHIP_FILES:
        made = (out / path.name).read_text(encoding="utf-8")
        assert made == path.read_text(encoding="utf-8"), path.name
    guns_seen = 0
    for name in SHIP_NAMES:
        spec = _ship_spec(name)
        p = spec.hull.profile
        fits = spec.armament.fits if spec.armament is not None else {}
        for fit_name, fit in fits.items():
            for gun in fit.guns:
                if gun.place not in PORT_PLACES:
                    continue
                guns_seen += 1
                assert gun.deck, (name, gun.id)
                on = [
                    t
                    for t in ports_of(p, gun.deck)
                    if abs(t[0] - gun.x_m) <= 0.01 and abs(t[1] - gun.height_m) <= 0.01
                ]
                assert on, (name, fit_name, gun.id, gun.deck, gun.x_m, gun.height_m)
    assert guns_seen > 100
    for name, (low, high) in LOWEST_SILL_BANDS.items():
        p = _ship_spec(name).hull.profile
        lowest = min(sill for _word, triples in p.ports_m for _x, sill, _hb in triples)
        assert low <= lowest <= high, (name, lowest)
    for name in ("lugger", "smack"):
        assert not _ship_spec(name).hull.profile.ports_m, name
