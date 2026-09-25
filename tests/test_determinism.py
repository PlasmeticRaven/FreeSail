from freesail.core.world import Scenario, World

ORDERS = [
    (0, "steer south-west by west"),
    (120, "speed 5 knots"),
    (900, "steer east"),
    (1800, "speed 8"),
    (2700, "stop"),
]


def drive(seed: int, ticks: int = 3600) -> World:
    w = World(seed=seed, scenario=Scenario(gustiness=1.0, variability=1.0))
    pending = list(ORDERS)
    while w.clock.tick < ticks:
        while pending and pending[0][0] == w.clock.tick:
            w.submit(pending.pop(0)[1])
        w.tick()
    return w


def test_same_seed_same_log():
    a, b = drive(11), drive(11)
    assert a.log.digest() == b.log.digest()
    assert a.state() == b.state()


def test_different_seed_different_log():
    a, b = drive(11), drive(12)
    assert a.log.digest() != b.log.digest()


def test_log_is_not_trivially_short():
    # the drive above should produce bells, orders and some weather
    w = drive(11)
    kinds = {e.kind for e in w.log}
    assert {"order.accepted", "helm.order", "clock.bell"} <= kinds
