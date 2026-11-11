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
