"""Package 33a: the checkpoint save (the cold review's item 6; `core.replay`).

A save stays a journal by definition; the checkpoint is the shortcut beside it. Proven
here: a world loaded from its checkpoint and a world replayed to the same tick carry on
to the same digest for a watch, with a fake watcher at its station, casts and bearings
in the account, the standing book firing and the weather and the sea in hand; the load
takes a fraction of the replay's time; a checkpoint that does not belong to the save
beside it, or is tampered with, is passed over for the replay; and the unpickler
refuses what is not the game's.
"""

from __future__ import annotations

import gzip
import io
import json
import pickle
import time

import pytest

from freesail.agents import fake as fake_mod
from freesail.api.session import ship_factory
from freesail.core import replay as replay_mod
from freesail.ui.console import station_watcher
from freesail.world.scenarios import begin, load_scenario, make_scenario_world

PASSAGE = "data/scenarios/gate-5b-passage.yaml"
SAVE_AT = 3 * 3600
WATCH = 3600


@pytest.fixture(scope="module")
def saved(tmp_path_factory):
    """A world of the passage with a fake watcher, three hours in, saved with its
    checkpoint, then carried on for a watch: the live digest to match."""
    path = tmp_path_factory.mktemp("cp") / "day.json"
    sf = load_scenario(PASSAGE)
    world = make_scenario_world(sf)
    station_watcher(world, "fake", out=None)
    begin(world, sf)
    world.run(SAVE_AT)
    world.submit("heave the lead")
    world.submit("take a bearing of the land")
    replay_mod.save_to_file(world, path)
    digest_at_save = world.log.digest()
    world.run(WATCH)
    return path, digest_at_save, world.log.digest(), world


def test_the_checkpoint_is_written_beside_the_save_and_names_it(saved):
    path, digest, _, world = saved
    cp = replay_mod.checkpoint_path(path)
    assert cp.exists() and cp.name == "day.checkpoint"
    with gzip.open(cp, "rb") as f:
        header = json.loads(f.readline().decode("utf-8"))
    assert header["format"] == replay_mod.CHECKPOINT_FORMAT
    assert header["seed"] == world.seed and header["end_tick"] == SAVE_AT
    assert header["digest"] == digest
    assert cp.stat().st_size < 2_000_000


def test_a_world_loaded_from_the_checkpoint_carries_on_to_the_replays_digest(saved):
    """The proof: the checkpoint's world and the replay's world, each given the live
    narrator the driver gives a loaded game, run a watch to the same digest as the world
    that was never saved."""
    path, digest_at_save, live_digest, _ = saved
    t0 = time.perf_counter()
    loaded, how = replay_mod.load(path, ship_factory)
    load_s = time.perf_counter() - t0
    assert how == "checkpoint"
    assert loaded.clock.tick == SAVE_AT and loaded.log.digest() == digest_at_save
    assert loaded.chart is not None and loaded.lookout.chart is loaded.chart
    assert loaded.ship.stepper is not None and loaded.ship.order_handler is not None
    assert loaded.navigation.world is loaded
    assert "watcher" in loaded.agents and isinstance(
        loaded.agents["watcher"].model, fake_mod.Transcript
    )
    station_watcher(loaded, "fake", out=None)
    loaded.run(WATCH)
    assert loaded.log.digest() == live_digest
    t0 = time.perf_counter()
    data = replay_mod.load_file(path)
    replayed = replay_mod.replay(data, ship_factory)
    replay_s = time.perf_counter() - t0
    assert replayed.log.digest() == digest_at_save
    station_watcher(replayed, "fake", out=None)
    replayed.run(WATCH)
    assert replayed.log.digest() == live_digest
    assert load_s < replay_s / 5, (load_s, replay_s)


def test_a_checkpoint_that_does_not_belong_is_passed_over_for_the_replay(saved, tmp_path):
    path, digest_at_save, _, world = saved
    # another save beside the same checkpoint: a different end tick
    other = tmp_path / "other.json"
    data = replay_mod.load_file(path)
    data["end_tick"] = SAVE_AT - 600
    other.write_text(json.dumps(data))
    replay_mod.checkpoint_path(other).write_bytes(replay_mod.checkpoint_path(path).read_bytes())
    loaded, how = replay_mod.load(other, ship_factory)
    assert how == "replay" and loaded.clock.tick == SAVE_AT - 600
    # a checkpoint whose world does not carry the digest it claims
    tampered = tmp_path / "tampered.json"
    tampered.write_text(json.dumps(replay_mod.load_file(path)))
    with gzip.open(replay_mod.checkpoint_path(path), "rb") as f:
        header = json.loads(f.readline().decode("utf-8"))
        body = f.read()
    header["digest"] = "0" * 64
    with gzip.open(replay_mod.checkpoint_path(tampered), "wb") as f:
        f.write(json.dumps(header).encode("utf-8") + b"\n")
        f.write(body)
    loaded, how = replay_mod.load(tampered, ship_factory)
    assert how == "replay" and loaded.log.digest() == digest_at_save
    # no checkpoint at all: the replay, as it always was
    alone = tmp_path / "alone.json"
    replay_mod.save_to_file(world, alone, checkpoint=False)
    assert not replay_mod.checkpoint_path(alone).exists()
    _, how = replay_mod.load(alone, ship_factory)
    assert how == "replay"


def test_the_unpickler_admits_the_games_classes_and_nothing_else():
    payload = pickle.dumps({"a": 1, "when": __import__("datetime").datetime(1805, 6, 10)})
    assert replay_mod._Unpickler(io.BytesIO(payload)).load()["a"] == 1
    foreign = pickle.dumps(__import__("os").system)
    with pytest.raises(pickle.UnpicklingError, match="may not hold"):
        replay_mod._Unpickler(io.BytesIO(foreign)).load()


def test_the_drivers_load_takes_the_checkpoint(saved, tmp_path):
    import argparse

    from freesail.ui.console import start_world

    path, digest_at_save, _, _ = saved
    args = argparse.Namespace(
        load=str(path), scenario=None, wind=None, heading=None, seed=None, ship=None
    )
    world, sf = start_world(args)
    assert sf is None and world.clock.tick == SAVE_AT
    assert getattr(world, "loaded_from", "") == "checkpoint"
    assert world.log.digest() == digest_at_save
