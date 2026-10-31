"""Package 75, stage 0H: the hull's shape (docs/design/Build-Ships.md §3.5, §5.0 to §5.3, §14.1).

The profile takes eight shape keys after `port_size_m`, every one optional and drawn only: the
knee of the head, the main breadth by station, sourced section points, the channel wale, the
floor and the rabbet (kept as data, not drawn), the `form` (the ends' fullness under water, the
stern and the head) and each line's one-word `marks`. The schema refuses in words what §5.2
refuses. `freesail/ship/form.py` draws the hull from them by §5.3's rule: the side passes through
every given point within a millimetre and its ends close to the stem and the stern; a profile
without `section_m` or shape keys is drawn as §6's three points a station, as the viewer drew it
before; `/api/ship` serves the drawn stations where the file has a profile. A profile without
them pickles as before them, and nothing but the schema, the form, the server and the tools
reads them (the guard): the drawing never changes how a ship sails or fights (§5.0 principle 8).

The rule is checked against measured lines, each typed from its note with the source beside it
and built here in memory, never as a ship file: Steel's 36, the hull it was tuned on, and the 64
and *Lynx*, which it was not.
"""

from __future__ import annotations

import ast
import copy
import math
import pickle
from dataclasses import fields, replace
from pathlib import Path

import pytest

from freesail.api.queries import ship_graph
from freesail.ship import form
from freesail.ship.loader import load_ship, ship_from_dict, spec_from_dict
from freesail.ship.profile import interp
from freesail.ship.schema import (
    PROFILE_KEYS,
    SHAPE_KEYS,
    HullForm,
    HullProfile,
    HullSpec,
    HullStern,
    ShipFileError,
)

ROOT = Path(__file__).resolve().parents[1]
FT = 0.3048

# A frigate's profile with every shape key, hand-built (round figures, each line easy to
# reckon, not a ship's): a square stern with a gallery tier and a band of lights, a figure on the
# knee of the head, a breadth line amidships, two stations of sourced points, and one side's
# ports on the upper deck for the gap check.
PROFILE = {
    "rail_m": [[-21.0, 5.0], [0.0, 4.0], [21.0, 5.0]],
    "breadth_m": [[-18.0, 3.0, 3.4], [0.0, 5.0, 4.6], [18.0, 2.0, 3.0]],
    "keel_m": [[-19.0, -4.5], [17.0, -4.4]],
    "stem_m": [[17.0, -4.4], [20.0, -1.0], [20.5, 0.0], [21.0, 5.0]],
    "stern_m": [[-19.0, -4.5], [-19.5, 0.0], [-20.5, 3.0], [-21.0, 5.0]],
    "wales_m": [[-18.0, 0.8, 1.4], [0.0, 0.5, 1.1], [18.0, 0.9, 1.5]],
    "section_m": [[-4.2, 0.2], [-3.0, 2.8], [-1.5, 4.3], [0.0, 4.9], [1.0, 5.1], [4.0, 4.6]],
    "decks_m": {"upper": [[-18.0, 1.8], [0.0, 1.5], [18.0, 1.9]]},
    "ports_m": {"upper": [[-8.0, 2.2, 4.5], [8.0, 2.3, 4.0]]},
    "port_size_m": {"upper": [0.8, 0.7]},
    "head_m": [[20.6, 0.5], [22.0, 3.0], [22.4, 4.6]],
    "breadth_line_m": [[-12.0, 1.4, 4.4], [0.0, 1.0, 5.1], [12.0, 1.6, 4.1]],
    "sections_m": [
        [-9.0, -2.0, 3.0],
        [-9.0, -1.0, 3.8],
        [9.0, -1.0, 3.2],
        [9.0, 0.0, 3.9],
        [9.0, 0.8, 4.2],
    ],
    "channel_wales_m": [[-10.0, 2.6, 3.0], [10.0, 2.7, 3.1]],
    "floor_m": [[-10.0, -3.6, 1.2], [0.0, -3.8, 2.0], [10.0, -3.4, 1.0]],
    "rabbet_m": [[-18.0, -4.2, 0.2], [16.0, -4.1, 0.2]],
    "form": {
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
    },
    "marks": {
        "rail_m": "sourced",
        "breadth_m": "sourced",
        "section_m": "stand-in",
        "sections_m": "sourced",
        "breadth_line_m": "rule",
        "form.stern": "stand-in",
        "form.stern.galleries_m": "judged",
        "form.head": "judged",
    },
}
# The eight shape keys, after port_size_m (§3.5 item 1)
SHAPE = (
    "head_m",
    "breadth_line_m",
    "sections_m",
    "channel_wales_m",
    "floor_m",
    "rabbet_m",
    "form",
    "marks",
)
# The profile's fields before stage 0H, in their order: its pickled state while it has no shape
OLD_FIELDS = (
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
)


def _doc(profile: dict | None = None, **hull) -> dict:
    """A small ship of one mast with the profile given."""
    h = {
        "length_waterline_m": 40.0,
        "beam_m": 10.0,
        "draught_m": 4.5,
        "displacement_kg": 900000,
        "gm_m": 1.2,
        "deck_height_m": 1.5,
        **hull,
    }
    if profile is not None:
        h["profile"] = copy.deepcopy(profile)
    return {
        "ship": {"name": "Test", "rig": "ship"},
        "hull": h,
        "spars": [{"id": "main", "class": "mast", "x_m": 0.0, "height_m": 20.0, "rating_kn": 400}],
    }


def _hull(profile: dict, **hull) -> HullSpec:
    return spec_from_dict(_doc(profile, **hull), "p.yaml").hull


def _without(*keys: str) -> dict:
    return {k: v for k, v in copy.deepcopy(PROFILE).items() if k not in keys}


def _interp(points, x: float, i: int) -> float:
    """A line's i-th number at x, straight between its points."""
    return interp([(pt[0], pt[i]) for pt in points], x)


def _stem_x(p: HullProfile, z: float) -> float:
    """The stem's fore edge's x at height z."""
    return interp([(pt[1], pt[0]) for pt in p.stem_m], z)


def _stern_x(p: HullProfile, z: float) -> float:
    """The stern's line's x at height z."""
    return interp([(pt[1], pt[0]) for pt in p.stern_m], z)


def _on(station, z: float) -> float:
    """A drawn station's half-breadth at height z, the upper of two points at one height."""
    pts = [(pt[1], pt[2]) for pt in station]
    if z >= pts[-1][0]:
        return pts[-1][1]
    i = max(k for k, (zk, _hb) in enumerate(pts) if zk <= z)
    return interp(pts[i:], z)


def _between(spec: HullSpec, x: float, z: float) -> float:
    """The side between the aftmost station and the transom at height z, straight."""
    drawn = form.stations(spec)
    station, aft = drawn[1], drawn[0]
    x_s, x_end = station[0][0], _stern_x(spec.profile, z)
    t = (x - x_s) / (x_end - x_s)
    hb_s = _on(station, z)
    knuckle, (top, foot) = 3.0, (3.0, 2.6)
    hb_end = foot + (top - foot) * (z - knuckle) / (5.0 - knuckle)
    assert _on(aft, z) == pytest.approx(hb_end)
    return hb_s + (hb_end - hb_s) * t


# -- the keys and the form ----------------------------------------------------------------


def test_the_eight_shape_keys_follow_port_size_m():
    assert PROFILE_KEYS[: len(OLD_FIELDS)] == OLD_FIELDS
    assert PROFILE_KEYS[len(OLD_FIELDS) :] == SHAPE == SHAPE_KEYS
    assert [f.name for f in fields(HullProfile)] == list(PROFILE_KEYS)
    assert list(PROFILE) == list(PROFILE_KEYS)  # the hand-built profile gives every key


def test_the_shape_keys_load_into_the_profile_in_the_files_order():
    p = _hull(PROFILE).profile
    assert p.head_m == ((20.6, 0.5), (22.0, 3.0), (22.4, 4.6))
    assert p.breadth_line_m[1] == (0.0, 1.0, 5.1)
    assert p.sections_m[2:] == ((9.0, -1.0, 3.2), (9.0, 0.0, 3.9), (9.0, 0.8, 4.2))
    assert p.channel_wales_m[0] == (-10.0, 2.6, 3.0)
    assert p.floor_m[1] == (0.0, -3.8, 2.0) and p.rabbet_m[1] == (16.0, -4.1, 0.2)
    assert p.form == HullForm(
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
    assert isinstance(p.form.stern.lights_m[0][2], int)  # a count, whole
    assert p.marks[0] == ("rail_m", "sourced") and dict(p.marks)["form.head"] == "judged"
    with pytest.raises(AttributeError):
        p.form = None  # frozen
    # each optional: a round stern names no transom, a form may give its head alone
    lean = _without("form", "marks")
    lean["form"] = {"stern": {"type": "round", "lights_m": [[3.0, 3.6, 3, 1.2]]}}
    stern = _hull(lean).profile.form.stern
    assert (stern.type, stern.transom_hb_m, stern.knuckle_z_m) == ("round", None, None)
    lean["form"] = {"head": "none"}
    assert _hull(lean).profile.form == HullForm(head="none")


# -- §5.2's shape refusals, in words -------------------------------------------------------


def _with(path: str, value) -> dict:
    """The hand-built profile with the key, a form's key ('form.stern.type') or a stern's taken
    out (value None) or set to value."""
    p = copy.deepcopy(PROFILE)
    *parents, last = path.split(".")
    where = p
    for key in parents:
        where = where[key]
    if value is None:
        where.pop(last)
    else:
        where[last] = value
    return p


SQUARE = PROFILE["form"]["stern"]
REFUSALS = [
    # x not increasing in the breadth line, the channel wale, the floor and the rabbet; z not
    # increasing in the head
    ("the breadth line aft", "breadth_line_m", [[0.0, 1.0, 5.0], [-1.0, 1.0, 5.0]], "each x"),
    ("the breadth line stepped", "breadth_line_m", [[0.0, 1.0, 5.0], [0.0, 1.2, 5.0]], "each x"),
    ("the channel wale aft", "channel_wales_m", [[1.0, 2.6, 3.0], [0.0, 2.6, 3.0]], "each x"),
    ("the floor aft", "floor_m", [[1.0, -3.0, 1.0], [0.0, -3.0, 1.0]], "each x greater"),
    ("the rabbet aft", "rabbet_m", [[1.0, -4.0, 0.2], [0.0, -4.0, 0.2]], "each x greater"),
    ("the head down", "head_m", [[22.0, 3.0], [21.0, 1.0]], "each z greater than the last"),
    # sections_m: x decreasing, z not rising within a station, a station of one point
    (
        "the sections aft",
        "sections_m",
        [[0.0, -1.0, 4.0], [0.0, 0.0, 4.5], [-1.0, -1.0, 4.0], [-1.0, 0.0, 4.4]],
        "goes from x 0 to -1; its stations run aft to forward, each x at or forward",
    ),
    (
        "a station down",
        "sections_m",
        [[0.0, 0.0, 4.5], [0.0, -1.0, 4.0]],
        "goes from z 0 to -1 in its station at x 0; a station's points run low to high",
    ),
    (
        "a station of one point",
        "sections_m",
        [[0.0, -1.0, 4.0], [0.0, 0.0, 4.5], [3.0, 0.0, 4.0]],
        "gives one point at x 3; a station gives two or more",
    ),
    # a point of the wrong shape
    ("a section point of two", "sections_m", [[0.0, 1.0]], r"not three numbers \[x, z, hb\]"),
    ("a head point of three", "head_m", [[21.0, 1.0, 2.0]], "not two numbers"),
    ("a wale of a word", "channel_wales_m", [[0.0, 2.6, "high"]], "not three numbers"),
    # a half-breadth or half-siding not positive
    ("a main breadth of nothing", "breadth_line_m", [[0.0, 1.0, 0.0]], "a half-breadth of 0 m"),
    (
        "a section point inside out",
        "sections_m",
        [[0.0, -1.0, 4.0], [0.0, 0.0, -1.0]],
        "a half-breadth of -1 m",
    ),
    ("a floor of nothing", "floor_m", [[0.0, -3.0, 0.0]], "a half-breadth of 0 m"),
    (
        "a rabbet of nothing",
        "rabbet_m",
        [[0.0, -4.0, 0.0]],
        "has a half-siding of 0 m at .0.0, -4.0, 0.0.; a half-siding is more than nothing",
    ),
    # the form: its sub-keys and the stern's, the stern's types and the head's words
    ("a form of a list", "form", ["square"], "the profile's form is not a mapping"),
    ("a form's beak", "form.beak", "long", "form has 'beak', which it does not take; its keys"),
    ("a stern's quarter", "form.stern.quarter_m", 1.0, "form.stern has 'quarter_m', which it"),
    ("a pink stern", "form.stern.type", "pink", "has the type 'pink'; a stern is square, raked"),
    ("a stern of no type", "form.stern.type", None, "has the type None; a stern is square"),
    ("a stern of a list", "form.stern", ["square"], "form.stern is not a mapping"),
    ("a lion's head", "form.head", "lion", "form.head is 'lion'; what stands on the head is"),
    # fullness: two numbers more than nothing
    ("a fullness of one", "form.fullness", [1.0], r"not two numbers \[run, entry\]"),
    ("a word for fullness", "form.fullness", "full", "not two numbers"),
    ("a run of nothing", "form.fullness", [0.0, 1.0], "has 0; a fullness is more than nothing"),
    ("an entry less", "form.fullness", [1.0, -2.0], "has -2; a fullness is more than nothing"),
    # the transom: on a square or raked stern, never on a round one
    ("a square stern, no transom", "form.stern.transom_hb_m", None, "is square and gives no"),
    (
        "a raked stern, no transom",
        "form.stern",
        {"type": "raked", "knuckle_z_m": 3.0},
        "is raked and gives no transom_hb_m; a raked stern gives its transom's half-breadths",
    ),
    (
        "a round stern's transom",
        "form.stern",
        {"type": "round", "transom_hb_m": [3.0, 2.6]},
        "is round and gives transom_hb_m; a round stern has no transom",
    ),
    ("a transom of nothing", "form.stern.transom_hb_m", [3.0, 0.0], "a half-breadth of 0 m"),
    # the stern without stern_m; the knuckle at or above the taffrail
    ("a stern and no stern_m", "stern_m", None, "gives a stern and the profile no stern_m"),
    (
        "the knuckle at the taffrail",
        "form.stern.knuckle_z_m",
        5.0,
        "has its knuckle at 5 m, at or above the taffrail .5 m, stern_m's top.",
    ),
    ("the knuckle over it", "form.stern.knuckle_z_m", 6.5, "at or above the taffrail"),
    ("a knuckle of a word", "form.stern.knuckle_z_m", "high", "is 'high', which is not a number"),
    ("a round up of a word", "form.stern.round_up_m", True, "is True, which is not a number"),
    # a gallery tier: four numbers, aft below fore and low below high
    (
        "a tier of three",
        "form.stern.galleries_m",
        [[-20.5, -17.0, 3.4]],
        r"not four numbers \[x_aft, x_fore, z_low, z_high\]",
    ),
    (
        "a tier fore to aft",
        "form.stern.galleries_m",
        [[-17.0, -20.5, 3.4, 4.6]],
        "a tier's aft x is below its fore x and its low z below its high z",
    ),
    ("a tier upside down", "form.stern.galleries_m", [[-20.5, -17.0, 4.6, 3.4]], "a tier's aft"),
    ("galleries of a word", "form.stern.galleries_m", "two", "galleries_m is not a list"),
    # a band of lights: low below high, a whole count of one or more, a half-breadth
    ("a band upside down", "form.stern.lights_m", [[4.4, 3.6, 6, 2.4]], "a band's low z is below"),
    ("a band of no lights", "form.stern.lights_m", [[3.6, 4.4, 0, 2.4]], "of 0 lights; a band"),
    ("half a light", "form.stern.lights_m", [[3.6, 4.4, 2.5, 2.4]], "of 2.5 lights; a band is a"),
    ("a band of no breadth", "form.stern.lights_m", [[3.6, 4.4, 6, 0.0]], "within a half-breadth"),
    ("a band of three", "form.stern.lights_m", [[3.6, 4.4, 6]], r"not four numbers \[z_low"),
    # marks: a line, a form group or a stern key the profile gives, in one of the four words
    ("marks of a list", "marks", ["rail_m"], "marks is not a mapping of its lines to their words"),
    ("a mark of no line", "marks.sheer_m", "sourced", "marks has 'sheer_m', which is not a line"),
    ("a mark of the form", "marks.form", "judged", "marks has 'form', which is not a line"),
    ("a mark of the marks", "marks.marks", "judged", "marks has 'marks', which is not a line"),
    ("a measured mark", "marks.rail_m", "measured", "has rail_m 'measured'; a line is marked"),
]


@pytest.mark.parametrize("words, path, value, match", REFUSALS, ids=[r[0] for r in REFUSALS])
def test_the_schema_refuses_the_shape_keys_in_words(words, path, value, match):
    if path.startswith("marks."):
        p = copy.deepcopy(PROFILE)
        p["marks"][path.removeprefix("marks.")] = value
    else:
        p = _with(path, value)
    with pytest.raises(ShipFileError, match=match) as e:
        spec_from_dict(_doc(p), "p.yaml")
    assert str(e.value).startswith("p.yaml: the profile's ")


def test_a_mark_names_only_what_the_profile_gives():
    """A line, a form group or a stern key the profile gives may be marked, and one it does
    not give cannot; the refusal lists what may be marked."""
    p = copy.deepcopy(PROFILE)
    p["marks"].update({"form.fullness": "rule", "form.stern.type": "sourced", "wales_m": "judged"})
    assert dict(spec_from_dict(_doc(p), "p.yaml").hull.profile.marks)["form.fullness"] == "rule"
    p = _without("wales_m")
    p["marks"]["wales_m"] = "judged"
    with pytest.raises(ShipFileError, match="'wales_m', which is not a line"):
        spec_from_dict(_doc(p), "p.yaml")
    p = copy.deepcopy(PROFILE)
    p["form"].pop("fullness")
    p["marks"]["form.fullness"] = "judged"
    with pytest.raises(ShipFileError, match="'form.fullness', which is not a line") as e:
        spec_from_dict(_doc(p), "p.yaml")
    assert "it may mark rail_m, breadth_m, keel_m, stem_m, stern_m, wales_m, section_m" in str(
        e.value
    )
    assert "form.stern.lights_m" in str(e.value) and "form.stern.type" in str(e.value)
    p = copy.deepcopy(PROFILE)
    p["form"]["stern"].pop("round_up_m")
    p["marks"]["form.stern.round_up_m"] = "judged"
    with pytest.raises(ShipFileError, match="'form.stern.round_up_m', which is not a line"):
        spec_from_dict(_doc(p), "p.yaml")


def test_the_refusals_read_as_sentences():
    with pytest.raises(ShipFileError) as e:
        spec_from_dict(_doc(_with("form.stern.knuckle_z_m", 5.0)), "p.yaml")
    assert str(e.value) == (
        "p.yaml: the profile's form.stern has its knuckle at 5 m, at or above the taffrail (5 m, "
        "stern_m's top); the knuckle is the transom's foot."
    )
    with pytest.raises(ShipFileError) as e:
        spec_from_dict(_doc(_with("sections_m", [[0.0, -1.0, 4.0]])), "p.yaml")
    assert str(e.value) == (
        "p.yaml: the profile's sections_m gives one point at x 0; a station gives two or more, "
        "low to high."
    )


# -- the drawn hull (§5.3) -------------------------------------------------------------------


def test_a_profile_without_section_m_or_shape_keys_is_drawn_as_three_points_a_station():
    """§5.3 step 7, §6: the cut 0.8 m below the water at 0.92 of the water's half-breadth, the
    water and the rail, at each station; the stations `breadth_m`'s and the rail's within them,
    no gap a sixteenth of the length or more; the ends closed straight up at the farther of the
    rail's and the half-breadths' ends, to the middle line."""
    bare = {k: PROFILE[k] for k in ("rail_m", "breadth_m")}
    spec = _hull(bare)
    drawn = form.stations(spec)
    regular = drawn[1:-1]
    xs = [s[0][0] for s in regular]
    assert {-18.0, 0.0, 18.0} <= set(xs) and xs == sorted(xs)
    assert max(b - a for a, b in zip(xs, xs[1:], strict=False)) < 40.0 / 16
    p = spec.profile
    for s in regular:
        x = s[0][0]
        hb_w = _interp(p.breadth_m, x, 1)
        hb_r = _interp(p.breadth_m, x, 2)
        rail = _interp(p.rail_m, x, 1)
        expected = ((x, -0.8, 0.92 * hb_w), (x, 0.0, hb_w), (x, rail, hb_r))
        assert [c for pt in s for c in pt] == pytest.approx([c for pt in expected for c in pt])
    aft, fore = drawn[0], drawn[-1]
    assert {pt[0] for pt in aft} == {-21.0} and {pt[0] for pt in fore} == {21.0}
    assert all(pt[2] == 0.0 for pt in aft + fore)
    assert (aft[0][1], aft[-1][1], fore[-1][1]) == (-0.8, 5.0, 5.0)


def test_the_drawn_side_passes_through_every_given_point_and_the_ends_close():
    """§5.3 steps 2, 5 and 6: `breadth_m`'s water and rail, `breadth_line_m`'s main breadth and
    `sections_m`'s points within a millimetre; the stem closed to the middle line along its fore
    edge; the stern to the post below the knuckle and to the transom above it, its half-breadths
    from the knuckle's to the taffrail's; nothing beyond the ends, above the rail or below the
    hull."""
    spec = _hull(PROFILE)
    p = spec.profile
    for x, z, hb in p.sections_m + p.breadth_line_m:
        assert form.half_breadth_at(spec, x, z) == pytest.approx(hb, abs=0.001), (x, z)
    for x, hw, hr in p.breadth_m:
        assert form.half_breadth_at(spec, x, 0.0) == pytest.approx(hw, abs=0.001)
        assert form.half_breadth_at(spec, x, _interp(p.rail_m, x, 1)) == pytest.approx(hr, abs=1e-3)
    drawn = form.stations(spec)
    for s in drawn:
        assert all(b[1] >= a[1] for a, b in zip(s, s[1:], strict=False))  # rising
    fore, aft = drawn[-1], drawn[0]
    assert all(hb == 0.0 for _x, _z, hb in fore)
    for x, z, _hb in fore:
        assert x == pytest.approx(_stem_x(p, z))
    assert fore[-1][:2] == (21.0, 5.0)  # the stem head
    below = [pt for pt in aft if pt[1] < 3.0]
    above = [pt for pt in aft if pt[1] >= 3.0]
    assert below and all(hb == 0.0 for _x, _z, hb in below)
    assert [pt[2] for pt in above] == pytest.approx([0.0, 2.6, 3.0])  # the knuckle, the taffrail
    assert aft[-1][:2] == (-21.0, 5.0)
    # nothing beyond the ends' lines, above the rail or below the keel
    assert form.half_breadth_at(spec, 20.6, 0.0) == 0.0
    assert form.half_breadth_at(spec, 20.4, 0.0) > 0.0
    assert form.half_breadth_at(spec, -19.9, 0.5) == 0.0  # abaft the post (x -19.67 there)
    assert form.half_breadth_at(spec, -19.6, 0.5) > 0.0
    assert form.half_breadth_at(spec, 0.0, 4.2) == 0.0
    assert form.half_breadth_at(spec, 0.0, -6.0) == 0.0
    # the transom: between the aftmost station and the transom's line the side closes to it
    assert form.half_breadth_at(spec, -20.6, 3.5) == pytest.approx(
        _between(spec, -20.6, 3.5), abs=1e-9
    )
    assert form.check(spec)  # the notes; every given point drawn through


def test_a_round_stern_and_a_stern_with_no_form_close_to_the_middle_line():
    for stern in ({"type": "round"}, None):
        p = _without("form", "marks")
        if stern is not None:
            p["form"] = {"stern": stern}
        aft = form.stations(_hull(p))[0]
        assert all(hb == 0.0 for _x, _z, hb in aft) and aft[-1][:2] == (-21.0, 5.0)


def test_the_fullness_fills_the_ends_and_leaves_the_body():
    """§5.3 step 3: the run's fullness abaft the greatest section and the entry's before it;
    above 1 fuller, below 1 finer; the body (a quarter of the half-length each side of the
    greatest section) as it is."""
    p = _without("sections_m", "form", "marks")
    p["form"] = {"fullness": [1.0, 1.0]}
    plain = _hull(p)
    p["form"] = {"fullness": [0.5, 3.0]}
    shaped = _hull(p)
    for x, way in ((-15.0, -1.0), (15.0, 1.0)):
        fuller = form.half_breadth_at(shaped, x, -2.0) - form.half_breadth_at(plain, x, -2.0)
        assert way * fuller > 0.0, x
    assert form.half_breadth_at(shaped, 2.0, -2.0) == pytest.approx(
        form.half_breadth_at(plain, 2.0, -2.0)
    )


def test_the_outlines_and_the_drawn_displacement():
    """The outline in each view is a closed polygon in normalised units, abeam from the taffrail
    along the rail to the stem head and back along the bottom; ahead and astern the fore and
    after bodies' widest, on both sides; an unknown view refused. The drawn displacement of a
    hull of one section all along, three points a station and its ends straight up, is the
    section's area by its length, in sea water."""
    spec = _hull(PROFILE)
    abeam = form.outline(spec, "abeam")
    assert abeam[0] == pytest.approx((-21.0 / 40.0, 5.0 / 4.0))  # the taffrail; 4 m of freeboard
    for view in ("ahead", "astern"):
        side = form.outline(spec, view)
        assert side[0][0] == pytest.approx(-side[-1][0]) and side[0][1] == side[-1][1]
        assert max(u for u, _v in side) == pytest.approx(5.1 / 5.0)  # the main breadth at x 0
    with pytest.raises(ValueError, match="abeam, ahead, astern, not 'aloft'"):
        form.outline(spec, "aloft")
    box = {
        "rail_m": [[-10.0, 2.0], [10.0, 2.0]],
        "breadth_m": [[-10.0, 2.0, 2.0], [10.0, 2.0, 2.0]],
    }
    kg = form.drawn_displacement_kg(_hull(box, length_waterline_m=20.0))
    assert kg == pytest.approx(20.0 * 0.8 * (2.0 + 0.92 * 2.0) * 1025.0, rel=1e-9)


def test_check_records_the_drawn_displacement_the_depth_and_the_port_gaps():
    notes = form.check(_hull(PROFILE))
    assert notes[0].startswith("drawn displacement ") and "against the filed 900 t" in notes[0]
    assert notes[1].startswith("drawn ") and "against the file's draught of 4.5 m" in notes[1]
    assert [n.split(":")[0] for n in notes[2:]] == [
        "the upper port at x -8",
        "the upper port at x 8",
    ]


def test_a_given_point_the_drawing_cannot_reach_is_named_by_check():
    """A main breadth above the rail is no point of the drawn side: `check` names it."""
    p = copy.deepcopy(PROFILE)
    p["breadth_line_m"][1] = [0.0, 4.5, 5.1]
    with pytest.raises(ValueError, match="misses breadth_line_m's point at x 0, z 4.5"):
        form.check(_hull(p))


def test_the_drawn_hull_wants_a_profile():
    with pytest.raises(ValueError, match="no profile has no drawn form"):
        form.stations(spec_from_dict(_doc(), "p.yaml").hull)


def test_on_the_transoms_line_the_side_is_the_transoms():
    """Above the knuckle the side closes to the transom's half-breadth on the stern's own line,
    not to nothing (§5.3 step 6): 2.8 m at z 4, half-way from the knuckle's 2.6 to the
    taffrail's 3.0, where the line stands at x -20.75; nothing a centimetre abaft it."""
    spec = _hull(PROFILE)
    assert form.half_breadth_at(spec, -20.75, 4.0) == pytest.approx(2.8, abs=1e-9)
    assert form.half_breadth_at(spec, -20.76, 4.0) == 0.0


def test_two_lines_giving_one_place_two_half_breadths_are_named_by_check():
    """A sourced point where the plan gives one too (her WL1 in `sections_m` and `breadth_m`,
    say, with two allowances for the plank) is drawn as the sourced, and `check` refuses the
    two figures unless alike within a millimetre."""
    p = copy.deepcopy(PROFILE)
    p["sections_m"][2:2] = [[0.0, -1.0, 4.6], [0.0, 0.0, 5.3]]
    with pytest.raises(ValueError, match="sections_m and breadth_m give the half-breadth at x 0"):
        form.check(_hull(p))
    p["sections_m"][3] = [0.0, 0.0, 5.0]  # breadth_m's own figure at the water there
    assert form.check(_hull(p))


def test_the_rule_runs_fair_between_stations_of_sourced_points():
    """§5.3 step 5: a station between two stations of sourced points is the rule's moved by
    their departures from the rule, straight between them, so that at every height both source
    the side runs fair from one to the next. The 64 with WL2 to WL5 sourced and a station of
    the rule's between each two: every such station within 0.10 m of the straight line between
    its sourced neighbours (measured 0.03 m; the bare rule between them stood 1.53 m off), and
    every sourced point drawn through within a millimetre (`check`)."""
    spec = _sixty_four_sourced()
    regular = form.stations(spec)[1:-1]
    sourced = {x for x, _z, _hb in spec.profile.sections_m}
    assert sum(s[0][0] not in sourced for s in regular) >= 20
    assert _off_the_sourced_line(spec) <= 0.10
    assert form.check(spec)


# PROFILE with its rail over the counter, two points abaft the aftmost station of `breadth_m`,
# and the rail ending at a beakhead bulkhead at x 17, abaft the stem head (21, 3.5) and the
# foremost station of `breadth_m` (x 18) (Build-Ships.md §5.1).
COUNTER = copy.deepcopy(PROFILE)
COUNTER["rail_m"] = [[-21.0, 5.0], [-20.3, 4.9], [-19.6, 4.85], [0.0, 4.0], [17.0, 4.5]]
COUNTER["stem_m"] = [[17.0, -4.4], [20.0, -1.0], [20.5, 0.0], [21.0, 3.5]]


def test_the_top_of_the_side_runs_through_every_rail_point_and_falls_to_the_stem_head():
    """The drawn top of the side passes through every rail point between the ends' lines: over
    the counter, a station at each rail point abaft the others, from where the stern's line
    crosses its x (no side drawn under the counter) up to the rail; forward of a rail that ends
    at a beakhead bulkhead, the top falls straight from its end to the stem head (§5.1, §6),
    never held at the rail's height to the stations beyond it."""
    spec = _hull(COUNTER)
    drawn = form.stations(spec)
    tops = {s[0][0]: s for s in drawn[1:-1]}
    for x, z in ((-20.3, 4.9), (-19.6, 4.85), (0.0, 4.0), (17.0, 4.5)):
        assert tops[x][-1][:2] == pytest.approx((x, z), abs=0.001), x
        assert form.half_breadth_at(spec, x, z - 0.01) > 0.0
        assert form.half_breadth_at(spec, x, z + 0.01) == 0.0
    # over the counter: each starts where the stern's line crosses it (z 2.4 and 0.3), at its x
    for x, z_low in ((-20.3, 2.4), (-19.6, 0.3)):
        assert {pt[0] for pt in tops[x]} == {x}
        assert tops[x][0][1] == pytest.approx(z_low, abs=1e-9)
        assert form.half_breadth_at(spec, x, z_low - 0.01) == 0.0
    # forward of the bulkhead: straight from (17, 4.5) to the stem head (21, 3.5)
    assert tops[18.0][-1][1] == pytest.approx(4.25, abs=1e-9)
    assert form.half_breadth_at(spec, 19.0, 4.0 - 0.01) > 0.0
    assert form.half_breadth_at(spec, 19.0, 4.0 + 0.01) == 0.0
    assert drawn[-1][-1][:2] == (21.0, 3.5)
    assert form.check(spec)


def test_the_abeam_outline_follows_the_stem_and_the_stern():
    """The abeam outline runs from the taffrail along the top of the side to the stem head,
    down the stem's fore edge, aft along the bottom and up the post, the counter and the stern,
    so that every point of `stem_m` and `stern_m` within the closures' heights is one of its
    corners (the pair check reads the ends' shapes, §5.6)."""
    for spec in (_hull(PROFILE), _hull(COUNTER), _lynx()):
        p = spec.profile
        abeam = form.outline(spec, "abeam")
        drawn = form.stations(spec)
        freeboard = interp(p.rail_m, _greatest_x(spec))
        assert abeam[0] == pytest.approx(
            (drawn[0][-1][0] / spec.length_waterline_m, drawn[0][-1][1] / freeboard)
        )  # the taffrail
        for line, closure in ((p.stem_m, drawn[-1]), (p.stern_m, drawn[0])):
            low = closure[0][1]
            for x, z in line:
                if z < low:
                    continue
                up = z / freeboard if z >= 0.0 else z / spec.draught_m
                corner = (x / spec.length_waterline_m, up)
                assert any(c == pytest.approx(corner, abs=1e-9) for c in abeam), (x, z)


def _greatest_x(spec: HullSpec) -> float:
    """The middle of the flat of greatest breadth at the water (`form`'s greatest section)."""
    greatest = max(hw for _x, hw, _hr in spec.profile.breadth_m)
    tied = [x for x, hw, _hr in spec.profile.breadth_m if hw == greatest]
    return 0.5 * (tied[0] + tied[-1])


# -- the checkpoint (§16.2) ----------------------------------------------------------------


def test_a_profile_without_the_shape_keys_pickles_as_before_0h():
    """The shape fields are plain class defaults, left out of the pickled state while empty, so
    that a profile without them (the 64's and the razee's, their shape fields set back to the
    defaults whatever their files come to give, and a hand-built one) pickles its ten fields in
    their order as before stage 0H, and one pickled before it loads and reads the defaults; a
    profile with them keeps them."""
    bare = _hull(_without(*SHAPE)).profile
    defaults = {f.name: f.default for f in fields(HullProfile) if f.name in SHAPE}
    for p in (
        replace(load_ship("data/ships/sixty-four.yaml").spec.hull.profile, **defaults),
        replace(load_ship("data/ships/razee-44.yaml").spec.hull.profile, **defaults),
        bare,
    ):
        assert list(p.__getstate__()) == list(OLD_FIELDS)
        data = pickle.dumps(p)
        for key in SHAPE:
            assert key.encode() not in data, key
        again = pickle.loads(data)
        assert again == p and not set(SHAPE) & set(again.__dict__)
    old = HullProfile.__new__(HullProfile)
    old.__dict__.update(bare.__getstate__())  # as a pickle from before 0H loads
    assert (old.head_m, old.sections_m, old.form, old.marks) == ((), (), None, ())
    assert old == bare
    full = _hull(PROFILE).profile
    assert list(full.__getstate__()) == list(PROFILE_KEYS)
    assert pickle.loads(pickle.dumps(full)) == full


SHIP_FILES = sorted((ROOT / "data" / "ships").glob("*.yaml"))


@pytest.mark.parametrize("path", SHIP_FILES, ids=[p.stem for p in SHIP_FILES])
def test_every_ships_spec_round_trips_its_pickle_with_the_shape_keys_its_file_gives(path):
    """Every ship's spec pickles and loads back equal, its profile's state carrying exactly the
    shape keys its file gives (none at stage 0H; hers from her stage B, the eight's from
    SW-2b.2) and no point key it does not give."""
    spec = load_ship(str(path)).spec
    data = pickle.dumps(spec)
    p = spec.hull.profile
    given = {key for key in SHAPE if p is not None and getattr(p, key)}
    if p is not None:
        assert set(p.__getstate__()) & set(SHAPE) == given
    for key in SHAPE[:6]:
        if key not in given:
            assert key.encode() not in data, key
    assert pickle.loads(data) == spec


# -- the guard (§5.0 principle 8; §14.1) ---------------------------------------------------

# The modules that may read a profile's shape fields (Build-Ships.md §5.6): the schema, the
# form and the server; the tools (the generator) and the tests are outside the package.
READERS = {"freesail/ship/schema.py", "freesail/ship/form.py", "freesail/api/queries.py"}
POINT_KEYS = SHAPE[:6]
# The form's and the stern's own fields, and the schema's names for the shape: none is read in
# the package outside the three readers (grep, at stage 0H), so each is a shape read anywhere.
FORM_FIELDS = ("fullness", "knuckle_z_m", "transom_hb_m", "round_up_m", "galleries_m", "lights_m")
SHAPE_NAMES = (
    "HullForm",
    "HullStern",
    "SHAPE_KEYS",
    "FORM_KEYS",
    "STERN_KEYS",
    "STERN_TYPES",
    "HEAD_WORDS",
    "MARK_WORDS",
)
# The drawing itself: an import of it, or its name in a string, is a read of the shape.
FORM_MODULE = "freesail.ship.form"


def _shape_reads(source: str) -> list[tuple[int, str]]:
    """Where a module's code reads the shape, (line, what), in line order:
    - an attribute or a string of one of the six point keys, anywhere (no other name in the
      package is like them);
    - `form` or `marks` read off a profile (`profile.form`, `spec.hull.profile.marks`,
      `prof.marks`, `getattr(profile, "form")`, or off a name the module binds to a profile or
      annotates as `HullProfile`), since `form` and `marks` are common names elsewhere;
    - a field of the form or the stern (`.fullness`, `.transom_hb_m`, ...), and a name of the
      schema's for the shape (`HullForm`, `SHAPE_KEYS`, ...), read or imported;
    - an import of `freesail.ship.form` in any of its ways (`import`, `from ... import`, `from
      freesail.ship import form`, relative), or its name in a string (`importlib`).
    The guard reads names, not types: a profile passed in under another name and never bound
    or annotated in the module is not seen, which the other kinds above still catch where it
    reaches the form."""
    tree = ast.parse(source)
    profiles = _profile_names(tree)
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute):
            if node.attr in POINT_KEYS or node.attr in FORM_FIELDS or node.attr in SHAPE_NAMES:
                found.append((node.lineno, node.attr))
            elif node.attr in ("form", "marks") and _a_profile(node.value, profiles):
                found.append((node.lineno, node.attr))
        elif isinstance(node, ast.Name) and node.id in SHAPE_NAMES:
            found.append((node.lineno, node.id))
        elif isinstance(node, ast.Constant) and (
            node.value in POINT_KEYS or node.value == FORM_MODULE
        ):
            found.append((node.lineno, node.value))
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == FORM_MODULE or alias.name.startswith(FORM_MODULE + "."):
                    found.append((node.lineno, FORM_MODULE))
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            names = [alias.name for alias in node.names]
            # `freesail.ship.form`, or relative `.form` (in ship/) and `..ship.form`
            whole = module == FORM_MODULE or (node.level and module in ("form", "ship.form"))
            # `freesail.ship` with `form`, or relative `.` (in ship/) and `..ship`
            parent = module == "freesail.ship" or (node.level and module in ("", "ship"))
            if whole or (parent and "form" in names):
                found.append((node.lineno, FORM_MODULE))
            found += [(node.lineno, name) for name in names if name in SHAPE_NAMES]
        elif (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "getattr"
            and len(node.args) >= 2
            and _a_profile(node.args[0], profiles)
            and isinstance(node.args[1], ast.Constant)
            and node.args[1].value in ("form", "marks")
        ):
            found.append((node.lineno, node.args[1].value))
    return sorted(found)


def _a_profile(node: ast.AST, profiles: set[str] = frozenset()) -> bool:
    """A node that is a profile by its name: a name or an attribute beginning with `prof` or
    ending in `profile`, a name the module binds to one or annotates as `HullProfile`, or
    `getattr(..., "profile")`."""
    if isinstance(node, ast.Name):
        return node.id.startswith("prof") or node.id.endswith("profile") or node.id in profiles
    if isinstance(node, ast.Attribute):
        return node.attr.startswith("prof") or node.attr.endswith("profile")
    return (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "getattr"
        and len(node.args) >= 2
        and isinstance(node.args[1], ast.Constant)
        and node.args[1].value == "profile"
    )


def _profile_names(tree: ast.AST) -> set[str]:
    """The names a module binds to a profile (`p = spec.hull.profile`, `p := ...`) or annotates
    as one (`def f(p: HullProfile)`, `p: HullProfile | None = ...`), anywhere in it."""
    names = set()

    def annotated(annotation: ast.AST | None) -> bool:
        return annotation is not None and any(
            (isinstance(n, ast.Name) and n.id == "HullProfile")
            or (isinstance(n, ast.Attribute) and n.attr == "HullProfile")
            or (isinstance(n, ast.Constant) and "HullProfile" in str(n.value))
            for n in ast.walk(annotation)
        )

    for node in ast.walk(tree):
        if isinstance(node, (ast.Assign, ast.NamedExpr)) and _a_profile(node.value):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            names |= {t.id for t in targets if isinstance(t, ast.Name)}
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            if annotated(node.annotation) or (node.value is not None and _a_profile(node.value)):
                names.add(node.target.id)
        elif isinstance(node, ast.arg) and annotated(node.annotation):
            names.add(node.arg)
    return names


def test_the_guard_finds_a_shape_read():
    snippet = (
        "a = spec.hull.profile.form\n"
        "b = p.sections_m\n"
        "c = getattr(profile, 'marks')\n"
        "d = raw['breadth_line_m']\n"
        "e = request.form\n"  # not a profile's: left alone
        "f = order.marks\n"
        "prof = ship.hull.spec.profile\n"  # a name bound to a profile: its form and marks
        "g = prof.marks\n"
        "h = prof.form.fullness\n"
        "i = stern.transom_hb_m\n"  # the stern's fields, read off anything
        "from freesail.ship.form import half_breadth_at\n"  # the drawing, imported any way
        "from freesail.ship import form\n"
        "import freesail.ship.form as drawn\n"
        "from .form import stations\n"
        "from ..ship import form as f2\n"
        "from freesail.ship.schema import SHAPE_KEYS, HullForm\n"  # the schema's shape names
        "j = HullStern\n"
        "k = importlib.import_module('freesail.ship.form')\n"
        "def l(q: HullProfile):\n"  # a name annotated as a profile
        "    return q.marks\n"
        "m = getattr(getattr(ship.hull.spec, 'profile'), 'form')\n"
        "n = schema.MARK_WORDS\n"
        "o = prof_in.marks\n"  # a name beginning with prof, bound nowhere in the module
    )
    assert _shape_reads(snippet) == [
        (1, "form"),
        (2, "sections_m"),
        (3, "marks"),
        (4, "breadth_line_m"),
        (8, "marks"),
        (9, "form"),
        (9, "fullness"),
        (10, "transom_hb_m"),
        (11, FORM_MODULE),
        (12, FORM_MODULE),
        (13, FORM_MODULE),
        (14, FORM_MODULE),
        (15, FORM_MODULE),
        (16, "HullForm"),
        (16, "SHAPE_KEYS"),
        (17, "HullStern"),
        (18, FORM_MODULE),
        (20, "marks"),
        (21, "form"),
        (22, "MARK_WORDS"),
        (23, "marks"),
    ]
    # what stays clear: the common words off what is not a profile, and other modules
    clear = (
        "x = order.marks\n"
        "y = request.form\n"
        "from freesail.combat import marks\n"
        "from freesail.ship.profile import rail_at\n"
        "import freesail.ship.schema\n"
    )
    assert _shape_reads(clear) == []


def test_nothing_but_the_schema_the_form_and_the_server_reads_the_shape_keys():
    """Nothing under `physics/`, `combat/`, `crew/` or `world/`, nor anywhere else in the package
    but the three readers, reads a shape key: the drawing never changes how a ship sails or
    fights."""
    found = {}
    for path in sorted((ROOT / "freesail").rglob("*.py")):
        rel = path.relative_to(ROOT).as_posix()
        if rel in READERS:
            continue
        reads = _shape_reads(path.read_text(encoding="utf-8"))
        if reads:
            found[rel] = reads
    assert found == {}


# -- the server ----------------------------------------------------------------------------


def test_the_ship_graph_serves_the_shape_and_the_drawn_stations_where_the_file_has_a_profile():
    """`_profile_entry` serves the shape keys, the form and the marks as the file gives them,
    each only where given; `hull.stations` is the drawn hull to the millimetre where the file
    has a profile, and a document with none is served neither."""
    ship = ship_from_dict(_doc(PROFILE), "p.yaml")
    hull = ship_graph(ship)["hull"]
    assert hull["profile"] == PROFILE and list(hull["profile"]) == list(PROFILE)
    assert list(hull["profile"]["form"]["stern"]) == list(PROFILE["form"]["stern"])
    drawn = form.stations(ship.hull.spec)
    assert len(hull["stations"]) == len(drawn)
    for served, s in zip(hull["stations"], drawn, strict=True):
        flat = [c for pt in s for c in pt]
        assert [c for pt in served for c in pt] == pytest.approx(flat, abs=0.0005)
    lean = {k: PROFILE[k] for k in ("rail_m", "breadth_m")}
    lean["form"] = {"head": "knee"}
    served = ship_graph(ship_from_dict(_doc(lean), "p.yaml"))["hull"]["profile"]
    assert served == lean
    plain = ship_graph(ship_from_dict(_doc(), "p.yaml"))["hull"]
    assert "profile" not in plain and "stations" not in plain
    assert ship_graph(load_ship("data/ships/sixty-four.yaml"))["hull"]["stations"]


# -- the rule against measured lines (§5.3; §14.1) -----------------------------------------

# The band that 15 degrees of heel lifts out of the water: a point of a section whose height
# above the water, heeled, is above it (`second_hull_check.py`, the hull's design).
HEEL = math.radians(15.0)


def _fi(s: str) -> float:
    """Feet and inches as Steel prints them ('18 10', '17 4¼'), in feet."""
    s = s.replace("¼", ".25").replace("½", ".5").replace("¾", ".75")
    feet, inches = s.split()
    return float(feet) + float(inches) / 12.0


# Steel's 36, "the frigate of 36 guns and 877 tons", by timber aft to forward
# (docs/design/ships-design/pages-steel-1805-bodies.md): x, the rail's height and the half-breadths
# at the water and at the rail, metres, moulded (§5.2); the upper height of breadth above the
# base, the main and the top-timber half-breadths and the 1st to 6th diagonals, feet and inches,
# as read on the page image (§3.1; None, Steel's blank).
STEEL_36 = [
    ("30", -20.02, 4.27, 1.31, 3.72, "23 1½", "13 7", "12 2½",
     ("0 8", "1 2", "2 3", "4 6", "7 4½", "13 5½")),
    ("29", -19.28, 4.20, 2.37, 3.84, "22 6", "14 0", "12 7",
     ("1 1½", "2 0", "3 8", "6 3½", "9 2½", "14 9½")),
    ("27", -17.81, 4.09, 3.72, 4.05, "22 1", "15 0", "13 3½",
     ("1 11½", "3 6½", "5 9½", "8 9½", "11 8", "16 7¼")),
    ("25", -16.33, 3.96, 4.35, 4.24, "21 6", "15 9", "13 11",
     ("2 10", "5 0", "7 7½", "10 8", "13 5½", "18 0")),
    ("23", -14.86, 3.85, 4.72, 4.42, "20 11", "16 5", "14 6",
     ("3 9", "6 4", "9 2", "12 3", "14 11", "19 2")),
    ("19", -11.91, 3.67, 5.19, 4.70, "20 1½", "17 5", "15 5",
     ("5 6½", "8 9½", "11 10½", "14 9½", "17 2½", None)),
    ("15", -8.97, 3.52, 5.47, 4.90, "19 5½", "18 1½", "16 1",
     ("7 1", "10 10", "13 10½", "16 8", "18 9", None)),
    ("11", -6.02, 3.41, 5.63, 5.04, "19 1", "18 6½", "16 6½",
     ("8 3", "12 5", "15 5½", "18 8", "19 11", None)),
    ("7", -3.07, 3.33, 5.70, 5.09, "18 10½", "18 9", "16 8½",
     ("8 10", "13 4", "16 4¼", "18 10¾", "20 8", None)),
    ("⊕", 2.11, 3.27, 5.73, 5.11, "18 11", "18 10", "16 9",
     ("9 4", "13 11½", "17 0", "19 4", "20 10½", None)),
    ("C", 5.77, 3.29, 5.73, 5.11, "18 11½", "18 10", "16 9",
     ("9 3", "13 9", "16 10", "19 1½", "20 9", None)),
    ("G", 8.71, 3.33, 5.71, 5.11, "19 1", "18 10", "16 9",
     ("8 10", "13 1", "16 2¼", "18 8", "20 5", None)),
    ("L", 11.66, 3.43, 5.55, 5.03, "19 6½", "18 5½", "16 6",
     ("7 11¼", "11 10½", "14 11½", "17 7½", "19 6", None)),
    ("P", 14.61, 3.54, 5.03, 4.81, "20 7½", "17 1½", "15 9½",
     ("6 6½", "9 10½", "12 10¾", "15 7½", "17 7½", None)),
    ("T", 17.54, 3.70, 3.73, 4.14, "22 6", "13 9", "13 7",
     ("4 2", "6 9½", "9 4½", "11 9½", "13 8½", None)),
    ("W", 19.01, 3.81, 2.52, 3.38, "23 11¼", "10 7½", "11 1",
     ("2 1", "4 4½", "6 6½", "8 8", "10 4", None)),
    ("X", 19.75, 3.89, 1.65, 2.77, "24 9½", "8 3", "9 1",
     ("0 8", "2 8½", "4 7", "6 5½", "7 11", None)),
]  # fmt: skip
# The diagonals (§3.1): their heights up the middle line above the base; the 1st to the 3d end
# on the base so far out, the 4th to the 6th on the side line (the dead flat's main
# half-breadth, 18 ft 10 in) so far up (feet and inches, read).
DIAGONAL_HEIGHTS = ("8 0", "12 0", "15 8", "19 2½", "22 2", "28 0")
DIAGONAL_ENDS = (("7 4", "0 0"), ("13 2", "0 0"), ("18 1", "0 0"),
                 ("18 10", "3 8½"), ("18 10", "7 10½"), ("18 10", "11 8"))  # fmt: skip
# The midship section at dead flat, z above the load line and the half-breadth with the plank
# (§5.4), and the plank, 4 in (§5.4: half of Folio I's extreme less moulded breadth), taken off
# all but the first point, the keel's rabbet, so that the section is moulded as the table is.
STEEL_36_SECTION = [(-4.96, 0.20), (-4.62, 2.02), (-4.17, 3.25), (-3.58, 4.02), (-2.85, 4.65),
                    (-2.05, 5.17), (0.29, 5.84), (0.80, 5.84), (3.27, 5.21)]  # fmt: skip
PLANK_36_M = 4.0 / 12.0 * FT
# The main keel's underside at the perpendiculars, AP and FP (§5.3, Folio I's draughts).
STEEL_36_KEEL = [[-20.88, -5.59], [20.88, -5.28]]


def _steel_36_load_line(x: float) -> float:
    """The load line above the base, feet: 15 ft 10 in at FP (x +20.88), 16 ft 10 in at AP,
    straight (§5.1)."""
    t = (x + 20.88) / 41.76
    return _fi("16 10") + t * (_fi("15 10") - _fi("16 10"))


def _steel_36(*, breadth_line: bool) -> HullSpec:
    """Steel's 36 as a profile: the table's stations, her keel and her moulded midship section;
    with her main breadth by station, as her file is to carry it (Build-Ships.md §5.7: S†), or
    without, the rule's default drawing it."""
    section = [STEEL_36_SECTION[0]] + [(z, hb - PLANK_36_M) for z, hb in STEEL_36_SECTION[1:]]
    profile = {
        "rail_m": [[x, rail] for _t, x, rail, *_ in STEEL_36],
        "breadth_m": [[x, hw, hr] for _t, x, _rail, hw, hr, *_ in STEEL_36],
        "keel_m": STEEL_36_KEEL,
        "section_m": [list(pt) for pt in section],
    }
    if breadth_line:
        profile["breadth_line_m"] = [
            [x, (_fi(upper) - _steel_36_load_line(x)) * FT, _fi(main) * FT]
            for _t, x, _rail, _hw, _hr, upper, main, *_ in STEEL_36
        ]
    return _hull(profile, length_waterline_m=41.76, beam_m=11.68, draught_m=5.44)


def _cross(station, origin: tuple[float, float], u: tuple[float, float]) -> float | None:
    """How far along the diagonal from `origin` (half-breadth, z) in direction `u` it first meets
    the drawn section."""
    best = None
    pts = [(pt[2], pt[1]) for pt in station]
    for (y0, z0), (y1, z1) in zip(pts, pts[1:], strict=False):
        ay, az = y1 - y0, z1 - z0
        det = u[0] * -az - u[1] * -ay
        if abs(det) < 1e-12:
            continue
        ry, rz = y0 - origin[0], z0 - origin[1]
        t = (ry * -az - rz * -ay) / det
        s = (u[0] * rz - u[1] * ry) / det
        if -1e-9 <= s <= 1.0 + 1e-9 and t > 0.0:
            best = t if best is None else min(best, t)
    return best


def _steel_36_errors(spec: HullSpec) -> tuple[list[float], list[float]]:
    """The drawn hull against Steel's table, metres: at each timber, the widest point drawn less
    the table's (the greater of the main and the top-timber half-breadths); and along each
    diagonal, at each point the band shows (15 degrees of heel, from windward), the drawn
    section's distance less the table's."""
    drawn = {s[0][0]: s for s in form.stations(spec)[1:-1]}
    widest, band = [], []
    for _t, x, _rail, _hw, _hr, _upper, main, top_timber, diagonals in STEEL_36:
        station = drawn[x]
        widest.append(max(pt[2] for pt in station) - max(_fi(main), _fi(top_timber)) * FT)
        water = _steel_36_load_line(x)
        for height, (ey, ez), d in zip(DIAGONAL_HEIGHTS, DIAGONAL_ENDS, diagonals, strict=True):
            if d is None:
                continue
            h, vy, vz = _fi(height), _fi(ey), _fi(ez) - _fi(height)
            n = math.hypot(vy, vz)
            u = (vy / n, vz / n)
            reach = _fi(d)
            y, z = reach * u[0] * FT, (h + reach * u[1] - water) * FT
            if y * math.sin(HEEL) + z * math.cos(HEEL) <= 0.0:
                continue  # under the heeled water
            t = _cross(station, (0.0, (h - water) * FT), u)
            if t is not None:
                band.append(t - reach * FT)
    return widest, band


# The 64, Indefatigable's class: the half-breadths of WL1 (the load line) to WL5, moulded, feet,
# by station in feet from AP, measured on ZAZ1407 (docs/design/Research-Indefatigable-2026-10.md
# §2.3.2: 5 to 130 ft on 1407T, 140 to 160 ft and WL1 at the post on 1407F); None where the
# waterline has ended.
SIXTY_FOUR_WL = {
    0: (0.6, None, None, None, None),
    5: (7.2, 3.1, 1.5, 1.0, 0.4),
    10: (12.1, 5.6, 2.6, 1.3, 0.6),
    20: (16.6, 13.0, 7.3, 3.5, 1.4),
    30: (18.8, 16.9, 12.6, 7.2, 2.9),
    40: (20.06, 18.9, 16.1, 11.4, 5.4),
    50: (20.8, 20.1, 18.0, 14.5, 9.0),
    60: (21.3, 20.7, 19.1, 16.3, 12.0),
    70: (21.6, 21.1, 19.7, 17.3, 13.8),
    80: (21.7, 21.3, 20.0, 17.8, 14.5),
    90: (21.75, 21.3, 20.0, 17.9, 14.7),
    100: (21.75, 21.3, 20.0, 17.6, 14.2),
    110: (21.75, 21.2, 19.6, 16.8, 12.8),
    120: (21.5, 20.7, 18.7, 15.1, 9.9),
    130: (20.5, 19.2, 16.5, 12.0, 6.2),
    140: (17.68, 15.54, 11.66, 7.17, 2.99),
    142: (16.81, 14.47, 10.46, 6.14, 2.47),
    144: (15.82, 13.22, 9.18, 5.13, 1.99),
    146: (14.62, 11.81, 7.80, 4.17, 1.54),
    148: (13.23, 10.28, 6.47, 3.29, 1.11),
    150: (11.70, 8.60, 5.12, 2.44, 0.72),
    152: (9.96, 6.88, 3.85, 1.63, None),
    154: (7.96, 5.11, 2.7, 0.89, None),
    155: (6.87, 4.24, 2.05, 0.55, None),
    156: (5.70, 3.35, 1.44, None, None),
    157: (4.51, 2.50, 0.92, None, None),
    158: (3.25, 1.63, None, None, None),
    159: (1.96, 0.77, None, None, None),
    160: (0.63, None, None, None, None),
}
# WL2 to WL5 lie 3.77 ft apart below WL1 (§2.3.1, measured on 1407F).
SIXTY_FOUR_WL_SPACING_FT = 3.77
# The midship section, the half-breadth in feet at heights in feet above the rabbet (§2.3.2,
# measured on 1407T), WL1 18.8 ft above the rabbet at midships (§2.3.1); its first point the
# rabbet at a half-siding of 0.75 ft (judgement, the hull's design's check: the note gives no
# siding).
SIXTY_FOUR_SECTION = [
    (0.0, 0.75), (0.7, 4.0), (1.5, 10.4), (2.35, 12.5), (3.2, 13.9), (4.0, 15.0), (5.7, 16.5),
    (7.3, 17.7), (9.0, 18.8), (10.6, 19.7), (12.3, 20.5), (13.9, 21.0), (15.6, 21.4),
    (17.3, 21.65), (23.0, 21.65), (24.6, 21.4), (26.3, 20.8), (28.0, 19.9), (29.6, 18.75),
    (31.3, 18.0), (34.6, 17.0), (37.1, 16.1),
]  # fmt: skip
SIXTY_FOUR_RABBET_FT = 18.8
# K, the keel's underside, below WL1 at AP and at 160 ft (§2.3.1: 6.48 m and 6.18 m).
SIXTY_FOUR_KEEL = [[-24.38, -6.48], [24.38, -6.18]]


def _sixty_four_profile() -> dict:
    """The 64 as a profile: WL1 by station and her midship section. The rail is not read by the
    band: it stands at the section's top, held, and its half-breadth is WL1's (judgement, for
    this test alone)."""
    breadth = [[(s - 80.0) * FT, wl[0] * FT, wl[0] * FT] for s, wl in SIXTY_FOUR_WL.items()]
    section = [[(h - SIXTY_FOUR_RABBET_FT) * FT, hb * FT] for h, hb in SIXTY_FOUR_SECTION]
    return {
        "rail_m": [[0.0, section[-1][0]]],
        "breadth_m": breadth,
        "keel_m": SIXTY_FOUR_KEEL,
        "section_m": section,
    }


def _sixty_four(profile: dict | None = None) -> HullSpec:
    return _hull(
        profile or _sixty_four_profile(), length_waterline_m=48.8, beam_m=13.54, draught_m=6.33
    )


def _sixty_four_sourced() -> HullSpec:
    """The 64 with WL2 to WL5 as sourced points at each station that gives two or more of them
    (§2.3.2, as her stage B is to give them), and a rail point midway between each two of her
    stations at the same held height, so that the rule draws a station between each two
    (judgement, for this test alone: the rail is not read)."""
    profile = _sixty_four_profile()
    top = profile["rail_m"][0][1]
    feet = sorted(SIXTY_FOUR_WL)
    profile["rail_m"] = [
        [(0.5 * (a + b) - 80.0) * FT, top] for a, b in zip(feet, feet[1:], strict=False)
    ]
    profile["sections_m"] = []
    for s in feet:
        points = [
            [(s - 80.0) * FT, -k * SIXTY_FOUR_WL_SPACING_FT * FT, hb * FT]
            for k, hb in enumerate(SIXTY_FOUR_WL[s])
            if k > 0 and hb is not None
        ]
        if len(points) >= 2:
            profile["sections_m"] += sorted(points, key=lambda pt: pt[1])
    return _sixty_four(profile)


def _off_the_sourced_line(spec: HullSpec) -> float:
    """The worst distance, metres, of a station that has no sourced point of its own from the
    straight line between the two sourced stations either side of it, at each height both of
    them source."""
    p = spec.profile
    by_x: dict[float, set[float]] = {}
    for x, z, _hb in p.sections_m:
        by_x.setdefault(x, set()).add(z)
    src = sorted(by_x)
    worst = 0.0
    for s in form.stations(spec)[1:-1]:
        x = s[0][0]
        if x in by_x or not src[0] < x < src[-1]:
            continue
        a, b = max(v for v in src if v < x), min(v for v in src if v > x)
        for z in by_x[a] & by_x[b]:
            ha, hb = form.half_breadth_at(spec, a, z), form.half_breadth_at(spec, b, z)
            straight = ha + (hb - ha) * (x - a) / (b - a)
            worst = max(worst, abs(form.half_breadth_at(spec, x, z) - straight))
    return worst


def _band_errors(spec: HullSpec, lines: list[tuple[float, float, float]]) -> list[float]:
    """At each measured point (x, depth below the water, half-breadth) that 15 degrees of heel
    can lift out of the water (no deeper than the water's half-breadth there by tan 15°) and
    that lies within the drawn hull's depth, the drawn half-breadth less the measured."""
    drawn = {s[0][0]: s for s in form.stations(spec)[1:-1]}
    out = []
    for x, depth, hb in lines:
        station = drawn[x]
        water = form.half_breadth_at(spec, x, 0.0)
        if depth > water * math.tan(HEEL) or -depth < station[0][1]:
            continue
        out.append(form.half_breadth_at(spec, x, -depth) - hb)
    return out


def _sixty_four_lines() -> list[tuple[float, float, float]]:
    return [
        ((s - 80.0) * FT, k * SIXTY_FOUR_WL_SPACING_FT * FT, hb * FT)
        for s, wl in SIXTY_FOUR_WL.items()
        for k, hb in enumerate(wl)
        if k > 0 and hb is not None
    ]


# Lynx (H.M. schooner Musquidobit, late Lynx: Chapelle 1930, fig. 17), from
# docs/design/ships-design/pages-chapelle-fig17.md: the profile's points in metres (§6: the rail,
# the half-breadths at the line and the rail, the keel's lower edge, the stem's fore edge, the
# post, the transom and the taffrail, and the midship section, moulded); and WL2 and WL3, 2.32 ft
# and 4.52 ft below the load line, their half-breadths in feet by station (§4, §5.2, measured).
LYNX = {
    "rail_m": [[-15.88, 2.44], [-13.00, 2.23], [-11.90, 2.17], [-10.71, 2.10], [-9.57, 2.04],
               [-8.42, 1.98], [-7.24, 1.94], [-6.08, 1.91], [-4.93, 1.89], [-3.77, 1.88],
               [-2.59, 1.87], [-1.44, 1.87], [-0.30, 1.87], [0.87, 1.88], [2.03, 1.90],
               [3.16, 1.94], [4.33, 1.98], [5.48, 2.03], [6.61, 2.08], [7.78, 2.15],
               [8.92, 2.23], [10.09, 2.30], [11.20, 2.38], [12.35, 2.45], [13.51, 2.57],
               [14.30, 2.64], [14.86, 2.70]],
    "breadth_m": [[-12.86, 0.34, 2.56], [-11.75, 0.97, 2.69], [-10.58, 1.70, 2.80],
                  [-9.44, 2.23, 2.89], [-8.29, 2.59, 2.99], [-7.11, 2.86, 3.09],
                  [-5.96, 3.03, 3.18], [-4.81, 3.18, 3.25], [-3.65, 3.27, 3.34],
                  [-2.47, 3.33, 3.40], [-1.32, 3.40, 3.46], [-0.18, 3.45, 3.51],
                  [0.99, 3.47, 3.54], [2.15, 3.47, 3.56], [3.29, 3.44, 3.55],
                  [4.46, 3.36, 3.56], [5.61, 3.23, 3.49], [6.74, 3.03, 3.38],
                  [7.92, 2.72, 3.21], [9.06, 2.30, 3.01], [10.24, 1.78, 2.71],
                  [11.36, 1.20, 2.33], [12.51, 0.54, 1.74]],
    "keel_m": [[-11.54, -3.91], [-8.93, -3.76], [-4.63, -3.52], [-0.34, -3.28], [3.95, -3.04],
               [8.24, -2.80], [10.60, -2.65]],
    "stem_m": [[10.60, -2.65], [10.98, -2.49], [12.08, -1.77], [12.91, -1.06], [13.55, -0.37],
               [13.85, 0.00], [14.21, 0.53], [14.61, 1.21], [14.79, 1.65], [14.86, 2.70]],
    "stern_m": [[-11.54, -3.91], [-12.11, -2.91], [-12.73, -1.87], [-13.36, -0.83],
                [-13.87, 0.00], [-14.11, 0.41], [-14.77, 1.34], [-15.88, 2.44]],
    "section_m": [[-2.52, 0.32], [-2.39, 0.53], [-2.20, 0.85], [-1.98, 1.24], [-1.75, 1.77],
                  [-1.52, 2.12], [-1.38, 2.26], [-0.71, 3.12], [0.00, 3.47], [1.00, 3.61],
                  [1.90, 3.56]],
}  # fmt: skip
LYNX_WL_FT = (2.32, 4.52)
LYNX_WL = [  # x (m); WL2, WL3 (ft)
    (-12.86, 0.28, None), (-11.75, 1.36, 0.70), (-10.58, 2.70, 1.38), (-9.44, 4.13, 2.20),
    (-8.29, 5.65, 3.10), (-7.11, 6.93, 4.10), (-5.96, 7.92, 5.00), (-4.81, 8.68, 5.81),
    (-3.65, 9.29, 6.48), (-2.47, 9.69, 6.94), (-1.32, 9.99, 7.33), (-0.18, 10.21, 7.54),
    (0.99, 10.31, 7.61), (2.15, 10.24, 7.43), (3.29, 9.96, 7.00), (4.46, 9.45, 6.37),
    (5.61, 8.61, 5.57), (6.74, 7.57, 4.59), (7.92, 6.34, 3.50), (9.06, 4.96, 2.42),
    (10.24, 3.43, 1.36), (11.36, 1.94, 0.42), (12.51, 0.30, None),
]  # fmt: skip


def _lynx() -> HullSpec:
    return _hull(LYNX, length_waterline_m=26.84, beam_m=7.3, draught_m=3.28)


def _lynx_lines() -> list[tuple[float, float, float]]:
    return [
        (x, depth * FT, hb * FT)
        for x, *wl in LYNX_WL
        for depth, hb in zip(LYNX_WL_FT, wl, strict=True)
        if hb is not None
    ]


def _mean(errors: list[float]) -> float:
    return math.fsum(abs(e) for e in errors) / len(errors)


# Steel's 36 drawn by the rule's default breadth line, the widest point drawn less the table's
# at timbers 30, 29, 27, 25 and 23, metres (measured): her after body keeps a tumblehome of
# 0.42-0.58 m over the top timber to the stern, which §5.3 step 2's default fades to nothing at
# the end stations, so the rule draws her quarters narrow there, outside §14.1's 0.20 m.
# Recorded, never moved: her own file is to carry her main breadth by station (§5.7, S†), drawn
# through. Open for the lead: §14.1's bound read per timber from timber 19 forward, and the after
# body's departure pinned here.
STEEL_36_AFTER_BODY_WIDEST = (-0.420, -0.379, -0.384, -0.340, -0.284)


def test_the_rule_against_steels_36_the_hull_it_was_tuned_on():
    """Steel's 36 (pages-steel-1805-bodies.md §3.1, §5), drawn by the rule's default breadth
    line: the widest point within 0.20 m of the table's at every timber from 19 forward (§14.1),
    the after body's five as recorded above, within a mean of 0.20 m over all seventeen, and the
    band 15 degrees of heel lifts out within a mean of 0.25 m. Drawn with her main breadth by
    station, as her file is to carry it: the widest point is her given main breadth or her rail,
    the side standing out beyond neither by 5 mm (`check` holds the given points themselves to a
    millimetre), and the band within a mean of 0.25 m."""
    widest, band = _steel_36_errors(_steel_36(breadth_line=False))
    assert max(abs(e) for e in widest[5:]) <= 0.20
    assert widest[:5] == pytest.approx(STEEL_36_AFTER_BODY_WIDEST, abs=0.005)
    assert _mean(widest) <= 0.20
    assert len(band) >= 12 and _mean(band) <= 0.25
    widest, band = _steel_36_errors(_steel_36(breadth_line=True))
    assert max(abs(e) for e in widest) <= 0.005
    assert len(band) >= 12 and _mean(band) <= 0.25


def test_the_rule_against_the_64_which_it_was_not_tuned_on():
    """The 64 (Research-Indefatigable §2.3.2): WL2 to WL5 where the band shows them, within a
    mean of 0.20 m."""
    band = _band_errors(_sixty_four(), _sixty_four_lines())
    assert len(band) >= 12 and _mean(band) <= 0.20


def test_the_rule_against_lynx_which_it_was_not_tuned_on():
    """Lynx (pages-chapelle-fig17.md §5.2): WL2 and WL3 where the band shows them, within a mean
    of 0.20 m."""
    band = _band_errors(_lynx(), _lynx_lines())
    assert len(band) >= 12 and _mean(band) <= 0.20
