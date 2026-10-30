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
- Package 75 (B5.2, docs/design/Design-ShipsEngineExtensions.md §6.1), on the fixture
  `frigate_with_mizen_yard()` (tests/rig_fixtures.py): the mizen course cut at the mast swung
  whole about its mast on its file's corners, its yard slung at its truss with the bare fore
  part to windward, its lifts from the yard's after part, its sheet to the taffrail; brailed to
  the mast and up under the yard, furled along it, reefed from the foot; the frame equal across
  states; a whole lateen with its cut drawn as a standing lug to leeward.
- Package 75 (B5.3, Ext §6.2), on the same fixture and on the profiled files with its yards cut
  on their own spars: each yard under the bowsprit or the jib-boom at its station, hanging
  under its spar; the spritsail hung from its yard, the sprit topsail's clews at the spritsail
  yard's arms, every foot above the water; the braces up to the fore top, the spritsail's
  sheets aft to the side, the lifts to the spar's end; each sorted at its own middle; and, by
  the lead's ruling of 2026-10-29, the bowsprit stood from the profile's stem head as long as
  the file has it, the jib-boom from its end.
- Package 75 (B5.5, Ext §17.6), on the fixture `frigate_with_driver()`: the driver of the 64 and
  the 74 cut at the mast, its throat and peak swung about the mast, its tack at the boom's jaws
  and its clew along the boom, the boom swung by its sheet and amidships while it is in the sail
  room; its head along the mizen yard's line and on along Steel's driver yard; brailed to the
  mast and furled along its head; its sheet from the boom's end to the taffrail; the yard laid
  on the course's corners whichever sail is bent, through the engine's shift and back; the frame
  holding the boom's swing beyond the taffrail across states.
"""

from __future__ import annotations

import json
import math
import random
import shutil
import subprocess
from dataclasses import replace
from pathlib import Path

import pytest
from rig_fixtures import (
    DRIVER_YARD_M,
    SPREAD,
    SPRIT_TOPSAIL_HANG_M,
    SPRIT_TOPSAIL_STATION,
    SPRITSAIL_FOOT_ABOVE_WATER_M,
    SPRITSAIL_HANG_M,
    SPRITSAIL_STATION,
    frigate_with_driver,
    frigate_with_driver_doc,
    frigate_with_mizen_yard,
    frigate_with_mizen_yard_doc,
    write_ship,
)

from freesail import orders
from freesail.api import queries
from freesail.api.session import make_ship, make_world
from freesail.core.world import Scenario
from freesail.evolutions import Runner
from freesail.evolutions.trim import set_sheet_angle
from freesail.physics.wind import Wind, WindParams
from freesail.ship import form
from freesail.ship.loader import ship_from_dict
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


# How far forward of B5.1's the end of each profiled file's bowsprit is drawn since B5.3, metres
# (the 64's 35.228 -> 37.001, the razee's 35.211 -> 36.903; their jib-booms' ends with them)
BOWSPRIT_END_FORWARD_OF_B5_1 = {SIXTY_FOUR: 1.773, RAZEE: 1.692}


@needs_node
@pytest.mark.parametrize("path", PROFILED)
def test_the_bowsprit_stands_from_the_stem_head_its_length_up_to_its_ends_height(tmp_path, path):
    """Indf §12.3: the heel at the stem head, or the rail there if that is lower (the razee's).
    B5.3 (the lead's ruling of 2026-10-29, Ext §6.2): the whole spar from there, as long as the
    file has it, up to its end's height above the datum, so that the yards under it hang from a
    bowsprit that stands where the file has it; the jib-boom from its end, as before.

    Old beside new: B5.1 drew the heel there and kept the end where a heel on the datum put it,
    `x_m` + sqrt(L^2 - min(H, 0.95 L)^2) forward at deck + H, so that the drawn spar fell short
    of the file's length (the 64's 12.65 m of 14.1, the razee's 12.72); its end now stands at
    the same height the file's length farther forward (BOWSPRIT_END_FORWARD_OF_B5_1)."""
    graph = graph_of(path)
    profile = graph["hull"]["profile"]
    deck = graph["hull"]["deck_height_m"]
    got = run_js(tmp_path, {"graph": graph}, SPARS_DRAWN)
    (bowsprit,) = [s for s in graph["spars"] if s["class"] == "bowsprit"]
    heel, tip = got["bowsprit"]
    hx, hz = profile["stem_m"][-1]
    assert heel == pytest.approx([hx, 0.0, min(hz, interp(profile["rail_m"], hx))], abs=0.001)
    length, height = bowsprit["length_m"], bowsprit["height_m"]
    assert math.dist(heel, tip) == pytest.approx(length)
    assert tip[1] == 0.0 and tip[2] == pytest.approx(deck + height)
    assert tip[0] > heel[0]
    # old (B5.1) beside new
    rise = min(height, 0.95 * length)
    old_tip = [bowsprit["x_m"] + math.sqrt(length * length - rise * rise), 0.0, deck + rise]
    assert tip[2] == pytest.approx(old_tip[2])
    assert tip[0] - old_tip[0] == pytest.approx(BOWSPRIT_END_FORWARD_OF_B5_1[path], abs=0.001)
    # the jib-boom from the bowsprit's end, its length up to its own end's height
    jib_heel, jib_end = got["jib_boom"]
    (jib_boom,) = [s for s in graph["spars"] if s["class"] == "jib_boom"]
    assert jib_heel == pytest.approx(tip)
    assert math.dist(jib_heel, jib_end) == pytest.approx(jib_boom["length_m"])
    assert jib_end[2] == pytest.approx(deck + jib_boom["height_m"])
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


# ---------------------------------------------------------------------------
# Package 75 (B5.2, docs/design/Design-ShipsEngineExtensions.md §6.1): the mizen course cut at the
# mast and its yard, on the fixture (tests/rig_fixtures.py; no file carries one yet)
# ---------------------------------------------------------------------------

MIZEN_COURSE = "mizzen.course"


def mizen_by_the_wind(
    tack: str, sheet_deg: float = 30.0, state: SailState = SailState.SET, reefs: int = 0
) -> dict:
    """`frigate_with_mizen_yard()` under plain sail on `tack`, her mizen course in `state`,
    sheeted `sheet_deg` off the centreline: the graph and snapshot."""
    ship = frigate_with_mizen_yard()
    for sid in ship.groups["plain sail"]:
        ship.sails[sid].state = SailState.SET
    course = ship.sails[MIZEN_COURSE]
    set_sheet_angle(ship, course, math.radians(sheet_deg))
    course.state, course.reefs = state, reefs
    awa = math.radians(60.0) * (1.0 if tack == "starboard" else -1.0)
    return ship_state(ship, awa=awa, tack=tack)


MIZEN_FIGURES = """
    const sk = P.buildSkeleton(d.graph, d.snap);
    const y = sk.spars['mizzen.yard'], m = sk.spars['mizzen.mast'];
    const course = sk.figures.filter(f => f.id === 'mizzen.course');
    const fig = course.length ? course[0] : null;
    const pts = fig ? fig.path.reduce((a, seg) => a.concat(seg), []) : [];
    const off = p => [Math.hypot(p[0] - m.xAt(p[2]), p[1]), p[2]];
    return {
      heel: y.a, peak: y.b, truss: y.truss, mx: m.xAt(y.truss[2]),
      corners: fig ? fig.corners : null, off: fig ? fig.corners.map(off) : null,
      path: pts, pathOff: pts.map(off), state: fig ? fig.state : null,
      lines: sk.figures.filter(f => f.kind === 'line' && (f.of === 'mizzen.yard' ||
        f.of === 'mizzen.course')).map(f => ({id: f.id, cls: f.cls, pts: f.pts,
        off: f.pts.map(off)})),
      masthead: m.head,
    };
"""


def _course_and_yard(graph: dict) -> tuple[dict, dict, float]:
    sail = next(s for s in graph["sails"] if s["id"] == MIZEN_COURSE)
    yard = next(s for s in graph["spars"] if s["id"] == "mizzen.yard")
    return sail, yard, graph["hull"]["deck_height_m"]


def _mast_line(graph: dict) -> tuple[list, list]:
    """The mizzen mast's raked line (`client/projection.js`'s `xAt`): a point on it at the deck
    and its direction up the mast."""
    mast = next(s for s in graph["spars"] if s["id"] == "mizzen.mast")
    deck = graph["hull"]["deck_height_m"]
    slope = -math.tan(mast.get("rake") or 0.0)
    up = math.hypot(slope, 1.0)
    return [mast["x_m"], 0.0, deck], [slope / up, 0.0, 1.0 / up]


def _off_the_line(p: list, origin: list, axis: list) -> list:
    """The part of p's offset from a line square to it (the line through `origin` along the
    unit `axis`)."""
    d = [a - b for a, b in zip(p, origin, strict=True)]
    along = sum(a * b for a, b in zip(d, axis, strict=True))
    return [a - along * b for a, b in zip(d, axis, strict=True)]


@needs_node
@pytest.mark.parametrize("tack", ["starboard", "larboard"])
def test_the_mizen_yard_is_slung_at_its_truss_its_fore_part_to_windward(tmp_path, tack):
    """Ext §6.1: the truss at the mast at deck plus the throat's height; the course swung whole
    about the mast, where its luff is laced, by the sheet's angle to the sheet's side, on its
    corners (each as far from the mast and from the others as the file has it); the yard's
    after part along its head to the peak, and the bare fore part on the same line forward of
    the mast by the rest of the yard, to windward as the after part lies to leeward. Its one
    sheet runs from the clew to the taffrail on the centreline."""
    data = mizen_by_the_wind(tack)
    got = run_js(tmp_path, data, MIZEN_FIGURES)
    sail, yard, deck = _course_and_yard(data["graph"])
    origin, axis = _mast_line(data["graph"])
    lee = 1.0 if tack == "larboard" else -1.0  # +1 starboard
    file = [[q[0], 0.0, deck + q[1]] for q in sail["corners_m"]]  # tack, throat, peak, clew
    heel, peak, truss = got["heel"], got["peak"], got["truss"]
    truss_z = deck + sail["corners_m"][1][1]
    on_mast = origin[0] + axis[0] / axis[2] * (truss_z - deck)
    assert truss == [pytest.approx(on_mast), 0.0, pytest.approx(truss_z)]
    assert heel[0] > truss[0] > peak[0]  # the fore part forward of the mast, the head abaft it
    assert heel[1] * lee < 0.0 < peak[1] * lee  # the fore part to windward, the peak to leeward
    assert math.dist(heel, peak) == pytest.approx(yard["length_m"])
    u = [p - t for p, t in zip(peak, truss, strict=True)]
    w = [h - t for h, t in zip(heel, truss, strict=True)]
    normal = (u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0])
    assert math.hypot(*normal) / math.hypot(*u) < 1e-6  # heel, truss and peak on one line
    # the corners, drawn [throat, peak, clew, tack]: swung whole, each as far from the mast and
    # from the others as in the file; the luff on the mast within 0.1 m; the throat at the truss
    # and the peak at the yard's peak
    drawn = [got["corners"][i] for i in (3, 0, 1, 2)]  # tack, throat, peak, clew
    for i, (p, q) in enumerate(zip(drawn, file, strict=True)):
        off_p, off_q = _off_the_line(p, origin, axis), _off_the_line(q, origin, axis)
        assert math.hypot(*off_p) == pytest.approx(math.hypot(*off_q), abs=1e-6), i
        for j in range(i):
            assert math.dist(p, drawn[j]) == pytest.approx(math.dist(q, file[j]), abs=1e-6)
    assert math.hypot(*_off_the_line(drawn[0], origin, axis)) <= 0.1  # the tack on the mast
    assert math.dist(drawn[1], truss) <= 0.1 and drawn[2] == pytest.approx(peak)
    # the sheet's angle about the mast: the peak's offset from it, swung from the file's
    off_p, off_q = _off_the_line(peak, origin, axis), _off_the_line(file[2], origin, axis)
    cos = sum(a * b for a, b in zip(off_p, off_q, strict=True)) / (
        math.hypot(*off_p) * math.hypot(*off_q)
    )
    assert math.degrees(math.acos(min(cos, 1.0))) == pytest.approx(30.0, abs=1e-6)
    assert drawn[3][1] * lee > 0.5  # the clew to leeward
    sheets = [ln for ln in got["lines"] if ln["cls"] == "sheet"]
    length = data["graph"]["hull"]["length_waterline_m"]
    assert [s["id"] for s in sheets] == ["mizzen.course.sheet"]
    assert sheets[0]["pts"] == [
        pytest.approx(drawn[3]),
        pytest.approx([-0.52 * length, 0.0, 1.02 * deck]),
    ]


@needs_node
def test_the_course_unswung_lies_on_its_files_corners(tmp_path):
    """With its sheet at no angle the course lies in the fore-and-aft plane on the file's
    corners, to the millimetre: the drawing is the file's cut, swung."""
    data = mizen_by_the_wind("larboard")
    for s in data["snap"]["sails"]:
        if s["id"] == MIZEN_COURSE:
            s["sheet_angle"] = 0.0
    got = run_js(tmp_path, data, MIZEN_FIGURES)
    sail, _yard, deck = _course_and_yard(data["graph"])
    drawn = [got["corners"][i] for i in (3, 0, 1, 2)]  # tack, throat, peak, clew
    for p, q in zip(drawn, sail["corners_m"], strict=True):
        assert p == pytest.approx([q[0], 0.0, deck + q[1]], abs=1e-3)


@needs_node
def test_the_mizen_yards_lifts_hold_its_after_part_from_the_masthead(tmp_path):
    """The lifts of every yard drawn faint (B5.1): the mizen yard's from its after part, where
    the sail hangs, the pair about its middle a twentieth of it apart either way (the starboard
    one nearer the peak), so that neither is drawn over the other, and the derrick nearer the
    peak, each up to the mizzen mast's head; no brace."""
    got = run_js(tmp_path, mizen_by_the_wind("larboard"), MIZEN_FIGURES)
    truss, peak = got["truss"], got["peak"]
    lifts = {ln["id"]: ln["pts"] for ln in got["lines"] if ln["cls"] == "lift"}
    shares = {
        "mizzen.yard.derrick": 2.0 / 3.0,
        "mizzen.yard.lift.starboard": 0.55,
        "mizzen.yard.lift.larboard": 0.45,
    }
    assert set(lifts) == set(shares)
    for lid, (foot, top) in lifts.items():
        want = [t + shares[lid] * (p - t) for t, p in zip(truss, peak, strict=True)]
        assert foot == pytest.approx(want), lid
        assert top == pytest.approx(got["masthead"]), lid
    starboard, larboard = (
        lifts["mizzen.yard.lift.starboard"][0],
        lifts["mizzen.yard.lift.larboard"][0],
    )
    assert math.dist(starboard, larboard) == pytest.approx(0.1 * math.dist(truss, peak))
    assert not [ln for ln in got["lines"] if ln["cls"] == "brace"]


HEELS = [0.0, 0.15, -0.15, 0.3, -0.3]


@needs_node
@pytest.mark.parametrize("facing_deg", [0.0, 45.0, 90.0, 135.0, 225.0])
def test_the_frame_holds_the_mizen_yards_swing_across_states(tmp_path, facing_deg):
    """Ext §6.1: `fullRigFrame` reaches the yard's swing about its truss, the fore part's with
    it, at the heights of the yard's ends and the sail's foot and at the quarters as well as
    the four sides, so every point of the yard, the course and their lines lies within the
    frame alone, upright or heeled; and the view's scale is the same on either tack, at any
    sheet, set, in the gear or furled."""
    states = {
        f"{tack}-{sheet}-{state.value}": mizen_by_the_wind(tack, sheet, state)
        for tack in ("starboard", "larboard")
        for sheet in (18.0, 45.0, 85.0)
        for state in (SailState.SET, SailState.IN_THE_GEAR, SailState.FURLED)
    }
    body = f"""
        const f = {math.radians(facing_deg)};
        const mizen = g => [g.id, g.of].some(i => i === 'mizzen.yard' || i === 'mizzen.course');
        const out = {{}};
        Object.keys(d).forEach(k => {{
          const sk = P.buildSkeleton(d[k].graph, d[k].snap);
          out[k] = {json.dumps(HEELS)}.map(h => {{
            const proj = P.makeProjector(f, h);
            const fr = sk.frame.map(proj);
            const xs = fr.map(p => p.x), ys = fr.map(p => p.y);
            const box = {{minX: Math.min(...xs), maxX: Math.max(...xs),
                          minY: Math.min(...ys), maxY: Math.max(...ys)}};
            let over = -1e9, n = 0;
            sk.figures.filter(mizen).forEach(g => {{
              (g.path ? P.flattenPath(g.path) : g.pts).map(proj).forEach(q => {{
                over = Math.max(over, box.minX - q.x, q.x - box.maxX, box.minY - q.y,
                                q.y - box.maxY);
                n += 1;
              }});
            }});
            return {{frame: box, over: over, n: n, bounds: P.project(sk, f, h).bounds}};
          }});
        }});
        return out;
    """
    got = run_js(tmp_path, states, body)
    first = got[next(iter(got))]
    for name, views in got.items():
        for heel, view, same in zip(HEELS, views, first, strict=True):
            assert view["n"] > 10 and view["over"] <= 1e-6, (name, heel, view["over"])
            for k in ("minX", "maxX", "minY", "maxY"):
                assert view["frame"][k] == pytest.approx(same["frame"][k], abs=1e-6), (name, k)
                assert view["bounds"][k] == pytest.approx(same["bounds"][k], abs=1e-6), (name, k)


def _off_the_segment(p: list, a: list, b: list) -> float:
    """How far the point p lies from the segment a-b."""
    u = [y - x for x, y in zip(a, b, strict=True)]
    t = sum((q - x) * c for q, x, c in zip(p, a, u, strict=True)) / sum(c * c for c in u)
    t = max(0.0, min(1.0, t))
    return math.dist(p, [x + t * c for x, c in zip(a, u, strict=True)])


@needs_node
def test_the_course_is_brailed_to_the_mast_and_furled_along_its_yard(tmp_path):
    """Ext §6.1: in the gear the course is gathered to the mast and up under the yard, its foot
    hauled up the mast and its leech in along the yard by the gear's depth (IN_GEAR_DEPTH,
    0.35), its sheet from the clew brailed in with it; furled, a bundle along the yard's after
    part, aloft, with no sheet drawn. The yard stays where it was."""
    lee = run_js(tmp_path, mizen_by_the_wind("larboard"), MIZEN_FIGURES)
    gear = mizen_by_the_wind("larboard", state=SailState.IN_THE_GEAR)
    brailed = run_js(tmp_path, gear, MIZEN_FIGURES)
    furled = run_js(tmp_path, mizen_by_the_wind("larboard", state=SailState.FURLED), MIZEN_FIGURES)
    truss, peak = lee["truss"], lee["peak"]
    for got in (brailed, furled):
        assert got["truss"] == pytest.approx(truss) and got["peak"] == pytest.approx(peak)
    luff = truss[2] - lee["corners"][3][2]
    head_aft = lee["off"][1][0]  # the peak's distance abaft the mast
    assert min(z for _aft, z in lee["pathOff"]) < truss[2] - 0.9 * luff  # set, down to its foot
    assert brailed["state"] == "in_the_gear"
    for aft, z in brailed["pathOff"]:
        assert z >= truss[2] - 0.35 * luff - 1e-6
        assert aft <= 0.35 * head_aft + 0.8 + 1e-6
    # the sheet from the clew in the bundle, not where it stood set, to the taffrail
    (sheet,) = [ln for ln in brailed["lines"] if ln["cls"] == "sheet"]
    aft, z = sheet["off"][0]
    assert truss[2] - 0.35 * luff < z < truss[2] and 0.0 < aft <= 0.35 * head_aft + 0.8
    length = gear["graph"]["hull"]["length_waterline_m"]
    deck = gear["graph"]["hull"]["deck_height_m"]
    assert sheet["pts"][1] == pytest.approx([-0.52 * length, 0.0, 1.02 * deck])
    assert furled["state"] == "furled"
    assert max(_off_the_segment(p, truss, peak) for p in furled["path"]) <= 0.35 + 1e-6
    assert not [ln for ln in furled["lines"] if ln["cls"] == "sheet"]  # furled: none drawn


@needs_node
@pytest.mark.parametrize("path", PROFILED)
def test_the_courses_sheet_leads_to_the_taffrail_of_a_hull_drawn_from_its_profile(tmp_path, path):
    """Ext §6.1: where the file gives a profile, as the 64's and the 74's do, the course's sheet
    runs from its clew to the profile's taffrail, the rail's after end (`rail_m`'s first point)
    on the centreline, not to the stern of the hull drawn without one. The fixture's rig on each
    profiled hull served."""
    data = mizen_by_the_wind("larboard")
    data["graph"]["hull"] = ship_state(make_ship(path))["graph"]["hull"]
    got = run_js(tmp_path, data, MIZEN_FIGURES)
    rail = data["graph"]["hull"]["profile"]["rail_m"][0]
    length = data["graph"]["hull"]["length_waterline_m"]
    (sheet,) = [ln["pts"] for ln in got["lines"] if ln["cls"] == "sheet"]
    assert sheet[0] == pytest.approx(got["corners"][2])  # the clew
    assert sheet[1] == pytest.approx([rail[0], 0.0, rail[1]], abs=1e-3)
    assert abs(rail[0] + 0.52 * length) > 0.1  # not the stern drawn without a profile


@needs_node
def test_a_reef_raises_the_courses_foot_up_the_mast(tmp_path):
    """Ext §6.1: the reef raises the foot as a gaff sail's does: the tack up the luff on the mast
    by the reef's share of it (the curve class's `reef_factor`, served), the clew with it."""
    whole = run_js(tmp_path, mizen_by_the_wind("larboard"), MIZEN_FIGURES)
    data = mizen_by_the_wind("larboard", reefs=1)
    reefed = run_js(tmp_path, data, MIZEN_FIGURES)
    sail, _yard, _deck = _course_and_yard(data["graph"])
    rise = sail["reef_factor"] * (whole["corners"][0][2] - whole["corners"][3][2])
    assert rise > 0.5
    assert reefed["corners"][3][2] == pytest.approx(whole["corners"][3][2] + rise)
    assert reefed["off"][3][0] <= 0.1  # the tack still on the mast
    assert reefed["corners"][2][2] == pytest.approx(whole["corners"][2][2] + rise)
    assert reefed["corners"][:2] == [pytest.approx(p) for p in whole["corners"][:2]]


@needs_node
def test_a_whole_lateen_with_its_cut_is_drawn_as_a_standing_lug_to_leeward(tmp_path):
    """Ext §6.1: a lateen with four corners and no key (a later package's tartane) is drawn by
    the lug's cut as a standing sail on the lee side of its tack, its yard from the cut's throat
    to its peak, not at the fixed tilt a lateen yard with no cut keeps."""
    doc = frigate_with_mizen_yard_doc()
    next(s for s in doc["sails"] if s["id"] == MIZEN_COURSE).pop("cut_at_mast")
    ship = ship_from_dict(doc, "whole.yaml")
    course = ship.sails[MIZEN_COURSE]
    course.state = SailState.SET
    set_sheet_angle(ship, course, math.radians(30.0))
    data = ship_state(ship, awa=math.radians(-60.0), tack="larboard")
    got = run_js(
        tmp_path,
        data,
        """
        const sk = P.buildSkeleton(d.graph, d.snap);
        const y = sk.spars['mizzen.yard'];
        const pieces = sk.figures.filter(f => f.id === 'mizzen.course');
        return {a: y.a, b: y.b, cut: !!y.cutAtMast, n: pieces.length,
                corners: pieces[0].corners};
        """,
    )
    deck = data["graph"]["hull"]["deck_height_m"]
    sail = next(s for s in data["graph"]["sails"] if s["id"] == MIZEN_COURSE)
    _tack, throat, peak, _clew = sail["corners_m"]
    assert not got["cut"] and got["n"] >= 1
    assert got["a"][2] == pytest.approx(deck + throat[1])
    assert got["b"][2] == pytest.approx(deck + peak[1])
    assert got["b"][1] > 0.5 and got["corners"][2][1] > 0.5  # the peak and the clew to leeward


@needs_node
def test_the_course_as_the_game_serves_it_is_drawn_at_its_mast(tmp_path):
    """The fixture's world through the game's own doors (`/api/ship`, `/api/state`): the graph
    serves the course's cut and key and the yard's class, and the drawing takes them as above.
    As she starts, the course furled at no sheet: the yard in the fore-and-aft plane, slung at
    its truss, the course a bundle along its after part; then set and sheeted, to leeward of
    the tack the state gives, the yard's fore part to windward, its sheet to the taffrail."""
    pytest.importorskip("fastapi")
    from fastapi.testclient import TestClient

    from freesail.ui.server import Driver, create_app

    path = write_ship(frigate_with_mizen_yard_doc(), tmp_path)
    scenario = Scenario(wind_from_deg=0.0, wind_speed_kn=10.0, ship_heading_deg=60.0)
    world = make_world(7, str(path), scenario)
    world.tick()  # her tack and her sails' states are read at a tick
    course = world.ship.sails[MIZEN_COURSE]
    with TestClient(create_app(Driver(world))) as client:
        start = {"graph": client.get("/api/ship").json(), "snap": client.get("/api/state").json()}
        course.state = SailState.SET
        set_sheet_angle(world.ship, course, math.radians(30.0))
        world.tick()
        sheeted = {"graph": client.get("/api/ship").json(), "snap": client.get("/api/state").json()}
    sail, yard, deck = _course_and_yard(start["graph"])
    assert sail["cut_at_mast"] is True and len(sail["corners_m"]) == 4
    assert yard["class"] == "lateen_yard"
    assert start["snap"]["ship"]["tack"] == sheeted["snap"]["ship"]["tack"] == "larboard"
    origin, axis = _mast_line(start["graph"])
    truss_z = deck + sail["corners_m"][1][1]
    on_mast = origin[0] + axis[0] / axis[2] * (truss_z - deck)

    furled = run_js(tmp_path, start, MIZEN_FIGURES)
    assert furled["state"] == "furled"
    assert furled["truss"] == [pytest.approx(on_mast), 0.0, pytest.approx(truss_z)]
    assert furled["heel"][1] == pytest.approx(0.0) and furled["peak"][1] == pytest.approx(0.0)
    assert furled["heel"][0] > furled["truss"][0] > furled["peak"][0]
    truss, peak = furled["truss"], furled["peak"]
    assert max(_off_the_segment(p, truss, peak) for p in furled["path"]) <= 0.35 + 1e-6
    assert not [ln for ln in furled["lines"] if ln["cls"] == "sheet"]

    set_ = run_js(tmp_path, sheeted, MIZEN_FIGURES)
    assert set_["state"] == "set" and set_["truss"] == pytest.approx(truss)
    assert set_["heel"][1] < 0.0 < set_["peak"][1]  # on the larboard tack: the peak to starboard
    assert set_["corners"][2][1] > 0.5  # the clew to leeward
    (sheet,) = [ln["pts"] for ln in set_["lines"] if ln["cls"] == "sheet"]
    length = start["graph"]["hull"]["length_waterline_m"]
    assert sheet == [
        pytest.approx(set_["corners"][2]),
        pytest.approx([-0.52 * length, 0.0, 1.02 * deck]),
    ]


# ---------------------------------------------------------------------------
# Package 75 (B5.3, docs/design/Design-ShipsEngineExtensions.md §6.2): the yards under the
# bowsprit, on the fixture (tests/rig_fixtures.py; no file carries them yet) and on the profiled
# files with the fixture's yards cut on their own bowsprit and jib-boom; the bowsprit stood from
# the profile's stem head (the lead's ruling of 2026-10-29)
# ---------------------------------------------------------------------------

SPRIT_YARDS = ("spritsail.yard", "sprit_topsail.yard")
SPRIT_SAILS = ("spritsail", "sprit_topsail")
# each yard's spar, and how far the fixture hangs it under that spar's line
SPRIT_HANG = {
    "spritsail.yard": ("bowsprit", SPRITSAIL_HANG_M),
    "sprit_topsail.yard": ("jib_boom", SPRIT_TOPSAIL_HANG_M),
}
CLEW_SPREAD = 0.9  # client/projection.js: a topsail's clews at nine-tenths of the yard below
HEAD_SPREAD = 0.9  # and a sail with no yard below as broad as nine-tenths of its own


def sprit_sails(
    state: SailState = SailState.SET,
    reefs: int = 0,
    brace_deg: float = 0.0,
    tack: str = "larboard",
) -> dict:
    """`frigate_with_mizen_yard()` under plain sail on `tack` with the wind on the quarter, her
    spritsail and sprit topsail in `state` (the spritsail with `reefs`), the two yards braced
    `brace_deg` from square (positive, the starboard yardarm forward): the graph and snapshot."""
    ship = frigate_with_mizen_yard()
    for sid in ship.groups["plain sail"]:
        ship.sails[sid].state = SailState.SET
    for sid in SPRIT_SAILS:
        sail = ship.sails[sid]
        sail.state, sail.reefs = state, min(reefs, sail.reef_bands)
    for yid in SPRIT_YARDS:
        ship.spars[yid].brace_angle = math.radians(brace_deg)
    awa = math.radians(120.0) * (1.0 if tack == "starboard" else -1.0)
    return ship_state(ship, awa=awa, tack=tack)


SPRIT_FIGURES = """
    const sk = P.buildSkeleton(d.graph, d.snap || null);
    const mine = ['spritsail.yard', 'sprit_topsail.yard', 'spritsail', 'sprit_topsail'];
    const spar = id => {
      const r = sk.spars[id];
      return r ? {a: r.a, b: r.b, centre: r.centre || null, half: r.half || null} : null;
    };
    const sails = {};
    sk.figures.filter(f => f.kind === 'sail' && mine.includes(f.id)).forEach(f => {
      sails[f.id] = {state: f.state, corners: f.corners, path: P.flattenPath(f.path)};
    });
    const fore = sk.spars['fore.mast'];
    const topZ = fore.head[2] - 1;
    return {
      spars: {bowsprit: spar('bowsprit'), jib_boom: spar('jib_boom'),
              'spritsail.yard': spar('spritsail.yard'),
              'sprit_topsail.yard': spar('sprit_topsail.yard')},
      drawn: sk.figures.filter(f => f.kind === 'spar' && mine.includes(f.id))
        .map(f => ({id: f.id, pts: f.pts, hoist: f.hoist})),
      sails: sails,
      lines: sk.figures.filter(f => f.kind === 'line' && mine.includes(f.of))
        .map(f => ({id: f.id, cls: f.cls, pts: f.pts})),
      foreTop: [fore.xAt(topZ), topZ],
      foreX: fore.x,
    };
"""


def head_chain(graph: dict) -> dict[str, tuple[list, list]]:
    """The bowsprit and the booms on it, heel and end, as the drawing stands them: with a
    profile, the bowsprit from the stem head (the rail there if that is lower), as long as the
    file has it, up to its end's height above the datum (B5.3; the lead's ruling of
    2026-10-29); without one, from its `x_m` on the datum, rising its `height_m` (at most 0.95
    of its length), as before; a boom from the end of the spar it is on, up to its own end's
    height (at most 0.7 of its length)."""
    hull = graph["hull"]
    deck, profile = hull["deck_height_m"], hull.get("profile")
    spars = {s["id"]: s for s in graph["spars"]}
    out: dict[str, tuple[list, list]] = {}

    def place(sid: str) -> tuple[list, list]:
        if sid not in out:
            s = spars[sid]
            length, height = s["length_m"], s["height_m"]
            if s["class"] == "bowsprit" and profile:
                hx, hz = profile["stem_m"][-1]
                heel = [hx, 0.0, min(hz, interp(profile["rail_m"], hx))]
                rise = min(max(deck + height - heel[2], 0.0), 0.95 * length)
            elif s["class"] == "bowsprit":
                heel, rise = [s["x_m"], 0.0, deck], min(height, 0.95 * length)
            else:
                heel = place(s["parent"])[1]
                rise = max(min(deck + height - heel[2], 0.7 * length), 0.0)
            reach = math.sqrt(max(length * length - rise * rise, 0.0))
            out[sid] = (heel, [heel[0] + reach, 0.0, heel[2] + rise])
        return out[sid]

    for s in graph["spars"]:
        if s["class"] in ("bowsprit", "jib_boom", "flying_jib_boom"):
            place(s["id"])
    return out


def _on_the_line(heel: list, end: list, x: float) -> float:
    """The height of the line heel-end at x."""
    return heel[2] + (end[2] - heel[2]) * (x - heel[0]) / (end[0] - heel[0])


def with_sprit_yards(path: str) -> dict:
    """The file's served graph with the fixture's two yards under the bowsprit, their square
    sails and their lines (tests/rig_fixtures.py), cut on her own bowsprit and jib-boom as they
    are drawn from her stem head (`head_chain`) as the fixture cuts them on the frigate's: at
    its stations and hangs, as long as her fore topsail and fore topgallant yards, the spritsail
    down to a metre above the water and the sprit topsail the trapezoid to the spritsail yard's
    arms; both set (the graph's state: no snapshot)."""
    graph = graph_of(path)
    fixture = queries.ship_graph(frigate_with_mizen_yard())
    deck = graph["hull"]["deck_height_m"]
    chain = head_chain(graph)
    length = {s["id"]: s["length_m"] for s in graph["spars"]}

    def station(on: str, share: float, hang: float) -> tuple[float, float]:
        heel, end = chain[on]
        return heel[0] + share * (end[0] - heel[0]), heel[2] + share * (end[2] - heel[2]) - hang

    ss_x, ss_z = station("bowsprit", SPRITSAIL_STATION, SPRITSAIL_HANG_M)
    st_x, st_z = station("jib_boom", SPRIT_TOPSAIL_STATION, SPRIT_TOPSAIL_HANG_M)
    ss_len, st_len = length["fore.topsail.yard"], length["fore.topgallant.yard"]
    ss_depth = ss_z - SPRITSAIL_FOOT_ABOVE_WATER_M
    head, foot, gap = SPREAD * st_len, SPREAD * ss_len, st_z - ss_z
    up = (2.0 * head + foot) / (3.0 * (head + foot))
    spars = {
        "spritsail.yard": {"x_m": ss_x, "height_m": ss_z - deck, "length_m": ss_len},
        "sprit_topsail.yard": {"x_m": st_x, "height_m": st_z - deck, "length_m": st_len},
    }
    sails = {
        "spritsail": {
            "area_m2": SPREAD * ss_len * ss_depth,
            "x_m": ss_x,
            "centre_height_m": ss_z - 0.5 * ss_depth,
        },
        "sprit_topsail": {
            "area_m2": 0.5 * (head + foot) * gap,
            "x_m": ss_x + up * (st_x - ss_x),
            "centre_height_m": ss_z + up * gap,
        },
    }
    graph["spars"] += [{**s, **spars[s["id"]]} for s in fixture["spars"] if s["id"] in spars]
    graph["sails"] += [
        {**s, **sails[s["id"]], "state": "set"} for s in fixture["sails"] if s["id"] in sails
    ]
    graph["lines"] += [ln for ln in fixture["lines"] if ln["of"] in spars or ln["of"] in sails]
    return graph


@needs_node
@pytest.mark.parametrize("state", [SailState.SET, SailState.IN_THE_GEAR, SailState.FURLED])
def test_each_yard_under_the_bowsprit_stands_at_its_station_under_its_spar(tmp_path, state):
    """Ext §6.2: a yard on the bowsprit or the jib-boom stands at its own `x_m` at deck plus its
    `height_m`, with no slinging offset and no hoist whatever its sail's state, its arms across
    the ship, as far under its spar's drawn line as the fixture hangs it (within its file's
    tenth of a metre); not at its spar's heel, where the trial's spritsail hung with its foot
    two metres under the water (Eng §5)."""
    data = sprit_sails(state)
    got = run_js(tmp_path, data, SPRIT_FIGURES)
    deck = data["graph"]["hull"]["deck_height_m"]
    spars = {s["id"]: s for s in data["graph"]["spars"]}
    for yid, (on, hang) in SPRIT_HANG.items():
        yard, drawn = spars[yid], got["spars"][yid]
        at = [yard["x_m"], 0.0, deck + yard["height_m"]]
        half = yard["length_m"] / 2.0
        assert yard["parent"] == on
        assert drawn["centre"] == pytest.approx(at, abs=1e-9)
        assert drawn["a"] == pytest.approx([at[0], -half, at[2]], abs=1e-9)
        assert drawn["b"] == pytest.approx([at[0], half, at[2]], abs=1e-9)
        heel, end = got["spars"][on]["a"], got["spars"][on]["b"]
        assert heel[0] + 1.0 < at[0] < end[0]  # under its spar, not at its heel
        assert _on_the_line(heel, end, at[0]) - at[2] == pytest.approx(hang, abs=0.1)
    assert {f["id"]: f["hoist"] for f in got["drawn"]} == {yid: 1 for yid in SPRIT_YARDS}


@needs_node
def test_the_spritsail_hangs_from_its_yard_and_the_sprit_topsail_is_sheeted_to_its_arms(tmp_path):
    """Ext §6.2: the spritsail, with no yard below it, hangs from its yard as `squareCut` hangs
    any such sail, nine-tenths of its yard broad, head and foot, and its area over that deep.
    The sprit topsail's clews are at the spritsail yard's arms, at nine-tenths of it as every
    topsail's are at the yard below (within 0.1 m: Ext §6.5), and its head along its own yard:
    the trapezoid between the two yards. Each is drawn to its file's area by the heights between
    its yards within a twentieth, and its centre where the file puts the sail's force (its `x_m`
    and `centre_height_m`, within 0.1 m: the drawing against the physics)."""
    data = sprit_sails()
    got = run_js(tmp_path, data, SPRIT_FIGURES)
    sails = {s["id"]: s for s in data["graph"]["sails"]}
    yard, top_yard = got["spars"]["spritsail.yard"], got["spars"]["sprit_topsail.yard"]
    ss = got["sails"]["spritsail"]["corners"]  # larboard head, starboard head, clews
    st = got["sails"]["sprit_topsail"]["corners"]
    x, _y, z = yard["centre"]
    spread = HEAD_SPREAD * 2.0 * yard["half"]
    deep = sails["spritsail"]["area_m2"] / spread
    assert ss == [
        pytest.approx([x, -spread / 2.0, z]),
        pytest.approx([x, spread / 2.0, z]),
        pytest.approx([x, spread / 2.0, z - deep]),
        pytest.approx([x, -spread / 2.0, z - deep]),
    ]
    arm = CLEW_SPREAD * yard["half"]
    assert math.dist(st[2], [x, arm, z]) <= 0.1 and math.dist(st[3], [x, -arm, z]) <= 0.1
    for corner in st[:2]:  # the head along its own yard
        assert corner[0] == pytest.approx(top_yard["centre"][0])
        assert corner[2] == pytest.approx(top_yard["centre"][2])
    assert span(st[0], st[1]) <= 2.0 * top_yard["half"] + 1e-6
    for sid, c in (("spritsail", ss), ("sprit_topsail", st)):
        assert quad_area(c) == pytest.approx(sails[sid]["area_m2"], rel=0.05), sid
        head, foot = span(c[0], c[1]), span(c[3], c[2])
        up = (2.0 * head + foot) / (3.0 * (head + foot))  # the trapezoid's centroid, from the foot
        mid_head = [(p + q) / 2.0 for p, q in zip(c[0], c[1], strict=True)]
        mid_foot = [(p + q) / 2.0 for p, q in zip(c[3], c[2], strict=True)]
        centre = [f + up * (h - f) for f, h in zip(mid_foot, mid_head, strict=True)]
        file = [sails[sid]["x_m"], 0.0, sails[sid]["centre_height_m"]]
        assert centre == pytest.approx(file, abs=0.1), sid


SPRIT_STATES = [
    (SailState.SET, 0),
    (SailState.SET, 1),
    (SailState.SET, 2),
    (SailState.GOOSE_WINGED, 0),
    (SailState.LOOSED, 0),
    (SailState.IN_THE_GEAR, 0),
    (SailState.FURLED, 0),
]


@needs_node
@pytest.mark.parametrize("brace_deg", [0.0, 30.0, -30.0])
def test_every_sprit_sails_foot_stands_above_the_water_in_every_state(tmp_path, brace_deg):
    """Ext §6.5: upright, each sail under the bowsprit and its yard stand clear of the water in
    every state: the spritsail set, reefed once and twice, goose-winged, loosed, in the gear and
    furled, square and braced to its limit either way; the lowest point of each drawn outline,
    its belly and its foot's sag taken, above the sea."""
    states = {f"{s.value}-{r}": sprit_sails(s, r, brace_deg) for s, r in SPRIT_STATES}
    body = """
        const mine = ['spritsail.yard', 'sprit_topsail.yard', 'spritsail', 'sprit_topsail'];
        const out = {};
        Object.keys(d).forEach(k => {
          const sk = P.buildSkeleton(d[k].graph, d[k].snap);
          out[k] = sk.figures.filter(f => mine.includes(f.id)).map(f =>
            [f.id, Math.min(...(f.path ? P.flattenPath(f.path) : f.pts).map(p => p[2]))]);
        });
        return out;
    """
    got = run_js(tmp_path, states, body)
    for name, figs in got.items():
        assert {fid for fid, _low in figs} == set(SPRIT_YARDS) | set(SPRIT_SAILS), name
        for fid, low in figs:
            assert low > 0.0, (name, fid, low)


@needs_node
@pytest.mark.parametrize("brace_deg", [0.0, 30.0])
def test_the_braces_lead_up_to_the_fore_top_the_sheets_aft_and_the_lifts_to_the_spars_end(
    tmp_path, brace_deg
):
    """Ext §6.2: the braces of a yard under the bowsprit or the jib-boom lead from its arms up to
    the fore top, the fore mast's head less a metre on its raked line, a little to their own
    side, not level aft (Lavery I30). The spritsail's sheets lead from its clews aft along the
    side to the deck a metre abaft the fore mast (I30's sheave in the side), not abreast the
    clew forward of the stem; the sprit topsail's to the spritsail yard's arms, as every
    topsail's to the yard below. Their lifts, as every yard's, from the arms up to the head of
    the spar each hangs on: the bowsprit's end and the jib-boom's. The guys are not drawn."""
    data = sprit_sails(brace_deg=brace_deg)
    got = run_js(tmp_path, data, SPRIT_FIGURES)
    deck = data["graph"]["hull"]["deck_height_m"]
    beam = data["graph"]["hull"]["beam_m"]
    lines = {ln["id"]: ln["pts"] for ln in got["lines"]}
    fore_x, top_z = got["foreTop"]
    for yid, (on, _hang) in SPRIT_HANG.items():
        yard = got["spars"][yid]
        for side, s in (("starboard", 1.0), ("larboard", -1.0)):
            arm = yard["b"] if s > 0 else yard["a"]
            brace = lines[f"{yid}.brace.{side}"]
            assert brace == [pytest.approx(arm), pytest.approx([fore_x, 0.3 * s, top_z])]
            lift = lines[f"{yid}.lift.{side}"]
            assert lift == [pytest.approx(arm), pytest.approx(got["spars"][on]["b"])]
    assert top_z > got["spars"]["sprit_topsail.yard"]["centre"][2] + 5.0  # up, not level aft
    below = got["spars"]["spritsail.yard"]
    ss, st = got["sails"]["spritsail"]["corners"], got["sails"]["sprit_topsail"]["corners"]
    for side, s in (("starboard", 1.0), ("larboard", -1.0)):
        sheet = lines[f"spritsail.sheet.{side}"]
        lead = [got["foreX"] - 1.0, s * beam / 2.0, deck]
        assert sheet == [pytest.approx(ss[2] if s > 0 else ss[3]), pytest.approx(lead)]
        sheet = lines[f"sprit_topsail.sheet.{side}"]
        clew, arm = (st[2], below["b"]) if s > 0 else (st[3], below["a"])
        assert sheet == [pytest.approx(clew), pytest.approx(arm)]
    assert not [ln for ln in got["lines"] if ln["cls"] == "guy"]


@needs_node
@pytest.mark.parametrize("facing_deg", [0.0, 45.0, 90.0])
def test_a_yard_and_sail_under_the_bowsprit_are_sorted_at_their_own_middle(tmp_path, facing_deg):
    """The painter's correction for a mast's rake (package 57) sorts a yard or a sail by where
    its mast stands at its height. A yard under the bowsprit hangs from no mast, and that
    correction would carry it and its sail half its spar's run forward (4.7 m on the fixture):
    each is sorted at its own middle, a yard at its centre and a sail at its centre."""
    facing = math.radians(facing_deg)
    body = f"""
        const sk = P.buildSkeleton(d.graph, d.snap);
        const proj = P.makeProjector({facing}, 0);
        const mine = ['spritsail.yard', 'sprit_topsail.yard', 'spritsail', 'sprit_topsail'];
        const own = {{}};
        sk.figures.filter(f => mine.includes(f.id)).forEach(f => {{
          const at = f.kind === 'sail' ? f.centre : sk.spars[f.id].centre;
          own[f.id] = [f.sortAt || null, proj(at).depth];
        }});
        return P.project(sk, {facing}, 0).figures.filter(f => mine.includes(f.id))
          .map(f => [f.id, f.depth, own[f.id]]);
    """
    got = run_js(tmp_path, sprit_sails(), body)
    assert sorted(fid for fid, _depth, _own in got) == sorted(SPRIT_YARDS + SPRIT_SAILS)
    for fid, depth, (sort_at, own) in got:
        assert sort_at is None, fid
        assert depth == pytest.approx(own, abs=1e-9), fid


@needs_node
@pytest.mark.parametrize("facing_deg", [0.0, 45.0, 90.0, 135.0, 225.0])
def test_the_frame_holds_the_yards_under_the_bowsprit_across_states(tmp_path, facing_deg):
    """The fixed scale (spec M3 §9 item 14): `fullRigFrame` reaches each yard's swing about its
    slings, so every point of the yards under the bowsprit, their sails and their lines lies
    within the frame alone, upright or heeled; and the view's scale is the same on either tack,
    square or braced to the limit either way, set, in the gear or furled."""
    states = {
        f"{tack}-{brace}-{state.value}": sprit_sails(state, brace_deg=brace, tack=tack)
        for tack in ("starboard", "larboard")
        for brace in (-30.0, 0.0, 30.0)
        for state in (SailState.SET, SailState.IN_THE_GEAR, SailState.FURLED)
    }
    body = f"""
        const f = {math.radians(facing_deg)};
        const ids = ['spritsail.yard', 'sprit_topsail.yard', 'spritsail', 'sprit_topsail'];
        const mine = g => ids.includes(g.id) || ids.includes(g.of);
        const out = {{}};
        Object.keys(d).forEach(k => {{
          const sk = P.buildSkeleton(d[k].graph, d[k].snap);
          out[k] = {json.dumps(HEELS)}.map(h => {{
            const proj = P.makeProjector(f, h);
            const fr = sk.frame.map(proj);
            const xs = fr.map(p => p.x), ys = fr.map(p => p.y);
            const box = {{minX: Math.min(...xs), maxX: Math.max(...xs),
                          minY: Math.min(...ys), maxY: Math.max(...ys)}};
            let over = -1e9, n = 0;
            sk.figures.filter(mine).forEach(g => {{
              (g.path ? P.flattenPath(g.path) : g.pts).map(proj).forEach(q => {{
                over = Math.max(over, box.minX - q.x, q.x - box.maxX, box.minY - q.y,
                                q.y - box.maxY);
                n += 1;
              }});
            }});
            return {{frame: box, over: over, n: n, bounds: P.project(sk, f, h).bounds}};
          }});
        }});
        return out;
    """
    got = run_js(tmp_path, states, body)
    first = got[next(iter(got))]
    for name, views in got.items():
        for heel, view, same in zip(HEELS, views, first, strict=True):
            assert view["n"] > 10 and view["over"] <= 1e-6, (name, heel, view["over"])
            for k in ("minX", "maxX", "minY", "maxY"):
                assert view["frame"][k] == pytest.approx(same["frame"][k], abs=1e-6), (name, k)
                assert view["bounds"][k] == pytest.approx(same["bounds"][k], abs=1e-6), (name, k)


@needs_node
@pytest.mark.parametrize("path", PROFILED)
def test_on_a_hull_drawn_from_her_profile_the_yards_hang_from_the_bowsprit_as_it_stands(
    tmp_path, path
):
    """The lead's ruling of 2026-10-29: where the file gives a profile, the yards under the
    bowsprit hang from a bowsprit stood from the stem head as long as the file has it, and the
    stand-in of a heel on the datum goes. The fixture's two yards cut on her own bowsprit and
    jib-boom as they stand (`with_sprit_yards`) hang exactly as far under the drawn spars as
    they were cut, at their own stations; the spritsail's foot a metre above the water, the
    sprit topsail's clews at the spritsail yard's arms, the braces up to her fore top."""
    graph = with_sprit_yards(path)
    got = run_js(tmp_path, {"graph": graph}, SPRIT_FIGURES)
    deck = graph["hull"]["deck_height_m"]
    chain = head_chain(graph)
    for sid in ("bowsprit", "jib_boom"):
        drawn = [got["spars"][sid]["a"], got["spars"][sid]["b"]]
        assert drawn == [pytest.approx(p, abs=1e-9) for p in chain[sid]], sid
    spars = {s["id"]: s for s in graph["spars"]}
    for yid, (on, hang) in SPRIT_HANG.items():
        yard, drawn = spars[yid], got["spars"][yid]
        at = [yard["x_m"], 0.0, deck + yard["height_m"]]
        assert drawn["centre"] == pytest.approx(at, abs=1e-9)
        assert _on_the_line(*chain[on], at[0]) - at[2] == pytest.approx(hang, abs=1e-6)
    ss = got["sails"]["spritsail"]["corners"]
    assert min(p[2] for p in ss) == pytest.approx(SPRITSAIL_FOOT_ABOVE_WATER_M)
    assert min(p[2] for p in got["sails"]["spritsail"]["path"]) > 0.0
    yard = got["spars"]["spritsail.yard"]
    x, _y, z = yard["centre"]
    st = got["sails"]["sprit_topsail"]["corners"]
    arm = CLEW_SPREAD * yard["half"]
    assert math.dist(st[2], [x, arm, z]) <= 0.1 and math.dist(st[3], [x, -arm, z]) <= 0.1
    fore_x, top_z = got["foreTop"]
    brace = {ln["id"]: ln["pts"] for ln in got["lines"]}["spritsail.yard.brace.starboard"]
    assert brace[1] == pytest.approx([fore_x, 0.3, top_z])


@needs_node
@pytest.mark.parametrize("path", WITHOUT_PROFILE)
def test_without_a_profile_the_bowsprit_and_its_booms_stand_as_before(tmp_path, path):
    """A graph with no profile draws its bowsprit from its `x_m` on the datum, rising its
    `height_m`, and the booms on it from its end, as before B5.3 (`head_chain`): the eight files
    and the 64 with her profile taken away alike."""
    graph = graph_of(SIXTY_FOUR if path.startswith("the 64") else path)
    graph["hull"].pop("profile", None)
    graph["hull"].pop("stations", None)
    got = run_js(tmp_path, {"graph": graph}, SPARS_DRAWN)
    chain = head_chain(graph)
    assert chain
    for sid, (heel, end) in chain.items():
        assert got[sid] == [pytest.approx(heel, abs=1e-12), pytest.approx(end, abs=1e-12)], sid


@needs_node
def test_the_yards_under_the_bowsprit_as_the_game_serves_them(tmp_path):
    """The fixture's world through the game's own doors (`/api/ship`, `/api/state`): the graph
    serves each yard's own `x_m` and its spar, and the drawing takes them as above. As she
    starts, the sprit sails furled on their yards at their stations; then set and the yards
    braced, each yard turned about its slings by the brace the state gives, and the sprit
    topsail's clews at the spritsail yard's arms."""
    pytest.importorskip("fastapi")
    from fastapi.testclient import TestClient

    from freesail.ui.server import Driver, create_app

    path = write_ship(frigate_with_mizen_yard_doc(), tmp_path)
    scenario = Scenario(wind_from_deg=0.0, wind_speed_kn=10.0, ship_heading_deg=150.0)
    world = make_world(7, str(path), scenario)
    world.tick()
    with TestClient(create_app(Driver(world))) as client:
        start = {"graph": client.get("/api/ship").json(), "snap": client.get("/api/state").json()}
        for sid in SPRIT_SAILS:
            world.ship.sails[sid].state = SailState.SET
        for yid in SPRIT_YARDS:
            world.ship.spars[yid].brace_angle = math.radians(20.0)
        world.tick()
        braced = {"graph": client.get("/api/ship").json(), "snap": client.get("/api/state").json()}
    deck = start["graph"]["hull"]["deck_height_m"]
    spars = {s["id"]: s for s in start["graph"]["spars"]}
    for yid, (on, _hang) in SPRIT_HANG.items():
        assert spars[yid]["parent"] == on and spars[yid]["x_m"] > spars["bowsprit"]["x_m"]
    furled = run_js(tmp_path, start, SPRIT_FIGURES)
    for yid in SPRIT_YARDS:
        at = [spars[yid]["x_m"], 0.0, deck + spars[yid]["height_m"]]
        assert furled["spars"][yid]["centre"] == pytest.approx(at)
    assert {sid: s["state"] for sid, s in furled["sails"].items()} == dict.fromkeys(
        SPRIT_SAILS, "furled"
    )
    set_ = run_js(tmp_path, braced, SPRIT_FIGURES)
    angle = {s["id"]: s["brace_angle"] for s in braced["snap"]["spars"]}
    for yid in SPRIT_YARDS:
        yard, th = set_["spars"][yid], angle[yid]
        x, _y, z = yard["centre"]
        assert abs(th) > 0.1
        assert yard["centre"] == pytest.approx(furled["spars"][yid]["centre"])
        want = [x + yard["half"] * math.sin(th), yard["half"] * math.cos(th), z]
        assert yard["b"] == pytest.approx(want)
    assert {sid: s["state"] for sid, s in set_["sails"].items()} == dict.fromkeys(
        SPRIT_SAILS, "set"
    )
    below = set_["spars"]["spritsail.yard"]
    arm = [c + CLEW_SPREAD * (b - c) for c, b in zip(below["centre"], below["b"], strict=True)]
    assert math.dist(set_["sails"]["sprit_topsail"]["corners"][2], arm) <= 0.1


# ---------------------------------------------------------------------------
# Package 75 (B5.5, docs/design/Design-ShipsEngineExtensions.md §17.6): the driver of the 64 and
# the 74, on the fixture `frigate_with_driver()` (tests/rig_fixtures.py; no file carries one yet)
# ---------------------------------------------------------------------------

DRIVER = "mizzen.driver"
DRIVER_BOOM = "mizzen.boom"
GEAR_DEPTH = 0.35  # client/projection.js: IN_GEAR_DEPTH


def driver_by_the_wind(
    tack: str, sheet_deg: float = 30.0, state: SailState = SailState.SET, bent: bool = True
) -> dict:
    """`frigate_with_driver(bent)` under plain sail on `tack`, her after sail in `state` and
    sheeted `sheet_deg` off the centreline: the driver bent in the course's place, or the course
    with the driver in the sail room. The graph and snapshot."""
    ship = frigate_with_driver(bent)
    for sid in ship.groups["plain sail"]:
        if ship.sails[sid].state is not SailState.UNBENT:
            ship.sails[sid].state = SailState.SET
    after = ship.sails[DRIVER if bent else MIZEN_COURSE]
    set_sheet_angle(ship, after, math.radians(sheet_deg))
    after.state = state
    awa = math.radians(60.0) * (1.0 if tack == "starboard" else -1.0)
    return ship_state(ship, awa=awa, tack=tack)


# The mizen yard, the boom, the two after sails, the driver yard and the lines of the yard and
# the two sails, as drawn: `DRIVER_FIGURES` of one state, `DRIVER_STATES` of each of several.
DRIVER_DRAWN = """
    function drawn(g) {
      const sk = P.buildSkeleton(g.graph, g.snap);
      const y = sk.spars['mizzen.yard'], b = sk.spars['mizzen.boom'];
      const sail = id => {
        const f = sk.figures.find(x => x.kind === 'sail' && x.id === id);
        return f ? {state: f.state, corners: f.corners, path: P.flattenPath(f.path)} : null;
      };
      return {
        heel: y.a, peak: y.b, truss: y.truss, jaws: b.a, boomEnd: b.b,
        driver: sail('mizzen.driver'), course: sail('mizzen.course'),
        driverYards: sk.figures.filter(f => f.cls === 'driver_yard')
          .map(f => ({kind: f.kind, id: f.id, of: f.of, pts: f.pts})),
        lines: sk.figures.filter(f => f.kind === 'line' &&
          ['mizzen.yard', 'mizzen.course', 'mizzen.driver'].includes(f.of))
          .map(f => ({id: f.id, cls: f.cls, pts: f.pts})),
      };
    }
"""
DRIVER_FIGURES = DRIVER_DRAWN + "return drawn(d);"
DRIVER_STATES = (
    DRIVER_DRAWN
    + "const each = {}; Object.keys(d).forEach(k => { each[k] = drawn(d[k]); }); return each;"
)


def _driver_file(graph: dict) -> tuple[list, dict, float]:
    """The driver's file corners [tack, throat, peak, clew] in ship coordinates, its boom's
    entry and the deck's height."""
    deck = graph["hull"]["deck_height_m"]
    sail = next(s for s in graph["sails"] if s["id"] == DRIVER)
    boom = next(s for s in graph["spars"] if s["id"] == DRIVER_BOOM)
    return [[q[0], 0.0, deck + q[1]] for q in sail["corners_m"]], boom, deck


def _sheet_of(data: dict, sid: str) -> float:
    """The sheet's angle the snapshot gives a sail, unsigned."""
    return abs(next(s["sheet_angle"] for s in data["snap"]["sails"] if s["id"] == sid))


def _unit(a: list, b: list) -> list:
    d = [q - p for p, q in zip(a, b, strict=True)]
    n = math.hypot(*d)
    return [c / n for c in d]


def _swung_deg(p: list, q: list, origin: list, axis: list) -> float:
    """The angle between p's and q's offsets square to the line through `origin` along `axis`."""
    off_p, off_q = _off_the_line(p, origin, axis), _off_the_line(q, origin, axis)
    cos = sum(a * b for a, b in zip(off_p, off_q, strict=True)) / (
        math.hypot(*off_p) * math.hypot(*off_q)
    )
    return math.degrees(math.acos(max(-1.0, min(cos, 1.0))))


def _abaft_the_mast(graph: dict):
    """How far a point lies from the mizzen mast's raked line at its own height, level."""
    origin, axis = _mast_line(graph)
    deck = graph["hull"]["deck_height_m"]
    return lambda p: math.hypot(p[0] - (origin[0] + axis[0] / axis[2] * (p[2] - deck)), p[1])


@needs_node
@pytest.mark.parametrize("tack", ["starboard", "larboard"])
def test_the_driver_is_swung_about_the_mast_its_foot_along_its_boom(tmp_path, tack):
    """Ext §17.6: the driver in §6.1's branch for a sail cut at the mast, with its boom. Its
    throat and peak are swung whole about the mast by the sheet's angle to the sheet's side,
    each as far from the mast and from the other as the file has them. The boom is swung about
    its jaws on the mast, level, to the same side by the same angle (`sheetAngleOf` takes the
    driver bent). The tack is at the boom's jaws, within 0.1 m of the file's tack on the mast,
    and the clew along the boom at the file's foot from the jaws, to leeward."""
    data = driver_by_the_wind(tack)
    got = run_js(tmp_path, data, DRIVER_FIGURES)
    file, boom, deck = _driver_file(data["graph"])
    origin, axis = _mast_line(data["graph"])
    lee = 1.0 if tack == "larboard" else -1.0  # +1 starboard
    sheet = _sheet_of(data, DRIVER)
    assert math.degrees(sheet) == pytest.approx(30.0, abs=1e-6)
    throat, peak, clew, tack_pt = got["driver"]["corners"]
    for p, q in ((throat, file[1]), (peak, file[2])):
        off_p, off_q = _off_the_line(p, origin, axis), _off_the_line(q, origin, axis)
        assert math.hypot(*off_p) == pytest.approx(math.hypot(*off_q), abs=1e-6)
    assert math.dist(throat, peak) == pytest.approx(math.dist(file[1], file[2]), abs=1e-6)
    assert _swung_deg(peak, file[2], origin, axis) == pytest.approx(math.degrees(sheet), abs=1e-6)
    assert peak[1] * lee > 0.5  # the peak to leeward
    jaws_z = deck + boom["height_m"]
    jaws_x = origin[0] + axis[0] / axis[2] * (jaws_z - deck)
    length = boom["length_m"]
    assert got["jaws"] == [pytest.approx(jaws_x), 0.0, pytest.approx(jaws_z)]
    assert got["boomEnd"] == pytest.approx(
        [jaws_x - length * math.cos(sheet), lee * length * math.sin(sheet), jaws_z]
    )
    assert tack_pt == pytest.approx(got["jaws"]) and math.dist(tack_pt, file[0]) <= 0.1
    assert _off_the_segment(clew, got["jaws"], got["boomEnd"]) == pytest.approx(0.0, abs=1e-9)
    assert math.dist(clew, tack_pt) == pytest.approx(math.dist(file[0], file[3]), abs=1e-6)
    assert clew[1] * lee > 0.5  # the clew to leeward


@needs_node
def test_the_driver_unswung_lies_on_its_files_corners_and_takes_no_reef(tmp_path):
    """With its sheet at no angle the driver lies in the fore-and-aft plane on the file's four
    corners: the throat and the peak to the millimetre, and the tack and the clew, taken from
    the boom, within 0.1 m (Ext §17.6, §17.2's cut). No reef is drawn: a reef in the snapshot,
    which the engine never gives the driver (Steel names no band in it), moves nothing."""
    data = driver_by_the_wind("larboard")
    snap = next(s for s in data["snap"]["sails"] if s["id"] == DRIVER)
    snap["sheet_angle"] = 0.0
    got = run_js(tmp_path, data, DRIVER_FIGURES)
    file, _boom, _deck = _driver_file(data["graph"])
    drawn = [got["driver"]["corners"][i] for i in (3, 0, 1, 2)]  # tack, throat, peak, clew
    for i, (p, q) in enumerate(zip(drawn, file, strict=True)):
        assert math.dist(p, q) <= (1e-3 if i in (1, 2) else 0.1), i
    snap["reefs"] = 1
    assert run_js(tmp_path, data, DRIVER_FIGURES)["driver"] == got["driver"]


@needs_node
def test_the_head_runs_along_the_yards_line_and_on_along_the_driver_yard(tmp_path):
    """Ext §17.6, on §17.2's cut: the driver's head runs straight from the throat, at the yard's
    truss within 0.1 m, along the mizen yard's line to the sail's peak, which lies on that line
    within 0.1 m and beyond the yard's peak by what the file's head has over the course's.
    Beyond the yard's peak the head is drawn on Steel's driver yard, a spar line drawn with the
    sail (its id, of class `driver_yard`) from the yard's peak to the driver's: no more than
    two-thirds of the driver yard, whose inner part lies along the mizen yard and is drawn as
    it. Set, in the gear and furled alike; with the course bent, none."""
    states = {
        st.value: driver_by_the_wind("larboard", state=st)
        for st in (SailState.SET, SailState.IN_THE_GEAR, SailState.FURLED)
    }
    states["course"] = driver_by_the_wind("larboard", bent=False)
    got = run_js(tmp_path, states, DRIVER_STATES)
    set_ = got["set"]
    truss, ypeak = set_["truss"], set_["peak"]
    throat, peak = set_["driver"]["corners"][:2]
    assert math.dist(throat, truss) <= 0.1
    assert math.hypot(*_off_the_line(peak, truss, _unit(truss, ypeak))) <= 0.1
    file, _boom, deck = _driver_file(states["set"]["graph"])
    course, _yard, _deck = _course_and_yard(states["set"]["graph"])
    course_peak = [course["corners_m"][2][0], 0.0, deck + course["corners_m"][2][1]]
    # the truss is on the mast's line, about which both are swung: each peak as far from it as
    # in the file
    beyond = math.dist(peak, truss) - math.dist(ypeak, truss)
    assert beyond == pytest.approx(
        math.dist(file[2], truss) - math.dist(course_peak, truss), abs=1e-6
    )
    assert 0.0 < beyond <= 2.0 / 3.0 * DRIVER_YARD_M
    for name in ("set", "in_the_gear", "furled"):
        assert got[name]["driverYards"] == [
            {
                "kind": "spar",
                "id": DRIVER,
                "of": DRIVER,
                "pts": [pytest.approx(ypeak), pytest.approx(peak)],
            }
        ], name
    assert got["course"]["driverYards"] == [] and got["course"]["driver"] is None


@needs_node
@pytest.mark.parametrize("tack", ["starboard", "larboard"])
def test_the_yard_lies_on_the_courses_line_whichever_sail_is_bent(tmp_path, tack):
    """Ext §17.6, B5.2's open item: the mizen yard is laid on the course's corners, the sail cut
    at the mast that names no boom, whether the course is bent or in the sail room, and swung by
    the sheet of the sail bent on it. With the driver bent and sheeted as the course was, the
    yard stands exactly where it stood with the course, set, in the gear or furled, at any
    sheet; at no sheet, on the course's file line, its peak at the course's peak. Laid on the
    bent sail's corners (`sailOnYard`), as B5.2 had it, its after part would run out to the
    driver's peak."""
    states = {}
    for sheet in (18.0, 45.0, 85.0):
        for st in (SailState.SET, SailState.IN_THE_GEAR, SailState.FURLED):
            for bent in (True, False):
                states[f"{sheet}-{st.value}-{bent}"] = driver_by_the_wind(tack, sheet, st, bent)
    still = driver_by_the_wind(tack)
    next(s for s in still["snap"]["sails"] if s["id"] == DRIVER)["sheet_angle"] = 0.0
    states["no sheet"] = still
    got = run_js(tmp_path, states, DRIVER_STATES)
    pairs = 0
    for key, drawn in got.items():
        if not key.endswith("-True"):
            continue
        course = got[key.removesuffix("True") + "False"]
        assert drawn["driver"] is not None and drawn["course"] is None, key
        assert course["course"] is not None and course["driver"] is None, key
        for end in ("heel", "truss", "peak"):
            assert drawn[end] == pytest.approx(course[end], abs=1e-9), (key, end)
        pairs += 1
    assert pairs == 9
    sail, yard, deck = _course_and_yard(still["graph"])
    peak = sail["corners_m"][2]
    unswung = got["no sheet"]
    assert unswung["peak"] == pytest.approx([peak[0], 0.0, deck + peak[1]], abs=1e-9)
    assert unswung["heel"][1] == pytest.approx(0.0, abs=1e-12)
    assert math.dist(unswung["heel"], unswung["peak"]) == pytest.approx(yard["length_m"])


@needs_node
def test_the_boom_lies_amidships_with_the_driver_in_the_sail_room(tmp_path):
    """Ext §17.6: `sheetAngleOf` takes a lateen cut at the mast that is not unbent. With the
    driver in the sail room the boom lies amidships, level at its jaws, whatever the course's
    sheet, as a boom with no sail does, and nothing of the driver is drawn; with the driver
    bent it lies to the driver's sheet's side by its angle, set or furled."""
    states = {
        "room": driver_by_the_wind("larboard", 45.0, bent=False),
        "set": driver_by_the_wind("larboard", 45.0),
        "furled": driver_by_the_wind("larboard", 45.0, SailState.FURLED),
    }
    got = run_js(tmp_path, states, DRIVER_STATES)
    _file, boom, _deck = _driver_file(states["room"]["graph"])
    length = boom["length_m"]
    room = got["room"]
    assert math.degrees(_sheet_of(states["room"], MIZEN_COURSE)) == pytest.approx(45.0)
    assert room["boomEnd"] == pytest.approx([room["jaws"][0] - length, 0.0, room["jaws"][2]])
    assert room["course"]["state"] == "set" and room["driver"] is None
    assert not room["driverYards"]
    assert not [ln for ln in room["lines"] if ln["id"].startswith(DRIVER)]
    for name in ("set", "furled"):
        sheet = _sheet_of(states[name], DRIVER)
        assert math.degrees(sheet) == pytest.approx(45.0)
        jaws, end = got[name]["jaws"], got[name]["boomEnd"]
        assert jaws == pytest.approx(room["jaws"])
        # on the larboard tack the sheet's side is to starboard
        want = [jaws[0] - length * math.cos(sheet), length * math.sin(sheet), jaws[2]]
        assert end == pytest.approx(want), name


@needs_node
def test_the_driver_is_brailed_to_the_mast_and_furled_along_its_head(tmp_path):
    """Ext §17.6: in the gear the driver is brailed to the mast as the course is, gathered to the
    mast and up under the yard, its foot hauled up the mast and its leech in along the head by
    the gear's depth (IN_GEAR_DEPTH, 0.35); furled, it is a bundle along its whole head, the
    yard's after part and the driver yard, aloft, out to its own peak. Its one sheet is rove
    through the boom's end, its tackle to the taffrail: it is drawn from the boom's end to the
    taffrail on the centreline, set or in the gear, and furled not at all. The yard and the boom
    stay where they were."""
    states = {
        st.value: driver_by_the_wind("larboard", state=st)
        for st in (SailState.SET, SailState.IN_THE_GEAR, SailState.FURLED)
    }
    got = run_js(tmp_path, states, DRIVER_STATES)
    graph = states["set"]["graph"]
    abaft = _abaft_the_mast(graph)
    set_, gear, furled = got["set"], got["in_the_gear"], got["furled"]
    for drawn in (gear, furled):
        for end in ("heel", "truss", "peak", "jaws", "boomEnd"):
            assert drawn[end] == pytest.approx(set_[end]), end
    throat, peak, _clew, tack_pt = set_["driver"]["corners"]
    luff = throat[2] - tack_pt[2]
    assert min(p[2] for p in set_["driver"]["path"]) < throat[2] - 0.9 * luff  # set: to its foot
    assert gear["driver"]["state"] == "in_the_gear"
    for p in gear["driver"]["path"]:
        assert p[2] >= throat[2] - GEAR_DEPTH * luff - 1e-3
        assert abaft(p) <= GEAR_DEPTH * abaft(peak) + 0.8 + 1e-3
    assert furled["driver"]["state"] == "furled"
    assert max(_off_the_segment(p, throat, peak) for p in furled["driver"]["path"]) <= 0.35 + 1e-6
    # the bundle runs the head's whole length, out to the driver's peak on the driver yard, not
    # only the yard's after part as Ext §17.6 words it: the head is laced to both spars, and the
    # driver yard stays aloft while the sail is bent (judgement, B5.5). Ended at the yard's peak
    # it passed the bound above
    reach = max(math.dist(p, throat) for p in furled["driver"]["path"])
    assert reach == pytest.approx(math.dist(throat, peak), abs=1e-6)
    assert reach > math.dist(throat, set_["peak"]) + 1.0
    length = graph["hull"]["length_waterline_m"]
    deck = graph["hull"]["deck_height_m"]
    taffrail = [-0.52 * length, 0.0, 1.02 * deck]
    for drawn in (set_, gear):
        (sheet,) = [ln for ln in drawn["lines"] if ln["cls"] == "sheet"]
        assert sheet["id"] == f"{DRIVER}.sheet"
        assert sheet["pts"] == [pytest.approx(drawn["boomEnd"]), pytest.approx(taffrail)]
    assert not [ln for ln in furled["lines"] if ln["cls"] == "sheet"]  # furled: none drawn


@needs_node
@pytest.mark.parametrize("facing_deg", [0.0, 45.0, 90.0, 135.0, 225.0])
def test_the_frame_holds_the_drivers_boom_beyond_the_taffrail_across_states(tmp_path, facing_deg):
    """Ext §17.6: `fullRigFrame` holds the boom's swing, which reaches far beyond the taffrail,
    every way about its jaws (with the four directions alone the boom sheeted 45 degrees moved
    the bounds seen on the quarter, measured), and the driver's peak on its driver yard about
    the yard's truss, so every point of the yard, the boom, the two after sails, the driver yard
    and their lines lies within the frame alone, upright or heeled; and the view's scale is the
    same on either tack, at any sheet, set, in the gear or furled, with the driver bent or in
    the sail room. The frame reaches aft to the boom's end, beyond the taffrail."""
    states = {
        f"{tack}-{sheet}-{state.value}-{'driver' if bent else 'course'}": driver_by_the_wind(
            tack, sheet, state, bent
        )
        for tack in ("starboard", "larboard")
        for sheet in (18.0, 45.0, 85.0)
        for state in (SailState.SET, SailState.IN_THE_GEAR, SailState.FURLED)
        for bent in (True, False)
    }
    body = f"""
        const f = {math.radians(facing_deg)};
        const ids = ['mizzen.yard', 'mizzen.boom', 'mizzen.course', 'mizzen.driver'];
        const mine = g => ids.includes(g.id) || ids.includes(g.of);
        const out = {{}};
        Object.keys(d).forEach(k => {{
          const sk = P.buildSkeleton(d[k].graph, d[k].snap);
          const views = {json.dumps(HEELS)}.map(h => {{
            const proj = P.makeProjector(f, h);
            const fr = sk.frame.map(proj);
            const xs = fr.map(p => p.x), ys = fr.map(p => p.y);
            const box = {{minX: Math.min(...xs), maxX: Math.max(...xs),
                          minY: Math.min(...ys), maxY: Math.max(...ys)}};
            let over = -1e9, n = 0;
            sk.figures.filter(mine).forEach(g => {{
              (g.path ? P.flattenPath(g.path) : g.pts).map(proj).forEach(q => {{
                over = Math.max(over, box.minX - q.x, q.x - box.maxX, box.minY - q.y,
                                q.y - box.maxY);
                n += 1;
              }});
            }});
            return {{frame: box, over: over, n: n, bounds: P.project(sk, f, h).bounds}};
          }});
          const t = sk.spars['mizzen.yard'].truss;
          out[k] = {{views: views, aft: Math.min(...sk.frame.map(p => p[0])),
                     jaws: sk.spars['mizzen.boom'].a, truss: t,
                     reach: sk.frame.map(p => [p[2], Math.hypot(p[0] - t[0], p[1] - t[1])])}};
        }});
        return out;
    """
    got = run_js(tmp_path, states, body)
    graph = next(iter(states.values()))["graph"]
    file, boom, _deck = _driver_file(graph)
    taffrail_x = -0.52 * graph["hull"]["length_waterline_m"]
    first = got[next(iter(got))]["views"]
    for name, drawn in got.items():
        assert drawn["aft"] <= drawn["jaws"][0] - boom["length_m"] + 1e-9 < taffrail_x, name
        # the yard's own swing reaches the driver's peak, bent or not, as it reaches the
        # course's (B5.2): at the peak's height, as far from the truss as the peak
        head = math.dist(file[2], drawn["truss"])
        at_peak = [r for z, r in drawn["reach"] if abs(z - file[2][2]) < 1e-9]
        assert at_peak and max(at_peak) >= head - 1e-9, name
        for heel, view, same in zip(HEELS, drawn["views"], first, strict=True):
            assert view["n"] > 10 and view["over"] <= 1e-6, (name, heel, view["over"])
            for k in ("minX", "maxX", "minY", "maxY"):
                assert view["frame"][k] == pytest.approx(same["frame"][k], abs=1e-6), (name, k)
                assert view["bounds"][k] == pytest.approx(same["bounds"][k], abs=1e-6), (name, k)


@needs_node
def test_the_yard_stays_on_the_courses_line_as_the_mizen_is_shifted_for_the_driver_and_back(
    tmp_path,
):
    """Ext §17.6, through the engine's own shift (B3.5, `shift_sail`): with the course set and
    sheeted, "shift the mizen for the driver" and then "shift the driver for the mizen" are run
    to their ends on a bare ship, and she is drawn at each change of the two sails' states and
    sheets (nine: the course set, brailed, both unbent, the driver furled, set, brailed, both
    unbent, the course furled, set). Throughout, the yard is slung at the same truss, and its
    heel and peak lie as far from the mast and as high along it as with the course set: it
    swings with the sheet of the sail bent on it and never runs out to the driver's peak. Only
    a bent sail is drawn, never both; the boom lies amidships until the driver is bent, and
    after by the driver's sheet (on a bare ship the shift leaves it at no angle)."""
    ship = frigate_with_driver()
    runner = Runner(ship)
    awa = math.radians(-30.0)  # on the larboard bow, as test_driver.py's bare ship
    ship.dyn.apparent_wind_angle, ship.dyn.apparent_wind_speed = awa, 6.0
    light_airs = Wind(WindParams.from_nautical(0.0, 3.0, 0.0, 0.0), random.Random(0))
    course, driver = ship.sails[MIZEN_COURSE], ship.sails[DRIVER]
    course.state = SailState.SET
    set_sheet_angle(ship, course, math.radians(30.0))
    states: dict[str, dict] = {}
    seen: list[tuple] = []

    def draw_if_changed() -> None:
        key = (course.state.value, driver.state.value, course.sheet_angle, driver.sheet_angle)
        if not seen or key != seen[-1]:
            seen.append(key)
            states[f"{len(states)} {key[:2]}"] = ship_state(ship, awa=awa, tack="larboard")

    draw_if_changed()
    for text in ("shift the mizen for the driver", "shift the driver for the mizen"):
        orders.handle(ship, text)
        for _tick in range(3000):
            if not runner.in_progress():
                break
            runner.step(ship, 1.0, light_airs)
            ship.drain_notes()
            draw_if_changed()
        assert not runner.in_progress(), text
    assert course.state is SailState.SET and driver.state is SailState.UNBENT
    assert len(states) == 9, list(states)
    got = run_js(tmp_path, states, DRIVER_STATES)
    graph = next(iter(states.values()))["graph"]
    origin, axis = _mast_line(graph)
    _file, boom, _deck = _driver_file(graph)

    def place(p: list) -> tuple[float, float]:
        """How far from the mast's line, and how far along it: what a swing about it keeps."""
        along = sum((a - o) * c for a, o, c in zip(p, origin, axis, strict=True))
        return math.hypot(*_off_the_line(p, origin, axis)), along

    first = got[next(iter(got))]
    seen_bent = set()
    for name, drawn in got.items():
        sails = {s["id"]: s for s in states[name]["snap"]["sails"]}
        bent = {sid for sid in (MIZEN_COURSE, DRIVER) if sails[sid]["state"] != "unbent"}
        shown = {sid for sid, k in ((MIZEN_COURSE, "course"), (DRIVER, "driver")) if drawn[k]}
        assert shown == bent and len(bent) <= 1, name
        seen_bent.add(tuple(sorted(bent)))
        assert drawn["truss"] == pytest.approx(first["truss"], abs=1e-9), name
        for end in ("heel", "peak"):
            assert place(drawn[end]) == pytest.approx(place(first[end]), abs=1e-9), (name, end)
        swing = abs(sails[DRIVER]["sheet_angle"]) if DRIVER in bent else 0.0
        jaws = drawn["jaws"]
        want = [jaws[0] - boom["length_m"] * math.cos(swing), boom["length_m"] * math.sin(swing)]
        assert drawn["boomEnd"][:2] == pytest.approx(want, abs=1e-9), name
    # the course bent, then neither while the driver is swayed up, then the driver, and back
    assert seen_bent == {(MIZEN_COURSE,), (), (DRIVER,)}
    assert any(d["driver"] and d["driver"]["state"] == "set" for d in got.values())


@needs_node
def test_the_driver_as_the_game_serves_it_is_drawn_on_its_boom(tmp_path):
    """The bent fixture's world through the game's own doors (`/api/ship`, `/api/state`): the
    graph serves the driver's cut and its boom among its roles, and the state the course
    unbent; the drawing takes them as above. As she starts, the driver furled at no sheet: the
    yard on the course's line in the fore-and-aft plane, the boom amidships, the driver a bundle
    along its head with its driver yard beyond the yard's peak, and no sheet drawn. Set and
    sheeted, the boom and the driver lie to leeward of the tack the state gives, the yard's fore
    part to windward, and the sheet runs from the boom's end to the taffrail."""
    pytest.importorskip("fastapi")
    from fastapi.testclient import TestClient

    from freesail.ui.server import Driver, create_app

    path = write_ship(frigate_with_driver_doc(bent=True), tmp_path)
    scenario = Scenario(wind_from_deg=0.0, wind_speed_kn=10.0, ship_heading_deg=60.0)
    world = make_world(7, str(path), scenario)
    world.tick()  # her tack and her sails' states are read at a tick
    driver = world.ship.sails[DRIVER]
    with TestClient(create_app(Driver(world))) as client:
        start = {"graph": client.get("/api/ship").json(), "snap": client.get("/api/state").json()}
        driver.state = SailState.SET
        set_sheet_angle(world.ship, driver, math.radians(30.0))
        world.tick()
        sheeted = {"graph": client.get("/api/ship").json(), "snap": client.get("/api/state").json()}
    sail = next(s for s in start["graph"]["sails"] if s["id"] == DRIVER)
    assert sail["cut_at_mast"] is True and sail["roles"]["boom"] == DRIVER_BOOM
    assert {s["id"]: s["state"] for s in start["snap"]["sails"]}[MIZEN_COURSE] == "unbent"
    assert start["snap"]["ship"]["tack"] == sheeted["snap"]["ship"]["tack"] == "larboard"
    course, _yard, deck = _course_and_yard(start["graph"])
    course_peak = [course["corners_m"][2][0], 0.0, deck + course["corners_m"][2][1]]

    furled = run_js(tmp_path, start, DRIVER_FIGURES)
    assert furled["driver"]["state"] == "furled" and furled["course"] is None
    assert furled["peak"] == pytest.approx(course_peak, abs=1e-9)
    assert furled["heel"][1] == pytest.approx(0.0) and furled["boomEnd"][1] == pytest.approx(0.0)
    throat, peak = furled["driver"]["corners"][:2]
    assert max(_off_the_segment(p, throat, peak) for p in furled["driver"]["path"]) <= 0.35 + 1e-6
    (yard,) = furled["driverYards"]
    assert yard["pts"] == [pytest.approx(furled["peak"]), pytest.approx(peak)]
    assert not [ln for ln in furled["lines"] if ln["cls"] == "sheet"]

    set_ = run_js(tmp_path, sheeted, DRIVER_FIGURES)
    assert set_["driver"]["state"] == "set" and set_["truss"] == pytest.approx(furled["truss"])
    assert set_["heel"][1] < 0.0 < set_["peak"][1]  # on the larboard tack: the peak to starboard
    assert set_["boomEnd"][1] > 0.5 and set_["driver"]["corners"][2][1] > 0.5  # boom and clew
    (sheet,) = [ln["pts"] for ln in set_["lines"] if ln["cls"] == "sheet"]
    length = start["graph"]["hull"]["length_waterline_m"]
    assert sheet == [
        pytest.approx(set_["boomEnd"]),
        pytest.approx([-0.52 * length, 0.0, 1.02 * deck]),
    ]
