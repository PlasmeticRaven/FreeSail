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
    for id, word in (("well", "well"), ("depth", "lead line")):
        row = R.REGISTRY.get(id)
        assert row.is_absent and row.getter is None
        assert word in row.absent and "yet" in row.absent
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
    ):
        assert words in R.EVENTS, words
    assert R.EVENTS["a sighting"].absent and R.EVENTS["a sounding"].absent
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
    w.submit("steer east")
    c = w.readings
    assert c is not b, "an order writes a log line and may change the ship at once"
    assert c["course"] == pytest.approx(math.pi / 2), "the course ordered, read at once"
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
