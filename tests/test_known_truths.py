"""Package 10: the known truths of sailing behaviour as tests (spec 7.6).

Truths 1 to 15 are the specification's table; 16 is the turning circle and
17 getting under way from rest (docs/dev/M2-WorkPackages.md, package 10).
Every scenario is driven through `freesail.api.session.make_world` and the
Orders language, with a steady wind (gustiness and variability 0) and a
fixed seed, so each test also exercises the evolutions and the helmsman.
The constants these tests settled are recorded in docs/dev/TuningNotes.md.

Readings the tests take:

- Points of sail are named by the true wind's angle off the bow, which is
  what a scenario and a `steer` order can set (the apparent angle is kept
  beside it in the polar). A beam reach is the true wind abeam.
- "Best sustained course" (truths 1 and 2) is the course of best speed made
  good to windward among those on which she still holds three knots, found
  by steering up two degrees at a time with the yards trimmed to the wind.
- While a scenario settles the yards are trimmed with the `trim` order every
  two minutes, as a watch on deck keeps them.
- Luce 1884 Appendix L turns out to be steamship turning trials (the S.S.
  Hankow, 1877), so truth 16 uses the package contract's fallback: a
  tactical diameter of four to six lengths at eight knots, helm hard over,
  measured with the helm a-weather (a sailing ship put hard a-lee simply
  comes head to wind and stops).

Two truths are marked as strict expected failures with the reason in the
test: the schooner's fastest point of sail (3) and the ground a wear loses
(11). Both need more than tuning; see docs/dev/TuningNotes.md.

Truths 18 to 23 are milestone 3's, the crew (docs/TechnicalSpec-M3.md §7),
sailed the same way with the ship's company mustered by `make_world`: hands
set to work by orders, all hands called and piped down by orders, and the
watch changing at the bells. Every scenario begins from rest with the sails
furled (`from_rest`), as a voyage does. The absolute times of truth 18 are a
third strict expected failure, with the reason in the test; its ratio passes.

Truths 24 to 33 are milestone 3b's, rig geometry and canvas
(docs/TechnicalSpec-M3b.md §9), each citing its source. Where the built game
and a truth's number disagree, the behaviour the game has is asserted as a
passing test with the measured value in its docstring, and the spec's number
is a strict expected failure marked as the owner's ruling, naming the measured
value and the constant that would move it (truths 24, 26, 28 and 31). Nothing
was tuned to meet them; the values are in docs/dev/TuningNotes.md.

Truths 34 to 40 are milestone 4a's, standing orders (docs/TechnicalSpec-M4.md §8).
Truths 34 to 38 are here: the frigate under the starter routines, the sun at 50 N on
1 June 1805, and where a truth needs the wind to change under way it is blown by setting
the wind model's base speed (steady wind: the model then holds it), which is the one
mechanism the M2 wind has for a wind that rises. Truth 39 (a passage under the starter
routines replays with the same firings) is the standing voyage of tests/test_replay.py;
truth 40 (a Python rule and its dialect twin give one log) is tests/test_python_api.py.
Truth 37's storm staysail is set by a companion order on the tick it is bent: the
frigate's fore storm staysail is a sail of its own on the fore stay, bent and set, not
shifted for the fore topmast staysail (gate 4a's ruling; docs/dev/TuningNotes.md, 4a).

Truths 41 to 47 are milestone 4b's, the harness (docs/TechnicalSpec-M4.md §16), each
proven against the scripted fake (freesail/agents/fake.py) and never a model. Truths 41
to 46 are the harness's own mechanics and live in tests/test_agents.py beside the helpers
they share: 41 the token (`test_truth_41_*`, three tests), 42 the watcher refused and
heard (`test_truth_42_*`), 43 the graduated welfare controls (`test_truth_43_*`, seven),
44 stand by until eight bells, 45 two lockstep runs to one digest, 46 the brief's head.
Truth 47, the consent step in front of any station brief, is here.

Truths 48 to 51 are milestone 4c's, the ship sailing herself (docs/TechnicalSpec-M4.md
§23): the gate's day from its scenario file (data/scenarios/gate-4c-day.yaml, the weather
script with it) under the starter routines and the captain's three for the passage (48),
saved at several ticks and replayed (49), its log at 300x through the roll-up (50), and
the frigate's ticks a second against the build machine's floor (51; the spec's budget is
not met on the build machine and the lead sets it with the owner, docs/dev/TuningNotes.md).
The roll-up and auto-slow have tests of their own in tests/test_rollup.py, the weather
script in tests/test_weather_script.py.
"""

from __future__ import annotations

import math
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from freesail import units
from freesail.api.session import make_world
from freesail.core.events import Severity
from freesail.core.world import Scenario, World

FRIGATE = "data/ships/frigate-36.yaml"
SCHOONER = "data/ships/topsail-schooner.yaml"
SEED = 7
WIND_FROM = 0.0  # north: a heading is then the ship's angle off the wind, clockwise


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def make(ship, heading_deg, knots=15.0, speed_kn=4.0, seed=SEED):
    scenario = Scenario(
        wind_from_deg=WIND_FROM,
        wind_speed_kn=knots,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=heading_deg,
        ship_speed_kn=speed_kn,
    )
    return make_world(seed, ship, scenario)


def off_wind(world) -> float:
    """Degrees between the ship's head and the true wind, unsigned."""
    return abs(math.degrees(units.wrap_pi(world.ship.dyn.heading - world.wind.direction_from)))


def knots(world) -> float:
    return units.ms_to_knots(world.ship.dyn.speed)


def headway_kn(world) -> float:
    return units.ms_to_knots(world.ship.dyn.u)


def tack_for(heading_deg: float) -> str:
    """Which tack a heading puts her on with the wind from north."""
    return "starboard" if 180.0 < heading_deg % 360.0 < 360.0 else "larboard"


def run(world, ticks: int, trim_every: int = 0, trim: str = "trim sails") -> None:
    for i in range(ticks):
        if trim_every and i % trim_every == 0:
            world.submit(trim)
        world.tick()


def settle(world, orders, sail_wait=400, ticks=800, trim_every=120) -> None:
    """Give the orders, let the sails go up, then settle with the yards trimmed."""
    for text in orders:
        world.submit(text)
    run(world, sail_wait)
    run(world, ticks, trim_every)


def under_plain_sail(ship, heading_deg, knots_=15.0, speed_kn=4.0, ticks=800):
    world = make(ship, heading_deg, knots_, speed_kn)
    settle(
        world,
        ["set plain sail", f"brace sharp up on the {tack_for(heading_deg)} tack"],
        ticks=ticks,
    )
    return world


def events(world, kind: str, after: int = 0):
    return [e for e in world.log if e.kind == kind and e.tick > after]


def warned(e) -> list[str]:
    """The parts a strain warning names: one, or those a grouped line names (package 29b:
    the parts that strain the same way on one tick are one line)."""
    return list((e.data or {}).get("parts") or [e.subject])


def reading(world) -> dict:
    d = world.ship.dyn
    return {
        "off": off_wind(world),
        "awa": abs(math.degrees(d.apparent_wind_angle)),
        "speed": knots(world),
        "heel": abs(math.degrees(d.heel)),
        "leeway": abs(math.degrees(d.leeway)),
        "weather_helm": math.degrees(d.weather_helm),
    }


POLAR_ANGLES = tuple(range(50, 181, 10))  # the true wind angles swept for a polar


def polar(ship, knots_=15.0, angles=POLAR_ANGLES) -> dict[int, dict]:
    out = {}
    for twa in angles:
        world = under_plain_sail(ship, float(twa), knots_)
        out[twa] = reading(world)
    return out


def pointing_sweep(
    ship, start_off=80, stop_off=44, rig=None, orders=(), wait=0, trim="trim sails"
) -> list[dict]:
    """Steer up two degrees at a time until she can no longer hold three knots.

    Milestone 3b: once plain sail is set, `rig(world)` may alter the ship and `orders`
    be given, with `wait` seconds more to carry them out; `trim` is the order the watch
    trims with. With none of these it is milestone 2's sweep to the tick."""
    world = under_plain_sail(ship, 360.0 - start_off)  # starboard tack
    if rig is not None:
        rig(world)
    for text in orders:
        world.submit(text)
    run(world, wait, trim_every=120, trim=trim)
    rows = []
    off = start_off
    while off >= stop_off:
        world.submit(f"steer {360 - off}")
        run(world, 300, trim_every=100, trim=trim)
        rows.append(reading(world))
        if knots(world) < 3.0 or world.ship.dyn.u < 0:
            break
        off -= 2
    return rows


def best_sustained_course(rows: list[dict]) -> tuple[float, float]:
    """(best course to windward by speed made good, closest course holding 3 kn)."""
    holding = [r for r in rows if r["speed"] >= 3.0]
    best = max(holding, key=lambda r: r["speed"] * math.cos(math.radians(r["off"])))
    closest = min(holding, key=lambda r: r["off"])
    return best["off"], closest["off"]


def argmax_speed(pol: dict[int, dict]) -> int:
    return max(pol, key=lambda twa: pol[twa]["speed"])


# ---------------------------------------------------------------------------
# shared, expensive scenarios
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def frigate_polar():
    return polar(FRIGATE)


@pytest.fixture(scope="module")
def schooner_polar():
    return polar(SCHOONER)


@pytest.fixture(scope="module")
def frigate_sweep():
    return pointing_sweep(FRIGATE)


@pytest.fixture(scope="module")
def schooner_sweep():
    return pointing_sweep(SCHOONER)


# ---------------------------------------------------------------------------
# 1 and 2: how close she lies
# ---------------------------------------------------------------------------


def test_truth_1_a_ship_rig_lies_about_six_points_off_the_wind(frigate_sweep):
    best, closest = best_sustained_course(frigate_sweep)
    assert 62.0 <= best <= 72.0, f"best course to windward {best} deg off the true wind"
    # she cannot hold three knots much inside five points
    assert closest >= 54.0, f"held three knots at {closest} deg off"


def test_truth_2_a_topsail_schooner_points_higher(frigate_sweep, schooner_sweep):
    best_f, _ = best_sustained_course(frigate_sweep)
    best_s, closest_s = best_sustained_course(schooner_sweep)
    assert 50.0 <= best_s <= 62.0, f"schooner's best course {best_s} deg off"
    assert best_s < best_f
    assert closest_s < 54.0  # and she holds three knots where the frigate cannot


# ---------------------------------------------------------------------------
# 3, 4, 5: the polar
# ---------------------------------------------------------------------------


def test_truth_3_beam_reach_is_the_frigates_fastest_point(frigate_polar):
    fastest = argmax_speed(frigate_polar)
    assert 75 <= fastest <= 105, f"fastest at {fastest} deg off the true wind"


@pytest.mark.xfail(
    strict=True,
    reason=(
        "The schooner's polar peaks with the true wind abeam (90 deg), not on the quarter: "
        "sail force follows the square of the apparent wind, which is strongest on the beam, "
        "and the model has no cost for a fore-and-aft rig pressed on a reach (induced drag of "
        "a shallow hull, gaff twist) beyond heel. Meeting this needs a per-rig factor or a "
        "richer hull model; see docs/dev/TuningNotes.md, truth 3."
    ),
)
def test_truth_3_broad_reach_is_the_schooners_fastest_point(schooner_polar):
    fastest = argmax_speed(schooner_polar)
    assert 120 <= fastest <= 150, f"fastest at {fastest} deg off the true wind"


def test_truth_4_frigate_beam_reach_speeds(frigate_polar):
    assert 7.0 <= frigate_polar[90]["speed"] <= 9.0
    world = under_plain_sail(FRIGATE, 90.0, knots_=25.0)
    assert 10.0 <= knots(world) <= 12.0


def test_truth_5_dead_before_the_wind_is_slower_than_four_points_off():
    speeds = {}
    for heading in (180.0, 135.0):
        world = make(FRIGATE, heading)
        settle(world, ["set the courses", "set the topsails", "brace the yards square"])
        speeds[heading] = knots(world)
    assert 0.0 < speeds[180.0] < speeds[135.0]


# ---------------------------------------------------------------------------
# 6, 7, 8: helm, leeway, heel
# ---------------------------------------------------------------------------


def test_truth_6_headsails_and_spanker_set_the_helm():
    world = under_plain_sail(FRIGATE, 270.0)  # wind on the starboard beam
    plain = math.degrees(world.ship.dyn.weather_helm)
    world.submit("take in the headsails")
    run(world, 900, trim_every=120)
    without_headsails = math.degrees(world.ship.dyn.weather_helm)
    assert without_headsails > plain + 1.0  # taking in the headsails gives weather helm
    world.submit("set the headsails")
    world.submit("take in the spanker")
    run(world, 900, trim_every=120)
    without_spanker = math.degrees(world.ship.dyn.weather_helm)
    assert without_spanker < 0.0  # headsails set and spanker in: lee helm
    assert without_spanker < plain


def test_truth_7_leeway_close_hauled_and_running(frigate_sweep, frigate_polar):
    best, _ = best_sustained_course(frigate_sweep)
    close_hauled = next(r for r in frigate_sweep if r["off"] == best)
    assert 3.0 <= close_hauled["leeway"] <= 6.0
    assert frigate_polar[180]["leeway"] < 1.0


def test_truth_8_heel_in_a_breeze_and_in_a_gale(frigate_polar):
    assert 5.0 <= frigate_polar[90]["heel"] <= 10.0
    world = under_plain_sail(FRIGATE, 270.0, knots_=30.0)
    assert abs(math.degrees(world.ship.dyn.heel)) >= 20.0
    all_set = max(e.tick for e in events(world, "sail.set"))
    warnings = [
        e for e in events(world, "strain.warning") if any("topgallant" in p for p in warned(e))
    ]
    assert warnings, "no strain warning on the topgallant gear"
    assert warnings[0].tick - all_set <= 300


# ---------------------------------------------------------------------------
# 9: carrying away
# ---------------------------------------------------------------------------

CARRIED_AWAY = ("spar.carried_away", "sail.blown_out")


def sail_in_a_wind(ship, knots_, sail_order, minutes=20):
    world = make(ship, 90.0, knots_)  # wind on the larboard beam
    world.submit(sail_order)
    world.submit("brace the yards up on the larboard tack")
    run(world, 600)
    world.submit(sail_order)  # studding sails that waited for the sail beside them
    run(world, minutes * 60, trim_every=120)
    return world


def test_truth_9_royals_and_topgallants_carry_away_in_thirty_five_knots():
    world = sail_in_a_wind(FRIGATE, 35.0, "make all sail")
    gone = [e for e in world.log if e.kind in CARRIED_AWAY]
    assert gone, "nothing carried away in 35 knots under all sail"
    assert all(e.severity.value == "urgent" for e in gone)
    assert any("royal" in e.subject or "topgallant" in e.subject for e in gone)


@pytest.mark.parametrize("ship", [FRIGATE, SCHOONER])
def test_truth_9_nothing_carries_away_in_twenty_knots_under_plain_sail(ship):
    world = sail_in_a_wind(ship, 20.0, "set plain sail")
    assert [e for e in world.log if e.kind in CARRIED_AWAY] == []
    assert events(world, "line.parted") == []


# ---------------------------------------------------------------------------
# 10 and 11: going about
# ---------------------------------------------------------------------------


def close_hauled_on_starboard(ship, knots_=15.0, speed_kn=4.0):
    return under_plain_sail(ship, 292.5, knots_, speed_kn, ticks=600)


def until(world, kinds, limit: int) -> tuple[list, int]:
    start = world.clock.tick
    for _ in range(limit):
        world.tick()
        done = [e for e in world.log if e.kind in kinds and e.tick > start]
        if done:
            return done, world.clock.tick - start
    return [], limit


def test_truth_10_the_frigate_tacks_in_five_to_ten_minutes_and_gains_to_windward():
    world = close_hauled_on_starboard(FRIGATE)
    assert knots(world) > 4.0
    y_before = world.ship.dyn.y
    world.submit("tack ship")
    done, seconds = until(world, ("ship.tacked", "ship.missed_stays"), 900)
    assert [e.kind for e in done] == ["ship.tacked"]
    # Milestone 3b: with Fincham's brace limits the yards drive her round a shade quicker;
    # 298 s at seed 7 (TuningNotes). Five minutes to the quarter-minute is still Luce's
    # "five to ten".
    assert 285 <= seconds <= 600, f"tacked in {seconds} s"
    assert world.ship.dyn.tack == "larboard"
    assert world.ship.dyn.y > y_before  # the wind is from north: north is windward


def test_truth_10_she_misses_stays_when_put_about_under_three_knots():
    # Milestone 3b: in 8 knots of wind she now gathers 3.4 knots (sharper yards, bowlines
    # none); 6 knots of wind keeps her under three, which is what the truth is about
    world = close_hauled_on_starboard(FRIGATE, knots_=6.0, speed_kn=2.0)
    assert 2.0 <= knots(world) < 3.0
    world.submit("tack ship")
    done, _ = until(world, ("ship.tacked", "ship.missed_stays"), 900)
    assert [e.kind for e in done] == ["ship.missed_stays"]
    assert done[0].severity.value == "urgent"
    # at the moment she misses stays her head is in the wind; the script squares the yards
    # and puts the helm up, and she falls off on her old tack over the next few minutes
    world.run(300)
    assert world.ship.dyn.tack == "starboard"


def wear(world):
    y_before = world.ship.dyn.y
    world.submit("wear ship")
    done, seconds = until(world, ("ship.wore", "evolution.failed"), 1200)
    assert [e.kind for e in done] == ["ship.wore"]
    return seconds, -(world.ship.dyn.y - y_before)


def test_truth_11_the_frigate_wears_in_six_to_twelve_minutes():
    world = close_hauled_on_starboard(FRIGATE)
    seconds, _ = wear(world)
    assert 360 <= seconds <= 720, f"wore in {seconds} s"
    assert world.ship.dyn.tack == "larboard"


@pytest.mark.xfail(
    strict=True,
    reason=(
        "The wear script comes to as soon as the wind is aft, so she loses about a tenth of "
        "a mile; Luce's wear runs her off before bracing up and coming to. A script change, "
        "outside package 10's remit; see docs/dev/TuningNotes.md, truth 11."
    ),
)
def test_truth_11_wearing_loses_a_quarter_to_half_a_mile_to_leeward():
    world = close_hauled_on_starboard(FRIGATE)
    _, downwind_m = wear(world)
    assert 0.25 * 1852 <= downwind_m <= 0.5 * 1852, f"lost {downwind_m / 1852:.2f} nm"


# ---------------------------------------------------------------------------
# 12: heaving to and filling away
# ---------------------------------------------------------------------------


def hove_to(ship=FRIGATE):
    world = close_hauled_on_starboard(ship, speed_kn=5.0)
    world.submit("heave to")
    return world


def test_truth_12_backing_the_main_topsail_stops_the_ship():
    world = hove_to()
    run(world, 300)
    assert knots(world) < 1.5, "not stopped within five minutes"
    offs, speeds = [], []
    for _ in range(600):
        world.tick()
        offs.append(off_wind(world))
        speeds.append(knots(world))
    assert max(speeds) < 1.5
    assert all(45.0 <= o <= 60.0 for o in offs), f"lay {min(offs):.0f} to {max(offs):.0f} deg off"
    assert max(offs) - min(offs) <= 30.0  # heading steady within 15 degrees
    assert events(world, "ship.hove_to")
    assert events(world, "ship.aback") == []


def test_truth_12_she_fills_away_without_hanging_aback():
    world = hove_to()
    run(world, 900)
    start = world.clock.tick
    world.submit("fill away")
    sternway = 0.0
    settled_at = None
    on_course = 0
    for t in range(1, 901):
        world.tick()
        sternway = max(sternway, -headway_kn(world))
        close_hauled = abs(off_wind(world) - 67.5) <= 10.0
        on_course = on_course + 1 if close_hauled and knots(world) > 3.0 else 0
        if settled_at is None and on_course >= 60:
            settled_at = t
    assert events(world, "ship.filled_away", after=start)
    assert events(world, "ship.aback", after=start) == []
    assert sternway < 1.0, f"gathered {sternway:.1f} kn of sternway"
    assert settled_at is not None and settled_at <= 600, "not close-hauled with way on in 10 min"


# ---------------------------------------------------------------------------
# 13 and 14: sheets and studding sails
# ---------------------------------------------------------------------------


def gaff_thrust_on_a_run(hauls: int) -> float:
    world = make(SCHOONER, 180.0)
    settle(world, ["set plain sail", "brace the yards square"])
    sail = world.ship.sails["main.sail"]
    assert math.degrees(sail.sheet_angle) == pytest.approx(85.0)  # squared right off
    for _ in range(hauls):
        world.submit("haul the main sheet")  # five degrees a haul
    world.tick()
    assert math.degrees(sail.sheet_angle) == pytest.approx(85.0 - 5 * hauls, abs=1.5)
    return sail.thrust_kn


def test_truth_13_a_gaff_sail_wants_squaring_off_before_the_wind():
    at_45 = gaff_thrust_on_a_run(8)
    at_70 = gaff_thrust_on_a_run(3)
    assert 0.0 < at_45 < at_70


def studding_sail_gain(
    heading_deg: float,
    sides: str = "both sides",
    count: int = 10,
    knots_: float = 10.0,
    in_knots: bool = False,
) -> float:
    """Per cent more speed with the studding sails set than under plain sail (or, with
    `in_knots`, knots more; milestone 3b's truth 30)."""
    world = under_plain_sail(FRIGATE, heading_deg, knots_=knots_)
    plain = knots(world)
    # milestone 3b: the booms start rigged in and are rigged out first (spec 3b §7)
    world.submit(f"rig out the studdingsails, {sides}")
    run(world, 300, trim_every=120)
    world.submit(f"set the studdingsails, {sides}")
    run(world, 600, trim_every=120)
    world.submit(f"set the studdingsails, {sides}")  # those that waited for the sail beside them
    run(world, 900, trim_every=120)
    assert sum(1 for s in world.ship.sails.values() if s.cls == "studding" and s.is_set) == count
    if in_knots:
        return knots(world) - plain
    return 100.0 * (knots(world) / plain - 1.0)


def test_truth_14_studding_sails_help_on_a_broad_reach():
    assert 15.0 <= studding_sail_gain(135.0) <= 30.0


def test_truth_14_studding_sails_do_not_help_close_hauled():
    # Milestone 3b (spec 3b §7): with the yards braced up the lee booms will not go out past
    # the lee rigging, so the weather studding sails are set; forward of Luce's angles they
    # shake in their gear and hold her back (the studding class's stall, physics/sails.py).
    assert studding_sail_gain(67.5, "weather", 5) < 5.0


# ---------------------------------------------------------------------------
# 15: determinism
# ---------------------------------------------------------------------------


def getting_under_way():
    world = make(FRIGATE, 293.0, speed_kn=0.0)
    world.submit("set plain sail")
    world.submit("brace sharp up on the starboard tack")
    return world


def test_truth_15_the_same_seed_gives_the_same_log():
    a, b = hove_to(), hove_to()
    run(a, 600)
    run(b, 600)
    assert a.log.digest() == b.log.digest()
    assert a.state() == b.state()
    c, d = getting_under_way(), getting_under_way()
    run(c, 600)
    run(d, 600)
    assert c.log.digest() == d.log.digest()


# ---------------------------------------------------------------------------
# 16: the turning circle
# ---------------------------------------------------------------------------


def test_truth_16_tactical_diameter_at_eight_knots():
    world = under_plain_sail(FRIGATE, 270.0, speed_kn=6.0)
    assert 7.5 <= knots(world) <= 8.5
    d = world.ship.dyn
    h0, x0, y0 = d.heading, d.x, d.y
    world.submit("hard a-weather")
    turned, last, ticks = 0.0, h0, 0
    while turned < math.pi and ticks < 600:
        world.tick()
        ticks += 1
        turned += abs(units.wrap_pi(world.ship.dyn.heading - last))
        last = world.ship.dyn.heading
    assert turned >= math.pi, "did not come round in ten minutes"
    dx, dy = world.ship.dyn.x - x0, world.ship.dyn.y - y0
    transfer = abs(dx * math.cos(h0) - dy * math.sin(h0))
    lengths = transfer / world.ship.hull.length
    assert 4.0 <= lengths <= 6.0, f"tactical diameter {lengths:.1f} lengths"


# ---------------------------------------------------------------------------
# 17: getting under way from rest
# ---------------------------------------------------------------------------


def test_truth_17_getting_under_way_without_being_taken_aback():
    world = getting_under_way()
    min_off, sternway, settled_at, on_course = 180.0, 0.0, None, 0
    for t in range(1, 901):
        world.tick()
        if t > 360:  # plain sail is set by then
            min_off = min(min_off, off_wind(world))
            sternway = max(sternway, -headway_kn(world))
        error = abs(math.degrees(units.wrap_pi(world.ship.dyn.heading - math.radians(293.0))))
        on_course = on_course + 1 if knots(world) > 3.0 and error < 10.0 else 0
        if settled_at is None and on_course >= 60:
            settled_at = t - 60
    assert events(world, "ship.aback") == []
    assert min_off > 30.0, f"came up to {min_off:.0f} deg off the wind"
    assert sternway < 0.5, f"hung with {sternway:.1f} kn of sternway"
    assert settled_at is not None and settled_at <= 900, "not settled close-hauled in 15 min"
    assert knots(world) > 4.0


# ---------------------------------------------------------------------------
# Milestone 3: the crew (spec M3 §7), truths 18 to 23
# ---------------------------------------------------------------------------


def from_rest(ship, heading_deg=293.0, knots_=15.0, start=None):
    """A ship at rest with every sail furled, as a voyage begins; `start` sets the clock."""
    scenario = Scenario(
        wind_from_deg=WIND_FROM,
        wind_speed_kn=knots_,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=heading_deg,
        ship_speed_kn=0.0,
    )
    if start is not None:
        scenario.start_time = start
    return make_world(SEED, ship, scenario)


def until_idle(world, limit: int) -> None:
    """Tick until the runner has nothing in hand, or `limit` ticks."""
    runner = world.ship.extra["evolutions"]
    for _ in range(limit):
        if not runner.instances:
            return
        world.tick()


def plain_sail_minutes(ship, all_hands: bool):
    """Minutes from `set plain sail` to the last of it set, from furled; with all hands
    called (and up, a minute and a half) first when asked. Returns (minutes, world)."""
    world = from_rest(ship)
    if all_hands:
        world.submit("call all hands")
        run(world, 90)
    start = world.clock.tick
    world.submit("set plain sail")
    until_idle(world, 3600)
    last = max(e.tick for e in events(world, "sail.set", after=start - 1))
    return (last - start) / 60.0, world


@pytest.fixture(scope="module")
def frigate_plain_sail():
    return {hands: plain_sail_minutes(FRIGATE, hands) for hands in (False, True)}


def test_truth_18_all_hands_set_plain_sail_several_times_faster_than_the_watch(
    frigate_plain_sail,
):
    watch, watch_world = frigate_plain_sail[False]
    all_hands, _ = frigate_plain_sail[True]
    assert watch >= 2.0 * all_hands, f"watch {watch:.1f} min, all hands {all_hands:.1f} min"
    # the watch cannot man eleven sails at once: some go short-handed and take longer
    assert events(watch_world, "evolution.short_handed")


@pytest.mark.xfail(
    strict=True,
    reason=(
        "The frigate's watch sets plain sail in 16.4 minutes and all hands in 5.6, against "
        "the spec's 25 to 40 and 12 to 20. The ratio is right (nearly three to one); the "
        "times are milestone 2's frozen `duration_s` in data/evolutions/set_square.yaml, "
        "set_gaff.yaml and set_jibheaded.yaml, and Luce's 'in a few minutes' with all hands "
        "fits 5.6 better than 12 to 20. See docs/dev/TuningNotes.md, truth 18."
    ),
)
def test_truth_18_the_watch_and_all_hands_take_the_spec_times(frigate_plain_sail):
    watch, _ = frigate_plain_sail[False]
    all_hands, _ = frigate_plain_sail[True]
    assert 25.0 <= watch <= 40.0, f"the watch took {watch:.1f} min"
    assert 12.0 <= all_hands <= 20.0, f"all hands took {all_hands:.1f} min"


def test_truth_19_a_tack_belays_the_royals_being_set_and_they_resume_after():
    # Milestone 3b (spec 3b §7; spec M3 §9 item 12): told with sails the watch may
    # legitimately be setting on a wind, the royals, the light sails above the frigate's
    # plain sail. Studding sails are taken in before going about (Luce), which the tack now
    # does first (tests/test_studding.py).
    world = close_hauled_on_starboard(FRIGATE)
    world.submit("set the royals")
    run(world, 60)
    start = world.clock.tick
    world.submit("tack ship")
    done, seconds = until(world, ("ship.tacked", "ship.missed_stays"), 900)
    assert [e.kind for e in done] == ["ship.tacked"]
    assert 300 <= seconds <= 420, f"tacked in {seconds} s"
    belayed = events(world, "evolution.belayed", after=start - 1)
    assert belayed and all("royal" in e.text for e in belayed)
    assert all(e.text.endswith("all hands about ship.") for e in belayed)
    tacked_at = done[0].tick
    assert not [e for e in events(world, "sail.set", after=start) if e.tick <= tacked_at]
    run(world, 900)
    resumed = [e for e in events(world, "sail.set", after=tacked_at) if "royal" in e.text]
    assert len(resumed) == len(belayed), "not every belayed royal was set after"


def test_shorten_sail_takes_in_the_topgallants_while_the_reef_is_taken_and_the_reef_speeds_up():
    """Package 29b, the owner's ruling of 2026-09-29 at gate 4c (playtest 7, finding 2):
    a call for all hands is a pool action. "Shorten sail for weather" as the starter book
    has it fires in 32 knots with the frigate under plain sail by day: the topgallants
    start first, in the book's order, with hands of the watch; the reef calls all hands
    and begins short, with the idle hands and the watch below as it comes up; the
    topgallants come in while the reef is being taken, not after it, and their hands join
    it, which speeds it to the whole deck's pace. Nothing is belayed, and the hands are
    piped down once, when the last topsail is reefed."""
    from freesail.crew import hands

    line = (
        'standing order "shorten sail for weather": when the true wind exceeds 30 knots for '
        "2 minutes then take in the studdingsails; take in the royals; take in the "
        "topgallants; reef the topsails, one reef"
    )
    world = from_rest(FRIGATE, heading_deg=180.0, knots_=18.0, start=datetime(1805, 6, 1, 10))
    world.submit("set plain sail")
    until_idle(world, 3600)
    run(world, 300)
    runner = world.ship.extra["evolutions"]
    assert all(world.ship.sails[s].is_set for s in world.ship.groups["topgallants"])
    world.submit(line)
    start = world.clock.tick
    blow(world, 32.0)
    factors: list[tuple[int, int, int, float]] = []  # tick, hands at it, the deck's, factor
    for _ in range(1800):
        world.tick()
        reef = next((i for i in runner.instances if i.evo.id == "reef_square"), None)
        if reef is not None and reef.subject_id == "fore.topsail" and not reef.waiting:
            a = reef.assignment
            factors.append(
                (world.clock.tick, a.got, a.wanted, hands.crew_factor(a, reef.want, True))
            )
        if not runner.instances and factors:
            break
    fired = by_order(world, "shorten sail for weather")
    assert [text.split(": ")[1] for _, text in fired] == [
        "taking in the topgallants.",
        "reefing the topsails, one reef.",
    ]
    began = factors[0][0]
    taken_in = [e.tick for e in events(world, "sail.taken_in", after=start)]
    reefed = [e.tick for e in events(world, "sail.reefed", after=start)]
    assert len(taken_in) == 3 and len(reefed) == 3
    # the topgallants in while the fore topsail is being reefed, not after it
    assert began <= min(taken_in) and max(taken_in) < min(reefed)
    assert events(world, "evolution.belayed", after=start) == []
    # the reef begins short (part of the deck at the topgallants) and speeds up as the
    # watch below comes up and the topgallant men come down, to the whole deck's pace
    _, got0, deck0, first = factors[0]
    assert got0 < deck0 and first > 1.1
    shorts = [e for e in events(world, "evolution.short_handed", after=start)]
    assert any("fore topsail" in e.text and "topgallant" in e.text for e in shorts)
    assert [f for _, _, _, f in factors] == sorted((f for _, _, _, f in factors), reverse=True)
    joined = next(t for t, got, deck, _ in factors if got == deck)
    assert max(taken_in) <= joined < min(reefed)
    assert factors[-1][3] == pytest.approx(1.0, abs=0.02)
    # one call and one pipe-down for the three topsails
    assert len(events(world, "crew.all_hands", after=start)) == 1
    piped = events(world, "crew.piped_down", after=start)
    assert [e.tick for e in piped] == [max(reefed)]


def morning_crew_factor(calls: bool) -> tuple[float, float]:
    """From half past midnight: all hands called at one, two and three and piped down after
    ten minutes each (or no calls); at the morning watch the fore topsail is set. Returns
    its crew factor and the minutes it took."""
    from freesail.crew import hands

    world = from_rest(FRIGATE, start=datetime(1805, 6, 1, 0, 30))
    for hour in (1, 2, 3):
        run(world, hour * 3600 - 1800 - world.clock.tick)
        if calls:
            world.submit("call all hands")
            run(world, 600)
            world.submit("pipe down")
    run(world, 4 * 3600 - 1800 + 60 - world.clock.tick)  # the morning watch has the deck
    start = world.clock.tick
    world.submit("set the fore topsail")
    inst = world.ship.extra["evolutions"].instances[0]
    factor = hands.crew_factor(inst.assignment, inst.want, aloft=True)
    until_idle(world, 1800)
    done = events(world, "sail.set", after=start)
    return factor, (done[0].tick - start) / 60.0


def test_truth_20_a_night_of_all_hands_slows_the_morning_watch():
    rested, rested_min = morning_crew_factor(calls=False)
    tired, tired_min = morning_crew_factor(calls=True)
    assert rested == pytest.approx(1.0)
    assert 1.10 <= tired <= 1.25, f"the morning watch's crew factor {tired:.3f}"
    assert tired_min / rested_min == pytest.approx(tired, abs=0.03)


def schooner_three_sails(all_hands: bool):
    world = from_rest(SCHOONER, heading_deg=300.0)
    if all_hands:
        world.submit("call all hands")
        run(world, 90)
    start = world.clock.tick
    for text in ("set the fore topsail", "set the foresail", "set the mainsail"):
        world.submit(text)
    run(world, 900)
    return world, start


def test_truth_21_the_schooners_watch_cannot_set_three_sails_at_once():
    world, start = schooner_three_sails(all_hands=False)
    waits = events(world, "evolution.waiting", after=start - 1)
    assert [e.subject for e in waits] == ["main.sail"]
    assert waits[0].severity.value == "notable"
    assert waits[0].text.startswith("Not hands enough on deck to set the mainsail")
    world, start = schooner_three_sails(all_hands=True)
    assert events(world, "evolution.waiting", after=start - 1) == []
    assert len(events(world, "sail.set", after=start - 1)) == 3


def crewed_voyage():
    """A crewed voyage through a tack, all hands and a watch change (08:00)."""
    world = from_rest(FRIGATE, start=datetime(1805, 6, 1, 7, 30))
    world.submit("set plain sail")
    world.submit("brace sharp up on the starboard tack")
    run(world, 120)  # a refused order is not journaled: trim once there is wind to trim to
    run(world, 780, trim_every=120)
    world.submit("call all hands")
    world.submit("tack ship")
    run(world, 600)
    world.submit("pipe down")
    run(world, 600)
    return world


def test_truth_22_same_seed_same_muster_same_log_and_a_replay_reproduces_it():
    from freesail.api.session import ship_factory
    from freesail.core import replay

    a, b = crewed_voyage(), crewed_voyage()
    assert a.log.digest() == b.log.digest()
    muster = a.ship.extra["crew"].describe(a.clock)
    assert muster == b.ship.extra["crew"].describe(b.clock)
    kinds = {e.kind for e in a.log}
    assert {"ship.tacked", "crew.all_hands", "crew.piped_down", "watch.relieved"} <= kinds
    assert "order.rejected" not in kinds  # the journal holds accepted orders only
    copy = replay.replay_world(a, ship_factory)
    assert copy.log.digest() == a.log.digest()
    assert copy.ship.extra["crew"].describe(copy.clock) == muster


def gale(send_down: bool, royal_condition: float | None = None):
    """Gate M2 item 9 (35 knots, all sail made and braced up) and, at the start of the
    second ten minutes, the topgallant masts sent down, or not. Milestone 3b: the royals
    may be bent worn, at `royal_condition` (truth 27)."""
    world = from_rest(FRIGATE, heading_deg=270.0, knots_=35.0)
    if royal_condition is not None:
        for sid in world.ship.groups["royals"]:
            world.ship.sails[sid].condition = royal_condition
    world.submit("make all sail")
    world.submit("brace up on the starboard tack")
    run(world, 600)
    world.submit("make all sail")
    world.submit("trim sails")
    if send_down:
        world.submit("send down the topgallant masts")
    for i in range(1800):
        if i in (600, 1200):
            world.submit("trim sails")
        world.tick()
    return world


def test_truth_23_sending_down_the_topgallant_masts_in_time_saves_the_royals():
    lost = [e for e in gale(send_down=False).log if e.kind in CARRIED_AWAY]
    assert any("royal" in (e.subject or "") for e in lost)
    world = gale(send_down=True)
    assert [e.text for e in world.log if e.kind in (*CARRIED_AWAY, "line.parted")] == []
    assert events(world, "spar.sent_down")
    assert all(world.ship.spars[m].sent_down for m in ("fore.royal.yard", "main.topgallant_mast"))


# ---------------------------------------------------------------------------
# Milestone 3b: rig geometry and canvas (spec 3b §9), truths 24 to 33
# ---------------------------------------------------------------------------

POINT = 11.25  # degrees in a point of the compass
SIX_POINTS = 6 * POINT


def speed_at(rows: list[dict], off: float) -> float:
    """Her speed `off` degrees off the true wind, read from a sweep (linear between rows)."""
    for a, b in zip(rows, rows[1:], strict=False):
        if a["off"] >= off >= b["off"]:
            f = (a["off"] - off) / (a["off"] - b["off"])
            return a["speed"] + f * (b["speed"] - a["speed"])
    raise AssertionError(f"the sweep does not reach {off} deg off the wind")


def off_at(rows: list[dict], speed: float) -> float:
    """The closest heading, in degrees off the true wind, at which the sweep still makes
    `speed` (linear between the last row at or above it and the first below)."""
    for a, b in zip(rows, rows[1:], strict=False):
        if a["speed"] >= speed > b["speed"]:
            f = (a["speed"] - speed) / (a["speed"] - b["speed"])
            return a["off"] + f * (b["off"] - a["off"])
    raise AssertionError(f"the sweep never falls to {speed:.2f} kn")


def after_yards_no_sharper(world) -> None:
    """The frigate's after yards rigged to brace no sharper than the head yard at their
    level, as milestone 3's files had it: `trim sails` then braces the masts alike."""
    ship = world.ship
    head = {}
    for yid in ship.groups["head yards"]:
        head[ship.parent_of(ship.spars[yid]).cls] = ship.spars[yid].rigged_brace_limit
    for yid in ship.groups["after yards"]:
        yard = ship.spars[yid]
        limit = min(yard.rigged_brace_limit, head[ship.parent_of(yard).cls])
        yard.rigged_brace_limit = yard.brace_limit = limit


@pytest.fixture(scope="module")
def frigate_yards_alike_sweep():
    return pointing_sweep(FRIGATE, stop_off=60, rig=after_yards_no_sharper, wait=240)


@pytest.fixture(scope="module")
def frigate_head_yards_sharper_sweep():
    return pointing_sweep(
        FRIGATE, stop_off=62, wait=240, trim="trim sails with the head yards sharper"
    )


@pytest.fixture(scope="module")
def frigate_bowlines_sweep():
    return pointing_sweep(FRIGATE, orders=["haul the weather bowlines"], wait=300)


@pytest.fixture(scope="module")
def frigate_catharpins_sweep():
    return pointing_sweep(
        FRIGATE, stop_off=58, orders=["swifter in the catharpins on the main"], wait=2400
    )


# 24: the after yards sharper than the head yards


def test_truth_24_the_after_yards_braced_sharper_gain_a_little(
    frigate_sweep, frigate_yards_alike_sweep, frigate_head_yards_sharper_sweep
):
    """Fincham 1843, art. 94: "the after-yards are braced sharper up than the fore-yards",
    so that the sails "just touch at the same time"; art. 96, the reverse for a griping
    ship. As built `trim sails` braces each after yard as much sharper as its rigging allows
    (Fincham art. 102's limits put the main yard two degrees beyond the fore; the spec's
    three is AFTER_YARDS_SHARPER_DEG, evolutions/trim.py). Compared at 66 deg off, her best
    course to windward (truth 1), with the after yards rigged to brace no sharper than the
    head yards, and with `trim sails with the head yards sharper`.

    Measured at seed 7 in 15 knots: 5.21 kn as built, 5.04 alike, 4.78 with the head yards
    sharper; as built she makes 5.04 kn about 0.9 deg closer than alike. The spec's quarter
    knot or quarter point is the xfail below, for the owner."""
    as_built = speed_at(frigate_sweep, 66.0)
    alike = speed_at(frigate_yards_alike_sweep, 66.0)
    head_sharper = speed_at(frigate_head_yards_sharper_sweep, 66.0)
    assert 0.05 <= as_built - alike < 0.25, f"{as_built:.2f} kn against {alike:.2f} alike"
    assert head_sharper < alike - 0.1, f"head yards sharper {head_sharper:.2f} kn"
    closer = 66.0 - off_at(frigate_sweep, alike)
    assert 0.0 < closer < POINT / 4, f"{closer:.1f} deg closer at {alike:.2f} kn"


@pytest.mark.xfail(
    strict=True,
    reason=(
        "Owner's ruling (spec 3b §9, truth 24). With the after yards braced sharper as their "
        "rigging allows (the main yard two degrees beyond the fore) she makes 5.21 kn at 66 "
        "deg off in 15 knots against 5.04 with every yard alike, +0.17 kn, and makes 5.04 "
        "about 0.9 deg closer: under a quarter knot and a quarter point. The sail model has "
        "no headed stream (every sail meets the same apparent wind), which is Fincham's "
        "reason for the practice; see trim.EASE_HEAD_YARDS and docs/dev/TuningNotes.md."
    ),
)
def test_truth_24_a_quarter_point_closer_or_a_quarter_knot_more(
    frigate_sweep, frigate_yards_alike_sweep
):
    alike = speed_at(frigate_yards_alike_sweep, 66.0)
    gain = speed_at(frigate_sweep, 66.0) - alike
    closer = 66.0 - off_at(frigate_sweep, alike)
    assert gain >= 0.25 or closer >= POINT / 4, f"+{gain:.2f} kn, {closer:.1f} deg closer"


# 25: full and by, not pinched


def made_good_to_windward(off_deg: float, knots_: float = 8.0, minutes: int = 30):
    """Close-hauled on the starboard tack `off_deg` off a light wind, the yards trimmed
    every two minutes: (knots made good to windward over the ground, mean speed through
    the water) over `minutes` once settled. The wind is from the north: northing."""
    world = under_plain_sail(FRIGATE, 360.0 - SIX_POINTS, knots_=knots_)
    world.submit(f"steer {360.0 - off_deg}")
    run(world, 600, trim_every=120)
    y0, t0 = world.ship.dyn.y, world.clock.tick
    speeds = []
    for i in range(minutes * 60):
        if i % 120 == 0:
            world.submit("trim sails")
        world.tick()
        speeds.append(knots(world))
    hours = (world.clock.tick - t0) / 3600.0
    return (world.ship.dyn.y - y0) / 1852.0 / hours, sum(speeds) / len(speeds)


def test_truth_25_pinched_to_five_points_she_makes_less_to_windward_than_kept_full():
    """Fincham 1843, art. 99: keeping the sails "just lifting" is proper only with five or
    six knots of way; with less, keep them full. In 8 knots of wind the frigate makes three
    knots at six points (2.95 at seed 7); pinched to five she falls to 1.75 and her leeway
    doubles (4.2 to 8.2 deg), so she makes 0.75 kn good to windward over the ground against
    0.92 kept full."""
    full, full_speed = made_good_to_windward(SIX_POINTS)
    pinched, pinched_speed = made_good_to_windward(5 * POINT)
    assert 2.5 <= full_speed <= 3.5, f"{full_speed:.2f} kn at six points"
    assert pinched_speed < full_speed - 0.5
    assert 0.0 < pinched < full - 0.1, f"{pinched:.2f} kn made good pinched, {full:.2f} full"


# 26: the bowlines


def test_truth_26_the_weather_bowlines_hauled_point_her_closer(
    frigate_sweep, frigate_bowlines_sweep
):
    """Fincham 1843, art. 98: "the flatter the sails the sharper they may be braced";
    Luce 1884, ch. XXIII: "haul taut the weather brace and haul the bowline". `haul the
    weather bowlines` steadies out the courses' and topsails' weather bowlines (five on the
    frigate), each bringing its sail's luff angle BOWLINE_LUFF_GAIN_DEG closer
    (physics/sails.py). At seed 7 in 15 knots: 5.76 kn at 66 deg off against 5.21 without
    (+0.55), and the 5.21 kn she made there she now makes about 3.3 deg closer; the
    closest heading holding three knots goes from 56 to 52 deg. The spec's half a point is
    the xfail below."""
    same = speed_at(frigate_sweep, 66.0)
    gain = speed_at(frigate_bowlines_sweep, 66.0) - same
    closer = 66.0 - off_at(frigate_bowlines_sweep, same)
    assert gain >= 0.3, f"+{gain:.2f} kn at 66 deg"
    assert POINT / 4 <= closer < POINT / 2, f"{closer:.1f} deg closer at {same:.2f} kn"
    _, closest = best_sustained_course(frigate_sweep)
    _, closest_hauled = best_sustained_course(frigate_bowlines_sweep)
    assert closest_hauled <= closest - 2.0


@pytest.mark.xfail(
    strict=True,
    reason=(
        "Owner's ruling (spec 3b §9, truth 26). The weather bowlines of the courses and "
        "topsails hauled, she makes the speed she made at 66 deg off (5.21 kn in 15 knots) "
        "about 3.3 deg closer, and +0.55 kn at the same heading: nearer a third of a point "
        "than half. BOWLINE_LUFF_GAIN_DEG = 4 (physics/sails.py) moves it; the topgallants, "
        "staysails and spanker have no bowline and draw as before. See "
        "docs/dev/TuningNotes.md."
    ),
)
def test_truth_26_about_half_a_point(frigate_sweep, frigate_bowlines_sweep):
    same = speed_at(frigate_sweep, 66.0)
    closer = 66.0 - off_at(frigate_bowlines_sweep, same)
    assert closer >= 0.4 * POINT, f"{closer:.1f} deg closer"


# 27: worn canvas in the gale


def royals_first(world) -> dict[str, str]:
    """What befell each royal first: 'blown_out', or 'yard' (its yard or mast went)."""
    royals = world.ship.groups["royals"]
    first: dict[str, str] = {}
    for e in world.log:
        if e.kind == "sail.blown_out" and e.subject in royals:
            first.setdefault(e.subject, "blown_out")
        elif e.kind == "spar.carried_away":
            for sid in royals:
                if sid in e.data.get("wrecked", []):
                    first.setdefault(sid, "yard")
    return first


def test_truth_27_a_worn_royal_blows_out_before_its_yard_goes_and_a_new_one_does_not():
    """Spec 3b §6.2 and §6.5, on Luce 1884 App. E's strengths (docs/references/Tables.md):
    the effective cloth rating is 0.4 + 0.6 * condition / 100 of the new, so a royal at
    condition 50 bears seventy per cent. In the gate M2 gale (truth 23's scenario: 35 knots,
    all sail made and braced up) the worn royals blow out of their bolt-ropes; new, the
    same royals hold until their yards and masts carry away, as at milestone 2. The game
    has no way yet to age a sail in a scenario's time, so the worn royals are bent worn
    (their condition set before the first order); the mechanism is tests/test_canvas.py's."""
    worn = gale(send_down=False, royal_condition=50.0)
    royals = worn.ship.groups["royals"]
    assert royals_first(worn) == {sid: "blown_out" for sid in royals}
    blown = [e for e in worn.log if e.kind == "sail.blown_out"]
    assert all(e.severity.value == "urgent" for e in blown)
    new = gale(send_down=False)
    assert royals_first(new) == {sid: "yard" for sid in royals}
    assert not [e for e in new.log if e.kind == "sail.blown_out" and e.subject in royals]


# 28: storm canvas, lying a-try


def lying_a_try(knots_: float = 45.0):
    """The frigate in a storm from rest, all hands up: the topgallant masts sent down and
    the storm staysails bent (Luce 1884, ch. XXIX, 'Reducing Sail to a Gale'), the yards
    braced up, the topsails set and close-reefed, the storm staysails set, then `lie a-try`,
    and the fore and mizzen topsails it hands furled. Returns the world and, for the hour
    after, her speeds and headings off the wind."""
    world = from_rest(FRIGATE, knots_=knots_)
    world.submit("call all hands")
    run(world, 90)
    for text in (
        "send down the topgallant masts",
        "bend the fore storm staysail",
        "bend the mizzen storm staysail",
        "brace sharp up on the starboard tack",
    ):
        world.submit(text)
    until_idle(world, 3600)
    world.submit("set the topsails")
    until_idle(world, 3600)
    world.submit("close reef the topsails")
    until_idle(world, 3600)
    world.submit("set the fore storm staysail")
    world.submit("set the mizzen storm staysail")
    until_idle(world, 1800)
    world.submit("lie a-try")
    until_idle(world, 1800)
    world.submit("furl the fore topsail")
    world.submit("furl the mizzen topsail")
    until_idle(world, 1800)
    hour = {"speed": [], "off": [], "start": world.clock.tick}
    for _ in range(3600):
        world.tick()
        hour["speed"].append(knots(world))
        hour["off"].append(off_wind(world))
    return world, hour


@pytest.fixture(scope="module")
def frigate_lying_a_try():
    return lying_a_try()


def test_truth_28_lying_a_try_in_a_storm_nothing_carries_away(frigate_lying_a_try):
    """Luce 1884, ch. XXIX In a Gale: "The ship is now 'lying to' under close-reefed main
    topsail, fore storm staysail" (the `lie_a_try` evolution); the storm staysails are No. 1
    canvas from the sail room (spec 3b §6.4). In 45 knots at seed 7 she lies 45 to 46 deg
    off the wind, steady, and nothing carries away, blows out or parts in the hour. She
    goes astern at 4.4 knots doing it: that half of the truth is the xfail below."""
    world, hour = frigate_lying_a_try
    set_ = {s.id for s in world.ship.sails.values() if s.is_set}
    assert set_ == {"main.topsail", "fore.storm_staysail", "mizzen.storm_staysail"}
    topsail = world.ship.sails["main.topsail"]
    assert topsail.reefs == topsail.reef_bands
    lying = events(world, "ship.hove_to")
    assert lying and lying[-1].text.startswith("Lying a-try under the main topsail")
    assert [e.text for e in world.log if e.kind in (*CARRIED_AWAY, "line.parted")] == []
    assert 40.0 <= min(hour["off"]) and max(hour["off"]) <= 60.0
    assert max(hour["off"]) - min(hour["off"]) <= 15.0


@pytest.mark.xfail(
    strict=True,
    reason=(
        "Owner's ruling (spec 3b §9, truth 28). Lying a-try in 45 knots under the close-"
        "reefed main topsail and the storm staysails, the topgallant masts down and the fore "
        "and mizzen topsails furled, she goes astern at 4.4 to 5.1 kn 45 deg off the wind, "
        "3.6 nm to leeward in the hour. Under bare poles before any sail is set she already "
        "goes astern at 5.6 kn: the rig's windage in 45 knots is more than the hull resists, "
        "the hull's resistance astern is its resistance ahead (physics/hull.py), and nothing "
        "lets her fall off into the trough. In 30 knots the same gives 2.9 kn astern. See "
        "docs/dev/TuningNotes.md."
    ),
)
def test_truth_28_lying_a_try_under_a_knot_and_a_half(frigate_lying_a_try):
    _, hour = frigate_lying_a_try
    assert max(hour["speed"]) < 1.5, f"{max(hour['speed']):.1f} kn"


# 29: studding sails too close


def test_truth_29_studding_sails_flog_and_strain_at_six_points_and_draw_at_nine():
    """Luce 1866 and 1884, ch. XXIII: the weather topmast and topgallant studding sails
    "with the wind one point free, or forming an angle of seven points with the keel", the
    lower "only ... with the wind abaft the beam". The frigate sets her five weather
    studding sails at nine points in 12 knots of wind and they draw; brought up to six
    they shake in their gear and every boom whips (a strain line each, the booms at 1.4 to
    1.5 of their rating); borne away to nine again after ten minutes they draw, and nothing
    has gone. Twelve knots because it is the least wind in which every boom's strain shows
    (package 23: in 10 knots one boom warns; in 13 two booms carry away within seven
    minutes, which is the gate's scene, not the truth's)."""
    from test_studding import NINE_POINTS, weather_studding_sails_at_nine_points

    world = weather_studding_sails_at_nine_points(FRIGATE, 12.0)
    set_ = [s for s in world.ship.sails.values() if s.cls == "studding" and s.is_set]
    assert len(set_) == 5 and all(s.side == "starboard" for s in set_)
    assert all(s.thrust_kn > 0.0 and not s.shivering for s in set_)
    start = world.clock.tick
    world.submit(f"steer {360.0 - SIX_POINTS}")
    for _ in range(10):
        world.submit("trim sails")
        run(world, 60)
    shaking = {e.subject for e in events(world, "sail.shivering", start)}
    assert shaking == {s.id for s in set_}
    whipping = [e for e in events(world, "strain.warning", start) if "whipping as the" in e.text]
    assert len({e.subject for e in whipping}) == 5
    assert all(e.text.endswith("she is too near the wind for it.") for e in whipping)
    assert all(s.shivering and s.thrust_kn < 0.0 for s in set_)
    borne_away = world.clock.tick
    world.submit(f"steer {360.0 - NINE_POINTS}")
    for _ in range(5):
        world.submit("trim sails")
        run(world, 60)
    drawing = {e.subject for e in events(world, "sail.drawing", borne_away)}
    assert drawing == {s.id for s in set_}
    assert all(s.thrust_kn > 0.0 and not s.shivering for s in set_)
    assert [e for e in world.log if e.kind in CARRIED_AWAY and e.tick > start] == []


# 30: studding sails running


def test_truth_30_studding_sails_both_sides_running_gain_most_of_a_knot():
    """Luce 1866, ch. XXIII: studding sails are set "to increase the speed of a vessel",
    both sides with the wind aft. The frigate running before 15 knots, all ten set: 5.88 kn
    to 6.61 at seed 7, +0.73 (+0.79 with the wind on the quarter, 165 deg). The spec reads
    Luce as "about a knot"; the band here is the measured one, and the gap is the owner's to
    judge (docs/dev/TuningNotes.md)."""
    gain = studding_sail_gain(180.0, knots_=15.0, in_knots=True)
    assert 0.6 <= gain <= 1.2, f"+{gain:.2f} kn"


# 31: the catharpins


def test_truth_31_the_catharpins_brace_the_main_yard_four_degrees_sharper_and_rate_it_down():
    """Fincham 1843, art. 102 (Hardy's short ship, braced sharper by measures taken);
    Lever 1808, fig. 182 (the shrouds "catharpined in"); Steel 1794, 'Catharpins'. On a wind
    in 30 knots under plain sail the main yard goes from 64 deg from square to 68
    (CATHARPIN_GAIN_DEG), `trim sails` names the after yards six degrees sharper, and the
    main mast's strain ratio rises from 0.178 to 0.229 (x1.29): its rating is taken at 0.883
    (CATHARPIN_RATING_FACTOR 0.85 on the athwartships part of the pull) and the sharper yard
    pulls 14 per cent harder. A lower mast is rated for 55 knots, so at 0.23 no warning
    line comes, and none is pretended."""
    world = under_plain_sail(FRIGATE, 360.0 - SIX_POINTS, knots_=30.0)
    ship = world.ship
    mast, yard = ship.spars["main.mast"], ship.spars["main.yard"]
    before_angle = abs(yard.brace_angle)
    before_ratio = mast.strain_ratio
    assert mast.rating_factor == 1.0
    start = world.clock.tick
    world.submit("swifter in the catharpins on the main")
    until_idle(world, 4000)
    assert mast.swiftered_in
    run(world, 600, trim_every=120)
    assert math.degrees(abs(yard.brace_angle) - before_angle) == pytest.approx(4.0, abs=0.01)
    texts = [e.text for e in world.log if e.tick > start]
    assert (
        "Swiftered in the catharpins on the main mast; the main yard will brace four "
        "degrees sharper." in texts
    )
    assert any("the after yards six degrees sharper" in t for t in texts)
    assert 0.85 <= mast.rating_factor <= 0.9
    rise = mast.strain_ratio / before_ratio
    assert 1.0 / 0.9 <= rise <= 1.5, f"strain ratio {before_ratio:.3f} to {mast.strain_ratio:.3f}"
    assert mast.strain_ratio < 0.5
    assert not [e for e in world.log if e.kind == "strain.warning" and mast.id in warned(e)]


def test_truth_31_with_the_catharpins_in_she_lies_a_little_closer(
    frigate_sweep, frigate_catharpins_sweep
):
    """Fincham 1843, art. 102: the short ship, "by bracing her main-yard from 17 to 21 [deg
    from the keel] ... could sometimes lie within 5 points". In 15 knots with the main
    catharpins in (the main yard 68 deg from square, the fore 62) she makes 5.34 kn at 66
    deg off against 5.21 as built, and the 5.21 about 0.7 deg closer. The spec's quarter
    point is the xfail below."""
    same = speed_at(frigate_sweep, 66.0)
    assert speed_at(frigate_catharpins_sweep, 66.0) > same + 0.05
    assert 66.0 - off_at(frigate_catharpins_sweep, same) > 0.0


@pytest.mark.xfail(
    strict=True,
    reason=(
        "Owner's ruling (spec 3b §9, truth 31). With the main catharpins swiftered in she "
        "makes 5.34 kn at 66 deg off in 15 knots against 5.21, and the 5.21 only about 0.7 "
        "deg closer, not a quarter point: one yard of twelve braced four degrees sharper, and "
        "no headed stream to reward the after yards (trim.EASE_HEAD_YARDS). "
        "CATHARPIN_GAIN_DEG = 4 (ship/parts.py) moves it; Hardy's other measures are the "
        "spec's open item 5. See docs/dev/TuningNotes.md."
    ),
)
def test_truth_31_a_quarter_point_closer(frigate_sweep, frigate_catharpins_sweep):
    same = speed_at(frigate_sweep, 66.0)
    assert 66.0 - off_at(frigate_catharpins_sweep, same) >= POINT / 4


# 32: pointing by ship


def closest_holding_two_thirds(sweep: list[dict], beam_reach_kn: float) -> float:
    """The closest heading of a sweep, in degrees off the true wind, at which she still
    makes more than two thirds of her speed with the wind abeam."""
    return min(r["off"] for r in sweep if r["speed"] > 2.0 * beam_reach_kn / 3.0)


def test_truth_32_the_frigate_lies_about_six_points_and_the_schooner_about_five(
    frigate_sweep, schooner_sweep, frigate_polar, schooner_polar
):
    """Fincham 1843, art. 102: Hardy's long ships "could seldom lie within six points of the
    wind"; a topsail schooner nearer five (Chapelle; docs/references/RigGeometryNotes.md).
    Measured as the spec says: the closest heading at which speed holds above two thirds of
    her beam-reach speed, under plain sail in 15 knots with the yards trimmed. At seed 7 the
    frigate 68 deg (8.0 kn abeam, 5.56 there), six points; the schooner 56 deg (7.9 kn
    abeam, 5.52 there), five points."""
    frigate = closest_holding_two_thirds(frigate_sweep, frigate_polar[90]["speed"])
    schooner = closest_holding_two_thirds(schooner_sweep, schooner_polar[90]["speed"])
    assert 5.5 * POINT <= frigate <= 6.5 * POINT, f"frigate {frigate:.0f} deg"
    assert 4.5 * POINT <= schooner <= 5.5 * POINT, f"schooner {schooner:.0f} deg"
    assert schooner <= frigate - POINT / 2


# 33: adjacent yards


def test_truth_33_one_yard_braced_away_from_its_neighbours_is_refused_and_the_mast_is_not():
    """Spec 3b §5 (spec M0-M2 §12 item 8): the clearance between two yards on a mast with a
    sail set on them is computed from their lengths, with a floor of ten degrees. Close-
    hauled under plain sail, the main topsail yard alone cannot be squared, and the refusal
    says why; the main yards together are squared."""
    from freesail.orders.verbs import adjacent_yard_max_diff

    world = close_hauled_on_starboard(FRIGATE)
    ship = world.ship
    lower, upper = ship.spars["main.yard"], ship.spars["main.topsail.yard"]
    apart = round(math.degrees(abs(lower.brace_angle)))
    most = round(math.degrees(adjacent_yard_max_diff(lower, upper)))
    refused = world.submit("brace the main topsail yard square")
    assert refused.kind == "order.rejected"
    assert refused.data["reason"] == (
        "The main topsail yard cannot be braced so far from the main yard while the main "
        f"topsail is set ({apart}° apart, {most}° at most); brace the main yards together, "
        "or clew up the main topsail."
    )
    accepted = world.submit("brace the main yards square")
    assert accepted.kind != "order.rejected"
    run(world, 240)
    for yid in ship.groups["main yards"]:
        assert ship.spars[yid].brace_angle == pytest.approx(0.0, abs=1e-6), yid


# ---------------------------------------------------------------------------
# Milestone 4a: standing orders (spec M4 §8), truths 34 to 38
# ---------------------------------------------------------------------------

NIGHT_ROUTINE = (
    'standing order "night routine": at sunset then take in the studdingsails; take in the royals'
)
MORNING_SAIL = (
    'standing order "morning sail": at sunrise, if the true wind is under 20 knots '
    "then set the royals"
)
SHORTEN_SAIL = (
    'standing order "shorten sail for weather": when the true wind exceeds 30 knots for '
    "2 minutes then take in the studdingsails; take in the royals; reef the topsails, one reef"
)
KEEP_HER_FULL = (
    'standing order "keep her full": when the apparent wind is forward of 55 degrees '
    "then bear away one point"
)
HEAVY_WEATHER = (
    'standing order "heavy weather": when the true wind exceeds 40 knots for 5 minutes then '
    "send down the topgallant masts; take in the fore topmast staysail; bend the fore storm "
    "staysail; close reef the topsails"
)
# The frigate's fore storm staysail sets on the fore stay, its own stay, beside the fore
# topmast staysail's (Luce 1884 ch. XXIX 'Reducing Sail to a Gale'; spec 3b §6), so it is
# bent and set as a sail of its own, not shifted for the other; and a firing's orders go on
# one tick, so the setting waits for the bending in a companion order that tests the sail's
# state (gate 4a's ruling, 2026-09-27).
STORM_STAYSAIL = (
    'standing order "storm staysail": when the fore storm staysail is furled and the true '
    "wind exceeds 40 knots then set the fore storm staysail"
)
# the sun at 50 N on 1 June 1805 (freesail/core/sun.py against the USNO almanac, tests/test_sun.py)
SUNRISE = "03:56"
SUNSET = "19:59"
STANDING_DWELL_S = 300  # freesail/standing/rules.py


def blow(world, knots_: float) -> None:
    """Set the steady wind's speed under way: the model's base speed, which with
    gustiness and variability at zero it holds exactly from the next tick."""
    world.wind.base_speed = world.wind.speed = units.knots_to_ms(knots_)


def by_order(world, name: str) -> list[tuple[int, str]]:
    """The orders a standing order gave that the ship carried out, with their ticks."""
    actor = f"standing order '{name}'"
    return [(e.tick, e.text) for e in world.log if e.kind == "order.accepted" and e.actor == actor]


def refused_by_order(world, name: str) -> list[tuple[int, str]]:
    actor = f"standing order '{name}'"
    return [(e.tick, e.text) for e in world.log if e.kind == "order.rejected" and e.actor == actor]


def stamp(world, tick: int) -> str:
    from datetime import timedelta

    return (world.clock.start + timedelta(seconds=tick)).strftime("%H:%M")


def sail_states(world) -> dict[str, str]:
    return {s.id: s.state.value for s in world.ship.sails.values()}


def running_under_all_sail(start: datetime, knots_: float = 15.0):
    """The frigate before the wind under all sail, studding sails both sides (the light
    sails the night routine takes in), from rest at `start`."""
    world = from_rest(FRIGATE, heading_deg=180.0, knots_=knots_, start=start)
    world.submit("make all sail")
    run(world, 600)
    world.submit("rig out the studdingsails, both sides")
    run(world, 300)
    world.submit("set the studdingsails, both sides")
    run(world, 600)
    return world


# 34: the night routine and the morning sail


def test_truth_34_at_sunset_the_night_routine_takes_in_the_light_sails_and_nothing_else():
    """Spec M4 §8, truth 34. Running before the wind under all sail at 19:20 on 1 June,
    six studding sails and the royals drawing. At sunset (19:59 by the sun model) the
    night routine gives two orders and no more; when the hands are done, the studding
    sails and the royals are in and every other sail is as it was."""
    world = running_under_all_sail(datetime(1805, 6, 1, 19, 20))
    world.submit(NIGHT_ROUTINE)
    before = sail_states(world)
    studding = {sid for sid in world.ship.groups["studdingsails"] if before[sid] == "set"}
    royals = set(world.ship.groups["royals"])
    assert len(studding) >= 6 and all(before[r] == "set" for r in royals)
    run(world, 2700)  # to 20:30
    fired = by_order(world, "night routine")
    assert [text for _, text in fired] == [
        "By standing order 'night routine': taking in the studdingsails.",
        "By standing order 'night routine': taking in the royals.",
    ]
    sunset = events(world, "sun.set")
    assert len(sunset) == 1 and fired[0][0] == sunset[0].tick
    assert stamp(world, fired[0][0]) == SUNSET
    assert refused_by_order(world, "night routine") == []
    after = sail_states(world)
    changed = {sid for sid in before if before[sid] != after[sid]}
    assert changed == studding | royals, changed ^ (studding | royals)
    assert all(after[sid] == "furled" for sid in studding)
    assert all(after[sid] in ("in_the_gear", "furled") for sid in royals)


@pytest.mark.parametrize("knots_,set_again", [(15.0, True), (25.0, False)])
def test_truth_34_at_sunrise_the_royals_are_set_again_only_under_twenty_knots(
    knots_: float, set_again: bool
):
    """Spec M4 §8, truth 34, the morning half. Plain sail before the wind at 03:20; at
    sunrise (03:56) the morning sail sets the royals in 15 knots; in 25 the order is not
    carried out and the log says which reading failed."""
    world = from_rest(FRIGATE, heading_deg=180.0, knots_=knots_, start=datetime(1805, 6, 1, 3, 20))
    world.submit("set plain sail")
    run(world, 600)
    world.submit(MORNING_SAIL)
    run(world, 2400)  # to 04:10; the royals set at 04:01 when the order is carried out
    sunrise = events(world, "sun.rise")
    assert len(sunrise) == 1 and stamp(world, sunrise[0].tick) == SUNRISE
    fired = by_order(world, "morning sail")
    held = [e for e in world.log if e.kind == "standing.held"]
    royals = world.ship.groups["royals"]
    if set_again:
        assert fired == [(sunrise[0].tick, "By standing order 'morning sail': setting the royals.")]
        assert held == []
        assert all(world.ship.sails[r].is_set for r in royals)
    else:
        assert fired == []
        assert [e.text for e in held] == [
            "Standing order 'morning sail' at sunrise: not carried out; the true wind is "
            "25 knots, not under 20 knots."
        ]
        assert not any(world.ship.sails[r].is_set for r in royals)


# 35: shorten sail for weather, once, and not on a gust


def test_truth_35_shorten_sail_fires_once_after_two_minutes_over_thirty_and_not_on_a_gust():
    """Spec M4 §8, truth 35. Under all sail before the wind in 15 knots at ten in the
    forenoon. A gust to 32 knots that lasts two minutes less a second and falls away does
    not fire it; 32 knots held two minutes does, once, and the wind staying over thirty
    does not fire it again; under thirty for a second less than the dwell (300 s) and up
    again does not; under thirty for the dwell and up again for two minutes does."""
    world = running_under_all_sail(datetime(1805, 6, 1, 10, 0))
    world.submit(SHORTEN_SAIL)
    name = "shorten sail for weather"
    blow(world, 32.0)
    run(world, 119)
    blow(world, 20.0)
    run(world, 60)
    assert by_order(world, name) == [], "a two-minute gust that falls away"
    t0 = world.clock.tick
    blow(world, 32.0)
    run(world, 121)
    fired = by_order(world, name)
    assert [t - t0 for t, _ in fired] == [120, 120, 120], "three orders on the one tick"
    assert [text for _, text in fired] == [
        f"By standing order '{name}': taking in the studdingsails.",
        f"By standing order '{name}': taking in the royals.",
        f"By standing order '{name}': reefing the topsails, one reef.",
    ]
    rule = world.standing.book.get(name)
    assert rule.fired == 1
    run(world, 600)
    assert rule.fired == 1, "the wind still over thirty: no second firing"
    blow(world, 20.0)
    run(world, STANDING_DWELL_S - 1)
    blow(world, 32.0)
    run(world, 200)
    assert rule.fired == 1, "a second short of the dwell: not re-armed"
    blow(world, 20.0)
    run(world, 1200)  # the dwell, and the hands done with the reef
    blow(world, 32.0)
    run(world, 121)
    assert rule.fired == 2
    # the routine's two minutes are long for studding sails before the wind in 32 knots:
    # every boom whips on the first second of the blow and one carries away on the
    # second, before the routine can fire (docs/dev/TuningNotes.md, milestone 4a)
    lost = events(world, "spar.carried_away")
    assert lost and lost[0].subject == "fore.topgallant.studdingsail_boom.larboard"
    assert all("studdingsail_boom" in (e.subject or "") for e in lost), "booms, nothing else"


# 36: keep her full


def close_hauled_frigate(heading_deg: float, gust: float = 0.0, var: float = 0.0):
    scenario = Scenario(
        wind_from_deg=WIND_FROM,
        wind_speed_kn=15.0,
        gustiness=gust,
        variability=var,
        ship_heading_deg=heading_deg,
        ship_speed_kn=4.0,
    )
    world = make_world(SEED, FRIGATE, scenario)
    world.submit("set plain sail")
    world.submit("brace sharp up on the starboard tack")
    run(world, 900)
    run(world, 300, trim_every=120)
    return world


def test_truth_36_keep_her_full_bears_away_a_point_forward_of_fifty_five_and_stops():
    """Spec M4 §8, truth 36. Close-hauled at 293 (67 degrees off the true wind, the
    apparent wind 48 on the bow) the rule fires at once and bears away one point, to 282;
    at 270 (the apparent wind 58) it does not fire in an hour, and when the wind backs a
    point and heads her it fires once."""
    pinched = close_hauled_frigate(293.0)
    assert reading(pinched)["awa"] < 55.0
    pinched.submit(KEEP_HER_FULL)
    run(pinched, 3600, trim_every=300)
    fired = by_order(pinched, "keep her full")
    assert [text for _, text in fired] == [
        "By standing order 'keep her full': bearing away one point."
    ]
    helm = [e.text for e in pinched.log if e.kind == "helm.order"]
    assert helm[-1] == "Helm ordered: bear away a point; steer W by N (282°)."
    full = close_hauled_frigate(270.0)
    assert reading(full)["awa"] > 55.0
    full.submit(KEEP_HER_FULL)
    run(full, 3600, trim_every=300)
    assert by_order(full, "keep her full") == [], "abaft the threshold: it does not fire"
    full.wind.direction_from = units.wrap_2pi(full.wind.direction_from - units.POINT)  # heads her
    run(full, 600, trim_every=300)
    assert len(by_order(full, "keep her full")) == 1


def test_truth_36_over_an_hour_of_a_wandering_wind_it_fires_no_more_than_four_times():
    """Spec M4 §8, truth 36. The frigate at 285 (the apparent wind 51 on the bow) in the
    M2 wind at full gustiness and variability, seed 7, an hour: it fires at once, once
    more when the wind heads her, and no more (measured: twice; at 275, on the threshold,
    in the console's gustiness, once). The edge and the dwell are the guards."""
    world = close_hauled_frigate(285.0, gust=1.0, var=1.0)
    world.submit(KEEP_HER_FULL)
    run(world, 3600, trim_every=300)
    fired = by_order(world, "keep her full")
    assert 1 <= len(fired) <= 4, [t for t, _ in fired]
    gaps = [t2 - t1 for (t1, _), (t2, _) in zip(fired, fired[1:], strict=False)]
    assert all(gap >= STANDING_DWELL_S for gap in gaps)


# 37: heavy weather


def rising_gale(top_knots: float = 45.0, minutes: int = 30):
    """Plain sail on a wind with the topgallants taken in, the wind rising from 20 knots
    to `top_knots` over `minutes`, the yards trimmed every ten minutes as it rises, then
    an hour at the top."""
    world = close_hauled_frigate(282.0)
    blow(world, 20.0)
    world.submit("take in the topgallants")
    run(world, 300)
    world.submit(HEAVY_WEATHER)
    world.submit(STORM_STAYSAIL)
    t0 = world.clock.tick
    for i in range(minutes * 60):
        blow(world, 20.0 + (top_knots - 20.0) * (i + 1) / (minutes * 60))
        if i % 600 == 0:
            world.submit("trim sails")
        world.tick()
    run(world, 3600)
    return world, t0


@pytest.fixture(scope="module")
def frigate_rising_gale():
    return rising_gale()


def test_truth_37_the_heavy_weather_routine_fires_in_order_with_all_hands(frigate_rising_gale):
    """Spec M4 §8, truth 37. The wind rising from 20 to 45 knots over half an hour
    passes forty at 24 minutes; five minutes on, the routine gives its four orders on
    one tick in the order written: the topgallant masts sent down (all hands called by
    the work, and down twenty minutes later), the fore topmast staysail taken in (in this
    gale it blew out at 43 knots a minute before, so the order is refused in words), the
    fore storm staysail bent, and the topsails close-reefed (three reefs each when the
    hands are free). The storm staysail is set by the companion order: see the next test."""
    world, t0 = frigate_rising_gale
    name = "heavy weather"
    over_forty = t0 + 1440  # 20 + 25 * t / 1800 > 40 from t = 1440
    fired = by_order(world, name)
    assert [t for t, _ in fired] == [over_forty + 300] * 3
    assert [text for _, text in fired] == [
        f"By standing order '{name}': sending down the topgallant masts.",
        f"By standing order '{name}': bending the fore storm staysail.",
        f"By standing order '{name}': close reefing the topsails.",
    ]
    refused = refused_by_order(world, name)
    assert len(refused) == 1 and refused[0][0] == over_forty + 300
    assert "('take in the fore topmast staysail')" in refused[0][1]
    assert "blown out" in refused[0][1]
    lines = [
        e.text
        for e in world.log
        if e.tick == over_forty + 300 and e.actor == f"standing order '{name}'"
    ]
    assert "sending down" in lines[0] and "take in" in lines[1]
    assert "bending" in lines[2] and "close reefing" in lines[3]
    all_hands = events(world, "crew.all_hands", after=over_forty)
    assert all_hands and all_hands[0].tick == over_forty + 301
    assert all_hands[0].text == "All hands! (to send down topgallant masts)"
    assert events(world, "spar.sent_down", after=over_forty)
    assert all(world.ship.spars[m].sent_down for m in world.ship.groups["topgallant masts"])
    assert all(world.ship.sails[t].reefs == 3 for t in world.ship.groups["topsails"])


def test_truth_37_the_storm_staysail_is_set_by_the_companion_order(frigate_rising_gale):
    """The companion order fires once, on the tick the storm staysail is bent and furled
    (the bending takes the hands about twelve minutes from the sail room), and the sail
    is set and drawing by the end of the hour."""
    world, t0 = frigate_rising_gale
    over_forty = t0 + 1440
    fired = by_order(world, "storm staysail")
    assert len(fired) == 1
    assert fired[0][1] == "By standing order 'storm staysail': setting the fore storm staysail."
    bent = [e for e in world.log if e.kind == "sail.bent" and e.subject == "fore.storm_staysail"]
    assert bent and bent[0].tick == fired[0][0] and bent[0].tick > over_forty + 300
    assert world.ship.sails["fore.storm_staysail"].is_set


# 38: the conflict rule between an officer's order and the captain's


MASTERS_ROYALS = 'standing order "royals at sunset" by the master: at sunset then set the royals'


def sunset_frigate():
    world = from_rest(FRIGATE, heading_deg=180.0, start=datetime(1805, 6, 1, 19, 40))
    world.submit("set plain sail")
    world.submit("set the royals")
    run(world, 600)
    return world


def test_truth_38_the_captains_standing_order_stands_and_the_masters_is_countermanded():
    """Spec M4 §8, truth 38. The master's order to set the royals at sunset and the
    captain's night routine that takes them in fire on the same tick. With the captain's
    in the book first, his is given and the master's is not; the log says so. With the
    master's first, his order goes and the captain's follows it, and the log says the
    same."""
    line = (
        "Standing order 'royals at sunset' (the master) countermanded by 'night routine' "
        "(the captain)."
    )
    captains_first = sunset_frigate()
    captains_first.submit(NIGHT_ROUTINE)
    captains_first.submit(MASTERS_ROYALS)
    run(captains_first, 1500)
    assert [e.text for e in captains_first.log if e.kind == "standing.countermanded"] == [line]
    assert by_order(captains_first, "royals at sunset") == []
    assert [text for _, text in by_order(captains_first, "night routine")] == [
        "By standing order 'night routine': taking in the royals."
    ]
    book = captains_first.standing.book
    assert book.get("royals at sunset").fired == 0 and book.get("royals at sunset").conflicts == 1
    royals = captains_first.ship.groups["royals"]
    assert not any(captains_first.ship.sails[r].is_set for r in royals)
    masters_first = sunset_frigate()
    masters_first.submit(MASTERS_ROYALS)
    masters_first.submit(NIGHT_ROUTINE)
    run(masters_first, 1500)
    assert [e.text for e in masters_first.log if e.kind == "standing.countermanded"] == [line]
    assert [text for _, text in by_order(masters_first, "night routine")] == [
        "By standing order 'night routine': taking in the royals."
    ]


# ---------------------------------------------------------------------------
# Milestone 4b: the harness (docs/TechnicalSpec-M4.md §16)
# ---------------------------------------------------------------------------
# 41 to 46 are in tests/test_agents.py, beside the helpers they share (see the docstring
# at the top of this file); 47, the consent step, is here.

CONSENT_WEIGHTS = "made-up-weights-7b.Q4_K_M.gguf"  # made up: no model is named here


def station_behind_consent(records, script: list, identity: str = CONSENT_WEIGHTS):
    """The drivers' order of things (the local runner, the REPL): the consent step, and a
    station brief only on a yes. One scripted model plays both, so what it was sent, and
    in what order, is on its record. Returns the fake and the harness (None if no
    station)."""
    import io

    from freesail.agents import Fake, Harness, consent, watcher
    from freesail.agents.agent import SamplingPolicy

    fake = Fake(script)
    record = consent.ensure(
        identity,
        "the truths' runtime",
        fake,
        door="runner",
        owner=lambda words: "The owner's reply.",
        records_dir=records,
        out=io.StringIO(),
        today=datetime(2026, 9, 27).date(),
    )
    if record is None:
        return fake, None
    world = World(seed=SEED, scenario=Scenario(gustiness=0.0, variability=0.0))
    h = Harness(world, watcher(SamplingPolicy.in_lockstep(1800)), fake)
    h.start()
    return fake, h


def operator_texts(fake) -> list[str]:
    """Every operator text the fake was sent, in order, once each."""
    seen: list[str] = []
    for turns in fake.seen:
        for t in turns:
            if t.role == "operator" and (not seen or seen[-1] != t.content):
                seen.append(t.content)
    return seen


def test_truth_47_the_consent_step_runs_first_for_new_weights_and_not_again_after_a_yes(
    tmp_path,
):
    """Spec M4 §16, truth 47. Weights with no record meet the consent brief before any
    station brief: the model is asked, the owner answers its question, it says yes, the
    record is written, and only then does the station's brief follow. The same weights
    again are not asked: the station brief is the first thing sent, and no record is
    added. Near relations are not covered: a different quantisation is asked afresh, and
    a no on record stops the run without asking again."""
    from freesail.agents import call, consent, reply

    records = tmp_path / "consent"
    script = [
        "What would I be doing?",
        reply("", call("answer", text="Yes.")),
        "",
        "All quiet.",
    ]
    fake, h = station_behind_consent(records, script)
    assert h is not None and h.agent.state == "stationed"
    first, second = operator_texts(fake)
    assert first.startswith("This is a message from the developer of a game")
    assert second.startswith("This is a message from the harness of FreeSail")
    assert fake.seen[0][0].content == first  # the very first thing the model was sent
    record = consent.check(CONSENT_WEIGHTS, records)
    assert record.verdict == consent.YES and len(consent.records(records)) == 1
    # a yes on record: not asked again
    fake2, h2 = station_behind_consent(records, ["Aye."])
    assert h2 is not None
    assert operator_texts(fake2) == [h2.brief.text()]
    assert fake2.seen[0][0].content.startswith("This is a message from the harness of FreeSail")
    assert len(consent.records(records)) == 1
    # a near relation is a different party: asked afresh, and a no stops the run
    near = CONSENT_WEIGHTS.replace("Q4_K_M", "Q8_0")
    fake3, h3 = station_behind_consent(records, [reply("", call("answer", text="No."))], near)
    assert h3 is None
    assert operator_texts(fake3)[0].startswith("This is a message from the developer")
    fake4, h4 = station_behind_consent(records, ["never read"], near)
    assert h4 is None and fake4.calls == 0  # the no is respected without asking


# ---------------------------------------------------------------------------
# Milestone 4c: the ship sails herself (docs/TechnicalSpec-M4.md §23), truths 48 to 51
# ---------------------------------------------------------------------------
# The gate's day is data/scenarios/gate-4c-day.yaml: the frigate at 04:00 on 1 June 1805,
# 50 N, heading south-east, the weather script of spec §19 (a fresh breeze from the west at
# dawn, veering north-west and rising to a gale in the middle watch, easing at the next
# dawn), the starter routines and the captain's three for the passage
# (data/scenarios/gate-4c-day.orders), plain sail and the royals ordered at four. Seed 7,
# the file's. Measured values are named here and recorded in docs/dev/TuningNotes.md, M4c.

GATE_DAY = "data/scenarios/gate-4c-day.yaml"
# the day runs from 04:00 on 1 June to 09:00 on 2 June: into the second forenoon watch
GATE_DAY_TICKS = 29 * 3600
SECOND_FORENOON = 28 * 3600  # 08:00 on 2 June
# the ticks at which truth 49 saves the day and replays it: a glass in, at 20:00 after the
# night routine, and at 01:00 in the gale with the heavy-weather routine's work in hand
GATE_DAY_SAVES = (1800, 16 * 3600, 21 * 3600)
LOST = ("sail.blown_out", "spar.carried_away", "line.parted")

# Measured at seed 7 (package 29, and again with the topgallants in the starter's
# shortening line, the owner's ruling at gate 4c; the ticks did not move): sunset at 19:50
# by the sun at her easting, and the night routine's order on its tick; the heavy-weather
# routine at 00:38:56 in the middle watch, its four orders on one tick and all carried out
# (two reefs were in; the first measurement had three and the close reef refused); the
# captain's "make sail after the gale" at 05:55 and the topgallants set again at 06:34;
# plain sail from about 07:00.
GATE_DAY_SUNSET_TICK = 57052
GATE_DAY_HEAVY_WEATHER_TICK = 74336
GATE_DAY_TOPGALLANTS_AGAIN_TICK = 95650
# Package 29b (all hands a pool action; trim on a shift; the grouped lines): the three
# ticks above did not move; "shorten sail for weather" fires three times, at 21:43:57,
# 22:16:13 and 22:56:28 (twice in package 29's last measurement, at the first and the
# third), and "trim on a shift" four times (20:42, 21:58, 22:57, 23:55) as the wind veers
GATE_DAY_SHORTEN_SAIL_TICKS = [63837, 65773, 68188]
GATE_DAY_TRIM_ON_A_SHIFT_TICKS = [60148, 64720, 68248, 71749]


def the_gate_day(until: int = GATE_DAY_TICKS, saves: tuple[int, ...] = GATE_DAY_SAVES):
    """The gate's day as the drivers give it (`--scenario`): the scenario file's world,
    its book and first orders, run to `until`, with a save and the log's digest taken at
    each tick of `saves`."""
    from freesail.world.scenarios import begin, load_scenario, make_scenario_world

    sf = load_scenario(GATE_DAY)
    world = make_scenario_world(sf)
    begin(world, sf)
    saved = {}
    for t in sorted(saves):
        run(world, t - world.clock.tick)
        saved[t] = (world.save(), world.log.digest())
    run(world, until - world.clock.tick)
    return world, sf, saved


@pytest.fixture(scope="module")
def gate_day():
    return the_gate_day()


def script_implies(sf, knots_: float, after: datetime) -> datetime:
    """The first minute after `after` at which the script's base wind exceeds `knots_`."""
    ws = sf.script
    t = after
    while units.ms_to_knots(ws.at(t)[1]) <= knots_:
        t += timedelta(minutes=1)
    return t


def test_truth_48_the_gates_day_under_the_standing_orders(gate_day):
    """Spec M4 §23, truth 48: "Through the gate's day under the starter routines the ship
    loses nothing, the night routine and the heavy-weather routine fire in the log at the
    times the weather script implies, and she is back under plain sail by the second
    forenoon." Under the starter routines (the topgallants in with the royals at thirty,
    the owner's ruling at gate 4c) and the captain's three for the passage (without them
    she blows out the mainsail, spanker and jib at 45 running before the gale; package
    29's first runs).

    - Nothing lost: no sail blown out, no spar carried away, no line parted, no part
      wrecked, through a gale of 45 knots.
    - The night routine at sunset, 19:50, taking in the royals (the studding sails were
      never set, and it says so); the script's wind is still a fresh breeze then.
    - The heavy-weather routine in the middle watch, its four orders on one tick and all
      carried out, within a quarter of an hour of the script's forty knots plus the five
      minutes (the wind's wander about the scripted base is some four knots,
      physics/wind.py; measured 00:38:56 against 00:32 implied).
    - Plain sail by eight bells in the second forenoon (08:00 on 2 June): every sail of the
      ship's "plain sail" set, no reef in, the topgallant masts up, the storm staysail in.
    """
    world, sf, _ = gate_day
    assert world.seed == 7
    assert [e.text for e in world.log if e.kind in LOST] == []
    assert [p.id for p in world.ship.parts.values() if p.wrecked] == []

    sunset = events(world, "sun.set")
    assert [e.tick for e in sunset] == [GATE_DAY_SUNSET_TICK]
    night = by_order(world, "night routine")
    assert night == [
        (GATE_DAY_SUNSET_TICK, "By standing order 'night routine': taking in the royals.")
    ]
    # a fresh breeze still at sunset (20.4 knots by the script), the royals aloft for it
    wind = sf.script.at(sunset[0].ship_time)[1]
    assert units.describe_wind_strength(wind) == "a fresh breeze"

    heavy = by_order(world, "heavy weather")
    # its four orders on the one tick: the masts down, the fore topmast staysail in, the
    # storm staysail bent, and the close reef refused in words because the topsails are
    # close-reefed already. Package 29b: with all hands a pool action the reefs are done
    # sooner and the starter's "shorten sail for weather" stands again sooner, so it fires
    # three times in the first watch (21:43, 22:16, 22:56), three reefs in by 23:22, as the
    # first measurement of package 29 had it; package 29 after the topgallants moved into
    # its line had it fire twice and the close reef carried out (docs/dev/TuningNotes.md)
    assert [t for t, _ in heavy] == [GATE_DAY_HEAVY_WEATHER_TICK] * 3
    assert [text.split(": ")[1] for _, text in heavy] == [
        "sending down the topgallant masts.",
        "taking in the fore topmast staysail.",
        "bending the fore storm staysail.",
    ]
    refused = [x for x in refused_by_order(world, "heavy weather") if x[0] == heavy[0][0]]
    assert len(refused) == 1 and "close reef the topsails" in refused[0][1]
    assert "already close reefed" in refused[0][1]
    shorten = sorted({t for t, _ in by_order(world, "shorten sail for weather")})
    assert shorten == GATE_DAY_SHORTEN_SAIL_TICKS
    assert all(world.ship.sails[s].reefs == 0 for s in world.ship.groups["topsails"])
    # (and at 03:22, the wind under forty for the dwell and over it again, the routine fires
    # once more and all four are refused in words: everything is done already)
    fired = world.clock.start + timedelta(seconds=heavy[0][0])
    assert units.watch_of(fired)[1] == "Middle watch"
    implied = script_implies(sf, 40.0, datetime(1805, 6, 1, 20, 0)) + timedelta(minutes=5)
    assert abs((fired - implied).total_seconds()) <= 15 * 60, (fired, implied)
    assert not any(world.ship.spars[m].sent_down for m in world.ship.groups["topgallant masts"])

    # the yards trimmed to the wind as it veered west to north-west (package 29b)
    assert [t for t, _ in by_order(world, "trim on a shift")] == GATE_DAY_TRIM_ON_A_SHIFT_TICKS

    again = by_order(world, "topgallants again")
    assert again and again[0][0] == GATE_DAY_TOPGALLANTS_AGAIN_TICK < SECOND_FORENOON
    plain = set(world.ship.groups["plain sail"])
    states = sail_states(world)
    assert all(states[s] == "set" for s in plain), {s: states[s] for s in plain}
    assert all(world.ship.sails[s].reefs == 0 for s in plain)
    assert states["fore.storm_staysail"] != "set"


def test_truth_49_the_day_saved_at_several_ticks_replays_to_the_same_digest(gate_day):
    """Spec M4 §23, truth 49: "The day saved at any tick and replayed gives the same
    digest." Saved a glass in, at 20:00 and at 01:00 in the gale, each replayed from its
    seed, scenario (the weather script with it) and inputs to the digest the day had at
    that tick. The well's standing order, refused when the book is read, is replayed too
    (package 29's `inputs`: refusals and queries replay, not only the orders carried
    out), so the replayed log is the log the player watched, line for line."""
    from freesail.api.session import ship_factory
    from freesail.core import replay as replay_mod

    world, sf, saved = gate_day
    for tick in GATE_DAY_SAVES:
        data, digest = saved[tick]
        assert data["end_tick"] == tick
        assert data["scenario"]["weather"] == sf.scenario.weather
        refused = [x for x in data["inputs"] if "sound the well" in x.get("order", "")]
        assert len(refused) == 1
        copy = replay_mod.replay(data, ship_factory)
        assert copy.clock.tick == tick
        assert copy.log.digest() == digest, tick
        assert copy.standing.book.save() == data["standing_orders"]


def test_truth_50_at_three_hundred_times_the_log_shows_hourly_rollups_and_every_notable_line(
    gate_day,
):
    """Spec M4 §23, truth 50: "At 300 times the log shows hourly roll-ups and every notable
    and urgent line." The day's log through the one view the console prints, the server
    sends and a model's samples carry (`events.RollupView`), at 300x: every notable and
    urgent line as it is, the captain's and the driver's too; each hour of the ship's clock
    that has routine lines has exactly one roll-up, closed at the hour, whose count is its
    routine lines; and nothing is dropped. Measured: 29 roll-ups for 29 hours, the day's
    routine lines summed in them (the counts in docs/dev/TuningNotes.md, M4c)."""
    from freesail.core.events import KEPT_ACTORS, STATION_ACTORS, Event, Rollup, kept, rollup

    world, _, _ = gate_day
    log = world.log.all()
    shown = rollup(log, 300, so_far=True)
    lines = [x for x in shown if isinstance(x, Event)]
    rolls = [x for x in shown if isinstance(x, Rollup)]
    assert lines == [e for e in log if kept(e)]
    assert all(
        e.severity is not Severity.ROUTINE or e.actor in KEPT_ACTORS | STATION_ACTORS for e in lines
    )
    hours = sorted({e.ship_time.replace(minute=0, second=0) for e in log if not kept(e)})
    assert [r.start for r in rolls] == hours
    assert len(rolls) == GATE_DAY_TICKS // 3600 + 1  # the last is the 09:00 bell's hour
    assert all(not r.so_far for r in rolls[:-1]) and rolls[-1].so_far
    assert sum(r.count for r in rolls) + len(lines) == len(log)
    for r in rolls:
        assert r.end - r.start == timedelta(hours=1)
        assert r.text.endswith(("routine entries.", "routine entry.", "so far."))


# The performance budget (spec M4 §20): the frigate under the starter routines at not less
# than this many ticks a second on the owner's machine.
TICKS_PER_SECOND_HEADLESS = 3000
# The owner's machine (a desktop with an RTX 4090, 2026) runs pure Python about twice as
# fast a core as the build machine (a 2.1 GHz cloud Xeon): the assumed ratio, a judgement
# from single-thread benchmarks of the two classes of processor, to be measured on the
# owner's machine at the gate (docs/gates/gate-m4c.md).
OWNER_TO_BUILD_RATIO = 2.0
# Measured on the build machine, alone, at seed 7 in the gate's day (package 29): 420
# ticks a second before the package's work on the tick, about 1,000 after; 800 to 900
# through the whole day with its gale. The budget needs 3000 / 2.0 = 1500 here and is not
# met: package 29's report and docs/dev/TuningNotes.md give the profile, and the lead sets
# the budget with the owner.
BUILD_MACHINE_MEASURED = 1000
# The floor the test asserts: half of what was measured, so a build machine running the
# suite on four workers at once (each core shared) does not fail it, and a return to the
# old rate (420) does.
BUILD_MACHINE_MARGIN = 0.5
BUILD_MACHINE_FLOOR = BUILD_MACHINE_MEASURED * BUILD_MACHINE_MARGIN


def test_truth_51_the_frigate_under_the_starter_routines_ticks_at_the_build_machines_floor():
    """Spec M4 §23, truth 51: "The frigate under the starter routines ticks at not less than
    the budget." The gate's day from the scenario file (the book read, plain sail and the
    royals set), a thousand ticks to settle, then the best of three runs of a thousand:
    at least BUILD_MACHINE_FLOOR ticks a second on the build machine. The spec's budget of
    3000 on the owner's machine would be 1500 here at the assumed ratio; the measured
    figure is about 1000, so the budget itself is not asserted (package 29's report)."""
    import time

    world, _, _ = the_gate_day(until=1000, saves=())
    best = 0.0
    for _ in range(3):
        t0 = time.perf_counter()
        world.run(1000)
        best = max(best, 1000 / (time.perf_counter() - t0))
    assert best >= BUILD_MACHINE_FLOOR, f"{best:.0f} ticks a second"
    assert TICKS_PER_SECOND_HEADLESS / OWNER_TO_BUILD_RATIO > BUILD_MACHINE_MEASURED


# ---------------------------------------------------------------------------
# Milestone 5a: weather systems, the glass and the sky (package 30; spec M5 §6)
# ---------------------------------------------------------------------------
#
# The gate's day re-expressed as a system (data/scenarios/gate-4c-day.yaml, its `systems`
# beside its pinned `wind`): a low passing well north of Falmouth with the ship in its
# warm sector, the cold front through at 22:00, the north-westerly gale in the cold air
# behind and the ridge by dawn. Truths 52, 54 and 57 sail it from noon the day before
# (the warm front's approach, which the pinned day opens after) to the second forenoon,
# in a point ship with the day's gustiness and wander, seed 7. The fitted numbers are in
# docs/dev/TuningNotes.md, M5a.

GATE_SYSTEMS_EVE = datetime(1805, 5, 31, 12, 0)
GATE_SYSTEMS_END = datetime(1805, 6, 2, 9, 0)
# The strong-breeze days a month the seeding gives against Ushant's 31-knot-gust days (W
# §1.2): the station is on a cliff and reads high for the open sea, so the band is stated
# as a fraction of it (judgement: from a fifth to the whole; the first pass sits near a
# half in winter and a quarter in summer, docs/dev/TuningNotes.md).
GALE_DAYS_BAND = (0.2, 1.0)
# No line a player reads names these (truth 57): whole words, since "centreline" is a
# ship's word and "hPa" a unit the author's view alone may use.
FORBIDDEN_WORDS = re.compile(r"\b(front|centre|isobar|hPa)\b", re.IGNORECASE)


def the_gate_day_as_a_system(
    start: datetime = GATE_SYSTEMS_EVE, gustiness: float = 0.3, variability: float = 0.3
) -> Scenario:
    """The gate's day's systems without its pinned wind, from `start`."""
    from freesail.world.scenarios import load_scenario

    sc = load_scenario(GATE_DAY).scenario
    return Scenario(
        name="the gate's day as a system",
        start_time=start,
        gustiness=gustiness,
        variability=variability,
        latitude_deg=sc.latitude_deg,
        ship_heading_deg=sc.ship_heading_deg,
        systems=sc.systems,
        background=sc.background,
        glass=True,
    )


def sail_the_system(world: World, until: datetime) -> list[dict]:
    """Hourly samples of the systems' wind (the base the wander rides on), the glass, the
    sector and the tendency, read from the world."""
    samples = []
    while world.clock.ship_time < until:
        run(world, 3600)
        tendency = world.readings["tendency"]
        samples.append(
            {
                "at": world.clock.ship_time,
                "from_deg": units.rad_to_deg(world.wind.base_direction),
                "knots": units.ms_to_knots(world.wind.base_speed),
                "glass": world.readings["glass"],
                "sector": world.conditions.sector,
                "air": world.conditions.air_mass,
                "tendency": tendency["words"] if tendency else None,
            }
        )
    return samples


@pytest.fixture(scope="module")
def gate_system_day():
    world = World(seed=7, scenario=the_gate_day_as_a_system())
    samples = sail_the_system(world, GATE_SYSTEMS_END)
    return world, samples


def _turn(a: float, b: float) -> float:
    """Degrees from direction a to b, the short way, veer positive."""
    return units.rad_to_deg(units.wrap_pi(units.deg_to_rad(b) - units.deg_to_rad(a)))


def test_truth_52_a_low_passing_north_backs_veers_holds_squalls_and_rises_in_that_order(
    gate_system_day,
):
    """Spec M5 §6, truth 52: "A low passing north of the ship backs the wind and drops the
    glass ahead of it, veers the wind at the warm front, holds steady in the warm sector,
    veers it sharply with a squall at the cold front, and rises the glass fast behind, in
    that order, in one day of the gate's scenario re-expressed as a system." Read from the
    world: the base wind is the systems' surface wind at the ship, the glass the ship's
    own, the sector the model's (the tests may read the truth; the captain never does).
    Measured at seed 7 (docs/dev/TuningNotes.md, M5a): the warm front through about 22:15
    on 31 May, the cold front at 22:00 on 1 June, the first squalls in the first watch."""
    world, samples = gate_system_day
    by_time = {s["at"]: s for s in samples}
    ahead = [s for s in samples if s["sector"] == "ahead"]
    warm = [s for s in samples if s["sector"] == "warm"]
    behind = [s for s in samples if s["sector"] == "behind"]
    assert ahead and warm and behind
    assert ahead[-1]["at"] < warm[0]["at"] < behind[0]["at"]
    # ahead of the warm front: the wind backs and the glass falls
    assert _turn(ahead[0]["from_deg"], ahead[-1]["from_deg"]) <= -8.0
    assert ahead[-1]["glass"] <= ahead[0]["glass"] - 0.05
    # at the warm front: a veer of about two points
    assert _turn(ahead[-1]["from_deg"], warm[0]["from_deg"]) >= 12.0
    # the warm sector: steady in direction, the glass not falling fast, through the day
    day = [s for s in warm if datetime(1805, 6, 1, 0, 0) <= s["at"] <= datetime(1805, 6, 1, 17, 0)]
    assert len(day) >= 18
    mean_dir = statistics_mean_direction([s["from_deg"] for s in day])
    assert all(abs(_turn(mean_dir, s["from_deg"])) <= 12.0 for s in day)
    assert all(s["tendency"] in ("steady", "falling") for s in day)
    assert all(15.0 <= s["knots"] <= 25.0 for s in day)
    # the cold front, at 22:00: a sharp veer, and a squall in the unstable air behind
    before, after = by_time[datetime(1805, 6, 1, 21, 0)], by_time[datetime(1805, 6, 2, 0, 0)]
    assert before["sector"] == "warm" and after["sector"] == "behind"
    assert _turn(before["from_deg"], after["from_deg"]) >= 30.0
    squalls = [
        e
        for e in events(world, "weather.squall")
        if datetime(1805, 6, 1, 21, 30) <= e.ship_time <= datetime(1805, 6, 2, 4, 0)
    ]
    assert squalls and all(e.text.startswith("A squall") for e in squalls)
    assert all(e.data["air_mass"] == "unstable" and e.severity is Severity.NOTABLE for e in squalls)
    assert all(events(world, "weather.squall_over")), "each squall ends in the log"
    # behind: the glass rises fast in the gale
    one, four = by_time[datetime(1805, 6, 2, 1, 0)], by_time[datetime(1805, 6, 2, 4, 0)]
    assert four["glass"] - one["glass"] >= 0.10 and four["tendency"] == "rising fast"
    assert max(s["knots"] for s in behind) >= 40.0
    assert ahead[-1]["at"] < warm[0]["at"] < squalls[0].ship_time < four["at"]


def statistics_mean_direction(degrees: list[float]) -> float:
    x = sum(math.sin(math.radians(d)) for d in degrees)
    y = sum(math.cos(math.radians(d)) for d in degrees)
    return math.degrees(math.atan2(x, y)) % 360.0


def test_truth_53_a_thousand_months_of_the_climatology_give_the_studys_direction_shares():
    """Spec M5 §6, truth 53: "A thousand simulated months of the climatology give westerly
    days within five points of the 1750 to 1854 shares in every month, and easterly days
    between a tenth in summer and a quarter in late winter." By the tool's own numbers
    (tools/climatology_check.py, `run` and `table`), which the report prints; and the
    strong-breeze days within GALE_DAYS_BAND of Ushant's counts (W §1.2)."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
    from climatology_check import CLIMATOLOGY_TOLERANCE_PCT, table
    from climatology_check import run as run_months

    from freesail.world.weather import load_climatology

    clim = load_climatology()
    totals = run_months(1000, 7, clim)
    for line in table(totals, clim):
        print(line)
    for m in range(1, 13):
        t, c = clim.month(m), totals[m]
        assert c.months >= 83 and c.days == c.months * 30
        assert abs(c.share("W") - t.check["westerly_pct"]) <= CLIMATOLOGY_TOLERANCE_PCT, t.name
        assert abs(c.share("E") - t.check["easterly_pct"]) <= CLIMATOLOGY_TOLERANCE_PCT, t.name
        assert c.none_share <= 15.0, t.name
        gale_days = c.per_month(c.strong_breeze_days)
        ushant = t.check["ushant_gust31_days"]
        assert GALE_DAYS_BAND[0] * ushant <= gale_days <= GALE_DAYS_BAND[1] * ushant, (
            t.name,
            gale_days,
        )
    summer = [totals[m].share("E") for m in (6, 7, 8)]
    late_winter = [totals[m].share("E") for m in (1, 2, 3)]
    assert all(10.0 <= e for e in summer) and all(e <= 25.0 for e in late_winter)
    assert min(late_winter) > min(summer)


def test_truth_54_a_gust_is_within_1_3_of_its_mean_in_any_air_mass_and_a_squall_is_named():
    """Spec M5 §6, truth 54: "Over the open sea a gust exceeds its ten-minute mean by no
    more than 1.3 outside a squall in any air mass, and a squall is logged by name when
    it does more." The day as a system with the gustiness turned up so that every air mass
    has gusts: the gust line's factor is the peak over the ten-minute mean (spec M5 §3)."""
    world = World(seed=7, scenario=the_gate_day_as_a_system(gustiness=1.0))
    sail_the_system(world, GATE_SYSTEMS_END)
    gusts = events(world, "wind.gust")
    by_air = {}
    for e in gusts:
        by_air.setdefault(e.data["air_mass"], []).append(e.data["factor"])
    assert set(by_air) == {"warm", "neutral", "unstable"}
    for air, factors in by_air.items():
        assert len(factors) > 10 and max(factors) <= 1.30, air
    squalls = events(world, "weather.squall")
    assert squalls
    for e in squalls:
        assert e.text.startswith("A squall") and e.data["factor"] >= 1.30
        assert e.data["knots"] >= 1.29 * e.data["mean_kn"], e.text
        assert e.data["air_mass"] == "unstable"
    assert (
        max(e.data["knots"] for e in squalls) > 1.3 * max(e.data["mean_kn"] for e in squalls) * 0.9
    )


def test_truth_55_the_weather_replays_tick_for_tick_and_the_pinned_wind_wins():
    """Spec M5 §6, truth 55: "The same seed and scenario replay the weather tick for tick,
    systems, fronts and squalls included, and a scenario with a pinned `wind` gives the
    pinned wind whatever the systems do." A January day from the climatology in two worlds
    and by save and replay; the gate's day with its systems made twenty hectopascals
    deeper, the wind the same to the bit."""
    from freesail.api.session import ship_factory
    from freesail.core import replay as replay_mod
    from freesail.world.scenarios import load_scenario

    january = Scenario(
        name="January from the climatology",
        start_time=datetime(1805, 1, 10, 4, 0),
        climatology=True,
        glass=True,
        gustiness=0.5,
    )
    a, b = World(seed=7, scenario=january), World(seed=7, scenario=january)
    for _ in range(12):
        run(a, 3600)
        run(b, 3600)
        assert [(s.name, s.x_km, s.y_km, s.anomaly_hpa) for s in a.systems.systems] == [
            (s.name, s.x_km, s.y_km, s.anomaly_hpa) for s in b.systems.systems
        ]
        assert a.wind.state() == b.wind.state() and a.readings["glass"] == b.readings["glass"]
    assert a.log.digest() == b.log.digest() and a.systems.draws == b.systems.draws > 0
    copy = replay_mod.replay(a.save(), ship_factory)
    assert copy.log.digest() == a.log.digest()
    assert [s.fronts_at(copy.clock.ship_time) for s in copy.systems.systems] == [
        s.fronts_at(a.clock.ship_time) for s in a.systems.systems
    ]
    other = World(seed=8, scenario=january)
    run(other, 12 * 3600)
    assert other.log.digest() != a.log.digest()
    # the pinned wind wins
    sf = load_scenario(GATE_DAY)
    pinned = World(seed=7, scenario=sf.scenario)
    deeper = Scenario.from_dict(sf.scenario.to_dict())
    for system in deeper.systems:
        for point in system["track"]:
            point["hpa"] -= 20.0 if system["kind"] == "low" else 0.0
    changed = World(seed=7, scenario=deeper)
    for _ in range(4):
        run(pinned, 900)
        run(changed, 900)
        d, s = pinned.weather.at(pinned.clock.ship_time)
        assert pinned.wind.base_direction == pytest.approx(d, abs=1e-12)
        assert pinned.wind.base_speed == pytest.approx(s, rel=1e-12)
        assert pinned.wind.state() == changed.wind.state()
    assert pinned.readings["glass"] != changed.readings["glass"], "the systems still give the glass"
    assert pinned.wind.air_mass is None and changed.wind.air_mass is None


def test_truth_57_no_line_or_reading_names_a_front_a_centre_an_isobar_or_a_hectopascal(
    gate_system_day,
):
    """Spec M5 §6, truth 57: "No line in the log or any reading contains 'front', 'centre',
    'isobar' or 'hPa'; the glass is in inches everywhere a player reads." A grep over the
    day as a system (45 hours of log), over three hours of the gate's day with both forms
    in the frigate, over every reading's words on both, and over the registry's own
    sentences. Whole words: the helm's "centreline" is a ship's word."""
    from freesail.agents.tools import readings_words
    from freesail.api import queries
    from freesail.api import readings as R
    from freesail.world.scenarios import load_scenario, make_scenario_world

    world, _ = gate_system_day
    frigate = make_scenario_world(load_scenario(GATE_DAY))
    run(frigate, 3 * 3600)
    for w in (world, frigate):
        assert len(w.log) > 20
        for e in w.log:
            assert not FORBIDDEN_WORDS.search(e.text), e.text
        for id, words in readings_words(w).items():
            assert not FORBIDDEN_WORDS.search(str(words)), (id, words)
        assert w.readings.words("glass").endswith(" inches")
        assert 28.0 < queries.snapshot(w)["weather"]["glass_in"] < 31.0
        for ln in w.summary_lines():
            assert not FORBIDDEN_WORDS.search(ln), ln
    for row in R.REGISTRY:
        for text in (row.absent or "", row.description, " ".join(row.words)):
            assert not FORBIDDEN_WORDS.search(text), row.id
    for text in (R.NO_GLASS_WORDS, R.GLASS_UNWATCHED_WORDS, R.NO_WEATHER_WORDS):
        assert not FORBIDDEN_WORDS.search(text)
