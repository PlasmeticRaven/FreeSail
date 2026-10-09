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
    assert sum(1 for _, _, t in original.journal if t.startswith("standing order")) == 9
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
        "heavy weather",
        "storm staysail",
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


def _restamp(path, stamp, checkpoint: bool = False) -> None:
    """Rewrite a save's stamp (None: unstamped), and its checkpoint's header's when asked,
    as another build would have written them."""
    import gzip
    import json

    data = json.loads(path.read_text())
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
    assert stamp["name"] == world_mod.BUILD_NAME == "m5c-c"
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
        _restamp(path, stamp)
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
            "rules open a sample.",
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
    _restamp(path, None)
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
