"""Lying to (package 37f, part one; the review of gate 5c's playtests, 5.7, 5.8 and 10.3
under the owner's note 6: "the helm and sails need to try to keep her hove to properly on
the tack she hove to on").

Heaving to that holds its tack: her way taken off before "Hove to" is said, and the watch
tending the helm and the sheets while the record stands; the record following what she
does when she is forced round all the same; `fill away` on the tack she is on, and `fill
away and steer <course>`; the record cleared by the anchor, the weighing, a tack, a wear
and the ground; `trim sails` declining while she is hove to, and the shipped books' trim
rules asleep through it.

The playtest's four failures are sailed here from like states built in a scripted world
(the brig under plain sail at seven knots with the wind abaft the beam; at four with it
on the beam; at a knot and a half in a wind of four or five knots under the sail she
carried, on either tack), since the game's own saves are the owner's and are not test
fixtures.
"""

from __future__ import annotations

import math
from datetime import datetime, timedelta

import pytest

from freesail import orders, units
from freesail.api.session import make_world
from freesail.core.world import Scenario
from freesail.evolutions import scripts
from freesail.orders import verbs
from freesail.orders.errors import OrderError
from freesail.ship.parts import HelmMode, SailState

FRIGATE = "data/ships/frigate-36.yaml"
SCHOONER = "data/ships/topsail-schooner.yaml"
CUTTER = "data/ships/cutter.yaml"
BRIG = "data/ships/brig.yaml"
POINT_DEG = 11.25
START = datetime(1805, 6, 1, 4, 0, 0)
# the sail the brig carried in the light airs of 15 June, beyond her plain sail
GAME_SAIL = (
    "set the royals",
    "set the flying jib",
    "set the main staysail",
    "set the main topmast staysail",
)


def world_for(ship, heading, knots, gust=0.0, wander=0.0, extra=(), seed=7, weather=None):
    """A vessel under plain sail, steady on `heading` with the wind from north (so 270 is
    the wind on the starboard beam, 240 abaft it), her yards and sheets trimmed."""
    scenario = Scenario(
        start_time=START,
        wind_from_deg=0.0,
        wind_speed_kn=knots,
        gustiness=gust,
        variability=wander,
        ship_heading_deg=heading,
        ship_speed_kn=3.0,
        weather=weather or [],
    )
    world = make_world(seed, ship, scenario)
    world.submit("set plain sail")
    world.submit(f"steer {heading:.0f}")
    for i in range(1200):
        if i % 120 == 0:
            world.submit("trim sails")
        world.tick()
    for order in extra:
        world.submit(order)
        world.run(200)
    return world


def wind_on_bow(world) -> float:
    """Degrees: + on the starboard bow, - on the larboard, 0 head to wind."""
    return math.degrees(units.wrap_pi(world.wind.direction_from - world.ship.dyn.heading))


def way_kn(world) -> float:
    return units.ms_to_knots(world.ship.dyn.u)


def events(world, *kinds, after=0):
    return [e for e in world.log if e.kind in kinds and e.tick > after]


def bring_to(world, minutes=15):
    """Give `heave to` and sail on: (the tack's sign, her head from the wind on that tack
    at each second, in degrees, her way at ten minutes)."""
    sign = 1.0 if wind_on_bow(world) > 0 else -1.0
    e = world.submit("heave to")
    assert e.kind == "order.accepted", e.text
    off, at_ten = [], None
    for t in range(1, minutes * 60 + 1):
        world.tick()
        off.append(sign * wind_on_bow(world))
        if t == 600:
            at_ten = way_kn(world)
    return sign, off, at_ten


# ---------------------------------------------------------------------------
# Item 1: heaving to that holds its tack
# ---------------------------------------------------------------------------

# (heading with the wind from north, wind in knots, gusts and wander, sail beyond plain
# sail, the way she must have on before the order)
THE_GAMES_FOUR = {
    "seven knots, the wind abaft the beam": (240.0, 15.0, 0.0, (), 6.5),
    "four knots, the wind on the beam": (270.0, 8.0, 0.0, (), 4.0),
    # package 37p: 0.98 knots on the larboard tack under the period's trim, the upper
    # yards braced in from the lower (before, at their limits, 1.0 and more)
    "a knot and a half in light airs, larboard tack": (50.0, 4.5, 0.3, GAME_SAIL, 0.95),
    "a knot and a half in light airs, starboard tack": (310.0, 4.5, 0.3, GAME_SAIL, 0.95),
}


@pytest.mark.parametrize("case", list(THE_GAMES_FOUR))
def test_the_brig_brought_to_from_each_of_the_games_states_holds_her_tack(case):
    """In game 9 the brig came up through the wind in four heave-tos of seven: inside a
    minute from seven knots, in two minutes from four, in six and in twenty minutes from
    a knot and a half. From each like state her head never comes within a point of the
    wind's eye, and after ten minutes she lies between four and seven points from it on
    the tack she hove to on, with under a knot and a half of way."""
    heading, knots, air, extra, way_before = THE_GAMES_FOUR[case]
    world = world_for(BRIG, heading, knots, gust=air, wander=air, extra=extra)
    assert way_kn(world) >= way_before, way_kn(world)
    start = world.clock.tick
    sign, off, at_ten = bring_to(world)
    assert min(off) > POINT_DEG, f"her head came within {min(off):.0f} degrees of the wind"
    assert all(4 * POINT_DEG <= o <= 7 * POINT_DEG for o in off[600:]), (
        min(off[600:]),
        max(off[600:]),
    )
    assert abs(at_ten) < 1.5, at_ten
    assert max(abs(way_kn(world)), abs(at_ten)) < 1.5
    said = events(world, "ship.hove_to", after=start)
    tack = "starboard" if sign > 0 else "larboard"
    assert len(said) == 1 and said[0].text.startswith(f"Hove to on the {tack} tack, main topsail")
    # she was not said to be hove to while she still carried her way
    assert said[0].data["speed_kn"] <= 1.5 and 4.0 <= said[0].data["off_points"] <= 7.0
    assert world.ship.extra["hove_to"]["sign"] == sign
    assert not events(world, "ship.forced_round", "ship.filled", "ship.aback", after=start)


@pytest.mark.parametrize("ship,most_kn", [(SCHOONER, 2.0), (CUTTER, 2.0)])
@pytest.mark.parametrize("heading,knots", [(240.0, 11.0), (270.0, 8.0), (300.0, 4.5)])
def test_a_fore_and_after_brought_to_holds_her_tack_in_her_own_manner(
    ship, most_kn, heading, knots
):
    """The schooner and the cutter, hove to the fore-and-after's way (the main sheet flat
    aft, the staysail's sheet to windward, the topsail to the mast): from a run, a reach
    and by the wind her head never comes within a point of the wind's eye, and after ten
    minutes she lies between four and seven points from it forereaching a knot or two."""
    world = world_for(ship, heading, knots)
    start = world.clock.tick
    sign, off, at_ten = bring_to(world, minutes=12)
    assert min(off) > POINT_DEG, min(off)
    assert all(4 * POINT_DEG - 1.0 <= o <= 7 * POINT_DEG for o in off[600:])
    assert abs(at_ten) < most_kn, at_ten
    assert len(events(world, "ship.hove_to", after=start)) == 1
    assert world.ship.extra["hove_to"]["sign"] == sign
    assert not events(world, "ship.forced_round", "ship.filled", after=start)


def shifting_weather() -> list[dict]:
    """Six hours and more of a wind from north that shifts two points at a time and
    ranges from three knots to twenty-two."""
    points = [
        (0, 0.0, 10.0),
        (30, 0.0, 10.0),
        (40, 22.5, 6.0),
        (70, 22.5, 3.0),
        (100, 0.0, 3.0),
        (130, 0.0, 8.0),
        (140, -22.5, 12.0),
        (180, -22.5, 16.0),
        (190, 0.0, 22.0),
        (230, 0.0, 22.0),
        (240, 22.5, 14.0),
        (280, 22.5, 9.0),
        (290, 0.0, 5.0),
        (330, 0.0, 4.0),
        (340, -22.5, 10.0),
        (420, -22.5, 10.0),
    ]
    return [
        {"at": (START + timedelta(minutes=m)).isoformat(), "from_deg": d % 360.0, "knots": k}
        for m, d, k in points
    ]


@pytest.mark.parametrize("ship", [BRIG, FRIGATE, SCHOONER, CUTTER])
def test_held_six_hours_through_shifts_and_all_winds_she_never_lies_abaft_the_beam(ship):
    """Hove to and held six hours through winds of three to twenty-two knots and shifts
    of two points, with the gusts and the wander on: she is never through the wind and
    never lies with it abaft the beam; the record stands; and the watch's tending writes
    one routine line a watch and nothing else."""
    world = world_for(ship, 292.0, 10.0, gust=0.3, wander=0.3, weather=shifting_weather())
    start = world.clock.tick
    world.submit("heave to")
    sign = 1.0
    low, high, fastest, winds = 180.0, -180.0, 0.0, set()
    hove = False
    for _ in range(6 * 3600):
        world.tick()
        hove = hove or "hove_to" in world.ship.extra
        if not hove:
            continue
        off = sign * wind_on_bow(world)
        low, high = min(low, off), max(high, off)
        fastest = max(fastest, abs(way_kn(world)))
        winds.add(round(units.ms_to_knots(world.wind.effective_speed)))
    assert min(winds) <= 3 and max(winds) >= 22
    assert low > POINT_DEG and high < 90.0, (low, high)
    assert 3.5 * POINT_DEG < low and high < 7.5 * POINT_DEG, (low, high)
    assert world.ship.extra["hove_to"]["sign"] == sign
    assert fastest < 3.5, fastest  # the cutter forereaches three knots in twenty-two of wind
    assert not events(world, "ship.forced_round", "ship.filled", "ship.aback", after=start)
    # 04:35 to 10:35: one change of the watch, at eight, and one routine line for it
    lines = events(world, "ship.lying_to", after=start)
    assert [e.severity.value for e in lines] == ["routine"]
    assert lines[0].ship_time.hour == 8 and lines[0].text.startswith(
        "Lying to on the starboard tack, her head "
    )
    assert lines[0].text.endswith("; the watch tending the helm and the sheets.")
    # the tending itself says nothing: no helm order, no sheet trimmed, in the log
    tended = [
        e
        for e in world.log
        if e.tick > start + 900 and e.kind in ("helm.order", "sail.trimmed", "helm.steady")
    ]
    assert tended == []


def test_the_frigate_brought_to_from_a_run_has_her_head_yards_braced_up():
    """Luce 1884, ch. XXVI, 'To heave to, having the wind aft, or on the quarter': "meet
    her, as she comes to, with the helm, and by bracing up the head yards, and hauling
    aft the head sheets". Left as they were trimmed for the wind on the quarter the yards
    that stay full are all but square, and every sail she has is aback when her head is
    five points from the wind: the brig so went astern at a knot and a half for as long
    as she lay."""
    world = world_for(FRIGATE, 240.0, 15.0)
    fore = world.ship.spars["fore.topsail.yard"]
    assert abs(fore.brace_angle) < 0.75 * fore.brace_limit  # braced in for the quarter
    start = world.clock.tick
    sign, off, at_ten = bring_to(world, minutes=11)
    assert fore.brace_angle == pytest.approx(sign * fore.brace_limit, abs=0.1)
    main = world.ship.spars["main.topsail.yard"]
    assert main.brace_angle == pytest.approx(-sign * main.brace_limit)
    steps = [e.text for e in events(world, "evolution.step", after=start)]
    assert any("braced up the other yards" in t for t in steps)
    assert 0.0 < at_ten < 1.5 and min(off) > 4 * POINT_DEG


def test_the_tending_costs_the_watch_its_hands_and_the_relief_takes_them_over():
    """It is a duty of the watch on deck and costs its hands: `keep_hands` of them stand
    by the spanker and head sheets while she lies to, are taken afresh from the relief
    when the watch changes, and are given back when she fills away."""
    world = world_for(BRIG, 292.0, 10.0)
    crew = world.ship.extra["crew"]

    def at_the_sheets():
        return [s for s in crew.sailors if s.at == scripts.LYING_TO_HANDS]

    assert at_the_sheets() == []
    world.submit("heave to")
    world.run(600)
    held = at_the_sheets()
    assert len(held) == 4 and len({s.watch for s in held}) == 1
    first_watch = held[0].watch
    # 04:30 or so: run on past eight bells, when the other watch relieves the deck
    while world.clock.ship_time.hour < 8:
        world.run(60)
    world.run(120)
    relieved = at_the_sheets()
    assert len(relieved) == 4 and {s.watch for s in relieved} != {first_watch}
    world.submit("fill away")
    world.run(5)
    assert at_the_sheets() == []
    world.run(300)
    assert "hove_to" not in world.ship.extra and at_the_sheets() == []


def test_a_conning_word_given_while_she_lies_to_is_the_captains_helm():
    """`right the helm` or `helm a-weather` said to a ship hove to puts the helm where the
    captain says, and the watch leaves it there and tends the sheets alone: an order is
    not undone a second after it is given."""
    world = world_for(BRIG, 292.0, 10.0)
    world.submit("heave to")
    world.run(600)
    assert world.ship.dyn.target_rudder != 0.0
    e = world.submit("right the helm")
    assert e.kind == "helm.order", e.text
    world.run(120)
    assert world.ship.dyn.helm_mode is HelmMode.RUDDER and world.ship.dyn.target_rudder == 0.0
    assert world.ship.extra["hove_to"]["helm_by_order"] is True


# ---------------------------------------------------------------------------
# Item 1: forced round all the same
# ---------------------------------------------------------------------------


def shift_the_wind(world, points: float) -> None:
    """The wind shifted `points` at a stroke (a squall's front: nothing the weather of
    the game does in a second, and so the one way to force her round in a test)."""
    wind = world.wind
    wind.follow(units.wrap_2pi(wind.base_direction + points * units.POINT), wind.base_speed)
    world.scenario.wind_from_deg = math.degrees(wind.base_direction)


def test_forced_round_by_a_shift_one_urgent_line_says_so_and_the_record_follows_her():
    """A shift of eight points across her bow: one urgent line says she has been forced
    round, and the record follows what she is doing. She lies on the other tack with her
    fore topsail to the mast, hove to on it; and then, her after yards full and gathering
    way, she is hove to no longer, in a second urgent line that says so."""
    world = world_for(BRIG, 292.0, 10.0)
    world.submit("heave to")
    world.run(600)
    record = world.ship.extra["hove_to"]
    assert record["sign"] == 1.0 and "main.topsail.yard" in record["yards"]
    start = world.clock.tick
    shift_the_wind(world, -8.0)
    world.run(60)
    round_ = events(world, "ship.forced_round", after=start)
    assert len(round_) == 1 and round_[0].severity.value == "urgent"
    assert round_[0].text == (
        "She has been forced round through the wind and lies on the larboard tack, the fore "
        "topsail to the mast: hove to on it. To stand on, fill away."
    )
    record = world.ship.extra["hove_to"]
    assert record["sign"] == -1.0 and "fore.topsail.yard" in record["yards"]
    assert "main.topsail.yard" not in record["yards"]
    assert world.readings.words("manoeuvre_in_hand") == "hove to"
    # lying there she gathers a knot and three quarters under her main topsail, full
    world.run(600)
    assert len(events(world, "ship.forced_round", after=start)) == 1
    filled = events(world, "ship.filled", after=start)
    assert len(filled) == 1 and filled[0].severity.value == "urgent"
    assert filled[0].text.startswith("Her after yards full, she gathers way, the wind on the")
    assert filled[0].text.endswith("hove to no longer. The helm keeps her full and by.")
    assert "hove_to" not in world.ship.extra
    assert world.readings.words("manoeuvre_in_hand") == "none"
    assert world.ship.dyn.helm_mode is HelmMode.FULL_AND_BY
    e = world.submit("steer west")  # and a course is taken at the first order
    assert e.kind == "helm.order", e.text


def test_a_brig_under_her_topsails_alone_that_falls_off_is_said_to_be_hove_to_no_longer():
    """Under her two topsails the brig has no sheet to regulate by: forced round, she
    falls off and lies with the wind abaft the beam, which is not lying to, and the log
    says so urgently (before this package she lay so for hours, going astern at two knots,
    the game answering "She is hove to")."""
    scenario = Scenario(
        start_time=START,
        wind_from_deg=225.0,
        wind_speed_kn=12.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=300.0,
    )
    world = make_world(7, BRIG, scenario)
    world.submit("set topsails")
    world.run(600)
    world.submit("heave to")
    world.run(1800)
    assert "hove_to" not in world.ship.extra
    said = events(world, "ship.filled")
    assert len(said) == 1 and said[0].severity.value == "urgent"
    assert "and the helm and the sheets will not bring her to: hove to no longer." in said[0].text
    assert said[0].data["why"] == "fallen off"


# ---------------------------------------------------------------------------
# Item 2: fill away on the tack she is on, and fill away and steer
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("heading,tack,course", [(292.0, "starboard", 292), (68.0, "larboard", 68)])
def test_fill_away_fills_her_on_the_tack_she_is_on(heading, tack, course):
    world = world_for(BRIG, heading, 10.0)
    world.submit("heave to")
    world.run(600)
    start = world.clock.tick
    e = world.submit("fill away")
    assert e.kind == "order.accepted", e.text
    world.run(420)
    done = events(world, "ship.filled_away", after=start)
    assert len(done) == 1
    assert done[0].text.startswith(f"Filled away on the {tack} tack; braced full and steering ")
    assert done[0].data["tack"] == tack
    assert abs(done[0].data["course_deg"] - course) < 3.0
    assert "hove_to" not in world.ship.extra
    assert not events(world, "ship.aback", after=start)
    assert way_kn(world) > 2.5 and abs(abs(wind_on_bow(world)) - 67.5) < 6.0
    assert (wind_on_bow(world) > 0) == (tack == "starboard")


def test_a_ship_that_has_come_round_is_filled_on_her_new_tack_not_the_recorded_one():
    """In game 9 `fill away` braced and steered for the tack recorded when she hove to,
    and took a brig that had put herself about back through the wind with every sail
    aback, three times. Put about by hand as she put herself, she is filled where she
    lies: her head never comes back within three points of the wind, and nothing is taken
    aback."""
    world = world_for(BRIG, 292.0, 10.0)
    world.submit("heave to")
    world.run(600)
    dyn = world.ship.dyn
    dyn.heading = units.wrap_2pi(world.wind.direction_from + math.radians(60.0))
    dyn.r = 0.0
    assert wind_on_bow(world) < 0  # on the larboard tack now, the record still starboard
    start = world.clock.tick
    world.submit("fill away")
    nearest = 180.0
    for _ in range(420):
        world.tick()
        nearest = min(nearest, -wind_on_bow(world))
    done = events(world, "ship.filled_away", after=start)
    assert len(done) == 1 and done[0].text.startswith("Filled away on the larboard tack; ")
    assert nearest > 3 * POINT_DEG, nearest
    assert not events(world, "ship.aback", after=start)
    assert way_kn(world) > 2.0 and wind_on_bow(world) < -55.0
    fore = world.ship.spars["fore.topsail.yard"]
    assert fore.brace_angle < 0  # braced round for the larboard tack


def test_fill_away_and_steer_gives_the_helm_the_course_when_she_is_full():
    """`fill away and steer <course>`, as the owner typed it: she is filled, and the helm
    then has the course; the words name the tack and the course."""
    world = world_for(BRIG, 292.0, 10.0)
    world.submit("heave to")
    world.run(600)
    start = world.clock.tick
    e = world.submit("fill away and steer WSW")
    assert e.kind == "order.accepted", e.text
    world.run(420)
    done = events(world, "ship.filled_away", after=start)
    assert [d.text for d in done] == [
        "Filled away on the starboard tack; braced full and steering WSW (248°), the course "
        "ordered."
    ]
    assert done[0].data["course_ordered"] is True
    dyn = world.ship.dyn
    assert dyn.helm_mode is HelmMode.HEADING
    assert math.degrees(dyn.target_heading) == pytest.approx(247.5)
    assert abs(math.degrees(units.wrap_pi(dyn.heading - dyn.target_heading))) < 3.0
    assert way_kn(world) > 3.0 and not events(world, "ship.aback", after=start)
    # degrees are taken as a compass point is
    again = world_for(BRIG, 292.0, 10.0)
    again.submit("heave to")
    again.run(600)
    assert again.submit("fill away and steer 250").kind == "order.accepted"
    again.run(420)
    assert math.degrees(again.ship.dyn.target_heading) == pytest.approx(250.0)


def test_filled_for_a_course_off_the_wind_she_is_braced_by_the_wind_first_and_nothing_lifts():
    """Braced at once for a course with the wind abaft the beam, the frigate's topsails
    lifted with her head still five points from the wind, and the log said "Her sails
    aback". She is braced full by the wind first, and her yards and sheets are trimmed to
    the wind she has as she pays off (Luce: "As she falls off ... trim to the course")."""
    world = world_for(FRIGATE, 292.0, 14.0)
    world.submit("heave to")
    world.run(600)
    start = world.clock.tick
    assert world.submit("fill away and steer W by S").kind == "order.accepted"
    world.run(420)
    (done,) = events(world, "ship.filled_away", after=start)
    assert done.text.endswith("steering W by S (259°), the course ordered.")
    assert 60 < done.tick - start <= 300  # full in a minute, on her course in three or four
    assert not events(world, "ship.aback", "sail.backed", after=start)
    dyn = world.ship.dyn
    assert abs(math.degrees(units.wrap_pi(dyn.heading - dyn.target_heading))) < 3.0
    assert way_kn(world) > 4.5
    # her yards are trimmed for the course's wind, not left sharp up
    fore = world.ship.spars["fore.topsail.yard"]
    assert abs(math.degrees(fore.brace_angle)) < math.degrees(fore.brace_limit) - 8.0


def test_fill_away_and_steer_a_course_she_cannot_lay_keeps_her_full_and_by_and_says_so():
    world = world_for(BRIG, 292.0, 10.0)
    world.submit("heave to")
    world.run(600)
    start = world.clock.tick
    world.submit("fill away and steer east")  # across the wind, on the other tack
    world.run(420)
    done = events(world, "ship.filled_away", after=start)
    assert len(done) == 1 and done[0].data["course_ordered"] is False
    assert done[0].text == (
        "Filled away on the starboard tack; braced full and steering WNW (292°), full and by "
        "(E (90°) lies on the other tack; she is kept full and by on the starboard tack: "
        "tack or wear for it)."
    )
    assert wind_on_bow(world) > 55.0 and not events(world, "ship.aback", after=start)
    # too near the wind on her own tack
    world = world_for(BRIG, 292.0, 10.0)
    world.submit("heave to")
    world.run(600)
    start = world.clock.tick
    world.submit("fill away and steer NW")
    world.run(420)
    done = events(world, "ship.filled_away", after=start)
    assert "NW (315°) lies too near the wind to be laid" in done[0].text
    # and the order with no course after it is refused in words
    with pytest.raises(OrderError, match="Fill away and steer where"):
        orders.handle(world_for(BRIG, 292.0, 10.0).ship, "fill away and steer")


# ---------------------------------------------------------------------------
# Item 3: the record that she is hove to
# ---------------------------------------------------------------------------


def test_the_record_is_cleared_by_a_tack_and_by_a_wear():
    """In the playtests the record survived a tack and refused a course to a ship under
    way for twenty-three minutes. A ship going about is hove to no longer: a wear from
    lying to clears it as the helm goes up, and a tack at "ready about" (a tack is refused
    a ship lying to, for want of way; its script is begun by hand here)."""
    world = world_for(FRIGATE, 292.0, 12.0)
    world.submit("heave to")
    world.run(600)
    assert "hove_to" in world.ship.extra
    e = world.submit("tack ship")
    assert e.kind == "order.rejected", e.text
    e = world.submit("wear ship")
    assert e.kind == "order.accepted", e.text
    world.run(5)
    assert "hove_to" not in world.ship.extra
    assert world.readings.words("manoeuvre_in_hand") == "wearing"
    # the tack's own beginning
    world = world_for(FRIGATE, 292.0, 12.0)
    world.submit("heave to")
    world.run(600)
    assert "hove_to" in world.ship.extra
    tack = scripts.TackScript(world.ship, {}, {})
    tack.begin({})
    assert "hove_to" not in world.ship.extra


def test_lain_a_try_anchored_and_weighed_she_takes_a_course_at_the_first_order():
    """The Roscoff morning of game 9: the brig lay a-try before she anchored, and the
    record outlived the night at anchor; with the anchor up `steer` was refused four times
    as "She is hove to", and `fill away` then turned her east into the road. The record is
    cleared when the anchor is let go: at anchor the manoeuvre in hand is none, and
    weighed, she takes a course at the first order."""
    scenario = Scenario(
        start_time=datetime(1805, 6, 10, 10, 0),
        wind_from_deg=225.0,
        wind_speed_kn=12.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=290.0,
        ship_speed_kn=3.0,
        position={"lat_deg": 50.120, "lon_deg": -5.030},  # the bay off Falmouth, twelve fathoms
        region="channel-west",
    )
    world = make_world(7, BRIG, scenario)
    for order in (
        "set topsails",
        "set the fore topmast staysail",
        "brace sharp up on the larboard tack",
    ):
        world.submit(order)
    world.run(600)
    world.submit("lie a try")
    world.run(900)
    assert world.ship.extra["hove_to"]["how"] == "a-try"
    assert world.submit("steer SW").kind == "order.rejected"  # lying to: as ever
    e = world.submit("come to an anchor")
    assert e.kind == "order.accepted", e.text
    for _ in range(3600):
        world.tick()
        if events(world, "ship.brought_up"):
            break
    assert world.at_anchor and "hove_to" not in world.ship.extra
    let_go = events(world, "ship.anchored")[0].tick
    assert not [e for e in world.log if e.kind == "ship.lying_to" and e.tick > let_go]
    assert world.readings.words("manoeuvre_in_hand") == "none"
    world.run(1800)  # the night at anchor
    assert world.readings.words("manoeuvre_in_hand") == "none"
    world.submit("weigh")
    for _ in range(3600):
        world.tick()
        if events(world, "ship.weighed"):
            break
    assert not world.at_anchor and "hove_to" not in world.ship.extra
    e = world.submit("steer SW")
    # (the wind is from the SW: steered as given into the wind's eye, and the line says
    # what that does, package 37m)
    assert e.kind == "helm.order" and e.text == (
        "Helm ordered: steer SW (225°); SW (225°) lies in the wind's eye from her head; she "
        "will be taken aback."
    ), e.text
    e = world.submit("fill away")
    assert e.kind == "order.rejected" and "She is not hove to" in e.text


def test_the_record_is_cleared_when_an_anchor_is_let_go_and_when_she_takes_the_ground():
    """`let go the anchor` to a ship hove to (as she was brought to in the Goulet), and a
    ship that drives ashore lying to: each ends the heave-to, the watch's hands with it."""
    scenario = Scenario(
        start_time=datetime(1805, 6, 10, 10, 0),
        wind_from_deg=225.0,
        wind_speed_kn=12.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=290.0,
        ship_speed_kn=3.0,
        position={"lat_deg": 50.120, "lon_deg": -5.030},
        region="channel-west",
    )
    world = make_world(7, BRIG, scenario)
    world.submit("set plain sail")
    world.submit("brace sharp up on the larboard tack")
    world.run(600)
    world.submit("heave to")
    world.run(600)
    crew = world.ship.extra["crew"]
    assert "hove_to" in world.ship.extra
    assert [s for s in crew.sailors if s.at == scripts.LYING_TO_HANDS]
    e = world.submit("let go the anchor")
    assert e.kind == "order.accepted", e.text
    world.run(60)
    assert world.at_anchor and "hove_to" not in world.ship.extra
    assert not [s for s in crew.sailors if s.at == scripts.LYING_TO_HANDS]
    assert world.ship.dyn.helm_mode is HelmMode.RUDDER and world.ship.dyn.target_rudder == 0.0
    # the ground: weighed and hove to again, she strikes (the World's own strike, given
    # the chart's word that she has touched)
    from types import SimpleNamespace

    world.submit("weigh")
    for _ in range(3600):
        world.tick()
        if events(world, "ship.weighed"):
            break
    world.submit("set plain sail")
    world.submit("brace sharp up on the larboard tack")
    world.run(420)
    e = world.submit("heave to")
    assert e.kind == "order.accepted", e.text
    world.run(600)
    assert "hove_to" in world.ship.extra
    touched = SimpleNamespace(
        where="forward",
        depth_m=2.0,
        bottom="sand",
        words="She has taken the ground forward",
        to_dict=dict,
    )
    world.ground._strike(touched, False)
    assert world.ship.extra.get("aground") and "hove_to" not in world.ship.extra
    assert not [s for s in crew.sailors if s.at == scripts.LYING_TO_HANDS]


def test_the_reading_and_the_dialects_guard_read_the_one_record():
    """`the manoeuvre in hand`, the dialect's `she is not hove to`, the helm's refusal and
    the trim's all read `ship.extra["hove_to"]`, and all change together when it goes."""
    from freesail.standing import parse_condition

    world = world_for(BRIG, 292.0, 10.0)
    guard = parse_condition("the manoeuvre in hand is not hove to", world.ship)
    assert guard.holds(world.readings) and not verbs.lying_to(world.ship)
    world.submit("heave to")
    world.run(600)
    assert world.readings.words("manoeuvre_in_hand") == "hove to"
    assert not guard.holds(world.readings) and verbs.lying_to(world.ship)
    assert scripts.end_lying_to(world.ship) is True
    world.tick()  # the readings are one view a tick
    assert world.readings.words("manoeuvre_in_hand") == "none"
    assert guard.holds(world.readings) and not verbs.lying_to(world.ship)
    assert scripts.end_lying_to(world.ship) is False
    assert world.submit("steer west").kind == "helm.order"


# ---------------------------------------------------------------------------
# Item 4: trim sails hove to
# ---------------------------------------------------------------------------


def test_trim_sails_is_declined_while_she_is_hove_to_in_words_that_carry_the_cure():
    """The owner's ruling: `trim sails` declines while she is hove to. In two games it
    braced a hove-to ship's backed yards round with the rest, four times, the record left
    standing. A yard braced by name and a sheet hauled by name are still taken."""
    world = world_for(BRIG, 292.0, 10.0)
    world.submit("heave to")
    world.run(30)  # the manoeuvre in hand: declined already
    for words in ("trim sails", "trim the yards", "brace the yards to the wind"):
        e = world.submit(words)
        assert e.kind == "order.rejected", (words, e.text)
        assert e.data["reason"] == (
            "She is hove to; fill away before trimming, or brace a yard by name."
        )
    e = world.submit("trim the sheets")  # every sheet: declined too, and the cure a sheet's
    assert e.kind == "order.rejected" and e.data["reason"] == verbs.HOVE_TO_TRIM_SHEETS_WORDS
    assert e.data["reason"].endswith("or work a sheet by name.")
    world.run(600)
    assert "hove_to" in world.ship.extra
    main = world.ship.spars["main.topsail.yard"]
    aback = main.brace_angle
    e = world.submit("trim sails")
    assert e.kind == "order.rejected" and e.data["reason"] == verbs.HOVE_TO_TRIM_WORDS
    world.run(120)
    assert main.brace_angle == aback and "hove_to" in world.ship.extra
    # by name: taken
    assert world.submit("brace the fore yards in").kind == "order.accepted"
    assert world.submit("ease the jib sheet").kind == "line.eased"
    assert world.submit("trim the jib").kind == "sail.trimmed"
    # filled away, she trims again
    world.submit("fill away")
    world.run(300)
    assert world.submit("trim sails").kind != "order.rejected"


@pytest.mark.parametrize(
    "book",
    [
        "data/standing_orders/starter.orders",
        "data/scenarios/merchant-passage.orders",
        "data/scenarios/naval-cruise.orders",
    ],
)
def test_every_shipped_trim_rule_carries_the_dialects_own_guard(book):
    """The starter book and each scenario book that trims by rule: every rule whose
    orders trim the whole ship sleeps while she is hove to, by the dialect's own guard
    (`the manoeuvre in hand is not hove to`)."""
    from pathlib import Path

    from freesail.standing.book import read_orders_file

    root = Path(__file__).resolve().parents[1]
    found = 0
    for sentence in read_orders_file(root / book):
        head, _, then = sentence.partition(" then ")
        whole_ship = [
            o.strip()
            for o in then.split(";")
            if o.strip() in ("trim sails", "trim the sheets", "trim the yards")
        ]
        if not whole_ship:
            continue
        found += 1
        assert "the manoeuvre in hand is not hove to" in head, sentence
    assert found >= 2, book


def test_the_starter_books_trim_rules_sleep_through_a_heave_to_and_wake_after_it():
    """The wind shifts two points while she lies to: `trim on a shift` and `tend the
    sheets` do not fire and are not refused; filled away, the next shift trims her."""
    world = world_for(
        FRIGATE,
        292.0,
        10.0,
        weather=[
            {"at": START.isoformat(), "from_deg": 0.0, "knots": 10.0},
            {"at": (START + timedelta(minutes=45)).isoformat(), "from_deg": 0.0, "knots": 10.0},
            {"at": (START + timedelta(minutes=55)).isoformat(), "from_deg": 22.5, "knots": 10.0},
            {"at": (START + timedelta(minutes=120)).isoformat(), "from_deg": 22.5, "knots": 10.0},
            {"at": (START + timedelta(minutes=130)).isoformat(), "from_deg": 0.0, "knots": 10.0},
            {"at": (START + timedelta(minutes=300)).isoformat(), "from_deg": 0.0, "knots": 10.0},
        ],
    )
    from freesail.standing.book import read_orders_file

    for line in read_orders_file("data/standing_orders/starter.orders"):
        world.submit(line)
    assert "trim on a shift" in world.standing.book.names
    world.submit("heave to")
    start = world.clock.tick
    while world.clock.ship_time < START + timedelta(minutes=110):
        world.run(60)
    assert "hove_to" in world.ship.extra
    by_rule = [
        e
        for e in world.log
        if e.tick > start
        and e.actor in ("standing order 'trim on a shift'", "standing order 'tend the sheets'")
    ]
    assert [e for e in by_rule if e.kind in ("order.accepted", "order.rejected")] == []
    world.submit("fill away")
    filled = world.clock.tick
    while world.clock.ship_time < START + timedelta(minutes=150):
        world.run(60)
    trimmed = [
        e
        for e in world.log
        if e.tick > filled
        and e.kind == "order.accepted"
        and e.actor in ("standing order 'trim on a shift'", "standing order 'tend the sheets'")
    ]
    assert trimmed, "the trim rules did not wake when she had filled away"


# ---------------------------------------------------------------------------
# Package 37k: heaving to with a sail that is set; the alarm for being taken aback
# ---------------------------------------------------------------------------


def test_a_heave_to_backs_a_sail_that_is_set_and_not_one_being_handed():
    """Item 3 (the review's G7, game 10): the officer was hauling down the cutter's
    foresail at the pilot's hail while the captain hove her to; the heave-to backed that
    same foresail, said "Hove to", and she filled within a minute when it came down. The
    head sail held to windward is one that is set and stays set, and the line says which."""
    w = world_for(CUTTER, 290.0, 12.0)
    foresail = w.ship.sails["fore.staysail"]
    assert foresail.is_set and w.ship.sails["jib"].is_set
    assert w.submit("take in the foresail").kind == "order.accepted"
    w.run(2)
    assert scripts.being_handed(w.ship, foresail)
    assert w.submit("heave to").kind == "order.accepted"
    w.run(20 * 60)
    steps = [e.text for e in events(w, "evolution.step") if "to windward" in e.text]
    assert steps and "the jib sheet to windward" in steps[0]
    assert "foresail" not in steps[0] and "staysail" not in steps[0]
    assert w.ship.extra["hove_to"]["headsail"] == "jib"
    assert not foresail.is_set
    (hove,) = events(w, "ship.hove_to")
    assert hove.text.startswith("Hove to on the starboard tack, ")
    assert "hove_to" in w.ship.extra and not events(w, "ship.filled", "ship.forced_round")
    off = wind_on_bow(w)
    assert 3.0 * POINT_DEG < off < 8.0 * POINT_DEG


def test_a_heave_to_never_lays_a_furled_topsail_to_the_mast():
    """The sail laid to the mast is one that is set and says so: the brig with her main
    topsail furled lays her main topgallant aback and lies to; with nothing standing on
    the main but its course (which a heave-to hauls up), the fore topsail (Luce 1866, ch.
    XXVI, 'To heave to with the fore topsail to the mast')."""
    w = world_for(BRIG, 290.0, 12.0)
    assert w.submit("furl the main topsail").kind == "order.accepted"
    w.run(600)
    assert not w.ship.sails["main.topsail"].is_set and w.ship.sails["main.topgallant"].is_set
    assert w.submit("heave to").kind == "order.accepted"
    w.run(12 * 60)
    said = [e.text for e in events(w, "evolution.step") if "aback" in e.text]
    assert said and said[0].startswith("Braced the main topgallant aback")
    (hove,) = events(w, "ship.hove_to")
    assert hove.text == "Hove to on the starboard tack, main topgallant to the mast, helm a-lee."
    w = world_for(BRIG, 290.0, 12.0)
    assert w.submit("furl the main topsail").kind == "order.accepted"
    assert w.submit("furl the main topgallant").kind == "order.accepted"
    w.run(900)
    assert not w.ship.sails["main.topgallant"].is_set and w.ship.sails["fore.topsail"].is_set
    assert w.submit("heave to").kind == "order.accepted"
    w.run(60)
    said = [e.text for e in events(w, "evolution.step") if "aback" in e.text]
    assert said and said[0].startswith("Braced the fore topsail aback")


def test_a_sail_still_being_set_or_trimmed_is_left_out_of_the_alarm():
    """Item 4: in game 10 two of the eight urgent cries of "Taken aback" came as sail was
    being made after weighing, the wind abeam and her way rising, the sails not yet
    sheeted and trimmed. A sail the hands are at is not judged; the sails that stand are."""
    from freesail.physics import integrate
    from freesail.physics.sails import sails_in_hand

    w = world_for(BRIG, 270.0, 12.0)
    runner = w.ship.extra["evolutions"]
    jib = w.ship.sails["flying_jib"]
    assert not jib.is_set
    assert w.submit("set the flying jib").kind == "order.accepted"
    runner.step(w.ship, 1.0, w.wind)
    assert sails_in_hand(w.ship) == {jib.id}
    # hoisted and not yet sheeted home and trimmed; every other sail furled, so that the
    # one sail she has set is the one the hands are at
    for sl in w.ship.sails.values():
        if sl.is_set:
            sl.state = SailState.FURLED
    jib.state = SailState.SET

    # the sail read as aback and the thrust astern, as the physics gives them for a sail
    # aback: ten seconds of it is the cry, for a sail that stands
    def aback(world, seconds=15):
        st = integrate.hp.hull_state(world.ship)
        for _ in range(seconds):
            st.last_thrust_n = -20_000.0
            for sl in world.ship.sails.values():
                sl.backed = sl.is_set
            integrate._log_notes(world.ship, st, 1.0)

    st = integrate.hp.hull_state(w.ship)
    st.seconds_aback, st.aback_noted, st.aback_lesser = 0.0, False, ""
    w.ship.drain_notes()
    aback(w)
    assert not [n for n in w.ship.drain_notes() if n[1] == "ship.aback"]
    # the work belayed, the same sail stands and is judged
    runner.belay(w.ship, runner.work())
    assert sails_in_hand(w.ship) == set()
    aback(w)
    assert len([n for n in w.ship.drain_notes() if n[1] == "ship.aback"]) == 1


def test_her_sails_lifting_is_said_before_she_is_taken_aback():
    """Item 4: "Taken aback" was cried eight times in game 10 "with no warning line before
    any of them". On a compass course close-hauled the wind heading her by a point at a
    time: "Her sails lifting", notable, comes first, and the cry after it."""
    from freesail.api import readings as R
    from freesail.core.events import Severity

    w = world_for(FRIGATE, 292.0, 14.0)
    n0 = len(w.log.all())
    for _ in range(8):
        shift_the_wind(w, -1.0)  # backing: ahead of her on the starboard bow
        w.run(40)
        if [e for e in w.log.all()[n0:] if e.kind == "ship.aback"]:
            break
    lines = [e for e in w.log.all()[n0:] if e.kind in ("ship.lifting", "ship.aback")]
    assert lines and lines[0].kind == "ship.lifting", [(e.kind, e.text) for e in lines]
    assert lines[0].severity is Severity.NOTABLE
    assert lines[0].text.startswith("Her sails lifting, the wind ")
    assert lines[0].text.endswith(
        " on the starboard bow: keep her away, or she will be taken aback."
    )
    assert len([e for e in lines if e.kind == "ship.lifting"]) == 1  # once an episode
    assert R.speaks_of_danger("ship.lifting", {}) == "her sails lifting"
    assert R.EVENTS["her sails lifting"].kind == "ship.lifting"


def test_no_lifting_line_under_full_and_by_in_a_steady_breeze():
    """Full and by the helmsman keeps her a margin outside her luffing angle: nothing
    lifts, and the line is not said."""
    w = world_for(FRIGATE, 292.0, 14.0)
    w.submit("keep her full and by")
    n0 = len(w.log.all())
    w.run(30 * 60)
    assert not [e for e in w.log.all()[n0:] if e.kind == "ship.lifting"]
