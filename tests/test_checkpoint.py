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
from pathlib import Path

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


# ---------------------------------------------------------------------------
# Package 37d, item 4: old checkpoints kept as tests (the review of gate 5c's playtests,
# section 9 under "Replay": "keep two or three of this playtest's own checkpoints as
# tests, so that a build which could no longer read them is caught on the day it is
# made")
# ---------------------------------------------------------------------------
#
# `tests/fixtures/saves/` holds two of the playtest's saves with their checkpoints,
# unchanged (the cutter of m5c at tick 34,091; the Harpy of m5c-b before 37c at tick
# 602,100; `CHANGES-m5c-c.md` says what each is), and a third of package 37d's own
# making (`THE_37D_SAVE`, below). The two playtest saves hold a model's transcript and
# journal and the owner's typed lines, and whether they go into the repository is the
# owner's to say: their tests skip, saying so, when the files are not there. A change
# that breaks one of these is mended with a class default or a step in
# `core.replay._rebind`, never by changing a fixture.

FIXTURE_SAVES = Path(__file__).resolve().parent / "fixtures" / "saves"
PLAYTEST_SAVES = {
    # the name: (the tick it was saved at, the station whose transcript it holds)
    "m5c-cutter-tick34091": (34091, "officer of the watch"),
    "m5c-b-harpy-tick602100": (602100, "officer of the watch"),
}
A_GLASS = 1800
A_WATCH = 4 * 3600


def _playtest_save(name: str) -> Path:
    save = FIXTURE_SAVES / f"{name}.json"
    if not save.exists() or not replay_mod.checkpoint_path(save).exists():
        pytest.skip(
            f"{name}: this playtest save is not in the tree (it holds a model's transcript "
            "and journal and the owner's typed lines; whether it goes into the repository "
            "is the owner's to say), so its test is skipped"
        )
    return save


def _header(save: Path) -> dict:
    with gzip.open(replay_mod.checkpoint_path(save), "rb") as f:
        return json.loads(f.readline().decode("utf-8"))


def _loaded_run_saved_and_loaded_again(save: Path, ticks: int, tmp_path: Path):
    """A kept save loaded from its checkpoint under this build (the road said to be the
    checkpoint, the log's digest the header's), run on for `ticks`, saved and loaded
    again. Returns the world run on and the first load's report."""
    header = _header(save)
    world, report = replay_mod.load_report(save, ship_factory)
    assert report.how == "checkpoint" and report.checkpoint == ""
    assert world.clock.tick == header["end_tick"]
    assert world.log.digest() == header["digest"]
    lines_at_load = len(world.log)
    world.run(ticks)
    assert world.clock.tick == header["end_tick"] + ticks and len(world.log) > lines_at_load
    again = replay_mod.save_to_file(world, tmp_path / save.name)
    copy, second = replay_mod.load_report(again, ship_factory)
    assert second.how == "checkpoint" and second.words == []
    assert copy.clock.tick == world.clock.tick and copy.log.digest() == world.log.digest()
    return world, report


@pytest.mark.parametrize("name", sorted(PLAYTEST_SAVES))
def test_a_playtest_save_loads_from_its_checkpoint_and_runs_on_a_glass(name, tmp_path):
    save = _playtest_save(name)
    tick, station = PLAYTEST_SAVES[name]
    world, report = _loaded_run_saved_and_loaded_again(save, A_GLASS, tmp_path)
    assert world.clock.tick == tick + A_GLASS
    # written before the stamp: one line says so, and the game is this build's from here
    assert report.build is None and report.checkpoint_build is None
    assert len(report.words) == 1 and report.words[0].startswith(
        "The checkpoint was written by another build (unstamped, before 37d) and is read by "
        "this one (m5c-c/37g, rules "
    )
    assert station in report.transcripts and station in world.agents
    here = replay_mod.build_stamp()
    assert world.played_under == [None, here]
    # saved again it is stamped by this build and says the game was begun under another;
    # without its checkpoint that save is not replayed for this build's own
    data = replay_mod.load_file(tmp_path / save.name)
    assert data["build"] == here and data["builds"] == [None, here]
    with pytest.raises(replay_mod.ReplayRefused) as refused:
        replay_mod.check_replay(data, "again.json")
    assert refused.value.report.words[1].startswith(
        "The save was written by this build (m5c-c/37g, rules "
    ) and refused.value.report.words[1].endswith(
        "but the game in it was played in part under another (unstamped, before 37d) and "
        "taken up from its checkpoint."
    )


@pytest.mark.parametrize("name", sorted(PLAYTEST_SAVES))
def test_a_playtest_save_loads_from_its_checkpoint_and_runs_on_a_watch(name, tmp_path):
    save = _playtest_save(name)
    world, _ = _loaded_run_saved_and_loaded_again(save, A_WATCH, tmp_path)
    assert world.clock.tick == PLAYTEST_SAVES[name][0] + A_WATCH


def test_the_cutters_save_is_refused_a_replay_without_the_flag(tmp_path):
    """Item 2 on a real save: the cutter's game of m5c with a model as mate, without its
    checkpoint beside it, is not replayed unless asked for, and the words say why."""
    save = _playtest_save("m5c-cutter-tick34091")
    alone = tmp_path / "cutter.json"
    alone.write_bytes(save.read_bytes())
    with pytest.raises(replay_mod.ReplayRefused) as refused:
        replay_mod.load(alone, ship_factory)
    words = refused.value.report.words
    assert words[0] == f"Not replayed: {alone}."
    assert words[1].startswith(
        "The save was written by another build (unstamped, before 37d); this is m5c-c/37g, "
    )
    assert words[2] == "Its checkpoint was not used: there is no checkpoint beside the save."
    assert words[3].startswith("It holds the officer of the watch's transcript (")
    assert "would not be the game that was played" in words[3]
    assert words[4].endswith("to replay it all the same, say --replay-anyway.")
    # the rule alone, for the doors that always replay, and the flag's leave
    data = replay_mod.load_file(alone)
    with pytest.raises(replay_mod.ReplayRefused):
        replay_mod.check_replay(data, alone)
    report = replay_mod.check_replay(data, alone, replay_anyway=True)
    assert report.how == "replay" and report.anyway and len(report.words) == 3


# The third kept save, of package 37d's own making (item 4): a short scripted game with
# the fake officer at his station and standing by, saved by the build of 37d on
# 2026-10-06 and never made again. It is kept so that a later build which can no longer
# read a checkpoint of 37d is caught on the day it is made; `make_the_37d_save` is how it
# was made, written down for the record and run by no test. Making it again would defeat
# it: the file would then be the later build's own.
THE_37D_SAVE = FIXTURE_SAVES / "m5c-c-37d-officer-tick5400.json"
THE_37D_TICK = 5400


def make_the_37d_save(path: Path = THE_37D_SAVE) -> Path:
    """The frigate of the gate-5b passage off Ushant at seed 7 under her book (the chart,
    the tide, the weather's systems, the reckoning with a bearing and a fix in it, the
    lookout with land, the shore and a departure in sight), a scripted officer seated at
    tick 0 after the game's opening line; the captain gives him the deck and his word for
    a fix; he takes the deck, takes a fix, heaves the log and stands by until eight
    bells; saved an hour and a half out, the officer standing by. RUN ONCE, on 2026-10-06;
    not to be run again."""
    from freesail.agents import Fake, Harness, SamplingPolicy, call, reply
    from freesail.agents.agent import officer

    sf = load_scenario(PASSAGE)
    world = make_scenario_world(sf)
    world.record_driver("routine", "driver.book", "The book of standing orders is the passage's.")
    script = [
        reply("I have the deck, sir.", call("journal", note="Took the deck off Ushant.")),
        reply("", call("submit_order", text="take a fix")),
        reply("", call("submit_order", text="heave the log")),
        reply("The departure is fixed; standing by.", call("stand_by", until="eight bells")),
    ]
    h = Harness(
        world,
        officer(SamplingPolicy.in_lockstep(1800, "notable", "urgent"), world=world),
        Fake(script),
        save=lambda w, why: None,
    )
    world.submit("you have the deck")
    world.submit("you may take a fix")
    h.start()
    begin(world, sf)
    world.run(THE_37D_TICK)
    assert world.clock.tick == THE_37D_TICK
    assert "standing by" in h.agent.words(), h.agent.words()
    return replay_mod.save_to_file(world, path)


def _the_37d_save() -> Path:
    assert THE_37D_SAVE.exists() and replay_mod.checkpoint_path(THE_37D_SAVE).exists(), (
        "the kept save of package 37d is gone from tests/fixtures/saves/; it is not to be "
        "made again (restore it from the repository)"
    )
    return THE_37D_SAVE


def test_the_packages_own_save_loads_from_its_checkpoint_and_runs_on_a_glass(tmp_path):
    """Item 4: the save of 37d's own making, with the fake officer at his station and
    standing by, loads from its checkpoint under this build, the road said to be the
    checkpoint and the log's digest the header's; it runs on a glass and is saved and
    loaded again. Its stamp is the build's that made it, which a later build is not."""
    save = _the_37d_save()
    header = _header(save)
    assert header["build"]["name"] == "m5c-c/37d" and len(header["build"]["rules"]) == 16
    assert header["end_tick"] == THE_37D_TICK
    data = replay_mod.load_file(save)
    assert data["build"] == header["build"] and data["builds"] == [header["build"]]
    record = data["agents"][0]
    assert record["station"]["name"] == "officer of the watch"
    # seated at tick 0 after the opening line and the captain's two words to him
    assert record["stationed_tick"] == 0 and record["stationed_after_inputs"] == 3
    world, report = _loaded_run_saved_and_loaded_again(save, A_GLASS, tmp_path)
    assert report.build == header["build"] and report.checkpoint_build == header["build"]
    officer = world.agents["officer of the watch"]
    assert officer.agent.deck and not officer.agent.released
    assert [e.kind for e in world.log if e.kind == "reckoning.fix"]
    if replay_mod.same_build(header["build"]):
        assert report.words == [] and world.played_under == [header["build"]]
    else:
        assert report.words[0].startswith(
            "The checkpoint was written by another build (m5c-c/37d, rules "
        )
        assert world.played_under == [header["build"], replay_mod.build_stamp()]


def test_the_packages_own_save_loads_from_its_checkpoint_and_runs_on_a_watch(tmp_path):
    world, _ = _loaded_run_saved_and_loaded_again(_the_37d_save(), A_WATCH, tmp_path)
    assert world.clock.tick == THE_37D_TICK + A_WATCH
    # the stand-by ran out at eight bells and the officer was sampled again
    assert [e for e in world.log if e.kind == "agent.resumed" and e.tick > THE_37D_TICK]


def test_the_packages_own_save_replays_only_under_the_build_that_made_it(tmp_path):
    """Item 2 on the third save: without its checkpoint, it replays under the build that
    wrote it to the digest its checkpoint holds (the officer seated at tick 0 after the
    opening line, item 3), and under any other build it is refused without the flag."""
    save = _the_37d_save()
    alone = tmp_path / "alone.json"
    alone.write_bytes(save.read_bytes())
    header = _header(save)
    if replay_mod.same_build(header["build"]):
        world, report = replay_mod.load_report(alone, ship_factory)
        assert report.how == "replay" and world.log.digest() == header["digest"]
    else:
        with pytest.raises(replay_mod.ReplayRefused) as refused:
            replay_mod.load(alone, ship_factory)
        assert "m5c-c/37d, rules " in refused.value.report.words[1]
        assert "the officer of the watch's transcript" in refused.value.report.words[3]


# ---------------------------------------------------------------------------
# Package 37g: what an older save with a station in it does under this build's rules
# ---------------------------------------------------------------------------


def test_an_older_save_with_a_station_held_plays_on_under_this_builds_rules(tmp_path):
    """The save of 37d's own making holds the officer at his station, with the deck, a
    word of the captain's for a fix, and a stand-by until eight bells. Loaded from its
    checkpoint under this build: every field this build added reads as its plain default;
    the captain's word of the older build (kept one to an order, "for the watch") is a
    grant by name and stands; the domain and the turn's budget are this build's; `I have
    the deck` takes the deck and leaves him seated; and the game runs on, is saved and is
    loaded again with all of it."""
    from freesail.agents import harness as harness_mod
    from freesail.agents import tools

    world, _ = replay_mod.load_report(_the_37d_save(), ship_factory)
    name = "officer of the watch"
    h = world.agents[name]
    a = h.agent
    assert not a.released and a.has_deck and a.standing_by
    assert (a.grants, a.general, a.general_words, a.deck_lost, a.leavings, a.relieved) == (
        (),
        False,
        "",
        "",
        (),
        "",
    )
    assert a.stand_by.bound is None  # a wait taken under the older rule has no bound added
    assert a.allowances == {"take a fix": ""}  # as the older build kept the captain's word
    assert [g.said() for g in h.grants()] == ["take a fix"] and a.allowances == {}
    assert world.submit("the officer of the watch").text == (
        "The officer of the watch: Mr Pearce, first lieutenant, has the deck since Morning "
        "watch, 8 bells (04:00); may also take a fix."
    )
    # the domain is this build's, whatever the checkpoint's copy of the station holds: a
    # fix is the officer's own now, and the course is still the captain's
    assert "take a fix" not in h.station.domain.verbs and "take a fix" in h.domain.verbs
    assert tools.judge(world, name, "take a fix")[1:] == ("", tools.DOMAIN)
    assert tools.judge(world, name, "steer N")[1].endswith(tools.DANGER_ROUTE)
    assert h.orders_per_turn == harness_mod.TOOL_CALLS_PER_SAMPLE == 16
    # the deck goes to and fro, and he stays
    e = world.submit("I have the deck")
    assert e.text == (
        "The captain has the deck. The officer of the watch stays at the station, off watch."
    )
    assert not a.released and not a.has_deck and [g.said() for g in h.grants()] == ["take a fix"]
    assert world.submit("you have the deck").kind == "agent.deck" and a.has_deck
    assert world.submit("you may work the ship").kind == "agent.deck" and a.general
    # no leaving is on its record, so the one rule seats whoever asks once it is released
    assert harness_mod.seating(world, name, "").ok
    world.run(A_GLASS)
    again = replay_mod.save_to_file(world, tmp_path / "on.json")
    copy, report = replay_mod.load_report(again, ship_factory)
    assert report.how == "checkpoint" and copy.log.digest() == world.log.digest()
    b = copy.agents[name].agent
    assert b.general and [g.said() for g in copy.agents[name].grants()] == ["take a fix"]


@pytest.mark.parametrize("name", sorted(PLAYTEST_SAVES))
def test_a_station_left_in_a_playtest_save_is_taken_again_by_the_one_rule(name, tmp_path):
    """The two playtest saves hold an officer who handed over the deck under the older
    rule, which stood the station down with it. Under this build that is a stand-down:
    the same model or another may take the station (its consent is the door's to look up),
    no question is owed for the leaving, and what the captain's word allowed lapsed when
    the station was left, so the officer who sits again starts from the domain."""
    from freesail.agents import Fake
    from freesail.agents import harness as harness_mod

    world, _ = replay_mod.load_report(_playtest_save(name), ship_factory)
    station = PLAYTEST_SAVES[name][1]
    h = world.agents[station]
    a = h.agent
    who = h.model_name
    assert a.released and who and a.leavings == ()
    assert "the deck handed over" in a.released_reason
    for identity in (who, "another-made-up-model"):
        decided = harness_mod.seating(world, station, identity)
        assert decided.ok and not decided.ask_again and not decided.why
    assert harness_mod.barred(world, who) is None
    assert a.allowances  # the older build's, which lapse at the leaving
    seatings = a.seatings
    h.reseat(Fake(["Aye."]), identity=who, door="mcp", save=lambda w, why: None)
    assert not a.released and a.seatings == seatings + 1 and not a.has_deck
    assert h.grants() == () and a.allowances == {} and not a.general
    stationed = [e.text for e in world.log if e.kind == "agent.stationed"][-1]
    assert stationed.startswith(f"The {station} takes the station again ({who}, through ")
    assert "the deck handed over" in stationed
    # the brief of the station taken again is this build's, with the last note in it
    brief = h.brief.text()
    assert "stand_down" in brief and "The last handover note in this station's journal" in brief
    world.run(A_GLASS)
    again = replay_mod.save_to_file(world, tmp_path / "on.json")
    copy, report = replay_mod.load_report(again, ship_factory)
    assert report.how == "checkpoint" and copy.log.digest() == world.log.digest()
