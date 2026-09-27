"""The sun (spec M4 §5): sunrise, sunset and civil twilight by the NOAA approximation
against an almanac, the `daylight` reading through the registry, the two events on the
sun's own tick and once a day, the first-tick rule, the ship's easting as longitude, the
high latitudes, and the latitude saved with the scenario.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta

import pytest

from freesail.api import readings as R
from freesail.api.session import make_world
from freesail.core import replay
from freesail.core.sun import (
    DAY,
    METRES_PER_DEGREE,
    NIGHT,
    TWILIGHT,
    Sun,
    declination_and_equation_of_time,
)
from freesail.core.world import Scenario, World

FRIGATE = "data/ships/frigate-36.yaml"

# The almanac: the U.S. Naval Observatory's rise/set service (aa.usno.navy.mil, "Complete
# Sun and Moon Data for One Day") for 50.0 N, 0.0 E on 1 June 2026, in UT, which is the
# mean time of that meridian: civil twilight begins 03:13, sunrise 03:56, sunset 20:00,
# civil twilight ends 20:43. The model is asked to be within two minutes of each
# (spec §5: "a few minutes' accuracy is plenty"); the year is 1805 here, which moves
# these by well under a minute.
ALMANAC_1_JUNE_50N = {"dawn": "03:13", "sunrise": "03:56", "sunset": "20:00", "dusk": "20:43"}
ALMANAC_TOLERANCE_MIN = 2.0


def minutes_between(a: datetime, hhmm: str) -> float:
    h, m = (int(x) for x in hhmm.split(":"))
    return abs((a - a.replace(hour=h, minute=m, second=0)).total_seconds()) / 60.0


def test_declination_and_equation_of_time_at_the_solstices_and_equinox():
    decl, eqt = declination_and_equation_of_time(datetime(1805, 6, 21, 12))
    assert 23.0 <= decl * 180 / 3.141592653589793 <= 23.6  # the obliquity, 23.44°
    assert abs(eqt) < 3.0  # the equation of time is small in late June
    decl, _ = declination_and_equation_of_time(datetime(1805, 12, 21, 12))
    assert -23.6 <= decl * 180 / 3.141592653589793 <= -23.0
    decl, _ = declination_and_equation_of_time(datetime(1805, 3, 21, 12))
    assert abs(decl) < 0.02
    _, eqt = declination_and_equation_of_time(datetime(1805, 11, 3, 12))
    assert 15.0 <= eqt <= 17.0  # the year's greatest, about sixteen and a half minutes


def test_the_channel_on_the_first_of_june_against_the_almanac():
    times = Sun(50.0).times(date(1805, 6, 1))
    assert times.sentence is None
    for key, hhmm in ALMANAC_1_JUNE_50N.items():
        when = getattr(times, key)
        assert minutes_between(when, hhmm) <= ALMANAC_TOLERANCE_MIN, (key, when, hhmm)
    assert times.describe().startswith("Sunrise 03:56, sunset 19:5")


def test_midwinter_is_short_and_the_phases_follow_the_elevation():
    sun = Sun(50.0)
    times = sun.times(date(1805, 12, 21))
    assert times.sunrise.hour == 7 and times.sunset.hour == 16
    assert sun.phase(datetime(1805, 12, 21, 12)) == DAY
    assert sun.phase(datetime(1805, 12, 21, 16, 20)) == TWILIGHT
    assert sun.phase(datetime(1805, 12, 21, 23)) == NIGHT
    # the phase by elevation and the times by hour angle agree to a minute
    assert sun.phase(times.sunrise - timedelta(minutes=1)) == TWILIGHT
    assert sun.phase(times.sunrise + timedelta(minutes=1)) == DAY
    assert sun.phase(times.dusk - timedelta(minutes=1)) == TWILIGHT
    assert sun.phase(times.dusk + timedelta(minutes=1)) == NIGHT


def test_high_latitudes_give_a_sentence_and_no_crossing():
    midnight_sun = Sun(70.0).times(date(1805, 6, 21))
    assert midnight_sun.sunrise is None
    assert midnight_sun.describe() == "The sun does not set today at this latitude."
    polar_night = Sun(70.0).times(date(1805, 12, 21))
    assert polar_night.describe() == "The sun does not rise today at this latitude."
    white_night = Sun(62.0).times(date(1805, 6, 21))  # sets, but never six degrees under
    assert white_night.sunrise is not None and white_night.dawn is None
    assert "twilight lasts the night" in white_night.describe()
    phases = {Sun(70.0).phase(datetime(1805, 6, 21, h)) for h in range(24)}
    assert phases == {DAY}


def test_easting_turns_to_longitude_and_brings_the_sun_earlier():
    sun = Sun(50.0)
    one_degree = METRES_PER_DEGREE * 0.6427876  # cos 50°
    assert sun.longitude_deg(one_degree) == pytest.approx(1.0, abs=1e-6)
    home = sun.times(date(1805, 6, 1))
    east = sun.times(date(1805, 6, 1), one_degree)
    west = sun.times(date(1805, 6, 1), -one_degree)
    # four minutes of clock time a degree, as the NOAA formula has it
    assert (home.sunrise - east.sunrise).total_seconds() == pytest.approx(240.0, abs=1.0)
    assert (west.sunset - home.sunset).total_seconds() == pytest.approx(240.0, abs=1.0)


# ---------------------------------------------------------------------------
# Through the World: the reading, the events, the first tick
# ---------------------------------------------------------------------------


def point_world(start: datetime, **kw) -> World:
    return World(seed=3, scenario=Scenario(start_time=start, gustiness=0.0, variability=0.0, **kw))


def sun_events(world: World) -> list[tuple[int, str, str]]:
    return [(e.tick, e.kind, e.text) for e in world.log if e.kind.startswith("sun.")]


def test_daylight_is_a_reading_of_the_registry_and_nowhere_else():
    row = R.REGISTRY.get("daylight")
    assert not row.is_absent and row.kind == "daylight" and row.words == ("daylight",)
    w = point_world(datetime(1805, 6, 1, 12, 0))
    assert w.readings["daylight"] == DAY
    assert w.readings.as_dict()["daylight"] == DAY
    assert point_world(datetime(1805, 6, 1, 1, 0)).readings["daylight"] == NIGHT
    assert point_world(datetime(1805, 6, 1, 3, 30)).readings["daylight"] == TWILIGHT
    # the console's state line reads it through the registry too
    assert w.summary_lines()[2].startswith("Day. Sunrise 03:56, sunset ")


def test_sunset_and_sunrise_are_events_on_the_suns_tick_once_a_day():
    w = point_world(datetime(1805, 6, 1, 19, 40))
    w.run(3900)  # to 20:45, through sunset and dusk
    events = sun_events(w)
    assert [k for _, k, _ in events] == ["sun.set"]
    tick, _, text = events[0]
    assert text == "Sunset."
    assert (w.clock.start + timedelta(seconds=tick)).strftime("%H:%M") == "19:59"
    sunset = w.log[[e.kind for e in w.log].index("sun.set")]
    assert sunset.severity.value == "notable"
    assert w.readings["daylight"] == NIGHT
    m = point_world(datetime(1805, 6, 1, 3, 0))
    m.run(2 * 3600)
    events = sun_events(m)
    assert [k for _, k, _ in events] == ["sun.rise"]
    assert events[0][2] == "Sunrise."
    assert (m.clock.start + timedelta(seconds=events[0][0])).strftime("%H:%M") == "03:56"


def test_a_sunrise_before_the_start_is_not_an_event_of_this_log():
    """The default scenario opens at 04:00 on 1 June at 50 N, four minutes after sunrise:
    the phase at the start is read, not announced, so the first event is the first
    crossing after tick 0 (sunset, sixteen hours on)."""
    w = World(seed=3)
    assert w.readings["daylight"] == DAY
    w.run(3600)
    assert sun_events(w) == []
    exactly = point_world(datetime(1805, 6, 1, 3, 56, 28))  # the crossing's own second
    assert exactly.readings["daylight"] == DAY
    exactly.run(600)
    assert sun_events(exactly) == []


def test_a_whole_day_raises_each_event_once_and_deterministically():
    def day() -> World:
        w = point_world(datetime(1805, 6, 1, 0, 0))
        w.run(24 * 3600)
        return w

    a, b = day(), day()
    assert [k for _, k, _ in sun_events(a)] == ["sun.rise", "sun.set"]
    assert sun_events(a) == sun_events(b)
    assert a.log.digest() == b.log.digest()


def test_the_midnight_sun_raises_nothing_and_does_not_crash():
    w = point_world(datetime(1805, 6, 21, 0, 0), latitude_deg=70.0)
    w.run(24 * 3600)
    assert sun_events(w) == []
    assert w.summary_lines()[2] == "Day. The sun does not set today at this latitude."


def test_the_ships_easting_moves_the_suns_clock():
    """A point ship steaming east all day meets sunset earlier by the clock: four
    minutes of clock time a degree of longitude."""
    still = point_world(datetime(1805, 6, 1, 12, 0))
    east = point_world(datetime(1805, 6, 1, 12, 0))
    east.submit("steer east")
    east.submit("speed 12 knots")
    still.run(9 * 3600)
    while not sun_events(east) and east.clock.tick < 9 * 3600:
        east.tick()
    (t_still, _, _), (t_east, _, _) = sun_events(still)[0], sun_events(east)[0]
    made_east_m = east.ship.x  # where she was when the sun set on her
    expected_earlier_s = 240.0 * east.sun.longitude_deg(made_east_m)
    assert expected_earlier_s > 60.0
    assert t_still - t_east == pytest.approx(expected_earlier_s, abs=60.0)


def test_latitude_is_saved_with_the_scenario_and_older_saves_load_at_fifty():
    w = point_world(datetime(1805, 6, 21, 0, 0), latitude_deg=70.0)
    w.run(600)
    data = w.save()
    assert data["scenario"]["latitude_deg"] == 70.0
    copy = replay.replay(data)
    assert copy.sun.latitude_deg == 70.0 and copy.log.digest() == w.log.digest()
    old = dict(data["scenario"])
    del old["latitude_deg"]
    assert Scenario.from_dict(old).latitude_deg == 50.0


def test_the_frigate_carries_the_same_sun(tmp_path):
    w = make_world(
        7,
        FRIGATE,
        Scenario(
            start_time=datetime(1805, 6, 1, 19, 50),
            wind_from_deg=0.0,
            gustiness=0.0,
            variability=0.0,
            ship_heading_deg=180.0,
        ),
    )
    w.submit("set plain sail")
    w.run(1200)
    assert [k for _, k, _ in sun_events(w)] == ["sun.set"]
    assert w.readings["daylight"] == TWILIGHT
    path = replay.save_to_file(w, tmp_path / "sunset.json")
    from freesail.api.session import ship_factory

    copy = replay.replay(replay.load_file(path), ship_factory)
    assert sun_events(copy) == sun_events(w)
