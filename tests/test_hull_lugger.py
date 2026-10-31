"""Package 75, SW-2 with SW-2b.2: the lugger's hull as drawn (docs/design/Build-Ships.md §5).

`tools/ships/hull_lugger.py` writes her profile, form and marks into `data/ships/lugger.yaml`; the
pages note `docs/design/ships-design/pages-zaz6306.md` (the note) holds every reading behind them.
These tests hold the three to each other, and hold what §5.0 principle 8 binds: the drawing moves
nothing the physics reads. What the form computes from her keys is reported here and in the
generator's report, never in her notes. Run with `-s` to see the report.
"""

from __future__ import annotations

import copy
import math
import re
import subprocess
from pathlib import Path

import pytest
import yaml

from freesail.ship import form as drawn
from freesail.ship.loader import load_ship, spec_from_dict
from freesail.ship.profile import deck_at, interp, rail_at

ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / "data" / "ships" / "lugger.yaml"
NOTE = ROOT / "docs" / "design" / "ships-design" / "pages-zaz6306.md"
FT = 0.3048
# The middle of ZAZ6306's two perpendiculars, feet from the after one, and the fore one (§3.2).
MID_FT, FP_FT = 29.63, 59.26
# Her file as it stood before the hull step, the commit the step was cut from.
BEFORE = "bb60222"
# The factors, the note's §6.2: sections by her moulded 20 ft 0 in over Le Coureur's 21 ft 10¾ in,
# her own 2 in of plank.
SECTIONS_FACTOR = 0.9135
PLANK_FT = 2.0 / 12.0
ROUNDED_M = 0.0051  # the file's centimetre, and a little
# A figure of §5.2's table, read to ±0.05 ft (0.015 m), against §6.1's list, within this.
READ_M = 0.011

SHAPE_MARKS = {
    "rail_m": "sourced",
    "breadth_m": "judged",
    "keel_m": "judged",
    "stem_m": "judged",
    "stern_m": "judged",
    "wales_m": "judged",
    "section_m": "stand-in",
    "decks_m": "judged",
    "breadth_line_m": "judged",
    "sections_m": "judged",
    "rabbet_m": "stand-in",
    "form.stern": "sourced",
    "form.head": "sourced",
}


@pytest.fixture(scope="module")
def doc() -> dict:
    return yaml.safe_load(FILE.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def profile(doc) -> dict:
    return doc["hull"]["profile"]


@pytest.fixture(scope="module")
def spec():
    return load_ship(FILE).hull.spec


@pytest.fixture(scope="module")
def note() -> str:
    return NOTE.read_text(encoding="utf-8")


# -- reading the note -------------------------------------------------------------------------

_NUMBER = r"[−-]?\d+\.\d+"
_POINT = re.compile(rf"\[({_NUMBER}(?:, {_NUMBER})+)\]")


def _figure(word: str) -> float:
    return float(word.replace("−", "-"))


def _points(text: str) -> list[list[float]]:
    """Every point in the text in the note's form, [x, z] or [x, z, hb], its figures to the
    hundredth; a form's words, as [x, z, hb], are no point."""
    return [[_figure(v) for v in m.group(1).split(", ")] for m in _POINT.finditer(text)]


def _part(note: str, heading: str) -> str:
    """One numbered part of the note, from its heading to the next at its level or above."""
    level = heading.split(" ", 1)[0]
    start = note.index(f"\n{heading}")
    rest = note[start + 1 + len(heading) :]
    stop = re.search(rf"\n#{{1,{len(level)}}} ", rest)
    return rest[: stop.start()] if stop else rest


def _bullet(part: str, key: str) -> str:
    """A key's bullet in §6: from `- **`key`**` to the next bullet at its level or a blank line."""
    start = part.index(f"- **`{key}`**")
    rest = part[start + 1 :]
    stop = re.search(r"\n- \*\*|\n\n", rest)
    return rest[: stop.start()] if stop else rest


def _table(part: str, first_cell: str) -> list[list[str]]:
    """The rows of the Markdown table whose header's first cell is `first_cell`, split in cells."""
    lines = part.splitlines()
    start = next(i for i, ln in enumerate(lines) if ln.startswith(f"| {first_cell} |"))
    rows = []
    for ln in lines[start + 2 :]:
        if not ln.startswith("|"):
            break
        rows.append([c.strip() for c in ln.strip().strip("|").split("|")])
    return rows


def _value(cell: str) -> float | None:
    """A table's cell as a number, ignoring what follows it in words; None for no plain figure."""
    m = re.match(rf"^({_NUMBER})(?: \(.*\))?$", cell)
    return _figure(m.group(1)) if m else None


def _feet_at(ft_from_ap: float) -> float:
    """A place in feet from her sheet's after perpendicular as §6's x, metres."""
    return (ft_from_ap - MID_FT) * FT


def _plank_on(ft: float) -> float:
    """A half-breadth read on Le Coureur, in feet, at the factors with her own plank on, metres."""
    return (SECTIONS_FACTOR * ft + PLANK_FT) * FT


def _coureur(note: str) -> tuple[dict, dict, dict]:
    """§11.4 by station: the sheer's row, the half-breadths' row, and the curve as read, a list of
    (feet above line A, half-breadth in feet) low to high."""
    part = _part(note, "### 11.4 ZAZ6170 by station")
    sheer = {row[0]: row for row in _table(part, "Stn")}
    breadths = {row[0]: row for row in _table(part, "Stn | Half-breadth at A")}
    heads = next(ln for ln in part.splitlines() if ln.startswith("| Stn | +6"))
    heights = [_figure(h.replace("+", "")) for h in heads.strip("| ").split(" | ")[1:]]
    curves = {
        row[0]: sorted((h, _figure(v)) for h, v in zip(heights, row[1:], strict=True) if v)
        for row in _table(part, "Stn | +6")
    }
    return sheer, breadths, curves


def _stations(note: str) -> list[tuple[str, float, list[list[float]]]]:
    """§6.2's table: each of Le Coureur's stations, its x, its points."""
    rows = _table(_part(note, "### 6.2 Under the water"), "Stn")
    return [(stn, _figure(x.replace("+", "")), _points(points)) for stn, x, points in rows]


# -- her profile and form load ----------------------------------------------------------------


def test_her_profile_and_form_load_and_draw(spec, profile):
    """§5.1: round at the rail, no counter, no head (S); the schema's form, drawn by the rule."""
    p = spec.profile
    assert p is not None
    assert list(profile)[:2] == ["rail_m", "breadth_m"]
    assert p.form.stern.type == "round" and p.form.stern.transom_hb_m is None
    assert p.form.stern.galleries_m == () and p.form.stern.lights_m == ()
    assert p.form.head == "none" and p.head_m == ()
    lines = drawn.check(spec)
    assert lines[0].startswith("drawn displacement")
    assert len(drawn.stations(spec)) >= len(p.breadth_m)


def test_her_rail_steps_as_her_sheet_draws_it(profile):
    """ZAZ6306 (the note's §5.1): raised aft to 15.07 ft from the after perpendicular by 1.83 ft and
    forward from 43.04 ft by 0.83 ft, the only two steps; the rest a fair sheer."""
    rail = profile["rail_m"]
    jumps = [(a, b) for a, b in zip(rail, rail[1:], strict=False) if b[0] - a[0] < 0.02]
    assert [(a[0], b[0]) for a, b in jumps] == [(-4.44, -4.43), (4.09, 4.1)]
    assert jumps[0][0][1] - jumps[0][1][1] == pytest.approx(1.83 * FT, abs=0.01)
    assert jumps[1][1][1] - jumps[1][0][1] == pytest.approx(0.83 * FT, abs=0.01)
    assert rail[0] == profile["stern_m"][-1]  # the taffrail, the post's top


# -- a mark on every shape line ---------------------------------------------------------------


def test_every_shape_line_carries_its_rung(profile):
    """§5.0 principle 4: each line says where it came from in one word, its weakest point's; the
    words the note's §6.5 gives. No line goes unmarked and none is marked that is not given."""
    lines = {k for k in profile if k not in ("form", "marks")}
    groups = {f"form.{k}" for k in profile["form"]}
    assert set(profile["marks"]) == lines | groups
    assert profile["marks"] == SHAPE_MARKS


def test_the_marks_are_the_notes(profile, note):
    part = _part(note, "### 6.5 The marks")
    said = re.findall(r"`([\w.]+):\s+(sourced|stand-in|rule|judged)`", part)
    assert dict(said) == profile["marks"]


# -- the guns and the sills -------------------------------------------------------------------


def _port_guns(doc: dict) -> list[tuple[str, dict]]:
    fits = (doc.get("armament") or {}).get("fits") or {}
    return [
        (name, gun)
        for name, fit in fits.items()
        for gun in fit.get("guns") or []
        if gun.get("place") in ("broadside", "bow", "stern")
    ]


def test_each_port_gun_stands_on_a_triple_of_its_deck(doc, spec):
    """§5.3, §5.6. Her file carries no gun today ("guns are not parts until milestone 7": the fit
    "gun lugger 1795" is SW-4's, §9.1), and the pick of the note's §6.4 gives her rail guns, which
    §5.1 gives no port. So the check stands for the fit to come, a port gun on a triple of its
    deck within 0.01 m, and today it holds of none."""
    p = spec.profile
    triples = {word: line for word, line in p.ports_m}
    for fit, gun in _port_guns(doc):
        word = gun["deck"]
        near = [t for t in triples.get(word, ()) if abs(t[0] - gun["x_m"]) <= 0.01]
        assert near, f"{fit}: {gun['id']} stands on no {word} triple"
        assert abs(near[0][1] - gun["height_m"]) <= 0.01, gun["id"]
    assert _port_guns(doc) == [] and p.ports_m == () and p.port_size_m == ()


def test_the_height_a_rail_gun_takes_is_in_its_sources_band(spec):
    """The sill she has none of, by §5.3 a rail gun's height from `rail_at`: the waist rail,
    measured on ZAZ6306 at 4.9 to 5.4 ft above the green line, 1.49 to 1.66 m (the note's §5.4).
    Steel 1805 p. 124's four to five feet for sloops and cutters (Build-Ships.md §5.4, OCR
    `:8268-8271`), 1.22 to 1.52 m, is §5.4's fallback, close under it: her own sheet rules."""
    p = spec.profile
    waist = [x / 10.0 for x in range(-44, 40)]
    heights = [rail_at(p, x) for x in waist]
    assert min(heights) >= 1.49 - ROUNDED_M and max(heights) <= 1.66 + ROUNDED_M


def _fallback(note: str) -> tuple[list[list[float]], list[float]]:
    """The note's §6.4: the triples were ports ever ruled, and their size."""
    part = _part(note, "### 6.4 The ports")
    at = part.index("`ports_m.upper`:")
    triples = _points(part[at:])[:2]
    size = _points(part[part.index("`port_size_m.upper`:") :])[0]
    return triples, size


def _with_fallback(doc: dict, note: str):
    triples, size = _fallback(note)
    d = copy.deepcopy(doc)
    d["hull"]["profile"]["ports_m"] = {"upper": triples}
    d["hull"]["profile"]["port_size_m"] = {"upper": size}
    return spec_from_dict(d, "p.yaml").hull, triples


def test_the_fallback_sills_are_in_their_sources_band_and_its_gaps_are_reported(doc, note):
    """Were ports ever ruled (the note's §6.4, every figure T): each sill above her deck at side
    within ZAZ4735's band for a carronade on the recoil, 0.78 to 1.0 ft above the deck by the black
    line (*Defender* as proposed, the note's §12.5, unscaled), and each triple within 0.05 m of the
    drawn side, the gap reported. None of it is in her file."""
    hull, triples = _with_fallback(doc, note)
    gaps = []
    for x, sill, hb in triples:
        above = sill - deck_at(hull.profile, x)
        assert 0.78 * FT - ROUNDED_M <= above <= 1.0 * FT + ROUNDED_M, x
        assert sill < rail_at(hull.profile, x)
        gap = drawn.half_breadth_at(hull, x, sill) - hb
        gaps.append(gap)
        assert abs(gap) <= drawn.PORT_GAP_M, x
    said = ", ".join(f"x {t[0]:+.2f}: {g:+.2f} m" for t, g in zip(triples, gaps, strict=True))
    print(f"\nlugger: no triple in her file; the fallback's gaps to the drawn side: {said}")


# -- each point against the note --------------------------------------------------------------


@pytest.mark.parametrize(
    "heading, key",
    [
        ("### 6.1 Her own sheet", "rail_m"),
        ("### 6.1 Her own sheet", "breadth_m"),
        ("### 6.1 Her own sheet", "stem_m"),
        ("### 6.1 Her own sheet", "stern_m"),
        ("### 6.1 Her own sheet", "wales_m"),
        ("### 6.2 Under the water", "section_m"),
        ("### 6.2 Under the water", "keel_m"),
        ("### 6.2 Under the water", "rabbet_m"),
        ("### 6.3 The shape keys", "breadth_line_m"),
    ],
)
def test_each_list_of_points_is_the_notes(profile, note, heading, key):
    """§6's lists, the file's to the centimetre."""
    assert _points(_bullet(_part(note, heading), key)) == profile[key]


def test_the_deck_is_the_notes(profile, note):
    text = _bullet(_part(note, "### 6.1 Her own sheet"), "decks_m.upper")
    said = _points(text[: text.index("The deck at the middle line")])
    assert said == profile["decks_m"]["upper"]
    assert list(profile["decks_m"]) == ["upper"]


def test_the_sections_are_the_notes(profile, note):
    rows = _table(_part(note, "### 6.2 Under the water"), "Stn")
    said = [[_figure(row[1])] + pt for row in rows for pt in _points(row[2])]
    assert said == profile["sections_m"]
    assert [row[0] for row in rows] == "12 11 10 9 8 7 6 5 4 3 2 1".split()


def test_the_form_is_the_notes(profile, note):
    part = _part(note, "### 6.3 The shape keys")
    assert "**`form.stern`**: `type: round`" in part and "**`form.head`**: `none`" in part
    assert profile["form"] == {"stern": {"type": "round"}, "head": "none"}


# -- and the points against the note's measures -------------------------------------------------


def test_her_own_lines_are_the_measured_table_in_metres(profile, note):
    """§5.2's table, feet above the green line, into §6.1's metres: the rail, the band, the deck at
    side and the plan's outline at every station they share."""
    rows = _table(_part(note, "### 5.2 By station"), "ft from AP")
    rail = {x: z for x, z in profile["rail_m"]}
    deck = {x: z for x, z in profile["decks_m"]["upper"]}
    wale = {x: (lo, hi) for x, lo, hi in profile["wales_m"]}
    plan = {x: hb for x, _hw, hb in profile["breadth_m"]}
    seen = {"rail": 0, "deck": 0, "wale": 0, "plan": 0}
    for ft_from_ap, x_m, a, b, c, _d, d2, hb in rows:
        x = _figure(x_m.replace("+", ""))
        if (z := _value(a.split(" (")[0])) is not None and x in rail:
            assert rail[x] == pytest.approx(z * FT, abs=READ_M), ft_from_ap
            seen["rail"] += 1
        if (z := _value(d2)) is not None and x in deck:
            assert deck[x] == pytest.approx(z * FT, abs=READ_M), ft_from_ap
            seen["deck"] += 1
        if (lo := _value(c)) is not None and (hi := _value(b)) is not None and x in wale:
            assert wale[x] == pytest.approx((lo * FT, hi * FT), abs=READ_M), ft_from_ap
            seen["wale"] += 1
        if (h := _value(hb)) is not None and x in plan:
            assert plan[x] == pytest.approx(h * FT, abs=READ_M), ft_from_ap
            seen["plan"] += 1
    assert seen["rail"] >= 20 and seen["deck"] == 23 and seen["wale"] == 7 and seen["plan"] >= 14


def test_the_water_and_the_sections_are_le_coureurs_at_the_factors(profile, note):
    """§11.4's body plan and stations through §6.2's factors: each station's place, each point of
    `sections_m` up to the water against the table, straight between its feet of height (the
    table's rows are interpolated from the curves, so 0.05 m), and the keel's foot at the five
    stations the keel's middle points stand on."""
    stations, _breadths, curves = _coureur(note)
    keel = {x: z for x, z in profile["keel_m"]}
    worst, feet = 0.0, []
    for stn, x_said, points in _stations(note):
        ft_ap = _figure(stations[stn][1])
        x = (-0.13 + 0.868 * (ft_ap - 0.40) - MID_FT) * FT
        assert x_said == pytest.approx(x, abs=READ_M), stn  # the factor to its four places
        curve = curves[stn]
        for z, hb in points:
            up = z / FT / SECTIONS_FACTOR
            if z > 0.0 or up < curve[0][0]:  # above the water, or below the table's lowest foot
                continue
            hers = _plank_on(interp(curve, up))
            worst = max(worst, abs(hb - hers))
            assert hb == pytest.approx(hers, abs=0.05), (stn, z)
        foot = _figure(stations[stn][-1]) * SECTIONS_FACTOR * FT
        if x_said in keel:
            assert keel[x_said] == pytest.approx(foot, abs=ROUNDED_M), stn
            feet.append(stn)
    assert feet == ["8", "6", "5", "4", "3"]
    print(f"\nlugger: sections_m against §11.4's table at the factors, the worst {worst:.3f} m")


def test_the_side_above_the_water_is_her_types_curve_moved_to_her_main_breadth(profile, note):
    """§6.2, T: above the water each section is the station's curve at the factors, moved straight
    in height by what her main breadth has over or under Le Coureur's there and never past it,
    and it stops short of the main breadth's height. So her side rounds as her type's does, where
    a straight line from the water to her main breadth would leave a hard corner."""
    _sheer, breadths, curves = _coureur(note)
    main = {x: (z, hb) for x, z, hb in profile["breadth_line_m"]}
    off, count = {}, 0
    for stn, x, points in _stations(note):
        z_main, hb_main = main[x]
        coureurs = _plank_on(_figure(breadths[stn][5]))
        water = dict(map(tuple, points))[0.0]
        for z, hb in points:
            if z <= 0.0:
                continue
            count += 1
            assert z <= z_main - 0.05 + 1e-9, (stn, z)
            moved = _plank_on(interp(curves[stn], z / FT / SECTIONS_FACTOR))
            moved += (hb_main - coureurs) * z / z_main
            assert hb == pytest.approx(min(moved, hb_main), abs=ROUNDED_M), (stn, z)
            chord = water + (hb_main - water) * z / z_main
            off[stn] = max(off.get(stn, 0.0), abs(hb - chord))
    assert count == 44
    assert off["12"] >= 0.2 and off["2"] >= 0.15 and off["3"] >= 0.1  # what the points are for
    assert max(off[stn] for stn in ("9", "8", "7", "6", "5", "4")) <= 0.04 + ROUNDED_M


def test_the_main_breadth_is_le_coureurs_height_on_her_own_plans_breadth(profile, note):
    """§6.3: the height of each station's greatest half-breadth on Le Coureur (§11.4) at the
    factor, the half-breadth her plan's outline with a tumblehome in proportion to it, from the
    caption's 20 ft 4 in less the plan's 19 ft 7 in, halved, amidships."""
    _sheer, breadths, _curves = _coureur(note)
    plan = [(x, hb) for x, _hw, hb in profile["breadth_m"]]
    main = {x: (z, hb) for x, z, hb in profile["breadth_line_m"]}
    tumblehome = (20 + 4 / 12 - (19 + 7 / 12)) / 2 * FT
    fade = 1.0 + tumblehome / max(hb for _x, hb in plan)
    for stn, x, _pts in _stations(note):
        height = float(re.match(r"\+?(\d+\.\d+)", breadths[stn][6]).group(1))
        assert main[x][0] == pytest.approx(height * SECTIONS_FACTOR * FT, abs=ROUNDED_M), stn
        assert main[x][1] == pytest.approx(interp(plan, x) * fade, abs=READ_M), stn
    assert len(main) == 12


def test_the_water_is_the_stations_between_them_and_its_two_ends(profile, note):
    """§6.1: the water's half-breadth, from -8.69 to +8.85, straight between the sections at z = 0
    and §11.4's two ends of line A, read to about 0.1 ft; only the five figures beyond are T."""
    part = _part(note, "### 11.4 ZAZ6170 by station")
    assert "about 1.7 ft half-breadth at about 1.6 ft from AP" in part
    assert "about 0.45 ft at about 68.2 ft from AP" in " ".join(part.split())

    def her_x(ft_ap: float) -> float:
        return (-0.13 + 0.868 * (ft_ap - 0.40) - MID_FT) * FT

    line = [(her_x(1.6), _plank_on(1.7))]
    line += [(x, dict(map(tuple, pts))[0.0]) for _stn, x, pts in _stations(note)]
    line += [(her_x(68.2), _plank_on(0.45))]
    held = [b for b in profile["breadth_m"] if -8.69 <= b[0] <= 8.85]
    assert len(held) == 22 and len(profile["breadth_m"]) - len(held) == 5
    for x, hb_water, _hb_rail in held:
        assert hb_water == pytest.approx(interp(line, x), abs=0.1 * FT), x


def test_the_midship_section_is_station_six_and_her_rail(profile, note):
    """§11.4's station 6 as read, at the factors, up to 0.30 m; the keel's lower edge and the
    half-siding at the foot; her own rail and plan at the top."""
    part = _part(note, "### 11.4 ZAZ6170 by station")
    start = part.index("**Station 6, the section as read**")
    read = sorted((a, b) for a, b in _points(part[start : part.index("**Deadrise 25°**")]))
    section = profile["section_m"]
    between = [pt for pt in section if -2.0 <= pt[0] <= 0.3]
    assert len(between) == 13
    for z, hb in between:
        hers = _plank_on(interp(read, z / FT / SECTIONS_FACTOR))
        assert hb == pytest.approx(hers, abs=0.02), z
    keel = {x: z for x, z in profile["keel_m"]}
    assert section[0][0] == keel[0.27]
    assert section[0][1] == pytest.approx(0.37 * SECTIONS_FACTOR * FT, abs=ROUNDED_M)
    rail = interp([(x, z) for x, z in profile["rail_m"]], 0.0)
    plan = interp([(b[0], b[2]) for b in profile["breadth_m"]], 0.0)
    assert section[-1] == [rail, plan]


def test_the_stem_and_the_post_are_her_measures_in_metres(profile, note):
    """§5.3's fore edge and dashed forefoot and §4's dashed post, feet from her after perpendicular
    into §6.1's metres, and the two feet her dashed lines carry on to the stand-in's keel (T)."""
    ends = " ".join(_part(note, "### 5.3 The ends").split())
    assert "0.90 ft before FP at the line, 1.11 ft from 4 to 6 ft up, 1.02 ft at its top" in ends
    assert "9.57 ft above the line" in ends
    stem, stern, keel = profile["stem_m"], profile["stern_m"], profile["keel_m"]
    at = {z: x for x, z in stem}
    assert at[0.0] == pytest.approx(_feet_at(FP_FT + 0.90), abs=READ_M)
    for z in (1.07, 1.83):
        assert at[z] == pytest.approx(_feet_at(FP_FT + 1.11), abs=READ_M)
    assert stem[-2][0] == pytest.approx(_feet_at(FP_FT + 1.02), abs=READ_M)
    assert stem[-2][1] == pytest.approx(9.57 * FT, abs=READ_M)
    assert stem[-1][0] == pytest.approx(
        _feet_at(FP_FT), abs=READ_M
    )  # the head, at the perpendicular
    sweep = ends[ends.index("forefoot sweeps aft") : ends.index("(measured, tentative, ±0.2 ft)")]
    read = re.findall(r"(\d\.\d\d)(?: ft down)? at (\d\d\.\d\d)", sweep)
    assert len(read) == 6
    for (down, ft), (x, z) in zip(read, stem[1:7][::-1], strict=True):
        assert (x, z) == pytest.approx((_feet_at(float(ft)), -float(down) * FT), abs=READ_M), ft
    table = {row[0]: row for row in _table(_part(note, "## 4. The waterline"), "What")}
    row = table["The post's after edge, dashed, where it meets the strip"]
    said = [_figure(row[1].split("(")[1].rstrip(")")), -float(row[2].split(" ft")[0]) * FT]
    assert stern[1] == pytest.approx(said, abs=READ_M)
    assert stern[2] == [pytest.approx(_feet_at(0.0), abs=READ_M), 0.0]  # the line at her AP
    row = table["The post's fore edge, dashed, at the strip"]
    said = [_figure(row[1].split("(")[1].rstrip(")")), -float(row[2].split(" ft")[0]) * FT]
    assert profile["rabbet_m"][1][:2] == pytest.approx(said, abs=READ_M)
    # the post, carried on at §5.3's 10.8°, and the forefoot at §4's 18°, to the stand-in's keel
    run = math.tan(math.radians(10.8)) * (stern[1][1] - stern[0][1])
    assert stern[0] == keel[0] and stern[0][0] == pytest.approx(stern[1][0] + run, abs=READ_M)
    run = (stem[1][1] - stem[0][1]) / math.tan(math.radians(18.0))
    assert stem[0] == keel[-1] and stem[0][0] == pytest.approx(stem[1][0] - run, abs=2 * READ_M)


def test_the_rabbet_is_le_coureurs_keel_top_at_the_factors(profile, note):
    """§6.2: at each station the rabbet stands from line A by §11.4's depth, at the factor, the
    half-siding hers at the factor."""
    sheer, _breadths, _curves = _coureur(note)
    rabbet = {x: (z, side) for x, z, side in profile["rabbet_m"]}
    held = 0
    for stn, x, _pts in _stations(note):
        if x in rabbet:
            z, side = rabbet[x]
            assert z == pytest.approx(-_figure(sheer[stn][2]) * SECTIONS_FACTOR * FT, abs=READ_M)
            assert side == pytest.approx(0.37 * SECTIONS_FACTOR * FT, abs=ROUNDED_M)
            held += 1
    assert held == 9


# -- reported beside the file, never moved ----------------------------------------------------


def test_the_drawn_hull_is_reported_beside_the_filed_figures(spec):
    """§5.6: the drawn displacement and depth beside the filed ones, recorded and not moved (§5.0
    principle 7). The two read alike in tons partly by coincidence (the note's §13.2)."""
    lines = drawn.check(spec)
    print("\nlugger: " + "; ".join(lines))
    assert spec.displacement_kg == 101000.0 and spec.draught_m == 2.1
    assert drawn.drawn_displacement_kg(spec) == pytest.approx(101500.0, rel=0.02)
    deepest = min(pt[1] for s in drawn.stations(spec) if s[0][0] == 0.0 for pt in s)
    assert deepest == pytest.approx(-2.53, abs=0.03)
    assert "against the file's draught of 2.1 m" in lines[1]


def test_the_note_says_the_ruling_on_her_depth_and_her_length(note):
    """The lead's note of 2026-10-31, point 2: the one factor of principle 7, 2.53 m, as built; the
    departure from principle 7's last sentence said with the 0.793 beside it, her line the re-read's
    18.33 m where the lead's note quotes the first reading's 18.39 m; the hold's floor line a depth
    of hold and no draught."""
    said = " ".join(_part(note, "### 13.4 Ruled by the lead (2026-10-31)").split())
    for words in (
        "the one factor of principle 7, 2.53 m",
        "a departure from principle 7's last sentence",
        "**0.793**",
        "18.33 m (60.14 ft",
        "quotes 18.39 m, the first reading's 60.32 ft",
        "a depth of hold and no draught",
    ):
        assert words in said, words
    assert "a depth of hold and no draught" in " ".join(_part(note, "## 4. The waterline").split())


def test_her_notes_carry_no_figure_a_rule_computes():
    """The lead's ruling (notes of 2026-10-29, item 2): the file's notes carry sources, departures
    and judgements; the drawn displacement, the depth and the gaps are the report's."""
    text = FILE.read_text(encoding="utf-8")
    block = text[text.index("  # Her lines (") : text.index("\nspars:")]
    comments = [ln for ln in block.splitlines() if ln.lstrip().startswith("#")]
    assert len(comments) >= 13
    said = " ".join(comments).lower()
    for word in ("drawn displacement", "against the filed", " deep at", "gap", "-14%", "+0%"):
        assert word not in said, word
    for figure in ("2.53", "101 t", "18.33", "2.98 m"):
        assert figure not in said, figure
    for source in ("ZAZ6306", "ZAZ6170", "0.868", "0.9135", "principle 7"):
        assert source in text[: text.index("\nspars:")], source


# -- nothing the physics reads moved (§5.0 principle 8, §5.6) ---------------------------------

# The hull's figures as filed before the step, kept here for a tree with no history (an archive).
HULL_AS_FILED = {
    "length_waterline_m": 16.8,
    "beam_m": 6.2,
    "draught_m": 2.1,
    "displacement_kg": 101000.0,
    "gm_m": 1.2,
    "clr_x_m": -1.6,
    "lateral_area_m2": 30,
    "hull_speed_kn": 9.9,
    "deck_height_m": 1.0,
    "rudder": {"area_m2": 1.4, "max_angle_deg": 35, "rate_deg_s": 5.0, "span_m": 2.5},
}


def test_no_hull_figure_the_physics_reads_moved(doc):
    hull = {k: v for k, v in doc["hull"].items() if k != "profile"}
    assert hull == HULL_AS_FILED
    assert list(doc["hull"])[-1] == "profile"


def test_the_bowsprits_rating_stands_as_filed_and_the_note_has_old_beside_new(doc, note):
    """The lead's note of 2026-10-30: rule (3)'s words are reported for the lead, and a rating is a
    figure the physics reads, so it is not moved here."""
    sprit = next(s for s in doc["spars"] if s["id"] == "bowsprit")
    assert sprit["rating_kn"] == 21.8
    assert "**old 21.8 kN, 37.4 kN by rule (3)'s words**" in _part(note, "## 7. Against")


def _before() -> dict | None:
    """Her file at the commit the step was cut from; None in a tree with no history."""
    try:
        run = subprocess.run(
            ["git", "show", f"{BEFORE}:data/ships/lugger.yaml"],
            cwd=ROOT,
            capture_output=True,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return yaml.safe_load(run.stdout.decode("utf-8"))


def test_a_diff_of_her_files_physics_keys_against_git_shows_none(doc):
    """Everything the physics reads in her file, its spars, sails, lines and every hull key but the
    profile, as it stood at the commit the step was cut from."""
    old = _before()
    if old is None:
        pytest.skip(f"no git history for {BEFORE} here; HULL_AS_FILED holds the hull's figures")
    assert "profile" not in old["hull"]
    assert {k: v for k, v in doc["hull"].items() if k != "profile"} == old["hull"]
    for section in ("spars", "sails", "lines", "groups", "aliases"):
        assert doc[section] == old[section], section
