"""Package 30's wind by the air mass (spec M5 §3; the study's §4), under every wind since
package 31b (the owner's ruling at gate 5a, decision 28).

The gust factor is drawn by the air mass as a multiple of the ten-minute mean, squalls
come only in unstable air with a veer and a few minutes' length, and the direction's
wander is mean-reverting about the base with a spread by the air mass. A wind given no
air mass (a fixed wind, a pinned wind whose scenario says nothing) is in neutral air; the
milestone 2 draws are retired.
"""

from __future__ import annotations

import random
import statistics

import pytest

from freesail import units
from freesail.core.rng import Rng
from freesail.physics import wind as Wm
from freesail.physics.wind import Wind, WindParams


def stream(seed: int = 7) -> random.Random:
    return Rng(seed).stream("wind")


def test_a_wind_given_no_air_mass_is_in_neutral_air_and_gusts_to_1_3_at_most():
    """The default air is neutral (`DEFAULT_AIR_MASS`): a fixed wind stepped a day at full
    gustiness gusts to 1.30 of its mean at most, never squalls, and its direction stays
    within the neutral spread of the base instead of walking away."""
    params = WindParams.from_nautical(270.0, 20.0, gustiness=1.0, variability=0.3)
    w = Wind(params, stream(7))
    assert w.air_mass == Wm.DEFAULT_AIR_MASS == "neutral"
    mean = units.knots_to_ms(20.0)
    gusts = 0
    peaks = []
    offsets = []
    for _ in range(24 * 3600):
        w.step(1.0, mean_speed=mean)
        assert not w.squall_started and not w.in_squall
        if w.gust_started:
            gusts += 1
            assert Wm.GUST_FACTOR_RANGES["neutral"][0] <= w.gust_factor <= 1.30
            peaks.append(w.effective_speed)
        offsets.append(units.rad_to_deg(units.wrap_pi(w.direction_from - w.base_direction)))
    assert gusts > 100 and max(peaks) <= mean * 1.30 + 1e-9
    assert max(abs(x) for x in offsets) < 5 * Wm.WANDER_SPREAD_DEG["neutral"]
    # the milestone 2 draws are retired: no factor above 1.30 in a day, where the old
    # rule drew 1.1 to 1.5 whatever the mean and reached 1.45 within an hour


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
    # a wind given no air mass is in neutral air: no squalls whatever the stream
    w = Wind(params, stream(5))
    assert w.air_mass == "neutral"
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


def test_follow_moves_the_base_and_the_offset_rides_on_it_in_any_air():
    for air in ("neutral", "warm", "unstable"):
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
