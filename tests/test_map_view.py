"""Package 33d: the chart's zoom and pan, and the library pane's Markdown, in Node.

`client/map.js` keeps the view's arithmetic in pure functions (`SeaMap.view`): the view
drawn from the track, the wheel's zoom about the point under it, the drag's pan, the
names at thirty pixels a mile and the scale bar's step. `client/library.js` renders the
library's pages from the Markdown the model reads (`Markdown.render`). Both are run here
in Node, as `tests/test_view_geometry.py` runs the projection; where Node is not
installed these tests are skipped.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

from freesail.agents import tools
from freesail.api.session import make_world
from freesail.core.world import Scenario

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "client" / "map.js"
LIBRARY = ROOT / "client" / "library.js"
NODE = shutil.which("node")
needs_node = pytest.mark.skipif(NODE is None, reason="Node is not installed")
NM = 1852.0
CABLE = 185.2


def run_js(tmp_path: Path, module: Path, data: object, body: str):
    """Run `body` in Node with `M` the module and `d` the data; its value comes back."""
    src = tmp_path / "data.json"
    src.write_text(json.dumps(data))
    script = (
        f"const M = require({json.dumps(str(module))});\n"
        f"const d = JSON.parse(require('fs').readFileSync({json.dumps(str(src))}, 'utf8'));\n"
        f"const out = (function () {{ {body} }})();\n"
        "process.stdout.write(JSON.stringify(out));\n"
    )
    res = subprocess.run([NODE, "-e", script], capture_output=True, text=True, timeout=60)
    assert res.returncode == 0, res.stderr
    return json.loads(res.stdout)


@needs_node
def test_the_fit_is_the_view_drawn_before_the_zoom(tmp_path):
    """With no zoom the map is drawn as before: the track and the ship with a margin of
    three tenths, at least `least` across, centred on their middle."""
    out = run_js(
        tmp_path,
        MAP,
        {},
        "return M.view.fitView([[0, 0], [1000, 500]], [1000, 500], 3 * 185.2, 300, 200);",
    )
    assert out["scale"] == pytest.approx(200 / 1300)
    assert (out["cx"], out["cy"]) == (500, 250)
    small = run_js(tmp_path, MAP, {}, "return M.view.fitView([], [10, 20], 555.6, 300, 300);")
    assert small["scale"] == pytest.approx(300 / (555.6 * 1.3))
    assert (small["cx"], small["cy"]) == (10, 20)


@needs_node
def test_the_wheel_zooms_about_the_point_under_it(tmp_path):
    """The spot under the cursor stays under it as the scale changes; the centre's own
    spot when the cursor is at the centre; within the limits."""
    out = run_js(
        tmp_path,
        MAP,
        {},
        """
        const V = M.view;
        const v = {scale: 0.1, cx: 1000, cy: -500};
        const spot = V.fromPixels(v, 400, 300, 320, 60);
        const z = V.zoomAbout(v, 1.25, 320, 60, 400, 300);
        const back = V.toPixels(z, 400, 300, spot[0], spot[1]);
        const mid = V.zoomAbout(v, 2, 200, 150, 400, 300);
        const most = V.zoomAbout(v, 1e9, 10, 10, 400, 300);
        const least = V.zoomAbout(v, 1e-9, 10, 10, 400, 300);
        return {z: z, back: back, mid: mid, most: most.scale, least: least.scale,
                max: V.MAX_SCALE, min: V.MIN_SCALE};
        """,
    )
    assert out["z"]["scale"] == pytest.approx(0.125)
    assert out["back"] == [pytest.approx(320), pytest.approx(60)]
    assert out["mid"] == {"scale": pytest.approx(0.2), "cx": 1000, "cy": -500}
    assert out["most"] == out["max"] and out["least"] == pytest.approx(out["min"])


@needs_node
def test_a_drag_moves_the_chart_with_the_hand(tmp_path):
    """A drag of (dx, dy) pixels carries what was under the hand with it: north is up, so
    a drag down shows what lies to the north."""
    out = run_js(
        tmp_path,
        MAP,
        {},
        """
        const V = M.view;
        const v = {scale: 0.5, cx: 0, cy: 0};
        const spot = V.fromPixels(v, 300, 300, 100, 100);
        const p = V.panBy(v, 40, 30);
        return {p: p, at: V.toPixels(p, 300, 300, spot[0], spot[1])};
        """,
    )
    assert out["p"] == {"scale": 0.5, "cx": -80, "cy": 60}
    assert out["at"] == [140, 130]


@needs_node
def test_the_names_and_the_scale_bar_follow_the_scale(tmp_path):
    """Names when a mile is thirty pixels (package 32's rule, kept); the graticule's step a
    cable, a mile, five miles or twenty by the view's width; the bar's words by its step."""
    out = run_js(
        tmp_path,
        MAP,
        {},
        """
        const V = M.view;
        return {
          named: [V.namesShown(31 / 1852), V.namesShown(29 / 1852)],
          steps: [V.gridStep(10 * 185.2), V.gridStep(21 * 185.2), V.gridStep(21 * 1852),
                  V.gridStep(101 * 1852)],
          words: [V.stepWords(185.2), V.stepWords(1852), V.stepWords(5 * 1852),
                  V.stepWords(20 * 1852)],
        };
        """,
    )
    assert out["named"] == [True, False]
    assert out["steps"] == [pytest.approx(CABLE), NM, 5 * NM, 20 * NM]
    assert out["words"] == ["1 cable", "1 mile", "5 miles", "20 miles"]


@needs_node
def test_a_place_held_on_the_chart_stays_as_the_reckoning_moves(tmp_path):
    """A view held at a place is kept by its latitude and longitude, so that it stays
    put on the chart while the reckoned position (the frame's origin) moves on."""
    out = run_js(
        tmp_path,
        MAP,
        {},
        """
        const V = M.view;
        const a = V.frameOf({reckoning: {lat_deg: 49.0, lon_deg: -5.0}, ship: {}});
        const at = a.at(3000, -2000);
        const b = V.frameOf({reckoning: {lat_deg: 49.05, lon_deg: -4.9}, ship: {}});
        const m = b.from(at);
        const back = b.at(m[0], m[1]);
        const plane = V.frameOf({ship: {x: 10, y: 20}});
        return {at: at, back: back, other: plane.from(at), plane: plane.from(plane.at(5, 6))};
        """,
    )
    assert out["back"]["lat"] == pytest.approx(out["at"]["lat"])
    assert out["back"]["lon"] == pytest.approx(out["at"]["lon"])
    assert out["at"]["lat"] == pytest.approx(49.0 - 2000 / (60 * NM))
    assert out["other"] is None, "a place on the chart is not a place on the plane"
    assert out["plane"] == [5, 6]


@needs_node
@needs_node
def test_old_bearing_lines_fade_and_are_dropped_from_the_drawing(tmp_path):
    """Package 37n, the owner's addition: a bearing is drawn full for a glass after it is
    taken, fades over the rest of a watch, is dropped after the watch, and at once when a
    later bearing of the same mark replaces it; the snapshot's list itself is not touched."""
    bearings = [
        {"tick": 0, "id": "lizard", "bearing_deg": 10.0},
        {"tick": 0, "id": "manacles", "bearing_deg": 300.0},
        {"tick": 5000, "id": "dodman", "bearing_deg": 40.0},
        {"tick": 9000, "id": "lizard", "bearing_deg": 20.0},
        {"tick": 9500, "id": "black_head", "bearing_deg": 80.0},
    ]
    out = run_js(
        tmp_path,
        MAP,
        bearings,
        """
        const V = M.view;
        const at = t => V.bearingsShown(d, t).map(s => [s.bearing.id, s.bearing.tick, s.alpha]);
        return {early: at(1000), later: at(10000), old: at(14500), n: d.length,
                full: V.BEARING_FULL_S, drop: V.BEARING_DROP_S, ghost: V.BEARING_GHOST_ALPHA};
        """,
    )
    assert (out["full"], out["drop"]) == (1800, 4 * 3600)  # a glass, a watch
    # within the glass every bearing is full; the first Lizard is not yet replaced
    assert [(i, a) for i, _, a in out["early"]] == [("lizard", 1), ("manacles", 1)]
    later = {(i, t): a for i, t, a in out["later"]}
    assert ("lizard", 0) not in later  # replaced by the later bearing of the Lizard
    assert later[("lizard", 9000)] == 1 and later[("black_head", 9500)] == 1
    assert out["ghost"] < later[("manacles", 0)] < later[("dodman", 5000)] < 1  # fading
    old = {i for i, _, _ in out["old"]}
    assert "manacles" not in old and "dodman" in old  # dropped after the watch
    assert out["n"] == 5  # the record untouched


@needs_node
def test_the_charts_tools_read_bearings_and_distances(tmp_path):
    """Package 37n: a line's bearing and length by the plane sailing at the middle
    latitude; a bearing true and by the compass with the variation the master allows; the
    rose's grips and its index turned to the hand; a mark in the list's words."""
    out = run_js(
        tmp_path,
        MAP,
        {},
        """
        const V = M.view;
        const north = V.measure({lat: 50, lon: -5}, {lat: 50.1, lon: -5});
        const east = V.measure({lat: 50, lon: -5}, {lat: 50, lon: -4.9});
        const plane = V.measure({x: 0, y: 0}, {x: -1852, y: -1852});
        return {
          north: north, east: east, plane: plane,
          words: V.bearingWords(45, 24), plain: V.bearingWords(45, null),
          cables: V.distanceWords(0.4), miles: V.distanceWords(3.25),
          hit: [V.roseHit(100, 100, 80, 105, 103), V.roseHit(100, 100, 80, 100, 25),
                V.roseHit(100, 100, 80, 140, 100)],
          turn: [V.bearingOfPixel(100, 100, 100, 20), V.bearingOfPixel(100, 100, 180, 100),
                 V.bearingOfPixel(100, 100, 20, 100)],
          ring: V.markWords(
            {kind: 'ring', points: [{lat: 49.9625, lon: -5.2}], radius_m: 3704}, 24),
          note: V.markWords({kind: 'note', points: [{x: 0, y: 1852}], text: 'shoal?'}, null),
          line: V.markWords({kind: 'line', points: [{x: 0, y: 0}, {x: 0, y: 926}]}, null),
          variation: V.variationOf({reckoning: {variation: {deg_west: 24.5}}}),
          none: V.variationOf({reckoning: null}),
        };
        """,
    )
    assert out["north"]["bearing_deg"] == pytest.approx(0.0)
    assert out["north"]["distance_nm"] == pytest.approx(6.0)
    assert out["east"]["bearing_deg"] == pytest.approx(90.0)
    assert out["east"]["distance_nm"] == pytest.approx(6.0 * 0.6428, rel=1e-3)  # cos 50°
    assert out["plane"]["bearing_deg"] == pytest.approx(225.0)
    assert out["words"] == "045° true, ENE by the compass (069°)"
    assert out["plain"] == "045° true, NE"
    assert (out["cables"], out["miles"]) == ("4 cables", "3.3 miles")
    assert out["hit"] == ["centre", "rim", None]
    assert out["turn"] == [0, 90, 270]
    assert out["ring"] == "ring of 2.0 miles about 49°58' N, 5°12' W"
    assert out["note"] == "note at x 0.00 nm, y 1.00 nm: shoal?"
    assert out["line"] == "line 000° true, N, 5 cables"
    assert (out["variation"], out["none"]) == (24.5, None)


def test_the_library_pane_renders_the_models_markdown(tmp_path):
    """The pane's renderer: a primer chapter's headings, tables and code from the very
    text the tool serves, nothing of the page let through as markup, and a
    `library(...)` named in a page's words made a link to that page."""
    world = make_world(7, "data/ships/frigate-36.yaml", Scenario())
    pages = {
        "chapter": str(tools.library(world, "captain", "primer 1", "all")),
        "contents": str(tools.library(world, "captain", "contents")),
        "listing": str(tools.library(world, "captain", "primer 3")),
        "hostile": "A <script>alert(1)</script> & a [link](javascript:x) `<b>`",
    }
    out = run_js(
        tmp_path,
        LIBRARY,
        pages,
        """
        const R = M.Markdown.render;
        const o = {};
        for (const k of Object.keys(d)) o[k] = R(d[k]);
        o.args = M.Markdown.callArgs("topic='primer 3', section='reefing'");
        return o;
        """,
    )
    assert "<h2>" in out["chapter"] and "<table>" in out["chapter"]
    assert "<pre><code>" in out["chapter"]
    assert 'class="library-call" data-topic="primer 3"' in out["contents"]
    assert '<ul class="numbered">' in out["listing"] and "3.1 " in out["listing"]
    assert "<script>" not in out["hostile"] and "&lt;script&gt;" in out["hostile"]
    assert "javascript" not in out["hostile"] and "<code>&lt;b&gt;</code>" in out["hostile"]
    assert out["args"] == {"topic": "primer 3", "section": "reefing", "find": ""}
