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
- Package 30b: the storm mizzen, a jib-headed sail on a stay with no run to another spar,
  placed from its file's geometry; a wreck cleared away not drawn.
- Package 75 (B5.1, docs/design/Build-Ships.md §6): a hull whose file gives a profile drawn
  from it, in strips; her masts' feet on her drawn decks and her bowsprit from her stem head;
  every other hull drawn as before; the lifts of every yard drawn faint.
- Package 75 (B5.6, §6 "The form's drawing"): the strips on the stations the server serves
  (freesail/ship/form.py's), down to the drawn depth; the stern by its type, the quarter
  galleries, the stern lights, the head and the channel wale; a lower mast's foot behind the
  near side; the hull below the water drawn three ways, hidden by the sea by default.
"""

from __future__ import annotations

import json
import math
import shutil
import subprocess
from dataclasses import replace
from pathlib import Path

import pytest

from freesail.api import queries
from freesail.api.session import make_ship, make_world
from freesail.core.world import Scenario
from freesail.evolutions.trim import set_sheet_angle
from freesail.ship import form
from freesail.ship.parts import LineState, SailState
from freesail.ship.profile import deck_at, interp
from freesail.ship.schema import HullStern

ROOT = Path(__file__).resolve().parents[1]
PROJECTION = ROOT / "client" / "projection.js"
FRIGATE = "data/ships/frigate-36.yaml"
SCHOONER = "data/ships/topsail-schooner.yaml"
CUTTER = "data/ships/cutter.yaml"  # package 32b: the four ships
BRIG = "data/ships/brig.yaml"
LUGGER = "data/ships/lugger.yaml"  # package 57
SIXTY_FOUR = "data/ships/sixty-four.yaml"  # package 75: the two files with a profile
RAZEE = "data/ships/razee-44.yaml"
PROFILED = [SIXTY_FOUR, RAZEE]
EVERY_SHIP = sorted(f"data/ships/{p.name}" for p in (ROOT / "data" / "ships").glob("*.yaml"))
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
    res = subprocess.run(
        [NODE, "-e", script], capture_output=True, text=True, encoding="utf-8", timeout=60
    )
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
                "lug_side": s.lug_side,  # package 57
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


@pytest.mark.parametrize("path", [FRIGATE, SCHOONER, CUTTER, BRIG])
def test_the_graph_and_snapshot_carry_what_the_view_reads(path):
    world = make_world(7, path, Scenario(wind_from_deg=0.0, wind_speed_kn=10.0))
    graph = queries.ship_graph(world.ship)
    snap = queries.snapshot(world)
    booms = [s for s in graph["spars"] if s["class"] == "studdingsail_boom"]
    if path != CUTTER:  # the cutter carries no studding sails (package 32b)
        assert booms
    assert all(s["rigged_out"] is False for s in booms)  # rigged in at the start
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
    # the head along the yard, its ends nine-tenths of the way out to the yardarms as the
    # ship file's course is cut (package 37n: the earings inside the yardarms)
    mid = [(p + q) / 2.0 for p, q in zip(a, b, strict=True)]

    def inside(arm):
        return [m + 0.9 * (x - m) for m, x in zip(mid, arm, strict=True)]

    assert lee == pytest.approx(inside(lee_arm)) and weather == pytest.approx(inside(weather_arm))
    assert clew[0] == pytest.approx(weather[0]) and clew[1] == pytest.approx(weather[1])
    assert clew[2] < weather_arm[2] - 5.0  # the weather clew sheeted home, well below
    # the foot rises from the weather clew to the lee clew, hauled up to the yard
    assert lee[2] > clew[2]
    corners = got["corners"]
    stbd_clew, larb_clew = corners[2], corners[3]  # a sheet finds its clew by side
    hauled_up = larb_clew if tack == "starboard" else stbd_clew
    assert hauled_up == lee
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
            x => { centres[key(x)] = proj(x.sortAt || x.centre).depth; });
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
    set_sheet_angle(ship, host, math.radians(60.0))  # through the sheet (package 32e)
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


# ---------------------------------------------------------------------------
# The storm mizzen (package 30b): a jib-headed sail on a stay with no run
# ---------------------------------------------------------------------------


def storm_mizzen_state(state: SailState = SailState.SET) -> dict:
    """The frigate with the storm mizzen bent in the spanker's place and the mizzen storm
    staysail set beside it, the wind on the larboard bow."""
    ship = make_ship(FRIGATE)
    ship.sails["mizzen.spanker"].state = SailState.UNBENT
    for sid in ("storm_mizzen", "mizzen.storm_staysail"):
        ship.sails[sid].state = state
        set_sheet_angle(ship, ship.sails[sid], math.radians(20.0))
    return ship_state(ship)


STORM_MIZZEN_BODY = """
    const sk = P.buildSkeleton(d.graph, d.snap);
    const f = id => sk.figures.filter(x => x.kind === 'sail' && x.id === id);
    const sm = f('storm_mizzen');
    return {n: sm.length, corners: sm.length ? sm[0].corners : null,
            path: sm.length ? sm[0].path : null,
            staysail: f('mizzen.storm_staysail').map(x => x.corners),
            stay: sk.stays['storm_mizzen.stay'], mizzen: sk.spars['mizzen.mast'],
            deck: d.graph.hull.deck_height_m};
"""


@needs_node
def test_the_storm_mizzen_is_drawn_from_its_file_on_its_vertical_stay(tmp_path):
    """The owner's report, playtest 10's finding 2: the storm mizzen's stay is of the
    mizzen mast and runs to no other spar (Luce 1884 ch. X: "hooked under the after
    trestle-tree, and set up on deck"), and the viewer drew it as a forestay, the sail lying
    on the mizzen storm staysail. It is placed from its file: the luff up the stay abaft the
    mast from a tack four feet above the deck, the foot aft towards the taffrail, the
    triangle's area and centre the file's."""
    ship = make_ship(FRIGATE)
    spec = next(s for s in ship.spec.sails if s.id == "storm_mizzen")
    mast_x = next(s for s in ship.spec.spars if s.id == "mizzen.mast").x_m
    got = run_js(tmp_path, storm_mizzen_state(), STORM_MIZZEN_BODY)
    assert got["n"] == 1  # drawn, whole: it crosses no mast
    tack, head, clew = got["corners"]
    stay = got["stay"]
    mizzen_head = got["mizzen"]["head"]
    # the stay hangs abaft the mizzen, parallel to it, from its head to the deck
    assert stay["abaft"] is True
    assert stay["head"][2] == pytest.approx(mizzen_head[2])
    assert stay["foot"][2] == pytest.approx(got["deck"])
    assert mast_x - 1.0 < stay["foot"][0] < mast_x
    # the luff lies along the stay; the tack four feet above the deck (the generator's)
    assert tack[1] == 0.0 and head[1] == 0.0
    assert tack[2] == pytest.approx(got["deck"] + 4 * 0.3048, abs=0.05)
    assert head[2] < mizzen_head[2]
    assert abs(head[0] - tack[0]) < 2.0  # nearly upright, as the raked mast is
    # the foot runs aft, to leeward (the wind on the larboard bow: to starboard)
    assert clew[0] < tack[0] - 4.0 and clew[1] > 0.0 and clew[2] == pytest.approx(tack[2])
    # the file's area and centre
    area = 0.5 * math.dist(tack, head) * math.dist(tack, clew)
    assert area == pytest.approx(spec.area_m2, rel=0.05)
    centre = [(tack[i] + head[i] + clew[i]) / 3 for i in range(3)]
    # a little abaft the file's centre: the stay stands abaft the mast, and the mast rakes aft
    assert spec.x_m - 1.2 < centre[0] < spec.x_m
    assert centre[2] == pytest.approx(spec.centre_height_m, abs=0.1)
    # and not on the mizzen storm staysail, which runs forward on the mizzen stay
    (mss,) = got["staysail"]
    assert all(c[0] > mast_x for c in mss)


@needs_node
def test_the_storm_mizzen_furled_is_drawn_as_a_bundle_at_its_luff(tmp_path):
    got = run_js(tmp_path, storm_mizzen_state(SailState.FURLED), STORM_MIZZEN_BODY)
    assert got["n"] == 1
    xs = [p[-1][0] for p in got["path"]]
    assert max(xs) - min(xs) < 2.0  # gathered along the stay, not spread aft


@needs_node
@needs_node
def test_the_cutter_is_drawn_from_her_file(tmp_path):
    """Package 32b: the viewer needs no art for a new hull. The cutter's gaff mainsail's
    boom overhangs the counter, her jib runs to the running bowsprit's end and her three
    yards hang on the one mast, every figure from the file's parts."""
    ship = make_ship(CUTTER)
    for sid in ship.groups["plain sail"]:
        ship.sails[sid].state = SailState.SET
    data = ship_state(ship)
    got = run_js(
        tmp_path,
        data,
        "const sk = P.buildSkeleton(d.graph, d.snap);"
        "const spars = {}; sk.figures.filter(x => x.kind === 'spar')"
        ".forEach(x => spars[x.id] = x.pts);"
        "const sails = {}; sk.figures.filter(x => x.kind === 'sail')"
        ".forEach(x => sails[x.id] = x.corners);"
        "return {spars: spars, sails: sails, hull: sk.hull};",
    )
    stern = -got["hull"]["length_waterline_m"] / 2.0
    boom = got["spars"]["main.boom"]
    assert boom[1][0] < stern  # the boom's end abaft the sternpost
    assert got["sails"]["main.sail"][2][0] < stern  # and the mainsail's clew with it
    bowsprit = got["spars"]["bowsprit"]
    tip = bowsprit[1]
    assert tip[0] > got["hull"]["length_waterline_m"] / 2.0 + 8.0  # a long bowsprit
    tack = got["sails"]["jib"][0]
    assert abs(tack[0] - tip[0]) < 1.5 and abs(tack[2] - tip[2]) < 1.5  # the jib's tack at its end
    yards = {
        sid: got["spars"][sid] for sid in ("square_sail.yard", "topsail.yard", "topgallant.yard")
    }
    heights = [(y[0][2] + y[1][2]) / 2.0 for y in yards.values()]
    assert heights == sorted(heights)  # square sail, topsail, topgallant, in order aloft
    assert len({round((y[0][0] + y[1][0]) / 2.0, 0) for y in yards.values()}) <= 2  # one mast


@needs_node
def test_the_brigs_staysails_are_drawn_between_her_masts(tmp_path):
    """Package 32b: the brig's main staysail, main topmast staysail and main topgallant
    staysail hang on stays from the main mast's heads to the fore mast, between the masts,
    and the viewer cuts none of them at a mast it does not cross."""
    ship = make_ship(BRIG)
    for sid in ("main.staysail", "main.topmast_staysail", "main.topgallant_staysail"):
        ship.sails[sid].state = SailState.SET
    data = ship_state(ship)
    got = run_js(
        tmp_path,
        data,
        "const sk = P.buildSkeleton(d.graph, d.snap);"
        "const out = {}; sk.figures.filter(x => x.kind === 'sail')"
        ".forEach(x => out[x.id] = x.corners);"
        "const spars = {}; sk.figures.filter(x => x.kind === 'spar')"
        ".forEach(x => spars[x.id] = x.pts);"
        "return {sails: out, spars: spars};",
    )
    fore_x = got["spars"]["fore.mast"][0][0]
    main_x = got["spars"]["main.mast"][0][0]
    for sid in ("main.staysail", "main.topmast_staysail", "main.topgallant_staysail"):
        corners = got["sails"][sid]
        assert corners, sid
        for p in corners:
            assert main_x - 1.0 <= p[0] <= fore_x + 1.0, (sid, p)
    heights = [
        got["sails"][sid][1][2]
        for sid in ("main.staysail", "main.topmast_staysail", "main.topgallant_staysail")
    ]
    assert heights == sorted(heights)  # each head above the last


def test_a_wreck_cleared_away_is_not_drawn(tmp_path):
    """Package 30b: the snapshot calls a spar carried away whose wreck has been cleared
    `cleared` (on deck or over the side); the viewer draws it, and what stood on it, no
    more than a spar sent down."""
    ship = make_ship(SCHOONER)
    boom = ship.spars["fore.topmast.studdingsail_boom.larboard"]
    boom.wrecked = boom.sent_down = True
    data = ship_state(ship)
    for s in data["snap"]["spars"]:
        if s["id"] == boom.id:
            s["state"] = "cleared"
    got = run_js(
        tmp_path,
        data,
        "return P.buildSkeleton(d.graph, d.snap).figures.filter(x => x.kind === 'spar')"
        ".map(x => x.id);",
    )
    assert boom.id not in got and "fore.topmast.studdingsail_boom.starboard" in got
    assert queries._spar_state(boom) == "cleared"


# ---------------------------------------------------------------------------
# Package 37n: the square sail from its file, and the yards at their hoist
# ---------------------------------------------------------------------------

SQUARE = (
    "const sk = P.buildSkeleton(d.graph, d.snap);"
    "const sails = {}; sk.figures.filter(x => x.kind === 'sail' && x.cls === 'square')"
    ".forEach(x => sails[x.id] = x.corners);"
    "const yards = {}; sk.figures.filter(x => x.kind === 'spar' && x.cls === 'yard')"
    ".forEach(x => yards[x.id] = {z: (x.pts[0][2] + x.pts[1][2]) / 2, hoist: x.hoist,"
    " state: x.state});"
    "const masts = {}; sk.figures.filter(x => x.kind === 'spar' && x.cls.endsWith('mast'))"
    ".forEach(x => masts[x.id] = {pts: x.pts, state: x.state});"
    "return {sails: sails, yards: yards, masts: masts, bounds: P.project(sk, 1.2, 0).bounds};"
)


def span(p, q) -> float:
    return math.hypot(q[0] - p[0], q[1] - p[1])


def quad_area(c) -> float:
    """A square sail's area from its corners: a trapezoid, the mean of head and foot by the
    depth between them (the yards braced square, so the depth is the heights')."""
    head, foot = span(c[0], c[1]), span(c[3], c[2])
    return (head + foot) / 2.0 * (c[0][2] - c[3][2])


def all_square(path: str, state: SailState = SailState.SET):
    ship = make_ship(path)
    for s in ship.sails.values():
        if s.cls == "square":
            s.state = state
    return ship


@needs_node
@pytest.mark.parametrize("path", [FRIGATE, SCHOONER, CUTTER, BRIG])
def test_every_square_sail_is_drawn_to_its_files_area_between_its_yards(tmp_path, path):
    """Set, braced square, every square sail's drawn area is the file's within a twentieth,
    its head within its yard and at the yard's height, and a sail with a yard below it
    reaches that yard: no sail falls short of the one below or overlaps it (the viewer drew
    a course a tenth short and a topgallant a sixth too deep)."""
    ship = all_square(path)
    for s in ship.spars.values():
        if s.is_yard:
            s.brace_angle = 0.0
    got = run_js(tmp_path, ship_state(ship), SQUARE)
    graph = queries.ship_graph(ship)
    yards = {s["id"]: s for s in graph["spars"]}
    for sail in graph["sails"]:
        if sail["class"] != "square":
            continue
        c = got["sails"][sail["id"]]
        assert quad_area(c) == pytest.approx(sail["area_m2"], rel=0.05), sail["id"]
        yard = yards[sail["roles"]["yard"]]
        assert span(c[0], c[1]) <= yard["length_m"] + 1e-6
        assert c[0][2] == pytest.approx(got["yards"][yard["id"]]["z"])
    pairs = (
        ("fore.topgallant", "fore.topsail.yard"),
        ("main.royal", "main.topgallant.yard"),
        ("topgallant", "topsail.yard"),
        ("topsail", "square_sail.yard"),
    )
    for sail, below in pairs:
        if sail in got["sails"] and below in got["yards"]:
            assert got["sails"][sail][3][2] == pytest.approx(got["yards"][below]["z"]), sail


@needs_node
def test_the_cutters_square_sail_is_its_files_twenty_seven_feet_deep(tmp_path):
    """The owner's note 6: the cutter's square sail is Steel's 'Sloop's square-sail, or
    cross-jack', 27 ft deep and nine-tenths of its 46 ft yard broad (tools/gen_ships.py, as
    its note in the file says); the viewer drew it 24 ft deep and the yard's whole breadth.
    The generator's figures were right: the fault was the viewer's."""
    ship = all_square(CUTTER)
    got = run_js(tmp_path, ship_state(ship), SQUARE)
    c = got["sails"]["square_sail"]
    feet = 0.3048
    assert (c[0][2] - c[3][2]) / feet == pytest.approx(27.0, abs=0.5)
    assert span(c[0], c[1]) == pytest.approx(0.9 * ship.spars["square_sail.yard"].length_m)
    assert "27 ft deep" in (ROOT / CUTTER).read_text()


@needs_node
@pytest.mark.parametrize("path", [FRIGATE, CUTTER])
def test_a_yard_is_drawn_at_its_hoist(tmp_path, path):
    """A topsail yard stands at the file's height with its sail set, on the cap of the
    mast below with its sail furled, halfway while its halyards are hoisted, and down by
    its reef's depth when reefed; a lower yard never moves; the view's scale is the same
    whatever the hoists."""
    sail, yard, lower_mast, lower = {
        FRIGATE: ("fore.topsail", "fore.topsail.yard", "fore.mast", "fore.yard"),
        CUTTER: ("topsail", "topsail.yard", "main.mast", "square_sail.yard"),
    }[path]
    base = make_ship(path)
    file_z = base.hull.spec.deck_height_m + base.spars[yard].height_m
    out = {}
    for case in ("set", "furled", "hoisting", "reefed"):
        ship = all_square(path, SailState.FURLED if case == "furled" else SailState.SET)
        if case == "hoisting":
            ship.sails[sail].state = SailState.SHEETED
        if case == "reefed":
            ship.sails[sail].reefs = 1
        data = ship_state(ship)
        if case == "hoisting":
            data["snap"]["evolutions_in_progress"] = [
                {"id": "set_square", "subject": sail, "step": "hoist", "waiting": False}
            ]
        out[case] = run_js(tmp_path, data, SQUARE)
    lower_head = max(p[2] for p in out["set"]["masts"][lower_mast]["pts"])
    assert out["set"]["yards"][yard] == {"z": pytest.approx(file_z), "hoist": 1, "state": "sound"}
    down = out["furled"]["yards"][yard]
    assert down["hoist"] == 0 and down["z"] == pytest.approx(lower_head + 0.3)
    half = out["hoisting"]["yards"][yard]
    assert half["hoist"] == 0.5 and half["z"] == pytest.approx((down["z"] + file_z) / 2)
    reefed = out["reefed"]["yards"][yard]["z"]
    assert down["z"] < reefed < file_z - 0.5
    for case in out.values():
        assert case["yards"][lower]["z"] == pytest.approx(out["set"]["yards"][lower]["z"])
        for k in ("minX", "maxX", "minY", "maxY"):
            assert case["bounds"][k] == pytest.approx(out["set"]["bounds"][k], abs=1e-6)


@needs_node
def test_struck_topmasts_are_housed_with_their_yards_on_the_caps(tmp_path):
    """Topmasts struck (strike_topmasts.yaml: the topgallant masts sent down first, the
    topsail yards "lowered on the caps", the topmasts sent down): the topmast is drawn
    housed, its head just above the lower cap, the topsail yard on that cap with its sail
    furled on it; the topgallant masts and yards sent down on deck are not drawn."""
    ship = all_square(FRIGATE, SailState.FURLED)
    upper = ("topmast", "topgallant_mast", "royal_mast")
    for s in ship.spars.values():
        if s.cls in upper or (s.is_yard and s.parent and ship.spars[s.parent].cls in upper):
            s.sent_down = True
    got = run_js(tmp_path, ship_state(ship), SQUARE)
    lower_head = max(p[2] for p in got["masts"]["fore.mast"]["pts"])
    topmast = got["masts"]["fore.topmast"]
    assert topmast["state"] == "struck"
    assert max(p[2] for p in topmast["pts"]) == pytest.approx(lower_head + 0.6)
    yard = got["yards"]["fore.topsail.yard"]
    assert yard["state"] == "struck" and yard["z"] == pytest.approx(lower_head + 0.3)
    assert "fore.topsail" in got["sails"]  # furled on its yard on the cap
    assert "fore.topgallant_mast" not in got["masts"]
    assert "fore.topgallant.yard" not in got["yards"] and "fore.topgallant" not in got["sails"]


# ---------------------------------------------------------------------------
# Package 57: the lug on its side, the draw order by the aspect, the brace shown, the
# flying sail sent down, Steel's four-sided staysails (the owner's notes of the Eclair's
# first cruise, 2026-10-17; the lead's finding of 18:29)
# ---------------------------------------------------------------------------


def lugger_by_the_wind(tack: str, sheet_deg: float = 20.0, topsails: bool = True) -> dict:
    """The lugger's lugs (and lug topsails) set on the lee side of `tack`, sheeted
    `sheet_deg` off the centreline: the graph and snapshot."""
    ship = make_ship(LUGGER)
    lee = "larboard" if tack == "starboard" else "starboard"
    ids = ["fore.lug", "main.lug", "mizen.lug"]
    if topsails:
        ids += ["fore.topsail", "main.topsail"]
    for sid in ids:
        sail = ship.sails[sid]
        sail.state = SailState.SET
        sail.sheet_angle = math.radians(sheet_deg)
        if sail.dipping:
            sail.lug_side = lee
    awa = math.radians(50.0) * (1.0 if tack == "starboard" else -1.0)
    return ship_state(ship, awa=awa, tack=tack)


LUG_FIGURES = """
    const sk = P.buildSkeleton(d.graph, d.snap);
    const fig = id => sk.figures.filter(f => f.id === id);
    const out = {};
    ['fore', 'main'].forEach(n => {
      const y = sk.spars[n + '.lug_yard'];
      const m = sk.spars[n + '.mast'];
      const pieces = fig(n + '.lug');
      const ts = fig(n + '.topsail');
      out[n] = {
        throat: y.a, peak: y.b, mx: m.xAt(y.centre[2]),
        pieces: pieces.map(f => [f.piece || '', f.centre]),
        corners: pieces[0].corners,
        topsail: ts.length ? ts[0].corners : null,
      };
    });
    return out;
"""


@needs_node
@pytest.mark.parametrize("tack", ["starboard", "larboard"])
def test_the_lugs_are_drawn_to_leeward_slung_a_third_from_their_fore_ends(tmp_path, tack):
    got = run_js(tmp_path, lugger_by_the_wind(tack), LUG_FIGURES)
    lee = -1.0 if tack == "starboard" else 1.0  # +1 starboard
    for name in ("fore", "main"):
        g = got[name]
        throat, peak, mx = g["throat"], g["peak"], g["mx"]
        # slung a third from the fore end: a third of the yard before the mast, two thirds
        # abaft it (Forfait pp. 5 to 6; the owner's confirmation of 2026-10-17)
        forward, abaft = throat[0] - mx, mx - peak[0]
        assert forward > 0.0 and abaft > 0.0, name
        assert abaft / forward == pytest.approx(2.0, rel=0.15), name
        # the yard's after end and the clew to leeward, the fore end nearer the centreline
        clew = g["corners"][2]
        assert peak[1] * lee > 0.5 and clew[1] * lee > 0.5, name
        assert throat[1] * lee < peak[1] * lee, name
        # cut at the mast: the part abaft it, the larger, lies to leeward
        pieces = dict(g["pieces"])
        assert set(pieces) == {"forward", "abaft"}, name
        assert pieces["abaft"][1] * lee > 0.0, name
        # the lug topsail lies with it, its clew at the lower lug's peak
        ts = g["topsail"]
        assert ts is not None and ts[2][1] * lee > 0.0, name
        assert ts[2] == pytest.approx(peak, abs=1e-6), name


@needs_node
def test_a_lug_running_is_an_offset_square_two_thirds_to_one_side(tmp_path):
    got = run_js(tmp_path, lugger_by_the_wind("starboard", sheet_deg=85.0), LUG_FIGURES)
    throat, peak = got["main"]["throat"], got["main"]["peak"]
    # nearly square across the ship, two thirds of the yard to leeward of the mast
    assert peak[1] < 0.0 < throat[1]
    assert abs(peak[1]) == pytest.approx(2.0 * abs(throat[1]), rel=0.25)


@needs_node
def test_a_lowered_lug_lies_on_deck_and_a_sent_down_topsail_is_not_drawn(tmp_path):
    data = lugger_by_the_wind("starboard", topsails=False)
    for s in data["snap"]["sails"]:
        if s["id"] == "main.lug":
            s["state"] = "in_the_gear"
    got = run_js(
        tmp_path,
        data,
        """
        const sk = P.buildSkeleton(d.graph, d.snap);
        const ids = sk.figures.filter(f => f.kind === 'sail').map(f => f.id);
        const ty = sk.figures.filter(f => f.id === 'main.topsail.lug_yard')[0];
        return {ids: ids, yard: sk.spars['main.lug_yard'].a, ty: ty.pts[0], tys: ty.state};
        """,
    )
    deck = data["graph"]["hull"]["deck_height_m"]
    assert "main.lug" in got["ids"] and "main.topsail" not in got["ids"]
    assert got["yard"][2] < deck + 1.0  # the lug lowered on deck with its yard
    assert got["ty"][2] < deck + 1.0 and got["tys"] == "sent_down_flying"


FIGURE_ORDER = """
    const sk = P.buildSkeleton(d.graph, d.snap);
    const out = {};
    [[0, 'ahead'], [Math.PI, 'astern']].forEach(([f, k]) => {
      out[k] = P.project(sk, f, 0).figures.map(x => x.id + (x.piece ? ':' + x.piece : ''));
    });
    return out;
"""


@needs_node
@pytest.mark.parametrize("path", [FRIGATE, BRIG])
def test_from_ahead_the_sail_hides_its_mast_and_from_astern_the_mast_hides_the_sail(tmp_path, path):
    ship = make_ship(path)
    for sid in ship.groups["plain sail"]:
        ship.sails[sid].state = SailState.SET
    got = run_js(tmp_path, ship_state(ship), FIGURE_ORDER)
    ahead, astern = got["ahead"], got["astern"]
    for sail, mast in (
        ("main.topsail", "main.topmast"),
        ("main.course", "main.mast"),
        ("fore.topgallant", "fore.topgallant_mast"),
        ("fore.topsail", "fore.topmast"),
    ):
        # painted later is nearer: from ahead the sail, from astern the mast
        assert ahead.index(sail) > ahead.index(mast), (sail, "ahead")
        assert astern.index(mast) > astern.index(sail), (sail, "astern")


@needs_node
def test_from_ahead_a_lugs_fore_third_hides_its_mast_and_from_astern_the_mast_the_rest(
    tmp_path,
):
    got = run_js(tmp_path, lugger_by_the_wind("starboard"), FIGURE_ORDER)
    ahead, astern = got["ahead"], got["astern"]
    assert ahead.index("main.lug:forward") > ahead.index("main.mast")
    assert ahead.index("main.mast") > ahead.index("main.lug:abaft")
    assert astern.index("main.lug:abaft") > astern.index("main.mast")
    assert astern.index("main.mast") > astern.index("main.lug:forward")


@needs_node
@pytest.mark.parametrize("brace_deg", [0.0, 30.0, 60.0])
def test_the_yards_brace_is_shown_from_the_beam(tmp_path, brace_deg):
    """The lead's finding of 18:29: a yard braced sharp up shows its breadth from the beam,
    a square yard is seen end on; the drawing is the yard's brace, foreshortened."""
    ship = make_ship(FRIGATE)
    yard = ship.spars["main.topsail.yard"]
    yard.brace_angle = math.radians(brace_deg)
    got = run_js(
        tmp_path,
        ship_state(ship),
        """
        const sk = P.buildSkeleton(d.graph, d.snap);
        const sc = P.project(sk, Math.PI / 2, 0);
        const y = sc.figures.filter(f => f.id === 'main.topsail.yard')[0];
        return Math.abs(y.pts[1].x - y.pts[0].x);
        """,
    )
    assert got == pytest.approx(yard.length_m * math.sin(math.radians(brace_deg)), abs=0.05)


@needs_node
def test_a_royal_sent_down_is_not_drawn_and_its_yard_lies_on_deck(tmp_path):
    ship = make_ship(FRIGATE)
    for sid in ship.groups["plain sail"]:
        ship.sails[sid].state = SailState.SET
    assert ship.sails["main.royal"].sent_down  # set flying: on deck until swayed up
    got = run_js(
        tmp_path,
        ship_state(ship),
        """
        const sk = P.buildSkeleton(d.graph, d.snap);
        const ids = sk.figures.filter(f => f.kind === 'sail').map(f => f.id);
        const y = sk.figures.filter(f => f.id === 'main.royal.yard')[0];
        const braces = sk.figures.filter(f => f.kind === 'line' && f.of === 'main.royal.yard');
        return {ids: ids, z: y.pts[0][2], dz: y.pts[1][2] - y.pts[0][2], braces: braces.length};
        """,
    )
    assert "main.royal" not in got["ids"] and "main.topgallant" in got["ids"]
    assert got["z"] < 3.0 and abs(got["dz"]) < 1e-6  # on deck, fore and aft
    assert got["braces"] == 0


@needs_node
def test_steels_staysails_are_drawn_from_their_cut(tmp_path):
    ship = make_ship(FRIGATE)
    for sid in ("main.topmast_staysail", "main.staysail", "mizzen.staysail"):
        ship.sails[sid].state = SailState.SET
    graph = {s["id"]: s for s in queries.ship_graph(ship)["sails"]}
    assert len(graph["main.topmast_staysail"]["corners_m"]) == 4  # Steel: quadrilateral
    assert len(graph["mizzen.staysail"]["corners_m"]) == 4
    assert len(graph["main.staysail"]["corners_m"]) == 3  # Steel: triangular
    got = run_js(
        tmp_path,
        ship_state(ship),
        """
        const sk = P.buildSkeleton(d.graph, d.snap);
        const out = {};
        sk.figures.filter(f => f.kind === 'sail').forEach(f => {
          (out[f.id] = out[f.id] || []).push(f.path.length);
        });
        return out;
        """,
    )
    # the four-sided sail's outline has a side more than the triangle's (whole or cut at a
    # mast, its pieces flattened)
    assert sum(got["main.topmast_staysail"]) >= 5
    assert got["mizzen.staysail"] and got["main.staysail"]


# ---------------------------------------------------------------------------
# Package 75 (B5.1, docs/design/Build-Ships.md §6): the hull drawn from her profile
# ---------------------------------------------------------------------------


def graph_of(path: str) -> dict:
    return queries.ship_graph(make_ship(path))


# A hull with a profile is drawn on the stations the server serves (B5.6: "served"), or, where
# a graph serves none, on B5.1's stations worked from the profile alone ("profile")
BUILDERS = ["served", "profile"]


def hull_of(path: str, builder: str = "served") -> dict:
    hull = graph_of(path)["hull"]
    if builder == "profile":
        del hull["stations"]
    return hull


# Each builder's stations as {x, pts: [[z, hb], ...]}, low to high: B5.1's, at one x each; B5.6's
# cut at the drawn depth, the stern's and the stem's closures with them, each point [z, hb, x]
# (a closure's x follows its line up).
STATIONS = """
    function stationsOf(hull) {
      if (!hull.stations) return P.profileHull(hull.profile).stations;
      const H = P.formHull(hull);
      return [H.aft].concat(H.mid, [H.fore])
        .map(s => ({x: s.x, pts: s.pts.map(p => [p[1], p[2], p[0]])}));
    }
"""


def todays_lens(hull: dict) -> list[dict]:
    """The hull as the viewer drew every hull before package 75 (`hullFigures`' lens), worked
    here from the same figures, so that a graph with no profile is drawn as it was."""
    length, beam = hull["length_waterline_m"], hull["beam_m"]
    freeboard = hull["deck_height_m"] or 1.5
    stern_x, bow_x = -length / 2 - 0.02 * length, length / 2 + 0.06 * length
    n = 14
    stbd, larb, stbd_low, larb_low = [], [], [], []
    for i in range(n + 1):
        t = -1 + 2 * i / n
        x = stern_x + (t + 1) / 2 * (bow_x - stern_x)
        half = 0.0 if i == n else beam / 2 * (1 - abs(t) ** 2.2) ** 0.55
        if i == 0:
            half = beam * 0.28
        z = freeboard * (1 + 0.12 * t * t + 0.1 * t)
        stbd.append([x, half, z])
        larb.append([x, -half, z])
        stbd_low.append([x, half * 0.92, -0.8])
        larb_low.append([x, -half * 0.92, -0.8])
    return [
        {"part": "deck", "pts": stbd + larb[::-1]},
        {"part": "side", "side": "starboard", "pts": stbd + stbd_low[::-1]},
        {"part": "side", "side": "larboard", "pts": larb + larb_low[::-1]},
        {"part": "transom", "pts": [stbd[0], larb[0], larb_low[0], stbd_low[0]]},
    ]


def inside_or_on(pt, poly, tol=1e-3) -> bool:
    """Whether (x, z) lies inside a closed polygon of (x, z) points, or within `tol` of it."""
    x, z = pt
    inside = False
    for i in range(len(poly)):
        (x0, z0), (x1, z1) = poly[i - 1], poly[i]
        if (z0 > z) != (z1 > z) and x < x0 + (x1 - x0) * (z - z0) / (z1 - z0):
            inside = not inside
        dx, dz = x1 - x0, z1 - z0
        length2 = dx * dx + dz * dz
        t = 0.0 if length2 == 0 else max(0.0, min(1.0, ((x - x0) * dx + (z - z0) * dz) / length2))
        if math.hypot(x - (x0 + t * dx), z - (z0 + t * dz)) <= tol:
            return True
    return inside


@needs_node
@pytest.mark.parametrize("builder", BUILDERS)
@pytest.mark.parametrize("path", PROFILED)
def test_the_sides_top_runs_through_every_rail_point_and_the_head_rule(tmp_path, path, builder):
    """The top of the drawn side passes through every point of `rail_m` within a millimetre;
    forward of the rail's end it runs straight to the stem head (the head rule), and the stem
    head is the side's foremost point. Each station's top is a corner of the side's strips."""
    hull = hull_of(path, builder)
    profile = hull["profile"]
    got = run_js(
        tmp_path,
        {"hull": hull},
        """
        const tops = d.hull.stations
          ? P.formHull(d.hull).stations.map(s => [s.top[0], s.top[1]])
          : P.profileHull(d.hull.profile).stations.map(s => [s.x, s.pts[s.pts.length - 1][0]]);
        const corners = new Set();
        P.hullFigures(d.hull).filter(f => f.part === 'side').forEach(f => f.pts.forEach(p => {
          corners.add(p[0].toFixed(6) + ',' + p[2].toFixed(6));
        }));
        return tops.map(t => [t[0], t[1], corners.has(t[0].toFixed(6) + ',' + t[1].toFixed(6))]);
        """,
    )
    assert all(on for _x, _z, on in got)
    for x, z in profile["rail_m"]:
        assert [t for t in got if abs(t[0] - x) < 1e-6 and abs(t[1] - z) <= 0.001], x
    (rx, rz), (hx, hz) = profile["rail_m"][-1], profile["stem_m"][-1]
    assert hx > rx  # her rail ends abaft the stem head, at the beakhead bulkhead
    for x, z, _on in got:
        if x > rx:
            assert z == pytest.approx(rz + (hz - rz) * (x - rx) / (hx - rx), abs=0.001), x
        elif x >= profile["rail_m"][0][0]:
            assert z == pytest.approx(interp(profile["rail_m"], x), abs=0.001), x
    assert max(x for x, _z, _on in got) == pytest.approx(hx, abs=1e-6)


@needs_node
@pytest.mark.parametrize("builder", BUILDERS)
@pytest.mark.parametrize("path", PROFILED)
def test_the_transom_runs_from_the_knuckle_to_the_taffrail(tmp_path, path, builder):
    hull = hull_of(path, builder)
    profile = hull["profile"]
    got = run_js(
        tmp_path,
        {"hull": hull},
        "return P.hullFigures(d.hull).filter(f => f.part === 'transom').map(f => f.pts);",
    )
    pts = [p for face in got for p in face]
    top = max(pts, key=lambda p: p[2])
    taffrail = profile["rail_m"][0]
    assert top[0] == pytest.approx(taffrail[0], abs=0.001)
    assert top[2] == pytest.approx(taffrail[1], abs=0.001)
    knuckle = profile["form"]["stern"]["knuckle_z_m"]
    assert min(p[2] for p in pts) == pytest.approx(knuckle, abs=0.001)
    # across the stern, alike on both sides
    widest = max(p[1] for p in pts)
    assert widest > 1.0 and min(p[1] for p in pts) == pytest.approx(-widest, abs=1e-9)


@needs_node
@pytest.mark.parametrize("builder", BUILDERS)
@pytest.mark.parametrize("path", PROFILED)
def test_each_deck_is_drawn_at_its_points_over_its_extent(tmp_path, path, builder):
    """Each deck at its own heights over its extent: on B5.1's stations inside the rail, at
    0.95 of its half-breadth or less; on the served ones (B5.6, §6) at 0.95 of the drawn side's
    half-breadth at the deck's height (freesail/ship/form.py's, within 5 mm: the stations are
    served to the millimetre)."""
    hull = hull_of(path, builder)
    profile = hull["profile"]
    spec = make_ship(path).hull.spec
    rail_hb = [(p[0], p[2]) for p in profile["breadth_m"]]
    got = run_js(
        tmp_path,
        {"hull": hull},
        "return P.hullFigures(d.hull).filter(f => f.part === 'deck').map(f => [f.deck, f.pts]);",
    )
    assert {word for word, _pts in got} == set(profile["decks_m"])
    for word, pts in got:
        line = profile["decks_m"][word]
        for x, y, z in pts:
            assert line[0][0] - 1e-6 <= x <= line[-1][0] + 1e-6, (word, x)
            assert z == pytest.approx(interp(line, x), abs=0.001), (word, x)
            if builder == "profile":
                assert abs(y) <= 0.95 * interp(rail_hb, x) + 0.001, (word, x)  # inside the rail
            else:
                side = form.half_breadth_at(spec, x, z)
                assert abs(y) == pytest.approx(0.95 * side, abs=0.005), (word, x, z)
    for word, line in profile["decks_m"].items():
        xs = [p[0] for w, pts in got if w == word for p in pts]
        assert min(xs) == pytest.approx(line[0][0], abs=0.001)
        assert max(xs) == pytest.approx(line[-1][0], abs=0.001)


# each spar's two ends, a lower mast drawn in two pieces (its foot and the rest, B5.6) as one
SPARS_DRAWN = """
    const sk = P.buildSkeleton(d.graph, null);
    const out = {};
    sk.figures.filter(f => f.kind === 'spar').forEach(f => {
      out[f.id] = out[f.id] ? [out[f.id][0], f.pts[1]] : f.pts;
    });
    return out;
"""


@needs_node
@pytest.mark.parametrize("path", PROFILED)
def test_a_lower_masts_foot_stands_on_the_drawn_deck_and_its_head_where_it_was(tmp_path, path):
    """The foot on the uppermost deck where the mast's rake line meets it (the 64's main mast
    on her quarterdeck, her fore on her forecastle), the head where the file's height puts it."""
    ship = make_ship(path)
    graph = queries.ship_graph(ship)
    deck = graph["hull"]["deck_height_m"]
    got = run_js(tmp_path, {"graph": graph}, SPARS_DRAWN)
    masts = [s for s in graph["spars"] if s["class"] == "mast"]
    assert len(masts) == 3
    for mast in masts:
        slope = -math.tan(mast["rake"])
        foot, head = got[mast["id"]]
        top = deck + mast["height_m"]
        assert head == pytest.approx([mast["x_m"] + slope * mast["height_m"], 0.0, top])
        assert foot[2] == pytest.approx(deck_at(ship.hull.spec.profile, foot[0]), abs=0.001)
        assert foot[0] == pytest.approx(mast["x_m"] + slope * (foot[2] - deck), abs=1e-6)
        assert foot[1] == 0.0
    if path == SIXTY_FOUR:
        assert got["main.mast"][0][2] == pytest.approx(5.27, abs=0.01)  # her quarterdeck
        assert got["fore.mast"][0][2] == pytest.approx(5.26, abs=0.01)  # her forecastle


@needs_node
@pytest.mark.parametrize("path", PROFILED)
def test_the_bowsprits_heel_is_at_the_stem_head_and_its_tip_where_it_was(tmp_path, path):
    """Indf §12.3: the heel at the stem head, or the rail there if that is lower (the razee's);
    the tip at the file's height above the datum, as before."""
    graph = graph_of(path)
    profile = graph["hull"]["profile"]
    deck = graph["hull"]["deck_height_m"]
    got = run_js(tmp_path, {"graph": graph}, SPARS_DRAWN)
    (bowsprit,) = [s for s in graph["spars"] if s["class"] == "bowsprit"]
    heel, tip = got["bowsprit"]
    hx, hz = profile["stem_m"][-1]
    assert heel == pytest.approx([hx, 0.0, min(hz, interp(profile["rail_m"], hx))], abs=0.001)
    length, height = bowsprit["length_m"], bowsprit["height_m"]
    rise = min(height, 0.95 * length)
    reach = math.sqrt(length * length - rise * rise)
    assert tip == pytest.approx([bowsprit["x_m"] + reach, 0.0, deck + rise], abs=1e-9)
    if path == RAZEE:
        assert heel[2] < hz  # her rail at the stem head stands below the stem head


WITHOUT_PROFILE = [p for p in EVERY_SHIP if p not in PROFILED] + ["the 64 without her profile"]


@needs_node
@pytest.mark.parametrize("path", WITHOUT_PROFILE)
def test_a_graph_with_no_profile_is_drawn_as_before_point_for_point(tmp_path, path):
    """The eight files carry no profile yet (Build-Ships.md §2.6): their hulls, masts' feet and
    bowsprits are drawn as they were, and so is the 64 with her profile taken away."""
    graph = graph_of(SIXTY_FOUR if path.startswith("the 64") else path)
    graph["hull"].pop("profile", None)
    graph["hull"].pop("stations", None)
    got = run_js(
        tmp_path,
        {"graph": graph},
        """
        const sk = P.buildSkeleton(d.graph, null);
        const spars = {};
        Object.keys(sk.spars).forEach(id => { spars[id] = [sk.spars[id].a, sk.spars[id].b]; });
        return {hull: P.hullFigures(d.graph.hull), spars: spars,
                inSkeleton: sk.figures.filter(f => f.kind === 'hull').length};
        """,
    )
    want = todays_lens(graph["hull"])
    assert len(got["hull"]) == len(want) == got["inSkeleton"]
    for drawn, then in zip(got["hull"], want, strict=True):
        assert drawn.get("part") == then["part"] and drawn.get("side") == then.get("side")
        assert len(drawn["pts"]) == len(then["pts"])
        for p, q in zip(drawn["pts"], then["pts"], strict=True):
            assert p == pytest.approx(q, abs=1e-9)
    deck = graph["hull"]["deck_height_m"]
    for spar in graph["spars"]:
        if spar["class"] in ("mast", "bowsprit"):
            assert got["spars"][spar["id"]][0] == pytest.approx([spar["x_m"], 0.0, deck])


NO_HOLLOW = (
    STATIONS
    + """
    const figs = P.hullFigures(d.hull).filter(f => f.part !== 'outline');
    function winding(pt, poly) {
      let w = 0;
      for (let i = 0; i < poly.length; i++) {
        const a = poly[i], b = poly[(i + 1) % poly.length];
        const cross = (b.x - a.x) * (pt.y - a.y) - (pt.x - a.x) * (b.y - a.y);
        if (a.y <= pt.y) { if (b.y > pt.y && cross > 0) w++; }
        else if (b.y <= pt.y && cross < 0) w--;
      }
      return w;
    }
    function nearEdge(pt, poly, tol) {
      for (let i = 0; i < poly.length; i++) {
        const a = poly[i], b = poly[(i + 1) % poly.length];
        const dx = b.x - a.x, dy = b.y - a.y, l2 = dx * dx + dy * dy;
        const t = l2 ? Math.max(0, Math.min(1, ((pt.x - a.x) * dx + (pt.y - a.y) * dy) / l2)) : 0;
        if (Math.hypot(pt.x - a.x - t * dx, pt.y - a.y - t * dy) <= tol) return true;
      }
      return false;
    }
    // a station's half-breadth and x at height z (a closure's x moves up its line)
    function atZ(s, z) {
      const pts = s.pts;
      let hb = pts[0][1], x = pts[0].length > 2 ? pts[0][2] : s.x;
      for (let i = 1; i < pts.length; i++) {
        const p = pts[i - 1], q = pts[i];
        if (z >= p[0] && z <= q[0]) {
          const t = q[0] > p[0] ? (z - p[0]) / (q[0] - p[0]) : 1;
          hb = p[1] + (q[1] - p[1]) * t;
          if (p.length > 2) x = p[2] + (q[2] - p[2]) * t;
        }
      }
      return [hb, x];
    }
    // the ends, closed: seen ahead, a station forward of the rail's end is hidden by figures
    // at or forward of it (the stem, the head rule's face); seen astern, a station abaft the
    // post at the water by figures at or abaft it (the counter, the transom)
    const prof = d.hull.profile;
    const railEnd = prof.rail_m[prof.rail_m.length - 1][0];
    let post = -Infinity;
    for (let i = 1; i < prof.stern_m.length; i++) {
      const p = prof.stern_m[i - 1], q = prof.stern_m[i];
      if (p[1] <= 0 && q[1] >= 0) post = p[0] + (q[0] - p[0]) * (0 - p[1]) / (q[1] - p[1]);
    }
    const out = {};
    [0, Math.PI].forEach(facing => {
      const proj = P.makeProjector(facing, 0);
      const polys = figs.map(f => f.pts.map(proj));
      const along = figs.map(f => {
        const fx = f.pts.map(p => p[0]);
        return [Math.min(...fx), Math.max(...fx)];
      });
      const boxes = polys.map(pl => {
        const xs = pl.map(p => p.x), ys = pl.map(p => p.y);
        return [Math.min(...xs) - 0.01, Math.max(...xs) + 0.01,
                Math.min(...ys) - 0.01, Math.max(...ys) + 0.01];
      });
      let samples = 0, ends = 0;
      const hollow = [], open = [];
      stationsOf(d.hull).forEach(s => {
        const z0 = s.pts[0][0], z1 = s.pts[s.pts.length - 1][0];
        if (z1 - z0 < 1e-6) return;
        for (let i = 1; i < 10; i++) {
          const z = z0 + (z1 - z0) * i / 10;
          const [hb, x] = atZ(s, z);
          const end = facing === 0 ? x >= railEnd - 1e-6 : x <= post + 1e-6;
          const before = k => (facing === 0 ? along[k][1] >= x - 1e-6 : along[k][0] <= x + 1e-6);
          for (let j = -9; j <= 9; j++) {
            const pt = proj([x, hb * j / 10, z]);
            const hit = k => {
              const b = boxes[k];
              if (pt.x < b[0] || pt.x > b[1] || pt.y < b[2] || pt.y > b[3]) return false;
              return winding(pt, polys[k]) !== 0 || nearEdge(pt, polys[k], 0.005);
            };
            samples++;
            if (!polys.some((pl, k) => hit(k))) hollow.push([x, hb * j / 10, z]);
            if (!end) continue;
            ends++;
            if (!polys.some((pl, k) => before(k) && hit(k))) open.push([x, hb * j / 10, z]);
          }
        }
      });
      let widest = 0;
      polys.forEach(pl => pl.forEach(p => { widest = Math.max(widest, Math.abs(p.x)); }));
      out[facing === 0 ? 'ahead' : 'astern'] = {
        samples: samples, hollow: hollow.slice(0, 5), n: hollow.length, widest: widest,
        ends: ends, open: open.slice(0, 5), nOpen: open.length};
    });
    return out;
"""
)


@needs_node
@pytest.mark.parametrize("builder", BUILDERS)
@pytest.mark.parametrize("path", PROFILED)
def test_ahead_and_astern_no_station_is_hollow_and_the_widest_is_her_greatest_half_breadth(
    tmp_path, path, builder
):
    """Seen dead ahead and dead astern, every station's section lies inside the hull's figures
    (one polygon a side left the hull hollow there: Build-Ships.md §6), and the drawn hull is
    as wide as her greatest half-breadth within a centimetre: `breadth_m`'s on B5.1's stations,
    the served stations' on B5.6's. At the ends the hull is closed by what stands before the
    station: seen ahead, the stem and the head rule's face across the bow; seen astern, the
    counter closing in to the post under the transom."""
    hull = hull_of(path, builder)
    if builder == "profile":
        greatest = max(max(p[1], p[2]) for p in hull["profile"]["breadth_m"])
    else:
        greatest = max(p[2] for station in hull["stations"] for p in station)
    got = run_js(tmp_path, {"hull": hull}, NO_HOLLOW)
    for view, seen in got.items():
        assert seen["samples"] > 1000 and seen["ends"] > 100, view
        assert seen["n"] == 0, (view, seen["hollow"])
        assert seen["nOpen"] == 0, (view, seen["open"])
        assert seen["widest"] == pytest.approx(greatest, abs=0.01), view


@needs_node
@pytest.mark.parametrize("builder", BUILDERS)
@pytest.mark.parametrize("path", PROFILED)
def test_no_side_figure_stands_forward_of_the_head_rule_above_the_water(tmp_path, path, builder):
    """Above the water every point of the side lies within her profile: the rail, the head rule
    to the stem head, the stem down to the water, and the stern's line up to the taffrail; so
    the bow never rakes aft of the stem, nor runs forward of the head rule."""
    hull = hull_of(path, builder)
    profile = hull["profile"]
    rail, stem, stern = profile["rail_m"], profile["stem_m"], profile["stern_m"]

    def x_at_water(line):
        for (x0, z0), (x1, z1) in zip(line, line[1:], strict=False):
            if z0 <= 0.0 <= z1:
                return x0 + (x1 - x0) * (0.0 - z0) / (z1 - z0)
        raise AssertionError("the line does not cross the water")

    region = [tuple(p) for p in rail]
    if stem[-1][0] > rail[-1][0]:
        region.append(tuple(stem[-1]))
    region += [tuple(p) for p in reversed(stem[:-1]) if p[1] > 0.0]
    region += [(x_at_water(stem), 0.0), (x_at_water(stern), 0.0)]
    region += [tuple(p) for p in stern if p[1] > 0.0]
    got = run_js(
        tmp_path,
        {"hull": hull},
        "return P.hullFigures(d.hull).filter(f => f.part === 'side').map(f => f.pts);",
    )
    above = [(p[0], p[2]) for pts in got for p in pts if p[2] > 1e-6]
    assert above
    assert [p for p in above if not inside_or_on(p, region)] == []
    assert max(x for x, _z in above) == pytest.approx(stem[-1][0], abs=1e-6)


CLOSED = """
    const figs = P.hullFigures(d.hull);
    let finite = true;
    figs.forEach(f => f.pts.forEach(p => p.forEach(c => {
      if (!Number.isFinite(c)) finite = false;
    })));
    const fewest = Math.min(...figs.filter(f => f.part !== 'outline').map(f => f.pts.length));
    const loops = {};
    ['starboard', 'larboard'].forEach(side => {
      const key = p => p.map(c => c.toFixed(6)).join(',');
      const near = {};
      figs.filter(f => f.part === 'outline' && f.side === side).forEach(f => {
        for (let i = 1; i < f.pts.length; i++) {
          const a = key(f.pts[i - 1]), b = key(f.pts[i]);
          if (a === b) continue;
          (near[a] = near[a] || []).push(b);
          (near[b] = near[b] || []).push(a);
        }
      });
      const keys = Object.keys(near);
      const seen = new Set(keys.slice(0, 1));
      const todo = keys.slice(0, 1);
      while (todo.length) {
        near[todo.pop()].forEach(n => { if (!seen.has(n)) { seen.add(n); todo.push(n); } });
      }
      loops[side] = {vertices: keys.length, reached: seen.size,
                     odd: keys.filter(k => near[k].length !== 2).length};
    });
    return {n: figs.length, finite: finite, fewest: fewest, loops: loops,
            parts: Array.from(new Set(figs.map(f => f.part))).sort()};
"""


@needs_node
@pytest.mark.parametrize(
    ("path", "builder"),
    [(p, "served") for p in EVERY_SHIP] + [(p, "profile") for p in PROFILED],
)
def test_every_file_draws_a_closed_hull_with_no_nan(tmp_path, path, builder):
    """Every file's hull: no coordinate that is not a number, every filled figure a polygon,
    and where the file gives a profile each side's outline one closed line, the rail along the
    top, the stem, the low edge and the stern; on the served stations (B5.6) with her
    galleries, her stern lights and her head."""
    hull = graph_of(path)["hull"]
    if builder == "profile":
        del hull["stations"]
    got = run_js(tmp_path, {"hull": hull}, CLOSED)
    assert got["finite"] and got["fewest"] >= 3
    if "profile" not in hull:
        assert got["n"] == 4 and got["parts"] == ["deck", "side", "transom"]
        return
    assert set(got["parts"]) >= {"side", "outline", "deck", "transom", "wale", "bottom"}
    if builder == "served":
        assert set(got["parts"]) >= {"gallery", "light", "head"}
    for side, loop in got["loops"].items():
        assert loop["vertices"] > 20, side
        assert loop["odd"] == 0 and loop["reached"] == loop["vertices"], (side, loop)


@needs_node
def test_a_hand_written_profile_of_rail_and_breadth_alone_is_drawn_closed(tmp_path):
    """A profile need give only `rail_m` and `breadth_m` (Build-Ships.md §5.2): with no stem, no
    stern and no section, the side is today's three points a station, closed aft by a transom
    and forward by the bow's face, its outline one closed line each side."""
    hull = {
        "length_waterline_m": 20.0,
        "beam_m": 6.0,
        "deck_height_m": 1.2,
        "profile": {
            "rail_m": [[-10.0, 2.0], [10.0, 2.5]],
            "breadth_m": [[-8.0, 2.0, 2.0], [0.0, 3.0, 2.8], [8.0, 2.0, 2.2]],
        },
    }
    got = run_js(tmp_path, {"hull": hull}, CLOSED)
    assert got["finite"] and got["fewest"] >= 3
    assert got["parts"] == ["bottom", "bulkhead", "outline", "side", "transom"]
    for side, loop in got["loops"].items():
        assert loop["odd"] == 0 and loop["reached"] == loop["vertices"] > 20, (side, loop)
    cut = run_js(
        tmp_path,
        {"hull": hull},
        """
        const s = P.profileHull(d.hull.profile).stations.find(st => st.x === 0);
        return s.pts;
        """,
    )
    # today's cut at 0.92 of the water's half-breadth, the water, and the rail
    assert cut == [pytest.approx(p) for p in ([-0.8, 0.92 * 3.0], [0.0, 3.0], [2.25, 2.8])]


@needs_node
def test_the_lifts_of_every_yard_run_from_its_arms_to_the_masthead_above(tmp_path):
    """The owner's answer (Build-Ships.md §19.1 item 7; §6): each lift the file carries drawn
    faint, a line as the braces are, from its yard's arm on its side up to the head of the mast
    the yard hangs on; a yard sent down on deck has none drawn."""
    ship = make_ship(FRIGATE)
    for sid in ship.groups["plain sail"]:
        ship.sails[sid].state = SailState.SET
    data = ship_state(ship)
    got = run_js(
        tmp_path,
        data,
        """
        const sk = P.buildSkeleton(d.graph, d.snap);
        const drawn = sk.figures.filter(f => f.kind === 'spar' && !(sk.spars[f.id] || {}).onDeck)
            .map(f => f.id);
        const lifts = sk.figures.filter(f => f.kind === 'line' && f.cls === 'lift').map(f => {
          const y = sk.spars[f.of];
          return {id: f.id, pts: f.pts, a: y.a, b: y.b, head: y.parent.head};
        });
        return {drawn: drawn, lifts: lifts};
        """,
    )
    lines = {ln["id"]: ln for ln in data["graph"]["lines"] if ln["class"] == "lift"}
    yards = {s["id"] for s in data["graph"]["spars"] if s["class"] == "yard"}
    drawn = set(got["drawn"])
    should = {lid for lid, ln in lines.items() if ln["of"] in yards and ln["of"] in drawn}
    assert {lift["id"] for lift in got["lifts"]} == should
    assert len(should) >= 16  # the courses', the topsails' and the topgallants'
    for lift in got["lifts"]:
        arm = lift["b"] if lines[lift["id"]]["side"] == "starboard" else lift["a"]
        assert lift["pts"] == [pytest.approx(arm), pytest.approx(lift["head"])], lift["id"]


# ---------------------------------------------------------------------------
# Package 75 (B5.6, docs/design/Build-Ships.md §6 "The form's drawing"): the served stations
# ---------------------------------------------------------------------------

UNDERWATER_HEEL = math.radians(20.0)  # projection.js's UNDERWATER_HEEL_DEG


def drawn_floor(station: list) -> float:
    """§6: how deep a served station is drawn, D = max(0.8 m, its half-breadth at the water x
    tan 20 deg), no deeper than the hull (its own lowest point), as a height."""
    zs = [p[1] for p in station]
    water = interp([(p[1], p[2]) for p in station], 0.0) if zs[0] < 0.0 < zs[-1] else 0.0
    return max(-max(0.8, water * math.tan(UNDERWATER_HEEL)), zs[0])


def x_at_height(line: list, z: float) -> float:
    """Where a line of [x, z, ...] points, z rising (the stem's, the stern's, the knee's), stands
    at height z: its x, held beyond its ends."""
    return interp([(p[1], p[0]) for p in line], z)


def flat_pts(points: list) -> list[float]:
    """A figure's points as one list of numbers, for `pytest.approx`."""
    return [c for p in points for c in p]


@needs_node
@pytest.mark.parametrize("path", PROFILED)
def test_the_strips_lie_on_the_served_stations_within_a_millimetre(tmp_path, path):
    """Every corner of the side's strips is a point of a served station, or on one between two
    of its points where the drawn depth cuts it, within a millimetre; and every served point
    above the drawn depth is a corner of the strips on both sides."""
    hull = graph_of(path)["hull"]
    stations = hull["stations"]
    got = run_js(
        tmp_path,
        {"hull": hull},
        "return P.hullFigures(d.hull).filter(f => f.part === 'side').map(f => [f.side, f.pts]);",
    )
    corners = {"starboard": set(), "larboard": set()}
    raw = {"starboard": [], "larboard": []}
    for side, pts in got:
        corners[side] |= {(round(x, 3), round(y, 3) + 0.0, round(z, 3)) for x, y, z in pts}
        raw[side] += pts
    reach = [(min(p[0] for p in s) - 0.001, max(p[0] for p in s) + 0.001) for s in stations]

    def on_a_station(x, hb, z):
        for (lo, hi), s in zip(reach, stations, strict=True):
            if not lo <= x <= hi:
                continue
            for a, b in zip(s, s[1:], strict=False):
                if not min(a[1], b[1]) - 1e-6 <= z <= max(a[1], b[1]) + 1e-6:
                    continue
                if b[1] == a[1]:  # two points at one height (a transom's foot): either
                    near = [a, b]
                else:
                    t = (z - a[1]) / (b[1] - a[1])
                    near = [(a[0] + (b[0] - a[0]) * t, z, a[2] + (b[2] - a[2]) * t)]
                if any(abs(q[0] - x) <= 0.001 and abs(q[2] - hb) <= 0.001 for q in near):
                    return True
        return False

    for side, sign in (("starboard", 1), ("larboard", -1)):
        assert all(sign * c[1] >= 0.0 for c in raw[side]), side
        off = [c for c in raw[side] if not on_a_station(c[0], sign * c[1], c[2])]
        assert off == [], (side, off[:5])
        for s in stations:
            floor = drawn_floor(s)
            for x, z, hb in s:
                if z >= floor - 1e-9:
                    key = (round(x, 3), round(sign * hb, 3) + 0.0, round(z, 3))
                    assert key in corners[side], (side, [x, z, hb])


@needs_node
@pytest.mark.parametrize("path", PROFILED)
def test_the_transom_stands_at_the_taffrail_and_transom_hb_m_its_foot_rounded_up(tmp_path, path):
    """A square stern's transom (§6): its top across the taffrail (`stern_m`'s top) at
    `transom_hb_m`'s first, within a centimetre; its foot at its edges the knuckle
    (`knuckle_z_m`), where it stands at the stern's line's half-breadth (`transom_hb_m`'s
    second, straight to the first at the taffrail: form.py's closure), and from there rounded up
    `round_up_m` to the middle line, the middle the higher as a beam rounds up (the 64's wing
    transom on her body plan: 6 ft 9 in above WL1 at the middle line, 6 ft 4 1/2 in at its
    ends); the tuck under the arch closes the stern down to the knuckle; every point of it on the
    stern's line at its height."""
    hull = graph_of(path)["hull"]
    profile = hull["profile"]
    stern = profile["form"]["stern"]
    assert stern["type"] == "square"
    zk, (hb_top, hb_knuckle) = stern["knuckle_z_m"], stern["transom_hb_m"]
    rise = stern["round_up_m"]
    assert rise > 0.1  # 4 in
    xt, zt = profile["stern_m"][-1]
    got = run_js(
        tmp_path,
        {"hull": hull},
        """
        return P.hullFigures(d.hull).filter(f => f.part === 'transom')
          .map(f => [f.cls || '', f.pts]);
        """,
    )
    pts = [p for _cls, face in got for p in face]
    top = [p for p in pts if abs(p[2] - zt) < 1e-6]
    assert top and all(p[0] == pytest.approx(xt, abs=0.001) for p in top)
    assert min(p[1] for p in top) == pytest.approx(-hb_top, abs=0.01)
    assert max(p[1] for p in top) == pytest.approx(hb_top, abs=0.01)
    assert max(p[2] for p in pts) == pytest.approx(zt, abs=1e-6)
    # the knuckle at the edges, the widest of the face, on the stern's line's half-breadth there
    low = [p for p in pts if abs(p[2] - zk) < 1e-6]
    assert {p[1] > 0 for p in low} == {True, False}
    assert all(abs(p[1]) == pytest.approx(hb_knuckle, abs=0.001) for p in low)
    assert min(p[2] for p in pts) == pytest.approx(zk, abs=1e-6)
    assert max(abs(p[1]) for p in pts) == pytest.approx(hb_knuckle, abs=0.001)
    # the foot an arch, its crown the knuckle and the round-up at the middle line
    tucks = [face for cls, face in got if "tuck" in cls.split()]
    assert len(tucks) == 1
    (tuck,) = tucks
    crown = max(tuck, key=lambda p: p[2])
    assert crown[1] == pytest.approx(0.0, abs=1e-9) and crown[2] == pytest.approx(zk + rise)
    for _x, y, z in tuck:
        assert z == pytest.approx(zk + rise * (1.0 - (y / hb_knuckle) ** 2), abs=0.002), (y, z)
    lowest = [
        face
        for cls, face in got
        if "tuck" not in cls.split() and min(q[2] for q in face) < zk + 1e-6
    ]
    assert len(lowest) == 1  # the face's lowest strip stands on the arch
    assert [q for q in lowest[0] if q[2] < zk + rise - 1e-9] == [
        q for q in tuck if q[2] < zk + rise - 1e-9
    ]
    for x, _y, z in pts:
        assert x == pytest.approx(x_at_height(profile["stern_m"], z), abs=0.01), (x, z)


@needs_node
def test_a_round_stern_has_no_transom_and_its_lights_lie_on_its_drawn_face(tmp_path):
    """§6: a round stern has no transom; the strips close to the middle line (form.py's closure
    there), and each band of lights is spread within its half-breadth across the drawn face, each
    mark's corners on the drawn side within a centimetre. The 64's stern made round here."""
    ship = make_ship(SIXTY_FOUR)
    spec = ship.hull.spec
    p = spec.profile
    was = p.form.stern
    stern = HullStern(type="round", galleries_m=was.galleries_m, lights_m=was.lights_m)
    spec = replace(spec, profile=replace(p, form=replace(p.form, stern=stern)))
    ship.hull.spec = spec
    hull = queries.ship_graph(ship)["hull"]
    assert hull["profile"]["form"]["stern"]["type"] == "round"
    assert all(hb == 0.0 for _x, _z, hb in hull["stations"][0])
    got = run_js(
        tmp_path,
        {"hull": hull},
        """
        const figs = P.hullFigures(d.hull);
        return {parts: Array.from(new Set(figs.map(f => f.part))).sort(),
                lights: figs.filter(f => f.part === 'light').map(f => [f.band, f.pts])};
        """,
    )
    assert "transom" not in got["parts"]
    assert {"light", "gallery", "side"} <= set(got["parts"])
    for b, (zl, zh, n, hb) in enumerate(was.lights_m):
        marks = [pts for band, pts in got["lights"] if band == b]
        assert len(marks) == n, b
        for pts in marks:
            assert min(q[2] for q in pts) == pytest.approx(zl, abs=0.01)
            assert max(q[2] for q in pts) == pytest.approx(zh, abs=0.01)
            for x, y, z in pts:
                assert abs(y) <= hb + 1e-9
                side = form.half_breadth_at(spec, x, z)
                assert side == pytest.approx(abs(y), abs=0.01), (x, y, z)


@needs_node
@pytest.mark.parametrize("path", PROFILED)
def test_each_gallery_and_band_of_lights_lies_at_its_place(tmp_path, path):
    """§6, §5.0 principle 9: each tier of `galleries_m` a plain box on each quarter at its extent
    and heights within a centimetre, its inner edges on the drawn side where the side stands
    there and its outer face GALLERY_OUT_M beyond it; each band of `lights_m` n plain marks at its
    heights within a centimetre, in n even bays within its half-breadth, each the light's share
    of its bay, on the transom (the stern's line at its height). Nothing stands off the hull: a
    tier is cut to the top of the side over its extent and to the stern's line at its heights, a
    band to the transom's knuckle and taffrail. Both ships' are drawn as filed: the razee's stand
    under her taffrail since her short roundhouse is in her profile (Build-Ships.md §19.1 item
    18), where before it they were cut to her side and her transom."""
    hull = graph_of(path)["hull"]
    profile = hull["profile"]
    stern = profile["form"]["stern"]
    spec = make_ship(path).hull.spec
    rail, stern_line = profile["rail_m"], profile["stern_m"]
    taffrail = stern_line[-1][1]

    def top_over(x0, x1):
        """The top of the drawn side over [x0, x1]: through the rail's points, held abaft the
        taffrail (form.py's)."""
        xs = [x0, x1] + [x for x, _z in rail if x0 < x < x1]
        return min(interp(rail, x) for x in xs)

    tiers, cut = [], False
    for x0, x1, zl, zh in stern["galleries_m"]:
        z_top = min(zh, top_over(x0, x1))
        x_aft = max(x0, x_at_height(stern_line, zl), x_at_height(stern_line, z_top))
        cut = cut or (z_top, x_aft) != (zh, x0)
        tiers.append((x_aft, x1, zl, z_top))
    bands = []
    for zl, zh, n, hb in stern["lights_m"]:
        z_top = min(zh, taffrail)
        cut = cut or z_top != zh
        bands.append((max(zl, stern["knuckle_z_m"]), z_top, n, hb))
    assert not cut  # the razee's roundhouse in (B1, 2026-10-29): nothing cut on either file
    got = run_js(
        tmp_path,
        {"hull": hull},
        """
        const parts = {gallery: 1, light: 1};
        return {out: P.constants.GALLERY_OUT_M, share: P.constants.LIGHT_SHARE,
                figs: P.hullFigures(d.hull).filter(f => parts[f.part]).map(f =>
                  ({part: f.part, side: f.side, tier: f.tier, band: f.band, pts: f.pts}))};
        """,
    )
    figs = got["figs"]
    out, share = got["out"], got["share"]
    assert (out, share) == (0.75, 0.6)
    for t, (x0, x1, zl, zh) in enumerate(tiers):
        for side, sign in (("starboard", 1), ("larboard", -1)):
            faces = [
                f["pts"]
                for f in figs
                if f["part"] == "gallery" and f["tier"] == t and f["side"] == side
            ]
            assert len(faces) == 5, (t, side)
            box = [q for face in faces for q in face]
            assert min(q[0] for q in box) == pytest.approx(x0, abs=0.01)
            assert max(q[0] for q in box) == pytest.approx(x1, abs=0.01)
            assert min(q[2] for q in box) == pytest.approx(zl, abs=0.01)
            assert max(q[2] for q in box) == pytest.approx(zh, abs=0.01)
            assert all(sign * q[1] > 0.0 for q in box)
            outer = max(abs(q[1]) for q in box)
            for x in (x0, x1):
                for z in (zl, zh):
                    here = form.half_breadth_at(spec, x, z)
                    assert outer >= here + out - 0.01, (t, x, z)
                    if here > 0.0:
                        on = [
                            q
                            for q in box
                            if abs(q[0] - x) < 0.01
                            and abs(q[2] - z) < 0.01
                            and abs(abs(q[1]) - here) < 0.01
                        ]
                        assert on, (t, side, x, z)
    line = [(z, x) for x, z in profile["stern_m"]]
    for b, (zl, zh, n, hb) in enumerate(bands):
        marks = [f["pts"] for f in figs if f["part"] == "light" and f["band"] == b]
        assert len(marks) == n, b
        bay = 2.0 * hb / n
        middles = sorted(0.5 * (min(q[1] for q in m) + max(q[1] for q in m)) for m in marks)
        assert middles == [pytest.approx(-hb + bay * (i + 0.5), abs=0.01) for i in range(n)]
        for m in marks:
            across = max(q[1] for q in m) - min(q[1] for q in m)
            assert across == pytest.approx(share * bay, abs=0.01)
            assert min(q[2] for q in m) == pytest.approx(zl, abs=0.01)
            assert max(q[2] for q in m) == pytest.approx(zh, abs=0.01)
            for x, y, z in m:
                assert abs(y) <= hb + 1e-9
                assert x == pytest.approx(interp(line, z), abs=0.01), (b, x, z)


@needs_node
@pytest.mark.parametrize("path", PROFILED)
def test_the_head_lies_on_head_m(tmp_path, path):
    """§6: the knee of the head, HEAD_SIDING_M each side of the middle line (judgement, 0.2 m):
    each of its two sides `head_m`'s points within a millimetre from the drawn depth at the stem
    (0.8 m: the water's half-breadth there is nothing) up to the head's top, then back to the
    stem head and down `stem_m`, seen only from its own side; its fore edge in strips across it
    on `head_m` up to the figure's foot. At its top, the figure (`form.head`) a plain shape the
    head's share tall, its top the head's, its front on `head_m`: its two sides as broad apart as
    it is deep, and its face across the ship at its middle. Seen ahead or astern the head is a
    strip with the figure on it, not a hairline."""
    hull = graph_of(path)["hull"]
    profile = hull["profile"]
    knee, stem = profile["head_m"], profile["stem_m"]
    assert profile["form"]["head"] == "figure"
    got = run_js(
        tmp_path,
        {"hull": hull},
        """
        const heads = P.hullFigures(d.hull).filter(f => f.part === 'head');
        const sk = {figures: heads.map(f => Object.assign({kind: 'hull'}, f))};
        const seen = [0, Math.PI].map(facing => {
          const xs = P.project(sk, facing, 0).figures
            .reduce((a, f) => a.concat(f.pts.map(p => p.x)), []);
          return Math.max(...xs) - Math.min(...xs);
        });
        return {share: P.constants.FIGURE_SHARE, siding: P.constants.HEAD_SIDING_M, seen: seen,
                head: heads.map(f => ({cls: f.cls || 'knee', side: f.side || null,
                                       outward: f.outward || null, pts: f.pts}))};
        """,
    )
    s = got["siding"]
    assert s == 0.2
    floor = -0.8
    front = [(x_at_height(knee, floor), floor)] + [(x, z) for x, z in knee if z > floor]
    back = [(x, z) for x, z in reversed(stem) if z > floor] + [(x_at_height(stem, floor), floor)]
    top = knee[-1][1]
    tall = got["share"] * top
    foot = top - tall
    figure = [h for h in got["head"] if h["cls"] == "figure"]
    for side, sign in (("starboard", 1), ("larboard", -1)):
        (plate,) = [h for h in got["head"] if h["cls"] == "knee" and h["side"] == side]
        assert plate["outward"] == [0, sign, 0]
        assert len(plate["pts"]) == len(front) + len(back)
        for q, (x, z) in zip(plate["pts"], front + back, strict=True):
            assert q == pytest.approx([x, sign * s, z], abs=0.001)
        (shape,) = [h for h in figure if h["side"] == side]
        assert shape["outward"] == [0, sign, 0]
        assert max(q[2] for q in shape["pts"]) == pytest.approx(top, abs=0.001)
        assert min(q[2] for q in shape["pts"]) == pytest.approx(foot, abs=0.001)
        front_x = max(q[0] for q in shape["pts"])
        assert front_x == pytest.approx(x_at_height(knee, top - tall / 2), abs=0.001)
        depth = front_x - min(q[0] for q in shape["pts"])
        assert all(q[1] == pytest.approx(sign * depth / 2) for q in shape["pts"])
    (face,) = [h for h in figure if h["side"] is None]
    assert max(q[1] for q in face["pts"]) == pytest.approx(tall / 4, abs=0.001)  # half its depth
    middle = x_at_height(knee, top - tall / 2) - tall / 4
    assert all(q[0] == pytest.approx(middle, abs=0.001) for q in face["pts"])
    edge = [h["pts"] for h in got["head"] if h["cls"] == "strip"]
    on_knee = [(x, z) for x, z in front if z <= foot + 1e-9]
    if on_knee[-1][1] < foot - 1e-9:
        on_knee.append((x_at_height(knee, foot), foot))
    assert len(edge) == len(on_knee) - 1
    for strip, (p, q) in zip(edge, zip(on_knee, on_knee[1:], strict=False), strict=True):
        want = [[p[0], -s, p[1]], [q[0], -s, q[1]], [q[0], s, q[1]], [p[0], s, p[1]]]
        assert flat_pts(strip) == pytest.approx(flat_pts(want), abs=0.001)
    # seen ahead and astern: the knee's breadth at least, the figure's at the most
    for breadth in got["seen"]:
        assert 2 * s - 1e-6 <= breadth <= tall / 2 + 1e-6


@needs_node
@pytest.mark.parametrize("path", PROFILED)
def test_nothing_is_drawn_below_the_drawn_depth(tmp_path, path):
    """§6: each station drawn down to D(x) = max(0.8 m, its half-breadth at the water x tan 20
    deg), no deeper than the hull, and no point of any of the hull's figures below that,
    straight between the stations under the water and 0.8 m at the stern's and the stem's lines
    and beyond them (the head); so no cut edge comes out of the water heeled 19.5 degrees either
    way."""
    hull = graph_of(path)["hull"]
    stations = hull["stations"]
    aft, fore = stations[0], stations[-1]
    line = [(x_at_height(aft, -0.8), -0.8)]
    line += [(s[0][0], drawn_floor(s)) for s in stations[1:-1] if s[0][1] < 0.0]
    line += [(x_at_height(fore, -0.8), -0.8)]
    got = run_js(
        tmp_path,
        {"hull": hull},
        """
        const figs = P.hullFigures(d.hull);
        const sk = {figures: figs.map(f => Object.assign({kind: 'hull'}, f))};
        const heeled = [0.34, -0.34].map(h => P.project(sk, Math.PI / 2, h, {underwater: 'solid'})
          .figures.filter(f => f.part === 'bottom').map(f => Math.min(...f.pts.map(p => p.y))));
        return {lows: P.formHull(d.hull).mid.map(s => [s.x, s.low[1]]),
                pts: figs.map(f => [f.part, f.pts]), heeled: heeled};
        """,
    )
    floors = {s[0][0]: drawn_floor(s) for s in stations[1:-1]}
    for x, z in got["lows"]:
        assert z == pytest.approx(floors[x], abs=0.001), x
    deepest = max(
        0.8,
        max(interp([(p[1], p[2]) for p in s], 0.0) for s in stations[1:-1] if s[0][1] < 0.0)
        * math.tan(UNDERWATER_HEEL),
    )
    assert min(z for _x, z in line) == pytest.approx(-deepest, abs=0.001)
    widest = max(b[1] for b in hull["profile"]["breadth_m"])
    assert deepest == pytest.approx(widest * math.tan(UNDERWATER_HEEL), abs=0.005)  # 2.4 m
    below = [
        (part, q) for part, pts in got["pts"] for q in pts if q[2] < interp(line, q[0]) - 0.001
    ]
    assert below == []
    for bottoms in got["heeled"]:
        assert bottoms and min(bottoms) >= -1e-6  # the cut stays under the sea line


FOOT_SORTED = """
    const sk = P.buildSkeleton(d.graph, null);
    const hull = sk.figures.filter(f => f.kind === 'hull');
    const views = [['to leeward', Math.PI / 2, 0], ['heeled 10 toward', Math.PI / 2, 0.1745],
                   ['heeled 20 toward', Math.PI / 2, 0.349],
                   ['heeled 30 toward', Math.PI / 2, 0.5236],
                   ['heeled 10 from windward', 3 * Math.PI / 2, 0.1745],
                   ['on the quarter', 3 * Math.PI / 4, 0], ['on the bow', Math.PI / 4, 0.1745]];
    const out = [];
    sk.figures.filter(f => f.kind === 'spar' && f.piece === 'foot').forEach(foot => {
      const rest = sk.figures.find(f => f.kind === 'spar' && f.id === foot.id && f !== foot);
      const x = foot.pts[0][0];
      const reach = f => {
        const xs = f.pts.map(p => p[0]);
        return Math.min(...xs) <= x && x <= Math.max(...xs);
      };
      views.forEach(([name, facing, heel]) => {
        const proj = P.makeProjector(facing, heel);
        const depth = f => (f.sortAt ? proj(f.sortAt).depth
          : f.pts.reduce((s, p) => s + proj(p).depth, 0) / f.pts.length) + (f.sortBias || 0);
        const near = Math.sin(facing) > 0 ? 'starboard' : 'larboard';
        const far = near === 'starboard' ? 'larboard' : 'starboard';
        const strips = side => hull.filter(f => f.part === 'side' && f.side === side && reach(f))
          .map(depth);
        const decks = hull.filter(f => f.part === 'deck' && reach(f) &&
          f.pts.some(p => Math.abs(p[2] - foot.pts[0][2]) < 0.05)).map(depth);
        out.push({id: foot.id, view: name, foot: depth(foot), near: strips(near),
                  far: strips(far), decks: decks, top: foot.pts[1][2],
                  rest: [rest.pts[0], rest.sortAt, foot.pts[0], rest.pts[1]]});
      });
    });
    return out;
"""


@needs_node
@pytest.mark.parametrize("path", PROFILED)
def test_a_lower_masts_foot_is_sorted_behind_the_near_side(tmp_path, path):
    """§6: a lower mast's foot, from its deck up to the top of the side there, is drawn before
    (behind) the near side's strip at its x, and after the deck it stands on and the far side:
    abeam to leeward, heeled 10, 20 and 30 degrees toward the viewer, from windward heeled 10,
    on the quarter and on the bow. The rest of the mast is sorted at the whole mast's middle, as
    the mast was."""
    graph = graph_of(path)
    profile = graph["hull"]["profile"]
    got = run_js(tmp_path, {"graph": graph}, FOOT_SORTED)
    assert {g["id"] for g in got} == {"fore.mast", "main.mast", "mizzen.mast"}
    for g in got:
        where = (g["id"], g["view"])
        assert g["near"] and g["far"] and g["decks"], where
        assert max(g["near"]) < g["foot"] - 1e-3, where  # the near side painted over it
        assert min(g["far"]) > g["foot"] + 1e-3, where
        assert min(g["decks"]) > g["foot"] + 1e-3, where  # it stands on its deck
        cut, sort_at, foot, head = g["rest"]
        assert cut[2] == pytest.approx(g["top"])
        assert cut[2] == pytest.approx(interp(profile["rail_m"], foot[0]), abs=1e-6)
        assert sort_at == pytest.approx([(foot[i] + head[i]) / 2 for i in range(3)])


@needs_node
@pytest.mark.parametrize("path", PROFILED)
def test_the_head_and_the_galleries_stay_inside_the_fixed_frame_across_states(tmp_path, path):
    """The fixed frame (spec M3 §9 item 14) holds the hull as drawn: furled, under plain sail,
    and with the topgallant masts sent down, the bounds are the same in each view, and the head,
    the galleries and the lights stand inside them. (Braced to their limits, the 64's yards move
    the frame on the quarter at 135 degrees, in the viewer before package 75 too: the rig's, not
    the hull's.)"""
    ship = make_ship(path)
    furled = ship_state(ship)
    for sid in ship.groups["plain sail"]:
        ship.sails[sid].state = SailState.SET
    plain = ship_state(ship)
    for spar in ship.spars.values():
        if spar.cls == "topgallant_mast":
            spar.sent_down = True
    struck = ship_state(ship)
    got = run_js(
        tmp_path,
        {"states": [furled, plain, struck]},
        """
        const parts = {head: 1, gallery: 1, light: 1};
        return [0, Math.PI / 2, 3 * Math.PI / 4, Math.PI].map(facing => d.states.map(st => {
          const sc = P.project(P.buildSkeleton(st.graph, st.snap), facing, 0);
          const b = sc.bounds;
          const these = sc.figures.filter(f => parts[f.part]);
          const outside = these.filter(f => f.pts.some(p =>
            p.x < b.minX - 1e-9 || p.x > b.maxX + 1e-9 || p.y < b.minY - 1e-9));
          return {bounds: b, outside: outside.length, parts: these.length};
        }));
        """,
    )
    for view in got:
        first = view[0]["bounds"]
        for state in view:
            assert state["bounds"] == pytest.approx(first, abs=1e-9)
            assert state["outside"] == 0 and state["parts"] > 0


UNDER_THE_WATER = """
    const sk = P.buildSkeleton(d.graph, null);
    const out = {default: P.constants.UNDERWATER};
    [0, 0.17].forEach(heel => {
      [null, 'hidden', 'faint', 'solid'].forEach(way => {
        const sc = way ? P.project(sk, Math.PI / 2, heel, {underwater: way})
                       : P.project(sk, Math.PI / 2, heel);
        const hull = sc.figures.filter(f => f.kind === 'hull');
        const ys = fs => fs.reduce((a, f) => a.concat(f.pts.map(p => p.y)), []);
        const over = ys(hull.filter(f => !f.under)), under = ys(hull.filter(f => f.under));
        out[heel + ' ' + (way || 'default')] = {
          n: hull.length, nUnder: hull.filter(f => f.under).length,
          overMax: Math.max(...over), underMin: under.length ? Math.min(...under) : null,
          bounds: sc.bounds, all: JSON.stringify(sc.figures)};
      });
    });
    try {
      P.project(sk, 0, 0, {underwater: 'murky'});
      out.error = null;
    } catch (e) {
      out.error = String(e.message);
    }
    return out;
"""


@needs_node
@pytest.mark.parametrize("path", [*PROFILED, FRIGATE])
def test_the_hull_below_the_water_is_drawn_three_ways_hidden_by_default(tmp_path, path):
    """§6, §19.1 item 16 (the owner's, on the sheets): `project`'s `underwater` draws a hull with a
    profile below the water hidden by the sea (UNDERWATER, proposed, the default: nothing of it
    under the sea line), faint (the part under the line marked `under`, all of it there), or
    solid (as its strips stand, down to the drawn depth); upright and heeled, the bounds the same
    three ways. A hull with no profile is drawn as before whichever is asked."""
    graph = graph_of(path)
    got = run_js(tmp_path, {"graph": graph}, UNDER_THE_WATER)
    assert got["default"] == "hidden"
    assert got["error"] and "murky" in got["error"]
    for heel in ("0", "0.17"):
        ways = {w: got[f"{heel} {w}"] for w in ("default", "hidden", "faint", "solid")}
        assert ways["default"]["all"] == ways["hidden"]["all"]
        for w in ways.values():
            assert w["bounds"] == pytest.approx(ways["solid"]["bounds"], abs=1e-9)
        if "profile" not in graph["hull"]:
            assert ways["hidden"]["all"] == ways["faint"]["all"] == ways["solid"]["all"]
            continue
        assert ways["hidden"]["nUnder"] == 0 and ways["hidden"]["overMax"] <= 1e-9
        assert ways["faint"]["nUnder"] > 0 and ways["faint"]["overMax"] <= 1e-9
        assert ways["faint"]["underMin"] >= -1e-9
        assert ways["solid"]["nUnder"] == 0 and ways["solid"]["overMax"] > 2.0  # 2.45 m drawn


@needs_node
@pytest.mark.parametrize("path", PROFILED)
def test_the_stern_lights_are_seen_only_from_abaft_the_transom(tmp_path, path):
    """The lights are marks on the transom's after face (no opening): drawn seen from astern and
    on the quarter, not from ahead, where the face's back stands above the bow, nor abeam, where
    it is seen edge on."""
    graph = graph_of(path)
    n = sum(band[2] for band in graph["hull"]["profile"]["form"]["stern"]["lights_m"])
    got = run_js(
        tmp_path,
        {"graph": graph},
        """
        const sk = P.buildSkeleton(d.graph, null);
        return [0, Math.PI / 2, 3 * Math.PI / 4, Math.PI].map(facing =>
          P.project(sk, facing, 0).figures.filter(f => f.part === 'light').length);
        """,
    )
    assert got == [0, 0, n, n]


# The views the review drew (heel positive lowers the starboard side, toward a viewer at pi/2)
FACES_SEEN = """
    const hull = P.hullFigures(d.hull);
    const sk = {figures: hull.map(f => Object.assign({kind: 'hull'}, f))};
    const views = {abeam: [Math.PI / 2, 0], toward10: [Math.PI / 2, 0.1745],
                   toward20: [Math.PI / 2, 0.349], away10: [Math.PI / 2, -0.1745],
                   ahead: [0, 0], astern: [Math.PI, 0], quarter: [3 * Math.PI / 4, 0],
                   bow: [Math.PI / 4, 0.1745]};
    const out = {hull: hull.filter(f => d.parts.includes(f.part)).map(f =>
      ({part: f.part, side: f.side || null, deck: f.deck || null, pts: f.pts}))};
    Object.keys(views).forEach(name => {
      const [facing, heel] = views[name];
      out[name] = P.project(sk, facing, heel, {underwater: 'solid'}).figures
        .filter(f => d.parts.includes(f.part)).map(f => [f.part, f.side || null, f.deck || null]);
    });
    return out;
"""


@needs_node
@pytest.mark.parametrize("builder", BUILDERS)
@pytest.mark.parametrize("path", PROFILED)
def test_wales_and_bands_are_drawn_only_on_the_outside_of_the_side(tmp_path, path, builder):
    """A wale or a port band is on the outside of the side (§6): seen from the far side's inboard,
    over the near rail as the ship heels toward the viewer (the page's lee view), it is not drawn
    on the far bulwark's inner face. Heeled 10 and 20 degrees toward the viewer abeam, no far
    (larboard) wale or band is drawn; abeam upright, every near one; ahead and astern, both
    sides' where the side's flare turns them to the viewer."""
    hull = hull_of(path, builder)
    got = run_js(tmp_path, {"hull": hull, "parts": ["wale", "band"]}, FACES_SEEN)
    near = [f for f in got["hull"] if f["side"] == "starboard"]
    assert near and len(near) == len(got["hull"]) / 2
    for view in ("toward10", "toward20", "abeam"):
        sides = [side for _part, side, _deck in got[view]]
        assert "larboard" not in sides, view
    assert len(got["abeam"]) == len(near)
    for view in ("ahead", "astern"):
        assert {side for _part, side, _deck in got[view]} == {"starboard", "larboard"}, view


@needs_node
@pytest.mark.parametrize("builder", BUILDERS)
@pytest.mark.parametrize("path", PROFILED)
def test_each_tier_of_ports_cut_in_the_side_is_drawn_as_a_band(tmp_path, path, builder):
    """§6's port bands (PORT_BANDS, the owner's to keep): a deck's strake of ports is drawn where
    its ports are cut in the side, each port's middle below the rail; not where the guns fire over
    the rail. The 64's lower, upper and quarterdeck tiers (1407F cuts all three in her side; her
    foremost quarterdeck port reaches 2 cm over the rail), none for her forecastle's and
    roundhouse's carronades, whose middles stand 0.3 m over it; the razee's three."""
    hull = hull_of(path, builder)
    profile = hull["profile"]
    got = run_js(tmp_path, {"hull": hull, "parts": ["band"]}, FACES_SEEN)
    drawn = {f["deck"] for f in got["hull"]}
    want = (
        {"lower", "upper", "quarterdeck"}
        if path == SIXTY_FOUR
        else {"upper", "quarterdeck", "forecastle"}
    )
    assert drawn == want
    for word, ports in profile["ports_m"].items():
        depth = profile["port_size_m"][word][1]
        over = [z + depth / 2 - interp(profile["rail_m"], x) for x, z, _hb in ports]
        assert (max(over) <= 0.0) == (word in want), (word, max(over))


@needs_node
@pytest.mark.parametrize("builder", BUILDERS)
@pytest.mark.parametrize("path", PROFILED)
def test_a_deck_is_drawn_only_where_its_top_is_seen(tmp_path, path, builder):
    """A deck strip's top faces up (`outward`): it is drawn only where the viewer sees that face,
    so a deck rising aft is not painted through the counter on the quarter, nor one heeled away
    through the near side. Heeled toward the viewer every deck strip is drawn; heeled away, and
    abeam upright (edge on), none; on the quarter only the strips whose top faces aft."""
    hull = hull_of(path, builder)
    got = run_js(tmp_path, {"hull": hull, "parts": ["deck"]}, FACES_SEEN)
    decks = got["hull"]
    assert decks
    assert len(got["toward10"]) == len(got["toward20"]) == len(decks)
    assert got["away10"] == [] and got["abeam"] == []
    falling_aft = 0
    for f in decks:  # the strip's x ends and its heights there
        (xa, _ya, za), (xb, _yb, zb) = f["pts"][0], f["pts"][1]
        falling_aft += zb > za + 1e-9 and xb > xa
    assert 0 < len(got["quarter"]) == falling_aft < len(decks)


@needs_node
@pytest.mark.parametrize("builder", BUILDERS)
@pytest.mark.parametrize("path", PROFILED)
def test_where_a_deck_ends_over_another_a_bulkhead_closes_the_space_between(
    tmp_path, path, builder
):
    """Where a deck ends with another running on under it, a face across the ship closes the
    space (§6's `bulkhead`; judgement, derived from `decks_m` and `rail_m`): at the deck's end,
    from the deck below up to the top of the side there, on the drawn side at each height. The
    64's roundhouse front, quarterdeck breast and forecastle's after end; the razee's breast and
    forecastle. So dead ahead the space under her quarterdeck and roundhouse is not seen through,
    and on the quarter her forecastle deck is not seen through its after end."""
    hull = hull_of(path, builder)
    profile = hull["profile"]
    decks = profile["decks_m"]
    got = run_js(
        tmp_path,
        {"hull": hull},
        """
        const H = d.hull.stations ? null : P.profileHull(d.hull.profile);
        const top = H ? (x => H.station(x).pts[H.station(x).pts.length - 1][0])
          : P.formHull(d.hull).topAt;
        return P.hullFigures(d.hull).filter(f => f.part === 'bulkhead' && f.deck)
          .map(f => ({deck: f.deck, pts: f.pts, top: top(f.pts[0][0])}));
        """,
    )
    ends = {
        "sixty-four": {("roundhouse", "fore"), ("quarterdeck", "fore"), ("forecastle", "aft")},
        "razee-44": {("roundhouse", "fore"), ("quarterdeck", "fore"), ("forecastle", "aft")},
    }[Path(path).stem]
    at = {(f["deck"], "aft" if f["pts"][0][0] == decks[f["deck"]][0][0] else "fore") for f in got}
    assert at == ends and len(got) == len(ends)
    for f in got:
        pts, word = f["pts"], f["deck"]
        x = pts[0][0]
        assert all(p[0] == x for p in pts)
        assert x in (decks[word][0][0], decks[word][-1][0])
        under = [
            interp(line, x)
            for line in decks.values()
            if line[0][0] < x < line[-1][0] and interp(line, x) < interp(decks[word], x)
        ]
        below = max(under)
        zs = [p[2] for p in pts]
        assert min(zs) == pytest.approx(below, abs=1e-6)
        assert max(zs) == pytest.approx(f["top"], abs=1e-6)
        assert f["top"] > interp(decks[word], x)
        half = len(pts) // 2
        for p, q in zip(pts[:half], reversed(pts[half:]), strict=True):
            assert p[1] > 0.0 and q[1] == pytest.approx(-p[1]) and q[2] == p[2]
