"""The tide (spec M5 §16; package 34; decision 29): the world's harmonic tide at the
eleven gauges and the streams by area, the captain's tide from his epitome and Moore's
rule, and the two kept apart. Truths 62, 63 and 64 of spec M5 §19.

The world's figures here are the author's view: no reading gives them, and the tests
read `world.tide` and `world.tide_state` directly, as the brief allows the tests to."""

from __future__ import annotations

import math
from datetime import date, datetime, timedelta

import pytest

from freesail import units
from freesail.api import readings as R
from freesail.api.session import make_world
from freesail.core.world import Scenario, World
from freesail.world import tide as T
from freesail.world.geo import Position, bearing_and_distance

FRIGATE = "data/ships/frigate-36.yaml"
REGION = "channel-west"
FALMOUTH = Position(50.155, -5.045)  # the outer road off Pendennis
THE_LIZARD = Position(49.93, -5.20)  # three miles south of the point
FULL_MOON_1805_06 = date(1805, 6, 12)  # the moon fifteen days old by the mean elements
FIRST_QUARTER_1805_06 = date(1805, 6, 4)
LAST_QUARTER_1805_06 = date(1805, 6, 19)


@pytest.fixture(scope="module")
def tide() -> T.Tide:
    return T.load_tide()


def _lmt_hours(when_ut: datetime, pos: Position) -> float:
    local = T.local_mean_time(when_ut, pos.lon_deg)
    return local.hour + local.minute / 60.0 + local.second / 3600.0


def _minutes_apart_mod(a_h: float, b_h: float, period_h: float) -> float:
    d = (a_h - b_h) % period_h
    return 60.0 * min(d, period_h - d)


# ---------------------------------------------------------------------------
# The world's tide
# ---------------------------------------------------------------------------


def test_the_constituents_are_the_studys_eleven_gauges_with_sources(tide):
    """Eleven gauges, each with M2, S2 and N2 and a mean level; the file names its
    source (TICON, verified from the archive) and the datum offsets' standing."""
    assert len(tide.gauges) == 11
    names = {g.name for g in tide.gauges}
    assert {"Newlyn", "Devonport", "Brest", "Dover"} <= names
    for g in tide.gauges:
        assert set(g.constants) == {"M2", "S2", "N2"}
        assert g.mean_level_m > 0.0
        for amp, phase in g.constants.values():
            assert amp > 0.0 and 0.0 <= phase < 360.0
    text = open(T.CONSTITUENTS_PATH, encoding="utf-8").read()
    assert "TICON" in text and "CC BY 4.0" in text
    assert "UNVERIFIED" in text  # the datum offsets open item 3 leaves open say so


def test_truth_62_high_water_at_falmouth_on_the_full_moon_falls_at_the_establishment(tide):
    """Spec M5 §19, truth 62: "At Falmouth high water on the day of full moon falls at the
    establishment within twenty minutes; springs are twice neaps; the perigean spring
    exceeds the apogean by about a fifth." The establishment is the world's own, from
    the constants (the hour of high water at full and change, local mean time)."""
    day = datetime(FULL_MOON_1805_06.year, FULL_MOON_1805_06.month, FULL_MOON_1805_06.day)
    assert 14.5 <= T.moon_age_days(day + timedelta(hours=12)) <= 15.5
    highs = tide.high_waters(FALMOUTH, day, 24.0)
    assert len(highs) == 2
    establishment_h = tide.establishment_at(FALMOUTH)
    assert 4.0 < establishment_h < 5.5  # 4h 41m: Dessiou's 5h 15m is the 1805 figure
    for when, height in highs:
        apart = _minutes_apart_mod(_lmt_hours(when, FALMOUTH), establishment_h, 12.42)
        assert apart <= 20.0, f"{when} is {apart:.0f} minutes from the establishment"
        assert 4.5 < height < 5.5  # a spring high water, metres above the datum
    # springs are twice neaps: the amplitudes M2 + S2 against M2 - S2
    state = tide.at(FALMOUTH, day)
    ratio = state.spring_amplitude_m / state.neap_amplitude_m
    assert 1.8 <= ratio <= 2.3, ratio
    # the perigean spring against the apogean, over half a year of springs
    start = datetime(1805, 1, 1)
    amplitudes = [
        tide.at(FALMOUTH, start + timedelta(minutes=30 * i)).amplitude_m for i in range(48 * 183)
    ]
    springs = []
    window = 48 * 7  # a week either side: one spring in each fortnight
    for i in range(window, len(amplitudes) - window):
        a = amplitudes[i]
        if a == max(amplitudes[i - window : i + window + 1]):
            springs.append(a)
    assert len(springs) >= 10
    excess = max(springs) / min(springs) - 1.0
    assert 0.1 <= excess <= 0.5, f"the perigean spring exceeds the apogean by {excess:.2f}"


def test_truth_63_off_the_lizard_the_stream_runs_east_about_high_water_at_two_knots(tide):
    """Spec M5 §19, truth 63: "Off the Lizard the stream runs east from about three hours
    before to three hours after local high water at two knots at springs and one at
    neaps"; the ship hove to for six hours is set the log's miles by it (below)."""
    assert tide.area_at(THE_LIZARD).id == "the-lizard"
    day = datetime(FULL_MOON_1805_06.year, FULL_MOON_1805_06.month, FULL_MOON_1805_06.day)
    hw, _ = tide.high_waters(THE_LIZARD, day, 24.0)[0]
    rates = {}
    for h in range(-6, 7):
        state = tide.at(THE_LIZARD, hw + timedelta(hours=h))
        rates[h] = (state.stream_kn, state.stream_toward_deg, state.slack)
    for h in (-2, -1, 0, 1, 2):
        kn, toward, _ = rates[h]
        assert 45.0 <= toward <= 125.0, f"HW{h:+d}: toward {toward:.0f}"  # east
    for h in (-5, -4, 4, 5):
        kn, toward, _ = rates[h]
        assert 225.0 <= toward <= 305.0, f"HW{h:+d}: toward {toward:.0f}"  # west
    assert rates[-3][2] or rates[-3][0] < 0.8
    assert rates[3][2] or rates[3][0] < 0.8
    strongest = max(rates[h][0] for h in (-2, -1, 0, 1, 2))
    assert 1.6 <= strongest <= 2.4, strongest  # two knots at springs
    neaps = datetime(1805, 6, 21)
    hw_n, _ = tide.high_waters(THE_LIZARD, neaps, 24.0)[0]
    strongest_n = max(tide.at(THE_LIZARD, hw_n + timedelta(hours=h)).stream_kn for h in (-1, 0, 1))
    assert 0.7 <= strongest_n <= 1.3, strongest_n  # one at neaps


def test_truth_63_a_ship_hove_to_six_hours_off_the_lizard_is_set_the_logs_miles():
    """The second clause of truth 63: a point ship (set by the stream alone) goes where
    the stream's run says; the frigate hove to for six hours is set along the stream's
    axis by the stream's miles, her own forereaching apart."""
    start = datetime(1805, 6, 12, 2, 0)  # the east-going stream of the forenoon
    sc = Scenario(
        start_time=start,
        wind_from_deg=225.0,
        wind_speed_kn=12.0,
        gustiness=0.0,
        variability=0.0,
        position={"lat_deg": THE_LIZARD.lat_deg, "lon_deg": THE_LIZARD.lon_deg},
        region=REGION,
    )
    point = World(seed=7, scenario=sc)
    run_e = run_n = 0.0
    for _ in range(6 * 60):
        state = point.tide_state
        run_e += state.stream_east_ms * 60.0
        run_n += state.stream_north_ms * 60.0
        point.run(60)
    expected = point.origin.advanced(run_e, run_n)
    assert bearing_and_distance(expected, point.position)[1] < 50.0  # the stream's integral
    miles = units.m_to_nm(math.hypot(run_e, run_n))
    assert 3.0 <= miles <= 14.0, miles  # the log's miles: a knot or two for six hours
    # the frigate hove to: set along the stream's axis by about the same
    frigate = make_world(7, FRIGATE, sc)
    frigate.submit("set plain sail")
    frigate.run(600)
    frigate.submit("heave to")
    frigate.run(900)
    assert "hove_to" in frigate.ship.extra
    x0, y0 = frigate.ship.dyn.x, frigate.ship.dyn.y
    tick0 = frigate.clock.tick
    set_e = set_n = 0.0  # the stream's run
    own_e = own_n = 0.0  # her own way through the water, the log's (by the second)
    while frigate.clock.tick < tick0 + 6 * 3600:
        state = frigate.tide_state
        set_e += state.stream_east_ms * 10.0
        set_n += state.stream_north_ms * 10.0
        d = frigate.ship.dyn
        ex, ey = math.sin(d.heading), math.cos(d.heading)
        own_e += (d.u * ex + d.v * ey) * 10.0
        own_n += (d.u * ey - d.v * ex) * 10.0
        frigate.run(10)
    moved = (frigate.ship.dyn.x - x0, frigate.ship.dyn.y - y0)
    along = math.hypot(set_e, set_n)
    assert units.m_to_nm(along) >= 3.0
    # over the ground she went her own way and the stream's: the set is the stream's
    # miles, which the log never saw
    set_found = (moved[0] - own_e, moved[1] - own_n)
    assert math.hypot(set_found[0] - set_e, set_found[1] - set_n) < 0.1 * along
    assert units.m_to_nm(math.hypot(own_e, own_n)) < 12.0  # hove to, a knot or two


def test_the_tide_is_deterministic_under_the_seed_and_the_stream_moves_the_track():
    """Two worlds at one seed agree tick for tick with the stream in; the same ship on
    the endless plane (no chart, no tide) is not moved by it."""
    sc = Scenario(
        start_time=datetime(1805, 6, 12, 8, 0),
        wind_from_deg=225.0,
        wind_speed_kn=12.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=90.0,
        position={"lat_deg": THE_LIZARD.lat_deg, "lon_deg": THE_LIZARD.lon_deg},
        region=REGION,
    )
    a, b = make_world(7, FRIGATE, sc), make_world(7, FRIGATE, sc)
    for w in (a, b):
        w.submit("set plain sail")
        w.run(3600)
    assert (a.ship.dyn.x, a.ship.dyn.y) == (b.ship.dyn.x, b.ship.dyn.y)
    assert a.tide_state.to_dict() == b.tide_state.to_dict()
    assert a.log.digest() == b.log.digest()
    assert a.ship.extra["water"] != (0.0, 0.0)
    # through the water her speed is her own; over the ground the stream is added
    plane = make_world(7, FRIGATE, Scenario(**{**sc.__dict__, "position": None, "region": None}))
    plane.submit("set plain sail")
    plane.run(3600)
    assert plane.ship.extra.get("water") is None
    assert abs(plane.ship.dyn.u - a.ship.dyn.u) < 0.3  # the same way through the water
    assert math.hypot(plane.ship.dyn.x - a.ship.dyn.x, plane.ship.dyn.y - a.ship.dyn.y) > 500.0


# ---------------------------------------------------------------------------
# The captain's tide
# ---------------------------------------------------------------------------


def test_truth_64_moores_rule_against_the_worlds_tide_at_full_moon_and_the_quarters(tide):
    """Spec M5 §19, truth 64: "The captain's tide worked from Moore's rule and an 1805
    establishment differs from the world's tide by less than an hour on the day of full
    moon and by up to an hour at the quarters." The captain's: Norie's Falmouth, 5h 15m
    at full and change, and the moon's age from the mean elements to the quarter day."""
    norie = T.Epitome.load("norie")
    port = norie.by_name("Falmouth")
    assert port is not None and abs(port.establishment_h - 5.25) < 1e-9
    worst = {}
    for label, day in (
        ("full", FULL_MOON_1805_06),
        ("first quarter", FIRST_QUARTER_1805_06),
        ("last quarter", LAST_QUARTER_1805_06),
    ):
        noon = datetime(day.year, day.month, day.day, 12, 0) + timedelta(minutes=20)  # GMT
        age = round(T.moon_age_days(noon) * 4.0) / 4.0
        captain = norie.high_waters(port, age, day)
        begin = datetime(day.year, day.month, day.day) + timedelta(minutes=20)  # LMT midnight
        world = [
            T.local_mean_time(t, FALMOUTH.lon_deg)
            for t, _ in tide.high_waters(FALMOUTH, begin, 24.0)
        ]
        assert captain and world
        apart = []
        for c in captain:
            nearest = min(world, key=lambda t: abs((t - c).total_seconds()))
            apart.append(abs((nearest - c).total_seconds()) / 60.0)
        worst[label] = max(apart)
    assert worst["full"] < 60.0, worst
    assert worst["first quarter"] <= 75.0 and worst["last quarter"] <= 75.0, worst
    assert max(worst.values()) > 15.0  # the two tides are not one


def test_the_captains_tide_is_a_reading_in_his_words_and_the_worlds_is_none():
    """Decision 29: the reading `the tide by the almanac` is the master's, from the
    epitome and the moon's age, in words; no reading gives the world's height or
    stream, and the registry's rows say nothing of a height in metres."""
    sc = Scenario(
        start_time=datetime(1805, 6, 12, 10, 0),
        wind_from_deg=225.0,
        wind_speed_kn=12.0,
        gustiness=0.0,
        variability=0.0,
        position={"lat_deg": FALMOUTH.lat_deg, "lon_deg": FALMOUTH.lon_deg},
        region=REGION,
    )
    w = make_world(7, FRIGATE, sc)
    w.run(60)
    r = w.readings["tide_by_almanac"]
    assert r["port"] == "Falmouth" and r["table"] == "norie"
    assert "by the epitome" in r["words"] and "5h 15m at full and change" in r["words"]
    assert "the moon fifteen days old" in r["words"]
    assert w.readings.words("tide_by_almanac") == r["words"]
    # the world's height is a number the tests may read and no reading gives
    assert w.tide_height_m > 0.0
    for row in R.REGISTRY:
        assert "height of the tide" not in row.description
        assert row.id not in ("tide", "tide_height", "stream")
    assert str(round(w.tide_height_m, 2)) not in r["words"]
    # the order at the prompt
    e = w.submit("the tide by the almanac")
    assert "High water at Falmouth about" in e.text
    # a ship of war carries Norie's table, a merchantman Moore's (judgement)
    schooner = make_world(7, "data/ships/topsail-schooner.yaml", sc)
    assert schooner.navigation.epitome.table == "moore"
    moore = schooner.readings["tide_by_almanac"]["words"]
    assert "Ramhead" in moore and "nearest place in the master's table" in moore  # no Falmouth


def test_the_lead_reads_the_tide_and_the_master_allows_for_it_by_his_almanac():
    """Spec M5 §16: the cast is the chart's depth and the tide's height; the master
    takes his own allowance off before he lays it on the chart (`_tide_allowance_m`),
    which is by his almanac and not the world's tide."""
    sc = Scenario(
        start_time=datetime(1805, 6, 12, 4, 0),  # near high water at springs
        wind_from_deg=225.0,
        wind_speed_kn=12.0,
        gustiness=0.0,
        variability=0.0,
        position={"lat_deg": 50.12, "lon_deg": -5.02},  # twelve fathoms off Pendennis
        region=REGION,
    )
    w = make_world(7, FRIGATE, sc)
    w.submit("heave the lead")
    w.run(300)
    cast = [e for e in w.log if e.kind == "sounding"][-1]
    chart = w.chart.depth_at(w.position)
    assert w.tide_height_m > 3.0  # near high water at springs
    assert cast.data["depth_m"] > chart + 1.5  # the lead reads the water, tide and all
    allowance = w.navigation._tide_allowance_m()
    assert 0.0 <= allowance <= units.feet_to_m(15.0)
    assert abs(allowance - w.tide_height_m) < 2.5  # his rule of thumb against the truth
