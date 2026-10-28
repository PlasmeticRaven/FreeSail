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
    assert crew is not None and isinstance(crew.own, hulls.Hull)
    assert crew.own.id == b.id and crew.own.world is crew and crew.own is not w.own
    assert crew.own.name == b.name and crew.ship is crew.own.ship and crew.ship is not w.ship
    assert crew.people is not w.people and crew.log is not w.log
    assert crew.own.chart is w.chart  # the shared chart, through her World's view of it
    # the checkpoint carries both hulls, and both worlds tick on alike
    data = replay_mod.checkpoint_bytes(w)
    again = replay_mod._Unpickler(io.BytesIO(data)).load()
    replay_mod._rebind(again)
    v = again.vessels.get(b.id)
    assert v.crew.own.id == b.id and v.crew.own.world is v.crew and again.own.id == PLAYER_ID
    again.run(60)
    w.run(60)
    assert again.log.digest() == w.log.digest()
    assert v.crew.log.digest() == crew.log.digest()


def _old_shape_checkpoint(world: World) -> bytes:
    """A checkpoint of `world` in the shape a build before step 1 wrote: the per-ship
    fields on the World's own dict and no `own`, pickled by the game's own pickler for
    everything else."""
    state = dict(world.__dict__)
    hull = state.pop("own")
    for name in hulls.PER_SHIP_FIELDS:
        if name in hull.__dict__:
            state[name] = hull.__dict__[name]
    state["chart"] = None
    state["_readings_view"] = None
    state["_readings_key"] = None
    state["_acts_frames"] = []

    class OldPickler(replay_mod._Pickler):
        def reducer_override(self, obj):
            if obj is world:
                return replay_mod._new, (World,), state
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
    assert "own" in loaded.__dict__ and isinstance(loaded.own, hulls.Hull)
    assert not any(name in loaded.__dict__ for name in hulls.PER_SHIP_FIELDS)
    assert loaded.own.world is loaded and loaded.own.id == PLAYER_ID
    assert loaded.log.digest() == w.log.digest() and loaded.ship.name == w.ship.name
    assert loaded.wind_settled == w.wind_settled and loaded.people.captain.name
    loaded.run(120)
    w.run(120)
    assert loaded.log.digest() == w.log.digest()
    # written again it holds `own`, and the pickler leaves the Hull's readings cache out
    again = replay_mod.checkpoint_bytes(loaded)
    copy = replay_mod._Unpickler(io.BytesIO(again)).load()
    assert "own" in copy.__dict__ and copy.own._readings_view is None
    assert copy.own._readings_key is None and copy.log.digest() == loaded.log.digest()


def test_lift_old_state_leaves_a_state_with_a_hull_as_it_is():
    w = make_world(7, CUTTER)
    state = {"own": w.own, "seed": 7}
    assert hulls.lift_old_state(w, state) is state and state["own"] is w.own
