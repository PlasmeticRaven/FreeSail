"""The readings registry (spec M4 §2): every reading on both ships against the physics'
own numbers, the absent ones' sentences, the per-tick cache, and parity with the snapshot.
"""

from __future__ import annotations

import math
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
    # the true wind is two readings behind one phrase: its speed and its direction
    assert [r.kind for r in R.REGISTRY.by_words("the true wind")] == ["speed", "direction"]


def test_absent_readings_carry_their_sentences():
    for id, word in (("well", "well"), ("glass", "glass"), ("depth", "lead line")):
        row = R.REGISTRY.get(id)
        assert row.is_absent and row.getter is None
        assert word in row.absent and "yet" in row.absent
    assert R.REGISTRY.get("glass").absent == (
        "The ship has no glass yet; that reading comes with the world."
    )
    w = World(seed=1)
    assert w.readings["glass"] is None
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
    # is aback; the schooner stalls at some thirty-four degrees apparent, her square
    # topsails shaking while her fore-and-aft canvas draws (the docstring of sails.py)
    world.submit("steer north")
    world.run(600)
    awa = units.rad_to_deg(abs(ship.dyn.apparent_wind_angle))
    for s in ship.sails.values():
        if not s.is_set:
            continue
        v = world.readings.value("sail", s.id)
        if ship.spec.rig == "topsail-schooner":
            assert 25 < awa < 45, awa
            assert v["shaking"] == (s.cls == "square"), (s.id, v, awa)
        else:
            assert awa < 25, awa
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
