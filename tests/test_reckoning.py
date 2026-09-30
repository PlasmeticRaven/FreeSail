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
from datetime import datetime

import pytest

from freesail import units
from freesail.api import readings as R
from freesail.api.session import make_world
from freesail.core.events import Severity
from freesail.core.world import Scenario, World
from freesail.orders.errors import OrderError
from freesail.world import reckoning as K
from freesail.world.geo import Position, bearing_and_distance

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
    r = K.Reckoning(Position(49.0, -6.0), sigma_nm=0.0)
    for h in range(24):
        r.advance(1.0, 0.0, 6.0, (h + 1) * 3600)
    along_before = r.sigma_north_nm
    # a line east and west, four miles north of the account, known to two miles
    moved = r.update_line(0.0, 4.0, 0.0, 1.0, 2.0)
    assert moved == pytest.approx(4.0)
    assert r.lat_deg == pytest.approx(49.0 + 24 * 6.0 / 60.0 + 4.0 / 60.0)
    assert r.sigma_north_nm == pytest.approx(2.0)
    assert r.sigma_east_nm == pytest.approx(r.ellipse()["sigma_east_nm"], abs=0.01)
    assert along_before > 0.0  # and the doubt along the line is what it was
    assert r.set_doubt[1] == 0.0 and r.set_doubt[0] > 0.0


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
    r = K.Reckoning(Position(49.0, -6.0), sigma_nm=0.0)
    for h in range(48):
        r.advance(1.0, math.pi / 2, 6.0, (h + 1) * 3600)
    east = r.sigma_east_nm
    assert r.sigma_north_nm > 2.0
    r.update_latitude(49.05, 2.0)
    assert r.lat_deg == pytest.approx(49.05)
    assert r.sigma_north_nm == pytest.approx(2.0)
    assert r.sigma_east_nm == pytest.approx(east)


def test_the_masters_words_and_the_ellipse():
    r = K.Reckoning(Position(49.5, -6.2), sigma_nm=1.0)
    assert r.words == "49° 30' N, 6° 12' W by account"
    assert r.uncertainty_words == (
        "I would not trust the reckoning within a mile east or west, nor a mile north or south."
    )
    r.P = [[400.0, 0.0], [0.0, 25.0]]
    assert r.uncertainty_words == (
        "I would not trust the reckoning within 20 miles east or west, nor 5 miles north or south."
    )
    e = r.ellipse()
    assert e["semi_major_nm"] == 20.0 and e["semi_minor_nm"] == 5.0
    assert e["major_bearing_deg"] == 90.0  # lying east and west
    d = r.to_dict()
    assert d["words"].endswith("by account") and "ellipse" in d and d["track"]
    assert "lat_deg" in d and "truth" not in str(d)


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
    assert casts[0].severity is Severity.NOTABLE
    assert deep.readings["depth"] is None
    assert deep.readings.words("depth").startswith("no bottom by the last cast")
    # the deep-sea lead with no way on her: a cast, the fathoms, the ground
    assert deep.submit("heave the deep-sea lead").kind == "order.accepted"
    deep.run(20 * 60)
    started = [e for e in deep.log if e.kind == "evolution.started"]
    assert any(e.text.startswith("Pass the deep-sea line forward") for e in started)
    casts = [e for e in deep.log if e.kind == "sounding"]
    assert len(casts) == 2
    assert casts[-1].text.endswith(" fathoms; fine grey sand with black specks.")
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
    assert abs(depth_at_account - cast.data["depth_m"]) <= units.fathoms_to_m(
        K.CONTOUR_TOLERANCE_DEEP_FATHOMS
    )
    assert abs(depth_at_account - truth_depth) < units.fathoms_to_m(5.0)
    # a sounding is a line, not a point (N §3): the account is on the contour, nearer
    # the truth than it was, and still along the contour from it
    before = miles_between(Position(50.0, -5.10), w.position)
    assert miles_between(r.position, w.position) < before
    e = r.ellipse()
    assert e["semi_minor_nm"] <= K.SOUNDING_ACROSS_SIGMA_NM + 0.01
    assert e["semi_major_nm"] > 6.0  # along the contour it stays as it was


def test_a_bearing_of_a_mark_in_sight_and_the_refusals_in_words():
    w = chart_world(49.80, -5.20, heading=0.0)  # ten miles south of the Lizard
    w.run(60)
    assert w.readings["land"]["in_sight"]
    e = w.submit("take a bearing of the Lizard")
    assert e.kind == "bearing.taken"
    assert e.text.startswith("The Lizard bore ") and e.text.endswith(" by estimation.")
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
    error = laid - sighting.bearing_deg
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
    assert "Longitude by account " in text and text.endswith("W.")
    assert noons[0].severity is Severity.NOTABLE
    transit = w.navigation.noon_by_the_sun()
    assert noons[0].ship_time == transit
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
    assert e.text.endswith("north or south.")
    e = w.submit("set the reckoning to 49 30 N 5 10 W")
    assert e.kind == "reckoning.set" and e.text.endswith("by the captain's order.")
    assert w.readings["reckoning"]["words"] == "49° 30' N, 5° 10' W by account"
    e = w.submit("allow one knot of set to the east")
    assert e.kind == "reckoning.set_allowance" and e.text.startswith("Allowing one knot of set")
    assert w.submit("allow no set").text == "No set allowed for in the reckoning."
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
    assert block["words"].endswith("by account") and block["uncertainty"].startswith("I would not")
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
    assert "lizard-point" in ids and SHORE_ID not in ids  # a headland in sight: no shore hail
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
