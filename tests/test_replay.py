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


STARTER = "data/standing_orders/starter.orders"


def standing_voyage() -> World:
    """Truth 39 (spec M4 §8): the frigate before the wind under all sail, studding sails
    both sides, from 19:30 on 1 June under the six starter routines (spec §6; the well's
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
        # the well's line is refused at load (spec §6), and a refused order is not
        # journaled, so its refusal line is not replayed: a day that loaded it replays to
        # the same ship and a log one line shorter. The voyage that must replay to the same
        # digest loads the five that enter.
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
        (2700, "standing order 'trim'"),
    ], "trim every ten minutes from 19:45; the night routine at sunset, 19:59"
    assert [e.tick for e in original.log if e.kind == "sun.set"] == [1742]
    assert all(not a.startswith("standing order") for _, a, _ in original.journal)
    assert sum(1 for _, _, t in original.journal if t.startswith("standing order")) == 6
    assert "order.rejected" not in {e.kind for e in original.log}
    path = replay.save_to_file(original, tmp_path / "standing.json")
    data = replay.load_file(path)
    assert [r["name"] for r in data["standing_orders"]] == [
        "night routine",
        "morning sail",
        "shorten sail for weather",
        "keep her full",
        "heavy weather",
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
