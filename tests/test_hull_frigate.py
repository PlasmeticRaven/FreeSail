"""Package 75, SW-2 with SW-2b.2: the frigate-36's hull as drawn (docs/design/Build-Ships.md §5.0 to
§5.3, §5.6, §5.7, §5.9), from the *Amazon* class's own lines, ZAZ2587 and ZAZ2559, through
`tools/ships/hull_frigate.py`; every figure is docs/design/ships-design/pages-zaz2587.md's (the
note, below), and `§` without a document's name is that note's.

- her profile and form load, and the viewer is served her stations;
- a mark on every line of her shape, each its weakest point's word (§5.0 principle 4);
- each port gun stands on a triple of its deck within 0.01 m, each sill in its source's band;
- each point of her file is the note's §8, and §8 is the note's own tables in metres;
- the side as drawn lies on the body plan's topside lines (§6.3);
- her drawn displacement and depth stand beside the filed ones, and each triple's gap to the drawn
  side is reported (run with `-s` to read them): recorded, never moved (§5.0 principle 8);
- nothing the physics or the gunnery reads moved: a diff of her file's keys against git shows her
  profile added and each gun's `deck` and `height_m`, the height read by nothing in the engine
  (Build-Ships.md §5.3), and no other key;
- her notes carry sources, departures and judgements, and no figure a rule computes from her keys
  (the lead's notes of 2026-10-29, item 2); those are the generator's report, with Steel's 36 old
  beside new.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from freesail.api.queries import ship_graph
from freesail.combat.ports import PORT_PLACES
from freesail.ship import form
from freesail.ship.loader import load_ship
from freesail.ship.profile import half_breadth_at_sill, interp, rail_at, sill_at

ROOT = Path(__file__).resolve().parents[1]
FRIGATE = "data/ships/frigate-36.yaml"
NOTE = ROOT / "docs" / "design" / "ships-design" / "pages-zaz2587.md"
# The commit the hull step's streams work from: her file before her lines.
BEFORE = "f5be9110"  # the trunk at the landing: bb60222 but for the boats' `file` keys
FT = 0.3048
PLANK_FT = 4.0 / 12.0
# The file's figures are to the centimetre, the note's feet to the hundredth (§8).
TO_THE_CM = 0.0051
# From a table of feet to a point in metres: the feet's own hundredth and the point's centimetre,
# and a little for a point the note takes from a fit through the table's column (§8.1, its decks).
FEET_TO_METRES = 0.012


@pytest.fixture(scope="module")
def ship():
    return load_ship(ROOT / FRIGATE)


@pytest.fixture(scope="module")
def spec(ship):
    return ship.spec.hull


@pytest.fixture(scope="module")
def profile(spec):
    return spec.profile


@pytest.fixture(scope="module")
def written():
    """Her `hull.profile` as the file writes it."""
    return yaml.safe_load((ROOT / FRIGATE).read_text(encoding="utf-8"))["hull"]["profile"]


@pytest.fixture(scope="module")
def note():
    return NOTE.read_text(encoding="utf-8")


def between(text, start, end):
    """The text from `start` to the next `end`."""
    a = text.index(start)
    return text[a : text.index(end, a + len(start))]


def points(text):
    """Every bracket of numbers in the text; a heading's own brackets hold words, and pass by."""
    found = re.findall(r"\[(-?[\d.]+(?:,\s*-?[\d.]+)+)\]", text)
    return [[float(v) for v in each.split(",")] for each in found]


def same_points(given, expected, words):
    assert len(given) == len(expected), words
    for g, e in zip(given, expected, strict=True):
        assert g == pytest.approx(e, abs=TO_THE_CM), (words, g, e)


def table_of(text, heading):
    """The note's table under `heading`, as rows of cells with the header's cells as keys."""
    block = text[text.index(heading) :]
    lines = []
    for line in block.splitlines()[1:]:
        if line.startswith("|"):
            lines.append(line)
        elif lines:
            break
    cells = [[c.strip() for c in line.strip("|").split("|")] for line in lines]
    return [dict(zip(cells[0], row, strict=True)) for row in cells[2:]]


def first_number(cell):
    """A cell's figure, whatever words stand after it; None where it is empty."""
    found = re.match(r"[-+]?[\d.]+", cell)
    return float(found.group(0)) if found else None


# ---------------------------------------------------------------------------
# She loads, and is served
# ---------------------------------------------------------------------------


def test_her_profile_and_form_load_and_the_viewer_is_served_her_stations(ship, spec, written):
    """The schema takes her and `form.check` passes her; the profile is the hull's last key; the
    graph serves it with the drawn stations."""
    assert form.check(spec)
    doc = yaml.safe_load((ROOT / FRIGATE).read_text(encoding="utf-8"))
    assert list(doc["hull"])[-1] == "profile"
    hull = ship_graph(ship)["hull"]
    assert hull["stations"] and hull["profile"]["form"]["head"] == "figure"
    assert written["form"]["stern"]["type"] == "square"
    # the first and the last stations close to the post and the stem; she is no shared lens
    drawn = form.stations(spec)
    assert len(drawn) > 28 and len(hull["stations"]) == len(drawn)


# ---------------------------------------------------------------------------
# Every line of her shape carries its rung (§5.0 principle 4; §8.5)
# ---------------------------------------------------------------------------

MARKS = {
    "sourced": (
        "stem_m", "stern_m", "section_m", "head_m", "breadth_line_m", "form.stern",
        "form.stern.knuckle_z_m", "form.stern.transom_hb_m", "form.stern.round_up_m",
        "form.stern.galleries_m",
    ),
    "judged": (
        # rail_m: the inboard sheets' heavy line in the waist taken for the rail; breadth_m: the
        # water from station 20 to H taken 0.05 ft inside the main breadth, and the top of the side
        # the top-timber line; keel_m: that the strip's top border is the false keel's lower edge;
        # wales_m: the upper edge at the ends and at 6 and 4; decks_m: the deck at side, the second
        # line and the plank; ports_m: the half-breadths, the file's x, the forecastle's sills;
        # port_size_m: the forecastle's; sections_m: the sill's point at each station; floor_m and
        # rabbet_m: what the line is, and the rabbet's half-sidings held along each; the stern's
        # lights: no elevation; the figure: the knee is drawn blank
        "rail_m", "breadth_m", "keel_m", "wales_m", "decks_m", "ports_m", "port_size_m",
        "sections_m", "floor_m", "rabbet_m", "form.stern.lights_m", "form.head",
    ),
}  # fmt: skip


def test_every_line_of_her_shape_carries_its_rung(written):
    """A mark on every line her profile gives and every key of her form but the stern's type, in
    the profile's order, none of them `stand-in` or `rule`: she is on her own lines."""
    lines = [key for key in written if key not in ("form", "marks")]
    stern = [f"form.stern.{key}" for key in written["form"]["stern"] if key != "type"]
    given = [*lines, "form.stern", *stern, "form.head"]
    marks = written["marks"]
    assert list(marks) == given
    assert marks == {key: word for word, keys in MARKS.items() for key in keys}


def test_no_channel_wale_is_drawn_and_none_is_written(written):
    """§5.7: no sheet draws one, so the key is left out by principle 9."""
    assert "channel_wales_m" not in written


# ---------------------------------------------------------------------------
# Her guns stand on her ports (§5.3, §5.6; truth 7-185)
# ---------------------------------------------------------------------------


def test_each_port_gun_stands_on_a_triple_of_its_deck(ship, profile):
    """Every gun of the one fit is a port gun, with a deck; each stands on a triple of that deck
    within 0.01 m of its x and its sill."""
    guns = ship.spec.armament.fit().guns
    assert guns and all(g.place in PORT_PLACES and g.deck for g in guns)
    triples = dict(profile.ports_m)
    for g in guns:
        on = [t for t in triples[g.deck] if abs(t[0] - g.x_m) <= 0.01]
        assert len(on) == 1, g.id
        assert abs(on[0][1] - g.height_m) <= 0.01, g.id
    # and every triple has its pair of guns, so no port stands empty
    for word, line in profile.ports_m:
        for x, _sill, _hb in line:
            assert sum(1 for g in guns if g.deck == word and abs(g.x_m - x) <= 0.01) == 2, (word, x)


def test_each_sill_stands_in_its_sources_band(ship, profile):
    """Each sill in its source's band, as `tests/test_ship_particulars.py` holds a file's."""
    guns = ship.spec.armament.fit().guns
    decks = dict(profile.decks_m)
    upper = [g for g in guns if g.deck == "upper"]
    assert len(upper) == 26
    for g in upper:
        # §7.1, measured on six sheets: the thirteen ports' sills 7 ft 2 in to 8 ft 6 in above WL1,
        # ZAZ2589, ZAZ2561, ZAZ2588, ZAZ2560, ZAZ2587 (±0.05 ft, and ±0.15 ft for WL1). The file's
        # guns stand within the sheet's first and last ports.
        assert 2.19 <= g.height_m <= 2.59, g.id
        # §5.3: the same sills 2.08 to 2.13 ft above the deck at side; Steel's 36 has 2 ft 2 in
        # (pages-steel-1805-bodies.md §5.3)
        above = (g.height_m - interp(decks["upper"], g.x_m)) / FT
        assert above == pytest.approx(2.1, abs=0.1), g.id
    amidships = [g.height_m for g in upper if abs(g.x_m) < 6.0]
    # §7.1: 7 ft 2 in to 7 ft 4 in amidships, 2.19-2.25 m between the sheet's ports 5 and 9; Steel's
    # 36's 2.34 m, Folio I (read: Build-Ships.md §5.4), and the file's old 2.4 m stand above it, old
    # beside new (§9)
    assert min(amidships) == 2.19 and max(amidships) <= 2.25
    for g in guns:
        if g.deck == "quarterdeck":
            # §7.2, measured on six sheets: a carronade port's sill 0.94-0.96 ft above the deck at
            # side (Steel's 11 in), a gun port's 1.53-1.58 ft (Steel's 1 ft 7 in). The sills at the
            # file's own x, 3.97 to 4.28 m (§9.1); no sheet port stands at these x.
            want = 0.95 if g.kind == "carronade" else 1.55
            above = (g.height_m - interp(decks["quarterdeck"], g.x_m)) / FT
            assert above == pytest.approx(want, abs=0.05), g.id
            assert 3.97 <= g.height_m <= 4.28, g.id
        if g.deck == "forecastle":
            # §7.3: no sheet draws a port here; the sill 2 in under the rail, the 64's rule (judged)
            under = (rail_at(profile, g.x_m) - g.height_m) / FT
            assert under == pytest.approx(2.0 / 12.0, abs=0.05), g.id
    # the lee port's reading (Build-Ships.md §7.1) finds her side at each gun's own x
    for g in guns:
        assert sill_at(profile, g.deck, g.x_m) == pytest.approx(g.height_m, abs=0.01)
        assert 4.5 <= half_breadth_at_sill(profile, g.deck, g.x_m) <= 5.6, g.id


# ---------------------------------------------------------------------------
# Each point against the note
# ---------------------------------------------------------------------------

# Each line of the note's §8 and where its points stop.
LINES = (
    ("rail_m", "- **`rail_m`**", "- **`breadth_m`**"),
    ("breadth_m", "- **`breadth_m`**", "- **`keel_m`**"),
    ("keel_m", "- **`keel_m`**", "- **`stem_m`**"),
    ("stem_m", "- **`stem_m`**", "- **`stern_m`**"),
    ("stern_m", "- **`stern_m`**", "- **`wales_m`**"),
    ("wales_m", "- **`wales_m`**", "- **`section_m`**"),
    ("section_m", "- **`section_m`**", "- **`decks_m`**"),
    ("head_m", "- **`head_m`**", "- **`breadth_line_m`**"),
    ("breadth_line_m", "- **`breadth_line_m`**", "- **`sections_m`**"),
    ("floor_m", "- **`floor_m`**", "- **`rabbet_m`**"),
    ("rabbet_m", "- **`rabbet_m`**", "**Checked against"),
)
BY_DECK = (
    ("decks_m", "upper", "  - `upper`, from", "  - `quarterdeck`, from"),
    ("decks_m", "quarterdeck", "  - `quarterdeck`, from", "  - `forecastle`:"),
    ("decks_m", "forecastle", "  - `forecastle`:", "  - `lower` ("),
    ("decks_m", "lower", "  - `lower` (", "### 8.2"),
    ("ports_m", "upper", "- `upper`:\n  [-16.5", "- `quarterdeck`: the file's pairs"),
    ("ports_m", "quarterdeck", "- `quarterdeck`: the file's pairs", "- `forecastle`: the file's"),
    ("ports_m", "forecastle", "- `forecastle`: the file's", "- **`port_size_m`:**"),
)


def test_each_point_of_her_file_is_the_notes(written, note):
    """Her file's lines, deck by deck and station by station, against §8's own figures."""
    s8 = between(note, "## 8. For the profile", "## 9. Against the file")
    for key, start, end in LINES:
        same_points(written[key], points(between(s8, start, end)), key)
    for key, word, start, end in BY_DECK:
        same_points(written[key][word], points(between(s8, start, end)), (key, word))
    stations = between(s8, "- **`sections_m`**", "- **`channel_wales_m`:**")
    flat = [
        [float(x), *point]
        for x, body in re.findall(r"- x ([-+][\d.]+): (.*)", stations)
        for point in points(body)
    ]
    same_points(written["sections_m"], flat, "sections_m")
    assert written["port_size_m"] == {
        "upper": [0.88, 0.75],
        "quarterdeck": [0.69, 0.71],
        "forecastle": [0.69, 0.71],
    }


def test_her_form_and_marks_are_the_notes(written, note):
    """§8.5's yaml block, as the file writes it."""
    block = between(note, "### 8.5", "- **Steel's method")
    said = yaml.safe_load(between(block, "```yaml\n", "```").removeprefix("```yaml\n"))
    assert said["form"] == written["form"]
    assert said["marks"] == written["marks"]


def test_the_notes_points_are_its_own_tables_in_metres(written, note):
    """§8 against the tables it is made from, so that a slip in either shows: the rail and the
    decks by station (§5.2), the wale (§5.7), the half-breadths by station (§6.1), the waterlines
    3.32 ft apart (§4.1), and the sheet's sills with WL1's fall taken out (§7.1)."""
    sections = {}
    for x, z, hb in written["sections_m"]:
        sections.setdefault(x, []).append((z, hb))
    by_station = table_of(note, "### 5.2 By station")
    assert len(by_station) == 28
    for row in by_station:
        x = first_number(row["m from x = 0"])
        rail = first_number(row["Rail"])
        assert interp(written["rail_m"], x) == pytest.approx(rail * FT, abs=FEET_TO_METRES), x
        upper = first_number(row["Upper, second line"])
        at = interp(written["decks_m"]["upper"], x)
        # a fit through the column, rms 0.04 ft, its largest off at station 10's 0.18 ft (§8.1)
        assert at == pytest.approx((upper + 0.25) * FT, abs=0.06), x
    wale_rows = table_of(note, "### 5.7 The wales")
    assert len(wale_rows) == 28
    for row in wale_rows:
        at_x = (first_number(row["ft from AP"]) - 71.9) * FT
        lower = first_number(row["Wale, lower edge"])
        z = interp([w[:2] for w in written["wales_m"]], at_x)
        assert z == pytest.approx(lower * FT, abs=FEET_TO_METRES), at_x
    waterlines = 0
    for row in table_of(note, "### 6.1 The half-breadths by station"):
        at_x = (first_number(row["ft from AP"]) - 71.9) * FT
        station = [x for x in sections if abs(x - at_x) < 0.02]
        if not station:  # station 32 and S+2 keep fewer lines, each still in the plan
            continue
        got = dict(sections[station[0]])
        for i, word in enumerate(("Water (WL1)", "WL2", "WL3", "WL4", "WL5")):
            hb = first_number(row[word])
            z = round(-i * 3.32 * FT, 2)
            if hb is None or z not in got:
                continue
            waterlines += 1
            # §6.1 is moulded and §8 has the 4 in of plank on
            assert got[z] == pytest.approx((hb + PLANK_FT) * FT, abs=FEET_TO_METRES), (at_x, word)
    assert waterlines > 120
    sills = table_of(note, "### 7.1 The upper deck")
    assert len(sills) == 13
    for row in sills:
        k = first_number(row["Sill above K (ft)"])
        ft = first_number(row["ft from AP"])
        wl1 = 19.23 - 1.46 * ft / 143.0
        assert first_number(row["Sill above WL1 (ft)"]) == pytest.approx(k - wl1, abs=0.011), ft


# §6.3's lines by name, to the station's place in §6.1. Not its line marked About AP: that is the
# stern's edge, its x going aft with the counters, and no section (§6.3).
TOPSIDE_LINES = ("18", "22", "24", "26", "28", "30", "32", "O", "Q", "S", "S+1", "S+2")
# The row at 19.4 ft lies in the heavy level line across the body plan and is not taken (§6.3).
LOWEST_ROW_TAKEN_FT = 20.0
# §6.3's ±0.1 ft and §3.5's ±0.3-0.4 ft at the ends, in metres, and the centimetre: the side is
# straight between the file's points, so a row between two of them may lie a little off.
ON_THE_LINE_M = 0.10


def test_the_drawn_side_lies_on_the_body_plans_topside_lines(spec, profile, note):
    """§6.3's lines, read on both draughts and again by a second route, against the side as drawn at
    each station and row under the rail. Under the breadth the rows are her own section points, and
    a chord from the water would miss station 32's line by 1.27 m, which this holds shut; from the
    breadth up they stand apart from her points but for the sill's, interpolated from them."""
    places = {
        row["Station"]: first_number(row["ft from AP"])
        for row in table_of(note, "### 6.1 The half-breadths by station")
    }
    readings = 0
    for row in table_of(note, "### 6.3 The topsides"):
        if row["Line"] not in TOPSIDE_LINES:
            assert row["Line"] == "About AP"
            continue
        ft = places[row["Line"]]
        x = (ft - 71.9) * FT
        wl1 = 19.23 - 1.46 * ft / 143.0
        for head, cell in row.items():
            height = first_number(head)
            moulded = first_number(cell)
            if height is None or moulded is None or height < LOWEST_ROW_TAKEN_FT:
                continue
            z = (height - wl1) * FT
            if z > rail_at(profile, x):  # the timberheads above the forecastle's rail (§5.5)
                continue
            readings += 1
            line = (moulded + PLANK_FT) * FT
            on = form.half_breadth_at(spec, x, z)
            assert on == pytest.approx(line, abs=ON_THE_LINE_M), (row["Line"], z)
    assert readings > 140


def test_the_transoms_edge_is_reported_beside_the_stern_board(spec, profile, note):
    """§8.5: `transom_hb_m` holds two half-breadths and she is drawn straight between them, so her
    transom's edge stands outside the stern board's at the counters (§5.6), by no more than a
    quarter of a metre; at the wing transom's ends it is the board's own."""
    aft = form.stations(spec)[0]

    def edge(z):
        return interp([(p[1], p[2]) for p in aft if p[2] > 0.0], z)

    wing = 12.65
    assert edge(profile.form.stern.knuckle_z_m) == pytest.approx((wing + PLANK_FT) * FT, abs=0.01)
    print()
    for word, above_ft, moulded in (
        ("at the lower counter", 8.53, 11.3),
        ("at the upper counter", 10.57, 10.85),
        ("under the taffrail", 14.27, 10.4),
    ):
        board = (moulded + PLANK_FT) * FT
        off = edge(above_ft * FT) - board
        print(f"the frigate-36's transom's edge, {word}: {off:+.2f} m off the stern board")
        assert 0.0 < off < 0.25, word
    assert "The transom's edge:" in note


def test_the_stern_lights_stand_on_the_stern_above_the_upper_counter(profile):
    """§8.5, judged: Steel's stern is ended below by the counters, with the great cabin's windows
    between them and the taffrail (OCR :15378-15382), so the band's foot is not under the upper
    counter at the middle line, 10.57 ft above WL1 (§5.6), and it stands within the transom."""
    stern = profile.form.stern
    assert len(stern.lights_m) == 1
    low, high, count, half_breadth = stern.lights_m[0]
    assert low == pytest.approx(10.57 * FT, abs=TO_THE_CM) and high > low and count == 5
    assert half_breadth < stern.transom_hb_m[0]  # inside the stern at its narrowest


def test_the_sheets_own_ports_are_kept_for_package_81(note, probe):
    """`SHEET_PORTS` is §8.2's: the sheet's thirteen and six a side, for 81, written nowhere in her
    file (§5.0 principle 11)."""
    s82 = between(note, "### 8.2", "### 8.3")
    sheet = probe["sheet"]
    same_points(sheet["upper"], points(between(s82, "- `upper`:", "- `quarterdeck`:")), "upper")
    same_points(sheet["quarterdeck"], points(s82[s82.index("- `quarterdeck`:") :]), "quarterdeck")
    assert len(sheet["upper"]) == 13 and len(sheet["quarterdeck"]) == 6


# ---------------------------------------------------------------------------
# Recorded beside the file, never moved (§5.0 principle 8)
# ---------------------------------------------------------------------------


def test_her_drawn_displacement_and_depth_are_reported_beside_the_filed(spec):
    """1,448 t against the filed 1,270 t and 5.05 m against the file's draught of 4.6 m, on the
    sheet's lines at the sheet's length (§8.4): within §5.0's 15%, and held so that a later change
    of her sections that tips it over is seen."""
    drawn_t = form.drawn_displacement_kg(spec) / 1000.0
    filed_t = spec.displacement_kg / 1000.0
    lines = form.check(spec)
    depth = next(line for line in lines if "deep at the greatest section" in line)
    print(f"\nthe frigate-36: {next(line for line in lines if 'drawn displacement' in line)}")
    print(f"the frigate-36: {depth}")
    assert filed_t == 1270.0 and spec.draught_m == 4.6
    assert drawn_t == pytest.approx(1448.0, abs=5.0)
    assert drawn_t / filed_t - 1.0 <= form.DISPLACEMENT_RECORD_SHARE
    assert "drawn 5.05 m deep" in depth


def test_each_port_triples_gap_to_the_drawn_side_is_reported(spec, profile):
    """Each triple's gap at its sill, within §5.6's 0.05 m (at most 0.02 m, measured). Plainly, no
    independent measure of the side: her sections carry the same sill points (§8.4)."""
    print()
    worst = 0.0
    for word, triples in profile.ports_m:
        gaps = [form.half_breadth_at(spec, x, sill) - hb for x, sill, hb in triples]
        print(f"the frigate-36, {word} ports' gaps, aft to forward:", [round(g, 3) for g in gaps])
        worst = max(worst, *(abs(g) for g in gaps))
    assert worst <= form.PORT_GAP_M
    assert worst <= 0.025


def test_the_sheets_figures_stand_beside_the_files_and_are_not_moved(spec, profile):
    """What the sheets give against what the file files (§9.1), so that neither is taken for the
    other: the water line 143.5 ft rabbet to rabbet against 137 ft, K 18 ft 6 in under it at the
    middle against 15 ft."""
    assert profile.breadth_m[-1][0] - profile.breadth_m[0][0] == pytest.approx(143.5 * FT, abs=0.02)
    assert spec.length_waterline_m == 41.8
    assert -interp(profile.keel_m, 0.0) == pytest.approx(18.5 * FT, abs=0.02)
    assert spec.draught_m == 4.6


# The hull's figures as filed before her lines, and which keys of her file may differ from it.
FILED = {
    "length_waterline_m": 41.8,
    "beam_m": 11.7,
    "draught_m": 4.6,
    "displacement_kg": 1270000.0,
    "gm_m": 1.3,
    "clr_x_m": 3.0,
    "lateral_area_m2": 160.0,
    "hull_speed_kn": 13.0,
    "deck_height_m": 1.8,
}


def without_the_drawing(doc):
    """Her document with what her lines may touch taken out: the profile, and each gun's `deck`
    and `height_m`. Each height is read by nothing in the engine (Build-Ships.md §5.3), so every
    key the physics, the gunnery or the crew reads remains, calibres and numbers and places."""
    doc["hull"].pop("profile", None)
    for fit in doc["armament"]["fits"].values():
        for gun in fit["guns"]:
            gun.pop("deck", None)
            gun.pop("height_m")
    return doc


def test_no_figure_the_physics_or_the_gunnery_reads_moved(spec):
    """Her file against git at the commit before her lines: the whole document but the profile and
    each gun's `deck` and `height_m`, every other key equal. The hull's figures are held here too,
    so that this bites on a checkout without that commit."""
    for key, value in FILED.items():
        assert getattr(spec, key) == value, key
    assert spec.rudder.area_m2 == 6.0 and spec.rudder.span_m == 4.6
    done = subprocess.run(
        ["git", "show", f"{BEFORE}:{FRIGATE}"], cwd=ROOT, capture_output=True, check=False
    )
    if done.returncode != 0:
        pytest.skip(f"git has no {BEFORE} here")
    old = yaml.safe_load(done.stdout.decode("utf-8"))
    new = yaml.safe_load((ROOT / FRIGATE).read_text(encoding="utf-8"))
    assert "profile" not in old["hull"]
    guns = [g for fit in old["armament"]["fits"].values() for g in fit["guns"]]
    assert {g["height_m"] for g in guns} == {2.4, 4.5} and all("deck" not in g for g in guns)
    assert without_the_drawing(new) == without_the_drawing(old)


def test_no_gun_moved_in_calibre_number_or_place(ship):
    """The fit as filed: thirteen pairs of long 18s from +16.5 to -16.5, the quarterdeck's INCORRECT
    four pairs of carronades and its pair of long 9s kept by the owner's ruling (Build-Ships.md
    §11), the forecastle's carronades and chasers."""
    guns = {g.id: g for g in ship.spec.armament.fit().guns}
    assert len(guns) == 40
    for i, x in enumerate(
        (16.5, 13.8, 11.0, 8.2, 5.5, 2.8, 0.0, -2.8, -5.5, -8.2, -11.0, -13.8, -16.5), start=1
    ):
        g = guns[f"gun.{i}.starboard"]
        assert (g.kind, g.pounder, g.x_m, g.deck) == ("long", 18, x, "upper"), i
    for number, x in ((14, -7.0), (15, -10.5), (16, -14.0), (17, -17.5)):
        g = guns[f"gun.{number}.larboard"]
        assert (g.kind, g.pounder, g.x_m, g.deck) == ("carronade", 32, x, "quarterdeck")
    g = guns["gun.18.starboard"]
    assert (g.kind, g.pounder, g.x_m, g.deck) == ("carronade", 32, 14.0, "forecastle")
    g = guns["gun.19.starboard"]
    assert (g.kind, g.pounder, g.x_m, g.deck) == ("long", 9, -4.5, "quarterdeck")
    g = guns["chaser.bow.starboard"]
    assert (g.kind, g.pounder, g.x_m, g.deck) == ("long", 9, 17.5, "forecastle")


# ---------------------------------------------------------------------------
# Her notes, and the generator's report
# ---------------------------------------------------------------------------

NOT_IN_HER_NOTES = (
    "The hull as drawn",
    "drawn displacement",
    "deep at the greatest section",
    "off the half-breadth by",
    "1,448",
    "+14%",
    "143.5 ft",
    "18 ft 6 in",
)


def test_her_notes_carry_sources_and_judgements_and_no_figure_a_rule_computes():
    """The lead's notes of 2026-10-29, item 2: what a rule computes from her keys is the report's.
    What the notes say, each line's source and the departures from the file, stays in them."""
    text = (ROOT / FRIGATE).read_text(encoding="utf-8")
    said = [line.strip() for line in text.splitlines() if line.strip().startswith("#")]
    for words in NOT_IN_HER_NOTES:
        assert not [line for line in said if words in line], words
    joined = "\n".join(said)
    assert "ZAZ2587 and ZAZ2559" in joined
    assert "pages-zaz2587.md" in joined
    assert "recorded, not moved" in joined
    assert "stands INCORRECT by the owner's ruling" in joined
    assert "Steel's 36, her stand-in until these were read" in joined
    # §5.0 principle 9: what no source shows is judged, and tagged on the owner's sheets
    assert "tagged on the owner's sheets" in joined


PROBE = """
import json, sys
sys.path.insert(0, "tools")
import gen_ships
sys.modules["gen_ships"] = gen_ships
from ships import hull_frigate as her
hull = {"length_waterline_m": 41.8, "beam_m": 11.7, "draught_m": 4.6, "displacement_kg": 1270000.0,
        "gm_m": 1.3, "clr_x_m": 3.0, "lateral_area_m2": 160.0, "hull_speed_kn": 13.0,
        "deck_height_m": 1.8,
        "rudder": {"area_m2": 6.0, "max_angle_deg": 35, "rate_deg_s": 3.0, "span_m": 4.6}}
notes = {}
her.add_her_lines(hull, notes)
print(json.dumps({"sheet": her.SHEET_PORTS, "report": her.REPORT, "notes": sorted(notes)}))
try:
    her.sill("upper", 1.0)
except ValueError as e:
    print(e, file=sys.stderr)
"""


@pytest.fixture(scope="module")
def probe():
    """Her module run alone, as the generator runs it, in a process of its own (one copy of the
    generator: tools/ships/__init__.py)."""
    done = subprocess.run(
        [sys.executable, "-c", PROBE],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert done.returncode == 0, done.stderr
    out = json.loads(done.stdout)
    out["stderr"] = done.stderr
    return out


def test_the_generators_report_says_what_her_notes_do_not(probe):
    """Printed to the standard error as her file is written: the drawn hull, the gaps deck by deck,
    her sheet's figures beside the file's, and Steel's 36 old beside new (§5.0 principle 12)."""
    said = probe["stderr"]
    drawn = "frigate-36: the hull as drawn (freesail/ship/form.py):"
    assert f"{drawn} drawn displacement 1448 t against the filed 1270 t (+14%)." in said
    assert f"{drawn} drawn 5.05 m deep at the greatest section" in said
    assert said.count("deck's ports: the side at each sill") == 3
    assert "her WL1 drawn 43.75 m rabbet to rabbet against the file's length_waterline_m" in said
    assert "Steel's 36 old beside new: the sill at midships 2.34 m, now 2.19 m;" in said
    assert "the taffrail's top 5.92 m, now 6.03 m" in said
    # a gun off every triple is refused, never placed between two (§5.2)
    assert "has no port triple at x 1" in said
    # a note on every line she writes
    for key in ("profile", "profile.rail_m", "profile.ports_m.upper", "profile.form.stern"):
        assert key in probe["notes"]
