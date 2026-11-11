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
                [f"{key}::{name}@{place}", {"place": place, "name": name, "words": name, "drawing": d}]
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
    """Truth 7-501: every flag of every root's colours.yaml served exactly as the trunk served
    it before package 102 widened the form, plain and union down."""
    before = json.loads(BEFORE.read_text(encoding="utf-8"))["served"]
    now = served_now()
    assert sorted(now) == sorted(before)
    for k in before:
        assert now[k] == before[k], k


@pytest.mark.skipif(not __import__("shutil").which("node"), reason="Node is not installed")
def test_every_colours_drawing_is_drawn_as_before_the_package(tmp_path):
    """Truth 7-501, the viewer's half: each of those flags drawn at the main truck and at the
    peak in the same figures, ids, colours and points as before package 102."""
    before = json.loads(BEFORE.read_text(encoding="utf-8"))["drawn"]
    now = drawn_now(tmp_path)
    assert sorted(now) == sorted(before)
    for k in before:
        assert now[k] == before[k], k
