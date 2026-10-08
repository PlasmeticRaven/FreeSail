"""The log's lines (package 37f, part three; the review of gate 5c's playtests, 5.8 and 8.2
under "The log"): what game 9's log said too often, said once.

No wind-shift line in airs too light or too unsteady to have a direction, with "light and
variable airs" once and the next settled wind once, and the event `a wind shift` under
the same floor; the aback lines by her state and not by the clock, and none for a sail
laid aback by order; a cast that finds no bottom routine, and `a sounding` bottom found;
a standing order with nothing to do saying so once a watch for each reason; and a
standing order's place checked when it is entered. ("A 'could not' that is no failure" is
with the runner's tests, `test_evolutions.py`.)
"""

from __future__ import annotations

from datetime import datetime, timedelta

import pytest

from freesail import units
from freesail.api import readings as R
from freesail.api.session import make_world
from freesail.core.events import Severity
from freesail.core.world import Scenario, World
from freesail.physics import hull as hp
from freesail.physics import integrate
from freesail.ship.parts import SailState
from freesail.standing.grammar import parse_condition
from freesail.standing.rules import Rule, Trigger

FRIGATE = "data/ships/frigate-36.yaml"
BRIG = "data/ships/brig.yaml"
T0 = datetime(1805, 6, 1, 4, 0)
CARRICK_ROAD = {"lat_deg": 50.160, "lon_deg": -5.034}
OFF_THE_LIZARD = {"lat_deg": 49.80, "lon_deg": -5.20}


def script(*points: tuple[float, float, float]) -> list[dict]:
    """Waypoints as (hours after 04:00, from degrees, knots), as the Scenario holds them."""
    return [
        {"at": (T0 + timedelta(hours=h)).isoformat(), "from_deg": d, "knots": k}
        for h, d, k in points
    ]


def point_world(weather: list[dict], seed: int = 7) -> World:
    """A point ship in the scripted wind, with no gusts and no wander."""
    sc = Scenario(start_time=T0, gustiness=0.0, variability=0.0)
    sc.weather = weather
    return World(seed=seed, scenario=sc)


def wind_lines(world):
    return [e.text for e in world.log if e.kind in ("wind.shift", "wind.variable")]


# ---------------------------------------------------------------------------
# Item 14: no wind-shift line in airs too light to have a direction
# ---------------------------------------------------------------------------


def test_the_floor_is_a_light_breeze_by_the_logs_own_scale():
    """Four knots: where Beaufort's scale, and the log's words for it, pass from "light
    airs" to "a light breeze"."""
    assert World.WIND_SHIFT_FLOOR_KN == 4.0
    assert units.describe_wind_strength(units.knots_to_ms(3.9)) == "light airs"
    assert units.describe_wind_strength(units.knots_to_ms(4.1)) == "a light breeze"


def test_a_calm_that_boxes_the_compass_logs_no_shift():
    """Game 9: 31 of its 50 wind-shift lines came with under four knots of wind, 18 of
    them at anchor in a calm ("Wind veered to S, calm."). A wind of two knots that goes
    round sixteen points in four hours says once that it is light and variable, and no
    shift."""
    w = point_world(script((0, 225, 2), (2, 315, 2), (4, 45, 2)))
    w.run(4 * 3600)
    assert wind_lines(w) == ["Light and variable airs."]
    (line,) = [e for e in w.log if e.kind == "wind.variable"]
    assert line.severity is Severity.NOTABLE and line.tick == pytest.approx(60, abs=2)
    assert not w.wind_settled


def test_the_wind_falling_light_is_said_once_and_the_next_settled_wind_once():
    """SW ten knots falls to two, wanders to NE in the calm, comes again at NE and then
    veers five points: one line as it falls light, none while it wanders, one when it
    has settled (which is where the next shift is measured from), and the veer after it
    as before."""
    w = point_world(
        script((0, 225, 10), (1, 225, 2), (2, 45, 2), (3, 45, 10), (4, 45, 10), (5, 45 + 56.25, 10))
    )
    w.run(5 * 3600 + 900)
    said = [(e.kind, e.text) for e in w.log if e.kind in ("wind.shift", "wind.variable")]
    assert said == [
        ("wind.variable", "Light and variable airs."),
        ("wind.shift", "The wind has settled at NE, a light breeze."),
        ("wind.shift", "Wind veered to ENE, a gentle breeze."),
        ("wind.shift", "Wind veered to E, a gentle breeze."),
    ]
    fell, settled = (e for e in w.log if e.kind == "wind.variable" or e.data.get("settled"))
    # the ten-minute mean passes four knots some minutes after the wind itself does
    assert 3000 < fell.tick < 3600 and 2 * 3600 < settled.tick < 3 * 3600
    assert settled.data["settled"] and w.wind_settled


def swinging(hours: int, knots: float = 9.0) -> list[dict]:
    """A breeze that swings between W and NW by N and back every forty minutes, as a
    slack gradient swings it."""
    points = [(0.0, 270.0, knots)]
    for k in range(1, hours * 3 + 1):
        points.append((k / 3.0, 270.0 + (56.25 if k % 2 else 0.0), knots))
    return script(*points)


def test_a_wind_that_swings_back_and_forth_is_unsteady_and_is_said_so_once():
    """The Speedwell among the Scilly Isles: 23 shifts in three hours and a half of a
    gentle breeze. A wind that veers, backs and veers again within the hour is unsteady:
    its second turn is said as that, once, and no shift after it until it has stood half
    an hour."""
    w = point_world(swinging(4) + script((4.5, 270.0, 9.0), (6.0, 270.0, 9.0)))
    w.run(4 * 3600)
    said = [(e.kind, e.text) for e in w.log if e.kind in ("wind.shift", "wind.variable")]
    kinds = [k for k, _ in said]
    assert kinds.count("wind.variable") == 1
    turn = kinds.index("wind.variable")
    # before it: the first swing out and the first back, each a shift or two, as before
    assert 2 <= turn <= 4 and all(t.startswith("Wind ") for _, t in said[:turn])
    assert {t.split()[1] for _, t in said[:turn]} == {"veered", "backed"}
    assert said[turn][1].startswith("The wind unsteady, backing and veering about ")
    assert said[turn][1].endswith(", a gentle breeze.")
    # after it, in three hours of the same swinging: not a line
    assert kinds[turn + 1 :] == [] and not w.wind_settled
    (line,) = [e for e in w.log if e.kind == "wind.variable"]
    assert line.severity is Severity.NOTABLE and line.tick < 2 * 3600
    # it stands at W: settled, said once, half an hour after it last moved two points
    w.run(2 * 3600)
    after = [e for e in w.log if e.kind in ("wind.shift", "wind.variable")][turn + 1 :]
    assert [e.text for e in after] == ["The wind has settled at W, a gentle breeze."]
    assert after[0].data["settled"] and w.wind_settled
    assert World.WIND_SWING_S == 3600 and World.WIND_STEADY_S == 1800


def test_a_wind_that_turns_once_is_no_unsteady_wind():
    """Backing before a front and veering at it, she has turned once: every shift is
    logged as it was, the sharp veer among them."""
    w = point_world(script((0, 225, 20), (1, 191.25, 20), (1.5, 191.25, 20), (1.6, 315, 30)))
    w.run(3 * 3600)
    assert [e.kind for e in w.log if e.kind == "wind.variable"] == []
    said = [e.text.split(",")[0] for e in w.log if e.kind == "wind.shift"]
    assert said[0].startswith("Wind backed to ") and said[-1].startswith("Wind veered to NW")
    assert all(s.startswith("Wind veered") for s in said[1:]) and len(said) >= 3
    assert w.wind_settled


def test_a_wind_flicking_about_a_steady_mean_logs_nothing():
    """The Harpy off Penlee (package 37c): a light breeze flung four points either way
    every minute. Its ten-minute mean holds still: no shift, and nothing unsteady in a
    mean that does not move."""
    flicks = [(0, 225, 6)] + [(m / 60, 225 + (45 if m % 2 else -45), 6) for m in range(1, 61)]
    w = point_world(script(*flicks))
    w.run(3600)
    assert wind_lines(w) == [] and w.wind_settled


def test_a_steady_breeze_shifts_as_it_did():
    w = point_world(script((0, 270, 15), (1, 270 + 5 * 11.25, 15)))
    w.run(3700)
    assert wind_lines(w) == [
        "Wind veered to WNW, a moderate breeze.",
        "Wind veered to NW, a moderate breeze.",
    ]
    assert w.wind_settled


def shift_firings(world):
    return [
        e.tick
        for e in world.log
        if e.kind == "order.accepted" and e.actor == "standing order 'shift'"
    ]


def at_a_wind_shift(world):
    """`standing order "shift": at a wind shift then steer 90`, entered as the Python
    API enters one (the point ship takes `steer` and has no book of its own to parse)."""
    rule = Rule(
        name="shift",
        trigger=Trigger("at", "at a wind shift", event="a wind shift"),
        actions=["steer 90"],
    )
    world.standing.book.add(rule)
    return rule


def test_the_event_a_wind_shift_keeps_the_same_floor():
    """A stand-by or a standing order `at a wind shift` waits for a wind that has a
    direction: nothing while a calm boxes the compass, and one shift when the wind that
    died at SW has settled at NE."""
    w = point_world(script((0, 225, 10), (1, 225, 2), (2, 45, 2), (3, 45, 10), (4, 45, 10)))
    at_a_wind_shift(w)
    w.run(2 * 3600)  # the calm, its mean gone round sixteen points
    assert not w.wind_settled and shift_firings(w) == []
    w.run(2 * 3600)
    (fired,) = shift_firings(w)
    (settled,) = [e for e in w.log if e.data.get("settled")]
    assert fired == pytest.approx(settled.tick, abs=2)
    # and in a breeze the event comes at each point, as it did
    steady = point_world(script((0, 270, 15), (1, 315, 15)))
    at_a_wind_shift(steady)
    steady.run(3700)
    assert len(shift_firings(steady)) >= 3


# ---------------------------------------------------------------------------
# Item 15: the aback lines, by state
# ---------------------------------------------------------------------------


def fixed(thrust: float = 0.0, side: float = 0.0):
    """Sail forces that are what the test says, whatever the sails."""
    from freesail.physics.sails import SailForces

    def compute(ship, wind, *_substep):
        return SailForces(thrust, side, 0.0, 0.0, 0.0)

    return compute


def aback_world(knots: float = 2.0):
    sc = Scenario(
        start_time=T0,
        wind_from_deg=0.0,
        wind_speed_kn=knots,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=0.0,
        ship_speed_kn=0.0,
    )
    w = make_world(7, FRIGATE, sc)
    w.ship.sails["main.topsail"].state = SailState.SET
    return w


def aback_lines(world, after=0):
    return [e for e in world.log.all()[after:] if e.kind == "ship.aback"]


def test_in_a_calm_her_sails_aback_is_said_once_however_long_it_lasts(monkeypatch):
    """Game 9: "Her sails aback; she had no way on to lose" ten times in three hours. The
    clock armed it again after a minute clear; her state arms it now, way on her again."""
    w = aback_world()
    for _ in range(12):  # three hours of a calm: aback ten minutes, clear five, by turns
        monkeypatch.setattr(integrate, "compute_sail_forces", fixed(thrust=-3_000.0))
        w.run(600)
        monkeypatch.setattr(integrate, "compute_sail_forces", fixed(thrust=0.0))
        w.ship.dyn.u = 0.0
        w.run(300)
    (line,) = aback_lines(w)
    assert line.severity is Severity.NOTABLE
    assert line.text == "Her sails aback; she had no way on to lose."
    assert hp.hull_state(w.ship).aback_lesser == "no_way"
    # she gathers way: the line is armed again by that, and said when she loses it
    n0 = len(w.log.all())
    monkeypatch.setattr(integrate, "compute_sail_forces", fixed(thrust=40_000.0))
    w.run(600)
    assert w.ship.dyn.u > units.knots_to_ms(hp.WAY_ON_KN)
    assert hp.hull_state(w.ship).aback_lesser == ""
    w.ship.dyn.u = 0.0  # and she has lost it again before her sails come aback
    monkeypatch.setattr(integrate, "compute_sail_forces", fixed(thrust=-3_000.0))
    w.run(120)
    (again,) = aback_lines(w, n0)
    assert again.severity is Severity.NOTABLE and "no way on to lose" in again.text


def test_the_urgent_line_has_its_own_flag_and_is_said_though_a_calms_line_stands(monkeypatch):
    """One flag for each severity: a calm's notable line standing does not keep back the
    urgent one when she is truly taken aback with way on in a breeze."""
    w = aback_world(knots=2.0)
    monkeypatch.setattr(integrate, "compute_sail_forces", fixed(thrust=-3_000.0))
    w.run(60)
    assert [e.severity for e in aback_lines(w)] == [Severity.NOTABLE]
    monkeypatch.setattr(integrate, "compute_sail_forces", fixed(thrust=0.0))
    w.run(int(hp.ABACK_REARM_SECONDS) + 5)
    state = hp.hull_state(w.ship)
    state.aback_lesser = "no_way"  # the calm's line stands, whatever she has done since
    n0 = len(w.log.all())
    w.wind.speed = w.wind.base_speed = units.knots_to_ms(14.0)
    w.ship.dyn.u = units.knots_to_ms(5.0)
    monkeypatch.setattr(integrate, "compute_sail_forces", fixed(thrust=-30_000.0))
    w.run(15)
    (urgent,) = aback_lines(w, n0)
    assert urgent.severity is Severity.URGENT and urgent.text.startswith("Taken aback")


def sail_lines(world, after=0):
    return [
        (e.kind, e.text)
        for e in world.log.all()[after:]
        if e.kind in ("sail.backed", "sail.filled")
    ]


def by_the_wind(knots=10.0, heading=60.0, ship=FRIGATE):
    sc = Scenario(
        start_time=T0,
        wind_from_deg=0.0,
        wind_speed_kn=knots,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=heading,
        ship_speed_kn=4.0,
    )
    w = make_world(7, ship, sc)
    w.submit("set topsails")
    w.submit("brace sharp up on the larboard tack")
    w.run(600)
    return w


def test_a_sail_taken_aback_is_said_once_an_episode():
    """Brought head to wind by her helm the topsails are taken aback, and say so, each
    once; flung off and on again without way they say no more; and with way on her and
    a minute full, they are armed again."""
    w = by_the_wind()
    n0 = len(w.log.all())
    for sail in ("fore.topsail", "main.topsail", "mizzen.topsail"):
        assert not w.ship.sails[sail].backed
    w.ship.dyn.heading = 0.0  # her head thrown into the wind, no order given the yards
    w.run(30)
    backed = [t for k, t in sail_lines(w, n0) if k == "sail.backed"]
    assert sorted(backed) == [
        "Fore topsail taken aback.",
        "Main topsail taken aback.",
        "Mizzen topsail taken aback.",
    ]
    # off and on four times with no way on her: "filled again" once each, and no more
    for _ in range(4):
        w.ship.dyn.u = 0.0
        w.ship.dyn.heading = units.deg_to_rad(60.0)
        w.run(30)
        w.ship.dyn.u = 0.0
        w.ship.dyn.heading = 0.0
        w.run(30)
    kinds = [k for k, _ in sail_lines(w, n0)]
    assert kinds.count("sail.backed") == 3 and kinds.count("sail.filled") == 3
    # full for a minute with way on: a new episode
    w.ship.dyn.heading = units.deg_to_rad(60.0)
    w.ship.dyn.u = units.knots_to_ms(4.0)
    w.run(200)
    assert w.ship.dyn.u > units.knots_to_ms(1.0)
    n1 = len(w.log.all())
    w.ship.dyn.heading = 0.0
    w.run(30)
    assert [k for k, _ in sail_lines(w, n1)].count("sail.backed") == 3


def test_a_sail_laid_aback_by_order_says_nothing():
    """`back the main topsail`, heaving to and filling away lay yards aback and fill them
    again as their own work: the orders' lines say so, and the sails' do not."""
    w = by_the_wind()
    n0 = len(w.log.all())
    assert w.submit("back the main topsail").kind == "order.accepted"
    w.run(240)
    assert w.ship.sails["main.topsail"].backed
    assert sail_lines(w, n0) == []
    assert any(e.kind == "yard.laid_aback" for e in w.log.all()[n0:])
    # hove to and filled away again: an hour of it, and not one sail's line
    w = by_the_wind(heading=67.0)
    n0 = len(w.log.all())
    assert w.submit("heave to").kind == "order.accepted"
    w.run(1800)
    assert "hove_to" in w.ship.extra and w.ship.sails["main.topsail"].backed
    assert w.submit("fill away").kind == "order.accepted"
    w.run(900)
    assert "hove_to" not in w.ship.extra and not w.ship.sails["main.topsail"].backed
    assert sail_lines(w, n0) == []


# ---------------------------------------------------------------------------
# Item 17: the cast that finds no bottom; the held lines
# ---------------------------------------------------------------------------


def chart_world(where, ship=FRIGATE, hour=10, **kw):
    sc = Scenario(
        start_time=datetime(1805, 6, 10, hour, 0),
        wind_from_deg=225.0,
        wind_speed_kn=kw.pop("knots", 10.0),
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=kw.pop("heading", 20.0),
        ship_speed_kn=kw.pop("speed", 0.0),
        position=where,
        region="channel-west",
        **kw,
    )
    return make_world(7, ship, sc)


def test_a_cast_that_finds_no_bottom_is_routine_and_a_sounding_is_bottom_found():
    off = chart_world(OFF_THE_LIZARD)  # forty fathoms and more: the hand lead finds none
    off.run(5)
    cast = off.submit("heave the lead")
    assert cast.kind != "order.rejected", cast.text
    off.run(120)
    (none,) = [e for e in off.log if e.kind == "sounding"]
    assert none.text == "No bottom at twenty fathoms." and none.severity is Severity.ROUTINE
    spec = R.EVENTS["a sounding"]
    assert not R.event_matches(spec, none.kind, none.data)
    road = chart_world(CARRICK_ROAD)
    road.run(5)
    road.submit("heave the lead")
    road.run(120)
    (found,) = [e for e in road.log if e.kind == "sounding"]
    assert found.severity is Severity.NOTABLE and found.data["depth_m"] is not None
    assert R.event_matches(spec, found.kind, found.data)


def test_at_a_sounding_waits_for_the_bottom():
    w = chart_world(OFF_THE_LIZARD)
    w.submit('standing order "bottom": at a sounding then steer 90')
    w.run(5)
    for _ in range(3):
        w.submit("heave the lead")
        w.run(120)
    assert len([e for e in w.log if e.kind == "sounding"]) == 3
    assert not [e for e in w.log if e.actor == "standing order 'bottom'" and e.tick > 0]


def held_lines(world, name):
    actor = f"standing order '{name}'"
    return [
        e for e in world.log if e.actor == actor and e.kind in ("standing.held", "order.rejected")
    ]


def test_a_standing_order_with_nothing_to_do_says_so_once_a_watch_for_each_reason():
    """The gate's merchant passage, at anchor in the Bay of Brest: "in the Bay: order not
    carried out ('come to an anchor'): she is at anchor already" twenty-six times and
    "tend the sheets ... She is at anchor" twenty-one, one a glass. Once, and then once a
    watch; routine always."""
    w = chart_world(CARRICK_ROAD)
    w.run(60)
    assert w.submit("let go the best bower").kind == "order.accepted"
    w.run(600)
    assert w.at_anchor
    w.submit('standing order "anchor": every glass then come to an anchor')
    w.submit('standing order "tend": every 10 minutes then trim the sheets')
    w.submit(
        'standing order "far": every 10 minutes, if the true wind exceeds 40 knots then steer 90'
    )
    assert sorted(w.standing.book.names) == ["anchor", "far", "tend"]
    start = w.clock.ship_time
    w.run(3 * 3600 + 1800)  # 10:11 to 13:41: the forenoon watch's end and the afternoon's
    assert start.hour == 10 and w.clock.ship_time.hour == 13
    for name, firings in (("anchor", 7), ("tend", 21), ("far", 21)):
        said = held_lines(w, name)
        assert len(said) == 2, (name, [e.text for e in said])  # one in each watch
        assert all(e.severity is Severity.ROUTINE for e in said)
        assert said[0].ship_time.hour < 12 <= said[1].ship_time.hour
        assert w.standing.book.get(name).fired <= firings
    assert "she is at anchor already" in held_lines(w, "anchor")[0].text
    assert "must wait till she weighs" in held_lines(w, "tend")[0].text
    assert "not carried out; the true wind is" in held_lines(w, "far")[0].text


@pytest.fixture
def synthetic():
    """`synthetic(id, fn)` makes reading `id` return `fn(world)`; restored at teardown."""
    originals: dict[str, R.Reading] = {}

    def set_reading(id: str, fn) -> None:
        row = R.REGISTRY.get(id)
        originals.setdefault(id, row)
        R.REGISTRY.add(
            R.Reading(id, row.words, row.kind, row.unit, lambda w, p: fn(w), row.parametric)
        )

    yield set_reading
    for row in originals.values():
        R.REGISTRY.add(row)


def test_the_same_reason_with_another_figure_is_one_and_a_reason_come_again_is_said(synthetic):
    """Each reason has its line; figures aside, the same reason is one. And when what
    held it holds it no longer, the next time is said again within the watch."""
    kn = {"v": 10.0}
    synthetic("true_wind_speed", lambda w: units.knots_to_ms(kn["v"]))
    w = World(seed=3, scenario=Scenario(start_time=datetime(1805, 6, 1, 8, 5)))
    w.standing.book.add(
        Rule(
            name="blow",
            trigger=Trigger("every", "every minute", interval_s=60),
            actions=["steer 90"],
            condition=parse_condition("the true wind exceeds 30 knots"),
        )
    )
    w.run(600)
    assert len(held_lines(w, "blow")) == 1
    kn["v"] = 12.0  # another figure, the same reason
    w.run(600)
    assert len(held_lines(w, "blow")) == 1
    kn["v"] = 35.0  # it fires
    w.run(120)
    assert w.standing.book.get("blow").fired >= 1
    kn["v"] = 10.0  # and is held again, in the same watch: said again
    w.run(120)
    assert len(held_lines(w, "blow")) == 2


# ---------------------------------------------------------------------------
# Item 18: a standing order's condition is checked when it is entered
# ---------------------------------------------------------------------------


def test_the_distance_to_the_land_is_refused_at_entry_with_the_forms_that_serve():
    """The owner needed four tries at 'Triangulate': "the distance to the land" was taken
    into the book and then held at every firing as "not on the chart"."""
    w = chart_world(OFF_THE_LIZARD)
    w.run(2)
    e = w.submit(
        'standing order "triangulate": every glass, if the distance to the land is under '
        "12 miles then take a fix"
    )
    assert e.kind == "order.rejected"
    why = e.data["reason"]
    assert why.startswith("'the land' is not a place on the chart")
    assert "'the distance to the Lizard'" in why and "48 20 N 4 36 W" in why
    assert "'the nearest land'" in why and "'the land is in sight'" in why
    assert w.standing.book.get("triangulate") is None
    # the forms it names are taken
    for cond in (
        "the nearest land is under 2 miles",
        "the land is in sight",
        "the distance to the Lizard is under 12 miles",
        "the distance to 48 20 N 4 36 W is under 12 miles",
    ):
        name = f"t{abs(hash(cond)) % 1000}"
        e = w.submit(f'standing order "{name}": every glass, if {cond} then take a fix')
        assert e.kind == "standing.given", (cond, e.text)


def test_a_name_the_chart_nearly_has_is_answered_with_that_name():
    w = chart_world(OFF_THE_LIZARD)
    w.run(2)
    e = w.submit(
        'standing order "near": when the distance to the Lizzard is under 4 miles then wear ship'
    )
    assert e.kind == "order.rejected"
    assert "'the lizzard' is not a place on the chart" in e.data["reason"].lower()
    assert "Did you mean" in e.data["reason"] and "Lizard" in e.data["reason"]
    e = w.submit(
        'standing order "trigger": when the distance to the moon is under 4 miles then wear ship'
    )
    assert e.kind == "order.rejected" and "is not a place on the chart" in e.data["reason"]


def test_the_shipped_books_enter_whole():
    """Every book the game ships names places the chart has."""
    from pathlib import Path

    from freesail.standing.book import read_orders_file

    w = chart_world(OFF_THE_LIZARD)
    w.run(2)
    books = sorted(Path("data").rglob("*.orders"))
    assert books
    for path in books:
        for line in read_orders_file(path):
            e = w.submit(line)
            assert "is not a place on the chart" not in e.text, (path.name, line, e.text)
            if e.kind == "standing.given":
                w.submit(f'strike standing order "{e.data["name"]}"')
