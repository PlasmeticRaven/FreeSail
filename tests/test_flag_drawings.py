"""Package 102 (the signals seen and the ship dressed), step 1: the drawing's form widened by
the least the plates ask (`poly`, a polygon of points on the flag's own square, and the flag's
`shape`, a swallow tail or a triangle), and every drawing that stood before it served and
drawn exactly as before.

The proof is old beside new: `tests/fixtures/flag_drawings_before_102.json` holds, as the
trunk served and drew them before the package (recorded at its head, 2026-11-11, by
`record()` below), every flag of every root's `colours.yaml` (each nation's block of basic's
too) served both ways (`Flag.served_drawing`, plain and turned union down) and the figures
`client/projection.js` draws for each at the main truck and at the peak of the frigate, the
wind on her larboard bow; the tests here serve and draw them again and compare.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from freesail.world import flags as F
from freesail.world import signals as S

ROOT = Path(__file__).resolve().parents[1]
BEFORE = ROOT / "tests" / "fixtures" / "flag_drawings_before_102.json"
PLACES = ("main truck", "peak")


def every_flag() -> list[tuple[str, str, F.Flag]]:
    """(the file's key, the flag's name, the flag) of every root and every block of basic's,
    in a fixed order."""
    out = []
    for root in sorted(S.roots()):
        f = F.load_colours(root)
        for key, g in [(root, f), *sorted((f"{root}/{k}", v) for k, v in f.nations.items())]:
            for name in sorted(g.flags):
                out.append((key, name, g.flags[name]))
    return out


def served_now() -> dict:
    return {
        f"{key}::{name}": [flag.served_drawing(False), flag.served_drawing(True)]
        for key, name, flag in every_flag()
    }


DRAW_EVERY = """
  const out = {};
  for (const [k, flag] of d.flags) {
    const snap = Object.assign({}, d.snap, {flags: [flag]});
    const sk = P.buildSkeleton(d.graph, snap);
    out[k] = sk.figures.filter(f => f.kind === 'flag').map(f => [f.id, f.cls, f.piece,
      f.pts.map(p => p.map(v => Math.round(v * 1e6) / 1e6))]);
  }
  return out;
"""


def drawn_now(tmp_path: Path) -> dict:
    from tests.test_view_action import FRIGATE, _state
    from tests.test_view_geometry import run_js

    data = _state(FRIGATE)
    flags = []
    for key, name, flag in every_flag():
        for place in PLACES:
            d = flag.served_drawing(False)
            flags.append(
                [
                    f"{key}::{name}@{place}",
                    {"place": place, "name": name, "words": name, "drawing": d},
                ]
            )
    data["flags"] = flags
    return run_js(tmp_path, data, DRAW_EVERY)


def record(tmp_path: Path) -> None:
    """Write the fixture (run once, on the trunk's head before the package's form)."""
    BEFORE.write_text(
        json.dumps({"served": served_now(), "drawn": drawn_now(tmp_path)}, sort_keys=True),
        encoding="utf-8",
    )


def test_every_colours_drawing_is_served_as_before_the_package():
    """Truth 7-500: every flag of every root's colours.yaml served exactly as the trunk served
    it before package 102 widened the form, plain and union down."""
    before = json.loads(BEFORE.read_text(encoding="utf-8"))["served"]
    now = served_now()
    assert sorted(now) == sorted(before)
    for k in before:
        assert now[k] == before[k], k


@pytest.mark.skipif(not __import__("shutil").which("node"), reason="Node is not installed")
def test_every_colours_drawing_is_drawn_as_before_the_package(tmp_path):
    """Truth 7-500, the viewer's half: each of those flags drawn at the main truck and at the
    peak in the same figures, ids, colours and points as before package 102."""
    before = json.loads(BEFORE.read_text(encoding="utf-8"))["drawn"]
    now = drawn_now(tmp_path)
    assert sorted(now) == sorted(before)
    for k in before:
        assert now[k] == before[k], k


# -- the widened form ------------------------------------------------------------------------


def _file(tmp_path, drawing: str, extra: str = "") -> F.ColoursFile:
    base = tmp_path / "signals"
    (base / "x").mkdir(parents=True, exist_ok=True)
    (base / "x" / "colours.yaml").write_text(
        "nation: x\nsources: [made]\nflags:\n  - name: cornet\n    kind: pendant\n"
        f"    proportion: [1, 2]\n{extra}    drawing:\n{drawing}    source: made\noccasions:\n"
        '  - {occasion: "at sea", role: "any", flags: [{name: cornet, where: "main truck"}]}\n',
        encoding="utf-8",
    )
    F.load_colours.cache_clear()
    try:
        return F.load_colours("x", str(base))
    finally:
        F.load_colours.cache_clear()


def test_a_poly_and_a_shape_are_read_and_served_apart(tmp_path):
    """Step 1: a `poly` part served under `polys` with its place in the drawing, the outline
    under `shape` with its cut (the default's where the file gives none); a part that is two
    things at once, a poly of two points and a shape not known are refused in words."""
    f = _file(
        tmp_path,
        "      - {rect: [0, 0, 1, 1], colour: white}\n"
        "      - {poly: [[0, 0], [1, 0], [0, 1]], colour: blue}\n",
        "    shape: swallowtail\n",
    )
    d = f.flags["cornet"].served_drawing()
    assert d["parts"] == [{"rect": [0, 0, 1, 1], "colour": "white", "n": 0}]
    assert d["polys"] == [{"poly": [[0, 0], [1, 0], [0, 1]], "colour": "blue", "n": 1}]
    assert d["shape"] == "swallowtail" and d["cut"] == pytest.approx(F.SWALLOWTAIL_CUT)
    assert "lines" not in d
    for bad, words in (
        ("      - {rect: [0, 0, 1, 1], poly: [[0, 0], [1, 0], [0, 1]], colour: red}\n", "a poly"),
        ("      - {poly: [[0, 0], [1, 0]], colour: red}\n", "a poly"),
    ):
        with pytest.raises(S.BookFileError, match=words):
            _file(tmp_path, bad)
    with pytest.raises(S.BookFileError, match="shape is one of"):
        _file(tmp_path, "      - {rect: [0, 0, 1, 1], colour: red}\n", "    shape: ball\n")


@pytest.mark.skipif(not __import__("shutil").which("node"), reason="Node is not installed")
def test_a_swallow_tail_is_cut_and_a_triangle_tapers(tmp_path):
    """Step 1, the viewer: a swallow-tailed flag's field drawn as its two halves with the notch
    out of the fly (no point of it inside the notch), a poly drawn at its points, and a
    triangle's fly drawn to a point at the middle of its hoist."""
    from tests.test_view_action import FRIGATE, _state
    from tests.test_view_geometry import run_js

    field = {"rect": [0, 0, 1, 1], "colour": "blue", "n": 0}
    half = {"poly": [[0, 0], [1, 1], [0, 1]], "colour": "white", "n": 1}
    tail = {"proportion": [1, 2], "parts": [field], "polys": [half], "shape": "swallowtail"}
    tail["cut"] = 0.5
    tri = {"proportion": [1, 2], "parts": [field], "shape": "triangle"}
    data = _state(FRIGATE)
    data["flags"] = [
        ["tail", {"place": "main truck", "name": "cornet", "words": "c", "drawing": tail}],
        ["tri", {"place": "main truck", "name": "repeater", "words": "r", "drawing": tri}],
        [
            "plain",
            {"place": "main truck", "name": "flag", "words": "f", "drawing": tri | {"shape": ""}},
        ],
    ]
    out = run_js(tmp_path, data, DRAW_EVERY)
    assert [f[0] for f in out["tail"]] == ["flag.0.0", "flag.0.1", "flag.0.2", "flag.0.3"]
    assert [f[1] for f in out["tail"]] == ["colour-blue"] * 2 + ["colour-white"] * 2
    plain = out["plain"][0][3]  # the same flag unshaped: its four corners
    head, foot = plain[0], plain[3]  # the hoist's head and foot
    fly_head = plain[1]

    def at(fx, fy):
        return [head[i] + fx * (fly_head[i] - head[i]) + fy * (foot[i] - head[i]) for i in range(3)]

    # the notch's apex, half the fly in at the middle, is a corner of both halves of the field
    apex = at(0.5, 0.5)
    for piece in out["tail"][:2]:
        assert any(all(abs(a - b) < 1e-4 for a, b in zip(p, apex, strict=True)) for p in piece[3])
    # the triangle's fly is one point, at the middle of the hoist's height
    tri_pts = out["tri"][0][3]
    tip = at(1.0, 0.5)
    assert all(abs(a - b) < 1e-4 for a, b in zip(tri_pts[1], tip, strict=True))
    assert all(abs(a - b) < 1e-4 for a, b in zip(tri_pts[2], tip, strict=True))


# -- step 2: every signal flag of every book drawn ----------------------------------------------


@pytest.mark.parametrize("root", S.roots())
def test_every_flag_a_hoist_can_hold_has_a_drawing(root):
    """Truth 7-501 (step 2): every flag a hoist of the root's books can hold (each numbered
    signal of the day and convoy books, each word of the dictionary, the answer, the private
    table's flags) and every flag its book.yaml declares has a drawing, marked `plate` or
    `made` with its source (tools/check_signals.py)."""
    from tools.check_signals import declared_flags, hoist_flag_names, signal_flags_problems

    books = S.load_books(root)
    names = hoist_flag_names(books) | declared_flags(books)
    assert F.ANSWERING in names and len(names) >= 10
    assert signal_flags_problems(root, books) == []
    for name in names:
        row = F.signal_flag(root, name, 1805)
        assert row.mark in F.MARKS and row.source, (root, name)


def test_a_flag_a_hoist_holds_and_no_file_draws_is_named(monkeypatch):
    """The check names a flag a hoist can hold that no flags.yaml draws."""
    from tools.check_signals import signal_flags_problems

    real = F.signal_flag
    monkeypatch.setattr(
        F, "signal_flag", lambda r, n, y: None if n == "numeral 7" else real(r, n, y)
    )
    problems = signal_flags_problems("britain", S.load_books("britain"))
    assert problems == ["britain: a hoist may hold the 'numeral 7' and no flags.yaml draws it"]


def test_the_british_numerals_are_drawn_by_the_year_from_perrins_plate():
    """Step 2: Britain's numeral 1 is Howe's red in 1792, the blue pierced white of the new
    arrangement in 1796 (the 1796 book's leaf 31), yellow, red, yellow in 1800 and white with
    the blue cross in 1805 (Perrin's Plate XIII); a year past the plate's last takes the
    nearest set (1820 the 1804-1810 set's), and the substitute changes with the sets."""

    def colours(name, year):
        return [p["colour"] for p in F.signal_flag("britain", name, year).flag.drawing]

    assert colours("numeral 1", 1792) == ["red"]
    assert colours("numeral 1", 1796) == ["blue", "white"]
    assert colours("numeral 1", 1800) == ["yellow", "red", "yellow"]
    assert colours("numeral 1", 1805) == ["white", "blue", "blue"]
    assert colours("numeral 1", 1820) == colours("numeral 1", 1805)
    assert colours("substitute", 1800) == ["white"]
    assert colours("substitute", 1805) == ["yellow", "black", "black"]
    assert F.signal_flag("britain", "numeral 1", 1805).mark == "plate"
    assert F.signal_flag("spain", "table flag 3", 1805).mark == "made"
    assert F.signal_flag("france", "guidon 1", 1805).flag.shape == "swallowtail"
    # a private table's plain flag is read from basic's file by every root
    assert F.signal_flag("naples", "blue pendant", 1805).flag.kind == "pendant"


def test_a_hoist_holds_its_flags_in_order_uppermost_first():
    """Step 2: the flags of a hoist, uppermost first: the first written figure uppermost
    (the 1796 book), a figure again the substitute, 111 the hundred pendant over 1 and the
    substitute; Barry's units uppermost; a table book's two flags a number, the universal for
    a lower flag the same as the upper, Spain's one-flag signals alone; Popham's word under the
    telegraph flag, the thousands' pendant over it; the answer the answering pendant; a private
    signal its flag; a light by night no flag."""

    def h(book, root, numbers=(), form="numerary", shown=""):
        x = S.Hoist(book=book, meaning="", by="", since=0, breaks_out=0, root=root)
        x.numbers, x.form, x.shown = tuple(numbers), form, shown
        return F.hoist_flags(x)

    assert h("numerary", "britain", (253,)) == ["numeral 2", "numeral 5", "numeral 3"]
    assert h("numerary", "britain", (16,)) == ["numeral 1", "numeral 6"]
    assert h("numerary", "britain", (22,)) == ["numeral 2", "substitute"]
    assert h("numerary", "britain", (111,)) == ["hundred pendant", "numeral 1", "substitute"]
    assert h("numerary", "united-states", (214,)) == ["numeral 4", "numeral 1", "numeral 2"]
    assert h("numerary", "france", (286,), "table") == ["table flag 15", "table flag 6"]
    assert h("numerary", "spain", (1,), "table") == ["table flag 1", "universal flag"]
    assert h("numerary", "spain", (409,), "table") == ["table flag 9"]
    assert h("numerary", "spain", (421,), "table") == ["universal flag"]
    assert h("telegraphic", "britain", (269,)) == [
        "telegraph flag",
        "numeral 2",
        "numeral 6",
        "numeral 9",
    ]
    assert h("telegraphic", "britain", (1987,))[:2] == ["telegraph flag", "thousand pendant"]
    assert h("answer", "britain") == ["answering pendant"]
    shown = "a blue pendant at the fore yardarm, with the ensign at the mizen peak"
    assert h("reply", "britain", shown=shown) == ["blue pendant"]
    assert h("night", "britain", shown="two lights horizontal at the mizen peak") == []


# -- step 3: a hoist has its place and is seen ---------------------------------------------------


def test_a_hoist_flies_at_the_main_unless_a_place_is_named_and_its_record_is_as_before():
    """Step 3 (a): a hoist with no place is 'at the main' in the lookout's words and its
    record (`to_dict`, the log's digest) and its pickle carry no place, as before the package;
    one at a named place says it and records it."""
    import pickle

    h = S.Hoist(book="numerary", meaning="Tack", by="a", since=0, breaks_out=0, numbers=(16,))
    assert h.flags_words() == "two flags at the main" and "place" not in h.to_dict()
    assert "place" not in pickle.loads(pickle.dumps(h)).__dict__
    h.place = "fore topgallant masthead"
    assert h.flags_words() == "two flags at the fore"
    assert h.to_dict()["place"] == "fore topgallant masthead"
    h.place = "main yardarm"
    assert h.flags_words() == "two flags at the main yardarm"
    for w in ("fore yardarm", "main topsail yardarm", "mizen topgallant yardarm"):
        assert F.place_ok(w)
    assert not F.place_ok("bowsprit yardarm")


def _signal_world():
    from tests.test_brains import world_at

    return world_at(49.5, -5.5, papers={"private_signals": True})


def test_the_players_hoist_is_served_at_its_place_flag_by_flag_and_gone_when_hauled_down():
    """Truth 7-502 (step 3, b): the player's own hoist, once broken out, is served in the
    snapshot's `hoists` at its place (the main topgallant masthead when the order names none),
    its flags in order, the uppermost first, each drawn by the scenario's year; an order may name
    the place ('at the fore'); hauled down, it is gone from the next snapshot."""
    from freesail.api import queries

    w = _signal_world()
    w.submit("make the signal No. 16")
    assert queries.snapshot(w)["hoists"] == []  # the minute to run it up
    w.run(120)
    snap = queries.snapshot(w)
    [h] = snap["hoists"]
    assert h["place"] == F.HOIST_PLACE and h["words"] == "two flags at the main"
    assert [f["name"] for f in h["flags"]] == ["numeral 1", "numeral 6"]
    year = w.clock.ship_time.year
    for f in h["flags"]:
        row = F.signal_flag("britain", f["name"], year)
        assert f["drawing"]["parts"] == row.flag.served_drawing()["parts"]
    w.submit("haul down the signal")
    assert queries.snapshot(w)["hoists"] == []
    w.submit("make the signal No. 16 at the fore")
    w.run(120)
    [h] = queries.snapshot(w)["hoists"]
    assert h["place"] == "fore topgallant masthead" and h["words"] == "two flags at the fore"
    said = [e for e in w.log if e.kind == "signal.ordered"][-1]
    assert said.data["hoist"]["place"] == "fore topgallant masthead"


def test_no_other_ships_hoist_is_served():
    """Step 3 (c) struck by the owner: a stranger's hoist is told as it is today, in words,
    and nothing of it is served in the snapshot."""
    from freesail.api import queries
    from tests.test_brains import put

    w = _signal_world()
    v = put(w, "frigate", "britain", "49 31 N 5 30 W", "bound for Plymouth", name="Amazon")
    books = S.load_books("britain")
    entry, q = books.find("tack in succession")
    h = S.make_hoist(S.vessel_locker(v), books, entry, q, v.id, int(w.clock.tick))
    assert h.flying(int(w.clock.tick) + 120)
    w.run(120)
    assert queries.snapshot(w)["hoists"] == []


@pytest.mark.skipif(not __import__("shutil").which("node"), reason="Node is not installed")
def test_a_hoist_is_drawn_down_its_halyard_from_its_place(tmp_path):
    """Truth 7-502, the viewer's half: each flag of a hoist hangs from its place, the uppermost
    first, the next one hoist (and the halyard's gap) lower, its hoist along the mast; at a
    yardarm from the yard's weather arm; nothing at a place the ship lacks."""
    from tests.test_view_action import FRIGATE, _state
    from tests.test_view_geometry import run_js

    def flag(name):
        row = F.signal_flag("britain", name, 1805)
        d = row.flag.served_drawing() | {"kind": row.flag.kind}
        return {"name": name, "words": row.words, "drawing": d}

    data = _state(FRIGATE)
    data["snap"]["hoists"] = [
        {
            "place": "main topgallant masthead",
            "key": "a",
            "words": "three flags at the main",
            "flags": [flag("numeral 2"), flag("numeral 5"), flag("numeral 3")],
        },
        {
            "place": "fore yardarm",
            "key": "b",
            "words": "a blue pendant",
            "flags": [flag("blue pendant")],
        },
    ]
    out = run_js(
        tmp_path,
        data,
        """
      const sk = P.buildSkeleton(d.graph, d.snap);
      const f = sk.figures.filter(f => f.kind === 'flag');
      const at = {};
      for (const w of ['main topgallant masthead', 'fore yardarm'])
        at[w] = P.flagPlace(d.graph, {}, sk.spars, w,
                            Math.sin(d.snap.wind.apparent_angle) >= 0 ? 1 : -1);
      const first = f.filter(x => x.id.endsWith('.0')).map(x => [x.of, x.pts]);
      return {ofs: f.map(x => x.of), first, at, beam: d.graph.hull.beam_m};
    """,
    )
    ofs = out["ofs"]
    assert ofs[0].startswith("hoist.0.") and {
        "hoist.0.0",
        "hoist.0.1",
        "hoist.0.2",
        "hoist.1.0",
    } <= set(ofs)
    tops = {of: max(p[2] for p in pts) for of, pts in out["first"]}
    top = out["at"]["main topgallant masthead"]
    assert abs(tops["hoist.0.0"] - top[2]) < 0.05
    assert tops["hoist.0.0"] > tops["hoist.0.1"] > tops["hoist.0.2"]
    beam = out["beam"]
    step = 0.3 * beam * 2 / 3 + 0.15  # a flag's hoist and the halyard's gap
    assert abs((tops["hoist.0.0"] - tops["hoist.0.1"]) - step) < 0.05
    arm = out["at"]["fore yardarm"]
    hoist_b = [pts for of, pts in out["first"] if of == "hoist.1.0"][0]
    assert min(abs(p[1] - arm[1]) + abs(p[0] - arm[0]) for p in hoist_b) < 0.05
    # nothing at a place the ship lacks: a brig has no mizen to cross a yard
    brig = _state("data/ships/brig.yaml")
    brig["snap"]["hoists"] = [
        {"place": "mizen yardarm", "key": "c", "words": "x", "flags": [flag("numeral 1")]}
    ]
    none = run_js(
        tmp_path,
        brig,
        "return P.buildSkeleton(d.graph, d.snap).figures.filter(f => f.kind === 'flag').length;",
    )
    assert none == 0


# -- step 4: dress ship -----------------------------------------------------------------------


def test_the_fashion_is_the_years_and_never_a_later_one():
    """Truth 7-503 (step 4): a ship dressed flies the fashion of the scenario's year: in 1805
    her flags in the yards, the stays and the shrouds (Röding 1794, Babron 1817), no flag
    along a line from masthead to masthead and none at a truck; the rainbow fashion only
    from 1884 (Luce), never before it."""
    from freesail.api import queries
    from freesail.api.session import make_ship
    from freesail.core.world import Scenario
    from freesail.world.nations import load_nations

    assert F.fashion_for("britain", 1805).name == "in the rigging"
    assert F.fashion_for("britain", 1883).name == "in the rigging"
    assert F.fashion_for("britain", 1884).name == "rainbow fashion"
    assert F.fashion_for("spain", 1795).name == "in the rigging"
    g = queries.ship_graph(make_ship("data/ships/frigate-36.yaml", Scenario()))
    n = load_nations()
    for year in (1792, 1805, 1825, 1883):
        hung = F.dressing_flies(g, n, "britain", "kings-ship", year)
        assert hung and not any("to" in x for x in hung), year
        assert not any(str(x.get("place", "")).endswith("truck") for x in hung), year
        places = {x.get("place") or "stay" for x in hung}
        assert {"fore yardarm", "main topsail yardarm", "stay"} <= places
    later = F.dressing_flies(g, n, "britain", "kings-ship", 1890)
    assert any("to" in x for x in later) and any(x.get("place") == "main truck" for x in later)
    # one flag of each in her stock: none hung twice
    names = [x["flags"][0]["name"] for x in F.dressing_flies(g, n, "britain", "kings-ship", 1805)]
    assert len(names) == len(set(names))
    # a merchantman dresses with what she has: her colours (package 96 holds what else)
    merchant = F.dressing_flies(g, n, "britain", "merchant", 1805)
    assert [x["flags"][0]["name"] for x in merchant] == ["merchant red ensign"]


def test_dress_ship_hangs_her_flags_until_undress_ship_sunset_or_the_colours_coming_down():
    """Truth 7-504 (step 4): `dress ship` on deck by day hangs her flags (served under the
    snapshot's `dressed`, and said by the `flags` reading); `undress ship` takes them down;
    dressed again, they come down at sunset of themselves, and with the colours; refused by
    night, with her colours down, and below as the colours' orders are."""
    from freesail.api import queries

    w = _signal_world()
    w.submit("dress ship")
    said = [e for e in w.log if e.kind == "colours.dressed"]
    assert said and "the yards, the stays and the shrouds" in said[-1].text
    hung = queries.snapshot(w)["dressed"]
    assert len(hung) >= 20 and all(len(x["flags"]) == 1 for x in hung)
    from freesail.api.signal_readings import _flags

    assert "the ship dressed" in _flags(w, None)["words"]
    w.submit("undress ship")
    assert queries.snapshot(w)["dressed"] == []
    assert [e for e in w.log if e.kind == "colours.undressed"]
    w.submit("dress ship")
    w.submit("haul down the colours")
    w.run(61)
    assert queries.snapshot(w)["dressed"] == []
    assert "colours down" in [e for e in w.log if e.kind == "colours.undressed"][-1].text
    w.submit("hoist the colours")
    w.submit("dress ship")
    assert queries.snapshot(w)["dressed"]
    while S.light_now(w) != "night":
        w.run(600)
    w.run(61)
    assert queries.snapshot(w)["dressed"] == []
    assert "Sunset" in [e for e in w.log if e.kind == "colours.undressed"][-1].text
    w.submit("dress ship")
    refused = [e for e in w.log if e.kind == "order.rejected"]
    assert "by day" in refused[-1].text


def test_dress_ship_is_refused_below_as_the_colours_are():
    """Step 4: the deck's order, refused from below in the colours' words (package 98,
    step 6)."""
    w = _signal_world()
    w.submit("hoist the colours")
    refused_colours = len([e for e in w.log if e.kind == "order.rejected"])
    w.submit("go below")
    w.run(30)
    w.submit("hoist the colours")
    w.submit("dress ship")
    refused = [e for e in w.log if e.kind == "order.rejected"][refused_colours:]
    assert len(refused) == 2
    assert refused[0].text.split(":")[-1] == refused[1].text.split(":")[-1]


def test_the_lookout_says_a_stranger_is_dressed():
    """Step 4: a stranger dressed, as the lookout reads her flags; not said of one that is
    not."""
    from tests.test_brains import put

    w = _signal_world()
    v = put(w, "frigate", "britain", "49 31 N 5 30 W", "bound for Plymouth", name="Amazon")
    assert "dressed" not in F.vessel_flies_words(w, v)
    S.vessel_locker(v).dressed = True
    assert F.vessel_flies_words(w, v).endswith("she is dressed in her flags")
