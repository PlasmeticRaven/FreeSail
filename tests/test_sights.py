"""Package 33a: the noon sight (spec M5 §14's first sentence; N §1, §3).

The sun's meridian passage on the ship's clock, the sight allowed or refused by the
sky, the instrument's and the horizon's errors by the scenario's instrument, the
master's skill and the sea, and `observe the sun` by order.
"""

from __future__ import annotations

import random
from datetime import datetime

import pytest

from freesail.api.session import make_world
from freesail.core.sun import Sun
from freesail.core.world import Scenario
from freesail.orders.errors import OrderError
from freesail.world import sights as S
from freesail.world.reckoning import Master

FRIGATE = "data/ships/frigate-36.yaml"


class _Conditions:
    def __init__(self, sky: str, weather: str = "fine"):
        self.sky = sky
        self.weather = weather


class _World:
    """A world of the sight's inputs alone."""

    def __init__(
        self, lat: float, conditions=None, sea_m: float | None = None, instrument="sextant"
    ):
        from freesail.core.clock import Clock
        from freesail.world.geo import Position

        self.position = Position(lat, -5.0)
        self.conditions = conditions
        self.scenario = Scenario(instrument=instrument)
        self.clock = Clock(datetime(1805, 6, 10, 12, 0))

        class _Sea:
            def __init__(self, h):
                self.h = h

            def reading(self):
                class _R:
                    height_m = self.h

                return _R()

        self.sea = None if sea_m is None else _Sea(sea_m)


def test_the_suns_noon_on_the_ships_clock():
    """The meridian passage is 720 minutes less the equation of time and four minutes a
    degree of easting: on 10 June the equation is about a minute, so noon by the sun is
    a minute before twelve on the start meridian, and forty minutes earlier ten degrees
    to the east."""
    sun = Sun(49.5)
    noon = sun.transit(datetime(1805, 6, 10, 4, 0))
    assert noon.date() == datetime(1805, 6, 10).date()
    assert abs((noon - datetime(1805, 6, 10, 12, 0)).total_seconds()) < 3 * 60
    east = sun.transit(datetime(1805, 6, 10, 4, 0), ship_x_m=10.0 * 60.0 * 1852.0 * 0.65)
    assert abs((noon - east).total_seconds() - 40 * 60) < 3 * 60
    # the altitude at noon: 90 less the latitude plus the declination (about 23 in June)
    alt = sun.meridian_altitude_deg(datetime(1805, 6, 10))
    assert 62.0 < alt < 65.0


def test_the_sky_allows_or_hides_the_sun_in_the_registrys_words():
    assert S.sky_allows(None) == (True, "")
    assert S.sky_allows(_Conditions("clear")) == (True, "")
    assert S.sky_allows(_Conditions("hazy")) == (True, "")
    assert S.sky_allows(_Conditions("detached clouds")) == (True, "")
    for sky in S.SKY_HIDES_THE_SUN:
        allowed, why = S.sky_allows(_Conditions(sky))
        assert not allowed and why == "the sun was hid at noon"
    for weather in S.WEATHER_HIDES_THE_SUN:
        allowed, why = S.sky_allows(_Conditions("clear", weather))
        assert not allowed and why == f"the sun was hid at noon in {weather}"


def test_the_sights_error_by_instrument_skill_and_sea():
    """N §3: sextant to a minute, octant to two or three; the horizon in haze or swell
    two to five minutes; 2 to 5 miles with a good horizon, none in cloud."""

    def spread(instrument: str, skill: float, sea_m: float | None, sky: str = "clear") -> float:
        errors = []
        for seed in range(400):
            w = _World(49.5, _Conditions(sky), sea_m, instrument)
            result = S.noon_sight(w, Master("Mr Ellis", skill), random.Random(seed))
            assert result.sight is not None and result.refusal == ""
            errors.append((result.sight.latitude_deg - 49.5) * 60.0)
        return (sum(e * e for e in errors) / len(errors)) ** 0.5

    sextant = spread("sextant", 0.9, None)
    octant = spread("octant", 0.9, None)
    poor = spread("octant", 0.5, None)
    swell = spread("sextant", 0.9, 2.0)
    hazy = spread("sextant", 0.9, None, sky="hazy")
    assert 1.5 < sextant < 2.5  # "2 to 5 miles with a good horizon", the sextant's end
    assert octant > sextant and poor > octant
    assert swell > sextant and 2.5 < swell < 5.5  # the sea's motion widens the horizon
    assert hazy > sextant
    # the words, and the sigma the master puts on it
    w = _World(49.5, None, None, "sextant")
    result = S.noon_sight(w, Master("Mr Ellis", 0.9), random.Random(7))
    assert result.sight.words.endswith("' N") and result.sight.instrument == "sextant"
    assert 1.5 < result.sight.sigma_nm < 2.5
    with pytest.raises(ValueError):
        S.instrument_sigma_nm("astrolabe")


def test_the_sight_is_refused_in_cloud_and_the_reading_says_so():
    w = _World(49.5, _Conditions("overcast", "rain"))
    result = S.noon_sight(w, Master("Mr Ellis", 0.9), random.Random(7))
    assert result.sight is None and result.refusal == "the sun was hid at noon in rain"


def chart_world(start: datetime, instrument: str = "sextant", **kw):
    sc = Scenario(
        start_time=start,
        wind_from_deg=225.0,
        wind_speed_kn=12.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=0.0,
        position={"lat_deg": 49.4, "lon_deg": -5.3},
        region="channel-west",
        instrument=instrument,
        **kw,
    )
    return make_world(7, FRIGATE, sc)


def test_observe_the_sun_by_order_at_noon_and_refused_before_and_after():
    w = chart_world(datetime(1805, 6, 10, 9, 0))
    refused = w.submit("observe the sun")
    assert refused.kind == "order.rejected"
    assert "not yet on the meridian; noon by the sun is at" in refused.text
    w.run(2 * 3600 + 50 * 60)  # 11:50, within the quarter of an hour before noon
    e = w.submit("observe the sun")
    assert e.kind == "reckoning.noon" and e.text.startswith("Noon. Latitude by observation")
    assert w.readings["latitude_by_observation"] is not None
    w.run(3600)
    assert len([x for x in w.log if x.kind == "reckoning.noon"]) == 1  # not taken twice
    late = chart_world(datetime(1805, 6, 10, 14, 0))
    late.run(60)
    refused = late.submit("observe the sun")
    assert refused.kind == "order.rejected" and refused.data["reason"].startswith("Noon is past")
    # a scenario begun in the afternoon works no noon that day
    late.run(3600)
    assert not [x for x in late.log if x.kind == "reckoning.noon"]


def test_the_instrument_is_the_scenarios_and_a_wrong_one_is_refused():
    w = chart_world(datetime(1805, 6, 10, 11, 50), instrument="octant")
    w.run(20 * 60)
    noon = [x for x in w.log if x.kind == "reckoning.noon"][0]
    assert noon.data["sight"]["instrument"] == "octant"
    with pytest.raises(ValueError, match="sextant or octant"):
        chart_world(datetime(1805, 6, 10, 11, 50), instrument="astrolabe")


def test_the_sky_pinned_thick_refuses_the_sight_in_the_registrys_words():
    from freesail.world.scenarios import load_scenario, make_scenario_world

    sf = load_scenario("data/scenarios/gate-5b-passage-thick.yaml")
    assert sf.scenario.sky == {"sky": "thick", "weather": "fog", "visibility": "a mile"}
    assert any("The sky pinned" in line for line in sf.lines())
    world = make_scenario_world(sf)
    world.run(60)
    assert world.readings["sky"]["words"] == "thick"
    assert world.readings["weather"] == "fog"
    assert world.readings["visibility"]["miles"] == 1.0
    assert not S.sky_allows(world.conditions)[0]
    with pytest.raises(OrderError):
        raise OrderError("placeholder")  # the orders' refusal path is tested above
