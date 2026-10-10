from freesail.core import replay
from freesail.core.world import BUILD_NAME, Scenario, World


def make_world() -> World:
    w = World(seed=99, scenario=Scenario(gustiness=1.0, variability=1.0))
    w.submit("steer north-east")
    w.run(300)
    w.submit("speed 7 knots")
    w.submit("steer 200")
    w.run(2000)
    w.submit("stop")  # an order at the final tick must also replay
    return w


def test_replay_reproduces_log_exactly():
    original = make_world()
    copy = replay.replay_world(original)
    assert copy.clock.tick == original.clock.tick
    assert copy.journal == original.journal
    assert copy.log.digest() == original.log.digest()
    assert copy.state() == original.state()


def test_save_round_trips_through_a_file(tmp_path):
    original = make_world()
    path = replay.save_to_file(original, tmp_path / "voyage.json")
    data = replay.load_file(path)
    assert data["end_tick"] == original.clock.tick
    copy = replay.replay(data)
    assert copy.log.digest() == original.log.digest()


def test_partial_replay_stops_early():
    original = make_world()
    copy = replay.replay(original.save(), until_tick=100)
    assert copy.clock.tick == 100
    assert copy.journal == [(0, "captain", "steer north-east")]


def test_bad_format_is_rejected(tmp_path):
    p = tmp_path / "x.json"
    p.write_text('{"format": 999}')
    try:
        replay.load_file(p)
    except ValueError as e:
        assert "format" in str(e)
    else:
        raise AssertionError("expected ValueError")


# ---------------------------------------------------------------------------
# A crewed voyage (spec M3 §2.4): the muster is rebuilt from the seed on replay
# ---------------------------------------------------------------------------

FRIGATE = "data/ships/frigate-36.yaml"


def crewed_voyage() -> World:
    """The frigate from rest at twenty to eight: plain sail, all hands and a tack, piped
    down, and the watch changed at eight bells."""
    from datetime import datetime

    from freesail.api.session import make_world

    scenario = Scenario(
        start_time=datetime(1805, 6, 1, 7, 40),
        wind_from_deg=0.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=293.0,
    )
    w = make_world(7, FRIGATE, scenario)
    w.submit("set plain sail")
    w.submit("brace sharp up on the starboard tack")
    w.run(600)
    w.submit("trim sails")
    w.run(300)
    w.submit("call all hands")
    w.submit("tack ship")
    w.run(600)
    w.submit("pipe down")
    w.run(120)
    return w


STARTER = "data/standing_orders/starter.orders"


def standing_voyage() -> World:
    """Truth 39 (spec M4 §8): the frigate before the wind under all sail, studding sails
    both sides, from 19:30 on 1 June under the starter routines (spec §6; the well's
    is refused at load and not journaled) and an `every` order, through sunset (19:59,
    when the night routine fires) to 20:20, `keep her full` belayed on the way. The
    firings are not journaled; only the orders that gave them are."""
    from datetime import datetime

    from freesail.api.session import make_world
    from freesail.standing.book import read_orders_file

    scenario = Scenario(
        start_time=datetime(1805, 6, 1, 19, 30),
        wind_from_deg=0.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=180.0,
    )
    w = make_world(7, FRIGATE, scenario)
    w.submit("make all sail")
    w.run(600)
    w.submit("rig out the studdingsails, both sides")
    w.run(300)
    w.submit("set the studdingsails, both sides")
    for text in read_orders_file(STARTER):
        # the well's line was refused at load (spec §6) until package 33c, which holds it
        # in the book instead; the voyage loads the others, as it always has.
        if "sound the well" not in text:
            w.submit(text)
    w.submit('standing order "trim": every 10 minutes then trim sails')
    w.run(1500)
    w.submit('belay standing order "keep her full"')
    w.run(600)
    return w


def test_truth_39_a_passage_under_the_starter_routines_replays_with_the_same_firings(tmp_path):
    from freesail.api.session import ship_factory

    original = standing_voyage()
    fired = [
        (e.tick, e.actor, e.text)
        for e in original.log
        if e.kind == "order.accepted" and e.actor.startswith("standing order")
    ]
    assert [(t, a) for t, a, _ in fired] == [
        (1500, "standing order 'trim'"),
        (1742, "standing order 'night routine'"),
        (1742, "standing order 'night routine'"),
        (2100, "standing order 'trim'"),
        (2700, "standing order 'tend the sheets'"),
        (2700, "standing order 'trim'"),
    ], "trim every ten minutes from 19:45; the night routine at sunset, 19:59; the sheets at 20:15"
    assert [e.tick for e in original.log if e.kind == "sun.set"] == [1742]
    assert all(not a.startswith("standing order") for _, a, _ in original.journal)
    assert sum(1 for _, _, t in original.journal if t.startswith("standing order")) == 8
    assert "order.rejected" not in {e.kind for e in original.log}
    path = replay.save_to_file(original, tmp_path / "standing.json")
    data = replay.load_file(path)
    assert [r["name"] for r in data["standing_orders"]] == [
        "night routine",
        "morning sail",
        "shorten sail for weather",
        "keep her full",
        "trim on a shift",
        "tend the sheets",
        "heavy weather",  # package 37p: it sets the storm staysails itself
        "trim",
    ]
    assert data["scenario"]["latitude_deg"] == 50.0
    copy = replay.replay(data, ship_factory)
    assert copy.log.digest() == original.log.digest()
    assert [
        (e.tick, e.actor, e.text)
        for e in copy.log
        if e.kind == "order.accepted" and e.actor.startswith("standing order")
    ] == fired
    assert copy.standing.book.save() == data["standing_orders"]
    assert copy.standing.book.get("keep her full").belayed


def test_a_crewed_voyage_replays_to_the_same_log_and_the_same_muster(tmp_path):
    from freesail.api.session import ship_factory

    original = crewed_voyage()
    kinds = [e.kind for e in original.log]
    for kind in ("crew.all_hands", "ship.tacked", "crew.piped_down", "watch.relieved"):
        assert kind in kinds, kind
    assert "order.rejected" not in kinds
    path = replay.save_to_file(original, tmp_path / "crewed.json")
    copy = replay.replay(replay.load_file(path), ship_factory)
    assert copy.log.digest() == original.log.digest()
    assert copy.ship.extra["crew"].describe(copy.clock) == original.ship.extra["crew"].describe(
        original.clock
    )
    assert [s.fatigue for s in copy.ship.extra["crew"].sailors] == [
        s.fatigue for s in original.ship.extra["crew"].sailors
    ]


# ---------------------------------------------------------------------------
# Package 37d, part one: the build's stamp, the load's rule and its words, a station
# seated at tick 0 in its place (the review of gate 5c's playtests, section 6 under "The
# cost CHANGES does not state" and section 9 under "Replay")
# ---------------------------------------------------------------------------


def _watched_game(ticks: int = 600) -> World:
    """A short game with the scripted watcher at its station: a save with a station's
    transcript in it."""
    from freesail.api.session import make_world
    from freesail.ui.console import station_watcher

    w = make_world(7, FRIGATE, Scenario(wind_from_deg=0.0, gustiness=0.0, variability=0.0))
    station_watcher(w, "fake", out=None)
    w.submit("set the topsails")
    w.run(ticks)
    return w


def _restamp(path, stamp, checkpoint: bool = False, before_42: bool = False) -> None:
    """Rewrite a save's stamp (None: unstamped), and its checkpoint's header's when asked,
    as another build would have written them; `before_42`, as a build from before package
    42 wrote it, with its stations' acts in no list."""
    import gzip
    import json

    data = json.loads(path.read_text())
    if before_42:
        data.pop("station_acts", None)
        for record in data.get("agents") or []:
            record.pop("acts", None)
    data.pop("build", None)
    if stamp is not None:
        data["build"] = stamp
    path.write_text(json.dumps(data))
    if checkpoint:
        cp = replay.checkpoint_path(path)
        with gzip.open(cp, "rb") as f:
            header = json.loads(f.readline().decode("utf-8"))
            body = f.read()
        header.pop("build", None)
        if stamp is not None:
            header["build"] = stamp
        with gzip.open(cp, "wb") as f:
            f.write(json.dumps(header).encode("utf-8") + b"\n")
            f.write(body)


OTHER_BUILD = {"name": "m5c-c/another", "rules": "0123456789abcdef"}


def test_a_save_and_its_checkpoint_carry_the_builds_stamp(tmp_path):
    """Item 1: `"build": {"name", "rules"}` in the save and in the checkpoint's header,
    the name set by hand and the rules the first sixteen hex digits of a SHA-256; the
    save's format and the engine's version do not move."""
    import gzip
    import json

    from freesail.core import world as world_mod

    original = make_world()
    data = original.save()
    stamp = data["build"]
    assert stamp == world_mod.build_stamp() == replay.stamp_of(data)
    assert stamp["name"] == world_mod.BUILD_NAME == "m6a"
    assert len(stamp["rules"]) == 16 and int(stamp["rules"], 16) >= 0
    assert data["format"] == world_mod.SAVE_FORMAT == 1
    assert data["engine"] == world_mod.ENGINE_VERSION == "0.0.1"
    path = replay.save_to_file(original, tmp_path / "voyage.json")
    with gzip.open(replay.checkpoint_path(path), "rb") as f:
        header = json.loads(f.readline().decode("utf-8"))
    assert header["build"] == stamp and header["format"] == replay.CHECKPOINT_FORMAT
    assert replay.same_build(stamp) and not replay.same_build(None)
    assert not replay.same_build(OTHER_BUILD)
    # a save from before the stamp reads as unstamped
    assert replay.stamp_of({"format": 1}) is None
    assert world_mod.build_words(None) == "unstamped, before 37d"
    assert world_mod.build_words(stamp) == f"{world_mod.BUILD_NAME}, rules {stamp['rules']}"


def test_the_fingerprint_is_of_the_code_and_the_data_and_not_of_the_line_endings(tmp_path):
    """Item 1's set: every `freesail/**/*.py` and every data file but the chart's tiles, in
    path order, CR LF made LF; nothing of the caches. Worked once a process and well
    under a tenth of a second (measured: three hundredths on the owner's machine)."""
    import time

    from freesail.core import world as world_mod

    root = tmp_path / "tree"
    (root / "freesail" / "core").mkdir(parents=True)
    (root / "freesail" / "__pycache__").mkdir()
    (root / "data" / "charts" / "tiles" / "3").mkdir(parents=True)
    (root / "freesail" / "core" / "a.py").write_bytes(b"x = 1\ny = 2\n")
    (root / "freesail" / "b.py").write_bytes(b"z = 3\n")
    (root / "data" / "v.yaml").write_bytes(b"verbs:\n  haul: 1\n")
    (root / "data" / "charts" / "manifest.yaml").write_bytes(b"tiles: [t]\n")
    (root / "data" / "charts" / "tiles" / "3" / "t.npz").write_bytes(b"\x00\x01")
    first = world_mod.fingerprint_of(root)
    assert len(first) == 16
    # a Windows checkout: the same files with CR LF
    (root / "freesail" / "core" / "a.py").write_bytes(b"x = 1\r\ny = 2\r\n")
    (root / "data" / "v.yaml").write_bytes(b"verbs:\r\n  haul: 1\r\n")
    assert world_mod.fingerprint_of(root) == first
    # the tiles and the caches are not in it
    (root / "data" / "charts" / "tiles" / "3" / "t.npz").write_bytes(b"\x02\x03")
    (root / "freesail" / "__pycache__" / "a.py").write_bytes(b"cached = 1\n")
    (root / "freesail" / "notes.txt").write_bytes(b"not code\n")
    assert world_mod.fingerprint_of(root) == first
    # a rule changed, a data file changed, a file moved: each another fingerprint
    (root / "freesail" / "b.py").write_bytes(b"z = 4\n")
    second = world_mod.fingerprint_of(root)
    assert second != first
    (root / "data" / "charts" / "manifest.yaml").write_bytes(b"tiles: [u]\n")
    third = world_mod.fingerprint_of(root)
    assert third not in (first, second)
    (root / "freesail" / "b.py").rename(root / "freesail" / "c.py")
    assert world_mod.fingerprint_of(root) not in (first, second, third)
    # this tree's own, timed afresh
    kept = world_mod.rules_fingerprint()
    world_mod._BUILD_RULES = None
    t0 = time.perf_counter()
    assert world_mod.rules_fingerprint() == kept
    assert time.perf_counter() - t0 < 0.5


def test_load_says_which_road_it_took_and_why_a_checkpoint_was_not_taken(tmp_path, monkeypatch):
    """Item 2: none beside the save; not this save's; could not be read, with the error's
    words, an import error among them (it escaped `load` before). A save of this build
    replays as it always did."""
    import json

    from freesail.api.session import ship_factory

    original = _watched_game()
    digest = original.log.digest()
    path = replay.save_to_file(original, tmp_path / "game.json")
    world, report = replay.load_report(path, ship_factory)
    assert report.how == "checkpoint" and report.checkpoint == "" and report.words == []
    assert report.same_build and world.log.digest() == digest
    assert report.transcripts == {"watcher": len(original.agents["watcher"].transcript)}
    # none beside the save
    alone = replay.save_to_file(original, tmp_path / "alone.json", checkpoint=False)
    world, report = replay.load_report(alone, ship_factory)
    assert report.how == "replay" and report.checkpoint == replay.NO_CHECKPOINT
    assert world.log.digest() == digest
    assert report.words == [
        "Replayed from its journal: there is no checkpoint beside the save. The save is "
        f"this build's ({BUILD_NAME}, rules {original.save()['build']['rules']})."
    ]
    # not this save's
    other = tmp_path / "other.json"
    data = replay.load_file(path)
    data["end_tick"] = 300
    data["inputs"] = [e for e in data["inputs"] if e["tick"] <= 300]
    data["journal"] = [e for e in data["journal"] if e[0] <= 300]
    for record in data["agents"]:
        record["transcript"] = [e for e in record["transcript"] if e["tick"] <= 300]
    other.write_text(json.dumps(data))
    replay.checkpoint_path(other).write_bytes(replay.checkpoint_path(path).read_bytes())
    world, report = replay.load_report(other, ship_factory)
    assert report.how == "replay" and world.clock.tick == 300
    assert report.checkpoint.startswith(replay.NOT_THIS_SAVES + " (it was written at tick 600")
    # could not be read: a spoiled file
    bad = replay.save_to_file(original, tmp_path / "bad.json", checkpoint=False)
    replay.checkpoint_path(bad).write_bytes(b"not a checkpoint")
    world, report = replay.load_report(bad, ship_factory)
    assert report.how == "replay" and world.log.digest() == digest
    assert report.checkpoint.startswith(replay.COULD_NOT_BE_READ + " (BadGzipFile: ")
    # could not be read: a class this build no longer has (an import error escaped before)
    gone = replay.save_to_file(original, tmp_path / "gone.json")

    def no_such_module(_path):
        raise ModuleNotFoundError("No module named 'freesail.world.gone'")

    monkeypatch.setattr(replay, "read_checkpoint", no_such_module)
    world, how = replay.load(gone, ship_factory)
    assert how == "replay" and world.log.digest() == digest
    _, report = replay.load_report(gone, ship_factory)
    assert report.checkpoint == (
        "the checkpoint beside it could not be read (ModuleNotFoundError: No module named "
        "'freesail.world.gone')"
    )


def test_another_builds_game_with_a_station_aboard_is_not_replayed_unless_asked(tmp_path):
    """Item 2's rule. Another build's save, or an unstamped one: with no station's
    transcript it replays and the words say the log may differ; with one it is refused in
    plain words (the build that wrote it, this build, why the checkpoint was not used,
    that a replay would not be the game that was played) unless `replay_anyway`. Loaded
    from another build's checkpoint, one line says which build wrote it."""
    import pytest

    from freesail.api.session import ship_factory

    here = replay.build_stamp()["rules"]
    # no station aboard: replayed, with the warning
    plain = replay.save_to_file(make_world(), tmp_path / "plain.json", checkpoint=False)
    _restamp(plain, OTHER_BUILD)
    world, report = replay.load_report(plain)
    assert report.how == "replay" and not report.same_build and report.transcripts == {}
    assert report.words == [
        "The save was written by another build (m5c-c/another, rules 0123456789abcdef); "
        f"this is {BUILD_NAME}, rules {here}.",
        "It was replayed from its journal under this build's rules, since there is no "
        "checkpoint beside the save: the log may differ from the one that was watched.",
    ]
    # a station aboard: refused, for another build's stamp and for none
    original = _watched_game()
    n = len(original.agents["watcher"].transcript)
    for stamp, wrote in ((OTHER_BUILD, "m5c-c/another, rules 0123456789abcdef"), (None, None)):
        path = replay.save_to_file(original, tmp_path / "game.json", checkpoint=False)
        _restamp(path, stamp, before_42=True)
        with pytest.raises(replay.ReplayRefused) as refused:
            replay.load(path, ship_factory)
        report = refused.value.report
        assert report.how == "refused" and report.transcripts == {"watcher": n}
        assert report.words == [
            f"Not replayed: {path}.",
            f"The save was written by another build ({wrote or 'unstamped, before 37d'}); "
            f"this is {BUILD_NAME}, rules {here}.",
            "Its checkpoint was not used: there is no checkpoint beside the save.",
            f"It holds the watcher's transcript ({n} replies), and a replay under this "
            "build's rules would not be the game that was played: a station's orders are "
            "not in the journal, and its recorded replies are handed back wherever today's "
            "rules open a sample (a save from before package 42, whose stations' acts are not "
            "inputs).",
            "Load it under the build that wrote it, or with its checkpoint beside it (a "
            "save is exact from its checkpoint); to replay it all the same, say "
            "--replay-anyway.",
        ]
        assert str(refused.value) == " ".join(report.words)
        # asked for: replayed, and the words say what it is
        world, report = replay.load_report(path, ship_factory, replay_anyway=True)
        assert report.how == "replay" and report.anyway
        assert world.clock.tick == original.clock.tick
        assert report.words[1] == (
            "Replayed all the same, as asked (--replay-anyway), since there is no "
            "checkpoint beside the save."
        )
        assert report.words[2].endswith("Read its log as another game from the same beginning.")
    # its checkpoint beside it: loaded from it, with the one line naming the build
    path = replay.save_to_file(original, tmp_path / "with.json")
    _restamp(path, OTHER_BUILD, checkpoint=True)
    world, report = replay.load_report(path, ship_factory)
    assert report.how == "checkpoint" and world.log.digest() == original.log.digest()
    assert report.words == [
        "The checkpoint was written by another build (m5c-c/another, rules "
        f"0123456789abcdef) and is read by this one ({BUILD_NAME}, rules {here}): the game "
        "goes on from where it was saved, under this build's rules."
    ]


def test_every_door_that_loads_or_replays_says_the_same_words_and_takes_the_flag(tmp_path, capsys):
    """Item 2's doors: the server's and the console's `--load` (one function,
    `console.start_world`, and one set of words, `console.loaded_words`), the console's
    `replay`, and the REPL door's `--load`, which always replays; each refuses another
    build's game with a station aboard in the load's words and takes `--replay-anyway`."""
    import argparse
    import io

    import pytest

    from freesail.agents import repl as repl_mod
    from freesail.ui.console import Console, loaded_words, start_world

    original = _watched_game(300)
    path = replay.save_to_file(original, tmp_path / "game.json", checkpoint=False)
    _restamp(path, None, before_42=True)
    refusal = "Not replayed: " + str(path)

    def args(anyway: bool) -> argparse.Namespace:
        return argparse.Namespace(
            load=str(path),
            scenario=None,
            wind=None,
            heading=None,
            seed=None,
            ship=None,
            replay_anyway=anyway,
        )

    # the server's and the console's --load
    with pytest.raises(SystemExit) as stopped:
        start_world(args(False))
    assert str(stopped.value).startswith(refusal) and "--replay-anyway" in str(stopped.value)
    world, _ = start_world(args(True))
    said = loaded_words(world, str(path))
    assert said[0].startswith(f"Loaded {path}: replayed to tick 300, ")
    assert said[1].startswith("The save was written by another build (unstamped, before 37d)")
    assert said[2].startswith("Replayed all the same, as asked (--replay-anyway)")
    # the console's `replay`
    out = io.StringIO()
    console = Console(World(seed=3), out=out)
    console.handle_line(f"replay {path}")
    assert refusal in out.getvalue() and console.world.seed == 3
    console.handle_line(f"replay {path} --replay-anyway")
    assert console.world.seed == 7 and console.world.clock.tick == 300
    assert "Replayed all the same, as asked (--replay-anyway)" in out.getvalue()
    # the REPL door's --load
    common = [FRIGATE, "--seed", "7", "--station", "watcher", "--turn", "--human"]
    common += ["--save", str(tmp_path / "state.json"), "--sample", str(tmp_path / "next.txt")]
    with pytest.raises(SystemExit) as stopped:
        repl_mod.main(common + ["--load", str(path)])
    assert str(stopped.value).startswith(refusal)
    assert repl_mod.main(
        common + ["--load", str(path), "--replay-anyway", "--max-ticks", "60"]
    ) in (
        0,
        3,
    )
    assert "Replayed all the same, as asked (--replay-anyway)" in capsys.readouterr().err
    # a save of this build is loaded by every door without a word of refusal
    mine = replay.save_to_file(original, tmp_path / "mine.json")
    ns = args(False)
    ns.load = str(mine)
    world, _ = start_world(ns)
    assert loaded_words(world, str(mine)) == [
        f"Loaded {mine}: from its checkpoint at tick 300, {world.clock.stamp()}; the log's "
        f"digest is {original.log.digest()[:16]}."
    ]


def test_an_officer_seated_at_tick_0_after_a_drivers_line_replays_in_his_place():
    """Item 3: a replay seats a station by its tick and the count of inputs before it
    (`stationed_after_inputs`); a driver's line is an input and no order, so the count of
    journaled orders alone seated an officer who came after the game's opening line
    before it, the same lines in another order and so another digest (the Amazon's save
    of m5c). A save without the count replays as it did."""
    import json

    from freesail.agents import Harness, SamplingPolicy
    from freesail.agents.agent import officer
    from freesail.agents.fake import officer_of_the_watch
    from freesail.api.session import make_world, ship_factory

    world = make_world(7, FRIGATE, Scenario(wind_from_deg=0.0, gustiness=0.0, variability=0.0))
    # the game's opening line, as the server writes it before any door is opened
    world.record_driver("routine", "driver.book", "The book of standing orders begins empty.")
    h = Harness(
        world,
        officer(SamplingPolicy.in_lockstep(600, "notable", "urgent"), world=world),
        officer_of_the_watch(),
        save=lambda w, why: None,
    )
    h.start()
    assert h.agent.stationed_tick == 0
    world.submit("you have the deck")
    world.submit("set the topsails")
    world.run(1500)
    data = json.loads(json.dumps(world.save()))
    record = data["agents"][0]
    assert record["stationed_after_inputs"] == 1 and record["stationed_after_orders"] == 0
    copy = replay.replay(data, ship_factory)
    assert copy.log.digest() == world.log.digest()
    assert [e.kind for e in copy.log][:4] == [e.kind for e in world.log][:4]
    # a save from before the count: seated before the opening line, as it was
    del record["stationed_after_inputs"]
    old = replay.replay(data, ship_factory)
    assert len(old.log) == len(world.log) and old.log.digest() != world.log.digest()
    assert sorted(e.text for e in old.log) == sorted(e.text for e in world.log)


# ---------------------------------------------------------------------------
# Package 37i, item 5: the line the replay dropped at a stand-down by the door (the
# review of gate 5c, G14 and the audit's C7: game 10's last save replayed to 4,239 lines
# for 4,240, the line missing at 08:00 on the 14th, "A notable event that speaks of
# danger: The Nut Rock ...; the officer of the watch is sampled again")
# ---------------------------------------------------------------------------


def _stood_down_by_the_door(driver_line: bool = False) -> World:
    """A fake of game 10's moment: the officer stands by; at the bell a standing order
    fires an order inside the World's tick and the harness's own step, at the end of the
    same tick, wakes him; the door (the runner, its server refusing) stands him down
    between that tick and the next, after a driver's line when `driver_line`."""
    from freesail.agents import Harness, SamplingPolicy
    from freesail.agents.agent import officer
    from freesail.agents.model import Reply, ToolCall
    from freesail.agents.remote import RemoteModel
    from freesail.api.session import make_world

    world = make_world(7, FRIGATE, Scenario(wind_from_deg=0.0, gustiness=0.0, variability=0.0))
    world.submit('standing order "the topsails": every glass then set the topsails')
    h = Harness(
        world,
        officer(SamplingPolicy.in_lockstep(1800, "notable", "urgent"), world=world),
        RemoteModel(),  # a door that answers late, between ticks, as the runner does
        save=lambda w, why: None,
    )
    h.start()
    h.deliver(Reply("", (ToolCall("stand_by", {"until": "one bell"}),)))
    assert h.agent.standing_by
    while h.open_sample is None:
        world.tick()
    if driver_line:
        world.record_driver("routine", "driver.compression", "The compression eased.")
    h.door_act("stand_down", "the model server could not be used", "the local runner")
    return world


def test_a_stand_down_by_the_door_replays_with_every_line_in_its_place():
    """The fault, found on a fake of the save (game 10's own saves are not in the
    review's evidence): a door's act is made between ticks, but a replay made it at the
    first order of its tick and of the count of orders before it, which a standing
    order's firing gives inside the World's tick, before the harness's own step has
    woken the station. So the stand-down came first, the station was released before
    its waking was written, and the log was one line short. A replay now makes an act of
    the tick it is at only between ticks, after as many inputs as were given before it."""
    import json

    from freesail.api.session import ship_factory

    world = _stood_down_by_the_door()
    kinds = [e.kind for e in world.log if e.tick == world.clock.tick]
    assert kinds[-3:] == ["order.accepted", "agent.resumed", "agent.stopped"]
    data = json.loads(json.dumps(world.save()))
    copy = replay.replay(data, ship_factory)
    assert len(copy.log) == len(world.log)  # 4,239 for 4,240 in game 10
    assert copy.log.digest() == world.log.digest()
    name = "officer of the watch"
    assert copy.agent_journals[name].save() == world.agent_journals[name].save()
    # a driver's line between the waking and the act (an input, and no order): the act is
    # recorded after it and made after it
    world = _stood_down_by_the_door(driver_line=True)
    data = json.loads(json.dumps(world.save()))
    act = data["agents"][0]["transcript"][-1]
    assert act["door"] == "stand_down" and act["after_inputs"] == len(world.inputs)
    copy = replay.replay(data, ship_factory)
    assert copy.log.digest() == world.log.digest()
    # a save from before the count (game 10's): every line is there, the line and the act
    # in another order
    del act["after_inputs"]
    old = replay.replay(data, ship_factory)
    assert len(old.log) == len(world.log)
    assert sorted(e.text for e in old.log) == sorted(e.text for e in world.log)


# ---------------------------------------------------------------------------
# Package 42, item 3 (spec M6 §14): the stations' acts as inputs, the replay driven by
# them and not by the transcript, on a build whose sampling differs
# ---------------------------------------------------------------------------


def three_stations(ticks: int = 1800) -> World:
    """The captain's, the officer's and the watcher's stations seated at once, each a fake
    in lockstep: the captain gives the deck, his general authority and an order, and stands
    by; the officer takes the deck and keeps it; the watcher narrates and answers."""
    from freesail.agents import Harness, SamplingPolicy
    from freesail.agents.agent import captain, officer, watcher
    from freesail.agents.fake import captain_of_the_ship, narrator, officer_of_the_watch
    from freesail.api.session import make_world as make

    world = make(
        7, FRIGATE, Scenario(wind_from_deg=0.0, wind_speed_kn=22, gustiness=0.0, variability=0.0)
    )
    world.record_driver("routine", "driver.book", "The book of standing orders begins empty.")
    every = SamplingPolicy.in_lockstep(600, "notable", "urgent")
    orders = ["you have the deck", "you may work the ship", "set the royals"]
    for station, model in (
        (captain(every, world=world), captain_of_the_ship(orders)),
        (officer(every, world=world), officer_of_the_watch()),
        (watcher(every, world=world), narrator()),
    ):
        Harness(world, station, model, save=lambda w, why: None).start()
    world.submit("set the topsails")
    world.run(ticks)
    world.submit("ask the watcher how the sails are drawing")
    world.run(ticks)
    return world


def sampled_every_other_glass(monkeypatch) -> None:
    """A build whose sampling differs: a station is sampled at every other turn of its
    interval and no more (its events as before)."""
    from freesail.agents import harness as harness_mod

    before = harness_mod.Harness._policy_due

    def sparser(self, new):
        p = self.policy
        if p.every_s and self.agent.stationed_tick is not None:
            since = self.world.clock.tick - self.agent.stationed_tick
            if since > 0 and since % p.every_s == 0 and since % (2 * p.every_s):
                return None
        return before(self, new)

    monkeypatch.setattr(harness_mod.Harness, "_policy_due", sparser)


def test_a_stations_acts_are_inputs_and_both_roads_replay_to_the_same_log():
    """Every station's act is journaled at its tick after its count of inputs: its
    seating, its orders under its own actor (in no list of the player's inputs), its lines,
    its journal's entries and its state. A save of this build replays by its transcript, as
    it did, and by its acts to the same log and the same journals."""
    import json

    from freesail.api.session import ship_factory

    world = three_stations()
    kinds = {
        next(k for k in e if k not in ("tick", "after_inputs", "station"))
        for e in world.station_acts
    }
    assert kinds == {"seated", "order", "line", "note", "state"}
    orders = [e["order"] for e in world.station_acts if "order" in e]
    assert {"order": "you have the deck", "actor": "the captain"}.items() <= orders[0].items()
    assert not any(i.get("actor") == "the captain" for i in world.inputs)
    data = json.loads(json.dumps(world.save()))
    assert [a["acts"] for a in data["agents"]] == [True, True, True]
    assert replay.road_of(data) == replay.BY_TRANSCRIPT  # this build's own game
    for road in (replay.BY_TRANSCRIPT, replay.BY_ACTS):
        copy = replay.replay(data, ship_factory, road=road)
        assert copy.log.digest() == world.log.digest(), road
        for name, journal in world.agent_journals.items():
            assert copy.agent_journals[name].save() == journal.save(), (road, name)
    # by its acts the stations take up the game where it stands, its record the save's
    copy = replay.replay(data, ship_factory, road=replay.BY_ACTS)
    for name, h in copy.agents.items():
        assert not h.driven and h.transcript == world.agents[name].transcript
        assert h.agent.words() == world.agents[name].agent.words()
    assert copy.agents["officer of the watch"].agent.deck
    # and it plays on; a save of it replays again by its acts
    copy.run(600)
    again = json.loads(json.dumps(copy.save()))
    assert [a["acts"] for a in again["agents"]] == [True, True, True]
    assert replay.replay(again, ship_factory, road=replay.BY_ACTS).log.digest() == copy.log.digest()


def test_a_replay_by_its_acts_is_the_same_game_on_a_build_whose_sampling_differs(
    monkeypatch, tmp_path
):
    """Another build's save, sampled otherwise: by its transcript the recorded replies land
    elsewhere and the log is another; by its acts (the load's road for another build's save
    whose stations' acts are in it) the log is the one that was played, and the words say
    which road it took."""
    from freesail.api.session import ship_factory

    world = three_stations()
    path = replay.save_to_file(world, tmp_path / "game.json", checkpoint=False)
    _restamp(path, OTHER_BUILD)
    sampled_every_other_glass(monkeypatch)
    data = replay.load_file(path)
    by_transcript = replay.replay(data, ship_factory, road=replay.BY_TRANSCRIPT)
    assert by_transcript.log.digest() != world.log.digest()
    loaded, report = replay.load_report(path, ship_factory)
    assert report.how == "replay" and report.road == replay.BY_ACTS
    assert loaded.log.digest() == world.log.digest()
    assert report.words[1].startswith("It was replayed by its stations' acts, since there is no ")
    assert "whatever this build's sampling would ask" in report.words[1]
    # a save from before package 42 is refused as before, and says why
    _restamp(path, OTHER_BUILD, before_42=True)
    import pytest

    with pytest.raises(replay.ReplayRefused) as refused:
        replay.load_report(path, ship_factory)
    assert "a save from before package 42" in str(refused.value)
    with pytest.raises(ValueError):
        replay.replay(replay.load_file(path), ship_factory, road=replay.BY_ACTS)


def test_a_door_act_at_the_stationing_tick_is_made_by_a_replay():
    """Spec M5 §33 item 11, closed: a door's act at the tick a station was seated, before
    any tick has run (here a stand-down by the door at tick 0), is made by a replay, by
    either road, and the station is released in it as it was in play."""
    import json

    from freesail.agents import Harness, SamplingPolicy
    from freesail.agents.agent import officer
    from freesail.agents.remote import RemoteModel
    from freesail.api.session import make_world as make
    from freesail.api.session import ship_factory

    world = make(7, FRIGATE, Scenario(wind_from_deg=0.0, gustiness=0.0, variability=0.0))
    h = Harness(
        world,
        officer(SamplingPolicy.in_lockstep(600, "notable", "urgent"), world=world),
        RemoteModel(),
        save=lambda w, why: None,
    )
    h.start()
    h.door_act("stand_down", "the door closed at once", "the local runner")
    assert world.clock.tick == 0 and h.agent.released
    world.run(300)
    data = json.loads(json.dumps(world.save()))
    for road in (replay.BY_TRANSCRIPT, replay.BY_ACTS):
        copy = replay.replay(data, ship_factory, road=road)
        assert copy.log.digest() == world.log.digest(), road
        assert copy.agents["officer of the watch"].agent.released, road


def test_an_act_names_none_but_the_games_own_records():
    """The acts' state is plain JSON with the game's own small records named; an act that
    names anything else is refused, as a checkpoint's foreign class is."""
    import pytest

    from freesail.agents.agent import Grant
    from freesail.core import acts

    grant = Grant("tack ship", "if the land closes")
    assert acts.decode(acts.encode((grant,))) == (grant,)
    with pytest.raises(ValueError):
        acts.decode({"__class__": "os:system", "fields": {}})


# ---------------------------------------------------------------------------
# Package 42 on package 41's wardroom: five stations' acts, each of 41's roads by which a
# station changes the World (a say heard, a tell, a hail, a stand-by on two conditions,
# the master's figure adopted, a station unbound under a fake) replayed by the acts
# ---------------------------------------------------------------------------


def five_stations() -> World:
    """The cutter standing ESE off the Lizard at ten past eleven, an hour: the captain's,
    the officer's, the master's, the lookout's and a passenger's stations held by fakes in
    lockstep. The captain gives the deck and tells the master; the officer stands by on
    two conditions; the master works the noon and his figure is the ship's account; the
    lookout hails from the masthead; the passenger says a word on the quarterdeck, which
    the stations there hear; and at the end the passenger's station is unbound under its
    fake."""
    import datetime as dt

    from freesail.agents import Fake, Harness, Reply, SamplingPolicy, call
    from freesail.agents.agent import (
        CAPTAIN,
        LOOKOUT,
        MASTER,
        OFFICER,
        PASSENGER,
        STATION_FACTORIES,
    )
    from freesail.agents.fake import (
        captain_of_the_ship,
        master_of_the_reckoning,
        passenger_aboard,
    )
    from freesail.api.session import make_world as make

    sc = Scenario(
        start_time=dt.datetime(1805, 6, 12, 11, 10),
        wind_from_deg=270.0,
        wind_speed_kn=12.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=112.0,
        ship_speed_kn=5.0,
        position={"lat_deg": 49.75, "lon_deg": -5.45},
        region="channel-west",
    )
    world = make(7, "data/ships/cutter.yaml", sc)
    world.record_driver("routine", "driver.book", "The book of standing orders begins empty.")
    world.submit("steer ESE")
    hail = Reply(calls=(call("submit_order", text="hail sail ho, two points on the lee bow"),))
    stand_by = Reply(calls=(call("stand_by", until="eight bells, or a sail sighted"),))
    for name, model, every in (
        (
            CAPTAIN,
            captain_of_the_ship(["you have the deck", "tell the master we keep the Channel"]),
            600,
        ),
        (OFFICER, Fake([stand_by], loop=True), 600),
        (MASTER, master_of_the_reckoning(), 3600),
        (LOOKOUT, Fake([Reply(), hail], when_done=Reply()), 600),
        (PASSENGER, passenger_aboard(["a fine morning for it"]), 600),
    ):
        st = STATION_FACTORIES[name](
            SamplingPolicy.in_lockstep(every, "notable", "urgent"), world=world
        )
        h = Harness(world, st, model, save=lambda w, why: None)
        h.model_name, h.door = f"the fake {name}", "runner"
        h.start()
    world.run(3600)
    world.stations.unbind(PASSENGER, "landed at Falmouth")
    world.run(60)
    return world


def test_five_stations_of_the_wardroom_replay_by_their_acts_on_a_build_whose_sampling_differs(
    monkeypatch, tmp_path
):
    """Each of package 41's roads by which a station changes the World is an act or an
    input: a say heard on the quarterdeck (the line, and the hearers' state), a tell from
    the captain's station to the master (an order), a hail from the masthead (a line), a
    stand-by on two conditions (the state), the master's figure adopted at noon (an order,
    the working's notice an act of its own), a station unbound under its fake (an input,
    the stand-down inside it the station's acts). Both roads give the log that was played
    and its journals; stamped as another build's and sampled at every other glass, the
    acts' road gives it still."""
    import json

    from freesail.api.session import ship_factory

    world = five_stations()
    kinds = {e.kind for e in world.log}
    assert {"agent.hail", "agent.spoke", "agent.stood_by", "agent.stopped"} <= kinds
    adopted = [e for e in world.log if e.kind == "reckoning.own" and e.data.get("adopted")]
    assert adopted, "the master's figure was not adopted"
    assert any(e.data.get("heard_by") for e in world.log if e.kind == "agent.spoke")
    assert any("binding" in i for i in world.inputs)
    officer = world.agents["officer of the watch"]
    assert officer.agent.stand_by is not None and officer.agent.stand_by.others
    assert any("working_told" in e for e in world.station_acts)
    told = [e["order"]["order"] for e in world.station_acts if "order" in e]
    assert "tell the master we keep the Channel" in told
    assert any(t.startswith("my reckoning is") for t in told)  # the master's figure
    assert world.agents["passenger"].agent.released
    data = json.loads(json.dumps(world.save()))
    assert all(a["acts"] for a in data["agents"]) and len(data["agents"]) == 5
    for road in (replay.BY_TRANSCRIPT, replay.BY_ACTS):
        copy = replay.replay(data, ship_factory, road=road)
        assert copy.log.digest() == world.log.digest(), road
        for name, journal in world.agent_journals.items():
            assert copy.agent_journals[name].save() == journal.save(), (road, name)
        assert copy.stations.names() == world.stations.names(), road
    path = replay.save_to_file(world, tmp_path / "five.json", checkpoint=False)
    _restamp(path, OTHER_BUILD)
    sampled_every_other_glass(monkeypatch)
    loaded, report = replay.load_report(path, ship_factory)
    assert report.road == replay.BY_ACTS
    assert loaded.log.digest() == world.log.digest()
    other = replay.replay(replay.load_file(path), ship_factory, road=replay.BY_TRANSCRIPT)
    assert other.log.digest() != world.log.digest()


def test_the_players_seat_hears_a_stations_say_and_a_replay_by_the_acts_hears_it_too():
    """The player's seat at the master's station hears the officer's say on the
    quarterdeck: the seat's state and its journal change inside the officer's act, so the
    seat's state is journaled with the acts (`seat_state`), and a replay by them gives the
    seat what it heard and the journal its line."""
    import json

    from freesail.agents import Fake, Harness, Reply, SamplingPolicy, call
    from freesail.agents.agent import OFFICER, officer
    from freesail.agents.seat import seat_player
    from freesail.api.session import make_world as make
    from freesail.api.session import ship_factory

    world = make(7, "data/ships/cutter.yaml", Scenario(gustiness=0.0, variability=0.0))
    seat = seat_player(world, "master", door="console")
    say = Reply(calls=(call("submit_order", text="say the glass is falling"),))
    h = Harness(
        world,
        officer(SamplingPolicy.in_lockstep(600, "notable", "urgent"), world=world),
        Fake([say], when_done=Reply()),
        save=lambda w, why: None,
    )
    h.start()
    world.run(700)
    assert seat.agent.heard and "the glass is falling" in seat.agent.heard[0]
    assert any("seat_state" in e for e in world.station_acts)
    data = json.loads(json.dumps(world.save()))
    for road in (replay.BY_TRANSCRIPT, replay.BY_ACTS):
        copy = replay.replay(data, ship_factory, road=road)
        assert copy.log.digest() == world.log.digest(), road
        assert copy.player_seat.agent.heard == seat.agent.heard, road
        for name, journal in world.agent_journals.items():
            assert copy.agent_journals[name].save() == journal.save(), (road, name)
    assert OFFICER in world.agents
