"""Package 75, SW-2 with SW-2b.2: the smack's hull as drawn (docs/design/Build-Ships.md §5.0 to
§5.3, §5.6, §5.7; tools/ships/hull_smack.py; docs/design/ships-design/pages-chapman-pl59.md).

Her profile and form load from her file, every shape line carries its rung, and every point stands
as the pages note gives it. She has no port gun and no port triple, since neither the plate nor
the sloop's table draws one and the file has no gun, so the tests that hold each port gun to a
triple and each sill to its source's band hold them to nothing, and say so. Her drawn displacement
and depth stand beside the filed ones, reported and never moved, and no figure the physics reads
has moved: everything in her file but `hull.profile` is what it was at the commit before her lines.
"""

from __future__ import annotations

import functools
import json
import math
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from freesail.ship import form
from freesail.ship.loader import load_ship
from freesail.ship.schema import PROFILE_KEYS, _parse_hull

ROOT = Path(__file__).resolve().parents[1]
SMACK = ROOT / "data" / "ships" / "smack.yaml"
NOTE = ROOT / "docs" / "design" / "ships-design" / "pages-chapman-pl59.md"
# The commit before her lines: the file as it stood, its physics to the figure.
BEFORE = "bb60222"
# The hull's keys the physics reads, as they stood at that commit (`physics/hull.py`,
# `physics/sails.py`, `world/lookout.py`, `api/readings.py`): pinned here as well as against git, so
# that a clone without that commit still holds them (Build-Ships.md §5.0 principle 8, §5.6).
PHYSICS_KEYS = {
    "length_waterline_m": 12.2,
    "beam_m": 4.3,
    "draught_m": 1.9,
    "displacement_kg": 46000.0,
    "gm_m": 0.9,
    "clr_x_m": -0.3,
    "lateral_area_m2": 20,
    "hull_speed_kn": 8.5,
    "deck_height_m": 0.75,
    "rudder": {"area_m2": 0.7, "max_angle_deg": 35, "rate_deg_s": 6.0, "span_m": 2.0},
}
# The drawn displacement, tonnes, by the body under the water (pages §5.3): recorded, not moved.
DRAWN_TONNES = {"steel": 53, "plate": 38}
DRAWN_DEPTH_M = 1.45
# Her factors (pages §5.3), for a place in feet on the plate to be found on her.
SWEDISH_FT = 0.2969
LENGTH_RATIO = 12.2 / 11.46
BEAM_RATIO = 4.3 / 4.06

MODULE_PROBE = """
import json, sys
sys.path.insert(0, "tools")
import gen_ships
sys.modules["gen_ships"] = gen_ships
from ships import hull_smack
word = sys.argv[1]
if word != "as built":
    hull_smack.UNDER_WATER = word
hull = json.loads(sys.argv[2])
notes = {}
hull_smack.add_her_lines(hull, notes)
print(json.dumps({
    "word": hull_smack.UNDER_WATER, "profile": hull["profile"], "report": hull_smack.REPORT,
    "notes": notes, "frames": hull_smack.frames_ft(), "module": {
        "wale": hull_smack.WALE_FT, "band": hull_smack.BAND_FT,
        "main": hull_smack.MAIN_BREADTH_FT, "half": hull_smack.HALF_BREADTH_FT,
        "x": hull_smack.STATION_X_FT, "frame_x": hull_smack.FRAME_X_FT,
        "rail": hull_smack.RAIL_FT, "stem": hull_smack.STEM_FT, "stern": hull_smack.STERN_FT,
        "keel": hull_smack.KEEL_FT, "deck": hull_smack.DECK_FT, "rabbet": hull_smack.RABBET_FT,
        "floor": hull_smack.FLOOR_FT, "foot": hull_smack.FRAME_FOOT_FT,
        "aft": hull_smack.BEYOND_AFT_FT, "fore": hull_smack.BEYOND_FORE_FT,
        "between": hull_smack.BETWEEN_FT, "main_between": hull_smack.MAIN_BREADTH_BETWEEN_FT,
    },
}))
"""


@pytest.fixture(scope="module")
def raw():
    return yaml.safe_load(SMACK.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def ship():
    return load_ship(str(SMACK))


@pytest.fixture(scope="module")
def hull(ship):
    return ship.spec.hull


def _her_hull_without_lines(raw):
    return {k: v for k, v in raw["hull"].items() if k != "profile"}


def _module(raw, word="as built"):
    """The module run as the generator runs it, on her hull without its lines: what it makes, its
    report and its notes. In its own process, so that its `gen_ships` is the one it imports."""
    return _module_run(json.dumps(_her_hull_without_lines(raw)), word)


@functools.cache
def _module_run(hull_json, word):
    """One run of the module, by the hull and the word it was given, so that each runs once."""
    run = subprocess.run(
        [sys.executable, "-c", MODULE_PROBE, word, hull_json],
        check=True,
        cwd=ROOT,
        capture_output=True,
        encoding="utf-8",
        env={**os.environ, "PYTHONIOENCODING": "utf-8"},
    )
    return json.loads(run.stdout)


@pytest.fixture(scope="module")
def built(raw):
    return _module(raw)


def _note_blocks():
    """The note's §5.3 blocks: the file's own, the plate's frames as ruled, and the sloop's, the
    check."""
    text = NOTE.read_text(encoding="utf-8")
    section = text[text.index("### 5.3 Carried to the file") : text.index("## 6. Against")]
    return [yaml.safe_load(b) for b in re.findall(r"```yaml\n(.*?)```", section, flags=re.S)]


def _flat(stations):
    return [point for station in stations for point in station]


def _table_rows(heading, until):
    """The rows of the note's table under `heading`, each its cells as written."""
    text = NOTE.read_text(encoding="utf-8")
    start = text.index(heading)
    section = text[start : text.index(until, start)]
    rows = [line for line in section.splitlines() if line.startswith("|")]
    return [[c.strip() for c in row.strip("|").split("|")] for row in rows]


def _feet(cell):
    """The first figure of a note's cell, its minus sign the note's own."""
    return float(re.search(r"[−-]?\d+\.\d+", cell).group().replace("−", "-"))


def _between(start, until):
    """The note's text from `start` up to `until`, on one line."""
    text = NOTE.read_text(encoding="utf-8")
    at = text.index(start)
    return " ".join(text[at : text.index(until, at)].split())


def _pairs(text):
    """Every 'x, z' of the note's text, as numbers."""
    found = re.findall(r"(−?\d+\.\d+), (−?\d+\.\d+)", text)
    return {(float(a.replace("−", "-")), float(b.replace("−", "-"))) for a, b in found}


def _spec(raw, profile):
    """Her hull as the load reads it, with `profile` for its lines."""
    return _parse_hull({**_her_hull_without_lines(raw), "profile": profile}, "the test")


def _x(feet):
    return round(feet * SWEDISH_FT * LENGTH_RATIO, 2)


def _body(feet):
    return feet * SWEDISH_FT * BEAM_RATIO


# -- her profile and form load ---------------------------------------------------------------


def test_her_profile_and_form_load_raked_and_rounded_with_no_head(hull):
    p = hull.profile
    assert p is not None
    assert p.form.stern.type == "raked"
    assert p.form.stern.transom_hb_m == (0.78, 0.93)  # §5.7's figure, at the plate's own size
    assert p.form.stern.round_up_m == 0.11
    assert p.form.head == "none"
    assert not p.head_m and not p.form.stern.galleries_m and not p.form.stern.lights_m
    assert not p.form.fullness  # the sections draw the ends
    lines = form.check(hull)
    assert any("drawn displacement" in line for line in lines)
    assert form.stations(hull)


def test_her_file_says_what_it_stands_on_and_no_figure_a_rule_computes(raw):
    """The notes carry sources, departures and judgements; what a rule computes from the file's
    own keys is the report's (the lead's notes of 2026-10-29, item 2)."""
    text = SMACK.read_text(encoding="utf-8")
    block = text[text.index("  # Her lines, drawn only") : text.index("\nspars:")]
    notes = re.findall(r"^ *# (.*)$", block, flags=re.M)
    assert len(notes) >= 15
    joined = " ".join(notes)
    for word in ("Chapman 1768", "pages-chapman-pl59.md", "Steel", "judgement", "§5.7"):
        assert word in joined, word
    for computed in (" t against", "drawn displacement", "1.0646", "1.0591", "+15%", "-18%"):
        assert computed not in joined, computed


# -- a mark on every shape line --------------------------------------------------------------


def test_every_line_she_gives_carries_its_rung(raw):
    p = raw["hull"]["profile"]
    marks = p["marks"]
    given = [k for k in PROFILE_KEYS if k in p and k not in ("form", "marks")]
    assert set(given) <= set(marks)
    for group in p["form"]:
        assert f"form.{group}" in marks
    for key in p["form"]["stern"]:
        if key != "type":
            assert f"form.stern.{key}" in marks
    assert set(marks.values()) == {"stand-in", "judged"}  # S† and T: no line of hers is S or R
    judged = {k for k, word in marks.items() if word == "judged"}
    # each a judgement at its weakest point, which its note names (pages §5.1): the side's height
    # and every line that ends on the rail; the water at 3 and ⊕; which band is the wale; frame H's
    # place; the transom's half-breadths at the plate's own size; and the four first so marked
    assert judged == {
        "rail_m",
        "breadth_m",
        "stem_m",
        "stern_m",
        "wales_m",
        "section_m",
        "decks_m",
        "breadth_line_m",
        "sections_m",
        "channel_wales_m",
        "floor_m",
        "rabbet_m",
        "form.stern.transom_hb_m",
    }
    # the rest wholly the plate's by principle 7's own factors
    assert {k for k, word in marks.items() if word == "stand-in"} == {
        "keel_m",
        "form.stern",
        "form.stern.knuckle_z_m",
        "form.stern.round_up_m",
        "form.head",
    }


# -- the port guns and their sills: she has none -----------------------------------------------


def test_she_has_no_port_gun_and_no_port_triple(ship, hull):
    """Each port gun on a triple of its deck within 0.01 m (§5.6): she has no gun at this commit,
    and the plate and the table draw no port (pages §4.16), so there is nothing to stand on one."""
    assert ship.spec.armament is None
    assert not hull.profile.ports_m and not hull.profile.port_size_m


def test_no_source_gives_her_a_sill(hull):
    """Each sill in its source's band, the source in a comment (§5.6). No source gives hers:
    Chapman's Pl. LIX No. 3 draws no port on the side or in the body plan (pages §4.16), Steel's
    sloop has none (Folio I's row Q and Folio XXXII's port rows are blank for her), and the file's
    guns land at SW-4 as rail guns, by `rail_at`, with no triple (Build-Ships.md §5.1, §9.1). So her
    side's height is judged, `rail_m` says so, and its note says why."""
    assert not hull.profile.ports_m
    assert not form.check(hull)[2:]  # no port's gap to report beside the displacement and depth


def test_her_port_triples_gaps_are_reported_as_none(built):
    assert any(line.startswith("her port triples: none") for line in built["report"])
    assert not any("port at x" in line or "deck's ports" in line for line in built["report"])


# -- each point against the note --------------------------------------------------------------


def test_each_point_stands_as_the_notes_block_gives_it(raw):
    """The file against the note's §5.3, line by line, the plate's frames under the water."""
    file_block, _sloop_block = _note_blocks()
    p = raw["hull"]["profile"]
    assert list(p) == [k for k in PROFILE_KEYS if k in p]
    assert set(p) == set(file_block)
    for key, line in file_block.items():
        want = _flat(line) if key == "sections_m" else line
        assert p[key] == want, key


def test_the_lead_ruled_the_plates_frames_and_the_sloop_stands_one_word_away(raw, built):
    """The lead's ruling of 2026-10-31 (pages §5.2): `UNDER_WATER` is "plate", sourced points over
    the rule. The module's one word still gives the sloop, the check, as the note gives it: the rest
    of her lines as they are, the marks and the file's checks unchanged."""
    assert built["word"] == "plate"
    made = _module(raw, "steel")
    _file_block, sloop_block = _note_blocks()
    assert made["word"] == "steel"
    assert made["profile"]["sections_m"] == _flat(sloop_block["sections_m"])
    for key in made["profile"]:
        if key != "sections_m":
            assert made["profile"][key] == built["profile"][key], key
    tonnes = [line for line in made["report"] if "drawn displacement" in line]
    assert f"drawn displacement {DRAWN_TONNES['steel']} t against the filed 46 t" in tonnes[0]


def test_the_module_makes_what_the_file_holds(raw, built):
    assert built["profile"] == raw["hull"]["profile"]
    assert {f"profile.{k}" for k in ("rail_m", "sections_m", "form.stern", "marks")} <= set(
        built["notes"]
    )


def test_the_modules_feet_are_the_notes_tables(built):
    """The module's tables against the note's §4, so that §5.3's block is not its own witness."""
    m = built["module"]
    # §4.10: the frames by level
    rows = _table_rows("### 4.10 The frames by station", "### 4.11")
    stations = rows[0][1:]
    assert stations == ["14", "12", "9", "6", "3", "⊕", "C", "F", "H"]
    x_row = next(r for r in rows if r[0] == "x")
    for st, cell in zip(stations, x_row[1:], strict=True):
        assert m["frame_x"][st] == _feet(cell), st
    levels = [r for r in rows if re.match(r"[−-]?\d+\.\d+ \(", r[0])]
    assert len(levels) == 18
    for row in levels:
        z = _feet(row[0])
        for st, cell in zip(stations, row[1:], strict=True):
            on = dict(map(tuple, built["frames"][st]))
            if cell:
                assert on[z] == _feet(cell), (st, z)
            else:
                assert z not in on, (st, z)
    # §4.2: the wale and the second band at each station (its columns as the table has them)
    for row in _table_rows("### 4.2 By station", "### 4.3")[2:]:
        st = row[0]
        x = m["x"][st]
        band_foot, band_top, wale_up, wale_low = (_feet(row[i]) for i in (4, 3, 7, 8))
        assert [x, wale_low, wale_up] in m["wale"], st
        assert [x, band_foot, band_top] in m["band"], st
    # §4.6: the rail's and the water's half-breadths by station
    for row in _table_rows("### 4.6 The half-breadths", "- **Corrected, 2026-10-30**")[2:]:
        st = row[0]
        assert m["x"][st] == _feet(row[1]), st
        assert m["half"][st] == [_feet(row[3]), _feet(row[4])], st
    # §4.11: the main breadth's height and half-breadth, at the frame's own place
    for row in _table_rows("### 4.11 The main breadth's height", "### 4.12")[2:]:
        st = row[0]
        assert m["frame_x"][st] == _feet(row[1]), st
        assert m["main"][st] == [_feet(row[2]), _feet(row[3])], st


def test_the_modules_other_lines_are_the_notes_too(built):
    """The rest of §5.3's block against §4: the rail, the ends, the keel, the deck, the rabbet, the
    floor, the frames' feet and the plan's lines beyond and between the stations."""
    m = built["module"]
    # §4.3 and §4.14: the rail, from the transom's side to the bow, and the taffrail's sweep
    cells = [c for row in _table_rows("### 4.3 The sheer", "The lowest reading")[2:] for c in row]
    listed = {(_feet(a), _feet(b)) for a, b in zip(cells[0::5], cells[1::5], strict=True) if a}
    listed |= {(_feet(a), _feet(b)) for a, b in zip(cells[3::5], cells[4::5], strict=True) if a}
    sweep, side, stop = m["rail"][:3], m["rail"][3:-2], m["rail"][-2:]
    assert all(tuple(p) in listed for p in side)
    heavy = _between("| Heavy, forward |", "| Middle |")
    assert all(tuple(p) in _pairs(heavy) for p in sweep)
    assert stop == [[18.13, 7.04], [18.16, 8.26]]  # the head's after edge, pages §4.5, §5
    # §4.5: the stem, the stern and the keel
    stem = _between("**The stem's fore edge**", "**The stem head**")
    assert all(tuple(p) in _pairs(stem) for p in m["stem"][:-1])
    assert m["stem"][-1] == [19.47, 8.68]
    stern = _between("**The stern**, low to high", "**The keel's lower edge**")
    assert all(tuple(p) in _pairs(stern) for p in m["stern"])
    keel = _between("**The keel's lower edge**", "In a frame level with the water")
    assert all(tuple(p) in _pairs(keel) for p in m["keel"])
    # §4.4: the deck at side, after and fore
    decks = _between("- **The after deck**", "- **No deck line**")
    decks += _between("- **The fore deck**", "At its after end")
    found = re.findall(r"(−?\d+\.\d+)(?: \(first 16\.32\))?: (−?\d+\.\d+)", decks)
    listed = {(float(a.replace("−", "-")), float(b.replace("−", "-"))) for a, b in found}
    assert all(tuple(p) in listed for p in m["deck"])
    # §4.12: the rabbet's upper line, along the keel and up the stem
    rows = _table_rows("### 4.12 The keel and the rabbet", "- **Up the stem**")[2:]
    along = {(_feet(r[1]), _feet(r[2])) for r in rows}
    up = _pairs(_between("- **Up the stem**", "then nearly"))
    assert all(tuple(p) in along | up for p in m["rabbet"])
    # §4.13: the floor, z from the profile's heavy curve, its half-breadth at the crossing
    rows = {r[0]: r for r in _table_rows("### 4.13 The diagonals", "It crosses the frames")[2:]}
    for st, z, hb in m["floor"]:
        if st == "⊕":
            assert z == _feet(rows["⊕, after"][4]) == _feet(rows["⊕, fore"][4])
            assert hb == pytest.approx(
                (_feet(rows["⊕, after"][3]) + _feet(rows["⊕, fore"][3])) / 2.0, abs=0.001
            )
        else:
            assert z == _feet(rows[st][4]) and hb == _feet(rows[st][3]), st
    # §4.10: each frame's foot on the rabbet
    feet = _between("where each frame's foot is", "frames' heads, the")
    for st, (z, hb) in m["foot"].items():
        assert f"{st}: {z:.2f}, {hb:.2f}".replace("-", "−") in feet, st
    # §4.6: the plan's lines beyond the stations, x, main breadth, rail, the water
    beyond = _between("- **The lines beyond the stations**", "Forward of about 17.4")
    for x, water, rail in [*m["aft"][2:], *m["fore"][:2], m["fore"][3]]:
        said = re.search(
            rf"{f'{x:.2f}'.replace('-', '−')} \([^)]*\): [\d.]+, ([\d.]+), ([\d.]+)", beyond
        )
        assert (float(said.group(1)), float(said.group(2))) == (rail, water), x
    # §4.6: the water's closure on the post, and the lines between the stations (the review's)
    closure = _between("- **The water's closure on the post**", "So the water line")
    for x, water, rail in m["aft"][:2]:
        assert f"{f'{x:.2f}'.replace('-', '−')}: {water:.2f}, {rail:.2f}" in closure, x
    said = _between("- **The lines between the stations**", "Only at 14.70")
    assert m["between"] == [[-15.4, 4.3, 4.67], [11.5, 6.07, 6.07], [14.7, 4.33, 5.2]]
    for piece in (
        "−15.40: 5.00 (4.99), 4.67 (4.66), 4.30 (4.28)",
        "11.50: 6.45 (6.44), and the rail and the LWL lying as one, 6.07 (6.07)",
        "14.70: 5.51 (5.52), 5.20 (5.21), 4.33 (4.36)",
    ):
        assert piece in said, piece
    assert m["main_between"] == [14.7, 5.51]
    # §4.2: the wale's ends and the second band's
    ends = _between("The wale's ends: aft,", "### 4.3")
    assert m["wale"][0] == [-19.18, 2.0, 2.03] and "−19.18, lower 2.00, upper 2.03" in ends
    assert m["wale"][1] == [-18.34, 1.02, 1.93] and "x −18.34, lower 1.02, upper 1.93" in ends
    assert m["wale"][-1] == [18.89, 3.11, 4.04] and "x 18.89, lower 3.11, upper 4.04" in ends
    assert m["band"][0] == [-20.96, 4.57, 4.83] and "x −20.96, foot 4.57, top 4.83" in ends
    assert m["band"][-1] == [18.86, 6.28, 6.54] and "x 18.86, foot 6.28, top 6.54" in ends


# -- the side above the water, and what the lead's ruling moves ---------------------------------


def test_the_plate_draws_her_above_the_water_under_either_body(raw, built):
    """§5.7 first gave the sloop under the water alone, and sourced points win (§5.0 principle 5):
    above the water both bodies draw the plate's frames, so that the lead's ruling moved nothing
    there the eye can tell (pages §5.3). They are given at the sloop's timbers under the sloop's
    body, a station with a point of its own being carried from no other."""
    steel = _spec(raw, _module(raw, "steel")["profile"])
    plate = _spec(raw, _module(raw, "plate")["profile"])
    off, near = [], []
    for s in form.stations(plate)[1:-1]:
        x = s[0][0]
        if not -5.7 < x < 5.7:
            continue
        top = min(s[-1][1], 1.3)
        for z in (0.1 * k for k in range(1, 14)):
            if z < top:
                d = form.half_breadth_at(steel, x, z) - form.half_breadth_at(plate, x, z)
                off.append(d)
                if abs(x) < 5.0:
                    near.append(d)
    assert len(off) > 200
    assert math.sqrt(sum(d * d for d in off) / len(off)) < 0.02
    assert max(abs(d) for d in near) < 0.03
    assert max(abs(d) for d in off) < 0.08  # at 14 and H, at the ends of the sloop's timbers
    # and each body against the frames themselves, at the plate's stations
    m, frames = built["module"], built["frames"]
    for spec, largest in ((plate, 0.01), (steel, 0.08)):
        for st, points in frames.items():
            for z, hb in points:
                if z > 0.0:
                    drawn = form.half_breadth_at(spec, _x(m["frame_x"][st]), _body(z))
                    assert drawn == pytest.approx(_body(hb), abs=largest), (st, z)


def test_the_sloops_timbers_end_on_a_flat_foot_and_the_plates_frames_do_not(raw):
    """One reason for the lead's ruling, and not mended in the check: the table gives no point below
    its first diagonal and the plate's midship section stops above it, so the sloop's timbers end
    about a metre out from the middle line from x -1.6 to x 4.2; no foot of the sloop's fits on the
    plate's keel (pages §5.2). Each of the plate's frames comes down to its keel. If the rule is
    changed, this says so."""
    steel = _spec(raw, _module(raw, "steel")["profile"])
    plate = _spec(raw, _module(raw, "plate")["profile"])

    def foot(spec, x):
        s = min(form.stations(spec)[1:-1], key=lambda s: abs(s[0][0] - x))
        return s[0][2]

    for x in (-1.62, -0.65, 0.36, 2.21, 3.21, 4.19):
        assert foot(steel, x) > 0.8, x
    assert foot(steel, 1.37) < 0.1  # the plate's ⊕ rules at midships: the notch in the bottom
    for x in (-5.33, -4.36, -2.91, -1.45, 0.01, 1.37, 2.73, 4.19, 5.21):
        assert foot(plate, x) < 0.1, x


def test_the_plans_water_closes_on_the_post_and_stands_on_the_plan_between_the_stations(
    hull, built
):
    """The plate's water by the plan's own columns, not straight from station to station: its run
    and its entry curve (pages §4.6, principle 2), and it closes on the post's half-siding."""
    m = built["module"]
    for x, water, rail in [*m["aft"], *m["between"]]:
        assert form.half_breadth_at(hull, _x(x), 0.0) == pytest.approx(_body(water), abs=0.006), x
        at = next(b for b in hull.profile.breadth_m if b[0] == _x(x))
        assert at[2] == pytest.approx(_body(rail), abs=0.006), x
    # abaft the closure it runs on down the post, no fuller than the post's half-siding there
    assert form.half_breadth_at(hull, -5.9, 0.0) < _body(0.26)
    # the main breadth between F and H, at the plan's half-breadth (pages §4.6)
    x, hb = m["main_between"]
    assert [b[2] for b in hull.profile.breadth_line_m if b[0] == _x(x)] == [
        pytest.approx(_body(hb), abs=0.006)
    ]


def test_the_wales_after_end_lies_on_the_counters_curve(hull):
    """Its upper line runs on abaft the scroll to the curve carrying the counter along the side, and
    the band's end is that curve (pages §4.2); it stands on the drawn side there."""
    first, second = hull.profile.wales_m[:2]
    assert first[0] < second[0] and first[1] > second[1] and first[2] > second[2]
    assert first[2] - first[1] < 0.02  # a point, not a square end
    assert form.half_breadth_at(hull, first[0], first[2]) > 0.0


# -- the drawn hull beside the file ------------------------------------------------------------


def test_her_drawn_displacement_and_depth_are_reported_beside_the_filed_ones(hull, built, capsys):
    """Recorded, never moved (§5.0 principle 8): the plate's frames, as the lead ruled, draw her
    38 t against the filed 46 t, 18% under and past the line's 15%, which the report says; the
    sloop, the check, drew her 15% over; neither moves `displacement_kg` or `draught_m`."""
    drawn_kg = form.drawn_displacement_kg(hull)
    deepest = min(pt[1] for s in form.stations(hull)[1:-1] for pt in s)
    with capsys.disabled():
        print(f"\nsmack: {built['report'][0]}")
        for line in built["report"][1:]:
            print(f"smack: {line}")
    assert round(drawn_kg / 1000.0) == DRAWN_TONNES[built["word"]]
    assert hull.displacement_kg == 46000.0
    lines = form.check(hull)
    assert lines[0] == (
        "drawn displacement 38 t against the filed 46 t (-18%), more than 15% off: recorded, not "
        "moved"
    )
    assert f"drawn {DRAWN_DEPTH_M:.2f} m deep at the greatest section" in lines[1]
    assert "the file's draught of 1.9 m" in lines[1]
    assert deepest < -DRAWN_DEPTH_M  # the depth said is the greatest section's, not the keel's
    assert built["report"][1:3] == [
        f"the hull as drawn (freesail/ship/form.py): {lines[0]}.",
        f"the hull as drawn (freesail/ship/form.py): {lines[1]}.",
    ]


def test_the_drawn_hull_is_her_files_length_and_beam(hull):
    """Principle 7: the plate carried to her, so that her masts sit true on it."""
    p = hull.profile
    aft, fore = form._end_x(p, "aft", 0.0), form._end_x(p, "fore", 0.0)
    assert fore - aft == pytest.approx(hull.length_waterline_m, abs=0.02)
    assert max(hb for _x, hb, _r in p.breadth_m) * 2.0 == pytest.approx(hull.beam_m, abs=0.01)


def test_the_stem_head_stands_narrow_and_square_as_the_plate_draws_it(hull):
    """The head's top is the plate's from its after edge, and only the head's half-siding wide; the
    rail on along its side is drawn below it (pages §4.5, §4.6, §5.3)."""
    p = hull.profile
    assert p.rail_m[-1] == (5.74, 2.6) and p.stem_m[-1] == (6.15, 2.74)
    assert form.half_breadth_at(hull, 5.76, 2.5) == pytest.approx(0.09, abs=0.005)
    assert form.half_breadth_at(hull, 5.76, 2.2) == pytest.approx(0.57, abs=0.03)
    assert form.half_breadth_at(hull, 5.73, 2.1) == pytest.approx(0.63, abs=0.03)


# -- nothing the physics reads has moved -------------------------------------------------------


def test_no_figure_the_physics_reads_has_moved_by_the_pins(raw):
    hull = _her_hull_without_lines(raw)
    assert hull == PHYSICS_KEYS
    assert list(hull) == list(PHYSICS_KEYS)  # the existing keys keep their order: §5.1


HEAD_SAYS = (
    "# Her drawn hull, the profile: Chapman 1768 Pl. LIX No. 3, a stand-in for the type\n"
    "# (docs/design/ships-design/pages-chapman-pl59.md; tools/ships/hull_smack.py), drawn\n"
    "# only.\n"
)


def test_her_file_but_for_her_lines_is_what_it_was_against_git(raw):
    """A diff of her file against the commit before her lines: `hull.profile` added last of the
    hull's keys, with its notes, and not a byte else (Build-Ships.md §5.0 principle 8, §5.6). SW-4,
    which brings her fits (§9.1), moves this file by design, and rebases this and the test of her
    having no gun."""
    run = subprocess.run(
        ["git", "show", f"{BEFORE}:data/ships/smack.yaml"],
        cwd=ROOT,
        capture_output=True,
        encoding="utf-8",
    )
    if run.returncode != 0:
        pytest.skip(f"no {BEFORE} in this clone: the pins above hold her figures")
    was = run.stdout.replace("\r\n", "\n")
    now = SMACK.read_text(encoding="utf-8").replace("\r\n", "\n")
    before = yaml.safe_load(was)
    after = {**raw, "hull": _her_hull_without_lines(raw)}
    assert after == before
    assert list(after) == list(before)
    # the file's head says where her lines are, as the cutter's does; that sentence and no more
    assert now.count(HEAD_SAYS) == 1
    now = now.replace(HEAD_SAYS, "")
    start = now.index("  # Her lines, drawn only")
    end = now.index("spars:\n", start)
    assert now[:start] + now[end:] == was
