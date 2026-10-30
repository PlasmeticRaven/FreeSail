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


# ---------------------------------------------------------------------------
# The directions (package 37e): what the master's books say of the streams
# ---------------------------------------------------------------------------


# The waters whose rates, springs and neaps, are the period's own (package 39a).
# (package 79b: the Looe, Mackenzie's survey as White 1835 quotes it, three knots and two)
PERIOD_RATES = {"alderney-race", "the-looe"}
# package 79c: the Mediterranean west's areas that carry the period's constant current (the
# Balearic channels' follows the wind and is none), in the file's order
MED_WEST_CURRENTS = [
    "cape-palos-offing",
    "granada-coast",
    "barbary-inshore-west",
    "barbary-algiers",
    "alboran-sea",
    "med-west-open",
]
# package 79d: the Mediterranean blocks' charts, whose areas carry the coasts' constant sets
# and no tide (`current:` alone), and their areas' ids
MEDITERRANEAN = {"gulf-of-lion", "ligurian-sea", "tyrrhenian"}
MEDITERRANEAN_AREAS = (
    "provence-current",
    "gulf-of-lion-open",
    "riviera-current",
    "bonifacio-strait",
    "ligurian-sea-open",
    "roman-coast-current",
    "tyrrhenian-open",
)


def test_the_directions_state_every_water_in_the_periods_form_beside_the_worlds_figures(tide):
    """Package 37e, item 5: each stream area carries what the sailing directions say of
    it beside the world's own figures, in the form the period's books give: the point
    the flood sets toward (a compass point, never a degree), the rate at springs to the
    half knot and at neaps half of that, and the hour of the tide at which it runs
    strongest to the half hour; with the source, and what of it is judgement said."""
    book = T.load_directions()
    assert [a.id for a in book.areas] == [a.id for a in tide.areas]  # every water, in order
    for said, world in zip(book.areas, tide.areas, strict=True):
        assert said.polygon == world.polygon  # the statement is of the same water
        assert units.parse_compass_point(said.set_point) == pytest.approx(said.set_rad)
        # the point is the world's axis to the nearest point (a book rounds); the open
        # Channel's is the period's own word, which is not the world's axis rounded
        off = abs(units.wrap_pi(said.set_rad - math.radians(world.axis_deg)))
        if said.id != "mid-channel":
            assert off <= math.radians(5.7), (said.id, said.set_point, world.axis_deg)
            assert "set" in said.judgement, said.id
        else:
            assert off == pytest.approx(math.radians(20.0)) and "set" not in said.judgement
        assert (said.spring_kn * 2.0) == round(said.spring_kn * 2.0), said.id  # to the half knot
        if "rates" in said.judgement:
            assert said.neap_kn == pytest.approx(said.spring_kn / 2.0), said.id
        else:
            # package 39a: where the period gives both rates they are the book's (White
            # 1835's survey of the Race: neaps not above 5 1/2 against 7 at springs)
            assert said.id in PERIOD_RATES and said.neap_kn > said.spring_kn / 2.0, said.id
        assert abs(said.spring_kn - world.spring_kn) <= 0.5, said.id
        assert (said.strongest_h * 2.0) == round(said.strongest_h * 2.0), said.id
        assert abs(said.strongest_h - world.phase_h) <= 0.5, said.id
        assert said.source, said.id  # whose each figure is
        assert ("rates" in said.judgement) != (said.id in PERIOD_RATES), said.id
        assert said.rate_kn(1.0) == said.spring_kn and said.rate_kn(0.0) == said.neap_kn
        if said.spring_kn > 0.0:  # package 43b: Torbay's book gives it no stream
            assert said.neap_kn < said.rate_kn(0.5) < said.spring_kn
    # the Fromveur at neaps is the book's half of springs, not the world's five knots
    # (the owner's ruling of 2026-10-07), and is marked judgement
    fromveur = book.by_id("the-fromveur")
    assert (fromveur.set_point, fromveur.spring_kn, fromveur.neap_kn) == ("NE", 7.0, 3.5)
    assert fromveur.judgement == ("set", "rates", "hour") and "JUDGEMENT" in fromveur.source
    assert tide.areas[[a.id for a in tide.areas].index("the-fromveur")].neap_kn == 5.0
    # the open Channel's set is the period's own word for it
    assert book.by_id("mid-channel").set_point == "NE" and book.areas[-1].polygon is None


def test_the_directions_are_looked_up_by_a_position_and_say_nothing_beyond_their_limits():
    """Package 37e, item 5: the master looks a position up in the directions (his
    account, never the ship's place), the first water that holds it; beyond the limits
    of the waters his books cover he has no statement."""
    book = T.load_directions()
    assert book.area_at(Position(48.17, -5.10)).id == "the-iroise"
    assert book.area_at(Position(48.337, -4.60)).id == "the-goulet"
    assert book.area_at(THE_LIZARD).id == "the-lizard"
    assert book.area_at(Position(49.3, -5.0)).id == "mid-channel"  # the rest is the Channel
    south, north, west, east = book.limits
    # package 39a: the limits reach east with the Channel east's chart; package 39b: the
    # directions reach Biscay north, one box over the three (package 39d: the first of the
    # boxes, a box a block)
    assert (south, north, west, east) == (45.9, 51.0, -7.0, -0.9)
    assert book.area_at(Position(49.70, -2.06)).id == "alderney-race"
    assert book.area_at(Position(50.49, -2.45)).id == "portland-race"
    assert book.area_at(Position(50.0, -2.5)).id == "mid-channel"
    for beyond in (Position(47.0, -8.0), Position(49.5, -7.5), Position(51.2, -5.0)):
        assert book.area_at(beyond) is None
    # package 39c: the bay south of Biscay north is Biscay south's open water, its own
    # waters before it
    assert book.area_at(Position(45.5, -6.0)).id == "open-bay-south"
    assert book.area_at(Position(45.60, -1.10)).id == "gironde-passes"
    assert book.area_at(Position(43.47, -3.77)).id == "santander-mouth"
    assert book.area_at(Position(43.36, -8.83)).id == "sisarga-passage"
    assert book.area_at(Position(48.045, -4.77)).id == "raz-de-sein"  # before the Iroise
    assert book.area_at(Position(47.27, -2.20)).id == "loire-mouth"
    assert book.area_at(Position(47.0, -3.0)).id == "open-bay"
    assert T.load_directions() is book  # read once a process, as the tide's tables are


def test_every_place_of_both_epitomes_has_a_rise_and_what_is_judgement_says_so(tide):
    """Package 37j, item 3: the master reduces a cast by his own tide, which wants the
    rise at springs of the nearest place in his table; package 34 gave it only where a
    period figure was in hand and took a flat three metres elsewhere (Moore's table has
    none, so a merchant took three metres off every cast whatever the tide). Every place
    of both tables now has a rise; where the period's table gives none it is marked
    judgement, and is the world's spring range there rounded to the foot."""
    for table in ("norie", "moore"):
        for port in T.Epitome.load(table).ports:
            assert port.spring_rise_ft is not None, (table, port.name)
            if port.rise_judgement:
                _level, consts = tide.constants_at(port.position)
                spring_range_ft = units.m_to_feet(2.0 * (consts["M2"][0] + consts["S2"][0]))
                assert abs(port.spring_rise_ft - spring_range_ft) <= 0.6, (table, port.name)
    # the period's own figures are kept where they were: Fowey's of 1774 for Falmouth
    falmouth = T.Epitome.load("norie").by_name("Falmouth")
    assert falmouth.spring_rise_ft == 15.0 and not falmouth.rise_judgement


# ---------------------------------------------------------------------------
# Package 38: the tide's table over a larger sea (spec M6 §26, item 5)
# ---------------------------------------------------------------------------


def test_the_gauges_within_reach_are_blended_and_beyond_every_gauge_the_nearest_alone(tide):
    """The interpolation is honest about distance: every position of the Channel's
    region blends the eleven gauges as package 34 pinned it (the reach is more than the
    farthest point of the region lies from Dover); off Lisbon, beyond the reach of every
    gauge, the constants are Brest's alone and the state says it is far (package 89: west
    of Portugal's block, whose own gauges serve Lisbon's water and no farther)."""
    assert tide.reach_m == 400 * units.NAUTICAL_MILE
    for pos in (THE_LIZARD, Position(48.0, -7.0), Position(51.0, -3.0), Position(48.0, -3.0)):
        _, consts, nearest_nm, far = tide.constants_about(pos)
        assert not far and nearest_nm < 100.0
        # the blend of all eleven: every gauge's distance within the reach
        assert all(bearing_and_distance(pos, g.position)[1] <= tide.reach_m for g in tide.gauges), (
            pos
        )
    off_lisbon = Position(38.6, -10.5)  # thirty miles west of the block's bound at 10 W
    assert not tide.blocks_at(off_lisbon)
    level, consts, nearest_nm, far = tide.constants_about(off_lisbon)
    gauge, distance_nm = tide.nearest_gauge(off_lisbon)
    assert far and gauge.id == "le-conquet"  # the westernmost of the French gauges
    assert 550.0 < nearest_nm == pytest.approx(distance_nm, abs=1.0)
    assert level == pytest.approx(gauge.mean_level_m, abs=1e-9)  # w x level / w, rounded
    for name, (amp, lag) in consts.items():
        assert amp == pytest.approx(gauge.constants[name][0]) and lag == pytest.approx(
            gauge.constants[name][1]
        )
    state = tide.at(off_lisbon, datetime(1805, 6, 12, 12, 0))
    assert state.far and state.gauge_nm == pytest.approx(nearest_nm)
    assert not tide.at(THE_LIZARD, datetime(1805, 6, 12, 12, 0)).far
    # within the block (package 89) Cascais is near and the place is not far
    inside = tide.at(Position(38.6, -9.4), datetime(1805, 6, 12, 12, 0))
    assert not inside.far and inside.gauge_nm < 10.0


def test_the_stream_areas_belong_to_a_chart_and_beyond_them_there_is_no_stream(tide):
    """`streams.yaml` takes areas by chart: each names its region, the open Channel's
    statement reaches the Channel's bounds and no farther, and beyond every tabulated
    area the world's stream is nought until a block tabulates the water."""
    import yaml

    manifest = yaml.safe_load(open("data/charts/manifest.yaml", encoding="utf-8"))
    names = set(manifest["charts"]) | set(manifest["regions"])
    assert all(a.chart in names for a in tide.areas), [a.chart for a in tide.areas]
    # the Channel's areas as package 34 and 37e made them, and the blocks' beside them
    channel = [a.id for a in tide.areas if a.chart == "channel-west"]
    # package 43b: fourteen with Torbay
    assert (
        len(channel) == 14 and channel[-1] == "mid-channel" and tide.areas[-1].id == "mid-channel"
    )
    # package 39a: the Channel east's areas lie east of 3 W, where no Channel west
    # position reaches, and come before the open Channel, whose bounds hold them
    names = [a.id for a in tide.areas]
    for a in tide.areas:
        if a.chart == "channel-mid":
            assert a.polygon is not None and min(lon for _, lon in a.polygon) > -3.0, a.id
            assert names.index(a.id) < names.index("mid-channel")
    mid = tide.area_at(Position(49.3, -5.0))
    assert mid.id == "mid-channel" and mid.bounds is not None
    # package 39d: off Lisbon is the bar of Lisbon's water now; the open ocean west of
    # Portugal is beyond every area
    assert tide.area_at(Position(38.6, -9.4)).id == "tagus-bar"
    far_out = tide.area_at(Position(37.0, -14.0))
    assert far_out is T.NO_STREAM and far_out.spring_kn == 0.0
    state = tide.at(Position(37.0, -14.0), datetime(1805, 6, 12, 12, 0))
    assert state.stream_kn == 0.0 and state.area_id == "open-sea"
    assert state.height_m > 0.0  # the height is still the nearest gauge's tide
    # package 58a (the cold review's R-04): where no stream runs there is neither flood nor
    # ebb; nought of stream fell back to the axis and read as the flood before
    assert not state.streaming and state.flood is None
    inside = tide.at(Position(38.6, -9.4), datetime(1805, 6, 12, 12, 0))
    assert inside.streaming and inside.flood in (True, False)


def test_far_from_every_place_of_his_table_the_master_says_his_tide_may_be_hours_out():
    """The doubt in the master's words: a day's sail and more from the nearest place in
    his epitome, `the tide by the almanac` says the tide here may differ by hours; near
    a place of the table it says nothing of the kind (as before)."""
    from freesail.api.session import make_world
    from freesail.core.world import Scenario

    def world_at(lat: float, lon: float, chart: str) -> World:
        sc = Scenario(
            start_time=datetime(1805, 6, 12, 10, 0),
            wind_from_deg=270.0,
            wind_speed_kn=10.0,
            gustiness=0.0,
            variability=0.0,
            position={"lat_deg": lat, "lon_deg": lon},
            chart=chart,
        )
        return make_world(7, "data/ships/frigate-36.yaml", sc)

    far = world_at(37.0, -14.0, "atlantic-east")
    words = far.navigation.tide_by_almanac()["words"]
    assert "nearest place in the master's table" in words
    # package 39b: the nearest place of the table off Lisbon was Brouage, 571 miles off
    # (it was Ushant, 621); package 39d put Lisbon in the table (Tofiño's 2h), so the far
    # place is the open sea west of Portugal, Lisbon 252 miles off (package 39e's Funchal
    # is 511)
    assert "may differ by hours" in words and "Lisbon" in words and "252 miles" in words
    near_lisbon = world_at(38.6, -9.4, "atlantic-east").navigation.tide_by_almanac()["words"]
    assert "Lisbon" in near_lisbon and "may differ by hours" not in near_lisbon
    near = world_at(49.9, -5.2, "atlantic-east")
    assert "may differ by hours" not in near.navigation.tide_by_almanac()["words"]


# ---------------------------------------------------------------------------
# Package 39a: the Channel east (spec M6 §26, block 1)
# ---------------------------------------------------------------------------


def test_the_race_of_alderney_runs_south_west_from_half_ebb_to_half_flood_at_whites_rate(tide):
    """White 1835, 'Alderney Tides', p. 132: in the Race the south-western stream begins at
    half-ebb exactly and runs six hours to half-flood, the north-eastern the other six,
    above seven knots at springs and not above five and a half at neaps: the world's
    stream there is strongest about high water to the north-east and about low water to
    the south-west, at springs within White's figures."""
    race = Position(49.70, -2.06)
    start = datetime(1805, 6, 12, 0, 0)  # two days after the new moon of 10 June 1805: springs
    states = [tide.at(race, start + timedelta(minutes=10 * i)) for i in range(6 * 25)]
    assert {s.area_id for s in states} == {"alderney-race"}
    fastest = max(states, key=lambda s: s.stream_kn)
    assert 6.0 < fastest.stream_kn <= 7.5
    for s in states:
        if s.stream_kn > 3.0:
            # north-eastward about high water (the phase near 0), south-westward about low
            north_east = abs(((s.stream_toward_deg - 30.0) + 180.0) % 360.0 - 180.0) < 1.0
            assert north_east == (s.phase_deg < 90.0 or s.phase_deg > 270.0), s
    said = T.load_directions().by_id("alderney-race")
    assert (said.spring_kn, said.neap_kn, said.strongest_h) == (7.0, 5.5, 0.0)
    assert said.judgement == ("set",) and "White 1835" in said.source


def test_the_channel_easts_gauges_were_read_and_are_held_and_the_eleven_do_not_move(tide):
    """The brief: TICON's gauges of the block read as package 34 read the file, the
    eleven gauges and their figures unmoved. The file has Weymouth, St Helier, Saint-Malo
    and Cherbourg (four of the eleven) and Bournemouth and Portsmouth beside them, which
    are held, read by nothing (a twelfth gauge would move every Channel position's
    blend); it has none at St Peter Port, Dartmouth or Portland."""
    import yaml

    doc = yaml.safe_load(open(T.CONSTITUENTS_PATH, encoding="utf-8"))
    # the Channel east's two (Biscay north's nine, package 39b, are held beside them;
    # the Channel's east block's six, package 79b, east of 1 W)
    held = {g["id"]: g for g in doc["held_gauges"] if g["lat_deg"] > 48.5 and g["lon_deg"] < -1.0}
    assert set(held) == {"bournemouth", "portsmouth"}
    assert all(g["mean_level_m"] is None for g in held.values())  # unverified, not invented
    assert len(tide.gauges) == 11 and not {g.id for g in tide.gauges} & set(held)
    assert {"weymouth", "st-helier", "saint-malo", "cherbourg"} <= {g.id for g in tide.gauges}
    # the tide at Saint-Malo's gauge against SHOM's references there (the RAM as the
    # constituents' head quotes them: mean high water springs 12.20 m, low 1.50 m)
    level, consts = tide.constants_at(Position(48.6408, -2.0281))
    springs = consts["M2"][0] + consts["S2"][0]
    assert level + springs == pytest.approx(12.20, abs=0.5)
    assert level - springs == pytest.approx(1.50, abs=0.5)


# ---------------------------------------------------------------------------
# Package 39b: Biscay north's tide (spec M6 §26, the block's item 4)
# ---------------------------------------------------------------------------


def _blocks_gauges(doc, block):
    """A block's gauges as the file has them (package 89: `gauges:` entries with their
    `block:`, after the eleven)."""
    return [g for g in doc["gauges"] if g.get("block") == block]


def _naive_blend(doc):
    """The tide every gauge of the file would give if each served every position: the
    blend the blocks' gauges were held out of until package 89 (their levels unread taken
    as Dover's 3.7 for the trial alone, never in the file)."""
    gauges = [
        {k: v for k, v in g.items() if k != "block"} | {"mean_level_m": g["mean_level_m"] or 3.7}
        for g in doc["gauges"]
    ]
    return T.Tide({**doc, "gauges": gauges}, {"areas": []})


def _the_eleven_alone(doc):
    """The tide the eleven alone give (the world's before package 89, everywhere)."""
    return T.Tide({**doc, "gauges": [g for g in doc["gauges"] if "block" not in g]}, {"areas": []})


def test_the_blocks_gauges_are_read_and_serve_their_own_water_and_not_the_channels(tide):
    """TICON's nine gauges of Biscay north, read in the eleven's form, their mean levels
    SHOM's RAM's; since package 89 `gauges:` entries with `block: biscay-north`, serving
    the positions within the block's bounds and no other, so that the Channel's tide does
    not move (blended everywhere they would move Falmouth's, the finding of 39b) and the
    world's tide over the block is its own gauges'."""
    import yaml

    doc = yaml.safe_load(open(T.CONSTITUENTS_PATH, encoding="utf-8"))
    held = _blocks_gauges(doc, "biscay-north")
    assert [g["id"] for g in held] == [
        "concarneau",
        "port-tudy",
        "le-crouesty",
        "saint-nazaire",
        "paimboeuf",
        "saint-gildas",
        "les-sables-dolonne",
        "la-rochelle-pallice",
        "ile-daix",
    ]
    for g in held:
        assert 46.0 <= g["lat_deg"] <= 48.0 and -4.0 <= g["lon_deg"] <= -1.0, g["id"]
        assert g["record"].startswith("GESLA-2, REFMAR") and 3.0 <= g["mean_level_m"] <= 4.0
        for name in ("M2", "S2", "N2"):
            assert 0.2 < g[name]["amplitude_m"] < 2.0 and 70.0 < g[name]["phase_deg"] < 150.0
    # (north of 42 N and west of 3 E: the Channel east's two of 39a, still held, the
    # Channel's east block's six of 79b and Biscay south's eleven of 39c beside these)
    north_of_42 = [
        g
        for g in doc["gauges"] + doc["held_gauges"]
        if g["lat_deg"] >= 42.0
        and g["lon_deg"] < 3.0
        and g["id"] not in {x.id for x in tide.gauges}
    ]
    assert len(north_of_42) == 2 + 6 + len(held) + len(_blocks_gauges(doc, "biscay-south"))
    assert len(tide.gauges) == 11 and not {g.id for g in tide.gauges} & {g["id"] for g in held}
    assert {g.id for g in tide.block_gauges} >= {g["id"] for g in held}
    # what blending them everywhere would do: the tide at Falmouth moves (and with it
    # every passage); by the rule it does not
    eleven = _the_eleven_alone(doc)
    _, here = tide.constants_at(FALMOUTH)
    _, there = _naive_blend(doc).constants_at(FALMOUTH)
    assert abs(here["M2"][1] - there["M2"][1]) > 0.05  # degrees of phase
    assert tide.constants_about(FALMOUTH) == eleven.constants_about(FALMOUTH)
    # over the block the eleven's blend was wrong: off the Isle of Aix its M2 lagged 160
    # degrees where the gauge's own is 97.7 (two hours late, the Channel's later tide of
    # St Malo and Jersey in the blend); the world's is the gauge's own now
    aix = Position(46.0074, -1.1743)
    assert 150.0 < eleven.constants_at(aix)[1]["M2"][1] < 170.0
    assert abs(tide.constants_at(aix)[1]["M2"][1] - 97.7) < 1.0


def test_the_blocks_stream_areas_keep_off_the_recorded_passages_other_sail(tide):
    """The Raz before the Iroise whose polygon holds it, the block's areas before the open
    Channel's; the open bay's polygon keeps clear of the water where the naval cruise's
    Diamond (eight miles about 48 N 4 55 W) and Harpy (ten about 47 50 N 6 W) patrol, so
    that the recorded passages read the streams they read."""
    from freesail.world.geo import destination

    ids = [a.id for a in tide.areas]
    assert ids.index("raz-de-sein") < ids.index("the-iroise") < ids.index("open-bay")
    assert ids.index("open-bay") < ids.index("mid-channel")
    assert tide.area_at(Position(48.045, -4.77)).id == "raz-de-sein"
    for centre, miles in ((Position(48.0, -4.9167), 8.0), (Position(47.8333, -6.0), 10.0)):
        for bearing in range(0, 360, 15):
            for frac in (0.25, 0.5, 0.75, 1.0):
                p = destination(centre, float(bearing), frac * miles * units.NAUTICAL_MILE)
                assert tide.area_at(p).id in ("mid-channel", "the-iroise", "raz-de-sein"), p
    assert tide.area_at(Position(47.40, -3.00)).id == "islands-passages"
    assert tide.area_at(Position(46.05, -1.20)).id == "aix-road"


# ---------------------------------------------------------------------------
# Package 39c: Biscay south and Galicia
# ---------------------------------------------------------------------------


def test_biscay_souths_gauges_are_read_and_serve_their_block_and_its_tide_is_no_longer_late(tide):
    """TICON's eleven gauges of Biscay south and Galicia, four French and seven Spanish:
    the French mean levels SHOM's RAM's, the Spanish unverified (null). While they were
    held the world blended the Channel's eleven alone, so that over the block its tide was
    the Channel's water and late, at Vigo and much more at Santander; since package 89
    they serve the block (`block: biscay-south`) and its tide is theirs."""
    import yaml

    doc = yaml.safe_load(open(T.CONSTITUENTS_PATH, encoding="utf-8"))
    south = _blocks_gauges(doc, "biscay-south")
    assert [g["id"] for g in south] == [
        "le-verdon",
        "arcachon",
        "boucau-bayonne",
        "socoa",
        "bilbao",
        "santander",
        "gijon",
        "ferrol",
        "corunna",
        "vilagarcia",
        "vigo",
    ]
    for g in south:
        assert 42.0 <= g["lat_deg"] <= 45.9 and -9.33 <= g["lon_deg"] <= -0.9, g["id"]
        if "REFMAR" in g["record"]:
            assert 2.0 <= g["mean_level_m"] <= 3.5, g["id"]
        else:
            assert g["mean_level_m"] is None, g["id"]  # unverified, as Bournemouth's
        for name in ("M2", "S2", "N2"):
            assert 0.2 < g[name]["amplitude_m"] < 1.6 and 55.0 < g[name]["phase_deg"] < 160.0
    assert len(tide.gauges) == 11 and not {g.id for g in tide.gauges} & {g["id"] for g in south}
    held = {g["id"]: g for g in south}
    eleven = _the_eleven_alone(doc)
    for gid, late_deg in (("vigo", 15.0), ("santander", 45.0)):
        g = held[gid]
        at = Position(g["lat_deg"], g["lon_deg"])
        _, was = eleven.constants_at(at)
        assert was["M2"][1] - g["M2"]["phase_deg"] > late_deg, gid
        _, world = tide.constants_at(at)
        assert abs(world["M2"][1] - g["M2"]["phase_deg"]) < 1.0, gid


def test_biscay_souths_stream_areas_are_the_blocks_and_before_the_open_channel(tide):
    """The block's five areas carry `chart: biscay-south` and go before the open
    Channel's; the block's box of the directions' limits is its bounds (package 39d made
    the limits a box a block), every position of it in one of its areas, the open bay the
    rest; west of 7 W north of 45.9 N stays beyond them; the recorded passages' other sail
    read the streams they read."""
    ids = [a.id for a in tide.areas]
    mine = [
        "gironde-passes",
        "santander-mouth",
        "ferrol-narrows",
        "sisarga-passage",
        "open-bay-south",
    ]
    assert [i for i in ids if i in mine] == mine
    assert all(ids.index(i) < ids.index("mid-channel") for i in mine)
    assert {a.chart for a in tide.areas if a.id in mine} == {"biscay-south"}
    book = T.load_directions()
    assert (42.0, 45.9, -9.33, -0.9) in book.boxes
    for lat in (42.1, 43.0, 44.5, 45.8):
        for lon in (-9.3, -8.0, -6.0, -3.0, -1.0):
            said = book.area_at(Position(lat, lon))
            assert said is not None and said.id != "mid-channel", (lat, lon)
    assert book.area_at(Position(47.0, -8.0)) is None
    assert tide.area_at(Position(47.8333, -6.0)).id == "mid-channel"  # Harpy's water


# ---------------------------------------------------------------------------
# Package 39d: Portugal and Cadiz's tide (spec M6 §26, the block's item 4)
# ---------------------------------------------------------------------------


def test_portugals_gauges_are_read_and_serve_their_block_where_le_conquets_tide_was(tide):
    """TICON's five records of the block (Cascais, Lagos, Huelva, Bonanza, Cadiz; none at
    Leixões, Lisbon or Setúbal) read in the eleven's form, the mean levels REDMAR's where
    read and judgement or none where not. While they were held the world's tide over the
    block was the nearest of the eleven alone, far, twice the range and an hour and
    three-quarters late (the finding); since package 89 (`block: portugal`) Cascais has
    its own tide, and no Channel position moves (every one beyond the reach of them all)."""
    import yaml

    doc = yaml.safe_load(open(T.CONSTITUENTS_PATH, encoding="utf-8"))
    held = {g["id"]: g for g in _blocks_gauges(doc, "portugal")}
    assert list(held) == ["cascais", "lagos", "huelva", "bonanza", "cadiz"]
    for g in held.values():
        assert 36.4 <= g["lat_deg"] <= 42.0 and -10.0 <= g["lon_deg"] <= -6.0, g["id"]
    assert (held["huelva"]["mean_level_m"], held["bonanza"]["mean_level_m"]) == (1.96, 1.54)
    assert held["cadiz"]["mean_level_m"] is None  # unverified, not invented
    for g in held.values():
        assert 0.9 < g["M2"]["amplitude_m"] < 1.1 and 55.0 < g["M2"]["phase_deg"] < 65.0
    assert len(tide.gauges) == 11 and not {g.id for g in tide.gauges} & set(held)
    cascais = Position(38.6917, -9.4167)
    level, consts, nearest_nm, far = _the_eleven_alone(doc).constants_about(cascais)
    assert far and nearest_nm > 550.0 and consts["M2"][0] > 2.0  # Le Conquet's, as it was
    level, own, nearest_nm, far = tide.constants_about(cascais)
    assert not far and nearest_nm < 1.0
    assert own["M2"][0] == pytest.approx(0.996, abs=0.01)
    assert level == pytest.approx(2.0, abs=0.05)  # Cascais's and Lagos's judgement, 2.0
    # blended everywhere, these would move no Channel position either (all beyond reach)
    with_levels = [
        {k: v for k, v in g.items() if k != "block"}
        for g in held.values()
        if g["mean_level_m"] is not None
    ]
    eleven = [g for g in doc["gauges"] if "block" not in g]
    blended = T.Tide({**doc, "gauges": eleven + with_levels}, {"areas": []})
    _, here = tide.constants_at(FALMOUTH)
    _, there = blended.constants_at(FALMOUTH)
    assert here["M2"] == pytest.approx(there["M2"])


def test_the_directions_reach_portugal_by_their_own_box_and_the_open_channel_keeps_its_own():
    """`book_limits` is a box a block (package 39d): Portugal's water has the block's
    statements (the bars, the river before Lisbon, Cadiz bay, the open coast), the
    Western Approaches west of 7 W have none (Biscay south has its own box, 39c), and the open
    Channel's statement answers within its own bounds and no farther."""
    book = T.load_directions()
    assert book.boxes[0] == book.limits == (45.9, 51.0, -7.0, -0.9)
    assert (36.4, 42.0, -10.0, -6.0) in book.boxes
    for pos, area in (
        (Position(38.65, -9.33), "tagus-bar"),
        (Position(38.70, -9.15), "tagus-river"),
        (Position(41.145, -8.68), "douro-bar"),
        (Position(36.55, -6.28), "cadiz-bay"),
        (Position(38.0, -9.5), "portuguese-coast"),
    ):
        assert book.area_at(pos).id == area, pos
    # (package 39c: 44 N 8 W is Biscay south's box now; the bay west of it beyond)
    for beyond in (Position(44.0, -12.0), Position(49.5, -7.5), Position(37.0, -14.0)):
        assert book.area_at(beyond) is None, beyond
    mid = book.by_id("mid-channel")
    assert mid.polygon is None and mid.bounds == (47.5, 52.0, -12.0, 2.0)
    assert mid.contains(Position(49.3, -5.0)) and not mid.contains(Position(44.0, -8.0))
    lisbon = T.Epitome.load("norie").by_name("Lisbon")
    assert (lisbon.hw_h, lisbon.hw_m) == (2, 0) and lisbon.rise_judgement
    cadiz = T.Epitome.load("norie").by_name("Cadiz")
    assert cadiz.spring_rise_ft == 10.0 and not cadiz.rise_judgement


# ---------------------------------------------------------------------------
# Package 39f: the Strait's tide and its constant current (spec M6 §26, block 6)
# ---------------------------------------------------------------------------

MID_STRAIT = Position(35.96, -5.55)  # the middle of the Strait, off Tarifa


def test_the_straits_middle_runs_east_on_the_inset_whatever_the_tide_and_the_shores_do_not(tide):
    """The constant current is a stream by area added to the tidal stream (`current:` in
    the streams' file): in the middle of the Strait the water sets east at two knots
    with the tide's two and a half at springs over it, so at the strength of the ebb it
    runs four and a half east and at the strength of the flood half a knot west (Purdy
    1826's westward set across the Strait at full and change); along the shores the tide
    alone, west on the rising water and east on the falling (Tofiño 1787, p. 8); every
    other area of the file names no current, so the Channel's streams are what they were."""
    area = tide.area_at(MID_STRAIT)
    assert area.id == "strait-middle" and area.chart == "strait"
    assert (area.current_toward_deg, area.current_kn) == (90.0, 2.0)
    # (package 79d: the Mediterranean blocks' areas carry the coasts' sets, below)
    assert [a.id for a in tide.areas if a.current_kn and a.chart not in MEDITERRANEAN] == [
        "strait-middle",
        "strait-east-mouth",
        "strait-west-approach",
        # package 79c: the Mediterranean west's currents, some 900 miles from the Channel
        *MED_WEST_CURRENTS,
    ]
    start = datetime(1805, 6, 12, 0, 0)  # springs
    states = [tide.at(MID_STRAIT, start + timedelta(minutes=10 * i)) for i in range(6 * 25)]
    east = [units.ms_to_knots(s.stream_east_ms) for s in states]
    assert 4.0 < max(east) < 4.8 and -0.8 < min(east) < 0.0
    assert sum(east) / len(east) == pytest.approx(2.0, abs=0.15)  # the inset, on the mean
    # the tide's part is the area's own stream: the state less the current
    for s in states:
        tidal = s.stream_east_ms - units.knots_to_ms(2.0)
        assert abs(tidal) <= units.knots_to_ms(s.rate_kn) + 1e-9
    # rising water runs west (the flood is the westward stream, strongest at half flood)
    rising = [units.ms_to_knots(s.stream_east_ms) for s in states if s.rising]
    falling = [units.ms_to_knots(s.stream_east_ms) for s in states if not s.rising]
    assert sum(rising) / len(rising) < 2.0 < sum(falling) / len(falling)
    shore = Position(36.02, -5.55)  # two miles off the Spanish shore east of Tarifa
    assert tide.area_at(shore).id == "strait-spanish-shore" and tide.area_at(shore).current_kn == 0
    shore_east = [
        units.ms_to_knots(tide.at(shore, start + timedelta(minutes=10 * i)).stream_east_ms)
        for i in range(6 * 25)
    ]
    assert sum(shore_east) / len(shore_east) == pytest.approx(0.0, abs=0.2)
    assert all(
        a.current_kn == 0.0
        for a in tide.areas
        if a.chart not in {"strait", *MEDITERRANEAN}  # package 79d
        and a.id not in MED_WEST_CURRENTS  # package 79c
    )


def test_the_master_allows_the_inset_from_his_directions_and_they_reach_the_strait():
    """The directions' statement for the Strait's middle gives the current beside the tide
    (`book: current:`), and the master works it into his account as one more course: in
    the middle of the Strait his tide's words name the current to the eastward. The
    directions reach the Strait by the block's own box in `book_limits` (package 39d's
    list form), the block's bounds: west of it, off the Moorish coast south of Cape
    Spartel's parallel, he has no statement."""
    book = T.load_directions()
    said = book.area_at(MID_STRAIT)
    assert said is not None and said.id == "strait-middle"
    assert (said.current_point, said.current_kn) == ("E", 2.0) and "current" in said.judgement
    assert (35.5, 36.4, -6.5, -5.0) in book.boxes
    assert book.area_at(Position(35.4, -6.3)) is None  # south of the box, no statement
    assert book.area_at(Position(36.10, -5.40)).id == "gibraltar-bay"
    assert book.area_at(Position(36.3, -6.3)).id == "strait-west-approach"
    assert all(
        a.current_kn == 0.0
        for a in book.areas
        if a.id not in {"strait-middle", "strait-east-mouth", "strait-west-approach"}
        and a.id not in MED_WEST_CURRENTS  # package 79c
        and not a.id.startswith(MEDITERRANEAN_AREAS)
    )
    sc = Scenario(
        start_time=datetime(1805, 6, 12, 10, 0),
        wind_from_deg=270.0,
        wind_speed_kn=10.0,
        gustiness=0.0,
        variability=0.0,
        position={"lat_deg": MID_STRAIT.lat_deg, "lon_deg": MID_STRAIT.lon_deg},
        chart="atlantic-east",
    )
    world = make_world(7, FRIGATE, sc)
    allowed = world.navigation.tide_allowed()
    assert allowed["by"] == "book" and allowed["water"] == "strait-middle"
    assert allowed["current_kn"] == 2.0 and allowed["current_toward_deg"] == 90.0
    assert "the current two knots to the E" in allowed["words"]


def test_the_straits_gauges_are_read_and_serve_the_strait_and_move_no_channel_position(tide):
    """TICON's file has Ceuta, Tarifa, Algeciras and Gibraltar (none at Tangier). While
    they were held the world's tide over the Strait was Le Conquet's alone (the nearest of
    the eleven, beyond the reach of every one), marked far: two metres of M2 where
    Gibraltar's own is 0.31. They lie beyond the reach of every position of the Channel's
    and Biscay north's regions, so they would move no recorded passage's tide whatever
    their water; since package 89 (`block: strait`) they serve the Strait, and the world's
    tide there is theirs. Their mean levels unread, the level there stays the eleven's (Le
    Conquet's 3.98 m), as it was, not invented."""
    import yaml

    doc = yaml.safe_load(open(T.CONSTITUENTS_PATH, encoding="utf-8"))
    held = {g["id"]: g for g in _blocks_gauges(doc, "strait")}
    assert list(held) == ["ceuta", "tarifa", "algeciras", "gibraltar"]
    assert all(g["mean_level_m"] is None for g in held.values())  # unverified, not invented
    assert not set(held) & {g.id for g in tide.gauges}
    gib = Position(held["gibraltar"]["lat_deg"], held["gibraltar"]["lon_deg"])
    eleven = _the_eleven_alone(doc)
    was_level, was, was_nm, was_far = eleven.constants_about(gib)
    assert was_far and eleven.nearest_gauge(gib)[0].id == "le-conquet" and was_nm > 700.0
    assert was["M2"][0] > 1.9 and held["gibraltar"]["M2"]["amplitude_m"] == 0.307
    level, own, nearest_nm, far = tide.constants_about(gib)
    assert not far and tide.nearest_gauge(gib)[0].id == "gibraltar" and nearest_nm < 1.0
    assert abs(own["M2"][0] - 0.307) < 0.02
    assert level == was_level == pytest.approx(3.98)  # the eleven's, the gauges' unread
    for g in held.values():
        here = Position(g["lat_deg"], g["lon_deg"])
        for corner in (Position(48.0, -7.0), Position(45.9, -0.9), Position(45.9, -5.0)):
            assert bearing_and_distance(here, corner)[1] > tide.reach_m
    # (their mean levels unread: nought for the trial's arithmetic, which the M2 test
    # ignores) blended everywhere, they would change no Channel or Biscay north position
    added = [
        {**{k: v for k, v in g.items() if k != "block"}, "mean_level_m": 0.0} for g in held.values()
    ]
    trial = T.Tide(
        {**doc, "gauges": [g for g in doc["gauges"] if "block" not in g] + added}, {"areas": []}
    )
    for pos in (FALMOUTH, THE_LIZARD, Position(48.0, -7.0), Position(46.0, -1.2)):
        assert trial.constants_at(pos)[1] == eleven.constants_at(pos)[1]


def test_torbay_is_its_own_water_with_next_to_no_stream(tide):
    """Package 43b: Torbay was the open Channel's water and set a ship at anchor in
    Brixham road by the Channel's knot and more; the bay is its own stream area now
    (Imray 1874 gives it "little stream"), with a fifth of a knot at springs, while off
    the Berry Head the Channel's stream runs as before."""
    brixham_road = Position(50.410, -3.508)
    torbay = Position(50.445, -3.545)
    off_berry_head = Position(50.40, -3.44)
    assert tide.area_at(brixham_road).id == "torbay"
    assert tide.area_at(torbay).id == "torbay"
    assert tide.area_at(off_berry_head).id != "torbay"
    day = datetime(FULL_MOON_1805_06.year, FULL_MOON_1805_06.month, FULL_MOON_1805_06.day)
    inside = max(tide.at(brixham_road, day + timedelta(hours=h)).stream_kn for h in range(25))
    outside = max(tide.at(off_berry_head, day + timedelta(hours=h)).stream_kn for h in range(25))
    assert inside <= 0.25 < outside
    assert T.load_directions().by_id("torbay").spring_kn == 0.0


# ---------------------------------------------------------------------------
# Package 79b: the Channel's east block's tide (the Wight to Dunkirk)
# ---------------------------------------------------------------------------


def test_the_east_blocks_six_gauges_serve_the_block_and_move_no_channel_position(tide):
    """TICON's gauges of the block (Newhaven, Le Havre, Dieppe, Boulogne, Calais, Dunkirk;
    Dover among the eleven), the French mean levels SHOM's RAM's and Newhaven's unverified.
    Every one is within the reach of every Channel position and, blended everywhere, would
    move Falmouth's tide and every recorded passage, so they were held, and the world's
    tide over the block was the eleven's blend, whose range at Newhaven and Dieppe was a
    fifth of the gauges' own. Since package 89 (`block: channel-east`) they serve the
    block's water and no other: Falmouth's tide is the eleven's, the block's its own."""
    import yaml

    doc = yaml.safe_load(open(T.CONSTITUENTS_PATH, encoding="utf-8"))
    held = _blocks_gauges(doc, "channel-east")
    assert [g["id"] for g in held] == [
        "newhaven",
        "le-havre",
        "dieppe",
        "boulogne",
        "calais",
        "dunkirk",
    ]
    assert held[0]["mean_level_m"] is None  # unverified, not invented
    assert all(3.0 < g["mean_level_m"] < 5.5 for g in held[1:])
    assert len(tide.gauges) == 11 and not {g.id for g in tide.gauges} & {g["id"] for g in held}
    # Newhaven's level unread: Dover's taken for the trial blend alone (never in the file)
    trial = [
        {**{k: v for k, v in g.items() if k != "block"}, "mean_level_m": g["mean_level_m"] or 3.7}
        for g in held
    ]
    eleven_doc = [g for g in doc["gauges"] if "block" not in g]
    blended = T.Tide({**doc, "gauges": eleven_doc + trial}, {"areas": []})
    eleven = _the_eleven_alone(doc)
    _, here = tide.constants_at(FALMOUTH)
    _, there = blended.constants_at(FALMOUTH)
    assert here["M2"] != there["M2"]  # blended everywhere they would move the passages
    assert tide.constants_about(FALMOUTH) == eleven.constants_about(FALMOUTH)  # they do not
    for g in (held[0], held[2]):  # Newhaven and Dieppe
        at = Position(g["lat_deg"], g["lon_deg"])
        gauge_range = 2.0 * (g["M2"]["amplitude_m"] + g["S2"]["amplitude_m"])
        _, was = eleven.constants_at(at)
        assert 2.0 * (was["M2"][0] + was["S2"][0]) < 0.5 * gauge_range, g["id"]
        _, world = tide.constants_at(at)
        world_range = 2.0 * (world["M2"][0] + world["S2"][0])
        assert world_range == pytest.approx(gauge_range, abs=0.05), (g["id"], world_range)


def test_the_east_blocks_waters_answer_from_their_own_areas_before_the_open_channels():
    """The block's stream areas are looked up first-match before the open Channel's; the
    block's box is in the directions' limits, every position of it within an area (the
    block's open reach the rest, beyond the open Channel's 2 E too); the polygons keep east
    of 1.3 W, far from the recorded passages' other sail."""
    book = T.load_directions()
    for pos, area in (
        (Position(50.76, -1.12), "spithead-road"),
        (Position(50.71, -0.75), "the-looe"),
        (Position(50.70, 0.30), "beachy-head"),
        (Position(51.25, 1.50), "the-downs-stream"),
        (Position(51.00, 1.45), "strait-of-dover"),
        (Position(51.10, 2.30), "flemish-banks"),
        (Position(49.47, 0.10), "seine-mouth"),
        (Position(50.20, 0.00), "channel-east-open"),
        (Position(49.20, 2.40), "channel-east-open"),
    ):
        assert book.area_at(pos).id == area, (pos, area)
    assert {"south": 49.0, "north": 51.5, "west": -1.0, "east": 2.5} in [
        {"south": s, "north": n, "west": w, "east": e} for s, n, w, e in book.boxes
    ]
    for a in book.areas:
        if a.id in {"spithead-road", "the-looe", "channel-east-open"}:
            assert min(lon for _, lon in a.polygon) > -1.3


# ---------------------------------------------------------------------------
# Package 89: the held gauges' water
# ---------------------------------------------------------------------------


def test_every_blocks_gauge_names_its_block_and_the_loader_refuses_one_that_does_not(tide):
    """Item 2: the blocks' gauges are `gauges:` entries each with its `block:`, a region
    of the chart's manifest, the eleven with none; the loader refuses a `block:` that
    names no region, a block the manifest does not name, and a gauge with no block and no
    mean level (a block's gauge that lost its block would serve every position). The
    figures are the eleven's form, unmoved; Newhaven's mean level stays null. Each gauge
    lies within its own block's bounds."""
    import yaml

    doc = yaml.safe_load(open(T.CONSTITUENTS_PATH, encoding="utf-8"))
    bounds = T.region_bounds()
    blocks = [g for g in doc["gauges"] if "block" in g]
    assert [g["id"] for g in doc["gauges"] if "block" not in g] == [g.id for g in tide.gauges]
    assert len(tide.gauges) == 11 and len(tide.block_gauges) == len(blocks) == 73
    for g in blocks:
        s, n, w, e = bounds[g["block"]]
        assert s <= g["lat_deg"] <= n and w <= g["lon_deg"] <= e, g["id"]
    assert {g["block"] for g in blocks} == {
        "biscay-north",
        "biscay-south",
        "portugal",
        "madeira",
        "azores",
        "strait",
        "channel-east",
        "mediterranean-west",
        "balearics",
        "gulf-of-lion",
        "ligurian-sea",
        "tyrrhenian",
    }
    newhaven = next(g for g in blocks if g["id"] == "newhaven")
    assert newhaven["mean_level_m"] is None
    assert next(g for g in tide.block_gauges if g.id == "newhaven").mean_level_m is None
    eleven = [g for g in doc["gauges"] if "block" not in g]
    dieppe = next(g for g in blocks if g["id"] == "dieppe")
    for bad, words in (
        ({**dieppe, "block": None}, "names no region"),
        ({**dieppe, "block": []}, "names no region"),
        ({**dieppe, "block": "the-thames"}, "does not name"),
        ({k: v for k, v in newhaven.items() if k != "block"}, "no mean level and no block"),
    ):
        with pytest.raises(ValueError, match=words):
            T.Tide({**doc, "gauges": eleven + [bad]}, {"areas": []})
    # a block that became two or three may be named as a list of its regions
    both = T.Tide(
        {**doc, "gauges": eleven + [{**dieppe, "block": ["channel-east", "channel-mid"]}]},
        {"areas": []},
    )
    assert both.block_gauges[0].blocks == ("channel-east", "channel-mid")


def test_the_fill_is_raised_by_the_level_the_worlds_tide_gives_each_cell():
    """`tools/build_charts.py`'s `mean_level_grid`, which raises GEBCO's fill to the
    chart's datum, reads the gauges that serve each cell (`Tide.gauges_at`, package 93):
    within a block the block's own water, as the world's tide gives it (over the Channel's
    east block a metre above the eleven's at Dieppe, at Mahón its own 0.20 m where the
    eleven gave Saint-Malo's 6.83), where no gauge of the blend has a level (the Strait's)
    the eleven's as the tide takes it, and outside every block the eleven alone, the raise
    unchanged (package 89 had kept the eleven's everywhere until the tiles were rebuilt)."""
    import importlib.util
    import sys
    from pathlib import Path

    import yaml

    root = Path(__file__).resolve().parents[1]
    spec = importlib.util.spec_from_file_location(
        "build_charts", root / "tools" / "build_charts.py"
    )
    tool = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = tool
    spec.loader.exec_module(tool)
    doc = yaml.safe_load(open(T.CONSTITUENTS_PATH, encoding="utf-8"))
    eleven = T.Tide(
        {**doc, "gauges": [g for g in doc["gauges"] if "block" not in g]}, {"areas": []}
    )
    tide = T.load_tide()
    cell = tool.FILL_LEVEL_CELL_DEG

    def cells(box):
        grid = tool.mean_level_grid(box)
        rows, cols = grid.values.shape
        for r in range(rows):
            for c in range(cols):
                centre = Position(grid.south + (r + 0.5) * cell, grid.west + (c + 0.5) * cell)
                yield centre, float(grid.values[r, c])

    # the Channel's east block, its gauges' water; Dieppe's cell a metre over the eleven's
    for centre, level in cells({"south": 49.85, "north": 50.0, "west": 1.0, "east": 1.15}):
        assert level == pytest.approx(tide.constants_at(centre)[0], abs=1e-4)
        if tide.blocks_at(centre):
            assert level - eleven.constants_at(centre)[0] > 0.9
    # Mahón's water (balearics), its gauges' level and not Saint-Malo's
    for centre, level in cells({"south": 39.8, "north": 39.95, "west": 4.2, "east": 4.35}):
        assert tide.blocks_at(centre) == {"balearics"}
        assert level == pytest.approx(tide.constants_at(centre)[0], abs=1e-4)
        assert level < 0.3 < 6.0 < eleven.constants_at(centre)[0]
    # the Strait: its gauges' levels unread, the eleven's level there, as the world's
    for centre, level in cells({"south": 35.9, "north": 36.05, "west": -5.6, "east": -5.45}):
        assert tide.blocks_at(centre) == {"strait"}
        assert level == pytest.approx(eleven.constants_at(centre)[0], abs=1e-4)
        assert level == pytest.approx(tide.constants_at(centre)[0], abs=1e-4)
    # outside every block (the Channel west, off the Lizard and Ushant): the eleven alone,
    # the raise every tile there was built by, unchanged
    for box in (
        {"south": 49.8, "north": 49.95, "west": -5.3, "east": -5.15},
        {"south": 48.3, "north": 48.45, "west": -5.2, "east": -5.05},
    ):
        for centre, level in cells(box):
            assert not tide.blocks_at(centre)
            assert level == pytest.approx(eleven.constants_at(centre)[0], abs=1e-4)
