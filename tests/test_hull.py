"""Package 5: hull physics, helm and integration, tested with stub sail forces.

Every test replaces `compute_sail_forces` in `freesail.physics.integrate` with
a stub returning fixed forces, so nothing here depends on package 4.
"""

from __future__ import annotations

import copy
import math
import random

import pytest

from freesail import units
from freesail.physics import hull as hp
from freesail.physics import integrate
from freesail.physics.sails import SailForces
from freesail.physics.wind import Wind, WindParams
from freesail.ship.loader import load_ship, ship_from_dict
from freesail.ship.parts import HelmMode, SailState
from tests.test_ship_loader import MINIMAL

FRIGATE = "data/ships/frigate-36.yaml"
SCHOONER = "data/ships/topsail-schooner.yaml"


def steady_wind(from_deg: float = 225.0, knots: float = 15.0) -> Wind:
    """A wind that is never stepped, so it never wanders."""
    return Wind(WindParams.from_nautical(from_deg, knots), random.Random(0))


def fixed(thrust=0.0, side=0.0, heel=0.0, yaw=0.0):
    """A stub `compute_sail_forces` returning the same forces every substep."""

    def stub(ship, wind):
        return SailForces(thrust, side, heel, yaw, 0.0)

    return stub


def run(ship, seconds, wind=None, collect=None):
    wind = wind or steady_wind()
    notes = []
    for _ in range(seconds):
        integrate.step(ship, 1.0, wind)
        notes.extend(ship.drain_notes())
        if collect is not None:
            collect(ship)
    return notes


@pytest.fixture
def frigate():
    return load_ship(FRIGATE)


@pytest.fixture
def schooner():
    return load_ship(SCHOONER)


# -- surge ----------------------------------------------------------------


def test_forward_force_reaches_terminal_speed_below_hull_speed(frigate, monkeypatch):
    monkeypatch.setattr(integrate, "compute_sail_forces", fixed(thrust=30_000.0))
    speeds = []
    run(frigate, 900, collect=lambda s: speeds.append(s.dyn.speed))
    assert all(b >= a - 1e-9 for a, b in zip(speeds, speeds[1:], strict=False))  # never slows
    assert speeds[-1] - speeds[-60] < 0.01  # settled
    assert units.knots_to_ms(6.0) < speeds[-1] < frigate.hull.hull_speed
    # at terminal speed the thrust equals the resistance
    assert math.isclose(-hp.resistance(frigate.hull, frigate.dyn.u), 30_000.0, rel_tol=0.02)
    assert frigate.dyn.leeway == pytest.approx(0.0)
    assert frigate.dyn.heading == pytest.approx(0.0)


def test_more_force_needed_near_hull_speed(frigate):
    hull = frigate.hull
    slow = -hp.resistance(hull, 0.25 * hull.hull_speed)
    fast = -hp.resistance(hull, hull.hull_speed)
    assert fast > 16 * slow * 1.5  # more than the plain square law by a good margin


def test_resistance_opposes_sternway(frigate):
    assert hp.resistance(frigate.hull, 2.0) < 0 < hp.resistance(frigate.hull, -2.0)


def test_thrust_astern_gives_sternway_that_is_bounded(frigate, monkeypatch):
    monkeypatch.setattr(integrate, "compute_sail_forces", fixed(thrust=-10_000.0))
    run(frigate, 300)
    assert -3.0 < frigate.dyn.u < 0.0
    assert frigate.dyn.y < 0.0


def test_position_follows_heading(schooner, monkeypatch):
    monkeypatch.setattr(integrate, "compute_sail_forces", fixed(thrust=8_000.0))
    schooner.dyn.heading = math.radians(90.0)
    schooner.dyn.target_heading = schooner.dyn.heading
    run(schooner, 120)
    assert schooner.dyn.x > 50.0
    assert abs(schooner.dyn.y) < 1.0


# -- sway, leeway, heel ----------------------------------------------------


@pytest.mark.parametrize("sign", [1.0, -1.0])
def test_side_force_gives_leeway_and_heel_of_the_right_sign(frigate, monkeypatch, sign):
    monkeypatch.setattr(
        integrate,
        "compute_sail_forces",
        fixed(thrust=30_000.0, side=sign * 40_000.0, heel=sign * 40_000.0 * 20.0),
    )
    run(frigate, 300)
    d = frigate.dyn
    assert sign * d.v > 0.0
    assert sign * d.leeway > 0.0
    assert math.radians(0.5) < abs(d.leeway) < math.radians(15.0)
    assert sign * d.heel > 0.0
    assert math.radians(1.0) < abs(d.heel) < math.radians(15.0)
    assert d.speed == pytest.approx(math.hypot(d.u, d.v))


def test_heel_relaxes_to_the_quasi_static_balance(frigate, monkeypatch):
    moment = 3.0e6
    monkeypatch.setattr(integrate, "compute_sail_forces", fixed(heel=moment))
    heels = []
    run(frigate, 40, collect=lambda s: heels.append(s.dyn.heel))
    righting = frigate.hull.spec.displacement_kg * units.G * frigate.hull.spec.gm_m
    expected = math.asin(moment / righting)
    assert heels[3] < expected * 0.8  # not there yet after a few seconds
    assert heels[-1] == pytest.approx(expected, rel=0.01)
    assert all(b >= a for a, b in zip(heels, heels[1:], strict=False))


def test_beam_ends_is_logged_once_per_episode(frigate, monkeypatch):
    righting = frigate.hull.spec.displacement_kg * units.G * frigate.hull.spec.gm_m
    monkeypatch.setattr(integrate, "compute_sail_forces", fixed(heel=0.9 * righting))
    notes = run(frigate, 120)
    kinds = [n[1] for n in notes if n[1] == "ship.beam_ends"]
    assert kinds == ["ship.beam_ends"]
    assert [n[0] for n in notes if n[1] == "ship.beam_ends"] == ["urgent"]
    assert frigate.dyn.heel > hp.BEAM_ENDS_HEEL


def test_sway_is_clamped_at_low_speed(schooner, monkeypatch):
    monkeypatch.setattr(integrate, "compute_sail_forces", fixed(side=200_000.0))
    run(schooner, 120)
    d = schooner.dyn
    assert abs(d.v) <= hp.SWAY_CLAMP_SLOPE * abs(d.u) + hp.SWAY_CLAMP_OFFSET + 1e-9


# -- rudder and yaw --------------------------------------------------------


@pytest.mark.parametrize("sign", [1.0, -1.0])
def test_rudder_turns_the_ship_the_way_it_is_put(frigate, monkeypatch, sign):
    monkeypatch.setattr(integrate, "compute_sail_forces", fixed(thrust=30_000.0))
    frigate.dyn.u = 4.0
    frigate.dyn.helm_mode = HelmMode.RUDDER
    frigate.dyn.target_rudder = sign * math.radians(20.0)
    run(frigate, 60)
    d = frigate.dyn
    assert d.rudder == pytest.approx(sign * math.radians(20.0))
    assert sign * d.r > 0.0
    assert sign * units.wrap_pi(d.heading) > math.radians(20.0)
    assert math.radians(0.5) < abs(d.r) < math.radians(3.0)  # a frigate swings slowly


def test_rudder_moves_no_faster_than_its_rate(frigate, monkeypatch):
    monkeypatch.setattr(integrate, "compute_sail_forces", fixed(thrust=30_000.0))
    frigate.dyn.helm_mode = HelmMode.RUDDER
    frigate.dyn.target_rudder = math.radians(90.0)  # beyond the stop
    run(frigate, 5)
    rate = math.radians(frigate.hull.spec.rudder.rate_deg_s)
    assert frigate.dyn.rudder == pytest.approx(5 * rate)
    run(frigate, 60)
    assert frigate.dyn.rudder == pytest.approx(math.radians(frigate.hull.spec.rudder.max_angle_deg))


def test_rudder_does_little_without_way(frigate, monkeypatch):
    monkeypatch.setattr(integrate, "compute_sail_forces", fixed())
    frigate.dyn.helm_mode = HelmMode.RUDDER
    frigate.dyn.target_rudder = math.radians(35.0)
    run(frigate, 120)
    assert abs(units.wrap_pi(frigate.dyn.heading)) < math.radians(3.0)


def test_yaw_moment_turns_to_starboard(schooner, monkeypatch):
    monkeypatch.setattr(integrate, "compute_sail_forces", fixed(thrust=8_000.0, yaw=50_000.0))
    schooner.dyn.helm_mode = HelmMode.RUDDER
    schooner.dyn.target_rudder = 0.0
    run(schooner, 60)
    assert schooner.dyn.r > 0.0
    assert units.wrap_pi(schooner.dyn.heading) > 0.0


# -- the helmsman -----------------------------------------------------------


def test_helmsman_reaches_ordered_heading_without_endless_oscillation(frigate, monkeypatch):
    monkeypatch.setattr(integrate, "compute_sail_forces", fixed(thrust=30_000.0, yaw=300_000.0))
    frigate.dyn.u = 4.0
    frigate.dyn.target_heading = math.radians(90.0)
    frigate.dyn.steady = False
    errors = []
    notes = run(
        frigate,
        600,
        collect=lambda s: errors.append(units.wrap_pi(s.dyn.heading - s.dyn.target_heading)),
    )
    # on the course, and still on it, for the whole last four minutes
    assert all(abs(e) < math.radians(2.0) for e in errors[-240:])
    assert abs(errors[-1]) < math.radians(0.5)
    steady = [n for n in notes if n[1] == "helm.steady"]
    assert len(steady) == 1
    assert steady[0][0] == "routine"
    assert "Steady on E" in steady[0][2]
    assert frigate.dyn.steady is True
    # the sails' yaw moment to starboard needs rudder to larboard to hold her
    assert frigate.dyn.rudder < -math.radians(2.0)
    # wind from SW, heading E: wind on the starboard quarter, she wants to round up
    assert frigate.dyn.weather_helm > 0.0


def test_helm_steady_is_logged_once_per_order(schooner, monkeypatch):
    monkeypatch.setattr(integrate, "compute_sail_forces", fixed(thrust=8_000.0))
    schooner.dyn.u = 3.0
    notes = run(schooner, 60)
    assert not [n for n in notes if n[1] == "helm.steady"]  # started steady: nothing to say
    schooner.dyn.target_heading = math.radians(30.0)
    schooner.dyn.steady = False
    notes = run(schooner, 400)
    assert len([n for n in notes if n[1] == "helm.steady"]) == 1
    notes = run(schooner, 400)
    assert not [n for n in notes if n[1] == "helm.steady"]
    schooner.dyn.steady = False  # same heading ordered again
    notes = run(schooner, 60)
    assert len([n for n in notes if n[1] == "helm.steady"]) == 1


@pytest.mark.parametrize(
    ("start_deg", "target_deg", "sense"),
    [(350.0, 10.0, 1.0), (10.0, 350.0, -1.0), (5.0, 355.0, -1.0)],
)
def test_heading_order_across_north_goes_the_short_way(
    schooner, monkeypatch, start_deg, target_deg, sense
):
    monkeypatch.setattr(integrate, "compute_sail_forces", fixed(thrust=8_000.0))
    schooner.dyn.u = 3.0
    schooner.dyn.heading = math.radians(start_deg)
    schooner.dyn.target_heading = math.radians(target_deg)
    schooner.dyn.steady = False
    rates = []
    notes = run(schooner, 300, collect=lambda s: rates.append(s.dyn.r))
    assert sense * rates[5] > 0.0  # set off the short way
    assert max(abs(r) for r in rates) < math.radians(5.0)
    err = units.wrap_pi(schooner.dyn.heading - math.radians(target_deg))
    assert abs(err) < math.radians(1.0)
    assert [n[1] for n in notes if n[1] == "helm.steady"] == ["helm.steady"]


@pytest.mark.parametrize("wind_from_deg", [45.0, 315.0])
def test_full_and_by_brings_her_up_to_the_luffing_angle_plus_margin(
    frigate, monkeypatch, wind_from_deg
):
    monkeypatch.setattr(integrate, "compute_sail_forces", fixed(thrust=20_000.0))
    wind = steady_wind(wind_from_deg, 15.0)
    frigate.dyn.u = 3.0
    frigate.dyn.heading = math.radians(180.0)
    frigate.dyn.helm_mode = HelmMode.FULL_AND_BY
    frigate.dyn.steady = False
    notes = run(frigate, 600, wind)
    awa, _ = hp.apparent_wind(frigate, wind)
    wanted = hp.FULL_AND_BY_DEFAULT_LUFF + hp.FULL_AND_BY_MARGIN
    assert abs(awa) == pytest.approx(wanted, abs=math.radians(3.0))
    # wind from NE is on the larboard bow after coming up; from NW on the starboard bow
    assert (awa < 0) == (wind_from_deg == 45.0)
    assert [n[1] for n in notes if n[1] == "helm.steady"] == ["helm.steady"]
    assert "full and by" in [n for n in notes if n[1] == "helm.steady"][0][2]


def test_full_and_by_uses_the_luff_angle_package_4_exposes(schooner, monkeypatch):
    monkeypatch.setattr(integrate, "compute_sail_forces", fixed(thrust=8_000.0))
    schooner.extra["luff_angle"] = math.radians(35.0)
    wind = steady_wind(0.0, 15.0)
    schooner.dyn.u = 3.0
    schooner.dyn.heading = math.radians(120.0)
    schooner.dyn.helm_mode = HelmMode.FULL_AND_BY
    schooner.dyn.steady = False
    run(schooner, 600, wind)
    awa, _ = hp.apparent_wind(schooner, wind)
    wanted = math.radians(35.0) + hp.FULL_AND_BY_MARGIN
    assert abs(awa) == pytest.approx(wanted, abs=math.radians(3.0))


# -- notes: aback and leeway ---------------------------------------------------


def test_taken_aback_is_urgent_after_ten_seconds_with_sail_set(frigate, monkeypatch):
    monkeypatch.setattr(integrate, "compute_sail_forces", fixed(thrust=-15_000.0))
    frigate.dyn.u = 3.0
    notes = run(frigate, 30)
    assert not [n for n in notes if n[1] == "ship.aback"]  # no sail set: not aback, just drifting
    frigate.sails["main.topsail"].state = SailState.SET
    notes = run(frigate, 9)
    assert not [n for n in notes if n[1] == "ship.aback"]
    notes = run(frigate, 2)
    aback = [n for n in notes if n[1] == "ship.aback"]
    assert len(aback) == 1
    assert aback[0][0] == "urgent"
    assert "aback" in aback[0][2].lower()
    notes = run(frigate, 60)
    assert not [n for n in notes if n[1] == "ship.aback"]  # once per episode
    # she fills again, then is taken aback anew
    monkeypatch.setattr(integrate, "compute_sail_forces", fixed(thrust=15_000.0))
    run(frigate, 5)
    monkeypatch.setattr(integrate, "compute_sail_forces", fixed(thrust=-15_000.0))
    notes = run(frigate, 15)
    assert len([n for n in notes if n[1] == "ship.aback"]) == 1


def test_leeway_change_is_noted_at_most_once_a_minute(frigate, monkeypatch):
    monkeypatch.setattr(integrate, "compute_sail_forces", fixed(thrust=30_000.0, side=40_000.0))
    frigate.dyn.u = 4.0
    notes = run(frigate, 600)
    leeway = [n for n in notes if n[1] == "ship.leeway"]
    assert leeway  # leeway grew from nothing as the side force took hold
    assert all(n[0] == "routine" for n in leeway)
    assert all("starboard" in n[2] for n in leeway)
    # no two notes within a minute of each other, and every note marks a change of over a degree
    assert len(leeway) <= 10
    values = [n[4]["leeway"] for n in leeway]
    assert all(abs(b - a) > math.radians(1.0) for a, b in zip(values, values[1:], strict=False))
    # settled: a further ten minutes says nothing new
    notes = run(frigate, 600)
    assert len([n for n in notes if n[1] == "ship.leeway"]) <= 1


def test_leeway_reads_zero_without_way(schooner, monkeypatch):
    monkeypatch.setattr(integrate, "compute_sail_forces", fixed(side=2_000.0))
    run(schooner, 10)
    assert schooner.dyn.speed < hp.LEEWAY_MIN_SPEED
    assert schooner.dyn.leeway == 0.0


# -- readings and helpers ------------------------------------------------------


def test_apparent_wind_on_deck():
    ship = ship_from_dict(copy.deepcopy(MINIMAL), "minimal")
    wind = steady_wind(45.0, 10.0)
    awa, aws = hp.apparent_wind(ship, wind)
    assert awa == pytest.approx(math.radians(45.0))  # stopped, heading N: wind on the starboard bow
    assert aws == pytest.approx(wind.speed_at_height(ship.hull.spec.deck_height_m))
    ship.dyn.u = 4.0
    awa2, aws2 = hp.apparent_wind(ship, wind)
    assert awa2 < awa  # way on draws the apparent wind ahead
    assert aws2 > aws
    ship.dyn.heading = math.radians(90.0)
    awa3, _ = hp.apparent_wind(ship, wind)
    assert awa3 < 0.0  # heading E, wind from NE: on the larboard bow


def test_weather_helm_reading_is_positive_when_she_wants_to_round_up():
    # wind on the starboard bow, rudder held to larboard: weather helm
    reading = 0.0
    for _ in range(1000):
        reading = hp.weather_helm_reading(reading, -0.1, math.radians(60.0), 0.25)
    assert reading == pytest.approx(0.1, abs=1e-3)
    # wind on the larboard bow, rudder held to larboard: lee helm
    reading = 0.0
    for _ in range(1000):
        reading = hp.weather_helm_reading(reading, -0.1, math.radians(-60.0), 0.25)
    assert reading == pytest.approx(-0.1, abs=1e-3)


def test_step_is_deterministic(frigate, monkeypatch):
    monkeypatch.setattr(
        integrate, "compute_sail_forces", fixed(thrust=25_000.0, side=30_000.0, yaw=200_000.0)
    )
    frigate.dyn.target_heading = math.radians(200.0)
    frigate.dyn.steady = False
    a = run(frigate, 300)
    state_a = frigate.dyn.state()
    other = load_ship(FRIGATE)
    other.dyn.target_heading = math.radians(200.0)
    other.dyn.steady = False
    b = run(other, 300)
    assert a == b
    assert state_a == other.dyn.state()


def test_both_reference_ships_run_under_bare_poles(frigate, schooner):
    """With every sail furled, the real sail physics gives only windage: the ships
    drift slowly and sanely, and the apparent wind is filled in."""
    for ship in (frigate, schooner):
        run(ship, 60)
        assert ship.dyn.speed < units.knots_to_ms(2.0)
        assert math.isfinite(ship.dyn.x) and math.isfinite(ship.dyn.heading)
        assert abs(ship.dyn.apparent_wind_angle) > 0.0
        assert ship.dyn.apparent_wind_speed > 0.0
        assert "hull" in ship.extra
