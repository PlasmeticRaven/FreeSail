"""Package 84, step 1: the Hull extracted behind the World's names (`freesail.world.hulls`;
`docs/design/Design-OneWorld.md` §2.2 and its migration's first step).

Proven here: a World keeps what it keeps of one ship on a `Hull` (`world.own`), and every
per-ship name of the World reads and writes the Hull's field, so nothing that reads a World
moves; the Hull reads the World's shared fields under their names; a crewed ship's World
has a Hull of her own under her vessel's id; a checkpoint written before the Hull (the
per-ship fields on the World's own dict) converts on load and carries on to the same digest
as the world it was written from; the kept saves of `tests/fixtures/saves/` are the same
proof on real files (`test_checkpoint.py`).
"""

from __future__ import annotations

import io
import pickle

import pytest

from freesail.api.session import make_world
from freesail.core import replay as replay_mod
from freesail.core.world import World
from freesail.world import hulls
from freesail.world.brains import PLAYER_ID

CUTTER = "data/ships/cutter.yaml"


def test_the_worlds_per_ship_names_are_the_hulls_fields_and_the_shared_ones_stay_its_own():
    w = make_world(7, CUTTER)
    assert isinstance(w.own, hulls.Hull) and w.own.world is w and w.own.id == PLAYER_ID
    # every per-ship field lives on the Hull and is read through the World under its name
    for name in hulls.PER_SHIP_FIELDS:
        assert name not in w.__dict__, name
        if hasattr(w.own, name):
            assert getattr(w, name) is getattr(w.own, name), name
    assert w.ship is w.own.ship and w.log is w.own.log and w.people is w.own.people
    assert w.water is w.own.water and w.health is w.own.health  # package 73's keepers, hers
    # the shared fields stay the World's, and the Hull reads them under the same names
    for name in hulls.SHARED_FIELDS:
        assert name not in w.own.__dict__, name
        assert getattr(w.own, name) is getattr(w, name), name
    assert w.own.clock is w.clock and w.own.rng is w.rng and w.own.vessels is w.vessels
    # since step 6 her seed, her streams, her scenario and her view of the sail are hers
    assert all(name in w.own.__dict__ for name in ("seed", "scenario", "rng", "vessels"))
    assert w.hulls == {PLAYER_ID: w.own} and w.followed == PLAYER_ID and w.is_followed
    # the Hull's own reads of her state agree with the World's
    assert w.own.name == w.ship.name and w.own.position == w.position
    assert w.own.ship_x == w.ship_x and w.own.at_anchor == w.at_anchor
    assert w.own.readings is w.readings and w.own.daylight == w.daylight


def test_setting_a_per_ship_name_through_the_world_sets_the_hull_and_a_missing_one_is_missing():
    w = make_world(7, CUTTER)
    token = object()
    w.conditions = token
    assert w.own.conditions is token and w.conditions is token
    w.own._position = None
    assert w.position is None
    # a per-ship name the Hull has not got reads as a missing attribute, as it did
    del w.own.fishery
    assert not hasattr(w, "fishery") and getattr(w, "fishery", "none") == "none"
    with pytest.raises(AttributeError):
        _ = w.fishery
    # the class defaults for a checkpoint from before are the Hull's
    assert hulls.Hull.wind_settled is True and hulls.Hull._recurring_said is None
    assert w.wind_settled is True and w._brought_up_s == 0


def test_the_hull_records_and_submits_through_its_world():
    w = make_world(7, CUTTER)
    n = len(w.log)
    e = w.own.submit("the people")
    assert e.kind.startswith("query.") and len(w.log) > n and w.log[-1] is w.own.log[-1]
    w.own.record("routine", "test.line", "A line of hers.")
    assert w.log[-1].kind == "test.line"


def test_a_crewed_ships_world_has_a_hull_of_her_own_under_her_vessels_id():
    from tests.test_crews import hove_to_world, put

    w = hove_to_world()
    b = put(
        w, "merchant brig", "britain", "49 33 N 5 30 W", "bound for Falmouth", "bound for Falmouth"
    )
    w.run(61)
    crew = b.crew
    # since step 6 she is a Hull of the one World, her own being herself (the façade)
    assert crew is not None and isinstance(crew, hulls.Hull) and crew.own is crew
    assert crew.id == b.id and crew.world is w and crew is not w.own and w.hulls[b.id] is crew
    assert crew.name == b.name and crew.ship is not w.ship
    assert crew.people is not w.people and crew.log is not w.log
    assert crew.chart is w.chart and crew.clock is w.clock  # the shared, through the façade
    assert crew.rng is not w.rng and crew.vessels is not w.vessels
    # the checkpoint carries both hulls, and both worlds tick on alike
    data = replay_mod.checkpoint_bytes(w)
    again = replay_mod._Unpickler(io.BytesIO(data)).load()
    replay_mod._rebind(again)
    v = again.vessels.get(b.id)
    assert v.crew.id == b.id and v.crew.world is again and again.own.id == PLAYER_ID
    assert again.hulls[b.id] is v.crew
    again.run(60)
    w.run(60)
    assert again.log.digest() == w.log.digest()
    assert v.crew.log.digest() == crew.log.digest()


def _old_shape_checkpoint(world: World) -> bytes:
    """A checkpoint of `world` in the shape a build before package 84 wrote: every World's
    per-ship fields on its own dict and no `own` or `registry` (step 1), each World's
    `People` with its own `people` and `things` lists and no hull, each person with his
    `aboard` as a bool and no whereabouts, each thing without its hull (step 2); pickled by
    the game's own pickler for everything else. Every World of the graph is written so,
    the crewed ships' included."""
    from freesail.world.people import People, Person
    from freesail.world.ports import Ports
    from freesail.world.ships import Vessels
    from freesail.world.things import Thing

    def world_state(w: World) -> dict:
        state = dict(w.__dict__)
        hull = state.pop("_own")  # `own` is a property over `_own` since step 6
        state.pop("hulls", None)
        state.pop("followed", None)
        state.pop("registry", None)
        for name in hulls.PER_SHIP_FIELDS:
            if name in hull.__dict__ and name != "dealings":
                state[name] = hull.__dict__[name]
        # the one `Ports` of before step 3: the port files and her dealings in one object
        old_ports = Ports.__new__(Ports)
        for key, value in hull.dealings.__dict__.items():
            if key != "world":
                old_ports.__dict__[key] = value
        old_ports.world = w
        old_ports.ports = w.ports.ports
        state["ports"] = old_ports
        state["chart"] = None
        state["_readings_view"] = None
        state["_readings_key"] = None
        state["_acts_frames"] = []
        return state

    def crew_state(h: hulls.Hull) -> dict:
        # a hull of step 6 written as the crewed World a build before step 6 had: her fields
        # on the World's dict with `parent`, `vessel` and `shape`, as `world_state` writes
        # the World's own
        state = {k: v for k, v in h.__dict__.items() if k in hulls.PER_SHIP_FIELDS}
        state.pop("dealings", None)
        state["parent"] = h.world
        state["vessel"] = h.vessel
        state["shape"] = h.shape
        state["clock"] = h.world.clock
        old_ports = Ports.__new__(Ports)
        for key, value in h.dealings.__dict__.items():
            if key != "world":
                old_ports.__dict__[key] = value
        old_ports.world = h
        old_ports.ports = h.world.ports.ports
        state["ports"] = old_ports
        state["chart"] = None
        state["_readings_view"] = None
        state["_readings_key"] = None
        state["_acts_frames"] = []
        return state

    def people_state(people: People) -> dict:
        state = dict(people.__dict__)
        hid = state.pop("hull_id")
        state["people"] = list(people.registry.company(hid))
        state["things"] = [
            t
            for t in people.registry.things
            if (t.hull == hid) or (t.keeper and any(p.id == t.keeper for p in state["people"]))
        ]
        return state

    def person_state(p: Person) -> dict:
        state = dict(p.__dict__)
        state.pop("hull", None)
        state.pop("home", None)
        state["aboard"] = p.aboard
        return state

    def thing_state(t: Thing) -> dict:
        state = dict(t.__dict__)
        state.pop("hull", None)
        return state

    def ports_state(ports: Ports) -> dict:
        # a step 3 `Ports` met on its own (the shared one): written as a bare old one
        return dict(ports.__dict__)

    class OldPickler(replay_mod._Pickler):
        def reducer_override(self, obj):
            if isinstance(obj, World):
                return replay_mod._new, (type(obj),), world_state(obj)
            if isinstance(obj, hulls.Hull) and obj is not world.own:
                from freesail.world.crews import CrewedWorld

                return replay_mod._new, (CrewedWorld,), crew_state(obj)
            if isinstance(obj, Vessels) and obj.__dict__.get("own") is not None:
                # the sea of before step 7: no vessel of the player's on it, no `own`
                state = dict(obj.__dict__)
                state["vessels"] = [v for v in obj.vessels if v is not obj.own]
                state.pop("own", None)
                return replay_mod._new, (Vessels,), state
            if isinstance(obj, Ports):
                return replay_mod._new, (Ports,), ports_state(obj)
            if isinstance(obj, People):
                return replay_mod._new, (People,), people_state(obj)
            if isinstance(obj, Person):
                return replay_mod._new, (Person,), person_state(obj)
            if isinstance(obj, Thing):
                return replay_mod._new, (Thing,), thing_state(obj)
            return super().reducer_override(obj)

    buf = io.BytesIO()
    OldPickler(buf, protocol=pickle.HIGHEST_PROTOCOL).dump(world)
    return buf.getvalue()


def test_a_checkpoint_from_before_the_hull_converts_on_load_and_carries_on_alike():
    w = make_world(7, CUTTER)
    w.run(300)
    w.submit("heave the lead")
    old = _old_shape_checkpoint(w)
    loaded = replay_mod._Unpickler(io.BytesIO(old)).load()
    replay_mod._rebind(loaded)
    assert "_own" in loaded.__dict__ and isinstance(loaded.own, hulls.Hull)
    assert not any(name in loaded.__dict__ for name in hulls.PER_SHIP_FIELDS)
    # the ports parted (step 3): the world's files on `ports`, her dealings on the hull
    assert type(loaded.ports).__name__ == "Ports" and "boat" not in loaded.ports.__dict__
    assert type(loaded.dealings).__name__ == "Dealings" and loaded.dealings.world is loaded
    assert loaded.ports.ports is loaded.dealings.ports and loaded.dealings.boat is not None
    assert loaded.own.world is loaded and loaded.own.id == PLAYER_ID
    assert loaded.log.digest() == w.log.digest() and loaded.ship.name == w.ship.name
    assert loaded.wind_settled == w.wind_settled and loaded.people.captain.name
    # the registry made at the load (step 2): his company's whereabouts from the bools
    assert loaded.registry.hulls == [PLAYER_ID] and loaded.people.hull_id == PLAYER_ID
    assert loaded.people.people is loaded.registry.company(PLAYER_ID)
    assert [p.name for p in loaded.people.all] == [p.name for p in w.people.all]
    for p in loaded.people.all:
        assert (p.hull, p.home, p.aboard) == (PLAYER_ID, PLAYER_ID, True)
    loaded.run(120)
    w.run(120)
    assert loaded.log.digest() == w.log.digest()
    # written again it holds `own`, and the pickler leaves the Hull's readings cache out
    again = replay_mod.checkpoint_bytes(loaded)
    copy = replay_mod._Unpickler(io.BytesIO(again)).load()
    assert "_own" in copy.__dict__ and copy.own._readings_view is None
    assert copy.own._readings_key is None and copy.log.digest() == loaded.log.digest()


def test_lift_old_state_leaves_a_state_with_a_hull_as_it_is():
    w = make_world(7, CUTTER)
    state = {"own": w.own, "seed": 7}
    assert hulls.lift_old_state(w, state) is state and state["_own"] is w.own
    assert "own" not in state  # step 6: `_own` behind the property
    state = {"_own": w.own}
    assert hulls.lift_old_state(w, state) is state and state["_own"] is w.own


def test_a_checkpoint_from_before_with_a_crewed_ship_and_persons_moved_converts_whole():
    """The owner's saves' shape: a crewed ship's World inside the checkpoint, written before
    the Hull and the registry. Loaded, each World has its Hull under the right id (the
    crewed World's own `__setstate__` runs before the parent's dict is filled, so the
    parent's puts her vessel's id right), the one registry holds both companies in the
    hulls' order, a person ashore keeps his whereabouts and a thing its hull, and both
    worlds carry on to the live ones' digests."""
    from freesail.world import things as TH
    from tests.test_crews import hove_to_world, put

    w = hove_to_world()
    b = put(
        w, "merchant brig", "britain", "49 33 N 5 30 W", "bound for Falmouth", "bound for Falmouth"
    )
    w.run(61)
    crew = b.crew
    w.world_order('person: make "Mr Gill", a merchant, ashore at Falmouth, at the market', "t")
    w.world_order("aboard: a sealed packet, on the cabin table", "t")
    crew.world_order("aboard: a letter, in the hold", "t")
    master = crew.people.find("the master")
    master.aboard, master.where, master.port, master.ashore_at = False, "shore", "falmouth", "quay"
    w.run(30)
    old = _old_shape_checkpoint(w)
    loaded = replay_mod._Unpickler(io.BytesIO(old)).load()
    replay_mod._rebind(loaded)
    v = loaded.vessels.get(b.id)
    lc = v.crew
    assert loaded.own.id == PLAYER_ID and lc.id == b.id and lc.world is loaded  # a hull now
    assert lc.registry is loaded.registry and loaded.registry.hulls == [PLAYER_ID, b.id]
    assert lc.people.hull_id == b.id and lc.people.people is loaded.registry.company(b.id)
    assert [p.name for p in lc.people.all] == [p.name for p in crew.people.all]
    assert [p.name for p in loaded.people.all] == [p.name for p in w.people.all]
    gill = loaded.people.find("Mr Gill")
    assert gill is not None and gill.hull is None and gill.home == PLAYER_ID and not gill.aboard
    lm = lc.people.find("the master")
    assert lm.hull is None and lm.home == b.id and (lm.port, lm.ashore_at) == ("falmouth", "quay")
    assert all(p.hull == b.id for p in lc.people.all if p is not lm)
    things = {t.name: t for t in TH.things_of(loaded)}
    assert things["a sealed packet"].hull == PLAYER_ID and things["a letter"].hull == b.id
    assert TH.lying_aboard(loaded) == {"cabin": [things["a sealed packet"]]}
    assert TH.lying_aboard(lc) == {"hold": [things["a letter"]]}
    loaded.run(60)
    w.run(60)
    assert loaded.log.digest() == w.log.digest() and lc.log.digest() == crew.log.digest()


# -- step 7: the player's ship a hull among the hulls; the shadow retired ------------------


def test_the_players_ship_is_a_vessel_of_the_sea_last_in_the_list_and_her_hull_the_followed():
    """Package 84, step 7: the player's ship is a vessel of the sea under `ships.PLAYER_ID`
    (the one definition), appended last and kept last when a vessel is added; her hull is
    the followed hull and the followed hull's `vessel` is she; `World.vessel` names her for
    the followed hull as it names another hull's far body; the shadow's name still answers
    with her and never moves her."""
    from freesail.world import ships as SH
    from freesail.world.brains import PLAYER_ID as from_brains
    from tests.test_crews import hove_to_world, put

    assert from_brains is SH.PLAYER_ID == "the ship"
    w = hove_to_world()
    own = w.vessels.own
    assert own is not None and own.id == SH.PLAYER_ID and own is w.vessels.vessels[-1]
    assert own.crew is w.own and w.own.vessel is own and w.vessel is own
    assert own.detail == "crewed" and own.brain is None and own.name == w.ship.name
    b = put(
        w, "merchant brig", "britain", "49 33 N 5 30 W", "bound for Falmouth", "bound for Falmouth"
    )
    assert w.vessels.vessels[-1] is own and w.vessels.vessels[-2] is b
    assert w.vessels.player_shadow(w) is own
    pos = own.position
    w.run(120)
    assert own.position == w.position and own.position != pos  # brought up to her truth
    assert own.speed_kn < 1.5  # hove to, a little way on; her sail state the shadow's words
    assert not own.done and own in w.vessels.vessels and w.vessels.vessels[-1] is own


def test_the_players_vessel_is_left_out_of_every_viewers_own_sail():
    """Rule 3 of the design's 3.3: the player's lookout never sights her own body, a hull's
    view of the sea has the player's ship but not the hull's own, and a brain's strangers
    list has her as the shadow gave her, nearest first."""
    from freesail.world import brains as B
    from freesail.world import ships as SH
    from tests.test_crews import hove_to_world, put

    w = hove_to_world()
    b = put(
        w, "merchant brig", "britain", "49 33 N 5 30 W", "bound for Falmouth", "bound for Falmouth"
    )
    w.run(61)
    own = w.vessels.own
    seen = w.vessels.in_sight(w.position, 20.0, 10.0, "day", viewer=own)
    assert [s.feature.name for s in seen] and all(
        "sail:the ship" not in s.feature.name for s in seen
    )
    assert not [
        e
        for e in w.log
        if e.kind == "lookout.sighting" and "a cable" in e.text and "frigate" in e.text
    ]
    hull = b.crew
    assert hull is not None and hull.shape == "full"
    theirs = hull.vessels.vessels
    assert own in theirs and b not in theirs and all(v is not b for v in theirs)
    p = B.perceive_vessel(w, b, b.brain)
    ids = [s["id"] for s in p.strangers]
    assert SH.PLAYER_ID in ids and b.id not in ids


def test_the_players_body_is_found_from_a_hulls_tick_as_any_vessels_is():
    """`action._body_of` and `target_of` find the player's ship through her vessel's hull as
    they find a crewed ship's, with the World under another hull's swap (step 6's finding,
    settled by one rule in step 7)."""
    from freesail.combat.action import _body_of
    from freesail.world import ships as SH
    from tests.test_crews import hove_to_world, put

    w = hove_to_world()
    b = put(
        w, "merchant brig", "britain", "49 33 N 5 30 W", "bound for Falmouth", "bound for Falmouth"
    )
    w.run(61)
    hull = b.crew
    assert _body_of(w, SH.PLAYER_ID) is w.ship and _body_of(w, b.id) is hull.ship
    with w.as_hull(hull):
        assert _body_of(w, SH.PLAYER_ID) is w.own.parent.ship
        assert _body_of(hull, SH.PLAYER_ID) is w.hulls[w.followed].ship
    assert _body_of(hull, SH.PLAYER_ID) is w.vessels.own.crew.ship


def test_a_checkpoint_keeps_the_players_vessel_as_the_seas_own(tmp_path):
    from tests.test_crews import hove_to_world, put

    w = hove_to_world()
    put(w, "merchant brig", "britain", "49 33 N 5 30 W", "bound for Falmouth", "bound for Falmouth")
    w.run(61)
    path = replay_mod.write_checkpoint(w, tmp_path / "own.ckpt")
    _, c = replay_mod.read_checkpoint(path)
    own = c.vessels.own
    assert own is not None and own is c.vessels.vessels[-1] and own.crew is c.own
    assert c.own.vessel is own and c.vessel is own
    c.run(60)
    w.run(60)
    assert c.log.digest() == w.log.digest()
