import math

import pytest

from freesail import units
from freesail.core.events import Severity
from freesail.core.world import Scenario, World


def test_world_starts_with_a_log_entry():
    w = World(seed=1)
    assert len(w.log) == 1
    assert w.log[0].kind == "world.start"
    assert w.clock.tick == 0


def test_orders_are_journaled_only_when_accepted():
    w = World(seed=1)
    e = w.submit("steer south-west")
    assert e.kind == "helm.order"
    assert w.journal == [(0, "captain", "steer south-west")]
    r = w.submit("splice the mainbrace")
    assert r.kind == "order.rejected"
    assert "not an order" in r.text
    assert len(w.journal) == 1


def test_ship_comes_round_to_ordered_heading():
    w = World(seed=1, scenario=Scenario(ship_heading_deg=0))
    w.submit("steer 90")
    w.run(30)  # 2 deg/s
    assert w.ship.heading == pytest.approx(units.deg_to_rad(60), abs=1e-6)
    w.run(30)
    assert w.ship.heading == pytest.approx(units.deg_to_rad(90), abs=1e-6)
    assert w.log.of_kind("helm.steady")


def test_ship_turns_the_short_way():
    w = World(seed=1, scenario=Scenario(ship_heading_deg=10))
    w.submit("steer 350")
    w.run(5)
    assert units.wrap_pi(w.ship.heading) == pytest.approx(units.deg_to_rad(0), abs=1e-6)


def test_ship_makes_way():
    w = World(seed=1, scenario=Scenario(ship_heading_deg=90))
    w.submit("speed 6 knots")
    w.run(600)
    assert w.ship.speed == pytest.approx(units.knots_to_ms(6))
    assert w.ship.x > 0 and abs(w.ship.y) < 1e-6
    w.submit("stop")
    w.run(600)
    assert w.ship.speed == pytest.approx(0.0)


def test_bells_are_logged_over_an_hour():
    w = World(seed=1)
    w.run(3600)
    bells = [e.data["bells"] for e in w.log.of_kind("clock.bell")]
    assert bells == [1, 2]  # 04:30 and 05:00


def test_wind_does_not_die_and_stays_near_base():
    w = World(seed=7, scenario=Scenario(wind_speed_kn=15))
    w.run(3600 * 6)
    kn = units.ms_to_knots(w.wind.speed)
    assert 5 < kn < 30
    assert 0 <= w.wind.direction_from < 2 * math.pi


def test_summary_and_state_shapes():
    w = World(seed=1)
    lines = w.summary_lines()
    assert lines[0].startswith("Morning watch")
    s = w.state()
    assert set(s) == {"tick", "ship_time", "stamp", "wind", "ship"}


def test_severity_of_rejection_is_routine():
    w = World(seed=1)
    e = w.submit("fly")
    assert e.severity is Severity.ROUTINE
