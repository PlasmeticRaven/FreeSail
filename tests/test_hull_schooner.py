"""Package 75, SW-2 with SW-2b.2: the schooners' one hull (docs/design/Build-Ships.md §5.0, §5.1,
§5.3, §5.4, §5.6, §5.7), built by `tools/ships/hull_schooner.py` from Lynx's draught as measured in
docs/design/ships-design/pages-chapelle-fig17.md (the note), for `data/ships/topsail-schooner.yaml`
and `data/ships/privateer-schooner.yaml`, one class in two roles (§5.0 principle 10).

Her profile and form load and draw. Every shape line carries its rung. Each point stands as the
note gives it, and the note's §6.1 goes to its §6.4 by §6.2's factors. Each port gun stands on a
triple of its deck, each sill in its source's band with the source in a comment. The drawn
displacement and depth stand beside the filed ones and the port triples' gaps to the drawn side are
reported, by the generator and here. No hull figure the physics reads moved: a diff of her file's
physics keys against git shows none. Nothing here writes a ship file.
"""

from __future__ import annotations

import math
import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from freesail.ship import form as drawn
from freesail.ship.loader import load_ship, load_spec
from freesail.ship.profile import deck_at, ports_of, rail_at

ROOT = Path(__file__).resolve().parents[1]
TOPSAIL = "data/ships/topsail-schooner.yaml"
PRIVATEER = "data/ships/privateer-schooner.yaml"
BOTH = (TOPSAIL, PRIVATEER)
NOTE = ROOT / "docs" / "design" / "ships-design" / "pages-chapelle-fig17.md"
FT = 0.3048
# The commit her files stood at before her hull: the physics keys are compared with it.
BEFORE = "bb602220"
# What the shape keys and §5.3 may add or move; everything else of her files stands as it stood.
STAND_IN = (
    "rail_m", "breadth_m", "keel_m", "stem_m", "stern_m", "section_m", "port_size_m",
    "head_m", "sections_m", "rabbet_m", "form.stern", "form.stern.knuckle_z_m",
    "form.stern.transom_hb_m", "form.stern.round_up_m", "form.head",
)  # fmt: skip
# The round up is the class's; the main breadth's height a band; five of the eight triples stand at
# the guns' places and not the plate's ports; the rail's half-breadth the plan's thin outer line;
# and every height above the water takes §6.2's two judged steps (the note, §6.2, §6.3, §6.4).
JUDGED = (
    "rail_m", "breadth_m", "stem_m", "stern_m", "section_m", "decks_m", "ports_m", "head_m",
    "breadth_line_m", "sections_m", "rabbet_m",
)  # fmt: skip


def flat(points) -> list[float]:
    """A line of points as one list of numbers, for `pytest.approx`."""
    return [v for point in points for v in point]


def note_section(number: str) -> str:
    """The note's section of that heading number, to the next heading of its level or above."""
    text = NOTE.read_text(encoding="utf-8")
    start = re.search(rf"^### {re.escape(number)} .*$", text, flags=re.M)
    assert start, number
    end = re.compile(r"^##+ ", flags=re.M).search(text, start.end())
    return text[start.end() : end.start() if end else len(text)]


def numbers(text: str) -> list[float]:
    """The figures in a piece of the note, its minus signs as it prints them."""
    return [float(v.replace("−", "-")) for v in re.findall(r"[−-]?\d+\.\d+", text)]


def note_list(section: str, key: str) -> list[list[float]]:
    """A bullet's list of points, **`key`** ...: [..], [..]., as the note prints it."""
    head = re.search(rf"^- \*\*`{re.escape(key)}`[^*]*\*\*[\s\S]*?:\s+(?=\[)", section, flags=re.M)
    assert head, key
    tail = re.compile(r"^- \*\*|\Z", flags=re.M).search(section, head.end())
    body = section[head.end() : tail.start()]
    # the list ends at its full stop: a sentence or a further list may follow it
    body = body[: re.search(r"\]\.(\s|$)|\Z", body).start() + 1]
    return [numbers(p) for p in re.findall(r"\[([^\[\]]+)\]", body)]


@pytest.fixture(scope="module")
def spec():
    return load_spec(TOPSAIL).hull


@pytest.fixture(scope="module")
def profile(spec):
    return spec.profile


@pytest.fixture(scope="module")
def raw():
    return yaml.safe_load((ROOT / TOPSAIL).read_text(encoding="utf-8"))["hull"]["profile"]


# -- her profile and form load --------------------------------------------------------------------


@pytest.mark.parametrize("path", BOTH)
def test_her_profile_and_form_load_and_draw(path):
    """Build-Ships.md §5.1, §5.7: a raked transom and a small knee. No wale and no rising line are
    drawn on the plates (the note, §8), so none is given; the form's check passes."""
    hull = load_ship(path).hull.spec
    p = hull.profile
    assert p is not None and p.form is not None
    assert p.form.stern.type == "raked"
    assert p.form.head == "knee"
    assert p.form.fullness is None or not p.form.fullness
    assert not p.form.stern.galleries_m and not p.form.stern.lights_m  # no lights, no galleries
    assert not p.wales_m and not p.channel_wales_m and not p.floor_m
    assert drawn.check(hull)
    assert len(drawn.stations(hull)) >= 24


def test_the_two_files_carry_one_hull():
    """§5.0 principle 10 (the owner, 2026-10-28: "they would look alike except for where they
    specifically differ in details"): the profile the same to the byte's worth, its notes too, and
    the outlines one on the other. The pair stands in `SAME_HULL_BY_INTENT`
    (tests/test_profiles.py)."""
    one, other = (load_spec(path).hull for path in BOTH)
    assert one.profile == other.profile
    for view in drawn.VIEWS:
        assert drawn.outline(one, view) == drawn.outline(other, view), view
    texts = [(ROOT / path).read_text(encoding="utf-8") for path in BOTH]
    blocks = [t[t.index("  profile:\n") : t.index("\nspars:\n")] for t in texts]
    assert blocks[0] == blocks[1]


def test_every_line_of_her_shape_carries_its_rung(profile):
    """§5.0 principle 4: a mark on every line her profile gives, every group of her form and every
    key of her stern, each its weakest point's word. S† is `stand-in` (§5.7); what `JUDGED` names is
    `judged`. A rung's own word in the notes' keys, too."""
    marks = dict(profile.marks)
    given = [
        key
        for key in (
            "rail_m", "breadth_m", "keel_m", "stem_m", "stern_m", "wales_m", "section_m",
            "decks_m", "ports_m", "port_size_m", "head_m", "breadth_line_m", "sections_m",
            "channel_wales_m", "floor_m", "rabbet_m",
        )
        if getattr(profile, key)
    ]  # fmt: skip
    stern = ["knuckle_z_m", "transom_hb_m", "round_up_m"]
    assert list(marks) == [*given, "form.stern", *(f"form.stern.{k}" for k in stern), "form.head"]
    assert marks == {
        **dict.fromkeys(STAND_IN, "stand-in"),
        **dict.fromkeys(JUDGED, "judged"),
    }


# -- each point against the note ------------------------------------------------------------------


@pytest.mark.parametrize(
    "key",
    ["rail_m", "breadth_m", "keel_m", "stem_m", "stern_m", "section_m", "head_m", "breadth_line_m",
     "rabbet_m"],
)  # fmt: skip
def test_each_line_stands_as_the_note_gives_it(raw, key):
    """The note's §6.4, point for point, to the centimetre."""
    assert flat(note_list(note_section("6.4"), key)) == pytest.approx(flat(raw[key]), abs=0.001)


def test_her_deck_ports_and_sections_stand_as_the_note_gives_them(raw):
    """§6.4: the deck at side, the triples, the port's size and the sections by station."""
    section = note_section("6.4")
    assert note_list(section, "decks_m.upper") == raw["decks_m"]["upper"]
    assert note_list(section, "ports_m.upper") == raw["ports_m"]["upper"]
    assert raw["port_size_m"]["upper"] == [0.61, 0.82]
    assert f"**`port_size_m.upper`**: {raw['port_size_m']['upper']}" in section
    rows = re.findall(r"^  - ([−\d.]+): (.+)$", section, flags=re.M)
    assert rows
    in_note = [
        [numbers(x)[0], *numbers(point)]
        for x, body in rows
        for point in re.findall(r"\[([^\[\]]+)\]", body)
    ]
    assert in_note == raw["sections_m"]
    stern = raw["form"]["stern"]
    assert f"`knuckle_z_m: {stern['knuckle_z_m']}`" in section
    assert f"`round_up_m: {stern['round_up_m']}`" in section
    assert "`transom_hb_m: [2.30, 2.33]`" in section and stern["transom_hb_m"] == [2.3, 2.33]


def test_the_notes_plate_goes_to_the_file_by_its_factors(raw, spec):
    """§5.0 principle 7, as the note's §6.2 writes it, reckoned here from the note's §6.1: lengths
    by the load lines, 25.9 m over Lynx's 26.84 m; sections by the breadths, 7.3 m over 24 ft; 2 in
    of plank; the lowest sill, port 3's 0.948 m, where the plate has it (the lead's ruling), the
    sheer's rise above it by the length ratio; between the water and the sill line straight, above
    it by the sections' factor. Each point within 0.01 m, the double rounding."""
    plate = note_section("6.1")
    k_l = spec.length_waterline_m / 26.84
    k_b = spec.beam_m / (24.0 * FT)
    plank = 2.0 / 12.0 * FT
    sill_line = note_list(plate, "sill line")

    def sill(x):
        xs = [p[0] for p in sill_line]
        if x <= xs[0]:
            return sill_line[0][1]
        if x >= xs[-1]:
            return sill_line[-1][1]
        i = next(j for j in range(len(xs) - 1) if xs[j] <= x <= xs[j + 1])
        t = (x - xs[i]) / (xs[i + 1] - xs[i])
        return sill_line[i][1] + (sill_line[i + 1][1] - sill_line[i][1]) * t

    def lifted(x):
        return 0.948 + k_l * (sill(x) - 0.948)

    def height(x, z):
        if z <= 0.0:
            return z * k_b
        s = sill(x)
        return z * lifted(x) / s if z <= s else lifted(x) + (z - s) * k_b

    for key, name in (("rail_m", "rail"), ("keel_m", "keel"), ("stem_m", "stem"),
                      ("stern_m", "stern"), ("head_m", "head")):  # fmt: skip
        points = note_list(plate, name)
        want = [[x * k_l, height(x, z)] for x, z in points]
        assert flat(want) == pytest.approx(flat(raw[key]), abs=0.0101), key
    points = note_list(plate, "deck")
    want = [[x * k_l, height(x, z)] for x, z in points]
    assert flat(want) == pytest.approx(flat(raw["decks_m"]["upper"]), abs=0.0101)
    breadth = note_list(plate, "breadth")
    want = [[x * k_l, (w + plank) * k_b, (r + plank) * k_b] for x, w, r in breadth[:-1]]
    assert flat(want) == pytest.approx(flat(raw["breadth_m"][:-1]), abs=0.0101)
    # the rest of what the plates give, by the same factors: the sections by station (§5.8), the
    # main breadth (§5.7), the dead flat (§5.6) and the rabbet (§6.1)
    rows = re.findall(r"^\| \d+ \| ([−\d.]+) \| (\[.*\]) \|$", note_section("5.8"), flags=re.M)
    assert len(rows) == 24
    want = []
    for x, body in rows:
        x = numbers(x)[0]
        points = [numbers(p) for p in re.findall(r"\[([^\[\]]+)\]", body)]
        for i, (z, hb) in enumerate(points):
            siding = x == 13.67 and i == 0  # the stem's half-siding takes no plank
            want.append([x * k_l, height(x, z), hb * k_b if siding else (hb + plank) * k_b])
    assert flat(want) == pytest.approx(flat(raw["sections_m"]), abs=0.0101)
    rows = re.findall(
        r"^\| \d+ \| ([−\d.]+) \| ([\d.]+) \| ([\d.]+) \| [\d.]+ to [\d.]+ \|$",
        note_section("5.7"),
        flags=re.M,
    )
    assert len(rows) == 15
    want = [
        [numbers(x)[0] * k_l, height(numbers(x)[0], float(z)), (float(hb) + plank) * k_b]
        for x, z, hb in rows
    ]
    assert flat(want) == pytest.approx(flat(raw["breadth_line_m"]), abs=0.0101)
    dead_flat = note_section("5.6")
    zs = numbers(re.search(r"^\| z \(m\) \|(.*)\|$", dead_flat, flags=re.M).group(1))
    hbs = numbers(re.search(r"^\| ½-breadth \(m\) \|(.*)\|$", dead_flat, flags=re.M).group(1))
    # the keel's lower edge and the rabbet are at the half-siding, which takes no plank
    want = [
        [height(2.15, z), hb * k_b if i < 2 else (hb + plank) * k_b]
        for i, (z, hb) in enumerate(zip(zs, hbs, strict=True))
    ]
    assert flat(want) == pytest.approx(flat(raw["section_m"]), abs=0.0101)
    want = [[x * k_l, height(x, z), hs * k_b] for x, z, hs in note_list(plate, "rabbet")]
    assert flat(want) == pytest.approx(flat(raw["rabbet_m"]), abs=0.0101)


def test_her_sections_run_fair_along_the_ship(raw):
    """The sheet's own lines are fair, so a misread section shows along the ship: at each level the
    file gives station by station, stations 3 to 19, the second difference of the half-breadths is
    within 0.15 m, each within 0.075 m of the straight between its neighbours (measured; the first
    reading gave 0.25 m at station 9 at z -1.9, and 0.18 m at z -2.4 and at the first point above
    the water: the note's §5.8)."""
    stations: dict[float, list[list[float]]] = {}
    for x, z, hb in raw["sections_m"]:
        stations.setdefault(x, []).append([z, hb])
    xs = sorted(stations)[3:20]  # the ends turn in as fast as they are read
    levels = {
        "below, -1.9": lambda points: [hb for z, hb in points if abs(z + 1.9) < 0.011],
        "below, -2.4": lambda points: [hb for z, hb in points if abs(z + 2.4) < 0.011],
        "above, the first": lambda points: [hb for z, hb in points if z > 0.0][:1],
        "above, the second": lambda points: [hb for z, hb in points if z > 0.0][1:2],
    }
    for level, pick in levels.items():
        run = [pick(stations[x])[0] for x in xs if pick(stations[x])]
        assert len(run) >= 10, level
        worst = max(abs(a - 2.0 * b + c) for a, b, c in zip(run, run[1:], run[2:], strict=False))
        assert worst <= 0.15, level


# -- her ports and guns ---------------------------------------------------------------------------


def test_each_port_gun_stands_on_a_triple_of_its_deck():
    """Build-Ships.md §4.4, §5.3 and truth 7-185: every port gun's (x_m, height_m) on a triple of
    its deck within 0.01 m, its deck named, in both fits (schema `_PORT_GUN_PLACES`); a pivot and a
    rail gun have no port and stand on the rail at their own x."""
    spec = load_spec(PRIVATEER)
    p = spec.hull.profile
    seen = 0
    for name, fit in spec.armament.fits.items():
        for gun in fit.guns:
            if gun.place in ("broadside", "bow", "stern"):
                assert gun.deck == "upper", gun.id
                on = [
                    t
                    for t in ports_of(p, gun.deck)
                    if abs(t[0] - gun.x_m) <= 0.01 and abs(t[1] - gun.height_m) <= 0.01
                ]
                assert on, (name, gun.id, gun.x_m, gun.height_m)
                seen += 1
            else:
                assert gun.deck is None, gun.id
                assert gun.height_m == pytest.approx(rail_at(p, gun.x_m), abs=0.01), gun.id
    assert seen == 10  # six long 6s and four carronades


def test_the_plates_seven_ports_stand_as_eight_triples(profile):
    """The note's §6.3: no gun's x_m moves (§5.3), so ports 1, 3 and 5, in which no gun stands, are
    the plate's, and the others stand at their guns' places, the second at two, one for each fit."""
    xs = [t[0] for t in ports_of(profile, "upper")]
    assert xs == [-10.86, -8.4, -7.5, -2.08, 0.0, 4.81, 8.4, 10.5]
    table = note_section("6.3")
    for x in xs:
        assert f"**{x:.2f}**".replace("-", "−") in table, x


def test_the_transom_rakes_about_38_degrees_the_chord_named(profile):
    """§5.7 as the lead amended it (2026-10-31; the note's §5.9): the face, from the transom's lower
    corner to the taffrail, rakes about 38° from the upright; the chord from the taffrail to the
    post's head, about 45°, crosses the foot's band and is no drawn line."""
    (x_head, z_head), (x_foot, z_foot), (x_top, z_top) = profile.stern_m[-3:]
    assert math.degrees(math.atan2(x_foot - x_top, z_top - z_foot)) == pytest.approx(38.0, abs=1.0)
    assert math.degrees(math.atan2(x_head - x_top, z_top - z_head)) == pytest.approx(45.0, abs=1.0)
    assert "**37.8° to 38.6° to the water's square**" in note_section("5.9")
    design = (ROOT / "docs" / "design" / "Build-Ships.md").read_text(encoding="utf-8")
    assert "raked about 38° from the upright" in design


def test_each_sill_stands_in_its_sources_band(profile):
    """§5.4, each sill's band and its source: the plate's own, her own sheet over Spider's 3 ft 5 in
    of 1835 (the lead's ruling, 2026-10-31; the note's §6.2)."""
    triples = {t[0]: t[1] for t in ports_of(profile, "upper")}
    # the lowest: the plate's port 3, 3 ft 1 in, measured 3.11 ft ±0.05 ft (the note's §5.4), as
    # Steel's schooner's 3 ft 1 in (Folio XXXII, the note's §10.1), and it stands where she has it
    assert min(triples.values()) == pytest.approx(3.11 * FT, abs=0.05 * FT)
    assert min(triples, key=triples.get) == -2.08
    # amidships, the ports 3 and 4 of the plate: 3 ft 1 in to 3 ft 2 in (the note's §5.4, ±0.05 ft)
    assert 3.06 * FT <= triples[0.0] <= 3.24 * FT
    # aft, the ports 1 and 2: 3 ft 4 in to 3 ft 11 in (the note's §5.4, ±0.05 ft), a gun's own port
    # read on the same line
    for x in (-10.86, -8.4, -7.5):
        assert 3.32 * FT <= triples[x] <= 3.98 * FT, x
    # forward: the plate's port 5, 3 ft 8 in, and ports 6 and 7, 4 ft 4 in to 5 ft 0 in, the rise
    # above the lowest by the length ratio (the note's §6.2) taking off at most 2 cm
    assert triples[4.81] == pytest.approx(3.63 * FT, abs=0.05 * FT)
    for x in (8.4, 10.5):
        assert (4.32 - 0.05) * FT - 0.02 <= triples[x] <= (5.02 + 0.05) * FT, x
    # above the deck at side and below the rail at each port (§5.2's refusals, as measured)
    for x, sill in triples.items():
        assert deck_at(profile, x) + 0.10 <= sill <= rail_at(profile, x) - 0.60, x


# -- the drawing beside the file, reported --------------------------------------------------------

REPORT_PROBE = """
import sys
sys.path.insert(0, "tools")
import gen_ships
sys.modules["gen_ships"] = gen_ships
gen_ships.schooner(sys.argv[1])
gen_ships.schooner(sys.argv[1], armed=True)
"""


def test_the_drawn_hull_stands_beside_the_filed_figures(spec):
    """§5.0 principle 8: recorded and never moved. The drawn displacement within 15% of the filed
    (198 t against 211, measured) and the drawn depth at the greatest section beside the file's
    draught (3.10 m against 3.3, the drag kept: Lynx's own). Printed, as the report does."""
    kg = drawn.drawn_displacement_kg(spec)
    share = kg / spec.displacement_kg - 1.0
    depth = -min(pt[1] for pt in drawn._station_at(drawn._built(spec), 1.515))
    print(f"drawn {kg / 1000.0:.0f} t against the filed {spec.displacement_kg / 1000.0:.0f} t")
    print(f"drawn {depth:.2f} m deep against the file's draught of {spec.draught_m:g} m")
    assert abs(share) <= 0.15
    assert kg / 1000.0 == pytest.approx(198.0, abs=2.0)
    assert depth == pytest.approx(3.10, abs=0.02)
    assert spec.draught_m == 3.3  # never moved


def test_each_port_triples_gap_to_the_drawn_side_is_reported_and_small(spec, capsys):
    """§5.3, §5.6: the plate's three ports measured, so a gap over 0.05 m raises at the generator;
    the five at the guns' places reported, as the cutter's three. All eight are held here, the worst
    0.016 m at the fore gun's port (measured). No triple is written from the drawing (§5.0
    principle 8)."""
    gaps = {}
    for x, sill, hb in ports_of(spec.profile, "upper"):
        gaps[x] = drawn.half_breadth_at(spec, x, sill) - hb
    with capsys.disabled():
        print("\nthe schooners' port triples, the drawn side less the half-breadth:", end=" ")
        print(", ".join(f"x {x:g} {g:+.3f} m" for x, g in gaps.items()))
    assert max(abs(g) for g in gaps.values()) <= 0.02
    assert len(gaps) == 8


def test_the_generators_report_says_what_her_notes_do_not(tmp_path):
    """The lead's ruling (2026-10-29, item 2): the drawn figures in the report argument, printed as
    each file is written, and in none of her notes; her two files come out as they stand."""
    done = subprocess.run(
        [sys.executable, "-c", REPORT_PROBE, str(tmp_path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert done.returncode == 0, done.stderr
    for path in BOTH:
        name = Path(path).stem
        said = "the hull as drawn (freesail/ship/form.py):"
        assert f"{name}: {said} drawn displacement 198 t against the filed 211 t" in done.stderr
        assert f"{name}: {said} drawn 3.10 m deep at the greatest section" in done.stderr
        assert f"{name}: {said} the upper deck's ports: the side at each sill" in done.stderr
        assert "the 3 measured each within 0.05 m" in done.stderr
        made = (tmp_path / Path(path).name).read_text(encoding="utf-8")
        text = (ROOT / path).read_text(encoding="utf-8")
        assert made == text
        for words in ("drawn displacement", "deep at the greatest section", "off the half-breadth",
                      "198 t", "3.10 m"):  # fmt: skip
            assert words not in text, words


# -- nothing the physics reads moved --------------------------------------------------------------


def physics_view(doc: dict) -> dict:
    """What the physics, the gunnery and the crews read of a file: the hull's figures but its
    profile, the spars, the sails, and the guns but for §5.3's height and deck."""
    hull = {k: v for k, v in doc["hull"].items() if k != "profile"}
    fits = {}
    for name, fit in (doc.get("armament") or {}).get("fits", {}).items():
        fits[name] = [
            {k: v for k, v in gun.items() if k not in ("height_m", "deck")} for gun in fit["guns"]
        ]
    return {"hull": hull, "spars": doc["spars"], "sails": doc["sails"], "fits": fits}


# The hull's figures as filed before her hull (`gen_ships.schooner`, read by the physics), so that
# this holds where git is not to hand.
HULL_FIGURES = {
    "length_waterline_m": 25.9,
    "beam_m": 7.3,
    "draught_m": 3.3,
    "displacement_kg": 211000.0,
    "gm_m": 1.0,
    "clr_x_m": 0.5,
    "hull_speed_kn": 11.5,
    "deck_height_m": 0.9,
}


@pytest.mark.parametrize("path", BOTH)
def test_no_figure_the_physics_reads_moved(path):
    """§5.0 principle 8, §5.6: her hull's figures as filed, and a diff of her file's physics keys
    against git, the commit before her hull, shows none: only the profile is added, and only a port
    or rail gun's height and its deck move (§5.3)."""
    now = yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))
    for key, value in HULL_FIGURES.items():
        assert now["hull"][key] == value, key
    assert now["hull"]["rudder"] == {
        "area_m2": 2.0, "max_angle_deg": 35, "rate_deg_s": 4.0, "span_m": 3.4,
    }  # fmt: skip
    shown = subprocess.run(
        ["git", "show", f"{BEFORE}:{path}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if shown.returncode != 0:
        pytest.skip(f"git has no {BEFORE} here: the hull's figures above still hold")
    before = yaml.safe_load(shown.stdout)
    assert physics_view(now) == physics_view(before)


def test_a_guns_height_is_what_moved_and_its_x_is_not():
    """§5.3: the guns' places as they were, from the file's own lines (Chapelle p. 82's ports, the
    fit's judgement): the six long 6s at +8.4, 0 and -8.4, the carronades at +10.5 and -7.5, the
    pivot at +2.6 and the swivels at +10 and -10; and the sills the triples'."""
    spec = load_spec(PRIVATEER)
    places = {
        name: sorted({(g.place, g.x_m) for g in fit.guns})
        for name, fit in spec.armament.fits.items()
    }
    assert places == {
        "long tom": sorted(
            [("pivot", 2.6), ("broadside", 10.5), ("broadside", -7.5), ("rail", 10.0),
             ("rail", -10.0)]
        ),
        "letter of marque": sorted(
            [("broadside", 8.4), ("broadside", 0.0), ("broadside", -8.4), ("rail", 10.0),
             ("rail", -10.0)]
        ),
    }  # fmt: skip
    heights = {
        name: sorted({(g.x_m, g.height_m) for g in fit.guns})
        for name, fit in spec.armament.fits.items()
    }
    assert heights == {
        "long tom": sorted([(2.6, 1.92), (10.5, 1.44), (-7.5, 1.04), (10.0, 2.3), (-10.0, 2.07)]),
        "letter of marque": sorted(
            [(8.4, 1.3), (0.0, 0.96), (-8.4, 1.07), (10.0, 2.3), (-10.0, 2.07)]
        ),
    }


def test_the_shut_heels_in_the_note_are_the_rule_of_the_game():
    """The note's §6.3: its sine is the sill less `PORT_SHUT_M` over the half-breadth, as
    `combat/shot.py`'s `lee_port_shut` reads them; the lowest port, 10.6 degrees (12.1 on Spider's
    3 ft 5 in, the first build)."""
    from freesail.combat.shot import PORT_SHUT_M, lee_port_shut

    heel = math.degrees(math.asin((0.95 - PORT_SHUT_M) / 3.51))
    assert heel == pytest.approx(10.6, abs=0.05)
    assert lee_port_shut(0.95, heel + 0.01, 3.51)
    assert not lee_port_shut(0.95, heel - 0.01, 3.51)
    assert "| **−2.08** | **0.95** | **3.51** | 10.6° |" in note_section("6.3")
