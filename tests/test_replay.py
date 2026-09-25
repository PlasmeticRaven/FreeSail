from freesail.core import replay
from freesail.core.world import Scenario, World


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
