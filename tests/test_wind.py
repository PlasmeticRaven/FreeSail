"""Package 30: the wind's two regimes (spec M5 §3; the study's §4).

Without an air mass the M2 wind is unchanged draw for draw, so every truth measured on a
fixed or pinned wind stands. With an air mass from the systems' sector the gust factor is
drawn by the air mass as a multiple of the ten-minute mean, squalls come only in unstable
air with a veer and a few minutes' length, and the direction's wander is mean-reverting
about the base with a spread by the air mass.
"""

from __future__ import annotations

import math
import random
import statistics

import pytest

from freesail import units
from freesail.core.rng import Rng
from freesail.physics import wind as Wm
from freesail.physics.wind import Wind, WindParams


def stream(seed: int = 7) -> random.Random:
    return Rng(seed).stream("wind")


def old_m2_step(w: Wind, r: random.Random, dt: float = 1.0) -> None:
    """The M2 `Wind.step` as it stood at the close of milestone 4, kept here as the
    regression's yardstick."""
    v = w.params.variability
    w._direction = units.wrap_2pi(w._direction + r.gauss(0.0, 0.0002 * v * math.sqrt(dt)))
    pull = (w.base_speed - w.speed) * 0.0005 * dt
    noise = r.gauss(0.0, 0.01 * v * w.base_speed * math.sqrt(dt))
    w.speed = max(w.MIN_SPEED, w.speed + pull + noise)
    w.gust_started = False
    if w.gust_remaining > 0:
        w.gust_remaining -= dt
        if w.gust_remaining <= 0:
            w.gust_factor = 1.0
    elif r.random() < w.params.gustiness * 0.002 * dt:
        w.gust_factor = r.uniform(1.1, 1.5)
        w.gust_remaining = r.uniform(5.0, 30.0)
        w.gust_started = True


def test_without_an_air_mass_the_m2_wind_is_unchanged_draw_for_draw():
    params = WindParams.from_nautical(270.0, 20.0, gustiness=0.5, variability=0.5)
    new = Wind(params, stream(7))
    old = Wind(params, stream(7))
    r_old = stream(7)  # the same numbers, stepped by the old code by hand
    old._stream = r_old
    gusts = 0
    for _ in range(7200):
        new.step(1.0)
        old_m2_step(old, r_old)
        assert new.direction_from == old.direction_from
        assert new.speed == old.speed and new.gust_factor == old.gust_factor
        assert new.effective_speed == old.speed * old.gust_factor
        gusts += new.gust_started
    assert gusts > 0 and new.air_mass is None and not new.in_squall


def test_the_m2_walk_is_a_fraction_of_a_degree_an_hour_not_a_point():
    """The corrected docstring (W §4): 0.0002 rad per root second at variability 1 is 0.69
    degrees an hour of standard deviation."""
    sd_per_hour = units.rad_to_deg(Wm.M2_WALK_RAD_PER_SQRT_S * math.sqrt(3600.0))
    assert sd_per_hour == pytest.approx(0.69, abs=0.01)
    assert sd_per_hour < units.rad_to_deg(units.POINT) / 10


@pytest.mark.parametrize("air", ["warm", "neutral", "unstable"])
def test_gusts_by_air_mass_are_multiples_of_the_ten_minute_mean(air):
    """The gust factor is drawn in the air mass's range (W §4) over the ten-minute mean
    the World hands in, so a gust's peak is the mean times the factor whatever the
    instant's wander; no gust in any air mass exceeds 1.30 of the mean (truth 54)."""
    params = WindParams.from_nautical(270.0, 20.0, gustiness=1.0, variability=0.3)
    w = Wind(params, stream(11))
    w.air_mass = air
    mean = units.knots_to_ms(20.0)
    factors = []
    for _ in range(4 * 3600):
        w.step(1.0, mean_speed=mean)
        if w.gust_started:
            factors.append(w.gust_factor)
            if not w.in_squall:  # a squall's peak stands above a gust's in unstable air
                assert w.effective_speed == pytest.approx(max(w.speed, mean * w.gust_factor))
    lo, hi = Wm.GUST_FACTOR_RANGES[air]
    assert len(factors) > 20 and all(lo <= f <= hi for f in factors)
    assert max(factors) <= 1.30
    assert min(factors) < lo + 0.03 and max(factors) > hi - 0.03


def test_squalls_come_only_in_unstable_air_with_a_veer_and_last_a_few_minutes():
    params = WindParams.from_nautical(315.0, 40.0, gustiness=0.3, variability=0.3)
    w = Wind(params, stream(5))
    w.air_mass = "unstable"
    mean = units.knots_to_ms(40.0)
    squalls = []
    seen: list[tuple[float, float, float]] = []
    for _ in range(8 * 3600):
        before = w.direction_from
        w.step(1.0, mean_speed=mean)
        if w.squall_started:
            veer = units.wrap_pi(w.direction_from - before)
            squalls.append((w.squall_factor, veer, w.squall_remaining))
            assert w.effective_speed == pytest.approx(max(w.speed, mean * w.squall_factor))
        if w.squall_ended:
            seen.append((w.squall_factor, w.squall_veer, w.effective_speed))
            assert not w.in_squall and w.squall_veer == 0.0
    assert squalls, "eight hours of unstable air bring a squall"
    for factor, veer, length in squalls:
        assert Wm.SQUALL_FACTOR_RANGE[0] <= factor <= Wm.SQUALL_FACTOR_RANGE[1]
        # a point or two, give or take the tick's wander
        assert units.POINT * 1.0 - 0.01 <= veer <= units.POINT * 2.0 + 0.01
        assert Wm.SQUALL_DURATION_S[0] <= length <= Wm.SQUALL_DURATION_S[1]
    # after a squall the wind is back to its gusts at most: no more than 1.30 of the mean
    assert seen and all(peak <= mean * 1.30 + 1e-9 for _, _, peak in seen)
    for air in ("warm", "neutral"):
        w = Wind(params, stream(5))
        w.air_mass = air
        for _ in range(8 * 3600):
            w.step(1.0, mean_speed=mean)
            assert not w.squall_started
    # no air mass: the M2 regime, no squalls whatever the stream
    w = Wind(params, stream(5))
    for _ in range(8 * 3600):
        w.step(1.0, mean_speed=mean)
        assert not w.squall_started and not w.in_squall


@pytest.mark.parametrize("air,spread", list(Wm.WANDER_SPREAD_DEG.items()))
def test_the_wander_reverts_to_the_base_with_the_air_masss_spread(air, spread):
    """Mean-reverting about the base (W §4): the direction's offset has the stationary
    spread of the air mass at the default variability and never walks away."""
    params = WindParams.from_nautical(
        270.0, 20.0, gustiness=0.0, variability=Wm.DEFAULT_VARIABILITY
    )
    w = Wind(params, stream(3))
    w.air_mass = air
    offsets = []
    for tick in range(12 * 3600):
        w.step(1.0)
        if tick > 3600:
            offsets.append(units.rad_to_deg(units.wrap_pi(w.direction_from - w.base_direction)))
    sd = statistics.pstdev(offsets)
    assert sd == pytest.approx(spread, rel=0.35), (air, sd)
    assert max(abs(x) for x in offsets) < 5 * spread
    assert abs(statistics.fmean(offsets)) < spread


def test_with_variability_nought_the_systems_wind_does_not_wander():
    params = WindParams.from_nautical(270.0, 20.0, gustiness=0.0, variability=0.0)
    w = Wind(params, stream(3))
    w.air_mass = "unstable"
    w.follow(units.deg_to_rad(300.0), units.knots_to_ms(25.0))
    for _ in range(3600):
        w.step(1.0, mean_speed=units.knots_to_ms(25.0))
    assert units.rad_to_deg(w.direction_from) == pytest.approx(300.0, abs=1e-9)
    assert w.speed == pytest.approx(units.knots_to_ms(25.0))


def test_follow_moves_the_base_and_the_offset_rides_on_it_in_both_regimes():
    for air in (None, "warm"):
        params = WindParams.from_nautical(270.0, 20.0, gustiness=0.0, variability=0.3)
        w = Wind(params, stream(9))
        w.air_mass = air
        for _ in range(600):
            w.step(1.0, mean_speed=w.speed)
        offset = units.wrap_pi(w.direction_from - w.base_direction)
        w.follow(units.deg_to_rad(315.0), units.knots_to_ms(30.0))
        assert units.wrap_pi(w.direction_from - w.base_direction) == pytest.approx(
            offset, abs=1e-12
        )
        assert w.base_speed == pytest.approx(units.knots_to_ms(30.0))
