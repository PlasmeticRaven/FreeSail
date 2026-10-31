"""Package 75's hull step, SW-2 with SW-2b.2: the *Diligence* class's hull, the brig's and the
merchant brig's one hull (docs/design/Build-Ships.md §5.0 principle 10, §5.3, §5.6, §5.7, §5.9;
tools/ships/hull_brig.py; docs/design/ships-design/pages-zaz4491.md, "the note" below).

Her lines are rung S, measured at full size on ZAZ4491 and ZAZ4492. Each point here is read against
the note; each port gun stands on a triple of its deck; each sill in its source's band; a mark on
every shape line. The drawn displacement and depth and the triples' gaps are reported beside the
filed figures (printed, and pinned in a band), never moved, and no figure the physics or the gunnery
reads differs from the commit before her lines came (§5.0 principle 8).

Her file's generator is not run here: `tests/test_ship_particulars.py` proves the bytes. Nothing is
written outside `tmp_path`, and a Greenwich image is never read.
"""

from __future__ import annotations

import copy
import importlib.util
import math
import re
import subprocess
from pathlib import Path

import pytest
import yaml

from freesail.api.queries import ship_graph
from freesail.combat.ports import PORT_PLACES
from freesail.ship import form
from freesail.ship.loader import load_ship
from freesail.ship.profile import deck_at, half_breadth_at_sill, interp, ports_of, rail_at, sill_at

ROOT = Path(__file__).resolve().parents[1]
BRIG = "data/ships/brig.yaml"
MERCHANT = "data/ships/merchant-brig.yaml"
NOTE = ROOT / "docs" / "design" / "ships-design" / "pages-zaz4491.md"
FT = 0.3048
# the commit before her lines came: the files as they stood, for the physics' keys
BEFORE = "bb60222"
# the note's figures are to the centimetre; a point reads as the note's within rounding
TO_THE_NOTE_M = 0.005
# the plank, the difference of the breadths moulded and extreme: the note's §5 tables are moulded
PLANK_FT = 0.25


def _raw(path: str) -> dict:
    return yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def note() -> str:
    return NOTE.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def lines(note) -> dict[str, list[list[float]]]:
    """§6.2's blocks, each line's points by its key as the note writes them."""
    block = note[note.index("### 6.2 The lines") : note.index("### 6.3 Plainly")]
    first, rest = block.split("`sections_m`, by station", 1)
    out: dict[str, list[list[float]]] = {}
    parts = re.split(r"^(\w+(?:\.\w+)?(?:, the [^:\n]*)?):", first, flags=re.M)
    for key, body in zip(parts[1::2], parts[2::2], strict=True):
        body = body.split("```")[0]
        out[key] = [[float(v) for v in p.split(",")] for p in re.findall(r"\[([^\[\]]+)\]", body)]
    sections = rest.split("```")[1]
    out["sections_m"] = [
        [float(v) for v in p.split(",")] for p in re.findall(r"\[([^\[\]]+)\]", sections)
    ]
    return out


def _table(note: str, start: str, end: str) -> dict[str, dict[str, float | None]]:
    """A table of the note's §5 by station, each row by its head's words, a blank cell None. Its
    `|---|` line does not begin `| `, so the rows follow the head straight."""
    block = note[note.index(start) : note.index(end)]
    rows = [ln for ln in block.split("\n") if ln.startswith("| ")]
    head = [c.strip() for c in rows[0].split("|")[1:-1]]
    out = {}
    for row in rows[1:]:
        cells = [c.strip() for c in row.split("|")[1:-1]]
        figures = [float(c) if c else None for c in cells[1:]]
        out[cells[0]] = dict(zip(head[1:], figures, strict=True))
    return out


def _sheer(note: str) -> dict[str, dict[str, float | None]]:
    """§5.2's table in feet, by station, its twenty-two."""
    table = _table(note, "### 5.2 By station", "### 5.3 The decks")
    assert len(table) == 22
    return table


# -- her profile and form load, and the viewer is served them ---------------------------------


@pytest.mark.parametrize("path", [BRIG, MERCHANT])
def test_her_profile_and_form_load_and_are_served(path):
    ship = load_ship(path)
    spec = ship.spec.hull
    p = spec.profile
    assert [word for word, _pts in p.decks_m] == ["upper"]  # flush: read on both sheets
    assert [word for word, _triples in p.ports_m] == ["upper"]
    assert len(ports_of(p, "upper")) == 10  # ten a side, read on both sheets and both sisters
    assert p.form.stern.type == "square" and p.form.head == "scroll"
    assert p.form.fullness is None  # the ends are drawn through her waterlines
    assert p.floor_m == ()  # no rising line is drawn on the sheet: no source
    # no galleries and no lights: the sheet's two stern ports are ports, package 81's
    assert p.form.stern.galleries_m == () and p.form.stern.lights_m == ()
    # the drawn hull stands, with the bowsprit's stem head and the taffrail where the sheet has them
    assert form.check(spec)
    assert p.stem_m[-1] == (15.10, 3.44) and p.stern_m[-1] == (-16.47, 3.68) == p.rail_m[0]
    graph = ship_graph(ship)["hull"]
    assert graph["profile"]["form"]["head"] == "scroll" and graph["stations"]


def test_one_hull_in_two_roles_alike_but_her_own_two_guns_ports():
    """§5.0 principle 10: the same hull's figures and profile in the two files, but the two ports
    the merchant brig's guns stand in, at her guns' x (the existing code decides her details)."""
    brig, merchant = _raw(BRIG)["hull"], _raw(MERCHANT)["hull"]
    a = brig["profile"]["ports_m"]["upper"]
    b = merchant["profile"]["ports_m"]["upper"]
    differ = [(p, q) for p, q in zip(a, b, strict=True) if p != q]
    assert differ == [
        ([-3.9, 1.6, 4.13], [-4.0, 1.6, 4.12]),
        ([3.9, 1.62, 4.21], [4.0, 1.62, 4.21]),
    ]
    brig["profile"]["ports_m"] = merchant["profile"]["ports_m"] = None
    assert brig == merchant


def test_the_two_files_draw_alike():
    """§5.0 principle 10, the pair §5.6's check holds as one class in two roles
    (`SAME_HULL_BY_INTENT`, tests/test_profiles.py): the outlines, abeam, ahead and astern, are the
    same to the point."""
    a, b = (load_ship(path).spec.hull for path in (BRIG, MERCHANT))
    for view in form.VIEWS:
        assert form.outline(a, view) == form.outline(b, view), view


# -- a mark on every shape line ---------------------------------------------------------------


@pytest.mark.parametrize("path", [BRIG, MERCHANT])
def test_a_mark_on_every_line_and_rung_s_throughout(path):
    """§5.0 principles 3 and 4: every line and form key marked, S throughout: `sourced`, or
    `judged` where the line's weakest point is reasoning on the class's own lines, each named."""
    profile = _raw(path)["hull"]["profile"]
    marks = profile["marks"]
    shape = {k for k in profile if k not in ("form", "marks")}
    groups = {f"form.{k}" for k in profile["form"]}
    stern = {f"form.stern.{k}" for k in profile["form"]["stern"] if k != "type"}
    assert set(marks) == shape | groups | stern
    assert {word for word in marks.values()} == {"sourced", "judged"}
    assert {k for k, word in marks.items() if word == "judged"} == {
        "keel_m",  # that the strip's border is K (the note's §5.4)
        "decks_m",  # which red line is the deck at side, the plank added (the note's §5.1)
        "ports_m",  # the half-breadths at the sills; a gun's port at the gun's x (§5.7, §6.3)
        "rabbet_m",  # the half-sidings between their two places
    }


# -- each port gun on a triple ----------------------------------------------------------------

# The guns' x are the file's and never move (Build-Ships.md §5.3).
GUN_X = {
    BRIG: {-9.1, -6.5, -3.9, -1.3, 1.3, 3.9, 6.5, 9.1, 12.0},
    MERCHANT: {-4.0, 4.0},
}


@pytest.mark.parametrize("path", [BRIG, MERCHANT])
def test_each_port_gun_stands_on_a_triple_of_its_deck(path):
    """Truth 7-185's clause (Build-Ships.md §5.1, §5.3, §15): every port gun's (x_m, height_m) on
    a triple of its deck within 0.01 m, its x the file's, its deck named."""
    ship = load_ship(path)
    p = ship.spec.hull.profile
    triples = ports_of(p, "upper")
    guns = [g for fit in ship.spec.armament.fits.values() for g in fit.guns]
    assert guns and {g.x_m for g in guns} == GUN_X[path]
    for g in guns:
        assert g.place in PORT_PLACES and g.deck == "upper", g.id
        assert any(
            abs(g.x_m - x) <= 0.01 and abs(g.height_m - sill) <= 0.01 for x, sill, _hb in triples
        ), g.id
        assert g.height_m == sill_at(p, "upper", g.x_m), g.id
        # the lee port reads this half-breadth, no geometry of its own (§5.1, §7.1)
        assert half_breadth_at_sill(p, "upper", g.x_m) > 2.0, g.id


# -- each sill in its source's band -----------------------------------------------------------


@pytest.mark.parametrize("path", [BRIG, MERCHANT])
def test_each_sill_in_its_sources_band(path, lines):
    """The sills' source is the sheet, rung S (§5.0 principles 3, 5 and 12), which decides over
    §5.4's rules:
    - ZAZ4491's ten sills, 5.15 to 6.53 ft above WL1, ±0.05 ft (the note's §5.7), read at a triple's
      x along them; ±0.03 m with the centimetres of both;
    - every sill 1 ft 4 in above the deck at side, 1.35 ft ±0.05 (the note's §5.7), as Steel's
      *Raven*'s 16 in (Steel 1805 p. lx, OCR l. 44380-44381), at the chase port too, written so;
    - the lowest 5 ft 2 in, 1.57 m, ±0.05 ft (ZAZ4492 gives it within 0.01 ft). Steel p. 124's four
      to five feet for "sloops, cutters, &c." (OCR l. 8268-8271), 1.22-1.52 m, the rung R of
      §5.4's first table, lies 0.05 m under it: recorded in the note's §7, and truth 7-185's band
      moved from it to the sheet's, old beside new (the lead's ruling; tests/test_profiles.py)."""
    p = load_ship(path).spec.hull.profile
    sheet = lines["ports_m.upper, the sheet's, as §5.7"]
    sills = [(x, sill) for x, sill, _hb in sheet]
    triples = ports_of(p, "upper")
    for x, sill, _hb in triples[:-1]:
        assert abs(sill - interp(sills, x)) <= 0.03, x
    for x, sill, _hb in triples:
        assert abs(sill - deck_at(p, x) - 1.35 * FT) <= 0.03, x
        assert deck_at(p, x) < sill < rail_at(p, x), x
    lowest = min(sill for _x, sill, _hb in triples)
    assert lowest == pytest.approx(5.15 * FT, abs=0.05 * FT)
    assert lowest - 1.52 == pytest.approx(0.05, abs=0.01)  # above Steel's band, by so much


def test_the_load_line_is_wl1_and_the_faint_line_is_recorded(note):
    """The lead's note of 2026-10-31, point 4: WL1, the faint ruled line recorded, in the note and
    in each file's own; §5.4's band goes to the sheet, old beside new."""
    choice = " ".join(note[note.index("### 4.2 Which") : note.index("### 4.3 The drag")].split())
    assert "Ruled (the lead, 2026-10-31): WL1, and the faint line recorded." in choice
    assert "**A faint ruled grey line lies just above" in note
    band = " ".join(note[note.index("**Truth 7-185 and §5.4's band") :].split())
    assert "old 1.22-1.52 m, Steel p. 124's four to five feet; new 5 ft 2 in ±0.05 ft" in band
    for path in (BRIG, MERCHANT):
        text = " ".join((ROOT / path).read_text(encoding="utf-8").split())
        assert "as the lead ruled" in text and "faint ruled grey line" in text, path


def test_the_triples_stand_by_the_sheets_ports(lines):
    """A port with a gun in it stands at the gun's x, by these from the sheet's centre (§6.3): the
    eight within 0.12 m, the merchant brig's two within 0.16 m, the chase port on port 10's fore
    edge, 0.43 m on. Port 1 holds no gun and stands at the sheet's."""
    sheet = [t[0] for t in lines["ports_m.upper, the sheet's, as §5.7"]]
    for path, reach in ((BRIG, 0.12), (MERCHANT, 0.16)):
        triples = _raw(path)["hull"]["profile"]["ports_m"]["upper"]
        off = [abs(t[0] - x) for t, x in zip(triples, sheet, strict=True)]
        assert off[0] == 0.0 and max(off[:-1]) <= reach + 0.001, path
        assert off[-1] == pytest.approx(0.43, abs=0.001), path


# -- each point against the note --------------------------------------------------------------

NOTE_LINES = {
    "rail_m": "rail_m",
    "breadth_m": "breadth_m",
    "keel_m": "keel_m",
    "stem_m": "stem_m",
    "stern_m": "stern_m",
    "wales_m": "wales_m",
    "section_m": "section_m",
    "head_m": "head_m",
    "breadth_line_m": "breadth_line_m",
    "rabbet_m": "rabbet_m",
    "sections_m": "sections_m",
}


@pytest.mark.parametrize("path", [BRIG, MERCHANT])
@pytest.mark.parametrize("key", list(NOTE_LINES))
def test_each_point_of_a_line_against_the_note(path, key, lines):
    written = _raw(path)["hull"]["profile"][key]
    said = lines[NOTE_LINES[key]]
    assert len(written) == len(said) > 1
    for a, b in zip(written, said, strict=True):
        assert a == pytest.approx(b, abs=TO_THE_NOTE_M), (key, a, b)


@pytest.mark.parametrize(
    "path, key",
    [
        (BRIG, "ports_m.upper, the brig's file, each port with a gun in it at the gun's x"),
        (MERCHANT, "ports_m.upper, the merchant brig's file, the same but her own two guns' ports"),
    ],
)
def test_each_port_and_the_deck_against_the_note(path, key, lines):
    profile = _raw(path)["hull"]["profile"]
    for written, said in (
        (profile["ports_m"]["upper"], lines[key]),
        (profile["decks_m"]["upper"], lines["decks_m.upper"]),
    ):
        assert [q for pt in written for q in pt] == pytest.approx(
            [q for pt in said for q in pt], abs=TO_THE_NOTE_M
        )
    assert profile["port_size_m"]["upper"] == [0.84, 0.7]


def test_the_sheets_ports_in_the_note_agree_with_its_table(note, lines):
    """§6.2's sheet triples are §5.7's table, feet to metres: the x, the sill and the half-breadth
    moulded with 3 in of plank."""
    table = note[note.index("### 5.7 The ports") : note.index("### 5.8 The channels")]
    rows = re.findall(r"^\| (\d+) \|(.*)\|$", table, flags=re.M)
    assert len(rows) == 10
    for (_n, row), (x, sill, hb) in zip(
        rows, lines["ports_m.upper, the sheet's, as §5.7"], strict=True
    ):
        c = [v.strip() for v in row.split("|")]
        assert float(c[1]) == pytest.approx(x, abs=TO_THE_NOTE_M)
        assert float(c[4].split()[1].strip("()")) == pytest.approx(sill, abs=TO_THE_NOTE_M)
        assert (float(c[7]) + 0.25) * FT == pytest.approx(hb, abs=TO_THE_NOTE_M + 0.003)


def test_the_file_against_the_notes_tables_by_station(note):
    """§5.2 in feet against the file's lines in metres at each station, within a centimetre: the
    rail, the deck at side, the wale's edges, the height of breadth."""
    p = load_ship(BRIG).spec.hull.profile
    pairs = {
        "Rail": lambda x: rail_at(p, x),
        "Deck at side": lambda x: deck_at(p, x),
        "Wale, lower edge": lambda x: interp(p.wales_m, x),
        "Wale, upper edge": lambda x: interp([(a, c) for a, _b, c in p.wales_m], x),
        "Height of breadth": lambda x: interp(p.breadth_line_m, x),
    }
    for station, row in _sheer(note).items():
        for word, at in pairs.items():
            assert at(row["m from mid"]) == pytest.approx(row[word] * FT, abs=0.01), (station, word)


def test_the_half_breadths_against_the_notes_table_by_station(note):
    """§5.10, moulded in feet, with the 3 in of plank, against the file's lines in metres at each
    station within a centimetre: WL1 and the top-timber line in `breadth_m`, the main breadth in
    `breadth_line_m`. WL2, WL3 and WL4 on the drawn side at the heights §5.2 gives them, WL4 rising
    to -7.08 ft at Q, within 2 cm, the centimetres of both."""
    spec = load_ship(BRIG).spec.hull
    p = spec.profile
    table = _table(note, "### 5.10 The half-breadths", "### 5.11 The sections")
    assert len(table) == 22
    lines = {
        "WL1": lambda x: interp(p.breadth_m, x),
        "Top-timber line": lambda x: interp([(a, c) for a, _b, c in p.breadth_m], x),
        "Main breadth": lambda x: interp([(a, c) for a, _b, c in p.breadth_line_m], x),
    }
    below = {"WL2": -2.39, "WL3": -4.75, "WL4": -7.13}
    for station, row in table.items():
        x = row["m from mid"]
        for word, at in lines.items():
            assert at(x) == pytest.approx((row[word] + PLANK_FT) * FT, abs=0.01), (station, word)
        for word, z in below.items():
            if row[word] is not None:
                z = -7.08 if (station, word) == ("Q", "WL4") else z
                said = (row[word] + PLANK_FT) * FT
                assert form.half_breadth_at(spec, x, z * FT) == pytest.approx(said, abs=0.02), word


def test_the_drawn_side_against_the_body_plan(note):
    """§5.11, each cell at its station's height above the rabbet line (§5.2), moulded in feet with
    the plank, against the drawn side, as the note's §6.1 says: above the water within 0.06 m, 0.03
    m rms; under it within 0.09 m, 0.04 m rms, the fore body's difference of the sheet's two views
    among them (the note's §5.11)."""
    spec = load_ship(BRIG).spec.hull
    sheer = _sheer(note)
    table = _table(note, "### 5.11 The sections", "## 6. For the profile")
    above, under = [], []
    for station, row in table.items():
        for level, cell in row.items():
            if cell is not None:
                z = (float(level) + sheer[station]["Rabbet line"]) * FT
                off = form.half_breadth_at(spec, sheer[station]["m from mid"], z)
                off -= (cell + PLANK_FT) * FT
                (above if z >= 0.0 else under).append(off)
    assert len(above) > 150 and len(under) > 150
    for offs, largest, rms in ((above, 0.06, 0.03), (under, 0.09, 0.04)):
        assert max(abs(off) for off in offs) <= largest
        assert math.sqrt(sum(off * off for off in offs) / len(offs)) <= rms


def test_each_section_point_stands_in_the_hull():
    """Every point of `sections_m` stands between the post's and the stem's lines at its height and
    at or above the rabbet line at its x, where the section ends: no line of the stem's siding
    read for a section's (section S ends on the stem's rabbet, the note's §5.11)."""
    p = load_ship(BRIG).spec.hull.profile
    post = [(z, x) for x, z in p.stern_m]
    stem = [(z, x) for x, z in p.stem_m]
    rabbet = [(x, z) for x, z, _half_siding in p.rabbet_m]
    for x, z, hb in p.sections_m:
        assert interp(post, z) < x < interp(stem, z), (x, z, hb)
        assert z >= interp(rabbet, x) - 0.01, (x, z, hb)


def test_no_side_is_drawn_under_the_counter():
    """Abaft the post at the water the sheet has the rudder under the counter, and the drawing
    nothing: a point of `breadth_line_m` there would stand a station down to the water, a box under
    the counter, so the line starts at section 23 (the note's §6.3). The side's foot follows the
    post and the counter, and from the post at the water to the counter's after end nothing is
    drawn under them."""
    spec = load_ship(BRIG).spec.hull
    p = spec.profile
    x_post = interp([(z, x) for x, z in p.stern_m], 0.0)
    counter = [(x, z) for x, z in reversed(p.stern_m) if 0.0 <= z <= 2.10]  # x rising, to the post
    assert x_post == pytest.approx(counter[-1][0], abs=0.02) and counter[0][0] < x_post - 1.0
    assert p.breadth_line_m[0][0] > x_post
    x = counter[0][0]
    while x < x_post:
        assert form.half_breadth_at(spec, x, interp(counter, x) - 0.05) == 0.0, x
        x += 0.1
    for station in form.stations(spec)[1:-1]:
        x = station[0][0]
        if x < x_post:
            assert station[0][1] >= interp(counter, x) - 0.01, x


def test_the_form_and_the_marks_against_the_note(note):
    block = note[note.index("`form` and `marks`:") : note.index("### 6.3 Plainly")]
    profile = _raw(BRIG)["hull"]["profile"]
    stern = profile["form"]["stern"]
    assert yaml.safe_load(block.split("```")[1].split("marks:")[0])["form"] == {
        "stern": stern,
        "head": profile["form"]["head"],
    }
    said = block.split("marks:")[1].split("```")[0]
    sourced, judged = said.split(": sourced")
    for key, word in profile["marks"].items():
        assert re.search(rf"(?<![\w.]){re.escape(key)}\b", sourced if word == "sourced" else judged)


# -- reported beside the file, never moved ----------------------------------------------------


@pytest.fixture(scope="module")
def report() -> tuple[list[str], dict]:
    """The generator's report and gaps for her hull, as `g.hull_form` gives them from the file."""
    spec = importlib.util.spec_from_file_location(
        "gen_ships_for_the_brig", ROOT / "tools" / "gen_ships.py"
    )
    gen = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gen)
    hull = copy.deepcopy(_raw(BRIG)["hull"])
    shape = {k: hull["profile"].pop(k) for k in ("form", "marks")}
    said: list[str] = []
    gaps = gen.hull_form(hull, form=shape["form"], marks=shape["marks"], report=said)
    return said, gaps


def test_the_drawn_displacement_and_depth_are_reported_beside_the_filed_ones(report):
    """§5.0 principle 8: drawn to WL1 she displaces about 303 t against the filed 413 t, -27%, and
    is drawn 2.87 m deep at the greatest section, where the drawn body stops near the rabbet line,
    against the file's 3.5 m; K stands 11.25 ft, 3.43 m, below WL1 at the middle. Recorded, never
    moved."""
    said, _gaps = report
    print("\n".join(said))
    spec = load_ship(BRIG).spec.hull
    assert spec.displacement_kg == 413000.0 and spec.draught_m == 3.5
    assert form.drawn_displacement_kg(spec) == pytest.approx(303_000.0, abs=3_000.0)
    assert any("drawn displacement 303 t against the filed 413 t (-27%)" in s for s in said)
    assert any("recorded, not moved" in s for s in said)
    assert any("drawn 2.87 m deep at the greatest section" in s for s in said)
    assert -interp(spec.profile.keel_m, 0.0) == pytest.approx(11.25 * FT, abs=0.02)


def test_her_drag_is_the_sheets_recorded_beside_the_files_and_winfields():
    """The drag read off ZAZ4491's waterlines (the note's §4.3): K against WL1 falls 3.11 ft ±0.03
    in the 95 ft, 9.69 ft forward and 12.80 ft aft at the perpendiculars. Beside it, recorded and
    not moved: the file's 10.5 and 12.5 ft, 11.5 ft mean (`gen_ships.brig`, judgement); and Winfield
    1793-1817 p. 256, *Harpy* as built, 7 ft 3 in and 10 ft 10 in, 3 ft 7 in of drag, near WL2."""
    spec = load_ship(BRIG).spec.hull
    (x0, z0), (x1, z1) = spec.profile.keel_m  # straight: carried to the perpendiculars
    half = 47.5 * FT
    aft = -(z0 + (z1 - z0) * (-half - x0) / (x1 - x0)) / FT
    fore = -(z0 + (z1 - z0) * (half - x0) / (x1 - x0)) / FT
    assert aft == pytest.approx(12.80, abs=0.05)
    assert fore == pytest.approx(9.69, abs=0.05)
    assert aft - fore == pytest.approx(3.11, abs=0.05)
    assert spec.draught_m == pytest.approx(11.5 * FT, abs=0.01)
    print(f"her drag: K below WL1 {aft:.2f} ft aft, {fore:.2f} ft forward, {aft - fore:.2f} ft")


def test_the_port_triples_gaps_to_the_drawn_side_are_reported(report):
    """§5.6: each triple's gap to the drawn side at its sill, reported for the eight files. All but
    one lie within `form.PORT_GAP_M`; the one at x 6.5, -0.05 m and a hair over it, is the fore
    body's difference of the sheet's two views (the note's §5.11), reported and never moved."""
    said, gaps = report
    print("\n".join(f"the {w} port at x {x:g}: {g:+.3f} m" for (w, x), g in gaps.items()))
    assert len(gaps) == 10
    assert all(abs(g) <= 0.06 for g in gaps.values())
    assert [x for (_w, x), g in gaps.items() if abs(g) > form.PORT_GAP_M] == [6.5]
    assert any("the upper deck's ports: the side at each sill" in s for s in said)


@pytest.mark.parametrize("path", [BRIG, MERCHANT])
def test_her_notes_carry_sources_and_no_figure_a_rule_computes(path):
    """The lead's ruling: the file's notes say sources, departures and judgements; what a rule
    computes from her keys is the generator's report and these tests'."""
    text = (ROOT / path).read_text(encoding="utf-8")
    comments = "\n".join(ln for ln in text.split("\n") if ln.lstrip().startswith("#"))
    for said in ("ZAZ4491", "ZAZ4492", "Winfield 1793-1817 p. 256", "pages-zaz4491.md", "1799"):
        assert said in comments, said
    for computed in (
        "drawn displacement",
        "off the half-breadth by",
        "deep at the greatest",
        "91 ft 10 in",
        "95 ft 2 in",
        "11 ft 3 in",
        "12 ft 10 in aft",
        "3 ft 10 in at side",
    ):
        assert computed not in comments, computed
    assert "28 ft 1 1/2 in extreme breadth, Harpy as built" in comments
    # the profile's own notes hold no difference worked from a key (a port off the sheet's centre,
    # a mast's x): the note's §6.3 and §7 hold those
    notes = text[text.index("# Her side, decks and ports") : text.index("\nspars:")]
    lines = [ln for ln in notes.split("\n") if ln.lstrip().startswith("#")]
    assert lines
    for line in lines:
        assert not re.search(r"within \d", line) and "+8.9" not in line, line
    # true of each role: the brig's one empty port is no word in the merchant brig's file
    assert ("the aftmost stands empty" in comments) == (path == BRIG)
    assert ("her own two guns' ports" in comments) == (path == MERCHANT)


# -- nothing the physics or the gunnery reads moved ---------------------------------------------


def _git_show(path: str) -> str | None:
    """The file at `BEFORE`; None where this checkout cannot give it (no git, a shallow clone, an
    archive), when `test_ship_particulars` still proves the bytes and this test says it skipped."""
    try:
        run = subprocess.run(
            ["git", "show", f"{BEFORE}:{path}"],
            cwd=ROOT,
            capture_output=True,
            timeout=60,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return run.stdout.decode("utf-8") if run.returncode == 0 else None


def _without_the_drawing(doc: dict) -> dict:
    """The file's mapping less what the drawing adds and what nothing but the lee port will read:
    the profile; a gun's `height_m` and `deck` (Build-Ships.md §5.3, §7.3: L1, no reader yet); and
    the era note's words."""
    doc = copy.deepcopy(doc)
    doc["hull"].pop("profile", None)
    doc["ship"].pop("era_notes", None)
    for fit in doc["armament"]["fits"].values():
        for gun in fit["guns"]:
            gun.pop("height_m", None)
            gun.pop("deck", None)
    return doc


@pytest.mark.parametrize("path", [BRIG, MERCHANT])
def test_no_figure_the_physics_or_the_gunnery_reads_moved(path):
    """§5.0 principle 8, §5.6: her file against git, every key but the drawing's: the hull's
    figures, the spars, the sails, the lines, the guns' calibre, place, x and crew, her stores and
    her company, all as they stood. Only the profile, each gun's height and deck and the era note's
    words differ."""
    before = _git_show(path)
    if before is None:
        pytest.skip(f"{BEFORE} is not in this checkout")
    now = yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))
    then = yaml.safe_load(before)
    assert _without_the_drawing(now) == _without_the_drawing(then)
    # and the hull's own keys are in their old order, the profile last (§5.1)
    assert list(now["hull"]) == [*then["hull"], "profile"]
    # the guns' heights and decks did move, as §5.3 has it; the x did not
    guns_then = {g["id"]: g for fit in then["armament"]["fits"].values() for g in fit["guns"]}
    for fit in now["armament"]["fits"].values():
        for g in fit["guns"]:
            assert g["x_m"] == guns_then[g["id"]]["x_m"] and g["deck"] == "upper"
            assert g["height_m"] < guns_then[g["id"]]["height_m"] == 2.1
