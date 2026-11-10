"""Package 81, the viewer's action: the drawing (docs/design/Design-ViewerAction.md §2-§6, §12),
run in Node on the graph and the snapshot the server serves, as `test_view_geometry.py` runs it.

- Each port on her drawn side at its triple, its sill and top as served, its edges parallel to
  its deck; open while its gun is cast loose, shut otherwise and when the sea is at its sill.
- Each gun by its state: run out, its muzzle outboard of the side by its kind's share; run in,
  inboard; secured, just inside; a barrel cut at the side, its outboard part apart.
- A shot hole on her side, held under her rail.
- The flags at their places, the ensign's hoist at the gaff's peak within 0.1 m.
- The clock, the rounds fired between snapshots, and the effects: a flash at each gun that
  fired and at no other, the plume drifting to leeward, the recoil.
- A hull with no profile draws no gun, no port and no hole.
- Every word a figure gives is the ship's own (no build's word).
"""

from __future__ import annotations

import math
from pathlib import Path

import pytest
from test_view_geometry import needs_node, run_js, ship_state, without_profile

from freesail.api import queries
from freesail.api.session import make_ship, make_world
from freesail.core.world import Scenario
from freesail.ship import form
from freesail.ship.loader import load_spec

FRIGATE = "data/ships/frigate-36.yaml"
SIXTY_FOUR = "data/ships/sixty-four.yaml"
# every armed file, drawn from her profile (a ship added later is drawn by these tests with her)
ARMED_PROFILED = sorted(
    f"data/ships/{p.name}"
    for p in Path(__file__).resolve().parents[1].joinpath("data", "ships").glob("*.yaml")
    if load_spec(p).armament is not None and load_spec(p).hull.profile is not None
)


def _state(path: str, guns_state: str | None = None, **extra) -> dict:
    data = ship_state(make_ship(path, Scenario()))
    snap = data["snap"]
    snap["tick"] = 100
    snap["guns"] = [
        {
            "id": g["id"],
            "state": guns_state or "secured",
            "loaded": False,
            "shut": False,
            "fired": 0,
        }
        for g in data["graph"]["guns"]
    ]
    snap.update(extra)
    return data


HOLE = {"side": "starboard", "x_m": 0, "z_m": 0.5, "diameter_m": 0.1, "plugged": False}

# Package 75's recorded departure at the *Neufchatel*'s No. 8 (`CUT_AT_A_CORNER_M`, 2.268 drawn
# against 2.27 served) went with 81's port-top rule (package 98, step 3, the lead's ruling of
# 2026-11-07): the served top takes the deck's tilt and the 2 mm, so the drawing honours it
# (`viewer_guns.port_top`; her No. 8 served 2.265).


def _barrels(figs: list, gid: str) -> list:
    return [f for f in figs if f["kind"] == "gun" and f["id"] == gid and f["part"] == "barrel"]


ACTION_FIGS = """
  const sk = P.buildSkeleton(d.graph, d.snap);
  return sk.figures.filter(f => f.kind === 'gun' || f.kind === 'flag' ||
    ['port', 'lid', 'hole'].includes(f.part));
"""


@needs_node
@pytest.mark.parametrize("path", ARMED_PROFILED)
def test_each_port_is_drawn_at_its_triple_on_both_sides(tmp_path, path):
    """§2.1 item 2: each port's corners at its x less and more half its width, its sill's and its
    top's middles at the served sill and top, on her drawn side; one a side. A port's top is served
    as the drawing cuts it, tilted with its deck (package 98, step 3)."""
    data = _state(path)
    spec = load_spec(path)
    figs = run_js(tmp_path, data, ACTION_FIGS)
    ports = data["graph"]["ports"]
    lids = [f for f in figs if f["part"] == "lid"]
    assert len(lids) == 2 * len(ports)
    by = {(f["side"], round(f["at_x"], 3), f["deck"]): f for f in lids}
    for p in ports:
        for side, sign in (("starboard", 1), ("larboard", -1)):
            f = by[(side, round(p["x_m"], 3), p["deck"])]
            xs = sorted(pt[0] for pt in f["pts"])
            assert xs[0] == pytest.approx(p["x_m"] - p["width_m"] / 2, abs=1e-6)
            assert xs[-1] == pytest.approx(p["x_m"] + p["width_m"] / 2, abs=1e-6)
            # its sill's middle and its top's at the triple's sill and the top as cut, the edges
            # tilted with the deck (portCorners: sill aft, sill forward, top forward, top aft)
            sill = (f["pts"][0][2] + f["pts"][1][2]) / 2
            top = (f["pts"][2][2] + f["pts"][3][2]) / 2
            assert sill == pytest.approx(p["sill_m"], abs=1e-6)
            if p["top_m"] < p["sill_m"] + p["depth_m"] - 1e-6:
                # cut to the rail: never above it, and down with it where it steps within the
                # port's width (the 64's foremost quarterdeck port, at her breast)
                assert p["top_m"] - 0.1 <= top <= p["top_m"] + 1e-6
            else:
                assert top == pytest.approx(p["top_m"], abs=1e-6)
            assert all(sign * pt[1] > 0 for pt in f["pts"])
            # the sill's ends on her drawn side (freesail/ship/form.py's, which the server's
            # stations are), whatever the gap the generator records to the triple (§5.3)
            for pt in f["pts"][:2]:
                drawn = form.half_breadth_at(spec.hull, pt[0], pt[2])
                assert abs(pt[1]) == pytest.approx(drawn, abs=0.01)


@needs_node
@pytest.mark.parametrize(
    "state,lid,muzzle",
    [("secured", "shut", "in"), ("run in", "open", "in"), ("run out", "open", "out")],
)
def test_the_frigates_upper_deck_guns_by_their_state(tmp_path, state, lid, muzzle):
    """§2.5, §3.3: the lid shut on a gun secured and open on one cast loose; the muzzle just
    inside the side secured, inboard by its recoil run in, outboard by its kind's share run
    out, the barrel cut at the side then into its inboard and outboard parts."""
    data = _state(FRIGATE, state)
    gun = next(g for g in data["graph"]["guns"] if g["id"] == "gun.7.starboard")
    figs = run_js(tmp_path, data, ACTION_FIGS)
    port = [f for f in figs if f.get("at_x") == gun["x_m"] and f["side"] == "starboard"]
    assert {f["cls"] for f in port} == ({"shut"} if lid == "shut" else {"open"})
    barrels = [
        f for f in figs if f["kind"] == "gun" and f["id"] == gun["id"] and f["part"] == "barrel"
    ]
    ys = [pt[1] for f in barrels for pt in f["pts"]]
    # her drawn side where the bore meets it: the port's own points there (tumblehome puts it
    # inside the triple's half-breadth at the sill)
    face = next(f for f in port if f["part"] == "port" or f["cls"] == "shut")
    side_y = sum(pt[1] for pt in face["pts"]) / 4
    L = gun["length_m"]
    half = gun["breech_m"] / 2
    if muzzle == "out":
        assert max(ys) == pytest.approx(side_y + 0.33 * L, abs=0.05)
        assert {f.get("piece") for f in barrels} == {"inboard", "outboard"}
    else:
        assert max(ys) < side_y + half
        if state == "run in":
            assert max(ys) == pytest.approx(side_y - 0.4 * L, abs=0.05)


@needs_node
def test_a_port_shut_by_the_sea_is_drawn_shut_and_its_gun_run_in(tmp_path):
    """§2.5: the lee port the engine shuts is drawn with its lid let down, its gun run in."""
    data = _state(FRIGATE, "run out")
    for g in data["snap"]["guns"]:
        if g["id"] == "gun.7.starboard":
            g.update({"state": "run in", "shut": True})
    figs = run_js(tmp_path, data, ACTION_FIGS)
    port = [
        f
        for f in figs
        if f.get("at_x") == 0.0 and f["side"] == "starboard" and f.get("deck") == "upper"
    ]
    assert [f["cls"] for f in port] == ["shut"]
    assert "the sea at its sill" in port[0]["words"]
    gun = [f for f in figs if f["kind"] == "gun" and f["id"] == "gun.7.starboard"]
    assert all(f["state"] == "run_in" for f in gun)


@needs_node
def test_a_gun_over_the_rail_is_drawn_above_it_through_no_port(tmp_path):
    """§2.1 item 5: the frigate's forecastle guns above her drawn rail, no port at them."""
    data = _state(FRIGATE, "run out")
    over = [g for g in data["graph"]["guns"] if g["how"] == "over the rail"]
    figs = run_js(tmp_path, data, ACTION_FIGS)
    xs = {round(f["at_x"], 3) for f in figs if f["part"] in ("port", "lid")}
    for g in over:
        assert round(g["x_m"], 3) not in xs
        barrel = [
            f for f in figs if f["kind"] == "gun" and f["id"] == g["id"] and f["part"] == "barrel"
        ]
        assert min(pt[2] for f in barrel for pt in f["pts"]) > g["axis_z_m"] - g["breech_m"]


@needs_node
def test_a_hole_is_drawn_on_her_side_under_her_rail(tmp_path):
    """§5: a hole at its place and size; one made above her rail held under it."""
    holes = [
        {"side": "larboard", "x_m": 2.0, "z_m": 0.6, "diameter_m": 0.13, "plugged": False},
        {"side": "starboard", "x_m": 0.0, "z_m": 9.0, "diameter_m": 0.13, "plugged": True},
    ]
    data = _state("data/ships/cutter.yaml", damage={"holes": holes})
    figs = run_js(tmp_path, data, ACTION_FIGS)
    drawn = [f for f in figs if f["part"] == "hole"]
    assert [f["cls"] for f in drawn] == ["open", "plugged"]
    low = drawn[0]
    assert all(pt[1] < 0 for pt in low["pts"])
    assert sum(pt[2] for pt in low["pts"]) / 8 == pytest.approx(0.6, abs=1e-6)
    assert "between wind and water" not in low["words"] and "to larboard" in low["words"]
    high = drawn[1]
    rail = max(pt[2] for pt in high["pts"])
    assert rail < 9.0 and "plugged" in high["words"]


@needs_node
def test_the_ensign_is_drawn_at_the_gaffs_peak(tmp_path):
    """§12.2: the ensign's hoist at the aftmost gaff's peak within 0.1 m."""
    flag = {
        "place": "peak",
        "name": "ensign",
        "words": "British colours, the red ensign",
        "drawing": {"proportion": [1, 2], "parts": [{"rect": [0, 0, 1, 1], "colour": "red"}]},
    }
    data = _state(FRIGATE, flags=[flag])
    out = run_js(
        tmp_path,
        data,
        """
      const sk = P.buildSkeleton(d.graph, d.snap);
      const flag = sk.figures.filter(f => f.kind === 'flag')[0];
      return { pts: flag.pts, cls: flag.cls, words: flag.words, peak: sk.spars['mizzen.gaff'].b };
    """,
    )
    assert out["cls"] == "colour-red" and out["words"].endswith("at the peak")
    assert math.dist(out["pts"][0], out["peak"]) <= 0.1


@needs_node
def test_a_hull_without_a_profile_draws_no_gun_port_or_hole(tmp_path):
    """§1: a graph with no profile draws as before: none of the action's figures."""
    data = without_profile(
        _state(
            FRIGATE,
            "run out",
            damage={
                "holes": [
                    {"side": "starboard", "x_m": 0, "z_m": 1, "diameter_m": 0.1, "plugged": False}
                ]
            },
        )
    )
    figs = run_js(tmp_path, data, ACTION_FIGS)
    assert figs == []


@needs_node
def test_the_effects_flash_at_each_gun_that_fired_and_the_smoke_goes_to_leeward(tmp_path):
    """§4: the rounds fired between two snapshots, stamped with the later one's tick; a flash
    at each gun that fired within FLASH_S and at no other; the plume carried to leeward of the
    apparent wind; the recoil moving the muzzle in; nothing alive after the half minute."""
    data = _state(FRIGATE, "run out")
    prev = data["snap"]
    snap = dict(prev, tick=101, guns=[dict(g) for g in prev["guns"]])
    fired = {"gun.3.starboard", "gun.4.starboard"}
    for g in snap["guns"]:
        if g["id"] in fired:
            g.update({"fired": 1, "state": "run in"})
    snap["wind"] = {"apparent_angle": math.radians(90.0), "apparent_speed": 6.0}
    out = run_js(
        tmp_path,
        {"graph": data["graph"], "prev": prev, "snap": snap},
        """
      const fs = P.firingsBetween(d.prev, d.snap);
      const at = t => P.effects(d.graph, d.snap, fs, t, {});
      const e0 = at(101.05), e10 = at(111), e40 = at(140);
      const plume = e10.figures.filter(f => f.cls === 'plume')[0];
      const flashes = [...new Set(e0.figures.filter(f => f.cls === 'flash').map(f => f.words))];
      return { fs, flashes, moving: e0.moving, plumeY: plume.centre[1],
               flashLater: at(101.5).figures.filter(f => f.cls === 'flash').length,
               alive40: e40.alive, first: P.firingsBetween(null, d.snap).length };
    """,
    )
    assert sorted(f["gun"] for f in out["fs"]) == sorted(fired)
    assert all(f["tick"] == 101 for f in out["fs"])
    assert out["first"] == 0
    assert len(out["flashes"]) == 2 and all("No. 3" in w or "No. 4" in w for w in out["flashes"])
    assert out["flashLater"] == 0
    # the wind on the starboard beam blows to larboard: the smoke drifts to larboard (y < 0)
    assert out["plumeY"] < 0
    assert set(out["moving"]) == fired
    assert out["alive40"] is False


@needs_node
def test_the_clock_runs_between_snapshots_and_holds_with_the_clock(tmp_path):
    """§6 item 2."""
    out = run_js(
        tmp_path,
        {},
        "return [P.clockAt(100, 0, 500, 1, true, 1), P.clockAt(100, 0, 5000, 10, true, 10),"
        " P.clockAt(100, 0, 500, 1, false, 1), P.clockAt(100, 0, 3000, 1, true, 1)];",
    )
    assert out == [100.5, 110, 100, 101]


@needs_node
@pytest.mark.parametrize("path", ARMED_PROFILED)
def test_every_word_a_figure_gives_is_in_world(tmp_path, path):
    """85's rule: the hover words name the gun, its kind and its state, the port, the hole, in
    the ship's own words; no build's word."""
    data = _state(
        path,
        "run out",
        damage={
            "holes": [
                {"side": "starboard", "x_m": 0, "z_m": 0.5, "diameter_m": 0.1, "plugged": False}
            ]
        },
    )
    figs = run_js(tmp_path, data, ACTION_FIGS)
    for f in figs:
        if f["kind"] == "flag":
            continue
        w = f["words"]
        assert w and "package" not in w.lower() and "_" not in w, w


def test_a_world_serves_what_the_drawing_reads():
    """The snapshot's `guns` carry every graph gun's id, so the drawing finds each."""
    w = make_world(7, FRIGATE)
    snap = queries.snapshot(w)
    graph = queries.ship_graph(w.ship)
    assert {g["id"] for g in snap["guns"]} == {g["id"] for g in graph["guns"]}


# ---------------------------------------------------------------------------
# Package 98, step 3: the viewer's paint order (the owner's play of 2026-11-09)
# ---------------------------------------------------------------------------

BEARINGS_AND_HEELS = """
  const views = [];
  for (const heel of [0, 15]) for (let b = 0; b < 360; b += 15) views.push([b, heel]);
"""

GUNS_BEHIND = (
    BEARINGS_AND_HEELS
    + """
  const sk = P.buildSkeleton(d.graph, d.snap);
  sk.figures.forEach(f => {
    if (f.part === 'lid' && f.cls === 'shut') f.id = 'lid:' + f.side + ':' + f.at_x;
    if (f.part === 'port') f.id = 'port:' + f.side + ':' + f.at_x;
  });
  const guns = d.graph.guns.filter(g => g.how === 'port');
  const out = [];
  for (const [b, heel] of views) {
    const figs = P.project(sk, b * Math.PI / 180, heel * Math.PI / 180).figures;
    const at = {};
    figs.forEach((f, i) => { if (f.id) (at[f.id] = at[f.id] || []).push([i, f.piece || '']); });
    const toV = Math.sin(b * Math.PI / 180);
    guns.forEach(g => {
      const sign = g.side === 'larboard' ? -1 : 1;
      if (sign * toV < 0.2) return;  // seen from outboard on its own side
      const key = g.side + ':' + g.x_m;
      const hole = (at['lid:' + key] || at['port:' + key] || [])[0];
      const mine = at[g.id] || [];
      if (!hole || !mine.length) return;
      const inboard = mine.filter(m => m[1] !== 'outboard').map(m => m[0]);
      const outboard = mine.filter(m => m[1] === 'outboard').map(m => m[0]);
      out.push({ gun: g.id, b, heel, inboard_after: inboard.filter(i => i > hole[0]).length,
                 outboard_before: outboard.filter(i => i < hole[0]).length });
    });
  }
  return out;
"""
)


# the armed, profiled files with a gun in a port (the lugger's, the smack's and the topsail
# schooner's are swivels on the rail)
PORT_ARMED = [
    p
    for p in ARMED_PROFILED
    if load_spec(p).armament.fit() is not None
    and any(g.place in ("broadside", "bow", "stern") for g in load_spec(p).armament.fit().guns)
]


@needs_node
@pytest.mark.parametrize("path", PORT_ARMED)
@pytest.mark.parametrize("state", ["secured", "run in", "run out"])
def test_a_port_guns_inboard_figures_paint_behind_its_side_and_lid_from_outboard(
    tmp_path, path, state
):
    """Truth 7-450 (package 98, step 3): a port gun's inboard figures sort with its port's
    strip, a hair inboard, so that from outboard on her side, at every 15 degrees, heel 0 and
    15, every one of them is painted before its port's lid (shut) or its opening (open); on
    every armed, profiled file with a port gun. Before the mend her steep deadrise put the
    strip's middle inboard of the whole carronade on the *Neufchatel*. (A gun run out's outboard
    figures keep their own middles, as before: found for the viewer's owner, see the notes.)"""
    rows = run_js(tmp_path, _state(path, state), GUNS_BEHIND)
    guns = {r["gun"] for r in rows}
    assert rows and guns, path
    bad = [r for r in rows if r["inboard_after"]]
    assert not bad, bad[:5]


FLAG_WHOLE = (
    BEARINGS_AND_HEELS
    + """
  const sk = P.buildSkeleton(d.graph, d.snap);
  const flagFigs = sk.figures.filter(f => f.kind === 'flag');
  const out = { parts: flagFigs.length, lines: flagFigs.filter(f => f.pts.length !== 4).length,
                broken: [] };
  for (const [b, heel] of views) {
    const figs = P.project(sk, b * Math.PI / 180, heel * Math.PI / 180).figures;
    const idx = [];
    figs.forEach((f, i) => { if (f.kind === 'flag') idx.push([i, +f.id.split('.').pop()]); });
    for (let j = 1; j < idx.length; j++)
      if (idx[j][0] !== idx[j - 1][0] + 1 || idx[j][1] <= idx[j - 1][1]) {
        out.broken.push([b, heel]);
        break;
      }
  }
  return out;
"""
)


def _ensigns() -> dict:
    """Every root's ensign as the snapshot serves it, her colours shown (basic's by
    Portugal, the nation that stands on it)."""
    from freesail.world import flags as F
    from freesail.world import signals as S
    from freesail.world.nations import load_nations

    n = load_nations()
    roots = {"britain": "britain", "france": "france", "spain": "spain"}
    roots |= {"united-states": "united-states", "naples": "naples", "basic": "portugal"}
    out = {}
    for root, nation in roots.items():
        flown = F.flies(n, S.Colours(state="shown", nation=nation), "kings-ship")
        out[root] = next(f for f in flown if f["place"] == "peak")
    return out


ENSIGNS = _ensigns()


@needs_node
@pytest.mark.parametrize("root", sorted(ENSIGNS))
@pytest.mark.parametrize("path", [FRIGATE, "data/ships/hermaphrodite-brig.yaml"])
def test_every_roots_ensign_paints_as_one_flag_in_its_drawings_order(tmp_path, root, path):
    """Truth 7-451 (package 98, step 3; §12.3, "a flag sorts at its own middle as a sail
    does"): every root's ensign at the peak paints as one flag, its parts and lines one after
    another in the drawing's order, at every 15 degrees, heel 0 and 15; before the mend each
    part sorted at its own middle and the canton went behind the stripes over half the
    circle. The Union's saltires are drawn as its lines, each inside the canton."""
    flag = ENSIGNS[root]
    out = run_js(tmp_path, _state(path, flags=[flag]), FLAG_WHOLE)
    lines = len(flag["drawing"].get("lines") or [])
    assert out["parts"] == len(flag["drawing"]["parts"]) + lines
    assert not out["broken"], out["broken"][:5]
    if root == "britain":
        assert lines == 4


@needs_node
def test_the_unions_lines_lie_inside_its_canton(tmp_path):
    """Package 98, step 3: a drawing's lines drawn (they were never drawn): the four of the
    Union's saltires each a band cut to the canton, on the flag's plane."""
    flag = ENSIGNS["britain"]
    out = run_js(
        tmp_path,
        _state(FRIGATE, flags=[flag]),
        """
      const sk = P.buildSkeleton(d.graph, d.snap);
      const f = sk.figures.filter(f => f.kind === 'flag');
      return { canton: f[1].pts, lines: f.slice(2, 6).map(x => [x.cls, x.pts]),
               order: f.map(x => x.cls), pieces: f.map(x => x.piece) };
    """,
    )
    # in the drawing's order: the field, the canton, the saltires, then the crosses over them
    drawn = ["red", "blue", "white", "white", "red", "red", "white", "white", "red", "red"]
    assert out["order"] == [f"colour-{c}" for c in drawn]
    assert out["pieces"] == ["", ""] + ["line"] * 4 + [""] * 4
    xs = [p[0] for p in out["canton"]]
    zs = [p[2] for p in out["canton"]]
    assert [c for c, _ in out["lines"]] == ["colour-white"] * 2 + ["colour-red"] * 2
    for _cls, pts in out["lines"]:
        assert len(pts) >= 3
        for p in pts:
            assert min(xs) - 1e-6 <= p[0] <= max(xs) + 1e-6
            assert min(zs) - 1e-6 <= p[2] <= max(zs) + 1e-6


@needs_node
@pytest.mark.parametrize("path", ARMED_PROFILED + ["data/ships/lugger.yaml"])
def test_a_flag_of_truce_is_drawn_white_at_the_fore(tmp_path, path):
    """Truth 7-452 (package 98, step 3): under a flag of truce the white is served and drawn
    at the fore truck (the basic file's occasion; the fallback had it at the peak), at a
    vessel of one mast her only mast's truck."""
    from freesail.api.session import make_world
    from tests.test_viewer_action import _locker

    w = make_world(7, path)
    _locker(w, "truce", "")
    w.run(1)
    snap = queries.snapshot(w)
    assert [(f["place"], f["name"]) for f in snap["flags"]] == [("fore truck", "flag of truce")]
    out = run_js(
        tmp_path,
        {"graph": queries.ship_graph(w.ship), "snap": snap},
        """
      const sk = P.buildSkeleton(d.graph, d.snap);
      return sk.figures.filter(f => f.kind === 'flag').map(f => [f.cls, f.words]);
    """,
    )
    assert out == [["colour-white", "a flag of truce, at the fore truck"]]


def test_a_ports_served_top_takes_its_decks_tilt_and_stands_under_the_rail():
    """Truth 7-453 (package 98, step 3; 81's port-top rule, the lead's ruling of 2026-11-07):
    every port's top as served, tilted with its deck as the viewer draws it, stands at both
    corners under the rail there less 2 mm or at its full depth; the *Neufchatel*'s No. 8
    served 2.265 (was 2.27, drawn 2.268: the departure `CUT_AT_A_CORNER_M` gone with it)."""
    from freesail.api import viewer_guns as V
    from freesail.ship.profile import rail_at

    for path in ARMED_PROFILED:
        prof = load_spec(path).hull.profile
        for port in _state(path)["graph"]["ports"]:
            s = V.deck_slope(prof, port["deck"], port["x_m"])
            w = port["width_m"] / 2
            full = port["sill_m"] + port["depth_m"]
            assert port["top_m"] <= full + 1e-9
            for c in (-1, 1):
                corner = port["top_m"] + c * s * w
                rail = rail_at(prof, port["x_m"] + c * w)
                assert corner <= rail - V.TOP_UNDER_RAIL_M + 1e-9 or port["top_m"] == full
    served = _state("data/ships/hermaphrodite-brig.yaml")["graph"]["ports"]
    eight = next(p for p in served if abs(p["x_m"] + 5.64) < 1e-6)
    assert eight["top_m"] == pytest.approx(2.265, abs=1e-9)


@needs_node
def test_a_settees_sheet_held_to_windward_is_served_and_drawn_there(tmp_path):
    """Truth 7-454 (package 98, step 3): the bilander's settee with its one sheet hauled to
    windward by order is served the side its sheet holds it (`sheet_side`, the weather side,
    only while it is) and drawn there, the clew on the weather side of the centreline; let go
    to leeward, nothing served and the clew to leeward as before. Her sheet's block stays on
    the lee side."""
    from freesail.api.session import make_world

    w = make_world(7, "data/ships/bilander.yaml")
    w.submit("set the settee")
    w.run(300)
    tack = queries.snapshot(w)["ship"]["tack"]
    weather = -1 if tack == "larboard" else 1

    def drawn() -> dict:
        snap = queries.snapshot(w)
        served = next(s for s in snap["sails"] if s["id"] == "main.settee")
        out = run_js(
            tmp_path,
            {"graph": queries.ship_graph(w.ship), "snap": snap},
            """
          const sk = P.buildSkeleton(d.graph, d.snap);
          const f = sk.figures.filter(f => f.kind === 'sail' && f.id === 'main.settee')[0];
          return { clew: f.corners ? f.corners[2] : f.pts[f.pts.length - 1] };
        """,
        )
        return {"served": served.get("sheet_side"), "clew_y": out["clew"][1]}

    lee = drawn()
    assert lee["served"] is None and lee["clew_y"] * weather < 0
    assert w.submit("haul the settee sheet to windward").kind == "line.hauled"
    w.run(5)
    held = drawn()
    assert held["served"] == ("larboard" if weather < 0 else "starboard")
    assert held["clew_y"] * weather > 0
    w.submit("haul the settee sheet to leeward")
    w.run(5)
    assert drawn()["served"] is None
