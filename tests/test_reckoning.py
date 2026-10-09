"""Package 33a: the reckoning (spec M5 §13, §15; `docs/design/Navigation1805.md` §3).

The arithmetic of `world.reckoning.Reckoning` (the traverse, the doubt grown by the
random terms and the biases, the observations as lines), the seeded errors of a ship,
the words the log says, the World's glue (`Navigation`: the log hove hourly in the
frigate and two-hourly in the schooner, the casts, the bearings, the noon, the orders
refused in words on the plane), the readings through the registry and the standing
dialect, the captain's chart without the truth, and determinism under the seed.
"""

from __future__ import annotations

import math
import random
from datetime import datetime, timedelta

import pytest

from freesail import units
from freesail.api import readings as R
from freesail.api.session import make_world
from freesail.core.events import Severity
from freesail.core.world import Scenario, World
from freesail.orders.errors import OrderError
from freesail.world import reckoning as K
from freesail.world.geo import Position, bearing_and_distance, destination, format_position

FRIGATE = "data/ships/frigate-36.yaml"
SCHOONER = "data/ships/topsail-schooner.yaml"
REGION = "channel-west"


def chart_world(
    lat: float,
    lon: float,
    ship: str = FRIGATE,
    heading: float = 0.0,
    start: datetime = datetime(1805, 6, 10, 10, 0),
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
        region=REGION,
        **kw,
    )
    return make_world(seed, ship, sc)


def miles_between(a: Position, b: Position) -> float:
    return bearing_and_distance(a, b)[1] / units.NAUTICAL_MILE


# ---------------------------------------------------------------------------
# The arithmetic
# ---------------------------------------------------------------------------


def test_the_traverse_runs_the_account_along_the_course_and_grows_the_doubt():
    r = K.Reckoning(Position(49.0, -6.0), sigma_nm=0.0)
    made = r.advance(1.0, 0.0, 6.0, 3600)  # an hour north at six knots
    assert made == pytest.approx((0.0, 6.0))
    assert r.lat_deg == pytest.approx(49.1)
    assert r.lon_deg == pytest.approx(-6.0)
    r.advance(1.0, math.pi / 2, 6.0, 7200)  # an hour east
    assert r.lat_deg == pytest.approx(49.1)
    assert r.lon_deg == pytest.approx(-6.0 + 6.0 / (60.0 * math.cos(math.radians(49.1))))
    assert r.run_since_noon_nm == pytest.approx(12.0)
    e = r.ellipse()
    # two hours: the read's quarter mile an hour along, the steering across, the set
    # doubt east and north in a straight line
    assert 0.3 < e["sigma_east_nm"] < 0.8 and 0.2 < e["sigma_north_nm"] < 0.6
    assert e["semi_major_nm"] >= e["semi_minor_nm"] > 0.0
    assert len(r.track) == 3


def test_the_random_terms_grow_as_the_root_of_the_steps_and_the_biases_in_a_line():
    """N §3: "the random terms grow the uncertainty as the square root of the number of
    steps; the biases ... grow it in a straight line"."""

    def after(hours: int) -> tuple[float, float]:
        r = K.Reckoning(Position(49.0, -6.0), sigma_nm=0.0)
        for h in range(hours):
            r.advance(1.0, math.pi / 2, 6.0, (h + 1) * 3600)  # east, the wind free
        return r.sigma_east_nm, r.sigma_north_nm

    e1, n1 = after(24)
    e4, n4 = after(96)
    # east and west the set's bias rules: four days is near four times one day
    assert 3.4 < e4 / e1 < 4.0
    # north and south the random steering rules with a small bias: between root and line
    assert 1.9 < n4 / n1 < 3.2


def test_a_line_measurement_puts_the_account_on_the_line_and_keeps_the_doubt_along_it():
    """Package 37e, the one rule, as package 37j amends it: a line the account plainly
    disagrees with, and which is the better figure, is taken, the account laid on it and
    its doubt across the line the line's own; along the line nothing changes. (A line it
    does not plainly disagree with is weighed, and a poorer one doubted: below.)"""
    r = K.Reckoning(Position(49.0, -6.0), sigma_nm=0.0)
    for h in range(24):
        r.advance(1.0, 0.0, 6.0, (h + 1) * 3600)
    along_before = r.sigma_east_nm
    across_before = r.sigma_north_nm
    # a line east and west, twelve miles north of the account, known to half a mile: more
    # than the two doubts together allow, and the better figure
    assert across_before > 0.5
    assert 12.0 > K.OBSERVATION_OUT_SIGMAS * (across_before + 0.5)
    obs = r.observe_line(0.0, 12.0, 0.0, 1.0, 0.5)
    assert obs.how == K.TAKEN and obs.moved_nm == pytest.approx(12.0)
    assert obs.toward_deg == pytest.approx(0.0) and obs.off_nm == pytest.approx(12.0)
    assert not obs.doubted and obs.off_toward_deg == pytest.approx(0.0)
    assert r.lat_deg == pytest.approx(49.0 + 24 * 6.0 / 60.0 + 12.0 / 60.0)
    assert r.sigma_north_nm == pytest.approx(0.5)
    assert r.sigma_east_nm == pytest.approx(along_before)  # along the line as it was
    assert r.set_doubt[1] == 0.0 and r.set_doubt[0] > 0.0
    assert r.update_line(0.0, 0.0, 0.0, 1.0, 2.0) == 0.0  # the old door, the miles moved


def test_two_bearings_cross_to_a_point_and_a_transit_is_exact():
    r = K.Reckoning(Position(49.90, -5.30), sigma_nm=8.0)
    lizard = Position(49.9594, -5.2067)
    # the ship is really five miles south-west of where she is reckoned; the Lizard
    # bears NE from the truth and the Land's End NW: a good cut
    truth = Position(49.85, -5.38)
    b1, _ = bearing_and_distance(truth, lizard)
    r.update_bearing(lizard, math.radians(b1), 0.3)
    assert r.sigma_east_nm > 1.0 or r.sigma_north_nm > 1.0  # one line: a strip
    lands_end = Position(50.065, -5.716)
    b2, _ = bearing_and_distance(truth, lands_end)
    assert 60.0 < abs(math.degrees(units.wrap_pi(math.radians(b1 - b2)))) < 120.0
    r.update_bearing(lands_end, math.radians(b2), 0.3)
    assert miles_between(r.position, truth) < 0.5
    assert r.ellipse()["semi_major_nm"] < 1.0
    # a transit: a cable across
    r.update_bearing(lizard, math.radians(b1), K.TRANSIT_SIGMA_NM)
    assert r.ellipse()["semi_minor_nm"] <= K.TRANSIT_SIGMA_NM + 1e-9


def test_the_noon_latitude_collapses_north_and_south_and_leaves_east_and_west():
    """Weighed by the two doubts (package 37e): the account moves toward the sight by the
    part its own doubt is of the two, north and south narrows to less than either, and
    east and west is left."""
    r = K.Reckoning(Position(49.0, -6.0), sigma_nm=0.0)
    for h in range(48):
        r.advance(1.0, math.pi / 2, 6.0, (h + 1) * 3600)
    east = r.sigma_east_nm
    north = r.sigma_north_nm
    assert north > 2.0
    obs = r.observe_latitude(49.05, 2.0)
    gain = north**2 / (north**2 + 2.0**2)
    assert obs.how == K.WEIGHED and obs.moved_nm == pytest.approx(3.0 * gain)
    assert r.lat_deg == pytest.approx(49.0 + 0.05 * gain)
    assert r.sigma_north_nm == pytest.approx(math.sqrt(north**2 * 4.0 / (north**2 + 4.0)))
    assert r.sigma_north_nm < min(north, 2.0)
    assert r.sigma_east_nm == pytest.approx(east)


def test_the_masters_words_and_the_ellipse():
    r = K.Reckoning(Position(49.5, -6.2), sigma_nm=1.0)
    assert r.words == "49° 30' N, 6° 12' W by account"
    assert r.uncertainty_words == (
        "I would not trust the reckoning within a mile east or west, nor a mile north or south."
    )
    r.P = [[400.0, 0.0], [0.0, 25.0]]
    assert r.uncertainty_words == (
        "I would not trust the reckoning within twenty miles east or west, nor five miles "
        "north or south."
    )
    e = r.ellipse()
    assert e["semi_major_nm"] == 20.0 and e["semi_minor_nm"] == 5.0
    assert e["major_bearing_deg"] == 90.0  # lying east and west
    d = r.to_dict()
    assert d["words"].endswith("by account") and "ellipse" in d and d["track"]
    assert "lat_deg" in d and "truth" not in str(d)


def test_the_doubt_is_said_in_cables_under_a_mile_and_with_its_lie_when_long_and_thin():
    """Package 37e, item 2. In game 9 the words said "a mile" for anything under a mile,
    so the master sounded the same at one cable as at nine; and a doubt long and thin
    along a sight was hidden by "east or west, north or south"."""
    r = K.Reckoning(Position(49.5, -6.2), sigma_nm=1.0)
    r.P = [[0.4**2, 0.0], [0.0, 0.07**2]]
    assert r.uncertainty_words == (
        "I would not trust the reckoning within four cables east or west, nor a cable north "
        "or south."
    )
    r.P = [[0.93**2, 0.0], [0.0, 0.96**2]]
    assert "within nine cables east or west, nor a mile north or south." in r.uncertainty_words
    # three miles NE and SW, a mile across
    a, b = 3.0, 1.0
    c, s_ = math.cos(math.radians(45.0)), math.sin(math.radians(45.0))
    r.P = [
        [a * a * s_ * s_ + b * b * c * c, (a * a - b * b) * s_ * c],
        [(a * a - b * b) * s_ * c, a * a * c * c + b * b * s_ * s_],
    ]
    assert r.uncertainty_words == (
        "I would not trust the reckoning within three miles NE and SW, nor a mile across."
    )
    assert r.ellipse()["major_bearing_deg"] == 45.0
    # lying NNW and SSE, and under a mile across
    lie = math.radians(150.0)
    c, s_ = math.cos(lie), math.sin(lie)
    a, b = 6.0, 0.5
    r.P = [
        [a * a * s_ * s_ + b * b * c * c, (a * a - b * b) * s_ * c],
        [(a * a - b * b) * s_ * c, a * a * c * c + b * b * s_ * s_],
    ]
    assert r.uncertainty_words == (
        "I would not trust the reckoning within six miles SSE and NNW, nor five cables across."
    )
    # not thin (under twice), or under a mile: east and west, north and south as before
    r.P = [[2.0, 0.9], [0.9, 2.0]]
    assert "east or west" in r.uncertainty_words
    r.P = [[0.3, 0.29], [0.29, 0.3]]
    assert "east or west" in r.uncertainty_words
    assert K.doubt_miles_words(0.04) == "a cable" and K.doubt_miles_words(12.4) == "ten miles"
    assert K.trust_words(0.83) == "within two miles" and K.trust_words(0.2) == "within four cables"


def test_the_seeded_errors_are_the_streams_and_within_the_studys_sizes():
    a = K.CompassErrors.draw(random.Random(7))
    b = K.CompassErrors.draw(random.Random(7))
    assert a == b
    assert K.LOG_LINE_SHORT_MIN <= a.log_line_short <= K.LOG_LINE_SHORT_MAX
    assert abs(a.deviation_b_deg) <= K.DEVIATION_MAX_DEG
    assert abs(a.leeway_bias_points) <= K.LEEWAY_ESTIMATE_ERROR_POINTS
    assert a.variation_error_deg == 2.5  # a decade's drift at a quarter of a degree
    # the deviation is by heading: the semicircular form
    n, e = a.deviation_deg(0.0), a.deviation_deg(math.pi / 2)
    assert n == pytest.approx(a.deviation_c_deg) and e == pytest.approx(a.deviation_b_deg)
    assert a.course_error_rad(0.0) == pytest.approx(math.radians(2.5 + a.deviation_c_deg))


def test_the_words_of_the_log_the_lead_and_the_ages():
    assert K.knots_words(6.5) == "six knots and a half"
    assert K.knots_words(7.25) == "seven knots and a quarter"
    assert K.knots_words(3.75) == "three knots and three quarters"
    assert K.knots_words(1.0) == "one knot" and K.knots_words(0.5) == "half a knot"
    assert K.knots_words(0.0) == "no way"
    assert K.chant(7.0, hand=True) == "By the mark seven"
    assert K.chant(9.0, hand=True) == "By the deep nine"
    assert K.chant(7.5, hand=True) == "And a half seven"
    assert K.chant(5.25, hand=True) == "And a quarter five"
    assert K.chant(4.75, hand=True) == "Quarter less five"
    assert K.chant(45.0, hand=False) == "Forty-five fathoms"
    assert K.chant(112.0, hand=False) == "A hundred and twelve fathoms"
    assert K.miles_words(131.4) == "131 miles" and K.miles_words(1.0) == "a mile"
    assert K.age_words(30) == "just now" and K.age_words(600) == "ten minutes ago"
    assert K.age_words(3600) == "an hour ago" and K.age_words(3 * 3600) == "three hours ago"
    assert K.age_words(2 * 86400) == "two days ago"
    assert K.number_words(45) == "forty-five" and K.number_words(120) == "a hundred and twenty"


# ---------------------------------------------------------------------------
# The World's glue
# ---------------------------------------------------------------------------


def test_the_log_is_hove_hourly_in_the_frigate_and_two_hourly_in_the_schooner():
    """Falconer 1780, 'Log': "once every hour in ships of war and East-Indiamen; and in
    all other vessels, once in two hours"; the read to a quarter knot with the line's
    marking (the ship overruns her reckoning); the account brought up at each heave."""
    frigate = chart_world(49.3, -5.5, heading=0.0, start=datetime(1805, 6, 10, 9, 0))
    frigate.submit("set plain sail")
    frigate.run(3 * 3600 + 60)
    heaves = [e for e in frigate.log if e.kind == "log.read"]
    assert [e.ship_time.strftime("%H:%M") for e in heaves] == ["10:00", "11:00", "12:00"]
    assert all(30 <= e.ship_time.second <= 45 for e in heaves)  # half a minute at the reel
    assert all(e.text.startswith("Hove the log: ") and e.text.endswith(".") for e in heaves)
    assert all(e.severity is Severity.ROUTINE and e.data["automatic"] for e in heaves)
    # the hourly heave says its one line: no "Hands to the log" of its own
    assert not [e for e in frigate.log if e.text == "Hands to the log."]
    read = heaves[-1].data["knots"]
    assert read == round(read * 4) / 4  # to the quarter knot
    stw = units.ms_to_knots(frigate.ship.dyn.u)
    assert read > stw * 1.0  # the line marked short: she overruns her reckoning
    assert frigate.navigation.log_interval_h == 1
    schooner = chart_world(
        49.3, -5.5, ship=SCHOONER, heading=0.0, start=datetime(1805, 6, 10, 9, 0)
    )
    schooner.submit("set plain sail")
    schooner.run(4 * 3600 + 60)
    assert schooner.navigation.log_interval_h == 2
    heaves = [e for e in schooner.log if e.kind == "log.read"]
    assert [e.ship_time.strftime("%H:%M") for e in heaves] == ["10:00", "12:00"]
    # the ordered heave says its start and the read, and is journaled
    e = schooner.submit("heave the log")
    assert e.kind == "order.accepted"
    schooner.run(60)
    assert [x for x in schooner.log if x.text == "Hands to the log."]
    assert len([e for e in schooner.log if e.kind == "log.read"]) == 3


def test_the_hand_lead_and_the_deep_sea_lead_cast_with_their_words_and_the_ground():
    """Luce 1884, ch. I 'The Lead'; Lever 1808: the hand lead to twenty fathoms from the
    chains with way on; the deep-sea lead with the line passed forward, wanting under
    four knots of way; "By the mark seven; fine grey sand with black specks."."""
    deep = chart_world(49.5, -5.2, heading=0.0)  # the Soundings: some fifty fathoms
    assert deep.submit("heave the lead").kind == "order.accepted"
    deep.run(120)
    casts = [e for e in deep.log if e.kind == "sounding"]
    assert len(casts) == 1 and casts[0].text == "No bottom at twenty fathoms."
    # routine since package 37f: a cast that finds no bottom is the watch's work, and
    # `a sounding` is bottom found (tests/test_log_lines.py)
    assert casts[0].severity is Severity.ROUTINE
    assert deep.readings["depth"] is None
    assert deep.readings.words("depth").startswith("no bottom by the last cast")
    # the deep-sea lead with no way on her: a cast, the fathoms, the ground
    assert deep.submit("heave the deep-sea lead").kind == "order.accepted"
    deep.run(20 * 60)
    started = [e for e in deep.log if e.kind == "evolution.started"]
    assert any(e.text.startswith("Pass the deep-sea line forward") for e in started)
    casts = [e for e in deep.log if e.kind == "sounding"]
    assert len(casts) == 2
    assert " fathoms; fine grey sand with black specks. The account " in casts[-1].text
    assert casts[-1].data["deep"] is True and 40 < casts[-1].data["fathoms"] < 65
    r = deep.readings
    assert 40 < units.m_to_fathoms(r["depth"]) < 65
    assert r.words("depth").endswith("fathoms") or "and a half" in r.words("depth")
    assert r["ground"]["words"] == "fine grey sand with black specks"
    assert r.words("ground").startswith("fine grey sand with black specks, by the cast ")
    # with way on her the deep-sea lead does not get bottom
    deep.submit("set plain sail")
    deep.run(1200)
    assert units.ms_to_knots(deep.ship.dyn.u) > K.DEEP_SEA_LEAD_MAX_KN
    deep.submit("heave the deep-sea lead")
    deep.run(20 * 60)
    last = [e for e in deep.log if e.kind == "sounding"][-1]
    assert last.text.startswith("The deep-sea lead would not get bottom")
    # the hand lead in Falmouth's mouth: the leadsman's chant, the pilot's ground
    shoal = chart_world(50.12, -5.03, heading=0.0)
    shoal.submit("heave the lead")
    shoal.run(120)
    cast = [e for e in shoal.log if e.kind == "sounding"][-1]
    head = cast.text.split(";")[0]
    assert head.startswith(
        ("By the mark", "By the deep", "And a half", "And a quarter", "Quarter less")
    )
    assert 8 < cast.data["fathoms"] < 25
    assert cast.data["ground"] and cast.data["ground"] in cast.text


def test_a_sounding_moves_the_account_onto_the_charts_contour_consistent_with_the_ground():
    """Spec M5 §13: the reckoning moves onto the nearest point of the chart's depth
    contour consistent with the ground, and the across-contour doubt shrinks to a few
    miles while along it stays."""
    w = chart_world(49.70, -5.20, heading=0.0)  # forty-six fathoms
    nav = w.navigation
    truth_depth = w.chart.depth_at(w.position)
    # the master's account is nineteen miles off, in the shoal water under the
    # Manacles, and he knows he is in doubt
    nav.reckoning.set_position(Position(50.0, -5.10), 0, sigma_nm=8.0)
    w.submit("heave the deep-sea lead")
    w.run(20 * 60)
    cast = [e for e in w.log if e.kind == "sounding"][-1]
    assert cast.data["matched"] and cast.data["moved_nm"] > 0.5
    r = nav.reckoning
    depth_at_account = w.chart.depth_at(r.position)
    # the lead reads the tide (package 34): the master lays his cast on the chart less
    # his own allowance for it, by his almanac
    cast_on_the_chart = cast.data["depth_m"] - nav._tide_allowance_m()
    # Package 37e: the cast is a line as good as the bottom is steep, weighed against the
    # account by their two doubts. Here the bottom shelves half a fathom in a mile, the
    # line is good to four or five miles, and the account, eight miles in doubt, goes
    # most of the way to it: nearer the cast's depth than it stood, and the words say so
    # (package 37j: the cast reduced by the master's tide above his chart's datum, the
    # line six miles and a tenth at this seed)
    assert cast.data["how"] == K.WEIGHED and 1.0 < cast.data["line_sigma_nm"] < 7.0
    assert "; fine grey sand with black specks. The account moved " in cast.text
    assert " to the SE" in cast.text or " to the SSE" in cast.text  # toward the deep water
    shoal = w.chart.depth_at(Position(50.0, -5.10))
    assert abs(depth_at_account - cast_on_the_chart) < 0.5 * abs(shoal - cast_on_the_chart)
    # within nine fathoms of the truth: the lead's error and the master's allowance for
    # the tide (package 34), which is by his almanac and not the world's
    assert abs(depth_at_account - truth_depth) < units.fathoms_to_m(9.0)
    assert truth_depth is not None
    # a sounding is a line, not a point (N §3): the account is nearer the truth than it
    # was, and still along the contour from it
    before = miles_between(Position(50.0, -5.10), w.position)
    assert miles_between(r.position, w.position) < before
    e = r.ellipse()
    assert e["semi_minor_nm"] < 5.0  # "a band a few miles wide" (N §3)
    assert e["semi_major_nm"] > 6.0  # along the contour it stays as it was


def test_a_bearing_of_a_mark_in_sight_and_the_refusals_in_words():
    w = chart_world(49.80, -5.20, heading=0.0)  # ten miles south of the Lizard
    w.run(60)
    assert w.readings["land"]["in_sight"]
    e = w.submit("take a bearing of the Lizard")
    assert e.kind == "bearing.taken"
    assert e.text.startswith("The Lizard bore ") and " by estimation: the account " in e.text
    assert e.data["how"] in (K.TAKEN, K.WEIGHED, K.KEPT)  # the words say which (37e)
    assert e.data["id"] == "lizard-point" and "reckoning" in e.data
    assert len(w.navigation.reckoning.bearings) == 1
    assert [x for x in w.log if x.kind == "bearing.taken"] == [e]  # said once
    # the land, and the mark by its modern name
    assert w.submit("take a bearing of the land").kind == "bearing.taken"
    assert w.submit("take a bearing of Lizard Point").kind == "bearing.taken"
    refused = w.submit("take a bearing of the Eddystone")
    assert refused.kind == "order.rejected" and "not in sight" in refused.text
    offing = chart_world(49.0, -6.5, heading=0.0)
    offing.run(60)
    refused = offing.submit("take a bearing of the land")
    assert "Nothing is in sight" in refused.text
    # the reading, parametric by the mark
    r = w.readings
    bearing = r.value("bearing_of", "the Lizard")
    assert bearing is not None and abs(units.wrap_pi(bearing - 0.0)) < math.radians(20)
    assert r.value("bearing_of", "the Eddystone") is None
    assert r.words("bearing_of", "the Eddystone") == "not in sight"


def test_the_bearing_is_by_compass_and_carries_the_ships_errors():
    """The master lays a bearing down as he reads it, with the chart's variation error
    and the deviation on her heading (N §3); the lookout's bearing is the truth's."""
    w = chart_world(49.80, -5.20, heading=0.0)
    w.run(60)
    e = w.submit("take a bearing of the Lizard")
    sighting = w.lookout.find("the Lizard")
    laid = e.data["bearing_deg"]
    error = math.degrees(units.wrap_pi(math.radians(laid - sighting.bearing_deg)))
    expected = math.degrees(w.navigation.errors.course_error_rad(0.0))
    assert abs(error - expected) < 3 * K.BEARING_SIGMA_DEG


def test_the_noon_the_days_work_and_the_readings_since_noon():
    w = chart_world(49.4, -5.3, heading=0.0, start=datetime(1805, 6, 10, 11, 30))
    w.submit("set plain sail")
    r = w.readings
    assert r["run_since_noon"] is None and r.words("run_since_noon").startswith("no noon yet")
    assert r["latitude_by_observation"] is None
    assert r.words("latitude_by_observation").startswith(
        "No sight yet today; noon by the sun is at"
    )
    w.run(3600)
    noons = [e for e in w.log if e.kind == "reckoning.noon"]
    assert len(noons) == 1
    text = noons[0].text
    assert text.startswith("Noon. Latitude by observation ") and "the reckoning was" in text
    assert "Longitude by account " in text and "' W. The day's work carried the master's " in text
    assert text.endswith("tide by the directions and the epitome.")  # whose tide (37e)
    assert noons[0].severity is Severity.NOTABLE
    transit = w.navigation.noon_by_the_sun()
    # to the minute: the transit is read at her easting, which the stream has moved a
    # few hundred metres since the master fixed his noon (package 34)
    assert abs((noons[0].ship_time - transit).total_seconds()) < 60
    # the master on deck for the sight, then below at the day's work, then on deck again
    places = [e for e in w.log if e.kind == "master.place"]
    assert places and places[-1].text.endswith("came on deck, the day's work done.")
    r = w.readings
    assert r["latitude_by_observation"] is not None
    assert abs(r["latitude_by_observation"]["lat_deg"] - w.position.lat_deg) < 8.0 / 60.0
    assert r.words("latitude_by_observation").endswith("' N")
    assert r["run_since_noon"] is not None and r["run_since_noon"]["metres"] > 0
    assert r["course_made_good"] is not None
    assert r.words("course_made_good").startswith("N")
    assert r.words("master").startswith("Mr ") and "on deck" in r.words("master")
    # by order after noon the sight is not taken twice
    e = w.submit("observe the sun")
    assert e.kind == "reckoning.sight" and e.text.startswith("The sun was observed at noon")
    assert len([e for e in w.log if e.kind == "reckoning.noon"]) == 1


def test_work_up_set_and_allow_and_shape_a_course_read_the_account_not_the_truth():
    w = chart_world(49.4, -5.3, heading=0.0)
    w.submit("set plain sail")
    w.run(2 * 3600)
    e = w.submit("work up the reckoning")
    assert e.kind == "reckoning.worked" and "by account" in e.text
    assert "north or south. The tide allowed: the " in e.text and e.data["tide"]["by"] == "book"
    e = w.submit("set the reckoning to 49 30 N 5 10 W")
    assert e.kind == "reckoning.set" and e.text.endswith("by the captain's order.")
    assert w.readings["reckoning"]["position"] == "49° 30' N, 5° 10' W by account"
    assert w.readings["reckoning"]["words"].startswith(
        "49° 30' N, 5° 10' W by account; the tide allowed: the "
    )
    e = w.submit("allow one knot of set to the east")
    assert e.kind == "reckoning.set_allowance" and e.text.startswith("Allowing one knot of set")
    assert w.submit("allow no set").text.startswith(
        "No set allowed for in the reckoning, by the captain's order"
    )
    e = w.submit("shape a course for Falmouth")
    assert e.kind == "helm.set" and e.text.startswith("Shaped a course for Falmouth: ")
    # from 49 30 N 5 10 W, Falmouth lies a little east of north: the truth is elsewhere
    falmouth = next(f for f in w.chart.features.values() if f.name == "Falmouth")
    wanted, _ = bearing_and_distance(Position(49.5, -5.1667), falmouth.position)
    assert abs(math.degrees(e.data["heading"]) - wanted) < 1.0
    assert abs(units.wrap_pi(w.ship.dyn.target_heading - math.radians(wanted))) < math.radians(1)
    refused = w.submit("shape a course for Timbuctoo")
    assert refused.kind == "order.rejected" and "no place named" in refused.text
    refused = w.submit("set the reckoning to somewhere warm")
    assert "not a position" in refused.text


def test_the_orders_are_refused_in_words_on_the_plane():
    plain = make_world(7, FRIGATE, Scenario(gustiness=0.0, variability=0.0))
    for text in ("heave the log", "heave the lead", "work up the reckoning", "observe the sun"):
        e = plain.submit(text)
        assert e.kind == "order.rejected" and "No reckoning is kept" in e.text, text
    r = plain.readings
    for rid in ("reckoning", "reckoning_uncertainty", "depth", "ground", "master"):
        assert r[rid] is None and r.words(rid) == R.NO_RECKONING_WORDS, rid
    assert plain.navigation is None


def test_the_dialect_reads_the_new_rows_for_nothing():
    """Spec M5 §15: `when the depth is under 40 fathoms then heave the lead every glass`
    is a book's line; the new kinds (a position, a distance, the ground, a person) are
    the standing grammar's."""
    from freesail.standing.grammar import parse_condition, parse_standing

    w = chart_world(49.5, -5.2, heading=0.0)
    w.submit("heave the deep-sea lead")
    w.run(20 * 60)
    for text, holds in (
        ("the depth is under 60 fathoms", True),
        ("the depth exceeds 60 fathoms", False),
        ("the ground is sand", True),
        ("the ground is not rock", True),
        ("the reckoning is north of 49 N", True),
        ("the reckoning is south of 49 30 N", False),
        ("the reckoning is west of 5 W", True),
        ("the reckoning's uncertainty is under 20 miles", True),
        ("the master is on deck", True),
        ("the master is below", False),
    ):
        c = parse_condition(text, w.ship)
        assert c.holds(w.readings, {}) is holds, text
    rule = parse_standing(
        w.ship, 'standing order "x": when the depth is under 40 fathoms then heave the lead'
    )
    assert rule.trigger.kind == "when" and rule.actions == ["heave the lead"]
    rule = parse_standing(w.ship, 'standing order "y": at a sounding then fill away')
    assert rule.trigger.event == "a sounding"
    rule = parse_standing(w.ship, 'standing order "z": at noon then work up the reckoning')
    assert rule.trigger.event == "noon"
    with pytest.raises(OrderError, match="cannot be"):
        parse_condition("the reckoning is shaking", w.ship)
    with pytest.raises(OrderError, match="what latitude"):
        parse_condition("the reckoning is north of", w.ship)


def test_the_captains_chart_carries_the_account_and_never_the_truth():
    """Spec M5 §17: the snapshot carries the reckoned position and its ellipse, the
    track by account, the noons, the bearings and the soundings, and no longer the
    truth."""
    from freesail.api import queries

    w = chart_world(49.80, -5.20, heading=0.0, start=datetime(1805, 6, 10, 11, 30))
    w.submit("set plain sail")
    w.run(3600)
    w.submit("take a bearing of the Lizard")
    w.submit("heave the deep-sea lead")
    w.run(60)
    snap = queries.snapshot(w)
    assert "position" not in snap
    assert snap["ship"]["x"] is None and snap["ship"]["y"] is None
    block = snap["reckoning"]
    assert " by account; the tide allowed: " in block["words"]
    assert block["uncertainty"].startswith("I would not") and block["tide"]["by"] == "book"
    assert block["ellipse"]["semi_major_nm"] > 0
    assert len(block["track"]) >= 2 and len(block["noons"]) == 1 and len(block["bearings"]) == 1
    assert block["master"]["name"].startswith("Mr ")
    account = Position(block["lat_deg"], block["lon_deg"])
    truth = w.position
    assert account != truth
    text = str(snap)
    assert f"{truth.lat_deg:.5f}" not in text and f"{truth.lon_deg:.5f}" not in text
    # the truth is in the save and the state for the tests, as before
    assert w.state()["position"] == truth.to_dict()
    lines = w.summary_lines()
    assert any(line.endswith("north or south.") for line in lines)


def test_the_same_seed_gives_the_same_account_and_a_replay_the_same_digest():
    from freesail.api.session import ship_factory
    from freesail.core import replay as replay_mod

    def passage() -> World:
        w = chart_world(49.4, -5.3, heading=10.0, start=datetime(1805, 6, 10, 11, 0))
        w.submit("set plain sail")
        w.run(2 * 3600)
        w.submit("heave to")
        w.run(600)
        w.submit("heave the deep-sea lead")
        w.run(20 * 60)
        return w

    a, b = passage(), passage()
    assert a.log.digest() == b.log.digest()
    assert a.navigation.reckoning.to_dict() == b.navigation.reckoning.to_dict()
    copy = replay_mod.replay(a.save(), ship_factory)
    assert copy.log.digest() == a.log.digest()
    assert copy.navigation.reckoning.words == a.navigation.reckoning.words
    # another seed: other errors, another account
    other = make_world(
        8,
        FRIGATE,
        Scenario(
            start_time=datetime(1805, 6, 10, 11, 0),
            wind_from_deg=225.0,
            wind_speed_kn=12.0,
            gustiness=0.0,
            variability=0.0,
            ship_heading_deg=10.0,
            position={"lat_deg": 49.4, "lon_deg": -5.3},
            region=REGION,
        ),
    )
    assert other.navigation.errors != a.navigation.errors


def test_the_shore_close_aboard_is_hailed_in_thick_weather_and_is_no_mark():
    """Package 33a: in a mile of fog the cliffs are seen before any named mark; the
    reading `the land` counts them, and a bearing of them is refused."""
    from freesail.world.lookout import SHORE_ID

    w = chart_world(50.0, -5.19, heading=0.0)  # two miles east of the Lizard's cliffs
    w.lookout.sightings = []
    w.lookout._announced = {}
    lines = w.lookout.look(w)
    ids = {s.feature.id for s in w.lookout.sightings}
    # the shore itself is a sighting beside the headland (package 37d: until then it was
    # hailed only when no headland of the chart was in sight)
    assert "lizard-point" in ids and SHORE_ID in ids
    # nothing in sight but the shore: a point of the coast with no mark within the fog
    from freesail.world.chart import Sighting

    w.lookout.sightings = [
        Sighting(w.chart.feature("lizard-point"), 0.0, 3000.0, "land"),
    ]
    assert w.lookout.find("the land").feature.id == "lizard-point"
    shore = w.lookout._shore_close_aboard(Position(50.0, -5.19), 1.0, "day")
    assert shore is None or shore.distance_m <= units.NAUTICAL_MILE
    close = w.lookout._shore_close_aboard(Position(49.975, -5.205), 1.0, "day")
    assert close is not None and close.feature.id == SHORE_ID and close.seen_as == "land"
    assert w.lookout.words(close, 0.0).startswith("The land about ")
    assert "close aboard" in w.lookout.words(close, 0.0)
    w.lookout.sightings = [close]
    assert w.readings["land"]["in_sight"] is True
    assert w.lookout.find("the land") is None
    assert lines is not None


# ---------------------------------------------------------------------------
# Package 37d: a bearing gives a line, a sail is no mark, and `take a fix` (the review of
# gate 5c's playtests, 5.1: "every bearing writes that held distance into the account")
# ---------------------------------------------------------------------------

FALMOUTH_BAY = (50.08, -4.95)  # five miles off the Manacles and St Anthony's, by day


def bay_world(seed: int = 7, **kw) -> World:
    return chart_world(*FALMOUTH_BAY, seed=seed, start=datetime(1805, 6, 12, 10, 0), **kw)


def no_compass_error(w: World) -> None:
    """A compass with no error the master cannot know, so a line's own doubt is all."""
    errors = w.navigation.errors
    errors.deviation_b_deg = errors.deviation_c_deg = 0.0
    errors.variation_error_deg = 0.0


def account_out(w: World, miles: float = 10.0, toward: float = 135.0, sigma: float = 3.0) -> None:
    w.navigation.reckoning.set_position(
        destination(w.position, toward, miles * units.NAUTICAL_MILE), w.clock.tick, sigma_nm=sigma
    )


def test_a_landfall_on_one_mark_lays_the_account_down_by_the_bearing_and_its_distance():
    """Package 37d's item 6 under 37e's one rule: a bearing and distance of a headland is
    the period's ordinary way to make a landfall, and with one mark in sight it is all
    the master has along the line. After a long run, the account leagues out and three
    miles in doubt, the bearing's line and the lookout's distance are each weighed
    against it by their doubts, and being much the better figures bring it nearly all
    the way; the words say how far and which way it moved."""
    w = bay_world()
    no_compass_error(w)
    nav = w.navigation
    mark = w.lookout.find("St Anthony's Head")
    account_out(w)  # ten miles out, three miles in doubt: the poorer figure
    e = w.submit("take a bearing of St Anthony's Head")
    assert e.kind == "bearing.taken" and e.data["distance_applied"] is True
    assert e.data["how"] == K.WEIGHED and e.data["distance"] == K.WEIGHED
    after = nav.reckoning.position
    laid = e.data["bearing_deg"]
    back, account_m = bearing_and_distance(after, mark.feature.position)
    # on the line, to a degree and a half (the distance weighed after it moves the account
    # along the sight from where the line put it; 1.2 degrees at this seed since 37j)
    assert abs(units.wrap_pi(math.radians(back - laid))) < math.radians(1.5)
    # within the estimate's own error of the lookout's distance: the eye's sixth is the
    # better figure by far, and the account went nine parts in ten of the way to it
    assert abs(account_m - mark.estimate_m) < K.DISTANCE_BY_ESTIMATION_FRACTION * mark.estimate_m
    assert miles_between(after, w.position) < 2.5
    assert e.text.startswith(
        f"St Anthony's Head bore {units.point_name(math.radians(laid))}, {e.data['estimate']} "
        "by estimation: the account moved "
    )
    assert e.text.endswith(f" to the {e.data['moved_toward']}.") and e.data["moved_nm"] > 7.0
    assert e.data["differs"] is False and "by the account" not in e.text
    # it was weighed in, not put in the account's place: the doubt along the sight is now
    # under the estimate's own, and the account is the better figure
    sigma = K.DISTANCE_BY_ESTIMATION_FRACTION * mark.estimate_m / units.NAUTICAL_MILE
    assert nav.reckoning.ellipse()["semi_major_nm"] < sigma


def test_six_bearings_of_one_mark_lay_the_distance_down_once_and_the_account_does_not_creep():
    """Package 37e, item 2: the same thing seen again tells him nothing new. The eye's
    error is the sighting's own, the same each time the mark is looked at, so once the
    distance has been weighed in a second estimate of it is not applied; the old fault
    (every bearing a fix by a poor distance, the master ever surer of the wrong place)
    cannot come back, the account does not creep along the line, and its doubt is no
    smaller for six bearings than for two."""
    w = bay_world()
    no_compass_error(w)
    nav = w.navigation
    mark = w.lookout.find("St Anthony's Head")
    account_out(w)
    applied, distances, doubts = [], [], []
    for _ in range(6):
        e = w.submit("take a bearing of St Anthony's Head")
        applied.append(e.data["distance_applied"])
        distances.append(bearing_and_distance(nav.reckoning.position, mark.feature.position)[1])
        doubts.append(nav.reckoning.ellipse()["semi_minor_nm"])
    assert applied == [True, False, False, False, False, False]
    assert max(distances) / min(distances) < 1.03
    assert e.text.endswith(" by estimation: the account kept.") and e.data["moved_nm"] < 0.05
    assert e.data["how"] == K.KEPT and e.data["line"] == K.KEPT
    # the second bearing may still better the first by its own draw; after it, nothing
    assert doubts[2:] == [doubts[2]] * 4
    # and never below the compass's own error in a bearing at that distance
    shared = mark.distance_m / units.NAUTICAL_MILE * math.tan(math.radians(K.COMPASS_ALLOWANCE_DEG))
    assert doubts[-1] >= 0.9 * shared


def test_after_a_fix_bearings_of_two_marks_whose_estimates_err_opposite_ways_move_nothing_along():
    """Package 37d's item 6 under 37e's one rule: in pilot water just after a fix the
    account is the better figure by far, so a distance by estimation weighed against it
    hardly moves it, and the account does not jump between two marks whose distances the
    eye has wrong by a third and more either way. A distance by estimation is the eye's
    guess and is never taken, however far it stands from the account; each line says the
    estimate and, differing by a third, the account's own distance."""
    from dataclasses import replace

    w = bay_world()
    no_compass_error(w)
    nav = w.navigation
    assert w.submit("take a fix").kind == "reckoning.fix"
    fixed = nav.reckoning.position
    wrong = {"St Anthony's Head": 1.6, "the Deadman": 0.6}
    w.lookout.sightings = [
        replace(s, estimate_m=s.distance_m * wrong[s.feature.name])
        if s.feature.name in wrong
        else s
        for s in w.lookout.sightings
    ]
    for name in ("St Anthony's Head", "the Deadman", "St Anthony's Head", "the Deadman"):
        e = w.submit(f"take a bearing of {name}")
        assert e.data["distance"] != K.TAKEN and "laid down" not in e.text
        assert (" by the account: the account " in e.text) is e.data["differs"]
        assert miles_between(nav.reckoning.position, fixed) < 0.5
    assert e.data["differs"] is True
    assert e.data["how"] == K.KEPT and e.text.endswith(": the account kept.")
    assert miles_between(nav.reckoning.position, w.position) < 0.7


def test_a_bearing_of_a_sail_moves_nothing():
    """Item 7: a sail is no mark. Her bearing is given in words and data and the account
    stands (on the Harpy one bearing of a pilot's boat moved it ten miles); her place,
    which is the truth's, is in no data and on no chart."""
    from freesail.world.chart import Feature, Sighting

    w = bay_world()
    nav = w.navigation
    account_out(w)
    before = nav.reckoning.position
    cov = [row[:] for row in nav.reckoning.P]
    sail = Feature("sail:brig-1", "sail", "a sail", 50.0, -4.9, modern="brig-1")
    w.lookout.sightings = [Sighting(sail, 170.0, 9000.0, "sail", 8000.0)] + w.lookout.sightings
    e = w.submit("take a bearing of the sail")
    assert e.kind == "bearing.taken" and e.text.startswith("A sail bore S")
    assert e.text.endswith(" by estimation.") and "the account" not in e.text
    assert e.data["sail"] is True and e.data["moved_nm"] == 0.0
    assert "distance_applied" not in e.data and "laid down" not in e.text  # never for a sail
    assert "mark_lat_deg" not in e.data and "mark_lon_deg" not in e.data
    assert nav.reckoning.position == before and nav.reckoning.P == cov
    assert nav.reckoning.bearings == []


def test_a_fix_by_two_marks_at_right_angles_brings_the_account_to_the_truth():
    """Package 37d's item 8 under 37e's one rule: two marks at right angles bring an
    account ten miles out to within the lines' doubt of the truth. The account is
    plainly out, so the fix is taken: the account is laid on it and its doubt becomes
    the fix's own, whatever it was before."""
    w = bay_world()
    no_compass_error(w)
    nav = w.navigation
    marks = {s.feature.name: s for s in nav._fix_marks()}
    a, b = marks["St Anthony's Head"], marks["the Deadman"]
    cut = abs(a.bearing_deg - b.bearing_deg) % 180.0
    assert 60.0 < min(cut, 180.0 - cut) <= 90.0
    account_out(w)
    e = w.submit("take a fix by St Anthony's Head and the Deadman")
    assert e.kind == "reckoning.fix" and e.severity is Severity.NOTABLE  # it moved over a mile
    assert e.data["how"] == K.TAKEN
    assert [m["name"] for m in e.data["marks"]] == ["St Anthony's Head", "the Deadman"]
    off = miles_between(nav.reckoning.position, w.position)
    # each line good to a degree and a half at its mark's distance: three sigma of the two
    doubt = math.hypot(K._bearing_sigma_nm(a.distance_m), K._bearing_sigma_nm(b.distance_m))
    assert off < 3.0 * doubt < 1.5
    ellipse = nav.reckoning.ellipse()
    assert ellipse["semi_major_nm"] < 0.6 and e.data["sigma_nm"] < 0.6
    assert e.data["hat_m"] is None and 9.0 < e.data["moved_nm"] < 11.0
    assert e.data["moved_toward"] == "NW"
    first, second = (f"{m['name']} {m['bearing']}" for m in e.data["marks"])
    assert e.text.startswith(f"Fixed by cross bearings: {first}, {second}; the lines cut at ")
    assert (
        " degrees. The reckoning was out by it; laid down by the fix: moved three leagues and "
        "a half to the NW: " in e.text
    )
    assert e.text.endswith(" by the fix, good to " + e.text.rsplit("good to ", 1)[1])
    assert f"{format_position(nav.reckoning.position)} by the fix" in e.text
    # the chart has the lines, the track the fix
    assert [x.feature_id for x in nav.reckoning.bearings] == [a.feature.id, b.feature.id]
    assert nav.reckoning.track[-1][1:] == (nav.reckoning.lat_deg, nav.reckoning.lon_deg)
    # taken again from where she is, the account hardly moves and the line is routine
    e = w.submit("take a fix by St Anthony's Head and the Deadman")
    assert e.severity is Severity.ROUTINE and e.data["moved_nm"] < 1.0
    assert e.data["how"] in (K.WEIGHED, K.KEPT)
    # the compass's own error, which the master cannot know, is common to the set: the
    # fix is out by it and still within a mile at five miles from the marks
    other = bay_world()
    account_out(other)
    other.submit("take a fix by St Anthony's Head and the Deadman")
    assert miles_between(other.navigation.reckoning.position, other.position) < 1.0


def test_a_fix_by_three_marks_says_the_cocked_hat_and_the_master_chooses_those_that_cut_best():
    """Package 37d's item 8 with 37e's item 3: unnamed, the master takes the two or three
    marks whose fix has the least doubt, of which some two lines cut by thirty degrees or
    more; with three the cocked hat's size is said and the doubt is no smaller than half
    of it."""
    w = bay_world()
    nav = w.navigation
    account_out(w)
    near = nav._fix_marks()[: K.FIX_MARKS_CONSIDERED]
    e = w.submit("take a fix")
    assert e.kind == "reckoning.fix" and len(e.data["marks"]) == 3 and e.data["by"] == []
    chosen = [w.lookout.find(m["name"]) for m in e.data["marks"]]
    assert K._best_cut_deg(chosen) >= K.FIX_MIN_CUT_DEG
    # no two or three of the marks he considered would fix her better
    from itertools import combinations

    allow = nav.compass_allowance_deg()
    best = min(
        K._fix_doubt_nm(g, allow)
        for n in (2, 3)
        for g in combinations(near, n)
        if K._best_cut_deg(list(g)) >= K.FIX_MIN_CUT_DEG
    )
    assert K._fix_doubt_nm(chosen, allow) == pytest.approx(best, abs=1e-4)
    assert e.data["hat_m"] is not None and "; the lines met " in e.text
    assert e.data["sigma_nm"] * units.NAUTICAL_MILE >= 0.5 * e.data["hat_m"] - 10.0
    assert miles_between(nav.reckoning.position, w.position) < 1.0
    names = ", ".join(f"{m['name']} {m['bearing']}" for m in e.data["marks"])
    assert e.text.startswith(f"Fixed by cross bearings: {names}; the lines met ")
    # three named, by the seaman's other words, with no commas left by the grammar
    account_out(w)
    e = w.submit("take cross bearings of Black Head, St Anthony's Head and the Deadman")
    assert e.kind == "reckoning.fix"
    assert e.data["by"] == ["Black Head", "St Anthony's Head", "the Deadman"]
    assert [m["name"] for m in e.data["marks"]] == e.data["by"]
    assert w.submit("fix her position").kind == "reckoning.fix"


def test_a_fix_is_refused_in_words_that_carry_the_cure():
    """Item 8: nothing in sight; one mark only, named, with `take a bearing of` it; marks
    that cut too fine, named, with how they bear from one another; a sail and the shore
    refused or passed over; a transit no mark."""
    from freesail.world.chart import Feature, Sighting
    from freesail.world.lookout import SHORE_ID

    w = bay_world()
    nav = w.navigation
    before = nav.reckoning.position
    marks = {s.feature.name: s for s in nav._fix_marks()}
    fine = w.submit("take a fix by Pendennis castle and Pendennis Point")
    assert fine.kind == "order.rejected"
    assert "Pendennis castle and Pendennis Point cut too fine for a fix: they bear " in fine.text
    assert "a fix wants 30" in fine.text and "Take a bearing of one for a line" in fine.text
    one = w.submit("take a fix by Black Head")
    assert "One mark gives a line and no fix: name a second with Black Head, or take a " in one.text
    assert "bearing of Black Head" in one.text
    absent = w.submit("take a fix by Black Head and the Eddystone")
    assert absent.kind == "order.rejected" and "not in sight" in absent.text
    # a sail named is refused; unnamed, a sail and the shore are passed over
    sail = Feature("sail:brig-1", "sail", "a sail", 50.0, -4.9, modern="brig-1")
    shore = Feature(SHORE_ID, "headland", "the land about Black Head", 50.0, -5.0)
    sightings = list(w.lookout.sightings)
    w.lookout.sightings = [
        Sighting(sail, 170.0, 900.0, "sail", 900.0),
        Sighting(shore, 250.0, 1000.0, "land", 1000.0),
        marks["Black Head"],
    ]
    refused = w.submit("take a fix by the sail and Black Head")
    assert "A sail is no mark for a fix" in refused.text
    alone = w.submit("take a fix")
    assert (
        "Only Black Head is in sight, and one mark gives a line and no fix: take a " in alone.text
    )
    w.lookout.sightings = w.lookout.sightings[:2]
    none = w.submit("take a fix")
    assert "No charted mark is in sight to take a fix by" in none.text
    w.lookout.sightings = []
    assert "Nothing is in sight to take a fix by" in w.submit("take a fix").text
    # two marks in one line of bearing, unnamed: too fine, with how they bear
    w.lookout.sightings = [marks["Pendennis castle"], marks["Pendennis Point"]]
    assert "cut too fine for a fix" in w.submit("take a fix").text
    w.lookout.sightings = sightings
    assert nav.reckoning.position == before and nav.reckoning.bearings == []


def test_two_worlds_of_one_seed_say_the_same_fix_and_another_seed_another():
    """Item 8: each mark's own draw comes from the reckoning's stream in the order the
    marks are said, so the same seed says the same words."""
    said = []
    for seed in (7, 7, 8):
        w = bay_world(seed=seed)
        account_out(w)
        e = w.submit("take a fix by St Anthony's Head, Black Head and the Deadman")
        assert e.kind == "reckoning.fix"
        said.append((e.text, e.data["lat_deg"], e.data["lon_deg"]))
    assert said[0] == said[1] and said[2] != said[0]


def test_the_standing_dialect_has_take_a_fix_for_nothing():
    """Item 8: `every glass then take a fix` parses and fires; `at a fix` is an event."""
    w = bay_world()
    account_out(w)
    given = w.submit('standing order "fix": every glass then take a fix')
    assert given.kind == "standing.given", given.text
    w.run(1801)
    fixes = [e for e in w.log if e.kind == "reckoning.fix"]
    assert len(fixes) == 1 and fixes[0].actor == "standing order 'fix'"
    assert R.event_matches(R.EVENTS["a fix"], fixes[0].kind, fixes[0].data)
    assert miles_between(w.navigation.reckoning.position, w.position) < 1.5


# ---------------------------------------------------------------------------
# Package 37e: the account. One rule for every observation; the doubt, honest; the fix by
# the marks that fix her best; the account hove to and becalmed; the master's own tide in
# the traverse; a shaped course that makes good. From the review of gate 5c's playtests,
# section 10 (the owner's game 9); the figures of the tests named for it are the game's
# own, from evidence/G9-brig-m5cc-measurements.txt beside the review.
# ---------------------------------------------------------------------------

BRIG = "data/ships/brig.yaml"
IROISE = (48.17, -5.10)  # the fifty-fathom sand off Ar Men, where game 9 lay becalmed


def at_rest(
    lat: float,
    lon: float,
    start: datetime = datetime(1805, 6, 15, 13, 0),
    ship: str = BRIG,
    **kw,
) -> World:
    """A ship with no sail set in a calm: she has no way, and goes where the water goes.
    (From one in the afternoon unless said, so that no noon sight falls in the test.)"""
    sc = Scenario(
        start_time=start,
        wind_from_deg=225.0,
        wind_speed_kn=0.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=0.0,
        position={"lat_deg": lat, "lon_deg": lon},
        region=REGION,
        **kw,
    )
    return make_world(7, ship, sc)


def pricked(pos: Position) -> str:
    """A point as the books prick it on the chart: '48 20.10 N 4 36.90 W'."""
    lat, lon = abs(pos.lat_deg), abs(pos.lon_deg)
    ns, ew = ("N" if pos.lat_deg >= 0 else "S"), ("E" if pos.lon_deg >= 0 else "W")
    lat_min, lon_min = (lat - int(lat)) * 60.0, (lon - int(lon)) * 60.0
    return f"{int(lat)} {lat_min:.2f} {ns} {int(lon)} {lon_min:.2f} {ew}"


def error_nm(w: World) -> float:
    return miles_between(w.position, w.navigation.account_now())


# -- item 1: one rule for every observation -------------------------------------------------


def test_one_rule_an_observation_is_weighed_by_the_two_doubts_whatever_the_run():
    """Item 1. An observation is weighed against the account by their two doubts,
    whatever the run since the last one: `FIX_RUN_NM` and the run's part in the rule are
    gone (the run is still counted, and nothing in the rule reads it)."""
    assert not hasattr(K, "FIX_RUN_NM") and not hasattr(K.Reckoning, "weigh_line")
    moved = []
    for run in (0.0, 50.0):
        r = K.Reckoning(Position(49.0, -6.0), sigma_nm=1.0)
        r.run_since_fix_nm = run
        obs = r.observe_line(0.0, 1.0, 0.0, 1.0, 1.0)  # a mile off, as good as the account
        assert obs.how == K.WEIGHED and obs.moved_nm == pytest.approx(0.5)
        assert obs.toward_deg == pytest.approx(0.0)
        assert r.sigma_north_nm == pytest.approx(math.sqrt(0.5))
        assert r.sigma_east_nm == pytest.approx(1.0) and r.run_since_fix_nm == 0.0
        moved.append((obs.moved_nm, r.lat_deg))
    assert moved[0] == moved[1]
    # a poor figure against a good account: weighed, and the account kept
    r = K.Reckoning(Position(49.0, -6.0), sigma_nm=1.0)
    obs = r.observe_line(0.0, 3.0, 0.0, 1.0, 12.0)
    assert obs.how == K.KEPT and obs.poorer and obs.moved_nm == pytest.approx(3.0 / 145.0)
    assert r.sigma_north_nm == pytest.approx(math.sqrt(144.0 / 145.0))
    assert K.verdict_words(obs) == "the account kept"
    # a good figure against a poor account: nearly all the way, and not "taken"
    r = K.Reckoning(Position(49.0, -6.0), sigma_nm=3.0)
    obs = r.observe_line(0.0, 6.0, 0.0, 1.0, 0.5)
    assert obs.how == K.WEIGHED and obs.moved_nm == pytest.approx(6.0 * 9.0 / 9.25)
    assert K.verdict_words(obs) == "the account moved six miles to the N"


def test_one_rule_an_observation_is_taken_when_the_account_is_plainly_out():
    """Item 1, as package 37j amends it. When the two disagree by more than their doubts
    together allow, one of them is plainly out, and the better figure is believed: the
    observation is taken, the account laid on it and the account's doubt in that
    direction becoming the observation's own, only when its doubt is no greater than the
    account's across its line. "Together" is the sum of what he would trust each within,
    twice its doubt (the number two kept, for that reason)."""
    assert K.OBSERVATION_OUT_SIGMAS == 2.0
    r = K.Reckoning(Position(49.0, -6.0), sigma_nm=2.0)
    edge = K.OBSERVATION_OUT_SIGMAS * (2.0 + 1.0)
    obs = r.observe_line(0.0, -(edge + 0.01), 0.0, 1.0, 1.0)
    assert obs.how == K.TAKEN and obs.moved_nm == pytest.approx(edge + 0.01)
    assert obs.toward_deg == pytest.approx(180.0) and not obs.doubted
    assert r.lat_deg == pytest.approx(49.0 - (edge + 0.01) / 60.0)
    assert r.sigma_north_nm == pytest.approx(1.0) and r.sigma_east_nm == pytest.approx(2.0)
    assert K.verdict_words(obs) == (
        "the reckoning was out by it; laid down by the observation: moved two leagues to the S"
    )
    r = K.Reckoning(Position(49.0, -6.0), sigma_nm=2.0)
    obs = r.observe_line(0.0, -(edge - 0.01), 0.0, 1.0, 1.0)
    assert obs.how == K.WEIGHED and obs.moved_nm == pytest.approx((edge - 0.01) * 4.0 / 5.0)
    assert not obs.doubted
    # the two doubts equal: the observation is no poorer, and is taken
    r = K.Reckoning(Position(49.0, -6.0), sigma_nm=1.5)
    obs = r.observe_line(0.0, -6.01, 0.0, 1.0, 1.5)
    assert obs.how == K.TAKEN and not obs.doubted
    # the poorer figure, as far out: weighed, and the master doubts it
    r = K.Reckoning(Position(49.0, -6.0), sigma_nm=1.0)
    obs = r.observe_line(0.0, -(edge + 0.01), 0.0, 1.0, 2.0)
    assert obs.how == K.WEIGHED and obs.doubted
    assert obs.moved_nm == pytest.approx((edge + 0.01) / 5.0)
    assert obs.off_toward_deg == pytest.approx(180.0) and r.sigma_north_nm < 1.0
    assert K.verdict_words(obs, what="the sight") == (
        "the sight stands two leagues to the S of the account, and the account, good to a "
        "mile, is the better figure: the account moved a mile to the S"
    )
    # a fix, the same rule in two directions: taken beyond the two doubts along the line
    # between them when it is the better figure, weighed within, doubted when poorer
    r = K.Reckoning(Position(49.0, -6.0), sigma_nm=1.0)
    cov = [[0.25, 0.0], [0.0, 0.25]]
    obs = r.observe_point(2.0, 2.0, cov)
    assert obs.how == K.WEIGHED and obs.moved_nm == pytest.approx(math.hypot(2.0, 2.0) * 0.8)
    assert r.sigma_east_nm == pytest.approx(math.sqrt(0.2)) and not obs.doubted
    r = K.Reckoning(Position(49.0, -6.0), sigma_nm=1.0)
    obs = r.observe_point(3.0, 3.0, cov)
    assert obs.how == K.TAKEN and obs.moved_nm == pytest.approx(math.hypot(3.0, 3.0))
    assert r.P == cov and r.lat_deg == pytest.approx(49.05)
    r = K.Reckoning(Position(49.0, -6.0), sigma_nm=0.5)
    obs = r.observe_point(3.0, 3.0, [[1.0, 0.0], [0.0, 1.0]])
    assert obs.how == K.WEIGHED and obs.doubted
    assert obs.moved_nm == pytest.approx(math.hypot(3.0, 3.0) * 0.2)


def test_the_lunar_of_game_9_moves_the_account_under_two_cables():
    """Item 1, from game 9 (tick 246,131): a lunar "which he would trust within 25 miles"
    (12.12 miles one sigma) against an account that trusted itself within two (0.83 east
    and west). Under the two-mile rule it replaced the account's longitude and blew its
    doubt up to twelve miles; weighed, it moves the account under two cables and leaves
    its doubt east and west under two miles, and the line says the account was kept."""
    from freesail.world import sights

    w = chart_world(48.516, -5.331, ship=BRIG, start=datetime(1805, 6, 15, 1, 22))
    nav = w.navigation
    r = nav.reckoning
    r.set_position(Position(48.511, -5.273), w.clock.tick)
    r.P = [[0.83**2, 0.0], [0.0, 0.59**2]]
    lunar = sights.Lunar("Markab", -5.37743, 12.12, w.clock.tick, None)
    nav._lunar_pending = (w.clock.tick, lunar)
    nav._lunar_cleared()
    line = [e for e in w.log if e.kind == "reckoning.lunar"][-1]
    assert line.data["how"] == K.KEPT and line.data["moved_nm"] < 0.2
    assert abs(r.lon_deg - (-5.273)) * 60.0 * math.cos(math.radians(48.5)) < 0.2
    assert r.sigma_east_nm < 2.0 and r.sigma_north_nm == pytest.approx(0.59)
    assert (
        "longitude by lunar 5° 23' W, which he would trust within 25 miles, and the account "
        "within two miles; the reckoning was 5° 16' W: the account kept." in line.text
    )
    # package 37j, the owner's note 5: the same lunar against the same account set
    # eighteen leagues off, further from it than the two doubts together, is still the
    # poorer figure (12.12 against 0.83): weighed and doubted, it moves the account a
    # cable or two, and the line says the master doubts it
    r.set_position(Position(48.511, -4.0), w.clock.tick)
    r.P = [[0.83**2, 0.0], [0.0, 0.59**2]]
    nav._lunar_pending = (w.clock.tick, lunar)
    nav._lunar_cleared()
    line = [e for e in w.log if e.kind == "reckoning.lunar"][-1]
    assert line.data["how"] == K.WEIGHED and 0.1 < line.data["moved_nm"] < 0.3
    assert r.sigma_east_nm < 0.83
    assert (
        ": the lunar stands 18 leagues and a half to the W of the account, and the account, "
        "good to "
        "eight cables, is the better figure: the account moved three cables to the W."
    ) in line.text
    # and against an account that doubts itself more than the lunar, as far out, it is
    # taken, and its line says so
    r.set_position(Position(48.511, -1.2), w.clock.tick)
    r.P = [[13.0**2, 0.0], [0.0, 0.59**2]]
    nav._lunar_pending = (w.clock.tick, lunar)
    nav._lunar_cleared()
    line = [e for e in w.log if e.kind == "reckoning.lunar"][-1]
    assert line.data["how"] == K.TAKEN and r.lon_deg == pytest.approx(-5.37743)
    assert r.sigma_east_nm == pytest.approx(12.12)
    assert ": the reckoning was out by it; laid down by the lunar: moved " in line.text


def test_game_9s_noon_is_doubted_by_the_lead_kept_account_and_weighed_by_an_honest_one():
    """Item 1, from game 9 (tick 370,860), as package 37j amends the rule: the octant's
    sight gave 48° 07' N (48.12183, good to 2.28 miles one sigma, and right within two);
    the account said 48° 12½' N and trusted itself within half a mile (0.26 north and
    south), the lead cast every glass having kept its doubt so small. 37e took the sight
    outright (5.23 miles apart is 2.06 of the two doubts together). Under the better
    figure's rule, against that account the sight is the poorer figure and is doubted:
    weighed, it moves the account a cable. The account was not that good: the cast not
    beyond doubt (item 2) is what keeps its doubt honest, and against an honest doubt the
    same sight is believed by the doubts. The figures of an honest doubt are measured by
    the scripted forenoon below (`test_the_forenoon_of_16_june_...`): there the casts
    leave a doubt of a mile and nine tenths at noon, where 37d's left a quarter; the two
    then stand within their doubts together, and the sight moves the account two fifths
    of the way to it. "Taken" outright it could not be against any account no better than
    itself: two doubts together, each no less than the sight's 2.28, are nine miles."""
    r = K.Reckoning(Position(48.209, -4.814), sigma_nm=1.0)
    r.P = [[0.61**2, 0.0], [0.0, 0.26**2]]
    obs = r.observe_latitude(48.12183, 2.28)
    assert obs.off_nm == pytest.approx(5.23, abs=0.01)
    assert obs.off_nm > K.OBSERVATION_OUT_SIGMAS * (0.26 + 2.28)  # plainly apart
    gain = 0.26**2 / (0.26**2 + 2.28**2)
    assert (
        obs.how == K.WEIGHED
        and obs.doubted
        and obs.moved_nm == pytest.approx(gain * 5.23, abs=0.01)
    )
    assert r.sigma_east_nm == pytest.approx(0.61)
    assert K.verdict_words(obs, what="the sight") == (
        "the sight stands five miles to the S of the account, and the account, good to three "
        "cables, is the better figure: the account moved a cable to the S"
    )
    # an honest account, as the forenoon's casts leave it (a mile and nine tenths): within
    # the two doubts together, weighed by them, two miles of the five
    r = K.Reckoning(Position(48.209, -4.814), sigma_nm=1.9)
    obs = r.observe_latitude(48.12183, 2.28)
    gain = 1.9**2 / (1.9**2 + 2.28**2)
    assert obs.how == K.WEIGHED and not obs.doubted
    assert obs.moved_nm == pytest.approx(gain * 5.23, abs=0.01) and obs.moved_nm > 2.0
    assert K.verdict_words(obs, what="the sight") == "the account moved two miles to the S"
    # an account that doubts itself more than the sight, and nine miles and a half out:
    # taken
    r = K.Reckoning(Position(48.12183 + 9.5 / 60.0, -4.814), sigma_nm=2.3)
    obs = r.observe_latitude(48.12183, 2.28)
    assert obs.how == K.TAKEN and r.lat_deg == pytest.approx(48.12183)
    # a mile out: weighed by the two doubts, and with a doubt of a quarter of a mile
    # against the sight's two and a quarter the account hardly moves
    r = K.Reckoning(Position(48.12183 + 1.0 / 60.0, -4.814), sigma_nm=1.0)
    r.P = [[0.61**2, 0.0], [0.0, 0.26**2]]
    obs = r.observe_latitude(48.12183, 2.28)
    gain = 0.26**2 / (0.26**2 + 2.28**2)
    assert obs.how != K.TAKEN and obs.moved_nm == pytest.approx(gain) and not obs.doubted
    # and with a doubt of a mile and a half, as an honest account has after a forenoon
    # in a stream, it goes three cables of the mile
    r = K.Reckoning(Position(48.12183 + 1.0 / 60.0, -4.814), sigma_nm=1.5)
    obs = r.observe_latitude(48.12183, 2.28)
    assert obs.how == K.WEIGHED
    assert K.verdict_words(obs) == "the account moved three cables to the S"


def test_a_bearing_of_a_light_eleven_miles_off_after_twelve_miles_of_doubt_lays_the_line_down():
    """Item 1, from game 9 (tick 246,153): with twelve miles of doubt east and west and
    the light on Ushant eleven miles off, a bearing worked as an angle at the account
    left 2.6 miles of error across the sight. When the account's doubt across the sight
    is more than a tenth of the distance the line itself is laid down, and the account
    is left within the bearing's own doubt of it."""
    w = chart_world(48.516, -5.331, ship=BRIG, heading=200.0, start=datetime(1805, 6, 15, 1, 22))
    w.run(60)
    nav = w.navigation
    light = w.lookout.find("the light on Ushant")
    assert light is not None and 10.0 < light.distance_m / units.NAUTICAL_MILE < 12.5
    r = nav.reckoning
    r.set_position(Position(48.511, -5.377), w.clock.tick)
    r.P = [[12.12**2, 0.0], [0.0, 0.6**2]]
    e = w.submit("take a bearing of the light on Ushant")
    assert e.kind == "bearing.taken" and e.data["line"] == K.WEIGHED
    laid = math.radians(e.data["bearing_deg"])
    de, dn = r.offset_nm(light.feature.position)
    off_the_line = abs(math.hypot(de, dn) * math.sin(units.wrap_pi(math.atan2(de, dn) - laid)))
    assert off_the_line < e.data["line_sigma_nm"] < 1.0
    assert miles_between(r.position, w.position) < 1.0
    # the angle's form is kept for an account whose doubt is small beside the distance:
    # it moves the account across the sight and not along it
    r.set_position(destination(w.position, 0.0, 0.5 * units.NAUTICAL_MILE), w.clock.tick, 0.3)
    _, before = bearing_and_distance(r.position, light.feature.position)
    nav._last_bearing_mark = None
    e = w.submit("take a bearing of the light on Ushant")
    _, after = bearing_and_distance(r.position, light.feature.position)
    assert e.data["distance"] == K.KEPT and abs(after - before) < 0.02 * units.NAUTICAL_MILE


def test_the_words_of_a_cast_a_noon_and_a_bearing_say_which_of_the_three():
    """Item 1: the words say what the master did, since the words are a model's whole
    view of it; the data says which (`taken`, `weighed`, `kept`) with the miles moved."""
    w = chart_world(49.4, -5.3, heading=0.0, start=datetime(1805, 6, 10, 11, 30))
    nav = w.navigation
    w.submit("set plain sail")
    w.run(1500)
    # an account four leagues south of her true place, trusting itself within three miles
    # (package 37j: the sight, a better figure than that, is taken)
    nav.reckoning.set_position(destination(w.position, 180.0, 12.0 * units.NAUTICAL_MILE), 0, 3.0)
    w.run(300)
    noon = [e for e in w.log if e.kind == "reckoning.noon"][-1]
    assert noon.data["how"] == K.TAKEN and noon.data["moved_nm"] > 7.0
    assert "; the reckoning was " in noon.text
    assert ": the reckoning was out by it; laid down by the observation: moved " in noon.text
    assert noon.text.rstrip(".").endswith("by the directions and the epitome")


# -- item 2: the doubt, honest --------------------------------------------------------------


def test_the_doubt_grows_by_the_hour_hove_to_and_becalmed_and_not_at_anchor():
    """Item 2. Until package 37e the hours hove to and without way were struck from the
    interval, so neither the account nor its doubt moved through them (game 9, hove to
    on 15 June from ten to noon: the true error grew from 3.3 miles to 4.8 and the doubt
    from 1.08 to 1.12). Hove to, lying a-try and becalmed she still drifts, and he still
    doubts; at anchor the account stays where it is and its doubt does not grow."""
    # becalmed, no sail set and no wind: nothing run, and the doubt grows
    calm = at_rest(*IROISE)
    nav = calm.navigation
    nav.reckoning.set_position(calm.position, 0, sigma_nm=0.3)
    before = nav.doubt_now()
    calm.run(3 * 3600)
    after = nav.doubt_now()
    assert after["semi_major_nm"] > before["semi_major_nm"] + 0.8
    assert calm.readings["reckoning_uncertainty"]["ellipse"] == {
        k: v for k, v in after.items() if k != "words"
    }
    # hove to in a breeze: the same, and more for his doubt of her drift
    hove = chart_world(*IROISE, ship=BRIG, heading=300.0, start=datetime(1805, 6, 15, 10, 0))
    hove.submit("set topsails")
    hove.run(600)
    assert hove.submit("heave to").kind == "order.accepted"
    hove.run(600)
    assert "hove_to" in hove.ship.extra
    hove.navigation.reckoning.set_position(hove.position, hove.clock.tick, sigma_nm=0.3)
    hove.run(3 * 3600)
    lying = hove.navigation.doubt_now()
    assert lying["semi_major_nm"] > 0.3 + 0.8  # as it does becalmed, and no clock stopped
    # at anchor: the account stays, and the doubt as it was
    road = chart_world(50.160, -5.034, ship=BRIG, start=datetime(1805, 6, 15, 13, 0))
    assert road.submit("let go the anchor").kind == "order.accepted"
    road.run(900)
    assert road.at_anchor
    nav = road.navigation
    nav.reckoning.set_position(road.position, road.clock.tick, sigma_nm=0.3)
    was, doubt = nav.account_now(), nav.doubt_now()
    road.run(3 * 3600)
    assert nav.account_now() == was and nav.doubt_now() == doubt
    assert road.readings["reckoning"]["tide"]["words"] == "none while she rides at anchor"


def test_the_doubt_of_the_stream_grows_along_its_set_and_no_further_than_the_stream_can_set_her():
    """Item 2. Where his directions give a stream the doubt grows by the part of it he
    cannot know (its hour, its rate, its set), along the set, in a straight line by the
    clock and no further than the stream can set her before it turns; what was grown in
    other water stays. Where they give none, by the open-water terms as before."""

    def grown(hours: int, stream) -> K.Reckoning:
        r = K.Reckoning(Position(48.2, -5.0), sigma_nm=0.0)
        for h in range(hours):
            r.advance(0.0, 0.0, 0.0, (h + 1) * 3600, clock_hours=1.0, stream=stream)
        return r

    north = ("the-iroise", 2.0, 0.0, 1.0)  # two knots, setting north, an hour of it
    open_water = grown(1, None)
    one = grown(1, north)
    # an hour: half the rate along the set, and across it the open-water terms alone
    assert one.sigma_east_nm == pytest.approx(open_water.sigma_east_nm)
    assert one.sigma_north_nm**2 - open_water.sigma_north_nm**2 == pytest.approx(
        (K.STREAM_DOUBT_FRACTION * 2.0) ** 2
    )
    two, six = grown(int(K.STREAM_DOUBT_HOURS), north), grown(6, north)
    cap = K.STREAM_DOUBT_FRACTION * 2.0 * K.STREAM_DOUBT_HOURS
    assert two.stream_doubt == pytest.approx([0.0, cap])
    assert six.stream_doubt == pytest.approx([0.0, cap])  # the stream has turned by then
    # passing into other water: what was grown stays, and the new water's grows beside it
    six.advance(
        0.0, 0.0, 0.0, 7 * 3600, clock_hours=1.0, stream=("mid-channel", 1.0, math.pi / 2, 1.0)
    )
    assert six.stream_water == "mid-channel"
    assert six.stream_doubt == pytest.approx([K.STREAM_DOUBT_FRACTION, 0.0])
    assert six.sigma_north_nm > cap
    # the hours hove to count for the set's doubt though nothing is run
    r = K.Reckoning(Position(48.2, -5.0), sigma_nm=0.0)
    r.advance(0.0, 0.0, 0.0, 3600, clock_hours=4.0)
    assert r.sigma_east_nm == pytest.approx(4.0 * K.SET_DOUBT_EAST_KN)
    assert r.lat_deg == 48.2 and r.lon_deg == -5.0


def test_the_master_doubts_his_log_line_and_his_compass_in_the_run():
    """Item 2, sized by measurement (TuningNotes, package 37e): the log-line is marked
    short on purpose and the compass carries every course to one side; the master knows
    the likely size of each and not its amount, and his doubt of the run says so: four
    per cent of it along the course, and across it the allowance he makes in a bearing.
    The traverse's own arithmetic (truth 58) has neither."""
    r = K.Reckoning(Position(49.0, -6.0), sigma_nm=0.0)
    plain = K.Reckoning(Position(49.0, -6.0), sigma_nm=0.0)
    allow = math.radians(K.COMPASS_ALLOWANCE_DEG)
    for h in range(10):
        r.advance(1.0, 0.0, 6.0, (h + 1) * 3600, run_doubt=K.LOG_LINE_DOUBT, course_doubt_rad=allow)
        plain.advance(1.0, 0.0, 6.0, (h + 1) * 3600)
    assert r.run_doubt == pytest.approx([0.0, 60.0 * K.LOG_LINE_DOUBT])
    assert r.course_doubt == pytest.approx([60.0 * allow, 0.0])
    assert r.sigma_north_nm**2 - plain.sigma_north_nm**2 == pytest.approx(2.4**2)
    assert r.sigma_east_nm**2 - plain.sigma_east_nm**2 == pytest.approx((60.0 * allow) ** 2)
    # there and back again: a bias of one sense on every course comes home with her
    for h in range(10):
        r.advance(
            1.0, math.pi, 6.0, (h + 11) * 3600, run_doubt=K.LOG_LINE_DOUBT, course_doubt_rad=allow
        )
    assert r.run_doubt == pytest.approx([0.0, 0.0], abs=1e-9)
    assert r.course_doubt == pytest.approx([0.0, 0.0], abs=1e-9)
    # an observation across the course resolves the compass's part and leaves the log's
    r = K.Reckoning(Position(49.0, -6.0), sigma_nm=0.0)
    for h in range(10):
        r.advance(1.0, 0.0, 6.0, (h + 1) * 3600, run_doubt=K.LOG_LINE_DOUBT, course_doubt_rad=allow)
    r.observe_longitude(r.lon_deg, 0.1)
    assert abs(r.course_doubt[0]) < 0.01 and r.run_doubt[1] == pytest.approx(2.4)
    # and in the ship the master passes both, less for the compass once he has observed
    w = chart_world(49.4, -5.3)
    assert w.navigation.compass_allowance_deg() == K.COMPASS_ALLOWANCE_DEG
    from freesail.world.sights import Variation

    w.navigation.variation = Variation(24.0, "amplitude")
    assert w.navigation.compass_allowance_deg() == K.COMPASS_ALLOWANCE_OBSERVED_DEG < 2.0


def test_the_same_thing_seen_again_tells_him_nothing_new():
    """Item 2. An observation shrank the doubt each time it was taken, even the same one
    again: the master talked himself into certainty. A second line of the same thing
    lying where the first lay carries the same error, so it cannot bring the doubt across
    the line below that error, and where the account is already as good it is not
    applied at all."""
    r = K.Reckoning(Position(49.0, -6.0), sigma_nm=3.0)
    first = r.observe_line(0.0, 1.0, 0.0, 1.0, 1.0, thing="a mark")
    left = r.sigma_north_nm
    assert first.how == K.WEIGHED and not first.repeat and left < 1.0
    for _ in range(8):
        again = r.observe_line(0.0, 0.0, 0.0, 1.0, 1.0, thing="a mark")
        assert again.repeat and again.how == K.KEPT and again.moved_nm == 0.0
    assert r.sigma_north_nm == left  # eight more, and no surer
    # an independent observation of another thing still narrows it
    r.observe_line(0.0, 0.0, 0.0, 1.0, 1.0, thing="another mark")
    assert r.sigma_north_nm < left
    # when the doubt has grown again with the hours the same thing is weighed again, and
    # leaves the doubt no smaller than its own error
    r = K.Reckoning(Position(49.0, -6.0), sigma_nm=3.0)
    r.observe_line(0.0, 1.0, 0.0, 1.0, 1.0, thing="a mark")
    r.P[1][1] = 25.0
    again = r.observe_line(0.0, 2.0, 0.0, 1.0, 1.0, thing="a mark")
    assert again.repeat and again.how == K.WEIGHED
    assert r.sigma_north_nm == pytest.approx(1.0)
    # the part of its doubt that is its own each time (a bearing's own draw) may still be
    # bettered; the part that is the same (the compass's error) may not
    r = K.Reckoning(Position(49.0, -6.0), sigma_nm=3.0)
    for _ in range(6):
        r.observe_line(0.0, 0.0, 0.0, 1.0, 1.0, thing="a mark", shared_sigma_nm=0.8)
    assert r.sigma_north_nm == pytest.approx(0.8)
    # a line of the same thing that has swung by more than five degrees is a new line
    r = K.Reckoning(Position(49.0, -6.0), sigma_nm=3.0)
    r.observe_line(0.0, 0.0, 0.0, 1.0, 1.0, thing="a mark")
    swung = math.radians(K.SAME_LINE_DEG + 1.0)
    obs = r.observe_line(0.0, 0.0, math.sin(swung), math.cos(swung), 1.0, thing="a mark")
    assert not obs.repeat


def test_eight_casts_in_a_calm_over_the_flat_sand_off_ar_men_narrow_nothing():
    """Item 2, from game 9 (the night of 15 June): eight casts of the deep-sea lead on a
    flat sandy bottom took the doubt from 2.2 miles to 1.3 while the error went from one
    mile to nearly five. A cast narrows the doubt only so far as the charted depth
    differs across his doubt: over a flat bottom it is no line at all. Eight casts leave
    the doubt as large as the first left it (and larger, by the hours)."""
    w = at_rest(*IROISE, start=datetime(1805, 6, 15, 17, 0))
    nav = w.navigation
    nav.reckoning.set_position(destination(w.position, 250.0, 1852.0), 0, sigma_nm=2.0)
    before = nav.doubt_now()
    doubts = []
    for _ in range(8):
        assert w.submit("heave the deep-sea lead").kind == "order.accepted"
        w.run(20 * 60)
        doubts.append(nav.doubt_now()["semi_major_nm"])
    casts = [e for e in w.log if e.kind == "sounding"]
    assert len(casts) == 8 and all(e.data["matched"] for e in casts)
    assert all("; fine grey sand with black specks. " in e.text for e in casts)
    # package 37j: his own tide off each cast, said when it is a fathom or more
    assert all(" of tide allowed by the epitome: " in e.text for e in casts)
    assert all(" on the chart. The account " in e.text for e in casts)
    # the bottom shelves a fathom or two in a mile here: a line good to a mile or so at
    # the best, which the first cast gives; the seven after it are the same ground, and
    # though the depth changing under her may move the account they narrow nothing
    assert all(e.data["line_sigma_nm"] > 0.5 for e in casts)
    assert doubts[0] <= before["semi_major_nm"] + 0.05
    assert min(doubts[1:]) >= doubts[0] - 0.01 and doubts[-1] > doubts[0]
    ellipses = nav.reckoning.ellipse()
    assert ellipses["semi_minor_nm"] >= 0.5 and doubts[0] > 1.0
    assert all(e.data["how"] in (K.KEPT, K.WEIGHED) for e in casts)
    # over a steep bottom a cast is a good line, once: in the Goulet's mouth
    assert nav._sounding_sigma_nm(Position(48.33, -4.60), K.CONTOUR_TOLERANCE_HAND_FATHOMS) < 0.5
    # and over a flat one, read across a doubt of leagues, it is no line at all
    assert nav._sounding_sigma_nm(Position(49.2, -5.6), K.CONTOUR_TOLERANCE_DEEP_FATHOMS, 6.0) > 6.0


# -- item 3: `take a fix`, by the marks that fix her best --------------------------------------


def test_in_the_goulet_the_master_takes_the_near_marks_before_camaret_brest_and_conquet():
    """Item 3, from game 9 (tick 387,115: she lay three cables west of the Mingan with
    Petit Minou inside a mile). The master took Camaret, Brest and Conquet, three to
    seven miles off, because they cut at the widest angles; their lines met within a
    mile and a half and the fix was three cables out. He now takes the marks whose fix
    has the least doubt, with the compass's shared error counted: a headland a mile off
    before a town six miles off."""
    w = chart_world(48.337, -4.5958, ship=BRIG, heading=90.0, start=datetime(1805, 6, 16, 16, 31))
    w.run(60)
    nav = w.navigation
    marks = {s.feature.name: s for s in nav._fix_marks()}
    for name in ("Petit Minou", "the Mingan", "Camaret", "Brest", "Conquet"):
        assert name in marks, name
    assert marks["Petit Minou"].distance_m < 1.2 * units.NAUTICAL_MILE
    assert marks["the Mingan"].distance_m < 0.4 * units.NAUTICAL_MILE
    nav.reckoning.set_position(destination(w.position, 200.0, 0.4 * units.NAUTICAL_MILE), 60, 0.4)
    e = w.submit("take a fix")
    assert e.kind == "reckoning.fix"
    chosen = [m["name"] for m in e.data["marks"]]
    # Petit Minou and the Mingan bear west and east, one line through her: one of the two
    # serves, with the nearest marks that cut it (Camaret is the only mark to the
    # southward, and Portzic is nearer than the towns); never Brest or Conquet
    assert "Petit Minou" in chosen or "the Mingan" in chosen
    assert not {"Brest", "Conquet", "the castle of Brest", "Point Conquet"} & set(chosen)
    assert min(marks[name].distance_m for name in chosen) < 1.2 * units.NAUTICAL_MILE
    assert max(marks[name].distance_m for name in chosen) < 4.0 * units.NAUTICAL_MILE
    allow = nav.compass_allowance_deg()
    far = [marks[name] for name in ("Camaret", "Brest", "Conquet")]
    assert K._fix_doubt_nm([marks[n] for n in chosen], allow) < 0.6 * K._fix_doubt_nm(far, allow)
    # (the fix's own draws since package 37j: the lines met within three cables, "good to
    # two cables", and the account a cable and a quarter from her)
    assert miles_between(nav.reckoning.position, w.position) < 0.15
    assert e.data["sigma_nm"] <= 0.2
    assert "good to a cable" in e.text or "good to two cables" in e.text
    # a headland a mile off is preferred to a town six miles off, other things equal
    near = [marks["Petit Minou"], marks["Camaret"]]
    assert K._fix_doubt_nm(near, allow) < K._fix_doubt_nm(
        [marks["Conquet"], marks["Camaret"]], allow
    )


def test_moored_in_brest_road_a_fix_by_far_marks_leaves_a_sound_account_where_it_was():
    """Item 3, from game 9 (tick 426,085): moored in Brest road, her account right to a
    cable, the standing order's fix by the castle of Brest and St Matthew's light (eleven
    miles off) moved it nearly a mile, and said it was good to three cables. A fix is
    weighed as any observation: by far marks it is the poorer figure, its "good to" says
    so, and it moves the account under a cable."""
    road = destination(Position(48.38294, -4.49824), 173.0, 1.8 * units.NAUTICAL_MILE)
    w = chart_world(
        road.lat_deg, road.lon_deg, ship=BRIG, heading=250.0, start=datetime(1805, 6, 17, 3, 21)
    )
    w.run(60)
    nav = w.navigation
    light = w.lookout.find("St Matthew's light")
    assert light is not None and light.distance_m > 10.0 * units.NAUTICAL_MILE
    nav.reckoning.set_position(destination(w.position, 30.0, 0.1 * units.NAUTICAL_MILE), 60, 0.1)
    before = nav.reckoning.position
    for k in range(3):
        e = w.submit("take a fix by the castle of Brest and St Matthew's light")
        assert e.kind == "reckoning.fix" and e.severity is Severity.ROUTINE
        assert e.data["sigma_nm"] > 0.45  # eleven miles of the compass's own error
        if k == 0:
            # the first, by its draw at this seed since package 37j, moves it a cable
            assert e.data["how"] in (K.KEPT, K.WEIGHED) and e.data["moved_nm"] < 0.12
            continue
        assert e.data["how"] == K.KEPT and e.data["moved_nm"] < 0.1
        assert ", the fix the poorer figure; the account kept, within " in e.text
    assert miles_between(nav.reckoning.position, before) < 0.1
    assert miles_between(nav.reckoning.position, w.position) < 0.2
    # the doubt is no smaller for three fixes by the same marks from the same place
    assert nav.reckoning.ellipse()["semi_major_nm"] >= 0.09
    # unnamed, he takes the near marks, and that fix may move her a cable
    e = w.submit("take a fix")
    assert (
        max(w.lookout.find(m["name"]).distance_m for m in e.data["marks"])
        < 3.0 * units.NAUTICAL_MILE
    )
    assert e.data["sigma_nm"] < 0.2


# The 61 fixes of game 9, by their marks and how far off each lay (the measurements'
# table "THE FIXES"): the miles off, and for each mark its name on the chart.
GAME_9_FIXES = (
    ("St Anthony's Head 1.5, St Budock church 2.5, Nare Point 5.0", 1),
    ("Pendennis castle 0.7, Trefusis Point 1.4, Nare Point 4.1", 1),
    ("St Anthony's Head 0.8, Trefusis Point 2.1", 1),
    ("Rosemullion Head 3.9, Lowland Point 4.4, Mylor Point 6.0", 1),
    ("the Lavandière 1.1, the Isle of Bas 2.4", 1),
    ("the Lavandière 0.4, the Isle of Bas 1.6, Pointe de Pergueridre 1.9", 1),
    ("the Lavandière 0.6, Pointe de Pergueridre 1.3", 3),
    ("the Isle of Bas 1.0, Pointe de Pergueridre 1.3", 12),
    ("the Lavandière 0.3, Pointe de Pergueridre 1.6", 1),
    ("Molène 11.6, Ushant 9.2", 1),
    ("St Matthew's light 13.7, the light on Ushant 19.1", 1),
    ("the Isle of Saints 10.2, St Matthew's Point 10.5", 1),
    ("Conquet 10.8, the Isle of Saints 10.5, Pointe des Pezeaux 11.9", 1),
    ("Point Conquet 10.6, the Raz 11.6, Pointe des Pezeaux 11.4", 1),
    ("the Raz 8.0, St Matthew's light 11.7, Pointe des Pezeaux 11.6", 1),
    ("the Raz 8.2, Point Bertheaume 11.5, Le Bec de la Chèvre 10.5", 1),
    ("Le Bec de la Chèvre 8.2, Point Conquet 9.1, Penaleuch point 11.4", 1),
    ("Camaret 6.0, Le Bec de la Chèvre 7.9, the Raz 11.5", 1),
    ("Point Bertheaume 5.5, Camaret 5.0, Le Bec de la Chèvre 7.8", 1),
    ("the Tas de Foin 2.8, St Matthew's light 5.4, Petit Minou 6.2", 1),
    ("Pointe des Pezeaux 2.9, Petit Minou 5.3, Conquet 6.4", 1),
    ("Point Bertheaume 2.8, Camaret 3.4, Petit Minou 3.5", 1),
    ("the Tas de Foin 3.0, Petit Minou 2.9, St Matthew's light 4.7", 1),
    ("Toulinguet 2.2, the Mingan 2.7, Conquet 5.9", 1),
    ("Pointe des Pezeaux 4.0, the castle of Brest 6.1, Conquet 6.2", 1),
    ("Camaret 3.2, Conquet 6.3, Brest 6.3", 2),
    ("Camaret 3.5, Brest 5.2, Conquet 7.2", 1),
    ("the Mingan 0.7, Camaret 4.0, Conquet 7.9", 1),
    ("the castle of Brest 4.0, Camaret 3.9, Conquet 7.8", 2),
    ("Portzic 1.8, Camaret 4.0, Conquet 8.0", 1),
    ("the Mingan 0.6, Penaleuch point 1.4", 3),
    ("Penaleuch point 1.5, Portzic 1.9", 5),
    ("Penaleuch point 1.0, Portzic 1.4", 1),
    ("Portzic 0.5, Brest 3.0, St Matthew's light 9.5", 2),
    ("Portzic 1.6, Penaleuch point 2.0, Brest 2.2", 1),
    ("Portzic 1.7, Brest 2.1", 2),
    ("the castle of Brest 1.8, St Matthew's light 11.2", 2),
)


def _place_by_distances(chart, marks: list[tuple[str, float]]) -> Position:
    """A place of the sea from which the marks lie the miles off the measurements give:
    the best fit by steps downhill, from a start on the marks' seaward side."""
    features = [(chart.find_feature(name), miles) for name, miles in marks]
    assert all(f is not None for f, _ in features), marks

    def misfit(p: Position) -> float:
        return sum(
            (bearing_and_distance(p, f.position)[1] / units.NAUTICAL_MILE - miles) ** 2
            for f, miles in features
        )

    best: tuple[float, Position] | None = None
    first = features[0][0].position
    for bearing in range(0, 360, 20):
        p = destination(first, float(bearing), features[0][1] * units.NAUTICAL_MILE)
        step = 1852.0
        while step > 5.0:
            moved = False
            for dx, dy in ((step, 0.0), (-step, 0.0), (0.0, step), (0.0, -step)):
                q = p.advanced(dx, dy)
                if misfit(q) < misfit(p):
                    p, moved = q, True
            if not moved:
                step /= 2.0
        depth = chart.depth_at(p)
        if depth is not None and depth > 0.0 and (best is None or misfit(p) < best[0]):
            best = (misfit(p), p)
    assert best is not None and best[0] < 0.6, (marks, best)
    return best[1]


def test_over_the_geometry_of_game_9s_fixes_good_to_is_honest():
    """Item 3, from game 9. In 12 fixes of 61 the true error was more than twice the
    stated figure: every bearing of a fix carries the compass's own error on her heading
    (two and a half degrees in that ship) and the lines share it, so a tight cocked hat
    can sit well off the ship, four cables at ten miles. With the master's allowance for
    it counted, over the same marks at the same distances and with that same error in
    every bearing, the true error is beyond twice "good to" in no more than one fix in
    ten."""
    from freesail.world.chart import Sighting, load_chart

    chart = load_chart(REGION)
    stream = random.Random(37)
    compass = math.radians(2.5)  # the brig's own error in game 9, measured 2.2 to 2.6
    fixes = out = 0
    said, far_said = [], []
    for row, times in GAME_9_FIXES:
        marks = []
        for part in row.split(", "):
            name, miles = part.rsplit(" ", 1)
            marks.append((name, float(miles)))
        truth = _place_by_distances(chart, marks)
        sightings = []
        for name, _ in marks:
            f = chart.find_feature(name)
            bearing, distance = bearing_and_distance(truth, f.position)
            sightings.append(Sighting(f, bearing, distance, "land", distance))
        for _ in range(times * 4):  # each fix of the game four times over, for the draws
            lines = [
                (
                    s,
                    (math.radians(s.bearing_deg) + compass + stream.gauss(0.0, math.radians(1.5)))
                    % units.TWO_PI,
                )
                for s in sightings
            ]
            fix, cov, hat_m = K._fix_of(
                truth.advanced(300.0, -200.0), lines, K.COMPASS_ALLOWANCE_DEG
            )
            good_to = math.sqrt(K._greatest_eigen(cov))
            if hat_m is not None:
                good_to = max(good_to, 0.5 * hat_m / units.NAUTICAL_MILE)
            fixes += 1
            out += miles_between(fix, truth) > 2.0 * good_to
            said.append(good_to)
            if min(m for _, m in marks) > 8.0:
                far_said.append(good_to)
    assert fixes == 61 * 4
    assert out <= 0.1 * fixes, (out, fixes)
    # and far marks are seen to be poor ones: four cables and more at ten miles
    assert min(far_said) > 0.4 and sorted(said)[len(said) // 2] < 0.2


# -- item 4: the account hove to, becalmed and after --------------------------------------------


def test_hove_to_the_master_reckons_her_drift_and_the_run_since_noon_takes_it():
    """Item 4. Hove to, the master reckons her drift and does not stop the clock: the
    tide he allows, and her drift by his eye (Falconer 1780, 'Drift': the line she
    drives on and the distance). The run since noon and the day's work take it."""
    w = chart_world(*IROISE, ship=BRIG, heading=300.0, start=datetime(1805, 6, 15, 12, 30))
    w.submit("set topsails")
    w.run(600)
    w.submit("heave to")
    w.run(600)
    nav = w.navigation
    nav.reckoning.set_position(w.position, w.clock.tick, sigma_nm=0.2)
    nav.noon_had = True
    nav.reckoning.noon_mark = (w.clock.tick, w.position.lat_deg, w.position.lon_deg)
    nav.reckoning.run_since_noon_nm = 0.0
    start, account = w.position, nav.account_now()
    w.run(3 * 3600)
    drifted = miles_between(start, w.position)
    reckoned = miles_between(account, nav.account_now())
    assert drifted > 3.0 and 0.6 * drifted < reckoned < 1.4 * drifted
    # a third of her drift (1.68 miles of 5.0 since package 37j: the account worked at the
    # heave-to itself, where the setting of it by hand left the board begun before)
    assert error_nm(w) < drifted / 2.8
    run, course = nav.since_noon_reading()
    assert run == pytest.approx(nav.reckoning.run_since_noon_nm + nav._run_since_step_nm())
    assert run > 0.6 * drifted and course is not None
    truth_course, _ = bearing_and_distance(start, w.position)
    assert abs(units.wrap_pi(math.radians(course - truth_course))) < math.radians(40.0)


def test_after_she_fills_away_her_way_is_judged_by_eye_until_the_log_is_next_hove():
    """Item 4. After she fills away, weighs or comes out of a calm her way is judged by
    eye until the log is next hove: the last read before she lay to is not used (as she
    got under way from an anchor the account ran wild for some minutes on a read hours
    old)."""
    w = chart_world(49.3, -5.5, heading=0.0, start=datetime(1805, 6, 10, 9, 0))
    w.submit("set plain sail")
    w.run(3600 + 120)
    nav = w.navigation
    read = nav.last_log_read_kn
    assert read is not None and read > 4.0 and nav._way_kn() == read
    w.submit("heave to")
    w.run(900)
    assert nav._read_stale and nav._way_kn() == nav._speed_by_eye_kn() < read
    # a course shaped as she fills away is reckoned on the way she will make again
    assert nav._way_to_shape_by_kn() == read
    w.submit("fill away")
    w.run(600)
    assert nav._read_stale and nav._way_kn() == nav._speed_by_eye_kn()
    w.submit("heave the log")
    w.run(120)
    assert not nav._read_stale and nav._way_kn() == nav.last_log_read_kn


# -- items 6 and 7: the master's own tide, and the proof that it is his own -----------------------


def test_the_master_works_the_tide_into_the_traverse_as_one_more_course():
    """Item 6. Bowditch 1802, 'Currents': the ship is affected "as if she had sailed in
    still water, with an additional course and distance exactly equal to the course and
    set of the current", worked "in the traverse table as one more course". A ship with
    no way in the Iroise: the account goes with the master's tide, by the quarter hour,
    and stands nearer her than an account that allowed none."""
    w = at_rest(*IROISE)
    nav = w.navigation
    nav.reckoning.set_position(w.position, 0, sigma_nm=0.3)
    start = w.position
    tide = nav.book_tide(nav.account_now(), w.clock.ship_time)
    assert tide is not None and tide.area.id == "the-iroise" and tide.port.name == "Ushant"
    assert tide.area.set_point == "NE by N" and 0.75 <= tide.rate_kn <= 1.5
    summed = [0.0, 0.0]
    for _ in range(12):  # three hours by the quarter
        w.run(K.TIDE_QUARTER_S)
        middle = w.clock.ship_time - timedelta(seconds=K.TIDE_QUARTER_S / 2)
        book = nav.book_tide(nav.account_now(), middle)
        summed[0] += book.along_kn * 0.25 * math.sin(book.area.set_rad)
        summed[1] += book.along_kn * 0.25 * math.cos(book.area.set_rad)
    made = nav.reckoning.offset_nm(start)
    now = nav.account_now()
    de = (now.lon_deg - start.lon_deg) * 60.0 * math.cos(math.radians(start.lat_deg))
    dn = (now.lat_deg - start.lat_deg) * 60.0
    assert math.hypot(de - summed[0], dn - summed[1]) < 0.05, (de, dn, summed, made)
    assert math.hypot(*summed) > 1.0
    drifted = miles_between(start, w.position)
    assert drifted > 1.5 and error_nm(w) < 0.5 * drifted
    # the chart and the readings agree with the next working
    before = nav.account_now()
    nav.bring_up()
    assert miles_between(before, nav.reckoning.position) < 1e-6
    assert w.readings["reckoning"]["tide"]["by"] == "book"


def test_the_masters_tide_is_his_own_two_ships_ten_miles_apart_work_the_same_tide():
    """Item 7, the proof. Two worlds of one seed whose ships lie ten miles apart and
    whose accounts are the same work the same tide to the last figure; a world with its
    true tide made nothing works the same tide as one with it."""
    a = at_rest(*IROISE)
    b = at_rest(IROISE[0] + 9.0 / 60.0, IROISE[1] - 9.0 / 60.0)  # ten miles off, other water
    c = at_rest(*IROISE)
    c.tide = None  # no tide in this world at all
    c.tide_state = None
    c.ship.extra.pop("water", None)
    assert miles_between(a.position, b.position) > 10.0
    same = Position(48.20, -5.05)
    for w in (a, b, c):
        w.navigation.reckoning.set_position(same, 0, sigma_nm=0.5)
    for w in (a, b, c):
        w.run(4 * 3600 + 400)
        w.navigation.bring_up()
    ra, rb, rc = (w.navigation.reckoning for w in (a, b, c))
    assert (ra.lat_deg, ra.lon_deg) == (rb.lat_deg, rb.lon_deg) == (rc.lat_deg, rc.lon_deg)
    assert ra.P == rb.P == rc.P
    assert miles_between(same, ra.position) > 1.0  # and it is a tide, not nothing
    # the three ships themselves are in three places: two carried by two waters, and one
    # where she lay, in a world with no tide to carry her
    assert miles_between(a.position, b.position) > 5.0
    assert miles_between(a.position, Position(*IROISE)) > 1.0
    assert miles_between(c.position, Position(*IROISE)) < 0.5
    when = a.clock.ship_time
    assert a.navigation.book_tide(same, when) == b.navigation.book_tide(same, when)
    assert a.readings["reckoning"]["tide"] == b.readings["reckoning"]["tide"]
    lines = [[e.text for e in w.log if e.kind == "reckoning.tide"] for w in (a, b, c)]
    assert lines[0] == lines[1] == lines[2]


def test_a_master_with_moores_table_works_another_hour_from_one_with_nories():
    """Item 7. A poorer epitome does not change the directions; it changes the hour:
    Moore's table has Ushant at 4h 30m and Norie's at 3h 47m."""
    norie = at_rest(*IROISE, epitome="norie")
    moore = at_rest(*IROISE, epitome="moore")
    when = norie.clock.ship_time
    place = Position(48.30, -5.05)
    n = norie.navigation.book_tide(place, when)
    m = moore.navigation.book_tide(place, when)
    assert n.area == m.area and n.rate_kn == m.rate_kn
    assert n.port.name == m.port.name == "Ushant"
    assert (m.high_water - n.high_water) == timedelta(minutes=43)
    assert n.along_kn != m.along_kn


def test_no_line_of_the_masters_tide_reads_the_worlds_tide_or_the_ships_true_place():
    """Item 7: the world keeps the truth and the captain keeps his account, for the tide
    as for the position. The functions that work the master's tide, the traverse, the
    doubt and a shaped course name neither the world's tide nor the truth's position."""
    import inspect

    nav = K.Navigation
    for fn in (
        nav.book_tide,
        nav._tide_between,
        nav._tide_port,
        nav._high_waters_about,
        nav.tide_allowed,
        nav._say_tide,
        nav._working,
        nav._account_with,
        nav.account_now,
        nav.doubt_now,
        nav.bring_up,
        nav._peg,
        nav.shape_for,
        nav._make_good,
        nav._line_shore,
        nav.allow_set,
        nav.allow_tide_by_book,
        nav.almanac_age_days,
        K.Reckoning.advance,
    ):
        source = inspect.getsource(fn)
        for word in (
            "world.position",
            "tide_state",
            ".world.tide.",
            ".world.tide,",
            ".world.tide)",
            "stream_at",
            "tide_height",
            "Tide.at",
        ):
            assert word not in source, (fn.__name__, word)
    from freesail.world import tide as tide_mod

    directions = inspect.getsource(tide_mod.Directions) + inspect.getsource(tide_mod.BookStream)
    assert "axis_deg" not in directions and "phase_h" not in directions


# -- item 8: the captain's word, and the master's --------------------------------------------------


def test_the_captains_set_replaces_the_masters_tide_until_he_hands_it_back():
    """Item 8. `allow <n> knots of set to <point>` replaces the master's own tide from
    that moment, and `allow no set` likewise (the captain's word that there is none);
    `allow the tide by the book` hands it back. The reading says whose it is."""
    w = at_rest(*IROISE)
    nav = w.navigation
    r = nav.reckoning
    r.set_position(w.position, 0, sigma_nm=0.3)
    assert w.readings["reckoning"]["tide"]["by"] == "book"
    words = w.readings.words("reckoning")
    assert "by account; the tide allowed: the " in words
    assert words.endswith(
        "by the directions for the Iroise and high water at Ushant by the epitome"
    )
    e = w.submit("allow two knots of set to the west")
    assert e.kind == "reckoning.set_allowance" and e.text == (
        "Allowing two knots of set to the west in the reckoning, by the captain's order, in "
        "place of the master's own tide."
    )
    assert r.set_allowance == (2.0, pytest.approx(1.5 * math.pi))
    assert w.readings.words("reckoning").endswith(
        "the tide allowed: by the captain's order, two knots to the westward"
    )
    start = r.position
    w.run(2 * 3600)
    nav.bring_up()
    de, dn = r.offset_nm(start)
    assert de == pytest.approx(4.0, abs=0.01) and dn == pytest.approx(0.0, abs=0.01)
    e = w.submit("allow no set")
    assert e.text == (
        "No set allowed for in the reckoning, by the captain's order; the master's own tide "
        "is laid by until it is handed back."
    )
    assert w.readings.words("reckoning").endswith("the tide allowed: none, by the captain's order")
    start = r.position
    w.run(3600)
    nav.bring_up()
    assert r.position == start  # no tide at all, though the directions give one here
    for text in ("allow the tide by the book", "allow the tide", "work the tide yourself"):
        w.submit("allow no set")
        e = w.submit(text)
        assert e.kind == "reckoning.set_allowance", (text, e.text)
        assert e.text.startswith(
            "The tide in the reckoning handed back to the master, by the book: "
        ) and e.text.endswith("high water at Ushant by the epitome.")
        assert r.set_allowance is None and w.readings["reckoning"]["tide"]["by"] == "book"
    again = w.submit("allow the tide by the book")
    assert again.text.startswith("The tide in the reckoning is the master's already, by the book: ")
    w.run(3600)
    nav.bring_up()
    assert miles_between(r.position, start) > 0.3  # his own tide again
    refused = w.submit("allow some set")
    assert refused.kind == "order.rejected" and "allow the tide by the book" in refused.text
    # beyond the directions' limits (by his account) he has no statement, and allows none
    # (package 39b: the limits reach Biscay north, 45.9 N; beyond them south of it)
    r.set_position(Position(45.5, -6.0), w.clock.tick)
    assert w.readings.words("reckoning").endswith("the tide allowed: none, in open water")
    r.set_position(w.position, w.clock.tick)
    # the standing dialect takes all three as actions
    for i, text in enumerate(
        ("allow one knot of set to the east", "allow no set", "allow the tide by the book")
    ):
        given = w.submit(f'standing order "tide {i}": at noon then {text}')
        assert given.kind == "standing.given", given.text


def test_the_log_says_when_the_masters_tide_turns_and_when_she_passes_into_other_waters():
    """Item 8. A routine line, kind `reckoning.tide`, when his tide turns and when she
    passes by his account into other waters, with an event for a stand-by and the
    dialect (`the turn of the tide by the reckoning`): the events of the tide's turn were
    the swing at anchor and never came under way."""
    w = at_rest(*IROISE, start=datetime(1805, 6, 15, 13, 0))
    nav = w.navigation
    nav.reckoning.set_position(w.position, 0, sigma_nm=0.3)
    given = w.submit(
        'standing order "the turn": at the turn of the tide by the reckoning then heave the log'
    )
    assert given.kind == "standing.given", given.text
    w.run(13 * 3600)
    lines = [e for e in w.log if e.kind == "reckoning.tide"]
    turns = [e for e in lines if e.data["turn"]]
    assert 2 <= len(turns) <= 3 and all(e.severity is Severity.ROUTINE for e in lines)
    assert {e.data["flood"] for e in turns} == {True, False}
    ebb = next(e for e in turns if not e.data["flood"])
    assert ebb.text.startswith("By the master's tide the ebb makes: allowing ")
    assert ebb.text.endswith(" to the SW by S.") and ebb.data["water"] == "the-iroise"
    gaps = [b.tick - a.tick for a, b in zip(turns, turns[1:], strict=False)]
    assert all(abs(g - K.TIDE_HOURS * 1800.0) < 600 for g in gaps)  # half a tide apart
    assert all(
        R.event_matches(R.EVENTS["the turn of the tide by the reckoning"], e.kind, e.data)
        for e in turns
    )
    fired = [
        e for e in w.log if e.actor == "standing order 'the turn'" and e.kind == "order.accepted"
    ]
    assert len(fired) == len(turns)
    # into other waters, by his account: the line names them, and is no turn
    nav.reckoning.set_position(Position(48.90, -5.20), w.clock.tick, sigma_nm=0.3)
    w.run(300)
    last = [e for e in w.log if e.kind == "reckoning.tide"][-1]
    assert last.text.startswith(
        "By the master's reckoning she is in the open Channel: allowing the "
    )
    assert last.data["turn"] is False and last.data["water"] == "mid-channel"
    assert not R.event_matches(
        R.EVENTS["the turn of the tide by the reckoning"], last.kind, last.data
    )


# -- item 9: a shaped course makes good -------------------------------------------------------


def _sailing(lat: float, lon: float, heading: float, wind_from: float) -> World:
    """The frigate under plain sail with the log hove, the wind well aft (and as far aft
    on the course she will be ordered, so that she keeps her way when she turns to it)."""
    sc = Scenario(
        start_time=datetime(1805, 6, 15, 9, 0),
        wind_from_deg=wind_from,
        wind_speed_kn=12.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=heading,
        position={"lat_deg": lat, "lon_deg": lon},
        region=REGION,
    )
    w = make_world(7, FRIGATE, sc)
    w.submit("set plain sail")
    w.run(1800)
    w.submit("heave the log")
    w.run(120)
    return w


def _held_to(w: World, target: Position, water, hours: float) -> float:
    """Hold the course ordered in a world whose true stream is `water(w)` (knots east and
    north), and give the nearest she passes the place, in miles."""
    w.tide = None  # the world's own tide laid by: the water is what the test says
    nearest = 1e9
    for _ in range(int(hours * 60)):
        east, north = water(w)
        w.ship.extra["water"] = (units.knots_to_ms(east), units.knots_to_ms(north))
        w.run(60)
        nearest = min(nearest, miles_between(w.position, target))
    return nearest


def test_a_course_shaped_across_a_stream_lies_up_tide_by_the_triangle_and_makes_the_place():
    """Item 9, by the owner's ruling: the helm is ordered the course to steer so that, by
    the master's reckoning, she makes good the line from the account to the place. With
    the captain's own set square across the line at half her way, the course ordered lies
    up-tide of the line by the angle the triangle gives (thirty degrees), and a ship that
    holds it in a world whose true stream is that set makes the place within a quarter
    of a mile."""
    w = _sailing(49.0, -6.0, heading=0.0, wind_from=165.0)
    nav = w.navigation
    way = nav._way_kn()
    assert way == nav.last_log_read_kn and way > 4.0
    nav.reckoning.set_position(w.position, w.clock.tick, sigma_nm=0.1)
    no_compass_error(w)
    target = destination(w.position, 0.0, 5.0 * units.NAUTICAL_MILE)
    set_kn = way / 2.0
    w.submit(f"allow {set_kn} knots of set to the east")
    e = w.submit(f"shape a course for {pricked(target)}")
    assert e.kind == "helm.set", e.text
    allowing = e.data["allowing"]
    assert allowing["by"] == "captain" and allowing["made_good"] is True
    assert e.data["line_deg"] == pytest.approx(0.0, abs=0.6)
    up_tide = units.wrap_pi(e.data["heading"] - math.radians(e.data["line_deg"]))
    assert math.degrees(up_tide) == pytest.approx(-30.0, abs=0.2)  # to the westward
    assert "by account, 5 miles. Allowing " in e.text
    assert (
        " of set to the eastward by the captain's order, steer NW by N to make it good." in e.text
    )
    assert e.text.endswith("Helm ordered: steer NW by N (330°).")
    # the log reads over by its marking, so her true way is a little under what he
    # reckoned on: within a quarter of a mile all the same
    passed = _held_to(w, target, lambda _w: (set_kn, 0.0), 1.2)
    assert passed < 0.25, passed
    # without the allowance the same ship in the same water is set a mile and more off
    w = _sailing(49.0, -6.0, heading=0.0, wind_from=165.0)
    w.navigation.reckoning.set_position(w.position, w.clock.tick, sigma_nm=0.1)
    w.submit("allow no set")
    target = destination(w.position, 0.0, 5.0 * units.NAUTICAL_MILE)
    e = w.submit(f"shape a course for {pricked(target)}")
    assert e.data["allowing"]["words"] == "" and "Allowing" not in e.text  # as it was
    assert _held_to(w, target, lambda _w: (set_kn, 0.0), 1.2) > 1.5


def test_a_course_shaped_by_the_masters_own_tide_makes_the_place_where_the_tide_is_the_books():
    """Item 9. The same with the master's own tide: in the Iroise on a spring flood the
    course for a place six miles to the south-east lies up-tide of the line, the words
    give both and say when the allowance lapses, and in a world whose true stream is the
    book's she makes the place within a quarter of a mile. It is worked once: nothing
    alters the helm afterwards."""
    w = _sailing(48.25, -5.15, heading=120.0, wind_from=293.0)
    nav = w.navigation
    nav.reckoning.set_position(w.position, w.clock.tick, sigma_nm=0.1)
    no_compass_error(w)
    target = destination(w.position, 120.0, 6.0 * units.NAUTICAL_MILE)
    tide = nav.tide_allowed()
    assert tide["by"] == "book" and tide["water"] == "the-iroise" and tide["knots"] > 0.5
    e = w.submit(f"shape a course for {pricked(target)}")
    assert e.kind == "helm.set", e.text
    allowing = e.data["allowing"]
    assert allowing["by"] == "book" and allowing["made_good"] is True
    off = math.degrees(units.wrap_pi(e.data["heading"] - math.radians(e.data["line_deg"])))
    way = allowing["way_kn"]
    toward = math.radians(allowing["toward_deg"])
    cross = allowing["knots"] * math.sin(toward - math.radians(e.data["line_deg"]))
    assert off == pytest.approx(-math.degrees(math.asin(cross / way)), abs=0.3) and abs(off) > 3.0
    assert (
        ". Allowing the " in e.text
        and " to make it good; the allowance holds till the tide turns, about " in e.text
    )
    ordered = w.ship.dyn.target_heading

    def book(world: World) -> tuple[float, float]:
        t = world.navigation.book_tide(world.navigation.account_now(), world.clock.ship_time)
        return t.along_kn * math.sin(t.area.set_rad), t.along_kn * math.cos(t.area.set_rad)

    passed = _held_to(w, target, book, 1.3)
    assert passed < 0.25, passed
    assert w.ship.dyn.target_heading == ordered  # the master does not alter the helm


def test_a_course_shaped_with_no_way_on_or_against_too_strong_a_stream_says_so():
    """Item 9. With no way on there is no triangle to work, and the words say so; when
    no course makes the line good at her present way they say so and give the course that
    loses least."""
    w = at_rest(*IROISE)
    w.navigation.reckoning.set_position(w.position, 0, sigma_nm=0.2)
    w.submit("allow two knots of set to the north")
    e = w.submit("shape a course for 48 10 N 4 55 W")
    assert e.kind == "helm.set" and e.data["allowing"]["made_good"] is False
    assert (
        "She has no way on to work an allowance by: two knots of set to the northward by "
        "the captain's order is not allowed for in the course; shape it again when she has "
        "gathered way." in e.text
    )
    assert math.degrees(e.data["heading"]) == pytest.approx(e.data["line_deg"], abs=0.01)
    w = _sailing(49.0, -6.0, heading=0.0, wind_from=165.0)
    nav = w.navigation
    nav.reckoning.set_position(w.position, w.clock.tick, sigma_nm=0.1)
    way = nav._way_kn()
    w.submit(f"allow {round(way * 1.5)} knots of set to the east")
    target = destination(w.position, 0.0, 5.0 * units.NAUTICAL_MILE)
    e = w.submit(f"shape a course for {pricked(target)}")
    assert e.data["allowing"]["made_good"] is False
    assert (
        ", no course makes it good at her present way of " in e.text and " loses least." in e.text
    )
    # the course whose course made good lies nearest the line: up-tide, and before the beam
    off = math.degrees(units.wrap_pi(e.data["heading"] - math.radians(e.data["line_deg"])))
    assert -90.0 < off < -30.0


def test_a_course_shaped_across_a_headland_or_close_along_the_shore_says_so():
    """Item 9. The line is tried against the land as it is against the charted dangers:
    in game 9 a course shaped for Brest from off Roscoff ran across Brittany without a
    word, and a waypoint chosen against the shore "came back clear"."""
    w = at_rest(48.78, -4.00, start=datetime(1805, 6, 14, 9, 0))  # off Roscoff
    w.navigation.reckoning.set_position(w.position, 0, sigma_nm=0.2)
    e = w.submit("shape a course for Brest")
    assert e.kind == "helm.set" and e.data["shore"]["crosses"] is True
    assert " the line crosses the land about " in e.text
    # a point pricked against the shore under Petit Minou, from the mouth of the Goulet
    w = at_rest(48.322, -4.640, start=datetime(1805, 6, 16, 16, 0))
    w.navigation.reckoning.set_position(w.position, 0, sigma_nm=0.1)
    e = w.submit("shape a course for 48 20.1 N 4 36.9 W")
    assert e.kind == "helm.set", e.text
    assert e.data["shore"]["crosses"] is False and e.data["shore"]["distance_m"] < 400
    assert "the line passes the shore under Petit Minou within " in e.text
    # a line that keeps half a mile clear says nothing of the shore, and a course for a
    # town says nothing of the town's own shore
    w = at_rest(48.25, -4.90, start=datetime(1805, 6, 16, 16, 0))
    w.navigation.reckoning.set_position(w.position, 0, sigma_nm=0.1)
    e = w.submit("shape a course for 48 16 N 4 48 W")
    assert e.kind == "helm.set" and "shore" not in e.data and "the land" not in e.text
    w = at_rest(49.90, -4.90, start=datetime(1805, 6, 14, 9, 0))
    w.navigation.reckoning.set_position(w.position, 0, sigma_nm=0.2)
    e = w.submit("shape a course for Falmouth")
    assert e.kind == "helm.set" and "shore" not in e.data, e.text
    chart = w.chart
    assert chart.line_shore(Position(48.78, -4.00), Position(48.39, -4.49), 900.0)[2] is True
    assert chart.line_shore(Position(49.6, -5.5), Position(49.2, -5.5), 900.0) is None


def test_a_cast_the_chart_about_the_account_already_answers_is_kept_whatever_the_search_finds(
    monkeypatch,
):
    """Package 37e, item 4 (found on the frigate's passage, 2026-10-07): the contour is
    searched on rings half a mile apart, and off a steep shore the nearest point the
    search finds may be miles away. Where the chart about the account shows less water on
    one hand and more on the other than the cast, the cast agrees with the account as
    nearly as the chart can say: the account is kept and nothing is narrowed. Off Black
    Head, the account a cable in doubt by a fix, the search made to answer two miles
    off."""
    w = at_rest(50.02, -5.07)
    nav = w.navigation
    nav.reckoning.set_position(w.position, 0, sigma_nm=0.1)
    least, most = w.chart.depth_span(w.position)
    assert units.m_to_fathoms(most - least) > 10.0  # a steep bottom: eleven fathoms to twenty-eight
    far = destination(w.position, 250.0, 2.0 * 1852.0)
    found = []

    def two_miles_off(pos, depth_m, *a, inside=None, **kw):
        found.append(depth_m)
        if inside is not None and not inside(far):
            return None  # package 37j: he looks within his doubt and no further
        return far, 0.0

    # the chart is shared between worlds (`chart.load_chart` caches it), so the search is
    # replaced for this test alone and put back after: left in place it made the cast
    # test below find its water sixteen leagues off whenever the file ran in one process
    monkeypatch.setattr(w.chart, "contour_point", two_miles_off)
    before = nav.doubt_now()
    w.submit("heave the lead")
    w.run(300)
    cast = [e for e in w.log if e.kind == "sounding"][-1]
    assert found and least <= found[0] <= most
    assert cast.data["how"] == K.KEPT and cast.text.endswith(" The account kept.")
    assert error_nm(w) < 0.2
    assert nav.doubt_now()["semi_minor_nm"] >= before["semi_minor_nm"] - 0.001
    # where the chart about the account does not answer the cast, and nothing within his
    # doubt does, the cast does not agree with the chart where he believes her (package
    # 37j; 37e laid the account down on the search's point two miles off, a cable's doubt
    # notwithstanding): the account is kept, and his doubt grown toward that water so far
    # that it lies at the edge of what he would trust the account within
    monkeypatch.setattr(
        w.chart,
        "depth_span",
        lambda pos, step_m=0.0: (units.fathoms_to_m(40.0), units.fathoms_to_m(45.0)),
    )
    kept_at = nav.reckoning.position
    w.submit("heave the lead")
    w.run(300)
    cast = [e for e in w.log if e.kind == "sounding"][-1]
    assert cast.data["how"] is None and cast.data["agrees"] is False
    assert " The cast does not agree with the chart where Mr " in cast.text
    assert cast.text.endswith(
        " believes her; the chart has that water nearest two miles to the WSW of the "
        "account: the account kept, and its doubt widened."
    )
    # not moved toward that water (the tide he allows carries it a cable in the five minutes)
    assert miles_between(nav.reckoning.position, kept_at) < 0.15
    assert miles_between(nav.reckoning.position, far) > 1.8
    holds, _reach = nav.reckoning.within_doubt(K.OBSERVATION_OUT_SIGMAS * 1.001)
    assert holds(far) and not nav.reckoning.within_doubt(K.OBSERVATION_OUT_SIGMAS * 0.99)[0](far)
    assert cast.data["apart"]["grown_nm"] > 0.5


def test_the_brig_hove_to_six_hours_of_a_spring_ebb_in_the_iroise_keeps_an_honest_account():
    """Package 37e, item 12, the proof by a scripted passage: the brig hove to for six
    hours of a spring ebb in the Iroise (12 June 1805, the moon full; slack water by the
    master's tide as she is brought to, the ebb to make) ends with her account inside
    twice the master's doubt
    and nearer the truth than a third of what she drifted. Before 37e the clock stopped
    while she lay to: the account stood where she was brought to and its doubt with it,
    while she drove thirteen miles to the SSE.

    Package 37f: under her topsails alone, as this test first had her, the brig was not
    hove to at all: she came round through the wind and lay with it abaft the other beam,
    going astern at two knots, and thirteen of those miles were her own. She is now hove
    to under plain sail, where she lies five points and a half from the wind on her tack
    forereaching a knot, and drives seven miles in the six hours."""
    w = chart_world(48.38, -5.15, ship=BRIG, heading=300.0, start=datetime(1805, 6, 12, 15, 30))
    w.submit("set plain sail")
    w.submit("brace sharp up on the larboard tack")
    w.run(900)
    w.submit("heave to")
    w.run(600)
    assert "hove_to" in w.ship.extra
    nav = w.navigation
    nav.reckoning.set_position(w.position, w.clock.tick, sigma_nm=0.2)
    start, account = w.position, nav.account_now()
    assert nav.tide_allowed()["words"].startswith("slack water, the ebb to make, ")
    within = []
    for _ in range(6):
        w.run(3600)
        within.append(error_nm(w) <= 2.0 * nav.doubt_now()["semi_major_nm"])
    drifted = miles_between(start, w.position)
    reckoned = miles_between(account, nav.account_now())
    error, doubt = error_nm(w), nav.doubt_now()["semi_major_nm"]
    assert "hove_to" in w.ship.extra  # on her tack the six hours through
    assert 5.0 < drifted < 10.0  # a knot and more: her forereach, her drift and the stream's
    assert 0.7 * drifted < reckoned < 1.3 * drifted  # the account went with her
    assert all(within) and error < 2.0 * doubt  # honest at every hour, and at the end
    assert error < drifted / 3.0
    assert 2.0 < doubt < 6.0  # and no wider than the stream and her drift can have set her


# ---------------------------------------------------------------------------
# Package 40b: the master's slate, and an officer's own reckoning (spec M6 §5)
# ---------------------------------------------------------------------------


def under_way(start: datetime = datetime(1805, 6, 12, 9, 30), seed: int = 7) -> World:
    """The frigate under plain sail off the Lizard, standing ESE across the ebb on the
    westerly, her account from a departure at the start."""
    sc = Scenario(
        start_time=start,
        wind_from_deg=270.0,
        wind_speed_kn=12.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=112.0,
        ship_speed_kn=6.0,
        position={"lat_deg": 49.75, "lon_deg": -5.45},
        region=REGION,
    )
    w = make_world(seed, FRIGATE, sc)
    w.submit("set plain sail")
    w.submit("steer ESE")
    w.run(600)
    w.submit("trim sails")
    return w


def worked_from_the_slate(data: dict) -> Position:
    """The slate's own figures worked by the traverse: from where it begins, each board's
    run along its course with the tide and the drift, and each sight's move."""
    start = data["from"]
    de = dn = 0.0
    boards = [x for x in data["entries"] if x["kind"] == "board"]
    if data["in_hand"]:
        boards.append(data["in_hand"])
    for b in boards:
        c = math.radians(b["course_deg"])
        de += b["run_nm"] * math.sin(c) + b["tide"][0] + b["drift"][0]
        dn += b["run_nm"] * math.cos(c) + b["tide"][1] + b["drift"][1]
    for s in data["entries"]:
        if s["kind"] == "sight":
            de += s["moved"][0]
            dn += s["moved"][1]
    return K._displaced(Position(start["lat_deg"], start["lon_deg"]), de, dn)


def test_the_slate_carries_the_boards_and_sights_since_the_last_fix_and_works_to_the_account():
    """Spec M6 §5 (package 40b): `work my reckoning` gives the master's slate since the
    last fix: where it begins and his doubt there, each board as he laid it down (the
    course with his variation and leeway allowed, the hours, her way by the log, the
    tide he allowed), the sights he worked in since, and the board in hand. Worked by its
    own figures it comes to the account as the master has it now, to the rounding."""
    w = under_way()
    w.run(2 * 3600)
    e = w.submit("work my reckoning")
    assert e.kind == "query.slate"
    assert e.text.startswith("The master's slate since the departure at 09:30: 49° 45' N, ")
    assert 'his doubt then: "I would not trust the reckoning within a mile' in e.text
    assert "by the log" in e.text and "the tide" in e.text
    assert e.text.endswith("Work it, and give your own with 'my reckoning is <position>'.")
    data = e.data
    boards = [x for x in data["entries"] if x["kind"] == "board"]
    assert len(boards) >= 2 and data["in_hand"] is not None
    assert all(b["tide_by"] == "book" for b in boards if b["run_nm"] > 1.0)
    assert miles_between(worked_from_the_slate(data), w.navigation.account_now()) < 0.02
    # the noon's latitude goes on the slate as a sight (or begins it again, taken), and
    # the slate still works to the account
    w.run(3600)
    e = w.submit("work my reckoning")
    noon = [x for x in w.log if x.kind == "reckoning.noon"]
    assert noon
    if "Latitude by observation" in noon[0].text:
        sights = [x["what"] for x in e.data["entries"] if x["kind"] == "sight"]
        assert sights == ["the noon latitude"] or e.data["from"]["what"].startswith(
            "the noon latitude, which laid the account down"
        )
    assert miles_between(worked_from_the_slate(e.data), w.navigation.account_now()) < 0.02


def test_a_fix_or_the_reckoning_set_by_hand_begins_the_slate_again():
    """The slate is wiped at a fix by cross bearings, whatever it did to the account, at
    the reckoning set by hand, and at an observation that laid the account down."""
    w = bay_world()
    w.run(60)
    fix = w.submit("take a fix")
    assert fix.kind == "reckoning.fix", fix.text
    e = w.submit("work my reckoning")
    assert e.text.startswith("The master's slate since the fix by cross bearings (")
    assert e.data["entries"] == []
    w.submit("set the reckoning to 50 05 N 5 00 W")
    e = w.submit("work my reckoning")
    assert e.text.startswith(
        "The master's slate since the reckoning set by the captain's order at 10:01: "
        "50° 05' N, 5° 00' W by account then"
    )
    r = w.navigation.reckoning
    r.slate_sight(w.clock.tick, "a bearing of the Lizard", r.position, K.TAKEN)
    assert r.slate_from["what"] == "a bearing of the Lizard, which laid the account down"


def test_work_my_reckoning_is_answered_never_logged_and_draws_nothing():
    """The slate is a reading in the reply and not a line the whole log keeps, and it
    draws nothing and changes nothing: a ship whose officer works his reckoning every
    hour keeps the log, line for line and to the digest, of one whose officer does not."""
    a, b = under_way(), under_way()
    for _ in range(3):
        n = len(a.log)
        e = a.submit("work my reckoning")
        assert e.kind == "query.slate" and len(a.log) == n
        a.run(3600)
        b.run(3600)
    assert a.log.digest() == b.log.digest()
    assert a.navigation.reckoning.position == b.navigation.reckoning.position


def test_my_reckoning_is_kept_beside_the_masters_moves_nothing_and_is_said_after_noon():
    """`my reckoning is <position>` keeps the station's own figure beside the master's and
    moves nothing; at noon the line after the noon's says it, run on by the log-board,
    beside the master's account before the sight, and it is carried on from that noon
    figure until another is given (the lead's ruling: it does not lapse at noon). A
    ship with none held has no such line, and every other line is the same."""
    w = under_way(start=datetime(1805, 6, 12, 10, 30))
    plain = under_way(start=datetime(1805, 6, 12, 10, 30))
    w.run(3600)
    plain.run(3600)
    nav = w.navigation
    account = nav.account_now()
    mine = K._displaced(account, -1.5, 0.0)  # a mile and a half west of the master's
    e = w.submit(f"my reckoning is {mine.lat_deg:.4f} N {-mine.lon_deg:.4f} W")
    assert e.kind == "reckoning.own", e.text
    assert e.text.startswith("Captain ") and "'s own reckoning: " in e.text
    assert "a mile and a half W of the master's account, within what he would trust it" in (e.text)
    assert e.text.endswith("kept beside the master's, it moves nothing, and is said at noon.")
    assert nav.account_now() == account
    assert w.readings["officers_reckoning"] is None  # it is the captain's own, here
    w.run(3600)
    plain.run(3600)
    log = w.log.all()
    noon = [i for i, x in enumerate(log) if x.kind == "reckoning.noon"]
    assert len(noon) == 1
    own = log[noon[0] + 1]
    assert own.kind == K.OWN_NOON_KIND and own.severity is Severity.NOTABLE
    assert own.text.startswith("The captain's own reckoning (Captain ")
    assert "worked at 11:40 and run on by the log-board: " in own.text
    assert own.data["from_master_nm"] == pytest.approx(1.5, abs=0.1)
    assert own.data["within"] is True
    if "Latitude by observation" in log[noon[0]].text:
        assert "of the master's account before the sight" in own.text
        assert "The latitude by observation lies " in own.text
    # carried on past noon from his own noon figure (the lead's ruling: it does not lapse)
    mine = nav.own["captain"]
    assert (round(mine["lat_deg"], 5), round(mine["lon_deg"], 5)) == (
        own.data["lat_deg"],
        own.data["lon_deg"],
    )
    assert mine["noon_tick"] == own.tick and mine["tick"] == e.tick
    assert w.submit("my reckoning is 49 40 N 5 0 W").kind == "reckoning.own"
    assert nav.own["captain"]["lat_deg"] == pytest.approx(49 + 40 / 60)  # replaced
    assert not [x for x in plain.log if x.kind == K.OWN_NOON_KIND]
    ours = [
        (x.kind, x.text)
        for x in w.log
        if x.kind not in (K.OWN_NOON_KIND, "reckoning.own") and "my reckoning is" not in x.text
    ]
    assert ours == [(x.kind, x.text) for x in plain.log]


def test_a_book_gives_neither_order_and_a_position_must_be_one():
    """A standing order may give neither: the dialect refuses them at entry, and a
    firing that reached one would be refused in words. A position that is not one is
    refused in the words of `set the reckoning to`."""
    w = chart_world(49.8, -5.2)
    for rule in (
        'standing order "x": at noon then work my reckoning',
        'standing order "y": every glass then my reckoning is 49 30 N 5 10 W',
    ):
        e = w.submit(rule)
        assert e.kind == "order.rejected"
        assert "a man's working from the slate, never a book's" in e.text
    e = w.submit("work my reckoning", actor="standing order 'x'")
    assert e.kind == "order.rejected" and "never a book's" in e.text
    e = w.submit("my reckoning is nowhere")
    assert e.kind == "order.rejected"
    assert "'nowhere' is not a position; say 'my reckoning is 49 52 N 6 10 W'." in e.text
    e = w.submit("work my reckoning at once")
    assert e.kind == "order.rejected" and "takes nothing after it" in e.text


def test_a_slate_from_before_the_package_begins_where_the_account_stands():
    """A checkpoint written before package 40b holds a reckoning with no slate: it is
    begun where the account stands when it is first asked for."""
    w = chart_world(49.8, -5.2)
    r = w.navigation.reckoning
    r.slate = None
    r.slate_from = None
    e = w.submit("work my reckoning")
    assert e.kind == "query.slate"
    assert e.text.startswith("The master's slate since the account as it stood at 10:00: ")


def test_a_reading_of_the_account_asked_mid_tick_changes_nothing_another_gets_after_it():
    """Package 37e, found on the naval cruise (2026-10-07): the account brought up to the
    moment is worked once and remembered, and the memory was kept by the tick alone, so
    a reading asked before the traverse board was pegged in a tick gave the next asker
    in that tick the account as it stood before the peg. A game with a chart open, or a
    test watching the log, then sailed a few yards from the game replayed without them,
    and the cruise's digest moved. The memory holds only while nothing the account is
    worked from has changed. Two ships of one seed: one is asked before the peg and
    after it, the other after it only, and they say the same."""
    asked, unasked = (_sailing(49.70, -5.10, 20.0, 225.0) for _ in range(2))
    for w in (asked, unasked):
        w.run(900)
    nav, twin = asked.navigation, unasked.navigation
    before = nav.account_now(), nav.doubt_now()  # a reading, mid-tick
    for n in (nav, twin):
        n._peg()  # the board pegged for this second, as `Navigation.tick` does
    assert nav.account_now() == twin.account_now() != before[0]
    assert nav.doubt_now() == twin.doubt_now()
    # and the log's read coming to hand within the tick is seen at once the same way
    for n in (nav, twin):
        if n is nav:
            n.account_now()
        n.last_log_read_kn = (n.last_log_read_kn or 0.0) + 1.0
    assert nav.account_now() == twin.account_now()
    # whose tide the day's work carried (the noon's last sentence) is noted when the board
    # is pegged and the account worked, never by a reading: asked while the captain's set
    # stood for a moment, the cruise's master had "the captain's set" in his day's work
    for w in (asked, unasked):
        w.submit("allow one knot of set to the east")
        w.run(5)
        if w is asked:
            w.navigation.account_now()
            w.readings.words("reckoning")
            w.navigation.doubt_now()
        w.submit("allow the tide by the book")
    assert nav._tide_used == twin._tide_used
    # and the nearest place of his epitome, remembered by the hundredth of a degree, is
    # that hundredth's own and not the first asker's (two askers in one hundredth on
    # either hand of the line between two places remembered two places)

    class Halved:
        def nearest(self, where):
            return ("north" if where.lat_deg >= 49.2000 else "south"), 0.0

    for n, first in ((nav, 49.2049), (twin, 49.1951)):
        n._ports, n.epitome = None, Halved()
        assert n._tide_port(Position(first, -5.3)) == "north"
    assert asked.log.digest() == unasked.log.digest()


# ---------------------------------------------------------------------------
# Package 37j: the account, amended
# ---------------------------------------------------------------------------

CUTTER = "data/ships/cutter.yaml"


def test_the_merchant_passages_second_noon_against_an_account_fixed_to_three_cables_is_doubted():
    """Item 1, the fold-in's finding (spec M5 §33 item 24): at the merchant passage's
    second noon, in the mouth of the Goulet with the account fixed by cross bearings to
    three cables a minute before, the octant's sight fell five miles and a half to the
    north, a hair over the two doubts together on Linux and a hair under on Windows; 37e
    took it outright on the one and weighed it on the other. The better figure is
    believed: the sight, ten times the account's doubt, is weighed either side of the
    line and the master doubts it, and the account stays within a cable of where the fix
    left it."""
    for off in (5.55, 5.65):  # a hair under the doubts together, and a hair over
        r = K.Reckoning(Position(48.33, -4.60), sigma_nm=0.3)
        obs = r.observe_latitude(48.33 + off / 60.0, 2.5)
        assert (off > K.OBSERVATION_OUT_SIGMAS * (0.3 + 2.5)) is obs.doubted
        assert obs.how == K.WEIGHED and obs.moved_nm < 0.1
        assert obs.moved_nm == pytest.approx(off * 0.09 / (0.09 + 6.25))
    assert K.verdict_words(obs, what="the sight") == (
        "the sight stands five miles and a half to the N of the account, and the account, good "
        "to three cables, is the better figure: the account moved a cable to the N"
    )


def test_the_cruises_chronometer_against_an_account_a_cable_in_doubt_is_doubted():
    """Item 1, 37e's finding on the naval cruise: hove to off Plymouth at 09:00, the
    account a cable in doubt by the land, a longitude by chronometer 7.6 miles out "which
    Mr Harvey would trust within 5 miles" (2.28 one sigma) was taken, and the bearing of
    Penlee half an hour after took it back. Now the account is the better figure: the
    sight is weighed and doubted, and the account kept."""
    r = K.Reckoning(Position(50.30, -4.20), sigma_nm=0.1)
    lon = -4.20 - 7.6 / (60.0 * math.cos(math.radians(50.30)))
    obs = r.observe_longitude(lon, 2.28)
    assert obs.off_nm == pytest.approx(7.6, abs=0.01)
    assert obs.doubted and obs.how == K.KEPT and obs.moved_nm < 0.05
    assert K.verdict_words(obs, what="the sight") == (
        "the sight stands two leagues and a half to the W of the account, and the account, good "
        "to a cable, is the better figure: the account kept"
    )
    w = chart_world(50.30, -4.20, start=datetime(1805, 6, 12, 9, 0))
    nav = w.navigation
    nav.reckoning.set_position(w.position, w.clock.tick, sigma_nm=0.1)
    from freesail.world import sights

    sight = sights.TimeSight(lon, 2.28, 40, w.clock.tick, True)
    nav.chronometer = sights.Chronometer.from_scenario(
        {"maker": "Arnold", "rated": "1805-05-03", "rate_s_per_day": 0.0},
        w.clock.ship_time,
        w.rng.stream("chronometer"),
    )
    real = sights.time_sight
    try:
        sights.time_sight = lambda *a, **k: (sight, "")
        text, data = nav.take_time_sight()
    finally:
        sights.time_sight = real
    assert data["how"] == K.KEPT and miles_between(nav.reckoning.position, w.position) < 0.05
    assert ": the sight stands two leagues and a half to the W of the account" in text
    assert "is the better figure: the account kept." in text


def test_a_cast_that_does_not_agree_within_the_doubt_keeps_the_account_and_widens_it_once():
    """Item 2, from game 10 (the owner's note 2: "a single stray sounding ... caused a
    jump in the reckoning by a mile which was totally unsound"). The cutter in St Mary's
    Sound, the account right and a quarter of a mile in doubt by a fix; the cast laid on
    the chart with no tide taken off (game 10's tide was a fathom off, by package 34's
    flat allowance), so that it reads more water than the chart shows anywhere within his
    doubt. 37e looked five miles about him, found that water a mile and a half off, and,
    the two being further apart than their doubts together, laid the account down there.
    Now he looks within his doubt and no further: the cast does not agree with the chart
    where he believes her, the account is kept, and his doubt is widened so that that
    water lies at the edge of what he would trust it within. The same cast again on the
    same ground is the same thing seen again, and widens nothing further."""
    w = at_rest(49.915, -6.34, start=datetime(1805, 6, 14, 4, 0), ship=CUTTER)
    nav = w.navigation
    nav.reckoning.set_position(w.position, 0, sigma_nm=0.25)
    nav._tide_allowance_m = lambda: 0.0  # the tide not allowed: the cast a fathom too deep
    texts, grown, doubts = [], [], []
    for _ in range(4):
        w.submit("heave the lead")
        w.run(120)
        cast = [e for e in w.log if e.kind == "sounding"][-1]
        texts.append(cast.text)
        assert cast.data["agrees"] is False and cast.data["how"] is None
        grown.append(cast.data["apart"]["grown_nm"])
        doubts.append(nav.doubt_now()["semi_major_nm"])
        assert error_nm(w) < 0.05  # never laid down where the cast says
    assert " The cast does not agree with the chart where Mr " in texts[0]
    assert texts[0].endswith(
        "; the chart has that water nearest a mile and a half to the SE of the account: the "
        "account kept, and its doubt widened."
    )
    assert grown[0] > 0.3 and grown[1:] == [0.0, 0.0, 0.0]
    assert all(t.endswith(": the account kept.") for t in texts[1:])
    assert doubts[0] > 0.6 and max(doubts[1:]) < doubts[0] + 0.01


def test_the_cast_is_reduced_by_the_masters_own_tide_and_the_line_says_it():
    """Item 3. The master reduces a cast to his chart's datum by his own tide (the rise
    and the hour of the nearest place in his epitome to his account), never the world's;
    a merchant with Moore's table has a rise for every place now, where package 34 took a
    flat three metres off every cast whatever the tide (game 10: a fathom out at St Mary's
    near high water). The line says the reduction when it is a fathom or more."""
    w = at_rest(49.905, -6.35, start=datetime(1805, 6, 14, 4, 0), ship=CUTTER)
    nav = w.navigation
    assert nav.epitome.table == "moore"
    port, _ = nav.epitome.nearest(nav.reckoning.position)
    assert port.name == "Scilly" and port.spring_rise_ft == 15.0 and port.rise_judgement
    allowed = nav._tide_allowance_m()
    assert abs(allowed - w.tide_height_m) < 1.0 < abs(K.TIDE_ALLOWANCE_DEFAULT_M - w.tide_height_m)
    w.submit("heave the lead")
    w.run(120)
    cast = [e for e in w.log if e.kind == "sounding"][-1]
    assert cast.data["tide_allowed_m"] == pytest.approx(allowed, abs=0.05)
    assert " of tide allowed by the epitome: " in cast.text and " on the chart. " in cast.text
    assert cast.text.startswith(f"{K.chant(cast.data['fathoms'], True)}; ")
    # his tide, never the world's: the same account and the same moment in a world whose
    # tide is made nothing works the same reduction
    still = at_rest(49.905, -6.35, start=datetime(1805, 6, 14, 4, 0), ship=CUTTER)
    still.tide, still.tide_state = None, None
    assert still.navigation._tide_allowance_m() == pytest.approx(allowed)
    # under a fathom the line says nothing of it: near low water at the neaps
    low = at_rest(49.905, -6.35, start=datetime(1805, 6, 20, 13, 0), ship=CUTTER)
    if low.navigation._tide_allowance_m() < units.fathoms_to_m(1.0):
        low.submit("heave the lead")
        low.run(120)
        assert " of tide allowed" not in [e for e in low.log if e.kind == "sounding"][-1].text


@pytest.mark.parametrize("casts", [True])
def test_the_forenoon_of_16_june_sailed_again_keeps_an_honest_doubt_and_the_noon_is_weighed(casts):
    """Items 1 and 2 together, game 9's forenoon of 16 June sailed again (the brig on the
    ebb in a calm off the Goulet's mouth, the account half a mile out and a quarter of a
    mile in doubt at 08:00, the deep-sea lead every glass). On 37d the casts kept the
    doubt at a quarter of a mile while the account went four miles wrong, and a right
    noon was all but ignored; on 37e it was taken outright against that small doubt. Now
    the master's tide (37e) carries the account with the ebb, a cast is laid down within
    his doubt or not at all, and the truth stays within twice his doubt at every glass;
    at noon the octant's sight (a mile and a half out, as game 9's was) and the account
    stand within their doubts together and are weighed by them."""
    w = at_rest(48.19, -4.80, start=datetime(1805, 6, 16, 8, 0))
    nav = w.navigation
    r = nav.reckoning
    r.set_position(destination(w.position, 0.0, 0.55 * units.NAUTICAL_MILE), w.clock.tick)
    r.P = [[0.23**2, 0.0], [0.0, 0.26**2]]
    for _ in range(7):
        if casts:
            assert w.submit("heave the deep-sea lead").kind == "order.accepted"
        w.run(1800)
        doubt = nav.doubt_now()["semi_major_nm"]
        assert error_nm(w) < 2.0 * doubt and error_nm(w) < 1.0
    assert nav.doubt_now()["sigma_north_nm"] > 1.2  # where 37d's casts left a quarter
    nav.bring_up()
    obs = r.observe_latitude(w.position.lat_deg - 1.4 / 60.0, 2.28)
    assert obs.how == K.WEIGHED and not obs.doubted


def test_each_board_is_laid_down_by_itself(monkeypatch):
    """Item 4, from game 10 (standing off and on off Scilly, the error grew from a quarter
    of a mile to two miles in an hour and three quarters): between workings the account
    was run on along the mean of her headings since the last, and boards on different
    courses were laid down as one board on their mean. Now at every alteration of two
    points and more (and at a tack, a wear, heaving to and filling away) the account is
    worked up to that minute and each board is laid down by itself. The cutter, logged
    every two hours, stands N and E by turns, eighteen minutes a board, the wind SW."""

    def boards(points: float) -> tuple[float, list[int], list[int]]:
        monkeypatch.setattr(K, "BOARD_ALTERATION_POINTS", points)
        w = chart_world(49.4, -5.6, ship=CUTTER, heading=0.0, start=datetime(1805, 6, 10, 13, 10))
        nav = w.navigation
        w.submit("set plain sail")
        w.submit("steer N")
        w.run(1200)
        nav.reckoning.set_position(w.position, w.clock.tick, sigma_nm=0.1)
        ordered = []
        for k in range(5):
            w.run(18 * 60)
            ordered.append(w.clock.tick)
            w.submit("steer E" if k % 2 == 0 else "steer N")
        w.run(18 * 60)
        return error_nm(w), ordered, [t for t, _a, _b in nav.reckoning.track]

    error, ordered, track = boards(K.BOARD_ALTERATION_POINTS)
    for tick in ordered:
        assert any(tick < t <= tick + 3 * 60 for t in track), tick  # worked at the turn
    mean, _, mean_track = boards(99.0)  # the mean of her headings, as before
    assert len(track) >= len(mean_track) + 5
    assert error < 0.6 * mean  # 2.7 miles against 5.4 at this seed


def test_a_fix_by_marks_on_one_hand_leaves_an_honest_account_at_anchor_in_the_bay():
    """Item 5, 37e's finding at anchor in the Bay of Brest: fixes every five minutes by
    three marks between W by N and N by W, each "good to two cables", weighed one after
    another, left the master believing himself good to a cable while three or four
    cables out: the compass's own error is common to all three and, with every mark on
    one hand, moves the fix more than his allowance said, and the weighing narrowed it
    away. Now how far that error moves a fix by these marks is a part of the doubt no fix
    narrows (`_compass_shift_nm`), and the doubt is said along the shore and off it when
    the two differ."""
    w = chart_world(48.345, -4.470, ship=BRIG, heading=250.0, start=datetime(1805, 6, 17, 9, 0))
    w.run(60)
    w.submit("let go the best bower")
    w.run(600)
    nav = w.navigation
    doubts = []
    for _ in range(6):
        e = w.submit("take a fix")
        assert e.kind == "reckoning.fix"
        assert {m["name"] for m in e.data["marks"]} <= {
            "the castle of Brest",
            "Penaleuch point",
            "Portzic",
            "Brest",
        }
        doubt = nav.reckoning.ellipse()["semi_major_nm"]
        doubts.append(doubt)
        assert error_nm(w) < 2.0 * doubt  # honest
        w.run(300)
    assert min(doubts) >= 0.1  # never surer than a cable
    # the words, by marks on one hand whose doubt differs along the shore and off it
    marks = nav._fix_marks()
    lines = [(s, math.radians(s.bearing_deg)) for s in marks[:3]]
    assert K._one_hand([(None, math.radians(b)) for b in (280.0, 330.0, 345.0)]) is not None
    assert K._one_hand([(None, math.radians(b)) for b in (0.0, 120.0, 240.0)]) is None
    shift = K._compass_shift_nm(w.position, lines, K.COMPASS_ALLOWANCE_DEG)
    assert math.hypot(*shift) > 0.05


def test_the_dangers_and_a_shaped_courses_warnings_are_said_to_the_cable_from_the_account():
    """Item 6: `the dangers` and the warnings of a shaped course are drawn from the account
    as it stands and said to the cable, where they were in whole miles (a ledge four cables
    off was "no distance", and a course's line passed every danger "within a mile")."""
    w = chart_world(50.03, -5.02, start=datetime(1805, 6, 12, 10, 0))
    said = w.readings.words("dangers")
    assert said.startswith("the Manacles NW, a mile and a half; ")
    items = w.readings["dangers"]["items"]
    from freesail.world.geo import distance_words

    for i in items:
        assert i["words"].endswith(distance_words(max(units.CABLE, i["metres"])))
    e = w.submit("shape a course for Falmouth")
    assert (
        "; the line passes the Penwin and the Vaze within a cable, the Manacles within two "
        "cables and the Governor within a mile." in e.text
    )
    passes = e.data["dangers"]
    assert passes and all("off_m" in p for p in passes)


def test_the_departure_is_where_she_is_and_the_run_since_noon_does_not_grow_at_anchor():
    """Item 8, the small faults of the reckoning from the review's G3. Every scenario
    opened with the account drawn a mile out: a departure is taken where she is, by the
    land in sight, and the mile is its doubt. And at anchor the run since noon does not
    grow, whatever the stream does past her."""
    w = chart_world(50.12, -5.03, start=datetime(1805, 6, 12, 13, 0))
    nav = w.navigation
    assert nav.reckoning.position == w.position
    assert nav.reckoning.sigma_east_nm == pytest.approx(K.DEPARTURE_SIGMA_NM)
    w.run(60)
    w.submit("let go the best bower")
    w.run(900)
    assert w.at_anchor
    nav.noon_had = True
    nav.bring_up()
    nav.reckoning.noon_mark = (w.clock.tick, nav.reckoning.lat_deg, nav.reckoning.lon_deg)
    nav.reckoning.run_since_noon_nm = 0.0
    runs = []
    for _ in range(4):
        w.run(3600)
        runs.append(nav.since_noon_reading()[0])
    assert runs == [runs[0]] * 4 and runs[0] < 0.05
