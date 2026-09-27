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


def standing_voyage() -> World:
    """The crewed voyage under two standing orders (spec M4 §4): one `at` eight bells,
    one `every` ten minutes, both firing during the run. Their firings are not
    journaled; only the orders that gave them are."""
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
    w.submit('standing order "bells": at eight bells then call all hands')
    w.submit('standing order "trim": every 10 minutes then trim sails')
    w.run(1500)
    w.submit('belay standing order "trim"')
    w.run(600)
    return w


def test_a_voyage_under_standing_orders_replays_with_the_same_firings(tmp_path):
    from freesail.api.session import ship_factory

    original = standing_voyage()
    fired = [
        (e.tick, e.actor, e.text)
        for e in original.log
        if e.kind == "order.accepted" and e.actor.startswith("standing order")
    ]
    assert [t for t, _, _ in fired] == [600, 1200, 1200], "trim at 600 and 1200, bells at 1200"
    assert all(not a.startswith("standing order") for _, a, _ in original.journal)
    path = replay.save_to_file(original, tmp_path / "standing.json")
    data = replay.load_file(path)
    assert [r["name"] for r in data["standing_orders"]] == ["bells", "trim"]
    copy = replay.replay(data, ship_factory)
    assert copy.log.digest() == original.log.digest()
    assert [
        (e.tick, e.actor, e.text)
        for e in copy.log
        if e.kind == "order.accepted" and e.actor.startswith("standing order")
    ] == fired
    assert copy.standing.book.save() == data["standing_orders"]


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
