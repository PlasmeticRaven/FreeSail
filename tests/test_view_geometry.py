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
  and its clew along the boom, the boom swung by its sheet; its head along the mizen yard's line
  and on along Steel's driver yard; brailed to the mast and furled along its head; its sheet from
  the boom's end to the taffrail; the yard laid on the course's corners whichever sail is bent,
  through the engine's shift and back; the frame holding the boom's swing beyond the taffrail
  across states.
- Package 75 (Ext §17.11, which replaces §17.6's "the boom lies amidships"): the driver's boom
  rigged in, on the booms with the driver below, not drawn, nor its sheet, as a spare on the booms
  is not; its swing kept in the frame, so that the view does not rescale at the shift; with it
  out, or with no key on its file, everything as B5.5 drew it; through the game's own routes.
- Package 75 (the 64's stage B): each of those cases run on her own files as well as the fixture
  where it applies, the mizen's and the driver's on `sixty-four.yaml`, the yards under the
  bowsprit's on both; the sprit topsail, whose yards stand far apart fore and aft, drawn to its
  file's area along the slant between them (Ext §6.2, risk 9).
- Package 75 (the hull step's landing, SW-2 with SW-2b.2; the lead's point 10): every file on its
  own lines, the hull's cases run on all ten, a hull with no profile on an in-test document
  (`WITHOUT_PROFILE`); the parts a file rightly has none of asserted exactly
  (`RIGHTLY_WITHOUT`); a band following the side between its heights, and its face taken from
  the whole of it; the head closed to the stem; every boom's swing in the frame and its sheet to
  the taffrail, old beside new; and the painter's order of her closed body, what stands on the head
  after its plate, a face seen from inside first, the stern seen from abaft last, a bulkhead only
  from its open side.
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
import yaml
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
from freesail.api.session import attach_systems, make_ship, make_world
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
SIXTY_FOUR = "data/ships/sixty-four.yaml"  # package 75: the pilot's two files
RAZEE = "data/ships/razee-44.yaml"
PILOT = [SIXTY_FOUR, RAZEE]
MERCHANT_BRIG = "data/ships/merchant-brig.yaml"  # and the rest of the eight (SW-2, SW-2b.2)
PRIVATEER = "data/ships/privateer-schooner.yaml"
SMACK = "data/ships/smack.yaml"
EVERY_SHIP = sorted(f"data/ships/{p.name}" for p in (ROOT / "data" / "ships").glob("*.yaml"))
# the ships' boats (package 82, item 4: `boat-*.yaml`, a lug on one mast, no bowsprit and
# no gaff sail; her drawing is that package's last step)
BOATS = [p for p in EVERY_SHIP if "/boat-" in p]
# every ship carries a profile since the hull step; a ship landing joins by it
PROFILED = [p for p in EVERY_SHIP if p not in BOATS]
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


def without_profile(data: dict) -> dict:
    """A state's graph, or a graph, as no file serves it since the hull step: its hull with no
    profile and no stations, so that the viewer's branch for one stays under test on an in-test
    document, and the fixtures cut before any file had a profile stand on what they were cut on."""
    hull = (data["graph"] if "graph" in data else data)["hull"]
    hull.pop("profile", None)
    hull.pop("stations", None)
    return data


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
    staysail set beside it, the wind on the larboard bow; her profile taken away, for these cases
    read the sail off its file. On her drawn deck (the stay's foot 1.80 m to 3.94 m, on her
    quarterdeck; the tack to her rail): see
    `test_her_storm_mizzens_foot_stands_clear_of_her_drawn_deck`."""
    ship = make_ship(FRIGATE)
    ship.sails["mizzen.spanker"].state = SailState.UNBENT
    for sid in ("storm_mizzen", "mizzen.storm_staysail"):
        ship.sails[sid].state = state
        set_sheet_angle(ship, ship.sails[sid], math.radians(20.0))
    return without_profile(ship_state(ship))


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


def slant_area(c) -> float:
    """The same for a sail under the bowsprit (Ext §6.2, risk 9), whose foot lies far abaft its
    head: the mean of head and foot by the slant from the middle of the one to the other's, along
    which the sail lies. A spritsail, hanging straight down, has the same area either way."""
    head, foot = span(c[0], c[1]), span(c[3], c[2])
    mid_head = [(p + q) / 2.0 for p, q in zip(c[0], c[1], strict=True)]
    mid_foot = [(p + q) / 2.0 for p, q in zip(c[3], c[2], strict=True)]
    return (head + foot) / 2.0 * math.dist(mid_head, mid_foot)


def all_square(path: str, state: SailState = SailState.SET):
    ship = make_ship(path)
    for s in ship.sails.values():
        if s.cls == "square":
            s.state = state
    return ship


@needs_node
@pytest.mark.parametrize("path", [FRIGATE, SCHOONER, CUTTER, BRIG, SIXTY_FOUR, RAZEE])
def test_every_square_sail_is_drawn_to_its_files_area_between_its_yards(tmp_path, path):
    """Set, braced square, every square sail's drawn area is the file's within a twentieth,
    its head within its yard and at the yard's height, and a sail with a yard below it
    reaches that yard: no sail falls short of the one below or overlaps it (the viewer drew
    a course a tenth short and a topgallant a sixth too deep). A sail under the bowsprit by the
    slant between its yards (`slant_area`), every other by the heights."""
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
        yard = yards[sail["roles"]["yard"]]
        area = slant_area(c) if yard["parent"] in ("bowsprit", "jib_boom") else quad_area(c)
        assert area == pytest.approx(sail["area_m2"], rel=0.05), sail["id"]
        assert span(c[0], c[1]) <= yard["length_m"] + 1e-6
        assert c[0][2] == pytest.approx(got["yards"][yard["id"]]["z"])
    pairs = (
        ("fore.topgallant", "fore.topsail.yard"),
        ("main.royal", "main.topgallant.yard"),
        ("topgallant", "topsail.yard"),
        ("topsail", "square_sail.yard"),
        ("sprit_topsail", "spritsail.yard"),
    )
    for sail, below in pairs:
        if sail in got["sails"] and below in got["yards"]:
            assert got["sails"][sail][3][2] == pytest.approx(got["yards"][below]["z"]), sail


@needs_node
def test_a_sail_on_a_raked_mast_keeps_the_heights_between_its_yards(tmp_path):
    """The slant between two yards is a sprit topsail's alone (Ext §6.2, risk 9), keyed on a yard
    under the bowsprit. A mast raked far enough to tell the two apart (half a radian, the slant
    a seventh over the heights) cuts its upper sails by the heights as ever: each drawn to its
    file's area by the heights within a twentieth, which the slant's cut would leave an eighth
    short."""
    ship = all_square(FRIGATE)
    for s in ship.spars.values():
        if s.is_yard:
            s.brace_angle = 0.0
    data = ship_state(ship)
    next(s for s in data["graph"]["spars"] if s["id"] == "fore.mast")["rake"] = 0.5
    got = run_js(tmp_path, data, SQUARE)
    sails = {s["id"]: s for s in data["graph"]["sails"]}
    for sid in ("fore.topgallant", "fore.royal"):
        c = got["sails"][sid]
        assert quad_area(c) == pytest.approx(sails[sid]["area_m2"], rel=0.05), sid
        assert slant_area(c) > 1.1 * quad_area(c), sid  # the two readings are told apart here


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
# B5.1's stations on the pilot's two files, where they were built and pinned; the eight are served
# from the day they carry a profile, and that builder is kept for a graph that serves none
DRAWN_BY = [(p, "served") for p in PROFILED] + [(p, "profile") for p in PILOT]


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
@pytest.mark.parametrize(("path", "builder"), DRAWN_BY)
def test_the_sides_top_runs_through_every_rail_point_and_the_head_rule(tmp_path, path, builder):
    """The top of the drawn side passes through every point of `rail_m` within a millimetre;
    forward of the rail's end, where it ends abaft the stem head, it runs straight to the stem head
    (the head rule), and the stem head is the side's foremost top. Each station's top is a corner
    of the side's strips."""
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
    assert hx >= rx  # her rail ends at the stem head (the schooners') or abaft it, at a bulkhead
    for x, z, _on in got:
        if x > rx:
            assert z == pytest.approx(rz + (hz - rz) * (x - rx) / (hx - rx), abs=0.001), x
        elif x >= profile["rail_m"][0][0]:
            assert z == pytest.approx(interp(profile["rail_m"], x), abs=0.001), x
    assert max(x for x, _z, _on in got) == pytest.approx(hx, abs=1e-6)


@needs_node
@pytest.mark.parametrize(("path", "builder"), [d for d in DRAWN_BY if d[0] != LUGGER])
def test_the_transom_runs_from_the_knuckle_to_the_taffrail(tmp_path, path, builder):
    """Every stern with a transom; the lugger's is round (`RIGHTLY_WITHOUT`)."""
    hull = hull_of(path, builder)
    profile = hull["profile"]
    got = run_js(
        tmp_path,
        {"hull": hull},
        "return P.hullFigures(d.hull).filter(f => f.part === 'transom').map(f => f.pts);",
    )
    pts = [p for face in got for p in face]
    top = max(pts, key=lambda p: p[2])
    taffrail = profile["stern_m"][-1]  # the rail's after end but on the cutter, 0.28 m abaft it
    assert top[0] == pytest.approx(taffrail[0], abs=0.001)
    assert top[2] == pytest.approx(taffrail[1], abs=0.001)
    knuckle = profile["form"]["stern"]["knuckle_z_m"]
    assert min(p[2] for p in pts) == pytest.approx(knuckle, abs=0.001)
    # across the stern, alike on both sides
    widest = max(p[1] for p in pts)
    assert widest > 0.5 and min(p[1] for p in pts) == pytest.approx(-widest, abs=1e-9)


@needs_node
@pytest.mark.parametrize(("path", "builder"), DRAWN_BY)
def test_each_deck_is_drawn_at_its_points_over_its_extent(tmp_path, path, builder):
    """Each deck at its own heights over its extent: on B5.1's stations inside the rail, at
    0.95 of its half-breadth or less; on the served ones (B5.6, §6) at 0.95 of the drawn side's
    half-breadth at the deck's height (freesail/ship/form.py's, within 5 mm: the stations are
    served to the millimetre). Abaft and forward of her regular stations, among the end stations,
    the strips stand on those stations' own heights where form.py's `half_breadth_at` runs straight
    to the stern's or the stem's line (the smack's after deck end at x -6.19, 0.56 m against 0.46
    m): there the deck is held to the strips, within the beam."""
    hull = hull_of(path, builder)
    profile = hull["profile"]
    spec = make_ship(path).hull.spec
    rail_hb = [(p[0], p[2]) for p in profile["breadth_m"]]
    regular = [b[0] for b in profile["breadth_m"]] + [s[0] for s in profile.get("sections_m", [])]
    regular += [b[0] for b in profile.get("breadth_line_m", [])]
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
            elif min(regular) <= x <= max(regular):
                side = form.half_breadth_at(spec, x, z)
                assert abs(y) == pytest.approx(0.95 * side, abs=0.005), (word, x, z)
            else:
                assert abs(y) <= 0.95 * 0.5 * hull["beam_m"], (word, x, z)
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
    assert masts
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


# How far forward of B5.1's the end of each file's bowsprit is drawn since B5.3, metres (the 64's
# 36.169 -> 37.173, the razee's 36.154 -> 37.095; their jib-booms' ends with them), and its steeve
# from the stem head, degrees (hers, 27: Indf §3.5 item 9). The eight's measured at the hull step's
# landing: no spar of theirs moved in the file, the heel moved to the stem head (the frigate's
# 30.339 -> 33.283, 16.86 degrees where the 36's bowsprit had stood from its `x_m` on the datum).
# The cutter's, the lugger's and the smack's lie level at the rail, their ends' filed heights under
# it (2.10 against 2.48 m, 2.50 against 2.83 m, 1.75 against 2.60 m); the smack's end falls 0.17 m
# short of the old one for it.
BOWSPRIT_DRAWN = {
    SIXTY_FOUR: (1.004, 27.05),
    RAZEE: (0.941, 27.77),
    FRIGATE: (2.944, 16.86),
    BRIG: (2.594, 17.53),
    MERCHANT_BRIG: (2.594, 17.53),
    CUTTER: (0.925, 0.0),
    LUGGER: (0.466, 0.0),
    SMACK: (-0.170, 0.0),
    SCHOONER: (2.833, 19.98),
    PRIVATEER: (2.833, 19.98),
}


@needs_node
@pytest.mark.parametrize("path", PROFILED)
def test_the_bowsprit_stands_from_the_stem_head_its_length_up_to_its_ends_height(tmp_path, path):
    """Indf §12.3: the heel at the stem head, or the rail there if that is lower (the razee's).
    B5.3 (the lead's ruling of 2026-10-29, Ext §6.2): the whole spar from there, as long as the
    file has it, up to its end's height above the datum, so that the yards under it hang from a
    bowsprit that stands where the file has it; the jib-boom from its end, as before.

    Old beside new: B5.1 drew the heel there and kept the end where a heel on the datum put it,
    `x_m` + sqrt(L^2 - min(H, 0.95 L)^2) forward at deck + H, so that the drawn spar fell short
    of the file's length; its end now stands at the same height the file's length farther forward
    (BOWSPRIT_END_FORWARD_OF_B5_1). Her stage B laid the file's root on the stem head (x_m 24.63
    to 25.15, length 14.1 to 13.5 m), so the drawn steeve is her 27 degrees with no viewer change
    (it was 32.8 on the 64 with the root at the knighthead's cap), the razee's 27.8, her heel
    lowered 0.12 m to her rail; and the end's move from B5.1's rule falls with it, 1.773 to 1.004
    m on the 64, 1.692 to 0.941 on the razee. The eight's, `BOWSPRIT_DRAWN`."""
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
    assert tip[1] == 0.0 and tip[2] == pytest.approx(max(deck + height, heel[2]))
    assert tip[0] > heel[0]
    # old (B5.1) beside new
    rise = min(height, 0.95 * length)
    old_tip = [bowsprit["x_m"] + math.sqrt(length * length - rise * rise), 0.0, deck + rise]
    forward, drawn_steeve = BOWSPRIT_DRAWN[path]
    assert tip[0] - old_tip[0] == pytest.approx(forward, abs=0.001)
    steeve = math.degrees(math.atan2(tip[2] - heel[2], tip[0] - heel[0]))
    assert steeve == pytest.approx(drawn_steeve, abs=0.01)
    # the jib-boom from the bowsprit's end, its length up to its own end's height
    for jib_boom in [s for s in graph["spars"] if s["class"] == "jib_boom"]:
        jib_heel, jib_end = got[jib_boom["id"]]
        assert jib_heel == pytest.approx(tip)
        assert math.dist(jib_heel, jib_end) == pytest.approx(jib_boom["length_m"])
        assert jib_end[2] == pytest.approx(deck + jib_boom["height_m"])
    if path == RAZEE:
        assert heel[2] < hz  # her rail at the stem head stands below the stem head


BARE = " with her profile taken away"
# No file comes without a profile since the hull step: each file's graph, in the test
WITHOUT_PROFILE = [f"{p}{BARE}" for p in PROFILED]


def graph_of_case(case: str) -> dict:
    """The file's served graph, or, for a case of `WITHOUT_PROFILE`, that with no profile."""
    if case.endswith(BARE):
        return without_profile(graph_of(case.removesuffix(BARE)))
    return graph_of(case)


@needs_node
@pytest.mark.parametrize("case", WITHOUT_PROFILE)
def test_a_graph_with_no_profile_is_drawn_as_before_point_for_point(tmp_path, case):
    """A graph with no profile, on an in-test document since every file carries one
    (Build-Ships.md §2.6, the landing of SW-2 with SW-2b.2): its hull, masts' feet and bowsprit
    are drawn as they were before package 75."""
    graph = graph_of_case(case)
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
@pytest.mark.parametrize(("path", "builder"), DRAWN_BY)
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
    # the schooners' rail runs to the stem head: seen ahead, no station stands forward of its end
    no_bow_to_close = hull["profile"]["rail_m"][-1][0] >= hull["profile"]["stem_m"][-1][0] - 1e-6
    for view, seen in got.items():
        assert seen["samples"] > 1000, view
        assert seen["ends"] > 100 or (view == "ahead" and no_bow_to_close), view
        assert seen["n"] == 0, (view, seen["hollow"])
        assert seen["nOpen"] == 0, (view, seen["open"])
        assert seen["widest"] == pytest.approx(greatest, abs=0.01), view


@needs_node
@pytest.mark.parametrize(("path", "builder"), DRAWN_BY)
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
    # the stem head, or the stem's fore edge where it stands forward of its head (the lugger's)
    assert max(x for x, _z in above) == pytest.approx(max(q[0] for q in stem), abs=1e-6)


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


# The exact files that rightly have none of a part, each read (the lead's point 10, 2026-10-31, the
# guard turned and not loosened: Build-Ships.md §5.7, and each file's `hull.profile`). Every other
# file must draw the part, a ship landing among them: she joins a set here only by her own lines.
# Galleries and lights: seven have none (§5.7's brig "no galleries or lights"; the cutter's and the
# smack's counters, the lugger's round stern and the schooners' plain transoms as their sheets draw
# them). The head: the cutter, the smack and the lugger (§5.7's "no head"; the note's "the cutter,
# the smack" with the lugger read beside them). No transom on the lugger's round stern; no wale on
# the schooners' plate; no ports cut in the side, so no band, on the lugger and the smack.
NO_GALLERY_OR_LIGHT = {BRIG, MERCHANT_BRIG, CUTTER, LUGGER, SMACK, SCHOONER, PRIVATEER}
# a ship's boat (package 82: her drawing by rule) has no gallery, no stern light, no head
# and no ports, a square transom and a rubbing strake for her wale
RIGHTLY_WITHOUT = {
    "gallery": NO_GALLERY_OR_LIGHT | set(BOATS),
    "light": NO_GALLERY_OR_LIGHT | set(BOATS),
    "head": {CUTTER, LUGGER, SMACK} | set(BOATS),
    "transom": {LUGGER},
    "wale": {SCHOONER, PRIVATEER},
    "band": {LUGGER, SMACK} | set(BOATS),
}
GALLERIED = [p for p in PROFILED if p not in RIGHTLY_WITHOUT["gallery"]]
LIT = [p for p in PROFILED if p not in RIGHTLY_WITHOUT["light"]]
HEADED = [p for p in PROFILED if p not in RIGHTLY_WITHOUT["head"]]
TRANSOMED = [p for p in PROFILED if p not in RIGHTLY_WITHOUT["transom"]]


def parts_filed(profile: dict) -> set[str]:
    """Which of `RIGHTLY_WITHOUT`'s parts a profile files the keys for."""
    stern = profile["form"]["stern"]
    filed = set()
    if stern.get("galleries_m"):
        filed.add("gallery")
    if stern.get("lights_m"):
        filed.add("light")
    if profile.get("head_m"):
        filed.add("head")
    if stern["type"] != "round":
        filed.add("transom")
    if profile.get("wales_m") or profile.get("channel_wales_m"):
        filed.add("wale")
    return filed


@needs_node
@pytest.mark.parametrize(
    ("path", "builder"),
    [(p, "served") for p in EVERY_SHIP] + [(p, "profile") for p in PROFILED],
)
def test_every_file_draws_a_closed_hull_with_no_nan(tmp_path, path, builder):
    """Every file's hull: no coordinate that is not a number, every filled figure a polygon, each
    side's outline one closed line, the rail along the top, the stem, the low edge and the stern;
    and on the served stations (B5.6) exactly the parts it should draw. The case that demanded
    gallery, light and head parts of every profiled file is turned, not loosened: `RIGHTLY_WITHOUT`
    names the exact files that have none of each, and every other file must draw it, both ways
    round, and the file's own keys must say the same."""
    hull = graph_of(path)["hull"]
    if builder == "profile":
        del hull["stations"]
    got = run_js(tmp_path, {"hull": hull}, CLOSED)
    assert got["finite"] and got["fewest"] >= 3
    if "profile" not in hull:  # a ship's boat, her drawing being package 82's last step
        assert path in BOATS and got["n"] == 4 and got["parts"] == ["deck", "side", "transom"]
        return
    drawn = set(got["parts"])
    assert drawn >= {"side", "outline", "deck", "bottom"}
    if builder == "served":
        filed = parts_filed(hull["profile"])
        for part, files in RIGHTLY_WITHOUT.items():
            assert (part in drawn) == (path not in files), part
            if part != "band":  # a band is the viewer's reading of the ports, not a key of its own
                assert (part in filed) == (path not in files), part
    for side, loop in got["loops"].items():
        assert loop["vertices"] > 20, side
        assert loop["odd"] == 0 and loop["reached"] == loop["vertices"], (side, loop)


def test_the_sets_of_files_with_no_part_name_files_that_exist():
    """A set of `RIGHTLY_WITHOUT` stays exact: no stale name in it, and a ship landing is demanded
    every part until her own lines put her in a set."""
    for part, files in RIGHTLY_WITHOUT.items():
        assert files <= set(EVERY_SHIP), part
        assert files, part
    assert set(PILOT) <= set(EVERY_SHIP) - set().union(*RIGHTLY_WITHOUT.values())


@needs_node
@pytest.mark.parametrize("case", WITHOUT_PROFILE)
def test_a_graph_with_no_profile_draws_its_lens_with_no_nan(tmp_path, case):
    """With no profile (`WITHOUT_PROFILE`, in the test) the hull is the four faces of the lens."""
    got = run_js(tmp_path, {"hull": graph_of_case(case)["hull"]}, CLOSED)
    assert got["finite"] and got["fewest"] >= 3
    assert got["n"] == 4 and got["parts"] == ["deck", "side", "transom"]


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
@pytest.mark.parametrize("path", TRANSOMED)
def test_the_transom_stands_at_the_taffrail_and_transom_hb_m_its_foot_rounded_up(tmp_path, path):
    """A square or raked stern's transom (§6): its top across the taffrail (`stern_m`'s top) at
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
    assert stern["type"] in ("square", "raked")
    zk, (hb_top, hb_knuckle) = stern["knuckle_z_m"], stern["transom_hb_m"]
    rise = stern["round_up_m"]
    assert rise > 0.05  # the 64's 4 in, the cutter's 0.07 m
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
@pytest.mark.parametrize("path", GALLERIED)
def test_each_gallery_and_band_of_lights_lies_at_its_place(tmp_path, path):
    """§6, §5.0 principle 9: each tier of `galleries_m` a plain box on each quarter at its extent
    and heights within a centimetre, its inner edges on the drawn side where the side stands
    there and its outer face GALLERY_OUT_M beyond it; each band of `lights_m` n plain marks at its
    heights within a centimetre, in n even bays within its half-breadth, each the light's share
    of its bay, on the transom (the stern's line at its height). Nothing stands off the hull: a
    tier is cut to the top of the side over its extent and to the stern's line at its heights, a
    band to the transom's knuckle and taffrail. The 64's and the razee's are drawn as filed: the
    razee's stand under her taffrail since her short roundhouse is in her profile (Build-Ships.md
    §19.1 item 18), where before it they were cut to her side and her transom. The frigate's tier,
    filed from x -23.99, is cut at its foot to her stern's line there."""
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
    # the razee's roundhouse in (B1, 2026-10-29): nothing cut on her two; the frigate's foot is
    assert cut == (path == FRIGATE)
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
@pytest.mark.parametrize("path", HEADED)
def test_the_head_lies_on_head_m(tmp_path, path):
    """§6: the knee of the head, HEAD_SIDING_M each side of the middle line (judgement, 0.2 m):
    each of its two sides `head_m`'s points within a millimetre, and `stem_m`'s under them where the
    knee leaves the stem above the water, from the foot of the stem's closure up to the head's top,
    then back to the stem head and down `stem_m`, seen only from its own side; its fore edge in
    strips across it on `head_m` up to the shape's foot; its back in strips across it on `stem_m`.
    At its top, what `form.head` stands there, a plain shape the head's share tall, its top the
    head's, its front on `head_m`: its two sides, and its face across the ship at its middle. Seen
    ahead or astern the head is a strip with the shape on it, not a hairline.

    Old beside new, the mends of the landing. The foot: 0.8 m down on every file, which stood under
    the low line where that reaches the stem higher, the brigs' at -0.44 m, the frigate's at -0.52
    m; the 64's and the razee's unmoved. The schooners' knee, whose top stands 0.85 m under the stem
    head: a wedge filled straight back to the stem head, and its foot starting in the air 0.52 m
    above the water, a step 0.4 m across; now level back to the stem at its top, and on down the
    stem. The back: none, and sky between the block and the stem from abaft the beam (below)."""
    hull = graph_of(path)["hull"]
    profile = hull["profile"]
    knee, stem = profile["head_m"], profile["stem_m"]
    word = profile["form"]["head"]
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
                floor: P.formHull(d.hull).fore.low[1],
                head: heads.map(f => ({cls: f.cls || 'knee', side: f.side || null,
                                       outward: f.outward || null, pts: f.pts}))};
        """,
    )
    s = got["siding"]
    assert s == 0.2
    floor = got["floor"]
    assert floor == pytest.approx(hull["stations"][-1][0][1] if floor > -0.8 else -0.8)
    line = [q for q in stem if q[1] < knee[0][1] - 1e-9] + knee
    front = [(x_at_height(line, floor), floor)] + [(x, z) for x, z in line if z > floor + 1e-9]
    top = knee[-1][1]
    back = [(x_at_height(stem, floor), floor)] + [(x, z) for x, z in stem if z > floor + 1e-9]
    if top < stem[-1][1]:  # the schooners': level back from the knee's top, and nothing above it
        back = [(x, z) for x, z in back if z < top - 1e-9] + [(x_at_height(stem, top), top)]
        assert max(q[2] for h in got["head"] for q in h["pts"]) == pytest.approx(top, abs=1e-9)
    tall = got["share"] * top
    across, high, half = {
        "figure": (tall / 2, tall, tall / 4),
        "scroll": (tall / 3, tall / 3, s),
    }.get(word, (0.0, 0.0, s))
    shaped = word in ("figure", "scroll")
    foot = top - high
    for side, sign in (("starboard", 1), ("larboard", -1)):
        (plate,) = [h for h in got["head"] if h["cls"] == "knee" and h["side"] == side]
        assert plate["outward"] == [0, sign, 0]
        want = front + back[::-1]
        assert len(plate["pts"]) == len(want)
        for q, (x, z) in zip(plate["pts"], want, strict=True):
            assert q == pytest.approx([x, sign * s, z], abs=0.001)
        if not shaped:
            continue
        (shape,) = [h for h in got["head"] if h["cls"] == word and h["side"] == side]
        assert shape["outward"] == [0, sign, 0]
        assert max(q[2] for q in shape["pts"]) == pytest.approx(top, abs=0.001)
        assert min(q[2] for q in shape["pts"]) == pytest.approx(foot, abs=0.001)
        front_x = max(q[0] for q in shape["pts"])
        assert front_x == pytest.approx(x_at_height(knee, top - high / 2), abs=0.001)
        assert front_x - min(q[0] for q in shape["pts"]) == pytest.approx(across, abs=0.001)
        assert all(q[1] == pytest.approx(sign * half) for q in shape["pts"])
    if shaped:
        (face,) = [h for h in got["head"] if h["cls"] == word and h["side"] is None]
        assert max(q[1] for q in face["pts"]) == pytest.approx(half, abs=0.001)
        middle = x_at_height(knee, top - high / 2) - across / 2
        assert all(q[0] == pytest.approx(middle, abs=0.001) for q in face["pts"])

    def strips(cls: str, line: list) -> None:
        drawn = [h["pts"] for h in got["head"] if h["cls"] == cls]
        assert len(drawn) == len(line) - 1, cls
        for strip, (a, b) in zip(drawn, zip(line, line[1:], strict=False), strict=True):
            want = [[a[0], -s, a[1]], [b[0], -s, b[1]], [b[0], s, b[1]], [a[0], s, a[1]]]
            assert flat_pts(strip) == pytest.approx(flat_pts(want), abs=0.001), cls

    on_knee = [(x, z) for x, z in front if z <= foot + 1e-9]
    if shaped and on_knee[-1][1] < foot - 1e-9:
        on_knee.append((x_at_height(knee, foot), foot))
    if not shaped:
        on_knee.append(back[-1])
    strips("strip", on_knee)
    strips("strip back", back)
    # seen ahead and astern: the knee's breadth at least, the shape's at the most
    for breadth in got["seen"]:
        assert 2 * s - 1e-6 <= breadth <= 2 * half + 1e-6


@needs_node
@pytest.mark.parametrize("path", HEADED)
def test_no_sky_shows_between_the_head_and_the_stem_from_abaft_the_beam(tmp_path, path):
    """The block's sides stand off the stem by HEAD_SIDING_M. Seen from abaft the beam, with no back
    to it, the sky showed between the near side and the stem: old, a sliver up to 0.09 m2 at 105
    degrees on the 64, 0.09 m2 at 135 on the schooners, 0.03 m2 on the frigate and the brigs, 0.02
    m2 on the razee (measured at 15-degree steps, the hull's figures alone). Now every point across
    that gap, up the stem from the water to the knee's top, is inside a drawn figure."""
    hull = graph_of(path)["hull"]
    profile = hull["profile"]
    top = min(profile["head_m"][-1][1], profile["stem_m"][-1][1])
    samples = [
        [x_at_height(profile["stem_m"], z), z]
        for z in (0.05 + (top - 0.1) * i / 24.0 for i in range(25))
    ]
    got = run_js(
        tmp_path,
        {"hull": hull, "samples": samples},
        """
        const figs = P.hullFigures(d.hull).filter(f => f.part !== 'outline');
        const sk = {figures: figs.map(f => Object.assign({kind: 'hull'}, f))};
        function winding(pt, poly) {
          let w = 0;
          for (let i = 0; i < poly.length; i++) {
            const a = poly[i], b = poly[(i + 1) % poly.length];
            const c = (b.x - a.x) * (pt.y - a.y) - (pt.x - a.x) * (b.y - a.y);
            if (a.y <= pt.y) { if (b.y > pt.y && c > 0) w++; }
            else if (b.y <= pt.y && c < 0) w--;
          }
          return w;
        }
        const open = [];
        [105, 120, 135, 150, 210, 225, 240, 255].forEach(deg => {
          const f = deg * Math.PI / 180, sign = deg < 180 ? 1 : -1;
          const proj = P.makeProjector(f, 0);
          const drawn = P.project(sk, f, 0).figures;
          d.samples.forEach(([x, z]) => {
            const pt = proj([x, sign * 0.1, z]);
            if (!drawn.some(g => winding(pt, g.pts) !== 0)) open.push([deg, x, z]);
          });
        });
        return open;
        """,
    )
    assert got == []


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
    # the 64's 2.4 m; the smack's the least, 0.8 m, her half-breadth's a little under it
    assert deepest == pytest.approx(max(0.8, widest * math.tan(UNDERWATER_HEEL)), abs=0.005)
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
    the mast was. The lugger's mizen is stepped abaft her deck's after end (x -8.70 against -8.27),
    on the deck's height held there, and so stands on no drawn strip of it; her round stern is so
    narrow there that heeled 20 and 30 degrees toward the viewer its foot comes nearer than her near
    side, 0.22 m at 20 degrees, and is drawn over it: recorded, for the owner's eye."""
    graph = graph_of(path)
    profile = graph["hull"]["profile"]
    got = run_js(tmp_path, {"graph": graph}, FOOT_SORTED)
    assert {g["id"] for g in got} == {s["id"] for s in graph["spars"] if s["class"] == "mast"}
    for g in got:
        where = (g["id"], g["view"])
        assert g["near"] and g["far"], where
        narrow = (path, g["id"]) == (LUGGER, "mizen.mast") and g["view"] in (
            "heeled 20 toward",
            "heeled 30 toward",
        )
        if not narrow:
            assert max(g["near"]) < g["foot"] - 1e-3, where  # the near side painted over it
        assert min(g["far"]) > g["foot"] + 1e-3, where
        if (path, g["id"]) != (LUGGER, "mizen.mast"):
            assert g["decks"] and min(g["decks"]) > g["foot"] + 1e-3, where  # it stands on its deck
        cut, sort_at, foot, head = g["rest"]
        assert cut[2] == pytest.approx(g["top"])
        assert cut[2] == pytest.approx(interp(profile["rail_m"], foot[0]), abs=1e-6)
        assert sort_at == pytest.approx([(foot[i] + head[i]) / 2 for i in range(3)])


@needs_node
@pytest.mark.parametrize("path", [p for p in PROFILED if p != LUGGER])
def test_the_head_and_the_galleries_stay_inside_the_fixed_frame_across_states(tmp_path, path):
    """The fixed frame (spec M3 §9 item 14) holds the hull as drawn: furled, under plain sail,
    and with the topgallant masts sent down, the bounds are the same in each view, and the head,
    the galleries and the lights stand inside them, where the file has any. (Braced to their
    limits, the 64's yards move the frame on the quarter at 135 degrees, in the viewer before
    package 75 too: the rig's, not the hull's. So on the lugger, with no head and no gallery, whose
    topsail's hoist moves her bounds 0.78 m set against furled, on her lines or with no profile
    alike: left out here.)"""
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
            assert state["outside"] == 0
            assert (state["parts"] > 0) == (path not in RIGHTLY_WITHOUT["head"])


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
@pytest.mark.parametrize("case", [*PROFILED, f"{FRIGATE}{BARE}"])
def test_the_hull_below_the_water_is_drawn_three_ways_hidden_by_default(tmp_path, case):
    """§6, §19.1 item 16 (the owner's, on the sheets): `project`'s `underwater` draws a hull with a
    profile below the water hidden by the sea (UNDERWATER, proposed, the default: nothing of it
    under the sea line), faint (the part under the line marked `under`, all of it there), or
    solid (as its strips stand, down to the drawn depth); upright and heeled, the bounds the same
    three ways. A hull with no profile is drawn as before whichever is asked."""
    graph = graph_of_case(case)
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
        # drawn down 2.45 m on the 64, and 0.8 m at the least
        assert ways["solid"]["nUnder"] == 0 and ways["solid"]["overMax"] > 0.75


@needs_node
@pytest.mark.parametrize("path", LIT)
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
@pytest.mark.parametrize(("path", "builder"), DRAWN_BY)
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


# Each file's tiers cut in the side, each port's middle below the rail: the frigate's forecastle
# ports stand 0.31 m over it, and the lugger and the smack file no ports
TIERS_IN_THE_SIDE = {
    SIXTY_FOUR: {"lower", "upper", "quarterdeck"},
    RAZEE: {"upper", "quarterdeck", "forecastle"},
    FRIGATE: {"upper", "quarterdeck"},
    BRIG: {"upper"},
    MERCHANT_BRIG: {"upper"},
    CUTTER: {"upper"},
    LUGGER: set(),
    SMACK: set(),
    SCHOONER: {"upper"},
    PRIVATEER: {"upper"},
}


@needs_node
@pytest.mark.parametrize(("path", "builder"), DRAWN_BY)
def test_each_tier_of_ports_cut_in_the_side_is_drawn_as_a_band(tmp_path, path, builder):
    """§6's port bands (PORT_BANDS, the owner's to keep): a deck's strake of ports is drawn where
    its ports are cut in the side, each port's middle below the rail; not where the guns fire over
    the rail. The 64's lower, upper and quarterdeck tiers (1407F cuts all three in her side; her
    foremost quarterdeck port reaches 2 cm over the rail), none for her forecastle's and
    roundhouse's carronades, whose middles stand 0.3 m over it; the razee's three; the eight's as
    their files have them (`TIERS_IN_THE_SIDE`)."""
    hull = hull_of(path, builder)
    profile = hull["profile"]
    got = run_js(tmp_path, {"hull": hull, "parts": ["band"]}, FACES_SEEN)
    drawn = {f["deck"] for f in got["hull"]}
    want = TIERS_IN_THE_SIDE[path]
    assert drawn == want
    for word, ports in (profile.get("ports_m") or {}).items():
        depth = profile["port_size_m"][word][1]
        over = [z + depth / 2 - interp(profile["rail_m"], x) for x, z, _hb in ports]
        assert (max(over) <= 0.0) == (word in want), (word, max(over))


# How far inside the drawn side the straight chord between a band's two heights stood at its worst,
# metres, read at each end from the band's own corners: what drew the comb along the wale and the
# port bands from ahead and astern, plainest on the frigate-36
CHORD_OFF_THE_SIDE_M = {
    FRIGATE: 0.613,
    RAZEE: 0.109,
    BRIG: 0.101,
    MERCHANT_BRIG: 0.101,
    SIXTY_FOUR: 0.095,
    CUTTER: 0.030,
    SMACK: 0.017,
    SCHOONER: 0.009,
    PRIVATEER: 0.009,
    LUGGER: 0.005,
}
BANDS = """
    const H = P.formHull(d.hull);
    return P.hullFigures(d.hull).filter(f => f.part === 'wale' || f.part === 'band').map(f => {
      const n = f.pts.length;
      const y = p => Math.abs(p[1]);
      let off = 0;
      // along each of the polygon's two ends, between its corners there
      for (let i = 0; i < n; i++) {
        const a = f.pts[i], b = f.pts[(i + 1) % n];
        if (Math.abs(a[0] - b[0]) > 1e-9) continue;
        for (let k = 1; k < 8; k++) {
          const t = k / 8, z = a[2] + (b[2] - a[2]) * t;
          off = Math.max(off, Math.abs(H.hbAt(a[0], z) - (y(a) + (y(b) - y(a)) * t)));
        }
      }
      // the chord from each end's lowest corner to its highest
      let chord = 0;
      [Math.min(...f.pts.map(p => p[0])), Math.max(...f.pts.map(p => p[0]))].forEach(x => {
        const end = f.pts.filter(p => Math.abs(p[0] - x) < 1e-9).sort((p, q) => p[2] - q[2]);
        const lo = end[0], hi = end[end.length - 1];
        for (let k = 1; k < 20; k++) {
          const t = k / 20, z = lo[2] + (hi[2] - lo[2]) * t;
          const d_ = H.hbAt(x, z) - (y(lo) + (y(hi) - y(lo)) * t);
          if (Math.abs(d_) > Math.abs(chord)) chord = d_;
        }
      });
      return {part: f.part, side: f.side, pts: f.pts, outward: f.outward, off: off, chord: chord,
              hb: f.pts.map(p => H.hbAt(p[0], p[2]))};
    });
"""


def area_vector(pts: list) -> list[float]:
    """A polygon's area vector, the sum over its edges about its first point, doubled."""
    total = [0.0, 0.0, 0.0]
    p0 = pts[0]
    for a, b in zip(pts[1:], pts[2:], strict=False):
        u = [a[i] - p0[i] for i in range(3)]
        v = [b[i] - p0[i] for i in range(3)]
        total[0] += u[1] * v[2] - u[2] * v[1]
        total[1] += u[2] * v[0] - u[0] * v[2]
        total[2] += u[0] * v[1] - u[1] * v[0]
    return total


def unit(n: list) -> list[float]:
    size = math.hypot(*n)
    return [c / size for c in n]


@needs_node
@pytest.mark.parametrize("path", PROFILED)
def test_a_band_follows_the_drawn_side_between_its_two_heights(tmp_path, path):
    """The lead's point 10. Each wale and port band's two ends follow the drawn side from its lower
    height to its upper, through every height its strip's stations have a point at, each corner on
    the side and the side within 2 mm between them (straight in x and z between stations, a hair
    off that beside a closure). Old beside new, the straight chord's worst off the side:
    `CHORD_OFF_THE_SIDE_M`, the frigate's 0.613 m at x -21.88 to 2 mm. The polygons run to 25
    points."""
    hull = graph_of(path)["hull"]
    got = run_js(tmp_path, {"hull": hull}, BANDS)
    assert got
    assert max(len(f["pts"]) for f in got) > 4
    worst_chord = 0.0
    for f in got:
        sign = 1.0 if f["side"] == "starboard" else -1.0
        for p, hb in zip(f["pts"], f["hb"], strict=True):
            assert sign * p[1] == pytest.approx(hb, abs=1e-9)
        assert f["off"] <= 0.002, (f["part"], f["pts"][0])
        worst_chord = max(worst_chord, abs(f["chord"]))
    assert worst_chord == pytest.approx(CHORD_OFF_THE_SIDE_M[path], abs=0.002)
    # its ends share its stations: every served point of a station within a band's heights at that
    # station's x is a corner of it
    corners = {(round(p[0], 6), round(p[2], 6)) for f in got for p in f["pts"]}
    for f in got:
        for x in {p[0] for p in f["pts"]}:
            end = [p[2] for p in f["pts"] if p[0] == x]
            for station in hull["stations"][1:-1]:
                if station[0][0] != x:
                    continue
                for _x, z, _hb in station:
                    if min(end) + 1e-6 < z < max(end) - 1e-6:
                        assert (round(x, 6), round(z, 6)) in corners, (x, z)


@needs_node
@pytest.mark.parametrize("path", PROFILED)
def test_a_bands_face_is_taken_from_the_whole_of_it(tmp_path, path):
    """`faceOut` reads a polygon of more points than four and not flat: its `outward` is the whole
    polygon's area vector, away from the middle line on its side, and on four points the cross of
    the diagonals as it was. Reading only the first four corners of a longer band would tilt it to
    the station at its fore end."""
    got = run_js(tmp_path, {"hull": graph_of(path)["hull"]}, BANDS)
    longer = 0
    for f in got:
        sign = 1.0 if f["side"] == "starboard" else -1.0
        whole = unit(area_vector(f["pts"]))
        assert sign * f["outward"][1] > 0.0, f["pts"][0]
        turned = 1.0 if sign * whole[1] > 0.0 else -1.0
        assert unit(f["outward"]) == pytest.approx([turned * c for c in whole], abs=1e-9)
        longer += len(f["pts"]) > 4
    assert longer > 0


@needs_node
def test_a_face_of_any_number_of_points_turns_as_its_area_does(tmp_path):
    """`faceOut` on its own: four points, the diagonals' cross; a triangle cut from four, by one
    corner twice; a bent face whose first four corners lean one way and the whole of it the other,
    the whole of it; away from the middle line by `sign`, and up with no sign."""
    quad = [[0, 1, 0], [1, 1, 0], [1, 1.2, 1], [0, 1.2, 1]]
    cut = [[0, 1, 0], [1, 1, 0], [1, 1.2, 1], [1, 1.2, 1]]
    # a band with an end of several heights: its first corners run in, the rest of it out
    bent = [
        [0, 3, 0],
        [2, 2.9, 0],
        [2, 2.8, 0.2],
        [2, 2.75, 0.4],
        [2, 3.6, 2],
        [0, 3.8, 2],
        [0, 3.2, 1],
    ]
    flat = [[0, 2, 1], [1, 2, 1], [1, -2, 1], [0, -2, 1]]
    got = run_js(
        tmp_path,
        {"quad": quad, "cut": cut, "bent": bent, "flat": flat},
        """
        return {quad: P.faceOut(d.quad, 1), quadPort: P.faceOut(d.quad, -1),
                cut: P.faceOut(d.cut, 1), bent: P.faceOut(d.bent, 1), flat: P.faceOut(d.flat, 0),
                flatRev: P.faceOut(d.flat.slice().reverse(), 0)};
        """,
    )
    (ax, ay, az), (bx, by, bz) = (
        [quad[2][i] - quad[0][i] for i in range(3)],
        [quad[3][i] - quad[1][i] for i in range(3)],
    )
    diagonals = [ay * bz - az * by, az * bx - ax * bz, ax * by - ay * bx]
    turned = 1 if diagonals[1] > 0 else -1
    assert unit(got["quad"]) == pytest.approx([c * turned for c in unit(diagonals)])
    assert got["quad"][1] > 0.0 > got["quadPort"][1]
    assert got["cut"][1] > 0.0
    whole = unit(area_vector(bent))
    assert got["bent"][1] > 0.0
    assert unit(got["bent"]) == pytest.approx([c * (1 if whole[1] > 0 else -1) for c in whole])
    assert got["flat"][2] > 0.0 and got["flatRev"][2] > 0.0


@needs_node
@pytest.mark.parametrize("path", PROFILED)
def test_the_bands_stand_inside_the_hulls_own_extent_so_the_view_does_not_rescale(tmp_path, path):
    """The band's mend moves pictures and no behaviour: every view's bounds are those of the hull's
    other figures alone, with or without the bands, and of the full frame."""
    graph = graph_of(path)
    got = run_js(
        tmp_path,
        {"graph": graph},
        """
        const hull = P.hullFigures(d.graph.hull);
        const tag = fs => ({figures: fs.map(f => Object.assign({kind: 'hull'}, f))});
        const rest = hull.filter(f => f.part !== 'wale' && f.part !== 'band');
        return [0, Math.PI / 4, Math.PI / 2, 3 * Math.PI / 4, Math.PI, 5 * Math.PI / 4].map(f =>
          [0, 0.17, -0.17].map(h => [P.project(tag(hull), f, h, {underwater: 'solid'}).bounds,
                                     P.project(tag(rest), f, h, {underwater: 'solid'}).bounds]));
        """,
    )
    for view in got:
        for whole, without in view:
            assert whole == pytest.approx(without, abs=1e-9)


@needs_node
@pytest.mark.parametrize(("path", "builder"), DRAWN_BY)
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
@pytest.mark.parametrize(("path", "builder"), DRAWN_BY)
def test_where_a_deck_ends_over_another_a_bulkhead_closes_the_space_between(
    tmp_path, path, builder
):
    """Where a deck ends with another running on under it, a face across the ship closes the
    space (§6's `bulkhead`; judgement, derived from `decks_m` and `rail_m`): at the deck's end,
    from the deck below up to the top of the side there, on the drawn side at each height. The
    64's roundhouse front, quarterdeck breast and forecastle's after end; the razee's breast and
    forecastle. So dead ahead the space under her quarterdeck and roundhouse is not seen through,
    and on the quarter her forecastle deck is not seen through its after end. The frigate's breast
    and forecastle, as the razee's but for her roundhouse; every other file carries one deck, with
    nothing to close."""
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
        "frigate-36": {("quarterdeck", "fore"), ("forecastle", "aft")},
    }.get(Path(path).stem, set())
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
# mast and its yard, on the fixture (tests/rig_fixtures.py) and on the 64's own file; the razee
# keeps a spanker on a gaff
# ---------------------------------------------------------------------------

MIZEN_COURSE = "mizzen.course"
FIXTURE = "the fixture"  # a case's rig: the fixture of its section, or a file's own
MIZEN_RIGS = [FIXTURE, SIXTY_FOUR]


def taffrail_of(graph: dict) -> list:
    """Where a sheet led to the stern is drawn to, on the centreline (`client/projection.js`'s
    `taffrail`): the stern's line's top on a hull drawn from her profile (the rail's after end but
    on the cutter, whose rail ends 0.28 m forward of it: old, the rail's end there), else the stern
    of the hull drawn without one."""
    hull = graph["hull"]
    if hull.get("profile"):
        stern = hull["profile"].get("stern_m")
        x, z = stern[-1] if stern else hull["profile"]["rail_m"][0]
        return [x, 0.0, z]
    return [-0.52 * hull["length_waterline_m"], 0.0, 1.02 * hull["deck_height_m"]]


def mizen_by_the_wind(
    tack: str,
    sheet_deg: float = 30.0,
    state: SailState = SailState.SET,
    reefs: int = 0,
    rig: str = FIXTURE,
) -> dict:
    """`frigate_with_mizen_yard()`, or the file `rig`, under plain sail on `tack`, her mizen
    course in `state`, sheeted `sheet_deg` off the centreline: the graph and snapshot."""
    ship = frigate_with_mizen_yard() if rig == FIXTURE else make_ship(rig)
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
@pytest.mark.parametrize("rig", MIZEN_RIGS)
@pytest.mark.parametrize("tack", ["starboard", "larboard"])
def test_the_mizen_yard_is_slung_at_its_truss_its_fore_part_to_windward(tmp_path, tack, rig):
    """Ext §6.1: the truss at the mast at deck plus the throat's height; the course swung whole
    about the mast, where its luff is laced, by the sheet's angle to the sheet's side, on its
    corners (each as far from the mast and from the others as the file has it); the yard's
    after part along its head to the peak, and the bare fore part on the same line forward of
    the mast by the rest of the yard, to windward as the after part lies to leeward. Its one
    sheet runs from the clew to the taffrail on the centreline."""
    data = mizen_by_the_wind(tack, rig=rig)
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
    assert [s["id"] for s in sheets] == ["mizzen.course.sheet"]
    assert sheets[0]["pts"] == [
        pytest.approx(drawn[3]),
        pytest.approx(taffrail_of(data["graph"]), abs=1e-9),
    ]


@needs_node
@pytest.mark.parametrize("rig", MIZEN_RIGS)
def test_the_course_unswung_lies_on_its_files_corners(tmp_path, rig):
    """With its sheet at no angle the course lies in the fore-and-aft plane on the file's
    corners, to the millimetre: the drawing is the file's cut, swung."""
    data = mizen_by_the_wind("larboard", rig=rig)
    for s in data["snap"]["sails"]:
        if s["id"] == MIZEN_COURSE:
            s["sheet_angle"] = 0.0
    got = run_js(tmp_path, data, MIZEN_FIGURES)
    sail, _yard, deck = _course_and_yard(data["graph"])
    drawn = [got["corners"][i] for i in (3, 0, 1, 2)]  # tack, throat, peak, clew
    for p, q in zip(drawn, sail["corners_m"], strict=True):
        assert p == pytest.approx([q[0], 0.0, deck + q[1]], abs=1e-3)


@needs_node
@pytest.mark.parametrize("rig", MIZEN_RIGS)
def test_the_mizen_yards_lifts_hold_its_after_part_from_the_masthead(tmp_path, rig):
    """The lifts of every yard drawn faint (B5.1): the mizen yard's from its after part, where
    the sail hangs, the pair about its middle a twentieth of it apart either way (the starboard
    one nearer the peak), so that neither is drawn over the other, and the derrick nearer the
    peak, each up to the mizzen mast's head; no brace."""
    got = run_js(tmp_path, mizen_by_the_wind("larboard", rig=rig), MIZEN_FIGURES)
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
@pytest.mark.parametrize("rig", MIZEN_RIGS)
@pytest.mark.parametrize("facing_deg", [0.0, 45.0, 90.0, 135.0, 225.0])
def test_the_frame_holds_the_mizen_yards_swing_across_states(tmp_path, facing_deg, rig):
    """Ext §6.1: `fullRigFrame` reaches the yard's swing about its truss, the fore part's with
    it, at the heights of the yard's ends and the sail's foot and at the quarters as well as
    the four sides, so every point of the yard, the course and their lines lies within the
    frame alone, upright or heeled; and the view's scale is the same on either tack, at any
    sheet, set, in the gear or furled."""
    states = {
        f"{tack}-{sheet}-{state.value}": mizen_by_the_wind(tack, sheet, state, rig=rig)
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
@pytest.mark.parametrize("rig", MIZEN_RIGS)
def test_the_course_is_brailed_to_the_mast_and_furled_along_its_yard(tmp_path, rig):
    """Ext §6.1: in the gear the course is gathered to the mast and up under the yard, its foot
    hauled up the mast and its leech in along the yard by the gear's depth (IN_GEAR_DEPTH,
    0.35), its sheet from the clew brailed in with it; furled, a bundle along the yard's after
    part, aloft, with no sheet drawn. The yard stays where it was."""
    lee = run_js(tmp_path, mizen_by_the_wind("larboard", rig=rig), MIZEN_FIGURES)
    gear = mizen_by_the_wind("larboard", state=SailState.IN_THE_GEAR, rig=rig)
    brailed = run_js(tmp_path, gear, MIZEN_FIGURES)
    furled = run_js(
        tmp_path, mizen_by_the_wind("larboard", state=SailState.FURLED, rig=rig), MIZEN_FIGURES
    )
    truss, peak = lee["truss"], lee["peak"]
    for got in (brailed, furled):
        assert got["truss"] == pytest.approx(truss) and got["peak"] == pytest.approx(peak)
    luff = truss[2] - lee["corners"][3][2]
    head_aft = lee["off"][1][0]  # the peak's distance abaft the mast
    assert min(z for _aft, z in lee["pathOff"]) < truss[2] - 0.9 * luff  # set, down to its foot
    assert brailed["state"] == "in_the_gear"
    for aft, z in brailed["pathOff"]:  # to the millimetre, as the driver's below
        assert z >= truss[2] - 0.35 * luff - 1e-3
        assert aft <= 0.35 * head_aft + 0.8 + 1e-3
    # the sheet from the clew in the bundle, not where it stood set, to the taffrail
    (sheet,) = [ln for ln in brailed["lines"] if ln["cls"] == "sheet"]
    aft, z = sheet["off"][0]
    assert truss[2] - 0.35 * luff < z < truss[2] and 0.0 < aft <= 0.35 * head_aft + 0.8
    assert sheet["pts"][1] == pytest.approx(taffrail_of(gear["graph"]), abs=1e-9)
    assert furled["state"] == "furled"
    assert max(_off_the_segment(p, truss, peak) for p in furled["path"]) <= 0.35 + 1e-6
    assert not [ln for ln in furled["lines"] if ln["cls"] == "sheet"]  # furled: none drawn


@needs_node
@pytest.mark.parametrize("path", PROFILED)
def test_the_courses_sheet_leads_to_the_taffrail_of_a_hull_drawn_from_its_profile(tmp_path, path):
    """Ext §6.1: where the file gives a profile, as every file does, the course's sheet runs from
    its clew to the profile's taffrail (`taffrail_of`) on the centreline, not to the stern of the
    hull drawn without one. The fixture's rig on each profiled hull served; the 64's own course on
    her own file in the cases above and in `test_her_after_sails_sheets_lead_to_her_own_taffrail`.
    Old beside new, the cutter's: the rail's after end, x -9.23 at 1.83 m, to the stern's line's
    top, x -9.51 at 1.95 m, 0.28 m abaft it, where her transom's top is drawn."""
    data = mizen_by_the_wind("larboard")
    data["graph"]["hull"] = ship_state(make_ship(path))["graph"]["hull"]
    got = run_js(tmp_path, data, MIZEN_FIGURES)
    taffrail = taffrail_of(data["graph"])
    length = data["graph"]["hull"]["length_waterline_m"]
    (sheet,) = [ln["pts"] for ln in got["lines"] if ln["cls"] == "sheet"]
    assert sheet[0] == pytest.approx(got["corners"][2])  # the clew
    assert sheet[1] == pytest.approx(taffrail, abs=1e-3)
    assert abs(taffrail[0] + 0.52 * length) > 0.1  # not the stern drawn without a profile


@needs_node
@pytest.mark.parametrize("rig", MIZEN_RIGS)
def test_a_reef_raises_the_courses_foot_up_the_mast(tmp_path, rig):
    """Ext §6.1: the reef raises the foot as a gaff sail's does: the tack up the luff on the mast
    by the reef's share of it (the curve class's `reef_factor`, served), the clew with it."""
    whole = run_js(tmp_path, mizen_by_the_wind("larboard", rig=rig), MIZEN_FIGURES)
    data = mizen_by_the_wind("larboard", reefs=1, rig=rig)
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
@pytest.mark.parametrize("rig", MIZEN_RIGS)
def test_the_course_as_the_game_serves_it_is_drawn_at_its_mast(tmp_path, rig):
    """The rig's world through the game's own doors (`/api/ship`, `/api/state`): the graph
    serves the course's cut and key and the yard's class, and the drawing takes them as above.
    As she starts, the course furled at no sheet: the yard in the fore-and-aft plane, slung at
    its truss, the course a bundle along its after part; then set and sheeted, to leeward of
    the tack the state gives, the yard's fore part to windward, its sheet to the taffrail."""
    pytest.importorskip("fastapi")
    from fastapi.testclient import TestClient

    from freesail.ui.server import Driver, create_app

    path = write_ship(frigate_with_mizen_yard_doc(), tmp_path) if rig == FIXTURE else rig
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
    assert sheet == [
        pytest.approx(set_["corners"][2]),
        pytest.approx(taffrail_of(start["graph"]), abs=1e-9),
    ]


# ---------------------------------------------------------------------------
# Package 75 (B5.3, docs/design/Design-ShipsEngineExtensions.md §6.2): the yards under the
# bowsprit, on the fixture (tests/rig_fixtures.py, with the frigate's profile taken away, as it was
# cut), on the pilot's two files as they are (the razee crosses
# no sprit-topsail yard: Indf §17 item 5) and on the profiled files with the fixture's yards cut in
# place of hers on their own bowsprit and jib-boom; the bowsprit stood from the profile's stem head
# (the lead's ruling of 2026-10-29)
# ---------------------------------------------------------------------------

SPRIT_YARDS = ("spritsail.yard", "sprit_topsail.yard")
SPRIT_SAILS = ("spritsail", "sprit_topsail")
SPRIT_RIGS = [FIXTURE, SIXTY_FOUR, RAZEE]
# each yard's spar, and how far the fixture hangs it under that spar's line
SPRIT_HANG = {
    "spritsail.yard": ("bowsprit", SPRITSAIL_HANG_M),
    "sprit_topsail.yard": ("jib_boom", SPRIT_TOPSAIL_HANG_M),
}
CLEW_SPREAD = 0.9  # client/projection.js: a topsail's clews at nine-tenths of the yard below
FOOT_SAG = 0.06  # client/projection.js: the sag of a square sail's foot, a fraction of its depth
HEAD_SPREAD = 0.9  # and a sail with no yard below as broad as nine-tenths of its own
SPRITSAIL_CENTRE_ON_HER_FILES = 0.25  # metres: filed by Steel's cut, hung by the drawing's rule


def sprit_sails(
    state: SailState = SailState.SET,
    reefs: int = 0,
    brace_deg: float = 0.0,
    tack: str = "larboard",
    rig: str = FIXTURE,
) -> dict:
    """`frigate_with_mizen_yard()`, or the file `rig`, under plain sail on `tack` with the wind on
    the quarter, her spritsail and sprit topsail in `state` (the spritsail with `reefs`), the
    yards under the bowsprit braced `brace_deg` from square (positive, the starboard yardarm
    forward): the graph and snapshot."""
    ship = frigate_with_mizen_yard() if rig == FIXTURE else make_ship(rig)
    for sid in ship.groups["plain sail"]:
        ship.sails[sid].state = SailState.SET
    for sid in SPRIT_SAILS:
        if sid in ship.sails:
            sail = ship.sails[sid]
            sail.state, sail.reefs = state, min(reefs, sail.reef_bands)
    for yid in SPRIT_YARDS:
        if yid in ship.spars:
            ship.spars[yid].brace_angle = math.radians(brace_deg)
    awa = math.radians(120.0) * (1.0 if tack == "starboard" else -1.0)
    data = ship_state(ship, awa=awa, tack=tack)
    if rig == FIXTURE:
        # hung by the frigate's spars as a hull with no profile draws them (`head_chain`), and so
        # drawn; a yard cut on a hull drawn from her profile: `with_sprit_yards`
        without_profile(data)
        _fixture_sprit_topsail_along_the_slant(data["graph"])
    return data


def _fixture_sprit_topsail_along_the_slant(graph: dict) -> None:
    """The fixture files its sprit topsail by the heights between its yards (35 m2), and the
    engine's tests read that figure (`tests/test_bowsprit_yards.py`'s polar, its furled windage).
    The drawing reckons a sail between two yards under the bowsprit along the slant between them
    (Ext §6.2, risk 9), so in the graph this section draws, and nowhere else, it is cut so: the
    same trapezoid, nine-tenths of each yard, as deep as that slant (108 m2, about the 64's own).
    Its centre, the trapezoid's along the slant, does not move."""
    spars = {s["id"]: s for s in graph["spars"]}
    below, yard = spars["spritsail.yard"], spars["sprit_topsail.yard"]
    slant = math.hypot(yard["x_m"] - below["x_m"], yard["height_m"] - below["height_m"])
    sail = next(s for s in graph["sails"] if s["id"] == "sprit_topsail")
    sail["area_m2"] = 0.5 * SPREAD * (yard["length_m"] + below["length_m"]) * slant


def sprit_parts(graph: dict) -> tuple[list[str], list[str]]:
    """The yards under the bowsprit and the sails on them a graph carries."""
    spars = {s["id"] for s in graph["spars"]}
    sails = {s["id"] for s in graph["sails"]}
    return [y for y in SPRIT_YARDS if y in spars], [s for s in SPRIT_SAILS if s in sails]


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
    sails and their lines (tests/rig_fixtures.py), in place of any of her own, cut on her own
    bowsprit and jib-boom as they are drawn from her stem head (`head_chain`) as the fixture cuts
    them on the frigate's: at its stations and hangs, as long as her fore topsail and fore
    topgallant yards, the spritsail down to a metre above the water and the sprit topsail the
    trapezoid to the spritsail yard's arms; both set (the graph's state: no snapshot)."""
    graph = graph_of(path)
    own = {*SPRIT_YARDS, *SPRIT_SAILS}
    graph["spars"] = [s for s in graph["spars"] if s["id"] not in own]
    graph["sails"] = [s for s in graph["sails"] if s["id"] not in own]
    graph["lines"] = [ln for ln in graph["lines"] if ln["of"] not in own]
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
            "area_m2": 0.5 * (head + foot) * math.hypot(st_x - ss_x, gap),
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
@pytest.mark.parametrize("rig", SPRIT_RIGS)
@pytest.mark.parametrize("state", [SailState.SET, SailState.IN_THE_GEAR, SailState.FURLED])
def test_each_yard_under_the_bowsprit_stands_at_its_station_under_its_spar(tmp_path, state, rig):
    """Ext §6.2: a yard on the bowsprit or the jib-boom stands at its own `x_m` at deck plus its
    `height_m`, with no slinging offset and no hoist whatever its sail's state, its arms across
    the ship, as far under its spar's drawn line as the fixture hangs it (within its file's
    tenth of a metre); not at its spar's heel, where the trial's spritsail hung with its foot
    two metres under the water (Eng §5). On her files, each under the spar as it is drawn from
    her stem head: the razee's heel, lowered to her rail, leaves her spritsail yard 0.04 m lower
    under it than the 64's."""
    data = sprit_sails(state, rig=rig)
    got = run_js(tmp_path, data, SPRIT_FIGURES)
    deck = data["graph"]["hull"]["deck_height_m"]
    spars = {s["id"]: s for s in data["graph"]["spars"]}
    yards, _sails = sprit_parts(data["graph"])
    for yid in yards:
        on, hang = SPRIT_HANG[yid]
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
    drawn_yards = [f for f in got["drawn"] if f["id"] in yards]
    assert {f["id"]: f["hoist"] for f in drawn_yards} == dict.fromkeys(yards, 1)


@needs_node
@pytest.mark.parametrize("rig", SPRIT_RIGS)
def test_the_spritsail_hangs_from_its_yard_and_the_sprit_topsail_is_sheeted_to_its_arms(
    tmp_path, rig
):
    """Ext §6.2: the spritsail, with no yard below it, hangs from its yard as `squareCut` hangs
    any such sail, nine-tenths of its yard broad, head and foot, and its area over that deep.
    The sprit topsail's clews are at the spritsail yard's arms, at nine-tenths of it as every
    topsail's are at the yard below (within 0.1 m: Ext §6.5), and its head along its own yard:
    the trapezoid between the two yards. Each is drawn to its file's area along the slant between
    its yards within a twentieth, and its centre where the file puts the sail's force (its `x_m`
    and `centre_height_m`, within 0.1 m: the drawing against the physics). Her spritsail is filed
    by Steel's cloths and depth, 14.9 m broad and 6.9 m deep, and hangs nine-tenths of her yard
    broad, 15.8 m, so a little shallower: its centre drawn 0.16 m high on the 64 and 0.20 m on
    the razee, within SPRITSAIL_CENTRE_ON_HER_FILES."""
    data = sprit_sails(rig=rig)
    got = run_js(tmp_path, data, SPRIT_FIGURES)
    sails = {s["id"]: s for s in data["graph"]["sails"]}
    yard = got["spars"]["spritsail.yard"]
    ss = got["sails"]["spritsail"]["corners"]  # larboard head, starboard head, clews
    x, _y, z = yard["centre"]
    spread = HEAD_SPREAD * 2.0 * yard["half"]
    deep = sails["spritsail"]["area_m2"] / spread
    assert ss == [
        pytest.approx([x, -spread / 2.0, z]),
        pytest.approx([x, spread / 2.0, z]),
        pytest.approx([x, spread / 2.0, z - deep]),
        pytest.approx([x, -spread / 2.0, z - deep]),
    ]
    drawn = [("spritsail", ss)]
    if "sprit_topsail" in got["sails"]:
        top_yard = got["spars"]["sprit_topsail.yard"]
        st = got["sails"]["sprit_topsail"]["corners"]
        arm = CLEW_SPREAD * yard["half"]
        assert math.dist(st[2], [x, arm, z]) <= 0.1 and math.dist(st[3], [x, -arm, z]) <= 0.1
        for corner in st[:2]:  # the head along its own yard
            assert corner[0] == pytest.approx(top_yard["centre"][0])
            assert corner[2] == pytest.approx(top_yard["centre"][2])
        assert span(st[0], st[1]) <= 2.0 * top_yard["half"] + 1e-6
        drawn.append(("sprit_topsail", st))
    else:
        assert rig == RAZEE  # she alone crosses none
    for sid, c in drawn:
        assert slant_area(c) == pytest.approx(sails[sid]["area_m2"], rel=0.05), sid
        head, foot = span(c[0], c[1]), span(c[3], c[2])
        up = (2.0 * head + foot) / (3.0 * (head + foot))  # the trapezoid's centroid, from the foot
        mid_head = [(p + q) / 2.0 for p, q in zip(c[0], c[1], strict=True)]
        mid_foot = [(p + q) / 2.0 for p, q in zip(c[3], c[2], strict=True)]
        centre = [f + up * (h - f) for f, h in zip(mid_foot, mid_head, strict=True)]
        file = [sails[sid]["x_m"], 0.0, sails[sid]["centre_height_m"]]
        within = SPRITSAIL_CENTRE_ON_HER_FILES if sid == "spritsail" and rig != FIXTURE else 0.1
        assert centre == pytest.approx(file, abs=within), sid


@needs_node
def test_her_sprit_topsail_is_drawn_along_the_slant_to_its_files_area(tmp_path):
    """Ext §6.2's risk 9, on her own yards. They hang where Steel's 9 yards of depth put them, 8.23
    m apart along the slant and 3.97 m by their heights, the sail's plane sloping far forward;
    `squareCut` takes the gap along that slant for a yard under the bowsprit alone (old beside
    new): the file's 103 m2 by the heights' gap filled the head to the whole yard, 10.50 m, and
    still reckoned 52 m2 by the heights, or 108 m2 as it lay along the slant; by the slant the
    head is 9.30 m and the foot 15.75 m, against Steel's 9.72 and 15.43, 103 m2. Its centre is
    the file's, its belly and festoons reckoned by the slant."""
    data = sprit_sails(rig=SIXTY_FOUR)
    got = run_js(tmp_path, data, SPRIT_FIGURES)
    spars = {s["id"]: s for s in data["graph"]["spars"]}
    sail = next(s for s in data["graph"]["sails"] if s["id"] == "sprit_topsail")
    below, yard = spars["spritsail.yard"], spars["sprit_topsail.yard"]
    gap = yard["height_m"] - below["height_m"]
    slant = math.hypot(yard["x_m"] - below["x_m"], gap)
    assert gap == pytest.approx(3.97, abs=0.05) and slant == pytest.approx(9.0 * 0.9144, abs=0.05)
    c = got["sails"]["sprit_topsail"]["corners"]
    head, foot = span(c[0], c[1]), span(c[3], c[2])
    assert foot == pytest.approx(CLEW_SPREAD * below["length_m"])
    assert head == pytest.approx(2.0 * sail["area_m2"] / slant - foot)
    assert head == pytest.approx(9.30, abs=0.05)  # within Steel's cloths, and within its yard
    assert head < yard["length_m"]
    assert slant_area(c) == pytest.approx(sail["area_m2"], abs=0.5)
    assert quad_area(c) < 0.55 * sail["area_m2"]  # by the heights it would fall far short
    # the foot's sag is reckoned by the slant, not by the heights: its control point (the path's
    # head, leech, foot, leech) stands twice FOOT_SAG of the slant under the mean of the clews
    control = run_js(
        tmp_path,
        data,
        """
        const sk = P.buildSkeleton(d.graph, d.snap);
        return sk.figures.find(f => f.kind === 'sail' && f.id === 'sprit_topsail').path[3][0];
        """,
    )
    clews = 0.5 * (c[2][2] + c[3][2])
    assert control[2] == pytest.approx(clews - 2.0 * FOOT_SAG * slant, abs=1e-6)


@needs_node
@pytest.mark.parametrize("rig", [FIXTURE, SIXTY_FOUR])
@pytest.mark.parametrize(
    "facing_deg,order",
    [
        (0.0, ("jib_boom", "sprit_topsail", "sprit_topsail.yard")),
        (30.0, ("jib_boom", "sprit_topsail", "sprit_topsail.yard")),
        (45.0, ("jib_boom", "sprit_topsail", "sprit_topsail.yard")),
        (60.0, ("jib_boom", "sprit_topsail", "sprit_topsail.yard")),
        (180.0, ("sprit_topsail", "jib_boom")),
    ],
)
def test_the_jib_boom_is_drawn_behind_the_sprit_topsail_from_ahead(
    tmp_path, facing_deg, order, rig
):
    """The sprit topsail stands forward of the jib-boom all the way up to its yard (on the 64, by
    0.95-1.35 m): seen from ahead the spar is behind the sail, and it does not end in the cloth,
    as it did sorted at its own middle. A jib-boom with a yard under it is sorted at its heel. From
    astern the spar is drawn over the sail."""
    facing = math.radians(facing_deg)
    body = f"""
        const sk = P.buildSkeleton(d.graph, d.snap);
        return P.project(sk, {facing}, 0).figures.map(f => f.id);
    """
    ids = run_js(tmp_path, sprit_sails(rig=rig), body)
    at = [ids.index(fid) for fid in order]
    assert at == sorted(at), (order, at)


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
@pytest.mark.parametrize("rig", SPRIT_RIGS)
@pytest.mark.parametrize("brace_deg", [0.0, 30.0, -30.0])
def test_every_sprit_sails_foot_stands_above_the_water_in_every_state(tmp_path, brace_deg, rig):
    """Ext §6.5: upright, each sail under the bowsprit and its yard stand clear of the water in
    every state: the spritsail set, reefed once and twice, goose-winged, loosed, in the gear and
    furled, square and braced to its limit either way; the lowest point of each drawn outline,
    its belly and its foot's sag taken, above the sea."""
    states = {f"{s.value}-{r}": sprit_sails(s, r, brace_deg, rig=rig) for s, r in SPRIT_STATES}
    yards, sails = sprit_parts(next(iter(states.values()))["graph"])
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
        assert {fid for fid, _low in figs} == {*yards, *sails}, name
        for fid, low in figs:
            assert low > 0.0, (name, fid, low)


@needs_node
@pytest.mark.parametrize("rig", SPRIT_RIGS)
@pytest.mark.parametrize("brace_deg", [0.0, 30.0])
def test_the_braces_lead_up_to_the_fore_top_the_sheets_aft_and_the_lifts_to_the_spars_end(
    tmp_path, brace_deg, rig
):
    """Ext §6.2: the braces of a yard under the bowsprit or the jib-boom lead from its arms up to
    the fore top, the fore mast's head less a metre on its raked line, a little to their own
    side, not level aft (Lavery I30). The spritsail's sheets lead from its clews aft along the
    side to the deck a metre abaft the fore mast (I30's sheave in the side), not abreast the
    clew forward of the stem; the sprit topsail's to the spritsail yard's arms, as every
    topsail's to the yard below. Their lifts, as every yard's, from the arms up to the head of
    the spar each hangs on: the bowsprit's end and the jib-boom's. The guys are not drawn."""
    data = sprit_sails(brace_deg=brace_deg, rig=rig)
    got = run_js(tmp_path, data, SPRIT_FIGURES)
    deck = data["graph"]["hull"]["deck_height_m"]
    beam = data["graph"]["hull"]["beam_m"]
    lines = {ln["id"]: ln["pts"] for ln in got["lines"]}
    fore_x, top_z = got["foreTop"]
    yards, sails = sprit_parts(data["graph"])
    for yid in yards:
        on, _hang = SPRIT_HANG[yid]
        yard = got["spars"][yid]
        for side, s in (("starboard", 1.0), ("larboard", -1.0)):
            arm = yard["b"] if s > 0 else yard["a"]
            brace = lines[f"{yid}.brace.{side}"]
            assert brace == [pytest.approx(arm), pytest.approx([fore_x, 0.3 * s, top_z])]
            lift = lines[f"{yid}.lift.{side}"]
            assert lift == [pytest.approx(arm), pytest.approx(got["spars"][on]["b"])]
    assert top_z > got["spars"][yards[-1]]["centre"][2] + 5.0  # up, not level aft
    below = got["spars"]["spritsail.yard"]
    ss = got["sails"]["spritsail"]["corners"]
    for side, s in (("starboard", 1.0), ("larboard", -1.0)):
        sheet = lines[f"spritsail.sheet.{side}"]
        # to half the beam, or on a hull drawn from her profile to her drawn side there, which is
        # narrower so far forward (the 64's 6.77 m stood 1.5 m outboard of it)
        x = got["foreX"] - 1.0
        out = beam / 2.0
        if rig != FIXTURE:
            out = form.half_breadth_at(make_ship(rig).hull.spec, x, deck)
        lead = [x, s * out, deck]
        assert sheet == [pytest.approx(ss[2] if s > 0 else ss[3]), pytest.approx(lead, abs=1e-3)]
        if "sprit_topsail" in sails:
            st = got["sails"]["sprit_topsail"]["corners"]
            sheet = lines[f"sprit_topsail.sheet.{side}"]
            clew, arm = (st[2], below["b"]) if s > 0 else (st[3], below["a"])
            assert sheet == [pytest.approx(clew), pytest.approx(arm)]
    assert not [ln for ln in got["lines"] if ln["cls"] == "guy"]


@needs_node
@pytest.mark.parametrize("rig", SPRIT_RIGS)
@pytest.mark.parametrize("facing_deg", [0.0, 45.0, 90.0])
def test_a_yard_and_sail_under_the_bowsprit_are_sorted_at_their_own_middle(
    tmp_path, facing_deg, rig
):
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
    data = sprit_sails(rig=rig)
    got = run_js(tmp_path, data, body)
    yards, sails = sprit_parts(data["graph"])
    assert sorted(fid for fid, _depth, _own in got) == sorted(yards + sails)
    for fid, depth, (sort_at, own) in got:
        assert sort_at is None, fid
        assert depth == pytest.approx(own, abs=1e-9), fid


@needs_node
@pytest.mark.parametrize("rig", SPRIT_RIGS)
@pytest.mark.parametrize("facing_deg", [0.0, 45.0, 90.0, 135.0, 225.0])
def test_the_frame_holds_the_yards_under_the_bowsprit_across_states(tmp_path, facing_deg, rig):
    """The fixed scale (spec M3 §9 item 14): `fullRigFrame` reaches each yard's swing about its
    slings, and a sail's foot hanging from it, so every point of the yards under the bowsprit,
    their sails and their lines lies within the frame alone, upright or heeled; and the view's
    scale is the same on either tack, square or braced to the limit either way, set, in the gear
    or furled. The foot's reach is the razee's: with no sprit-topsail yard above it, her spritsail
    set and braced passed the frame by 2 cm, heeled 0.3 rad, seen on the bow or the quarter."""
    states = {
        f"{tack}-{brace}-{state.value}": sprit_sails(state, brace_deg=brace, tack=tack, rig=rig)
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
@pytest.mark.parametrize("path", [p for p in PROFILED if p not in (CUTTER, LUGGER, SMACK)])
def test_on_a_hull_drawn_from_her_profile_the_yards_hang_from_the_bowsprit_as_it_stands(
    tmp_path, path
):
    """The lead's ruling of 2026-10-29: where the file gives a profile, the yards under the
    bowsprit hang from a bowsprit stood from the stem head as long as the file has it, and the
    stand-in of a heel on the datum goes. The fixture's two yards cut on her own bowsprit and
    jib-boom as they stand (`with_sprit_yards`) hang exactly as far under the drawn spars as
    they were cut, at their own stations; the spritsail's foot a metre above the water, the
    sprit topsail's clews at the spritsail yard's arms, the braces up to her fore top: every file
    with a jib-boom (the cutter, the lugger and the smack carry none)."""
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
@pytest.mark.parametrize("path", PILOT)
def test_her_headsails_are_tacked_on_the_spars_as_they_are_drawn(tmp_path, path):
    """Indf §3.5 item 9 and Ext §6.2 as built, on her own files: with the file's bowsprit rooted
    on the stem head, the drawn spars pass through the tacks her corners give, within 0.1 m: the
    fore staysail's on the bowsprit, the fore topmast staysail's at its end and the jib's at the
    jib-boom's. Old beside new, the fore staysail's tack on the 64: 0.04 m from the spar at B5.1,
    about 0.6 m at B5.3 with the file's root still on the knighthead's cap, now 0.01 m. The
    razee's heel, lowered 0.12 m to her rail, leaves her bowsprit's end 0.10 m short of the fore
    topmast staysail's tack, within 0.15 m fore and aft."""
    ship = make_ship(path)
    data = ship_state(ship)
    got = run_js(tmp_path, data, SPARS_DRAWN)
    deck = data["graph"]["hull"]["deck_height_m"]
    sails = {s["id"]: s for s in data["graph"]["sails"]}
    for sid, on in (
        ("fore.staysail", "bowsprit"),
        ("fore.topmast_staysail", "bowsprit"),
        ("jib", "jib_boom"),
    ):
        heel, end = got[on]
        x, z = sails[sid]["corners_m"][0]
        assert heel[0] <= x <= end[0] + 0.15, sid
        assert _on_the_line(heel, end, x) == pytest.approx(deck + z, abs=0.1), sid
    assert sails["fore.topmast_staysail"]["corners_m"][0][0] == pytest.approx(
        got["bowsprit"][1][0], abs=0.15
    )
    assert sails["jib"]["corners_m"][0][0] == pytest.approx(got["jib_boom"][1][0], abs=0.15)


@needs_node
@pytest.mark.parametrize("case", WITHOUT_PROFILE)
def test_without_a_profile_the_bowsprit_and_its_booms_stand_as_before(tmp_path, case):
    """A graph with no profile draws its bowsprit from its `x_m` on the datum, rising its
    `height_m`, and the booms on it from its end, as before B5.3 (`head_chain`): every file's graph
    with its profile taken away (`WITHOUT_PROFILE`)."""
    graph = graph_of_case(case)
    got = run_js(tmp_path, {"graph": graph}, SPARS_DRAWN)
    chain = head_chain(graph)
    assert chain
    for sid, (heel, end) in chain.items():
        assert got[sid] == [pytest.approx(heel, abs=1e-12), pytest.approx(end, abs=1e-12)], sid


@needs_node
@pytest.mark.parametrize("rig", SPRIT_RIGS)
def test_the_yards_under_the_bowsprit_as_the_game_serves_them(tmp_path, rig):
    """The rig's world through the game's own doors (`/api/ship`, `/api/state`): the graph
    serves each yard's own `x_m` and its spar, and the drawing takes them as above. As she
    starts, the sprit sails furled on their yards at their stations; then set and the yards
    braced, each yard turned about its slings by the brace the state gives, and the sprit
    topsail's clews at the spritsail yard's arms."""
    pytest.importorskip("fastapi")
    from fastapi.testclient import TestClient

    from freesail.ui.server import Driver, create_app

    path = write_ship(frigate_with_mizen_yard_doc(), tmp_path) if rig == FIXTURE else rig
    scenario = Scenario(wind_from_deg=0.0, wind_speed_kn=10.0, ship_heading_deg=150.0)
    world = make_world(7, str(path), scenario)
    world.tick()
    with TestClient(create_app(Driver(world))) as client:
        start = {"graph": client.get("/api/ship").json(), "snap": client.get("/api/state").json()}
        yards, sails = sprit_parts(start["graph"])
        for sid in sails:
            world.ship.sails[sid].state = SailState.SET
        for yid in yards:
            world.ship.spars[yid].brace_angle = math.radians(20.0)
        world.tick()
        braced = {"graph": client.get("/api/ship").json(), "snap": client.get("/api/state").json()}
    deck = start["graph"]["hull"]["deck_height_m"]
    spars = {s["id"]: s for s in start["graph"]["spars"]}
    for yid in yards:
        on, _hang = SPRIT_HANG[yid]
        assert spars[yid]["parent"] == on and spars[yid]["x_m"] > spars["bowsprit"]["x_m"]
    furled = run_js(tmp_path, start, SPRIT_FIGURES)
    for yid in yards:
        at = [spars[yid]["x_m"], 0.0, deck + spars[yid]["height_m"]]
        assert furled["spars"][yid]["centre"] == pytest.approx(at)
    assert {sid: s["state"] for sid, s in furled["sails"].items()} == dict.fromkeys(sails, "furled")
    set_ = run_js(tmp_path, braced, SPRIT_FIGURES)
    angle = {s["id"]: s["brace_angle"] for s in braced["snap"]["spars"]}
    for yid in yards:
        yard, th = set_["spars"][yid], angle[yid]
        x, _y, z = yard["centre"]
        assert abs(th) > 0.1
        assert yard["centre"] == pytest.approx(furled["spars"][yid]["centre"])
        want = [x + yard["half"] * math.sin(th), yard["half"] * math.cos(th), z]
        assert yard["b"] == pytest.approx(want)
    assert {sid: s["state"] for sid, s in set_["sails"].items()} == dict.fromkeys(sails, "set")
    if "sprit_topsail" in sails:
        below = set_["spars"]["spritsail.yard"]
        arm = [c + CLEW_SPREAD * (b - c) for c, b in zip(below["centre"], below["b"], strict=True)]
        assert math.dist(set_["sails"]["sprit_topsail"]["corners"][2], arm) <= 0.1


# ---------------------------------------------------------------------------
# Package 75 (B5.5, docs/design/Design-ShipsEngineExtensions.md §17.6): the driver of the 64 and
# the 74, on the fixture `frigate_with_driver()` (tests/rig_fixtures.py) and on the 64's own file
# ---------------------------------------------------------------------------

DRIVER = "mizzen.driver"
DRIVER_BOOM = "mizzen.boom"
GEAR_DEPTH = 0.35  # client/projection.js: IN_GEAR_DEPTH


def driver_doc(rig: str, rigged_out: bool | None = False) -> dict:
    """The fixture's document with the driver in the sail room, or the file `rig`'s, its boom
    filing `rigged_out`, or no key at all with None. False is what `mizen_yard.driver()` files
    (Ext §17.11, B1's regeneration), given here so that a case on her own file reads the same
    before that regeneration and after it."""
    if rig == FIXTURE:
        doc = frigate_with_driver_doc()
    else:
        doc = yaml.safe_load((ROOT / rig).read_text(encoding="utf-8"))
    boom = next(s for s in doc["spars"] if s["id"] == DRIVER_BOOM)
    boom.pop("rigged_out", None)
    if rigged_out is not None:
        boom["rigged_out"] = rigged_out
    return doc


def driver_ship(rig: str, bent: bool, key: bool = True):
    """`frigate_with_driver(bent)`, or the file `rig`: the driver bent in the course's place with
    the boom rigged out, the course in the sail room, or as she is filed with the driver in the
    sail room and the boom rigged in. `key` false: the boom files no `rigged_out`, and stands out
    all the voyage (Ext §17.11's toggle)."""
    if rig == FIXTURE and key:
        return frigate_with_driver(bent)
    ship = attach_systems(ship_from_dict(driver_doc(rig, False if key else None), rig))
    if bent:
        ship.sails[MIZEN_COURSE].state = SailState.UNBENT
        ship.sails[DRIVER].state = SailState.FURLED
        ship.spars[DRIVER_BOOM].rigged_out = True
    return ship


def driver_by_the_wind(
    tack: str,
    sheet_deg: float = 30.0,
    state: SailState = SailState.SET,
    bent: bool = True,
    rig: str = FIXTURE,
    key: bool = True,
) -> dict:
    """`driver_ship(rig, bent, key)` under plain sail on `tack`, her after sail in `state` and
    sheeted `sheet_deg` off the centreline: the driver bent in the course's place, or the course
    with the driver in the sail room. The graph and snapshot."""
    ship = driver_ship(rig, bent, key)
    for sid in ship.groups["plain sail"]:
        if ship.sails[sid].state is not SailState.UNBENT:
            ship.sails[sid].state = SailState.SET
    after = ship.sails[DRIVER if bent else MIZEN_COURSE]
    set_sheet_angle(ship, after, math.radians(sheet_deg))
    after.state = state
    awa = math.radians(60.0) * (1.0 if tack == "starboard" else -1.0)
    return ship_state(ship, awa=awa, tack=tack)


# The mizen yard, the boom, the two after sails, the driver yard and the lines of the yard, the
# boom and the two sails, as drawn: `DRIVER_FIGURES` of one state, `DRIVER_STATES` of each of
# several. `jaws` and `boomEnd` are where the boom is placed, drawn or not; `boom` its figures.
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
        boom: sk.figures.filter(f => f.kind === 'spar' && f.id === 'mizzen.boom')
          .map(f => ({state: f.state, pts: f.pts})),
        driver: sail('mizzen.driver'), course: sail('mizzen.course'),
        driverYards: sk.figures.filter(f => f.cls === 'driver_yard')
          .map(f => ({kind: f.kind, id: f.id, of: f.of, pts: f.pts})),
        lines: sk.figures.filter(f => f.kind === 'line' &&
          ['mizzen.yard', 'mizzen.boom', 'mizzen.course', 'mizzen.driver'].includes(f.of))
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
@pytest.mark.parametrize("rig", MIZEN_RIGS)
@pytest.mark.parametrize("tack", ["starboard", "larboard"])
def test_the_driver_is_swung_about_the_mast_its_foot_along_its_boom(tmp_path, tack, rig):
    """Ext §17.6: the driver in §6.1's branch for a sail cut at the mast, with its boom. Its
    throat and peak are swung whole about the mast by the sheet's angle to the sheet's side,
    each as far from the mast and from the other as the file has them. The boom is swung about
    its jaws on the mast, level, to the same side by the same angle (`sheetAngleOf` takes the
    driver bent). The tack is at the boom's jaws, within 0.1 m of the file's tack on the mast,
    and the clew along the boom at the file's foot from the jaws, to leeward."""
    data = driver_by_the_wind(tack, rig=rig)
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
@pytest.mark.parametrize("rig", MIZEN_RIGS)
def test_the_driver_unswung_lies_on_its_files_corners_and_takes_no_reef(tmp_path, rig):
    """With its sheet at no angle the driver lies in the fore-and-aft plane on the file's four
    corners: the throat and the peak to the millimetre, and the tack and the clew, taken from
    the boom, within 0.1 m (Ext §17.6, §17.2's cut). No reef is drawn: a reef in the snapshot,
    which the engine never gives the driver (Steel names no band in it), moves nothing."""
    data = driver_by_the_wind("larboard", rig=rig)
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
@pytest.mark.parametrize("rig", MIZEN_RIGS)
def test_the_head_runs_along_the_yards_line_and_on_along_the_driver_yard(tmp_path, rig):
    """Ext §17.6, on §17.2's cut: the driver's head runs straight from the throat, at the yard's
    truss within 0.1 m, along the mizen yard's line to the sail's peak, which lies on that line
    within 0.1 m and beyond the yard's peak by what the file's head has over the course's.
    Beyond the yard's peak the head is drawn on Steel's driver yard, a spar line drawn with the
    sail (its id, of class `driver_yard`) from the yard's peak to the driver's: no more than
    two-thirds of the driver yard, whose inner part lies along the mizen yard and is drawn as
    it. Set, in the gear and furled alike; with the course bent, none."""
    states = {
        st.value: driver_by_the_wind("larboard", state=st, rig=rig)
        for st in (SailState.SET, SailState.IN_THE_GEAR, SailState.FURLED)
    }
    states["course"] = driver_by_the_wind("larboard", bent=False, rig=rig)
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
@pytest.mark.parametrize("rig", MIZEN_RIGS)
@pytest.mark.parametrize("tack", ["starboard", "larboard"])
def test_the_yard_lies_on_the_courses_line_whichever_sail_is_bent(tmp_path, tack, rig):
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
                states[f"{sheet}-{st.value}-{bent}"] = driver_by_the_wind(
                    tack, sheet, st, bent, rig
                )
    still = driver_by_the_wind(tack, rig=rig)
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
@pytest.mark.parametrize("rig", MIZEN_RIGS)
def test_the_boom_rigged_in_is_not_drawn_with_the_driver_in_the_sail_room(tmp_path, rig):
    """Ext §17.11, which replaces §17.6's "the boom lies amidships" and closes §17.10 item 10.
    With the driver in the sail room the boom is rigged in: there is no figure of it, nor of its
    sheet, whatever the course's sheet, as a spare on the booms is not drawn, and nothing of the
    driver. **Old beside new**, the course set with the driver in the sail room: old (B5.5, this
    case as `test_the_boom_lies_amidships_...`), a spar drawn level from its jaws, amidships,
    19.9 m aft, its jaws 1.5 m up the course's laced luff on the fixture; new, no spar. It is still
    placed there, which is how its swing stays in the frame. With the driver bent it is drawn as
    B5.5 drew it, to the driver's sheet's side by its angle, set or furled (`sheetAngleOf`)."""
    states = {
        "room": driver_by_the_wind("larboard", 45.0, bent=False, rig=rig),
        "set": driver_by_the_wind("larboard", 45.0, rig=rig),
        "furled": driver_by_the_wind("larboard", 45.0, SailState.FURLED, rig=rig),
    }
    got = run_js(tmp_path, states, DRIVER_STATES)
    _file, boom, _deck = _driver_file(states["room"]["graph"])
    length = boom["length_m"]
    room = got["room"]
    assert math.degrees(_sheet_of(states["room"], MIZEN_COURSE)) == pytest.approx(45.0)
    assert boom["rigged_out"] is False and room["boom"] == []
    assert room["boomEnd"] == pytest.approx([room["jaws"][0] - length, 0.0, room["jaws"][2]])
    assert room["course"]["state"] == "set" and room["driver"] is None
    assert not room["driverYards"]
    assert not [ln for ln in room["lines"] if ln["id"].startswith((DRIVER, DRIVER_BOOM))]
    assert [ln["cls"] for ln in room["lines"] if ln["id"].startswith(MIZEN_COURSE)] == ["sheet"]
    for name in ("set", "furled"):
        sheet = _sheet_of(states[name], DRIVER)
        assert math.degrees(sheet) == pytest.approx(45.0)
        jaws, end = got[name]["jaws"], got[name]["boomEnd"]
        assert jaws == pytest.approx(room["jaws"])
        # on the larboard tack the sheet's side is to starboard
        want = [jaws[0] - length * math.cos(sheet), length * math.sin(sheet), jaws[2]]
        assert end == pytest.approx(want), name
        (figure,) = got[name]["boom"]
        assert figure["pts"] == [pytest.approx(jaws), pytest.approx(end)], name


@needs_node
@pytest.mark.parametrize("rig", MIZEN_RIGS)
def test_a_drivers_boom_with_no_key_on_its_file_stands_as_b5_5_drew_it(tmp_path, rig):
    """Ext §17.11's toggle, "no file moves until it carries it". A driver's boom whose file does
    not say `rigged_out` is served true all the voyage, and is drawn as B5.5 drew it: amidships,
    level at its jaws, whatever the course's sheet, with the driver in the sail room (the figure
    the case above moved). With the driver bent, nothing of the whole drawing differs between no
    key and the boom rigged out: everything, its frame too, equal to the last figure."""
    room = driver_by_the_wind("larboard", 45.0, bent=False, rig=rig, key=False)
    states = {"room": room}
    for state in (SailState.SET, SailState.IN_THE_GEAR, SailState.FURLED):
        for key in (True, False):
            states[f"{state.value}-{key}"] = driver_by_the_wind(
                "larboard", 45.0, state, rig=rig, key=key
            )
    body = (
        DRIVER_DRAWN
        + """
        const whole = g => {
          const sk = P.buildSkeleton(g.graph, g.snap);
          return JSON.stringify({figures: sk.figures, frame: sk.frame});
        };
        const each = {};
        Object.keys(d).forEach(k => { each[k] = {drawn: drawn(d[k]), whole: whole(d[k])}; });
        return each;
    """
    )
    got = run_js(tmp_path, states, body)
    _file, boom, _deck = _driver_file(room["graph"])
    assert boom["rigged_out"] is True
    drawn = got["room"]["drawn"]
    jaws = drawn["jaws"]
    (figure,) = drawn["boom"]
    assert figure["pts"] == [
        pytest.approx(jaws),
        pytest.approx([jaws[0] - boom["length_m"], 0.0, jaws[2]]),
    ]
    assert drawn["course"]["state"] == "set" and drawn["driver"] is None
    for state in (SailState.SET, SailState.IN_THE_GEAR, SailState.FURLED):
        assert got[f"{state.value}-True"]["whole"] == got[f"{state.value}-False"]["whole"], state


@needs_node
@pytest.mark.parametrize("path", EVERY_SHIP)
def test_only_a_drivers_boom_goes_from_the_drawing_when_it_is_rigged_in(tmp_path, path):
    """The rule's key, every file: `rigged_out` false on a boom that a lateen cut at the mast
    names. Every boom of every file is served rigged in, as no file can say of a gaff sail's (the
    schema refuses it). A gaff sail's boom is drawn where it was, the whole drawing equal to the
    last figure; only a driver's goes, the 64's alone of the ten, and every other spar, a studding
    sail boom rigged in among them, keeps its figure."""
    served = ship_state(make_ship(path))
    rigged_in = json.loads(json.dumps(served))
    booms = {s["id"] for s in served["graph"]["spars"] if s["class"] == "boom"}
    for s in rigged_in["graph"]["spars"] + rigged_in["snap"]["spars"]:
        if s["id"] in booms:
            s["rigged_out"] = False
    body = """
        const out = {};
        Object.keys(d).forEach(k => {
          const sk = P.buildSkeleton(d[k].graph, d[k].snap);
          out[k] = {
            spars: sk.figures.filter(f => f.kind === 'spar').map(f => f.id),
            whole: JSON.stringify({figures: sk.figures, frame: sk.frame}),
          };
        });
        return out;
    """
    got = run_js(tmp_path, {"served": served, "rigged_in": rigged_in}, body)
    every = {s["id"] for s in served["graph"]["spars"]}
    of_a_cut = {
        s["roles"]["boom"]
        for s in served["graph"]["sails"]
        if s.get("cut_at_mast") and "boom" in s["roles"]
    }
    assert set(got["rigged_in"]["spars"]) == every - of_a_cut
    assert of_a_cut == ({DRIVER_BOOM} if path == SIXTY_FOUR else set())
    if not of_a_cut:
        assert got["rigged_in"]["whole"] == got["served"]["whole"]


@needs_node
def test_the_boom_rigged_in_is_read_from_the_state_then_from_the_graph(tmp_path):
    """Served `rigged_out`, the snapshot's before the graph's, and the graph's in a static
    drawing with no snapshot (`buildSkeleton(graph, null)`), each both ways. A bent driver on a
    boom rigged in, which only a boom carried away on the booms in its own phase leaves
    (test_driver.py, `test_a_boom_carried_away_in_its_own_phase_is_passed_over`): the sail is drawn,
    its foot where the boom is placed, with no boom and no sheet, for it has no end to be rove
    through; a sheet from a spar not drawn would stand in the air. A wreck of the boom follows the
    same rule, drawn out and not drawn in; cleared, not drawn either way, as every wreck. Only a
    served false takes it away: a graph and a state that say nothing of it, as no door of the game
    does, leave it standing."""
    out = driver_by_the_wind("larboard", 30.0, rig=FIXTURE)
    room = driver_by_the_wind("larboard", 30.0, bent=False, rig=FIXTURE)

    def served(data: dict, rigged_out: bool, state: str = "sound") -> dict:
        data = json.loads(json.dumps(data))
        spar = next(s for s in data["snap"]["spars"] if s["id"] == DRIVER_BOOM)
        spar["rigged_out"], spar["state"] = rigged_out, state
        return data

    unsaid = json.loads(json.dumps(room))
    for spar in unsaid["graph"]["spars"] + unsaid["snap"]["spars"]:
        if spar["id"] == DRIVER_BOOM:
            del spar["rigged_out"]
    states = {
        "bent, in": served(out, False),
        "room, out": served(room, True),
        "wreck, out": served(out, True, "wrecked"),
        "wreck, in": served(out, False, "wrecked"),
        "cleared, out": served(out, True, "cleared"),
        "out": out,
        "static, out": {"graph": out["graph"], "snap": None},
        "static, in": {"graph": room["graph"], "snap": None},
        "unsaid": unsaid,
    }
    got = run_js(tmp_path, states, DRIVER_STATES)

    def sheets(name: str) -> list:
        return [ln for ln in got[name]["lines"] if ln["id"] == f"{DRIVER}.sheet"]

    assert got["bent, in"]["boom"] == [] and sheets("bent, in") == []
    assert got["bent, in"]["driver"]["state"] == "set"
    assert got["bent, in"]["driver"]["corners"] == got["out"]["driver"]["corners"]
    assert len(got["out"]["boom"]) == 1 and len(sheets("out")) == 1
    assert len(got["room, out"]["boom"]) == 1 and got["room, out"]["driver"] is None
    assert [f["state"] for f in got["wreck, out"]["boom"]] == ["wrecked"]
    assert got["wreck, in"]["boom"] == [] and got["cleared, out"]["boom"] == []
    assert len(got["static, out"]["boom"]) == 1 and got["static, in"]["boom"] == []
    assert len(got["unsaid"]["boom"]) == 1


@needs_node
@pytest.mark.parametrize("rig", MIZEN_RIGS)
def test_the_driver_is_brailed_to_the_mast_and_furled_along_its_head(tmp_path, rig):
    """Ext §17.6: in the gear the driver is brailed to the mast as the course is, gathered to the
    mast and up under the yard, its foot hauled up the mast and its leech in along the head by
    the gear's depth (IN_GEAR_DEPTH, 0.35); furled, it is a bundle along its whole head, the
    yard's after part and the driver yard, aloft, out to its own peak. Its one sheet is rove
    through the boom's end, its tackle to the taffrail: it is drawn from the boom's end to the
    taffrail on the centreline, set or in the gear, and furled not at all. The yard and the boom
    stay where they were."""
    states = {
        st.value: driver_by_the_wind("larboard", state=st, rig=rig)
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
    taffrail = taffrail_of(graph)
    for drawn in (set_, gear):
        (sheet,) = [ln for ln in drawn["lines"] if ln["cls"] == "sheet"]
        assert sheet["id"] == f"{DRIVER}.sheet"
        assert sheet["pts"] == [pytest.approx(drawn["boomEnd"]), pytest.approx(taffrail)]
    assert not [ln for ln in furled["lines"] if ln["cls"] == "sheet"]  # furled: none drawn


@needs_node
@pytest.mark.parametrize("bent", [False, True])
@pytest.mark.parametrize("state", [SailState.SET, SailState.IN_THE_GEAR])
def test_her_after_sails_sheets_lead_to_her_own_taffrail(tmp_path, bent, state):
    """Ext §6.1 and §17.6 on the 64's own file: the course's sheet from its clew and the driver's
    from its boom's end, each to the rail's after end on her profile, on her centreline, not to
    the stern of a hull drawn without one, 2.97 m farther forward and 5.25 m lower."""
    data = driver_by_the_wind("larboard", state=state, bent=bent, rig=SIXTY_FOUR)
    got = run_js(tmp_path, data, DRIVER_FIGURES)
    hull = data["graph"]["hull"]
    rail = hull["profile"]["rail_m"][0]
    (sheet,) = [ln["pts"] for ln in got["lines"] if ln["cls"] == "sheet"]
    assert sheet[1] == pytest.approx([rail[0], 0.0, rail[1]], abs=1e-9)
    assert rail[0] == pytest.approx(-28.35, abs=0.01) and rail[1] == pytest.approx(8.53, abs=0.01)
    stern = [-0.52 * hull["length_waterline_m"], 0.0, 1.02 * hull["deck_height_m"]]
    assert sheet[1][0] - stern[0] == pytest.approx(-2.97, abs=0.01)
    assert sheet[1][2] - stern[2] == pytest.approx(5.25, abs=0.01)
    if bent:
        assert sheet[0] == pytest.approx(got["boomEnd"])
    elif state is SailState.SET:
        assert sheet[0] == pytest.approx(got["course"]["corners"][2])


# Each file's gaff sail on a boom (the 64's driver has its own cases, the lugger no boom)
BOOM_SAIL = {
    RAZEE: "mizzen.spanker",
    FRIGATE: "mizzen.spanker",
    BRIG: "main.spanker",
    MERCHANT_BRIG: "main.spanker",
    CUTTER: "main.sail",
    SMACK: "main.sail",
    SCHOONER: "main.sail",
    PRIVATEER: "main.sail",
}
# Across those states the frame itself is one on every file but the smack's: the top of it there
# is her gaff's peak as that stands sheeted, 0.09 m higher at 85 degrees heeled 0.3 rad. A gaff's,
# and no boom's, and as before her lines: recorded.
FRAME_STILL_MOVES_M = {SMACK: 0.092}
# And the schooners' ringtail, her boom sheeted 85 degrees and heeled 0.15 rad, bellies 0.29 m
# past the frame, in a state she does not sail: recorded. Every other file's stands within it.
RINGTAIL_PAST_THE_FRAME_M = {SCHOONER: 0.29, PRIVATEER: 0.29}
# How far the view's bounds moved as that sail was sheeted or she tacked, with its boom reached in
# the frame's four directions alone (the lead's "the eight taking it at SW-2's pictures"), metres,
# at the views below: old, each file with its profile taken away; new, on her own lines, none.
FRAME_MOVED_OLD_M = {
    RAZEE: 7.38,
    FRIGATE: 5.59,
    BRIG: 4.92,
    MERCHANT_BRIG: 4.92,
    CUTTER: 4.25,
    SMACK: 3.13,
    SCHOONER: 6.97,
    PRIVATEER: 6.97,
}
# Old, the sheet's end abaft her taffrail in the air by that sail's clew two metres aft, by the
# sheet at 18 degrees on the larboard tack: x (old, new) metres. New, the taffrail on the
# centreline.
SHEET_END_X_M = {
    RAZEE: (-37.48, -27.51),
    FRIGATE: (-30.93, -25.27),
    BRIG: (-22.00, -16.47),
    MERCHANT_BRIG: (-22.00, -16.47),
    CUTTER: (-14.43, -9.51),
    SMACK: (-10.43, -7.09),
    SCHOONER: (-22.11, -15.32),
    PRIVATEER: (-22.11, -15.32),
}


def on_her_boom(path: str, tack: str, sheet_deg: float, ringtail: bool = False) -> dict:
    """The file under plain sail on `tack`, her gaff sail on its boom set and sheeted `sheet_deg`
    off the centreline, with or without the ringtail set on its boom run out, where she carries
    one: the graph and snapshot."""
    ship = make_ship(path)
    for sid in ship.groups["plain sail"]:
        ship.sails[sid].state = SailState.SET
    sail = ship.sails[BOOM_SAIL[path]]
    sail.state = SailState.SET
    set_sheet_angle(ship, sail, math.radians(sheet_deg))
    data = ship_state(
        ship, awa=math.radians(60.0) * (1.0 if tack == "starboard" else -1.0), tack=tack
    )
    if ringtail:
        snap = next(s for s in data["snap"]["sails"] if s["id"] == "ringtail")
        snap["state"] = "set"
        boom = next(s for s in data["snap"]["spars"] if s["id"] == "ringtail_boom")
        boom["rigged_out"] = True
    return data


@needs_node
@pytest.mark.parametrize("path", list(BOOM_SAIL))
def test_the_frame_holds_her_boom_across_states_old_beside_new(tmp_path, path):
    """The fixed scale, every file with a gaff sail on a boom: the razee's boom is as long as the
    64's driver's, 19.9 m, and over her stern by 9 m. Reached in the frame's four directions alone
    it moved the bounds seen on the quarter by 7.4 m as it was sheeted or she tacked (the frigate's
    by 5.6 m), so on a hull drawn from her profile every boom's swing is reached every way, the
    ringtail boom's with it. The view's scale is the same on either tack, at any sheet, with the
    ringtail set or not, and every point of the boom, the gaff, the two sails and their lines
    within it. The bounds are held in what the view's scale reads (`ShipView.render`: both sides and
    the top); a sail's control points may reach under the sea line past the frame heeled 0.3 rad,
    the schooners' ringtail's by 0.57 m, which reads nothing. Old beside new, each file with its
    profile taken away: `FRAME_MOVED_OLD_M`."""
    ship = make_ship(path)
    roles = ship.sails[BOOM_SAIL[path]].roles
    carries_ringtail = (
        "ringtail" in ship.sails and ship.spars["ringtail_boom"].parent == roles["boom"]
    )
    sheets = (18.0, 45.0, 85.0)
    states = {
        f"{tack}-{sheet}-{ringtail}": on_her_boom(path, tack, sheet, ringtail)
        for tack in ("starboard", "larboard")
        for sheet in sheets
        for ringtail in ((False, True) if carries_ringtail else (False,))
    }
    ids = [roles["gaff"], roles["boom"], BOOM_SAIL[path], "ringtail_boom", "ringtail"]
    body = f"""
        const ids = {json.dumps(ids)};
        const mine = g => ids.includes(g.id) || ids.includes(g.of);
        const out = {{}};
        Object.keys(d).forEach(k => {{
          const sk = P.buildSkeleton(d[k].graph, d[k].snap);
          out[k] = [0, 45, 90, 135, 225].map(deg => {{
            const f = deg * Math.PI / 180;
            return {json.dumps(HEELS)}.map(h => {{
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
        }});
        return out;
    """
    got = run_js(tmp_path, states, body)
    first = got[next(iter(got))]
    tol = FRAME_STILL_MOVES_M.get(path, 1e-6)
    past = RINGTAIL_PAST_THE_FRAME_M.get(path, 1e-6)
    for name, views in got.items():
        for by_heel, same_by_heel in zip(views, first, strict=True):
            for heel, view, same in zip(HEELS, by_heel, same_by_heel, strict=True):
                assert view["n"] > 10 and view["over"] <= past, (name, heel, view["over"])
                for k in ("minX", "maxX", "minY", "maxY"):
                    assert view["frame"][k] == pytest.approx(same["frame"][k], abs=tol), (name, k)
                for k in ("minX", "maxX", "minY"):
                    bound = pytest.approx(same["bounds"][k], abs=max(tol, past))
                    assert view["bounds"][k] == bound, (name, k)
    # old: the same states with no profile, the four directions alone
    bare = {
        k: without_profile(on_her_boom(path, *k.split("-")[:1], float(k.split("-")[1])))
        for k in (f"{tack}-{sheet}" for tack in ("starboard", "larboard") for sheet in sheets)
    }
    old = run_js(
        tmp_path,
        bare,
        """
        const boxes = {};
        Object.keys(d).forEach(k => {
          const sk = P.buildSkeleton(d[k].graph, d[k].snap);
          [0, 45, 90, 135, 225].forEach(deg => [0, 0.17].forEach(h => {
            (boxes[deg + ' ' + h] = boxes[deg + ' ' + h] || [])
              .push(P.project(sk, deg * Math.PI / 180, h).bounds);
          }));
        });
        let spread = 0;
        Object.keys(boxes).forEach(key => ['minX', 'maxX', 'minY', 'maxY'].forEach(k => {
          const vs = boxes[key].map(b => b[k]);
          spread = Math.max(spread, Math.max(...vs) - Math.min(...vs));
        }));
        return spread;
        """,
    )
    assert old == pytest.approx(FRAME_MOVED_OLD_M[path], abs=0.01)


@needs_node
@pytest.mark.parametrize("sheet_deg", [18.0, 45.0, 85.0])
@pytest.mark.parametrize("tack", ["starboard", "larboard"])
@pytest.mark.parametrize("path", list(BOOM_SAIL))
def test_her_boom_sails_sheet_leads_from_its_boom_to_her_own_taffrail(
    tmp_path, path, tack, sheet_deg
):
    """On a hull drawn from her profile a boom sail's sheet runs from the boom's end to the taffrail
    on the centreline, as the driver's does (Ext §17.6). Old, to the side 2 m abaft the clew: on
    the razee, whose boom overhangs her taffrail by 9 m, a lead 11 m abaft her stern at her deck's
    datum, in the air; on the eight 3.3 to 6.8 m abaft theirs (`SHEET_END_X_M`). A hull with no
    profile keeps that lead."""
    data = on_her_boom(path, tack, sheet_deg)
    sail, graph = BOOM_SAIL[path], data["graph"]
    boom_id = next(s for s in graph["sails"] if s["id"] == sail)["roles"]["boom"]
    body = f"""
        const sk = P.buildSkeleton(d.graph, d.snap);
        return {{boomEnd: sk.spars['{boom_id}'].b,
                 sheets: sk.figures.filter(f => f.kind === 'line' && f.cls === 'sheet' &&
                                                f.of === '{sail}').map(f => f.pts)}};
    """
    got = run_js(tmp_path, data, body)
    hull = graph["hull"]
    taffrail = taffrail_of(graph)
    assert got["sheets"] == [[pytest.approx(got["boomEnd"]), pytest.approx(taffrail, abs=1e-9)]]
    old_x, new_x = SHEET_END_X_M[path]
    assert taffrail[0] == pytest.approx(new_x, abs=0.005)
    if path == RAZEE and sheet_deg == 18.0:  # by the wind she carries it out far beyond her stern
        assert got["boomEnd"][0] < taffrail[0] - 5.0
    without_profile(data)
    bare = run_js(tmp_path, data, body)
    lee = 1.0 if tack == "larboard" else -1.0
    end = bare["boomEnd"]
    lead = [end[0] - 2.0, lee * hull["beam_m"] / 2.0, hull["deck_height_m"]]
    assert bare["sheets"] == [[pytest.approx(end), pytest.approx(lead)]]
    if tack == "larboard" and sheet_deg == 18.0:
        assert lead[0] == pytest.approx(old_x, abs=0.005)


HEAD_ROOM_M = 6.0 * 0.3048  # the 64's driver boom's (Bel §1.5, §4.6; the lead's note of 2026-10-29)
# Each file's boom, level from its jaws, from them to her taffrail: its least over her drawn decks
# and over her rail, metres. The eight's are measured at the hull step's landing and recorded, not
# ruled: no spar moves in it (Build-Ships.md §5.6, §5.0 principle 8). Under the rail, a negative:
# the frigate's boom runs 0.10 m under her quarterdeck and 1.83 m under her taffrail, the brigs'
# 0.38 m under theirs, the smack's 0.11 m, the schooners' 0.02 m; a rig's heights against the drawn
# lines are a later package's, for the owner's eye first.
BOOM_CLEAR_M = {
    SIXTY_FOUR: (HEAD_ROOM_M, 1.16),
    RAZEE: (1.15, 0.01),
    FRIGATE: (-0.10, -1.83),
    BRIG: (1.63, -0.38),
    MERCHANT_BRIG: (1.63, -0.38),
    CUTTER: (1.68, 0.57),
    SMACK: (0.87, -0.11),
    SCHOONER: (1.25, -0.02),
    PRIVATEER: (1.25, -0.02),
}


@needs_node
@pytest.mark.parametrize("path", list(BOOM_CLEAR_M))
def test_her_booms_and_her_courses_foot_stand_clear_of_her_drawn_decks(tmp_path, path):
    """The clew check (Bel §1.5) and the lead's rulings of 2026-10-30 as they are drawn, the after
    sail at no sheet, in the fore-and-aft plane. The boom, level from its jaws, stands over her
    drawn decks and her rail as far aft as she goes, by `BOOM_CLEAR_M`. Old beside new: the 64's
    2.26 m and 1.59 m to 1.83 m (6 ft, the head room still set by it) and 1.16 m; the razee's 1.84 m
    and 0.70 m to 1.15 m and 0.01 m, literally the least that clears her taffrail (at stage A, 0.20
    m and 1.33 m under them). The 64's course, Steel's words read from the deck its mast stands
    through, stands 1.84 to 1.14 m over her roundhouse deck at its clew, and no lower than 1.6 to
    0.9 m with the drawn sag of its foot."""
    ship = make_ship(path)
    for sid in ship.groups["plain sail"]:
        ship.sails[sid].state = SailState.SET
    for sail in ship.sails.values():
        sail.sheet_angle = 0.0
    data = ship_state(ship)
    (boom,) = [s["id"] for s in data["graph"]["spars"] if s["class"] == "boom"]
    got = run_js(
        tmp_path,
        {**data, "boom": boom},
        """
        const sk = P.buildSkeleton(d.graph, d.snap);
        const f = sk.figures.find(x => x.kind === 'sail' && x.id === 'mizzen.course');
        const b = sk.spars[d.boom];
        return {a: b.a, b: b.b,
                course: f ? {corners: f.corners, path: P.flattenPath(f.path)} : null};
        """,
    )
    profile = ship.hull.spec.profile
    jaws, end = got["a"], got["b"]
    assert jaws[1:] == [0.0, end[2]] and end[1] == pytest.approx(0.0, abs=1e-9)
    taffrail = profile.rail_m[0][0]
    assert end[0] < taffrail < jaws[0]  # she carries it out beyond her stern
    stations = [taffrail + 0.25 * i for i in range(int((jaws[0] - taffrail) / 0.25) + 1)]
    over_deck, over_rail = BOOM_CLEAR_M[path]
    assert min(jaws[2] - deck_at(profile, x) for x in stations) >= over_deck - 1e-2
    assert min(jaws[2] - interp(profile.rail_m, x) for x in stations) >= over_rail - 5e-3
    if got["course"]:
        clew = got["course"]["corners"][2]
        assert clew[2] - deck_at(profile, clew[0]) == pytest.approx(1.14, abs=0.02)
        over = [p[2] - deck_at(profile, p[0]) for p in got["course"]["path"]]
        assert min(over) >= 0.9
    else:
        assert path != SIXTY_FOUR  # the course is hers alone


@needs_node
@pytest.mark.parametrize(
    "state, sheet_deg",
    [
        ("as she starts", 0.0),
        ("furled", 25.0),
        ("in_the_gear", 25.0),
        ("set", 0.0),
        ("set", 18.0),
        ("set", 30.0),
    ],
)
def test_the_razees_spanker_stands_clear_of_the_taffrail_its_boom_clears(
    tmp_path, state, sheet_deg
):
    """The lead's ruling of 2026-10-30 as it is drawn: the boom literally the least that clears her
    taffrail, so its sail must not be drawn through it. Her spanker's foot is laced along its boom,
    with no sag below it, and furled it lies on the boom. Old beside new: the set foot's lowest 6.54
    m above the datum (0.62 m under the boom, by a square sail's sag) and the furled bundle's 6.81 m
    (0.35 m under it), against her taffrail's 7.15 m, to 7.16 m, the boom's. Its head and its leech
    are unmoved, and every other sail: `cutG` is hers alone among the ten."""
    ship = make_ship(RAZEE)
    if state != "as she starts":
        for sid in ship.groups["plain sail"]:
            ship.sails[sid].state = SailState.SET
        ship.sails["mizzen.spanker"].state = SailState[state.upper()]
        ship.sails["mizzen.spanker"].sheet_angle = math.radians(sheet_deg)
    got = run_js(
        tmp_path,
        ship_state(ship),
        """
        const sk = P.buildSkeleton(d.graph, d.snap);
        const f = sk.figures.find(x => x.kind === 'sail' && x.id === 'mizzen.spanker');
        const b = sk.spars['mizzen.boom'];
        return {state: f.state, boom: b.a[2], path: P.flattenPath(f.path)};
        """,
    )
    assert got["state"] == ("furled" if state == "as she starts" else state)
    assert got["boom"] == pytest.approx(7.16, abs=0.01)
    lowest = min(point[2] for point in got["path"])
    assert lowest >= ship.hull.spec.profile.rail_m[0][1]
    assert lowest == pytest.approx(got["boom"], abs=1e-6)


@needs_node
@pytest.mark.parametrize("path", [p for p in PROFILED if p not in (LUGGER, *PILOT)])
def test_every_other_gaff_sail_keeps_the_foot_and_the_bundle_it_was_drawn_with(tmp_path, path):
    """The razee's spanker alone is drawn laced along its boom (`gaffCutOn`, which asks for a
    profile and four filed corners, and no gaff sail of the eight files them). On the seven files
    with a gaff sail on a boom the set foot still sags under the boom (measured 0.50-0.88 m) and
    the furled bundle hangs under it (0.26-0.33 m), as at `af9f13d`, on their own lines as before
    them: her mend moves no figure of theirs."""
    bands = {SailState.SET: (0.4, 1.0), SailState.FURLED: (0.2, 0.4)}
    for state, (least, most) in bands.items():
        ship = make_ship(path)
        for sail in ship.sails.values():
            if sail.cls == "gaff":
                sail.state = state
        got = run_js(
            tmp_path,
            ship_state(ship),
            """
            const sk = P.buildSkeleton(d.graph, d.snap);
            return d.graph.sails.filter(s => s.class === 'gaff' && (s.roles || {}).boom).map(s => {
              const f = sk.figures.find(x => x.kind === 'sail' && x.id === s.id);
              const lowest = Math.min(...P.flattenPath(f.path).map(p => p[2]));
              return sk.spars[s.roles.boom].a[2] - lowest;
            });
            """,
        )
        assert got, path
        for under in got:
            assert least <= under <= most, (path, state)


@needs_node
def test_the_razees_spanker_is_drawn_on_its_files_cut(tmp_path):
    """Her gaff sail with its four corners filed, on a hull drawn from her profile: at no sheet its
    tack, throat, peak and clew on the file's, within the rounding, its gaff at the file's peak and
    its head and foot along the gaff and the boom, which it does not fill; the area the file's.
    Old beside new, by the fixed rule: the gaff at 35 degrees and the whole of both spars, the peak
    (-27.10, 24.60) to (-25.53, 24.69), the clew's x -36.48 to -34.50, 215 to 191 m2 against the
    filed 191 (the owner's measure, Steel's 202 for a 38: drawn +6.5% to -5.5%, filed -5.4%); on the
    boom at her taffrail (the lead's ruling of 2026-10-30) the clew's x -34.47, the area 200 m2
    filed and drawn, -1%."""
    ship = make_ship(RAZEE)
    for sid in ship.groups["plain sail"]:
        ship.sails[sid].state = SailState.SET
    for sail in ship.sails.values():
        sail.sheet_angle = 0.0
    got = run_js(
        tmp_path,
        ship_state(ship),
        """
        const sk = P.buildSkeleton(d.graph, d.snap);
        const f = sk.figures.find(x => x.kind === 'sail' && x.id === 'mizzen.spanker');
        const g = sk.spars['mizzen.gaff'], b = sk.spars['mizzen.boom'];
        return {corners: f.corners, gaff: [g.a, g.b], boom: [b.a, b.b]};
        """,
    )
    spanker = ship.sails["mizzen.spanker"]
    deck = ship.hull.spec.deck_height_m
    tack, throat, peak, clew = [[x, 0.0, z + deck] for x, z in spanker.corners_m]
    drawn_throat, drawn_peak, drawn_clew, drawn_tack = got["corners"]
    for drawn, filed in (
        (drawn_tack, tack),
        (drawn_throat, throat),
        (drawn_peak, peak),
        (drawn_clew, clew),
    ):
        assert drawn == pytest.approx(filed, abs=0.03)
    drawn = [(p[0], p[2]) for p in got["corners"]]
    area = 0.5 * abs(
        sum(
            x1 * z2 - x2 * z1
            for (x1, z1), (x2, z2) in zip(drawn, drawn[1:] + drawn[:1], strict=True)
        )
    )
    assert area == pytest.approx(spanker.area_m2, abs=0.5)
    (gaff_a, gaff_b), (boom_a, boom_b) = got["gaff"], got["boom"]
    assert math.dist(gaff_a, gaff_b) > math.dist(gaff_a, drawn_peak)
    run, rise = gaff_a[0] - gaff_b[0], gaff_b[2] - gaff_a[2]
    assert math.degrees(math.atan2(rise, run)) == pytest.approx(40.0, abs=0.5)
    assert math.dist(boom_a, boom_b) > math.dist(boom_a, drawn_clew)
    assert drawn_tack == pytest.approx(boom_a)


# The least the storm mizzen's foot stands over the deck under it, metres: over 0.1 on the 64 and
# the razee, and the frigate's 0.041, measured at no sheet at its clew, where her quarterdeck rises
STORM_MIZZEN_CLEAR_M = {SIXTY_FOUR: 0.1, RAZEE: 0.1, FRIGATE: 0.04}


@needs_node
@pytest.mark.parametrize("path", list(STORM_MIZZEN_CLEAR_M))
@pytest.mark.parametrize("sheet_deg", [0.0, 25.0])
def test_her_storm_mizzens_foot_stands_clear_of_her_drawn_deck(tmp_path, path, sheet_deg):
    """The clew check's reason on her storm mizzen (old, the 64's foot 0.05-0.91 m under her
    roundhouse deck, the razee's 0.93-0.95 m): cut from the quarterdeck, its foot ran through the
    deck she carries over it. Its tack stands at her rail over the foot's run, and drawn, at no
    sheet and sheeted, the foot from tack to clew stands over the deck under it: every file that
    carries a storm mizzen, the rest a storm trysail on the boom."""
    ship = make_ship(path)
    after = "mizzen.course" if "mizzen.course" in ship.sails else "mizzen.spanker"
    ship.sails[after].state = SailState.UNBENT
    storm = ship.sails["storm_mizzen"]
    storm.state = SailState.SET
    storm.sheet_angle = math.radians(sheet_deg)
    got = run_js(
        tmp_path,
        ship_state(ship),
        """
        const sk = P.buildSkeleton(d.graph, d.snap);
        const f = sk.figures.find(x => x.kind === 'sail' && x.id === 'storm_mizzen');
        return {corners: f.corners};
        """,
    )
    profile = ship.hull.spec.profile
    tack, clew = got["corners"][0], got["corners"][-1]
    if tack[2] > clew[2] + 1.0:  # the corners run from the peak: take the foot's two ends
        tack = got["corners"][1]
    assert abs(tack[2] - clew[2]) < 1e-6
    for t in [i / 8.0 for i in range(9)]:
        x = tack[0] + t * (clew[0] - tack[0])
        assert tack[2] - deck_at(profile, x) > STORM_MIZZEN_CLEAR_M[path], x


@needs_node
@pytest.mark.parametrize("facing_deg", [150.0, 180.0, 210.0, 0.0, 30.0, 330.0])
@pytest.mark.parametrize("rig", MIZEN_RIGS)
def test_the_mizen_yards_after_part_stands_on_its_own_side_of_the_mizzen_topsail(
    tmp_path, facing_deg, rig
):
    """The mizen yard is cut at its truss into two pieces, each sorted at its own middle. Its after
    part stands up to 8.3 m abaft the mizzen topsail: seen from aft it is drawn over that sail,
    with the course it carries behind it; seen from forward, behind it. As one figure, sorted at
    the yard's middle, the topsail hid it from astern and it crossed the topsail from the bow."""
    facing = math.radians(facing_deg)
    body = f"""
        const sk = P.buildSkeleton(d.graph, d.snap);
        return P.project(sk, {facing}, 0).figures.map(f => [f.id, f.kind, f.piece || null]);
    """
    data = mizen_by_the_wind("larboard", 30.0, rig=rig)
    ids = [tuple(fig) for fig in run_js(tmp_path, data, body)]
    after = ids.index(("mizzen.yard", "spar", None))
    fore = ids.index(("mizzen.yard", "spar", "fore"))
    topsail = ids.index(("mizzen.topsail", "sail", None))
    course = ids.index((MIZEN_COURSE, "sail", None))
    assert after != fore
    if abs(facing_deg - 180.0) <= 90.0:  # seen from aft: the farther drawn first
        assert topsail < after and topsail < course
    else:
        assert after < topsail and course < topsail
    assert sum(1 for i in ids if i[0] == "mizzen.yard") == 2


@needs_node
@pytest.mark.parametrize("sail", [MIZEN_COURSE, DRIVER])
@pytest.mark.parametrize("sheet_deg", [0.0, 30.0, 60.0])
def test_a_luff_laced_to_the_mast_lies_on_the_mast(tmp_path, sail, sheet_deg):
    """On her file the course and the driver are laced to the mast, so the drawn luff stays on it
    however the sail is sheeted: it bellied as a leech does, standing 1.02 m off the mast (the
    course) and 0.93 m (the driver) at a sheet of 30 degrees."""
    data = driver_by_the_wind("larboard", sheet_deg, bent=sail == DRIVER, rig=SIXTY_FOUR)
    body = f"""
        const sk = P.buildSkeleton(d.graph, d.snap);
        const m = sk.spars['mizzen.mast'];
        const f = sk.figures.find(x => x.kind === 'sail' && x.id === '{sail}');
        const pts = P.flattenPath(f.path);
        return pts.slice(-3).map(p => Math.hypot(p[0] - m.xAt(p[2]), p[1]));
    """
    assert max(run_js(tmp_path, data, body)) < 0.01


@needs_node
@pytest.mark.parametrize("path", PROFILED)
@pytest.mark.parametrize("tack", ["starboard", "larboard"])
def test_her_headsails_sheets_lead_to_her_drawn_side_abaft_the_fore_mast(tmp_path, path, tack):
    """Every jib-headed sail forward of her foremost mast has its sheet from its clew aft to her
    drawn side a metre abaft that mast, at the deck, as the spritsail's. The rule a hull with no
    profile keeps, two metres abaft the clew and half the beam out, stops abreast the knee of the
    head on the 64's hull (the jib's, at x 29.10 m, y 6.77 m), in the air where she has no
    breadth."""
    ship = make_ship(path)
    for sid in ship.groups["plain sail"]:
        ship.sails[sid].state = SailState.SET
    fore_x = max(s.x_m for s in ship.spars.values() if s.cls == "mast")
    heads = {
        s.id
        for s in ship.sails.values()
        if s.cls == "jibheaded" and s.x_m > fore_x and s.state is not SailState.UNBENT
    }
    assert heads
    for sid in heads:
        ship.sails[sid].state = SailState.SET
    awa = math.radians(60.0) * (1.0 if tack == "starboard" else -1.0)
    data = ship_state(ship, awa=awa, tack=tack)
    got = run_js(
        tmp_path,
        data,
        """
        const sk = P.buildSkeleton(d.graph, d.snap);
        const of = {};
        sk.figures.filter(f => f.kind === 'sail').forEach(f => { of[f.id] = f.corners; });
        const masts = d.graph.spars.filter(s => s.class === 'mast').map(s => sk.spars[s.id].x);
        return {foreX: Math.max(...masts), of: of, lines: sk.figures
          .filter(f => f.kind === 'line' && f.cls === 'sheet').map(f => [f.of, f.pts])};
        """,
    )
    deck = data["graph"]["hull"]["deck_height_m"]
    x = got["foreX"] - 1.0
    out = form.half_breadth_at(ship.hull.spec, x, deck)
    assert 0.0 < out < data["graph"]["hull"]["beam_m"] / 2.0
    head = [ln for ln in got["lines"] if ln[0] in heads]
    assert {ln[0] for ln in head} == heads
    for sid, (clew, lead) in head:
        assert clew == pytest.approx(got["of"][sid][2]), sid
        assert lead[0] == pytest.approx(x), sid
        assert abs(lead[1]) == pytest.approx(out, abs=1e-3), sid
        assert lead[2] == pytest.approx(deck), sid


@needs_node
@pytest.mark.parametrize("rig", MIZEN_RIGS)
@pytest.mark.parametrize("facing_deg", [0.0, 45.0, 90.0, 135.0, 225.0])
def test_the_frame_holds_the_drivers_boom_beyond_the_taffrail_across_states(
    tmp_path, facing_deg, rig
):
    """Ext §17.6: `fullRigFrame` holds the boom's swing, which reaches far beyond the taffrail,
    every way about its jaws (with the four directions alone the boom sheeted 45 degrees moved
    the bounds seen on the quarter, measured), and the driver's peak on its driver yard about
    the yard's truss, so every point of the yard, the boom, the two after sails, the driver yard
    and their lines lies within the frame alone, upright or heeled; and the view's scale is the
    same on either tack, at any sheet, set, in the gear or furled, with the driver bent or in
    the sail room, its boom rigged in and not drawn (Ext §17.11). The frame reaches aft to the
    boom's end, beyond the taffrail."""
    states = {
        f"{tack}-{sheet}-{state.value}-{'driver' if bent else 'course'}": driver_by_the_wind(
            tack, sheet, state, bent, rig
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
    taffrail_x = taffrail_of(graph)[0]
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


def shifted_for_the_driver_and_back(rig: str) -> dict[str, dict]:
    """Through the engine's own shift (B3.5, `shift_sail`; Ext §17.11), with the course set and
    sheeted: "shift the mizen for the driver" and then "shift the driver for the mizen", run to
    their ends on a bare ship. The graph and snapshot at each change of the two sails' states and
    sheets and of the boom's being rigged out, eleven, in their order: the course set, brailed,
    both unbent; the boom out; the driver furled, set, brailed, both unbent; the boom in; the
    course furled, set. (Nine before the boom went with the driver, Ext §17.11.)"""
    ship = driver_ship(rig, bent=False)
    runner = Runner(ship)
    awa = math.radians(-30.0)  # on the larboard bow, as test_driver.py's bare ship
    ship.dyn.apparent_wind_angle, ship.dyn.apparent_wind_speed = awa, 6.0
    light_airs = Wind(WindParams.from_nautical(0.0, 3.0, 0.0, 0.0), random.Random(0))
    course, driver = ship.sails[MIZEN_COURSE], ship.sails[DRIVER]
    boom = ship.spars[DRIVER_BOOM]
    course.state = SailState.SET
    set_sheet_angle(ship, course, math.radians(30.0))
    states: dict[str, dict] = {}
    seen: list[tuple] = []

    def draw_if_changed() -> None:
        key = (
            course.state.value,
            driver.state.value,
            boom.rigged_out,
            course.sheet_angle,
            driver.sheet_angle,
        )
        if not seen or key != seen[-1]:
            seen.append(key)
            states[f"{len(states)} {key[:3]}"] = ship_state(ship, awa=awa, tack="larboard")

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
    assert boom.rigged_out is False
    assert len(states) == 11, list(states)
    return states


@needs_node
@pytest.mark.parametrize("rig", MIZEN_RIGS)
def test_the_yard_stays_on_the_courses_line_as_the_mizen_is_shifted_for_the_driver_and_back(
    tmp_path, rig
):
    """Ext §17.6, through the engine's own shift (`shifted_for_the_driver_and_back`). Throughout,
    the yard is slung at the same truss, and its heel and peak lie as far from the mast and as high
    along it as with the course set: it swings with the sheet of the sail bent on it and never runs
    out to the driver's peak. Only a bent sail is drawn, never both. The boom (Ext §17.11, old
    beside new): old, drawn in all nine states, amidships until the driver is bent; new, drawn only
    while it is rigged out, from its own phase before the bend to its own phase after the unbend,
    amidships until the driver is bent, and after by the driver's sheet (on a bare ship the shift
    leaves it at no angle); placed there in every state."""
    states = shifted_for_the_driver_and_back(rig)
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
        out = next(s for s in states[name]["snap"]["spars"] if s["id"] == DRIVER_BOOM)
        assert [f["pts"] for f in drawn["boom"]] == (
            [[pytest.approx(jaws), pytest.approx(drawn["boomEnd"])]] if out["rigged_out"] else []
        ), name
    # the course bent, then neither while the driver is swayed up, then the driver, and back
    assert seen_bent == {(MIZEN_COURSE,), (), (DRIVER,)}
    assert any(d["driver"] and d["driver"]["state"] == "set" for d in got.values())
    # out from the fourth state to the eighth: bare, furled, set, brailed and bare again
    assert [bool(d["boom"]) for d in got.values()] == [False] * 3 + [True] * 5 + [False] * 3


# The view's frame and bounds in each of `d`'s states, at five facings and every heel, and how
# far aft the frame reaches.
SHIFT_FRAMES = f"""
    const out = {{}};
    Object.keys(d).forEach(k => {{
      const sk = P.buildSkeleton(d[k].graph, d[k].snap);
      const views = [];
      [0, Math.PI / 4, Math.PI / 2, 3 * Math.PI / 4, 5 * Math.PI / 4].forEach(f => {{
        {json.dumps(HEELS)}.forEach(h => {{
          const proj = P.makeProjector(f, h);
          const fr = sk.frame.map(proj);
          const xs = fr.map(p => p.x), ys = fr.map(p => p.y);
          views.push({{frame: {{minX: Math.min(...xs), maxX: Math.max(...xs),
                                minY: Math.min(...ys), maxY: Math.max(...ys)}},
                       bounds: P.project(sk, f, h).bounds}});
        }});
      }});
      const b = sk.spars['mizzen.boom'];
      out[k] = {{views: views, aft: Math.min(...sk.frame.map(p => p[0])),
                 boomEnd: b.a[0] - b.spec.length_m}};
    }});
    return out;
"""


def _frames_are_one(got: dict) -> None:
    """Every state's frame and bounds equal the first's, at every facing and heel, and the frame
    reaches aft to the boom's end."""
    first = got[next(iter(got))]["views"]
    for name, drawn in got.items():
        assert drawn["aft"] <= drawn["boomEnd"] + 1e-9, name
        for view, same in zip(drawn["views"], first, strict=True):
            for k in ("minX", "maxX", "minY", "maxY"):
                assert view["frame"][k] == pytest.approx(same["frame"][k], abs=1e-6), (name, k)
                assert view["bounds"][k] == pytest.approx(same["bounds"][k], abs=1e-6), (name, k)


@needs_node
@pytest.mark.parametrize("rig", MIZEN_RIGS)
def test_the_frame_is_equal_across_the_shift_and_back(tmp_path, rig):
    """Ext §17.11: the boom's swing stays in the fixed frame rigged in as rigged out, so the view
    does not rescale at the shift. In all eleven states of the engine's own shift and back, the boom
    drawn in five of them, the frame and the view's bounds are equal at five facings and every heel,
    and the frame reaches aft to the boom's end, beyond the taffrail."""
    states = shifted_for_the_driver_and_back(rig)
    got = run_js(tmp_path, states, SHIFT_FRAMES)
    _frames_are_one(got)
    graph = next(iter(states.values()))["graph"]
    assert got[next(iter(got))]["aft"] < taffrail_of(graph)[0]


@needs_node
@pytest.mark.parametrize("rig", MIZEN_RIGS)
def test_the_driver_as_the_game_serves_it_is_drawn_on_its_boom(tmp_path, rig):
    """The bent rig's world through the game's own doors (`/api/ship`, `/api/state`): the
    graph serves the driver's cut and its boom among its roles, and the state the course
    unbent; the drawing takes them as above. As she starts, the driver furled at no sheet: the
    yard on the course's line in the fore-and-aft plane, the boom amidships, the driver a bundle
    along its head with its driver yard beyond the yard's peak, and no sheet drawn. Set and
    sheeted, the boom and the driver lie to leeward of the tack the state gives, the yard's fore
    part to windward, and the sheet runs from the boom's end to the taffrail."""
    pytest.importorskip("fastapi")
    from fastapi.testclient import TestClient

    from freesail.ui.server import Driver, create_app

    path = write_ship(frigate_with_driver_doc(bent=True), tmp_path) if rig == FIXTURE else rig
    scenario = Scenario(wind_from_deg=0.0, wind_speed_kn=10.0, ship_heading_deg=60.0)
    world = make_world(7, str(path), scenario)
    if rig != FIXTURE:  # she is filed with the course bent: the shift's end, as the fixture's doc
        world.ship.sails[MIZEN_COURSE].state = SailState.UNBENT
        world.ship.sails[DRIVER].state = SailState.FURLED
        world.ship.spars[DRIVER_BOOM].rigged_out = True  # out with it (Ext §17.11)
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
    assert len(furled["boom"]) == 1
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
    assert sheet == [
        pytest.approx(set_["boomEnd"]),
        pytest.approx(taffrail_of(start["graph"]), abs=1e-9),
    ]


@needs_node
def test_the_boom_goes_out_and_comes_in_with_the_driver_through_the_games_own_routes(tmp_path):
    """Ext §17.11 through the game's own doors, on the fixture as the game loads her: `/api/order`
    for the orders, `/api/driver` for the clock, `/api/ship` and `/api/state` for what is drawn. As
    she starts the boom is served rigged in by both, and not drawn. "Shift the mizen for the
    driver": the boom is served out, and drawn amidships, before the driver is bent; then the driver
    on it, furled. "Set the driver": its sheet from the boom's end. "Shift the driver for the
    mizen": the driver down, then the boom served in and gone from the drawing before the course
    goes up. The view's frame and bounds are one through all of it."""
    pytest.importorskip("fastapi")
    from fastapi.testclient import TestClient

    from freesail.ui.server import Driver, create_app

    scenario = Scenario(
        wind_from_deg=0.0,
        wind_speed_kn=10.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=240.0,
        ship_speed_kn=4.0,
    )
    world = make_world(7, write_ship(frigate_with_driver_doc(), tmp_path), scenario)
    states: dict[str, dict] = {}
    seen: list[tuple] = []

    with TestClient(create_app(Driver(world))) as client:

        def look() -> None:
            """The two doors the page reads, kept at each change of what they serve of the rig."""
            snap = client.get("/api/state").json()
            sails = {s["id"]: s["state"] for s in snap["sails"]}
            spars = {s["id"]: s["rigged_out"] for s in snap["spars"]}
            key = (sails[MIZEN_COURSE], sails[DRIVER], spars[DRIVER_BOOM])
            if not seen or key != seen[-1]:
                seen.append(key)
                graph = client.get("/api/ship").json()
                states[f"{len(states)} {key}"] = {"graph": graph, "snap": snap}

        def do(text: str, done) -> None:
            """The order by its door, and the clock by its door until `done` of what is served."""
            assert client.post("/api/order", json={"text": text}).json()["kind"] == "order.accepted"
            for _ in range(200):
                tick = client.post("/api/driver", json={"action": "tick", "value": 20})
                assert tick.status_code == 200
                look()
                if done(seen[-1]):
                    return
            raise AssertionError(f"{text}: {seen}")

        client.post("/api/driver", json={"action": "tick", "value": 1})
        look()
        do("shift the mizen for the driver", lambda key: key[1] == "furled")
        do("set the driver", lambda key: key[1] == "set")
        do("shift the driver for the mizen", lambda key: key[0] == "set")

    start = next(iter(states.values()))
    assert seen[0][1:] == ("unbent", False)
    boom_served = next(s for s in start["graph"]["spars"] if s["id"] == DRIVER_BOOM)
    assert boom_served["rigged_out"] is False
    got = run_js(tmp_path, states, DRIVER_STATES)
    # (course, driver, boom out), each in turn as the doors served it, the boom's figure beside it
    drawn = [got[name] for name in states]
    assert [bool(d["boom"]) for d in drawn] == [key[2] for key in seen]
    assert [d["driver"] is not None for d in drawn] == [key[1] != "unbent" for key in seen]
    # out before the driver is bent, and it lies amidships then
    bare_and_out = seen.index(("unbent", "unbent", True))
    (figure,) = drawn[bare_and_out]["boom"]
    assert figure["pts"][1][1] == pytest.approx(0.0)
    assert seen.index(("unbent", "furled", True)) == bare_and_out + 1
    # in after the driver is down, and before the course goes up
    bare_and_in = len(seen) - 1 - seen[::-1].index(("unbent", "unbent", False))
    assert seen[bare_and_in - 1] == ("unbent", "unbent", True)
    assert seen[bare_and_in + 1][0] != "unbent"
    assert drawn[bare_and_in]["boom"] == [] and seen[-1][2] is False
    # set: its sheet from the boom's end; the course back at the end: its own sheet, no boom
    (set_, end) = (drawn[seen.index(("unbent", "set", True))], drawn[-1])
    (sheet,) = [ln["pts"] for ln in set_["lines"] if ln["id"] == f"{DRIVER}.sheet"]
    assert sheet[0] == pytest.approx(set_["boomEnd"])
    assert end["course"]["state"] == "set" and end["boom"] == [] and end["driver"] is None
    assert not [ln for ln in end["lines"] if ln["id"].startswith(DRIVER)]
    _frames_are_one(run_js(tmp_path, states, SHIFT_FRAMES))


# -- the painter's order of a hull drawn from her profile (the hull step's landing) ---------------

SWEEP = """
    const whole = P.buildSkeleton(d.graph, d.snap);
    const hull = whole.figures.filter(f => f.kind === 'hull');
    const sk = d.hullOnly ? {figures: hull, frame: []} : whole;
    const out = [];
    for (let deg = 0; deg < 360; deg += 15) {
      for (const heel of [0, 0.1, -0.1, 0.2, -0.2]) {
        const scene = P.project(sk, deg * Math.PI / 180, heel);
        out.push({deg, heel, figures: scene.figures.map(f => ({
          kind: f.kind, part: f.part || null, cls: f.cls || null, side: f.side || null,
          layer: f.layer || null, depth: f.depth, id: f.id || null, at: f.at,
          faces: f.faces || null}))});
      }
    }
    return out;
"""


def sweep_of(tmp_path, path, *, hull_only=False):
    return run_js(tmp_path, {**ship_state(make_ship(path)), "hullOnly": hull_only}, SWEEP)


def toward(deg: int) -> tuple[float, float]:
    return math.cos(math.radians(deg)), math.sin(math.radians(deg))


@needs_node
def test_a_lug_at_the_stern_stands_before_the_quarter_and_abaft_it_behind(tmp_path):
    """The lugger's mizen lug, her mast at the stern, from ahead: cut at the mast, its fore part
    inboard of her quarter's faces seen from inside is painted after them, in front of her bulwark;
    its after part, abaft her stern and beyond their planes, stays before them."""
    state = ship_state(make_ship(LUGGER))
    views = run_js(tmp_path, {**state, "hullOnly": False}, SWEEP)
    view = next(v for v in views if v["deg"] == 0 and v["heel"] == 0)
    figures = view["figures"]
    pieces = [i for i, f in enumerate(figures) if f["kind"] == "sail" and f["id"] == "mizen.lug"]
    assert len(pieces) == 2
    aft, fore = sorted(pieces, key=lambda i: figures[i]["at"][0])
    assert figures[aft]["at"][0] < -9.45  # abaft her taffrail
    faces = [i for i, f in enumerate(figures) if f["layer"] == 1 and f["faces"]]
    assert faces
    inboard = [i for i in faces if fore > i]
    assert inboard, "the fore part comes after faces seen from inside"

    def beyond(rig, face):
        off = [a - b for a, b in zip(rig["at"], face["at"], strict=True)]
        return sum(a * n for a, n in zip(off, face["faces"], strict=True)) > 0

    behind = [
        i
        for i in faces
        if beyond(figures[aft], figures[i]) and figures[aft]["depth"] > figures[i]["depth"]
    ]
    assert behind and all(aft < i for i in behind)


@needs_node
@pytest.mark.parametrize("path", [SIXTY_FOUR, RAZEE, FRIGATE, BRIG, MERCHANT_BRIG])
def test_what_stands_on_the_head_paints_after_the_plate_it_stands_on(tmp_path, path):
    """Old beside new (the hull step's landing): each shape's side sorted at its own middle and the
    plate's at the plate's, so abaft the beam, and abeam from the high side, the plate covered it:
    the figure hidden 0.87 m2 on the frigate at facing 270, 1.16 on the 64, 1.34 on the razee at
    105. Now it sorts with its plate and paints straight after it, at every facing and heel."""
    word = graph_of(path)["hull"]["profile"]["form"]["head"]
    assert word in ("figure", "scroll")
    seen = 0
    for view in sweep_of(tmp_path, path):
        figures = view["figures"]
        for side in ("starboard", "larboard"):
            on = [
                i
                for i, f in enumerate(figures)
                if f["part"] == "head" and f["side"] == side and f["cls"] != "strip"
            ]
            plate = [i for i in on if figures[i]["cls"] != word]
            shape = [i for i in on if figures[i]["cls"] == word]
            if shape:
                assert plate and max(plate) < min(shape), (view["deg"], view["heel"], side)
                seen += 1
    assert seen > 0


@needs_node
@pytest.mark.parametrize("path", PROFILED)
def test_a_face_seen_from_inside_goes_first_among_the_hull(tmp_path, path):
    """Old beside new (the hull step's landing): a side's strips and the transom's sorted each at
    its middle, so near end on the far side's cut across the deck's far edge in a saw-tooth, 0.14 m2
    on the frigate and 0.18 on the smack at facing 165. She is a closed body: a face seen from
    inside can cover nothing of hers, so it goes before every other figure of the hull, by a margin
    at edge on, the far quarter's gallery with them forward of about 120 degrees off the bow."""
    seen = 0
    for view in sweep_of(tmp_path, path, hull_only=True):
        figures = view["figures"]
        where = (view["deg"], view["heel"])
        layers = [f["layer"] for f in figures]
        inside = [i for i, layer in enumerate(layers) if layer == 1]
        assert inside == list(range(len(inside))), where
        seen += len(inside)
        along, across = toward(view["deg"])
        if abs(across) > 0.3:
            near = "starboard" if across > 0 else "larboard"
            decks = [i for i, f in enumerate(figures) if f["part"] == "deck"]
            far = [
                i
                for i, f in enumerate(figures)
                if f["part"] == "side" and f["side"] not in (near, None) and layers[i] == 1
            ]
            if decks and far:
                assert max(far) < min(decks), where
            if along > -0.5:
                for i, f in enumerate(figures):
                    if f["part"] == "gallery" and f["side"] not in (near, None):
                        assert layers[i] == 1, where
    assert seen > 0


@needs_node
@pytest.mark.parametrize("path", PROFILED)
def test_the_rig_keeps_its_order_but_against_a_face_seen_from_inside(tmp_path, path):
    """The whole picture, for the same layers. The hull but for those faces and the stern keeps the
    depth's order with the rig among it: no spar or sail moves against a deck or the near side. What
    stands in her is painted after a face seen from inside, in front of it (the lugger's mizen lug
    at her stern against her quarter's bulwark). A rig figure beyond that face's plane, outside her,
    lies behind it and stays before it, as the depths have it (the after part of that lug), and that
    alone holds a face back."""

    def beyond(rig, face):
        off = [a - b for a, b in zip(rig["at"], face["at"], strict=True)]
        return sum(a * n for a, n in zip(off, face["faces"], strict=True)) > 0

    for view in sweep_of(tmp_path, path):
        figures = view["figures"]
        where = (view["deg"], view["heel"])
        rest = [f for f in figures if not f["layer"]]
        for a, b in zip(rest, rest[1:], strict=False):
            assert a["depth"] >= b["depth"] - 1e-3, (where, a, b)
        for i, face in enumerate(figures):
            if face["layer"] != 1:
                continue
            before = [f for f in figures[:i] if f["layer"] != 1]
            if before:
                held_by = before[-1]
                assert held_by["kind"] != "hull", (where, face, held_by)
                assert face["faces"] and held_by["depth"] > face["depth"], (where, face, held_by)
                assert beyond(held_by, face), (where, face, held_by)
            if face["faces"]:
                for rig in figures[i + 1 :]:
                    if rig["kind"] != "hull" and rig["depth"] > face["depth"]:
                        assert not beyond(rig, face), (where, face, rig)


@needs_node
@pytest.mark.parametrize("path", TRANSOMED)
def test_the_stern_seen_from_abaft_is_painted_after_the_rest_of_the_hull(tmp_path, path):
    """Old beside new (the hull step's landing): the lower transom strips sorted forward of the
    aftmost side strips, whose polygons then painted over its corners, 1.03 m2 on the frigate dead
    astern upright and 3.42 on the 64 at facing 165. Abaft about 120 degrees off the bow the stern
    goes after every other figure of the hull. From forward of the beam its face is seen from
    inside and goes first; near the beam it stays at its depth, the quarter standing before it."""
    for view in sweep_of(tmp_path, path, hull_only=True):
        figures = view["figures"]
        along, _across = toward(view["deg"])
        where = (view["deg"], view["heel"])
        stern = [i for i, f in enumerate(figures) if f["part"] in ("transom", "light")]
        assert stern, where
        layers = {figures[i]["layer"] for i in stern}
        if along < -0.5:
            assert layers == {2}, where
            others = [i for i, f in enumerate(figures) if i not in set(stern)]
            assert max(others) < min(stern), where
        elif along >= 0.2:
            # the tuck, sorted with the strip above it, has no face of its own
            assert {figures[i]["layer"] for i in stern if figures[i]["cls"] != "strip tuck"} == {1}
        else:
            assert layers == {None}, where


@needs_node
@pytest.mark.parametrize("path", TRANSOMED)
def test_the_stern_stays_under_a_rig_figure_abaft_and_nearer(tmp_path, path):
    """A boom's end or a sheet abaft the transom and nearer than all of it stays in front of it, the
    stern's layer going no later than that; so nothing but such a figure comes between."""
    for view in sweep_of(tmp_path, path):
        figures = view["figures"]
        stern = [i for i, f in enumerate(figures) if f["layer"] == 2]
        if not stern:
            continue
        where = (view["deg"], view["heel"])
        assert stern == list(range(stern[0], stern[0] + len(stern))), where
        for rig in figures[: stern[0]]:
            if rig["kind"] != "hull" and rig["at"][0] < max(figures[i]["at"][0] for i in stern):
                assert rig["depth"] >= figures[stern[-1]]["depth"], (where, rig)
        after = figures[stern[-1] + 1 :]
        if any(f["kind"] == "hull" for f in after):
            foremost = max(figures[i]["at"][0] for i in stern)
            nearest = figures[stern[-1]]["depth"]
            first = after[0]
            assert first["kind"] != "hull", (where, first)
            assert first["at"][0] < foremost and first["depth"] < nearest, (where, first)


@needs_node
def test_a_hull_with_no_profile_takes_no_layer(tmp_path):
    """Her painter's order is a hull drawn from her profile's: with none, the depths alone, as
    before (a kept save, or a ship landing before her profile)."""
    state = ship_state(make_ship(FRIGATE))
    state["graph"] = without_profile(state["graph"])
    for view in run_js(tmp_path, {**state, "hullOnly": False}, SWEEP):
        assert not any(f["layer"] for f in view["figures"]), (view["deg"], view["heel"])


@needs_node
@pytest.mark.parametrize("path", PROFILED)
def test_a_strip_faces_by_its_part_above_the_water(tmp_path, path):
    """The way a strip of the side faces, for the layers, is its part above the water's, where she
    is seen: the whole ring's is carried by the run's turn under it, and read a near quarter's
    topsides as seen from inside, painting them under a sail at her stern."""
    got = run_js(
        tmp_path,
        ship_state(make_ship(path)),
        """
        const sk = P.buildSkeleton(d.graph, d.snap);
        return sk.figures.filter(f => f.part === 'side' && f.faces).map(f => {
          const up = f.pts.filter(p => p[2] >= 0);
          const sign = f.side === 'starboard' ? 1 : -1;
          return {faces: f.faces, want: P.faceOut(up.length >= 3 ? up : f.pts, sign)};
        });
        """,
    )
    assert got
    for strip in got:
        assert strip["faces"] == pytest.approx(strip["want"])


@needs_node
@pytest.mark.parametrize("path", [FRIGATE, SIXTY_FOUR, RAZEE])
def test_a_bulkhead_is_seen_only_from_its_open_side(tmp_path, path):
    """Old beside new (the hull step's landing): drawn from both sides, a deck's end was painted
    over the deck above it, a dark wedge across the after end of the frigate's forecastle deck from
    forward of the beam, 0.59 m2 at her sailed heel and 1.97 at 0.205 rad, and on the 64 and the
    razee the same. A deck's after end now shows from abaft and its fore end from forward, and the
    frame does not move for it."""
    graph = graph_of(path)
    decks = graph["hull"]["profile"]["decks_m"]
    got = run_js(
        tmp_path,
        ship_state(make_ship(path)),
        """
        const sk = P.buildSkeleton(d.graph, d.snap);
        const hull = P.hullFigures(d.graph.hull).filter(f => f.part === 'bulkhead' && f.deck);
        const seen = deg => P.project({figures: hull, frame: []}, deg * Math.PI / 180, 0.1)
          .figures.length;
        const bounds = deg => {
          const kept = {figures: sk.figures.filter(f => !f.deck), frame: sk.frame};
          return [P.project(sk, deg * Math.PI / 180, 0.1).bounds,
                  P.project(kept, deg * Math.PI / 180, 0.1).bounds];
        };
        return {ends: hull.map(f => [f.deck, f.pts[0][0]]), forward: seen(30), abaft: seen(150),
                frame: bounds(30)};
        """,
    )
    fore_ends = [word for word, x in got["ends"] if x == decks[word][-1][0]]
    aft_ends = [word for word, x in got["ends"] if x == decks[word][0][0]]
    assert fore_ends and aft_ends and len(fore_ends) + len(aft_ends) == len(got["ends"])
    assert got["forward"] == len(fore_ends)
    assert got["abaft"] == len(aft_ends)
    # the bounds are noted before a figure is culled, so the frame holds a face seen neither way
    frame, without = got["frame"]
    assert frame["minX"] <= without["minX"] and frame["maxX"] >= without["maxX"]


@needs_node
def test_the_hovers_words_on_the_head_name_no_strip(tmp_path):
    """Old beside new: the closing strips of the head (class `strip back`) read "the strip back on
    the head" on hover, 16 polygons at facing 135 on the brig. Now they read as the head itself, and
    what stands on it by its own word."""
    state = ship_state(make_ship(BRIG))
    shipview = ROOT / "client" / "shipview.js"
    titles = run_js(
        tmp_path,
        state,
        f"""
        function node(name) {{
          return {{name, children: [], textContent: '',
            get firstChild() {{ return this.children[0]; }},
            setAttribute() {{}}, appendChild(c) {{ this.children.push(c); return c; }},
            removeChild(c) {{ this.children.splice(this.children.indexOf(c), 1); }}}};
        }}
        global.window = {{Projection: P}};
        global.document = {{createElementNS: (_ns, name) => node(name)}};
        new Function(require('fs').readFileSync({json.dumps(str(shipview))}, 'utf8'))();
        const sk = P.buildSkeleton(d.graph, d.snap);
        const svg = node('svg');
        const hover = [];
        for (const deg of [45, 135, 225, 315]) {{
          window.ShipView.render(svg, P.project(sk, deg * Math.PI / 180, 0.1), null);
          const walk = n => n.children.forEach(c => {{
            if (c.name === 'title') hover.push(c.textContent);
            walk(c);
          }});
          walk(svg);
        }}
        return hover;
        """,
    )
    on_the_head = [t for t in titles if "head" in t and t.startswith("hull")]
    assert on_the_head
    assert not [t for t in titles if "strip" in t]
    assert any("the scroll on the head" in t for t in on_the_head)
