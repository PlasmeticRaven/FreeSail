"""Package 29: the weather script (spec M4 §19) and the scenario files that carry it.

The script sets the base wind; the gusts and the wander ride on it as on a fixed one; it
is scenario data, saved with the game and followed again by a replay; a wind that turns
is a wind that backs or veers, and the log and the readings see it.
"""

from __future__ import annotations

import math
from datetime import datetime, timedelta

import pytest

from freesail import units
from freesail.api.session import make_world, ship_factory
from freesail.core import replay
from freesail.core.world import Scenario, World
from freesail.world.scenarios import ScenarioError, begin, load_scenario, make_scenario_world
from freesail.world.weather_script import ScriptError, Waypoint, WeatherScript

FRIGATE = "data/ships/frigate-36.yaml"
GATE_DAY = "data/scenarios/gate-4c-day.yaml"
T0 = datetime(1805, 6, 1, 4, 0)


def script(*points: tuple[float, float, float]) -> list[dict]:
    """Waypoints as (hours after 04:00, from degrees, knots), as the Scenario holds them."""
    return [
        {"at": (T0 + timedelta(hours=h)).isoformat(), "from_deg": d, "knots": k}
        for h, d, k in points
    ]


def calm_world(weather: list[dict], seed: int = 7, **kw) -> World:
    """A point ship in the scripted wind, with no gusts and no wander unless asked."""
    sc = Scenario(start_time=T0, gustiness=kw.get("gust", 0.0), variability=kw.get("var", 0.0))
    sc.weather = weather
    return World(seed=seed, scenario=sc)


# -- the script ---------------------------------------------------------------------------


def test_the_wind_turns_and_freshens_linearly_between_waypoints():
    ws = WeatherScript.from_list(script((0, 270, 18), (4, 315, 38)))
    d, s = ws.at(T0)
    assert units.rad_to_deg(d) == pytest.approx(270.0)
    assert units.ms_to_knots(s) == pytest.approx(18.0)
    d, s = ws.at(T0 + timedelta(hours=1))  # a quarter of the way
    assert units.rad_to_deg(d) == pytest.approx(281.25)
    assert units.ms_to_knots(s) == pytest.approx(23.0)
    d, s = ws.at(T0 + timedelta(hours=4))
    assert units.rad_to_deg(d) == pytest.approx(315.0)
    assert units.ms_to_knots(s) == pytest.approx(38.0)


def test_before_the_first_and_after_the_last_the_script_holds():
    ws = WeatherScript.from_list(script((1, 270, 18), (2, 315, 30)))
    assert ws.at(T0) == ws.at(T0 + timedelta(hours=1))
    assert ws.at(T0 + timedelta(days=3)) == ws.at(T0 + timedelta(hours=2))


def test_the_wind_turns_the_short_way_round():
    """North-west to north-east is eight points through north, not twenty-four."""
    ws = WeatherScript.from_list(script((0, 315, 20), (2, 45, 20)))
    d, _ = ws.at(T0 + timedelta(hours=1))
    assert units.rad_to_deg(d) == pytest.approx(0.0, abs=1e-9) or units.rad_to_deg(
        d
    ) == pytest.approx(360.0)
    backing = WeatherScript.from_list(script((0, 45, 20), (2, 315, 20)))
    d, _ = backing.at(T0 + timedelta(hours=1))
    assert units.rad_to_deg(units.wrap_pi(d)) == pytest.approx(0.0, abs=1e-9)


def test_the_script_says_itself_in_words():
    ws = WeatherScript.from_list(script((0, 270, 18), (16, 315, 45), (26, 315, 18)))
    lines = ws.lines()
    assert lines[0] == (
        "From W, 18 knots (a fresh breeze) at 04:00 on 1 June, veering 4 points and freshening;"
    )
    assert lines[1] == "From NW, 45 knots (a strong gale) at 20:00 on 1 June, easing;"
    assert lines[-1] == "to NW, 18 knots (a fresh breeze) at 06:00 on 2 June."


@pytest.mark.parametrize(
    "entries,words",
    [
        ([], "at least one waypoint"),
        (script((1, 270, 18), (1, 280, 18)), "not after"),
        (script((2, 270, 18), (1, 280, 18)), "not after"),
        ([{"at": "1805-06-01T04:00", "from_deg": 270, "knots": -3}], "-3.0 knots"),
        ([{"at": "1805-06-01T04:00", "from_deg": 270}], "'from_deg' and 'knots'"),
        ([{"from_deg": 270, "knots": 3}], "needs a time"),
    ],
)
def test_a_script_that_cannot_be_followed_is_refused_in_words(entries, words):
    with pytest.raises(ScriptError, match=words):
        WeatherScript.from_list(entries)


def test_a_waypoint_round_trips_through_its_dictionary():
    p = Waypoint(at=T0, from_deg=292.5, knots=28.0)
    assert Waypoint.from_dict(p.to_dict()) == p


# -- the World follows it ------------------------------------------------------------------


def test_the_world_follows_the_script_exactly_with_no_gusts_and_no_wander():
    """With gustiness and variability at nothing the true wind is the script's, tick for
    tick: the base wind moves and the wind with it."""
    w = calm_world(script((0, 270, 18), (1, 315, 30)))
    assert units.rad_to_deg(w.wind.direction_from) == pytest.approx(270.0)
    for _ in range(4):
        w.run(900)
        d, s = w.weather.at(w.clock.ship_time)
        assert w.wind.direction_from == pytest.approx(d, abs=1e-9)
        assert w.wind.effective_speed == pytest.approx(s, rel=1e-9)
    assert units.rad_to_deg(w.wind.direction_from) == pytest.approx(315.0)
    assert units.ms_to_knots(w.wind.base_speed) == pytest.approx(30.0)


def test_the_gusts_and_the_wander_ride_on_the_scripted_base():
    """The script draws nothing from the wind's stream, so a scripted wind wanders about its
    moving base by the same steps an unscripted one wanders about a fixed base: the offset
    of direction from the base is the same, draw for draw, and the gusts come on the same
    ticks."""
    scripted = calm_world(script((0, 270, 18), (2, 315, 18)), gust=1.0, var=1.0)
    fixed = calm_world(script((0, 270, 18)), gust=1.0, var=1.0)
    gusts_s, gusts_f = [], []
    for _ in range(7200):
        scripted.tick()
        fixed.tick()
        gusts_s.append(scripted.wind.gust_started)
        gusts_f.append(fixed.wind.gust_started)
    assert gusts_s == gusts_f and any(gusts_s)
    off_s = units.wrap_pi(scripted.wind.direction_from - scripted.wind.base_direction)
    off_f = units.wrap_pi(fixed.wind.direction_from - fixed.wind.base_direction)
    assert off_s == pytest.approx(off_f, abs=1e-9)
    assert off_s != 0.0, "the wander is there"
    assert scripted.wind.speed == pytest.approx(fixed.wind.speed, rel=1e-9)


# Five points in the hour, so that the two-point marks fall between ticks (a turn of
# exactly four points reaches its second mark on the last tick, where the arithmetic of
# the interpolation may leave it a hair short of two points since the first).
FIVE_POINTS = 5 * 11.25


def test_a_veering_script_is_logged_as_a_veer_and_a_standing_order_sees_it():
    """West to north-west by north over an hour is five points: the log says the wind
    veered each time it has turned two points since it last said so
    (World.WIND_SHIFT_LOG_THRESHOLD), at 24 and 48 minutes, and a standing order that waits
    for the true wind to veer two points fires with the first."""
    sc = Scenario(start_time=T0, gustiness=0.0, variability=0.0, ship_heading_deg=135.0)
    sc.weather = script((0, 270, 15), (1, 270 + FIVE_POINTS, 15))
    w = make_world(7, FRIGATE, sc)
    w.submit('standing order "veer": when the true wind veers 2 points then tend the sheets')
    w.run(3700)
    shifts = [e for e in w.log if e.kind == "wind.shift"]
    assert [e.text for e in shifts] == [
        "Wind veered to WNW, a moderate breeze.",
        "Wind veered to NW, a moderate breeze.",
    ]
    assert [e.tick for e in shifts] == [pytest.approx(1440, abs=1), pytest.approx(2880, abs=1)]
    fired = [e for e in w.log if e.actor == "standing order 'veer'" and e.tick > 0]
    assert fired and fired[0].tick == pytest.approx(1440, abs=1)


def test_a_backing_script_is_logged_as_a_backing():
    w = calm_world(script((0, 315, 20), (1, 315 - FIVE_POINTS, 20)))
    w.run(3600)
    assert [e.text.split(",")[0] for e in w.log if e.kind == "wind.shift"] == [
        "Wind backed to WNW",
        "Wind backed to W",
    ]


def test_without_a_script_nothing_changes():
    w = World(seed=7, scenario=Scenario())
    assert w.weather is None and w.scenario.weather == []
    assert w.wind.base_direction == w.wind.direction_from


# -- scenario data: saved with the game, followed by a replay -----------------------------


def test_the_script_is_saved_with_the_scenario_and_a_replay_follows_it(tmp_path):
    w = calm_world(script((0, 270, 18), (1, 315, 30)), gust=0.5, var=0.5)
    w.run(2400)
    path = replay.save_to_file(w, tmp_path / "scripted.json")
    data = replay.load_file(path)
    assert data["scenario"]["weather"] == w.scenario.weather
    copy = replay.replay(data)
    assert copy.log.digest() == w.log.digest()
    assert copy.wind.state() == w.wind.state()


def test_a_save_from_before_the_script_loads_with_none():
    data = World(seed=7).save()
    del data["scenario"]["weather"]
    copy = replay.replay(data)
    assert copy.weather is None


# -- scenario files -------------------------------------------------------------------------


def test_the_gate_day_scenario_file():
    """data/scenarios/gate-4c-day.yaml: the day of spec §19 as data."""
    sf = load_scenario(GATE_DAY)
    sc = sf.scenario
    assert sf.seed == 7 and sf.ship_file == FRIGATE
    assert sc.start_time == datetime(1805, 6, 1, 4, 0)
    assert sc.latitude_deg == 50.0 and sc.ship_heading_deg == 135.0
    assert sf.standing_orders == [
        "data/standing_orders/starter.orders",
        "data/scenarios/gate-4c-day.orders",
    ]
    assert sf.orders == ["set plain sail", "set the royals"]
    ws = sf.script
    assert ws is not None
    first, peak = ws.waypoints[0], max(ws.waypoints, key=lambda p: p.knots)
    # a fresh breeze from the west at dawn (Beaufort's 17 to 21 knots) ...
    assert (first.from_deg, units.describe_wind_strength(units.knots_to_ms(first.knots))) == (
        270.0,
        "a fresh breeze",
    )
    # ... veering north-west and rising to a gale in the middle watch ...
    assert peak.from_deg == 315.0 and peak.knots > 40.0
    assert units.watch_of(peak.at)[1] == "Middle watch"
    # ... easing at the next dawn
    last = ws.waypoints[-1]
    assert last.at.date() > first.at.date() and last.knots < 22.0
    assert sc.wind_from_deg == 270.0 and sc.wind_speed_kn == first.knots


def test_the_gate_day_world_begins_with_its_book_and_its_first_orders():
    sf = load_scenario(GATE_DAY)
    w = make_scenario_world(sf)
    assert w.seed == 7 and w.ship.save_ref() == {"type": "file", "path": FRIGATE}
    n = begin(w, sf)
    names = [r["name"] for r in w.standing.book.save()]
    assert names == [
        "night routine",
        "morning sail",
        "shorten sail for weather",
        "keep her full",
        "heavy weather",
        "storm staysail",
        "topgallants",
        "gale canvas",
        "make sail after the gale",
        "topgallants again",
    ]
    assert n == 13  # seven lines of the starter file, four of the day's, two orders
    refused = [e.text for e in w.log if e.kind == "order.rejected"]
    assert len(refused) == 1 and "sound the well" in refused[0]
    assert [t for _, _, t in w.journal][-2:] == ["set plain sail", "set the royals"]


def test_a_seed_on_the_command_line_wins_over_the_file():
    sf = load_scenario(GATE_DAY)
    assert make_scenario_world(sf, seed=11).seed == 11


@pytest.mark.parametrize(
    "text,words",
    [
        ("start: yesterday\n", "is not a time"),
        ("weather:\n  - {at: 1805-06-01T04:00, from_deg: 270}\n", "'from_deg' and 'knots'"),
        (
            "weather:\n  - {at: 1805-06-01T05:00, from_deg: 270, knots: 5}\n"
            "  - {at: 1805-06-01T04:00, from_deg: 270, knots: 5}\n",
            "not after",
        ),
        ("- a list\n", "a mapping of fields"),
    ],
)
def test_a_scenario_file_that_cannot_be_read_says_why(tmp_path, text, words):
    p = tmp_path / "bad.yaml"
    p.write_text(text, encoding="utf-8")
    with pytest.raises(ScenarioError, match=words):
        load_scenario(p)


def test_a_scenario_world_replays_from_its_save(tmp_path):
    """The scenario file's world, its book and first orders given, a short way into the
    day, saved and replayed to the same digest: the script rides in the scenario, the
    orders in the journal."""
    sf = load_scenario(GATE_DAY)
    w = make_scenario_world(sf)
    begin(w, sf)
    w.run(900)
    data = replay.load_file(replay.save_to_file(w, tmp_path / "day.json"))
    assert len(data["scenario"]["weather"]) == len(sf.scenario.weather)
    copy = replay.replay(data, ship_factory)
    assert copy.log.digest() == w.log.digest()
    assert math.isclose(copy.wind.direction_from, w.wind.direction_from)
