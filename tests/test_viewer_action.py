"""Package 81, the viewer's action: the data served (docs/design/Design-ViewerAction.md §7).

- The rule of placing (§2) on every armed file under data/ships: each gun placed in a port,
  over the rail, on the rail or as a pivot, or refused with why; the ports of the hull with the
  guns that stand in them, and none where a triple stands over the rail.
- The gun's figure (§3) by kind, calibre and the file's own weight against Adye's patterns.
- The graph's `guns` and `ports`; the snapshot's `guns`, `damage` and `flags`; a snapshot that
  writes nothing of the world (the battery, the damage keeper and the locker read where the
  ship keeps them, never made).
- The flags' fallback until 76's colours.yaml (§12.1): the plain ensign of the nation shown,
  the other's under false colours, turned over in distress, the white under truce, none
  struck or with no colours.
"""

from __future__ import annotations

import glob

import pytest

from freesail.api import queries, viewer_flags, viewer_guns
from freesail.ship.loader import load_ship, load_spec
from freesail.ship.profile import rail_at

ARMED = sorted(f for f in glob.glob("data/ships/*.yaml") if load_spec(f).armament is not None)
FIGURE_KEYS = {"x_m", "y_m", "axis_z_m", "deck_z_m", "train_deg", "length_m", "bore_m"}


def _fits(path: str):
    spec = load_spec(path)
    return [(name, fit) for name, fit in spec.armament.fits.items()]


@pytest.mark.parametrize("path", ARMED)
def test_every_gun_of_every_armed_file_is_placed_by_the_rule(path):
    """§2: every gun of every fit placed, none refused, a port gun on its own triple within
    0.01 m; the triple a port where the side stands its depth above the sill (within 0.05 m),
    a place over the rail where it does not."""
    profile = load_spec(path).hull.profile
    for name, fit in _fits(path):
        for g in fit.guns:
            p = viewer_guns.place(profile, g)
            assert p.how is not None, (path, name, g.id, p.refused)
            if p.how in ("port", "over the rail"):
                assert abs(p.x_m - g.x_m) <= viewer_guns.TRIPLE_TOLERANCE_M + 1e-9
                gap = rail_at(profile, p.x_m) - p.triple[1]
                depth = dict(profile.port_size_m)[g.deck][1]
                assert (p.how == "port") == (gap >= depth - viewer_guns.PORT_FIT_M)
            if p.how == "port":
                assert p.port_top_m <= rail_at(profile, p.x_m) + 1e-9
                assert p.axis_z_m > p.triple[1]
            if p.how == "over the rail":
                assert p.axis_z_m > rail_at(profile, p.x_m)


def test_the_frigates_forecastle_guns_are_over_the_rail_and_her_upper_deck_in_ports():
    """§2.3: the frigate's pair 18 and her bow chasers over the rail, the rest in ports, her
    upper deck's of its own size."""
    spec = load_spec("data/ships/frigate-36.yaml")
    profile = spec.hull.profile
    fit = spec.armament.fits[spec.armament.default]
    hows = {g.id: viewer_guns.place(profile, g) for g in fit.guns}
    over = sorted(gid for gid, p in hows.items() if p.how == "over the rail")
    assert over == sorted(g.id for g in fit.guns if g.deck == "forecastle")
    assert len(over) == 4
    for g in fit.guns:
        if g.deck == "upper":
            assert hows[g.id].how == "port" and hows[g.id].port == (0.88, 0.75)


def test_the_64s_forecastle_9s_of_1784_are_over_the_rail_by_the_sides_test_and_said():
    """§2.2 (the lead's ruling): her foremost forecastle triple stands 0.07 m under the rail,
    where a 0.69 m port cannot be cut; it is a place over the rail, and the checker's note says
    it is not at the generator's 0.05 m."""
    spec = load_spec("data/ships/sixty-four.yaml")
    profile = spec.hull.profile
    fit = spec.armament.fits["ardent class 1784"]
    nines = [g for g in fit.guns if g.deck == "forecastle"]
    assert nines and all(g.kind == "long" and g.pounder == 9 for g in nines)
    for g in nines:
        p = viewer_guns.place(profile, g)
        assert p.how == "over the rail"
        assert any("not at 0.05 m" in n for n in p.notes)


def test_a_triple_over_the_rail_is_no_port():
    """§2.5: the 64's roundhouse triples, which bear no gun in the fit of 1784, are no ports."""
    spec = load_spec("data/ships/sixty-four.yaml")
    profile = spec.hull.profile
    fit = spec.armament.fits["ardent class 1784"]
    placings = [viewer_guns.place(profile, g) for g in fit.guns]
    ports = viewer_guns.ports(profile, placings, {g.id: g.side for g in fit.guns})
    assert not [p for p in ports if p.deck == "roundhouse"]
    assert [p for p in ports if p.deck == "quarterdeck" and not p.guns]


def test_a_gun_off_its_triple_or_without_its_deck_is_refused_and_says_why():
    """§2.1: a gun whose x finds no triple, or whose deck gives no ports, is not placed."""
    from dataclasses import replace

    spec = load_spec("data/ships/brig.yaml")
    profile = spec.hull.profile
    g = spec.armament.fits[spec.armament.default].guns[0]
    off = viewer_guns.place(profile, replace(g, x_m=g.x_m + 0.5))
    assert off.how is None and "no port of the upper deck" in off.refused
    nodeck = viewer_guns.place(profile, replace(g, deck="quarterdeck"))
    assert nodeck.how is None and "no ports of the quarterdeck deck" in nodeck.refused
    assert viewer_guns.place(None, g).refused == "her file gives no profile"


@pytest.mark.parametrize(
    "kind,pounder,cwt,length_ft,judged",
    [
        ("long", 18, 42.0, 9.5, False),
        ("long", 24, 49.5, 9.5, False),
        ("long", 9, 26.0, 7.5, False),  # the generator's 26 from memory: Adye's 7 ft 6 in
        ("long", 6, 20.0, 8.0, False),
        ("long", 3, 7.0, 4.5, False),
        ("carronade", 32, 17.0, 4.0 + 0.5 / 12, False),
        ("carronade", 12, 6.0, 2.0 + 2 / 12, False),
        ("swivel", 0.5, 0.5, 3.0, True),
    ],
)
def test_the_figure_is_the_pattern_of_nearest_weight(kind, pounder, cwt, length_ft, judged):
    """§3.1: a gun's length its pattern's in Adye, chosen by the file's own weight."""
    f = viewer_guns.figure(kind, pounder, cwt)
    assert f.length_m == pytest.approx(length_ft * 0.3048, abs=1e-6)
    assert f.judged is judged
    assert f.breech_m > f.bore_m and f.muzzle_m > f.bore_m


@pytest.mark.parametrize("path", ARMED)
def test_no_gun_of_the_files_stands_a_tenth_off_its_pattern(path):
    """§3.2: no file's gun more than WEIGHT_LISTED_SHARE off its pattern's weight today."""
    for _name, fit in _fits(path):
        for g in fit.guns:
            f = viewer_guns.figure(g.kind, g.pounder, g.weight_cwt)
            assert f.weight_off <= viewer_guns.WEIGHT_LISTED_SHARE, (g.id, f.pattern)


def test_the_graph_serves_the_guns_and_the_ports():
    """§7: the graph's `guns`, each with its placing and figure or why not, and `ports`."""
    ship = load_ship("data/ships/frigate-36.yaml")
    g = queries.ship_graph(ship)
    assert len(g["guns"]) == len(ship.guns) == 40
    for e in g["guns"]:
        assert e["how"] in ("port", "over the rail") and FIGURE_KEYS <= set(e)
        assert "package" not in e["name"] and "package" not in e["kind_words"]
    assert e["kind_words"] in ("long 9-pounder", "long 18-pounder", "32-pounder carronade")
    ports = g["ports"]
    assert (
        len(ports) == 13 + 5
    )  # the upper deck's and the quarterdeck's; the forecastle's are over the rail
    assert all(set(p["guns"]) == {"starboard", "larboard"} for p in ports)


def test_a_hull_without_a_profile_serves_no_placing():
    """§1: a graph with no profile serves each gun refused and no port."""
    spec = load_spec("data/ships/brig.yaml")
    out = viewer_guns.served(None, spec.armament.fits[spec.armament.default].guns)
    assert out["ports"] == [] and all(e["how"] is None for e in out["guns"])


def _cutters():
    from test_known_truths import _two_cutters_at_pistol_shot

    return _two_cutters_at_pistol_shot()


def test_the_snapshot_serves_each_guns_rounds_and_the_holes_and_writes_nothing():
    """§4.1, §5, §7: the guns whose rounds rose are the guns `action.fired` names; the hole
    made in the mark is served with its side, place and size; a snapshot makes no battery,
    damage keeper or locker where the ship has none."""
    w, _v, enemy, _battery = _cutters()
    before = {g["id"]: g["fired"] for g in queries.snapshot(w)["guns"]}
    w.submit("fire")
    w.run(70)
    after = {g["id"]: g["fired"] for g in queries.snapshot(w)["guns"]}
    rose = sorted(gid for gid in after if after[gid] > before[gid])
    named = sorted(gid for e in w.log if e.kind == "action.fired" for gid in e.data["guns"])
    assert rose and rose == named
    snap = queries.snapshot(enemy)
    keeper = enemy.ship.extra["damage"]
    assert len(snap["damage"]["holes"]) == len(keeper.holes)
    for served, hole in zip(snap["damage"]["holes"], keeper.holes, strict=True):
        assert served["side"] == hole["side"] and served["x_m"] == hole["x_m"]
        assert served["z_m"] == hole["z_m"] and served["diameter_m"] == hole["diameter_m"]
    from freesail.api.session import make_world

    fresh = make_world(7, "data/ships/brig.yaml")
    keys = set(fresh.ship.extra)
    assert not keys & {"battery", "damage", "signals"}
    for _ in range(3):
        queries.snapshot(fresh)
    assert set(fresh.ship.extra) == keys


def test_a_lee_port_shut_by_the_sea_is_served_shut_and_its_gun_run_in():
    """§2.5, §7: the battery's shut ports served on their guns, each run in."""
    from test_lee_ports import CUTTER, _at_quarters, _Serving, _shut_heels

    w = _at_quarters(CUTTER, "carronades")
    serving = _Serving(w, "starboard")
    lee = serving.lee_guns("upper")
    serving.serve(max(_shut_heels(serving.ship, lee).values()) + 0.5, 2)
    snap = {g["id"]: g for g in queries.snapshot(w)["guns"]}
    assert {g.id for g in lee} <= serving.battery._shut
    for g in lee:
        assert snap[g.id]["shut"] and snap[g.id]["state"] == "run in"


def _locker(world, state, nation=""):
    from freesail.world.signals import locker_of, set_colours

    c = locker_of(world.ship).colours
    if state == "truce":
        c.state = "truce"  # 74's state for the cartel (the lead's ruling of 2026-11-07)
    else:
        set_colours(c, world.nations, state, nation, 0)


@pytest.mark.parametrize(
    "state,nation,words,colour,inverted",
    [
        ("shown", "britain", "British colours, the red ensign", "red", False),
        ("false", "france", "French colours, the tricolour", "cloth", False),
        (
            "distress",
            "britain",
            "British colours, the red ensign, the ensign union down",
            "red",
            True,
        ),
        ("truce", "", "a flag of truce", "white", False),
        ("none", "", None, None, None),
        ("struck", "", None, None, None),
    ],
)
def test_the_flags_fallback_follows_the_colours(state, nation, words, colour, inverted):
    """§12.1: one plain ensign at the peak while her colours show, of the nation shown; the
    white of a flag of truce; nothing with no colours or struck."""
    from freesail.api.session import make_world

    w = make_world(7, "data/ships/frigate-36.yaml")
    _locker(w, state, nation)
    flags = queries.snapshot(w)["flags"]
    if words is None:
        assert flags == []
        return
    (f,) = flags
    assert f["place"] == "peak" and f["words"] == words
    assert f["drawing"]["parts"][0]["colour"] == colour
    assert bool(f["drawing"].get("inverted")) is inverted


def test_the_field_colour_is_the_first_colour_the_flag_word_names():
    assert viewer_flags.field_colour("the red ensign") == "red"
    assert viewer_flags.field_colour("the white ensign with the arms") == "white"
    assert viewer_flags.field_colour("the Dannebrog") == viewer_flags.PLAIN_CLOTH
