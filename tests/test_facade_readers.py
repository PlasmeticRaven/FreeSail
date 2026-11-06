"""The hull façade's readers (package 97; `docs/design/Design-FacadeReaders.md`).

84's per-hull delegation answers for the hull whose block is running (`World.own`,
`World.as_hull`, `hulls.PER_SHIP_FIELDS`), so an object of one hull that reads her fields
through a World handle reads another hull's from inside that hull's block, and under
`follow` reads the followed hull's. The player's own hull's systems were built with the
World itself (a crewed hull's are rebound to her Hull by `crews.adopt_hull`); since this
package every hull's are bound to her Hull at her making (`hulls.bind_to_hull`), the
director's log, station and holder are read on the player's own hull by her own handle
(`director.director_hull`), and an act of hers is given to her again under `follow`
(`acts.target_of`).

Truths 7-422 to 7-425, and the guard that walks every hull's graph for a World handle.
"""

from __future__ import annotations

import pytest

from freesail.agents import director as D
from freesail.core import acts
from freesail.core.world import World
from freesail.world import seats
from freesail.world.hearing import station_spot
from freesail.world.hulls import _walkable
from tests.test_crews import _frigate_and_the_brig_x_on_the_sea

# The systems of a hull that read her fields through their `world` (the design note's list,
# item 1): each must read her own ship whichever hull's block is running.
SYSTEMS = (
    "people",
    "stations",
    "papers",
    "dealings",
    "navigation",
    "ground",
    "needs",
    "water",
    "health",
    "standing",
    "captain",
)


@pytest.fixture(scope="module")
def two_hulls():
    """The frigate (the player's ship, her own hull) hove to, the brig X promoted beside
    her as a hull of the World."""
    return _frigate_and_the_brig_x_on_the_sea()


# ---------------------------------------------------------------------------
# Truth 7-422: the player's hull's holder read under another hull's block
# ---------------------------------------------------------------------------


def test_truth_7_422_the_players_stations_read_her_own_people_under_another_hulls_block(
    two_hulls,
):
    """82b's finding: her `Stations` was built with the World, so `holder` read the running
    block's people and a station on her named another hull's man. Bound to her hull at her
    making, her stations, her people and every system of hers read her inside the brig's
    block as at home."""
    w, _b, x = two_hulls
    f = w.players
    home = {
        "captain": f.stations.holder("captain").name,
        "master": f.stations.holder("master").name,
        "names": f.stations.names(),
        "aboard": f.stations.aboard("second officer"),
    }
    assert home["captain"] != x.people.captain.name  # two hulls, two captains
    with w.as_hull(x):
        assert w.own is x  # the brig's block is running
        assert f.stations.holder("captain").name == home["captain"]
        assert f.stations.holder("master").name == home["master"]
        assert f.stations.names() == home["names"]
        assert f.stations.aboard("second officer") == home["aboard"]
        for name in SYSTEMS:
            system = getattr(f, name)
            assert system.world is f, name  # bound to her hull, not the World
            assert system.world.ship is f.ship, name
    # and the brig's own read hers in the player's block (the far side, unchanged)
    with w.as_hull(f):
        assert x.stations.holder("captain").name == x.people.captain.name


# ---------------------------------------------------------------------------
# Truth 7-423: the director's own writes under `follow`
# ---------------------------------------------------------------------------


def test_truth_7_423_the_directors_writes_land_on_the_players_hull_under_follow():
    """65's finding: the director's log is a station's journal of the hull it is kept on,
    and under `follow` the World's names read the followed hull, so the brief's, the
    budget's and the seat's lines landed in the brig's journals. They are the game's one
    log, on the player's own hull, whichever is followed; its station is bound there and its
    holder found there; an act of hers journaled under `follow` is given to her again."""
    w, _b, x = _frigate_and_the_brig_x_on_the_sea()
    f = w.players
    w.follow('"X"')
    assert w.own is x and w.followed == x.id
    D.set_brief(w, "quiet-passage", source="the test")
    D.set_budget(w, "budget 60 samples, 10 acts", source="the test")
    seats._log(w, "The seat held: a test's seat for 1 hour.")
    kinds = [e.kind for e in f.agent_journals[D.DIRECTOR].entries]
    assert kinds.count("director.brief") == 2, kinds  # the brief, and the budget's brief
    assert "director.seat" in kinds, kinds
    assert D.DIRECTOR not in x.agent_journals  # nothing of the director's on the brig
    assert D.log_of(w) is f.agent_journals[D.DIRECTOR]
    assert D.log_of(x) is D.log_of(w)  # read from either hull's handle, the one log
    assert f.stations.aboard(D.DIRECTOR) and not x.stations.aboard(D.DIRECTOR)
    # an act of the player's own hull ("" by `hull_id_of`) is hers under `follow`
    with w.as_hull(f):
        assert acts.hull_id_of(w) == ""
    assert acts.act_target_of(w, {"station": D.DIRECTOR}) is f
    assert acts.act_target_of(w, {"station": "captain", "ship": x.id}) is x
    # an input keyed "" is the followed hull's, as `World.submit` keys it, and stays so
    assert acts.target_of(w, {"order": "set the royals"}) is w and w.own is x
    w.follow('"the ship"')
    assert acts.act_target_of(w, {"station": D.DIRECTOR}) is w  # the World itself, as before


# ---------------------------------------------------------------------------
# Truth 7-424: a façade read from inside another hull's order
# ---------------------------------------------------------------------------


def test_truth_7_424_a_hulls_facade_read_from_inside_another_hulls_order_reads_her(two_hulls):
    """65's finding: `station_spot(hull, ...)` read inside the brig's `say` gave the
    frigate's captain the brig's quarterdeck (mended for `_say` alone by `station_spot_on`).
    An order of the brig's runs in her block (`Hull.submit`); every read of the frigate's
    by her hull's handle inside it is the frigate's, the spot by the plain `station_spot`."""
    w, _b, x = two_hulls
    f = w.players
    at_home = {s: station_spot(f, s) for s in ("captain", "master", "lookout")}
    assert at_home["captain"][1] == f.id
    seen: dict[str, object] = {}
    real = World.submit

    def submit(self, text, *a, **kw):
        # inside the brig's order, before it is given: the frigate read by her handle
        if self.own is x and not seen:
            seen["spots"] = {s: station_spot(f, s) for s in at_home}
            seen["holder"] = f.stations.holder("captain").name
            seen["water"] = f.water.ship.name
            seen["reckoning"] = f.navigation.world.ship.name
        return real(self, text, *a, **kw)

    World.submit = submit
    try:
        x.submit("set the topsails")
    finally:
        World.submit = real
    assert seen, "the brig's order was not given in her block"
    assert seen["spots"] == at_home
    assert seen["holder"] == f.stations.holder("captain").name
    assert seen["water"] == seen["reckoning"] == f.ship.name != x.ship.name


# ---------------------------------------------------------------------------
# Truth 7-425: the hail's refusal gives the strangers' words
# ---------------------------------------------------------------------------


def test_truth_7_425_a_hail_to_no_sail_in_sight_is_refused_with_the_strangers_words(two_hulls):
    """95's builder's finding: `hail_order`'s refusal said "the strangers are listed" and
    listed none; it gives the strangers' words as the lookout's refusal does."""
    w, _b, _x = two_hulls
    with w.as_hull(w.players):
        e = w.submit("hail the frigate right astern: what ship is that?")
    assert e.kind == "order.rejected", e.text
    assert e.text.endswith(
        "Nothing in sight answers to 'the frigate right astern'; the strangers: a brig right "
        "ahead, bearing N, distant three miles: standing to the north-eastward (NE by N), "
        "under plain sail."
    ), e.text
    assert "the strangers are listed" not in e.text


# ---------------------------------------------------------------------------
# The guard: no hull's own graph holds the World
# ---------------------------------------------------------------------------

# The references to the World a hull's graph keeps by design, each a thing of the sea or
# of the world and not of hers (the design note's "kept"): her view of the sail (a
# `HullView`'s `game`, the sea it views) and her far body's brain (`vessel`, the sea's).
KEPT = {("HullView", "game"), ("FarCaptain", "world")}


def world_handles(hull, world) -> list[str]:
    """The paths in a hull's own graph at which the World itself is held (her back-
    reference `hull.world` aside); the shared things are not entered."""
    skip = {
        id(x)
        for x in (
            world,
            world.clock,
            getattr(world, "chart", None),
            world.registry,
            world.ports,
            world.nations,
            getattr(world, "tide", None),
            getattr(world, "systems", None),
            getattr(world, "weather", None),
            getattr(world, "squadrons", None),
            getattr(world, "business", None),
            world.sea_vessels,
            world.hulls,
        )
        if x is not None
    }
    found, seen, stack = [], set(), [(hull, "hull")]
    while stack:
        obj, path = stack.pop()
        if id(obj) in seen or id(obj) in skip:
            continue
        seen.add(id(obj))
        if isinstance(obj, dict):
            items = [(repr(k), v) for k, v in obj.items()]
        elif isinstance(obj, (list, tuple, set, frozenset)):
            items = [(f"[{i}]", v) for i, v in enumerate(obj)]
        else:
            d = getattr(obj, "__dict__", None)
            if d is None:
                continue
            items = list(d.items())
        for key, v in items:
            if obj is hull and key == "world":
                continue
            if v is world:
                if (type(obj).__name__, key) not in KEPT:
                    found.append(f"{path}.{key} ({type(obj).__name__})")
            elif _walkable(v):
                stack.append((v, f"{path}.{key}"))
    return found


def test_the_guard_no_hulls_system_holds_the_world_whatever_is_followed_or_saved():
    """Every hull's systems hold her Hull and not the World: the player's own at her making,
    a crewed ship's at her adoption, the keepers made at a tick, the stations seated on
    either, through `follow` and back, and after a checkpoint's round trip. A new system
    built with the World (`X(self)` in `World.__init__`, or a reader kept on one) fails here
    by its path."""
    import io

    from freesail.core import replay
    from tests.test_director import seat_captain

    w, _b, x = _frigate_and_the_brig_x_on_the_sea()
    D.set_brief(w, "quiet-passage", source="the test")
    seat_captain(w)
    w.follow('"X"')
    w.run(61)
    w.follow('"the ship"')
    w.run(61)
    for hull in w.hulls.values():
        assert world_handles(hull, w) == [], hull
    # the checkpoint's own road (`core.replay`: its pickler leaves the harnesses' doors out)
    w2 = replay._Unpickler(io.BytesIO(replay.checkpoint_bytes(w))).load()
    for hull in w2.hulls.values():
        assert world_handles(hull, w2) == [], hull
