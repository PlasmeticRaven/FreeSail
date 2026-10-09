"""The readings registry (spec M4 §2): every reading on both ships against the physics'
own numbers, the absent ones' sentences, the per-tick cache, and parity with the snapshot.
"""

from __future__ import annotations

import math
import random
from pathlib import Path

import pytest

from freesail import units
from freesail.api import queries
from freesail.api import readings as R
from freesail.api.session import make_world
from freesail.core.world import Scenario, World
from freesail.crew import bill
from freesail.crew.model import fatigue_words
from freesail.ship.parts import SailState

ROOT = Path(__file__).resolve().parents[1]
SHIPS = [ROOT / "data/ships/frigate-36.yaml", ROOT / "data/ships/topsail-schooner.yaml"]


def world_for(path: Path, heading: float = 293.0) -> World:
    w = make_world(
        7,
        path,
        Scenario(wind_from_deg=0.0, wind_speed_kn=15.0, ship_heading_deg=heading, gustiness=0.0),
    )
    w.submit("set plain sail")
    w.run(900)
    w.submit("brace sharp up on the starboard tack")
    w.run(300)
    return w


@pytest.fixture(params=SHIPS, ids=[p.stem for p in SHIPS])
def world(request) -> World:
    return world_for(request.param)


# -- the rows ---------------------------------------------------------------------------


def test_every_row_of_the_spec_is_registered():
    words = set(R.REGISTRY.words())
    for phrase in (
        "the true wind",
        "the apparent wind",
        "the heading",
        "the course",
        "the speed",
        "the leeway",
        "the heel",
        "the helm",
        "the watch",
        "the time",
        "daylight",
        "the <sail>",
        "the strain",
        "the hands on deck",
        "the watch below",
        "the well",
        "the glass",
        "the depth",
        "a sail in sight",
    ):
        assert phrase in words, phrase
    assert {r.kind for r in R.REGISTRY} <= set(R.KINDS)
    # the true wind is three readings behind one phrase: its speed, its direction, and
    # (package 29b) the instant's against its ten-minute mean
    assert [r.kind for r in R.REGISTRY.by_words("the true wind")] == [
        "speed",
        "direction",
        "gust",
    ]
    assert [r.kind for r in R.REGISTRY.by_words("the mean wind")] == ["speed", "direction"]


def test_absent_readings_carry_their_sentences():
    for id, word in (("well", "well"),):
        row = R.REGISTRY.get(id)
        assert row.is_absent and row.getter is None
        assert word in row.absent and "yet" in row.absent
    # a sail in sight arrived with package 35 (spec M5 §25): the lookout's, the pilot
    # cutter the first sail; None without a chart, in the chart's words
    row = R.REGISTRY.get("sail_in_sight")
    assert not row.is_absent and row.kind == "sight"
    # the lead's cast arrived with package 33a (spec M5 §15): `the depth` is a reading,
    # None before a cast, in the reckoning's words on a ship with no position
    row = R.REGISTRY.get("depth")
    assert not row.is_absent and row.kind == "depth"
    assert World(seed=1).readings["depth"] is None
    assert World(seed=1).readings.words("depth") == R.NO_RECKONING_WORDS
    # the glass arrived with package 30 (spec M5 §5): a reading, None on a ship without one
    row = R.REGISTRY.get("glass")
    assert not row.is_absent and row.kind == "glass"
    w = World(seed=1)
    assert w.readings["glass"] is None
    assert w.readings.words("glass") == R.NO_GLASS_WORDS
    # the sun arrived with package 26: daylight is a reading, not an absence
    row = R.REGISTRY.get("daylight")
    assert not row.is_absent and row.kind == "daylight"
    assert w.readings["daylight"] == "day", "04:00 on 1 June at 50 N is four minutes past sunrise"


def test_events_and_intervals_of_the_spec():
    for words in (
        "sunset",
        "sunrise",
        "eight bells",
        "the change of the watch",
        "a strain warning",
        "a sail shaking",
        "a spar carrying away",
        "a sail blown out",
        "all hands called",
        "the watch piped down",
        "a sighting",
        "a sounding",
        "a landfall",
        "noon",
    ):
        assert words in R.EVENTS, words
    # the lookout's sighting (package 32) and the lead's sounding (package 33a) are raised
    assert not R.EVENTS["a sighting"].absent and not R.EVENTS["a sounding"].absent
    assert R.event_matches(R.EVENTS["a landfall"], "lookout.sighting", {"landfall": True})
    assert not R.event_matches(R.EVENTS["a landfall"], "lookout.sighting", {"landfall": False})
    assert R.event_matches(R.EVENTS["eight bells"], "clock.bell", {"bells": 8})
    assert not R.event_matches(R.EVENTS["eight bells"], "clock.bell", {"bells": 4})
    assert R.INTERVALS["a glass"] == R.INTERVALS["a bell"] == 1800
    assert R.INTERVALS["an hour"] == 3600 and R.INTERVALS["a watch"] == 14400


# -- every reading against the physics, on both ships --------------------------------------


def test_readings_are_the_physics_own_numbers(world: World):
    r = world.readings
    d = world.ship.dyn
    assert r["true_wind_speed"] == world.wind.effective_speed
    assert r["true_wind_from"] == world.wind.direction_from
    assert r["apparent_wind_angle"] == d.apparent_wind_angle
    assert r["apparent_wind_speed"] == d.apparent_wind_speed
    assert r["heading"] == d.heading
    assert r["course"] == d.target_heading
    assert r["speed"] == d.speed and r["speed"] > 0.5
    assert r["leeway"] == d.leeway
    assert r["heel"] == d.heel and r["heel"] != 0.0
    assert r["helm"] == d.rudder
    assert r["watch"] == world.clock.watch().lower() == "morning watch"
    assert r["time"]["bells"] == 8 and r["time"]["watch"] == "Morning watch"
    # the strain: the worst ratio aboard, and per part
    worst = max(
        p.strain_ratio
        for p in world.ship.parts.values()
        if not p.wrecked and getattr(p, "sent_down", False) is False
    )
    assert r.value("strain") == pytest.approx(worst) and worst > 0
    for pid, part in world.ship.parts.items():
        assert r.value("strain", pid) == part.strain_ratio
    # every sail: state as the part has it
    for sid, sail in world.ship.sails.items():
        v = r.value("sail", sid)
        assert v["state"] == sail.state.value
        assert v["reefs"] == sail.reefs
        assert v["aback"] == (sail.backed and sail.state is SailState.SET)
    # the hands: the watch bill's count and fatigue in the crew's own words
    crew = world.ship.extra["crew"]
    deck = bill.on_deck(crew, world.clock)
    assert r["hands_on_deck"]["count"] == len(deck)
    mean = round(sum(s.fatigue for s in deck) / len(deck), R.FATIGUE_DECIMALS)
    assert r["hands_on_deck"]["fatigue"] == mean
    assert r["hands_on_deck"]["words"] == fatigue_words(mean)
    assert r["watch_below"]["count"] == len(bill.below(crew, world.clock))
    # the same values by the other doors
    assert r.as_dict()["speed"] == d.speed
    assert r.get("speed") == d.speed and r.get("no such reading", 3) == 3


def test_a_sail_shaking_and_aback_read_from_the_physics(world: World):
    """A drawing sail with the apparent wind inside its luff is shaking; one with the
    wind on its fore face is aback, not shaking (physics/sails.py)."""
    ship = world.ship
    square = next(s for s in ship.sails.values() if s.cls == "square" and s.is_set)
    r = world.readings
    drawing = [
        s.id
        for s in ship.sails.values()
        if s.is_set and not r.value("sail", s.id)["shaking"] and not r.value("sail", s.id)["aback"]
    ]
    assert drawing, "on a reach some sail draws"
    if ship.spec.rig == "topsail-schooner":
        # the schooner sails by her fore-and-aft canvas with the square topsail shaking
        # (physics/sails.py): the reading says so
        assert r.value("sail", square.id)["shaking"]
    else:
        assert square.id in drawing
    # brought up toward the wind: the frigate comes head to wind and every sail shakes or
    # is aback. The schooner, whose sheets stand as trimmed (package 32e), luffs as she is
    # brought up, loses her way and goes through the wind into irons, her canvas aback by
    # its sheets on what is now the weather side; before, the free tending flattened her
    # sheets as she came up and she stalled at some thirty-four degrees apparent with her
    # fore-and-aft canvas still drawing (the docstring of sails.py then)
    world.submit("trim sails")
    world.run(150)
    world.submit("steer north")
    world.run(600)
    awa = units.rad_to_deg(abs(ship.dyn.apparent_wind_angle))
    assert awa < (45 if ship.spec.rig == "topsail-schooner" else 25), awa
    for s in ship.sails.values():
        if not s.is_set:
            continue
        if any(ln.side is None for ln in ship.sheets_of(s)):
            continue  # a boom sail swings to leeward of whatever wind she has, and fills
        v = world.readings.value("sail", s.id)
        assert v["shaking"] or v["aback"], (s.id, v, awa)
    # the physics' own flag decides "aback"
    square.backed = True
    world.record("routine", "test.bump", "readings recomputed")  # a new log line: a new view
    v = world.readings.value("sail", square.id)
    assert v["aback"] and not v["shaking"]


def test_readings_on_the_schooner_name_her_own_sails():
    w = world_for(SHIPS[1])
    r = w.readings
    assert set(w.ship.sails) and all(r.value("sail", s) is not None for s in w.ship.sails)
    assert r.value("sail", "no.such.sail") is None
    assert r.value("strain", "no.such.part") is None


# -- the cache ----------------------------------------------------------------------------


def test_the_view_is_cached_per_tick_and_per_order():
    w = world_for(SHIPS[0])
    a = w.readings
    assert w.readings is a, "the same tick, the same view"
    w.tick()
    b = w.readings
    assert b is not a, "a new tick, a new view"
    # a course laid on the tack she is on (package 37m: east from her head on the starboard
    # tack lies across the wind's eye, and she would be put about for it, the course given
    # her only as she comes round)
    w.submit("steer west")
    c = w.readings
    assert c is not b, "an order writes a log line and may change the ship at once"
    assert c["course"] == pytest.approx(3 * math.pi / 2), "the course ordered, read at once"
    # the view itself remembers what it read: a getter is called once per (id, part)
    calls = []
    original = R.REGISTRY.get("speed")
    R.REGISTRY.add(
        R.Reading(
            "speed", original.words, original.kind, original.unit, lambda wd, p: calls.append(1)
        )
    )
    try:
        v = w.readings
        v["speed"]
        v["speed"]
        assert len(calls) == 1
    finally:
        R.REGISTRY.add(original)


# -- parity with the snapshot ----------------------------------------------------------------


def test_snapshot_reads_its_instruments_from_the_registry(world: World):
    snap = queries.snapshot(world)
    r = world.readings
    assert snap["wind"]["true_from"] == r["true_wind_from"]
    assert snap["wind"]["true_speed"] == r["true_wind_speed"]
    assert snap["wind"]["apparent_angle"] == r["apparent_wind_angle"]
    assert snap["wind"]["apparent_speed"] == r["apparent_wind_speed"]
    assert snap["ship"]["heading"] == r["heading"]
    assert snap["ship"]["speed_through_water"] == r["speed"]
    assert snap["ship"]["leeway"] == r["leeway"]
    assert snap["ship"]["heel"] == r["heel"]
    assert snap["ship"]["rudder"] == r["helm"]
    assert snap["bell"] == r["time"]
    for s in snap["sails"]:
        assert s["state"] == r.value("sail", s["id"])["state"]
        assert s["strain_ratio"] == r.value("strain", s["id"])
    for s in snap["spars"] + snap["lines"]:
        assert s["strain_ratio"] == r.value("strain", s["id"])
    assert snap["crew"]["on_deck"] == r["hands_on_deck"]["count"]
    assert snap["crew"]["fatigue_mean_on_deck"] == r["hands_on_deck"]["fatigue"]


def test_a_reading_replaced_in_the_registry_reaches_rule_and_snapshot_alike():
    """Parity is structural: swap a row and both doors see the swap."""
    w = world_for(SHIPS[0])
    original = R.REGISTRY.get("heel")
    R.REGISTRY.add(
        R.Reading("heel", original.words, original.kind, original.unit, lambda wd, p: 0.25)
    )
    try:
        w.record("routine", "test.bump", "a new view")
        assert w.readings["heel"] == 0.25
        assert queries.snapshot(w)["ship"]["heel"] == 0.25
    finally:
        R.REGISTRY.add(original)


def test_describe_value_speaks_the_nautical_units():
    assert R.describe_value(R.REGISTRY.get("true_wind_speed"), units.knots_to_ms(24)) == "24 knots"
    assert R.describe_value(R.REGISTRY.get("true_wind_from"), math.radians(315)) == "from NW"
    assert R.describe_value(R.REGISTRY.get("apparent_wind_angle"), math.radians(-50)) == (
        "50 degrees on the larboard bow"
    )
    assert R.describe_value(R.REGISTRY.get("heel"), math.radians(-12)) == "12 degrees"
    assert R.describe_value(R.REGISTRY.get("watch"), "middle watch") == "the middle watch"
    assert R.describe_value(R.REGISTRY.get("glass"), None) == "not to be had"


# -- package 28c: the readings' words (playtests 1 and 3) --------------------------------


def test_the_apparent_wind_is_named_by_the_points_of_sail():
    """Playtest 3: 119 degrees apparent read "on the larboard bow", which is abaft the
    beam. The words follow the primer's chapter 2: the bow, the beam, the quarter abaft
    the beam, astern (`units.wind_bearing_words`, half a point either side of each)."""
    row = R.REGISTRY.get("apparent_wind_angle")
    said = {d: R.describe_value(row, math.radians(d)) for d in (-50, 84, 90, -119, 165, 180)}
    assert said == {
        -50: "50 degrees on the larboard bow",
        84: "84 degrees on the starboard bow",
        90: "90 degrees on the starboard beam",
        -119: "119 degrees on the larboard quarter, abaft the beam",
        165: "165 degrees astern, a little on the starboard quarter",
        180: "180 degrees right astern",
    }
    # the band edges are the primer's points: seven and a half, eight and a half, fourteen
    # and a half, fifteen and a half
    assert units.wind_bearing_words(units.points_to_rad(7.49)).endswith("bow")
    assert units.wind_bearing_words(units.points_to_rad(7.51)).endswith("beam")
    assert units.wind_bearing_words(units.points_to_rad(8.51)).startswith("on the starboard q")
    assert units.wind_bearing_words(units.points_to_rad(14.51)).startswith("astern")
    assert units.wind_bearing_words(units.points_to_rad(15.51)) == "right astern"


def test_course_and_leeway_are_not_readings_with_no_way_on():
    """Playtest 1's "Leeway 145°" from a standing start and playtest 3's course NW by W
    with the heading E by N in stays: under `READING_SPEED_FLOOR_KN` of headway the
    course and the leeway read None, and in words say why."""
    from freesail.agents import tools

    assert R.READING_SPEED_FLOOR_KN == 0.5
    w = make_world(7, SHIPS[0], Scenario(wind_from_deg=0.0, ship_heading_deg=180.0))
    d = w.ship.dyn
    assert d.u == 0.0
    r = w.readings
    assert r["course"] is None and r["leeway"] is None
    words = tools.readings_words(w)
    assert words["course"] == words["leeway"] == R.NO_WAY_WORDS
    assert R.NO_WAY_WORDS == "no way on; course and leeway not meaningful"
    assert queries.snapshot(w)["ship"]["leeway"] is None  # the instrument says no way on
    # sternway, as hove to: said so
    d.u, d.v, d.leeway = -0.6, 0.2, math.radians(160.0)
    w.record("routine", "test.bump", "a new view")
    assert w.readings["leeway"] is None
    assert tools.readings_words(w)["leeway"] == R.STERNWAY_WORDS
    # with way on, the physics' own numbers again
    world = world_for(SHIPS[0])
    assert world.ship.dyn.u > units.knots_to_ms(R.READING_SPEED_FLOOR_KN)
    assert world.readings["leeway"] == world.ship.dyn.leeway
    assert tools.readings_words(world)["course"] == units.format_heading(world.readings["course"])


def test_the_log_writes_no_leeway_line_without_way_on(monkeypatch):
    """The log's leeway line keeps the same floor: a ship driven astern with a side force
    (the physics' leeway then near 180 degrees) writes no leeway line; driven ahead, it
    does."""
    from freesail.physics import integrate
    from freesail.physics.sails import SailForces
    from freesail.physics.wind import Wind, WindParams
    from freesail.ship.loader import load_ship

    wind = Wind(WindParams.from_nautical(225.0, 15.0), random.Random(0))  # never stepped

    def leeway_lines(ship, seconds, thrust, side):
        forces = SailForces(thrust, side, 0.0, 0.0, 0.0)
        monkeypatch.setattr(integrate, "compute_sail_forces", lambda s, w, *a: forces)
        notes = []
        for _ in range(seconds):
            integrate.step(ship, 1.0, wind)
            notes.extend(ship.drain_notes())
        return [n for n in notes if n[1] == "ship.leeway"]

    ship = load_ship(SHIPS[0])
    ship.dyn.u = -1.0
    astern = leeway_lines(ship, 120, -20_000.0, 30_000.0)
    assert ship.dyn.u < 0 and abs(ship.dyn.leeway) > math.radians(90)
    assert astern == []
    ship = load_ship(SHIPS[0])
    ship.dyn.u = 4.0
    assert leeway_lines(ship, 300, 30_000.0, 40_000.0)


def test_the_apparent_wind_is_read_before_the_clock_has_run():
    """Playtest 3: at 04:00, before the first tick, the apparent wind read 0 knots in a
    15-knot breeze. It is the sails model's own function over the ship as she lies, read
    without writing anything; the first tick gives the same."""
    w = make_world(7, SHIPS[0], Scenario(wind_from_deg=0.0, ship_heading_deg=180.0))
    assert w.clock.tick == 0 and w.ship.dyn.apparent_wind_speed == 0.0
    before = (w.readings["apparent_wind_angle"], w.readings["apparent_wind_speed"])
    assert units.ms_to_knots(before[1]) > 10
    assert R.describe_value(R.REGISTRY.get("apparent_wind_angle"), before[0]).endswith(
        "right astern"
    )
    assert w.ship.dyn.apparent_wind_speed == 0.0  # nothing written
    w.tick()
    assert w.readings["apparent_wind_speed"] == pytest.approx(before[1], rel=0.05)
    assert w.readings["apparent_wind_angle"] == w.ship.dyn.apparent_wind_angle


# -- the mean wind (package 29b; playtest 7, finding 4) --------------------------------------


def gusty_world(seed: int = 1) -> World:
    return World(seed=seed, scenario=Scenario(wind_speed_kn=20.0, gustiness=1.0, variability=0.3))


def test_the_mean_wind_is_the_last_ten_minutes_of_the_true_wind():
    """The mean true wind beside the instant's: the plain mean of the last ten minutes'
    speeds, and the direction of their mean vector; before the first tick, the instant's."""
    from freesail.physics.wind import MEAN_WIND_WINDOW_S

    w = gusty_world()
    r = w.readings
    assert r["mean_true_wind_speed"] == w.wind.effective_speed
    assert r["mean_true_wind_from"] == w.wind.direction_from
    speeds, dirs = [], []
    for _ in range(MEAN_WIND_WINDOW_S + 300):
        w.tick()
        speeds.append(w.wind.effective_speed)
        dirs.append(w.wind.direction_from)
    assert MEAN_WIND_WINDOW_S == 600
    last, last_dirs = speeds[-600:], dirs[-600:]
    assert w.readings["mean_true_wind_speed"] == pytest.approx(sum(last) / len(last))
    east = sum(s * math.sin(d) for s, d in zip(last, last_dirs, strict=True))
    north = sum(s * math.cos(d) for s, d in zip(last, last_dirs, strict=True))
    assert w.readings["mean_true_wind_from"] == pytest.approx(
        units.wrap_2pi(math.atan2(east, north))
    )
    # the gusts blew, and the mean is steadier than the instant
    assert max(last) > 1.1 * min(last)
    assert [e for e in w.log if e.kind == "wind.gust"]


def test_the_label_says_gust_above_the_mean_the_mean_or_a_lull_in_words():
    from freesail.agents import tools

    w = gusty_world()
    seen = set()
    for _ in range(3600):
        w.tick()
        label = w.readings["true_wind_against_mean"]
        seen.add(label)
        if w.wind.gust_factor >= 1.25 and w.wind_record.mean_speed() < w.wind.speed * 1.1:
            assert label == "a gust above the mean"
    assert {"a gust above the mean", "at the mean"} <= seen
    w.wind.speed = w.wind.base_speed = w.wind.speed * 0.6  # the wind drops away
    w.wind.gust_factor = 1.0
    w.wind.gust_remaining = 0.0
    w.tick()
    assert w.readings["true_wind_against_mean"] == "a lull"
    words = tools.readings_words(w)
    # in the samples and the readings tool, beside the instant's reading
    assert list(words)[:5] == [
        "true_wind_speed",
        "true_wind_from",
        "mean_true_wind_speed",
        "mean_true_wind_from",
        "true_wind_against_mean",
    ]
    assert words["true_wind_against_mean"] == "a lull"
    assert words["mean_true_wind_speed"].endswith(" knots")


def test_the_gust_line_names_the_mean_and_the_dialect_reads_the_mean_and_the_label():
    from freesail.standing.grammar import parse_condition

    w = gusty_world()
    w.run(1800)
    gusts = [e for e in w.log if e.kind == "wind.gust"]
    assert gusts and all(", the mean " in e.text for e in gusts)
    assert all("mean_kn" in e.data for e in gusts)
    c = parse_condition("the mean wind exceeds 30 knots and the true wind is not a gust")
    assert [(x.reading, x.comparison.op) for x in c.clauses] == [
        ("mean_true_wind_speed", "gt"),
        ("true_wind_against_mean", "is_not"),
    ]
    for said, value in (
        ("is a lull", "a lull"),
        ("is a gust", "a gust above the mean"),
        ("is at the mean", "at the mean"),
    ):
        clause = parse_condition(f"the true wind {said}").clauses[0]
        assert (clause.reading, clause.comparison.value) == ("true_wind_against_mean", value)
    # the true wind's speed is read as before
    clause = parse_condition("the true wind is under 20 knots").clauses[0]
    assert clause.reading == "true_wind_speed"


# ---------------------------------------------------------------------------
# Package 37d: `the nearest land`, a reading in the registry (so the prompt, the dialect
# and every station's sample have it), and the three events
# ---------------------------------------------------------------------------


def _coast_world(lat: float, lon: float, heading: float = 20.0, hour: int = 10, day: int = 19):
    from datetime import datetime

    sc = Scenario(
        start_time=datetime(1805, 6, day, hour, 0),
        wind_from_deg=225.0,
        wind_speed_kn=10.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=heading,
        position={"lat_deg": lat, "lon_deg": lon},
        region="channel-west",
    )
    return make_world(7, ROOT / "data/ships/frigate-36.yaml", sc)


def test_the_nearest_land_is_a_reading_in_the_lookouts_words_and_never_the_charts_metres():
    """Item 9: where it lies from the ship's head, its bearing to the point, its distance
    by estimation in the lookout's own words and the coast's name; the value behind the
    words is the distance as he said it, in whole cables, for the dialect."""
    from freesail import units
    from freesail.agents.tools import readings_words
    from freesail.world.lookout import SHORE_ID

    row = R.REGISTRY.get("nearest_land")
    assert row.kind == "distance" and row.words == ("the nearest land", "the nearest shore")
    w = _coast_world(50.300, -4.20)  # under a mile south of Rame Head
    shore = next(s for s in w.lookout.sightings if s.feature.id == SHORE_ID)
    value = w.readings["nearest_land"]
    said = w.readings.words("nearest_land")
    assert (
        said
        == value["words"]
        == (
            f"the land about Rame Head, {value['relative']}, bearing {value['bearing']}, "
            f"{value['estimate']}"
        )
    )
    assert value["relative"] == "on the larboard bow" and value["estimate"].endswith("cables")
    # as said, never as measured: whole cables, and no true figure in the value
    cables = value["metres"] / units.CABLE
    assert abs(cables - round(cables)) < 1e-9
    assert value["metres"] != shore.distance_m and set(value) == {
        "metres",
        "words",
        "name",
        "relative",
        "bearing",
        "estimate",
    }
    # at the prompt, by either name, and in every station's sample
    e = w.submit("the nearest land")
    assert e.kind == "query.reading" and e.text == f"The nearest land: {said}."
    assert w.submit("the nearest shore").text == f"The nearest shore: {said}."
    assert readings_words(w)["nearest_land"] == said
    # the dialect compares what he said, in miles
    given = w.submit(
        'standing order "close": when the nearest land is under a mile then heave the lead'
    )
    assert given.kind == "standing.given", given.text
    assert (
        w.submit(
            'standing order "far": when the nearest shore exceeds 2 miles then heave the log'
        ).kind
        == "standing.given"
    )
    w.run(2)
    fired = {
        e.actor for e in w.log if e.kind == "order.accepted" and e.actor.startswith("standing")
    }
    assert fired == {"standing order 'close'"}
    refused = w.submit('standing order "x": when the nearest land is in sight then heave the lead')
    assert refused.kind == "order.rejected" and "compared in miles" in refused.text


def test_the_nearest_land_says_none_within_a_league_and_not_to_be_seen():
    """Item 9: beyond a league, "no land within a league"; when the weather or the night
    bounds his sight short of that, none seen within how far he can see, and what lies
    beyond it not to be told (package 37l, G5: the words were "not to be seen: in this
    weather the shore shows within a cable at most", read by an officer as land within a
    cable); with no chart, the chart's own absent words."""
    from types import SimpleNamespace

    far = _coast_world(50.20, -4.20)  # seven miles south of Rame Head: the land in sight
    assert far.readings["land"]["in_sight"] and far.readings["nearest_land"] is None
    assert far.readings.words("nearest_land") == "no land within a league"
    night = _coast_world(50.285, -4.20, hour=1, day=26)  # a dark night, two miles off
    assert night.daylight == "night" and not night.lookout.moonlit
    assert night.readings["nearest_land"] is None
    assert night.readings.words("nearest_land") == (
        "none seen within a mile; by night the shore shows no further off than that, and "
        "land beyond it cannot be told"
    )
    fog = _coast_world(50.300, -4.20)
    assert fog.readings["nearest_land"] is not None
    fog.conditions = SimpleNamespace(visibility_nm=0.1, air_mass="neutral")
    fog.lookout.look(fog)
    fog._readings_key = None
    assert fog.readings.words("nearest_land") == (
        "none seen within a cable; in this weather the shore shows no further off than "
        "that, and land beyond it cannot be told"
    )
    plane = make_world(7, ROOT / "data/ships/frigate-36.yaml", Scenario())
    assert plane.readings["nearest_land"] is None
    assert plane.readings.words("nearest_land") == R.NO_CHART_WORDS


def test_the_three_events_of_package_37d_are_in_the_registry():
    spec = R.EVENTS
    assert R.event_matches(spec["a fix"], "reckoning.fix", {})
    assert R.event_matches(spec["land ahead"], "lookout.land_ahead", {"urgent": False})
    assert not R.event_matches(spec["land ahead"], "lookout.land_ahead", {"urgent": True})
    assert R.event_matches(spec["land close ahead"], "lookout.land_ahead", {"urgent": True})
    assert not R.event_matches(spec["land close ahead"], "lookout.land_ahead", {"urgent": False})
    w = _coast_world(50.300, -4.20)
    for name in ("a fix", "land ahead", "land close ahead"):
        given = w.submit(f'standing order "{name}": at {name} then heave the lead')
        assert given.kind == "standing.given", given.text


def test_the_reckonings_reading_carries_the_tide_allowed_and_the_doubt_as_it_stands_now():
    """Package 37e: `the reckoning` gives the position by account and the tide allowed in
    it, with whose it is; `the reckoning's uncertainty` gives the master's doubt as it
    stands at this moment, which grows between the workings of the account, with the
    ellipse the chart draws; and the turn of the master's own tide is an event."""
    w = _coast_world(50.300, -4.20)
    reading = w.readings["reckoning"]
    assert set(reading) >= {"words", "position", "tide"}
    tide = reading["tide"]
    assert tide["by"] == "book" and tide["words"] in reading["words"]
    assert reading["words"].startswith(reading["position"] + "; the tide allowed: ")
    assert w.readings.words("reckoning") == reading["words"]
    doubt = w.readings["reckoning_uncertainty"]
    assert doubt["words"].startswith("I would not trust the reckoning within ")
    assert set(doubt["ellipse"]) >= {"semi_major_nm", "semi_minor_nm", "major_bearing_deg"}
    before = doubt["ellipse"]["semi_major_nm"]
    w.run(1800)  # half an hour with no working of the account: the doubt has grown
    w._readings_key = None
    assert w.readings["reckoning_uncertainty"]["ellipse"]["semi_major_nm"] > before
    spec = R.EVENTS["the turn of the tide by the reckoning"]
    assert R.event_matches(spec, "reckoning.tide", {"turn": True})
    assert not R.event_matches(spec, "reckoning.tide", {"turn": False})
    given = w.submit(
        'standing order "the tide": at the turn of the tide by the reckoning then '
        "work up the reckoning"
    )
    assert given.kind == "standing.given", given.text


# ---------------------------------------------------------------------------
# Package 37j: `the port` and `the depth of water` by the captain's means
# ---------------------------------------------------------------------------


def _at_rest_on_the_chart(lat: float, lon: float):
    """A ship at rest in a calm on the chart, at a quiet hour; the world's tide made
    nothing, so that the two ships of the proof below feel the same water."""
    from datetime import datetime

    w = make_world(
        7,
        ROOT / "data/ships/brig.yaml",
        Scenario(
            start_time=datetime(1805, 6, 12, 13, 0),
            wind_from_deg=225.0,
            wind_speed_kn=0.0,
            gustiness=0.0,
            variability=0.0,
            ship_heading_deg=0.0,
            position={"lat_deg": lat, "lon_deg": lon},
            region="channel-west",
        ),
    )
    w.tide, w.tide_state = None, None
    w.ship.extra.pop("water", None)
    return w


# The lookout's own rows: what the eye sees of the land and the compass's bearing of a
# mark in sight, which are observations the man on deck makes, by estimate and by compass
# (spec M5 §12); they differ with where she truly is, as they should, and give no figure
# of her position but through the master's working of them (`take a bearing`, `take a fix`).
THE_EYES_ROWS = frozenset({"in_sight", "land", "nearest_land", "bearing_of", "sail", "strangers"})
# And the sky over her: the moon's altitude and azimuth in the data behind `the moon`
# (whose words are the same), which is the sky seen from where she is, as a sight is.
THE_SKYS_ROWS = frozenset({"moon"})


def test_no_reading_gives_the_true_position_by_any_road():
    """Item 7, the proof (the review's G4; as 37e's proved it of the master's tide): two
    ships of one seed whose true places are four miles apart and whose accounts are one
    say every reading alike, but the lookout's own. In open water they say all alike; in
    sight of the Manacles all but what the eye and the compass make of the land. Before
    package 37j `the depth of water` (the chart at the truth) and `the port` (the true
    bearing and distance of its road, to a tenth of a mile) differed in both."""
    from freesail.world.geo import Position

    params = {"mark": "the Lizard", "person": "the master"}
    for pa, pb, same, eyes in (
        ((49.0, -6.5), (49.05, -6.42), (49.02, -6.47), frozenset()),
        ((50.05, -5.0), (50.08, -4.95), (50.06, -4.98), THE_EYES_ROWS),
    ):
        a, b = _at_rest_on_the_chart(*pa), _at_rest_on_the_chart(*pb)
        for w in (a, b):
            w.navigation.reckoning.set_position(Position(*same), 0, sigma_nm=1.0)
        for w in (a, b):
            w.run(600)
        assert a.navigation.account_now() == b.navigation.account_now()
        differ = []
        for row in R.REGISTRY:
            if row.is_absent or row.parametric in ("sail", "part"):
                continue
            param = params.get(row.parametric) if row.parametric else None
            if a.readings.words(row.id, param) != b.readings.words(row.id, param):
                differ.append(row.id)
            if row.id not in eyes | THE_SKYS_ROWS and row.parametric is None:
                va, vb = a.readings[row.id], b.readings[row.id]
                assert repr(va) == repr(vb), row.id
        assert set(differ) <= eyes, differ
        assert a.readings["depth_of_water"] is not None and a.readings["port"] is not None


def test_the_depth_of_water_is_the_charts_at_the_account_and_the_port_is_by_account():
    """Item 7: `the depth of water` is the chart's depth at the position by account,
    said as the chart's and never as a cast, with what the chart shows within the
    account's doubt when that is a fathom or more; `the port` gives the bearing and
    distance of the port's road by account, with the account's doubt, as `shape a course
    for` does."""
    from freesail.world.chart import fathoms_words
    from freesail.world.geo import Position, bearing_and_distance, destination

    w = _at_rest_on_the_chart(50.05, -5.0)
    nav = w.navigation
    off = destination(w.position, 90.0, 3.0 * units.NAUTICAL_MILE)
    nav.reckoning.set_position(Position(off.lat_deg, off.lon_deg), 0, sigma_nm=0.5)
    here = nav.account_now()
    depth = w.readings["depth_of_water"]
    assert depth == pytest.approx(w.chart.depth_at(here))
    assert depth != pytest.approx(w.chart.depth_at(w.position))
    said = w.readings.words("depth_of_water")
    assert said.startswith(
        f"{fathoms_words(depth)} at low water by the chart, at the position by account"
    )
    assert "cast" not in said and "lead" not in said
    port = w.readings["port"]
    road = w.ports.ports["falmouth"].nearest_spot(here)
    assert port["by"] == "account"
    assert port["distance_nm"] == pytest.approx(road[1], abs=0.01)
    bearing = bearing_and_distance(here, road[0].position)[0]
    assert f"bearing {units.point_name(math.radians(bearing))} by account, " in port["words"]
    assert ", the account good to " in port["words"]
    # the snapshot to the browser carries no landmark's true distance, and a mark's
    # bearing only to the point the lookout said it by
    snap = queries.snapshot(w)
    for item in snap["lookout"]["items"]:
        assert "distance_m" not in item
        if item["seen_as"] != "sail":
            assert (item["bearing_deg"] / 11.25) == pytest.approx(
                round(item["bearing_deg"] / 11.25)
            )
    nearest = w.readings["land"]["nearest"]
    assert nearest is None or "distance_m" not in nearest
