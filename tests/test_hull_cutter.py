"""Package 75, the hull step (SW-2 with SW-2b.2; docs/design/Build-Ships.md §5, §5.6, §5.7, §5.9):
the cutter Sherbourne's hull drawn from her own draught.

`tools/ships/hull_cutter.py` holds her points and `data/ships/cutter.yaml` carries them; the sources
are RMG ZAZ6381 and its fellows, read in `docs/design/ships-design/pages-zaz6381.md` (the note).
These tests hold that her profile and form load and draw; that every shape line has its mark; that
each port gun stands on a triple of its deck and each sill in its source's band; that each point
is the note's, and the note's sections meet its plan; that the drawn hull's figures are reported
beside the filed ones; and that nothing the physics or the gunnery reads moved (§5.0 principle 8,
§5.6), against the file as it stood.
"""

from __future__ import annotations

import importlib.util
import math
import re
import subprocess
from pathlib import Path

import pytest
import yaml

from freesail.ship import form as drawn
from freesail.ship.loader import load_ship
from freesail.ship.profile import deck_at, interp, ports_of, rail_at

ROOT = Path(__file__).resolve().parents[1]
CUTTER = ROOT / "data" / "ships" / "cutter.yaml"
NOTE = ROOT / "docs" / "design" / "ships-design" / "pages-zaz6381.md"
FT = 0.3048
# The commit whose file this step left its physics alone against (the lead's note of 2026-10-30).
BASE = "f5be9110"  # the trunk at the landing: bb60222 but for the boats' `file` keys
# The sheet's four ports, x by ZAZ6381 and ZAZ6382 (the note §5.8).
SHEET_PORT_X = (-4.75, -2.35, 0.02, 3.58)
# The file's three guns a side, kept where they stand between those ports (Build-Ships.md §5.3).
GUN_X = (-3.5, -0.5, 2.5)


@pytest.fixture(scope="module")
def ship():
    return load_ship(CUTTER)


@pytest.fixture(scope="module")
def spec(ship):
    return ship.hull.spec


@pytest.fixture(scope="module")
def doc():
    return yaml.safe_load(CUTTER.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def module():
    """Her module on its own: it needs no generator to give its figures."""
    found = importlib.util.spec_from_file_location(
        "hull_cutter_under_test", ROOT / "tools" / "ships" / "hull_cutter.py"
    )
    loaded = importlib.util.module_from_spec(found)
    found.loader.exec_module(loaded)
    return loaded


@pytest.fixture(scope="module")
def six():
    """The note's §6, the points in metres."""
    text = NOTE.read_text(encoding="utf-8")
    return text[text.index("## 6. For the profile") : text.index("## 7. Against")]


def points_in(text):
    """Every bracketed list of numbers in the text, in order."""
    return [
        [float(n) for n in body.split(",")]
        for body in re.findall(r"\[(-?\d+\.\d+(?:, -?\d+\.\d+)+)\]", text)
    ]


def bullet(six, key):
    """The points of one bullet of §6, from the colon after its name to its end."""
    line = next(ln for ln in six.splitlines() if ln.startswith(f"- **`{key}`**"))
    return points_in(line)


def same_points(given, written):
    assert len(given) == len(written)
    for g, w in zip(given, written, strict=True):
        assert len(g) == len(w), (g, w)
        for a, b in zip(g, w, strict=True):
            assert abs(a - b) < 0.005, (g, w)


# ---------------------------------------------------------------------------
# She loads and draws
# ---------------------------------------------------------------------------


def test_her_profile_and_form_load_and_draw(spec, doc):
    p = spec.profile
    assert p is not None
    # a square stern with no head and nothing invented on it (the note §5.5, §5.6; §5.0 principle 9)
    assert p.form.stern.type == "square"
    assert p.form.head == "none"
    assert not p.form.stern.galleries_m and not p.form.stern.lights_m
    assert doc["hull"]["profile"]["form"]["stern"]["transom_hb_m"] == [1.75, 2.02]
    # the viewer's hull: finite, rising, through every given point, or `check` raises in words
    assert any("drawn displacement" in line for line in drawn.check(spec))
    assert list(doc["hull"])[-1] == "profile"  # the existing keys keep their order (§5.1)


def test_a_mark_on_every_shape_line_and_each_by_its_rung(doc):
    """§5.0 principle 4: each line's one word, its weakest point's. S is `sourced`; the keel under
    the strip, the deck at the middle line for the side, the guns' three sills, the three lines
    named by judgement, the rabbet's line and half-siding, and which corner is the knuckle are
    `judged` (the note §6)."""
    profile = doc["hull"]["profile"]
    marks = profile["marks"]
    lines = [key for key in profile if key.endswith("_m")]
    assert set(lines) <= set(marks)
    stern = [f"form.stern.{key}" for key in profile["form"]["stern"] if key != "type"]
    assert set(stern) | {"form.stern", "form.head"} <= set(marks)
    assert set(marks.values()) <= {"sourced", "stand-in", "rule", "judged"}
    judged = {key for key, word in marks.items() if word == "judged"}
    assert judged == {
        "keel_m",
        "decks_m",
        "ports_m",
        "wales_m",
        "channel_wales_m",
        "floor_m",
        "rabbet_m",
        "form.stern.knuckle_z_m",
    }
    assert "stand-in" not in marks.values() and "rule" not in marks.values()


def test_the_stem_head_is_the_box_her_sheets_draw(spec, doc):
    """The note's §5.5: a box above the rail, 1.3 ft fore and aft, its top from 54.5 to 55.88 ft
    from the after perpendicular at 9.21 ft above the line, 0.7 ft across on ZAZ6382. First written,
    the rail ran on to x 8.54 and the side closed straight to the stem head, a pointed fin 0.56 m
    across (the landing's review of the drawing)."""
    p = doc["hull"]["profile"]
    from_ap = 27.16
    assert p["rail_m"][-1] == [8.34, 2.81]  # the box's after edge, its top
    assert p["rail_m"][-2] == [8.33, 2.44]  # where the rail meets it
    assert p["rail_m"][-1][0] == pytest.approx((54.5 - from_ap) * FT, abs=0.01)
    assert p["stem_m"][-1] == [8.75, 2.81]  # its fore edge at its top, the stem head
    assert p["stem_m"][-1][0] == pytest.approx((55.88 - from_ap) * FT, abs=0.01)
    assert p["stem_m"][-1][1] == pytest.approx(9.21 * FT, abs=0.01)
    half_across = 0.5 * 0.7 * FT
    assert p["breadth_m"][-1] == [8.33, 0.11, 0.11]
    assert p["breadth_m"][-1][2] == pytest.approx(half_across, abs=0.005)
    # square across the ship at its after edge to its top, not narrowing up as a fin; in plan the
    # form closes it straight to the fore edge, as every stem head
    for z in (2.5, 2.65, 2.8):
        assert drawn.half_breadth_at(spec, 8.34, z) == pytest.approx(half_across, abs=0.005), z


# ---------------------------------------------------------------------------
# The ports and the guns
# ---------------------------------------------------------------------------


def test_each_port_gun_stands_on_a_triple_of_its_deck(ship, spec):
    """§5.6: within 0.01 m, by its deck. Both fits; every gun's place as it was (no x moves)."""
    p = spec.profile
    for fit in ship.spec.armament.fits.values():
        guns = [g for g in fit.guns if g.place == "broadside"]
        assert {g.deck for g in guns} == {"upper"}, fit.name
        assert sorted({g.x_m for g in guns}) == sorted(GUN_X), fit.name
        for g in guns:
            assert any(
                abs(g.x_m - x) <= 0.01 and abs(g.height_m - z) <= 0.01
                for x, z, _hb in ports_of(p, g.deck)
            ), (fit.name, g.id)


def test_each_swivel_stands_on_the_rail(ship, spec):
    """§5.3: a rail gun has no port; it takes the rail at its x."""
    fits = ship.spec.armament.fits.values()
    on_the_rail = [g for fit in fits for g in fit.guns if g.place == "rail"]
    assert len(on_the_rail) == 8
    for g in on_the_rail:
        assert abs(g.height_m - rail_at(spec.profile, g.x_m)) <= 0.01, g.id


def test_each_sill_in_its_sources_band(spec):
    """Her sills as built. The source is her own draught: ZAZ6381's note, 'Height of the Port Sills
    should be 1-3 and not 1-0 1/2 as drawn', above the deck's top, which CHN0224 draws within
    0.09 ft at 1.2 in a pixel, 3.41, 3.32, 3.43 and 4.01 ft above the load line (the note §5.8).
    The guns' three, where the sheet draws no port, stand on the same line within a centimetre.
    All fall under Steel's four to five feet for sloops and cutters (1805 p. 124, OCR l.
    8268-8271; 1.22-1.52 m), the file's old 1.5 m's band: recorded for the lead before L2, on the
    load line the note takes (§4.2), and pinned here so that it is not lost."""
    p = spec.profile
    triples = {x: (sill, hb) for x, sill, hb in ports_of(p, "upper")}
    assert sorted(triples) == sorted(SHEET_PORT_X + GUN_X)
    chn0224_ft = dict(zip(SHEET_PORT_X, (3.41, 3.32, 3.43, 4.01), strict=True))
    for x, ft in chn0224_ft.items():
        assert abs(triples[x][0] - ft * FT) <= 0.03, x
    one_ft_three = 1.25 * FT
    for x in SHEET_PORT_X + GUN_X:
        assert abs(triples[x][0] - (deck_at(p, x) + one_ft_three)) <= 0.015, x
    for x in GUN_X:
        assert abs(triples[x][0] - (deck_at(p, x) + one_ft_three)) <= 0.01, x
    sills = [sill for sill, _hb in triples.values()]
    assert 1.00 <= min(sills) and max(sills) <= 1.23
    assert min(sills) < 1.22 and max(sills) < 1.52
    # The rail stands over each port by its depth, the ports being open to its underside (read)
    width, depth = dict(p.port_size_m)["upper"]
    assert (width, depth) == (0.58, 0.47)
    for x in SHEET_PORT_X:
        assert 0.0 <= rail_at(p, x) - (triples[x][0] + depth) <= 0.2, x


def test_the_port_triples_gaps_to_the_drawn_side_are_reported(spec, capsys):
    """§5.6: each triple's gap at its sill, asserted within 0.05 m for the four measured and
    reported for all seven; with the angle the lee-port rule would shut each at, for the lead
    before L2 (Build-Ships.md §5.4's reckoning, `PORT_SHUT_M` 0.3048 m)."""
    with capsys.disabled():
        print()
        for x, sill, hb in ports_of(spec.profile, "upper"):
            gap = drawn.half_breadth_at(spec, x, sill) - hb
            shut = math.degrees(math.asin((sill - 0.3048) / hb))
            whose = "the sheet's" if x in SHEET_PORT_X else "a gun's"
            print(
                f"the cutter, {whose} port at x {x:+.2f}: sill {sill:.2f} m, half-breadth "
                f"{hb:.2f} m, gap to the drawn side {gap:+.3f} m, shuts at {shut:.1f} deg"
            )
            if x in SHEET_PORT_X:
                assert abs(gap) <= drawn.PORT_GAP_M, x


def test_the_drawn_hull_is_reported_beside_the_filed_figures(spec, capsys):
    """§5.6: the drawn displacement and depth beside the filed ones, reported and never moved. A
    band in her own lines' terms: within §5.0 principle 8's 15% of the filed 106 t, and the drawn
    depth at the rabbet's height, the keel's 1 ft under it being kept and not drawn."""
    kg = drawn.drawn_displacement_kg(spec)
    lines = drawn.check(spec)
    deep = next(line for line in lines if "deep at the greatest section" in line)
    with capsys.disabled():
        print()
        print(f"the cutter: {lines[0]}.")
        print(f"the cutter: {deep}.")
    assert spec.displacement_kg == 106000.0
    assert abs(kg / spec.displacement_kg - 1.0) <= drawn.DISPLACEMENT_RECORD_SHARE
    assert 2.2 <= float(deep.split(" m deep")[0].split()[-1]) <= 2.4


# ---------------------------------------------------------------------------
# Each point against the note
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "key",
    [
        "rail_m",
        "breadth_m",
        "keel_m",
        "stem_m",
        "stern_m",
        "wales_m",
        "section_m",
        "breadth_line_m",
        "channel_wales_m",
        "floor_m",
        "rabbet_m",
    ],
)
def test_each_line_is_the_notes(doc, six, key):
    same_points(bullet(six, key), doc["hull"]["profile"][key])


def test_the_deck_ports_and_size_are_the_notes(doc, six):
    profile = doc["hull"]["profile"]
    same_points(bullet(six, "decks_m.upper"), profile["decks_m"]["upper"])
    same_points(bullet(six, "port_size_m.upper"), [profile["port_size_m"]["upper"]])
    line = next(ln for ln in six.splitlines() if ln.startswith("- **`ports_m.upper`**"))
    sheet = points_in(line[line.index("The sheet's four:") : line.index("Sill:")])
    guns = points_in(line[line.index("The guns' three:") : line.index("the same sill line")])
    assert [p[0] for p in sheet] == list(SHEET_PORT_X)
    assert [p[0] for p in guns] == list(GUN_X)
    same_points(sorted(sheet + guns), profile["ports_m"]["upper"])


def test_each_section_is_the_notes_station_by_station(doc, six):
    written = doc["hull"]["profile"]["sections_m"]
    stations = re.findall(r"^  - (\w+): (\[.*)$", six, flags=re.M)
    assert [name for name, _ in stations] == [
        "17", "16", "14", "12", "10", "8", "6", "4", "2", "O", "B", "D", "F", "H", "K", "M",
    ]  # fmt: skip
    given = [point for _name, body in stations for point in points_in(body)]
    same_points(given, written)


def note_table(head):
    """The note's table whose header begins so: its rows, each cell stripped, the first the row's
    name."""
    lines = NOTE.read_text(encoding="utf-8").splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith(head))
    rows = []
    for line in lines[start + 2 :]:
        if not line.startswith("|"):
            break
        rows.append([cell.strip() for cell in line.strip("|").split("|")])
    return rows


@pytest.fixture(scope="module")
def section_cells():
    """The note's §5.7 table of the sections: {station: {feet above the load line: half-breadth,
    moulded, feet}}."""
    return {
        row[0]: {z: float(v) for z, v in zip(range(-9, 7), row[1:], strict=True) if v}
        for row in note_table("| St | -9 | -8")
    }


def test_the_notes_section_table_is_its_list_of_points(doc, section_cells):
    """§5.7's cells and §6's `sections_m` say the same: a cell in feet, moulded, is its point in
    metres with 2 1/2 in of plank, to the centimetre, wherever §6 keeps a point at that foot."""
    by_station = {row[0]: float(row[2]) for row in note_table("| St | ft from AP | m from mid")}
    points = {}
    for x, z, hb in doc["hull"]["profile"]["sections_m"]:
        points.setdefault(x, {})[z] = hb
    checked = 0
    for name, cells in section_cells.items():
        for feet, hb_ft in cells.items():
            kept = points[by_station[name]].get(round(feet * FT, 2))
            if kept is not None:
                assert abs((hb_ft + 2.5 / 12) * FT - kept) <= 0.008, (name, feet, hb_ft, kept)
                checked += 1
    assert checked >= 190


def test_the_sections_meet_the_plans_waterlines(section_cells):
    """§5.7's check, the sheet's two views against each other: each section at the three greens
    against the half-breadth plan's, all 47 within 0.21 ft. A section read on its neighbour's line
    shows here: station 2's three cells on O's heavy line stood 0.23 ft off WL3."""
    gaps = []
    for row in note_table("| St | ft from AP | Main breadth"):
        cells = section_cells[row[0]]
        line = sorted(cells.items())
        for feet, plan in ((0.0, row[4]), (-2.47, row[5]), (-4.94, row[6])):
            if plan and feet >= line[0][0]:
                gaps.append(interp(line, feet) - float(plan))
    assert len(gaps) == 47
    assert max(abs(gap) for gap in gaps) <= 0.21
    assert abs(sum(gaps) / len(gaps)) <= 0.03


def test_abaft_station_17_the_rail_is_the_plans_inner_line(doc):
    """The plan's outer line there is the main breadth, ending at the after perpendicular; its
    inner, the rail, comes in steadily from station 17 to the taffrail's side (the note §5.7): so
    the rail narrows going aft, inside the main breadth and outside the transom's top."""
    profile = doc["hull"]["profile"]
    aft = [hb for x, _water, hb in profile["breadth_m"] if x <= -7.79]
    assert len(aft) == 4 and aft == sorted(aft) and len(set(aft)) == 4
    main_at_17 = next(hb for x, _z, hb in profile["breadth_line_m"] if x == -7.79)
    assert aft[-1] < main_at_17
    assert aft[0] > profile["form"]["stern"]["transom_hb_m"][0]


def test_the_module_gives_the_files_lines_and_the_guns_figures(module, doc):
    """`add_to` wrote them; `gun_sill` and `rail` are what the armament read them through."""
    profile = doc["hull"]["profile"]
    same_points(module.RAIL_M, profile["rail_m"])
    same_points(module.PORTS_M, profile["ports_m"]["upper"])
    for x in GUN_X:
        assert module.gun_sill(x) == pytest.approx(next(t[1] for t in module.PORTS_M if t[0] == x))
    with pytest.raises(ValueError, match="no port triple"):
        module.gun_sill(1.0)  # a place read between two ports is refused, never made up
    assert module.rail(-8.28) == 1.74


def test_her_notes_carry_no_figure_a_rule_computes(doc):
    """The lead's ruling (hull_form's docstring): the drawn figures go to the report, not the file,
    and every source and departure stands in the notes."""
    text = CUTTER.read_text(encoding="utf-8")
    assert "drawn displacement" not in text
    assert "off the half-breadth by" not in text
    for computed in ("54 ft 1 1/2 in", "56 ft 1 in", "8 ft 9 in", "2 ft 2 in above"):
        assert computed not in text, computed  # the rails', keel's and deck's, the note's §7's
    assert not re.search(r"\d+ tons of 35", text)  # her sections' displacement is the note's §4.2
    assert not re.search(r"\b\d+ t (?:against|by)\b", text)
    for word in ("ZAZ6381", "CHN0224", "CHN0103", "recorded, not moved"):
        assert word in text, word
    assert "the Greenwich draught not reached" not in doc["ship"]["era_notes"]


# ---------------------------------------------------------------------------
# Nothing the physics or the gunnery reads moved (§5.0 principle 8, §5.6)
# ---------------------------------------------------------------------------

# Pinned as figures too, so that the check stands where the base commit cannot be read.
HULL_AS_FILED = {
    "length_waterline_m": 15.2,
    "beam_m": 5.8,
    "draught_m": 2.6,
    "displacement_kg": 106000.0,
    "gm_m": 1.1,
    "clr_x_m": -0.4,
    "lateral_area_m2": 34,
    "hull_speed_kn": 9.5,
    "deck_height_m": 0.9,
    "rudder": {"area_m2": 1.2, "max_angle_deg": 35, "rate_deg_s": 5.0, "span_m": 2.7},
}
# What a gun gains by this step: the height the lee port will read (none reads it yet: the module
# freesail/combat/ports.py's stage 0) and the deck word.
GUN_DRAWN_KEYS = {"height_m", "deck"}


def test_the_hull_figures_stand_as_filed(doc):
    hull = {key: value for key, value in doc["hull"].items() if key != "profile"}
    assert hull == HULL_AS_FILED
    masts = {s["id"]: s for s in doc["spars"]}
    assert masts["main.mast"]["x_m"] == 1.5 and masts["main.mast"]["rake_deg"] == 5.2


def test_a_diff_of_her_physics_keys_against_git_shows_none(doc):
    done = subprocess.run(
        ["git", "show", f"{BASE}:data/ships/cutter.yaml"],
        cwd=ROOT,
        capture_output=True,
    )
    if done.returncode != 0:
        pytest.skip(f"the base commit {BASE} cannot be read here")
    filed = yaml.safe_load(done.stdout.decode("utf-8"))
    assert {key: v for key, v in doc["hull"].items() if key != "profile"} == filed["hull"]
    assert list(doc["hull"])[:-1] == list(filed["hull"])  # the existing keys keep their order
    assert list(doc) == list(filed)
    # of the ship's own keys her source note alone is reworded
    assert list(doc["ship"]) == list(filed["ship"])
    assert {key: v for key, v in doc["ship"].items() if key != "era_notes"} == {
        key: v for key, v in filed["ship"].items() if key != "era_notes"
    }
    for section in filed:
        if section in ("ship", "hull", "armament"):
            continue
        assert doc[section] == filed[section], section
    assert doc["armament"]["default"] == filed["armament"]["default"]
    assert list(doc["armament"]["fits"]) == list(filed["armament"]["fits"])

    def without_drawn(gun):
        return {key: value for key, value in gun.items() if key not in GUN_DRAWN_KEYS}

    for name, fit in filed["armament"]["fits"].items():
        mine = doc["armament"]["fits"][name]
        assert list(mine) == list(fit), name
        for key in fit:
            if key == "guns":
                assert [without_drawn(g) for g in mine["guns"]] == [
                    without_drawn(g) for g in fit["guns"]
                ], name
            else:
                assert mine[key] == fit[key], (name, key)
