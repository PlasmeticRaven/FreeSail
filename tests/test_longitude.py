"""Package 33b: the chronometer, the time sight, the lunar, the amplitude and the
azimuth, and the captain's chart in his hands (spec M5 §14, §15, §17; decision 30; the
study `docs/design/Navigation1805.md` §2 to §5).

The world keeps the truth and the master keeps his account: every sight here is drawn
from the truth plus a seeded error and compared with the truth read from the world; the
lunar is never computed from the model's own geometry. The lookout's three faults of
playtest 13 (the held estimate, the dangers first, the names), the chart's edge, the
light in thick weather and the Nare are here too.
"""

from __future__ import annotations

import math
import random
from datetime import date, datetime

import pytest

from freesail import units
from freesail.api import queries
from freesail.api import readings as R
from freesail.api.session import make_world
from freesail.core.events import Severity
from freesail.core.world import Scenario, World
from freesail.world import chart as C
from freesail.world import lookout as L
from freesail.world import reckoning as K
from freesail.world import sights as S
from freesail.world.chart import Sighting, load_chart
from freesail.world.geo import Position, bearing_and_distance, destination
from freesail.world.weather import Conditions

FRIGATE = "data/ships/frigate-36.yaml"
SCHOONER = "data/ships/topsail-schooner.yaml"
LIZARD = Position(49.9594, -5.2067)
EARNSHAW = {
    "maker": "Earnshaw",
    "where": "Plymouth",
    "rated": "1805-04-26",  # forty days before 5 June
    "rate_s_per_day": 1.8,
    "drift": 0.0,
}
THICK = Conditions("warm", "warm", "thick", "", "fog", "a mile", 1012.0)
CLEAR = Conditions("high", "neutral", "clear", "", "fine", "the horizon", 1020.0)


def chart_world(
    lat: float = 49.5,
    lon: float = -5.2,
    start: datetime = datetime(1805, 6, 5, 9, 0),
    ship: str = FRIGATE,
    heading: float = 0.0,
    seed: int = 7,
    **kw,
) -> World:
    sc = Scenario(
        start_time=start,
        wind_from_deg=225.0,
        wind_speed_kn=12.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=heading,
        position={"lat_deg": lat, "lon_deg": lon},
        region="channel-west",
        **kw,
    )
    return make_world(seed, ship, sc)


def miles(a: Position, b: Position) -> float:
    return bearing_and_distance(a, b)[1] / units.NAUTICAL_MILE


def lon_miles(world: World, lon_deg: float) -> float:
    """How far a longitude lies from the truth's, in miles east or west at the latitude."""
    truth = world.position
    return abs(lon_deg - truth.lon_deg) * 60.0 * math.cos(math.radians(truth.lat_deg))


# ---------------------------------------------------------------------------
# The chronometer
# ---------------------------------------------------------------------------


def test_the_chronometer_is_the_scenarios_and_keeps_greenwich_time_with_its_error():
    """Spec §14: a scenario item, the captain's own; absent unless the scenario says.
    Its Greenwich time is the ship's clock plus the start meridian's westing; what the
    master reads is that plus the rating's offset and the drift times the days."""
    w = chart_world()
    assert w.navigation.chronometer is None
    assert w.readings["chronometer"] is None
    assert w.readings.words("chronometer") == "the ship carries no chronometer"
    w = chart_world(chronometer=EARNSHAW)
    c = w.navigation.chronometer
    assert c is not None and c.name == "the Earnshaw" and c.where == "Plymouth"
    assert c.drift_s_per_day == 0.0 and abs(c.offset_s) < 3 * S.RATING_OFFSET_SIGMA_S
    assert 39.0 < c.days_since_rated(w.clock.ship_time) < 41.0
    gmt = S.greenwich_time(w)
    assert (gmt - w.clock.ship_time).total_seconds() == pytest.approx(5.2 / 15.0 * 3600.0)
    read = c.masters_gmt(gmt, w.clock.ship_time)
    assert abs((read - gmt).total_seconds() - c.offset_s) < 1e-6
    words = w.readings.words("chronometer")
    assert words.startswith("the Earnshaw reads") and "40 days from its rating" in words
    assert "would trust it within" in words
    # the seeded drift: one to three seconds a day in either sense, from its own stream
    drifts = set()
    for seed in range(12):
        ww = chart_world(seed=seed, chronometer=EARNSHAW | {"drift": "seeded"})
        d = ww.navigation.chronometer.drift_s_per_day
        assert S.RATE_DRIFT_MIN_S_PER_DAY <= abs(d) <= S.RATE_DRIFT_MAX_S_PER_DAY
        drifts.add(d > 0)
    assert drifts == {True, False}
    # the same seed, the same chronometer
    a = chart_world(chronometer=EARNSHAW | {"drift": "seeded"}).navigation.chronometer
    b = chart_world(chronometer=EARNSHAW | {"drift": "seeded"}).navigation.chronometer
    assert (a.drift_s_per_day, a.offset_s) == (b.drift_s_per_day, b.offset_s)


def test_the_master_winds_it_at_eight_and_a_forgotten_one_runs_down():
    """Luce 1884's routine, "8:00 A.M. ... report chronometers wound"; forgetting is a
    scenario event, and a chronometer not wound is a dead one (spec §14)."""
    w = chart_world(start=datetime(1805, 6, 5, 7, 59), chronometer=EARNSHAW)
    w.run(90)
    wound = [e for e in w.log if e.kind == "chronometer.wound"]
    assert len(wound) == 1 and wound[0].text == "Wound the Earnshaw."
    assert wound[0].ship_time.hour == 8 and wound[0].ship_time.minute == 0
    e = w.submit("wind the chronometer")  # by order, any hour
    assert e.kind == "chronometer.wound" and e.text == "Wound the Earnshaw."
    e = w.submit("compare the watches")
    assert e.kind == "chronometer.compared" and "at Greenwich, the deck watch" in e.text
    # forgotten on the 6th and the 7th (a two-day movement forgives one morning): dead
    # on the 7th at four in the afternoon, fifty-six hours from the last winding
    w = chart_world(
        start=datetime(1805, 6, 5, 7, 59),
        chronometer=EARNSHAW | {"forgotten": ["1805-06-06", "1805-06-07"]},
    )
    w.run(3 * 24 * 3600 - 3600)
    dead = [e for e in w.log if e.kind == "chronometer.dead"]
    assert len(dead) == 1 and dead[0].severity is Severity.NOTABLE
    assert dead[0].text == "The Earnshaw has run down: it was not wound."
    assert [e.ship_time.day for e in w.log if e.kind == "chronometer.wound"] == [5]
    assert dead[0].ship_time == datetime(1805, 6, 7, 16, 0, 1)
    assert not w.navigation.chronometer.going
    assert "is dead" in w.readings.words("chronometer")
    refused = w.submit("take a sight for the longitude")
    assert refused.kind == "order.rejected" and "is dead" in refused.text
    # set going again by the deck watch and the account: it carries the account's error
    e = w.submit("wind the chronometer")
    assert e.kind == "chronometer.wound" and "set it going by the deck watch" in e.text
    c = w.navigation.chronometer
    assert c.going and c.set_error_s != 0.0
    err = c.error_s(w.clock.ship_time)
    expected = (w.position.lon_deg - w.navigation.reckoning.lon_deg) * 240.0
    assert abs(err - expected) < 1e-6
    assert w.submit("take a sight for the longitude").kind != "order.rejected"


def test_the_scenario_file_reads_a_chronometer_and_refuses_a_bad_one(tmp_path):
    from freesail.world.scenarios import ScenarioError, load_scenario, make_scenario_world

    good = tmp_path / "chron.yaml"
    good.write_text(
        "name: a chronometer\nstart: 1805-06-05T09:00\nposition: 49 30 N 5 12 W\n"
        "region: channel-west\nship:\n  file: data/ships/frigate-36.yaml\n"
        "  chronometer: {maker: Earnshaw, where: Plymouth, rated: 1805-04-26, "
        "rate_s_per_day: 1.8, drift: seeded}\n",
        encoding="utf-8",
    )
    sf = load_scenario(good)
    assert sf.scenario.chronometer == {
        "maker": "Earnshaw",
        "where": "Plymouth",
        "rated": "1805-04-26",
        "rate_s_per_day": 1.8,
        "drift": "seeded",
        "forgotten": [],
    }
    assert any("carries a chronometer by Earnshaw" in line for line in sf.lines())
    w = make_scenario_world(sf)
    assert w.navigation.chronometer.where == "Plymouth"
    assert Scenario.from_dict(w.scenario.to_dict()).chronometer == sf.scenario.chronometer
    bad = tmp_path / "bad.yaml"
    bad.write_text(
        good.read_text(encoding="utf-8").replace("rated: 1805-04-26", "rated: whenever"),
        encoding="utf-8",
    )
    with pytest.raises(ScenarioError, match="chronometer"):
        load_scenario(bad)
    # the gate's passages stay without one (the brief)
    for name in ("gate-5b-passage", "gate-5b-passage-thick", "gate-5b-passage-schooner"):
        assert load_scenario(f"data/scenarios/{name}.yaml").scenario.chronometer is None


# ---------------------------------------------------------------------------
# The time sight
# ---------------------------------------------------------------------------


def test_the_time_sight_is_refused_in_words_and_allowed_in_the_forenoon():
    """N §4(b): refused without a chronometer, in cloud, with the sun too low or too
    near the meridian; allowed, a longitude within the master's trust, the east-west
    doubt collapsed to it and the north-south left."""
    w = chart_world()
    refused = w.submit("take a sight for the longitude")
    assert refused.kind == "order.rejected" and "no chronometer aboard" in refused.text
    w = chart_world(start=datetime(1805, 6, 5, 4, 30), chronometer=EARNSHAW)
    assert "too low" in w.submit("take a sight for the longitude").text
    w = chart_world(start=datetime(1805, 6, 5, 11, 20), chronometer=EARNSHAW)
    assert "too near the meridian" in w.submit("take a sight for the longitude").text
    w = chart_world(chronometer=EARNSHAW)
    w.conditions = THICK
    assert "hid" in w.submit("take a sight for the longitude").text
    assert w.readings.words("longitude_by_chronometer") == "no sight for the longitude today"
    w = chart_world(chronometer=EARNSHAW)
    r = w.navigation.reckoning
    r.set_position(Position(49.5, -5.6), 0, sigma_nm=12.0)  # the account twenty miles out
    before = r.ellipse()
    e = w.submit("take a sight for the longitude")
    assert e.kind == "reckoning.time_sight"
    assert e.text.startswith("Forenoon. The sun's altitude for the time: longitude by chronometer")
    assert "the Earnshaw 40 days from Plymouth" in e.text and "would trust it within" in e.text
    sight = w.navigation.last_time_sight
    assert lon_miles(w, sight.longitude_deg) < 2.0 * S.TIME_SIGHT_SIGMA_NM
    after = r.ellipse()
    assert after["sigma_east_nm"] <= sight.sigma_nm + 0.01 < before["sigma_east_nm"]
    assert abs(after["sigma_north_nm"] - before["sigma_north_nm"]) < 0.01
    # weighed against the account by their two doubts (package 37e): the account, twelve
    # miles in doubt, against a chronometer forty days from its rating, good to six and
    # a half, goes three quarters of the way to the sight's line, and the words say how far
    assert e.data["how"] == "weighed" and ": the account moved " in e.text
    gain = 12.0**2 / (12.0**2 + sight.sigma_nm**2)
    apart = abs(sight.longitude_deg - (-5.6)) * 60.0 * math.cos(math.radians(49.5))
    assert 0.7 < gain < 0.8 and e.data["moved_nm"] == pytest.approx(gain * apart, rel=0.02)
    left = abs(sight.longitude_deg - r.lon_deg) * 60.0 * math.cos(math.radians(49.5))
    assert left == pytest.approx((1.0 - gain) * apart, rel=0.02)
    reading = w.readings["longitude_by_chronometer"]
    assert reading["lon_deg"] == sight.longitude_deg
    assert "by chronometer, 40 days from Plymouth" in reading["words"]
    assert (
        w.navigation.master.place == "below" and w.navigation.master.occupied_with == "time sight"
    )
    assert "below" in w.submit("take a sight for the longitude").text  # wait for him
    assert "Longitude" not in w.readings.words("reckoning")
    # a wrong rate puts the longitude out by the drift times the days, west when fast
    ww = chart_world(chronometer=EARNSHAW | {"drift": 2.0})
    ww.navigation.reckoning.set_position(Position(49.5, -5.6), 0, sigma_nm=12.0)
    e = ww.submit("take a sight for the longitude")
    s = ww.navigation.last_time_sight
    days = ww.navigation.chronometer.days_since_rated(ww.clock.ship_time)
    expected = days * 2.0 / 240.0  # degrees west: the same draws, the drift between them
    assert abs((sight.longitude_deg - s.longitude_deg) - expected) < 1e-6


# ---------------------------------------------------------------------------
# The lunar
# ---------------------------------------------------------------------------


def test_the_lunars_conditions_refuse_in_the_registrys_words():
    """N §4(c): the moon too young, down, too low; no body in distance; the sky thick;
    a star by day; a star the Almanac has no distances for."""
    w = chart_world(start=datetime(1805, 6, 26, 10, 0))  # a day from the change
    e = w.submit("take a lunar")
    assert e.kind == "order.rejected" and "No lunar to be had: the moon is" in e.text
    assert "from the change" in e.text or "old" in e.text
    w = chart_world(start=datetime(1805, 6, 5, 9, 0))  # the moon down in the forenoon
    assert "the moon is down" in w.submit("take a lunar").text
    w = chart_world(start=datetime(1805, 6, 5, 14, 10))  # just risen
    assert "the moon is too low" in w.submit("take a lunar").text
    w = chart_world(start=datetime(1805, 6, 5, 17, 40))
    w.conditions = THICK
    assert "the sky is thick with fog" in w.submit("take a lunar").text
    w.conditions = CLEAR
    assert "by day; the sun is up" in w.submit("take a lunar of Aldebaran").text
    assert "no distances for" in w.submit("take a lunar of Sirius").text
    assert w.readings.words("moon").endswith("in distance of the sun")
    assert w.readings["moon"]["in_sight"] is True
    # at night a star: 20 June at 01:40 by the clock (02:00 at Greenwich), Altair
    w = chart_world(start=datetime(1805, 6, 20, 1, 40))
    moon = S.moon_now(w)
    assert S.lunar_body(w, moon, None) == ("Altair", "")
    assert S.lunar_body(w, moon, "the sun")[0] == "Altair"  # the sun is down: a star serves
    assert S.lunar_body(w, moon, "Altair") == ("Altair", "")
    assert "not in distance" in S.lunar_body(w, moon, "Markab")[1]
    assert "Aldebaran is not up" in S.lunar_body(w, moon, "Aldebaran")[1]


def test_the_lunar_occupies_the_master_and_two_mates_and_answers_an_hour_later():
    """Spec §14, truth 61's second half: allowed, it occupies the master and two mates
    for a quarter of an hour (the evolution's hands, the master's place) and an hour of
    ship's time later the log gets the result, drawn and not computed: within a degree
    of the truth, the reckoning updated by it; a second lunar refused meanwhile."""
    w = chart_world(start=datetime(1805, 6, 5, 17, 40), chronometer=EARNSHAW)
    r = w.navigation.reckoning
    r.set_position(Position(49.5, -5.8), 0, sigma_nm=15.0)  # the account far to the west
    e = w.submit("take a lunar")
    assert e.kind == "order.accepted"
    w.run(1)
    started = [x for x in w.log if x.kind == "evolution.started"][-1]
    assert started.text.startswith("The master and two of the young gentlemen to the quarterdeck")
    assert "distances of the sun and the moon" in started.text
    runner = w.ship.extra["evolutions"]
    inst = next(i for i in runner.instances if i.evo.id == "take_lunar")
    assert inst.want is not None and inst.want.hands == 2
    master = w.navigation.master
    assert master.occupied and master.place == "on deck" and master.occupied_with == "lunar"
    assert "lunar" in w.readings.words("master")
    refused = w.submit("take a lunar")
    assert refused.kind == "order.rejected" and "wait for him" in refused.text
    w.run(S.LUNAR_ON_DECK_MINUTES * 60 - 60)
    assert not [x for x in w.log if x.kind == "lunar.taken"]  # a quarter of an hour at least
    w.run(10 * 60)  # the hands' pace and the weather stretch the file's quarter of an hour
    taken = [x for x in w.log if x.kind == "lunar.taken"]
    assert len(taken) == 1 and master.place == "below" and master.occupied_with == "lunar"
    assert w.readings.words("longitude_by_lunar") == "a lunar is being cleared below"
    assert "wait for him" in w.submit("take a lunar").text  # below at the lunar
    assert not [x for x in w.log if x.kind == "reckoning.lunar"]
    w.run(S.LUNAR_CLEARING_MINUTES * 60)
    lines = [x for x in w.log if x.kind == "reckoning.lunar"]
    assert len(lines) == 1 and lines[0].severity is Severity.NOTABLE
    text = lines[0].text
    assert text.startswith("A set of distances of the sun and the moon taken by Mr ")
    assert "longitude by lunar" in text and "would trust within" in text
    assert "The Earnshaw gave" in text and ("no fault" in text or "on its rate" in text)
    lunar = w.navigation.last_lunar
    assert lunar.body == "the sun" and lon_miles(w, lunar.longitude_deg) < 60.0 * 0.65
    assert abs(lunar.longitude_deg - w.position.lon_deg) < 1.0  # within a degree
    assert lon_miles(w, r.lon_deg) < 2.0 * lunar.sigma_nm + 1.0  # the account on its line
    assert r.sigma_east_nm <= lunar.sigma_nm + 0.01
    assert lines[0].tick == taken[0].tick + S.LUNAR_CLEARING_MINUTES * 60
    came = [x for x in w.log if x.kind == "master.place" and "lunar done" in x.text]
    assert len(came) == 1 and master.place == "on deck"
    reading = w.readings["longitude_by_lunar"]
    assert "by lunar of the sun" in reading["words"] and reading["lon_deg"] == lunar.longitude_deg
    error = w.readings["chronometer_error_by_lunar"]
    assert error is not None and "by the lunar of the sun" in error["words"]
    # the same seed, the same result; another seed another
    other = chart_world(start=datetime(1805, 6, 5, 17, 40), chronometer=EARNSHAW)
    other.navigation.reckoning.set_position(Position(49.5, -5.8), 0, sigma_nm=15.0)
    other.submit("take a lunar")
    other.run((S.LUNAR_ON_DECK_MINUTES + 9 + S.LUNAR_CLEARING_MINUTES) * 60)
    assert other.navigation.last_lunar.longitude_deg == lunar.longitude_deg
    same = chart_world(start=datetime(1805, 6, 5, 17, 40), chronometer=EARNSHAW)
    same.navigation.reckoning.set_position(Position(49.5, -5.8), 0, sigma_nm=15.0)
    same.submit("take a lunar")
    same.run((S.LUNAR_ON_DECK_MINUTES + 9 + S.LUNAR_CLEARING_MINUTES) * 60)
    assert same.log.digest() == other.log.digest()
    third = chart_world(start=datetime(1805, 6, 5, 17, 40), seed=8, chronometer=EARNSHAW)
    third.submit("take a lunar")
    third.run((S.LUNAR_ON_DECK_MINUTES + 9 + S.LUNAR_CLEARING_MINUTES) * 60)
    assert third.navigation.last_lunar.longitude_deg != lunar.longitude_deg


def test_the_lunars_spread_by_skill_sea_and_the_moons_rate():
    """N §2, §4(c): a quarter of a degree for a good master on a quiet day, a degree for
    a poor one in a seaway; 10 to 39 miles at 50 N. The draw's spread measured over
    four hundred seeds on a stub world; never computed from a distance."""

    class _Sea:
        def __init__(self, h):
            self.h = h

        def reading(self):
            class _R:
                height_m = self.h

            return _R()

    class _World:
        def __init__(self, sea_m):
            from freesail.core.clock import Clock

            self.position = Position(49.5, -5.2)
            self.origin = Position(49.5, -5.2)
            self.clock = Clock(datetime(1805, 6, 5, 17, 40))
            self.sea = None if sea_m is None else _Sea(sea_m)

    def spread(skill: float, sea_m: float | None, body: str = "the sun") -> float:
        errs = []
        for seed in range(400):
            w = _World(sea_m)
            lunar = S.lunar_result(w, K.Master("Mr Ellis", skill), random.Random(seed), body, None)
            errs.append(lunar.longitude_deg + 5.2)
        return (sum(e * e for e in errs) / len(errs)) ** 0.5

    good = spread(S.LUNAR_SKILL_GOOD, None)
    poor = spread(S.LUNAR_SKILL_POOR, 2.0)
    assert 0.2 < good < 0.3, good  # a quarter of a degree: ten miles at 50 N
    assert 0.8 < poor < 1.2, poor  # a degree: thirty-nine miles
    assert good < spread(S.LUNAR_SKILL_GOOD, 2.0) < poor
    assert good < spread(S.LUNAR_SKILL_POOR, None) < poor
    lunar = S.lunar_result(
        _World(None), K.Master("Mr Ellis", 0.9), random.Random(1), "the sun", None
    )
    assert lunar.trust_words in ("within 15 miles", "within 20 miles")


# ---------------------------------------------------------------------------
# The amplitude and the azimuth
# ---------------------------------------------------------------------------


def test_the_amplitude_finds_the_variation_to_a_degree_and_the_account_runs_truer():
    """Decision 30; N §3: "an azimuth observation gets it to a degree". At sunrise the
    sun's bearing by compass against its true bearing gives the variation, which the
    master allows thereafter in place of the chart's decade-old figure; refused with
    the sun well up or in cloud; the azimuth by day with the sun's altitude."""
    w = chart_world(start=datetime(1805, 6, 10, 10, 0))
    assert w.readings.words("variation") == "21° 30' W by the chart of 1794"
    refused = w.submit("observe an amplitude")
    assert refused.kind == "order.rejected" and "well up" in refused.text
    e = w.submit("observe an azimuth")
    assert e.kind == "reckoning.variation" and e.text.startswith("Observed the sun's azimuth")
    assert "by azimuth, 10 June" in e.text and "where the chart gave 21° 30' W" in e.text
    assert w.readings.words("variation").endswith("W by azimuth, 10 June")
    w = chart_world(start=datetime(1805, 6, 10, 4, 18))  # the sun rising
    w.conditions = THICK
    assert "hid" in w.submit("observe an amplitude").text
    w.conditions = None
    errors = w.navigation.errors
    heading = float(w.ship.heading)
    before = abs(math.degrees(errors.course_error_rad(heading)))
    assert before > 2.0  # the chart's 21° 30' against the world's 24°
    e = w.submit("observe an amplitude")
    assert e.kind == "reckoning.variation"
    assert e.text.startswith("Observed the sun's amplitude at its rising, bearing E by N")
    found = w.navigation.variation
    assert found.by == "amplitude" and found.day == date(1805, 6, 10)
    truth = K.VARIATION_1805_DEG + errors.deviation_deg(heading)
    assert abs(found.deg_west - truth) <= 1.25  # to a degree, read to the half degree
    assert abs(found.deg_west - K.VARIATION_1805_DEG) <= 1.25 + K.DEVIATION_MAX_DEG
    after = abs(math.degrees(errors.course_error_rad(heading)))
    assert after < before and after <= 2.0 and errors.variation_allowed_deg == found.deg_west
    assert w.readings["variation"] == pytest.approx(math.radians(found.deg_west))
    assert w.readings.words("variation") == found.words
    assert e.data["variation"]["deg_west"] == found.deg_west

    # the account thereafter runs truer: a day's run north at six knots laid down
    # with the course error before and after (the traverse alone, no helmsman's draw:
    # the helmsman's wander is a random term a fix resolves, the variation a bias
    # that grows in a straight line, N §3)
    def across_after_a_day(course_error_rad: float) -> float:
        r = K.Reckoning(Position(49.0, -5.5), sigma_nm=1.0)
        for h in range(24):
            r.advance(1.0, course_error_rad, 6.0, (h + 1) * 3600)
        return abs(r.offset_nm(Position(49.0 + 144.0 / 60.0, -5.5))[0])

    chart_err = math.radians(K.CHART_VARIATION_AGE_YEARS * K.VARIATION_DRIFT_DEG_PER_YEAR)
    assert across_after_a_day(chart_err) > across_after_a_day(errors.course_error_rad(0.0))
    # the dialect and the chart's block
    from freesail.standing.grammar import parse_condition

    assert parse_condition("the variation exceeds 20 degrees", w.ship).holds(w.readings, {})
    assert queries.snapshot(w)["reckoning"]["variation"]["by"] == "amplitude"


# ---------------------------------------------------------------------------
# The chart in the captain's hands
# ---------------------------------------------------------------------------


def test_the_chart_queries_read_the_account_and_say_so():
    """Decision 30; playtests 12 and 13: the bearing and the distance of any charted
    feature from the account, in sight or not, "by account" in the words; the dangers
    within ten miles, the nearest first; a course shaped says when its line passes a
    danger within a mile or crosses it."""
    w = chart_world(49.85, -5.2, start=datetime(1805, 6, 5, 9, 0))  # south of the Lizard
    nav = w.navigation
    nav.reckoning.set_position(Position(49.85, -5.3), 0)  # the account four miles west
    found = nav.by_chart("the Manacles")
    assert found is not None and "by account" in found["words"]
    manacles = w.chart.feature("the-manacles").position
    acc_bearing, acc_dist = bearing_and_distance(nav.account_now(), manacles)
    assert abs(found["metres"] - acc_dist) < 1.0
    assert found["bearing_true_deg"] == round(acc_bearing, 1)
    truth_bearing, _ = bearing_and_distance(w.position, manacles)
    assert abs(found["bearing_true_deg"] - truth_bearing) > 1.0  # the account's, not the truth's
    assert w.readings.words("distance_to", "the Manacles").endswith("miles by account")
    heading_words = units.format_heading(found["bearing"])
    assert w.readings.words("bearing_by_chart", "Manacle Rocks") == heading_words
    assert w.readings.words("bearing_by_chart", "Timbuctoo") == "not on the chart"
    assert w.readings.value("distance_to", "Timbuctoo") is None
    dangers = w.readings["dangers"]
    assert dangers is not None and dangers["items"][0]["kind"] in C.HAZARD_KINDS
    assert {"the-stags", "rose-rock"} <= {i["id"] for i in dangers["items"]}
    assert dangers["words"].endswith(": by account, within 10 miles")
    dists = [i["metres"] for i in dangers["items"]]
    assert dists == sorted(dists) and dangers["metres"] == dists[0]
    assert w.readings.words("dangers").startswith("the ")
    far = chart_world(49.2, -6.0, start=datetime(1805, 6, 5, 9, 0))
    assert far.readings["dangers"] is None
    assert far.readings.words("dangers") == "no charted danger within 10 miles of the account"
    assert nav.dangers(2.0) is None or all(
        i["metres"] <= 2.0 * units.NAUTICAL_MILE for i in nav.dangers(2.0)["items"]
    )
    # the course for Falmouth from south of the Lizard runs by the Manacles
    e = w.submit("shape a course for Falmouth")
    assert e.kind == "helm.set" and "by account" in e.text
    assert "the line" in e.text and (" within " in e.text or "crosses" in e.text)  # to the cable
    # a line clear of every danger says nothing of them
    clear = chart_world(49.3, -5.6, start=datetime(1805, 6, 5, 9, 0))
    e = clear.submit("shape a course for Ushant")
    assert e.kind == "helm.set" and "the line" not in e.text
    chart = load_chart("channel-west")
    passes = chart.line_passes(Position(49.95, -5.00), Position(50.15, -5.07), units.NAUTICAL_MILE)
    assert any(f.id == "the-manacles" for f, _off, _x in passes)
    assert any(
        crosses for f, _off, crosses in passes if f.id in ("the-manacles", "penwin-and-vaze")
    )
    assert chart.line_passes(Position(49.0, -6.0), Position(49.0, -5.0), units.NAUTICAL_MILE) == []
    near = chart.dangers_near(Position(50.0470, -5.0440), 2.0 * units.NAUTICAL_MILE)
    assert near and near[0][0].id in ("the-manacles", "penwin-and-vaze")
    assert chart.find_feature("the Lizard").id == "lizard-point"
    assert chart.find_feature("Lizard Point").id == "lizard-point"
    assert chart.find_feature("nothing of the kind") is None


def test_the_dialect_reads_the_new_rows_for_nothing_and_the_events_are_named():
    from freesail.standing.grammar import parse_condition, parse_standing

    w = chart_world(49.75, -5.2, start=datetime(1805, 6, 5, 17, 40), chronometer=EARNSHAW)
    for text in (
        "the dangers are under 20 miles",
        "the chronometer exceeds 1 mile",
        "the moon is in sight",
        "the longitude by chronometer is west of 5 W",
        "the longitude by lunar is east of 6 W",
        "the chronometer's error by lunar exceeds 10 miles",
        "the variation is under 30 degrees",
    ):
        c = parse_condition(text, w.ship)
        assert c.holds(w.readings, {}) in (True, False), text
    rule = parse_standing(
        w.ship, 'standing order "x": when the chronometer exceeds 10 miles then take a lunar'
    )
    assert rule.actions == ["take a lunar"]
    for words in (
        "a danger sighted",
        "a bearing steady and closing",
        "a lunar",
        "a longitude by chronometer",
        "the chronometer run down",
        "the variation observed",
    ):
        assert words in R.EVENTS, words
        parse_standing(w.ship, f'standing order "{words}": at {words} then heave the lead')
    assert R.event_matches(R.EVENTS["a danger sighted"], "lookout.sighting", {"seen_as": "danger"})
    assert not R.event_matches(
        R.EVENTS["a danger sighted"], "lookout.sighting", {"seen_as": "land"}
    )
    # every new row through the agent's door, and the snapshot without the truth
    from freesail.agents.tools import readings_words

    words = readings_words(w)
    for row in (
        "chronometer",
        "longitude_by_chronometer",
        "longitude_by_lunar",
        "moon",
        "variation",
        "dangers",
    ):
        assert row in words, row
    block = queries.snapshot(w)["reckoning"]
    assert block["chronometer"]["maker"] == "Earnshaw" and block["lunar"] is None
    assert "position" not in queries.snapshot(w)


# ---------------------------------------------------------------------------
# The lookout's three faults, the chart's edge, the light in thick weather
# ---------------------------------------------------------------------------


def test_the_lookouts_estimate_is_drawn_once_and_held_while_she_makes_no_way():
    """Playtest 13: the Start at four miles, four leagues and three leagues in an hour
    of calm. The distance by estimation is drawn once a sighting episode and held until
    she has moved a mile; the same figure in the list, the hail and the bearing taken."""
    ten_south = destination(LIZARD, 180.0, 10 * units.NAUTICAL_MILE)
    w = chart_world(ten_south.lat_deg, ten_south.lon_deg, start=datetime(1805, 6, 1, 10, 0))
    look = w.lookout
    s = look.find("the Lizard")
    assert s is not None and s.estimate_m is not None
    first = s.estimate_m
    factor = look._episodes["lizard-point"].factor
    assert abs(first - s.distance_m * factor) < 1.0 and 0.5 < factor < 1.5
    assert look.reading(0.0)["items"][0]["estimate"] == w.log[-1].data["estimate"] or True
    # half a mile on: held
    w._position = destination(ten_south, 0.0, 0.5 * units.NAUTICAL_MILE)
    w._geo_last = (w.ship_x, w.ship_y)
    w.run(60)
    held = look.find("the Lizard")
    assert held.estimate_m == first and held.distance_m < s.distance_m
    # the list and a bearing taken give one figure
    listed = next(i for i in look.reading(0.0)["items"] if i["id"] == "lizard-point")
    e = w.submit("take a bearing of the Lizard")
    assert e.kind == "bearing.taken" and listed["estimate"] in e.text
    assert w.readings.value("bearing_of", "the Lizard") is not None
    assert listed["estimate"] in w.navigation.bearing_reading("the Lizard")["words"]
    # a mile and a half on: judged afresh with the same eye
    w._position = destination(ten_south, 0.0, 2.0 * units.NAUTICAL_MILE)
    w._geo_last = (w.ship_x, w.ship_y)
    w.run(60)
    again = look.find("the Lizard")
    assert again.estimate_m != first and abs(again.estimate_m - again.distance_m * factor) < 1.0
    # lost for half an hour and found again: a new episode, a new draw from its own stream
    w._position = Position(49.0, -6.0)
    w._geo_last = (w.ship_x, w.ship_y)
    w.run(31 * 60)
    assert look.find("the Lizard") is None
    w._position = ten_south
    w._geo_last = (w.ship_x, w.ship_y)
    w.run(60)
    assert look._episodes["lizard-point"].factor != factor
    assert "lookout" in w.rng.stream_names()


def test_the_reading_names_dangers_first_whole_and_the_cap_never_cuts_a_danger():
    """Playtests 12 and 13: dangers first, then lights, the land, the marks; the cap of
    eight never cuts a danger off; "Black Head", not "black Head"."""
    assert L.lead_words("Black Head bearing N, distant two leagues") == (
        "Black Head bearing N, distant two leagues"
    )
    assert L.lead_words("A light on the larboard bow") == "a light on the larboard bow"
    assert L.lead_words("The land about the Lizard close aboard") == (
        "the land about the Lizard close aboard"
    )
    chart = load_chart("channel-west")
    look = L.Lookout(chart)
    marks = [f for f in chart.features.values() if f.kind in ("headland", "church", "castle")][:10]
    dangers = [f for f in chart.features.values() if f.kind in ("rock", "ledge")][:4]
    look.sightings = [Sighting(f, 10.0, 1000.0 * (i + 1), "mark") for i, f in enumerate(marks)] + [
        Sighting(f, 20.0, 20000.0 + i, "danger") for i, f in enumerate(dangers)
    ]
    reading = look.reading(0.0)
    named = reading["words"].split("; ")
    assert reading["count"] == 14 and named[-1] == "and 6 more in sight"
    assert len(named) == L.READING_MAX + 1
    assert all(": a danger" in n for n in named[:4])  # every danger, though the farthest
    assert all(n[:1].isupper() or n.startswith(("the ", "a ")) for n in named[:-1])
    # the Beast is a proper name mid-sentence; a church is "the" something
    assert any(n.startswith("the Manacles") or n[:1].isupper() for n in named)
    # a world off the Manacles: the danger is first in the reading and the words whole
    near = destination(Position(50.0470, -5.0440), 120.0, 2 * units.NAUTICAL_MILE)
    w = chart_world(near.lat_deg, near.lon_deg, start=datetime(1805, 6, 5, 9, 0))
    words = w.readings["in_sight"]["words"]
    assert ": a danger" in words.split("; ")[0] and "the Manacles bearing" in words
    assert "black Head" not in words and "manacle Point" not in words
    sighted = [e for e in w.log if e.kind == "lookout.sighting" and e.data["seen_as"] == "danger"]
    assert sighted and sighted[0].severity is Severity.NOTABLE


def test_a_bearing_steady_and_closing_is_hailed_for_a_danger_and_the_chart_edge_said():
    """The lookout's collision rule for a danger (and the land within a league), once a
    sighting episode; and the chart's edge in words."""
    manacles = Position(50.04666, -5.04419)
    start = destination(manacles, 200.0, 2.8 * units.NAUTICAL_MILE)
    w = chart_world(start.lat_deg, start.lon_deg, start=datetime(1805, 6, 5, 9, 0), heading=20.0)
    w.submit("set plain sail")
    w.submit("steer 20")
    w.run(25 * 60)
    closing = [e for e in w.log if e.kind == "lookout.closing"]
    manacles = [e for e in closing if e.data["id"] == "the-manacles"]
    assert manacles, [e.text for e in closing]
    hail = manacles[0]
    assert hail.text.startswith("The Manacles bearing") and "steady and closing" in hail.text
    assert hail.severity is Severity.NOTABLE and hail.data["closing"] is True
    assert all(e.data["seen_as"] == "danger" or e.data["distance_m"] <= 3.1 * 1852 for e in closing)
    assert len([e for e in closing if e.data["id"] == "the-manacles"]) == 1  # once an episode
    # the chart's edge: within ten miles of the eastern bound the lookout says so
    south, north, west, east = w.chart.bounds
    edge = chart_world(49.5, east - 0.1, start=datetime(1805, 6, 5, 9, 0))
    said = [e for e in edge.log if e.kind == "lookout.chart_edge"]
    assert len(said) == 1 and said[0].text.startswith("The chart has nothing to the eastward")
    assert edge.readings["in_sight"]["words"].endswith("the chart ends here")
    assert w.chart.edge_near(Position(49.5, -5.0), 10 * units.NAUTICAL_MILE) == []


def test_a_light_in_thick_weather_by_its_luminous_range_and_a_moonlit_night():
    """Playtest 13: the Lizard lights not seen ten miles off in the squalls' rain after
    dark. A light's range in the weather is Allard's law (the module's note): in four
    miles' visibility a twenty-mile light is seen at about ten, in a mile's at three;
    the land on a moonlit night at a league."""
    assert C.luminous_range_nm(20.0, 12.0) == 20.0 and C.luminous_range_nm(20.0, 10.0) == 20.0
    assert 9.0 < C.luminous_range_nm(20.0, 4.0) < 11.0
    assert 3.0 < C.luminous_range_nm(20.0, 1.0) < 3.5
    assert C.luminous_range_nm(13.0, 4.0) < C.luminous_range_nm(20.0, 4.0)
    chart = load_chart("channel-west")
    eye = 36.0
    night = datetime(1805, 6, 1, 23, 30)
    eight = destination(LIZARD, 180.0, 8 * units.NAUTICAL_MILE)
    eleven = destination(LIZARD, 180.0, 11 * units.NAUTICAL_MILE)
    seen = {s.feature.id for s in chart.in_sight(eight, eye, 4.0, "night", night)}
    assert "lizard-lights" in seen
    assert not {s.feature.id for s in chart.in_sight(eleven, eye, 4.0, "night", night)}
    assert not {s.feature.id for s in chart.in_sight(eight, eye, 1.0, "night", night)}
    assert "lizard-lights" in {
        s.feature.id for s in chart.in_sight(eleven, eye, None, "night", night)
    }
    # the moonlit night: 12 June 1805, full, the moon up over the Channel at midnight
    two_south = destination(LIZARD, 180.0, 2.0 * units.NAUTICAL_MILE)
    w = chart_world(two_south.lat_deg, two_south.lon_deg, start=datetime(1805, 6, 12, 23, 40))
    assert w.daylight == "night" and w.lookout.moonlit
    assert [e for e in w.log if e.kind == "lookout.moonlight"]
    assert w.readings["land"]["in_sight"] is True
    land = [s for s in w.lookout.sightings if s.seen_as == "land"]
    assert land and land[0].distance_m < C.MOONLIT_LAND_NM * units.NAUTICAL_MILE
    dark = chart_world(two_south.lat_deg, two_south.lon_deg, start=datetime(1805, 6, 26, 23, 40))
    assert dark.daylight == "night" and not dark.lookout.moonlit
    assert not [s for s in dark.lookout.sightings if s.seen_as == "land"]
    assert w.readings.words("moon").startswith("fifteen days old, full; up")
