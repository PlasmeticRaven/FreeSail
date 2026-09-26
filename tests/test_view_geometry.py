"""Milestone 3b, package 23: the view's geometry (spec 3b §8).

`client/projection.js` is pure functions with no DOM, so its geometry is tested here by
running it in Node on the ship graph and snapshot the server serves (`freesail.api.
queries`). Where Node is not installed those tests are skipped; the Python tests of the
fields the projection reads always run.

- Goose-winging drawn true (spec M3 §9 item 13): the lee clew hauled up to the yard, the
  weather clew sheeted home, the sail a triangle whose foot rises to the lee yardarm.
- The fixed scale (item 14): the frame is the ship file's full rig, so spars sent down
  and yards braced round leave the bounds as they were.
- The draw order (spec M0-M2 §12 item 9): sails by the depth of their centre along the
  view axis, a class tie-break, and a staysail that crosses a mast cut in two there.
- Bowlines drawn faintly from the leech forward when hauled; the ringtail boom at the
  spanker's boom end.
"""

from __future__ import annotations

import json
import math
import shutil
import subprocess
from pathlib import Path

import pytest

from freesail.api import queries
from freesail.api.session import make_ship, make_world
from freesail.core.world import Scenario
from freesail.ship.parts import LineState, SailState

ROOT = Path(__file__).resolve().parents[1]
PROJECTION = ROOT / "client" / "projection.js"
FRIGATE = "data/ships/frigate-36.yaml"
SCHOONER = "data/ships/topsail-schooner.yaml"
NODE = shutil.which("node")
needs_node = pytest.mark.skipif(NODE is None, reason="Node is not installed")


def run_js(tmp_path: Path, data: dict, body: str):
    """Run `body` in Node with `P` the projection module and `d` the data; the value it
    returns comes back as JSON."""
    src = tmp_path / "data.json"
    src.write_text(json.dumps(data))
    script = (
        f"const P = require({json.dumps(str(PROJECTION))});\n"
        f"const d = JSON.parse(require('fs').readFileSync({json.dumps(str(src))}, 'utf8'));\n"
        f"const out = (function () {{ {body} }})();\n"
        "process.stdout.write(JSON.stringify(out));\n"
    )
    res = subprocess.run([NODE, "-e", script], capture_output=True, text=True, timeout=60)
    assert res.returncode == 0, res.stderr
    return json.loads(res.stdout)


WIND_ON_THE_LARBOARD_BOW = math.radians(-60.0)


def ship_state(ship, awa=WIND_ON_THE_LARBOARD_BOW, tack="larboard") -> dict:
    """The graph and a snapshot-shaped state for a bare ship (no World), with the wind
    and tack given rather than sailed to."""
    graph = queries.ship_graph(ship)
    snap = {
        "ship": {"tack": tack, "heel": 0.0},
        "wind": {"apparent_angle": awa},
        "sails": [
            {
                "id": s.id,
                "state": s.state.value,
                "reefs": s.reefs,
                "sheet_angle": s.sheet_angle,
                "backed": s.backed,
            }
            for s in ship.sails.values()
        ],
        "spars": [
            {
                "id": s.id,
                "state": "sent_down" if s.sent_down else "sound",
                "brace_angle": s.brace_angle,
                "rigged_out": s.rigged_out,
            }
            for s in ship.spars.values()
        ],
        "lines": [
            {"id": ln.id, "state": ln.state.value, "hauled": ln.hauled}
            for ln in ship.lines.values()
        ],
        "evolutions_in_progress": [],
    }
    return {"graph": graph, "snap": snap}


# ---------------------------------------------------------------------------
# The fields the projection reads
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("path", [FRIGATE, SCHOONER])
def test_the_graph_and_snapshot_carry_what_the_view_reads(path):
    world = make_world(7, path, Scenario(wind_from_deg=0.0, wind_speed_kn=10.0))
    graph = queries.ship_graph(world.ship)
    snap = queries.snapshot(world)
    booms = [s for s in graph["spars"] if s["class"] == "studdingsail_boom"]
    assert booms and all(s["rigged_out"] is False for s in booms)  # rigged in at the start
    assert all(s["rigged_out"] is True for s in graph["spars"] if s["class"] == "boom")
    assert all("rigged_out" in s for s in snap["spars"])
    bowlines = [ln for ln in graph["lines"] if ln["class"] == "bowline"]
    assert bowlines and all("hauled" in ln for ln in graph["lines"])
    assert all(ln["state"] == "free" for ln in bowlines)  # rove, not hauled out
    assert all("shivering" in s for s in snap["sails"])


# ---------------------------------------------------------------------------
# Goose-winging drawn true
# ---------------------------------------------------------------------------


@needs_node
@pytest.mark.parametrize("tack", ["starboard", "larboard"])
def test_a_goose_winged_sail_is_a_triangle_with_its_foot_rising_to_leeward(tmp_path, tack):
    ship = make_ship(FRIGATE)
    ship.sails["fore.course"].state = SailState.GOOSE_WINGED
    awa = math.radians(60.0 if tack == "starboard" else -60.0)
    data = ship_state(ship, awa=awa, tack=tack)
    got = run_js(
        tmp_path,
        data,
        """
        const sk = P.buildSkeleton(d.graph, d.snap);
        const f = sk.figures.find(x => x.kind === 'sail' && x.id === 'fore.course');
        const y = sk.spars['fore.yard'];
        return {corners: f.corners, path: f.path, centre: f.centre, a: y.a, b: y.b};
        """,
    )
    a, b = got["a"], got["b"]  # larboard and starboard yardarms
    weather_arm, lee_arm = (b, a) if tack == "starboard" else (a, b)
    tri = [p[-1] for p in got["path"]]  # the path's corners in order
    assert len(tri) == 4 and tri[0] == tri[-1]  # closed: three corners
    lee, weather, clew = tri[0], tri[1], tri[2]
    assert lee == lee_arm and weather == weather_arm  # the head along the whole yard
    assert clew[0] == pytest.approx(weather_arm[0]) and clew[1] == pytest.approx(weather_arm[1])
    assert clew[2] < weather_arm[2] - 5.0  # the weather clew sheeted home, well below
    # the foot rises from the weather clew to the lee clew, hauled up to the yard
    assert lee[2] > clew[2]
    corners = got["corners"]
    stbd_clew, larb_clew = corners[2], corners[3]  # a sheet finds its clew by side
    hauled_up = larb_clew if tack == "starboard" else stbd_clew
    assert hauled_up == lee_arm
    # its centre lies out to weather, as physics/sails.py puts the goose-wing's force
    side = 1.0 if tack == "starboard" else -1.0
    assert side * got["centre"][1] > 0.0


# ---------------------------------------------------------------------------
# The fixed scale
# ---------------------------------------------------------------------------


@needs_node
@pytest.mark.parametrize("facing_deg", [0.0, 90.0, 225.0])
def test_the_scale_is_the_full_rigs_whatever_is_sent_down_or_braced(tmp_path, facing_deg):
    ship = make_ship(FRIGATE)
    ship.sails["fore.topsail"].state = SailState.SET
    as_rigged = ship_state(ship)
    for spar in ship.spars.values():
        if spar.cls == "topgallant_mast":
            spar.sent_down = True
        if spar.is_yard:
            spar.brace_angle = spar.brace_limit
    struck = ship_state(ship)
    body = f"""
        const f = {math.radians(facing_deg)};
        const b = s => P.project(P.buildSkeleton(d[s].graph, d[s].snap), f, 0).bounds;
        const drawn = s => P.buildSkeleton(d[s].graph, d[s].snap).figures.filter(
            x => x.kind === 'spar' && x.id.includes('topgallant')).length;
        return {{rigged: b('rigged'), struck: b('struck'),
                n1: drawn('rigged'), n2: drawn('struck')}};
    """
    got = run_js(tmp_path, {"rigged": as_rigged, "struck": struck}, body)
    assert got["n1"] > 0 and got["n2"] == 0  # the topgallant masts and yards are not drawn
    for k in ("minX", "maxX", "minY", "maxY"):
        assert got["struck"][k] == pytest.approx(got["rigged"][k], abs=1e-6), k


# ---------------------------------------------------------------------------
# The draw order
# ---------------------------------------------------------------------------


@needs_node
def test_sails_are_drawn_far_to_near_by_their_centres(tmp_path):
    ship = make_ship(FRIGATE)
    for sid in ship.groups["plain sail"]:
        ship.sails[sid].state = SailState.SET
    for spar in ship.spars.values():
        if spar.is_yard:
            spar.brace_angle = -0.8 * spar.brace_limit
    data = ship_state(ship)
    got = run_js(
        tmp_path,
        data,
        """
        const f = 2.3;
        const sk = P.buildSkeleton(d.graph, d.snap);
        const proj = P.makeProjector(f, 0);
        const sc = P.project(sk, f, 0);
        const centres = {};
        const key = x => x.id + (x.piece ? ':' + x.piece : '');
        sk.figures.filter(x => x.kind === 'sail').forEach(
            x => { centres[key(x)] = proj(x.centre).depth; });
        return sc.figures.filter(x => x.kind === 'sail').map(
            x => [key(x), x.depth, centres[key(x)]]);
        """,
    )
    depths = [d for _, d, _ in got]
    assert depths == sorted(depths, reverse=True)  # far first
    for sid, depth, centre in got:
        assert depth == pytest.approx(centre), sid  # each by its centre


@needs_node
def test_a_tie_in_depth_is_broken_by_class(tmp_path):
    figs = [
        {"kind": "sail", "cls": "studding", "depth": 1.0, "id": "a"},
        {"kind": "spar", "cls": "yard", "depth": 1.0, "id": "b"},
        {"kind": "sail", "cls": "square", "depth": 1.0, "id": "c"},
        {"kind": "sail", "cls": "jibheaded", "depth": 1.0, "id": "d"},
        {"kind": "sail", "cls": "gaff", "depth": 1.0, "id": "e"},
        {"kind": "hull", "depth": 1.0, "id": "f"},
        {"kind": "sail", "cls": "square", "depth": 5.0, "id": "g"},
    ]
    got = run_js(tmp_path, {"figs": figs}, "return P.sortFigures(d.figs).map(f => f.id);")
    assert got == ["g", "f", "d", "e", "c", "a", "b"]


@needs_node
def test_a_staysail_that_crosses_a_mast_is_drawn_in_two_parts(tmp_path):
    ship = make_ship(FRIGATE)
    ship.sails["main.topmast_staysail"].state = SailState.SET
    data = ship_state(ship)
    whole = run_js(
        tmp_path,
        data,
        """
        const sk = P.buildSkeleton(d.graph, d.snap);
        return sk.figures.filter(x => x.id === 'main.topmast_staysail').map(x => x.corners);
        """,
    )
    assert len(whole) == 1  # as rigged it lies between the fore and main masts
    xs = [c[0] for c in whole[0]]
    # step the main mast forward into the staysail's cloth: it now crosses the mast
    for s in data["graph"]["spars"]:
        if s["id"] == "main.mast":
            s["x_m"] = (min(xs) + max(xs)) / 2.0
    got = run_js(
        tmp_path,
        data,
        """
        const sk = P.buildSkeleton(d.graph, d.snap);
        const parts = sk.figures.filter(x => x.id === 'main.topmast_staysail');
        const mx = parts[0].cut;  // the raked mast's x at the sail's centre height
        const sc = P.project(sk, 0.4, 0);
        const mine = sc.figures.filter(x => x.id === 'main.topmast_staysail');
        return {mx: mx,
                parts: parts.map(p => ({piece: p.piece, xs: p.path.map(s => s[s.length - 1][0])})),
                projected: mine.map(x => [x.piece, x.depth]),
                d: P.pathData(mine[0].path, true)};
        """,
    )
    assert abs(got["mx"] - (min(xs) + max(xs)) / 2.0) < 2.0  # at the mast, raked
    pieces = {p["piece"]: p["xs"] for p in got["parts"]}
    assert set(pieces) == {"forward", "abaft"}
    assert min(pieces["forward"]) >= got["mx"] - 1e-9
    assert max(pieces["abaft"]) <= got["mx"] + 1e-9
    depths = dict(got["projected"])
    assert depths["forward"] != pytest.approx(depths["abaft"])  # each in its own place
    assert got["d"].startswith("M") and " L" in got["d"] and got["d"].endswith("Z")


# ---------------------------------------------------------------------------
# Bowlines and the ringtail boom
# ---------------------------------------------------------------------------


@needs_node
def test_a_bowline_is_drawn_forward_from_the_leech_only_when_hauled(tmp_path):
    ship = make_ship(FRIGATE)
    ship.sails["main.topsail"].state = SailState.SET
    for spar in ship.spars.values():
        if spar.is_yard:
            spar.brace_angle = spar.brace_limit  # braced up for the starboard tack
    free = ship_state(ship, awa=math.radians(50.0), tack="starboard")
    line = ship.lines["main.topsail.bowline.starboard"]
    line.state, line.hauled = LineState.BELAYED, 1.0
    hauled = ship_state(ship, awa=math.radians(50.0), tack="starboard")
    body = """
        const lines = s => P.buildSkeleton(d[s].graph, d[s].snap).figures.filter(
            x => x.kind === 'line' && x.cls === 'bowline');
        const sk = P.buildSkeleton(d.hauled.graph, d.hauled.snap);
        const sail = sk.figures.find(x => x.id === 'main.topsail');
        return {free: lines('free').length, hauled: lines('hauled').map(x => [x.id, x.pts]),
                corners: sail.corners, fore: sk.spars['fore.mast'].x};
    """
    got = run_js(tmp_path, {"free": free, "hauled": hauled}, body)
    assert got["free"] == 0
    assert [h[0] for h in got["hauled"]] == ["main.topsail.bowline.starboard"]
    start, end = got["hauled"][0][1]
    b, c = got["corners"][1], got["corners"][2]  # the starboard leech
    assert start == pytest.approx([(b[i] + c[i]) / 2 for i in range(3)])
    assert end[0] > start[0]  # forward
    assert end[0] == pytest.approx(got["fore"], abs=1.0)  # to the mast ahead


@needs_node
@pytest.mark.parametrize(("path", "gaff_boom"), [(FRIGATE, "mizzen.boom"), (SCHOONER, "main.boom")])
def test_the_ringtail_boom_is_at_the_gaff_sails_boom_end(tmp_path, path, gaff_boom):
    ship = make_ship(path)
    host = next(s for s in ship.sails.values() if s.roles.get("boom") == gaff_boom)
    host.state = SailState.SET
    host.sheet_angle = math.radians(60.0)
    ringtail = ship.sails["ringtail"]
    ringtail.state = SailState.SET
    ship.spars["ringtail_boom"].rigged_out = True
    data = ship_state(ship, awa=math.radians(-150.0), tack="larboard")
    got = run_js(
        tmp_path,
        data,
        f"""
        const sk = P.buildSkeleton(d.graph, d.snap);
        const rb = sk.spars['ringtail_boom'], gb = sk.spars['{gaff_boom}'];
        const f = sk.figures.find(x => x.id === 'ringtail');
        return {{rb: [rb.a, rb.b], gb: [gb.a, gb.b], corners: f.corners}};
        """,
    )
    (ra, rb), (ga, gb) = got["rb"], got["gb"]
    assert ra == pytest.approx(gb)  # from the boom end, not the mast
    out = [rb[i] - ra[i] for i in range(3)]
    along = [gb[i] - ga[i] for i in range(3)]
    cos = sum(o * a for o, a in zip(out, along, strict=True)) / (
        math.dist(rb, ra) * math.dist(gb, ga)
    )
    assert cos == pytest.approx(1.0)  # run out along the boom
    assert rb[1] > 0.0  # to leeward (the wind on the larboard quarter)
    assert got["corners"][3] == pytest.approx(gb)  # the ringtail's inner clew at the boom end
